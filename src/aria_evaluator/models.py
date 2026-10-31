from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class SeverityEnum(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class HiringRecommendation(str, Enum):
    STRONG_HIRE = "STRONG_HIRE"
    HIRE = "HIRE"
    LEANING_HIRE = "LEANING_HIRE"
    LEANING_REJECT = "LEANING_REJECT"
    STRONG_REJECT = "STRONG_REJECT"


class CodeMetric(BaseModel):
    total_files: int = 0
    total_loc: int = 0
    total_functions: int = 0
    total_classes: int = 0
    avg_cyclomatic_complexity: float = 0.0
    max_cyclomatic_complexity: int = 0
    complexity_hotspots: List[str] = Field(default_factory=list)


class SecurityVulnerability(BaseModel):
    rule_id: str
    severity: SeverityEnum
    title: str
    description: str
    file_path: str
    line_number: Optional[int] = None
    cwe_id: Optional[str] = None
    remediation: str


class AgentFinding(BaseModel):
    agent_name: str
    dimension: str
    dimension_score: float = Field(ge=0.0, le=100.0)
    strengths: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)
    key_observations: str


class CandidateEvaluationResult(BaseModel):
    evaluation_id: str
    target_name: str
    role_target: str = "Backend / AI Engineer"
    overall_score: float = Field(ge=0.0, le=100.0)
    recommendation: HiringRecommendation
    metrics: CodeMetric
    dimension_scores: Dict[str, float] = Field(default_factory=dict)
    security_findings: List[SecurityVulnerability] = Field(default_factory=list)
    agent_breakdowns: Dict[str, AgentFinding] = Field(default_factory=dict)
    executive_summary: str
    constructive_feedback: List[str] = Field(default_factory=list)
    rubric_calibration_version: str = "1.0.0-aria-rubric"
    evaluated_at: str
