import json

from google import genai
from google.genai import types

from config.config import Config
from redisClient.redis_client import redis_client
from service import item_service

config = Config()

client = genai.Client(api_key=config.GEMINI_API_KEY)

WINDOW_SIZE = 10
MAX_MESSAGES = WINDOW_SIZE * 2
SUMMARY_TRIGGER = MAX_MESSAGES


def build_history_text(history: list) -> str:
    return "\n".join(f"{m['role']}: {m['content']}" for m in history)


def build_prompt(summary: str | None, messages: list, new_message: str, items):
    prompt = ""

    if summary:
        prompt += f"Conversation summary so far:\n{summary}\n\n"

    prompt += "Recent conversation:\n"

    prompt += build_history_text(messages)

    prompt += f"\nUser: {new_message}\n"

    prompt += (
        f"\nItems in store:\n{items}\n"
    )

    return prompt


async def ask_gemini(prompt) -> str:
    sys_instruct = (
        "You are a helpful shopping assistant. "
        "Use the provided summary and recent chat history."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=1.2,
                system_instruction=sys_instruct
            )
        )

        return response.text
    except Exception as e:
        print(f"Gemini Server Error: {e}")


async def add_message(session_id: str, role: str, content: str):
    key = f"chat:{session_id}:messages"

    message = {
        "role": role,
        "content": content
    }

    await redis_client.rpush(key, json.dumps(message))
    await redis_client.expire(key, 86400)


async def get_history(session_id: str) -> list[dict]:
    key = f"chat:{session_id}:messages"
    messages = await redis_client.lrange(key, -MAX_MESSAGES, -1)

    return [json.loads(message) for message in messages]


async def save_summary(session_id: str, summary: str):
    key = f"chat:{session_id}:summary"

    await redis_client.set(key, summary, ex=86400)


async def get_summary(session_id: str) -> str:
    summary_key = f"chat:{session_id}:summary"
    summary = await redis_client.get(summary_key)

    return summary


async def should_summarize(session_id: str) -> bool:
    key = f"chat:{session_id}:messages"

    length = await redis_client.llen(key)

    return length > 0 and length >= SUMMARY_TRIGGER


async def create_summary(history: list, old_summary: str | None) -> str:
    text = ""

    if old_summary:
        text += f"Previous summary:\n{old_summary}\n\n"

    text += build_history_text(history)

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"Summarize the following conversation clearly:\n\n{text}",
        config=types.GenerateContentConfig(
            temperature=0.3
        )
    )

    return response.text


async def chat_orchestrator(session_id: str, message: str) -> str:
    summary = await get_summary(session_id)
    history = await get_history(session_id)
    items = await item_service.get_all_items()

    prompt = build_prompt(summary, history, message, items)

    answer = await ask_gemini(prompt)

    await add_message(session_id, "user", message)

    await add_message(session_id, "assistant", answer)

    if await should_summarize(session_id):
        full_history = await get_history(session_id)
        new_summary = await create_summary(full_history, summary)
        await save_summary(session_id, new_summary)

        key = f"chat:{session_id}:messages"

        await redis_client.ltrim(key, -WINDOW_SIZE, -1)

    return answer
