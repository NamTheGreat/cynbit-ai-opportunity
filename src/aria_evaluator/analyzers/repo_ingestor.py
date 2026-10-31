import os
from pathlib import Path
from typing import Dict, List, Tuple
from aria_evaluator.config import settings


class RepositoryIngestor:
    """
    Ingests local codebases or extracted repositories, filtering out
    vendored assets and heavy binaries, creating clean file representations for analysis.
    """

    IGNORE_DIRS = {
        "node_modules", ".git", ".venv", "venv", "__pycache__", ".next",
        "dist", "build", "coverage", ".idea", ".vscode", ".tox"
    }

    def ingest_directory(self, root_dir: str) -> Dict[str, str]:
        path = Path(root_dir).resolve()
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Directory does not exist or is not a folder: {root_dir}")

        collected_files: Dict[str, str] = {}

        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in self.IGNORE_DIRS]

            for file in files:
                ext = Path(file).suffix.lower()
                if ext in settings.supported_extensions:
                    full_path = Path(root) / file
                    try:
                        # Skip files over 500 KB to avoid token blowup
                        if full_path.stat().st_size > 500 * 1024:
                            continue
                        rel_path = str(full_path.relative_to(path))
                        collected_files[rel_path] = full_path.read_text(encoding="utf-8", errors="ignore")
                    except Exception:
                        continue

        return collected_files

    def extract_manifest_summary(self, files: Dict[str, str]) -> Dict[str, Any]:
        has_package_json = "package.json" in files
        has_requirements = "requirements.txt" in files or "pyproject.toml" in files
        has_prisma = any(f.endswith(".prisma") for f in files)
        has_tests = any("test" in f.lower() for f in files)
        has_docker = "Dockerfile" in files or "docker-compose.yml" in files

        return {
            "has_package_json": has_package_json,
            "has_python_manifest": has_requirements,
            "has_prisma_orm": has_prisma,
            "has_test_suite": has_tests,
            "has_dockerfile": has_docker,
        }
