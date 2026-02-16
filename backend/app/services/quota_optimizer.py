from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.platform_account import PlatformAccount
from app.models.quota import Quota
from app.services.quota_tracker import quota_tracker


class QuotaOptimizer:
    """Service for optimizing quota usage and generating recommendations"""
    
    def calculate_urgency_score(self, quota_info: Dict) -> float:
        """
        Calculate urgency score based on:
        1. Time until reset (shorter = higher priority)
        2. Remaining quota (more remaining = higher priority)
        3. Current usage rate
        """
        now = datetime.utcnow()
        reset_at = quota_info["reset_at"]
        
        if isinstance(reset_at, str):
            reset_at = datetime.fromisoformat(reset_at.replace('Z', '+00:00'))
        
        time_until_reset = (reset_at - now).total_seconds() / 3600  # hours
        remaining_quota = quota_info["remaining_quota"]
        total_quota = quota_info["total_quota"]
        
        # Avoid division by zero
        if time_until_reset <= 0:
            return 0.0
        
        if total_quota <= 0:
            return 0.0
        
        # Urgency increases with:
        # - Less time until reset
        # - More remaining quota
        remaining_percentage = remaining_quota / total_quota
        time_factor = max(0, 1 - (time_until_reset / 24))  # Normalize to 0-1
        
        urgency_score = (remaining_percentage * 0.6) + (time_factor * 0.4)
        
        return round(urgency_score * 100, 2)
    
    def predict_waste(self, quota_info: Dict, usage_history: List[Dict]) -> bool:
        """Predict if quota will be wasted based on current usage rate"""
        if not usage_history:
            return False
        
        remaining = quota_info["remaining_quota"]
        time_until_reset = (quota_info["reset_at"] - datetime.utcnow()).total_seconds() / 3600
        
        if time_until_reset <= 0:
            return False
        
        # Calculate average usage rate (simple approach)
        if len(usage_history) >= 2:
            recent_usage = sum(log.get("amount", 0) for log in usage_history[-10:])
            hours_tracked = len(usage_history[-10:])
            avg_rate = recent_usage / max(hours_tracked, 1)
            
            predicted_usage = avg_rate * time_until_reset
            
            # If predicted usage is less than 50% of remaining, flag as potential waste
            if predicted_usage < (remaining * 0.5):
                return True
        
        return False
    
    async def get_recommendations(self, db: AsyncSession, user_id: int) -> Dict:
        """Get platform recommendations for optimal quota usage"""
        # Get all user's accounts
        result = await db.execute(
            select(PlatformAccount).where(PlatformAccount.user_id == user_id)
        )
        accounts = result.scalars().all()
        
        if not accounts:
            return {
                "recommended_platform": None,
                "reason": "No connected accounts found. Please connect your AI platform accounts first.",
                "alternatives": []
            }
        
        # Collect quota info for all accounts
        platform_scores = []
        
        for account in accounts:
            quotas = await quota_tracker.get_quota_status(db, account.id)
            if not quotas:
                continue
            
            platform_info = quota_tracker.get_platform_info(account.platform_id)
            if not platform_info:
                continue
            
            # Calculate average urgency across all quotas
            urgency_scores = []
            for quota in quotas:
                score = self.calculate_urgency_score(quota)
                urgency_scores.append(score)
            
            avg_urgency = sum(urgency_scores) / len(urgency_scores) if urgency_scores else 0
            
            # Find the most urgent quota
            most_urgent_quota = max(quotas, key=lambda q: self.calculate_urgency_score(q))
            time_until_reset = (most_urgent_quota["reset_at"] - datetime.utcnow())
            
            platform_scores.append({
                "platform_id": account.platform_id,
                "platform_name": platform_info["name"],
                "account_id": account.id,
                "quotas": quotas,
                "urgency_score": avg_urgency,
                "time_until_reset": self._format_timedelta(time_until_reset),
                "most_urgent_quota": most_urgent_quota
            })
        
        # Sort by urgency score
        platform_scores.sort(key=lambda x: x["urgency_score"], reverse=True)
        
        if not platform_scores:
            return {
                "recommended_platform": None,
                "reason": "No quota information available.",
                "alternatives": []
            }
        
        recommended = platform_scores[0]
        
        # Generate recommendation reason
        reason = self._generate_recommendation_reason(recommended)
        
        return {
            "recommended_platform": recommended,
            "reason": reason,
            "alternatives": platform_scores[1:4]  # Top 3 alternatives
        }
    
    def _generate_recommendation_reason(self, platform_info: Dict) -> str:
        """Generate human-readable recommendation reason"""
        quota = platform_info["most_urgent_quota"]
        remaining_pct = quota["remaining_quota"] / quota["total_quota"] * 100 if quota["total_quota"] > 0 else 0
        
        reasons = []
        
        if remaining_pct > 70:
            reasons.append(f"{remaining_pct:.0f}% quota remaining")
        
        if platform_info["urgency_score"] > 70:
            reasons.append(f"resets in {platform_info['time_until_reset']}")
        
        if remaining_pct > 50 and platform_info["urgency_score"] > 50:
            reasons.append("high risk of quota waste")
        
        if reasons:
            return f"Recommended: {', '.join(reasons)}"
        
        return "Best available option based on current quota status"
    
    def _format_timedelta(self, td: timedelta) -> str:
        """Format timedelta to human-readable string"""
        total_seconds = int(td.total_seconds())
        
        if total_seconds < 0:
            return "expired"
        
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 24:
            days = hours // 24
            return f"{days} day{'s' if days != 1 else ''}"
        elif hours > 0:
            return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            return f"{minutes} minute{'s' if minutes != 1 else ''}"
    
    async def generate_daily_schedule(self, db: AsyncSession, user_id: int) -> List[Dict]:
        """Generate optimal daily usage schedule"""
        recommendations = await self.get_recommendations(db, user_id)
        
        schedule = []
        platforms = [recommendations.get("recommended_platform")]
        platforms.extend(recommendations.get("alternatives", []))
        platforms = [p for p in platforms if p is not None]
        
        # Distribute platforms across the day
        time_slots = [
            "Morning (6-9 AM)",
            "Late Morning (9-12 PM)",
            "Afternoon (12-3 PM)",
            "Late Afternoon (3-6 PM)",
            "Evening (6-9 PM)",
            "Night (9-12 AM)"
        ]
        
        for i, platform in enumerate(platforms[:len(time_slots)]):
            schedule.append({
                "time_slot": time_slots[i],
                "platform_id": platform["platform_id"],
                "platform_name": platform["platform_name"],
                "action": "Use available quota",
                "reason": f"Urgency score: {platform['urgency_score']:.0f}"
            })
        
        return schedule


# Singleton instance
quota_optimizer = QuotaOptimizer()
