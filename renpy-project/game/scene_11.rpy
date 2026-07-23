# -*- coding: utf-8 -*-
# 场景 11：《Day 4 状态空间搜索-2》（由原作 s11.json 自动生成）

label s11:
    "..ZzZzzz.."
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-1 Day-4{/size}{w=0.5}{nw}"
    sevenzero "今天和状态空间搜索的 Day 2，\n我准备了四道习题，可能你们已经会做了。"
    sevenzero "额，今天学长比较忙，如果还不会做得话，\n放学之后可以来问我 ..."
    sevenzero "じゃなぁ ..."
    kotori e5 "（什么嘛。。。结果还是要靠自己啊。。）"
    $ exam_group_solved = 0  # 生成题组 exam1（原作 generateExam）

label s11_exam1:
    menu:
        "POJ 3250":
            if exam_done.get("51Nod-2067") != True:
                call oj_challenge("51Nod", "2067", OJ_TIME_LIMIT, "s11_ac_0", "s11_fail_0")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s11_exam1
        "1":
            if exam_done.get("POJ-1077") != True:
                call oj_challenge("POJ", "1077", OJ_TIME_LIMIT, "s11_ac_1", "s11_fail_1")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s11_exam1
        "251Nod-2067":
            if exam_done.get("POJ-1101") != True:
                call oj_challenge("POJ", "1101", OJ_TIME_LIMIT, "s11_ac_2", "s11_fail_2")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s11_exam1
        "51Nod-2067":
            if exam_done.get("POJ-1455") != True:
                call oj_challenge("POJ", "1455", OJ_TIME_LIMIT, "s11_ac_3", "s11_fail_3")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s11_exam1
        "1":
            if exam_done.get("POJ-1324") != True:
                call oj_challenge("POJ", "1324", OJ_TIME_LIMIT, "s11_ac_4", "s11_fail_4")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s11_exam1
        "1":
            pass
    kotori e5 "（我靠这些题目码力也太坑了吧。。）"
    # 〔执行JS（原作游戏逻辑），重制版略〕
    sevenzero "我回来啦..."
    sevenzero "（Kotori 同学通过了 [exam_group_solved] 道题目啊...）"
    if exam_group_solved > 0:
        pass
    scene black with dissolve  # 消除图像
    jump s15  # 更换场景 -> Day 5 数据结构-2


label s11_ac_0:
    $ exam_done["51Nod-2067"] = True
    $ exam_group_solved += 1
    jump s11_exam1

label s11_fail_0:
    jump s11_exam1

label s11_ac_1:
    $ exam_done["POJ-1077"] = True
    $ exam_group_solved += 1
    jump s11_exam1

label s11_fail_1:
    jump s11_exam1

label s11_ac_2:
    $ exam_done["POJ-1101"] = True
    $ exam_group_solved += 1
    jump s11_exam1

label s11_fail_2:
    jump s11_exam1

label s11_ac_3:
    $ exam_done["POJ-1455"] = True
    $ exam_group_solved += 1
    jump s11_exam1

label s11_fail_3:
    jump s11_exam1

label s11_ac_4:
    $ exam_done["POJ-1324"] = True
    $ exam_group_solved += 1
    jump s11_exam1

label s11_fail_4:
    jump s11_exam1
