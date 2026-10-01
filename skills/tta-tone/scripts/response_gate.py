#!/usr/bin/env python3
"""Small protocol adapter core for per-turn tta-tone response gates.

The script is intentionally conservative: it checks only observable output
shape and expression policy. Semantic preservation remains a model/checker task.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any


EMOJI_RE = re.compile(
    r"[\U0001F300-\U0001FAFF\u2600-\u27BF]"
)
KAOMOJI_RE = re.compile(r"(?:[\(\（][^\n]{0,18}[\)\）]|[｡ﾟ﹏＿˘ωツง人])")
NATURAL_RE = re.compile(r"[A-Za-z\u3400-\u9FFF]")


def _text(payload: dict[str, Any]) -> str:
    for key in ("last_assistant_message", "lastAssistantMessage", "draft", "response", "message"):
        value = payload.get(key)
        if isinstance(value, str):
            return value
    return ""


def _has_expression(text: str) -> bool:
    return bool(EMOJI_RE.search(text) or KAOMOJI_RE.search(text))


def _feedback(reason: str) -> str:
    return f"TTA Tone response gate: {reason} 保留事实、范围、限定词、因果和技术字面量后重新生成。"


def _protocol(payload: dict[str, Any]) -> str:
    return str(payload.get("protocol") or "generic").lower()


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        assert _has_expression("完成了 ✅")
        assert _has_expression("完成了 (￣▽￣)")
        assert not _has_expression("plain technical result")
        print("response_gate self-test: PASS")
        return 0

    explicit_protocol = ""
    if "--protocol" in sys.argv:
        index = sys.argv.index("--protocol")
        if index + 1 < len(sys.argv):
            explicit_protocol = sys.argv[index + 1].lower()
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw or "{}")
    except json.JSONDecodeError:
        print("response_gate: invalid JSON input", file=sys.stderr)
        return 0  # never break the host on malformed hook input
    if not isinstance(payload, dict):
        return 0
    event = str(payload.get("hook_event_name") or payload.get("hookEventName") or "")
    protocol = explicit_protocol or _protocol(payload)
    if event in {"SessionStart", "PreInvocation"}:
        out = {"hookSpecificOutput": {"hookEventName": event, "additionalContext":
            "每次用户可见自然语言输出都要重新执行 tta-tone 场景路由和最终自检；保留事实、范围、限定词、因果与技术字面量。"}}
        print(json.dumps(out, ensure_ascii=False))
        return 0
    if event == "UserPromptSubmit":
        out = {"hookSpecificOutput": {"hookEventName": event, "additionalContext":
            "本轮输出发送前必须经过 tta-tone；自然语言回复使用合适的 emoji 或颜文字，代码、命令、日志和引用原文保持字面量。"}}
        if protocol in {"codex", "claude", "zcode", "kimi"}:
            print(json.dumps(out, ensure_ascii=False))
        return 0
    if event not in {"Stop", "PostInvocation"}:
        return 0
    if payload.get("stop_hook_active") is True:
        return 0  # bounded retry: never create a loop
    text = _text(payload)
    if not text or not NATURAL_RE.search(text) or _has_expression(text):
        return 0
    reason = _feedback("自然语言草稿缺少场景匹配的 emoji 或颜文字。")
    if protocol == "antigravity":
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    elif protocol in {"codex", "claude", "zcode", "kimi"}:
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
