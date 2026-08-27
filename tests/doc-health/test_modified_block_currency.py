"""The twenty-second family: currency of an active change's MODIFIED blocks.

`add-modified-block-currency-check`, Speckit feature
`019-modified-block-currency-family` (F1). What is under test, and the direction
each group fails in:

1. **THE DERIVATION IS NORMATIVE**, so it is tested as a rule and not as an
   implementation detail. Backticked spans are masked before any sentence
   split; a dated bold note is ONE unit; a fenced block is neither a unit nor a
   marker; and matching is SAME-KIND and EXACT. The two negatives that carry the
   whole family are here: a block unit CONTAINING canon's unit does not carry it
   (issue #351's widening mechanism, which a containment rule reports nothing
   on), and normalization stops at whitespace (so a case or trailing-period
   change is a text change, deliberately unlike `promotion_fidelity.norm`).

2. **THE THREE ARMS ARE THREE FINDING CLASSES, AND THERE ARE FOUR CLASSES.**
   Scenario-title completeness at `warning`, the carriage ledger at `info` and
   at most one finding per requirement, title resolution / ordering at
   `warning` — plus marker defects at `info`, which is a defect in a
   DECLARATION rather than a comparison between documents.

3. **THE MARKER IS RECOGNIZED BY FORM AND NEVER BY PROSE.** The corpus's five
   existing dated notes all record RESTORATIONS, one of them naming seven
   scenario titles in backticks, so a prose rule would read a faithful
   restatement of `doc-health`'s own "Deterministic check families" as
   declaring seven deletions. The form anchor is asserted on this packet's own
   delta prose, which promotes into canon.

4. **THE ADVISORY LAUNCH IS PINNED IN BOTH HALVES**, and the three severities
   are pinned APART: the flip `add-modified-block-currency-check` § 7.2 reserves
   moves the scenario-title arm alone, so one shared constant would drag the
   title-resolution arm to `error` on a flip nobody asked for.

5. **ORDERING IS BY DECLARATION, NEVER BY DATE** (ruled 2026-08-27, "By
   declaration"). One test would pass under date ordering and fails under it, so
   the withdrawn reading cannot creep back.

These tests call `modified_block_currency.fam_modified_block_currency` DIRECTLY
rather than through `families.FAMILIES`. That is deliberate: the registration is
GATED on `add-family-enumeration-check` archiving (plan.md § Sequencing gate),
and routing every behavioural test through the registry would have made the
whole file wait for another change to land.
"""

from __future__ import annotations

from doc_health import INFO, WARNING
from doc_health import modified_block_currency as mbc
from doc_health.promotion_fidelity import norm as norm_title


# ------------------------------------------------- 4. the advisory launch, pinned


def test_the_three_launch_severities_are_named_apart():
    """Three constants, not one — and the names matter as much as the values.

    `_LAUNCH_SEVERITY` is the identifier `promotion_fidelity`,
    `duplicate_packet` and `family_enumeration` all use, and it is the grep that
    ties every reader of a launch decision together. It carries the
    SCENARIO-TITLE arm here, because that is the arm § 7.2's flip moves. The
    other two arms have their own constants so the flip cannot drag them.
    """
    assert mbc._LAUNCH_SEVERITY == WARNING
    assert mbc._RESOLUTION_SEVERITY == WARNING
    assert mbc._LEDGER_SEVERITY == INFO
    # ...and they are genuinely three names, not three aliases of one value:
    # a half-flip has to be able to move one without moving the others.
    assert len({id(n) for n in ("_LAUNCH_SEVERITY", "_RESOLUTION_SEVERITY",
                                "_LEDGER_SEVERITY")}) == 3


def test_the_family_id_is_the_registry_id():
    """The prose name canon will carry is `modified-block currency`, which
    `family_enumeration.normalize_family_name` maps mechanically onto this id.
    If they diverge, the enumeration check needs an ALIASES entry — and
    `test_every_alias_is_load_bearing` exists to make that expensive."""
    assert mbc.FAMILY == "modified-block-currency"

    from doc_health.family_enumeration import normalize_family_name
    assert normalize_family_name("modified-block currency") == mbc.FAMILY


# --------------------------------------------- 1. the derivation: normalization


def test_normalization_collapses_whitespace_and_nothing_else():
    assert mbc.normalize("a  b\n  c ") == "a b c"
    assert mbc.normalize("  ") == ""
    assert mbc.normalize(mbc.normalize("a  b")) == mbc.normalize("a  b")
    # punctuation and backticks survive untouched: the delta's "no
    # normalization beyond it applies" is a closed list of one operation.
    assert mbc.normalize("a `b.c`, d.") == "a `b.c`, d."


def test_unit_normalization_is_not_the_promotion_fidelity_spelling():
    """`dh:84-90` — "matched in full after whitespace normalization ... no
    normalization beyond it applies".

    `promotion_fidelity.norm` collapses whitespace AND CASEFOLDS, which is
    correct for a requirement TITLE (a title's case is a rendering choice no
    reader acts on differently) and forbidden for a UNIT. So the two cannot be
    the same function, and this test exists so a later refactor cannot quietly
    merge them.
    """
    from doc_health import promotion_fidelity as pf

    assert mbc.normalize("A Clause") == "A Clause"
    assert pf.norm("A Clause") == "a clause"
    assert mbc.normalize("A Clause") != pf.norm("A Clause")


