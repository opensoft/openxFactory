# clearing-dispatch-boundary Specification (delta)

## ADDED Requirements

### Requirement: The clearing repository is the single door to a governed execution host
Exactly ONE repository — the CLEARING REPOSITORY — SHALL be authorized to
originate execution on a governed execution host, and no other repository
SHALL be broadly authorized to do so. The provider-side runner group serving
that host restricts BOTH the repositories that may reach it AND the exact
workflow paths permitted, and the workflow allowlist CONVERGES to exactly
ONE PERMANENT ENTRY per group: the clearing workflow's exact path, admitted
by the operator once.

Because the provider evaluates the workflow allowlist against the workflow
file that DIRECTLY CONTAINS the job requesting the runner, every
host-touching job SHALL live physically inside the clearing workflow file; a
host job delegated to a reusable or called workflow is non-conformant,
because that file would need an allowlist entry of its own and the door
would no longer be single.

Existing host-touching workflows that predate this contract SHALL be carried
as a CLOSED, ENUMERATED GRANDFATHER LIST which is APPEND-NEVER and
SHRINK-ONLY: no workflow is ever added to it, each member retires into a
clearing operation, and the enumeration reaching empty is what convergence
means. Enforcement is FAIL-CLOSED and the failure mode is stated rather than
assumed: a job requesting a governed host from outside the permitted set is
not executed ungoverned, it is never claimable. Any future reconsideration of
direct access SHALL be a SINGLE EXACT WORKFLOW PATH on a protected default
branch; repository-wide admission is refused.

#### Scenario: A factory dispatches a governed-host job directly
- **WHEN** a workflow in a repository other than the clearing repository requests a governed runner group
- **THEN** the job MUST NOT execute
- **AND** it remains unclaimable rather than being served by a runner
- **AND** the attempt is observable as a queued job that no runner can claim

#### Scenario: The allowlist is measured at convergence
- **WHEN** the workflow allowlist of a governed runner group is read from the provider
- **THEN** it MUST contain the clearing workflow's exact path
- **AND** every other entry MUST be a current member of the enumerated grandfather list

#### Scenario: A host job is moved into a reusable workflow
- **WHEN** a change moves a job that requests a governed runner group out of the clearing workflow file into a reusable or called workflow
- **THEN** the change MUST be refused as non-conformant
- **AND** the reason recorded is that the allowlist is evaluated against the file containing the job

#### Scenario: Someone proposes adding a workflow to the grandfather list
- **WHEN** a change proposes adding a workflow path to the enumerated grandfather list
- **THEN** it MUST be refused
- **AND** the host-touching lane it wanted MUST instead be expressed as a permitted operation of the clearing workflow

#### Scenario: Direct access is reconsidered later
- **WHEN** an operator ruling admits a producing repository's own path to a governed runner group
- **THEN** the admission MUST name a single exact workflow path on a protected default branch
- **AND** a repository-wide or pattern admission MUST be refused

### Requirement: Work crosses the boundary only as a sealed bounded request
Cross-repository work SHALL reach a governed execution host only as a SEALED
BOUNDED REQUEST, and the sealed request SHALL carry all TEN declared fields:
(1) the originating repository and workflow; (2) the source commit; (3) a
unique job id and an expiration; (4) the selected-file manifest with a hash
per file; (5) the permitted operation; (6) the required worker profile; (7)
the exact runner group and the unique dispatch label; (8) the output schema;
(9) the data-handling classification; and (10) a signature or trusted
hosted-workflow provenance.

The sealed request SHALL be a SHORT-LIVED SEALED JOB OBJECT and SHALL NOT be
a committed path of copied data in any repository: an expiring object is a
REQUEST, while a committed copy is a MIRROR that outlives the work, carries
the source's handling class into a second repository's permanent history, and
cannot distinguish two dispatches of the same content. A request whose
expiration has passed is refused rather than served, and a bundle carrying
selected files without their hashes, or hashes that do not match the files
carried, is refused.

Hashes and any bundle digest SHALL be computed with the ONE digest
construction `signed-execution-chain` already puts in force, and the sealed
request SHALL NOT define a second job-envelope, handling-classification, or
digest vocabulary; it seals a job expressed in existing vocabulary.

#### Scenario: A conformant sealed request is presented
- **WHEN** a producer presents a sealed bounded request at the boundary
- **THEN** all ten declared fields MUST be present
- **AND** every selected file MUST carry a hash matching its bytes
- **AND** a missing or empty declared field MUST refuse the request with the field named

