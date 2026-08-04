// The staging workbench's BRANCH-SESSION affordances — the three live session
// verbs, their outcomes, and the copyable CLI descriptors that replace them where
// this plane has no authority (007-workbench-branch-sessions T082;
// FR-044–FR-046; plan Constraint 11; research R6).
//
// WHY THIS IS A FOURTH MODULE AND NOT PART OF ANY EXISTING ONE. Three pins meet
// here and all three are the boundary, not an inconvenience:
//
//   * `test_renderer.py:130` pins the bundle's same-origin call-site set to five
//     files with per-file counts. A transport that uses the INJECTED-fetcher
//     spelling (`const doFetch = fetcher || fetch;`) contributes no call site, so
//     this file stays out of that set — the same trick `swb-create.js` uses.
//   * `test_staging_workbench.py` pins `staging-workbench.js` and
//     `staging-workbench-model.js` transport-free, and the model additionally
//     import-free (it is copied ALONE into a node harness). So the view cannot
//     hold this and the model cannot either.
//   * the same file pins ONE write-method literal per transport module. This
//     module addresses THREE routes, so the three verbs share ONE request helper
//     and select their route from the model's constants. That is the pin's
//     design: a second write literal would be a second, unreviewed write site.
//
// WHAT IT CAN DO — exactly three things, and each is a HUMAN-only gate verb the
// engine enforces independently of anything decided here:
//
//   edit     rewrite an EXISTING document inside the tile's session (FR-015).
//            Session-only: with no session live the engine refuses and names
//            `edit-apply`, the main-resident redline path, which is untouched.
//   save     push the session branch and open (or update) its pull request into
//            the EXISTING Merge-Master ritual (FR-029). It merges, approves,
//            self-reviews, and bypasses nothing — the port declares no such
//            operation (FR-030) and branch protection enforces it outside the
//            dashboard either way.
//   abandon  end the session without saving, with the REQUIRED durable reason
//            (FR-021/FR-022). Pushed history and any open pull request survive;
//            the branch is retained and its deletion is a separate, human-invoked
//            verb (FR-028).
//
// WHAT IT DELIBERATELY CANNOT DO. `refresh notebook` is DESCRIPTOR-ONLY in BOTH
// gate postures (spec C10, FR-044): it is not a gate route and not a `gate`
// subcommand, FR-040 maps it to `sync-notebooklm-books.py --session-ref`, and no
// ratified text asks for a live button. Giving it one would invent an FR-020
// parity obligation and FR-047 pin arithmetic out of thin air. It renders here as
// the copyable invocation, filled in for this session's branch.
//
// GATE-OFF (FR-046): with the probe's gate capability absent — an unresolved
// actor, or the static bundle whose `/capabilities` 404s — the mount returns the
// DESCRIPTORS before any live control exists. Enforcement is at the route
// regardless; withholding the control is a courtesy, never the boundary.
//
// HOSTED (FR-048) is a DIFFERENT answer, and conflating the two was review
// finding 14: a plane that explicitly reports `session: false` gets NOTHING —
// no posture line, no descriptor, no branch name. It has no sessions to describe
// and no checkout to run a CLI in, and a descriptor there would publish the
// topic ids of unmerged work. `sessionSurfaceHidden` is that discriminator.
//
// THE ENDING RE-DERIVES (Phase 7 note 4). A save that comes back `merged: true`
// means the branch was already merged, so the SESSION ENDED instead of being
// saved again: the response carries `torn_down` / `branch_deleted` /
// `record: null` rather than a pull request. An abandon ends it too. Either way
// the affordances must stop offering a session that is over, so both land in the
// page-lifetime `ended` overlay below and the mount re-renders from it — exactly
// how `dispose.js` treats an applied disposition.
//
// DOM-SAFETY: every dynamic value binds through `helpers.el`'s textContent; the
// only innerHTML assignments are literal "" clears. Refusals render in
// `dispose.js`'s shared panel, so a session refusal looks like every other
// refusal on the page.