def test_case_and_trailing_punctuation_are_significant():
    """Two mutations this pins: `normalize` gaining a `.casefold()`, and
    `normalize` stripping trailing periods.

    `promotion_fidelity.norm`'s own docstring names the wider normalization it
    refuses — "stripping backticks, punctuation, trailing periods" — and gives
    the reason: the codex gap hid inside a `tier-2`-to-`tier 2` normalization.
    """
    canon = [mbc.Unit("body", "The pass SHALL do X.")]
    assert mbc.carried(canon, [mbc.Unit("body", "the pass shall do x.")])
    assert mbc.carried(canon, [mbc.Unit("body", "The pass SHALL do X")])
    assert not mbc.carried(canon, [mbc.Unit("body", "The pass  SHALL do X.")])


# ------------------------------------------------ 1. the derivation: the mask


def test_masking_preserves_length():
    for text in ("see `.openspec.yaml` here", "a ``x`.`y`` b", "no spans",
                 "`", "``unclosed", ""):
        assert len(mbc.mask_code_spans(text)) == len(text), text


def test_a_period_inside_a_backticked_token_never_ends_a_sentence():
    masked = mbc.mask_code_spans("Reads `.openspec.yaml` now.")
    assert "." in masked                       # the sentence's own terminator
    assert masked.count(".") == 1              # the two inside the span are gone


def test_a_longer_fence_masks_its_inner_backticks():
    masked = mbc.mask_code_spans("a ``an `openxFactory` clause`` b")
    assert masked.startswith("a ``")
    assert masked.endswith("`` b")
    assert "openxFactory" not in masked


def test_an_unterminated_backtick_run_masks_nothing():
    text = "unclosed ` tail. more"
    assert mbc.mask_code_spans(text) == text


# --------------------------------------------- 1. the derivation: the sentences


def test_sentences_split_on_a_terminator_followed_by_whitespace():
    assert mbc.split_sentences("One. Two.") == ["One.", "Two."]
    assert mbc.split_sentences("Q? A! Done.") == ["Q?", "A!", "Done."]


def test_the_terminator_stays_with_its_sentence():
    assert mbc.split_sentences("Really?! Yes.") == ["Really?!", "Yes."]


def test_a_period_with_no_following_whitespace_is_not_a_boundary():
    assert mbc.split_sentences("a.b") == ["a.b"]
    assert mbc.split_sentences("version 1.13 ships.") == ["version 1.13 ships."]


def test_boundaries_are_computed_on_the_mask_and_sliced_from_the_original():
    got = mbc.split_sentences("Reads `.openspec.yaml` now. Then stops.")
    assert got == ["Reads `.openspec.yaml` now.", "Then stops."]
    # the emitted text is the ORIGINAL, never the mask: a reader of a finding
    # must never see filler characters.
    assert "\x00" not in "".join(got)


def test_a_paragraph_with_no_terminator_is_one_sentence():
    assert mbc.split_sentences("No terminator") == ["No terminator"]


# ---------------------------------------------------- 3. the marker: code spans


def _spans(text):
    return [c for _s, _e, c in mbc.extract_code_spans(text)]


def test_code_spans_extract_in_document_order():
    assert _spans("`a`; `b`") == ["a", "b"]


def test_a_unit_containing_backticks_is_extracted_whole_under_a_longer_fence():
    """`dh:135-142`. Roughly a third of this corpus's body units and a sixth of
    its bullets contain a backtick, because they cite things like
    `openxFactory`. The mutation this kills is a non-greedy `` `([^`]*)` ``,
    which truncates at the first inner backtick and makes the marker name a
    FRAGMENT that is not a unit at all."""
    text = "``an adapter reaching `openxFactory` SHALL use the broker lane``"
    assert _spans(text) == ["an adapter reaching `openxFactory` SHALL use the "
                            "broker lane"]


def test_one_space_each_side_is_stripped_per_commonmark():
    """CommonMark's own rule, and the double fence is how a span carries a
    backtick at either end (CommonMark example 328).

    The first assertion is the one that corrects a plausible misreading: with
    SINGLE fences, `` ` `x` ` `` is not one span around `` `x` `` — the first
    backtick string closes at the next one of equal length, giving two spans
    each holding a space. That is the rule this parser follows, and reading it
    the other way is how a marker comes to name a fragment.
    """
    assert _spans("`` `x` ``") == ["`x`"]
    assert _spans("` `x` `") == [" ", " "]
    assert _spans("` x `") == ["x"]
    assert _spans("` x`") == [" x"]


def test_an_unterminated_run_yields_no_span():
    assert _spans("`unclosed") == []


# --------------------------------------------------- 3. the marker: fenced code


def test_fenced_block_lines_are_identified():
    lines = ["prose", "```", "**Removed from canon by add-x (2026-08-27):** `u`",
             "```", "more prose"]
    assert mbc.fenced_regions(lines) == {1, 2, 3}


