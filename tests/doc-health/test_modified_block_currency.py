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

2. **THE THREE ARMS ARE THREE FINDING CLASSES, AND THERE ARE FIVE CLASSES.**
   Scenario-title completeness at `warning`, the carriage ledger at `info` and
   at most one finding per requirement, title resolution / ordering at
   `warning` — plus marker defects at `info`, which is a defect in a
   DECLARATION rather than a comparison between documents, and unplaced-finding
   drift at `warning`, which is a defect in the family's own CLASS MAP
   (`add-unclassified-finding-class`).

3. **THE MARKER IS RECOGNIZED BY FORM AND NEVER BY PROSE.** The corpus's five
   existing dated notes all record RESTORATIONS, one of them naming seven
   scenario titles in backticks, so a prose rule would read a faithful
   restatement of `doc-health`'s own "Deterministic check families" as
   declaring seven deletions. The form anchor is asserted on this packet's own
   delta prose, which promotes into canon.

4. **THE ADVISORY LAUNCH IS PINNED IN BOTH HALVES**, and the four severities
   are pinned APART: the flip `add-modified-block-currency-check` § 7.2 reserves
   moves the scenario-title arm alone, so one shared constant would drag the
   title-resolution arm to `error` on a flip nobody asked for — and would drag
   the fifth class with it invisibly, which is what the simulated-flip test
   below exists to make falsifiable.

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

from doc_health import ERROR, INFO, WARNING
from doc_health import modified_block_currency as mbc
from doc_health.promotion_fidelity import norm as norm_title


# ------------------------------------------------- 4. the advisory launch, pinned


def test_the_three_launch_severities_are_named_apart():
    """Three constants, not one — and the names matter as much as the values.

    `_LAUNCH_SEVERITY` is the identifier `promotion_fidelity`,
    `duplicate_packet` and `family_enumeration` all use, and it is the grep that
    ties every reader of a launch decision together. It carries the
    SCENARIO-TITLE arm here, because that is the arm § 7.2's flip moves — and
    which it MOVED, on 2026-08-31 (issue #357), once the measured population
    read zero. The other two arms have their own constants precisely so the
    flip could not drag them, and O8 is why they still read as launched.
    """
    assert mbc._LAUNCH_SEVERITY == ERROR
    assert mbc._RESOLUTION_SEVERITY == WARNING
    assert mbc._LEDGER_SEVERITY == INFO
    # ...and they are three SEPARATELY ASSIGNABLE module attributes, which is
    # what makes a one-arm flip possible. Asserted by moving one and checking the
    # others do not follow — the previous version of this line compared the ids
    # of three string LITERALS, which is true of any three distinct strings and
    # therefore proved nothing.
    names = ("_LAUNCH_SEVERITY", "_RESOLUTION_SEVERITY", "_LEDGER_SEVERITY")
    for name in names:
        before = {n: getattr(mbc, n) for n in names}
        try:
            setattr(mbc, name, "sentinel")
            after = {n: getattr(mbc, n) for n in names}
            assert after[name] == "sentinel"
            assert all(after[n] == before[n] for n in names if n != name), name
        finally:
            setattr(mbc, name, before[name])


def test_the_realized_flip_of_the_launch_severity_did_not_drag_the_drift_class():
    """THE FOURTH CONSTANT, AND THE ONLY PIN THAT CAN SEE WHY IT EXISTS.

    `_DRIFT_SEVERITY = WARNING` and `_LAUNCH_SEVERITY = WARNING` were
    VALUE-IDENTICAL before the flip, so every assertion about the constants'
    values passed under either — and so did the separately-assignable check
    above, because rebinding one module attribute never moves another even
    when both were bound from the same expression. The module's own § 2.1
    note called an accidental merge of the two "INVISIBLE" for exactly that
    reason: a shared constant would move the fifth class's rendered caption
    AND its findings together, and no VALUE-based pin taken before the flip
    could tell the difference.

    UNTIL THE FLIP LANDED FOR REAL. `add-modified-block-currency-check` § 7.2
    flipped `_LAUNCH_SEVERITY` to `error` on 2026-08-31 (issue #357), which is
    when `_LAUNCH_SEVERITY` and `_DRIFT_SEVERITY` stopped being
    value-identical — so the guard this test now needs is a DIRECT read of the
    module's real, POST-FLIP state, not a simulation of a flip that already
    happened. (Before the flip this test simulated it over `inspect.getsource`,
    substituting one line and executing the result as a module in this
    package's namespace — a mechanism the flip itself retires: there is no
    more "before" state in the real source to substitute out of.) Added by
    the mutation round of `026-unplaced-finding-drift`, which is where
    `add-unclassified-finding-class` tasks.md § 2.14(e) says this pin is owed
    if it is missing. It was missing.
    """
    # the arm the flip reserved moved
    assert mbc._LAUNCH_SEVERITY == ERROR
    # ...and the fifth class did NOT ride it — the property this test exists
    # to hold, now falsifiable by a plain value comparison because the two are
    # no longer value-identical
    assert mbc._DRIFT_SEVERITY == WARNING
    assert mbc._DRIFT_SEVERITY != mbc._LAUNCH_SEVERITY

    bands = {klass.id: klass.band for klass in mbc.CLASSES}
    assert bands[mbc.CLASS_TITLES] == ERROR, bands
    assert bands[mbc.CLASS_DRIFT] == WARNING, bands
    # the other two arms are untouched too, which is what the split has always
    # been for
    assert bands[mbc.CLASS_RESOLUTION] == WARNING, bands
    assert bands[mbc.CLASS_LEDGER] == INFO, bands
    assert bands[mbc.CLASS_LEDGER] == INFO, bands


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


# --------------------------------- 3b. the marker: where the reason begins
#
# `amend-marker-reason-boundary` (openxFactory issue #692). The promoted
# sentence measured the reason from BEHIND — "everything after the LAST code
# span's following ` — `" — so every code span an author wrote INSIDE the reason
# was harvested as a declared-removed NAME. The amended sentence puts the
# boundary at the FIRST ` — ` standing OUTSIDE every code span; the names are
# the spans that close before it, and a span inside the reason names nothing.


def test_a_code_span_inside_the_reason_is_prose_and_names_nothing():
    """THE DEFECT, in one line. The reason is prose, and prose in this corpus
    quotes: a reason explaining that a `WHEN` bullet was replaced would, under
    the retired rule, declare `WHEN` itself removed."""
    m = mbc.parse_marker(
        "**Removed from canon by add-example-change (2026-08-27):** "
        "`Gate verbs hide on a composed view` — the unit is REPLACED, by the "
        "`WHEN` that names both facts and the `AND` beside it")
    assert m is not None
    assert m.names == ["Gate verbs hide on a composed view"]
    assert m.reason == ("the unit is REPLACED, by the `WHEN` that names both "
                        "facts and the `AND` beside it")


def test_a_separator_inside_a_code_span_is_a_unit_s_own_bytes():
    """The boundary tests SPAN MEMBERSHIP, never "the last one". A named unit
    that cites the separator itself — this very corpus carries one — must not
    be split at its own quotation."""
    m = mbc.parse_marker(
        "**Removed from canon by add-example-change (2026-08-27):** "
        "``the reason is everything after the last code span's following "
        "` — `.`` — the sentence measures the reason from behind")
    assert m is not None
    assert m.names == ["the reason is everything after the last code span's "
                       "following ` — `."]
    assert m.reason == "the sentence measures the reason from behind"


def test_a_marker_with_no_separator_still_names_every_span():
    """UNCHANGED BY THE AMENDMENT, and it is the form canon's own written-out
    `Merged into` example is in: where no separator stands outside a span,
    every span names a unit and the marker carries no reason."""
    m = mbc.parse_marker(
        "**Removed from canon by add-example-change (2026-08-27):** `A unit.`; "
        "`A second unit.`; `A third unit.`")
    assert m.names == ["A unit.", "A second unit.", "A third unit."]
    assert m.reason is None

    merged = mbc.parse_marker(MERGED)
    assert merged.names == ["Gate verbs hide on a composed view"]
    assert merged.reason is None


