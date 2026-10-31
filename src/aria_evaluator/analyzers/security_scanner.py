import re
from typing import List
from aria_evaluator.models import SecurityVulnerability, SeverityEnum


class StaticSecurityScanner:
    """
    Scans code files for OWASP Top 10 anti-patterns, exposed credentials,
    unvalidated redirects, SSRF triggers, and injection vectors.
    """

    RULES = [
        {
            "id": "SEC-R001",
            "title": "Hardcoded Secret or API Key",
            "regex": r'(?i)(?:api_key|secret|password|bearer|auth_token)\s*=\s*[\'"][A-Za-z0-9_\-\.]{16,}[\'"]',
            "severity": SeverityEnum.CRITICAL,
            "cwe": "CWE-798",
            "description": "High-entropy credential literal detected in code. Secrets must be sourced from environment variables.",
            "remediation": "Move the sensitive secret to environment variables or a secrets manager."
        },
        {
            "id": "SEC-R002",
            "title": "Unrestricted SSRF Request Vector",
            "regex": r'(?:requests\.(?:get|post)|fetch|urllib\.request\.urlopen)\s*\(\s*(?![\'"]https://)[a-zA-Z0-9_\.\[\]]+',
            "severity": SeverityEnum.HIGH,
            "cwe": "CWE-918",
            "description": "HTTP request invoked on dynamic external URL without visible DNS-pinning or private CIDR validation.",
            "remediation": "Validate target URL scheme (HTTPS only), pin DNS resolution, and reject private/loopback/IMDS CIDR blocks."
        },
        {
            "id": "SEC-R003",
            "title": "Raw SQL String Formatting / Injection Risk",
            "regex": r'(?:execute|query|rawQuery)\s*\(\s*f[\'"]|\bSELECT\b.+WHERE.+\+|(?:execute|raw)\s*\(\s*`[^`]*\$\{[^}]+\}',
            "severity": SeverityEnum.HIGH,
            "cwe": "CWE-89",
            "description": "SQL statement constructed via string interpolation rather than parameterized queries.",
            "remediation": "Use parameterized queries or ORM query builders (e.g., Prisma, SQLAlchemy, or parameterized placeholders)."
        },
        {
            "id": "SEC-R004",
            "title": "Dangerous Dynamic Code Execution (eval / exec)",
            "regex": r'\b(?:eval|exec)\s*\(',
            "severity": SeverityEnum.CRITICAL,
            "cwe": "CWE-95",
            "description": "Dynamic code evaluation can lead to arbitrary remote code execution (RCE).",
            "remediation": "Eliminate eval/exec and replace with structured parsing (JSON or AST)."
        },
        {
            "id": "SEC-R005",
            "title": "Overly Permissive CORS Policy",
            "regex": r'(?:access-control-allow-origin|allow_origins)\s*[:=]\s*[\'"]\*[\'"]',
            "severity": SeverityEnum.MEDIUM,
            "cwe": "CWE-942",
            "description": "Wildcard CORS origin (*) allows any origin to read sensitive response data.",
            "remediation": "Explicitly restrict CORS to trusted client origins."
        },
        {
            "id": "SEC-R006",
            "title": "Weak Cryptographic Hashing for Passwords",
            "regex": r'(?:hashlib\.md5|hashlib\.sha1|crypto\.createHash\([\'"]md5[\'"]|crypto\.createHash\([\'"]sha1[\'"])',
            "severity": SeverityEnum.HIGH,
            "cwe": "CWE-328",
            "description": "MD5/SHA1 are cryptographically broken and vulnerable to collision attacks.",
            "remediation": "Use Argon2id, bcrypt, or SHA-256/HMAC for capability tokens and password hashing."
        },
        {
            "id": "SEC-R007",
            "title": "Production Debug Mode Enabled",
            "regex": r'\b(?:DEBUG|debug)\s*=\s*True\b',
            "severity": SeverityEnum.LOW,
            "cwe": "CWE-489",
            "description": "Debug mode exposes internal stack traces, interactive debuggers, and server internals.",
            "remediation": "Ensure debug mode is conditionally disabled in production environments."
        }
    ]

    def scan_file(self, content: str, file_path: str) -> List[SecurityVulnerability]:
        findings: List[SecurityVulnerability] = []
        lines = content.splitlines()

        for idx, line in enumerate(lines, 1):
            for rule in self.RULES:
                if re.search(rule["regex"], line):
                    findings.append(
                        SecurityVulnerability(
                            rule_id=rule["id"],
                            severity=rule["severity"],
                            title=rule["title"],
                            description=rule["description"],
                            file_path=file_path,
                            line_number=idx,
                            cwe_id=rule["cwe"],
                            remediation=rule["remediation"],
                        )
                    )

        return findings