import { el } from "./helpers.js";
import { panelEntry } from "./dispose.js";
import {
  SESSION_ABANDON, SESSION_AFFORDANCES, SESSION_EDIT, SESSION_LABELS,
  SESSION_FIRST_EDIT, SESSION_REFRESH_NOTEBOOK, SESSION_SAVE, SESSION_VERBS,
  consoleHeaders, firstEditBody, firstEditVerdict, notebookRefreshCommand,
  sessionActionsLive, sessionCommand, sessionRequest, sessionRoute,
  sessionSurfaceHidden,
} from "./staging-workbench-model.js";

// ---- the page-lifetime overlays --------------------------------------------
//
// The roster the posture reads was fetched at BOOT, so it is stale in both
// directions the moment the human acts: it does not yet know about a session a
// `create-document` just OPENED, and it still advertises one that just ENDED.
// These two maps are what make the indicator and the affordances honest between an
// action and a reload. Session-local only — nothing derived is mutated, exactly
// like dispose.js's `applied` map, and a reload replaces both with the server's
// own answer.

const opened = new Map();  // branch -> true
const ended = new Map();   // branch -> "merged" | "abandoned"
// branch -> { affordance, result, ending }: the ENGINE'S OWN report for the action
// that ended the session, remembered because the ending RE-RENDERS the affordance
// row and the re-render rebuilds the host the outcome was written into (T088,
// found by the Playwright smoke). Without this the answer to the most
// consequential action of a session's life — what was torn down, whether the
// branch was deleted — appeared and vanished inside one tick, leaving only
// tooltips. FR-044 wants the engine's answer to REACH the human.
const endedReports = new Map();

// Called by the view when a create response names a session `ref` (the create
// transport lives in swb-create.js; the view wires the two together rather than
// making the sibling modules depend on each other).
export function sessionOpened(branch) {
  const ref = String(branch || "");
  if (ref) opened.set(ref, true);
}

export function openedSessions() {
  return [...opened.keys()];
}

// The THIRD page-lifetime overlay (T092 defect 1 + defect 5): the documents this
// page's creates brought into existence, per session branch. A created document
// is the one thing outside a tile's own material its session may rewrite — the
// route says the same thing from the other side (`foreign_document_refusal`) — and
// the snapshot the page holds was fetched before the create, so without this the
// create→edit loop cannot be completed in one sitting on a tile that owns no
// folder. Session-local, exactly like `opened`: a reload replaces it with the
// session snapshot, which by then carries the document.
const created = new Map();  // branch -> Set(path)

export function documentCreated(branch, path) {
  const ref = String(branch || "");
  const rel = String(path || "");
  if (!ref || !rel) return;
  if (!created.has(ref)) created.set(ref, new Set());
  created.get(ref).add(rel);
}

export function createdDocuments(branch) {
  const ref = String(branch || "");
  return ref && created.has(ref) ? [...created.get(ref)] : [];
}

export function endedSessions() {
  return [...ended.keys()];
}

export function sessionEnding(branch) {
  return ended.get(String(branch)) || null;
}

export function sessionEndingReport(branch) {
  return endedReports.get(String(branch)) || null;
}

// ---- the ONE request site --------------------------------------------------
//
// Three routes, one helper, one write-method literal. `fetcher` is the injected
// transport seam every sibling module takes.

async function submitSession(affordance, body, fetcher, caps) {
  const doFetch = fetcher || fetch;
  const response = await doFetch(sessionRoute(affordance), {
    method: "POST",
    // the human-console header among them (FR-019's third clause): a write that
    // cannot present this serve's token is refused before its body is parsed
    headers: consoleHeaders(caps),
    body: JSON.stringify(body),
  });
  try {
    return await response.json();
  } catch {
    return { ok: false, message: "malformed response (HTTP " + response.status + ")" };
  }
}

// ---- the doxBench Save transport (010-doxbench-editor-chat T080) -----------
//
// The CANVAS's governed-Save wire, composed here because this module is where
// the branch-session verbs already live and `submitSession` is the ONE request
// site (three routes became four, same helper, same single write-method
// literal). This export is the TRANSPORT half only -- app.js composes it with
// the pure planner (doxbench-save.js) into the seam the canvas receives, so
// this module keeps its no-sibling-import harness discipline. Both wire
// translations are the MODEL's pure functions; nothing here invents
// vocabulary. One request per buffer, in the order the planner sends them.
export function firstEditTransport({ fetcher, caps } = {}) {
  return async (req) => firstEditVerdict(
    await submitSession(
      SESSION_FIRST_EDIT,
      firstEditBody(req.key.repository, req.key, req),
      fetcher, caps));
}

