# Humanizer Tone Examples

Use these examples for calibration, not as fixed templates.

## 1. Coding-agent completion report

Too model-like:

> 当然！我已经成功完成了您要求的配置工作。以下是本次操作的详细总结：
>
> **规则文件：** 已经成功写入。
> **加载验证：** 已经顺利完成。
> **下一步：** 如果您愿意，我还可以继续帮助您优化其他配置。

Preferred:

> 已完成，规则链正常。
>
> - `~/.agents/AGENTS.md`：12 条规则已加载
> - `~/.claude/CLAUDE.md`：仅保留 `@~/.agents/AGENTS.md`
> - 新 session 验证通过，无乱码、无 import 警告

## 2. Simple answer stays simple

Too much structure:

> ## 结论
> 当前配置没有问题。
>
> ## 原因
> 经检查，两个文件的路径均正确。
>
> ## 下一步
> 无需进一步操作。

Preferred:

> 当前配置没问题，两个路径都正确，不需要再动。

## 3. Complex answer may expand

> 我建议保留 A，删除 B。A 仍在加载链上；B 已经没有引用。
>
> **风险**
> - 删除 B 不影响当前 session。
> - A 仍被 `settings.json` 引用，不能一起删。
>
> **执行**
> 先备份 B，再删除并起新 session 验证。

## 4. Fake reversal

Before:
> 这不是一个 Shell 的问题，而是环境识别的问题。

After:
> 问题在环境识别。

Keep the contrast when correcting an actual misconception is itself part of the message.

## 5. Unsupported grandiosity

Before:
> 这项关键改动标志着整个 Agent 治理体系迈入了一个全新的阶段。

After:
> 这项改动把公共规则和 Claude 专属配置分开了。

## 6. Existing data beats abstraction

Before:
> 本次清理显著减少了冗余 MCP。原来有 19 个，现在剩 15 个。

After:
> MCP 从 19 个减到 15 个。

## 7. Do not fabricate specificity

Source:
> 构建速度明显变快了。

Wrong:
> 构建时间从 90 秒降到 32 秒。

Correct:
> 构建速度变快了。

## 8. Preserve a meaningful qualifier

Source:
> 这个改动在很大程度上解决了启动卡顿，但偶尔仍会复现。

Wrong:
> 这个改动解决了启动卡顿，但偶尔仍会复现。

Correct:
> 这个改动在很大程度上解决了启动卡顿，但偶尔仍会复现。

The qualifier carries the author's confidence and must survive.

## 9. Reduce only stacked hedging

Source:
> 这个问题可能潜在地在一定程度上或许与缓存有关。

Preferred:
> 这个问题可能与缓存有关。

The uncertainty remains; only redundant layers are removed.

## 10. Keep required technical lists

Good:
> 需要检查三个文件：`settings.json`、`CLAUDE.md`、`AGENTS.md`。

Do not collapse this merely because it contains three items.

## 11. Protect commands

Input:
```powershell
Get-Content $HOME\.claude\CLAUDE.md
```

Do not rewrite the command. Humanize only the explanation around it.

## 12. Editing mode preserves structure

Source:
> ## 原因
> 这个方案不是因为性能更高，而是因为依赖更少。
>
> ## 风险
> 迁移可能影响旧接口。

Preservation edit:
> ## 原因
> 这个方案的优势是依赖更少。
>
> ## 风险
> 迁移可能影响旧接口。

## 13. Do not fake human experience

Bad:
> 我个人一直很讨厌这种配置，它让我有点不舒服。

Better:
> 这个配置给 Agent 完整文件系统权限，风险较高。

First person is fine for real agent actions such as `我检查了三个配置文件`, not invented human experience.

## 14. No generic closing

Before:
> 以上就是本次分析。希望这些信息能帮助你更好地理解当前配置。如果你愿意，我还可以继续深入分析。

After:
> 当前先处理这两个冲突项，其他配置不用动。

## 15. Title without staged slogan

Bad:
> 主流 AI Coding Agent：先选工作方式

Better:
> 主流 AI Coding Agent 的工作方式

The staged second half is fine only when the material supports that conclusion.

## 16. Keep the natural particle when removal stiffens the sentence

Source:
> 使用的时候要先看日志。

Do not compress to:
> 使用时先看日志。

When the fuller form reads naturally aloud and the target register is prose, keep it. The rule targets empty particles, not grammatical ones.

## 17. Do not restate the same fact in the next paragraph

Reaction paragraph should reference, not re-report:

Weak:
> 缓存命中率从 62% 提到 89%。这一提升让命中率从 62% 提高到了 89%，效果显著。

Better:
> 缓存命中率从 62% 提到 89%。这个提升直接减少了回源请求。

## 18. Do not open with invented collective experience

Bad:
> 很多人都在问，全局规则到底该放哪。

Unless the material actually shows that; otherwise state the situation directly:

Better:
> 全局规则放 AGENTS.md，工具专属配置放各自的 Harness。

## 19. Publication bait goes

Bad:
> 以上就是本期分享，建议收藏，关注不迷路！

Better:
> 先把这两个冲突项处理掉，其他配置不用动。

End on the result or next step; never on an engagement call.

## 20. Hollow verb back to action

Source:
> 我们对构建流程进行了优化，实现了提升。

Wrong (still hollow, now with numbers invented):
> 我们对构建流程进行了深度优化，性能提升明显。

Better (only when the material supports it):
> 构建流程改成增量编译，构建时间从 90 秒降到 40 秒。

Without supporting data, keep only what the source states.
