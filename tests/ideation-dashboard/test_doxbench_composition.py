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
  // Amendment 1: the act is the CANVAS slot's now. One reader for all three of
  // its occupancies, so each state is measured the same way.
  const slot = () => ({
    unloadHidden: ctx.one('doxbench-unload').hidden === true,
    unloadDisabled: ctx.one('doxbench-unload').disabled === true,
    unloadTitle: String(ctx.one('doxbench-unload').title || ''),
    // F7: the reason as VISIBLE text, not only a hover title -- an inert button
    // cannot take focus, so a title alone reaches nobody.
    unloadNoteHidden: ctx.one('doxbench-unload-note').hidden === true,
    unloadNoteText: String(ctx.one('doxbench-unload-note').textContent || ''),
    saveHidden: ctx.one('doxbench-save').hidden === true,
    cancelHidden: ctx.one('doxbench-cancel').hidden === true,
  });
  // STATE: nothing dirty, a loaded document selected -> Unload, alone.
  out.f9 = {
    optionsAfterLoad: ctx.one('doxchat-loaded').children.map((o) => o.value),
    clean: slot(),
    railControlGone: ctx.one('doxchat-unload') === null,
    // F6: the control must NAME the buffer it would act on, so the probe records
    // which document is actually selected and the assertion compares the two.
    selectedWhenClean: ctx.one('doxchat-loaded').value,
  };

  // STATE: dirty -> Save and Cancel come back and Unload GOES AWAY. This is the
  // amended dirty-refusal discharge: the act is not reachable at all while a
  // buffer holds unsaved work, so there is no press to refuse.
  const editorTab = ctx.byClass('doxbench-viewtab')[0];
  await fire(editorTab, 'click');
  await quiesce(10);
  const loadedArea = ctx.byClass('doxbench-textarea')[2];
  loadedArea.value = '# unsaved work in the loaded document\n';
  await fire(loadedArea, 'input');
  await quiesce(30);
  out.f9.dirty = slot();
  out.f9.dirtyStillLoaded = ctx.one('doxchat-loaded').children.map((o) => o.value);

  // Cancel it back to clean, and the slot swaps again.
  await fire(ctx.one('doxbench-cancel'), 'click');
  await quiesce(40);
  out.f9.afterCancel = slot();

  // …and NOW the act runs: the document leaves the set.
  await fire(ctx.one('doxbench-unload'), 'click');
  await quiesce(40);
  out.f9.afterUnload = ctx.one('doxchat-loaded').children.map((o) => o.value);
  out.f9.editorsAfterUnload = ctx.byClass('doxbench-textarea').length;
  // `unloadDocumentBuffer` moves the selection to the outline when the unloaded
  // buffer held it, so the slot lands on the reserved-outline posture.
  out.f9.selectionAfterUnload = ctx.one('doxchat-loaded').value;
  out.f9.outline = slot();
}

// =====================================================================
// F10 (Amendment 1): the swap reads ANY-buffer-dirty, not selected-buffer-dirty.
// A human whose OUTLINE holds unsaved text, standing on a CLEAN loaded document,
// must still be able to see Save. Under a selected-buffer rule the slot would
// show Unload here and the only Save on the surface would be hidden behind a
// selection change nobody told them to make.
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A, DOC_B] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await until(() => ctx.one('doxchat-loaded') !== null, 'the selector');
  await quiesce(40);
  // Dirty the OUTLINE, which is the buffer selected at mount.
  const editorTab = ctx.byClass('doxbench-viewtab')[0];
  await fire(editorTab, 'click');
  await quiesce(10);
  const outlineArea = ctx.byClass('doxbench-textarea')[0];
  outlineArea.value = '# unsaved outline work\n';
  await fire(outlineArea, 'input');
  await quiesce(30);
  // Now LOAD a document, which selects it. A load replaces nothing, so the
  // outline keeps its unsaved bytes while the selection moves to a CLEAN buffer.
  const reservedIsA = ctx.byClass('doxbench-textarea')[1].value.includes(DOC_A);
  const other = reservedIsA ? DOC_B : DOC_A;
  const tile = await expandTileFor(ctx, other);
  await fire(tile.tile.querySelector('.swb-docload'), 'click');
  await until(() => ctx.byClass('doxbench-textarea').length === 3,
              'the loaded document its own editor');
  await quiesce(40);
  out.f10 = {
    selected: ctx.one('doxchat-loaded').value,
    selectedIsClean: ctx.one('doxchat-loaded').value !== 'outline',
    unloadHidden: ctx.one('doxbench-unload').hidden === true,
    saveHidden: ctx.one('doxbench-save').hidden === true,
    cancelHidden: ctx.one('doxbench-cancel').hidden === true,
    saveDisabled: ctx.one('doxbench-save').disabled === true,
    // Cancel is scoped to the SELECTED buffer, which is clean -- so it is on
    // screen and inert, which is the honest pair for this state.
    cancelDisabled: ctx.one('doxbench-cancel').disabled === true,
  };
}

