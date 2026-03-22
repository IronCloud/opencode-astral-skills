# opencode-astral-skills

Reusable OpenCode skills for Astral tooling: `uv`, `ruff`, and `ty`.

This repo is intentionally skills-only. It does not ship model, permission, or plugin defaults, so teams can adopt it without changing existing OpenCode behavior.

The intent is to provide an OpenCode-friendly, shareable port of the official Astral Claude plugin skills, with minimal ergonomic additions for installation and usage.

## Contents

- `skills/uv/SKILL.md`: guidance for using `uv` in Python projects and scripts.
- `skills/ruff/SKILL.md`: guidance for linting and formatting Python code with Ruff.
- `skills/ty/SKILL.md`: guidance for type checking Python code with ty.
- `docs/INSTALL.md`: canonical installation and verification instructions.

## Installation

### For humans

1) Clone the repository:

```bash
git clone https://github.com/IronCloud/opencode-astral-skills
```

2) Run OpenCode with this config directory (recommended):

```bash
OPENCODE_CONFIG_DIR="$PWD/opencode-astral-skills" opencode
```

This is session-scoped and does not change your shell profile.

Optional (persistent setup):

```bash
export OPENCODE_CONFIG_DIR=/absolute/path/to/opencode-astral-skills
```

Then run:

```bash
opencode
```

Verify skill files exist:

```bash
test -f "$PWD/opencode-astral-skills/skills/uv/SKILL.md"
test -f "$PWD/opencode-astral-skills/skills/ruff/SKILL.md"
test -f "$PWD/opencode-astral-skills/skills/ty/SKILL.md"
```

### For LLM agents

Use `docs/INSTALL.md` as the canonical install guide.

- `docs/INSTALL.md`

Raw URL:

```text
https://raw.githubusercontent.com/IronCloud/opencode-astral-skills/main/docs/INSTALL.md
```

## Alternative installation

If you do not want to use `OPENCODE_CONFIG_DIR`, copy one or more skill folders to an OpenCode skill discovery path:

- Project-local: `.opencode/skills/<name>/SKILL.md`
- User-global: `~/.config/opencode/skills/<name>/SKILL.md`

## Usage

The agent can load these skills on demand with the `skill` tool when tasks involve Python dependency management, linting/formatting, or type checking.

You can also prompt explicitly, for example:

```text
Use the uv, ruff, and ty skills and set up this Python project with Astral best practices.
```

## Versioning and updates

- Keep `SKILL.md` content aligned with upstream Astral guidance where possible.
- Keep changes focused and additive.
- Use semantic version tags when behavior changes in meaningful ways.
- Document notable guidance changes in release notes.

## License

MIT. See `LICENSE`.
