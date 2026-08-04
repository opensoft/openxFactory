"""The doxBench workspace slice: a Send that cannot submit nothing, and a
three-pane layout a human can actually work in.

RED-FIRST: authored before `canSend`, the expand/full-screen controls, or
their styles exist.

WHY THIS EXISTS. Brett tried to rule five open questions in doxBench and
stopped, twice over:

  * he clicked Send during a slow turn, the composer had already cleared, and
    an EMPTY message went to the server — which refused it as malformed. The
    client's only guard was `sendBtn.disabled = state.phase !== "idle"`, so
    the surface let him send something the contract forbids
    (`message` minLength 1). Two sibling gaps ride along: no model selected,
    and no indication that a turn is in flight;
  * and the working area is too small: the head + session bar own the top of
    the panel while the three panes — where all the work happens — share what
    is left.

WHAT THESE TESTS DO AND DO NOT PROVE. The send gate is a PURE predicate, so
it is tested by behaviour in Node. The layout is CSS, and CSS cannot be
executed by this suite: the tests below pin the stylesheet CONTRACT (the
rules exist, the default survives, the compressed panes keep a non-zero
floor) and the CONTROL contract (the buttons exist, are labelled, and carry
their pressed state). They do NOT prove rendered geometry — a pane can
satisfy every assertion here and still render at 20px. Rendered widths are
measured by the operator rig (`~/browser-ui-operator`/`at_passes.py` family),
which is where the T100 P1-1 unstyled-rail failure was actually caught.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from conftest import REPO_ROOT

NODE = shutil.which("node")
WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
VIEWS = WEB / "views"
CHAT_MODEL_JS = VIEWS / "doxbench-chat-model.js"
CHAT_VIEW_JS = VIEWS / "doxbench-chat.js"
SHELL_JS = VIEWS / "staging-workbench.js"
STYLES = WEB / "styles.css"

# The three regions, in the order the shell appends them. `swb-context` is the
# docs/lens/outline pane; the rail is chat; the canvas is the authoring editor.
REGIONS = ("context", "rail", "canvas")

_SEND_HARNESS = """
import { createChatState, adoptCatalog, selectModel, editComposer, canSend }
  from "./doxbench-chat-model.mjs";

const KEY = { repository: "fixture-repo", ref: "main",
              tile_kind: "staged", tile_id: "topic-x" };
const ENTRY = { model_id: "model-a", label: "Approved authoring model",
                provider_class: "on-tenant", available: true,
                input_limit_bytes: 800000, output_limit_bytes: 900000,
                data_handling: "Processed in the approved tenant boundary" };
const ENVELOPE = { schema_version: 1, kind: "workbench-model-catalog",
                   models: [ENTRY] };

const ready = editComposer(
  selectModel(adoptCatalog(createChatState(KEY), ENVELOPE), "model-a"),
  "a real question");

