from fastapi import FastAPI
import models
from features.auth.router import router as auth_router
from features.roadmaps.router import (
    router as roadmap_router
)
from features.topics.router import (
    router as topic_router
)

app = FastAPI(
    title="PrepForge API",
    version="1.0.0",
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    roadmap_router,
    prefix="/roadmaps",
    tags=["Roadmaps"],
)
app.include_router(
    topic_router,
    prefix="/topics",
    tags=["topics"],
)


@app.get("/")
def root():
    return {
        "message": "PrepForge API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }