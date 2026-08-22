"""The outline tab's templated section index and add-section affordance, driven
through the REAL composition (add-staged-topic-outline-template tasks 3.2-3.5,
asserted by task 4.4).

Why the real composition and not a stub. Task 3.2's whole claim is a WIRING claim
— that adding a section writes into the outline BUFFER and that the human's
existing Save carries it through `edit-document` — and the adversarial review of
PR #207 found four broken flows that every harness-stubbed test in this suite was
blind to for exactly that reason. So this module mounts `mountStagingWorkbench`
against the same minimal DOM instrument `test_doxbench_view.py` owns (imported,
never copied, so the two cannot drift), serves `/source` bytes through a stub
`fetch`, and drives the tab the way a human does: open it, look at what it says,
press the add button, then Save.

The pure half — what text lands, where, and under which heading — is asserted in
test_outline_model.py, without a DOM. Nothing is duplicated between the two.

What is pinned here:

* **3.2** the add lands in the outline buffer, dirties it, carries `Added-by:`
  provenance, and the Save that follows names `edit-document` on the wire. The
  Save path is the REAL one: `savePlanState` + `runSave` over a recording
  transport, wired exactly as app.js wires it, so the verb is read off the
  request the transport was handed rather than off a fixture.
* **3.3** a pre-template fragment renders its real sections, is not called
  broken, and is not rewritten by the act of opening the tab — the buffer is
  still clean afterwards.
* **3.4** with no gate capability the add controls are inert AND unbound: no
  listener, so there is no write path on the page to reach.
* **3.5** the buffer key space and the save order are untouched by this slice.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT
# The SAME DOM instrument the canvas suite drives, imported rather than copied.
from test_doxbench_view import _EDITOR_DOM_SHIM

NODE = shutil.which("node")
VIEWS = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
VENDOR = REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "vendor"

# A fragment mid-migration: it carries Claims / Conflicts / Exit and lacks the
# idea-notes and open-questions sections. The FENCED example is the point — a
# fence-blind index would report this topic as carrying two sections it does not.
PARTLY_MIGRATED = """# Staged: topic x

Status: staged
Summary: a topic mid-migration onto the outline template.

## Claims

- A settled fact this topic treats as fixed.

## Conflicts

- Contradicts nothing yet. — Added-by: brett · 2026-08-16

Copy this when migrating:

```markdown
## Idea notes (pre-document, non-documented)

## Open questions
```

## Exit

Every open question carries a disposition other than open.
"""

# Staged long before the template ratified: none of the required sections, and
# nothing about it is a fault. Opt-in migration means this is the corpus's
# NORMAL shape for now.
PRE_TEMPLATE = """# Staged: topic y

Status: staged
Summary: a topic staged before the outline template existed.

## Background

Some prose nobody has restructured.

## Why

