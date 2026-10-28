from fastapi import APIRouter
from . import health, company, research, copilot

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(company.router, prefix="/company", tags=["Company"])
api_router.include_router(research.router, prefix="/research", tags=["Research"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["Copilot"])

__all__ = ["api_router"]
