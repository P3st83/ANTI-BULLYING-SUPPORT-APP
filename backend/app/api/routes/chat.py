from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import openai
import re
from app.core.config import settings, AI_RESPONSE_GUIDELINES, CONTENT_SAFETY_RULES

router = APIRouter()

class ChatMessage(BaseModel):
    content: str
    is_from_user: bool
    timestamp: str
    type: str = "text"

class ChatRequest(BaseModel):
    message: str
    user_age: Optional[int] = None
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: Optional[List[str]] = None
    emergency_detected: bool = False
    resources: Optional[List[dict]] = None

# Mock OpenAI client for development
class MockOpenAIClient:
    def __init__(self):
        self.supportive_responses = [
            "Thank you for sharing that with me. Your feelings are completely valid, and I want you to know that you're not alone. 💙",
            "I hear you, and I'm here to listen. It takes courage to talk about difficult experiences. 🌟",
            "That sounds really challenging. Remember that what you're going through is not your fault. 💜",
            "I'm proud of you for reaching out. Your feelings matter, and there are people who care about you. 🤗",
            "It's okay to feel this way. Sometimes talking to a trusted adult like a parent, teacher, or counselor can really help. 💙",
        ]
        
        self.calming_suggestions = [
            "Try taking 5 deep breaths with me - in for 4 counts, hold for 4, out for 4. 🫁",
            "Look around and name 5 things you can see, 4 things you can touch, 3 things you can hear. 👀",
            "Imagine your favorite peaceful place. What does it look like? What sounds do you hear? 🏞️",
            "Gently stretch your arms up high, then let them slowly fall to your sides. 🤸‍♀️",
        ]
        
        self.resources = [
            {
                "title": "Breathing Exercise",
                "type": "activity",
                "description": "A simple breathing exercise to help you feel calmer",
                "duration": "2 minutes"
            },
            {
                "title": "Talk to Someone",
                "type": "resource",
                "description": "Information about trusted adults you can talk to",
                "link": "/resources/trusted-adults"
            }
        ]

    def generate_response(self, message: str, user_age: Optional[int] = None) -> ChatResponse:
        message_lower = message.lower()
        
        # Check for emergency content
        emergency_detected = any(keyword in message_lower for keyword in CONTENT_SAFETY_RULES["emergency_triggers"])
        
        if emergency_detected:
            return ChatResponse(
                response="I'm concerned about what you've shared. Please reach out to a trusted adult, parent, or counselor right away. If you're in immediate danger, please call emergency services. You don't have to go through this alone. 🆘",
                emergency_detected=True,
                resources=[
                    {
                        "title": "Crisis Text Line",
                        "contact": "Text HOME to 741741",
                        "type": "emergency"
                    },
                    {
                        "title": "National Suicide Prevention Lifeline",
                        "contact": "988",
                        "type": "emergency"
                    }
                ]
            )
        
        # Check for bullying content
        bullying_keywords = ['bully', 'bullied', 'bullying', 'mean', 'hurt', 'scared', 'afraid', 'tease', 'pick on']
        has_bullying_content = any(keyword in message_lower for keyword in bullying_keywords)
        
        if has_bullying_content:
            return ChatResponse(
                response="I'm sorry you're experiencing this. Bullying is never okay, and it's not your fault. You're brave for talking about it. 💙",
                suggestions=[
                    "Talk to a trusted adult about this",
                    "Learn strategies for dealing with bullying",
                    "Create an anonymous report",
                    "Practice calming techniques"
                ],
                resources=self.resources
            )
        
        # Check for emotional content
        sad_keywords = ['sad', 'crying', 'upset', 'depressed', 'lonely', 'down']
        anxious_keywords = ['worried', 'anxious', 'nervous', 'scared', 'afraid', 'stress']
        
        if any(keyword in message_lower for keyword in sad_keywords):
            return ChatResponse(
                response="I hear that you're feeling sad, and that's completely okay. Your feelings are valid and important. 💙",
                suggestions=self.calming_suggestions[:2],
                resources=self.resources
            )
        
        if any(keyword in message_lower for keyword in anxious_keywords):
            return ChatResponse(
                response="Feeling anxious or worried is completely normal. Let's try to help you feel more calm and centered. 🌸",
                suggestions=self.calming_suggestions[2:],
                resources=self.resources
            )
        
        # Default supportive response
        import random
        return ChatResponse(
            response=random.choice(self.supportive_responses),
            suggestions=["Tell me more about how you're feeling", "Would you like to try a calming activity?"],
            resources=self.resources[:1]
        )

# Initialize mock client
mock_client = MockOpenAIClient()