<!-- xspec:candidate target=ideation-dashboard -->
Because of a reason.
<!-- /xspec:candidate -->
"""

_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';

globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');
globalThis.window = { location: { href: 'http://localhost/' } };

const { mountStagingWorkbench } = await import('./staging-workbench.js');
// The REAL Save composition, wired exactly as app.js wires it: the plan and the
// action choice are the shipped module's, and only the transport is ours.
const { runSave, savePlanState, saveBufferOrder, SAVE_DOCUMENT_ORDER_RULE } =
  await import('./doxbench-save.js');
const { BUFFER_KINDS, contentIdentity } = await import('./doxbench-state.js');

const FRAGMENTS = JSON.parse(process.argv[2]);

function snapshotFor(topic, files) {
  return {
    repository: 'fixture-repo',
    generation: { source_revision: '1'.repeat(40) },
    documents: files.map((p) => ({
      id: p, path: p, topics: ['alpha'],
      destinations: { staged_topics: [topic] } })),
    clusters: [], possibles: [],
    staged_topics: [{ staging_id: topic, files }],
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
async function quiesce(n = 40) { for (let i = 0; i < n; i += 1) await settle(); }

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

// The ONE /source read the outline pane makes is viewer.js's own, so the stub
// goes on the global `fetch` rather than into a seam this pane does not have.
function installFetch(bytes) {
  const asked = [];
  globalThis.fetch = async (url) => {
    asked.push(String(url));
    const path = String(url).replace(/^\/source\//, '');
    if (!Object.prototype.hasOwnProperty.call(bytes, path)) {
      return { ok: false, status: 404, headers: { get: () => null },
               text: async () => '' };
    }
    return { ok: true, status: 200, headers: { get: () => 'aligned' },
             text: async () => bytes[path] };
  };
  return asked;
}

// A HOLDABLE content-identity seam, so the hash-settling window is a state the
// test can stand still inside instead of a race it has to win. Off by default:
// the canvas's own `contentIdentity` is what every other case runs on.
function holdableHash() {
  const gate = { holding: false, waiting: [] };
  gate.hash = async (content) => {
    if (gate.holding) await new Promise((resolve) => gate.waiting.push(resolve));
    return contentIdentity(content);
  };
  gate.release = () => {
    gate.holding = false;
    const waiting = gate.waiting.splice(0);
    for (const resolve of waiting) resolve();
  };
  return gate;
}

async function mount({ topic, files, bytes, gate = true, waitForIndex = true,
                       hashGate = null }) {
  const container = document.createElement('div');
  const log = { saves: [], asked: installFetch(bytes) };
  const caps = gate
    ? { actions: { gate: true, session: true }, actor: 'brett' }
    : { actions: {}, actor: 'brett' };
  const transport = async (request) => {
    log.saves.push(request);
    return { ok: true, ref: 'draft/' + topic, revision: 'r2',
             content_hash: { algorithm: 'sha256', hex: 'e'.repeat(64) } };
  };
  const doxbench = {
    // The buffer is seeded from the same bytes the pane renders, which is what a
    // real console does -- the two readings differ only by unsaved work.
    loadSource: async (path) => ({
      content: Object.prototype.hasOwnProperty.call(bytes, path) ? bytes[path] : '',
      ref: 'main' }),
    storage: new FakeStorage(),
    hash: hashGate ? hashGate.hash : undefined,
    save: (request) => runSave(savePlanState(request), { transport }),
  };
  const workbench = mountStagingWorkbench(container, snapshotFor(topic, files), {
    caps,
    onOpenDoc: () => null,
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
  workbench.open('staged', topic);
  const byClass = (cls) => container.walk().filter(
    (n) => String(n.className).split(' ').includes(cls));
  const one = (cls) => byClass(cls)[0] || null;
  // The outline SELECTION tab -- the same click a human makes.
  const outlineTab = byClass('swb-tab').find(
    (b) => String(b.textContent).toLowerCase().includes('outline'));
  await fire(outlineTab, 'click');
  if (waitForIndex) {
    await until(() => one('swb-outlinestate') !== null, 'the outline index');
  }
  await quiesce(40);
  return { container, workbench, log, byClass, one };
}

function indexRows(ctx) {
  return ctx.byClass('swb-outlinerow').map((row) => ({
    title: String(row.children[0].textContent),
    chip: String(row.children[1].textContent),
  }));
}

// The OUTLINE buffer's own status sentence -- the first status region, which is
// the reserved outline key's.
function outlineStatus(ctx) {
  return String((ctx.byClass('doxbench-status')[0] || {}).textContent || '');
}

// The `## ` headings OUTSIDE code fences, implemented HERE rather than through
// outline-model.js: the fixture deliberately quotes the canonical skeleton inside
// a ```markdown fence, so a fence-blind reading of the buffer counts headings
// that are examples. An assertion that consulted the scanner under test could
// not have caught a fence bug in it.
function realHeadings(text) {
  const found = [];
  let fenced = false;
  for (const line of String(text).split('\n')) {
    if (line.trimStart().startsWith('```')) { fenced = !fenced; continue; }
    if (!fenced && line.startsWith('## ')) found.push(line.slice(3).trim());
  }
  return found;
}

// Task 3.5 is an INVARIANT: this slice is presentation and addressing only, so
// the buffer key space and the declared save order must be exactly what Phase B
// left. Read off the LIVE modules the composition below imports.
const out = {
  bufferKinds: BUFFER_KINDS,
  saveOrderRule: SAVE_DOCUMENT_ORDER_RULE,
  saveOrder: [...saveBufferOrder(['b.md', 'outline', 'a.md'])],
};

// =====================================================================
// 3.1/3.2: a partly migrated topic -- what the index says, and one add
// =====================================================================
{
  const outline = 'ideation/staging/topic-x/topic-x.md';
  const ctx = await mount({
    topic: 'topic-x', files: [outline],
    bytes: { [outline]: FRAGMENTS.partly } });
  out.partly = {
    state: String(ctx.one('swb-outlinestate').textContent),
    header: String(ctx.one('swb-abstractlabel').textContent),
    headerTitle: String(ctx.one('swb-abstractlabel').title || ''),
    rows: indexRows(ctx),
    gaps: ctx.byClass('swb-outlinegaplabel').map((n) => String(n.textContent)),
    addButtons: ctx.byClass('swb-outlineaddgap').map((b) => ({
      disabled: b.disabled === true,
      bound: ((b.listeners || {}).click || []).length,
      title: b.title,
    })),
    // NOTHING was rewritten by opening the tab: the buffer is clean.
    statusBeforeAdd: outlineStatus(ctx),
  };

  // Press the add for the FIRST missing required section.
  const add = ctx.byClass('swb-outlineaddgap')[0];
  await fire(add, 'click');
  await quiesce(80);
  out.partly.note = String(ctx.one('swb-outlinenote').textContent);
  const area = ctx.byClass('doxbench-textarea')[0];
  out.partly.bufferText = String(area.value);
  out.partly.bufferHeadings = realHeadings(area.value);
  out.partly.statusAfterAdd = outlineStatus(ctx);

  // …and the human's own Save, which is the only thing that writes.
  const saveBtn = ctx.one('doxbench-save');
  out.partly.saveReachable = saveBtn.disabled !== true;
  await fire(saveBtn, 'click');
  await quiesce(80);
  out.partly.saveRequests = ctx.log.saves.map((r) => ({
    kind: r.kind, action: r.action, document: r.document,
    carriesSection: String(r.content || '').includes(
      '## Idea notes (pre-document, non-documented)'),
  }));
  // The affordance itself asked for nothing: every /source read is the viewer's.
  out.partly.asked = ctx.log.asked;
}

// =====================================================================
// 3.2 (refusal): the section the buffer already holds
// =====================================================================
{
  const outline = 'ideation/staging/topic-z/topic-z.md';
  const ctx = await mount({
    topic: 'topic-z', files: [outline],
    bytes: { [outline]: FRAGMENTS.partly } });
  const add = ctx.byClass('swb-outlineaddgap')[0];
  await fire(add, 'click');
  await quiesce(80);
  const firstNote = String(ctx.one('swb-outlinenote').textContent);
  // Pressed a SECOND time: the stored fragment still lacks the section, so the
  // button is still offered -- but the buffer now has it.
  await fire(add, 'click');
  await quiesce(80);
  out.twice = {
    first: firstNote,
    second: String(ctx.one('swb-outlinenote').textContent),
    headings: realHeadings(ctx.byClass('doxbench-textarea')[0].value),
  };

  // …and the FREE-FORM add, whose target the human names. That target is the
  // patch's addressing key, so it is read at click time, not at render time.
  ctx.one('swb-outlinetitle').value = 'Prior art';
  ctx.one('swb-outlineafter').value = 'Conflicts';
  await fire(ctx.one('swb-outlineaddfree'), 'click');
  await quiesce(80);
  out.freeform = {
    note: String(ctx.one('swb-outlinenote').textContent),
    headings: realHeadings(ctx.byClass('doxbench-textarea')[0].value),
    text: String(ctx.byClass('doxbench-textarea')[0].value),
  };

  // Review finding F2, through the real control: a heading that merely RESEMBLES
  // a template one is addable and lands verbatim. Every one of these was refused
  // before, naming a section the human never asked for.
  out.resembling = [];
  for (const title of ['Exit criteria', 'Conflicts with promoted specs',
                       'Notes on conflicts']) {
    ctx.one('swb-outlinetitle').value = title;
    ctx.one('swb-outlineafter').value = '';
    await fire(ctx.one('swb-outlineaddfree'), 'click');
    await quiesce(80);
    out.resembling.push({
      title,
      note: String(ctx.one('swb-outlinenote').textContent),
      landed: realHeadings(ctx.byClass('doxbench-textarea')[0].value)
        .includes(title),
    });
  }
  out.resemblingText = String(ctx.byClass('doxbench-textarea')[0].value);
}

// =====================================================================
// F3: the seam's CODE is mapped; its text is never echoed
// =====================================================================
{
  // The settling window, held open. A keystroke leaves the outline buffer
  // `hash_pending` until its identity resolves; pressing add inside that window
  // is the reachable `unsettled` refusal, and before the fix the human was handed
  // the canvas's own sentence with no recovery in it.
  const outline = 'ideation/staging/topic-h/topic-h.md';
  const hashGate = holdableHash();
  const ctx = await mount({
    topic: 'topic-h', files: [outline],
    bytes: { [outline]: FRAGMENTS.partly }, hashGate });
  hashGate.holding = true;
  const area = ctx.byClass('doxbench-textarea')[0];
  const editorTab = ctx.byClass('doxbench-viewtab')[0];
  await fire(editorTab, 'click');
  await quiesce(10);
  area.value = FRAGMENTS.partly + '\nA keystroke.\n';
  fire(area, 'input');            // deliberately NOT awaited: the hash is held
  await quiesce(20);
  const add = ctx.byClass('swb-outlineaddgap')[0];
  await fire(add, 'click');
  await quiesce(20);
  out.unsettled = {
    note: String(ctx.one('swb-outlinenote').textContent),
    // nothing was written while the identity was in flight
    stillHasNoSection: !realHeadings(area.value).includes(
      'Idea notes (pre-document, non-documented)'),
  };
  // …and once it settles, the same press works. The refusal's advice is true.
  hashGate.release();
  await quiesce(60);
  await fire(add, 'click');
  await quiesce(80);
  out.unsettled.afterRelease = String(ctx.one('swb-outlinenote').textContent);
  out.unsettled.landedAfterRelease = realHeadings(area.value).includes(
    'Idea notes (pre-document, non-documented)');
}

// =====================================================================
// 3.3: the pre-template topic
// =====================================================================
{
  const outline = 'ideation/staging/topic-y/topic-y.md';
  const ctx = await mount({
    topic: 'topic-y', files: [outline],
    bytes: { [outline]: FRAGMENTS.preTemplate } });
  out.pre = {
    state: String(ctx.one('swb-outlinestate').textContent),
    rows: indexRows(ctx),
    status: outlineStatus(ctx),
    bufferText: String(ctx.byClass('doxbench-textarea')[0].value),
    saveRequests: ctx.log.saves.length,
    // the viewer's own rendering is still there, unchanged
    viewerBody: ctx.byClass('viewer-body').length,
  };
}

// =====================================================================
// 3.4: no gate capability
// =====================================================================
{
  const outline = 'ideation/staging/topic-x/topic-x.md';
  const ctx = await mount({
    topic: 'topic-x', files: [outline],
    bytes: { [outline]: FRAGMENTS.partly }, gate: false });
  const controls = ctx.byClass('swb-outlineadd').map((b) => ({
    disabled: b.disabled === true,
    bound: ((b.listeners || {}).click || []).length,
    title: b.title,
  }));
  out.gateOff = {
    indexRendered: ctx.byClass('swb-outlinerow').length,
    controls,
    inputDisabled: ctx.one('swb-outlinetitle').disabled === true,
    selectDisabled: ctx.one('swb-outlineafter').disabled === true,
    canvasMounted: ctx.byClass('doxbench-textarea').length,
  };
  // Fire every listener the page carries on those controls: nothing happens,
  // because nothing is bound.
  for (const btn of ctx.byClass('swb-outlineadd')) await fire(btn, 'click');
  await quiesce(40);
  out.gateOff.saveRequests = ctx.log.saves.length;
  out.gateOff.note = String((ctx.one('swb-outlinenote') || {}).textContent || '');
}

// =====================================================================
// 3.3 (degraded load): the fragment's bytes never arrive
// =====================================================================
{
  const outline = 'ideation/staging/topic-w/topic-w.md';
  const ctx = await mount({
    topic: 'topic-w', files: [outline], bytes: {}, waitForIndex: false });
  await quiesce(80);
  out.degraded = {
    index: ctx.byClass('swb-outlineindex').length,
    stateLines: ctx.byClass('swb-outlinestate').length,
    controls: ctx.byClass('swb-outlineadd').length,
    viewerBody: String((ctx.one('viewer-body') || {}).textContent || ''),
    saveRequests: ctx.log.saves.length,
  };
}

// =====================================================================
// H1: a throwing `onText` must not take the viewer down with it
// =====================================================================
{
  // Direct at the seam, because no production caller can be made to throw on
  // demand. Callers do NOT await renderViewer, so an escaping throw here is a
  // silent unhandled rejection AFTER the document has already rendered.
  const { renderViewer } = await import('./viewer.js');
  globalThis.fetch = async () => ({
    ok: true, status: 200, headers: { get: () => 'aligned' },
    text: async () => '# A document\n\nWith prose.\n' });
  const root = document.createElement('div');
  let rejected = null;
  let called = 0;
  await renderViewer(root, {
    path: 'ideation/staging/topic-v/topic-v.md',
    sourceBase: '/source/',
    onText: (text) => { called += 1; void text; throw new Error('derivation bug'); },
  }).then(() => null, (error) => { rejected = String(error && error.message); });
  out.throwingOnText = {
    called,
    rejected,
    // the document itself still rendered -- the throw was the LAST statement
    bodyRendered: root.walk().some(
      (n) => String(n.className).split(' ').includes('viewer-body')
        && String(n.innerHTML).includes('A document')),
  };

  // …and the ASYNC shape (PR #208 review). An async `onText` never throws: it
  // hands back a rejected promise, which a bare try/catch does not see at all.
  // Installing the process handler is what makes the escape OBSERVABLE instead
  // of fatal -- without one, node would print the rejection and take the harness
  // with it, which is exactly the failure mode being closed.
  const escaped = [];
  process.on('unhandledRejection', (reason) => {
    escaped.push(String((reason && reason.message) || reason));
  });
  const asyncRoot = document.createElement('div');
  let asyncRejected = null;
  let asyncCalled = 0;
  await renderViewer(asyncRoot, {
    path: 'ideation/staging/topic-u/topic-u.md',
    sourceBase: '/source/',
    onText: async (text) => {
      asyncCalled += 1;
      void text;
      throw new Error('async derivation bug');
    },
  }).then(() => null, (error) => { asyncRejected = String(error && error.message); });
  // Node reports an unhandled rejection a tick AFTER the microtask queue drains,
  // so the escape has to be given room to surface before it is measured.
  for (let i = 0; i < 8; i += 1) await new Promise((r) => setTimeout(r, 0));
  out.asyncThrowingOnText = {
    called: asyncCalled,
    rejected: asyncRejected,
    escaped: [...escaped],
    bodyRendered: asyncRoot.walk().some(
      (n) => String(n.className).split(' ').includes('viewer-body')
        && String(n.innerHTML).includes('A document')),
  };
}

console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def tab(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the outline-tab composition probe")
    root = tmp_path_factory.mktemp("outline-tab")
    views = root / "views"
    shutil.copytree(VIEWS, views)
    shutil.copytree(VENDOR, root / "vendor")
    (root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (root / "vendor" / "package.json").write_text('{"type": "commonjs"}',
                                                  encoding="utf-8")
    harness = views / "outline-tab-harness.mjs"
    harness.write_text(_HARNESS, encoding="utf-8")
    fragments = json.dumps({"partly": PARTLY_MIGRATED,
                            "preTemplate": PRE_TEMPLATE})
    done = subprocess.run([NODE, str(harness), fragments],
                          capture_output=True, text=True, timeout=180)
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


# ---------------------------------------------------------------------------
# 3.1 wired: the index says what the fragment says, and nothing more
# ---------------------------------------------------------------------------


def test_the_index_reports_the_fragments_own_sections(tab):
    rows = tab["partly"]["rows"]
    assert [r["title"] for r in rows] == ["Claims", "Conflicts", "Exit"]


def test_a_fenced_example_is_never_reported_as_an_adopted_section(tab):
    """The fixture pastes the canonical skeleton's headings inside a ```markdown
    fence. A fence-blind index would report this topic as carrying idea notes and
    open questions — and would then withhold the very add buttons that migrate
    it."""
    titles = [r["title"] for r in tab["partly"]["rows"]]
    assert "Idea notes (pre-document, non-documented)" not in titles
    assert "Open questions" not in titles
    assert set(tab["partly"]["gaps"]) == {
        "no pre-document idea notes section", "no open questions section"}


def test_the_state_line_names_the_migration_stage_not_a_fault(tab):
    assert "partly templated" in tab["partly"]["state"]


# ---------------------------------------------------------------------------
# 3.2: the add writes into the buffer, with provenance, and Save carries it
# ---------------------------------------------------------------------------


def test_the_add_control_is_live_where_editing_is(tab):
    controls = tab["partly"]["addButtons"]
    assert len(controls) == 2
    for control in controls:
        assert control["disabled"] is False
        assert control["bound"] == 1
        assert "edit-document" in control["title"]


def test_the_added_section_lands_in_the_outline_buffer_with_provenance(tab):
    text = tab["partly"]["bufferText"]
    assert "## Idea notes (pre-document, non-documented)" in text
    # The provenance names the gate's own actor and a REAL ISO date. Asserted as a
    # pattern because the prefix-only form this replaces ("· 20") passed on a
    # literal "20" and so proved nothing about the date at all.
    assert re.search(r"Added-by: brett · \d{4}-\d{2}-\d{2}", text), text
    # …in its canonical place, between Claims and Conflicts
    assert tab["partly"]["bufferHeadings"] == [
        "Claims", "Idea notes (pre-document, non-documented)", "Conflicts", "Exit"]


def test_the_add_dirties_the_buffer_exactly_as_typing_does(tab):
    """The insert goes through the canvas's own `applyProposal` -> `edit()` path,
    so the dirty state, the hashing and the Save plan are the ones a keystroke
    produces. A second insertion mechanism would have had to re-earn all three."""
    assert tab["partly"]["statusBeforeAdd"] == "Outline: no unsaved changes"
    assert tab["partly"]["statusAfterAdd"] == "Outline: unsaved changes"


def test_the_note_says_what_landed_and_what_did_not(tab):
    note = tab["partly"]["note"]
    assert "Idea notes (pre-document, non-documented)" in note
    assert "outline buffer" in note
    assert "unsaved" in note
    # the verb is named for the human, and it is the session content verb
    assert "edit-document" in note
    assert "edit-apply" not in note


def test_the_save_that_follows_names_edit_document(tab):
    """Amendment 1's whole content, proven on the wire rather than asserted. The
    plan is the shipped `savePlanState` + `runSave`; only the transport is the
    test's, so the action is the one the real Save path chose."""
    assert tab["partly"]["saveReachable"] is True
    requests = tab["partly"]["saveRequests"]
    assert len(requests) == 1, requests
    assert requests[0]["kind"] == "outline"
    assert requests[0]["action"] == "edit-document"
    assert requests[0]["document"] == "ideation/staging/topic-x/topic-x.md"
    assert requests[0]["carriesSection"] is True


