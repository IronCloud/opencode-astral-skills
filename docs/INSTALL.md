# Install opencode-astral-skills

These instructions install the `uv`, `ruff`, and `ty` skills through native
OpenCode skill discovery.

## Prerequisites

- `git` is installed.
- OpenCode supports the native `skill` tool and `opencode debug skill`.

## Updateable installation

Clone the repository to a stable location:

```bash
git clone https://github.com/IronCloud/opencode-astral-skills \
  "$HOME/.local/share/opencode-astral-skills"
```

Add the clone's `skills` directory to either the global
`~/.config/opencode/opencode.json` or a project's `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["~/.local/share/opencode-astral-skills/skills"]
  }
}
```

Preserve existing configuration and append this path to an existing
`skills.paths` array. Quit and restart OpenCode after changing configuration.

## Project-local copy

Copy the skills into a project's official discovery directory when the project
should carry its own snapshot:

```bash
test ! -e ".opencode/skills/uv" &&
test ! -e ".opencode/skills/ruff" &&
test ! -e ".opencode/skills/ty" &&
mkdir -p ".opencode/skills" &&
cp -R "/path/to/opencode-astral-skills/skills/uv" ".opencode/skills/" &&
cp -R "/path/to/opencode-astral-skills/skills/ruff" ".opencode/skills/" &&
cp -R "/path/to/opencode-astral-skills/skills/ty" ".opencode/skills/"
```

Do not overwrite an existing `.opencode/skills/uv`, `ruff`, or `ty` directory
without reviewing it first.

For a user-global copy, use `~/.config/opencode/skills/` instead. Copied skills
must be recopied manually to receive updates.

## Temporary verification

Test a clone without modifying OpenCode configuration:

```bash
OPENCODE_CONFIG_CONTENT='{"skills":{"paths":["/absolute/path/to/opencode-astral-skills/skills"]}}' \
  opencode debug skill
```

Use an absolute path in inline configuration. This command should list `uv`,
`ruff`, and `ty` with locations under that path.

## Verify installation

Run:

```bash
opencode debug skill
```

Confirm all three names are present and each `location` is the intended source.
If a name resolves elsewhere, remove or rename the duplicate before relying on
the skill. If a skill is absent, check its frontmatter and any
`permission.skill` rules that deny access.

## Update

For an updateable clone:

```bash
git -C "$HOME/.local/share/opencode-astral-skills" pull --ff-only
```

Restart OpenCode and rerun `opencode debug skill` after an update.

For copied installations, update the source clone, review the changes, and
recopy the three skill directories.

## Remove

For a `skills.paths` installation, remove the repository path from the relevant
`opencode.json`, then delete the clone if it is no longer needed.

For a copied installation, remove only the directories installed from this
repository:

```bash
rm -rf ".opencode/skills/uv" ".opencode/skills/ruff" ".opencode/skills/ty"
```

Review each path before removal. Restart OpenCode and verify the resulting skill
registry afterward.

## Agent installation runbook

Agents must treat installation as a configuration change with explicit scope,
preflight checks, verification, and rollback.

### Success criteria

- The user approved project-local or user-global scope.
- Existing OpenCode configuration and same-named skills were preserved.
- `opencode debug skill` resolves `uv`, `ruff`, and `ty` to the intended source.
- The final report includes the source commit, destination, config changed, and
  restart requirement.

### 1. Establish scope

Ask one short question if the user did not specify project-local or user-global
installation. Do not infer permission to modify `~/.config/opencode/` from a
request made inside a project.

Prefer an updateable `skills.paths` installation when the user wants the skills
across projects. Prefer `.opencode/skills/` when the project should own and
review a fixed copy.

### 2. Preflight

Before writing:

```bash
git --version
opencode --version
opencode debug skill
```

Read the target `opencode.json` or `opencode.jsonc`, if present. Check the
destination directories and existing discovery output for `uv`, `ruff`, and
`ty`. Stop and ask before replacing any same-named skill.

### 3. Install without replacing configuration

Require a user-approved full commit SHA before cloning. Do not silently install
the repository's mutable default branch or assume a tag cannot move. Clone
without checkout, select the approved commit, and record it:

```bash
mkdir -p "/approved/path"
git clone --no-checkout https://github.com/IronCloud/opencode-astral-skills \
  "/approved/path/opencode-astral-skills"
git -C "/approved/path/opencode-astral-skills" checkout --detach \
  "<approved-full-commit>"
git -C "/approved/path/opencode-astral-skills" rev-parse --verify HEAD
```

Review the selected commit and the three `SKILL.md` files before adding them to
OpenCode discovery. Do not execute scripts from a newly cloned repository as an
installation step.

For an updateable installation, edit the selected OpenCode config with a
structure-aware editing tool. Preserve `$schema`, comments in JSONC, existing
fields, and existing `skills.paths` values; append only the new absolute path.
Do not rewrite the config with shell redirection or a formatter.

For a project-local copy, create `.opencode/skills/` and copy only after proving
the three destination directories do not exist. Leave the copied files visible
in the project diff for review.

For a later agent-managed update, do not use `git pull` on the detached checkout.
Fetch the remote, inspect the changes from the installed commit to a candidate
full commit SHA, obtain user approval for that SHA, and then check it out with
`git checkout --detach`. Reverify discovery after every update.

### 4. Validate and verify

Verify discovery before declaring success:

```bash
opencode debug skill
```

Inspect the JSON output, not only the exit code. Each expected name must resolve
to the intended `SKILL.md`. Check the target project's `git status` and disclose
all files created or changed.

Do not launch an interactive OpenCode session as an installation or verification
step. OpenCode configuration is loaded at startup, so tell the user to quit and
restart existing sessions.

### 5. Report and rollback

Report:

- installation scope and destination;
- source commit;
- configuration or project files changed;
- resolved locations for `uv`, `ruff`, and `ty`;
- verification commands and results;
- restart requirement.

Provide the matching rollback without executing it unless requested: remove the
added `skills.paths` entry, or remove only the three copied directories after
reconfirming their paths. Rerun `opencode debug skill` after rollback.
