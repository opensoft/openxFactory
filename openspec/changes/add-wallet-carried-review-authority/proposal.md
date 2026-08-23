---
code_surface: none — this change's own diff is spec text in openxFactory only: one new capability spec (`review-authority-intake`) plus a MODIFIED delta on `roles-authority-model`. NO `contracts/` artifact is added or changed: the delegation instrument is expressed in the already-shipped `contracts/openxwallet/openxwallet-grant.schema.yaml` vocabulary (see "One capability, and why no schema"), so there is no new schema, no `contracts/manifest.yaml` entry and no `contracts/CHANGELOG.md` line. The physical work this change authorizes but does NOT perform — standing up the intake register, wiring a validator to it, the runtime refusal in the Hermes install, and any scaffolding by which codexFactory offers the recommended three-repository project schema — is downstream realization named in ## Impact, each act its own successor change carrying its OWN code_surface and archiving on merged, green evidence per `release-realization`.
target_release: implemented (the doc-only pair; no contract bundle is cut)
---

# Proposal: add-wallet-carried-review-authority

Status: draft
Proposed: 2026-08-22, on direction from the convener, Brett Heap — the same day
`add-substantive-review-lane` was ratified and the `gate_rules_council`
returned its `codexfactory-routine-code-clearance` convening. This change acts
on a finding that convening produced.

Circulated first as `add-assembly-plane-separation`, whose spine was a
three-repository topology. Both alignment reviews are retained beside this
proposal (`alignment-stack-architect.md`, `alignment-qa-lead.md`); the convener
reshaped the spine after reading them, and the topology is retained below as a
RECOMMENDED PROJECT SCHEMA rather than deleted. Every finding either applies to
the reshaped text or is recorded in ## Findings superseded by the reshape.

**This is a proposal-only circulation.** Spec deltas and `tasks.md` follow the
bench's ruling on the narrowed floor reading and the open questions; there is
no `tasks.md` today and the front matter does not claim one.

## Why

The family now has a governed AI reviewer that genuinely works.
`add-substantive-review-lane` ratified it 2026-08-22 and settled where it
lives: codexFactory's councils review substantive pull requests in EVERY
governed repository, because "a pull request's diff is software regardless of
the domain"
(`openspec/changes/add-substantive-review-lane/specs/roles-authority-model/spec.md:152-157`),
and no domain instantiates review personas of its own — the scenario "No second
persona home is instantiated" makes that enforceable (`:176-182`).

That same delta drew the line the reviewer may never cross. Any candidate class
"touching contract bytes, gate or workflow definitions, credential surfaces, or
security posture" is "permanently human-only regardless of unanimity"
(`:336-337`, the constitutional floor at `:323-344`, its scenario at
`:352-357`). **The line is correct and this change does not move it.**

**The operator's own framing, which this proposal is obliged to carry
honestly.** Brett Heap is the sole developer. Author-cannot-self-approve
composes with sole-code-owner into a deadlock, and the deadlock has exactly one
routine exit: `--admin`. Today every governed merge takes it. A gate whose only
habitual discharge is its own bypass is a ritual, not a control — and a ritual
that runs daily teaches everyone, including the machinery, that the gate is
decorative. The ask is not to widen what the council may clear. It is to let
each reviewing body hold, provably and revocably, exactly the authority it was
issued — and to make the permanently-human remainder SMALL, EXPLICIT and
STRUCTURALLY ISOLATED.

**Today that remainder is defended by path rules inside one tree, and the
defence has been shown to be softer than it reads.** codexFactory currently
holds the boundary with four in-tree mechanisms, all in the repository the
candidate also ships in:

1. A never-clearable gate-integrity floor of **35 patterns**
   (`scripts/merge_master/codexfactory-routine-code-clearance.yaml:59-127`),
   headed by `"scripts/**"` — commented, in the file, as "the decision core's
   whole import root" (`:61`).
2. A CODEOWNERS entry `/scripts/ @brettheap`, added the same day
   (`.github/CODEOWNERS:29`), whose own note records why: "anything inside it
   can shadow the module that judges a candidate (proven by execution during
   the change council debate — a six-line `scripts/yaml.py` made the tier-1
   core emit `"approve": true` on forged facts)" (`:11-20`).
3. A run-time import-root coverage test,
   `test_every_import_root_of_the_core_is_covered_by_the_floor`
   (`tests/merge-master/test_generalized_core.py:504-522`), computing the roots
   at run time "so a NEW import root fails this test".
4. A widen-only validator that is supposed to make the floor un-narrowable.

Mechanism 4 does not hold for the widenings it was given. The lead-security
seat PROVED it by execution during the 2026-08-22 convening (finding LS-A3,
`hermes/domain/review-councils/records/2026-08-22-seat-returns/lead-security.md:154-160`):
the widen-only check is anchored on a probe set enumerating only the seven
canonical entries, so deleting `.github/**` and all six agent-instruction
widenings from the rule returned **ACCEPTED**. The seat's conclusion is the
sentence this proposal is built on: "A bench must not adopt a control on a
description of an enforcement that does not enforce it" (`:158`). The convening
ratified the rule AS AMENDED with that gap as an activation condition
(`records/2026-08-22-gate-rules-regular-pr-council-clearance.md`), and four of
five seats independently found other elements of the same rule unwired.

**That rule is not live yet, and the margin matters to how urgent this is.**
`codexfactory-routine-code-clearance` stands mid-activation with **thirteen of
fourteen** activation-gate entries outstanding: `activation_gate.requires` was
extended "from five entries to fourteen" by amendment R10, "the five entries
the rule shipped with stand unchanged; these nine are added," and ratification
"satisfies exactly one of the activation gate's entries"
(`records/2026-08-22-gate-rules-regular-pr-council-clearance.md:165`, `:226`,
`:106`). So the surface this change reasons about is a surface still being
wired — which is the cheapest moment to settle where its authority comes from,
and the last moment before the wiring encodes an answer by default.

Every one of those four mechanisms answers one question: *can the thing being
reviewed reach the thing doing the reviewing?* Inside a single tree the answer
is yes-unless-forbidden, and the forbidding has to be complete, correct, and
maintained forever against a tree that grows.

## The convener's ruling, 2026-08-22 — why the spine is authority, not topology

