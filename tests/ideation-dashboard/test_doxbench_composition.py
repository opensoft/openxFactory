"""doxBench Phase B, driven through the REAL COMPOSITION.

Why this file exists, stated plainly: the adversarial review of PR #207 found
four broken flows that every harness-stubbed test in the suite was blind to. Each
one lived in the WIRING — between the canvas controller, the shell, the docs
wheel, the chat rail and the released turn envelope — and each one passed its
own unit tests because those tests supplied the seam the shipped code does not.

So this module mounts `mountStagingWorkbench` for real, against the same minimal
DOM instrument `test_doxbench_view.py` uses (the shim is IMPORTED from there
rather than copied, so the two cannot drift), and drives:

* **F1** — loading a document made every chat turn refuse. The released v1
  envelope carries exactly the outline and the reserved `document` slot, so
  `active_document_path` can only ever name the reserved slot's path; handing it
  the SELECTED buffer's path named a buffer the wire never carried and the route
  answered with its fixed redacted `turn_scope_refused` code. A governance
  refusal for a limitation of our own wire.
* **F2** — the tile Save was enabled and then refused for every restored Phase A
  session, because the marking resolved the buffer BY PATH and the save resolved
  it BY KEY.
* **F3** — `Editing is unavailable` was unrealized: the verbs always existed, so a
  gate-off surface failed ON ACTIVATION with the wrong sentence.
* **F6** — the selector's ratified empty state could never render, because the
  always-present reserved `document` slot was counted as a loaded document.

Every assertion here is about the composition, and every one of them FAILS
against the code as PR #207 first proposed it.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT
# The SAME DOM instrument the canvas suite drives, imported rather than copied:
# a second shim is a second set of behaviours to keep in step, and the two
# drifting is precisely how a composition defect hides.
from test_doxbench_view import _EDITOR_DOM_SHIM

NODE = shutil.which("node")
VIEWS = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
VENDOR = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "vendor"

_COMPOSITION_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';

globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');
globalThis.window = { location: { href: 'http://localhost/' } };

const { mountStagingWorkbench } = await import('./staging-workbench.js');

const OUTLINE_PATH = 'ideation/staging/topic-x/topic-x.md';
const DOC_A = 'ideation/staging/topic-x/detail.md';
const DOC_B = 'ideation/staging/topic-x/second.md';
// N1 (PR #207 re-verification): two paths that sort BEFORE the literal reserved
// key `"document"` under the declared UTF-16 code-unit order (uppercase letters
// precede lowercase). They exist to DISCRIMINATE the F1 wire fix: the reverted
// implementation fell through to the first loaded document by key order, which the
// original fixture's `detail.md`/`second.md` never were, because both sort AFTER
// `"document"` and the reserved slot therefore won by accident rather than by
// rule. TWO of them, so that whichever one the projection happens to make the
// reserved slot, at least one is still loadable.
const EARLY_A = 'BOOK.md';
const EARLY_B = 'README.md';

function snapshotFor(files) {
  return {
    repository: 'fixture-repo',
    generation: { source_revision: '1'.repeat(40) },
    documents: files.map((p) => ({
      id: p, path: p, topics: ['alpha'],
      destinations: { staged_topics: ['topic-x'] } })),
    clusters: [], possibles: [],
    staged_topics: [{ staging_id: 'topic-x', files }],
  };
}

const settle = () => new Promise((r) => setTimeout(r, 0));
async function until(predicate, label) {
  for (let i = 0; i < 600; i += 1) {
    if (predicate()) return;
    await settle();
  }
  throw new Error('timed out waiting for ' + label);
}
async function quiesce(n = 30) { for (let i = 0; i < n; i += 1) await settle(); }

function fire(node, type, ev = {}) {
  const listeners = (node.listeners && node.listeners[type]) || [];
  return Promise.all(listeners.map(
    (fn) => fn({ target: node, stopPropagation() {}, preventDefault() {}, ...ev })));
}

class FakeStorage {
  constructor() { this.values = new Map(); }
  getItem(k) { return this.values.has(k) ? this.values.get(k) : null; }
  setItem(k, v) { this.values.set(k, String(v)); }
  removeItem(k) { this.values.delete(k); }
}

const MODEL = { model_id: 'model-a', label: 'Approved model', available: true,
                provider_class: 'on-tenant', input_limit_bytes: 800000,
                output_limit_bytes: 900000, data_handling: 'tenant boundary' };

// One whole mount, with every seam recording what it was asked to do.
async function mount({ files, gate = true, saveAnswer = null }) {
  const container = document.createElement('div');
  const log = { turns: [], saves: [] };
  const caps = gate
    ? { actions: { gate: true, session: true }, actor: 'brett' }
    : { actions: {}, actor: 'brett' };
  const doxbench = {
    loadSource: async (path) => ({ content: '# ' + path + '\n', ref: 'main' }),
    storage: new FakeStorage(),
    catalog: async () => ({ schema_version: 1,
      kind: 'workbench-model-catalog', models: [MODEL] }),
    chatTurn: async (request) => {
      log.turns.push(request);
      return { ok: false, status: 502, payload: {} };
    },
    hash: undefined,
    save: async (request) => {
      log.saves.push(request);
      return saveAnswer || {
        status: 'committed',
        buffers: (request.buffers || []).map((row) => ({
          key: row.key ?? row.kind, status: 'committed',
          action: 'edit-document', ref: 'draft/topic-x', revision: 'r2',
          content_hash: { algorithm: 'sha256', hex: 'e'.repeat(64) },
          message: null })),
        state: { key: request.key, active_buffer: 'outline', buffers: {} },
      };
    },
  };
  const opened = [];
  const workbench = mountStagingWorkbench(container, snapshotFor(files), {
    caps,
    // A real embedding supplies the reader (app.js hands the explorer's own
    // `openDoc`). Without it the tile's `read` is correctly unreachable, which
    // would have made this harness prove the wrong thing.
    onOpenDoc: (path) => opened.push(path),
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
  return { container, workbench, log, byClass, one, doxbench, opened };
}

// The docs wheel needs a measurable host before it lays tiles out, and only a
// laid-out expanded tile mounts its action row.
async function expandTileFor(ctx, path) {
  const pane = ctx.container.walk().find((n) => n.__docWheel);
  const host = ctx.one('swb-docselector');
  host.clientHeight = 420;
  pane.__docWheelRefresh();
  await quiesce(5);
  const tiles = ctx.byClass('wheeltile');
  const index = tiles.findIndex((t) => t.title === path);
  if (index < 0) throw new Error('no tile for ' + path);
  for (let attempt = 0; attempt < 3; attempt += 1) {
    if (tiles[index].querySelector('.wheelactions')) break;
    await fire(tiles[index], 'click');
    await quiesce(5);
  }
  const row = tiles[index].querySelector('.wheelactions');
  if (!row) throw new Error('tile for ' + path + ' never expanded');
  return { tile: tiles[index], row, pane };
}

async function chooseModel(ctx) {
  const selector = ctx.one('doxchat-model');
  selector.value = 'model-a';
  await fire(selector, 'change');
  await quiesce(5);
}

async function typeAndSend(ctx, message) {
  const composer = ctx.one('doxchat-composer');
  composer.value = message;
  await fire(composer, 'input');
  await quiesce(5);
  const send = ctx.one('doxchat-send');
  const disabledBefore = send.disabled === true;
  await fire(send, 'click');
  await quiesce(40);
  return { disabledBefore, title: send.title,
           failure: String((ctx.one('doxchat-failure') || {}).textContent || ''),
           unavailable: String((ctx.one('doxchat-unavailable') || {}).textContent || '') };
}

const out = {};

// =====================================================================
// F1 / N4: loading a document must not kill the chat, and the chat now BINDS
// to whichever buffer is selected (contract-v1.34, §13)
// =====================================================================
{
  const ctx = await mount({
    files: [OUTLINE_PATH, DOC_A, DOC_B, EARLY_A, EARLY_B] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await until(() => ctx.one('doxchat-loaded') !== null, 'the chat rail');
  await quiesce(40);
  await chooseModel(ctx);
  out.f1 = {};

  // A BASELINE turn first, so the reserved slot's own path is read off the WIRE
  // rather than assumed: whichever document the projection made active at mount
  // is the one that slot holds, and that is the fact the rest is measured
  // against.
  await typeAndSend(ctx, 'baseline turn before any load');
  out.f1.baselineSent = ctx.log.turns.length;
  const first = ctx.log.turns[0] || null;
  out.f1.reservedPath = first ? first.buffers[1].path : null;
  out.f1.baselineKind = first ? first.kind : null;
  out.f1.baselineBound = first ? first.bound_buffer : null;
  out.f1.baselineHasActiveDocumentPath =
    first ? ('active_document_path' in first) : null;

  // Load a DIFFERENT document through the tile's OWN verb -- the one route in,
  // and deliberately one whose key sorts BEFORE the reserved `"document"` key, so
  // an implementation that fell through to "the first loaded document by key
  // order" would pick IT rather than what the human selected (N1).
  const other = [EARLY_A, EARLY_B, DOC_A, DOC_B].find(
    (candidate) => candidate !== out.f1.reservedPath);
  out.f1.loadedPath = other;
  const loaded = await expandTileFor(ctx, other);
  const loadBtn = loaded.tile.querySelector('.swb-docload');
  out.f1.readReachable =
    loaded.tile.querySelector('.swb-docread').disabled !== true;
  out.f1.loadReachable = loadBtn.disabled !== true;
  await fire(loadBtn, 'click');
  await quiesce(60);
  out.f1.verbNote = String((ctx.one('swb-docverbnote') || {}).textContent || '');
  out.f1.textareasAfterLoad = ctx.byClass('doxbench-textarea').length;
  out.f1.statusRegions = ctx.byClass('doxbench-status').map((n) => n.className);

  // The selector now lists BOTH documents and names the loaded one as selected.
  const selectNode = ctx.one('doxchat-loaded');
  out.f1.selectorOptions = selectNode.children.map((o) => o.value);
  out.f1.selectorValue = selectNode.value;

  // …and a send on that selection SUCCEEDS. Under the interim N4 posture this
  // was held closed pre-flight with a stated reason; the widened envelope
  // carries the loaded set and DECLARES the binding, so the turn goes out.
  const attempt = await typeAndSend(ctx, 'what does this document say?');
  out.f1.sendDisabledWhileBound = attempt.disabledBefore;
  out.f1.turnsAfterBoundSend = ctx.log.turns.length;
  const boundRequest = ctx.log.turns[ctx.log.turns.length - 1] || null;
  out.f1.boundKind = boundRequest ? boundRequest.kind : null;
  out.f1.boundBuffer = boundRequest ? boundRequest.bound_buffer : null;
  out.f1.boundWirePaths = boundRequest
    ? boundRequest.buffers.map((b) => b.path) : null;
  out.f1.boundWireKinds = boundRequest
    ? boundRequest.buffers.map((b) => b.kind) : null;
  out.f1.boundHasActiveDocumentPath =
    boundRequest ? ('active_document_path' in boundRequest) : null;

  // Selecting the OUTLINE re-points the binding, and the request still carries
  // every loaded buffer: binding says what the chat works ON, never what it sees.
  const outlineTab = ctx.byClass('swb-tab').find(
    (b) => String(b.textContent).toLowerCase().includes('outline'));
  await fire(outlineTab, 'click');
  await quiesce(40);
  const recovered = await typeAndSend(ctx, 'and the outline?');
  out.f1.sendEnabledOnOutline = recovered.disabledBefore === false;
  out.f1.turnsAfterOutlineSend = ctx.log.turns.length;
  const request = ctx.log.turns[ctx.log.turns.length - 1] || null;
  out.f1.outlineBound = request ? request.bound_buffer : null;
  out.f1.wireBufferKinds = request
    ? request.buffers.map((b) => b.kind) : null;
  out.f1.wireBufferPaths = request
    ? request.buffers.map((b) => b.path) : null;
}

// =====================================================================
// F2: the tile Save on a RESERVED-SLOT document (every restored Phase A session)
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await quiesce(40);
  // Dirty the reserved document buffer through the real editor.
  const editorTab = ctx.byClass('doxbench-viewtab')[0];
  await fire(editorTab, 'click');
  await quiesce(10);
  const area = ctx.byClass('doxbench-textarea')[1];
  area.value = '# edited by the human\n';
  await fire(area, 'input');
  await until(() => ctx.byClass('doxbench-status').some(
    (n) => String(n.textContent || '').includes('unsaved')), 'the dirty buffer');
  await quiesce(20);

  const expanded = await expandTileFor(ctx, DOC_A);
  const saveBtn = expanded.tile.querySelector('.swb-docsave');
  out.f2 = {
    saveReachable: saveBtn.disabled !== true,
    saveTitle: saveBtn.title,
    markedNeedsSave: expanded.tile.classList.contains('swb-docneedssave'),
  };
  await fire(saveBtn, 'click');
  await quiesce(80);
  out.f2.savesAttempted = ctx.log.saves.length;
  out.f2.saveRowKeys = ctx.log.saves.length
    ? (ctx.log.saves[0].buffers || []).map((r) => r.key ?? r.kind) : null;
  out.f2.only = ctx.log.saves.length ? (ctx.log.saves[0].only ?? null) : null;
  out.f2.verbNote = String((ctx.one('swb-docverbnote') || {}).textContent || '');
}

// =====================================================================
// F3: where EDITING is unreachable, load and save state the absence
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A], gate: false });
  await quiesce(60);
  const expanded = await expandTileFor(ctx, DOC_A);
  const read = expanded.tile.querySelector('.swb-docread');
  const load = expanded.tile.querySelector('.swb-docload');
  const save = expanded.tile.querySelector('.swb-docsave');
  out.f3 = {
    canvasMounted: ctx.byClass('doxbench-textarea').length > 0,
    readReachable: read.disabled !== true,
    loadDisabled: load.disabled === true,
    loadTitle: load.title,
    saveDisabled: save.disabled === true,
    saveTitle: save.title,
  };
  await fire(load, 'click');
  await fire(save, 'click');
  await quiesce(20);
  out.f3.nothingHappened = ctx.log.saves.length === 0;
  out.f3.noteStayedSilent =
    String((ctx.one('swb-docverbnote') || { hidden: true }).textContent || '') === '';
}

// =====================================================================
// F6: the selector's empty state, on the state the canvas actually produces
// =====================================================================
{
  // A topic whose ONLY file is its outline: the canvas still builds the reserved
  // `document` slot, with `path: null`. That is the state the ratified empty
  // state describes, and the one a count including the reserved slot could
  // never see.
  const ctx = await mount({ files: [OUTLINE_PATH] });
  await until(() => ctx.one('doxchat-loaded') !== null, 'the selector');
  await quiesce(60);
  const selectNode = ctx.one('doxchat-loaded');
  const emptyNode = ctx.one('doxchat-loaded-empty');
  out.f6 = {
    options: selectNode.children.map((o) => o.value),
    value: selectNode.value,
    emptyHidden: emptyNode.hidden === true,
    emptyText: String(emptyNode.textContent || ''),
    headerAbsent: ctx.one('doxchat-header') === null,
  };
}

// =====================================================================
// F9: the loaded set's one way OUT, and its dirty refusal
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A, DOC_B] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await until(() => ctx.one('doxchat-loaded') !== null, 'the selector');
  await quiesce(40);
  const first = ctx.log.turns;  // unused; keeps the shape symmetrical
  void first;
  // With the reserved slot backed, loading the OTHER document adds a second one.
  const reservedIsA = ctx.byClass('doxbench-textarea')[1].value.includes(DOC_A);
  const other = reservedIsA ? DOC_B : DOC_A;
  const tile = await expandTileFor(ctx, other);
  await fire(tile.tile.querySelector('.swb-docload'), 'click');
  await until(() => ctx.byClass('doxbench-textarea').length === 3,
              'the loaded document its own editor');
  await quiesce(30);
  const unload = ctx.one('doxchat-unload');
  out.f9 = {
    optionsAfterLoad: ctx.one('doxchat-loaded').children.map((o) => o.value),
    reachable: unload.disabled !== true,
    label: unload.textContent,
  };

  // Dirty it, then try to unload: REFUSED, and the control says what a second
  // press would mean.
  const editorTab = ctx.byClass('doxbench-viewtab')[0];
  await fire(editorTab, 'click');
  await quiesce(10);
  const loadedArea = ctx.byClass('doxbench-textarea')[2];
  loadedArea.value = '# unsaved work in the loaded document\n';
  await fire(loadedArea, 'input');
  await quiesce(30);
  await fire(unload, 'click');
  await quiesce(30);
  out.f9.dirtyRefusedNote = String((ctx.one('doxchat-loaded-note') || {}).textContent || '');
  out.f9.stillLoaded = ctx.one('doxchat-loaded').children.map((o) => o.value);
  out.f9.armedLabel = unload.textContent;
  out.f9.armedTitle = unload.title;

  // A SECOND press states the discard, and only then does it leave.
  await fire(unload, 'click');
  await quiesce(40);
  out.f9.afterDiscard = ctx.one('doxchat-loaded').children.map((o) => o.value);
  out.f9.afterNote = String((ctx.one('doxchat-loaded-note') || {}).textContent || '');

  // With the OUTLINE selected the control is unreachable and says why.
  const outlineTab = ctx.byClass('swb-tab').find(
    (b) => String(b.textContent).toLowerCase().includes('outline'));
  await fire(outlineTab, 'click');
  await quiesce(30);
  out.f9.outlineDisabled = ctx.one('doxchat-unload').disabled === true;
  out.f9.outlineTitle = ctx.one('doxchat-unload').title;
}

// =====================================================================
// N3: the RESERVED document slot rides every turn, so it is never unloaded
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A, DOC_B] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await until(() => ctx.one('doxchat-loaded') !== null, 'the selector');
  await quiesce(40);
  await chooseModel(ctx);
  // Select the RESERVED slot -- it is a legitimate, listed, selectable entry, and
  // the chat binds to it. What it is not is unloadable.
  const selectNode = ctx.one('doxchat-loaded');
  selectNode.value = 'document';
  await fire(selectNode, 'change');
  await quiesce(30);
  const unload = ctx.one('doxchat-unload');
  out.n3 = {
    selected: selectNode.value,
    listed: selectNode.children.map((o) => o.value),
    disabled: unload.disabled === true,
    title: unload.title,
  };
  // Press it anyway: the click path refuses too, so the render's disabled state is
  // not the only thing standing between a human and a wedged chat.
  await fire(unload, 'click');
  await quiesce(40);
  out.n3.stillListed = ctx.one('doxchat-loaded').children.map((o) => o.value);
  out.n3.editors = ctx.byClass('doxbench-textarea').length;
  // …and a turn STILL BUILDS, which is the failure this guards: emptying the slot
  // left `buildTurnRequest` reading `buffers.document.path` on an absent buffer,
  // caught as the generic unsettled-buffer failure, so the rail said "still
  // settling; try Send again in a moment" forever.
  const sent = await typeAndSend(ctx, 'a turn after attempting the unload');
  out.n3.turns = ctx.log.turns.length;
  out.n3.failureNote = sent.failure;
  const request = ctx.log.turns[ctx.log.turns.length - 1] || null;
  out.n3.wireDocumentPath = request ? request.buffers[1].path : null;
}

console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def composition(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench composition probe")
    root = tmp_path_factory.mktemp("doxbench-composition")
    views = root / "views"
    shutil.copytree(VIEWS, views)
    shutil.copytree(VENDOR, root / "vendor")
    (root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (root / "vendor" / "package.json").write_text('{"type": "commonjs"}',
                                                  encoding="utf-8")
    harness = views / "composition-harness.mjs"
    harness.write_text(_COMPOSITION_HARNESS, encoding="utf-8")
    done = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=180)
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


# ---------------------------------------------------------------------------
# F1
# ---------------------------------------------------------------------------


def test_loading_a_document_does_not_kill_the_chat(composition):
    """F1's headline: before the fix, loading a document made EVERY subsequent
    turn refuse with the route's fixed redacted `turn_scope_refused` code."""
    f1 = composition["f1"]
    assert f1["readReachable"] is True
    assert f1["loadReachable"] is True
    assert "loaded for editing" in f1["verbNote"]
    # The load really happened: the selector lists the outline, the reserved slot
    # and the newly loaded document, and names the new one as selected.
    assert set(f1["selectorOptions"]) == {"outline", "document", f1["loadedPath"]}
    assert f1["selectorValue"] == f1["loadedPath"]
    # …and the listing is in the DECLARED order, which is what puts the loaded key
    # before the reserved one here and is exactly what makes N1's discrimination
    # possible.
    assert f1["selectorOptions"] == ["outline"] + sorted(
        [key for key in f1["selectorOptions"] if key != "outline"])
    # The baseline turn went out before any of this, which is what makes the
    # reserved slot's path a measured fact rather than an assumption.
    assert f1["baselineSent"] == 1
    assert f1["baselineKind"] == "workbench-chat-turn-v2"


