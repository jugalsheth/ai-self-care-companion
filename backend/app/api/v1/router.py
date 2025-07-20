from fastapi import APIRouter

from app.api.v1 import auth, routines, analytics, moods

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(routines.router, prefix="/routines", tags=["routines"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(moods.router, prefix="/moods", tags=["moods"])