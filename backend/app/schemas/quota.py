from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PlatformQuotaInfo(BaseModel):
    platform_id: str
    platform_name: str
    account_id: Optional[int]
    quotas: List[dict]
    urgency_score: float
    recommendation: str
    time_until_reset: Optional[str]


class DashboardResponse(BaseModel):
    total_platforms: int
    connected_accounts: int
    total_quota_usage_percentage: float
    platforms: List[PlatformQuotaInfo]
    last_updated: datetime


class RecommendationResponse(BaseModel):
    recommended_platform: Optional[PlatformQuotaInfo]
    reason: str
    alternatives: List[PlatformQuotaInfo]


class ScheduleItem(BaseModel):
    time_slot: str
    platform_id: str
    platform_name: str
    action: str
    reason: str


class ScheduleResponse(BaseModel):
    schedule_type: str  # "daily" or "weekly"
    schedule: List[ScheduleItem]
    generated_at: datetime
