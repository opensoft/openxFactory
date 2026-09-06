// The HOSTED intent plane's client half - emission, the two-feed join, the
// chips, and the refusal panel's feed side (openxFactory
// add-ideation-intent-plane task 4.4; Brett Heap's rulings D-1 / Path A on
// openxFactory #656).
//
// WHAT THIS IS. On the hosted plane the dashboard has no write authority at
// all (design D16): the pod is credential-free and the gate routes it serves
// refuse everything that is not loopback. A verb therefore does not EXECUTE
// here - it EMITS a `gate-intent`, a REQUEST the apply lane revalidates
// server-side and either applies or refuses. This module owns that emission
// and the feedback loop that covers the latency between the click and the
// merged truth (design D1).
//
// TWO FEEDS, JOINED IN THE BROWSER, and it has to be the browser:
//
//   * `GET /intents?actor=&status=`  -> the intent INBOX pod. It holds what is
//     PENDING (dispatched, not yet decided) and the refusals it made itself
//     (a verb outside the actor's allowlist, refused before dispatch - those
//     never reach git at all).
//   * `GET /committed-intents.json`  -> THIS dashboard, reading the corpus
//     (ruling D-1). It holds every TERMINAL decision the apply lane committed:
//     applied, and lane-refused (stale view, target gone, engine refusal).
//
// They are different pods. The dashboard pod may not hold a credential and may
// not call the inbox on the browser's behalf (D16), and the inbox never learns
// what the lane later decided - it NEVER updates its own store after a
// successful dispatch, so every dispatched intent sits there reading "pending"
// forever. That last fact is why the join has a precedence rule rather than a
// concatenation: A COMMITTED RECORD WINS over an inbox row with the same
// identity. Without it the ordinary path - dispatch, apply, commit - would show
// a pending chip beside its own applied chip, permanently.
//
// DOM-safety: every dynamic value (actor names, refusal reasons, verbs, target
// ids) is bound through `el()`, which assigns textContent. No innerHTML with
// data, ever - the house posture, and the DOM probe asserts it mechanically.
//
// TWO-PLANE RENDERING: nothing here mutates the snapshot or anything derived
// from it. The feed decorates; the snapshot remains the only view-model source
// (the delta's Two-plane rendering requirement).

import { el } from "./helpers.js";

// The inbox, reached SAME-ORIGIN. The gateway proxies `/intents*` to the inbox
// pod and stamps the authenticated identity onto the request; the browser
// sends no credential and no actor of its own (a body-claimed actor is
// discarded by the inbox anyway).
export const INTENT_ROUTE = "/intents";
// This dashboard's own corpus read (see serve.py COMMITTED_INTENTS_ROUTE for
// why it cannot be called `/intents`).
export const COMMITTED_INTENTS_ROUTE = "/committed-intents.json";

// Poll cadence. Modest by design: the apply lane runs a GitHub workflow and
// then commits, so the interesting transition is tens of seconds away at best,
// and a hosted dashboard may have many tabs open against one small pod.
export const POLL_MS = 15000;
export const MAX_POLL_MS = 120000;   // backoff ceiling after repeated errors

// The verb's one target key - mirrored from the kernel schema and from
// intent_apply_lane.VERB_TARGET_KEY. The target object MUST carry this key and
// NOTHING else: the inbox digests the raw target it is handed while the lane
// digests the canonical one, so a stray member mints a different identity and
// silently breaks the join between a pending chip and its own outcome.
export const VERB_TARGET_KEY = {
  "demote": "change_id",
  "edit-apply": "change_id",
  "ratify": "change_id",
  "kickoff": "change_id",
  "dispose-possible": "possible_id",
  "propose": "topic_id",
  "promote-to-staging": "possible_id",
  "derive-possibles": "cluster_id",
  "research-brief": "possible_id",
  "create-project": "project_id",
  "edit-project": "project_id",
};

/** Does this plane emit intents? The negative of `gateCapable` by
 *  construction (serve.py: `intent = not loopback`), so a tray asks one
 *  question and gets one transport. */
export function intentCapable(caps) {
  return !!(caps && caps.actions && caps.actions.intent);
}

/** The display identity the feed is filtered by. DISPLAY-ONLY, exactly as the
 *  account menu reads it: it selects which rows to show, never what may be
 *  done. The inbox stamps the real actor from the ingress. */
export function feedActor(caps) {
  const hosted = caps && caps.hosted_actor;
  return typeof hosted === "string" && hosted ? hosted : null;
}

