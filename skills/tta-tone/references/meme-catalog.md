# Meme source inventory and routing

This is a provenance and routing record, not a copied meme encyclopedia. The
full clones stay in `temp/references/sources/`; the Skill uses only a reviewed
subset and records why a source is trusted or restricted.

## Priority tiers

### Tier 1: Chinese internet and programmer-adjacent usage

| Source | Pinned revision | What it contributes | Decision |
| --- | --- | --- | --- |
| [CHIME](https://github.com/yuboxie/chime) | `865ef186a0e797ec5ac242524a3c45b30a429542` | 1,458 phrase memes; meaning, origin, examples, type, profanity/offense labels | Research and safety labels; only reviewed low-risk entries enter the runtime catalog |
| [Meme Archive](https://github.com/ThySummer14/meme-archive) | `e2ebc04a48e59155093828db1a3a788eb9cc7082` | 11 circles, lifecycle (`active`, `longevity`, `fading`, `fossil`), platforms, sources, related memes | Main taxonomy and freshness gate; no unsourced or stale entry is auto-emitted |
| [wesbos/dad-jokes](https://github.com/wesbos/dad-jokes) | `892d244f6710f27e7a0168589c1abd03fcdeb5ea` | Programmer wordplay such as Git, SQL, API, and language jokes | Inspiration only; no direct joke insertion into work reports |
| [ABSphreak/readme-jokes](https://github.com/ABSphreak/readme-jokes) | `eb29fd08ae0cd4121c060c7dd8f1dc9aac133a30` | A derived programming-joke feed and API presentation pattern | Inspiration only; upstream README says its jokes are generated from `wesbos/dad-jokes` |

CHIME is MIT and labels profanity/offense, but it is a research dataset. Meme
Archive has rich provenance fields but no root license file in the inspected
clone. The joke repositories have permissive or unclear content boundaries and
are not treated as distributable source text. We carry taxonomy and gating
ideas, not bulk copied entries.

### Tier 2: other circles

Meme Archive's `gaming`, `acg`, `kawaii`, `film-tv`, `platform`, and
`international` categories are optional expansion pools. Add an entry only when
it has a source, a clear meaning, a freshness state, and a non-offensive use
case. Do not let a niche circle become the default voice for general technical
work.

### Tier 3: image and reaction archives

Image-template collections and scraped meme crawlers are reference-only. They
often carry image rights, unstable links, missing provenance, or platform-
specific meanings. TTA Tone should not fetch or reproduce an image meme merely
because a phrase resembles its caption.

## Meme routing gates

Before using a meme, check in order:

1. **Audience**: the user has used the meme, asks for a playful style, or the
   context is explicitly casual.
2. **Meaning**: the intended meaning is known without relying on an uncertain
   origin story.
3. **Risk**: no security, legal, financial, medical, privacy, harassment, or
   irreversible-action content is being softened.
4. **State**: the meme does not turn partial success, a candidate cause, or an
   unverified estimate into a confident claim.
5. **Freshness**: `active` and `longevity` entries are preferred; `fading` and
   `fossil` entries require user-led or explanatory context.
6. **Frequency**: one meme at most per response, and no repeated meme in
   adjacent turns unless quoting the user.

If any gate fails, use a cataloged emoji or kaomoji instead. If the user asks
what a meme means, explain it plainly first and mark the origin as uncertain
when the source does not establish it.