def test_an_unclosed_fence_runs_to_the_end_of_the_block():
    lines = ["prose", "````text", "anything", "at all"]
    assert mbc.fenced_regions(lines) == {1, 2, 3}


def test_a_shorter_inner_run_does_not_close_a_longer_fence():
    lines = ["````", "```", "still inside", "````", "out"]
    assert mbc.fenced_regions(lines) == {0, 1, 2, 3}


# ------------------------------------------------------- 3. the marker: the form


REMOVED = ("**Removed from canon by add-example-change (2026-08-27):** "
           "`Gate verbs hide on a composed view`; ``an adapter that reaches a "
           "hosted provider SHALL obtain its credential through the "
           "`openxFactory` broker lane`` — the affordance is now tile-bound")
MERGED = ("**Merged into `Tile-bound gate verbs hide on a composed view` by "
          "add-example-change (2026-08-27):** "
          "`Gate verbs hide on a composed view`")


def test_both_marker_forms_parse():
    m = mbc.parse_marker(REMOVED)
    assert m is not None and m.form == "removed"
    assert m.change_id == "add-example-change" and m.date == "2026-08-27"
    assert m.names == ["Gate verbs hide on a composed view",
                       "an adapter that reaches a hosted provider SHALL obtain "
                       "its credential through the `openxFactory` broker lane"]
    assert m.reason == "the affordance is now tile-bound"
    assert m.destination is None

    m = mbc.parse_marker(MERGED)
    assert m is not None and m.form == "merged"
    assert m.destination == "Tile-bound gate verbs hide on a composed view"
    assert m.names == ["Gate verbs hide on a composed view"]


def test_the_merge_destination_is_not_a_named_unit():
    """`dh:148-151` — "reading it as a named unit would make every valid merge
    marker report itself under the rule below"."""
    m = mbc.parse_marker(MERGED)
    assert m.destination not in m.names


def test_a_marker_wrapped_across_lines_is_one_marker():
    wrapped = ("**Removed from canon by add-example-change\n(2026-08-27):**\n"
               "`Gate verbs hide on a composed view`\n— it moved")
    m = mbc.parse_marker(wrapped)
    assert m is not None
    assert m.names == ["Gate verbs hide on a composed view"]
    assert m.reason == "it moved"


def test_a_marker_with_no_reason_is_still_a_marker():
    """The delta's OWN written-out `Merged into` example carries no reason
    (`dh:189`), and form is anchored on the prefix alone (`dh:125-129`)."""
    m = mbc.parse_marker(MERGED)
    assert m is not None and m.reason is None


def test_a_quoted_marker_template_is_not_a_marker():
    """THE ANCHOR IS LOAD-BEARING (`dh:125-133`). This requirement's own text and
    `document-lifecycle`'s both set the two templates out in prose that PROMOTES
    INTO CANON, and a looser test would read them as markers and exempt them
    from carriage — "the check quietly declining to check the paragraphs that
    define it"."""
    assert mbc.parse_marker(
        "**Removed from canon by <change-id> (<YYYY-MM-DD>):** followed by the "
        "deleted units, then ` — <reason>`.") is None
    assert mbc.parse_marker(
        "**Merged into `<destination scenario title>` by <change-id> "
        "(<YYYY-MM-DD>):** followed by the superseded scenario titles.") is None


def test_a_non_iso_date_is_not_a_marker():
    assert mbc.parse_marker(
        "**Removed from canon by add-x (27-08-2026):** `A`") is None


def test_a_missing_closing_colon_is_not_a_marker():
    assert mbc.parse_marker(
        "**Removed from canon by add-x (2026-08-27)** `A`") is None


def test_a_marker_needs_its_bold_run():
    assert mbc.parse_marker(
        "Removed from canon by add-x (2026-08-27): `A`") is None


def test_a_dated_bold_note_that_is_not_a_reserved_form_parses_as_no_marker():
    """The guard on the finding that canon's own restoration notes must NEVER be
    read as declarations of deletion. `doc-health`'s "Deterministic check
    families" carries one naming SEVEN of its eight scenario titles in backticks
    — as the seven that were RESTORED."""
    assert mbc.parse_marker(
        "**CORRECTED 2026-08-25 ON BRETT'S RULING — this block is now "
        "SCENARIO-COMPLETE.** The seven are restored below: `Drift checks "
        "fire`, `Catalog conformance checks fire`.") is None


def test_the_deltas_own_fenced_marker_examples_never_reach_the_parser():
    """RULED 2026-08-27 (N7). The two example lines at
    `add-modified-block-currency-check/specs/doc-health/spec.md`:187-190 are
    COMPLETE markers — real change id, real ISO date, closing colon — and they
    live inside a fenced code block that promotes into canon with the
    requirement.

    Two halves, and both matter. `parse_marker` is FORM-BLIND: handed the line
    in isolation it parses, and it should, because the line IS of marker form.
    What protects canon is that `fenced_regions` never offers it.
    """
    assert mbc.parse_marker(REMOVED) is not None      # form-blind, by design

    lines = ["Written out, the two forms are exactly:", "", "```",
             REMOVED, MERGED, "```", ""]
    fenced = mbc.fenced_regions(lines)
    assert {3, 4} <= fenced, "the two example lines must be inside the fence"


