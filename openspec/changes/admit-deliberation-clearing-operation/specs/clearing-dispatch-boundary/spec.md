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
unchanged. TWO of those requirements RESERVE AN ACT TO A GOVERNED CHANGE and
this one performs both, which is exercising them rather than amending them: the
closed register's "adding an operation SHALL be a governed contract change", and
the dispatch record's "a ground absent from that enumeration SHALL be added by a
governed change rather than recorded as free text".

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

**Lanes.** THE ARTIFACT LANE, AND ONLY THE ARTIFACT LANE: `lane_key`
`artifact`, `runner_group` `xfactory-artifact-workers`, `dispatch_label`
`host-rider-cpc-brett01`, `expected_runner` `xfactory-artifact-cpc-brett01` —
the four members the register's lane shape requires, none of them optional. The entry SHALL NOT permit the
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

THE RETURN IS A FAMILY RECORD AND ITS KIND IS NAMED HERE RATHER THAN COINED AT
REALIZATION: `xfactory_clearing_deliberation_return`, in the family's existing
`xfactory_clearing_*` form, admitted BY THIS CHANGE to the routing that maps a
record's `kind` to the schema it is validated against. The kind is named in the
ratified text because the verdict scan below is DISPATCHED ON KIND, so a
realization free to choose the kind would be free to choose whether the scan
reaches this operation at all.

**Data handling.** `internal-governance` — STRICTER than entry number one's
`public_log_only`, which the register instance's own comment promised a
bundle-carrying operation would be. The justification is the difference in what
crosses: entry number one reports only facts about the runner that are already
visible in a public run log, while this operation carries SELECTED SOURCE FILES
AND A GOVERNANCE PACKET across the boundary, and its return carries the seats'
reasoning about them. THE ATTRIBUTION IS STATED EXACTLY, because a borrowed word
credited to the wrong family is a word nobody owns: the `data_handling` FIELD
borrows its vocabulary as the register's own schema says, from
`document-cataloging`, which carries a document's handling as a SOURCE-DECLARED
MECHANICAL INVENTORY FIELD copied verbatim — its catalog snapshot types
`handling` as a free string — and which decides, in its handling gate, whether a
host is authorized for a class; it defines no controlled set of class names. THE
CLASS NAME `internal-governance` IS THE `Handling:` HEADER VALUE THE ESTATE'S
GOVERNANCE CORPUS ALREADY TRAVELS UNDER, of the `document-lifecycle` /
doc-health header family, and the handling authorization the doc-health worker
dispatch requires by default. This entry declares WHICH class its output
carries; it mints no class and no vocabulary.

**Refusal grounds, named here because the enumeration is closed and this is the
governed change.** A refusal SHALL be recorded with its ground named from the
CLOSED, NAMED ENUMERATION the dispatch record carries, and a ground absent from
that enumeration SHALL be added by a governed change rather than recorded as
free text. That enumeration HELD TWO MEMBERS AT THIS CHANGE'S AUTHORING —
`unregistered_operation` and `unknown_lane_selector` — one per refusal the
realization can actually emit, and the record's own words are that each further
ground "becomes a member AS THE OPERATION THAT CAN PRODUCE IT LANDS". THIS ENTRY
IS THAT OPERATION FOR THREE OF THEM, so this change ADMITS EXACTLY THREE FURTHER
GROUNDS — carrying the enumeration to FIVE — and names them rather than leaving a
realizer to coin them. The count is written as a reading TAKEN AT A MOMENT rather
than as a standing fact, because a ratified sentence that its own realization
falsifies is a sentence a later reader cannot rely on:

- `lane_not_permitted` — entry number one permits BOTH lanes, so no dispatch
  could reach this refusal; entry number two is the first entry that permits one
  lane and refuses the other, and the refusal is this entry's own scenario.
- `output_schema_failure` — the ground of a return refused whole for failing the
  declared neutral schema, which entry number two is the first entry to make
  reachable by declaring a return shape a host actually produces.
- `origin_scoped_credential` — entry number one's job carries NO token at all,
  so no credential could be mis-scoped into it; entry number two is the first
  entry whose job carries a token, and the refusal is this entry's own scenario.
  ONE GROUND COVERS THE WHOLE CLASS of material scoped to the originating
  repository that must never reach the host, A SEAT KEY INCLUDED. The record's
  awaited list names no separate signing-key ground, and coining one here would
  be minting a CONCEPT rather than rendering a NAME — which is the line this
  entry holds. `origin` in this identifier carries the meaning the dispatch
  record already fixes for it in its own field names, THE ORIGINATING REPOSITORY
  (`origin_repository`, `origin_signature`), and not "the origin signing key":
  the ground is a credential SCOPED TO the originating repository, wherever it
  came from.

THE THREE ENGLISH NAMES ARE THE RECORD'S OWN; THE THREE IDENTIFIERS ARE THIS
CHANGE'S, MECHANICALLY DERIVED, AND THE ENUMERATION MOVES AT REALIZATION BY THIS
TEXT. The dispatch record names its awaited grounds IN PROSE and not in
identifiers — "lane not permitted", "output-schema failure" and "origin-scoped
credential" are three of the nine it lists, in those words — so there is no
identifier anywhere to copy and a realizer would have had to invent one. This
change invents no CONCEPT. It renders each of those three names into the
identifier form the two seeded members already carry, by the single rule those
two follow: lower case, words joined by underscores, no `clearing-` prefix, and
a hyphen inside a compound becoming an underscore. The rendering is ratified here
precisely so that the enumeration moves BY THIS TEXT rather than by a realizer's
ear. Applying the same rule to the six grounds that stay absent is not
authorization to seed them.

