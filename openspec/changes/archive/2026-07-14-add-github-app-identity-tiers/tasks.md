## 1. Spec and validation

- [x] 1.1 Verify the `roles-authority-model` delta spec at `specs/roles-authority-model/spec.md` — the `MODIFIED` block reproduces the full existing "Structural parking in external enforcement" requirement plus its new scenario, and the `ADDED` block's two new requirements each have at least one scenario, exactly four `####` hashtags.
- [x] 1.2 Run `OPENSPEC_TELEMETRY=0 openspec validate add-github-app-identity-tiers --strict` and fix any reported issues.
- [x] 1.3 Run `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` to confirm this change does not break any other change's or spec's strict validation.

## 2. Neutral doc update

- [x] 2.1 Update `docs/roles-and-authority.md` to describe the content-vs-administration App identity tiers and the administration-tier credential-custody obligation, consistent with the ratified spec delta (do not restate domain-specific execution roles or examples — those stay in the owning DomainxFactory per the existing "Neutral authority model ownership" requirement).
- [x] 2.2 Cross-reference `docs/credential-access-model.md` from the new doc content rather than duplicating the credential-contracts shape description.

## 3. Ratification and realization evidence

- [x] 3.1 Obtain Brett's ratify-gate approval for this change (the underlying design questions are already ratified per `ideation/staging/github-administration-plane/multi-app-identity-and-github-administration.md`; this task is the formal OpenSpec ratify step for the change itself).
- [x] 3.2 On ratification, add `Status: ratified` and `Ratified by: add-github-app-identity-tiers` to `docs/roles-and-authority.md`'s header per the document-lifecycle convention.
- [x] 3.3 Add this change to the openxFactory README's "OpenSpec Records" block.
- [x] 3.4 Archive this change once realized (code_surface: none, so archive follows straight from merge — no external realization evidence gate applies). Archived as `2026-07-14-add-github-app-identity-tiers`; 2 requirements added, 1 modified, folded into `openspec/specs/roles-authority-model/spec.md`.

## 4. Handoff to the sibling change

- [x] 4.1 Once this change is ratified, draft the sibling OpsxFactory-local `github-administration` change, instantiating the App-identity tiers defined here as an actual second GitHub App, a dedicated write workflow, and concrete credential records for Opensoft's own vendor org. Drafted as `add-github-administration-workflow` in OpsxFactory (4/4 artifacts, strict-valid); implementation in progress.
- [x] 4.2 Update the `github-administration-plane` staging topic's Exit section to record this change's landed ID once merged.

## Bookkeeping correction (2026-08-23, `govern-openspec-corpus-membership`)

`proposal.md` gained TWO header lines in one edit — `Status: ratified` and a single `Ratified:` citation, at real lines 3 and 4, both well inside the fifteen-real-line header window. Nothing else on the page moved: the writer asserted per file that deleting exactly those two lines recovers the original bytes, and refused to write otherwise. The ruling is OQ-6's of 2026-08-23 (Brett Heap, in-session multiple-choice round), which DEPARTED from its own recommendation — no grandfather, no contract date, no reduced-severity class — and backfills every headerless proposal from its OWN record, stopping and reporting rather than inventing where a record cannot carry one. The status and the citation are coupled because the promoted rule in `openspec/specs/document-lifecycle/spec.md` holds that a bare, uncited `Status: ratified` is a violation whatever else the document says.

This document's citation takes derivation route (a), an explicit ratification act named on the record: the archive commit `1e10742`, whose body opens "Ratified 2026-07-14", together with this change's own tasks.md 3.1 under its "## 3. Ratification and realization evidence" heading, which calls itself "the formal OpenSpec ratify step for the change itself". The three-way floor is cleared on the APPROVER axis, the DATE axis and a resolvable RECORD PATH, measured through `doc_health.families` before the line was written, not assumed.

It is entered in `docs/archive-record-discrepancies.md` as C2's successor. This note travels with the change, as 5B's twenty-seven do.
