// saki-oj-proxy — Cloudflare Worker
// 浏览器(Web 版游戏) -> 本 Worker -> vjudge.net / codeforces.com / atcoder.jp / luogu.com.cn
// 解决各 OJ API 无 CORS 头导致浏览器无法直连的问题。

const VJ_STATUS = "https://vjudge.net/status/data";
const VJ_HEADERS = {
  "User-Agent": "Mozilla/5.0",
  "X-Requested-With": "XMLHttpRequest",
};
const UA_HEADERS = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" };

function corsHeaders(extra = {}) {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Max-Age": "86400",
    ...extra,
  };
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: corsHeaders({ "Content-Type": "application/json; charset=utf-8" }),
  });
}

async function vjudgeStatus(params) {
  const qs = new URLSearchParams(params).toString();
  const resp = await fetch(`${VJ_STATUS}?${qs}`, { headers: VJ_HEADERS });
  if (!resp.ok) {
    throw new Error(`vjudge responded ${resp.status}`);
  }
  return resp.json();
}

// 题目 key 形如 "POJ-2559"、"洛谷-P3406"、"51Nod-1021"
function parseProblemKey(s) {
  const i = s.indexOf("-");
  if (i <= 0 || i === s.length - 1) return null;
  return [s.slice(0, i), s.slice(i + 1)];
}

// GET /check?u=<用户>&since=<秒>&problems=<OJ-题号,...>
async function handleCheck(url) {
  const u = url.searchParams.get("u") || "";
  if (!u || u.length > 64) {
    return json({ ok: false, error: "bad u" }, 400);
  }
  let since = parseInt(url.searchParams.get("since") || "0", 10);
  if (!Number.isFinite(since) || since < 0) since = 0;

  const problemsParam = url.searchParams.get("problems") || "";
  const keys = problemsParam.split(",").filter((s) => s.length > 0 && s.length <= 64);
  if (keys.length === 0 || keys.length > 20) {
    return json({ ok: false, error: "bad problems" }, 400);
  }
  const wanted = new Map(); // "oj|prob" -> "OJ-prob" 原样
  for (const k of keys) {
    const parts = parseProblemKey(k);
    if (parts) wanted.set(`${parts[0]}|${parts[1]}`, k);
  }
  if (wanted.size === 0) {
    return json({ ok: false, error: "bad problems" }, 400);
  }

  const data = await vjudgeStatus({ draw: 1, start: 0, length: 50, un: u });
  const solved = [];
  for (const row of data.data || []) {
    if (row.status !== "Accepted") continue;
    const key = `${row.oj}|${row.probNum}`;
    if (!wanted.has(key)) continue;
    const t = (row.time || 0) / 1000.0;
    if (t >= since) solved.push(wanted.get(key));
  }
  return json({ ok: true, solved });
}

// GET /pool — 全站最近 AC 提交流去重题池（深分页被封，仅 ~120 条窗口）
async function handlePool(_url) {
  const starts = [0, 20, 50, 100];
  const results = await Promise.all(
    starts.map((start) => vjudgeStatus({ draw: 1, start, length: 20 }))
  );
  const seen = new Set();
  const pool = [];
  for (const data of results) {
    for (const row of data.data || []) {
      if (row.status !== "Accepted") continue;
      const oj = row.oj;
      const prob = String(row.probNum ?? "");
      if (!oj || !prob || prob === "None") continue;
      const key = `${oj}|${prob}`;
      if (seen.has(key)) continue;
      seen.add(key);
      pool.push({ oj, prob });
    }
  }
  return json({ ok: true, pool });
}

// GET /status?... — 通用透传到 vjudge /status/data（兜底）
async function handleStatus(url) {
  const params = {};
  for (const [k, v] of url.searchParams.entries()) params[k] = v;
  if (!params.draw) params.draw = 1;
  if (!params.start) params.start = 0;
  if (!params.length) params.length = 20;
  const data = await vjudgeStatus(params);
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: corsHeaders({ "Content-Type": "application/json; charset=utf-8" }),
  });
}

// ---------------- /profile：选手档案聚合 ----------------

const CF_SUBMISSION_SAMPLE = 10000; // user.status 取样上限（tag 统计在 Worker 端完成）

