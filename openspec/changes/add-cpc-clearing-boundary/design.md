# Design: the origin-identity and sign-on-return extension to the clearing boundary

## Context

The operator's ruling of 2026-09-01 produced TWO governance packets, not one.
`add-clearing-dispatch-boundary` — ratified the same day, ten requirements, its
realization already live on xFactory main — is the boundary itself. This packet
is the SAME-DAY EXTENSION recorded on codexFactory issue #156: per-repository
origin keys and sign-on-return.

An earlier draft of this packet did not know the first one existed and
re-authored about seven of its requirements in divergent vocabulary. Adversarial
review caught it. This design is written to the corrected scope, and its first
decision is the scope itself.

### What the basis already settles, and is not revisited here

The single door and its append-never, shrink-only grandfather enumeration; the
TEN-field sealed request; the refusal of any second digest, envelope, or
handling-classification vocabulary; the short-lived sealed job object; the
provider-API verification of the fields that have authoritative answers and the
refusal to call the others "verified"; the re-seal and the clearing side's own
scoped read-only credential; the producer's dispatch credential scoped to
dispatching the clearing workflow alone, with the compromised-producer residual
stated rather than hidden; the closed permitted-operations register with
`readiness-diagnostic` as entry one; the hosted finalizer; the authoring-time
guard; and the periodic single-door attestation.

### What the ruling's extension adds, which the basis does not reach

One Ed25519 origin key per factory, private half in its hosted environment and
public half registered in openxFactory, verified at clearing alongside — never
instead of — provider provenance; origin attestation and seat attestation held
to be distinct keys and distinct acts; and seat-return signing resolved to
option (b), sign-on-return, with seat private halves never touching the host and
no key re-minted.

## Goals / Non-Goals

**Goals** — close field (10)'s disjunction for a registered originator; add
origin-signature verification as its own conjunctive class; state sign-on-return
as a neutral rule; make act distinctness enforceable by something that can
actually be checked today.

**Non-Goals** — no re-authoring of the basis; no eleventh manifest field; no
second digest or envelope vocabulary; no new contract schema; no workflow, key,
row, or authorization entry; and no claim that anything is in force which the
estate cannot yet perform.

## Decisions

### D1 — Origin keys live in a SIBLING register at `governance/factory-identity/` **DECIDED, AND SINCE CONFIRMED BY THE OPERATOR**

The alternative was rows with a new `act` value in
`governance/review-authority/register.yaml`. Rejected, chiefly because the
ruling's act-distinctness requirement becomes STRUCTURAL across two registers
read by two reader invocations, where inside one file it is a field predicate
one mistyped `act:` from collapse. Supporting grounds: the intake register's
rows answer "may this holder decide about this repository's objects" while an
origin row answers "did this request come from this repository" — provenance,
not decision authority; the consumers are different parties with different
staleness regimes; custody differs; and the blast radius of a compromised origin
key (bounded by provider verification, the closed operation register, and the
hosted finalizer) differs from that of a compromised review key. The operator
confirmed this decision on 2026-09-01.

### D2 — The sibling register does NOT inherit the seat-council spelling **DECIDED**

The intake register carries council-seat rules — an agent-holder prefix and a
per-seat key-block shape — that exist because its subjects are seated agents. An
originating repository is not one. A conformant origin row written in that
spelling would fail rules written for a different subject, so the origin
register declares `holder_class: organisation` and carries no seat-key block,
and the spec says so explicitly rather than leaving the omission to be inferred.

### D3 — The sibling inherits the "deliberately kindless" REGISTER discipline; the records beside it stay kinded **DECIDED**

The intake register carries `register_version` and rows and no
`schema_version`/`kind`, on the recorded ground that no contract schema should
be minted for a shape with one instance. This is instance TWO; two does not fire
the rule of three, so the discipline is kept and the trigger is recorded here so
the third register's author finds it. Wallet, grant, and attestation records
beside it carry `schema_version` + `kind` from the pinned neutral vocabulary.

### D4 — MODIFY three of the basis's ten requirements, carrying them verbatim, each under its OWN per-requirement `Modified over` marker **DECIDED**

`govern-sibling-added-modified-deltas` (ratified 2026-08-31) governs precisely
this shape: a `## MODIFIED Requirements` block whose requirement exists only as
an active sibling's `ADDED`. Its third reserved marker form is required, at most
one PER REQUIREMENT, naming the basis change-id as a code span, carrying this
change as its `by` identifier and a nonempty ` — ` reason tail.

**THE MARKER IS PER REQUIREMENT, NOT PER SECTION, AND THE FIRST DRAFT GOT THIS
WRONG.** One paragraph under the `## MODIFIED Requirements` heading looks like it
declares the whole block; it declares nothing, and the pairing arm reports every
requirement in the block as carrying no marker of the reserved form. Each
MODIFIED requirement here therefore carries its own marker inside its own body,
placed AFTER the requirement's opening sentence so the SHALL stays on line one,
and each states the reason specific to what that requirement's addition does. Because a MODIFIED requirement REPLACES its basis
wholesale, every original scenario is carried verbatim beside the new ones —
latent scenario loss across sibling packets being the defect family issues #329
and #330 record.

