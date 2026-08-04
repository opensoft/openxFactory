// Repository selector + refresh affordance (add-dashboard-repo-selector tasks
// 3.2/3.6, and Brett's 2026-07-26 open-question rulings). The header control
// that switches the ACTIVE (repository, ref) snapshot and asks the serving side
// for fresher data.
//
// TWO same-origin backend routes, both answered by serve.py and both absent from
// a static image (which is exactly how the whole control degrades away):
//   GET  /snapshot-index.json  — the roster + per-entry freshness
//   POST /actions/refresh      — ONE affordance, the BINDING chosen by the plane
//                                (served: re-fetch; local: regenerate)
// The bundle NEVER addresses the external data source: the serving side performs
// that fetch (design D5), so the grep-proven no-external-URL boundary in
// tests/ideation-dashboard/test_renderer.py survives this change unedited.
//
// PASSIVE FRESHNESS HINT (ruling on open question 2): a background poll of the
// THIN index every POLL_INTERVAL_MS shows a "newer data available" badge when
// the source advertises a newer snapshot than the one loaded. It NEVER reloads
// by itself — the viewer clicks refresh. The poll re-uses the same index fetch,
// so no new data path appears.
//
// DOM-SAFETY: every dynamic value binds through textContent; innerHTML is never
// assigned here.

import {
  buildRoster, freshnessLabel, hintLabel, keyId, newerAvailable, parseKeyId,
  sameKey, staleNotice,
} from "./repo-selector-model.js";

export const SNAPSHOT_INDEX_ROUTE = "/snapshot-index.json";
export const ACTIONS_REFRESH_ROUTE = "/actions/refresh";
// ~5 minutes: the ruled cadence. Slow enough that the serving side's own peek
// cache absorbs N viewers, fast enough that "did my doc land?" answers itself
// while the tab is open.
export const POLL_INTERVAL_MS = 300000;

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

// Fetch the snapshot index. ANY failure (a static image 404s this route, an old
// server does not know it, file:// throws) resolves to null — the caller then
// renders exactly today's single-snapshot dashboard. Never throws.
export async function fetchIndex(injectedFetch) {
  try {
    const response = injectedFetch
      ? await injectedFetch(SNAPSHOT_INDEX_ROUTE, { cache: "no-store" })
      : await fetch(SNAPSHOT_INDEX_ROUTE, { cache: "no-store" });
    if (!response?.ok) return null;
    return await response.json();
  } catch {
    return null;
  }
}

// POST the refresh. Resolves to the backend's freshness result, or throws an
// Error carrying the backend's fixed message — the caller reports it INLINE and
// keeps the currently rendered snapshot (spec scenario "A refresh fails").
export async function postRefresh(body, injectedFetch) {
  const opts = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  };
  const response = injectedFetch
    ? await injectedFetch(ACTIONS_REFRESH_ROUTE, opts)
    : await fetch(ACTIONS_REFRESH_ROUTE, opts);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data?.message || data?.error || ("HTTP " + response.status));
  return data;
}

export function refreshCapable(caps) {
  return caps?.actions?.refresh === true;
}

export function refreshBinding(caps) {
  return caps?.refresh?.binding || null;
}

function optionLabel(option) {
  const suffix = option.available ? "" : " (unavailable)";
  const ref = option.ref && option.ref !== "main" ? " @ " + option.ref : "";
  return option.label + ref + suffix;
}

function buildSelect(roster, active, onSelect) {
  const select = el("select", "repopick");
  select.id = "repopick";
  select.setAttribute("aria-label", "active repository");
  for (const option of roster) {
    const opt = el("option", null, optionLabel(option));
    opt.value = option.id;
    if (sameKey(option, active)) opt.selected = true;
    select.appendChild(opt);
  }
  select.addEventListener("change", () => {
    const key = parseKeyId(select.value);
    if (key) onSelect(key, roster.find((o) => o.id === select.value) || null);
  });
  return select;
}

