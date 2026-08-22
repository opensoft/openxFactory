"""DOM behaviour of the user-account menu (add-dashboard-account-menu).

Drives the REAL `account-menu.js` under node against the minimal DOM shim this
repo already uses for view probes (see test_wheel_verbs_dom.py). Nothing here
reads the module's SOURCE — every claim is made by mounting, opening, and
inspecting the resulting tree, so a passing test means the behaviour exists.

The shim's `innerHTML` setter throws on any non-empty assignment, which turns
"every dynamic value is bound via textContent" from a promise into a mechanical
guarantee: the harness could not complete if the view ever reached innerHTML.

Pins the four ADDED requirements' menu scenarios:
  * hosted session → username, derived access level, an enabled logout to /logout
  * local session  → the local actor or a generic label, and NO logout
  * the header-popover contract: open/close on the button, Escape, outside click,
    aria-expanded on the button, anchored under it.
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
    this.className = ''; this._text = ''; this.hidden = false; this.type = '';
    this.title = ''; this.href = ''; this.id = '';
    this.style = {}; this.offsetWidth = 40; this.focused = false;
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) { this.children = []; this._text = String(value); }
  set innerHTML(value) {
    if (String(value) !== '') throw new Error('only literal "" clears are allowed');
    this.children = []; this._text = '';
  }
  get firstChild() { return this.children[0] || null; }
  appendChild(child) { child.parent = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  removeChild(child) {
    const at = this.children.indexOf(child);
    if (at >= 0) this.children.splice(at, 1);
    return child;
  }
  contains(node) {
    return this === node || this.children.some((c) => c.contains(node));
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return this.attributes[name]; }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() { this.focused = true; globalThis.__focusLog.push(this); }
  getBoundingClientRect() { return { top: 10, bottom: 30, left: 100, right: 140,
    width: 40, height: 20 }; }
  walk() {
    return this.children.reduce((all, c) => all.concat(c.walk()), [this]);
  }
}
globalThis.__focusLog = [];
const __byId = {};
const __docListeners = {};
globalThis.document = {
  createElement: (tag) => new Node(tag),
  createTextNode: (text) => { const n = new Node('#text'); n._text = String(text);
    return n; },
  body: new Node('body'),
  getElementById: (id) => __byId[id] || null,
  addEventListener: (type, fn) => { (__docListeners[type] ||= []).push(fn); },
};
globalThis.window = { addEventListener: () => {} };

function registerButton(id) {
  const btn = new Node('button'); btn.id = id; __byId[id] = btn; return btn;
}
async function fire(node, type, ev) {
  for (const fn of node.listeners[type] || []) await fn(ev || {});
}
async function fireDoc(type, ev) {
  for (const fn of __docListeners[type] || []) await fn(ev || {});
}
function panelOf() {
  return globalThis.document.body.children.find(
    (n) => String(n.className).includes('accountmenu')) || null;
}
function byClass(root, cls) {
  return root.walk().filter((n) => String(n.className).split(' ').includes(cls));
}
"""

