from fastapi import FastAPI
from backend.connections.database import Base,engine
from backend.users.user  import router as user_router
from backend.users.user_profile import router as user_profile_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PrepForge",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(user_profile_router)


@app.get("/health-check")
def root():
    return {"message": "API is running"}