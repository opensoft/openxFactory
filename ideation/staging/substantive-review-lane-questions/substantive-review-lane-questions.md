# Staged: Open questions for the substantive review lane

Status: staged
Kind: staging-packet
Summary: Tracks the five open questions the ad-hoc-authored proposal
`add-substantive-review-lane` (openxFactory PR #178, Status: draft) declares
but does not decide, so they surface in the ideation dashboard as an
iterating staging topic while the proposal awaits Brett's ratification. This
topic is NOT the proposal's origin — it exists purely to iterate the
proposal's already-parked open questions after the fact.
Topics: substantive-review-lane, merge-master, gate-rules-council,
merge-readiness-council, roles-authority-model, review-personas,
codexfactory, openxfactory-pilot, hermes-domain-overlay
Repository context: openxFactory owns the neutral `roles-authority-model`
capability the proposal's spec delta targets (six ADDED requirements);
codexFactory owns the `gate_rules_council` / `merge_readiness_council`
persona and council machinery being generalized (leads: lead-architect,
lead-quality, lead-security, lead-integration; tenant seat:
company-policy-lead); the xFactory aggregation repo owns
`merge-master-approval.yml` / `merge-approval-envelope.yml`, the mechanical
GitHub-App enforcer whose candidate-class list this lane extends.
Staging ID: openxFactory:staging:substantive-review-lane-questions
Captured: 2026-08-15
Source: Brett Heap's direction 2026-08-15 to track, as an iterating staging
topic, the declared-open-not-decided questions of the proposal
`add-substantive-review-lane` (openxFactory PR #178, branch
`change/add-substantive-review-lane`, Status: draft — awaiting ratification).
Same pattern as the `manager-review-approval-scope-kind` topic, which tracks
a sibling in-flight artifact's parked question rather than originating it.
**Honesty note (not the origin):** the proposal's own `.openspec.yaml` origin
block declares `kind: ad_hoc`, `id:
openxFactory:adhoc:2026-08-15-add-substantive-review-lane`, authored directly
from verified current-state facts (autonomous `gate_rules_council` +
`merge_readiness_council` deliberation proven live 2026-08-14 on xFactory
PRs #85 and #100) — the proposal was created BEFORE this topic existed. This
topic is post-proposal tracking of its parked questions, never a claimed
staged origin; nothing here retroactively edits the proposal's immutable
origin declaration.
Target capabilities: `roles-authority-model` — tracked, not owned here. The
in-flight change `add-substantive-review-lane` carries the six ADDED
requirements against this capability; this topic makes no capability delta
of its own. It exists only to iterate the proposal's five declared open
questions and closes when all five are dispositioned.

## Context

`add-substantive-review-lane` generalizes codexFactory's proven
`gate_rules_council` (lead-architect + lead-security + lead-quality + the
tenant `company-policy-lead` seat, which sets per-repo `per_repo_gate_rules`)
and `merge_readiness_council` (lead-quality + lead-security +
lead-integration, which judges individual PRs `ready | blocked |
needs_human_review`), plus the aggregation repo's mechanical
`merge-master-approval.yml` GitHub-App enforcer, from their one proven lane
(the nightly `doc-health-nightly` / `docs_only_path_overflow` candidate
class, aggregation repo only) into a named substantive review lane spanning
governed xFactory repos — piloted on `opensoft/openxFactory`, reviewed by
codexFactory's councils (the software-engineering domain reviewing the
engineering-contracts repo).

The proposal encodes six decided principles as ADDED requirements and is
explicit that it decides nothing about rollout order, non-engineering
persona homes, per-PR company-policy-lead seating, per-repo ruleset
mechanics, or the risk-tier taxonomy. Those five gaps are declared in the
proposal's own "Open questions" section as parked for review, not resolved
by it. This topic gives them a durable staging home so they iterate and
surface on the ideation dashboard while the proposal sits at Status: draft,
instead of sitting invisibly inside one proposal document until someone
happens to reread it.

## Claims

The following six principles are **settled in the proposal and are NOT
reopened by this topic** — they are recorded here only so the open questions
below can be read against a stable baseline, not to relitigate them:

1. Councils judge; Merge Master stays the mechanical enforcer — the
   generalization adds candidate classes and council scope, never moves
   judgment into the enforcer.
2. Accountability is the product — every seat produces a written rationale,
   the verdict transports as a signed identity-bound check-run, an audit
   artifact records inputs/rules-version/verdicts, and the approving review
   is cast by a dedicated reviewer/merge-master App identity, never
   `GITHUB_TOKEN` and never the author's identity.
3. Identity separation — the reviewing council and enforcing identity must
   be distinct from the PR author's identity (human or agent), and review
   rules always evaluate from the base branch.
4. Fail-closed — anything outside a defined candidate class, any
   non-unanimous or conditioned verdict, or any stale/missing rule set
   yields no approval and parks with explanation; `needs_human_review`
   escalation is always available, and some classes may be declared
   human-only by the gate-rules council.
5. Council-defined candidate classes with risk tiers — the
   `gate_rules_council` (which includes the tenant company-policy-lead seat)
   defines per-repo candidate classes covering substantive human- and
   agent-authored PRs, each with a risk tier and a clearance rule, reviewing
   for company-policy compliance AND domain best practices.
6. Pilot: openxFactory reviewed by codexFactory — `opensoft/openxFactory` is
   reviewed by codexFactory's councils (the software-engineering domain
   reviewing the engineering-contracts repo), then extended per adoption.

