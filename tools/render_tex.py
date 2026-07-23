# -*- coding: utf-8 -*-
"""
render_tex.py — 扫描 game/*.rpy 中的 {tex=...} 标签，用 matplotlib mathtext
离线渲染为透明底白字 PNG（game/images/tex/<hash>.png），并生成
game/tex_images.rpy 图像定义。

用法（在仓库根目录 D:/dev/fable-vibe/saki 下）：
    .tmp/venv/Scripts/python.exe tools/render_tex.py

注意：
- 不需要安装完整 LaTeX，使用 matplotlib 内置 mathtext（语法为其子集，
  支持 \\frac \\sqrt \\sum \\binom \\mathrm 等常用命令）。
- 公式内容即渲染 key：md5(公式)[:12] 为文件名 / 图像名后缀。
- Ren'Py 文本中写公式时，花括号写法见 README（{tex=...} 内可正常使用 {}）。
"""
import io
import os
import re
import sys
import hashlib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, 'renpy-project', 'game')
TEX_DIR = os.path.join(GAME, 'images', 'tex')
OUT_RPY = os.path.join(GAME, 'tex_images.rpy')

FONTSIZE = 16   # 公式字号（渲染后约 40+px 行高，适合 1200x720 窗口内联显示）
DPI = 200


def find_tex_tags(text):
    """找出所有 {tex=...} 的公式内容（公式分组用全角花括号 ｛｝ 书写）。"""
    rv = []
    for m in re.finditer(r'\{tex=', text):
        i = m.end()
        depth = 1
        start = i
        while i < len(text) and depth:
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
            i += 1
        if depth == 0:
            # 全角花括号 -> LaTeX 花括号；剧本中的 \\（Python 字符串转义）-> 单反斜杠
            # （与 tex_tag.rpy 运行时拿到的字符串保持一致）
            raw = text[start:i - 1]
            conv = raw.replace('｛', '{').replace('｝', '}').replace('\\\\', '\\')
            rv.append(conv)
    return rv


def tex_hash(formula):
    return hashlib.md5(formula.strip().encode('utf-8')).hexdigest()[:12]


def render(formula, path):
    fig = plt.figure()
    fig.text(0.5, 0.5, f'${formula}$', fontsize=FONTSIZE, color='white',
             ha='center', va='center')
    fig.savefig(path, dpi=DPI, transparent=True,
                bbox_inches='tight', pad_inches=0.04)
    plt.close(fig)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(TEX_DIR, exist_ok=True)
    formulas = []
    for fn in sorted(os.listdir(GAME)):
        if fn.endswith('.rpy'):
            for line in open(os.path.join(GAME, fn), encoding='utf-8'):
                if line.lstrip().startswith('#'):  # 忽略整行注释
                    continue
                for f in find_tex_tags(line):
                    if f not in formulas:
                        formulas.append(f)
    defs = ['# -*- coding: utf-8 -*-',
            '# LaTeX 公式图像定义（由 tools/render_tex.py 自动生成，勿手改）', '']
    n_new = 0
    for f in formulas:
        h = tex_hash(f)
        png = os.path.join(TEX_DIR, h + '.png')
        if not os.path.exists(png):
            try:
                render(f, png)
            except Exception as e:
                print(f'[FAIL] {f!r}: {type(e).__name__}: {e}')
                continue
            n_new += 1
            print(f'[渲染] {h}.png  <-  {f}')
        defs.append(f'image tex_{h} = "images/tex/{h}.png"')
    defs.append('')
    open(OUT_RPY, 'w', encoding='utf-8').write('\n'.join(defs))
    print(f'完成：共 {len(formulas)} 个公式，新渲染 {n_new} 个，定义写入 {os.path.relpath(OUT_RPY, ROOT)}')


if __name__ == '__main__':
    main()
