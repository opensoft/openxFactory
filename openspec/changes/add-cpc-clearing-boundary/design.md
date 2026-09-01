# Design: the clearing boundary — sealed bounded requests and per-factory origin keys

## Context

On 2026-09-01 the operator refused the obvious way to let one factory run work
on another estate's shared hardware — authorize the factory's repository at the
execution surface — and commissioned the inverse as governed design. This
document is the neutral half: the contract two capabilities express, the
decisions already taken by the ruling, the decisions this design takes on top
of them, and the questions left open on purpose.

The vocabulary is deliberately neutral. An **originating factory** is any
domain factory that needs bounded work executed somewhere it does not own. An
**execution estate** is the party that owns the hardware and its authorization
surface. The **clearing boundary** is the estate's single admission point. The
estate that provoked the ruling and the factory that provoked it are named in
this change only as dependent realizations, never as contract content.

### Rulings already taken (operator, 2026-09-01 — decided inputs, not open)

- The execution estate is THE clearing and dispatch boundary. Authorization
  lists stay estate-only. No factory is broadly authorized to originate
  execution directly.
- Cross-factory work reaches the estate as a sealed bounded request, through
  hosted packaging → clearing → sealed dispatch → hosted finalization.
- The clearing surface is not a committed folder; it is a short-lived sealed
  job object.
- The manifest's field set is enumerated by the ruling and the clearing
  boundary verifies those fields against the hosting platform's API rather
  than trusting the bundle.
- Readiness becomes the clearing lane's FIRST operation; the authorization
  surface converges to one permanent entry per execution group, and the
  standalone readiness diagnostic retires into the clearing operation.
- Seat-return signing is **option (b), sign-on-return**: the estate produces
  unsigned results; the factory's hosted workflow verifies the sealed return
  and signs there. Seat private halves never touch the estate; no key is
  re-minted.
- Each factory holds **one Ed25519 origin key**, private half in its hosted
  environment, public half registered in openxFactory under the
  register/wallet/grant pattern, verified at clearing ALONGSIDE — never
  instead of — platform provenance. Origin attestation and seat attestation
  are distinct keys and distinct acts.

### Why the inversion is the whole design

The refused shape and the sanctioned shape differ in exactly one property:
what grows when a factory is added. In the refused shape, adding a factory
widens access to the hardware. In the sanctioned shape, adding a factory adds
a register row behind an admission point whose authorization footprint does not
move. Every other property — no credentials in the estate, no clone on the
target, bounded blast radius from a compromised factory workflow, one place for
audit and shutdown — follows from that one, and none of them is achievable in
the refused shape at any amount of care.

## Goals / Non-Goals

**Goals**

- Express the sealed bounded request, its verification, its isolation, its
  return path, and its attestation as a neutral contract any estate and any
  factory can conform to.
- Make the origin identity a *registered, revocable* thing with declared
  custody, reusing the ratified wallet/grant/custody vocabulary rather than
  inventing a second key story.
- Make origin-versus-review act distinctness STRUCTURAL, so that satisfying
  one act with the other's key is impossible rather than merely forbidden.

**Non-Goals**

- No workflow is written here, in any repository.
- No key is minted, no register row is issued, no authorization list is edited.
- No estate topology, runner group, label value, or secret name is contract
  content; those appear only as dependent-realization detail.
- The clearing boundary is not a job scheduler and does not replace the
  neutral job envelope; it admits work into an estate.

## Decisions

### D1 — Origin keys live in a SIBLING register, not as an extension of the review-authority intake register **DECIDED**

The alternative was to add rows with a new `act` value to
`governance/review-authority/register.yaml`. Rejected, on five grounds:

1. **The act-distinctness requirement is the point, and a sibling makes it
   structural.** The ruling requires that a key registered for one act be
   REFUSED for the other. Inside one file that is a field predicate — one
   mistyped `act:` and an origin key becomes review authority, and a single
   authorized write to that file can silently promote one. Across two
   registers read by two reader invocations for two acts, cross-satisfaction
   is not a rule to enforce but a path that does not exist.
2. **The existing register is scoped to authority over governed OBJECTS in a
   target repository** — its row shape is holder × target_repo × act × tier ×
   grant, answering "may this holder decide about this repository's objects".
   An origin row answers "did this request come from this factory", which is
   provenance, not decision authority. Same key machinery, different question,
   different consumers.
3. **The consumers are different parties with different trust paths.** The
   intake register is read by the review lane inside this repository's REQUIRED
   wallet-validation check. The factory-identity register is read by an estate's
   clearing workflow in a DIFFERENT repository, through a projection whose
   staleness must be bounded for a real-time admission decision. One register
   would have to serve both staleness regimes; two can each declare their own
   bound.
