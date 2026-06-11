from fastapi import FastAPI
import models
from features.auth.router import router as auth_router
from features.roadmaps.router import (
    router as roadmap_router
)
from features.topics.router import (
    router as topic_router
)
from features.progress.router import (
    router as progress_router
)
from features.revisions.router import (
    router as revision_router,
)
from features.notes.router import (
    router as note_router,
)
from features.dashboard.router import (
    router as dashboard_router,
)
from features.resources.router import (
    router as resource_router,
)
from features.questions.router import (
    router as question_router,
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
app.include_router(
    progress_router,
    prefix="/progress",
    tags=["Progress"],
)
app.include_router(
    revision_router,
    prefix="/revisions",
    tags=["Revisions"],
)
app.include_router(
    note_router,
    prefix="/notes",
    tags=["Notes"],
)
app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"],
)
app.include_router(
    resource_router,
    prefix="/resources",
    tags=["Resources"],
)
app.include_router(
    question_router,
    prefix="/questions",
    tags=["Questions"],
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }