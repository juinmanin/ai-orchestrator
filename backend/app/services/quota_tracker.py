from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.quota import Quota
from app.models.platform_account import PlatformAccount
import json


class QuotaTracker:
    """Service for tracking and updating quota usage"""
    
    def __init__(self):
        self.platform_data = self._load_platform_data()
    
    def _load_platform_data(self) -> Dict:
        """Load platform quota information"""
        try:
            with open("/app/app/data/platform_quotas.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default data if file doesn't exist
            return {
                "platforms": [
                    {
                        "id": "openai_free",
                        "name": "ChatGPT Free",
                        "quotas": [
                            {"type": "3hour", "limit": 50, "reset_hours": 3, "unit": "messages"}
                        ]
                    },
                    {
                        "id": "gemini_free",
                        "name": "Gemini Free",
                        "quotas": [
                            {"type": "minute", "limit": 60, "reset_hours": 0.0166, "unit": "requests"},
                            {"type": "daily", "limit": 1500, "reset_hours": 24, "unit": "requests"}
                        ]
                    },
                    {
                        "id": "claude_free",
                        "name": "Claude Free",
                        "quotas": [
                            {"type": "daily", "limit": 30, "reset_hours": 24, "unit": "messages"}
                        ]
                    },
                    {
                        "id": "leonardo_free",
                        "name": "Leonardo AI Free",
                        "quotas": [
                            {"type": "daily", "limit": 150, "reset_hours": 24, "unit": "tokens"}
                        ]
                    },
                    {
                        "id": "huggingface_free",
                        "name": "Hugging Face Free",
                        "quotas": [
                            {"type": "monthly", "limit": 1000, "reset_hours": 720, "unit": "requests"}
                        ]
                    },
                    {
                        "id": "cohere_free",
                        "name": "Cohere Free",
                        "quotas": [
                            {"type": "monthly", "limit": 1000, "reset_hours": 720, "unit": "calls"}
                        ]
                    }
                ]
            }
    
    def get_platform_info(self, platform_id: str) -> Optional[Dict]:
        """Get platform information by ID"""
        for platform in self.platform_data.get("platforms", []):
            if platform["id"] == platform_id:
                return platform
        return None
    
    async def initialize_quotas(self, db: AsyncSession, account_id: int, platform_id: str):
        """Initialize quota records for a new account"""
        platform_info = self.get_platform_info(platform_id)
        if not platform_info:
            return
        
        for quota_info in platform_info.get("quotas", []):
            reset_at = datetime.utcnow() + timedelta(hours=quota_info["reset_hours"])
            quota = Quota(
                account_id=account_id,
                quota_type=quota_info["type"],
                total_quota=float(quota_info["limit"]),
                used_quota=0.0,
                reset_at=reset_at
            )
            db.add(quota)
        
        await db.commit()
    
    async def update_usage(self, db: AsyncSession, account_id: int, amount: float):
        """Update quota usage for an account"""
        result = await db.execute(
            select(Quota).where(Quota.account_id == account_id)
        )
        quotas = result.scalars().all()
        
        for quota in quotas:
            # Check if quota needs reset
            if datetime.utcnow() >= quota.reset_at:
                await self.reset_quota(db, quota)
            
            # Update usage
            quota.used_quota += amount
        
        await db.commit()
    
    async def reset_quota(self, db: AsyncSession, quota: Quota):
        """Reset quota to initial values"""
        result = await db.execute(
            select(PlatformAccount).where(PlatformAccount.id == quota.account_id)
        )
        account = result.scalar_one_or_none()
        if not account:
            return
        
        platform_info = self.get_platform_info(account.platform_id)
        if not platform_info:
            return
        
        for quota_info in platform_info.get("quotas", []):
            if quota_info["type"] == quota.quota_type:
                quota.used_quota = 0.0
                quota.reset_at = datetime.utcnow() + timedelta(hours=quota_info["reset_hours"])
                break
        
        await db.commit()
    
    async def get_quota_status(self, db: AsyncSession, account_id: int) -> List[Dict]:
        """Get current quota status for an account"""
        result = await db.execute(
            select(Quota).where(Quota.account_id == account_id)
        )
        quotas = result.scalars().all()
        
        status = []
        for quota in quotas:
            # Auto-reset if needed
            if datetime.utcnow() >= quota.reset_at:
                await self.reset_quota(db, quota)
            
            remaining = max(0, quota.total_quota - quota.used_quota)
            percentage = (quota.used_quota / quota.total_quota * 100) if quota.total_quota > 0 else 0
            
            status.append({
                "quota_type": quota.quota_type,
                "total_quota": quota.total_quota,
                "used_quota": quota.used_quota,
                "remaining_quota": remaining,
                "reset_at": quota.reset_at,
                "usage_percentage": round(percentage, 2)
            })
        
        return status


# Singleton instance
quota_tracker = QuotaTracker()
