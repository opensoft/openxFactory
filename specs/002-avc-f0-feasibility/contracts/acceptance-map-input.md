# Contract: Baseline Acceptance-Map Input (ACR-ID sourcing)

**Feature**: 002-avc-f0-feasibility | Phase 1 design artifact

F0 sources the concrete `ACR-*` IDs its interface-impact report cites from the versioned
kernel acceptance map (Q3 / FR-018). This is a **read-only** input; F0 never edits it and the
contract-kernel owner retains disposition of the IDs.

## Source

```
openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml
```

## Ingestion & digest gate

1. Read the map; require `interface_baseline == avatar-client-parallel-v1`.
2. Compute its SHA-256; compare to the pinned `--acceptance-map-sha256`.
3. Record `{source_path, source_commit, content_sha256}` into
   `f0-interface-impact.yaml.acceptance_map`.
4. Parse requirement IDs; F0-relevant requirements (with `live_f0` evidence and this change in
   `owner_changes`) are:

   | ID | Title | F0 relevance |
   |----|-------|--------------|
   | ACR-003 | Brokered direct media with sideband control | ordering, held answer, readiness ceiling, revocation |
   | ACR-008 | Consent-before-capture and enforceable speech gates | revocation bound (ACR-008-S06) |
   | ACR-011 | Redacted telemetry and latency evidence | redaction, latency markers |
   | ACR-012 | Deterministic-first release gating and kill switches | F0-gates-publication, kill path |

## Fail-closed rule

Missing file, wrong `interface_baseline`, or digest mismatch ⇒ the run is `INCONCLUSIVE`
(never `PASS`/`FAIL` inferred), and F0 **mints no placeholder IDs** (FR-018). Any variance
cites only concrete IDs present in the digest-verified map.