The first draft answered that question with a repository topology: split every
governed unit into SPEC / CODE / ASSEMBLY repositories and let the boundary do
the work. **The convener demoted that topology from the spine to a recommended
project schema, and the argument is decisive.** He did not discard it — he
holds that separating spec from code is good practice because it makes
ownership clear — but a recommendation a human elects per project is a
different object from a governance requirement, and only the second was on the
table.

**A repository topology imposes a shape on every repository codexFactory
reviews.** That fights the model ratified the same morning. The substantive
review lane is deliberately a SINGLE reviewing home whose councils judge every
governed repository whatever domain it governs
(`add-substantive-review-lane/specs/roles-authority-model/spec.md:152-157`,
scenario `:176-182`). A topology requirement inverts that: instead of the
reviewer travelling to the repository, every repository must be restructured
before the reviewer may arrive. The lane's whole value is that it does not care
what a repository is shaped like.

**Wallet-carried authority travels.** In the convener's words: *"codexFactory
can be run against any repo. We just need an intake where we set the
authorities and duties in the wallet for each ai and council."* A grant is
issued to a holder over named objects at a named tier; nothing about the target
repository has to change for it to apply. The reviewer arrives carrying what it
may do.

**The house already ratified this exact move, in these exact words.**
`openxwallet`'s second requirement is titled "**Authority travels as attenuated
grants, never as keys**" (`openspec/specs/openxwallet/spec.md:28-35`), and
`openxwallet-agent-profile` closes it for machines: "no authority exists for
that agent outside a grant" (`:59-63`), with a parallel authority vocabulary
declared a validation failure (`:65-69`). This change does not invent a
mechanism. It names review authority as one more thing that travels the way the
family already decided authority travels.

**The strongest counter-evidence against the topology is openxFactory
itself** — and under the new spine it becomes supporting evidence. The house
ratified spec-and-code CO-RESIDENCE in one repository
(`shared-contract-ownership:113-137`, openxFactory owning non-deployable
reference code under `xfactory/avatar_runtime/`), and `adopt-neutral-tooling-home`
(2026-08-03) moved tooling INTO the publisher on purpose — "Tooling hosted in
the publisher verifies released bytes, not a declared pin" (`:139-146`). The
family's most recent ruling on where code lives moved it TOWARD the artifacts it
reads. A three-plane rule would have had to overturn both. Wallet-carried
authority overturns neither: it is indifferent to where files sit, because it
binds the HOLDER, not the tree.

## What Changes

### 1. Authority travels in grants, not in repository shape

- **Every governed target's review authorities are expressed as openxwallet
  grants.** A grant names its `audience` (a `wallet_ref`, `holder_ref`
  optional — `contracts/openxwallet/openxwallet-grant.schema.yaml:53-57`), its
  `scope.acts` over optional `scope.objects` (`:59-79`), the REQUIRED
  `scope.authority_tier` (`required: [acts, authority_tier]` at `:61`, the
  field at `:79`) drawn from the closed four-rung ladder in
  `contracts/openxwallet/openxwallet-custody.registry.yaml:15-37`, `expires_at`
  (`:88`), `parent_grant_ref` — "Present iff this grant is derived. Attenuation
  is checked against the parent named here, and revocation propagates down this
  edge" (`:91-94`) — and a `revocation` block with reason and propagation
  (`:98-105`). Derivation is MONOTONICALLY NARROWING
  (`openxwallet/spec.md:43-47`).

- **The holder may be a human OR an agent, and the vocabulary already says so.**
  "the holder may be a person, practitioner, organisation, or agent — AND no
  requirement in this capability assumes a particular class"
  (`openxwallet/spec.md:22-26`). No holder-class rule has to be written; one
  has to be USED.

- **Spec authority and code authority become two grant SCOPES, not two
  repositories.** The same target's specs and its implementation are two named
  object sets under two grants. Where the bench requires them held apart, the
  separation is not a topology and not a convention: it is
  `distinct_holder_constraint_refs`
  (`openxwallet-grant.schema.yaml:106-111`), the schema field that realizes
  `openxwallet`'s ratified requirement "Distinct-holder constraints are
  expressible" (`openspec/specs/openxwallet/spec.md:133-153`). The grants NAME
  the constraint and the constraint is enforced at exercise; a grant naming none
  is subject to none (`:139-140`), so the naming is the act. This converts
  "spec owner and code owner are distinct" from an assertion into a validated
  refusal.

### 2. The ceiling is already structural — it is not a new rule

The first draft asserted "no delegated role discharges a terminal human gate."
It does not need to assert it. **The custody registry enforces it.**

- Custody caps authority (`openxwallet/spec.md:71-91`), and today's software
  custody models both ceiling at `act`: `holder_readable`
  (`openxwallet-custody.registry.yaml:52`) and `isolated_invocable` (`:72`).
  Only `isolated_per_use_authorized` reaches `act_unsupervised` (`:94`), and it
  requires "an authorization that context cannot itself supply — a hardware
  presence check, an external policy approval, a separate custodian" (`:87-92`).
  There is no key infrastructure in the stack today; the registry says so in
  terms (`:53-58`).
- The rung the ceiling lands on is `act`, defined as "Complete an effecting
  act, **with approval required before apply**. A distinct authority reviews,
  which is what makes environment-level evidence survivable at this tier"
  (`:26-31`).

**So "no delegated agent discharges a terminal gate" is a consequence of the
custody registry, not a rule this change adds.** Stated any other way it would
become the parallel authority vocabulary that
`openxwallet-agent-profile:65-69` declares a validation failure.

**The prerequisite must be stated with the bonus.** `audience` requires
`wallet_ref` (`openxwallet-grant.schema.yaml:53-57`), so a delegate must hold a
wallet with a declared custody model: **no wallet, no delegation.** That is a
real cost, and it is bounded — `openxwallet` deliberately keeps wallets
optional for domains (`openspec/specs/openxwallet/spec.md:155-163`), so this
change makes a wallet a prerequisite for HOLDING REVIEW AUTHORITY and for
nothing else.

**And one more property arrives free, from the agent profile.** An agent
holder declares its composition as a hash over a declared component set —
"model version, prompt contract, tool manifest, policy version, parameters, and
retrieval corpus" (`openxwallet-agent-profile/spec.md:6-25`) — and any change to
that composition revokes its outstanding grants at once, "with no tolerance
band and no grace period" (`:27-48`). A reviewer whose prompt contract or model
version silently moves is not the reviewer that was authorized, and its grants
die on the spot.

