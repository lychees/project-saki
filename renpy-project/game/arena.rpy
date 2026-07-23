# -*- coding: utf-8 -*-
# 竞技场模式（Arena）：随机抽 n 道题限时挑战。
# 桌面版：实时拉取全站最近 AC 提交流组成题池 + 后台轮询判题；
# Web 版：无网络栈，用内置题池 + 手动「标记通过」。
# 所有变量以 arena_ 前缀命名，与剧情模式隔离；线程对象不入 store。

# 玩家可调设置（保留在存档中）
default arena_n = 5            # 题数 1~10
default arena_limit_min = 90   # 总时限 30/60/90/120 分钟

init python:

    import time as _arena_time
    import json as _arena_json
    import random as _arena_random

    ARENA_IS_WEB = renpy.variant("web")

    # 网络栈仅桌面平台导入（同 oj.rpy 的平台隔离模式；自包含 SSL context，
    # 不依赖 oj.rpy 的 init 顺序）
    if not ARENA_IS_WEB:
        import threading as _arena_threading
        import ssl as _arena_ssl
        import urllib.request as _arena_urlreq
        import urllib.parse as _arena_urlparse
        try:
            import certifi as _arena_certifi
            _arena_ssl_ctx = _arena_ssl.create_default_context(cafile=_arena_certifi.where())
        except Exception:
            _arena_ssl_ctx = _arena_ssl._create_unverified_context()

    renpy._arena_thread = None
    renpy._arena_stop = False

    ARENA_POLL_INTERVAL = 15.0

    # ---- 内置题池（打包在 game/arena_pool.json，可用 tools/harvest_pool.py 刷新）----
    try:
        with renpy.file("arena_pool.json") as _f:
            _arena_pool_bundled = [list(x) for x in _arena_json.load(_f).get("problems", [])]
    except Exception:
        _arena_pool_bundled = []
    store.arena_pool_bundled = _arena_pool_bundled

    def _arena_get(url):
        req = _arena_urlreq.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest"})
        with _arena_urlreq.urlopen(req, timeout=10, context=_arena_ssl_ctx) as r:
            return _arena_json.loads(r.read().decode("utf-8"))

    # ---- 实时题池抓取（桌面；全站最近 AC 提交流，深分页被封只取 ~120 条窗口）----
    def _arena_fetch_loop():
        pool = []
        seen = set()
        for start in (0, 20, 50, 100):
            if renpy._arena_stop:
                return
            try:
                q = _arena_urlparse.urlencode({"draw": 1, "start": start, "length": 20})
                data = _arena_get("https://vjudge.net/status/data?" + q)
                for row in data.get("data", []):
                    if row.get("status") != "Accepted":
                        continue
                    oj, prob = row.get("oj"), str(row.get("probNum"))
                    if oj and prob and prob != "None" and (oj, prob) not in seen:
                        seen.add((oj, prob))
                        pool.append([oj, prob])
            except Exception:
                store.arena_fetch_status = "neterr"
        if len(pool) >= store.arena_n:
            store.arena_pool_live = pool
            store.arena_fetch_status = "ok"
        else:
            # 去重题数不足：回退内置池
            store.arena_pool_live = []
            store.arena_fetch_status = "fallback"

    def _arena_fetch_pool():
        """开始抽题准备：桌面起线程抓实时池；Web 经 Worker /pool 同步抓取。"""
        store.arena_pool_live = []
        if ARENA_IS_WEB:
            # renpy.fetch 在非交互上下文调用（label 流程中），不卡帧
            try:
                r = renpy.fetch(store.OJ_PROXY_BASE + "/pool", timeout=10, result="json")
                if r.get("ok") and len(r.get("pool", [])) >= store.arena_n:
                    store.arena_pool_live = [[x["oj"], x["prob"]] for x in r["pool"]]
                    store.arena_fetch_status = "ok"
                else:
                    store.arena_fetch_status = "fallback"
            except Exception:
                store.arena_fetch_status = "fallback"
            return
        store.arena_fetch_status = "fetching"
        renpy._arena_stop = False
        th = _arena_threading.Thread(target=_arena_fetch_loop)
        th.daemon = True
        renpy._arena_thread = th
        th.start()

    def _arena_begin():
        """抽题并开始计时。返回是否成功。"""
        renpy._arena_stop = True
        renpy._arena_thread = None
        pool = store.arena_pool_live or store.arena_pool_bundled
        if not pool:
            return False
        n = min(store.arena_n, len(pool))
        picked = _arena_random.sample(pool, n)
        store.arena_problems = [{"oj": oj, "prob": prob, "ac": False} for oj, prob in picked]
        store.arena_start = _arena_time.time()
        store.arena_deadline = store.arena_start + store.arena_limit_min * 60.0
        store.arena_status = "polling"
        store.arena_last_poll = 0.0
        # 启动判题轮询线程（桌面；Web 由 tick 经代理轮询）
        if not ARENA_IS_WEB:
            renpy._arena_stop = False
            th = _arena_threading.Thread(target=_arena_poll_loop)
            th.daemon = True
            renpy._arena_thread = th
            th.start()
        return True

    # ---- 判题轮询（桌面；经 Worker /check 聚合接口一次判全套题。
    #      竞技场为限时挑战，历史 AC 不算）----
    def _arena_poll_loop():
        while not renpy._arena_stop:
            try:
                q = _arena_urlparse.urlencode({
                    "u": renpy.store.persistent.vjudge_user,
                    "since": int(store.arena_start - 5),
                    "problems": ",".join(
                        "{}-{}".format(p["oj"], p["prob"]) for p in store.arena_problems)})
                data = _arena_get(store.OJ_PROXY_BASE + "/check?" + q)
                if not data.get("ok"):
                    raise ValueError("proxy error: {}".format(data.get("error")))
                solved = set(data.get("solved", []))
                for p in store.arena_problems:
                    if not p["ac"] and "{}-{}".format(p["oj"], p["prob"]) in solved:
                        p["ac"] = True
                store.arena_status = "polling"
            except Exception:
                store.arena_status = "neterr"
            for _ in range(int(ARENA_POLL_INTERVAL * 10)):
                if renpy._arena_stop:
                    return
                _arena_time.sleep(0.1)

    def _arena_teardown():
        renpy._arena_stop = True
        renpy._arena_thread = None

    def _arena_remaining():
        return max(0.0, store.arena_deadline - _arena_time.time())

    def _arena_remaining_text():
        s = int(_arena_remaining() + 0.5)
        return "{:02d}:{:02d}:{:02d}".format(s // 3600, (s % 3600) // 60, s % 60)

    def _arena_ac_count():
        return sum(1 for p in store.arena_problems if p["ac"])

    def _arena_elapsed_text():
        s = int(_arena_time.time() - store.arena_start)
        return "{} 分 {} 秒".format(s // 60, s % 60)

    def _arena_status_text():
        st = store.arena_status
        if st == "neterr":
            return "网络异常，重试中……"
        return "判题轮询中……（每 {} 秒）".format(int(ARENA_POLL_INTERVAL))

    def _arena_open_problem(p):
        _oj_webbrowser.open("https://vjudge.net/problem/{}-{}".format(p["oj"], p["prob"]))

    def _arena_tick():
        """主界面定时器（主线程）：刷新、判胜负、轮询/恢复判题。"""
        # 调试钩子（测试用）
        dbg = getattr(renpy.store, "_arena_debug_result", None)
        if dbg:
            renpy.end_interaction(dbg)
            return
        if ARENA_IS_WEB:
            # Web：经 Worker /check 聚合判题（主线程 fetch，非后台线程）
            now = _arena_time.time()
            if now - store.arena_last_poll >= ARENA_POLL_INTERVAL:
                store.arena_last_poll = now
                wanted = [(p["oj"], p["prob"]) for p in store.arena_problems if not p["ac"]]
                if wanted:
                    solved = _oj_proxy_check(
                        persistent.vjudge_user, store.arena_start - 5, wanted)
                    if solved is None:
                        store.arena_status = "neterr"
                    else:
                        store.arena_status = "polling"
                        for p in store.arena_problems:
                            if not p["ac"] and "{}-{}".format(p["oj"], p["prob"]) in solved:
                                p["ac"] = True
        else:
            # 读档后线程丢失 -> 恢复（桌面）
            th = getattr(renpy, "_arena_thread", None)
            if th is None or not th.is_alive():
                renpy._arena_stop = False
                th = _arena_threading.Thread(target=_arena_poll_loop)
                th.daemon = True
                renpy._arena_thread = th
                th.start()
        if _arena_ac_count() >= len(store.arena_problems):
            renpy.end_interaction("win")
            return
        if _arena_remaining() <= 0:
            renpy.end_interaction("timeout")
            return
        renpy.restart_interaction()

    def _arena_fetch_tick():
        if store.arena_fetch_status != "fetching":
            renpy.end_interaction(store.arena_fetch_status)
        else:
            renpy.restart_interaction()

    def _arena_verdict():
        """按用时给一句 OI 风格评价。"""
        used = _arena_time.time() - store.arena_start
        if used < 30 * 60:
            return "神 牛 在 世 ！"
        if used < 60 * 60:
            return "稳！Au 到手软。"
        return "压线 Accepted，心跳的感觉。"

    def _arena_unsolved_text():
        uns = ["{}-{}".format(p["oj"], p["prob"]) for p in store.arena_problems if not p["ac"]]
        return "、".join(uns) if uns else "无"


# ---- 设置界面 ----
screen arena_setup_screen():
    modal True
    add Solid("#000c")

    frame:
        align (0.5, 0.5)
        padding (50, 36)
        vbox:
            spacing 18
            xalign 0.5

            text "竞技场模式" size 36 xalign 0.5
            text "随机抽题，限时挑战。全部 Accepted 即胜利！" size 18 color "#aaa" xalign 0.5

            hbox:
                spacing 16
                xalign 0.5
                text "题数" size 24 yalign 0.5
                textbutton "－" action SetVariable("arena_n", max(1, arena_n - 1)) text_size 24
                text "[arena_n]" size 24 yalign 0.5
                textbutton "＋" action SetVariable("arena_n", min(10, arena_n + 1)) text_size 24

            hbox:
                spacing 16
                xalign 0.5
                text "总时限" size 24 yalign 0.5
                textbutton "－" action SetVariable("arena_limit_min", max(30, arena_limit_min - 30)) text_size 24
                text "[arena_limit_min] 分钟" size 24 yalign 0.5
                textbutton "＋" action SetVariable("arena_limit_min", min(120, arena_limit_min + 30)) text_size 24

            hbox:
                spacing 16
                xalign 0.5
                text "vjudge 账号" size 20 yalign 0.5
                textbutton "[persistent.vjudge_user or '未设置（点击设置）']" action Show("oj_username_input") text_size 20

            hbox:
                spacing 30
                xalign 0.5
                textbutton "开始挑战" action Return("start") text_size 26
                textbutton "返回" action Return("back") text_size 26


# ---- 抽题等待界面 ----
screen arena_fetching_screen():
    modal True
    timer 0.3 repeat True action Function(_arena_fetch_tick)
    add Solid("#000c")
    frame:
        align (0.5, 0.5)
        padding (40, 30)
        vbox:
            spacing 10
            text "正在抽取题目……" size 26
            if store.arena_fetch_status == "neterr":
                text "网络异常，重试中……" size 18 color "#f88"


# ---- 竞技场主界面 ----
screen arena_screen():
    modal True
    zorder 100

    timer 0.5 repeat True action Function(_arena_tick)

    add Solid("#000d")

    frame:
        align (0.5, 0.5)
        xsize 1000
        padding (40, 30)

        vbox:
            spacing 12
            xalign 0.5

            text "竞技场" size 32 xalign 0.5

            hbox:
                spacing 40
                xalign 0.5
                text "剩余 [_arena_remaining_text()]" size 40 color ("#f66" if _arena_remaining() < 600 else "#fff") yalign 0.5
                text "AC [_arena_ac_count()]/[len(store.arena_problems)]" size 24 yalign 0.5

            text "[_arena_status_text()]" size 16 color "#aaa" xalign 0.5

            null height 6

            for i, p in enumerate(store.arena_problems):
                hbox:
                    spacing 16
                    xalign 0.5
                    if p["ac"]:
                        text "✔" size 26 color "#6f6" yalign 0.5
                    else:
                        text "✘" size 26 color "#f66" yalign 0.5
                    text "[p['oj']]-[p['prob']]" size 24 yalign 0.5
                    textbutton "打开题目页面" action Function(_arena_open_problem, p) text_size 18 yalign 0.5

            null height 10

            hbox:
                spacing 24
                xalign 0.5
                textbutton "放弃挑战" action Return("giveup") text_size 20
                textbutton "存档" action ShowMenu("save") text_size 16
                textbutton "读档" action ShowMenu("load") text_size 16
                textbutton "设置" action ShowMenu("preferences") text_size 16


# ---- 结算界面 ----
screen arena_result_screen(victory):
    modal True
    add Solid("#000d")

    frame:
        align (0.5, 0.5)
        padding (50, 36)
        vbox:
            spacing 16
            xalign 0.5

            if victory:
                text "挑 战 成 功 ！" size 44 color "#6f6" xalign 0.5
                text "全部 [len(store.arena_problems)] 题 Accepted，总用时 [_arena_elapsed_text()]" size 22 xalign 0.5
                text "[_arena_verdict()]" size 26 color "#fc6" xalign 0.5
            else:
                text "时 间 到" size 44 color "#f66" xalign 0.5
                text "战绩：AC [_arena_ac_count()]/[len(store.arena_problems)]" size 22 xalign 0.5
                if _arena_unsolved_text() != "无":
                    text "未过题：[_arena_unsolved_text()]" size 18 color "#aaa" xalign 0.5
                text "回去加训。明年今日，再战！" size 22 color "#fc6" xalign 0.5

            textbutton "返回主菜单" action Return(True) text_size 24 xalign 0.5


# ---- 主流程 ----
label arena_setup:

    scene black with dissolve
    call screen arena_setup_screen
    if _return == "back":
        return

    # 全平台判题都需要 vjudge 账号
    while not persistent.vjudge_user:
        call screen oj_username_input_modal
        if not persistent.vjudge_user:
            menu:
                "竞技场需要 vjudge 账号来自动判题。"
                "再试一次":
                    pass
                "返回主菜单":
                    return
    $ _arena_fetch_pool()
    call screen arena_fetching_screen

    $ _arena_ok = _arena_begin()
    if not _arena_ok:
        "题池为空……请检查网络后重试。（可运行 tools/harvest_pool.py 刷新内置题池）"
        return

    if store.arena_fetch_status == "fallback":
        "（实时题池获取失败或题数不足，已改用内置题池。）"

    call screen arena_screen
    $ _arena_result = _return
    $ _arena_teardown()

    call screen arena_result_screen(_arena_result == "win")
    return