def test_the_affordance_opens_no_route_of_its_own(tab):
    """Every `/source` read on the page is the viewer's ONE fetch for the
    fragment; the add performs no request at all."""
    assert tab["partly"]["asked"] == ["/source/ideation/staging/topic-x/topic-x.md"]


def test_a_section_the_buffer_already_holds_is_refused_not_duplicated(tab):
    """The button is offered from what the STORED fragment lacks, so it stays
    offered after an unsaved add — and pressing it again must refuse rather than
    write a second copy."""
    assert "added" in tab["twice"]["first"]
    assert "already carries" in tab["twice"]["second"]
    headings = tab["twice"]["headings"]
    assert headings.count("Idea notes (pre-document, non-documented)") == 1


def test_the_free_form_add_is_scoped_by_the_target_the_human_names(tab):
    """A heading with no canonical place is anchored explicitly, and the anchor is
    read at CLICK time — a control that closed over its values at render time
    would always patch against the empty form."""
    free = tab["freeform"]
    assert 'after "Conflicts"' in free["note"]
    assert free["headings"] == [
        "Claims", "Idea notes (pre-document, non-documented)", "Conflicts",
        "Prior art", "Exit"]
    # a section beyond the required set carries the section-level provenance line
    assert re.search(r"## Prior art\n\nAdded-by: brett · \d{4}-\d{2}-\d{2}",
                     free["text"]), free["text"]


