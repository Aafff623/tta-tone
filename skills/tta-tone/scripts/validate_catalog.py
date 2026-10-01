"""Validate the machine-readable expression and meme allowlists."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    expression = json.loads((ROOT / "references" / "expression-catalog.json").read_text(encoding="utf-8"))
    meme = json.loads((ROOT / "references" / "meme-catalog.json").read_text(encoding="utf-8"))
    roles = expression.get("roles", {})
    if not roles or any(not role.get("emoji") and not role.get("kaomoji") for role in roles.values()):
        raise SystemExit("expression catalog has an empty role")
    if expression.get("default_limit_per_response") != 1 or meme.get("default_limit_per_response") != 1:
        raise SystemExit("catalog default limit must be 1")
    entries = meme.get("entries", [])
    ids = [entry.get("id") for entry in entries]
    if not entries or any(not item for item in ids) or len(ids) != len(set(ids)):
        raise SystemExit("meme catalog IDs must be non-empty and unique")
    for entry in entries:
        if not entry.get("meaning") or not entry.get("allowed") or not entry.get("blocked"):
            raise SystemExit(f"incomplete meme entry: {entry.get('id')}")
    print(f"catalogs valid: {len(roles)} expression roles, {len(entries)} meme entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
