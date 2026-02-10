from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._initialize_database()
    
    def _initialize_database(self):
        try:
            if settings.DATABASE_URL:
                self.engine = create_engine(
                    settings.DATABASE_URL,
                    pool_pre_ping=True,
                    pool_recycle=300
                )
                self.SessionLocal = sessionmaker(
                    autocommit=False, 
                    autoflush=False, 
                    bind=self.engine
                )
                logger.info("Database connection initialized successfully")
            else:
                logger.warning("DATABASE_URL not configured, using mock data")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_session(self) -> Session:
        if self.SessionLocal:
            return self.SessionLocal()
        else:
            raise RuntimeError("Database not initialized")
    
    def create_tables(self):
        if self.engine:
            from ..models.base import Base
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        else:
            logger.warning("Cannot create tables: database not initialized")

db_service = DatabaseService()

def get_db():
    if db_service.SessionLocal:
        db = db_service.get_session()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None