def test_a_heading_that_merely_resembles_a_template_one_is_addable(tab):
    """Review finding F2, through the real control. Each of these was refused on a
    conforming fragment — with a message naming a section the human never asked
    for — and the near-misses were silently rewritten into the required heading."""
    landed = {row["title"]: row for row in tab["resembling"]}
    assert set(landed) == {"Exit criteria", "Conflicts with promoted specs",
                           "Notes on conflicts"}
    for title, row in landed.items():
        assert row["landed"] is True, row["note"]
        assert "already carries" not in row["note"], row["note"]
        assert '"' + title + '"' in row["note"], row["note"]
    # …and the required Conflicts section is still there exactly once, with its own
    # seed intact — nothing was canonicalized on top of it
    text = tab["resemblingText"]
    assert text.count("\n## Conflicts\n") == 1
    assert "## Notes on conflicts\n\nAdded-by: brett" in text
    assert "<conflict text> — Added-by" not in text.split(
        "## Notes on conflicts", 1)[1]


# ---------------------------------------------------------------------------
# F3: the seam's code is mapped to this tab's sentences; its text is not echoed
# ---------------------------------------------------------------------------


def test_pressing_add_inside_the_settling_window_gets_recovery_advice(tab):
    """W-10's lesson, on this surface. The window is genuinely reachable — a
    keystroke leaves the buffer `hash_pending` until its identity resolves — and
    the human used to be handed the canvas's own sentence, which states the
    situation and no way out of it."""
    unsettled = tab["unsettled"]
    assert unsettled["note"] == (
        "the outline buffer's identity is still settling — press add again in a "
        "moment")
    # the canvas's own text, and the chat's noun, are both absent
    assert "proposal" not in unsettled["note"]
    assert "still settling" in unsettled["note"] and "moment" in unsettled["note"]
    # nothing was written while the identity was in flight
    assert unsettled["stillHasNoSection"] is True


