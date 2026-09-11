# Evaluations

盲评配对评测：对比 baseline（裸任务提示词）与 candidate（注入 SKILL.md 全文）在同一用例上的回复质量。评测体系移植自 [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)（MIT），维度按 tta-tone 定位重设。

## 用例目录的镜像规则

- `cases.jsonl`：盲评流水线的唯一用例源（id/category/prompt/risk/criteria）。
- `evals.json`：随 skill 分发的静态断言用例（部分 harness 直接读取该格式）。

两者重叠的用例内容必须一致：改任何一边，同步改另一边（与 tone_check.py ↔ patterns.md 的镜像纪律相同）。

## 验证与规划

```bash
python scripts/run_evals.py validate
python scripts/run_evals.py plan --trials 3
```

## 跑分（以本地 InferX 免费端点为例）

`runners.local.json` 是本机运行配置（已 gitignore，不含密钥）；`openai_runner.py` 从环境变量读 `OPENAI_BASE_URL` / `OPENAI_MODEL` / `OPENAI_API_KEY`，密钥永不落文件。也可参考 `runners.example.json` 用 claude/codex CLI 跑（agent CLI 隔离用 `--setting-sources ""`；provider 路由在 settings env 块里会被隔离剥掉，需配 `claude_isolated.py` 包装）。

```bash
export OPENAI_BASE_URL="https://model.inferx.net/endpoints/v1"
export OPENAI_MODEL="glm-5.3-flash"
export OPENAI_API_KEY=...   # InferX key, ix- 前缀

python scripts/run_evals.py run \
  --runner-config evals/runners.local.json --runner inferx \
  --condition baseline --trials 3 \
  --budget-usd 1 --allow-unmetered \
  --output evals/results/responses.jsonl

python scripts/run_evals.py run \
  --runner-config evals/runners.local.json --runner inferx \
  --condition candidate --condition-skill SKILL.md --trials 3 \
  --budget-usd 1 --allow-unmetered \
  --output evals/results/responses.jsonl
```

免费端点不报美元成本，必须显式 `--allow-unmetered`（端点本身零计费即视为有硬顶）。跑分可断点续跑：同一命令重跑会跳过已完成的 `(case, trial, condition, runner)` 行。runner 在临时空目录里执行，防止 agent CLI 把 skill 仓库当项目上下文。

## 盲评与汇总

```bash
python scripts/judge.py \
  --runner-config evals/runners.local.json --runner inferx \
  --responses evals/results/responses.jsonl \
  --output evals/results/scores.jsonl

python scripts/run_evals.py score evals/results/scores.jsonl
```

judge 按 `(case_id, trial)` 分组、一次调用内盲评全部条件：条件重标为 A/B/C，置换由组键哈希派生（可复跑、按组乱序）。rubric 只有 `judge:begin/end` 标记之间的部分发给裁判，条件名不会泄漏。坏裁判回复只跳过本组，不拖垮整个输出文件。

## 发布门禁

candidate 需同时满足：无 blocker；correctness / safety / truth_preservation 各自不低于 baseline −0.1；加权总分高于 baseline。公开发布对比数字时，用例、模型、trial 数、rubric 必须同批，并记录 CLI 与模型版本。

## 单元测试

```bash
python -m unittest discover -s tests
```

覆盖标签置换、盲评提示词不泄漏条件名、坏回复跳组、评分配对校验（不发起真实 LLM 调用）。
