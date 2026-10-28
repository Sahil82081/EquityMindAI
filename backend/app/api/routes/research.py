from fastapi import APIRouter, HTTPException, status
from app.schemas.research import ResearchRequest, ResearchResponse
from app.services.research_service import create_research, get_research

router = APIRouter()


@router.post(
    "",
    response_model=ResearchResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Start research on a company",
)
def start_research(request: ResearchRequest):
    return create_research(request.company)


@router.get(
    "/{research_id}",
    response_model=ResearchResponse,
    summary="Get research results by research ID",
)
def get_research_by_id(research_id: str):
    res = get_research(research_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Research with ID '{research_id}' was not found",
        )
    return res
