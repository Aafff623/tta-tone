# 知识库来源

读取日期：2026-08-13。

这份名单只给维护和核对用。`SKILL.md` 主步骤、`README.md` 产品介绍、`agents/openai.yaml`、短卡标题和开火线索，用 tta 的词，不出现下面这些人名和产品名。

## 工程轨读过的

| 名字 | URL | 抽了什么 |
| --- | --- | --- |
| GitHub Spec Kit | https://github.github.io/spec-kit/concepts/sdd.html ；https://github.com/github/spec-kit | 规格先于代码；文档自标 experimental |
| OpenSpec | https://openspec.dev/docs/overview | 先达成协议；delta 变更夹；一行修复不必上仪式 |
| Kiro Specs | https://kiro.dev/docs/specs/ | 复杂功能分相：需求 / 设计 / 任务 |
| HumanLayer / Dex Horthy，12-factor agents | https://github.com/humanlayer/12-factor-agents | 主干在确定性软件；LLM 插在决策点 |
| Anthropic：有效 agent | https://www.anthropic.com/engineering/building-effective-agents | 工作流先于自主环；能简单就不要加层 |
| Anthropic：上下文工程 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 注意力预算；最少高信号 token |
| Anthropic：Agent Skills | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 元数据常驻、正文触发、附件按需 |
| Claude Code 实践 | https://code.claude.com/docs/en/best-practices | 看起来做完会停；先探再改；小修复跳过计划 |
| Cursor Rules | https://cursor.com/docs/rules | 规则短、可组合；重复犯错再补 |
| Codex 实践 | https://developers.openai.com/codex/learn/best-practices | 写清怎么跑、怎么算完成；错两次再固化 |
| Aider | https://aider.chat/docs/repomap.html ；https://aider.chat/docs/usage.html | 只把要改的文件放进会话 |
| 本机 `skill-creator` | 本机 Skill | 三层披露；主文件发胀就拆 |
| 本机 `writing-for-agents` | 本机 Skill | 指针措辞决定会不会读到；完成条件要可核对 |
| 本机 `tdd`（Pocock 系） | 本机 Skill | 红绿一次一条缝；测公开界面 |

## 编排与轮转读过的

| 名字 | URL | 抽了什么 |
| --- | --- | --- |
| Matt Pocock / AI Hero | https://www.aihero.dev/ ；https://github.com/mattpocock/skills | 人触发编排、模型发现词表；阶段停点 |
| Dictionary of AI coding | https://github.com/mattpocock/dictionary-of-ai-coding | Harness、聪明区、上下文指针 |
| 本机 `ask-matt`（Ask Matt / `/ask-matt`） | 本机 Skill（`~/.claude/skills/ask-matt`，Codex 平行副本 `~/.codex/skills/ask-matt`） | 给人用的开发 Skill 路由器；`disable-model-invocation`，只能提示不能替人开火；阶段停点问法才读它自带的 `PHASE-BOUNDARIES.md`。不是 `wayfinder`（大雾画地图） |
| 本机 `ask-matt`、`to-spec`、`to-tickets`、`implement`、`wayfinder`、`grilling` | 本机 Skill | 对齐/规格可同窗；实现清窗；编排入口互不调用 |

## 探索轨读过的

| 名字 | URL | 抽了什么 |
| --- | --- | --- |
| Andrej Karpathy，Software 2.0 | https://karpathy.medium.com/software-2-0-a64152b37c35 | 同一功能可走代码或权重 |
| Karpathy，vibe coding 原文 | https://x.com/karpathy/status/1886192184808149383 （存档 https://archive.ph/yNSTA ） | 不看 diff 只给周末扔掉的项目 |
| Karpathy，YC 2025 / Software 3.0 | https://www.youtube.com/watch?v=LCEmiRjPEtQ ；https://www.latent.space/p/s3 | 窗口说明也是程序；部分自主滑杆 |
| Karpathy，Ascent 2026 清洗稿 | https://karpathy.bearblog.dev/sequoia-ascent-2026/ | 能核对的才自动化；生产看 diff、设评测 |
| Karpathy，autoResearch | https://github.com/karpathy/autoResearch | 人写说明书；评测锁死；agent 改可动文件 |
| Karpathy，State of GPT / How I use LLMs | https://www.youtube.com/watch?v=bZQun8Y4L2A ；https://www.youtube.com/watch?v=EWvNQjAaOHw | 尖齿工具；上下文是工作记忆 |
| Geoffrey Huntley，Ralph | https://ghuntley.com/ralph/ | 磁盘才是记忆；外环停手在可机检条件 |
| HumanLayer：Ralph 简史 | https://humanlayer.dev/blog/brief-history-of-ralph | bash 外环不是会话内钩子；规格差则循环废 |
| Anthropic：长程 harness | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 一口吃完半截；看一眼就宣告完成 |
| Aviator：先审规格 | https://www.aviator.co/blog/what-if-code-review-happened-before-the-code-was-written/ | 人审 spec；写的不给自己打分 |
| DebateCoder | https://aclanthology.org/2025.acl-long.589/ | 测例当辩论介质；执行结果定输赢 |
| AgentCoder | https://arxiv.org/html/2312.13010 | 测例设计和代码生成拆开 |
| 本机 `playground` / `eval-harness` / `continuous-learning` | 本机 Skill | 隔离沙箱；评测口径；不要每会话长出新 Skill |

## 不要混、不要写进短卡正文

- 本机 `ralph-loop` 是六段流程（研究 → 分析 → 学习 → 计划 → 编码 → 修复）。Huntley 的 Ralph 是 bash 外环、新鲜窗口。名字撞车，机制不是同一套。
- 本机 `tdd-workflow`（ECC，覆盖率口径）不进这套。窄缝只走公开界面、一次一条。
- Recipe for Training Neural Networks 的「静默变差 / 一次一层」已经接到讲授「打开再解」，不要在 kb 里再摘要一遍。
- 表演句不进短卡：合同金额、醒来六个仓、科幻序、钢铁侠、10x。
