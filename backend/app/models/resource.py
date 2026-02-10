from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class LearningResource(Base, TimestampMixin):
    __tablename__ = "learning_resources"
    
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)  # Markdown content
    
    resource_type = Column(String(20), nullable=False)
    category = Column(String(20), nullable=False)
    
    min_age = Column(Integer, default=7)
    max_age = Column(Integer, default=16)
    
    duration_minutes = Column(Integer, nullable=True)
    difficulty_level = Column(Integer, default=1)  # 1-5 scale
    
    tags = Column(Text, nullable=True)  # JSON array
    external_url = Column(String(500), nullable=True)
    
    is_published = Column(Boolean, default=True)
    view_count = Column(Integer, default=0)
    
    progress = relationship("UserProgress", back_populates="resource")

class UserProgress(Base, TimestampMixin):
    __tablename__ = "user_progress"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    resource_id = Column(Integer, ForeignKey("learning_resources.id"), nullable=False, index=True)
    
    is_completed = Column(Boolean, default=False)
    progress_percentage = Column(Integer, default=0)
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    notes = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 scale
    
    user = relationship("User", back_populates="progress")
    resource = relationship("LearningResource", back_populates="progress")