async function fetchCf(handle) {
  const infoResp = await fetch(
    `https://codeforces.com/api/user.info?handles=${encodeURIComponent(handle)}`,
    { headers: UA_HEADERS }
  );
  const info = await infoResp.json();
  if (info.status !== "OK" || !info.result || !info.result[0]) {
    return { available: false };
  }
  const u = info.result[0];

  // 提交记录 -> tag 统计（verdict==OK，按 contestId+index 去重）
  const tags = {};
  let sampled = 0;
  try {
    const stResp = await fetch(
      `https://codeforces.com/api/user.status?handle=${encodeURIComponent(handle)}&from=1&count=${CF_SUBMISSION_SAMPLE}`,
      { headers: UA_HEADERS }
    );
    const st = await stResp.json();
    if (st.status === "OK" && Array.isArray(st.result)) {
      const seen = new Set();
      for (const sub of st.result) {
        if (sub.verdict !== "OK" || !sub.problem) continue;
        const key = `${sub.problem.contestId}|${sub.problem.index}`;
        if (seen.has(key)) continue;
        seen.add(key);
        sampled++;
        for (const t of sub.problem.tags || []) {
          tags[t] = (tags[t] || 0) + 1;
        }
      }
    }
  } catch (e) {
    // tag 统计失败不阻塞 rating
  }

  return {
    available: true,
    rating: u.rating ?? null,
    maxRating: u.maxRating ?? null,
    rank: u.rank ?? null,
    maxRank: u.maxRank ?? null,
    tags,
    sampled,
  };
}

async function fetchAtcJson(user) {
  const url = `https://atcoder.jp/users/${encodeURIComponent(user)}/history/json`;
  let resp = await fetch(url, { headers: UA_HEADERS });
  if (resp.status === 403) {
    // AtCoder 封锁数据中心 IP：经 r.jina.ai 读取（返回内嵌 JSON 的 markdown）
    resp = await fetch(`https://r.jina.ai/${url}`, { headers: UA_HEADERS });
    if (resp.ok) {
      const text = await resp.text();
      const i = text.indexOf("[");
      if (i >= 0) {
        return new Response(text.slice(i), { status: 200 });
      }
    }
  }
  return resp;
}

// kenkoooo (AtCoder Problems) — 稳定的替代指标源（Rated Point Sum / AC 数）
async function fetchAtcKenkoooo(user) {
  const resp = await fetch(
    `https://kenkoooo.com/atcoder/atcoder-api/v2/user_info?user=${encodeURIComponent(user)}`,
    { headers: UA_HEADERS }
  );
  if (!resp.ok) return { available: false, debug: "kenkoooo http " + resp.status };
  const d = await resp.json();
  if (!d || !d.user_id) return { available: false, debug: "kenkoooo no user" };
  return {
    available: true,
    source: "kenkoooo",
    rating: null,
    ratedPointSum: d.rated_point_sum ?? null,
    ratedPointSumRank: d.rated_point_sum_rank ?? null,
    acceptedCount: d.accepted_count ?? null,
    acceptedCountRank: d.accepted_count_rank ?? null,
  };
}

async function fetchAtc(user) {
  // 1) 直连 / 2) r.jina.ai 回退（拿真实 rating+历史） 3) kenkoooo 兜底指标
  const resp = await fetchAtcJson(user);
  if (resp.ok) {
    try {
      const hist = await resp.json();
      if (Array.isArray(hist) && hist.length > 0) {
        const history = hist.map((h) => [h.Date, h.NewRating]);
        const latest = hist[hist.length - 1];
        let highest = 0;
        for (const h of hist) if (h.NewRating > highest) highest = h.NewRating;
        return {
          available: true,
          source: "atcoder",
          rating: latest.NewRating ?? null,
          highest,
          history,
        };
      }
    } catch (e) { /* fall through to kenkoooo */ }
  }
  return fetchAtcKenkoooo(user);
}

// Luogu 有 __client_id cookie 反爬：先取 cookie 再带 cookie 重试。
// 数据内嵌在 HTML 中（_contentOnly 的 JSON 形式对数据中心 IP 常失效），用正则提取字段。
async function luoguHttp(url, headers) {
  let resp = await fetch(url, { headers, redirect: "manual" });
  if (resp.status === 302 || resp.status === 301) {
    let cookies = [];
    try {
      cookies = resp.headers.getSetCookie().map((c) => c.split(";")[0]);
    } catch (e) {
      const sc = resp.headers.get("set-cookie");
      if (sc) cookies = sc.split(",").map((c) => c.split(";")[0]);
    }
    resp = await fetch(url, {
      headers: { ...headers, Cookie: cookies.join("; ") },
      redirect: "manual",
    });
  }
  return resp;
}

