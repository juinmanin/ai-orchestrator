from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AccountCreate(BaseModel):
    platform_id: str
    account_identifier: Optional[str] = None
    api_key: str


class AccountUpdate(BaseModel):
    account_identifier: Optional[str] = None
    api_key: Optional[str] = None


class QuotaInfo(BaseModel):
    quota_type: str
    total_quota: float
    used_quota: float
    remaining_quota: float
    reset_at: datetime
    usage_percentage: float
    
    class Config:
        from_attributes = True


class AccountResponse(BaseModel):
    id: int
    platform_id: str
    account_identifier: Optional[str]
    api_key_preview: str  # masked: "sk-...xxxx"
    is_verified: bool
    last_verified_at: Optional[datetime]
    created_at: datetime
    quotas: Optional[list[QuotaInfo]] = []
    
    class Config:
        from_attributes = True


class AccountVerifyResponse(BaseModel):
    success: bool
    message: str
    details: Optional[dict] = None
