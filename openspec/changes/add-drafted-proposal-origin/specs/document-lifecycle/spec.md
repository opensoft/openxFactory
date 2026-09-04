# document-lifecycle Specification Delta

## MODIFIED Requirements

### Requirement: Proposal origin declaration
Every OpenSpec change proposal SHALL declare exactly one origin in its
`.openspec.yaml`. The origin's IDENTITY — `kind`, `id`, and for a staged
origin `path` — is fixed when the proposal is created and unchanged for the
life of the change; that identity is what the support manifest repeats and
what a disagreement reports as post-ratification mutation. A `staged` origin
carries `kind: staged`, a durable
`id` of the form `<repo>:staging:<topic-slug>`, and a `path` naming the
original repository-relative staging folder; at the proposal transition the
staged folder MUST contain a document whose `Staging ID:` equals
`origin.id`. An `ad_hoc` origin carries `kind: ad_hoc`, a durable `id` of
the form `<repo>:adhoc:<date>-<sequence-or-slug>`, a required `reason`, and
EITHER approval provenance (`approved_by` and `approved_on`) OR drafting
provenance (`proposed_by` and `proposed_on`) — one of the two pairs in full,
never neither and never half of one. An APPROVED ad-hoc origin is an
explicit,
approved exception — it MUST NOT substitute for staging when organized
source material exists, and a proposal MUST NOT declare both origin kinds.
Durable ids remain valid after the staging folder moves, is compressed, or
is removed; `origin.path` is the historical record of the transition
source, not a live link.

**AN UNAPPROVED PROPOSAL SHALL BE EXPRESSIBLE.** An ad-hoc origin declaring
`proposed_by` and `proposed_on` in place of the approval pair declares
provenance WITHOUT asserting approval: a lawful state of the record, not a
defect awaiting one. The state exists because this corpus produces it
deliberately — a "scout and draft, do not implement" assignment is supposed
to yield a packet that exists, validates, and is not yet approved — and
because before it existed the only shapes available to such a packet were an
ad-hoc origin missing its required approval date, or no origin block at all.
Both were reported, so the only mechanical ways to clear the report were to
approve the change, delete the draft, or write an approval date nobody gave.
Inventing that date is the defect the approval fields exist to prevent, and a
rule whose only remedy is the defect it forbids is a rule that trains its
readers to disbelieve the checker.

**APPROVAL IS AN ADDITION, NEVER A REWRITE.** When an unapproved origin is
approved, the approval pair SHALL be added to the declared origin and the
identity SHALL NOT move: the durable id minted at drafting remains the
durable id after approval, so no manifest that repeats it comes to disagree
with the packet, and the addition MUST NOT be read as mutation of a fixed
origin. The drafting pair MAY remain beside the approval, and normally
should: it is the record of who drafted the proposal and when, which the
approval does not restate.

**APPROVAL SHALL APPEAR WHEN A STATUS CLAIMS IT.** A proposal whose own
`Status:` declares `ratified`, or any standing beyond it, SHALL carry
approval provenance in its origin. A proposal that declares such a standing
while its origin asserts no approval is a defect in the record, and its
lawful remedies are exactly two: record the approval provenance the status
claims, or return the proposal to a pre-ratification standing. Writing an
approval date the record does not carry is not a third remedy. The
unapproved state relaxes WHEN approval must be recorded; it does not relax
WHETHER a ratified proposal was approved, and it MUST NOT be entered to
quiet a check on a proposal that claims ratification.

#### Scenario: A staged proposal is created
- **WHEN** an OpenSpec change is created from a staged topic
- **THEN** its `.openspec.yaml` MUST declare `kind: staged` with the topic's durable id and original staging path
- **AND** the staged folder MUST contain, at transition, a document whose `Staging ID:` equals the declared id

#### Scenario: An ad-hoc proposal is created
- **WHEN** an OpenSpec change is deliberately created without a staging source, and its creation is approved
- **THEN** its `.openspec.yaml` MUST declare `kind: ad_hoc` with a durable id, the reason, the approving authority, and the approval date
- **AND** supporting evidence MAY still live under `supporting-docs/` but MUST NOT claim a fabricated staging source

#### Scenario: An unapproved proposal is drafted
- **WHEN** an OpenSpec change is deliberately created without a staging source and no approval act exists yet
- **THEN** its `.openspec.yaml` MUST declare `kind: ad_hoc` with a durable id, the reason, `proposed_by`, and `proposed_on`
- **AND** it MUST NOT carry an approval date no authority gave
- **AND** the origin MUST NOT be reported as incomplete for lacking the approval pair

#### Scenario: An unapproved origin is later approved
- **WHEN** an authority approves a proposal whose origin declared drafting provenance
- **THEN** `approved_by` and `approved_on` MUST be added to the declared origin
- **AND** `kind`, `id`, and `path` MUST remain exactly as declared at drafting
- **AND** the addition MUST NOT be reported as mutation of a fixed origin

#### Scenario: A proposal claims a ratification its origin does not carry
- **WHEN** a proposal's `Status:` declares `ratified` or beyond while its origin carries drafting provenance and no approval
- **THEN** health tooling MUST report it
- **AND** the remedy is to record the approval provenance or to return the proposal to a pre-ratification standing, never to invent an approval date

#### Scenario: The proposal gate rejects a malformed origin
- **WHEN** a proposal's origin is missing, declares an unknown kind, declares both kinds, carries a staged id or path that does not resolve before transition, disagrees with the staging header or support manifest, lacks ad-hoc reason, declares neither approval nor drafting provenance, or completes only half of the pair it declares
- **THEN** strict proposal validation MUST fail

#### Scenario: The staging folder later disappears
- **WHEN** a declared staged origin's topic folder moves, is compressed, or is removed after the proposal transition
- **THEN** the origin id and path remain unchanged as historical provenance and MUST NOT be rewritten to track the new location
