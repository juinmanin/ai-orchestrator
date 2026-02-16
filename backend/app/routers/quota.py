from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.routers.auth import get_current_user
from app.schemas.quota import DashboardResponse, RecommendationResponse, ScheduleResponse, PlatformQuotaInfo, ScheduleItem
from app.services.quota_tracker import quota_tracker
from app.services.quota_optimizer import quota_optimizer
from sqlalchemy import select
from app.models.platform_account import PlatformAccount

router = APIRouter(prefix="/api/quota", tags=["Quota"])


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get complete quota dashboard"""
    # Get all user's accounts
    result = await db.execute(
        select(PlatformAccount).where(PlatformAccount.user_id == current_user.id)
    )
    accounts = result.scalars().all()
    
    platforms = []
    total_usage = 0
    total_quotas = 0
    
    for account in accounts:
        platform_info = quota_tracker.get_platform_info(account.platform_id)
        if not platform_info:
            continue
        
        quotas = await quota_tracker.get_quota_status(db, account.id)
        
        # Calculate urgency score
        if quotas:
            avg_urgency = sum(
                quota_optimizer.calculate_urgency_score(q) for q in quotas
            ) / len(quotas)
            
            # Find most urgent quota for time display
            most_urgent = max(quotas, key=lambda q: quota_optimizer.calculate_urgency_score(q))
            time_until_reset = quota_optimizer._format_timedelta(
                most_urgent["reset_at"] - datetime.utcnow()
            )
            
            # Calculate recommendation
            recommendation = "Use now" if avg_urgency > 70 else "Available" if avg_urgency > 30 else "Low priority"
        else:
            avg_urgency = 0
            time_until_reset = "N/A"
            recommendation = "No quota data"
        
        # Aggregate usage
        for quota in quotas:
            total_usage += quota["used_quota"]
            total_quotas += quota["total_quota"]
        
        platforms.append(PlatformQuotaInfo(
            platform_id=account.platform_id,
            platform_name=platform_info["name"],
            account_id=account.id,
            quotas=quotas,
            urgency_score=avg_urgency,
            recommendation=recommendation,
            time_until_reset=time_until_reset
        ))
    
    # Calculate overall usage percentage
    overall_percentage = (total_usage / total_quotas * 100) if total_quotas > 0 else 0
    
    # Get all supported platforms count
    all_platforms = quota_tracker.platform_data.get("platforms", [])
    
    return DashboardResponse(
        total_platforms=len(all_platforms),
        connected_accounts=len(accounts),
        total_quota_usage_percentage=round(overall_percentage, 2),
        platforms=platforms,
        last_updated=datetime.utcnow()
    )


@router.get("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get platform recommendations for optimal usage"""
    recommendations = await quota_optimizer.get_recommendations(db, current_user.id)
    
    return RecommendationResponse(
        recommended_platform=recommendations.get("recommended_platform"),
        reason=recommendations.get("reason", ""),
        alternatives=recommendations.get("alternatives", [])
    )


@router.get("/schedule", response_model=ScheduleResponse)
async def get_schedule(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get optimal daily usage schedule"""
    schedule = await quota_optimizer.generate_daily_schedule(db, current_user.id)
    
    schedule_items = [ScheduleItem(**item) for item in schedule]
    
    return ScheduleResponse(
        schedule_type="daily",
        schedule=schedule_items,
        generated_at=datetime.utcnow()
    )


@router.get("/{account_id}")
async def get_account_quota(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed quota information for a specific account"""
    result = await db.execute(
        select(PlatformAccount).where(
            PlatformAccount.id == account_id,
            PlatformAccount.user_id == current_user.id
        )
    )
    account = result.scalar_one_or_none()
    
    if not account:
        return {"error": "Account not found"}
    
    platform_info = quota_tracker.get_platform_info(account.platform_id)
    quotas = await quota_tracker.get_quota_status(db, account.id)
    
    return {
        "platform_id": account.platform_id,
        "platform_name": platform_info["name"] if platform_info else "Unknown",
        "quotas": quotas,
        "account_id": account.id
    }
