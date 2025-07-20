from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional

from app.config import settings

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    timezone = Column(String, default="UTC")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    routines = relationship("Routine", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user", uselist=False)
    completions = relationship("RoutineCompletion", back_populates="user")


class UserPreference(Base):
    """User preferences model"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preferred_moods = Column(JSON, nullable=True)  # List of preferred moods
    preferred_duration = Column(Integer, default=15)  # Default duration in minutes
    preferred_categories = Column(JSON, nullable=True)  # List of preferred categories
    notification_enabled = Column(Boolean, default=True)
    daily_reminder_time = Column(String, nullable=True)  # Time in HH:MM format
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preferences")


class Routine(Base):
    """Routine model"""
    __tablename__ = "routines"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood = Column(String, nullable=False)
    goal = Column(Text, nullable=False)
    steps = Column(JSON, nullable=False)  # List of steps
    context = Column(Text, nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in minutes
    category = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    is_template = Column(Boolean, default=False)
    completion_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="routines")
    completions = relationship("RoutineCompletion", back_populates="routine")


class RoutineCompletion(Base):
    """Routine completion tracking model"""
    __tablename__ = "routine_completions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=False)
    completed_steps = Column(JSON, nullable=False)  # List of completed step indices
    mood_before = Column(String, nullable=True)
    mood_after = Column(String, nullable=True)
    effectiveness_rating = Column(Integer, nullable=True)  # 1-5 scale
    notes = Column(Text, nullable=True)
    duration_taken = Column(Integer, nullable=True)  # Actual duration taken
    completed_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="completions")
    routine = relationship("Routine", back_populates="completions")


class RoutineTemplate(Base):
    """Pre-built routine templates"""
    __tablename__ = "routine_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    mood_tags = Column(JSON, nullable=False)  # List of applicable moods
    goal_tags = Column(JSON, nullable=False)  # List of applicable goals
    steps = Column(JSON, nullable=False)  # List of steps
    category = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    estimated_duration = Column(Integer, nullable=False)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class MoodEntry(Base):
    """Mood tracking entries"""
    __tablename__ = "mood_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mood = Column(String, nullable=False)
    intensity = Column(Integer, nullable=True)  # 1-10 scale
    context = Column(Text, nullable=True)
    triggers = Column(JSON, nullable=True)  # List of triggers
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User")


# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)