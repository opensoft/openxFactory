# Migration evidence: split-ideation-book-per-repo

Status: record
Date: 2026-08-10 (migration executed 03:1x–04:37 UTC-4)

## What ran

Sequenced per-book `--apply` runs from the workspace root using the realized
sync (small books first, openxFactory last, canon caught up in the same
window), followed by a full-workspace apply and an idempotence dry-run.

## Books created (provider ids in `examples/lifecycle-notebook-workspaces.yaml`)

| Book | Created | Members migrated | Final occupancy |
|---|---|---|---|
| xFactory Ideation — OpsxFactory | 99b1ff52 | 15 (was 4 in the capped book) | 15/300 |
| xFactory Ideation — codexFactory | c2b89469 | 15 (was 11) | 15/300 |
| xFactory Ideation — MedxFactory | 5830dbd2 | 49 (was 36) | 49/300 |
| xFactory Ideation — LedgerxFactory | 48ac861d | 66 (was 62) | 66/300 |
| xFactory Ideation — openxFactory | 74ace7c8 | 189 (was 188) | 189/300 |

Each creation seeded title, `xfactory,lifecycle` tags, chat framing, charter,
grounding, and its `external_source_workspace` record. The capped legacy book
had silently starved repos in path order (OpsxFactory worst at 4 of 15);
the split recovered ~18 dropped members. Canon 98/300 and Working Drafts
168/300 caught up in the same window.

## Op counts and wall clock

- Small books: 149 adds (~12 min). openxFactory: 189 adds, 03:36:49–04:03:02
  (26m13s, ≈ 8.3 s/add — provider ingestion dominates the 2 s rate floor).
- Canon catch-up: 27 ops across retries + final pass; drafts: 7 ops.
- Auth held for the whole window; no re-login was needed (the doc's ~20-min
  session estimate was conservative tonight).

## Parity (task 3.2)

Title-set equality per book: 5/5 OK (15, 15, 49, 66, 189 observed = expected,
charter and grounding accounted). Union reconciliation: corpus 314 members =
observed 314, reconciled against the corpus scan, not the legacy book.

## Retirement (task 3.3)

- Legacy notebook 27b1880b archive-renamed:
  "xFactory — Ideation (RETIRED 2026-08-10 — split per-repo)".
- `xf-ideation` alias deleted (verified unresolvable); never repointed.
- Its workspace record retired in place (commented, with the retirement note).

## Incidents during migration — all fixed in the realization, live-proven

1. **Errno 7 (argv limit)**: the promoted ideation-dashboard spec (>128 KiB)
   cannot ride `--text` (Linux MAX_ARG_STRLEN). Fix: oversized docs upload as
   a temp file and are renamed to the contract title (the CLI titles `--file`
   sources by filename and ignores `--title`). The per-book containment held:
   every other book completed, exit nonzero.
2. **`source rename` requires `--notebook`** — discovered on the first retry
   pass; fixed.
3. **Transient provider failure behind an EMPTY CLI error** on a 3 KB doc
   that succeeded by hand seconds later — the cap incident's own signature is
   sometimes just a transient. Fix: one retry after a 10 s pause; real
   failures still raise.

## Idempotence (task 4.1)

Final full dry-run: **0 pending ADD/DEL/UPD across all seven books**; guard
silent (largest headroom consumer: openxFactory ideation at 189/300,
headroom 111); orphan sweep clean; both phases exit 0.
