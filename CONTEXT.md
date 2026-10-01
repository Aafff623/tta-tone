# Project Context

## Purpose

This repository packages `tta-tone`, a language-quality Skill for AI coding agents and general assistants. It combines response-output rules, conservative preservation editing, drafting guidance, a pattern catalog, a deterministic checker, and paired evaluations.

## Runtime inheritance

The control-plane files have different jobs and are not interchangeable:

| File | Role | TTA relationship |
| --- | --- | --- |
| `AGENTS.md` | Repository boundaries, safety, validation, and temporary-workspace rules | Selects `skills/tta-tone/SKILL.md` as the language authority and records the routing contract |
| `CLAUDE.md` | Claude Code entrypoint | Points to `AGENTS.md` and tells Claude to use the same `tta-tone` source; it contains no duplicate rule catalog |
| `CONTEXT.md` | Project map and provenance boundary | Documents the relationship for maintainers; it is not itself the runtime Skill |
| `skills/tta-tone/SKILL.md` | Distributable runtime language layer | Authoritative source for Direct / Casual, Preservation Edit, Agent Output, and Free Draft |

`AGENTS.md`, `CLAUDE.md`, and `CONTEXT.md` participate in the TTA system by pointing to and constraining the Skill; they are not three separate copies of the Skill. A file named `cloud.md` is not present in this workspace; if a separate Harness uses that filename, it needs its own adapter that points to the same Skill source.

The runtime contract loads the instruction chain at conversation start and re-applies TTA routing and the final language pass before every user-facing response, including the completion report. This is an instruction requirement, not proof of automatic hook enforcement or model compliance. Public presentation rules, project boundaries, and Skill behavior must stay consistent without duplicating the full catalog.

## Authoritative paths

- `skills/tta-tone/SKILL.md`: runtime instructions.
- `skills/tta-tone/references/routing.md`: mode selection and conflict rules.
- `skills/tta-tone/references/distillation.md`: pinned reference-repository decisions.
- `skills/tta-tone/references/caveman-comparison.md`: five default-versus-TTA behavior examples; illustrative, not provider A/B evidence.
- `skills/tta-tone/references/expression-catalog.md`: reviewed emoji/kaomoji roles and limits.
- `skills/tta-tone/references/meme-catalog.md`: meme-source provenance, priority tiers, and routing gates.
- `skills/tta-tone/references/expression-catalog.json` and `meme-catalog.json`: machine-readable allowlists checked by `scripts/validate_catalog.py`.
- `skills/tta-tone/references/`: detailed rules and examples.
- `skills/tta-tone/scripts/`: checker and evaluation runners.
- `skills/tta-tone/tests/`: test coverage for the evaluation harness.
- `README.md`: repository installation and validation contract.
- `temp/`: ignored local research and working material.

## Provenance boundary

The pattern catalog records borrowed approaches from `lieflat-less-ai-tone`, `humanizer-zh`, `oil-tone`, and earlier `tta-tone` material. Evaluation infrastructure records adaptation from `ayghri/i-have-adhd`. Exact source revisions must be recorded in the local reference inventory before being treated as verified.

## Constraints

- Preserve the `skills/tta-tone/` distribution path.
- Do not turn pattern detections into unconditional word bans; inspect context.
- Preserve facts, scope, uncertainty, causality, source-stated values, and technical literals.
- Keep local clones and evaluation outputs out of Git.
