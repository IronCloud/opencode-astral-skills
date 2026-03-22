---
name: ty
description: Use ty for Python type checking with practical, project-aligned rules.
license: MIT
compatibility: opencode
metadata:
  ecosystem: python
  tool: ty
  maintainer: opencode-astral-skills
---

# ty

ty is the default type-checking workflow in this skill pack.

## When to use this skill

Use this skill for Python type checking and for configuring type-checking rules.

Prefer ty when you see:

- `[tool.ty]` in `pyproject.toml`
- `ty.toml`

## How to invoke ty

- `uv run ty ...` when ty is a project dependency.
- `uvx ty ...` for one-off checks when ty is not pinned.

## Commands

### Type checking

```bash
ty check
ty check path/to/file.py
ty check src/
ty check --watch
ty check --output-format json
```

### Rule controls

```bash
ty check --error possibly-unresolved-reference
ty check --warn division-by-zero
ty check --ignore unresolved-import
```

### Python targeting

```bash
ty check --python-version 3.12
ty check --python-platform linux
ty check --python .venv/bin/python
```

### Other useful flags

```bash
ty check --respect-ignore-files
ty check --verbose
ty check --quiet
```

## Configuration

ty can be configured in `pyproject.toml` or `ty.toml`.

```toml
[tool.ty.environment]
python-version = "3.12"

[tool.ty.rules]
possibly-unresolved-reference = "warn"
division-by-zero = "error"

[tool.ty.src]
include = ["src/**/*.py"]
exclude = ["**/migrations/**"]
```

### Per-file overrides

```toml
[[tool.ty.overrides]]
include = ["tests/**", "**/test_*.py"]

[tool.ty.overrides.rules]
possibly-unresolved-reference = "warn"
```

## Migration mappings

### mypy to ty

```bash
mypy .               -> ty check
mypy --strict .      -> ty check --error-on-warning
mypy path/to/file.py -> ty check path/to/file.py
```

### Pyright to ty

```bash
pyright .               -> ty check
pyright path/to/file.py -> ty check path/to/file.py
```

## Ignore policy

- Prefer fixing type issues over suppressing them.
- Add ignore comments only when explicitly justified.
- Prefer rule-specific ignores.
- `ty` supports both `# ty: ignore[...]` and `# type: ignore`.
- Prefer `ty` comments for ty-specific suppressions.

```python
x = undefined_var  # ty: ignore[possibly-unresolved-reference]

# file-level suppression
# ty: ignore-file[unresolved-import]
```

## Language server

`ty` can run as a language server:

```bash
ty server
ty server --python-version 3.12
```

## References

- https://docs.astral.sh/ty/
