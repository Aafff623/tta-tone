# 对话调味

对话收束可以从这里抽一条**现成的**颜文字 + emoji 混排。不要手搓 `(・ω・) ✨` 这类输入法里见惯的组合。旧规范里「全程融入、自己拼组合、输入法常见脸」作废。

读者成稿不加。风险、密钥、FAIL、标识清点、commit 说明、卡住停手不加。

编程工具对话的外壳（横式 `now` / `before` 表 + 引文框碎碎念和对话摘要）写在 [modes.md](modes.md)「对话收尾」。调味是外壳之外偶尔一处，不是把表情填进表格。

## 什么时候加

只用于对话里的讲授、答问、维护回复。一则最多一处，放在收束。事实句、路径、命令、风险清单里不插。

连续几则里最多一则带。上一则已经调过，这一则默认不加。

下面任一成立，直接不加，不要为了调味去找情绪：

- 这一则是读者成稿（博客、演讲、PPT、网站、简介、README、SKILL、commit、PR）
- 这一则在报风险、密钥、FAIL、标识残留、提交说明
- 这一则是失败停手、两次工具失败后的换方法
- 连续上一则已经贴过调味

## 先认这一则，再抽

调味不是装饰，是收束时对**这一则处境**的一次点到。识别看两件事：任务结果，用户这轮的口气。不要表演情绪，也不要把用户没有的心情写进正文。

| 这一则实际发生了什么 | 场景 | `--scene` |
| --- | --- | --- |
| 事情做完，对方下一步是去看、去用 | 办妥 | `done` |
| 做完或做到一半，还要标未做项、小坑、注意点 | 点出小坑 | `peek` |
| 材料不够、判断没落地、只把问题摊开 | 还在想 | `think` |
| 结果和文档、预期、上一则说法不一致 | 意外 | `surprise` |
| 本轮收住、先这样、暂时停 | 到此为止 | `tea` |
| 明确轮到对方看、标、刷新，这一则不再改 | 交给对方 | `wait` |
| 收下指令或名单，下一则才干活 | 记下了 | `ack` |
| 任务本身是挑样子、看陈列、轻松维护 | 轻松收束 | `play` |

同一则只落一个场景。办完又带剩余风险，走 `peek`，不走 `done`。只记下名单、还没动手，走 `ack`，不要连续两则都 `ack`。`play` 不用在讲授主课、答问结论和任何禁区。

场景里的字，是 TTA 按工作区对话编的路由，不是把 kaomojikan 的日文标签原样拿来当分类。完整 slug 在 [data/season-catalog.json](data/season-catalog.json)。

## 怎么抽

```bash
python <tta-tone Skill 目录>/scripts/season.py --scene peek
```

本会话已经贴过的混排，再抽时全部排除：

```bash
python <tta-tone Skill 目录>/scripts/season.py --scene tea --exclude "(´∀`)b👍" --exclude "|ω・)👁"
```

`--exclude` 可以是混排原文，也可以是 `emoji-0087` 这种 slug。`--mood` 是 `--scene` 的旧名字，效果相同。

把 stdout 原样贴上。不要改符号，不要再拼一个 emoji。

## 随意性

同一会话里，同一条混排只用一次。不要一则里出现两处，也不要隔两则再贴同一条。

脚本在指定场景的池子里随机抽。池子被 `--exclude` 抽空时，才向邻近场景借（`done` 借 `ack`/`tea`，`peek` 借 `think`/`wait`，以此类推），仍然避开已经用过的。邻近也空了，这一则不加，不要退回输入法常见脸，也不要自己拼。

查看某个场景现在有哪些字：

```bash
python <tta-tone Skill 目录>/scripts/season.py --scene done --list
```

自检：

```bash
python <tta-tone Skill 目录>/scripts/season.py --self-test
```

## 默认池进什么、不进什么

进默认路由的，是用户三轮筛选之后仍留下的 絵文字ミックス，再按上面的场景收了一遍。约 47 条。

剩下仍在陈列里、但不进默认路由的，记在 catalog 的 `idle` 里，原因是和这个工作区的收束不匹配：

- 发火、砸东西、过劳脸
- 撒娇、心跳、号泣
- 猛烈惊吓（爆炸、仰天）
- 安慰拍头、纪念日式庆祝
- 输入法里见惯的圆脸
- 动物脸只走 `play`，不进 `done` / `peek`

陈列里的纯颜（egao / copype / kirakira）先不进默认池。默认只抽已经拼好的混排，避免再把手搓组合做回来。

## 这些字从哪来

中文输入法里的颜文字包，几乎都不自己发明。常见灌入路径：

1. 日本颜文字辞典和站点：`みんなの顔文字辞典`、[顔文字屋](https://www.kaomojiya.org/)、[kaomoji.ru](https://kaomoji.ru/)、2channel / 5channel / A岛匿名版的 AA 和颜文字。
2. 搜狗细胞词库页（`pinyin.sogou.com/dict/ywz`）把上面的符号打成「哈哈 / 啦啦」可触发的词。百度、微信输入法走同一条路：内置一份，再加表情商店。
3. 开源输入法侧有人把这些源再编成词库，例如 [aoguai/rime_kaomoji_dict](https://github.com/aoguai/rime_kaomoji_dict)（搜狗颜文字 + A岛 + 拉米工具 + 贴吧 Temreg）。
4. emoji 半边走 Unicode：[CLDR annotations](https://github.com/unicode-org/cldr-json)、[github/gemoji](https://github.com/github/gemoji)。图形实现另有 Noto Emoji、Twemoji，那是字体，不是字表。

「颜文字和 emoji 已经拼好」的开源库，是 [kaomojikan/kaomoji-data](https://github.com/kaomojikan/kaomoji-data) 的 `emoji` 类（絵文字ミックス，177 条，MIT）。本 Skill 用的是这一份的快照。用户淘汰的 slug 不进 `season-catalog.json` 的场景表。

更大的纯颜文字库（需要时再扩，不要默认加载）：

- [kaomojiya-collection](https://github.com/kaomojiya-collection/kaomoji-collection)：4 万+ 条，535 类，MIT
- [ekohrt/emoticon_kaomoji_dataset](https://github.com/ekohrt/emoticon_kaomoji_dataset)：6.2 万条带标签，多站抓取
