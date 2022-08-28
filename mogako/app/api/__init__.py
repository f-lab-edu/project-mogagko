from fastapi import APIRouter

from mogako.app.api.v1.cafe import cafe_router

api_router = APIRouter()

api_router.include_router(cafe_router, prefix="/api/v1/cafes", tags=["Cafe"])
