# Implementation Notes — The Register and Its Reader (S4)

## Operator rulings (Brett Heap, 2026-08-25, in-session)

1. **First grant minted within S4** — without it the register row is
   "documentation that confers nothing" in requirement 2's own words; with it,
   OXWR-R1/R2 get their first positive exercise.
2. **Target repository**: `opensoft/openxFactory` (the pilot).
3. **expires_at**: ~90-day term → `2026-11-23T12:00:00Z`.

## Gate evidence

### Final run (2026-08-25) — ALL GREEN

- Whole-checkout sweep `--strict`: **exit 0** — `repo scan: 2 openxWallet
  artifact(s) validated` (013's wallet + the new grant); corpus note
  unchanged: **17 positives / 36 negatives across 13/13 requirements**
  (SC-001/SC-002).
- Layer-1 self-test: **0 errors** with all EIGHT S4 synthesized-tree probes
  green (SC-003): clean · computed-expiry (register-row-expired +
  grant-state-stale + register-no-active-row simultaneously) · no-active-row
  via `rows: []` (proving no silent early return) · tier-act-unattested ·
  minimal-shape-exceeded · row-malformed · absent-register postures.
- Live production-wiring mutation probe (SC-004): register renamed away →
  sweep FAILED with `register-no-active-row` naming grant-mrc-0001;
  restored → exit 0. Run once, restored immediately; nothing red committed.
- `pytest tests/wallet_yaml_syntax_gate/ -q`: **4 passed**.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: **75 passed /
  0 failed**.
- SC-005 boundary proofs vs branch base dda06ba3: contracts/.github diff
  empty; private-material diff scan clean.

## Development findings recorded

- The empty-`rows` early-return variant SILENTLY SKIPPED the headline
  obligation — caught by the probe during development, fixed by making the
  empty case fall through to the inverse sweep. The comment at that branch
  exists so the simplification never comes back.

## Boundary ledger

- NOT done here, deliberately: codexFactory floor entry BY NAME (§5.4);
  revocation surface + staleness bound (S5); exercise records (S3);
  composition mapping (task 4.4); register CONTRACT SCHEMA (D11 successor);
  multi-holder/multi-target registers; grant-side unattested-cap enforcement
  inside check_grant (cap binds at this reader where admission happens).
- Durable note for S5: when the revocation surface lands on Hermes, its
  lookup must reconcile against THIS file's rows AND their computed expiry —
  the Q1c constraint recorded in the register header is the standing warning
  that this file is an issuance-time snapshot.
