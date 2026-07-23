var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// src/index.js
var VJ_STATUS = "https://vjudge.net/status/data";
var VJ_HEADERS = {
  "User-Agent": "Mozilla/5.0",
  "X-Requested-With": "XMLHttpRequest"
};
function corsHeaders(extra = {}) {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Max-Age": "86400",
    ...extra
  };
}
__name(corsHeaders, "corsHeaders");
function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: corsHeaders({ "Content-Type": "application/json; charset=utf-8" })
  });
}
__name(json, "json");
async function vjudgeStatus(params) {
  const qs = new URLSearchParams(params).toString();
  const resp = await fetch(`${VJ_STATUS}?${qs}`, { headers: VJ_HEADERS });
  if (!resp.ok) {
    throw new Error(`vjudge responded ${resp.status}`);
  }
  return resp.json();
}
__name(vjudgeStatus, "vjudgeStatus");
function parseProblemKey(s) {
  const i = s.indexOf("-");
  if (i <= 0 || i === s.length - 1) return null;
  return [s.slice(0, i), s.slice(i + 1)];
}
__name(parseProblemKey, "parseProblemKey");
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
  const wanted = /* @__PURE__ */ new Map();
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
    const t = (row.time || 0) / 1e3;
    if (t >= since) solved.push(wanted.get(key));
  }
  return json({ ok: true, solved });
}
__name(handleCheck, "handleCheck");
async function handlePool(_url) {
  const starts = [0, 20, 50, 100];
  const results = await Promise.all(
    starts.map((start) => vjudgeStatus({ draw: 1, start, length: 20 }))
  );
  const seen = /* @__PURE__ */ new Set();
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
__name(handlePool, "handlePool");
async function handleStatus(url) {
  const params = {};
  for (const [k, v] of url.searchParams.entries()) params[k] = v;
  if (!params.draw) params.draw = 1;
  if (!params.start) params.start = 0;
  if (!params.length) params.length = 20;
  const data = await vjudgeStatus(params);
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: corsHeaders({ "Content-Type": "application/json; charset=utf-8" })
  });
}
__name(handleStatus, "handleStatus");
var src_default = {
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
  }
};

// ../.tmp/worker/node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;

// ../.tmp/worker/node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    const body = JSON.stringify(error);
    const headers = {
      "Content-Type": "application/json",
      "MF-Experimental-Error-Stack": "true"
    };
    const encoded = encodeURIComponent(body);
    if (encoded.length <= 8192) {
      headers["MF-Experimental-Error-Stack-Payload"] = encoded;
    }
    return new Response(body, { status: 500, headers });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;

// .wrangler/tmp/bundle-eVpbgq/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = src_default;

// ../.tmp/worker/node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");

// .wrangler/tmp/bundle-eVpbgq/middleware-loader.entry.ts
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  scheduledTime;
  cron;
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default as default
};
//# sourceMappingURL=index.js.map
