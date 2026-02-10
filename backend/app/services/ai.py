import re
import random
from typing import List, Dict, Optional
from openai import OpenAI
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            logger.warning("OpenAI API key not configured, using mock responses")
        
        self.emergency_keywords = settings.EMERGENCY_KEYWORDS
        self.personal_info_patterns = settings.PERSONAL_INFO_PATTERNS
        self.inappropriate_content_keywords = settings.INAPPROPRIATE_CONTENT_KEYWORDS
    
    def process_message(self, message: str, user_age: int = 12) -> Dict:
        safety_check = self._check_message_safety(message)
        
        if safety_check["is_emergency"]:
            return {
                "response": self._get_emergency_response(),
                "is_emergency": True,
                "safety_flags": safety_check["flags"],
                "contains_personal_info": safety_check["contains_personal_info"]
            }
        
        if safety_check["contains_personal_info"]:
            return {
                "response": self._get_privacy_warning(),
                "is_emergency": False,
                "safety_flags": safety_check["flags"],
                "contains_personal_info": True
            }
        
        if safety_check["is_inappropriate"]:
            return {
                "response": self._get_appropriate_redirect(),
                "is_emergency": False,
                "safety_flags": safety_check["flags"],
                "contains_personal_info": False
            }
        
        response = self._generate_response(message, user_age)
        
        return {
            "response": response,
            "is_emergency": False,
            "safety_flags": [],
            "contains_personal_info": False
        }
    
    def _check_message_safety(self, message: str) -> Dict:
        message_lower = message.lower()
        flags = []
        
        is_emergency = any(
            keyword.lower() in message_lower 
            for keyword in self.emergency_keywords
        )
        if is_emergency:
            flags.append("emergency_keywords")
        
        contains_personal_info = any(
            re.search(pattern, message, re.IGNORECASE) 
            for pattern in self.personal_info_patterns
        )
        if contains_personal_info:
            flags.append("personal_information")
        
        is_inappropriate = any(
            keyword.lower() in message_lower 
            for keyword in self.inappropriate_content_keywords
        )
        if is_inappropriate:
            flags.append("inappropriate_content")
        
        return {
            "is_emergency": is_emergency,
            "contains_personal_info": contains_personal_info,
            "is_inappropriate": is_inappropriate,
            "flags": flags
        }
    
    def _generate_response(self, message: str, user_age: int) -> str:
        if self.client:
            return self._generate_openai_response(message, user_age)
        else:
            return self._generate_mock_response(message)
    
    def _generate_openai_response(self, message: str, user_age: int) -> str:
        try:
            system_prompt = f"""You are a supportive AI assistant helping children aged {user_age} who may be experiencing bullying. 

{settings.AI_RESPONSE_GUIDELINES}

Age-appropriate considerations:
- Use simple, clear language appropriate for a {user_age}-year-old
- Be encouraging and supportive
- Focus on practical advice and emotional support
- Always maintain a safe, non-judgmental tone
- Encourage talking to trusted adults when appropriate

Never provide specific personal information, locations, or contact details beyond general resources."""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._generate_mock_response(message)
    
    def _generate_mock_response(self, message: str) -> str:
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["sad", "upset", "crying", "hurt"]):
            responses = [
                "I'm really sorry you're feeling this way. It's completely normal to feel sad when someone is being mean to you. Remember that you're important and deserving of kindness. 💙",
                "Your feelings are valid, and it's okay to feel upset. You're stronger than you know, and this difficult time won't last forever. Is there a trusted adult you can talk to?",
                "I can hear that you're hurting right now. That takes courage to share. You don't have to go through this alone - there are people who want to help you."
            ]
        elif any(word in message_lower for word in ["angry", "mad", "furious", "hate"]):
            responses = [
                "It sounds like you're feeling really angry, and that's understandable. When someone treats us badly, anger is a natural response. Let's think about healthy ways to handle these big feelings.",
                "Anger can be a powerful emotion. It's okay to feel mad when someone is being unfair to you. What helps you feel calmer when you're upset?",
                "I can feel your frustration. It's hard when people don't treat us with respect. Remember, your feelings matter, but let's focus on ways to stay safe and get support."
            ]
        elif any(word in message_lower for word in ["scared", "afraid", "frightened", "worried"]):
            responses = [
                "Feeling scared is completely understandable when you're being bullied. You're brave for reaching out. Remember, asking for help is a sign of strength, not weakness.",
                "It's normal to feel afraid in situations like this. Your safety is the most important thing. Have you been able to talk to a parent, teacher, or another trusted adult?",
                "Being worried shows that you care about yourself and your wellbeing. That's actually a good thing! Let's think about people in your life who can help keep you safe."
            ]
        elif any(word in message_lower for word in ["school", "classroom", "teacher", "student"]):
            responses = [
                "School should be a safe place for everyone. If something is happening at school, it's really important to tell a teacher, counselor, or principal. They're there to help protect you.",
                "I'm glad you're thinking about your school situation. Remember, you have the right to feel safe at school. Don't hesitate to speak up to school staff who can help.",
                "School problems can feel overwhelming, but you don't have to handle them alone. Teachers and school counselors are trained to help with situations like this."
            ]
        elif any(word in message_lower for word in ["friend", "friends", "lonely", "alone"]):
            responses = [
                "Friendships can be complicated, especially when bullying is involved. Remember, real friends treat each other with kindness and respect. You deserve friends who make you feel good about yourself.",
                "Feeling lonely is really hard. Sometimes when we're being bullied, it can feel like we don't have anyone on our side. But there are people who care about you, even if it doesn't feel that way right now.",
                "It's tough when friend situations get complicated. Focus on the people who treat you well and make you feel happy to be yourself. Those are your real friends."
            ]
        elif any(word in message_lower for word in ["help", "what do i do", "don't know"]):
            responses = [
                "I'm proud of you for asking for help - that's actually a really important first step! Here are some things you can do: talk to a trusted adult, document what's happening, and remember that this isn't your fault.",
                "Asking 'what do I do' shows you're being thoughtful about your situation. The most important thing is to tell a trusted adult what's happening. They can help you figure out the best next steps.",
                "It's completely normal to feel unsure about what to do. Every situation is different, but you're not alone in figuring this out. Consider talking to a parent, teacher, or school counselor."
            ]
        else:
            responses = [
                "Thank you for sharing with me. It takes courage to talk about difficult experiences. Remember, you deserve to be treated with kindness and respect. 🌟",
                "I'm here to listen and support you. You're important, and your feelings matter. Is there anything specific you'd like to talk about today?",
                "It sounds like you're going through a tough time. I want you to know that you're not alone, and it's not your fault. You deserve support and understanding.",
                "I appreciate you trusting me with your thoughts. Remember, every person deserves to feel safe and valued. You have strengths that can help you through this.",
                "Your wellbeing is important to me. Whatever you're experiencing, please know that there are people who want to help and support you."
            ]
        
        return random.choice(responses)
    
    def _get_emergency_response(self) -> str:
        return """I'm really concerned about what you've shared with me. Your safety is the most important thing right now.

🆘 **If you're in immediate danger, please:**
- Call 911 (emergency services)
- Tell a trusted adult right away
- Go to a safe place

📞 **Crisis Resources:**
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741
- National Child Abuse Hotline: 1-800-4-A-CHILD (1-800-422-4453)

Please don't wait to get help. You matter, and there are people who want to keep you safe. 💙"""
    
    def _get_privacy_warning(self) -> str:
        return """I noticed you might have shared some personal information. For your safety, please don't share things like:

🚫 **Don't share:**
- Your full name, address, or phone number
- Your school's name or specific location
- Names of other people involved
- Photos or identifying details

✅ **It's okay to share:**
- How you're feeling
- General types of situations you're experiencing
- Questions about getting help

I'm here to support you while keeping you safe! Is there something else you'd like to talk about?"""
    
    def _get_appropriate_redirect(self) -> str:
        return """I want to keep our conversation positive and helpful. Let's focus on:

✨ **Things we can talk about:**
- How you're feeling and coping strategies
- Ways to build confidence and resilience  
- Getting support from trusted adults
- Making good choices and staying safe

I'm here to help you feel better and find healthy ways to handle difficult situations. What would you like to focus on today? 🌟"""
    
    def get_conversation_starters(self) -> List[str]:
        return [
            "How are you feeling today?",
            "What's been on your mind lately?",
            "Is there something you'd like to talk about?",
            "What's one good thing that happened today?",
            "How can I help support you right now?",
            "What would make you feel safer or happier?",
            "Tell me about someone who makes you feel good about yourself",
            "What are some things you're good at?"
        ]

ai_service = AIService()