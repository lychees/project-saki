# -*- coding: utf-8 -*-
# CG 鉴赏（对应原作自定义模块「CG鉴赏」）
# 原作 CG#1「标题背景」引用的图片（Title_1.png 等）在服务器上已不存在（404），
# 仅 CG#2「Week1Day1」可在剧情中解锁。

screen gallery():
    tag menu

    use game_menu(_("CG鉴赏")):

        vbox:
            spacing 20

            text "在剧情中解锁的 CG 会出现在这里。" size 22

            hbox:
                spacing 30

                # CG#1 标题背景（原作图片缺失，无法解锁）
                vbox:
                    spacing 6
                    frame:
                        xysize (360, 203)
                        background Solid("#222")
                        text "？？？" align (0.5, 0.5) size 40 color "#666"
                    text "CG#1 标题背景（原作图片缺失）" size 18

                # CG#2 Week1Day1
                vbox:
                    spacing 6
                    if persistent.cg_xiaodai:
                        imagebutton:
                            idle im.Scale("images/cg/illustration/xiaodai_door_crash.jpg", 360, 203)
                            action Show("gallery_full", img="images/cg/illustration/xiaodai_door_crash.jpg")
                        text "CG#2 Week1Day1" size 18
                    else:
                        frame:
                            xysize (360, 203)
                            background Solid("#222")
                            text "？？？" align (0.5, 0.5) size 40 color "#666"
                        text "CG#2 Week1Day1（未解锁）" size 18


screen gallery_full(img):
    modal True
    add img at truecenter
    key "dismiss" action Hide("gallery_full")
    imagebutton:
        idle Solid("#0000")
        xysize (1200, 720)
        action Hide("gallery_full")