// =====================================================================
// F9 (adversarial review): ONE loaded-set tail per act. `onLoadedSetChanged` is
// the canvas's declared notification for "the loaded SET or the SELECTION
// changed", and the shell's tail behind it re-syncs the context and redraws the
// docs tiles. Two spellings of that tail -- the notification AND an explicit
// call pair inside each seam -- is the exact criticism that retired the old
// `unloadBuffer` seam, so it is measured rather than assumed. A counting wrapper
// on the wheel's own `__docWheelRefresh` is the honest instrument: it is the
// thing the tail actually drives.
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A, DOC_B] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await until(() => ctx.one('doxchat-loaded') !== null, 'the selector');
  await quiesce(40);
  const pane = ctx.container.walk().find((n) => n.__docWheel);
  const real = pane.__docWheelRefresh;
  let refreshes = 0;
  pane.__docWheelRefresh = (...args) => { refreshes += 1; return real.apply(pane, args); };
  const measure = async (act) => {
    refreshes = 0;
    await act();
    await quiesce(40);
    return refreshes;
  };

  // LOAD. `expandTileFor` drives its own refreshes to lay the tile out, so the
  // counter is zeroed inside `measure`, after the expansion, by measuring only
  // the verb click itself.
  const reservedIsA = ctx.byClass('doxbench-textarea')[1].value.includes(DOC_A);
  const other = reservedIsA ? DOC_B : DOC_A;
  const tile = await expandTileFor(ctx, other);
  const loadVerb = tile.tile.querySelector('.swb-docload');
  const onLoad = await measure(async () => {
    await fire(loadVerb, 'click');
    await until(() => ctx.byClass('doxbench-textarea').length === 3,
                'the loaded document its own editor');
  });

  // SELECT, through the rail selector's seam.
  const selectNode = ctx.one('doxchat-loaded');
  const onSelect = await measure(async () => {
    selectNode.value = 'outline';
    await fire(selectNode, 'change');
  });

  // UNLOAD, through the canvas slot. Select the loaded document back first --
  // that selection is itself an act and is not part of the unload's count.
  selectNode.value = other;
  await fire(selectNode, 'change');
  await quiesce(40);
  const onUnload = await measure(async () => {
    await fire(ctx.one('doxbench-unload'), 'click');
  });

  // RE-LOAD OF AN ALREADY-LOADED DOCUMENT. Corrected after the R1 review: an
  // earlier version of this block called itself a "docs-row switch" and claimed
  // to drive `switchDocument`. It does not, and cannot -- by this point the
  // reserved slot is backed, so the load verb takes
  // `loadDocumentForEditing`'s ALREADY-LOADED short-circuit, which selects the
  // held buffer through `setActiveBuffer` and never reaches `switchDocument` at
  // all. The measurement was always valid as an ACT; only its stated route was
  // wrong, and a comment naming the wrong route is how the next reader
  // "verifies" a path nothing exercises.
  //
  // `switchDocument`'s own two shapes are counted where they can actually be
  // reached -- at the canvas module, in
  // `test_doxbench_view.py::test_one_loaded_set_notify_per_switch_whichever_shape`.
  const heldTile = await expandTileFor(ctx, reservedIsA ? DOC_A : DOC_B);
  const heldVerbHost = heldTile.tile;
  const onReloadHeld = await measure(async () => {
    const verb = heldVerbHost.querySelector('.swb-docload');
    if (verb) await fire(verb, 'click');
  });

  out.refreshCounts = { onLoad, onSelect, onUnload, onReloadHeld };
}

