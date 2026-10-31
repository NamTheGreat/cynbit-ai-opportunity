from datetime import datetime, timezone
from typing import Dict, List
import uuid
from aria_evaluator.config import settings
from aria_evaluator.models import (
    CandidateEvaluationResult,
    AgentFinding,
    CodeMetric,
    SecurityVulnerability,
    HiringRecommendation,
)


class SynthesisEvaluationAgent:
    """
    Synthesizes findings from domain agents, calibrates rubric weights,
    determines hiring recommendations, and produces constructive candidate feedback.
    """

    def synthesize(
        self,
        target_name: str,
        role_target: str,
        metrics: CodeMetric,
        security_findings: List[SecurityVulnerability],
        agent_findings: Dict[str, AgentFinding]
    ) -> CandidateEvaluationResult:
        sec_score = agent_findings.get("security", AgentFinding(agent_name="Sec", dimension="Security", dimension_score=70.0, key_observations="")).dimension_score
        arch_score = agent_findings.get("architecture", AgentFinding(agent_name="Arch", dimension="Architecture", dimension_score=70.0, key_observations="")).dimension_score
        clean_score = agent_findings.get("clean_code", AgentFinding(agent_name="Clean", dimension="Clean", dimension_score=70.0, key_observations="")).dimension_score
        
        # Complexity dimension score: 100 base, decremented by complexity penalty
        complexity_score = max(30.0, min(100.0, 100.0 - (metrics.avg_cyclomatic_complexity * 4.0) - (len(metrics.complexity_hotspots) * 5.0)))

        # Weighted calculation
        overall = (
            sec_score * settings.weight_security +
            arch_score * settings.weight_architecture +
            clean_score * settings.weight_clean_code +
            complexity_score * settings.weight_complexity
        )
        overall = round(max(0.0, min(100.0, overall)), 1)

        # Recommendation calibration
        if overall >= settings.strong_hire_threshold:
            recommendation = HiringRecommendation.STRONG_HIRE
        elif overall >= settings.hire_threshold:
            recommendation = HiringRecommendation.HIRE
        elif overall >= settings.leaning_hire_threshold:
            recommendation = HiringRecommendation.LEANING_HIRE
        elif overall >= settings.leaning_reject_threshold:
            recommendation = HiringRecommendation.LEANING_REJECT
        else:
            recommendation = HiringRecommendation.STRONG_REJECT

        # Constructive feedback synthesis
        feedback: List[str] = []
        for af in agent_findings.values():
            for c in af.concerns:
                feedback.append(f"[{af.dimension}] {c}")
        if not feedback:
            feedback.append("No critical defects observed; maintain current architectural discipline.")

        # Executive summary
        exec_summary = (
            f"Candidate codebase evaluated across {metrics.total_files} files ({metrics.total_loc} lines of code). "
            f"Demonstrated an overall score of {overall}/100 resulting in a '{recommendation.value}' recommendation. "
            f"Architecture scored {arch_score}/100 and Security scored {sec_score}/100, showing strong "
            f"foundational competence with {len(security_findings)} static security alert(s)."
        )

        return CandidateEvaluationResult(
            evaluation_id=f"eval-{uuid.uuid4().hex[:8]}",
            target_name=target_name,
            role_target=role_target,
            overall_score=overall,
            recommendation=recommendation,
            metrics=metrics,
            dimension_scores={
                "Security & Access Control": sec_score,
                "Architecture & Modularity": arch_score,
                "Clean Code & Testability": clean_score,
                "Complexity & Maintainability": round(complexity_score, 1),
            },
            security_findings=security_findings,
            agent_breakdowns=agent_findings,
            executive_summary=exec_summary,
            constructive_feedback=feedback[:6],
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )
