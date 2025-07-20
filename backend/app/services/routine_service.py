from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from datetime import datetime, timedelta
import logging

from app.models.database import Routine, RoutineCompletion, User, RoutineTemplate
from app.models.schemas import (
    RoutineCreate, RoutineResponse, RoutineCompletion as RoutineCompletionSchema,
    AnalyticsResponse, GenerateRequest
)
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)


class RoutineService:
    """Service for managing self-care routines"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    async def generate_routine(self, db: Session, request: GenerateRequest, user_id: int) -> RoutineResponse:
        """Generate a new routine using AI"""
        # Get user history for context
        user_history = self.get_user_history_for_ai(db, user_id)
        
        # Generate routine using AI
        ai_response = await self.ai_service.generate_routine(request, user_history)
        
        # Create routine in database
        routine_data = RoutineCreate(
            mood=request.mood,
            goal=request.goal,
            steps=ai_response.steps,
            context=request.context,
            duration=ai_response.estimated_duration,
            category=ai_response.category,
            priority=ai_response.priority
        )
        
        routine = self.create_routine(db, routine_data, user_id)
        
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
    
    def create_routine(self, db: Session, routine_data: RoutineCreate, user_id: int) -> Routine:
        """Create a new routine"""
        db_routine = Routine(
            user_id=user_id,
            mood=routine_data.mood,
            goal=routine_data.goal,
            steps=routine_data.steps,
            context=routine_data.context,
            duration=routine_data.duration,
            category=routine_data.category,
            priority=routine_data.priority,
            is_template=routine_data.is_template
        )
        
        db.add(db_routine)
        db.commit()
        db.refresh(db_routine)
        
        return db_routine
    
    def get_routine(self, db: Session, routine_id: int, user_id: int) -> Optional[Routine]:
        """Get a specific routine"""
        return db.query(Routine).filter(
            and_(Routine.id == routine_id, Routine.user_id == user_id)
        ).first()
    
    def get_user_routines(self, db: Session, user_id: int, limit: int = 10, offset: int = 0) -> List[Routine]:
        """Get user's routines"""
        return db.query(Routine).filter(
            Routine.user_id == user_id
        ).order_by(desc(Routine.created_at)).offset(offset).limit(limit).all()
    
    def get_routine_templates(self, db: Session, limit: int = 20) -> List[RoutineTemplate]:
        """Get available routine templates"""
        return db.query(RoutineTemplate).order_by(desc(RoutineTemplate.usage_count)).limit(limit).all()
    
    def complete_routine(self, db: Session, completion_data: RoutineCompletionSchema, user_id: int) -> RoutineCompletion:
        """Record routine completion"""
        # Get the routine
        routine = self.get_routine(db, completion_data.routine_id, user_id)
        if not routine:
            raise ValueError("Routine not found")
        
        # Create completion record
        db_completion = RoutineCompletion(
            user_id=user_id,
            routine_id=completion_data.routine_id,
            completed_steps=completion_data.completed_steps,
            mood_after=completion_data.mood_after,
            effectiveness_rating=completion_data.effectiveness_rating,
            notes=completion_data.notes
        )
        
        db.add(db_completion)
        
        # Update routine completion count
        routine.completion_count += 1
        
        db.commit()
        db.refresh(db_completion)
        
        return db_completion
    
    def get_user_analytics(self, db: Session, user_id: int, days: int = 30) -> AnalyticsResponse:
        """Get user analytics"""
        # Date range
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total routines
        total_routines = db.query(Routine).filter(
            and_(Routine.user_id == user_id, Routine.created_at >= start_date)
        ).count()
        
        # Completed routines
        completed_routines = db.query(RoutineCompletion).filter(
            and_(RoutineCompletion.user_id == user_id, RoutineCompletion.completed_at >= start_date)
        ).count()
        
        # Completion rate
        completion_rate = (completed_routines / total_routines) if total_routines > 0 else 0
        
        # Most common mood
        mood_query = db.query(
            Routine.mood, func.count(Routine.mood).label('count')
        ).filter(
            and_(Routine.user_id == user_id, Routine.created_at >= start_date)
        ).group_by(Routine.mood).order_by(desc('count')).first()
        
        most_common_mood = mood_query.mood if mood_query else None
        
        # Average effectiveness
        avg_effectiveness = db.query(
            func.avg(RoutineCompletion.effectiveness_rating)
        ).filter(
            and_(RoutineCompletion.user_id == user_id, RoutineCompletion.completed_at >= start_date)
        ).scalar()
        
        # Calculate streaks
        current_streak, longest_streak = self.calculate_streaks(db, user_id)
        
        # Mood trends
        mood_trends = self.get_mood_trends(db, user_id, days)
        
        # Category distribution
        category_dist = self.get_category_distribution(db, user_id, days)
        
        return AnalyticsResponse(
            total_routines=total_routines,
            completed_routines=completed_routines,
            completion_rate=round(completion_rate, 2),
            most_common_mood=most_common_mood,
            average_effectiveness=round(avg_effectiveness, 2) if avg_effectiveness else None,
            current_streak=current_streak,
            longest_streak=longest_streak,
            mood_trends=mood_trends,
            category_distribution=category_dist
        )
    
    def calculate_streaks(self, db: Session, user_id: int) -> tuple[int, int]:
        """Calculate current and longest streaks"""
        # Get completion dates
        completions = db.query(RoutineCompletion).filter(
            RoutineCompletion.user_id == user_id
        ).order_by(desc(RoutineCompletion.completed_at)).all()
        
        if not completions:
            return 0, 0
        
        # Calculate current streak
        current_streak = 0
        current_date = datetime.utcnow().date()
        
        for completion in completions:
            completion_date = completion.completed_at.date()
            if completion_date == current_date or completion_date == current_date - timedelta(days=1):
                current_streak += 1
                current_date = completion_date - timedelta(days=1)
            else:
                break
        
        # Calculate longest streak (simplified)
        longest_streak = current_streak  # TODO: Implement proper longest streak calculation
        
        return current_streak, longest_streak
    
    def get_mood_trends(self, db: Session, user_id: int, days: int = 30) -> Dict[str, int]:
        """Get mood trends over time"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        mood_counts = db.query(
            Routine.mood, func.count(Routine.mood).label('count')
        ).filter(
            and_(Routine.user_id == user_id, Routine.created_at >= start_date)
        ).group_by(Routine.mood).all()
        
        return {mood: count for mood, count in mood_counts}
    
    def get_category_distribution(self, db: Session, user_id: int, days: int = 30) -> Dict[str, int]:
        """Get category distribution"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        category_counts = db.query(
            Routine.category, func.count(Routine.category).label('count')
        ).filter(
            and_(Routine.user_id == user_id, Routine.created_at >= start_date, Routine.category.isnot(None))
        ).group_by(Routine.category).all()
        
        return {category: count for category, count in category_counts}
    
    def get_user_history_for_ai(self, db: Session, user_id: int, limit: int = 5) -> List[Dict[str, Any]]:
        """Get user routine history for AI context"""
        recent_routines = db.query(Routine).filter(
            Routine.user_id == user_id
        ).order_by(desc(Routine.created_at)).limit(limit).all()
        
        return [
            {
                "mood": routine.mood,
                "goal": routine.goal,
                "steps": routine.steps,
                "completion_count": routine.completion_count
            }
            for routine in recent_routines
        ]
    
    def search_routines(self, db: Session, user_id: int, query: str, limit: int = 10) -> List[Routine]:
        """Search user's routines"""
        return db.query(Routine).filter(
            and_(
                Routine.user_id == user_id,
                Routine.goal.ilike(f"%{query}%") | Routine.mood.ilike(f"%{query}%")
            )
        ).order_by(desc(Routine.created_at)).limit(limit).all()
    
    def get_recommendations(self, db: Session, user_id: int, limit: int = 5) -> List[Routine]:
        """Get personalized routine recommendations"""
        # Get user's most successful routines (high completion count)
        return db.query(Routine).filter(
            Routine.user_id == user_id
        ).order_by(desc(Routine.completion_count)).limit(limit).all()


# Global routine service instance
routine_service = RoutineService()