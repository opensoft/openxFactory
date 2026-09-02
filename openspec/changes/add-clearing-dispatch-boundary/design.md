# Design: the clearing and dispatch boundary — one door, and the machinery that keeps it one

## Context

The estate runs two governed execution hosts, both Cloud PCs, reached through
two provider-side runner groups. The state of that configuration on
2026-09-01, read from the provider API rather than remembered:

| group | repositories admitted | workflow paths allowlisted | runner |
|---|---|---|---|
| `xfactory-artifact-workers` (id 5) | `opensoft/xFactory`, **`opensoft/codexFactory`** | 6 | `xfactory-artifact-cpc-brett01`, label `host-rider-cpc-brett01` |
| `xfactory-execution-lane-workers` (id 7) | `opensoft/xFactory` | 1 | `xfactory-coding-cpc-brett01`, label `host-coding-cpc-brett01` |

TEN workflow files in xFactory declare a job on one of those groups. Seven
are allowlisted and work. Two — `ideation-organizer-worker.yml` and
`review-lane-worker.yml` — declare a group job and are NOT allowlisted, so
their children are already fail-closed today, which nothing reports. The
tenth is `runner-readiness-diagnostic.yml` (`opensoft/xFactory#188`, merged
`4fffb6e5`),
never allowlisted and, under Brett's option-1 ruling, never to be: its
checks become the clearing lane's first operation.

Those seven-plus-two are the NINE grandfathered worker workflows this design
speaks of: `execution-lane-coding-worker`, `council-deliberation-worker`,
`review-lane-worker`, `ideation-organizer-worker`, `dashboard-image-worker`,
and the four doc-health workers (analysis, readiness, cataloger,
derive-possibles).

The estate ALREADY moves work to those hosts the way the ruling describes.
`execution-lane-coding-worker.yml` takes `source_run_id`, `source_sha`,
`correlation_id`, `bundle_digest` and `dispatch_label`; its first step
resolves the parent run from the provider API and refuses unless the run's
`head_sha` matches the claimed SHA and the run's `path` is exactly
`.github/workflows/execution-lane.yml`; it then downloads a sealed bundle
artifact and RECOMPUTES the bundle digest before running anything. So the
mechanics of this contract are not speculative. What is missing is the rule
that makes them the ONLY way in, and the enforcement that notices when they
stop being.

## Decisions

### D1 — Verification is API-side, never bundle-trusted

A sealed bundle is a set of CLAIMS made by whoever packaged it. Its internal
consistency proves only that the packager was consistent. So for every field
that has an authoritative provider-side answer — originating repository,
originating workflow path, source commit, dispatch identity, artifact
existence and its run of origin — the clearing workflow resolves the answer
from the API and compares, and the bundle's copy exists to be CONTRADICTED,
not consulted.

The three consequences that are easy to get wrong:

1. **An unreadable API refuses.** A verification that cannot be performed is
   not a verification that passed. Fail-closed here, as everywhere.
2. **The field stays in the bundle anyway.** It is what makes a disagreement
   detectable at all, and it is what a ledger entry records as "claimed"
   beside "verified".
3. **Fields with no authoritative provider answer are a different class.**
   Data-handling classification, required worker profile, permitted
   operation and output schema cannot be resolved from the API; they are
   checked against the CLOSED REGISTER and against policy instead. The
   contract must not blur the two classes, because "verified" applied to a
   field nothing could verify is the exact false assurance this design
   exists to prevent.

### D2 — Every host job lives physically inside the clearing workflow file

The provider evaluates a group's workflow allowlist against the workflow
file that DIRECTLY CONTAINS the job requesting the runner — not against the
top-level caller that triggered it. The estate's own configuration is the
evidence: all seven working entries name the WORKER file that physically
carries `runs-on.group`, and the parents that merely dispatch or call
(`execution-lane.yml`, `doc-health-nightly.yml`, `review-lane.yml`) appear
on no allowlist while their lanes function.