### 3. One boundary survives: the checker must not live in the checked tree

The topology is demoted; the property it existed to guarantee is not. **The
essential property is that ONE PULL REQUEST CANNOT CHANGE BOTH A THING AND ITS
CHECKER.**

**For convening admission the Hermes runtime already provides it.** The
governed council orchestration admits a convening —
`admit_layer_convening` /`admit_convening`,
`installs/hermes-install/src/hermes_install/domain/council_orchestration.py:451`
and the module contract at `:12-18`: "The named council must exist in the
layer's materialized `review_council` content (an unseeded stack cannot
convene), the subject pin must be present, a referenced mix must exist in
materialized `deliberation_mix` content." That runtime lives in a SEPARATE
repository (`opensoft/xFactory-Hermes-Install`) and a SEPARATE deployment
(live on AKS), and **a codexFactory pull request cannot reach it.** The checker
is already outside the checked tree, by deployment rather than by decree.

**Non-self-review therefore becomes a runtime refusal, not a path denylist:** a
council MAY NOT be convened over a candidate that touches the machinery that
council is assembled from. The refusal is issued where a candidate cannot edit
it.

**The honest dependency, stated rather than glossed.** The runtime enforces
against the layer's MATERIALIZED content, and that content originates in
codexFactory's `hermes/domain/` — the neutral content manifest maps the
`review_council` kind to `hermes/domain/review-councils`
(`contracts/hermes-domain-overlay/content-manifest.schema.yaml:37`;
`contracts/hermes-domain-overlay/examples/hermes-domain-content-manifest.example.yaml:9`),
and it reaches the runtime through a governed seeding act that resolves a digest
pin, fetches the pinned archive and verifies its sha256 fail-closed before
materializing
(`installs/hermes-install/src/hermes_install/lifecycle/seed_layer_content.py:1-14`).
**The refusal is therefore only as strong as the governance on that content.**
Today that governance is: `/hermes/ @brettheap` in codexFactory's CODEOWNERS
(`.github/CODEOWNERS:18`); the surface's own declared consequence that "a path
outside the tier-1 allowlist is never-clearable, which is the fail-closed
direction" and `hermes/**` is outside it; and the digest-pinned, fail-closed
seeding act above. That is three real controls and it is not the same claim as
"structurally unreachable." Saying so is the point — LS-A3 exists because a
control was adopted on a description of an enforcement that did not enforce it.

### 4. The intake — the genuinely new operational artifact

Everything above composes ratified primitives. **This does not, and it is the
piece with no prior art in the corpus.**

**A governed surface where each AI and each council is issued its authorities
and duties.** For every reviewing holder — each agent seat, each council as a
body — the intake records: what it may review (`scope.acts`), over which
objects (`scope.objects`), at which rung (`scope.authority_tier`), until when
(`expires_at`), under what revocation, derived from which parent
(`parent_grant_ref`), and issued by whom (`issued_by`). Duties sit beside
authorities: the seat a holder is required to fill, and the distinct-holder
constraints it is subject to.

**This is what makes the model operational.** Without it, "authority travels in
grants" is a doctrine with no register to read. With it, running codexFactory
against a new repository is an INTAKE act — issue the grants — rather than a
restructuring act.

Its questions are posed in ## Open questions, not decided here. The one
substantive shape this proposal does assert is negative, and it comes from the
liaison doctrine: **the intake MUST NOT issue one holder both the review act
and the approval act over the same object**, because that collapses
`execution_binding.actor_ref` into `approval.authority_ref` — the three parties
`client-infrastructure-liaison/spec.md:18-30` says are "never collapsed into
one" (structurally restated at `docs/client-infrastructure-liaison.md:79-82`).
`distinct_holder_constraint_refs` is exactly the field that expresses it.

## What this creates that does not exist

Established by investigation, and CORRECTED against both alignment reviews —
each earlier silence claim that did not survive verification is restated rather
than repeated.

- **Spec authority distinct from code authority AS A HELD, DELEGABLE ROLE** —
  absent. The adjacent prior art is REPOSITORY-grain, not role-grain:
  `openspec/changes/archive/2026-07-09-reconcile-domain-neutral-and-engineering-spec-ownership/`
  settled which REPOSITORY owns neutral specs versus engineering
  implementation, and did so with three MODIFIED deltas and no new capability
  (referenced at `docs/domain-to-neutral-promotion-process.md:302`). What is
  genuinely absent is a NAMED, HELD, DELEGABLE authority on either side. Any
  such role's canonical definition must live in openxFactory
  (`canonical-policy-migration:33-38`), which is why the role definitions land
  in the `roles-authority-model` delta and not in the new capability.

- **A register issuing authorities to reviewing agents and councils** — the
  intake. Nothing in `openspec/specs/`, `docs/` or `contracts/` carries one.
  `openxwallet` supplies the record type and says nothing about who keeps the
  register; `openxwallet-agent-profile` supplies the composition declaration and
  says nothing about issuance.

- **Ownership of a path or artifact BY A ROLE** — CODEOWNERS borrows the syntax
  but means "human gate" (codexFactory `.github/CODEOWNERS:5-9`), it has no
  upstream neutral source, and **no validator anywhere in openxFactory reads
  it** (zero hits across `scripts/`, `openspec/specs/`, `contracts/`; verified
  independently by both reviewers).

- **A general rule that a body may not review its own machinery** — the corpus
  has per-instance identity-equality refusals (author ≠ reviewer, the
  three-identity separation at codexFactory
  `.github/workflows/council-convening-lane.yml:47-53`, the distinct-holder
  constraints of `openspec/specs/openxwallet/spec.md:133-153`) but no general
  rule. **Correction to the first draft:** the rule-setter ≠ rule-applier
  RATIONALE is not absent — it is ratified requirement text awaiting promotion,
  "preserving the rule-setting/rule-applying separation" inside the ADDED
  requirement "Company-policy seat participation in per-PR councils"
  (`add-substantive-review-lane/specs/roles-authority-model/spec.md:231-234`).
  It appears in no PROMOTED spec today, and because this change declares its
  deltas relative to that change's outcome it must treat the rationale as
  promoted text and BUILD ON it rather than introduce it. What remains a
  silence after that change lands is the general rule, not its rationale.

- **Delegating a named authority to a named holder** — not merely absent but
  apparently contradicted twice. Both reconciliations are worked in the next
  section; neither is left as "the specs phase will handle it."

