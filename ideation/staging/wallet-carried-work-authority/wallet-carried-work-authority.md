# Staged: authority names the work, not the repository that holds it

Status: staged
Kind: capability-proposal
Summary: `add-wallet-carried-review-authority` ratified that review authority is
held as an openxwallet grant and by nothing else, and demoted the
SPEC/CODE/ASSEMBLY three-repository schema to a per-project human election that
"changes no gate, no floor, no grant, and no clearance eligibility". That
demotion is true in the prose and false in the machinery: `scope.objects` is used
at REPOSITORY granularity (the one live grant scopes `review` to
`opensoft/openxFactory`), there is no path or branch narrowing, and only `review`
is an act with a reader — so the only way to seat spec authority and code
authority separately over one project is to put spec and code in different
repositories, which makes the confers-nothing schema silently LOAD-BEARING. This
topic removes the coupling from the authority side: path-prefix objects below
repository granularity, `author` and `merge` given the kind of named reader
`review` already has, and an openxFactory consuming capability —
`work-authority-intake`, sibling of `review-authority-intake` — checking author
grants at pull-request open and merge grants at the merge gate. Brett Heap ruled
this on 2026-09-02 over the alternative of making the three-repo schema the
default wherever the two authorities diverge, because that alternative quietly
re-imports layout as an authority carrier. Co-residence is untouched; the
three-repo schema stays human-elected and becomes genuinely optional.
Topics: openxwallet, grant-scope, path-scoped-objects, author-act, merge-act,
work-authority-intake, review-authority-intake, signed-execution-chain,
neutral-product-pin, distinct-holder
Repository context: SPLIT ACROSS TWO HOMES, which is the sequencing problem.
`opensoft/openXwallet` owns the grant schema, custody registry, distinct-holder
constraint schema and `scripts/validate-openxwallet.py`; the object grammar and
act readers are ITS deltas and cannot be authored here. `openxFactory` owns the
seam — `governance/review-authority/`, the consuming capability and its required
check, and `contracts/openxwallet-pin.yaml`, which consumes openXwallet at a
commit plus eight per-file `sha256`s (label `contract_bundle_tag: wallet-v1.3`)
under `neutral-product-pin`.
Staging ID: openxFactory:staging:wallet-carried-work-authority
Captured: 2026-09-02
Source: Brett Heap's ruling of 2026-09-02, in session with Claude, recorded
verbatim under "The ruling" below. Origin context is the ratified
`add-wallet-carried-review-authority` (its "recommended project schema" section
and design D1) plus the live grant and register under
`governance/review-authority/`.
Target capabilities: MODIFIED `openxwallet` (openXwallet-owned — `scope.objects`
gains a path-prefix form below repository granularity with prefix containment as
the attenuation test; `author` and `merge` gain named readers and constraints the
way `review` has them); ADDED `work-authority-intake` (openxFactory-owned — a
required check reading author grants at PR open and merge grants at the merge
gate, exercise recorded); MODIFIED `neutral-product-pin` realization (the digest
pin bumps to the release carrying the extension). NEITHER `openxwallet` NOR
`work-authority-intake` IS FENCED as an `xspec:candidate` target below, on
`openxwallet-neutral-home`'s recorded precedent: `openxwallet` no longer resolves
here (it left with `split-openxwallet-repo`) and `work-authority-intake` does not
exist yet, so fencing either emits tag-hygiene unresolved-target findings. The
fences target the three capabilities that resolve and that this topic touches.

## Last proposal attempt (round-trip provenance)

<!-- Stays "none yet" until this topic first reaches proposal. On DEMOTE,
     replace every field below with the ACTUAL values from the demoted
     change — never re-blank them; that is the whole point of this slot. -->

Change ID: none yet
Raised: n/a
Status at demote: n/a
Demoted: n/a
Demote reason: n/a

## The ruling

Brett Heap, convener, 2026-09-02, in session with Claude. Two coherent options
were put to him, stated as they were put:

1. Keep grants repo-granular and make the three-repo schema the default wherever
   spec and code authority diverge (requires revisiting co-residence).
