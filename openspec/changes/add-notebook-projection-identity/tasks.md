# Tasks: add-notebook-projection-identity

Status: draft

NOTHING BELOW RUNS BEFORE RATIFICATION. This change's own diff is the spec
deltas and these records; every task here is realization, authorized by the
ratification read and not by the landing of this proposal.

Sequencing matters in one place: §4 (Opensoft's own migration) is the change's
evidence gate and cannot start before §1 and §2 are real, because it is the
first thing to run under a declared account.

## 1. The declared hosting identity, read and honored

- [ ] 1.1 Define where an install declares its hosting identity, and the shape
  of the declaration: the case (operator-hosted / self-hosted), the account
  address, and — for the operator-hosted case — the domain the operating party
  administers. Name the intake surface that carries it; no such flow was named
  at capture, and choosing it is part of this task rather than a prerequisite.
- [ ] 1.2 Teach `scripts/sync-notebooklm-books.py` to READ the declaration.
  An undeclared install does not BREAK — it keeps today's default-profile
  behavior — but it is reported as NOT MEETING the requirement, a transition
  state rather than a third legitimate case, and is never silently presented as
  governed.
- [ ] 1.3 Bind every CLI invocation to the declared identity's `nlm` profile.
  The script passes NO profile today — `subprocess.run(["nlm", *args])`, no
  flag, no environment — so this touches the single `nlm()` helper rather than
  each call site. A run that cannot resolve the declared profile FAILS; it must
  not fall back to the default profile silently.
- [ ] 1.4 Refuse an operator-hosted declaration naming a consumer account, and
  refuse any non-user principal, each with a message naming the reason (missing
  administrative control; the platform's no-API/user-account-only constraint)
  rather than a bare validation failure.
- [ ] 1.5 Record Opensoft's own declaration: operator-hosted,
  `xFactor001@opensoft.one`.

## 2. The share-out roster and the governed approval lane

- [ ] 2.1 Decide and build the roster's artifact form — a contract-family schema
  with a validator, or a lighter governed record. The requirement fixes the six
  fields an entry carries, the stable `(hosting_account, user, book_or_alias)`
  uniqueness key with the decision fields as attributes, and the roster's role
  as the approval record; the artifact shape is this task's call (see design.md,
  "Honest limitations").
- [ ] 2.2 Make the grantee part of the uniqueness key, and prove it with the
  case that broke the client-identity roster: two grantees, one book, one
  hosting account — both entries must stand. Prove the converse too: one
  grantee re-approved or re-roled on the same book UPDATES their single live
  entry, leaving no stale grant asserted beside the current one.
- [ ] 2.3 Reference an identity-brokering persona where one resolves, with a
  bare address only where none does. `add-identity-brokering` is ACTIVE and its
  capability is not yet promoted, so this is a soft reference today; do not
  create a hard dependency on an unpromoted capability.
- [ ] 2.4 Write the approval lane's procedure: who the designated
  company-policy actor is, where they act (the hosting account's own UI), and
  how approving WRITES the roster entry and denying is recorded in the same
  lane. No API is designed against; the platform has none.
- [ ] 2.5 Retire the standing workaround honestly — the pending request from
  2026-08-15 sitting in `brettheap@gmail.com` is either granted through the new
  lane or recorded as denied. It is not left to expire unrecorded.

## 3. Documentation amendments

- [ ] 3.1 `docs/lifecycle-notebook-projection.md` section 1: the "quota is one
  shared account" framing becomes the DECLARED hosting account, with the quota
  point preserved (it is still one account per install; that is now a declared
  fact rather than an accident).
- [ ] 3.2 Section 6's operator runbook: rewrite the auth flow for a declared
  account, including the profile selection. State honestly what is still
  unsolved about authenticating a Workspace user to the CLI rather than
  implying it is routine.
- [ ] 3.3 Cross-link the two-case custody rule to `credential-contracts` so the
  runbook does not restate the principle it now consumes.

## 4. Opensoft's own migration — the evidence gate

- [ ] 4.1 Add a parity/report mode to the sync. 2026-08-10's parity was
  hand-assembled from `nlm source list`; the migration requirement asks for
  parity to be PROVEN, and proving it by hand a second time is how the first
  gap got missed.
- [ ] 4.2 Add a bulk session-migration mode, or an explicit per-session
  procedure. VERIFIED GAP: a plain `--apply` never creates live `xf-session-*`
  notebooks — `--session-ref` handles one named session and returns before the
  lifecycle loop, `--session-sweep` only retires. Without this, live sessions
  stay on the account being abandoned.
- [ ] 4.3 Add the explicit workspace-record REPLACEMENT step. VERIFIED GAP:
  `ensure_workspace_record()` derives `record_id` from `spec.key`, unchanged in
  the new account; finding that id with a different `provider_notebook_id` it
  returns WITHOUT registering the replacement. Retiring the old record on top of
  that leaves the company-hosted book unregistered. Leave exactly one active
  record per live book.
- [ ] 4.4 Re-derive the three lifecycle books under `xFactor001@opensoft.one`
  in one `--apply` (precedent: 314 sources, roughly 40 minutes), then migrate
  every live session notebook per §4.2.
- [ ] 4.5 Prove parity: per-book title-set equality plus a union reconciliation
  against THE CORPUS SCAN — not against the legacy books — then a final dry run
  showing zero pending ADD/DEL/UPD. Record the output as the evidence.
- [ ] 4.6 Retire the personal-hosted books by RECORDED ACT: archive-rename each
  legacy book and DELETE its alias (never repoint). Do NOT retire the workspace
  record §4.3 just made current — its id is key-derived and unchanged, so it IS
  the live book's registration; retire the legacy PROVIDER NOTEBOOK and preserve
  the act in the record's history. (This is where the 2026-08-10 runbook does
  not transfer: its successors carried new record ids, so there was a separate
  legacy record to retire.) Record the act.
- [ ] 4.7 Share out to the current human readers from the new account through
  the §2.4 lane, so the first roster entries are written by the governed act
  rather than backfilled.

## 5. Close the operational item and validate green

- [ ] 5.1 `docs/notebooklm-sync-open-item.md`: close it on the realization. It
  was deliberately left OPEN by the disposition round (PR #272 added only a
  dated pointer), because it closes on this change's realization and not on the
  rulings. Its "Strategic direction" section is what §4 executes.
- [ ] 5.2 Gates: `pytest tests/ideation-dashboard`, `pytest
  tests/ideation_dashboard`, `pytest tests/doc-health`, `OPENSPEC_TELEMETRY=0
  openspec validate --all --strict`, doc-health zero-new against a fresh
  `origin/main` baseline, and `scripts/validate-ideation-dashboard-contracts.py`
  at its 0-error / 4-warning baseline.
- [ ] 5.3 If §2.1 lands a contract-family artifact, register it in
  `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive
  bundle cut and follow `docs/contract-versioning-policy.md`. If it lands a
  lighter governed record, say so explicitly and cut no bundle.

## 6. Bookkeeping

- [ ] 6.1 Retire the staged topic from `ideation/staging/INDEX.md` once its
  material has moved, per the index's own maintenance rule.
- [ ] 6.2 README OpenSpec Records: move this change from active to archived when
  it archives, on merged code with green realization evidence.

## 7. NOT part of this change

- The `xf-wb-*` cross-checkout deletion bug (a routine `--apply` in one checkout
  can delete another engineer's scratch notebooks). Already recorded in
  `docs/notebooklm-sync-open-item.md` as wanting its own change.
- Any automated share-request detection or approval. Revisit only if the
  platform ever exposes a surface; the approval stays a human act regardless.
- Renaming the `credential-contracts` requirement whose body this change
  generalizes. Flagged for the ratification read in design.md, Ruling 2.