## Reconciling the two standing statements

The first draft said this change "must overturn" two standing statements. It
must not, and saying so was itself a defect: an unmarked contradiction of a
promoted spec is a reportable health finding under the Explicit delta rule
(`openspec/specs/document-lifecycle/spec.md:96-113`, scenario `:111-113`).
**Both reconcile by SCOPING, and neither needs a MODIFIED delta.**

**"Authority never transfers" (`openspec/specs/doc-health/spec.md:572-575`) —
reconciled by scope, not by attribution.** It is a `#### Scenario:` heading
under the requirement "Candidates become staged proposals under human approval"
(`:557`), and its body is scoped entirely to the neutrality-drift lane: "it
reports and stages only — content authority stays with the owning factory"
(`:575`). What that scenario bars is a REPORTING LANE acquiring EDITING
authority IMPLICITLY, BY DISCOVERY — finding a misplacement does not license
moving it. An explicit, audience-named, expiring, revocable grant is a
different act performed by a different party: conferral by the holder, recorded
before the fact, revocable at exercise. The scenario governs conferral by
discovery; the instrument is conferral by issuance.

The anti-stand-in fixture is a SEPARATE and also-necessary argument on the
attribution axis: a delegate acts AS ITSELF under its own grant, never as a
proxy laundering an act onto the audience — "precisely the false audit record
this family exists to refuse"
(`contracts/openxwallet/examples/negative/exercise-attributed-to-a-wallet-not-presenting-its-key.yaml:12-14`,
realizing `openxwallet/spec.md:93-111`). The first draft used the attribution
answer to settle the conferral question. They are two answers to two questions
and both are given.

**"Ownership confers no authority" — reconciled because the instrument
CONFORMS to it, not despite it.** This is promoted requirement text, not doc
prose: `openspec/specs/client-infrastructure-liaison/spec.md:18-30`,
Requirement "Coordination, execution, and validation separation," scenario
"Ownership does not confer authority" at `:28-30` — the liaison "gains no
tenant-administration authority from that ownership, and any privileged action
still requires the binding's approved execution owner **and grant**." That is
this change's own position. Under wallet-carried authority a holder's standing
comes ENTIRELY from its grant and NEVER from an ownership label. The liaison
doctrine and this instrument say the same thing.

**Which is why the roles are renamed.** The first draft called them "spec
owner" and "code owner" while the corpus reserves "ownership" for a relation
that explicitly confers no authority — a collision that would re-litigate
itself at every future reading. They are **spec authority** and **code
authority** throughout this proposal and in the `roles-authority-model` delta.
The standing is carried by the grant; the name now says so.

## `consent-instrument` is a named NON-precedent

The first draft recommended modelling the instrument on `consent-instrument`.
**That recommendation is DROPPED.** It is incompatible with the grant
realization, on three counts, and both reviewers reached the same conclusion
independently:

1. `consent-instrument` requires an amendment to be "a status transition
   carrying its delta on the existing instrument; a new instrument referencing
   a parent is **nonconformant**" (`:115-126`). openxwallet narrows ONLY by
   deriving a new grant carrying `parent_grant_ref`
   (`openxwallet-grant.schema.yaml:91-94`). Under the grant model, amending a
   delegation IS revoke-and-reissue-as-derived — the exact shape
   `consent-instrument` calls nonconformant.
2. The lifecycles are different closed enums:
   `draft → pending_signatures → executed → amended → terminated` plus
   `withdrawn` as a DISTINCT second terminal state that "MUST NOT be declared
   as an alias of `terminated`" (`consent-instrument:69-98`), against the
   grant's `state: [active, expired, revoked]`
   (`openxwallet-grant.schema.yaml:95-97`) under `additionalProperties: false`
   (`:42`).
3. Modelling on one while realizing as the other would produce precisely the
   "parallel authority vocabulary" that is a declared validation failure
   (`openxwallet-agent-profile/spec.md:65-69`).

`consent-instrument` is nonetheless kept as a NAMED NON-PRECEDENT, because
being explicit about what was considered and rejected is cheaper than
rediscovering it. Its subject is consent between party-ladder rungs of a client
engagement, with signed-original custody
("The Signed Original Never Enters A Product Repo", `:176-190`) and third-party
estate hosts; an internal review-authority grant has no consenting subject and
no party ladder.

**Its sole-operator passage is the near-miss worth naming.** "Authority Basis
Is First-Class" (`:100-113`) handles one person controlling multiple rungs of
an engagement — "the Meds Rx case" — by recording the authority basis per party
and treating a shared signer as "a recorded SHOULD deviation, not a silent
one." **That is a DISCLOSURE answer, not a STRUCTURAL one**, and the corpus's
only sole-operator pattern is therefore disclosure. This change proposes
structure instead — but the bench should know that where structure runs out,
the house's existing answer is to disclose, and the intake is the natural place
to record such a deviation.

## The recommended project schema, and the option the bench rules

Two separate things sit here and the convener separated them deliberately. The
first is NOT a bench question; the second is.

### The three-repository project schema — recommended, elected per project by a human

**The convener agrees with the stack architect that keeping spec and code in
separate repositories is GOOD PRACTICE, because it makes ownership legible at a
glance.** He also wants portability, which is why the wallet is the spine. His
ruling resolves the tension without a governance rule: *"For our own internal
projects, we can have codeXfactory recommend and run a 3 repo project schema.
But let the human project manager decide."*

**So the topology is a RECOMMENDED PROJECT SCHEMA, not an alternative spine and
not something this bench rules on.** codexFactory may recommend — and scaffold
— a three-repository shape for a project: SPEC (the governing specs and
contracts), CODE (the implementations), and ASSEMBLY (the code that assembles a
review team, shared across the family). The argument for it is ergonomic and
real: when spec and code sit in different repositories, who holds spec
authority and who holds code authority is visible from the repository list
instead of inferable from a register.

**Adoption is a PER-PROJECT DECISION BY A HUMAN, never a precondition of review
and never a governance requirement.** A one-repository project and a
three-repository project are reviewed IDENTICALLY, because the authority
travels in the grants rather than in the layout. That is precisely what makes
the choice safe to leave to a human: nothing about correctness rides on it.

**The recommendation confers nothing, and this must be stated so it is never
read as a soft requirement.** Electing the schema changes no gate, no floor, no
grant, and no clearance eligibility. A project that DECLINES it is not less
governed and is not reviewed more suspiciously; a project that ADOPTS it earns
no additional clearance. The wallet is what governs. The layout is ergonomics.

