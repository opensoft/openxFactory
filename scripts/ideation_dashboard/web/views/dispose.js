// Dispose tray + refusal panel — the LOCAL action center's first verb
// (openxFactory add-ideation-intent-plane §3, design D5 local-first; the
// hosted intent plane later swaps the transport, not this UI).
//
// The tray mounts on a pending_review possible tile when the capability
// probe reports `actions.gate` (loopback bind + real checkout + resolved
// actor — the deployed image never qualifies). Accept / reject / defer POST
// to `/actions/gate/dispose-possible`; reject collects the REQUIRED reason
// and citation first (the register kernel's uncited-rejection rule — the
// engine refuses without them, and that refusal renders in the panel).
//
// TWO TRANSPORTS, ONE TRAY (add-ideation-intent-plane task 4.4, design D5:
// "the identical tray then targets the intent API when hosted"). `opts.intent`
// selects the HOSTED transport: the click emits a `gate-intent` to the inbox
// instead of executing, and the tray shows the feed's chips for this target
// beside the buttons. Absent `opts.intent` NOTHING about the local path
// changes — same route, same body, same panel entries, same overlay.
//
// DOM-safety: every dynamic value is bound via textContent — refusal
// messages from the engine included — never innerHTML (the house posture).
// Two-plane rendering: a successful disposition NEVER mutates the
// snapshot-derived model; it lands in the local `applied` overlay the wheel
// consults, and the tile shows the verdict with a regenerate hint.

import { el } from "./helpers.js";
import { emitIntent, renderIntentChips } from "./intent-feed.js";

export const GATE_DISPOSE_ROUTE = "/actions/gate/dispose-possible";
export const GATE_PROPOSE_ROUTE = "/actions/gate/propose";

// verdict -> { label, needsCitation }
const VERDICTS = [
  { outcome: "accepted", label: "✓ accept", title: "becomes first-class latent backlog (keeps ai-derived provenance)" },
  { outcome: "rejected", label: "✕ reject", title: "closes it with a required reason + citation; never silently re-derived" },
  { outcome: "deferred", label: "◔ defer", title: "parks it; the only re-disposable outcome" },
];

// The session-local applied overlay: possible id -> outcome. Snapshot stays
// deterministic; views consult this to decorate tiles until a regenerate.
const applied = new Map();

export function appliedOutcome(possibleId) {
  return applied.get(possibleId) || null;
}

export function gateCapable(caps) {
  return !!(caps && caps.actions && caps.actions.gate);
}

// ---- refusal panel (one per page; every refusal is visible, never silent) --

let panel = null;

function ensurePanel() {
  if (panel && document.body.contains(panel)) return panel;
  panel = el("aside", "refusalpanel");
  panel.hidden = true;
  const head = el("header", "refusalpanel-head");
  head.appendChild(el("span", "refusalpanel-title", "gate console"));
  const clear = el("button", "refusalpanel-clear", "clear");
  clear.type = "button";
  clear.addEventListener("click", () => {
    list.innerHTML = "";
    panel.hidden = true;
  });
  head.appendChild(clear);
  const list = el("ul", "refusalpanel-list");
  panel.append(head, list);
  document.body.appendChild(panel);
  return panel;
}

// The panel's vocabulary. "ok"/"refused" are the LOCAL executing plane's two
// outcomes and are unchanged; the other three are the hosted plane's, because a
// submitted intent is neither applied nor refused yet and calling it either
// would be a lie the human acts on (design D1: the click is the decision, the
// apply is the custody step behind it).
//
// THE HOSTED PLANE HAS FOUR OUTCOMES, NOT TWO, and the panel must be able to
// SAY each of them. `emitIntent` normalizes the inbox's responses to
// pending | refused | stalled | error, and the last two are not refusals:
//   * "stalled" (HTTP 502) - the intent WAS recorded and the apply run could
//     not be started. Labelling it "refused" tells the human their decision was
//     rejected when in fact it is on file and undecided, so they re-submit a
//     decision that is already queued.
//   * "error" (401 / 429 / 400, or an unreachable inbox) - NOTHING was
//     recorded. Labelling that "refused" is the opposite lie: it reads as a
//     server verdict on the decision when the decision never arrived, so the
//     human does NOT re-submit the thing that never got sent.
const PANEL_KIND = {
  ok: { label: "applied", cls: "is-ok" },
  queued: { label: "queued", cls: "is-queued" },
  stalled: { label: "stalled", cls: "is-stalled" },
  error: { label: "not sent", cls: "is-error" },
  refused: { label: "refused", cls: "is-refused" },
};

