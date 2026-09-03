#!/usr/bin/env python3
"""Check Chinese/English copy for known humanizer-tone issues.

FAIL  = confirmed issue (empty filler, hype jargon, officialese, chatbot
        residue, publication bait, fabricated-looking attribution).
WARN  = possible AI tell; keep when it carries real function.
STRUCT= whole-document checks (short-sentence drumming, question flooding,
        bold-as-crutch); always advisory.

Zero dependencies (Python 3 stdlib only). Rules mirror references/patterns.md.
Run self-test before trusting the rules:  python3 tone_check.py --self-test
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

Rule = tuple[re.Pattern[str], str]

# FAIL: functionally empty / formulaic in almost every occurrence.
RULES: tuple[Rule, ...] = (
    (re.compile(r"(?:说白了|说穿了|一句话总结|先说结论|值得注意的是|值得一提的是|需要指出的是|毋庸置疑|众所周知|不言而喻)"), "空泛开场/转场,直接进入具体内容。"),
    (re.compile(r"(?:核心问题是|关键区别在于|原因很简单|综上所述|总而言之)"), "模板化领起/总结语,删除后直接说明内容。"),
    (re.compile(r"(?:真正重要的是|真正的关键是|这不仅仅?是|从更大的角度看|理解了……才能……)"), "没有增加信息的升华表达,删除或改为具体判断。"),
    (re.compile(r"(?:未来可期|开启(?:了)?(?:全新|新)的篇章|迈出(?:了)?(?:重要|关键)(?:的)?一步|让我们拭目以待|前景广阔|充满无限可能|大有可为)"), "通用乐观结尾,改为具体结果/下一步或直接结束。"),
    (re.compile(r"(?:当然可以|这是一个(?:非常|很)?好的问题|你说得完全正确|希望这对(?:你|您)有帮助|如需更多(?:信息|帮助))"), "聊天残留/讨好表达。"),
    (re.compile(r"(?:业内|行业|专家|观察者|不少用户|多项研究)(?:普遍)?(?:认为|指出|表示|表明|反馈)"), "模糊归因;有真实来源时写出来源,没有则不保留权威背书。"),
    (re.compile(r"(?:赋能|撬动|抓手|闭环|沉淀价值|彰显意义|破局|组合拳|全链路|价值落地|底层逻辑|顶层设计|新质生产力|降本增效|提质增效|数智化)"), "宣传黑话/政经套话,直接说明具体作用。"),
    (re.compile(r"齐心协力|攻坚克难|砥砺前行|再创辉煌"), "空泛官腔,直接说明具体动作或结果。"),
    (re.compile(r"具有(?:深远|划时代|里程碑式)的?(?:历史)?意义|谱写了?.{0,12}新华章"), "空泛重要性判断,改为材料已确认的动作、变化或结果。"),
    (re.compile(r"(?:在当今|在当前)[^。]{0,16}(?:时代|背景|环境)下"), "空泛时代背景开场,无必要背景时删除。"),
    (re.compile(r"(?:标志着|代表着)[^。]{0,20}(?:重要|关键)(?:一步|时刻|转折点)"), "改为已确认的动作/变化/结果。"),
    (re.compile(r"说人话版本?|我踩过的坑"), "公开稿不要用这类标签当标题或节名。"),
)

# WARN: possible AI tell; decide by context and function.
WARNING_RULES: tuple[Rule, ...] = (
    (re.compile(r"随着[^。]{0,16}(?:不断|持续)(?:发展|演变|变化)"), "确认该变化是否与后文有具体关系,否则删除。"),
    (re.compile(r"(?:可能|或许|也许|在一定程度上|在某种程度上).{0,10}(?:可能|或许|也许|在一定程度上|在某种程度上)"), "合并重复限定,保留一个符合事实状态的限定词。"),
    (re.compile(r"(?:此外|与此同时|换言之)"), "若仅作路标连接可删;表达真实逻辑时保留。"),
    (re.compile(r"(?:这意味着|这表明|这说明)"), "若仅复述上句则合并;有新推断时保留。"),
    (re.compile(r"(?:搞|弄|整)(?:顺|清楚|明白|好|完|懂|定|起来|下去)"), "含义含糊的单字动作词;改用准确动词。"),
    (re.compile(r"跑(?:测试|流程)"), "『运行测试/流程』更准确。"),
    (re.compile(r"把[^。]{0,12}(?:塞进|塞到|喂给)[^。]{0,12}"), "『写入/添加/提供』更准确。"),
    (re.compile(r"(?:显著|大幅|明显)(?:提升|增长|改善|优化)"), "附近有具体数据时优先用数据;没有数据时不夸大。"),
    (re.compile(r"(?:智慧导师|永不疲倦的秘书|全能顾问|贴身数字管家)"), "理想化拟人;改为实际功能描述。"),
    (re.compile(r"从[^。]{0,12}到[^。]{0,12}"), "确认 A/B 是否构成有意义范围;无则删。"),
    (re.compile(r"(?:不仅|不只)[^。]{0,15}(?:更是|而且)"), "确认是否空泛递进;两边都有独立信息时保留。"),
    (re.compile(r"不是[^。]{2,24}而是"), "少堆『不是……而是……』;纠正误解时最多自然用一次,能正面说就正面说。"),
    (re.compile(r"(?:从而确保|进而体现|进一步彰显|反映了更深层次)"), "事实后的分析尾句;材料不支持该因果或判断时删除。"),
    (re.compile(r"尽管[^。]{0,24}(?:挑战|困难)[^。]{0,24}(?:仍|依然|未来)|机遇与挑战并存|挑战中蕴含机遇"), "直接说明已确认的限制、结果或后续安排。"),
    (re.compile(r"为.{1,24}奠定(?:了)?(?:坚实的?)?基础"), "说明具体产生了什么后续条件或结果。"),
    (re.compile(r"(?:彰显|凸显|体现)(?:了)?[^。]{0,20}(?:重要性|意义|价值)"), "确认重要性判断是否有材料支持。"),
    (re.compile(r"(?:建议收藏|点个收藏|点个关注|一键三连|以上就是本期分享|让我们开始吧|关注不迷路|质的飞跃|以下是关于[^。]{0,24}的(?:介绍|分析|回答|说明))"), "发布腔/营销号召/报告腔开场,直接进入问题或内容。"),
    (re.compile(r"亮眼成绩|蓬勃发展|欣欣向荣|硕果累累|如火如荼"), "软文形容词;改为材料已确认的动作、数量或结果,没有材料就删。"),
    (re.compile(r"仅供参考|不当之处敬请指正|抛砖引玉|以上只是个人浅见"), "客套保护句;写清哪一句没写死,不用客套代替判断。"),
    (re.compile(r"据了解|相关人士(?:透露|表示)|权威数据显示"), "写出材料提供的明确来源;没有来源时删除模糊归因。"),
    (re.compile(r"(?:这一课只带走|这一课结束|这一课就结束)"), "课表腔;把眼前的问题解开,停在对方下一步能做的事。"),
    (re.compile(r"进行了[^。]{0,8}(?:优化|分析|调整|提升)|实现了[^。]{0,8}(?:优化|提升|增长)"), "名词化动词改回具体动作:谁做了什么,结果是什么。"),
    (re.compile(r"(?i)(?:In this article|Let's get started|You'?ve got this|Keep going|Bookmark this|Feel free to Star)"), "英文发布腔开场/收尾/号召,删除后直接进入内容。"),
)


def read_text(name: str) -> str:
    return sys.stdin.read() if name == "-" else Path(name).read_text(encoding="utf-8")


def visible_lines(text: str) -> list[tuple[int, str]]:
    """Strip fenced code, inline code, script/style, and HTML tags."""
    lines: list[tuple[int, str]] = []
    in_fence = False
    in_script = False
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.search(r"<(script|style)\b", raw, flags=re.IGNORECASE):
            in_script = True
        if in_script:
            if re.search(r"</(script|style)>", raw, flags=re.IGNORECASE):
                in_script = False
            continue
        without_tags = re.sub(r"<[^>]+>", " ", raw)
        without_code = re.sub(r"`[^`]*`", " ", without_tags)
        visible = html.unescape(re.sub(r"\s+", " ", without_code)).strip()
        if visible:
            lines.append((number, visible))
    return lines


def find_matches(text: str, rules: tuple[Rule, ...]) -> list[tuple[int, str, str]]:
    matches: list[tuple[int, str, str]] = []
    for line_number, line in visible_lines(text):
        for pattern, fix in rules:
            if pattern.search(line):
                matches.append((line_number, line, fix))
    return matches


def find_failures(text: str) -> list[tuple[int, str, str]]:
    return find_matches(text, RULES)


def find_warnings(text: str) -> list[tuple[int, str, str]]:
    return find_matches(text, WARNING_RULES)


def find_structural(text: str) -> list[tuple[int, str, str]]:
    """Whole-document structure checks: short-sentence drumming, question
    flooding, bold-as-crutch. Advisory only; prose paragraphs, not lists."""
    matches: list[tuple[int, str, str]] = []
    entries: list[tuple[int, str]] = []
    in_fence = False
    for number, raw in enumerate(text.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not stripped:
            continue
        if re.match(r"(?:[-*+]|\d+[.)])\s", stripped) or stripped.startswith(("|", ">", "#", "!")):
            continue
        content = re.sub(r"`[^`]*`", " ", stripped)
        content = re.sub(r"\s+", " ", html.unescape(content)).strip()
        if content:
            entries.append((number, content))
    run: list[tuple[int, str]] = []
    for number, line in entries:
        if len(line) <= 12:
            run.append((number, line))
            continue
        if len(run) >= 3:
            matches.append((run[0][0], run[0][1], "连续单句段落是在用短句造气势;把判断合并回有主语的段落。"))
        run = []
    if len(run) >= 3:
        matches.append((run[0][0], run[0][1], "连续单句段落是在用短句造气势;把判断合并回有主语的段落。"))
    question_marks = sum(line.count("？") + line.count("?") for _, line in entries)
    if question_marks > 10:
        first = entries[0][0] if entries else 1
        matches.append((first, "全篇设问偏多", f"全文出现 {question_marks} 个问号;确认每个问句承担过渡作用,口播稿可放宽。"))
    bold_count = 0
    bold_line = 1
    for number, line in entries:
        count = len(re.findall(r"\*\*[^*\n]{1,60}\*\*", line))
        if count and not bold_count:
            bold_line = number
        bold_count += count
    if bold_count > 5:
        matches.append((bold_line, "加粗偏多", f"全文加粗 {bold_count} 处;加粗要真承重,超过五处多半在拿加粗当拐棍。"))
    return matches


def self_test() -> int:
    bad = "\n".join((
        "说白了,这个方案更稳。",
        "值得注意的是,接口已发布。",
        "核心问题是:如何扩展。",
        "真正重要的是,我们理解了边界。",
        "产品升级完成,未来可期。",
        "当然可以!这是一个好问题。",
        "专家认为这种方案更可靠。",
        "这套系统赋能了开发团队。",
        "在当今快速变化的时代下,团队要保持敏捷。",
        "这标志着产品迈出了重要一步。",
        "先说结论,这个能用。",
        "总而言之,值得尝试。",
        "我们要讲清楚底层逻辑。",
        "团队齐心协力完成了上线。",
        "这次升级具有里程碑式意义。",
        "下面是说人话版本。",
        "用组合拳破局,打通全链路。",
        "产品完成升级,让我们拭目以待。",
    ))
    good = "\n".join((
        "接口在 2025 年 3 月升级后,旧客户端无法登录。",
        "方案更稳,因为依赖更少。",
        "问题在环境识别,不是 Shell。",
        "产品支持批量处理和离线模式。",
        "这项政策可能影响结果。",
        "检查了三个文件:settings.json、CLAUDE.md、AGENTS.md。",
        "如果接口确实返回 404,再看缓存。",
        "结论是保留 A,删除 B。",
    ))
    warning_bad = "\n".join((
        "随着人工智能技术的不断发展,工具越来越多。",
        "这项政策可能在一定程度上或许会影响结果。",
        "此外,还需要检查日志。",
        "这意味着该功能已经完成。",
        "先把流程搞顺再上线。",
        "让模型跑测试。",
        "把提示词喂给子 Agent。",
        "本次优化显著提升了构建速度。",
        "它是团队永不疲倦的秘书。",
        "从效率到体验都很好。",
        "这不仅是一次升级,更是全新开始。",
        "这不是固定流程,而是一套会根据情况变化的方法。",
        "这项改动进一步彰显了产品价值。",
        "尽管面临诸多挑战,团队未来仍将继续前进。",
        "这次更新为后续增长奠定了坚实的基础。",
        "学会这套方法,你的水平会有质的飞跃。",
        "点个关注,关注不迷路。",
        "以上就是本期分享,建议收藏。",
        "今年取得了亮眼成绩。",
        "以上建议仅供参考。",
        "据了解,接口将在下周关闭。",
        "这一课结束。",
        "我们对接口进行了优化,实现了提升。",
        "In this article we compare three tools.",
        "Let's get started with the setup.",
        "You've got this.",
        "Bookmark this for later.",
    ))
    # No warning_good assertion: WARN rules intentionally over-trigger and
    # rely on human/model judgment. Good prose is only asserted against FAIL
    # and structural rules.
    structural_bad = "\n".join((
        "这不是运气。",
        "这是选择。",
        "这也是纪律。",
        "那为什么工具越强,翻车的方式越花?",
        "为什么名册越肥,真正被点名的越少?",
        "为什么配置越全,缝隙反而越显眼?",
        "为什么补丁越打,问题换个地方又回来?",
        "为什么文档越写越厚,答案越来越难找?",
        "为什么演示很顺,落地就散架?",
        "为什么团队越大,上线反而越慢?",
        "为什么评审越多,低级错误越漏?",
        "为什么指标越全,方向感越差?",
        "为什么教程越写越长,能跟着走完的越少?",
        "为什么盘点越做越勤,判断反而越少?",
        "**这一句是全文第一处加粗的金句。**",
        "**这一句是全文第二处加粗的金句。**",
        "**这一句是全文第三处加粗的金句。**",
        "**这一句是全文第四处加粗的金句。**",
        "**这一句是全文第五处加粗的金句。**",
        "**这一句是全文第六处加粗的金句。**",
    ))
    structural_good = "\n".join((
        "接口升级后,旧版客户端无法继续登录,需要清理本地缓存才能恢复。",
        "它帮我把两个开源项目交叉的顽固 bug 跑通了,纯文本模型跑了将近一个小时。",
        "下面把这次排查中确认过的配置和验证步骤摊开讲一遍,方便直接照做。",
    ))
    failures = find_failures(bad)
    warnings = find_warnings(warning_bad)
    structural_failures = find_structural(structural_bad)
    failure_lines = {n for n, _, _ in failures}
    warning_lines = {n for n, _, _ in warnings}
    # FAIL rules must catch every bad line and never fire on good prose.
    # WARN rules must catch every bad line; they may legitimately fire on good
    # prose because WARN exists to ask for human judgment, not to assert guilt.
    # Structural checks must flag exactly the three engineered problems.
    if (
        failure_lines != set(range(1, len(bad.splitlines()) + 1))
        or find_failures(good)
        or warning_lines != set(range(1, len(warning_bad.splitlines()) + 1))
        or len(structural_failures) != 3
        or find_structural(structural_good)
    ):
        print("FAIL  tone_check self-test")
        for f in failures:
            print(f"      fail-miss: {f}")
        for w in warnings:
            print(f"      warn-miss: {w}")
        for s in structural_failures:
            print(f"      struct: {s}")
        return 1
    print("PASS  tone_check self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check copy for known humanizer-tone issues.")
    parser.add_argument("files", nargs="*", help="UTF-8 files to scan, or - for stdin")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.files:
        parser.error("provide one or more files, or use --self-test")
    failed = False
    warned = False
    for name in args.files:
        content = read_text(name)
        for line_number, line, fix in find_failures(content):
            print(f"FAIL  {name}:{line_number}: {line}\n      {fix}")
            failed = True
        for line_number, line, fix in find_warnings(content):
            print(f"WARN  {name}:{line_number}: {line}\n      {fix}")
            warned = True
        for line_number, line, fix in find_structural(content):
            print(f"STRUCT  {name}:{line_number}: {line}\n      {fix}")
            warned = True
    if not failed and not warned:
        print("PASS  no known humanizer-tone failures")
    elif not failed:
        print("PASS  no confirmed failures; review warnings")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
