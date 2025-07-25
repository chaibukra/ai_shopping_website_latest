from pydantic import BaseConfig
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class Config(BaseConfig):
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")
    REDIS_TTL: int = 120
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRY_TIME: float = 20.0
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_USERNAME = os.getenv("REDIS_USERNAME", None)
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    REDIS_SSL = os.getenv("REDIS_SSL", "False").lower() == "true"
