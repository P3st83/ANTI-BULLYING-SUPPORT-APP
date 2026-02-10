from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class CommunityStory(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    author_age: int
    is_anonymous: bool
    author_name: Optional[str] = None
    upvotes: int = 0
    is_moderated: bool = False
    tags: List[str] = []
    created_at: Optional[str] = None

class StoryCreate(BaseModel):
    title: str
    content: str
    author_age: int
    is_anonymous: bool = True
    author_name: Optional[str] = None
    tags: List[str] = []

# Mock community stories
mock_stories = [
    {
        "id": "story_1",
        "title": "How I Found My Confidence",
        "content": """When I started middle school, I was really shy and some kids made fun of my glasses. I felt really bad about myself and didn't want to go to school.

But then my teacher helped me join the art club, and I met other kids who liked the same things I did. We became friends and they showed me that being different is actually cool!

Now I'm proud of who I am. I still wear glasses, but I also know I'm creative, kind, and a good friend. The bullies don't bother me anymore because I have people who care about me.

To anyone going through something similar - you are amazing just the way you are! Find your people and don't let anyone dim your light. ✨""",
        "author_age": 13,
        "is_anonymous": True,
        "author_name": None,
        "upvotes": 24,
        "is_moderated": True,
        "tags": ["confidence", "friendship", "school"],
        "created_at": "2024-01-10T14:30:00Z"
    },
    {
        "id": "story_2", 
        "title": "Standing Up Made a Difference",
        "content": """I saw someone in my class being picked on every day at lunch. At first I didn't know what to do because I was scared the bullies would pick on me too.

But I remembered what we learned about being a good bystander. So I went and sat with the kid being bullied and started talking to them about video games. The bullies just walked away!

Now we're friends and we always sit together. Sometimes other kids join us too. It feels really good to help someone and make a new friend at the same time.

Even if you're scared, try to help. You might be surprised how much difference you can make! 💪""",
        "author_age": 11,
        "is_anonymous": True,
        "author_name": None,
        "upvotes": 31,
        "is_moderated": True,
        "tags": ["bystander", "friendship", "courage"],
        "created_at": "2024-01-08T16:45:00Z"
    },
    {
        "id": "story_3",
        "title": "My Family Helped Me Through It",
        "content": """When kids at school were saying mean things about me online, I was really upset and didn't want to tell anyone. I thought it would just make things worse.

But my mom noticed I was sad and asked what was wrong. When I told her, she didn't get mad or take away my phone. Instead, she helped me report it and talked to the school.

The school took it seriously and the cyberbullying stopped. My mom also helped me understand that the problem was with the bullies, not with me.

Don't be afraid to tell a trusted adult. They want to help you and they know how to handle these situations. You don't have to go through it alone! 💙""",
        "author_age": 14,
        "is_anonymous": False,
        "author_name": "Sarah",
        "upvotes": 18,
        "is_moderated": True,
        "tags": ["family-support", "cyberbullying", "school"],
        "created_at": "2024-01-05T11:20:00Z"
    }
]

@router.get("/stories", response_model=List[CommunityStory])
async def get_stories(
    limit: int = 20,
    tag: Optional[str] = None,
    moderated_only: bool = True
):
    """Get community stories with optional filtering."""
    
    filtered_stories = mock_stories
    
    if moderated_only:
        filtered_stories = [s for s in filtered_stories if s["is_moderated"]]
    
    if tag:
        filtered_stories = [s for s in filtered_stories if tag in s["tags"]]
    
    # Sort by upvotes and date
    filtered_stories.sort(key=lambda x: (x["upvotes"], x["created_at"]), reverse=True)
    
    return [CommunityStory(**story) for story in filtered_stories[:limit]]

@router.post("/stories", response_model=CommunityStory)
async def create_story(story: StoryCreate):
    """Submit a new community story."""
    
    # Content validation
    if len(story.content) < 50:
        raise HTTPException(
            status_code=400,
            detail="Story content must be at least 50 characters long"
        )
    
    if len(story.content) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Story content must be under 2000 characters"
        )
    
    # Age validation
    if story.author_age < 7 or story.author_age > 18:
        raise HTTPException(
            status_code=400,
            detail="Author age must be between 7 and 18"
        )
    
    # Create new story
    story_dict = {
        "id": f"story_{len(mock_stories) + 1}",
        "title": story.title,
        "content": story.content,
        "author_age": story.author_age,
        "is_anonymous": story.is_anonymous,
        "author_name": story.author_name if not story.is_anonymous else None,
        "upvotes": 0,
        "is_moderated": False,  # Requires moderation before appearing
        "tags": story.tags,
        "created_at": datetime.now().isoformat()
    }
    
    mock_stories.append(story_dict)
    
    return CommunityStory(**story_dict)

