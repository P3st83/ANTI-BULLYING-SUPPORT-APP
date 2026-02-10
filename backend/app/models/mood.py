from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class MoodEntry(Base, TimestampMixin):
    __tablename__ = "mood_entries"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    
    mood_type = Column(String(20), nullable=False)  # happy, sad, angry, anxious, etc.
    intensity = Column(Integer, nullable=False)  # 1-5 scale
    
    activities = Column(Text, nullable=True)  # JSON array of activities
    notes = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="mood_entries")
    
    __table_args__ = (
        {"schema": None}
    )