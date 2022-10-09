from fastapi import APIRouter

from mogako.app.api.v1.cafe import cafe_router
from mogako.app.api.v1.crawling import crawling_router
from mogako.app.api.v1.user import user_router

api_router = APIRouter()

api_router.include_router(cafe_router, prefix="/api/v1/cafes", tags=["Cafe"])
api_router.include_router(user_router, prefix="/api/v1/users", tags=["User"])
api_router.include_router(crawling_router, prefix="/crawling", tags=["crawling"])
