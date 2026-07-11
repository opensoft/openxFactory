# Contract: F0 Evidence Outputs

**Feature**: 002-avc-f0-feasibility | Phase 1 design artifact

Every run emits three artifacts, written **directly and atomically** under
`openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/` — the single committed
evidence location, with no second copy (Q5 / FR-015, FR-021, SC-011).

## Artifacts

| File | Format | Schema | Notes |
|------|--------|--------|-------|
| `f0-results.json` | JSON | 002-owned `f0-results.schema.yaml` (Draft 2020-12) | machine-readable; validates with zero errors (SC-008) |
| `f0-results.md` | Markdown | — | narrative; its SHA-256 is bound into `f0-results.json.report_sha256` |
| `f0-interface-impact.yaml` | YAML | 002-owned [`f0-interface-impact.schema.yaml`](./f0-interface-impact.schema.yaml) | always emitted; empty `variances` on a clean pass |

## Schema ownership & drift guard

Both schemas are owned by 002 and live at `experiments/avatar-brokered-call/schemas/`. An
offline test asserts `f0-results.schema.yaml` is byte-identical (sha256 `a52f2abe…`) to the
OpenSpec-registered supporting-docs copy, so the owned source never diverges from the
registered snapshot. `f0-interface-impact.schema.yaml` is newly authored by 002.

## Redaction allowlist (fail-closed — FR-017, SC-007)

Evidence is serialized only from typed models whose fields are an explicit allowlist:
durations (ms), enum statuses, SHA-256 hashes, bounded reason/assertion codes, and small
bounded notes. Before writing, a scan rejects any prohibited class:

- credential material (key prefixes/tokens);
- SDP (`v=0`, `m=`, `a=` lines) and ICE candidates;
- raw provider payloads/headers;
- audio bytes and transcript text;
- arbitrary or high-cardinality subject identifiers (provider IDs appear only as hashes);
- unbounded strings (all string fields are length-capped).

A single finding ⇒ `redaction_scan.status = FAIL`, overall `FAIL`, and the run does **not**
commit evidence (CLI exit 3). The scan also covers logs, traces, and crash output.

## Classification (FR-016)

`overall` = `PASS` only if every mandatory trial ran, every assertion passed, all metric
bounds held, and redaction passed; `FAIL` on any reproduced contrary observation, metric-bound
miss, or redaction finding; `INCONCLUSIVE` if a mandatory trial could not run / lacked
evidence, the candidate was unavailable, or the acceptance map was absent/mismatched — never
`PASS`. See [data-model.md](../data-model.md#overall-classification-fr-016-derivation).
