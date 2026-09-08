"""DOM behaviour of the wheel action-row verbs (011 add-wheel-action-verbs).

Drives the REAL `dispose.js` under node against the minimal DOM shim this repo
already uses for view probes. Nothing here reads a module's SOURCE — every claim
is made by mounting, clicking, and inspecting the resulting tree, so a passing
test means the behaviour exists rather than that the code looks right.

The shim's `innerHTML` setter throws on any non-empty assignment, which is what
turns "refusals render as text" from a promise into a mechanical guarantee
(contracts/wheel-action-row.md D1).

Pins D1–D6.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"

_DOM_SHIM = r"""
class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = []; this.attributes = {}; this.listeners = {};
    this.className = ''; this._text = ''; this.disabled = false;
    this.value = ''; this.hidden = false; this.type = '';
    this.dataset = {};
    this.focused = false;
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) { this.children = []; this._text = String(value); }
  set innerHTML(value) {
    if (String(value) !== '') throw new Error('only literal "" clears are allowed');
    this.children = []; this._text = '';
  }
  appendChild(child) { child.parent = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  insertBefore(child, ref) {
    const at = this.children.indexOf(ref);
    this.children.splice(at < 0 ? 0 : at, 0, child);
    return child;
  }
  remove() {
    if (!this.parent) return;
    const at = this.parent.children.indexOf(this);
    if (at >= 0) this.parent.children.splice(at, 1);
  }
  contains(node) {
    return this === node || this.children.some((c) => c.contains(node));
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return this.attributes[name]; }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() { this.focused = true; globalThis.__focusLog.push(this); }
  querySelector(selector) {
    const cls = selector.replace(/^\./, '');
    return this.walk().find((n) => String(n.className).split(' ').includes(cls))
      || null;
  }
  walk() {
    return this.children.reduce((all, c) => all.concat(c.walk()), [this]);
  }
}
globalThis.__focusLog = [];
globalThis.document = {
  createElement: (tag) => new Node(tag),
  createTextNode: (text) => { const n = new Node('#text'); n._text = String(text);
    return n; },
  body: new Node('body'),
};
globalThis.window = {
  prompt: () => { throw new Error('a blocking prompt is forbidden for this verb'); },
};
function byClass(root, cls) {
  return root.walk().filter((n) => String(n.className).split(' ').includes(cls));
}
async function click(node) {
  for (const fn of node.listeners.click || []) await fn({ stopPropagation() {} });
}
async function keydown(node, key) {
  for (const fn of node.listeners.keydown || []) {
    await fn({ key, preventDefault() {}, stopPropagation() {} });
  }
}
// Records whether the handler stopped the event from bubbling. The wheel
// collapses an expanded tile on ANY Escape that reaches it, so a reason form
// that lets Escape bubble cancels itself AND destroys the row it lives in.
async function keydownProbe(node, key) {
  let stopped = false;
  for (const fn of node.listeners.keydown || []) {
    await fn({ key, preventDefault() {}, stopPropagation() { stopped = true; } });
  }
  return stopped;
}
function panelText() {
  const panel = globalThis.document.body.walk()
    .filter((n) => String(n.className).includes('refusalpanel-msg'));
  return panel.map((n) => n.textContent);
}
"""

_HARNESS = _DOM_SHIM + """
import { mountWheelVerb, commissionedVerb, resetSessionCommissions }
  from './dispose.js';
import { actionsFor, actionRowIsStale } from './wheel-model.js';

const results = {};
const OK = (extra) => async () => ({ status: 200,
  json: async () => ({ ok: true, verb: 'x', workflow: 'w', record: 'r',
                       job: 'j', ...extra }) });
const REFUSE = (message) => async () => ({ status: 409,
  json: async () => ({ ok: false, error: 'gate_refused', message }) });

// ---- D1: a refusal carrying markup renders as LITERAL TEXT ----------------
{
  resetSessionCommissions();
  const row = new Node('div');
  const evil = '<img src=x onerror=alert(1)> & "quoted"';
  mountWheelVerb(row, { id: 'pos-a' }, {
    verb: 'research-brief', label: 'brief', fetcher: REFUSE(evil) });
  await click(byClass(row, 'disposebtn')[0]);
  const texts = panelText();
  results.d1_literal = texts.some((t) => t.includes(evil));
  results.d1_no_element_from_message =
    !globalThis.document.body.walk().some((n) => n.tagName === 'IMG');
}

