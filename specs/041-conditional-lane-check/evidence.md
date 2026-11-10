# Validation Evidence

Status: draft
Recorded: 2026-11-10

Both repository workflow variants passed 21 actual-shell and structural regression cases. OpenSpec change validation passed. The owner commissioned restoring the in-force rule; new local prose ratification is not asserted. Hosted checks and exact-head review remain required before landing.

Tracked-path probe reconciliation, where applicable, records the measured result below. No admission rule, behavior snapshot, authority floor or protection setting is changed.

Pinned OpenSpec all/strict gate: exit 0 with one existing accepted exception; zero undispositioned failures. Sequenced-after and lifecycle-status validators passed.

The authoritative pin gate, not the unrelated CLI on PATH, supplies corpus acceptance. The PATH CLI reports historical corpus failures; this change is valid under both individual-change validators. No historical text or disposition is altered.

The first sequenced-after suite run found the newly declared empty parent field and stale corpus ledger (5 failures, 302 passes). The draft does not assert a parent/root chain and now omits that optional declaration. The sanctioned generator adds this new packet to the ledger while preserving unchanged rows. The rerun below is authoritative for the reconciled tree.

After reconciliation: lane-line and sequenced-after suites passed 307 tests; generated ledger adds exactly one row and preserves every existing row.
