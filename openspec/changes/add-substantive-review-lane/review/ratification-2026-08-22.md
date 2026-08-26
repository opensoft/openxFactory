# Proposal Ratification: add-substantive-review-lane

Status: ratified
Decision date: 2026-08-22
Ratifier: Brett Heap (repository owner) — in-session via question prompts
Ratified: 2026-08-22 by Brett Heap (repository owner) — in-session via question prompts
Ratified baseline: this change as committed in the ratification commit
carrying this record (proposal.md, design.md, tasks.md,
specs/roles-authority-model/spec.md, .openspec.yaml — ten ADDED requirements,
validated `--strict` and `--all --strict`, 67/67 across 18 changes and 49
specs).

## Decision

Brett ratified the substantive review lane: the generalization of
codexFactory's proven `gate_rules_council` + `merge_readiness_council` + Merge
Master machinery, beyond its one rules-as-code candidate class, into a named
lane under which governed councils review substantive human- and
agent-authored pull requests across governed xFactory repos, with Merge Master
remaining the mechanical enforcer.

This ratification authorizes the downstream realization named in tasks §3–§5
(codexFactory council/gate-rules instantiation, aggregation workflow and
envelope generalization, pilot-repo wiring and records). It lands no workflow,
no council edit, and no ruleset change by itself, and it moves no contract
bytes — `target_release: none`.

## Provenance: two distinct rounds, one day

Both rounds are Brett's, both on 2026-08-22, both in-session via question
prompts, and they are NOT the same act:

1. **The clarify round (earlier).** The five questions this proposal declared
   open on 2026-08-15 — rollout order, persona home, company-policy-lead
   per-PR seating, per-repo ruleset shape, risk-tier taxonomy — were ruled.
   Two rulings departed from the written recommendation: **Q2** (Brett
   overrode the two-axis engineering/domain-content split — codexFactory
   reviews every governed repo, zero new persona homes) and **Q3** (Brett
   chose a bounded conditional pull-in over flat rules-only). Those rulings
   are recorded per-question in `proposal.md`'s "Decided questions" section,
   encoded as requirement text, and reflected in `design.md` Decisions B–F.
   Their staging provenance is the now-retired
   `substantive-review-lane-questions` topic, whose exit record lives in
   `ideation/staging/INDEX.md`.
2. **The ratification read (this record).** Four read-items put to Brett after
   an adversarial fidelity review of the encoding. Ruled below.

## What was ratified at the read — the four items

1. **FORM ELEVATION — ACCEPTED.** Brett's Q1 and Q5 rulings said the evidence
   bar and the constitutional floor were to be recorded "in the proposal" /
   "as proposal text". They were encoded instead as PROMOTED REQUIREMENTS, and
   the change flagged that elevation rather than performing it silently: a
   floor that outranks every unanimous verdict must be checkable, and a bar
   whose whole job is to gate a FUTURE adoption change cannot live in prose
   that disappears at archive. Brett accepted the elevation. Both stay
   requirements. Recorded in `design.md` Decisions B and E.
2. **Q1 BAR COUNTING RULE — ANY COUNCIL-CLEARED VERDICT COUNTS.** This
   OVERRODE the encoder's reading. A unanimous `merge_readiness_council`
   verdict counts toward the ≥3 bar whether the approving review was then cast
   by the merge-master App or by a human. The bar measures COUNCIL QUALITY,
   not enforcer autonomy — a council that deliberated well and whose verdict a
   human executed is exactly the evidence the bar exists to collect. The
   earlier encoding said "only the autonomous ones count toward the Q1
   evidence bar" (tasks §5.2) and that clause is replaced. Encoded in the
   "Adoption beyond the pilot qualifies on recorded evidence" requirement, its
   "A human-approved council-cleared pull request still counts" scenario,
   `design.md` Decision G, and tasks §5.2.
3. **ORDERING PRINCIPLE — STAYS ABSOLUTE.** The literal consequence was put to
   Brett before he ruled: read flat, "engineering-owned repos before domain
   repos" means a DORMANT engineering-owned repository — one nobody is
   proposing, with no adoption work under way — blocks every domain
   repository's adoption indefinitely, simply by remaining unadopted. Two
   softenings were offered (a recorded-waiver clause; scoping the block to
   actively-maintained engineering repos) and Brett declined BOTH. The escape
   path, when genuinely needed, is a direct escalation to Brett inside the
   future adoption change that needs it — a human decision made in the open —
   not requirement text that lets the order be routed around quietly.
   Recorded in `design.md` Decision E.
