# Humanizer Tone Pattern Catalog

This catalog deeply merges the two source approaches into one hierarchy. It keeps the empirical, minimal-edit discipline of `lieflat-less-ai-tone` and the broader coverage of `humanizer-zh`, while removing their contradictions.

## 1. Strong patterns

### Fake reversal and contrast

Trigger when the text invents an unnecessary wrong frame only to overturn it: `不是 A，而是 B`, `并非 A，而是 B`, `不在于 A，而在于 B`, `你以为……其实……`, `看似……实则……`.

Prefer the positive claim directly. Keep the contrast when the material genuinely corrects a real misconception or compares two actual alternatives.

### Dense enumeration and forced completeness

Do not ban three items. Change enumeration only when the list is padded, repetitive, or clearly shaped to look comprehensive.

Keep required technical lists, legal items, configuration sets, and procedures intact.

### Repeated sentence skeletons

When adjacent sentences repeat nearly the same grammatical order, punctuation, length, and ending, vary one sentence by merging, splitting, or reordering while preserving information.

Do not disturb deliberate parallel steps, requirements, dialogue, or literary rhetoric.

### Reveal-style em dash

Remove em dashes used only to stage a reveal or slogan.

Bad: `答案很简单——专注。`
Good: `答案是专注。`

Do not globally ban em dashes when they carry real parenthetical or rhetorical function.

### Empty colon framing

Fix empty lead-ins such as `核心是：`, `一句话总结：`, `原因如下：`, or a sentence that only announces the list below.

Keep colons in URLs, code, key-value data, dialogue, headings, and genuine general-to-specific explanation.

### Mechanical numbered headings

When three or more headings mechanically begin with `一、二、三` or `第一、第二、第三` and the numbering adds no reference value, keep the meaningful heading text and remove the number.

Keep numbered procedures, legal clauses, timelines, and headings referenced elsewhere by number.

### Idealized occupational personification

Replace praise-heavy metaphors such as `智慧导师`, `永不疲倦的秘书`, `全能顾问`, `贴身数字管家` with the actual function when the metaphor adds no mechanism or information.

Do not ban metaphor in general.

### Hide-the-data abstraction

If concrete data already exists nearby, prefer it over generic `显著提升`, `大幅增长`, `明显改善`, `进行了优化`.

Bad: `系统实现了效率提升。处理时间从两小时缩短到四十分钟。`
Good: `系统把处理时间从两小时缩短到四十分钟。`

Never invent data when none exists.

### Empty openers

Remove `说白了`, `说穿了`, `先说结论`, `一句话总结`, `值得注意的是` when they only announce rhetoric and add no information.

### Paragraph-opening subjectless commentary

If a non-opening paragraph starts with `听起来`, `看起来`, `关键在于`, `问题在于`, `意味着` and the referent is missing, add the smallest clear referent such as `这` or the actual subject.

## 2. Translation-pattern family

Treat only these recurring forms as targeted translation patterns. Long or formal Chinese is not automatically translationese.

### Long pre-nominal modifiers

Split overly long noun modifiers or repeated `的` chains when they force rereading, without changing information.

### Front-loaded `当……时`

When `当 + complete clause + 时` merely mirrors English `When ..., ...`, simplify if the temporal relation stays clear. Keep it when the time boundary matters.

### Front-loaded topic shells

Reduce `对于……来说`, `对……而言`, `就……而言`, `关于……`, `在……方面` when the object can directly serve as topic/subject and no scope limitation is lost.

### Sentence-initial signpost connectors

Move or remove `然而`, `因此`, `此外`, `与此同时`, `换言之`, `总而言之` only when they function as repetitive road signs. Keep them when they express real logic.

### `这意味着 / 这表明 / 这说明` recap

Merge or simplify when the sentence only restates the previous sentence. Keep it when it draws a genuinely new inference.

## 3. Contextual patterns

These are not automatic rewrite triggers.

### Grandiosity and promotional language

Watch for unsupported `至关重要`, `深刻`, `开创性`, `令人叹为观止`, `充满活力`, `关键转折点`, `不断演变的格局`, `持久影响`.

Replace hype with the actual fact or function when the material does not support the claim.

### Vague attribution