// =====================================================================
// N3, RE-RULED BY AMENDMENT 2 (2026-08-21, Brett, browser annotation): the
// BACKED reserved `document` slot unloads like any other document once it is
// back in the neutral position. "only the outline can never unload."
//
// Driven as BRETT REPORTED IT: edit the tile's own document, CANCEL instead of
// saving, then unload. That is the sequence that came back stippled.
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A, DOC_B] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await until(() => ctx.one('doxchat-loaded') !== null, 'the selector');
  await quiesce(40);
  await chooseModel(ctx);
  // Select the RESERVED slot -- a legitimate, listed, selectable entry the chat
  // binds to, and now an unloadable one.
  const selectNode = ctx.one('doxchat-loaded');
  selectNode.value = 'document';
  await fire(selectNode, 'change');
  await quiesce(30);
  const slot = () => ({
    rendered: ctx.one('doxbench-unload').hidden !== true,
    disabled: ctx.one('doxbench-unload').disabled === true,
    title: String(ctx.one('doxbench-unload').title || ''),
    noteHidden: ctx.one('doxbench-unload-note').hidden === true,
    saveHidden: ctx.one('doxbench-save').hidden === true,
    cancelHidden: ctx.one('doxbench-cancel').hidden === true,
  });
  out.n3 = {
    selected: selectNode.value,
    listed: selectNode.children.map((o) => o.value),
    clean: slot(),
  };
  // EDIT it. The pair comes back and Unload goes away -- unchanged by Amendment
  // 2, which narrowed WHICH KEYS are reachable, never the dirty rule.
  await fire(ctx.byClass('doxbench-viewtab')[0], 'click');
  await quiesce(10);
  const area = ctx.byClass('doxbench-textarea')[1];
  area.value = '# the tile document, edited\n';
  await fire(area, 'input');
  await quiesce(30);
  out.n3.dirty = slot();
  // CANCEL -- not Save. The buffer returns to its base text, which is the
  // "neutral position" the ruling names.
  await fire(ctx.one('doxbench-cancel'), 'click');
  await quiesce(40);
  out.n3.afterCancel = slot();
  // …and NOW the act runs, on the tile's own document.
  await fire(ctx.one('doxbench-unload'), 'click');
  await quiesce(40);
  out.n3.listedAfter = ctx.one('doxchat-loaded').children.map((o) => o.value);
  out.n3.emptyNote = String((ctx.one('doxchat-loaded-empty') || {}).textContent || '');
  out.n3.editors = ctx.byClass('doxbench-textarea').length;
  // The chat is NOT wedged. The turn builds, reaches the transport, and carries
  // the outline it bound to -- the old v1 failure (an absent buffer read inside
  // the request builder, reported forever as "still settling") is unreachable.
  const sent = await typeAndSend(ctx, 'a turn after the unload');
  out.n3.turns = ctx.log.turns.length;
  out.n3.failureNote = sent.failure;
  const request = ctx.log.turns[ctx.log.turns.length - 1] || null;
  out.n3.wireBufferKinds = request ? request.buffers.map((b) => b.kind) : null;
  out.n3.wireBound = request ? request.bound_buffer : null;
}

