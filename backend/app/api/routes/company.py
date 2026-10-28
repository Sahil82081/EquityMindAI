from fastapi import APIRouter, Query
from app.schemas.company import CompanySearchResponse
from app.services.company_service import search_companies

router = APIRouter()


@router.get("/search", response_model=CompanySearchResponse, summary="Search companies by name or ticker")
def search(q: str = Query(default="", description="Search query string")):
    return search_companies(q)