# ----------------------------------------------- 1. the derivation: dated notes


def test_a_dated_bold_note_is_recognized_by_form():
    assert mbc.is_dated_bold_note(
        "**CORRECTED 2026-08-25 ON BRETT'S RULING — this block is now "
        "SCENARIO-COMPLETE.** As first written it restated only ONE scenario.")


def test_an_undated_bold_lead_is_not_a_note():
    assert not mbc.is_dated_bold_note(
        "**Emphasis** leading an otherwise ordinary paragraph. Two sentences.")
    assert not mbc.is_dated_bold_note(
        "Plain prose mentioning 2026-08-25 with no bold run at all.")


def test_the_real_notes_this_corpus_carries_are_each_one_unit():
    """O6's predicate, MEASURED against the corpus rather than asserted.

    `openspec/specs/doc-health/spec.md` carries three dated bold notes today, at
    least one of them several sentences long. Each must derive as ONE undivided
    unit: a note is a single editorial statement whose sentences mean nothing
    apart, and reporting its third sentence as a lost obligation would be
    reporting noise about noise.

    THE PROBE MATTERS AND THE FIRST CUT OF IT WAS WRONG. Scanning canon
    line-by-line finds only ONE of the three, because two of them WRAP and a
    half-line carries no closing `**`. `derive_units` joins a paragraph before
    classifying it, so the real pipeline sees all three — and a test that probed
    differently from the pipeline would have "proven" the predicate on a third
    of its population. So this reads the requirement's own lines and runs the
    derivation, which is the only path that ships.
    """
    from pathlib import Path

    from conftest import REPO_ROOT

    lines = Path(REPO_ROOT, "openspec/specs/doc-health/spec.md").read_text(
        encoding="utf-8").splitlines()
    start = lines.index("### Requirement: Deterministic check families")
    end = next(i for i in range(start + 1, len(lines))
               if lines[i].startswith("### Requirement: "))

    units, markers = mbc.derive_units(lines[start + 1:end])
    notes = [u for u in units if mbc.is_dated_bold_note(u.text)]
    assert len(notes) == 2, [u.text[:70] for u in notes]

    # ...each one WHOLE, not split at its internal sentence boundaries, and
    # none of them read as a marker — every dated note in this corpus records a
    # RESTORATION, and one of them names seven scenario titles in backticks as
    # the seven that were restored.
    assert markers == [], [m.paragraph[:70] for m in markers]
    for note in notes:
        assert note.kind == mbc.BODY
        assert len(mbc.split_sentences(note.text)) > 1, (
            "a note with only one sentence proves nothing about undividedness")


# ------------------------------------------------ 1. the derivation: the units


BLOCK = [
    "The pass SHALL do X. It reads `.openspec.yaml` first.",
    "",
    "- a body bullet obligation",
    "",
    "**CORRECTED 2026-08-25 — one note. Two sentences.**",
    "",
    "#### Scenario: A run executes",
    "- **WHEN** a run executes",
    "- **THEN** it MUST do X",
]


def _units(lines=None):
    return mbc.derive_units(lines if lines is not None else BLOCK)[0]


def test_body_and_scenario_regions_split_at_the_first_scenario_heading():
    kinds = [(u.kind, u.text) for u in _units()]
    assert kinds == [
        (mbc.BODY, "The pass SHALL do X."),
        (mbc.BODY, "It reads `.openspec.yaml` first."),
        (mbc.BODY, "a body bullet obligation"),
        (mbc.BODY, "**CORRECTED 2026-08-25 — one note. Two sentences.**"),
        (mbc.SCENARIO_TITLE, "A run executes"),
        (mbc.SCENARIO_BULLET, "**WHEN** a run executes"),
        (mbc.SCENARIO_BULLET, "**THEN** it MUST do X"),
    ]


def test_a_body_bullet_is_one_unit_with_its_marker_stripped():
    texts = [u.text for u in _units()]
    assert "a body bullet obligation" in texts
    assert not any(t.startswith("-") for t in texts)


def test_a_dated_note_is_one_unit_not_three():
    notes = [u for u in _units() if u.text.startswith("**CORRECTED")]
    assert len(notes) == 1
    assert "Two sentences." in notes[0].text


def test_a_scenario_bullet_records_its_owning_scenario():
    bullets = [u for u in _units() if u.kind == mbc.SCENARIO_BULLET]
    assert {u.scenario for u in bullets} == {"A run executes"}
    # ...and the owning scenario is NOT part of identity: bullets compare across
    # the whole block, so a bullet moved under another heading is carried.
    moved = mbc.Unit(mbc.SCENARIO_BULLET, "**WHEN** a run executes", "Elsewhere")
    assert mbc.carried(bullets[:1], [moved]) == []


