"""Browser-session namespace and recovery for pure doxBench working state."""

from __future__ import annotations

import json
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
# the API driven below (`mountDoxBenchCanvas`, `DOXBENCH_BUFFER_TABS`,
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
  DOXBENCH_BUFFER_TABS,
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

  controller.setActiveTab('outline');
  const outlineArea = controller.elements().textarea('outline');
  outlineArea.selectionStart = 2; outlineArea.selectionEnd = 5; outlineArea.scrollTop = 10;
  outlineArea.focus();
  const outlineViewAfterFocus = controller.viewState('outline');

  controller.setActiveTab('document');
  const documentArea = controller.elements().textarea('document');
  documentArea.selectionStart = 1; documentArea.selectionEnd = 3; documentArea.scrollTop = 20;
  const documentViewNoFocus = controller.viewState('document');
  const activeElementAfterSwitchNoFocus = describeEl(globalThis.document.activeElement);

  controller.setActiveTab('outline');
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
  globalThis.document.activeElement = null;
  controller.setActiveTab('document');
  const afterDoc = describeEl(globalThis.document.activeElement);
  controller.setActiveTab('outline');
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
  controller1.setActiveTab('document');
  controller1.destroy();

  const calls2 = [];
  const controller2 = mountDoxBenchCanvas(new Node('div'), projection, {
    loadSource: makeLoadSource(CONTENT, calls2), storage, previewDelayMs: 5,
  });
  await controller2.ready;
  const restoredState = controller2.state();
  const restoredTab = controller2.activeTab();
  controller2.destroy();

  const differentKeyProjection = makeProjection({ key: { tile_id: 'topic-y' } });
  const calls3 = [];
  const controller3 = mountDoxBenchCanvas(new Node('div'), differentKeyProjection, {
    loadSource: makeLoadSource(CONTENT, calls3), storage, previewDelayMs: 5,
  });
  await controller3.ready;
  const freshState = controller3.state();
  const freshTab = controller3.activeTab();

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
  await controller.edit('document', '# dirty for guard focus\n');
  await controller.selectDocument(DOC_B);
  const focusedOnShow = describeEl(globalThis.document.activeElement);
  await controller.resolveGuard('cancel');
  const focusedAfterCancel = globalThis.document.activeElement === controller.elements().textarea('document');

  const calls2 = [];
  const controller2 = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls2), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller2.ready;
  await controller2.edit('document', '# dirty for guard focus 2\n');
  await controller2.selectDocument(DOC_B);
  await controller2.resolveGuard('discard');
  const focusedAfterDiscard = globalThis.document.activeElement === controller2.elements().textarea('document');

  return { focusedOnShow, focusedAfterCancel, focusedAfterDiscard };
}