@router.post("/send", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message to the AI chatbot and receive a supportive response."""
    
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if len(request.message) > settings.MAX_CHAT_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400, 
            detail=f"Message too long. Maximum {settings.MAX_CHAT_MESSAGE_LENGTH} characters allowed."
        )
    
    # Content safety check
    if contains_inappropriate_content(request.message):
        raise HTTPException(
            status_code=400,
            detail="Message contains inappropriate content. Please keep the conversation supportive and safe."
        )
    
    try:
        # For development, use mock client
        # In production, replace with actual OpenAI client
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "":
            # Use real OpenAI client
            response = await generate_openai_response(request.message, request.user_age)
        else:
            # Use mock client for development
            response = mock_client.generate_response(request.message, request.user_age)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Sorry, I'm having trouble responding right now. Please try again.")

async def generate_openai_response(message: str, user_age: Optional[int] = None) -> ChatResponse:
    """Generate response using OpenAI API (for production use)."""
    
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    system_prompt = f"""
    You are a supportive AI friend for children and teens (ages 7-16) who may be experiencing bullying or emotional difficulties. 

    Guidelines:
    - Be warm, supportive, and non-judgmental
    - Use age-appropriate language for {user_age if user_age else "7-16"} year olds
    - Validate their feelings and experiences
    - Always encourage talking to trusted adults
    - Never provide medical or legal advice
    - If they mention self-harm or suicide, immediately suggest emergency resources
    - Keep responses under 300 words
    - Use occasional emojis to be friendly but not excessive
    - Focus on emotional support and coping strategies
    
    Remember: You are a supportive listener, not a therapist or counselor.
    """
    
    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content
        
        # Check if emergency content was detected
        emergency_detected = any(
            keyword in message.lower() 
            for keyword in CONTENT_SAFETY_RULES["emergency_triggers"]
        )
        
        return ChatResponse(
            response=ai_response,
            emergency_detected=emergency_detected,
            suggestions=generate_suggestions(message) if not emergency_detected else None,
            resources=generate_resources(message) if not emergency_detected else get_emergency_resources()
        )
        
    except Exception as e:
        # Fallback to mock response
        return mock_client.generate_response(message, user_age)

def contains_inappropriate_content(message: str) -> bool:
    """Check if message contains inappropriate content."""
    
    inappropriate_patterns = [
        r'\b\d{3}-\d{3}-\d{4}\b',  # Phone numbers
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email addresses
        r'\b\d{1,5}\s+\w+\s+(street|st|avenue|ave|road|rd|drive|dr|lane|ln)\b',  # Addresses
    ]
    
    for pattern in inappropriate_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    
    return False

def generate_suggestions(message: str) -> List[str]:
    """Generate contextual suggestions based on the message."""
    
    suggestions = []
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['bully', 'bullying', 'mean']):
        suggestions.extend([
            "Learn about bullying prevention strategies",
            "Talk to a trusted adult about this",
            "Practice confidence-building activities"
        ])
    
    if any(word in message_lower for word in ['sad', 'upset', 'down']):
        suggestions.extend([
            "Try a calming breathing exercise",
            "Think about things that make you happy",
            "Reach out to someone who cares about you"
        ])
    
    if any(word in message_lower for word in ['anxious', 'worried', 'nervous']):
        suggestions.extend([
            "Practice mindfulness techniques",
            "Try progressive muscle relaxation",
            "Talk through your worries with someone"
        ])
    
    return suggestions[:3]  # Return up to 3 suggestions

def generate_resources(message: str) -> List[dict]:
    """Generate relevant resources based on the message content."""
    
    resources = []
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['bully', 'bullying']):
        resources.append({
            "title": "Understanding Bullying",
            "type": "article",
            "description": "Learn about different types of bullying and how to respond",
            "link": "/resources/understanding-bullying"
        })
    
    if any(word in message_lower for word in ['calm', 'relax', 'stress']):
        resources.append({
            "title": "Calming Techniques",
            "type": "activity",
            "description": "Simple exercises to help you feel more relaxed",
            "link": "/resources/calming-techniques"
        })
    
    return resources

def get_emergency_resources() -> List[dict]:
    """Get emergency resources for crisis situations."""
    
    return [
        {
            "title": "Crisis Text Line",
            "contact": "Text HOME to 741741",
            "type": "emergency",
            "available": "24/7"
        },
        {
            "title": "National Suicide Prevention Lifeline",
            "contact": "988",
            "type": "emergency",
            "available": "24/7"
        },
        {
            "title": "Trusted Adult",
            "contact": "Parent, teacher, counselor, or other trusted adult",
            "type": "local",
            "available": "Immediate"
        }
    ]

@router.get("/suggestions")
async def get_conversation_starters():
    """Get conversation starter suggestions for users."""
    
    return {
        "starters": [
            "How are you feeling today?",
            "Tell me about your day",
            "What's been on your mind lately?",
            "Is there something bothering you?",
            "I'd like to talk about what happened at school",
            "I'm feeling worried about something",
            "Can you help me understand my feelings?",
            "I need someone to listen"
        ],
        "topics": [
            {
                "title": "Feelings & Emotions",
                "examples": ["I'm feeling sad", "I'm worried about...", "I'm excited because..."]
            },
            {
                "title": "School & Friends",
                "examples": ["Something happened at school", "I'm having trouble with friends", "I feel left out"]
            },
            {
                "title": "Family",
                "examples": ["Things at home are difficult", "I want to talk to my parents but..."]
            },
            {
                "title": "General Support",
                "examples": ["I need encouragement", "I'm feeling overwhelmed", "Can you help me feel better?"]
            }
        ]
    }