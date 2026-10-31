from typing import Dict, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aria_evaluator.pipeline import AriaEvaluationPipeline
from aria_evaluator.models import CandidateEvaluationResult
from aria_evaluator.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="REST API for Aria Autonomous Technical Assessment & Code Quality Evaluator",
)

pipeline = AriaEvaluationPipeline()


class EvaluateCodeRequest(BaseModel):
    target_name: str = "Candidate Submission"
    role_target: str = "Backend / AI Engineer"
    files: Dict[str, str]


class EvaluatePathRequest(BaseModel):
    directory_path: str
    target_name: Optional[str] = None
    role_target: str = "Backend / AI Engineer"


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.app_name, "version": settings.version}


@app.get("/api/v1/rubrics")
def get_rubrics():
    return {
        "weights": {
            "security": settings.weight_security,
            "architecture": settings.weight_architecture,
            "clean_code": settings.weight_clean_code,
            "complexity": settings.weight_complexity,
        },
        "thresholds": {
            "strong_hire": settings.strong_hire_threshold,
            "hire": settings.hire_threshold,
            "leaning_hire": settings.leaning_hire_threshold,
            "leaning_reject": settings.leaning_reject_threshold,
        },
    }


@app.post("/api/v1/evaluate/code", response_model=CandidateEvaluationResult)
def evaluate_code(req: EvaluateCodeRequest):
    if not req.files:
        raise HTTPException(status_code=400, detail="No source code files provided in payload.")
    return pipeline.evaluate_files(req.files, target_name=req.target_name, role_target=req.role_target)


@app.post("/api/v1/evaluate/local", response_model=CandidateEvaluationResult)
def evaluate_local_directory(req: EvaluatePathRequest):
    try:
        return pipeline.evaluate_directory(
            req.directory_path,
            target_name=req.target_name,
            role_target=req.role_target
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
