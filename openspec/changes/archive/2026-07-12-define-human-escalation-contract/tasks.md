# Tasks — Define Human Escalation Contract

## 1. Decisions

- [x] 1.1 Resolve OQ1 with Brett: tenant-contractual interrupt class in the neutral set, or left to tenant policy (draft position: tenant policy may add classes; neutral set stays minimal) — resolved by 2026-07-12 ratification: drafted position stands

## 2. Neutral contract text

- [x] 2.1 Add the "Human Escalation Contract" section to `docs/roles-and-authority.md`: the route/park/interrupt ladder, the conjunctive containment-failure test, the enumerated interrupt classes, the non-interrupt list, and the cite-the-class audit rule
- [x] 2.2 Add the parked-decision delivery rules (decision-ready packet fields, root-cause dedupe, fail-closed silence semantics)
- [x] 2.3 Define the low-risk enforcement envelope and rewrite the Merge Master text in "External Enforcement Authority" to reference it (replacing "low-risk"/"medium/high-risk"/"risky" adjectives with the envelope conditions)
- [x] 2.4 Rewrite the "Escalation Boundaries" bullet list to reference the ladder and drop the circular "human-review requirements" trigger

## 3. Validation and records

- [x] 3.1 Run `OPENSPEC_TELEMETRY=0 openspec validate define-human-escalation-contract --strict` and `--all --strict`
- [x] 3.2 List this change in openxFactory README's "OpenSpec Records" block as active
- [x] 3.3 On ratification, mark `docs/roles-and-authority.md` with `Ratified by:` per the document lifecycle

## 4. Domain follow-through (codexFactory, after ratification)

- [x] 4.1 Replace `` `HR` when present `` in `codexFactory/docs/engineering-roles-and-authority.md:43` with a reference to the escalation ladder (merge approvals outside the envelope park at the merge gate)
- [x] 4.2 Add engineering examples of the interrupt classes to the same doc in GitHub terms (live token exposure beyond agent revocation; active unauthorized repo access; in-flight irreversible external action such as a published package or triggered deployment that no agent may halt)
- [x] 4.3 Confirm `omnigent/domain-overlay.yaml` routing and stop conditions conform (routes go to agent authorities; stop conditions block); add a conformance note referencing the ladder
- [x] 4.4 Record the candidate follow-up: dangling-consultation-identifier lint in codexFactory's conformance gate (OQ2), and interrupt-audit / parked-queue-aging as future doc-health family candidates
- [x] 4.5 Encode the structural parking gates in GitHub: branch protection/ruleset requiring review, CODEOWNERS scoping the human-gated surfaces (`stack.yaml`, `credentials/`, `.github/workflows/`, governance `docs/`) to the named human, and environment required reviewers for deploy/production jobs; document the mapping in `docs/pr-admission-merge-readiness.md` (repo-side artifacts landed: CODEOWNERS + §7a; ruleset/environment settings are admin deployment config, documented, pending push)
- [x] 4.6 Define the Merge Master GitHub identity path (bot/App account listed as owner for non-human-gated surfaces) so the low-risk lane can satisfy review requirements without weakening the human gates; record as a follow-up if deployment is not yet ready

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 5 and 6, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (a), an explicit ratification act named on the record: this change's own tasks.md 1.1, "resolved by 2026-07-12 ratification: drafted position stands". No ratifier is named in prose, so the date only is recorded. The three-way floor is cleared on the DATE axis, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
