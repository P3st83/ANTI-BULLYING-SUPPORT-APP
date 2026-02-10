#!/usr/bin/env python3
"""
Database initialization script for the Anti-Bullying Support App
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.database import db_service
from app.models.base import Base
from app.core.config import settings

def init_database():
    """Initialize the database with tables"""
    print("🔧 Initializing database...")
    print(f"📍 Database URL: {settings.DATABASE_URL}")
    
    try:
        if not db_service.engine:
            print("❌ Database engine not initialized!")
            return False
            
        # Create all tables
        db_service.create_tables()
        print("✅ Database tables created successfully!")
        
        # Test connection
        with db_service.get_session() as session:
            print("✅ Database connection test successful!")
            
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🛡️  Anti-Bullying Support App - Database Setup")
    print("=" * 50)
    
    success = init_database()
    
    if success:
        print("\n🎉 Database setup complete!")
        print("💡 You can now start the application with:")
        print("   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8002")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1) 