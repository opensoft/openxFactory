# Contract: F0 Harness CLI Interface

**Feature**: 002-avc-f0-feasibility | Phase 1 design artifact

The harness exposes one CLI entrypoint under `experiments/avatar-brokered-call/`. It is a
disposable, outbound-only lab tool — it never listens on a socket, deploys, or persists a
provider key.

## Command

```
avatar-f0 run [options]
```

## Inputs

| Option | Default | Contract |
|--------|---------|----------|
| `--groups G[,G...]` | all six | subset of {F0-A,F0-B,F0-C,F0-D,F0-E,F0-F} |
| `--readiness-ms N` | 3000 | 1000–5000; **> 5000 rejected at preflight** |
| `--acceptance-map PATH` | kernel supporting-docs map | repo-relative path |
| `--acceptance-map-sha256 HEX` | pinned | 64-hex; mismatch ⇒ INCONCLUSIVE |
| `--evidence-dir PATH` | change `evidence/` dir | must resolve under the change's evidence dir |
| `--offline-selftest` | off | run offline self-tests only; make no provider call |

**Credential**: read **only** from the `OPENAI_API_KEY` process environment variable (CI or an
approved secret store may inject it; a gitignored local `.env` may populate it). The key MUST
NOT be accepted via any option, and any attempt to pass a credential as an argument, or via a
tracked `.env`/config/evidence file, is rejected at preflight (FR-001, FR-003).

## Preflight rejections (exit non-zero, before any provider call)

Tenant identifiers/content present · tools enabled · credential in arguments/tracked files ·
readiness > 5000 ms · non-lab or unpinned profile. (FR-003, SC-009)

## Outputs (side effects)

Writes exactly three artifacts under the change's `evidence/` directory and nothing outside
its two owned locations (`experiments/avatar-brokered-call/`, the change `evidence/` dir):
`f0-results.json`, `f0-results.md`, `f0-interface-impact.yaml`. See
[evidence-outputs.md](./evidence-outputs.md).

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | run completed; overall status is written to evidence (`PASS`/`FAIL`/`INCONCLUSIVE`) |
| 2 | preflight rejection (invalid/unsafe config) — no provider call attempted |
| 3 | redaction failure detected — run marked `FAIL`, evidence not committed (FR-017) |

**Note**: A terminal `INCONCLUSIVE` (e.g. no lab key, provider unavailable, acceptance-map
absent/mismatch) is a **successful** run of the tool (exit 0) and a valid feature-completion
state — a live `PASS` is not required (SC-013).
