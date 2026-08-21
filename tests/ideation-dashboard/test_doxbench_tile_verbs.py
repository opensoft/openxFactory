"""add-doxbench-editing-phase-b: the LOADED SET's two human surfaces.

Two of Brett's 2026-08-18 rulings, and the surfaces that carry them:

Q1, the chat rail's header stops being a label and becomes a SELECTOR --
"make this a dropdown box that lists the files that have been loaded by
clicking the edit button on the wheel. the selected one is the file we are
working on. if not fit in one line, then use hover to expand to see full
filename."

Q3, the docs tile carries THREE verbs -- "add a load button. read will still
pull up an imersive reader experience of the doc in a large window. the new
<Edit> button will then load this into the chat context. Once loaded and
editable by chat, color this tile so we know is must be saved. also add a save
button here. So we have read, edit, save and save only active if there are
changes. the save acts same as the save button that is in the preview panel."

Both are driven against a minimal DOM, the same instrument
`test_wheel_verbs_dom.py` and `test_staging_workbench.py` already use, so the
behaviour is pinned without a browser.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
VIEWS = WEB / "views"
STYLES = WEB / "styles.css"

_DOM_SHIM = r"""
class Node {
  constructor(tag) {
    this.tagName = String(tag).toUpperCase();
    this.children = []; this.attributes = {}; this.listeners = {};
    this.className = ''; this._text = ''; this.disabled = false;
    this.value = ''; this.hidden = false; this.type = '';
    this.style = {}; this.tabIndex = 0;
    this._classes = new Set();
    this.classList = {
      add: (c) => { this._classes.add(c); this._sync(); },
      remove: (c) => { this._classes.delete(c); this._sync(); },
      toggle: (c, on) => {
        if (on === undefined) {
          if (this._classes.has(c)) this._classes.delete(c);
          else this._classes.add(c);
        } else if (on) this._classes.add(c);
        else this._classes.delete(c);
        this._sync();
      },
      contains: (c) => this._classes.has(c),
    };
  }
  _sync() {
    const base = String(this.className).split(' ').filter(
      (c) => c && !this._tracked.has(c));
    this.className = base.concat([...this._classes]).join(' ').trim();
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
  remove() {
    if (!this.parent) return;
    const at = this.parent.children.indexOf(this);
    if (at >= 0) this.parent.children.splice(at, 1);
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) {
    return Object.prototype.hasOwnProperty.call(this.attributes, name)
      ? this.attributes[name] : null;
  }
  removeAttribute(name) { delete this.attributes[name]; }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  focus() {}
  querySelector(selector) {
    const cls = selector.replace(/^\./, '');
    return this.walk().slice(1).find(
      (n) => String(n.className).split(' ').includes(cls)) || null;
  }
  walk() {
    return this.children.reduce((all, c) => all.concat(c.walk()), [this]);
  }
}
// `_tracked` is the set of classes the classList shim owns, so a `_sync` cannot
// drop a class that was set through `className` at construction.
Node.prototype._tracked = new Set([
  'wheeloffwindow', 'wheelfocused', 'wheelexpanded',
  'swb-docloaded', 'swb-docneedssave', 'swb-docwheel',
]);
const doc = { createElement: (tag) => new Node(tag) };
globalThis.document = doc;
const byClass = (root, cls) => root.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));
// The real click handler reads `ev.target` (a click on the expanded tile's own
// action belongs to the action, not the tile), so the shim supplies it -- the
// node the event is fired on, exactly as a browser would.
const fire = async (node, type, ev = {}) => {
  for (const fn of node.listeners[type] || []) {
    await fn({ target: node, stopPropagation() {}, preventDefault() {}, ...ev });
  }
};
"""

# ---------------------------------------------------------------------------
# Q3: the docs tile's three verbs
# ---------------------------------------------------------------------------

_TILE_HARNESS = _DOM_SHIM + r"""
import { renderDocWheel, DOC_TILE_VERBS } from "./doc-wheel.js";

const A = 'ideation/staging/t/alpha.md';
const B = 'ideation/staging/t/beta.md';
const C = 'docs/inherited.md';

