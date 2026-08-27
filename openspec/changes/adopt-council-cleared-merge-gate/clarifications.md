# Clarifications: adopt-council-cleared-merge-gate

Status: draft

What this packet decided, what it was corrected on, and what it refuses to
decide. Five review records are retained beside it — `alignment-qa-lead.md`,
`alignment-stack-architect.md`, `council-product-advocate.md`,
`council-systems-architect.md`, `council-adversary-engineer.md`.

## N1 — The direction's literal shape was not implementable, and doctrine agreed

The convener's sketch was "required checks `wallet-validation` + `pytest-suite` +
`merge-master-approval` **in place of** the 1-approving-review rule". The packet
does not implement it, for reasons that arrived from two independent directions.

Mechanically: the 1-approval rule lives in **org** ruleset `18962101`, targeting
seven repositories, and openxFactory has no repository-level ruleset at all. A
GitHub ruleset cannot branch on pull-request class, so per-class gating is not
expressible at the ruleset layer. A check-satisfier design would therefore have
relocated the enforcement of human review from GitHub into codexFactory's Python.

Doctrinally: `add-substantive-review-lane`'s *Ruleset interaction shape*
prescribes an App-cast `APPROVE` review, forbids a check-run as satisfier
("MUST NEVER"), and forbids removing the human path.

**Resolution:** the gate composition is unchanged and only the approver set
moves. The sketch is recorded as rejected alternative 1 in `design.md`, not
silently dropped, because it was the convener's own framing.

## N2 — The boundary must be derived from rules-as-code, not from ratified prose

The first draft derived its class boundary from openxFactory's ratified prose and
did not check it against codexFactory's implemented enforcer. The enforcer
refused three of its clearable entries: `openspec/changes/**` sits in the PR-time
`GATE_INTEGRITY_FLOOR` and `openspec/` in the definition-time
`PROTECTED_CLASS_SURFACES`; `CLAUDE.md` and `AGENTS.md` are `PROTECTED_ROOT_FILES`;
`governance/` is wholly protected, inverting the draft's carve-out.

**Resolution:** the derivation was reversed — start from the enforcer's
constants, assert only what they do not cover. This closed three of the draft's
five open questions and shrank the floor-widening gate.

**Recorded because it is this change's own subject matter:** a packet written to
prevent "a described control treated as existing" had itself described a boundary
the enforcer would have refused to implement.

## N3 — The value claim is narrower than the direction supposed, and says so

The direction supposed "openxFactory is a contracts/docs repo so most PRs
qualify". **That is false.** openxFactory's dominant traffic is
`openspec/changes/**`, floored twice. What remains clearable is `docs/**/*.md`,
`ideation/**/*.md`, `README.md` and two derived `health/` trees.

**Resolution:** stated prominently in the proposal rather than buried, including
that **this packet's own diff would not qualify under its own boundary.** No
attempt was made to widen the boundary to fit the ambition; narrowing a floor is
forbidden outright.

## N4 — The boundary is expressed as named classes, because that is what an
## enforcer matches

The implemented object is a four-layer classification: declared class intent →
path allowlist → gate-integrity denylist → per-condition predicates, with an
envelope candidate bound to a per-repo gate rule by explicit
`applies_to.candidate_id`, and `classification_intent` the sole authority for
advisory-versus-clearable.

**Resolution:** two named classes — `openxfactory-governance-prose` and
`openxfactory-derived-health-artifact` — each enrolled `advisory`, each owing a
`risk_tier`, an owning seat and a resolvable `intent_reference`. The human-only
enumeration is a reader's aid, not the control, since an allowlist admits only
what it names.

Two classes rather than one is a decision, not a formality: a canary confined to
one class cannot detect a class-boundary error, which is the failure a canary on
a classification change exists to catch.

## N5 — The floor is six conditions, only two of them path-shaped

The *Constitutional floor* names its source of truth as codexFactory's
`gate_rules_council` record of 2026-07-23, "and where it and that record ever
diverge the record governs". That floor has six members: identity mismatch,
head-ref mismatch, failed or pending required checks, secret findings,
security-touching paths, gate-weakening changes.

**Resolution:** the packet presents its path list as the path-shaped **subset**
of a six-condition floor, and raises **Q5** for who restates the other four for
openxFactory. A requirement in the new capability makes leaving them
unattributed an incompleteness rather than a silent inheritance.

## N6 — Five questions closed by shipped code, not by argument

