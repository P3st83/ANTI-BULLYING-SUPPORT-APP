from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    role: MessageRole

class ChatMessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime
    is_emergency: bool
    contains_personal_info: bool
    safety_flags: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

class ChatMessage(ChatMessageResponse):
    pass

class ChatSessionBase(BaseModel):
    title: Optional[str] = Field(None, max_length=255)

class ChatSessionResponse(ChatSessionBase):
    id: int
    user_id: int
    is_active: bool
    last_activity: Optional[datetime]
    created_at: datetime
    message_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ChatSession(ChatSessionResponse):
    messages: Optional[List[ChatMessage]] = []