from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.database import get_db, User
from app.models.schemas import (
    MoodCreate, 
    MoodUpdate, 
    MoodResponse, 
    MoodAnalyticsResponse
)
from app.services.mood_service import mood_service
from app.api.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_model=MoodResponse)
async def create_mood_entry(
    mood_data: MoodCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new mood entry"""
    try:
        mood_entry = mood_service.create_mood_entry(db, current_user.id, mood_data)
        return mood_entry
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[MoodResponse])
async def get_mood_entries(
    skip: int = Query(0, ge=0, description="Number of entries to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of entries to return"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's mood entries with pagination and date filtering"""
    try:
        # Parse dates if provided
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        mood_entries = mood_service.get_user_moods(
            db, 
            current_user.id, 
            skip=skip, 
            limit=limit,
            start_date=start_dt,
            end_date=end_dt
        )
        return mood_entries
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{mood_id}", response_model=MoodResponse)
async def get_mood_entry(
    mood_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific mood entry by ID"""
    mood_entry = mood_service.get_mood_entry(db, mood_id, current_user.id)
    if not mood_entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return mood_entry


@router.put("/{mood_id}", response_model=MoodResponse)
async def update_mood_entry(
    mood_id: int,
    mood_data: MoodUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a mood entry"""
    mood_entry = mood_service.update_mood_entry(db, mood_id, current_user.id, mood_data)
    if not mood_entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return mood_entry


@router.delete("/{mood_id}")
async def delete_mood_entry(
    mood_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a mood entry"""
    success = mood_service.delete_mood_entry(db, mood_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return {"message": "Mood entry deleted successfully"}


@router.get("/analytics/overview", response_model=MoodAnalyticsResponse)
async def get_mood_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mood analytics for the user"""
    try:
        analytics = mood_service.get_mood_analytics(db, current_user.id, days)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/trends")
async def get_mood_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mood trends over time"""
    try:
        analytics = mood_service.get_mood_analytics(db, current_user.id, days)
        return {"trends": analytics["trends"], "daily_averages": analytics["daily_averages"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/distribution")
async def get_mood_distribution(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get mood distribution statistics"""
    try:
        analytics = mood_service.get_mood_analytics(db, current_user.id, days)
        return {
            "mood_distribution": analytics["mood_distribution"],
            "most_common_mood": analytics["most_common_mood"],
            "total_entries": analytics["total_entries"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 