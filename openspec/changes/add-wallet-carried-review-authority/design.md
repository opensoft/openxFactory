# Design: add-wallet-carried-review-authority

Companion to `proposal.md`. The proposal argues the doctrine and names the
build; this document records the DECISIONS, the alternatives that were weighed
and rejected, the risks that survive, and the build plan's gates.

## Context

Three facts set the whole shape of this design.

**One.** codexFactory now has a governed AI reviewer that works, ratified
2026-08-22 by `add-substantive-review-lane` as a SINGLE reviewing home judging
substantive pull requests in every governed repository. Its constitutional floor
makes contract bytes, gate and workflow definitions, credential surfaces and
security posture permanently human-only regardless of unanimity.

**Two.** The sole developer's deadlock — author-cannot-self-approve composed with
sole-code-owner — discharges daily through `--admin`. The in-tree defences that
hold the human-only remainder were shown softer than they read: LS-A3 proved by
execution that the widen-only validator does not enforce the widenings it was
given, and its conclusion is this design's first principle — *a bench must not
adopt a control on a description of an enforcement that does not enforce it.*

**Three.** The 2026-08-22 proposal violated that principle three times, against
the Hermes runtime, the custody registry, and the composition hash. Three council
seats found it independently. This design's organizing constraint is therefore
**nothing is described as existing that does not exist**, and every control the
doctrine leans on is either verified live or named as S-work with its honest
current state.

Baseline verified for this design (2026-08-23): zero live wallet instances in the
family; `validate-openxwallet.py` present and in no workflow; `issued_by`
optional and read by zero validator rules; no exercise record of any kind; no
grant register; the Hermes content channel FIXED and landed but not yet
redeployed.

## Goals

- Ratify the doctrine — authority travels in openxwallet grants, held by named
  holders, revocable, expiring — in a shape that survives adversarial reading.
- Name every missing control as build work with a gate, so the capability's
  realization is checkable rather than assertable.
- Make the register unforgeable at its root and unreadable-by-nobody: an issuer
  anchor and a reader in CI.
- Give the exercise a home that is outside the checked tree AND permitted to
  enforce.
- Leave the constitutional floor whole.

## Non-goals

- Ending any `--admin` merge. This change is a precondition; the enrolled
  routine-code lane is the remedy, and governance-file merges stay human by the
  floor permanently.
- Building anything. S1–S5 are successors, each with its own code surface.
- Amending the floor in any direction, including the narrowed reading.
- Making wallets a prerequisite for anything except holding review authority.
- Deciding whether any project elects the three-repository schema.

## Decisions

### D1 — The spine is wallet-carried authority, not repository topology

**Decision.** Review authority is carried by openxwallet grants bound to holders,
not by a repository layout.

**Alternative rejected: the three-repository topology (the first circulation's
spine).** It imposes a shape on every repository codexFactory reviews, which
inverts the single-reviewing-home model ratified the same morning. It would also
have had to overturn `shared-contract-ownership:113-137` (spec/code co-residence)
and `adopt-neutral-tooling-home` (tooling moved INTO the publisher). Demoted by
the convener 2026-08-22 to a RECOMMENDED PROJECT SCHEMA a human elects per
project; the adversary independently confirmed the demotion was right.

**Alternative rejected: a new delegation record type modelled on
`consent-instrument`.** Three independent incompatibilities, the first decisive:
`consent-instrument` calls "a new instrument referencing a parent" nonconformant
(`:115-126`) while openxwallet narrows ONLY by deriving a grant carrying
`parent_grant_ref`; the lifecycles are different closed enums; and modelling on
one while realizing as the other produces the parallel authority vocabulary that
`openxwallet-agent-profile:65-69` declares a validation failure. Kept as a named
non-precedent.

### D2 — The tier ceiling is written as a rule, not inherited as a consequence

**Decision.** `review-authority-intake` states outright that a review-authority
grant SHALL NOT name `act_unsupervised` and that an unattested custody
declaration caps at `request`.

