from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.health import router as health_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered Cloud Reliability and Root-Cause Intelligence"
)


app.include_router(
    health_router,
    prefix=settings.API_V1_PREFIX,
    tags=["Health"]
)


@app.get("/")
def root():
    return {
        "message": "Welcome to TraceWise API",
        "version": settings.APP_VERSION
    }