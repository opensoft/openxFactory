"""T086/T087 (010-doxbench-editor-chat, US5): the accessible-surface contract.

Conformance target: **WCAG 2.1 AA** for the doxBench surface (SC-010 as
clarified 2026-07-30), evidenced by the FR-041 mode checklist rather than a
formal external audit. This suite pins the SEMANTIC layer statically — live
regions, dialog semantics, focus discipline markers, responsive/mode CSS —
while the behavioral halves (keyboard order, focus trap and restoration,
guard flows) are exercised by the node harnesses in test_doxbench_view.py,
which this suite deliberately does not duplicate.

Split by ownership, per the wave's fences:
  * doxbench-editor.js assertions pin what US1-US4 already built (green
    tripwires — a regression here is a real accessibility loss);
  * staging-workbench.js / styles.css assertions pin what T092/T093 must add
    (TRUE REDS until realized; hypothesized surfaces follow the wave's
    negotiable-spec rule — adjust THESE tests only if realization forces it,
    and report the delta).
"""

from __future__ import annotations

import re

from conftest import REPO_ROOT

WEB = REPO_ROOT / "scripts" / "ideation_dashboard" / "web"
EDITOR_JS = WEB / "views" / "doxbench-editor.js"
SHELL_JS = WEB / "views" / "staging-workbench.js"
STYLES_CSS = WEB / "styles.css"

WCAG_TARGET = "WCAG 2.1 AA"


def _editor() -> str:
    return EDITOR_JS.read_text(encoding="utf-8")


def _shell() -> str:
    return SHELL_JS.read_text(encoding="utf-8")


def _styles() -> str:
    return STYLES_CSS.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# T086 — semantic regions, accessible names, live status, focus discipline
# ---------------------------------------------------------------------------

def test_editor_status_regions_are_live_regions():
    # The per-buffer status line announces politely; the guard announces
    # assertively. Both exist today (US1/US4) — this is a tripwire.
    editor = _editor()
    assert 'setAttribute("aria-live", "polite")' in editor
    assert 'aria-live", "assertive"' in editor.replace("setAttribute(\"", "")


def test_editor_disabled_controls_carry_the_aria_state_and_a_reason():
    editor = _editor()
    assert 'aria-disabled' in editor
    assert "SAVE_UNAVAILABLE_REASON" in editor  # the stated reason, not bare disablement


def test_editor_busy_state_is_announced_not_only_styled():
    # US4's wired posture: an in-flight Save is announced via aria-busy and a
    # visible "saving" status (pinned behaviorally by T073; the marker is the
    # semantic contract).
    editor = _editor()
    assert 'aria-busy' in editor


def test_shell_names_its_three_regions_semantically():
    # T092 (TRUE RED until realized): docs/lens context, authoring canvas, and
    # the (future) chat rail are labelled semantic regions, so assistive
    # navigation can land on them by name (FR-003/FR-041).
    shell = _shell()
    assert shell.count('setAttribute("role", "region")') >= 2, (
        "shell regions must be labelled")
    assert 'setAttribute("aria-label"' in shell


def test_shell_announces_posture_and_session_status_via_a_live_region():
    # T092 (TRUE RED until realized): posture/session changes are announced,
    # not merely repainted.
    assert 'setAttribute("aria-live"' in _shell()


def test_shell_dialogs_declare_dialog_semantics():
    # T092 (TRUE RED until realized): any shell modal/confirm surface carries
    # dialog semantics; focus containment is asserted behaviorally in the view
    # suite once the surface exists.
    # green-on-arrival: the overlay already declares dialog semantics and a
    # labelled title (aria-labelledby) — pinned here so it cannot regress.
    shell = _shell()
    assert 'setAttribute("role", "dialog")' in shell
    assert 'setAttribute("aria-modal", "true")' in shell


# ---------------------------------------------------------------------------
# T087 — narrow, zoom, reduced motion, forced colors, long text, overflow
# ---------------------------------------------------------------------------