// =====================================================================
// N3b (Amendment 2): the OTHER neutral position -- SAVED rather than cancelled.
// "If saved or canceled so the document is in neutral position, then we can
// unload it." Same slot, same act, reached through the governed Save.
// =====================================================================
{
  const ctx = await mount({ files: [OUTLINE_PATH, DOC_A] });
  await until(() => ctx.byClass('doxbench-textarea').length >= 2, 'the canvas');
  await until(() => ctx.one('doxchat-loaded') !== null, 'the selector');
  await quiesce(40);
  const selectNode = ctx.one('doxchat-loaded');
  selectNode.value = 'document';
  await fire(selectNode, 'change');
  await quiesce(30);
  await fire(ctx.byClass('doxbench-viewtab')[0], 'click');
  await quiesce(10);
  const area = ctx.byClass('doxbench-textarea')[1];
  area.value = '# the tile document, edited then saved\n';
  await fire(area, 'input');
  await quiesce(30);
  out.n3b = {
    dirtyUnloadHidden: ctx.one('doxbench-unload').hidden === true,
    saveHidden: ctx.one('doxbench-save').hidden === true,
  };
  await fire(ctx.one('doxbench-save'), 'click');
  // POLL the transition the assertion is about -- the slot swapping back once
  // every buffer has rebased clean -- rather than a fixed delay that hopes it.
  await until(() => ctx.one('doxbench-unload').hidden !== true,
              'the Save to settle and the slot to swap back');
  await quiesce(20);
  out.n3b.saves = ctx.log.saves.length;
  out.n3b.afterSaveDisabled = ctx.one('doxbench-unload').disabled === true;
  out.n3b.afterSaveTitle = String(ctx.one('doxbench-unload').title || '');
  await fire(ctx.one('doxbench-unload'), 'click');
  await quiesce(40);
  out.n3b.listedAfter = ctx.one('doxchat-loaded').children.map((o) => o.value);
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


def test_the_canvas_slot_shows_unload_only_while_nothing_is_dirty(composition):
    """F9, RE-CUT by Amendment 1 (Brett, 2026-08-21): the loaded set's one way out
    moved from the chat rail onto the CANVAS control slot, and the slot's
    occupancy is now the whole answer to "is this canvas holding unsaved work".

    STATE 1 (clean, a loaded document selected): Unload alone.
    STATE 2 (anything dirty): Save and Cancel, and NO Unload — which is the
    amended discharge of the loaded-set requirement's dirty clause. The old
    two-press arm flow refused a press; withholding the control refuses the act
    itself, which is strictly stronger and leaves nothing to press by mistake."""
    f9 = composition["f9"]
    assert f9["railControlGone"] is True, (
        "the rail's standalone unload control is superseded")
    # Two documents are loaded (plus the outline entry).
    assert len(f9["optionsAfterLoad"]) == 3

    # STATE 1 — clean: Unload alone, reachable, naming what it would unload.
    assert f9["clean"]["unloadHidden"] is False
    assert f9["clean"]["unloadDisabled"] is False
    # It NAMES the selected document, not just the act (F6). The scenario says
    # the control "MUST name the selected document it would unload", so the
    # assertion compares the title against the selection rather than against a
    # constant tail that any buffer would satisfy.
    assert f9["clean"]["unloadTitle"] == (
        "unload " + f9["selectedWhenClean"] + " from the loaded set")
    assert f9["selectedWhenClean"] != "outline"
    # Reachable: the control speaks for itself, so no standing reason beside it.
    assert f9["clean"]["unloadNoteHidden"] is True
    assert f9["clean"]["saveHidden"] is True
    assert f9["clean"]["cancelHidden"] is True

    # STATE 2 — dirty: the pair returns and Unload is GONE. Nothing is dropped.
    assert f9["dirty"]["saveHidden"] is False
    assert f9["dirty"]["cancelHidden"] is False
    assert f9["dirty"]["unloadHidden"] is True, (
        "a dirty canvas must not offer the unload act at all")
    assert f9["dirty"]["unloadNoteHidden"] is True, (
        "a reason for a control that is not on screen explains nothing")
    assert f9["dirtyStillLoaded"] == f9["optionsAfterLoad"], (
        "going dirty must drop nothing")

    # Back to clean, and the slot swaps back.
    assert f9["afterCancel"]["unloadHidden"] is False
    assert f9["afterCancel"]["saveHidden"] is True


def test_the_canvas_unload_actually_unloads_and_selection_falls_to_the_outline(
        composition):
    """The act still performs, and it performs exactly what `unloadDocumentBuffer`
    defines: the document leaves the set, and because the unloaded buffer held the
    selection, the selection moves to the reserved outline."""
    f9 = composition["f9"]
    assert len(f9["afterUnload"]) == 2, "the document must leave the loaded set"
    assert f9["selectionAfterUnload"] == "outline"
    # The panes keep their boxes for a cheap re-load, so the editor count is not
    # the membership answer — the selector's listing above is.
    assert f9["editorsAfterUnload"] >= 2


def test_the_swap_reads_any_buffer_dirty_not_the_selected_buffer(composition):
    """Amendment 1 states the predicate explicitly, because the two readings of
    Brett's "if there is a change to save or cancel" differ exactly here.

    Save answers for the WHOLE canvas. With the outline dirty and a CLEAN loaded
    document selected, a selected-buffer rule would swap the slot to Unload and
    hide the only Save on the surface from a human who still has unsaved outline
    text — the precise hazard the discard rules exist to prevent. Any-buffer-dirty
    keeps the pair on screen: Save live because something needs saving, Cancel
    inert because the buffer they are standing on does not."""
    f10 = composition["f10"]
    assert f10["selectedIsClean"] is True, (
        "the probe must be standing on the loaded document, not the outline")
    assert f10["unloadHidden"] is True, (
        "a dirty outline must not be hidden behind an Unload-only slot")
    assert f10["saveHidden"] is False
    assert f10["saveDisabled"] is False, (
        "Save answers for the whole canvas, and the outline is dirty")
    assert f10["cancelHidden"] is False
    assert f10["cancelDisabled"] is True, (
        "Cancel is scoped to the selected buffer, which is clean")


def test_the_outline_is_never_unloadable(composition):
    """Its key is permanently reserved and it is the one buffer that rides every
    turn, so the control STATES that rather than offering an act it must refuse.

    Amendment 1 keeps this posture and moves it: the control is RENDERED and
    visibly inert rather than absent, because an absent control answers no
    question and a slot that emptied itself would collapse the row on every
    selection change."""
    f9 = composition["f9"]
    assert f9["outline"]["unloadHidden"] is False, (
        "the reserved posture is inert-and-stated, never absent")
    assert f9["outline"]["unloadDisabled"] is True
    assert "reserved buffer" in f9["outline"]["unloadTitle"]
    # …and the reason is VISIBLE text beside it, not only the hover title (F7):
    # the control is disabled, so it cannot take focus to reveal one.
    assert f9["outline"]["unloadNoteHidden"] is False
    assert f9["outline"]["unloadNoteText"] == f9["outline"]["unloadTitle"]
    assert "reserved buffer" in f9["outline"]["unloadNoteText"]
    assert f9["outline"]["saveHidden"] is True


# ---------------------------------------------------------------------------
# N3
# ---------------------------------------------------------------------------


def test_the_backed_reserved_slot_unloads_after_an_edit_is_cancelled(
        composition):
    """AMENDMENT 2 (2026-08-21, Brett, ruled via browser annotation): "if I do
    the workflow to edit a document, and then cancel instead of save, then try to
    unload, the unload button is stippled. It should allow the document to
    unload. only the outline can never unload. we always want that to be loaded.
    If saved or canceled so the document is in neutral position, then we can
    unload it."

    This test is the sequence Brett reported, driven end to end through the real
    composition: select the tile's own document under the reserved `document`
    key, edit it, CANCEL, and unload. It used to come back stippled.

    WHAT THE RULING REPLACED. N3 (PR #207) found that emptying this slot under
    the v1 envelope left `buildTurnRequest` reading `buffers.document.path` on an
    absent buffer — caught as the generic unsettled-buffer failure, so the rail
    said "the buffers are still settling; try Send again in a moment" FOREVER, a
    permanently false sentence. The withholding was re-reasoned at contract-v1.34
    (F7) onto the ONE-DOCUMENT FLOOR instead: `request_v2.buffers` declares
    `minItems: 2` and the server requires an outline plus at least one document.

    Both facts survive the amendment and neither justifies the withholding any
    longer. The v1 wedge is gone with the envelope — the widened builder carries
    whatever the set holds and reads no absent buffer, which the send at the end
    of this test measures. The floor is real and still stated in both places, but
    it is a WIRE bound, and a wire bound is discharged by refusing at send with
    the composer preserved, not by making a clean document permanently
    unremovable. The rail states the honest empty state in the same breath."""
    n3 = composition["n3"]
    # It IS a first-class, listed, selectable entry — unchanged.
    assert "document" in n3["listed"]
    assert n3["selected"] == "document"
    # CLEAN: the slot shows Unload, REACHABLE, naming the document it would act
    # on rather than stating a reservation it no longer has.
    assert n3["clean"]["rendered"] is True
    assert n3["clean"]["disabled"] is False, (
        "Amendment 2: a backed reserved-slot document in the neutral position "
        "unloads like any other document")
    assert n3["clean"]["title"].startswith("unload ")
    assert "from the loaded set" in n3["clean"]["title"]
    assert n3["clean"]["noteHidden"] is True, (
        "a reachable control speaks for itself; the note is for inert ones")
    # DIRTY: the pair returns and Unload leaves. Amendment 2 narrowed WHICH KEYS
    # are reachable and touched the dirty rule not at all.
    assert n3["dirty"]["rendered"] is False
    assert n3["dirty"]["saveHidden"] is False
    assert n3["dirty"]["cancelHidden"] is False
    # CANCELLED — Brett's word, and the state his annotation was made in.
    assert n3["afterCancel"]["rendered"] is True
    assert n3["afterCancel"]["disabled"] is False, (
        "the annotated defect exactly: cancelled back to neutral and still "
        "stippled")
    # …and the act runs.
    assert n3["listedAfter"] == ["outline"], (
        "the tile's own document left the loaded set")
    assert n3["editors"] >= 2, (
        "the boxes stay, blanked and hidden, so a re-load reuses them")
    # The ratified empty state renders honestly the moment the set empties.
    assert "no document is loaded" in n3["emptyNote"]
    # THE CHAT IS NOT WEDGED. The turn builds, reaches the transport, binds to
    # the outline, and nothing says the permanently false sentence.
    assert n3["turns"] == 1
    assert n3["wireBufferKinds"] == ["outline"]
    assert n3["wireBound"] == "outline"
    assert "still settling" not in n3["failureNote"], (
        "the wedged-chat sentence must be unreachable")


def test_the_backed_reserved_slot_unloads_after_a_save(composition):
    """The other neutral position the ruling names: "If saved or canceled … then
    we can unload it." Same slot, same act, reached through the governed Save
    rather than through Cancel — because "neutral" is a property of the BUFFER,
    not of which control put it there."""
    n3b = composition["n3b"]
    # Dirty: the pair, no Unload.
    assert n3b["dirtyUnloadHidden"] is True
    assert n3b["saveHidden"] is False
    # Saved: one governed Save ran, and the slot came back with a REACHABLE
    # Unload naming the document.
    assert n3b["saves"] == 1
    assert n3b["afterSaveDisabled"] is False
    assert n3b["afterSaveTitle"].startswith("unload ")
    assert n3b["listedAfter"] == ["outline"]


def test_one_loaded_set_tail_runs_per_act(composition):
    """F9 (adversarial review): `onLoadedSetChanged` is the ONE tail. It was
    introduced beside the two explicit `syncContextFromCanvas(); refreshDocTiles()`
    call pairs the seams already ran, so every pre-existing act redrew the wheel
    twice — idempotent, but two spellings of one tail, which is the exact
    criticism that retired the `unloadBuffer` seam. Measured on a counting
    wrapper around the wheel's own refresh, because "it is idempotent" is not an
    argument for doing it twice.

    These are the acts reachable THROUGH THE SHELL. `switchDocument`'s own two
    shapes cannot be driven from here — once the reserved slot is backed, the
    load verb takes the already-loaded short-circuit — so they are counted at the
    canvas module in
    `test_doxbench_view.py::test_one_loaded_set_notify_per_switch_whichever_shape`
    instead of being claimed here."""
    counts = composition["refreshCounts"]
    expected = {"onLoad": 1, "onSelect": 1, "onUnload": 1, "onReloadHeld": 1}
    assert counts == expected, (
        "each act must drive exactly one wheel refresh; measured " + str(counts))
