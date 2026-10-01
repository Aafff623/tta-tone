# TTA Tone routing and conflict rules

The router prevents one response shape from being applied to every task. It selects a mode; it does not change the shared truth-preservation core.

## Decision order

Use this order. “只给结果” and similar phrases are output contracts, not a reason to downgrade an existing-source edit to Direct / Casual.

1. Existing source text plus an edit request → Preservation Edit.
2. Agent state, progress, error, review, plan, handoff, or tool result → Agent Output.
3. New prose or an explicitly free rewrite → Free Draft.
4. Otherwise → Direct / Casual.

For mixed responses, route source-derived spans and new framing independently.

## Decision table

| Evidence in the request | Mode | Main risk | Default shape |
| --- | --- | --- | --- |
| “只给版本号”, direct fact, thanks, short acknowledgement | Direct / Casual | over-answering | one sentence or literal |
| existing text plus “改自然/去 AI 味/保持结构/保留原意” | Preservation Edit | semantic or structural drift | source structure preserved |
| repository status, progress, error, review, handoff, next step | Agent Output | vague state or false certainty | result/state first |
| new article, explanation, documentation, public copy, free rewrite | Free Draft | generic prose or invented detail | reader-oriented prose |

If the request contains existing source text and asks for a new explanation around it, use Preservation Edit for the source and the other matching mode for the explanation.

## Tie-breaking

1. An explicit output contract controls length and presentation (`只给结果`, `不要解释过程`, `保持两段`); it does not override Preservation Edit’s source-protection rules.
2. Source-derived spans use the least-permissive mode. New framing may use a freer mode.
3. Safety, truth, scope, and uncertainty beat actionability and concision.
4. A style sample beats generic anti-AI heuristics.
5. If the mode is genuinely ambiguous, preserve the source and ask one short diagnostic question instead of guessing.

## What changes by mode

- Direct / Casual turns off scaffolding.
- Preservation Edit turns off free restructuring and personality injection.
- Agent Output enables state, verification, candidate-cause, tangent-parking, and next-action rules.
- Free Draft enables useful reordering, reader context, and format selection, but never invented specificity.

## Short examples

### Same fact, different mode

Input: `CLAUDE.md` now only references `@~/.agents/AGENTS.md`; a new session passed.

- Direct / Casual: `已验证通过。`
- Agent Output: `已完成：CLAUDE.md 现在只引用 @~/.agents/AGENTS.md，新 session 验证通过。`
- Free Draft: `这次调整把公共规则收口到 @~/.agents/AGENTS.md，新的 session 已验证能够正常加载。`

The last version is suitable only when the user asks for an explanatory paragraph; it is too expansive for a status report.

### Existing text always stays stricter

Input: “去 AI 味，但保持结构和‘在很大程度上’。”

The router must preserve headings, paragraph order, the qualifier, and the stated limitation. Removing an empty opener is allowed; adding evidence, examples, or a stronger conclusion is not.

### Unknown error cause

Agent Output may say: `auth.spec.ts:42 失败：expected 200, got 401。缺少 Authorization header 是一个候选原因，先确认请求是否带了该 header。`

It must not state the candidate as confirmed when the input contains no such evidence.