// `emitIntent`/`readEmission` state -> the panel's word for it. Unknown states
// fall back to "refused", the conservative reading (something went wrong and
// the human must look), which is also what the whole map used to collapse to.
export const EMISSION_PANEL_KIND = {
  pending: "queued",
  refused: "refused",
  stalled: "stalled",
  error: "error",
};

export function panelEntry(kind, message) {
  const host = ensurePanel();
  const list = host.querySelector(".refusalpanel-list");
  const shape = PANEL_KIND[kind] || PANEL_KIND.refused;
  const item = el("li", "refusalpanel-item " + shape.cls);
  item.appendChild(el("span", "refusalpanel-kind", shape.label));
  item.appendChild(el("span", "refusalpanel-msg", message));
  list.insertBefore(item, list.firstChild);
  host.hidden = false;
}

// ---- the tray ---------------------------------------------------------------

async function post(route, body, fetcher) {
  const doFetch = fetcher || fetch;
  const response = await doFetch(route, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = { ok: false, message: "malformed response (HTTP " + response.status + ")" };
  }
  return payload;
}

// Collect reason + citation for a rejection. window.prompt keeps v1 honest
// and tiny; a refusal for an empty value is the engine's job, surfaced in
// the panel like every other refusal.
function collectRejection() {
  const reason = window.prompt("Rejection REASON (required — the durable why):", "");
  if (reason === null) return null; // cancelled
  const citation = window.prompt("Rejection CITATION (required — what the rejection cites):", "");
  if (citation === null) return null;
  return { reason, citation };
}

// Mount the tray for one pending possible into `container`. `opts.fetcher`
// and `opts.collect` are test seams; `opts.onApplied(outcome)` lets the view
// refresh its overlay.
//
// `opts.intent` present => THE HOSTED TRANSPORT (task 4.4). It carries
// `{ snapshotRev, rows, error, emit? }`: the revision the human is looking at
// (design D4's `snapshot_rev_seen`), the merged feed rows and error this
// render saw, and an optional emitter seam. The verdict buttons then submit a
// request instead of performing an act, and the chips for this target render
// beside them from the rows handed in — the tray subscribes to nothing and
// owns no timer, so a rail redraw can never leak one.
export function mountDisposeTray(container, possible, opts) {
  const o = opts || {};
  const intent = o.intent || null;
  const tray = el("span", "disposetray");
  for (const v of VERDICTS) {
    const btn = el("button", "disposebtn dispose-" + v.outcome, v.label);
    btn.type = "button";
    btn.title = intent
      ? v.title + " (hosted: this submits an intent the apply lane decides)"
      : v.title;
    btn.addEventListener("click", async (ev) => {
      ev.stopPropagation();
      const body = { possible_id: possible.id, outcome: v.outcome };
      if (v.outcome === "rejected") {
        const extra = (o.collect || collectRejection)();
        if (extra === null) return; // human cancelled
        body.reason = extra.reason;
        body.citation = extra.citation;
      }
      tray.classList.add("is-busy");
      if (intent) {
        // The kernel forbids a target key inside `args` (the validated target
        // is the only target — intent_apply_lane.shape_error), so the verb's
        // arguments travel WITHOUT `possible_id`.
        const { possible_id: _target, ...args } = body;
        const result = await (intent.emit || emitIntent)({
          verb: "dispose-possible",
          targetId: possible.id,
          args,
          snapshotRev: intent.snapshotRev,
          fetcher: o.fetcher,
        });
        tray.classList.remove("is-busy");
        panelEntry(EMISSION_PANEL_KIND[result.state] || "refused",
          possible.id + " → dispose-possible " + v.outcome + ": " +
          result.message);
        if (o.onEmitted) o.onEmitted(result);
        return;
      }
      const result = await post(GATE_DISPOSE_ROUTE, body, o.fetcher);
      tray.classList.remove("is-busy");
      if (result && result.ok) {
        applied.set(possible.id, result.outcome);
        panelEntry("ok", possible.id + " → " + result.outcome +
          " (regenerate the snapshot to fold it in)");
        if (o.onApplied) o.onApplied(result.outcome);
      } else {
        panelEntry("refused", (result && result.message) || "gate action failed");
      }
    });
    tray.appendChild(btn);
  }
  container.appendChild(tray);
  if (intent) {
    container.appendChild(renderIntentChips(el("span", "intentchips"),
      possible.id, intent.rows, intent.error));
  }
  return tray;
}