def test_the_settling_refusal_tells_the_truth_about_its_own_recovery(tab):
    """An advice sentence that does not work is worse than none: the same press,
    once the identity settles, lands."""
    unsettled = tab["unsettled"]
    assert "added" in unsettled["afterRelease"]
    assert "Idea notes (pre-document, non-documented)" in unsettled["afterRelease"]
    assert unsettled["landedAfterRelease"] is True


def test_the_refusal_mapping_is_a_code_whitelist_with_no_text_echo():
    """Both other consumers of `applyProposal` forbid echoing the seam's text —
    doxbench-chat.js calls its mapping a WHITELIST and drops the text unread, and
    the canvas states its sentences are "never echoed". This tab now does the same,
    and the pin is on the shape rather than on any one sentence: the refusal branch
    reads `code` and nothing else."""
    view = (VIEWS / "staging-workbench.js").read_text(encoding="utf-8")
    assert "function addSectionRefusal(outcome)" in view
    mapper = view.split("function addSectionRefusal(outcome) {", 1)[1].split(
        "\n}\n", 1)[0]
    # every branch keys off the CODE, and every answer is one of the four fixed
    # sentences — no interpolation, no seam text
    assert 'code === "unsettled"' in mapper
    assert 'code === "stale"' in mapper
    assert 'code === "unavailable"' in mapper
    assert "outcome.error" not in mapper
    assert mapper.count("return ADD_SECTION_") == 4
    # …and the add path itself never reaches for the seam's text
    body = view.split("async function runAddSection(", 1)[1].split(
        "\n}\n", 1)[0]
    assert "note.textContent = addSectionRefusal(outcome);" in body
    assert ".error" not in body, "the seam's own text must not reach the note"
    # the pre-fix fallback sentence is gone
    assert "the insertion was refused and stated no reason" not in view


