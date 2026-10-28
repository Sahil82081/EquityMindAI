from fastapi import APIRouter
from app.schemas.copilot import CopilotRequest, CopilotResponse
from app.services.copilot_service import answer_copilot_question

router = APIRouter()


@router.post("", response_model=CopilotResponse, summary="Ask research copilot a question")
def copilot_query(request: CopilotRequest):
    return answer_copilot_question(request)
