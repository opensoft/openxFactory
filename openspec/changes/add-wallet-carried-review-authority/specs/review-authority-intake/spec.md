# review-authority-intake Specification

## ADDED Requirements

### Requirement: Review authority is held as an openxwallet grant and by nothing else
A holder SHALL exercise review authority over a governed object only under an
`xfactory_wallet_grant` whose `audience.wallet_ref` names that holder's wallet,
whose `scope.acts` names the review act, whose `scope.objects` names the object,
and whose `scope.authority_tier` is drawn from the closed ladder in
`contracts/openxwallet/openxwallet-custody.registry.yaml:15-37`; no review
authority SHALL be conferred by an ownership label, a `CODEOWNERS` entry, a role
name, a seat assignment, or any other declaration outside a grant, and this
capability SHALL NOT define a second authority vocabulary — an authority word
that is not a `scope.authority_tier` value is a validation failure per
`openspec/specs/openxwallet-agent-profile/spec.md:50-69`.

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

### Requirement: A grant with no reader in a required check confers nothing
A review-authority grant SHALL confer no authority until a named validator that
reads it runs as a REQUIRED check on the repository that holds the register, and
until that check is required an intake entry SHALL be treated as documentation
that confers nothing; the capability SHALL NOT describe the validator's rules as
though the description were the enforcement, and any statement of what the
intake enforces SHALL name the check that enforces it.

