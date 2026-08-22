"""T029 (010-doxbench-editor-chat, US1): mutation-sentinel proof that the
doxBench editing/preview/tab-switch/Discard loop makes NO writes before Save.

Pins FR-008 ("Local buffer editing and preview MUST write no corpus, branch,
snapshot, register, manifest, or governance artifact before Save"), FR-009
("Discard MUST restore the applicable loaded or saved base without
persistence or a model call"), and SC-003 ("Across the mutation test matrix,
editing, preview, chat, Apply, Discard, model selection, and transcript
restoration produce zero corpus, branch, snapshot, register, manifest, or
governance writes before Save").

Two independent layers, mirroring tests/hermeticity.py's own "structural, not
per-test-discipline" argument:

  1. STATIC -- `doxbench-editor.js` and `doxbench-state.js` are grepped for
     every network/dynamic-import/filesystem primitive; each absence is its
     own assertion so a future addition fails on a named line, not a vague
     diff.
  2. BEHAVIOURAL -- a full US1 loop (load, edit both buffers, preview,
     switch tabs, hit the document-switch guard, resolve it twice, discard
     both buffers, refresh context) runs against traps standing in for
     `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`,
     `navigator.sendBeacon`, and `localStorage` that each RECORD the attempt
     and throw, and against a real scratch corpus directory used as the
     process `cwd` so a stray relative-path filesystem write would land
     somewhere this test can see it. The one companion node run backing
     every test in this module returns a single JSON object plus a
     before/after manifest of that scratch corpus, so the whole T029 set
     costs one process (`mutation_results` below).

`doxbench-editor.js` does not exist yet (Phase B builds it); every test here
is expected to fail RED until then.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

EDITOR_JS = (
    REPO_ROOT
    / "scripts"
    / "ideation_dashboard"
    / "web"
    / "views"
    / "doxbench-editor.js"
)
STATE_JS = (
    REPO_ROOT
    / "scripts"
    / "ideation_dashboard"
    / "web"
    / "views"
    / "doxbench-state.js"
)
VIEWER_JS = (
    REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views" / "viewer.js"
)
VENDOR_MARKDOWN_JS = (
    REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "vendor" / "markdown-it.min.js"
)
NODE = shutil.which("node")


# ---------------------------------------------------------------------------
# Item 1: static sentinels. Every absent primitive is its own assertion with
# a clear message, exactly as the brief for this task requires -- a future
# regression that adds ONE of these fails on a named line, not a vague diff.
# ---------------------------------------------------------------------------

_FORBIDDEN_NEEDLES = [
    ("fetch(", "a fetch( call"),
    ("doFetch", "an injected-fetcher transport seam (this slice has none)"),
    ("XMLHttpRequest", "an XMLHttpRequest construction"),
    ("WebSocket", "a WebSocket construction"),
    ("EventSource", "an EventSource construction"),
    ("sendBeacon", "a sendBeacon call"),
    ("import(", "a dynamic import("),
    ("require(", "a require("),
    ("node:", "a Node builtin-module import"),
    ("localStorage", "a localStorage reference"),
    ("/actions/", "a governance action route literal"),
    ("git ", "a shelled-out git invocation"),
    ("fs.", "a Node fs module call"),
]


@pytest.mark.parametrize("needle,label", _FORBIDDEN_NEEDLES)
def test_editor_module_contains_no_network_or_filesystem_primitive(needle, label):
    source = EDITOR_JS.read_text(encoding="utf-8")
    assert needle not in source, f"doxbench-editor.js must not contain {label}: {needle!r}"


@pytest.mark.parametrize("needle,label", _FORBIDDEN_NEEDLES)
def test_state_module_contains_no_network_or_filesystem_primitive(needle, label):
    source = STATE_JS.read_text(encoding="utf-8")
    assert needle not in source, f"doxbench-state.js must not contain {label}: {needle!r}"


def test_editor_module_contains_no_bare_post_verb():
    source = EDITOR_JS.read_text(encoding="utf-8")
    assert "POST" not in source, "doxbench-editor.js must not name the POST verb anywhere"


def test_state_module_contains_no_bare_post_verb():
    source = STATE_JS.read_text(encoding="utf-8")
    assert "POST" not in source, "doxbench-state.js must not name the POST verb anywhere"


# ---------------------------------------------------------------------------
# Items 2-5: ONE behavioural + filesystem run backs every remaining test.
# ---------------------------------------------------------------------------

# Same instrument as test_doxbench_view.py's editor harness, trimmed to what
# driving the controller needs (no rich querySelector/closest introspection).
_DOM_SHIM = r"""
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
  get hidden() { return this._hidden; }
  set hidden(v) {
    this._hidden = !!v;
    // A real browser blurs a focused DESCENDANT the instant an ancestor
    // becomes hidden, not only the exact node hidden -- hiding a pane while
    // its interior textarea holds focus must drop that focus too.
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
  get textContent() { return this._text + this.children.map((c) => c.textContent).join(''); }
  set textContent(value) { this.children = []; this._text = String(value); }
  get innerHTML() { return this._innerHTML; }
  set innerHTML(value) { this._innerHTML = String(value); this.children = []; this._text = ''; }
  get value() { return this._value; }
  set value(v) { this._value = String(v); }
  get selectionStart() { return this._selectionStart; }
  set selectionStart(v) { this._selectionStart = v; }
  get selectionEnd() { return this._selectionEnd; }
  set selectionEnd(v) { this._selectionEnd = v; }
  get scrollTop() { return this._scrollTop; }
  set scrollTop(v) { this._scrollTop = v; }
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
    return Object.prototype.hasOwnProperty.call(this.attributes, name) ? this.attributes[name] : null;
  }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() { globalThis.document.activeElement = this; }
  blur() { if (globalThis.document.activeElement === this) globalThis.document.activeElement = null; }
  walk() { return this.children.reduce((all, c) => all.concat(c.walk()), [this]); }
  querySelector() { return null; }
  querySelectorAll() { return []; }
}
globalThis.document = {
  createElement: (tag) => new Node(tag),
  createTextNode: (text) => { const n = new Node('#text'); n._text = String(text); return n; },
  activeElement: null,
  addEventListener() {},
  body: new Node('body'),
};
"""

# Drives the exact US1 loop the task brief specifies: load, edit outline,
# edit document, flush preview, switch tabs both ways, attempt a blocked
# document switch, resolveGuard("save"), resolveGuard("cancel"), discard
# both buffers, refreshContext -- with every network/storage primitive
# trapped and recording, and a snapshot of storage taken immediately before
# and after the "save" resolution (item 5: it must persist nothing).
_MUTATION_HARNESS = _DOM_SHIM + r"""
import { createRequire } from 'node:module';
globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');