def test_names_separated_by_the_separator_fail_in_the_CONSERVATIVE_direction():
    """THE COST OF THE RULE, WRITTEN DOWN. An author who separated NAMES with
    ` — ` has the later ones read as reason. They suppress nothing, so the units
    that author meant to declare are REPORTED rather than silently dropped —
    which is the direction a carriage check must fail in. No marker in this
    corpus is written that way (measured; see the corpus test below)."""
    m = mbc.parse_marker(
        "**Removed from canon by add-example-change (2026-08-27):** `A unit.` "
        "— `A second unit.` — `A third unit.`")
    assert m.names == ["A unit."]
    assert m.reason == "`A second unit.` — `A third unit.`"

    # ...and the two that were dropped are therefore NOT suppressed
    canon_units = [mbc.Unit(mbc.BODY, "A unit."),
                   mbc.Unit(mbc.BODY, "A second unit.")]
    suppressed, defective = mbc.suppression([m], canon_units, [])
    assert suppressed == {(mbc.BODY, "A unit.")}
    assert defective == []


def _corpus_markers():
    """Every unit-naming marker in every promoted spec and every active delta.

    Read through `derive_units`, which is the shipping path: it drops fenced
    regions first, so this requirement's own written-out examples — complete
    markers that promote into canon — are never offered, exactly as they are
    never offered to a run.
    """
    from pathlib import Path

    from conftest import REPO_ROOT

    root = Path(REPO_ROOT)
    paths = sorted(root.glob("openspec/specs/*/spec.md"))
    paths += sorted(root.glob("openspec/changes/*/specs/*/spec.md"))
    out = []
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        units, markers = mbc.derive_units(lines)
        for marker in markers:
            if marker.form != mbc._PAIRING_FORM:
                out.append((path.relative_to(root), marker, units))
    return out


def test_no_marker_in_this_corpus_loses_a_name_it_meant_to_declare():
    """THE MEASUREMENT THE AMENDMENT RESTS ON, run as a test rather than quoted.

    For every unit-naming marker the corpus carries, the names the amended rule
    derives are a SUBSET of what the retired rule derived — the boundary can
    only move names into the reason, never the other way — and every name it
    drops matches NO derived unit anywhere in the document that carries the
    marker. So nothing any author declared is lost by the amendment: what is
    dropped is prose the reason quotes.

    Measured 2026-09-06: SEVEN unit-naming markers, TWO of them misread by the
    retired rule (both in `openspec/specs/doc-health/spec.md`, three names each
    where their authors declared one). A FLOOR rather than an exact count, so an
    unrelated archive that promotes a marker is not read as this rule's
    regression.
    """
    markers = _corpus_markers()
    assert len(markers) >= 5, [str(p) for p, _m, _u in markers]

    for rel, marker, units in markers:
        spans = mbc.extract_code_spans(marker.paragraph)
        old_names = [mbc.normalize(c) for _s, _e, c in spans
                     if mbc.normalize(c) != marker.destination]
        for name in marker.names:
            assert name in old_names, (rel, name)
        dropped = [n for n in old_names if n not in marker.names
                   and n != marker.destination]
        real = {u.text for u in units}
        for name in dropped:
            assert name not in real, (
                f"{rel}: the amended boundary drops `{name}`, which IS a unit "
                f"of that document — a declaration would be lost")


def test_the_promoted_markers_this_corpus_carries_parse_to_their_authors_names():
    """THE TWO LIVE INSTANCES, located by CONTENT and never by line number.

    `doc-health`'s *Release-tag publication* carries two `Removed from canon`
    markers whose reasons quote the words `WHEN` and `AND`. Each declared ONE
    unit — the `WHEN` bullet it retired — and the retired rule read THREE.
    """
    from pathlib import Path

    from conftest import REPO_ROOT

    lines = Path(REPO_ROOT, "openspec/specs/doc-health/spec.md").read_text(
        encoding="utf-8").splitlines()
    _units, markers = mbc.derive_units(lines)
    live = [m for m in markers
            if m.change_id in ("amend-published-tip-unreadable-scenario",
                               "amend-unreadable-read-sibling-scenarios")]
    assert len(live) == 2, [m.change_id for m in markers]

    for marker in live:
        assert len(marker.names) == 1, marker.names
        assert marker.names[0].startswith("**WHEN** the blob read for"), marker
        assert marker.reason is not None
        assert marker.reason.startswith("the clause after the dash"), marker
        # the two words the retired rule harvested are in the REASON, not named
        assert "WHEN" not in marker.names and "AND" not in marker.names
        assert "`WHEN`" in marker.reason and "`AND`" in marker.reason


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
    # A FLOOR, NOT AN EXACT COUNT, and the first cut got that wrong: it pinned
    # `== 2` and broke the moment `add-family-enumeration-check` archived and
    # promoted its third note. The population GROWS every time the corpus
    # records a repair on this requirement, so pinning it exactly makes an
    # unrelated archive look like this family's regression. Three at the time of
    # writing; two is the floor that keeps the undividedness check meaningful.
    assert len(notes) >= 2, [u.text[:70] for u in notes]

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


def test_the_scenario_arm_is_an_error():
    """FLIPPED 2026-08-31 (issue #357); launched `warning`. See
    `_LAUNCH_SEVERITY`."""
    assert {f.severity for f in _titles(_run())} == {ERROR}


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


def test_a_run_configured_fail_on_error_now_catches_the_scenario_arm():
    """N4, RE-AIMED BY THE FLIP (2026-08-31, issue #357). Through the advisory
    launch this test was named `..._is_unaffected` and asserted the opposite of
    what it asserts now: that NOTHING here reached `error`, so `--fail-on
    error` never reddened on this family. That was the whole point of an
    advisory launch and is no longer true BY DESIGN — the scenario-title arm
    is gate-bearing now, and this fixture's lossy block is exactly the shape
    it exists to catch.

    What SC-009 still guarantees, and what O8 reserves, is that the OTHER
    classes did not ride the flip: assert the finding list is NON-EMPTY FIRST,
    then split by arm rather than asserting one band over the whole list.
    """
    findings = _run()
    assert findings, "a vacuous pass is not a pass"
    titles = _titles(findings)
    others = [f for f in findings if f not in titles]
    assert {f.severity for f in titles} == {ERROR}
    assert {f.severity for f in others} <= {WARNING, INFO}
    assert not [f for f in others if f.severity in ("critical", "error")]


def test_the_file_level_scenario_count_is_not_what_the_family_reads():
    """WHY COUNTING CANNOT SEE THIS CLASS. The lossy delta's own ADDED
    requirement brings SEVEN scenarios while its MODIFIED block drops seven, so
    the FILE-LEVEL count is flat — 8 in canon, 8 in the delta — and the family
    fires anyway, because it accounts PER REQUIREMENT."""
    canon = mbc.promoted(_root(), CAP)[norm_title(REQ)]
    delta_text = (_root() / LOSSY).read_text()
    # canon states EIGHT scenarios for the requirement the block modifies, and
    # the delta FILE carries eight — one restated plus seven brought by the
    # change's own ADDED requirement. Count the file and nothing has moved.
    assert len(canon.scenario_titles) == 8
    assert delta_text.count("#### Scenario:") == 8
    assert _titles(_run()), "the flat count must not buy silence"


# --------------------------------------------------- 2. arm 2: the ledger (US2)


def _ledger(findings):
    """Ledger findings only.

    Matched on the arm's own phrase AND on "body units", because the first cut
    matched "does not carry" alone and swept up a RESOLUTION finding whose text
    happened to contain it. Two finding classes that share a phrase are two
    classes a helper must still keep apart.
    """
    return [f for f in findings
            if "does not carry" in f.rule and "body units" in f.rule]


def test_uncarried_body_units_and_bullets_are_one_info_finding_per_requirement():
    """`dh:56-57`: "It SHALL emit at most one finding per requirement, listing
    the units, rather than one finding per unit." Ten standing warnings on a
    clean repository is how a report stops being read; ten standing ROWS inside
    one finding is a list somebody reads once."""
    hits = [f for f in _ledger(_run()) if repr(REQ) in f.rule]
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


# ---------------------------------------- 4. arm 3: resolution and order (US4)


def _res_run():
    from conftest import make_ctx
    return mbc.fam_modified_block_currency(
        make_ctx("modified-block-currency-resolution"))


def _unresolved(findings):
    return [f for f in findings if "resolves to no" in f.rule]


def test_a_change_s_own_rename_resolves_first_and_the_arms_compare_the_old_name():
    """`dh:58-64`: FIRST against the change's own `## RENAMED Requirements`
    block, and where it renames a promoted requirement to this title THE THREE
    ARMS RUN — "a rename being a change of title rather than of the content a
    block must carry".

    Asserted by what the arms SAID, not by silence: the block drops canon's
    second body clause, so the ledger must report it AGAINST CANON UNDER THE OLD
    NAME. A build that resolved the rename and then compared nothing would pass
    a silence assertion.
    """
    findings = _res_run()
    mine = [f for f in findings if "add-rename-and-amend" in f.path]
    assert _unresolved(mine) == [], "an own-rename must not read as unresolved"
    hits = _ledger(mine)
    assert len(hits) == 1, [f.rule[:90] for f in hits]
    assert "A second clause holds too." in hits[0].rule
    assert "openspec/specs/res-cap/spec.md" in hits[0].rule


