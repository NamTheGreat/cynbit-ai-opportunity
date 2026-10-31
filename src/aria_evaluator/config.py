import os
from pydantic import BaseModel


class EvaluatorSettings(BaseModel):
    app_name: str = "Aria Studio Evaluator"
    version: str = "1.0.0"
    default_role: str = "Backend / AI Engineer"
    
    # Supported file extensions for static code parsing
    supported_extensions: list[str] = [
        ".py", ".ts", ".tsx", ".js", ".jsx", ".prisma", ".sql", ".json", ".md"
    ]
    
    # Weight distributions for overall rubric scoring
    weight_security: float = 0.30
    weight_architecture: float = 0.30
    weight_clean_code: float = 0.20
    weight_complexity: float = 0.20

    # Minimum thresholds
    strong_hire_threshold: float = 85.0
    hire_threshold: float = 72.0
    leaning_hire_threshold: float = 60.0
    leaning_reject_threshold: float = 45.0

    # API Keys / Environment
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    use_mock_llm_fallback: bool = True


settings = EvaluatorSettings()
