// The staging workbench's CREATE-DOCUMENT affordance — dialog + transport
// (openxFactory `add-workbench-bullseye-and-create`, design D5/D7/D8).
//
// WHY THIS IS A SIBLING MODULE AND NOT PART OF staging-workbench.js: the view
// file is PINNED free of transport (test_staging_workbench.py asserts it carries
// no fetch call, no method literal, no XHR) and the pure model module is pinned
// import-free for its node harness. So the one write the workbench performs
// lives here, in the shape dispose.js / gate.js / lens.js already established:
// an injectable fetcher (`const doFetch = fetcher || fetch`), which is also what
// keeps this file out of test_renderer.py's pinned set of fetch-bearing bundle
// files.
//
// WHAT IT CAN DO: exactly one thing — bring a NEW document into existence
// through the human-only gate verb, which drives the tested authoring scaffold
// (`authoring.create_scaffold` -> `boundary.create_document`, create-only). It
// cannot edit, cannot delete, and cannot overwrite: an existing target refuses
// as a source-edit and the refusal renders here verbatim.
//
// GATE-OFF (design D8): with `caps.actions.gate` absent — the hosted static
// image, a non-loopback bind, an unresolved actor — no live control is rendered
// at all. The affordance becomes a COPYABLE CLI DESCRIPTOR carrying the seeded
// values, which is strictly more useful than a greyed-out button because it is
// the whole action, transportable to where the authority lives. Enforcement is
// at the route regardless; hiding the control is a courtesy, never the boundary.
//
// DOM-SAFETY: every dynamic value binds through textContent (helpers.el); the
// only innerHTML assignments are literal "" clears.

import { el } from "./helpers.js";
import { panelEntry } from "./dispose.js";
import {
  CONTINUATIONS, CREATE_ROUTE, consoleHeaders, createDocumentCommand,
  createRequest,
} from "./staging-workbench-model.js";

export function createGateLive(caps) {
  return !!(caps && caps.actions && caps.actions.gate);
}

async function submitCreate(body, fetcher, caps) {
  const doFetch = fetcher || fetch;
  const response = await doFetch(CREATE_ROUTE, {
    method: "POST",
    // the human-console header among them (FR-019's third clause)
    headers: consoleHeaders(caps),
    body: JSON.stringify(body),
  });
  try {
    return await response.json();
  } catch {
    return { ok: false, message: "malformed response (HTTP " + response.status + ")" };
  }
}

function labelledInput(host, label, value, opts) {
  const o = opts || {};
  const row = el("label", "swb-cfield");
  row.appendChild(el("span", "swb-clabel", label));
  const input = document.createElement("input");
  input.type = "text";
  input.value = value == null ? "" : String(value);
  input.setAttribute("aria-label", label);
  if (o.placeholder) input.setAttribute("placeholder", o.placeholder);
  row.appendChild(input);
  host.appendChild(row);
  return input;
}

// A create inside a tile scope opens or joins its branch session. Await the
// shell hand-off before the document jump, so the source read and edit action
// cannot observe different repository/ref keys.
async function renderSessionLanding(box, result, onSessionOpened) {
  if (!result.ref) return true;
  box.appendChild(el("div", "swb-cline", "session branch: " + result.ref +
    (result.joined ? " (joined)" : " (opened)")));
  box.appendChild(el("div", "swb-cline", "commit: " + result.commit));
  if (!onSessionOpened) return false;
  try {
    await onSessionOpened(result);
    return true;
  } catch {
    box.appendChild(el("div", "swb-cnote swb-notice",
      "notice: the session opened, but its document view could not be " +
      "loaded; refresh and select the session branch"));
    return false;
  }
}

async function renderLanded(host, result, onOpenDoc, onSessionOpened) {
  const box = el("div", "swb-clanded");
  box.appendChild(el("div", "swb-ch", "created ✓ — recorded gate dispatch"));
  box.appendChild(el("div", "swb-cline", "document: " + result.path));
  box.appendChild(el("div", "swb-cline", "gate-action record: " + result.record));
  const sessionViewReady = await renderSessionLanding(
    box, result, onSessionOpened);
  // FR-042 / D19: a session that opened WITHOUT its notebook is a NOTICE, not a
  // failure — the session is live and fully usable.
  if (result.notebook_notice) {
    box.appendChild(el("div", "swb-cnote swb-notice",
      "notice: " + result.notebook_notice));
  }
  if (result.hint) box.appendChild(el("div", "swb-cnote", result.hint));
  host.appendChild(box);
  panelEntry("ok", "created " + result.path + " (record " + result.record + ")"
    + (result.ref ? " on " + result.ref : ""));
  if (onOpenDoc && sessionViewReady) onOpenDoc(result.path);
}

