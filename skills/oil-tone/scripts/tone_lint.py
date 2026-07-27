#!/usr/bin/env python3
"""Reject confirmed oil-tone failures in reader-facing Chinese copy."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


Rule = tuple[re.Pattern[str], str]

RULES: tuple[Rule, ...] = (
    (re.compile(r"先保哪一个|保(?:重点|逻辑|意思|准确|清楚|自然|风格|质量|结构)"), "使用「遵循、保留、确保」等准确动词。"),
    (re.compile(r"(?:一个|这个)?(?:代码)?问题.{0,8}怎么走"), "改成「一个代码问题通常怎么处理」。"),
    (re.compile(r"(?:线索|结果|结论|内容).{0,8}(?:带回来|丢回来|交回来)"), "写清楚谁说明或提交了什么。"),
    (re.compile(r"(?:先)?把(?:事实|证据).{0,8}(?:找出来|建立(?:起来)?)"), "改成具体动作，例如查看调用、检查配置、确认当前实现。"),
    (re.compile(r"(?:逻辑|流程).{0,6}跑(?:到|下去)"), "使用「执行」或具体说明调用关系。"),
    (re.compile(r"(?:问题|流程|事情|能力|价值).{0,6}落(?:下去|到|地)"), "说明具体实现或处理动作。"),
    (re.compile(r"(?:吃下|吞下).{0,10}(?:对话|内容|信息|上下文)"), "使用「读取、接收、包含」等准确动词。"),
    (re.compile(r"(?:把)?(?:内容|信息|上下文).{0,8}(?:塞进|塞到|喂给)"), "使用「写入、添加、提供」等准确动词。"),
    (re.compile(r"跑测试"), "使用「运行测试」。"),
    (re.compile(r"(?:搞|弄)(?:顺|清楚|明白|好|完|懂|定|起来|下去)"), "说明具体动作和结果，不使用含义含糊的单字动作词。"),
    (re.compile(r"承接(?:需求|任务|工作|内容)"), "使用「处理、负责、实现」等准确动词。"),
    (re.compile(r"(?:赋能|撬动|抓手|闭环|沉淀价值|价值落地)"), "删除宣传黑话，直接说明具体作用。"),
    (re.compile(r"原因很简单[：:，,。]?"), "删除模板化领起语，直接说明具体原因。"),
    (re.compile(r"(?:真正重要的是|真正的关键是|这不仅仅?是|从更大的角度看)"), "删除没有增加信息的总结或升华表达。"),
    (re.compile(r"任务.{0,12}停在[“\"]?代码已经写出来"), "直接说明 Codex 写完代码后继续执行哪些检查。"),
)


def read_text(name: str) -> str:
    return sys.stdin.read() if name == "-" else Path(name).read_text(encoding="utf-8")


def visible_lines(text: str) -> list[tuple[int, str]]:
    lines: list[tuple[int, str]] = []
    in_fence = False
    in_script = False
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.search(r"<(script|style)\b", raw, flags=re.IGNORECASE):
            in_script = True
        if in_script:
            if re.search(r"</(script|style)>", raw, flags=re.IGNORECASE):
                in_script = False
            continue
        without_tags = re.sub(r"<[^>]+>", " ", raw)
        without_code = re.sub(r"`[^`]*`", " ", without_tags)
        visible = html.unescape(re.sub(r"\s+", " ", without_code)).strip()
        if visible:
            lines.append((number, visible))
    return lines


def find_failures(text: str) -> list[tuple[int, str, str]]:
    failures: list[tuple[int, str, str]] = []
    for line_number, line in visible_lines(text):
        for pattern, fix in RULES:
            if pattern.search(line):
                failures.append((line_number, line, fix))
                break
    return failures


def self_test() -> int:
    bad = "\n".join((
        "模型不知道先保哪一个。",
        "一个问题平时可以怎么走。",
        "Explorer 把线索带回来。",
        "先把事实找出来。",
        "这个流程怎么跑下去。",
        "让这个能力落下去。",
        "子 Agent 直接吃下整段对话。",
        "把内容塞进提示词。",
        "让模型跑测试。",
        "先把这段流程搞顺。",
        "这个功能负责承接需求。",
        "这套方案可以赋能开发团队。",
        "原因很简单：它读取了错误的文件。",
        "真正重要的是，我们理解了工具的边界。",
        "任务不必停在“代码已经写出来”。",
    ))
    good = "\n".join((
        "模型必须先遵循事实准确这项要求。",
        "一个代码问题通常怎么处理。",
        "Explorer 把查到的调用和配置说明清楚。",
        "查看调用和配置，确认当前实现。",
        "这个流程由主 Agent 继续执行。",
        "实现这项能力。",
        "子 Agent 读取与任务有关的对话。",
        "把内容写进提示词。",
        "让模型运行测试。",
        "这个功能负责处理需求。",
        "这套方法会根据情况变化，没有固定流程。",
        "这不是固定流程，而是一套会根据情况变化的方法。",
        "使用 Codex 时，先说明任务；完成后，再查看改动。",
    ))
    failures = find_failures(bad)
    if len(failures) != len(bad.splitlines()) or find_failures(good):
        print("FAIL  tone lint self-test")
        for failure in failures:
            print(f"      {failure}")
        return 1
    print("PASS  tone lint self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Reject known oil-tone failures.")
    parser.add_argument("files", nargs="*", help="UTF-8 files to scan, or - for stdin")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.files:
        parser.error("provide one or more files, or use --self-test")
    failed = False
    for name in args.files:
        for line_number, line, fix in find_failures(read_text(name)):
            print(f"FAIL  {name}:{line_number}: {line}\n      {fix}")
            failed = True
    if not failed:
        print("PASS  no known oil-tone failures")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
