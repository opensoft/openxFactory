# Contract: Conformance & Realization Artifacts

**Feature**: 003-avc-reference-runtime | **Date**: 2026-07-11

Two runtime-owned YAML artifacts make conformance machine-checkable and record realization
evidence. Both live under `tests/avatar_runtime/conformance/`, carry `schema_version` + `kind`
(constitution Principle IV), and are validated by `check_conformance.py` and the final
conformance run. Shapes are normative; exact field encodings settle in implementation.

## 1. `scenario-test-map.yaml`  (FR-034, Q6)

Binds every **required** scenario ID (runtime-owned `ARR-*` + applicable kernel `ACR-*`) to
either collected test node IDs or an explicit non-applicability disposition.

```yaml
schema_version: 1
kind: avatar-runtime-scenario-test-map
acceptance_sources:
  - id: avatar-client-parallel-v1          # provisional baseline during parallel work
    path: openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml
    source_commit: <commit>                 # verified
    digest: <sha256>                        # verified
  # at realization, replaced by:
  # - id: avatar-client-released
  #   path: contracts/avatar-client/acceptance-map.yaml
  #   source_commit: <commit>
  #   digest: <sha256>
mappings:
  - scenario_id: ARR-004-S01
    disposition: mapped
    test_node_ids:
      - "tests/avatar_runtime/test_grant_retry.py::test_exact_retry_returns_same_grant"
  - scenario_id: ACR-XX-SNN
    disposition: non_applicable
    rationale: "Deployment-only scenario; no reference-runtime surface. See design Non-Goals."
```

**Checker rules** (`check_conformance.py` — fails the run on any of):

| Failure | Meaning |
|---------|---------|
| `missing` | A required scenario_id from the acceptance source(s) has no mapping. |
| `duplicate` | A scenario_id appears more than once, or a `mapped` entry also `non_applicable`. |
| `dangling` | A `test_node_ids` entry does not exist in the collected test set. |
| `skipped-required` | A required scenario's mapped test is skipped/xfailed in the run. |
| `unknown` | A mapping references a scenario_id not present in the acceptance source(s). |

The checker derives the **required** set from the digest-verified `acceptance_sources` (never a
second hand-maintained enumeration — FR-034a). All `ARR-*` scenarios are `mapped` (SC-001);
applicable `ACR-*` are `mapped` or `non_applicable` with rationale (SC-002).

## 2. `realization-pin.yaml`  (FR-005, SC-006, Q7)

Records the five coordinated release coordinates and the final conformance result. **Absent
before realization**; populated only when the released kernel exists. A bare tag without the
exact commit and all digests fails realization (FR-005, ARR-002-S03).

```yaml
schema_version: 1
kind: avatar-runtime-realization-pin
released_kernel:
  tag: contract-vX.Y                        # (1) released tag
  commit: <exact-commit-sha>                # (2) exact commit
  file_digests:                             # (3) per-file SHA-256 of consumed contract files
    contracts/avatar-client/acceptance-map.yaml: <sha256>
    # ... each consumed canonical file
  interface_lock_digest: <sha256>           # (4) interface-lock digest
  acceptance_map_digest: <sha256>           # (5) acceptance-map digest
conformance:
  provisional_adapter_disabled: true        # FR-035: final run with provisional seam off
  seeds: [<seed1>, <seed2>, ...]            # recorded pytest-randomly seeds (SC-003)
  suite_result: pass
  scenario_test_map_result: pass
  boundary_gate_result: pass                 # scripts/validate-avatar-runtime.py
  canonical_matches_provisional: true        # FR-035: no divergence
```

**Validation** (part of final conformance):

- All five `released_kernel` coordinates present and non-empty, else realization **fails**.
- `provisional_adapter_disabled: true` and `boundary_gate_result: pass` required (FR-035, FR-004a).
- `canonical_matches_provisional: false` → realization **fails**; mapped behavior corrected
  (FR-035, ARR-002-S03).

## Ownership & read-only note

Both acceptance-map source paths are **sibling-owned** and consumed read-only; this feature never
edits them (FR-036). The only artifacts this feature writes are these two files (inside
`tests/avatar_runtime/`), the runtime package, the test suite, and the single
`scripts/validate-avatar-runtime.py` gate + its README index line (SC-008).
