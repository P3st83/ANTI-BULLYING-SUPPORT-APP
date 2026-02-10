from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=7, le=16)
    
    profile_color: str = Field(default="#6366f1", pattern=r"^#[0-9A-Fa-f]{6}$")
    avatar_emoji: str = Field(default="😊", max_length=10)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    parent_email: Optional[EmailStr] = None
    
    @validator('parent_email')
    def validate_parental_consent(cls, v, values):
        if 'age' in values and values['age'] < 13 and not v:
            raise ValueError('Parental email required for users under 13')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    profile_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    avatar_emoji: Optional[str] = Field(None, max_length=10)

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    parental_consent: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class User(UserResponse):
    pass