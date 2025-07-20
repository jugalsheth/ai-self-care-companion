from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.database import get_db
from app.models.schemas import (
    GenerateRequest, GenerateResponse, RoutineResponse, RoutineCompletion,
    AnalyticsResponse
)
from app.services.routine_service import routine_service
from app.api.dependencies import get_current_active_user

router = APIRouter()


@router.post("/generate", response_model=RoutineResponse)
async def generate_routine(
    request: GenerateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Generate a new self-care routine"""
    try:
        routine = await routine_service.generate_routine(db, request, current_user.id)
        return routine
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate routine: {str(e)}"
        )


@router.get("/", response_model=List[RoutineResponse])
async def get_routines(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0)
):
    """Get user's routines"""
    routines = routine_service.get_user_routines(db, current_user.id, limit, offset)
    
    return [
        RoutineResponse(
            id=routine.id,
            mood=routine.mood,
            goal=routine.goal,
            steps=routine.steps,
            context=routine.context,
            duration=routine.duration,
            category=routine.category,
            priority=routine.priority,
            is_template=routine.is_template,
            created_at=routine.created_at,
            user_id=routine.user_id,
            completion_count=routine.completion_count
        )
        for routine in routines
    ]


@router.get("/{routine_id}", response_model=RoutineResponse)
async def get_routine(
    routine_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific routine"""
    routine = routine_service.get_routine(db, routine_id, current_user.id)
    
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found"
        )
    
    return RoutineResponse(
        id=routine.id,
        mood=routine.mood,
        goal=routine.goal,
        steps=routine.steps,
        context=routine.context,
        duration=routine.duration,
        category=routine.category,
        priority=routine.priority,
        is_template=routine.is_template,
        created_at=routine.created_at,
        user_id=routine.user_id,
        completion_count=routine.completion_count
    )


@router.post("/{routine_id}/complete")
async def complete_routine(
    routine_id: int,
    completion_data: RoutineCompletion,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Complete a routine"""
    try:
        # Update completion data with routine ID
        completion_data.routine_id = routine_id
        
        completion = routine_service.complete_routine(db, completion_data, current_user.id)
        
        return {"message": "Routine completed successfully", "completion_id": completion.id}
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete routine: {str(e)}"
        )


@router.get("/search/", response_model=List[RoutineResponse])
async def search_routines(
    query: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    limit: int = Query(10, ge=1, le=50)
):
    """Search user's routines"""
    routines = routine_service.search_routines(db, current_user.id, query, limit)
    
    return [
        RoutineResponse(
            id=routine.id,
            mood=routine.mood,
            goal=routine.goal,
            steps=routine.steps,
            context=routine.context,
            duration=routine.duration,
            category=routine.category,
            priority=routine.priority,
            is_template=routine.is_template,
            created_at=routine.created_at,
            user_id=routine.user_id,
            completion_count=routine.completion_count
        )
        for routine in routines
    ]


@router.get("/recommendations/", response_model=List[RoutineResponse])
async def get_recommendations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    limit: int = Query(5, ge=1, le=10)
):
    """Get personalized routine recommendations"""
    routines = routine_service.get_recommendations(db, current_user.id, limit)
    
    return [
        RoutineResponse(
            id=routine.id,
            mood=routine.mood,
            goal=routine.goal,
            steps=routine.steps,
            context=routine.context,
            duration=routine.duration,
            category=routine.category,
            priority=routine.priority,
            is_template=routine.is_template,
            created_at=routine.created_at,
            user_id=routine.user_id,
            completion_count=routine.completion_count
        )
        for routine in routines
    ]