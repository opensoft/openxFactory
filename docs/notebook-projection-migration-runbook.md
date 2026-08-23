# NotebookLM Projection — Hosting Migration Runbook

Status: ratified
Ratified by: add-notebook-projection-identity
Purpose: move a lifecycle notebook projection from one hosting account to
another, under the requirements ratified 2026-08-23 — re-derive, prove parity
against the corpus scan, then retire the originals by recorded act.

This runbook is written for the migration it was ratified for: Opensoft's own
projection, from the personal `brettheap@gmail.com` (`nlm` profile `personal`)
to the declared Workspace account `xFactor001@opensoft.one` (profile
`company`). It generalizes to any hosting change.

## The gate: one interactive act only Brett can perform

**Everything else in this change is landed and green. The migration is not,
and cannot be automated:** `nlm login` is a browser act, the session lives
about 20 minutes, and the account being authenticated is a human-owned Google
identity. Authenticating a Workspace user to this CLI is the open blocker
recorded in
[the open operational item](notebooklm-sync-open-item.md) — this runbook does
not solve it, it sequences around it.

The migration begins when Brett runs, in a host shell with a browser:

```bash
nlm login --profile company
```

and signs in as **`xFactor001@opensoft.one`**. On WSL2 without a Linux
browser, add `--wsl` (it launches Windows Chrome); if that corrupts the
terminal, use the CDP route recorded in the open item
(`nlm login --cdp-url http://127.0.0.1:9444 --profile company`).

Verify before going further — the profile must SEE the right account, and the
CLI stores no email to check it by:

```bash
nlm login --check
nlm config get auth.default_profile        # expect: company, after step 2
nlm notebook list                          # expect: EMPTY (a fresh account)
```

An account that already lists `xFactory — Canon` is the OLD one; stop.

## Step 1 — Bind this host to the declared profile

```bash
nlm login switch company
```

Profile selection is process-global; the sync verifies it and refuses to run
against anything else. Until the declaration's `migration.state` flips, the
sync binds to `personal` — so do this step and step 5 together, not apart.

## Step 2 — Flip the declaration out of the pending state

In `examples/notebook-projection-hosting.yaml`, set
`hosting.migration.state: complete`. Only now does the sync bind to `company`.
Commit it with the migration evidence; do not flip it early, or every sync
refuses until the books actually move.

## Step 3 — Re-derive the lifecycle books (~40 minutes)

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py .            # preview
python3 openxFactory/scripts/sync-notebooklm-books.py . --apply    # ~40 min
```

One run, because the projection is DERIVED — the books are reconstructed from
the corpus, not copied. The 2026-08-10 precedent moved 314 sources in roughly
40 minutes; expect that order. The run creates each book, its tags, chat
framing, charter and grounding, its alias, and its workspace record.

## Step 4 — Migrate every LIVE session notebook, one at a time

**A plain `--apply` does not create session notebooks.** `--session-ref`
handles exactly one named session and returns before the lifecycle loop;
`--session-sweep` reconciles and retires but never creates. So for each live
branch session:

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py . \
    --session-ref <branch> [--session-repository <repo>] --apply
```

Enumerate the live ones first (worktrees across every session repository, not
just canonical checkouts). A migration that moves the lifecycle books alone
leaves live sessions hosted on the account being abandoned.

## Step 5 — Replace each workspace record, do not just retire it

`ensure_workspace_record()` derives the record id from the book's KEY, which is
unchanged in the new account. Finding that id with a different
`provider_notebook_id`, it prints `reconcile by hand` and returns WITHOUT
registering the replacement. So, per book, update the existing record's
`provider_notebook_id` in `examples/lifecycle-notebook-workspaces.yaml` to the
new notebook's id, leaving exactly ONE active record per live book.

## Step 6 — Prove parity against the CORPUS SCAN

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py . --parity
```

Parity is measured against the scan, never against the legacy books — those are
the artifact whose fidelity is in question. The run reports per-book title-set
equality plus a union reconciliation and exits non-zero if anything is pending.
Finish with a plain dry run showing zero pending ADD/DEL/UPD:

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py .
```

Keep both outputs; they are the migration evidence.

## Step 7 — Retire the legacy books by recorded act

Only once parity holds. Exactly as 2026-08-10 did, and with one difference this
migration must observe:

1. **Archive-rename** each legacy notebook, e.g.
   `xFactory — Canon (RETIRED 2026-08-DD — hosting migration)`.
2. **Delete** its alias — never repoint it.
3. **Do NOT retire the workspace record** that step 5 made current. Its id is
   key-derived and unchanged, so it IS the live book's registration; retiring
   it would leave the company-hosted book unregistered — the exact failure the
   replacement exists to prevent. What is retired is the legacy PROVIDER
   NOTEBOOK, recorded in the act and in the record's history. (The 2026-08-10
   runbook could retire records in place only because its successors carried
   NEW record ids.)
4. Record the retirement — the renamed titles, the deleted aliases, and the
   parity output — as the migration evidence.

## Step 8 — Share out, through the governed lane

Grant the current human readers from the new account, and let the approval act
write the roster rather than backfilling it:

```bash
nlm share invite xf-canon <email> --role viewer --profile company
nlm share status xf-canon --json --profile company     # reconcile the roster
```

Each grant becomes a `share_out` entry in
`examples/notebook-projection-hosting.yaml`. The pending request from
2026-08-15 sitting in the personal account is granted here or recorded as
denied — it is not left to expire unrecorded.

## Step 9 — Close the operational item

[The open operational item](notebooklm-sync-open-item.md) closes on this
migration's realization, per its own terms — not on the rulings that authorized
it. Close it with the parity output and the retirement record.