// The entry shape `docWheelEntries` produces, as the wheel reads it.
const entry = (path, over = {}) => ({
  path, resolved: true, label: path.split('/').at(-1),
  section: 'topic folder documents', inherited: false,
  stage: 'staged', kind: 'note', score: null,
  row: { path, doc: {} }, ...over });

function entriesFor() {
  return [entry(A), entry(B), entry(C, { owned: false, inherited: true })];
}

// The LIVE buffer state each case presents: A is loaded and dirty, B is loaded
// and clean, C is loaded as read-only CONTEXT (`owned: false`).
const LIVE = {
  [A]: { loaded: true, dirty: true, owned: true },
  [B]: { loaded: true, dirty: false, owned: true },
  [C]: { loaded: true, dirty: true, owned: false },
};

// THE LOCKED GESTURE, driven as a human drives it: a click on a tile that is
// not on the line focuses it, and a click once it IS on the line expands it. The
// centred tile therefore needs ONE click and any other needs two, so the helper
// clicks until the action row exists rather than assuming a count.
async function expand(tiles, i) {
  for (let attempt = 0; attempt < 3; attempt += 1) {
    if (tiles[i].querySelector('.wheelactions')) return tiles[i];
    await fire(tiles[i], 'click');
  }
  if (!tiles[i].querySelector('.wheelactions')) {
    throw new Error('tile ' + i + ' never expanded');
  }
  return tiles[i];
}

function mount(overrides = {}) {
  const host = new Node('div');
  host.clientHeight = 400;
  const calls = { read: [], load: [], save: [] };
  const wheel = renderDocWheel(host, entriesFor(), {
    onRead: (row) => calls.read.push(row.path),
    onLoad: (row) => calls.load.push(row.path),
    onSave: (row) => calls.save.push(row.path),
    bufferStateFor: (path) => LIVE[path] || null,
    ...overrides,
  });
  return { host, wheel, calls };
}

const out = { verbs: DOC_TILE_VERBS };

// ---- the expanded tile's action row carries exactly the three verbs ----
{
  const { host, calls } = mount();
  const tiles = byClass(host, 'wheeltile');
  await expand(tiles, 0);
  const row = tiles[0].querySelector('.wheelactions');
  out.actionRow = row === null ? null : row.children.map((b) => ({
    className: b.className, label: b.textContent,
    disabled: b.disabled === true, title: b.title || '',
  }));
  const read = tiles[0].querySelector('.swb-docread');
  await fire(read, 'click');
  const save = tiles[0].querySelector('.swb-docsave');
  await fire(save, 'click');
  out.dirtyTileSaved = calls.save.slice();
  out.readInvoked = calls.read.slice();
}

// ---- a CLEAN loaded document's Save is visibly inert ----
{
  const { host, calls } = mount();
  const tiles = byClass(host, 'wheeltile');
  await expand(tiles, 1);
  const save = tiles[1].querySelector('.swb-docsave');
  out.cleanSave = { disabled: save.disabled === true, title: save.title };
  await fire(save, 'click');
  out.cleanTileSaved = calls.save.slice();
}

// ---- a CONTEXT-ONLY document loads, but offers NO reachable Save ----
{
  const { host, calls } = mount();
  const tiles = byClass(host, 'wheeltile');
  await expand(tiles, 2);
  const save = tiles[2].querySelector('.swb-docsave');
  const load = tiles[2].querySelector('.swb-docload');
  out.contextOnly = {
    saveDisabled: save.disabled === true, saveTitle: save.title,
    loadDisabled: load.disabled === true,
  };
  await fire(load, 'click');
  out.contextOnlyLoaded = calls.load.slice();
  out.contextOnlyMarking = {
    loaded: tiles[2].classList.contains('swb-docloaded'),
    needsSave: tiles[2].classList.contains('swb-docneedssave'),
    stated: tiles[2].getAttribute('data-doxbench-buffer'),
  };
}

// ---- the MARKING, across the whole reel and off LIVE state only ----
{
  const { host } = mount();
  const tiles = byClass(host, 'wheeltile');
  out.marking = tiles.map((tile) => ({
    loaded: tile.classList.contains('swb-docloaded'),
    needsSave: tile.classList.contains('swb-docneedssave'),
    stated: tile.getAttribute('data-doxbench-buffer'),
  }));
}