def test_a_title_pending_on_a_sibling_s_addition_compares_nothing_and_reports_its_pairing():
    """`dh:278-280`: "the promoted requirement being pending rather than
    absent". NOTHING IS COMPARED — and that half is unchanged.

    **MOVED BY `govern-sibling-added-modified-deltas`, 2026-09-01, AND RENAMED
    WITH THE CLAIM IT MAKES.** As written this was
    `test_a_title_pending_on_a_sibling_s_addition_is_quiet` and asserted the
    EMPTY LIST. That second half is exactly what the packet's § Why calls the
    defect: the block was dropped before ANY check looked at it, so the arms'
    silence read as clearance when it was uncomparability. What replaces the
    empty list is ONE finding of the pairing class and no other — the three
    comparison arms still do not run, the 2026-08-27 ruling against
    synthesising a basis from the sibling's ADDED text is untouched, and no
    requirement text is compared anywhere in this path.

    `add-pending-title` carries no marker, so its state is UNDECLARED: the
    corpus's own standing shape before the § 6 sweep declared the four live
    pairs.
    """
    mine = [f for f in _res_run() if "add-pending-title" in f.path]
    assert len(mine) == 1, [f.rule[:120] for f in mine]
    assert mbc.classify(mine[0]) == mbc.CLASS_PAIRING
    assert mine[0].severity == WARNING
    assert "the pairing is undeclared" in mine[0].rule
    assert "add-the-sibling" in mine[0].rule

    # ...and NOT ONE COMPARISON. Named apart from the count above, because a
    # count of one would also pass over a build that emitted a ledger finding
    # and no pairing one.
    assert _ledger(mine) == [] and _titles(mine) == []
    assert _unresolved(mine) == [] and _ordering(mine) == []


def test_a_title_resolving_to_nothing_is_reported():
    findings = [f for f in _res_run() if "add-unresolved" in f.path]
    assert len(findings) == 1, [f.rule[:90] for f in findings]
    assert findings[0].severity == WARNING
    assert "Nothing carries this title" in findings[0].rule


def test_a_capability_with_no_promoted_spec_at_all_resolves_to_nothing():
    """A DISTINCT code path: `promoted()` returns None rather than a dict that
    happens not to carry the title. Both are unresolved, and a build that only
    handled the second would crash or go silent on the first."""
    findings = [f for f in _res_run() if "add-no-canon" in f.path]
    assert len(findings) == 1, [f.rule[:90] for f in findings]
    assert "absent-cap" in findings[0].rule
    assert findings[0].severity == WARNING


# ------------------------------------------- 4. the two-writers rule, by declaration


def _tw_run():
    from conftest import make_ctx
    return mbc.fam_modified_block_currency(
        make_ctx("modified-block-currency-two-writers"))


def _ordering(findings):
    return [f for f in findings if "ordering" in f.rule]


def _in(cap, findings=None):
    return [f for f in (findings if findings is not None else _tw_run())
            if f"/{cap}/" in f.path]


def test_the_declaring_block_is_measured_against_the_sibling_s_outcome():
    """RULED 2026-08-27, "By declaration". The declaring change IS the later
    writer, and its block is measured against the sibling's OUTCOME — which for
    a MODIFIED sibling is that sibling's block, because `MODIFIED` replaces a
    requirement wholesale."""
    quiet = _in("ordered-carried")
    assert quiet == [], [f.rule[:90] for f in quiet]


def test_the_declaring_block_missing_the_siblings_addition_is_reported_by_the_ledger():
    """RULING B3: A DECLARATION IS BASIS SUBSTITUTION ONLY.

    The declaring block drops the earlier change's addition, so the LEDGER
    reports it — measured against the sibling's delta rather than against canon —
    and the resolution arm emits NOTHING for it. A second `warning` would report
    at one severity the very units the ledger already reports at another, and
    `dh:264` asks for the addition to be REPORTED, not reported twice.
    """
    findings = _in("ordered-missing")
    hits = _ledger(findings)
    assert len(hits) == 1, [f.rule[:90] for f in findings]
    assert "add-om-later" in hits[0].path, "reported against the DECLARING delta"
    assert "The earlier change's own addition." in hits[0].rule
    # measured against the sibling's outcome, and the finding says so
    assert "add-om-earlier" in hits[0].rule
    # ...and no second finding for the same units
    assert _ordering(findings) == []


def test_neither_declaring_fires_against_both_blocks():
    """`dh:76-80`: "where neither does the run SHALL report the undeclared
    ordering against both blocks, no reader being able to tell which text canon
    will keep"."""
    hits = _ordering(_in("undeclared"))
    assert {f.path.split("/")[2] for f in hits} == {"add-un-a", "add-un-b"}
    assert {f.severity for f in hits} == {WARNING}


def test_both_declaring_fires_too():
    """"mutual declaration deciding nothing" — a cycle states nothing."""
    hits = _ordering(_in("mutual"))
    assert len(hits) == 2, [f.rule[:90] for f in hits]
    assert all("2 declarations" in f.rule or "mutual" in f.rule for f in hits)


def test_a_change_id_inside_a_longer_id_declares_nothing():
    """The whole-token match `duplicate_packet._mention` already implements, and
    the reason its boundaries are `[\\w-]` rather than `\\b`: change ids are
    hyphenated, so `\\b` would treat the hyphen as a boundary and match the
    fragment. `add-li-b` names `add-li-a-extended` and declares NOTHING about
    `add-li-a`, so the pair is undeclared and both blocks are reported."""
    hits = _ordering(_in("longer-id"))
    assert len(hits) == 2, [f.rule[:90] for f in hits]


def test_an_unratified_sibling_creates_no_declaration_obligation():
    """`release-realization` scopes the obligation to an active RATIFIED change
    and `dh:30-36` states the READING scope separately and deliberately wider.
    So the draft block is READ — it is derived and its arms run — and no ordering
    finding is created for either writer."""
    findings = _in("unratified-sibling")
    assert _ordering(findings) == [], [f.rule[:90] for f in findings]
    blocks = mbc.active_blocks(
        __import__("conftest").FIXTURES
        / "modified-block-currency-two-writers" / "alphaFactory")
    draft = [b for b in blocks if b.change == "add-ur-b"]
    assert draft and draft[0].standing == "draft" and draft[0].units


def test_a_group_of_three_writers_with_one_declaration_is_reported_as_unanchored():
    """Assumption A4, RE-AIMED BY ISSUE #627 — and the fixture is unmoved.

    The 2026-08-27 reading reported EVERY group of three or more as unstated
    "whatever they declare", because `dh:262` says "two or more" and then
    describes a pair, and because the population in the real corpus was ZERO.
    The population is now five (OpsxFactory `aks-administration-workflow`), and
    `release-realization`'s "Ordered deltas and branch vocabulary" obligates the
    declaration from EVERY later writer — so the arm now reads a chain.

    THIS FIXTURE IS NOT A CHAIN AND NEVER WAS: `add-tw-b` declares relative to
    `add-tw-a`, and `add-tw-c` declares relative to nothing, so two of the three
    writers are starting points and no single order runs through them. It is
    still reported against all three blocks, each still measured against canon
    — the OUTCOME is unchanged and the REASON is now specific.
    """
    hits = _ordering(_in("three-writers"))
    assert len(hits) == 3, [f.rule[:90] for f in hits]
    assert all(
        "3 active ratified changes write it and add-tw-a, add-tw-c each "
        "declare relative to no other ratified writer of it, so the "
        "declarations state 2 starting points rather than one chain" in f.rule
        for f in hits), [f.rule[:200] for f in hits]


