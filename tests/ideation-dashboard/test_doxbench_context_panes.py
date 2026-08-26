"""The context pane restructure: the lens in three subtabs, and a docs pane
split between a selector and the selected document's abstract.

RED-FIRST: authored before either restructure exists.

SOURCE. Two operator annotations, verbatim (vibe-annotations MCP, both
`pending`, selector `div.swb-body`):

  * `vibe_1785602062606_397p8iakz` — "when this pane is showing the lens ...
    restructure this so that the 3 sections of the lens widget are in 3
    subtabs."
  * `vibe_1785602331813_gvku9sh2s` — "when this pane shows the docs: on the
    docs subpane, split this vertically. make the lower half be the same
    wheel of the docs we have used before ... for the top half when a doc is
    selected on the wheel, we load a viewer of that doc. so the top half of
    shows the doc slected distilled summary abstract. it is an abstract that
    is the surfaces the key items delivered by doc."

THE WHEEL LANDED (2026-08-03, later the same day this scope note was first
written — see `test_doc_wheel.py`). The mini-wheel this note once deferred —
"the same wheel at 0.4 radius" needing a reusable single-wheel widget
extracted from `renderWheel`, which draws all six deck columns at a
viewport-derived radius — was extracted into its own module, `doc-wheel.js`
(`renderDocWheel`), and the lower half of this split is that widget at its
own 0.4 radius: the deck's own drum reused, not a placeholder list. The
compact document selector this note describes existed only until then. This
file pins that the split MOUNTS the wheel and wires its selection to the
abstract above (`test_the_docs_pane_is_split_into_selector_and_abstract`
below); the wheel's own derivation, radius and gesture pins live in
`test_doc_wheel.py`.

THE DETERMINISTIC ABSTRACT was RULED "header + structure, honestly labelled"
(Brett, 2026-08-03): the facts the snapshot ALREADY indexes for that
document — its own Summary, declared Topics, stage/kind, where it lands, and
the five completeness signals. That ruling said it is not an AI distillation
and must not be captioned as one — true of THIS abstract, and it still is.

REVERSED IN PART, 2026-08-25 (Brett ruled option C on #84, recorded on the
issue): the deterministic abstract above SURVIVES exactly as ruled, captioned
"From the document's own headers" — never "distilled". Beside it, doxBench
now ALSO generates a SEPARATE, model-derived abstract on explicit human
request (`add-doxbench-distilled-abstract`) — a sibling artifact, not a
replacement, captioned "Distilled by a model — not authoritative; regenerable
from the document." The two are captioned so a reader can never mistake one
for the other. The whole-file source sweep that used to pin the 08-03 ruling
here is gone: with both captions living in this one file, only a source
sweep could no longer tell "the model-derived abstract correctly says
distilled" from "the deterministic one wrongly does" — so the pin now lives
on the Node harness fixture below, as a per-abstract CAPTION FIELD assertion
against `doxbench_knowledge.RULED_CAPTIONS`.

WHAT THESE PROVE. Structure and derivation, in Node and by source contract.
They do not prove rendered geometry — that stays with the operator rig
(`~/browser-ui-operator/measure_workspace.py`), which is what caught the two
defects the previous slice's suite could not see.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess

import pytest

from conftest import REPO_ROOT  # noqa: F401  (sys.path side effect)

from ideation_dashboard import doxbench_knowledge as kn  # noqa: E402
# The SAME DOM instrument the full-shell composition suite drives, imported
# rather than copied (`test_doxbench_composition.py`'s own reasoning): a
# second shim is a second set of behaviours to keep in step, and a keydown
# harness that quietly drifted from the canvas one is exactly how a
# behavioural pin would stop meaning anything.
from test_doxbench_view import _EDITOR_DOM_SHIM  # noqa: E402

NODE = shutil.which("node")
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
VIEWS = WEB / "views"
SHELL_JS = VIEWS / "staging-workbench.js"
MODEL_JS = VIEWS / "staging-workbench-model.js"
STYLES = WEB / "styles.css"

LENS_SUBTABS = ("keywords", "bullseye", "matrix")

_ABSTRACT_HARNESS = """
import { documentAbstract } from "./staging-workbench-model.mjs";

