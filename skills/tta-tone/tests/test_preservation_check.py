import unittest

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import preservation_check  # noqa: E402


class PreservationCheckTest(unittest.TestCase):
    SOURCE = """## 结果
这个方案可能在很大程度上减少冷启动。

命令是 `claude --version`，当前版本为 2.1.263。

```powershell
Get-Content settings.json
```
"""

    def test_accepts_local_wording_edit(self):
        edited = self.SOURCE.replace("这个方案可能在很大程度上减少冷启动。", "这个方案在很大程度上可能减少冷启动。")
        self.assertEqual([], preservation_check.check(self.SOURCE, edited))

    def test_rejects_literal_and_structure_loss(self):
        edited = "## 结果\n这个方案减少冷启动。\n"
        failures = preservation_check.check(self.SOURCE, edited)
        self.assertIn("protected inline code missing: {'claude --version': 1}", failures)
        self.assertIn("protected numeric token missing: {'2.1.263': 1}", failures)
        self.assertIn("fenced code blocks changed", failures)
        self.assertIn("paragraph count changed: 3 -> 1", failures)

    def test_rejects_added_evidence_and_heading_level(self):
        failures = preservation_check.check("## 结果\n只测了 4 次。", "# 结果\n只测了 4 次，提升 50%。")
        self.assertIn("heading sequence changed", failures)
        self.assertTrue(any("numeric token added" in failure for failure in failures))

    def test_tilde_and_long_fences_are_protected(self):
        for fence in ("~~~", "````"):
            source = f"{fence}text\n90 秒\n{fence}\n"
            self.assertEqual([], preservation_check.check(source, source))
            self.assertIn("fenced code blocks changed", preservation_check.check(source, source.replace("90", "40")))

    def test_list_and_quote_structure_is_preserved(self):
        self.assertIn("list markers changed", preservation_check.check("- 甲\n- 乙", "甲和乙"))
        self.assertIn("quotation markers changed", preservation_check.check("> 引语", "引语"))


if __name__ == "__main__":
    unittest.main()
