# document-lifecycle Specification Delta

## ADDED Requirements

### Requirement: Ratified spec deltas reach the promoted specification
A ratified spec delta SHALL be applied to its promoted
`openspec/specs/<capability>/spec.md` when its change archives, and a
requirement it ADDED or MODIFIED — the requirement itself and every scenario
the delta states under it — SHALL be present in that promoted spec
thereafter; a requirement it REMOVED SHALL be absent.

This is the obligation the archive act has always carried and that nothing
stated. `openspec --strict` validates a delta's SHAPE, never its ARRIVAL, and
the four lifecycle families this capability governs read a packet's headers,
never its bodies — so a ratified requirement could archive and silently never
reach canon while every check reported the corpus healthy.
`docs/archive-record-discrepancies.md` records the instance under FU-DOM-CODEX:
codexFactory's archived `2026-08-08-activate-nightly-sweep-council-clearance`
ratified a MODIFIED requirement carrying six scenarios, the promoted
`merge-master-approval` spec carried the title with two, and the archive commit
never touched that file.

**A delta is held to this only where its own proposal claims ratification.**
The obligation attaches to a claim of approval, so where a packet's
`proposal.md` carries a `Status:` other than `ratified` — or carries none —
its spec deltas are archived design evidence rather than promoted canon, and
this requirement says nothing about them. That is not a new marker invented
for the rule: it is the header the corpus already carries, and
`docs/archive-record-discrepancies.md` C5 is the case it reads.
`2026-06-26-enable-live-openxfactory` was archived with `--skip-specs`,
deliberately retaining four spec deltas as design evidence, and its 2026-08-23
supersession addendum backfilled exactly one line onto it to say so in this
capability's own vocabulary — `Status: draft`, "the honest value this folder
has always supported: never ratified".

**The authority for a requirement is the MOST RECENT archived delta that
touches it, and that one alone.** A ratified change may legitimately rewrite,
rename, or remove what an earlier ratified change stated, and canon carrying
the later text is canon being correct rather than canon drifting. Ordering is
by the archive folder's date; where two archived changes share a date, the
later ARCHIVE ACT is the later statement. A `RENAMED` block retires the title
it names, because `openspec archive` applies RENAMED before MODIFIED.

#### Scenario: A ratified delta never reaches canon
- **WHEN** an archived change whose `proposal.md` reads `Status: ratified` carries a spec delta ADDING or MODIFYING a requirement
- **THEN** the promoted `openspec/specs/<capability>/spec.md` MUST carry that requirement by title, and MUST carry every scenario the delta states under it
- **AND** where it does not, health tooling MUST report the gap against the archived delta's own path, naming the promoted spec it failed to reach

#### Scenario: A ratified delta removes a requirement
- **WHEN** an archived ratified change carries a `## REMOVED Requirements` delta
- **THEN** the promoted spec MUST NOT carry that requirement thereafter
- **AND** a requirement still present after its ratified removal MUST be reported

#### Scenario: A deliberate non-promotion is recorded
- **WHEN** a change is archived without promoting its spec deltas, and its own `proposal.md` carries a status other than `ratified`
- **THEN** its deltas are archived design evidence and MUST NOT be reported as unpromoted
- **AND** the recorded status is what makes the non-promotion deliberate — a label, a title, or a claim in prose MUST NOT be read as one

#### Scenario: A later ratified change supersedes an earlier delta
- **WHEN** more than one archived ratified change carries a delta touching the same capability and requirement title
- **THEN** only the most recent one SHALL be checked against canon, ordered by archive date and, on a shared date, by the later archive act
- **AND** a requirement title retired by a later `RENAMED` block MUST NOT be reported as missing from canon