const attempts = [];
globalThis.fetch = (...args) => {
  attempts.push({ kind: 'fetch', arg: String(args[0]) });
  throw new Error('fetch blocked');
};
globalThis.XMLHttpRequest = function XMLHttpRequest() {
  attempts.push({ kind: 'XMLHttpRequest' });
  throw new Error('xhr blocked');
};
globalThis.WebSocket = function WebSocket(...args) {
  attempts.push({ kind: 'WebSocket', arg: String(args[0]) });
  throw new Error('ws blocked');
};
globalThis.EventSource = function EventSource(...args) {
  attempts.push({ kind: 'EventSource', arg: String(args[0]) });
  throw new Error('es blocked');
};
// Node >= 21 ships read-only globals for `navigator` (and sometimes
// `WebSocket`); the trap must replace the property descriptor rather than
// assign straight through it.
Object.defineProperty(globalThis, 'navigator', {
  configurable: true,
  writable: true,
  value: {
    sendBeacon: (...args) => {
      attempts.push({ kind: 'sendBeacon', arg: String(args[0]) });
      throw new Error('beacon blocked');
    },
  },
});
globalThis.localStorage = new Proxy({}, {
  get(_target, prop) {
    attempts.push({ kind: 'localStorage', prop: String(prop) });
    throw new Error('localStorage blocked');
  },
});

class FakeStorage {
  constructor() { this.values = new Map(); }
  getItem(key) { return this.values.has(key) ? this.values.get(key) : null; }
  setItem(key, value) { this.values.set(key, String(value)); }
  removeItem(key) { this.values.delete(key); }
}
function snapshotStorage(storage) {
  return JSON.stringify([...storage.values.entries()].sort(([a], [b]) => a.localeCompare(b)));
}

const { mountDoxBenchCanvas } = await import('./doxbench-editor.js');

