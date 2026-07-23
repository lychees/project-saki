# -*- coding: utf-8 -*-
# 场景 28：《生日礼物》（由原作 s28.json 自动生成）

label s28:
    play sound "audio/se/typing.mp3"
    centered "{size=36}1997 年，11 月 生日{/size}{w=1.0}{nw}"
    play music "audio/bgm/Moonwisher.mp3" fadein 1.0
    scene bg_h003c at fullscreen, gcoffset(-3, -82) with dissolve
    # 〔添加材质/滤镜效果，重制版略〕
    mother "生日快乐，宝贝！又长大一岁了呢。"
    "蜡烛的火苗在蛋糕上摇曳着\n温暖充盈了房间"
    "6 岁生日的那天 ..."
    mother "对着蛋糕许个愿望吧！"
    kotori "（唔嗯 ... Kotori 许个什么愿望好呢？）"
    "这样思索着，脑海中飞快的闪现出未来的无限多种可能 ...\n每一种未来似乎都在一瞬间进行了一遍演绎 ..."
    "但是果然 Kotori 还是最想成为 ..."
    menu:
        "大数学家":
            kotori "（嗯 ... Kotori 想要成为 ... 像欧拉那样的 大数学家！）"
        "大理论计算机科学家":
            kotori "（嗯 ... Kotori 想要成为 ... 像图灵那样的 大理论计算机科学家！）"
        "大工程师":
            kotori "（嗯 ... Kotori 想要成为 ... 像特斯拉那样的 大工程师！）"
        "大作家":
            kotori "（嗯 ... Kotori 想要成为 ... 像曹雪芹那样的 大作家！）"
        "大艺术家":
            kotori "（嗯 ... Kotori 想要成为 ... 像莫扎特那样的 大艺术家！）"
        "大福利姬":
            kotori "（嗯 ... Kotori 想要成为 ... 像三上悠亚那样的 大福利姬！）"
    scene bg_qq at fullscreen, gcoffset(322, 180) with dissolve
    "这样想着，小手攥紧，在生日蜡烛前兴奋地低下头，小声许愿"
    kotori "许好了！"
    kotori "哈 ...\n呼~~！"
    "我一口气吹熄了生日蜡烛，而母上在一旁为我高兴地鼓起掌。"
    # 〔消除图像 #2〕
    mother "然后是礼物。"
    "母上大人拿出了一个很大的盒子。"
    mother "这是你爸从深圳寄给你的礼物。\n快打开吧。"
    kotori "（前年是变形金刚，去年是 FC。。。\n今年会是什么呢...）"
    "我迫不及待地拆开了盒子。"
    kotori "哇。。。是电脑。。。"
    "外壳是白色的，方大的显示器，长方形的机箱上有着不少按钮和接口，还有键盘和鼠标。"
    kotori "好厉害。。。 和科技馆看到的那个。。\n一模一样。。。。"
    stop music fadeout 2.0
    "学着在科技馆看见的操作，我把电脑搬上桌，接上电源和键盘鼠标的接线，然后按下了机箱上小小的开机键。"
    # 〔添加材质/滤镜效果，重制版略〕
    play sound "audio/se/windows95_open.ogg"
    scene bg_computer at fullscreen with dissolve
    "..."
    "运行。。\n蓝天白云\nWindows 95"
    kotori "（お父さん ...）"
    # 〔移动图片/渐变 30帧〕
    kotori "（だいすき…）"
    scene black with dissolve  # 消除图像
    jump s2  # 更换场景 -> Day 1 数据结构-1