**Consequently this change declares NO repository-boundary obligation.** It
creates no repository, moves no runtime code, changes no submodule pointer and
advances no pin — so the obligations that attach to a repository act do not
attach to it. Where the earlier draft treated them as its own, they are
recorded in ## Findings superseded by the reshape as NOT APPLICABLE, with the
note that any project actually electing the schema takes them on at that
moment:

- a new repository is the NINETEENTH submodule of the aggregation repo (18
  today per `/home/brett/projects/xFactory/.gitmodules`; the README's 13-entry
  `## Current Submodules` list is stale);
- the boundary is declared BEFORE the repository exists — the house does this
  routinely, eight instances, zero new capabilities, `add-identity-brokering`
  adding "Keycloak install repository boundary" for a repo
  `implement-keycloak-install-repo` created afterwards;
- the template is "Neutral avatar-client repository boundary"
  (`repo-boundary-governance:113-137`) — what a non-install repository owns
  from creation, what it pins, what it MUST NOT contain — NOT "Install
  repository scope" (`:29-40`), which is name-scoped to the two install repos;
  and the aggregation act is bound by "Deferred aggregation and web-console
  integration" (`:165-181`) with its eight-element record (path, remote,
  visibility, exact validated commit, checkout, compatibility, update,
  rollback);
- moving existing machinery trips a declared STOP CONDITION on two counts —
  beyond copy-first (`:41-58`), `:59-76` makes "moving runtime code" and
  "changing submodule pointers" stop conditions requiring a return to Hermes
  approval under a narrower exception approved for that specific feature
  (`:62-64`);
- and it is a devolution act: "the owning Domain Hermes approves surrendering
  or receiving a concept, boundary governance approves the neutral side, and
  both gates are OpenSpec changes, never bare commits"
  (`docs/domain-to-neutral-promotion-process.md:299-306`).

**Two substantive cautions the bench should hear even though it is not ruling.**
First, if an ASSEMBLY repository ever holds the gate RULES rather than only the
engine, it collides with a canonical home: `codexfactory-routine-code-clearance.yaml`
is rules-as-code — merge authority POLICY — canonically openxFactory's under
`repo-boundary-governance:8-13` ("merge authority concepts"; scenario `:16-17`
naming "merge council behavior") and `canonical-policy-migration:44-48`. The
recommendation should scaffold ENGINE, and leave rules where policy lives.
Second, any consumer pin the schema introduces must be content-addressed:
`shared-contract-ownership:84-91` and `:101-103` already require "the exact
openxFactory commit and per-file digests" and rule that a tag alone is not a
content-addressed pin.

**One property the schema does buy, worth recording because it is not
ergonomics.** Today the aggregation caller "checks out `opensoft/codexFactory`
at a migration pin because the decision core is a FOREIGN repository there",
while the local lane deliberately does not pin because "the base-branch
checkout — not a pin — is what stops a candidate altering the rules that govern
it" (`council-convening-lane.yml:36-45`). Under a separated assembly plane the
core is foreign to every consumer, so a change to the review machinery is
judged under the PRIOR constitution. That is a real gain, and it costs a new
failure mode in every stale pin. It argues for the recommendation; it does not
make it a rule.

### The narrowed floor amendment — a reviewer CLASS, not a relaxation

The ratified floor forecloses an AI reviewer for gate machinery: candidate
classes "touching contract bytes, gate or workflow definitions, credential
surfaces, or security posture SHALL be permanently human-only regardless of
unanimity"
(`add-substantive-review-lane/specs/roles-authority-model/spec.md:336-337`),
with "no verdict under it SHALL ever produce an autonomous approval"
(`:352-357`).

**This proposal does NOT propose undoing it.** Under the floor as ratified, the
review machinery is human-only, full stop, and the intake issues no grant that
would clear it. That is the operative position of this document everywhere
else.

The convener observes that the floor was ratified BEFORE this issue was
understood, and asks the bench to rule on a NARROW reading:

**The floor's target is CORRELATED-SEAT UNANIMITY.** Its operative phrase is
"regardless of unanimity" — the harm it names is a bench agreeing with itself.
Three seats drawn from one assembly are not three pieces of evidence.

**Today's seeded-corpus run supports that reading, and its own caveat must
travel with it.** codexFactory's `2026-08-22-seeded-adversarial-corpus.md`
records: "**Verdict-level inter-seat disagreement: ZERO.** All 30 judgments…
No split vote occurred, so the runtime's unanimity composition was never
exercised against a divided bench" (`:327-330`); and on the one axis where the
seats visibly differ, "The seats converge on the verdict and diverge on what
must be fixed. That is worth knowing, but **it is not the independence Q3 asked
about**" (`:338-342`). The correlation-exploit candidate C4 failed to exploit
anything (`:352-357`). **The record's own warning is quoted here rather than
omitted:** "This corpus cannot distinguish 'diversity does not help' from
'these three defects were too easy for the question to arise', because no
defect was missed by anybody… Anyone citing this record for the proposition
that seat diversity is unnecessary is citing it wrongly" (`:359-364`). The
narrow claim survives that warning exactly: the run evidences that three-seat
unanimity on one bench has NOT been shown to be independent evidence — which is
the floor's concern — and evidences nothing about whether diversity helps.

**A DIGEST-DISJOINT reviewer is a class that did not exist when the clause was
drafted.** Enforceably: a reviewer is digest-disjoint from machinery *M* at
commit *c* iff **(i)** its declared agent-composition component set — model
version, prompt contract, tool manifest, policy version, parameters, retrieval
corpus, as a hash over a DECLARED set
(`openxwallet-agent-profile/spec.md:6-25`) — shares NO component whose content
digest appears in *M* at *c*; **and (ii)** it resolves its own machinery from a
pin naming a different source AND a disjoint digest set, content-addressed per
`shared-contract-ownership:84-91` and `:101-103`, where "the tag alone is not a
content-addressed pin."

**A FORK FAILS PRONG (i)**, and naming that is the whole point: a fork is a
different repository with an independent pin and 100% of the same packet
builder, seat prompts and gate machinery. So do vendoring and
copy-at-a-different-path. A different MODEL alone also fails: swapping weights
under the same prompt contract and tool manifest changes one component of the
declared set, not the set's intersection with *M*.