def test_narrow_layout_media_queries_exist():
    # Narrow viewports are already handled for the workbench family — tripwire.
    assert len(re.findall(r"@media \(max-width", _styles())) >= 1


def test_reduced_motion_is_honored():
    # Two prefers-reduced-motion blocks exist today — tripwire (FR-041).
    assert "prefers-reduced-motion" in _styles()


def test_forced_colors_high_contrast_is_handled():
    # T093 (TRUE RED until realized): forced-colors/high-contrast mode must
    # keep status and authority boundaries visible (FR-041, US5 edge case).
    assert "forced-colors" in _styles()


def test_doxbench_canvas_has_narrow_and_zoom_safe_rules():
    # T093 (TRUE RED until realized): the doxBench canvas itself participates
    # in the narrow/zoom story rather than inheriting desktop-only sizing.
    styles = _styles()
    media_blocks = re.findall(r"@media[^{]+\{[\s\S]*?\n\}", styles)
    assert any("doxbench" in block for block in media_blocks), (
        "no @media block addresses the doxbench canvas"
    )


def test_long_text_wraps_instead_of_overflowing():
    # T093 (TRUE RED until realized): unusually long unbroken text in buffers,
    # titles, and status lines wraps or scrolls inside its region (FR-041's
    # long-text/overflow mode; US5 edge case).
    styles = _styles()
    assert re.search(r"(overflow-wrap|word-break)[^;]*;", styles), (
        "no wrapping rule anywhere in the stylesheet"
    )


# ---------------------------------------------------------------------------
# CHK007 (T100 AT measurement 2026-08-02 FAILED it): the WAI-ARIA APG tablist
# pattern — roving tabindex plus Arrow/Home/End selection, with the arrows
# consumed so they no longer scroll the page. The live-DOM proof is the T098
# smoke's step 10c; these are the source and structure pins that keep the
# wiring from silently regressing.
#
# PIN EVOLUTION (add-doxbench-editing-phase-a): the strip these pins measure
# is now the canvas's VIEW tablist (`Editor` / `Preview`). The BUFFER tablist
# they were written for is retired as a control — the context region selects
# the buffer — and the pattern was carried across UNCHANGED precisely because
# it was measured and fixed once already and must not be re-lost in the move.
# The behavioural half (one tabbable tab, and it is the selected one) is
# measured on the live DOM in test_doxbench_view.py.
# ---------------------------------------------------------------------------

def test_the_view_tablist_implements_the_apg_roving_pattern():
    source = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
              / "doxbench-editor.js").read_text(encoding="utf-8")
    # roving tabindex maintained by the one function that owns what is on screen
    assert "tabIndex = selected ? 0 : -1" in source
    # every APG key, including the Up/Down the operator reached for first
    for key in ("ArrowRight", "ArrowLeft", "ArrowUp", "ArrowDown",
                "Home", "End"):
        assert key in source, key
    # the arrows must be consumed, or the page scrolls instead (the observed
    # T100 failure mode)
    assert "ev.preventDefault()" in source
    assert 'tabBtn.addEventListener("keydown"' in source


def test_the_retired_standing_status_stays_in_the_accessibility_tree():
    """Brett's 2026-08-18 annotation round 2: "remove these lines. the UI must be
    intuitive and not rely on this text to inform the user."

    Removing the lines VISUALLY is the instruction; removing them from the
    accessibility tree would be a different and much worse change, because these
    regions are announced, they are where every stated refusal on this canvas
    lands, and they are the per-buffer surface the ratified buffer contract
    requires a partial Save to be readable in. So the class is `sronly`, not
    `hidden`: `display: none` and the `hidden` attribute both take a live region
    out of the tree along with the text."""
    editor = _editor()
    assert "doxbench-sronly" in editor
    assert 'status.setAttribute("aria-live", "polite")' in editor
    styles = _styles()
    # the house sr-only recipe, not display:none and not hidden
    block = styles[styles.index(".doxbench-sronly {"):]
    block = block[:block.index("}")]
    assert "position: absolute" in block
    assert "clip-path: inset(50%)" in block
    assert "display: none" not in block


