from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class PlatformAccount(Base):
    __tablename__ = "platform_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform_id = Column(String, nullable=False)  # e.g., "openai_free", "gemini_free"
    account_identifier = Column(String, nullable=True)  # email or username
    encrypted_api_key = Column(Text, nullable=False)  # Fernet encrypted
    is_verified = Column(Boolean, default=False)
    last_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="platform_accounts")
    quotas = relationship("Quota", back_populates="account", cascade="all, delete-orphan")
    usage_logs = relationship("UsageLog", back_populates="account", cascade="all, delete-orphan")