2. Keep co-residence and extend the grant schema with path-scoped objects plus
   `author` and `merge` acts, then let the staged `signed-execution-chain` topic
   carry the enrollment-to-merge gate.

**Brett chose option 2 and said "stage it as a topic".** Reasoning recorded by
the session: option 2 matches the ratified doctrine that layout confers nothing;
option 1 quietly re-imports layout as an authority carrier.

## Pre-document idea notes

Unstructured, kept because the reasoning is younger than the vocabulary.

- The defect is not that the three-repository schema is wrong. It is that the
  schema was demoted in PROSE and promoted in MECHANISM on the same day. Take
  "electing the schema changes no grant" at its word, try to seat a spec owner
  and a code owner separately inside one repository, and no grant can say it. —
  Added-by: Claude Opus 5 (session) · 2026-09-02
- Narrowest statement of the gap: `scope.objects` items are `identifier`s under
  `^[A-Za-z0-9][A-Za-z0-9._:/-]*$`, which ALREADY admits
  `opensoft/openxFactory:openspec/` — slash and colon are both legal. No new
  regex is needed. What changes is attenuation SEMANTICS: today a derived
  grant's objects must be a set subset of the parent's, and prefix containment
  is a different comparison. "Extend the grant schema" sounds like a rewrite and
  is not. — Added-by: Claude Opus 5 (session) · 2026-09-02
- There is no closed act enumeration anywhere in openXwallet. `scope.acts` is a
  list of free identifiers; the packaged examples use `create_transaction` /
  `post_transaction`. One token has a reader — `REVIEW_ACT_TOKEN = "review"` in
  `scripts/validate-openxwallet.py`, where membership in `scope.acts` is what
  makes a grant REVIEW-class. Nothing forbids writing `author` in a grant today;
  it simply means nothing. The delta is a READER and its constraints, not an
  enum entry. — Added-by: Claude Opus 5 (session) · 2026-09-02
