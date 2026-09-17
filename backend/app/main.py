"""
FastAPI application entrypoint.

Run with (from the backend/ directory, venv active):
    uvicorn app.main:app --reload --port 8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import init_indexes
from app.routers import auth, users, dashboard, resumes, prediction, career, skills, admin

app = FastAPI(
    title="Trajectory — Smart Placement Prediction Portal API",
    description="All 9 modules: Auth, Dashboard, Resume Upload/Analysis, Placement "
                "Prediction, Career Recommendation, Skill Gap Analysis, Learning "
                "Roadmap, Admin Dashboard",
    version="1.0.0",
)

origins = [o.strip() for o in settings.frontend_origin.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_indexes()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(resumes.router)
app.include_router(prediction.router)
app.include_router(career.router)
app.include_router(skills.router)
app.include_router(admin.router)


@app.get("/api/health", tags=["health"])
def health_check():
    return {"status": "ok"}
