# -*- coding: utf-8 -*-
# 场景 7：《Day 2 动态规划》（由原作 s7.json 自动生成）

label s7:
    "..ZzZzzz.."
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-1 Day-2{/size}{w=0.5}{nw}"
    oneplus "今天来介绍动态规划的部分，\n关于理论部分，比如重叠子问题，最优子结构以及无后效性，\n这里就不再赘述了，大家可以自己去看教材或讲义。"
    oneplus "关于动态规划的动机，其一是重叠子问题，其二是多阶段决策。\n而具体做起来主要考察的就是，设计状态，寻找 状态转移方程，\n以及最后的优化时间复杂度。"
    oneplus "我们先来看一道最简单的模型。\n最大连续子序列和问题 ..."
    oneplus "最大连续子序列和问题，有时也被称作最大子段和问题，\n给定 n 个整数的序列 a，求所有连续子序列中，和最大的一个，\n例如给定序列 -2, 11, -4, 13, -5, -2，\n其最大连续子序列为 11, -4, 13，和为 11-4+13 = 20。"
    $ exam_group_solved = 0  # 生成题组 exam2（原作 generateExam）

label s7_exam2:
    menu:
        "POJ 3250":
            if exam_done.get("POJ-1141") != True:
                call oj_challenge("POJ", "1141", OJ_TIME_LIMIT, "s7_ac_0", "s7_fail_0")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s7_exam2
        "打完收工":
            pass
    oneplus "我们再来看一道经典的问题 ...\n最长递增子序列（Longest Increasing Subsequence）问题。"
    oneplus "求一个序列的最长递增子序列，\n这里还是注意子序列和子串的不同，\n前者不要求位置连续。\n例如：4 2 3 1 5 的最长递增子序列为 2 3 5，长度为 3 。"
    oneplus "做法如下。"
    scene cg_lis at fullscreen, gcoffset(250, 12) with dissolve
    oneplus "我们设 dp[[i] 表示以 a[[i] 结尾的 LIS 长度，那么有：\ndp[[i] = max(dp[[j] + 1)  | j ..."
    oneplus "我们把 +1 放在循环外面，就是上面的代码了。\n上面的代码复杂度是 O(n2)。\n下面再来介绍复杂度更优秀的 O(nlogn) 做法。"
    oneplus "上面内层循环中，实际上存在着许多的冗余。\n我们并不需要枚举之前所有的数，而是去记录一个当前最优的 LIS，\n也就是每个位置的数都尽可能小。"
    # 〔消除图像 #2〕
    kotori e5 "（啊。。。又开始困了。。。）"
    menu:
        "好困...":
            kotori e5 "（小睡一会儿的话，应该，没关系的吧。。）"
            "..ZzZzzz.."
            oneplus "下面我们来做一些习题。"
            kotori e5 "（啊。。。怎么又直接到习题阶段了。。。）"
            jump s7_jump1
        "振作一点，Kotori！":
            pass
    oneplus "我们设 b 数组表示这个最优的 LIS，那么每次新增加一个数 a[[i]，\n要么我们可以将 a[[i] 添加在 b 的末尾，\n要么我们用 a[[i] 去更新 b 数组中，\n第一个大于等于 a[[i] 的数。"
    scene cg_lis2 at fullscreen, gcoffset(19, 11) with dissolve
    oneplus "由于 b 数组符合 LIS 性质，单调递增，\n因而我们可以使用二分查找将复杂度优化到 O(nlogn)。"
    oneplus "下面我们来做一些习题。"

label s7_jump1:
    $ exam_group_solved = 0  # 生成题组 exam1（原作 generateExam）

label s7_exam1:
    menu:
        "POJ 3250":
            if exam_done.get("POJ-2533") != True:
                call oj_challenge("POJ", "2533", OJ_TIME_LIMIT, "s7_ac_1", "s7_fail_1")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s7_exam1
        "打完收工":
            pass
    # 〔消除图像 #3〕
    oneplus "下面我们再来看一道经典的例题 ...\n石子归并 ..."
    oneplus "有一个石子归并的游戏。最开始的时候，有 n 堆石子排成一列，\n目标是要将所有的石子合并成一堆，合并规则如下：\n每一次可以合并 相邻 位置的两堆石子\n每次合并的代价为所合并的两堆石子的重量之和\n求出最小的合并代价。"
    $ exam_group_solved = 0  # 生成题组 exam3（原作 generateExam）

label s7_exam3:
    menu:
        "POJ 3250":
            if exam_done.get("51Nod-1021") != True:
                call oj_challenge("51Nod", "1021", OJ_TIME_LIMIT, "s7_ac_2", "s7_fail_2")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s7_exam3
        "打完收工":
            pass
    oneplus "再看一题？"
    $ exam_group_solved = 0  # 生成题组 exam4（原作 generateExam）

label s7_exam4:
    menu:
        "POJ 3250":
            if exam_done.get("HDU-1231") != True:
                call oj_challenge("HDU", "1231", OJ_TIME_LIMIT, "s7_ac_3", "s7_fail_3")
            else:
                "你已经完成所有题目了哦！"
                jump s7_exam4
        "打完收工":
            pass
    oneplus "今天的课程到这里就结束了。"
    scene black with dissolve  # 消除图像
    jump s8  # 更换场景 -> Day 3 状态空间搜索-1


label s7_ac_0:
    $ exam_done["POJ-1141"] = True
    $ exam_group_solved += 1
    jump s7_exam2

label s7_fail_0:
    jump s7_exam2

label s7_ac_1:
    $ exam_done["POJ-2533"] = True
    $ exam_group_solved += 1
    jump s7_exam1

label s7_fail_1:
    jump s7_exam1

label s7_ac_2:
    $ exam_done["51Nod-1021"] = True
    $ exam_group_solved += 1
    jump s7_exam3

label s7_fail_2:
    jump s7_exam3

label s7_ac_3:
    $ exam_done["HDU-1231"] = True
    $ exam_group_solved += 1
    jump s7_exam4

label s7_fail_3:
    jump s7_exam4