#### Scenario: A request is presented as committed data
- **WHEN** work is offered to the boundary as a committed folder, branch, or path of copied source rather than as a sealed job object
- **THEN** the offer MUST be refused
- **AND** the refusal MUST NOT be worked around by committing the bundle into the clearing repository

#### Scenario: An expired handle is replayed
- **WHEN** a sealed request whose declared expiration has passed is dispatched
- **THEN** the boundary MUST refuse it
- **AND** the refusal MUST be recorded as an expiry refusal rather than a transient failure

#### Scenario: A second digest rule is proposed
- **WHEN** a manifest hash or bundle digest is specified for the sealed request
- **THEN** it MUST use the digest construction already in force for the estate
- **AND** a new construction MUST NOT be defined by this capability

### Requirement: Every verifiable field is verified against the provider's authoritative API
The clearing workflow SHALL verify each sealed-request field that has an
authoritative provider-side answer by resolving that answer from the
provider's API and comparing it, and SHALL NEVER accept a field as true
because the bundle asserts it. A bundle is a set of CLAIMS by its packager;
its internal consistency evidences only the packager's consistency.

The fields with an authoritative answer — the originating repository, the
originating workflow path, the source commit, the dispatching identity, and
the existence of the sealed object together with the run that produced it —
SHALL be resolved and compared before any dispatch. The fields with NO
authoritative provider answer — permitted operation, required worker profile,
output schema, and data-handling classification — SHALL be validated against
the closed permitted-operations register and against policy, and SHALL NOT
be reported as VERIFIED, because "verified" applied to a field nothing could
verify is precisely the false assurance this boundary exists to prevent.

A verification that cannot be performed SHALL refuse: an unreadable or
erroring provider API is not a verification that passed. The claimed value
SHALL be retained beside the resolved value in the dispatch record, because a
discarded claim makes a disagreement undetectable after the fact.

#### Scenario: The bundle names a workflow the provider contradicts
- **WHEN** the bundle's declared originating workflow path differs from the path the provider reports for the run that produced the sealed object
- **THEN** the dispatch MUST be refused before any runner is selected
- **AND** both the claimed and the resolved value MUST be recorded

#### Scenario: The claimed source commit does not match the run
- **WHEN** the bundle's declared source commit differs from the head commit the provider reports for the originating run
- **THEN** the dispatch MUST be refused

#### Scenario: The provider API cannot be read
- **WHEN** a required provider-side resolution fails, times out, or returns an error
- **THEN** the boundary MUST refuse the dispatch
- **AND** it MUST NOT proceed on the bundle's own assertion of the same fact

#### Scenario: A policy-checked field is reported
- **WHEN** the dispatch record reports on the permitted operation, worker profile, output schema, or data-handling classification
- **THEN** those fields MUST be reported as policy-checked against the register
- **AND** they MUST NOT be reported as provider-verified

### Requirement: One sanctioned exit, and the host is served from the clearing run
A producing repository SHALL express "this work needs governed-host
execution" in exactly ONE conformant way: package the sealed bounded request
on hosted infrastructure, then dispatch the clearing workflow with the handle
to that sealed object. No other producer behaviour is conformant, and a
producer SHALL NOT reach a governed host by any route that bypasses the
clearing workflow.

The governed host SHALL NOT receive any credential scoped to the originating
repository and SHALL NOT clone, fetch, or check out the originating
repository. Because a sealed object belongs to the run that produced it, the
boundary RE-SEALS: the hosted clearing side ADMITS the producer's object
using a scoped, short-lived, read-only credential held on the CLEARING side
and recorded as a `credential-contracts` record with declared custody,
verifies it per the API-verification requirement, and serves the host from
the clearing side's own sealed object. The host therefore reads with a
credential scoped to the clearing repository alone.

Selected source files only SHALL cross the boundary: the sealed request
carries the files its manifest names and nothing else, and a request seeking
the originating repository's working tree, history, or credentials is refused
rather than narrowed.

#### Scenario: A producer packages and dispatches
- **WHEN** a producing repository packages a sealed bounded request on hosted infrastructure and dispatches the clearing workflow with its handle
- **THEN** the exit is conformant
- **AND** no further producer-side authorization on the governed host is required or granted

