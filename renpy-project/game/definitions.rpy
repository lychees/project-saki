# -*- coding: utf-8 -*-
# 角色 / 变量 / 声道定义（重制版）

# 角色（image= 对应 images.rpy 中的 side image，即原作对话框立绘头像）
define kotori = Character("Kotori", image="kotori")
define ykotori = Character("Kotori（幼年）", image="ykotori")
define oneplus = Character("OnePlus", image="oneplus")
define mmc = Character("MoonMayCry", image="mmc")
define xiaodai = Character("xiaodai", image="xiaodai")
define sevenzero = Character("sevenzero", image="sevenzero")
define mother = Character("母上")
define father = Character("父亲")
define teacher = Character("班主任")
define unknown = Character("？？？")

# 做题系统（原作依赖 vjudge API，重制版本地化）
default exam_done = {}          # 各题完成标记（键为原作选项文本）
default exam_group_solved = 0   # 当前题组已通过数量（对应原作玩家变量 #2001）

# 流程标记
default main_story_done = False
default todo_card_shown = False

# 开发者模式（设置界面开关，开启后 Shift+K 呼出开发者跳转菜单）
default persistent.dev_mode = False

# CG 鉴赏（原作 CG#1「标题背景」的图片在服务器上已不存在，仅有 CG#2）
default persistent.cg_xiaodai = False

# 环境音声道（原作 BGS）
init python:
    renpy.music.register_channel("amb", mixer="music", loop=True)
