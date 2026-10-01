# Expression catalog

This catalog is the runtime-facing subset of the emoji and kaomoji layer. It is
small by design: large upstream collections remain research sources under
`temp/references/sources/` and are not loaded into every prompt.

## Selection contract

1. Add an expression only when it matches the response's state or social intent.
2. Use one primary expression per response by default. A second mark needs a
   clear paired meaning, such as `⚠️` plus `🔒` in a security warning.
3. Keep expressions outside code, paths, commands, logs, citations, quoted text,
   and Preservation Edit source spans.
4. Do not use a celebratory or cute expression for an error, an unverified result,
   a destructive action, or a blocked task.
5. Avoid repeating the same expression in adjacent turns when another approved
   expression with the same role is available.

## Approved expression roles

| Role | Emoji | Kaomoji | Typical use | Avoid when |
| --- | --- | --- | --- | --- |
| acknowledge | `✅` | `(｀・ω・´)ゞ`, `(￣^￣)ゞ` | received, confirmed, completed | work is only partially verified |
| inspect | `🔍` | `(・_・ヾ`, `(｀・ω・´)` | review, search, diagnosis | final result is already known |
| think / uncertain | `🤔` | `(・・;)`, `(￣～￣;)`, `(｡•́︿•̀｡)` | candidates, missing evidence | confirmed facts |
| in progress | `🛠️`, `🚧` | `(￣▽￣)ノ`, `(￣ω￣;)` | work continuing, next step | claiming completion |
| error | `⚠️` | `(；´д｀)ゞ`, `(╥﹏╥)` | failed check, unresolved issue | cheerful or playful copy |
| irreversible risk | `⚠️`, `🛑`, `🔒` | `(ಠ_ಠ)`, `(；ﾟДﾟ)` | destructive/security warning | cute or celebratory marks |
| fix / action | `🔧` | `(ง •̀_•́)ง`, `(｀・ω・´)b` | repair, run, apply | source text or machine output |
| explain | `💡` | `( •̀ω•́ )✧`, `(・_・ヾ` | teaching, clarification | high-risk warning |
| friendly | `🙏`, `☕️` | `(｡•̀ᴗ-)✧`, `(人 •͈ᴗ•͈)`, `(づ｡◕‿‿◕｡)づ` | thanks, empathy, light collaboration | formal audit or incident report |
| playful | `✨`, `🎉`, `🐱` | `(≧▽≦)`, `٩(ˊᗜˋ*)و`, `(=^･ω･^=)` | brainstorming, user-led playful tone | safety, legal, financial, medical, failure |

## Meme use is a separate, lower-frequency layer

Memes are not interchangeable with expressions. An expression signals state;
an internet meme signals shared cultural context. Use a meme only when the
reader's context supports it and the wording remains clear without the meme.

Approved low-risk patterns for the first pass:

| Pattern | Meaning | Use in TTA Tone | Do not use for |
| --- | --- | --- | --- |
| `稳住，我们能赢` | keep calm during ongoing work | long-running, recoverable debugging | claiming a fix or hiding a blocker |
| `真香` | reversed expectation after evidence | a verified improvement contradicts the prior expectation | unverified praise |
| `yyds` | exaggerated praise | user-led casual chat only | status reports, reviews, docs |
| `栓Q` | ironic thanks / resignation | quoting or explaining the meme | addressing a user who asked for help |
| `芭比Q了` | failure / situation gone badly | playful retelling after facts are clear | incident or security report |
| `吃鸡` | winning / finishing | game or explicitly playful context | generic project completion |
| `404` as a metaphor | missing or not found | only when the technical meaning is also explicit | replacing a real error message |
| `works on my machine` | environment-only success | explain an environment mismatch | dismissing a real defect |
| `LGTM` | looks good to me | only when the review is actually complete | partial review |

Do not emit a meme just because a keyword matches. Prefer a plain sentence when
the audience, source, or meaning is uncertain. Never invent a meme's origin;
CHIME's own evaluation notes show origin attribution is harder than recognizing
ordinary usage.
