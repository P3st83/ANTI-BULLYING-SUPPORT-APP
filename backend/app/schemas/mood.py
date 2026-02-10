from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum

class MoodType(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    ANXIOUS = "anxious"
    EXCITED = "excited"
    CALM = "calm"
    FRUSTRATED = "frustrated"
    CONFIDENT = "confident"

class MoodEntryBase(BaseModel):
    mood_type: MoodType
    intensity: int = Field(..., ge=1, le=5)
    activities: Optional[List[str]] = None
    notes: Optional[str] = Field(None, max_length=1000)

class MoodEntryCreate(MoodEntryBase):
    date: Optional[date] = None
    
    @validator('date', pre=True, always=True)
    def set_date(cls, v):
        return v or date.today()

class MoodEntryResponse(MoodEntryBase):
    id: int
    user_id: int
    date: date
    created_at: datetime
    
    class Config:
        from_attributes = True

class MoodEntry(MoodEntryResponse):
    pass

class MoodStats(BaseModel):
    total_entries: int
    current_streak: int
    longest_streak: int
    average_mood_score: float
    most_common_mood: str
    mood_distribution: Dict[str, int]
    recent_trend: str  # "improving", "stable", "declining"
    weekly_scores: List[float]