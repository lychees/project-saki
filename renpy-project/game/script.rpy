# -*- coding: utf-8 -*-
# 主入口 + 章节选择枢纽（对应原作场景 10《选剧本》、12《暑期集训篇》、
# 13《回忆碎片》、14《Week1》、18《Week2》菜单场景）

label start:
    scene black
    stop music
    jump s1  # 序章《海棠无香》
    return


# ---- 章节选择（原作场景 10：选剧本） ----
label chapter_select:
    scene black with dissolve
    if main_story_done and not todo_card_shown:
        $ todo_card_shown = True
        centered "{size=24}暑期集训篇 Week-1 的主线剧情到此为止。\n原作是未完成的 Demo，Day 6 之后的章节尚未实装。\n你仍可以在章节选择中体验「回忆碎片」支线剧情。{/size}{w=3.5}{nw}"
    menu:
        "暑期集训篇":
            jump camp_menu
        "开学篇（原作未实装）":
            jump stub_26
        "回忆碎片":
            jump memory_menu


# ---- 暑期集训篇（原作场景 12） ----
label camp_menu:
    scene black with dissolve
    menu:
        "Day 0":
            jump s27
        "Week1":
            jump week1_menu
        "Week2":
            jump week2_menu
        "返回章节选择":
            jump chapter_select


# ---- Week1（原作场景 14） ----
label week1_menu:
    scene black with dissolve
    menu:
        "Day 1 数据结构-1":
            jump s2
        "Day 2 动态规划":
            jump s7
        "Day 3 状态空间搜索-1":
            jump s8
        "Day 4 状态空间搜索-2":
            jump s11
        "Day 5 数据结构-2":
            jump s15
        "Day 6 多校-1（原作未实装）":
            jump stub_16
        "Day 7 休息日（原作未实装）":
            jump stub_17
        "返回":
            jump camp_menu


# ---- Week2（原作场景 18，整周未实装） ----
label week2_menu:
    scene black with dissolve
    menu:
        "Day 1 图论-1（原作未实装）":
            jump stub_19
        "Day 2 图论-2（原作未实装）":
            jump stub_20
        "Day 3 数论-1（原作未实装）":
            jump stub_21
        "Day 4 字符串-1（原作未实装）":
            jump stub_22
        "Day 5 计算几何-1（原作未实装）":
            jump stub_23
        "Day 6 比賽（原作未实装）":
            jump stub_24
        "Day 7 休息日（原作未实装）":
            jump stub_25
        "返回":
            jump camp_menu


# ---- 回忆碎片（原作场景 13） ----
label memory_menu:
    scene black with dissolve
    menu:
        "生日礼物":
            jump s28
        "与父亲的冲突-1":
            jump s9
        "地外生命和宇宙人":
            jump s4
        "自由意志":
            jump s5
        "网络流篇-1":
            jump s6
        "冲突 - 褪色奖状":
            jump s29
        "生成函数篇":
            jump s31
        "返回章节选择":
            jump chapter_select


# ---- 未实装章节提示卡 ----
# 原作中 Day6/7 与 Week2 仅有一张章节标题卡（含教室背景与打字机音效），
# 开学篇为空场景。重制版在标题卡后追加未实装提示，不续写剧情。

label stub_16:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-1 Day-6{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_17:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-1 Day-7{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_19:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-2 Day-1{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_20:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-2 Day-2{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_21:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-2 Day-3{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_22:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-2 Day-4{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_23:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-2 Day-5{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_24:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-2 Day-6{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_25:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-2 Day-7{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_26:
    scene black with dissolve
    centered "{size=36}开学篇{/size}{w=1.0}{nw}"
    jump stub_todo

label stub_todo:
    centered "{size=22}—— 原作的剧情到此为止，敬请期待（本重制版不续写未实装内容）——{/size}{w=2.5}{nw}"
    jump chapter_select