async function fetchLuogu(uid) {
  if (!/^\d+$/.test(uid)) return { available: false };
  try {
    const resp = await luoguHttp(
      `https://www.luogu.com.cn/user/${uid}?_contentOnly=1`,
      UA_HEADERS
    );
    if (!resp.ok) return { available: false, debug: "http " + resp.status };
    const text = await resp.text();

    // 优先 _contentOnly JSON
    let user = null;
    try {
      const data = JSON.parse(text);
      user = data.currentData && data.currentData.user;
    } catch (e) {
      user = null;
    }

    // 回退：从 HTML 内嵌数据提取（用户对象 "user":{...} 为扁平结构）
    let scope = text;
    const um = text.match(/"user":\{([^}]*"registerTime"[^}]*)\}/);
    if (um) scope = um[1];
    function fieldNum(name) {
      const m = scope.match(new RegExp('"' + name + '":(\\d+|null)'));
      if (!m || m[1] === "null") return null;
      return parseInt(m[1], 10);
    }
    function fieldStr(name) {
      const m = scope.match(new RegExp('"' + name + '":"((?:[^"\\\\]|\\\\.)*)"'));
      if (!m) return null;
      // 字符串中的 \uXXXX 转义需要 JSON 解码还原为汉字
      try {
        return JSON.parse('"' + m[1] + '"');
      } catch (e) {
        return m[1];
      }
    }
    const out = {
      available: true,
      name: (user && user.name) || fieldStr("name"),
      ranking: (user && user.ranking) ?? fieldNum("ranking"),
      ccfLevel: (user && user.ccfLevel) ?? fieldNum("ccfLevel"),
      passedProblemCount:
        (user && user.passedProblemCount) ?? fieldNum("passedProblemCount"),
      elo: (user && (user.eloValue ?? user.elo)) ?? fieldNum("eloValue"),
    };
    if (!out.name && out.ranking == null && out.passedProblemCount == null) {
      return { available: false, debug: "parse failed" };
    }
    return out;
  } catch (e) {
    return { available: false, debug: String(e && e.message ? e.message : e).slice(0, 120) };
  }
}

async function fetchVj(user) {
  // vjudge 无用户信息接口：只能统计最近窗口的 AC 数（注明"仅近期"）
  try {
    const data = await vjudgeStatus({ draw: 1, start: 0, length: 100, un: user });
    let ac = 0;
    const seen = new Set();
    for (const row of data.data || []) {
      if (row.status !== "Accepted") continue;
      const key = `${row.oj}|${row.probNum}`;
      if (seen.has(key)) continue;
      seen.add(key);
      ac++;
    }
    return { available: true, recentAc: ac, recentOnly: true };
  } catch (e) {
    return { available: false };
  }
}

// GET /profile?cf=<handle>&atc=<user>&luogu=<uid>&vj=<user>
async function handleProfile(url) {
  const cf = (url.searchParams.get("cf") || "").slice(0, 64);
  const atc = (url.searchParams.get("atc") || "").slice(0, 64);
  const luogu = (url.searchParams.get("luogu") || "").slice(0, 16);
  const vj = (url.searchParams.get("vj") || "").slice(0, 64);
  if (!cf && !atc && !luogu && !vj) {
    return json({ ok: false, error: "no handles given" }, 400);
  }

  const jobs = {};
  if (cf) jobs.cf = fetchCf(cf).catch(() => ({ available: false }));
  if (atc) jobs.atc = fetchAtc(atc).catch(() => ({ available: false }));
  if (luogu) jobs.luogu = fetchLuogu(luogu).catch(() => ({ available: false }));
  if (vj) jobs.vj = fetchVj(vj).catch(() => ({ available: false }));

  const names = Object.keys(jobs);
  const results = await Promise.all(names.map((n) => jobs[n]));
  const out = { ok: true };
  names.forEach((n, i) => (out[n] = results[i]));
  return json(out);
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }
    if (request.method !== "GET") {
      return json({ ok: false, error: "method not allowed" }, 405);
    }

    try {
      switch (url.pathname) {
        case "/check":
          return await handleCheck(url);
        case "/pool":
          return await handlePool(url);
        case "/status":
          return await handleStatus(url);
        case "/profile":
          return await handleProfile(url);
        default:
          return json({ ok: false, error: "not found" }, 404);
      }
    } catch (e) {
      return json({ ok: false, error: String(e && e.message ? e.message : e) }, 502);
    }
  },
};