## Open questions

These are the proposal's five declared-open items, carried here to iterate
independently. Resolving one does not require resolving the others; each may
land as a proposal edit (while it is still `Status: draft`), a follow-up
change, or a Brett-ruled recorded decision.

1. **Rollout order beyond the pilot.** Once the `opensoft/openxFactory`
   pilot is live, which governed repo adopts the substantive review lane
   next, in what order, and what gates each adoption (a green pilot
   evidence bar? a per-repo readiness check? Brett's direct sequencing?).
   The proposal names the pilot but is silent on what comes after it or
   what qualifies a repo to be next.
2. **Persona home for non-engineering domain repos.** When a substantive PR
   lands in MedxFactory, LedgerxFactory, OpsxFactory, or AdxFactory, does
   that domain repo instantiate its own review personas/councils (mirroring
   codexFactory's `hermes/domain/review-councils/`), or does codexFactory
   review all *software* changes regardless of which repo carries them (on
   the theory that a PR's diff is software regardless of the domain the
   repo governs)? Both shapes are consistent with the proposal's six
   decided requirements — it deliberately picks neither.
3. **Whether the tenant `company-policy-lead` seat joins per-PR
   merge-readiness councils.** Today that seat sits only in
   `gate_rules_council` (rule-setting), not in the per-PR
   `merge_readiness_council` (individual verdict). Does the substantive
   lane fold it into per-PR deliberation as PR volume grows across more
   repos, or does it remain rules-council-only indefinitely, with company
   policy expressed entirely through the candidate-class rules it already
   sets?
4. **Ruleset interaction shape per repo.** For a given governed repo, does
   satisfying the required-review gate mean the merge-master App casts a
   real `APPROVE` review (as codexFactory's proven flow does today), or a
   required check-run the ruleset also accepts, or both configured
   per-repo? And separately: does human review remain an always-available
   alternate satisfying path on every repo, or can a repo's ruleset be
   configured so only the council-cleared App path satisfies it? The
   proposal calls this "a per-repo ruleset-wiring decision" without making
   it.
5. **Risk-tier taxonomy for candidate classes.** The proposal requires
   every candidate class to declare a risk tier and a clearance rule, but
   does not enumerate the tier vocabulary itself. Candidate tiers named in
   discussion (docs-only, config, contract, runtime-code) are illustrative,
   not adopted. Which tiers exist, how they are ordered, and — critically —
   which tiers, if any, are EVER eligible for autonomous (no
   `needs_human_review` escalation) clearance, versus which tiers are
   permanently human-only regardless of unanimous council verdict, is
   undecided.

## Exit

Each question above resolves independently and lands in one of three
places: an edit to the governing proposal's own text while it remains
pre-ratification (`Status: draft`); a named follow-up OpenSpec change raised
after ratification, for a question whose answer only becomes decidable once
the pilot is live and producing evidence (rollout order and the risk-tier
taxonomy are the likeliest candidates for this path); or a recorded decision
Brett rules directly, noted back into this fragment with the date and
rationale. This topic carries no exit change of its own — it tracks another
change's parked questions rather than proposing anything — and it closes
(the folder is retired, its content kept as provenance) once all five
questions carry a disposition, whichever of the three routes each took.