### D5 — Field (10) tightens only for a REGISTERED originator **DECIDED**

Making the signature unconditional would break every producer before a key is
issued and would make the register a precondition of the boundary rather than a
strengthening of it. Conditioning on registration means issuing a key TIGHTENS a
producer and never loosens one, and the boundary stays usable in the interval
before any key exists — which is the interval it is in today.

### D6 — Verification is conjunctive, and reported as a third class **DECIDED**

The basis carefully separates provider-VERIFIED fields from policy-CHECKED ones
and refuses to report the second as the first, on the ground that "verified"
applied to a field nothing could verify is false assurance. The origin signature
is neither: it is verified, but against a register rather than the provider. It
therefore gets its own reported outcome, and the spec carries both failure
directions as scenarios — valid signature over contradicted provenance, and
confirmed provenance with no verifying signature — because a conjunction stated
once decays into an either/or in implementation.

### D7 — The policy-checked fields are RESOLVED FROM the register, not read from the bundle **DECIDED**

The basis validates the bundle's claimed operation against the closed register.
This packet takes the further step: the class constraints, worker profile,
permitted lanes, and output schema the dispatch RUNS ON are the register entry's,
and the bundle's copies are claims compared against it. Validating a claim and
executing on the register's own answer are different acts, and only the second
denies a producer the ability to choose its own worker profile or lane by
writing them into a bundle it controls. On disagreement the register governs and
the request is refused rather than silently corrected — a silent correction
would hide a producer defect or an attack.

### D8 — Act distinctness ships as a CHECKED DISJOINTNESS RULE, and the read-time half is declared not yet in force **DECIDED**

Review found the fail-open direction: the pinned openXwallet reader indexes every
wallet and grant record in the tree into one context, so an origin wallet under
`governance/factory-identity/wallets/` would resolve as a review row's
`wallet_ref`. Writing "a key registered for one act is refused for the other" as
though it were in force would have been a contract asserting a property the
estate does not have.

So the enforceable half ships now — a validator asserting that no `key_id`, no
identifier, and no public-key fingerprint appears in both register families,
checkable today by reading two trees — and the read-time refusal is written as
an explicitly NOT-YET-IN-FORCE obligation whose reader dependency is named. The
spec carries a scenario that REFUSES the premature claim, so the gap cannot be
closed by assertion.

### D9 — `factory-origin-identity` declares its OWN staleness bound, and at-clearing revocation is declared unrealizable for now **DECIDED**

The withdrawn draft borrowed the review side's revocation lifecycle and asserted
revocation "re-checked at clearing". Review found that mechanism is four unmerged
PRs with no automatic projection refresh on the openxFactory side. Borrowing an
unbuilt mechanism to make a contract look stronger is the failure this estate's
own doc-health rules exist to catch. This capability therefore declares its own
bound and its own ceiling, states that propagation is no faster than the view a
consumer holds, and carries a scenario that REFUSES any claim that revocation is
effective at clearing while no projection path exists.

### D10 — Workspace disposal rides the dispatch record **DECIDED**

The withdrawn draft said an unprovable wipe "SHALL be reported as a governance
finding" — with no reader, no surface, and no family to report it. The basis
already requires a dispatch record per dispatch and already attests that audit's
completeness, so disposal evidence becomes a FIELD of that record and the
existing attestation is what reads it. Same obligation, an actual enforcer.

### D11 — Convergence is the basis's, and is NOT restated here **DECIDED, against a review suggestion**

Review asked for a transition requirement naming the grandfather enumeration as
the only legal non-door entry. The basis ALREADY ratifies exactly that — the
enumeration is append-never and shrink-only, each member declares its group and
whether it holds an allowlist entry, and the basis states in terms that
convergence is a TERMINAL STATE and not an entry condition, so the interval
before the operator admits the clearing path is a not-yet-converged state and
not a breach. Adding a requirement saying the same thing would be the exact
duplication this rework exists to remove. It is cited in the proposal instead,
and this decision records why no requirement was written.

### D14 — The attestation's read set is widened by a MODIFIED block, not by reaching in from outside **DECIDED**

The ADDED workspace-disposal requirement makes disposal evidence a field of the
dispatch record, and then says the periodic attestation reports a missing one.
That second half is an EXTENSION OF A RATIFIED REQUIREMENT — the basis's
"Every dispatch is recorded, and the single door is attested rather than
assumed" — written from outside it, which is precisely the undeclared coupling
`govern-sibling-added-modified-deltas` exists to catch. The alternative was to
narrow the ADDED requirement so it made no claim on the attestation, leaving the
disposal field recorded but unread. Rejected: an evidence field nothing reads is
not evidence. So the basis requirement gets its own MODIFIED block, carried
verbatim with its own marker, adding one field to what the attestation READS and
nothing to what it AUTHORIZES.