Therefore the clearing workflow cannot delegate its host jobs to a reusable
workflow, however much cleaner that would read. A reusable workflow holding
the host job would itself need an allowlist entry, and the single door would
become two — one of them a file whose path no operator remembers granting.
This is the one place where the contract dictates FILE LAYOUT, and it does
so because the enforcement is evaluated against file layout. THE NEUTRAL
REQUIREMENT IS PHRASED ONE LEVEL UP from this paragraph, deliberately: it
says the host-touching job must be declared in THE ARTIFACT THE PROVIDER
EVALUATES ITS ALLOWLIST AGAINST, and names the workflow file only as the
realization on this provider. The reasoning in this section is
GitHub-specific and stays that way — it is the evidence for the resolution,
not the rule — because a provider that evaluated its allowlist against
something else would keep the property and change the file layout.

The corollary is a real cost, stated rather than hidden: the clearing
workflow will grow one job per permitted operation, in one file, forever.
That is the price of the property, and the register being closed is what
keeps the growth governed.

### D3 — The grandfather enumeration converges, and only shrinks

Two dishonest options were available. Declare the nine existing workers
non-conformant, and the contract ratifies an estate that is instantly in
violation and stays there. Say nothing about them, and "one door" is a claim
contradicted by seven allowlist entries.

So they are ENUMERATED in-repo, as a closed list with an explicit terminal
state. The rules that make an enumeration a convergence rather than a
parking lot:

- **Append-never.** No workflow is ever ADDED to the enumeration. A new
  host-touching lane is a clearing operation or it is nothing.
- **Shrink-only, one retirement at a time.** Each member retires into a
  clearing operation, and its allowlist entry is removed in the same act
  (D4/L3). The enumeration and the live allowlist are compared by the L5
  attestation, so a member removed from one and left in the other is a
  finding.
- **Terminal state named.** One entry per group: the clearing workflow's
  exact path. The enumeration reaching empty is what "converged" means, and
  it is checkable rather than aspirational.
- **It is DATA, with group attribution and allowlist status.** The
  enumeration is a machine-readable file both consumers read (OQ3, settled),
  and each member declares which GOVERNED GROUP it targets and whether it
  currently HOLDS AN ALLOWLIST ENTRY. Neither field is bookkeeping: without
  the group, the attestation cannot compute one group's expected set;
  without the status, the two dark lanes below read as breaches instead of
  as the strictly-safer condition they are.

### D4 — Fail-closed is the floor, and it is not sufficient

Run `33381257642` proves the floor holds: a codexFactory-path job, on a
group that admits the codexFactory repository but not that workflow path,
was never claimable and never ran. Nothing executed ungoverned.

It also proves the floor is not enough. The run sat QUEUED for about
eighteen hours before a human noticed and cancelled it. A bypass attempt
under this contract produces, unaided, a silent stuck job — indistinguishable
at a glance from a busy runner, a paused host, or a bug. Hence the two
layers that surround the floor:

- **L4, at authoring time.** The guard turns "this will queue forever" into
  a red required check on the pull request that would have caused it. The
  eighteen hours become zero. WITH ONE CAPABILITY THE CLEARING REPOSITORY
  DOES NOT HAVE YET: measured 2026-09-01, none of `opensoft/xFactory`'s five
  active rulesets declares `required_status_checks` — the Tier-1 main
  protection (`18962101`) carries `pull_request`, `non_fast_forward` and
  `deletion`, the code-owner and stale-approval rulesets carry
  `pull_request`, the Copilot ruleset `copilot_code_review`, and the bot
  confinement ruleset push rules only. So "required check" is an OBLIGATION
  THIS DESIGN CREATES, not a mechanism it inherits: `tasks.md` §4.5 is the
  operator act that creates the rule naming `validate`. And even after it,
  ruleset `18962101`'s `bypass_actors` list — `OrganizationAdmin`, mode
  `always` — means a required check is bypassable by an organization
  administrator. That is the same residual class as the console itself: the
  guard buys authoring-time VISIBILITY, and the last word stays with the
  operator.
- **L5, continuously.** The attestation turns "the door is still single"
  from an assumption into a measurement.

