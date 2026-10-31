import pytest
from aria_evaluator.analyzers.security_scanner import StaticSecurityScanner
from aria_evaluator.models import SeverityEnum


def test_security_scanner_detects_secrets():
    scanner = StaticSecurityScanner()
    code = 'api_key = "AKIA1234567890EXAMPLEKEY123"'
    findings = scanner.scan_file(code, "config.py")
    assert len(findings) == 1
    assert findings[0].rule_id == "SEC-R001"
    assert findings[0].severity == SeverityEnum.CRITICAL


def test_security_scanner_detects_eval():
    scanner = StaticSecurityScanner()
    code = 'def run(user_input): return eval(user_input)'
    findings = scanner.scan_file(code, "runner.py")
    assert any(f.rule_id == "SEC-R004" for f in findings)


def test_security_scanner_clean_code():
    scanner = StaticSecurityScanner()
    code = """
import os

PORT = int(os.getenv("PORT", 3000))
def get_user(db, user_id):
    return db.users.find_unique(where={"id": user_id})
"""
    findings = scanner.scan_file(code, "clean.py")
    assert len(findings) == 0
