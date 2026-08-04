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

SCOPE RULED BY BRETT, 2026-08-03. The mini-wheel is NOT in this slice:
`renderWheel` renders all six columns from a snapshot with a viewport-derived
radius, so "the same wheel at 0.4 radius" needs a reusable single-wheel widget
extracted from that module — its own piece of work, deliberately not rushed
against the most visually complex module in the dashboard. The lower half
carries a compact document selector until that lands.

THE ABSTRACT is "header + structure, honestly labelled" (ruled): the facts the
snapshot ALREADY indexes for that document — its own Summary, declared Topics,
stage/kind, where it lands, and the five completeness signals. It is not an
AI distillation and must not be captioned as one.

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

from conftest import REPO_ROOT

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


def test_the_abstract_is_never_captioned_as_a_distillation():
    """RULED (Brett, 2026-08-03): this is 'header + structure, honestly
    labelled' — the facts already indexed, NOT an AI distillation. Calling it
    one would be the surface claiming an analysis nobody ran."""
    source = SHELL_JS.read_text(encoding="utf-8")
    lowered = source.lower()
    for claim in ("distilled", "ai summary", "ai-generated"):
        assert claim not in lowered, (
            f"the abstract is captioned '{claim}' but nothing distils it")


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


def test_the_deferred_wheel_is_recorded_where_the_selector_stands():
    """Brett ruled the mini-wheel out of THIS slice because it needs a
    reusable single-wheel widget extracted from `renderWheel` (which today
    renders all six columns at a viewport-derived radius). The placeholder
    must say so, so the next reader knows the list is an interim selector and
    not a decision against the wheel."""
    source = SHELL_JS.read_text(encoding="utf-8")
    idx = source.index('"swb-docselector"')
    window = source[max(0, idx - 1600):idx]
    assert "wheel" in window.lower(), (
        "nothing near the selector records that a wheel is the intended "
        "affordance and why it is not here yet")


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
