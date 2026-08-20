# opencode-astral-skills

Native OpenCode skills for Astral tooling: `uv`, `ruff`, and `ty`.

The skills provide on-demand guidance without setting models, permissions, or
other OpenCode defaults. OpenCode still merges skills from every configured
source, so check for existing skills with the same names before installation.

## Contents

- `skills/uv/SKILL.md`: Python project, script, environment, and tool workflows.
- `skills/ruff/SKILL.md`: focused Python linting and formatting workflows.
- `skills/ty/SKILL.md`: Python type-checking workflows.
- `docs/INSTALL.md`: canonical installation, update, and removal instructions.
- `UPSTREAM.md`: reviewed source files and synchronization policy.

## Installation

Clone the repository to a stable location:

```bash
git clone https://github.com/IronCloud/opencode-astral-skills \
  "$HOME/.local/share/opencode-astral-skills"
```

Add its `skills` directory to your global `~/.config/opencode/opencode.json` or
project `opencode.json`. Merge this with existing configuration rather than
replacing other fields:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["~/.local/share/opencode-astral-skills/skills"]
  }
}
```

Restart OpenCode after changing configuration, then verify discovery:

```bash
opencode debug skill
```

Confirm `uv`, `ruff`, and `ty` each resolve to the cloned repository. See
[`docs/INSTALL.md`](docs/INSTALL.md) for project-local copies, temporary use,
updates, removal, collision handling, and agent-safe installation.

Agent installers should follow the runbook in `docs/INSTALL.md`. After the user
approves a full commit SHA, the immutable raw URL has this form:

```text
https://raw.githubusercontent.com/IronCloud/opencode-astral-skills/<approved-full-commit>/docs/INSTALL.md
```

## Usage

OpenCode exposes each skill through its native `skill` tool and loads the full
guidance on demand. You can also request them explicitly:

```text
Use the uv, ruff, and ty skills to set up this Python project with Astral best practices.
```

Skill access can be controlled through OpenCode's `permission.skill` rules. A
denied skill is hidden from the agent even when its file is installed.

## Development

Run the local checks before submitting changes:

```bash
uv run scripts/validate_skills.py
python3 scripts/check_cli_compatibility.py
python3 scripts/smoke_opencode.py
python3 scripts/check_upstream.py
```

## Versioning

Behavioral changes use semantic version tags and are summarized in
[`CHANGELOG.md`](CHANGELOG.md). Upstream skill revisions are reviewed rather
than copied automatically; see [`UPSTREAM.md`](UPSTREAM.md).

## License

MIT. See [`LICENSE`](LICENSE).
