from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base, TimestampMixin

class ContactRelationship(PyEnum):
    PARENT = "parent"
    GUARDIAN = "guardian"
    TEACHER = "teacher"
    COUNSELOR = "counselor"
    FAMILY_FRIEND = "family_friend"
    OTHER = "other"

class NotificationType(PyEnum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    EMERGENCY_CALL = "emergency_call"

class NotificationStatus(PyEnum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"

class EmergencyContact(Base, TimestampMixin):
    __tablename__ = "emergency_contacts"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    name = Column(String(255), nullable=False)
    contact_relationship = Column(String(20), nullable=False)
    
    phone_number = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    
    is_primary = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    notes = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="emergency_contacts")

class NotificationLog(Base, TimestampMixin):
    __tablename__ = "notification_logs"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    notification_type = Column(String(20), nullable=False)
    status = Column(String(20), default="pending")
    
    recipient = Column(String(255), nullable=False)  # email/phone number
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    
    trigger_event = Column(String(100), nullable=True)  # e.g., "emergency_report", "mood_alert"
    
    sent_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    user = relationship("User", back_populates="notifications")