def test_prose_under_a_scenario_heading_is_a_body_unit():
    """Decision O9, flagged for veto. The delta defines a scenario region's
    HEADING and its BULLETS and is silent on a non-bullet paragraph inside one.
    Deriving it as a body unit keeps it under both carriage arms; dropping it
    would let a block move an obligation into scenario prose and have neither
    arm see it. Population in this corpus: 2."""
    units = _units(["#### Scenario: A run executes",
                    "Prose smuggled under a heading.",
                    "- **WHEN** it runs"])
    assert [(u.kind, u.text) for u in units] == [
        (mbc.SCENARIO_TITLE, "A run executes"),
        (mbc.BODY, "Prose smuggled under a heading."),
        (mbc.SCENARIO_BULLET, "**WHEN** it runs"),
    ]


def test_a_marker_paragraph_yields_no_unit_in_either_document():
    """`dh:109-110` and `dh:179-183`: a marker is a unit in NEITHER direction.
    If it were, a promoted marker would be text every later block had to restate
    forever, and the durable record of a deletion is the archived delta."""
    units, markers = mbc.derive_units(["Body text.", "", REMOVED])
    assert [u.text for u in units] == ["Body text."]
    assert len(markers) == 1 and markers[0].form == "removed"


def test_fenced_block_lines_are_neither_units_nor_markers():
    """N7, now through the derivation: the delta's own example lines, fenced."""
    units, markers = mbc.derive_units([
        "Written out, the two forms are exactly:", "", "```", REMOVED, MERGED,
        "```"])
    assert [u.text for u in units] == ["Written out, the two forms are exactly:"]
    assert markers == []


# ------------------------------------------- 1. the derivation: what carries what


def test_a_canon_unit_is_carried_only_by_a_unit_of_the_same_kind():
    """Without the kind, a block could satisfy the ledger by quoting canon's
    obligations in PROSE while deleting the scenarios that made them testable."""
    canon = [mbc.Unit(mbc.SCENARIO_BULLET, "**THEN** it MUST do X", "S")]
    same_text_wrong_kind = [mbc.Unit(mbc.BODY, "**THEN** it MUST do X")]
    assert mbc.carried(canon, same_text_wrong_kind) == canon
    assert mbc.carried(canon, canon) == []


def test_a_block_unit_containing_canon_s_unit_does_not_carry_it():
    """ISSUE #351'S WIDENING MECHANISM, and the case a containment rule loses.

    Canon's bullet is a SUBSTRING of the widened replacement, so a rule that
    asked "does the unit appear in the block" reports nothing here — on the very
    defect PR #358 had to repair by hand. `dh:91-97` forbids containment for
    exactly this reason.
    """
    canon = [mbc.Unit(mbc.SCENARIO_BULLET,
                      "**THEN** the selector MUST show exactly the available "
                      "catalog entries and their data-handling badges", "S")]
    widened = [mbc.Unit(mbc.SCENARIO_BULLET,
                        "**THEN** the selector MUST show exactly the available "
                        "catalog entries and their data-handling badges and "
                        "their provider lanes", "S")]
    assert mbc.carried(canon, widened) == canon


def test_a_rewrapped_paragraph_is_carried():
    """The case LINE-level matching fails. PR #358's manual verification worked
    only because that repair copied canon verbatim, preserving its wrapping — and
    a rule that only works when the author preserved wrapping is not a rule."""
    canon = mbc.derive_units(["A clause that wraps across two lines in canon."])[0]
    block = mbc.derive_units(["A clause that wraps",
                              "across two lines in canon."])[0]
    assert mbc.carried(canon, block) == []


# ------------------------------------------------------ 2. the document readers


FIXTURE_REPO = "alphaFactory"
CAP = "ideation-dashboard"
LOSSY = ("openspec/changes/add-lossy-block/specs/ideation-dashboard/spec.md")
REQ = "Composed views are read-only with a repository jump"


def _root():
    from conftest import FIXTURES
    return FIXTURES / "modified-block-currency" / FIXTURE_REPO


def test_active_deltas_are_discovered_and_the_archive_is_excluded():
    blocks = mbc.active_blocks(_root())
    assert {b.change for b in blocks} == {"add-lossy-block", "add-draft-block"}
    assert not [b for b in blocks if "archive" in b.delta_rel]
    assert [b.delta_rel for b in blocks if b.change == "add-lossy-block"] == [LOSSY]


def test_a_draft_change_is_read_exactly_like_a_ratified_one():
    """`dh:30-36`. Reading scope is deliberately WIDER than the two-writers
    obligation, which `release-realization` scopes to an active RATIFIED change
    and which this family does not widen."""
    blocks = {b.change: b for b in mbc.active_blocks(_root())}
    assert blocks["add-draft-block"].standing == "draft"
    assert blocks["add-lossy-block"].standing == "ratified"
    assert blocks["add-draft-block"].units, "a draft block is still derived"


def test_the_promoted_reader_returns_bodies_and_bullets_not_just_titles():
    """`promotion_fidelity.parse_promoted` returns `{requirement: [titles]}` and
    cannot serve this family: the carriage ledger needs BODIES and BULLETS."""
    canon = mbc.promoted(_root(), CAP)
    from doc_health.promotion_fidelity import norm

    req = canon[norm(REQ)]
    kinds = {u.kind for u in req.units}
    assert kinds == {mbc.BODY, mbc.SCENARIO_TITLE, mbc.SCENARIO_BULLET}
    assert len([u for u in req.units if u.kind == mbc.SCENARIO_TITLE]) == 8
    assert req.spec_rel == f"openspec/specs/{CAP}/spec.md"


