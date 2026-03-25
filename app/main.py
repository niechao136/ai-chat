import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router
from app.services.auth_service import AuthError
from app.services.chat_graph import init_graph
import logging.config
from contextlib import asynccontextmanager

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},
    "root": {"level": "INFO", "handlers": ["console"]},
}

logging.config.dictConfig(LOGGING_CONFIG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 生产环境强制校验持久化存储配置
    if os.getenv("ENV") == "production" and "MEMORY" in settings.PROJECT_NAME:
        raise RuntimeError("Production environment must not use MemorySaver")
        
    app.state.graph = await init_graph()
    yield
    if hasattr(app.state.graph, "checkpointer") and hasattr(app.state.graph.checkpointer, "aclose"):
        await app.state.graph.checkpointer.aclose()

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0", lifespan=lifespan)

@app.exception_handler(AuthError)
async def auth_exception_handler(request: Request, exc: AuthError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

app.include_router(auth_router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(chat_router, prefix=settings.API_V1_STR, tags=["chat"])

@app.get("/health")
async def health():
    return {"status": "ok"}