// ---- the propose button (add-propose-verb) ---------------------------------
// Mounts on a STAGED tile under the same capability gate as the tray: one click
// commissions proposal authoring for the topic (a recorded workflow-job
// dispatch — never authoring). Session-local overlay only; the snapshot stays
// deterministic.
//
// `opts.compact` is the IN-TILE mount (2026-07-25): the button now lives in the
// expanded tile's action row rather than the badge rail, so it takes smaller
// chrome (.dispose-intile) to fit. Behaviour is identical either way — same
// route, same panel entries, same disable-on-success.

// SESSION COMMISSIONS, keyed by (VERB, TARGET) — 011 add-wheel-action-verbs.
//
// This map used to be keyed by target id alone, which was unambiguous only
// while one verb per column existed. The possibles column now hosts TWO
// commission verbs, so a target-keyed flag would retire both when either fired
// — contradicting the (verb, target) duplicate rule the engine enforces
// (FR-027/FR-033). `propose` keeps its exact observable behaviour: it is simply
// the "propose" verb in the same store, and `commissionedWorkflow` still
// answers for it with the same signature.
//
// The VALUE is a per-verb marker, not strictly a workflow id: the three
// commissions store their workflow, and `demote` — which commissions nothing —
// stores a non-workflow marker recording that a plan was recorded this session
// (FR-033a). Session-local only: nothing is persisted, and a reload clears it.
const commissions = new Map();   // `${verb}\u0000${target}` -> marker

const DEMOTE_RECORDED = "demote:planned";

function commissionKey(verb, targetId) {
  return `${verb}\u0000${targetId}`;
}

export function commissionedVerb(verb, targetId) {
  return commissions.get(commissionKey(verb, targetId)) || null;
}

export function setCommission(verb, targetId, marker) {
  commissions.set(commissionKey(verb, targetId), marker);
}

/** TEST SEAM: the store is process-lifetime state, so probes reset it. */
export function resetSessionCommissions() {
  commissions.clear();
}

export function commissionedWorkflow(topicId) {
  return commissionedVerb("propose", topicId);
}

export function mountProposeButton(container, topic, opts) {
  const o = opts || {};
  const btn = el("button",
    "disposebtn dispose-propose" + (o.compact ? " dispose-intile" : ""),
    "\u25b6 draft proposal");
  btn.type = "button";
  btn.title = "commission proposal authoring for this staging topic " +
    "(recorded dispatch; the change lands for review + ratify)";
  btn.addEventListener("click", async (ev) => {
    ev.stopPropagation();
    btn.disabled = true;
    const result = await post(GATE_PROPOSE_ROUTE, { topic_id: topic.id }, o.fetcher);
    if (result && result.ok) {
      setCommission("propose", topic.id, result.workflow);
      panelEntry("ok", topic.id + " \u2192 proposal authoring commissioned (" +
        result.workflow + "); the change arrives for review + ratify");
      if (o.onApplied) o.onApplied(result.workflow);
    } else {
      btn.disabled = false;
      panelEntry("refused", (result && result.message) || "gate action failed");
    }
  });
  container.appendChild(btn);
  return btn;
}


// ---- the wheel action-row verbs (011 add-wheel-action-verbs) ---------------
//
// ONE mounter for all four. They differ only in their target field and in
// whether they collect a reason first, so a per-verb mounter would be four
// copies of the same transport with four chances to diverge.
//
// Every control is composed with `el`, which assigns `textContent` — so a
// refusal message can never introduce markup, and the DOM probe asserts that
// rather than trusting it.

const VERB_TARGET_FIELD = {
  "promote-to-staging": "possible_id",
  "research-brief": "possible_id",
  "derive-possibles": "cluster_id",
  "demote": "change_id",
};

const VERB_TITLE = {
  "promote-to-staging":
    "commission this ACCEPTED possible into a staging fragment " +
    "(recorded dispatch; the register is not touched)",
  "research-brief":
    "commission a pre-verdict evidence brief for this possible " +
    "(it informs the verdict and never makes it)",
  "derive-possibles":
    "commission a cluster-scoped run of the derivation lane " +
    "(candidates arrive pending_review)",
  "demote":
    "send this proposal back to staging: PLANS and RECORDS only — " +
    "the file moves stay a separate, human-run step",
};