- The `approve` act is a real hole, found while checking Q2.
  `review-authority-intake` carries a ratified requirement titled "No holder is
  issued both the review act and the approval act over one object" — yet no
  `approve` token exists in openXwallet's contracts, examples or validator:
  approval is a POSTURE (`approval_posture`, keys drawn from the neutral job
  envelope's `approval_policy`), not an act. A ratified requirement names
  something the substrate does not have. — Added-by: Claude Opus 5 (session) ·
  2026-09-02
- The distinct-holder constraint needs NO schema change to express
  author-versus-review: `xfactory_wallet_distinct_holder_constraint` already
  takes `object_kind`, `acts.prior`, `acts.subsequent`, `comparison_basis:
  recorded_holder_of_prior_act` and an optional `distinctness_floor`. A
  constraint naming `{prior: author, subsequent: review}` is a new INSTANCE, not
  a new shape. What is genuinely new is that the object is a path scope rather
  than a repository — which is Q6. — Added-by: Claude Opus 5 (session) ·
  2026-09-02
- The uncomfortable version: if path-scoped objects work, the three-repository
  schema loses most of its argument. That is fine and not the point. Its
  argument was ergonomic — authority "visible from the repository list instead of
  inferable from a register" — and ergonomics survive a register that can answer
  the question. What it must not be is the only way to ASK. — Added-by: Claude
  Opus 5 (session) · 2026-09-02

## Claims

<!-- Settled context the open questions below should NOT reopen. -->

1. **Layout confers nothing.** Repository ownership, a CODEOWNERS entry, a role
   name or a seat assignment confer no authority — ratified in
   `review-authority-intake` requirement 1, asserted here rather than
   re-decided. FALSIFIABLE BY: an admitted act whose authority basis resolves to
   a repository or path label and to no grant.
2. **Path-scoped objects are monotonically narrower than a repo-scoped parent by
   PREFIX CONTAINMENT.** FALSIFIABLE BY: a prefix pair where the child admits a
   path the parent does not — which is why globs and negation are unacceptable
   (Q1) rather than merely verbose.
3. **Author and review over one object cannot be one holder**, extended by
   DECLARATION — a constraint instance naming `{prior: author, subsequent:
   review}` — with the ratified refusal of one holder holding both review and
   approval over one object as precedent, not as a competing rule. FALSIFIABLE
   BY: an exercise record where the author act's recorded holder equals the
   review holder on the same object and the evaluation is recorded satisfied.
4. **A worker never holds an author grant as key access.** Omnigent workers
   carry `execute_final_action: false` and `access_secrets: false` as
   schema-level `const` in `contracts/omnigent/omnigent-domain-overlay.schema.yaml`,
   with the negative fixture `overlay-semantic-carries-grant.yaml` rejecting an
   overlay smuggling `grant: repo_admin`. The author act is exercised under TIER
   1 human-held authority and evidenced by a TIER 2 harness-issued ephemeral
   attestation, exactly as `signed-execution-chain` ruled its tier split.
   FALSIFIABLE BY: any design where a runner holds the key that signs an author
   exercise.
5. **Branch protection and CODEOWNERS remain external enforcement and are
   layout-bound, so they cannot be the carrier.** FALSIFIABLE BY: a proposal
   storing the authority fact in a CODEOWNERS file or ruleset and treating the
   grant as its projection.
6. **The three-repository schema stays human-elected and becomes genuinely
   optional** — its ratified demotion becomes mechanically true once the
   register can answer the spec-versus-code question inside one repository.
   FALSIFIABLE BY: any gate, floor, grant or clearance rule that reads a
   project's repository count after this lands.
7. **The act vocabulary is open; the reader is what confers.** FALSIFIABLE BY:
   finding a closed act enumeration in the openXwallet contracts.

## Why

<!-- xspec:candidate target=roles-authority-model -->
`add-wallet-carried-review-authority` ratified two things on one day that have
not been made consistent. Its design D1 rejected the three-repository topology as
the spine of review authority — it "would also have had to overturn
`shared-contract-ownership:113-137` (spec/code co-residence) and
`adopt-neutral-tooling-home` (tooling moved INTO the publisher)" — and its
proposal demoted the schema to a per-project human election that "changes no
gate, no floor, no grant, and no clearance eligibility". Doctrine settled:
authority is a grant, spec authority and code authority are two grant SCOPES,
repository ownership confers nothing. But the substrate cannot express the
distinction the doctrine describes. `scope.objects` is an optional list of opaque
identifiers used at repository granularity — the live `grant-mrc-0001` scopes
`review` to `opensoft/openxFactory` — with no path narrowing, no branch
narrowing, and no act beyond `review` carrying a reader. The consequence is that
the only mechanism available for seating a spec owner and a code owner
separately is to put spec and code in different repositories. The schema whose
ratified text says it confers nothing is today the sole carrier of a distinction
the doctrine calls essential, and a project that declines it cannot express that
distinction at all. Either the doctrine is wrong or the substrate is incomplete.
The substrate is incomplete.
<!-- /xspec:candidate -->

## What changes

<!-- xspec:candidate target=review-authority-intake -->
Three deltas across two repositories, in a fixed order. FIRST, in openXwallet:
`scope.objects` gains a PATH-PREFIX form below repository granularity — an
ordered list of literal path prefixes, no globs and no negation — and the
attenuation rule in `scripts/validate-openxwallet.py` (rule (f)) gains prefix
containment beside its existing set-subset test, so a child scoped to
`opensoft/openxFactory:openspec/` is accepted as narrower than a parent scoped to
`opensoft/openxFactory` while a sibling prefix outside the parent's cover is
refused; the identifier pattern already admits the form, so this is a semantic
delta rather than a grammar one. In the same change `author` and `merge` become
acts with named readers and declared constraints the way `review` did:
membership in `scope.acts` makes a grant AUTHOR-class or MERGE-class, an
author-class grant is bound to the tier ladder and to a distinct-holder
constraint against `review` on the same object, and a merge-class grant carries
the approval posture the merge gate requires. SECOND, in openxFactory: a
consuming capability, working name `work-authority-intake`, sibling of
`review-authority-intake` and built on its shape — a register plus a READER
running as a REQUIRED check, because that capability's own ratified requirement
says a grant with no reader in a required check confers nothing. The reader
resolves author grants when a pull request OPENS and merge grants at the MERGE
GATE, refuses fail-closed on an unreadable register, re-checks revocation at use
against a declared staleness bound, and RECORDS THE EXERCISE the way review
exercise is recorded at verdict conformance. THIRD, the openxFactory digest pin
bumps to the openXwallet release carrying the extension, which is what makes the
extension readable here at all.
<!-- /xspec:candidate -->

## Impact

<!-- xspec:candidate target=neutral-product-pin -->
- Affected specs: `openxwallet` (MODIFIED — object grammar and act readers;
  openXwallet-owned, not authorable here); `work-authority-intake` (ADDED —
  openxFactory); `roles-authority-model` (MODIFIED — spec authority and code
  authority named as grant scopes rather than repository roles);
  `neutral-product-pin` (realization — the pin bumps by commit and per-file
  digest, tag-only refused).
- Affected code: `openXwallet/contracts/openxwallet/openxwallet-grant.schema.yaml`
  and `openXwallet/scripts/validate-openxwallet.py` (attenuation rule (f), an
  act-class reader, fixtures with negatives for a widening prefix, a glob and a
  negation); `openxFactory/contracts/openxwallet-pin.yaml`;
  `openxFactory/governance/`; `openxFactory/.github/workflows/` (a required check
  alongside `wallet-validation`).
- External enforcement unchanged in kind: branch protection and CODEOWNERS stay
  the forge-side executor the reader configures, and making a new check REQUIRED
  remains an operator act the capability must declare in the present tense.
- Blast radius NOT taken: no change to the custody ladder, none to the
  distinct-holder constraint SCHEMA, no new authority vocabulary, no second
  identity substrate.
<!-- /xspec:candidate -->

## What this topic explicitly does NOT change

- `shared-contract-ownership` co-residence STAYS — the publisher keeps its
  contract kernel and the validator that reads it in one repository, and
  `adopt-neutral-tooling-home` is untouched. Option 1 would have reopened both;
  the ruling declined it.
- The SPEC / CODE / ASSEMBLY schema STAYS human-elected, its ratified demotion
  preserved word for word. Electing it is simply no longer the only way to make
  spec-versus-code authority legible: the schema is DECOUPLED from authority
  legibility, not deprecated. Its scaffolding task (predecessor §8.4, still
  unchecked) is neither cancelled by this topic nor a dependency of it.
- The review act, its register, its reader and its ratified requirements stay as
  they are. This topic adds siblings and amends none of them.

## Conflicts

<!-- Honest tensions this topic has NOT resolved. -->

- **Three "N-repo" governance ideas coexist unreconciled, and this topic
  reconciles only what it touches.** (a) canonical-plus-install repositories
  under `repo-boundary-governance`, the oldest; (b) neutral `open*` product,
  then `<Domainx><Product>` descendant, then DomainxFactory — 2026-08-26 onward
  as `domain-descendant-boundary` + `neutral-product-pin`; (c)
  SPEC/CODE/ASSEMBLY, optional, 2026-08-22/23. Not contradictory, but not
  composed either, and nothing says which applies when. This topic makes (c)
  genuinely optional by removing its hidden coupling to authority legibility; it
  does NOT reconcile (a) with (b). — Added-by: Claude Opus 5 (session) ·
  2026-09-02
- **The predecessor's substrate is half-built and this topic depends on the
  unbuilt halves.** In `add-wallet-carried-review-authority/tasks.md`, S3
  (exercise recording at verdict conformance) has 6.1 merged — the
  hermes-install successor `add-wallet-exercise-verdict-conformance`, ratified at
  `401da4f`, 2026-08-27 — and 6.2 through 6.8 unchecked, including where exercise
  records are STORED (6.4, undecided). S5 (revocation lifecycle) is four pull
  requests, none merged, with 7.1–7.4 and 7.6–7.7 unchecked. Exercise recording
  and revocation-at-use are the difference between a grant and a label, and this
  topic must duplicate neither. — Added-by: Claude Opus 5 (session) ·
  2026-09-02
- **`register.yaml` says in its own header that it is NOT a revocation
  surface** — every distribution path is digest-pinned and lagging, so the file
  is an issuance-time snapshot carrying `revocation_staleness_bound: P7D`, and
  the conforming home for revocation is a live lookup on the Hermes runtime. A
  merge gate is a worse place than a council convening to honour a seven-day-stale
  revocation, because merge is irreversible where a parked candidate is not.
  Inherited, not solved. — Added-by: Claude Opus 5 (session) · 2026-09-02
- **A ratified requirement names an act the substrate does not define** — see
  the `approve` note above. Satisfiable today only by reading "approval act" as
  "approval posture", which is a different kind of thing. Q2 is where it bites.
  — Added-by: Claude Opus 5 (session) · 2026-09-02
- **`neutral-product-pin` and `domain-descendant-boundary` both still carry
  `Purpose: TBD - created by archiving change split-openxwallet-repo. Update
  Purpose after archive.`** The two specs governing how this topic's openXwallet
  delta reaches openxFactory have never had their purpose written. Not this
  topic's to fix, and a real drag on anyone sequencing across the seam. —
  Added-by: Claude Opus 5 (session) · 2026-09-02
- **Composition with `signed-execution-chain` is asserted, not demonstrated.**
  Its link 6 is a signed PR-OPEN decision and its link 8 a chain-validating MERGE
  GATE; this topic puts an author check at PR open and a merge check at the merge
  gate. Same two moments — and two independent readers at one moment is precisely
  the "two records of one decision" defect the family keeps finding. Until a
  change draws that seam (Q5, and Q3's sequencing) it is a live conflict rather
  than a clean composition. — Added-by: Claude Opus 5 (session) · 2026-09-02

## Open questions

### Q1. What is the object grammar for a path-scoped grant?

Context: `scope.objects` items are `identifier`s under
`^[A-Za-z0-9][A-Za-z0-9._:/-]*$`, which already admits
`opensoft/openxFactory:openspec/`. Attenuation compares objects as a SET and
requires subset; a path narrowing is not a subset relation. Candidates are
literal prefixes, globs (the CODEOWNERS idiom), and prefixes with negation.
Recommended answer: An ORDERED LIST OF LITERAL PATH PREFIXES — no globs, no
negation. A prefix is `<repository>:<posix path prefix>`; a bare repository
identifier keeps its current meaning as the widest prefix. Attenuation is PREFIX
CONTAINMENT: every child prefix must be covered by some parent prefix, with the
set-subset test retained for objects carrying no path part.
Explanation: Claim 2 is provable only for containment. A glob's cover is not
decidable by inspection — `openspec/**/spec.md` versus `**/openspec/*` have no
readable containment relation — and a validator that must EXECUTE patterns to
compare authority has made attenuation a computation rather than a reading.
Negation is worse: `A but not A/b` is not narrower than `A` under any containment
test, it is a different set, and monotonic narrowing stops holding. Ordering is
for deterministic diagnostics, not conflict resolution — without negation there
are no conflicts. The cost is honest: "everything except the vendored tree" needs
several prefixes instead of one negation, and that verbosity is the price of a
rule a human can check by eye.
Disposition status: open
Added-by: Claude Opus 5 (session) · 2026-09-02

### Q2. Is `merge` a distinct act, or `approve` at a higher custody tier?

Context: No `approve` act token exists in openXwallet. Approval is
`approval_posture`, whose keys come from the neutral job envelope's
`approval_policy`, validated against it at run time and bound to
`authority_tier` by validator rules (f) and (g). Meanwhile
`review-authority-intake` carries a ratified requirement about "the approval
act", and forbids a review-authority grant from ever naming `act_unsupervised`.
Recommended answer: A DISTINCT ACT — `merge` is its own token with its own
reader, not a tier promotion of an approval that does not exist as an act.
Explanation: The tier ladder answers "how much does a signature evidence"
(`attest`, `request`, `act`, `act_unsupervised`), capped by the audience wallet's
custody model. It does not answer "which act". Making merge a tier forces the
ladder to double as an act vocabulary — the parallel-authority-vocabulary failure
the grant schema declares a validation error — and is unexpressible anyway,
because the distinct-holder constraint compares `acts.prior` to
`acts.subsequent` and an act that is really a tier can be named as neither.
Merge is also the act with an irreversible external effect, so it is the one that
must carry `hermes_approval_required_before_apply: true` as a POSTURE — a
property of a grant FOR an act, which presupposes the act exists. The honest
consequence: the corpus's approval-act gap gets sharper rather than smaller, and
a later change may need to define `approve` as an act too.
Disposition status: open
Added-by: Claude Opus 5 (session) · 2026-09-02

### Q3. What is the landing shape across the two repositories?

Context: The schema and validator are openXwallet's; the readers, register and
required check are openxFactory's; openxFactory consumes openXwallet only through
`contracts/openxwallet-pin.yaml` at a commit plus per-file digests, tag-only
refused. One change cannot author deltas into both spec corpora.
Recommended answer: TWO SEQUENCED OPENSPEC CHANGES. First
`extend-openxwallet-object-scope` in openXwallet — object grammar, attenuation
rule, `author` and `merge` readers, fixtures including negatives, and a contract
release. Then `add-wallet-carried-work-authority` in openxFactory — the
`work-authority-intake` capability, its register, reader and required check, plus
the digest-pin bump to the release the first change cut, carried as its own first
task. Neither ticks the other's boxes; the second declares the first a
precondition.
Explanation: This is the shape `split-openxwallet-repo` established and
`neutral-product-pin` ratified — the publisher cuts a release, the consumer pins
it by commit and digest, and the consumer's change moves the pin. One combined
change would require openxFactory to author a delta into openXwallet's spec
corpus, refused on the same grounds `hermes-domain-overlay` refuses it for
refusal vocabulary. Doing the openxFactory side first gives it a reader for a
grammar its pinned validator cannot parse: a grant with no reader confers
nothing, and a reader with no grammar refuses everything.
Disposition status: open
Added-by: Claude Opus 5 (session) · 2026-09-02

### Q4. How does the merge-act reader bind to GitHub branch protection?

Context: Branch protection and CODEOWNERS are the forge's own enforcement. A
required status check is the only thing branch protection understands, and making
a check REQUIRED is an operator act — as the predecessor's §2.5 records for
`wallet-validation`. Claim 5 says these stay external enforcement.
Recommended answer: The reader binds as ONE REQUIRED STATUS CHECK reporting its
verdict, and branch protection is CONFIGURED FROM the register rather than
consulted as a source of authority. Where a CODEOWNERS file or ruleset must exist
for forge-side reasons it is a PROJECTION of the register — regenerated,
drift-checked, never hand-edited, never read back as the authority fact.
Explanation: The refusal has to happen where merge happens, and on GitHub that
is a required check; a bot comment or a post-merge audit is a record, not a
permission. Making the ruleset a projection keeps claim 1 true while accepting
that the forge needs its own copy: the register is the source, the ruleset a
rendering, the drift check what keeps the rendering honest. This deliberately
does NOT have the reader edit branch protection at run time, which would put
repository-admin credentials in the checking lane — precisely the authority the
omnigent constitutional booleans exist to deny.
Disposition status: open
Added-by: Claude Opus 5 (session) · 2026-09-02

### Q5. Is an author grant checked per commit, or at PR-open plus the merge gate?

Context: A pull request holds many commits, authored over time, possibly by
several holders and by runners acting under a holder's authority. Grants expire
and are revoked; the register is an issuance-time snapshot with a declared
staleness bound. `signed-execution-chain` already attests per runner and per task
inside a branch.
Recommended answer: AT PR-OPEN AND AT THE MERGE GATE, not per commit.
Intra-branch commits are covered by the chain's tier-2 attestations, which
already say what ran and under whose declared authority.
Explanation: Per-commit checking sounds stricter and is weaker where it matters.
It multiplies revocation-window exposure by the commit count without narrowing it
— a grant revoked mid-branch still passed every earlier commit — and it resolves
authority against a register snapshot on every push, cost with no new refusal.
The two recommended moments are the two DECISIONS: opening a pull request is one
(`signed-execution-chain` link 6 signs it as such) and merging is the
irreversible one. Checking authority at a decision and evidencing execution
between decisions is the division of labour that topic's tier model already
draws, and reusing it avoids a third opinion about what a commit means.
Disposition status: open
Added-by: Claude Opus 5 (session) · 2026-09-02

### Q6. Does ASSEMBLY need its own object kind, or is it another path prefix?

Context: ASSEMBLY is the code that assembles a review team, shared across the
family. Under co-residence it is not a repository at all — it is `scripts/` and
workflow content inside the publisher, already covered by codexFactory's
`"scripts/**"` floor entry, its CODEOWNERS line and its import-root test. The
distinct-holder constraint takes an `object_kind`, so this topic must say what
kind a path scope is.
Recommended answer: ANOTHER PATH PREFIX, with no ASSEMBLY-specific object kind.
One new object kind is introduced for the constraint's benefit — a path scope —
and ASSEMBLY content is named by prefixes within it.
Explanation: A separate object kind would have to answer "what makes this content
ASSEMBLY", and the only available answer is where it sits — reintroducing layout
as the authority carrier by a side door. A prefix says the same thing without the
claim: whoever holds `author` over `<repo>:scripts/` holds it over the assembly
code, and if that content moves the prefix moves with it in a reviewable edit.
The genuine ASSEMBLY-specific concern — that code being higher-stakes than
ordinary code — is already carried by the floor, a REFUSAL surface rather than an
authority one, which this topic does not retire.
Disposition status: open
Added-by: Claude Opus 5 (session) · 2026-09-02

### Q7. Its own register, or a second table in the review register?

Context: `governance/review-authority/register.yaml` is deliberately KINDLESS —
no contract schema exists for it, its shape IS its reader — and it is a
PERMANENTLY HUMAN-ONLY surface entered by name as a never-clearable floor member.
It carries `revocation_staleness_bound: P7D` beside the rows it bounds.
Recommended answer: ITS OWN REGISTER beside the review one, sharing the reader
implementation and the human-only floor treatment but not the file.
Explanation: The bound is declared beside the rows it bounds because how long a
revocation may go unhonoured is a governance decision per surface, and merge needs
a tighter answer than council convening does — one file cannot carry two bounds
without a per-row override the current shape does not have. Sharing the FILE
would also silently widen what the never-clearable floor entry covers, changing a
ratified floor member's blast radius as a side effect. Sharing the READER is the
part worth keeping: one parser, one refusal vocabulary, one drift check.
Disposition status: open
Added-by: Claude Opus 5 (session) · 2026-09-02

## Exit path

Two OpenSpec changes in the order Q3 recommends, and a precondition about
neither of them.

**What must be true before the FIRST change is proposed.** The predecessor's
exercise recording and revocation lifecycle must have LANDED, or this topic's
first change must be explicitly LOCKSTEPPED to them with the dependency declared
in its own tasks: tasks 6.2–6.8, whose 6.4 has still not decided where exercise
records are stored, and tasks 7.1–7.4 and 7.6–7.7, whose four pull requests are
open and unmerged. An author or merge grant whose exercise is unrecorded and
whose revocation is not re-checked at use is a label, and this topic exists to
stop labels conferring authority. The precondition is a state of that work, not a
citation of it.

**Change one, in openXwallet: `extend-openxwallet-object-scope`.** Object grammar
below repository granularity as ordered literal path prefixes; prefix containment
added to the attenuation rule beside set subset; `author` and `merge` as acts
with named readers; a distinct-holder constraint instance for author-versus-review
over the path-scope object kind; negative fixtures for a widening prefix, a glob
and a negation; a contract release with manifest entry, changelog entry,
annotated tag and per-file digests.

**Change two, in openxFactory: `add-wallet-carried-work-authority`.** The
`work-authority-intake` capability and its register; the reader resolving author
grants at pull-request open and merge grants at the merge gate; the required
check; the exercise record; the drift-checked projection into branch protection;
and, as its first task, the digest-pin bump to the release change one cut.

**The proposal gate for this topic** is every open question above carrying a
disposition other than `open`, plus the precondition state above being true or
lockstepped. Q1, Q2 and Q6 gate change one's contract text; Q3 gates the shape of
both; Q4, Q5 and Q7 gate change two only, so change one is not held by them.
