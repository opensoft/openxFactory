"""The twenty-second deterministic family: currency of an active change's
`## MODIFIED Requirements` blocks (`add-modified-block-currency-check`).

WHAT IT ANSWERS. OpenSpec's `MODIFIED` REPLACES a requirement wholesale; it does
not merge. So whatever a MODIFIED block says is what canon says after the
archive act, and every clause and scenario the block does not restate is deleted
silently. `openspec validate --strict` checks a delta's SHAPE — the heading, the
keyword on the first line, at least one scenario — and never what promotion will
do to the requirement being replaced.

THE CLASS IS NOT HYPOTHETICAL. It happened four times in this repository in one
week and a human caught it every time. `add-doxchat-model-intake` (issue #351)
was holding the deletion of six body clauses, two scenarios and one REVERTED
scenario line, with `validate --strict` green throughout; and
`add-release-inventory-drift-check`, `add-promotion-fidelity-check` and
`add-duplicate-packet-check` each restated ONE of the eight scenarios of
`doc-health`'s own "Deterministic check families" (issue #329).

THE DEFECT IS A FUNCTION OF TIME, NOT OF CARE. #351's block was written on
2026-08-21 against a pre-`02a71d6e` canon and was correct when written. Canon
moved; nothing re-read the block; four days later it was holding a nine-item
deletion. Issue #357 states the gap in the sentence this family exists to
retire: "a long-lived active change that MODIFIES a requirement goes stale as
canon moves".

COUNTING CANNOT SEE IT. The `add-release-inventory-drift-check` case nearly
escaped because the FILE-LEVEL scenario count did not move: that change's own
ADDED requirement brought seven scenarios and its MODIFIED block was about to
drop seven, so `doc-health/spec.md` read 98 -> 98. Only per-requirement
accounting shows it.

AND THE FAMILY WHOSE WHOLE JOB IS DELTA-VERSUS-SPEC FIDELITY IS STRUCTURALLY
BLIND TO IT (#330). `promotion_fidelity` compares an ARCHIVED delta to the
promoted spec, and after the archive act canon IS the delta — a block that
dropped seven scenarios and a canon now missing them agree perfectly. The
comparison that can see the loss is between an ACTIVE delta and the canon it has
not yet replaced: a different document pair, read at a different moment, which
is why this is a separate family rather than a wider reading of that one.

THREE ARMS, FOUR FINDING CLASSES, AND THE NUMBERS DIFFER ON PURPOSE:

1. **Scenario-title completeness** (`_LAUNCH_SEVERITY`, `warning`). Every
   `#### Scenario:` title canon carries must appear as a scenario title in the
   block. Short titled strings rather than prose, reporting deletion at the
   granularity the defect occurs at. THIS is the arm that carries the family's
   gate, and the only arm the flip in `tasks.md` § 7.2 moves.
2. **The carriage ledger** (`_LEDGER_SEVERITY`, `info`). Every body unit and
   every scenario bullet the block does not carry, as AT MOST ONE finding per
   requirement. It CANNOT distinguish a deliberate rewording from stale text and
   its rule text says so: it is the list a reviewer reads to confirm each
   divergence was intended.
3. **Title resolution and ordering** (`_RESOLUTION_SEVERITY`, `warning`). A
   block whose title resolves to nothing, and an ordering between two active
   RATIFIED writers that no declaration settles.
4. **Marker defects** (`_LEDGER_SEVERITY`, `info`) — not an arm. A marker that
   names a unit the block still carries declares nothing and is reported itself.
   It does NOT inherit the ledger's hedge, because a marker naming a carried
   unit is wrong with certainty.

MATCHING IS SAME-KIND AND EXACT, and both halves of that are load-bearing.
CONTAINMENT IS FORBIDDEN: canon's bullet `**THEN** the selector MUST show
exactly the available catalog entries and their data-handling badges` is a
SUBSTRING of the widened line `add-doxchat-model-intake` replaced it with, so a
containment rule reports nothing on the very defect PR #358 had to repair by
hand. SIMILARITY IS FORBIDDEN TOO: a threshold high enough to pass an ordinary
reword also passes a clause whose meaning has been REVERSED, and #351's ninth
item was exactly that. And normalization stops at whitespace — see `normalize`,
which is deliberately NOT `promotion_fidelity.norm`.

CLASSIFICATION AT LAUNCH IS ADVISORY IN BOTH HALVES: `warning`/`info`
severities, AND deliberate absence from `families.FAMILY_RESOLUTION`. The second
half is the one that is easy to lose — `report.uncited_resolutions` turns a
`contested` finding that VANISHES between reports into an `error`, so a
`contested` advisory family reds the nightly the first time anyone corrects a
block, which is enforcement through the back door on the run that proves the
launch worked. Both halves flip together, by ruling, on the discharge of a
measured population.

THIS MODULE READS THE CHECKED-OUT TREE AND NOTHING ELSE. The live-`main` basis
`promotion_fidelity` carries is ruled for that family alone and would be
actively wrong here: an active change lives on a branch, so a family reading
`main` would measure a delta `main` does not carry against canon the branch may
have moved.
"""

from __future__ import annotations

from . import INFO, WARNING

FAMILY = "modified-block-currency"

# THE SEVERITIES, THREE OF THEM, NAMED APART ON PURPOSE.
#
# `_LAUNCH_SEVERITY` is the identifier `promotion_fidelity`, `duplicate_packet`
# and `family_enumeration` all carry, and it is the grep that ties every reader
# of a launch decision together. Here it belongs to the SCENARIO-TITLE arm,
# because that is the one arm the flip reserved in
# `add-modified-block-currency-check` tasks.md § 7.2 moves — raising it to
# `error` AND adding the `contested` classification, together, in one commit,
# after the standing population is discharged.
#
# The other two are separate constants precisely so that flip cannot drag them.
# A single shared constant would take the title-resolution arm to `error` at the
# same time, which no ruling asked for; and the carriage ledger has NO flip
# proposed at all, its population being standing by construction — every
# legitimate MODIFIED block edits something, so an editorial band is the honest
# launch state and a permanent yellow row for a condition nobody should act on
# is how a report stops being read.
_LAUNCH_SEVERITY = WARNING
_RESOLUTION_SEVERITY = WARNING
_LEDGER_SEVERITY = INFO

# The two document sets, and there is no third. `archive/` is excluded by the
# reader rather than by the glob, because a glob that happened to match an
# archived path would be a silent widening of this family's scope.
DELTA_GLOB = "openspec/changes/*/specs/*/spec.md"
CANON_TEMPLATE = "openspec/specs/{capability}/spec.md"

_ACTION = ("restate the requirement as canon currently states it, or declare "
           "the deletion with a `Removed from canon by` marker")
