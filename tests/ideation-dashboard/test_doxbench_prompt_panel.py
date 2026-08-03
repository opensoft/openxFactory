"""THE PROMPT PANEL: model picker and effort slider inside the composer.

RED-FIRST: authored before the panel exists.

SOURCE. Brett, 2026-08-03: "lets make the prompt pannel for our chat pannel ...
make this look like the prompt panel from chatgpt desktop. it should allow the
model slection and then a slider for the effort level just like codex/chatgpt
desktop app. this will give us more space removing this dropdown from the top
of the panel."

THE CONSTRAINT THAT SHAPES ALL OF THIS. The released chat-turn request envelope
is CLOSED (`additionalProperties: false`) and its properties are fixed:
schema_version, kind, client_turn_id, scope, active_document_path,
working_subject, message, model_id, last_assistant_turn_id, transcript,
buffers. There is no effort field, and the model-catalog entry is closed too
(model_id, label, provider_class, available, input_limit_bytes,
output_limit_bytes, data_handling). So an effort value CANNOT travel as its own
field without changing the released contract.

`model_id` is therefore the only channel, and the catalog owns its meaning. An
effort level is expressed as a SEPARATE CATALOG ENTRY — `<family>.<effort>` —
which makes the slider strictly governed: it can only ever offer a
configuration the plane already advertised as approved and available. The
console never invents an id; it selects an entry it was handed.

That convention is a DISPLAY grouping only. Two rules keep it honest:

  1. every id the console sends is one the catalog advertised, verbatim (the
     separator is a DOT, not a colon, because the schema constrains model_id to
     `^[A-Za-z0-9][A-Za-z0-9._-]*$` — the route refuses a colon outright);
  2. when the catalog advertises no effort variants, NO SLIDER RENDERS — the
     console must never show a control the plane gave it nothing to drive.
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
CHAT_JS = VIEWS / "doxbench-chat.js"
CHAT_MODEL_JS = VIEWS / "doxbench-chat-model.js"
STYLES = WEB / "styles.css"

_HARNESS = """
import { modelFamilies, EFFORT_LEVELS, effortOfModelId, familyOfModelId,
         modelIdForEffort } from "./doxbench-chat-model.mjs";

const HANDLING = "Subscription-primary: consumer terms, not ZDR.";
const entry = (id, label, available = true) => ({
  model_id: id, label, provider_class: "subscription-primary",
  available, input_limit_bytes: 800000, output_limit_bytes: 60000,
  data_handling: HANDLING,
});

// a catalog that advertises TWO families, one with four efforts, one with one
const GRADED = [
  entry("claude-sonnet-subscription.low", "Claude Sonnet"),
  entry("claude-sonnet-subscription.medium", "Claude Sonnet"),
  entry("claude-sonnet-subscription.high", "Claude Sonnet"),
  entry("claude-sonnet-subscription.max", "Claude Sonnet"),
  entry("claude-haiku-subscription", "Claude Haiku"),
];
// today's catalog: no effort variants at all
const FLAT = [
  entry("claude-sonnet-subscription", "Claude Sonnet"),
  entry("claude-haiku-subscription", "Claude Haiku"),
];
// an unavailable variant must never become a slider position
const WITH_UNAVAILABLE = [
  entry("m.low", "M"), entry("m.high", "M", false), entry("m.max", "M"),
];

