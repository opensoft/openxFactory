---
code_surface: none — this change's own diff is spec text in openxFactory only: one new capability spec (`review-authority-intake`, 12 ADDED requirements) plus a `roles-authority-model` delta (2 ADDED, 1 MODIFIED). NO `contracts/` artifact is added or changed: the delegation instrument is expressed in the already-shipped `contracts/openxwallet/openxwallet-grant.schema.yaml` vocabulary (see "One capability, and why no grant schema"), so there is no new schema, no `contracts/manifest.yaml` entry and no `contracts/CHANGELOG.md` line. The physical work this change authorizes but does NOT perform is named in ## The build, in order as S1–S5, each act its own successor change carrying its OWN code_surface and archiving on merged, green evidence per `release-realization`.
target_release: implemented (the doc-only pair; no contract bundle is cut)
---

# Proposal: add-wallet-carried-review-authority

Status: ratified
Ratified: 2026-08-23 by Brett Heap (openxFactory operator authority) — in-session
ruling (the same mechanism that ratified add-substantive-review-lane on
2026-08-22). Realization proceeds per tasks.md, S1 first.

## Ratification record, 2026-08-23

Three rulings, recorded verbatim from the convener's in-session answers:

1. **Ratified as restructured** — PART I (the doctrine), PART II (the
   substrate, S1–S5, nothing pretended), PART III (the narrowed floor
   DECLINED; assembly-class surfaces stay permanently human-only; no
   independence-test successor named). Q9 and Q10 stay open as carried
   items — they amend or interpret `add-substantive-review-lane`'s text
   and are not this change's to settle.
2. **All four lead constructions confirmed** (each remains overturnable
   by a later ruling): register ≠ revocation surface; the intake register
   itself floored permanently human-only; the no-schema conclusion as
   no-new-GRANT-schema with the register shape and job-envelope field as
   declared successors; the project-schema section kept and trimmed rather
   than coupled to the declined floor or cut to staging.
3. **Q8 deferred to S5's design**: the composition-drift reissuance policy
   (standing reissue as a first-class intake act, drift-vs-cause survival,
   operator notification) is proposed by S5's implementer, with the
   model-family-pin question surfaced for the convener's ruling at that
   point, informed by real wallet mechanics.
Proposed: 2026-08-22, on direction from the convener, Brett Heap — the same day
`add-substantive-review-lane` was ratified and the `gate_rules_council`
returned its `codexfactory-routine-code-clearance` convening. This change acts
on a finding that convening produced.

**Restructured 2026-08-23** on the convener's ruling after council review. Five
review files are retained beside this proposal and are the complete review
record: `alignment-stack-architect.md`, `alignment-qa-lead.md` (both against the
first circulation, `add-assembly-plane-separation`), and
`council-product-advocate.md`, `council-systems-architect.md`,
`council-adversary-engineer.md` (against the 2026-08-22 proposal text). Every
finding's disposition is recorded in ## The council's disposition ledger; none
is dropped silently.

## The council's shared diagnosis, accepted in full

Three seats reached the same conclusion by three routes, and the convener
accepts it without qualification:

> **the proposal repeatedly treats a described control as an existing one.** It
> knows this failure mode by name — it is built on LS-A3 — and it applies the
> lesson rigorously to codexFactory's widen-only validator while granting the
> Hermes runtime, the custody registry, and the composition hash the benefit of
> the doubt it denies the mechanism it is replacing.
> — Adversary Engineer

The systems architect found the same shape from the enforcement side: "after the
reshape, *every* enforcement point it needs is either inside the checked tree or
forbidden from enforcing." The product advocate found it from the delivery side:
"a doctrine, a register with seven undecided properties, an advisory layout
nobody will elect, and a prerequisite (wallets) that does not exist anywhere in
the family."

**This is the proposal's own founding error, committed against itself.** LS-A3
exists because a bench adopted a control on a description of an enforcement that
did not enforce it. The 2026-08-22 text did that three more times, at higher
altitude, and this restructure is the correction.

## The convener's ruling, 2026-08-23

Brett Heap, openxFactory operator authority, ruled three things after reading
all five reviews. This document is organized around them.

1. **The doctrine is ratified-shape NOW.** What survived attack is kept and
   sharpened: authority travels in openxwallet grants; spec authority and code
   authority as distinct held roles; the general non-self-review rule; the
   doctrinal reconciliations by scoping; `consent-instrument` as a named
   non-precedent; the recommended project schema as a human election that
   confers nothing. That is PART I.
2. **The substrate is a named build with nothing pretended.** Every control the
   doctrine leans on that does not exist today is named as successor work S1–S5
   with its honest current state, and the doctrine states plainly what it does
   not yet have. That is PART II.
3. **The narrowed floor is DECLINED.** It is removed as a bench question
   entirely; the declination and its grounds are recorded. That is PART III.

Where the ruling ANSWERS a question the 2026-08-22 text posed, this document
answers it and stops posing it. Q1–Q7 are all disposed of; the surviving open
set is three questions, and one of them is new.

---

## PART I — THE DOCTRINE

Ratified-shape now. Nothing in this part depends on a control that does not
exist; where it names one, it names it as S-work and says so.

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
habitual discharge is its own bypass is a ritual, not a control. The ask is not
to widen what the council may clear. It is to let each reviewing body hold,
provably and revocably, exactly the authority it was issued — and to make the
permanently-human remainder SMALL, EXPLICIT and STRUCTURALLY ISOLATED.

### The first bypass this ends: NONE, directly

The product advocate's first concern is upheld, and the answer is stated here
rather than recovered from ## Out of scope. **This change ends no `--admin`
merge on the day it ratifies.** It is a PRECONDITION, not a remedy.

- The bypasses that end FIRST are the enrolled routine-code lane's, already in
  flight in codexFactory as `codexfactory-routine-code-clearance` — ratified as
  amended and standing at **thirteen of fourteen** activation-gate entries
  outstanding (`activation_gate.requires` was extended "from five entries to
  fourteen" by amendment R10; ratification "satisfies exactly one of the
  activation gate's entries" —
  `hermes/domain/review-councils/records/2026-08-22-gate-rules-regular-pr-council-clearance.md:165`,
  `:226`, `:106`). That lane is the remedy; this change is one of the things
  that makes its authority checkable.
- **Governance-file merges remain human by the floor, permanently.** Contract
  bytes, gate and workflow definitions, credential surfaces and security
  posture are human-only regardless of unanimity, and the intake register this
  change proposes is DECLARED into that set (PART II, S4). So the operator's
  daily governance merges are unchanged by design, and will remain so.
- The register itself will therefore be maintained by human merge. That is the
  intended posture, not an oversight: an authority ledger that a council could
  clear would let councils clear their own commissions.

Every sentence claiming more than this has been deleted from the document. The
Why sells a precondition, and that is what it is.

**Today the permanently-human remainder is defended by path rules inside one
tree, and the defence has been shown to be softer than it reads.** codexFactory
currently holds the boundary with four in-tree mechanisms, all in the repository
the candidate also ships in:

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
description of an enforcement that does not enforce it" (`:158`).

Every one of those four mechanisms answers one question: *can the thing being
reviewed reach the thing doing the reviewing?* Inside a single tree the answer
is yes-unless-forbidden, and the forbidding has to be complete, correct, and
maintained forever against a tree that grows.

## Why the spine is authority, not topology

The first circulation answered that question with a repository topology: split
every governed unit into SPEC / CODE / ASSEMBLY repositories and let the
boundary do the work. **The convener demoted that topology from the spine to a
recommended project schema (2026-08-22), and the argument is decisive.** He did
not discard it — he holds that separating spec from code is good practice
because it makes ownership clear — but a recommendation a human elects per
project is a different object from a governance requirement.

**A repository topology imposes a shape on every repository codexFactory
reviews.** That fights the model ratified the same morning. The substantive
review lane is deliberately a SINGLE reviewing home whose councils judge every
governed repository whatever domain it governs
(`add-substantive-review-lane/specs/roles-authority-model/spec.md:152-157`,
scenario `:176-182`). A topology requirement inverts that: instead of the
reviewer travelling to the repository, every repository must be restructured
before the reviewer may arrive.

**Wallet-carried authority travels.** In the convener's words: *"codexFactory
can be run against any repo. We just need an intake where we set the
authorities and duties in the wallet for each ai and council."* A grant is
issued to a holder over named objects at a named tier; nothing about the target
repository has to change for it to apply.

**The house already ratified this exact move, in these exact words.**
`openxwallet`'s second requirement is titled "**Authority travels as attenuated
grants, never as keys**" (`openspec/specs/openxwallet/spec.md:28-35`), and
`openxwallet-agent-profile` closes it for machines: "no authority exists for
that agent outside a grant" (`:59-63`), with a parallel authority vocabulary
declared a validation failure (`:65-69`). This change does not invent a
mechanism. It names review authority as one more thing that travels the way the
family already decided authority travels.

