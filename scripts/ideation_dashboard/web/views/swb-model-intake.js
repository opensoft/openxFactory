// THE MODEL INTAKE FLOW — dialog plus transport
// (openxFactory `add-doxchat-model-intake`, sections 2 and 3).
//
// WHY THIS IS A SIBLING MODULE. The chat rail is pinned free of transports and
// free of every credential-shaped literal (test_doxbench_privacy.py scans both
// chat files for every transport primitive, for storage, and for the vocabulary
// a provider client
// would need), and the workbench view is pinned free of write methods. So the
// one flow that carries a provider credential lives here, in the shape
// `swb-create.js` and `swb-session.js` already established: an injectable
// fetcher (`const doFetch = fetcher || fetch`), which is also what keeps this
// file out of test_renderer.py's pinned set of fetch-bearing bundle files.
//
// WHAT IT CAN DO, exactly three things:
//
//   1. ASK whether enrolment is offered at all. It is offered only where the
//      install declares a broker to take custody, and the answer is the
//      server's — never a guess. That answer is what decides whether the rail
//      renders its intake affordance, because the ratified sequencing
//      requirement says the affordance SHALL NOT be released ahead of the flow
//      it opens.
//   2. ENROL: hand what the human supplied to the server, which hands it to the
//      broker and keeps only the reference. This browser holds nothing
//      afterwards — the field is cleared, no value is stored, and the answer
//      that comes back is a binding read-back that names a secret it does not
//      contain.
//   3. APPROVE: the flow's own explicit last step (OQ-5, ruled 2026-08-21).
//      Enrolling PROPOSES a model; this act APPROVES it, and the server records
//      a gate action naming the declaration before anything becomes available.
//      A human who just authorized a subscription is the right approver at the
//      right moment; routing them to a separate console to finish would make
//      the pending state a trap rather than a safeguard.
//
// WHAT IT MUST NEVER DO, and does not: hold the supplied value in any state that
// outlives the request, write it to any storage, put it in a URL, echo it back
// into the page, or send it anywhere but this same-origin route. The value rides
// the request BODY and the facts ride the query string, mirroring the server's
// own split — because a query string is a thing proxies and access logs record.
//
// THE OAUTH KIND IS OFFERED AND NEVER SIMULATED. The server hands the human to
// the broker's own authorization surface (OQ-2, ruled 2026-08-21) and this page
// is never the party that receives a provider token. Where the declared broker
// has not implemented that flow, the refusal it produces is shown verbatim as
// the server's own fixed sentence — no redirect is invented here, and no field
// that would take token material is ever presented for that kind.
//
// DOM-SAFETY: every dynamic value binds through textContent (helpers.el); the
// only innerHTML assignments are literal "" clears.

import { el } from "./helpers.js";
import {
  MODEL_INTAKE_SURFACE_ROUTE, MODEL_INTAKE_ROUTE, MODEL_APPROVAL_ROUTE,
  consoleHeaders, intakeQuery, withConsoleRepair,
} from "./staging-workbench-model.js";

// The fixed sentence this module shows when it has no better one to show. The
// SERVER's own stated reason is preferred wherever it sends one — those are
// module constants over there, never a broker's words and never a provider's —
// and this stands in when a response carried none.
export const INTAKE_UNKNOWN_REFUSAL =
  "the console refused and stored nothing; nothing was enrolled and nothing "
  + "was approved.";

// ---- the transport -------------------------------------------------------
//
// ONE request helper, so this file carries exactly one write-method literal —
// the per-file pin `swb-create.js` and `swb-session.js` both keep. A second
// literal here would mean a second, unreviewed write site.
async function submitIntake(url, init, repair) {
  const doFetch = init.fetcher || fetch;
  const send = async () => {
    const response = await doFetch(url, {
      method: "POST",
      headers: init.headers,
      body: init.body,
    });
    const payload = await response.json().catch(() => null);
    return payload || { ok: false, message: INTAKE_UNKNOWN_REFUSAL };
  };
  return withConsoleRepair(send, repair);
}

