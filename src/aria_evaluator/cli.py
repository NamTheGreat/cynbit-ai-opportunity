import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from aria_evaluator.pipeline import AriaEvaluationPipeline

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Aria Autonomous Codebase Evaluator CLI")
    parser.add_argument("path", help="Path to local repository or folder to evaluate")
    parser.add_argument("--role", default="Backend / AI Engineer", help="Role target for evaluation rubric")
    parser.add_argument("--name", default=None, help="Candidate or project name")

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    if not target_path.exists():
        console.print(f"[bold red]Error: Path '{target_path}' does not exist.[/bold red]")
        sys.exit(1)

    console.print(Panel(f"[bold cyan]Running Aria Autonomous Multi-Agent Evaluation on:[/bold cyan] {target_path}", title="Aria Evaluator"))

    pipeline = AriaEvaluationPipeline()
    result = pipeline.evaluate_directory(str(target_path), target_name=args.name, role_target=args.role)

    # Summary table
    table = Table(title="Evaluation Scorecard", show_header=True, header_style="bold magenta")
    table.add_column("Dimension", style="cyan")
    table.add_column("Score (0-100)", justify="right")
    table.add_column("Key Agent Observation", style="white")

    for dim, score in result.dimension_scores.items():
        table.add_row(dim, f"{score:.1f}", "")

    console.print(table)

    rec_color = "green" if "HIRE" in result.recommendation.value else "yellow" if "LEANING" in result.recommendation.value else "red"
    console.print(Panel(
        f"[bold]Overall Rubric Score:[/bold] [bold cyan]{result.overall_score}/100[/bold cyan]\n"
        f"[bold]Hiring Recommendation:[/bold] [{rec_color}]{result.recommendation.value}[/{rec_color}]\n\n"
        f"[bold]Executive Summary:[/bold]\n{result.executive_summary}",
        title="Final Recommendation"
    ))

    if result.security_findings:
        sec_table = Table(title="Static Security Findings", show_header=True, header_style="bold red")
        sec_table.add_column("Rule ID", style="dim")
        sec_table.add_column("Severity")
        sec_table.add_column("Title")
        sec_table.add_column("Location")

        for sf in result.security_findings:
            sev_color = "red" if sf.severity == "CRITICAL" else "yellow" if sf.severity == "HIGH" else "white"
            sec_table.add_row(sf.rule_id, f"[{sev_color}]{sf.severity}[/{sev_color}]", sf.title, f"{sf.file_path}:{sf.line_number}")

        console.print(sec_table)


if __name__ == "__main__":
    main()
