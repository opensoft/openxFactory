"""Feature `sequenced-after-integrity` (add-sequenced-after-substrate tasks
5.3, 5.5, 5.6): the trust-root-floor doctrine record.

The record is the half of the trust-root requirement openxFactory can hold on its
own: it states the four properties, separates what the neutral substrate asserts
from what only an enrolled repository's envelope and verifier can enforce, cites
the first consumer's walk policy AS THE FIRST INSTANCE rather than as neutral
doctrine, and records the FIRST POST-ADOPTION SWEEP READING with the plain
statement that the reading is ZERO EVIDENCE about any gate's ceiling.

The recorded reading is DATED, not current: the corpus grows, and the re-runnable
sweep — not the paragraph — is the authority. These assertions therefore check
that the reading IS recorded with its date, its figure and its caveat, and never
that it still equals today's sweep.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCTRINE = ROOT / "docs" / "sequenced-after-trust-root-floor.md"
SIBLING = ROOT / "docs" / "scope-globs-trust-root-floor.md"


def _flat() -> str:
    return " ".join(DOCTRINE.read_text(encoding="utf-8").split())


def test_the_doctrine_doc_exists_and_is_lifecycle_stamped():
    assert DOCTRINE.is_file()
    text = DOCTRINE.read_text(encoding="utf-8")
    assert "Status: ratified" in text
    assert "Ratified by: add-sequenced-after-substrate" in text


def test_it_carries_THE_FOUR_TRUST_ROOT_PROPERTIES():
    flat = _flat()
    for phrase in ("Base-read", "Ratification-covered", "Non-author-mutable",
                   "Frozen after ratification"):
        assert phrase in flat, phrase


def test_it_states_the_never_clearable_floor_and_the_no_autonomous_write_rule():
    flat = _flat()
    assert "never-clearable floor member of EVERY repository" in flat
    assert "no autonomous merge SHALL write to it" in flat
    assert "SHALL NOT enable a chain-consuming gate for any non-docs class" in flat


def test_it_separates_what_openxFactory_asserts_from_what_it_does_not():
    flat = _flat()
    assert "What openxFactory asserts, and what it does not" in flat
    assert "openxFactory does **not** enforce" in flat
    # The two halves openxFactory CAN hold.
    assert "--archive-gate" in flat
    assert "no depth ceiling, no fan-out cap and no composition operator" in flat


def test_it_records_that_ABSENCE_IS_NOT_A_ROOT_and_the_cross_check_is_the_consumers():
    flat = _flat()
    assert "SHALL NOT infer root status from the ABSENCE of the field" in flat
    assert "A control that rewards omission is not a control." in flat
    assert "The cross-check is the consumer's to implement" in flat


def test_it_cites_the_consumers_walk_policy_AS_THE_FIRST_INSTANCE_only():
    # Task 5.6: the depth ceiling, the fan-out disposition and the composition
    # operator are the CONSUMING GATE's, declared in the gate's own
    # specification. The consumer's current values are cited, and explicitly NOT
    # adopted as neutral doctrine.
    flat = _flat()
    assert "as the first instance, not adopted as neutral doctrine" in flat
    assert "FOUR hops inclusive of the terminal change" in flat
    assert "INTERSECTION" in flat
    assert ("Raising any gate's ceiling is a specification change with a "
            "recorded disposition") in flat


def test_it_records_the_FIRST_POST_ADOPTION_SWEEP_READING_and_how_to_re_run_it():
    flat = _flat()
    assert "first post-adoption reading, 2026-09-01" in flat.lower()
    assert "validate-sequenced-after.py . --sweep" in flat
    assert "153 change ids" in flat
    assert "deepest declared chain it resolves is 1 hop" in flat
    # ...and the authoring-time reading it replaces is named as what it was.
    assert "zero hops BY CONSTRUCTION" in flat


def test_it_states_plainly_that_the_reading_is_ZERO_EVIDENCE_about_any_ceiling():
    flat = _flat()
    assert "ZERO EVIDENCE ABOUT ANY GATE'S CEILING" in flat.upper()
    assert "remains an UNMEASURED one" in flat


def test_it_is_linked_in_the_README_doc_index_beside_its_sibling():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/sequenced-after-trust-root-floor.md" in readme
    assert "docs/scope-globs-trust-root-floor.md" in readme
    assert (readme.index("docs/scope-globs-trust-root-floor.md")
            < readme.index("docs/sequenced-after-trust-root-floor.md")), (
        "the pair reads in the order the fields were added")


def test_the_sibling_record_is_cross_referenced():
    assert SIBLING.is_file()
    assert "scope-globs-trust-root-floor.md" in _flat()
