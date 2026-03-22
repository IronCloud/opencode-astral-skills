---
name: ruff
description: Use ruff for fast Python linting and formatting with safe, focused fixes.
license: MIT
compatibility: opencode
metadata:
  ecosystem: python
  tool: ruff
  maintainer: opencode-astral-skills
---

# ruff

Ruff is the default linter and formatter for Python code in this skill pack.

## When to use this skill

Use this skill for Python linting, code quality fixes, and formatting.

Prefer Ruff when you see:

- `[tool.ruff]` in `pyproject.toml`
- `ruff.toml` or `.ruff.toml`

## Core rules

- Scope fixes to files you are actively changing unless asked otherwise.
- Run lint fixes before formatting.
- Avoid broad formatting churn in repositories that are not consistently Ruff-formatted.
- Review unsafe fixes before applying them.

## How to invoke Ruff

- `uv run ruff ...` when Ruff is in project dependencies.
- `uvx ruff ...` for one-off use when Ruff is not pinned in the project.
- `ruff ...` only when globally installed and project conventions allow it.

## Commands

### Linting

```bash
ruff check .
ruff check path/to/file.py
ruff check --fix .
ruff check --fix --unsafe-fixes .
ruff check --watch
ruff check --select E,F .
ruff check --ignore E501 .
ruff check --extend-select B .
ruff check --output-format=github
ruff check --statistics
ruff check --show-settings
ruff rule E501
```

### Formatting

```bash
ruff format .
ruff format path/to/file.py
ruff format --check .
ruff format --diff .
```

### Common workflow

```bash
ruff check --select I --fix .
ruff format .
```

## Configuration

Ruff is typically configured in `pyproject.toml`.

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["myproject"]
```

## Migration mappings

### Black to Ruff

```bash
black .          -> ruff format .
black --check .  -> ruff format --check .
black --diff .   -> ruff format --diff .
```

### Flake8 to Ruff

```bash
flake8 .                   -> ruff check .
flake8 --select E,F .      -> ruff check --select E,F .
flake8 --ignore E501 .     -> ruff check --ignore E501 .
```

### isort to Ruff

```bash
isort .          -> ruff check --select I --fix .
isort --check .  -> ruff check --select I .
isort --diff .   -> ruff check --select I --diff .
```

## Recommended sequence

```bash
ruff check --fix .
ruff format .
```

## Safety notes

- `--unsafe-fixes` can change behavior; inspect diffs first.
- Keep changes minimal and aligned with repository conventions.

## References

- https://docs.astral.sh/ruff/
