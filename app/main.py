from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.auth import router as auth_router
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
    "root": {"level": "INFO", "handlers": ["console"]},
}

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.include_router(auth_router, prefix=settings.API_V1_STR, tags=["auth"])

@app.get("/health")
async def health():
    return {"status": "ok"}
