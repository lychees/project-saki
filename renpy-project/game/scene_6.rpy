# -*- coding: utf-8 -*-
# 场景 6：《网络流篇-1》（由原作 s6.json 自动生成）

label s6:
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    kotori "xiaodai 学长！"
    # 〔画面特效，重制版略〕
    "我气喘吁吁的追上正在收拾书包的 xiaodai 学长 ..."
    kotori "请，请教我做网络流！"
    xiaodai "唉？为什么这么突然。。。"
    kotori "因为我听他们群里面说，一切算法皆网络流！\n我也想理解其中的秘辛！"
    xiaodai "那种事情，只是 DIY 群里的段子吧。。。"
    kotori "我知道... 可是，就算是我，也是想要变强的！"
    xiaodai "好吧，最短路学过了没？"
    kotori "学过了。"
    xiaodai "流网络的定义看过了么？"
    kotori "看过了。"
    xiaodai "那么先从最大流算法开始，最主流的算法就是增广路算法，\n也就是不断的寻找增广路，像是 Dinic、Sap 都属于这类。"
    kotori "那么，请问，什么是增广路呢？"
    xiaodai "就是在残量网络中，源点到汇点的路径。\n匈牙利算法的证明里也有类似的概念，乃不会都没学进去吧。"
    kotori "呜呜... 可以沿着增广路继续推流，因此此时一定不是最大流，我能理解。\n可是为什么不存在增广路时，能保证找到的一定就是最大流呢？"
    xiaodai "这个证明就是最大流最小割定理。\n简单的来说就是对于流网络来说，\n找到最大流，不存在增广路，和存在某个容量等于\n最大流的割这三件事，是等价的。"
    xiaodai "证明的过程主要就是说明当不存在增广路时，\n可以构造性的找到某个割，使得该割容量等于当前流。\n又因为流量总是小于等于割的容量，\n所以此时的流一定最大流，找到的割集既最小割。"
    xiaodai "至于用什么方法找增广路，就看你的喜好了，\n随便套个模板就行。我给你个 sap 的模板吧。"
    kotori "なるほど... 那这么看其实还挺简单的。。"
    xiaodai "当然最大流最小割定理真正重要的是说明了\n找到最大流的同时也找到了最小割。\n而这类题目真正困难的就是用最小割建模。"
    kotori "只要有了这个网络流模板，就算是我，也可以天下无敌了吧。\n什么最小割建模，我也可以的 ..."
    xiaodai "是吗，那么让我来考考你 ..."
    xiaodai "Andrew Stankevich Contest #4, Unique Attack ...\n给定一个流网络，判断其最小割是否唯一 ..."
    $ exam_group_solved = 0  # 生成题组 section1（原作 generateExam）

label s6_jump2:
    menu:
        "POJ 3250":
            if exam_done.get("ZOJ-2587") != True:
                call oj_challenge("ZOJ", "2587", OJ_TIME_LIMIT, "s6_ac_0", "s6_fail_0")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s6_jump2
        "打完收工":
            if exam_group_solved == 0:
                xiaodai " 不给力啊，Kotori 老师 ..."
                kotori e15 "呜 ..."
                xiaodai "最大流最小割定理的证明里，已经包含了最小割的构造方法。\n方法是从 S 出发，沿残量网络 dfs() 染色即可。\n要判断最小割是否唯一，可以从 S 和 T 分别染色，\n看是否可以覆盖所有结点。"
                kotori e15 "我再学习一下 ..."
                xiaodai "今天就先到这里，先去吃饭吧 ..."
            else:
                xiaodai "不愧是 Kotori 老师 。。。"
                kotori e2 "那必须的 ... 这种题目根本塞牙缝都不够 ..."
                xiaodai "看来你已经熟练掌握最小割的构造方法，\n不妨我们再看一个例题 ..."
                $ exam_group_solved = 0  # 生成题组 section2（原作 generateExam）
                menu:
                    "POJ 3250":
                        if exam_done.get("POJ-3469") != True:
                            call oj_challenge("POJ", "3469", OJ_TIME_LIMIT, "s6_ac_1", "s6_fail_1")
                        else:
                            "你已经完成这个题目了哦！去试试其他的题目吧。"
                            jump s6_jump2
                    "打完收工":
                        if exam_group_solved == 0:
                            xiaodai " 不给力啊，Kotori 老师 ..."
                            kotori e15 "呜 ..."
                        else:
                            xiaodai "不愧是 Kotori 老师 。。。"
                            kotori e2 "那必须的 ... 这种题目根本塞牙缝都不够 ..."
    scene black with dissolve  # 消除图像
    jump chapter_select  # 更换场景 -> 选剧本


label s6_ac_0:
    $ exam_done["ZOJ-2587"] = True
    $ exam_group_solved += 1
    jump s6_jump2

label s6_fail_0:
    jump s6_jump2

label s6_ac_1:
    $ exam_done["POJ-3469"] = True
    $ exam_group_solved += 1
    jump s6_jump2

label s6_fail_1:
    jump s6_jump2