// S3: the document picker is the one way a human reaches selectDocument.
async function documentPickerScenario() {
  const calls = [];
  const controller = mountDoxBenchCanvas(new Node('div'), makeProjection(), {
    loadSource: makeLoadSource(CONTENT, calls), storage: new FakeStorage(), previewDelayMs: 5,
  });
  await controller.ready;
  const picker = controller.elements().documentPicker();
  const optionValues = picker.children.map((opt) => opt.value);
  const initialValue = picker.value;

  // a clean switch: picker adopts the new path
  picker.value = DOC_B;
  await fireEvent(picker, 'change');
  const afterCleanSwitch = { value: picker.value, path: controller.state().buffers.document.path };

  // make it dirty, then attempt to switch back through the picker: blocked,
  // and the control must snap back to the CURRENT path, not the attempted one
  await controller.edit('document', '# dirty via picker test\n');
  picker.value = DOC_A;
  await fireEvent(picker, 'change');
  const afterBlockedAttempt = {
    value: picker.value,
    documentPath: controller.state().buffers.document.path,
    guardHidden: controller.elements().guard().hidden,
  };

  // resolve with Discard: the switch completes and the picker shows it
  await controller.resolveGuard('discard');
  const afterDiscardResolves = { value: picker.value, path: controller.state().buffers.document.path };

  return {
    optionValues, initialValue, afterCleanSwitch, afterBlockedAttempt, afterDiscardResolves,
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
  const tabBefore = controller.activeTab();
  controller.setActiveTab('document');
  const tabAfter = controller.activeTab();
  const stateAfter = controller.state().buffers.document;
  const storageAfter = JSON.stringify([...storage.values.entries()]);

  return {
    editResult, discardResult, selectResult, guardResult,
    tabUnchanged: tabBefore === tabAfter,
    stateContent: stateAfter.content,
    storageUnchanged: storageBefore === storageAfter,
  };
}

const previewCases = JSON.parse(readFileSync(process.argv[2], 'utf8'));

const results = {
  bufferTabs: DOXBENCH_BUFFER_TABS,
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
  typedOutlineOverridesEmpty: await typedOutlineOverridesEmptyScenario(),
  typedDocumentOverridesUnavailable: await typedDocumentOverridesUnavailableScenario(),
  outOfScopeSelectDocument: await outOfScopeSelectDocumentScenario(),
  accessibility: await accessibilityScenario(),
  guardFocus: await guardFocusScenario(),
  documentPicker: await documentPickerScenario(),
  postDestroyInert: await postDestroyInertScenario(),
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


def test_doxbench_buffer_tabs_are_exactly_outline_and_document(editor_results):
    """FR-004: the authoring canvas has exactly two primary buffers."""
    assert editor_results["bufferTabs"] == [
        {"key": "outline", "label": "Outline"},
        {"key": "document", "label": "Document"},
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
    `setActiveTab` round trips, and one buffer's values never bleed into the
    other's."""
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
    document picker — refuses autofill. The status line and heading stay
    direction-unset ON PURPOSE: status text is the fixed refusal/save
    vocabulary (it never echoes buffer content, by house rule) and the
    heading always leads with the LTR product name, so `dir="auto"` would
    resolve identically there and only imply a content-derivation that does
    not exist."""
    source = EDITOR_JS.read_text(encoding="utf-8")
    assert 'textarea.setAttribute("dir", "auto")' in source
    assert 'preview.setAttribute("dir", "auto")' in source
    assert 'textarea.setAttribute("autocomplete", "off")' in source
    assert 'picker.setAttribute("autocomplete", "off")' in source


def test_selected_tab_styling_rides_aria_selected_not_a_shadow_class():
    """T104 F9-6: the selected-tab look is owned by the
    `.doxbench-tab[aria-selected="true"]` rule (the T100 operator patch
    overrides every property the old `.doxbench-tab-active` rule set), so the
    class and the lockstep classList.toggle that maintained it were dead
    weight — a second spelling of the same state that could silently drift
    from the ARIA truth. Both are gone; selection state has exactly one
    spelling: `aria-selected`."""
    source = EDITOR_JS.read_text(encoding="utf-8")
    styles = (EDITOR_JS.parent.parent / "styles.css").read_text(encoding="utf-8")
    assert "doxbench-tab-active" not in source
    assert "doxbench-tab-active" not in styles


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
    """S1b (FR-001/SC-009): the mounted region is an accessible `region`
    whose name begins with the exact casing `doxBench`, and the visible
    heading states it too -- never `Doxbench`/`DoxBench`/`doxbench`."""
    result = editor_results["accessibility"]
    assert result["hostRole"] == "region"
    assert result["hostAriaLabel"].startswith("doxBench")
    assert "doxBench · Topic X" in result["hostTextContent"]
    visible = result["hostTextContent"]
    for wrong_casing in ("Doxbench", "DoxBench", "doxbench"):
        assert wrong_casing not in visible


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


def test_the_document_picker_reaches_select_document_and_reverts_when_blocked(
    editor_results,
):
    """S3 (T035 / acceptance scenario 4): the labelled document picker is
    the one way a human reaches selectDocument. A clean switch adopts the
    new path; a blocked switch snaps the control back to the CURRENT path
    until the guard resolves; resolving with Discard completes the switch
    and the control shows the new path."""
    result = editor_results["documentPicker"]
    assert set(result["optionValues"]) == {
        "ideation/staging/topic-x/detail.md",
        "ideation/staging/topic-x/second.md",
    }
    assert result["initialValue"] == "ideation/staging/topic-x/detail.md"

    assert result["afterCleanSwitch"]["value"] == "ideation/staging/topic-x/second.md"
    assert result["afterCleanSwitch"]["path"] == "ideation/staging/topic-x/second.md"

    blocked = result["afterBlockedAttempt"]
    assert blocked["guardHidden"] is False
    assert blocked["documentPath"] == "ideation/staging/topic-x/second.md"
    assert blocked["value"] == "ideation/staging/topic-x/second.md", (
        "the picker must snap back to the CURRENT path, not the attempted one"
    )

    resolved = result["afterDiscardResolves"]
    assert resolved["path"] == "ideation/staging/topic-x/detail.md"
    assert resolved["value"] == "ideation/staging/topic-x/detail.md"


def test_the_controller_is_fully_inert_after_destroy(editor_results):
    """S4: after destroy(), edit/discard/selectDocument/resolveGuard become
    stated refusals and setActiveTab is a no-op; nothing further persists."""
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

    assert (
        "const canvasOffered = !!scope && createGateLive(caps) && "
        "!sessionSurfaceHidden(caps) &&" in view
    )
    assert "!!active?.repository && !!active?.ref;" in view

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
                      'onIdentitySettled: () =>'):
        assert forwarded in view
    assert 'railController.refreshCurrency(' in view
    # T104 F2: the rail is handed the tile's USABLE documents (the scope
    # authority's own intersection), so a "no active document" refusal can name
    # one the operator could pick instead of dead-ending. Read from the
    # projection the canvas was mounted on -- the shell derives nothing here.
    assert 'documentCandidates: () => projection.active_document_candidates' in view
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

const { mountDoxBenchCanvas, SAVE_UNAVAILABLE_REASON } =
  await import('./doxbench-editor.js');

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

// A scripted seam. `verdicts` maps buffer kind -> outcome row; anything absent
// is reported committed. `gate` (optional) is awaited before answering, which is
// how the BUSY posture is observed mid-flight rather than inferred.
function seamFor(verdicts, { gate = null, calls = null } = {}) {
  return async (request) => {
    if (calls) calls.push(request);
    if (gate) await gate.promise;
    const rows = request.buffers.map((buffer) => {
      const scripted = verdicts[buffer.kind];
      if (scripted) return { kind: buffer.kind, ...scripted };
      return {
        kind: buffer.kind, status: 'committed', action: 'edit-document',
        ref: SESSION_REF, revision: 'newrev-' + buffer.kind,
        content_hash: identity(buffer.kind + 'saved'), message: null,
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
  const { controller, host, storage } = await mount({
    save: seamFor({}, { calls }) });
  await controller.edit('outline', '# Outline edited\n');
  await controller.edit('document', '# Document A edited\n');
  const before = controller.state();
  const outcome = await controller.save();
  const after = controller.state();
  return {
    calls, outcome,
    beforeDirty: { outline: before.buffers.outline.dirty,
                   document: before.buffers.document.dirty },
    afterBuffers: after.buffers,
    afterKey: after.key,
    status: { outline: describe(controller.elements().status('outline')),
              document: describe(controller.elements().status('document')) },
    saveBtn: { outline: describe(controller.elements().save('outline')),
               document: describe(controller.elements().save('document')) },
    hostText: host.textContent,
    storedKeys: [...storage.values.keys()],
    removedKeys: storage.removed,
  };
}

// ---- partial: outline commits, document refuses ---------------------------
async function partial() {
  const { controller, host } = await mount({
    save: seamFor({ document: {
      status: 'refused', action: 'edit-document', ref: null, revision: null,
      content_hash: null, message: 'the document base moved under this buffer' } }) });
  await controller.edit('outline', '# Outline edited\n');
  await controller.edit('document', '# Document A edited\n');
  const outcome = await controller.save();
  const after = controller.state();
  return {
    outcome, afterBuffers: after.buffers,
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
    save: describe(controller.elements().save('outline')),
    discard: describe(controller.elements().discard('outline')),
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
    after: { save: describe(controller.elements().save('outline')),
             discard: describe(controller.elements().discard('outline')),
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

// ---- the unwired posture, in this same harness ---------------------------
async function noSeam() {
  const { controller, host } = await mount({});
  await controller.edit('outline', '# Outline edited\n');
  const attempted = await controller.save();
  return {
    attempted,
    saveBtn: describe(controller.elements().save('outline')),
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
    buttons = save_seam_results["bothCommitted"]["saveBtn"]
    for kind in ("outline", "document"):
        assert buttons[kind]["disabled"] is False, kind
        assert buttons[kind]["ariaDisabled"] in (None, "false"), kind
    assert save_seam_results["saveUnavailableReason"] not in \
        save_seam_results["bothCommitted"]["hostText"]


# ---- what the seam is handed -------------------------------------------

def test_only_dirty_buffers_are_handed_to_the_save_seam(save_seam_results):
    """FR-031: Save persists only CHANGED buffers. The controller decides what
    is dirty; it does not decide order or action."""
    calls = save_seam_results["bothCommitted"]["calls"]
    assert len(calls) == 1, "one explicit Save is one call to the seam"
    kinds = sorted(b["kind"] for b in calls[0]["buffers"])
    assert kinds == ["document", "outline"]
    for buffer in calls[0]["buffers"]:
        assert buffer["dirty"] is True
        assert set(buffer) >= {"kind", "path", "content", "base_ref",
                               "base_revision", "base_hash", "dirty", "owned"}


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
    rows = {row["kind"]: row for row in result["outcome"]["buffers"]}
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
    after = save_seam_results["busy"]["after"]
    assert after["save"]["disabled"] is False
    assert after["discard"]["disabled"] is False
    assert after["status"]["busy"] in (None, "false")
    assert "saving" not in (after["status"]["text"] or "").lower()


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
    discardButtons: byText(/discard/i).length,
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
  // reports its unavailable state INLINE and the context/picker stays.
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
  const picker = controller.elements().documentPicker();
  output.outlineOnly = {
    ...survey(root),
    text: root.textContent.slice(0, 4000),
    pickerOptions: picker.children.length,
    pickerDisabled: picker.disabled === true,
    pickerLabel: picker.parentNode.textContent,
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
    assert view["discardButtons"] >= 1
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
    # the outline buffer still loaded and stays usable; the picker/context
    # survives the unavailable document rather than vanishing with it
    assert view["textareas"] >= 1 and view["textareasDisabled"] == 0
    assert view["selects"] >= 1
    assert view["discardButtons"] >= 1


def test_an_outline_only_tile_states_that_posture_instead_of_an_empty_picker(
        posture_results):
    """G-1 (PR #63 re-verification): on 16 of 21 real staged topics the tile's
    ONLY editable path is its own primary fragment, which this canvas loads as
    the OUTLINE and which T104 F2 therefore does not offer as a DOCUMENT. The
    picker used to render as an empty, enabled control that did nothing. It now
    STATES the posture — and the canvas stays fully usable, because chat
    grounds on the outline alone (`active_document_path: null`)."""
    view = posture_results["outlineOnly"]
    assert view["pickerOptions"] == 0
    assert view["pickerDisabled"] is True
    assert "only editable document" in view["pickerLabel"]
    # the Document buffer's own status says it too, instead of the misleading
    # "no document selected" (there is none to select)
    assert "no document selected" not in view["documentStatus"]
    assert "only editable document" in view["documentStatus"]
    assert view["documentPath"] is None
    # nothing is withheld: both buffers, Save/Discard and the preview remain
    assert view["textareas"] == 2 and view["textareasDisabled"] == 0
    assert view["discardButtons"] >= 1 and view["saveButtons"] >= 1


def test_gate_off_and_hidden_surfaces_withhold_the_canvas_at_the_shell():
    # Hosted/gate-off absence is enforced one level up: the shell never mounts
    # the canvas at all (the strongest "absent, not disabled").
    source = (EDITOR_JS.parent / "staging-workbench.js").read_text(encoding="utf-8")
    assert "createGateLive(caps)" in source
    assert "sessionSurfaceHidden(caps)" in source
    assert "canvas.hidden = !canvasOffered" in source
    assert "if (!canvasOffered) return;" in source


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
  return Promise.all(listeners.map((fn) => fn({ target: node })));
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
  loadSource: async (path) => ({
    content: '# ' + path + '\n\nloaded from main.\n',
    ref: 'main', revision: '1'.repeat(40) }),
  // the governed Save: the OUTLINE lands on a freshly opened session branch,
  // the DOCUMENT is refused, so its unsaved text is exactly what must survive
  // the re-key that follows
  save: async (request) => {
    saveRequests.push(request);
    return {
      status: 'committed',
      buffers: request.buffers.map((row) => (row.kind === 'outline'
        ? { kind: 'outline', status: 'committed', action: 'edit-document',
            ref: SESSION_REF, revision: '2'.repeat(40),
            content_hash: row.current_hash, message: null }
        : { kind: 'document', status: 'refused', action: 'edit-document',
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
const second = mountStagingWorkbench(reopened, snapshot, {
  caps,
  fetcher: async () => ({ ok: false }),
  active: { repository: 'fixture-repo', ref: SESSION_REF },
  index: { entries: [] },
  doxbench: emptyCatalogDoxbench,
  sourceBase: '/source/' + SESSION_REF + '/',
  edit: null,
  onSessionRekey: async () => null,
  onSessionEnded: async () => null,
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
