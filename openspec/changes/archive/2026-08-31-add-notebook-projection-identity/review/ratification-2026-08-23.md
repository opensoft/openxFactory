# Proposal Ratification: add-notebook-projection-identity

Status: ratified
Decision date: 2026-08-23
Ratifier: Brett Heap (repository owner) — in-session via question prompts
Ratified: 2026-08-23 by Brett Heap (repository owner) — in-session via question prompts
Ratified baseline: this change as committed in the ratification commit
carrying this record (proposal.md, design.md, tasks.md, .openspec.yaml,
specs/lifecycle-notebook-projection/spec.md — 3 ADDED and 2 MODIFIED
requirements, specs/credential-contracts/spec.md — 1 MODIFIED requirement),
validated `--strict` and `--all --strict`, 69/69 across 20 changes and 49
specs.

## Decision

Brett ratified the change: the NotebookLM projection's hosting identity
becomes a DECLARED TWO-CASE INTAKE FACT — operator-hosted (a company-owned
Google Workspace USER account in the operating party's own domain) or
self-hosted/personal, both legitimate — with the sync running under the
declared account's `nlm` profile, access shared out FROM that account, each
share act decided by a governed human and RECORDED as the share-out roster
entry itself, and a migration path that re-derives, proves parity against the
corpus scan, and retires the originals by recorded act.

He ruled TWO things in the same read, and they are separate acts:

1. **RATIFY** — the requirement set stands as it is at this record's commit.
2. **REALIZATION MODE = DIRECT** — the `add-roster-device-admission-surface`
   precedent (archived 2026-08-22), not a Speckit flow. The code surface is
   modest and self-contained, so the realization tasks land directly rather
   than through a successor change. `design.md`'s "Realization mode" section
   offered this as the likely route and left it to the read; the read chose
   it.

The change remains ACTIVE after this ratification. Its
`target_release: implementation_pending` archives it only on merged code with
green realization evidence, per `release-realization` — this record authorizes
the realization, it does not perform or archive it.

## Provenance: the dispositions, then this read

Two distinct acts, both Brett's, both 2026-08-23, both in-session via question
prompts:

1. **The disposition round (earlier).** The staged topic
   `notebook-projection-identity` carried five questions open since
   2026-08-15. All five were dispositioned and merged as openxFactory PR #272
   (squash `49758389`). Two are Brett's own rulings — **Q2**, the account type
   (a Google Workspace USER account in the operating tenant's own domain,
   never a consumer Gmail), and the **account timing** (create now/soon) —
   followed the same day by his CONFIRMATION that the account exists as
   `xFactor001@opensoft.one` and his authorization to raise this change on it.
   Q1, Q3, Q4 and Q5 are architect adjudications on executed evidence,
   recorded per-question on the staged fragment with dated disposition
   paragraphs and `Dispositioned-by:` lines.
2. **The ratification read (this record).** Three items were flagged in the
   proposal for the read rather than decided by the encoder. All three were
   before Brett, and he ratified WITH THEM IN VIEW.

## The three flagged read-items, and what happened to them

1. **The generalized `credential-contracts` requirement KEEPS ITS
   VAULT-SPECIFIC HEADER.** The MODIFIED requirement is still titled "The
   credential vault operator is an execution binding, never contract content"
   while its body now states the general operated-identity rule with the vault
   as its first instance. The alternative — renaming it — is a REMOVE plus an
   ADD, which discards the requirement's identity for a wording improvement
   the disposition did not ask for. Flagged in `design.md` Ruling 2 as an open
   naming question. **Ratified as it stands: the header is kept.** A later
   change may rename it; nothing here depends on the name.
2. **The share-out roster's ARTIFACT FORM is a realization call.** The
   requirement fixes the entry's six fields, its stable
   `(hosting_account, user, book_or_alias)` uniqueness key, and the roster's
   role as the approval record — deliberately not whether it is a
   contract-family schema with a validator or a lighter governed record.
   Flagged in `design.md` "Honest limitations" and tasks §2.1. **Ratified as a
   realization decision**, to be made and FLAGGED during realization.
3. **REALIZATION MODE.** Offered as likely-direct and left to the read; ruled
   DIRECT (see Decision, item 2).

## Pre-ratification review

Two bot rounds ran on the proposal PR (#273) before this read, and every
finding was dispositioned on the record.

**Codex — three findings, all real defects in the encoding, all fixed before
ratification (commit `fc8392a4`):**

- **P1 — the retirement retired the replacement.** The migration requirement
  inherited "retire its workspace record in place" from the 2026-08-10
  `split-ideation-book-per-repo` runbook while ALSO requiring the replacement
  step to reuse the same key-derived record id. Followed in order, the
  retirement would have retired the replacement and reproduced exactly the
  unregistered-book failure the replacement exists to prevent. The runbook only
  worked there because its successors carried NEW record ids. Retirement now
  archive-renames the legacy book, deletes its alias, and retires the legacy
  PROVIDER NOTEBOOK with the act preserved in the record's history; retiring a
  workspace record in place survives only where a migration leaves a genuinely
  separate record under a distinct id. Two scenarios cover both branches.
- **P2 — the undeclared install was both conforming and violating.** The
  requirement opened with an unconditional `SHALL declare` and then described
  an undeclared install as legal. Undeclared is now an explicitly
  NONCONFORMING TRANSITION STATE: the sync does not break on one, but reports
  it as unmet rather than as a third legitimate case.
- **P2 — the roster key contradicted the roster's own job.** Including `role`,
  `granted_at` and `granted_by` in the UNIQUENESS key meant a re-approval, a
  role change, or a grant by a different actor each minted a second live
  record, letting a roster defined as the record of CURRENT access assert a
  stale grant beside a live one. Uniqueness is now the stable
  `(hosting_account, user, book_or_alias)` triple with the decision fields as
  attributes and superseded decisions kept as history. All six ruled fields
  still ride on the entry and **the grantee is still in the key** — the
  structural finding the whole Q3 disposition rests on — so this refines the
  tuple rather than reopening the ruling, and is recorded as a refinement in
  `design.md` Ruling 1.

**Copilot — refuted from the record.** It flagged the client-identity-roster
closure count as 14-not-11; on PR #272 the same reviewer had flagged the same
evidence in the OPPOSITE direction. Eleven is what survives checking: a raw
`grep -c` returns 14 because three of its matches are backtick-quoted prose
inside the schema's own header block scalar (lines 37, 40, 43) explaining the
closure convention rather than applying it, while parsing the YAML gives 11
objects whose `additionalProperties` is `false` (and 1 for
`xfactory-credential-contracts.schema.yaml`). `design.md` Ruling 1 now states
which count it means so a third pass does not repeat it.

**Sourcery** filed its usual upsell stub — no findings.

Both MODIFIED requirements were verified programmatically, after every edit, to
carry their promoted scenarios BYTE-IDENTICALLY; the amendments are body text
plus added scenarios only.

## Conscious-acceptance notes (Brett, at ratification)

1. **Authenticating a Workspace account to the `nlm` CLI is not solved by this
   change.** The section 6 runbook's browser-login flow assumes a human at a
   keyboard with a ~20-minute session; a company account changes that story and
   the change says so rather than implying it is routine. The live migration is
   consequently gated on an interactive `nlm login` performed by Brett on a host
   with a browser.
2. **The roster's artifact form is genuinely open at ratification** (read-item
   2). The realization decides it and flags the reasoning — including whether
   placing it under `contracts/` would invoke the contract-release ritual, which
   must be weighed openly rather than allowed to decide the shape silently.
3. **The two migration gaps found in the #272 review are carried as scope, not
   as solved problems.** A plain `--apply` never creates live `xf-session-*`
   notebooks, and `ensure_workspace_record()` refuses to re-register a same-key
   book under a new provider id. Both are tasks (§4.2, §4.3), and the P1 finding
   above is a third defect in the same area found only at the proposal read.
4. **Case B carries no governance obligation, by design.** A personal install's
   own account is a complete binding. The share-approval lane, the roster and
   the offboarding argument all attach to the operator-hosted case because an
   operator exists to bear them.

## Next

Realization runs DIRECTLY, per Brett's mode ruling, against the ratified tasks:
the declared-field read and profile pass-through in
`scripts/sync-notebooklm-books.py`, the parity/report mode, the share-out
roster in whatever form the realization flags, the
`docs/lifecycle-notebook-projection.md` amendments, Opensoft's own Case A
declaration on `xFactor001@opensoft.one`, and the tie-in that closes
`docs/notebooklm-sync-open-item.md`.

The LIVE MIGRATION is gated on Brett's interactive authentication and is not
performed by the realization landing. The change archives only when that
evidence exists, per `release-realization`.