def test_an_event_refusal_has_a_visible_live_region_of_its_own():
    """The same annotation's other constraint: an EVENT a sighted human must not
    miss cannot hide in an sr-only region. One transient visible line carries
    refusals and non-committed Save verdicts, announced politely like every
    other refusal channel on this surface."""
    editor = _editor()
    assert 'const eventNote = el("div", "doxbench-eventnote")' in editor
    assert 'eventNote.setAttribute("aria-live", "polite")' in editor
    assert "function stateEvent(text)" in editor
    # it clears itself — standing text is what the annotation removed
    assert "eventNote.hidden = true;" in editor
    assert "doxbench-eventnote" in _styles()


def test_the_model_selector_sits_by_send_and_states_why_send_is_unreachable():
    """Brett's 2026-08-18 annotation round 2: "add a model selector down next to
    the send button. make this text the hover text for the send button if no
    model selected."

    Two a11y obligations ride that. The selector must be LABELLED (it is a bare
    `<select>` with no visible label text beside it), and the disabled Send's
    reason must be associated PROGRAMMATICALLY rather than living in a `title`
    a screen reader may never surface — so the sentence stays in the DOM,
    sr-only, as the button's `aria-describedby` target."""
    rail = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
            / "doxbench-chat.js").read_text(encoding="utf-8")
    assert 'selector.setAttribute("aria-label", "approved model")' in rail
    assert 'const sendrow = el("div", "doxchat-sendrow")' in rail
    assert "sendrow.append(selector, sendBtn);" in rail
    assert 'sendBtn.setAttribute("aria-describedby", unavailableNote.id)' in rail
    assert '"doxchat-unavailable doxchat-sronly"' in rail
    # the title carries the same sentence, from the same one selector
    assert "sendBtn.title = sendTitle(inFlight, sendBtn.disabled, modelReason)" in rail
    assert "unavailabilityNote(state)" in rail
    styles = _styles()
    assert ".doxchat-sendrow" in styles
    assert ".doxchat-sronly" in styles


def test_the_working_subject_box_says_what_it_is_and_what_it_does():
    """Brett's 2026-08-21 annotation round 2, on `input.doxchat-subject`: "what
    is the box used for? i do not know how to use it."

    It was a bare text box above the transcript carrying an `aria-label` and
    nothing a sighted human could read — no visible label, no placeholder, and
    (the ratified default from the tile's title being unrealized at the time)
    no seeded value either. So the field answers the question in its own two
    affordances, which is the standard the annotation round before this one set:
    "the UI must be intuitive and not rely on this text to inform the user"
    retired STANDING explanatory lines, and an affordance on the control itself
    is exactly what it left in their place.

    The third part of the answer — the promoted default from the tile's title —
    was realized later, so the box now usually opens carrying a value and the
    placeholder shows where it does not (an emptied box, or a title the
    512-byte bound refuses to seed). Both affordances are unchanged by it, which
    is what the assertions below hold; the seed itself is pinned in
    test_doxbench_chat_view.py.

    The PLACEHOLDER names the field on the house `"<name> — e.g. <value>"` idiom
    the canvas id field already uses (the one prior instance of that exact
    form in these views), and it is an addition,
    never a replacement: a placeholder disappears the moment a human types, so it
    is not an accessible name and the `aria-label` stays. The TITLE carries what
    the value DOES, which is the half the annotation actually asked about."""
    rail = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
            / "doxbench-chat.js").read_text(encoding="utf-8")
    # The accessible name is untouched by the affordance.
    assert 'subjectInput.setAttribute("aria-label", "working subject")' in rail
    assert ('subjectInput.setAttribute("placeholder", SUBJECT_FIELD_PLACEHOLDER)'
            in rail)
    assert "subjectInput.title = SUBJECT_FIELD_TITLE;" in rail
    # It NAMES the field and shows one, rather than describing it abstractly.
    assert "working subject — e.g." in rail
    # …and the title says where the value goes and that it is optional, because
    # "what is this for" is not answered by a name.
    assert "rides every turn" in rail
    assert "may be left empty" in rail