Neither adds enforcement the provider does not already perform. Both add
OBSERVABILITY of enforcement, which is what was actually missing on
2026-09-01.

### D5 — The clearing surface is a sealed job object with an expiry

The ruling is explicit: not a committed folder of copied data. The design
reasons for it, since the ruling states the conclusion:

- A committed copy makes the boundary a MIRROR. Every selected file lands
  in a second repository's history, permanently, under whatever handling
  class it carried, and the retention decision is made once by whoever wrote
  the commit.
- A sealed object EXPIRES. Field 3's expiration is not decoration: it is
  what makes the bundle a request rather than a copy, and it is what a
  replayed handle runs into.
- A committed copy has no unique job identity. Two dispatches of the same
  path are indistinguishable in the ledger, and L5's completeness claim
  quietly stops being true.

The realization is a short-lived run artifact, which the estate's existing
workers already use for exactly this.

### D6 — The boundary RE-SEALS; the host is served from the clearing run

The ruling says the host receives only the sealed bundle and never
repository credentials. That has a mechanical consequence worth writing
down, because the obvious implementation violates it.

The producer's bundle is an artifact of the PRODUCER's run, in the
producer's repository. For the host to download it directly, the host's job
would need a token with read access to the producer repository's artifacts —
which is a repository credential for the originating repository, on the
host, which is the thing the ruling forbids. (The existing coding worker
downloads with `repository:` and `run-id:` inputs and `github.token`, which
works only because parent and child are the SAME repository.)

So the hosted clearing side ADMITS the bundle: it fetches the producer's
artifact using a scoped, short-lived, read-only credential held on the
CLEARING side (a `credential-contracts` record, custody declared),
verifies it against D1, and re-uploads it as an artifact of the clearing
run. The host then downloads from the clearing run with a token scoped to
the clearing repository alone — which is the token it already has.

The re-seal is also where verification EARNS something: the object the host
receives is one the clearing workflow has already read, hashed and admitted,
not one it merely pointed at.

### D7 — The L4 guard is structural, and the estate contains the case that proves it

A grep for the group names would be wrong today, before anyone tries to
defeat it. Two xFactory workflows carry

```yaml
concurrency:
  group: xfactory-artifact-worker
```

— a CONCURRENCY group whose name differs from the runner group
`xfactory-artifact-workers` by one character, in `doc-health-nightly.yml`
and `review-lane.yml`. A text search either flags them (and the guard is
noise a reviewer learns to override) or is tuned until it misses the real
thing.

So the guard PARSES the workflow and resolves `jobs.<id>.runs-on.group`.
Two rules follow:

- **The group must be a LITERAL.** `group: ${{ inputs.whatever }}` is
  unresolvable at authoring time and is refused as such, rather than
  guessed at. A guard that can be defeated by an expression is not a guard.
- **The LABEL may be an expression.** The estate's coding worker already
  uses `labels: ${{ inputs.dispatch_label }}`, because a parent chooses the
  attested runner at dispatch time. That is safe here: the label NARROWS
  within a group already restricted by repository and by workflow path, and
  the clearing workflow verifies the label against the bundle's field 7
  before dispatching. Group is the security boundary; label is routing.

The group rule is stated as a REFUSAL OF EXPRESSIONS, not as a refusal of
UNRESOLVABLE expressions. The weaker form invites a guard that tries to
resolve them, and an evaluator inside a guard is a second thing to defeat;
the strong form has one question with a syntactic answer.

**How the guard refuses an APPEND to the enumeration, and what that refusal
is worth.** The mechanism is a FROZEN ORIGIN SET: the guard's test holds the
enumeration's nine founding names as a constant and asserts that the live
enumeration's members are a SUBSET of it. A retirement shrinks the set and
passes; an addition breaks the subset relation and turns the check red. What
that is NOT is an unforgeable refusal — the data file, the guard and the test
all live in the repository whose changes they police, so one diff can edit
both the enumeration and the constant that guards it. So the honest claim,
and the one the spec makes, is that an append cannot happen SILENTLY: it is a
red check plus a diff touching the enumeration or the guard, and REVIEW OF
THAT DIFF is the backstop. Naming a review as the backstop is weaker than a
cryptographic refusal and stronger than the alternative on offer, which was a
constant in a test module that nobody would have looked at twice.

