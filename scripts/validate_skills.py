# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML==6.0.2"]
# ///

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml  # ty: ignore[unresolved-import]

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED_SKILLS = {"ruff", "ty", "uv"}
ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata"}
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    """Print one validation error to standard error.

    Args:
        message (str): Human-readable explanation of the validation failure.

    Returns:
        None: This function only prints the message; it does not return a value
        or stop validation.
    """
    print(f"error: {message}", file=sys.stderr)


def main() -> int:
    """Validate every native OpenCode skill definition in the repository.

    The validation covers the expected skill directories, YAML frontmatter,
    OpenCode naming constraints, metadata types, license declarations, and the
    presence of a non-empty instruction body.

    Args:
        None.

    Returns:
        int: Process exit code. Returns 0 when all skills are valid, or 1 when
        one or more validation errors were found.
    """
    errors = 0
    names: set[str] = set()
    files = sorted(SKILLS.glob("*/SKILL.md"))

    if {path.parent.name for path in files} != EXPECTED_SKILLS:
        fail(f"expected skill directories: {', '.join(sorted(EXPECTED_SKILLS))}")
        errors += 1

    for path in files:
        text = path.read_text(encoding="utf-8")

        # A SKILL.md starts and ends its YAML frontmatter with `---`. Limiting
        # the split to two separators leaves any later Markdown horizontal
        # rules untouched in the instruction body.
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            fail(f"{path.relative_to(ROOT)} must start with YAML frontmatter")
            errors += 1
            continue

        try:
            data = yaml.safe_load(parts[1])
        except yaml.YAMLError as error:
            fail(f"{path.relative_to(ROOT)} has invalid YAML: {error}")
            errors += 1
            continue

        if not isinstance(data, dict):
            fail(f"{path.relative_to(ROOT)} frontmatter must be a mapping")
            errors += 1
            continue

        unknown = set(data) - ALLOWED_FIELDS
        if unknown:
            fail(
                f"{path.relative_to(ROOT)} has unknown fields: {', '.join(sorted(unknown))}"
            )
            errors += 1

        name = data.get("name")
        description = data.get("description")
        metadata = data.get("metadata", {})

        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            fail(f"{path.relative_to(ROOT)} has an invalid skill name")
            errors += 1
        elif name != path.parent.name:
            fail(f"{path.relative_to(ROOT)} name must match its directory")
            errors += 1
        elif name in names:
            fail(f"duplicate skill name: {name}")
            errors += 1
        else:
            names.add(name)

        if not isinstance(description, str) or not 1 <= len(description) <= 1024:
            fail(f"{path.relative_to(ROOT)} description must contain 1-1024 characters")
            errors += 1

        if data.get("license") != "MIT":
            fail(f"{path.relative_to(ROOT)} must declare the repository's MIT license")
            errors += 1

        # OpenCode requires both metadata keys and values to be strings. Check
        # the container first so malformed scalar or list values fail cleanly.
        if not isinstance(metadata, dict) or any(
            not isinstance(key, str) or not isinstance(value, str)
            for key, value in metadata.items()
        ):
            fail(
                f"{path.relative_to(ROOT)} metadata must be a string-to-string mapping"
            )
            errors += 1

        if not parts[2].strip():
            fail(f"{path.relative_to(ROOT)} has no skill instructions")
            errors += 1

    if errors:
        return 1

    print(f"validated {len(files)} skills: {', '.join(sorted(names))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