**What the bench is asked to rule.** Not whether to weaken the floor — whether
a digest-disjoint reviewer is a member of the class the floor excludes at all.
If the bench rules that it is not, that ruling requires its OWN explicit
MODIFIED delta amending the floor requirement, declared at that time and marked
as an amendment under the Explicit delta rule
(`document-lifecycle:96-113`). **This proposal does not pre-declare it**, and
nothing elsewhere in this document assumes it.

## Open questions — posed, not decided

**Q1 — Where does the intake register live?** The constraint is real and
narrows the answer: openxFactory owns "the canonical cross-factory role and
authority model… their canonical responsibility, authority, and escalation
boundaries MUST live in openxFactory" (`canonical-policy-migration:33-38`), and
merge-authority concepts are canonically openxFactory's
(`repo-boundary-governance:8-13`). But the per-repo `stack.yaml` is the
corpus's existing machine-readable declaration surface, and grants are
per-target. *Posed: canonical neutral register with per-target rows, or neutral
schema with per-repo instances? The answer decides Q3.*

**Q2 — Who issues, and what bounds the issuer?** Grants carry `issued_by`
(`openxwallet-grant.schema.yaml:90`) and derive under `parent_grant_ref`, so
the register is a chain with a root. The root is an authority no grant confers.
*Posed: is the root the operator's own standing, a Hermes-level role, or a
recorded act of the convening bench? Whichever it is, it is the thing whose
compromise compromises everything, and it should be named rather than
defaulted.*

**Q3 — What validator reads it?** Today NOTHING in openxFactory reads
CODEOWNERS (verified: zero hits across `scripts/`, `openspec/specs/`,
`contracts/`), and that is the cautionary precedent — an authority declaration
no tool reads is documentation. The specs phase must fix the register's
repository and path, and name the validator. *Posed rather than decided, but
this proposal records that an intake with no reader repeats the CODEOWNERS
mistake at higher stakes.*

**Q4 — How is revocation checked AT EXERCISE?** This is not optional and not
deferrable to taste: "A capability consuming grants SHALL check revocation at
exercise rather than trusting issuance" (`openxwallet/spec.md:113-119`), with
the scenario "revocation is checked at use" refusing an exercise after the
holder's standing was revoked and rejecting issuance-time validity as evidence
of current validity (`:127-131`). *Posed: what is the exercise checkpoint for a
review — convening admission, seat return, verdict consumption, or all three?*

**Q5 — What CONSTITUTES an exercise, and what carries its proof?** Every
exercise must carry proof of possession and produce a key-attributed record
(`openxwallet/spec.md:49-69`, `:93-111`). **A council seat casting a GitHub
review produces no wallet-signed exercise today.** *Posed with its two honest
exits: either the specs phase names a signing point in the convening flow, or
it scopes the delegation as a grant that is RECORDED while its exercise is
evidenced by the existing council/enforcement audit trail — and names that
explicitly as a declared deviation rather than letting it pass unnoticed.*

**Q6 — What is the refusal's subject?** The runtime refusal of §3 needs a
machine-checkable answer to "the machinery this council is assembled from." The
materialized `review_council` content and the digest-pinned archive it was
seeded from are the available handles
(`seed_layer_content.py:1-14`). *Posed: is the subject the seeded archive's
digest, the declared component set of each seat, or the union?*

**Q7 — Where is a project's schema election recorded, and which role makes
it?** The convener's ruling leaves the three-repository schema to "the human
project manager," which raises two questions the corpus can partly answer.

*Where.* The natural home is the project register at the aggregation root,
`/home/brett/projects/xFactory/project-register.yaml` (`kind: project-register`,
neutral schema at `contracts/schemas/project-register.schema.yaml`), which
already maps projects to their repositories, is HUMAN-EDITABLE, and is
`development-plane-authoritative` under Brett's D5 ruling on the
`dashboard-project-scoping` staged topic. Decisively, it already declares the
exact posture a schema election needs: "Grouping is descriptive navigation
only: **it confers no lifecycle state and no authority** over the repositories
it names" — a register that confers nothing is the right place to record a
choice that confers nothing. The alternatives are the project's own
`stack.yaml`, or nowhere machine-readable at all, which is defensible if the
election is purely advisory. *Posed, not decided.*

*Which role.* Checked against the neutral Owns/Decides table rather than
invented (`docs/roles-and-authority.md:67-74`), the convener's phrase maps to
`PM` Project Manager — which owns "sequencing, milestones, dependency
coordination, capacity, delivery process" and decides "when work happens, how
features are sequenced" (`:70`). But the DECISION CONTENT here is repository
layout, and the table already assigns that elsewhere: `PA` Project Architect
owns "project architecture, project integration shape, project architecture
decisions" and decides "**where project boundaries sit**" (`:72`), with `CA`
Chief Architect deciding "whether repo design violates the system model"
(`:71`). **This proposal flags the mismatch rather than resolving it by
paraphrase:** on the ratified table the election reads as a `PA` decision,
`CA`-constrained and `PM`-sequenced. Since both `PA` and `PM` are HUMAN
Hermes-level roles, the convener's substantive point — a human decides, not the
machinery — holds either way. *Posed for the bench to name the role precisely,
because "the human project manager" is a phrase and `PM` is a defined role, and
the two may not be the same thing here.*

## Capabilities

### New Capabilities

- **`review-authority-intake`** — the authority intake and the delegation
  instrument, together. It carries: the intake register (what each reviewing
  agent and each council is issued — acts, objects, tier, expiry, revocation,
  issuer, parent — and the duties beside them); the instrument's composition
  from openxwallet grants rather than a parallel record type; the obligation
  that revocation is checked AT EXERCISE, not at issuance; the wallet
  prerequisite and the custody-derived tier ceiling; the requirement that no
  holder is issued both the review act and the approval act over one object;
  and the declared agent-composition record that makes digest-disjointness
  computable whether or not the bench ever rules for it.

  **Why one capability, not two.** The first draft split topology from
  authority; the topology is no longer the spine, so that seam is gone. The
  remaining seam that MATTERS is instrument-versus-role, and it does not fall
  inside this capability — it falls between this capability and
  `roles-authority-model` (below). Register and instrument are not separably
  ratifiable: an instrument with no register is unexercisable and a register of
  nothing is empty. They have one subject, one realization, and one consumer.