#### Scenario: The host is asked to fetch from the originating repository
- **WHEN** an operation, bundle, or workflow would have the governed host clone, fetch, or authenticate to the originating repository
- **THEN** it MUST be refused as non-conformant
- **AND** the sealed object MUST be admitted and re-served by the hosted clearing side instead

#### Scenario: A credential for the originating repository would reach the host
- **WHEN** a dispatch would place a token, key, or credential scoped to the originating repository into the host's job environment
- **THEN** the dispatch MUST be refused
- **AND** the admission credential MUST remain on the hosted clearing side

#### Scenario: A bundle asks for more than its manifest
- **WHEN** a sealed request would carry the originating repository's whole tree or history rather than the files its manifest names
- **THEN** the request MUST be refused

### Requirement: Returned output is validated on hosted infrastructure before any repository effect
Output returned by a governed execution host SHALL be treated as UNTRUSTED
INPUT and SHALL be validated, and where the register entry so declares
tested, by a hosted finalizer in the clearing repository BEFORE it may affect
any repository. No output from a host SHALL reach a branch, commit, pull
request, artifact of record, or downstream consumer without passing that
finalizer.

Each register entry SHALL declare whether its operation returns
REPOSITORY-AFFECTING OUTPUT. An operation that declares such output SHALL
have its return validated against the entry's declared output schema, and a
return that fails its schema SHALL be refused and recorded rather than
partially applied. An operation that declares NO repository-affecting output
SHALL be prevented from having one: its return is evidence, and a change
that gives it a repository effect is a register change.

#### Scenario: A patch-returning operation returns a patch
- **WHEN** an operation declaring repository-affecting output returns its result
- **THEN** the hosted finalizer MUST validate and test it before any branch, commit, or pull request is created
- **AND** an unvalidated return MUST have no repository effect

#### Scenario: A return fails its declared output schema
- **WHEN** a host's return does not validate against the output schema its register entry declares
- **THEN** it MUST be refused whole
- **AND** the refusal MUST be recorded with the schema violation named

#### Scenario: A read-only operation acquires a repository effect
- **WHEN** a change would give an operation declaring no repository-affecting output an effect on a repository
- **THEN** the change MUST be refused unless the register entry is amended by a governed change

### Requirement: The permitted-operations register is closed
An operation SHALL exist only as an entry in a CLOSED PERMITTED-OPERATIONS
REGISTER: the set of operations a governed execution host may be asked to
perform is closed, and a sealed request naming an operation with no register
entry SHALL be refused before any runner is selected.

Each entry SHALL declare its operation id, what the operation may do and
what it may not, its class constraints (at minimum: whether it checks out
code, whether it writes, whether it may reference secrets, and the token
scopes its job carries), its required worker profile, the lanes — runner
group and dispatch label — it may be dispatched to, its declared output
schema, and whether it returns repository-affecting output.

ADDING AN OPERATION SHALL BE A GOVERNED CONTRACT CHANGE with a spec delta
and a reviewer, and SHALL NOT be a workflow edit: an operation set that any
lane author may extend is a self-service widening of what the estate's hosts
do, reviewed only as workflow configuration. Widening an existing entry's
class constraints SHALL be a governed change on the same terms.

#### Scenario: A bundle names an unregistered operation
- **WHEN** a sealed request declares an operation id with no entry in the register
- **THEN** the dispatch MUST be refused with the unknown operation named
- **AND** no runner MUST be selected

#### Scenario: An operation is added by workflow edit
- **WHEN** a change adds a host job for a new operation to the clearing workflow without a register entry
- **THEN** the change MUST be refused as non-conformant

#### Scenario: A bundle requests a lane its operation does not permit
- **WHEN** a sealed request's declared runner group or dispatch label is not one the operation's register entry permits
- **THEN** the dispatch MUST be refused

#### Scenario: An operation's constraints are widened
- **WHEN** a change would let a registered operation check out code, write, or reference secrets where its entry forbids it
- **THEN** the widening MUST require a governed change amending the entry

### Requirement: readiness-diagnostic is register entry number one and is strictly read-only
The register's FIRST ENTRY SHALL be `readiness-diagnostic`, and it SHALL be
a strictly read-only probe that asserts only facts the host can state about
itself: the runner's identity compared against the identity expected for the
lane, the runner group, the dispatch label, the service account the runner
executes as, the host identity, a heartbeat and clock reading, an
environment echo restricted to a NAME ALLOWLIST of known non-secret
variables, and a harmless fixed-input, fixed-expected-digest compute round
trip.

