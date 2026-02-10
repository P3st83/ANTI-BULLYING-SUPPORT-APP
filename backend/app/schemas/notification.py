from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ContactRelationship(str, Enum):
    PARENT = "parent"
    GUARDIAN = "guardian"
    TEACHER = "teacher"
    COUNSELOR = "counselor"
    FAMILY_FRIEND = "family_friend"
    OTHER = "other"

class NotificationType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    EMERGENCY_CALL = "emergency_call"

class NotificationStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"

class EmergencyContactBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    relationship: ContactRelationship
    phone_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    is_primary: bool = False
    notes: Optional[str] = Field(None, max_length=500)

class EmergencyContactCreate(EmergencyContactBase):
    pass

class EmergencyContact(EmergencyContactBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationLogBase(BaseModel):
    notification_type: NotificationType
    recipient: str = Field(..., min_length=1, max_length=255)
    subject: Optional[str] = Field(None, max_length=255)
    content: str = Field(..., min_length=1)
    trigger_event: Optional[str] = Field(None, max_length=100)

class NotificationLogResponse(NotificationLogBase):
    id: int
    user_id: int
    status: NotificationStatus
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    error_message: Optional[str]
    retry_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotificationLog(NotificationLogResponse):
    pass