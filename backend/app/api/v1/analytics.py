from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.models.schemas import AnalyticsResponse
from app.services.routine_service import routine_service
from app.api.dependencies import get_current_active_user

router = APIRouter()


@router.get("/", response_model=AnalyticsResponse)
async def get_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """Get user analytics"""
    analytics = routine_service.get_user_analytics(db, current_user.id, days)
    return analytics


@router.get("/mood-trends")
async def get_mood_trends(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    days: int = Query(30, ge=1, le=365)
):
    """Get mood trends over time"""
    trends = routine_service.get_mood_trends(db, current_user.id, days)
    return {"mood_trends": trends}


@router.get("/category-distribution")
async def get_category_distribution(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    days: int = Query(30, ge=1, le=365)
):
    """Get category distribution"""
    distribution = routine_service.get_category_distribution(db, current_user.id, days)
    return {"category_distribution": distribution}