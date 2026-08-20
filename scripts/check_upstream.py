from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / "upstream.json").read_text(encoding="utf-8"))
    repository = manifest["repository"]
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "opencode-astral-skills",
    }
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"

    changed: list[str] = []
    for name, source in sorted(manifest["skills"].items()):
        query = urllib.parse.urlencode({"path": source["path"], "per_page": 1})
        url = f"https://api.github.com/repos/{repository}/commits?{query}"
        try:
            with urllib.request.urlopen(
                urllib.request.Request(url, headers=headers), timeout=30
            ) as response:
                commits = json.load(response)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            print(f"error: could not check upstream {name}: {error}", file=sys.stderr)
            return 1

        latest = commits[0]["sha"] if commits else None
        if latest != source["commit"]:
            changed.append(f"{name}: pinned {source['commit']}, latest {latest}")

    if changed:
        print("upstream skill changes require review:", file=sys.stderr)
        for item in changed:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("no newer upstream commits detected for the tracked skill paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
