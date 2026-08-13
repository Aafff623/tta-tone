<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="tta-tone：让 AI 文案保持真实、平实、完整和易读">
</p>

<p align="center">
  <a href="https://github.com/Aafff623/tta-tone/releases/tag/v0.0.1"><img src="https://img.shields.io/badge/version-0.0.1-2ea44f?style=for-the-badge" alt="version 0.0.1"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-informational?style=for-the-badge" alt="MIT"></a>
  <a href="https://github.com/Aafff623/tta-tone"><img src="https://img.shields.io/badge/github-Aafff623%2Ftta--tone-181717?style=for-the-badge" alt="Aafff623/tta-tone"></a>
</p>

`tta-tone` 是 threetwoa 的个人文风 Skill。它让模型在事实边界内，用同一套口吻完成中英文成稿、讲授项目模块、给出可执行建议，以及在编程工具对话里做克制的收尾。

当前公开版本 **0.0.1**。品牌是 threetwoa，源仓在 [Aafff623/tta-tone](https://github.com/Aafff623/tta-tone)。

## 三种任务

| 分支 | 何时用 | 骨架 |
| --- | --- | --- |
| 成稿 | 润色、改写、博客、演讲、PPT 文案、网站、简介 | 事实先写清，标题当标签，说完就停 |
| 讲授 | 分析模块、讲知识、带看代码 | 先定一个可检查的赢，打开仓库再讲，给完动作就停 |
| 答问 | 怎么办、要不要、下一步怎么选 | 先接处境，再给可执行结论，不加油 |

读者成稿不加颜文字和 emoji，也不加对话收尾表。对话里的讲授和答问：正文仍平实；收束用横式 `now` / `before` 表和引文框摘要；需要调味时按场景抽取现成混排。

## 对话收尾和调味

编程工具里的对话回复，末尾用横式两列表格：

| now | before |
| --- | --- |
| 这一则做了什么 | 上一则已经完成什么 |

表格下方用引用框写碎碎念，并补一句迄今为止整段对话的摘要。

调味不是全程撒表情。先认这一则的处境，再运行：

```bash
python skills/tta-tone/scripts/season.py --scene peek
```

| 这一则实际在干什么 | `--scene` |
| --- | --- |
| 做完，下一步是去看、去用 | `done` |
| 做完或做到一半，还要点未做项 | `peek` |
| 材料不够、判断没落地 | `think` |
| 和文档、预期、上一则说法不一致 | `surprise` |
| 先这样、本轮收住 | `tea` |
| 明确交给对方看、标、刷新 | `wait` |
| 只记下指令，下一则才动手 | `ack` |
| 挑样子、看陈列这类轻维护 | `play` |

本会话已经贴过的混排加 `--exclude`。同一条组合只用一次。不要手搓 `(・ω・) ✨` 这类输入法常见组合。细则在 `skills/tta-tone/references/seasoning.md`。

## 修改效果

| 常见写法 | tta-tone 的处理 |
| --- | --- |
| `主流 AI Coding Agent：先选工作方式` | `主流 AI Coding Agent 的工作方式` |
| `单文件 HTML 的结构：简单，但不随意` | `单文件 HTML 的基本结构` |
| `先把流程搞顺` | 说明需要检查、修改或确认的具体对象 |
| `真正重要的是，我们理解了工具的边界` | 内容说明完成后直接结束 |

这些修改不是为了把句子统一改短，而是删除材料没有支持的态度、节奏和升华，让标题与正文继续提供有效信息。

## 它会检查什么

- 事实是否来自现有材料，第一人称内容是否有依据。
- 面向读者时，是否根据情况自然使用「我们」或「大家」。
- 动词和对象是否准确，是否存在 `搞顺`、`跑起来` 等含糊动作。
- 句子语法、因果关系和操作过程是否完整。
- 标题是否直接说明内容，而不是自行制造文案感。
- 结尾是否添加了没有新信息的感悟或价值总结。
- 讲授时判断是否来自当前仓库，是否收在一个可检查的动作上。
- 建议是否落到具体对象，结尾是否多余加油。
- 读者成稿是否多加了颜文字、emoji，或误加了 `now` / `before` 表。

文件成稿用 `tone_lint.py`。程序只能识别已知套话，通读不能省。

## 安装

仓库中的 Skill 位于 `skills/tta-tone/`。远程是 `Aafff623/tta-tone`。

```bash
git clone https://github.com/Aafff623/tta-tone.git
```

Codex：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Aafff623/tta-tone \
  --path skills/tta-tone
```

手动安装：

```bash
cp -R tta-tone/skills/tta-tone ~/.codex/skills/tta-tone
```

安装后，在下一轮任务中使用 `$tta-tone` 调用。

## 使用

```text
使用 $tta-tone，把这份产品介绍改成可以直接发布的中文成稿。
```

```text
使用 $tta-tone，用我的语气讲清当前仓库里这个模块做什么、该打开哪些文件。一课收在一个我能检查的动作上。
```

```text
使用 $tta-tone，按现有材料给建议：要不要为这件事新开一个 Skill。
```

讲授和答问的顺序在 `skills/tta-tone/references/modes.md`。

## 脚本

只使用 Python 标准库。本机运行用 `python`。

```bash
python skills/tta-tone/scripts/tone_lint.py draft.md
python skills/tta-tone/scripts/tone_lint.py --self-test
python skills/tta-tone/scripts/season.py --scene tea --exclude "(´∀`)b👍"
python skills/tta-tone/scripts/season.py --self-test
```

`FAIL` 会让 lint 失败；`WARN` 对照上下文，有真实限定作用的可以留。

## 仓库结构

```text
tta-tone/
├── assets/readme/hero.svg
├── skills/tta-tone/
│   ├── agents/openai.yaml
│   ├── references/modes.md
│   ├── references/seasoning.md
│   ├── references/data/kaomojikan-emoji.json
│   ├── references/data/season-catalog.json
│   ├── scripts/season.py
│   ├── scripts/tone_lint.py
│   └── SKILL.md
├── CHANGELOG.md
├── LICENSE
├── README.md
└── VERSION
```

## 贡献

如果你发现一类稳定出现的 AI 文案问题，可以提交 Issue 或 PR。请同时提供：

1. 原句。
2. 问题在哪里。
3. 更自然、准确的改法。
4. 这条规则适用和不适用的情况。

这样可以避免为了修复一个例句，增加一条会伤害其他内容的机械规则。

## License

[MIT](./LICENSE)

## 从 oil-* 迁移

1. 删除旧安装：`rm -rf ~/.codex/skills/oil-* ~/.claude/skills/oil-*`
2. 删除旧配置：`rm -rf ~/.oil-cover ~/.config/oil-motion`（按需备份 API key）
3. 重新安装：`git clone https://github.com/Aafff623/tta-tone.git`
4. 重新写入 API key 到新配置路径（`~/.config/tta-cover/`、`~/.config/tta-motion/`）