def test_every_refusal_the_seam_makes_for_itself_carries_a_code():
    """A refusal with no code falls through to the generic sentence, so the seam's
    own two must be coded or the accurate message is lost."""
    view = (VIEWS / "staging-workbench.js").read_text(encoding="utf-8")
    seam = view.split("function outlineSectionSeam() {", 1)[1].split(
        "\n  }\n", 1)[0]
    refusals = re.findall(r"return \{ ok: false,[^}]*\}", seam, re.DOTALL)
    assert refusals, seam
    for refusal in refusals:
        assert "code:" in refusal, refusal


# ---------------------------------------------------------------------------
# H2: the index says which bytes it is describing
# ---------------------------------------------------------------------------


def test_the_index_header_says_it_describes_the_stored_bytes(tab):
    """Without it the gap row above ("no pre-document idea notes section") reads as
    contradicting the refusal below it ("this outline already carries…") — two
    honest answers about two different texts, looking like one surface arguing with
    itself. The two-renderings split itself is deliberate and stays."""
    assert tab["partly"]["header"] == "outline template — as stored"
    title = tab["partly"]["headerTitle"]
    assert "SAVED" in title and "unsaved" in title


# ---------------------------------------------------------------------------
# 3.3: a pre-template fragment degrades and is never rewritten
# ---------------------------------------------------------------------------


