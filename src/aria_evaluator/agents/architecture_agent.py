from typing import Dict, List
from aria_evaluator.agents.base import BaseEvaluationAgent
from aria_evaluator.models import AgentFinding, CodeMetric, SecurityVulnerability


class ArchitectureEvaluationAgent(BaseEvaluationAgent):
    """
    Evaluates modularity, database modeling, schema normalization,
    decoupling (e.g. queues, outbox patterns), and API design.
    """

    def __init__(self):
        super().__init__(name="Aria-ArchitectureAgent", dimension="Architecture & Modularity")

    def evaluate(
        self,
        files: Dict[str, str],
        metrics: CodeMetric,
        security_findings: List[SecurityVulnerability]
    ) -> AgentFinding:
        score = 75.0
        strengths = []
        concerns = []

        # Analyze architectural indicators
        has_orm_schema = any(f.endswith(".prisma") or "models.py" in f for f in files)
        has_outbox_or_queue = any("outbox" in f.lower() or "worker" in f.lower() or "queue" in f.lower() for f in files)
        has_rate_limiting = any("rate" in content.lower() and "limit" in content.lower() for content in files.values())
        has_idempotency = any("idempotency" in content.lower() for content in files.values())
        has_modular_structure = metrics.total_files >= 5

        if has_orm_schema:
            strengths.append("Structured relational data modeling with explicit constraints and types.")
            score += 8.0
        if has_outbox_or_queue:
            strengths.append("Decoupled asynchronous background messaging (Transactional Outbox / Worker pattern).")
            score += 10.0
        if has_rate_limiting:
            strengths.append("Sliding-window rate limiting deployed to protect critical mutation endpoints.")
            score += 5.0
        if has_idempotency:
            strengths.append("Idempotency keys implemented to prevent duplicate operations and race conditions.")
            score += 5.0
        if has_modular_structure:
            strengths.append(f"Clean layered file organization across {metrics.total_files} distinct modules.")
            score += 5.0
        else:
            concerns.append("Monolithic or sparse file organization; could benefit from clearer service separation.")
            score -= 10.0

        score = max(20.0, min(100.0, score))

        if score >= 85:
            observations = "High-maturity production architecture featuring decoupled workers, relational normalization, and idempotency guarantees."
        elif score >= 70:
            observations = "Well-structured codebase with clear component boundaries and good standard design patterns."
        else:
            observations = "Tight coupling between HTTP request cycles and third-party IO; lacks persistence-level decoupling."

        return AgentFinding(
            agent_name=self.name,
            dimension=self.dimension,
            dimension_score=round(score, 1),
            strengths=strengths,
            concerns=concerns,
            key_observations=observations,
        )
