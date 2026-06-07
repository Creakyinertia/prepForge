from fastapi import FastAPI

from features.auth.router import router as auth_router


app = FastAPI(
    title="PrepForge API",
    version="1.0.0",
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
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