# Claude Code Entry

Read and follow [`AGENTS.md`](./AGENTS.md). For user-facing language, use the scenario-aware Skill at [`skills/tta-tone/SKILL.md`](./skills/tta-tone/SKILL.md) through the routing contract defined there; do not duplicate its rules in this file. The Skill source is under [`skills/tta-tone/`](./skills/tta-tone/); local reference material and reports belong under ignored [`temp/`](./temp/).

Load this chain at conversation start and enforce the per-response contract in `AGENTS.md` throughout execution, including the final completion report. A startup load is not a substitute for the final language pass before each response.