const OUTLINE_PATH = 'ideation/staging/topic-x/topic-x.md';
const DOC_A = 'ideation/staging/topic-x/detail.md';
const DOC_B = 'ideation/staging/topic-x/second.md';
const CONTENT = {
  [OUTLINE_PATH]: '# Outline\n',
  [DOC_A]: '# Document A\n',
  [DOC_B]: '# Document B\n',
};
async function loadSource(path) {
  if (!(path in CONTENT)) return null;
  return { content: CONTENT[path], revision: 'rev-' + path, ref: 'main' };
}
const projection = {
  key: { repository: 'fixture-repo', ref: 'draft/topic-x', tile_kind: 'staged', tile_id: 'topic-x' },
  title: 'Topic X',
  source_revision: 'a'.repeat(40),
  outline_path: OUTLINE_PATH,
  editable_paths: [OUTLINE_PATH, DOC_A, DOC_B],
  context_paths: [OUTLINE_PATH, DOC_A, DOC_B],
  active_document_candidates: [DOC_A, DOC_B],
  sections: [],
};

const storage = new FakeStorage();
const host = new Node('div');
const controller = mountDoxBenchCanvas(host, projection, { loadSource, storage, previewDelayMs: 5 });

await controller.ready;                                    // load
await controller.edit('outline', '# Outline edited\n');    // edit outline
await controller.edit('document', '# Document A edited\n');// edit document
await controller.flushPreview();                            // flush preview
controller.setActiveBuffer('document');                     // switch buffers
controller.setActiveBuffer('outline');                       //   both ways
controller.setActiveView('editor');                          // and both views
controller.setActiveView('preview');                         //   (Phase A)
const blocked = await controller.selectDocument(DOC_B);      // blocked switch
const storageBeforeSave = snapshotStorage(storage);
const saveResolved = await controller.resolveGuard('save');  // resolveGuard("save")
const storageAfterSave = snapshotStorage(storage);
const cancelResolved = await controller.resolveGuard('cancel'); // resolveGuard("cancel")
await controller.discard('outline');                          // discard both
await controller.discard('document');                         //   buffers
await controller.refreshContext(projection);                  // refreshContext
controller.destroy();

const storagePayloadKeys = [...storage.values.keys()];
const storagePayloads = Object.fromEntries(
  [...storage.values.entries()].map(([k, v]) => [k, JSON.parse(v)]),
);

