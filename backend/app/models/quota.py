from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Quota(Base):
    __tablename__ = "quotas"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("platform_accounts.id"), nullable=False)
    quota_type = Column(String, nullable=False)  # "hourly", "daily", "monthly"
    total_quota = Column(Float, nullable=False)
    used_quota = Column(Float, default=0.0)
    reset_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    account = relationship("PlatformAccount", back_populates="quotas")
