# Tasks: add-notebook-projection-identity

Status: ratified
Ratified: 2026-08-23 — `review/ratification-2026-08-23.md`. Realization mode: DIRECT
(Brett, at the read). These tasks are AUTHORIZED, not performed, by the
ratification.

NOTHING BELOW RUNS BEFORE RATIFICATION. This change's own diff is the spec
deltas and these records; every task here is realization, authorized by the
ratification read and not by the landing of this proposal.

Sequencing matters in one place: §4 (Opensoft's own migration) is the change's
evidence gate and cannot start before §1 and §2 are real, because it is the
first thing to run under a declared account.

## 1. The declared hosting identity, read and honored

- [x] 1.1 Define where an install declares its hosting identity, and the shape
  of the declaration: the case (operator-hosted / self-hosted), the account
  address, and — for the operator-hosted case — the domain the operating party
  administers. Name the intake surface that carries it; no such flow was named
  at capture, and choosing it is part of this task rather than a prerequisite.
  - REALIZED 2026-08-23: Declared in `examples/notebook-projection-hosting.yaml`, beside the workspace registry for this same projection. FLAGGED: the packet left the intake surface unnamed; for the only live install the declaration must be somewhere `sync-notebooklm-books.py` can read, and that file is where the projection's other governed record already lives. A future multi-install intake flow can source it from there without moving it.
- [x] 1.2 Teach `scripts/sync-notebooklm-books.py` to READ the declaration.
  An undeclared install does not BREAK — it keeps today's default-profile
  behavior — but it is reported as NOT MEETING the requirement, a transition
  state rather than a third legitimate case, and is never silently presented as
  governed.
  - REALIZED 2026-08-23: `read_hosting_declaration()` — a narrow scalar reader, not a YAML parse, because this script carries no YAML dependency (the workspace registry beside it is text-handled for the same reason). Undeclared reports a transition state and proceeds.
- [x] 1.3 Bind every CLI invocation to the declared identity's `nlm` profile.
  The script passes NO profile today — `subprocess.run(["nlm", *args])`, no
  flag, no environment — so this touches the single `nlm()` helper rather than
  each call site. A run that cannot resolve the declared profile FAILS; it must
  not fall back to the default profile silently.
  - HARDENED 2026-08-23 on review (Codex P1 + P2, PR #277): the binding is re-asserted BEFORE EVERY invocation from the CLI's own config file, because a single opening check does not bind a forty-minute run when another terminal can switch the process-global profile; and the declaration's load-bearing rules are enforced inline on the operational path, because nothing the sync ran invoked the validator.
  - REALIZED 2026-08-23: `enforce_hosting_profile()`. CHANGED BY A VERIFIED CLI FACT: of the verbs this sync issues, NONE accepts a per-invocation `--profile` — selection is process-global via `auth.default_profile`. So the binding is VERIFIED and the run REFUSES when the active profile is not the declared one, carrying the exact `nlm login switch` remediation. The sync never switches the profile itself: shared user state, and other sessions race on it. While a migration is pending it binds to the account that still holds the books.
- [x] 1.4 Refuse an operator-hosted declaration naming a consumer account, and
  refuse any non-user principal, each with a message naming the reason (missing
  administrative control; the platform's no-API/user-account-only constraint)
  rather than a bare validation failure.
  - REALIZED 2026-08-23: `scripts/validate-notebook-projection-hosting.py` refuses a consumer account for the operator-hosted case (naming the missing administrative control) and any service account (naming the platform constraint), plus a domain mismatch and a third case.
- [x] 1.5 Record Opensoft's own declaration: operator-hosted,
  `xFactor001@opensoft.one`.

## 2. The share-out roster and the governed approval lane
  - REALIZED 2026-08-23: Opensoft's declaration: operator-hosted, `xFactor001@opensoft.one`, Workspace user in `opensoft.one`, profile `company`, migration pending from `brettheap@gmail.com`/`personal`.
- [x] 2.1 Decide and build the roster's artifact form — a contract-family schema
  with a validator, or a lighter governed record. The requirement fixes the six
  fields an entry carries, the stable `(hosting_account, user, book_or_alias)`
  uniqueness key with the decision fields as attributes, and the roster's role
  as the approval record; the artifact shape is this task's call (see design.md,
  "Honest limitations").
  - REALIZED 2026-08-23: DECIDED: a governed YAML **outside `contracts/`**, at `examples/notebook-projection-hosting.yaml`, validated by a dedicated script. Reasoning, flagged rather than left implicit: the record is the operator's own governance artifact for ONE install's tooling account — no other repository, install or domain consumes it and nothing pins it, which is what `contracts/` membership is for — and its sibling `lifecycle-notebook-workspaces.yaml`, the workspace registry for this same projection read and written by the same script, sits there for exactly that reason. The decision is made on the consumer/ownership test, NOT on the cost of the contract-release ritual; promoting the shape into `contracts/` stays available as a later deliberate act if a second install ever needs to interoperate. **No contract-release ritual fires: `contracts/` is untouched.**
- [x] 2.2 Make the grantee part of the uniqueness key, and prove it with the
  case that broke the client-identity roster: two grantees, one book, one
  hosting account — both entries must stand. Prove the converse too: one
  grantee re-approved or re-roled on the same book UPDATES their single live
  entry, leaving no stale grant asserted beside the current one.
  - REALIZED 2026-08-23: Uniqueness is the stable `(hosting_account, user, book_or_alias)` triple. Both directions are tested: two grantees on one book stay distinct (the case that broke the client-identity roster), and a re-decision on one is refused as a duplicate key so it must update the live entry.
- [x] 2.3 Reference an identity-brokering persona where one resolves, with a
  bare address only where none does. `add-identity-brokering` is ACTIVE and its
  capability is not yet promoted, so this is a soft reference today; do not
  create a hard dependency on an unpromoted capability.
  - REALIZED 2026-08-23: Soft reference by design — `add-identity-brokering` is ACTIVE and unpromoted, so the roster carries addresses today and gains persona references when that capability lands. No hard dependency created.
- [ ] 2.4 Write the approval lane's procedure: who the designated
  company-policy actor is, where they act (the hosting account's own UI), and
  how approving WRITES the roster entry and denying is recorded in the same
  lane. No API is designed against; the platform has none.
- [ ] 2.5 Retire the standing workaround honestly — the pending request from
  2026-08-15 sitting in `brettheap@gmail.com` is either granted through the new
  lane or recorded as denied. It is not left to expire unrecorded.

## 3. Documentation amendments

- [x] 3.1 `docs/lifecycle-notebook-projection.md` section 1: the "quota is one
  shared account" framing becomes the DECLARED hosting account, with the quota
  point preserved (it is still one account per install; that is now a declared
  fact rather than an accident).
  - REALIZED 2026-08-23: §1 now names the declared hosting identity and the two cases; §9's quota sentence attributes the ceiling to the install's one declared account rather than to "one shared account", keeping the capacity point intact.
- [x] 3.2 Section 6's operator runbook: rewrite the auth flow for a declared
  account, including the profile selection. State honestly what is still
  unsolved about authenticating a Workspace user to the CLI rather than
  implying it is routine.
  - REALIZED 2026-08-23: §6 gains step 0 (read and bind the profile) and step 2b (`--parity`), and says plainly that profile selection is process-global and what is verified is the profile NAME, not the address — the CLI stores no email.
- [x] 3.3 Cross-link the two-case custody rule to `credential-contracts` so the
  runbook does not restate the principle it now consumes.
  - REALIZED 2026-08-23: §12 cross-links the rule to `credential-contracts` rather than restating it.

## 4. Opensoft's own migration — the evidence gate
- [x] 4.1 Add a parity/report mode to the sync. 2026-08-10's parity was
  hand-assembled from `nlm source list`; the migration requirement asks for
  parity to be PROVEN, and proving it by hand a second time is how the first
  gap got missed.
  - REALIZED 2026-08-23: `--parity`: per-book title-set equality plus a union reconciliation against THE CORPUS SCAN, reporting only. A test asserts it issues no mutating verb — a parity proof that changes what it measures is not a proof.
- [ ] 4.2 Add a bulk session-migration mode, or an explicit per-session
  procedure. VERIFIED GAP: a plain `--apply` never creates live `xf-session-*`
  notebooks — `--session-ref` handles one named session and returns before the
  lifecycle loop, `--session-sweep` only retires. Without this, live sessions
  stay on the account being abandoned.
  - N1 (review 2026-08-23): `scripts/ideation_dashboard/workbench.py` creates session notebooks through its OWN `subprocess.run(["nlm", ...])`, outside this sync's profile binding — a second unbound path to the same account. Scope-adjacent and explicitly covered by this deferral: binding it rides whichever change gives sessions a bulk migration mode. The runbook says meanwhile to migrate sessions through the sync, not the workbench.
  - PROCEDURE LANDED, code deferred to the migration itself: runbook step 5 gives the explicit per-session procedure the task allows as the alternative to a bulk mode (`--session-ref <branch> --apply`, once per live session, enumerated across every worktree). A bulk mode stays worth adding; nothing is migrated until Brett authenticates, so it is not on this landing's critical path.
- [ ] 4.3 Add the explicit workspace-record REPLACEMENT step. VERIFIED GAP:
  `ensure_workspace_record()` derives `record_id` from `spec.key`, unchanged in
  the new account; finding that id with a different `provider_notebook_id` it
  returns WITHOUT registering the replacement. Retiring the old record on top of
  that leaves the company-hosted book unregistered. Leave exactly one active
  record per live book.
  - PROCEDURE LANDED, code gap OPEN and stated: runbook step 5 makes the record replacement an explicit numbered step with the reason `ensure_workspace_record()` will not do it. The function still returns `reconcile by hand`; teaching it to replace is a code change that belongs with the migration run, not before it.
- [x] 4.4 Re-derive the three lifecycle books under `xFactor001@opensoft.one`
  in one `--apply` (precedent: 314 sources, roughly 40 minutes), then migrate
  every live session notebook per §4.2.
  - **DONE 2026-08-24**, evidence in PR #289 (`546e0a98`),
    `docs/notebook-projection-migration-evidence-2026-08-24.md`: 7 books, 626
    managed sources. **THE TICK WAS OWED SINCE THAT DATE** — #289 recorded the
    evidence document but touched no task box, so this list read as unstarted
    work that had in fact run. Ticked 2026-08-26 against that recorded evidence.
    The session-notebook half of this task is the separately HELD step 5 and is
    NOT claimed here.
- [x] 4.5 Prove parity: per-book title-set equality plus a union reconciliation
  against THE CORPUS SCAN — not against the legacy books — then a final dry run
  showing zero pending ADD/DEL/UPD. Record the output as the evidence.
  - **DONE — but ticked against the 2026-08-25 run, not the 2026-08-24 one, and
    the difference is the point.** The 2026-08-24 pass (608/608 titles) was
    produced by a parity mode later proven unable to see this class of gap:
    `add-projection-title-uniqueness` (archived 2026-08-25) established that
    comparing derived TITLES against live TITLES *"reports OK on a book that is
    missing documents"*, and measured three collisions, eight documents, five
    displaced — with `ideation-medxfactory`, which our own evidence recorded as
    `PARITY OK: 48 titles match`, among them.
  - The run that satisfies this task is the one taken AFTER that fix, under the
    amended rule: **`parity: PROVEN`, exit 0**, every book reading *N documents
    in N titles* (canon 113/113, drafts 188/188, openxFactory 246/246,
    LedgerxFactory 65/65, MedxFactory 51/51, OpsxFactory 16/16, codexFactory
    14/14), union 675 derived / 675 live managed, **0 unprojected, 0
    unaccounted**, and a convergence dry run planning ZERO operations. Full
    reasoning: `review/retirement-gate-clearance-2026-08-26.md` § 3.
- [ ] 4.6 **READY — AWAITING OPERATOR EXECUTION.** The gate is CLEARED: Brett
  Heap ruled 2026-08-26 that the 2026-08-24 retirement hold is discharged on its
  own stated terms — the 228KB spec has a projected form — with the live provider
  check as post-hoc confirmation rather than a precondition. Record:
  `review/retirement-gate-clearance-2026-08-26.md`.
  This box stays UNTICKED because retirement is an ACT and nothing in this
  repository can perform it: it renames seven notebooks inside
  `brettheap@gmail.com`, which needs an `nlm` session bound to the legacy
  account, and profile selection is process-global user state the sync refuses to
  switch. Prepared instead, to be run in one sitting:
  **`docs/notebook-projection-retirement-runbook-step8.md`** — seven exact
  renames with the legacy ids resolved from each workspace record's own
  `provider_notebook_id`, three verifications, and the abort conditions. Tick
  this from the operator's recorded output, not from the runbook existing.
  The original task text, unchanged, is what that runbook performs:
  Retire the personal-hosted books by RECORDED ACT: archive-rename each
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
- [x] 5.2 Gates: `pytest tests/ideation-dashboard`, `pytest
  tests/ideation_dashboard`, `pytest tests/doc-health`, `OPENSPEC_TELEMETRY=0
  openspec validate --all --strict`, doc-health zero-new against a fresh
  `origin/main` baseline, and `scripts/validate-ideation-dashboard-contracts.py`
  at its 0-error / 4-warning baseline.
  - GREEN AT THE LANDING SQUASH 2026-08-23 (`40b33845`, PR #277): 3983
    passed / 15 skipped (ideation-dashboard); 902 passed / 13 subtests
    (notebooklm + doc-health + ideation_dashboard) pre-merge and 839 + 13 at
    the squash; `openspec --all --strict` 72/72 fresh-counted at the squash (69
    before three other sessions' changes landed alongside); dashboard validator
    0 error / 4 warning; hosting validator 0 error. doc-health ZERO NEW
    attributable to this squash, measured against a baseline taken at
    `7431f033` — the commit immediately before it — because main had advanced
    by fourteen commits from other sessions and a plain pre-merge comparison
    would have charged this change with two `proposal-origin` errors belonging
    to the MedxChart/MedxPractice boundary changes.
- [x] 5.3 If §2.1 lands a contract-family artifact, register it in
  `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive
  bundle cut and follow `docs/contract-versioning-policy.md`. If it lands a
  lighter governed record, say so explicitly and cut no bundle.
  - RESOLVED 2026-08-23, SAID EXPLICITLY: §2.1 landed a LIGHTER GOVERNED
    RECORD (`examples/notebook-projection-hosting.yaml` plus
    `scripts/validate-notebook-projection-hosting.py`), NOT a contract-family
    artifact. **No bundle was cut and no contract-release ritual fired**: no
    CHANGELOG allocation, no `contracts/manifest.yaml` row or digest, no
    `contract_bundle_version` bump, no inventory rebuild, no verify-commit, no
    tag. `contracts/` is byte-untouched across the whole realization, asserted
    at every gate run and again at the squash. The published bundle remains
    `contract-v1.40`.

## 6. Bookkeeping

- [ ] 6.1 Retire the staged topic from `ideation/staging/INDEX.md` once its
  material has moved, per the index's own maintenance rule.
- [ ] 6.2 README OpenSpec Records: move this change from active to archived when
  it archives, on merged code with green realization evidence.

- [x] 6.3 Adversarial review round (2026-08-23, PR #277): 1 blocking + 5
  should-fix, all reproduced before fixing, all fixed on the branch.
  - **B1** the runbook's re-derivation repointed the aliases its retirement
    step was required to DELETE — the alias store is one flat,
    profile-independent file and `resolve_or_create_book()` registers on the
    FOUND path too. The runbook now records the legacy notebook ids and
    deletes the aliases in step 1, before any `--apply`, per the 2026-08-10
    order; steps renumbered accordingly.
  - **S1** `--parity` issued three `alias set` calls while claiming never to
    mutate. Alias binding is now switchable and off for the read-only caller,
    and the test's blocklist covers `alias set`/`alias delete`.
  - **S2** a hosting file the narrow reader could not parse (flow style,
    four-space, tabs) took the UNDECLARED branch and ran the whole job
    unbound, while the validator passed the same file. An existing file now
    always yields a dict, and an empty one REFUSES.
  - **S3** `migration.state: in_progress` failed the validator and passed the
    sync, which bound the declared profile while the books were elsewhere.
    `_refuse_unusable_declaration()` now owns the state vocabulary and the
    pending-requires-`from_nlm_profile` rule — one rule, one owner.
  - **S4** "the CLI stores no email for a profile" was FALSE:
    `profiles/<name>/metadata.json` carries `email` (`farheap` populated,
    `personal` null). The sync now compares it to the declared account when
    present, reports null as unknown, and the claim is corrected in the
    docstring, §12 and the runbook.
  - **S5** runbook step references were off by one at the stranding point;
    corrected, and the deliberate refuse-window between binding the host and
    flipping the state is now stated.
  - All five new guards revert-tested individually.
- [x] 6.4 Notes recorded rather than fixed (review N2-N5):
  - **N2** a microsecond TOCTOU remains between `assert_still_bound()` and the
    `subprocess.run` after it. It cannot be closed without a per-invocation
    profile flag the CLI does not offer for these verbs; STATED in §12 rather
    than left implicit.
  - **N3** the hosting validator is not wired into CI. The pytest gate
    exercises it against the committed record
    (`test_the_committed_record_conforms`), which mitigates but does not
    replace a CI wiring; a follow-up may add it beside the other validators.
  - **N4** `self_hosted` declarations ignore `account_type` and `domain`, and
    the `denied:` list has no field discipline. Both are realization
    follow-ups: the self-hosted case deliberately carries no organizational
    obligation, and no denial has been recorded yet.
  - **N5** the runbook's `nlm share invite` and §12's "in the account's own UI"
    now describe ONE act with two interfaces, with the decision human either
    way, rather than reading as two different lanes.

## 7. NOT part of this change

- The `xf-wb-*` cross-checkout deletion bug (a routine `--apply` in one checkout
  can delete another engineer's scratch notebooks). Already recorded in
  `docs/notebooklm-sync-open-item.md` as wanting its own change.
- Any automated share-request detection or approval. Revisit only if the
  platform ever exposes a surface; the approval stays a human act regardless.
- Renaming the `credential-contracts` requirement whose body this change
  generalizes. Flagged for the ratification read in design.md, Ruling 2.
