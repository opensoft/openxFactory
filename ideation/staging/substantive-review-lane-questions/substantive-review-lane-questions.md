# Staged: Open questions for the substantive review lane

Status: staged
Kind: staging-packet
Summary: Tracks the five open questions the ad-hoc-authored proposal
`add-substantive-review-lane` (openxFactory PR #178, Status: draft) declared
but did not decide, so they surface in the ideation dashboard as an
iterating staging topic while the proposal awaits Brett's ratification. This
topic is NOT the proposal's origin — it exists purely to iterate the
proposal's already-parked open questions after the fact. **ALL FIVE ARE NOW
DISPOSITIONED — ruled by Brett Heap in-session 2026-08-22 — so this topic has
met its own Exit condition and closes.**
Topics: substantive-review-lane, merge-master, gate-rules-council,
merge-readiness-council, roles-authority-model, review-personas,
codexfactory, openxfactory-pilot, hermes-domain-overlay
Repository context: openxFactory owns the neutral `roles-authority-model`
capability the proposal's spec delta targets (six ADDED requirements as
authored, ten after the 2026-08-22 rulings); codexFactory owns the
`gate_rules_council` / `merge_readiness_council` persona and council
machinery being generalized (leads: lead-architect, lead-quality,
lead-security, lead-integration; tenant seat: company-policy-lead); the
xFactory aggregation repo owns `merge-master-approval.yml` /
`merge-approval-envelope.yml`, the mechanical GitHub-App enforcer whose
candidate-class list this lane extends.
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
origin declaration. That immutability is enforced, not merely asserted:
`scripts/proposal-support.py transition` REFUSES to move this fragment into
the proposal's `supporting-docs/` precisely because the packet declares
`kind: ad_hoc` and a transition would have to declare `kind: staged`
("origins are immutable"). This topic therefore closes without a
supporting-docs move — see Exit.
Target capabilities: `roles-authority-model` — tracked, not owned here. The
in-flight change `add-substantive-review-lane` carries the ADDED
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

The proposal encodes six decided principles as ADDED requirements and was
explicit that it decided nothing about rollout order, non-engineering
persona homes, per-PR company-policy-lead seating, per-repo ruleset
mechanics, or the risk-tier taxonomy. Those five gaps were declared in the
proposal's own "Open questions" section as parked for review, not resolved
by it. This topic gave them a durable staging home so they iterated and
surfaced on the ideation dashboard while the proposal sat at Status: draft,
instead of sitting invisibly inside one proposal document until someone
happened to reread it.