Its class constraints SHALL be: no checkout, no writes, no secret reference,
no token scopes, and a bounded timeout. The environment echo SHALL be a name
allowlist and SHALL NOT be a wholesale environment dump, so that a
credential which someday appears in the host's process environment cannot be
printed into a run log by accident. A runner identity that does not match the
expected identity SHALL fail the operation with the observed identity named,
rather than proceeding against an unexpected host.

The operation SHALL emit a STRUCTURED OPERATION REPORT — the probed facts as
data, not as a log a human reads — and SHALL declare NO repository-affecting
output, so no finalizer applies and its return is evidence only. The report
SHALL NOT be a readiness DECISION: it is evidence produced BY passing
through the boundary, and it MUST NOT be presented as, or grown into, the
neutral infrastructure-readiness result that the promoted `document-cataloging`
and `ideation-routing` preflights await, which is a decision input consulted
BEFORE dispatch. Where a standalone workflow already performs these checks
outside the boundary, landing this operation SHALL retire it under the
route-retirement requirement.

#### Scenario: The probe runs on a lane
- **WHEN** `readiness-diagnostic` is cleared and dispatched to a lane
- **THEN** it MUST report runner identity, group, dispatch label, service account, host identity, heartbeat and clock, the allowlisted environment names, and the compute round trip
- **AND** it MUST check out nothing, write nothing, reference no secret, and carry no token scopes

#### Scenario: The runner is not the expected host
- **WHEN** the runner's reported identity differs from the identity expected for the dispatched lane
- **THEN** the operation MUST fail
- **AND** the observed identity MUST be named in the report

#### Scenario: An environment dump is proposed
- **WHEN** a change would echo the host's environment wholesale rather than by name allowlist
- **THEN** it MUST be refused as non-conformant with this entry's class constraints

#### Scenario: The report is mistaken for a readiness decision
- **WHEN** a consumer or a later change would treat the operation report as the neutral infrastructure-readiness result, or add an eligibility verdict to it
- **THEN** it MUST be refused
- **AND** the report MAY be declared a candidate INPUT to that contract when that contract is proposed

#### Scenario: The compute round trip disagrees
- **WHEN** the fixed-input digest computed on the host differs from the fixed expected digest
- **THEN** the operation MUST fail with both values recorded

### Requirement: Routing a route through the clearing lane retires the old route
Routing an existing direct governed-host route through the clearing lane SHALL
RETIRE that route in the same change, and SHALL NOT leave it dormant. A
retired route's workflow allowlist entry SHALL be removed and its member SHALL
be struck from the grandfather enumeration in the same act, so no dormant
second door survives a migration.

A route that is retired SHALL be retired in both places at once — the live
allowlist and the in-repo enumeration — and a member present in one and
absent from the other SHALL be a finding of the single-door attestation
rather than a tolerated skew. The precedent this contract carries in its own
first slice is the standalone runner-readiness diagnostic workflow, which
retires into the `readiness-diagnostic` operation as that operation lands.

#### Scenario: A grandfathered lane becomes a clearing operation
- **WHEN** a change registers a clearing operation replacing a grandfathered workflow's host job
- **THEN** the same change MUST remove that workflow's host job and its allowlist entry
- **AND** the grandfather enumeration MUST shrink by that member

#### Scenario: A migration leaves the old route in place
- **WHEN** a change adds a clearing operation for work an existing direct route still performs
- **THEN** the change MUST be refused as leaving a dormant second door

#### Scenario: The standalone readiness workflow retires
- **WHEN** the `readiness-diagnostic` operation lands in the clearing workflow
- **THEN** the standalone runner-readiness diagnostic workflow MUST be deleted in the same change
- **AND** it MUST NOT be added to any workflow allowlist

### Requirement: An authoring-time guard refuses a host job outside the door
The clearing repository SHALL carry a REQUIRED CHECK that refuses, at
pull-request time, any workflow file which declares a job on a governed
runner group and is neither the clearing workflow nor a current member of the
grandfather enumeration. A bypass MUST be caught where it is authored rather
than discovered later as an unclaimable queued run, because fail-closed
enforcement without authoring-time detection produces a silent stuck job
indistinguishable at a glance from a busy host.

