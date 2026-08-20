# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and releases use [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Native OpenCode discovery, frontmatter, CLI compatibility, and upstream drift checks.
- Upstream skill provenance and reviewed revision tracking.
- Update, removal, collision, and agent installation guidance.

### Changed

- Replaced the custom config-directory installation with native `skills.paths`
  and standard OpenCode skill directories.
- Scoped Ruff mutation examples and added unsafe-fix previews.
- Updated GitHub workflow actions to their current major releases and use the
  official `astral-sh/setup-uv` action for pinned uv installation and caching.

### Fixed

- Removed the unsupported `uv sync --dev` option.
- Replaced ty's unsupported JSON output example.
- Corrected ty file-level suppression syntax.
- Restored the upstream MIT copyright notice.