// ---- outcomes --------------------------------------------------------------

function line(host, text) {
  host.appendChild(el("div", "swb-cline", text));
}

function yesNo(value) {
  return value ? "yes" : "no";
}

// What the engine reported, rendered VERBATIM per verb. Every one of these fields
// is a response key the route contract declares; nothing is inferred, and a field
// the response omits is simply not shown.
function renderLanded(host, affordance, result) {
  if (affordance === SESSION_EDIT) {
    line(host, "document: " + result.document);
    line(host, "session branch: " + result.ref);
    line(host, "commit: " + result.commit);
    line(host, "gate-action record: " + result.record);
    return;
  }
  if (affordance === SESSION_ABANDON) {
    line(host, "session branch: " + result.ref);
    line(host, "reason: " + result.reason);
    line(host, "torn down: " + (result.torn_down || []).join(", "));
    line(host, "branch retained: " + yesNo(result.branch_retained));
    line(host, "gate-action record: " + result.record);
    return;
  }
  if (result.merged) {
    // the ENDING, not a save: the branch was already merged, so there is no pull
    // request to report and no record was written (Phase 7 note 4)
    line(host, "session branch: " + result.ref + " — MERGED, so the session ENDED");
    line(host, "torn down: " + (result.torn_down || []).join(", "));
    line(host, "branch deleted: " + yesNo(result.branch_deleted));
    return;
  }
  line(host, "pull request: " + result.pull_request);
  line(host, result.updated
    ? "an open pull request already existed — it was UPDATED, never duplicated"
    : "opened into the existing Merge-Master ritual");
  line(host, "session branch: " + result.ref);
  line(host, "gate-action record: " + result.record);
}

// Whether this outcome ENDED the session, and how. `merged: true` on a save is
// the merge ending (FR-033); an abandon is the other one (FR-021).
function endingOf(affordance, result) {
  if (affordance === SESSION_ABANDON) return "abandoned";
  if (affordance === SESSION_SAVE && result && result.merged) return "merged";
  return null;
}

// The LANDED box, built in ONE place so the live outcome and the ending's replay
// (below) can never drift apart — the same reason the `ended` overlay itself is
// one map rather than a re-derivation per call site.
function landedBox(affordance, result, ending) {
  const verb = SESSION_VERBS[affordance];
  const box = el("div", "swb-clanded");
  box.appendChild(el("div", "swb-ch", ending
    ? verb + " ✓ — the session ENDED (" + ending + ")"
    : verb + " ✓ — recorded gate dispatch"));
  renderLanded(box, affordance, result);
  if (result.hint) box.appendChild(el("div", "swb-cnote", result.hint));
  for (const note of result.notes || []) box.appendChild(el("div", "swb-cnote", note));
  // FR-042 / D19: a session that opened without its notebook is a NOTICE, not an
  // error — the session is live and fully usable
  if (result.notebook_notice) {
    box.appendChild(el("div", "swb-cnote swb-notice",
      "notice: " + result.notebook_notice));
  }
  if (result.view_notice) {
    box.appendChild(el("div", "swb-cnote swb-notice",
      "notice: " + result.view_notice));
  }
  return box;
}