// ---- with NO buffer state at all, nothing is marked ----
{
  const { host } = mount({ bufferStateFor: () => null });
  const tiles = byClass(host, 'wheeltile');
  out.unmarked = tiles.map((tile) => ({
    loaded: tile.classList.contains('swb-docloaded'),
    needsSave: tile.classList.contains('swb-docneedssave'),
    stated: tile.getAttribute('data-doxbench-buffer'),
  }));
}

// ---- where EDITING is unreachable: read stays, load and save STATE it ----
{
  const { host, calls } = mount({ onLoad: null, onSave: null });
  const tiles = byClass(host, 'wheeltile');
  await expand(tiles, 0);
  const read = tiles[0].querySelector('.swb-docread');
  const load = tiles[0].querySelector('.swb-docload');
  const save = tiles[0].querySelector('.swb-docsave');
  await fire(load, 'click');
  await fire(save, 'click');
  out.editingUnreachable = {
    readReachable: read.disabled !== true,
    loadDisabled: load.disabled === true, loadTitle: load.title,
    saveDisabled: save.disabled === true, saveTitle: save.title,
    nothingHappened: calls.load.length === 0 && calls.save.length === 0,
  };
}

// ---- refreshBufferState re-derives the marking from the LIVE state ----
{
  const { host, wheel } = mount();
  const tiles = byClass(host, 'wheeltile');
  const before = tiles[1].classList.contains('swb-docneedssave');
  LIVE[B] = { loaded: true, dirty: true, owned: true };
  wheel.refreshBufferState();
  out.refresh = { before, after: tiles[1].classList.contains('swb-docneedssave') };
  LIVE[B] = { loaded: true, dirty: false, owned: true };
}