// The controller. `host` is the header slot; nothing is rendered when the index
// is absent (the static-image path) beyond whatever the caller already shows.
//
// `onSelect(key)` is the caller's "load that snapshot" hook; `onRefreshed(result)`
// runs after a successful refresh. Both `fetchIndex`/`postRefresh` are injectable
// for tests, and `schedule` replaces setInterval so the poll is testable.
export function mountRepoSelector(host, opts) {
  const o = opts || {};
  const post = o.post || postRefresh;
  const load = o.loadIndex || fetchIndex;
  let index = o.index || null;
  let active = o.active || null;
  let snapshot = o.snapshot || null;
  const caps = o.caps || {};
  const binding = refreshBinding(caps);

  const wrap = el("span", "repopicker");
  const status = el("span", "repopick-msg");
  const hint = el("button", "repohint", "");
  hint.type = "button";
  hint.hidden = true;
  hint.title = "the publication lane has newer data — click to load it";
  // Operator AT nit (2026-08-02): `title` is not a reliable accessible name,
  // and this badge ships EMPTY until `renderHint` fills it — so an assistive
  // technology meeting it mid-render would find an unnamed button. The
  // aria-label states the action independently of the visible glyph text.
  hint.setAttribute("aria-label", "load the newer published data");
  let button = null;

  function renderHint() {
    const show = newerAvailable(active, snapshot);
    hint.hidden = !show;
    if (show) hint.textContent = "◆ " + hintLabel(active);
  }

  async function runRefresh() {
    if (!button) return;
    const label = button.textContent;
    button.disabled = true;
    button.textContent = "refreshing…";
    status.textContent = "";
    try {
      const result = await post({
        repository: active?.repository, ref: active?.ref,
      });
      status.textContent = "";
      if (typeof o.onRefreshed === "function") o.onRefreshed(result);
    } catch (err) {
      // The previously rendered snapshot stays exactly as it is.
      status.textContent = "refresh failed: " + (err?.message || "error");
    } finally {
      button.disabled = false;
      button.textContent = label;
    }
  }

  if (Array.isArray(index?.entries) && index.entries.length) {
    const roster = buildRoster(index);
    if (roster.length > 1 || o.alwaysShow) {
      wrap.appendChild(buildSelect(roster, active, (key) => o.onSelect?.(key)));
    }
  }
  if (refreshCapable(caps)) {
    button = el("button", "repobtn", binding === "regenerate" ? "↻ regenerate" : "↻ refresh");
    button.type = "button";
    button.title = binding === "regenerate"
      ? "re-run the generator against this checkout (derived snapshot only)"
      : "re-fetch the published index and snapshot (read-only)";
    button.addEventListener("click", runRefresh);
    wrap.appendChild(button);
  }
  wrap.appendChild(hint);
  wrap.appendChild(status);
  hint.addEventListener("click", runRefresh);
  renderHint();
  if (host) {
    host.textContent = "";
    host.appendChild(wrap);
  }

  // The background index poll: index only, never a snapshot, never a reload.
  let timer = null;
  const schedule = o.schedule || ((fn, ms) => setInterval(fn, ms));
  async function poll() {
    const fresh = await load();
    if (!fresh) return;
    index = fresh;
    const roster = buildRoster(index);
    active = roster.find((r) => sameKey(r, active)) || active;
    renderHint();
  }
  if (o.poll !== false && refreshCapable(caps)) {
    timer = schedule(poll, o.intervalMs || POLL_INTERVAL_MS);
  }

  return {
    element: wrap,
    binding,
    poll,
    // Idempotent by design: clearing the handle is conditional, forgetting it is
    // NOT (a second stop() must stay a no-op). Braced so that reads the way it
    // runs — the one-line form said "conditional" and meant otherwise (S2681).
    stop() {
      if (timer) { clearInterval(timer); }
      timer = null;
    },
    setSnapshot(next) { snapshot = next; renderHint(); },
    setActive(next) { active = next; renderHint(); },
    refresh: runRefresh,
  };
}

// The stale banner (design D6) and the sparse-station note (D10). Rendered by
// the app shell above the views: a fallback that renders silently is the failure
// this change exists to end, so the banner is part of the contract, not chrome.
export function renderStaleBanner(host, active, sparseText) {
  if (!host) return null;
  host.textContent = "";
  const stale = staleNotice(active);
  if (!stale && !sparseText) {
    host.hidden = true;
    return null;
  }
  host.hidden = false;
  if (stale) host.appendChild(el("div", "stalebanner-line", "⚠ " + stale));
  if (sparseText) host.appendChild(el("div", "stalebanner-line sparse", "· " + sparseText));
  return host;
}

export { freshnessLabel, keyId };
