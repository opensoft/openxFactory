# domain-descendant-boundary — Spec Delta

The promoted `domain-descendant-boundary` requirement below carries the
`xFactories/` placement as **REALIZED BUT NOT YET RATIFIED**, names THIS change
as the establishing act that would settle it, and states in its own scenario
that when this change archives the requirement "is amended by an explicit delta
to say so rather than by re-reading". This file IS that explicit delta. It is
carried by `create-medxchart-overlay-boundary` and by no other packet: the
sibling `create-medxpractice-overlay-boundary` cites this delta and carries
none of its own, so one requirement has one writer.

## MODIFIED Requirements

### Requirement: A descendant is placed at a ratified placement
A descendant SHALL be aggregated at one of exactly two placements, whose STANDING
differs and SHALL be stated rather than blended, and it MAY carry both.
**RATIFIED:** nested into its DomainxFactory as a submodule (`MedxAvatar` in
`MedxFactory`, DTN-022, 2026-08-03). **RATIFIED 2026-09-03:** the aggregation's
`xFactories/`, realized 2026-08-23 and ratified by its establishing act
`create-medxchart-overlay-boundary` on Brett Heap's in-session ruling of
2026-09-03, whose REALIZED placements are BOTH `xFactories/MedxChart` (gitlink
`68d2f1f5db932cb5099ceac75dab66316ef22579`) and `xFactories/MedxPractice`
(gitlink `d8d73195609df3b567643a7bf1252eac352d9996`), each entered in
`opensoft/xFactory`'s `.gitmodules` at its own `git@github.com:opensoft/` remote
rather than at a relative URL. The choice between
them is the owning domain's, on whether the descendant needs standalone cloning.
A third placement SHALL NOT be used until a change ratifies it. What this
ratification settles is the PLACEMENT and nothing beside it: a placement being
ratified SHALL NOT be read as ratifying the CREATION of a descendant, which the
lazy-creation requirement below governs on its own terms, and both `xFactories/`
descendants are REPORTED EMPTY BOUNDARIES under that requirement rather than
precedent for creating more.

**Removed from canon by create-medxchart-overlay-boundary (2026-09-03):** ``**REALIZED BUT NOT YET RATIFIED:** the aggregation's `xFactories/` (`MedxChart`, 2026-08-23, whose establishing act `create-medxchart-overlay-boundary` is still `Status: draft`) — permitted here, and confirmed as ratified precedent when that change archives.``; ``**THEN** the placement is permitted, AND its standing is recorded as REALIZED-but-not-yet-ratified until `create-medxchart-overlay-boundary` archives``; ``**THEN** the `xFactories/` placement becomes ratified precedent, and this requirement is amended by an explicit delta to say so rather than by re-reading`` — all three units named the pending condition this ratification discharges, and the amendment the third of them deferred to the archive act is this block.

#### Scenario: A descendant is placed under the aggregation's xFactories/
- **WHEN** a descendant is aggregated at `xFactories/<Descendant>`
- **THEN** the placement is permitted, AND its standing is recorded as RATIFIED, on the 2026-09-03 ratification of `create-medxchart-overlay-boundary`

#### Scenario: The draft establishing act archives
- **WHEN** `create-medxchart-overlay-boundary` archives
- **THEN** the explicit delta this requirement asked for has ALREADY been written, is this block, and promotes with the archive rather than being derived by re-reading
- **AND** the establishing act is no longer a draft, having been ratified 2026-09-03 before its archive gate opened

#### Scenario: A third placement is proposed
- **WHEN** a descendant is placed anywhere other than nested in its DomainxFactory or under the aggregation's `xFactories/`
- **THEN** the placement is refused until a change ratifies it

#### Scenario: A descendant carries both placements
- **WHEN** a descendant needs standalone cloning AND presence in its domain tree
- **THEN** it MAY carry both gitlinks, AND the two gitlinks SHALL name the same commit, so that "which checkout was read" has one answer
