# Upstream skill sources

This project uses the Astral skill guidance from
[`astral-sh/claude-code-plugins`](https://github.com/astral-sh/claude-code-plugins)
as source material for its native OpenCode skills.

Reviewed upstream commit:
`f3ce88a7ba830f53afd6d944c1d0278ed318e142`.

Only these upstream files are source inputs:

- `plugins/astral/skills/uv/SKILL.md`
- `plugins/astral/skills/ruff/SKILL.md`
- `plugins/astral/skills/ty/SKILL.md`

All other files and behavior in the upstream repository are outside this
project's scope. OpenCode-specific frontmatter, installation, validation, and
release documentation are maintained here.

Run `python3 scripts/check_upstream.py` to detect newer commits to the three
source paths. This is a drift sentinel, not proof that local adaptations match
upstream. Review source changes before updating `upstream.json` and the local
skills.
