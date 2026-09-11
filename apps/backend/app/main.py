import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.api.routes.health import router as health_router
from app.api.routes.datasets import router as datasets_router
from app.api.routes.training import router as training_router

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("ModelForge API started successfully")
    logger.info("\n")
    logger.info("🚀 API: http://localhost:8000")
    logger.info("🛠️  Swagger UI: http://localhost:8000/docs")
    logger.info("❤️  Health check: http://localhost:8000/health")
    logger.info("\n")

    yield

    logger.info("ModelForge API stopped")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the ModelForge MLOps platform.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(datasets_router)
app.include_router(training_router)

@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to ModelForge API",
        "version": settings.app_version,
        "docs": "/docs",
    }