**The strongest counter-evidence against the topology is openxFactory
itself** — and under this spine it becomes supporting evidence. The house
ratified spec-and-code CO-RESIDENCE in one repository
(`shared-contract-ownership:113-137`), and `adopt-neutral-tooling-home`
(2026-08-03) moved tooling INTO the publisher on purpose — "Tooling hosted in
the publisher verifies released bytes, not a declared pin" (`:139-146`). A
three-plane rule would have had to overturn both. Wallet-carried authority
overturns neither: it is indifferent to where files sit, because it binds the
HOLDER, not the tree.

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
  object sets under two grants. Where they must be held apart, the separation is
  `distinct_holder_constraint_refs`
  (`openxwallet-grant.schema.yaml:106-111`), the schema field realizing
  `openxwallet`'s ratified "Distinct-holder constraints are expressible"
  (`openspec/specs/openxwallet/spec.md:133-153`). A grant naming no constraint
  is subject to none (`:139-140`), so the naming is the act.

  **What that observable costs, stated rather than glossed** (systems architect,
  concern 3). `contracts/openxwallet/openxwallet-distinct-holder-constraint.schema.yaml`
  fixes the comparison basis as the PRIOR ACT'S RECORDED HOLDER — what the
  exercise record for that act actually carries. Enforcing it therefore needs a
  queryable exercise-record store keyed by (object, act), and **none exists.**
  So `distinct_holder_constraint_refs` supersedes QA 4.2's "no observable"
  finding only once S3 lands the exercise record; until then it is a declared
  constraint with no store to check it against, and this document says so.

- **The prerequisite, with the bonus.** `audience` requires `wallet_ref`
  (`openxwallet-grant.schema.yaml:53-57`), so a delegate must hold a wallet with
  a declared custody model: **no wallet, no delegation.** That is a real cost,
  and it is bounded — `openxwallet` deliberately keeps wallets optional for
  domains (`openspec/specs/openxwallet/spec.md:155-163`), so this change makes a
  wallet a prerequisite for HOLDING REVIEW AUTHORITY and for nothing else. What
  the cost actually is on day one is costed in ## Cold start, not asserted to be
  small.

### 2. The tier ceiling is a RULE this change writes, not a consequence it inherits

The 2026-08-22 text said "the ceiling is already structural — it is not a new
rule," deriving it from the custody registry. **That was the second instance of
the founding error, and the adversary's third finding is upheld in full.**

- The whole of the ceiling's enforcement is `check_grant` rule (e) in
  `scripts/validate-openxwallet.py`: resolve `grant.audience.wallet_ref` →
  `wallet.custody.model` → `registry[model].authority_ceiling`, compare ranks.
  The wallet's custody model is **declared by whoever writes the wallet record**;
  `declared_by` is a free identifier with no attestation, and
  `check_wallet_record` validates only that the model id is a member of the
  closed set. **Nothing anywhere attests that a wallet declaring isolated
  custody actually has an isolated key.** "Raising authority requires changing
  custody, not asserting trust" is realized today as: raising authority requires
  editing one string.
- The registry's negative fixtures (`custody-registry-unearned-ceiling.yaml`,
  `custody-registry-readable-claims-holder.yaml`,
  `custody-registry-collapsed-ceilings.yaml`) test the registry's INTERNAL
  DERIVATION CONSISTENCY — that `evidences` follows from the two booleans. They
  cannot test a wallet's declaration against reality. Registry consistency is
  not deployment attestation.
- The ceiling is checked at static file-scan time and nowhere else: `repo_scan`
  builds its context from the scanned repo's own records, a corpus closed over
  itself. **The ceiling binds a file, not an act** — and, per S1, it binds it
  only when a human types the command.

**The sentence "today's software custody models both ceiling at `act`" is
DELETED.** It was a claim about today's CHOICES dressed as a claim about
software. `isolated_per_use_authorized` reaches `act_unsupervised`
(`openxwallet-custody.registry.yaml:81-94`), and its stated bar is "an
authorization that context cannot itself supply — a hardware presence check, **an
external policy approval, a separate custodian**." Neither of the last two is
hardware and neither is required by the text to be human. A remote signing
service requiring an approval call from a second process satisfies the literal
words, and the validator would hand that holder `act_unsupervised`. **Whether a
non-human authorizer satisfies that clause is UNRESOLVED** — it is carried as
Q10 — and until it is ruled, holders declaring `isolated_per_use_authorized` are
excluded from review-authority grants by the rule below.

**So this change WRITES the rule instead of inheriting it**, scoped so it is not
a parallel vocabulary — a scope restriction on one consuming capability, which
`openxwallet-agent-profile:65-69` does not bar:

> **A grant conferring review authority SHALL NOT name
> `authority_tier: act_unsupervised`, and the intake SHALL refuse to issue
> one.**

And, because a self-declared string is not an attestation:

> **A custody model with no recorded attestation — who verified the isolation,
> against what, when — caps a review-authority grant at `request`, not `act`.**

Both are ADDED requirements of `review-authority-intake`. Writing them as rules
rather than as consequences is deliberate: a stated ceiling with no mechanism is
worse than an explicit rule, because it stops anyone looking.

### 3. One boundary survives: the checker must not live in the checked tree

The topology is demoted; the property it existed to guarantee is not. **The
essential property is that ONE PULL REQUEST CANNOT CHANGE BOTH A THING AND ITS
CHECKER.**

**The Hermes runtime provides the PLACE for that refusal.** The governed council
orchestration admits a convening — `admit_layer_convening` / `admit_convening`,
`installs/hermes-install/src/hermes_install/domain/council_orchestration.py:451`
and `:256` — and that runtime lives in a SEPARATE repository
(`opensoft/xFactory-Hermes-Install`) and a SEPARATE deployment (live on AKS),
which a codexFactory pull request cannot reach.

**What the 2026-08-22 text got wrong, upheld from both the systems architect and
the adversary: the place is not the control.** Three corrections, all carried
into the `review-authority-intake` delta as requirement text:

**(a) The refusal's INPUT is the load-bearing question, and it must be
DERIVED, never REPORTED.** `admit_convening` reads exactly `council_id`,
`subject_pin` and `mix_id` from the posted block; `packet_refs` is never read;
there is no diff, no changed-path set, no repository handle. And the block is
CONSTRUCTED BY THE CHECKED TREE —
`codexFactory/.github/workflows/council-lane-reusable.yml:473-478`. A candidate
that narrows what its own commissioning lane reports as touched would get a
clean admission. **Ruling: the runtime computes the touched-object set from the
subject pin under its OWN credential, and a convening whose touched-object set
is unavailable, self-reported or unverifiable is REFUSED rather than admitted.**
Q6b — the candidate-side predicate, which nobody had posed — is answered, and the
cost (a per-target repository credential held by Hermes, cluster egress, a
per-target machinery map) is named as S-work rather than assumed away.

**(b) The refusal's reachable subject is MATERIALIZED DOMAIN CONTENT ONLY, and
the runtime refusal is ADDITIVE, never a replacement.** The domain content set
is `escalation-rules.yaml`, `agent-mixes.yaml`, `memory-boundaries.yaml`,
`practice-catalog.yaml`, `roles/`, `policies/`, `review-councils/`. `scripts/` —
"the decision core's whole import root", the surface LS-A3's `scripts/yaml.py`
attack actually used — is NOT domain content and never will be. **The runtime
refusal, fully built, would not have caught the one attack that has been
executed.** codexFactory's `"scripts/**"` floor entry, its `/scripts/ @brettheap`
CODEOWNERS line and its import-root coverage test therefore remain the SOLE
defence for the decision core. Nothing in this change retires them, and no
sentence in this document claims the runtime refusal substitutes for them.

**(c) The content channel is now wired — this was a live drift and it is
FIXED.** The 2026-08-22 text cited the neutral SCHEMA and its EXAMPLE for the
`review_council` mapping while codexFactory's live manifest declared only
`domain_ontology`, and the runtime's `CONTENT_KINDS` did not know
`domain_ontology` at all — so the archive failed to seed pre-write and
`admit_convening` refused every convening with `council.unseeded`. Both halves
landed 2026-08-23 and are on `origin/main` in both repositories:

- **codexFactory `dcfbd96`** — "Domain content manifest declares the COMPLETE
  shipped set (reseed-breaking drift, half 2 of 2)": `hermes/domain/content-manifest.yaml`
  now declares all eight kinds at their conventional locations, including
  `review_council: hermes/domain/review-councils` and
  `deliberation_mix: hermes/domain/agent-mixes.yaml`, with a completeness guard
  `tests/domain-content/test_content_manifest_completeness.py` that fails when
  the repo ships a conventional artifact the manifest does not declare.
