from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Anti-Bullying Support API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:19006",  # Expo dev server
        "exp://localhost:19000",   # Expo app
        "http://127.0.0.1:3000",
        "http://127.0.0.1:19006",
    ]
    
    # Database settings
    DATABASE_URL: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI/OpenAI settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    MAX_CHAT_HISTORY: int = 50
    
    # Notification settings
    SENDGRID_API_KEY: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    
    # Content moderation
    ENABLE_CONTENT_MODERATION: bool = True
    MAX_REPORT_LENGTH: int = 2000
    MAX_CHAT_MESSAGE_LENGTH: int = 500
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    CHAT_RATE_LIMIT_PER_MINUTE: int = 20
    
    # File upload settings
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "image/gif"]
    
    # Redis settings (for caching and rate limiting)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Emergency contacts
    EMERGENCY_NOTIFICATION_ENABLED: bool = True
    EMERGENCY_KEYWORDS: List[str] = [
        "suicide", "kill myself", "hurt myself", "end it all",
        "want to die", "self harm", "cutting", "overdose"
    ]
    
    # Content safety patterns
    PERSONAL_INFO_PATTERNS: List[str] = [
        r'\b\d{3}-\d{3}-\d{4}\b',  # Phone numbers
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email addresses
        r'\b\d{1,5}\s\w+\s(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)\b',  # Addresses
        r'\b\d{5}(-\d{4})?\b',  # ZIP codes
        r'\bSSN\s*:?\s*\d{3}-?\d{2}-?\d{4}\b'  # Social Security Numbers
    ]
    
    INAPPROPRIATE_CONTENT_KEYWORDS: List[str] = [
        "explicit", "inappropriate", "sexual", "violent", "illegal",
        "drugs", "alcohol", "weapons", "hate speech"
    ]
    

    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

# Create global settings instance
settings = Settings()

# Content safety guidelines
CONTENT_SAFETY_RULES = {
    "prohibited_topics": [
        "explicit violence",
        "self-harm instructions",
        "illegal activities",
        "inappropriate contact information sharing",
        "cyberbullying coordination"
    ],
    "required_moderation": [
        "personal information",
        "contact details",
        "location information",
        "school-specific information"
    ],
    "emergency_triggers": settings.EMERGENCY_KEYWORDS
}

# Age-appropriate response guidelines
AI_RESPONSE_GUIDELINES = {
    "tone": "supportive, calm, non-judgmental",
    "language_level": "age-appropriate for 7-16 years",
    "max_response_length": 300,
    "always_include": [
        "validation of feelings",
        "encouragement to talk to trusted adults",
        "reminder that help is available"
    ],
    "never_include": [
        "medical advice",
        "legal advice",
        "diagnostic statements",
        "promises of specific outcomes"
    ]
}