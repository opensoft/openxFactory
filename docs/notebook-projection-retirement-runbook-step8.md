# Step 8 — Retire the legacy notebooks (operator runbook)

Status: draft
Kind: runbook
Repository context: openxFactory
Backed by: `openspec/changes/add-notebook-projection-identity/review/retirement-gate-clearance-2026-08-26.md`

One sitting, roughly fifteen minutes. Seven archive-renames and three
verifications. **Only the operator can run this** — it acts on notebooks in
`brettheap@gmail.com`, and the `nlm` profile is process-global user state.

The gate is cleared: Brett Heap ruled 2026-08-26 that the retirement condition is
satisfied on the repository evidence chain. This runbook is the act.

---

## Before you start

**The rename is reversible; deletion is not.** This runbook NEVER deletes a
notebook. The 2026-08-10 precedent deleted a retired book only after a separate,
later act. Do not shortcut to deletion here — the legacy books are the only copy
of anything the migration got wrong, and they cost nothing to keep.

You need:

* a shell where `nlm` is on PATH,
* the **personal** profile authenticated (the legacy account), and
* this file open, because the ids are not memorable.

### The seven notebooks

Legacy id is what you rename. The new id is listed only so you can prove you are
not touching it. Both were read from each workspace record's own
`provider_notebook_id` in `examples/lifecycle-notebook-workspaces.yaml`.

| Book | Legacy id — RENAME THIS | Company id — DO NOT TOUCH |
| --- | --- | --- |
| drafts | `b83e63e3-262a-4dfe-9b9f-332b3d27d1bb` | `991f0af7-2077-4c26-ac1d-d92e2af9f99c` |
| canon | `6f10282a-7b5b-41c5-9109-55e603890730` | `b331ed13-fa0b-456a-8004-184f66939ecd` |
| ideation-opsxfactory | `99b1ff52-2a93-43c2-b8fc-a153328ccd77` | `2c2ba7ae-65e1-436a-ba4c-0a5f8f2a99bb` |
| ideation-codexfactory | `c2b89469-396e-4fef-9154-fa9ade81d64c` | `251c118f-4a02-4c9e-8ea2-025b12237e1c` |
| ideation-medxfactory | `5830dbd2-5624-4852-987d-9f4e37746448` | `81217e98-1cd2-4bb4-a4b8-917c601ce9e5` |
| ideation-ledgerxfactory | `48ac861d-5a5c-4515-92fc-5b7b251c22c7` | `0042f5e6-6e49-4ea1-9a14-e298bfe0fb09` |
| ideation-openxfactory | `74ace7c8-b3df-4373-bcd2-64043b153cba` | `02295a6e-0193-4f6f-9501-c6e9e03bdc01` |

---

## 0. Confirm which account you are on

```bash
nlm auth status
```

**Expected:** the **personal** profile (`brettheap@gmail.com`) is active.

> **ABORT** if it shows `company` / `xFactor001@opensoft.one`. Renaming there
> would retitle the LIVE books. Switch with `nlm login switch personal` and
> re-run this check before going on.

---

## 1. Prove the legacy notebooks are still there, under the expected ids

```bash
nlm notebook list --json | jq -r '.[] | "\(.id)\t\(.title)"' | grep -F -f - <<'IDS'
b83e63e3-262a-4dfe-9b9f-332b3d27d1bb
6f10282a-7b5b-41c5-9109-55e603890730
99b1ff52-2a93-43c2-b8fc-a153328ccd77
c2b89469-396e-4fef-9154-fa9ade81d64c
5830dbd2-5624-4852-987d-9f4e37746448
48ac861d-5a5c-4515-92fc-5b7b251c22c7
74ace7c8-b3df-4373-bcd2-64043b153cba
IDS
```

If that pipeline is awkward in your shell, the plain form is fine:

```bash
nlm notebook list --json | jq -r '.[] | "\(.id)  \(.title)"'
```

**Expected:** all seven ids present, with their original (un-suffixed) titles.

> **ABORT** if an id is missing. A missing legacy notebook means something else
> already acted on this account — stop and find out what before renaming
> anything.
>
> **NOTE, not an abort:** a title already carrying `(RETIRED …)` means that book
> was done in an earlier attempt. Skip it in step 2 and say so in step 5.

---

## 2. Archive-rename each legacy notebook

Seven commands. The suffix is the recorded form from runbook step 8; today's
date is already filled in.

