# Project Agent Rules

## Project boundary

`D:\code\tta\tta-tone` is the source repository for the distributable `tta-tone` Skill. The authoritative Skill content lives in `skills/tta-tone/`; the root `README.md` documents installation and validation. `temp/` is local-only working material and is not a source of truth.

## TTA tone contract

- The runtime language layer is [`skills/tta-tone/SKILL.md`](./skills/tta-tone/SKILL.md). Do not copy its full rule catalog into this file; follow the source Skill and its references.
- Route user-facing output before writing: existing source plus an edit request uses `Preservation Edit`; repository state, progress, errors, reviews, plans, and handoffs use `Agent Output`; new prose uses `Free Draft`; short direct answers use `Direct / Casual`.
- Output contracts such as “只给结果” or “不要解释过程” control presentation but do not override preservation of source structure, facts, scope, uncertainty, causality, or technical literals.
- At conversation start, load the applicable rules and `tta-tone`. Before every user-facing natural-language response, including progress, errors, reviews, handoffs, and the final completion report, re-apply routing and the Skill's final pass. Loading once does not satisfy later responses. Keep commands, paths, configs, logs, code, and quoted source text literal unless the user explicitly asks to edit them.
- Keep output policy in one place: public rules define the concise presentation contract; this file defines repository boundaries; the Skill defines language behavior. Local rules may refine presentation but must not weaken truth, scope, uncertainty, causality, preservation, or verification evidence. Remove or rewrite conflicting duplicate output instructions instead of accumulating exceptions.
- For existing prose, use [`skills/tta-tone/scripts/preservation_check.py`](./skills/tta-tone/scripts/preservation_check.py) in addition to the wording checker when the edit is substantial. Report static checks, execution, and target-environment verification as separate states.
- If this file and the Skill appear to overlap, this file supplies repository boundaries and safety constraints; the Skill supplies language routing and output behavior.

## Working rules

- Inspect Git status and existing changes before editing. Preserve unrelated work.
- Keep the distribution path `skills/tta-tone/` stable unless the task explicitly changes the packaging contract.
- Treat `SKILL.md`, its references, scripts, and tests as tracked source. Evaluation outputs and machine-local runner settings stay under ignored paths.
- Do not place tokens, cookies, credentials, or private machine configuration in tracked files. If a credential is explicitly received for local work, persist it under the ignored `temp/secrets/` model and never echo it into reports.
- Mark claims as verified, inferred, or pending confirmation. Do not invent upstream provenance or validation results.

## Validation

Run the smallest relevant checks after changes. The documented checks are `python skills/tta-tone/scripts/tone_check.py --self-test`, `python skills/tta-tone/scripts/run_evals.py validate`, and `python -m unittest discover -s skills/tta-tone/tests`. Report which checks actually ran.

## Temporary workspace

Use `temp/` for cloned reference sources, reports, handoffs, logs, scripts, previews, and secrets. Keep only `temp/README.md` and `temp/AGENTS.md` tracked; all payloads remain ignored.
