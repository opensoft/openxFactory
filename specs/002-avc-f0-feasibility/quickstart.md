# Quickstart & Validation Guide: Avatar Brokered-Call F0 Harness

**Feature**: 002-avc-f0-feasibility | Phase 1 design artifact

This guide proves the harness works end-to-end. The **offline** path requires no lab key and
is sufficient for feature completion (a terminal `INCONCLUSIVE` record is valid — SC-013). The
**live** path additionally exercises the provider when `OPENAI_API_KEY` is present.

## Prerequisites

- Python 3.12 (pinned by `experiments/avatar-brokered-call/.python-version`).
- Dependencies installed from the committed hash-locked file (no unpinned installs).
- No lab key needed for the offline path. Credential preparation for the future live path
  follows the [OpenAI Realtime F0 Lab Credential SOP](../../docs/sops/openai-realtime-f0-lab-credential.md):
  `OPENAI_API_KEY` is injected into the process from an external secret binding and is
  never passed as an argument or stored in this repository.

## Setup

```bash
cd experiments/avatar-brokered-call
python -m venv .venv && . .venv/bin/activate
pip install --require-hashes -r requirements.lock
```

## Offline validation (no provider call)

```bash
# Full offline self-test suite
pytest tests/offline -q

# Or drive the harness in offline-only mode
python -m avatar_f0 run --offline-selftest
```

**Expected outcomes** (each is an offline test; see [contracts](./contracts) and
[data-model.md](./data-model.md) for shapes):

| Check | Expected |
|-------|----------|
| Preflight rejection | tenant data / tools-enabled / key-in-args / readiness > 5000 ms / non-lab profile ⇒ exit 2, no provider call (SC-009) |
| Credential safeguard | key never appears in any written artifact, log, or trace (FR-001) |
| Acceptance-map digest gate | matching digest ⇒ ACR IDs loaded; missing/mismatch ⇒ INCONCLUSIVE, no placeholder IDs (FR-018) |
| Fixture determinism | regenerated audit fixture reproduces the pinned byte SHA-256 (Q7) |
| Schema drift guard | `schemas/f0-results.schema.yaml` byte-matches the registered copy (sha256 `a52f2abe…`) |
| Evidence schema validity | a synthesized results record validates against `f0-results.schema.yaml`; interface-impact validates against `f0-interface-impact.schema.yaml` (SC-008) |
| Redaction fail-closed | injected prohibited content ⇒ `redaction_scan.status=FAIL`, overall FAIL, no commit, exit 3 (FR-017, SC-007) |
| Group/assertion accounting | exactly six groups / 70 trials; readiness-timeout inside F0-C; cleanup cross-cutting (Q4) |
| Classification | PASS/FAIL/INCONCLUSIVE derived per FR-016 (a p95/ceiling miss cannot be averaged away) |

## Credential readiness (live validation currently blocked)

```bash
OPENAI_API_KEY="$(tr -d '\r\n' <"$HOME/.ai-keys/openai.key")"
export OPENAI_API_KEY
test -n "${OPENAI_API_KEY:-}" && printf 'OPENAI_API_KEY=present\n'
```

The current `HttpBroker`, live sideband client, live media peer, and live test are stubs.
The CLI does not call the provider when the key is present; it writes an `INCONCLUSIVE`
record with reason `live_path_deferred`. Credential authentication may be checked using
the SOP, but the command below must not be represented as executable until those stubs are
implemented:

```bash
python -m avatar_f0 run --groups F0-A,F0-B,F0-C,F0-D,F0-E,F0-F
```

**Required outcomes after the live transport is implemented**:

- Three artifacts written under `openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/`
  (`f0-results.json`, `f0-results.md`, `f0-interface-impact.yaml`), and nothing outside the two
  owned locations (SC-011).
- Ordering holds (media authorized after both control channels verified, before answer
  application/first media); one provider call per request (SC-001).
- Metrics: `sideband_ready_ms` p95 ≤ 3000 / max ≤ 5000; `first_playable_after_authorized_ms`
  p95 ≤ 2000; `hangup_to_terminal_ms` max ≤ 5000 (SC-002/003/005).
- `overall` is exactly one of PASS/FAIL/INCONCLUSIVE.

## No-key behavior

```bash
unset OPENAI_API_KEY
python -m avatar_f0 run
```

**Expected**: no provider call is attempted; a schema-valid `INCONCLUSIVE` record is written
with zero fabricated artifacts (exit 0). This satisfies feature completion (SC-013).

## Gate before commit

Run repo-local validators and `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` from the
`openspec/` root, plus `git diff --check`, and confirm no canonical contract, reference-runtime,
UI, DomainxFactory, or deployment file changed (SC-011). Implementation task detail lives in
`tasks.md` (produced by `/speckit-tasks`), not here.
