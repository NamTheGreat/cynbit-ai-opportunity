from pathlib import Path
from typing import Dict, Optional, List
from aria_evaluator.analyzers.ast_analyzer import ASTCodeAnalyzer
from aria_evaluator.analyzers.security_scanner import StaticSecurityScanner
from aria_evaluator.analyzers.repo_ingestor import RepositoryIngestor
from aria_evaluator.agents.security_agent import SecurityEvaluationAgent
from aria_evaluator.agents.architecture_agent import ArchitectureEvaluationAgent
from aria_evaluator.agents.clean_code_agent import CleanCodeEvaluationAgent
from aria_evaluator.agents.synthesis_agent import SynthesisEvaluationAgent
from aria_evaluator.models import CandidateEvaluationResult, SecurityVulnerability


class AriaEvaluationPipeline:
    """
    End-to-end multi-agent evaluation pipeline.
    Parses codebase -> runs AST metrics & security scanners -> dispatches
    to specialized domain agents -> synthesizes calibrated score and report.
    """

    def __init__(self):
        self.ingestor = RepositoryIngestor()
        self.ast_analyzer = ASTCodeAnalyzer()
        self.security_scanner = StaticSecurityScanner()
        self.security_agent = SecurityEvaluationAgent()
        self.architecture_agent = ArchitectureEvaluationAgent()
        self.clean_code_agent = CleanCodeEvaluationAgent()
        self.synthesis_agent = SynthesisEvaluationAgent()

    def evaluate_directory(
        self,
        directory_path: str,
        target_name: Optional[str] = None,
        role_target: str = "Backend / AI Engineer"
    ) -> CandidateEvaluationResult:
        dir_name = target_name or Path(directory_path).name
        files = self.ingestor.ingest_directory(directory_path)
        return self.evaluate_files(files, target_name=dir_name, role_target=role_target)

    def evaluate_files(
        self,
        files: Dict[str, str],
        target_name: str = "Codebase Submission",
        role_target: str = "Backend / AI Engineer"
    ) -> CandidateEvaluationResult:
        file_metrics = []
        all_security_findings: List[SecurityVulnerability] = []

        for file_path, content in files.items():
            # AST Analysis
            if file_path.endswith(".py"):
                m = self.ast_analyzer.analyze_python_file(content, file_path)
            elif file_path.endswith((".ts", ".tsx", ".js", ".jsx")):
                m = self.ast_analyzer.analyze_ts_js_file(content, file_path)
            else:
                m = self.ast_analyzer._heuristic_analyze(content, file_path)
            file_metrics.append(m)

            # Security Scanning
            findings = self.security_scanner.scan_file(content, file_path)
            all_security_findings.extend(findings)

        aggregated_metrics = self.ast_analyzer.aggregate_metrics(file_metrics)

        # Multi-Agent Domain Evaluation
        sec_finding = self.security_agent.evaluate(files, aggregated_metrics, all_security_findings)
        arch_finding = self.architecture_agent.evaluate(files, aggregated_metrics, all_security_findings)
        clean_finding = self.clean_code_agent.evaluate(files, aggregated_metrics, all_security_findings)

        agent_findings = {
            "security": sec_finding,
            "architecture": arch_finding,
            "clean_code": clean_finding,
        }

        # Synthesis
        return self.synthesis_agent.synthesize(
            target_name=target_name,
            role_target=role_target,
            metrics=aggregated_metrics,
            security_findings=all_security_findings,
            agent_findings=agent_findings,
        )
