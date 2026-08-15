# 知识库索引

这是**工程短卡**。成稿用词、黑话、联想走 [voice/](../voice/INDEX.md)，不要从这里找开口。

闲聊、纯润色、只改开口：不读这里。

讲开发、agent 怎么干活、何时停、怎么写给 agent 看的文档：打开本页，只打开命中的 1–2 篇，读完就关。不要整套搬。不要报编号。文风、招式、交付仍走 `SKILL.md` / `layers.md`。这不是第四张嘴。

## 先抽这条树

1. 有没有机检停条件？没有 → 不要循环。读 [craft/stop-and-scout.md](craft/stop-and-scout.md)。问的是「能不能把人从内环拿开」时，再读 [explore/verify-inner.md](explore/verify-inner.md)。
2. 记忆在磁盘还是聊天？聊天 → 不要跨窗口。读 [explore/disk-memory.md](explore/disk-memory.md)。
3. 写的和验的是不是同一个模型？是 → 拆开。读 [explore/spec-then-split.md](explore/spec-then-split.md)；评测文件会不会被改，读 [explore/human-writes-eval.md](explore/human-writes-eval.md)。

一条树走完仍没命中，再查下面的表。已经打开两篇就停。

## 工程轨

相对稳定。讲 workflow、规格、规则怎么写、测试怎么锁时抽。

| 线索 | 读 | 停 |
| --- | --- | --- |
| 先写规范再做；随口就改；已有代码怕顺手重构 | [craft/spec-delta.md](craft/spec-delta.md) | 规格过目，或确认这是一行修复 |
| 怎么算做完；要不要先计划；看起来做完了 | [craft/stop-and-scout.md](craft/stop-and-scout.md) | 停条件可运行，或小修复已跳过计划 |
| agent 不稳；要不要全自主；谁批准 | [craft/spine-and-gate.md](craft/spine-and-gate.md) | 控制流在代码里，或停在人闸 |
| 规则太长；上下文烂；Skill 怎么拆；为什么不听 | [craft/budget-and-pointer.md](craft/budget-and-pointer.md) | 新材料有指针，同一错才补规 |
| 测试先行；测了内部；红绿一次补太多 | [craft/narrow-seam.md](craft/narrow-seam.md) | 公开界面上一条缝已绿 |
| 这块完了下一块；实现和讨论挤在一起；长会话发糊 | [craft/phase-window.md](craft/phase-window.md) | 对齐/规格可同窗，实现已清窗 |
| 两份入口同一套问法；主文件发胀；人记名字还是模型发现 | [craft/entry-lexicon.md](craft/entry-lexicon.md) | 编排归人触发，词表归一份 |
| 不知道用哪份开发 Skill；懵了该走哪条流程；不是写稿也不是讲模块 | [craft/skill-router.md](craft/skill-router.md) | 已接处境并写出 `ask-matt`；目录选型不由 tta-tone 做 |

## 探索轨

实验性。谈 agent 循环、评测、自主、范式时才抽。不当默认 workflow。

| 线索 | 读 | 停 |
| --- | --- | --- |
| 手写、训练、还是交给窗口说明 | [explore/three-ways.md](explore/three-ways.md) | 这轮只派一条路 |
| Accept All；生产放飞；周末扔掉的项目 | [explore/autonomy-slider.md](explore/autonomy-slider.md) | 自主量是人定的，生产看 diff |
| 跨会话；过夜；进度只在聊天里 | [explore/disk-memory.md](explore/disk-memory.md) | 进度已落在 git 或计划文件 |
| 人写说明书；评测被 agent 改；有没有单一标量 | [explore/human-writes-eval.md](explore/human-writes-eval.md) | 评测锁死，没有标量就不要循环 |
| 规格先审；自己给自己打分；用辩论代替运行 | [explore/spec-then-split.md](explore/spec-then-split.md) | 写和验拆开；无执行器就不要辩论 |
| 模型能力不均匀；未知库；想法还没形状 | [explore/jagged-sandbox.md](explore/jagged-sandbox.md) | 先隔离目录，再决定进主仓 |
| 这活交给 agent 会不会飞；何时把人从内环拿开 | [explore/verify-inner.md](explore/verify-inner.md) | 不能自动核对就留人 |

## 不要

- 让用户报层号、短卡编号、轻 / 述 / 拆。
- 把短卡写进开口、身份、招式轴。
- 外来产品名当标题。人名和 URL 见 [sources.md](sources.md)。
- 本机一份六段循环 Skill，和网上「外环脚本」不是同一套；不要混讲。
- 另一套覆盖率流程不要写进窄缝。
- 大雾画地图那份（`wayfinder`）不是给人用的开发 Skill 路由器。

出处人名、产品名和 URL 见 [sources.md](sources.md)。读取日期 2026-08-13。
