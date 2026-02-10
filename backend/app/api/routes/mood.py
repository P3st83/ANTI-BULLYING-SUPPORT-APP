from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, date

router = APIRouter()

class MoodEntry(BaseModel):
    id: Optional[str] = None
    user_id: str
    mood: str  # happy, sad, angry, anxious, calm, excited, confused, scared
    intensity: int  # 1-5 scale
    notes: Optional[str] = None
    date: str
    created_at: Optional[str] = None

class MoodStats(BaseModel):
    total_entries: int
    current_streak: int
    average_mood_intensity: float
    most_common_mood: str
    trend: str  # improving, declining, stable

# Mock mood data storage
mock_mood_entries = []

@router.post("/entries", response_model=MoodEntry)
async def create_mood_entry(entry: MoodEntry):
    """Create a new mood entry for the user."""
    
    # Validate mood type
    valid_moods = ["happy", "sad", "angry", "anxious", "calm", "excited", "confused", "scared"]
    if entry.mood not in valid_moods:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mood. Must be one of: {', '.join(valid_moods)}"
        )
    
    # Validate intensity
    if entry.intensity < 1 or entry.intensity > 5:
        raise HTTPException(
            status_code=400,
            detail="Intensity must be between 1 and 5"
        )
    
    # Check if user already has an entry for today
    today = date.today().isoformat()
    existing_entry = next(
        (e for e in mock_mood_entries 
         if e["user_id"] == entry.user_id and e["date"].split("T")[0] == today),
        None
    )
    
    if existing_entry:
        # Update existing entry
        existing_entry.update({
            "mood": entry.mood,
            "intensity": entry.intensity,
            "notes": entry.notes,
        })
        return MoodEntry(**existing_entry)
    
    # Create new entry
    entry_dict = {
        "id": f"mood_{len(mock_mood_entries) + 1}",
        "user_id": entry.user_id,
        "mood": entry.mood,
        "intensity": entry.intensity,
        "notes": entry.notes,
        "date": entry.date,
        "created_at": datetime.now().isoformat()
    }
    
    mock_mood_entries.append(entry_dict)
    return MoodEntry(**entry_dict)

@router.get("/entries", response_model=List[MoodEntry])
async def get_mood_entries(user_id: str, limit: int = 30):
    """Get mood entries for a user."""
    
    user_entries = [
        entry for entry in mock_mood_entries 
        if entry["user_id"] == user_id
    ]
    
    # Sort by date descending
    user_entries.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [MoodEntry(**entry) for entry in user_entries[:limit]]

@router.get("/stats", response_model=MoodStats)
async def get_mood_stats(user_id: str):
    """Get mood tracking statistics for a user."""
    
    user_entries = [
        entry for entry in mock_mood_entries 
        if entry["user_id"] == user_id
    ]
    
    if not user_entries:
        return MoodStats(
            total_entries=0,
            current_streak=0,
            average_mood_intensity=0.0,
            most_common_mood="",
            trend="stable"
        )
    
    # Calculate stats
    total_entries = len(user_entries)
    
    # Calculate average intensity
    avg_intensity = sum(entry["intensity"] for entry in user_entries) / total_entries
    
    # Find most common mood
    mood_counts = {}
    for entry in user_entries:
        mood_counts[entry["mood"]] = mood_counts.get(entry["mood"], 0) + 1
    
    most_common_mood = max(mood_counts, key=mood_counts.get) if mood_counts else ""
    
    # Calculate streak (simplified)
    current_streak = calculate_streak(user_entries)
    
    # Calculate trend (simplified)
    trend = calculate_trend(user_entries)
    
    return MoodStats(
        total_entries=total_entries,
        current_streak=current_streak,
        average_mood_intensity=round(avg_intensity, 1),
        most_common_mood=most_common_mood,
        trend=trend
    )

@router.get("/today")
async def get_today_mood(user_id: str):
    """Get today's mood entry for a user."""
    
    today = date.today().isoformat()
    
    today_entry = next(
        (entry for entry in mock_mood_entries 
         if entry["user_id"] == user_id and entry["date"].split("T")[0] == today),
        None
    )
    
    if today_entry:
        return MoodEntry(**today_entry)
    
    return None

def calculate_streak(entries: List[dict]) -> int:
    """Calculate current consecutive days streak."""
    
    if not entries:
        return 0
    
    # Sort entries by date
    sorted_entries = sorted(entries, key=lambda x: x["date"], reverse=True)
    
    streak = 0
    current_date = date.today()
    
    for entry in sorted_entries:
        entry_date = datetime.fromisoformat(entry["date"]).date()
        
        if entry_date == current_date:
            streak += 1
            current_date = current_date.replace(day=current_date.day - 1)
        else:
            break
    
    return streak

def calculate_trend(entries: List[dict]) -> str:
    """Calculate mood trend over recent entries."""
    
    if len(entries) < 4:
        return "stable"
    
    # Get recent entries (last 7 days vs previous 7 days)
    sorted_entries = sorted(entries, key=lambda x: x["date"], reverse=True)
    
    recent_entries = sorted_entries[:7]
    older_entries = sorted_entries[7:14] if len(sorted_entries) >= 14 else []
    
    if not older_entries:
        return "stable"
    
    recent_avg = sum(entry["intensity"] for entry in recent_entries) / len(recent_entries)
    older_avg = sum(entry["intensity"] for entry in older_entries) / len(older_entries)
    
    difference = recent_avg - older_avg
    
    if difference > 0.5:
        return "improving"
    elif difference < -0.5:
        return "declining"
    else:
        return "stable"