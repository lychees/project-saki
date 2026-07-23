# -*- coding: utf-8 -*-
# 场景 15：《Day 5 数据结构-2》（由原作 s15.json 自动生成）

label s15:
    centered "{size=36}暑期集训篇 Week-1 Day-5{/size}{w=0.5}{nw}"
    play sound "audio/se/typing.mp3"
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    oneplus "我又回来了 ..."
    oneplus "今天我们来继续数据结构的课程，这一期我们来介绍线段树，\n线段树是用来维护区间信息的数据结构。"
    oneplus "还记得 Day 2 介绍的最大子段和问题吗？\n我们来看那个题目的区间询问版本 —— SPOJ GSS1。"
    oneplus "此题中我们有多组询问，每次询问需要回答给定区间的最大子段和，\n如果每个询问都重新 dp 一遍，复杂度是 O(n2)，显然无法通过给定时限。"
    oneplus "这类涉及区间修改，区间询问的问题，通常可以用线段树方便的解决，"
    oneplus "线段树将每个长度不为 1 的区间划分成左右两个区间递归求解，\n把整个线段划分为一个树形结构，通过合并左右两区间信息来求得该区间的信息。\n这种数据结构可以方便的进行大部分的区间操作。通常情况下，\n线段树对于单点修改，区间修改，区间查询等操作的时间复杂度都是 O(logn) 。"
    oneplus "此题中我们有多组询问，每次询问需要回答给定区间的最大连续子序列和，\n如果每个询问都重新 dp 一遍，复杂度是 O(n2)，显然无法通过给定时限。"
    oneplus "我们可以用线段树维护每个区间的最大子段和，\n为了能够方便的处理区间合并，对于每个区间，我们还需要记录一些额外信息，\n它们分别是："
    scene cg_gss1 at fullscreen, gcoffset(434, 213) with dissolve
    oneplus "ss: 区间和。\nls: 左起最大子段和。\nrs: 右起最大子段和。\nms: 最大子段和。"
    scene cg_gss2 at fullscreen, gcoffset(434, 213) with dissolve
    oneplus "有了这些信息，就可以方便的维护区间的最大子段和信息了。\n区间的最大子段和等于左区间的最大子段和，右区间的最大子段和，以及\n左区间的右起最大子段和+右区间的左起最大子段和 ...\n三者的最大值。"
    oneplus "剩下就是线段树的常规操作，这里就不再赘述了。"
    # 〔消除图像 #2〕
    oneplus "在这道题里，我们不仅复习了 Day 2 所介绍的最大子段和问题，\n而且为了用线段树维护最大子段和，我们需要思考添加怎么额外的辅助数据，\n并且同时进行了维护了区间和，区间最值这些线段树的常规操作。"
    oneplus "下面是今天的习题。"
    $ exam_group_solved = 0  # 生成题组 exam1（原作 generateExam）

label s15_exam1:
    menu:
        "POJ 3250":
            if exam_done.get("SPOJ-GSS1") != True:
                call oj_challenge("SPOJ", "GSS1", OJ_TIME_LIMIT, "s15_ac_0", "s15_fail_0")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s15_exam1
        "打完收工":
            pass
    scene black with dissolve  # 消除图像
    $ main_story_done = True
    jump chapter_select  # 更换场景 -> 选剧本


label s15_ac_0:
    $ exam_done["SPOJ-GSS1"] = True
    $ exam_group_solved += 1
    jump s15_exam1

label s15_fail_0:
    jump s15_exam1
