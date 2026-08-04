// "Open in NotebookLM" tile action (v2 local-backend seam debut). This is the
// ONLY module besides app.js (the snapshot fetch) and viewer.js (the /source
// pass-through) that issues a network call: it probes GET /capabilities ONCE at
// load and POSTs to /actions/notebook on click. Both routes exist only on a
// loopback LOCAL backend (serve.py); the static SERVED image (nginx) serves
// neither, so probeCapabilities degrades to "notebook: false" and no button is
// ever mounted — the capability-probe degradation story in one place.
//
// DOM-SAFETY: every dynamic value binds through textContent (helpers discipline);
// innerHTML is never assigned here. Errors surface inline via textContent only.

export const CAPABILITIES_ROUTE = "/capabilities";
export const ACTIONS_NOTEBOOK_ROUTE = "/actions/notebook";

// Local textContent-first element builder (this view keeps its own, like the
// other textContent-family views — see helpers.js scope note).
function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text != null) node.textContent = text;
  return node;
}

// pure — node-testable. True only when the probe EXPLICITLY reported the
// notebook action available; any other shape reads as unavailable.
export function notebookCapable(caps) {
  return caps?.actions?.notebook === true;
}

// Probe the local backend ONCE. Any non-OK response (the static image 404s this
// route) or a network failure (file://) degrades to "not available" — never
// throws, never blocks the dashboard. `injectedFetch` is for tests.
export async function probeCapabilities(injectedFetch) {
  try {
    const response = injectedFetch
      ? await injectedFetch(CAPABILITIES_ROUTE, { cache: "no-store" })
      : await fetch(CAPABILITIES_ROUTE, { cache: "no-store" });
    if (!response?.ok) return { actions: { notebook: false } };
    return await response.json();
  } catch {
    return { actions: { notebook: false } };
  }
}

// POST one tile action; resolves to the backend's {url, notebook_alias,
// sources, created}, or throws an Error carrying the backend's fixed catalog
// message (preferring the human `message` over the stable `error` code).
export async function postNotebookAction(body, injectedFetch) {
  const opts = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
  const response = injectedFetch
    ? await injectedFetch(ACTIONS_NOTEBOOK_ROUTE, opts)
    : await fetch(ACTIONS_NOTEBOOK_ROUTE, opts);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data?.message || data?.error || ("HTTP " + response.status));
  return data;
}

// One click cycle: disable + spinner text -> POST -> open the url in a new tab
// -> restore; error -> inline message (textContent). Extracted so `button`
// stays a small factory.
async function runClick(btn, msg, kind, id, post, open) {
  const label = btn.textContent;
  btn.disabled = true;
  btn.textContent = "opening NotebookLM…";
  msg.textContent = "";
  try {
    const result = await post({ tile_kind: kind, tile_id: id });
    if (result?.url) open(result.url);
    else msg.textContent = "no notebook url returned";
  } catch (err) {
    msg.textContent = "could not open NotebookLM: " + (err?.message || "error");
  } finally {
    btn.disabled = false;
    btn.textContent = label;
  }
}

// The action controller. `button(kind, id)` returns a mount-ready element when
// enabled, else null — so views append `notebook.button(...)` guarded by a
// truthiness check and nothing renders when the capability is absent. `post`
// and `open` are injectable for tests.
export function createNotebookAction(opts) {
  const options = opts || {};
  const enabled = Boolean(options.enabled);
  const post = options.post || postNotebookAction;
  const open = options.open
    || ((url) => window.open(url, "_blank", "noopener"));

  function button(kind, id) {
    if (!enabled) return null;
    const wrap = el("span", "nb-action");
    const btn = el("button", "nbbtn", "◇ open in NotebookLM");
    btn.type = "button";
    const msg = el("span", "nb-msg");
    btn.addEventListener("click", (ev) => {
      ev.stopPropagation();  // never trip the funnel card's click-to-pin gesture
      runClick(btn, msg, kind, id, post, open);
    });
    wrap.appendChild(btn);
    wrap.appendChild(msg);
    return wrap;
  }

  return { enabled, button };
}
