# medxpractice-overlay-boundary Specification

## Purpose
TBD - created by archiving change create-medxpractice-overlay-boundary. Update Purpose after archive.
## Requirements
### Requirement: MedxPractice pins openPractice at one named revision

`MedxPractice` SHALL pin `opensoft/openPractice` at revision
`9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d` and SHALL declare that revision in
`contracts/openpractice-pin.yaml`, which carries top-level `schema_version: 1`
and `kind: medxpractice_openpractice_pin`, and under `pin:` the fields
`repository: opensoft/openPractice`,
`remote: git@github.com:opensoft/openPractice.git`,
`revision: 9526bd9ef27bb6b017c2357ebaf1a24cfe570f0d`,
`submodule_path: openPractice`, `source_path: .` and
`relationship: pinned_upstream_composition`. **The manifest is NESTED, not
flat**: only the two declaration fields sit at the top level and the six pin
fields sit under `pin:`, which is the shape the scenario below reads as
`pin.revision`.

The two repositories' VISIBILITIES DIFFER AND THAT ASYMMETRY IS THE BOUNDARY'S
REASON FOR EXISTING:
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

### Requirement: The aggregation reaches openPractice only through MedxPractice

The xFactory aggregation SHALL reach `openPractice` ONLY through
`MedxPractice`'s nested gitlink, and no direct `xFactories/openPractice`
aggregate entry SHALL exist. This is the act of this change that NO promoted
requirement covers: `domain-descendant-boundary` governs where a DESCENDANT is
placed and how it pins its product, and says nothing about how the aggregation
reaches the PRODUCT itself.

**The relocation's OTHER half is deliberately not obliged here.** As authored
this requirement also swore that the canonical standalone `openPractice`
checkout lives at the projects workspace root rather than inside the aggregation
workspace. Where a checkout sits on a developer's local filesystem is
unverifiable by any remote or by CI — `review/verification-2026-09-03.md` § 9
says so in as many words, and the act's own success criterion is that it leaves
no trace in Git — so obliging it would be a SHALL no reader can settle. It is
recorded instead as a LOCAL CONVENTION at `design.md` Decision 4. What survives
here is the half a remote reading DOES settle, and § 5 of that verification
record settles it.

#### Scenario: The aggregation is asked for openPractice

- **WHEN** the aggregation's `.gitmodules` and `xFactories/` tree are read on
  `opensoft/xFactory`'s `main`
- **THEN** the practice-operations upstream is reached through
  `xFactories/MedxPractice`'s nested `openPractice` gitlink
- **AND** neither carries an `xFactories/openPractice` entry

#### Scenario: The public upstream is still independently addressable

- **WHEN** `opensoft/openPractice` is read on its own remote
- **THEN** it is PUBLIC, its history and tracked content are unchanged by the
  relocation, and it is usable without any Medx checkout
- **AND** the aggregation holds no second copy of it

### Requirement: MedxPractice is aggregated at the cited placement and named by MedxFactory

The xFactory aggregation SHALL carry `MedxPractice` at the placement the cited
delta ratifies, at the gitlink and remote form that delta records, and
MedxFactory SHALL name MedxPractice as the practice-operations composition with
`openPractice` as its pinned public upstream. **THE PLACEMENT IS NOT RATIFIED
HERE AND IT IS NOT RESTATED HERE.** It is governed by the promoted
**A descendant is placed at a ratified placement**
(`openspec/specs/domain-descendant-boundary/spec.md:76-85`) as amended by the
explicit delta the sibling change carries at
`openspec/changes/create-medxchart-overlay-boundary/specs/domain-descendant-boundary/spec.md`,
which ratifies that placement on the 2026-09-03 ruling and names this descendant
among its two realized placements, at the remote form and the gitlink that delta
records. This change CITES that delta and carries none of its own. **The
concrete values — the path, the absolute remote and the gitlink — appear in this
requirement's scenarios ONLY, as EVIDENCE that the cited rule holds of this
descendant today, never as a second statement of the rule itself.**

#### Scenario: The aggregate submodule manifest is inspected

- **WHEN** the xFactory superproject's `.gitmodules` and `xFactories/` tree are
  read
- **THEN** the practice-operations entry is `xFactories/MedxPractice` at
  `git@github.com:opensoft/MedxPractice.git`, containing neither a relative path
  nor a host-absolute local path
- **AND** the recorded gitlink is `d8d73195609df3b567643a7bf1252eac352d9996`,
  equal to `opensoft/MedxPractice`'s own `main`

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

