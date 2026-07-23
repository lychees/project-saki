# -*- coding: utf-8 -*-
"""列出 game/ 下文件名含非 ASCII 或空格的文件。"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

GAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'renpy-project', 'game')

bad = []
for root, dirs, files in os.walk(GAME):
    for f in files:
        full = os.path.join(root, f)
        rel = os.path.relpath(full, GAME).replace(os.sep, '/')
        if not rel.isascii() or ' ' in rel:
            bad.append(rel)
for b in sorted(bad):
    print(b)
print(len(bad), 'files')
