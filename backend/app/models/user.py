from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    
    parental_consent = Column(Boolean, default=False, nullable=False)
    parent_email = Column(String(255), nullable=True)
    
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    profile_color = Column(String(7), default="#6366f1")
    avatar_emoji = Column(String(10), default="😊")
    
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    mood_entries = relationship("MoodEntry", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")
    reports = relationship("BullyingReport", back_populates="user")
    progress = relationship("UserProgress", back_populates="user")
    stories = relationship("CommunityStory", back_populates="user")
    story_votes = relationship("StoryVote", back_populates="user")
    emergency_contacts = relationship("EmergencyContact", back_populates="user")
    notifications = relationship("NotificationLog", back_populates="user")