def test_a_turn_bound_to_a_loaded_document_now_sends_and_declares_that_binding(
        composition):
    """THE N4 DISSOLUTION, proven through the REAL MOUNT (task 8.6 -> §13).

    SUPERSEDES the interim posture this test used to pin: under the released v1
    envelope a turn bound to a document loaded beside the tile's own was held
    closed pre-flight, because the wire carried the outline plus one reserved
    slot and could not say which of N buffers the chat was on. The widened
    envelope carries the loaded set and DECLARES the binding, so the same
    selection sends — and the request names that document as the bound buffer.

    Everything here is driven through `mountStagingWorkbench`: a real tile load,
    a real selector, a real send. The stubbed-seam version of this test is what
    hid three broken flows behind 3050 green ones in PR #207."""
    f1 = composition["f1"]
    assert f1["sendDisabledWhileBound"] is False, (
        "the interim binding gate is retired: Send is reachable on a selection "
        "the widened envelope can carry")
    assert f1["turnsAfterBoundSend"] == 2, (
        "the baseline turn plus this one: the selection now reaches the transport")
    assert f1["boundKind"] == "workbench-chat-turn-v2"
    assert f1["boundBuffer"] == f1["loadedPath"], (
        "the DECLARED binding is the buffer the human selected")
    # N1: the loaded document's KEY sorts BEFORE the reserved `"document"` key, so
    # an implementation that fell through to "the first document by key order"
    # could not be told from one that read the selection. The fixture makes that
    # discrimination possible.
    assert f1["loadedPath"] < "document", (
        "the fixture must load a key that sorts before the reserved one, or this "
        "assertion cannot tell a declared binding from a lucky sort order")
    # GROUNDING is unnarrowed: the outline, the reserved slot and the loaded
    # document all ride the request.
    assert f1["boundWireKinds"] == ["outline", "document", "document"]
    assert f1["loadedPath"] in f1["boundWirePaths"]
    assert f1["reservedPath"] in f1["boundWirePaths"]


