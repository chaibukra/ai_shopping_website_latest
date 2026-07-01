from fastapi import APIRouter

from model.chat_request import ChatRequest
from model.chat_response import ChatResponse
from service import gemini_service, item_service

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.post("/ask", response_model=ChatResponse)
async def chat(request: ChatRequest):

    answer = await gemini_service.chat_orchestrator(request.session_id, request.message)

    return ChatResponse(answer=answer)
