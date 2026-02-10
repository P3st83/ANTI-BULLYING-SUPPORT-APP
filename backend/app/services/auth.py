from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..core.config import settings
from ..models.user import User
from ..schemas.user import UserCreate
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = settings.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except JWTError as e:
            logger.warning(f"Token verification failed: {e}")
            return None
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        if not db:
            logger.warning("Database not available, using mock authentication")
            return self._mock_authenticate_user(username, password)
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_user(self, db: Session, user_create: UserCreate) -> User:
        if not db:
            logger.warning("Database not available, using mock user creation")
            return self._mock_create_user(user_create)
        
        hashed_password = self.get_password_hash(user_create.password)
        
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            age=user_create.age,
            parent_email=user_create.parent_email,
            parental_consent=user_create.age >= 13 or bool(user_create.parent_email),
            profile_color=user_create.profile_color,
            avatar_emoji=user_create.avatar_emoji
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        if not db:
            return self._mock_get_user(username)
        return db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        if not db:
            return self._mock_get_user_by_id(user_id)
        return db.query(User).filter(User.id == user_id).first()
    
    def _mock_authenticate_user(self, username: str, password: str) -> Optional[User]:
        mock_users = {
            "testuser": {
                "id": 1,
                "username": "testuser",
                "email": "test@example.com",
                "hashed_password": self.get_password_hash("testpass123"),
                "first_name": "Test",
                "last_name": "User",
                "age": 14,
                "is_active": True,
                "parental_consent": True
            }
        }
        
        if username in mock_users:
            user_data = mock_users[username]
            if self.verify_password(password, user_data["hashed_password"]):
                return User(**user_data)
        return None
    
    def _mock_create_user(self, user_create: UserCreate) -> User:
        import random
        return User(
            id=random.randint(1000, 9999),
            username=user_create.username,
            email=user_create.email,
            hashed_password=self.get_password_hash(user_create.password),
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            age=user_create.age,
            parent_email=user_create.parent_email,
            parental_consent=user_create.age >= 13 or bool(user_create.parent_email),
            profile_color=user_create.profile_color,
            avatar_emoji=user_create.avatar_emoji,
            is_active=True,
            is_verified=False,
            created_at=datetime.utcnow()
        )
    
    def _mock_get_user(self, username: str) -> Optional[User]:
        if username == "testuser":
            return User(
                id=1,
                username="testuser",
                email="test@example.com",
                hashed_password=self.get_password_hash("testpass123"),
                first_name="Test",
                last_name="User",
                age=14,
                is_active=True,
                parental_consent=True,
                created_at=datetime.utcnow()
            )
        return None
    
    def _mock_get_user_by_id(self, user_id: int) -> Optional[User]:
        if user_id == 1:
            return User(
                id=1,
                username="testuser",
                email="test@example.com",
                hashed_password=self.get_password_hash("testpass123"),
                first_name="Test",
                last_name="User",
                age=14,
                is_active=True,
                parental_consent=True,
                created_at=datetime.utcnow()
            )
        return None

auth_service = AuthService()