def test_the_widened_wire_declares_its_binding_and_carries_no_active_path(
        composition):
    """D17, proven on the REQUEST rather than described: the binding the record
    will name is DECLARED on the wire, and the field Phase A's review found it
    mis-derived from is not on this envelope at all — so there is nothing left to
    infer it from, on any turn, whichever buffer is selected."""
    f1 = composition["f1"]
    assert f1["baselineHasActiveDocumentPath"] is False
    assert f1["boundHasActiveDocumentPath"] is False
    # Selecting the outline re-points the binding immediately, with no
    # confirmation step and no reload…
    assert f1["sendEnabledOnOutline"] is True
    assert f1["turnsAfterOutlineSend"] == 3
    assert f1["outlineBound"] == "outline"
    # …and the same three buffers still ride it. Binding names what the chat
    # works ON; it never narrows what the turn may be grounded on.
    assert f1["wireBufferKinds"] == ["outline", "document", "document"]
    assert f1["loadedPath"] in f1["wireBufferPaths"]
    assert f1["reservedPath"] in f1["wireBufferPaths"]


# ---------------------------------------------------------------------------
# F2
# ---------------------------------------------------------------------------


def test_the_tile_save_reaches_the_pipeline_for_a_reserved_slot_document(
        composition):
    """F2: `bufferStateFor` resolves the buffer BY PATH and returns the KEY it is
    held under; `saveDocument` takes the KEY. The two differ for exactly the buffer
    every restored Phase A session holds — a real document under the reserved
    `document` key — so passing the path made the control enabled and then
    refused."""
    f2 = composition["f2"]
    assert f2["markedNeedsSave"] is True
    assert f2["saveReachable"] is True
    assert f2["savesAttempted"] == 1, (
        "the tile Save must actually reach the governed pipeline")
    assert f2["saveRowKeys"] == ["document"], (
        "the row is keyed by the reserved key the buffer is held under")
    # Design D4: the act is SCOPED to that document plus the ancestry step. The
    # scope may be a key or a list of keys -- `runSave` accepts either -- so what
    # is asserted is that it names EXACTLY this document and no other.
    only = f2["only"]
    assert (only == "document" or only == ["document"]), only
    assert "saved through the governed Save" in f2["verbNote"]


