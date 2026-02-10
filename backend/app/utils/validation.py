import re
from typing import List, Dict
from ..core.config import settings

def validate_content_safety(content: str) -> Dict:
    content_lower = content.lower()
    flags = []
    
    for keyword in settings.INAPPROPRIATE_CONTENT_KEYWORDS:
        if keyword.lower() in content_lower:
            flags.append(f"inappropriate_keyword: {keyword}")
    
    for pattern in settings.PERSONAL_INFO_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            flags.append(f"personal_info_detected")
            break
    
    return {
        "is_safe": len(flags) == 0,
        "flags": flags
    }

def validate_age_appropriate(content: str, user_age: int) -> Dict:
    content_lower = content.lower()
    warnings = []
    
    complex_topics = [
        "depression", "suicide", "self-harm", "violence", 
        "abuse", "assault", "drugs", "alcohol"
    ]
    
    if user_age < 10:
        for topic in complex_topics:
            if topic in content_lower:
                warnings.append(f"complex_topic_for_age: {topic}")
    
    return {
        "is_appropriate": len(warnings) == 0,
        "warnings": warnings,
        "suggested_age": 10 if warnings else user_age
    }

def sanitize_user_input(text: str, max_length: int = 1000) -> str:
    if not text:
        return ""
    
    text = text.strip()
    
    if len(text) > max_length:
        text = text[:max_length]
    
    unsafe_patterns = [
        r'<script.*?>.*?</script>',
        r'<.*?>',
        r'javascript:',
        r'vbscript:',
        r'onload=',
        r'onerror='
    ]
    
    for pattern in unsafe_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
    
    return text

def validate_email_format(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone_format(phone: str) -> bool:
    phone = re.sub(r'[^\d]', '', phone)
    return len(phone) >= 10 and len(phone) <= 15