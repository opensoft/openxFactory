// Dashboard settings — the header gear (⚙) and the small anchored panel it
// opens. PURE FRONTEND: no data path of any kind (no fetch, no snapshot read).
// Settings are viewer preferences, not governance state, so they live only in
// localStorage under ONE JSON key (`xf-dashboard-settings`) — future settings
// join that object instead of growing new keys.
//
// Today the panel carries exactly one knob: "wheel diameter", the wheel's drum
// radius factor (radius = wheel-window height × factor). The parse/clamp/
// precedence math is NOT here — it is pure wheel geometry and lives in
// wheel-model.js (`DRUM`, `drumCandidate`, `drumFactor`), where the pytest node
// harness already exercises it.
//
// LOAD-TIME PRECEDENCE: an explicit `?drum=` URL param wins (it is the
// compare-by-URL tuning tool), else the saved setting, else the default 1.
// Moving the slider always wins from then on: it updates the live value, saves
// it, and announces it.
//
// LIVE APPLICATION: every change dispatches a `xf-settings-change` CustomEvent
// on `document` carrying the resolved values. Views subscribe (wheel.js redraws
// its cylinder on the next frame) rather than re-reading storage, so there is
// one owner of the live value and no polling.
//
// DOM-safety: every dynamic value is bound via textContent/value — never
// innerHTML (the house posture).

import { DRUM, drumCandidate, drumFactor } from "./wheel-model.js";
import { el } from "./helpers.js";

export const SETTINGS_KEY = "xf-dashboard-settings";
export const SETTINGS_EVENT = "xf-settings-change";

// ---- storage (best-effort; a blocked or corrupt store is not an error) -------
// localStorage throws outright in some privacy modes, `getItem` can return
// anything a previous version (or another tab) wrote, and the quota can be
// full. None of that may break the dashboard, so every access degrades to "no
// saved settings" / "not saved".

function storageOf(store) {
  if (store) return store;
  try {
    return window.localStorage;
  } catch {
    return null;
  }
}

// The saved settings object, always a plain object (never null, never an array).
export function readSettings(store) {
  const s = storageOf(store);
  if (!s) return {};
  let raw = null;
  try {
    raw = s.getItem(SETTINGS_KEY);
  } catch {
    return {};
  }
  if (!raw) return {};
  try {
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return {};
    return parsed;
  } catch {
    return {}; // corrupt JSON: treated as absent, and the next write repairs it
  }
}

// Merge a patch into the saved object (so one knob never clobbers another).
function saveSettings(patch, store) {
  const s = storageOf(store);
  if (!s) return;
  const next = { ...readSettings(s), ...patch };
  try {
    s.setItem(SETTINGS_KEY, JSON.stringify(next));
  } catch {
    /* quota/private mode: the session keeps the live value, it just won't persist */
  }
}

// ---- the live values --------------------------------------------------------

function urlDrumRaw(loc) {
  const search = (loc || window.location).search || "";
  return new URLSearchParams(search).get("drum");
}

let liveDrum = null; // resolved once per page, then owned by the slider

// The drum factor in force RIGHT NOW. First call resolves the load-time
// precedence; later calls return whatever the slider last set (so a view
// mounted after a change picks up the current value, not the stored one).
export function currentDrumFactor(opts) {
  if (liveDrum === null) {
    const o = opts || {};
    liveDrum = drumFactor(urlDrumRaw(o.location), readSettings(o.storage).wheelDiameter);
  }
  return liveDrum;
}

// Set + save + announce. Out-of-range input clamps, garbage falls back to the
// default (drumCandidate's contract); the announced number is the applied one.
export function setDrumFactor(value, opts) {
  const o = opts || {};
  const next = drumCandidate(value) ?? DRUM.default;
  liveDrum = next;
  saveSettings({ wheelDiameter: next }, o.storage);
  document.dispatchEvent(new CustomEvent(SETTINGS_EVENT, {
    detail: { drum: next },
  }));
  return next;
}

function drumLabel(value) {
  return value.toFixed(2) + "×";
}

// ---- the panel --------------------------------------------------------------
// A fixed-position popover appended to <body> and anchored under the gear by
// script: the app shell (`.wrap`) clips overflow, so an in-header absolute
// popover would be cut off. Same idiom as dispose.js's refusal panel.

function buildPanel(onDrum) {
  const panel = el("aside", "settingspanel");
  panel.id = "settingspanel";
  panel.hidden = true;
  panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "dashboard settings");

  const head = el("header", "settingspanel-head");
  head.appendChild(el("span", "settingspanel-title", "settings"));
  const close = el("button", "settingspanel-close", "✕");
  close.type = "button";
  close.title = "close settings";
  close.setAttribute("aria-label", "close settings");
  head.appendChild(close);

  const row = el("div", "settingsrow");
  const label = el("label", "settingslabel", "wheel diameter");
  label.htmlFor = "set-wheel-diameter";
  const range = document.createElement("input");
  range.className = "settingsrange";
  range.id = "set-wheel-diameter";
  range.type = "range";
  range.min = String(DRUM.min);
  range.max = String(DRUM.max);
  range.step = String(DRUM.step);
  range.setAttribute("aria-label", "wheel diameter (drum radius factor)");
  const readout = el("output", "settingsval");
  readout.htmlFor = "set-wheel-diameter";
  const reset = el("button", "settingsreset", "reset");
  reset.type = "button";
  reset.title = "back to the default " + drumLabel(DRUM.default);
  row.append(label, range, readout, reset);

  const note = el("p", "settingsnote",
    "drum radius = wheel-window height × this factor. " +
    drumLabel(DRUM.min) + " wraps the horizon inside the window (slot-drum), " +
    drumLabel(DRUM.default) + " is the gentle wrap, " + drumLabel(DRUM.max) +
    " flattens it. An explicit ?drum= URL wins until you move the slider.");

  panel.append(head, row, note);

  // one place that mirrors a value into the controls
  const show = (value) => {
    range.value = String(value);
    readout.textContent = drumLabel(value);
  };
  range.addEventListener("input", () => show(onDrum(Number.parseFloat(range.value))));
  reset.addEventListener("click", () => show(onDrum(DRUM.default)));

  return { panel, close, show };
}

// Wire the header gear. Idempotent-by-construction (app.js calls it once);
// returns null when the button is absent (a trimmed host page), and otherwise a
// tiny controller so a caller/test can drive it without synthetic clicks.
export function initSettings(opts) {
  const o = opts || {};
  const btn = document.getElementById(o.buttonId || "settingsbtn");
  if (!btn) return null;

  const { panel, close, show } = buildPanel((v) => setDrumFactor(v, o));
  document.body.appendChild(panel);
  show(currentDrumFactor(o));

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
    if (next) anchor();
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
  // outside the panel (the gear's own handler stops propagation).
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
    setDrum: (v) => show(setDrumFactor(v, o)),
  };
}