# ---------------------------------------------------------------------------
# F3
# ---------------------------------------------------------------------------


def test_where_editing_is_unreachable_the_tile_states_it_and_read_remains(
        composition):
    """F3: `docTileVerbs()` used to return live functions unconditionally, so a
    gate-off surface failed ON ACTIVATION with the wrong sentence — the exact
    posture the ratified requirement forbids. Read needs no gate capability and
    stays."""
    f3 = composition["f3"]
    assert f3["canvasMounted"] is False, (
        "gate-off must not mount an editing canvas at all")
    assert f3["readReachable"] is True, (
        "read needs no gate capability and must stay available")
    assert f3["loadDisabled"] is True
    assert f3["saveDisabled"] is True
    assert "editing capability" in f3["loadTitle"]
    assert "editing capability" in f3["saveTitle"]
    assert f3["nothingHappened"] is True
    assert f3["noteStayedSilent"] is True, (
        "an unreachable verb states its absence; it does not report an outcome")


# ---------------------------------------------------------------------------
# F6
# ---------------------------------------------------------------------------


def test_the_selector_empty_state_renders_on_the_state_the_canvas_produces(
        composition):
    """F6: the canvas builds the reserved `document` slot in EVERY state, and while
    its path is null it is the create flow's not-yet-created artifact — not a
    loaded document. Counting it made `documentCount` never zero, so the ratified
    "no document is loaded" sentence could never render on any real surface."""
    f6 = composition["f6"]
    assert f6["options"] == ["outline"], (
        "a buffer nobody loaded must not be listed as loaded")
    assert f6["value"] == "outline"
    assert f6["emptyHidden"] is False
    assert "no document is loaded" in f6["emptyText"]
    assert "outline is workable on its own" in f6["emptyText"]
    # Brett's 2026-08-21 annotation removed the standing header line, so the
    # count it used to claim is now carried by the empty state asserted just
    # above — the same fact, on the surface that survived. Pinned as an ABSENCE
    # rather than deleted, so a re-introduced header line fails here.
    assert f6["headerAbsent"] is True, (
        "the standing 'Working on — … · Chatting about — …' line is removed; "
        "the selector and its empty state state the binding now")


