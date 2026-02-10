from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from ..services.auth import auth_service
from ..services.database import get_db
from ..models.user import User
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = auth_service.verify_token(token)
        
        if payload is None:
            raise credentials_exception
            
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        raise credentials_exception
    
    user = auth_service.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
        
    return user

async def require_auth(current_user: User = Depends(get_current_user)) -> User:
    return current_user

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not credentials:
        return None
        
    try:
        token = credentials.credentials
        payload = auth_service.verify_token(token)
        
        if payload is None:
            return None
            
        username: str = payload.get("sub")
        if username is None:
            return None
            
        user = auth_service.get_user_by_username(db, username=username)
        return user if user and user.is_active else None
        
    except Exception as e:
        logger.error(f"Optional auth error: {e}")
        return None