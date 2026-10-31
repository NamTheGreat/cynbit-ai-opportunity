from abc import ABC, abstractmethod
from typing import Dict, Any, List
from aria_evaluator.models import AgentFinding, CodeMetric, SecurityVulnerability


class BaseEvaluationAgent(ABC):
    """
    Abstract base class for Aria Evaluator specialized agents.
    """

    def __init__(self, name: str, dimension: str):
        self.name = name
        self.dimension = dimension

    @abstractmethod
    def evaluate(
        self,
        files: Dict[str, str],
        metrics: CodeMetric,
        security_findings: List[SecurityVulnerability]
    ) -> AgentFinding:
        pass
