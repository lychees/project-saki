# 天才算法少女 · Ren'Py 重制版

> **在线试玩（Web 版）**：https://lychees.github.io/project-saki/
> **仓库地址**：https://github.com/lychees/project-saki

OI / 信息学竞赛题材 galgame《天才算法少女》的 Ren'Py 重制工程。

- **原作**：GameCreator 平台作品《天才算法少女》，作者 **岛娘岛娘岛**
- **原作链接**：https://www.gamecreator.com.cn/work/det/316?reid=1553
- **重要事实**：**原作是未完成的 Demo**。主线剧情只实装到「暑期集训篇 Week1 Day 5」，
  Week1 Day 6/7 与 Week2 全部章节只有标题卡，「开学篇」是空场景，也没有实装结局。
  本重制版**忠实复刻原作已有内容，不续写任何未实装剧情**；
  未实装章节在游戏内以「原作到此为止，敬请期待」提示卡标注。

## 目录结构

```
saki/
├── original/               # 原作数据提取结果（重制依据）
│   ├── raw/                #   GameCreator 原始 JSON（startup.json 解包 + 场景/立绘数据）
│   ├── assets/             #   原作素材（bg/char/cg/bgm/se/ui 分类，138 个文件）
│   ├── script.md           #   提取的完整剧情文本（486 条对话、73 个选项）
│   ├── assets_manifest.md  #   素材清单及用途
│   └── notes.md            #   原作系统设定 / 数据格式笔记
├── renpy-project/          # Ren'Py 工程（本重制版）
│   └── game/
│       ├── script.rpy      #   入口 + 章节选择枢纽 + 未实装章节提示卡（手写）
│       ├── oj.rpy          #   真实 OJ 判题系统：挑战界面/轮询线程/用户名设置（手写）
│       ├── definitions.rpy #   角色 / 变量 / 声道定义（手写）
│       ├── gallery.rpy     #   CG 鉴赏界面（手写）
│       ├── dev.rpy         #   开发者模式：Shift+K 跳转菜单 + OJ 题目直通过渡 label（手写）
│       ├── scene_*.rpy     #   14 个剧情场景（由原作 JSON 自动生成）
│       ├── images.rpy      #   图像定义 + fullscreen/gcoffset transform
│       ├── tex_tag.rpy     #   {tex} LaTeX 内联公式标签（手写）
│       ├── tex_images.rpy  #   公式图像定义（tools/render_tex.py 生成）
│       ├── gui.rpy / screens.rpy / options.rpy  # GUI（基于 Ren'Py 默认模板修改）
│       ├── images/ audio/  #   素材（复制自 original/assets；images/tex/ 为公式渲染产物）
│       └── fonts/NotoSansCJKsc-Regular.otf      # 思源黑体（SIL OFL，可商用）
├── tools/render_tex.py     # LaTeX 公式离线渲染管线（matplotlib mathtext）
└── .tmp/                   # 提取/生成脚本、Ren'Py SDK、venv（不参与打包）
```

## 已实现章节（与原作一一对应）

| 章节 | 场景 label | 内容 |
|---|---|---|
| 序章《海棠无香》 | `s1` | Kotori 的独白，ICPCCamp 回忆 |
| Day 0 | `s27` | 前往哈尔滨的列车，OI 背景介绍 |
| 生日礼物（回忆） | `s28` | 幼年 Kotori 与父亲 |
| Week1 Day 1 数据结构-1 | `s2` | 栈；课堂选项；习题 POJ-3250 / POJ-2559 |
| Week1 Day 2 动态规划 | `s7` | DP；习题 POJ-2533 / POJ-1141 / 51Nod-1021 / HDU-1231 |
| Week1 Day 3 状态空间搜索-1 | `s8` | 搜索；习题 UVALive-2026 / LibreOJ-10027 |
| Week1 Day 4 状态空间搜索-2 | `s11` | sevenzero 授课；5 道习题 |
| Week1 Day 5 数据结构-2 | `s15` | 线段树；习题 SPOJ-GSS1 |
| 回忆碎片 ×6 | `s4` `s5` `s9` `s6` `s29` `s31` | 地外生命与宇宙人 / 自由意志 / 冲突 / 网络流篇-1 / 冲突-褪色奖状 / 生成函数 |
| 章节选择菜单 | `chapter_select` 等 | 对应原作场景 10/12/13/14/18 |
| 未实装提示卡 | `stub_*` | Day6/7、Week2 整周、开学篇 |

游戏流程：标题画面 → 开始游戏 → 序章 → Day 1 → … → Day 5 → 章节选择枢纽
（可进入 Day 0 / 生日礼物 / 回忆碎片支线 / 未实装章节提示卡）。

## 重制说明

