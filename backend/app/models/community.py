from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class CommunityStory(Base, TimestampMixin):
    __tablename__ = "community_stories"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)  # Nullable for anonymous stories
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    
    is_anonymous = Column(Boolean, default=True)
    author_age = Column(Integer, nullable=True)
    
    status = Column(String(20), default="pending")
    
    tags = Column(Text, nullable=True)  # JSON array
    trigger_warnings = Column(Text, nullable=True)  # JSON array
    
    upvotes = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    
    is_featured = Column(Boolean, default=False)
    moderation_notes = Column(Text, nullable=True)
    
    approved_at = Column(DateTime(timezone=True), nullable=True)
    
    user = relationship("User", back_populates="stories")
    votes = relationship("StoryVote", back_populates="story", cascade="all, delete-orphan")

class StoryVote(Base, TimestampMixin):
    __tablename__ = "story_votes"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    story_id = Column(Integer, ForeignKey("community_stories.id"), nullable=False, index=True)
    
    is_upvote = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="story_votes")
    story = relationship("CommunityStory", back_populates="votes")