### Modified Capabilities

- **`roles-authority-model`** — carries three things, all of which this
  capability already owns:
  1. **The role definitions: SPEC AUTHORITY and CODE AUTHORITY.** This
     capability owns "Hermes-level governance roles (project ownership,
     sequencing, system and project architecture, merge readiness and merge
     authority)" (`openspec/specs/roles-authority-model/spec.md:9-14`), and the
     realizing artifact is the `| ID | Role | Owns | Decides |` table at
     `docs/roles-and-authority.md:67-74`. Defining two new neutral governance
     roles anywhere else would collide with a promoted ownership requirement.
  2. **The non-self-review rule** — a body may not be convened over a candidate
     touching the machinery it is assembled from — as a general requirement,
     built on the ratified rule-setting/rule-applying rationale it generalizes
     (`add-substantive-review-lane/…:231-234`).
  3. **The single-reviewing-home requirement's authority counterpart**: the
     home is single, and what each holder within it may do is carried by grant.

  **The delta declares NO change to the constitutional floor.** The
  non-self-review rule can only REFUSE convenings; it never clears one. The
  narrowed reading carried under ## The recommended project schema is an option
  the bench rules on and, if ruled for, is amended by its own declared delta.

  **The delta is declared relative to `add-substantive-review-lane`'s
  OUTCOME.** `release-realization:64-70` requires BOTH limbs — "references that
  change AND declares its deltas relative to that change's outcome" — with
  scenario `:72-74` making it a MUST. This change therefore quotes the target
  requirement text as that delta will promote it and states its modification
  against that text. Archive ordering is a CONSEQUENCE, not the remedy; see
  ## Impact.

### The runtime refusal: downstream realization, not a delta

**Decided, with the reason.** The non-self-review refusal of §3 executes in the
Hermes runtime, which runs its OWN OpenSpec instance in a different repository
— `installs/hermes-install/openspec/specs/` holds `council-orchestration`,
`layer-content-seeding`, `governed-job-lifecycle` and four more. openxFactory
cannot author a delta into another repository's spec corpus.

The seam is not merely practical, it is ratified. `hermes-domain-overlay`'s
requirement "The subject overlay's enforceable slice is specified, and
materialization is not" (`:254-264`) sets the division precisely:
"**Extraction, transaction shape, provenance, digest verification, and refusal
vocabulary remain the consumer's; openxFactory owns document shape and canonical
validation.**" A convening refusal IS refusal vocabulary. It is therefore named
here as downstream realization — a successor change in
`opensoft/xFactory-Hermes-Install` against its `council-orchestration`
capability, carrying its own code surface and its own green-evidence archive
gate.

What openxFactory MAY owe is a `hermes-domain-overlay` delta if the refusal
needs a new declarable content kind or a new field on the content manifest
(`contracts/hermes-domain-overlay/content-manifest.schema.yaml:37` today maps
`review_council` to a location and nothing more). That is contingent on Q6 and
is not declared now.

### One capability, and why no schema

**No `contracts/` schema, and this is stronger than "premature".** Two grounds,
both corrected against the alignment reviews:

1. *Rule of three.* The instrument has exactly ONE named consumer today: this
   change. `ideation/staging/tier2-council-clearance-pattern` was proposed and
   demoted the same day, 2026-08-05, on the convener's own reasoning —
   "rule-of-three trigger not fired — no second consumer has named itself"
   (`ideation/staging/INDEX.md:68`). The precedent applies directly.
2. *A schema would be the very thing the corpus forbids.* The grant schema
   shipped at `contract-v1.31` and is sufficient as it stands. It carries
   `audience` (`:49-58`), `scope.acts`/`scope.objects` (`:59-79`), the REQUIRED
   `scope.authority_tier` (`:61`, `:79`) drawn from the closed four-rung ladder
   at `openxwallet-custody.registry.yaml:15-37`, `expires_at` (`:88`),
   `issued_by` (`:90`), `parent_grant_ref` (`:91-94`), `revocation` (`:98-105`)
   and `distinct_holder_constraint_refs` (`:106-111`). Every property this
   change needs is present, INCLUDING the ceiling: a reviewing holder's grant
   names `act` — "complete an effecting act, with approval required before
   apply" — and never `act_unsupervised`. Inventing a parallel vocabulary is
   barred: "a parallel authority vocabulary is a validation failure"
   (`openxwallet-agent-profile/spec.md:65-69`).

The instrument therefore lands as REQUIREMENT text in
`review-authority-intake`, composing openxwallet rather than duplicating it. If
a second consumer names itself, a schema — or a grant-scope vocabulary
extension — is a named successor.

**`openxwallet` is NOT declared as a modified capability, on a verified
finding.** `ideation/staging/INDEX.md:70` records delegation chains among the
`add-openxwallet` material deferred as "a named successor gated on a consumer
of its own", and this change is that consumer. But the CHAIN MECHANICS shipped
with the 2026-08-07 realization: `parent_grant_ref` plus revocation propagation
in the schema, "attenuation only narrows" at
`openspec/specs/openxwallet/spec.md:43-47`, and "revoking a parent kills the
chain" at `:121-125`. What was deferred was a consumer, not the primitive. The
successor therefore takes the form of a COMPOSING capability — the same
structural seam as `openxwallet-agent-profile` — and no core delta is declared.
If the specs phase finds a genuine core gap, an `openxwallet` MODIFIED delta is
added then, and this paragraph is the record of why it was not declared now.

## Impact

- **Sequencing against `add-substantive-review-lane`.** The requirements this
  change builds on are ADDED by that change, which is ratified but ACTIVE — its
  text is not yet promoted into `openspec/specs/roles-authority-model/spec.md`
  (11 requirements today, none of them the floor, the pilot requirement, or the
  company-policy seat). Per `release-realization:64-74` this change references
  that change AND declares its deltas relative to its OUTCOME — the operative
  mechanism, not a fallback. Archive ordering is the consequence:
  `add-substantive-review-lane` carries a three-repository code surface and
  stands at 3 of 19 tasks, so waiting on its archive is not a near-term option.
  The house already runs this pattern routinely —
  `implement-keycloak-install-repo` MODIFIES a requirement ADDED by the still
  active `add-identity-brokering`.
- **No `contracts/` artifact, no `contracts/manifest.yaml` entry, no
  `contracts/CHANGELOG.md` line, no bundle cut.**
