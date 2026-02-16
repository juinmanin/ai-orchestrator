from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class UsageLog(Base):
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("platform_accounts.id"), nullable=True)
    action = Column(String, nullable=False)  # "api_call", "quota_check", "account_verify", etc.
    details = Column(Text, nullable=True)
    amount = Column(Float, default=0.0)  # quota used
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="usage_logs")
    account = relationship("PlatformAccount", back_populates="usage_logs")
