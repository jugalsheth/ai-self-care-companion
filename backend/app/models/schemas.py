from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MoodType(str, Enum):
    """Predefined mood types"""
    STRESSED = "Stressed"
    TIRED = "Tired"
    FOCUSED = "Focused"
    ANXIOUS = "Anxious"
    CALM = "Calm"
    HAPPY = "Happy"
    SAD = "Sad"
    EXCITED = "Excited"
    OVERWHELMED = "Overwhelmed"
    MOTIVATED = "Motivated"


class RoutineCategory(str, Enum):
    """Routine categories"""
    MINDFULNESS = "Mindfulness"
    PHYSICAL = "Physical"
    EMOTIONAL = "Emotional"
    PRODUCTIVITY = "Productivity"
    RELAXATION = "Relaxation"
    SOCIAL = "Social"
    CREATIVE = "Creative"


class PriorityLevel(str, Enum):
    """Priority levels for routines"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# Request/Response Models
class GenerateRequest(BaseModel):
    """Request model for generating self-care routines"""
    mood: str = Field(..., description="Current mood or feeling")
    goal: str = Field(..., description="What the user wants to achieve")
    context: Optional[str] = Field(None, description="Additional context or preferences")
    duration: Optional[int] = Field(None, ge=5, le=120, description="Preferred duration in minutes")
    
    @validator('mood')
    def validate_mood(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Mood cannot be empty')
        return v.strip()
    
    @validator('goal')
    def validate_goal(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Goal cannot be empty')
        return v.strip()


class GenerateResponse(BaseModel):
    """Response model for generated routines"""
    steps: List[str] = Field(..., description="List of self-care steps")
    estimated_duration: Optional[int] = Field(None, description="Estimated duration in minutes")
    category: Optional[RoutineCategory] = Field(None, description="Routine category")
    priority: Optional[PriorityLevel] = Field(None, description="Priority level")
    tips: Optional[List[str]] = Field(None, description="Additional tips")


class UserCreate(BaseModel):
    """User creation model"""
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    name: str = Field(..., min_length=2, description="User's full name")
    timezone: Optional[str] = Field("UTC", description="User's timezone")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()


class UserResponse(BaseModel):
    """User response model"""
    id: int
    email: str
    name: str
    timezone: str
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


class UserPreferences(BaseModel):
    """User preferences model"""
    preferred_moods: Optional[List[MoodType]] = Field(None, description="User's common moods")
    preferred_duration: Optional[int] = Field(15, ge=5, le=120, description="Preferred routine duration")
    preferred_categories: Optional[List[RoutineCategory]] = Field(None, description="Preferred routine categories")
    notification_enabled: bool = Field(True, description="Enable notifications")
    daily_reminder_time: Optional[str] = Field(None, description="Daily reminder time (HH:MM)")


class RoutineCreate(BaseModel):
    """Routine creation model"""
    mood: str
    goal: str
    steps: List[str]
    context: Optional[str] = None
    duration: Optional[int] = None
    category: Optional[RoutineCategory] = None
    priority: Optional[PriorityLevel] = None
    is_template: bool = False


class RoutineResponse(BaseModel):
    """Routine response model"""
    id: int
    mood: str
    goal: str
    steps: List[str]
    context: Optional[str]
    duration: Optional[int]
    category: Optional[RoutineCategory]
    priority: Optional[PriorityLevel]
    is_template: bool
    created_at: datetime
    user_id: int
    completion_count: int
    
    class Config:
        from_attributes = True


class RoutineCompletion(BaseModel):
    """Routine completion model"""
    routine_id: int
    completed_steps: List[int] = Field(..., description="List of completed step indices")
    mood_after: Optional[str] = Field(None, description="Mood after completion")
    effectiveness_rating: Optional[int] = Field(None, ge=1, le=5, description="Effectiveness rating (1-5)")
    notes: Optional[str] = Field(None, description="Additional notes")


class AnalyticsResponse(BaseModel):
    """Analytics response model"""
    total_routines: int
    completed_routines: int
    completion_rate: float
    most_common_mood: Optional[str]
    average_effectiveness: Optional[float]
    current_streak: int
    longest_streak: int
    mood_trends: dict
    category_distribution: dict


class Token(BaseModel):
    """JWT token model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token data model"""
    user_id: Optional[int] = None
    email: Optional[str] = None


# Mood Tracking Models
class MoodCreate(BaseModel):
    """Mood entry creation model"""
    mood: str = Field(..., description="Mood description")
    intensity: Optional[int] = Field(None, ge=1, le=10, description="Mood intensity (1-10)")
    context: Optional[str] = Field(None, description="Context or situation")
    triggers: Optional[List[str]] = Field(None, description="List of triggers")
    created_at: Optional[datetime] = Field(None, description="Entry timestamp")
    
    @validator('mood')
    def validate_mood(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Mood cannot be empty')
        return v.strip()


class MoodUpdate(BaseModel):
    """Mood entry update model"""
    mood: Optional[str] = Field(None, description="Mood description")
    intensity: Optional[int] = Field(None, ge=1, le=10, description="Mood intensity (1-10)")
    context: Optional[str] = Field(None, description="Context or situation")
    triggers: Optional[List[str]] = Field(None, description="List of triggers")


class MoodResponse(BaseModel):
    """Mood entry response model"""
    id: int
    user_id: int
    mood: str
    intensity: Optional[int]
    context: Optional[str]
    triggers: Optional[List[str]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MoodAnalyticsResponse(BaseModel):
    """Mood analytics response model"""
    total_entries: int
    average_intensity: float
    most_common_mood: Optional[str]
    mood_distribution: dict
    daily_averages: dict
    trends: dict