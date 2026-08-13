#!/usr/bin/env python3
"""Pick one ready-made kaomoji+emoji mix for tta-tone dialogue seasoning."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path


DATA = Path(__file__).resolve().parents[1] / "references" / "data"
MIX_PATH = DATA / "kaomojikan-emoji.json"
CATALOG_PATH = DATA / "season-catalog.json"

OVERUSED = (
    "(・ω・)",
    "(¬‿¬)",
    "(￣▽￣)",
    "(･ω･)",
    "(´･ω･`)",
)

# --mood stays as a synonym so old commands still run.
SCENES = (
    "done",
    "peek",
    "think",
    "surprise",
    "tea",
    "wait",
    "ack",
    "play",
)


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("expected object: " + str(path))
    return payload


def load_mix() -> dict[str, dict]:
    payload = load_json(MIX_PATH)
    items = payload.get("items")
    if not isinstance(items, list) or not items:
        raise SystemExit("seasoning data missing items: " + str(MIX_PATH))
    by_slug: dict[str, dict] = {}
    for item in items:
        slug = str(item.get("slug") or "").strip()
        text = str(item.get("text") or "").strip()
        if slug and text:
            by_slug[slug] = item
    return by_slug


def load_catalog() -> dict:
    payload = load_json(CATALOG_PATH)
    scenes = payload.get("scenes")
    if not isinstance(scenes, dict) or not scenes:
        raise SystemExit("season catalog missing scenes: " + str(CATALOG_PATH))
    return payload


def overused(text: str) -> bool:
    return any(face in text for face in OVERUSED)


def scene_entries(mix: dict[str, dict], catalog: dict, scene: str) -> list[tuple[str, str]]:
    spec = (catalog.get("scenes") or {}).get(scene) or {}
    slugs = spec.get("slugs") or []
    out: list[tuple[str, str]] = []
    seen: set[str] = set()
    for slug in slugs:
        item = mix.get(slug)
        if not item:
            continue
        text = str(item.get("text") or "").strip()
        if not text or text in seen or overused(text):
            continue
        out.append((slug, text))
        seen.add(text)
    return out


def resolve_exclude(mix: dict[str, dict], catalog: dict, raw: list[str]) -> set[str]:
    """Return excluded texts. Accepts exact mix text or a slug."""
    known_text: set[str] = set()
    slug_to_text: dict[str, str] = {}
    for scene in SCENES:
        for slug, text in scene_entries(mix, catalog, scene):
            known_text.add(text)
            slug_to_text[slug] = text
    banned: set[str] = set()
    for item in raw:
        token = item.strip()
        if not token:
            continue
        if token in slug_to_text:
            banned.add(slug_to_text[token])
            continue
        if token in known_text:
            banned.add(token)
            continue
        banned.add(token)
    return banned


def widen_order(catalog: dict, scene: str) -> list[str]:
    seen = {scene}
    order = [scene]
    for name in catalog.get("widen") or {}.get(scene) or []:
        if name in SCENES and name not in seen:
            order.append(name)
            seen.add(name)
    for name in SCENES:
        if name not in seen:
            order.append(name)
            seen.add(name)
    return order


def pool_for(
    mix: dict[str, dict],
    catalog: dict,
    scene: str,
    exclude: set[str],
    *,
    allow_widen: bool,
) -> list[tuple[str, str]]:
    if scene not in SCENES:
        raise SystemExit("unknown scene: " + scene)
    order = widen_order(catalog, scene) if allow_widen else [scene]
    for name in order:
        batch = [
            (slug, text)
            for slug, text in scene_entries(mix, catalog, name)
            if text not in exclude
        ]
        if batch:
            return batch
    return []


def pick(
    scene: str,
    exclude: list[str] | None = None,
    seed: int | None = None,
    *,
    allow_widen: bool = True,
) -> str:
    mix = load_mix()
    catalog = load_catalog()
    banned = resolve_exclude(mix, catalog, exclude or [])
    pool = pool_for(mix, catalog, scene, banned, allow_widen=allow_widen)
    if not pool:
        raise SystemExit(
            "empty seasoning pool for scene="
            + scene
            + " (all routed mixes already used this session)"
        )
    rng = random.Random(seed)
    return rng.choice(pool)[1]


def self_test() -> int:
    mix = load_mix()
    catalog = load_catalog()
    if len(mix) < 100:
        print("FAIL  expected 177-mix snapshot", file=sys.stderr)
        return 1
    routed: set[str] = set()
    for scene in SCENES:
        entries = scene_entries(mix, catalog, scene)
        if len(entries) < 3:
            print("FAIL  scene too small: " + scene, file=sys.stderr)
            return 1
        if any(overused(text) for _, text in entries):
            print("FAIL  overused face in " + scene, file=sys.stderr)
            return 1
        for slug, _text in entries:
            routed.add(slug)
        once = pick(scene, seed=0, allow_widen=False)
        again = pick(scene, seed=0, allow_widen=False)
        if once != again:
            print("FAIL  seed not stable for " + scene, file=sys.stderr)
            return 1
        other = pick(scene, exclude=[once], seed=0, allow_widen=False)
        if other == once:
            print("FAIL  exclude did not rotate " + scene, file=sys.stderr)
            return 1
    idle = catalog.get("idle") or {}
    for group, slugs in idle.items():
        clash = routed.intersection(slugs)
        if clash:
            print("FAIL  idle " + group + " overlaps routed", file=sys.stderr)
            return 1
    peek_texts = [text for _, text in scene_entries(mix, catalog, "peek")]
    widened = pick("peek", exclude=peek_texts, seed=0, allow_widen=True)
    if widened in peek_texts:
        print("FAIL  widen still returned peek", file=sys.stderr)
        return 1
    print("PASS  season picker self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scene",
        default=None,
        choices=SCENES,
        help="done/peek/think/surprise/tea/wait/ack/play；见 seasoning.md",
    )
    parser.add_argument(
        "--mood",
        default=None,
        choices=SCENES,
        help="--scene 的旧名字，效果相同",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="本会话已贴过的混排原文或 slug，可重复",
    )
    parser.add_argument("--list", action="store_true", help="print the pool, do not pick")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--no-widen",
        action="store_true",
        help="scene pool empty after exclude → error, do not borrow siblings",
    )
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    scene = args.scene or args.mood or "done"
    mix = load_mix()
    catalog = load_catalog()
    banned = resolve_exclude(mix, catalog, args.exclude)
    allow_widen = not args.no_widen
    if args.list:
        if args.scene is None and args.mood is None:
            for name in SCENES:
                for slug, text in scene_entries(mix, catalog, name):
                    print(name + "\t" + slug + "\t" + text)
            return 0
        for slug, text in pool_for(mix, catalog, scene, banned, allow_widen=allow_widen):
            print(slug + "\t" + text)
        return 0
    print(pick(scene, args.exclude, seed=args.seed, allow_widen=allow_widen))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