const DOC = {
  path: "ideation/staging/topic-x/topic-x.md",
  id: "topic-x", stage: "staged", kind: "capability-proposal",
  summary: "A neutral contract for the thing every domain re-invents.",
  topics: ["alpha", "beta", "gamma"],
  destinations: { staged_topics: ["topic-x"], capabilities: ["cap-a"] },
  completeness: { score: 0.65, structure: { value: 1, count: 6 },
                  length: { value: 0.8, count: 320 },
                  open_markers: { value: 0.4, count: 3 },
                  keyword_coverage: { value: 0.5, count: 3 },
                  link_degree: { value: 0.66, count: 4 } },
};
const BARE = { path: "docs/plain.md", id: "plain", resolved: true };

const out = {
  full: documentAbstract(DOC),
  bare: documentAbstract(BARE),
  none: documentAbstract(null),
};
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def abstract(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the document-abstract probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-abstract")
    shutil.copy(MODEL_JS, tmp_path / "staging-workbench-model.mjs")
    harness = tmp_path / "abstract-harness.mjs"
    harness.write_text(_ABSTRACT_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# the abstract — derivation only, from what the snapshot already indexes
# ---------------------------------------------------------------------------


def test_the_abstract_surfaces_what_the_document_declares(abstract):
    a = abstract["full"]
    assert a["title"] == "topic-x.md"
    assert a["summary"].startswith("A neutral contract")
    assert a["topics"] == ["alpha", "beta", "gamma"]
    assert a["stage"] == "staged"
    assert a["kind"] == "capability-proposal"


def test_the_abstract_names_where_the_document_lands(abstract):
    """`destinations` is how a reader learns what this document FEEDS — the
    closest thing the snapshot has to 'key items delivered'."""
    lands = abstract["full"]["lands"]
    assert any("topic-x" in entry for entry in lands)
    assert any("cap-a" in entry for entry in lands)


def test_the_abstract_carries_the_completeness_signals_not_just_the_score(abstract):
    """The score alone says 0.65 and explains nothing. The five signals say
    WHICH part is thin — that is the actionable half."""
    signals = abstract["full"]["signals"]
    names = sorted(s["name"] for s in signals)
    assert names == sorted(["structure", "length", "open_markers",
                            "keyword_coverage", "link_degree"])
    markers = next(s for s in signals if s["name"] == "open_markers")
    assert markers["count"] == 3


def test_the_abstract_is_honest_about_a_document_it_knows_nothing_about(abstract):
    """A document the snapshot carries no derivation for must render an
    explicit absence, never an empty box that reads as 'nothing to say'."""
    bare = abstract["bare"]
    assert bare["title"] == "plain.md"
    assert bare["summary"] is None
    assert bare["signals"] == []
    assert bare["note"], "an unindexed document states no reason for its emptiness"


def test_the_abstract_refuses_no_document(abstract):
    assert abstract["none"] is None


def _flatten_strings(value):
    """Yield every string value inside a JSON-shaped structure, depth-first.

    Used by the two captioning pins below to check a claim never appears
    ANYWHERE in a model object — every field, every nested list/dict entry —
    not only in the fields an author remembered to name, which is the same
    generality the retired whole-file source sweep had (it read the entire
    file, not a hand-picked set of lines) and which a field-by-field
    assertion would quietly lose."""
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _flatten_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from _flatten_strings(v)


def test_the_deterministic_caption_field_matches_ruled_text_once_present(abstract):
    """THE RELOCATED PIN (add-doxbench-distilled-abstract, ruling 5 / task
    8.1), now in its SECOND and final phase. This replaced
    `test_the_abstract_is_never_captioned_as_a_distillation`, which used to
    sweep the WHOLE `staging-workbench.js` source for "distilled"/"ai
    summary"/"ai-generated" (RULED, Brett, 2026-08-03; see the module docstring
    above for the full 2026-08-25 reversal this pin now honours). Once the
    model-derived abstract's own caption shipped containing "Distilled by a
    model...", a file-level sweep could no longer tell that caption FROM a
    violation on the deterministic one — both abstracts live in the same file —
    so the pin moved onto this Node harness fixture, per-abstract, keyed on
    `doxbench_knowledge.RULED_CAPTIONS`.

    PHASE TWO, landed with §7.8: `documentAbstract()` now RETURNS a `caption`
    field, so the model-level fallback the first phase ran on — "no string
    value anywhere in the output contains distill" — is GONE, along with its
    TODO. What stands is the assertion the fallback was standing in for: the
    field literally equals `RULED_CAPTIONS[CAPTION_DETERMINISTIC]` ("From the
    document's own headers"), and it never contains "distill" (case-
    insensitive, so it also catches "distillation" — the exact gap the old
    sweep had, since it banned "distilled" but not "distillation"). The
    unconditional model-level invariant it used to share the work with is the
    test below, which is not replaced by this one and covers every OTHER field.

    The field's presence is asserted rather than assumed: a `documentAbstract`
    that quietly stopped returning a caption would otherwise make this test
    vacuous, which is how a relocated pin turns back into a comment.
    """
    for label in ("full", "bare"):
        value = abstract[label]
        assert "caption" in value, (
            f"the deterministic {label} abstract returns no caption field; "
            "§7.8's formatter is what puts it there and the relocated pin has "
            "nothing to assert without it")
        assert value["caption"] == kn.RULED_CAPTIONS[kn.CAPTION_DETERMINISTIC]
        assert "distill" not in value["caption"].lower()


def test_the_deterministic_abstract_is_never_captioned_as_a_distillation(abstract):
    """The half of the 2026-08-03 guard that STAYS TRUE after the 2026-08-25
    reversal (task 8.4 — kept from the deleted whole-file sweep this test
    replaces, at the model level rather than the source level). The
    DETERMINISTIC abstract — `documentAbstract()`'s own output, "header +
    structure" lifted verbatim from the document's own declared fields — must
    never claim a distillation. What FLIPS is the separate model-derived
    sibling abstract (§7.8), which IS captioned as one on purpose; this test
    is scoped to the deterministic abstract only and must never be widened to
    cover that sibling.

    Unlike the test above, this one is UNCONDITIONAL and permanent — it does
    not tighten or wait on the caption field, because "the deterministic
    abstract never claims a distillation" is true regardless of whether a
    `caption` field exists to say so explicitly.
    """
    for label, doc in (("full", abstract["full"]), ("bare", abstract["bare"])):
        for value in _flatten_strings(doc):
            assert "distill" not in value.lower(), (
                f"the deterministic {label} abstract value {value!r} claims "
                "a distillation nothing produced")


# ---------------------------------------------------------------------------
# the lens subtabs
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", LENS_SUBTABS)
def test_the_lens_offers_its_three_sections_as_subtabs(name):
    source = SHELL_JS.read_text(encoding="utf-8")
    assert f'"{name}"' in source, f"the lens has no {name} subtab"


def test_the_lens_subtabs_are_a_real_tablist():
    """CHK007 was a FAIL on this surface once already: correct roles, no roving
    tabindex. A new strip must not repeat it."""
    source = SHELL_JS.read_text(encoding="utf-8")
    strip = source[source.index("swb-subtabs"):]
    for needle in ('role", "tablist"', 'role", "tab"', "aria-selected", "tabIndex"):
        assert needle in strip[:4000], (
            f"the lens subtab strip is missing {needle} — the APG pattern the "
            "context strip already implements")


# ---------------------------------------------------------------------------
# the lens subtabs' KEYBOARD reachability (task 2.5, handed over from
# `ratify-doxbench-landed-context-surfaces` §2.7): the source-text pin above
# only checks that `role`/`aria-selected`/`tabIndex` APPEAR somewhere in the
# strip. It proves nothing about whether Arrow/Home/End actually MOVE
# anything — the behaviour lives in the keydown handler at
# `staging-workbench.js:491-503`, and this is the missing behavioural half.
#
# The file had no DOM double capable of mounting `staging-workbench.js` and
# dispatching real events at it — the `abstract` harness above only imports
# the pure `staging-workbench-model.js`. Rather than build a second DOM shim
# for this one file (a second shim is a second thing to keep in step with the
# full-shell one, which is exactly the drift this suite's captioning pin
# elsewhere exists to avoid), this EXTENDS the harness in this file only by
# reusing `test_doxbench_view._EDITOR_DOM_SHIM` UNMODIFIED — the same DOM
# double `test_doxbench_composition.py` already drives against a real,
# fully-mounted `mountStagingWorkbench` — and adding a small local
# `fire()`/keydown-dispatch helper scoped to this harness string alone, the
# same technique every harness file in this suite already uses locally
# rather than sharing one dispatch helper across files.
# ---------------------------------------------------------------------------

_LENS_TABLIST_HARNESS = _EDITOR_DOM_SHIM + r"""
import { createRequire } from 'node:module';

globalThis.markdownit = createRequire(import.meta.url)('../vendor/markdown-it.min.js');
globalThis.window = { location: { href: 'http://localhost/' } };

// EXTENDING THE SHARED SHIM, IN THIS FILE ONLY (task 2.5(i) covers this too):
// the imported `_EDITOR_DOM_SHIM` has no `document.createElementNS`
// (`bullseye.js` draws its rings as SVG) and each node's `style` is a bare
// object with no `setProperty` (the lens's keyword rail sets a `--h` CSS
// custom property per chip). Neither gap is `test_doxbench_view.py`'s to
// carry — it never mounts the lens's bullseye subtab — so both are patched
// HERE, over the shim's own `document.createElement`, local to this harness
// string and invisible to every other file that imports the shim unmodified.
{
  const rawCreateElement = document.createElement;
  function withStyleMethods(node) {
    node.style.setProperty = (name, value) => { node.style[name] = value; };
    node.style.removeProperty = (name) => { delete node.style[name]; };
    node.style.getPropertyValue = (name) => node.style[name] || '';
    return node;
  }
  document.createElement = (tag) => withStyleMethods(rawCreateElement(tag));
  // `bullseye.js`'s own `svg()` helper only calls
  // `setAttribute`/`textContent`/`appendChild`/`addEventListener` on what it
  // creates — every one already supported by the shim's generic node — so
  // the SVG namespace is served that SAME generic node rather than a second
  // element class this harness would have to maintain.
  document.createElementNS = (_ns, tag) => document.createElement(tag);
}

const { mountStagingWorkbench } = await import('./staging-workbench.js');

function snapshotFor() {
  const path = 'ideation/staging/topic-x/topic-x.md';
  return {
    repository: 'fixture-repo',
    generation: { source_revision: '1'.repeat(40) },
    documents: [{ id: path, path, topics: ['alpha', 'beta'],
                  destinations: { staged_topics: ['topic-x'] } }],
    clusters: [], possibles: [],
    staged_topics: [{ staging_id: 'topic-x', files: [path] }],
  };
}

// Dispatches DIRECTLY on the node the production code registered the
// listener on (the tablist itself, per `staging-workbench.js:491`) rather
// than simulating bubbling from a focused child — this shim has no bubbling
// model, and the production listener is on the tablist regardless.
async function fire(node, type, extra = {}) {
  let prevented = false;
  for (const fn of (node.listeners && node.listeners[type]) || []) {
    await fn({ target: node, stopPropagation() {},
               preventDefault() { prevented = true; }, ...extra });
  }
  return prevented;
}
const settle = () => new Promise((r) => setTimeout(r, 0));
async function quiesce(n = 10) { for (let i = 0; i < n; i += 1) await settle(); }

const container = document.createElement('div');
const doxbench = {
  loadSource: async (path) => ({ content: '# ' + path + '\n', ref: 'main' }),
  storage: { getItem: () => null, setItem() {}, removeItem() {} },
  catalog: async () => ({ schema_version: 1, kind: 'workbench-model-catalog',
                          models: [] }),
  chatTurn: async () => ({ ok: false, status: 502, payload: {} }),
  save: async () => ({ status: 'committed', buffers: [] }),
};
const workbench = mountStagingWorkbench(container, snapshotFor(), {
  caps: { actions: {}, actor: 'brett' },
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
await quiesce();

const byClass = (cls) => container.walk().filter(
  (n) => String(n.className).split(' ').includes(cls));
const one = (cls) => byClass(cls)[0] || null;

// the lens tab is not the default (docs is) — switch to it for real, through
// the same click a human would use, not by reaching into module state
const lensTabBtn = byClass('swb-tab').find((b) => b.textContent === 'lens');
if (!lensTabBtn) throw new Error('no lens tab button found');
await fire(lensTabBtn, 'click');
await quiesce();

const subtabs = one('swb-subtabs');
const subButtons = byClass('swb-subtab');
if (!subtabs || subButtons.length !== 3) {
  throw new Error('lens subtabs did not mount as expected: ' +
                   subButtons.length + ' buttons, tablist ' + !!subtabs);
}

function state() {
  return {
    selected: subButtons.map((b) => b.getAttribute('aria-selected') === 'true'),
    tabIndex: subButtons.map((b) => b.tabIndex),
    focusedIndex: subButtons.indexOf(document.activeElement),
  };
}

const steps = [];
function record(label, prevented) { steps.push({ label, prevented, ...state() }); }

record('initial', null);
record('arrowRight1', await fire(subtabs, 'keydown', { key: 'ArrowRight' }));
record('arrowRight2', await fire(subtabs, 'keydown', { key: 'ArrowRight' }));
// a THIRD ArrowRight from the last section must WRAP back to the first
record('arrowRight3_wraps', await fire(subtabs, 'keydown', { key: 'ArrowRight' }));
// ArrowLeft from the first section must WRAP to the last
record('arrowLeft_wraps', await fire(subtabs, 'keydown', { key: 'ArrowLeft' }));
record('home', await fire(subtabs, 'keydown', { key: 'Home' }));
record('end', await fire(subtabs, 'keydown', { key: 'End' }));
// an unrelated key must move nothing and must not be consumed
record('unrelated_key', await fire(subtabs, 'keydown', { key: 'a' }));

process.stdout.write(JSON.stringify({
  steps, subtabLabels: subButtons.map((b) => b.textContent),
}));
"""


@pytest.fixture(scope="module")
def lens_tablist(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the lens-tablist probe")
    root = tmp_path_factory.mktemp("doxbench-lens-tablist")
    views = root / "views"
    shutil.copytree(VIEWS, views)
    shutil.copytree(WEB / "vendor", root / "vendor")
    (root / "package.json").write_text('{"type": "module"}', encoding="utf-8")
    (root / "vendor" / "package.json").write_text('{"type": "commonjs"}',
                                                   encoding="utf-8")
    harness = views / "lens-tablist-harness.mjs"
    harness.write_text(_LENS_TABLIST_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True, text=True,
                          timeout=120)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


# index of the section [keywords, bullseye, matrix] that must be selected AND
# focused after each step, and whether that step's key must be consumed
_LENS_TABLIST_EXPECTED = {
    "initial": (0, None),
    "arrowRight1": (1, True),
    "arrowRight2": (2, True),
    "arrowRight3_wraps": (0, True),
    "arrowLeft_wraps": (2, True),
    "home": (0, True),
    "end": (2, True),
    "unrelated_key": (2, False),
}


def test_the_lens_tablist_moves_focus_and_selection_on_arrows_home_and_end(
        lens_tablist):
    """THE MISSING BEHAVIOURAL PIN (task 2.5(i)). The APG roving-tabindex
    pattern is not "the right attributes are somewhere in the source" (that
    is `test_the_lens_subtabs_are_a_real_tablist` above, and it is not
    replaced by this) — it is that ArrowRight/ArrowLeft wrap through the
    three sections, Home/End jump to the ends, focus MOVES WITH selection
    (one roving tabbable tab, always the selected one), the four navigation
    keys are CONSUMED (`ev.preventDefault()`, or the page would scroll
    instead — the exact CHK007 failure mode this pattern exists to avoid),
    and an unrelated key is left alone. Dispatched as real keydown events at
    a really-mounted tablist in the Node harness above, not inferred from
    source text.
    """
    assert lens_tablist["subtabLabels"] == list(LENS_SUBTABS)
    for step in lens_tablist["steps"]:
        label = step["label"]
        expected_index, expected_prevented = _LENS_TABLIST_EXPECTED[label]
        assert step["selected"] == [
            i == expected_index for i in range(3)], label
        assert step["tabIndex"] == [
            0 if i == expected_index else -1 for i in range(3)], label
        assert step["prevented"] == expected_prevented, label
        if label != "initial":
            # focus follows selection — the one roving tabbable tab is the
            # one actually holding focus, not merely marked selected
            assert step["focusedIndex"] == expected_index, label


def test_the_forming_line_survives_the_subtab_split():
    """The forming line states what the checked keywords currently select. It
    is the lens's status, not one of its three sections, so it must stay
    visible whichever subtab is active — hiding it would make the bullseye and
    matrix unreadable in isolation."""
    source = SHELL_JS.read_text(encoding="utf-8")
    forming = source.index('"swb-forming"')
    subtabs = source.index('"swb-subtabs"')
    body = source[min(forming, subtabs):max(forming, subtabs)]
    assert "swb-subtabpane" not in body, (
        "the forming line was moved inside a subtab pane; it is the lens's "
        "status line and belongs outside them")


# ---------------------------------------------------------------------------
# the docs split
# ---------------------------------------------------------------------------


def test_the_docs_pane_is_split_into_selector_and_abstract():
    source = SHELL_JS.read_text(encoding="utf-8")
    assert "swb-docsplit" in source
    assert "swb-docabstract" in source
    assert "swb-docselector" in source


def test_the_docs_split_gives_the_selector_the_lower_half():
    """The annotation is explicit about the arrangement: selector BELOW,
    the selected document's abstract ABOVE it."""
    styles = STYLES.read_text(encoding="utf-8")
    rule = re.search(r"\.swb-docsplit\s*\{([^}]*)\}", styles)
    assert rule, "the docs split has no rule"
    assert "column" in rule.group(1), (
        "the docs split is not a vertical (column) split")
    source = SHELL_JS.read_text(encoding="utf-8")
    assert source.index('"swb-docabstract"') < source.index('"swb-docselector"'), (
        "the selector is constructed above the abstract; the annotation puts "
        "the abstract on top and the selector in the lower half")


# `test_the_deferred_wheel_is_recorded_where_the_selector_stands` — the pin
# that a "wheel is deferred" note stood near `"swb-docselector"` — was DELETED
# here (task 2.5, handed over from `ratify-doxbench-landed-context-surfaces`
# §2.7), not replaced, because the wheel it was deferring landed 2026-08-03
# (see the module docstring above) and it had gone green ONLY BY ACCIDENT
# since: the placeholder note it looked for is long gone, and what it
# actually matched by then was unrelated "wheel" prose that happens to sit
# near the selector. It is FULLY REDUNDANT with two tests already in
# `test_doc_wheel.py`, run in the same suite invocation as this file:
# `test_the_docs_pane_mounts_the_wheel` (`renderDocWheel` / `doc-wheel.js`
# are present where the selector stands) and `test_the_deferral_note_is_gone`
# (the retired "NOT YET A WHEEL" / "ruled out of this slice" notes are
# actually gone). Keeping a third pin for the same fact here would be a
# second copy of one claim to keep in sync, which is the drift this file's
# own captioning-pin relocation exists to avoid elsewhere.


def test_the_restructured_panes_are_height_constrained():
    """MEASURED FAILURE, pinned (2026-08-03). `.swb-body` scrolls and
    `.swb-pane` is unconstrained, so both restructured panes grew to their
    content — the docs selector measured 2445px and the lens subtab container
    1079px — and every `overflow-y: auto` inside them was inert, because
    nothing bounded them. A split whose halves both grow is not a split.

    After the fix: abstract 280px above a 379px selector; lens container 499px
    and scrolling. The suite cannot measure that, so it pins the rule that
    makes it possible."""
    styles = STYLES.read_text(encoding="utf-8")
    rule = re.search(
        r"\.swb-pane-docs,\s*\.swb-pane-lens\s*\{([^}]*)\}", styles)
    assert rule, (
        "the restructured panes are no longer height-constrained; their inner "
        "scroll regions will be inert again")
    body = rule.group(1)
    assert "height" in body and "min-height" in body


def test_the_abstracts_prose_bound_is_the_number_the_280px_budget_bought():
    """S4 (adversarial review, 2026-08-25). THE ABSOLUTE PIN for
    `doxbench_turns.MAX_ABSTRACT_PROSE_BYTES`, and it lives HERE — beside the
    measured height budget — because 1_500 is not a preference: it is what fits
    the 280px region the rule above declares, at the type sizes this sheet sets,
    and `validate_abstract_prose` REFUSES an over-long answer rather than
    trimming it into the box.

    Every other pin on this constant is RELATIVE (it is smaller than the chat
    surface's prose bound; an answer one byte over it is refused), so a mutation
    to 2_000 left all of them green while shipping an abstract that overflows
    the region it was sized for. This one names the number, and the budget it
    came from is one screen above it."""
    from ideation_dashboard import doxbench_turns

    assert doxbench_turns.MAX_ABSTRACT_PROSE_BYTES == 1_500


def test_each_half_of_the_restructured_panes_contains_its_own_overflow():
    """The point of bounding the pane is that neither half can push the other
    out of view: a long document list must not displace the abstract, and a
    long matrix must not displace the subtab strip.

    AMENDED 2026-08-03, when the lower half became the wheel. Scrolling was
    never the requirement — CONTAINMENT was, and scrolling was how a list
    achieved it. A drum achieves it more strongly: it places a fixed reel in
    its own window and spins, so it cannot grow at all, and it must CLIP
    because tiles past the horizon are placed outside the window by design.
    So the halves that hold documents-as-a-list still scroll, and the half that
    holds the wheel contains itself by clipping."""
    styles = STYLES.read_text(encoding="utf-8")
    for selector in (".swb-docabstract", ".swb-subtabpanes"):
        declared = " ".join(
            b for s, b in _RULES(styles)
            if any(part.strip() == selector for part in s.split(",")))
        assert "overflow-y: auto" in declared, (
            f"{selector} does not scroll on its own")
    wheel_window = " ".join(
        b for s, b in _RULES(styles)
        if any(part.strip() == ".swb-docselector" for part in s.split(",")))
    assert "overflow: hidden" in wheel_window, (
        "the wheel window neither scrolls nor clips — its off-horizon tiles "
        "will paint outside the pane")
    assert "min-height: 0" in wheel_window, (
        "the wheel window is not height-constrained, so it will grow to its "
        "content exactly as the unbounded panes did")


def _RULES(css: str):
    """(selector, body) for every rule in the sheet.

    COMMENTS ARE STRIPPED FIRST, and that is not cosmetic: a comment contains no
    braces, so without this it is swallowed into the FOLLOWING rule's selector
    text and that rule stops matching by name. Every documented rule in this
    stylesheet — which is most of the load-bearing ones — was invisible to these
    assertions, so they passed by finding nothing. Caught 2026-08-03 when the
    wheel-window rule was asserted on and came back empty."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        yield match.group(1).strip(), match.group(2)
