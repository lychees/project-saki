# -*- coding: utf-8 -*-
# 自定义文本标签 {tex=...}：在对话文本中内联显示 LaTeX 公式。
# 公式 PNG 由 tools/render_tex.py 离线预渲染（matplotlib mathtext），
# 本标签运行时按公式内容的 md5 找到对应图片显示；找不到时显示红色占位提示。

init python:

    import hashlib

    def _tex_hash(formula):
        # 剧本里用全角花括号 ｛｝ 代替 {}（Ren'Py 文本标签不支持嵌套花括号）
        formula = formula.replace('｛', '{').replace('｝', '}')
        return hashlib.md5(formula.strip().encode("utf-8")).hexdigest()[:12]

    def tex_tag(tag, argument):
        h = _tex_hash(argument)
        fn = "images/tex/" + h + ".png"
        if renpy.loadable(fn):
            return [(renpy.TEXT_DISPLAYABLE, im.Image(fn))]
        # 未渲染：提醒作者去跑 tools/render_tex.py（用全角括号避免被当成标签）
        return [(renpy.TEXT_DISPLAYABLE,
                 Text("「公式未渲染」", color="#ff6666", size=20))]

    config.self_closing_custom_text_tags["tex"] = tex_tag
