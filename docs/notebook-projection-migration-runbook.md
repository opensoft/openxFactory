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

**Read step 1 before running anything.** The alias store is a single flat file
shared by every profile, and an `--apply` REGISTERS aliases as it resolves each
book. Running the re-derivation first would silently repoint `xf-canon`,
`xf-drafts` and every `xf-ideation-*` to the new notebooks — after which the
ratified requirement to DELETE the legacy aliases rather than repoint them can
no longer be honoured, and the legacy notebook ids are no longer recoverable
from the store.

## The gate: one interactive act only Brett can perform

**Everything else in this change is landed and green. The migration is not,
and cannot be automated:** `nlm login` is a browser act, the session lives
about 20 minutes, and the account being authenticated is a human-owned Google
identity. Authenticating a Workspace user to this CLI is the open blocker
recorded in [the open operational item](notebooklm-sync-open-item.md) — this
runbook does not solve it, it sequences around it.

The migration begins when Brett runs, in a host shell with a browser:

```bash
nlm login --profile company
```

and signs in as **`xFactor001@opensoft.one`**. On WSL2 without a Linux
browser, add `--wsl` (it launches Windows Chrome); if that corrupts the
terminal, use the CDP route recorded in the open item
(`nlm login --cdp-url http://127.0.0.1:9444 --profile company`).

This creates and authenticates the profile; it does **not** change the default
profile, which step 2 does. Verify the new profile before going further:

```bash
nlm login profile list          # the profile's recorded email, when it has one
nlm login --check
nlm notebook list --profile company 2>/dev/null || nlm notebook list
```

A fresh account lists **no** notebooks. One that already shows
`xFactory — Canon` is the OLD account: stop. The CLI records a profile's email
in `profiles/<name>/metadata.json` — populated by a recent login, left null by
an older one — and the sync compares it to the declared account when it is
there, so a populated wrong address is refused rather than trusted.

## Step 1 — Record the legacy notebook ids, then DELETE the aliases

Do this FIRST, while the CLI is still on `personal`, and before any `--apply`.

```bash
nlm alias list                       # the flat, profile-independent store
nlm alias get xf-canon               # record each id somewhere durable
nlm alias get xf-drafts
nlm alias get xf-ideation-openxfactory   # ...and every other xf-ideation-*
```

Write those ids into the migration evidence. They are how the legacy notebooks
are addressed in step 8 once the aliases are gone.

```bash
nlm alias delete xf-canon
nlm alias delete xf-drafts
nlm alias delete xf-ideation-openxfactory    # ...and the rest
```

Deleting rather than repointing is the ratified requirement, and doing it here
is what makes that possible: the re-derivation in step 4 would otherwise
repoint them for you. This is the 2026-08-10 precedent's order.

## Step 2 — Bind this host to the declared profile

```bash
nlm login switch company
nlm config get auth.default_profile     # expect: company
```

Profile selection is process-global; the sync verifies it before every
invocation and refuses when it is not the expected one.

**Between step 2 and step 3 every sync run refuses, by design.** The
declaration still says `migration.state: pending`, so the sync expects
`personal` while the host is now on `company`. That window is intentional — it
is what stops a half-configured host from writing into either account — and
step 3 closes it. Do steps 2 and 3 together.

## Step 3 — Flip the declaration out of the pending state

In `examples/notebook-projection-hosting.yaml`, set
`hosting.migration.state: complete`. Only now does the sync bind to `company`.
Commit it with the migration evidence; do not flip it early, or every sync
refuses until the books actually move.

## Step 4 — Re-derive the lifecycle books (~40 minutes)

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py .            # preview
python3 openxFactory/scripts/sync-notebooklm-books.py . --apply    # ~40 min
```

One run, because the projection is DERIVED — the books are reconstructed from
the corpus, not copied. The 2026-08-10 precedent moved 314 sources in roughly
40 minutes; expect that order. The run creates each book, its tags, chat
framing, charter and grounding, its alias (now pointing only at the new
notebook, since step 1 cleared the old one), and its workspace record.

## Step 5 — Migrate every LIVE session notebook, one at a time

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

Note that the dashboard's own workbench (`ideation_dashboard/workbench.py`)
creates session notebooks through its own `nlm` invocation, outside this
sync's profile binding. Until that path is bound too — deferred with task 4.2 —
run session migrations through the sync above, not through the workbench.

## Step 6 — Replace each workspace record, do not just retire it

`ensure_workspace_record()` derives the record id from the book's KEY, which is
unchanged in the new account. Finding that id with a different
`provider_notebook_id`, it prints `reconcile by hand` and returns WITHOUT
registering the replacement. So, per book, update the existing record's
`provider_notebook_id` in `examples/lifecycle-notebook-workspaces.yaml` to the
new notebook's id, leaving exactly ONE active record per live book.

## Step 7 — Prove parity against the CORPUS SCAN

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py . --parity
```

Parity is measured against the scan, never against the legacy books — those are
the artifact whose fidelity is in question. The run reports per-book title-set
equality plus a union reconciliation and exits non-zero if anything is pending.
It is read-only, including the alias store. Finish with a plain dry run showing
zero pending ADD/DEL/UPD:

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py .
```

Keep both outputs; they are the migration evidence.

## Step 8 — Retire the legacy books by recorded act

Only once parity holds. Address the legacy notebooks by the **ids recorded in
step 1** — their aliases are already gone.

1. **Archive-rename** each legacy notebook, e.g.
   `xFactory — Canon (RETIRED 2026-08-DD — hosting migration)`.
2. Its alias was deleted in step 1, never repointed. Confirm none was
   re-registered: `nlm alias list`.
3. **Do NOT retire the workspace record** that step 6 made current. Its id is
   key-derived and unchanged, so it IS the live book's registration; retiring
   it would leave the company-hosted book unregistered — the exact failure the
   replacement exists to prevent. What is retired is the legacy PROVIDER
   NOTEBOOK, recorded in the act and in the record's history. (The 2026-08-10
   runbook could retire records in place only because its successors carried
   NEW record ids.)
4. Record the retirement — the recorded ids, the renamed titles, the deleted
   aliases, and the parity output — as the migration evidence.

## Step 9 — Share out, through the governed lane

The decision is a human act: a designated company-policy actor approves or
denies each request. Where that person prefers the account's own sharing UI,
the UI is the interface; where they prefer the CLI, these are the same act
performed from a terminal, and both take `--profile`:

```bash
nlm share invite xf-canon <email> --role viewer --profile company
nlm share status xf-canon --json --profile company     # reconcile the roster
```

Either way the approval writes a `share_out` entry in
`examples/notebook-projection-hosting.yaml` — the entry IS the record. The
pending request from 2026-08-15 sitting in the personal account is granted here
or recorded as denied; it is not left to expire unrecorded.

## Step 10 — Close the operational item

[The open operational item](notebooklm-sync-open-item.md) closes on this
migration's realization, per its own terms — not on the rulings that authorized
it. Close it with the parity output and the retirement record.