- **做题系统（真实 OJ 提交验证）**：原作课堂习题通过 vjudge API 在线判题、聊天通过
  rct.ai 生成（后者已失效，聊天功能未重制）。重制版的判题使用**真实的 vjudge 状态
  API**（已验证可用）：选择题目后进入 OJ 挑战界面，需先在 vjudge.net 注册账号并
  在弹窗中填入用户名（存于 persistent，之后可在 设置界面 / 挑战界面 随时更换）；
  点击「打开题目页面」跳转到真实题目，**限时 30 分钟**（`oj.rpy` 中的常量
  `OJ_TIME_LIMIT`，可按需调整）内提交并获得 Accepted 才算通过——后台线程每约 12 秒
  轮询一次提交状态（只认挑战开始后新提交的 AC；若检测到你**历史已 AC** 该题，
  界面会提示并出现「我已通过」直通按钮）。超时或点「放弃挑战」进入未通过分支，
  可回到题目菜单重试；答过再选会显示原作提示
  「你已经完成这个题目了哦！去试试其他的题目吧。」，「打完收工」的嘲讽/夸奖分支
  按原作条件（本题组通过数是否为 0）实现。
  **注意：本功能需要联网**；断网或 API 异常时界面显示「网络异常，正在重试」，
  不会卡死，可正常存档/读档/放弃。
- **标记映射**：原作 `[pN]` 停顿标记 → Ren'Py `{w=N/20}`；`[@v2001]` 变量插值 →
  Ren'Py 变量 `[exam_group_solved]`；`<span>` 颜色标记（原作全为白色）已剥离。
- **立绘头像**：原作对话框内的 400×400 立绘头像以 Ren'Py side image 实现，
  表情差分（Kotori 长发/短发/害怕等、MoonMayCry 差分）按原作指令的表情编号切换。
- **演出简化**：原作的界面演出（手机/QQ/Gmail 界面）、滤镜材质、图像层运镜以注释或
  等效淡入淡出替代，剧情文本零删减。
- **CG 鉴赏**：CG#2「Week1Day1」可在 Day 1 剧情中解锁；CG#1 的原作图片在服务器上
  已不存在（404），以占位槽标注。
- 标题画面使用原作标题图（`Title_1 - 副本.png`）与标题 BGM（`Title.mp3`）。
- **场景背景/CG 全屏**：所有 `scene` 演出统一套用 `images.rpy` 中集中定义的
  `transform fullscreen: xysize (1200, 720)`（直接拉伸铺满窗口，不保持宽高比）；
  对话框内的 side image 立绘头像不受影响。

## 在剧本中内联 LaTeX 公式（{tex} 标签）

对话文本里可以用自定义标签 `{tex=...}` 内联显示数学公式（matplotlib mathtext
离线预渲染，**运行时不需要 LaTeX**）：

```renpy
kotori "（二项式定理 {tex=(a+b)^n = \\sum_｛k=0｝^｛n｝ \\binom｛n｝｛k｝ a^｛n-k｝ b^｛k｝} 嘛。）"
```

**书写规则（重要）**：

1. **反斜杠写两个**：`\\sum`、`\\binom`、`\\frac`。Ren'Py 对话字符串按 Python
   字符串处理转义（`\b` 会变成退格符），双反斜杠在运行时还原为一个。
2. **分组花括号用全角 ｛｝**（U+FF5B/FF5D）：`\\sum_｛k=0｝^｛n｝`、`\\frac｛n!｝｛k!(n-k)!｝`。
   Ren'Py 文本标签不支持嵌套 ASCII 花括号，管线与运行时都会自动把 ｛｝ 转成 {}。
3. 不需要分组的单字符上下标可直接写：`x^n`、`a_k`。
4. 语法为 matplotlib **mathtext 子集**（\\frac \\sqrt \\sum \\prod \\binom \\mathrm
   \\alpha…\\omega \\cdot \\infty \\leq \\neq 等常用命令可用；不支持完整 LaTeX 宏、
   矩阵环境、\\text 中文等）。整行注释（`#` 开头）里的 {tex} 会被忽略。

**改完剧本必须重新渲染**（需要 .tmp/venv 里的 matplotlib）：

```bash
.tmp/venv/Scripts/python.exe tools/render_tex.py
```

脚本扫描 `game/*.rpy`，把每个公式渲染成透明底白字 PNG 到
`game/images/tex/<md5前12位>.png`，并更新 `game/tex_images.rpy`。
新增/修改公式后跑一遍即可（已存在的 PNG 会跳过）；忘记渲染时游戏内显示红色
「公式未渲染」占位提示。演示见 scene_31.rpy（生成函数章节，母函数与二项式定理）。


## 开发者模式（章节任意跳转）

在「设置」界面开启 **开发者模式**（状态存 `persistent.dev_mode`，即时生效）后：

