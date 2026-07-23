# -*- coding: utf-8 -*-
# 场景 2：《Day 1 数据结构-1》（由原作 s2.json 自动生成）

label s2:
    "..ZzZzzz.."
    play sound "audio/se/typing.mp3"
    centered "{size=36}暑期集训篇 Week-1 Day-1{/size}{w=0.5}{nw}"
    scene bg_h012a at fullscreen with dissolve
    # 〔添加材质/滤镜效果，重制版略〕
    play music "audio/bgm/harvest_spring.mp3" fadein 1.0
    "清晨 ..."
    kotori e3 "（頭が痛い ...）"
    kotori e3 "（またあの夢か？...）"
    "清晨的阳光透过窗外投射进枕边。"
    "被过去的梦境折磨的 Kotori 艰难的从晨光之中苏醒。"
    "不知在床上坐了多久，困扰 Kotori 的头痛稍稍得到了缓解。"
    kotori e3 "糟糕，已经 7：50 了吗，\n来不及吃早饭了。。。"
    kotori e3 "呜哈 ~...\n要赶快去教室了 ..."
    scene bg_020 at fullscreen with dissolve
    play sound "audio/se/footsteps.mp3"
    "来不及洗漱吃饭的我，连忙从床上跳起，匆匆的漱了一下口，就往教室飞快的跑去。"
    scene bg_018 at fullscreen with dissolve
    "..."
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    kotori "呼 ...幸好赶上了 ..."
    kotori "啊切，好冷... "
    "第一次来到北方的 Kotori，显然还没有适应这座城市的节奏，\n每天都显得睡眠不足。。。"
    "再加上没吃早饭，更是显得体力不支了。"
    kotori "（开始了！）"
    oneplus "同学们大家好，欢迎来参加 HIT 的暑期算法集训。\n我是目前大四的 OnePlus 学长，目前担任实验室的学生教练。"
    oneplus "集训的课表大家都拿到了，我们每天上午 8：00 准时开始讲课，\n迟到早退的同学会被扣分哦！\n那么现在就让我们开始第一天的内容。"
    "这时，从教室门口传来一阵跑步声，\n然后，“嘭！”的一声，教室门被用力打开了，\n一位学姐正站在门口气喘吁吁。"
    scene cg_xiaodai at fullscreen with dissolve
    $ persistent.cg_xiaodai = True
    $ renpy.notify("CG 鉴赏已解锁：Week1Day1")
    "// 此处应有 CG"
    unknown "哈。。。哈。。。\n赶上了。。。"
    scene bg_017 at fullscreen, gcoffset(0, -177) with dissolve
    kotori e3 "（啊，这位同学，难道是 ...）"
    "尽管并没有见过面，但是我的直觉告诉我，\n眼前这位比我更加匆忙的似乎就是 OIBH 上的 xiaodai 学长。"
    "OIBH，信息学初学者之家，全称 Olympiad in Informatics Beginners' Home。\n是我 OIer 时期经常水的一个论坛，\n我在上面参加过几次训练，也办过一次生日纪念赛，也认识了很多朋友，\n仰慕到了很多大牛 ..."
    "但是。。。\n从去年开始已经打不开了。。。"
    "难道昨天 OnePlus 学长提到的就是他？"
    "我打开手机，向 xiaodai 学长发了一条信息。\n回头后朝他挥手。"
    xiaodai "（挥手）"
    "果然是..."
    oneplus "咳咳。。"
    oneplus "刚才迟到的同学，请找后排的位置坐好。"
    "xiaodai学长在后排安静地坐了下来。\n小小的骚动很快就平息了。"
    oneplus "今天由我来给大家介绍基础数据结构"
    oneplus "栈是算法竞赛中常用的一种线性数据结构。\n栈的修改是按照后进先出的原则进行的，\n因此栈通常被称为是后进先出（last in first out）表，\n简称 LIFO 表。"
    oneplus "我们可以方便的使用数组来模拟一个栈，代码如下："
    oneplus "int stk[[N];\n// 这里使用 stk[[0]( 即 *stk ) 代表栈中元素数量，同时也是栈顶下标\n// 压栈 ：\nstk[[++*stk] = var1;\n// 取栈顶 ：\nint u = stk[[*stk];\n// 弹栈 ：注意越界问题, *stk == 0 时不能继续弹出\nif (*stk) --*stk;\n// 清空栈\n*stk = 0;{w=0.25}{w=0.75}{w=2.50}"
    kotori e5 "啊哈...好困...\n如果是栈和队列的话...早就学过了吧...\n或许可以趁现在接着补下觉什么的。"
    menu:
        "好困...":
            "..ZzZzzz.."
            "..ZzZzzz.."
            oneplus "下面我们来看一道习题..."
            kotori e5 "唔...醒了...\n不对，已经开始做题了吗... ）\n看来得加把劲了。"
        "还是好好听完吧。。":
            kotori "（だめだね！怎么能第一天上课就开始睡觉呢，\n要给大家留下一个好印象才行！）"
            kotori "（振作起来啊，你忘记自己的屈辱了吗？Kotori！）"
            "Kotori 拍了一下自己的脑袋..."
            "于是讲课继续，"
            oneplus "那么首先，我们来看一下这道例题。"
            oneplus "n 个人正在排队进入一个音乐会。人们等得很无聊，\n于是他们开始转来转去，想在队伍里寻找自己的熟人。"
            oneplus "队列中任意两个人 a 和 b，\n如果他们是相邻或他们之间没有人比 a 或 b 高，\n那么他们是可以互相看得见的。\n问有多少对人可以互相看见。\nn <= 500000"
            oneplus "很容易想到暴力 O(n3) 的做法。\n枚举每一对人，再枚举中间每个人看是否都没有比两边高。\n顺带一提，这个过程也可以用线段树或者 Sparse Table \n实现中间的 RMQ 优化到 O(n2logn)。\n但是显然在 n = 500000 的数据范围下都跑不出结果。"
            oneplus "我们考察每新增加一个人，对答案的影响。\n比如如果左边第一个人的身高最高，那么显然\n所有在他左边的人都不会被新来的人看见。\n因而我们只需要维护一个单调递减的栈，\n来记录左边所有有可能被看见的人的身高。"
            oneplus "每个人进栈一次且至多出栈一次，因此复杂度是线性的。"
            oneplus "当然，具体实现的时候，还需要注意考虑身高相等的情况。"
            oneplus "下面我们来看一道习题..."

label s2_jump2:
    $ exam_group_solved = 0  # 生成题组 section2（原作 generateExam）
    menu:
        "POJ 3250":
            if exam_done.get("POJ-3250") != True:
                call oj_challenge("POJ", "3250", OJ_TIME_LIMIT, "s2_ac_0", "s2_fail_0")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s2_jump2
        "POJ 2559":
            if exam_done.get("POJ-2559") != True:
                call oj_challenge("POJ", "2559", OJ_TIME_LIMIT, "s2_ac_1", "s2_fail_1")
            else:
                "你已经完成这个题目了哦！去试试其他的题目吧。"
                jump s2_jump2
        "打完收工":
            pass
    scene black with dissolve  # 消除图像
    jump s7  # 更换场景 -> Day 2 动态规划


label s2_ac_0:
    $ exam_done["POJ-3250"] = True
    $ exam_group_solved += 1
    jump s2_jump2

label s2_fail_0:
    jump s2_jump2

label s2_ac_1:
    $ exam_done["POJ-2559"] = True
    $ exam_group_solved += 1
    jump s2_jump2

label s2_fail_1:
    jump s2_jump2
