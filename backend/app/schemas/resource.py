from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ResourceType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    WORKSHEET = "worksheet"

class ResourceCategory(str, Enum):
    PREVENTION = "prevention"
    COPING = "coping"
    REPORTING = "reporting"
    HEALING = "healing"
    PARENTS = "parents"

class LearningResourceBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10, max_length=1000)
    resource_type: ResourceType
    category: ResourceCategory
    
    min_age: int = Field(default=7, ge=7, le=16)
    max_age: int = Field(default=16, ge=7, le=16)
    
    duration_minutes: Optional[int] = Field(None, ge=1, le=480)
    difficulty_level: int = Field(default=1, ge=1, le=5)
    
    tags: Optional[List[str]] = None
    external_url: Optional[HttpUrl] = None

class LearningResourceResponse(LearningResourceBase):
    id: int
    content: str
    is_published: bool
    view_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LearningResource(LearningResourceResponse):
    pass

class UserProgressBase(BaseModel):
    progress_percentage: int = Field(default=0, ge=0, le=100)
    notes: Optional[str] = Field(None, max_length=1000)
    rating: Optional[int] = Field(None, ge=1, le=5)

class UserProgressCreate(UserProgressBase):
    resource_id: int

class UserProgressResponse(UserProgressBase):
    id: int
    user_id: int
    resource_id: int
    is_completed: bool
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProgress(UserProgressResponse):
    resource: Optional[LearningResource] = None