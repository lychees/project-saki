# -*- coding: utf-8 -*-
# 场景 8：《Day 3 状态空间搜索-1》（由原作 s8.json 自动生成）

label s8:
    "..ZzZzzz.."
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-1 Day-3{/size}{w=0.5}{nw}"
    oneplus "从今天开始我们将开始新的主题，\n后续两天的课程将由 Sevenzero 学长负责。"
    sevenzero "大家好。。。"
    kotori "哇呜..."
    kotori "（这个就是 HIT 现役最强的选手吗？）"
    kotori "（不知道和 Sevenkplus 相比谁更厉害。）"
    kotori "（不管怎么说，先加入《个别名单记录》，\n如果想进入 WorldFinal 就必须先打败她才行！）"
    "不知为何，Kotori 的心中燃起了斗志。"
    sevenzero "（搜索吗，真是无聊的问题。）"
    sevenzero "（姑且用来打发打发时间吧。）"
    sevenzero "（不知道这个学期会不会有厉害的新人加入。如果没有就太无聊了。。。）"
    sevenzero "嗯啊。（清嗓子）"
    sevenzero "今天和大家讲解状态空间搜索，\n也就是 —— 暴搜。"
    sevenzero "暴搜是 ACM 里最基本的解题方法，\n在人工智能和图论里也经常出现，"
    sevenzero "说起来多少是有一些无脑的策略，反正学了也没啥坏处，\n当你在赛场上实在没有事情可干时，\n至少，还可以暴搜找找规律。"
    sevenzero "根据搜索顺序的不同主要可以分为\n深度优先搜索（DFS）和广度优先搜索（BFS）两种。"
    sevenzero "前者使用栈保存当前访问的状态，\n后者使用队列。"
    sevenzero "下面先来看一个 dfs() 的例子。"
    sevenzero "生成排列问题。\n输入 n，按照字典序输出 n 的所有排列。"
    sevenzero "例如输入 3，输出：\n1 2 3\n1 3 2\n2 1 3\n2 3 1\n3 1 2\n3 2 1"
    sevenzero "代码大概如下："
    scene cg_perm at fullscreen, gcoffset(318, 9) with dissolve
    sevenzero "因为可以方便的使用递归，\n所以 dfs() 的时候一般不需要写手工栈。\n除非一些特殊情况，要维护额外的东西或者评测姬又爆栈的可能。"
    sevenzero "一般说来在递归函数里，我们先处理边界情况。\n在这道题里是就是 k=n 时，\n说明我们的函数已经找到了一组排列，printf 即可。"
    sevenzero "k 为了保证字典序，我们总是从最小的元素开始枚举，\n如果当前元素未被使用，就标记使用，递归到下一层。\n记得递归回来时要将这个标记删除。"
    sevenzero "下面是例题。"
    $ exam_group_solved = 0  # 生成题组 exam1（原作 generateExam）

label s8_exam1:
    menu:
        "POJ 3250":
            if exam_done.get("UVALive-2026") != True:
                call oj_challenge("UVALive", "2026", OJ_TIME_LIMIT, "s8_ac_0", "s8_fail_0")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s8_exam1
        "打完收工":
            pass
    # 〔消除图像 #2〕
    sevenzero "讲完了 dfs()，下面再来看 bfs()。"
    sevenzero "和 dfs()，在 bfs() 中我们按照距离初始结点的距离，\n从近到远扩展结点，因此在一些需要求最短距离的题目中会比 dfs() 更加直接。"
    sevenzero "我们再来看一道 bfs() 的例题 —— 魔板。\n我们有一张拥有 8 个格子的魔板，初始状态为：\n1 2 3 4\n8 7 6 5"
    sevenzero "我们可以对魔板进行三种操作。\nA：交换上下两行\nB：将最右一列插入左侧\nC：魔板中间四个格子顺时针旋转。\n给出一个状态排列，求转换至初始状态所需的最少操作。"
    sevenzero "对于这道题，我们可以使用bfs()来求解。\n首先，我们先构建这道题所需的答案，\n设Ai为排列，Si为从给出的起点排列到排列Ai所需的步骤。\n我们可以轻松地用字符串和map来构建答案，\n我们将排列和步骤都存储为字符串，并存入map中。"
    sevenzero "接下来构建bfs部分，将每个排序看成节点，每个操作看成连接节点的边。\n然后再使用队列储存需要处理的节点，弹出处理完毕的节点。\n可以很容易地构建出\n“从一个起点排序开始，进行循环处理，\n每次处理一种针对该排列的操作，然后将操作后得出的排序存入队列，\n再将对应的状态步骤，也就是我们需要的答案存入map中。\n一个排序的处理结束后，将其弹出队列，然后再处理被存入队列的下一个排序。\n当处理至我们的目标排序时，结束处理并输出存在map中的答案。”\n这样的操作。\n就是这样，简单易懂。\n剩下的就是把代码写出来了。"
    sevenzero "好了，来自己做做？"
    $ exam_group_solved = 0  # 生成题组 exam2（原作 generateExam）

label s8_exam2:
    menu:
        "POJ 3250":
            if exam_done.get("LibreOJ-10027") != True:
                call oj_challenge("LibreOJ", "10027", OJ_TIME_LIMIT, "s8_ac_1", "s8_fail_1")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s8_exam2
        "打完收工":
            pass
    sevenzero "这道题是很简单的bfs的模板题，除此之外还有很多变形的题目，\n也有许多基于bfs的变形算法来处理这些复杂问题。\n可不要做会了一道题就觉得自己学懂了哦。\n明天会介绍一些更复杂的题目。"
    scene black with dissolve  # 消除图像
    jump s11  # 更换场景 -> Day 4 状态空间搜索-2


label s8_ac_0:
    $ exam_done["UVALive-2026"] = True
    $ exam_group_solved += 1
    jump s8_exam1

label s8_fail_0:
    jump s8_exam1

label s8_ac_1:
    $ exam_done["LibreOJ-10027"] = True
    $ exam_group_solved += 1
    jump s8_exam2

label s8_fail_1:
    jump s8_exam2