function renderRefused(host, result) {
  const refused = el("div", "swb-crefused");
  refused.appendChild(el("div", "swb-ch", "refused ✕"));
  refused.appendChild(el("div", "swb-cline",
    result?.message || "the create was refused"));
  host.appendChild(refused);
  panelEntry("refused", result?.message || "create-document refused");
}

// The landing confirmation / refusal. The engine's refusal message reaches the
// human verbatim (the route's response discipline) — never a paraphrase.
async function renderOutcome(host, result, onOpenDoc, onSessionOpened) {
  host.innerHTML = "";
  if (result?.ok) {
    await renderLanded(host, result, onOpenDoc, onSessionOpened);
    return;
  }
  renderRefused(host, result);
}

// The FR-025 continuation control: unset, `resume`, or `new`. Unset is the
// default and the ordinary case — the field is only meaningful once the engine has
// REPORTED the choice, and the report is a refusal that renders right below.
function continuationPicker(host) {
  const row = el("label", "swb-cfield");
  row.appendChild(el("span", "swb-clabel", "Continuation"));
  const select = document.createElement("select");
  select.setAttribute("aria-label",
    "answer the resume-or-new report on a tile whose abandoned branch survives");
  const unset = document.createElement("option");
  unset.value = "";
  unset.textContent = "(none — be shown the choice)";
  select.appendChild(unset);
  for (const token of CONTINUATIONS) {
    const option = document.createElement("option");
    option.value = token;
    option.textContent = token === "resume"
      ? "resume — keep the existing branch and its history"
      : "new — open the next ordinal session";
    select.appendChild(option);
  }
  row.appendChild(select);
  host.appendChild(row);
  return select;
}

// The create form: every seeded value editable, `title` and `summary` the
// human's to type (design D7 — they have no honest machine seed, and a generated
// one would be prose the dashboard invented).
function renderForm(host, seed, opts) {
  const o = opts || {};
  host.innerHTML = "";
  const form = el("div", "swb-cform");
  form.appendChild(el("div", "swb-ch", "new document in this scope"));
  form.appendChild(el("div", "swb-cnote",
    "seeded from what this tab already knows — every value is editable, and the " +
    "create is create-only: an existing path is refused, never overwritten."));

  const title = labelledInput(form, "Title", seed.title,
    { placeholder: "the document's H1 (— Brainstorm is appended by the engine)" });
  const summary = labelledInput(form, "Summary", seed.summary,
    { placeholder: "one sentence — yours to write, never generated here" });
  const topics = labelledInput(form, "Topics", (seed.topics || []).join(", "),
    { placeholder: "comma-separated declared topics" });
  const area = labelledInput(form, "Area", seed.area);
  // `Status:` is seeded `brainstorm` and NEVER follows the area (Brett's
  // 2026-07-25 ruling on open question 1 — "these are brainstorm docs"; the
  // packet tie is the AREA's placement, not this header). Editable, so a human
  // writing an organized fragment can promote it here.
  const status = labelledInput(form, "Status", seed.status);
  const kind = labelledInput(form, "Kind", seed.kind);
  form.appendChild(el("div", "swb-cnote", "Repository context: " +
    (seed.repositoryContext || "(none in this snapshot)")));
  form.appendChild(el("div", "swb-csource", "Source: " + seed.source));
  // THE RESUME-OR-NEW ANSWER (007-workbench-branch-sessions T082, FR-025). The
  // CHOICE is the refusal: on a tile whose ABANDONED branch survives, the first
  // create is REFUSED with a report naming the branch, both continuations, and
  // the ordinal a NEW session would allocate. The human answers HERE and
  // resubmits — which is why this control is deliberately unset by default: a
  // seeded answer would answer for them, and every ordinary create sends none.
  const continuation = continuationPicker(form);

  const result = el("div", "swb-cresult");
  result.setAttribute("aria-live", "polite");
  const bar = el("div", "swb-cactions");
  const submit = el("button", "cbtn", "create document");
  submit.type = "button";
  submit.title = "EXECUTES via the local gate route (actor: " +
    ((o.caps && o.caps.actor) || "local") + ")";
  const cancel = el("button", "cbtn", "cancel");
  cancel.type = "button";
  cancel.addEventListener("click", () => { host.innerHTML = ""; });

  submit.addEventListener("click", async () => {
    // The tile's SCOPE rides the seed (`scopeKind` / `scopeId`, set by
    // `createSeed`) into `createRequest`, which is where the wire spelling lives
    // — so this transport gains the branch-session identity
    // (007-workbench-branch-sessions T023a) without gaining a second request
    // site or a second body definition. The model is the payload contract; this
    // file stays the ONE write.
    const body = createRequest(seed, {
      title: title.value.trim(),
      summary: summary.value.trim(),
      topics: topics.value.split(",").map((t) => t.trim()).filter((t) => t),
      area: area.value.trim(),
      status: status.value.trim(),
      kind: kind.value.trim(),
      continuation: continuation.value,
    });
    submit.disabled = true;
    const payload = await submitCreate(body, o.fetcher, o.caps);
    await renderOutcome(result, payload, o.onOpenDoc, o.onSessionOpened);
    // a refused create is retriable in place; a landed one is done
    if (!(payload && payload.ok)) submit.disabled = false;
  });

  bar.append(submit, cancel);
  form.appendChild(bar);
  form.appendChild(result);
  // Escape closes the FORM, not the whole workbench (the shell's document-level
  // Escape handler would otherwise take the human out of their scope).
  form.addEventListener("keydown", (ev) => {
    if (ev.key === "Escape") { ev.stopPropagation(); host.innerHTML = ""; }
  });
  host.appendChild(form);
  title.focus();
}

