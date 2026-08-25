"""Browser-session namespace and recovery for pure doxBench working state."""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

STATE_JS = (
    REPO_ROOT
    / "scripts"
    / "ideation_dashboard"
    / "web"
    / "views"
    / "doxbench-state.js"
)
NODE = shutil.which("node")


_STORAGE_HARNESS = """
import {
  beginBufferEdit,
  clearDoxBenchSession,
  createDoxBenchState,
  persistDoxBenchState,
  restoreDoxBenchState,
  scopeStorageKey,
  settleBufferHash,
} from './doxbench-state.mjs';

class FakeStorage {
  constructor() {
    this.values = new Map();
    this.removed = [];
  }
  getItem(key) { return this.values.has(key) ? this.values.get(key) : null; }
  setItem(key, value) { this.values.set(key, String(value)); }
  removeItem(key) { this.removed.push(key); this.values.delete(key); }
}
const key = {
  repository: 'fixture-repo',
  ref: 'draft/topic-x',
  tile_kind: 'staged',
  tile_id: 'topic-x',
};
const otherKey = {
  repository: 'fixture-repo',
  ref: 'main',
  tile_kind: 'staged',
  tile_id: 'topic-x',
};
const collisionA = {
  repository: 'ab',
  ref: 'c',
  tile_kind: 'cluster',
  tile_id: 'd',
};
const collisionB = {
  repository: 'a',
  ref: 'bc',
  tile_kind: 'cluster',
  tile_id: 'd',
};
const initial = await createDoxBenchState({
  key,
  outline: {
    path: 'ideation/staging/topic-x/topic-x.md',
    owned: true,
    base_ref: key.ref,
    base_revision: '2'.repeat(40),
    content: '# Outline\\n',
  },
  document: {
    path: 'ideation/staging/topic-x/detail.md',
    owned: true,
    base_ref: key.ref,
    base_revision: '2'.repeat(40),
    content: '# Document\\n',
  },
});
const pending = beginBufferEdit(initial.buffers.document, '# Unsaved work\\n');
const editedDocument = settleBufferHash(
  pending.buffer,
  await pending.completion,
).buffer;
const edited = {
  ...initial,
  active_buffer: 'document',
  buffers: { ...initial.buffers, document: editedDocument },
};

const storage = new FakeStorage();
const saved = persistDoxBenchState(edited, storage);
const raw = storage.getItem(scopeStorageKey(key));
const restored = await restoreDoxBenchState(key, storage);
const wrongKeyRestore = await restoreDoxBenchState(otherKey, storage);

const otherState = await createDoxBenchState({
  key: otherKey,
  outline: {
    path: null,
    owned: true,
    base_ref: otherKey.ref,
    base_revision: '3'.repeat(40),
    content: '',
  },
  document: {
    path: 'ideation/brainstorm/other.md',
    owned: false,
    base_ref: otherKey.ref,
    base_revision: '3'.repeat(40),
    content: '# Other\\n',
  },
});
persistDoxBenchState(otherState, storage);
const cleared = clearDoxBenchSession(key, storage);
const endedRestore = await restoreDoxBenchState(key, storage);
const survivingRestore = await restoreDoxBenchState(otherKey, storage);

const corruptStorage = new FakeStorage();
corruptStorage.setItem(scopeStorageKey(key), '{not json');
const corruptRestore = await restoreDoxBenchState(key, corruptStorage);

const wrongVersionStorage = new FakeStorage();
wrongVersionStorage.setItem(
  scopeStorageKey(key),
  JSON.stringify({ schema_version: 99, kind: 'doxbench-working-state' }),
);
const wrongVersionRestore = await restoreDoxBenchState(key, wrongVersionStorage);

const otherTab = new FakeStorage();
const otherTabRestore = await restoreDoxBenchState(key, otherTab);

const throwingStorage = {
  getItem() { throw new Error('blocked'); },
  setItem() { throw new Error('blocked'); },
  removeItem() { throw new Error('blocked'); },
};
const blockedSave = persistDoxBenchState(edited, throwingStorage);
const blockedRestore = await restoreDoxBenchState(key, throwingStorage);
const blockedClear = clearDoxBenchSession(key, throwingStorage);

console.log(JSON.stringify({
  storageKeys: {
    active: scopeStorageKey(key),
    other: scopeStorageKey(otherKey),
    collisionA: scopeStorageKey(collisionA),
    collisionB: scopeStorageKey(collisionB),
  },
  saved,
  raw: JSON.parse(raw),
  restored,
  wrongKeyRestore,
  clear: {
    cleared,
    endedRestore,
    survivingRestore,
    removed: storage.removed,
  },
  corrupt: {
    restored: corruptRestore,
    removed: corruptStorage.removed,
  },
  wrongVersion: {
    restored: wrongVersionRestore,
    removed: wrongVersionStorage.removed,
  },
  otherTabRestore,
  blocked: {
    save: blockedSave,
    restore: blockedRestore,
    clear: blockedClear,
  },
}));
"""


@pytest.fixture(scope="module")
def storage_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench session-storage probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-storage")
    shutil.copy(STATE_JS, tmp_path / "doxbench-state.mjs")
    harness = tmp_path / "storage-harness.mjs"
    harness.write_text(_STORAGE_HARNESS, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_scope_storage_key_is_collision_safe_and_uses_all_four_fields(storage_results):
    keys = storage_results["storageKeys"]
    assert keys["active"] != keys["other"]
    assert keys["collisionA"] != keys["collisionB"]
    assert keys["active"].startswith("doxbench:v1:")


def test_dirty_buffers_restore_only_for_the_identical_scope_key(storage_results):
    assert storage_results["saved"] is True
    restored = storage_results["restored"]
    assert restored["active_buffer"] == "document"
    assert restored["buffers"]["document"]["content"] == "# Unsaved work\n"
    assert restored["buffers"]["document"]["dirty"] is True
    assert restored["buffers"]["document"]["current_hash"]["algorithm"] == "sha256"
    assert storage_results["wrongKeyRestore"] is None


def test_persisted_state_contains_derived_inputs_not_trusted_hashes(storage_results):
    raw = storage_results["raw"]
    assert raw["schema_version"] == 1
    assert raw["kind"] == "doxbench-working-state"
    assert set(raw["buffers"]) == {"outline", "document"}
    for buffer in raw["buffers"].values():
        assert "base_hash" not in buffer
        assert "current_hash" not in buffer
        assert "dirty" not in buffer
        assert "hash_generation" not in buffer


def test_session_end_clears_only_the_exact_ref_and_tile_key(storage_results):
    result = storage_results["clear"]
    assert result["cleared"] is True
    assert result["endedRestore"] is None
    assert result["survivingRestore"]["key"]["ref"] == "main"
    assert result["removed"] == [storage_results["storageKeys"]["active"]]


def test_corrupt_or_wrong_version_state_degrades_to_absent_and_is_removed(
    storage_results,
):
    for key in ("corrupt", "wrongVersion"):
        result = storage_results[key]
        assert result["restored"] is None
        assert result["removed"] == [storage_results["storageKeys"]["active"]]


def test_separate_browser_session_store_does_not_share_working_state(storage_results):
    assert storage_results["otherTabRestore"] is None


def test_blocked_session_storage_never_breaks_live_state(storage_results):
    assert storage_results["blocked"] == {
        "save": False,
        "restore": None,
        "clear": False,
    }


def test_state_module_never_uses_persistent_local_storage():
    source = STATE_JS.read_text(encoding="utf-8")
    assert "localStorage" not in source
    assert "sessionStorage" in source


# ---------------------------------------------------------------------------
# T027 / T030 (010-doxbench-editor-chat, US1): the doxBench two-buffer
# editing canvas -- FR-003..FR-010, acceptance scenarios 1-5.
#
# `doxbench-editor.js` does not exist yet; Phase B builds it against exactly
# the API driven below (`mountDoxBenchCanvas`, `DOXBENCH_VIEW_TABS`,
# `SAVE_UNAVAILABLE_REASON` -- see specs/010-doxbench-editor-chat/plan
# artifacts). Every test below is expected to fail RED until then: either
# Node's own "Cannot find module" (the harness imports the module under its
# real name so Phase B needs no test changes) or a bare FileNotFoundError
# from the plain source read in
# `test_doxbench_editor_source_has_no_private_html_sink_or_second_sanitizer`.
#
# Harness pattern, modelled on test_staging_workbench.py's `_DOM_SHIM`
# (widened to the editor's textarea/preview surface) and on
# test_renderer.py's vendored-markdown-it-via-createRequire probe:
# copies of doxbench-editor.js, doxbench-state.js and viewer.js land under
# their REAL names in tmp_path/views (so the module's own
# `import "./viewer.js"` resolves unchanged), the vendored UMD bundle sits in
# tmp_path/vendor with its own commonjs package.json override, and ONE node
# run drives every T027/T030 scenario and prints a single JSON object -- the
# same one-process-per-result-set shape as `storage_results` above.
# ---------------------------------------------------------------------------

EDITOR_JS = (
    REPO_ROOT
    / "scripts"
    / "ideation_dashboard"
    / "web"
    / "views"
    / "doxbench-editor.js"
)
VIEWER_JS = (
    REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views" / "viewer.js"
)
VENDOR_MARKDOWN_JS = (
    REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "vendor" / "markdown-it.min.js"
)
PREVIEW_CASES_PATH = (
    REPO_ROOT
    / "tests"
    / "ideation-dashboard"
    / "fixtures"
    / "doxbench_preview_cases.json"
)


# A minimal HTML-ish DOM: `class Node` with textarea properties
# (value/selectionStart/selectionEnd/scrollTop), a `hidden` setter that blurs
# a focused node the instant it is hidden (real browsers cannot keep focus on
# a non-rendered element -- a module that only relies on that ambient
# blur/never re-focuses explicitly would fail the tab-restoration tests
# below), classList, and an `innerHTML` setter that records every NON-EMPTY
# assignment into a global `htmlSinks` list (empty-string clears go to a
# separate `htmlClears` list) so tests can prove there is exactly one live
# HTML sink and pin its exact bytes. Modelled on test_staging_workbench.py's
# `_DOM_SHIM`, widened for the editor's surface.
_EDITOR_DOM_SHIM = r"""
const htmlSinks = [];
const htmlClears = [];
const focusLog = [];

class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = [];
    this.attributes = {};
    this.listeners = {};
    this.className = '';
    this._text = '';
    this._hidden = false;
    this.disabled = false;
    this.title = '';
    this.type = '';
    this.id = '';
    this.tabIndex = -1;
    this._value = '';
    this._selectionStart = 0;
    this._selectionEnd = 0;
    this._scrollTop = 0;
    this._innerHTML = '';
    this.parentNode = null;
    // Every element has one, and the wheel writes `transform`/`opacity`/
    // `zIndex` through it on every layout pass. Absent, the wheel's layout threw
    // and no test could reach the tiles it places -- the same gap that hid the
    // composition defects the PR #207 review found.
    this.style = {};
    // Measured height. Zero is the honest default for an unlaid-out stub, and
    // `doc-wheel.js` deliberately waits for a real box rather than dividing by
    // it; a harness that wants tiles placed sets it.
    this.clientHeight = 0;
    const self = this;
    this.classList = {
      add(...names) {
        const list = self.className.split(' ').filter(Boolean);
        for (const n of names) if (!list.includes(n)) list.push(n);
        self.className = list.join(' ');
      },
      remove(...names) {
        self.className = self.className.split(' ').filter(Boolean)
          .filter((c) => !names.includes(c)).join(' ');
      },
      toggle(name, force) {
        const has = self.className.split(' ').filter(Boolean).includes(name);
        const want = force === undefined ? !has : !!force;
        if (want && !has) self.classList.add(name);
        if (!want && has) self.classList.remove(name);
        return want;
      },
      contains(name) {
        return self.className.split(' ').filter(Boolean).includes(name);
      },
    };
  }
  // Every node in a real document has one; doxbench-chat.js reads it to
  // build its DOM (`host.ownerDocument`), which the shell composition harness
  // at the bottom of this file exercises.
  get ownerDocument() { return globalThis.document; }
  get hidden() { return this._hidden; }
  set hidden(v) {
    this._hidden = !!v;
    // A hidden/unrendered element cannot hold focus in a real browser -- and
    // neither can a DESCENDANT of one (an element is only focusable if it
    // and every ancestor is rendered), so hiding a pane must drop focus from
    // whatever inside it currently holds it. The module must track "was
    // focused" itself rather than lean on the DOM to remember it for free.
    if (this._hidden && globalThis.document && globalThis.document.activeElement
        && this.contains(globalThis.document.activeElement)) {
      globalThis.document.activeElement.blur();
    }
    // And a hidden element loses its LAYOUT BOX, which is where a browser
    // keeps a textarea's scroll offset -- so hiding drops every descendant's
    // scrollTop (T104 / FR-010: this shim used to keep it for free, which is
    // exactly why the missing write-back passed the tab round-trip tests
    // while a real browser landed the human at the top of the buffer).
    // Selection is DOM state, not layout, and survives.
    if (this._hidden) {
      const dropScroll = (node) => {
        if (node._scrollTop !== undefined) node._scrollTop = 0;
        for (const child of (node.children || [])) dropScroll(child);
      };
      dropScroll(this);
    }
  }
  contains(node) {
    let n = node;
    while (n) {
      if (n === this) return true;
      n = n.parentNode;
    }
    return false;
  }
  get textContent() {
    return this._text + this.children.map((c) => c.textContent).join('');
  }
  set textContent(value) { this.children = []; this._text = String(value); }
  get innerHTML() { return this._innerHTML; }
  set innerHTML(value) {
    const str = String(value);
    if (str === '') {
      htmlClears.push({ cls: this.className });
    } else {
      htmlSinks.push({ cls: this.className, length: str.length, value: str });
    }
    this._innerHTML = str;
    this.children = [];
    this._text = '';
  }
  get value() { return this._value; }
  set value(v) { this._value = String(v); }
  get selectionStart() { return this._selectionStart; }
  set selectionStart(v) { this._selectionStart = v; this._notify('select'); }
  get selectionEnd() { return this._selectionEnd; }
  set selectionEnd(v) { this._selectionEnd = v; this._notify('select'); }
  get scrollTop() { return this._scrollTop; }
  set scrollTop(v) { this._scrollTop = v; this._notify('scroll'); }
  _notify(type) { for (const fn of (this.listeners[type] || [])) fn({ target: this }); }
  appendChild(child) { child.parentNode = this; this.children.push(child); return child; }
  append(...kids) { for (const k of kids) this.appendChild(k); }
  insertBefore(child, ref) {
    child.parentNode = this;
    const at = this.children.indexOf(ref);
    this.children.splice(at < 0 ? this.children.length : at, 0, child);
    return child;
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  // A real DOM method the shipped code has always used (`doc-wheel.js` clears
  // `aria-hidden` on every tile it lays out). The shim lacked it, which is why
  // no test in this suite had ever driven the docs wheel's LAYOUT -- and the
  // adversarial review of PR #207 found three composition defects hiding behind
  // exactly that gap. Added as the real method, never as a no-op.
  removeAttribute(name) { delete this.attributes[name]; }
  // A tile carries its own removal too (`mountActions` rebuilds the action row).
  remove() {
    if (!this.parentNode) return;
    const at = this.parentNode.children.indexOf(this);
    if (at >= 0) this.parentNode.children.splice(at, 1);
    this.parentNode = null;
  }
  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name] : null;
  }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  removeEventListener(type, fn) {
    if (this.listeners[type]) this.listeners[type] = this.listeners[type].filter((f) => f !== fn);
  }
  focus() {
    globalThis.document.activeElement = this;
    focusLog.push({ tag: this.tagName, cls: this.className });
    this._notify('focus');
  }
  blur() {
    if (globalThis.document.activeElement === this) globalThis.document.activeElement = null;
    this._notify('blur');
  }
  walk() { return this.children.reduce((all, c) => all.concat(c.walk()), [this]); }
  closest(selector) {
    const cls = selector.replace(/^\./, '');
    let node = this;
    while (node) {
      if (String(node.className).split(' ').includes(cls)) return node;
      node = node.parentNode;
    }
    return null;
  }
  querySelector(selector) {
    const cls = selector.replace(/^\./, '');
    return this.walk().find((n) => n !== this && String(n.className).split(' ').includes(cls)) || null;
  }
  querySelectorAll(selector) {
    const cls = selector.replace(/^\./, '');
    return this.walk().filter((n) => n !== this && String(n.className).split(' ').includes(cls));
  }
}

globalThis.document = {
  createElement: (tag) => new Node(tag),
  createTextNode: (text) => { const n = new Node('#text'); n._text = String(text); return n; },
  activeElement: null,
  addEventListener() {},
  removeEventListener() {},
  body: new Node('body'),
};
"""

# The full T027 + T030 scenario driver. Vendors markdown-it via createRequire
# BEFORE importing doxbench-editor.js (mirrors test_renderer.py's shared
# Markdown probe), builds one fixed projection/content-map pair, and runs
# every guard / focus / restoration / preview / Unicode scenario, printing
# ONE JSON object so the whole T027+T030 set costs a single node process.
_EDITOR_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';

globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');

const {
  mountDoxBenchCanvas,
  DOXBENCH_VIEW_TABS,
  DOXBENCH_BUFFER_LABELS,
  SAVE_UNAVAILABLE_REASON,
} = await import('./doxbench-editor.js');
const { renderSafeMarkdownHtml } = await import('./viewer.js');
const { contentIdentity } = await import('./doxbench-state.js');

const OUTLINE_PATH = 'ideation/staging/topic-x/topic-x.md';
const DOC_A = 'ideation/staging/topic-x/detail.md';
const DOC_B = 'ideation/staging/topic-x/second.md';

const CONTENT = {
  [OUTLINE_PATH]: '# Outline\n',
  [DOC_A]: '# Document A\n',
  [DOC_B]: '# Document B\n',
};

function makeProjection(overrides = {}) {
  const base = {
    key: { repository: 'fixture-repo', ref: 'draft/topic-x', tile_kind: 'staged', tile_id: 'topic-x' },
    title: 'Topic X',
    source_revision: 'a'.repeat(40),
    outline_path: OUTLINE_PATH,
    editable_paths: [OUTLINE_PATH, DOC_A, DOC_B],
    context_paths: [OUTLINE_PATH, DOC_A, DOC_B],
    active_document_candidates: [DOC_A, DOC_B],
    sections: [
      {
        key: 'folder', label: 'Folder', note: null, inherited: false, owned: true,
        documents: [OUTLINE_PATH, DOC_A, DOC_B].map((p) => ({ id: p, path: p, resolved: true })),
      },
    ],
  };
  const merged = { ...base, ...overrides };
  merged.key = { ...base.key, ...(overrides.key || {}) };
  return merged;
}

function makeLoadSource(map, calls) {
  return async (path) => {
    calls.push(path);
    if (!(path in map)) return null;
    return { content: map[path], revision: 'rev-' + path, ref: 'main' };
  };
}

class FakeStorage {
  constructor() { this.values = new Map(); }
  getItem(key) { return this.values.has(key) ? this.values.get(key) : null; }
  setItem(key, value) { this.values.set(key, String(value)); }
  removeItem(key) { this.values.delete(key); }
}

function describeEl(node) { return node ? { tag: node.tagName, cls: node.className } : null; }

// Fires a real DOM event through the listeners the module itself registered
// (never calling controller.edit(...) directly), and awaits every listener
// -- the module's own `input` listener is async in the fix round, so a test
// driving the REAL event must await it the same way a real dispatch would
// let the module's own promise chain settle before the next assertion.
async function fireEvent(node, type) {
  for (const fn of (node.listeners[type] || [])) await fn({ target: node });
}

// Items 1-4: a dirty Document buffer blocks a switch; save/cancel/discard
// each get their OWN fresh mount so the three resolutions never interact.
async function guardScenario(choice) {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  await controller.edit('document', '# Document A edited\n');
  const dirtyBuffer = controller.state().buffers.document;
  const blocked = await controller.selectDocument(DOC_B);
  const guardEl = controller.elements().guard();
  const guardText = guardEl ? (String(guardEl.textContent) + String(guardEl.innerHTML)) : null;
  const resolved = await controller.resolveGuard(choice);
  const afterBuffer = controller.state().buffers.document;
  return { dirtyBuffer, blocked, guardText, resolved, afterBuffer, calls: calls.slice() };
}

// Amendment 1 (F3): WHERE THE GATE CAPABILITY IS ABSENT THE SLOT DOES NOT SWAP.
// Mounted with NO save seam and nothing dirty — the state that would otherwise
// show Unload. The pair must stay, with Save's absence stated as visible text,
// because swapping would replace the one statement that this surface cannot save
// with a control that never says so.
//
// Written at the CANVAS MODULE, which is where the clause actually reaches:
// through the shipped shell a gate-off console renders no canvas controls at
// all, so this is a module-level invariant rather than an end-user posture.
async function gateAbsentSlotScenario() {
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const els = controller.elements();
  return {
    anythingDirty: Object.values(controller.state().buffers).some((b) => b.dirty),
    saveHidden: els.save().hidden === true,
    cancelHidden: els.cancel().hidden === true,
    unloadHidden: els.unload().hidden === true,
    saveDisabled: els.save().disabled === true,
  };
}

// Amendment 1 (F5): A SAVE IN FLIGHT KEEPS THE PAIR ON SCREEN. The bytes are
// mid-flight and the buffers are about to stop being dirty but have not yet, so
// swapping the slot under a running Save would answer a question nobody asked.
// The seam is held open on a promise this scenario resolves by hand.
// The same bounded-poll idiom the later harnesses in this file already carry
// (`settle`/`until`), spelled here because this harness had no waiter of its own
// and a fixed `setTimeout` is a guess about scheduler load rather than a wait
// for the thing under test. Bounded, so a transition that never arrives fails
// with its own name instead of hanging the probe.
const inFlightSettle = () => new Promise((r) => setTimeout(r, 0));
async function inFlightUntil(predicate, label) {
  for (let i = 0; i < 400; i += 1) {
    if (predicate()) return;
    await inFlightSettle();
  }
  throw new Error('timed out waiting for ' + label);
}

async function saveInFlightSlotScenario() {
  let release = null;
  const held = new Promise((resolve) => { release = resolve; });
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
    save: async (request) => {
      await held;
      return {
        status: 'committed',
        buffers: (request.buffers || []).map((row) => ({
          key: row.key ?? row.kind, status: 'committed', action: 'edit-document',
          ref: 'draft/x', revision: 'r2',
          content_hash: { algorithm: 'sha256', hex: 'e'.repeat(64) }, message: null })),
      };
    },
  });
  await controller.ready;
  await controller.edit('outline', '# dirty outline\n');
  const els = controller.elements();
  const dirty = {
    saveHidden: els.save().hidden === true,
    unloadHidden: els.unload().hidden === true,
  };
  const running = controller.save();
  // POLL the specific transition, never a fixed delay (Copilot, PR #229): a
  // wall-clock sleep is a guess about scheduler load, and the thing this
  // scenario is about — WHICH controls are on screen mid-flight — is exactly the
  // thing a slow machine would race. `saving` reaches the panel by disabling
  // Save, so that is the transition to wait on.
  await inFlightUntil(() => els.save().disabled === true,
                      'the Save to report itself in flight');
  const inFlight = {
    saveHidden: els.save().hidden === true,
    cancelHidden: els.cancel().hidden === true,
    unloadHidden: els.unload().hidden === true,
    saveDisabled: els.save().disabled === true,
    cancelDisabled: els.cancel().disabled === true,
  };
  release();
  await running;
  // …and the settled read waits on the state the assertion is about — every
  // buffer clean — rather than on a delay that hopes the rebase already ran.
  const clean = () => !Object.values(controller.state().buffers).some((b) => b.dirty);
  await inFlightUntil(clean, 'the saved buffers to rebase clean');
  const settled = {
    saveHidden: els.save().hidden === true,
    unloadHidden: els.unload().hidden === true,
    anythingDirty: !clean(),
  };
  return { dirty, inFlight, settled };
}

// Item 5: a CLEAN Document buffer switches immediately, no guard offered.
async function cleanSwitchScenario() {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const result = await controller.selectDocument(DOC_B);
  const guardEl = controller.elements().guard();
  return { result, guardPresent: !!(guardEl && !guardEl.hidden), buffer: controller.state().buffers.document };
}

// Items 6-8: per-buffer focus/selection/scroll independence across tab
// switches, and survival across refreshContext + a preview flush.
async function focusPersistenceScenario() {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;

  // PIN EVOLUTION (add-doxbench-editing-phase-a): the canvas opens on the
  // `Preview` view tab, so a scenario about a TEXTAREA's focus, selection and
  // scroll has to stand where the textareas are. The buffer switch it exercises
  // is `setActiveBuffer` — the buffer tablist that used to drive it is retired
  // and the context region owns that choice now.
  controller.setActiveView('editor');
  controller.setActiveBuffer('outline');
  const outlineArea = controller.elements().textarea('outline');
  outlineArea.selectionStart = 2; outlineArea.selectionEnd = 5; outlineArea.scrollTop = 10;
  outlineArea.focus();
  const outlineViewAfterFocus = controller.viewState('outline');

  controller.setActiveBuffer('document');
  const documentArea = controller.elements().textarea('document');
  documentArea.selectionStart = 1; documentArea.selectionEnd = 3; documentArea.scrollTop = 20;
  const documentViewNoFocus = controller.viewState('document');
  const activeElementAfterSwitchNoFocus = describeEl(globalThis.document.activeElement);

  controller.setActiveBuffer('outline');
  const outlineViewAfterReturn = controller.viewState('outline');
  const activeElementAfterReturn = describeEl(globalThis.document.activeElement);

  await controller.refreshContext(makeProjection());
  await controller.flushPreview();
  const outlineViewAfterRefresh = controller.viewState('outline');
  const activeElementAfterRefresh = describeEl(globalThis.document.activeElement);

  return {
    outlineViewAfterFocus, documentViewNoFocus,
    activeElementAfterSwitchNoFocus,
    outlineViewAfterReturn, activeElementAfterReturn,
    outlineViewAfterRefresh, activeElementAfterRefresh,
    outlineElSame: controller.elements().textarea('outline') === outlineArea,
  };
}

// Item 8 (the negative half): with NEITHER buffer ever focused, tab
// switches must not steal focus onto either one.
async function noAutoFocusScenario() {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  // the Editor view is selected so the textareas are genuinely on screen --
  // "never steals focus" has to be measured where focus was possible
  controller.setActiveView('editor');
  globalThis.document.activeElement = null;
  controller.setActiveBuffer('document');
  const afterDoc = describeEl(globalThis.document.activeElement);
  controller.setActiveBuffer('outline');
  const afterOutline = describeEl(globalThis.document.activeElement);
  return { afterDoc, afterOutline };
}

// Item 9: active tab + dirty buffers restore from the injected storage on a
// fresh mount with the identical scope key; a different key restores
// nothing. `destroy()` is the documented teardown seam, so it is the point
// at which working state is expected to be handed to storage.
async function sessionRestoreScenario() {
  const storage = new FakeStorage();
  const projection = makeProjection();
  const calls1 = [];
  const controller1 = mountDoxBenchCanvas(new Node('div'), projection, {
    loadSource: makeLoadSource(CONTENT, calls1), storage, previewDelayMs: 5,
  });
  await controller1.ready;
  await controller1.edit('document', '# Restore me\n');
  controller1.setActiveBuffer('document');
  controller1.destroy();

  const calls2 = [];
  const controller2 = mountDoxBenchCanvas(new Node('div'), projection, {
    loadSource: makeLoadSource(CONTENT, calls2), storage, previewDelayMs: 5,
  });
  await controller2.ready;
  const restoredState = controller2.state();
  const restoredTab = controller2.activeBuffer();
  controller2.destroy();

  const differentKeyProjection = makeProjection({ key: { tile_id: 'topic-y' } });
  const calls3 = [];
  const controller3 = mountDoxBenchCanvas(new Node('div'), differentKeyProjection, {
    loadSource: makeLoadSource(CONTENT, calls3), storage, previewDelayMs: 5,
  });
  await controller3.ready;
  const freshState = controller3.state();
  const freshTab = controller3.activeBuffer();

  return { restoredState, restoredTab, freshState, freshTab };
}

// Item 10: outline_path === null is an explicit empty/create state, and
// NEVER infers an outline from the Document buffer's own headings (the
// document fixture below carries a distinctive marker heading that must
// never leak into the outline pane).
async function emptyOutlineScenario() {
  const MARKER_PATH = 'ideation/staging/topic-x/marker.md';
  const calls = [];
  const projection = makeProjection({
    outline_path: null,
    active_document_candidates: [MARKER_PATH],
    editable_paths: [MARKER_PATH],
    context_paths: [MARKER_PATH],
  });
  const map = { ...CONTENT, [MARKER_PATH]: '# INFERRED-OUTLINE-MARKER\nbody\n' };
  const controller = mountDoxBenchCanvas(new Node('div'), projection, {
    loadSource: makeLoadSource(map, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  await controller.flushPreview();
  const outline = controller.state().buffers.outline;
  const outlinePreview = controller.elements().preview('outline');
  const outlineTextarea = controller.elements().textarea('outline');
  return {
    outline,
    outlinePreviewHtml: outlinePreview ? outlinePreview.innerHTML : null,
    outlinePreviewText: outlinePreview ? outlinePreview.textContent : null,
    outlineTextareaValue: outlineTextarea ? outlineTextarea.value : null,
  };
}

// Item 11: with no `loadSource` injected at all, every backed path reports
// `unavailable` with empty content -- nothing fabricated, no network.
async function noLoadSourceScenario() {
  const projection = makeProjection();
  const controller = mountDoxBenchCanvas(new Node('div'), projection, {
    storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  await controller.flushPreview();
  const outline = controller.state().buffers.outline;
  const doc = controller.state().buffers.document;
  const outlinePreview = controller.elements().preview('outline');
  const docPreview = controller.elements().preview('document');
  return {
    outline, doc,
    outlineReason: outlinePreview
      ? (String(outlinePreview.innerHTML) + String(outlinePreview.textContent)) : null,
    docReason: docPreview
      ? (String(docPreview.innerHTML) + String(docPreview.textContent)) : null,
  };
}

// T030.2: hostile Markdown through the ONE shared sanitizer seam.
async function hostilePreviewScenario() {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const source = [
    '# doxBench preview',
    '',
    '<script>alert(1)</script>',
    '',
    '[bad](javascript:alert(2))',
    '',
    '![tracker](https://example.invalid/pixel.png)',
    '',
    '![legacy](ftp://example.invalid/pixel.png)',
    '',
    '![local](images/local.png)',
  ].join('\n');
  const before = htmlSinks.length;
  await controller.edit('document', source);
  await controller.flushPreview();
  const produced = htmlSinks.slice(before);
  const previewNode = controller.elements().preview('document');
  const expectedHtml = renderSafeMarkdownHtml(source);
  return {
    producedCount: produced.length,
    producedClasses: produced.map((s) => s.cls),
    previewCls: previewNode.className,
    sinkValue: produced.length ? produced[produced.length - 1].value : null,
    expectedHtml,
  };
}

// T030.3: byte-exact content identity over unusual Unicode/Markdown, driven
// from the fixture file so no giant string literals live in this harness.
async function unicodeScenario(cases) {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const out = {};
  for (const c of cases) {
    await controller.edit('document', c.content);
    await controller.flushPreview();
    const buf = controller.state().buffers.document;
    out[c.id] = { content: buf.content, dirty: buf.dirty, hash: buf.current_hash, loadState: buf.load_state };
  }
  const base = controller.state().buffers.document.base_content;
  await controller.edit('document', base);
  await controller.flushPreview();
  out.__backToBase = { dirty: controller.state().buffers.document.dirty };
  return out;
}

// T030.4: an unpaired UTF-16 surrogate is refused honestly, never a silent
// crash and never a corrupted buffer.
async function surrogateScenario() {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const before = controller.state().buffers.document;
  const orphan = '\uD800lone-high-surrogate';
  let threw = false;
  let result = null;
  try {
    result = await controller.edit('document', orphan);
  } catch (err) {
    threw = true;
    result = { message: err && err.message, name: err && err.constructor && err.constructor.name };
  }
  const after = controller.state().buffers.document;
  return { before, after, threw, result };
}

// ---------------------------------------------------------------------------
// Phase C fix round. B1: the generation-staleness guard must actually guard
// -- settleBufferHash has to be paired against the LIVE buffer at settle
// time, never the snapshot the edit began from (that snapshot's own
// generation trivially matches its own completion, which makes the
// staleness check a no-op and lets a slow hash silently overwrite a newer
// Discard, edit, or document switch). Each race below gates exactly ONE
// named piece of content so the interleaving is deterministic, never
// timing-dependent: the injected `hash` only awaits a manually-released gate
// for that one marker string, and resolves immediately for everything else
// (including the mount's own initial-load hashing, which would otherwise
// deadlock before `ready` ever resolves).
// ---------------------------------------------------------------------------

async function generationRaceScenario() {
  const calls = [];
  let releaseFirst;
  const firstGate = new Promise((resolve) => { releaseFirst = resolve; });
  const FIRST_TEXT = '# generation race: first\n';
  const SECOND_TEXT = '# generation race: second\n';
  const gatedHash = async (content) => {
    if (content === FIRST_TEXT) await firstGate;
    return contentIdentity(content);
  };
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
    hash: gatedHash,
  });
  await controller.ready;

  const firstEditPromise = controller.edit('document', FIRST_TEXT);
  const secondResult = await controller.edit('document', SECOND_TEXT);
  const afterSecond = controller.state().buffers.document;
  releaseFirst();
  const firstResult = await firstEditPromise;
  const afterFirst = controller.state().buffers.document;

  function snap(buf) {
    return {
      content: buf.content, dirty: buf.dirty, generation: buf.hash_generation,
      hashHex: buf.current_hash && buf.current_hash.hex,
    };
  }
  return {
    secondResult, firstResult,
    afterSecond: snap(afterSecond), afterFirst: snap(afterFirst),
  };
}

async function editThenDiscardBeforeSettleScenario() {
  const calls = [];
  const EDIT_TEXT = '# edit-then-discard race\n';
  let releaseEdit;
  const gate = new Promise((resolve) => { releaseEdit = resolve; });
  const gatedHash = async (content) => {
    if (content === EDIT_TEXT) await gate;
    return contentIdentity(content);
  };
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
    hash: gatedHash,
  });
  await controller.ready;
  const baseContent = controller.state().buffers.document.base_content;

  const editPromise = controller.edit('document', EDIT_TEXT);
  await controller.discard('document');
  const afterDiscard = controller.state().buffers.document;
  releaseEdit();
  await editPromise;
  const afterEditSettles = controller.state().buffers.document;

  return {
    baseContent,
    afterDiscard: { content: afterDiscard.content, dirty: afterDiscard.dirty },
    afterEditSettles: { content: afterEditSettles.content, dirty: afterEditSettles.dirty },
  };
}

async function editThenSwitchBeforeSettleScenario() {
  const calls = [];
  const RACE_TEXT = '# edit-then-switch race\n';
  let releaseEdit;
  const gate = new Promise((resolve) => { releaseEdit = resolve; });
  const gatedHash = async (content) => {
    if (content === RACE_TEXT) await gate;
    return contentIdentity(content);
  };
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
    hash: gatedHash,
  });
  await controller.ready;
  await controller.edit('document', '# stable first edit\n'); // settled, real hash, dirty

  const racePromise = controller.edit('document', RACE_TEXT); // dirty synchronously, hash gated
  const blocked = await controller.selectDocument(DOC_B);      // blocked: buffer is dirty
  const discardResolution = await controller.resolveGuard('discard'); // discards + switches to DOC_B
  const afterSwitch = controller.state().buffers.document;
  releaseEdit();
  await racePromise; // the stale RACE_TEXT completion must be dropped, not reapplied
  const afterRaceSettles = controller.state().buffers.document;

  return {
    blocked, discardResolution,
    afterSwitch: { path: afterSwitch.path, content: afterSwitch.content },
    afterRaceSettles: { path: afterRaceSettles.path, content: afterRaceSettles.content },
  };
}