export function createModelIntakeTransports(capsOf, repair, fetcher) {
  const caps = () => (typeof capsOf === "function" ? capsOf() : capsOf);
  return {
    // WHETHER THE FLOW EXISTS. A refusal of any kind answers `offered: false`
    // with no reason of this page's own invention: the rail then renders no
    // affordance, which is indistinguishable from its behaviour before this
    // change — the sequencing requirement's own test.
    async surface() {
      const doFetch = fetcher || fetch;
      const headers = consoleHeaders(caps());
      delete headers["Content-Type"];
      const response = await doFetch(MODEL_INTAKE_SURFACE_ROUTE, {
        cache: "no-store",
        headers,
      });
      if (!response.ok) return { offered: false };
      const body = await response.json().catch(() => null);
      return body && typeof body === "object" ? body : { offered: false };
    },

    // ENROL. `facts` are the declared, non-secret facts; `supplied` is what the
    // human typed, and it is passed straight through as the request body and
    // referenced nowhere else in this module — not stored, not logged, not
    // returned, and not read back out of the DOM afterwards.
    async enrol(facts, supplied) {
      const headers = consoleHeaders(caps());
      // A DELIBERATE CONTENT TYPE. The body is not a document and is not JSON:
      // it is exactly what the human supplied, so the server can stream it into
      // the broker without ever parsing it into a value of its own.
      headers["Content-Type"] = "text/plain; charset=utf-8";
      return submitIntake(
        intakeQuery(MODEL_INTAKE_ROUTE, facts),
        { headers, body: typeof supplied === "string" ? supplied : "",
          fetcher },
        repair);
    },

    // APPROVE. Carries a name and nothing else — no value, no reference, no
    // provider fact. The RECORD is the server's to write.
    async approve(bindingId) {
      return submitIntake(
        MODEL_APPROVAL_ROUTE,
        { headers: consoleHeaders(caps()),
          body: JSON.stringify({ binding: bindingId }), fetcher },
        repair);
    },
  };
}

// ---- the dialog ----------------------------------------------------------

function field(host, labelText, name, placeholder) {
  const wrap = el("label", "swb-intake-field");
  wrap.appendChild(el("span", "swb-intake-label", labelText));
  const input = el("input", "swb-intake-input");
  input.name = name;
  input.type = "text";
  input.setAttribute("autocomplete", "off");
  if (placeholder) input.setAttribute("placeholder", placeholder);
  wrap.appendChild(input);
  host.appendChild(wrap);
  return input;
}

