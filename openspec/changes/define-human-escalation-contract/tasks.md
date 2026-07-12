# Tasks — Define Human Escalation Contract

## 1. Decisions

- [ ] 1.1 Resolve OQ1 with Brett: tenant-contractual interrupt class in the neutral set, or left to tenant policy (draft position: tenant policy may add classes; neutral set stays minimal)

## 2. Neutral contract text

- [ ] 2.1 Add the "Human Escalation Contract" section to `docs/roles-and-authority.md`: the route/park/interrupt ladder, the conjunctive containment-failure test, the enumerated interrupt classes, the non-interrupt list, and the cite-the-class audit rule
- [ ] 2.2 Add the parked-decision delivery rules (decision-ready packet fields, root-cause dedupe, fail-closed silence semantics)
- [ ] 2.3 Define the low-risk enforcement envelope and rewrite the Merge Master text in "External Enforcement Authority" to reference it (replacing "low-risk"/"medium/high-risk"/"risky" adjectives with the envelope conditions)
- [ ] 2.4 Rewrite the "Escalation Boundaries" bullet list to reference the ladder and drop the circular "human-review requirements" trigger

## 3. Validation and records

- [ ] 3.1 Run `OPENSPEC_TELEMETRY=0 openspec validate define-human-escalation-contract --strict` and `--all --strict`
- [ ] 3.2 List this change in openxFactory README's "OpenSpec Records" block as active
- [ ] 3.3 On ratification, mark `docs/roles-and-authority.md` with `Ratified by:` per the document lifecycle

## 4. Domain follow-through (codexFactory, after ratification)

- [ ] 4.1 Replace `` `HR` when present `` in `codexFactory/docs/engineering-roles-and-authority.md:43` with a reference to the escalation ladder (merge approvals outside the envelope park at the merge gate)
- [ ] 4.2 Add engineering examples of the interrupt classes to the same doc in GitHub terms (live token exposure beyond agent revocation; active unauthorized repo access; in-flight irreversible external action such as a published package or triggered deployment that no agent may halt)
- [ ] 4.3 Confirm `omnigent/domain-overlay.yaml` routing and stop conditions conform (routes go to agent authorities; stop conditions block); add a conformance note referencing the ladder
- [ ] 4.4 Record the candidate follow-up: dangling-consultation-identifier lint in codexFactory's conformance gate (OQ2), and interrupt-audit / parked-queue-aging as future doc-health family candidates
- [ ] 4.5 Encode the structural parking gates in GitHub: branch protection/ruleset requiring review, CODEOWNERS scoping the human-gated surfaces (`stack.yaml`, `credentials/`, `.github/workflows/`, governance `docs/`) to the named human, and environment required reviewers for deploy/production jobs; document the mapping in `docs/pr-admission-merge-readiness.md`
- [ ] 4.6 Define the Merge Master GitHub identity path (bot/App account listed as owner for non-human-gated surfaces) so the low-risk lane can satisfy review requirements without weakening the human gates; record as a follow-up if deployment is not yet ready
