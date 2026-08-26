// The user-account menu — the header user-icon (👤) button and the small
// anchored dropdown it opens (add-dashboard-account-menu). It mirrors the
// settings.js header-popover contract exactly: an aside appended to <body>
// (the app shell `.wrap` clips overflow, so an in-header popover would be cut
// off), anchored under its button by script, closed on Escape and on any
// outside click, keyboard-focusable, and DOM-safe — every dynamic value bound
// via textContent/el(), never innerHTML.
//
// WHAT IT SHOWS is DISPLAY DATA the serve already reports on `/capabilities`:
//   * the signed-in username = `hosted_actor` (the gateway-stamped identity),
//     or the local actor / a generic "local session" label when absent;
//   * the access level DERIVED from the existing `/capabilities.actions` map —
//     read-only when no write/gate/edit action is granted, otherwise naming the
//     granted capabilities. This invents NO new authorization flag and consults
//     no identity; it reads the same verdict every other affordance reads.
//   * a logout control shown ONLY when `hosted_actor` is present, which
//     navigates the browser to the gateway-owned `/logout` (the dashboard
//     terminates no session itself — local mode has no gateway session to end,
//     so it renders no logout that would 404).
//
// It authorizes NOTHING. The menu is a reader of a stamped fact; the gateway is
// the identity authority and the write/gate/edit boundary is unchanged.

import { el } from "./helpers.js";

// The write-class capabilities: their absence is what "read-only" means, and
// their presence is what the access level names. Read from the existing
// `/capabilities.actions` map — no new flag is invented here.
const WRITE_ACTIONS = ["gate", "edit", "session"];

// Pure — node-testable. The signed-in username: the hosted actor when the
// gateway stamped one, else the resolved local actor, else the generic label.
export function accountName(caps) {
  const hosted = caps && caps.hosted_actor;
  if (typeof hosted === "string" && hosted) return hosted;
  const local = caps && caps.actor;
  if (typeof local === "string" && local) return local;
  return "local session";
}

// Pure — node-testable. The access level derived from the capability verdict:
// "read-only" when no write/gate/edit action is granted, otherwise the names of
// the granted write-class capabilities.
export function accessLevel(caps) {
  const actions = (caps && caps.actions) || {};
  const granted = WRITE_ACTIONS.filter((k) => actions[k] === true);
  return granted.length ? granted.join(", ") : "read-only";
}

// Pure — node-testable. A logout control belongs only to a hosted session:
// local/loopback has no gateway session to end.
export function hasLogout(caps) {
  const hosted = caps && caps.hosted_actor;
  return typeof hosted === "string" && !!hosted;
}

// The logout target: the gateway-owned route that clears the session cookie and
// redirects to /login. The dashboard delegates; it terminates nothing itself.
export const LOGOUT_ROUTE = "/logout";

// ---- the panel --------------------------------------------------------------

function buildPanel() {
  const panel = el("aside", "accountmenu");
  panel.id = "accountmenu";
  panel.hidden = true;
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "account");

  const head = el("header", "accountmenu-head");
  head.appendChild(el("span", "accountmenu-title", "account"));
  const close = el("button", "accountmenu-close", "✕");
  close.type = "button";
  close.title = "close account menu";
  close.setAttribute("aria-label", "close account menu");
  head.appendChild(close);

  // The signed-in line and the access-level line — both bound via textContent.
  const who = el("p", "accountmenu-who");
  const level = el("p", "accountmenu-level");

  // The logout control lives in its own row so it can be shown/removed cleanly
  // without disturbing the identity lines.
  const logoutRow = el("div", "accountmenu-logoutrow");

  panel.append(head, who, level, logoutRow);

  // One place that mirrors the current capabilities into the panel controls.
  // Rebuilt from stored caps on every update/open, so the menu can never show a
  // stale identity or verdict.
  function render(caps) {
    who.textContent = "Signed in as " + accountName(caps);
    level.textContent = "access: " + accessLevel(caps);
    // Rebuild the logout row from scratch each render (literal "" clear is the
    // only innerHTML the house posture allows; here we remove children instead).
    while (logoutRow.firstChild) logoutRow.removeChild(logoutRow.firstChild);
    if (hasLogout(caps)) {
      const logout = el("a", "accountmenu-logout", "log out");
      logout.href = LOGOUT_ROUTE;
      logout.setAttribute("role", "button");
      logoutRow.appendChild(logout);
    }
  }

  return { panel, close, render };
}

// Wire the header user-account button. Idempotent-by-construction (app.js calls
// it once); returns null when the button is absent (a trimmed host page), and
// otherwise a tiny controller so a caller/test can drive it without synthetic
// clicks and hand it fresh capabilities without a rebind or a second fetch.
export function initAccountMenu(opts) {
  const o = opts || {};
  const btn = document.getElementById(o.buttonId || "accountbtn");
  if (!btn) return null;

  const { panel, close, render } = buildPanel();
  document.body.appendChild(panel);

  // The capabilities object the serve reported on `/capabilities`. Passed in by
  // app.js (which already fetched it — no second fetch here) via the initial
  // option and refreshed through `update()` on each render.
  let caps = o.capabilities || null;
  render(caps);

  let open = false;

  function anchor() {
    const r = btn.getBoundingClientRect();
    panel.style.top = (r.bottom + 6) + "px";
    // right-align to the button, but never off the left edge on a narrow window
    const left = Math.max(8, r.right - panel.offsetWidth);
    panel.style.left = left + "px";
  }

  function setOpen(next) {
    open = next;
    panel.hidden = !next;
    btn.setAttribute("aria-expanded", String(next));
    if (next) {
      render(caps); // reflect the latest verdict at open time
      anchor();
    }
  }

  btn.addEventListener("click", (ev) => {
    ev.stopPropagation(); // the outside-click handler must not immediately close it
    setOpen(!open);
  });
  close.addEventListener("click", () => {
    setOpen(false);
    btn.focus();
  });
  // Escape closes from anywhere; click-outside closes on any pointer landing
  // outside the panel (the button's own handler stops propagation).
  document.addEventListener("keydown", (ev) => {
    if (open && ev.key === "Escape") {
      setOpen(false);
      btn.focus();
    }
  });
  document.addEventListener("click", (ev) => {
    if (open && !panel.contains(ev.target)) setOpen(false);
  });
  // the anchor is viewport-relative: re-derive it if the window moves under us
  window.addEventListener("resize", () => {
    if (open) anchor();
  });

  setOpen(false);
  return {
    element: panel,
    isOpen: () => open,
    toggle: () => setOpen(!open),
    close: () => setOpen(false),
    // app.js hands the freshly probed capabilities here after each render's
    // `/capabilities` probe — the same object the corner controls wait on, so
    // the menu needs no fetch of its own.
    update: (next) => { caps = next; render(caps); },
  };
}