### D8 — No second vocabulary, stated as a table so a reviewer can check it

| this capability needs | it is already owned by | how this capability uses it |
|---|---|---|
| runner group, labels, trust tier, lease | `worker-enrollment-broker` | consumed by name; the ledger records the group/label a dispatch used, it does not define them |
| enrollment audit record | `worker-enrollment-broker` | left alone; its subject is who may BE a runner. The dispatch ledger's subject is what was CLEARED to one |
| digest construction | `signed-execution-chain` | the manifest hashes and the bundle digest use THAT construction; no second digest rule |
| transparency log | `signed-execution-chain` | a dispatch REFERENCES a chain where one governs the work (OQ2) |
| scoped short-lived credential | `credential-contracts` | the clearing side's admission credential is one of its records |
| job scope references | `neutral-job-envelope` | the sealed request seals a job; it is not a second job envelope |
| handling class, tenant/data-boundary attestation | `document-cataloging`, `ideation-routing` | field 9 cites the existing handling vocabulary; no second classification |
| what an agent may DO once running | `contracts/omnigent/` permission matrix | untouched. The register governs what may be DISPATCHED to a host, not what an executing worker is permitted; the constitutional `execute_final_action: false` is not weakened, restated, or referenced as authority |

**One row's owner is not promoted canon, and the table should not imply it
is.** `worker-enrollment-broker` — the owner of runner group, labels, trust
tier, lease, and the enrollment audit record — is the ACTIVE change
`openspec/changes/add-worker-enrollment-broker`, RATIFIED AND REALIZED at
`contract-v1.29` but NOT under `openspec/specs/`. It is therefore
RATIFIED-BUT-UNPROMOTED, and this capability consumes its vocabulary on that
footing. The practical consequence is small and worth stating anyway: the
vocabulary is authoritative enough to consume and not yet promoted, so a
future promotion of that capability may reword it, and this packet cites it
by name rather than quoting its text. The other rows'
owners — `signed-execution-chain`, `credential-contracts`,
`neutral-job-envelope`, `document-cataloging`, `ideation-routing`,
`contracts/omnigent/` — are cited as they stand.

### D9 — The operation report is NOT the awaited infrastructure-readiness result

This is the one place where the packet pulls against promoted canon, so it
is recorded rather than smoothed.

`document-cataloging` and `ideation-routing` BOTH say the same thing, in the
same words: a hosted preflight *"SHALL consume the current neutral
infrastructure-readiness result when that contract is promoted"*, and until
then the existing runner/heartbeat preflight is the bridge and *"MUST NOT be
generalized into a competing readiness-result schema."*

An operation literally named `readiness-diagnostic`, emitting a structured
report about a host, walks straight into that clause. The distinction the
contract draws, and must keep drawing:

- The awaited **readiness RESULT** is a DECISION INPUT: orchestration
  consults it BEFORE dispatching to decide whether the host is fit, and it
  carries profile, version, heartbeat freshness, boundary attestation and
  handling authorization.
- This capability's **operation report** is EVIDENCE FROM A DISPATCH: the
  output of one cleared job on one host at one moment, produced by going
  THROUGH the boundary, and useless as a precondition for itself.

So: this packet does not define a readiness-result schema, and the register
entry's output schema for `readiness-diagnostic` is an OPERATION REPORT
shape. When the neutral infrastructure-readiness contract is proposed, this
report is a candidate INPUT to it and the register entry re-points at it;
the report does not become it by growing fields. If a future author is
tempted to add `eligible: true` to this report, that is the moment the
non-competition clause is being broken.

### D10 — Ten fields, and why the awkward ones stay

The ruling enumerates ten. None is dropped, and three deserve their reason
in writing:

- **Field 3, expiration** — what makes the object a request rather than a
  copy (D5), and what a replayed handle hits.