// ---- D4: success decorates + retires ONLY that verb -----------------------
{
  resetSessionCommissions();
  const row = new Node('div');
  let applied = 0;
  mountWheelVerb(row, { id: 'pos-a' }, {
    verb: 'research-brief', label: 'brief', fetcher: OK({ workflow: 'wf-brief' }),
    onApplied: () => { applied += 1; } });
  await click(byClass(row, 'disposebtn')[0]);
  results.d4_marked_commissioned = commissionedVerb('research-brief', 'pos-a') === 'wf-brief';
  results.d4_other_verb_untouched = commissionedVerb('promote-to-staging', 'pos-a') === null;
  results.d4_other_target_untouched = commissionedVerb('research-brief', 'pos-b') === null;
  results.d4_onApplied = applied;
  results.d4_button_disabled = byClass(row, 'disposebtn')[0].disabled === true;
}

// ---- D5: a refusal re-enables and retires NOTHING -------------------------
{
  resetSessionCommissions();
  const row = new Node('div');
  mountWheelVerb(row, { id: 'pos-a' }, {
    verb: 'promote-to-staging', label: 'promote', fetcher: REFUSE('not promotable') });
  const btn = byClass(row, 'disposebtn')[0];
  await click(btn);
  results.d5_reenabled = btn.disabled === false;
  results.d5_not_retired = commissionedVerb('promote-to-staging', 'pos-a') === null;
}

// ---- D6: a demote response with NO workflow field is handled --------------
{
  resetSessionCommissions();
  const row = new Node('div');
  let threw = null;
  mountWheelVerb(row, { id: 'add-x' }, {
    verb: 'demote', label: 'demote', collectReason: () => 'because',
    fetcher: async () => ({ status: 200, json: async () => ({
      ok: true, verb: 'demote', change_id: 'add-x',
      plan: 'p.yaml', record: 'r.yaml' }) }) });
  try { await click(byClass(row, 'disposebtn')[0]); } catch (e) { threw = String(e); }
  results.d6_no_throw = threw;
  results.d6_recorded = commissionedVerb('demote', 'add-x') !== null;
  results.d6_panel_mentions_plan = panelText().some((t) => t.includes('p.yaml'));
}

// ---- D2/D3: the reason form cancels and refuses an empty submit -----------
{
  resetSessionCommissions();
  let dispatches = 0;
  const counting = async () => { dispatches += 1;
    return { status: 200, json: async () => ({ ok: true, plan: 'p', record: 'r' }) }; };

  // cancel via Escape
  const row = new Node('div');
  mountWheelVerb(row, { id: 'add-x' }, {
    verb: 'demote', label: 'demote', fetcher: counting });
  await click(byClass(row, 'disposebtn')[0]);
  const form = byClass(row, 'wheelreasonform')[0];
  results.d2_form_opened = !!form;
  const input = byClass(row, 'wheelreasoninput')[0];
  results.d2_input_labelled = !!(input && input.attributes['aria-label']);
  results.d2_focus_on_open = globalThis.__focusLog.includes(input);
  await keydown(input, 'Escape');
  results.d2_cancel_dispatched_nothing = dispatches === 0;
  results.d2_form_closed = byClass(row, 'wheelreasonform').length === 0;
  results.d2_focus_returned = globalThis.__focusLog.slice(-1)[0]
    === byClass(row, 'disposebtn')[0];

  // empty submit
  await click(byClass(row, 'disposebtn')[0]);
  const input2 = byClass(row, 'wheelreasoninput')[0];
  input2.value = '   ';
  await keydown(input2, 'Enter');
  results.d3_empty_submit_dispatched_nothing = dispatches === 0;
  results.d3_form_still_open = byClass(row, 'wheelreasonform').length === 1;

  // a real reason dispatches exactly once
  input2.value = 'not agreed';
  await keydown(input2, 'Enter');
  results.d3_real_reason_dispatched = dispatches === 1;
}