// Open the flow into `host`, replacing whatever it held. Returns a controller
// with `close()` so the shell can dismiss it; the shell owns where the panel
// lives, exactly as it does for the create dialog.
export function openModelIntake(host, options) {
  const opts = options || {};
  const transports = opts.transports || {};
  const panel = el("div", "swb-intake-panel");
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "add a model");
  host.textContent = "";
  host.appendChild(panel);
  host.hidden = false;

  const status = el("div", "swb-intake-status");
  status.setAttribute("aria-live", "polite");

  function close() {
    host.textContent = "";
    host.hidden = true;
    if (typeof opts.onClose === "function") opts.onClose();
  }

  function say(text) {
    status.hidden = !text;
    status.textContent = text || "";
  }

  // The server's own stated reason wherever it sent one. Never composed here,
  // never assembled from parts, and never a broker's or a provider's words: the
  // server's refusal bodies carry a `reason` drawn from its own module
  // constants, and this shows exactly that string or the fixed fallback.
  function refusalText(payload) {
    const reason = payload && payload.reason;
    if (typeof reason === "string" && reason !== "") return reason;
    const message = payload && payload.message;
    if (typeof message === "string" && message !== "") return message;
    return INTAKE_UNKNOWN_REFUSAL;
  }

  function renderApproval(declaration, surface) {
    panel.textContent = "";
    panel.appendChild(el("h3", "swb-intake-heading", "Approve this model"));
    panel.appendChild(el("p", "swb-intake-note",
      typeof declaration.availability === "string"
        ? declaration.availability : ""));
    panel.appendChild(el("p", "swb-intake-note",
      "Enrolling declared this model. Approving it is a separate act and it "
      + "is recorded: the console writes a gate action naming this declaration, "
      + "with who issued it, who approved it, when the approval expires, and "
      + "the audit reference, before the model becomes selectable."));
    panel.appendChild(status);
    const approveBtn = el("button", "swb-intake-approve",
                          "Approve and make selectable");
    approveBtn.type = "button";
    approveBtn.addEventListener("click", async () => {
      approveBtn.disabled = true;
      say("recording the approval…");
      const answer = await transports.approve(declaration.binding_id);
      if (!answer || answer.ok !== true) {
        approveBtn.disabled = false;
        say(refusalText(answer));
        return;
      }
      panel.textContent = "";
      panel.appendChild(el("h3", "swb-intake-heading", "Model approved"));
      panel.appendChild(el("p", "swb-intake-note",
        typeof answer.availability === "string" ? answer.availability : ""));
      const done = el("button", "swb-intake-close", "Close");
      done.type = "button";
      done.addEventListener("click", () => {
        if (typeof opts.onApproved === "function") opts.onApproved();
        close();
      });
      panel.appendChild(done);
    });
    panel.appendChild(approveBtn);
    const later = el("button", "swb-intake-close", "Leave it pending");
    later.type = "button";
    later.addEventListener("click", close);
    panel.appendChild(later);
    return surface;
  }

  function renderForm(surface) {
    panel.textContent = "";
    panel.appendChild(el("h3", "swb-intake-heading", "Add a model"));
    const form = el("div", "swb-intake-form");
    const id = field(form, "a short name for this model", "binding",
                     "authoring-model");
    const label = field(form, "how it should read in the menu", "label",
                        "Authoring model");
    const provider = field(form, "the provider taking custody", "provider",
                           "the provider name your broker knows");
    const endpoint = field(form, "where turns are sent", "endpoint",
                           "the request endpoint this model answers on");
    const dialectWrap = el("label", "swb-intake-field");
    dialectWrap.appendChild(el("span", "swb-intake-label",
                               "the request grammar it speaks"));
    const dialect = el("select", "swb-intake-dialect");
    for (const value of surface.dialects || []) {
      const opt = el("option", "", String(value));
      opt.value = String(value);
      dialect.appendChild(opt);
    }
    dialectWrap.appendChild(dialect);
    form.appendChild(dialectWrap);

    // THE KINDS COME FROM THE SERVER, and so does whether each one takes a
    // supplied value. This page names neither: the workspace's absolute rule
    // keeps that vocabulary out of every browser module, so the kind is rendered
    // by its label and submitted verbatim.
    const kindWrap = el("label", "swb-intake-field");
    kindWrap.appendChild(el("span", "swb-intake-label", "how you authenticate"));
    const kind = el("select", "swb-intake-kind");
    const kinds = Array.isArray(surface.auth_kinds) ? surface.auth_kinds : [];
    for (const entry of kinds) {
      const opt = el("option", "", String(entry.label || entry.kind));
      opt.value = String(entry.kind);
      kind.appendChild(opt);
    }
    kindWrap.appendChild(kind);
    form.appendChild(kindWrap);

    const valueWrap = el("label", "swb-intake-field swb-intake-value");
    valueWrap.appendChild(el("span", "swb-intake-label",
                             "paste it here — it is handed to the broker and "
                             + "this console keeps only the reference"));
    const value = el("input", "swb-intake-input");
    value.type = "password";
    value.name = "supplied";
    value.setAttribute("autocomplete", "off");
    valueWrap.appendChild(value);
    form.appendChild(valueWrap);
    const kindNote = el("p", "swb-intake-note");
    form.appendChild(kindNote);

    // NO FIELD THAT WOULD ACCEPT A VALUE IS PRESENTED FOR A KIND THAT TAKES
    // NONE. Hidden AND cleared, so a human who switched kinds mid-form cannot
    // leave a typed value behind in a control nobody can see.
    function syncKind() {
      const chosen = kinds.find((entry) => String(entry.kind) === kind.value);
      const takes = !!(chosen && chosen.accepts_secret === true);
      valueWrap.hidden = !takes;
      if (!takes) value.value = "";
      kindNote.textContent = chosen && typeof chosen.note === "string"
        ? chosen.note : "";
    }
    kind.addEventListener("change", syncKind);
    syncKind();

    panel.appendChild(form);
    panel.appendChild(status);
    const submit = el("button", "swb-intake-submit", "Hand it to the broker");
    submit.type = "button";
    submit.addEventListener("click", async () => {
      submit.disabled = true;
      say("handing it over…");
      const answer = await transports.enrol({
        binding: id.value.trim(),
        label: label.value.trim(),
        provider: provider.value.trim(),
        endpoint: endpoint.value.trim(),
        dialect: dialect.value,
        kind: kind.value,
      }, value.value);
      // CLEARED IMMEDIATELY, on both paths. The value has left this page one
      // way or another and there is no reason for the control to keep holding
      // it while a human reads a refusal.
      value.value = "";
      if (!answer || answer.ok !== true) {
        submit.disabled = false;
        say(refusalText(answer));
        return;
      }
      renderApproval({
        binding_id: (answer.declaration || {}).binding_id,
        availability: answer.availability,
      }, surface);
    });
    panel.appendChild(submit);
    const cancel = el("button", "swb-intake-close", "Cancel");
    cancel.type = "button";
    cancel.addEventListener("click", close);
    panel.appendChild(cancel);
  }

  function renderRefusal(surface) {
    panel.textContent = "";
    panel.appendChild(el("h3", "swb-intake-heading", "Add a model"));
    // THE FLOW REFUSES RATHER THAN DEGRADING, and it presents NO field that
    // would accept a value. A form that collected one with nowhere governed to
    // put it would have to hold it somewhere, and every somewhere available to
    // this browser is forbidden.
    panel.appendChild(el("p", "swb-intake-note",
      typeof surface.reason === "string" ? surface.reason
        : INTAKE_UNKNOWN_REFUSAL));
    const done = el("button", "swb-intake-close", "Close");
    done.type = "button";
    done.addEventListener("click", close);
    panel.appendChild(done);
  }

  const ready = (async () => {
    let surface = null;
    try {
      surface = await transports.surface();
    } catch (unused) {
      surface = null;  // a THROWN transport: the answer was not read
    }
    if (!surface || surface.offered !== true) {
      renderRefusal(surface || {});
      return;
    }
    renderForm(surface);
  })();

  return { ready, close };
}
