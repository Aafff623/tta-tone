#!/usr/bin/env python3
"""Report tta-tone failures and context-sensitive warnings in Chinese copy."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


Rule = tuple[re.Pattern[str], str]

RULES: tuple[Rule, ...] = (
    (re.compile(r"(?:赋能|撬动|抓手|闭环|破局|组合拳|全链路|沉淀价值|价值落地)"), "删除宣传黑话，直接说明具体作用。"),
    (re.compile(r"原因很简单[：:，,。]?"), "删除模板化领起语，直接说明具体原因。"),
    (re.compile(r"(?:真正重要的是|真正的关键是|这不仅仅?是|从更大的角度看)"), "删除没有增加信息的总结或升华表达。"),
    (re.compile(r"任务.{0,12}停在[“\"]?代码已经写出来"), "直接说明 Codex 写完代码后继续执行哪些检查。"),
    (re.compile(r"综上所述|总而言之"), "删除模板化领起语，直接说明已经确认的结果或下一步。"),
    (re.compile(r"具有(?:深远|划时代|里程碑式)的?(?:历史)?意义|谱写了.{0,20}新华章"), "改为材料已经确认的动作、变化或结果。"),
    (re.compile(r"(?:底层逻辑|顶层设计|新质生产力|降本增效|提质增效|数智化)"), "删除宣传黑话，直接说明具体作用。"),
    (re.compile(r"齐心协力|攻坚克难|砥砺前行|再创辉煌"), "删除没有增加信息的官腔，直接说明具体动作或结果。"),
    (re.compile(r"说人话版本?"), "公开稿不要用「说人话版本」当标签或节名。"),
    (re.compile(r"我踩过的坑"), "公开稿不要用「我踩过的坑」当标题或标签。"),
)

WARNING_RULES: tuple[Rule, ...] = (
    (re.compile(r"(?:在当今|在当前).{0,16}(?:时代|背景|环境)下"), "确认这段背景是否提供了必要信息，否则直接进入具体内容。"),
    (re.compile(r"随着.{0,16}(?:不断|持续)(?:发展|演变|变化)"), "确认这段变化是否与后文存在具体关系。"),
    (re.compile(r"(?:值得注意的是|值得一提的是|需要指出的是|毋庸置疑|不可否认的是?)"), "删除没有承担限定或转折作用的固定领起语。"),
    (re.compile(r"(?:标志着|代表着).{0,24}(?:重要|关键)(?:一步|时刻|转折点)"), "改为材料已经确认的动作、变化或结果。"),
    (re.compile(r"为.{1,24}奠定(?:了)?(?:坚实的?)?基础"), "说明具体产生了什么后续条件或结果。"),
    (re.compile(r"(?:彰显|凸显|体现)(?:了)?.{0,20}(?:重要性|意义|价值)"), "确认重要性判断是否有材料支持。"),
    (re.compile(r"(?:业内|行业|专家|观察者)(?:普遍)?(?:认为|指出|表示)"), "写出材料提供的明确来源；没有来源时删除模糊归因。"),
    (re.compile(r"(?:很多|不少|部分)用户(?:认为|指出|表示|反馈)"), "确认用户判断或反馈是否有明确材料依据。"),
    (re.compile(r"(?:有|相关|多项|大量)研究(?:均)?(?:表明|显示|指出)"), "写出材料提供的研究来源；不能自行补充来源。"),
    (re.compile(r"(?:从而确保|进而体现|进一步彰显|反映了更深层次)"), "确认尾句是否有真实因果或材料依据。"),
    (re.compile(r"尽管.{0,24}(?:挑战|困难).{0,24}(?:仍|依然|未来)|机遇与挑战并存|挑战中蕴含机遇"), "直接说明已经确认的限制、结果或后续安排。"),
    (re.compile(r"(?:未来可期|迈出(?:了)?(?:至关重要|重要|关键)的一步|开启(?:了)?(?:全新|新的?)篇章)|让我们拭目以待|前景广阔|充满无限可能|大有可为"), "删除通用乐观结尾，说明具体结果或下一步。"),
    (re.compile(r"(?:当然可以|这是一个(?:非常|很)?好的问题|你说得(?:完全)?正确|希望这对(?:你|您)有帮助|如需更多(?:信息|帮助).{0,8}(?:请)?(?:随时)?(?:告诉我|联系我)|针对您的问题|以下是关于.{0,24}的(?:介绍|分析|回答|说明))"), "删除读者成稿中的聊天残留或讨好表达。"),
    (re.compile(r"(?:建议收藏|点个收藏|点个关注|以上就是本期分享|让我们开始吧|关注不迷路|一键三连|质的飞跃)"), "删除读者成稿中的发布腔、营销号召或飞跃式收尾，直接进入问题或下一步。"),
    (re.compile(r"(?:亮眼成绩|蓬勃发展|欣欣向荣|硕果累累|如火如荼)"), "改为材料已经确认的动作、数量或结果；没有材料时删除软文形容词。"),
    (re.compile(r"仅供参考|不当之处敬请指正|抛砖引玉|以上只是个人浅见"), "保护句写清哪一句没写死，不要用客套代替判断。"),
    (re.compile(r"据了解|相关人士(?:透露|表示)|权威数据显示"), "写出材料提供的明确来源；没有来源时删除模糊归因。"),
    (re.compile(r"(?:这一课只带走|这一课结束|这一课就结束)"), "讲授不要写成开课通知，先把眼前的问题解开。"),
    (re.compile(r"不是.{2,24}而是"), "少用「不是……而是……」堆砌；能正面说就正面说。纠正误解时最多自然用一次。"),
    (re.compile(r"(?i)(?:In this article|Let's get started)"), "删除英文发布腔开场，直接进入内容。"),
    (re.compile(r"(?i)(?:You've got this|Keep going)"), "删除没有新信息的英文加油收尾。"),
    (re.compile(r"(?i)(?:Bookmark this|Feel free to Star)"), "删除英文发布腔号召或 Star 号召。"),
    (re.compile(r"(?:可能|或许|也许|在一定程度上|在某种程度上).{0,8}(?:可能|或许|也许|在一定程度上|在某种程度上)"), "合并重复限定，保留一个符合事实状态的说法。"),
    (re.compile(r"进行了.{0,8}(?:优化|分析|调整|提升)|实现了.{0,8}(?:优化|提升|增长)"), "名词化动词改回具体动作：谁做了什么，结果是什么。"),
)


def read_text(name: str) -> str:
    return sys.stdin.read() if name == "-" else Path(name).read_text(encoding="utf-8")


def visible_lines(text: str) -> list[tuple[int, str]]:
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
            matches.append((run[0][0], run[0][1], "连续单句段落是在用短句造气势；把判断合并回有主语的段落。"))
        run = []
    if len(run) >= 3:
        matches.append((run[0][0], run[0][1], "连续单句段落是在用短句造气势；把判断合并回有主语的段落。"))
    question_marks = sum(line.count("？") + line.count("?") for _, line in entries)
    if question_marks > 10:
        first = entries[0][0] if entries else 1
        matches.append((first, "全篇设问偏多", f"全文出现 {question_marks} 个问号；确认每个问句承担过渡作用，口播稿可放宽。"))
    bold_count = 0
    bold_line = 1
    for number, line in entries:
        count = len(re.findall(r"\*\*[^*\n]{1,60}\*\*", line))
        if count and not bold_count:
            bold_line = number
        bold_count += count
    if bold_count > 5:
        matches.append((bold_line, "加粗偏多", f"全文加粗 {bold_count} 处；加粗要真承重，超过五处多半在拿加粗当拐棍（人格稿金句可放宽）。"))
    return matches


def self_test() -> int:
    bad = "\n".join((
        "这套方案可以赋能开发团队。",
        "原因很简单：它读取了错误的文件。",
        "真正重要的是，我们理解了工具的边界。",
        "任务不必停在“代码已经写出来”。",
        "综上所述，项目已经完成。",
        "这项改动具有里程碑式意义。",
        "我们要讲清楚底层逻辑。",
        "团队齐心协力完成了上线。",
        "下面是说人话版本。",
        "第三节：我踩过的坑。",
        "用组合拳破局，打通全链路。",
    ))
    good = "\n".join((
        "模型必须先遵循事实准确这项要求。",
        "先把这段流程搞顺，再让模型跑测试。",
        "子 Agent 直接吃下整段对话，把内容塞进提示词。",
        "那天晚上我还在旧池子里猛蹬，官方悄摸摸把正式版挂了出来。",
        "Explorer 把查到的调用和配置说明清楚。",
        "查看调用和配置，确认当前实现。",
        "这个功能负责处理需求。",
        "这套方法会根据情况变化，没有固定流程。",
        "使用 Codex 时，先说明任务；完成后，再查看改动。",
    ))
    warning_bad = "\n".join((
        "在当今快速变化的时代下，团队需要保持敏捷。",
        "随着人工智能技术的不断发展，工具越来越多。",
        "值得注意的是，这项功能已经发布。",
        "这标志着产品迈出了重要一步。",
        "这次更新为后续增长奠定了坚实的基础。",
        "这体现了自动化的重要性。",
        "业内普遍认为，这种方案更可靠。",
        "不少用户反馈，新的设计更自然。",
        "有研究表明，这种方法可以提高效率。",
        "这项改动进一步彰显了产品价值。",
        "尽管面临诸多挑战，团队未来仍将继续前进。",
        "产品完成升级，未来可期。",
        "希望这对你有帮助。",
        "以上就是本期分享，建议收藏。",
        "这一课结束。",
        "学会这套方法，你的水平会有质的飞跃。",
        "点个关注，关注不迷路。",
        "In this article we compare three tools.",
        "Let's get started with the setup.",
        "You've got this.",
        "Keep going.",
        "Bookmark this for later.",
        "Feel free to Star the repository.",
        "这项政策可能在一定程度上或许会影响结果。",
        "让我们拭目以待。",
        "今年取得了亮眼成绩。",
        "以下是关于登录接口的介绍。",
        "以上建议仅供参考。",
        "据了解，接口将在下周关闭。",
        "机遇与挑战并存。",
        "这不是固定流程，而是一套会根据情况变化的方法。",
        "我们对接口进行了优化，实现了提升。",
    ))
    warning_good = "\n".join((
        "2025 年 3 月接口升级后，旧版客户端无法继续登录。",
        "清华大学发布的报告显示，样本中的响应时间缩短了 12%。",
        "产品支持批量处理和离线模式。",
        "这项政策可能影响结果。",
    ))
    structural_bad = "\n".join((
        "这不是运气。",
        "这是选择。",
        "这也是纪律。",
        "那为什么工具越强，翻车的方式越花？",
        "为什么名册越肥，真正被点名的越少？",
        "为什么配置越全，缝隙反而越显眼？",
        "为什么补丁越打，问题换个地方又回来？",
        "为什么文档越写越厚，答案越来越难找？",
        "为什么演示很顺，落地就散架？",
        "为什么团队越大，上线反而越慢？",
        "为什么评审越多，低级错误越漏？",
        "为什么指标越全，方向感越差？",
        "为什么教程越写越长，能跟着走完的越少？",
        "为什么盘点越做越勤，判断反而越少？",
        "**这一句是全文第一处加粗的金句。**",
        "**这一句是全文第二处加粗的金句。**",
        "**这一句是全文第三处加粗的金句。**",
        "**这一句是全文第四处加粗的金句。**",
        "**这一句是全文第五处加粗的金句。**",
        "**这一句是全文第六处加粗的金句。**",
    ))
    structural_good = "\n".join((
        "那天晚上我还在旧池子里猛蹬，官方悄摸摸把正式版挂了出来。",
        "它帮我把两个开源项目交叉的顽固 bug 跑通了，纯文本模型跑了将近一个小时。",
        "那么各位小园丁，下面把我摸到的配置摊开揉碎讲一遍。",
    ))
    failures = find_failures(bad)
    warnings = find_warnings(warning_bad)
    structural_failures = find_structural(structural_bad)
    failure_lines = {line_number for line_number, _, _ in failures}
    warning_lines = {line_number for line_number, _, _ in warnings}
    if (
        failure_lines != set(range(1, len(bad.splitlines()) + 1))
        or find_failures(good)
        or warning_lines != set(range(1, len(warning_bad.splitlines()) + 1))
        or find_warnings(warning_good)
        or len(structural_failures) != 3
        or find_structural(structural_good)
    ):
        print("FAIL  tone lint self-test")
        for failure in failures:
            print(f"      {failure}")
        for warning in warnings:
            print(f"      {warning}")
        for structural in structural_failures:
            print(f"      {structural}")
        return 1
    print("PASS  tone lint self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Chinese copy for known tta-tone issues.")
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
            print(f"WARN  {name}:{line_number}: {line}\n      {fix}")
            warned = True
    if not failed and not warned:
        print("PASS  no known tta-tone failures")
    elif not failed:
        print("PASS  no confirmed tta-tone failures; review warnings")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
