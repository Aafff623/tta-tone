# Preservation Edit Mode

Use this reference when editing existing user-supplied prose. The purpose is to remove clearly identifiable AI-writing artifacts without silently changing the author's substance.

## Preserve information

Do not add, remove, or strengthen factual content. Preserve:

- people, organizations, roles, places, product names;
- numbers, percentages, money, counts, durations;
- dates, times, chronology, sequencing;
- quotations, reported speech, citations, URLs;
- causal claims, motives, mental states;
- scope and modality: `可能`, `通常`, `大多`, `在一定程度上`, `某些情况下`, `据说`, `看起来` when they carry real uncertainty.

A single meaningful qualifier is not filler. Remove only redundant stacks such as `可能潜在地在一定程度上或许` while preserving the intended degree of uncertainty.

Do not invent concrete details to replace abstract writing. If the source says only `速度明显变快`, do not fabricate timings. If the source lacks a source, example, date, or number, keep that absence or flag it when the task calls for review.

## Preserve structure

Unless the user explicitly asks for restructuring, keep:

- title hierarchy;
- section order;
- paragraph order and count when practical;
- lists and tables;
- quotation placement;
- code-block placement;
- argument and narrative sequence.

Do not turn prose into a list, merge sections, or reorder claims merely because another structure feels cleaner.

## Protect exact spans

Do not modify code, shell commands, paths, filenames, identifiers, API/library/model names, environment variables, config keys, logs, stack traces, error messages, quotations, URLs, JSON/YAML/XML/CSV, or source excerpts unless the user explicitly asks to edit those exact spans.

## Editing workflow

1. Identify the requested target style and any supplied author/style reference.
2. Lock protected information and structure.
3. Identify only passages that clearly match a rule in `patterns.md` or a direct user instruction.
4. Make the smallest local edit that resolves the problem.
5. Re-read each changed passage for information conservation and modality.
6. Re-check every untouched passage remains untouched unless another rule clearly applies.
7. Return the edited text. Explain changes only when asked.

## Default decision rule

When uncertain whether a phrase is an AI tell, preserve it.

When a real author/style reference conflicts with a generic anti-AI heuristic, the real style reference wins.
