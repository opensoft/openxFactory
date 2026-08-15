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
   for what is fundamentally one authority model extended by six
   requirements. If a later change adds enough NEW machinery (e.g. a
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
check-run directly) is left as a declared open question because it is a
per-repo GitHub configuration choice, not a transport-mechanism choice.

## Decision D — Company-policy-lead seat stays rules-only for this proposal

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
