import pytest
from aria_evaluator.analyzers.ast_analyzer import ASTCodeAnalyzer


def test_ast_python_analyzer():
    analyzer = ASTCodeAnalyzer()
    python_code = """
def complex_function(a, b):
    if a > 0:
        if b > 0:
            return a + b
        else:
            return a - b
    elif a < 0:
        for i in range(10):
            print(i)
    return 0

class SampleService:
    def execute(self):
        pass
"""
    result = analyzer.analyze_python_file(python_code, "service.py")
    assert result["loc"] > 5
    assert result["functions"] == 2
    assert result["classes"] == 1
    assert result["total_complexity"] >= 4


def test_ast_ts_analyzer():
    analyzer = ASTCodeAnalyzer()
    ts_code = """
export function handleRequest(req: Request) {
    if (req.method === 'POST') {
        const body = req.body;
        if (body && body.isValid) {
            return { status: 200 };
        }
    }
    return { status: 400 };
}
"""
    result = analyzer.analyze_ts_js_file(ts_code, "handler.ts")
    assert result["loc"] > 3
    assert result["functions"] >= 1
    assert result["total_complexity"] >= 2