def test_the_promoted_reader_stops_at_the_next_section():
    """N10's invariant. A promoted spec carries `## ` sections after its
    requirements; without the stop, the LAST requirement swallows them as body
    units and every block modifying it is reported as failing to carry text that
    was never part of it."""
    canon = mbc.promoted(_root(), CAP)
    for req in canon.values():
        assert not [u for u in req.units
                    if u.text.startswith("#") or "Specification" in u.text]


def test_the_delta_side_reads_through_promotion_fidelity_parse_delta():
    """One grammar for these headings, not two. `promotion_fidelity`'s docstring
    names the lesson `align-status-reader-to-real-lines` paid for."""
    import inspect

    src = inspect.getsource(mbc.active_blocks)
    assert "parse_delta" in src
    assert "_REQUIREMENT" not in src, "no second heading grammar in this module"


def test_a_live_main_basis_request_changes_nothing():
    """FR-002's second half, BEHAVIOURALLY (N3): the checked-out tree is this
    family's only basis, so a `promotion_fidelity_basis` on the context must not
    reach it. `dh:206-210` reserves that basis for promotion fidelity and calls
    it "actively wrong here" — an active change lives on a branch, so a family
    reading `main` would measure a delta `main` does not carry against canon the
    branch may have moved."""
    from conftest import FakeGit, make_ctx

    plain = make_ctx("modified-block-currency")
    asked = make_ctx("modified-block-currency",
                     git=FakeGit(refs={(FIXTURE_REPO, "origin/main"): "d" * 40},
                                 ref_trees={(FIXTURE_REPO, "origin/main"): {
                                     f"openspec/specs/{CAP}/spec.md":
                                         "# totally different canon\n"}}))
    asked.promotion_fidelity_basis = "live-main"

    assert ([f.rule for f in mbc.fam_modified_block_currency(plain)]
            == [f.rule for f in mbc.fam_modified_block_currency(asked)])


def test_the_family_publishes_no_basis_note():
    """A `FAMILY_NOTES` entry exists to say WHICH TREE produced a family's
    findings, and it exists for promotion fidelity because the nightly varies
    that family's basis by ruling. A family with one basis needs no entry, and
    an entry that said nothing would teach a reader to skip the ones that do."""
    from doc_health.families import FAMILY_NOTES

    assert mbc.FAMILY not in FAMILY_NOTES


# ------------------------------------ 2. arm 1: scenario-title completeness (US1)


def _run(ctx=None):
    from conftest import make_ctx
    return mbc.fam_modified_block_currency(
        ctx if ctx is not None else make_ctx("modified-block-currency"))


def _titles(findings):
    return [f for f in findings if "scenario" in f.rule and "omits" in f.rule]


def test_a_block_that_drops_scenarios_names_every_one_of_them():
    """The #329 SHAPE at F1 grain: a block restating 1 of a promoted
    requirement's 8 scenarios. Asserted on the NAMED titles, never on a count —
    "some finding fired on that path" would pass over a build that reported the
    wrong seven."""
    hits = _titles(_run())
    assert len(hits) == 1, [f.rule for f in hits]
    rule = hits[0].rule
    for title in ("The menu offers a routing rule",
                  "A fourth provider verb is proposed",
                  "The jump names its repository",
                  "A read-only view refuses an edit",
                  "The badge set is complete",
                  "A stale composed view refreshes",
                  "An empty composed view says so"):
        assert title in rule, title
    # ...and the one it DID restate is not named as missing.
    assert "'Gate verbs hide on a composed view'" not in rule
    # ...and the promoted spec it was read from is named, because that is what a
    # reader has to open next.
    assert f"openspec/specs/{CAP}/spec.md" in rule


def test_the_finding_lands_on_the_active_delta_s_own_path():
    """`dh:6-10`: reported against the active delta's own path, WHILE THE CHANGE
    CAN STILL BE EDITED. That is the whole difference from promotion fidelity,
    which reports against archived paths where the remedy no longer lives."""
    assert {f.path for f in _titles(_run())} == {LOSSY}
    assert {f.family for f in _run()} == {mbc.FAMILY}
    assert {f.repo for f in _run()} == {FIXTURE_REPO}


def test_the_scenario_arm_is_a_warning():
    assert {f.severity for f in _titles(_run())} == {WARNING}


