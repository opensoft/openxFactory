# document-lifecycle

## ADDED Requirements

### Requirement: A promoted specification carries a written Purpose, repaired in the promoted specification
A promoted `openspec/specs/<capability>/spec.md` SHALL carry a `## Purpose`
that a human wrote, and SHALL NOT carry the placeholder sentence the archive
act itself writes when it creates a capability — `TBD - created by archiving
change <X>. Update Purpose after archive.` — nor a bare `TBD`/`TODO` left in
its place; where such a placeholder is found, the repair SHALL be made in the
promoted specification directly and SHALL NOT be attempted through a spec
delta.

**THE PLACEHOLDER IS WRITTEN BY THE TOOL, NOT BY AN AUTHOR, AND NOTHING WAS
ASKING FOR IT BACK.** `openspec archive` creates a new capability's promoted
spec with that sentence in the Purpose slot and an instruction to replace it
after archiving. The instruction is addressed to nobody in particular, arrives
at the moment the packet's author is finished, and had gone undischarged on 39
of this corpus's promoted specifications when they were counted on 2026-09-05.
A capability whose Purpose says only that it was created by archiving tells a
reader nothing the directory name did not.

**AND THE REPAIR CANNOT BE MADE THE WAY EVERY OTHER SPEC EDIT IS MADE**, which
is why this is worth stating rather than leaving to habit. A `## Purpose` in a
change's spec delta is read ONLY when the capability is created; on any later
archive it is ignored. So an author who follows the corpus's ordinary reflex —
write a delta, ratify it, archive it — produces a packet that validates, that
archives, and that changes nothing, and the placeholder survives the ceremony
intact. The promoted specification is the only surface where the edit lands.

A Purpose SHALL say what the capability is FOR. It is prose ABOUT the
capability and carries no SHALL, so it is not a canon unit: replacing a
placeholder removes nothing from canon and owes no `Removed from canon by`
marker.

#### Scenario: A capability is archived and its Purpose is never written
- **WHEN** a promoted specification's `## Purpose` still carries the sentence the archive act writes, or a bare `TBD`/`TODO` in its place
- **THEN** the specification does not satisfy this requirement
- **AND** the defect is the promoted specification's, not the archiving change's, and is repaired wherever it is found rather than by reopening that change

#### Scenario: The repair is attempted through a delta
- **WHEN** a change proposes a `## Purpose` in a spec delta over a capability that already exists
- **THEN** that Purpose is read by nothing at archive time and the placeholder survives
- **AND** the conformant repair is an edit to the promoted `openspec/specs/<capability>/spec.md` itself

#### Scenario: A Purpose is replaced
- **WHEN** a placeholder Purpose is replaced by written prose
- **THEN** no requirement, scenario, or lifecycle status is altered by that edit
- **AND** no canon unit leaves the specification, so no `Removed from canon by` marker is owed
