from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Health check endpoint")
@router.head("/health", include_in_schema=False)
def health_check():
    return {
        "status": "healthy",
        "service": "EquityMind AI Backend",
        "version": "1.0.0",
    }
