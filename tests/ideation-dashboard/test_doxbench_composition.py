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
// F1: loading a document must not kill the chat
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A, DOC_B] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await until(() => ctx.one('doxchat-header') !== null, 'the chat rail');
  await quiesce(40);
  await chooseModel(ctx);
  out.f1 = {};

  // A BASELINE turn first, so the reserved slot's own path is read off the WIRE
  // rather than assumed: whichever document the projection made active at mount
  // is the one the released envelope carries, and that is the fact under test.
  const baseline = await typeAndSend(ctx, 'baseline turn before any load');
  out.f1.baselineSent = ctx.log.turns.length;
  const first = ctx.log.turns[0] || null;
  out.f1.reservedPath = first ? first.buffers[1].path : null;
  out.f1.baselineActiveDocumentPath = first ? first.active_document_path : null;

  // Load a DIFFERENT document through the tile's OWN verb -- the one route in.
  const other = out.f1.reservedPath === DOC_B ? DOC_A : DOC_B;
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

  // …and a send is REFUSED PRE-FLIGHT, with our own stated reason, having
  // consulted no transport at all.
  const attempt = await typeAndSend(ctx, 'what does this document say?');
  out.f1.sendDisabledWhileBound = attempt.disabledBefore;
  out.f1.turnsAfterBoundSend = ctx.log.turns.length;
  out.f1.statedReason = attempt.title;
  out.f1.statedInDescribedBy = attempt.unavailable;

  // Selecting the OUTLINE makes the chat sendable again, and the request names
  // the RESERVED SLOT's path -- never the loaded document's.
  const outlineTab = ctx.byClass('swb-tab').find(
    (b) => String(b.textContent).toLowerCase().includes('outline'));
  await fire(outlineTab, 'click');
  await quiesce(40);
  const recovered = await typeAndSend(ctx, 'and the outline?');
  out.f1.sendEnabledOnOutline = recovered.disabledBefore === false;
  out.f1.turnsAfterOutlineSend = ctx.log.turns.length;
  const request = ctx.log.turns[ctx.log.turns.length - 1] || null;
  out.f1.wireActiveDocumentPath = request ? request.active_document_path : null;
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
    header: String((ctx.one('doxchat-header') || {}).textContent || ''),
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
    assert f1["selectorOptions"] == ["outline", "document", f1["loadedPath"]]
    assert f1["selectorValue"] == f1["loadedPath"]
    # The baseline turn went out before any of this, which is what makes the
    # reserved slot's path a measured fact rather than an assumption.
    assert f1["baselineSent"] == 1
    assert f1["baselineActiveDocumentPath"] == f1["reservedPath"]


def test_a_turn_bound_to_a_loaded_document_is_refused_pre_flight_and_says_why(
        composition):
    """The house degraded-posture idiom (design §3.4): a capability that is absent
    SAYS SO and consults nothing. Never a redacted governance refusal for a
    limitation of our own wire."""
    f1 = composition["f1"]
    assert f1["sendDisabledWhileBound"] is True, (
        "Send must be closed before the click, not refused after it")
    assert f1["turnsAfterBoundSend"] == 1, (
        "only the baseline turn: the bound-to-loaded attempt consulted no "
        "transport, no route and no provider")
    for surface in (f1["statedReason"], f1["statedInDescribedBy"]):
        assert "released turn envelope" in surface
        assert "select the outline or the tile's own document" in surface
        # …and it says what still works, because the editors and the loaded set
        # are genuinely unaffected.
        assert "Editing, Save and" in surface


def test_the_released_wire_only_ever_names_the_reserved_slots_path(composition):
    """The invariant the fix restores, proven on the REQUEST: the released v1
    envelope carries the outline and the reserved `document` slot, so
    `active_document_path` names the reserved slot's own path — even with another
    document loaded and even when the human is standing on the outline."""
    f1 = composition["f1"]
    assert f1["sendEnabledOnOutline"] is True
    assert f1["turnsAfterOutlineSend"] == 2, (
        "the baseline turn plus this one; the bound-to-loaded attempt sent none")
    assert f1["wireBufferKinds"] == ["outline", "document"]
    assert f1["wireActiveDocumentPath"] == f1["reservedPath"]
    assert f1["wireBufferPaths"][1] == f1["reservedPath"]
    # The loaded document is NOT on the wire, which is exactly why the chat
    # cannot be bound to it yet.
    assert f1["loadedPath"] not in f1["wireBufferPaths"]


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
    assert "0 loaded documents" in f6["header"]


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
