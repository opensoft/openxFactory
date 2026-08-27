# Design: adopt-council-cleared-merge-gate

Status: draft
Subject: the POLICY half of council-cleared merging for `opensoft/openxFactory`.
This document records the design decisions, the parity analysis against the
capabilities this change touches, and the alternatives rejected with reasons.

## The shape of the problem

Three constraints fix the design almost completely, and they were discovered in
this order:

1. **Ratified doctrine prescribes the mechanism.** `add-substantive-review-lane`'s
   *Ruleset interaction shape for the substantive review lane* requires the
   approval to be a real `APPROVE` review by the merge-master App, forbids the
   council-verdict check-run from ever being a ruleset satisfier, and forbids
   removing human review as an alternate path.
2. **The approval rule is not openxFactory's to edit.** It lives in org ruleset
   `18962101`, targeting seven repositories. openxFactory has no
   repository-level ruleset at all.
3. **A GitHub ruleset cannot branch on pull-request class.** Required checks and
   approval counts apply to every pull request on the branch.

Constraint 3 is what makes the sketched design ("required checks in place of the
approval rule") not merely disfavoured but unimplementable as described: per-class
gating cannot be expressed at the ruleset layer, so a check-satisfier design
would have had to move the enforcement of human review out of GitHub and into
codexFactory's Python. Constraints 1 and 2 then agree with 3 from different
directions. **The design that survives all three is the one that changes nothing
about the gate's composition and only changes who may cast the review.**

## Decisions

### D1 — The gate composition is unchanged; only the approver set moves

The required-review rule stays at one approving review. `wallet-validation` and
`pytest-suite` stay required. No new required check is added. For a candidate in
an enrolled clearable class, the approving review is cast by the merge-master App
on a unanimous council verdict; for everything else a human casts it, exactly as
today.

The consequence worth stating: **this design has no rollback surface in the
ruleset**, which is its principal safety property. Rolling back is returning one
YAML field to `advisory`.

### D2 — One ruleset edit, and it is a hardening

`dismiss_stale_reviews_on_push: true` currently reaches openxFactory only by
inheritance from `18834180`, the `~ALL`-repositories code-owner ruleset, and both
`pull_request` rules carry `require_last_push_approval: false`. An autonomous
approval's most obvious attack — clear a prose diff, then push code onto the
approved head — is therefore closed today by a ruleset this change has no
standing to defend.

Ruleset `21538893` targets `openxFactory` alone. Writing
`dismiss_stale_reviews_on_push: true` and `require_last_push_approval: true`
there makes the property locally owned at zero blast radius. It is the only
ruleset edit this change proposes, it strengthens the gate, and it should survive
a rollback rather than be undone by one.

### D3 — ONE candidate class (revised by the council from two)

`openxfactory-governance-prose`: `docs/**/*.md`, `ideation/**/*.md`, `README.md`,
plus a depth-independent PR-time refusal of the twelve `PROTECTED_ROOT_FILES`
basenames — because that floor is applied **root-exact** (`:1045`), so
`docs/**/*.md` would otherwise admit `docs/AGENTS.md`.

A prior revision of this design carried a second class,
`openxfactory-derived-health-artifact`, over `health/derive-possibles/**` and
`health/neutrality-drift/**`. **All three council seats independently required
its removal**, and the systems-architect seat blocked on it. Three grounds, any
one sufficient:

1. **No traffic.** `health/neutrality-drift/` has produced zero pull requests
   ever; `health/derive-possibles/` two, the last five weeks ago. Both lanes are
   documented dormant.
2. **Its only historical PR shape was unclearable anyway** — both carried
   `ideation/cross-reference.yaml`, a `.yaml` outside `DERIVED_ARTIFACT_ROOTS`.
3. **Its allowlist re-admitted a protected comparator.**
   `health/neutrality-drift/**` admits `.../baseline/codexFactory.yaml`, the
   tree's only file and the immutable comparator `load_baseline` reads back.
   `PROTECTED_PATH_SEGMENTS` guards **patterns**, not changed paths, so the
   broader glob validates. That makes it a **floor narrowing presented as a
   boundary**, which `regular-pr-council-clearance/spec.md:55` forbids outright.

The consequence for the canary is decisive and is why this was blocking rather
than cosmetic: a canary requiring ≥3 observations in a class with no producer
**can never complete**, so G7's flip would have been structurally unreachable and
the packet would have ratified a boundary it made permanently unexercisable. The
canary is now prose-only at N=3, and **each class carries its own canary in the
change that enrolls it** — which preserves class-boundary-error detection without
conditioning this class on traffic that does not exist. The derived class is
deferred to a successor, to be raised when a wired producer exists and the
`add-classification-intent-and-substantive-classes` Phase-2 hold is lifted.

The class enrolls at `advisory`. That is not caution:
`_validate_defined_not_wired` refuses `clearable` for a class whose target
repository is unwired, because the class-floor derivation reads a base-branch
allowlist that does not yet exist. The flip is G7, a separate ratified act.

### D3b — A succession claim withdrawn, and why it is recorded

A prior revision said codexFactory's
`openxfactory-derived-health-artifact-advisory-v1` was "PREPARED AND PARKED
2026-08-25" with `state: defined_not_wired`. **That artifact does not exist in
rules-as-code**: it appears only as prose in the **active, unarchived**
`add-classification-intent-and-substantive-classes`, at tasks 7.2/7.3, **both
unchecked**, where it is merely proposed "for the Council to accept or amend" —
behind a task 7.1 that holds Phase 2 outright.

So this design attributed a shipped rules-as-code state to an unchecked task and
claimed succession from an artifact never authored. **That is precisely the LS-A3
error this change exists to prevent, committed by this change.** It is recorded
rather than quietly deleted, because a withdrawn claim that leaves no trace
teaches nobody — and because it is the second time in this packet's history that
deriving from prose rather than from code produced a false claim (see D4).

### D4 — The boundary is derived from rules-as-code, not from prose

The first draft of this packet derived its boundary from ratified prose and did
not check it against the implemented enforcer. The code is stricter and more
specific, and it refused three of the draft's clearable entries outright —
`openspec/changes/**` sits in the PR-time gate-integrity floor and `openspec/` in
the class floor; `CLAUDE.md` and `AGENTS.md` are protected root files;
`governance/` is wholly protected.

The corrected derivation runs the other way: start from the enforcer's constants,
assert only what they do not cover. The method is recorded because the failure it
caught is this change's own subject matter — **a packet written to prevent "a
described control treated as existing" had described a boundary the enforcer
would have refused to implement.**

The honest consequence is a narrower change than the direction envisaged.
openxFactory's dominant traffic is `openspec/changes/**`, which is not clearable
and does not become clearable here. **This change's own diff would not qualify
under its own boundary.** That is the correct outcome and it is stated in the
proposal rather than engineered around.

### D4b — The mixed-diff mechanism was misstated

A prior revision asserted "a mixed diff takes the most restrictive class of any
path it touches", presenting it as existing `docs_only_path_overflow` discipline.
There is **no cross-candidate arbitration**: `_find_surface` (`envelope.py:510`)
selects on `target_repos` and **head ref only** — paths are never consulted — and
it is **first-match-wins**. The real semantics are that a mixed diff parks on the
selected candidate's `path_allowlist` overflow. The safety conclusion survives
(both are fail-closed); the mechanism was wrong. With one class the question does
not arise, but any future second class must prove its head-ref matcher **disjoint**
from this one's and declare candidate order, or it is dead code.

### D5 — No new required check (alternative rejected)

Making `merge-master-approval` a required status check was considered as additive
hardening and rejected on three surviving grounds: it buys no safety (the floor
is evaluated inside the approver, so a broken lane produces no verdict and
therefore no approval — already fail-closed); it is a repo-wide wedge (R1
deliberately fails red on missing credentials, which is safe only while nothing
requires the check); and a required context named for a job id is weakly bound to
the workflow that should own it.

A fourth ground was withdrawn under review. The self-reference deadlock is real —
the enforcer's envelope requires every required check to pass, so its own
required check would sit inside the envelope it gates — but the house already
solved it with `check_exclusions: [merge-master-approval]`, which is why the job
id is load-bearing. **The hazard is therefore an invariant openxFactory's own
envelope must carry, not a bar.** An envelope omitting it would deadlock
silently.

If the hardening is wanted anyway, the coherent form is a separately named check
(`review-lane-floor`) that is not the approver. Recorded as Q3.

### D6 — Floors go in the carriers that can hold them

`openxfactory-review-authority-floor.yaml` is `kind: repository_gate_floor`;
`repository_floor.py` refuses wildcards outright and matches by exact set
membership. It can hold exact chokepoint FILES and nothing else. So the floor
work splits three ways: a glob floor belongs in an `openxfactory-*-clearance.yaml`
clearance rule (the carrier `codexfactory-routine-code-clearance.yaml` already
demonstrates); exact-file additions belong in the `repository_gate_floor`; and
the repo-independent class floor already refuses `contracts/`, `.github/`,
`scripts/`, `tests/`, `governance/`, `openspec/` and `schemas/` for every
repository, so most of the apparent distance between this policy and the running
system does not exist.

### D6b — The enforcer requires fields this change must define

Recorded because several are hard validation failures if omitted, and one is
unreviewable until this change closes it: `risk_tier.id` has **no closed
vocabulary in code** (`:1263` accepts any non-empty string), so the vocabulary
must be defined here rather than gestured at; `anti_normalization` must declare
its semantics explicitly (`consecutive_candidates` or `rolling_window` with their
respective parameters), never inferred from the surface (`:1338`);
`activation_dependency` is required by the same `_validate_defined_not_wired`
this design leans on; `gate_integrity.never_clearable_paths` is mandatory once a
rule declares `classification_intent`; `requires_intent_reference` is **opt-in,
not automatic** (`:1672` returns `None` without it), so the class must declare
`true`; `require_same_repository: true` is schema-forced wherever
`author_class.council_cleared_logins` is present, which is this class's only
viable shape; and `human.accountable` must be a **bare login** — `:1477` refuses
a leading `@`, which every earlier revision of this packet wrote.

One enforcer contradiction blocks this today and is named rather than
worked around: widen-only forces a declared floor to cover every
`GATE_INTEGRITY_PROBES` path including `instantiation-answers.yaml` and
`sonar-project.properties`, **both absent from openxFactory**, while reachability
refuses entries matching nothing — and R1's own
`test_the_caller_opts_into_the_floor_reachability_check` establishes openxFactory
must opt in. The two controls contradict each other for any foreign repository.
The fix is repo-relative probes in codexFactory, carried as a task.

### D7 — The approval-capable caller is a distinct surface from R1

R1 is structurally read-only (`pull-requests: read`; its header states "NO
APPROVAL … The absence is STRUCTURAL"). Nothing in the advisory lane can cast a
review. G4b therefore names a separate openxFactory workflow that reads the
envelope from the base branch, computes the class and the tier-1 envelope
decision, carries `check_exclusions`, holds `pull-requests: write`, mints a
dedicated App token and submits the `APPROVE`.

Keeping it distinct from R1 is deliberate: R1's fail-red-on-missing-credential
behaviour is correct for a gate-nothing advisory reader and wrong for an
approver, and the two cannot share one file without one of those choices becoming
wrong. R1's read-only-ness is additionally **proven by test over its own file
text** (`test_the_caller_holds_only_read_permissions`,
`test_the_caller_contains_no_approval_shaped_step`), so growing it would mean
retiring the assertions that make its safety legible.

Four corrections the council made to this decomposition, all of them mechanical:
the approver's job id must **share the `merge-master-approval` substring** yet
not equal R1's — shared because `excluded()` matches by substring, so a distinct
name would leave the approver's own check inside the all-checks-green test it
computes and **reopen the deadlock this packet records as closed**; not equal,
because two same-named check-runs on one SHA are ambiguous for latest-run-per-name
selection. `check_exclusions` is a **per-candidate envelope field, not a workflow
property**, and must list **both** job ids — a prior revision put it on the
workflow and named only R1's check. The envelope must land **before** the
approver, since the approver resolves the envelope from the base branch and
cannot see the pull request that introduces it. And G4(a) will turn R1's landed
`test_the_caller_ships_no_envelope_instance` **red**; retiring it is an owned
task.

## Parity analysis

Per `docs/release-realization-flow.md`, a proposal touching a requirement an
active ratified change already modifies must declare its deltas relative to that
change's outcome — first-ratified wins. Three capabilities were examined; **this
change amends none of them**, and the reasoning is recorded so the absence of
deltas is a finding rather than an oversight.

- **`roles-authority-model` — PARITY, no delta.** The promoted requirement
  *Structural parking in external enforcement* already contains the hook this
  change needs, in its scenario *Autonomous lane coexists*: "the Merge Master
  identity may satisfy the enforcement system's review requirement without human
  involvement, **where deployment policy allows**." This change **is** the
  deployment policy for openxFactory; it supplies a permission the promoted text
  already anticipates, so no promoted text changes. Its companion scenario
  *Enforcement identity is authority-separated* is adopted as a requirement of
  the new capability rather than restated here. Against the active
  `add-substantive-review-lane` delta the position is parity on three
  requirements: *Ruleset interaction shape* (this change adopts the prescribed
  shape and declares **no divergence**, so that requirement's
  divergence-recording clause is not invoked), *Pilot repository and reviewing
  domain* (which names `opensoft/openxFactory` as the pilot — this change is that
  pilot's adoption change, not an extension, so the beyond-pilot evidence bar
  does not bind it and is not claimed), and *Constitutional floor* (adopted as
  the boundary's source, with its six-member source record named and only its two
  path-shaped members drawn).
- **`review-authority-intake` — CONSUMER, no delta.** This change consumes S3
  (exercise-at-verdict) and S5 (revocation-at-consumption) and treats both as
  unrealized. It amends no requirement. It inherits the constraint that no holder
  hold both the review act and the approval act over one object — today satisfied
  vacuously, because the approving act is held by nobody, which is why Q4 is a
  missing-artifact question rather than an interpretive one.
- **`workflow-gate-contract` — PARITY, no delta.** Its four requirements govern
  the neutral workflow-contract schema, the gate record and blocking vocabulary,
  the owner-layer constraint and adoption completion. This change adds no
  workflow contract and changes no gate record vocabulary; the merge gate it
  governs is a repository enforcement configuration, not a `workflow_contract`
  artifact. **A delta here was expected by the direction and is deliberately not
  authored** — writing a MODIFIED block that changes nothing would be noise and
  would put `promotion_fidelity.py` to work comparing text against itself.

## Alternatives considered and rejected

1. **Remove openxFactory from ruleset `18962101` and create a repo-scoped
   replacement with zero approvals plus a required `merge-master-approval`
   check.** This was the sketched design. Rejected: forbidden by ratified
   doctrine on two counts (check-run as satisfier; human path removed), and it
   relocates the enforcement of human review from GitHub into codexFactory's
   Python, because a ruleset cannot branch on class.
2. **Keep one candidate class covering both prose and derived artifacts.**
   Rejected under D3 — it makes the canary blind to class-boundary error.
3. **Grow R1 into the approver.** Rejected under D7.
4. **Widen the per-repo `repository_gate_floor` to cover the whole human-only
   surface.** Rejected under D6 — the carrier cannot express it, and the class
   floor already does most of it.
5. **Narrow the `OrganizationAdmin` bypass actor as part of this change.**
   Rejected: it is a seven-repository act, and avoiding seven-repository acts is
   this design's premise. Raised as Q6 rather than dropped, so the change cannot
   claim to "end the bypass" while the bypass stands untouched.

## Migration plan

Ordered, and the order is load-bearing. Full detail in `tasks.md`.

1. This packet lands (policy only; nothing enabled).
2. G3 — R1 (PR #439) merges; the advisory lane reports on a subsequent PR.
3. G4a — openxFactory authors its own envelope with the ONE candidate; CODEOWNERS
   widens to `.github/`; R1's no-envelope test is retired in the same change.
4. G4c — codexFactory's gate rule and clearance-rule glob floor land, advisory;
   the class-floor helper is wired into a production gate; repo-relative probes
   land; G4d — the pin advances as a recorded re-point ceremony.
5. G4b — the approval-capable caller lands, still with no clearable class.
6. G5 — the App is installed with write; the evidence artifact is captured.
7. G1, G2 — hermes-install S3 and S5 realize. **These are the long poles and
   neither is close.**
8. G6 — the register row is re-issued before 2026-11-23.
9. Canary — three dual-run observations on the prose class, all recorded.
10. G7 — a separate ratified change flips the class to `clearable`.

**The ordering of steps 4 and 5 was swapped by the council.** A prior revision
landed the approval-capable caller before codexFactory's floor work, leaving a
live App token whose only restraint was one advisory field in another
repository's YAML, read through a pin. Steps 2-6 are useful on their own and
carry no autonomy. Nothing between here and step 10 permits an autonomous
approval.

## Open questions

Carried at the proposal's dispositions; see its "Open questions" section for the
five closed by shipped rules-as-code and the six that remain (Q1 App write
access on this repository — empirical and gating; Q2 the floor's
mid-inversion source of truth; Q3 the optional named floor check; Q4 the
approval act's missing register row; Q5 who restates the floor's four non-path
conditions; Q6 whether the bypass actor should be narrowed).