# ---------------------------------------------------------------------------
# F9
# ---------------------------------------------------------------------------


def test_a_loaded_document_can_be_unloaded_and_a_dirty_one_refuses_first(
        composition):
    """F9: the ratified loaded-set requirement says "a document SHALL leave the
    loaded set only by an explicit human act, and that act MUST refuse or require
    an explicit discard while the buffer is dirty". The state primitive shipped
    with no control at all, so the act did not exist — and the declared bound was
    a dead end, because a session that reached it could never get back under it.

    The control lives beside the selector, which is the surface that presents the
    loaded set, and an irreversible discard is never one unannounced click: the
    first press REFUSES and the label changes to say what the second one means."""
    f9 = composition["f9"]
    # Two documents are loaded, and the control is reachable for the selected one.
    assert len(f9["optionsAfterLoad"]) == 3
    assert f9["reachable"] is True
    assert f9["label"] == "Unload"

    # Dirty: refused, nothing dropped, and the control re-labels itself.
    assert "unsaved" in f9["dirtyRefusedNote"]
    assert f9["stillLoaded"] == f9["optionsAfterLoad"], (
        "a refused unload must drop nothing")
    assert f9["armedLabel"] == "Discard and unload"
    assert "press again to DISCARD" in f9["armedTitle"]

    # The second press states the discard, and only then does the buffer leave.
    assert len(f9["afterDiscard"]) == 2
    assert "unloaded" in f9["afterNote"]