### D12 — Two digest constructions, named, with the manifest subject owed by a tranche widening **DECIDED**

The basis forbids a second digest vocabulary, and the first pass took that to
mean "one construction covers everything". It does not. The estate's canonical
construction is `xfc-jcs-sha256-1` — JCS over a JSON value — and its
`digest_subject` enumeration is CLOSED at seventeen members, none of them a
request, return, or bundle manifest. Two consequences, both stated in the spec
rather than glossed. First, an origin signature over the manifest needs a
manifest SUBJECT admitted to that enumeration, which is a tranche widening of
subjects and never a second construction — the one way that file's own header
says it is meant to move — so until it lands the requirement is reported
UNREALIZABLE rather than satisfied. Second, per-file content hashes are not JSON
values at all: canonical JSON has nothing to canonicalize in a byte stream, so
they are plain algorithm-tagged SHA-256 over bytes. Naming both is what keeps
this from being the second vocabulary the basis refuses: one construction for
JSON values, one byte hash for file content, both already in use, neither
invented here.

### D13 — The inbound re-seal is stated, not left to symmetry **DECIDED**

The basis's re-seal requirement is OUTBOUND ONLY: the clearing side admits the
producer's sealed object and serves the host from its own. Nothing in the basis
or in the first pass of this packet said what happens on the way back, and
codexFactory PR #165 currently takes the return path "by symmetry". Symmetry is
not a requirement. An originator reading the execution host's artifact directly
would need a credential into the execution estate — reintroducing on the return
path exactly the cross-boundary reach the outbound rule removes — so the return
is admitted, verified, re-sealed, and re-served from the clearing side, and this
packet ADDS that requirement rather than filing it as a question. It is added
here rather than left to #555's realization because it is a contract gap, not a
realization detail, and the packet that noticed it is the cheapest place to
close it.

## Risks / Trade-offs

- **Two packets now touch one capability**, and the ordering obligation is real:
  this one archives after the basis. Declared in the front matter and carried by
  the marker.
- **Merge order is load-bearing.** #555 merges first; if this packet led, the
  three contested warnings would enter the baseline and #555 would resolve them
  uncited, becoming three errors. The disposition rows are the belt — and they
  live in the AGGREGATION repo, so they are a cross-repo act (tasks § 5.3), not
  something this PR can carry.
- **The pairing arm cannot see the basis until #555 merges.**
  `modified-block-currency` reports three contested warnings saying the MODIFIED
  blocks resolve to no promoted requirement and no active sibling's addition,
  because the ratified basis is not in this tree. The finding is right, the
  marker is already present for when it is, and the condition is cited in
  tasks § 1.9 rather than dispositioned away.
- **The disjointness rule is weaker than read-time refusal.** Accepted openly:
  it is what can be enforced before the reader is scoped, and the spec says so
  rather than implying more.
- **Field (10)'s conditional tightening means two classes of producer** coexist
  until every originator holds a key. Intentional; the alternative blocks the
  live boundary.
- **Register-resolved constraints mean the register must be readable at
  dispatch**; an unreadable register refuses, consistent with the basis's
  treatment of an unreadable provider API.

## Open Questions

### OQ1 — How does a projection of the factory-identity register reach the clearing workflow? **OPEN**

Four shapes, none chosen: a scheduled projection refresher publishing a
bounded-staleness view; a checked-in digest-pinned projection in the clearing
repository, re-pinned by a governed sync; a live cross-repository read at
clearing time; or a runtime authority lookup. The trade is the same each time —
propagation speed against a new dependency in the admission path — and D9's
honesty clause stands until it is settled: whatever bound the chosen shape
supports is the real ceiling on revocation.

### OQ2 — Does the neutral job envelope carry the bundle manifest, or reference it? **RESOLVED: REFERENCE**

Resolved rather than left open, because the basis settles it. The sealed request
is the basis's TEN declared fields and the basis forbids defining a second
job-envelope, handling-classification, or digest vocabulary — so carrying the
manifest INTO `neutral-job-envelope` would be minting exactly the second
vocabulary that is forbidden. The manifest is referenced, not carried, and NO
manifest schema is added by this change; the code surface shrinks accordingly.

### OQ3 — Who scopes the review-authority reader so the read-time refusal becomes true? **OPEN**

The reader is pinned vocabulary owned outside this repository. Three routes: a
vocabulary change in the pinned repository scoping wallet and grant resolution
to the invoking register; a consumer-side check beside the reader invocation
here; or leaving the disjointness rule as the whole of the enforcement. Named as
an openXwallet dependency task; D8's not-yet-in-force clause holds until it
lands.
