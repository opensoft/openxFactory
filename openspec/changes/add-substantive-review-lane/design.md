# Design: add-substantive-review-lane

## Decision A — Spec home is `roles-authority-model`, not `workflow-gate-contract`, and not a new capability

Considered three homes for the ADDED requirements:

1. **`roles-authority-model`.** Already owns the Hermes-level governance
   roles ("merge readiness and merge authority"), the Merge Master
   autonomous-approval envelope ("Low-risk enforcement envelope" —
   critically, its body already reads "any policy-required **governed
   review verdict** is ADMIT with no undispositioned conditions", so a
   generalized council verdict was already anticipated, just never defined),
   and the two-tier GitHub App identity model
   (`add-github-app-identity-tiers`, 2026-07-14) that the client-tenant
   liaison change later extended in place with a MODIFIED requirement
   rather than a new capability. This is precedent for exactly the move
   this proposal makes: generalize an existing roles-authority-model
   requirement by adding sibling requirements next to it.
2. **`workflow-gate-contract`.** Owns the neutral **domain workflow
   contract** schema (`contracts/schemas/xfactory-workflow.schema.yaml`) and
   its `gates[]`/`owner_layer` vocabulary — DTN-001/002 promoted content.
   That schema governs `workflows/*.yaml` files domains author for their
   OWN internal workflow gates (Adx campaign-intake, Ledgerx client-intake,
   Medx decision-foundation-loop, codex branch-review). The council +
   Merge Master + GitHub ruleset machinery this proposal generalizes is a
   different mechanism entirely — it is not expressed as a
   `workflow_contract` `gates[]` entry anywhere today, and forcing it into
   that schema would conflate "a domain's own internal gate" with "GitHub's
   external branch-protection enforcement," which `roles-authority-model`
   already treats as a distinct, later-enforcement layer ("Structural
   parking in external enforcement", "GitHub App identity tiers"). Rejected.
3. **A new `substantive-review-lane` capability.** Considered because the
   candidate-class/council/verdict-transport mechanism is genuinely more
   machinery than a typical roles-authority-model requirement describes.
   Rejected for now: every concept this proposal needs already has a home
   in `roles-authority-model` (Merge Master, the low-risk envelope, GitHub
   App identity tiers, human-attention escalation), and splitting it into a
   second capability would force cross-capability requirement references
   for what is fundamentally one authority model extended by a single
   requirement set (six as authored 2026-08-15, ten after the 2026-08-22
   rulings added four). If a later change adds enough NEW machinery (e.g. a
   full candidate-class schema family with its own validator, packaged
   examples, and manifest entry — the "neutral contract realization
   pattern" `add-client-identity-roster` used), promoting a dedicated
   capability at that point remains open and is not foreclosed here.

**Adopted: (1), `roles-authority-model`, ADDED requirements.** Flagged
explicitly in this change's report for orchestrator review, since it is the
single structural judgment call this proposal makes without an open
question wrapped around it.

## Decision B — Candidate-class model: declare-only risk tier and clearance rule, not a taxonomy

The existing `.github/merge-approval-envelope.yml` `candidates: []` list has
exactly one entry (`doc-health-nightly`) with no risk-tier or clearance-rule
field at all — the single candidate class both defines the risk implicitly
(bot-authored, append-only, revert-suffices) and IS the clearance rule
(`docs_only_path_overflow` council-clearable, everything else the tier-1
deterministic envelope alone). Generalizing to many classes across many
repos needs those two concerns named explicitly, but this proposal does not
enumerate the vocabulary:

- **Option 1 — enumerate the risk-tier vocabulary now** (e.g.
  `docs_only | config | contract | runtime_code`) directly in the
  `roles-authority-model` requirement text. Rejected: premature. The one
  real candidate class in production is docs-only; inventing the other
  tiers' names and which are ever autonomous-eligible before a second real
  class exists risks the same "unfalsifiable, re-slice until conformant"
  failure the `add-client-identity-roster` cross-model review found in that
  proposal's first draft. Declared as an open question instead.
- **Option 2 — require presence, not vocabulary** (adopted): every
  candidate class MUST declare A risk tier and A clearance rule (some
  string the `gate_rules_council` record names and the enforcer reads), but
  the taxonomy of tier names and which tiers may ever clear autonomously is
  left to the `gate_rules_council`'s own per-repo record until a follow-on
  change (or accumulated repo precedent) promotes a shared vocabulary. This
  mirrors how `workflow-gate-contract`'s "Owner layer constraint"
  requirement accepts either canonical role names or a domain's own
  `stack.yaml`-declared layer id — presence and validity, not a closed
  enumeration, at the neutral layer.

**AMENDED 2026-08-22 by Brett's Q5 ruling.** Option 2 stands: the tier
VOCABULARY is still not enumerated, and its deferral is now explicit rather
than merely "open" — the enumerated, ordered vocabulary with per-tier
clearance eligibility goes to a named follow-up change raised on pilot
evidence. What the ruling adds on top of Option 2 is a CONSTITUTIONAL FLOOR
that does not wait for the vocabulary, because it is expressible without one:
the ratified never-clearable conditions are tier-independent and unoverridable
by any tier, clearance rule, or unanimous verdict; classes touching contract
bytes, gate/workflow definitions, credential surfaces, or security posture are
permanently human-only; and autonomous clearance is eligible only for
docs-/derived-artifact-shaped blast radii, which today is exactly the proven
docs class. This is the omnigent permission matrix's constitutional-false
precedent applied to clearance: a "never, regardless of verdict" band can be
fixed before the graded band above it is named, and fixing it first is what
keeps the deferral safe rather than merely convenient. Encoded as the
"Constitutional floor for autonomous clearance" requirement.

## Decision C — Approval-transport: reuse the proven check-run + APPROVE pattern unchanged

Considered redesigning the verdict transport for the generalized lane (for
example, a required *check* the ruleset itself requires, rather than a
required *review* the App satisfies). Rejected: the current transport
(`council-verdict/merge-readiness` check-run, App-identity-bound per
`vars.COUNCIL_LANE_APP_ID` so a forged same-name check-run from a lesser
App cannot buy an approval, then a real `APPROVE` review cast with a
dedicated merge-master App token) is proven live with an adversarial-review
pass already closed (the anti-spoofing binding exists BECAUSE an earlier
review round found the forgery gap). Reinventing transport for the
generalized lane would re-open a solved problem for no stated gain. Adopted:
every new candidate class consumes the SAME transport; what generalizes is
the candidate-matching logic (author/head/path/repo shape) and which repos'
councils are authorized to emit it, not the check-run/review mechanism
itself. The per-repo *ruleset interaction shape* (does the App's review
satisfy a required-reviewer rule, or does the repo instead require the
check-run directly) was left as a declared open question here, because it is
a per-repo GitHub configuration choice, not a transport-mechanism choice.

**AMENDED 2026-08-22 by Brett's Q4 ruling — the shape is no longer open.** The
proven shape becomes the STANDING DEFAULT for every governed repo, not a
per-repo choice made from scratch: the App casts a real `APPROVE` review and
that review is what satisfies the required-review rule; the check-run stays
verdict transport and is NEVER configured as a ruleset-accepted satisfier
(this decision's own anti-spoofing analysis is the recorded reason — making
the transport a satisfier would re-open exactly the forgery gap the
`COUNCIL_LANE_APP_ID` binding was added to close); and human review remains an
always-available alternate satisfying path on every repo, so no repo may be
wired App-path-only and a council outage can never block humans. Per-repo
divergence stays possible but is now an exception that must be recorded as its
own decision inside that repo's adoption change, rather than a blank the
adoption change fills in silently. Encoded as the "Ruleset interaction shape
for the substantive review lane" requirement.

## Decision D — Company-policy-lead seat stays rules-only for this proposal — SUPERSEDED IN PART 2026-08-22

**Reading order.** The paragraph below is the decision as authored 2026-08-15
and is kept verbatim, because its defense of the rules-only posture is still
the reason that posture is the DEFAULT. What it no longer holds is its last
clause — that per-PR seating is "left as a declared open question". Brett
ruled Q3 on 2026-08-22 and the ruling is recorded immediately after it.

`gate_rules_council` already seats `company-policy-lead` (tenant layer) for
RULE-SETTING; `merge_readiness_council` seats only domain personas
(lead-quality, lead-security, lead-integration) for PER-PR judgment — a
distinction the codexFactory council files mark "PERMANENTLY DISTINCT... a
body that sets the rules must not also apply them." This proposal's
"Substantive candidate classes" requirement satisfies decided principle 5
("the council reviews for company-policy compliance AND domain best
practices") by requiring the company-policy-lead seat's compliance rationale
at CLASS-DEFINITION time, not at every individual PR's review time. Whether
that seat should ALSO join `merge_readiness_council` per-PR deliberation —
which would blur the rule-setting/rule-applying separation the councils were
explicitly designed to preserve — is left as a declared open question rather
than decided here, because it is a seat-composition change to an already
proven-live council, not a pure additive extension.

**SUPERSEDING RULING (Brett Heap, 2026-08-22) — the default survives, a
bounded exception is added.** Brett declined both flat answers. Rules-only
remains the DEFAULT posture and the 2026-07-22 permanent separation stands
for every class that says nothing; what is added is a per-class, declared
EXCEPTION. A candidate class MAY declare a company-policy pull-in condition,
and a PR matching such a class pulls the `company-policy-lead` seat into THAT
PR's `merge_readiness_council` convening.

Three properties are what make this narrower than the option this decision
rejected, and they are the reason it is adoptable without re-litigating
2026-07-22:

1. **It reuses a shape the councils already run**, rather than inventing one.
   `gate-rules.yaml` already seats `client-security-compliance-officer` with
   `when: rule_touches_security_posture` — a conditional seat pulled in by a
   declared trigger. Q3 is the same mechanism aimed at a different council and
   a policy trigger.
2. **The seat itself sets its own summons, on the record.** The pull-in
   condition is defined PER CANDIDATE CLASS by the `gate_rules_council` — the
   body the `company-policy-lead` seat already sits in — at class-definition
   time, never per pull request. So the rule-setting act stays in the
   rule-setting body; only the rule-APPLYING act reaches per-PR, and only for
   classes the rule-setting body itself flagged. The separation is bent at a
   declared, recorded point rather than dissolved.
3. **The availability cost is bounded and priced.** `missing_required_seat:
   refused` means a convening that cannot seat a required seat is refused and
   parked — so for a pull-in class, tenant-seat unavailability parks the PR.
   This decision's original objection (adding a tenant-availability failure
   mode to EVERY PR) is answered by scope: only policy-flagged classes carry
   it; every other class keeps domain-seats-only per-PR councils. Brett
   accepted that cost explicitly for the flagged classes.

Encoded as the "Company-policy seat participation in per-PR councils"
requirement, whose default clause and exception clause map one-to-one onto
this decision's surviving half and its superseding half.

## Decision E — Pilot scope is one repo before any rollout ordering

`opensoft/openxFactory` is named as the sole pilot (decided principle 6)
rather than proposing a rollout wave, because: it is the repo carrying the
neutral contracts every domain factory consumes (so a defect in the review
lane here is caught before it propagates), it currently has NO merge-master
workflow or persona/council instantiation at all (a clean generalization
test, not a migration), and codexFactory's councils are the only ones proven
live end-to-end (2026-08-14). Rollout order beyond the pilot is left open
rather than sequenced here, because sequencing depends on the still-open
"persona home for non-engineering domains" question — proposing an order
before that question resolves would silently presuppose an answer to it.

**AMENDED 2026-08-22 by Brett's Q1 and Q2 rulings.** The stated reason for
leaving the order open is now discharged: Q2 answered the persona-home
question (codexFactory reviews every governed repo), so an order no longer
presupposes anything about who reviews. The order is nonetheless STILL not
sequenced here — but for a different and narrower reason, which the ruling
makes explicit: it is now deferred on EVIDENCE rather than on an unresolved
dependency. What is decided now is the bar the pilot must clear before any
next adoption (≥3 council-cleared substantive PRs spanning ≥2 candidate
classes, zero enforcer incidents, one completed gate-rules review cycle) and
the ordering principle that applies once repos clear it (engineering-owned
before domain). The order itself lands in a named follow-up change raised on
that evidence — the same follow-up path Q5's tier vocabulary takes. Encoded as
the "Adoption beyond the pilot qualifies on recorded evidence" requirement.

## Decision F — Reviewing persona home: codexFactory reviews every governed repo (Brett Heap, 2026-08-22)

Recorded here because Q2 had no decision entry of its own — it was carried
only as an open question, and Decision E's deferral leaned on it.

The recommendation put to Brett was a TWO-AXIS split: the engineering
dimension of every governed repo's PRs (code, contracts, validators,
workflows) belongs to codexFactory, and the domain-content dimension
(hermes/ overlays, clinical/ledger/ops templates) belongs to the owning
domain, whose adoption change would name and instantiate its own review body
at adoption time. That option was chosen to avoid asserting standing
codexFactory has no claim to: a MedxFactory PR's CONTENT can be medical
governance.

**Brett OVERRODE it.** codexFactory's `gate_rules_council` and
`merge_readiness_council` review substantive PRs in ALL governed xFactory
repos, whatever domain the repo governs, on the ground that a PR's diff is
software regardless of the domain. NO domain repo instantiates review
personas or councils for this lane; zero new persona homes are created. The
policy dimension continues to be carried by the tenant `company-policy-lead`
seat, which is cross-layer and domain-independent and already sits in
codexFactory's `gate_rules_council` (and now, under Decision D's superseding
ruling, may be pulled per-PR for classes that declare it).

What the ruling does NOT do, and the requirement text is careful about it:
it does not delete the adoption-change-per-repo mechanism. Every repo beyond
the pilot still adopts the lane through its own named change. What that
change names changes — the repository, plus an affirmation that codexFactory
is its reviewing body — instead of a per-domain persona home to be stood up.
The persona-home FORK is what is removed, not the per-repo gate.

The residual risk is recorded rather than argued away: for a domain repo
whose PR content is domain governance rather than software, codexFactory's
councils are reviewing material outside their domain expertise. Brett's
ruling accepts that; the mitigations that exist today are the
`needs_human_review` escalation available at every candidate class, the
`gate_rules_council`'s power to declare any class human-only, and the Q5
constitutional floor, which keeps contract bytes, gate/workflow definitions,
credential surfaces, and security posture permanently human-only regardless
of unanimity. A domain repo that needs more than that can record the need in
its own adoption change.