NO OTHER GROUND IS SEEDED. The remaining grounds the record names as awaited
stay absent until the operation that can produce them lands, an enumeration
seeded with grounds no implementation can emit being closed in name only.

AND NO VALIDATOR REFUSAL CODE IS MINTED BY THIS ENTRY. The grounds above are
members of the RECORD's enumeration and are not members of the canonical
validator's closed finding-code set; the two are different sets with different
spellings, so this requirement states WHICH COMPONENT EMITS WHICH rather than
leaving realization to decide it:

- The two finding codes this entry's refusals need ALREADY EXIST —
  `clearing-lane-not-permitted` and `clearing-report-carries-a-verdict` — and
  this entry uses them unchanged.
- A return that FAILS ITS DECLARED SCHEMA is reported BY THE CANONICAL VALIDATOR
  as the family's SHAPE refusal, `schema`, which the closed finding-code set
  deliberately excludes because it is JSON Schema's rule and not this family's.
  That reporting begins only once the new `kind` is ROUTED to its schema: an
  unrouted kind is not validated at all rather than validated loosely, which is
  why the routing is a named realization task and not an assumption.
- The dispatch record's ground `output_schema_failure` is written BY THE CLEARING
  WORKFLOW'S HOSTED FINALIZER at dispatch time — where the basis already places
  that refusal — and NOT by the canonical validator, which never writes a
  dispatch record at all. `origin_scoped_credential` is likewise a property of a
  dispatch ATTEMPT rather than of any packaged shape, so no fixture can make it
  fire and none is owed: the family's "every closed refusal code is red-proven"
  rule binds the validator's finding CODES, not this enumeration's MEMBERS, whose
  proof is that a packaged record naming them validates clean.
- The validator's only duty over these members is the one it already performs.
  `clearing-record-refusal-ground-unknown` reads the enumeration OUT OF THE
  SCHEMA at run time, so admitting the three members requires no validator code
  and grants no new refusal.

ASSIGNING AN EXISTING REFUSAL TO AN EXISTING COMPONENT IS NOT A WIDENING. A
widening of the finding-code set would be a separate governed change and this
entry does not make one.

**Repository-affecting output.** `false`. The return is evidence. A change that
gave this entry a repository effect would need a hosted finalizer and would BE a
change to this entry, made on the same governed terms as its admission.

ADMITTING THIS ENTRY AUTHORIZES NO HOST JOB BY ITSELF, and the boundary's
route-retirement requirement SHALL bind the change that declares one. THE
READING IS STATED RATHER THAN ASSUMED, because that requirement's own scenario
"A migration leaves the old route in place" refuses a change that "adds a
clearing operation for work an existing direct route still performs", and a
reader could take THIS change to be that one. It is not, and the test is whether
a SECOND DOOR EXISTS: a register entry with no host job declared anywhere is not
a route, nothing can be dispatched through it, and the direct route is still the
only door. The act that opens the second door is the act that declares the host
job, and that act is where the requirement bites — which is why the obligation
is carried forward onto it below rather than discharged here.

The governed group `xfactory-artifact-workers` carries, AT THIS CHANGE'S
RATIFICATION, the grandfathered member `council-deliberation-worker.yml`, whose
host jobs perform exactly this work by the direct route. THE CHANGE IN THE CLEARING REPOSITORY THAT DECLARES
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
- **AND** the refusal MUST be recorded with the ground `lane_not_permitted`, admitted to the record's closed enumeration by this change
- **AND** the refusal MUST NOT be cured by widening the entry's lanes without a governed change

#### Scenario: A change widens the entry's class constraints
- **WHEN** a change would let `deliberation` check out a repository, write outside the runner's temporary plumbing, reference a secret, hold a signing key, or return repository-affecting output
- **THEN** the change MUST be refused as a widening that owes its own governed contract change amending this entry
- **AND** the refusal MUST be presented as a review-backed tripwire rather than as an unforgeable one, the register, the validator that reads it and the tests that pin it sharing a repository with the changes they police

#### Scenario: The return carries a verdict
- **WHEN** a return from this operation carries a member whose name reads as a verdict, an eligibility, a decision, a go/no-go, an approval or a recommendation
- **THEN** it MUST be refused with `clearing-report-carries-a-verdict`
- **AND** the scan that produces that refusal MUST be applied to records of kind `xfactory_clearing_deliberation_return` as well as to the operation report, a refusal that fires only on a kind this operation never emits being no refusal at all for it

#### Scenario: The return does not validate against the declared neutral schema
- **WHEN** a return from this operation does not validate against `contracts/clearing/deliberation-return.schema.yaml`
- **THEN** it MUST be refused whole and recorded rather than partially applied
- **AND** it MUST have no effect on any repository, the return being evidence in the first place
- **AND** the ground MUST be `output_schema_failure`, a member this change admits to the record's closed refusal enumeration, rather than free text

#### Scenario: A key or a producer-scoped credential would reach the host
- **WHEN** a dispatch of this operation would place a seat key, any other signing key, or any credential scoped to the originating repository into the host's job environment
- **THEN** the dispatch MUST be refused with the ground `origin_scoped_credential`, a member this change admits to the record's closed refusal enumeration
- **AND** the return MUST remain UNSIGNED on the host and be signed on return by the originating repository's own hosted signer

#### Scenario: The host job lands while the direct route still stands
- **WHEN** the clearing workflow declares the `deliberation` host job while `council-deliberation-worker.yml` still declares its host jobs on `xfactory-artifact-workers`, holds its workflow-allowlist entry, or remains a member of the grandfather enumeration
- **THEN** the change MUST be refused as leaving a dormant second door
- **AND** the retirement MUST happen in the same act, in both the live allowlist and the in-repo enumeration