def test_no_basis_is_synthesized_from_a_siblings_added_block():
    """RULING B4. `add-mo-modifier` MODIFIES a title only `add-mo-adder` ADDS,
    and declares itself relative to it. The title is PENDING (`dh:278-280`), so
    it is compared against NOTHING — no basis is built from the adder's text.

    The deleted clause this pins would have measured all seven of the real
    corpus's MODIFIED-over-a-sibling's-ADDED pairs and invented roughly six
    `info` findings against text no promoted requirement carries.

    **MOVED BY `govern-sibling-added-modified-deltas`, 2026-09-01, AND THE
    RULING IT PINS IS UNCHANGED.** The assertion was `_in("pending-cap") == []`
    and is now "no COMPARISON finding, and one PAIRING finding". The ruling is
    about SYNTHESISING A BASIS; the packet adds a check whose inputs are the
    delta's own markers and the set of active additions, and which compares no
    requirement text at all. Keeping the empty list would have pinned the drop
    rather than the ruling.

    **AND THIS BLOCK IS THE ONE THAT PROVES THE PROPOSAL CROSS-REFERENCE IS NOT
    THE MARKER.** `add-mo-modifier`'s proposal DOES name `add-mo-adder` — that
    is what the two-writers arm reads for its ordering — and the pairing is
    still UNDECLARED, because a change-level mention cannot say which
    requirement rests on which sibling.
    """
    mine = _in("pending-cap")
    assert _ledger(mine) == [] and _titles(mine) == []
    assert _unresolved(mine) == [] and _ordering(mine) == []

    assert len(mine) == 1, [f.rule[:120] for f in mine]
    assert mbc.classify(mine[0]) == mbc.CLASS_PAIRING
    assert "the pairing is undeclared" in mine[0].rule
    # the cross-reference the arm above reads, and the marker it is not
    from conftest import FIXTURES
    proposal = (FIXTURES / "modified-block-currency-two-writers" / "alphaFactory"
                / "openspec" / "changes" / "add-mo-modifier" / "proposal.md")
    assert "add-mo-adder" in proposal.read_text(encoding="utf-8")


def test_no_date_folder_or_created_field_decides_the_ordering():
    """The pin that stops the WITHDRAWN reading creeping back. The spike first
    resolved "later" by `.openspec.yaml` `created:`; Brett ruled "By
    declaration" on 2026-08-27 and that reading is withdrawn.

    `add-oc-earlier` sorts BEFORE `add-oc-later` by name and by any date a
    fixture could carry, and the declaration points the same way — so the
    discriminating assertion is structural: no reader of a date, a folder name or
    a `created:` field exists in this module at all.
    """
    import inspect
    import re

    src = inspect.getsource(mbc)
    # MATCHED ON CALL SHAPES, NEVER ON BARE NAMES. The first cut forbade the
    # substring "created" and failed on this module's own docstrings, which
    # DESCRIBE the withdrawn reading — and a test that forbids describing the
    # rule is a bad test (the same lesson `test_the_reader_list_is_structural_
    # not_incidental` records about matching `_lifecycle_scope(` rather than the
    # bare name).
    forbidden = (
        r"_archive_date\s*\(",          # promotion fidelity's folder-date reader
        r"first_commit_timestamp\s*\(",  # its archive-commit tie-breaker
        r"\.created\b",                 # a `created:` field read off an object
        r"""\[["']created["']\]""",      # ...or off a mapping
        r"""get\s*\(\s*["']created["']""",
        r"strftime\s*\(",
        r"datetime\.",
    )
    for pattern in forbidden:
        assert not re.search(pattern, src), pattern
    # and no date module is imported at all
    assert not re.search(r"^\s*(?:import|from)\s+(?:datetime|time)\b", src,
                         re.M)


# ------------------------------------- 4b. N writers, by a chain of declarations
#
# ISSUE #627. The arm resolved groups of exactly two and reported every larger
# group, which cannot read a corpus `release-realization` already obliges to
# declare. Each capability of `modified-block-currency-chains` is ONE
# arrangement of N declarations, on the `-two-writers` tree's convention that
# arrangements must not interfere.


def _ch_run():
    from conftest import make_ctx
    return mbc.fam_modified_block_currency(
        make_ctx("modified-block-currency-chains"))


def _ch(cap, findings=None):
    return [f for f in (findings if findings is not None else _ch_run())
            if f"/{cap}/" in f.path]


def test_a_declared_chain_of_three_ratified_writers_resolves_and_says_nothing():
    """THE POSITIVE CASE, and it is silence.

    Three ratified writers, each declaring its predecessor, state one order —
    so each is measured against the block before it, each carries that block,
    and the arm emits nothing. A resolved chain is exactly as quiet as a
    resolved pair; the ordering finding is what an UNSTATED order costs.
    """
    quiet = _ch("chain-three")
    assert quiet == [], [f.rule[:120] for f in quiet]


def test_the_chain_basis_is_the_predecessor_s_block_and_carries_it_transitively():
    """RULING B3 EXTENDED ALONG THE CHAIN, and the finding names the basis.

    `add-cb-c` declares `add-cb-b`, which declares `add-cb-a`. `MODIFIED`
    replaces a requirement wholesale, so the outcome the third writer is
    measured against is the SECOND writer's block — which itself carries the
    first writer's addition. The third block drops that addition, and what
    reports it is the LEDGER, against the third delta's own path, naming the
    SECOND writer's delta as the text it was measured against. Against canon
    the same block would be clean, so this assertion is what makes the chain's
    basis substitution falsifiable rather than merely stated.
    """
    findings = _ch("chain-basis")
    hits = _ledger(findings)
    assert len(hits) == 1, [f.rule[:120] for f in findings]
    assert "add-cb-c" in hits[0].path, "reported against the LAST writer"
    assert "openspec/changes/add-cb-b/specs/chain-basis/spec.md" in hits[0].rule
    assert "The first writer's addition." in hits[0].rule
    assert _ordering(findings) == []


def test_a_redundant_declaration_three_links_back_still_resolves():
    """THE REAL-CORPUS SHAPE, and the reason the rule is a TOTAL ORDER rather
    than one predecessor per writer.

    OpsxFactory's five-writer chain has `reanchor-keycloak-broker-to-syscore2`
    naming both its predecessor `admit-secretproviderclass-to-aks-scope` AND,
    three links back, `adopt-keycloak-broker-qa` — the change it re-anchors and
    could hardly discuss without naming. That edge states nothing transitivity
    does not already state. A rule counting one declaration per writer would
    report the compliant corpus as forked, which is the defect this test
    exists to keep out: `add-cr-d` declares `add-cr-c` and `add-cr-a`, and the
    four writers still state one order.
    """
    quiet = _ch("chain-redundant")
    assert quiet == [], [f.rule[:120] for f in quiet]


def test_two_writers_declaring_the_same_predecessor_are_reported_as_a_fork():
    """A FORK STATES NO ORDER between the two branches, so it is reported.

    `add-fk-b` and `add-fk-c` both declare relative to `add-fk-a` and neither
    declares relative to the other: whichever archives last is the text canon
    keeps, and no reader can tell which. Reported against all three blocks —
    the root included, because the group's order is what is unstated.
    """
    hits = _ordering(_ch("fork-branches"))
    assert {f.path.split("/")[2] for f in hits} == {
        "add-fk-a", "add-fk-b", "add-fk-c"}
    assert {f.severity for f in hits} == {WARNING}
    assert all(
        "3 active ratified changes write it and the declarations fork at "
        "add-fk-b, add-fk-c: each is declared later than a writer already "
        "placed and none is declared later than another" in f.rule
        for f in hits), [f.rule[:200] for f in hits]


def test_declarations_running_in_a_cycle_are_reported_as_a_cycle():
    """"mutual declaration deciding nothing" AT LENGTH THREE. A cycle of two is
    the pair path's own case; a cycle of three states no order for the same
    reason, and the arm says which writers the cycle runs through so a reader
    does not have to re-derive it from three proposals."""
    hits = _ordering(_ch("cycle-three"))
    assert len(hits) == 3, [f.rule[:120] for f in hits]
    assert all(
        "3 active ratified changes write it and their declarations run in a "
        "cycle, leaving add-cy-a, add-cy-b, add-cy-c unplaceable — a cycle "
        "states no order" in f.rule
        for f in hits), [f.rule[:200] for f in hits]


def test_a_declaration_naming_an_unratified_writer_anchors_nothing_in_the_group():
    """THE `outside` REFINEMENT OF `unanchored`, and it exists to answer the
    question the bare defect leaves open.

    `add-oa-c` DID declare — it names `add-oa-d`, which writes this requirement
    too but is a draft, so `release-realization`'s obligation is not discharged
    by it and the chain gains no link. The group therefore has two starting
    points, and reporting only that would send a reader to a proposal that
    looks compliant. The finding names the declaration and says why it anchors
    nothing.
    """
    hits = _ordering(_ch("outside-anchor"))
    assert len(hits) == 3, [f.rule[:120] for f in hits]
    assert "add-oa-d" not in {f.path.split("/")[2] for f in hits}, (
        "the draft writer is not a ratified writer and takes no finding")
    assert all(
        "3 active ratified changes write it and add-oa-c declares relative to "
        "add-oa-d, which writes it but is not ratified, so that declaration "
        "anchors nothing inside the ratified group" in f.rule
        for f in hits), [f.rule[:200] for f in hits]