- **Field 7, exact group AND unique dispatch label** — the group is the
  security boundary and the label is the routing choice (D7). Both are in
  the bundle so the clearing workflow can refuse a bundle asking for a lane
  its operation is not registered for, before any runner is involved.
- **Field 10, signature OR trusted hosted-workflow provenance** — a
  disjunction on purpose. The estate has no signing identity for factory
  packaging today; requiring a signature would make the contract
  unimplementable, and requiring nothing would make field 10 decoration.
  Trusted hosted-workflow provenance is the interim floor, verified API-side
  per D1, and OQ1 carries the decision of when a signature becomes required.

### D11 — What this slice deliberately does not do

- **No CODING operation.** The register is closed and gains entries by
  governed change; the coding operation arrives with the packaging
  realization that produces its bundles.
- **No factory-side PACKAGING realization.** Named successor
  `realize-factory-bundle-packaging`. Writing the producer half here would
  fix codexFactory's implementation before the boundary it must satisfy has
  been ratified.
- **No hosted FINALIZER implementation.** The OBLIGATION is a requirement
  here, because it is the ruling's; the finalizer itself is written against
  the first returning operation, not against a guess about one.
- **No throttling or emergency-shutdown mechanics.** The ruling names them
  as reasons the boundary should exist, and a single door is what makes them
  possible in one place. Specifying them here would be extending the ruling
  rather than encoding it.
- **No group, host, runner, label, or credential provisioning.** Those exist
  already and are operator surface.
- **No console change.** The operator's one act per group is in `tasks.md`
  because it must happen; it is not this repository's artifact.

### D12 — The register is CLOSED, and that is a governance choice not an ergonomic one

An open register — operations declared per-lane, in the workflow, by the
author who needs one — would make every new lane a self-service widening of
what the estate's hosts do, reviewed only as workflow YAML. Closing it
means adding an operation is a contract change with a spec delta and a
reviewer, and it means the ledger's operation column has a finite, known
range. It costs a governed change per operation. That is the intended cost.

## Open questions carried, with a recommendation each

### OQ1 — When does a signature become REQUIRED for field 10? (hardest)

Trusted hosted-workflow provenance is the interim floor (D10). The question
is what promotes it. **Recommendation**: require a signature when the
producer is a repository whose write population differs from the clearing
repository's — i.e. the first cross-organization producer — and express the
requirement against `trust-anchor`'s certificate record rather than minting
a bundle-signing vocabulary. Settle before the sealed-bundle schema is
authored, since field 10's shape depends on it.

### OQ2 — Is the dispatch ledger a new record or a transparency-log entry?

`signed-execution-chain` owns a signed transparency log. A dispatch is not a
chain link, but a chain that runs on a governed host has a dispatch in its
history. **Recommendation**: the ledger is its own record kind with a
REFERENCE to the chain where one governs the work, not a second log format
and not a chain link. Settle before the ledger schema is authored.

### OQ3 — Where does the grandfather enumeration physically live? — SETTLED AT REALIZATION, PENDING RATIFICATION

**Status: SETTLED AT REALIZATION, carried to ratification for confirmation.**
The question's history stays below rather than being deleted, because a
settled question whose alternatives have been erased reads like a question
nobody asked, and the rejected candidates are the reason the answer is the
answer.

**The question as it stood.** Candidates: the clearing workflow's own
comments (closest to what it describes, invisible to tooling), a file in
xFactory (tool-readable, but the neutral contract cannot cite it), or the
neutral register instance (citable, but it enumerates one repository's files
in a domain-neutral contract). **The recommendation was**: an xFactory-side
declaration read by the L4 guard and by the L5 attestation, with the NEUTRAL
contract requiring only that such an enumeration exist, be closed, and
shrink. Settle at realization.

**The settlement, and what forced it.** Realization began with the
enumeration as a CONSTANT INSIDE THE GUARD'S TEST MODULE — the fourth
candidate, which the question had not listed because nobody proposes it, one
merely arrives at it. That fails the recommendation's own condition on a
detail the question had not surfaced: the L5 ATTESTATION IS A SECOND
CONSUMER, and a list inside one consumer's test is a list the other consumer
must copy. Two copies of the closed set is the failure mode the closed set
exists to prevent.

