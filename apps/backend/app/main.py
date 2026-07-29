from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for the ModelForge MLOps platform.",
)

app.include_router(health_router)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to ModelForge API",
        "version": settings.app_version,
        "docs": "/docs",
    }