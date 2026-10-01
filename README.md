# tta-tone

给 AI coding agent 和通用助手用的输出语言层 Skill:让每一条面向用户的自然语言回复直接、自然、少 AI 腔,同时保住事实、限定词、范围和技术字面量。对既有文稿只做最小修改,对新成稿按目标文风直接写对,不靠事后修饰。会话回复还要求对读者可执行:下一步动作先行、可执行步骤编号、跨轮重述进度,但可执行性不得凌驾于真实性之上。

Skill 位于本仓库的 `skills/tta-tone/`。

规则链在对话开始加载，执行期间每次回复和最终汇报都重新经过场景路由与输出自检；首次加载不能替代后续执行。公共规则定义输出契约，项目 `AGENTS.md`/`CLAUDE.md` 引用 Skill 并补充仓库边界，`CONTEXT.md` 记录维护事实。该约束属于指令层，不能保证模型永不偏离，也不等于已实现 Hook 拦截。

## 按场景路由的四种模式

| 模式 | 何时用 | 纪律 |
| --- | --- | --- |
| Direct / Casual | 短问答、致谢、明确要求只给一个值 | 只回答所问,不制造结构 |
| Preservation Edit | 用户要求去 AI 味、润色既有文稿 | 最小修改,不动结构、事实、语气 |
| Agent Output | 会话回复、状态汇报、评审、计划、交接 | 结果先行,状态和下一步清楚 |
| Free Draft | 起草新文稿、用户允许大改 | 按读者和体裁重组,不编造事实 |

四种模式共享同一层事实、范围、限定词、因果和技术字面量保护规则;模式决定结构和改写权限，输出密度在路由后单独选择。路由和冲突处理见 [skills/tta-tone/references/routing.md](skills/tta-tone/references/routing.md)。

输出密度在路由之后单独选择：`Normal` 保持完整语法，`Tight` 去掉重复框架，`Compressed` 只在顺序和因果仍清楚时使用。安全警告、不可逆操作、多步顺序和证据不足的片段自动恢复完整表达；密度规则不等于上下文压缩，也不能单独证明 token 或成本下降。Caveman 的蒸馏取舍和 pinned revision 见 [skills/tta-tone/references/distillation.md](skills/tta-tone/references/distillation.md)。

Emoji、颜文字和互联网梗属于独立的表达层。每条自然语言回复都带一个场景匹配的表达标记；梗的使用频率低于 emoji/颜文字，并经过受众、风险、含义、时效和来源检查。规则与小型词库见 [expression-catalog.md](skills/tta-tone/references/expression-catalog.md) 和 [meme-catalog.md](skills/tta-tone/references/meme-catalog.md)。

规则冲突时按序裁决:事实与用户本轮要求 > 因果/时间线/范围完整 > 含义与结构 > 节奏排版。

## 它会检查什么

每条面向用户的自然语言回复必须包含至少一个适合场景的 emoji 或颜文字，通常一条回复用一个。闲聊可用颜文字，技术解释用语义符号，错误和安全警告使用克制的风险符号。符号不进入代码、命令、日志、机器数据或受保护原文；后续明确要求无表情或精确格式时遵从该要求。

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
python skills/tta-tone/scripts/preservation_check.py source.md edited.md
python skills/tta-tone/scripts/validate_catalog.py
```

语气扫描的 `FAIL` 是明确命中的问题，`WARN` 和 `STRUCT` 需要结合上下文判断，不因提示就机械改写；用 `--mode direct|preservation|agent|draft` 指定场景，全文结构提示仅用于 draft。守恒检查的 `FAIL` 表示检测到结构或字面量变化，仍须检查是否有明确改写授权。两种脚本都不能证明语义等价。

盲评评测流水线(移植自 i-have-adhd,维度按本 skill 重设,详见 [skills/tta-tone/evals/README.md](skills/tta-tone/evals/README.md)):

```bash
python skills/tta-tone/scripts/run_evals.py validate
python -m unittest discover -s skills/tta-tone/tests
```

改 SKILL.md 后想拿分数说话,按 evals/README.md 的流程跑 baseline/candidate 配对盲评。

五个 Caveman × TTA Tone 场景的默认/润色对照见 [skills/tta-tone/references/caveman-comparison.md](skills/tta-tone/references/caveman-comparison.md)，用于行为回归示例，不冒充模型或 provider 实测。

## 仓库结构

```text
tta-tone/
├── skills/tta-tone/
│   ├── agents/openai.yaml
│   ├── references/patterns.md
│   ├── references/preservation-edit.md
│   ├── references/examples.md
│   ├── references/routing.md
│   ├── references/distillation.md
│   ├── references/caveman-comparison.md
│   ├── references/expression-catalog.md
│   ├── references/meme-catalog.md
│   ├── references/expression-catalog.json
│   ├── references/meme-catalog.json
│   ├── evals/evals.json
│   ├── evals/cases.jsonl
│   ├── evals/rubric.md
│   ├── evals/runners.example.json
│   ├── evals/README.md
│   ├── scripts/tone_check.py
│   ├── scripts/preservation_check.py
│   ├── scripts/run_evals.py
│   ├── scripts/judge.py
│   ├── scripts/claude_isolated.py
│   ├── scripts/openai_runner.py
│   ├── tests/test_judge.py
│   ├── tests/test_preservation_check.py
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

## 致谢

Agent Output 模式的可执行性规则（步骤编号、状态重述、错误就事论事、收尾单一动作等）吸收自 [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)（MIT），并按本 skill 的保真优先原则做了约束收敛。

## License

[MIT](./LICENSE)