console.log(JSON.stringify({
  attempts,
  blocked,
  saveResolved,
  cancelResolved,
  storageBeforeSave,
  storageAfterSave,
  storagePayloadKeys,
  storagePayloads,
}));
"""


@pytest.fixture(scope="module")
def mutation_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench mutation-boundary probe")
    harness_root = tmp_path_factory.mktemp("doxbench-mutation-harness")
    (harness_root / "views").mkdir()
    (harness_root / "vendor").mkdir()
    shutil.copy(EDITOR_JS, harness_root / "views" / "doxbench-editor.js")
    shutil.copy(STATE_JS, harness_root / "views" / "doxbench-state.js")
    shutil.copy(VIEWER_JS, harness_root / "views" / "viewer.js")
    shutil.copy(VENDOR_MARKDOWN_JS, harness_root / "vendor" / "markdown-it.min.js")
    (harness_root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (harness_root / "vendor" / "package.json").write_text(
        '{"type": "commonjs"}', encoding="utf-8"
    )
    harness = harness_root / "views" / "mutation-harness.mjs"
    harness.write_text(_MUTATION_HARNESS, encoding="utf-8")

    # A scratch corpus the node process runs WITH AS ITS CWD, so a stray
    # relative-path filesystem write lands somewhere this test can see it.
    # ESM import specifiers resolve relative to the importing file's own
    # location, not process.cwd(), so pointing cwd at a directory that has
    # nothing to do with harness_root does not affect module resolution.
    scratch = tmp_path_factory.mktemp("doxbench-mutation-scratch")
    (scratch / "nested").mkdir()
    (scratch / "a.md").write_text("# A\n", encoding="utf-8")
    (scratch / "b.md").write_text("# B\n", encoding="utf-8")
    (scratch / "nested" / "c.md").write_text("# C\n", encoding="utf-8")

    def manifest():
        rows = {}
        for path in sorted(scratch.rglob("*")):
            if path.is_file():
                data = path.read_bytes()
                rows[str(path.relative_to(scratch))] = (
                    len(data),
                    hashlib.sha256(data).hexdigest(),
                    path.stat().st_mtime_ns,
                )
        return rows

    manifest_before = manifest()
    proc = subprocess.run(
        [NODE, str(harness)],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=scratch,
    )
    manifest_after = manifest()

    assert proc.returncode == 0, proc.stderr
    return {
        "json": json.loads(proc.stdout),
        "manifest_before": manifest_before,
        "manifest_after": manifest_after,
    }


def test_full_us1_loop_makes_no_network_or_storage_escape_attempts(mutation_results):
    """Item 2: load, edit both buffers, preview, switch tabs both ways, hit
    and resolve the document-switch guard twice, discard both buffers, and
    refresh context -- against traps for every transport and for
    localStorage -- record ZERO attempts."""
    attempts = mutation_results["json"]["attempts"]
    assert attempts == [], f"unexpected transport/storage attempts: {attempts}"


def test_full_us1_loop_leaves_the_working_directory_byte_identical(mutation_results):
    """Item 3: running the loop with cwd set to a scratch corpus leaves that
    corpus byte-identical (path, size, sha256, and mtime all unchanged), and
    creates no new path -- in particular no .git, gate-record, snapshot,
    registry, or manifest file."""
    before = mutation_results["manifest_before"]
    after = mutation_results["manifest_after"]
    assert after == before
    assert set(after) == set(before)
    forbidden_markers = (".git", "gate-record", "snapshot", "registry", "manifest")
    new_paths = set(after) - set(before)
    for path in new_paths:  # empty given the equality assert above; explicit anyway
        assert not any(marker in path for marker in forbidden_markers)


def test_the_only_persistence_is_the_injected_session_storage(mutation_results):
    """Item 4: the ONLY persistence the loop performs is into the injected
    session-storage-like object; every key starts with `doxbench:v1:`, and
    the recorded payload carries no hash/dirty fields (doxbench-state.js's
    `persistedBuffer` deliberately persists derived inputs only). The fake
    `localStorage` is never touched (redundant with the attempts-empty
    assertion above, checked again here for this specific claim)."""
    payload_keys = mutation_results["json"]["storagePayloadKeys"]
    assert payload_keys, "expected the destroyed controller to have persisted something"
    for key in payload_keys:
        assert key.startswith("doxbench:v1:")
    for envelope in mutation_results["json"]["storagePayloads"].values():
        for buffer in envelope["buffers"].values():
            assert "base_hash" not in buffer
            assert "current_hash" not in buffer
            assert "dirty" not in buffer
            assert "hash_generation" not in buffer
    local_storage_attempts = [
        a for a in mutation_results["json"]["attempts"] if a["kind"] == "localStorage"
    ]
    assert local_storage_attempts == []


def test_resolve_guard_save_performs_no_persistence(mutation_results):
    """Item 5: resolveGuard("save") refuses with the fixed reason and leaves
    the storage payload byte-identical to what it was immediately before the
    call."""
    result = mutation_results["json"]
    assert result["saveResolved"]["status"] == "refused"
    assert result["storageBeforeSave"] == result["storageAfterSave"]


# ===========================================================================
# T072 (010-doxbench-editor-chat, US4): served-checkout immutability and
# governance-action audit assertions for the eligible first Save.
#
# Two deliberately different KINDS of assertion live below, and the difference
# is the point:
#
#   * IMMUTABILITY TRIPWIRES, which are green on arrival. Nothing in the
#     doxBench client surface names a delete, merge, approve, or model-write
#     verb today, and the served checkout is moved by no session operation.
#     Pinning that BEFORE the Save wave lands is the whole value: FR-037 is a
#     boundary that is easy to cross by accident while adding a write path, and
#     a tripwire that only starts failing once somebody crosses it reports the
#     crossing on a named line. A green assertion here is evidence, not filler.
#   * AUDIT-SHAPE ASSERTIONS for the first-edit transaction, which are RED
#     until T074 lands `branch_session.commit_first_edit`. They pin FR-034's
#     "one existing governance action per changed document" and FR-032's
#     "persist only in the resulting session" as measured facts about records,
#     commits, and the served checkout's fingerprint.
#
# Pins FR-032, FR-033, FR-034, FR-037 and SC-006.
# ===========================================================================

from pathlib import Path  # noqa: E402  (the T029 block above needs no filesystem paths)

import yaml  # noqa: E402

from session_fixtures import GATE_RECORDS_PREFIX  # noqa: E402

from ideation_dashboard import branch_session as bs  # noqa: E402
from ideation_dashboard import doxbench_hash as dh  # noqa: E402
from ideation_dashboard import gate_console as gc  # noqa: E402
from ideation_dashboard import session_git as sg  # noqa: E402
from ideation_dashboard import snapshot_registry as reg  # noqa: E402
from ideation_dashboard.boundary import HumanGate  # noqa: E402
from ideation_dashboard.generator import generate_snapshot  # noqa: E402

SAVE_JS = (
    REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views" / "doxbench-save.js"
)

TOPIC = "demo-topic"
DRAFT = "draft/demo-topic"
OWNED_PREFIX = f"ideation/staging/{TOPIC}/"
OUTLINE = f"{OWNED_PREFIX}README.md"          # exists in the served checkout
NEW_DOC = f"{OWNED_PREFIX}detail.md"          # a path nothing has created yet
ALLOWLIST = (GATE_RECORDS_PREFIX, "ideation/staging/")
AT = "2026-07-30T09:00:00Z"
AT_LATER = "2026-07-30T09:00:05Z"


# ---------------------------------------------------------------------------
# FR-037, static: no doxBench client module may NAME a delete, merge, approve,
# or write-authority verb. Green on arrival for the editor and the state
# module; RED for `doxbench-save.js` until T077 creates it.
# ---------------------------------------------------------------------------

_WRITE_AUTHORITY_NEEDLES = [
    ("delete", "a delete verb (FR-037: no doxBench path deletes a document)"),
    ("unlink", "a filesystem unlink"),
    # NOT `removeItem(`: clearing BROWSER-LOCAL session storage is FR-039's
    # requirement, not an FR-037 authority. `doxbench-state.js` owns that API.
    ("merge", "a merge verb (FR-037: no doxBench path merges a pull request)"),
    ("approve", "an approval verb (FR-037: no doxBench path approves)"),
    ("open-pr", "the pull-request action name"),
    ("abandon", "the session-ending action name"),
    ("grant", "an authority grant (FR-037: no model write authority)"),
    ("model_write", "a model write-authority field"),
    ("write_authority", "a write-authority field"),
]

_CLIENT_MODULES = [("doxbench-editor.js", EDITOR_JS),
                   ("doxbench-state.js", STATE_JS),
                   ("doxbench-save.js", SAVE_JS)]


def _client_source(name, path):
    assert path.is_file(), (
        f"{name} does not exist yet, so FR-037's write-authority sentinels "
        f"cannot be asserted over it (expected at {path})")
    return path.read_text(encoding="utf-8")


@pytest.mark.parametrize("module_name,module_path", _CLIENT_MODULES,
                         ids=[n for n, _ in _CLIENT_MODULES])
@pytest.mark.parametrize("needle,label", _WRITE_AUTHORITY_NEEDLES,
                         ids=[n for n, _ in _WRITE_AUTHORITY_NEEDLES])
def test_no_doxbench_client_module_names_a_write_authority_verb(
        module_name, module_path, needle, label):
    """FR-037's four forbidden authorities, asserted as ABSENCE of the verb
    from every doxBench client module — including the Save orchestrator, whose
    whole job is to reach governance actions and which is therefore the exact
    module where a delete/merge/approve/grant would first appear."""
    source = _client_source(module_name, module_path)
    assert needle not in source, f"{module_name} must not contain {label}: {needle!r}"


# ---------------------------------------------------------------------------
# R2's convention, applied to the Save orchestrator: it may be HANDED a
# transport, and must construct none of its own. This is a narrower rule than
# the editor's and state module's (which may not even have a transport seam),
# so it gets its own list rather than reusing `_FORBIDDEN_NEEDLES`.
# ---------------------------------------------------------------------------

_SAVE_OWN_TRANSPORT_NEEDLES = [
    ("fetch(", "a fetch( call of its own (the transport is INJECTED)"),
    ("XMLHttpRequest", "an XMLHttpRequest construction"),
    ("WebSocket", "a WebSocket construction"),
    ("EventSource", "an EventSource construction"),
    ("sendBeacon", "a sendBeacon call"),
    ("import(", "a dynamic import("),
    ("require(", "a require("),
    ("node:", "a Node builtin-module import"),
    ("localStorage", "a localStorage reference"),
    ("fs.", "a Node fs module call"),
    ("git ", "a shelled-out git invocation"),
]


@pytest.mark.parametrize("needle,label", _SAVE_OWN_TRANSPORT_NEEDLES)
def test_the_save_module_constructs_no_transport_of_its_own(needle, label):
    """T077's module is import-free pure state plus an INJECTED transport (R2).
    It therefore reaches the network through what it is handed and through
    nothing else — the seam every test in this feature drives it by."""
    source = _client_source("doxbench-save.js", SAVE_JS)
    assert needle not in source, f"doxbench-save.js must not contain {label}: {needle!r}"


def test_the_save_module_has_no_import_statement():
    """Import-free, like `doxbench-state.js`: the Node harness executes the
    exact browser bytes, so a bare `import` of a sibling would make the two
    surfaces different programs."""
    source = _client_source("doxbench-save.js", SAVE_JS)
    offenders = [line for line in source.splitlines()
                 if line.startswith("import ") or line.startswith("import{")]
    assert offenders == [], f"doxbench-save.js must stay import-free: {offenders}"


# ---------------------------------------------------------------------------
# The first-edit transaction, measured. RED until T074.
# ---------------------------------------------------------------------------

def _registry(repo, tmp_path):
    path = tmp_path / "main-snapshot.json"
    path.write_text(json.dumps(generate_snapshot(repo.root, repo.repository)),
                    encoding="utf-8")
    registry = reg.SnapshotRegistry()
    registry.register(reg.entry_from_snapshot_file(
        path, repository=repo.repository, ref=reg.DEFAULT_REF,
        source_root=repo.root), active=True)
    return registry


def _gate_factory(actor="brett"):
    """The seam T074 builds its worktree-rooted gate through. A session rewrite
    is written through a gate rooted at the WORKTREE and DECLARING it, so the
    rewrite allowance and the record's residence are the same tree."""
    def build(worktree):
        return HumanGate(worktree, list(ALLOWLIST), human_actor=actor,
                         session_root=worktree)
    return build