**Alternative rejected: derive the ceiling from the custody registry** (the
2026-08-22 position). The registry's ceiling resolves through a wallet's
`custody.model`, which is a self-declared string with a free-identifier
`declared_by` and no attestation; the registry's negative fixtures test the
registry's internal derivation consistency, not any deployed wallet. And
`isolated_per_use_authorized` DOES reach `act_unsupervised` on an authorizer
clause ("an external policy approval, a separate custodian") that does not
require a human. A stated ceiling with no mechanism is worse than an explicit
rule because it stops anyone looking.

**Why this is not a parallel vocabulary.** A scope restriction imposed by ONE
consuming capability on values that already exist in the shared ladder is not a
second vocabulary; `openxwallet-agent-profile:65-69` bars inventing authority
words, not narrowing which existing ones a consumer may use.

### D3 — The exercise is recorded at verdict conformance

**Decision.** The seat's wallet key is minted inside the deliberation job; the
Hermes runtime verifies the signature over the seat return at `check_verdict`;
the exercise record is written there.

**Alternative rejected: enforce at convening admission (exit A).** The runtime's
ratified `council-orchestration` capability makes a recorded verdict "advisory
evidence only" and forbids deriving any state transition from it. Enforcing at
admission needs a MODIFIED delta inverting that requirement — a far larger act
than downstream realization, and one that changes what the runtime IS.

