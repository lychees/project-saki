# -*- coding: utf-8 -*-
"""
ascii_rename.py — 一次性脚本：把 renpy-project/game/ 下的非 ASCII / 含空格 /
含 '+' 的素材文件重命名为 Web 安全的 ASCII 名，并全局替换所有 .rpy 引用。
同时修复 audio/se/se/ 双层嵌套（引用路径本来就是 audio/se/ 单层）。

用法：python tools/ascii_rename.py        （在仓库根目录执行，幂等）
"""
import os
import re
import sys
import glob
import shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, 'renpy-project', 'game')

# old rel path -> new rel path（相对于 game/）
MAPPING = {
    'audio/bgm/何日君再来.ogg': 'audio/bgm/he_ri_jun_zai_lai.ogg',
    'audio/bgm/牧场物语 春.mp3': 'audio/bgm/harvest_spring.mp3',
    'audio/bgm/逆转裁判 1 BGM.mp3': 'audio/bgm/ace_attorney_1_bgm.mp3',
    'audio/bgm/龙出现.ogg': 'audio/bgm/dragon_appears.ogg',
    'audio/se/打字.mp3': 'audio/se/typing.mp3',
    'audio/se/敲门.mp3': 'audio/se/knock.mp3',
    'audio/se/汽笛声.mp3': 'audio/se/whistle.mp3',
    'audio/se/脚步声.mp3': 'audio/se/footsteps.mp3',
    'audio/se/铁轨声.mp3': 'audio/se/railway.mp3',
    'audio/se/逆转裁判/gallary.ogg': 'audio/se/ace_attorney/gallery.ogg',
    'audio/se/逆转裁判/realization.ogg': 'audio/se/ace_attorney/realization.ogg',
    'images/bg/background/QQ图片20210617223344.jpg': 'images/bg/background/qq_photo_20210617.jpg',
    'images/cg/illustration/蜜汁破门而入的Xiaodai.jpg': 'images/cg/illustration/xiaodai_door_crash.jpg',
    'images/cg/titles/Title_1 - 副本.png': 'images/cg/titles/title_1.png',
    'images/char/characters/kotori/幼年/c152019-d605227-p605227+.png':
        'images/char/characters/kotori/childhood/c152019-d605227-p605227_plus.png',
    'images/char/characters/kotori/短发/c635752-d75956-p143679 害怕.png':
        'images/char/characters/kotori/short/c635752-d75956-p143679_scared.png',
    'images/char/characters/kotori/短发/c635752-d75956-p424008.png':
        'images/char/characters/kotori/short/c635752-d75956-p424008.png',
    'images/char/characters/kotori/短发/c635752-d75956-p466843.png':
        'images/char/characters/kotori/short/c635752-d75956-p466843.png',
    'images/char/characters/kotori/短发/c635752-d75956-p507942.png':
        'images/char/characters/kotori/short/c635752-d75956-p507942.png',
    'images/char/characters/kotori/短发/c635752-d75956-p598344.png':
        'images/char/characters/kotori/short/c635752-d75956-p598344.png',
    'images/char/characters/kotori/短发/c635752-d75956-p603059 疑惑 帽子.png':
        'images/char/characters/kotori/short/c635752-d75956-p603059_confused_hat.png',
    'images/char/characters/kotori/长发/c635752-d75956-p100924.png':
        'images/char/characters/kotori/long/c635752-d75956-p100924.png',
    'images/char/characters/kotori/长发/c635752-d75956-p153987.png':
        'images/char/characters/kotori/long/c635752-d75956-p153987.png',
    'images/char/characters/kotori/长发/c635752-d75956-p61336.png':
        'images/char/characters/kotori/long/c635752-d75956-p61336.png',
    'images/char/characters/kotori/长发/c635752-d75956-p969930.png':
        'images/char/characters/kotori/long/c635752-d75956-p969930.png',
    'images/ui/ui/menu/new/default Image.png': 'images/ui/ui/menu/new/default_image.png',
    'images/ui/ui/menu/new/title_CG gallery.png': 'images/ui/ui/menu/new/title_cg_gallery.png',
    'images/ui/ui/menu/new/未命名文件夹/textInputBg.png':
        'images/ui/ui/menu/new/unnamed/textInputBg.png',
}


def flatten_se():
    """audio/se/se/* -> audio/se/（修复双层嵌套）。"""
    nested = os.path.join(GAME, 'audio', 'se', 'se')
    if not os.path.isdir(nested):
        return 0
    n = 0
    for item in os.listdir(nested):
        shutil.move(os.path.join(nested, item), os.path.join(GAME, 'audio', 'se', item))
        n += 1
    os.rmdir(nested)
    return n


def main():
    n_flat = flatten_se()
    if n_flat:
        print(f'[扁平化] audio/se/se/ 下 {n_flat} 项上移到 audio/se/')

    renamed = 0
    for old, new in MAPPING.items():
        src = os.path.join(GAME, old)
        dst = os.path.join(GAME, new)
        if not os.path.exists(src):
            if os.path.exists(dst):
                continue  # 已重命名过（幂等）
            print(f'[警告] 源文件不存在: {old}')
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        os.rename(src, dst)
        renamed += 1
        print(f'[重命名] {old}  ->  {new}')

    # 清理已空的旧目录
    for d in ('audio/se/逆转裁判',
              'images/char/characters/kotori/幼年',
              'images/char/characters/kotori/短发',
              'images/char/characters/kotori/长发',
              'images/ui/ui/menu/new/未命名文件夹'):
        p = os.path.join(GAME, d)
        if os.path.isdir(p) and not os.listdir(p):
            os.rmdir(p)
            print(f'[删空目录] {d}')

    # 全局替换 .rpy 引用
    n_file = n_sub = 0
    for f in glob.glob(os.path.join(GAME, '*.rpy')):
        text = open(f, encoding='utf-8').read()
        orig = text
        for old, new in MAPPING.items():
            if old in text:
                text = text.replace(old, new)
                n_sub += 1
        if text != orig:
            open(f, 'w', encoding='utf-8').write(text)
            n_file += 1
    print(f'[替换] {n_file} 个 .rpy 文件，{n_sub} 处引用')

    # 删除旧的编译缓存（内含旧路径）
    n_rpyc = 0
    for f in glob.glob(os.path.join(GAME, '**', '*.rpyc'), recursive=True):
        os.remove(f)
        n_rpyc += 1
    print(f'[清理] 删除 {n_rpyc} 个 .rpyc')

    # 校验：game/ 下不应再有非 ASCII / 空格 / '+' 文件名
    bad = []
    for root, dirs, files in os.walk(GAME):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), GAME).replace(os.sep, '/')
            if not rel.isascii() or ' ' in rel or '+' in rel:
                bad.append(rel)
    if bad:
        print('[残留问题文件]')
        for b in bad:
            print('  ', b)
    else:
        print('[校验] 所有文件名已 ASCII 安全')
    print(f'完成：重命名 {renamed} 个文件')


if __name__ == '__main__':
    main()
