---
code_surface: xFactory aggregation repo (.github/workflows/merge-master-approval.yml + .github/merge-approval-envelope.yml — additional substantive candidate classes and generalized council-verdict consumption; per-repo instances of these files for repos beyond opensoft/xFactory), codexFactory (hermes/domain/review-councils/gate-rules.yaml candidate-class + risk-tier + per-class company-policy pull-in-condition additions, hermes/domain/review-councils/merge-readiness.yaml conditional company-policy-lead seat, merge_readiness_council scope generalized to substantive human- and agent-authored PRs), openxFactory (this spec delta on roles-authority-model; opensoft/openxFactory as the pilot repo's ruleset + workflow wiring). This change's own diff is the spec delta; the workflow/council/ruleset realization across the three surfaces is downstream, tracked in tasks.md and archived only on merged, green realization evidence per release-realization.
target_release: implemented (no contract-bundle involvement — this generalizes the roles-authority-model authority doc and cross-repo rules-as-code, not a `contracts/schemas/` artifact; realization lands as workflow, council, and ruleset changes in the affected repos)
---

# Proposal: add-substantive-review-lane

Status: ratified
Ratified: 2026-08-22 by Brett Heap — in-session via question prompts at the
ratification read; record: `review/ratification-2026-08-22.md`. Four
read-items were ruled in that round: (1) the FORM ELEVATION of Q1's evidence
bar and Q5's constitutional floor from proposal text into promoted
requirements is ACCEPTED; (2) the Q1 bar's COUNTING RULE is that any
council-cleared verdict counts — a unanimous council verdict counts toward
the ≥3 bar whether the approving review was cast by the merge-master App or
by a human, because the bar measures council quality, not enforcer autonomy
(this OVERRODE the encoder's autonomous-only reading); (3) the ordering
principle stays ABSOLUTE — no waiver clause and no activity scoping, the
dormant-engineering-repo consequence accepted, with a direct Brett escalation
inside a future adoption change as the escape path rather than requirement
text; and (4) RATIFY. Authored 2026-08-15 from verified current state
(`.openspec.yaml` origin block). Separately and earlier the same day, the
five questions this proposal originally declared open were RULED by Brett
Heap in-session and are recorded below under "Decided questions", each
encoded as requirement text in this change's spec delta; that clarify round
is distinct from this ratification and is cross-referenced from the
ratification record.

## Why

Governed xFactory repos carry review-required rulesets. Today there are
exactly two ways past one: a human review, or an `--admin` bypass.

A governed, accountable AI reviewer already exists, and it is already live —
but only for one narrow lane. codexFactory's `gate_rules_council`
(lead-architect + lead-security + lead-quality + the tenant
company-policy-lead seat) sets per-repo merge/gate rules
(`per_repo_gate_rules`, `enforcement: merge_master_operator`); its
`merge_readiness_council` (lead-quality + lead-security + lead-integration)
judges individual pull requests `ready | blocked | needs_human_review`; and
the aggregation repo's `merge-master-approval.yml` +
`merge-approval-envelope.yml` is a mechanical GitHub-App operator that
consumes a signed, identity-bound council-verdict check-run
(`council-verdict/merge-readiness`, App 4397053) and, when the low-risk
envelope clears, mints a dedicated merge-master App token — never
`GITHUB_TOKEN` — and posts a real `APPROVE` review as `codexfactory[bot]`.
This is not a design sketch: fully autonomous council deliberation ran
2026-08-14 — three seats, written rationales, unanimous READY, a signed
check-run, a real GitHub approval (records in
`xFactories/codexFactory/hermes/domain/review-councils/records/`, proven on
xFactory PRs #85 and #100).

**The gap is that the candidate class is rules-as-code-limited to almost
nothing.** The one entry in `.github/merge-approval-envelope.yml`
(`doc-health-nightly`) matches only `expected_author: openxfactory[bot]`,
`expected_head_ref: doc-health/nightly`, `path_allowlist: [health/**]`, and
`target_repos: [opensoft/xFactory]`. The one council-clearable condition is
`docs_only_path_overflow`. No human-authored PR, no other agent-authored PR,
and no repo other than the aggregation repo itself can ever receive a
council-cleared approval — and openxFactory, the repo carrying the neutral
contracts this whole family depends on, has no merge-master workflow and no
persona/council instantiation of its own at all.

This proposal generalizes the proven machinery: extend the council + Merge
Master pattern so substantive PRs — human- and agent-authored, across
governed xFactory repos — can receive a team-member-equivalent, accountable,
policy-and-best-practices review from Hermes-stack personas, replacing
`--admin` bypasses without ever letting the mechanical enforcer originate a
judgment it does not already hold as a verdict.

## Decided principles (encoded as requirements; not reopened by this change)

1. **Councils judge; Merge Master stays the mechanical enforcer.** The
   generalization adds candidate classes and council scope — it never moves
   judgment into the enforcer.
2. **Accountability is the product.** Every seat produces a written
   rationale; the verdict transports as a signed, identity-bound check-run;
   an audit artifact records inputs, rules version, and verdicts; the
   approving review is cast by a dedicated reviewer/merge-master App
   identity, never `GITHUB_TOKEN`, never the author's identity.
3. **Identity separation.** The reviewing council and enforcing identity
   must be distinct from the PR author's identity (human or agent); review
   rules always evaluate from the base branch.
4. **Fail-closed.** Anything outside a defined candidate class, any
   non-unanimous or conditioned verdict, any stale/missing rule set → no
   approval, park with explanation; `needs_human_review` escalation is
   always available and some classes may be declared human-only by the
   gate-rules council.
5. **Substantive candidate classes.** The `gate_rules_council` (which
   includes the tenant company-policy-lead seat) defines per-repo candidate
   classes covering substantive human- and agent-authored PRs, each with a
   risk tier and a clearance rule — the council reviews for company-policy
   compliance AND domain best practices.
6. **Pilot.** `opensoft/openxFactory` is reviewed by codexFactory's councils
   — not because the pilot happens to be an engineering-contracts repo, but
   on the ground Brett ruled for every repo (Q2, 2026-08-22): a pull
   request's diff is software regardless of the domain the repository
   governs, so codexFactory's councils review substantive PRs in all
   governed repos — then extended per adoption. *(The original parenthetical
   here read "the software-engineering domain reviewing the
   engineering-contracts repo" — a domain-match rationale that would have
   made the pilot a special case and non-engineering repos an open question.
   That rationale is exactly what the Q2 ruling overrode, so it is corrected
   rather than left standing under a "not reopened" heading.)*

## What Changes

- **`roles-authority-model` (ADDED requirements)** — ten new requirements
  generalizing the existing "Low-risk enforcement envelope" and "GitHub App
  identity tiers" requirements into a named substantive review lane. Six
  carry the decided principles above: authority generalization,
  gate-rules-council-defined candidate classes, accountability (rationale +
  signed check-run + audit artifact + dedicated identity), reviewer/enforcer
  identity separation from the author, fail-closed envelope generalization,
  and the pilot repository/reviewing domain declaration. Four more encode
  Brett's 2026-08-22 rulings on the previously open questions: adoption
  beyond the pilot qualifies on recorded evidence (Q1), company-policy seat
  participation in per-PR councils (Q3), the ruleset interaction shape (Q4),
  and the constitutional floor for autonomous clearance (Q5); the Q2 ruling
  is encoded by rewriting the pilot requirement's persona-home clause rather
  than by adding a requirement. See `design.md` for why
  `roles-authority-model` is the target rather than `workflow-gate-contract`
  or a new capability.
- **Downstream realization (named, not performed by this change; tracked in
  `tasks.md`)**:
  - codexFactory's `gate-rules.yaml` gains a `risk_tier` and `clearance_rule`
    field per candidate class, and its `gate_rules_council` record for
    `opensoft/openxFactory` names the pilot's substantive candidate classes.
  - codexFactory's `merge-readiness.yaml` gains the Q3 conditional pull-in:
    an optional `company-policy-lead` seat with a per-class `when:` condition,
    mirroring `gate-rules.yaml`'s existing
    `client-security-compliance-officer` / `rule_touches_security_posture`
    conjunction, under the file's existing `missing_required_seat: refused`
    fail-closed rule.
  - The aggregation repo's `merge-master-approval.yml` and
    `merge-approval-envelope.yml` generalize their single-candidate,
    single-repo matching to a candidate-class list keyed by
    `(repo, author-shape, path/diff-shape, risk_tier)`, with the
    council-verdict transport and anti-spoofing binding unchanged.
  - `opensoft/openxFactory` gets its own ruleset wiring in the Q4-decided
    shape (the merge-master App's real `APPROVE` review satisfying its
    required-review rule; the council-verdict check-run never a satisfier;
    human review still an always-available alternate path) and its own
    workflow instance, since `pull_request_target` events fire in the repo
    the PR is opened against.
  - A `gate_rules_council` record and, on first live candidate, a
    `merge_readiness_council` record for an `opensoft/openxFactory` PR,
    mirroring the 2026-08-14 xFactory precedent.

## Decided questions (ruled by Brett Heap 2026-08-22)

The five questions this proposal declared open on 2026-08-15 were ruled
in-session by Brett Heap on 2026-08-22, against a written recommendation set
built on full recon of this packet, codexFactory's council machinery, the
aggregation repo's merge-master enforcer, and the two proven autonomous
clearances (xFactory PRs #85/#100). Two rulings departed from the
recommendation and are marked. Each ruling below names the requirement that
encodes it; none of them is reopened by this change.

- **Q1 — Rollout order beyond the pilot: DEFERRED TO PILOT EVIDENCE, WITH THE
  BAR RECORDED NOW.** The adoption ORDER beyond the openxFactory pilot is
  decided by a named follow-up change raised on pilot evidence, through the
  one-change-per-repo mechanism the "Pilot repository and reviewing domain"
  requirement already carries. The EVIDENCE BAR is decided now: the pilot
  qualifies a next adoption only after ≥3 council-cleared substantive PRs
  spanning ≥2 candidate classes, zero enforcer incidents, and one completed
  gate-rules review cycle. The ordering principle is decided now too:
  engineering-owned repos before domain repos. *Encoded as the "Adoption
  beyond the pilot qualifies on recorded evidence" requirement. Route: this
  proposal edit for the bar and the principle; a named follow-up change for
  the order itself.*
- **Q2 — Persona home: CODEXFACTORY REVIEWS EVERYTHING** *(Brett overrode the
  recommended two-axis engineering-vs-domain-content split).* codexFactory's
  `gate_rules_council` and `merge_readiness_council` review substantive PRs in
  ALL governed xFactory repos, whatever domain the repo governs — a PR's diff
  is software regardless of the domain. NO domain repo instantiates its own
  review personas or councils for this lane; there are zero new persona homes.
  The tenant `company-policy-lead` seat, cross-layer and domain-independent,
  continues to carry the policy dimension inside codexFactory's councils. The
  per-repo adoption change survives unchanged — what it names is the
  repository, and it affirms codexFactory as the reviewer instead of naming a
  persona home. *Encoded by rewriting the "Pilot repository and reviewing
  domain" requirement's persona-home clause. Route: this proposal edit.*
- **Q3 — Company-policy-lead per-PR seating: CONDITIONAL PULL-IN** *(Brett
  chose a bounded third option over the recommended flat rules-only rule).*
  The DEFAULT stands: the seat is rules-council-only, preserving the
  2026-07-22 permanent rule-setting/rule-applying separation. The EXCEPTION is
  bounded and declared: a candidate class MAY declare a company-policy pull-in
  condition, and a PR matching such a class pulls the `company-policy-lead`
  seat into THAT PR's `merge_readiness_council` convening — the same
  conjunction shape as the existing
  `client-security-compliance-officer` / `rule_touches_security_posture`
  pull-in in codexFactory's `gate-rules.yaml`. The condition is defined PER
  CANDIDATE CLASS by the `gate_rules_council` (where the seat already sits) at
  class-definition time, so the seat itself decides, on the record, which
  classes summon it per-PR. Fail-closed semantics follow the existing
  `missing_required_seat: refused` rule: for a class that declares the
  pull-in, a convening missing the seat is refused and parked. That
  availability cost is accepted, bounded to policy-flagged classes only —
  every other class keeps domain-seats-only per-PR councils. *Encoded as the
  "Company-policy seat participation in per-PR councils" requirement; design.md
  Decision D is superseded in part. Route: this proposal edit.*
- **Q4 — Ruleset interaction shape: THE PROVEN SHAPE, EVERYWHERE.** The
  merge-master App casts a REAL `APPROVE` review and that review satisfies the
  repo's required-review rule. The council-verdict check-run remains verdict
  TRANSPORT only and is never configured as a ruleset-accepted satisfier — the
  workflow's own anti-spoofing analysis is the recorded reason. Human review
  REMAINS an always-available alternate satisfying path on EVERY governed
  repo; no repo's ruleset may be configured App-path-only, because a council
  outage must never block humans. Per-repo divergence from this default, if
  ever wanted, requires its own recorded decision inside that repo's adoption
  change. *Encoded as the "Ruleset interaction shape for the substantive
  review lane" requirement. Route: this proposal edit.*
- **Q5 — Risk tiers: CONSTITUTIONAL FLOOR NOW, VOCABULARY LATER.** Ruled now,
  in three clauses: (i) the ratified never-clearable floor — identity
  mismatch, HEAD-REF mismatch, failed or pending required checks, secret
  findings, security-touching paths, gate-weakening changes — is
  TIER-INDEPENDENT, and no tier, clearance rule, or unanimous verdict ever
  overrides it. (The floor has SIX members. The ruling as put to Brett, and
  the recommendation behind it, both restated it with five — head-ref
  mismatch was dropped somewhere upstream of the ruling. The ratifying record
  is authoritative and lists six: codexFactory
  `hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`
  — "identity, head ref, any failed check, secret findings, security-touching
  paths, gate-weakening changes". Restoring the sixth is FIDELITY to the
  artifact the ruling names, not a new ruling: Brett ruled that "the ratified
  floor" is tier-independent, and the ratified floor is what the record says
  it is. The requirement therefore names the record as the floor's source of
  truth, so a future divergence is caught against the artifact rather than
  against a restated list.) (ii) any
  candidate class touching contract bytes, gate/workflow definitions,
  credential surfaces, or security posture is PERMANENTLY human-only,
  regardless of unanimity; (iii) autonomous clearance is only ever eligible
  for classes whose blast radius is docs- or derived-artifact-shaped, which
  today is exactly the proven docs class. The enumerated, ordered tier
  vocabulary with per-tier clearance eligibility is explicitly DEFERRED to the
  evidence-driven follow-up change — the same follow-up path Q1's rollout
  order takes; they may share one change or come separately. *Encoded as the
  "Constitutional floor for autonomous clearance" requirement, which also
  records the deferral. Route: this proposal edit for the floor; a named
  follow-up change for the vocabulary.*

## Capabilities

### Modified Capabilities

- `roles-authority-model`: ten ADDED requirements generalizing the
  substantive-review authority, accountability, identity-separation, and
  fail-closed envelope machinery already partially present (Merge Master's
  low-risk envelope, GitHub App identity tiers) into a named, extensible
  lane, plus a declared pilot, the evidence bar and ordering principle for
  adoption beyond it, the company-policy seat's default and its declared
  per-class pull-in exception, the standing ruleset interaction shape, and
  the constitutional floor for autonomous clearance.

## Impact

- No change to any `contracts/schemas/` artifact, `contracts/manifest.yaml`,
  or `contracts/CHANGELOG.md` — this is a roles-authority-model spec delta
  plus cross-repo rules-as-code realization, not a neutral contract bundle
  release.
- No existing candidate class, workflow, or council record is removed or
  altered by this change; `doc-health-nightly` / `docs_only_path_overflow`
  continues operating exactly as proven 2026-08-14.
- Downstream realization touches three repos (xFactory aggregation,
  codexFactory, openxFactory) and is tracked, not performed, by this change
  — see `tasks.md` §3–§5, each task marked as its own successor realization
  step with archive-on-evidence discipline per `release-realization`.
- No `--admin` bypass is removed by this proposal; it is a precondition
  (the substantive review lane existing and being wired for a given repo)
  for later retiring bypass usage on that repo, which is out of scope here.

## Out of scope, deliberately

- Two residues of the 2026-08-22 rulings, both deliberately deferred to a
  named follow-up change raised on pilot evidence (they may share one change
  or come separately): the adoption ORDER beyond the pilot (Q1 — the evidence
  bar and the engineering-before-domain ordering principle ARE decided here;
  which repo is actually next is not), and the enumerated, ordered risk-tier
  VOCABULARY with per-tier clearance eligibility (Q5 — the constitutional
  floor IS decided here; the tier names are not). The other three questions —
  the persona home, company-policy-lead per-PR seating, and the per-repo
  ruleset interaction shape — are decided in full above and are not
  reopened.
- Retiring any existing `--admin` bypass usage on any repo — this proposal
  only makes a governed alternative available; removing bypass access is a
  separate, per-repo policy decision.
- Any change to the council-verdict transport mechanism itself (the signed
  `council-verdict/merge-readiness` check-run, its anti-spoofing App-identity
  binding, or the merge-master token-minting flow) — the proven transport is
  reused as-is; see `design.md` Decision C.
- Non-GitHub enforcement surfaces (client-tenant infrastructure) — this
  lane governs Opensoft's own vendor build org only, consistent with the
  existing "GitHub App identity tiers" requirement's scope.
