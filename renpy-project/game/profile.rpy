# -*- coding: utf-8 -*-
# 选手档案：绑定 AtCoder / Codeforces / Luogu / vjudge 账号，
# 经 Worker /profile 聚合查询，显示 rating 卡片（按段位着色）+ 技能雷达图。
# 数据缓存于 persistent（带时间戳），刷新按钮手动更新。

# 账号绑定（persistent）
default persistent.cf_user = ""
default persistent.atc_user = ""
default persistent.luogu_user = ""
# vjudge 用户名沿用 persistent.vjudge_user（oj.rpy）

# 查询缓存
default persistent.profile_data = None
default persistent.profile_time = 0.0

init python:

    import time as _prof_time
    import math as _prof_math

    PROFILE_IS_WEB = renpy.variant("web")

    if not PROFILE_IS_WEB:
        import threading as _prof_threading

    renpy._prof_thread = None
    renpy._prof_stop = False

    # ---- 段位配色 ----
    def _cf_color(r):
        if r is None:
            return "#888888"
        if r < 1200:
            return "#808080"
        if r < 1400:
            return "#008000"
        if r < 1600:
            return "#03a89e"
        if r < 1900:
            return "#0000ff"
        if r < 2100:
            return "#aa00aa"
        if r < 2400:
            return "#ff8c00"
        return "#ff0000"

    def _atc_color(r):
        if r is None:
            return "#888888"
        if r < 400:
            return "#808080"
        if r < 800:
            return "#804000"
        if r < 1200:
            return "#008000"
        if r < 1600:
            return "#00c0c0"
        if r < 2000:
            return "#0000ff"
        if r < 2400:
            return "#c0c000"
        if r < 2800:
            return "#ff8000"
        return "#ff0000"

    # ---- CF tag -> 技能轴映射 ----
    RADAR_AXES = ["数学", "动态规划", "图论", "贪心", "搜索", "数据结构", "字符串", "暴力模拟"]
    RADAR_TAG_MAP = {
        "数学": ["math", "number theory", "combinatorics", "probabilities", "geometry", "matrices"],
        "动态规划": ["dp"],
        "图论": ["graphs", "trees", "flows", "graph matchings", "shortest paths"],
        "贪心": ["greedy"],
        "搜索": ["dfs and similar", "binary search", "two pointers", "meet in the middle", "ternary search"],
        "数据结构": ["data structures", "dsu"],
        "字符串": ["strings", "string suffix structures", "hashing", "palindromes"],
        "暴力模拟": ["brute force", "implementation", "constructive algorithms", "simulation"],
    }

    def _radar_level(count):
        if count <= 0:
            return 0
        if count <= 2:
            return 1
        if count <= 6:
            return 2
        if count <= 15:
            return 3
        if count <= 30:
            return 4
        return 5

    def _profile_radar_levels():
        """从缓存的 CF tag 统计计算 8 轴等级（0~5）。"""
        d = persistent.profile_data or {}
        cf = d.get("cf") or {}
        tags = cf.get("tags") or {}
        levels = []
        for axis in RADAR_AXES:
            n = sum(tags.get(t, 0) for t in RADAR_TAG_MAP[axis])
            levels.append(_radar_level(n))
        return levels

    def _profile_bound_any():
        return bool(persistent.cf_user or persistent.atc_user
                    or persistent.luogu_user or persistent.vjudge_user)

    def _profile_params():
        p = {}
        if persistent.cf_user:
            p["cf"] = persistent.cf_user
        if persistent.atc_user:
            p["atc"] = persistent.atc_user
        if persistent.luogu_user:
            p["luogu"] = persistent.luogu_user
        if persistent.vjudge_user:
            p["vj"] = persistent.vjudge_user
        return p

    # ---- 查询（桌面后台线程 / Web renpy.fetch 同步）----
    def _prof_fetch_worker():
        try:
            r = renpy.fetch(store.OJ_PROXY_BASE + "/profile",
                            params=_profile_params(), timeout=15, result="json")
            if r.get("ok"):
                persistent.profile_data = r
                persistent.profile_time = _prof_time.time()
                store.profile_status = "ok"
            else:
                store.profile_status = "neterr"
        except Exception:
            store.profile_status = "neterr"

    def _profile_refresh():
        if PROFILE_IS_WEB:
            store.profile_status = "fetching"
            _prof_fetch_worker()  # 非交互上下文同步执行，不卡帧
        else:
            store.profile_status = "fetching"
            renpy._prof_stop = False
            th = _prof_threading.Thread(target=_prof_fetch_worker)
            th.daemon = True
            renpy._prof_thread = th
            th.start()

    def _profile_status_text():
        st = getattr(store, "profile_status", "")
        if st == "fetching":
            return "查询中……"
        if st == "neterr":
            return "网络异常，显示的是缓存数据（可点刷新重试）"
        if persistent.profile_time:
            return "更新于 " + _prof_time.strftime("%Y-%m-%d %H:%M",
                                                   _prof_time.localtime(persistent.profile_time))
        return ""

    def _prof_status_tick():
        # 查询状态刷新（桌面线程完成后重绘界面）
        renpy.restart_interaction()

    def _profile_home_url(platform, handle):
        """平台个人主页 URL。"""
        if platform == "cf":
            return "https://codeforces.com/profile/" + handle
        if platform == "atc":
            return "https://atcoder.jp/users/" + handle
        if platform == "luogu":
            return "https://www.luogu.com.cn/user/" + handle
        if platform == "vj":
            return "https://vjudge.net/user/" + handle
        return "https://vjudge.net"

    # ---- 技能雷达图（Creator-Defined Displayable，参照竞赛数据面板风格）----
    class ProfileRadar(renpy.Displayable):

        def __init__(self, levels, size=360, **kwargs):
            super(ProfileRadar, self).__init__(**kwargs)
            self.levels = list(levels)
            self.size = size

        def render(self, w, h, st, at):
            s = self.size
            r = renpy.Render(s, s)
            c = r.canvas()
            cx = cy = s / 2.0
            R = s / 2.0 - 18
            n = len(self.levels)

            def pt(i, frac):
                ang = -_prof_math.pi / 2 + 2 * _prof_math.pi * (i % n) / n
                return (cx + R * frac * _prof_math.cos(ang),
                        cy + R * frac * _prof_math.sin(ang))

            # 等级环（1~5 层虚线多边形）
            for L in range(1, 6):
                frac = L / 5.0
                col = "#3a4a5a" if L < 5 else "#4a6a7a"
                for i in range(n):
                    p1 = pt(i, frac)
                    p2 = pt(i + 1 if i + 1 < n else 0, frac)
                    for a in range(3):  # 3 段画 2 段形成虚线
                        if a == 1:
                            continue
                        t0, t1 = a / 3.0, (a + 1) / 3.0
                        q1 = (p1[0] + (p2[0] - p1[0]) * t0,
                              p1[1] + (p2[1] - p1[1]) * t0)
                        q2 = (p1[0] + (p2[0] - p1[0]) * t1,
                              p1[1] + (p2[1] - p1[1]) * t1)
                        c.line(col, q1, q2, 1)

            # 轴线
            for i in range(n):
                c.line("#3a4a5a", (cx, cy), pt(i, 1.0), 1)

            # 技能多边形（半透明填充 + 实线描边 + 顶点）
            pts = [pt(i, max(0.05, lv / 5.0)) for i, lv in enumerate(self.levels)]
            c.polygon("#33ccff44", pts, 0)
            c.polygon("#33ccff", pts, 2)
            for p in pts:
                c.circle("#66ddff", (int(p[0]), int(p[1])), 3, 0)
            return r

    def _radar_label_pos(i, size=360):
        """第 i 个轴标签的位置（相对雷达框左上角，含外扩边距）。"""
        n = len(RADAR_AXES)
        ang = -_prof_math.pi / 2 + 2 * _prof_math.pi * (i % n) / n
        R = size / 2.0 + 6
        cx = cy = size / 2.0
        return (int(cx + R * _prof_math.cos(ang)),
                int(cy + R * _prof_math.sin(ang)))