def _first_save(repo, registry, *, document, content, base_hash=None, at=AT,
                owned_prefix=OWNED_PREFIX, git=None, **over):
    """One eligible first Save through T074's transaction entry point."""
    return bs.commit_first_edit(
        git or sg.SessionGit(repo.root), registry,
        repository=repo.repository,
        tile=bs.Tile(bs.STAGED_TOPIC, TOPIC),
        document=document, content=content,
        gate_factory=_gate_factory(),
        checkout_root=repo.root, owned_prefix=owned_prefix,
        base_hash=base_hash, at=at, records_dir=GATE_RECORDS_PREFIX, **over)


def _records_under(root):
    return sorted(p.relative_to(root).as_posix()
                  for p in (root / GATE_RECORDS_PREFIX).rglob("*.gate-action.yaml"))


def _commit_files(worktree, sha):
    out = subprocess.run(["git", "show", "--name-only", "--format=", sha],
                         cwd=str(worktree), text=True, capture_output=True,
                         check=True).stdout
    return sorted(line for line in out.split() if line)


def test_a_first_save_of_a_new_path_leaves_the_served_checkout_byte_identical(
        scratch_repo, tmp_path):
    """FR-037 + FR-032, measured rather than argued: the served checkout is the
    branch's base and no doxBench path writes to it. Its branch, HEAD, and
    porcelain are identical across a Save that creates a document, and the new
    bytes exist ONLY in the session worktree."""
    registry = _registry(scratch_repo, tmp_path)
    before = scratch_repo.served_fingerprint()
    origin_before = scratch_repo.origin_branches()

    outcome = _first_save(scratch_repo, registry,
                          document=NEW_DOC, content="# Detail\n\nfirst save.\n")

    assert scratch_repo.served_fingerprint() == before
    assert scratch_repo.origin_branches() == origin_before, (
        "an eligible first Save pushes nothing; `open-pr` is the save verb")
    assert not (scratch_repo.root / NEW_DOC).exists(), (
        "the created document must exist on the SESSION BRANCH only")
    assert (Path(outcome.session.worktree) / NEW_DOC).read_text(
        encoding="utf-8") == "# Detail\n\nfirst save.\n"


