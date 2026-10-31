import ast
import re
from pathlib import Path
from typing import Dict, Any, List
from aria_evaluator.models import CodeMetric


class ASTCodeAnalyzer:
    """
    Analyzes codebase structure, extracts function/class metrics,
    and calculates Cyclomatic Complexity across Python, TypeScript, and JavaScript.
    """

    def analyze_python_file(self, content: str, file_name: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self._heuristic_analyze(content, file_name)

        functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

        total_complexity = 0
        hotspots = []

        for fn in functions:
            fn_complexity = 1
            for node in ast.walk(fn):
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.ExceptHandler, ast.With, ast.Assert)):
                    fn_complexity += 1
                elif isinstance(node, ast.BoolOp):
                    fn_complexity += len(node.values) - 1

            total_complexity += fn_complexity
            if fn_complexity >= 10:
                hotspots.append(f"{file_name}:{fn.name} (complexity={fn_complexity})")

        loc = len([line for line in content.splitlines() if line.strip() and not line.strip().startswith("#")])
        avg_comp = total_complexity / max(1, len(functions))

        return {
            "loc": loc,
            "functions": len(functions),
            "classes": len(classes),
            "total_complexity": total_complexity,
            "avg_complexity": avg_comp,
            "max_complexity": max([1] + [total_complexity]),
            "hotspots": hotspots,
        }

    def analyze_ts_js_file(self, content: str, file_name: str) -> Dict[str, Any]:
        lines = [line.strip() for line in content.splitlines()]
        loc = len([l for l in lines if l and not l.startswith("//") and not l.startswith("/*")])

        # Functions & classes regex
        functions = len(re.findall(r'(?:function\s+\w+|const\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>|\b\w+\s*\([^)]*\)\s*:\s*[^={]+=>)', content))
        classes = len(re.findall(r'\bclass\s+\w+', content))

        # Branching keyword count for Cyclomatic Complexity approximation: M = E - N + 2P
        branch_patterns = [
            r'\bif\s*\(',
            r'\belse\s+if\s*\(',
            r'\bfor\s*\(',
            r'\bwhile\s*\(',
            r'\bcase\s+[^:]+:',
            r'\bcatch\s*\(',
            r'&&',
            r'\|\|',
            r'\?\?',
            r'\?[^:\n]+\:',  # ternary
        ]
        
        branch_count = 0
        for pattern in branch_patterns:
            branch_count += len(re.findall(pattern, content))

        complexity = max(1, branch_count + 1)
        hotspots = []
        if complexity >= 15:
            hotspots.append(f"{file_name} (module complexity={complexity})")

        return {
            "loc": loc,
            "functions": max(1, functions),
            "classes": classes,
            "total_complexity": complexity,
            "avg_complexity": complexity / max(1, functions),
            "max_complexity": complexity,
            "hotspots": hotspots,
        }

    def _heuristic_analyze(self, content: str, file_name: str) -> Dict[str, Any]:
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        return {
            "loc": len(lines),
            "functions": 1,
            "classes": 0,
            "total_complexity": 1,
            "avg_complexity": 1.0,
            "max_complexity": 1,
            "hotspots": [],
        }

    def aggregate_metrics(self, file_results: List[Dict[str, Any]]) -> CodeMetric:
        if not file_results:
            return CodeMetric()

        total_files = len(file_results)
        total_loc = sum(r["loc"] for r in file_results)
        total_fn = sum(r["functions"] for r in file_results)
        total_cls = sum(r["classes"] for r in file_results)
        total_comp = sum(r["total_complexity"] for r in file_results)
        max_comp = max(r["max_complexity"] for r in file_results)

        hotspots = []
        for r in file_results:
            hotspots.extend(r["hotspots"])

        avg_comp = round(total_comp / max(1, total_fn), 2)

        return CodeMetric(
            total_files=total_files,
            total_loc=total_loc,
            total_functions=total_fn,
            total_classes=total_cls,
            avg_cyclomatic_complexity=avg_comp,
            max_cyclomatic_complexity=max_comp,
            complexity_hotspots=hotspots[:5],
        )
