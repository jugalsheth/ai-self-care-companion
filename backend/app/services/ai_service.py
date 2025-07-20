import openai
from typing import List, Dict, Any, Optional
import json
import logging
from datetime import datetime

from app.config import settings
from app.models.schemas import GenerateRequest, GenerateResponse, RoutineCategory, PriorityLevel

logger = logging.getLogger(__name__)

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


class AIService:
    """AI service for generating self-care routines"""
    
    def __init__(self):
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
    
    async def generate_routine(self, request: GenerateRequest, user_history: Optional[List[Dict]] = None) -> GenerateResponse:
        """Generate a personalized self-care routine"""
        
        # Build context-aware prompt
        prompt = self._build_prompt(request, user_history)
        
        try:
            response = await self._call_openai(prompt)
            parsed_response = self._parse_response(response)
            
            return GenerateResponse(
                steps=parsed_response.get("steps", []),
                estimated_duration=parsed_response.get("duration", request.duration),
                category=self._determine_category(request.mood, request.goal),
                priority=self._determine_priority(request.mood),
                tips=parsed_response.get("tips", [])
            )
            
        except Exception as e:
            logger.error(f"Error generating routine: {str(e)}")
            return self._fallback_routine(request)
    
    def _build_prompt(self, request: GenerateRequest, user_history: Optional[List[Dict]] = None) -> str:
        """Build a context-aware prompt for AI generation"""
        
        base_prompt = f"""
        You are an expert self-care and wellness coach. Create a personalized routine for a user who:
        - Currently feels: {request.mood}
        - Wants to achieve: {request.goal}
        """
        
        if request.context:
            base_prompt += f"\n- Additional context: {request.context}"
        
        if request.duration:
            base_prompt += f"\n- Preferred duration: {request.duration} minutes"
        
        if user_history:
            base_prompt += f"\n- Previous successful routines: {self._format_history(user_history)}"
        
        base_prompt += """
        
        Please generate a response in the following JSON format:
        {
            "steps": ["step 1", "step 2", "step 3"],
            "duration": estimated_duration_in_minutes,
            "tips": ["tip 1", "tip 2"]
        }
        
        Requirements:
        - Provide 3-5 specific, actionable steps
        - Each step should be concise and clear
        - Consider the user's current mood and goal
        - Make it practical and achievable
        - Include helpful tips for better results
        - Ensure the routine is evidence-based and safe
        """
        
        return base_prompt
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API with error handling"""
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful and knowledgeable self-care coach. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            return response.choices[0].message.content.strip()
            
        except openai.RateLimitError:
            logger.warning("OpenAI rate limit exceeded")
            raise Exception("Service temporarily unavailable. Please try again later.")
        
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception("AI service error. Please try again.")
        
        except Exception as e:
            logger.error(f"Unexpected error calling OpenAI: {str(e)}")
            raise Exception("Service error. Please try again.")
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured format"""
        try:
            # Try to parse as JSON first
            if response.startswith('{') and response.endswith('}'):
                return json.loads(response)
            
            # Extract JSON from response if it's wrapped in other text
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Fallback: parse as text
            return self._parse_text_response(response)
            
        except json.JSONDecodeError:
            logger.warning("Failed to parse AI response as JSON, falling back to text parsing")
            return self._parse_text_response(response)
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse text response into structured format"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        steps = []
        tips = []
        
        for line in lines:
            # Look for numbered steps
            if any(line.startswith(f"{i}.") for i in range(1, 10)):
                step = line.split('.', 1)[1].strip()
                steps.append(step)
            # Look for tips
            elif line.lower().startswith('tip'):
                tip = line.split(':', 1)[1].strip() if ':' in line else line
                tips.append(tip)
        
        return {
            "steps": steps[:5],  # Limit to 5 steps
            "tips": tips[:3],    # Limit to 3 tips
            "duration": None
        }
    
    def _determine_category(self, mood: str, goal: str) -> RoutineCategory:
        """Determine routine category based on mood and goal"""
        mood_lower = mood.lower()
        goal_lower = goal.lower()
        
        # Category mapping based on keywords
        if any(word in mood_lower for word in ['anxious', 'stressed', 'overwhelmed']):
            return RoutineCategory.MINDFULNESS
        elif any(word in mood_lower for word in ['tired', 'low energy', 'sluggish']):
            return RoutineCategory.PHYSICAL
        elif any(word in goal_lower for word in ['creative', 'art', 'write', 'music']):
            return RoutineCategory.CREATIVE
        elif any(word in goal_lower for word in ['social', 'connect', 'friends', 'family']):
            return RoutineCategory.SOCIAL
        elif any(word in goal_lower for word in ['relax', 'calm', 'peaceful']):
            return RoutineCategory.RELAXATION
        elif any(word in goal_lower for word in ['productive', 'focus', 'work']):
            return RoutineCategory.PRODUCTIVITY
        else:
            return RoutineCategory.EMOTIONAL
    
    def _determine_priority(self, mood: str) -> PriorityLevel:
        """Determine priority level based on mood intensity"""
        mood_lower = mood.lower()
        
        if any(word in mood_lower for word in ['crisis', 'emergency', 'urgent', 'severe']):
            return PriorityLevel.URGENT
        elif any(word in mood_lower for word in ['very', 'extremely', 'really', 'intense']):
            return PriorityLevel.HIGH
        elif any(word in mood_lower for word in ['somewhat', 'a bit', 'slightly']):
            return PriorityLevel.LOW
        else:
            return PriorityLevel.MEDIUM
    
    def _format_history(self, history: List[Dict]) -> str:
        """Format user history for prompt context"""
        if not history:
            return "No previous routines"
        
        formatted = []
        for routine in history[-3:]:  # Use last 3 routines
            formatted.append(f"Mood: {routine.get('mood')}, Goal: {routine.get('goal')}")
        
        return "; ".join(formatted)
    
    def _fallback_routine(self, request: GenerateRequest) -> GenerateResponse:
        """Provide fallback routine when AI fails"""
        logger.info("Using fallback routine")
        
        # Basic fallback routines based on mood
        fallback_routines = {
            "stressed": {
                "steps": [
                    "Take 5 deep breaths, inhaling for 4 counts and exhaling for 6 counts",
                    "Step outside or near a window for fresh air and natural light",
                    "Write down 3 things you're grateful for today"
                ],
                "category": RoutineCategory.MINDFULNESS,
                "priority": PriorityLevel.HIGH
            },
            "tired": {
                "steps": [
                    "Drink a glass of water to rehydrate",
                    "Do 5 gentle stretches or light movement",
                    "Take a 5-minute walk or do some light exercise"
                ],
                "category": RoutineCategory.PHYSICAL,
                "priority": PriorityLevel.MEDIUM
            },
            "anxious": {
                "steps": [
                    "Practice the 5-4-3-2-1 grounding technique",
                    "Listen to calming music or nature sounds for 5 minutes",
                    "Call or text someone you care about"
                ],
                "category": RoutineCategory.MINDFULNESS,
                "priority": PriorityLevel.HIGH
            }
        }
        
        mood_key = next((key for key in fallback_routines.keys() if key in request.mood.lower()), "stressed")
        fallback = fallback_routines[mood_key]
        
        return GenerateResponse(
            steps=fallback["steps"],
            estimated_duration=15,
            category=fallback["category"],
            priority=fallback["priority"],
            tips=["Take your time with each step", "Focus on the present moment", "Be kind to yourself"]
        )