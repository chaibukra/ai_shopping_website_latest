

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
    items = await item_service.get_all_items()

    answer = gemini_service.ask_gemini(
        message=request.message,
        history=request.history,
        items=items
    )

    return ChatResponse(answer=answer)