- **`doc-health` is NOT declared as a modified capability, with the reason.**
  The "Authority never transfers" scenario (`:572-575`) is scoped to the
  neutrality-drift lane, so a recorded, issued, revocable grant sits OUTSIDE it
  rather than as an exception to it. This is reconciliation by scoping, which
  the Explicit delta rule (`document-lifecycle:96-113`) admits; it is recorded
  here so the reconciliation is not silent.
- **`client-infrastructure-liaison` is NOT declared as a modified capability,
  with the reason.** Its Requirement "Coordination, execution, and validation
  separation" (`:18-30`) already locates authority in "the binding's approved
  execution owner and grant" and never in ownership (`:28-30`), so a holder
  whose standing is entirely in its grant CONFORMS to that requirement. The
  intake additionally adopts its three-parties-never-collapsed rule as a
  positive obligation. Nothing there is scoped, narrowed or amended.
- **Downstream realization, named and NOT performed here** — each its own
  successor change with archive-on-evidence discipline per `release-realization`:
  the intake register's creation and its validator (Q1, Q3); the exercise and
  revocation-check wiring (Q4, Q5); the runtime non-self-review refusal in
  `opensoft/xFactory-Hermes-Install` against its own `council-orchestration`
  capability (Q6); and the scaffolding by which codexFactory OFFERS the
  three-repository project schema (Q7) — offering it is realization work,
  electing it is a human's per-project act, and neither is performed here.
  Nothing in this change retires codexFactory's `"scripts/**"` floor entry, its
  `/scripts/` CODEOWNERS line or its import-root coverage test; those defences
  stand.
- **Domain realizations are downstream, not done here.** codexFactory's
  CODEOWNERS, its council definitions and its gate rules are named as work, not
  written by this change. No domain repository is edited by this diff.
- **`repo-boundary-governance` and `shared-contract-ownership` deltas are NOT
  declared, and not merely deferred.** This change creates no repository, moves
  no runtime code, changes no submodule pointer and advances no pin, so neither
  capability is engaged by it. A PROJECT that later elects the recommended
  schema takes those obligations on in its own change; the obligations are
  enumerated under ## The recommended project schema so an electing project
  inherits the list rather than rediscovering it.
- **README bookkeeping.** This change MUST be listed in `README.md`'s
  `## OpenSpec Records` → `Active changes:` block (`:303-305`) in the same
  commit that first tracks the change folder.
- **No existing gate is weakened and no `--admin` bypass is removed by this
  proposal.** The constitutional floor stands exactly as ratified. The
  non-self-review rule is refusal-only.

## Findings superseded by the reshape

Recorded explicitly rather than dropped silently. Each was a correct finding
against the topology spine. None is disputed; what changed is the subject.
"NOT APPLICABLE" means the finding's obligation attaches to a repository act
this change no longer performs — it is carried forward to whichever project
elects the recommended schema, not waved away. "SUPERSEDED" means the mechanism
the finding was about is gone and something else now does that work.

- **Architect F1** (fifteenth → nineteenth submodule) — **NOT APPLICABLE to
  this change.** The correction is right and the corrected count is carried
  under the recommended schema for any project that elects it, but this change
  creates no repository, so it incurs no submodule act.
- **Architect F7** (the house declares a repository boundary before the repo
  exists; eight instances) — **NOT APPLICABLE to this change.** F7's force was
  that a repository-boundary delta must not be DEFERRED behind a contingency.
  This change does not defer one: it declares no repository boundary because it
  imposes none. The precedent is recorded under the recommended schema, where
  an electing project's own change is the place it binds.
- **Architect F3, F4, F5, F6 and QA 5.3, 5.4, 5.5** (canonical home of the gate
  rules; the moving-runtime-code and submodule-pointer stop conditions; the
  correct boundary template; the Domain-Hermes surrender gate; the
  content-addressed pin shape) — all applied, all relocated into the
  recommended-schema section as the obligation list an electing project
  inherits. Each is an obligation ON A REPOSITORY ACT, and this change performs
  none.
- **QA 5.2** (the repository predicate under-covers the path predicate) —
  SUPERSEDED at its root: the spine declares no repository predicate at all,
  and the `roles-authority-model` delta makes no change to the floor. The
  finding's underlying warning is nonetheless honoured — nothing in this
  document both claims and disclaims a floor change, and the one place a floor
  change is contemplated (the narrowed reading) says plainly that it would
  require its own declared amendment.
- **QA 4.2** (spec/code owner "distinct by construction" has no observable) —
  SUPERSEDED by the mechanism change. Distinctness is no longer "by
  construction"; it is `distinct_holder_constraint_refs` named on the grants and
  refused at exercise, which IS the observable the finding asked for.
- **QA 4.4** (the three-plane declaration has no carrier; the retirement
  trigger has no evidencing artifact) — SUPERSEDED for the spine, since there
  is no plane declaration and no retirement — the in-tree defences stand
  untouched. Both re-arm for a project that elects the recommended schema, and
  are named there as that project's work.

Findings applied to the reshaped text rather than superseded: F2 (turned into
supporting evidence), F8, F9, F10, F11, F12, F13, F14, F15, F16, F17, F18, F19,
F20, F21, and QA 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 4.1, 4.3,
5.1, 5.6, 5.7, 5.8, 6.1, 6.2.

## Out of scope, deliberately

- Ruling the narrowed floor reading, or any of Q1–Q7. They are posed for the
  bench and this proposal takes no decision on them; where it recommends, it
  says so and says why.
- Deciding whether any project adopts the three-repository schema. That is the
  human's per-project election by the convener's ruling, and a bench cannot
  make it on a project's behalf without turning a recommendation back into the
  requirement that was demoted.
- Amending the constitutional floor. The narrow reading is put to the bench; if
  the bench rules for it, the amendment is a separate declared delta.
- Procuring or building a digest-disjoint reviewer. This change offers the
  enforceable DEFINITION; conforming to it is separate work.
- Any change to the council-verdict transport, the merge-master token-minting
  flow, or the three-identity separation. All are reused unchanged.
- Extending, narrowing, or re-tiering what councils may autonomously clear.
- Retiring `--admin` usage on any repository. That is a per-repo policy decision
  downstream of both this change and the substantive review lane.
- Making wallets a prerequisite for anything other than holding review
  authority. `openxwallet/spec.md:155-163` keeps them optional for domains and
  this change does not disturb that.
