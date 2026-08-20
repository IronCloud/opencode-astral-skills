from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUFF_VERSION = os.environ.get("RUFF_VERSION", "0.16.3")
TY_VERSION = os.environ.get("TY_VERSION", "0.0.73")

CONTRACTS = {
    "uv sync": (["uv", "sync", "--help"], ["--locked", "--all-extras", "--all-groups"]),
    "uv pip install": (
        ["uv", "pip", "install", "--help"],
        ["--requirements", "--all-extras", "--group"],
    ),
    "Ruff check": (
        ["uvx", f"ruff@{RUFF_VERSION}", "check", "--help"],
        ["--fix", "--unsafe-fixes", "--diff", "--output-format"],
    ),
    "Ruff format": (
        ["uvx", f"ruff@{RUFF_VERSION}", "format", "--help"],
        ["--check", "--diff"],
    ),
    "ty check": (
        ["uvx", f"ty@{TY_VERSION}", "check", "--help"],
        [
            "--watch",
            "--output-format",
            "concise",
            "--python-version",
            "--python-platform",
        ],
    ),
}

FORBIDDEN_GUIDANCE = {
    "uv sync --locked --all-extras --dev": "uv has no sync --dev option",
    "ty check --output-format json": "ty has no generic JSON output format",
    "ty: ignore-file": "ty uses an own-line ty: ignore comment for file suppression",
    "ty server --python-version": "ty server does not accept Python targeting options",
}


def main() -> int:
    errors = 0

    for label, (command, expected) in CONTRACTS.items():
        result = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True, check=False
        )
        output = result.stdout + result.stderr
        if result.returncode:
            print(f"error: {label} help failed: {' '.join(command)}", file=sys.stderr)
            print(output, file=sys.stderr)
            errors += 1
            continue
        for option in expected:
            if option not in output:
                print(f"error: {label} no longer documents {option}", file=sys.stderr)
                errors += 1

    skill_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "skills").glob("*/SKILL.md"))
    )
    for snippet, reason in FORBIDDEN_GUIDANCE.items():
        if snippet in skill_text:
            print(f"error: unsupported guidance `{snippet}`: {reason}", file=sys.stderr)
            errors += 1

    if errors:
        return 1

    print(
        f"validated selected CLI guidance with Ruff {RUFF_VERSION} and ty {TY_VERSION}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