- 游戏内任意时刻按 **Shift+K** 呼出「开发者跳转」菜单（该键未被 Ren'Py 默认快捷键占用）；
- 标题主菜单导航栏也会出现「开发者跳转」入口按钮。

跳转菜单按组列出（跳转前有 confirm 确认）：

- **主线**：序章《海棠无香》、Day 0、生日礼物、Week1 Day 1~5 各场景入口；
- **回忆碎片**：6 条支线各自入口；
- **OJ 题目直通**：16 道题各自的 `dev_sN_qK` 入口 label（复用对应场景的
  `sN_ac_K`/`sN_fail_K`，便于独立测试判题流程，通过后落回该题组菜单）；
- **系统**：章节选择菜单、未实装提示卡示例。

实现说明：菜单从主菜单进入时用 `Start(label)`（退出主菜单上下文，否则 overlay/
快捷菜单会被抑制——这是调试中发现的 Ren'Py 上下文坑），游戏内进入用 `Jump`；
快捷键由 `config.overlay_screens` 中的 `dev_hotkey` 屏幕监听，关闭开发者模式后
入口与快捷键同时失效。跳转所需变量（`exam_group_solved`、`exam_done`、
`persistent.vjudge_user` 等）均有 default 覆盖，OJ 入口 label 会重置题组计数。

## 运行方式

1. 下载 Ren'Py SDK 8.5+（本工程已用 8.5.3 验证，位于 `.tmp/renpy-sdk/renpy-8.5.3-sdk/`）。
2. 启动 `renpy.exe`（Windows）/ `renpy.sh`（macOS/Linux），在启动器中
   「添加工程」选择 `renpy-project/` 目录，点击「启动工程」。
3. 命令行检查：`renpy.exe <本目录>/renpy-project lint`（当前 0 错误；
   仅有 26 条「素材文件名含非 ASCII 字符」提示，桌面端运行无影响）。

## 竞技场模式（Arena）

主菜单「竞技场」入口（开发者跳转菜单里也有直通入口）。玩法：

- 开局前设置**题数 n**（默认 5，1~10 可调）与**总时限**（默认 90 分钟，
  30/60/90/120 可调），桌面版沿用 vjudge 用户名自动判题
- **抽题机制**：桌面版开局时实时抓取 vjudge 全站最近提交流
  （`status/data?start=0/20/50/100`，深分页已被官方限制，可用窗口约 120 条），
  过滤 Accepted、按 (OJ, 题号) 去重，得到近期有真人 AC 的题池后随机抽 n 道；
  抓取失败或去重题数不足时回退到内置题池 `game/arena_pool.json`
  （可随时运行 `python tools/harvest_pool.py` 刷新，当前内置 32 道）
- **判题**（桌面版）：后台线程每约 15 秒轮询该用户最近提交，挑战开始后
  新提交的 Accepted 才算（**历史 AC 不计**，已 AC 过的题需重新提交）；
  断网显示「网络异常，重试中」，可正常存档/读档（读档后按原 deadline 恢复）
- **结算**：全部 AC → 胜利结算（总用时 + OI 风格评价）；超时/放弃 →
  战绩 x/n + 未过题清单
- **Web 版降级**：无网络栈，使用内置题池抽题、不轮询，每题旁提供
  「标记通过」手动按钮，其余流程一致

## 打包发布

启动器中选择「生成分发版」即可打包 Windows/Mac/Linux 版。
素材文件名已全部 ASCII 化（tools/ascii_rename.py 一次性完成并重写引用），
Web/桌面构建均可直接使用。

### Web 版（GitHub Pages）

`docs/` 目录是 Ren'Py Web 构建产物（`renpy.exe launcher web_build renpy-project
--destination docs`，需 SDK 的 web 支持组件），通过 GitHub Pages
（main 分支 /docs）发布到 https://lychees.github.io/project-saki/ 。

**Web 版与桌面版的差异**：

- **OJ 判题降级**：Web 平台（Pyodide/Emscripten）没有 `_ssl`/网络栈，也无法
  可靠运行后台线程，桌面专用的 ssl/urllib/threading/certifi 代码已按平台
  条件导入隔离（Web 完全不加载）。`oj_challenge` 在 Web 上自动降级为
  **手动确认模式**——轮询不启动，挑战界面始终显示「我已通过」按钮，
  玩家在 vjudge 提交通过后手动点击继续（桌面版仍为自动轮询判题）。
  倒计时与放弃分支两端一致。
- 存档保存在浏览器 IndexedDB 中，与桌面版存档不互通。
- 首次加载需下载约 50MB（game.zip），请耐心等待。

## 版权说明

- 剧情文本与素材版权归原作者 **岛娘岛娘岛** 所有，本工程仅作学习/ preservation 用途。
- 中文字体 Noto Sans CJK SC 采用 SIL Open Font License 1.1。
- Ren'Py 引擎遵循其自身许可（含 LGPL 组件）。