async function renderOutcome(host, affordance, result, opts) {
  const o = opts || {};
  host.innerHTML = "";
  const verb = SESSION_VERBS[affordance];
  if (!(result && result.ok)) {
    const refused = el("div", "swb-crefused");
    refused.appendChild(el("div", "swb-ch", "refused ✕"));
    // the engine's refusal reaches the human VERBATIM (the route's response
    // discipline) — never a paraphrase, and never swallowed
    refused.appendChild(el("div", "swb-cline",
      (result && result.message) || (verb + " was refused")));
    host.appendChild(refused);
    panelEntry("refused", (result && result.message) || (verb + " refused"));
    return null;
  }
  const ending = endingOf(affordance, result);
  const box = landedBox(affordance, result, ending);
  host.appendChild(box);
  panelEntry("ok", verb + " " + result.ref + (ending ? " → session " + ending : ""));
  if (ending) {
    ended.set(String(result.ref), ending);
    // remembered BEFORE the re-render below, which rebuilds `host`'s ancestor
    endedReports.set(String(result.ref), { affordance, result, ending });
    if (o.onSessionEnded) {
      try {
        await o.onSessionEnded(result, ending);
      } catch {
        result.view_notice = "the session ended, but the main view could not " +
          "be loaded; reload the dashboard";
        box.appendChild(el("div", "swb-cnote swb-notice",
          "notice: " + result.view_notice));
      }
    }
  } else if (o.onSessionChanged) {
    o.onSessionChanged(result);
  }
  return ending;
}

// ---- the gate-off rendering (FR-046) ---------------------------------------
//
// Every affordance as the REAL `cli.py gate <verb>` invocation for this tile,
// selectable and copyable. Defined ABOVE the mount so the early return below
// reads in the order it executes, and deliberately holding no reference to the
// request helper: with the gate off there is no path from this page to a write.

function descriptorBox(host, label, note, command) {
  const box = el("div", "swb-cdescriptor");
  box.appendChild(el("div", "swb-clabel", label));
  box.appendChild(el("div", "swb-cnote", note));
  const cmd = el("code", "swb-ccmd", command);
  cmd.tabIndex = 0;
  box.appendChild(cmd);
  host.appendChild(box);
  return box;
}

// The notebook re-sync descriptor, rendered in BOTH postures (spec C10): the
// dry-run line first — the script prints the op list for a human to eyeball —
// then the explicit apply form.
function renderNotebookDescriptor(host, ctx) {
  const posture = ctx.posture || {};
  const branch = posture.branch;
  const box = el("div", "swb-cdescriptor");
  box.appendChild(el("div", "swb-clabel", SESSION_LABELS[SESSION_REFRESH_NOTEBOOK]));
  // WHY THERE MAY BE NO BRANCH HERE (PR #49 second-review finding 18). This
  // command re-syncs a notebook FROM a worktree, so a branch that is another
  // tile's session must never reach it: it would re-sync that tile's session
  // notebook from that tile's worktree. The posture withholds an ambiguous ref, and
  // this says so rather than silently offering the `<branch>` placeholder.
  box.appendChild(el("div", "swb-cnote", branch
    ? "the session notebook is re-synced from the WORKTREE by the sync script — "
      + "not a gate verb and not a dashboard route, so it is a copyable command "
      + "in every posture. Dry-run first, then apply:"
    : (posture.ambiguousRef
      ? "no ref can be filled in here: " + posture.ambiguousRef + " is in this "
        + "tile's ordinal family AND is tile " + posture.ambiguousOwner + "'s own "
        + "session branch, so re-syncing it could re-sync ANOTHER tile's session "
        + "notebook from another tile's worktree. Resolve the ambiguity first (end "
        + "that session from the tile that owns it, or rename one tile):"
      : "no session branch to re-sync yet — the first recorded write opens one, "
        + "and its notebook is created with it:")));
  for (const apply of [false, true]) {
    const cmd = el("code", "swb-ccmd", notebookRefreshCommand({ branch, apply }));
    cmd.tabIndex = 0;
    box.appendChild(cmd);
  }
  host.appendChild(box);
  return box;
}

function renderSessionDescriptors(host, ctx, opts) {
  const o = opts || {};
  const wrap = el("div", "swb-sessiondescriptors");
  wrap.appendChild(el("div", "swb-cnote",
    "this surface has no session authority (read-only host) — run these in your "
    + "own checkout, where the authority and the identity live:"));
  for (const affordance of SESSION_AFFORDANCES) {
    if (affordance === SESSION_REFRESH_NOTEBOOK) {
      renderNotebookDescriptor(wrap, ctx);
      continue;
    }
    const command = sessionCommand(affordance, { scope: ctx.scope, actor: o.actor });
    if (!command) continue;
    descriptorBox(wrap, SESSION_LABELS[affordance],
      "the " + SESSION_VERBS[affordance] + " verb, filled in for this tile:",
      command);
  }
  host.appendChild(wrap);
  return wrap;
}

