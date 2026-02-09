"""Pydantic schemas for request/response validation."""
from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    """Request schema for image analysis endpoint."""
    description: str = Field(..., max_length=200, description="Text description of the application")
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Validate and clean description."""
        return v.strip()


class AnalysisResponse(BaseModel):
    """Response schema for analysis endpoint."""
    analysis_summary: str = Field(..., description="AI-generated summary of the analysis")
    generated_files: Dict[str, str] = Field(..., description="Generated code files (file name -> file content)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_summary": "This is a food pantry management system...",
                "generated_files": {
                    "models.py": "# SQLAlchemy models...",
                    "main.py": "# FastAPI endpoints...",
                    "App.jsx": "// React component...",
                    "README.md": "# Setup instructions..."
                }
            }
        }