- **hermes-install `3de0519`** — "Runtime learns domain_ontology
  (reseed-breaking drift, half 1 of 2)": `CONTENT_KINDS` admits
  `domain_ontology`, with a schema-parity guard against the neutral
  `content-manifest.schema.yaml`.
- End-to-end proven, and **the deploy constraint is recorded, not glossed**:
  codexFactory `3143f34`,
  `hermes/domain/review-councils/records/2026-08-23-reseed-deploy-ordering-addendum.md`
  — *no reseed until a hermes-install image at `3de0519`+ is deployed; the
  repository state is safe in every order since `dcfbd96`, the deployed state is
  not until the image ships.*

This is cited as **landed evidence with a deploy constraint**, not as a
precondition. The systems architect's concern 4 and the adversary's finding 1(b)
are discharged by the fix rather than argued with.

**(d) What remains honestly unfixed.** The floor's own SOURCE OF TRUTH is a
markdown record (`hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`,
and "where it and that record ever diverge the record governs" —
`add-substantive-review-lane/…:328-333`), while `_find_dir_at` seeds only
`*.yaml` and hard-excludes `/records/`. So the authoritative text of the ceiling
this proposal declares untouchable lives in a file that is structurally excluded
from the runtime that would enforce against it, has no schema and no validator,
and is gated only by `/hermes/ @brettheap` — which `--admin` bypasses. **That
inversion is real, it is not fixed by this change, and it is carried as Q9.**

### 4. The intake — the genuinely new operational artifact, with its MVP named

Everything above composes ratified primitives. **This does not, and it is the
piece with no prior art in the corpus.**

**A governed surface where each AI and each council is issued its authorities
and duties.** For every reviewing holder the intake records: what it may review
(`scope.acts`), over which objects (`scope.objects`), at which rung
(`scope.authority_tier`), until when (`expires_at`), under what revocation,
derived from which parent (`parent_grant_ref`), and issued by whom (`issued_by`).
Duties sit beside authorities: the seat a holder is required to fill, and the
distinct-holder constraints it is subject to. Beside those, per S2 and the
custody rule of §2, it records each wallet's custody ATTESTATION.

**The product advocate's concern 3 is upheld: an artifact designed entirely in
open questions is not a design.** The MVP is therefore named IN SCOPE, and it is
a requirement of the capability rather than a suggestion — see S4. Its shape:
one file at a fixed path in openxFactory, one holder (the
`merge_readiness_council` as a body), one target repository, one act, tier
`act`, one `expires_at`, and one validator whose only job is to fail a convening
that admits a holder with no active row. **Everything wider is a successor** —
per-seat grants, per-project schema election, distinct-holder enforcement,
multi-target rows.

**And the ratification condition the product advocate asked for is adopted:**
`review-authority-intake` is NOT realized until the register and a validator
that reads it land in the SAME change. That is the cheapest available guard
against the CODEOWNERS outcome, and it costs one requirement.

**One negative shape is asserted, and it comes from the liaison doctrine:** the
intake MUST NOT issue one holder both the review act and the approval act over
the same object, because that collapses `execution_binding.actor_ref` into
`approval.authority_ref` — the three parties
`client-infrastructure-liaison/spec.md:18-30` says are "never collapsed into
one".

## What this creates that does not exist

Established by investigation, and corrected against all five reviews — each
earlier silence claim that did not survive verification is restated rather than
repeated.

- **Spec authority distinct from code authority AS A HELD, DELEGABLE ROLE** —
  absent. The adjacent prior art is REPOSITORY-grain, not role-grain:
  `openspec/changes/archive/2026-07-09-reconcile-domain-neutral-and-engineering-spec-ownership/`
  settled which REPOSITORY owns neutral specs versus engineering
  implementation, with three MODIFIED deltas and no new capability. What is
  genuinely absent is a NAMED, HELD, DELEGABLE authority on either side. Any
  such role's canonical definition must live in openxFactory
  (`canonical-policy-migration:33-38`), which is why the role definitions land
  in the `roles-authority-model` delta and not in the new capability.

- **A register issuing authorities to reviewing agents and councils** — the
  intake. Nothing in `openspec/specs/`, `docs/` or `contracts/` carries one.
  `openxwallet` supplies the record type and says nothing about who keeps the
  register; `openxwallet-agent-profile` supplies the composition declaration and
  says nothing about issuance. **Nor does anything supply an issuer bound:**
  `issued_by` is optional in the grant schema (`:90`, absent from `required:` at
  `:34-41`) and is read by ZERO rules in `scripts/validate-openxwallet.py`.
  There is no notion of issuer authority anywhere in the contract family. S2
  supplies one.

- **Ownership of a path or artifact BY A ROLE** — CODEOWNERS borrows the syntax
  but means "human gate" (codexFactory `.github/CODEOWNERS:5-9`), it has no
  upstream neutral source, and **no validator anywhere in openxFactory reads
  it** (zero hits across `scripts/`, `openspec/specs/`, `contracts/`; verified
  independently by two reviewers).

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
  What remains a silence after that change lands is the general rule, not its
  rationale.

- **An exercise record for a review act** — absent, and this is the gap S3
  closes. A council seat casting a GitHub review produces no wallet-signed
  exercise today; `grep` across `openxFactory/scripts/`,
  `installs/hermes-install/src/` and codexFactory returns zero wallet code and
  zero `xfactory_wallet_grant` instances outside `contracts/openxwallet/examples/`.
  **openxwallet is contract-only and has never been instantiated.**

## Reconciling the two standing statements

The first draft said this change "must overturn" two standing statements. It
must not, and saying so was itself a defect: an unmarked contradiction of a
promoted spec is a reportable health finding under the Explicit delta rule
(`openspec/specs/document-lifecycle/spec.md:96-113`, scenario `:111-113`).
**Both reconcile by SCOPING, and neither needs a MODIFIED delta.** The adversary
tested both and could not break either; they are kept unchanged.

**"Authority never transfers" (`openspec/specs/doc-health/spec.md:572-575`) —
reconciled by scope, not by attribution.** It is a `#### Scenario:` heading
under the requirement "Candidates become staged proposals under human approval"
(`:557`), and its body is scoped entirely to the neutrality-drift lane: "it
reports and stages only — content authority stays with the owning factory"
(`:575`). What that scenario bars is a REPORTING LANE acquiring EDITING
authority IMPLICITLY, BY DISCOVERY — finding a misplacement does not license
moving it. An explicit, audience-named, expiring, revocable grant is a different
act by a different party: conferral by the holder, recorded before the fact,
revocable at exercise. The scenario governs conferral by discovery; the
instrument is conferral by issuance.

The anti-stand-in fixture is a SEPARATE and also-necessary argument on the
attribution axis: a delegate acts AS ITSELF under its own grant, never as a
proxy laundering an act onto the audience — "precisely the false audit record
this family exists to refuse"
(`contracts/openxwallet/examples/negative/exercise-attributed-to-a-wallet-not-presenting-its-key.yaml:12-14`,
realizing `openxwallet/spec.md:93-111`).

**And the adversary's limit on that fixture is upheld and carried.** The fixture
is an EXERCISE-RECORD rule: it works by deriving the presenting wallet from the
verified proof key. Under an exercise model with no wallet signature there IS no
exercise record, so the fixture's key binding never runs — and what is left is
an intake entry saying "seat X holds review authority over object Y" plus an
approval cast by the merge-master GitHub App, a shared installation credential
that `openxwallet/spec.md:93-111` requires be recorded as transport with the act
`unattributed`. A reader of the intake plus the check-run would attribute the act
to seat X. **That is the same false audit record, relocated one layer up from the
record to the register.** It is the decisive reason exit B is rejected in S3, and
the intake carries an explicit requirement that a recorded grant never supplies
attribution a key did not establish.

**"Ownership confers no authority" — reconciled because the instrument
CONFORMS to it, not despite it.** Promoted requirement text, not doc prose:
`openspec/specs/client-infrastructure-liaison/spec.md:18-30`, Requirement
"Coordination, execution, and validation separation," scenario "Ownership does
not confer authority" at `:28-30` — the liaison "gains no tenant-administration
authority from that ownership, and any privileged action still requires the
binding's approved execution owner **and grant**." Under wallet-carried
authority a holder's standing comes ENTIRELY from its grant and NEVER from an
ownership label.

**Which is why the roles are renamed.** The first draft called them "spec owner"
and "code owner" while the corpus reserves "ownership" for a relation that
explicitly confers no authority. They are **spec authority** and **code
authority** throughout this proposal and in the `roles-authority-model` delta.

## `consent-instrument` is a named NON-precedent

The first draft recommended modelling the instrument on `consent-instrument`.
**That recommendation is DROPPED.** Incompatible with the grant realization on
three counts; three reviewers reached this independently and the adversary
called the first count decisive on its own:

1. `consent-instrument` requires an amendment to be "a status transition
   carrying its delta on the existing instrument; a new instrument referencing
   a parent is **nonconformant**" (`:115-126`). openxwallet narrows ONLY by
   deriving a new grant carrying `parent_grant_ref` (`:91-94`). Amending a
   delegation IS revoke-and-reissue-as-derived — the exact shape
   `consent-instrument` calls nonconformant.
2. The lifecycles are different closed enums:
   `draft → pending_signatures → executed → amended → terminated` plus
   `withdrawn` as a DISTINCT second terminal state that "MUST NOT be declared
   as an alias of `terminated`" (`:69-98`), against the grant's
   `state: [active, expired, revoked]` (`openxwallet-grant.schema.yaml:95-97`)
   under `additionalProperties: false` (`:42`).
3. Modelling on one while realizing as the other would produce precisely the
   "parallel authority vocabulary" that is a declared validation failure
   (`openxwallet-agent-profile/spec.md:65-69`).

Kept as a NAMED NON-PRECEDENT, because being explicit about what was considered
and rejected is cheaper than rediscovering it.

**Its sole-operator passage is the near-miss worth naming.** "Authority Basis Is
First-Class" (`:100-113`) handles one person controlling multiple rungs of an
engagement by recording the authority basis per party and treating a shared
signer as "a recorded SHOULD deviation, not a silent one." **That is a
DISCLOSURE answer, not a STRUCTURAL one** — and the corpus's only sole-operator
pattern is therefore disclosure. This change proposes structure instead, and the
intake is the natural place to record such a deviation when structure runs out.

## The recommended project schema — human-elected, and it confers nothing

**Not a bench question.** The convener's 2026-08-22 ruling: *"For our own
internal projects, we can have codeXfactory recommend and run a 3 repo project
schema. But let the human project manager decide."*

codexFactory may recommend — and scaffold — a three-repository shape for a
project: SPEC (the governing specs and contracts), CODE (the implementations),
and ASSEMBLY (the code that assembles a review team, shared across the family).
The argument for it is ergonomic and real: when spec and code sit in different
repositories, who holds spec authority and who holds code authority is visible
from the repository list instead of inferable from a register.

**Adoption is a PER-PROJECT DECISION BY A HUMAN, never a precondition of review
and never a governance requirement.** A one-repository project and a
three-repository project are reviewed IDENTICALLY, because the authority travels
in the grants rather than in the layout. **Electing the schema changes no gate,
no floor, no grant, and no clearance eligibility.** A project that DECLINES it is
not less governed and is not reviewed more suspiciously; a project that ADOPTS
it earns no additional clearance.

**Q7's deciding role is RESOLVED, and this document stops posing it.** Checked
against the ratified neutral Owns/Decides table (`docs/roles-and-authority.md:67-74`):
the decision content is repository layout, and `PA` Project Architect owns
"project architecture, project integration shape, project architecture
decisions" and decides "**where project boundaries sit**" (`:72`) — `CA`
Chief Architect constrains it by deciding "whether repo design violates the
system model" (`:71`), and `PM` sequences it (`:70`). **The election is a `PA`
decision, `CA`-constrained and `PM`-sequenced.** The convener's phrase "the human
project manager" named the human, not the role token; the ratified table names
the role. Both `PA` and `PM` are human Hermes-level roles, so the convener's
substantive point holds either way.

*Where it is recorded* is the project register at the aggregation root
(`kind: project-register`, neutral schema at
`contracts/schemas/project-register.schema.yaml`), which already declares the
exact posture a schema election needs: "Grouping is descriptive navigation only:
**it confers no lifecycle state and no authority** over the repositories it
names." A register that confers nothing is the right place to record a choice
that confers nothing. Recording it there is S-work for whichever project elects
the schema, not work of this change.

**Consequently this change declares NO repository-boundary obligation.** It
creates no repository, moves no runtime code, changes no submodule pointer and
advances no pin. The obligations that WOULD attach to an electing project are
enumerated here so that project inherits the list rather than rediscovering it:

- a new repository is the NINETEENTH submodule of the aggregation repo (18
  today; the README's 13-entry `## Current Submodules` list is stale);
- the boundary is declared BEFORE the repository exists — the house does this
  routinely, eight instances, zero new capabilities;
- the template is "Neutral avatar-client repository boundary"
  (`repo-boundary-governance:113-137`), NOT "Install repository scope"
  (`:29-40`), which is name-scoped to the two install repos; and the aggregation
  act is bound by "Deferred aggregation and web-console integration"
  (`:165-181`) with its eight-element record (path, remote, visibility, exact
  validated commit, checkout, compatibility, update, rollback);
- moving existing machinery trips a declared STOP CONDITION on two counts —
  beyond copy-first (`:41-58`), `:59-76` makes "moving runtime code" and
  "changing submodule pointers" stop conditions requiring a return to Hermes
  approval;
- and it is a devolution act: "the owning Domain Hermes approves surrendering or
  receiving a concept, boundary governance approves the neutral side, and both
  gates are OpenSpec changes, never bare commits"
  (`docs/domain-to-neutral-promotion-process.md:299-306`).

**Two cautions for any electing project.** If an ASSEMBLY repository ever holds
the gate RULES rather than only the engine, it collides with a canonical home:
`codexfactory-routine-code-clearance.yaml` is rules-as-code — merge authority
POLICY — canonically openxFactory's under `repo-boundary-governance:8-13` and
`canonical-policy-migration:44-48`. Scaffold ENGINE; leave rules where policy
lives. And any consumer pin must be content-addressed:
`shared-contract-ownership:84-91` and `:101-103` require "the exact openxFactory
commit and per-file digests" and rule that a tag alone is not a content-addressed
pin.

**One property the schema buys that is not ergonomics.** Today the aggregation
caller "checks out `opensoft/codexFactory` at a migration pin because the
decision core is a FOREIGN repository there", while the local lane deliberately
does not pin because "the base-branch checkout — not a pin — is what stops a
candidate altering the rules that govern it"
(`council-convening-lane.yml:36-45`). Under a separated assembly plane the core
is foreign to every consumer, so a change to the review machinery is judged
under the PRIOR constitution. **The product advocate proposed coupling that
property to a digest-disjointness ruling to give election something to earn.
That coupling is DECLINED, because the narrowed floor it would couple to is
declined (PART III).** The property is recorded as a true ergonomic-plus-safety
argument for election, and election stays worth nothing in governance terms —
which is the whole point of leaving it to a human.

---

## PART II — THE SUBSTRATE

Nothing in this part is pretended. Each item names what exists today, what does
not, and what closes the gap. The doctrine of PART I is ratifiable now; the
controls it names become real here, in order.

## Cold start

**Zero wallet instances exist in the family.** There is no `xfactory_wallet`
record anywhere in openxFactory outside `contracts/openxwallet/examples/` (16
example files, zero live); `grep` across `openxFactory/scripts/`,
`installs/hermes-install/src/`, codexFactory `scripts/` and `hermes/` returns
zero wallet code. openxwallet is contract-only and has never been instantiated.

**The custody registry says the key situation in terms.** `holder_readable`'s
own notes: "This tier reaches `act` deliberately. Capping software custody lower
would stall every consumer… **there is no key infrastructure in the stack
today.** Approval before apply is the compensating control at this tier"
(`openxwallet-custody.registry.yaml:53-58`).

**The holders needing wallets are about eight.** codexFactory's `gate-rules.yaml`
and `merge-readiness.yaml` name roughly six distinct seats —
`company-policy-lead`, the intent-owner role slot, `lead-quality`,
`lead-security`, `lead-integration`, plus the conditional CSC seat — plus the two
councils as bodies. Each needs a wallet with a declared custody model (realistically
`holder_readable`, the only model achievable with no key infrastructure), a
declared composition hash over six components, and — per §2 — a recorded custody
attestation, or its grants cap at `request`.

**The root issuer needs no wallet, and that single sentence removes the circular
dependency.** The root issuer of review authority is the RESPONSIBLE OPERATOR,
whose authority is STANDING under the Human Escalation Contract
(`docs/roles-and-authority.md:103-140`), whose parked-decision list names
"privileged capability grants (deployment, production)" among the decisions only
a human holds (`:127`). That standing is not conferred by any grant, is not
recorded in the register it writes into, and therefore needs no wallet. This is
the answer to the question the 2026-08-22 text posed as Q2 and it is now settled
requirement text, not a posed option.

**Day-one order, and it is not negotiable in sequence:**

1. **S1** — wire the validator into CI as a required check. Until this, no grant
   is operative, so issuing one first would be issuing nothing.
2. **S2** — the issuer anchor: `issued_by` required for review-authority grants,
   the root-grant class defined, the operator named as root issuer.
3. **The first wallet** — one holder, `holder_readable`, with its attestation row.
4. **S4's MVP** — the register and its reader, in one change.

S3 and S5 follow; neither is reachable before a grant exists that a reader
honours.

## The build, in order — S1 through S5

Each item states its HONEST CURRENT STATE first. None of these is performed by
this change; each is a successor carrying its own `code_surface` and archiving
on merged, green evidence per `release-realization`.

### S1 — Wire `validate-openxwallet` into CI as a required check

**Current state: it runs in NO workflow.** `.github/workflows/` in openxFactory
contains exactly `doc-health-reusable.yml` and `session-open-pr.yml`;
`validate-openxwallet` appears in neither, and there is no `tests/*wallet*`
directory. Every rule the doctrine leans on — the custody ceiling, attenuation,
the audience binding, the revocation chain — runs only when a human types the
command.

**The adversary's rule is adopted VERBATIM as requirement text:** *an intake
entry with no reader confers nothing.* Until the validator is a required check
on the repository holding the register, **NO grant is operative** and this
document does not describe grant properties in the present tense.

**Gate:** the check is required on the register's repository, and a deliberately
malformed grant fails the PR.

### S2 — The issuer anchor

**Current state: `issued_by` is OPTIONAL in the grant schema (`:90`, absent from
`required:` at `:34-41`) and is read by ZERO rules in the validator.** There is
no notion of issuer authority anywhere in the contract family. Attenuation binds
only where `parent_grant_ref` is present, so a grant WITHOUT one is a root, and
the only thing bounding it is the audience wallet's declared custody ceiling —
which §2 has just established is a self-declared string. **Monotonic attenuation
below an unbounded root is a strictly local property.**

**What S2 does.** `issued_by` becomes REQUIRED **for review-authority grants** —
a scope restriction imposed by the composing capability, NOT a schema change:
the field already exists and stays optional in the shared grant schema, so no
other consumer is disturbed and no contract bundle is cut. A grant carrying no
`parent_grant_ref` is a NAMED ROOT-GRANT CLASS, and a root grant's issuer's
authority is recorded OUTSIDE the register that grant writes into.

**Q2 is ANSWERED, not posed.** The root issuer is the responsible operator,
whose authority is standing under the Human Escalation Contract, and who needs
no wallet (## Cold start). A root grant naming an agent holder as issuer is
refused — a root issuer's authority cannot be conferred by the register it
writes into.

**Gate:** the validator refuses a review-authority grant with no `issued_by`,
and refuses a root grant whose named issuer is not the recorded operator anchor.

### S3 — The exercise record, at verdict conformance

**Current state: there is no exercise.** A council seat casting a GitHub review
produces no wallet-signed exercise record. `contracts/openxwallet/openxwallet-grant-exercise.schema.yaml`
requires `proof_of_possession`, `attribution`, `custody_model_in_force`,
`revocation_check` and `event_class` under `additionalProperties: false`.

**Two exits were on the table and one is REJECTED.**

*Exit A — a signing point in the convening flow, enforced at admission.* The
only out-of-tree component is the Hermes runtime, whose ratified
`council-orchestration` capability forbids it from enforcing: "A recorded verdict
is advisory evidence only… SHALL derive no approval, merge, dispatch, or any
other state transition beyond the job's own resolution from any verdict."
Inverting that is a much larger act than "downstream realization".

*Exit B — grant recorded, exercise evidenced by the existing council or
enforcement audit trail.* **REJECTED, on the adversary's ground.** Such an act
records as `event_class: unauthenticated_request` and `unattributed`;
`openxwallet/spec.md` rules that such an act "is not assigned to a holder" and
that "no authority is conferred by presentation alone". **A grant whose every
exercise is unattributed confers nothing checkable** — that is not a declared
deviation, it is a grant that is documentation, at higher stakes than the
CODEOWNERS precedent. Declaring it does not stop it being the thing.

**ADOPTED — the systems architect's third exit.** The seat's wallet key is minted
INSIDE the deliberation job; the Hermes runtime verifies the signature over the
seat return at **`check_verdict`**; the exercise is recorded there.

**Why this needs no `council-orchestration` amendment, stated precisely.** The
runtime's SECOND requirement — "A convening verdict conforms to the council's
materialized semantics or is refused" — already has the runtime refuse a
completion fail-closed when the verdict block is malformed: wrong pin, missing
seat result, inconsistent unanimity. A missing or unverifiable seat signature is
a CONFORMANCE defect of the same kind. The runtime is not interpreting the
verdict, deriving an approval, or transitioning anything beyond the job's own
resolution — so the advisory-only requirement is untouched. **Refusing a
malformed verdict is already the runtime's job.**

**Gate:** a convening completion whose seat return carries no verifiable
signature is refused fail-closed, and a conforming one writes an exercise record.
**Only when S3 lands does `distinct_holder_constraint_refs` become the observable
that supersedes QA 4.2** — the constraint's comparison basis is the prior act's
RECORDED HOLDER, and until exercise records exist there is nothing to compare
against.

### S4 — The register and its reader, landing together

**Current state: no register exists, and the cautionary precedent is live** —
nothing in openxFactory reads CODEOWNERS, verified twice.

**A ratification condition of the capability, per the product advocate:** the
register and a validator that reads it land in ONE change. A register alone does
not realize `review-authority-intake` and must not be archived as though it did.

**MVP shape, in scope and normative:**

| element | first shape | successor |
|---|---|---|
| location | one file at a fixed path in openxFactory | per-repo instances |
| holder | codexFactory's `merge_readiness_council`, as a body | per-seat grants |
| target | one repository | all governed targets |
| act | one review act | the act vocabulary |
| tier | `act` | — (`act_unsupervised` is refused, §2) |
| expiry | one `expires_at` | lifecycle policy |
| reader | one validator: fail a convening admitting a holder with no active row | full grant validation |

**Q1 is ANSWERED for the first shape and its LIMIT is stated.** The register's
canonical home is openxFactory: it owns "the canonical cross-factory role and
authority model… their canonical responsibility, authority, and escalation
boundaries MUST live in openxFactory" (`canonical-policy-migration:33-38`), and
merge-authority concepts are canonically openxFactory's
(`repo-boundary-governance:8-13`).

**Q1c — the design constraint that must travel with that answer.** *A file-based
register cannot satisfy revocation-at-exercise.* `openxwallet/spec.md:113-119`
requires checking revocation at exercise and its scenario rejects issuance-time
validity as evidence of current validity. Both file-based options — a canonical
neutral register with per-target rows, and a neutral schema with per-repo
instances — are git files reaching consumers through digest-pinned, lagging
distribution (`stack.yaml` pins the openxFactory version; layer content is
fetched by digest pin and sha256-verified fail-closed). **A pinned register IS an
issuance-time snapshot**, and a revocation would take effect only at the next
re-pin and re-seed, a human lifecycle act. The conforming home for the REVOCATION
SURFACE is a **live lookup on the Hermes runtime**, which already holds Postgres,
layer identity and the job lifecycle. The first shape is a file because the first
shape has one holder and one target; the revocation surface is named as its own
successor and the file is not pretended to be one.

**The register is DECLARED a permanently human-only surface under the
constitutional floor, explicitly** — not left to inference from the floor's four
path clauses. The adversary's ground is decisive and is upheld: openxFactory is
the substantive review lane's PILOT REPOSITORY (`add-substantive-review-lane:149`),
so without this declaration the register that issues review authority would live
in a repository whose PRs are reviewed by councils holding grants issued from
that register — **councils clearing their own commissions.** A grant register is
authority policy but is not literally "contract bytes, gate or workflow
definitions, credential surfaces, or security posture", so it plausibly falls
OUTSIDE the floor's four clauses. It is therefore entered by name.

**Gate:** the register exists at its declared path, its validator is a required
check (S1), the register's path is a named never-clearable floor member in the
target's gate rules, and a convening admitting a holder with no active row fails.

### S5 — Revocation, lifecycle, and blast radius

**Current state: the runtime is issuance-bound by construction, deliberately.**
`verdict_for_completion` takes the member roster AND the content provenance from
the `convening` stamp written at ADMISSION — the docstring says why: "the
convening was authorized against that content." A seat whose grant is revoked
between commission and verdict is still a required member; honoring the stamp is
exactly the issuance-time trust `openxwallet:127-131` forbids. Dropping the seat
trips `VerdictMissingSeatError` under `missing_required_seat: refused`, so the
convening parks. **Q4's "all three?" was a contradiction, not a menu.** Grant
expiry has the same shape: `expires_at` is REQUIRED, `state` is a field INSIDE
the grant record, and nothing recomputes it.

**What S5 requires:**

1. **The exercise checkpoint is reconciled with the admission stamp.**
   Re-check at VERDICT CONSUMPTION; on a revoked or expired holder, **park with a
   NAMED REFUSAL** — never silently honour the stamp, and never accept the
   stamp as evidence of current validity.
2. **A declared staleness bound** on the register, stated as a duration.
3. **Unreadable register ⇒ REFUSE, never proceed.** Unreachable, unparseable, or
   older than the bound all refuse.
4. **Composition blast radius bounded.** `openxwallet-agent-profile:27-48`
   revokes on ANY single component change, "with no tolerance band and no grace
   period", and `distinctness_floor: composition_hash` makes model version a
   declared component. A provider silently rolling a model alias therefore
   revokes every seat grant in the fleet at once; with
   `missing_required_seat: refused`, every in-flight and future convening parks;
   and **the only routine exit from a parked candidate under a sole code owner is
   `--admin`** — the change's own strictest inherited control manufacturing the
   ritual the change exists to break. So: **model version and prompt corpus are
   PINNED as declared components**, the retrieval corpus is never the candidate
   repository at HEAD, and a provider roll becomes a **governed re-issuance event
   with a named runbook** rather than a silent fleet-wide revocation.

**Gate:** a revoked holder parks a convening with a named refusal in a rehearsed
test; an unreadable register refuses; the runbook exists and has been walked once
against a deliberate composition bump.

---

## PART III — THE FLOOR

## The narrowed floor amendment is DECLINED

The 2026-08-22 text asked the bench to rule on a NARROW reading of the
constitutional floor: that a DIGEST-DISJOINT reviewer is not a member of the
class the floor excludes. **The convener declines it and removes it as a bench
question entirely.** It is not carried as an open question, not deferred, and not
named as a successor.

**The grounds, from the adversary's fifth finding, quoted where quotable:**

- **The primitive carries its own disclaimer, in the schema this change is
  composing.** `contracts/openxwallet/openxwallet-distinct-holder-constraint.schema.yaml:30-36`:
  *"Two agents from the same model, orchestrator and prompt are not independent
  the way two humans are; this constraint defends against slips and loops, not
  against a wrong policy applied consistently by both. The agent profile's
  composition hash gives an objective floor — different hash, different holder —
  and **whether that floor suffices is left to the consuming domain**."* The
  composition hash shipped as a DISTINCTNESS floor with an explicit disclaimer
  that it is not an independence test. Repurposing it as one, to justify
  narrowing a floor whose stated target is correlated unanimity, uses the
  primitive against its own recorded caveat.
- **It is ANTI-CORRELATED with the property it proxies for.** It "rejects the
  right case and admits the wrong one": different weights under the same prompt
  contract — the case that most improves independence — FAILS prong (i), while
  two seats on the same base model with independently authored prompts, tool
  manifests and corpora share no digests and pass cleanly while being maximally
  correlated.
- **Byte identity is the wrong measure.** A fork fails prong (i) only where bytes
  are identical; a fork whose prompts are regenerated from the same generator, or
  reformatted, or carry a version header, produces different digests and passes.
- **Completeness is unverifiable.** The hash is over a DECLARED set;
  `check_agent_composition` never checks that a digest is correct and cannot
  check that the set is complete. A reviewer can be digest-disjoint by OMITTING
  the components it shares with the machinery. Since the intake is where the
  declaration is recorded and the same operator configures the reviewer,
  self-report is the whole chain.

**The seeded-corpus evidence does not rescue it either, and its own warning is
quoted rather than omitted.** codexFactory's `2026-08-22-seeded-adversarial-corpus.md`:
"This corpus cannot distinguish 'diversity does not help' from 'these three
defects were too easy for the question to arise', because no defect was missed by
anybody… **Anyone citing this record for the proposition that seat diversity is
unnecessary is citing it wrongly**" (`:359-364`).

**The operative position, and it is now the only position in this document.**
The constitutional floor stands WHOLE. Assembly-class surfaces — contract bytes,
gate and workflow definitions, credential surfaces, security posture, and the
intake register — stay **permanently human-only** until a real independence test
exists. **Defining one is NOT named as a successor, because it is not currently
definable.** If someone later believes it is, that is a new proposal starting
from zero, and it will need its own declared MODIFIED delta amending the floor
requirement under the Explicit delta rule (`document-lifecycle:96-113`). Nothing
in this change pre-declares it and nothing elsewhere in this document assumes it.

---

## Open questions — the reduced set

The 2026-08-22 text posed seven. **Six are answered above and are no longer
posed**; the seventh (the narrowed floor) is declined. Three questions remain,
one of them new.

| was | disposition |
|---|---|
| Q1 — where does the register live? | ANSWERED — openxFactory, one file at a fixed path (S4); with Q1c's constraint that a file cannot satisfy revocation-at-exercise and the revocation surface's conforming home is a live Hermes lookup |
| Q2 — who issues, what bounds the issuer? | ANSWERED — the responsible operator, standing under the Human Escalation Contract, needs no wallet (S2, ## Cold start) |
| Q3 — what validator reads it? | ANSWERED — S1 wires one into CI as a required check; S4 makes register-and-reader a ratification condition |
| Q4 — the exercise checkpoint | ANSWERED — verdict consumption, reconciled with the admission stamp, parking with a named refusal (S5) |
| Q5 — what constitutes an exercise | ANSWERED — the systems architect's third exit, at verdict conformance; exit B rejected (S3) |
| Q6 — the refusal's subject | ANSWERED — materialized domain content only, additive not replacing; and Q6b, its input, is derived never reported (§3) |
| Q7 — the schema election's home and role | ANSWERED — the project register; `PA`, `CA`-constrained, `PM`-sequenced |
| the narrowed floor | DECLINED (PART III) |

### Q8 — Composition drift for hosted-model holders (NEW)

Every reviewing holder in this family is a hosted model. `openxwallet-agent-profile`
revokes an agent's outstanding grants on ANY declared-component change with no
tolerance band and no grace period, and model version is a declared component.
S5 bounds the blast radius by requiring pins and a runbook; **it does not settle
the policy questions the first alias roll will raise.** Posed with its exits, not
decided:

- *Is a standing reissue policy a first-class INTAKE ACT?* Exits: (a) the intake
  supports a declared "reissue on composition change" policy per holder,
  executed as a governed act with the operator's root authority; (b) every roll
  is a fresh manual issuance; (c) grants carry a composition-tolerant derivation
  that the agent profile does not currently admit — which would need an
  `openxwallet-agent-profile` delta and is named here as the expensive exit.
- *Do DERIVED grants survive a parent revoked for DRIFT rather than for CAUSE?*
  The chain rule (`openxwallet:121-125`) kills the chain on any parent
  revocation. Exits: (a) they die, and re-issuance is a chain-wide act; (b) the
  revocation block's `reason` distinguishes drift from cause and derived grants
  survive drift — which is a real narrowing of a ratified propagation rule and
  would need its own delta.
- *Who tells the operator the register emptied?* Nothing notifies today.
  Exits: (a) the required check fails on the next PR and that is the
  notification — cheap, late; (b) a scheduled staleness sweep parks a
  decision-ready packet per the Human Escalation Contract; (c) the runtime
  refuses at exercise and the refusal is the signal — which is the worst,
  because it lands mid-convening.
- *May a hosted holder pin a model FAMILY rather than a version?* **Today that
  is a validation failure** — the declared component is a version and any change
  revokes. Exits: (a) no, and the operational answer is the reissue policy above;
  (b) yes, with the family pin declared as a reference-bound component carrying a
  governing-configuration digest — which weakens the composition hash's meaning
  and must be argued on its own.

*Posed for a bench, not decided here. It is a real product decision and it will
be discovered at the first model bump if it is not answered before.*

### Q9 — The floor's source-of-truth inversion

The constitutional floor's SOURCE OF TRUTH is a markdown record in the reviewed
tree that the runtime structurally cannot read: "where it and that record ever
diverge the record governs"
(`add-substantive-review-lane/specs/roles-authority-model/spec.md:328-333`),
while `_find_dir_at` seeds only `*.yaml` and hard-excludes `/records/`. The
record has no schema and no validator, and is gated only by `/hermes/ @brettheap`,
which `--admin` bypasses. *Posed with two exits: (a) move the floor's
source-of-truth into a seedable, schema-validated `.yaml` carrier and demote the
record to evidence; or (b) amend `roles-authority-model` so the PROMOTED SPEC
TEXT governs and the record is evidence. Both are amendments to a ratified
requirement and neither is taken here.* This is the adversary's finding 1(c),
carried rather than closed, because closing it is an amendment to another
change's ratified text.

### Q10 — Does a non-human authorizer satisfy `isolated_per_use_authorized`?

`openxwallet-custody.registry.yaml:81-94` sets the bar for the only custody model
reaching `act_unsupervised` as "an authorization that context cannot itself
supply — a hardware presence check, an external policy approval, a separate
custodian." Two of the three are not hardware and the text does not require them
to be human. *Posed: does a remote signing service requiring an approval call
from a second process satisfy the clause?* **Until it is ruled, holders declaring
`isolated_per_use_authorized` are excluded from review-authority grants** by §2's
`act_unsupervised` refusal, so the answer does not block this change — but it is
the design's largest unexamined assumption and it is named rather than left
inside a quoted clause.

## Capabilities

### New Capabilities

- **`review-authority-intake`** — the authority intake and the delegation
  instrument, together: **12 ADDED requirements.** It carries the doctrine
  (authority held only as a grant, ownership conferring nothing, no parallel
  vocabulary) and every substrate rule the councils established was missing —
  the no-reader-confers-nothing rule (S1), the issuer anchor and root-grant class
  (S2), the exercise at verdict conformance with exit B rejected (S3), the
  register-and-reader-together ratification condition with its MVP shape and its
  human-only declaration (S4), revocation at verdict consumption with a staleness
  bound and unreadable-refuses (S5), composition pinning, the `act_unsupervised`
  refusal, the unattested-custody cap at `request`, the never-both-acts rule, and
  the derived-never-reported rule for the runtime refusal's input.

  **Why one capability, not two.** The remaining seam that matters is
  instrument-versus-role, and it falls between this capability and
  `roles-authority-model` (below), not inside this one. Register and instrument
  are not separably ratifiable: an instrument with no register is unexercisable
  and a register of nothing is empty. One subject, one realization, one consumer.

### Modified Capabilities

- **`roles-authority-model`** — **2 ADDED, 1 MODIFIED.**
  1. **ADDED: the role definitions, SPEC AUTHORITY and CODE AUTHORITY.** This
     capability owns "Hermes-level governance roles (project ownership,
     sequencing, system and project architecture, merge readiness and merge
     authority)" (`openspec/specs/roles-authority-model/spec.md:9-14`), and the
     realizing artifact is the `| ID | Role | Owns | Decides |` table at
     `docs/roles-and-authority.md:67-74`. Defining two new neutral governance
     roles anywhere else would collide with a promoted ownership requirement
     (QA 6.1, upheld).
  2. **ADDED: the general non-self-review rule** — a body may not be convened
     over a candidate touching the machinery it is assembled from — REFUSAL-ONLY,
     built on the ratified rule-setting/rule-applying rationale it generalizes
     (`add-substantive-review-lane/…:231-234`), and carrying the honest limb the
     councils forced: where no out-of-tree enforcement point exists for a
     surface, the rule is recorded as UNENFORCED for that surface rather than
     described as though it held.
  3. **MODIFIED: "Pilot repository and reviewing domain"** — the
     single-reviewing-home requirement gains its authority counterpart: the home
     is single, what each holder within it may do is carried by grant, and
     extending the lane is an INTAKE act rather than a restructuring act.

  **The delta declares NO change to the constitutional floor.** The
  non-self-review rule can only REFUSE convenings; it never clears one. The
  narrowed reading is declined outright (PART III), so no floor amendment is
  contemplated anywhere in this change.

  **The delta is declared relative to `add-substantive-review-lane`'s OUTCOME.**
  `release-realization:64-70` requires BOTH limbs — "references that change AND
  declares its deltas relative to that change's outcome" — with scenario `:72-74`
  making it a MUST. The delta file states this at its head, restates the target
  requirement's FULL TEXT as that change's delta will promote it, and declares
  its modification against that text. Archive ordering is a CONSEQUENCE, not the
  remedy (QA 5.8, upheld).

### The runtime refusal and the exercise record: downstream realization, not deltas

**Decided, with the reason.** The non-self-review refusal of §3 and the
verdict-conformance exercise check of S3 both execute in the Hermes runtime,
which runs its OWN OpenSpec instance in a different repository —
`installs/hermes-install/openspec/specs/` holds `council-orchestration`,
`layer-content-seeding`, `governed-job-lifecycle` and four more. openxFactory
cannot author a delta into another repository's spec corpus.

The seam is ratified, not merely practical. `hermes-domain-overlay`'s requirement
"The subject overlay's enforceable slice is specified, and materialization is
not" (`:254-264`): "**Extraction, transaction shape, provenance, digest
verification, and refusal vocabulary remain the consumer's; openxFactory owns
document shape and canonical validation.**" A convening refusal IS refusal
vocabulary. Both are therefore successor changes in
`opensoft/xFactory-Hermes-Install` against its `council-orchestration`
capability, each carrying its own code surface and green-evidence archive gate.

**What openxFactory may owe, named rather than denied** (systems architect,
concern 4, second half): the refusal's derived candidate-side input may need a
field on the posted convening block, and `neutral-job-envelope` is an
openxFactory capability; and the register acquires a shape the moment its
validator exists. Neither is declared now — the register's first shape is one
file with one row and the rule-of-three has not fired — but both are named as
DECLARED SUCCESSORS rather than as absent. The 2026-08-22 conclusion is
accordingly softened from "no schema" to **"no new GRANT schema"**.

### One capability, and why no grant schema

**No `contracts/` schema for the grant, and this is stronger than "premature".**

1. *Rule of three.* The instrument has exactly ONE named consumer today: this
   change. `ideation/staging/tier2-council-clearance-pattern` was proposed and
   demoted the same day, 2026-08-05, on the convener's own reasoning —
   "rule-of-three trigger not fired — no second consumer has named itself"
   (`ideation/staging/INDEX.md:68`).
2. *A parallel grant schema is the very thing the corpus forbids.* The grant
   schema shipped at `contract-v1.31` and carries every property this change
   needs: `audience` (`:49-58`), `scope.acts`/`scope.objects` (`:59-79`), the
   REQUIRED `scope.authority_tier` (`:61`, `:79`), `expires_at` (`:88`),
   `issued_by` (`:90`), `parent_grant_ref` (`:91-94`), `revocation` (`:98-105`)
   and `distinct_holder_constraint_refs` (`:106-111`). "A parallel authority
   vocabulary is a validation failure" (`openxwallet-agent-profile/spec.md:65-69`).

The instrument therefore lands as REQUIREMENT text in `review-authority-intake`,
composing openxwallet rather than duplicating it. **The two scope restrictions
this change imposes — `issued_by` required, `act_unsupervised` refused — are
restrictions BY THE CONSUMING CAPABILITY on fields that already exist, not schema
changes**, so no bundle is cut and no other consumer is disturbed.

**`openxwallet` is NOT declared as a modified capability, on a verified
finding.** `ideation/staging/INDEX.md:70` records delegation chains among the
`add-openxwallet` material deferred as "a named successor gated on a consumer of
its own", and this change is that consumer. But the CHAIN MECHANICS shipped with
the 2026-08-07 realization: `parent_grant_ref` plus revocation propagation in the
schema, "attenuation only narrows" (`openxwallet/spec.md:43-47`), and "revoking a
parent kills the chain" (`:121-125`). What was deferred was a consumer, not the
primitive. The successor therefore takes the form of a COMPOSING capability — the
same structural seam as `openxwallet-agent-profile` — and no core delta is
declared. Q8's second and third exits WOULD need core deltas; they are named
there as expensive for that reason.

## Impact

- **Sequencing against `add-substantive-review-lane`.** The requirements this
  change builds on are ADDED by that change, which is ratified but ACTIVE — its
  text is not yet promoted into `openspec/specs/roles-authority-model/spec.md`
  (11 requirements today, none of them the floor, the pilot requirement, or the
  company-policy seat). Per `release-realization:64-74` this change references
  that change AND declares its deltas relative to its OUTCOME. The house runs
  this pattern routinely — `implement-keycloak-install-repo` MODIFIES a
  requirement ADDED by the still-active `add-identity-brokering`.
- **No `contracts/` artifact, no `contracts/manifest.yaml` entry, no
  `contracts/CHANGELOG.md` line, no bundle cut.**
- **Landed evidence this change relies on, with its deploy constraint.**
  codexFactory `dcfbd96` (complete eight-kind content manifest plus completeness
  guard) and hermes-install `3de0519` (runtime learns `domain_ontology` plus
  schema-parity guard) are on `origin/main` in both repositories and the path is
  proven end to end. The constraint recorded in codexFactory `3143f34`
  (`records/2026-08-23-reseed-deploy-ordering-addendum.md`) travels with them: **no
  reseed until a hermes-install image at `3de0519`+ is deployed.** These are cited
  as landed evidence, NOT as preconditions of this change.
- **`doc-health` is NOT declared as a modified capability, with the reason.**
  The "Authority never transfers" scenario (`:572-575`) is scoped to the
  neutrality-drift lane, so a recorded, issued, revocable grant sits OUTSIDE it
  rather than as an exception to it. Reconciliation by scoping, recorded so it is
  not silent (`document-lifecycle:96-113`).
- **`client-infrastructure-liaison` is NOT declared as a modified capability,
  with the reason.** Its Requirement "Coordination, execution, and validation
  separation" (`:18-30`) already locates authority in "the binding's approved
  execution owner and grant" and never in ownership, so a holder whose standing
  is entirely in its grant CONFORMS to it. The intake additionally adopts its
  three-parties-never-collapsed rule as a positive obligation.
- **`repo-boundary-governance` and `shared-contract-ownership` deltas are NOT
  declared, and not merely deferred.** This change creates no repository, moves
  no runtime code, changes no submodule pointer and advances no pin. A PROJECT
  that later elects the recommended schema takes those obligations on in its own
  change; they are enumerated under ## The recommended project schema.
- **Downstream realization, named and NOT performed here** — S1 through S5, each
  its own successor with archive-on-evidence discipline per `release-realization`,
  plus the scaffolding by which codexFactory OFFERS the three-repository project
  schema (offering it is realization work; electing it is a human's per-project
  act; neither is performed here).
- **Nothing here retires any existing in-tree defence.** codexFactory's
  `"scripts/**"` floor entry, its `/scripts/` CODEOWNERS line and its import-root
  coverage test stand untouched, and §3(b) states that the runtime refusal cannot
  reach the decision core at all.
- **README bookkeeping.** This change MUST be listed in `README.md`'s
  `## OpenSpec Records` → `Active changes:` block (`:303-305`) in the same commit
  that first tracks the change folder (Architect F20).
- **No existing gate is weakened and no `--admin` bypass is removed by this
  proposal.** The constitutional floor stands exactly as ratified and is now
  declared to cover the intake register. The non-self-review rule is
  refusal-only. ## Why states this up front rather than leaving it to be
  discovered here.

## The council's disposition ledger

Every finding from the five review files, with where it landed. **VALID** =
carried into this proposal or its deltas. **NOTED** = real, but a design-level
or operational constraint — recorded in `clarifications.md` or `design.md`.
**NOT APPLICABLE / SUPERSEDED** = the subject changed under the reshape.

### Council — Adversary Engineer

| # | Finding | Disposition |
|---|---|---|
| 1(a) | Refusal's input is authored inside the checked tree | **VALID** — §3(a); intake requirement "derived, never reported" |
| 1(b) | codexFactory's manifest declares only `domain_ontology`; the channel is unwired | **VALID, and FIXED since the review** — §3(c), landed at `dcfbd96` / `3de0519` |
| 1(c) | The floor's source of truth is an unseedable markdown record | **VALID — carried as Q9**, because closing it amends another change's ratified text |
| 2 | Nothing bounds a root grant; no tool reads any grant; register reviewed by its grantees | **VALID** — S1, S2, S4's human-only declaration; the no-reader rule adopted verbatim |
| 2 (exit-B limb) | A recorded grant supplies attribution no key established | **VALID** — exit B rejected in S3; carried as intake requirement text |
| 3 | The custody ceiling is a self-declared string; `act_unsupervised` is reachable in software | **VALID** — §2 rewritten; both suggested rules ADOPTED (refusal + attestation cap); the deleted sentence deleted; Q10 raised |
| 4 | Revocation is unsatisfiable against an issuance-bound stamp; composition revocation feeds the `--admin` loop | **VALID** — S5, all three limbs |
| 5 | Digest-disjointness measures byte identity and is anti-correlated with independence | **VALID — and decisive**; the narrowed floor is DECLINED (PART III) rather than repaired |

### Council — Systems Architect

| # | Finding | Disposition |
|---|---|---|
| 1 | No candidate-side input; both paths re-enter the checked tree; Q6's handles under-cover the machinery | **VALID** — §3(a) and §3(b); Q6b answered; additive-not-replacement stated |
| 2 | No checkpoint both outside the tree and permitted to enforce; exits A and B both fail | **VALID** — the third exit ADOPTED as S3; exit B rejected on the adversary's ground |
| 3 | Revocation-at-exercise unsatisfiable by either Q1 option; composition is an availability trap; distinct-holder has no store | **VALID** — Q1c stated as a design constraint; S5; the distinct-holder store limitation stated in §1 |
| 4 (first half) | The "already provides it" premise is not live | **VALID, and FIXED since the review** — §3(c) |
| 4 (second half) | "No new schema" will not hold — job envelope field, register shape | **VALID** — softened to "no new GRANT schema"; both named as declared successors |

### Council — Product Advocate

| # | Finding | Disposition |
|---|---|---|
| 1 | The Why sells a cure the Out-of-scope returns; no first bypass named | **VALID** — "The first bypass this ends: NONE, directly" written into ## Why; over-selling sentences deleted |
| 2 | Cold start unaddressed; composition revocation is an unattended tripwire | **VALID** — ## Cold start written; Q8 raised with the four exits as asked |
| 3 | The intake is designed entirely in open questions; no MVP | **VALID** — S4's MVP table is normative; register-and-reader-together is a ratification condition |
| 4 | "Confers nothing" guarantees the schema is never elected — couple it or cut it | **PARTIALLY DECLINED, with ground.** Q7's role question RESOLVED to `PA` as asked. The COUPLING is declined: it would tie election to digest-disjointness, which PART III declines. The section is kept, trimmed, and its non-ergonomic property recorded as an argument for election that earns nothing in governance terms |

### Alignment — Stack Architect (first circulation)

F1, F7 — **NOT APPLICABLE** to this change (no repository act); carried to any
electing project. F3, F4, F5, F6 — **VALID, relocated** into the
recommended-schema obligation list. F2 — **VALID, inverted**: the strongest
evidence against the first spine is supporting evidence for this one. F8, F9 —
**VALID**, both silence claims corrected in ## What this creates. F10, F11 —
**VALID**, the capability split now follows the ownership seam. F12 —
**VALID**, `authority_tier` carried throughout as REQUIRED and closed. F13 —
**VALID**, the wallet prerequisite and the custody cap are both stated, and now
costed in ## Cold start. F14 — **VALID**, `consent-instrument` dropped as a
model. F15 — **VALID**, `distinct_holder_constraint_refs` named, with its
store limitation stated. F16 — **VALID**, the conjunction restored. F17 —
**VALID, DISCHARGED**: the origin block is present and immutable. F18 —
**VALID, DISCHARGED**: deltas and `tasks.md` now exist and `--strict` is green.
F19 — **VALID**, `target_release: implemented`. F20 — **VALID**, a README
listing task. F21 — **VALID**, ranges corrected.

### Alignment — QA Lead (first circulation)

1.1, 1.2, 1.3 — **VALID**, citations corrected (the 13-of-14 activation-gate
figure is carried in ## Why). 2.1–2.5 — **VALID**, the liaison reconciliation
rewritten and the attribution/conferral axes separated. 3.1, 3.2 — **VALID**,
`consent-instrument` demoted to a named non-precedent. 4.1 — **VALID**, and its
subject is now DECLINED rather than repaired (PART III). 4.2 — **SUPERSEDED,
conditionally**: `distinct_holder_constraint_refs` is the observable the finding
asked for, but only once S3 lands the exercise store — stated in §1 rather than
claimed. 4.3 — **VALID**, S4 fixes path, reader and revocation check. 4.4 —
**SUPERSEDED** for the spine; re-arms for an electing project. 5.1, 5.2 —
**SUPERSEDED at the root**: there is no repository predicate and no AI-reviewer
clause; the floor is untouched and the narrowed reading is declined. 5.3, 5.4,
5.5 — **VALID, relocated** to the recommended-schema obligation list. 5.6 —
**VALID, DISCHARGED** (origin present). 5.7 — **VALID, DISCHARGED** (specs and
tasks present). 5.8 — **VALID**, the framing inverted. 6.1 — **VALID**, role
definitions land in `roles-authority-model`. 6.2 — **SUPERSEDED**, no floor
re-expression exists to correct.

## Out of scope, deliberately

- **The narrowed floor reading.** Not deferred, not posed — DECLINED (PART III).
  Defining a real independence test is not named as a successor because it is not
  currently definable.
- Deciding whether any project adopts the three-repository schema. That is a
  human's per-project `PA` election; a bench cannot make it on a project's behalf
  without turning a recommendation back into the requirement that was demoted.
- Amending the constitutional floor, in any direction.
- Performing S1–S5. Each is a named successor with its own code surface.
- Procuring or building a digest-disjoint reviewer.
- Any change to the council-verdict transport, the merge-master token-minting
  flow, or the three-identity separation. All are reused unchanged.
- Extending, narrowing, or re-tiering what councils may autonomously clear.
- Retiring `--admin` usage on any repository. ## Why states plainly that this
  change ends no bypass directly.
- Making wallets a prerequisite for anything other than holding review authority.
  `openxwallet/spec.md:155-163` keeps them optional for domains and this change
  does not disturb that.