// ---- emission ---------------------------------------------------------------

/**
 * Emit ONE intent. Same-origin POST to the inbox; the body is the kernel's
 * request half and nothing more - no actor (stamped at the ingress), no
 * idempotency key (the inbox computes it, and the lane RECOMPUTES it from
 * validated fields, so a client-supplied one would be decoration a server
 * ignores).
 *
 * `snapshotRev` is the snapshot `generation.source_revision` the human was
 * LOOKING at (design D4) and must be the full revision the header renders
 * from, unabbreviated: the lane resolves an abbreviated rev to a full one
 * before digesting, so an abbreviated submission decides correctly but joins
 * wrongly.
 *
 * Returns a normalized outcome - never throws, never leaves a failure on the
 * console only:
 *   { state: "pending"|"refused"|"stalled"|"error", intent, message }
 */
export async function emitIntent(opts) {
  const o = opts || {};
  const key = VERB_TARGET_KEY[o.verb];
  if (!key) return { state: "error", message: "unknown intent verb: " + o.verb };
  if (!o.targetId) return { state: "error", message: "intent has no target" };
  if (!o.snapshotRev) {
    // Refuse LOCALLY rather than submit a request the lane must refuse: an
    // intent with no viewed revision cannot carry D4's stale-view guarantee.
    return { state: "error",
             message: "no snapshot revision on screen - reload before deciding" };
  }
  const body = {
    verb: o.verb,
    target: { [key]: o.targetId },
    snapshot_rev_seen: o.snapshotRev,
  };
  if (o.args && Object.keys(o.args).length) body.args = o.args;
  const doFetch = o.fetcher || fetch;
  let response = null;
  let payload = null;
  try {
    response = await doFetch(INTENT_ROUTE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    payload = await response.json();
  } catch (err) {
    return { state: "error",
             message: "the intent could not be submitted (" +
               ((err && err.message) || "network error") + ")" };
  }
  return readEmission(response && response.status, payload);
}

/** Pure - the inbox's response vocabulary, normalized. Separated from the
 *  transport so every branch is testable without a socket. */
export function readEmission(status, payload) {
  const p = payload && typeof payload === "object" ? payload : {};
  const intent = p.intent && typeof p.intent === "object" ? p.intent : null;
  if (intent && intent.status === "refused") {
    // The inbox's OWN refusal (403, verb outside the allowlist). It is never
    // dispatched and never committed, so this response is the only place it
    // is ever seen - it has to reach the panel now.
    return { state: "refused", intent,
             message: intent.refusal_reason || "the inbox refused this intent" };
  }
  if (intent && intent.dispatch_error) {
    // HTTP 502: recorded with status still "pending" plus a dispatch_error.
    // A status filter cannot tell this from a healthy queue, so the feed
    // gives it its own state rather than letting it read as in-flight.
    return { state: "stalled", intent,
             message: "the intent was recorded but its apply run could not be " +
               "started (" + intent.dispatch_error + ")" };
  }
  if (intent) {
    return { state: "pending", intent,
             message: p.deduplicated
               ? "already queued - this decision is waiting to apply"
               : "queued - the apply lane decides it and the feed reports back" };
  }
  const message = p.error || p.message ||
    ("the inbox rejected the intent (HTTP " + (status || "?") + ")");
  return { state: "error", message: String(message) };
}

// ---- the two-feed join ------------------------------------------------------

/** The identity a row joins on. `idempotency_key` when the servers agree on
 *  one; otherwise the tuple it is a digest of, which is what makes the join
 *  survive a digest-canonicalization difference between inbox and lane. */
export function intentKeys(row) {
  const keys = [];
  if (row && typeof row.idempotency_key === "string" && row.idempotency_key) {
    keys.push("k:" + row.idempotency_key);
  }
  const targetKey = VERB_TARGET_KEY[row && row.verb];
  const targetId = row && (row.target_id ||
    (targetKey && row.target && row.target[targetKey]));
  if (targetId) {
    keys.push(["t", row.actor || "", row.verb || "", targetId,
      row.snapshot_rev_seen || ""].join(" "));
  }
  return keys;
}

/** The instant a record is ordered by, as a NUMBER.
 *
 *  The two feeds spell RFC 3339 differently — the inbox stamps
 *  `datetime.now(timezone.utc).isoformat()` ("...+00:00") and the apply lane
 *  stamps `strftime("%Y-%m-%dT%H:%M:%SZ")` ("...Z") — and those two spellings
 *  of the SAME instant do not compare correctly as strings ("Z" sorts after
 *  "+"), so a lexical sort would always float the lane's rows above the
 *  inbox's whatever the clock said. Parsed, both are one number. An
 *  unparseable stamp sorts oldest rather than throwing. */
export function instantOf(row) {
  const raw = row.appliedAt || row.requestedAt || "";
  const at = Date.parse(raw);
  return Number.isNaN(at) ? 0 : at;
}

function normalize(row, source) {
  const targetKey = VERB_TARGET_KEY[row && row.verb];
  const targetId = row && (row.target_id ||
    (targetKey && row.target && row.target[targetKey]));
  if (!targetId) return null;
  let state = row.status === "applied" ? "applied"
    : row.status === "refused" ? "refused" : "pending";
  if (source === "inbox" && row.dispatch_error) state = "stalled";
  return {
    source,
    state,
    actor: typeof row.actor === "string" ? row.actor : "",
    verb: row.verb,
    targetId,
    requestedAt: typeof row.requested_at === "string" ? row.requested_at : "",
    appliedAt: typeof row.applied_at === "string" ? row.applied_at : "",
    reason: typeof row.refusal_reason === "string" ? row.refusal_reason
      : (row.dispatch_error ? String(row.dispatch_error) : ""),
    record: typeof row.applied_record === "string" ? row.applied_record : "",
    outcome: (row.args && typeof row.args.outcome === "string")
      ? row.args.outcome : "",
    keys: intentKeys(row),
  };
}

function withInstant(rec) {
  rec.at = instantOf(rec);
  return rec;
}

/**
 * Join the inbox rows with the committed rows. Pure, so the precedence rule is
 * testable without a server.
 *
 * THE RULE: a committed (corpus) record wins over any inbox row sharing an
 * identity, because the inbox never learns the outcome and would otherwise
 * report "pending" forever for every intent that actually applied.
 */
export function mergeFeeds(inboxRows, committedRows) {
  const merged = [];
  const claimed = new Set();
  for (const row of committedRows || []) {
    const rec = normalize(row, "corpus");
    if (!rec) continue;
    for (const k of rec.keys) claimed.add(k);
    merged.push(withInstant(rec));
  }
  for (const row of inboxRows || []) {
    const rec = normalize(row, "inbox");
    if (!rec) continue;
    if (rec.keys.some((k) => claimed.has(k))) continue;   // decided already
    for (const k of rec.keys) claimed.add(k);
    merged.push(withInstant(rec));
  }
  merged.sort((a, b) => b.at - a.at);                     // newest first
  return merged;
}

/** The one state a tile shows: the newest record for that target. */
export function stateFor(rows, targetId) {
  for (const rec of rows || []) if (rec.targetId === targetId) return rec.state;
  return null;
}

/** The same answer for EVERY target at once, built ONCE per feed update.
 *  The wheel decorates its tiles on every animation frame, so a per-tile scan
 *  of the feed would be an O(tiles x rows) cost inside the draw loop. Rows
 *  arrive newest-first, so the first entry for a target wins. */
export function statesByTarget(rows) {
  const states = new Map();
  for (const rec of rows || []) {
    if (!states.has(rec.targetId)) states.set(rec.targetId, rec.state);
  }
  return states;
}

// ---- the live feed ----------------------------------------------------------

const CHIP_LABEL = {
  pending: "pending",
  applied: "applied",
  refused: "refused",
  stalled: "stalled",
};

const CHIP_TITLE = {
  pending: "submitted - the apply lane decides it; the snapshot is unchanged " +
    "until the decision is baked",
  applied: "applied and committed by the apply lane (the snapshot catches up " +
    "at the next bake)",
  refused: "refused - the reason is in the gate console panel",
  stalled: "recorded, but its apply run could not be started",
};

/**
 * Start polling both feeds. Returns a controller:
 *   { stop(), refresh(), rows(), error(), subscribe(fn) }
 *
 * ERRORS ARE STATE, NOT SILENCE. A failing feed sets `error()` (which the
 * chips render), notifies subscribers, and backs the interval off toward
 * MAX_POLL_MS; a success clears it and restores the cadence. Nothing is
 * swallowed to the console.
 */
export function startIntentFeed(opts) {
  const o = opts || {};
  const doFetch = o.fetcher || fetch;
  const base = Math.max(1000, o.intervalMs || POLL_MS);
  const timer = o.timer || ((fn, ms) => setTimeout(fn, ms));
  const clear = o.clearTimer || ((h) => clearTimeout(h));
  const subscribers = [];
  let rows = [];
  let error = null;
  let handle = null;
  let stopped = false;
  let wait = base;
  const seen = new Set();     // refusals already sent to the panel, by identity

  async function readJson(route) {
    const response = await doFetch(route,
      { headers: { Accept: "application/json" } });
    if (response && response.ok === false) {
      throw new Error("HTTP " + response.status);
    }
    return await response.json();
  }

  function announce() {
    // Every refusal is visible ONCE (the delta: never silently dropped), and
    // the panel is a log, not a live view - so a repeat poll must not re-file
    // a refusal it already filed.
    if (o.onRefusal) {
      for (const rec of rows) {
        if (rec.state !== "refused" && rec.state !== "stalled") continue;
        const id = rec.keys[0] || (rec.verb + " " + rec.targetId);
        if (seen.has(id)) continue;
        seen.add(id);
        o.onRefusal(rec);
      }
    }
    for (const fn of subscribers) fn(rows, error);
  }

  async function poll() {
    if (stopped) return;
    try {
      const query = o.actor ? "?actor=" + encodeURIComponent(o.actor) : "";
      const [inbox, corpus] = await Promise.all([
        readJson(INTENT_ROUTE + query),
        readJson(COMMITTED_INTENTS_ROUTE + query),
      ]);
      rows = mergeFeeds((inbox && inbox.intents) || [],
                        (corpus && corpus.intents) || []);
      error = null;
      wait = base;
    } catch (err) {
      error = (err && err.message) || "the intent feed is unreachable";
      wait = Math.min(wait * 2, MAX_POLL_MS);
    }
    // A SUBSCRIBER'S failure must not stop the poll loop. `announce` calls
    // into rendering, and a render that throws used to take the rescheduling
    // line below with it — the overlay would then freeze on whatever it last
    // drew, silently and permanently, which is the one failure mode this feed
    // exists to prevent. It becomes feed state like any other error instead.
    try {
      announce();
    } catch (err) {
      error = "the intent overlay could not render (" +
        ((err && err.message) || "error") + ")";
    }
    if (!stopped) handle = timer(poll, wait);
  }

  handle = timer(poll, 0);
  return {
    stop() { stopped = true; if (handle != null) clear(handle); },
    refresh() { return poll(); },
    rows() { return rows; },
    error() { return error; },
    subscribe(fn) {
      subscribers.push(fn);
      return () => {
        const at = subscribers.indexOf(fn);
        if (at >= 0) subscribers.splice(at, 1);
      };
    },
  };
}

// ---- the overlay ------------------------------------------------------------

/** One chip. `el` binds text via textContent, so a reason carrying markup is
 *  a reason, never an element. */
export function intentChip(rec) {
  const chip = el("span", "intentchip intentchip-" + rec.state,
    CHIP_LABEL[rec.state] || rec.state);
  chip.dataset.intentState = rec.state;
  chip.dataset.intentTarget = rec.targetId;
  const detail = [rec.verb, rec.outcome, rec.actor].filter(Boolean).join(" / ");
  chip.title = (CHIP_TITLE[rec.state] || rec.state) +
    (detail ? " - " + detail : "");
  return chip;
}

/**
 * Render the chips for ONE target into `container`, replacing whatever was
 * there. `rows` is a merged feed; `error` renders as its own chip so an
 * unreachable feed reads as unknown rather than as "nothing happened".
 */
export function renderIntentChips(container, targetId, rows, error) {
  container.textContent = "";
  if (error) {
    const chip = el("span", "intentchip intentchip-error", "feed unavailable");
    chip.title = "the intent feed could not be read: " + error;
    container.appendChild(chip);
    return container;
  }
  const mine = (rows || []).filter((r) => r.targetId === targetId);
  if (!mine.length) return container;
  for (const rec of mine.slice(0, 3)) container.appendChild(intentChip(rec));
  return container;
}

/** The feed's line for the refusal panel: verb, target and the reason, as
 *  text. */
export function refusalLine(rec) {
  const head = rec.targetId + " -> " + rec.verb +
    (rec.state === "stalled" ? " not started" : " refused");
  return rec.reason ? head + ": " + rec.reason : head;
}