// B2: a refused edit must never revert the textarea silently. Drives the
// REAL `input` event (never controller.edit(...) directly) so the fix in
// the listener itself -- not just in edit() -- is what gets proven.
async function inputRefusalScenario() {
  async function runCase(content) {
    const calls = [];
    const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
      loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
    });
    await controller.ready;
    const textarea = controller.elements().textarea('document');
    const status = controller.elements().status('document');
    const before = controller.state().buffers.document;
    textarea.value = content;
    await fireEvent(textarea, 'input');
    const after = controller.state().buffers.document;
    return {
      before: { content: before.content, dirty: before.dirty },
      after: { content: after.content, dirty: after.dirty },
      status: String(status.textContent),
    };
  }
  const surrogate = await runCase('\uD800lone-surrogate-via-input');
  const oversized = await runCase('a'.repeat(400001));
  return { surrogate, oversized };
}

// W-8/W-9 companion (wave re-review): a document SELECTION during the loading
// window. selectDocument refuses it (the F6-2 loading posture), and the
// refusal must be STATED -- it used to be silent, leaving whichever control
// asked showing a choice that never landed, forever.
//
// PIN EVOLUTION (Brett's 2026-08-15 annotation round): this drove the canvas's
// own picker, which is retired -- the context region's docs wheel is the sole
// human route now. What it actually pins is `selectDocument`'s refusal, which
// is where the sentence has lived since the PR #196 review (F6) and is shared
// by every route into it, so the scenario drives the method directly.
async function selectDuringLoadScenario() {
  let releaseLoad;
  const gate = new Promise((resolve) => { releaseLoad = resolve; });
  const inner = makeLoadSource(CONTENT, []);
  const gated = async (path) => { await gate; return inner(path); };
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: gated, storage: new FakeStorage(), previewDelayMs: 5,
  });
  const refused = await controller.selectDocument(DOC_B);  // the load is open
  const duringLoad = {
    refused,
    status: String(controller.elements().status('document').textContent),
  };
  releaseLoad();
  await controller.ready;
  return {
    duringLoad,
    afterLoad: {
      bufferPath: controller.state().buffers.document.path,
    },
  };
}

// W-10 (wave re-review): the editor's apply refusals carry fixed CODES the
// rail maps to its own vocabulary -- staleness and an unavailable target are
// different recoveries and must stop sharing one sentence.
async function applyRefusalCodesScenario() {
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const stale = await controller.applyProposal('document', {
    base_hash: 'f'.repeat(64), content: '# other\n' });
  const unavailable = await controller.applyProposal('document', null);
  return { stale, unavailable };
}

// B3: once a buffer has ANY typed content, that content must render and the
// dirty fact must be reported -- load_state alone (which the state module
// preserves across every edit on purpose) must never keep showing the
// canned empty/unavailable statement forever.
async function typedOutlineOverridesEmptyScenario() {
  const calls = [];
  const projection = makeProjection({ outline_path: null });
  const controller = mountDoxBenchCanvas(new Node('div'), projection, {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  await controller.edit('outline', '# My new outline\n');
  await controller.flushPreview();
  const preview = controller.elements().preview('outline');
  const status = controller.elements().status('outline');
  return {
    previewHtml: preview.innerHTML,
    statusText: String(status.textContent),
    loadState: controller.state().buffers.outline.load_state,
    dirty: controller.state().buffers.outline.dirty,
  };
}

async function typedDocumentOverridesUnavailableScenario() {
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    // no loadSource -> the Document buffer loads `unavailable`
    storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  await controller.edit('document', '# Recovered content\n');
  await controller.flushPreview();
  const preview = controller.elements().preview('document');
  const status = controller.elements().status('document');
  return {
    previewHtml: preview.innerHTML,
    statusText: String(status.textContent),
    loadState: controller.state().buffers.document.load_state,
  };
}

// B4: selectDocument must refuse a path this scope never declared.
async function outOfScopeSelectDocumentScenario() {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const before = controller.state().buffers.document;
  const result = await controller.selectDocument('ideation/staging/topic-x/not-in-scope.md');
  const after = controller.state().buffers.document;
  const inScopeResult = await controller.selectDocument(DOC_B);
  const afterInScope = controller.state().buffers.document;
  return {
    result, inScopeResult,
    before: { path: before.path, content: before.content },
    after: { path: after.path, content: after.content },
    afterInScope: { path: afterInScope.path },
  };
}

// S1a/S1b: structural accessibility -- each editor is described by its own
// preview, the mounted region carries the exact product name, and the
// visible heading reads it too.
async function accessibilityScenario() {
  const calls = [];
  const host = new Node('div');
  const controller = mountDoxBenchCanvas(host, makeProjection({ title: 'Topic X' }), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const outlineTextarea = controller.elements().textarea('outline');
  const outlinePreview = controller.elements().preview('outline');
  const documentTextarea = controller.elements().textarea('document');
  const documentPreview = controller.elements().preview('document');
  return {
    hostRole: host.getAttribute('role'),
    hostAriaLabel: host.getAttribute('aria-label'),
    hostTextContent: host.textContent,
    // the retired visible heading, counted rather than assumed gone
    headings: host.walk().filter((n) => n.tagName === 'H2').length,
    outlineDescribedBy: outlineTextarea.getAttribute('aria-describedby'),
    outlinePreviewId: outlinePreview.id,
    documentDescribedBy: documentTextarea.getAttribute('aria-describedby'),
    documentPreviewId: documentPreview.id,
  };
}

// S2: opening the guard moves focus to Discard; resolving it (cancel or
// discard) returns focus to the Document textarea. Never a focus trap.
async function guardFocusScenario() {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  // PIN EVOLUTION (PR #196 review F1): the human SELECTS the document before
  // typing in it, which is what makes it the active buffer -- and it is the
  // active buffer's editor that focus can legitimately return to, because a
  // hidden pane holds no real focus. Resolving the guard no longer re-binds,
  // so the scenario has to establish the binding the way a human does.
  await controller.selectDocument(DOC_A);
  await controller.edit('document', '# dirty for guard focus\n');
  await controller.selectDocument(DOC_B);
  const focusedOnShow = describeEl(globalThis.document.activeElement);
  const activeBufferOnShow = controller.activeBuffer();
  await controller.resolveGuard('cancel');
  const focusedAfterCancel = globalThis.document.activeElement === controller.elements().textarea('document');
  const activeBufferAfterCancel = controller.activeBuffer();

  const calls2 = [];
  const controller2 = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls2), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller2.ready;
  await controller2.selectDocument(DOC_A);
  await controller2.edit('document', '# dirty for guard focus 2\n');
  await controller2.selectDocument(DOC_B);
  await controller2.resolveGuard('discard');
  const focusedAfterDiscard = globalThis.document.activeElement === controller2.elements().textarea('document');

  return { focusedOnShow, activeBufferOnShow, focusedAfterCancel,
           activeBufferAfterCancel, focusedAfterDiscard };
}

// S3, re-pinned (Brett's 2026-08-15 annotation round): the canvas no longer
// renders a document picker of its own — "we do not need this section now that
// the left panel will let us select the active document" — so the SELECTION
// route it used to drive belongs entirely to the context region's docs wheel,
// where it is exercised against the real shell in `selection_results`.
//
// What survives here is the rule the picker existed to carry, and it is now
// carried by `selectDocument` itself (PR #196 review F4/F6 moved the guard,
// the refusal sentence and the reconcile into it — which is what made the
// control removable without losing anything): a clean switch lands, a dirty
// Document buffer BLOCKS with the guard, and Discard resolves it. Driven
// through the method, and the canvas is asserted to render no picker at all.
async function selectDocumentRouteScenario() {
  const calls = [];
  const root = new Node('div');
  const controller = mountDoxBenchCanvas(root, makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const initialPath = controller.state().buffers.document.path;

  // a clean switch lands
  const cleanSwitch = await controller.selectDocument(DOC_B);
  const afterCleanSwitch = { result: cleanSwitch,
                             path: controller.state().buffers.document.path };

  // make it dirty, then attempt to switch back: blocked, guard shown, and the
  // buffer stays exactly where it was
  await controller.edit('document', '# dirty via the selection route\n');
  const blocked = await controller.selectDocument(DOC_A);
  const afterBlockedAttempt = {
    result: blocked,
    documentPath: controller.state().buffers.document.path,
    guardHidden: controller.elements().guard().hidden,
  };

  // resolve with Discard: the switch completes
  await controller.resolveGuard('discard');
  const afterDiscardResolves = { path: controller.state().buffers.document.path };

  return {
    initialPath, afterCleanSwitch, afterBlockedAttempt, afterDiscardResolves,
    // the retired control, asserted absent rather than assumed gone
    selects: root.walk().filter((n) => n.tagName === 'SELECT').length,
    pickerNodes: root.walk().filter(
      (n) => String(n.className).includes('doxbench-document-picker')).length,
  };
}

// S4: destroy() makes the controller fully inert -- no further mutation, no
// further persistence.
async function postDestroyInertScenario() {
  const calls = [];
  const storage = new FakeStorage();
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage, previewDelayMs: 5,
  });
  await controller.ready;
  controller.destroy();
  const storageBefore = JSON.stringify([...storage.values.entries()]);

  const editResult = await controller.edit('document', '# post destroy\n');
  const discardResult = await controller.discard('document');
  const selectResult = await controller.selectDocument(DOC_B);
  const guardResult = await controller.resolveGuard('cancel');
  const tabBefore = controller.activeBuffer();
  controller.setActiveBuffer('document');
  const tabAfter = controller.activeBuffer();
  const stateAfter = controller.state().buffers.document;
  const storageAfter = JSON.stringify([...storage.values.entries()]);

  return {
    editResult, discardResult, selectResult, guardResult,
    tabUnchanged: tabBefore === tabAfter,
    stateContent: stateAfter.content,
    storageUnchanged: storageBefore === storageAfter,
  };
}

// ---------------------------------------------------------------------------
// T104 F6-1: EVERY transition that moves a buffer's settled identity tells the
// composition, not only edit(). Discard moves current_hash back to the base
// and a document switch replaces the whole buffer -- with no callback the
// rail's proposal cards kept scoring 'current' (Apply enabled) against text
// the buffer no longer held. The save() half of the same finding is pinned in
// the Save-seam harness below, where a seam exists.
// ---------------------------------------------------------------------------
async function identitySettledScenario() {
  const settled = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
    onIdentitySettled: (kind, hash) =>
      settled.push({ kind, hex: hash && hash.hex }),
  });
  await controller.ready;
  await controller.edit('document', '# identity moves\n');
  const afterEdit = settled.slice();
  await controller.discard('document');
  const afterDiscard = settled.slice();
  const baseHex = controller.state().buffers.document.base_hash.hex;
  await controller.selectDocument(DOC_B);
  const afterSwitch = settled.slice();
  const switchedHex = controller.state().buffers.document.current_hash.hex;
  return { afterEdit, afterDiscard, afterSwitch, baseHex, switchedHex };
}

// ---------------------------------------------------------------------------
// T104 F6-2: the textareas are mounted BEFORE initialLoad() resolves, so a
// keystroke during the source fetch used to throw an unhandled TypeError off
// the async input listener (state is still null) and then be silently
// overwritten by the load's own sync. The pre-state posture must refuse
// VISIBLY (CHK016/CHK019): disabled surfaces, a stated loading line, and a
// fixed refusal for anything that reaches the API anyway.
// ---------------------------------------------------------------------------
async function inputDuringLoadScenario() {
  let releaseLoad;
  const gate = new Promise((resolve) => { releaseLoad = resolve; });
  const gatedLoadSource = async (path) => {
    await gate;
    return { content: CONTENT[path], revision: 'rev-' + path, ref: 'main' };
  };
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: gatedLoadSource, storage: new FakeStorage(), previewDelayMs: 5,
    // a seam, so save() reaches its own state dereference rather than the
    // unwired-refusal early return
    save: async () => ({ status: 'unchanged', buffers: [] }),
  });
  const textarea = controller.elements().textarea('document');
  const status = controller.elements().status('document');
  const duringDisabled = {
    outline: controller.elements().textarea('outline').disabled === true,
    document: textarea.disabled === true,
  };
  // P3-2: the controls whose handlers DROP their refusal objects must be
  // physically refused too, exactly like the textareas -- a clickable Discard
  // whose click silently does nothing is the dishonest half of this posture.
  const duringControls = {
    // PIN EVOLUTION (add-doxbench-editing-phase-a): the panel carries ONE
    // Cancel where each buffer used to carry its own Discard, so the controls
    // are looked up without a buffer kind. The posture itself is unchanged.
    discardDisabled: controller.elements().cancel().disabled === true,
    saveDisabled: controller.elements().save().disabled === true,
  };
  const duringStatus = String(status.textContent);
  let threw = null;
  textarea.value = '# typed before the load settled\n';
  try { await fireEvent(textarea, 'input'); } catch (err) { threw = String(err && err.message); }
  const statusAfterKeystroke = String(status.textContent);
  const results = {};
  const attempt = async (name, fn) => {
    try { results[name] = await fn(); }
    catch (err) { results[name] = { threw: String(err && err.message) }; }
  };
  await attempt('discard', () => controller.discard('document'));
  await attempt('save', () => controller.save());
  await attempt('select', () => controller.selectDocument(DOC_B));
  await attempt('apply', () => controller.applyProposal('document', {
    base_hash: 'c'.repeat(64), content: '# applied\n' }));
  releaseLoad();
  await controller.ready;
  return {
    duringDisabled, duringControls, duringStatus, threw, statusAfterKeystroke,
    results,
    afterDisabled: textarea.disabled === true,
    afterContent: controller.state().buffers.document.content,
    // P3-2: the first syncBufferDom ends the mount-time posture. Since Brett's
    // 2026-08-18 annotation round 2 the controls also carry the DIRTY state, so
    // a settled-but-clean canvas holds them disabled for a second, honest
    // reason -- both probes are taken so the two reasons stay distinguishable.
    afterControls: {
      discardDisabled: controller.elements().cancel().disabled === true,
      saveDisabled: controller.elements().save().disabled === true,
      },
    afterDirtyControls: await (async () => {
      // the ACTIVE buffer, because Cancel is aimed at that one and Save at the
      // whole dirty set -- dirtying only the inactive buffer would leave Cancel
      // correctly unreachable and prove nothing about the loading window
      await controller.edit('outline', '# dirty after the load settled\n');
      return {
        discardDisabled: controller.elements().cancel().disabled === true,
        saveDisabled: controller.elements().save().disabled === true,
      };
    })(),
  };
}

