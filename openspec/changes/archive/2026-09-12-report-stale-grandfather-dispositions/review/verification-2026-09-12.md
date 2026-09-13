# Verification: report-stale-grandfather-dispositions

Status: record
Kind: report

**EVERY LINE BELOW IS A COMMAND RUN IN THIS CLONE (`pkt-965`), ON THE RATIFIED
TREE, IMMEDIATELY BEFORE THE RATIFICATION COMMIT**, with its exit code and its
own output quoted, and — for everything that can differ by what `main` alone
already carries — a CONTROL run beside it on a fresh `git worktree` at
`origin/main` `1f0686466ea20fa4f76ca1cb9a8aa044a3c48a75` (the tip this branch
merged, at `d4ccd285`, one commit before this ratification). The packet's own
`tasks.md` § 5.1–5.12 already carries the gate set taken in the PR #981 bench
round at `origin/main` `0805c3bb`; the figures here are RE-DERIVED at this
lane's own merge to `1f068646` and after the ratification edits, not carried
across the two merges the packet took since.

- **`OPENSPEC_TELEMETRY=0 openspec validate report-stale-grandfather-dispositions
  --strict`** (PATH CLI, 1.2.0) → **exit 0**. *"Change
  'report-stale-grandfather-dispositions' is valid"*.
- **`python3 scripts/validate-openspec-cli-pin.py --change
  report-stale-grandfather-dispositions --no-cache`** (pinned CLI, 1.12.0) →
  **exit 0**. Content address verified (`integrity sha512-oFE2Lj7WVSc87nSi…`),
  dependency closure verified (80 packages, `lockfile_integrity
  sha512-aw5lIN45tQq2WZll…`, `npm ci --ignore-scripts`), *"Totals: 1 passed, 0
  failed (1 items)"*. **BOTH CLI GENERATIONS ACCEPT THE RATIFIED PACKET.**
- **`OPENSPEC_TELEMETRY=0 openspec validate --all --strict`** (PATH, 1.2.0) →
  branch **exit 1**, *"Totals: 101 passed, 2 failed (103 items)"*; control at
  `1f068646` **exit 1**, *"Totals: 100 passed, 2 failed (102 items)"*. **THE
  TWO FAILURES ARE IDENTICAL ON BOTH SIDES** —
  `change/disposition-codexfactory-declared-renames` and
  `change/disposition-codexfactory-floor-relocation-retitle` — so this packet
  adds exactly ONE passing item and no failure; this is `main`'s own standing
  state and not this packet's doing.
- **`python3 scripts/validate-openspec-cli-pin.py --all --cache-dir <scratch>`**
  (pinned, 1.12.0) → branch **exit 0**, *"Totals: 101 passed, 2 failed (103
  items)"*; control **exit 0**, *"Totals: 100 passed, 2 failed (102 items)"* —
  both read *"every target validated --strict with 0 UNDISPOSITIONED failures.
  THIS IS NOT A CLEAN TREE: 2 finding(s) are ACCEPTED EXCEPTIONS"*, the SAME
  two on both sides (`add-chain-attestation` / `signed-execution-chain`, and
  `add-composed-view-authoring` / `ideation-dashboard`, each *"accepted by:
  Brett Heap, 2026-09-05, 'take exit 2'"*). **IDENTICAL, ENTRY FOR ENTRY.**
- **`python3 scripts/proposal-support.py . verify
  report-stale-grandfather-dispositions`** → **exit 0**, *"proposal support
  verification ok"*.
- **`python3 scripts/validate-sequenced-after.py .`** → **exit 0**,
  *"sequenced_after validation passed (41 active changes, 11 declaring the
  field)"*; *"archive-date agreement passed"*; *"archive-date-vs-commit
  agreement passed (… 12 disposition(s) in force, enforcement error)"*. And
  **`--ledger-diff`** → **exit 0**, *"per-change sweep ledger consistent with
  the corpus (204 rows)"* — the seed this packet's own commit `37427342` took
  still agrees with the corpus at this head; **no re-seed is owed.**
- **`python3 scripts/validate-scope-globs.py .`** → **exit 0**,
  *"scope_globs validation passed (all active changes conform)"*.
- **`python3 scripts/doc-health.py --single-repo .`** → **exit 0**, headline
  *"Findings: 31 critical, 5 error, 23 warning, 16 info. New regressions vs
  previous report: 0."* on both branch and control, **NORMALIZED-IDENTICAL**
  (repo-basename token substituted before diffing — the two clones' directory
  names differ and nothing else should): **0 diff lines** on the steady-state
  re-run. **Zero findings name this packet** (`grep -c
  'report-stale-grandfather-dispositions'` over the report → 0), which is the
  asymmetry `design.md` D2 and `tasks.md` § 5.8/§ 7.4 already pin: a
  `--single-repo` run has no aggregation root, so the arm this packet adds
  reports nothing in this repository's own gate. **ONE TRANSIENT LINE WAS
  OBSERVED AND IS DISCLOSED RATHER THAN SUPPRESSED**: a single branch run
  produced one extra `Skipped:` note under `release-tag-publication`
  (*"the published refs for contract-v3.6 could not be consulted"*) — a live
  network check, unrelated to anything this packet touches
  (`contracts/releases/contract-v3.6*` is not in this diff). Re-run twice more
  on the branch and twice on the control under the same heavy concurrent load
  (multiple sessions on this host), the note appeared exactly once and did not
  reproduce; the steady-state comparison quoted above (0 diff lines) is the
  repeatable result.
- **`python3 -m pytest tests/doc-health/test_grandfather_dispositions.py -q`**
  → **exit 0, 40 passed** (1.48s — the rig this packet extends, 23 → 40 test
  functions).
- **`python3 -m pytest tests/doc-health -q --tb=no`** → branch **exit 0, 1742
  passed** (7 warnings, 336.63s); control **exit 0, 1725 passed** (7 warnings,
  322.02s — machine under heavy multi-lane load throughout, hence slow on both
  sides). **THE DIFFERENCE IS EXACTLY SEVENTEEN**,
  matching `design.md` D3's net-new-test claim for this file (18 added, 1
  renamed) with no other file in `tests/doc-health/` gaining or losing a test
  function.

**NOTHING IN THIS COMMIT TOUCHES `scripts/` OR `tests/`.** Every gate above was
re-run to confirm the RATIFICATION (a documentation-only commit: `.openspec.yaml`,
`proposal.md`, `design.md`, `tasks.md`, `README.md`, and the two new
`review/*.md` files) changed no measured figure that a code or test edit would
have moved — and none did, except that this repository's own openspec corpus
now carries one more `Status: ratified` document, which is exactly what
`openspec validate --all --strict`'s ONE EXTRA PASSING ITEM already shows.

Every path in this file is repo-relative.