def test_a_first_save_of_an_existing_owned_path_leaves_the_served_bytes_alone(
        scratch_repo, tmp_path):
    """The same claim for the rewrite arm, which is the one that could plausibly
    reach the served copy: the served checkout's own copy of the document is
    byte-identical afterwards, and the replacement lives on the branch."""
    registry = _registry(scratch_repo, tmp_path)
    served_bytes = (scratch_repo.root / OUTLINE).read_bytes()
    base_hash = dh.sha256_hex(served_bytes.decode("utf-8"))
    before = scratch_repo.served_fingerprint()

    outcome = _first_save(scratch_repo, registry, document=OUTLINE,
                          content="# Demo Topic\n\nrewritten by doxBench.\n",
                          base_hash=base_hash)

    assert scratch_repo.served_fingerprint() == before
    assert (scratch_repo.root / OUTLINE).read_bytes() == served_bytes
    assert (Path(outcome.session.worktree) / OUTLINE).read_text(
        encoding="utf-8") == "# Demo Topic\n\nrewritten by doxBench.\n"


def test_a_first_save_writes_exactly_one_governance_record_naming_its_branch(
        scratch_repo, tmp_path):
    """FR-034's "one existing governance action per changed document", read off
    disk: ONE gate-action record, carrying the EXISTING action name, naming the
    session branch as its ref, and carrying exactly one commit artifact that
    references its own action stamp and no sha (D18's validator requirement)."""
    registry = _registry(scratch_repo, tmp_path)

    outcome = _first_save(scratch_repo, registry,
                          document=NEW_DOC, content="# Detail\n\nfirst save.\n")

    worktree = Path(outcome.session.worktree)
    records = _records_under(worktree)
    assert len(records) == 1, records
    record = yaml.safe_load((worktree / records[0]).read_text(encoding="utf-8"))
    assert record["action"] == gc.ACTION_CREATE_DOCUMENT
    assert record["target"]["ref"] == DRAFT
    assert record["actor"] == "brett"
    artifacts = [a for a in record["artifacts"] if a.get("kind") == gc.ART_COMMIT]
    assert len(artifacts) == 1, record["artifacts"]
    assert artifacts[0]["reference"] == bs.action_stamp(AT)
    assert outcome.commit.sha not in json.dumps(record), (
        "the sha is RETURNED for the response and never written into the record")
    # and the served checkout holds no record for this action at all
    assert _records_under(scratch_repo.root) == []


