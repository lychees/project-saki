# -*- coding: utf-8 -*-
# 真实 OJ 提交验证系统（替代原作的 vjudge API 方案，重制版实现）
#
# 用法：
#   call oj_challenge("POJ", "2559", OJ_TIME_LIMIT, "s2_ac_1", "s2_fail_1")
# 玩家在限时内（默认 30 分钟）到真实 OJ 页面提交并通过（Accepted）后，
# 后台轮询检测到 AC → 播放 SE → 跳 pass_label；超时或点"放弃" → 跳 fail_label。
# 若检测到该账号的历史 AC（早于本次挑战开始），界面提示并允许点"我已通过"直通。

define OJ_TIME_LIMIT = 30  # 每题时间限制（分钟），集中定义便于调整

# Cloudflare Worker 代理（浏览器无法直连 vjudge API——无 CORS 头）。
# Web 端经由此代理判题；桌面竞技场也走 /check 聚合接口。
# 本地联调时临时改为 http://127.0.0.1:8787 （wrangler dev）
define OJ_PROXY_BASE = "https://saki-oj-proxy.lychees-saki.workers.dev"

default persistent.vjudge_user = ""

init python:

    import time
    import json as _oj_json
    import webbrowser as _oj_webbrowser

    # Web 平台（Pyodide/Emscripten）不支持可靠的后台线程与网络栈：
    # 桌面走后台线程直连 vjudge；Web 走 renpy.fetch -> Cloudflare Worker 代理。
    OJ_IS_WEB = renpy.variant("web")

    def _oj_proxy_check(user, since, problems):
        """通过 Worker /check 一次判一批题。
        problems: [(oj, prob), ...]；返回 {"OJ-prob", ...} 集合，出错返回 None。
        renpy.fetch 全平台可用（Web 端为浏览器 fetch，CORS 由 Worker 提供）。"""
        if not user or not problems:
            return None
        plist = ",".join("{}-{}".format(o, p) for o, p in problems)
        try:
            r = renpy.fetch(
                store.OJ_PROXY_BASE + "/check",
                params={"u": user, "since": int(since), "problems": plist},
                timeout=8, result="json")
            if r.get("ok"):
                return set(r.get("solved", []))
        except Exception:
            pass
        return None

    # ssl / urllib / threading / certifi 为桌面专用：Pyodide 没有 _ssl，
    # 顶层 import 会直接 ModuleNotFoundError，故只在非 Web 平台导入。
    if not OJ_IS_WEB:
        import threading
        import ssl as _oj_ssl
        import urllib.request as _oj_urlreq
        import urllib.parse as _oj_urlparse

        # Ren'Py 内置 Python 在 Windows 上默认找不到系统 CA 证书，
        # 使用随引擎分发的 certifi 证书库验证 HTTPS；实在没有才退化为不校验。
        try:
            import certifi as _oj_certifi
            _oj_ssl_ctx = _oj_ssl.create_default_context(cafile=_oj_certifi.where())
        except Exception:
            _oj_ssl_ctx = _oj_ssl._create_unverified_context()

    # ---- 线程私有状态（放在 renpy 模块上，绝不进 store，保证存档兼容）----
    renpy._oj_thread = None
    renpy._oj_stop = False

    OJ_POLL_INTERVAL = 12.0   # 轮询间隔（秒）
    OJ_HTTP_TIMEOUT = 10.0    # 单次请求超时（秒）

    def _oj_problem_url(oj, prob):
        return "https://vjudge.net/problem/{}-{}".format(oj, prob)

    def _oj_status_url(user, oj, prob):
        q = _oj_urlparse.urlencode({
            "draw": 1, "start": 0, "length": 20,
            "un": user, "OJId": oj, "probNum": prob,
        })
        return "https://vjudge.net/status/data?" + q

    def _oj_poll_loop(start_ts):
        """后台线程：轮询 vjudge 提交状态，结果写入可序列化的 store 变量。"""
        while not renpy._oj_stop:
            user = renpy.store.persistent.vjudge_user
            if not user:
                renpy.store._oj_status = "nouser"
            else:
                try:
                    url = _oj_status_url(user, renpy.store._oj_oj, renpy.store._oj_prob)
                    req = _oj_urlreq.Request(url, headers={
                        "User-Agent": "Mozilla/5.0",
                        "X-Requested-With": "XMLHttpRequest",
                    })
                    with _oj_urlreq.urlopen(req, timeout=OJ_HTTP_TIMEOUT, context=_oj_ssl_ctx) as r:
                        data = _oj_json.loads(r.read().decode("utf-8"))
                    new_ac = hist_ac = False
                    for row in data.get("data", []):
                        if row.get("status") == "Accepted":
                            # time 字段为毫秒时间戳；宽限 5 秒抵消时钟误差
                            if (row.get("time") or 0) / 1000.0 >= start_ts - 5:
                                new_ac = True
                            else:
                                hist_ac = True
                    if new_ac:
                        renpy.store._oj_ac = True
                        renpy.store._oj_status = "ac"
                        return
                    if hist_ac:
                        renpy.store._oj_hist_ac = True
                    renpy.store._oj_status = "polling"
                except Exception:
                    # 断网 / 超时 / 解析失败：提示并继续重试
                    renpy.store._oj_status = "neterr"
            # 可中断的睡眠
            for _ in range(int(OJ_POLL_INTERVAL * 10)):
                if renpy._oj_stop:
                    return
                time.sleep(0.1)

    def _oj_setup(oj, prob, minutes):
        """主线程调用：初始化挑战状态并启动轮询（桌面起线程；Web 由 tick 轮询代理）。"""
        renpy._oj_stop = True
        renpy._oj_thread = None
        store._oj_oj = oj
        store._oj_prob = prob
        store._oj_start = time.time()
        store._oj_deadline = time.time() + minutes * 60.0
        store._oj_ac = False
        store._oj_hist_ac = False
        store._oj_status = "polling"
        if OJ_IS_WEB:
            # Web：fetch 轮询状态（主线程 tick 驱动，非后台线程）
            store._oj_last_poll = 0.0
            store._oj_hist_checked = False
            return
        renpy._oj_stop = False
        th = threading.Thread(target=_oj_poll_loop, args=(store._oj_start,))
        th.daemon = True
        renpy._oj_thread = th
        th.start()

    def _oj_teardown():
        renpy._oj_stop = True
        renpy._oj_thread = None

    def _oj_remaining():
        return max(0.0, store._oj_deadline - time.time())

    def _oj_countdown_text():
        s = int(_oj_remaining() + 0.5)
        return "{:02d}:{:02d}".format(s // 60, s % 60)

    def _oj_status_text():
        st = store._oj_status
        if st == "ac":
            return "检测到 Accepted！"
        if st == "neterr":
            return "网络异常，正在重试……"
        if st == "nouser":
            return "未设置 vjudge 用户名，请先设置账号。"
        if store._oj_hist_ac:
            return "检测到你此前已通过此题（历史提交）。"
        return "正在轮询提交状态……（每 {} 秒刷新）".format(int(OJ_POLL_INTERVAL))

    def _oj_tick():
        """界面定时器回调（主线程）：刷新界面、判胜负、轮询/恢复判题。"""
        # 调试钩子：store._oj_debug_result 设为 "pass"/"fail" 时直接分出胜负（测试用）
        dbg = getattr(renpy.store, "_oj_debug_result", None)
        if dbg:
            renpy.end_interaction(dbg)
            return
        if OJ_IS_WEB:
            # Web：先查历史 AC（仅首开直通按钮），再按挑战开始时间判新提交
            if not store._oj_hist_checked and time.time() - store._oj_last_poll >= OJ_POLL_INTERVAL:
                store._oj_last_poll = time.time()
                solved = _oj_proxy_check(persistent.vjudge_user, 0,
                                         [(store._oj_oj, store._oj_prob)])
                store._oj_hist_checked = True
                if solved is None:
                    store._oj_status = "neterr"
                else:
                    store._oj_status = "polling"
                    key = "{}-{}".format(store._oj_oj, store._oj_prob)
                    if key in solved:
                        store._oj_hist_ac = True
            elif store._oj_hist_checked and time.time() - store._oj_last_poll >= OJ_POLL_INTERVAL:
                store._oj_last_poll = time.time()
                solved = _oj_proxy_check(persistent.vjudge_user, store._oj_start - 5,
                                         [(store._oj_oj, store._oj_prob)])
                if solved is None:
                    store._oj_status = "neterr"
                else:
                    store._oj_status = "polling"
                    key = "{}-{}".format(store._oj_oj, store._oj_prob)
                    if key in solved:
                        store._oj_ac = True
        elif not store._oj_ac and _oj_remaining() > 0:
            # 读档等情况下线程丢失且未分胜负 -> 用存档中的参数恢复轮询
            th = getattr(renpy, "_oj_thread", None)
            if th is None or not th.is_alive():
                renpy._oj_stop = False
                th = threading.Thread(target=_oj_poll_loop, args=(store._oj_start,))
                th.daemon = True
                renpy._oj_thread = th
                th.start()
        if store._oj_ac:
            renpy.end_interaction("pass")
            return
        if _oj_remaining() <= 0:
            renpy.end_interaction("fail")
            return
        renpy.restart_interaction()

    def _oj_open_problem():
        _oj_webbrowser.open(_oj_problem_url(store._oj_oj, store._oj_prob))


# ---- 用户名设置界面（首次挑战前自动弹出，也可随时从设置界面进入）----
# 注意：oj_username_input（Show 模式，Hide 关闭）用于设置/挑战/竞技场界面的
# 弹窗；oj_username_input_modal（call screen 模式）用于必须等待输入完成的
# 流程——Web 端 call screen + Hide 不会结束交互（实测踩坑），故用
# 定时器 + Return 保证返回。

screen oj_username_body(call_mode):
    vbox:
        spacing 16
        text "请输入你的 vjudge 用户名：" size 26
        text "（用于验证你的 OJ 提交；没有账号请先到 vjudge.net 注册）" size 18 color "#aaa"
        input value FieldInputValue(persistent, "vjudge_user") length 32 size 28
        if call_mode:
            textbutton "确定" action Return(False) xalign 0.5
        else:
            textbutton "确定" action Hide("oj_username_input") xalign 0.5

screen oj_username_input():
    modal True
    zorder 200
    add Solid("#000a")
    frame:
        xalign 0.5
        yalign 0.5
        padding (40, 30)
        use oj_username_body(False)

screen oj_username_input_modal():
    modal True
    zorder 200
    add Solid("#000a")
    # 注意：Web 端 call screen + Hide 不会结束交互（实测踩坑），
    # 所以「确定」必须用 Return 而非 Hide，保证 call screen 一定返回。
    frame:
        xalign 0.5
        yalign 0.5
        padding (40, 30)
        use oj_username_body(True)


# ---- OJ 挑战界面 ----
screen oj_challenge_screen():
    modal True
    zorder 100

    timer 0.5 repeat True action Function(_oj_tick)

    add Solid("#000b")

    frame:
        xalign 0.5
        yalign 0.5
        padding (50, 36)
        vbox:
            spacing 14
            xalign 0.5

            text "OJ 挑战：[store._oj_oj]-[store._oj_prob]" size 34 xalign 0.5
            text "账号：[persistent.vjudge_user]" size 18 color "#aaa" xalign 0.5

            text "剩余时间 [_oj_countdown_text()]" size 48 xalign 0.5 color ("#f66" if _oj_remaining() < 300 else "#fff")

            text "[_oj_status_text()]" size 20 xalign 0.5

            if store._oj_hist_ac and not store._oj_ac:
                text "检测到你已通过此题，可直接点击「我已通过」继续剧情。" size 18 color "#8f8" xalign 0.5

            hbox:
                spacing 20
                xalign 0.5
                textbutton "打开题目页面" action Function(_oj_open_problem) text_size 22
                # 历史 AC（任意平台）允许手动直通
                if store._oj_hist_ac:
                    textbutton "我已通过" action Return("pass") text_size 22
                textbutton "更换账号" action Show("oj_username_input") text_size 22
                textbutton "放弃挑战" action Return("fail") text_size 22

            hbox:
                spacing 20
                xalign 0.5
                textbutton "存档" action ShowMenu("save") text_size 16
                textbutton "读档" action ShowMenu("load") text_size 16
                textbutton "设置" action ShowMenu("preferences") text_size 16


# ---- 挑战主流程（可复用 label）----
# oj: OJ 名（POJ/HDU/SPOJ/ZOJ/51Nod/UVALive/LibreOJ）
# prob: 题号；time_limit_min: 限时（分钟）
# pass_label / fail_label: 通过 / 未通过跳转的 label 名（字符串）
label oj_challenge(oj, prob, time_limit_min, pass_label, fail_label):

    while not persistent.vjudge_user:
        call screen oj_username_input_modal
        if not persistent.vjudge_user:
            menu:
                "未设置 vjudge 账号，无法进行 OJ 验证。"
                "再试一次":
                    pass
                "放弃本次挑战":
                    jump expression fail_label

    $ _oj_setup(oj, prob, time_limit_min)
    call screen oj_challenge_screen
    $ _oj_result = _return
    $ _oj_teardown()

    if _oj_result == "pass":
        play sound "audio/se/ace_attorney/realization.ogg"
        jump expression pass_label
    else:
        centered "{size=28}挑战结束（未通过）。{/size}{w=1.2}{nw}"
        jump expression fail_label