// The gate-off rendering: the exact CLI invocation, selectable and copyable.
function renderDescriptor(host, seed, opts) {
  const o = opts || {};
  const box = el("div", "swb-cdescriptor");
  box.appendChild(el("div", "swb-clabel", o.label || "new document in this scope"));
  box.appendChild(el("div", "swb-cnote",
    "this surface has no gate capability (read-only host) — run the seeded " +
    "command in your pinned checkout, where the authority lives:"));
  const cmd = el("code", "swb-ccmd",
    createDocumentCommand(seed, { actor: (o.caps && o.caps.actor) || null }));
  cmd.tabIndex = 0;
  box.appendChild(cmd);
  host.appendChild(box);
  return box;
}

// Mount ONE create affordance into `host` for `seed`. With the gate capability
// live this is a labelled button revealing the form; without it, a copyable CLI
// descriptor and no write path at all. `opts`: { caps, fetcher, label,
// onOpenDoc, onSessionOpened } — `onOpenDoc(path)` opens the created document in
// the read-only viewer (the same seam the docs rows use), and
// `onSessionOpened(result)` tells the shell the create opened or joined a BRANCH
// SESSION, so its posture indicator stops reading from a boot-time roster.
export function mountCreateAffordance(host, seed, opts) {
  const o = opts || {};
  if (!createGateLive(o.caps)) return renderDescriptor(host, seed, o);
  const wrap = el("div", "swb-cwrap");
  // `opts.slot` lets a caller share ONE dialog host between this button and
  // another opener (the lens tab's centre-ring gesture), so the two affordances
  // can never render two competing forms.
  const slot = o.slot || el("div", "swb-cslot");
  const open = el("button", "cbtn swb-cbtn", o.label || "＋ new document");
  open.type = "button";
  open.title = "create a header-compliant document in " + seed.area +
    " through the human-only gate verb (create-only)";
  open.addEventListener("click", () => renderForm(slot, seed, o));
  wrap.appendChild(open);
  if (!o.slot) wrap.appendChild(slot);
  host.appendChild(wrap);
  return wrap;
}

// The centre-ring gesture's opener (design D6): the SAME dialog with the SAME
// seeding rule, so the ring and the button can never diverge. Gate-off, the ring
// reveals the descriptor rather than a form — still no write from the page.
export function openCreateDialog(host, seed, opts) {
  const o = opts || {};
  host.innerHTML = "";
  if (!createGateLive(o.caps)) return renderDescriptor(host, seed, o);
  return renderForm(host, seed, o);
}