**Alternative rejected: audit-trail-evidenced exercise (exit B).** REJECTED on
the adversary's ground: such an act records as `event_class:
unauthenticated_request` and `unattributed`, and `openxwallet` rules that such an
act is not assigned to a holder and that presentation alone confers no authority.
A grant whose every exercise is unattributed confers nothing checkable. Worse, it
recreates the anti-stand-in fixture's own failure one layer up: a reader of the
register plus a check-run cast by the shared merge-master installation credential
would attribute the act to the seat, which is the false audit record the family
exists to refuse. Declaring it a deviation does not stop it being the thing.

**Why the adopted exit needs no amendment.** The runtime's SECOND requirement
already refuses a completion fail-closed when the verdict block is malformed —
wrong pin, missing seat result, inconsistent unanimity. **A missing or
unverifiable seat signature is a conformance defect of the same kind.** The
runtime interprets nothing, derives no approval, and transitions nothing beyond
the job's own resolution, so advisory-only is untouched.

### D4 — The register and its reader are one change

**Decision.** A ratification condition of `review-authority-intake`: the register
and a validator that reads it land together, and a register alone does not
realize the capability.

**Alternative rejected: register first, reader as a successor.** That is the
CODEOWNERS failure at higher stakes — an authority declaration no tool reads,
which the corpus has already run once (zero validators anywhere in openxFactory
read CODEOWNERS). The cost of the guard is one requirement.

**MVP shape** (normative, from the product advocate's concern 3): one file at a
fixed path in openxFactory; one holder — codexFactory's `merge_readiness_council`
as a body; one target repository; one act; tier `act`; one `expires_at`; one
validator whose only job is to fail a convening that admits a holder with no
active row. Per-seat grants, multi-target rows, distinct-holder enforcement and
schema election are successors.

### D5 — The register is file-based first, and its revocation surface is not

**Decision.** The first register is a file in openxFactory (canonical home:
`canonical-policy-migration:33-38`, `repo-boundary-governance:8-13`). The
REVOCATION SURFACE's conforming home is a live lookup on the Hermes runtime, and
that is named as a successor rather than pretended into the file.

**Alternatives rejected as revocation surfaces.** Both file-based options — a
canonical neutral register with per-target rows, and a neutral schema with
per-repo instances — cannot satisfy `openxwallet:113-119` ("check revocation at
exercise", with its scenario rejecting issuance-time validity as evidence of
current validity). Every distribution path in this family is digest-pinned and
lagging: `stack.yaml` pins the openxFactory version; layer content is fetched by
digest pin and sha256-verified fail-closed. **A pinned register IS an
issuance-time snapshot** and a revocation takes effect only at the next re-pin
and re-seed, a human lifecycle act. Hermes already holds Postgres, layer identity
and the job lifecycle, which is why it is the conforming home.

**Why the file is nonetheless right for the MVP.** One holder, one target, one
row: the staleness bound is trivially satisfiable by hand, and the alternative is
building a service before a single grant exists.

### D6 — The register is a permanently human-only surface, declared explicitly

**Decision.** The register's path is entered BY NAME as a never-clearable floor
member, not left to inference.

**Ground.** openxFactory is the substantive review lane's PILOT repository. A
grant register is authority policy but is not literally "contract bytes, gate or
workflow definitions, credential surfaces, or security posture", so it plausibly
falls OUTSIDE the floor's four clauses — and then the councils holding grants
issued from the register would be eligible to clear changes to it. Councils
clearing their own commissions is the one outcome the whole change exists to
prevent.

### D7 — The non-self-review refusal's input is derived, never reported

**Decision.** The runtime computes the touched-object set from the subject pin
under its OWN credential; unavailable, self-reported or unverifiable ⇒ REFUSE.

**Alternative rejected: the commissioning lane posts the changed-path set.** The
poster is a workflow file in the checked tree that the candidate pull request can
edit in the same pull request. That is strictly weaker than the in-tree floor it
would improve on, and it is LS-A3 exactly.

**Cost, named rather than assumed away:** a per-target repository credential held
by Hermes, egress from the cluster, and a per-target machinery map.

**Scope, stated plainly:** the refusal's reachable subject is MATERIALIZED DOMAIN
CONTENT ONLY. `scripts/` — the decision core's import root, the surface LS-A3's
attack actually used — is not domain content and never will be, so **the runtime
refusal fully built would not have caught the one attack that has been
executed.** codexFactory's `"scripts/**"` floor entry, `/scripts/ @brettheap`
CODEOWNERS line and import-root coverage test remain the SOLE defence for the
decision core. The runtime refusal is additive.

### D8 — Role definitions live in `roles-authority-model`, mechanics in the new capability

**Decision.** SPEC AUTHORITY and CODE AUTHORITY are ADDED to
`roles-authority-model`; the instrument and register mechanics are the new
capability.

**Ground.** `roles-authority-model:9-14` already owns Hermes-level governance
role definition, and `canonical-policy-migration:33-38` requires any such role's
canonical definition to live in openxFactory. Defining them in the new capability
would collide with a promoted ownership requirement (QA 6.1).

**Naming decision.** Not "spec owner" / "code owner": the corpus reserves
ownership for a relation that explicitly confers no authority
(`client-infrastructure-liaison:28-30`), and the collision would re-litigate
itself at every reading.

### D9 — The `roles-authority-model` delta is declared relative to an active change's outcome

**Decision.** The MODIFIED requirement is `add-substantive-review-lane`'s
"Pilot repository and reviewing domain", restated in FULL as that change's delta
will promote it, with this change's modification declared against that text.

**Ground.** `release-realization:64-74` requires both limbs — reference the
change AND declare relative to its outcome — and its scenario makes it a MUST.
Archive ordering is a consequence, not the remedy: `add-substantive-review-lane`
carries a three-repository code surface at 3 of 19 tasks, so waiting on its
archive is not a near-term option. House precedent:
`implement-keycloak-install-repo` MODIFIES a requirement ADDED by the still-active
`add-identity-brokering`.

### D10 — The narrowed floor is declined, not repaired

**Decision.** Removed as a bench question entirely; not carried, not deferred,
and defining a real independence test is NOT named as a successor.

**Alternative rejected: repair the definition** (the adversary's conditional
three additions — attested completeness, a base-model disjointness prong, the
schema's caveat carried verbatim). Even repaired, the test measures byte
identity, which is anti-correlated with independence: it rejects different
weights and admits same-model-different-prompts. The primitive's own schema says
"whether that floor suffices is left to the consuming domain". The honest
position is that no independence test is currently definable, so the floor stands
whole and assembly-class surfaces stay permanently human-only.

**Consequence, accepted:** the product advocate's proposed coupling — election of
the three-repository schema earning prong (ii) of digest-disjointness — is
declined with it. The schema keeps its ergonomic argument and earns nothing in
governance terms, which is what makes it safe to leave to a human.

### D11 — Two scope restrictions, no schema change

**Decision.** `issued_by` becomes REQUIRED **for review-authority grants** and
`act_unsupervised` is REFUSED for them. Both are restrictions imposed by the
consuming capability on fields that already exist.

**Ground.** No `contracts/` edit, no manifest entry, no CHANGELOG line, no bundle
cut, and no other openxwallet consumer is disturbed. The rule-of-three has not
fired for a register schema (one named consumer:
`ideation/staging/INDEX.md:68` precedent), so the register's shape is a declared
successor rather than a contract authored now — but the 2026-08-22 conclusion is
softened from "no schema" to "no new GRANT schema", because a register with a
reader IS a shape and the derived candidate-side input may need a
`neutral-job-envelope` field.

## Risks

### R1 — The `--admin` composition loop (HIGH)

`openxwallet-agent-profile:27-48` revokes on ANY declared-component change with
no tolerance band and no grace period; model version is a declared component; all
holders are hosted models. A provider silently rolling a model alias revokes
every seat grant at once. Under `missing_required_seat: refused` every in-flight
and future convening parks, and **the only routine exit from a parked candidate
under a sole code owner is `--admin`** — the change's own strictest inherited
control manufacturing the ritual the change exists to break.

*Mitigation:* S5 pins model version and prompt corpus as declared components,
forbids the candidate repository at HEAD as retrieval corpus, and makes a
provider roll a governed re-issuance event with a named runbook. *Residual:* the
policy questions are Q8 and are not decided; a roll before Q8 is answered is
handled by the runbook and the operator's root authority, manually.

### R2 — The day-one empty world (HIGH)

Zero wallets, zero exercise records, no key infrastructure, ~8 holders needing
wallets, and a validator in no workflow. Any statement of the doctrine in the
present tense is false on day one.

*Mitigation:* ## Cold start states the order — S1, then S2, then the first
wallet, then S4's MVP — and the no-reader rule makes "no grant is operative"
requirement text rather than a caveat. The root issuer needs no wallet, which
removes the circular dependency that would otherwise block step one.
*Residual:* the operator's rational shortcut under key-management pressure is to
omit model version from the declared component set, which converts the register
into the CODEOWNERS failure with extra steps. S5's pinning requirement exists to
make that omission a validation failure rather than a convenience.

### R3 — The vacuous-pass class (HIGH)

Every control in this design has a shape where it passes while checking nothing:
a validator that runs in no required check; a custody model self-declared and
validated for spelling; a composition hash over a set the declarer chooses, with
digests never verified for correctness and completeness unverifiable; a
distinct-holder constraint whose comparison basis is an exercise store that does
not exist; a register whose staleness nobody bounds. **Each of these is a
described control that would be treated as an existing one.**

*Mitigation:* each is named with its gate — S1's required check, S2's issuer
refusal, the attestation cap, S3's exercise record, S5's staleness bound — and
the capability carries an explicit requirement that any statement of what the
intake enforces MUST name the check that enforces it, with an unenforced
requirement recorded as UNMET rather than partially met.

### R4 — The refusal that cannot see the attack (MEDIUM-HIGH)

The runtime refusal's reachable subject is materialized domain content only; the
executed attack used `scripts/`, which is not domain content.

*Mitigation:* stated in the proposal, in the design, and in requirement text —
the refusal is ADDITIVE and the in-tree defences are the sole defence for the
decision core. *Residual:* the floor's own source-of-truth record is an unseedable
markdown file gated only by CODEOWNERS, which `--admin` bypasses (Q9).

### R5 — The register lands and stops being maintained (MEDIUM)

The register is a floor-covered artifact the operator maintains by human merge,
exactly like CODEOWNERS, which drifted.

*Mitigation:* D4's register-and-reader-together condition means a stale register
FAILS a convening rather than silently permitting one; the failure mode is
loud. *Residual:* loud failure under a sole operator is itself an `--admin`
pressure (R1's shape), which is why the staleness bound is declared rather than
implicit.

### R6 — Sequencing against an active ratified change (LOW-MEDIUM)

The MODIFIED requirement is not promoted text; if `add-substantive-review-lane`'s
outcome text changes before it archives, this delta's restatement goes stale.

*Mitigation:* D9's relative-to-outcome declaration is the ratified mechanism for
exactly this, and the delta file names the source. *Residual:* a task to re-check
the restated text against that change's final promoted text before archive.

## Build plan — S1 through S5, with gates

Dependency-ordered. Each is a SEPARATE successor change with its own
`code_surface`, archiving on merged, green realization evidence per
`release-realization`.

| # | Work | Repository | Gate |
|---|---|---|---|
| S1 | Wire `validate-openxwallet` (or the register's validator) into CI as a REQUIRED check | openxFactory | The check is required on the register's repository; a deliberately malformed grant fails the PR |
| S2 | Issuer anchor: `issued_by` required for review-authority grants; root-grant class; operator named as root issuer | openxFactory | Validator refuses a review-authority grant with no `issued_by`, and refuses a root grant whose issuer is not the recorded operator anchor |
| — | The first wallet: one holder, `holder_readable`, with its custody attestation row | openxFactory | The wallet record validates and its attestation row is present |
| S4 | The register + its reader, MVP shape, in ONE change; register path declared a never-clearable floor member | openxFactory (+ codexFactory gate-rule entry) | A convening admitting a holder with no active row fails the required check |
| S3 | Exercise at verdict conformance: seat key minted in the deliberation job; signature verified at `check_verdict`; exercise recorded | hermes-install (`council-orchestration`) | A seat return with no verifiable signature is refused fail-closed; a conforming one writes an exercise record |
| S5 | Revocation re-check at verdict consumption; staleness bound; unreadable ⇒ refuse; composition pinning + re-issuance runbook | hermes-install + openxFactory | A revoked holder parks a convening with a named refusal in a rehearsed test; an unreadable register refuses; the runbook is walked once against a deliberate composition bump |

**Ordering constraints that are not negotiable.** S1 precedes everything (until a
reader exists, issuing a grant issues nothing). S2 precedes the first wallet (an
unanchored root grant is an unbounded one). S4 cannot precede S1 by its own
ratification condition. S3 precedes the useful part of S5 — a revocation re-check
at exercise needs an exercise — and S3 also precedes any claim that
`distinct_holder_constraint_refs` is an observable, since its comparison basis is
the prior act's RECORDED holder.

**One cross-repository deploy constraint travels with all of this.** codexFactory
`dcfbd96` and hermes-install `3de0519` are landed on `origin/main`, but per
codexFactory `3143f34`
(`records/2026-08-23-reseed-deploy-ordering-addendum.md`): **no reseed until a
hermes-install image at `3de0519`+ is deployed.** Any S-work that depends on
materialized `review_council` content in the live stack is gated on that image
shipping.

## Open questions

Reduced to three; the proposal's table maps Q1–Q7 to where each was answered.

- **Q8 — composition drift for hosted-model holders.** Standing reissue policy as
  a first-class intake act; whether derived grants survive a parent revoked for
  drift rather than cause; who tells the operator the register emptied; whether a
  hosted holder may pin a model FAMILY (today a validation failure). Posed with
  exits in the proposal; the second and third exits would need
  `openxwallet-agent-profile` / `openxwallet` core deltas and are named expensive
  for that reason.
- **Q9 — the floor's source-of-truth inversion.** The record governs, and the
  record is an unseedable, unschema'd markdown file in the reviewed tree. Two
  exits, both amendments to another change's ratified text; neither taken here.
- **Q10 — does a non-human authorizer satisfy `isolated_per_use_authorized`?**
  Does not block this change, because D2's refusal excludes those holders from
  review-authority grants until it is ruled — but it is the design's largest
  unexamined assumption and is named rather than left inside a quoted clause.