// ---- the live forms --------------------------------------------------------

function field(host, label, value, opts) {
  const o = opts || {};
  const row = el("label", "swb-cfield");
  row.appendChild(el("span", "swb-clabel", label));
  const input = o.multiline
    ? document.createElement("textarea")
    : document.createElement("input");
  if (!o.multiline) input.type = "text";
  if (o.multiline) input.rows = 12;
  input.value = value == null ? "" : String(value);
  input.setAttribute("aria-label", label);
  if (o.placeholder) input.setAttribute("placeholder", o.placeholder);
  row.appendChild(input);
  host.appendChild(row);
  return input;
}

function documentPicker(host, ctx) {
  const row = el("label", "swb-cfield");
  row.appendChild(el("span", "swb-clabel", "Document"));
  const select = document.createElement("select");
  select.setAttribute("aria-label", "the document to rewrite");
  for (const path of ctx.documents || []) {
    const option = document.createElement("option");
    option.value = path;
    option.textContent = path;
    select.appendChild(option);
  }
  row.appendChild(select);
  host.appendChild(row);
  return select;
}

// The per-affordance form. One shape, one submit path, so the three verbs cannot
// grow three postures. Every field is the request body's own — `sessionRequest`
// in the pure model owns the wire spelling.
function renderForm(host, affordance, ctx, opts) {
  const o = opts || {};
  host.innerHTML = "";
  const form = el("div", "swb-cform");
  form.appendChild(el("div", "swb-ch", SESSION_LABELS[affordance]));
  const values = {};
  let picker = null;
  let content = null;
  if (affordance === SESSION_EDIT) {
    form.appendChild(el("div", "swb-cnote",
      "the replacement is the document's WHOLE text: this verb rewrites, it never "
      + "patches, and an empty replacement is refused as a delete in disguise. "
      + "Read the current text in the viewer beside this panel first."));
    picker = documentPicker(form, ctx);
    content = field(form, "Replacement", "",
      { multiline: true, placeholder: "the document's full new text" });
  } else if (affordance === SESSION_SAVE) {
    // WHAT BLANK MEANS, honestly (PR #49 second-review finding R2-13). It used to
    // say "left blank, the engine names the branch and its tile" full stop, while
    // a second save with the form blank REPLACED whatever a human had written.
    // Blank now means what this text says on both paths: defaults on the FIRST
    // save, unchanged on every later one.
    form.appendChild(el("div", "swb-cnote",
      "pushes this session's branch and opens (or updates) its pull request into "
      + "the existing Merge-Master ritual. It merges, approves, and reviews "
      + "nothing. Title and body are optional: on the FIRST save, left blank, the "
      + "engine names the branch and its tile and carries the "
      + "merge-commit-never-squash notice — on a LATER save, left blank, the pull "
      + "request's existing title and body are left exactly as they are. A save "
      + "never overwrites reviewer-facing text you wrote."));
    values.title = field(form, "Title", "",
      { placeholder: "optional — blank keeps the existing title (the first save "
                     + "names the branch and its tile)" });
    values.body = field(form, "Body", "",
      { multiline: true,
        placeholder: "optional — blank keeps the existing body (the first save "
                     + "carries D18's notice)" });
  } else {
    form.appendChild(el("div", "swb-cnote",
      "ends this session without saving. The reason is REQUIRED and durable, "
      + "exactly as a demotion's is; the branch and any pushed history SURVIVE, "
      + "and deleting it later is a separate, human-invoked verb."));
    values.reason = field(form, "Reason", "",
      { placeholder: "the durable why this exploration stopped" });
  }

  const result = el("div", "swb-cresult");
  result.setAttribute("aria-live", "polite");
  const bar = el("div", "swb-cactions");
  const submit = el("button", "cbtn", SESSION_VERBS[affordance]);
  submit.type = "button";
  submit.title = "EXECUTES via the local gate route (actor: " + (o.actor || "local") + ")";
  const cancel = el("button", "cbtn", "cancel");
  cancel.type = "button";
  cancel.addEventListener("click", () => { host.innerHTML = ""; });

  submit.addEventListener("click", async () => {
    const body = sessionRequest(affordance, ctx.scope, {
      // the repository the page is reading, carried so the route can refuse a
      // session write it cannot honour (review finding 8)
      repository: ctx.posture ? ctx.posture.repository : null,
      document: picker ? picker.value : null,
      content: content ? content.value : null,
      title: values.title ? values.title.value : null,
      body: values.body ? values.body.value : null,
      reason: values.reason ? values.reason.value : null,
    });
    if (!body) {
      panelEntry("refused",
        "this tile resolves no session scope, so no session verb can address it");
      return;
    }
    submit.disabled = true;
    const payload = await submitSession(affordance, body, o.fetcher, o.caps);
    const ending = await renderOutcome(result, affordance, payload, o);
    // a refusal is retriable in place; a landed action is done, and an ENDING
    // takes the whole affordance set with it
    if (!(payload && payload.ok)) submit.disabled = false;
    if (ending && o.onRerender) o.onRerender();
  });

  bar.append(submit, cancel);
  form.appendChild(bar);
  form.appendChild(result);
  // Escape closes the FORM, not the whole workbench
  form.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape") { ev.stopPropagation(); host.innerHTML = ""; }
  });
  host.appendChild(form);
}