def test_the_canvas_region_is_named_without_a_duplicate_visible_heading():
    """Brett's 2026-08-15 annotation round: "why do we need this line? i do not
    see what it is adding to our UI."

    The answer was: nothing an assistive technology did not already get. A
    `role=region` is announced BY ITS ACCESSIBLE NAME on entry, and the retired
    `h2.doxbench-heading` rendered that same string a second time, visibly,
    costing a row of a narrow panel. Removing it is only safe while the name
    itself survives — so this pins the posture rather than the removal: the
    canvas host is a named region, the name carries the exact `doxBench`
    casing, and the module constructs no heading to restate it.

    The house idiom is the sibling regions': `swb-context` and `doxbench-rail`
    are both `role=region` + `aria-label` with no heading of their own, which is
    why an `aria-label` (rather than a visually-hidden heading) is what this
    canvas keeps — a visually-hidden h2 INSIDE a region that already has a name
    would simply be announced twice."""
    editor = _editor()
    assert 'host.setAttribute("role", "region")' in editor
    assert 'host.setAttribute("aria-label", canvasLabel)' in editor
    assert 'canvasLabel = "doxBench"' in editor
    # no heading element is constructed at all
    assert 'el("h2"' not in editor
    # the retired class name may survive in the prose that RECORDS the removal,
    # never as a string the module hands to the DOM builder
    assert '"doxbench-heading"' not in editor
    # the siblings this idiom is copied from, still named the same way
    shell = _shell()
    assert 'aria-label", "docs and lens context"' in shell
    assert 'aria-label", "doxBench chat rail"' in shell


def test_the_panel_controls_sit_in_the_tab_row_but_outside_the_tablist():
    """Brett's 2026-08-15 annotation round: "place the save and cancel in line
    with the tabs." They are in the tab ROW and outside the TABLIST — a button
    inside `role=tablist` would be announced as a tab and would join the
    roving-tabindex arrow cycle, turning two controls into two phantom views.

    Amendment 1 (2026-08-21) adds Unload as the slot's third occupant. It joins
    the SAME group outside the tablist, for the same reason — the three are one
    slot with two occupancies, never a control that lives somewhere else."""
    editor = _editor()
    assert 'const tabrow = el("div", "doxbench-tabrow")' in editor
    assert 'const actions = el("div", "doxbench-actions")' in editor
    assert "actions.append(cancelBtn, saveBtn, unloadBtn);" in editor
    # the tablist takes the tabs and nothing else
    assert "tabrow.append(viewTablist, actions);" in editor
    assert "viewTablist.appendChild(tabBtn);" in editor


def test_the_slot_swap_reads_saves_own_dirty_derivation_and_not_a_second_one():
    """Amendment 1: "The dirty condition SHALL be read from the SAME per-buffer
    dirty flag Save and Cancel already derive their reachability from, and a
    realization that introduces a second source of dirtiness for the swap MUST be
    rejected."

    This MUST cannot be held behaviorally — a second derivation that happened to
    be byte-identical in behaviour would pass every driven state, and would then
    drift the first time one of the two was touched. It is a STRUCTURAL claim
    about the source, so it is pinned structurally, in this module's established
    idiom: there is exactly ONE `anythingDirty` binding, Save reads it, and the
    swap reads that same name rather than recomputing over the buffers."""
    editor = _editor()
    assert editor.count("const anythingDirty =") == 1, (
        "a second dirtiness derivation is exactly what the requirement rejects")
    assert "saveBtn.disabled = saving || !anythingDirty;" in editor
    assert "const showUnload = !anythingDirty" in editor
    # …and the swap must not re-derive over the buffers on its own.
    swap = editor[editor.index("const showUnload ="):]
    swap = swap[:swap.index("syncUnloadControl();")]
    assert ".dirty" not in swap, (
        "the swap must read the shared derivation, never its own buffer scan")


