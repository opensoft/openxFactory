# document-lifecycle Specification Delta

## ADDED Requirements

### Requirement: A ruling is discharged once
An archived change SHALL be the single discharge of the ruling it carries, and
an archived packet whose spec delta restates the requirement content another
archived packet already ratified SHALL name that packet's change id in its own
`proposal.md`.

This is the neighbour of "Ratified spec deltas reach the promoted
specification", and it is stated separately because the two failures are
invisible to each other. That requirement is unmet when canon is missing what
a ratified delta stated. THIS one is unmet when canon holds exactly what two
independent packets said it should hold — and no comparison against canon can
show it, because canon looks correct. `openspec --strict` validates each
packet's shape in isolation and has no view across packets; the lifecycle
families read headers, and two duplicate discharges both carry impeccable ones.

The instance on record is a NEAR MISS rather than a defect, and the twenty
minutes that made it one are the argument. openxFactory PR #317 and the landed
`2026-08-25-apply-branch-sessions-deltas` both restated the identical 2026-08-01
`add-workbench-branch-sessions` delta — the same git blob — from parallel
sessions. A human closed the second unmerged and recorded why: "One ruling, one
discharge: the landed packet is it."

**NAMING RECORDS LINEAGE, NOT AUTHORITY.** The remedy this corpus prescribes
for an unpromoted delta is a packet that restates the ratified text
BYTE-FAITHFULLY — any edit would be new normative content carried under an old
ratification — so a restatement is lawful and expected. What makes it
traceable, and distinguishes it from a second independent discharge, is that the
restating packet names the packet whose ruling it applies. Naming does not
confer the standing to restate; the ratification that does is the original's,
and a packet claiming standing it lacks is a ratification-citation defect
governed elsewhere in this capability. A packet that restates without naming is
reporting nothing about its own authority — it is leaving the record unable to
tell one ruling from two.

Restatement is judged on CONTENT, not resemblance: identical requirement
bodies, once trailing whitespace is set aside. Revising a requirement is not
restating it, and a rule loose enough to conflate the two would report the
ordinary case of a capability's requirement being rewritten by a later change.

A packet whose own `proposal.md` declares a standing of `draft` or lower is
outside this requirement for the same reason it is outside the promotion
obligation: it claimed no ratification, so it discharged no ruling.

#### Scenario: One ruling reaches the archive twice
- **WHEN** two archived packets carry spec deltas stating the same capability and requirement title with requirement bodies that differ only in trailing whitespace, and neither packet's `proposal.md` names the other's change id
- **THEN** health tooling MUST report the later packet's delta, naming the earlier packet it restates
- **AND** the remedy is to name the restated packet in the proposal or to withdraw the duplicate discharge

#### Scenario: A remedial packet applies a ratified delta
- **WHEN** a packet exists to apply an earlier packet's ratified but unpromoted delta, and restates that delta byte-faithfully
- **THEN** its `proposal.md` MUST name the earlier packet's change id
- **AND** a packet that does so MUST NOT be reported as a duplicate discharge
- **AND** naming the earlier packet MUST NOT be read as establishing that the restating packet had standing to restate

#### Scenario: Two packets independently remedy one gap
- **WHEN** two packets each restate a third packet's ratified delta and each names that third packet, and neither names the other
- **THEN** neither packet's pairing with the original MUST be reported
- **AND** the pairing the two remedials form MUST be reported, one gap having been discharged twice

#### Scenario: A later change revises a requirement
- **WHEN** a later archived change states a requirement title an earlier archived change also stated, with any difference in the requirement body beyond trailing whitespace
- **THEN** the later change is a revision and MUST NOT be reported as a duplicate discharge
