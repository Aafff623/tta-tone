# Reference distillation

This document records what was carried into `tta-tone` and what was deliberately left out. The following local clone revisions were inspected on 2026-10-01 (Asia/Shanghai). These are pinned comparison sources, not claims about the latest upstream versions.

| Source | Repository | Inspected revision |
| --- | --- | --- |
| lieflat-less-ai-tone | https://github.com/larashero3-dotcom/lieflat-less-ai-tone | 27d29232f10124db904ca9c0536d0b67cb3b2833 |
| humanizer-zh | https://github.com/ZeddYu/humanizer_zh | c743bc12f72fdf3a392035df139671bb539fc77a |
| oil-tone | https://github.com/oil-oil/oil-tone | 39cbf92f76c90b7bb27a5b5d4ed88a1fc5fa31f6 |
| i-have-adhd | https://github.com/ayghri/i-have-adhd | 839872f9d1cd634fed642b4589ce7226199cc15f |
| caveman | https://github.com/JuliusBrussee/caveman | f5d729488caa8f6a5b6c8086fe2cccd3e8a63f91 |
| chime | https://github.com/yuboxie/chime | 865ef186a0e797ec5ac242524a3c45b30a429542 |
| meme-archive | https://github.com/ThySummer14/meme-archive | e2ebc04a48e59155093828db1a3a788eb9cc7082 |
| dad-jokes | https://github.com/wesbos/dad-jokes | 892d244f6710f27e7a0168589c1abd03fcdeb5ea |
| readme-jokes | https://github.com/ABSphreak/readme-jokes | eb29fd08ae0cd4121c060c7dd8f1dc9aac133a30 |

Local clones under `temp/` are comparison material, not distribution source.

## `lieflat-less-ai-tone`

Carried in:

- whitelist-style editing: only change a confirmed pattern;
- preserve structure, quotations, lists, numbers, scope, modality, and author voice;
- explicit false positives for sentence length, passive voice, questions, metaphors, and technical formality;
- concrete evidence takes priority over abstract summary.

Not carried as a universal default: its finished-copy cleanup posture. `tta-tone` uses those rules in Preservation Edit and contextual anti-pattern review, while Agent Output and Free Draft have different formatting goals.

## `humanizer-zh`

Carried in:

- identify text type and reader before changing register;
- distinguish diagnosis, rewrite, and scoring requests;
- replace report, publicity, and hollow-verb language with supported actors and actions;
- allow a supplied style sample to override generic heuristics;
- keep reader-facing structure proportional to the requested output.

Constrained: broad humanizer advice cannot authorize invented examples, numbers, feelings, or a uniform conversational voice.

## `oil-tone`

Carried in:

- natural word order and grammatical function words;
- reader knowledge and first-use explanation of new objects;
- complete fact–reason–effect–limitation relationships;
- paragraph, list, and table choice based on retrieval needs;
- links and sources placed beside the supported claim.

Constrained: its drafting guidance is active in Free Draft, not automatically in Preservation Edit or Direct / Casual.

## `i-have-adhd`

Carried in:

- visible current state and one bounded next action for Agent Output;
- concrete progress numbering, error location, candidate causes, and tangent parking;
- no ceremonial opener or generic closer;
- short direct replies for trivial exchanges.

Constrained: the persistent reader profile and its universal action-oriented shape are not adopted. Agent Output rules activate only when the task is an agent report, plan, review, handoff, or debugging exchange.

## `caveman`

Carried in:

- separate **density** from task mode: normal, tight, and compressed are presentation choices applied after routing;
- remove filler and repeated framing only when the shorter wording is not less clear;
- preserve technical terms, code, commands, paths, exact errors, numbers, and ordering;
- auto-clarity gates for security warnings, irreversible actions, ambiguous multi-step procedures, and unsupported causes;
- distinguish measured values from estimates and require same-task A/B plus quality review before claiming savings or parity.

Deliberately left out:

- proxy, middleware, browser extension, hook, telemetry, and input/context compression; those are runtime or integration concerns, not a language-layer rule;
- `full` and `ultra` as persistent global modes; TTA routes per request so a compact status line does not leak into a preservation edit or safety warning;
- caveman grammar, invented abbreviations, dropped function words, and claims such as “65% fewer tokens”; the upstream repo's own `HONEST-NUMBERS.md` says style alone does not compress input and has no general reviewed reduction number.

The reference was inspected as a local clone under `temp/references/sources/caveman`. The clone is comparison material only; no installer, hook, proxy, telemetry, or `npx` command was run.

## Meme and expression sources

The expression and meme layer is documented in [expression-catalog.md](expression-catalog.md) and [meme-catalog.md](meme-catalog.md). We carried the source schemas, provenance fields, lifecycle gates, and safety labels. We did not copy bulk meme text, image assets, scraped archives, or joke feeds into the Skill. Meme origin is treated as a claim that needs a source; cultural familiarity alone is not evidence.

## Resulting design rule

The four source approaches contribute different layers. They must not be flattened into one blacklist or one response template:

```text
shared truth-preservation core
        + mode router
        + expression layer (emoji/kaomoji)
        + low-frequency meme layer
        + Direct / Casual adapter
        + Preservation Edit adapter
        + Agent Output adapter
        + Free Draft adapter
```

This separation is the main design change in the current `tta-tone` revision.
