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

    history = await gemini_service.get_history(request.session_id)

    answer = gemini_service.ask_gemini(
        message=request.message,
        history=history,
        items=items)

    await gemini_service.add_message(request.session_id, "user", request.message)

    await gemini_service.add_message(request.session_id, "assistant", answer)

    return ChatResponse(answer=answer)
