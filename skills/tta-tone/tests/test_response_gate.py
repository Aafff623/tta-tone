import json
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "response_gate.py"


def run(payload, protocol):
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--protocol", protocol],
        input=json.dumps(payload, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout) if proc.stdout.strip() else {}


class ResponseGateTests(unittest.TestCase):
    def test_session_start_injects_context(self):
        result = run({"hook_event_name": "SessionStart"}, "codex")
        self.assertIn("tta-tone", result["hookSpecificOutput"]["additionalContext"])

    def test_user_prompt_injects_per_turn_reminder(self):
        result = run({"hook_event_name": "UserPromptSubmit"}, "claude")
        self.assertIn("本轮输出", result["hookSpecificOutput"]["additionalContext"])

    def test_stop_blocks_plain_natural_language(self):
        result = run(
            {"hook_event_name": "Stop", "last_assistant_message": "完成了本次修改"},
            "zcode",
        )
        self.assertEqual(result["decision"], "block")

    def test_stop_allows_expression_and_ignores_retry(self):
        allowed = run(
            {"hook_event_name": "Stop", "last_assistant_message": "完成了 ✅"},
            "codex",
        )
        self.assertEqual(allowed, {})
        retry = run(
            {
                "hook_event_name": "Stop",
                "last_assistant_message": "完成了本次修改",
                "stop_hook_active": True,
            },
            "claude",
        )
        self.assertEqual(retry, {})


if __name__ == "__main__":
    unittest.main()