def test_an_unratified_writer_is_no_link_in_the_chain():
    """`release-realization` scopes the ordering obligation to an active
    RATIFIED change, and this family does not widen it — the reading scope stays
    deliberately wider, so the draft block is still derived and its arms still
    run.

    THE SILENCE IS THE PROOF. All four blocks drop canon's second clause.
    `add-mx-a` is the chain's root and `add-mx-d` is a draft outside it, so both
    are measured against CANON and both are reported; `add-mx-b` and `add-mx-c`
    are measured against their predecessors' blocks, which drop the same clause,
    and are silent. A draft counted as a link, or a chain not resolved, moves
    that count immediately.
    """
    findings = _ch("mixed-unratified")
    assert _ordering(findings) == [], [f.rule[:90] for f in findings]
    assert {f.path.split("/")[2] for f in _ledger(findings)} == {
        "add-mx-a", "add-mx-d"}
    blocks = mbc.active_blocks(
        __import__("conftest").FIXTURES
        / "modified-block-currency-chains" / "alphaFactory")
    draft = [b for b in blocks if b.change == "add-mx-d"]
    assert draft and draft[0].standing == "draft" and draft[0].units


def test_the_two_writer_path_never_consults_the_chain_rule():
    """THE PAIR CASE IS UNMOVED, asserted STRUCTURALLY rather than by re-reading
    its findings.

    Issue #627 asks for byte-identical behaviour on groups of two, and the tests
    above this section already read those bytes. What they cannot show is that
    the pair outcome does not merely AGREE with the chain rule today — a later
    edit routing pairs through `_chain` would keep them all green and would put
    the pair case's three ruled outcomes (resolved, mutual, undeclared) at the
    mercy of a rule ruled for a different population. So the chain rule is made
    to explode, and every two-ratified-writer group in the `-two-writers` tree
    is still evaluated.
    """
    import pytest

    from conftest import FIXTURES

    root = FIXTURES / "modified-block-currency-two-writers" / "alphaFactory"
    blocks = mbc.active_blocks(root)
    declared = mbc.declarations(root, blocks)
    groups: dict[tuple[str, str], list] = {}
    for block in blocks:
        groups.setdefault((block.capability, norm_title(block.title)),
                          []).append(block)

    def boom(*args, **kwargs):
        raise AssertionError("the pair path consulted the chain rule")

    seen = 0
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(mbc, "_chain", boom)
        for key in sorted(groups):
            group = groups[key]
            if len([b for b in group if b.standing == "ratified"]) != 2:
                continue
            seen += 1
            mbc._arm_ordering("alphaFactory", group, declared)
    assert seen >= 4, f"only {seen} two-writer groups — the tree moved"


def test_the_chain_rule_is_a_total_order_and_names_where_it_fails():
    """`_chain` DIRECTLY, over the shapes no fixture should have to be built for.

    The fixtures above are the corpus-shaped evidence; this is the algebra they
    rest on, and it is asserted apart because a fixture per graph would be seven
    trees for one function. `(a, b)` means a's proposal names b, so a is the
    LATER writer and the earliest is the one naming nobody.
    """
    chain, defect, blamed = mbc._chain(
        ["a", "b", "c"], {("b", "a"), ("c", "b")})
    assert (chain, defect, blamed) == (["a", "b", "c"], "", [])

    # a redundant edge the chain already implies changes nothing
    chain, defect, _ = mbc._chain(
        ["a", "b", "c"], {("b", "a"), ("c", "b"), ("c", "a")})
    assert (chain, defect) == (["a", "b", "c"], "")

    # two starting points, no declaration between them
    assert mbc._chain(["a", "b", "c"], {("b", "a")}) == (
        None, "unanchored", ["a", "c"])

    # one root, and the fork is found where the second placement is ambiguous
    assert mbc._chain(["a", "b", "c"], {("b", "a"), ("c", "a")}) == (
        None, "forked", ["b", "c"])

    # a cycle blocks the writers downstream of it too, and the finding names
    # every writer no order could be placed over rather than the cycle alone
    assert mbc._chain(["a", "b", "c"], {("a", "b"), ("b", "a"), ("c", "a")}) == (
        None, "cycle", ["a", "b", "c"])


# ------------------------------------- 5. dispositions, skip, and determinism


def _dispositions(tmp_path, body: str):
    health = tmp_path / "health"
    health.mkdir(parents=True, exist_ok=True)
    (health / "dispositions.yaml").write_text(body, encoding="utf-8")
    return tmp_path


def _with_agg(agg):
    from conftest import make_ctx
    return mbc.fam_modified_block_currency(
        make_ctx("modified-block-currency", agg_root=agg))


def test_a_disposition_naming_this_family_suppresses_the_path(tmp_path):
    """THE EXISTING MECHANISM, read through `promotion_fidelity`'s reader under
    this family's own name — no second reader (`tasks:113-116`). An entry with no
    `requirement:` key disposes every finding on that path, which is the coarser
    behaviour every other family's entry already has."""
    agg = _dispositions(tmp_path, f"""
- family: {mbc.FAMILY}
  repo: {FIXTURE_REPO}
  path: {LOSSY}
  cite: add-modified-block-currency-check
""")
    assert [f for f in _with_agg(agg) if f.path == LOSSY] == []
    assert [f for f in _run() if f.path == LOSSY], \
        "the same tree without the disposition still reports on that path"
    # ...and ONLY that path: the draft change's own block is untouched, because
    # a disposition names a path and not a family-wide amnesty.
    assert [f for f in _with_agg(agg) if "add-draft-block" in f.path]


def test_an_entry_narrowed_by_requirement_suppresses_only_that_requirement(tmp_path):
    agg = _dispositions(tmp_path, f"""
- family: {mbc.FAMILY}
  repo: {FIXTURE_REPO}
  path: {LOSSY}
  requirement: {REQ}
  cite: add-modified-block-currency-check
""")
    findings = _with_agg(agg)
    assert [f for f in findings if repr(REQ) in f.rule] == []
    # its file-mate is NOT suppressed: the entry names one requirement. (The
    # lossy delta's OTHER block is in the same file.)
    assert findings, "a narrowed entry must not silence the whole path"


def test_an_uncited_entry_disposes_nothing(tmp_path):
    """An entry without a `cite` records no decision — the rule every other
    family's reader already applies to the same file."""
    agg = _dispositions(tmp_path, f"""
- family: {mbc.FAMILY}
  repo: {FIXTURE_REPO}
  path: {LOSSY}
""")
    assert _with_agg(agg)


def test_a_disposition_for_another_family_disposes_nothing(tmp_path):
    """THE COLLISION THIS PREVENTS is the argument D1 makes for a separate
    family: one citation must not buy silence for a promotion gap and a currency
    gap on the same path."""
    agg = _dispositions(tmp_path, f"""
- family: promotion-fidelity
  repo: {FIXTURE_REPO}
  path: {LOSSY}
  cite: add-promotion-fidelity-check
""")
    assert _with_agg(agg)


def test_a_single_repo_run_has_no_aggregation_root_and_applies_no_disposition():
    """THE INHERITED CAVEAT, pinned so the self-gate's silence about dispositions
    is understood rather than discovered: `health/dispositions.yaml` lives at the
    AGGREGATION root, and a `--single-repo` run has none. That is the
    pre-existing shape of the mechanism (`runner.main` guards the same read with
    `if ctx.agg_root`), not something this family chose."""
    from conftest import make_ctx

    ctx = make_ctx("modified-block-currency")
    assert getattr(ctx, "agg_root", None) is None
    assert mbc.fam_modified_block_currency(ctx)


def test_a_scope_with_no_changes_directory_skips_with_its_reason():
    """`dh:291-294`: "the family MUST be reported as skipped with its reason,
    never silently omitted"."""
    from doc_health import Skip
    from conftest import make_ctx

    out = mbc.fam_modified_block_currency(make_ctx("modified-block-currency-noscope"))
    assert isinstance(out, Skip)
    assert out.family == mbc.FAMILY
    assert "changes" in out.reason


def test_a_scope_with_active_changes_but_no_modified_block_is_not_skipped():
    """THE OTHER STATE, and canon keeps them apart: the skip rule is "cannot
    run", not "found nothing". A scope carrying active changes with no MODIFIED
    block among them RAN — and a family that reported itself skipped there would
    teach a reader that it never runs."""
    from doc_health import Skip
    from conftest import make_ctx

    out = mbc.fam_modified_block_currency(make_ctx("modified-block-currency-quiet"))
    assert not isinstance(out, Skip)
    assert out == []