`专家认为`, `行业报告显示`, `观察者指出`, `多个来源表示` require a real source if used as evidence. In existing text, do not invent the missing source. In generated text, omit unsupported attribution.

### Formulaic challenge/future sections

Do not automatically add `挑战`, `未来展望`, or a positive outlook. Keep them only when requested or supported by real material.

### AI-word clusters

Words such as `此外`, `关键`, `格局`, `赋能`, `彰显`, `深入探讨`, `相互作用`, `复杂性` are weak signals individually. Rewrite only when several cluster together while adding little precision.

### Synonym cycling

Do not rotate precise nouns merely to avoid repetition. Repeating the correct term is better than artificial variety.

### Over-formatting

Avoid mechanical bold labels, decorative emoji, nested headings, one-line sections, and list fragmentation when a sentence or compact list is clearer. Do not ban formatting that improves scanability.

### Chatbot residue and flattery

Remove empty `当然！`, `好问题！`, `你说得完全正确！`, `希望这对你有帮助`, and generic `如果你愿意，我还可以……`.

Keep genuine acknowledgment when it carries social or task value.

### Generic positive endings

Do not end with `未来可期`, `迈出了重要一步`, `令人期待`. End on a concrete result, next step, limit, or simply stop.

### Excessive hedging

Reduce only redundant stacks. Preserve a single meaningful qualifier and the original confidence level.

### Model-centric disclaimers

Replace `根据我最后的训练数据`, `基于我可用的信息` with the actual evidence state when needed: what was checked, what was not verified, or what source is missing.

Do not hide real uncertainty.

### False ranges

Avoid `从 X 到 Y` when X and Y do not form a meaningful scale. Keep genuine ranges, timelines, numeric intervals, and ordered scopes.

### Inflated copula avoidance

Prefer plain `是 / 有 / 可以` when `作为 / 代表 / 标志着 / 充当 / 拥有 / 提供` only adds ceremony. Keep those verbs when they carry real technical meaning.

### English-only surface patterns

For English prose, also watch for trailing participial clauses that add fake depth (`..., highlighting/ensuring/reflecting ...`) and unnecessary Title Case in headings.

## 4. Explicit false positives

Do not rewrite solely because of:

- long or short sentences;
- paragraph length;
- passive voice;
- nominalization;
- rhetorical questions;
- metaphor in general;
- lack of first person;
- repeated use of the same precise noun;
- normal `首先 / 其次` in prose;
- a genuine three-item list;
- technical formality;
- ordinary connectors used for real logic.

## 5. Conflict resolutions between the source Skills

- **“Inject soul” vs preservation:** personality is allowed only in new drafting when context supports it. Existing-text edits do not add personality that was absent.
- **Vary rhythm vs evidence:** sentence-length variation is not a standalone target. Change rhythm only when repetition or clarity calls for it.
- **Two items vs three items:** there is no numeric ban. Only forced completeness is targeted.
- **AI vocabulary blacklist vs context:** individual words are weak signals; context and function decide.
- **First person:** never force `我/你`. For AI agents, use first person only for real agent actions or uncertainty, never fake lived experience.
- **Concrete details:** use provided or verified facts only. Never fabricate specificity.
- **Formatting:** do not globally ban bold, lists, or emoji; remove only mechanical or distracting use.
- **Structure:** preserve existing structure in editing; allow useful restructuring in new drafts.

Do not run the two source rule sets independently after applying this merged catalog. This file is the resolved authority.

## 6. Additional merged coverage

### Notability or media-name laundry lists

Do not use a list of famous outlets, experts, or follower counts as a substitute for the actual relevant claim. If a specific source matters, state the source and the point it supports. In Preservation Edit Mode, never invent a missing source or remove a cited source merely because the list feels promotional.

### Slogan-like negation and escalation

Treat `不仅……而且……`, `不仅仅是……更是……`, and repeated `这不只是……` as problems only when they function as empty escalation. Keep them when both sides carry distinct information or real contrast.

### Mechanical formatting

Bold labels, inline-heading lists, decorative emoji, and one-line sections are not banned. Simplify them only when they fragment a simple answer or add visual ceremony without improving scanability.

### English surface cleanup