def test_a_pre_template_fragment_renders_what_it_has(tab):
    assert [r["title"] for r in tab["pre"]["rows"]] == ["Background", "Why"]
    # its `xspec:`-fenced section is classified from the marker, not sniffed
    assert [r["chip"] for r in tab["pre"]["rows"]] == ["added", "proposal element"]
    assert tab["pre"]["viewerBody"] == 1


def test_a_pre_template_fragment_is_not_reported_as_broken(tab):
    state = tab["pre"]["state"].lower()
    assert "staged before the outline template" in state
    assert "opt-in" in state
    for alarm in ("error", "invalid", "broken", "fail", "must be fixed"):
        assert alarm not in state, state


def test_opening_the_tab_rewrites_nothing(tab):
    """Conformance is earned when a human next works the topic, never by the act
    of viewing it. So the buffer is CLEAN and the bytes are the stored bytes."""
    assert tab["pre"]["status"] == "Outline: no unsaved changes"
    assert tab["pre"]["bufferText"] == PRE_TEMPLATE
    assert tab["pre"]["saveRequests"] == 0


# ---------------------------------------------------------------------------
# 3.4: gate off
# ---------------------------------------------------------------------------


def test_with_no_gate_capability_no_add_control_is_live(tab):
    gate_off = tab["gateOff"]
    assert gate_off["canvasMounted"] == 0      # no editing canvas on this plane
    assert gate_off["controls"], "the affordance must still say what it would be"
    for control in gate_off["controls"]:
        assert control["disabled"] is True
        # …and, the load-bearing half: NO HANDLER IS BOUND, so there is no write
        # path on the page even for something that re-enabled the node.
        assert control["bound"] == 0
        assert "editing capability" in control["title"]
    assert gate_off["inputDisabled"] is True
    assert gate_off["selectDisabled"] is True