# ---- 通用账号输入弹窗（Show 模式）----
screen account_input(title, field, note=""):
    modal True
    zorder 210
    add Solid("#000a")
    frame:
        xalign 0.5
        yalign 0.5
        padding (40, 30)
        vbox:
            spacing 14
            text "[title]" size 26
            if note:
                text "[note]" size 16 color "#aaa"
            input value FieldInputValue(persistent, field) length 32 size 28
            textbutton "确定" action Hide("account_input") xalign 0.5


# ---- 账号绑定面板 ----
screen account_binding():
    modal True
    zorder 200
    add Solid("#000c")

    frame:
        align (0.5, 0.5)
        padding (46, 34)
        vbox:
            spacing 16
            xalign 0.5

            text "账号绑定" size 32 xalign 0.5
            text "绑定后可在「选手档案」查看各平台 rating 与技能雷达" size 16 color "#aaa" xalign 0.5

            for label, field, note in [
                    ("Codeforces", "cf_user", "handle，如 tourist"),
                    ("AtCoder", "atc_user", "用户名，如 chokudai"),
                    ("Luogu", "luogu_user", "数字 UID（个人主页 URL 里的数字）"),
                    ("vjudge", "vjudge_user", "用户名")]:
                hbox:
                    spacing 18
                    xalign 0.5
                    text "[label]" size 22 yalign 0.5
                    text "[getattr(persistent, field) or '未绑定']" size 20 color "#8fc" yalign 0.5
                    textbutton ("修改" if getattr(persistent, field) else "绑定"):
                        action Show("account_input", title=label, field=field, note=note)
                        text_size 20
                        yalign 0.5

            textbutton "关闭" action Hide("account_binding") text_size 22 xalign 0.5


