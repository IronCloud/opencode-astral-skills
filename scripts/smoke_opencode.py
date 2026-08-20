from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {"ruff", "ty", "uv"}


def snapshot(root: Path) -> dict[str, bytes]:
    """Capture every file below a directory for later mutation detection.

    Args:
        root (Path): Directory whose descendant files should be recorded.

    Returns:
        dict[str, bytes]: Mapping from each relative file path to its exact byte
        content. Comparing two snapshots detects added, removed, or modified
        files, including files ignored by Git.
    """
    return {
        str(path.relative_to(root)): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def main() -> int:
    """Verify that OpenCode discovers all skills without changing their source.

    A temporary copy of the skills is registered through inline OpenCode
    configuration. The command output is parsed as JSON and each discovered
    location is compared with the expected SKILL.md path. File snapshots ensure
    discovery does not write into the configured skill source.

    Args:
        None.

    Returns:
        int: Process exit code. Returns 0 when all expected skills are discovered
        at the correct paths without file mutations, otherwise returns a
        non-zero command exit code or 1 for validation failures.
    """
    # Use a disposable copy so this test can detect all filesystem mutations
    # without touching or relying on the state of the developer's checkout.
    with tempfile.TemporaryDirectory(prefix="opencode-astral-skills-") as directory:
        test_root = Path(directory)
        skill_root = test_root / "skills"
        shutil.copytree(ROOT / "skills", skill_root)
        before = snapshot(test_root)

        env = os.environ.copy()
        env.update(
            {
                # Inline configuration registers only this temporary skill path.
                "OPENCODE_CONFIG_CONTENT": json.dumps(
                    {"skills": {"paths": [str(skill_root)]}}
                ),
                # External skill sources are disabled so same-named user skills
                # cannot hide a failure in the repository copy being tested.
                "OPENCODE_DISABLE_EXTERNAL_SKILLS": "1",
                "OPENCODE_DISABLE_CLAUDE_CODE_SKILLS": "1",
            }
        )
        result = subprocess.run(
            ["opencode", "debug", "skill"],
            cwd=test_root,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            return result.returncode

        try:
            discovered = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            print(f"error: opencode returned invalid JSON: {error}", file=sys.stderr)
            return 1

        # Indexing by name makes the expected-skill checks direct and also
        # mirrors how OpenCode resolves one active definition for each name.
        by_name = {item["name"]: item for item in discovered}
        errors = 0
        for name in sorted(EXPECTED_SKILLS):
            item = by_name.get(name)
            expected = (skill_root / name / "SKILL.md").resolve()
            if item is None:
                print(f"error: OpenCode did not discover {name}", file=sys.stderr)
                errors += 1
                continue
            if Path(item["location"]).resolve() != expected:
                print(
                    f"error: {name} resolved to {item['location']}, expected {expected}",
                    file=sys.stderr,
                )
                errors += 1

        if snapshot(test_root) != before:
            print(
                "error: OpenCode discovery modified the configured skill source",
                file=sys.stderr,
            )
            errors += 1

    if errors:
        return 1

    print("OpenCode discovered uv, ruff, and ty from the configured skills path")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