def test_two_runs_agree_byte_for_byte():
    a, b = _tw_run(), _tw_run()
    assert ([f.__dict__ for f in a] == [f.__dict__ for f in b])


def test_the_family_returns_its_findings_sorted_severity_first():
    """`runner.run_suite` sorts the WHOLE report, so an unsorted family is
    invisible there — and visible immediately in a `--family` run, which is what
    a session uses while fixing a block.

    SEVERITY LEADS THE KEY, by ruling of 2026-08-27, and the reason is the shape
    of every real tree: the ledger's population is standing by construction, so
    the ONE gate-bearing `warning` is outnumbered by editorial `info` rows. Under
    a path-first sort it rendered in the middle of them — burying the precise
    signal in the editorial ones, which is the exact failure the delta split the
    arms to avoid.
    """
    from doc_health import SEVERITY_RANK

    for findings in (_run(), _tw_run(), _markers_run()):
        keys = [(SEVERITY_RANK[f.severity], f.repo, f.path, f.rule)
                for f in findings]
        assert keys == sorted(keys)

    # ...and on the real shape — one gate-bearing finding among many info rows
    # — that finding is FIRST, which is the property the ruling actually
    # bought. WARNING through the advisory launch; ERROR since the flip
    # (2026-08-31, issue #357) — SEVERITY_RANK still ranks it ahead of INFO
    # either way, so this is the flip's own severity, not a re-derivation.
    findings = _run()
    assert findings[0].severity == mbc._LAUNCH_SEVERITY == ERROR
    assert [f.severity for f in findings].count(INFO) > 1


# ------------------------------ 6. the registration, and three mutation escapes


def test_the_family_is_registered_and_reachable_through_the_registry():
    """The module is only reachable through the report a session reads if it is
    registered. Routed through `FAMILIES` here — and ONLY here plus the two tests
    below — because everything else in this file calls the module directly, which
    is what let phases 1-7 land while the registration was gated."""
    from doc_health.families import FAMILIES

    assert mbc.FAMILY in FAMILIES
    assert FAMILIES[mbc.FAMILY] is mbc.fam_modified_block_currency
    from conftest import make_ctx
    assert FAMILIES[mbc.FAMILY](make_ctx("modified-block-currency"))


def test_the_family_joined_family_resolution_on_the_flip():
    """THE SECOND HALF, PINNED AT BOTH ENDS OF THE FLIP.

    Through the advisory launch this test was named `..._is_absent_from_
    family_resolution_at_launch` and pinned the opposite: `report.
    uncited_resolutions` turns a `contested` finding that VANISHES between
    reports into an `error`, so a `contested` class at launch would have red
    the nightly on the first correction — enforcement arriving through the
    back door on the run that proves the advisory launch worked.

    FLIPPED 2026-08-31 by ruling, together with `_LAUNCH_SEVERITY` (issue
    #357). `families.FAMILY_RESOLUTION` has no per-class grain — `runner.main`
    applies it by `Finding.family` alone — so the one row the flip adds
    reaches every class this family emits, the ledger included: a finding that
    vanishes now owes a citation the same way `promotion-fidelity`'s and
    `duplicate-packet`'s do. See the `FAMILY_RESOLUTION` entry in `families.py`
    for the reading in full.

    NON-VACUOUS BY CONSTRUCTION: membership in `FAMILIES` is asserted in the
    same test, so this cannot pass against an empty or misspelled registry.
    """
    from doc_health import CONTESTED
    from doc_health.families import FAMILIES, FAMILY_RESOLUTION

    assert mbc.FAMILY in FAMILIES, "the membership below means nothing otherwise"
    assert FAMILY_RESOLUTION.get(mbc.FAMILY) == CONTESTED
    # and the severities that make up the other half — one moved, two did not
    assert mbc._LAUNCH_SEVERITY == ERROR
    assert mbc._LEDGER_SEVERITY == INFO


def test_the_reporting_list_mirrors_the_registry():
    """`FAMILY_IDS` is the registry's complete projection onto the report, not a
    second definition of the set. It drifted for months once —
    `staged-topic-template` and `proposal-origin` reported 61 findings, three of
    them ERRORS, under no section at all."""
    from doc_health import FAMILY_IDS
    from doc_health.families import FAMILIES

    assert set(FAMILY_IDS) == set(FAMILIES)
    assert len(FAMILY_IDS) == len(set(FAMILY_IDS)) == len(FAMILIES) == 23
    assert mbc.FAMILY in FAMILY_IDS


def test_the_promoted_reader_cannot_reach_a_measurement_basis():
    """ADDED BY THE MUTATION ROUND. `test_a_live_main_basis_request_changes_
    nothing` asserts the OUTCOME is unaffected, and a mutant that made the
    reader consult a basis survived it — because the assertion compares two runs
    that would BOTH have consulted it.

    The guarantee is structural and now says so: `promoted` takes a filesystem
    root and a capability, full stop. No context, no git shim, no ref. There is
    nothing for a basis option to arrive through.
    """
    import inspect

    assert list(inspect.signature(mbc.promoted).parameters) == [
        "root", "capability"]
    assert list(inspect.signature(mbc.active_blocks).parameters) == ["root"]
    import re

    src = inspect.getsource(mbc)
    # MATCHED ON USE, NOT ON MENTION — and this test failed its first run for
    # exactly that reason: `promoted`'s docstring NAMES `WorkingTree` and
    # `GitRefTree` to say it uses neither. A test that forbids describing the
    # rule is a bad test, which is the third time this file has learnt it.
    for pattern in (r"promotion_fidelity_basis",
                    r"\bWorkingTree\s*\(", r"\bGitRefTree\s*\(",
                    r"\.resolve_ref\s*\(", r"\.ls_tree_paths\s*\(",
                    r"\.show_blob\s*\(", r"\bctx\.git\b"):
        assert not re.search(pattern, src), pattern


def test_a_marker_whose_author_is_not_a_change_id_is_not_a_marker():
    """ADDED BY THE MUTATION ROUND. Loosening the change-id group to `(.+?)`
    SURVIVED, because the only quoted-template case in this file also carries a
    placeholder DATE — so the date group was doing all the work and the id group
    was unpinned.

    The id matters on its own: `**Removed from canon by Brett (2026-08-27):**`
    is a paragraph a human could plausibly write, and it is NOT a declaration.
    The marker's whole falsifiability is that it names the CHANGE accountable for
    the deletion, which is what an archived delta can later be read against.
    """
    assert mbc.parse_marker(
        "**Removed from canon by Brett (2026-08-27):** `A unit.`") is None
    assert mbc.parse_marker(
        "**Removed from canon by Some Change (2026-08-27):** `A unit.`") is None
    assert mbc.parse_marker(
        "**Removed from canon by ADD-UPPER (2026-08-27):** `A unit.`") is None
    # ...and the real spelling still parses
    assert mbc.parse_marker(
        "**Removed from canon by add-a-change (2026-08-27):** `A unit.`")


# ============================================================================
# THE PAIRING CLASS AND THE COLLISION CLASS
# (`govern-sibling-added-modified-deltas`, Speckit F1 § 2 and F2 § 3)
# ============================================================================
#
# TWO TREES, AND EACH ASSERTION BELOW NAMES ITS SUBJECT. `-pairing` carries
# every reported state of the pairing class plus BOTH silent ones plus the
# own-rename carve; `-collision` carries the unsafe archive order in both basis
# forms plus the lawful-rename negative control. Their READMEs carry the table.
#
# NOTHING HERE COMPARES REQUIREMENT TEXT, which is the whole of what the
# 2026-08-27 ruling protects: the pairing check's inputs are a delta's own
# markers and the set of active additions.

def _pair_run():
    from conftest import make_ctx
    return mbc.fam_modified_block_currency(
        make_ctx("modified-block-currency-pairing"))


def _coll_run():
    from conftest import make_ctx
    return mbc.fam_modified_block_currency(
        make_ctx("modified-block-currency-collision"))


def _pairing(findings):
    return [f for f in findings if mbc.classify(f) == mbc.CLASS_PAIRING]


def _pair_for(change, findings=None):
    """The pairing findings against ONE change's delta path.

    Keyed on the PATH the family put on the finding, never on a re-read of the
    fixture: this file asserts what the family wrote.
    """
    return [f for f in _pairing(findings if findings is not None
                                else _pair_run())
            if f"/changes/{change}/" in f.path]