/**
 * The in-page reason form (FR-006/FR-006a). Deliberately NOT `window.prompt`:
 * accessibility item 19 moved this codebase off blocking prompts, and adopting
 * one for new work would walk that back.
 *
 * Focus moves to the input on open and returns to `opener` on cancel or submit,
 * so a keyboard user is never stranded. An empty submit refocuses and dispatches
 * nothing; Escape cancels and dispatches nothing.
 */
function mountReasonForm(container, opener, onReason) {
  const form = el("div", "wheelreasonform");
  const input = el("input", "wheelreasoninput");
  input.type = "text";
  input.setAttribute("aria-label", "Reason this proposal goes back to staging");
  const close = () => { form.remove(); opener.disabled = false; opener.focus(); };
  const submit = () => {
    const reason = String(input.value || "").trim();
    if (!reason) { input.focus(); return; }   // nothing dispatched
    close();
    onReason(reason);
  };
  input.addEventListener("keydown", (ev) => {
    if (ev.key !== "Enter" && ev.key !== "Escape") return;
    // STOP THE EVENT HERE. The wheel collapses an expanded tile on any Escape
    // that reaches it ("Escape collapses from anywhere the keypress can
    // reach", wheel.js) — so a bubbling Escape would cancel this form AND
    // destroy the action row it lives in, leaving the verb unoffered and no
    // control to return focus to. Found by driving the real dashboard; a
    // synthetic event aimed straight at this input has no ancestor to reach,
    // which is why the unit probe missed it.
    ev.preventDefault();
    ev.stopPropagation();
    if (ev.key === "Enter") submit(); else close();
  });
  const ok = el("button", "cbtn wheelreasonsubmit", "record demotion");
  ok.type = "button";
  ok.addEventListener("click", (ev) => { ev.stopPropagation(); submit(); });
  const cancel = el("button", "cbtn wheelreasoncancel", "cancel");
  cancel.type = "button";
  cancel.addEventListener("click", (ev) => { ev.stopPropagation(); close(); });
  form.append(input, ok, cancel);
  container.appendChild(form);
  input.focus();
  return form;
}

/**
 * Mount ONE action-row verb. `opts.verb` selects the route, the target field
 * and the title; `opts.collectReason` is a test seam standing in for the form.
 *
 * On success the verb is retired for this (verb, target) THIS SESSION and the
 * tile is decorated by the caller's `onApplied`. On refusal the control is
 * re-enabled and nothing is retired, so the human can correct and retry.
 */
export function mountWheelVerb(container, item, opts) {
  const o = opts || {};
  const verb = o.verb;
  const targetField = VERB_TARGET_FIELD[verb];
  const btn = el("button",
    "disposebtn dispose-" + verb + (o.compact === false ? "" : " dispose-intile"),
    o.label || verb);
  btn.type = "button";
  btn.title = VERB_TITLE[verb] || verb;

  const dispatch = async (extra) => {
    btn.disabled = true;
    const body = { [targetField]: item.id, ...(extra || {}) };
    if (o.topic) body.topic = o.topic;
    const result = await post("/actions/gate/" + verb, body, o.fetcher);
    if (result && result.ok) {
      // demote commissions no workflow, so the marker is per-verb, never a
      // required `workflow` field on the response (FR-033a).
      setCommission(verb, item.id, result.workflow || DEMOTE_RECORDED);
      const where = result.job || result.plan || result.record || "";
      panelEntry("ok", item.id + " → " + verb + " recorded" +
        (where ? " (" + where + ")" : ""));
      if (o.onApplied) o.onApplied(result.workflow || DEMOTE_RECORDED);
    } else {
      btn.disabled = false;                       // retry after correcting
      panelEntry("refused", (result && result.message) || "gate action failed");
    }
  };

  btn.addEventListener("click", async (ev) => {
    ev.stopPropagation();
    if (verb !== "demote") { await dispatch(); return; }
    // demote REQUIRES a typed reason, collected before anything is dispatched
    if (o.collectReason) {
      const reason = o.collectReason();
      if (!reason) return;                        // cancelled: nothing sent
      await dispatch({ reason });
      return;
    }
    btn.disabled = true;                          // the form owns the control now
    mountReasonForm(container, btn, (reason) => { dispatch({ reason }); });
  });

  container.appendChild(btn);
  return btn;
}