The guard SHALL resolve a job's declared runner group STRUCTURALLY, from the
workflow's job definition, and SHALL NOT be a text search for group names: a
concurrency group or other same-named value is not a host job, and a guard
tuned to ignore such matches is a guard tuned to miss real ones. A job's
declared runner GROUP SHALL be a literal value, and a group given as an
unresolvable expression SHALL be refused rather than guessed at; a job's
dispatch LABEL MAY be an expression, because the group is the boundary the
provider enforces while the label routes within it and is verified against
the sealed request before dispatch.

The guard SHALL also refuse a change that adds a member to the grandfather
enumeration, and SHALL treat the enumeration as the authority for which
non-clearing files may declare a host job.

#### Scenario: A new workflow targets a governed group
- **WHEN** a pull request adds or edits a workflow file, outside the clearing workflow and the enumeration, that declares a job on a governed runner group
- **THEN** the required check MUST fail
- **AND** the failure MUST name the file and the group

#### Scenario: A concurrency group shares a runner group's name
- **WHEN** a workflow declares a concurrency group whose name resembles a governed runner group
- **THEN** the guard MUST NOT report it
- **AND** the guard MUST reach that conclusion structurally rather than by pattern exception

#### Scenario: A job hides its group behind an expression
- **WHEN** a job's declared runner group is an expression the guard cannot resolve at authoring time
- **THEN** the check MUST fail
- **AND** the group MUST be required as a literal value

#### Scenario: A dispatch label is an expression
- **WHEN** a permitted host job's dispatch label is supplied as an input expression while its group is a literal
- **THEN** the guard MUST allow it
- **AND** the label MUST be verified against the sealed request's declared label before dispatch

### Requirement: Every dispatch is recorded, and the single door is attested rather than assumed
The clearing workflow SHALL RECORD every dispatch it clears and every
request it refuses, and each record SHALL carry the verified provenance —
the resolved originating repository and workflow, the resolved source commit,
the job id, the operation, the runner group and dispatch label, the
data-handling classification, and the outcome — together with the CLAIMED
values where they differed from the resolved ones. A refusal SHALL be
recorded with its ground named, because a boundary that logs only successes
cannot evidence what it stopped.

Because the door is single, that record IS the complete audit of everything
that ever reached the governed host. That completeness claim is TRUE ONLY
WHILE THE DOOR IS SINGLE, so the estate SHALL ATTEST the door periodically
rather than assume it: an attestation reads each governed runner group's
admitted repositories and workflow allowlist from the provider's API and
compares them against the expected set — the clearing workflow's path plus
the current grandfather enumeration, and the clearing repository alone — and
a divergence in either direction SHALL be a finding that names what was
found and what was expected.

The RESIDUAL SHALL be declared rather than implied: runner-group membership
and workflow allowlists are provider-side configuration outside the
repository's version control, changeable by an administrator with no pull
request. This contract does not make that configuration versioned, and it
SHALL NOT be read as claiming to; it makes a change to it OBSERVABLE within
one attestation cycle, and the ledger's completeness claim is conditioned on
that attestation being current and green.

The dispatch record SHALL NOT restate vocabulary another capability owns: it
REFERENCES a signed execution chain where one governs the work rather than
defining a second log, and it is distinct from the enrollment audit record,
whose subject is which hosts may BE runners rather than what was CLEARED to
one.

#### Scenario: A dispatch clears
- **WHEN** the clearing workflow admits a sealed request and dispatches it
- **THEN** a record MUST be written carrying the resolved provenance, the operation, the lane, the handling classification, and the outcome
- **AND** any claimed value that differed from the resolved value MUST be recorded beside it

#### Scenario: A request is refused
- **WHEN** the clearing workflow refuses a request for any ground in this capability
- **THEN** the refusal MUST be recorded with its ground named

#### Scenario: The attestation finds an extra allowlist entry
- **WHEN** a governed runner group's workflow allowlist contains a path that is neither the clearing workflow nor a current grandfather member
- **THEN** the attestation MUST report a finding naming the group, the unexpected path, and the expected set

#### Scenario: The attestation finds an extra admitted repository
- **WHEN** a governed runner group admits a repository other than the clearing repository
- **THEN** the attestation MUST report a finding naming that repository

#### Scenario: The completeness of the audit is claimed
- **WHEN** the dispatch record is presented as the complete audit of what reached the governed host
- **THEN** the claim MUST cite a current, green single-door attestation
- **AND** without one the record MUST be presented as complete only for dispatches that came through the door
