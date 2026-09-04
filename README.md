# tta-tone

给 AI coding agent 和通用助手用的输出语言层 Skill:让每一条面向用户的自然语言回复直接、自然、少 AI 腔,同时保住事实、限定词、范围和技术字面量。对既有文稿只做最小修改,对新成稿按目标文风直接写对,不靠事后修饰。

Skill 位于本仓库的 `skills/tta-tone/`。

## 三种模式

| 模式 | 何时用 | 纪律 |
| --- | --- | --- |
| Agent Output(默认) | 会话回复、状态汇报、评审、计划、交接 | 结果先行,短段落或 2–6 条紧凑要点 |
| Preservation Edit | 用户要求去 AI 味、润色既有文稿 | 最小修改,不动结构、事实、语气 |
| Free Draft | 起草新文稿、用户允许大改 | 允许重组,但不编造事实和伪人味 |

规则冲突时按序裁决:事实与用户本轮要求 > 因果/时间线/范围完整 > 含义与结构 > 节奏排版。

## 它会检查什么

- 空泛开场和模板领起语(`说白了`、`值得注意的是`、`原因很简单`)。
- 宣传黑话、政经套话和官腔(`赋能`、`抓手`、`底层逻辑`、`砥砺前行`)。
- 通用乐观结尾、空泛重要性判断(`未来可期`、`里程碑式意义`)。
- 聊天残留、发布腔和营销号召(`当然可以`、`建议收藏`、`点个关注`)。
- 模糊归因和客套保护句(`专家认为`、`仅供参考`)。
- 名词化空壳动词(`进行了优化`)、重复限定、刻意反转(`不是……而是……`)。
- 全文级结构:连续单句短段、设问偏多、加粗当拐棍。

完整目录见 [skills/tta-tone/references/patterns.md](skills/tta-tone/references/patterns.md)。规则是检查线索,不是禁词表:单次出现且承担真实限定或逻辑作用时保留。

## 安装

```bash
git clone https://github.com/Aafff623/tta-tone.git
```

把 `skills/tta-tone/` 拷进你的 harness 的 skills 目录(已知兼容 `~/.agents/skills/`、`~/.claude/skills/`、`~/.cursor/skills/`,其他支持 Anthropic skill 格式的目录同样适用):

```bash
cp -R tta-tone/skills/tta-tone ~/.agents/skills/
```

安装后,在下一轮任务中按 harness 的方式调用(如 `$tta-tone`)。

## 使用

```text
把这段汇报去 AI 味,结构和小标题不要动。
```

```text
用自然的方式给我汇报结果:改了哪三个文件、验证是否通过。
```

```text
按这份材料写一篇发布用的说明,不编数据,不加营销号召。
```

## 脚本

只用 Python 标准库。

```bash
python skills/tta-tone/scripts/tone_check.py draft.md
python skills/tta-tone/scripts/tone_check.py --self-test
```

`FAIL` 是已确认问题,改完再运行;`WARN` 和 `STRUCT` 需要结合上下文判断,确有作用时可以保留。程序只能识别已知模式,不能判断事实,也不能代替通读。

## 仓库结构

```text
tta-tone/
├── skills/tta-tone/
│   ├── agents/openai.yaml
│   ├── references/patterns.md
│   ├── references/preservation-edit.md
│   ├── references/examples.md
│   ├── evals/evals.json
│   ├── scripts/tone_check.py
│   └── SKILL.md
├── LICENSE
└── README.md
```

## 贡献

如果你发现一类稳定出现的 AI 文案问题,可以提交 Issue 或 PR。请同时提供:

1. 原句。
2. 问题在哪里。
3. 更自然、准确的改法。
4. 这条规则适用和不适用的情况。

这样可以避免为了修复一个例句,增加一条会伤害其他内容的机械规则。

## License

[MIT](./LICENSE)