// ---- D8: retirement REMOVES the control; a refusal does NOT --------------
//
// FR-033: "Retirement MUST REMOVE the row from the rendered action row rather
// than render a disabled control." The wheel's redraw has to reconcile the row
// against what the table now offers. This drives the REAL mounters and the REAL
// `actionsFor` / `actionRowIsStale`; the ~6 lines of rebuild glue mirror what
// `syncActions` does (that function is a closure inside wheel.js and cannot be
// imported). The true end-to-end proof is the Playwright matrix, which asserts
// absence in the real page.
{
  resetSessionCommissions();
  const item = { id: 'pos-a', demo: false, derivedPending: false,
                 ref: { id: 'pos-a', state: 'latent' } };
  const tile = new Node('div');
  const OKW = async () => ({ status: 200,
    json: async () => ({ ok: true, workflow: 'wf', record: 'r', job: 'j' }) });
  const NO = async () => ({ status: 409,
    json: async () => ({ ok: false, error: 'gate_refused', message: 'nope' }) });
  let fetcher = OKW;
  const syncRow = () => {
    const desired = actionsFor('possibles', item,
      { gate: true, commissioned: (v) => !!commissionedVerb(v, item.id) }).map(a => a.id);
    let row = tile.children.find(c => String(c.className).includes('wheelactions'));
    if (row) {
      const mounted = String(row.dataset.verbs || '').split(' ').filter(Boolean);
      if (!actionRowIsStale(mounted, desired)) return row;
      row.remove();
    }
    row = new Node('div'); row.className = 'wheelactions';
    row.dataset.verbs = desired.join(' ');
    for (const id of desired) {
      if (id === 'workbench') continue;
      mountWheelVerb(row, item, { verb: id, label: id, fetcher: (...a) => fetcher(...a) });
    }
    tile.appendChild(row);
    return row;
  };
  const ctrl = (row, verb) =>
    row.walk().find(n => String(n.className).includes('dispose-' + verb)) || null;

  let row = syncRow();
  results.d8_initial = [...row.walk()].filter(n => String(n.className).includes('disposebtn')).length;
  // a REFUSAL must leave the control present AND enabled
  fetcher = NO;
  await click(ctrl(row, 'promote-to-staging'));
  row = syncRow();
  const afterRefusal = ctrl(row, 'promote-to-staging');
  results.d8_refusal_control_present = afterRefusal !== null;
  results.d8_refusal_control_enabled = afterRefusal ? afterRefusal.disabled === false : null;
  // a SUCCESS must REMOVE the control on the next redraw
  fetcher = OKW;
  await click(ctrl(row, 'promote-to-staging'));
  row = syncRow();
  results.d8_retired_control_absent = ctrl(row, 'promote-to-staging') === null;
  const sib = ctrl(row, 'research-brief');
  results.d8_sibling_present = sib !== null;
  results.d8_sibling_enabled = sib ? sib.disabled === false : null;
}

// ---- D7: the reason form must not let its keys reach the wheel -----------
{
  resetSessionCommissions();
  const row = new Node('div');
  mountWheelVerb(row, { id: 'add-x' }, {
    verb: 'demote', label: 'demote',
    fetcher: async () => ({ status: 200, json: async () => ({ ok: true, plan: 'p', record: 'r' }) }) });
  await click(byClass(row, 'disposebtn')[0]);
  const input = byClass(row, 'wheelreasoninput')[0];
  results.d7_escape_stops_propagation = await keydownProbe(input, 'Escape');
  await click(byClass(row, 'disposebtn')[0]);
  const input2 = byClass(row, 'wheelreasoninput')[0];
  input2.value = 'a reason';
  results.d7_enter_stops_propagation = await keydownProbe(input2, 'Enter');
}