@router.post("/stories/{story_id}/upvote")
async def upvote_story(story_id: str, user_id: str):
    """Upvote a community story."""
    
    story = next((s for s in mock_stories if s["id"] == story_id), None)
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # In production, check if user already upvoted
    story["upvotes"] += 1
    
    return {
        "message": "Story upvoted successfully",
        "story_id": story_id,
        "total_upvotes": story["upvotes"]
    }

@router.get("/stories/{story_id}", response_model=CommunityStory)
async def get_story(story_id: str):
    """Get a specific community story."""
    
    story = next((s for s in mock_stories if s["id"] == story_id), None)
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    return CommunityStory(**story)

@router.get("/stories/tags/popular")
async def get_popular_tags():
    """Get popular story tags."""
    
    # Count tag usage
    tag_counts = {}
    for story in mock_stories:
        if story["is_moderated"]:
            for tag in story["tags"]:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # Sort by popularity
    popular_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "popular_tags": [
            {"tag": tag, "count": count} 
            for tag, count in popular_tags[:10]
        ]
    }

@router.post("/stories/{story_id}/report")
async def report_story(story_id: str, reason: str):
    """Report a story for inappropriate content."""
    
    story = next((s for s in mock_stories if s["id"] == story_id), None)
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # In production, log the report and notify moderators
    return {
        "message": "Story reported successfully. Our moderation team will review it.",
        "story_id": story_id,
        "reason": reason
    }

@router.get("/guidelines")
async def get_community_guidelines():
    """Get community guidelines for story sharing."""
    
    return {
        "title": "Community Guidelines",
        "subtitle": "Creating a safe and supportive space for everyone",
        "guidelines": [
            {
                "title": "Be Kind and Respectful",
                "description": "Treat others with kindness and respect. No mean comments or bullying."
            },
            {
                "title": "Share Positive Stories",
                "description": "Focus on stories of overcoming challenges, finding support, or helping others."
            },
            {
                "title": "Protect Privacy",
                "description": "Don't share real names, schools, or specific locations. Use anonymous or first names only."
            },
            {
                "title": "Keep It Age-Appropriate",
                "description": "Content should be suitable for ages 7-16. No inappropriate language or topics."
            },
            {
                "title": "No Personal Information",
                "description": "Never share phone numbers, addresses, social media accounts, or other personal details."
            },
            {
                "title": "Report Problems",
                "description": "If you see something that doesn't belong, report it to our moderation team."
            }
        ],
        "moderation_note": "All stories are reviewed by our moderation team before appearing on the platform to ensure they meet our community standards.",
        "support_note": "If you need immediate help or support, please use the chat feature or contact a trusted adult rather than posting in the community."
    }

@router.get("/stats")
async def get_community_stats():
    """Get community statistics."""
    
    total_stories = len([s for s in mock_stories if s["is_moderated"]])
    total_upvotes = sum(s["upvotes"] for s in mock_stories if s["is_moderated"])
    
    # Age distribution
    age_groups = {"7-10": 0, "11-13": 0, "14-16": 0, "17+": 0}
    for story in mock_stories:
        if story["is_moderated"]:
            age = story["author_age"]
            if age <= 10:
                age_groups["7-10"] += 1
            elif age <= 13:
                age_groups["11-13"] += 1
            elif age <= 16:
                age_groups["14-16"] += 1
            else:
                age_groups["17+"] += 1
    
    return {
        "total_stories": total_stories,
        "total_upvotes": total_upvotes,
        "age_distribution": age_groups,
        "anonymous_stories": len([s for s in mock_stories if s["is_anonymous"] and s["is_moderated"]]),
        "stories_this_month": len([
            s for s in mock_stories 
            if s["is_moderated"] and 
            datetime.fromisoformat(s["created_at"]).month == datetime.now().month
        ])
    }