def _state(finding):
    """The state word the finding renders, read out of the rendered rule."""
    return finding.rule.split(" and the pairing is ")[1].split(":")[0]


def test_the_third_reserved_form_is_recognized_by_its_complete_prefix():
    """§ 2.1. The anchor is load-bearing for the reason it is on the other two
    forms: this packet's own delta text and `document-lifecycle`'s both set the
    template out in prose, and both promote into canon."""
    good = ("**Modified over `add-a-basis`'s addition by add-a-carrier "
            "(2026-09-01):** — because the basis is still active")
    marker = mbc.parse_marker(good)
    assert marker is not None
    assert (marker.form, marker.basis, marker.change_id, marker.date) == (
        "pairing", "add-a-basis", "add-a-carrier", "2026-09-01")
    assert marker.reason == "because the basis is still active"

    # THE QUOTED TEMPLATE IS NOT A MARKER, which is why the prefix is complete:
    # `document-lifecycle` prints this exact line in prose that promotes.
    assert mbc.parse_marker(
        "**Modified over `<basis change-id>`'s addition by <change-id> "
        "(<YYYY-MM-DD>):**") is None
    # ...nor is a prefix missing any one of its parts
    for bad in (
        "**Modified over `add-a-basis` addition by add-a-carrier (2026-09-01):**",
        "**Modified over `add-a-basis`'s addition by add-a-carrier:**",
        "**Modified over add-a-basis's addition by add-a-carrier (2026-09-01):**",
        "**Modified over `add-a-basis`'s addition by ADD-UPPER (2026-09-01):**",
        "**Modified over `Not A Change Id`'s addition by add-a-carrier "
        "(2026-09-01):**",
    ):
        assert mbc.parse_marker(bad) is None, bad


def test_the_third_form_names_no_units_and_is_no_carriage_declaration():
    """§ 2.2, and every consequence of it is a consequence of ONE fact: the
    marker's `names` list is empty.

    It therefore suppresses nothing, can never reach the marker-defect class
    (that list is only appended to from inside the per-name loop), and — like
    every marker — is no unit of the block or of canon.
    """
    marker = mbc.parse_marker(
        "**Modified over `add-a-basis`'s addition by add-a-carrier "
        "(2026-09-01):** — the reason names `a code span` inside itself")
    assert marker.names == []
    # THE WHOLE TAIL, not what follows the last code span: this form names no
    # units, so there is nothing in the tail to measure the reason from behind.
    assert marker.reason == "the reason names `a code span` inside itself"

    canon_units = [mbc.Unit(mbc.BODY, "A unit.")]
    suppressed, defective = mbc.suppression([marker], canon_units, [])
    assert suppressed == set() and defective == []

    # ...and it is no unit on either side of a comparison
    units, markers = mbc.derive_units([
        "**Modified over `add-a-basis`'s addition by add-a-carrier "
        "(2026-09-01):** — a reason.",
        "",
        "A body sentence.",
    ])
    assert [u.text for u in units] == ["A body sentence."]
    assert [m.form for m in markers] == ["pairing"]


def test_the_reason_is_harvested_always_and_an_absent_tail_is_a_value():
    """§ 2.2's second half. Recognition ENDS AT THE CLOSING COLON, so a
    prefix-only paragraph is a MARKER OF THIS FORM whose declaration is
    defective — never a non-marker, which would return it to the body units and
    hand its author the absent-marker remedy for a marker the block carries."""
    prefix_only = mbc.parse_marker(
        "**Modified over `add-a-basis`'s addition by add-a-carrier "
        "(2026-09-01):**")
    assert prefix_only is not None and prefix_only.form == "pairing"
    assert prefix_only.reason is None
    # an empty reason declares exactly what an absent one does
    empty = mbc.parse_marker(
        "**Modified over `add-a-basis`'s addition by add-a-carrier "
        "(2026-09-01):** —   ")
    assert empty is not None and empty.reason is None


def test_the_sibling_set_carries_the_adder_its_standing_and_its_block_kind():
    """§ 2.3. The TITLE CONTENT is unchanged — both basis forms still make a
    title pending — and what is added is three facts about the DELTA: who adds
    it, what that change's own proposal declares, and whether the title arrived
    by an addition or by a rename's `TO:` half.

    Read through the module's own `_standing` path, never a private regex: the
    fact that qualifies a finding's wording and the fact the UNDISCLOSED state
    turns on are ONE fact read once.
    """
    from conftest import FIXTURES
    root = FIXTURES / "modified-block-currency-pairing" / "alphaFactory"
    siblings = mbc.sibling_titles(root)

    ratified = siblings[("pair-cap", "declared and resolving")]
    assert [(b.change, b.kind, b.standing) for b in ratified] == [
        ("add-basis-ratified", "added", "ratified")]
    draft = siblings[("pair-cap", "undisclosed basis")]
    assert [(b.change, b.kind, b.standing) for b in draft] == [
        ("add-basis-draft", "added", "draft")]
    headerless = siblings[("pair-cap", "headerless basis")]
    assert [(b.change, b.kind, b.standing) for b in headerless] == [
        ("add-basis-headerless", "added", None)]
    # the rename's `TO:` half, and the discriminator that tells it from an
    # addition — which is what the self-referential state is defined by
    rename = siblings[("pair-cap", "promoted new name")]
    assert [(b.change, b.kind) for b in rename] == [
        ("mod-rename-amend", "renamed")]


def test_every_reported_state_is_reached_and_each_block_carries_exactly_one():
    """§ 2.5. FOUR REPORTED STATES, ONE FINDING PER BLOCK, AND THE ORDER IS
    WHAT MAKES THEM EXCLUSIVE.

    Asserted as a MAP from change to state rather than as a count: a count
    passes over a build that reported the right number of findings in the wrong
    states, and the words a reader is given are the deliverable.
    """
    findings = _pair_run()
    states = {}
    for f in _pairing(findings):
        change = f.path.split("/changes/")[1].split("/")[0]
        assert change not in states, (change, "two findings for one block")
        states[change] = _state(f)

    assert states == {
        "mod-undeclared": "undeclared",
        "mod-self": "self-referential",
        "mod-self-marked": "self-referential",
        "mod-wrong-basis": "misdeclared",
        "mod-carrier-basis": "misdeclared",
        "mod-wrong-by": "misdeclared",
        "mod-two-markers": "misdeclared",
        "mod-no-reason": "misdeclared",
        "mod-empty-reason": "misdeclared",
        "mod-no-reason-unratified": "misdeclared",
        "mod-undisclosed": "undisclosed",
        "mod-headerless": "undisclosed",
        # THE CARVE'S OTHER SIDE. The carrier's OWN rename made this title
        # pending — its `FROM:` half is a title canon does not carry, so
        # `resolve`'s own-rename precedence never fired — and it is UNDECLARED,
        # not self-referential: a title pair is no second text. This row is what
        # a widening of the self-addition condition to renames fails on.
        "mod-own-rename-unpromoted": "undeclared",
    }
    # ...and the three silent ones are silent
    for silent in ("mod-one-marker", "mod-declared", "mod-disclosed",
                   "mod-rename-amend"):
        assert _pair_for(silent, findings) == [], silent


def test_the_self_referential_state_is_examined_first_and_excludes_the_others():
    """§ 2.5's ordering, at the one place it changes an answer. A
    self-referential block carrying NO marker satisfies UNDECLARED as well, so
    without the order the run emits two findings with two remedies for one
    defect — and this state's remedy, withdrawing one of the two blocks, is one
    no marker supplies.

    READ FROM THE CARRIER'S OWN `## ADDED Requirements` BLOCK AND FROM NOTHING
    ELSE: `mod-rename-amend` renames a PROMOTED requirement to the title it also
    modifies, and that is the rename-and-amend shape canon resolves under the
    OLD name one step before `pending`.
    """
    findings = _pair_run()
    no_marker = _pair_for("mod-self", findings)
    assert len(no_marker) == 1 and _state(no_marker[0]) == "self-referential"
    # ...and the UNDECLARED remedy is not what it names. Asserted on the
    # undeclared state's own wording rather than on the phrase "no marker",
    # which this state's text uses to say that no marker CAN cure it.
    assert "carries no marker of the reserved" not in no_marker[0].rule

    # ...and a marker naming the change ITSELF does not move it either
    marked = _pair_for("mod-self-marked", findings)
    assert len(marked) == 1 and _state(marked[0]) == "self-referential"

    # ...AND THE CONDITION IS THE CARRIER'S OWN ADDITION AND NOTHING ELSE.
    # `mod-own-rename-unpromoted` is the carrier's OWN rename to the title, with
    # a `FROM:` half canon does not carry — so `resolve`'s own-rename precedence
    # does not fire and the block reaches this check with the carrier as the
    # only writer of the title. Widening the condition to renames reports the
    # supported shape as a defect, and this is the row that says so.
    own_rename = _pair_for("mod-own-rename-unpromoted", findings)
    assert len(own_rename) == 1 and _state(own_rename[0]) == "undeclared"
    assert "rename to the title" in own_rename[0].rule