// ---- the gate-off contract: the mounter is never reached -------------------
console.log(JSON.stringify(results));
"""


def _run(tmp_path):
    """Drive the REAL dispose.js under node against the minimal DOM."""
    if NODE is None:
        pytest.skip("node not available for the DOM-driven action-row probe")
    views = tmp_path / "views"
    views.mkdir()
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    # `intent-feed.js` rides along because dispose.js imports it
    # (add-ideation-intent-plane task 4.4: the tray's hosted transport). This
    # probe drives the LOCAL path only — no `opts.intent` is ever passed — so
    # the module is present purely to make the import resolve.
    for name in ("dispose.js", "helpers.js", "wheel-model.js", "intent-feed.js"):
        shutil.copy(WEB / "views" / name, views / name)
    harness = views / "wheel-verbs.js"
    harness.write_text(_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


# ---- D1 -------------------------------------------------------------------

def test_d1_refusal_message_renders_as_literal_text(tmp_path):
    """D1: a refusal carrying markup appears verbatim and creates no element.
    The shim throws on any non-empty innerHTML, so this is mechanical."""
    r = _run(tmp_path)
    assert r["d1_literal"] is True
    assert r["d1_no_element_from_message"] is True


# ---- D4 -------------------------------------------------------------------

def test_d4_success_retires_only_that_verb_on_that_target(tmp_path):
    """D4 / FR-027 / FR-033: retirement is keyed by (verb, target), so one
    commission never retires another verb or the same verb elsewhere."""
    r = _run(tmp_path)
    assert r["d4_marked_commissioned"] is True
    assert r["d4_other_verb_untouched"] is True
    assert r["d4_other_target_untouched"] is True
    assert r["d4_onApplied"] == 1
    assert r["d4_button_disabled"] is True


# ---- D5 -------------------------------------------------------------------

def test_d5_a_refusal_re_enables_and_retires_nothing(tmp_path):
    """D5: the human must be able to correct the input and retry."""
    r = _run(tmp_path)
    assert r["d5_reenabled"] is True
    assert r["d5_not_retired"] is True


# ---- D6 -------------------------------------------------------------------

def test_d6_demote_response_without_a_workflow_field_is_handled(tmp_path):
    """D6 / FR-033a: demote commissions no workflow, so the browser must not
    require one — the session marker is a per-verb value, not a workflow id."""
    r = _run(tmp_path)
    assert r["d6_no_throw"] is None
    assert r["d6_recorded"] is True
    assert r["d6_panel_mentions_plan"] is True


# ---- D2 / D3 --------------------------------------------------------------

def test_d2_reason_form_is_accessible_and_cancel_dispatches_nothing(tmp_path):
    """D2 / FR-006 / FR-006a: a labelled in-page form, focus on open, Escape
    cancels, focus returns to the control that opened it. No browser prompt —
    the harness makes window.prompt throw, so using one fails the run."""
    r = _run(tmp_path)
    assert r["d2_form_opened"] is True
    assert r["d2_input_labelled"] is True
    assert r["d2_focus_on_open"] is True
    assert r["d2_cancel_dispatched_nothing"] is True
    assert r["d2_form_closed"] is True
    assert r["d2_focus_returned"] is True


def test_d3_empty_reason_dispatches_nothing_and_a_real_one_dispatches_once(tmp_path):
    """D3 / FR-006: an empty submit keeps the form open and sends nothing; a
    real reason sends exactly one request."""
    r = _run(tmp_path)
    assert r["d3_empty_submit_dispatched_nothing"] is True
    assert r["d3_form_still_open"] is True
    assert r["d3_real_reason_dispatched"] is True


# ---- D7 (regression: found by interactive Playwright, 2026-08-02) ---------

def test_d7_reason_form_keys_do_not_bubble_to_the_wheel(tmp_path):
    """D7 — the reason form MUST stop its own Enter/Escape from propagating.

    Found by driving the real dashboard with Playwright, not by unit test: the
    wheel collapses an expanded tile on any Escape that reaches it
    (`wheel.js`: "Escape collapses from anywhere the keypress can reach"). A
    reason form that lets Escape bubble therefore cancels itself AND destroys
    the action row it lives in — so the verb is no longer offered and there is
    no control left to return focus to, breaking FR-006a and the contract's
    "cancel dispatches nothing and leaves the verb offered".

    The earlier D2 test could not catch this: it dispatches a synthetic event
    straight at the input, where there is no ancestor handler to reach.
    """
    r = _run(tmp_path)
    assert r["d7_escape_stops_propagation"] is True
    assert r["d7_enter_stops_propagation"] is True


# ---- D8 (regression: found by supervisor rerun of the matrix, 2026-08-02) --

def test_d8_retirement_removes_the_control_and_a_refusal_does_not(tmp_path):
    """D8 — FR-033: retirement REMOVES the row entry; it does not disable it.

    Found by an independent rerun of the Playwright matrix: after a successful
    commission the verb stayed in the row as a DISABLED control, because the
    wheel's redraw returned early whenever a row already existed. My own matrix
    accepted that, having asserted retirement loosely (disabled OR gone) — a
    weak assertion is how a defect passes a test that was supposed to catch it.

    The two halves must both hold, and they pull in opposite directions:
    a SUCCESS removes the control, a REFUSAL keeps it and re-enables it.
    """
    r = _run(tmp_path)
    assert r["d8_initial"] == 2                       # both possibles verbs mounted
    assert r["d8_refusal_control_present"] is True    # refusal != retirement
    assert r["d8_refusal_control_enabled"] is True
    assert r["d8_retired_control_absent"] is True     # FR-033: removed, not disabled
    assert r["d8_sibling_present"] is True
    assert r["d8_sibling_enabled"] is True
