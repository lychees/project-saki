// saki-oj-proxy — Cloudflare Worker
// 浏览器(Web 版游戏) -> 本 Worker -> vjudge.net
// 解决 vjudge API 无 CORS 头导致浏览器无法直连的问题。

const VJ_STATUS = "https://vjudge.net/status/data";
const VJ_HEADERS = {
  "User-Agent": "Mozilla/5.0",
  "X-Requested-With": "XMLHttpRequest",
};

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
        default:
          return json({ ok: false, error: "not found" }, 404);
      }
    } catch (e) {
      return json({ ok: false, error: String(e && e.message ? e.message : e) }, 502);
    }
  },
};
