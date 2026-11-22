from typing import List
from pydantic import BaseModel, Field

class ResumeMatchReport(BaseModel):
    overall_match_score: int = Field(..., ge=0, le=100)
    estimated_years_experience: float
    matched_skills: List[str]
    missing_skills: List[str]
    candidate_strengths: List[str]
    improvement_suggestions: List[str]
    hiring_recommendation: str