#### Scenario: The validator exists but no workflow runs it
- **WHEN** `scripts/validate-openxwallet.py` (or the register's own validator) is present in the repository but appears in no workflow that is a required check
- **THEN** every grant in the register confers nothing, and the intake states so rather than asserting the grants' properties in the present tense

#### Scenario: A described control is not an existing one
- **WHEN** a requirement of this capability is stated as satisfied by a rule inside a validator
- **THEN** the statement MUST name the required check under which that validator executes
- **AND** where no such check exists the requirement is UNMET, not partially met

### Requirement: The register and the reader are ratified together
The intake register and a validator that reads it SHALL land in one change, and
this capability SHALL NOT be treated as realized by a register alone; the
register's first shape SHALL be minimal and named — one file at a fixed path in
`openxFactory`, one holder (codexFactory's `merge_readiness_council` as a body),
one target repository, one review act, `authority_tier: act`, one `expires_at` —
and the validator's only obligation at that shape SHALL be to fail a convening
that admits a holder carrying no active row.

#### Scenario: A register lands without its reader
- **WHEN** a change adds the intake register and defers the validator to a successor
- **THEN** the change does not realize this capability and MUST NOT be archived as realizing it

#### Scenario: The minimal shape is exceeded
- **WHEN** a first-shape register declares more than one holder, more than one target repository, or per-seat grants
- **THEN** the additional scope is a named successor rather than part of the first shape

#### Scenario: The reader's single obligation is exercised
- **WHEN** a convening admits a holder for which the register carries no active row
- **THEN** the validator fails the check and the convening is refused

### Requirement: The intake register is a permanently human-only surface
The intake register SHALL be declared a permanently human-only surface under the
constitutional floor of `roles-authority-model`, explicitly and not by inference
from the floor's four path-shaped clauses, and no council verdict SHALL ever
produce an autonomous approval of a change to the register; a council whose own
commission is recorded in the register SHALL NOT be eligible to clear a candidate
that edits it.

#### Scenario: A council is offered its own commission
- **WHEN** a candidate edits the intake register and a council holding a grant issued from that register is convened over it
- **THEN** the candidate is human-only and no verdict clears it

#### Scenario: The declaration is explicit
- **WHEN** the register's path is added to a repository's gate rules
- **THEN** it is entered as a never-clearable floor member by name, not left to be inferred from "credential surfaces" or "gate definitions"

### Requirement: Every review-authority grant names its issuer, and a root grant's issuer is anchored outside the register
A review-authority grant SHALL name `issued_by`, which the grant schema leaves
OPTIONAL — this capability restricts the scope it composes rather than changing
the schema — and a grant carrying no `parent_grant_ref` SHALL be a named ROOT
GRANT whose issuer's authority to issue is recorded OUTSIDE the register that
grant writes into; the root issuer of review authority in this family SHALL be
the responsible operator, whose authority is standing under the Human Escalation
Contract (`docs/roles-and-authority.md:103-140`, whose parked-decision list names
"privileged capability grants" as a decision only a human holds) and therefore
requires no wallet and no grant of its own.

#### Scenario: A grant omits its issuer
- **WHEN** a review-authority grant is issued with no `issued_by`
- **THEN** the intake refuses it, even though the grant schema would validate

#### Scenario: A root grant is issued
- **WHEN** a grant carries no `parent_grant_ref`
- **THEN** it is recorded as a root grant naming the responsible operator as issuer
- **AND** the anchor for that issuer's authority is the Human Escalation Contract, cited in the register, not a row in the register

#### Scenario: A root grant names a machine issuer
- **WHEN** a root grant names an agent holder as `issued_by`
- **THEN** the intake refuses it — a root issuer's authority cannot be conferred by the register it writes into

### Requirement: A review-authority grant never names act_unsupervised
A review-authority grant SHALL NOT name `authority_tier: act_unsupervised`, and
the intake SHALL refuse to issue one; this is a scope restriction on one
consuming capability and not a parallel authority vocabulary, and it is stated as
a RULE this capability writes rather than as a consequence inherited from the
custody registry, because the registry's ceiling is a self-declared string in a
wallet record checked only by a scanner that runs in no required check.

#### Scenario: A wallet declares isolated custody
- **WHEN** a reviewing holder's wallet declares `isolated_per_use_authorized`, whose registry ceiling is `act_unsupervised`
- **THEN** the intake still refuses to issue that holder a review-authority grant above `act`

#### Scenario: The ceiling is not assumed structural
- **WHEN** the capability states the tier ceiling
- **THEN** it states it as this requirement's refusal, and MUST NOT state that today's software custody models make `act_unsupervised` unreachable

### Requirement: An unattested custody declaration caps a review-authority grant at request
A review-authority grant's tier SHALL be capped at `request` when the audience
wallet's custody model carries no recorded attestation, and the intake SHALL
record per wallet WHO verified the custody isolation, AGAINST WHAT, and WHEN;
`declared_by` in a wallet record is a free identifier and is not an attestation,
and the custody registry's negative fixtures test the registry's internal
derivation consistency rather than any deployed wallet's declaration.

#### Scenario: A wallet declares act-capable custody with no attestation
- **WHEN** a wallet declares `holder_readable` or `isolated_invocable` and the intake holds no attestation row for it
- **THEN** any review-authority grant to that wallet is capped at `request`

#### Scenario: An attestation is recorded
- **WHEN** the intake records an attester, the artifact verified against, and a date for a wallet's custody model
- **THEN** grants to that wallet may reach `act`, still subject to the `act_unsupervised` refusal

### Requirement: No holder is issued both the review act and the approval act over one object
The intake SHALL NOT issue one holder both the review act and the approval act
over the same object, and where two grants would collapse
`execution_binding.actor_ref` into `approval.authority_ref` the intake SHALL name
a `distinct_holder_constraint_refs` entry on both grants rather than relying on
the holders being different in practice; the three parties
`openspec/specs/client-infrastructure-liaison/spec.md:18-30` says are never
collapsed into one are carried here as a positive obligation.

#### Scenario: One holder is offered both acts
- **WHEN** an intake entry would give a holder a review grant and an approval grant over the same object
- **THEN** the intake refuses the second grant

#### Scenario: Distinctness is named, not assumed
- **WHEN** two grants are required to be held apart
- **THEN** both name the constraint in `distinct_holder_constraint_refs`, since a grant naming no constraint is subject to none

### Requirement: The exercise of review authority is recorded at verdict conformance
The exercise of a review-authority grant SHALL be recorded at VERDICT
CONFORMANCE in the Hermes runtime: the seat's wallet key is minted inside the
deliberation job, the runtime verifies the signature over the seat return when it
checks the verdict, and the exercise record is written there; this keeps
enforcement outside the checked tree WITHOUT amending the runtime's advisory-only
requirement, because refusing a MALFORMED VERDICT is already the runtime's job
(`installs/hermes-install/openspec/specs/council-orchestration/spec.md`,
"A convening verdict conforms to the council's materialized semantics or is
refused"). An exercise evidenced only by the existing council or enforcement
audit trail SHALL NOT be accepted as an exercise of a grant.

#### Scenario: A seat return carries no verifiable signature
- **WHEN** a convening completion presents a seat result whose wallet signature is absent or fails verification
- **THEN** the verdict is refused fail-closed as nonconforming, and no exercise is recorded

#### Scenario: Audit-trail evidence is not an exercise
- **WHEN** a grant's exercise is proposed to be evidenced by the council record and the enforcement check-run rather than by a wallet-signed return
- **THEN** the proposal is refused, because such an act records as `event_class: unauthenticated_request` and `unattributed` and confers nothing checkable

#### Scenario: Attribution is not supplied by the register
- **WHEN** an act is performed under a shared installation credential
- **THEN** that credential is recorded as transport and the act as unattributed, and the intake's record of a grant MUST NOT be read as supplying the attribution the key did not establish

### Requirement: Revocation is re-checked at verdict consumption against a declared staleness bound
Revocation SHALL be re-checked at verdict consumption and not trusted from the
convening's admission stamp, and a seat whose grant was revoked or expired
between commission and verdict SHALL park the candidate with a NAMED REFUSAL
rather than be silently honored because the roster was stamped at admission; the
register SHALL declare a revocation staleness bound, and an intake that cannot be
read at exercise SHALL refuse rather than proceed.

#### Scenario: A grant is revoked mid-convening
- **WHEN** a seat's grant is revoked after the convening was admitted and before its verdict is consumed
- **THEN** the candidate parks with a refusal naming the revoked holder
- **AND** the admission stamp is not accepted as evidence of current validity

#### Scenario: The register cannot be read
- **WHEN** the intake register is unreachable, unparseable, or older than the declared staleness bound at exercise
- **THEN** the exercise is refused, never proceeded with

#### Scenario: A grant expires between commission and verdict
- **WHEN** `expires_at` passes between admission and verdict consumption
- **THEN** the grant is treated as expired at exercise regardless of the `state` field recorded in the grant file

### Requirement: A reviewing holder's composition is pinned, and a composition roll is a governed re-issuance
A reviewing holder's declared composition SHALL pin its model version and its
prompt corpus as declared components, and SHALL NOT declare the candidate
repository at HEAD as its retrieval corpus, so that a provider alias roll becomes
a GOVERNED RE-ISSUANCE EVENT with a named runbook rather than a silent
fleet-wide revocation; the capability SHALL record that
`openspec/specs/openxwallet-agent-profile/spec.md:27-48` revokes on any single
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

### Requirement: The non-self-review refusal's candidate-side input is derived, never reported
The runtime SHALL compute the candidate's touched-object set from the subject
pin under its own credential when refusing a convening over the machinery a
council is assembled from, and SHALL REFUSE a convening whose touched-object set is
unavailable, self-reported by the candidate's own repository, or otherwise
unverifiable; the refusal's reachable subject SHALL be stated plainly as
MATERIALIZED DOMAIN CONTENT ONLY, so codexFactory's `"scripts/**"` floor entry,
its `/scripts/ @brettheap` CODEOWNERS line and its import-root coverage test
remain the SOLE defence for the decision core, and the runtime refusal SHALL be
ADDITIVE to them and never a replacement.

#### Scenario: The commissioning lane reports the changed paths
- **WHEN** the touched-object set reaches the runtime from a workflow file the candidate pull request can edit
- **THEN** the input is self-reported and the convening is refused rather than admitted on it

#### Scenario: The touched-object set cannot be derived
- **WHEN** the runtime cannot resolve the subject pin's content under its own credential
- **THEN** the convening is refused fail-closed

#### Scenario: The decision core is outside the refusal's reach
- **WHEN** a candidate touches the decision core's import root, which is not materialized domain content
- **THEN** the runtime refusal does not see it, and the in-tree floor entry, CODEOWNERS line and import-root test are the defence
- **AND** no statement of this capability claims the runtime refusal replaces them
