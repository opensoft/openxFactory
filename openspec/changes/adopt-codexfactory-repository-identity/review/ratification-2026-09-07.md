# Proposal Ratification: adopt-codexfactory-repository-identity

Status: record

Decision date: 2026-09-07

Ratifier: Brett Heap (convener) — in session, lane `provenance-autonomous-merge`,
recorded on openxFactory PR
[#763](https://github.com/opensoft/openxFactory/pull/763#issuecomment-5576174434)
at **2026-09-07T22:21:44Z**, the comment beginning "RATIFIED
2026-09-07T22:21Z".

## Decision

Brett Heap ruled, verbatim:

> accept all [A] and ratify 763

https://github.com/opensoft/openxFactory/pull/763#issuecomment-5576174434

**It is one sentence doing two acts, and the two are recorded together because
they were given together.** "ratify 763" ratifies THIS packet's text — the
change as committed at the ratified head, below. "accept all [A]" ratifies, in
the same breath, the four dispositions of a DIFFERENT document — the
ideation-split decision sheet
`~/session-prompts/ideation-split-decision-2026-09-07.md` — which is how this
packet's own OQ-3 gets answered. Neither act stands in for the other; both are
named here because both bear on this packet.

**Ratified baseline: this change as committed at the head this word was given
against — `5bfdcf3c06478167bd7509f1576db3528ce4ede1`** (`git rev-parse HEAD`,
run before this record's commit): `proposal.md`, `design.md`, `tasks.md`,
`.openspec.yaml`, and the four-requirement `## ADDED Requirements` delta at
`specs/repository-identity/spec.md`, exactly as authored. No commit landed
between that head and this record.

## What is ratified

- **The proposal as written**, `code_surface`/`target_release`/
  `sequenced_after` front-matter included: the four ADDED requirements on
  `repository-identity` (cryptographic freeze; identity-as-authorization-scope
  re-issuance; disposition-by-rule-plus-recorded-sweep; cross-organization
  reachability), no `MODIFIED` block against any promoted capability, no new
  capability, no check family.
- **The disposition set** — which 123 occurrences across 60 files rename at
  realization, which 78 across 54 are frozen (and why), and which 80 across 36
  are deliberately not swept (other lanes' in-flight packets and
  pre-governance `ideation/`).
- **`design.md`'s measurements and its § 8 open-questions list**, three of
  which this same word moves to RULED, alongside the two already ruled at
  authoring time — see the ledger below.
- **`tasks.md`'s nine groups**, as authored, with no realization box ticked by
  this ratification.

## The rulings ledger

Six open questions were named at authoring. Two were already ruled the same
day as authoring (OQ-1, OQ-2); OQ-5 was ruled in the commit that became this
packet's ratified head. This word rules a fourth — OQ-3 — leaving two open.

| OQ | status | ruling |
| --- | --- | --- |
| OQ-1 | **RULED, VERIFIED** | Add the `codeXfactory` organization to the Opensoft GitHub Enterprise, so codexFactory's reusable workflows stay callable cross-organization while the repository stays private. Verified against the live API: `gh api orgs/codeXfactory --jq .plan.name` reads `enterprise`, `updated_at` **2026-09-07T16:41:04Z**. |
| OQ-2 | **RULED** | Apache-2.0, for both `openxFactory` and `openXwallet`. The `LICENSE` files are a separate lane's code surface, not this packet's; the ordering consequence recorded here is that `LICENSE` at the repository root is a precondition of the openxFactory public flip. Landed: openxFactory [#762](https://github.com/opensoft/openxFactory/pull/762) (merged 2026-09-07T16:16:39Z) and openXwallet [#22](https://github.com/opensoft/openXwallet/pull/22) (merged 2026-09-07T16:00:34Z), both "Add the Apache License 2.0". |
| OQ-3 | **RULED — this word** | Via the ideation-split decision sheet (`~/session-prompts/ideation-split-decision-2026-09-07.md`, ruled the same instant as this comment, "accept all [A]", 2026-09-07T22:21Z): **Q1** — redact the two sensitive files (`staging/notebook-projection-identity/notebook-projection-identity.md` and `staging/INDEX.md` row 73, both carrying Brett's real addresses in cleartext) to role placeholders. **Q2** — editorial split of `staging/treatment-options-engine/treatment-options-engine.md`: the neutral `governed-derived-model` remainder stays in openxFactory, the clinical half moves to MedxSoft/MedxFactory `ideation/staging/treatment-plan-generation/`, cross-linked both ways. **Q3** — delete `staging/campaign-memory-fill-maintenance-mapping/campaign-marketing.md` as stale scaffolding — an AdxFactory-named stub never entered in `INDEX.md`. **Q4** — three receiving pull requests (codexFactory 14 files, MedxFactory 9, LedgerxFactory 1) plus one openxFactory removal pull request that also re-runs the cross-reference bootstrap and updates the README/INDEX pointers, with a NotebookLM sync across all three repositories after landing. This packet's own OQ-3 text — does `ideation/`, `governance/`, `health/`, `experiments/`, `.claude/`, `.codex/` and `.specify/` go public with openxFactory, or move behind a private mirror? — is answered **accept publication**, GATED on the four moves above landing first. |
| OQ-4 | OPEN | GHCR namespace sequencing — whether the bench-image dual-publish window opens before the transfer or after it. Recommendation on record: dual-publish first, per the pattern lane `browser-ui-repair` used. **Not ruled by this word.** |
| OQ-5 | RULED (prior act, carried here) | Exercise the `MIGRATION_PIN` re-point ceremony rather than riding GitHub's redirect — the same recorded shape codexFactory `add-regular-pr-council-clearance` task 5.1 performed: *"[xFactory][OPERATOR] Re-point ceremony … performed on the record, with the prior SHA recorded as the rollback target."* Ruled 2026-09-07 in the commit that is this packet's ratified head; carried here for completeness and not re-ruled by this word. |
| OQ-6 | OPEN | Canonical owner-segment casing (`codeXfactory` vs. the GHCR-lowercased `codexfactory`) and whether that lowercasing consequence is accepted and recorded in the mapping. **Not ruled by this word.** |

## What this ratification does NOT do

- **No realization.** No row is added to `contracts/policies/repository-identity.yaml`,
  no factory-origin identity record is re-issued, no contract bundle is cut,
  and none of the 123 live occurrences is renamed. No box in `tasks.md`
  Groups 1-9 is ticked by this ratification, with one exception: task 0.3 —
  "record the ratification word" — is ticked, because that record is this
  document, a diff landed in the same commit as this ratification, which is
  what lets that one box be ticked under house practice (the same reasoning
  `disposition-codexfactory-declared-renames` task 5.4 used for its own
  ratification-recording box). Task 0.1's text is brought current to name
  OQ-3 among the ruled questions, for the same reason.
- **No merge.** This record is written on the branch, before any merge. Per
  Rule 6 (a change-directory pull request), the landing lane posts
  LANDING/LANDED at merge time; nothing here performs that. The pull request
  is taken out of draft and its body updated to say it is ratified and
  awaiting the merge word — it is not merged by this act.
- **OQ-4 and OQ-6 stay open.** Neither is answered here, and no task gated on
  either may be ticked on the strength of this record.
- **The ideation-split sheet's own execution is a separate, later act.**
  Ruling "accept all [A]" authorizes the four moves; it does not itself write
  the redaction, perform the editorial split, delete the stub, or open the
  three receiving pull requests plus the removal pull request. Each is its
  own act, in its own repository or its own pull request, still owed.
- **The operator ceremony is untouched.** The GitHub transfer, the two
  visibility flips, the aggregation's lockstep commit, the App installations,
  the environment and secret inventory, the container namespace move and the
  SonarCloud rebind remain the runbook's
  (`~/session-prompts/runbook-codexfactory-org-transfer.md`) and are not
  performed or blessed by this ratification.

## Records

- This packet's pull request: openxFactory
  [#763](https://github.com/opensoft/openxFactory/pull/763), branch
  `change/adopt-codexfactory-repository-identity`.
- The ratifying comment: <https://github.com/opensoft/openxFactory/pull/763#issuecomment-5576174434>,
  2026-09-07T22:21:44Z.
- The ideation-split decision sheet ruled in the same word:
  `~/session-prompts/ideation-split-decision-2026-09-07.md` (its own closing
  line: `Rulings: Q1[A] Q2[A] Q3[A] Q4[A] — Brett, "accept all [A]",
  2026-09-07T22:21Z`).
- OQ-1 verification: `gh api orgs/codeXfactory --jq '.plan.name, .updated_at'`
  → `enterprise`, `2026-09-07T16:41:04Z`.
- OQ-2 landings: openxFactory
  [#762](https://github.com/opensoft/openxFactory/pull/762) (merged
  2026-09-07T16:16:39Z), openXwallet
  [#22](https://github.com/opensoft/openXwallet/pull/22) (merged
  2026-09-07T16:00:34Z).
- OQ-5's cited shape: codexFactory `add-regular-pr-council-clearance` task 5.1.
- Sequencing premise re-confirmed at this record's writing: `adopt-medxsoft-repository-identity`
  is still active on `main`, `Status: draft`, still the author of
  `contracts/policies/repository-identity.yaml` at its own task 1.1 — task 0.2's
  premise holds.
