from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class StoryStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class CommunityStoryBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    content: str = Field(..., min_length=50, max_length=5000)
    is_anonymous: bool = True
    author_age: Optional[int] = Field(None, ge=7, le=16)
    tags: Optional[List[str]] = None
    trigger_warnings: Optional[List[str]] = None

class CommunityStoryCreate(CommunityStoryBase):
    pass

class CommunityStoryResponse(CommunityStoryBase):
    id: int
    user_id: Optional[int]
    status: StoryStatus
    upvotes: int
    view_count: int
    is_featured: bool
    created_at: datetime
    approved_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class CommunityStory(CommunityStoryResponse):
    pass

class StoryVoteBase(BaseModel):
    is_upvote: bool = True

class StoryVoteCreate(StoryVoteBase):
    story_id: int

class StoryVote(BaseModel):
    id: int
    user_id: int
    story_id: int
    is_upvote: bool
    created_at: datetime
    
    class Config:
        from_attributes = True