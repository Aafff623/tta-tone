#!/usr/bin/env python3
"""Run an isolated `claude` invocation while keeping provider routing.

`--setting-sources ""` (which the eval runners pass for isolation) also drops
the `env` block from ~/.claude/settings.json, where provider routing such as
ANTHROPIC_BASE_URL and ANTHROPIC_AUTH_TOKEN lives. Without it the runner falls
back to the operator's default login, which is exactly the contamination the
isolation is meant to prevent — and may bill the wrong account.

This wrapper forwards argv verbatim to the `claude` executable and injects only
the provider-routing environment read from settings at runtime. No credential
is written to any new file, printed, or logged.

Usage (from a runners config):

    ["python", "<abs-path>/claude_isolated.py", "--print", "--output-format",
     "json", "--no-session-persistence", "--setting-sources", "",
     "--model", "<model-id>", "--tools", ""]
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROUTING_PREFIXES = ("ANTHROPIC_", "API_TIMEOUT_MS")
SETTINGS = Path.home() / ".claude" / "settings.json"


def routing_env() -> dict[str, str]:
    if not SETTINGS.exists():
        return {}
    try:
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    env = settings.get("env") or {}
    if not isinstance(env, dict):
        return {}
    return {
        key: str(value)
        for key, value in env.items()
        if isinstance(key, str) and key.startswith(ROUTING_PREFIXES)
    }


def main(argv: list[str]) -> int:
    executable = shutil.which("claude")
    if executable is None:
        print("claude_isolated: `claude` executable not found on PATH", file=sys.stderr)
        return 127

    child_env = os.environ.copy()
    child_env.update(routing_env())

    completed = subprocess.run(
        [executable, *argv],
        env=child_env,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
