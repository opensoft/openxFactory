# review-authority-intake Specification

Deltas here are declared RELATIVE TO the OUTCOME of the active change
`add-wallet-carried-review-authority`: `review-authority-intake` is NOT in
`openspec/specs/`, and the three requirements below are among that change's
twelve `ADDED` requirements. Per
`openspec/specs/release-realization/spec.md:64-79`'s ordered-delta rule each
delta references that change and restates the target requirement's full text as
that change will promote it, plus this change's modification — applied by PARITY
rather than by the rule's letter, since these requirements are ADDED rather than
already MODIFIED, and the parity is declared rather than implied.

Three modifications, all of them dangling wallet references that
`split-openxwallet-repo` would otherwise leave unresolved. The named target is
the reader requirement, whose scenario becomes UNSATISFIABLE after P3 because the
validator is no longer present in this repository at all; the rewrite from
"present" to "reachable … in-tree or through a digest-pinned submodule"
STRENGTHENS the rule rather than narrowing it, since the pin's digest is what
makes "which reader ran" auditable. The other two carry the same delta's V12
extension: the three citations at this spec's `:10`, `:15` and `:208` resolve
into paths that leave this repository, and `:10`/`:15` sit inside *Review
authority is held as an openxwallet grant and by nothing else* while `:208` sits
inside *A reviewing holder's composition is pinned…*, so both requirements are
restated with their citations repointed. What does NOT change in any of the
three: the register's location, its human-only floor, or the fact that it is
`openxFactory`'s own review authority.

## MODIFIED Requirements

_Declared relative to `add-wallet-carried-review-authority`'s ADDED text (parity with `release-realization`'s ordered-delta rule, as the proposal states)._

### Requirement: A grant with no reader in a required check confers nothing
A review-authority grant SHALL confer no authority until a named validator that
reads it — whether in-tree or REACHABLE THROUGH A DIGEST-PINNED SUBMODULE, in
which case the pin's digest is what makes WHICH READER RAN auditable — runs as a
REQUIRED check on the repository that holds the register, and
until that check is required an intake entry SHALL be treated as documentation
that confers nothing; the capability SHALL NOT describe the validator's rules as
though the description were the enforcement, and any statement of what the
intake enforces SHALL name the check that enforces it.

#### Scenario: The validator exists but no workflow runs it
- **WHEN** `scripts/validate-openxwallet.py` (or the register's own validator) is reachable in the repository, in-tree or through a digest-pinned submodule, but appears in no workflow that is a required check
- **THEN** every grant in the register confers nothing, and the intake states so rather than asserting the grants' properties in the present tense

#### Scenario: A described control is not an existing one
- **WHEN** a requirement of this capability is stated as satisfied by a rule inside a validator
- **THEN** the statement MUST name the required check under which that validator executes
- **AND** where no such check exists the requirement is UNMET, not partially met

#### Scenario: The reader runs as the pinned tool from the register-holding repository's root
- **WHEN** the reader is invoked as `python3 openXwallet/scripts/validate-openxwallet.py .` from the `openxFactory` root, under a required check, at the digest recorded in `contracts/openxwallet-pin.yaml`
- **THEN** the grants under `governance/review-authority/` are read and this requirement is SATISFIED, because a digest-pinned reader running as a required check over the tree that holds the register is exactly what it asks for
- **AND** the pin's digest is what makes "which reader ran" an audit fact rather than an assumption

#### Scenario: A malformed register row turns the pull request red
- **WHEN** a deliberately malformed row is placed under `openxFactory`'s `governance/review-authority/`
- **THEN** the required consumer check fails that pull request
- **AND** until that red proof exists the requirement is UNMET rather than partially met, and the proof discharges in the repository that HOLDS the register, never in the product repository whose tree has no register for a malformed row to sit in

_Declared relative to `add-wallet-carried-review-authority`'s ADDED text (parity with `release-realization`'s ordered-delta rule, as the proposal states)._

### Requirement: Review authority is held as an openxwallet grant and by nothing else
A holder SHALL exercise review authority over a governed object only under an
`xfactory_wallet_grant` whose `audience.wallet_ref` names that holder's wallet,
whose `scope.acts` names the review act, whose `scope.objects` names the object,
and whose `scope.authority_tier` is drawn from the closed ladder in
`openxwallet-custody.registry.yaml:15-37`, consumed from `opensoft/openXwallet`
at the pin recorded in `contracts/openxwallet-pin.yaml` — the tiers themselves
(`attest`, `request`, `act`, `act_unsupervised`) are unchanged bytes at the named
carve commit; no review
authority SHALL be conferred by an ownership label, a `CODEOWNERS` entry, a role
name, a seat assignment, or any other declaration outside a grant, and this
capability SHALL NOT define a second authority vocabulary — an authority word
that is not a `scope.authority_tier` value is a validation failure per
`openspec/specs/openxwallet-agent-profile/spec.md:50-69`, read in openXwallet's
own OpenSpec instance at that same pin.

#### Scenario: A seat without a grant holds nothing
- **WHEN** a reviewing seat is named in a council definition but no active grant names its wallet as audience over the candidate's objects
- **THEN** the seat holds no review authority over that candidate
- **AND** the seat assignment alone MUST NOT be read as conferring any

#### Scenario: A parallel authority word is refused
- **WHEN** an intake entry declares a reviewing holder's standing with a word outside the `authority_tier` ladder
- **THEN** the entry is refused as a parallel authority vocabulary

#### Scenario: Ownership is not standing
- **WHEN** a holder is recorded as the owner of a path, an artifact, or a repository
- **THEN** that record confers no review authority, consistent with `openspec/specs/client-infrastructure-liaison/spec.md:18-30`

#### Scenario: The authority-tier ladder is cited after the capability exits this corpus
- **WHEN** this capability's authority vocabulary is checked against the closed `authority_tier` ladder
- **THEN** the ladder resolves through `contracts/openxwallet-pin.yaml` to the pinned openXwallet checkout, never to a path in this repository
- **AND** an uninitialized checkout or a custody-registry digest disagreeing with the pin refuses the check rather than admitting an unladdered authority word

_Declared relative to `add-wallet-carried-review-authority`'s ADDED text (parity with `release-realization`'s ordered-delta rule, as the proposal states)._

### Requirement: A reviewing holder's composition is pinned, and a composition roll is a governed re-issuance
A reviewing holder's declared composition SHALL pin its model version and its
prompt corpus as declared components, and SHALL NOT declare the candidate
repository at HEAD as its retrieval corpus, so that a provider alias roll becomes
a GOVERNED RE-ISSUANCE EVENT with a named runbook rather than a silent
fleet-wide revocation; the capability SHALL record that
`openspec/specs/openxwallet-agent-profile/spec.md:27-48`, read in openXwallet's
own OpenSpec instance at the pin recorded in `contracts/openxwallet-pin.yaml`,
revokes on any single
component change with no tolerance band and no grace period, and that under
`missing_required_seat: refused` a fleet-wide revocation parks every in-flight
convening, whose only routine exit under a sole code owner is the `--admin`
bypass this change exists to make unnecessary.

#### Scenario: A provider rolls a model alias
- **WHEN** a hosted holder's model version moves under an unpinned alias
- **THEN** the composition hash moves and every outstanding grant to that holder is revoked at once
- **AND** the intake requires the pin precisely so this is a scheduled re-issuance rather than an unannounced outage

#### Scenario: The retrieval corpus is declared as the candidate repository
- **WHEN** a reviewing holder declares its retrieval corpus as the repository under review at HEAD
- **THEN** the declaration is refused — every candidate commit would revoke the reviewer
