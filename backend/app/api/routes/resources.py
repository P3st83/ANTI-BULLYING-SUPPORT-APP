from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class LearningResource(BaseModel):
    id: str
    title: str
    description: str
    type: str  # video, article, activity, story
    age_group: str
    category: str
    content: str
    duration: Optional[int] = None
    thumbnail_url: Optional[str] = None

# Mock learning resources
mock_resources = [
    {
        "id": "1",
        "title": "What is Bullying?",
        "description": "Learn about different types of bullying and how to recognize them.",
        "type": "article",
        "age_group": "7-12",
        "category": "bullying-prevention",
        "content": """
# What is Bullying?

Bullying is when someone repeatedly hurts, threatens, or excludes another person on purpose. It's not just physical - bullying can be:

## Types of Bullying:

### Physical Bullying 🤕
- Hitting, kicking, or pushing
- Taking or breaking someone's things
- Making someone feel unsafe

### Verbal Bullying 💬
- Name-calling or teasing
- Threatening to hurt someone
- Saying mean things about someone

### Social Bullying 👥
- Leaving someone out on purpose
- Spreading rumors or lies
- Embarrassing someone in public

### Cyberbullying 📱
- Sending mean messages online
- Sharing embarrassing photos
- Excluding someone from online groups

## Remember:
- Bullying is NEVER okay
- It's not your fault if someone bullies you
- There are always adults who can help
- You deserve to feel safe and respected

If you're being bullied, tell a trusted adult like a parent, teacher, or counselor. You don't have to face this alone! 💙
        """,
        "duration": 5,
        "thumbnail_url": ""
    },
    {
        "id": "2", 
        "title": "Standing Up for Others",
        "description": "How to safely help someone who is being bullied.",
        "type": "video",
        "age_group": "10-16",
        "category": "bystander-help",
        "content": """
# Being a Good Bystander 🦸‍♀️

When you see someone being bullied, you can make a difference! Here's how to help safely:

## Safe Ways to Help:

### During the Situation:
- Don't join in or laugh
- If it's safe, tell the bully to stop
- Get help from an adult immediately
- Stay with the person being bullied

### After the Situation:
- Check on the person who was bullied
- Listen to them and be supportive
- Help them tell a trusted adult
- Be their friend and include them

## When NOT to Get Involved:
- If there's physical violence
- If you might get hurt too
- If there are weapons involved

**In these cases, get an adult immediately!**

## What to Say:
- "That's not okay."
- "Leave them alone."
- "We don't treat people that way here."
- "Come on, let's go." (to the person being bullied)

## Remember:
- Your safety comes first
- Even small actions can make a big difference
- Speaking up shows courage and kindness
- You can help create a kinder world! ✨

Every act of kindness matters. You have the power to make someone's day better! 💖
        """,
        "duration": 8,
        "thumbnail_url": ""
    },
    {
        "id": "3",
        "title": "Building Confidence",
        "description": "Activities and tips to boost your self-confidence.",
        "type": "activity",
        "age_group": "7-16", 
        "category": "self-confidence",
        "content": """
# Building Your Confidence 💪

Confidence is like a muscle - the more you practice, the stronger it gets!

## Daily Confidence Boosters:

### Morning Affirmations 🌅
Say these to yourself every morning:
- "I am brave and strong"
- "I deserve kindness and respect"
- "I can handle whatever comes my way"
- "I am a good friend"
- "I have special talents and gifts"

### Confidence Poses 🦸‍♂️
Stand like a superhero for 2 minutes:
- Feet apart, hands on hips
- Chest out, chin up
- Breathe deeply
- Imagine you're wearing a cape!

### Success Journal 📓
Every day, write down:
- One thing you did well
- One compliment someone gave you
- One challenge you faced bravely
- One thing you're grateful for

### Kindness Practice 💝
- Help someone else
- Give a genuine compliment
- Include someone who looks lonely
- Share something you enjoy

## Confidence Building Activities:

### Try New Things 🎨
- Learn a new skill
- Join a club or activity
- Take on a small challenge
- Ask questions when curious

### Practice Speaking Up 🗣️
- Share your opinion in class
- Ask for help when you need it
- Say "no" when something doesn't feel right
- Express your feelings clearly

### Celebrate Your Uniqueness 🌟
- Make a list of what makes you special
- Share your talents with others
- Don't compare yourself to others
- Be proud of your differences

## Remember:
- Confidence grows with practice
- Everyone feels unsure sometimes
- Your worth isn't based on what others think
- You are enough, just as you are! 💙

Start with one small confidence-building activity today. You've got this! 🌈
        """,
        "duration": 10,
        "thumbnail_url": ""
    },
    {
        "id": "4",
        "title": "Managing Big Emotions",
        "description": "Learn healthy ways to cope with difficult feelings.",
        "type": "article",
        "age_group": "7-16",
        "category": "emotional-support", 
        "content": """
# Managing Big Emotions 🌊

Sometimes our feelings can feel really big and overwhelming. That's completely normal! Here are ways to help yourself feel better:

## When You Feel Angry 😠

### Cool Down Techniques:
- Count to 10 slowly
- Take deep breaths
- Go for a walk
- Listen to calming music
- Squeeze a stress ball

### Express It Safely:
- Draw your feelings
- Write in a journal
- Talk to someone you trust
- Do physical exercise
- Punch a pillow (not a person!)

## When You Feel Sad 😢

### Comfort Activities:
- Hug a pet or stuffed animal
- Watch a favorite movie
- Call a friend or family member
- Do something creative
- Take a warm bath

### Remember:
- It's okay to cry
- Sad feelings don't last forever
- You don't have to be happy all the time
- Someone cares about you

## When You Feel Worried 😰

### Calming Strategies:
- Practice deep breathing
- Use the 5-4-3-2-1 technique:
  - 5 things you can see
  - 4 things you can touch
  - 3 things you can hear
  - 2 things you can smell
  - 1 thing you can taste
- Talk about your worries
- Write them down

## The STOP Technique 🛑

When emotions feel too big:
- **S**top what you're doing
- **T**ake a deep breath
- **O**bserve how you're feeling
- **P**roceed with a helpful action

## Feeling Thermometer 🌡️

Rate your emotions 1-10:
- 1-3: Feeling okay, manageable
- 4-6: Starting to feel stressed
- 7-8: Need to use coping skills
- 9-10: Need adult help immediately

## Remember:
- All feelings are valid
- Emotions come and go like waves
- You can learn to ride the waves
- Help is always available
- You're stronger than you think! 💪

Practice these skills when you're calm, so they're easier to use when emotions feel big. 🌈
        """,
        "duration": 6,
        "thumbnail_url": ""
    },
    {
        "id": "5",
        "title": "Kindness Challenge",
        "description": "Fun activities to spread kindness in your community.",
        "type": "activity",
        "age_group": "7-16",
        "category": "bullying-prevention",
        "content": """
# 30-Day Kindness Challenge 💝

Small acts of kindness can change the world! Try these ideas:

## Week 1: At School 🏫

### Day 1: Compliment Someone
Give a genuine compliment to a classmate or teacher.

### Day 2: Help a Friend
Offer to help with homework or carry their books.

### Day 3: Include Someone
Invite someone who looks lonely to join your group.

### Day 4: Thank a Teacher
Write a thank you note to a teacher or school staff member.

### Day 5: Share Something
Share your snack, art supplies, or something you enjoy.

### Day 6: Clean Up
Pick up trash or help tidy a classroom without being asked.

### Day 7: Listen Actively
Really listen when someone is talking to you.

## Week 2: At Home 👨‍👩‍👧‍👦

### Day 8: Help with Chores
Do a chore without being asked.

### Day 9: Hug Family
Give extra hugs to family members.

### Day 10: Make Something
Create a drawing or craft for someone you love.

### Day 11: Say Thank You
Thank your parents/guardians for something specific.

### Day 12: Be Patient
Practice patience with siblings or family.

### Day 13: Surprise Someone
Leave a nice note for a family member to find.

### Day 14: Cook Together
Help prepare a meal or treat for the family.

## Week 3: In Your Community 🏘️

### Day 15: Smile at Strangers
Share genuine smiles with people you pass.

### Day 16: Hold the Door
Hold doors open for others.

### Day 17: Thank Service Workers
Thank cashiers, delivery people, or other service workers.

### Day 18: Donate Items
Give away toys, clothes, or books you've outgrown.

### Day 19: Help a Neighbor
Offer to help an elderly neighbor or pet owner.

### Day 20: Pick Up Litter
Clean up litter in your neighborhood or park.

### Day 21: Support Local
Visit or support a local business.

## Week 4: Random Acts of Kindness 🌟

### Day 22: Leave Positive Notes
Leave encouraging sticky notes in public places.

### Day 23: Pay It Forward
Do something nice for someone, and ask them to pass it on.

### Day 24: Apologize Sincerely
If you've hurt someone, offer a heartfelt apology.

### Day 25: Forgive Someone
Let go of a grudge or hurt feeling.

### Day 26: Stand Up for Someone
Defend someone who's being treated unfairly.

### Day 27: Volunteer
Help with a community project or charity.

### Day 28: Send Cards
Make cards for people in nursing homes or hospitals.

### Day 29: Be Kind to Animals
Help care for pets or wildlife.

### Day 30: Celebrate Others
Celebrate someone else's success or achievement.

## Kindness Ideas Bank 💡

### Quick Acts (1 minute):
- Smile genuinely
- Say "please" and "thank you"
- Give a high-five
- Hold an elevator

### Medium Acts (5-10 minutes):
- Write a thank you note
- Help carry something heavy
- Listen to someone's problem
- Share your lunch

### Big Acts (30+ minutes):
- Volunteer at a shelter
- Organize a cleanup
- Tutor someone
- Visit someone lonely

## Kindness Tracker 📊

Keep track of your kind acts:
- How did it make you feel?
- How did the other person react?
- What was the easiest kind act?
- What was the most meaningful?

## Remember:
- Kindness is contagious! 
- Small acts can have big impacts
- Being kind makes you feel good too
- Everyone deserves kindness
- You have the power to brighten someone's day! ☀️

Challenge yourself to do one act of kindness every day. Watch how it transforms your world! 🌍💙
        """,
        "duration": 15,
        "thumbnail_url": ""
    }
]