def test_the_own_rename_carve_never_reaches_this_check_and_the_arms_run():
    """§ 2.4. `resolve()` IS NOT TOUCHED, and its second step is why: the
    carrying change's own `## RENAMED Requirements` block is examined BEFORE the
    set of titles active changes add, so a rename-and-amend block resolves
    against canon under the OLD name and never reaches the classifier.

    ASSERTED POSITIVELY, not as a silence. A silence assertion passes over a
    build that resolved the rename and then compared nothing — so the ONE
    dropped clause is what proves the comparison arms RAN.
    """
    findings = _pair_run()
    assert _pair_for("mod-rename-amend", findings) == []
    ledger = [f for f in findings if "/changes/mod-rename-amend/" in f.path]
    assert len(ledger) == 1, [f.rule[:120] for f in ledger]
    assert "A second clause holds too." in ledger[0].rule
    assert "openspec/specs/pair-cap/spec.md" in ledger[0].rule


def test_the_misdeclared_grounds_are_named_apart_in_the_finding():
    """§ 2.5. FOUR GROUNDS, ONE STATE, ONE ACTION — and the finding SHALL say
    which ground it names, because more than one marker, a wrong basis, a wrong
    author and an absent reason are repaired by four different edits.

    THE COUNT IS READ FIRST, so a block carrying a good marker and a bad one is
    placed by a fact about the BLOCK rather than by which marker a loop reached.
    `mod-one-marker` is that block's PAIR — the same valid marker, alone — and
    it is silent.
    """
    findings = _pair_run()

    count = _pair_for("mod-two-markers", findings)
    assert len(count) == 1
    assert "carries 2 markers of the reserved" in count[0].rule
    assert _pair_for("mod-one-marker", findings) == []

    basis = _pair_for("mod-wrong-basis", findings)
    assert "names `mod-undeclared` as basis" in basis[0].rule
    assert "no active change of that id ADDS" in basis[0].rule

    carrier = _pair_for("mod-carrier-basis", findings)
    assert "names the carrying change `mod-carrier-basis` as its own basis" \
        in carrier[0].rule

    author = _pair_for("mod-wrong-by", findings)
    assert "`by` identifier is `mod-undeclared`" in author[0].rule
    assert "carried by `mod-wrong-by`" in author[0].rule

    for change in ("mod-no-reason", "mod-empty-reason"):
        reason = _pair_for(change, findings)
        assert "no ` — <reason>` tail" in reason[0].rule, change


def test_the_reason_is_read_before_the_disclosure():
    """§ 2.5's fifth ordering claim, and the fixture that fails a classifier
    reading them the other way round.

    `mod-no-reason-unratified` carries a right basis, a right `by` and NO tail
    at all, over a `draft` basis. Read disclosure-first it would be told to
    write `unratified` into a sentence that does not exist, while the identical
    marker over a RATIFIED basis (`mod-no-reason`) passed in silence — one
    defect named two ways at two titles.
    """
    findings = _pair_run()
    ordered = _pair_for("mod-no-reason-unratified", findings)
    assert len(ordered) == 1
    assert _state(ordered[0]) == "misdeclared"
    assert "no ` — <reason>` tail" in ordered[0].rule
    assert "unratified" not in ordered[0].rule.split(": ", 1)[1]

    # ...and the identical marker over a RATIFIED basis is reported on the SAME
    # ground, so the finding does not depend on the basis's standing
    ratified = _pair_for("mod-no-reason", findings)
    assert _state(ratified[0]) == "misdeclared"
    assert "no ` — <reason>` tail" in ratified[0].rule


def test_the_undisclosed_state_names_the_basis_and_its_standing():
    """§ 2.5's fourth state — the one that gives `document-lifecycle`'s
    disclosure obligation an enforcer at all.

    A basis whose header declares NO standing this reader can resolve is treated
    as not ratified, the whole point of the disclosure being to warn about text
    no authority has been shown to accept.
    """
    findings = _pair_run()
    draft = _pair_for("mod-undisclosed", findings)
    assert "`add-basis-draft`" in draft[0].rule
    assert "declared standing `draft`" in draft[0].rule

    headerless = _pair_for("mod-headerless", findings)
    assert "no standing its proposal header declares" in headerless[0].rule

    # ...and the disclosure is read as a WORD, so the disclosed pair is silent
    assert _pair_for("mod-disclosed", findings) == []


def test_the_pairing_class_carries_its_own_band_and_action():
    """The band is `warning` at launch, from a constant of its own — NOT
    `_LAUNCH_SEVERITY`, whose § 7.2 flip moved it alone at `7f656980`.

    The action states EVERY half of the remedy, and it is spelled out here
    rather than compared with the module's constant: a test asserting
    `f.action == mbc._PAIRING_ACTION` passes whatever that constant is mutated
    to.
    """
    findings = _pairing(_pair_run())
    assert findings
    assert {f.severity for f in findings} == {WARNING}
    assert {f.action for f in findings} == {
        "declare the basis with ONE `Modified over` marker and no more than "
        "one, name the change carrying the block as that marker's `by` "
        "identifier, give the marker the ` — <reason>` tail its form requires, "
        "disclose in that reason clause where the basis is not ratified, and "
        "hold the archive until the declared change promotes"}
    # THE TWO CONSTANTS ARE APART, AND THE FLIP IS THE PROOF: `_LAUNCH_SEVERITY`
    # moved to `error` at `7f656980` and this class launches at `warning`, so a
    # shared constant is falsified by their current values rather than by an
    # argument about them.
    assert mbc._PAIRING_SEVERITY == WARNING and mbc._LAUNCH_SEVERITY == ERROR


def test_the_collision_class_reports_both_basis_forms_and_never_the_from_half():
    """F2 § 3.1. The `TO:` half is the collision shape; the `FROM:` half is a
    title canon is EXPECTED to carry, so reading it would report every lawful
    rename in the corpus.

    The negative control is `lawful-rename`, whose `FROM:` title canon carries
    and whose `TO:` title it does not.
    """
    findings = _coll_run()
    assert {mbc.classify(f) for f in findings} == {mbc.CLASS_COLLISION}
    by_change = {f.path.split("/changes/")[1].split("/")[0]: f
                 for f in findings}
    assert sorted(by_change) == ["add-the-basis", "rename-the-basis"]

    added = by_change["add-the-basis"]
    assert added.severity == WARNING
    assert "`## ADDED Requirements` block for" in added.rule
    assert "'Promoted by the unsafe order'" in added.rule
    assert "openspec/specs/coll-cap/spec.md already states" in added.rule

    renamed = by_change["rename-the-basis"]
    assert "`## RENAMED Requirements` `TO:` block for" in renamed.rule
    assert "'Promoted by the unsafe rename order'" in renamed.rule
    # the NEGATIVE control: a lawful rename is silent, and its FROM: title is
    # one canon carries
    assert "lawful-rename" not in {f.path for f in findings}
    assert "Lawful rename source" not in " ".join(f.rule for f in findings)


def test_the_collision_class_reads_a_repository_carrying_no_modified_block():
    """F2 § 3.1's placement, and it is not tidying. The repository most likely
    to hold this evidence is one whose MODIFYING packet has already archived —
    which may leave it with no active `## MODIFIED Requirements` block at all.

    The `-collision` tree is exactly that repository, so the family's
    `if not blocks: continue` guard must not stand in front of this class.
    """
    from conftest import FIXTURES
    root = FIXTURES / "modified-block-currency-collision" / "alphaFactory"
    assert mbc.active_blocks(root) == []
    assert len(_coll_run()) == 2


def test_the_collision_class_carries_its_own_band_and_action():
    """`warning` at launch from its own constant, and an action naming BOTH
    remedies. The action is spelled out rather than compared with the module's
    own copy of it."""
    findings = _coll_run()
    assert {f.severity for f in findings} == {WARNING}
    assert {f.action for f in findings} == {
        "promote nothing further until the collision is resolved, and — where "
        "the requirement genuinely already exists — convert the addition to a "
        "modification declared against canon, or withdraw or re-target the "
        "rename whose `TO:` title canon already carries"}
    assert mbc._COLLISION_SEVERITY == WARNING
