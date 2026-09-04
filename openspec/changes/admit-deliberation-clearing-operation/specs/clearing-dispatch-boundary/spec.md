# clearing-dispatch-boundary Specification (delta)

## ADDED Requirements

### Requirement: deliberation is register entry number two and returns evidence only
The register's SECOND ENTRY SHALL be `deliberation`, and it SHALL be a
bundle-carrying operation whose entire return is EVIDENCE: it runs the seat
deliberations of an admitted convening on the governed host and hands back the
per-seat outputs as a structured return, and it SHALL NOT compute, carry, or
imply the outcome those outputs are later used to decide.

THIS REQUIREMENT IS WRITTEN OVER `add-clearing-dispatch-boundary`'s ADDITION,
which is RATIFIED (2026-09-01, Brett Heap) and REALIZED (PR #628, `0d5e1ba9`)
but NOT YET ARCHIVED, so the capability it extends exists today only as that
active change's `## ADDED Requirements` block and not in any promoted
specification. The pairing is declared here because
`govern-sibling-added-modified-deltas` (ratified 2026-08-31) makes an undeclared
pairing the defect, and it is declared IN PROSE rather than in that capability's
reserved marker form because the reserved form is required of a
`## MODIFIED Requirements` block and this is an `## ADDED` one — the same reading
the sibling packet `add-cpc-clearing-boundary` already ships, whose three
MODIFIED requirements each carry the marker and whose ADDED block carries none.
Nothing in the basis is restated, narrowed, or widened here: this entry is
ADMITTED UNDER the closed-register requirement's own terms, and every general
rule it names — the single door, the ten-field sealed request, API-resolved
provenance, the re-seal, the hosted finalizer, the authoring-time guard, the
dispatch record and the periodic attestation — governs this operation
unchanged.

THE ENTRY SHALL DECLARE EVERY FACT the closed-register requirement demands of an
entry, and this requirement fixes each of them.

**Operation id.** `deliberation`.

**What it MAY do.** Read the admitted, RE-SEALED deliberation bundle served to it
from the CLEARING run — never from the originating repository; run the seat
deliberations the bundle's resolved run specification names, the candidate bytes
reaching a seat only as delimited untrusted input; and emit the per-seat outputs
as a STRUCTURED RETURN of evidence — seat identity, that seat's output, and the
run identifiers that bind the return to the convening job id, the verified
subject pin, and the inbound bundle digest it answers — sealed as an object of
the clearing run so the clearing side can re-serve it to the originator.

**What it MAY NOT do.** Check out any repository, the originating repository
included — a checkout writes the runner workspace and there is no route by which
the host may fetch, clone, or authenticate to the producer. Write anything
outside the runner's own temporary plumbing, and it SHALL prove its staging area
is gone when it terminates. Reference a secret, in any expression or environment
block. HOLD ANY SEAT KEY, OR ANY OTHER SIGNING KEY, IN ANY FORM: the return is
UNSIGNED on the host and is signed on return by the originating repository's own
hosted signer, so NO KEY IS EVER PRESENT ON THE HOST. Carry a verdict,
eligibility, decision, go/no-go, approval, or recommendation field: what the
seats produce is evidence, and the outcome is computed by the runtime from the
signed returns, downstream of and outside this boundary. Report OBSERVED
runner-group membership — observed membership is established only by the
periodic single-door attestation reading the provider's API. Affect any
repository.

**Class constraints.** `checks_out_code: false`; `writes: false`;
`may_reference_secrets: false`; `token_scopes` carrying EXACTLY the clearing
side's own scoped, short-lived, READ-ONLY admission credential and nothing else
— sufficient to read the CLEARING repository's own run artifacts and no more,
spelled `actions:read` in the identifier form the register's schema requires and
in the vocabulary `credential-contracts` already carries for a scoped dispatch
credential, this family minting no scope vocabulary of its own; and a BOUNDED
`timeout_minutes`. THE EMPTY TOKEN-SCOPE LIST OF ENTRY NUMBER ONE IS NOT
WIDENED BY THIS ENTRY AND SHALL NOT BE READ AS HAVING BEEN. Entry number one's
constraints bind entry number one; the basis says in as many words that "a later
bundle-carrying operation carries the clearing side's admission credential under
its OWN entry's constraints", and this is that entry. A CREDENTIAL SCOPED TO THE
ORIGINATING REPOSITORY SHALL NEVER APPEAR IN THIS OPERATION'S JOB ENVIRONMENT,
whatever this entry's scopes say, that refusal being the basis's and not this
entry's to relax.

**Required worker profile.** `council-deliberation-worker`.

**Lanes.** THE ARTIFACT LANE, AND ONLY THE ARTIFACT LANE: `runner_group`
`xfactory-artifact-workers`, `dispatch_label` `host-rider-cpc-brett01`,
`expected_runner` `xfactory-artifact-cpc-brett01`. The entry SHALL NOT permit the
coding lane, and a sealed request declaring `xfactory-execution-lane-workers` or
`host-coding-cpc-brett01` for this operation SHALL be refused with
`clearing-lane-not-permitted` before any runner is selected. The lane constants
are the ones entry number one already declares for the artifact lane and the ones
the clearing workflow declares literally; this entry introduces none.

**Declared output schema.** `contracts/clearing/deliberation-return.schema.yaml`
— a NEW NEUTRAL SCHEMA authored in this repository, ruled on 2026-09-04 by Brett
Heap ("Ruling OQ1: new neutral deliberation-return schema"). A return SHALL be
validated against THIS value and NEVER against a bundle's copy of it, and the
declared schema SHALL NOT be a path owned by a producing repository: a neutral
register that pointed at a domain repository's file would make the producer the
author of the shape its own return is checked against.

**Data handling.** `internal-governance` — STRICTER than entry number one's
`public_log_only`, which the register instance's own comment promised a
bundle-carrying operation would be. The justification is the difference in what
crosses: entry number one reports only facts about the runner that are already
visible in a public run log, while this operation carries SELECTED SOURCE FILES
AND A GOVERNANCE PACKET across the boundary, and its return carries the seats'
reasoning about them. The class name is `document-cataloging`'s vocabulary and
is the class the estate's governance corpus already travels under; this family
declares no classification of its own.

**Repository-affecting output.** `false`. The return is evidence. A change that
gave this entry a repository effect would need a hosted finalizer and would BE a
change to this entry, made on the same governed terms as its admission.

ADMITTING THIS ENTRY AUTHORIZES NO HOST JOB BY ITSELF, and the boundary's
route-retirement requirement SHALL bind the change that declares one. The
governed group `xfactory-artifact-workers` today carries the grandfathered
member `council-deliberation-worker.yml`, whose host jobs perform exactly this
work by the direct route. THE CHANGE IN THE CLEARING REPOSITORY THAT DECLARES
THE `deliberation` HOST JOB SHALL, IN THE SAME ACT, remove that workflow's host
jobs, remove its workflow-allowlist entry on that group, and shrink the
grandfather enumeration by that member. This entry existing beside a live direct
route is the dormant second door the basis refuses, and naming the obligation
here is what makes it checkable at the moment it can be violated rather than
discovered afterwards.

#### Scenario: A bundle names deliberation on the artifact lane
- **WHEN** a sealed bounded request declares operation `deliberation`, runner group `xfactory-artifact-workers` and dispatch label `host-rider-cpc-brett01`, and every provider-answerable field resolves and agrees
- **THEN** the dispatch MUST clear
- **AND** the operation, worker profile, output schema and data-handling classification MUST be reported as POLICY-CHECKED against this entry and MUST NOT be reported as provider-verified
- **AND** the host MUST be served the re-sealed bundle from the clearing run rather than reaching the originating repository

#### Scenario: A bundle asks for the coding lane
- **WHEN** a sealed request declaring operation `deliberation` names runner group `xfactory-execution-lane-workers` or dispatch label `host-coding-cpc-brett01`
- **THEN** the dispatch MUST be refused with `clearing-lane-not-permitted`
- **AND** no runner MUST be selected
- **AND** the refusal MUST NOT be cured by widening the entry's lanes without a governed change

#### Scenario: A change widens the entry's class constraints
- **WHEN** a change would let `deliberation` check out a repository, write outside the runner's temporary plumbing, reference a secret, hold a signing key, or return repository-affecting output
- **THEN** the change MUST be refused as a widening that owes its own governed contract change amending this entry
- **AND** the refusal MUST be presented as a review-backed tripwire rather than as an unforgeable one, the register, the validator that reads it and the tests that pin it sharing a repository with the changes they police

#### Scenario: The return carries a verdict
- **WHEN** a return from this operation carries a member whose name reads as a verdict, an eligibility, a decision, a go/no-go, an approval or a recommendation
- **THEN** it MUST be refused with `clearing-report-carries-a-verdict`
- **AND** the scan that produces that refusal MUST be applied to THIS operation's declared return shape as well as to the operation report, a refusal that fires only on a kind this operation never emits being no refusal at all for it

#### Scenario: The return does not validate against the declared neutral schema
- **WHEN** a return from this operation does not validate against `contracts/clearing/deliberation-return.schema.yaml`
- **THEN** it MUST be refused whole and recorded rather than partially applied
- **AND** it MUST have no effect on any repository, the return being evidence in the first place
- **AND** the ground MUST be a member of the closed refusal enumeration, added by a governed change rather than recorded as free text

#### Scenario: A key or a producer-scoped credential would reach the host
- **WHEN** a dispatch of this operation would place a seat key, any other signing key, or any credential scoped to the originating repository into the host's job environment
- **THEN** the dispatch MUST be refused
- **AND** the return MUST remain UNSIGNED on the host and be signed on return by the originating repository's own hosted signer

#### Scenario: The host job lands while the direct route still stands
- **WHEN** the clearing workflow declares the `deliberation` host job while `council-deliberation-worker.yml` still declares its host jobs on `xfactory-artifact-workers`, holds its workflow-allowlist entry, or remains a member of the grandfather enumeration
- **THEN** the change MUST be refused as leaving a dormant second door
- **AND** the retirement MUST happen in the same act, in both the live allowlist and the in-repo enumeration
