import json

from google import genai
from google.genai import types

from config.config import Config
from redisClient.redis_client import redis_client

config = Config()

client = genai.Client(api_key=config.GEMINI_API_KEY)


def convert_history(history):
    gemini_history = []

    for msg in history:
        role = "model" if msg["role"] == "assistant" else "user"

        gemini_history.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": msg["content"]
                    }
                ]
            }
        )

    return gemini_history


def ask_gemini(message: str, history: list, items) -> str:
    sys_instruct = (
        f"You are a helpful helper to a shopping site. "
        f"These are the details about the items in stock: {items}. "
        "Users can ask about products or general questions. "
        "If quantity is 0 inform them that the product is out of stock."
    )
    message_history = convert_history(history)
    chat = client.chats.create(
        model="gemini-2.5-flash",
        history=message_history,
        config=types.GenerateContentConfig(
            temperature=1.5,
            system_instruction=sys_instruct
        )
    )

    try:
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        print(f"Gemini Server Error: {e}")


async def add_message(session_id: str, role: str, content: str):
    key = f"chat:{session_id}"

    message = {
        "role": role,
        "content": content
    }

    await redis_client.rpush(key, json.dumps(message))
    await redis_client.expire(key, 86400)


async def get_history(session_id: str) -> list[dict]:
    key = f"chat:{session_id}"
    messages = await redis_client.lrange(key, 0, -1)

    return [json.loads(message) for message in messages]
