from fastapi import FastAPI

from config.config import Config
from controller.user_controller import router as user_router
from controller.item_controller import router as item_router
from controller.user_favorite_item_controller import router as user_favorite_item_router
from controller.order_controller import router as order_router
from controller.auth_controller import router as auth_router
from controller.predict_controller import router as predict_router
from controller.gemini_controller import router as gemini_router
from fastapi.middleware.cors import CORSMiddleware
from repository.database import database


config = Config()

if config.ENVIRONMENT == "local":
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
else:
    allowed_origins = [
        config.FRONTEND_URL,
    ]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(user_router)
app.include_router(item_router)
app.include_router(user_favorite_item_router)
app.include_router(order_router)
app.include_router(auth_router)
app.include_router(predict_router)
app.include_router(gemini_router)