def test_the_outline_is_never_unloadable(composition):
    """Its key is permanently reserved and it is the one buffer that rides every
    turn, so the control states that rather than offering an act it must refuse."""
    f9 = composition["f9"]
    assert f9["outlineDisabled"] is True
    assert "reserved buffer" in f9["outlineTitle"]


# ---------------------------------------------------------------------------
# N3
# ---------------------------------------------------------------------------


def test_the_reserved_document_slot_is_selectable_but_never_unloadable(
        composition):
    """N3 (PR #207 re-verification): the reserved `document` key was listed as an
    ORDINARY loaded entry whenever it carried a path, so Unload was reachable for
    it — and one click emptied the slot, after which `buildTurnRequest` read
    `buffers.document.path` on an absent buffer. That threw, was caught as the
    generic unsettled-buffer failure, and the rail then said "the buffers are
    still settling; try Send again in a moment" FOREVER: a permanently false
    sentence, which is the worst thing a refusal can be.

    RE-REASONED at contract-v1.34 (F7, adversarial review of the §13 slice). The
    guard stands; the reason it stands changed with the wire. It used to be that
    the released envelope carried exactly the outline and this slot, so emptying
    the slot left the request builder reading an absent buffer. The widened
    envelope carries the whole loaded set, and the floor is now stated in two
    places that agree: `request_v2.buffers` declares `minItems: 2`, and the
    server's `require_outline_and_documents` requires an outline plus AT LEAST
    ONE document. A session holding only the outline and this slot therefore has
    no document to spare. Listing it stays right: it is selectable and the chat
    binds to it."""
    n3 = composition["n3"]
    # It IS a first-class, listed, selectable entry.
    assert "document" in n3["listed"]
    assert n3["selected"] == "document"
    # …and Unload is withheld for it, with the reason naming why.
    assert n3["disabled"] is True
    assert "never unloaded" in n3["title"]
    assert "load another document to work beside it" in n3["title"]
    # Pressing it anyway changes nothing: the click path refuses too.
    assert n3["stillListed"] == n3["listed"]
    assert n3["editors"] >= 2
    # And the chat is not wedged: a turn builds, reaches the transport, and carries
    # the reserved slot's own path exactly as it did before.
    assert n3["turns"] == 1
    assert n3["wireDocumentPath"] is not None
    assert "still settling" not in n3["failureNote"], (
        "the wedged-chat sentence must be unreachable")