4. **Custody differs.** A review or seat private half lives with the reviewing
   holder's signing arrangement; an origin private half lives in the factory's
   hosted packaging environment. Mixing them in one register invites one
   custody attestation to be read as covering both.
5. **Blast radius differs.** Compromise of an origin key buys an attacker the
   ability to originate a bounded request that still faces platform provenance
   verification, the permitted-operation bound, and hosted output validation.
   Compromise of a review key buys verdicts. Keeping their registration,
   rotation, and revocation separate keeps their incident responses separate.

The sibling therefore mirrors the intake register's four-file shape —
`register.yaml` beside `wallets/`, `grants/`, and `attestations/` — under
`governance/factory-identity/`, reusing the same grant and wallet-record kinds
from the pinned neutral wallet vocabulary. What is NOT duplicated is the
question the rows answer.

### D2 — The sibling register inherits the "deliberately kindless" register discipline; the records beside it stay kinded **DECIDED**

The intake register carries `register_version` and its rows and no
`schema_version`/`kind`, on the recorded ground that no contract schema should
be minted for a shape with one instance — the READER is the shape. The sibling
is instance TWO. Two instances do not fire the rule of three, so this change
keeps the discipline rather than schema-ing the register shape prematurely; a
THIRD register of this shape is the trigger to promote a register schema, and
this design records that trigger so it is not rediscovered. The records beside
the register — wallet records, grants, and the manifest schema if OQ2 lands
here — carry `schema_version` and `kind` as every other contract record does,
because their kinds already exist in the pinned vocabulary.

### D3 — One origin identity per factory, superseded rather than multiplied **DECIDED**

One Ed25519 key per factory (the ruling). Rotation supersedes the row; two
concurrently active origin rows for one factory are refused. This keeps "which
key speaks for factory X" a question with exactly one answer at any instant,
which is what makes a clearing-time verification decidable without policy.

### D4 — Verification is CONJUNCTIVE, and the design says so in both directions **DECIDED**

Platform provenance and origin signature are both required. The specs carry a
scenario for each failure direction — valid signature over false provenance,
and true provenance with no valid signature — because "verify provenance and
the signature" is the kind of requirement that decays into an either/or in
implementation. Neither check subsumes the other: the platform API proves which
run produced the artifact, and the origin signature proves the factory intended
that manifest, including its bundle digest.

### D5 — Sign-on-return, and the reason it is not a compromise **DECIDED (ruling)**

The tempting alternative was to give the estate a signing key so results are
signed where they are produced. Refused. Sign-on-return costs one extra hosted
verification step and buys the property that attestation keys never leave the
factory — which also means the existing key placement needs no re-mint and no
relocation. The spec states the return is verified BEFORE anything is signed,
so the hosted signer cannot be turned into an oracle that attests whatever the
estate returns.

### D6 — Two capabilities, not one **DECIDED**

`clearing-boundary` and `factory-origin-identity` are separately consumable. An
estate can conform to the boundary's isolation, validation, and wipe
requirements before any origin key exists (falling back to hosted-workflow
provenance alone, which the manifest field set already permits as the
alternative attestation). A factory's origin identity is meaningful to any
verifier of its bundles, not only to a clearing boundary. Splitting them also
keeps the human-only register requirements out of the boundary's spec, where
they would read as unrelated.

### D7 — Neutral capability names, incident-named change directory **DECIDED**

The change directory keeps the name the ruling gave it, so the record is
findable from the incident. The capabilities do not: they are
`clearing-boundary` and `factory-origin-identity`, and the specs use
"originating factory", "execution estate", and "execution group" throughout.
Estate- and hardware-specific nouns appear only in `tasks.md` and the impact
map, as realization pointers.

### D8 — Revocation is inherited, not re-invented **DECIDED**

Origin identities revoke under the ratified wallet revocation lifecycle:
propagation through the derivation chain at the moment revocation is taken,
check-at-exercise rather than trust-at-admission, computed expiry rather than a
trusted state field, distinct diagnoses for revoked / expired / unrecognized,
no un-revoking, and reason classes recorded without narrowing propagation. The
one addition this design makes is naming the exercise point precisely: for an
origin identity, "exercise" is the moment a sealed bounded request is CLEARED,
not the moment it was packaged. A bundle packaged under a key revoked before
clearing must be refused.

The intake register recorded a design constraint that applies here unchanged: a
file-based register is an issuance-time snapshot and cannot itself be a
revocation surface, because every distribution path is pinned and lagging.
That is exactly why OQ1 below is open rather than answered by "read the file".