def test_a_first_save_rides_exactly_one_commit_carrying_document_and_record(
        scratch_repo, tmp_path):
    """FR-034 again, from the commit's side: the document and its record are the
    ENTIRE content of one commit on the session branch."""
    registry = _registry(scratch_repo, tmp_path)

    outcome = _first_save(scratch_repo, registry,
                          document=NEW_DOC, content="# Detail\n\nfirst save.\n")

    worktree = Path(outcome.session.worktree)
    git = sg.SessionGit(scratch_repo.root)
    assert git.commits_ahead("main", DRAFT) == 1
    assert _commit_files(worktree, outcome.commit.sha) == sorted(
        [NEW_DOC, outcome.commit.record_relpath])
    assert git.staged_paths(worktree) == ()
    assert outcome.revision == outcome.commit.sha
    assert outcome.ref == DRAFT
    assert outcome.action == gc.ACTION_CREATE_DOCUMENT
    assert outcome.content_hash == dh.content_identity(
        "# Detail\n\nfirst save.\n").as_dict()


def test_two_changed_documents_produce_two_records_and_two_commits(
        scratch_repo, tmp_path):
    """FR-034's ordering clause at the transaction layer: each changed document
    is its OWN existing governance action. Two Saves are two records and two
    commits — never one commit carrying both under a single trailer."""
    registry = _registry(scratch_repo, tmp_path)
    git = sg.SessionGit(scratch_repo.root)
    served = (scratch_repo.root / OUTLINE).read_text(encoding="utf-8")

    first = _first_save(scratch_repo, registry, document=OUTLINE,
                        content="# Demo Topic\n\noutline saved.\n",
                        base_hash=dh.sha256_hex(served), at=AT, git=git)
    second = _first_save(scratch_repo, registry, document=NEW_DOC,
                         content="# Detail\n\ndocument saved.\n", at=AT_LATER,
                         git=git)

    worktree = Path(first.session.worktree)
    assert second.session.branch == first.session.branch
    assert second.joined is True, "the second Save JOINS the session the first opened"
    assert git.commits_ahead("main", DRAFT) == 2
    assert len(_records_under(worktree)) == 2
    assert _commit_files(worktree, first.commit.sha) == sorted(
        [OUTLINE, first.commit.record_relpath])
    assert _commit_files(worktree, second.commit.sha) == sorted(
        [NEW_DOC, second.commit.record_relpath])
    assert first.action == gc.ACTION_EDIT_DOCUMENT
    assert second.action == gc.ACTION_CREATE_DOCUMENT


