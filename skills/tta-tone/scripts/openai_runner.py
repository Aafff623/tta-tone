#!/usr/bin/env python3
"""Call an OpenAI-compatible chat endpoint and print the reply text.

Eval-runner convenience for providers without an agent CLI, or whose CLI
isolation fights provider routing (for that case see claude_isolated.py).
Reads the prompt from stdin when invoked empty-handed (the judge path) or
from the first positional argument (the generation path), so a runner command
ending in an option that takes a value never swallows the prompt.

Configuration comes from the environment; the key is never written anywhere
or printed:

    OPENAI_BASE_URL   e.g. https://model.inferx.net/endpoints/v1
    OPENAI_MODEL      e.g. qwen38-flash-next
    OPENAI_API_KEY    bearer token

Optional: OPENAI_MAX_TOKENS (default 8192), OPENAI_TIMEOUT (seconds, default
180).
"""

import json
import os
import sys
import urllib.error
import urllib.request


def main(argv: list[str]) -> int:
    prompt = argv[1] if len(argv) > 1 else sys.stdin.read()
    base = os.environ.get("OPENAI_BASE_URL", "").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "")
    key = os.environ.get("OPENAI_API_KEY", "")
    if not (base and model and key and prompt.strip()):
        missing = [
            name
            for name, value in (
                ("OPENAI_BASE_URL", base),
                ("OPENAI_MODEL", model),
                ("OPENAI_API_KEY", key),
            )
            if not value
        ] or (["prompt"] if not prompt.strip() else [])
        print(f"openai_runner: missing {', '.join(missing)}", file=sys.stderr)
        return 2

    body: dict = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": int(os.environ.get("OPENAI_MAX_TOKENS", "8192")),
    }
    request = urllib.request.Request(
        base + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}",
        },
    )
    try:
        with urllib.request.urlopen(
            request, timeout=int(os.environ.get("OPENAI_TIMEOUT", "180"))
        ) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        print(f"openai_runner: HTTP {exc.code}: {detail}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"openai_runner: {exc}", file=sys.stderr)
        return 1

    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        print(f"openai_runner: unexpected payload shape: {exc}", file=sys.stderr)
        return 1
    if not str(content).strip():
        print(
            "openai_runner: empty content (reasoning may have consumed the token budget)",
            file=sys.stderr,
        )
        return 1
    print(str(content).strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
