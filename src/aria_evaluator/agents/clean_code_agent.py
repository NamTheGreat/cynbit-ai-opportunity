from typing import Dict, List
from aria_evaluator.agents.base import BaseEvaluationAgent
from aria_evaluator.models import AgentFinding, CodeMetric, SecurityVulnerability


class CleanCodeEvaluationAgent(BaseEvaluationAgent):
    """
    Evaluates clean code principles, test coverage indicators,
    type annotations, documentation quality, and complexity hotspots.
    """

    def __init__(self):
        super().__init__(name="Aria-CleanCodeAgent", dimension="Clean Code & Testability")

    def evaluate(
        self,
        files: Dict[str, str],
        metrics: CodeMetric,
        security_findings: List[SecurityVulnerability]
    ) -> AgentFinding:
        score = 80.0
        strengths = []
        concerns = []

        # Check for test files
        test_files = [f for f in files if "test" in f.lower() or "spec" in f.lower()]
        has_tests = len(test_files) > 0

        # Check for typing
        has_typescript = any(f.endswith(".ts") or f.endswith(".tsx") for f in files)
        has_python_types = any("->" in content and ": " in content for f, content in files.items() if f.endswith(".py"))

        # Check documentation
        has_docs = any(f.endswith(".md") for f in files)

        if has_tests:
            strengths.append(f"Dedicated test coverage present with {len(test_files)} test suite file(s).")
            score += 10.0
        else:
            concerns.append("No automated test suites identified; risks regressions during maintenance.")
            score -= 15.0

        if has_typescript or has_python_types:
            strengths.append("Strong static typing utilized across core service contracts and data models.")
            score += 5.0
        else:
            concerns.append("Limited type hints observed; increases cognitive load and type mismatch risks.")

        if has_docs:
            strengths.append("Comprehensive project documentation and technical audit reports provided.")
            score += 5.0

        # Complexity penalty
        if metrics.avg_cyclomatic_complexity > 8.0:
            concerns.append(f"High average cyclomatic complexity ({metrics.avg_cyclomatic_complexity:.1f}) in function logic.")
            score -= 10.0
        elif metrics.avg_cyclomatic_complexity <= 4.0:
            strengths.append(f"Low cyclomatic complexity ({metrics.avg_cyclomatic_complexity:.1f}) promotes high readability.")
            score += 5.0

        if metrics.complexity_hotspots:
            concerns.append(f"{len(metrics.complexity_hotspots)} complexity hotspot(s) could benefit from refactoring.")

        score = max(20.0, min(100.0, score))

        if score >= 85:
            observations = "Exemplary code craft: thorough test suites, comprehensive type annotations, and minimal cognitive complexity."
        elif score >= 70:
            observations = "Clean, readable implementation with satisfactory maintainability and good documentation."
        else:
            observations = "Requires refactoring for cyclomatic complexity reduction and missing unit test coverage."

        return AgentFinding(
            agent_name=self.name,
            dimension=self.dimension,
            dimension_score=round(score, 1),
            strengths=strengths,
            concerns=concerns,
            key_observations=observations,
        )