def test_a_refused_first_save_writes_no_governance_artifact_anywhere(
        scratch_repo, tmp_path):
    """FR-033 + FR-037 together: a first Save refused for ineligibility persists
    no record and no commit, and the served checkout — the thing a refusal is
    most likely to have touched on its way out — is byte-identical."""
    registry = _registry(scratch_repo, tmp_path)
    inherited = "ideation/staging/other-topic/README.md"
    scratch_repo.write(inherited, "# Other Topic\n\nsomebody else's material.\n")
    scratch_repo.commit("Add another topic's material", inherited)
    before = scratch_repo.served_fingerprint()
    served_bytes = (scratch_repo.root / inherited).read_bytes()

    with pytest.raises(bs.SessionRefused):
        _first_save(scratch_repo, registry, document=inherited,
                    content="# Other Topic\n\nrewritten from doxBench.\n",
                    base_hash=dh.sha256_hex(served_bytes.decode("utf-8")))

    assert scratch_repo.served_fingerprint() == before
    assert (scratch_repo.root / inherited).read_bytes() == served_bytes
    assert _records_under(scratch_repo.root) == []
    assert bs.is_live(registry, scratch_repo.repository, DRAFT) is False, (
        "an ineligible target is refused BEFORE anything is opened")
    assert not bs.worktree_path(scratch_repo.root, DRAFT).exists()


# ---------------------------------------------------------------------------
# T059/T064 (US3, red-first): local Apply mutates exactly ONE buffer, is
# reversible through the EXISTING Discard path, revalidates exact identity
# immediately before the swap, and performs no persistence of any kind —
# a lean standalone harness over doxbench-state.js alone.
# ---------------------------------------------------------------------------

_APPLY_HARNESS = r"""
import { createDoxBenchState, applyProposalToBuffer, settleBufferHash,
         discardBuffer } from "./doxbench-state.mjs";

const fakeHash = (content) => ({ algorithm: "sha256",
  hex: "a".repeat(63) + String(content.length % 10) });
const descriptor = (kind, content) => ({
  kind, path: kind === "outline" ? "docs/outline.md" : null, owned: true,
  base_ref: "draft/topic-x", base_revision: "r1", content });
const out = {};
const state = await createDoxBenchState({
  key: { repository: "fixture-repo", ref: "draft/topic-x",
         tile_kind: "staged", tile_id: "topic-x" },
  active_buffer: "outline",
  outline: descriptor("outline", "# Outline base"),
  document: descriptor("document", "# Document base"),
}, { hash: fakeHash });
const outline = state.buffers.outline;
const documentBuffer = state.buffers.document;
const proposal = { target: "outline", base_hash: outline.current_hash.hex,
                   summary: "Rework", content: "# Outline reworked" };

// current apply: one buffer changes, sibling untouched, reversible
const pending = applyProposalToBuffer(outline, proposal, { hash: fakeHash });
out.applyAccepted = pending !== null;
const settled = settleBufferHash(pending.buffer, await pending.completion);
out.applied = { content: settled.buffer.content, dirty: settled.buffer.dirty,
                siblingUntouched:
                  documentBuffer === state.buffers.document
                  && documentBuffer.content === "# Document base" };
const reverted = discardBuffer(settled.buffer);
out.reverted = { content: reverted.buffer ? reverted.buffer.content
                 : reverted.content ?? null };

// stale refusal: wrong base identity refuses with null, buffer untouched
out.staleRefused = applyProposalToBuffer(
  outline, { ...proposal, base_hash: "f".repeat(64) },
  { hash: fakeHash }) === null;
out.originalIntact = outline.content === "# Outline base";

// unsettled-hash refusal: a buffer mid-hash cannot be applied onto
out.pendingRefused = applyProposalToBuffer(
  pending.buffer, proposal, { hash: fakeHash }) === null;
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def apply_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for doxBench apply probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-apply")
    shutil.copy(STATE_JS, tmp_path / "doxbench-state.mjs")
    harness = tmp_path / "apply-harness.mjs"
    harness.write_text(_APPLY_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_a_current_apply_changes_exactly_one_buffer(apply_results):
    assert apply_results["applyAccepted"] is True
    a = apply_results["applied"]
    assert a["content"] == "# Outline reworked"
    assert a["dirty"] is True
    assert a["siblingUntouched"] is True


def test_apply_is_reversible_through_the_existing_discard_path(apply_results):
    assert apply_results["reverted"]["content"] == "# Outline base"


def test_a_stale_or_unsettled_buffer_refuses_apply(apply_results):
    assert apply_results["staleRefused"] is True
    assert apply_results["originalIntact"] is True
    assert apply_results["pendingRefused"] is True