4. **RATIFY.** The requirement set is ratified as it stands at this record's
   commit.

## Pre-ratification review

An adversarial fidelity review of the encoding ran before the read. Q2, Q4,
and Q5's clauses (ii) and (iii) were confirmed FAITHFUL to the rulings. Two
blocking items and six should-fixes were taken in one pass before ratification
(commit `53f181ef`):

- **B1** — the constitutional floor was enumerated one member SHORT of the
  ratified record it names. codexFactory
  `hermes/domain/review-councils/records/2026-07-23-gate-rules-nightly-sweep-clearance.md`
  records SIX members; HEAD-REF MISMATCH was missing, dropped upstream in the
  recommendation and the ruling summary. Restored, and that record is now
  named in the requirement as the floor's SOURCE OF TRUTH, with the restated
  enumeration explicitly subordinate to it.
- **B2** — Q1's ordering principle had drifted into a two-candidate tie-break
  with a departure hatch. Reverted to the ruled flat form (see item 3 above).
- **S1** — Q3's pull-in granularity resolved to CONDITION-HOLDS on Brett's own
  option text ("a defined per-PR pull-in condition"), with the
  declared-but-not-holding case given its own scenario.
- **S2** — principle 6's overridden two-axis parenthetical corrected. **S3** —
  the form elevation surfaced for this read. **S4** — the codexFactory
  "PERMANENTLY DISTINCT" header amendment assigned to tasks §3.3. **S5** — the
  rulings' interaction squeeze recorded as Decision G.
- Notes: the ADMIT mapping's third conjunct added
  (`undispositioned_conditions == 0`); tasks §4.5's "one key read two ways"
  corrected to a naming hazard after verifying `rule.repository` is never read
  in the decision path; Q4's opening reworded so it obliges nothing to be
  approved.

Copilot's substantive finding on PR #178 — Requirement 5 saying "unanimous
ADMIT" while the enforcer checks `ready`+unanimous — was closed before the
read by adding an explicit layer-mapping sentence and scenario rather than by
swapping the neutral word for the enforcement word.

## Conscious-acceptance notes (Brett, at ratification)

1. **The pilot's autonomous surface is narrow, by construction.** Q5 (ii) +
   (iii) plus the exact-string head-ref matcher confine the first
   autonomously clearable class to docs-shaped AND fixed-branch space. Brett
   ratifies with that in view; item 2 above is what keeps it from also
   slowing the evidence bar. Full analysis in `design.md` Decision G.
2. **Q2's residual risk is accepted, not solved.** For a domain repo whose PR
   content is domain governance rather than software, codexFactory's councils
   review material outside their domain expertise. Mitigations are
   `needs_human_review` at every class, the gate-rules council's human-only
   power, and the Q5 floor. `design.md` Decision F.
3. **Q3 leaves a live inconsistency in codexFactory.** Both council files
   still mark the rule-setting/rule-applying separation "PERMANENTLY DISTINCT"
   (decided 2026-07-22); the bounded exception bends that. Discharging it is
   assigned to tasks §3.3, in the same codexFactory change that adds the
   conditional seat. Until that runs, the wording stands unamended.
4. **Two residues remain deliberately deferred** to a named follow-up change
   raised on pilot evidence, and may share one change or come separately: the
   adoption ORDER beyond the pilot (Q1), and the enumerated, ordered risk-tier
   VOCABULARY with per-tier clearance eligibility (Q5).

## Next

Realization, all post-ratification and all tracked, not performed, by this
change: codexFactory's gate-rules `risk_tier` / `clearance_rule` fields, the
Q3 conditional seat plus the "PERMANENTLY DISTINCT" amendment, and the pilot's
`gate_rules_council` record (§3); the aggregation envelope and workflow
generalization, including the head-ref matcher work and the `rule.repository`
semantics pin (§4); and openxFactory's own workflow instance, ruleset wiring
in the Q4-decided shape, and first live candidate (§5). Archive follows
`release-realization` discipline on that evidence.
