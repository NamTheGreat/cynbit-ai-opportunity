import pytest
from aria_evaluator.pipeline import AriaEvaluationPipeline
from aria_evaluator.models import HiringRecommendation


def test_pipeline_evaluates_clean_codebase():
    pipeline = AriaEvaluationPipeline()
    files = {
        "src/server.py": """
import os
from pydantic import BaseModel

class Config(BaseModel):
    env: str = os.getenv("ENV", "production")

def is_safe_ip(ip: str) -> bool:
    if ip == "127.0.0.1" or ip == "169.254.169.254":
        return False
    return True
""",
        "tests/test_server.py": """
def test_safe_ip():
    assert True
""",
        "schema.prisma": "datasource db { provider = 'postgresql' }"
    }

    result = pipeline.evaluate_files(files, target_name="Clean Repo")
    assert result.overall_score >= 70.0
    assert result.recommendation in [HiringRecommendation.STRONG_HIRE, HiringRecommendation.HIRE]
    assert len(result.security_findings) == 0


def test_pipeline_evaluates_vulnerable_codebase():
    pipeline = AriaEvaluationPipeline()
    files = {
        "vulnerable.py": """
API_KEY = "AKIA1234567890SECRETKEY12345"
def execute_code(cmd):
    return eval(cmd)
"""
    }

    result = pipeline.evaluate_files(files, target_name="Vulnerable Repo")
    assert result.overall_score < 70.0
    assert len(result.security_findings) >= 2
    assert any(f.severity == "CRITICAL" for f in result.security_findings)
