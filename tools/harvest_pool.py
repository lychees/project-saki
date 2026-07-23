# -*- coding: utf-8 -*-
"""
harvest_pool.py — 抓取 vjudge 全站最近提交流，生成竞技场内置题池
renpy-project/game/arena_pool.json。

原理：GET https://vjudge.net/status/data?draw=1&start=<0|20|50|100>&length=20
（深分页 start>=200 已被封，可用窗口仅最近 ~120 条），过滤 status=="Accepted"，
按 (oj, probNum) 去重。这些题近期有真人 AC，保证真实存在且可通过 vjudge 提交。

用法：python tools/harvest_pool.py     （在仓库根目录执行）
"""
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'renpy-project', 'game', 'arena_pool.json')

STARTS = (0, 20, 50, 100)

CTX = ssl.create_default_context()
try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except Exception:
    pass


def fetch(start):
    q = urllib.parse.urlencode({"draw": 1, "start": start, "length": 20})
    req = urllib.request.Request(
        "https://vjudge.net/status/data?" + q,
        headers={"User-Agent": "Mozilla/5.0",
                 "X-Requested-With": "XMLHttpRequest"})
    with urllib.request.urlopen(req, timeout=15, context=CTX) as r:
        return json.loads(r.read().decode('utf-8'))


def main():
    pool = []
    seen = set()
    for s in STARTS:
        try:
            data = fetch(s)
        except Exception as e:
            print(f'start={s} 抓取失败: {type(e).__name__}: {e}')
            continue
        rows = data.get('data', [])
        print(f'start={s}: {len(rows)} 条提交')
        for row in rows:
            if row.get('status') != 'Accepted':
                continue
            key = (row.get('oj'), str(row.get('probNum')))
            if key[0] and key[1] and key[1] != 'None' and key not in seen:
                seen.add(key)
                pool.append([key[0], key[1]])
        time.sleep(1.0)  # 礼貌抓取
    # 兼容已有池：合并去重
    if os.path.exists(OUT):
        try:
            old = json.load(open(OUT, encoding='utf-8')).get('problems', [])
            for oj, prob in old:
                if (oj, prob) not in seen:
                    seen.add((oj, prob))
                    pool.append([oj, prob])
        except Exception:
            pass
    json.dump({"problems": pool}, open(OUT, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'题池已写入 {os.path.relpath(OUT, ROOT)}，共 {len(pool)} 道题')


if __name__ == '__main__':
    main()