const out = {
  levels: EFFORT_LEVELS,
  graded: modelFamilies(GRADED),
  flat: modelFamilies(FLAT),
  unavailable: modelFamilies(WITH_UNAVAILABLE),
  none: modelFamilies([]),
  effortOf: {
    graded: effortOfModelId("claude-sonnet-subscription.high"),
    plain: effortOfModelId("claude-haiku-subscription"),
    bogus: effortOfModelId("claude-haiku-4.5"),
    empty: effortOfModelId(""),
  },
  familyOf: {
    graded: familyOfModelId("claude-sonnet-subscription.high"),
    plain: familyOfModelId("claude-haiku-subscription"),
    bogus: familyOfModelId("claude-haiku-4.5"),
  },
  pick: {
    real: modelIdForEffort(modelFamilies(GRADED)[0], "high"),
    absent: modelIdForEffort(modelFamilies(GRADED)[0], "xhigh"),
    nofam: modelIdForEffort(null, "high"),
  },
};
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def probe(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the prompt-panel probe")
    tmp = tmp_path_factory.mktemp("prompt-panel")
    shutil.copy(CHAT_MODEL_JS, tmp / "doxbench-chat-model.mjs")
    harness = tmp / "probe.mjs"
    harness.write_text(_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


# ---------------------------------------------------------------------------
# grouping the catalog into families and efforts
# ---------------------------------------------------------------------------


def test_the_effort_levels_are_the_ones_the_runtime_accepts(probe):
    """low · medium · high · xhigh · max — the CLI's own set, read off its
    refusal message. Inventing a sixth would offer a level nothing honours."""
    assert probe["levels"] == ["low", "medium", "high", "xhigh", "max"]


def test_a_graded_catalog_collapses_into_families(probe):
    fams = probe["graded"]
    assert [f["familyId"] for f in fams] == [
        "claude-sonnet-subscription", "claude-haiku-subscription"]
    assert fams[0]["label"] == "Claude Sonnet"
    assert fams[0]["efforts"] == ["low", "medium", "high", "max"]


def test_efforts_are_ordered_by_strength_not_by_catalog_order(probe):
    """A slider's positions must ascend. The catalog is a set, not a
    sequence, so the order comes from EFFORT_LEVELS."""
    assert probe["graded"][0]["efforts"] == ["low", "medium", "high", "max"]


def test_a_family_with_no_variants_reports_no_efforts(probe):
    """"Claude Haiku" is advertised once, with no effort suffix. It is still a
    family — it just has nothing for a slider to move through."""
    haiku = probe["graded"][1]
    assert haiku["familyId"] == "claude-haiku-subscription"
    assert haiku["efforts"] == []
    assert haiku["plainId"] == "claude-haiku-subscription"


def test_todays_catalog_yields_two_families_and_no_slider_anywhere(probe):
    """THE HONEST-DEGRADATION CASE, and the one that is live right now: the
    operator's adapter advertises two plain entries. The panel must render a
    model picker and NO effort control at all."""
    fams = probe["flat"]
    assert len(fams) == 2
    assert all(f["efforts"] == [] for f in fams)


def test_an_unavailable_variant_is_not_a_slider_position(probe):
    """`available: false` is the plane withdrawing a configuration. A slider
    that could still land on it would offer what the catalog refused."""
    fam = probe["unavailable"][0]
    assert fam["efforts"] == ["low", "max"], fam
    assert "high" not in fam["efforts"]


def test_an_empty_catalog_yields_no_families(probe):
    assert probe["none"] == []


# ---------------------------------------------------------------------------
# reading and choosing ids — never fabricating one
# ---------------------------------------------------------------------------


def test_the_effort_of_an_id_is_read_only_when_it_is_a_real_level(probe):
    e = probe["effortOf"]
    assert e["graded"] == "high"
    assert e["plain"] is None
    assert e["bogus"] is None, (
        "a dot suffix that is not an effort level must not be read as one — "
        "a real provider id like claude-haiku-4.5 ends in one")
    assert e["empty"] is None


def test_the_family_of_an_id_keeps_a_non_effort_suffix(probe):
    f = probe["familyOf"]
    assert f["graded"] == "claude-sonnet-subscription"
    assert f["plain"] == "claude-haiku-subscription"
    assert f["bogus"] == "claude-haiku-4.5", (
        "splitting on a dot that is not an effort marker would invent a "
        "family that the catalog never advertised")


def test_choosing_an_effort_returns_the_catalogs_own_id(probe):
    """THE governing rule: the console selects an ADVERTISED entry. It never
    composes `family + ':' + effort` itself, because a composed string could
    name a configuration the plane never approved."""
    assert probe["pick"]["real"] == "claude-sonnet-subscription.high"


def test_choosing_an_effort_the_catalog_lacks_returns_nothing(probe):
    assert probe["pick"]["absent"] is None
    assert probe["pick"]["nofam"] is None


def test_the_console_never_composes_a_model_id():
    """Source contract for the rule above. If the view or the model ever
    builds an id by concatenation, the slider stops being governed by the
    catalog and starts asserting configurations of its own."""
    for source_file in (CHAT_JS, CHAT_MODEL_JS):
        source = source_file.read_text(encoding="utf-8")
        assert not re.search(r'\+\s*"[.:]"\s*\+', source), (
            f"{source_file.name} composes a model id from parts")


# ---------------------------------------------------------------------------
# the panel itself
# ---------------------------------------------------------------------------


def test_the_model_dropdown_is_gone_from_the_top_of_the_panel():
    """The ask in one line: "this will give us more space removing this
    dropdown from the top of the panel"."""
    source = CHAT_JS.read_text(encoding="utf-8")
    assert 'el("select", "doxchat-model")' not in source, (
        "the top-of-panel model <select> is still there")


def test_the_prompt_panel_holds_the_composer_and_its_controls():
    source = CHAT_JS.read_text(encoding="utf-8")
    for cls in ("doxchat-prompt", "doxchat-tools", "doxchat-modelpill"):
        assert cls in source, f"the prompt panel has no {cls}"
    prompt = source.index("doxchat-prompt")
    composer = source.index('"doxchat-composer"')
    assert abs(prompt - composer) < 3000, (
        "the composer is not constructed inside the prompt panel")


def test_the_model_picker_is_a_real_menu_button():
    """CHK007 failed on this surface for correct roles with no keyboard. A
    button that opens a listbox needs the whole pattern, not just the role."""
    # Whole-file, not a window after the pill: the element is constructed in
    # one place and its handlers are bound in another, which is the right
    # structure — a proximity window would only be measuring that choice.
    source = CHAT_JS.read_text(encoding="utf-8")
    for needle in ("aria-haspopup", "aria-expanded", '"listbox"', '"option"',
                   "aria-selected", "Escape", "ArrowDown", "ArrowUp"):
        assert needle in source, f"the model picker is missing {needle}"


def test_the_effort_slider_is_a_native_range_with_a_spoken_value():
    """A range input gives keyboard control for free. `aria-valuetext` is what
    stops a screen reader announcing "3" — the number is meaningless, the
    level is the fact."""
    source = CHAT_JS.read_text(encoding="utf-8")
    assert "doxchat-effort" in source
    assert 'type = "range"' in source or '"range"' in source
    assert "aria-valuetext" in source, (
        "the slider announces a bare index instead of the effort level")


def test_the_slider_is_absent_when_the_catalog_advertises_no_efforts():
    """The honest-degradation rule, in the view. Today's live catalog has no
    variants, so a slider rendered anyway would be a control wired to
    nothing."""
    source = CHAT_JS.read_text(encoding="utf-8")
    assert re.search(r"hidden\s*=\s*efforts\.length\s*<\s*2", source), (
        "nothing hides the slider when the selected family advertises fewer "
        "than two efforts — it would be a control wired to nothing")
    assert re.search(r"efforts\.length\s*<\s*2\)\s*return", source), (
        "the slider is hidden but still populated; the guard must stop before "
        "writing a value the catalog cannot honour")


def test_the_handling_disclosure_survives_the_restructure():
    """The old <option> text carried each model's data_handling — consumer
    subscription terms, NOT an enterprise ZDR agreement. Moving to a pill must
    not drop it: it has to be reviewable BEFORE selection (in the menu) and
    visible at the send moment."""
    source = CHAT_JS.read_text(encoding="utf-8")
    model_source = CHAT_MODEL_JS.read_text(encoding="utf-8")
    # The terms reach the menu as the FAMILY's handling — the model layer is
    # what reads `data_handling` off the catalog entry, so assert the chain
    # rather than the field name appearing in the view.
    assert "data_handling" in model_source, (
        "the family grouping no longer carries each model's handling terms")
    assert "family.handling" in source, (
        "the menu rows no longer render the handling terms, so a model can be "
        "chosen without its terms being reviewable")
    assert "doxchat-menuterms" in source, (
        "the terms have no element of their own in the menu row")
    # And at the send moment, unchanged.
    assert "sendDisclosure" in source


def test_the_panel_is_styled():
    styles = STYLES.read_text(encoding="utf-8")
    for selector in (".doxchat-prompt", ".doxchat-tools", ".doxchat-modelpill",
                     ".doxchat-menu", ".doxchat-effort"):
        assert selector in styles, f"{selector} has no rules at all"


def test_escape_in_the_menu_does_not_reach_the_workbench_overlay():
    """MEASURED DEFECT, pinned (2026-08-03). The menu's Escape handler called
    preventDefault but not stopPropagation, so the key travelled on to the
    workbench overlay's own close handler and tore the whole rail down — the
    rig found `.doxchat-menu` itself gone from the DOM after one Escape.
    "Never mind, close this little menu" must never mean "discard my authoring
    session"."""
    source = CHAT_JS.read_text(encoding="utf-8")
    handler = source[source.index("modelMenu.addEventListener(\"keydown\""):]
    body = handler[:handler.index("});")]
    assert "stopPropagation" in body, (
        "the model menu's keys still bubble to the overlay; Escape will close "
        "the workbench instead of the menu")


def test_the_disclosure_is_clamped_rather_than_dropped():
    """MEASURED (2026-08-03). Rendering the ~250-character handling paragraph
    in full grew the prompt panel from 121px to 246px the moment a model was
    selected, taking the transcript from 63% of the rail to 47% — the opposite
    of what moving the picker into the panel was for.

    The fix must be a VISUAL clamp, never a truncation: the full text stays in
    the DOM so the live region announces all of it, and `title` returns it on
    hover. Measured after: panel 157px, transcript 58%."""
    styles = STYLES.read_text(encoding="utf-8")
    rule = re.search(r"\.doxchat-disclosure\s*\{([^}]*)\}", styles)
    assert rule, "the disclosure has no rule"
    assert "line-clamp" in rule.group(1), (
        "the disclosure is unclamped and will cost the transcript its height")
    source = CHAT_JS.read_text(encoding="utf-8")
    assert "disclosure.title = handling" in source, (
        "the clamped text has no way back — set title to the full handling")
    assert "slice(" not in source[source.index("disclosure.textContent"):][:200], (
        "the disclosure text is being cut in JS; a screen reader would then "
        "announce a sentence that stops mid-word")