**2026-08-22: all five were ruled.** A recommendation set was built on full
recon of the PR #178 packet, codexFactory's council machinery, the
aggregation repo's merge-master enforcer, the two proven autonomous
clearances (xFactory PRs #85/#100), and the prior-art vocabularies, then put
to Brett as five questions. He ruled all five in-session. Three rulings took
the recommendation; on Q2 he OVERRODE it, and on Q3 he chose a bounded third
option neither of the two surveyed shapes offered. Every disposition is
recorded per-question below.

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

## Idea notes (pre-document, non-documented)

- Two realization facts surfaced while the rulings were being encoded, and
  neither belongs to any of the five questions. They were booked into the
  proposal's `tasks.md` (§4.4, §4.5) rather than left here, because they are
  work items for the realization, not open topics: the envelope matcher
  compares head refs by exact string equality (codexFactory
  `scripts/merge_master/envelope.py`'s `_find_surface`), so no candidate
  class can span arbitrary branches without a matcher change; and the
  per-repo rule file's `repository:` key means "whose rules these are" in
  `nightly-sweep-council-clearance.yaml` (`opensoft/codexFactory`) while the
  PRs it governs are the aggregation repo's, which the envelope names in
  `target_repos` — one key, two readings, invisible at one repo and a
  correctness hazard at several. — Added-by: Claude Opus 5 (agent) ·
  2026-08-22
- Q1 and Q5 both terminate in "a named follow-up change raised on pilot
  evidence". Nobody has ruled whether that is ONE change or two. The
  disposition text deliberately records the PATH rather than a change name,
  so whichever shape gets raised satisfies both. — Added-by: Claude Opus 5
  (agent) · 2026-08-22
- Q3's conditional pull-in has a natural second use nobody asked for: the
  same per-class `when:` shape could seat other cross-layer personas per-PR
  (a data-protection seat, say) without touching the default. Not proposed,
  not needed, recorded only so the mechanism's generality is on the record
  rather than rediscovered. — Added-by: Claude Opus 5 (agent) · 2026-08-22

## Conflicts

- **Q2's ruling versus the recommendation put to Brett.** The written
  recommendation was a TWO-AXIS split — codexFactory owns the engineering
  dimension of every repo's PRs, the owning domain owns the domain-content
  dimension and stands up its own review body at adoption. Brett overrode it:
  codexFactory reviews everything, zero new persona homes. The tension the
  recommendation was built around is NOT resolved by the override, it is
  ACCEPTED: a MedxFactory PR whose content is medical governance is reviewed
  by a council with no standing in that domain. Recorded honestly in
  `design.md` Decision F with the mitigations that actually exist
  (`needs_human_review` at every class, the gate-rules council's human-only
  power, and the Q5 constitutional floor). — Added-by: Claude Opus 5 (agent)
  · 2026-08-22
- **Q3's ruling versus the councils' own 2026-07-22 "PERMANENTLY DISTINCT"
  text.** Both codexFactory council files state that a body which sets the
  rules must not also apply them. Brett's conditional pull-in bends that at a
  declared point: for classes that opt in, the rule-setting seat joins the
  rule-applying council. This is a real inconsistency with the recorded
  wording, not a reinterpretation of it, and it is left standing deliberately
  — the ruling bounds it (the rule-setting body itself declares which classes
  summon it, at class-definition time, never per PR) rather than repealing
  the 2026-07-22 decision. If the council files' wording is ever amended, it
  is that amendment's job to say so. — Added-by: Claude Opus 5 (agent) ·
  2026-08-22
- **Q3's ruling versus `design.md` Decision D as authored.** Decision D
  defended rules-council-only and named per-PR seating a declared open
  question. It is now SUPERSEDED IN PART, not replaced: its defense survives
  as the reason rules-only is the DEFAULT, and its last clause no longer
  holds. Kept verbatim in the design doc with the superseding ruling recorded
  after it. — Added-by: Claude Opus 5 (agent) · 2026-08-22

## Open questions

All five carry a disposition. None is `open`.

### Q1. Once the openxFactory pilot is live, which governed repo adopts the substantive review lane next, in what order, and what qualifies a repo to be next?

Context: Requirement 6 already makes each adoption its own change. The
machinery is per-repo workflow instances — the convening lane is a thin
caller, but `merge-master-approval.yml` is a 55KB copy-per-repo today, and
openxFactory currently has almost no CI surface. Brett had already ruled once
(2026-08-15) that this topic is sequenced after the doxBench sprint, which is
now complete. The proposal named the pilot and was silent on what comes after
it.
Recommended answer: Defer the ORDER to pilot evidence, but record the
evidence BAR and the ordering principle now.
Explanation: The order is not decidable before the pilot produces evidence,
but the bar that evidence has to clear IS decidable now, and recording it now
is what stops "the pilot went fine" from being an unfalsifiable qualification
later. The ordering principle costs nothing to fix and removes a whole class
of argument at adoption time.
Disposition status: RULED as recommended — Brett Heap, in-session 2026-08-22.
The adoption ORDER is decided by a named follow-up change raised on pilot
evidence, through the one-change-per-repo mechanism the pilot requirement
already carries. The EVIDENCE BAR is decided now: ≥3 council-cleared
substantive PRs spanning ≥2 candidate classes, zero enforcer incidents, and
one completed gate-rules review cycle. The ORDERING PRINCIPLE is decided now:
engineering-owned repos before domain repos. ROUTE: proposal edit for the bar
and the principle (encoded as the "Adoption beyond the pilot qualifies on
recorded evidence" requirement); named follow-up change for the order itself.
Added-by: Brett Heap (ruling) · Claude Opus 5 (agent, recording) · 2026-08-22

### Q2. When a substantive PR lands in a non-engineering domain repo, does that repo instantiate its own review personas and councils, or does codexFactory review software changes wherever they land?

Context: Only codexFactory has instantiated review personas; replicating them
means each domain authors its own domain-hermes-content instance. The tenant
company-policy-lead seat is already cross-layer and domain-independent, and
the proven deliberation runs on a shared runtime, so "codexFactory reviews
everywhere" is the zero-new-persona option. Against it: a Medx PR's CONTENT
can be medical governance, where codexFactory has no standing.
Recommended answer: Rule a two-axis principle — the ENGINEERING dimension of
every governed repo's PRs belongs to codexFactory, the DOMAIN-CONTENT
dimension belongs to the owning domain, whose adoption change names and
instantiates its own review body at adoption time.
Explanation: It picks neither global shape, makes the choice per-repo at
adoption, and never duplicates the engineering half — while refusing to
assert standing codexFactory does not have over domain content.
Disposition status: RULED — Brett Heap, in-session 2026-08-22 — and the
recommendation was OVERRIDDEN. codexFactory's `gate_rules_council` and
`merge_readiness_council` review substantive PRs in ALL governed xFactory
repos, whatever domain the repo governs: a PR's diff is software regardless
of the domain. NO domain repo instantiates its own review personas or
councils for this lane; zero new persona homes. The tenant
company-policy-lead seat continues to carry the policy dimension inside
codexFactory's councils. The adoption-change-per-repo requirement SURVIVES —
only the persona-home fork is removed, and an adoption change now names the
repo and affirms codexFactory as its reviewer. ROUTE: proposal edit
(rewritten "Pilot repository and reviewing domain" requirement, plus a new
`design.md` Decision F recording the override and the residual risk).
Added-by: Brett Heap (ruling) · Claude Opus 5 (agent, recording) · 2026-08-22

### Q3. Does the tenant company-policy-lead seat join per-PR merge-readiness councils, or stay rules-council-only?

Context: Today that seat sits only in `gate_rules_council` (rule-setting),
not in the per-PR `merge_readiness_council`. Both council files declare the
separation PERMANENT, decided 2026-07-22: "a body that sets the rules must
not also apply them." `missing_required_seat: refused` means adding the seat
to per-PR councils makes every convening fail-closed on that seat's
availability. The seat has been exercised at class-definition time and it
worked (the 2026-07-23 clearance record).
Recommended answer: Rules-council-only, indefinitely — company policy
expresses through the candidate-class rules the seat already sets, and per-PR
policy concerns route through `needs_human_review` escalation.
Explanation: Folding the seat into per-PR deliberation would re-litigate a
recorded 2026-07-22 architectural decision and add a tenant-availability
failure mode to every PR.
Disposition status: RULED — Brett Heap, in-session 2026-08-22 — and he chose
a BOUNDED THIRD OPTION rather than either surveyed shape. DEFAULT: the seat
stays rules-council-only and the 2026-07-22 separation stands as the default
posture. EXCEPTION, bounded and declared: a candidate class MAY declare a
company-policy pull-in condition, and a PR matching such a class pulls the
company-policy-lead seat into THAT PR's `merge_readiness_council` convening —
mirroring the existing `client-security-compliance-officer` /
`rule_touches_security_posture` conjunction in `gate-rules.yaml`. The
condition is defined PER CANDIDATE CLASS by the `gate_rules_council` (where
the seat already sits) at class-definition time, so the seat itself decides,
on the record, which classes summon it per-PR. Fail-closed follows the
existing `missing_required_seat: refused` rule: for a pull-in class, a
convening missing the seat is refused and parked — an accepted cost, bounded
to policy-flagged classes, with every other class keeping domain-seats-only
per-PR councils. ROUTE: proposal edit (new "Company-policy seat participation
in per-PR councils" requirement; `design.md` Decision D marked SUPERSEDED IN
PART, its text kept).
Added-by: Brett Heap (ruling) · Claude Opus 5 (agent, recording) · 2026-08-22

### Q4. For a given governed repo, what satisfies the required-review gate — a real App APPROVE review, a required check-run, or both — and does human review remain an always-available alternate path?

Context: The proven flow casts a real `APPROVE` review from the dedicated
merge-master App (GITHUB_TOKEN approvals do not satisfy required review). The
check-run is the verdict TRANSPORT, deliberately not the ruleset satisfier —
the workflow's own anti-spoofing analysis explains why a name-matched
check-run would be forgeable. The neutral spec's parking language already
says "named or counted required reviewers"; ruleset edits require the
administration-tier App under governed custody.
Recommended answer: Standardize the proven shape as the default for every
governed repo — real APPROVE satisfies required review; the check-run stays
transport only and is never a ruleset satisfier; human review remains an
always-available alternate path on every repo; per-repo divergence needs its
own recorded decision.
Explanation: The shape is proven, its anti-spoofing property is the reason
the transport is not the satisfier, and an App-path-only repo would let a
council outage block humans.
Disposition status: RULED as recommended — Brett Heap, in-session 2026-08-22.
The merge-master App casts a REAL APPROVE review and that review satisfies
the repo's required-review rule. The council-verdict check-run remains
verdict TRANSPORT only and is NEVER configured as a ruleset-accepted
satisfier (the anti-spoofing analysis is the recorded reason). Human review
REMAINS an always-available alternate satisfying path on EVERY governed repo;
no repo's ruleset may be configured App-path-only, because a council outage
must never block humans. Per-repo divergence, if ever wanted, requires its
own recorded decision inside that repo's adoption change. ROUTE: proposal
edit (new "Ruleset interaction shape for the substantive review lane"
requirement; `design.md` Decision C amended).
Added-by: Brett Heap (ruling) · Claude Opus 5 (agent, recording) · 2026-08-22

### Q5. Which risk tiers exist, how are they ordered, and which are ever eligible for autonomous clearance versus permanently human-only?

Context: No `risk_tier` / `clearance_rule` field exists anywhere yet; the one
clearable condition is hard-coded in Python. A ratified never-clearable floor
already exists (identity mismatch, failed checks, secret findings,
security-touching paths, gate-weakening changes). The docs-class allowlist
was already narrowed once by a council finding. `design.md` Decision B
deliberately requires tier PRESENCE, not a vocabulary, citing the
unfalsifiable-first-draft lesson. The omnigent permission matrix's
constitutional-false is the standing precedent for "never, regardless of
verdict".
Recommended answer: Split it — rule the CONSTITUTIONAL FLOOR now, defer the
vocabulary to pilot evidence.
Explanation: The "never, regardless of verdict" band is expressible without a
vocabulary and is the half that actually bounds risk; naming the graded band
above it before a second real candidate class exists would repeat the
unfalsifiable-first-draft failure Decision B was written to avoid.
Disposition status: RULED as recommended — Brett Heap, in-session 2026-08-22.
Ruled NOW, in three clauses: (i) the ratified never-clearable floor is
TIER-INDEPENDENT — no tier, clearance rule, or unanimous verdict ever
overrides it; (ii) any candidate class touching contract bytes, gate/workflow
definitions, credential surfaces, or security posture is PERMANENTLY
human-only, regardless of unanimity; (iii) autonomous clearance is only ever
eligible for classes whose blast radius is docs-/derived-artifact-shaped,
today exactly the proven docs class. DEFERRED: the enumerated, ordered tier
vocabulary with per-tier clearance eligibility, to the evidence-driven
follow-up change — the same follow-up path Q1's rollout order takes; they may
share one change or come separately. ROUTE: proposal edit for the floor (new
"Constitutional floor for autonomous clearance" requirement, whose own text
records the deferral; `design.md` Decision B amended); named follow-up change
for the vocabulary.
Added-by: Brett Heap (ruling) · Claude Opus 5 (agent, recording) · 2026-08-22

## Exit

Each question resolved independently and landed in one of the three places
this section named at capture: an edit to the governing proposal's own text
while it remains pre-ratification (`Status: draft`); a named follow-up
OpenSpec change raised after ratification, for a question whose answer only
becomes decidable once the pilot is live and producing evidence; or a
recorded decision ruled directly and noted back into this fragment with the
date and rationale. In the event all five took the first route for the part
that was decidable now, with two of them ALSO naming the second route for a
deliberately deferred residue (the adoption order, and the risk-tier
vocabulary) — and all five were ruled directly, so the third route is how
each disposition above is worded.

This topic carries no exit change of its own — it tracked another change's
parked questions rather than proposing anything — and with all five questions
dispositioned it has met its own closing condition: the folder is retired and
its content kept as provenance. It cannot exit by moving into a proposal's
`supporting-docs/`, the route the two prior exited topics took, because the
governing proposal's origin is `ad_hoc` and the transition tool refuses to
restate an immutable origin as `staged`. The retirement is therefore recorded
in `ideation/staging/INDEX.md`, whose row is kept and flipped to the
exit-record form, naming this file's final committed state rather than
linking to a path that will no longer resolve.
