# Avatar F0 Brokered-Call Feasibility Harness

Disposable, tenant-data-free lab experiment for the openxFactory change
`qualify-avatar-brokered-call-feasibility`. It empirically measures whether an
OpenAI-brokered WebRTC call can be created, held under sideband + in-harness control
authorization until media is authorized, and terminated within the required bounds.

> **Not for live use.** A `PASS` never qualifies a provider profile, enables internal-live
> or production media, or opens the kernel publication gate on its own. See
> `specs/002-avc-f0-feasibility/spec.md` (§FR-019/FR-020, SC-012/SC-013).

## Safety & redaction

- The provider credential is read **only** from the `OPENAI_API_KEY` process environment
  variable. The standard local binding is the host-only file defined by the
  [OpenAI Realtime F0 Lab Credential SOP](../../docs/sops/openai-realtime-f0-lab-credential.md);
  CI or an approved secret store may inject it. It is never accepted via CLI args or
  tracked files, and never written to any artifact (FR-001/FR-003).
- Committed evidence is built from an allowlist and re-scanned before writing; a redaction
  finding fails the run closed and blocks the write (FR-017/SC-007). No binary audio is
  committed and no real-user recording is used (Q7).
- A run writes only under `experiments/avatar-brokered-call/` and the change's
  `evidence/` directory (SC-011).

## Setup

```bash
cd experiments/avatar-brokered-call
python3 -m venv .venv           # gitignored
. .venv/bin/activate
pip install -r requirements.lock  # pinned; the lock's content sha256 feeds the profile digest
pip install -e . --no-deps
```

## Offline validation (no lab key)

```bash
pytest tests/offline            # harness self-tests + redaction tests (the DoD offline gate)
avatar-f0 run                   # emits the terminal record; no key => INCONCLUSIVE, exit 0
```

A no-key run is a **valid completion** (SC-013): it attempts no provider call, fabricates
nothing, and writes a schema-valid `INCONCLUSIVE` record to the change `evidence/` dir.

## Credential preparation (live transport pending)

```bash
OPENAI_API_KEY="$(tr -d '\r\n' <"$HOME/.ai-keys/openai.key")"
export OPENAI_API_KEY
test -n "${OPENAI_API_KEY:-}" && printf 'OPENAI_API_KEY=present\n'
```

Do not run or describe this harness as a live 70-trial provider matrix yet. The current
`aiortc`, `websockets`, and `httpx` live clients and the live test remain explicit stubs;
with a key present, the CLI still emits `INCONCLUSIVE` with reason `live_path_deferred`.
The key can be installed and authenticated now, but the live transport and supervised
matrix must be implemented before a provider result can gate contract publication. Follow
the SOP for non-disclosing authentication, container injection, rotation, and revocation.

## Layout

- `src/avatar_f0/` — harness (config/preflight, candidate, credential, clock, control
  stub, sideband/broker/media, trials F0-A…F0-F, assertions, metrics, classification,
  redaction, evidence writer, CLI).
- `schemas/` — 002-owned `f0-results.schema.yaml` (byte-identical to the registered
  supporting-docs copy, drift-guarded) and `f0-interface-impact.schema.yaml`.
- `tests/offline/` — self-tests that run without a key. `tests/live/` — key-gated.