const out = {
  ready: canSend(ready),
  emptyComposer: canSend(editComposer(ready, "")),
  whitespaceComposer: canSend(editComposer(ready, "   \\n  ")),
  noModel: canSend(editComposer(
    adoptCatalog(createChatState(KEY), ENVELOPE), "a real question")),
  emptyCatalog: canSend(editComposer(adoptCatalog(createChatState(KEY),
    { schema_version: 1, kind: "workbench-model-catalog", models: [] }),
    "a real question")),
  inFlight: canSend({ ...ready, phase: "sending" }),
};
process.stdout.write(JSON.stringify(out));
"""


@pytest.fixture(scope="module")
def send_gate(tmp_path_factory):
    if NODE is None:
        pytest.skip("node not available for the doxBench send-gate probe")
    tmp_path = tmp_path_factory.mktemp("doxbench-send-gate")
    shutil.copy(CHAT_MODEL_JS, tmp_path / "doxbench-chat-model.mjs")
    harness = tmp_path / "send-harness.mjs"
    harness.write_text(_SEND_HARNESS, encoding="utf-8")
    proc = subprocess.run([NODE, str(harness)], capture_output=True,
                          text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_send_is_offered_only_when_a_turn_could_actually_be_built(send_gate):
    """The one state that MAY send: idle, a model chosen, and real text."""
    assert send_gate["ready"] is True


def test_send_refuses_an_empty_or_whitespace_composer(send_gate):
    """THE REPORTED DEFECT. The released request schema requires
    `message` minLength 1, so an empty composer can only ever produce a
    malformed request — the client must not offer it. Whitespace is the same
    fact: it is empty text wearing spaces."""
    assert send_gate["emptyComposer"] is False
    assert send_gate["whitespaceComposer"] is False


def test_send_refuses_without_a_selected_model(send_gate):
    """`model_id` is minLength 1 in the released request schema, and an empty
    catalog is a legitimate editor-only posture — neither may reach the wire
    as a refusal the server has to author."""
    assert send_gate["noModel"] is False
    assert send_gate["emptyCatalog"] is False


def test_send_refuses_while_a_turn_is_in_flight(send_gate):
    """Preserved from the previous guard: one turn in flight per conversation.
    This is the ONLY condition the old `phase !== "idle"` check covered."""
    assert send_gate["inFlight"] is False


def test_the_send_control_states_that_a_turn_is_running(send_gate):
    """A control that is merely disabled explains nothing — the operator
    clicked twice precisely because the button looked available. The view must
    say a turn is running, not just refuse."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert re.search(r'sendBtn\.textContent\s*=', source), (
        "the Send button never changes its label, so an in-flight turn is "
        "invisible on the control the human is looking at")


def test_the_view_gates_send_through_the_pure_predicate(send_gate):
    """The view must not re-derive the rule. A second copy of the condition is
    how the three gaps drifted apart in the first place."""
    source = CHAT_VIEW_JS.read_text(encoding="utf-8")
    assert "canSend(" in source
    assert 'sendBtn.disabled = state.phase !== "idle"' not in source, (
        "the phase-only guard is still present; it is the defect")


# ---------------------------------------------------------------------------
# layout contract — the stylesheet and the controls, NOT rendered geometry
# ---------------------------------------------------------------------------


def test_equal_thirds_remains_the_default_layout():
    """Brett's ruling on annotation vibe_1785561229002_13j8c18kk: thirds is the
    DEFAULT and expand is a temporary override. A slice that quietly changed
    the default would be reversing a ruling, not implementing one."""
    styles = STYLES.read_text(encoding="utf-8")
    assert re.search(r"\.swb-regions\.has-rail[^{]*\{[^}]*33\.33%", styles), (
        "the equal-thirds default rule is gone or no longer 33.33%")


@pytest.mark.parametrize("region", REGIONS)
def test_each_region_can_be_expanded(region):
    styles = STYLES.read_text(encoding="utf-8")
    assert f".swb-regions.is-expanded-{region}" in styles, (
        f"no expand rule for the {region} pane")


PANE_CLASS = {"context": ".swb-context", "rail": ".doxbench-rail",
              "canvas": ".doxbench-canvas"}


def _rules(css: str):
    """(selector, body) for every rule — enough structure to ask which
    declarations actually apply to a pane, instead of matching text shapes."""
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
        yield match.group(1).strip(), match.group(2)


@pytest.mark.parametrize("region", REGIONS)
def test_an_expanded_pane_leaves_the_others_visible(region):
    """Brett asked for the other two to take 'a thinner slice' — NOT to
    disappear. Each compressed pane must keep a non-zero floor, so the context
    it holds is never lost.

    Asks the question by PROPERTY, not by text layout: gather every rule that
    applies while this region is expanded, and check what those rules say
    about the other two panes. An earlier version of this test matched a
    block shape and failed on a stylesheet that was correct — the shape of the
    CSS is not the contract; the declarations are.
    """
    css = STYLES.read_text(encoding="utf-8")
    others = [PANE_CLASS[r] for r in REGIONS if r != region]
    marker = f".swb-regions.is-expanded-{region}"
    floored = {name: False for name in others}
    for selector, body in _rules(css):
        if marker not in selector:
            continue
        assert "display: none" not in body, (
            f"a pane is hidden while {region} is expanded — that loses "
            "context rather than thinning it")
        for name in others:
            if any(part.strip().startswith(marker) and name in part
                   for part in selector.split(",")):
                if "min-width" in body:
                    floored[name] = True
    missing = [name for name, ok in floored.items() if not ok]
    assert not missing, (
        f"while {region} is expanded these panes have no min-width floor and "
        f"can collapse to zero: {missing}")