// ---------------------------------------------------------------------------
// T104 F6-6: a document whose bytes exceed the hashing bound used to
// dead-letter the whole mount -- createDoxBenchState rejected inside
// initialLoad(), no production code consumed the returned ready promise,
// `state` stayed null forever, and the canvas rendered as a silently broken
// editor whose every keystroke threw. The failure must be STATED (the size
// class, never the content) and the surfaces must hold the same refuse-visibly
// posture as the loading state.
// ---------------------------------------------------------------------------
async function oversizedInitialLoadScenario() {
  const big = 'a'.repeat(400001);
  const map = { ...CONTENT, [DOC_A]: big };
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(map, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  let readyThrew = null;
  try { await controller.ready; } catch (err) { readyThrew = String(err && err.message); }
  const status = controller.elements().status('document');
  const textarea = controller.elements().textarea('document');
  const statusText = String(status.textContent);
  const outlineStatusText = String(controller.elements().status('outline').textContent);
  let inputThrew = null;
  textarea.value = '# typed into a failed canvas\n';
  try { await fireEvent(textarea, 'input'); } catch (err) { inputThrew = String(err && err.message); }
  return {
    readyThrew, inputThrew, statusText, outlineStatusText,
    stateIsNull: controller.state() === null,
    textareaDisabled: textarea.disabled === true,
    statusAfterKeystroke: String(status.textContent),
    // P3-2: after a FAILED load syncBufferDom never runs, so the mount-time
    // disabled posture is what keeps these controls honest permanently.
    failedControls: {
      discardDisabled: controller.elements().cancel().disabled === true,
      saveDisabled: controller.elements().save().disabled === true,
      },
  };
}

// ---------------------------------------------------------------------------
// T104 F10-3, the client half of FR-045's byte-exact round-trip: a real
// browser's textarea API value is LF-normalized BY SPECIFICATION no matter
// what the document's bytes are, so this scenario TYPES in the LF domain the
// way a browser reports it and asserts the BUFFER keeps the document's own
// CRLF flavor -- identity, dirtiness, and Save payload all speak the file's
// real line endings while the display speaks the textarea's.
// ---------------------------------------------------------------------------
async function eolPreservationScenario() {
  const CRLF_PATH = 'ideation/staging/topic-x/windows.md';
  const CRLF_BASE = '# Title\r\n\r\nline one\r\nline two\r\n';
  const map = { ...CONTENT, [CRLF_PATH]: CRLF_BASE };
  const projection = makeProjection({
    editable_paths: [OUTLINE_PATH, CRLF_PATH, DOC_A],
    context_paths: [OUTLINE_PATH, CRLF_PATH, DOC_A],
    active_document_candidates: [CRLF_PATH, DOC_A],
  });
  const controller = mountDoxBenchCanvas(new Node('div'), projection, {
    loadSource: makeLoadSource(map, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const textarea = controller.elements().textarea('document');
  const loadedBuffer = controller.state().buffers.document;
  const loaded = {
    content: loadedBuffer.content,
    dirty: loadedBuffer.dirty,
    textareaValue: textarea.value,
  };

  textarea.value = '# Title\n\nline one\nline two\ntyped\n'; // the browser's LF spelling
  await fireEvent(textarea, 'input');
  const typedBuffer = controller.state().buffers.document;
  const expectedTyped = '# Title\r\n\r\nline one\r\nline two\r\ntyped\r\n';
  const expectedIdentity = await contentIdentity(expectedTyped);
  const typed = {
    content: typedBuffer.content, dirty: typedBuffer.dirty,
    hashHex: typedBuffer.current_hash && typedBuffer.current_hash.hex,
    expectedContent: expectedTyped,
    expectedHex: expectedIdentity.hex,
    textareaValue: textarea.value,
  };

  textarea.value = '# Title\n\nline one\nline two\n'; // back to the loaded text
  await fireEvent(textarea, 'input');
  const backBuffer = controller.state().buffers.document;
  const back = { content: backBuffer.content, dirty: backBuffer.dirty };

  // W-2: a PROPOSAL enters through the same lens as a keystroke. The model's
  // spelling is LF regardless of the document's flavor; applied verbatim it
  // made the buffer pure LF (a Save then committed an every-line-ending
  // rewrite) and the next keystroke flipped the file back -- two byte-level
  // outcomes for one reviewed proposal.
  const preApply = controller.state().buffers.document;
  const applyRes = await controller.applyProposal('document', {
    base_hash: preApply.current_hash.hex,
    content: '# Title\n\nrewritten by the model\n',
  });
  const appliedBuffer = controller.state().buffers.document;
  const expectedApplied = '# Title\r\n\r\nrewritten by the model\r\n';
  const appliedIdentity = await contentIdentity(expectedApplied);
  const applied = {
    ok: !!(applyRes && applyRes.ok === true),
    content: appliedBuffer.content,
    expectedContent: expectedApplied,
    hashHex: appliedBuffer.current_hash && appliedBuffer.current_hash.hex,
    expectedHex: appliedIdentity.hex,
    textareaValue: textarea.value,
  };
  // the applied proposal left the buffer dirty; discard so the document
  // switch below is not intercepted by the Save-or-Discard guard
  await controller.discard('document');

  // the LF control: an LF document's keystrokes must not invent CRs
  await controller.selectDocument(DOC_A);
  textarea.value = '# Document A\nplus one line\n';
  await fireEvent(textarea, 'input');
  const lfBuffer = controller.state().buffers.document;
  const lf = { content: lfBuffer.content, dirty: lfBuffer.dirty };

  // ... and neither must an applied proposal (the lens applies the document's
  // OWN flavor, never a fixed one)
  const lfPre = controller.state().buffers.document;
  await controller.applyProposal('document', {
    base_hash: lfPre.current_hash.hex,
    content: '# Document A\nmodel rewrite\n',
  });
  const lfApplied = { content: controller.state().buffers.document.content };

  return { loaded, typed, back, applied, lf, lfApplied };
}

// ---------------------------------------------------------------------------
// P3-1 (wave re-review P3 tail): EOL-ONLY dirtiness is STATED. The first-break
// rule unifies a mixed-EOL document on the first keystroke, so a buffer can be
// dirty while the textarea's display is byte-identical to the loaded text --
// invisible dirtiness, and a Save then commits a whole-file line-ending diff
// nobody saw. The status line must state that fact in fixed vocabulary, while
// an ordinarily dirty buffer keeps the ordinary sentence.
// ---------------------------------------------------------------------------
async function eolOnlyDirtyScenario() {
  const MIXED_PATH = 'ideation/staging/topic-x/mixed.md';
  // first line break is CRLF (names the flavor); one stray LF line mixes it
  const MIXED_BASE = '# Title\r\nline a\nline b\r\n';
  const map = { ...CONTENT, [MIXED_PATH]: MIXED_BASE };
  const projection = makeProjection({
    editable_paths: [OUTLINE_PATH, MIXED_PATH],
    context_paths: [OUTLINE_PATH, MIXED_PATH],
    active_document_candidates: [MIXED_PATH],
  });
  const controller = mountDoxBenchCanvas(new Node('div'), projection, {
    loadSource: makeLoadSource(map, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const textarea = controller.elements().textarea('document');
  const status = controller.elements().status('document');
  // type-and-revert in the display domain: the textarea's value is unchanged,
  // but read-back re-flavors the stray LF line to the document's own CRLF --
  // the bytes move while the display does not.
  textarea.value = textarea.value;
  await fireEvent(textarea, 'input');
  const buffer = controller.state().buffers.document;
  const eolOnly = {
    dirty: buffer.dirty,
    bytesMoved: buffer.content !== buffer.base_content,
    displayIdentical: textarea.value === buffer.base_content.replace(/\r\n?/g, '\n'),
    status: String(status.textContent),
  };
  // an ORDINARY dirty edit keeps the ordinary sentence
  textarea.value = textarea.value + 'typed\n';
  await fireEvent(textarea, 'input');
  const ordinary = { status: String(status.textContent) };
  return { eolOnly, ordinary };
}

// ---------------------------------------------------------------------------
// P3-10 (wave re-review P3 tail): an edit whose async hash settles AFTER
// destroy() must leave the world alone. The settle continuation used to run
// to completion on the corpse -- replaceBuffer, persistNow, onIdentitySettled
// -- so a destroy followed by the FR-039 clear had its cleared record quietly
// re-persisted by the losing race. destroy()'s OWN persist (before the clear)
// is legitimate and stays.
// ---------------------------------------------------------------------------
async function destroyDuringEditSettleScenario() {
  const RACE = '# destroyed mid-hash\n';
  let release;
  const gate = new Promise((resolve) => { release = resolve; });
  const gatedHash = async (content) => {
    if (content === RACE) await gate;
    return contentIdentity(content);
  };
  const storage = new FakeStorage();
  const settledKinds = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage, previewDelayMs: 5,
    hash: gatedHash,
    onIdentitySettled: (kind) => settledKinds.push(kind),
  });
  await controller.ready;
  const editPromise = controller.edit('document', RACE);
  controller.destroy();       // persists its own final record on the way out
  storage.values.clear();     // the FR-039-style clear then removes it
  const notifiedBeforeSettle = settledKinds.length;
  release();
  const editResult = await editPromise;
  return {
    editResult,
    storageKeysAfterSettle: [...storage.values.keys()],
    lateNotifications: settledKinds.length - notifiedBeforeSettle,
  };
}

// ---------------------------------------------------------------------------
// add-doxbench-editing-phase-a. The canvas presents ONE buffer -- the active
// one, chosen by the context region -- as two VIEW tabs, and carries one Save
// and one Cancel outside both of them.
// ---------------------------------------------------------------------------

function surveyCanvas(root) {
  const nodes = root.walk();
  const hasClass = (n, c) => String(n.className).split(' ').includes(c);
  return {
    tablists: nodes.filter((n) => n.getAttribute('role') === 'tablist')
      .map((n) => ({ cls: n.className, label: n.getAttribute('aria-label') })),
    tabs: nodes.filter((n) => n.getAttribute('role') === 'tab')
      .map((n) => ({ cls: n.className, text: n.textContent,
                     selected: n.getAttribute('aria-selected'),
                     tabIndex: n.tabIndex,
                     controls: n.getAttribute('aria-controls') })),
    tabpanels: nodes.filter((n) => n.getAttribute('role') === 'tabpanel')
      .map((n) => ({ cls: n.className, id: n.id, tabIndex: n.tabIndex,
                     labelledBy: n.getAttribute('aria-labelledby'),
                     hidden: n.hidden === true })),
    saveButtons: nodes.filter((n) => hasClass(n, 'doxbench-save')).length,
    cancelButtons: nodes.filter((n) => hasClass(n, 'doxbench-cancel')).length,
    textareas: nodes.filter((n) => n.tagName === 'TEXTAREA').length,
  };
}

// The mount posture: two view tabs, Preview selected, no second tablist, and
// exactly one of each panel control.
async function viewTabsScenario() {
  const root = new Node('div');
  const controller = mountDoxBenchCanvas(root, makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const atMount = surveyCanvas(root);
  const activeView = controller.activeView();
  // the Editor pane is not on screen beside the rendering -- it is the OTHER
  // view of the same buffer
  const editorPaneHidden = controller.elements().textarea('outline')
    .closest('.doxbench-viewpane').hidden === true;
  const previewPaneHidden = controller.elements().preview('outline')
    .closest('.doxbench-viewpane').hidden === true;
  // only the ACTIVE buffer is mounted on the canvas
  const activeBufferBoxHidden = {
    outline: controller.elements().preview('outline')
      .closest('.doxbench-bufferbox').hidden === true,
    document: controller.elements().preview('document')
      .closest('.doxbench-bufferbox').hidden === true,
  };
  controller.setActiveView('editor');
  const afterEditor = surveyCanvas(root);
  const afterEditorPanes = {
    editorHidden: controller.elements().textarea('outline')
      .closest('.doxbench-viewpane').hidden === true,
    previewHidden: controller.elements().preview('outline')
      .closest('.doxbench-viewpane').hidden === true,
  };
  return {
    atMount, activeView, editorPaneHidden, previewPaneHidden,
    activeBufferBoxHidden, afterEditor, afterEditorPanes,
    activeBuffer: controller.activeBuffer(),
  };
}

// D2: switching INTO Preview brings the rendering up to the buffer's current
// content BEFORE the pane is shown; switching into Editor needs no flush and
// transforms nothing.
async function viewSwitchFlushScenario() {
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(),
    previewDelayMs: 10_000,   // long enough that only an explicit flush can win
  });
  await controller.ready;
  controller.setActiveView('editor');
  const preview = controller.elements().preview('outline');
  await controller.edit('outline', '# typed while Preview was hidden\n');
  const renderedBeforeSwitch = String(preview.innerHTML);
  controller.setActiveView('preview');
  const renderedAfterSwitch = String(preview.innerHTML);
  // and back: the raw text is shown as it stands, untransformed
  controller.setActiveView('editor');
  const textareaAfterReturn = controller.elements().textarea('outline').value;
  return { renderedBeforeSwitch, renderedAfterSwitch, textareaAfterReturn };
}

// The context region's two selection routes, driven through the controller
// primitives the shell calls: the outline selection tab, and a scoped docs row.
async function selectionDrivesTheActiveBufferScenario() {
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  controller.setActiveBuffer('outline');
  const afterOutlineTab = {
    active: controller.activeBuffer(),
    stateActive: controller.state().active_buffer,
  };
  const switched = await controller.selectDocument(DOC_B);
  const afterDocsRow = {
    active: controller.activeBuffer(),
    stateActive: controller.state().active_buffer,
    path: controller.state().buffers.document.path,
  };
  // choosing the row that is ALREADY loaded still binds to it
  controller.setActiveBuffer('outline');
  const unchanged = await controller.selectDocument(DOC_B);
  const afterReselect = controller.activeBuffer();
  // and a view tab may never be asked to choose a buffer
  let viewTabRefusal = null;
  try { controller.setActiveView('document'); }
  catch (err) { viewTabRefusal = String(err && err.message); }
  return {
    afterOutlineTab, switched, afterDocsRow, unchanged, afterReselect,
    viewTabRefusal, activeAfterRefusal: controller.activeBuffer(),
  };
}

// Cancel: the ACTIVE buffer returns to its base, no other buffer moves, the
// buffer it reverted is NAMED, and the settled-identity notification fires
// exactly as the guard's Discard fires it.
async function panelCancelScenario() {
  const settled = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
    onIdentitySettled: (kind, hash) => settled.push({ kind, hex: hash && hash.hex }),
  });
  await controller.ready;
  await controller.edit('outline', '# outline edited\n');
  await controller.edit('document', '# document edited\n');
  controller.setActiveBuffer('document');
  const settledBefore = settled.length;
  const cancelBtn = controller.elements().cancel();
  await fireEvent(cancelBtn, 'click');
  const after = controller.state().buffers;
  return {
    cancelledKindStated: String(controller.elements().status('document').textContent),
    document: { content: after.document.content, dirty: after.document.dirty },
    outline: { content: after.outline.content, dirty: after.outline.dirty },
    identityAfterCancel: settled.slice(settledBefore),
    documentBaseHex: after.document.base_hash.hex,
    // no force path: Cancel persists nothing and reaches no seam
    controls: {
      save: controller.elements().save().className,
      cancel: cancelBtn.className,
    },
  };
}

// PR #196 review F1: DECLINING a document switch must not move the chat's
// working context. The human is on the OUTLINE, the document buffer happens to
// be dirty, they pick a different docs row, the guard opens -- and they say
// Cancel. Nothing about that sequence is a decision to work on the document,
// and the binding is PERSISTED, so a wrong one survives the reload too.
async function guardCancelDoesNotRebindScenario() {
  const storage = new FakeStorage();
  const projection = makeProjection();
  const controller = mountDoxBenchCanvas(new Node('div'), projection, {
    loadSource: makeLoadSource(CONTENT, []), storage, previewDelayMs: 5,
  });
  await controller.ready;
  controller.setActiveBuffer('outline');           // the human is on the outline
  await controller.edit('document', '# unsaved document work\n');
  const before = {
    active: controller.activeBuffer(),
    stateActive: controller.state().active_buffer,
  };
  const blocked = await controller.selectDocument(DOC_B);   // guard opens
  const activeWhileGuarded = controller.activeBuffer();
  const cancelled = await controller.resolveGuard('cancel');
  const after = {
    active: controller.activeBuffer(),
    stateActive: controller.state().active_buffer,
    documentPath: controller.state().buffers.document.path,
    documentDirty: controller.state().buffers.document.dirty,
  };
  // the PERSISTED record is the half a reload would resurrect
  const persistedActive = JSON.parse(
    storage.values.get([...storage.values.keys()].pop())).active_buffer;
  // …and the DISCARD arm, by contrast, really does switch, so it really does
  // bind: a switch that happened is a binding that happened.
  const controller2 = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller2.ready;
  controller2.setActiveBuffer('outline');
  await controller2.edit('document', '# unsaved document work\n');
  await controller2.selectDocument(DOC_B);
  await controller2.resolveGuard('discard');
  return {
    before, blocked, activeWhileGuarded, cancelled, after, persistedActive,
    afterDiscardArm: {
      active: controller2.activeBuffer(),
      path: controller2.state().buffers.document.path,
    },
  };
}

// PR #196 review F6: a document past the hashing bound rejects INSIDE the
// switch. Every route into selectDocument reaches it through a handler that
// drops the returned promise, so an uncontained rejection said nothing at all
// and left the asking control showing a document that never loaded.
async function oversizedSwitchScenario() {
  const map = { ...CONTENT, [DOC_B]: 'a'.repeat(400001) };
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(map, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const before = controller.state().buffers.document;
  let threw = null;
  let result = null;
  try {
    result = await controller.selectDocument(DOC_B);
  } catch (err) {
    threw = String(err && err.message);
  }
  const after = controller.state().buffers.document;
  // …and again through the GUARD's discard arm, the other caller that reaches
  // switchDocument through a handler which drops the returned promise
  await controller.edit('document', '# dirty before the failing switch\n');
  await controller.selectDocument(DOC_B);              // blocked by the guard
  let guardThrew = null;
  let guardResolved = null;
  try { guardResolved = await controller.resolveGuard('discard'); }
  catch (err) { guardThrew = String(err && err.message); }
  return {
    threw, result, guardThrew, guardResolved,
    status: String(controller.elements().status('document').textContent),
    before: { path: before.path, content: before.content },
    after: { path: after.path, content: after.content, dirty: after.dirty },
    afterGuard: { path: controller.state().buffers.document.path },
  };
}

// PR #196 review F7: the remembered caret and scroll belong to the document
// that LEFT. Carried across a switch they are re-applied to a document that
// never had them -- an offset with no relationship to the text under it.
async function switchDropsTheStaleViewScenario() {
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  controller.setActiveView('editor');
  controller.setActiveBuffer('document');
  const area = controller.elements().textarea('document');
  area.selectionStart = 5; area.selectionEnd = 7; area.scrollTop = 40;
  area.focus();
  // leaving CAPTURES the view; this is the entry that must not survive a
  // whole-buffer replacement
  controller.setActiveBuffer('outline');
  const capturedWhileAway = controller.viewState('document');
  await controller.selectDocument(DOC_B);   // replaces the buffer, and re-binds
  const after = controller.viewState('document');
  return {
    capturedWhileAway,
    activeAfter: controller.activeBuffer(),
    after: { selectionStart: after.selectionStart, selectionEnd: after.selectionEnd,
             scrollTop: after.scrollTop },
    content: controller.state().buffers.document.content,
  };
}

// Brett's 2026-08-18 annotation round 2: "remove these lines. the UI must be
// intuitive and not rely on this text to inform the user." The STANDING text
// goes; the state it carried becomes control state, the durable per-buffer
// sentences go sr-only, and an EVENT gets one transient visible line.
async function statusbarPostureScenario() {
  const root = new Node('div');
  const controller = mountDoxBenchCanvas(root, makeProjection(), {
    loadSource: makeLoadSource(CONTENT, []), storage: new FakeStorage(),
    previewDelayMs: 5, eventNoteMs: 50,
    save: async () => ({ status: 'refused', buffers: [{
      key: 'outline', status: 'refused', action: 'edit-document', ref: null,
      revision: null, content_hash: null,
      message: 'the outline base moved under this buffer' }] }),
  });
  await controller.ready;
  const srOnly = (kind) => String(controller.elements().status(kind).className)
    .includes('doxbench-sronly');
  const note = controller.elements().eventNote();
  const clean = {
    saveDisabled: controller.elements().save().disabled === true,
    cancelDisabled: controller.elements().cancel().disabled === true,
    statusSrOnly: { outline: srOnly('outline'), document: srOnly('document') },
    // the sentences are still THERE, and still name their buffer
    statusText: String(controller.elements().status('outline').textContent),
    live: controller.elements().status('outline').getAttribute('aria-live'),
    eventHidden: note.hidden === true,
    // the wired posture's standing "Save persists only the changed buffers…"
    // note is deleted outright
    hostText: root.textContent,
  };
  // dirty the ACTIVE buffer: both controls come live, with no sentence needed
  await controller.edit('outline', '# outline edited\n');
  const dirty = {
    saveDisabled: controller.elements().save().disabled === true,
    cancelDisabled: controller.elements().cancel().disabled === true,
  };
  // an EVENT -- a Save that refuses -- is visible, transiently
  await controller.save();
  const onEvent = {
    eventHidden: note.hidden === true,
    eventText: String(note.textContent),
    // …and the durable per-buffer verdict is still in its own sr-only region
    statusText: String(controller.elements().status('outline').textContent),
  };
  await new Promise((r) => setTimeout(r, 90));
  const afterFade = {
    eventHidden: note.hidden === true,
    eventText: String(note.textContent),
    statusText: String(controller.elements().status('outline').textContent),
  };
  return { clean, dirty, onEvent, afterFade };
}

const previewCases = JSON.parse(readFileSync(process.argv[2], 'utf8'));

const results = {
  viewTabs: DOXBENCH_VIEW_TABS,
  bufferLabels: DOXBENCH_BUFFER_LABELS,
  saveUnavailableReason: SAVE_UNAVAILABLE_REASON,
  guardSave: await guardScenario('save'),
  guardCancel: await guardScenario('cancel'),
  guardDiscard: await guardScenario('discard'),
  cleanSwitch: await cleanSwitchScenario(),
  focusPersistence: await focusPersistenceScenario(),
  noAutoFocus: await noAutoFocusScenario(),
  sessionRestore: await sessionRestoreScenario(),
  emptyOutline: await emptyOutlineScenario(),
  noLoadSource: await noLoadSourceScenario(),
  hostilePreview: await hostilePreviewScenario(),
  unicode: await unicodeScenario(previewCases),
  surrogate: await surrogateScenario(),
  generationRace: await generationRaceScenario(),
  editThenDiscardBeforeSettle: await editThenDiscardBeforeSettleScenario(),
  editThenSwitchBeforeSettle: await editThenSwitchBeforeSettleScenario(),
  inputRefusal: await inputRefusalScenario(),
  selectDuringLoad: await selectDuringLoadScenario(),
  applyRefusalCodes: await applyRefusalCodesScenario(),
  typedOutlineOverridesEmpty: await typedOutlineOverridesEmptyScenario(),
  typedDocumentOverridesUnavailable: await typedDocumentOverridesUnavailableScenario(),
  outOfScopeSelectDocument: await outOfScopeSelectDocumentScenario(),
  accessibility: await accessibilityScenario(),
  guardFocus: await guardFocusScenario(),
  selectDocumentRoute: await selectDocumentRouteScenario(),
  postDestroyInert: await postDestroyInertScenario(),
  identitySettled: await identitySettledScenario(),
  inputDuringLoad: await inputDuringLoadScenario(),
  oversizedLoad: await oversizedInitialLoadScenario(),
  eolPreservation: await eolPreservationScenario(),
  eolOnlyDirty: await eolOnlyDirtyScenario(),
  destroyDuringEditSettle: await destroyDuringEditSettleScenario(),
  viewTabSurvey: await viewTabsScenario(),
  viewSwitchFlush: await viewSwitchFlushScenario(),
  selectionDrivesTheActiveBuffer: await selectionDrivesTheActiveBufferScenario(),
  panelCancel: await panelCancelScenario(),
  guardCancelDoesNotRebind: await guardCancelDoesNotRebindScenario(),
  oversizedSwitch: await oversizedSwitchScenario(),
  switchDropsStaleView: await switchDropsTheStaleViewScenario(),
  statusbarPosture: await statusbarPostureScenario(),
  gateAbsentSlot: await gateAbsentSlotScenario(),
  saveInFlightSlot: await saveInFlightSlotScenario(),
};

console.log(JSON.stringify(results));
"""


@pytest.fixture(scope="module")
def editor_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench editor probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-editor")
    (tmp_path / "views").mkdir()
    (tmp_path / "vendor").mkdir()
    shutil.copy(EDITOR_JS, tmp_path / "views" / "doxbench-editor.js")
    shutil.copy(STATE_JS, tmp_path / "views" / "doxbench-state.js")
    shutil.copy(VIEWER_JS, tmp_path / "views" / "viewer.js")
    shutil.copy(VENDOR_MARKDOWN_JS, tmp_path / "vendor" / "markdown-it.min.js")
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "vendor" / "package.json").write_text(
        '{"type": "commonjs"}', encoding="utf-8"
    )
    harness = tmp_path / "views" / "editor-harness.mjs"
    harness.write_text(_EDITOR_HARNESS, encoding="utf-8")
    proc = subprocess.run(
        [NODE, str(harness), str(PREVIEW_CASES_PATH)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_canvas_view_tabs_are_exactly_editor_and_preview(editor_results):
    """add-doxbench-editing-phase-a, first ADDED requirement. PIN EVOLUTION:
    this test used to read `DOXBENCH_BUFFER_TABS` and assert the canvas's own
    two BUFFER tabs. That tablist is retired as a control — the context region
    selects the buffer now, and two surfaces answering one question is how the
    two come to disagree. What the canvas tabs is the VIEW of the one active
    buffer, and it is exactly `Editor` and `Preview`, in that rendered order."""
    assert editor_results["viewTabs"] == [
        {"key": "editor", "label": "Editor"},
        {"key": "preview", "label": "Preview"},
    ]


def test_the_buffer_labels_survive_the_retired_tablist_without_being_a_control(
    editor_results,
):
    """FR-004 + Phase A task 2.2: the two buffers are unchanged, and their
    labels survive under a name that does not claim to be a control — they
    feed accessible names (each buffer's status region and its textarea), and
    nothing renders them as a tab strip any more. The exactly-two invariant
    itself is asserted against `BUFFER_KINDS` in test_doxbench_state.py, which
    is where the enumeration authority actually lives."""
    assert editor_results["bufferLabels"] == {
        "outline": "Outline",
        "document": "Document",
    }


def test_the_canvas_mounts_on_preview_with_one_tablist_and_one_of_each_control(
    editor_results,
):
    """add-doxbench-editing-phase-a, "The canvas mounts" + "The canvas offers
    its controls": exactly two view tabs with `Preview` selected, the raw text
    and its rendering never both visible in one pane, exactly ONE tablist on
    the canvas (the retired buffer tablist is not rendered at all), and exactly
    one Save and one Cancel — outside both view tabs, so neither is drawn per
    view or per buffer."""
    survey = editor_results["viewTabSurvey"]
    at_mount = survey["atMount"]
    assert len(at_mount["tablists"]) == 1
    assert at_mount["tablists"][0]["cls"] == "doxbench-viewtabs"
    # the label names the VIEW CHOICE over the active buffer, never the old
    # generic "doxBench buffers" the retired tablist carried
    assert at_mount["tablists"][0]["label"] != "doxBench buffers"
    assert at_mount["tablists"][0]["label"].startswith("view of the active")
    assert [t["text"] for t in at_mount["tabs"]] == ["Editor", "Preview"]
    assert [t["selected"] for t in at_mount["tabs"]] == ["false", "true"]
    assert survey["activeView"] == "preview"
    # both buffers' textareas still exist (built once at mount); what changed
    # is that raw text and rendering are two VIEWS, never one split pane
    assert at_mount["textareas"] == 2
    assert survey["editorPaneHidden"] is True
    assert survey["previewPaneHidden"] is False
    # ONE buffer on the canvas: the active one
    assert survey["activeBuffer"] == "outline"
    assert survey["activeBufferBoxHidden"] == {"outline": False, "document": True}
    # ONE Save, ONE Cancel, and they do not multiply with the view
    assert at_mount["saveButtons"] == 1
    assert at_mount["cancelButtons"] == 1
    assert survey["afterEditor"]["saveButtons"] == 1
    assert survey["afterEditor"]["cancelButtons"] == 1


def test_the_view_tablist_keeps_the_apg_roving_pattern_it_inherited(editor_results):
    """CHK007 was measured and fixed once on the buffer tablist; moving the
    strip must not re-lose it. Exactly one tab is tabbable, and it is the
    selected one — the source-level Arrow/Home/End half is pinned in
    test_doxbench_accessibility.py."""
    for survey_key, selected_view in (("atMount", "Preview"), ("afterEditor", "Editor")):
        tabs = editor_results["viewTabSurvey"][survey_key]["tabs"]
        tabbable = [t for t in tabs if t["tabIndex"] == 0]
        assert len(tabbable) == 1, survey_key
        assert tabbable[0]["text"] == selected_view, survey_key
        assert tabbable[0]["selected"] == "true", survey_key
        # every tab controls the pane it labels
        assert all(t["controls"] for t in tabs), survey_key


def test_the_view_tabpanels_are_reachable_by_keyboard(editor_results):
    """PR #196 review F5 (WCAG 2.1.1): `Preview` is where a mount LANDS, and it
    is a scrollable region whose content — rendered Markdown — contains nothing
    focusable, so a keyboard-only human could tab to the panel and then be
    unable to scroll it. The APG's remedy for a tabpanel with no focusable
    content is a tabbable panel, applied to both panes so the rule survives a
    change of content."""
    panels = editor_results["viewTabSurvey"]["atMount"]["tabpanels"]
    assert len(panels) == 2
    for panel in panels:
        assert panel["tabIndex"] == 0, panel["cls"]
        assert panel["labelledBy"], panel["cls"]
    # …and exactly one of them is on screen: the panel pair is a view switch,
    # never a split
    assert [p["hidden"] for p in panels] == [True, False]


def test_switching_into_preview_flushes_the_pending_render(editor_results):
    """add-doxbench-editing-phase-a, "A human types and then switches to
    Preview": the debounce is allowed to leave a pane nobody can see stale, so
    the moment it becomes visible is exactly when it must not be. The scenario
    uses a 10-second debounce, so only the switch's own flush can have
    rendered the new text."""
    result = editor_results["viewSwitchFlush"]
    assert "typed while Preview was hidden" not in result["renderedBeforeSwitch"]
    assert "typed while Preview was hidden" in result["renderedAfterSwitch"]


def test_switching_back_to_editor_shows_the_raw_markdown_untransformed(editor_results):
    """The other half: `Editor` needs no flush, because raw text is never
    debounced, and the switch transforms no content."""
    result = editor_results["viewSwitchFlush"]
    assert result["textareaAfterReturn"] == "# typed while Preview was hidden\n"


def test_the_context_selection_chooses_the_active_buffer_not_the_view_tabs(
    editor_results,
):
    """add-doxbench-editing-phase-a: the outline selection tab makes the
    `outline` buffer active; selecting a scoped document makes the `document`
    buffer active and loads that exact document; re-selecting the document
    already loaded still BINDS to it; and a view tab asked to choose a buffer
    is refused outright."""
    result = editor_results["selectionDrivesTheActiveBuffer"]
    assert result["afterOutlineTab"] == {"active": "outline", "stateActive": "outline"}
    assert result["switched"]["status"] == "switched"
    assert result["afterDocsRow"]["active"] == "document"
    assert result["afterDocsRow"]["stateActive"] == "document"
    assert result["afterDocsRow"]["path"] == "ideation/staging/topic-x/second.md"
    assert result["unchanged"]["status"] == "unchanged"
    assert result["afterReselect"] == "document"
    assert result["viewTabRefusal"] is not None
    assert "view tab" in result["viewTabRefusal"]
    assert result["activeAfterRefusal"] == "document"


def test_declining_a_document_switch_does_not_move_the_chat_binding(editor_results):
    """PR #196 review F1 (BLOCKING, regression): the guard's Cancel is the "no,
    leave it alone" choice. It used to re-bind — the guard's focus return called
    `setActiveBuffer("document")` — so a human working on the OUTLINE who
    declined a document switch came back bound to the document, persisted, and
    every chat turn after that worked on material they never chose. Resolving
    the guard is a decision about a SWITCH; the binding follows a switch that
    actually happened, and nothing else."""
    result = editor_results["guardCancelDoesNotRebind"]
    assert result["before"] == {"active": "outline", "stateActive": "outline"}
    assert result["blocked"] == {"status": "blocked", "reason": "dirty_document"}
    # opening the guard is not a decision either
    assert result["activeWhileGuarded"] == "outline"
    assert result["cancelled"]["status"] == "cancelled"
    assert result["after"]["active"] == "outline"
    assert result["after"]["stateActive"] == "outline"
    # the persisted record is what a reload would resurrect
    assert result["persistedActive"] == "outline"
    # …and declining changed nothing else either: the document keeps its path
    # and its unsaved text
    assert result["after"]["documentPath"] == "ideation/staging/topic-x/detail.md"
    assert result["after"]["documentDirty"] is True
    # the contrapositive: the DISCARD arm really switches, so it really binds
    assert result["afterDiscardArm"] == {
        "active": "document", "path": "ideation/staging/topic-x/second.md",
    }


def test_a_document_that_cannot_be_loaded_refuses_visibly_instead_of_rejecting(
    editor_results,
):
    """PR #196 review F6: a document past the hashing bound rejects inside
    `createBufferState`, and every route into `selectDocument` reaches it
    through a click/change handler that drops the returned promise — so the
    rejection dead-lettered: nothing stated, and the asking control left
    showing a document that never loaded. Contained into the same stated
    refusal every other selection failure speaks, with the buffer untouched
    (the replacement never ran) and the picker reverted to what is really
    loaded."""
    result = editor_results["oversizedSwitch"]
    assert result["threw"] is None
    # PIN EVOLUTION (Brett's 2026-08-15 annotation round): the picker is retired,
    # so the second promise-dropping caller measured here is the GUARD's discard
    # arm, which reaches the same `switchDocument`.
    assert result["guardThrew"] is None
    assert result["guardResolved"]["status"] == "refused"
    assert result["afterGuard"]["path"] == result["before"]["path"]
    assert result["result"]["status"] == "refused"
    # the message names the byte class, never the document's text
    assert "400" in result["result"]["reason"] or "bytes" in result["result"]["reason"]
    assert "refused -- " in result["status"]
    # the buffer is exactly what it was
    assert result["after"]["path"] == result["before"]["path"]
    assert result["after"]["content"] == result["before"]["content"]
    assert result["after"]["dirty"] is False
    # …and the buffer never moved off the document it really holds


def test_a_document_switch_drops_the_previous_documents_caret_and_scroll(
    editor_results,
):
    """PR #196 review F7: FR-010 remembers a buffer's caret and scroll so a
    switch of VIEW or of BUFFER can put the human back where they were. A
    whole-document replacement is neither: the remembered offsets belong to a
    document that is no longer there, and re-applying them lands the human at a
    position with no relationship to the text under it (and, past the new
    document's end, at a caret the browser silently clamps). The entry is
    dropped with the buffer it described."""
    result = editor_results["switchDropsStaleView"]
    # the view really was captured on the way out — otherwise this proves nothing
    assert result["capturedWhileAway"]["selectionStart"] == 5
    assert result["capturedWhileAway"]["selectionEnd"] == 7
    # …and the new document starts clean
    assert result["content"] == "# Document B\n"
    assert result["activeAfter"] == "document"
    # SCROLL is the half this harness can speak to: hiding a pane drops the
    # layout box the browser keeps the offset in (the shim models exactly
    # that), so a non-zero scroll here could only have come from the restore
    # re-applying an offset that belonged to the document that left.
    assert result["after"]["scrollTop"] == 0
    # Selection is DOM state and survives hiding in both the shim and a real
    # document; a real browser additionally resets it when `.value` is
    # reassigned, which the shim does not model — so it is deliberately NOT
    # asserted here rather than asserted against the shim's own behaviour.


def test_the_standing_status_text_is_gone_and_the_controls_carry_the_state(
    editor_results,
):
    """Brett's 2026-08-18 annotation round 2: "remove these lines. the UI must be
    intuitive and not rely on this text to inform the user."

    The lines he is looking at are the STANDING ones — "Outline: no unsaved
    changes" beside "Document: no unsaved changes", and under them a permanent
    sentence explaining what Save does. He is right that a control's own
    enabled state says that better: Save is reachable exactly when there is
    something to save, Cancel exactly when the ACTIVE buffer has something to
    revert. So the state moves onto the controls and the sentences stop
    standing."""
    clean = editor_results["statusbarPosture"]["clean"]
    dirty = editor_results["statusbarPosture"]["dirty"]
    # nothing dirty: both controls say so by being unreachable
    assert clean["saveDisabled"] is True
    assert clean["cancelDisabled"] is True
    # something dirty: both come live, with no sentence needed
    assert dirty["saveDisabled"] is False
    assert dirty["cancelDisabled"] is False
    # …and the standing explanation of what Save does is deleted outright
    assert "Save persists only the changed buffers" not in clean["hostText"]


def test_the_per_buffer_sentences_survive_sr_only(editor_results):
    """The other half of the same annotation, and the reason it is not simply a
    deletion: these regions are the per-buffer verdict surface the ratified
    buffer contract requires a PARTIAL Save to be readable in, they are where
    every stated refusal on this canvas lands, and they are announced. They stay
    in the DOM, visually hidden, in the same sr-only idiom `.doxchat-announce`
    uses one region over — so a screen reader still hears them and every rule
    pinned on their sentences still holds."""
    clean = editor_results["statusbarPosture"]["clean"]
    assert clean["statusSrOnly"] == {"outline": True, "document": True}
    assert clean["live"] == "polite"
    # the sentence is still there, still naming its buffer
    assert clean["statusText"].startswith("Outline: ")
    assert "no unsaved changes" in clean["statusText"]


def test_an_event_refusal_is_visible_transiently_not_standing(editor_results):
    """The third half: an EVENT — a refusal, or a Save that did not wholly land
    — must still reach a sighted human, and the annotation forbids it standing
    there forever. One transient visible line carries exactly those, and clears
    itself; the durable, per-buffer detail stays in the sr-only regions, so
    nothing a test or an assistive technology relies on is lost with it."""
    posture = editor_results["statusbarPosture"]
    # nothing to say at rest
    assert posture["clean"]["eventHidden"] is True
    # a refused Save is said, visibly, and names the buffer it is about
    on_event = posture["onEvent"]
    assert on_event["eventHidden"] is False
    assert "Outline: " in on_event["eventText"]
    assert "base moved" in on_event["eventText"]
    # …and it clears itself, which is what makes it an event and not standing text
    after = posture["afterFade"]
    assert after["eventHidden"] is True
    assert after["eventText"] == ""
    # while the DURABLE per-buffer verdict is still readable in its own region
    assert "Save refused" in after["statusText"]
    assert "base moved" in after["statusText"]


def test_cancel_reverts_only_the_active_buffer_and_says_which(editor_results):
    """add-doxbench-editing-phase-a, "Cancel is invoked": the ACTIVE buffer
    returns to its last loaded or saved base, no other buffer changes, and the
    control names the buffer it reverted — one control that could have been
    aimed at either owes the human that sentence. Driven through the rendered
    button, not the method."""
    result = editor_results["panelCancel"]
    assert result["document"] == {"content": "# Document A\n", "dirty": False}
    # the buffer the human was NOT looking at is untouched: no silent reversal
    assert result["outline"] == {"content": "# outline edited\n", "dirty": True}
    assert "Cancel reverted the Document buffer" in result["cancelledKindStated"]


def test_cancel_moves_an_identity_and_says_so_like_a_discard(editor_results):
    """add-doxbench-editing-phase-a, "Cancel moves an identity": a discard
    moves the buffer's content identity back to its base, so the settled-identity
    notification MUST fire — otherwise the rail's proposal cards keep offering
    Apply against text the buffer no longer holds. Exactly ONE notification,
    for exactly the buffer that moved."""
    result = editor_results["panelCancel"]
    assert result["identityAfterCancel"] == [
        {"kind": "document", "hex": result["documentBaseHex"]},
    ]


def test_dirty_document_buffer_blocks_switching_to_a_different_document(editor_results):
    """FR-007 / AS4: selecting a different document while the active Document
    buffer is dirty is refused, the dirty text and path are untouched, and a
    guard region naming both Save and Discard is shown."""
    result = editor_results["guardSave"]
    assert result["blocked"] == {"status": "blocked", "reason": "dirty_document"}
    assert result["dirtyBuffer"]["content"] == "# Document A edited\n"
    assert result["dirtyBuffer"]["dirty"] is True
    assert result["dirtyBuffer"]["path"] == "ideation/staging/topic-x/detail.md"
    guard_text = (result["guardText"] or "").lower()
    assert "save" in guard_text and "discard" in guard_text


def test_resolve_guard_save_refuses_with_the_fixed_unavailable_reason(editor_results):
    """This slice has no governed Save (FR-031 is out of scope); resolving the
    guard with "save" MUST refuse with SAVE_UNAVAILABLE_REASON and change
    nothing -- no switch, buffer stays exactly as dirty as it was."""
    result = editor_results["guardSave"]
    assert result["resolved"]["status"] == "refused"
    assert result["resolved"]["reason"] == editor_results["saveUnavailableReason"]
    assert result["afterBuffer"] == result["dirtyBuffer"]


def test_resolve_guard_cancel_keeps_the_dirty_buffer_and_does_not_switch(editor_results):
    """resolveGuard("cancel") keeps the dirty Document buffer exactly as it
    was and performs no switch."""
    result = editor_results["guardCancel"]
    assert result["resolved"]["status"] == "cancelled"
    assert result["afterBuffer"] == result["dirtyBuffer"]


def test_resolve_guard_discard_restores_base_then_switches_to_the_requested_document(
    editor_results,
):
    """AS5: Discard restores the buffer to its last loaded base and THEN
    switches to the requested document, and the new path's loadSource is
    called exactly once."""
    result = editor_results["guardDiscard"]
    assert result["resolved"]["status"] == "switched"
    after = result["afterBuffer"]
    assert after["path"] == "ideation/staging/topic-x/second.md"
    assert after["dirty"] is False
    assert after["content"] == "# Document B\n"
    assert result["calls"].count("ideation/staging/topic-x/second.md") == 1


def test_clean_document_buffer_switches_immediately_without_a_guard(editor_results):
    """The contrapositive of AS4: a CLEAN Document buffer switches at once,
    with no guard ever shown."""
    result = editor_results["cleanSwitch"]
    assert result["result"] == {"status": "switched", "reason": None}
    assert result["guardPresent"] is False
    assert result["buffer"]["path"] == "ideation/staging/topic-x/second.md"


def test_focus_selection_and_scroll_are_independent_per_buffer_across_tab_switches(
    editor_results,
):
    """FR-010 / AS3: each buffer's focus/selection/scroll survive
    `setActiveBuffer` round trips (the buffer tablist that used to drive them
    is retired -- the context region owns that choice now), and one buffer's
    values never bleed into the other's."""
    result = editor_results["focusPersistence"]
    assert result["outlineViewAfterFocus"] == {
        "selectionStart": 2, "selectionEnd": 5, "scrollTop": 10, "focused": True,
    }
    assert result["documentViewNoFocus"]["selectionStart"] == 1
    assert result["documentViewNoFocus"]["selectionEnd"] == 3
    assert result["documentViewNoFocus"]["scrollTop"] == 20
    assert result["documentViewNoFocus"]["focused"] is False
    assert result["outlineViewAfterReturn"] == {
        "selectionStart": 2, "selectionEnd": 5, "scrollTop": 10, "focused": True,
    }
    assert result["outlineElSame"] is True


def test_focus_selection_and_scroll_survive_refresh_context_and_preview_flush(
    editor_results,
):
    """FR-010 / AS3: a docs/lens context refresh and a preview render must
    not disturb the active buffer's focus, selection, or scroll state."""
    result = editor_results["focusPersistence"]
    assert result["outlineViewAfterRefresh"] == result["outlineViewAfterReturn"]
    assert result["activeElementAfterRefresh"] == result["activeElementAfterReturn"]


def test_focus_restores_to_the_previously_focused_buffer_and_is_not_stolen_when_unfocused(
    editor_results,
):
    """FR-010: switching back to a tab that previously held real DOM focus
    restores that focus; switching to a tab that never held focus must not
    steal focus onto it."""
    result = editor_results["focusPersistence"]
    assert result["activeElementAfterSwitchNoFocus"] is None
    assert result["activeElementAfterReturn"]["tag"] == "TEXTAREA"

    no_auto = editor_results["noAutoFocus"]
    assert no_auto["afterDoc"] is None
    assert no_auto["afterOutline"] is None


def test_active_tab_and_dirty_buffers_restore_only_for_the_identical_scope_key(
    editor_results,
):
    """FR-011: a fresh mount with the identical scope key and the same
    injected storage restores the active tab and dirty Document content; a
    DIFFERENT tile_id restores nothing."""
    result = editor_results["sessionRestore"]
    assert result["restoredTab"] == "document"
    assert result["restoredState"]["buffers"]["document"]["dirty"] is True
    assert result["restoredState"]["buffers"]["document"]["content"] == "# Restore me\n"
    assert result["freshTab"] == "outline"
    assert result["freshState"]["buffers"]["document"]["dirty"] is False


def test_null_outline_path_is_explicit_empty_state_and_never_infers_from_document_headings(
    editor_results,
):
    """FR-006 / AS2: outline_path === null yields an explicit empty/create
    state -- never fabricated content, and never a heading borrowed from the
    Document buffer."""
    result = editor_results["emptyOutline"]
    outline = result["outline"]
    assert outline["path"] is None
    assert outline["content"] == ""
    assert outline["load_state"] == "empty"
    assert result["outlineTextareaValue"] == ""
    combined = (result["outlinePreviewHtml"] or "") + (result["outlinePreviewText"] or "")
    assert "INFERRED-OUTLINE-MARKER" not in combined
    assert combined.strip() != "", "the empty outline pane must state something, not blank"


def test_absent_load_source_reports_unavailable_backed_paths_without_fabrication(
    editor_results,
):
    """FR-007 edge case: with no `loadSource` injected at all, every backed
    path degrades to `unavailable` with empty content and an inline stated
    reason -- never fabricated, never a network attempt."""
    result = editor_results["noLoadSource"]
    assert result["outline"]["load_state"] == "unavailable"
    assert result["outline"]["content"] == ""
    assert result["doc"]["load_state"] == "unavailable"
    assert result["doc"]["content"] == ""
    assert (result["outlineReason"] or "").strip() != ""
    assert (result["docReason"] or "").strip() != ""


# ---- T030: shared Markdown preview safety + unusual-Unicode identity ------

def test_doxbench_editor_source_has_no_private_html_sink_or_second_sanitizer():
    """T030.1: the editor imports the ONE sanitizer seam from viewer.js,
    never assigns innerHTML itself, never constructs a second markdown-it,
    and never imports the vendored renderer directly."""
    source = EDITOR_JS.read_text(encoding="utf-8")
    assert "from \"./viewer.js\"" in source or "from './viewer.js'" in source
    assert "mountSafeMarkdown" in source
    assert "innerHTML" not in source
    assert "markdownit" not in source
    assert "markdown-it" not in source


def test_authoring_surfaces_disable_autofill_and_derive_text_direction():
    """T104 F9-2 + F9-4 (FR-044/FR-045), mirroring the chat rail's own pin
    (test_doxbench_chat_view.py's authoring-inputs test): the canvas's
    content-derived surfaces — each buffer's authoring textarea and its
    preview — derive text direction from their own bytes (`dir="auto"`), and
    every control a browser might try to autofill — the textareas and the
    textareas — refuses autofill. The status line stays direction-unset ON
    PURPOSE: status text is the fixed refusal/save vocabulary and never echoes
    buffer content, by house rule, so `dir="auto"` there would only imply a
    content-derivation that does not exist.

    PIN EVOLUTION (Brett's 2026-08-15 annotation round): the document picker
    was the other autofill-refusing control and it is retired, so its line goes
    with it — and the heading clause goes too, because the heading is retired
    as well (the region's accessible name carries the product name now)."""
    source = EDITOR_JS.read_text(encoding="utf-8")
    assert 'textarea.setAttribute("dir", "auto")' in source
    assert 'preview.setAttribute("dir", "auto")' in source
    assert 'textarea.setAttribute("autocomplete", "off")' in source
    # the retired picker's own autofill refusal is gone with the control
    assert "doxbench-document-picker" not in source


def test_selected_tab_styling_rides_aria_selected_not_a_shadow_class():
    """T104 F9-6: the selected-tab look is owned by the
    `.doxbench-viewtab[aria-selected="true"]` rule (the T100 operator patch
    overrides every property the old `-active` shadow-class rule set), so the
    class and the lockstep classList.toggle that maintained it were dead
    weight — a second spelling of the same state that could silently drift
    from the ARIA truth. Both are gone; selection state has exactly one
    spelling: `aria-selected`."""
    source = EDITOR_JS.read_text(encoding="utf-8")
    styles = (EDITOR_JS.parent.parent / "styles.css").read_text(encoding="utf-8")
    for shadow in ("doxbench-tab-active", "doxbench-viewtab-active"):
        assert shadow not in source, shadow
        assert shadow not in styles, shadow
    # and the class the rule keys on is the VIEW tab's, since that is the strip
    # the canvas now renders (add-doxbench-editing-phase-a)
    assert '.doxbench-viewtab[aria-selected="true"]' in styles


def test_hostile_markdown_preview_renders_through_the_one_safe_sink(editor_results):
    """T030.2: editing to hostile Markdown and flushing the preview produces
    exactly ONE non-empty HTML sink, whose class is the preview container's
    and whose bytes equal `renderSafeMarkdownHtml` computed independently in
    the same harness; script tags are escaped, javascript: links are inert,
    and external-scheme images defer behind the click-to-load placeholder."""
    result = editor_results["hostilePreview"]
    assert result["producedCount"] == 1
    assert result["producedClasses"] == [result["previewCls"]]
    assert result["sinkValue"] == result["expectedHtml"]
    assert "<script>" not in result["sinkValue"]
    assert "&lt;script&gt;" in result["sinkValue"]
    assert '<a href="javascript:' not in result["sinkValue"]
    assert result["sinkValue"].count('class="ext-img"') == 2
    assert '<img src="images/local.png"' in result["sinkValue"]


def _preview_case(editor_results, case_id):
    return editor_results["unicode"][case_id]


def test_combining_and_precomposed_unicode_forms_hash_differently(editor_results):
    """T030.3: `e` + a combining acute accent (NFD) and the precomposed
    character (NFC) are visually identical but byte-different -- their
    content identities MUST differ (no Unicode normalization anywhere)."""
    decomposed = _preview_case(editor_results, "combining_decomposed")
    precomposed = _preview_case(editor_results, "combining_precomposed")
    assert decomposed["content"] != precomposed["content"]
    assert decomposed["hash"]["hex"] != precomposed["hash"]["hex"]
    assert decomposed["dirty"] is True and precomposed["dirty"] is True


def test_crlf_and_lf_line_endings_hash_differently(editor_results):
    """T030.3: CRLF and LF variants of the same visible text MUST hash
    differently -- no newline normalization."""
    crlf = _preview_case(editor_results, "crlf")
    lf = _preview_case(editor_results, "lf")
    assert crlf["hash"]["hex"] != lf["hash"]["hex"]
    assert crlf["dirty"] is True and lf["dirty"] is True


def test_unusual_unicode_and_long_content_edit_and_preview_without_crashing(editor_results):
    """T030.3: a ZWJ emoji sequence, RTL override marks, a lone CR, an
    astral-plane character, and a very long single line all edit and preview
    without crashing, each producing a real sha256 identity and a dirty
    buffer; editing back to the base content cleans the buffer again."""
    for case_id in (
        "zwj_emoji_family", "rtl_override", "lone_cr",
        "astral_plane_char", "very_long_single_line",
    ):
        case = _preview_case(editor_results, case_id)
        assert case["dirty"] is True, case_id
        assert case["hash"]["algorithm"] == "sha256", case_id
        assert len(case["hash"]["hex"]) == 64, case_id
    assert editor_results["unicode"]["__backToBase"]["dirty"] is False


def test_unpaired_utf16_surrogate_edit_is_refused_honestly(editor_results):
    """T030.4: an unpaired UTF-16 surrogate surfaces the state module's
    ContentEncodingError as a stated editor error -- NOT a silent crash, and
    the buffer keeps its previous content exactly."""
    result = editor_results["surrogate"]
    assert result["threw"] is False, (
        "edit() must resolve with a stated error, not reject uncontrolled"
    )
    assert "surrogate" in (result["result"].get("error") or "").lower()
    assert result["after"]["content"] == result["before"]["content"]
    assert result["after"]["dirty"] == result["before"]["dirty"]


# ===========================================================================
# PHASE C fix round (010-doxbench-editor-chat): B1-B4 blockers and the
# S1-S4 should-fix items from the consolidated review. S5 (composition pins
# on staging-workbench.js, which this file does not own) is its own section
# further below.
# ===========================================================================


def test_a_stale_hash_completion_is_dropped_and_never_overwrites_a_newer_edit(
    editor_results,
):
    """B1: settleBufferHash MUST be paired against the LIVE buffer at settle
    time, not the snapshot the edit began from -- otherwise the staleness
    check is a no-op (a snapshot's own generation trivially matches its own
    completion). Edit A begins and is held open on its hash; Edit B is
    issued and settles first; when A's hash finally resolves, B's newer text
    and hash must survive untouched."""
    race = editor_results["generationRace"]
    assert race["afterSecond"]["content"] == "# generation race: second\n"
    assert race["afterSecond"]["dirty"] is True
    assert race["afterFirst"]["content"] == "# generation race: second\n", (
        "the stale first completion must not have reverted the newer edit"
    )
    assert race["afterFirst"]["generation"] == race["afterSecond"]["generation"]
    assert race["afterFirst"]["hashHex"] == race["afterSecond"]["hashHex"]


def test_discard_before_a_pending_edit_settles_wins_over_the_stale_completion(
    editor_results,
):
    """B1: an edit begins and is held open on its hash; Discard runs before
    it settles. When the stale completion finally resolves, the base content
    Discard restored must still be in place."""
    result = editor_results["editThenDiscardBeforeSettle"]
    assert result["afterDiscard"]["content"] == result["baseContent"]
    assert result["afterDiscard"]["dirty"] is False
    assert result["afterEditSettles"]["content"] == result["baseContent"]
    assert result["afterEditSettles"]["dirty"] is False


def test_document_switch_before_a_pending_edit_settles_wins_over_the_stale_completion(
    editor_results,
):
    """B1: an edit begins and is held open on its hash while the buffer is
    already dirty from an earlier, settled edit; a document switch (via the
    guard's Discard) completes before the stale hash resolves. The switched
    document must survive untouched when the stale completion lands."""
    result = editor_results["editThenSwitchBeforeSettle"]
    assert result["blocked"] == {"status": "blocked", "reason": "dirty_document"}
    assert result["discardResolution"]["status"] == "switched"
    assert result["afterSwitch"]["path"] == "ideation/staging/topic-x/second.md"
    assert result["afterSwitch"]["content"] == "# Document B\n"
    assert result["afterRaceSettles"]["path"] == "ideation/staging/topic-x/second.md"
    assert result["afterRaceSettles"]["content"] == "# Document B\n"


def test_a_refused_edit_states_the_refusal_in_the_status_region_not_silently(
    editor_results,
):
    """B2: driven through the REAL `input` event (never controller.edit(...)
    directly). An unpaired surrogate or an over-the-byte-bound paste must
    never just revert the textarea with nothing said -- the buffer's status
    region must name the refusal, and the buffer itself must be unchanged."""
    result = editor_results["inputRefusal"]
    surrogate = result["surrogate"]
    assert surrogate["after"] == surrogate["before"]
    assert "surrogate" in surrogate["status"].lower()

    oversized = result["oversized"]
    assert oversized["after"] == oversized["before"]
    assert "400001" in oversized["status"], "the measured size must be stated"
    assert "400000" in oversized["status"], "the limit must be stated"


def test_typed_outline_text_overrides_the_empty_placeholder_in_preview_and_status(
    editor_results,
):
    """B3: outline_path is null (a scope with no outline yet -- the headline
    US1 case). Typing MUST reach the preview and the status; the canned
    "no outline yet" statement must not survive a single non-empty edit
    (US1 acceptance scenarios 2/3)."""
    result = editor_results["typedOutlineOverridesEmpty"]
    assert "<h1>My new outline</h1>" in result["previewHtml"]
    assert "no outline yet" not in result["previewHtml"].lower()
    assert result["loadState"] == "empty", (
        "load_state itself is preserved by the state module -- only the "
        "RENDERING must stop treating it as blank"
    )
    assert result["dirty"] is True
    assert "unsaved changes" in result["statusText"].lower()


def test_typed_document_text_overrides_the_unavailable_placeholder_but_keeps_the_fact_stated(
    editor_results,
):
    """B3: a Document buffer that loaded `unavailable` (no loadSource
    injected). Typing MUST reach the preview; the "could not load" fact must
    still be stated in the status, ALONGSIDE the dirty fact rather than
    instead of it -- it still governs what a later Save would mean."""
    result = editor_results["typedDocumentOverridesUnavailable"]
    assert "<h1>Recovered content</h1>" in result["previewHtml"]
    assert "could not load" not in result["previewHtml"].lower()
    assert result["loadState"] == "unavailable"
    status = result["statusText"].lower()
    assert "unsaved changes" in status
    assert "unavailable" in status


def test_select_document_refuses_a_path_outside_the_declared_scope(editor_results):
    """B4: FR-007 says "the explicitly selected SCOPED document" -- a path
    neither in context_paths nor editable_paths must be refused outright,
    with no buffer change, and an in-scope path must still work afterward."""
    result = editor_results["outOfScopeSelectDocument"]
    assert result["result"] == {"status": "refused", "reason": "out_of_scope"}
    assert result["after"] == result["before"]
    assert result["inScopeResult"]["status"] == "switched"
    assert result["afterInScope"]["path"] == "ideation/staging/topic-x/second.md"


def test_each_buffer_editor_is_described_by_its_own_preview(editor_results):
    """S1a (CHK020): the textarea and its preview are linked by
    aria-describedby / id, per buffer, so assistive tech can associate the
    live rendering with the control that produces it."""
    result = editor_results["accessibility"]
    assert result["outlinePreviewId"]
    assert result["outlineDescribedBy"] == result["outlinePreviewId"]
    assert result["documentPreviewId"]
    assert result["documentDescribedBy"] == result["documentPreviewId"]
    assert result["outlinePreviewId"] != result["documentPreviewId"]


def test_the_canvas_region_carries_the_exact_product_name(editor_results):
    """S1b (FR-001/SC-009): the mounted region is an accessible `region` whose
    name carries the exact casing `doxBench` and the opened scope --
    never `Doxbench`/`DoxBench`/`doxbench`.

    PIN EVOLUTION (Brett's 2026-08-15 annotation round: "why do we need this
    line? i do not see what it is adding to our UI"). The name used to be
    rendered TWICE — as this region's `aria-label` and again as a visible
    `h2.doxbench-heading` carrying the identical string. The h2 is retired: it
    duplicated the accessible name a screen reader already announces on
    entering the region, and cost a row of a narrow panel to do it. The
    ACCESSIBLE name is what actually names a region, and it is unchanged; the
    two sibling regions (`swb-context`, `doxbench-rail`) have always been
    named exactly this way, with `aria-label` and no heading."""
    result = editor_results["accessibility"]
    assert result["hostRole"] == "region"
    assert result["hostAriaLabel"] == "doxBench · Topic X"
    # the exact casing, wherever the name appears
    for wrong_casing in ("Doxbench", "DoxBench", "doxbench"):
        assert wrong_casing not in result["hostAriaLabel"]
        assert wrong_casing not in result["hostTextContent"]
    # …and it is NOT duplicated as visible text: no heading node survives, and
    # the region's own rendered text does not restate its name
    assert result["headings"] == 0
    assert "doxBench" not in result["hostTextContent"]


def test_save_unavailable_reason_is_visible_text_not_only_a_hover_title(editor_results):
    """S1c: the fixed Save-unavailable reason must be legible without
    hovering -- rendered as real visible text (checked via the mounted
    region's own aggregated textContent, which a `title` attribute would
    never contribute to)."""
    result = editor_results["accessibility"]
    assert editor_results["saveUnavailableReason"] in result["hostTextContent"]


def test_showing_the_guard_moves_focus_to_discard_and_resolving_returns_it(
    editor_results,
):
    """S2 (CHK006/CHK010/CHK011, T036): opening the guard moves focus to its
    Discard choice; resolving it -- by Cancel OR by Discard -- returns focus
    to the Document buffer. The guard never traps focus."""
    result = editor_results["guardFocus"]
    assert "doxbench-guard-discard" in (result["focusedOnShow"]["cls"] or "")
    assert result["focusedAfterCancel"] is True
    assert result["focusedAfterDiscard"] is True


def test_the_canvas_renders_no_document_picker_and_the_route_still_guards(
    editor_results,
):
    """PIN EVOLUTION (Brett's 2026-08-15 annotation round): "we do not need
    this section now that the left panel will let us select the active
    document." The canvas's own picker — S3's "the one way a human reaches
    selectDocument" — is retired; the context region's docs wheel is that way
    now, and it is driven against the real shell in `selection_results`.

    This test therefore asserts two things instead of the control: the picker
    is genuinely GONE (not merely hidden), and every rule it used to carry
    still holds on `selectDocument`, which is where the PR #196 review (F4/F6)
    moved the guard, the refusal sentence and the reconcile — the move that
    made the control removable without losing a rule. A clean switch lands; a
    dirty Document buffer BLOCKS with the guard shown and the buffer untouched;
    Discard resolves it."""
    result = editor_results["selectDocumentRoute"]
    assert result["selects"] == 0, "the canvas renders no <select> at all"
    assert result["pickerNodes"] == 0
    assert result["initialPath"] == "ideation/staging/topic-x/detail.md"

    assert result["afterCleanSwitch"]["result"]["status"] == "switched"
    assert result["afterCleanSwitch"]["path"] == "ideation/staging/topic-x/second.md"

    blocked = result["afterBlockedAttempt"]
    assert blocked["result"] == {"status": "blocked", "reason": "dirty_document"}
    assert blocked["guardHidden"] is False
    assert blocked["documentPath"] == "ideation/staging/topic-x/second.md", (
        "the buffer must stay on the CURRENT document, not the attempted one"
    )

    assert result["afterDiscardResolves"]["path"] == "ideation/staging/topic-x/detail.md"


def test_the_controller_is_fully_inert_after_destroy(editor_results):
    """S4: after destroy(), edit/discard/selectDocument/resolveGuard become
    stated refusals and setActiveBuffer is a no-op; nothing further
    persists."""
    result = editor_results["postDestroyInert"]
    assert result["editResult"]["ok"] is False
    assert result["discardResult"]["ok"] is False
    assert result["selectResult"]["status"] == "refused"
    assert result["guardResult"]["status"] == "refused"
    assert result["tabUnchanged"] is True
    assert result["storageUnchanged"] is True


# ---------------------------------------------------------------------------
# S5: composition pins on staging-workbench.js, from the doxBench side. This
# file does not own staging-workbench.js in this fix round; these are
# READ-ONLY source assertions so a later drift away from the reviewed T037
# shape is caught here regardless. staging-workbench-model.js (NOT this
# file) carries an embedded NUL byte that makes plain `grep` treat it as
# binary -- irrelevant here since staging-workbench.js itself is clean UTF-8,
# confirmed the same way the Phase B report confirmed it.
# ---------------------------------------------------------------------------

STAGING_WORKBENCH_JS = (
    REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views" / "staging-workbench.js"
)


def test_staging_workbench_composes_the_doxbench_canvas_without_new_transport():
    view = STAGING_WORKBENCH_JS.read_text(encoding="utf-8")
    assert 'import { mountDoxBenchCanvas } from "./doxbench-editor.js";' in view
    assert "doxbenchScopeProjection" in view

    # RE-PINNED (PR #207 review, F3): the offering derivation moved OUT of
    # `drawCanvas` into `canvasOffered()`, because the docs tile's verbs must read
    # the SAME answer -- a tile that decided its own capability from whether the
    # canvas controller happened to have mounted yet said "no editing capability"
    # on a console that has one (the docs pane is drawn first). One derivation, two
    # readers; every clause of it is unchanged and still asserted here.
    assert "function canvasOffered() {" in view
    assert (
        "return !!scope && createGateLive(caps) && !sessionSurfaceHidden(caps)"
        in view
    )
    assert "&& !!active?.repository && !!active?.ref;" in view

    # T023 (+T080 client half, 2026-07-30; PIN EVOLUTION T100 P1-A,
    # 2026-08-01): the composition forwards ONLY the seams app.js injects via
    # the `doxbench` option -- loadSource/hash and the governed Save seam --
    # plus ONE pure callback of its own, `onIdentitySettled`, which reads the
    # live controller state and refreshes the rail's proposal currency. It is
    # NOT a transport (the no-fetch needles below still hold) and it carries
    # no request; it exists because the stale transition never reached the
    # rendered DOM without it (the T100 run-2 finding).
    assert 'mountDoxBenchCanvas(canvas, projection, {' in view
    for forwarded in ('title: scope.title', 'loadSource: doxbench?.loadSource',
                      'hash: doxbench?.hash', 'save: doxbench?.save',
                      # PIN EVOLUTION (add-doxbench-editing-phase-a, then
                      # PR #196 review F4): the same pure callback, now a NAMED
                      # function because more than one caller needs it -- a
                      # context-region selection change moves no content
                      # identity, so nothing else would have refreshed the rail
                      # (whose header states the bound buffer) or put the docs
                      # wheel back on the document the canvas ended up holding.
                      'onIdentitySettled: syncContextFromCanvas'):
        assert forwarded in view
    assert 'railController.refreshCurrency(' in view
    # RE-PINNED at contract-v1.34 (add-doxbench-editing-phase-b §13). The rail
    # used to be handed the tile's USABLE documents, so a "no active document"
    # refusal could name one instead of dead-ending -- a refusal that existed
    # only because the v1 envelope made a turn declare ONE active document path.
    # The widened envelope carries the whole loaded set and binds to the SELECTED
    # buffer, so neither the refusal nor the seam that fed it exists; the rail
    # reads its binding off the state authority itself.
    assert 'documentCandidates' not in view
    assert 'activeDocumentPath' not in view
    for needle in ("fetch(", "XMLHttpRequest", "doFetch", "/actions/"):
        assert needle not in view

    # any previous controller is destroyed before a new one mounts, and
    # close() destroys + clears too
    assert view.count("canvasController.destroy()") >= 2
    assert 'canvas.innerHTML = "";' in view

    # PIN EVOLUTION (T104 F1): a fresh open and a session ENDING still redraw
    # the canvas outright -- the ending's working state is deliberately cleared
    # (FR-039), so rebuilding from the surviving main view is correct. A session
    # KEY CHANGE no longer does: `rekeyToSession` and the Save hand-off both go
    # through `adoptSessionRef`, whose `recanvasForKeyChange` keeps a canvas
    # holding unsaved work ALIVE and re-keys it in place (the destructive
    # remount discarded every unsaved byte). The behaviour itself is pinned
    # live at the bottom of this file, by a test that mounts the real shell;
    # these remain structural pins on the composition.
    opened = view.split("function open(kind, id) {", 1)[1].split(
        "\n  }\n\n  return { open, close };", 1)[0]
    assert "drawCanvas();" in opened
    rekey = view.split("function adoptSessionRef(ref, {", 1)[1].split(
        "\n  }\n", 1)[0]
    assert "recanvasForKeyChange(" in rekey
    assert "function rekeyToSession(ref) {" in view
    assert "return adoptSessionRef(ref);" in view
    ending = view.split("onSessionEnded: async () => {", 1)[1].split(
        "\n      },", 1)[0]
    assert "drawCanvas();" in ending
    # the ending tears the canvas down BEFORE the FR-039 clear, so `destroy()`'s
    # own persist cannot re-write the record the clear just removed
    assert ending.index("canvasController.destroy()") < \
        ending.index("clearDoxBenchSession(")
    # the Save hand-off exists and re-keys through the SAME adoption path
    assert "onSaveLanded: (ref) => adoptSessionRef(ref, " in view
    assert "railController.rekey(railScopeKey());" in view

    # the three-region wrapper leaves body's identity intact: drawTab()'s own
    # clear touches only the context region
    assert 'const body = el("div", "swb-body");' in view
    assert "context.append(tabbar, body);" in view
    assert 'body.innerHTML = "";' in view


# ===========================================================================
# T073 (010-doxbench-editor-chat, US4): the ACTIVE Save posture — status, busy,
# rekey, refresh, partial outcome, and focus.
#
# Save is POSTURE-GATED. `mountDoxBenchCanvas` activates its Save arm only when
# a `save` seam is injected; with no seam the control stays disabled and states
# SAVE_UNAVAILABLE_REASON, which is the honest answer for a console that has no
# governed Save wired (FR-040's unreachable-control clause). Every pre-existing
# test in this file mounts WITHOUT a seam and keeps asserting that inert posture
# unchanged — including :1197, :1558 and :1567 — so this block deliberately runs
# its OWN node process over its OWN scenarios rather than extending
# `editor_results`. Two fixtures, two postures, no shared mutation.
#
# The seam's contract is the SaveOutcome doxBench already speaks (data-model 11):
#
#   save({ key, buffers }) -> { status, buffers: [ { kind, status, action, ref,
#                               revision, content_hash, message } ] }
#
# The controller's job is not to decide anything — the ordering, the per-buffer
# action and the partial verdict are the orchestrator's (T077/T078). Its job is
# to report that verdict truthfully and accessibly, advance ONLY the bases that
# committed, keep the refused buffer dirty, and never lie about being busy.
#
# Pins FR-035, FR-038, FR-039 and FR-041. RED until T079.
# ===========================================================================

_SAVE_SEAM_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';
globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');

const { mountDoxBenchCanvas, SAVE_UNAVAILABLE_REASON, unadoptedCommitReason } =
  await import('./doxbench-editor.js');
// #290: the adopting module, so the guard scenario can ask it for the exact
// refusal the canvas caught instead of transcribing one.
const { adoptSavedBase } = await import('./doxbench-state.js');

const OUTLINE_PATH = 'ideation/staging/topic-x/topic-x.md';
const DOC_A = 'ideation/staging/topic-x/detail.md';
const CONTENT = { [OUTLINE_PATH]: '# Outline\n', [DOC_A]: '# Document A\n' };
const SESSION_REF = 'draft/topic-x';

class FakeStorage {
  constructor() { this.values = new Map(); this.removed = []; }
  getItem(k) { return this.values.has(k) ? this.values.get(k) : null; }
  setItem(k, v) { this.values.set(k, String(v)); }
  removeItem(k) { this.removed.push(k); this.values.delete(k); }
}

function projection(overrides = {}) {
  const base = {
    key: { repository: 'fixture-repo', ref: 'main',
           tile_kind: 'staged', tile_id: 'topic-x' },
    title: 'Topic X', source_revision: 'a'.repeat(40),
    outline_path: OUTLINE_PATH,
    editable_paths: [OUTLINE_PATH, DOC_A],
    context_paths: [OUTLINE_PATH, DOC_A],
    active_document_candidates: [DOC_A],
    sections: [],
  };
  const merged = { ...base, ...overrides };
  merged.key = { ...base.key, ...(overrides.key || {}) };
  return merged;
}

const loadSource = async (path) => (path in CONTENT
  ? { content: CONTENT[path], revision: 'rev-' + path, ref: 'main' } : null);

// A deterministic, LOWERCASE-HEX stand-in for a real digest. The shape matters:
// doxbench-state.js validates every identity it writes into working state as a
// lowercase SHA-256 identity, and the gate this seam stands in for can only ever
// report one (gate_routes.execute_first_edit returns
// `doxbench_hash.content_identity`). A fixture emitting 64 arbitrary characters
// would model a server that cannot exist, and would then "prove" the client
// tolerates something no server can send.
function identity(seed) {
  let hex = '';
  for (const ch of String(seed)) hex += ch.charCodeAt(0).toString(16).padStart(2, '0');
  return { algorithm: 'sha256', hex: hex.padEnd(64, '0').slice(0, 64) };
}

// A scripted seam. `verdicts` maps buffer KEY -> outcome row; anything absent is
// reported committed. `gate` (optional) is awaited before answering, which is how
// the BUSY posture is observed mid-flight rather than inferred.
//
// PIN EVOLUTION (add-doxbench-editing-phase-b): the seam request row's identifier
// and the outcome row's identifier are both `key` rather than `kind`. The rename
// is ./doxbench-save.js's -- a row keyed by `kind` would carry a document's PATH
// under the word `kind` once the buffer set widens, which is a false statement
// about the field -- and this fixture models the same wire the real seam does. Not
// a weakening: the same rows, the same verdicts, the same lookups, keyed by the
// identifier the contract now uses.
function seamFor(verdicts, { gate = null, calls = null } = {}) {
  return async (request) => {
    if (calls) calls.push(request);
    if (gate) await gate.promise;
    const rows = request.buffers.map((buffer) => {
      const scripted = verdicts[buffer.key];
      if (scripted) return { key: buffer.key, ...scripted };
      return {
        key: buffer.key, status: 'committed', action: 'edit-document',
        ref: SESSION_REF, revision: 'newrev-' + buffer.key,
        content_hash: identity(buffer.key + 'saved'), message: null,
      };
    });
    const statuses = new Set(rows.map((r) => r.status));
    const status = statuses.has('committed') && statuses.size > 1 ? 'partial'
      : (statuses.has('committed') ? 'committed' : 'refused');
    return { status, buffers: rows };
  };
}

function deferred() {
  let resolve; const promise = new Promise((r) => { resolve = r; });
  return { promise, release: () => resolve() };
}

function describe(node) {
  if (!node) return null;
  return { cls: node.className || null, disabled: !!node.disabled,
           text: node.textContent, busy: node.getAttribute('aria-busy'),
           ariaDisabled: node.getAttribute('aria-disabled'),
           ariaLive: node.getAttribute('aria-live'),
           role: node.getAttribute('role') };
}

async function mount(opts = {}, over = {}) {
  const storage = new FakeStorage();
  const host = new Node('div');
  const controller = mountDoxBenchCanvas(host, projection(over), {
    loadSource, storage, previewDelayMs: 5, ...opts,
  });
  await controller.ready;
  return { controller, host, storage };
}

// ---- both buffers commit -------------------------------------------------
async function bothCommitted() {
  const calls = [];
  // T104 F6-1's save() half: adoptSavedBase moves the buffer identity onto the
  // committed one, and the composition must hear about it exactly like it
  // hears about an edit -- only the calls AFTER the save started are the pin.
  const identitySettled = [];
  const { controller, host, storage } = await mount({
    save: seamFor({}, { calls }),
    onIdentitySettled: (kind, hash) =>
      identitySettled.push({ kind, hex: hash && hash.hex }),
  });
  await controller.edit('outline', '# Outline edited\n');
  await controller.edit('document', '# Document A edited\n');
  const before = controller.state();
  // annotation round 2: the CONTROL carries the state, so its posture is
  // measured on both sides of the save — reachable while something is dirty,
  // unreachable once nothing is
  const saveBtnWhileDirty = describe(controller.elements().save());
  const cancelBtnWhileDirty = describe(controller.elements().cancel());
  const settledBeforeSave = identitySettled.length;
  const outcome = await controller.save();
  const after = controller.state();
  return {
    calls, outcome,
    identityAfterSave: identitySettled.slice(settledBeforeSave),
    beforeDirty: { outline: before.buffers.outline.dirty,
                   document: before.buffers.document.dirty },
    afterBuffers: after.buffers,
    afterKey: after.key,
    status: { outline: describe(controller.elements().status('outline')),
              document: describe(controller.elements().status('document')) },
    // PIN EVOLUTION (add-doxbench-editing-phase-a): ONE Save on the panel, so
    // this is one description, not one per buffer. What it asserts -- the
    // wired posture is enabled and the fixed unavailable reason is GONE
    // rather than restyled -- is unchanged.
    saveBtn: describe(controller.elements().save()),
    saveBtnWhileDirty, cancelBtnWhileDirty,
    hostText: host.textContent,
    storedKeys: [...storage.values.keys()],
    removedKeys: storage.removed,
  };
}

// ---- partial: outline commits, document refuses ---------------------------
async function partial() {
  // T104 F6-1: only the buffer whose base actually ADVANCED may refresh
  // currency -- a notification for the refused document would claim an
  // identity move that never happened.
  const identitySettled = [];
  const { controller, host } = await mount({
    save: seamFor({ document: {
      status: 'refused', action: 'edit-document', ref: null, revision: null,
      content_hash: null, message: 'the document base moved under this buffer' } }),
    onIdentitySettled: (kind, hash) =>
      identitySettled.push({ kind, hex: hash && hash.hex }),
  });
  await controller.edit('outline', '# Outline edited\n');
  await controller.edit('document', '# Document A edited\n');
  const settledBeforeSave = identitySettled.length;
  const outcome = await controller.save();
  const after = controller.state();
  return {
    outcome, afterBuffers: after.buffers,
    identityAfterSave: identitySettled.slice(settledBeforeSave),
    status: { outline: describe(controller.elements().status('outline')),
              document: describe(controller.elements().status('document')) },
    hostText: host.textContent,
    focusedAfter: describe(globalThis.document.activeElement),
  };
}

// ---- busy, observed mid-flight ------------------------------------------
async function busy() {
  const gate = deferred();
  const { controller } = await mount({ save: seamFor({}, { gate }) });
  await controller.edit('outline', '# Outline edited\n');
  const focusedBefore = describe(globalThis.document.activeElement);
  const pending = controller.save();
  const during = {
    save: describe(controller.elements().save()),
    discard: describe(controller.elements().cancel()),
    status: describe(controller.elements().status('outline')),
    focused: describe(globalThis.document.activeElement),
  };
  // a second Save while one is in flight must be refused, not queued
  const reentrant = await controller.save();
  const editDuring = await controller.edit('outline', '# raced\n');
  gate.release();
  const outcome = await pending;
  return {
    focusedBefore, during, reentrant, editDuring, outcome,
    after: { save: describe(controller.elements().save()),
             discard: describe(controller.elements().cancel()),
             status: describe(controller.elements().status('outline')) },
  };
}

// ---- rekey: the session ref the Save landed on ---------------------------
async function rekey() {
  const { controller, storage } = await mount({ save: seamFor({}) });
  const keyBefore = controller.state().key;
  const storedBefore = [...storage.values.keys()];
  await controller.edit('outline', '# Outline edited\n');
  const outcome = await controller.save();
  controller.destroy();
  return {
    keyBefore, storedBefore, outcome,
    keyAfter: controller.state().key,
    storedAfter: [...storage.values.keys()],
    removed: storage.removed,
  };
}

// ---- nothing dirty ------------------------------------------------------
async function nothingDirty() {
  const calls = [];
  const { controller } = await mount({ save: seamFor({}, { calls }) });
  const outcome = await controller.save();
  return { calls, outcome,
           status: describe(controller.elements().status('outline')) };
}

// ---- the guard's Save arm, now reachable ---------------------------------
async function guardSave() {
  const { controller } = await mount({ save: seamFor({}) });
  await controller.edit('document', '# Document A edited\n');
  const blocked = await controller.selectDocument(OUTLINE_PATH);
  const guardText = controller.elements().guard()
    ? controller.elements().guard().textContent : null;
  const resolved = await controller.resolveGuard('save');
  return { blocked, guardText, resolved,
           afterDirty: controller.state().buffers.document.dirty,
           guardHidden: !!controller.elements().guard().hidden };
}

// ---- #290: the guard's sentence is the BUFFER's, never the row's ---------
//
// The third surface of the same defect. The guard asks "why is this buffer
// still dirty?" and answered from the outcome ROW, which for a commit this
// canvas could not adopt reads `committed` -- so it printed "Save did not land
// the Document buffer: saved as edit-document on draft/topic-x." Its BEHAVIOUR
// was already right (it keys off `dirty`, so it stays open); the sentence it
// showed contradicted the buffer's own status region beside it.
async function guardSaveMeetsUnadoptableCommit() {
  const { controller } = await mount({
    save: seamFor({ document: {
      status: 'committed', action: 'edit-document', ref: SESSION_REF,
      revision: 'newrev-document',
      // uppercase hex: a `committed` row the state module refuses to adopt
      content_hash: { algorithm: 'sha256', hex: 'A'.repeat(64) },
      message: null } }),
  });
  await controller.edit('document', '# Document A edited\n');
  const blocked = await controller.selectDocument(OUTLINE_PATH);
  const resolved = await controller.resolveGuard('save');
  const buffer = controller.state().buffers.document;
  // the sentence the two owning modules BUILD for this failure, so the pin
  // compares against them and not against a copy that a reword would orphan
  let adoptDetail = null;
  try {
    adoptSavedBase(buffer, { ref: SESSION_REF, revision: 'newrev-document',
                             content_hash: { algorithm: 'sha256',
                                             hex: 'A'.repeat(64) } });
  } catch (error) {
    adoptDetail = String(error && error.message);
  }
  const read = {
    blocked, resolved,
    expectedReason: unadoptedCommitReason(adoptDetail) + '.',
    adoptDetail,
    // the DATA a landing would have named -- the ref it landed on and the
    // action it performed. A reason carrying either is reporting a commit.
    sessionRef: SESSION_REF,
    committedAction: 'edit-document',
    guardText: String(controller.elements().guard().textContent),
    guardHidden: controller.elements().guard().hidden === true,
    statusDocument: String(controller.elements().status('document').textContent),
    dirty: buffer.dirty,
    content: buffer.content,
    baseHex: buffer.base_hash.hex,
  };
  controller.destroy();   // releases the transient line's own timer
  return read;
}

// ---- W-8: the guard's Save arm survives the remount its own Save triggers --
async function guardSaveIntoRemount() {
  const identitySettled = [];
  let controllerRef = null;
  const { controller, storage } = await mount({
    save: seamFor({}),
    // The shell's recanvas analogue: a Save that lands on a session ref
    // makes staging-workbench destroy this controller and remount a fresh
    // one. The corpse used to keep going -- switchDocument mutated state,
    // PERSISTED under the rekeyed key after destroy() had written its own
    // record, and fired a late onIdentitySettled into the torn-down
    // composition.
    onSaveLanded: async () => { if (controllerRef) controllerRef.destroy(); },
    onIdentitySettled: (kind) => identitySettled.push(kind),
  });
  controllerRef = controller;
  await controller.edit('document', '# Document A edited\n');
  const blocked = await controller.selectDocument(OUTLINE_PATH);
  const settledBeforeResolve = identitySettled.length;
  const resolved = await controller.resolveGuard('save');
  const lastKey = [...storage.values.keys()].pop();
  const record = JSON.parse(storage.values.get(lastKey));
  return {
    blocked: blocked.status,
    resolved,
    // the save's OWN adopted-kind notification is legitimate; a second
    // 'document' fire would be the corpse's switchDocument
    identityAfterResolve: identitySettled.slice(settledBeforeResolve),
    persistedDocumentPath: record.buffers.document.path,
  };
}

// ---- add-doxbench-editing-phase-a: the panel Save, inside the guard -------
//
// The consolidation must not have opened a path AROUND the per-buffer
// staleness guard, so this drives the RENDERED panel button (not `save()`)
// against a seam that refuses one buffer for a moved base.
async function panelSaveMeetsMovedIdentity() {
  const { controller } = await mount({
    save: seamFor({ document: {
      status: 'refused', action: 'edit-document', ref: null, revision: null,
      content_hash: null, message: 'the document base moved under this buffer' } }),
  });
  await controller.edit('outline', '# Outline edited\n');
  await controller.edit('document', '# Document A edited\n');
  const before = controller.state().buffers.document;
  const saveBtn = controller.elements().save();
  for (const fn of (saveBtn.listeners.click || [])) await fn({ target: saveBtn });
  // the click handler drops save()'s promise, so settle the microtask queue
  await new Promise((r) => setTimeout(r, 0));
  const after = controller.state().buffers;
  return {
    // the refused buffer keeps its text, its base, and its dirty flag EXACTLY
    preserved: {
      content: after.document.content === before.content,
      baseHex: after.document.base_hash.hex === before.base_hash.hex,
      baseContent: after.document.base_content === before.base_content,
      dirty: after.document.dirty,
    },
    // …and the buffer that DID land still landed: one button, two answers
    outlineDirty: after.outline.dirty,
    statuses: {
      outline: String(controller.elements().status('outline').textContent),
      document: String(controller.elements().status('document').textContent),
    },
  };
}

// Neither panel control gains authority by being consolidated: no force
// path, no bypass, no second write route.
async function panelControlsGrantNoNewAuthority() {
  const gate = deferred();
  const { controller } = await mount({ save: seamFor({}, { gate }) });
  await controller.edit('outline', '# Outline edited\n');
  const pending = controller.save();
  const during = {
    saveDisabled: controller.elements().save().disabled === true,
    cancelDisabled: controller.elements().cancel().disabled === true,
    secondSave: await controller.save(),
    cancelMidSave: await controller.cancel(),
    editMidSave: await controller.edit('outline', '# raced\n'),
  };
  gate.release();
  await pending;
  // the mid-save Cancel changed nothing: the buffer still holds the bytes the
  // verdict described, and the base advanced only through the answer
  const after = controller.state().buffers.outline;
  return { during, afterDirty: after.dirty, afterContent: after.content };
}

// ---- the unwired posture, in this same harness ---------------------------
async function noSeam() {
  const { controller, host } = await mount({});
  await controller.edit('outline', '# Outline edited\n');
  const attempted = await controller.save();
  return {
    attempted,
    saveBtn: describe(controller.elements().save()),
    hostNamesReason: host.textContent.includes(SAVE_UNAVAILABLE_REASON),
    stillDirty: controller.state().buffers.outline.dirty,
  };
}

console.log(JSON.stringify({
  saveUnavailableReason: SAVE_UNAVAILABLE_REASON,
  bothCommitted: await bothCommitted(),
  partial: await partial(),
  busy: await busy(),
  rekey: await rekey(),
  nothingDirty: await nothingDirty(),
  guardSave: await guardSave(),
  guardUnadoptableCommit: await guardSaveMeetsUnadoptableCommit(),
  guardSaveIntoRemount: await guardSaveIntoRemount(),
  panelSaveMovedIdentity: await panelSaveMeetsMovedIdentity(),
  panelAuthority: await panelControlsGrantNoNewAuthority(),
  noSeam: await noSeam(),
}));
"""


@pytest.fixture(scope="module")
def save_seam_results(tmp_path_factory):
    """A SECOND editor probe, mounting WITH an injected Save seam.

    Deliberately separate from `editor_results`: that fixture's scenarios pin the
    unwired posture and must keep doing so untouched."""
    if NODE is None:
        pytest.skip("node not available for the doxBench Save-seam probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-save-seam")
    (tmp_path / "views").mkdir()
    (tmp_path / "vendor").mkdir()
    shutil.copy(EDITOR_JS, tmp_path / "views" / "doxbench-editor.js")
    shutil.copy(STATE_JS, tmp_path / "views" / "doxbench-state.js")
    shutil.copy(VIEWER_JS, tmp_path / "views" / "viewer.js")
    shutil.copy(VENDOR_MARKDOWN_JS, tmp_path / "vendor" / "markdown-it.min.js")
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "vendor" / "package.json").write_text(
        '{"type": "commonjs"}', encoding="utf-8")
    harness = tmp_path / "views" / "save-seam-harness.mjs"
    harness.write_text(_SAVE_SEAM_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


# ---- the posture gate itself --------------------------------------------

def test_without_a_save_seam_the_control_stays_disabled_and_states_why(
        save_seam_results):
    """The gate, asserted from the ACTIVE harness so the two postures are proven
    to be the same code path: no seam injected means Save is genuinely
    unreachable and says so, and an attempted Save persists nothing."""
    result = save_seam_results["noSeam"]
    assert result["saveBtn"]["disabled"] is True
    assert result["saveBtn"]["ariaDisabled"] == "true"
    assert result["hostNamesReason"] is True
    assert result["attempted"]["status"] == "refused"
    assert result["attempted"]["reason"] == save_seam_results[
        "saveUnavailableReason"]
    assert result["stillDirty"] is True


def test_with_a_save_seam_the_control_becomes_enabled(save_seam_results):
    """The other half: an injected seam makes Save reachable, and the disabled
    posture and its note are gone rather than merely restyled."""
    # PIN EVOLUTION (add-doxbench-editing-phase-a): ONE Save on the panel, so
    # this reads one control rather than one per buffer.
    #
    # PIN EVOLUTION (Brett's 2026-08-18 annotation round 2): reachability is now
    # measured WHILE SOMETHING IS DIRTY, because the control carries the state
    # the retired status text used to spell out — Save is reachable exactly when
    # there is something to save. The seam-gated half this test exists for is
    # unchanged: a seam makes Save reachable at all, and the fixed unavailable
    # reason is GONE rather than restyled.
    button = save_seam_results["bothCommitted"]["saveBtnWhileDirty"]
    assert button["disabled"] is False
    assert button["ariaDisabled"] in (None, "false")
    assert save_seam_results["bothCommitted"]["cancelBtnWhileDirty"][
        "disabled"] is False
    # …and once the save has landed there is nothing left to save, so the
    # control says so by being unreachable rather than by a sentence
    settled = save_seam_results["bothCommitted"]["saveBtn"]
    assert settled["disabled"] is True
    assert settled["ariaDisabled"] == "true"
    assert save_seam_results["saveUnavailableReason"] not in \
        save_seam_results["bothCommitted"]["hostText"]


# ---- what the seam is handed -------------------------------------------

def test_only_dirty_buffers_are_handed_to_the_save_seam(save_seam_results):
    """FR-031: Save persists only CHANGED buffers. The controller decides what
    is dirty; it does not decide order or action.

    PIN EVOLUTION (add-doxbench-editing-phase-b): each seam request row names its
    buffer with `key` rather than `kind`. The field had to be renamed, not merely
    reinterpreted, because a document buffer's key is its PATH once the loaded set
    widens and a path carried under the word `kind` is a false statement about the
    field — the same rename ./doxbench-save.js made to its plan and outcome rows.
    Not a weakening: the identifier is still asserted present, still asserted to
    name both buffers, and every other required field is unchanged."""
    calls = save_seam_results["bothCommitted"]["calls"]
    assert len(calls) == 1, "one explicit Save is one call to the seam"
    keys = sorted(b["key"] for b in calls[0]["buffers"])
    assert keys == ["document", "outline"]
    for buffer in calls[0]["buffers"]:
        assert buffer["dirty"] is True
        assert set(buffer) >= {"key", "path", "content", "base_ref",
                               "base_revision", "base_hash", "dirty", "owned"}
    # …and the whole-canvas Save carries NO scope restriction: `only` is what the
    # tile Save adds, and its absence here is what makes this the broad control.
    assert "only" not in calls[0]


def test_a_save_with_nothing_dirty_never_calls_the_seam(save_seam_results):
    """An explicit Save with nothing to persist reaches no governance action at
    all — it does not open a session to discover it had nothing to do."""
    result = save_seam_results["nothingDirty"]
    assert result["calls"] == []
    assert result["outcome"]["status"] == "unchanged"


# ---- refresh: advance only what committed ------------------------------

def test_a_fully_committed_save_advances_both_bases_and_clears_dirty(
        save_seam_results):
    """FR-038: the controller adopts the identity the SERVER reported, so
    buffers, freshness, and later turns agree with the branch."""
    result = save_seam_results["bothCommitted"]
    assert result["beforeDirty"] == {"outline": True, "document": True}
    # PIN EVOLUTION (add-doxbench-editing-phase-b): outcome rows are keyed by
    # buffer KEY (`row.key`), the rename ./doxbench-save.js made for the reason
    # given above. Same rows, same seven fields, same verdicts.
    rows = {row["key"]: row for row in result["outcome"]["buffers"]}
    for kind in ("outline", "document"):
        buffer = result["afterBuffers"][kind]
        assert buffer["dirty"] is False, kind
        assert buffer["base_hash"] == rows[kind]["content_hash"], kind
        assert buffer["base_revision"] == rows[kind]["revision"], kind
        assert buffer["base_ref"] == rows[kind]["ref"], kind
        assert buffer["base_content"] == buffer["content"], kind


def test_a_partial_save_advances_only_the_committed_base(save_seam_results):
    """FR-035, and the US4 independent test: the first base advances while the
    second stays exactly as dirty as it was."""
    result = save_seam_results["partial"]
    assert result["outcome"]["status"] == "partial"
    outline = result["afterBuffers"]["outline"]
    document = result["afterBuffers"]["document"]
    assert outline["dirty"] is False
    assert outline["base_ref"] == "draft/topic-x"
    assert document["dirty"] is True
    assert document["content"] == "# Document A edited\n"
    assert document["base_revision"] == "rev-" + \
        "ideation/staging/topic-x/detail.md", (
            "a refused buffer's base must not move")


# ---- partial outcome, reported accessibly ------------------------------

def test_a_partial_save_reports_both_verdicts_separately_and_visibly(
        save_seam_results):
    """FR-035's reporting clause: committed and refused are reported SEPARATELY,
    per buffer, as visible text — never as one blended verdict."""
    result = save_seam_results["partial"]
    outline_text = (result["status"]["outline"]["text"] or "").lower()
    document_text = (result["status"]["document"]["text"] or "").lower()
    assert "saved" in outline_text or "committed" in outline_text
    assert "the document base moved under this buffer" in \
        result["status"]["document"]["text"]
    assert "unsaved changes" in document_text
    assert "the document base moved under this buffer" in result["hostText"]


def test_the_per_buffer_status_region_announces_outcomes(save_seam_results):
    """FR-041: an outcome the human cannot hear is not reported. The per-buffer
    status region is a live region, so a Save verdict is announced without
    stealing focus."""
    for scenario in ("bothCommitted", "partial"):
        for kind in ("outline", "document"):
            region = save_seam_results[scenario]["status"][kind]
            assert region is not None, (scenario, kind)
            assert region["ariaLive"] in ("polite", "assertive"), (scenario, kind)


def test_a_partial_save_does_not_steal_focus(save_seam_results):
    """A refusal must not yank the caret out of whatever the human was editing;
    the live region carries the news instead (FR-041)."""
    focused = save_seam_results["partial"]["focusedAfter"]
    assert focused is None or "doxbench-save" not in (focused["cls"] or ""), (
        "focus must not be moved onto the Save control by its own outcome")


# ---- busy ---------------------------------------------------------------

def test_an_in_flight_save_marks_itself_busy_and_disables_its_controls(
        save_seam_results):
    """A Save in flight says so. Leaving Save and Discard live during the
    governed action is how a double-submit becomes two governance actions."""
    during = save_seam_results["busy"]["during"]
    assert during["save"]["disabled"] is True
    assert during["discard"]["disabled"] is True
    assert during["status"]["busy"] == "true"
    assert "saving" in (during["status"]["text"] or "").lower()


def test_a_second_save_while_one_is_in_flight_is_refused_not_queued(
        save_seam_results):
    """A losing race fails loudly rather than silently producing a second
    governance action."""
    reentrant = save_seam_results["busy"]["reentrant"]
    assert reentrant["status"] == "refused"
    assert reentrant["reason"]


def test_an_edit_during_a_save_is_refused_so_the_saved_bytes_stay_truthful(
        save_seam_results):
    """The bytes handed to the seam are the bytes the outcome will describe. An
    edit landing mid-flight would make the returned content identity a lie."""
    assert save_seam_results["busy"]["editDuring"]["ok"] is False
    assert save_seam_results["busy"]["editDuring"]["error"]


def test_the_busy_posture_is_cleared_when_the_save_settles(save_seam_results):
    """The BUSY posture — `aria-busy`, the stated "saving" line, both controls
    withdrawn — is lifted the moment the save settles.

    PIN EVOLUTION (Brett's 2026-08-18 annotation round 2): "withdrawn" and
    "restored" used to be the same fact as "disabled" and "enabled", because
    dirtiness played no part in it. Now it does: this scenario's save COMMITS,
    so once it settles nothing is dirty and the controls are correctly
    unreachable — by the state rule, not by the busy rule. What this test must
    still prove is that the BUSY half cleared, so it reads `aria-busy` and the
    status sentence rather than the disabled flags, which now answer a different
    question."""
    after = save_seam_results["busy"]["after"]
    assert after["status"]["busy"] in (None, "false")
    assert "saving" not in (after["status"]["text"] or "").lower()
    # the controls are unreachable for the HONEST reason — the save landed and
    # left nothing to save — and the in-flight scenario above already proves
    # they were reachable while the buffer was dirty
    assert after["save"]["disabled"] is True
    assert save_seam_results["busy"]["during"]["save"]["disabled"] is True


def test_an_in_flight_save_does_not_move_focus(save_seam_results):
    """FR-041: starting a governed action must not relocate the caret."""
    result = save_seam_results["busy"]
    assert result["during"]["focused"] == result["focusedBefore"]


# ---- rekey -------------------------------------------------------------

def test_a_save_that_lands_on_a_session_ref_rekeys_the_browser_state(
        save_seam_results):
    """FR-038 + FR-039 at the browser-state layer: the buffers now belong to the
    SESSION ref, so the working state is persisted under the session's scope key
    and the pre-session key is not left behind to be restored over it later."""
    result = save_seam_results["rekey"]
    assert result["keyBefore"]["ref"] == "main"
    assert result["keyAfter"]["ref"] == "draft/topic-x", (
        "the controller must follow the resulting session ref")
    assert any("draft" in key for key in result["storedAfter"]), (
        f"no session-keyed working state was persisted: {result['storedAfter']}")
    stale = [k for k in result["storedAfter"] if "main" in k]
    assert stale == [], f"the pre-session key survived the rekey: {stale}"


# ---- add-doxbench-editing-phase-a: the panel controls, inside the guard ---

def test_the_panel_save_still_refuses_a_buffer_whose_identity_moved(
        save_seam_results):
    """add-doxbench-editing-phase-a, "Save meets a moved identity" (task 6.2):
    driven through the RENDERED panel button, so the consolidation is SHOWN not
    to have opened a path around the per-buffer content-identity guard. The
    refused buffer keeps its text, its base and its dirty flag exactly, and the
    buffer that did land still landed — one button, two answers."""
    result = save_seam_results["panelSaveMovedIdentity"]
    assert result["preserved"] == {
        "content": True, "baseHex": True, "baseContent": True, "dirty": True,
    }
    assert result["outlineDirty"] is False
    # the partial outcome stays SEPARATELY readable with one button on screen
    assert "saved as" in result["statuses"]["outline"]
    assert "Save refused" in result["statuses"]["document"]
    assert "base moved" in result["statuses"]["document"]


def test_neither_panel_control_grants_authority_it_did_not_already_have(
        save_seam_results):
    """add-doxbench-editing-phase-a, "A control is asked for authority it does
    not have" (task 6.3): moving a control MUST NOT widen what it may do. While
    a Save is in flight both controls are withdrawn, a second Save is REFUSED
    rather than queued, a concurrent edit is refused rather than landing under
    the verdict, and Cancel gets no force path of its own — the bytes handed
    over stay the bytes the verdict describes."""
    result = save_seam_results["panelAuthority"]
    during = result["during"]
    assert during["saveDisabled"] is True
    assert during["cancelDisabled"] is True
    assert during["secondSave"]["status"] == "refused"
    assert "already in flight" in during["secondSave"]["reason"]
    assert during["cancelMidSave"]["ok"] is False
    assert "already in flight" in during["cancelMidSave"]["error"]
    assert during["editMidSave"]["ok"] is False
    assert "cannot change" in during["editMidSave"]["error"]
    # the in-flight Cancel changed nothing: the save's own answer is what moved
    # the base, and the buffer is clean because it COMMITTED
    assert result["afterDirty"] is False
    assert result["afterContent"] == "# Outline edited\n"


def test_the_view_surface_is_expressed_over_the_buffer_set_not_two_names():
    """add-doxbench-editing-phase-a, "A view surface names a buffer literally"
    (the fifth ADDED requirement): the view tabs, the one Save, the one Cancel
    and the chat binding read the declared buffer enumeration and the
    active-buffer key. Widening the buffer set must be a change to the buffer
    contract and to NOTHING on this surface.

    PIN EVOLUTION (add-doxbench-editing-phase-b), and it is a FINDING against
    Phase A's own task 7.4 ("doxbench-editor.js is verified UNCHANGED in
    structure") rather than a routine re-pin. WHAT MOVED: every assertion below
    used to read `BUFFER_KINDS` as the module's enumeration source. That constant
    is the KIND VOCABULARY — Phase B's state module says so explicitly — and using
    it as the state's KEY LIST is precisely the "literal buffer names baked into
    the view's structure" this requirement refuses: with two documents loaded, a
    loop over `BUFFER_KINDS` walks a set that is not the buffer set.

    WHY IT IS NOT A WEAKENING: each assertion is replaced by the SAME assertion
    over a STRICTER source. `perBuffer(seed)` seeded from a constant becomes
    per-key registration in `ensureBufferDom`, so no fixed-length seed exists to
    assert; the per-buffer loops become loops over `bufferKeysNow()`, which is the
    state's own declared order; the membership refusal becomes `holdsBufferKey`,
    which asks the state instead of a name list and therefore refuses strictly
    MORE (an unloaded key as well as an unknown one); and the label lookup keeps
    its fallback while gaining the collision rule the selector requirement needs.
    The absence assertions — no literal buffer name in the view tabs, no
    "must be outline or document" — are unchanged and still absolute.

    Note what this does NOT claim: the module still names the RESERVED
    `document` key where the reserved-selection-slot machinery lives (the
    document-switch guard, `switchDocument`). That slot is a reserved key in the
    contract, not a member of the buffer enumeration, and naming it is what keeps
    a Phase A session restoring unchanged."""
    source = EDITOR_JS.read_text(encoding="utf-8")
    # the per-buffer structures are registered PER KEY, lazily, and nothing seeds
    # them from a fixed-length name list
    assert "function ensureBufferDom(bufferKey) {" in source
    assert "const perBuffer =" not in source
    assert "BUFFER_KINDS.map(" not in source
    # …and every per-buffer surface is built by looping the STATE's keys
    assert "return state ? bufferKeysInOrder(state) : BUFFER_KINDS;" in source
    assert source.count("for (const key of keys) {") >= 4
    # the view tabs render the ACTIVE buffer; they never enumerate buffers
    view_tab_block = source.split("for (const view of DOXBENCH_VIEW_TABS) {", 1)[1] \
        .split("\n  }\n", 1)[0]
    for literal in ('"outline"', '"document"'):
        assert literal not in view_tab_block, literal
    # Save operates over the declared set; Cancel over the active key
    assert "const changed = scope.filter((key) => state.buffers[key].dirty);" in source
    assert "const held = bufferKeysNow();" in source
    assert "const key = activeBuffer;" in source
    # and the active-buffer refusal asks whether the STATE HOLDS the key
    assert "if (!holdsBufferKey(key)) {" in source
    assert "must name a buffer this canvas holds" in source
    assert "must be outline or document" not in source
    # labels are a lookup with a fallback, so a new key can never be unnamed…
    assert "|| DOXBENCH_BUFFER_LABELS[bufferKey]" in source
    assert "|| String(bufferKey);" in source
    # …and two loaded documents sharing a basename stay distinguishable
    assert "function bufferLabelFor(bufferKey, siblingKeys) {" in source


def test_the_editor_module_exposes_no_force_or_bypass_verb():
    """The source half of the same rule (task 6.3): there is no force-save,
    force-discard, refusal bypass, or second write route anywhere in the
    module — Save reaches exactly one seam, and Cancel reaches none."""
    source = EDITOR_JS.read_text(encoding="utf-8")
    # a word-boundary match, so the prose that EXPLAINS the rule ("enforced
    # structurally", "no force-save") does not stand in for the rule itself
    for verb in (r"forceSave", r"forceDiscard", r"\bforce\s*[:=(]",
                 r"\bbypass\s*[:=(]", r"\boverride\s*[:=(]"):
        assert not re.search(verb, source), verb
    # exactly one call site for the injected Save seam
    assert source.count("saveSeam({") == 1
    # Cancel is the existing per-buffer discard, aimed at the active buffer —
    # not a new primitive and not a whole-canvas reversal
    #
    # PIN EVOLUTION (add-doxbench-editing-phase-b): the per-buffer parameter is
    # spelled `key`, because it names a buffer KEY (a path, for a loaded document)
    # and no longer a two-value kind. Same call, same target, same narrowness.
    assert "const result = await discard(key);" in source
    assert "const key = activeBuffer;" in source
    # …and the tile Save is the SAME seam through the SAME function, narrowed —
    # never a second call site and never a second write route
    assert "await save({ only: key })" in source


# ---- the guard's Save arm ----------------------------------------------

def test_the_guard_save_choice_becomes_reachable_and_resolves_the_switch(
        save_seam_results):
    """The document-switch guard offered Save as a disabled choice naming the
    fixed reason. With a seam it is a real choice, and taking it persists the
    dirty Document and lets the switch proceed."""
    result = save_seam_results["guardSave"]
    assert result["blocked"] == {"status": "blocked", "reason": "dirty_document"}
    assert result["resolved"]["status"] in ("switched", "committed")
    assert result["afterDirty"] is False
    assert result["guardHidden"] is True


def test_the_guard_says_the_commit_was_not_adopted_not_that_it_was_saved(
        save_seam_results):
    """openxFactory #290, the third surface: the guard's sentence must agree
    with the buffer beside it.

    `resolveGuard("save")` asks one question -- why is this buffer STILL dirty?
    -- and answered it from the outcome ROW, which for a commit this canvas
    could not adopt says `committed`, because the server did commit. So the
    guard printed "Save did not land the Document buffer: saved as
    edit-document on draft/topic-x", a sentence that contradicts itself and the
    buffer's own status region in the same breath. Its BEHAVIOUR was never
    wrong -- it keys off `dirty`, so it correctly stays open -- which is exactly
    why the wrong sentence could survive: nothing that moves was broken.

    The reason now comes from the SAME unadopted list the tile verdict reads,
    so the three surfaces (tile note, buffer region, guard) state one fact in
    one wording. A future reader who trusts the row again fails here.
    """
    result = save_seam_results["guardUnadoptableCommit"]
    # preconditions: the guard really opened, and the Save really was taken
    assert result["blocked"] == {"status": "blocked", "reason": "dirty_document"}
    assert result["resolved"]["status"] == "refused", result["resolved"]

    reason = result["resolved"]["reason"]
    # THE SENTENCE, asserted as the one the two owning modules BUILD -- the state
    # module's own refusal for this identity, inside the canvas's exported
    # reason. Not a phrase copied into this file: a copy pins the copy, and a
    # consistent reword of the module would leave it passing while describing
    # nothing.
    assert result["adoptDetail"], "the state module must refuse this identity"
    assert reason == result["expectedReason"], (reason, result["expectedReason"])
    # …and it is the buffer's OWN durable sentence, not a second wording of it
    assert reason.rstrip(".") in result["statusDocument"], (
        reason, result["statusDocument"])
    # …and it names NEITHER thing a landing would have named. Asserted as DATA
    # (the ref, the action) rather than as the committed sentence's wording, so
    # the negative survives a reword too.
    assert result["sessionRef"] not in reason, reason
    assert result["committedAction"] not in reason, reason
    # …and it is what the human actually reads, in the guard that stayed open
    assert result["guardHidden"] is False
    assert reason in result["guardText"], result["guardText"]
    assert result["sessionRef"] not in result["guardText"], result["guardText"]

    # BEHAVIOUR UNCHANGED: the guard stays open over a buffer that kept its
    # text, and no base advanced onto an identity nothing can verify.
    assert result["dirty"] is True
    assert result["content"] == "# Document A edited\n"
    assert result["baseHex"] != "A" * 64, result["baseHex"]


def test_the_guard_no_longer_names_the_unavailable_reason_when_wired(
        save_seam_results):
    """The guard's sentence must stop claiming Save is unwired once it is — while
    still naming both choices, which is what makes it operable."""
    guard_text = (save_seam_results["guardSave"]["guardText"] or "")
    assert save_seam_results["saveUnavailableReason"] not in guard_text
    lowered = guard_text.lower()
    assert "save" in lowered and "discard" in lowered


# ==========================================================================
# T084 + T085 (010-doxbench-editor-chat, US5): deployment postures at the
# canvas, and write-implying-control ABSENCE (FR-040: absent, not disabled).
# Shell-level withholding (hosted / gate-off) is pinned at the source of
# staging-workbench.js -- the canvas is never mounted there, which is the
# strongest form of absence; canvas-level postures run behaviorally below.
# The two TRUE REDS at the bottom pin T090/T091's hypothesized surfaces
# (negotiable-spec rule: adjust these NEW tests only if realization forces it).
# ==========================================================================

_POSTURE_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';

globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');

const { mountDoxBenchCanvas } = await import('./doxbench-editor.js');

const OUTLINE_PATH = 'ideation/staging/topic-x/topic-x.md';
const DOC_A = 'ideation/staging/topic-x/detail.md';

function projection() {
  return {
    key: { repository: 'fixture-repo', ref: 'draft/topic-x', tile_kind: 'staged', tile_id: 'topic-x' },
    title: 'Topic X',
    source_revision: 'a'.repeat(40),
    outline_path: OUTLINE_PATH,
    editable_paths: [OUTLINE_PATH, DOC_A],
    context_paths: [OUTLINE_PATH, DOC_A],
    active_document_candidates: [DOC_A],
    sections: [{
      key: 'folder', label: 'Folder', note: null, inherited: false, owned: true,
      documents: [OUTLINE_PATH, DOC_A].map((p) => ({ id: p, path: p, resolved: true })),
    }],
  };
}

class FakeStorage {
  constructor() { this.values = new Map(); }
  getItem(key) { return this.values.has(key) ? this.values.get(key) : null; }
  setItem(key, value) { this.values.set(key, String(value)); }
  removeItem(key) { this.values.delete(key); }
}

function survey(root) {
  const nodes = root.walk();
  const buttons = nodes.filter((n) => n.tagName === 'BUTTON');
  const byText = (re) => buttons.filter((b) => re.test(b.textContent));
  return {
    textareas: nodes.filter((n) => n.tagName === 'TEXTAREA').length,
    textareasDisabled: nodes.filter((n) => n.tagName === 'TEXTAREA' && n.disabled === true).length,
    selects: nodes.filter((n) => n.tagName === 'SELECT').length,
    // PIN EVOLUTION (add-doxbench-editing-phase-a): the panel's own reversal
    // control is Cancel, aimed at the ACTIVE buffer. `Discard` survives only
    // as the document-switch guard's choice, so it is counted separately --
    // conflating the two would let a lost panel control hide behind the guard.
    cancelButtons: buttons.filter((b) =>
      String(b.className).split(' ').includes('doxbench-cancel')).length,
    guardChoices: byText(/discard/i).length,
    saveButtons: byText(/save/i).length,
    saveDisabled: byText(/save/i).every((b) => b.disabled === true),
    chatControls: nodes.filter((n) =>
      String(n.className).includes('chat')
      || (n.tagName === 'BUTTON' && /\bchat\b|\bmodel\b/i.test(n.textContent))).length,
    applyControls: nodes.filter((n) =>
      n.tagName === 'BUTTON' && /\bapply\b/i.test(n.textContent)).length,
    writeVerbControls: nodes.filter((n) =>
      n.tagName === 'BUTTON'
      && /merge|approve|pull request|open pr|abandon|delete/i.test(n.textContent)).length,
  };
}

const output = {};

{
  // CAPABLE LOCAL (unwired Save): everything loads, both buffers usable.
  const root = new Node('div');
  const controller = mountDoxBenchCanvas(root, projection(), {
    loadSource: async (path) => ({
      content: path === OUTLINE_PATH ? '# Outline\n' : '# Document A\n',
      revision: 'rev-' + path, ref: 'main',
    }),
    storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  output.capable = { ...survey(root), text: root.textContent.slice(0, 4000) };
  controller.destroy();
}

{
  // SOURCE UNAVAILABLE for the document: the outline still loads; the document
  // reports its unavailable state INLINE and the rest of the canvas stays.
  const root = new Node('div');
  const controller = mountDoxBenchCanvas(root, projection(), {
    loadSource: async (path) => (path === OUTLINE_PATH
      ? { content: '# Outline\n', revision: 'rev-o', ref: 'main' }
      : null),
    storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  output.sourceUnavailable = { ...survey(root), text: root.textContent.slice(0, 4000) };
  controller.destroy();
}

{
  // G-1: OUTLINE-ONLY tile — its one editable path IS the outline, so there is
  // no document candidate to pick. The posture is STATED; the canvas stays
  // fully usable and chat still grounds on the outline.
  const root = new Node('div');
  const outlineOnly = {
    ...projection(),
    editable_paths: [OUTLINE_PATH],
    context_paths: [OUTLINE_PATH],
    active_document_candidates: [],
  };
  const controller = mountDoxBenchCanvas(root, outlineOnly, {
    loadSource: async () => ({ content: '# Outline\n', revision: 'rev-o', ref: 'main' }),
    storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  output.outlineOnly = {
    ...survey(root),
    text: root.textContent.slice(0, 4000),
    documentStatus: controller.elements().status('document').textContent,
    documentPath: controller.state().buffers.document.path,
  };
  controller.destroy();
}

console.log(JSON.stringify(output));
"""


@pytest.fixture(scope="module")
def posture_results(tmp_path_factory):
    """A THIRD editor probe: deployment postures (T084/T085), its own process so
    the unwired-posture and Save-seam fixtures keep pinning what they pin."""
    if NODE is None:
        pytest.skip("node not available for the doxBench posture probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-posture")
    (tmp_path / "views").mkdir()
    (tmp_path / "vendor").mkdir()
    shutil.copy(EDITOR_JS, tmp_path / "views" / "doxbench-editor.js")
    shutil.copy(STATE_JS, tmp_path / "views" / "doxbench-state.js")
    shutil.copy(VIEWER_JS, tmp_path / "views" / "viewer.js")
    shutil.copy(VENDOR_MARKDOWN_JS, tmp_path / "vendor" / "markdown-it.min.js")
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "vendor" / "package.json").write_text(
        '{"type": "commonjs"}', encoding="utf-8")
    harness = tmp_path / "views" / "posture-harness.mjs"
    harness.write_text(_POSTURE_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_capable_local_console_offers_both_editors_and_discard(posture_results):
    view = posture_results["capable"]
    assert view["textareas"] >= 1 and view["textareasDisabled"] == 0
    assert view["cancelButtons"] == 1
    # the guard's own Discard choice is the ONLY surviving "discard" control:
    # counted separately (PR #196 review test nit — it used to be measured and
    # never asserted) so a panel control lost to a refactor cannot hide behind
    # the guard's vocabulary
    assert view["guardChoices"] == 1
    # Save is PRESENT but honestly inert without a seam (the pinned posture);
    # presence-with-truthful-reason is the local console's shape, absence is
    # the hosted/gate-off shells' shape (pinned below at the shell source).
    assert view["saveButtons"] >= 1 and view["saveDisabled"] is True


def test_chat_apply_and_write_verbs_are_absent_not_disabled(posture_results):
    # FR-040 + FR-025's absence half: no chat, model, Apply, or write-implying
    # control exists ANYWHERE in the canvas DOM in either posture -- absent
    # rather than disabled. (Chat arrives only with the released catalog and
    # its own wave; nothing may suggest it earlier.)
    for posture in ("capable", "sourceUnavailable"):
        view = posture_results[posture]
        assert view["chatControls"] == 0, posture
        assert view["applyControls"] == 0, posture
        assert view["writeVerbControls"] == 0, posture


def test_an_unavailable_source_is_reported_inline_with_context_retained(
        posture_results):
    view = posture_results["sourceUnavailable"]
    assert "source unavailable" in view["text"]
    # the outline buffer still loaded and stays usable; the rest of the canvas
    # survives the unavailable document rather than vanishing with it
    assert view["textareas"] >= 1 and view["textareasDisabled"] == 0
    assert view["cancelButtons"] == 1
    # PIN EVOLUTION (Brett's 2026-08-15 annotation round): this used to assert
    # `selects >= 1` for the canvas's own document picker. That control is
    # retired — the context region's docs wheel is the selection route — so the
    # canvas renders no <select> at all, and the pin flips to say so.
    assert view["selects"] == 0


def test_an_outline_only_tile_states_that_posture_in_the_buffers_own_status(
        posture_results):
    """G-1 (PR #63 re-verification): on 16 of 21 real staged topics the tile's
    ONLY editable path is its own primary fragment, which this canvas loads as
    the OUTLINE and which T104 F2 therefore does not offer as a DOCUMENT.

    PIN EVOLUTION (Brett's 2026-08-15 annotation round): the posture used to be
    stated TWICE — on the picker's own label and in the Document buffer's
    status. The picker is retired, so the status carries it alone, which is
    where it belonged: it is a fact about the BUFFER, not about a control. The
    canvas stays fully usable, because chat grounds on the outline alone
    (`active_document_path: null`)."""
    view = posture_results["outlineOnly"]
    # the retired control leaves nothing empty behind
    assert view["selects"] == 0
    # the Document buffer's own status says the posture, instead of the
    # misleading "no document selected" (there is none to select)
    assert "no document selected" not in view["documentStatus"]
    assert "only editable document" in view["documentStatus"]
    assert view["documentPath"] is None
    # nothing is withheld: both buffers, Save/Discard and the preview remain
    assert view["textareas"] == 2 and view["textareasDisabled"] == 0
    assert view["cancelButtons"] == 1 and view["saveButtons"] >= 1


def test_gate_off_and_hidden_surfaces_withhold_the_canvas_at_the_shell():
    # Hosted/gate-off absence is enforced one level up: the shell never mounts
    # the canvas at all (the strongest "absent, not disabled").
    source = (EDITOR_JS.parent / "staging-workbench.js").read_text(encoding="utf-8")
    assert "createGateLive(caps)" in source
    assert "sessionSurfaceHidden(caps)" in source
    assert "const offered = canvasOffered();" in source
    assert "canvas.hidden = !offered" in source
    assert "if (!offered) return;" in source
    # …and the docs tile's verbs read the SAME predicate, so the two surfaces
    # cannot disagree about whether this console can edit (PR #207 review, F3).
    assert "if (!canvasOffered()) {" in source


def test_the_shell_derives_one_explicit_presentation_posture():
    # T090 (TRUE RED until realized): one derivation names the posture the
    # presentation is in, so control omission is a stated decision rather than
    # a scatter of independent conditionals.
    source = (EDITOR_JS.parent / "staging-workbench-model.js").read_text(encoding="utf-8")
    assert "export function presentationPosture(" in source


def test_the_shell_explains_unavailable_postures_inline():
    # T091 (TRUE RED until realized): empty-catalog / hosted / gate-off /
    # source-unavailable get an inline explanation that RETAINS context.
    source = (EDITOR_JS.parent / "staging-workbench.js").read_text(encoding="utf-8")
    assert "swb-posture-note" in source


# ==========================================================================
# T104 F1 (PR #63 second review): THE POST-SAVE SESSION RE-KEY, live
#
# Every pin above this line either drives the canvas controller directly or
# reads staging-workbench.js as TEXT. The F1 family is precisely what neither
# can see: a Save opens a branch session server-side, and only the CANVAS
# re-keys itself. The shell's `active`/source base, the session bar and the
# chat rail's `scopeKey` (captured by value at mount; `railController.rekey`
# had no caller anywhere in the bundle) all stayed on the pre-session ref, so
# from the first Save onward every chat turn carried a scope the buffers had
# left. `test_a_save_that_lands_on_a_session_ref_rekeys_the_browser_state`
# (:2139 at the reviewed head) proves the canvas half and passes today for one
# reason: it mounts NO chat rail.
#
# So this section mounts the REAL shell -- `mountStagingWorkbench` over the
# whole views bundle -- in the DOM shim, and drives it the way an operator
# does: type, Save, then chat. Two assertions the source pins cannot make:
#
#   (a) the turn request the rail sends AFTER the Save carries the SESSION
#       ref, and
#   (b) an unsaved buffer still holds its text once the re-key has run --
#       the remount path used to destroy and rebuild the canvas, dropping
#       every unsaved byte with no dirty check, guard or warning.
# ==========================================================================

_SHELL_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';

globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');
globalThis.window = { location: { href: 'http://localhost/' } };

const { mountStagingWorkbench } = await import('./staging-workbench.js');

const OUTLINE_PATH = 'ideation/staging/topic-x/topic-x.md';
const DOC_PATH = 'ideation/staging/topic-x/detail.md';
const SESSION_REF = 'draft/topic-x';

const snapshot = {
  repository: 'fixture-repo',
  generation: { source_revision: '1'.repeat(40) },
  documents: [
    { id: OUTLINE_PATH, path: OUTLINE_PATH, topics: ['alpha'],
      destinations: { staged_topics: ['topic-x'] } },
    { id: DOC_PATH, path: DOC_PATH, topics: ['alpha'],
      destinations: { staged_topics: ['topic-x'] } },
  ],
  clusters: [], possibles: [],
  staged_topics: [{ staging_id: 'topic-x', files: [OUTLINE_PATH, DOC_PATH] }],
};

const caps = { actions: { gate: true, session: true }, actor: 'brett' };

const chatRequests = [];
const saveRequests = [];

function fire(node, type) {
  const listeners = (node.listeners && node.listeners[type]) || [];
  // A real event carries both, and the docs tile's own action handlers call
  // `stopPropagation` (a click on an action belongs to the action, not the tile).
  return Promise.all(listeners.map((fn) => fn({
    target: node, stopPropagation() {}, preventDefault() {} })));
}

const settle = () => new Promise((r) => setTimeout(r, 0));
async function until(predicate, label) {
  for (let i = 0; i < 400; i += 1) {
    if (predicate()) return;
    await settle();
  }
  throw new Error('timed out waiting for ' + label);
}

class FakeStorage {
  constructor() { this.values = new Map(); }
  getItem(k) { return this.values.has(k) ? this.values.get(k) : null; }
  setItem(k, v) { this.values.set(k, String(v)); }
  removeItem(k) { this.values.delete(k); }
}
const storage = new FakeStorage();

const container = document.createElement('div');
const doxbench = {
  // PRODUCTION SHAPE (wave re-review, R-12 machinery): app.js's source
  // loader returns {content, ref} and NOTHING ELSE — no per-file revision
  // exists on the wire. This fake used to return one, exercising a dead arm
  // of baseRevisionOf and masking that a real client's base_revision is the
  // PROJECTION's source_revision (the W-4 finding's whole mechanism).
  loadSource: async (path) => ({
    content: '# ' + path + '\n\nloaded from main.\n', ref: 'main' }),
  // the governed Save: the OUTLINE lands on a freshly opened session branch,
  // the DOCUMENT is refused, so its unsaved text is exactly what must survive
  // the re-key that follows
  save: async (request) => {
    saveRequests.push(request);
    return {
      status: 'committed',
      buffers: request.buffers.map((row) => (row.key === 'outline'
        ? { key: 'outline', status: 'committed', action: 'edit-document',
            ref: SESSION_REF, revision: '2'.repeat(40),
            content_hash: row.current_hash, message: null }
        : { key: 'document', status: 'refused', action: 'edit-document',
            ref: null, revision: null, content_hash: null,
            message: 'not this time' })),
    };
  },
  storage,
  catalog: async () => ({
    schema_version: 1, kind: 'workbench-model-catalog',
    models: [{ model_id: 'model-a', label: 'Approved model', available: true,
               provider_class: 'on-tenant', input_limit_bytes: 800000,
               output_limit_bytes: 900000, data_handling: 'tenant boundary' }],
  }),
  chatTurn: async (request) => {
    chatRequests.push(request);
    return { ok: false, status: 502, payload: {
      schema_version: 1, kind: 'workbench-chat-turn-failure',
      client_turn_id: request.client_turn_id, error: 'model_failed',
      message: 'the model request failed' } };
  },
};

const workbench = mountStagingWorkbench(container, snapshot, {
  caps,
  fetcher: async () => ({ ok: false }),
  active: { repository: 'fixture-repo', ref: 'main' },
  index: { entries: [] },
  doxbench,
  sourceBase: '/source/',
  edit: null,
  // the shell's EXISTING re-key seam: app.js fetches the session's own view
  // of the world and hands it back
  onSessionRekey: async (ref) => ({
    snapshot, active: { repository: 'fixture-repo', ref },
    index: { entries: [] }, sourceBase: '/source/' + ref + '/' }),
  onSessionEnded: async () => null,
  onScopeOpened: () => null,
});

workbench.open('staged', 'topic-x');

const byClass = (cls) => container.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));
const one = (cls) => byClass(cls)[0] || null;

await until(() => byClass('doxbench-textarea').length === 2,
            'the canvas textareas');
const [outlineArea, documentArea] = byClass('doxbench-textarea');
await until(() => outlineArea.value.includes(OUTLINE_PATH), 'the loaded outline');

// type in BOTH buffers, and let each identity settle
outlineArea.value = '# outline edited\n';
await fire(outlineArea, 'input');
documentArea.value = '# thirty minutes of unsaved document work\n';
await fire(documentArea, 'input');
await until(() => (one('doxbench-status').textContent || '').includes('unsaved'),
            'the dirty status');
for (let i = 0; i < 20; i += 1) await settle();

const out = { railBefore: byClass('doxchat-composer').length };

// SAVE. The seam opens the session and answers with its ref.
const saveButton = byClass('doxbench-save')[0];
await fire(saveButton, 'click');
for (let i = 0; i < 60; i += 1) await settle();

out.saveSeamCalled = saveRequests.length;
out.saveKeyRef = saveRequests.length ? saveRequests[0].key.ref : null;

// (b) the unsaved DOCUMENT buffer survived the re-key
const areasAfter = byClass('doxbench-textarea');
out.textareaCount = areasAfter.length;
out.documentTextAfter = areasAfter.length === 2 ? areasAfter[1].value : null;

// the shell itself followed the session: the posture line and the source base
out.postureText = (one('swb-posture') || {}).textContent || '';

// (a) the NEXT turn carries the session ref. The operator picks a model and
// sends; the rail must still be able to (a re-key that left it with an empty
// selector would be a different dead end).
const selector = one('doxchat-model');
const composer = one('doxchat-composer');
out.railAfter = composer ? 1 : 0;
if (selector && composer) {
  await until(() => selector.children.length > 1, 'the adopted catalog');
  selector.value = 'model-a';
  await fire(selector, 'change');
  composer.value = 'what should we close next?';
  await fire(composer, 'input');
  await fire(one('doxchat-send'), 'click');
  for (let i = 0; i < 40; i += 1) await settle();
}
out.turnCount = chatRequests.length;
out.turnScopeRef = chatRequests.length ? chatRequests[0].scope.ref : null;
out.turnOutlineBaseRef = chatRequests.length
  ? chatRequests[0].buffers[0].base_ref : null;
out.turnDocumentBaseRef = chatRequests.length
  ? chatRequests[0].buffers[1].base_ref : null;
// the value a REAL client declares: the projection's source_revision, since
// the production loader carries no per-file revision (W-4's mechanism)
out.turnDocumentBaseRevision = chatRequests.length
  ? chatRequests[0].buffers[1].base_revision : null;
out.turnFailureNote = (one('doxchat-failure') || {}).textContent || '';

// ---- R-1, the restore half (F1 P1 staging-workbench.js:787 / :898) ----
// Type a chat subject, close the overlay (which persists buffers AND the
// rail's companion blob in ONE record), then reopen the tile on a plane whose
// model catalog is EMPTY -- the documented editor-only posture, and the one
// where the approved-model count never changes.
const subjectInput = one('doxchat-subject');
subjectInput.value = 'the acceptance boundary';
await fire(subjectInput, 'input');
const composerAgain = one('doxchat-composer');
composerAgain.value = 'and a half-written question';
await fire(composerAgain, 'input');
for (let i = 0; i < 20; i += 1) await settle();
workbench.close();
for (let i = 0; i < 20; i += 1) await settle();
out.persistedKeys = [...storage.values.keys()];

const reopened = document.createElement('div');
const emptyCatalogDoxbench = { ...doxbench,
  catalog: async () => ({ schema_version: 1,
                          kind: 'workbench-model-catalog', models: [] }) };
// The second mount is ALSO the FR-039 stage (T104 F7-7): its roster
// advertises the session ref (a live session is an ordinary roster row,
// FR-014/FR-045), its fetcher can answer the abandon verb, and its
// onSessionEnded hands back the surviving main view — the three things a
// session ENDING through the mounted shell needs.
const ABANDON_RESULT = {
  ok: true, ref: SESSION_REF, reason: 'the spike answered its question',
  torn_down: ['worktree', 'registry-entry', 'notebook'], branch_retained: true,
  record: 'ideation/dashboard/gate-records/draft-topic-x/abandon.yaml',
};
const second = mountStagingWorkbench(reopened, snapshot, {
  caps,
  fetcher: async () => ({ status: 200, json: async () => ABANDON_RESULT }),
  active: { repository: 'fixture-repo', ref: SESSION_REF },
  index: { entries: [{ repository: 'fixture-repo', ref: SESSION_REF }] },
  doxbench: emptyCatalogDoxbench,
  sourceBase: '/source/' + SESSION_REF + '/',
  edit: null,
  onSessionRekey: async () => null,
  // the surviving main view; the refetched roster still advertises the ended
  // ref for a while (sessionPosture's own "session ended" label documents
  // exactly this window)
  onSessionEnded: async () => ({
    snapshot, active: { repository: 'fixture-repo', ref: 'main' },
    index: { entries: [{ repository: 'fixture-repo', ref: SESSION_REF }] },
    sourceBase: '/source/' }),
  onScopeOpened: () => null,
});
second.open('staged', 'topic-x');
const inSecond = (cls) => (reopened.walk().filter(
  (n) => String(n.className).split(' ').includes(cls))[0] || null);
await until(() => inSecond('doxchat-subject') !== null, 'the reopened rail');
for (let i = 0; i < 60; i += 1) await settle();
out.restoredSubject = (inSecond('doxchat-subject') || {}).value || '';
out.restoredComposer = (inSecond('doxchat-composer') || {}).value || '';
out.restoredModelOptions = (inSecond('doxchat-model') || { children: [] })
  .children.length;
out.restoredDocumentText = (reopened.walk().filter(
  (n) => String(n.className).split(' ').includes('doxbench-textarea'))[1]
  || {}).value || '';

// ---- T104 F7-7: a session END through the mounted shell clears the
// FakeStorage record (FR-039). The shell's onSessionEnded handler calls
// clearDoxBenchSession at the one moment the dying ref is still known; with
// the seam unthreaded the clear silently targeted ambient
// window.sessionStorage — absent here, exactly as absent as it is on any
// non-window plane — and the ended session's record survived. ----
const { scopeStorageKey } = await import('./doxbench-state.js');
const SESSION_RECORD_KEY = scopeStorageKey({
  repository: 'fixture-repo', ref: SESSION_REF,
  tile_kind: 'staged', tile_id: 'topic-x' });
out.sessionKeyedBeforeEnd = [...storage.values.keys()]
  .filter((k) => k === SESSION_RECORD_KEY).length;

const abandonBtn = inSecond('swb-sessionbtn')
  ? reopened.walk().filter((n) =>
      String(n.className).split(' ').includes('swb-sessionbtn'))
      .find((b) => b.textContent.toLowerCase().includes('abandon'))
  : null;
out.abandonOffered = Boolean(abandonBtn && abandonBtn.disabled !== true);
if (abandonBtn) {
  await fire(abandonBtn, 'click');
  const reason = reopened.walk().find(
    (n) => n.attributes && n.attributes['aria-label'] === 'Reason');
  if (reason) reason.value = ABANDON_RESULT.reason;
  const submit = reopened.walk().filter((n) =>
    String(n.className).split(' ').includes('cbtn'))
    .find((b) => b.textContent === 'abandon-session');
  out.abandonSubmitFound = Boolean(submit);
  if (submit) await fire(submit, 'click');
  for (let i = 0; i < 60; i += 1) await settle();
}
out.endingReported = reopened.walk().some((n) =>
  String(n.className).split(' ').includes('swb-clanded'));
out.sessionKeyedAfterEnd = [...storage.values.keys()]
  .filter((k) => k === SESSION_RECORD_KEY).length;
out.storageKeysAfterEnd = [...storage.values.keys()];

// ---- W-13: the shell's posture note follows the CATALOG FAILURE, not only
// the approved-model count. In the shipped zero-adapter posture the count is
// 0 before and after a failed fetch, so the failure half of the rail
// onState comparison is the ONLY thing that re-renders the shell's note --
// drop it and the shell claims "no approved model is configured" over a
// stale console token forever, the F10-1 bug shape one surface up. ----
const third = document.createElement('div');
const staleTokenDoxbench = { ...doxbench,
  catalog: async () => ({ failed: 'console_required' }) };
const thirdMount = mountStagingWorkbench(third, snapshot, {
  caps, fetcher: async () => ({ ok: false }),
  active: { repository: 'fixture-repo', ref: 'main' },
  index: { entries: [] }, doxbench: staleTokenDoxbench,
  sourceBase: '/source/', edit: null,
  onSessionRekey: async () => null, onSessionEnded: async () => null,
  onScopeOpened: () => null,
});
thirdMount.open('staged', 'topic-x');
const inThird = (cls) => (third.walk().filter(
  (n) => String(n.className).split(' ').includes(cls))[0] || null);
await until(() => inThird('swb-posture-note') !== null, 'the third posture note');
for (let i = 0; i < 60; i += 1) await settle();
// PIN EVOLUTION (Brett's 2026-08-18 annotation round 2): a CHAT rung's sentence
// no longer stands in the shell's posture note -- it is the send button's stated
// reason, inside the rail, where the human is trying to act. Both halves are
// probed: the standing line is empty, and the sentence arrived where it went.
out.staleTokenPosture = (inThird('swb-posture-note') || {}).textContent || '';
out.staleTokenSendTitle = (inThird('doxchat-send') || {}).title || '';
out.staleTokenSendDescribedBy =
  (inThird('doxchat-send') || { getAttribute: () => null })
    .getAttribute('aria-describedby') || '';
out.staleTokenRailNote = (inThird('doxchat-unavailable') || {}).textContent || '';
out.staleTokenRailNoteSrOnly = String(
  (inThird('doxchat-unavailable') || {}).className || '').includes('doxchat-sronly');

console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def shell_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench shell probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-shell")
    views = tmp_path / "views"
    shutil.copytree(EDITOR_JS.parent, views)
    shutil.copytree(EDITOR_JS.parent.parent / "vendor", tmp_path / "vendor")
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "vendor" / "package.json").write_text(
        '{"type": "commonjs"}', encoding="utf-8")
    harness = views / "shell-harness.mjs"
    harness.write_text(_SHELL_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_shell_really_composes_a_canvas_and_a_rail(shell_results):
    """The harness is worth nothing if the composition it drives is not the
    real one: both regions must actually be mounted before the Save."""
    assert shell_results["railBefore"] == 1
    assert shell_results["saveSeamCalled"] == 1
    assert shell_results["saveKeyRef"] == "main"


def test_a_save_that_opens_a_session_rekeys_the_chat_rail_not_only_the_canvas(
        shell_results):
    """F1(a): the rail's NEXT turn carries the session ref. Before the fix the
    rail's scopeKey was the object literal captured at mount, so this request
    named `main` while the buffers it carried were based on the session
    branch -- a disagreement the server's own FR-015 binding check refuses,
    which is why every chat turn after the first Save was dead."""
    assert shell_results["turnCount"] == 1, (
        f"the rail sent no turn after the Save: "
        f"{shell_results['turnFailureNote']!r}")
    assert shell_results["turnScopeRef"] == "draft/topic-x"
    # and the buffer the Save landed agrees with it
    assert shell_results["turnOutlineBaseRef"] == "draft/topic-x"


def test_an_unsaved_buffer_survives_the_post_save_rekey(shell_results):
    """F1(b): the re-key must not be a destroy-and-remount. It was: the
    session re-key called `drawCanvas()`, which destroyed the controller and
    rebuilt it from `/source`, silently discarding every unsaved byte with no
    dirty check, no guard and no warning."""
    assert shell_results["textareaCount"] == 2
    assert shell_results["documentTextAfter"] == \
        "# thirty minutes of unsaved document work\n"


def test_the_post_save_turn_still_declares_the_pre_session_base_for_unsaved_buffers(
        shell_results):
    """R-12 CLOSED (reviewer ruling 2026-08-02) -- and this pin RE-PURPOSED,
    never deleted: it is now the record that PROVENANCE IS PRESERVED.

    `rekeyDoxBenchState` (doxbench-state.js) deliberately keeps both buffers
    exactly as they are, and
    `test_rekeying_moves_the_scope_key_and_keeps_both_buffers_exactly`
    (test_doxbench_state.py:454) pins that byte-for-byte, including
    `sameDocumentObject is True`. So a buffer the Save did NOT land still
    declares `base_ref` = the pre-session ref while the scope names the
    session -- and that stays TRUE, because `base_ref` means "where these
    base bytes came from" and must never be rewritten to something the bytes
    did not come from. What the ruling changed is the COMPARISON:
    `doxbench_turns._require_buffer_binding` now accepts this pairing when
    the buffer names the ref the session branched from at the session's own
    recorded base revision and the session has not diverged past that base
    for this document (turn-succeeds guard:
    test_doxbench_routes.py::test_the_post_partial_save_turn_grounds_the_unlanded_buffer_on_the_session_base;
    divergence guard:
    ::test_a_pre_session_buffer_is_refused_once_the_session_moved_the_document)."""
    assert shell_results["turnDocumentBaseRef"] == "main"
    assert shell_results["turnScopeRef"] == "draft/topic-x"
    # and the revision a REAL client declares is the PROJECTION's
    # source_revision — the production loader returns no per-file revision,
    # which is exactly why W-4 records the serving snapshot's revision as an
    # accepted alias at open (this harness used to fake a loader revision,
    # masking the whole mechanism)
    assert shell_results["turnDocumentBaseRevision"] == "1" * 40


def test_the_restored_chat_state_is_applied_on_a_plane_with_no_approved_models(
        shell_results):
    """F1's R-1 half (P1 staging-workbench.js:787 and :898). The restored chat
    working state was applied ONLY from inside the rail's
    `if (count !== approvedModelCount)` branch, so on the shipped zero-adapter
    posture -- an EMPTY catalog, where that count never changes -- the subject,
    model, composer, transcript and proposals were silently dropped on every
    remount. The canvas made it worse by handing the blob over BEFORE
    `state = restored` was assigned, so the one call that did fire always read a
    null canvas state and bailed.

    This reopens the tile through the real shell on an empty-catalog plane and
    asserts the operator's own words came back."""
    assert shell_results["persistedKeys"], "nothing was persisted to reopen from"
    assert shell_results["restoredSubject"] == "the acceptance boundary"
    assert shell_results["restoredComposer"] == "and a half-written question"
    # the empty catalog really is empty: only the placeholder option renders,
    # so the count-changed branch could not have carried this
    assert shell_results["restoredModelOptions"] == 1


def test_the_shell_itself_follows_the_session_after_a_save(shell_results):
    """The same re-key reaches the SHELL: the posture line stops describing a
    view that is now reading the session branch as if it were main."""
    assert "draft/topic-x" in shell_results["postureText"] or \
        "draft" in shell_results["postureText"].lower()


def test_a_session_end_through_the_mounted_shell_clears_the_working_record(
        shell_results):
    """T104 F7-7 (FR-039): the shell's onSessionEnded handler called
    `clearDoxBenchSession({...})` with ONE argument, silently targeting
    ambient window.sessionStorage instead of the injected `doxbench.storage`
    seam — so under any injected storage (this harness's FakeStorage; the
    editor threads the seam correctly at its own re-key clear,
    doxbench-editor.js) the ended session's record was never removed. The
    abandon here runs through the REAL mounted shell: the affordance row, the
    gate verb, the onSessionEnded rebind — and the session-keyed record must
    be gone afterwards."""
    assert shell_results["sessionKeyedBeforeEnd"] >= 1, (
        "precondition: the session's working record was persisted")
    assert shell_results["abandonOffered"] is True, (
        "precondition: the mounted shell offered the abandon verb")
    assert shell_results["abandonSubmitFound"] is True
    assert shell_results["endingReported"] is True, (
        "precondition: the ending really landed and was reported")
    assert shell_results["sessionKeyedAfterEnd"] == 0, (
        f"the ended session's record survived in the injected storage: "
        f"{shell_results['storageKeysAfterEnd']}")


# ==========================================================================
# T104 F6 wave (doxBench review, 2026-08-04) + F10-3's client half.
#
# F6-1: onIdentitySettled fired only from edit(); discard(), switchDocument()
#       and save()'s adoptSavedBase all move a buffer's identity and told
#       nobody, so the rail's proposal cards kept 'current' + enabled Apply
#       against text they no longer matched.
# F6-2: every editing entry point dereferenced `state.buffers` while the
#       textareas were mounted ENABLED before initialLoad() resolved --
#       keystrokes during the source fetch threw unhandled TypeErrors and
#       were then silently overwritten (CHK016/CHK019).
# F6-6: a hashing failure inside initialLoad() (an oversized document) had no
#       consumer, so `state` stayed null forever and the canvas rendered as a
#       silently broken editor.
# F10-3: the editor read buffer content back from the <textarea>, whose API
#       value is LF-normalized, so a CRLF document could never round-trip
#       byte-exactly (FR-045) and syncBufferDom's comparison never settled.
# ==========================================================================


def test_discard_refreshes_proposal_currency_via_identity_settled(editor_results):
    """F6-1: Discard moves current_hash back to the base identity, and the
    composition is told with the post-transition hash."""
    result = editor_results["identitySettled"]
    assert len(result["afterEdit"]) == 1, "the edit() wire is the baseline"
    assert result["afterEdit"][0]["kind"] == "document"
    assert len(result["afterDiscard"]) == 2, (
        "discard() must notify onIdentitySettled")
    assert result["afterDiscard"][-1] == {
        "kind": "document", "hex": result["baseHex"]}


def test_a_document_switch_refreshes_proposal_currency_via_identity_settled(
        editor_results):
    """F6-1: a document switch replaces the whole Document buffer; the
    composition hears the NEW buffer's settled identity."""
    result = editor_results["identitySettled"]
    assert len(result["afterSwitch"]) == 3, (
        "switchDocument() must notify onIdentitySettled")
    assert result["afterSwitch"][-1] == {
        "kind": "document", "hex": result["switchedHex"]}


def test_a_landed_save_notifies_identity_settled_with_the_adopted_hashes(
        save_seam_results):
    """F6-1's save() half: after adoptSavedBase lands, the composition hears
    each committed buffer's POST-adoption identity -- the server-reported one,
    which is exactly what the rendered proposal cards must re-score against."""
    result = save_seam_results["bothCommitted"]
    settled = {row["kind"]: row["hex"] for row in result["identityAfterSave"]}
    for kind in ("outline", "document"):
        assert settled.get(kind) == \
            result["afterBuffers"][kind]["current_hash"]["hex"], kind


def test_a_partial_save_notifies_identity_settled_only_for_the_landed_buffer(
        save_seam_results):
    """F6-1: the refused buffer's identity did NOT move, so no notification may
    claim it did."""
    result = save_seam_results["partial"]
    kinds = [row["kind"] for row in result["identityAfterSave"]]
    assert kinds == ["outline"]
    assert result["identityAfterSave"][0]["hex"] == \
        result["afterBuffers"]["outline"]["current_hash"]["hex"]


def test_input_during_the_initial_load_neither_throws_nor_vanishes_silently(
        editor_results):
    """F6-2 (CHK016/CHK019): a keystroke arriving before initialLoad resolves
    must not throw an unhandled TypeError, and must not be silently discarded
    -- the surfaces are disabled with a stated loading line, and a keystroke
    that reaches the listener anyway gets a visible refusal."""
    result = editor_results["inputDuringLoad"]
    assert result["threw"] is None, (
        f"a keystroke during load threw: {result['threw']!r}")
    assert result["duringDisabled"] == {"outline": True, "document": True}
    assert "loading" in result["duringStatus"].lower()
    after = result["statusAfterKeystroke"].lower()
    assert "refused" in after and "loading" in after
    # the load then settles normally: surfaces re-enable, content arrives
    assert result["afterDisabled"] is False
    assert result["afterContent"] == "# Document A\n"


def test_every_editing_surface_refuses_with_the_loading_posture_before_state_exists(
        editor_results):
    """F6-2: discard/save/selectDocument/applyProposal all dereferenced
    `state.buffers` with no guard; each must refuse with the fixed loading
    vocabulary instead of crashing."""
    results = editor_results["inputDuringLoad"]["results"]
    assert results["discard"].get("ok") is False
    assert "loading" in (results["discard"].get("error") or "").lower()
    assert results["save"].get("status") == "refused"
    assert "loading" in (results["save"].get("reason") or "").lower()
    assert results["select"].get("status") == "refused"
    assert "loading" in (results["select"].get("reason") or "").lower()
    assert results["apply"].get("ok") is False
    assert "loading" in (results["apply"].get("error") or "").lower()


def test_an_oversized_document_mounts_to_a_stated_failure_not_a_dead_canvas(
        editor_results):
    """F6-6: a >400,000-byte document used to reject inside initialLoad with no
    consumer -- state null forever, every keystroke a TypeError. The failure is
    now caught and STATED (the size class by its byte counts, never content),
    and the surfaces hold the same refuse-visibly posture as the loading
    state."""
    result = editor_results["oversizedLoad"]
    assert result["readyThrew"] is None, (
        f"the ready promise still rejects: {result['readyThrew']!r}")
    assert result["inputThrew"] is None, (
        f"a keystroke on the failed canvas threw: {result['inputThrew']!r}")
    assert result["stateIsNull"] is True
    for status_text in (result["statusText"], result["outlineStatusText"]):
        assert "400001" in status_text, "the measured size must be stated"
        assert "400000" in status_text, "the limit must be stated"
        assert "aaaa" not in status_text, "content is never echoed"
    assert result["textareaDisabled"] is True
    after = result["statusAfterKeystroke"]
    assert "refused" in after.lower()
    assert "400001" in after


def test_a_crlf_document_loads_clean_and_the_textarea_shows_the_lf_projection(
        editor_results):
    """F10-3 (FR-045): the buffer keeps the document's real bytes (CRLF) while
    the textarea holds the LF projection a real browser would report anyway --
    which is also what makes syncBufferDom's comparison settle: both sides of
    it now live in the display domain."""
    loaded = editor_results["eolPreservation"]["loaded"]
    assert loaded["dirty"] is False
    assert "\r\n" in loaded["content"]
    assert "\r" not in loaded["textareaValue"]
    assert loaded["textareaValue"] == loaded["content"].replace("\r\n", "\n")


def test_a_keystroke_in_a_crlf_document_preserves_its_line_endings_and_hash(
        editor_results):
    """F10-3: typing (in the browser's LF domain) produces buffer content with
    the document's CRLF endings preserved and an identity hashed over those
    real bytes -- the Save payload reads buffer content, so this is the half
    that makes FR-045's byte-exact round-trip possible at all."""
    typed = editor_results["eolPreservation"]["typed"]
    assert typed["content"] == typed["expectedContent"]
    assert typed["dirty"] is True
    assert typed["hashHex"] == typed["expectedHex"]
    # the display stays in the textarea's own LF domain -- no CRLF is ever
    # written back into a surface that would normalize it away again
    assert typed["textareaValue"] == "# Title\n\nline one\nline two\ntyped\n"


def test_typing_back_to_the_loaded_crlf_text_reads_clean_again(editor_results):
    """F10-3: the round trip closes -- typing back to exactly the loaded text
    re-derives the base bytes, so the buffer reads clean instead of dirty
    forever against an unchanged file."""
    back = editor_results["eolPreservation"]["back"]
    assert back["content"] == "# Title\r\n\r\nline one\r\nline two\r\n"
    assert back["dirty"] is False


def test_an_lf_document_is_untouched_by_the_eol_lens(editor_results):
    """F10-3's control: an LF document's keystrokes pass through unchanged --
    the lens re-applies the document's OWN flavor, never a fixed one."""
    lf = editor_results["eolPreservation"]["lf"]
    assert lf["content"] == "# Document A\nplus one line\n"
    assert "\r" not in lf["content"]
    assert lf["dirty"] is True


def test_a_proposal_enters_through_the_same_eol_lens_as_a_keystroke(
        editor_results):
    """W-2 (wave re-review): `applyProposal` used to hand the model's text to
    `edit()` verbatim -- only the HUMAN path routed through the lens -- so an
    LF proposal into a CRLF document made the buffer pure LF (a Save then
    committed an every-line-ending rewrite) and the next keystroke flipped
    the whole file back to CRLF: two byte-level outcomes for one reviewed
    proposal, re-opening the silent-mass-rewrite class F10-3 closed. The
    proposal now re-flavors exactly like read-back."""
    applied = editor_results["eolPreservation"]["applied"]
    assert applied["ok"] is True
    assert applied["content"] == applied["expectedContent"]
    assert applied["hashHex"] == applied["expectedHex"]
    # the display stays in the textarea's LF domain
    assert "\r" not in applied["textareaValue"]
    # and the LF control: the lens applies the document's OWN flavor
    lf_applied = editor_results["eolPreservation"]["lfApplied"]
    assert lf_applied["content"] == "# Document A\nmodel rewrite\n"


def test_the_guard_save_arm_stops_on_the_remount_its_own_save_triggers(
        save_seam_results):
    """W-8 (wave re-review): the guard's Save arm awaits a Save whose
    onSaveLanded hand-off REMOUNTS this canvas (the shell's recanvas on a key
    change destroys the controller). The corpse used to keep going:
    switchDocument mutated state, PERSISTED under the rekeyed session key
    after destroy() had written its own record — a reload in that window
    resurrected the wrong active document — and fired a late
    onIdentitySettled into the torn-down composition. The arm now re-checks
    destroyed after the await, and switchDocument refuses on a corpse."""
    remount = save_seam_results["guardSaveIntoRemount"]
    assert remount["blocked"] == "blocked"
    assert remount["resolved"]["status"] == "refused"
    # the save's OWN adopted-kind notification is the only one — no late
    # switch-fire from the destroyed controller
    assert remount["identityAfterResolve"] == ["document"]
    # the persisted record is destroy()'s own: the pre-switch document
    assert remount["persistedDocumentPath"] == "ideation/staging/topic-x/detail.md"


def test_a_selection_during_the_load_is_refused_and_says_so(editor_results):
    """W-9 (wave re-review): a document selection during the loading window is
    refused by the F6-2 posture, and the refusal must be STATED — it used to be
    silent, leaving whichever control asked showing a choice that never landed,
    forever, lying about which document edits land in and turns ground on.

    PIN EVOLUTION (Brett's 2026-08-15 annotation round): this drove the canvas's
    own picker and asserted the value it reverted to. The picker is retired —
    the context region's docs wheel is the sole human route — so what remains
    is the rule that outlived the control: `selectDocument` refuses, states the
    refusal in the Document buffer's own status region, and leaves the buffer
    on the document it really holds. The reverting half now belongs to the
    wheel and is pinned live in `test_a_blocked_selection_leaves_wheel_and_canvas_agreeing`."""
    probe = editor_results["selectDuringLoad"]
    doc_a = "ideation/staging/topic-x/detail.md"
    assert probe["duringLoad"]["refused"]["status"] == "refused"
    assert "refused --" in probe["duringLoad"]["status"]
    # the status names the buffer it reports (the annotation round's other half)
    assert probe["duringLoad"]["status"].startswith("Document: ")
    assert probe["afterLoad"]["bufferPath"] == doc_a


def test_eol_only_dirtiness_is_stated_in_fixed_vocabulary(editor_results):
    """P3-1 (wave re-review P3 tail): the first-break unification makes a
    mixed-EOL buffer dirty while its DISPLAY projection is byte-identical to
    the loaded text -- invisible dirtiness, and a Save then commits a
    whole-file line-ending diff nobody saw. When a dirty buffer's display
    projection equals the base's, the status line states the fact in fixed
    vocabulary; an ordinary dirty buffer keeps the ordinary sentence."""
    probe = editor_results["eolOnlyDirty"]
    eol = probe["eolOnly"]
    # preconditions: the invisible-dirtiness shape really occurred
    assert eol["dirty"] is True
    assert eol["bytesMoved"] is True
    assert eol["displayIdentical"] is True
    assert "unsaved changes" in eol["status"]
    assert "line endings only" in eol["status"]
    assert "mixed CR LF styles" in eol["status"]
    assert "saving unifies them" in eol["status"]
    ordinary = probe["ordinary"]
    assert "unsaved changes" in ordinary["status"]
    assert "line endings only" not in ordinary["status"]


def test_the_loading_and_failed_load_postures_disable_the_refusing_controls(
        editor_results):
    """P3-2 (wave re-review P3 tail): Save/Discard and the document picker
    were enabled from construction through the loading window (and forever
    after a failed load) while their handlers DISCARDED the refusal objects
    -- a silently dead click. They now mount disabled exactly like the
    textareas (the module's own honest-posture idiom), the first
    syncBufferDom re-enables them, and a failed load (where syncBufferDom
    never runs) leaves them disabled beside the stated failure.

    PIN EVOLUTION (Brett's 2026-08-15 annotation round): the picker is retired,
    so the posture is measured on the two controls that remain. The rule is
    unchanged and so is its reason — a control whose handler drops its refusal
    must be one the browser physically refuses."""
    during = editor_results["inputDuringLoad"]["duringControls"]
    assert during == {"discardDisabled": True, "saveDisabled": True}
    # PIN EVOLUTION (Brett's 2026-08-18 annotation round 2): a settled canvas is
    # CLEAN, and the controls now carry that — Save is reachable exactly when
    # there is something to save. So "the loading window ended" is proven by
    # making something dirty and watching them come live, which distinguishes
    # the two reasons a control can be unreachable instead of conflating them.
    after = editor_results["inputDuringLoad"]["afterControls"]
    assert after == {"discardDisabled": True, "saveDisabled": True}
    after_dirty = editor_results["inputDuringLoad"]["afterDirtyControls"]
    assert after_dirty == {"discardDisabled": False, "saveDisabled": False}
    failed = editor_results["oversizedLoad"]["failedControls"]
    assert failed == {"discardDisabled": True, "saveDisabled": True}


def test_an_edit_settling_after_destroy_leaves_storage_untouched(editor_results):
    """P3-10 (wave re-review P3 tail): an edit whose async hash settles after
    destroy() used to run its whole settle continuation on the corpse --
    persistNow re-wrote the record the FR-039 clear had just removed, and a
    late onIdentitySettled fired into the torn-down composition. The settle
    path now returns before persist/notify on a destroyed controller;
    destroy()'s own persist (which runs BEFORE the clear) is untouched."""
    probe = editor_results["destroyDuringEditSettle"]
    assert probe["storageKeysAfterSettle"] == [], (
        "the settle continuation re-persisted the cleared record")
    assert probe["lateNotifications"] == 0, (
        "a late identity notification fired into the torn-down composition")
    assert probe["editResult"]["ok"] is False
    assert "destroyed" in (probe["editResult"]["error"] or "")


def test_the_shell_posture_note_follows_the_catalog_failure(shell_results):
    """W-13 (wave re-review): the F10-1 shell threading was pinned only by a
    source-grep whose docstring claimed more than its assertions checked —
    deleting the failure half of the rail onState comparison left the whole
    repo green while the shell's note never left "no approved model is
    configured" on a failed catalog (the count is 0 before and after, so the
    count half never fires). This drives a failing catalog through the REAL
    mounted shell and reads the rendered note."""
    # PIN EVOLUTION (Brett's 2026-08-18 annotation round 2): the threading this
    # test guards is unchanged — the rail's catalog FAILURE must reach the human
    # and must not stay stuck on "no approved model is configured" — but its
    # destination moved. A chat rung's sentence is the SEND BUTTON's stated
    # reason now ("make this text the hover text for the send button if no model
    # selected"), so the standing shell line is empty and the sentence is read
    # where it went.
    assert shell_results["staleTokenPosture"] == ""
    title = shell_results["staleTokenSendTitle"]
    assert "console token is stale" in title, title
    assert "no approved model is configured" not in title
    # …and it is associated programmatically, not by title alone
    note = shell_results["staleTokenRailNote"]
    assert "console token is stale" in note
    assert shell_results["staleTokenRailNoteSrOnly"] is True
    assert shell_results["staleTokenSendDescribedBy"]


def test_the_editors_apply_refusals_carry_their_fixed_codes(editor_results):
    """W-10 (wave re-review): the rail's refusal vocabulary is chosen by the
    seam's CODE, so the editor must spell them — staleness advises a new
    turn, an unavailable target does not, and neither ever again claims the
    other's condition."""
    codes = editor_results["applyRefusalCodes"]
    assert codes["stale"]["ok"] is False
    assert codes["stale"]["code"] == "stale"
    assert codes["unavailable"]["ok"] is False
    assert codes["unavailable"]["code"] == "unavailable"


# ==========================================================================
# PR #196 review F3 + F4: THE CONTEXT REGION AND THE CANVAS, LIVE.
#
# Both findings are about three controls that answer ONE question -- the docs
# wheel, the canvas's own picker, and the buffer the canvas actually holds --
# and neither is visible to a source pin:
#
#   F3: selecting the document already loaded takes the `unchanged` route, which
#       still moves the chat's binding. The rail's header states that binding,
#       and nothing refreshed it, so the rail kept saying "Working on --
#       outline" beside a chat now working on the document. (The reviewer also
#       found the header had NO test at all; it does now.)
#   F4: a selection the guard BLOCKS leaves the wheel showing a document the
#       canvas never loaded. The picker has always reverted itself; the wheel
#       had no reconciliation and `doc-wheel.js`'s `selectPath` -- written for
#       exactly this -- had zero callers.
#
# So this mounts the REAL shell and drives it the way an operator does. The
# wheel's own selection is read through `pane.__docWheel.focused()`, the handle
# the pane already keeps for teardown -- no test-only DOM was added to observe
# it. Its LAYOUT is inert here (no measurable box in the shim, so `layout()`
# returns before it paints), which is exactly why selection is read from the
# controller rather than from `aria-selected`.
# ==========================================================================

_SELECTION_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';

globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');
globalThis.window = { location: { href: 'http://localhost/' } };

const { mountStagingWorkbench } = await import('./staging-workbench.js');

const OUTLINE_PATH = 'ideation/staging/topic-x/topic-x.md';
const DOC_A = 'ideation/staging/topic-x/detail.md';
const DOC_B = 'ideation/staging/topic-x/second.md';

const snapshot = {
  repository: 'fixture-repo',
  generation: { source_revision: '1'.repeat(40) },
  documents: [OUTLINE_PATH, DOC_A, DOC_B].map((p) => ({
    id: p, path: p, topics: ['alpha'],
    destinations: { staged_topics: ['topic-x'] } })),
  clusters: [], possibles: [],
  staged_topics: [{ staging_id: 'topic-x', files: [OUTLINE_PATH, DOC_A, DOC_B] }],
};

const caps = { actions: { gate: true, session: true }, actor: 'brett' };

function fire(node, type) {
  const listeners = (node.listeners && node.listeners[type]) || [];
  // A real event carries these too, and the docs tile's action handlers call
  // `stopPropagation` -- a click on an action belongs to the action, not the
  // tile it sits on.
  return Promise.all(listeners.map((fn) => fn({
    target: node, stopPropagation() {}, preventDefault() {} })));
}
// A real keydown: the wheel reads `ev.key` and consumes the event, so a bare
// {target} would sail straight past its handler.
function fireKey(node, key) {
  const listeners = (node.listeners && node.listeners.keydown) || [];
  return Promise.all(listeners.map(
    (fn) => fn({ target: node, key, preventDefault() {} })));
}
const settle = () => new Promise((r) => setTimeout(r, 0));
async function until(predicate, label) {
  for (let i = 0; i < 400; i += 1) {
    if (predicate()) return;
    await settle();
  }
  throw new Error('timed out waiting for ' + label);
}
class FakeStorage {
  constructor() { this.values = new Map(); }
  getItem(k) { return this.values.has(k) ? this.values.get(k) : null; }
  setItem(k, v) { this.values.set(k, String(v)); }
  removeItem(k) { this.values.delete(k); }
}

const container = document.createElement('div');
const doxbench = {
  loadSource: async (path) => ({ content: '# ' + path + '\n', ref: 'main' }),
  storage: new FakeStorage(),
  catalog: async () => ({
    schema_version: 1, kind: 'workbench-model-catalog',
    models: [{ model_id: 'model-a', label: 'Approved model', available: true,
               provider_class: 'on-tenant', input_limit_bytes: 800000,
               output_limit_bytes: 900000, data_handling: 'tenant boundary' }],
  }),
  chatTurn: async () => ({ ok: false, status: 502, payload: {} }),
};

const workbench = mountStagingWorkbench(container, snapshot, {
  caps,
  fetcher: async () => ({ ok: false }),
  active: { repository: 'fixture-repo', ref: 'main' },
  index: { entries: [] },
  doxbench,
  sourceBase: '/source/',
  edit: null,
  onSessionRekey: async () => null,
  onSessionEnded: async () => null,
  onScopeOpened: () => null,
});

workbench.open('staged', 'topic-x');

const byClass = (cls) => container.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));
const one = (cls) => byClass(cls)[0] || null;

await until(() => byClass('doxbench-textarea').length === 2, 'the canvas');
await until(() => one('doxchat-loaded') !== null, 'the chat rail');
const documentArea = byClass('doxbench-textarea')[1];
await until(() => documentArea.value.includes(DOC_A), 'the loaded document');

// the wheel's OWN selection, through the handle the pane already keeps
const wheelPane = container.walk().find((n) => n.__docWheel);
const wheelPath = () => {
  const focused = wheelPane.__docWheel.focused();
  return focused ? focused.path : null;
};
// the canvas's own picker is retired (Brett's 2026-08-15 annotation round), so
// the surfaces that must agree are the wheel and the canvas itself
const pickerNodes = () => byClass('doxbench-document-picker').length;
// Brett's 2026-08-21 annotation removed the standing header line, so the STATED
// binding is read off the two surfaces that carry it now: the selector's own
// selection, and the sr-only full-name region beside it.
const bindingText = () => String((one('doxchat-loaded-full') || {}).textContent || '');
const boundValue = () => String((one('doxchat-loaded') || {}).value || '');
// the canvas's own answer: the fake source names the path it loaded
const canvasDocument = () => (byClass('doxbench-textarea')[1] || {}).value || '';
// The canvas's OWN answer to "which document am I holding", independent of
// the two controls under test: a switch to DOC_B would have replaced the
// buffer's text with DOC_B's, taking the human's unsaved bytes with it.
const agree = () => ({
  wheel: wheelPath(), pickerNodes: pickerNodes(), editors: byClass('doxbench-textarea').length,
  // the canvas's OWN answer, independent of the two controls under test: a
  // switch that landed would have replaced the buffer's text with DOC_A's,
  // taking the human's unsaved bytes with it
  canvasSwitchedToA: canvasDocument().includes(DOC_A),
});

const out = {};
// the rail renders once before the canvas's initial load settles, so wait for
// the binding statement to be reading real buffers rather than pinning the
// empty frame
await until(() => bindingText().includes(OUTLINE_PATH.split('/').pop()),
            'the rail binding statement to read the loaded buffers');
out.bindingAtMount = bindingText();
out.boundAtMount = boundValue();
out.headerAbsent = byClass('doxchat-header').length === 0;

// ---- F3: the tile's LOAD verb moves the STATED binding --------------------
// RE-CUT by `add-doxbench-editing-phase-b` (PR #207 review, F1's root cause).
// A docs-row SELECTION no longer binds anything -- the ratified delta names the
// outline tab, LOADING a document, and the rail's selector as the three
// selection routes, and keeping the row selection made the loaded set
// unreachable. So the binding change this test is about is driven through the
// verb that actually performs it now.
const selector = one('swb-docselector');
selector.clientHeight = 420;
const docsPane = container.walk().find((n) => n.__docWheelRefresh);
docsPane.__docWheelRefresh();
for (let i = 0; i < 5; i += 1) await settle();
const tiles = byClass('wheeltile');
const target = tiles.find((t) => t.title === DOC_B);
for (let attempt = 0; attempt < 3; attempt += 1) {
  if (target.querySelector('.wheelactions')) break;
  await fire(target, 'click');
  for (let i = 0; i < 5; i += 1) await settle();
}
await fire(target.querySelector('.swb-docload'), 'click');
await until(() => byClass('doxbench-textarea').length === 3,
            'the loaded document its own editor');
for (let i = 0; i < 20; i += 1) await settle();
out.wheelAfterLoad = wheelPath();
out.bindingAfterLoad = bindingText();
out.boundAfterLoad = boundValue();
out.loadedEditorCount = byClass('doxbench-textarea').length;
// The FIRST document is untouched by the second one arriving: its own editor
// still holds its own text, under its own key.
out.firstStillHeld = byClass('doxbench-textarea')[1].value.includes(DOC_A);
out.secondHeld = byClass('doxbench-textarea')[2].value.includes(DOC_B);

// ---- F4: a load REPLACES nothing, so no guard can fire ---------------------
// Type into the first document, then load ANOTHER one. Under Phase A this was
// the guard's whole reason to exist: the switch would have overwritten those
// bytes. Under Phase B the second document arrives BESIDE the first, under its
// own key, so there is nothing to guard -- which is exactly what the delta says
// ("a selection change no longer replaces any buffer's content once documents
// are held side by side rather than in one slot") and what this now pins.
const editorTab = byClass('doxbench-viewtab')[0];
await fire(editorTab, 'click');
for (let i = 0; i < 10; i += 1) await settle();
const firstArea = byClass('doxbench-textarea')[1];
firstArea.value = '# unsaved work in the first document\n';
await fire(firstArea, 'input');
await until(() => byClass('doxbench-status').some(
  (n) => String(n.textContent || '').includes('unsaved')), 'the dirty document');
for (let i = 0; i < 20; i += 1) await settle();
// A THIRD document is loaded while the first holds unsaved work.
const third = byClass('wheeltile').find((t) => t.title === OUTLINE_PATH);
for (let attempt = 0; attempt < 3; attempt += 1) {
  if (third.querySelector('.wheelactions')) break;
  await fire(third, 'click');
  for (let i = 0; i < 5; i += 1) await settle();
}
await fire(third.querySelector('.swb-docload'), 'click');
for (let i = 0; i < 40; i += 1) await settle();
out.guardShown = !(one('doxbench-guard') || { hidden: true }).hidden;
out.unsavedWorkSurvived =
  byClass('doxbench-textarea')[1].value.includes('unsaved work');
out.afterLoad = agree();

console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def selection_results(tmp_path_factory):
    """A live shell mount for the context-region selection routes (PR #196
    review F3/F4). Its own process, like every other harness in this file."""
    if NODE is None:
        pytest.skip("node not available for the doxBench selection probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-selection")
    views = tmp_path / "views"
    shutil.copytree(EDITOR_JS.parent, views)
    shutil.copytree(EDITOR_JS.parent.parent / "vendor", tmp_path / "vendor")
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "vendor" / "package.json").write_text(
        '{"type": "commonjs"}', encoding="utf-8")
    harness = views / "selection-harness.mjs"
    harness.write_text(_SELECTION_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=90)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_the_rail_states_the_buffer_the_chat_is_working_on(selection_results):
    """PR #196 review F3, first half: the rail's header states the ACTIVE
    buffer -- the chat's working context -- and it had no test at all. At mount
    the outline is active, so that is what it must say.

    RE-PINNED by `add-doxbench-editing-phase-b` (task 7.1). The BINDING half is
    untouched and still asserted exactly: the header states the selected buffer,
    first, by name. What moved is the GROUNDING half. Phase A's header enumerated
    two fixed buffer names ("Outline: … · Document: …") because the set held
    exactly those two; Phase B holds the outline plus N loaded documents, and an
    enumeration of N filenames in a one-line header is unreadable at four
    documents and impossible at twenty.

    So the header STATES the count and the ENUMERATION moves into the
    loaded-document selector immediately beside it -- which is where a human can
    also act on it, and which is what Q1's ruling asked for. The claim the
    Phase A assertion was making is not weakened: grounding still names every
    buffer the turn carries, the header still says so, and the selector now
    proves it entry by entry (`test_doxbench_tile_verbs.py`). The outline keeps
    its own named slot because its key is permanently reserved and it is the one
    buffer that rides every turn.

    RE-PINNED AGAIN by Brett's 2026-08-21 annotation on `div.doxchat-header`
    ("remove this section."). The standing line is gone as a restatement of what
    the selector below it already showed, so the CLAIM this test makes now rests
    on the two surfaces that survived it: the selector's own selection, and the
    sr-only full-name region that names it for assistive technology. The
    grounding COUNT the line used to carry is the selector's own listing, pinned
    entry by entry in `test_doxbench_tile_verbs.py`.
    """
    assert selection_results["headerAbsent"] is True, (
        "the standing header line must not come back")
    # At mount the OUTLINE is the selected buffer, and both surfaces say so. The
    # selector carries the reserved KEY (the outline's key is permanently
    # `outline`, never its path); the sr-only region names the path in full.
    assert selection_results["boundAtMount"] == "outline"
    assert selection_results["bindingAtMount"] == (
        "Working on ideation/staging/topic-x/topic-x.md")


def test_the_tile_load_verb_moves_the_stated_binding(selection_results):
    """PR #196 review F3, second half — RE-CUT by `add-doxbench-editing-phase-b`
    (PR #207 review, F1's root cause).

    The CLAIM is unchanged: a route that moves the binding without moving a
    content identity must still refresh the rail's header, or the rail keeps
    naming the outline beside a chat now working on a document. What moved is
    WHICH route does that. Phase A bound from a docs-row selection; the ratified
    delta names the outline tab, LOADING a document, and the rail's selector as
    the three selection routes, and keeping the row selection made the loaded set
    unreachable (a tile click pre-switched the single reserved slot, so the LOAD
    that followed always found the document already loaded). So the binding change
    is driven here through the verb that performs it now.

    (The `unchanged` route — selecting the document the canvas already holds —
    is the same binding change with no switch at all; it is refreshed by the
    same call, is pinned as a shell doctrine in test_staging_workbench.py, and
    its binding half is driven at the controller in
    `test_the_context_selection_chooses_the_active_buffer_not_the_view_tabs`.)"""
    assert selection_results["wheelAfterLoad"].endswith("second.md")
    # Brett's 2026-08-21 annotation removed the standing header line; the STATED
    # binding the claim is about is the selector's own selection and the sr-only
    # region beside it, and the LOAD verb must still move both.
    assert selection_results["boundAfterLoad"] == (
        "ideation/staging/topic-x/second.md")
    assert selection_results["bindingAfterLoad"] == (
        "Working on ideation/staging/topic-x/second.md")
    # The second document arrived BESIDE the first: three editors, each holding
    # its own text under its own key. Phase A had one document slot, so this was
    # the switch the guard existed to protect; Phase B replaces nothing.
    assert selection_results["loadedEditorCount"] == 3
    assert selection_results["firstStillHeld"] is True
    assert selection_results["secondHeld"] is True


def test_loading_beside_unsaved_work_replaces_nothing_and_needs_no_guard(
    selection_results,
):
    """PR #196 review F4 — RE-CUT by `add-doxbench-editing-phase-b` (PR #207
    review).

    Phase A's guard existed because switching the ONE document slot overwrote
    whatever unsaved bytes it held, and this test drove a guard-blocked switch to
    prove the wheel and the canvas still agreed afterwards. Under Phase B a load
    adds a buffer BESIDE the others under its own key and replaces nothing, so
    there is no switch to block — which is exactly what the ratified delta says
    ("a selection change no longer replaces any buffer's content once documents
    are held side by side rather than in one slot") and what is pinned here
    instead: the unsaved work survives untouched, no guard is raised, and the
    surfaces still agree.

    The guard itself is NOT retired and is NOT weakened: it still governs
    `selectDocument`, which the load verb still reaches for the one transition
    that does replace content — filling a reserved slot that is still unbacked.
    Its narrowed applicability is the delta's own prediction that it is
    "unchanged by this rule WHERE IT STILL APPLIES" and never extended to
    selection.

    The ORIGINAL claim — that the controls answering "which document" must not
    disagree — is what the docs wheel had no reconciliation for, so a blocked
    left it showing a document the canvas never loaded -- and `doc-wheel.js`'s
    `selectPath`, which exists for precisely this, had zero callers.

    PIN EVOLUTION (Brett's 2026-08-15 annotation round): there were THREE such
    surfaces; the canvas's own picker is retired, so there are two, and the
    third is asserted absent. Blocked, and then declined, the wheel and the
    canvas must still name the document that is actually open."""
    # NO GUARD IS RAISED, because nothing is replaced: the third document arrives
    # under its own key beside the two already held.
    assert selection_results["guardShown"] is False
    # …and the unsaved work is exactly where the human left it. Under Phase A this
    # load would have been a SWITCH, and these bytes are what the guard existed to
    # stand in front of.
    assert selection_results["unsavedWorkSurvived"] is True
    # The surfaces still agree, which is the original claim: the wheel names a
    # document the canvas really holds, there is no third selection surface, and
    # the first document was not flushed by the arrival of another.
    state = selection_results["afterLoad"]
    assert state["pickerNodes"] == 0
    assert state["wheel"] is not None
    assert state["editors"] >= 3, (
        "each loaded buffer holds its own editor; none replaced another")
    # `canvasSwitchedToA` is False here BY CONSTRUCTION and that is the point: the
    # human typed OVER the first document's text, so its editor holds their bytes
    # rather than the loaded source's — and `unsavedWorkSurvived` above is the
    # assertion that those bytes are still there after another document arrived.
    assert state["canvasSwitchedToA"] is False


# ===========================================================================
# add-doxbench-editing-phase-b: THE LOADED SET, on the live canvas.
#
# One harness, its own node process like every other in this file, driving the
# controller's Phase B surface against the SAME DOM shim and the SAME injected
# seams the Phase A scenarios use. What is new is only how many buffers exist.
#
# The tile-Save scenario deliberately composes the REAL `doxbench-save.js`
# (`runSave(savePlanState(request), {transport, only: request.only})`) rather
# than a scripted stand-in, because the whole claim under test is that the tile
# Save is the SAME pipeline narrowed — a hand-written seam could "prove" a scope
# the real orchestrator does not honour.
#
# WHAT THIS DOES NOT CLAIM (PR #207 review, F7): it is not a tripwire on the
# console's own composition. The canvas narrows the buffer set BEFORE it builds
# the request, so a composition that dropped `only` would still persist exactly
# these rows and this harness could not tell. Forwarding the scope is defence in
# depth, said as such in `app.js`, and the mechanism `only` performs is pinned
# where it lives — `runSave` over a four-buffer state in
# `test_doxbench_save.py::test_the_tile_save_persists_that_document_plus_the_ancestry_step_only`,
# which DOES fail if the scope stops being honoured.
# ===========================================================================

_LOADED_SET_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';
globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');

const { mountDoxBenchCanvas, boundReachedReason, unadoptedCommitReason } =
  await import('./doxbench-editor.js');
const { runSave, savePlanState, IDENTITY_NOT_ADOPTABLE } =
  await import('./doxbench-save.js');
// #290: the ADOPTING module, so a scenario can ask it for the very refusal the
// canvas will have caught rather than transcribing one and hoping they match.
const { adoptSavedBase } = await import('./doxbench-state.js');

const OUTLINE_PATH = 'ideation/staging/topic-x/topic-x.md';
const DOC_A = 'ideation/staging/topic-x/detail.md';
const DOC_B = 'ideation/staging/topic-x/second.md';
const DOC_C = 'ideation/staging/topic-x/third.md';
const COLLIDE_A = 'ideation/staging/topic-x/alpha/README.md';
const COLLIDE_B = 'ideation/staging/topic-x/beta/README.md';
const CONTEXT_DOC = 'ideation/brainstorm/inherited.md';
const SESSION_REF = 'draft/topic-x';
const CONTENT = {
  [OUTLINE_PATH]: '# Outline\n',
  [DOC_A]: '# Document A\n',
  [DOC_B]: '# Document B\n',
  [DOC_C]: '# Document C\n',
  [COLLIDE_A]: '# Alpha readme\n',
  [COLLIDE_B]: '# Beta readme\n',
  [CONTEXT_DOC]: '# Inherited\n',
};

class FakeStorage {
  constructor() { this.values = new Map(); this.removed = []; }
  getItem(k) { return this.values.has(k) ? this.values.get(k) : null; }
  setItem(k, v) { this.values.set(k, String(v)); }
  removeItem(k) { this.removed.push(k); this.values.delete(k); }
}

const loadSource = async (path) => (path in CONTENT
  ? { content: CONTENT[path], revision: 'rev-' + path, ref: 'main' } : null);

// The same lowercase-SHA-256-shaped stand-in the save-seam harness uses: the
// state module validates every identity it writes into working state, so a
// fixture emitting 64 arbitrary characters would model a server that cannot
// exist.
function identity(seed) {
  let hex = '';
  for (const ch of String(seed)) hex += ch.charCodeAt(0).toString(16).padStart(2, '0');
  return { algorithm: 'sha256', hex: hex.padEnd(64, '0').slice(0, 64) };
}

function projection(overrides = {}) {
  const editable = [OUTLINE_PATH, DOC_A, DOC_B, DOC_C, COLLIDE_A, COLLIDE_B];
  const base = {
    key: { repository: 'fixture-repo', ref: 'main',
           tile_kind: 'staged', tile_id: 'topic-x' },
    title: 'Topic X', source_revision: 'a'.repeat(40),
    outline_path: OUTLINE_PATH,
    editable_paths: editable,
    context_paths: editable.concat([CONTEXT_DOC]),
    active_document_candidates: [DOC_A],
    sections: [],
  };
  const merged = { ...base, ...overrides };
  merged.key = { ...base.key, ...(overrides.key || {}) };
  return merged;
}

// THE REAL ORCHESTRATOR, composed exactly as the console's own seam must be.
function realSeam(calls) {
  return (request) => runSave(savePlanState(request), {
    only: request.only,
    transport: async (req) => {
      calls.push({ kind: req.kind, document: req.document, action: req.action });
      return {
        ok: true, action: req.action, ref: SESSION_REF,
        revision: 'rev-' + calls.length,
        content_hash: identity(String(req.document) + 'saved'),
      };
    },
  });
}

// THE RESERVED UNBACKED SLOT IS LEFT UNBACKED (`activeDocumentPath: null`), so
// every document below arrives through the LOAD verb under its own path key.
// A mount that pre-seeded the reserved slot with the first candidate would make
// loading THAT document the already-loaded case — which is correct behaviour and
// is pinned on its own in `alreadyLoaded`, but it is not what these scenarios are
// measuring.
async function mount(opts = {}, over = {}) {
  const host = new Node('div');
  const controller = mountDoxBenchCanvas(host, projection(over), {
    loadSource, storage: new FakeStorage(), previewDelayMs: 5,
    activeDocumentPath: null, ...opts,
  });
  await controller.ready;
  return { controller, host };
}

const classCount = (host, cls) => host.walk()
  .filter((n) => String(n.className).split(' ').includes(cls)).length;
const dirtyMap = (controller) => Object.fromEntries(
  controller.bufferKeys().map((k) => [k, controller.state().buffers[k].dirty]));

// ---- a third document is a first-class buffer -----------------------------
async function thirdDocument() {
  const { controller, host } = await mount();
  const results = [];
  for (const path of [DOC_A, DOC_B, DOC_C]) {
    results.push(await controller.loadDocumentForEditing(path));
  }
  // …and one of the three is edited, so dirtiness is per buffer
  await controller.edit(DOC_B, '# Document B edited\n');
  const statusFor = (k) => {
    const node = controller.elements().status(k);
    return { text: String(node.textContent), name: node.getAttribute('aria-label'),
             hidden: node.hidden === true, cls: String(node.className) };
  };
  return {
    results,
    keys: controller.bufferKeys(),
    loaded: controller.loadedBuffers(),
    dirty: dirtyMap(controller),
    active: controller.activeBuffer(),
    textareas: classCount(host, 'doxbench-textarea'),
    previews: classCount(host, 'doxbench-preview'),
    statuses: classCount(host, 'doxbench-status'),
    statusB: statusFor(DOC_B),
    statusC: statusFor(DOC_C),
    // the third document's own text really is its own
    contentC: controller.state().buffers[DOC_C].content,
    contentB: controller.state().buffers[DOC_B].content,
  };
}

// ---- an unheld key is refused, a held one is not -------------------------
async function unheldKey() {
  const { controller } = await mount();
  await controller.loadDocumentForEditing(DOC_A);
  let refusal = null;
  try {
    controller.setActiveBuffer(DOC_B);   // in scope, never loaded
  } catch (error) {
    refusal = String(error && error.message);
  }
  let typoRefusal = null;
  try {
    controller.setActiveBuffer('outlien');
  } catch (error) {
    typoRefusal = String(error && error.message);
  }
  return {
    refusal, typoRefusal,
    activeAfterRefusal: controller.activeBuffer(),
    heldAccepted: controller.setActiveBuffer(DOC_A),
    outlineAccepted: controller.setActiveBuffer('outline'),
  };
}

// ---- the bound refuses and STATES the measured number -------------------
async function boundRefusal() {
  const notified = [];
  // THREE, because the reserved unbacked slot every mount builds is itself a
  // buffer that may hold unsaved work, and the state module counts it -- which is
  // the whole point of the bound. So two loads fill the set and the third refuses.
  const { controller } = await mount({
    maxLoadedDocuments: 3,
    onLoadedSetChanged: (snapshot) => notified.push(snapshot.documents.length),
  });
  const first = await controller.loadDocumentForEditing(DOC_A);
  const second = await controller.loadDocumentForEditing(DOC_B);
  // the third is one past the bound
  const third = await controller.loadDocumentForEditing(DOC_C);
  return {
    first, second, third,
    keys: controller.bufferKeys(),
    // the exact sentence the module builds, so the numbers are pinned rather
    // than matched loosely
    expected: boundReachedReason(3, 3),
    eventNote: String(controller.elements().eventNote().textContent),
    notified,
  };
}

// ---- unloading a dirty buffer refuses ----------------------------------
async function dirtyUnload() {
  const { controller } = await mount();
  await controller.loadDocumentForEditing(DOC_A);
  await controller.edit(DOC_A, '# Document A edited\n');
  const refused = controller.unloadDocument(DOC_A);
  const afterRefusal = {
    keys: controller.bufferKeys(),
    content: controller.state().buffers[DOC_A].content,
    dirty: controller.state().buffers[DOC_A].dirty,
  };
  const discarded = controller.unloadDocument(DOC_A, { discardUnsavedEdits: true });
  return {
    refused, afterRefusal, discarded,
    keysAfter: controller.bufferKeys(),
    activeAfter: controller.activeBuffer(),
    // the nodes stay, blanked and hidden, so a re-load reuses them
    statusHidden: controller.elements().status(DOC_A).hidden === true,
    statusText: String(controller.elements().status(DOC_A).textContent),
    reloaded: await controller.loadDocumentForEditing(DOC_A),
    contentAfterReload: controller.state().buffers[DOC_A].content,
  };
}

// ---- the UNBACKED slot is inert: there is nothing to unload --------------
// AMENDMENT 2 narrowed the reserved set to the OUTLINE ALONE, and this is the one
// non-outline key the canvas control still withholds -- for a different reason
// entirely, which is why it needs its own measurement. The create flow's
// not-yet-created slot IS a held buffer, but it names no document, so it has no
// loaded-set membership for Unload to end. `loadedBuffers` filters it out for
// exactly that reason and the selector never lists it.
//
// A save seam is supplied because without one the slot does not swap at all
// (the gate-absent clause), and this scenario is about what the SWAPPED slot
// shows.
async function unbackedSlotInert() {
  const { controller } = await mount({ save: realSeam([]) });
  controller.setActiveBuffer('document');
  const els = controller.elements();
  const before = {
    path: controller.state().buffers.document.path,
    listed: controller.loadedBuffers().map((row) => row.key),
    rendered: els.unload().hidden !== true,
    disabled: els.unload().disabled === true,
    title: String(els.unload().title || ''),
    noteHidden: els.unloadNote().hidden === true,
    noteText: String(els.unloadNote().textContent || ''),
  };
  // Press it anyway: the click path re-derives the same rule, so the render's
  // disabled state is not the only thing holding it.
  for (const fn of (els.unload().listeners.click || [])) {
    await fn({ target: els.unload(), stopPropagation() {}, preventDefault() {} });
  }
  return { before, keysAfter: controller.bufferKeys(),
           activeAfter: controller.activeBuffer() };
}

// ---- the OUTLINE is refused by the same one rule -------------------------
// The other half of the narrowed guard, measured at the canvas module: dropping
// the outline's reservation must not pass.
async function outlineStaysReserved() {
  const { controller } = await mount({ save: realSeam([]) });
  await controller.loadDocumentForEditing(DOC_A);
  controller.setActiveBuffer('outline');
  const els = controller.elements();
  const posture = {
    rendered: els.unload().hidden !== true,
    disabled: els.unload().disabled === true,
    title: String(els.unload().title || ''),
    noteText: String(els.unloadNote().textContent || ''),
  };
  for (const fn of (els.unload().listeners.click || [])) {
    await fn({ target: els.unload(), stopPropagation() {}, preventDefault() {} });
  }
  return { posture, keysAfter: controller.bufferKeys(),
           refusal: controller.unloadDocument('outline') };
}

// ---- the tile Save is the same pipeline, narrowed ----------------------
async function tileSave() {
  const calls = [];
  const { controller } = await mount({ save: realSeam(calls) });
  await controller.loadDocumentForEditing(DOC_A);
  await controller.loadDocumentForEditing(DOC_B);
  await controller.edit('outline', '# Outline edited\n');
  await controller.edit(DOC_A, '# Document A edited\n');
  await controller.edit(DOC_B, '# Document B edited\n');
  const outcome = await controller.saveDocument(DOC_A);
  return {
    outcome,
    calls,
    dirty: dirtyMap(controller),
    // the untouched document's bytes are exactly what the human left
    contentB: controller.state().buffers[DOC_B].content,
    statusB: String(controller.elements().status(DOC_B).textContent),
    statusA: String(controller.elements().status(DOC_A).textContent),
    statusOutline: String(controller.elements().status('outline').textContent),
    // …and the outline it DID act on advanced onto the reported base
    outlineBaseRef: controller.state().buffers['outline'].base_ref,
  };
}

// ---- a context-only document loads, and its tile Save does not -----------
async function contextOnlyTileSave() {
  const calls = [];
  const { controller } = await mount({ save: realSeam(calls) });
  const loaded = await controller.loadDocumentForEditing(CONTEXT_DOC);
  await controller.edit(CONTEXT_DOC, '# Inherited, edited\n');
  const refused = await controller.saveDocument(CONTEXT_DOC);
  return {
    loaded, refused, calls,
    owned: controller.loadedBuffers().map((row) => ({ key: row.key, owned: row.owned })),
  };
}

// ---- R-5 (#81): the ONE visible Save line leads with the FIRST failing
// ---- cause, never with a downstream consequence of it --------------------
//
// THE REAL ORCHESTRATOR again, with a transport that refuses the ANCESTRY step.
// `runSave` then reports the outline `refused` with the transport's own reason
// and every document behind it `not_attempted` with the missing-ancestry reason
// -- a root and its consequences, in save order -- which is precisely the shape
// a single transient line has to choose from. A scripted stand-in could not
// produce it: the `not_attempted` rows are the orchestrator's own answer.
const ANCESTRY_REFUSAL = 'the outline base moved under this buffer';

function refusingSeam(calls, refusals) {
  return (request) => runSave(savePlanState(request), {
    only: request.only,
    transport: async (req) => {
      calls.push({ kind: req.kind, document: req.document });
      const refusal = refusals[req.kind];
      if (refusal) return { ok: false, message: refusal };
      return {
        ok: true, action: req.action, ref: SESSION_REF,
        revision: 'rev-' + calls.length,
        content_hash: identity(String(req.document) + 'saved'),
      };
    },
  });
}

async function refusedAncestryLeadsTheSummary() {
  const calls = [];
  const { controller } = await mount({
    save: refusingSeam(calls, { outline: ANCESTRY_REFUSAL }),
  });
  await controller.loadDocumentForEditing(DOC_A);
  await controller.loadDocumentForEditing(DOC_B);
  await controller.edit('outline', '# Outline edited\n');
  await controller.edit(DOC_A, '# Document A edited\n');
  await controller.edit(DOC_B, '# Document B edited\n');
  const outcome = await controller.save();
  const note = controller.elements().eventNote();
  const read = {
    outcome, calls,
    eventNote: String(note.textContent),
    eventNoteHidden: note.hidden === true,
    // every buffer's OWN durable sentence, which is where the per-buffer
    // detail lives whichever row the transient line leads with
    statuses: Object.fromEntries(controller.bufferKeys().map(
      (k) => [k, String(controller.elements().status(k).textContent)])),
  };
  controller.destroy();   // releases the note's own timer
  return read;
}

// ---- …and an `unchanged` row is not something to report ------------------
//
// The companion case to the one above, in TWO scenarios since issue #291.
//
// `cleanOutlineDoesNotTakeTheLead` is the real-orchestrator half. A tile Save
// scopes to ONE document; the canvas hands the seam the buffers that CHANGED,
// so a clean outline is not in the reshaped state and -- since #291 stopped
// `saveBufferOrder` inventing the reserved key -- gets no row at all. The
// refused document is therefore the only row, it leads, and the clean outline's
// own region states its honest condition (`no unsaved changes`) rather than a
// Save verdict about an act it was never part of.
//
// `vacuousRowNeverLeads` keeps the RULE pinned where the shape now lives: the
// canvas reads whatever rows a seam hands it, `unchanged` is a declared
// per-buffer status, and a lead chosen from "every row that is not committed"
// takes the vacuous row and buries the refusal behind it -- the #81 defect from
// the other end. `tileSaveVerdict` filters to the withheld set
// (`refused`/`not_attempted`); the visible line must use the SAME set, which is
// what makes "the two surfaces agree" true rather than nearly true. The rows are
// scripted here on purpose: that is exactly the shape the orchestrator used to
// produce, and the canvas must still refuse to lead with it.
async function cleanOutlineDoesNotTakeTheLead() {
  const { controller } = await mount({
    save: (request) => runSave(savePlanState(request), {
      only: request.only,
      transport: async () => ({
        ok: false, message: 'the document base moved under this buffer' }),
    }),
  });
  await controller.loadDocumentForEditing(DOC_A);
  // the outline is deliberately NOT edited: it stays clean and reports `unchanged`
  await controller.edit(DOC_A, '# Document A edited\n');
  const outcome = await controller.saveDocument(DOC_A);
  const read = {
    rows: outcome.buffers.map((row) => ({ key: row.key, status: row.status })),
    tileError: outcome.error,
    eventNote: String(controller.elements().eventNote().textContent),
    statusA: String(controller.elements().status(DOC_A).textContent),
    statusOutline: String(controller.elements().status('outline').textContent),
  };
  controller.destroy();
  return read;
}

// The scripted half: a seam answer that DOES carry a vacuous row, first.
const VACUOUS_REFUSAL = 'the document base moved under this buffer';

async function vacuousRowNeverLeads() {
  const { controller } = await mount({
    save: async (request) => ({
      status: 'refused',
      buffers: [
        { key: 'outline', status: 'unchanged', action: null, ref: null,
          revision: null, content_hash: null, message: null },
        { key: DOC_A, status: 'refused', action: 'edit-document', ref: null,
          revision: null, content_hash: null, message: VACUOUS_REFUSAL },
      ],
    }),
  });
  await controller.loadDocumentForEditing(DOC_A);
  await controller.edit(DOC_A, '# Document A edited\n');
  const outcome = await controller.saveDocument(DOC_A);
  const read = {
    rows: outcome.buffers.map((row) => ({ key: row.key, status: row.status })),
    tileError: outcome.error,
    eventNote: String(controller.elements().eventNote().textContent),
    statusA: String(controller.elements().status(DOC_A).textContent),
    statusOutline: String(controller.elements().status('outline').textContent),
  };
  controller.destroy();
  return read;
}

// ---- …and when nothing failed, the line stays away entirely --------------
//
// The third case in the same family, and the one Brett RULED (2026-08-24):
// a Save with nothing withheld says nothing on the transient line. Narrowing
// the lead to the withheld set (above) realized that as a side effect -- a
// fully successful tile save used to flash `Outline: nothing to save in this
// buffer`, because the clean outline's `unchanged` row was "not committed" and
// took the line. That is a report about the one buffer the human did not act
// on, standing in for the one they did.
//
// Realized-but-unpinned is how a ruling quietly stops being true, so it is
// pinned here rather than left to the code that happens to produce it. What
// must NOT change with it: every buffer's own sr-only region still carries its
// own outcome sentence (FR-035), and the tile still reports its success. The
// line going quiet is the absence of a PROBLEM, never the absence of a report.
async function nothingToSayTakesNoLine() {
  const calls = [];
  const { controller } = await mount({ save: realSeam(calls) });
  await controller.loadDocumentForEditing(DOC_A);
  // again the outline is deliberately NOT edited: it rides along `unchanged`
  await controller.edit(DOC_A, '# Document A edited\n');
  const outcome = await controller.saveDocument(DOC_A);
  const note = controller.elements().eventNote();
  const read = {
    rows: outcome.buffers.map((row) => ({
      key: row.key, status: row.status, action: row.action || null,
      ref: row.ref || null })),
    ok: outcome.ok === true,
    error: outcome.error,
    // #290: the field is an array on EVERY answer a seam returned, so a fully
    // adopted Save reports an EMPTY one rather than omitting it
    unadopted: outcome.unadopted,
    eventNoteText: String(note.textContent),
    eventNoteHidden: note.hidden === true,
    // the durable per-buffer regions, which is where the report actually lives
    statuses: Object.fromEntries(controller.bufferKeys().map(
      (k) => [k, String(controller.elements().status(k).textContent)])),
  };
  controller.destroy();
  return read;
}

// ---- #290: a commit this canvas could not adopt is NOT a tile success
//
// TWO ARMS, because the defect has two layers and repairing either one alone
// leaves the other reachable.
//
// ARM 1 is the TRIGGER, through the REAL orchestrator: a validator divergence.
// `doxbench-save.js` accepted ANY non-empty algorithm and ANY 64 characters,
// while `doxbench-state.js` -- the module that WRITES the identity into working
// state -- accepts only a lowercase SHA-256 one. Two differently strict judges
// of one value, so an uppercase-hex answer read `committed` here and threw
// there.
//
// ARM 2 is the BRANCH ITSELF, reached directly. The seam is INJECTED, so a row
// the state module cannot adopt is always constructible whatever the
// orchestrator does with identities, and the canvas's own answer must stay
// honest for whatever future trigger arrives at it.
const UPPERCASE_IDENTITY = { algorithm: 'sha256', hex: 'A'.repeat(64) };

async function unadoptableIdentityThroughTheRealOrchestrator() {
  const calls = [];
  const { controller } = await mount({
    save: (request) => runSave(savePlanState(request), {
      only: request.only,
      transport: async (req) => {
        calls.push({ kind: req.kind, document: req.document });
        return {
          ok: true, action: req.action, ref: SESSION_REF,
          revision: 'rev-' + calls.length,
          content_hash: UPPERCASE_IDENTITY,
        };
      },
    }),
  });
  await controller.loadDocumentForEditing(DOC_A);
  // the outline is deliberately NOT edited: this act is about ONE document
  await controller.edit(DOC_A, '# Document A edited\n');
  const outcome = await controller.saveDocument(DOC_A);
  const buffer = controller.state().buffers[DOC_A];
  const read = {
    calls,
    ok: outcome.ok === true,
    error: outcome.error,
    rows: outcome.buffers.map((row) => ({
      key: row.key, status: row.status, message: row.message })),
    dirtyA: buffer.dirty,
    contentA: buffer.content,
    baseHexA: buffer.base_hash.hex,
    statusA: String(controller.elements().status(DOC_A).textContent),
    eventNote: String(controller.elements().eventNote().textContent),
    // the SAVE MODULE's own words for this refusal, so the pin compares against
    // the module rather than against a transcription of it
    identityNotAdoptable: IDENTITY_NOT_ADOPTABLE,
  };
  controller.destroy();   // releases the note's own timer
  return read;
}

async function committedRowThisCanvasCannotAdopt() {
  const seen = [];
  const { controller } = await mount({
    save: async (request) => {
      seen.push(request.buffers.map((row) => row.key));
      return {
        status: 'committed',
        buffers: [
          { key: 'outline', status: 'unchanged', action: null, ref: null,
            revision: null, content_hash: null, message: null },
          { key: DOC_A, status: 'committed', action: 'edit-document',
            ref: SESSION_REF, revision: 'rev-1',
            content_hash: UPPERCASE_IDENTITY, message: null },
        ],
      };
    },
  });
  await controller.loadDocumentForEditing(DOC_A);
  await controller.edit(DOC_A, '# Document A edited\n');
  const outcome = await controller.saveDocument(DOC_A);
  const buffer = controller.state().buffers[DOC_A];
  const note = controller.elements().eventNote();
  // THE SENTENCE THE CANVAS SHOULD BE SHOWING, assembled from the two modules
  // that own its halves: the adopting module's own refusal for this identity,
  // wrapped in the canvas's own exported reason. Nothing here is transcribed,
  // so a reword of either half moves the expectation with the code.
  let adoptDetail = null;
  try {
    adoptSavedBase(buffer, { ref: SESSION_REF, revision: 'rev-1',
                             content_hash: UPPERCASE_IDENTITY });
  } catch (error) {
    adoptDetail = String(error && error.message);
  }
  const read = {
    seen,
    expectedError: unadoptedCommitReason(adoptDetail),
    adoptDetail,
    ok: outcome.ok === true,
    error: outcome.error,
    status: outcome.status,
    unadopted: (outcome.unadopted || []).map((row) => row.key),
    rows: outcome.buffers.map((row) => ({ key: row.key, status: row.status })),
    dirtyA: buffer.dirty,
    contentA: buffer.content,
    baseRefA: buffer.base_ref,
    baseHexA: buffer.base_hash.hex,
    statusA: String(controller.elements().status(DOC_A).textContent),
    eventNoteText: String(note.textContent),
    eventNoteHidden: note.hidden === true,
    // the scope key must not have followed a ref nothing was adopted onto
    ref: controller.state().key.ref,
  };
  controller.destroy();
  return read;
}

// ---- …and a seam that THREW is not a tile success either ----------------
//
// The other half of the same `ok` computation, and the half no row can speak
// for: when the seam throws, `save()` returns before any buffer row exists at
// all -- `{status: "refused", reason}` and nothing else. `ok` is false there
// only because it also requires the whole-Save status to be a landing, which is
// the clause that has no pin of its own: drop it and every rowless answer (a
// thrown seam, a destroyed canvas, an unloaded one) reads as a tile SUCCESS.
async function throwingSeamIsNotOk() {
  const boom = 'the console lost the gate mid-request';
  const { controller } = await mount({
    save: async () => { throw new Error(boom); },
  });
  await controller.loadDocumentForEditing(DOC_A);
  await controller.edit(DOC_A, '# Document A edited\n');
  const outcome = await controller.saveDocument(DOC_A);
  const buffer = controller.state().buffers[DOC_A];
  const read = {
    boom,
    ok: outcome.ok === true,
    error: outcome.error,
    status: outcome.status,
    reason: outcome.reason,
    // there are no rows to reason from: this is the rowless answer
    rows: outcome.buffers === undefined ? null : outcome.buffers,
    dirtyA: buffer.dirty,
    contentA: buffer.content,
    statusA: String(controller.elements().status(DOC_A).textContent),
  };
  controller.destroy();
  return read;
}

// ---- two loaded documents sharing a basename stay distinguishable --------
async function basenameCollision() {
  const { controller } = await mount();
  await controller.loadDocumentForEditing(COLLIDE_A);
  const beforeSecond = controller.loadedBuffers().map((row) => row.label);
  await controller.loadDocumentForEditing(COLLIDE_B);
  const labels = controller.loadedBuffers().map((row) => row.label);
  return {
    beforeSecond, labels,
    names: [COLLIDE_A, COLLIDE_B].map(
      (k) => controller.elements().status(k).getAttribute('aria-label')),
    textareaNames: [COLLIDE_A, COLLIDE_B].map(
      (k) => controller.elements().textarea(k).getAttribute('aria-label')),
    // the CSS fragments are distinct too, because a path is not a class name
    classes: [COLLIDE_A, COLLIDE_B].map(
      (k) => String(controller.elements().status(k).className)),
  };
}

// ---- loading a path already loaded SELECTS it and re-reads nothing -------
async function alreadyLoaded() {
  const { controller } = await mount();
  await controller.loadDocumentForEditing(DOC_A);
  await controller.edit(DOC_A, '# unsaved work in A\n');
  await controller.loadDocumentForEditing(DOC_B);   // move the selection away
  const again = await controller.loadDocumentForEditing(DOC_A);
  return {
    again,
    active: controller.activeBuffer(),
    content: controller.state().buffers[DOC_A].content,
    dirty: controller.state().buffers[DOC_A].dirty,
    keys: controller.bufferKeys(),
  };
}

// ---- R1: ONE loaded-set notify per switch, whichever shape the switch is ----
// `switchDocument` fires the tail only when `setActiveBuffer` did not already do
// it, because `setActiveBuffer` early-returns on an already-active key. That
// dedupe is behaviourally right on every shape and was completely unpinned:
// dropping the condition restores the double, inverting it fires zero on one
// shape and twice on the other, and dropping the tail loses it entirely. All
// four shapes are counted here on the injected notification itself.
async function switchNotifyCounts() {
  const counts = {};

  // CROSS-KEY. The reserved slot is unbacked and the OUTLINE is selected, so the
  // switch MOVES the selection onto the reserved key and `setActiveBuffer` owns
  // the tail.
  {
    const notified = [];
    const { controller } = await mount({
      onLoadedSetChanged: () => notified.push(1) });
    notified.length = 0;
    const result = await controller.selectDocument(DOC_A);
    counts.crossKey = { notifies: notified.length, status: result.status,
                        active: controller.activeBuffer() };
  }

  // SAME-KEY CONTENT SWITCH. The reserved slot is BACKED and already selected, so
  // the selection does not move -- `setActiveBuffer` early-returns and says
  // nothing -- but the buffer's whole CONTENT is replaced, which the wheel and
  // the selector must still hear. This is the shape the conditional tail exists
  // for, and the one an unconditional dedupe would silence.
  {
    const notified = [];
    const { controller } = await mount({
      activeDocumentPath: DOC_A,
      onLoadedSetChanged: () => notified.push(1) });
    controller.setActiveBuffer('document');
    notified.length = 0;
    const result = await controller.selectDocument(DOC_B);
    counts.sameKey = { notifies: notified.length, status: result.status,
                       active: controller.activeBuffer(),
                       content: controller.state().buffers.document.content };
  }

  // UNCHANGED, same path AND already the selected key. Nothing moves and nothing
  // is replaced, so nothing is announced -- this route never reaches
  // `switchDocument` at all.
  {
    const notified = [];
    const { controller } = await mount({
      activeDocumentPath: DOC_A,
      onLoadedSetChanged: () => notified.push(1) });
    controller.setActiveBuffer('document');
    notified.length = 0;
    const result = await controller.selectDocument(DOC_A);
    counts.unchangedSameKey = { notifies: notified.length, status: result.status };
  }

  // UNCHANGED path, but the OUTLINE is selected. Choosing it is still an act of
  // BINDING even though no content moves, so it is announced exactly once.
  {
    const notified = [];
    const { controller } = await mount({
      activeDocumentPath: DOC_A,
      onLoadedSetChanged: () => notified.push(1) });
    notified.length = 0;
    const result = await controller.selectDocument(DOC_A);
    counts.unchangedFromOutline = { notifies: notified.length,
                                    status: result.status,
                                    active: controller.activeBuffer() };
  }

  return counts;
}

console.log(JSON.stringify({
  thirdDocument: await thirdDocument(),
  unheldKey: await unheldKey(),
  boundRefusal: await boundRefusal(),
  switchNotifyCounts: await switchNotifyCounts(),
  dirtyUnload: await dirtyUnload(),
  unbackedSlotInert: await unbackedSlotInert(),
  outlineStaysReserved: await outlineStaysReserved(),
  tileSave: await tileSave(),
  contextOnlyTileSave: await contextOnlyTileSave(),
  refusedAncestry: await refusedAncestryLeadsTheSummary(),
  cleanOutlineLead: await cleanOutlineDoesNotTakeTheLead(),
  vacuousRowLead: await vacuousRowNeverLeads(),
  nothingToSay: await nothingToSayTakesNoLine(),
  unadoptableIdentity: await unadoptableIdentityThroughTheRealOrchestrator(),
  unadoptableRow: await committedRowThisCanvasCannotAdopt(),
  throwingSeam: await throwingSeamIsNotOk(),
  basenameCollision: await basenameCollision(),
  alreadyLoaded: await alreadyLoaded(),
}));
"""


@pytest.fixture(scope="module")
def loaded_set_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench loaded-set probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-loaded-set")
    views = tmp_path / "views"
    shutil.copytree(EDITOR_JS.parent, views)
    shutil.copytree(EDITOR_JS.parent.parent / "vendor", tmp_path / "vendor")
    (tmp_path / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (tmp_path / "vendor" / "package.json").write_text(
        '{"type": "commonjs"}', encoding="utf-8")
    harness = views / "loaded-set-harness.mjs"
    harness.write_text(_LOADED_SET_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=120)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_third_loaded_document_is_a_first_class_buffer(loaded_set_results):
    """add-doxbench-editing-phase-b, "A second document is loaded" and "The
    buffer set widens": a document the human loads gets its OWN key, its own
    editor, its own preview, its own live status region and its own dirty state
    — and loading it replaces, discards and flushes nothing."""
    result = loaded_set_results["thirdDocument"]
    for row in result["results"]:
        assert row["ok"] is True, row
        assert row["already_loaded"] is False, row
    # the outline first, then the documents in the declared lexicographic order
    # (the reserved unbacked `document` slot the mount always builds sorts first
    # among them, because the rule is a plain ascending comparison of the key)
    assert result["keys"] == [
        "outline",
        "document",
        "ideation/staging/topic-x/detail.md",
        "ideation/staging/topic-x/second.md",
        "ideation/staging/topic-x/third.md",
    ]
    assert result["textareas"] == 5
    assert result["previews"] == 5
    assert result["statuses"] == 5
    # each buffer's own dirty state, and only the edited one is dirty
    assert result["dirty"]["ideation/staging/topic-x/second.md"] is True
    assert result["dirty"]["ideation/staging/topic-x/third.md"] is False
    assert result["dirty"]["outline"] is False
    # the third document's own live status region names it and reports it
    assert result["statusC"]["hidden"] is False
    assert result["statusC"]["name"] == "third.md buffer status"
    assert "third.md: no unsaved changes" == result["statusC"]["text"]
    assert "second.md: unsaved changes" == result["statusB"]["text"]
    assert "doxbench-sronly" in result["statusC"]["cls"]
    # …and the texts did not bleed between buffers
    assert result["contentB"] == "# Document B edited\n"
    assert result["contentC"] == "# Document C\n"
    # loading selects, so the last load is the selected buffer
    assert result["active"] == "ideation/staging/topic-x/third.md"


def test_set_active_buffer_refuses_a_key_the_canvas_does_not_hold(
    loaded_set_results,
):
    """The widened form of Phase A's enumeration guard. Membership is a question
    about the STATE, so an in-scope path that was never LOADED is refused exactly
    as a misspelling is — which is strictly more than the old
    `BUFFER_KINDS.includes(...)` refused, since that constant would have
    accepted neither and rejected both for the wrong reason."""
    result = loaded_set_results["unheldKey"]
    assert "must name a buffer this canvas holds" in result["refusal"]
    assert "must name a buffer this canvas holds" in result["typoRefusal"]
    # a refused selection moves nothing
    assert result["activeAfterRefusal"] == "ideation/staging/topic-x/detail.md"
    # …and a key the canvas DOES hold is accepted, including the reserved outline
    assert result["heldAccepted"] == "ideation/staging/topic-x/detail.md"
    assert result["outlineAccepted"] == "outline"


def test_the_loaded_set_bound_refuses_with_the_measured_number(
    loaded_set_results,
):
    """add-doxbench-editing-phase-b, "The loaded-set bound is reached": the load
    refuses, STATES the measured bound, and evicts nothing — because every loaded
    buffer may hold unsaved work, so making room would be discarding human
    text."""
    result = loaded_set_results["boundRefusal"]
    assert result["first"]["ok"] is True
    assert result["second"]["ok"] is True
    third = result["third"]
    assert third["ok"] is False
    assert third["key"] is None
    assert third["refusal"] == "loaded_set_bound_reached"
    # the MEASURED numbers, in the sentence. The reserved unbacked slot every
    # mount builds counts toward the bound, because it is a buffer that may hold
    # unsaved work — which is exactly what the bound protects.
    assert third["measured"] == 3
    assert third["bound"] == 3
    assert third["error"] == result["expected"]
    assert "already holds 3 documents" in third["error"]
    assert "declared bound of 3" in third["error"]
    # nothing was evicted to make room
    assert result["keys"] == [
        "outline",
        "document",
        "ideation/staging/topic-x/detail.md",
        "ideation/staging/topic-x/second.md",
    ]
    # …and the refusal is VISIBLE, not only returned
    assert "refused" in result["eventNote"]
    # the loaded-set notification fired for the two loads and not for the refusal
    assert result["notified"][-1] == 2


def test_unloading_a_dirty_document_refuses_until_the_discard_is_explicit(
    loaded_set_results,
):
    """add-doxbench-editing-phase-b, "A dirty document is unloaded": the unload
    refuses or requires an explicit discard, and MUST NOT silently drop the
    text."""
    result = loaded_set_results["dirtyUnload"]
    assert result["refused"]["ok"] is False
    assert result["refused"]["refusal"] == "unsaved_edits"
    assert "unloading it would drop them" in result["refused"]["error"]
    # the buffer is exactly as it was
    assert result["afterRefusal"]["content"] == "# Document A edited\n"
    assert result["afterRefusal"]["dirty"] is True
    assert "ideation/staging/topic-x/detail.md" in result["afterRefusal"]["keys"]
    # the explicit discard is honoured, and the selection returns to the outline
    assert result["discarded"]["ok"] is True
    assert result["keysAfter"] == ["outline", "document"]
    assert result["activeAfter"] == "outline"
    # the unloaded region says nothing rather than standing there stale
    assert result["statusHidden"] is True
    assert result["statusText"] == ""
    # …and a re-load reuses the same nodes and reads the document afresh
    assert result["reloaded"]["ok"] is True
    assert result["contentAfterReload"] == "# Document A\n"


def test_the_unbacked_create_slot_has_nothing_to_unload(loaded_set_results):
    """AMENDMENT 2 kept exactly one non-outline withholding, and changed its
    reason to the true one.

    The reserved `document` key can hold two very different things. BACKED, it is
    the tile's own document and it now unloads like any other (pinned end to end
    in `test_doxbench_composition.py`). UNBACKED, it is the create flow's
    not-yet-created artifact: a held buffer with a null path, which
    `loadedBuffers` filters out and the selector never lists, because it is not a
    member of the loaded set at all. There is no membership for Unload to end, so
    the control is inert and says so — and it says the true thing, not the
    retired "reserved buffer a turn falls back on".

    Cancel is the control that acts on this buffer. Unload has no subject."""
    result = loaded_set_results["unbackedSlotInert"]
    before = result["before"]
    assert before["path"] is None, "the mount must leave the slot unbacked"
    assert before["listed"] == [], (
        "an unbacked slot is not a loaded document, and is not listed")
    # Inert-and-stated, never absent — the same posture the outline gets.
    assert before["rendered"] is True
    assert before["disabled"] is True
    assert "nothing to unload" in before["title"]
    assert "has not been created yet" in before["title"]
    # …and the reason is VISIBLE text beside it, not only a hover title.
    assert before["noteHidden"] is False
    assert before["noteText"] == before["title"]
    # The retired sentence must not come back with it.
    assert "never unloaded" not in before["title"], (
        "Amendment 2: only the outline is never unloaded")
    # Pressing it changes nothing: the click path re-derives the same rule.
    assert result["keysAfter"] == ["outline", "document"]
    assert result["activeAfter"] == "document"


def test_the_outline_reservation_survives_the_narrowed_rule(loaded_set_results):
    """The other half of Amendment 2, measured at the canvas module: narrowing
    the reserved set to the outline must not narrow it past the outline.

    "only the outline can never unload. we always want that to be loaded." Three
    layers still say so and this pins all three — the control is inert with the
    reason stated, its click path refuses, and the controller's public
    `unloadDocument` hard-refuses the key whatever any surface does."""
    result = loaded_set_results["outlineStaysReserved"]
    posture = result["posture"]
    assert posture["rendered"] is True, (
        "inert-and-stated, never absent — an absent control answers nothing")
    assert posture["disabled"] is True
    assert "never unloaded" in posture["title"]
    assert "reserved buffer" in posture["title"]
    assert posture["noteText"] == posture["title"]
    # The press changed nothing, and the loaded document beside it is untouched.
    assert "outline" in result["keysAfter"]
    assert "ideation/staging/topic-x/detail.md" in result["keysAfter"]
    # …and the controller refuses the key directly, below any surface.
    assert result["refusal"]["ok"] is False
    assert "reserved for this scope and cannot be unloaded" in (
        result["refusal"]["error"])


def test_the_tile_save_persists_its_document_and_the_ancestry_step_only(
    loaded_set_results,
):
    """add-doxbench-editing-phase-b design D4, and the `docs`-tile requirement:
    the tile Save runs the SAME pipeline restricted to that document plus the
    outline-ancestry step, MUST NOT persist another loaded document the human is
    not looking at, and reports every buffer it acted on per buffer.

    Driven through the REAL `doxbench-save.js`, so the scope is the
    orchestrator's own `only` and not a fixture's opinion of it."""
    result = loaded_set_results["tileSave"]
    # exactly two governed actions, the outline FIRST as ancestry
    assert [call["document"] for call in result["calls"]] == [
        "ideation/staging/topic-x/topic-x.md",
        "ideation/staging/topic-x/detail.md",
    ]
    assert [call["kind"] for call in result["calls"]] == ["outline", "document"]
    # the verdict is per buffer, and names ONLY the buffers it acted on
    rows = {row["key"]: row for row in result["outcome"]["buffers"]}
    assert sorted(rows) == ["ideation/staging/topic-x/detail.md", "outline"]
    assert rows["outline"]["status"] == "committed"
    assert rows["ideation/staging/topic-x/detail.md"]["status"] == "committed"
    assert result["outcome"]["ok"] is True
    # the document the human was NOT looking at is untouched and still dirty
    assert result["dirty"]["ideation/staging/topic-x/second.md"] is True
    assert result["contentB"] == "# Document B edited\n"
    assert "second.md: unsaved changes" == result["statusB"]
    # …while both buffers it DID act on report their own verdict
    assert "saved as edit-document" in result["statusA"]
    assert "saved as edit-document" in result["statusOutline"]
    assert result["dirty"]["outline"] is False
    assert result["dirty"]["ideation/staging/topic-x/detail.md"] is False
    assert result["outlineBaseRef"] == "draft/topic-x"


def test_a_context_only_document_loads_but_has_no_reachable_tile_save(
    loaded_set_results,
):
    """add-doxbench-editing-phase-b design D2 and "A context-only document is
    loaded": an inherited document is loadable for grounding, carries
    `owned: false`, and its tile Save states its absence rather than reaching a
    governance action that would only refuse it."""
    result = loaded_set_results["contextOnlyTileSave"]
    assert result["loaded"]["ok"] is True
    assert result["owned"] == [
        {"key": "ideation/brainstorm/inherited.md", "owned": False}]
    assert result["refused"]["ok"] is False
    assert "read-only context" in result["refused"]["error"]
    # nothing reached the governed action at all
    assert result["calls"] == []


def test_the_one_visible_save_line_leads_with_the_first_failing_cause(
    loaded_set_results,
):
    """R-5 (openxFactory #81): the operator MUST read the ROOT, not a
    consequence of it.

    A partial/refused ordered Save produces one row per buffer in SAVE ORDER,
    and when the ancestry step is the thing that failed, every document behind
    it is `not_attempted` *because of it*. There is exactly ONE transient
    visible line, so the row it carries is a choice — and the only truthful
    choice is the FIRST failing row in save order, the cause the other rows are
    consequences of. Leading with a downstream row hands the human the
    missing-ancestry sentence and never names the refusal that produced it.

    Asserted as the SEMANTIC, not as a sentence: the visible line must be the
    lead row's own stated outcome, which is exactly the opening of that
    buffer's own durable status region — and must not be any later row's.
    Nothing is hidden by the choice: every row keeps its own sr-only sentence,
    which is what the per-buffer reporting rule (FR-035) requires.
    """
    result = loaded_set_results["refusedAncestry"]
    rows = result["outcome"]["buffers"]
    withheld = [row for row in rows
                if row["status"] in ("refused", "not_attempted")]
    # the shape this defect needs: a ROOT and its CONSEQUENCES, in save order
    assert [row["status"] for row in withheld] == [
        "refused", "not_attempted", "not_attempted"], rows
    lead, *downstream = withheld
    assert lead["key"] == "outline"
    note = result["eventNote"]
    assert result["eventNoteHidden"] is False
    assert note

    # THE LEAD. The visible line is the first failing row's own verdict — the
    # same sentence, attributed to the same buffer, that row's status region
    # opens with.
    statuses = result["statuses"]
    assert statuses[lead["key"]].startswith(note), (note, statuses)
    assert lead["message"] in note

    # …and it is NOT a downstream row's. Each consequence keeps its own
    # sentence in its own region, and none of them is what the human reads
    # first.
    for row in downstream:
        assert not statuses[row["key"]].startswith(note), (note, row)
        assert row["message"] not in note
        assert row["message"] in statuses[row["key"]]


def test_an_unchanged_row_never_takes_the_one_visible_save_line(
    loaded_set_results,
):
    """R-5 (openxFactory #81), the companion case: `unchanged` is not a report.

    RESHAPED by issue #291 (2026-08-24), which removed the row this scenario
    used to be built on. A tile Save scopes to one document, and the canvas
    hands the seam the buffers that CHANGED -- so a clean outline is not in the
    state `savePlanState` reshapes, and `saveBufferOrder` no longer invents the
    reserved key for it. The refused document is the only row there is.

    What the scenario still pins is the half that was always the point: the
    visible line is the REFUSED row's own verdict, it is the same sentence the
    tile verdict leads with, and the clean outline -- untouched by an act it was
    never part of -- states its own honest condition instead of a Save verdict.
    The vacuous-row lead itself is pinned on the scripted rows next door, which
    is where that shape now lives.
    """
    result = loaded_set_results["cleanOutlineLead"]
    statuses = [(row["key"], row["status"]) for row in result["rows"]]
    # the shape after #291: no verdict about a buffer the reshaped state does
    # not hold, so the real failure is the only row
    assert statuses == [("ideation/staging/topic-x/detail.md", "refused")], statuses

    note = result["eventNote"]
    # the line is the refused row's own verdict, the opening of its own region
    assert result["statusA"].startswith(note), (note, result["statusA"])
    # …and NOT the clean outline's "nothing to save in this buffer"
    assert "nothing to save" not in note, note
    assert not result["statusOutline"].startswith(note), (note, result)
    # the outline says what is TRUE of it -- it is clean -- rather than carrying
    # a verdict from a Save that neither sent it nor was asked about it
    assert result["statusOutline"] == "Outline: no unsaved changes", result
    # …and the line is the very sentence the tile verdict leads with (same set)
    assert result["tileError"] in note, (note, result["tileError"])


def test_a_vacuous_unchanged_row_never_takes_the_visible_line(
    loaded_set_results,
):
    """R-5 (openxFactory #81), the rule the scenario above used to carry.

    The canvas leads its ONE transient line from whatever rows a seam hands it,
    and `unchanged` is a declared per-buffer status. Handed a vacuous row FIRST
    and the real refusal behind it -- exactly the shape the orchestrator
    produced before issue #291 -- a lead chosen from "every row that is not
    `committed`" takes the vacuous row and the refusal never reaches the human.

    The line must come from the SAME set the tile verdict already uses -- the
    withheld rows, `refused` and `not_attempted` -- so that the two surfaces
    agree in fact and not only in the common case.
    """
    result = loaded_set_results["vacuousRowLead"]
    statuses = [(row["key"], row["status"]) for row in result["rows"]]
    # the shape this defect needs: a vacuous row FIRST, the real failure behind it
    assert statuses[0] == ("outline", "unchanged"), statuses
    refused = [row for row in result["rows"] if row["status"] == "refused"]
    assert len(refused) == 1, statuses

    note = result["eventNote"]
    # the line is the refused row's own verdict, the opening of its own region
    assert result["statusA"].startswith(note), (note, result["statusA"])
    # …and NOT the vacuous row's "nothing to save in this buffer"
    assert "nothing to save" not in note, note
    assert not result["statusOutline"].startswith(note), (note, result)
    # nothing is hidden by the choice: the vacuous row still states itself in
    # its OWN region, which is where the per-buffer report lives (FR-035)
    assert "nothing to save in this buffer" in result["statusOutline"], result
    # …and the line is the very sentence the tile verdict leads with (same set)
    assert result["tileError"] in note, (note, result["tileError"])


def test_a_save_with_nothing_withheld_leaves_the_visible_line_alone(
    loaded_set_results,
):
    """R-5 (openxFactory #81), Brett's ruling of 2026-08-24: a Save with
    nothing withheld says NOTHING on the one transient line.

    The third case in the family. A tile Save scopes to one document; before the
    lead was narrowed to the withheld set, the clean outline's vacuous
    `unchanged` row was "not committed" and took the line, so a fully SUCCESSFUL
    save flashed `Outline: nothing to save in this buffer` -- a report about the
    buffer the human did not act on, standing in for the one they did. Narrowing
    the lead realized the ruling; this pins it, because a ruled behaviour that
    nothing asserts is one refactor away from silently ceasing to hold.

    Issue #291 then removed the vacuous row itself, at its source: the clean
    outline is not in the state the seam is handed, so no verdict is stated
    about it. The ruling is unchanged and so is every assertion below it -- the
    row that could have taken the line is simply gone as well as ignored, which
    is a narrower fact than this test needs and never a wider one.

    The line going quiet is the absence of a PROBLEM, not the absence of a
    report, so the second half matters as much as the first: the committed
    buffer's own region must still state the outcome it committed under. A
    change that satisfied this test by reporting LESS would be the failure it
    exists to prevent.
    """
    result = loaded_set_results["nothingToSay"]
    rows = result["rows"]
    statuses = [(row["key"], row["status"]) for row in rows]
    # the shape: nothing withheld, and (since #291) no vacuous row either
    assert not [row for row in rows
                if row["status"] in ("refused", "not_attempted")], statuses
    assert not [row for row in rows if row["status"] == "unchanged"], statuses
    committed = [row for row in rows if row["status"] == "committed"]
    assert len(committed) == 1, statuses
    # the clean outline still states its own condition in its own region --
    # nothing was lost by not stating a verdict about it
    assert result["statuses"]["outline"] == "Outline: no unsaved changes", result

    # THE RULING: no visible line at all, and the region is hidden rather than
    # left showing an empty box.
    assert result["eventNoteText"] == "", result["eventNoteText"]
    assert result["eventNoteHidden"] is True, result

    # …and nothing was lost by the silence. The tile reports its success…
    assert result["ok"] is True, result
    assert result["error"] is None, result["error"]
    # …with the adoption result stated as EMPTY rather than omitted (#290): the
    # field is an array on every answer a seam returned, so no reader has to
    # tell "adopted everything" apart from an answer that never said. Making it
    # conditional on there being something to report passes every other test.
    assert result["unadopted"] == [], result["unadopted"]
    # …and the committed buffer's own region still states what it committed as
    # and where, which is the per-buffer report FR-035 requires.
    landed = result["statuses"][committed[0]["key"]]
    assert committed[0]["action"] in landed, (landed, committed[0])
    assert committed[0]["ref"] in landed, (landed, committed[0])


def test_an_identity_the_canvas_cannot_adopt_is_refused_before_it_is_committed(
    loaded_set_results,
):
    """openxFactory #290, arm 1: ONE identity rule, not two.

    The trigger is a VALIDATOR DIVERGENCE. `doxbench-save.js` used to accept any
    non-empty algorithm and any 64 characters as a stated identity, while
    `doxbench-state.js` -- the module that WRITES that identity into working
    state through `adoptSavedBase` -- accepts only a lowercase SHA-256 one. Two
    differently strict judges of the same value is not caution: an uppercase-hex
    or `sha512` answer passed the reader as `committed` and then threw in the
    writer, so the buffer kept its unsaved text while the tile reported success.

    The rule is therefore applied where the value is READ as well as where it is
    written: an identity the canvas could not adopt is not a commit this Save
    will report, and the refusal is stated in the row vocabulary that already
    exists (`refused`) with a message naming what was wrong. Nothing else moves
    -- the buffer keeps its text, its dirty flag and its base.
    """
    result = loaded_set_results["unadoptableIdentity"]
    # precondition: the act really did reach the transport, so this is a verdict
    # about a returned answer and not about a Save that never ran
    assert [c["document"] for c in result["calls"]] == [
        "ideation/staging/topic-x/detail.md"], result["calls"]

    # THE TILE. Never a success over a buffer that kept its unsaved text.
    assert result["ok"] is False, result
    assert result["error"], result
    row = [r for r in result["rows"] if r["key"] == "ideation/staging/topic-x/detail.md"]
    assert len(row) == 1, result["rows"]
    assert row[0]["status"] == "refused", row
    # the SAVE MODULE's own clause for "stated, but not in a form anything can
    # adopt" -- asserted as its exported constant, because a test that carries
    # its own copy of a sentence stops describing the module the moment the
    # module is reworded, and goes on passing while it does
    assert result["identityNotAdoptable"] in row[0]["message"], row

    # …and the tile's one line is the buffer's OWN sentence, so the two surfaces
    # cannot contradict each other whatever else changes.
    assert result["error"] in result["statusA"], result
    assert result["statusA"].endswith("unsaved changes"), result["statusA"]
    assert result["eventNote"], "a refusal must reach the one visible line"
    assert result["error"] in result["eventNote"], result

    # NOTHING WAS ADOPTED. The text is the human's, the buffer is still dirty,
    # and the base was not advanced onto an identity nothing can verify later.
    assert result["dirtyA"] is True
    assert result["contentA"] == "# Document A edited\n"
    assert result["baseHexA"] != "A" * 64, result["baseHexA"]


def test_a_commit_the_canvas_cannot_adopt_never_reads_as_a_tile_success(
    loaded_set_results,
):
    """openxFactory #290, arm 2: the ADOPT-FAILURE BRANCH itself.

    Arm 1 closes the one trigger the issue identified. This closes the branch,
    which had no coverage at all: the save seam is INJECTED, so a `committed`
    row the state module refuses is constructible whatever the orchestrator does
    with identities, and `tileSaveVerdict` computed `ok` from the outcome ROWS
    alone -- rows that say `committed`, because the server did commit. The
    canvas's own failure to adopt was known only to `save()`, so the tile
    reported `ok: true, error: null` while the buffer's own status region said
    "this buffer keeps its unsaved text".

    The verdict therefore CONSUMES the adoption result: a commit this canvas
    could not adopt is a failed tile Save, stated in the same sentence the
    buffer's own region carries. What must NOT change with it: the row keeps
    saying `committed`, because that is what the SERVER did and rewriting it
    would be a false statement about the governed action in the other direction.
    """
    result = loaded_set_results["unadoptableRow"]
    # precondition: exactly the shape the defect needs -- a row the orchestrator
    # calls `committed` that the state module refuses to adopt
    assert result["seen"] == [["ideation/staging/topic-x/detail.md"]], result["seen"]
    assert result["status"] == "committed", result
    by_key = {row["key"]: row["status"] for row in result["rows"]}
    assert by_key["ideation/staging/topic-x/detail.md"] == "committed", by_key

    # THE VERDICT. Not ok, and the reason is the adoption failure itself --
    # asserted as the sentence the two owning modules BUILD (the state module's
    # own refusal for this identity, inside the canvas's exported reason), never
    # as a phrase copied into this file.
    assert result["ok"] is False, result
    assert result["adoptDetail"], "the state module must refuse this identity"
    assert result["error"] == result["expectedError"], result
    assert result["unadopted"] == ["ideation/staging/topic-x/detail.md"], result

    # …and it is WORD FOR WORD the buffer's own durable sentence, which is the
    # contradiction the issue reported: the tile claimed success while this
    # region said the text was still unsaved.
    assert result["error"] in result["statusA"], result
    assert result["statusA"].endswith("unsaved changes"), result["statusA"]
    # …and the one visible line carries it too, rather than staying silent about
    # the only thing that went wrong.
    assert result["eventNoteHidden"] is False, result
    assert result["error"] in result["eventNoteText"], result

    # NOTHING MOVED. No base, no key, no dirty flag -- an unadopted commit
    # advances none of them.
    assert result["dirtyA"] is True
    assert result["contentA"] == "# Document A edited\n"
    assert result["baseRefA"] == "main"
    assert result["baseHexA"] != "A" * 64, result["baseHexA"]
    assert result["ref"] == "main", result["ref"]


def test_a_save_seam_that_threw_is_never_a_tile_success(loaded_set_results):
    """openxFactory #290, the rowless half of the same verdict.

    `tileSaveVerdict` reads two things: the failing causes among the rows, and
    the whole-Save status. The rows are what the adopt fix taught it to read
    properly -- but a Save whose SEAM THREW has no rows at all. `save()` catches
    the throw, tells every buffer it was handed, and returns
    `{status: "refused", reason}` with no `buffers` key, so "no failing causes"
    is trivially true of it. What makes the tile answer honestly there is the
    OTHER clause, that the whole-Save status must itself be a landing --
    `committed` or `unchanged`.

    That clause was load-bearing and unpinned: dropping it passes the whole
    suite while turning every rowless answer (a thrown seam, a destroyed canvas,
    an unloaded one) into `ok: true` on the tile. It is pinned here at the
    shape that reaches a human first -- a governed Save that could not be
    performed at all -- and the buffer keeps its text, which is the fact the
    tile must not contradict.
    """
    result = loaded_set_results["throwingSeam"]
    # the precondition that makes this test what it claims to be: NO rows
    assert result["rows"] is None, result["rows"]
    assert result["status"] == "refused", result

    assert result["ok"] is False, result
    assert result["error"], result
    # the reason names what actually happened, and reaches the buffer's region
    assert result["boom"] in result["error"], result
    assert result["error"] == result["reason"], result
    assert result["boom"] in result["statusA"], result["statusA"]

    # …and the human's text is untouched, which is why a success would be a lie
    assert result["dirtyA"] is True
    assert result["contentA"] == "# Document A edited\n"


def test_two_loaded_documents_sharing_a_basename_stay_distinguishable(
    loaded_set_results,
):
    """add-doxbench-editing-phase-b, "Two loaded documents share a basename":
    the surface MUST distinguish them. The declared rule is the shortest
    trailing path suffix that no other loaded document shares, applied to the
    WHOLE set — so the second `README.md` lengthens the first one's label as
    well as its own."""
    result = loaded_set_results["basenameCollision"]
    # alone, the basename is unambiguous and that is what shows
    assert result["beforeSecond"] == ["README.md"]
    # together, both lengthen — and neither is left ambiguous
    assert result["labels"] == ["alpha/README.md", "beta/README.md"]
    assert result["names"] == ["alpha/README.md buffer status",
                              "beta/README.md buffer status"]
    assert result["textareaNames"] == ["alpha/README.md buffer text",
                                       "beta/README.md buffer text"]
    # and the CSS fragments are distinct, because a path is not a class name
    first, second = result["classes"]
    assert first != second
    for cls in (first, second):
        assert "/" not in cls
        assert "doxbench-status " in cls + " "


def test_loading_a_document_already_loaded_selects_it_and_re_reads_nothing(
    loaded_set_results,
):
    """add-doxbench-editing-phase-b, "A document already loaded is loaded
    again": that buffer becomes the selected one and MUST NOT be reloaded from
    source, because reloading would silently discard its unsaved text."""
    result = loaded_set_results["alreadyLoaded"]
    assert result["again"]["ok"] is True
    assert result["again"]["already_loaded"] is True
    assert result["again"]["key"] == "ideation/staging/topic-x/detail.md"
    assert result["active"] == "ideation/staging/topic-x/detail.md"
    # the unsaved text survived the second load verb exactly
    assert result["content"] == "# unsaved work in A\n"
    assert result["dirty"] is True
    # …and no second buffer claimed the same path
    assert result["keys"].count("ideation/staging/topic-x/detail.md") == 1


def test_the_slot_does_not_swap_where_the_gate_capability_is_absent(
        editor_results):
    """Amendment 1: "Where the gate capability is absent the slot SHALL keep its
    Save and Cancel posture unchanged and MUST NOT swap to Unload, because a
    surface that cannot save must go on saying so."

    Nothing is dirty here, which is exactly the state that shows Unload on a
    gated canvas — so this is the state where a missing carve-out would be
    invisible. An ungated surface has no reachable editing and is therefore never
    dirty, which means an unconditional swap would have made Save's stated
    absence unreachable for good rather than merely sometimes.

    Driven at the CANVAS MODULE, which is where the clause reaches: through the
    shipped shell a gate-off console renders no canvas controls at all."""
    gate_off = editor_results["gateAbsentSlot"]
    assert gate_off["anythingDirty"] is False, (
        "the probe must stand in the state that would otherwise show Unload")
    assert gate_off["unloadHidden"] is True, (
        "an ungated canvas must not swap its stated Save absence for an Unload")
    assert gate_off["saveHidden"] is False
    assert gate_off["cancelHidden"] is False
    assert gate_off["saveDisabled"] is True


def test_a_save_in_flight_keeps_the_pair_on_screen(editor_results):
    """Amendment 1's `!saving` half. While the bytes are in flight the buffers
    are about to stop being dirty but have not yet, so swapping the slot mid-Save
    would answer a question nobody asked — and would offer an unload of a buffer
    whose verdict has not landed. Both controls stay, both inert; the swap
    happens only once the Save settles and the canvas is genuinely clean."""
    flight = editor_results["saveInFlightSlot"]
    # dirty, pre-Save: the pair is up
    assert flight["dirty"]["saveHidden"] is False
    assert flight["dirty"]["unloadHidden"] is True
    # in flight: still the pair, and both inert
    assert flight["inFlight"]["unloadHidden"] is True, (
        "a Save in flight must not swap the slot to Unload")
    assert flight["inFlight"]["saveHidden"] is False
    assert flight["inFlight"]["cancelHidden"] is False
    assert flight["inFlight"]["saveDisabled"] is True
    assert flight["inFlight"]["cancelDisabled"] is True
    # settled and clean: NOW it swaps
    assert flight["settled"]["anythingDirty"] is False
    assert flight["settled"]["unloadHidden"] is False
    assert flight["settled"]["saveHidden"] is True


def test_one_loaded_set_notify_per_switch_whichever_shape(loaded_set_results):
    """R1 (adversarial review): `switchDocument`'s tail is CONDITIONAL, because
    `setActiveBuffer` early-returns on an already-active key and therefore does
    not always announce the change itself. The condition was behaviourally right
    on every shape and pinned by nothing — three mutations at that one line
    survived the whole suite.

    The two switch shapes are genuinely different and both must announce ONCE:

    * CROSS-KEY — the selection moves onto the reserved key, so `setActiveBuffer`
      announces and the conditional tail must stay quiet, or the wheel redraws
      twice (F9's double, live-reachable through the shell on the first fill of
      an unbacked reserved slot).
    * SAME-KEY CONTENT SWITCH — the selection does not move, so `setActiveBuffer`
      says nothing and the conditional tail is the ONLY announcement; silence
      here leaves the wheel and the selector describing the previous document.

    And the two no-op shapes differ from each other too: re-selecting the path
    already in the reserved slot announces nothing when that key is already
    selected, but still announces once when the binding moves off the outline."""
    counts = loaded_set_results["switchNotifyCounts"]

    cross = counts["crossKey"]
    assert cross["status"] == "switched"
    assert cross["active"] == "document"
    assert cross["notifies"] == 1, (
        f"a cross-key switch must announce once, saw {cross['notifies']}")

    same = counts["sameKey"]
    assert same["status"] == "switched"
    assert same["active"] == "document"
    # the buffer really did take the new document's content
    assert "Document B" in same["content"]
    assert same["notifies"] == 1, (
        f"a same-key content switch must announce once, saw {same['notifies']}")

    unchanged = counts["unchangedSameKey"]
    assert unchanged["status"] == "unchanged"
    assert unchanged["notifies"] == 0, (
        "re-selecting the already-selected path moves and replaces nothing")

    rebound = counts["unchangedFromOutline"]
    assert rebound["status"] == "unchanged"
    assert rebound["active"] == "document"
    assert rebound["notifies"] == 1, (
        "binding off the outline is a selection change and must be announced")