def test_the_slot_swap_keeps_its_defensive_in_flight_term():
    """`!saving` in the swap condition has NO reachable state of its own today,
    and that is worth saying out loud rather than discovering later.

    `save()` clears `saving` in its `finally` BEFORE `adoptSavedBase` rebases any
    buffer, so a buffer is still dirty for the whole flight and `!anythingDirty`
    alone already holds the pair on screen — which the behavioural probe in
    `test_doxbench_view.py::test_a_save_in_flight_keeps_the_pair_on_screen` pins.
    The term is kept because it states the intent directly and is the guard that
    would matter the moment that ordering changed. A claim with no reachable
    behaviour can only be pinned structurally; pretending otherwise would be a
    behavioural test asserting nothing."""
    editor = _editor()
    assert "const showUnload = !anythingDirty && !saving;" in editor, (
        "the defensive in-flight term must not be dropped as dead code")


def test_the_inert_unload_states_its_reason_as_visible_text():
    """Amendment 1 holds the inert Unload to the SAME standard the requirement
    already sets for an unreachable Save: the reason is visible text beside the
    control, not only a hover title. It matters more here, not less — a disabled
    button cannot take focus, so a `title` alone reaches neither a keyboard nor a
    screen reader."""
    editor = _editor()
    assert 'const unloadNote = el("span", "doxbench-unload-note")' in editor
    assert "statusbar.appendChild(unloadNote);" in editor
    assert 'unloadBtn.setAttribute("aria-describedby", unloadNoteId);' in editor
    # the reason reaches BOTH the note and the title, and the note is shown
    assert "unloadNote.textContent = reason;" in editor
    assert "unloadBtn.title = reason;" in editor
    # …and the class the tripwire checks has a rule
    assert ".doxbench-unload-note" in _styles()


def test_each_buffer_status_names_the_buffer_it_reports():
    """The per-buffer verdict surface had to survive the chrome's retirement
    (partial saves and stated refusals are load-bearing). It moved to a compact
    status row — and each line now NAMES its buffer visibly, because stacked in
    the old chrome the two regions rendered as "no unsaved changesno unsaved
    changes": two identical sentences a reader could not attribute, which is
    exactly the case a PARTIAL save has to report.

    PIN EVOLUTION (add-doxbench-editing-phase-b): the per-buffer parameter is
    spelled `key`, and the refusal sentence reads the LIVE label rather than the
    one captured when the region was built — because a basename collision can
    arrive later, and the second `README.md` to be loaded must lengthen the FIRST
    one's name too. Same strength: every sentence is still built from the buffer's
    own label, and the label is still the only thing that names it."""
    editor = _editor()
    assert 'const prefix = bufferLabel(key) + ": ";' in editor
    assert 'label + ": " + EDITOR_LOADING_REASON' in editor
    assert 'const named = bufferLabel(bufferKey);' in editor
    assert 'named + ": refused -- "' in editor
    # …and the regions are still per buffer, still live, still separately named
    assert 'status.setAttribute("aria-live", "polite")' in editor
    assert 'status.setAttribute("aria-label", label + " buffer status")' in editor


def test_the_retired_buffer_tablist_is_not_rendered_as_a_control():
    """add-doxbench-editing-phase-a task 2.2: two tablists answering "which
    buffer" and "which view" in one panel is how a design conversation stops
    being able to say which one it means. The buffer strip is gone as a
    RENDERED control; its labels survive only as accessible names."""
    source = (REPO_ROOT / "scripts" / "ideation_dashboard" / "web" / "views"
              / "doxbench-editor.js").read_text(encoding="utf-8")
    assert "DOXBENCH_BUFFER_TABS" not in source
    assert "DOXBENCH_VIEW_TABS" in source
    assert "DOXBENCH_BUFFER_LABELS" in source
    # exactly one tablist is constructed on this canvas
    assert source.count('setAttribute("role", "tablist")') == 1
