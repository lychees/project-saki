# -*- coding: utf-8 -*-
# 开发者模式：设置界面开启 persistent.dev_mode 后，
#   - 游戏内按 Shift+K 呼出「开发者跳转」菜单（overlay 屏幕监听按键）
#   - 标题主菜单导航栏出现「开发者跳转」按钮
# 跳转均为 jump（非 call），不污染场景调用栈。

init python:
    config.overlay_screens.append("dev_hotkey")

    # (分组名, [(显示名, 目标 label), ...])
    DEV_GROUPS = [
        ("主线", [
            ("序章《海棠无香》", "s1"),
            ("Day 0", "s27"),
            ("生日礼物", "s28"),
            ("Week1 Day 1 数据结构-1", "s2"),
            ("Week1 Day 2 动态规划", "s7"),
            ("Week1 Day 3 状态空间搜索-1", "s8"),
            ("Week1 Day 4 状态空间搜索-2", "s11"),
            ("Week1 Day 5 数据结构-2", "s15"),
        ]),
        ("回忆碎片", [
            ("地外生命与宇宙人", "s4"),
            ("自由意志", "s5"),
            ("冲突", "s9"),
            ("网络流篇-1", "s6"),
            ("冲突 - 褪色奖状", "s29"),
            ("生成函数", "s31"),
        ]),
        ("OJ 题目直通（测试判题流程）", [
            ("Day1 · POJ-3250", "dev_s2_q1"),
            ("Day1 · POJ-2559", "dev_s2_q2"),
            ("Day2 · POJ-1141", "dev_s7_q1"),
            ("Day2 · POJ-2533", "dev_s7_q2"),
            ("Day2 · 51Nod-1021", "dev_s7_q3"),
            ("Day2 · HDU-1231", "dev_s7_q4"),
            ("Day3 · UVALive-2026", "dev_s8_q1"),
            ("Day3 · LibreOJ-10027", "dev_s8_q2"),
            ("Day4 · 51Nod-2067", "dev_s11_q1"),
            ("Day4 · POJ-1077", "dev_s11_q2"),
            ("Day4 · POJ-1101", "dev_s11_q3"),
            ("Day4 · POJ-1455", "dev_s11_q4"),
            ("Day4 · POJ-1324", "dev_s11_q5"),
            ("Day5 · SPOJ-GSS1", "dev_s15_q1"),
            ("网络流 · ZOJ-2587", "dev_s6_q1"),
            ("网络流 · POJ-3469", "dev_s6_q2"),
        ]),
        ("系统", [
            ("章节选择菜单", "chapter_select"),
            ("未实装提示卡示例（Week-1 Day-6）", "stub_16"),
            ("竞技场模式", "arena_setup"),
        ]),
    ]


# 游戏内快捷键（仅开发者模式生效；shift_K_k 未被 Ren'Py 默认快捷键占用）
screen dev_hotkey():
    if persistent.dev_mode:
        key "shift_K_k" action Show("dev_jump")


# 开发者跳转菜单
screen dev_jump():
    modal True
    zorder 300

    add Solid("#000c")

    frame:
        align (0.5, 0.5)
        xsize 1060
        padding (36, 28)

        vbox:
            spacing 10

            hbox:
                text "开发者跳转" size 30
                null width 30
                textbutton "关闭" action Hide("dev_jump") text_size 20 yalign 0.5

            viewport:
                ysize 520
                scrollbars "vertical"
                mousewheel True

                vbox:
                    spacing 14

                    for gname, items in DEV_GROUPS:
                        text gname size 22 color "#ffcc66"
                        $ _rows = (len(items) + 3) // 4
                        grid 4 _rows:
                            spacing 8
                            for name, target in items:
                                # 先 Hide 本菜单（modal 会挡住 confirm），确认后跳转；
                                # 主菜单上下文必须用 Start（退出主菜单上下文），游戏内用 jump。
                                textbutton name:
                                    text_size 17
                                    action [
                                        Hide("dev_jump"),
                                        Confirm(
                                            "确认跳转到「" + name + "」？（jump，无返回）",
                                            yes=(Start(target) if main_menu else Jump(target))),
                                    ]
                            # 补齐 grid 空位
                            for _ in range(4 * _rows - len(items)):
                                null


# ---- OJ 题目直通的入口 label（复用各场景的 ac/fail label，不改变剧情）----
# 通过判题后会落回对应场景的题目菜单（sN_ac_K -> 题目循环 label），
# 未通过同理（sN_fail_K），便于完整测试判题流程。

label dev_s2_q1:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "3250", OJ_TIME_LIMIT, "s2_ac_0", "s2_fail_0")

label dev_s2_q2:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "2559", OJ_TIME_LIMIT, "s2_ac_1", "s2_fail_1")

label dev_s6_q1:
    $ exam_group_solved = 0
    call oj_challenge("ZOJ", "2587", OJ_TIME_LIMIT, "s6_ac_0", "s6_fail_0")

label dev_s6_q2:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "3469", OJ_TIME_LIMIT, "s6_ac_1", "s6_fail_1")

label dev_s7_q1:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "1141", OJ_TIME_LIMIT, "s7_ac_0", "s7_fail_0")

label dev_s7_q2:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "2533", OJ_TIME_LIMIT, "s7_ac_1", "s7_fail_1")

label dev_s7_q3:
    $ exam_group_solved = 0
    call oj_challenge("51Nod", "1021", OJ_TIME_LIMIT, "s7_ac_2", "s7_fail_2")

label dev_s7_q4:
    $ exam_group_solved = 0
    call oj_challenge("HDU", "1231", OJ_TIME_LIMIT, "s7_ac_3", "s7_fail_3")

label dev_s8_q1:
    $ exam_group_solved = 0
    call oj_challenge("UVALive", "2026", OJ_TIME_LIMIT, "s8_ac_0", "s8_fail_0")

label dev_s8_q2:
    $ exam_group_solved = 0
    call oj_challenge("LibreOJ", "10027", OJ_TIME_LIMIT, "s8_ac_1", "s8_fail_1")

label dev_s11_q1:
    $ exam_group_solved = 0
    call oj_challenge("51Nod", "2067", OJ_TIME_LIMIT, "s11_ac_0", "s11_fail_0")

label dev_s11_q2:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "1077", OJ_TIME_LIMIT, "s11_ac_1", "s11_fail_1")

label dev_s11_q3:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "1101", OJ_TIME_LIMIT, "s11_ac_2", "s11_fail_2")

label dev_s11_q4:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "1455", OJ_TIME_LIMIT, "s11_ac_3", "s11_fail_3")

label dev_s11_q5:
    $ exam_group_solved = 0
    call oj_challenge("POJ", "1324", OJ_TIME_LIMIT, "s11_ac_4", "s11_fail_4")

label dev_s15_q1:
    $ exam_group_solved = 0
    call oj_challenge("SPOJ", "GSS1", OJ_TIME_LIMIT, "s15_ac_0", "s15_fail_0")