// ---- the mount -------------------------------------------------------------

// Mount the session affordance row into `host`.
//
// `ctx`: { scope, posture, documents } — the tile's scope (the session identity
// every request carries), the posture derived in the transport-free model, and
// the scope's document paths for the edit picker.
// `opts`: { caps, actor, fetcher, onSessionEnded, onSessionChanged, onRerender }.
//
// The FIRST statement is the capability branch, and it RETURNS: gate-off, no live
// control is constructed at all (FR-046). The capability is asked exactly once,
// through the pure model's one derivation, so no branch of this file can reach a
// different verdict than the posture indicator shows.
export function mountSessionAffordances(host, ctx, opts) {
  const o = opts || {};
  // FR-048 FIRST: a plane that declares `session: false` is the HOSTED plane and
  // exposes NOTHING of this capability — not a live control, and not a
  // descriptor naming the verb and the branch (review finding 14).
  if (sessionSurfaceHidden(o.caps)) return null;
  if (!sessionActionsLive(o.caps)) return renderSessionDescriptors(host, ctx, o);
  const wrap = el("div", "swb-sessionactions");
  const slot = el("div", "swb-cslot");
  const ending = ctx.posture ? sessionEnding(ctx.posture.branch) : null;
  for (const affordance of SESSION_AFFORDANCES) {
    if (affordance === SESSION_REFRESH_NOTEBOOK) continue;   // descriptor-only, below
    const button = el("button", "cbtn swb-sessionbtn", SESSION_LABELS[affordance]);
    button.type = "button";
    button.title = "the human-only " + SESSION_VERBS[affordance] +
      " gate verb, recorded (actor: " + (o.actor || "local") + ")";
    if (ending) {
      // the session ended during this page's life: say so rather than offering a
      // verb that can only be refused
      button.disabled = true;
      button.title = "this tile's session " + ending +
        " — reload to see the tile's current state";
    }
    button.addEventListener("click", () => renderForm(slot, affordance, ctx, o));
    wrap.appendChild(button);
  }
  host.appendChild(wrap);
  // DESCRIPTOR-ONLY in this posture too (spec C10) — it is not a gate verb
  renderNotebookDescriptor(host, ctx);
  host.appendChild(slot);
  // THE ENDING'S REPORT, REPLAYED (T088). The ending re-renders this row, and the
  // re-render destroyed the slot the outcome had just been written into — so the
  // engine's own account of the teardown is put back into the slot this call just
  // built, verbatim and through the SAME renderer. A reload replaces it with the
  // server's answer, exactly like every other page-lifetime overlay here.
  if (ending) {
    const report = endedReports.get(String(ctx.posture && ctx.posture.branch));
    if (report) slot.appendChild(landedBox(report.affordance, report.result,
                                          report.ending));
  }
  return wrap;
}
