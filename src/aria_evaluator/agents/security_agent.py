from typing import Dict, List
from aria_evaluator.agents.base import BaseEvaluationAgent
from aria_evaluator.models import AgentFinding, CodeMetric, SecurityVulnerability, SeverityEnum


class SecurityEvaluationAgent(BaseEvaluationAgent):
    """
    Evaluates codebase security posture, input validation, authentication,
    and exposure to OWASP Top 10 API vulnerabilities.
    """

    def __init__(self):
        super().__init__(name="Aria-SecurityAgent", dimension="Security & Access Control")

    def evaluate(
        self,
        files: Dict[str, str],
        metrics: CodeMetric,
        security_findings: List[SecurityVulnerability]
    ) -> AgentFinding:
        critical_count = sum(1 for f in security_findings if f.severity == SeverityEnum.CRITICAL)
        high_count = sum(1 for f in security_findings if f.severity == SeverityEnum.HIGH)
        medium_count = sum(1 for f in security_findings if f.severity == SeverityEnum.MEDIUM)

        # Baseline score: 95
        score = 95.0
        score -= critical_count * 25.0
        score -= high_count * 15.0
        score -= medium_count * 5.0
        score = max(10.0, min(100.0, score))

        strengths = []
        concerns = []

        # Check for positive security patterns
        has_env_validation = any("zod" in content.lower() and "env" in content.lower() for content in files.values())
        has_ssrf_guards = any("isprivate" in content.lower() or "cidr" in content.lower() for content in files.values())
        has_hmac_or_timing_safe = any("timingsafeequal" in content.lower() or "hmac" in content.lower() for content in files.values())

        if has_env_validation:
            strengths.append("Enforces strict boot-time environment schema validation preventing runtime leaks.")
            score = min(100.0, score + 5.0)
        if has_ssrf_guards:
            strengths.append("Contains explicit SSRF defense and private CIDR network boundary checks.")
            score = min(100.0, score + 5.0)
        if has_hmac_or_timing_safe:
            strengths.append("Employs constant-time signature comparison resisting side-channel timing attacks.")
            score = min(100.0, score + 5.0)

        if critical_count > 0:
            concerns.append(f"Identified {critical_count} critical security issues (e.g., hardcoded secrets or dynamic eval).")
        if high_count > 0:
            concerns.append(f"Identified {high_count} high-severity issues requiring architectural remediation.")
        if not has_env_validation and not has_ssrf_guards:
            concerns.append("Lacks explicit input/URL allowlisting or environment variable contract enforcement.")

        if score >= 85:
            observations = "Exceptional defensive coding practices with robust credential handling, boundary checks, and input sanitization."
        elif score >= 70:
            observations = "Sound security baseline with minor exposure areas that can be addressed via standard middleware."
        else:
            observations = "Significant vulnerabilities observed that expose the application to unauthorized access or injection."

        return AgentFinding(
            agent_name=self.name,
            dimension=self.dimension,
            dimension_score=round(score, 1),
            strengths=strengths,
            concerns=concerns,
            key_observations=observations,
        )