def test_with_no_gate_capability_activation_writes_nothing(tab):
    assert tab["gateOff"]["saveRequests"] == 0
    assert tab["gateOff"]["note"] == ""


def test_the_index_still_reads_on_a_gate_off_plane(tab):
    """Reading a topic's structure needs no authority, and withholding it would
    make the hosted image less useful for no governance gain."""
    assert tab["gateOff"]["indexRendered"] == 3


# ---------------------------------------------------------------------------
# 3.5: the buffer contract is untouched
# ---------------------------------------------------------------------------


def test_the_buffer_key_space_and_save_order_are_untouched(tab):
    """A diff in either means this change has overreached into
    `doxbench-editing-model` Phase B's territory. Asserted from the LIVE module
    the composition imported, not from a re-read of the file."""
    assert tab["bufferKinds"] == ["outline", "document"]
    assert tab["saveOrderRule"] == \
        "ascending lexicographic by buffer key (UTF-16 code unit)"
    assert tab["saveOrder"] == ["outline", "a.md", "b.md"]
    save_js = (VIEWS / "doxbench-save.js").read_text(encoding="utf-8")
    assert 'export const SAVE_ACTION_EDIT = "edit-document";' in save_js
    assert 'export const OUTLINE_BUFFER_KEY = "outline";' in save_js


def test_this_slice_added_no_write_verb_and_no_transport():
    """Task 3.2's ruling in one grep: the outline tab introduces no second write
    verb and no route. `edit-document` appears only as the verb the existing Save
    path already uses, and `edit-apply` — the gate console's main-resident redline
    verb Amendment 1 rejected — is never reached from here."""
    view = (VIEWS / "staging-workbench.js").read_text(encoding="utf-8")
    model = (VIEWS / "outline-model.js").read_text(encoding="utf-8")
    for source in (view, model):
        assert "fetch(" not in source
        assert "/actions/" not in source
        assert "edit-apply" not in source
    # the pure model stays standalone-importable for the node harness (the same
    # rule staging-workbench-model.js keeps): it imports nothing at all
    assert not re.findall(r"^\s*import\s", model, re.MULTILINE)


# ---------------------------------------------------------------------------
# 3.3 (degraded load): bytes that never arrive
# ---------------------------------------------------------------------------


def test_a_throwing_read_back_seam_does_not_take_the_viewer_down(tab):
    """H1. `renderViewer` is never awaited by its callers, so a throw inside a
    caller's derivation becomes a silent unhandled rejection — and it happens
    AFTER the document has rendered, so the honest outcome is a missing index, not
    a broken page and not a message about someone else's bug."""
    thrown = tab["throwingOnText"]
    assert thrown["called"] == 1, "the seam must still be invoked on a good load"
    assert thrown["rejected"] is None, thrown["rejected"]
    assert thrown["bodyRendered"] is True


def test_an_async_read_back_seam_that_rejects_is_contained_too(tab):
    """PR #208 review (Copilot). A try/catch catches a THROW; an async `onText`
    never throws — it returns a rejected promise, which sails straight past it and
    becomes the very unhandled rejection the containment comment claims to
    prevent. Our one caller is synchronous today, so this half was latent; the
    claim still has to be true for both shapes, because that comment is what the
    next caller reads before writing an async one."""
    thrown = tab["asyncThrowingOnText"]
    assert thrown["called"] == 1, "the seam must still be invoked on a good load"
    # the viewer's own promise resolves — the caller's failure is not the read's
    assert thrown["rejected"] is None, thrown["rejected"]
    # …and nothing escaped to the process as an unhandled rejection
    assert "async derivation bug" not in thrown["escaped"], thrown["escaped"]
    assert thrown["escaped"] == [], thrown["escaped"]
    assert thrown["bodyRendered"] is True


def test_a_fragment_that_fails_to_load_gets_no_fabricated_index(tab):
    """The index is built from the bytes the viewer hands back and from nothing
    else, so a 404 leaves the host empty and the viewer's own message standing
    alone. An index derived from an absent load would describe a file nobody
    read."""
    degraded = tab["degraded"]
    assert degraded["index"] == 1            # the host exists…
    assert degraded["stateLines"] == 0       # …and says nothing
    assert degraded["controls"] == 0
    assert "could not load" in degraded["viewerBody"]
    assert degraded["saveRequests"] == 0