Recorded as closed so they are not re-opened as undecided: `scripts/**`,
`tests/**`, `contracts/*.schema.yaml` and `.github/**` are human-only by
inherited running controls (not by this change's assertion); an App-cast
`APPROVE` does satisfy ruleset `18962101` (xFactory PRs #85 and #100, same
unmodified ruleset, `reviewDecision: APPROVED` from App `codexfactory`);
`require_extra_approval_for_unattributed_changes` keys on the pull request's
author, not the reviewer; the self-reference deadlock is escapable and already
escaped (`check_exclusions: [merge-master-approval]`); and the beyond-pilot
≥3-verdict bar does not bind this change, because openxFactory is the **named
pilot**.

**Presenting a shipped control as an owed one is the same class of error as the
reverse**, and the draft made it four times.

## N7 — Gate evidence is an artifact at a path, never a checkbox

The draft's gates were loose enough to wave through: G1 cited task numbers that
exist in **two** packets where ticking one does not tick the other; G2's
"rehearsed test" named a prose `**Gate:**` line; G5 — the gate the whole
mechanism turns on — asked only for "one verification".

**Resolution:** every gate now names an observable artifact at a stated path, and
a requirement in the new capability forbids opening a gate on evidence inherited
from the adoption document's own text. G5 requires a throwaway pull request, the
App's cast `APPROVE`, and captured `gh api` JSON committed at
`evidence/g5-app-review.md`.

## N8 — What "ending the bypass" means, stated rather than implied

All three gating rulesets keep `OrganizationAdmin / bypass_mode: always`, and
this change proposes no task that narrows it. What ends is the bypass's
**routine use**.

The ritual is measured, not asserted: the last 25 merges to openxFactory `main`
all show `reviewDecision: REVIEW_REQUIRED` with `mergedBy: brettheap`.

**Resolution:** a proposal subsection states this plainly; a capability
requirement obliges any adoption to do the same; and **Q6** asks whether the
actor should be narrowed, kept out of this change because narrowing an org-level
bypass is a seven-repository act.

## N9 — Nothing here authorizes an autonomous approval

The packet's most important negative claim. Both classes enroll `advisory`;
`_validate_defined_not_wired` makes `clearable` structurally unreachable for an
unwired repository; seven gates are recorded **NOT MET**; and the flip to
`clearable` is **G7**, a separate ratified act this change explicitly does not
perform.

**Refused deliberately:** ratification. A gate-policy change is the convener's
own ruling. This packet stops at `Status: draft` and no agent writes
`Status: ratified`.

---

# Council round, 2026-08-27

Three seats. **Tally: 2 APPROVE WITH CONDITIONS (product-advocate, adversary-engineer),
1 BLOCK (systems-architect).** Twenty-five conditions in total, **all accepted and
applied**. The block was answered by revision, not argument.

## N10 — The council's one unanimous act: the second class is gone

All three seats independently required the removal of
`openxfactory-derived-health-artifact`, on three different grounds, and the
systems-architect blocked on it:

- **Value** — its two trees have produced **three pull requests ever**, none in
  five weeks, both lanes documented dormant; and both historical pull requests
  also carried a `.yaml` outside `DERIVED_ARTIFACT_ROOTS`, so **even they would
  not have cleared**.
- **Security** — `health/neutrality-drift/**` admits
  `health/neutrality-drift/baseline/codexFactory.yaml`, **the only tracked file in
  that tree**, documented immutable and read back by `load_baseline` to decide
  what the next run treats as already judged. `PROTECTED_PATH_SEGMENTS` guards
  **patterns**, not changed paths, so the broad glob validates. The enforcer's own
  docstring names the hazard verbatim — "reachable by moving one glob". **This
  proposal wrote that glob.**
- **Structure** — the canary required ≥3 observations in a class with no
  producer, so **G7's flip was structurally unreachable** and the packet would
  have ratified a boundary it made permanently unexercisable.

**Resolution:** ONE class. The canary is prose-only at N=3, and **each class
carries its own canary in the change that enrolls it** — which keeps the
class-boundary-error detection the alignment round asked for without conditioning
adoption on traffic that does not exist. The derived class is deferred to a
successor, gated on a wired producer and on the
`add-classification-intent-and-substantive-classes` Phase-2 hold being lifted.

## N11 — Three claims this packet made about the running system were false

Each was caught by executing the code rather than reading it, and each is
**withdrawn in a named subsection rather than quietly edited**, because a
withdrawn claim that leaves no trace teaches nobody.

- **The class floor does NOT "already refuse" the human-only surfaces for
  openxFactory.** `class_floor_problem` returns `None` for any advisory rule, its
  callsites resolve no candidate for a foreign repository, and the helpers that
  *would* judge an advisory class have **zero production callsites — tests only**.
  A repository with no gate rule gets **no evaluation at all**: today's protection
  is the absence of a mechanism, not a running control. **This was the packet's
  single largest reliance.**
- **The predecessor class does not exist.**
  `openxfactory-derived-health-artifact-advisory-v1` lives only as prose in an
  active, unarchived change at two **unchecked** tasks, behind a held Phase-2
  gate. The draft called it "PREPARED AND PARKED" with a `state:` value — a
  shipped rules-as-code state attributed to an unchecked task.
- **"A mixed diff takes the most restrictive class" is not implemented.**
  `_find_surface` selects on `target_repos` and **head ref only**, first-match-wins;
  paths are never consulted for selection. A mixed diff parks on the selected
  candidate's allowlist overflow. Fail-closed either way, so the safety conclusion
  survived; the mechanism did not.

**Recorded as the packet's own lesson:** LS-A3 was committed here **three times**,
each time by deriving from prose rather than from code. Once by the first draft
(N2), twice more by the post-alignment draft. The alignment round's reversal of
the derivation was right and was not applied deeply enough.

## N12 — The value claim is published, not buried

The council required a falsifiable throughput figure. Measured: **0 of the last 40
merged pull requests** would have qualified; 13 of 140, twelve of those from one
closed campaign on one file. **~0 pull requests per week today.**

The proposal now states that this is the strongest argument against ratifying it
on throughput grounds, and rests its case on **option-closing** instead — the
product-advocate seat's own defence, which it called the strongest part of the
packet: the boundary constrains a mechanism whose shape is *already committed in
code*, and G1/G2 land signature verification, not classification, so their arrival
will not reopen it.

## N13 — The traffic is somewhere this change cannot go, and Q7 says so

**Four of the recent 40 merged pull requests are `openspec/changes/**/tasks.md`-only
checkbox ticks** — 10% of recent traffic, more than the clearable class at its
peak. openxFactory's bypass ritual is **bookkeeping under `openspec/`, not prose.**
It is floored twice and narrowing a floor is forbidden, so reaching it needs a
doctrine amendment nobody has proposed — plausibly a checkbox-only class defined
by **diff shape** rather than path, since the objection to `openspec/changes/**`
is that it holds the change records, which a checkbox tick does not alter.

**Raised as Q7** rather than left unasked, together with the alternative the seat
offered: move the pilot to `opensoft/xFactory`, which already carries the org's
only `clearable` class and a recurring producer.

## N14 — The kill switch had two stops, not three; and the CODEOWNERS floor is
## discharged by the bypass it was meant to replace

Stop A (`human.kill_switch`) and stop B (credential removal) run. **Stop C —
register revocation — depends on S5, which this change itself records as
unbuilt.** G6's expiry safety rests on the same unbuilt S5. Both corrected.

Separately: `@brettheap` is the sole CODEOWNERS owner **and** the only
`OrganizationAdmin` bypass actor, and GitHub bars self-approval. So on a pull
request he authors touching an owned path, the code-owner floor **can only ever be
discharged by the bypass this change exists to end** — and the owed widening of
the route to `.github/` *enlarges* that surface. Consequence 4's claim of
independent human accountability is corrected to: un-spoofable **against the
App**, unsatisfiable **by its sole owner**. Folded into Q6, which is therefore not
a tidiness question but the question of whether the assembly-class floor means
anything today.

## N15 — Mechanical corrections carried without argument

`check_exclusions` is a **per-candidate envelope field**, not a workflow property,
and must list **both** job ids; the approver's job id must **share** the
`merge-master-approval` substring (because `excluded()` matches by substring) yet
not equal R1's (because two same-named check-runs on one SHA are ambiguous);
`requires_intent_reference` is **opt-in**; `human.accountable` must be a **bare
login**; `risk_tier.id` has **no closed vocabulary in code**, so this change must
define one; `anti_normalization` semantics are mandatory and never inferred;
`21538893` sets `strict: false`, so the stale-approval analysis covered head
pushes only; G4(a) will turn R1's `test_the_caller_ships_no_envelope_instance`
**red**, and retiring it is now an owned task; and the gate order is **G4(c)
before G4(b)**, so an approval-capable App token does not idle while its only
restraint is one advisory field in another repository.

One enforcer contradiction is named rather than worked around: widen-only demands
a declared floor cover `instantiation-answers.yaml` and
`sonar-project.properties`, **both absent from openxFactory**, while reachability
refuses entries matching nothing — and R1 requires openxFactory to opt in. Fixed
by repo-relative probes in codexFactory, **not** by silently declining to pass
`tree_paths`.

## N16 — What the council did not change

The spine. Per-repo self-hosting; the App-cast `APPROVE` satisfying the existing
review rule with no org ruleset relaxed; advisory-first enrollment; gates before
acts; the one repo-scoped ruleset **hardening**; and the refusal to ratify. Three
seats examined the design's shape and none proposed a different one.