_HARNESS = _DOM_SHIM + """
import { initAccountMenu } from './account-menu.js';

const results = {};
const clickEv = () => ({ stopPropagation() {} });

// ---- HOSTED session: username, access level, enabled logout to /logout -----
{
  const btn = registerButton('accountbtn');
  const caps = { hosted_actor: 'alice', actor: null,
    actions: { gate: true, edit: true, session: true, notebook: false, refresh: true } };
  const ctrl = initAccountMenu({ buttonId: 'accountbtn', capabilities: caps });
  results.hosted_returns_controller = !!ctrl;
  const panel = panelOf();
  results.hosted_panel_appended = !!panel;
  results.hosted_aria_controls = btn.getAttribute('aria-controls') === undefined
    ? null : btn.getAttribute('aria-controls');   // set in HTML, not the view
  // starts closed
  results.hosted_starts_closed = panel.hidden === true
    && btn.getAttribute('aria-expanded') === 'false';
  // open via the button
  await fire(btn, 'click', clickEv());
  results.hosted_open_after_click = panel.hidden === false
    && btn.getAttribute('aria-expanded') === 'true';
  results.hosted_anchored = panel.style.top === '36px'; // bottom(30)+6
  const who = byClass(panel, 'accountmenu-who')[0];
  const level = byClass(panel, 'accountmenu-level')[0];
  results.hosted_username = who ? who.textContent : null;
  results.hosted_level = level ? level.textContent : null;
  const logout = byClass(panel, 'accountmenu-logout')[0];
  results.hosted_logout_present = !!logout;
  results.hosted_logout_tag = logout ? logout.tagName : null;
  results.hosted_logout_href = logout ? logout.href : null;
  // Escape closes and returns focus to the button
  await fireDoc('keydown', { key: 'Escape' });
  results.hosted_escape_closed = panel.hidden === true
    && btn.getAttribute('aria-expanded') === 'false';
  results.hosted_escape_focus = globalThis.__focusLog.slice(-1)[0] === btn;
  // reopen, then an OUTSIDE click closes it
  await fire(btn, 'click', clickEv());
  const stray = new Node('div');
  await fireDoc('click', { target: stray });
  results.hosted_outside_click_closed = panel.hidden === true;
  // reset the shared body/registry for the next case
  globalThis.document.body.children = [];
  delete __byId['accountbtn'];
}

// ---- LOCAL session WITH a resolved actor: name shown, NO logout ------------
{
  registerButton('accountbtn');
  const caps = { hosted_actor: null, actor: 'Session Harness',
    actions: { gate: false, edit: false, session: false, notebook: false, refresh: true } };
  initAccountMenu({ buttonId: 'accountbtn', capabilities: caps });
  const panel = panelOf();
  const who = byClass(panel, 'accountmenu-who')[0];
  const level = byClass(panel, 'accountmenu-level')[0];
  results.local_actor_username = who ? who.textContent : null;
  results.local_actor_level = level ? level.textContent : null;
  results.local_actor_no_logout = byClass(panel, 'accountmenu-logout').length === 0;
  globalThis.document.body.children = [];
  delete __byId['accountbtn'];
}

// ---- LOCAL session with NO actor: generic label, NO logout -----------------
{
  registerButton('accountbtn');
  const caps = { hosted_actor: null, actor: null, actions: {} };
  initAccountMenu({ buttonId: 'accountbtn', capabilities: caps });
  const panel = panelOf();
  const who = byClass(panel, 'accountmenu-who')[0];
  const level = byClass(panel, 'accountmenu-level')[0];
  results.generic_username = who ? who.textContent : null;
  results.generic_level = level ? level.textContent : null;
  results.generic_no_logout = byClass(panel, 'accountmenu-logout').length === 0;
  globalThis.document.body.children = [];
  delete __byId['accountbtn'];
}

// ---- a trimmed host page (no button) returns null --------------------------
{
  results.absent_button_returns_null = initAccountMenu({ buttonId: 'accountbtn' }) === null;
}

// ---- update() refreshes the identity without a rebind ----------------------
{
  registerButton('accountbtn');
  const ctrl = initAccountMenu({ buttonId: 'accountbtn',
    capabilities: { hosted_actor: null, actor: null, actions: {} } });
  const before = panelOf();
  ctrl.update({ hosted_actor: 'bob',
    actions: { gate: true, edit: false, session: false, notebook: false, refresh: true } });
  const after = panelOf();
  results.update_no_rebind = before === after
    && globalThis.document.body.children.filter(
        (n) => String(n.className).includes('accountmenu')).length === 1;
  results.update_username = byClass(after, 'accountmenu-who')[0].textContent;
  results.update_logout_present = byClass(after, 'accountmenu-logout').length === 1;
  globalThis.document.body.children = [];
  delete __byId['accountbtn'];
}

console.log(JSON.stringify(results));
"""


def _run(tmp_path):
    if NODE is None:
        pytest.skip("node not available for the DOM-driven account-menu probe")
    views = tmp_path / "views"
    views.mkdir()
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    for name in ("account-menu.js", "helpers.js"):
        shutil.copy(WEB / "views" / name, views / name)
    harness = views / "account-menu-probe.js"
    harness.write_text(_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert proc.returncode == 0, f"node harness failed:\n{proc.stderr}"
    return json.loads(proc.stdout)


def test_hosted_session_shows_username_level_and_logout(tmp_path):
    r = _run(tmp_path)
    assert r["hosted_returns_controller"] is True
    assert r["hosted_panel_appended"] is True
    assert r["hosted_starts_closed"] is True
    assert r["hosted_open_after_click"] is True
    assert r["hosted_anchored"] is True
    assert r["hosted_username"] == "Signed in as alice"
    # the derived access level names the granted write-class capabilities
    assert "gate" in r["hosted_level"] and "read-only" not in r["hosted_level"]
    assert r["hosted_logout_present"] is True
    assert r["hosted_logout_tag"] == "A"
    assert r["hosted_logout_href"] == "/logout"


def test_hosted_menu_closes_on_escape_and_outside_click(tmp_path):
    r = _run(tmp_path)
    assert r["hosted_escape_closed"] is True
    assert r["hosted_escape_focus"] is True
    assert r["hosted_outside_click_closed"] is True


def test_local_session_with_actor_shows_name_and_no_logout(tmp_path):
    r = _run(tmp_path)
    assert r["local_actor_username"] == "Signed in as Session Harness"
    assert r["local_actor_level"] == "access: read-only"
    assert r["local_actor_no_logout"] is True


def test_local_session_without_actor_shows_generic_label_and_no_logout(tmp_path):
    r = _run(tmp_path)
    assert r["generic_username"] == "Signed in as local session"
    assert r["generic_level"] == "access: read-only"
    assert r["generic_no_logout"] is True


def test_a_trimmed_host_page_returns_null(tmp_path):
    r = _run(tmp_path)
    assert r["absent_button_returns_null"] is True


def test_update_refreshes_identity_without_a_rebind(tmp_path):
    r = _run(tmp_path)
    assert r["update_no_rebind"] is True
    assert r["update_username"] == "Signed in as bob"
    assert r["update_logout_present"] is True
