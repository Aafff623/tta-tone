#!/usr/bin/env python3
"""Check machine-observable preservation invariants for an edited document.

This is a narrow structural gate, not a semantic judge. It compares headings,
fenced code blocks, inline code, URLs, numeric tokens, and paragraph count.
Run it after a Preservation Edit alongside human/model review.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


NUMBER = re.compile(r"(?<![\w])\d+(?:[.,]\d+)*(?:\s*%|％)?")
URL = re.compile(r"https?://[^\s)\]>]+")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _fenced_blocks(text: str) -> list[str]:
    blocks: list[str] = []
    current: list[str] | None = None
    fence = ""
    for line in text.splitlines(keepends=True):
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if current is None and opening:
            current = [line]
            fence = opening.group(1)
        elif current is not None:
            current.append(line)
            if re.match(r"^ {0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                blocks.append("".join(current))
                current = None
    if current is not None:
        blocks.append("".join(current))
    return blocks


def _paragraph_count(text: str) -> int:
    return sum(bool(block.strip()) for block in re.split(r"\n\s*\n", text.strip()))


def _heading_sequence(text: str) -> list[tuple[str, str]]:
    return [match.groups() for line in text.splitlines() if (match := HEADING.match(line))]


def _tokens(text: str, pattern: re.Pattern[str]) -> Counter[str]:
    return Counter(pattern.findall(text))


def check(source: str, edited: str) -> list[str]:
    failures: list[str] = []
    source_headings = _heading_sequence(source)
    edited_headings = _heading_sequence(edited)
    if source_headings != edited_headings:
        failures.append("heading sequence changed")

    source_fences = _fenced_blocks(source)
    edited_fences = _fenced_blocks(edited)
    if source_fences != edited_fences:
        failures.append("fenced code blocks changed")

    for label, pattern in (("inline code", INLINE_CODE), ("URL", URL), ("numeric token", NUMBER)):
        missing = _tokens(source, pattern) - _tokens(edited, pattern)
        added = _tokens(edited, pattern) - _tokens(source, pattern)
        if missing:
            failures.append(f"protected {label} missing: {dict(missing)}")
        if added:
            failures.append(f"protected {label} added: {dict(added)}")

    for label, pattern in (
        ("list markers", re.compile(r"(?m)^\s*([-*+] |\d+[.)] )")),
        ("table rows", re.compile(r"(?m)^\s*(\|).*\|\s*$")),
        ("quotation markers", re.compile(r"(?m)^\s*(>+)")),
    ):
        if _tokens(source, pattern) != _tokens(edited, pattern):
            failures.append(f"{label} changed")

    source_paragraphs = _paragraph_count(source)
    edited_paragraphs = _paragraph_count(edited)
    if source_paragraphs != edited_paragraphs:
        failures.append(
            f"paragraph count changed: {source_paragraphs} -> {edited_paragraphs}"
        )
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("edited", type=Path)
    args = parser.parse_args(argv)
    failures = check(_read(args.source), _read(args.edited))
    if failures:
        for failure in failures:
            print(f"FAIL  {failure}")
        return 1
    print("PASS  preservation invariants")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
