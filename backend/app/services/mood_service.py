from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from app.models.database import MoodEntry, User
from app.models.schemas import MoodCreate, MoodUpdate, MoodResponse


class MoodService:
    """Service for mood tracking operations"""
    
    def create_mood_entry(self, db: Session, user_id: int, mood_data: MoodCreate) -> MoodEntry:
        """Create a new mood entry"""
        mood_entry = MoodEntry(
            user_id=user_id,
            mood=mood_data.mood,
            intensity=mood_data.intensity,
            context=mood_data.context,
            triggers=mood_data.triggers,
            created_at=mood_data.created_at or datetime.utcnow()
        )
        db.add(mood_entry)
        db.commit()
        db.refresh(mood_entry)
        return mood_entry
    
    def get_mood_entry(self, db: Session, mood_id: int, user_id: int) -> Optional[MoodEntry]:
        """Get a specific mood entry by ID"""
        return db.query(MoodEntry).filter(
            MoodEntry.id == mood_id,
            MoodEntry.user_id == user_id
        ).first()
    
    def get_user_moods(
        self, 
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[MoodEntry]:
        """Get user's mood entries with pagination and date filtering"""
        query = db.query(MoodEntry).filter(MoodEntry.user_id == user_id)
        
        if start_date:
            query = query.filter(MoodEntry.created_at >= start_date)
        if end_date:
            query = query.filter(MoodEntry.created_at <= end_date)
        
        return query.order_by(desc(MoodEntry.created_at)).offset(skip).limit(limit).all()
    
    def update_mood_entry(
        self, 
        db: Session, 
        mood_id: int, 
        user_id: int, 
        mood_data: MoodUpdate
    ) -> Optional[MoodEntry]:
        """Update a mood entry"""
        mood_entry = self.get_mood_entry(db, mood_id, user_id)
        if not mood_entry:
            return None
        
        update_data = mood_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(mood_entry, field, value)
        
        mood_entry.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(mood_entry)
        return mood_entry
    
    def delete_mood_entry(self, db: Session, mood_id: int, user_id: int) -> bool:
        """Delete a mood entry"""
        mood_entry = self.get_mood_entry(db, mood_id, user_id)
        if not mood_entry:
            return False
        
        db.delete(mood_entry)
        db.commit()
        return True
    
    def get_mood_analytics(self, db: Session, user_id: int, days: int = 30) -> Dict:
        """Get mood analytics for the user"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get mood entries in date range
        mood_entries = db.query(MoodEntry).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.created_at >= start_date,
            MoodEntry.created_at <= end_date
        ).all()
        
        if not mood_entries:
            return {
                "total_entries": 0,
                "average_intensity": 0,
                "most_common_mood": None,
                "mood_distribution": {},
                "daily_averages": {},
                "trends": {}
            }
        
        # Calculate analytics
        total_entries = len(mood_entries)
        intensities = [entry.intensity for entry in mood_entries if entry.intensity]
        average_intensity = sum(intensities) / len(intensities) if intensities else 0
        
        # Most common mood
        mood_counts = {}
        for entry in mood_entries:
            mood_counts[entry.mood] = mood_counts.get(entry.mood, 0) + 1
        
        most_common_mood = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else None
        
        # Daily averages
        daily_averages = {}
        for entry in mood_entries:
            date_key = entry.created_at.strftime('%Y-%m-%d')
            if date_key not in daily_averages:
                daily_averages[date_key] = []
            if entry.intensity:
                daily_averages[date_key].append(entry.intensity)
        
        # Calculate average for each day
        for date_key in daily_averages:
            daily_averages[date_key] = sum(daily_averages[date_key]) / len(daily_averages[date_key])
        
        return {
            "total_entries": total_entries,
            "average_intensity": round(average_intensity, 2),
            "most_common_mood": most_common_mood,
            "mood_distribution": mood_counts,
            "daily_averages": daily_averages,
            "trends": self._calculate_trends(mood_entries)
        }
    
    def _calculate_trends(self, mood_entries: List[MoodEntry]) -> Dict:
        """Calculate mood trends over time"""
        if not mood_entries:
            return {}
        
        # Group by week
        weekly_data = {}
        for entry in mood_entries:
            week_key = entry.created_at.strftime('%Y-W%U')
            if week_key not in weekly_data:
                weekly_data[week_key] = []
            if entry.intensity:
                weekly_data[week_key].append(entry.intensity)
        
        # Calculate weekly averages
        weekly_averages = {}
        for week_key, intensities in weekly_data.items():
            weekly_averages[week_key] = sum(intensities) / len(intensities)
        
        return weekly_averages


# Create service instance
mood_service = MoodService() 