@router.get("/", response_model=List[LearningResource])
async def get_resources(
    category: Optional[str] = None,
    type: Optional[str] = None,
    age_group: Optional[str] = None
):
    """Get learning resources with optional filtering."""
    
    filtered_resources = mock_resources
    
    if category:
        filtered_resources = [r for r in filtered_resources if r["category"] == category]
    
    if type:
        filtered_resources = [r for r in filtered_resources if r["type"] == type]
    
    if age_group:
        filtered_resources = [r for r in filtered_resources if age_group in r["age_group"]]
    
    return [LearningResource(**resource) for resource in filtered_resources]

@router.get("/{resource_id}", response_model=LearningResource)
async def get_resource(resource_id: str):
    """Get a specific learning resource by ID."""
    
    resource = next((r for r in mock_resources if r["id"] == resource_id), None)
    
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return LearningResource(**resource)

@router.get("/categories/list")
async def get_categories():
    """Get list of available resource categories."""
    
    return {
        "categories": [
            {
                "id": "bullying-prevention",
                "name": "Bullying Prevention",
                "description": "Learn about recognizing and preventing bullying",
                "icon": "shield-checkmark"
            },
            {
                "id": "emotional-support", 
                "name": "Emotional Support",
                "description": "Tools for managing emotions and feelings",
                "icon": "heart"
            },
            {
                "id": "bystander-help",
                "name": "Helping Others",
                "description": "How to safely support others and be a good bystander",
                "icon": "people"
            },
            {
                "id": "self-confidence",
                "name": "Self-Confidence",
                "description": "Activities to build confidence and self-esteem",
                "icon": "star"
            }
        ]
    }

@router.post("/{resource_id}/complete")
async def mark_resource_complete(resource_id: str, user_id: str):
    """Mark a resource as completed by a user."""
    
    resource = next((r for r in mock_resources if r["id"] == resource_id), None)
    
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    # In production, store completion in database
    return {
        "message": "Resource marked as completed",
        "resource_id": resource_id,
        "user_id": user_id,
        "completed_at": datetime.now().isoformat()
    }

@router.get("/user/{user_id}/progress")
async def get_user_progress(user_id: str):
    """Get learning progress for a specific user."""
    
    # Mock progress data
    return {
        "user_id": user_id,
        "total_resources": len(mock_resources),
        "completed_resources": 2,
        "completion_percentage": 40,
        "favorite_categories": ["emotional-support", "self-confidence"],
        "learning_streak": 5,
        "total_learning_time": 45,  # minutes
        "achievements": [
            {
                "id": "first_complete",
                "title": "First Steps",
                "description": "Completed your first learning resource",
                "earned_at": "2024-01-15T10:00:00Z"
            },
            {
                "id": "emotional_learner",
                "title": "Emotional Intelligence",
                "description": "Completed 3 emotional support resources",
                "earned_at": "2024-01-20T14:30:00Z"
            }
        ]
    }