For English prose, also watch for unnecessary Title Case, trailing participial phrases that pretend to add analysis (`..., highlighting/ensuring/reflecting ...`), and generic consultancy-style closings. Preserve established names, quoted text, and domain-specific capitalization.

### Quotation marks and punctuation

Do not normalize quotation marks or punctuation solely to make text look less AI-generated. Follow the target language, source style, and user conventions. Never change code, JSON/YAML, shell syntax, or quoted source material for typography alone.

## 7. Borrowed from oil-tone (drafting-oriented)

These target long-form drafting in Preservation Edit / Free Draft Mode. They are weaker signals in short agent replies.

### Title/slogan staging

Do not add a second half after a colon, comma, or dash to make a heading feel opinionated, rhythmic, or decisive: no `先……`, `简单,但……`, `不只是……`, `关键在于……` appended unless the material actually supports that claim.

Bad: `主流 AI Coding Agent:先选工作方式`
Better: `主流 AI Coding Agent 的工作方式`

Bad: `单文件 HTML 的结构:简单,但不随意`
Better: `单文件 HTML 的基本结构`

Keep the second half only when it is a real, material-supported conclusion the reader needs.

### Adjacent repeated facts

Do not restate the same number, fact, or conclusion in neighboring paragraphs. A paragraph that reacts or judges should reference the earlier fact, not re-report it. Closing summaries are the exception.

### Dropped process steps

When material includes a cause, an actual effect, and a follow-up action, keep all three related. Do not delete the middle step to shorten the text; completeness means the fact–reason–impact–handling chain is unbroken, not that the text is long.

### Spoken rhythm vs filler particles

Two separate things, do not merge them:

- Remove particles that carry no meaning (`当然可以`, `其实吧`, empty `呢/啊`).
- Keep structural particles that make a sentence read naturally aloud. `在、的、了、的时候` often carry grammar and rhythm. If compressing `使用的时候` into `使用时` makes the sentence read stiffly, keep the fuller form.

Do not fake spoken style by piling on interjections, and do not compress real function words to sound more telegraphic.

### Unsupported everyday-generalization openers

Do not open with invented collective experience: `很多人认为`, `经常有人问`, `大家都遇到过` when the material supplies no such group. State the actual situation or source.

## 8. Borrowed from tta-tone lint (broader coverage)

Same philosophy as section 7: drafting-oriented signals, weaker in short agent replies.

### Hollow nominalized verbs

`进行了优化`, `实现了提升`, `做了调整` hide the actor and the result. Rewrite to who did what and what changed. This targets the empty verb+abstract-noun shell only; ordinary nominalization stays fine (see false positives).

Bad: `我们对接口进行了优化,实现了提升。`
Better: `我们把接口的重试次数从 1 改到 3,超时率降了一半。`

### Publication bait and engagement calls

Reader-facing copy does not beg for engagement: `建议收藏`, `点个关注`, `一键三连`, `以上就是本期分享`, `关注不迷路`, `让我们开始吧`, `质的飞跃`; English `In this article`, `Let's get started`, `Bookmark this`. Open with the problem, end with the result or next step.

### Report-style openings

`以下是关于……的介绍/分析` restages a chatbot frame. Start with the subject doing something, not with an announcement of what the text will do.

### Openings carry their subject

The first sentence should show who is doing what in which situation. Do not open with subjectless drumming, `本文将介绍`, or a self-introduction. Reader-facing long-form may open with background, but the background still has a subject.

### Course-cliché framings

`这一课只带走`, `这一课结束` turn explanation into a lecture notice. Solve the problem at hand and stop at what the reader can do next.

### Courtesy shields

`仅供参考`, `抛砖引玉`, `不当之处敬请指正`, `以上只是个人浅见` swap judgment for politeness. State plainly which claim is not settled instead.

### Soft-news adjectives

`亮眼成绩`, `蓬勃发展`, `硕果累累`, `如火如荼` gesture at success without evidence. Use the material's numbers and actions; without material, delete.

### Officialese and slogan jargon

`砥砺前行`, `攻坚克难`, `齐心协力`, `底层逻辑`, `顶层设计`, `新质生产力`, `组合拳`, `全链路`, `破局` are empty in almost every occurrence. Name the concrete action or mechanism instead.
