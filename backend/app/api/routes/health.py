from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Health check endpoint")
def health_check():
    return {
        "status": "healthy",
        "service": "EquityMind AI Backend",
        "version": "1.0.0",
    }
