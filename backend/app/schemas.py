"""
Pydantic schemas for request validation and response serialization.

MongoDB's `_id` (an ObjectId) is always surfaced to the frontend as a
plain string `id` field — simplest approach, and matches what a JSON
API client expects.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


# ---------------- Auth ----------------

class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------------- Resume (modules 3 & 4) ----------------

class ResumeAnalysisOut(BaseModel):
    id: str
    filename: str
    ats_score: float
    word_count: int
    email: Optional[str]
    phone: Optional[str]
    sections_found: List[str]
    skills: List[str]
    suggestions: List[str]
    uploaded_at: datetime


# ---------------- Placement prediction (module 5) ----------------

class StudentInput(BaseModel):
    cgpa: float = Field(..., ge=0, le=10)
    tenth_percentage: float = Field(..., ge=0, le=100)
    twelfth_percentage: float = Field(..., ge=0, le=100)
    backlogs: int = Field(0, ge=0)
    internships: int = Field(0, ge=0)
    projects: int = Field(0, ge=0)
    certifications: int = Field(0, ge=0)
    aptitude_score: float = Field(..., ge=0, le=100)
    technical_score: float = Field(..., ge=0, le=100)
    communication_score: float = Field(..., ge=0, le=100)
    coding_score: float = Field(..., ge=0, le=100)
    branch: str


class PredictionResult(BaseModel):
    id: Optional[str] = None
    placement_probability: float
    placement_status: str
    # predicted_package_lpa: Optional[float]
    top_skill_gaps: List[str] = []
    created_at: Optional[datetime] = None


class PredictionHistoryOut(PredictionResult):
    cgpa: float
    branch: str


# ---------------- Career recommendation (module 6) ----------------

class CareerAlternative(BaseModel):
    career: str
    confidence: float


class CareerRecommendationOut(BaseModel):
    id: Optional[str] = None
    recommended_career: str
    confidence: float
    alternatives: List[CareerAlternative]
    created_at: Optional[datetime] = None


# ---------------- Skill gap analysis (module 7) ----------------

class SkillGapRequest(BaseModel):
    target_career: str
    known_skills: List[str] = Field(default_factory=list)
    use_latest_resume: bool = True


class SkillItem(BaseModel):
    skill: str
    weight: int


class SkillGapOut(BaseModel):
    target_career: str
    readiness_percent: float
    matched_skills: List[SkillItem]
    missing_skills: List[SkillItem]
    available_careers: List[str] = []


# ---------------- Learning roadmap (module 8) ----------------

class RoadmapStage(BaseModel):
    stage: int
    skill: str
    priority: str
    topics: List[str]


class RoadmapOut(BaseModel):
    target_career: str
    stages: List[RoadmapStage]


# ---------------- Admin dashboard (module 9) ----------------

class AdminStudentOut(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    total_predictions: int
    latest_placement_status: Optional[str] = None
    latest_probability: Optional[float] = None
    has_resume: bool
    latest_career: Optional[str] = None


class AdminStatsOut(BaseModel):
    total_students: int
    total_predictions: int
    placement_rate_percent: float
    # average_predicted_package: Optional[float] = None
    branch_breakdown: dict
    top_recommended_careers: dict


# ---------------- Dashboard ----------------

class DashboardOut(BaseModel):
    full_name: str
    email: EmailStr
    role: str
    member_since: datetime
    modules_unlocked: List[str]
    modules_upcoming: List[str]
    has_resume: bool = False
    latest_resume_score: Optional[float] = None
    total_predictions: int = 0
    latest_prediction: Optional[PredictionResult] = None
    latest_career: Optional[str] = None