# ---- 选手档案主面板 ----
# 卡片头部的账号链接（可点击跳转平台主页；空账号不可点）
screen profile_platform_link(platform, handle):
    if handle:
        textbutton handle:
            action Function(_oj_webbrowser.open, _profile_home_url(platform, handle))
            text_size 16
            text_underline True
            text_idle_color "#8fc"
            text_hover_color "#66ccff"
    else:
        text "未绑定" size 16 color "#666"


screen profile_card(title, body_lines, platform=None, handle="", accent="#33ccff"):
    frame:
        xsize 268
        ysize 152
        background Solid("#141a24")
        padding (16, 12)
        vbox:
            spacing 6
            hbox:
                spacing 8
                text title size 18 color "#9ab" yalign 0.5
                if platform:
                    text "·" size 18 color "#9ab" yalign 0.5
                    use profile_platform_link(platform, handle)
            for txt, col, sz in body_lines:
                text txt size sz color col


screen player_profile_screen():
    modal True
    add Solid("#0d1117")

    timer 1.0 repeat True action Function(_prof_status_tick)

    $ _pd = persistent.profile_data or {}
    $ _cf = _pd.get("cf") or {}
    $ _atc = _pd.get("atc") or {}
    $ _lg = _pd.get("luogu") or {}
    $ _vj = _pd.get("vj") or {}

    vbox:
        xalign 0.5
        ypos 24
        spacing 16

        hbox:
            xalign 0.5
            spacing 30
            text "选手档案" size 34
            textbutton "刷新" action Return("refresh") text_size 22 yalign 0.6
            textbutton "账号绑定" action Show("account_binding") text_size 22 yalign 0.6
            textbutton "返回主菜单" action Return("back") text_size 22 yalign 0.6

        text "[_profile_status_text()]" size 16 color "#fa8" xalign 0.5

        # rating 卡片区
        hbox:
            xalign 0.5
            spacing 14

            if _cf.get("available"):
                use profile_card("Codeforces", platform="cf", handle=persistent.cf_user, body_lines=[
                    ("rating", "#9ab", 16),
                    (str(_cf.get("rating")), _cf_color(_cf.get("rating")), 40),
                    ("max " + str(_cf.get("maxRating")) + "  " + str(_cf.get("rank")), "#9ab", 15)])
            else:
                use profile_card("Codeforces", platform="cf", handle=persistent.cf_user, body_lines=[
                    ("暂未获取", "#888", 24),
                    (persistent.cf_user or "未绑定", "#666", 15)])

            if _atc.get("available") and _atc.get("rating") is not None:
                use profile_card("AtCoder", platform="atc", handle=persistent.atc_user, body_lines=[
                    ("rating", "#9ab", 16),
                    (str(_atc.get("rating")), _atc_color(_atc.get("rating")), 40),
                    ("highest " + str(_atc.get("highest")), "#9ab", 15)])
            elif _atc.get("available"):
                # kenkoooo 兜底指标（atcoder.jp 不可达时保证有数据）
                use profile_card("AtCoder", platform="atc", handle=persistent.atc_user, body_lines=[
                    ("Rated Point Sum", "#9ab", 15),
                    (str(_atc.get("ratedPointSum")), "#13c2c2", 36),
                    ("AC " + str(_atc.get("acceptedCount")) + " (rank " + str(_atc.get("acceptedCountRank")) + ")", "#9ab", 15)])
            else:
                use profile_card("AtCoder", platform="atc", handle=persistent.atc_user, body_lines=[
                    ("暂未获取", "#888", 24),
                    (persistent.atc_user or "未绑定", "#666", 15)])

            if _lg.get("available"):
                use profile_card("Luogu", platform="luogu", handle=persistent.luogu_user, body_lines=[
                    (str(_lg.get("name")), "#8fc", 20),
                    ("Lv." + str(_lg.get("ccfLevel")), "#13c2c2", 36),
                    ("排名 " + str(_lg.get("ranking")) + "  通过 " + (str(_lg.get("passedProblemCount")) if _lg.get("passedProblemCount") is not None else "—"), "#9ab", 15)])
            else:
                use profile_card("Luogu", platform="luogu", handle=persistent.luogu_user, body_lines=[
                    ("暂未获取", "#888", 24),
                    (persistent.luogu_user or "未绑定", "#666", 15)])

            if _vj.get("available"):
                use profile_card("vjudge", platform="vj", handle=persistent.vjudge_user, body_lines=[
                    ("近期活跃（近 100 提交）", "#9ab", 15),
                    ("AC " + str(_vj.get("recentAc")), "#33ccff", 40),
                    ("仅近期窗口统计", "#666", 14)])
            else:
                use profile_card("vjudge", platform="vj", handle=persistent.vjudge_user, body_lines=[
                    ("暂未获取", "#888", 24),
                    (persistent.vjudge_user or "未绑定", "#666", 15)])

        # 雷达 + tag 明细
        hbox:
            xalign 0.5
            spacing 80

            if _cf.get("available") and _cf.get("tags"):
                $ _levels = _profile_radar_levels()
                fixed:
                    xsize 380
                    ysize 400
                    add ProfileRadar(_levels, 360) pos (10, 20)
                    for i, axis in enumerate(RADAR_AXES):
                        $ _lx, _ly = _radar_label_pos(i, 360)
                        text "[axis] Lv.[_levels[i]]":
                            size 15
                            color ("#33ccff" if _levels[i] > 0 else "#556")
                            pos (_lx + 10, _ly + 20)
                            anchor (0.5, 0.5)
            else:
                frame:
                    xsize 380
                    ysize 400
                    background Solid("#141a24")
                    text "绑定 Codeforces 账号后\n显示技能雷达图" size 18 color "#667" align (0.5, 0.5) text_align 0.5

            if _cf.get("available") and _cf.get("tags"):
                vbox:
                    spacing 4
                    text "CF 标签 AC 数 TOP10（取样 [_cf.get('sampled')] 题）" size 15 color "#9ab"
                    $ _top = sorted(_cf["tags"].items(), key=lambda kv: -kv[1])[:10]
                    for _tag, _cnt in _top:
                        text "{}: {}".format(_tag, _cnt) size 15 color "#8ab"


# ---- 空状态引导 ----
screen profile_empty_screen():
    modal True
    add Solid("#0d1117")

    # 绑定完成后自动进入主面板（Show 模式的绑定面板不阻塞此界面）
    timer 0.5 repeat True action If(_profile_bound_any(), true=Return("bound"), false=NullAction())

    frame:
        align (0.5, 0.5)
        padding (50, 36)
        vbox:
            spacing 18
            xalign 0.5
            text "选手档案" size 32 xalign 0.5
            text "还没有绑定任何竞赛平台账号。\n绑定 Codeforces / AtCoder / Luogu / vjudge 后，\n这里会显示你的 rating 和技能雷达图。" size 18 color "#9ab" xalign 0.5 text_align 0.5
            textbutton "去绑定" action Show("account_binding") text_size 24 xalign 0.5
            textbutton "返回主菜单" action Return(True) text_size 20 xalign 0.5


label player_profile:
    scene black with dissolve

    if not _profile_bound_any():
        call screen profile_empty_screen
        if _return != "bound":
            return

    label player_profile_main:
        if not persistent.profile_data:
            $ _profile_refresh()
        call screen player_profile_screen
        if _return == "refresh":
            $ _profile_refresh()
            jump player_profile_main
    return