```bash
nlm notebook rename b83e63e3-262a-4dfe-9b9f-332b3d27d1bb "xFactory — Drafts (RETIRED 2026-08-26 — hosting migration)"
nlm notebook rename 6f10282a-7b5b-41c5-9109-55e603890730 "xFactory — Canon (RETIRED 2026-08-26 — hosting migration)"
nlm notebook rename 99b1ff52-2a93-43c2-b8fc-a153328ccd77 "xFactory — Ideation OpsxFactory (RETIRED 2026-08-26 — hosting migration)"
nlm notebook rename c2b89469-396e-4fef-9154-fa9ade81d64c "xFactory — Ideation codexFactory (RETIRED 2026-08-26 — hosting migration)"
nlm notebook rename 5830dbd2-5624-4852-987d-9f4e37746448 "xFactory — Ideation MedxFactory (RETIRED 2026-08-26 — hosting migration)"
nlm notebook rename 48ac861d-5a5c-4515-92fc-5b7b251c22c7 "xFactory — Ideation LedgerxFactory (RETIRED 2026-08-26 — hosting migration)"
nlm notebook rename 74ace7c8-b3df-4373-bcd2-64043b153cba "xFactory — Ideation openxFactory (RETIRED 2026-08-26 — hosting migration)"
```

**Expected:** each returns success and echoes the new title.

> **If one fails:** re-run that single command. The rename is idempotent in
> effect — renaming to a title it already has is harmless. Do not proceed to
> step 3 with a failure unexplained.
>
> **If `nlm notebook rename` does not exist under that spelling**, check
> `nlm notebook --help`. Do not improvise with a delete-and-recreate.

---

## 3. Confirm no alias was re-registered

The aliases were deleted in step 1 of the migration and must never have been
repointed — repointing an alias at a retired book is the failure the original
runbook's B1 finding was about.

```bash
nlm alias list
```

**Expected:** no alias resolves to any of the seven **legacy** ids. The
`xf-canon` / `xf-drafts` / `xf-ideation-*` aliases should resolve to the
**company** ids in the right-hand column, or not exist.

> **ABORT AND REPORT** if any alias points at a legacy id. Do not "fix" it by
> repointing — record what you found first.

---

## 4. Confirm the company books are untouched

The whole risk of this runbook is acting on the wrong account, so prove you
didn't.

```bash
nlm login switch company
nlm auth status                       # expect xFactor001@opensoft.one
nlm notebook list --json | jq -r '.[] | "\(.id)  \(.title)"'
```

**Expected:** the seven **company** ids present, titles WITHOUT any `(RETIRED …)`
suffix.

Then the definitive read the clearance record called post-hoc confirmation:

```bash
python3 openxFactory/scripts/sync-notebooklm-books.py . --parity
```

**Expected:** `parity: PROVEN`, exit 0 — each book reading *N documents in N
titles*, union 0 unprojected / 0 unaccounted.

> **This is confirmation, not a gate.** If it disagrees with the 2026-08-25 run,
> that is a finding worth stopping on and reporting — but the retirement act in
> step 2 is already ruled and done, and is reversible by rename if needed.

---

## 5. Record the act

Retirement is a RECORDED act; the rename alone is not the deliverable. Report
back, or write it straight into
`docs/notebook-projection-migration-evidence-2026-08-24.md` under a
`## Step 8 — EXECUTED 2026-08-26` heading:

* the seven legacy ids and their new titles (copy step 2's echoes),
* the `nlm alias list` output from step 3,
* the `--parity` output from step 4,
* anything you skipped and why (a book already carrying `(RETIRED …)`).

**Do NOT retire the workspace records.** Their ids are key-derived and unchanged,
so each record IS the live company book's registration. What was retired is the
legacy PROVIDER NOTEBOOK. The records need one edit only: the block at the top of
`examples/lifecycle-notebook-workspaces.yaml` currently says *"Status: PENDING
RETIREMENT"* and *"THE LEGACY NOTEBOOKS ARE NOT RETIRED"* — that becomes the
executed statement, with the date.

An agent can make that edit and tick task 4.6 from your step-5 output; it needs
nothing but the record.

---

## What this runbook deliberately does not do

* **No deletion.** See the top.
* **No share-out.** That is step 9, and it waits on task 2.4 naming the
  designated company-policy actor — still unnamed as of 2026-08-26.
* **No session-notebook migration.** Step 5 is separately held and is not
  cleared by the 2026-08-26 retirement ruling.