So the enumeration is a GOVERNED DATA FILE:
`.github/clearing/grandfather-enumeration.yaml` in `opensoft/xFactory`, read
by BOTH the L4 guard and the future L5 attestation. Each member declares:

| field | why it is there |
|---|---|
| workflow filename | the subject — what the allowlist entry would name |
| governed runner group | REQUIRED for the attestation: the expected allowlist of one group cannot be computed from a list that does not say which group a member belongs to |
| the governed-host job ids in that file | so the guard reports the job, not just the file, and so a file gaining a SECOND host job is visible |
| allowlist-entry status (`present` \| `absent`) | REQUIRED to keep a dark lane from reading as a breach: an enumerated member with no entry is already fail-closed, which is the opposite condition from an entry nobody granted |

The NEUTRAL contract still cites none of this. It requires only that such an
enumeration EXIST, be CLOSED, carry per-member GROUP ATTRIBUTION and
ALLOWLIST STATUS, and SHRINK — which is the recommendation's shape, with the
two fields the attestation's definition turned out to need.

The APPEND REFUSAL moved with it and is described in D7: the test keeps the
nine founding names as a frozen ORIGIN set and asserts the data file's
members are a subset, with review of any diff touching the file or the guard
as the declared backstop.

### OQ4 — What cadence for the L5 attestation, and where does a finding land?

**Recommendation**: ride the existing nightly lane rather than adding a
schedule, and emit a doc-health-shaped finding, so a divergence surfaces
where the estate already looks. Settle at realization; the requirement
states the obligation and not the cadence.

## Risks

- **The console remains unversioned.** An administrator can widen a group
  with no pull request. L5 detects it after the fact, within one attestation
  cycle. This is stated in the requirement text rather than left to be
  discovered, and it is the residual the ruling itself acknowledges.
- **One file, many jobs.** D2 forces the clearing workflow to accumulate a
  job per operation. Mitigation: the closed register bounds the growth, and
  the non-host parts of an operation may live anywhere.
- **The re-seal is a second copy.** D6 means the bundle exists twice for the
  life of two runs. Mitigation: both are expiring run artifacts, and the
  alternative is a repository credential on the host.
- **Two lanes are dark today.** `ideation-organizer-worker` and
  `review-lane-worker` declare group jobs with no allowlist entry, so they
  are already failing closed with nothing reporting it. This packet does not
  fix them; the L4 guard makes their state visible, and `tasks.md` carries
  the disposition — retire into an operation, or remove the reference.
- **The `artifact-only` label on the coding runner — and the hazard is
  SYMMETRIC.** Runner `xfactory-coding-cpc-brett01` in the execution-lane
  group carries labels `artifact-only`, `rider` and `coding-patch`. A
  coding-lane host labelled `artifact-only` is at best a leftover and at
  worst a routing hazard, since a job requesting `artifact-only` could land
  on the coding host. The symmetry, measured the same day and easy to miss
  when only one runner is inspected: the ARTIFACT runner
  `xfactory-artifact-cpc-brett01` ALSO carries `artifact-only` AND `rider`.
  So neither of those two labels discriminates the lanes IN EITHER
  DIRECTION — a job requesting `artifact-only` or `rider` may land on
  either host — and the only labels that do discriminate are
  `coding-patch` (coding host only), the per-lane
  `host-coding-cpc-brett01` / `host-rider-cpc-brett01`, and the artifact
  host's task labels (`doc-analysis`, `document-cataloger`,
  `ideation-readiness`, `derive-possibles`, `dashboard-image`). This is why
  the contract makes the GROUP the boundary and the per-lane
  `host-*-cpc-brett01` label the routing choice: the shared labels are not
  a boundary and were never one. `tasks.md` §5.3 keeps the coding runner's
  verbatim label set as the measurement of record; investigation is a task,
  not a requirement.
