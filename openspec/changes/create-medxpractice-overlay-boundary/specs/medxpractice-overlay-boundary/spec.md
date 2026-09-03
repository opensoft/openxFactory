# medxpractice-overlay-boundary — Spec Delta

**NARROWED 2026-09-03, at ratification, under Brett Heap's decision 2 option 1.**
As authored this file carried three requirements whose bodies restated promoted
`domain-descendant-boundary` in different words: "MedxPractice owns the branded
practice-operations boundary" restated **A domain consumes a neutral product
through a descendant repository** (`openspec/specs/domain-descendant-boundary/spec.md:6-16`)
and **A descendant carries profile, never fork** (`:55-62`); "The upstream
revision is immutable and reviewable" restated **A descendant pins the product
by commit, twice** (`:30-41`) near-verbatim; and "Aggregate and domain
references use MedxPractice" restated **A descendant is placed at a ratified
placement** (`:76-85`). Restating promoted policy in differing words is a defect
under `document-lifecycle`'s **Explicit delta rule**
(`openspec/specs/document-lifecycle/spec.md:149-161`), not a strengthening of
it, so what survives here is only what is MedxPractice-SPECIFIC: the identity of
this pin, the relocation this change performed, and this descendant's placement
CITED from its one writer.

**What this change RELIES ON WITHOUT MODIFYING**, named rather than repeated —
ALL FIVE promoted `domain-descendant-boundary` requirements, each of which
governs MedxPractice on its own terms and none of which this packet amends:
**A domain consumes a neutral product through a descendant repository** (`:6-16`),
**A descendant pins the product by commit, twice** (`:30-41`),
**A descendant carries profile, never fork** (`:55-62`),
**A descendant is placed at a ratified placement** (`:76-85`) as amended by the
delta the sibling carries, and
**A descendant is created on its first profile, not before** (`:103-120`), under
which MedxPractice is a REPORTED EMPTY BOUNDARY (`tasks.md` § 6) rather than
precedent for creating more. **THIS CHANGE CARRIES NO `## MODIFIED Requirements`
BLOCK**: the placement amendment is written once, by
`create-medxpractice-overlay-boundary`'s sibling, at
`openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/spec.md`,
so one requirement has one writer, and this packet is the ratification packet
that cites that delta.

## ADDED Requirements

### Requirement: MedxPractice pins openPractice at one named revision

`MedxPractice` SHALL pin `opensoft/openPractice` at revision
`9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d` and SHALL declare that revision in
`contracts/openpractice-pin.yaml` carrying `schema_version: 1`,
`kind: medxpractice_openpractice_pin`, `repository: opensoft/openPractice`,
`remote: git@github.com:opensoft/openPractice.git`,
`submodule_path: openPractice`, `source_path: .` and
`relationship: pinned_upstream_composition`. The two repositories' VISIBILITIES
DIFFER AND THAT ASYMMETRY IS THE BOUNDARY'S REASON FOR EXISTING:
`opensoft/openPractice` is PUBLIC and `opensoft/MedxPractice` is PRIVATE, so the
branded Medx composition can be held closed over an upstream that stays open,
without forking it. This requirement states the IDENTITY of one pin and says
nothing about the FORM pins take: the twice-pinned obligation, the
`contracts/<product>-pin.yaml` location, the
`<descendant_repo_snake>_<product_snake>_pin` kind grammar, the
`relationship:` field and the same-commit discipline are all stated once by the
promoted **A descendant pins the product by commit, twice**
(`openspec/specs/domain-descendant-boundary/spec.md:30-41`), which this change
relies on and does not restate.

#### Scenario: The declared pin and the gitlink are read

- **WHEN** `MedxPractice` is checked out at `d8d73195609df3b567643a7bf1252eac352d9996`
- **THEN** its nested `openPractice` gitlink reads
  `9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`
- **AND** `contracts/openpractice-pin.yaml`'s `pin.revision` reads the same
  commit, in the same manifest shape this requirement names

#### Scenario: The public upstream advances past the pinned revision

- **WHEN** `opensoft/openPractice`'s `main` moves ahead of the pinned revision —
  as it has, reading `0ec9fca72ecf493e2520e676387f0c3f327cc6e6`, two commits
  ahead, on 2026-09-03
- **THEN** the MedxPractice composition remains at
  `9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d` and no moving branch reference
  advances it
- **AND** moving it is a deliberate re-pin performed under the cited promoted
  same-commit rule, never a consequence of the upstream having moved

### Requirement: The standalone openPractice checkout lives outside the aggregation workspace

The canonical standalone `openPractice` checkout SHALL live at the projects
workspace root rather than inside the xFactory aggregation workspace, with its
own Git history, origin and tracked content unchanged by the relocation, and the
aggregation SHALL reach openPractice ONLY through `MedxPractice`'s nested
gitlink rather than through a second checkout of its own. This is the act of
this change that NO promoted requirement covers:
`domain-descendant-boundary` governs where a DESCENDANT is placed and how it
pins its product, and says nothing about where the PRODUCT's own standalone
checkout lives.

#### Scenario: The relocated upstream is inspected

- **WHEN** `openPractice` is opened from its workspace-root location
- **THEN** its origin is `opensoft/openPractice` and its history and tracked
  content are unchanged by the move
- **AND** it remains independently usable without any Medx checkout

#### Scenario: The aggregation is asked for openPractice

- **WHEN** the xFactory aggregation resolves the practice-operations upstream
- **THEN** it reaches it through `xFactories/MedxPractice`'s nested
  `openPractice` gitlink
- **AND** no direct `xFactories/openPractice` aggregate entry exists

### Requirement: MedxPractice is aggregated at the cited xFactories placement

The xFactory aggregation SHALL carry `MedxPractice` at
`xFactories/MedxPractice`, with the ABSOLUTE
`git@github.com:opensoft/MedxPractice.git` remote its sibling submodules use and
the gitlink `d8d73195609df3b567643a7bf1252eac352d9996`, and MedxFactory SHALL
name MedxPractice as the practice-operations composition with `openPractice` as
its pinned public upstream. **THE PLACEMENT IS NOT RATIFIED HERE AND IS NOT
RESTATED HERE.** The `xFactories/` placement is governed by the promoted
**A descendant is placed at a ratified placement**
(`openspec/specs/domain-descendant-boundary/spec.md:76-85`) as amended by the
explicit delta the sibling change carries at
`openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/spec.md`,
which ratifies that placement on the 2026-09-03 ruling and names
`xFactories/MedxPractice` at this exact gitlink among its two realized
placements. This change CITES that delta and carries none of its own.

#### Scenario: The aggregate submodule manifest is inspected

- **WHEN** the xFactory superproject's `.gitmodules` and `xFactories/` tree are
  read
- **THEN** the practice-operations entry is `xFactories/MedxPractice` at
  `git@github.com:opensoft/MedxPractice.git`, containing neither a relative path
  nor a host-absolute local path
- **AND** the recorded gitlink equals `opensoft/MedxPractice`'s own `main`

#### Scenario: A reader asks what ratifies this placement

- **WHEN** a reader asks on what authority `xFactories/MedxPractice` is a
  permitted placement
- **THEN** the answer is the promoted placement requirement as amended by
  `create-medxchart-overlay-boundary`'s delta, which this change names by path
- **AND** this change states no second version of that rule, so the two Medx
  packets can never disagree about it

#### Scenario: MedxFactory names the branded dependency

- **WHEN** MedxFactory's stack orientation is read
- **THEN** it names MedxPractice as the practice-operations composition and
  identifies openPractice as its pinned public upstream