def test_the_workbench_offers_full_screen_and_per_pane_expand_controls():
    source = SHELL_JS.read_text(encoding="utf-8")
    assert "swb-fullscreen" in source, "no full-screen control is constructed"
    assert "swb-expand" in source, "no per-pane expand control is constructed"


def test_the_layout_controls_carry_state_and_names_for_assistive_tech():
    """Toggles must expose `aria-pressed`; icon-only buttons must carry an
    accessible name (the `repohint` lesson: a glyph is not a name)."""
    source = SHELL_JS.read_text(encoding="utf-8")
    for needle in ("aria-pressed", "aria-label"):
        assert needle in source, (
            f"the layout controls set no {needle}; an icon-only toggle with "
            "neither is unusable and unannounced")


def test_the_head_does_not_reclaim_the_space_this_slice_freed():
    """The operator's complaint was vertical: the head and session bar owned
    the top of the panel while the three panes shared the remainder. Pin the
    compact values so a later style edit cannot silently restore the old
    padding."""
    styles = STYLES.read_text(encoding="utf-8")
    head = re.search(r"\.swb-head\s*\{[^}]*\}", styles)
    assert head, ".swb-head rule is missing"
    padding = re.search(r"padding:\s*(\d+)px", head.group(0))
    assert padding and int(padding.group(1)) <= 8, (
        "the head's vertical padding grew back above 8px")


def test_every_constructed_expand_control_survives_a_pane_remount():
    """MEASURED FAILURE, pinned (2026-08-02). Three controls were constructed
    and only TWO rendered: each pane's controller clears its own host when it
    mounts (`drawCanvas` does `canvas.innerHTML = ""`), so a control appended
    at construction is gone by the time the pane draws. The first fix
    re-attached at the TOP of the draw and was wiped by the mount that follows
    it. Only a rendered-geometry measurement caught either.

    The suite cannot measure geometry, so it pins the INVARIANT that made the
    bug possible: attachment must be re-asserted after mounting, not once at
    construction."""
    source = SHELL_JS.read_text(encoding="utf-8")
    assert "attachExpandControls" in source, (
        "expand controls are attached once at construction; a pane remount "
        "will silently remove them")
    draw = source[source.index("function drawCanvas()"):]
    body = draw[:draw.index("\n  }\n")]
    clear = body.index('canvas.innerHTML = ""')
    reattach = body.index("attachExpandControls()")
    assert reattach > clear, (
        "attachExpandControls runs BEFORE the pane is cleared/mounted — that "
        "is the placement that was already proven wrong")


def test_the_session_host_cannot_reclaim_the_panel():
    """MEASURED (2026-08-02): the head was 55px and the session host 222px —
    the reference material (session verbs plus the notebook re-sync CLI block)
    owned a quarter of the panel above the working area, which is what the
    operator was actually complaining about. Capped so it scrolls in its own
    box; every command stays selectable, the panes get the height back.
    Hiding it would lose the descriptor the degrade-to-CLI path depends on."""
    styles = STYLES.read_text(encoding="utf-8")
    # A property may be declared in ANY rule that matches the element, so ask
    # the union rather than the first rule found — the same mistake this file
    # already made once with the expand blocks.
    declared = " ".join(
        body for selector, body in _rules(styles)
        if any(part.strip().endswith(".swb-sessionhost")
               for part in selector.split(",")))
    assert declared, ".swb-sessionhost has no rule; the 222px regression is back"
    assert "max-height" in declared, "the session host is uncapped again"
    assert "overflow-y: auto" in declared, (
        "the session host is capped without a scroll — that HIDES the CLI "
        "descriptors rather than thinning them")