## Risks / Trade-offs

- **The manifest is long, and long field sets rot.** Mitigation: the field set
  is stated once as a requirement with a refusal scenario for any missing
  field, so a realization cannot quietly drop one; whether it is also schema'd
  is OQ2.
- **The clearing boundary is a single point of failure by design.** That is the
  intended trade — one place to audit and shut down is worth one place to keep
  available. The spec makes the failure mode fail-CLOSED (stale or unreadable
  projection refuses), which converts an availability incident into a stoppage
  rather than an unverified admission.
- **Sign-on-return adds a hop where a returned result waits to be attested.**
  Accepted; the alternative places attestation keys on shared hardware.
- **A projection introduces a window** in which a revoked origin key still
  verifies at the boundary. Bounded by the declared staleness bound, and the
  bound is a ceiling the estate may narrow but never widen. Closing the window
  entirely needs a live lookup — OQ1.
- **Act distinctness needs the OTHER register's reader to refuse too.** This
  change states the requirement in both directions, but the intake reader is
  pinned vocabulary owned elsewhere; see OQ3.

## Open Questions

### OQ1 — How does a projection of the factory-identity register reach the clearing workflow?

The register lives here; the clearing workflow lives in the estate's
repository and must resolve an origin key at admission time with a bounded
staleness. Four shapes, none chosen:

- **(a) A scheduled projection refresher.** A governed job publishes a
  projection of the register on a cadence; the clearing workflow reads the
  projection and refuses if it is older than the declared bound. Pro: no
  cross-repository read at admission time, staleness is explicit and
  measurable. Con: another moving part, and the refresher becomes a
  liveness dependency of all cross-boundary execution.
- **(b) A checked-in, digest-pinned projection in the estate repository.**
  Re-pinned by a governed sync, exactly as neutral contract consumption is
  pinned today. Pro: reuses machinery that already exists and is already
  gated; the projection is reviewable in a diff. Con: staleness is bounded by
  human cadence, so revocation propagates only as fast as someone re-pins —
  the weakest revocation story of the four.
- **(c) A live read of the register at clearing time.** The clearing workflow
  reads the register from this repository at admission. Pro: no projection,
  no staleness window. Con: a cross-repository read credential in the
  clearing path, and this repository becomes an availability dependency of the
  estate's admissions.
- **(d) A runtime lookup.** The conforming home the intake register already
  named for revocation-at-exercise — a live authority lookup served by the
  governed runtime, with the file remaining the issuance-time record. Pro:
  the only option that actually satisfies revocation-at-exercise, and it
  converges with the review side's own open successor. Con: the largest
  dependency, and it does not exist yet for this act.

The likely resolution couples (a)-or-(d) with the staleness bound already in
the register vocabulary, but the choice interacts with the review side's own
revocation successor and should be taken with it rather than ahead of it.

### OQ2 — Should the neutral job envelope CARRY the bundle manifest, or REFERENCE it?

`neutral-job-envelope` is the neutral core of the governed job, run, and event
schemas, with optional neutral references and a domain-overlay pattern. The
bundle manifest is a different animal — a dispatch-admission artifact whose
fields are about packaging, provenance, and a target's isolation, not about a
job's subject and scope. Two shapes:

- **Carry it.** Add the manifest as an optional neutral structure on the
  envelope, so a cleared dispatch IS a job envelope. Pro: one artifact
  crosses the boundary, and existing envelope tooling applies. Con: the
  envelope's loosening-only compatibility guarantee makes the manifest's
  own strictness awkward to state, and a required-field-complete manifest
  sits oddly inside a schema whose rule is that required fields must not
  encode one party's needs.
- **Reference it.** Keep the manifest a separate contract record and have the
  envelope carry an `artifact_refs`-style reference to it. Pro: each schema
  keeps its own strictness discipline; the manifest can require every
  enumerated field without touching the envelope's guarantee. Con: two
  artifacts to correlate, and the correlation becomes something to verify.

The second is the recommendation this design leans toward and does not take;
it also determines whether the manifest schema is part of this change's code
surface at all.

### OQ3 — Who teaches the review-authority reader to refuse an origin key?

Act distinctness is stated in both directions, but the intake register's
reader is part of pinned neutral wallet vocabulary owned outside this
repository. Refusing an origin-registered key presented for a review act is
therefore an edit somewhere else, at some pin. Whether that lands as a
vocabulary change in the pinned repository, as a consumer-side check beside
the reader invocation here, or as a validator rule that simply asserts the two
registers share no key, is not determined.
