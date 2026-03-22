# Install opencode-astral-skills

Canonical installation instructions for humans and LLM agents.

## Goal

Install this repository as an OpenCode config directory so OpenCode can discover:

- `skills/uv/SKILL.md`
- `skills/ruff/SKILL.md`
- `skills/ty/SKILL.md`

## Prerequisites

- `git` is installed.
- `opencode` is installed and available on PATH.

## For humans

Recommended (session-scoped, no persistent shell changes):

```bash
git clone https://github.com/IronCloud/opencode-astral-skills && OPENCODE_CONFIG_DIR="$PWD/opencode-astral-skills" opencode
```

Optional persistent setup:

```bash
export OPENCODE_CONFIG_DIR=/absolute/path/to/opencode-astral-skills
```

Then run:

```bash
opencode
```

## For LLM agents

Follow these steps exactly.

1) Clone repository

```bash
git clone https://github.com/IronCloud/opencode-astral-skills
```

2) Verify required skill files exist

```bash
test -f "$PWD/opencode-astral-skills/skills/uv/SKILL.md"
test -f "$PWD/opencode-astral-skills/skills/ruff/SKILL.md"
test -f "$PWD/opencode-astral-skills/skills/ty/SKILL.md"
```

3) Launch OpenCode with session-scoped config dir

```bash
OPENCODE_CONFIG_DIR="$PWD/opencode-astral-skills" opencode
```

4) Report completion

- Confirm which path was used for `OPENCODE_CONFIG_DIR`.
- Confirm all 3 skill file checks passed.

## Guardrails for agents

- Do not modify user global config files unless explicitly requested.
- Prefer session-scoped `OPENCODE_CONFIG_DIR=... opencode` over persistent exports.
- If any step fails, stop and report the exact failing command and error.

## Troubleshooting

- If OpenCode does not discover skills, confirm `OPENCODE_CONFIG_DIR` points to repo root (contains `skills/`).
- Ensure files are named exactly `SKILL.md` in uppercase.
- If using a persistent `export`, start a new shell session or source your shell profile.
