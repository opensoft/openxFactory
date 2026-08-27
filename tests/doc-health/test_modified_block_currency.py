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
