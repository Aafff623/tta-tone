import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import tone_check


class ModeCheckTest(unittest.TestCase):
    def scan(self, mode, source):
        output = io.StringIO()
        with patch.object(sys, "argv", ["tone_check", "--mode", mode, "-"]), patch.object(sys, "stdin", io.StringIO(source)), contextlib.redirect_stdout(output):
            result = tone_check.main()
        return result, output.getvalue()

    def test_real_technical_term_is_not_a_hard_failure(self):
        result, output = self.scan("agent", "值得注意的是，控制系统已发布。")
        self.assertEqual(0, result)
        self.assertIn("WARN", output)
        self.assertNotIn("FAIL", output)

    def test_short_conversation_does_not_trigger_draft_structure(self):
        source = "收到。\n解决了。\n谢谢。"
        self.assertNotIn("STRUCT", self.scan("direct", source)[1])
        self.assertIn("STRUCT", self.scan("draft", source)[1])