console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def tile_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench tile-verb probe")
    root = tmp_path_factory.mktemp("doxbench-tile-verbs")
    for name in ("doc-wheel.js", "wheel-model.js", "helpers.js"):
        shutil.copy(VIEWS / name, root / name)
    (root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    harness = root / "tile-harness.mjs"
    harness.write_text(_TILE_HARNESS, encoding="utf-8")
    done = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


def test_the_contract_names_the_three_verbs(tile_results):
    """Design D8: the CONTRACT names are read / load-for-editing / save, and
    `read` replaces Phase A's `open` -- a naming debt Phase A opened on purpose
    so this verb could exist without a third claimant to the word "edit"."""
    assert tile_results["verbs"] == ["read", "load-for-editing", "save"]


def test_the_expanded_tile_offers_read_load_and_save(tile_results):
    """The delta's `A tile is expanded` scenario."""
    row = tile_results["actionRow"]
    assert row is not None, "the expanded tile mounted no action row"
    assert [b["label"] for b in row] == ["read", "loaded", "save"]
    classes = [b["className"] for b in row]
    assert "swb-docread" in classes[0]
    assert "swb-docload" in classes[1]
    assert "swb-docsave" in classes[2]
    # Read keeps its Phase A class as well, so the CSS and every existing pin
    # that names the reader still match the control that IS the reader.
    assert "swb-docopen" in classes[0]


def test_read_is_unchanged_and_a_dirty_tiles_save_reaches_the_pipeline(
        tile_results):
    assert tile_results["readInvoked"] == ["ideation/staging/t/alpha.md"]
    assert tile_results["dirtyTileSaved"] == ["ideation/staging/t/alpha.md"]


def test_save_is_reachable_only_while_that_documents_buffer_is_dirty(
        tile_results):
    """"save only active if there are changes" -- the control's own state answers
    "does this need saving" without a sentence of standing text, and a click on
    the inert control reaches nothing."""
    clean = tile_results["cleanSave"]
    assert clean["disabled"] is True
    assert "no unsaved changes" in clean["title"]
    assert tile_results["cleanTileSaved"] == []


def test_a_context_only_document_loads_but_offers_no_reachable_save(
        tile_results):
    """The delta's `A context-only document is loaded` scenario and design D2:
    loadable for grounding and conversation, NO reachable Save, and NOT marked as
    needing one -- marking a document "must be saved" when the tile may not save
    it would be a false statement about the surface's own authority."""
    context = tile_results["contextOnly"]
    assert context["loadDisabled"] is False
    assert context["saveDisabled"] is True
    assert "read-only context" in context["saveTitle"]
    assert tile_results["contextOnlyLoaded"] == ["docs/inherited.md"]
    marking = tile_results["contextOnlyMarking"]
    assert marking["loaded"] is True
    assert marking["needsSave"] is False, (
        "a context-only tile must never be marked as needing a save")
    assert marking["stated"] == "loaded"


def test_a_loaded_and_dirty_tile_is_marked_across_the_whole_reel(tile_results):
    """The delta's `A loaded document's tile is marked` scenario. Both states
    Brett named are distinguishable, and the marking is announced as well as
    coloured, because colour alone is not an accessible state."""
    marking = tile_results["marking"]
    assert marking[0] == {"loaded": True, "needsSave": True,
                          "stated": "loaded-dirty"}
    assert marking[1] == {"loaded": True, "needsSave": False, "stated": "loaded"}


def test_the_marking_comes_from_live_state_and_nothing_else(tile_results):
    """Design D9: driven from live session-local buffer state, never persisted.
    With no live state there is nothing to mark -- which is exactly the posture a
    regenerated snapshot's own generator would produce, because it cannot observe
    a browser."""
    for tile in tile_results["unmarked"]:
        assert tile == {"loaded": False, "needsSave": False, "stated": None}
    # …and a buffer that becomes dirty is marked on the next refresh.
    assert tile_results["refresh"] == {"before": False, "after": True}


def test_where_editing_is_unreachable_load_and_save_state_it(tile_results):
    """The delta's `Editing is unavailable` scenario: load and save are
    unreachable and STATE the absence rather than failing on activation, and read
    remains available because it needs no gate capability."""
    posture = tile_results["editingUnreachable"]
    assert posture["readReachable"] is True
    assert posture["loadDisabled"] is True
    assert posture["saveDisabled"] is True
    assert "editing capability" in posture["loadTitle"]
    assert "editing capability" in posture["saveTitle"]
    assert posture["nothingHappened"] is True


# ---------------------------------------------------------------------------
# Q1: the chat rail's loaded-document selector
# ---------------------------------------------------------------------------

_SELECTOR_HARNESS = _DOM_SHIM + r"""
import {
  distinguishingLabels, loadedSelectorModel, LOADED_SELECTOR_EMPTY_NOTE,
  mountDoxBenchChatRail,
} from "./doxbench-chat.js";

const out = { emptyNote: LOADED_SELECTOR_EMPTY_NOTE };

const bufferOf = (kind, path, over = {}) => ({
  kind, path, owned: true, dirty: false,
  base_ref: 'main', base_revision: 'r1',
  base_hash: { algorithm: 'sha256', hex: 'c'.repeat(64) },
  current_hash: { algorithm: 'sha256', hex: 'd'.repeat(64) },
  hash_pending: false, content: '# ' + kind, ...over });

const ALPHA = 'ideation/staging/t/alpha.md';
const NESTED = 'ideation/staging/t/nested/alpha.md';
const ZULU = 'ideation/staging/t/zulu.md';
const CONTEXT = 'docs/inherited.md';

const FIVE = {
  active_buffer: NESTED,
  buffers: {
    outline: bufferOf('outline', 'ideation/staging/t/t.md'),
    [ZULU]: bufferOf('document', ZULU),
    [ALPHA]: bufferOf('document', ALPHA, { dirty: true }),
    [NESTED]: bufferOf('document', NESTED),
    [CONTEXT]: bufferOf('document', CONTEXT, { owned: false }),
    'ideation/staging/t/delta.md': bufferOf(
      'document', 'ideation/staging/t/delta.md'),
  },
};

out.labels = Object.fromEntries(distinguishingLabels([ALPHA, NESTED, ZULU]));
out.five = loadedSelectorModel(FIVE);
out.outlineSelected = loadedSelectorModel({ ...FIVE, active_buffer: 'outline' })
  .entries.map((e) => [e.key, e.selected]);
out.empty = loadedSelectorModel({
  active_buffer: 'outline',
  buffers: { outline: bufferOf('outline', 'ideation/staging/t/t.md') } });
out.absent = loadedSelectorModel(null);

// ---- the MOUNTED rail: options, hover names, empty state, selection ----
const KEY = { repository: 'fixture-repo', ref: 'main',
              tile_kind: 'staged', tile_id: 't' };
function mountRail(stateRef, selectBuffer) {
  const host = new Node('div');
  host.ownerDocument = doc;
  const rail = mountDoxBenchChatRail(host, {
    scopeKey: KEY,
    transports: { catalog: async () => ({ schema_version: 1,
      kind: 'workbench-model-catalog', models: [] }), chatTurn: async () => null },
    editorState: () => stateRef.value,
    selectBuffer,
  });
  return { host, rail };
}

{
  const stateRef = { value: FIVE };
  const chosen = [];
  const { host, rail } = mountRail(stateRef, async (key) => { chosen.push(key); });
  await rail.ready;
  const select = byClass(host, 'doxchat-loaded')[0];
  out.mounted = {
    ariaLabel: select.getAttribute('aria-label'),
    autocomplete: select.getAttribute('autocomplete'),
    disabled: select.disabled === true,
    value: select.value,
    options: select.children.map((o) => ({
      value: o.value, label: o.textContent,
      title: o.getAttribute('title'),
      ariaLabel: o.getAttribute('aria-label'),
      owned: o.getAttribute('data-owned'),
      dirty: o.getAttribute('data-dirty'),
      selected: o.getAttribute('selected'),
    })),
  };
  out.fullNameRegion = byClass(host, 'doxchat-loaded-full')[0].textContent;
  out.emptyHidden = byClass(host, 'doxchat-loaded-empty')[0].hidden;
  // SELECTING is immediate and goes through the injected seam.
  select.value = ZULU;
  await fire(select, 'change');
  out.selected = chosen.slice();
  // A value naming no held buffer is put back rather than acted on.
  select.value = 'ideation/staging/t/never-loaded.md';
  await fire(select, 'change');
  out.refusedSelection = { chosen: chosen.slice(), value: select.value };
  // Brett's 2026-08-21 annotation: the standing header line is REMOVED, and the
  // binding is read off the selector's own selection and the sr-only full-name
  // region asserted above.
  out.headerAbsent = byClass(host, 'doxchat-header').length === 0;
}

{
  const stateRef = { value: {
    active_buffer: 'outline',
    buffers: { outline: bufferOf('outline', 'ideation/staging/t/t.md') } } };
  const { host, rail } = mountRail(stateRef, async () => {});
  await rail.ready;
  const select = byClass(host, 'doxchat-loaded')[0];
  out.railEmpty = {
    options: select.children.map((o) => o.value),
    value: select.value,
    note: byClass(host, 'doxchat-loaded-empty')[0].textContent,
    hidden: byClass(host, 'doxchat-loaded-empty')[0].hidden,
  };
}

console.log(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def selector_results(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench selector probe")
    root = tmp_path_factory.mktemp("doxbench-loaded-selector")
    for name in ("doxbench-chat.js", "doxbench-chat-model.js"):
        shutil.copy(VIEWS / name, root / name)
    (root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    harness = root / "selector-harness.mjs"
    harness.write_text(_SELECTOR_HARNESS, encoding="utf-8")
    done = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=60)
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


def test_the_selector_lists_every_loaded_document_and_names_the_selected_one(
        selector_results):
    """The delta's `Several documents are loaded` scenario: all of them listed,
    none folded away, dropped, or evicted to fit -- the control IS the overflow
    policy (design D6)."""
    model = selector_results["five"]
    keys = [entry["key"] for entry in model["entries"]]
    # The outline leads, because the selector's selected entry must be able to BE
    # the selected buffer -- a selector that could not show an outline selection
    # would disagree with the canvas the moment the outline tab was focused.
    assert keys[0] == "outline"
    assert keys[1:] == [
        "ideation/staging/t/alpha.md",
        "ideation/staging/t/delta.md",
        "ideation/staging/t/nested/alpha.md",
        "ideation/staging/t/zulu.md",
        "docs/inherited.md",
    ] or sorted(keys[1:]) == sorted([
        "ideation/staging/t/alpha.md",
        "ideation/staging/t/delta.md",
        "ideation/staging/t/nested/alpha.md",
        "ideation/staging/t/zulu.md",
        "docs/inherited.md",
    ])
    assert model["documentCount"] == 5
    assert [e["key"] for e in model["entries"] if e["selected"]] == [
        "ideation/staging/t/nested/alpha.md"]
    assert model["emptyNote"] is None


def test_the_listing_order_is_the_declared_deterministic_one(selector_results):
    """Ascending lexicographic by buffer key, exactly as `doxbench-state.js`
    declares it -- a listing whose order depended on insertion would reorder
    itself under the human's cursor."""
    keys = [e["key"] for e in selector_results["five"]["entries"]][1:]
    assert keys == sorted(keys)


def test_two_loaded_documents_sharing_a_basename_stay_distinguishable(
        selector_results):
    """The delta's `Two loaded documents share a basename` scenario. A selector
    that cannot tell two files apart is worse than one that shows a longer
    name, so a colliding entry grows leftwards until every label is distinct --
    and the non-colliding entry keeps its short basename."""
    labels = selector_results["labels"]
    assert labels["ideation/staging/t/zulu.md"] == "zulu.md"
    assert labels["ideation/staging/t/alpha.md"] == "t/alpha.md"
    assert labels["ideation/staging/t/nested/alpha.md"] == "nested/alpha.md"
    assert len(set(labels.values())) == len(labels)


def test_a_long_name_is_revealed_on_hover_and_to_assistive_technology(
        selector_results):
    """The delta's `A long filename does not fit` scenario. Hover is Q1's own
    word; the assistive half is a SEPARATE obligation a title attribute alone
    does not discharge, so the selected entry's full name is also stated in a
    live region."""
    options = selector_results["mounted"]["options"]
    for option in options:
        if option["value"] == "outline":
            continue
        assert option["title"] == option["value"]
        assert option["ariaLabel"] == option["value"]
        # The visible label is shorter than the full path it stands for.
        assert len(option["label"]) <= len(option["value"])
    assert selector_results["fullNameRegion"] == (
        "Working on ideation/staging/t/nested/alpha.md")


def test_a_context_only_entry_declares_its_non_owned_status(selector_results):
    """Design D2: a context-only document is loadable for grounding, and its
    non-owned status rides the entry so the surface never implies it can be
    saved here."""
    options = {o["value"]: o for o in selector_results["mounted"]["options"]}
    assert options["docs/inherited.md"]["owned"] == "false"
    assert options["ideation/staging/t/zulu.md"]["owned"] is None
    assert options["ideation/staging/t/alpha.md"]["dirty"] == "true"


def test_selecting_is_immediate_and_goes_through_the_one_selection_authority(
        selector_results):
    """Design D7: the selector renders `state.active_buffer` and SETS it through
    the injected seam. It is not a second state authority, and there is no
    confirmation step, because changing which buffer is selected replaces no
    content and destroys nothing."""
    assert selector_results["selected"] == ["ideation/staging/t/zulu.md"]


def test_a_value_naming_no_held_buffer_is_put_back_rather_than_acted_on(
        selector_results):
    refused = selector_results["refusedSelection"]
    assert refused["chosen"] == ["ideation/staging/t/zulu.md"], (
        "a selection naming no held buffer must reach the seam")
    assert refused["value"] == "ideation/staging/t/nested/alpha.md", (
        "the selector must render the selection the state actually holds")


def test_the_selector_states_the_binding_without_a_standing_header_line(
        selector_results):
    """The chat STATES its current binding on the chat surface itself and makes
    it SELECTABLE there. Phase A stated it on a standing header line beside the
    selector; Brett's 2026-08-21 annotation on `div.doxchat-header` ("remove
    this section.") removed that line as a restatement of what the selector
    below it already showed. The obligation now rests entirely on the selector's
    own SELECTED entry plus the sr-only full-name region — both asserted here so
    the removal cannot quietly take the binding statement with it."""
    assert selector_results["headerAbsent"] is True, (
        "the standing header line must not come back")
    # READ: the selector renders the bound buffer, and names it in full for
    # assistive technology.
    assert selector_results["refusedSelection"]["value"] == (
        "ideation/staging/t/nested/alpha.md")
    assert selector_results["fullNameRegion"] == (
        "Working on ideation/staging/t/nested/alpha.md")
    # …and the loaded COUNT the header used to claim is the selector's own
    # listing, which is where a human can also act on it.
    documents = [option for option in selector_results["mounted"]["options"]
                 if option["value"] != "outline"]
    assert len(documents) == 5


def test_the_empty_state_is_rendered_honestly_rather_than_hidden(
        selector_results):
    """The delta's `Nothing is loaded yet` scenario: the selector renders its
    empty state rather than hiding, and the outline remains selectable and
    workable on its own."""
    model = selector_results["empty"]
    assert [e["key"] for e in model["entries"]] == ["outline"]
    assert model["entries"][0]["selected"] is True
    assert model["documentCount"] == 0
    assert model["emptyNote"] == selector_results["emptyNote"]
    assert "outline is workable on its own" in selector_results["emptyNote"]
    rail = selector_results["railEmpty"]
    assert rail["options"] == ["outline"]
    assert rail["value"] == "outline"
    assert rail["hidden"] is False
    assert rail["note"] == selector_results["emptyNote"]
    # …and a rail with a loaded set does NOT show the empty note.
    assert selector_results["emptyHidden"] is True


def test_selection_from_another_route_leaves_the_selector_agreeing(
        selector_results):
    """The delta's `Selection is changed from another route` scenario: the
    selector is rebuilt from the live state on every render, so "the selector,
    the canvas and the chat agree" is structural rather than a rule three call
    sites have to remember."""
    assert selector_results["outlineSelected"][0] == ["outline", True]
    assert all(selected is False
               for _, selected in selector_results["outlineSelected"][1:])


def test_an_absent_editor_state_degrades_to_an_honest_empty_selector(
        selector_results):
    """The rail mounts before the canvas's initial load settles, and a selector
    that threw on an absent state would take the whole rail down with it."""
    model = selector_results["absent"]
    assert model["entries"] == []
    assert model["documentCount"] == 0
    assert model["selected"] == "outline"


# ---------------------------------------------------------------------------
# the surfaces declare their own rules
# ---------------------------------------------------------------------------


def test_every_new_surface_declares_its_own_styles():
    """The house rule: "the rail once shipped with ZERO rules under a green
    suite. Any new surface declares its own"."""
    styles = STYLES.read_text(encoding="utf-8")
    for selector in (".swb-docload", ".swb-docsave", ".swb-docverbnote",
                     ".swb-doctile.swb-docloaded", ".swb-doctile.swb-docneedssave",
                     ".doxchat-loaded", ".doxchat-loaded-empty"):
        assert selector in styles, f"{selector} has no rules at all"


def test_the_shell_wires_the_tile_verbs_through_the_canvas_controller():
    """The tile's verbs reach the loaded set and the governed Save through the
    CANVAS's own primitives -- no second loaded-set store, no second save path.
    Anchored on the mount call rather than on a character distance."""
    source = (VIEWS / "staging-workbench.js").read_text(encoding="utf-8")
    mount = source.index("renderDocWheel(selector")
    window = source[mount:mount + 1800]
    assert "onRead:" in window
    assert "onLoad:" in window
    assert "onSave:" in window
    assert "bufferStateFor:" in window
    # …and the verbs themselves go through the canvas controller.
    verbs = source[source.index("function docTileVerbs()"):][:6000]
    assert "canvasController.loadDocumentForEditing" in verbs
    assert "canvasController.saveDocument" in verbs
    # …and the load's OTHER route, for a reserved slot that is still unbacked:
    # `selectDocument` through the shell's own `bindCanvasToDocument`, which is
    # where Phase A's unsaved-edit guard still applies (PR #207 review, F1).
    assert "bindCanvasToDocument(path)" in verbs
    assert "docBufferState" in verbs


def test_the_rail_is_given_the_loaded_set_seams():
    """The rail owns the loaded set's two human acts — SELECT and UNLOAD — and both
    reach the canvas's own primitives, which hold the state authority and the dirty
    refusal. The window widened when `unloadBuffer` joined it (PR #207 review, F9);
    both are asserted rather than only the one that was there first."""
    source = (VIEWS / "staging-workbench.js").read_text(encoding="utf-8")
    mount = source.index("mountDoxBenchChatRail(rail")
    window = source[mount:mount + 5000]
    assert "selectBuffer:" in window
    assert "canvasController.setActiveBuffer" in window
    assert "unloadBuffer:" in window
    assert "canvasController.unloadDocument" in window