def test_a_scenario_complete_block_that_rewraps_every_paragraph_is_quiet():
    """Mutation: `normalize` becomes the identity. Then a re-wrapped restatement
    reports every paragraph it carries, and the family is unusable."""
    canon = mbc.promoted(_root(), CAP)[norm_title(REQ)]
    rewrapped = []
    for u in canon.units:
        if u.kind == mbc.SCENARIO_TITLE:
            rewrapped.append(f"#### Scenario: {u.text}")
        elif u.kind == mbc.SCENARIO_BULLET:
            rewrapped.append(f"- {u.text}")
        else:
            # A real re-wrap: ONE paragraph broken across two lines at a word
            # boundary, with no blank line between them. (The first cut of this
            # helper inserted blank lines and so produced TWO paragraphs, which
            # is a different edit entirely — and the test failed, correctly.)
            words = u.text.split(" ")
            cut = max(1, len(words) // 2)
            rewrapped += ["", " ".join(words[:cut]), " ".join(words[cut:]), ""]
    units, _ = mbc.derive_units(rewrapped)
    assert mbc.carried(canon.units, units) == []


def test_a_run_configured_fail_on_error_is_unaffected():
    """N4: assert the finding list is NON-EMPTY FIRST. On an empty list the
    severity assertion is vacuous — and an empty list is exactly what a broken
    discovery returns, so the vacuous version would pass over the one build that
    matters."""
    findings = _run()
    assert findings, "a vacuous pass is not a pass"
    assert {f.severity for f in findings} <= {WARNING, INFO}
    assert not [f for f in findings if f.severity in ("critical", "error")]


def test_the_file_level_scenario_count_is_not_what_the_family_reads():
    """WHY COUNTING CANNOT SEE THIS CLASS. The lossy delta's own ADDED
    requirement brings SEVEN scenarios while its MODIFIED block drops seven, so
    the FILE-LEVEL count is flat — 8 in canon, 8 in the delta — and the family
    fires anyway, because it accounts PER REQUIREMENT."""
    canon_text = (_root() / f"openspec/specs/{CAP}/spec.md").read_text()
    delta_text = (_root() / LOSSY).read_text()
    assert (canon_text.count("#### Scenario:")
            == delta_text.count("#### Scenario:") == 8)
    assert _titles(_run()), "the flat count must not buy silence"


# --------------------------------------------------- 2. arm 2: the ledger (US2)


def _ledger(findings):
    return [f for f in findings if "does not carry" in f.rule]


def test_uncarried_body_units_and_bullets_are_one_info_finding_per_requirement():
    """`dh:56-57`: "It SHALL emit at most one finding per requirement, listing
    the units, rather than one finding per unit." Ten standing warnings on a
    clean repository is how a report stops being read; ten standing ROWS inside
    one finding is a list somebody reads once."""
    hits = _ledger(_run())
    assert len(hits) == 1, [f.rule[:80] for f in hits]
    assert hits[0].severity == INFO
    assert hits[0].path == LOSSY

    rule = hits[0].rule
    # the body sentence the block WIDENED (its replacement contains canon's
    # text as a prefix, which is why containment cannot be carriage)
    assert "The selector MUST show exactly the available catalog entries" in rule
    # the body bullet the block dropped entirely
    assert "every loaded editor MUST remain usable" in rule
    # the dated note the block dropped — ONE row, not one per sentence
    assert rule.count("CORRECTED 2026-08-25") == 1
    # the scenario bullet dropped from the ONE scenario the block did restate
    assert "the selector MUST stay read-only" in rule


def test_the_ledger_finding_does_not_assert_intent():
    """`dh:252-255`: the finding "MUST NOT assert that the divergence is
    unintended, the arm having no means to distinguish a rewording from stale
    text". The hedge is IN THE FINDING, not only in the docs, because the
    finding is what a reader sees."""
    rule = _ledger(_run())[0].rule
    assert "CANNOT distinguish" in rule
    assert "rewording" in rule


def test_a_bullet_carried_under_a_different_scenario_is_not_reported():
    """`dh:47-53`. Bullets compare against ALL bullets of ALL scenarios in the
    block, never scenario by scenario — otherwise a block could retitle a
    scenario, declare the retitle, and drop the bullets underneath it
    unreported. The chosen consequence, stated in the delta rather than
    discovered: a bullet moved verbatim under a DIFFERENT scenario IS carried,
    and the arm says nothing about it. The fixture's block carries canon's
    `**THEN** it MUST name the owning repository` under another heading."""
    rule = _ledger(_run())[0].rule
    assert "it MUST name the owning repository" not in rule


def test_no_reported_unit_is_a_backtick_fragment():
    """THE TOKENIZATION INVARIANT, end to end through the family rather than
    through `derive_units` alone, so a wiring regression cannot hide behind a
    green unit test. A unit whose backticks are unbalanced is a FRAGMENT — the
    signature of a sentence split that fell inside a code span."""
    for f in _run():
        for chunk in f.rule.split("'"):
            assert chunk.count("`") % 2 == 0 or "``" in chunk, chunk[:80]


def test_the_tokenized_sentences_are_carried_and_not_reported():
    """Canon and the block both carry `` The jump SHALL read `.openspec.yaml`
    for its repository name. `` verbatim. Masked, that is ONE unit on each side
    and it matches. Unmasked, it is two fragments on each side — which would
    ALSO match, so this pairs with the unit-level masking tests rather than
    replacing them: what it proves is that the family's wiring passes the
    masking path at all, and that neither half is reported."""
    rule = _ledger(_run())[0].rule
    assert ".openspec.yaml" not in rule
    assert "It SHALL NOT guess." not in rule


# --------------------------------------------- 3. the marker, end to end (US3)


MARKER_DELTA = "openspec/changes/add-marker-cases/specs/marker-cases/spec.md"


def _markers_run():
    from conftest import make_ctx
    return mbc.fam_modified_block_currency(
        make_ctx("modified-block-currency-markers"))


def _for(requirement, findings=None):
    return [f for f in (findings if findings is not None else _markers_run())
            if repr(requirement) in f.rule]


def test_a_marker_suppresses_exactly_the_units_it_names():
    """`dh:153-156`, and the "exactly" is the whole assertion: the marker names
    two of the three body units the block dropped, so the THIRD is still
    reported."""
    hits = _ledger(_for("Suppression names exactly two of three"))
    assert len(hits) == 1, [f.rule[:90] for f in hits]
    rule = hits[0].rule
    assert "Body three." in rule
    assert "Body one." not in rule
    assert "Body two." not in rule


def test_a_marker_naming_a_carried_unit_emits_one_info_finding():
    """THE FOURTH FINDING CLASS (ruled 2026-08-27). "A marker naming a unit the
    block still carries declares nothing and SHALL itself be reported, because a
    declaration that does not describe the block is a declaration no reader can
    rely on."

    The first cut of this plan gave that rule a PRODUCER and no emitter, which
    is how a `SHALL` ends up realized in a docstring.
    """
    hits = [f for f in _for("A marker naming a carried unit")
            if "declaration" in f.rule]
    assert len(hits) == 1, [f.rule[:90] for f in hits]
    finding = hits[0]
    assert finding.severity == INFO          # info, never error
    assert finding.path == MARKER_DELTA
    assert "add-marker-cases" in finding.rule and "2026-08-27" in finding.rule
    assert "Kept one." in finding.rule
    # ...and it does NOT inherit the ledger's hedge: a marker naming a carried
    # unit is wrong with certainty, so "cannot distinguish a rewording from
    # stale text" would be false of it.
    assert "CANNOT distinguish" not in finding.rule
    # nothing was suppressed by that name, and the block carries both units, so
    # the ledger has nothing to say about this requirement
    assert _ledger(_for("A marker naming a carried unit")) == []


def test_a_genuinely_removed_scenario_title_carries_its_bullets():
    """`dh:158-165`. The block names the scenario removed and adds NO scenario
    title canon does not carry, so the three bullets that scenario carried go
    with it. "Declaring a scenario genuinely gone and then reporting its bullets
    forever would make the declaration useless for the act it exists to
    declare"."""
    assert _for("A genuine removal carries its bullets") == []


def test_a_surviving_bullet_of_a_removed_scenario_is_carried():
    """The other half of the same rule: a bullet of the removed scenario that
    DOES appear elsewhere in the block is carried, and nothing is reported about
    it either way."""
    assert _for("A survivor of a removed scenario is carried") == []


def test_a_removal_marker_plus_a_replacement_scenario_still_reports_the_bullets():
    """`dh:167-177` — THE COMBINATION CASE, and the one place the two marker
    rules could contradict each other.

    A `Removed from canon` marker names the old title AND the block adds a
    replacement scenario carrying one of its three bullets. That shape is a
    RETITLE whatever the marker calls it, so the extension does NOT apply and the
    two uncarried bullets are reported. Suppressing them would let a retitle
    relabelled as a removal drop obligations with nothing reported — which is
    exactly the defect the bullet arm exists to close.

    This test FAILS under any scenario-paired bullet comparison, and it is why
    the delta compares bullets across the whole block.
    """
    hits = _ledger(_for("A retitle relabelled as a removal"))
    assert len(hits) == 1, [f.rule[:90] for f in hits]
    rule = hits[0].rule
    assert "it MUST do a second thing" in rule
    assert "it MUST do a third thing" in rule
    # the bullet the replacement DOES carry is not reported
    assert rule.count("it MUST do one thing") == 0
    # and the title itself is declared, so arm 1 stays quiet
    assert _titles(_for("A retitle relabelled as a removal")) == []


def test_the_merge_destination_is_never_read_as_a_named_unit_end_to_end():
    """`dh:148-151`: "reading it as a named unit would make every valid merge
    marker report itself". The destination is PRESENT in the block by
    construction, so if it were a named unit this would emit a marker defect on
    every legitimate merge."""
    assert _for("A merge destination is present") == []


def test_a_promoted_marker_is_not_a_carriage_unit():
    """`dh:179-183`. Canon carries a marker paragraph from an older change; the
    block does not restate it, and must not have to. "A marker promotes into
    canon with the requirement, and if it were a unit every later block would
    have to restate every marker any predecessor ever wrote, forever"."""
    assert _for("A promoted marker is not a carriage unit") == []


def test_a_prose_dated_note_declares_nothing():
    """THE GUARD ON THE FINDING THAT MADE THE MARKER NEW. Canon carries a dated
    bold note naming `Dropped body.` in backticks — as the clause that was
    RESTORED, which is what every such note in this corpus records. It declares
    NOTHING, so the dropped clause is still reported, and the note itself is a
    body unit the block did not carry."""
    hits = _ledger(_for("A prose dated note declares nothing"))
    assert len(hits) == 1, [f.rule[:90] for f in hits]
    rule = hits[0].rule
    assert "Dropped body." in rule, "a prose note must suppress nothing"
    assert "CORRECTED 2026-08-25" in rule
