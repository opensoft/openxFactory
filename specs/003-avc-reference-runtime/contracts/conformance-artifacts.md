# Contract: Conformance & Realization Artifacts

**Feature**: 003-avc-reference-runtime | **Date**: 2026-07-11

Two runtime-owned YAML artifacts make conformance machine-checkable and record realization
evidence. Both live under `tests/avatar_runtime/conformance/`, carry `schema_version` + `kind`
(constitution Principle IV), and are validated by `check_conformance.py` and the final
conformance run. Shapes are normative; exact field encodings settle in implementation.

## 1. `scenario-test-map.yaml`  (FR-034, Q6)

Binds every **required** scenario ID (runtime-owned `ARR-*` + applicable kernel `ACR-*`) to
exactly ONE entry per scenario, whose disposition is `mapped` (a list of one-or-more collected
test node IDs), `non_applicable` (with rationale), or `gate` (a non-pytest checker/gate evidence
reference).

The **required set** is derived from BOTH acceptance sources, each digest-verified: (a) the
runtime `ARR-*` map and (b) the client `ACR-*` baseline map (C2). Neither is duplicated into a
hand-maintained enumeration (FR-034a).

```yaml
schema_version: 1
kind: avatar-runtime-scenario-test-map
acceptance_sources:
  # (a) runtime-owned ARR required-set source (34 ARR scenarios)
  - id: avatar-reference-runtime
    role: arr
    path: tests/avatar_runtime/conformance/avatar-reference-runtime-acceptance-map.yaml
    source_commit: <commit>                 # verified
    digest: <sha256>                        # verified — recorded in realization-pin.yaml (survives change-dir archival)
  # (b) client ACR baseline source during parallel work (applicable ACR subset)
  - id: avatar-client-parallel-v1
    role: acr
    path: openspec/changes/define-avatar-client-contract-kernel/supporting-docs/avatar-client-acceptance-map.yaml
    source_commit: <commit>                 # verified
    digest: <sha256>                        # verified
  # at realization the ACR source switches to:
  # - id: avatar-client-released
  #   role: acr
  #   path: contracts/avatar-client/acceptance-map.yaml
  #   source_commit: <commit>
  #   digest: <sha256>
mappings:
  # 'mapped' — ONE entry per scenario; dual-story coverage lists ALL its nodes (never duplicate entries) (F1)
  - scenario_id: ARR-004-S01
    disposition: mapped
    test_node_ids:
      - "tests/avatar_runtime/test_grant_retry.py::test_exact_retry_returns_same_grant"
  - scenario_id: ARR-007-S01                 # covered by BOTH US1 and US3 tests — one entry, both nodes (F1)
    disposition: mapped
    test_node_ids:
      - "tests/avatar_runtime/test_authority_ports.py::test_purpose_mapping_absent_denies"
      - "tests/avatar_runtime/test_failclosed_inspection.py::test_purpose_mapping_absent_denies"
  - scenario_id: ARR-007-S02                 # confirmation stale/superseded (C1)
    disposition: mapped
    test_node_ids:
      - "tests/avatar_runtime/test_operation_confirmation.py::test_superseded_confirmation_blocks_operation"
  - scenario_id: ARR-008-S04                 # non-pytest evidence: the diff/ownership gate (E1)
    disposition: gate
    gate: git-diff-ownership
    evidence: "T060 git diff --check + 0 sibling-owned file changes"
  - scenario_id: ACR-XX-SNN
    disposition: non_applicable
    rationale: "Deployment-only scenario; no reference-runtime surface. See design Non-Goals."
```

**Checker rules** (`check_conformance.py` — fails the run on any of):

| Failure | Meaning |
|---------|---------|
| `missing` | A required scenario_id from the acceptance source(s) has no mapping entry. |
| `duplicate` | A scenario_id appears in more than one entry, or an entry mixes dispositions. (Multiple `test_node_ids` **within one** `mapped` entry is valid and expected for dual-story coverage — F1.) |
| `dangling` | A `test_node_ids` entry (of a `mapped` disposition) does not exist in the collected test set. `gate` and `non_applicable` entries are exempt (they carry no pytest node — E1). |
| `skipped-required` | A required scenario's mapped test is skipped/xfailed in the run. |
| `unknown` | A mapping references a scenario_id not present in either acceptance source. |

The checker derives the **required** set from BOTH digest-verified `acceptance_sources` — the
runtime `ARR-*` map (role `arr`) and the client `ACR-*` map (role `acr`) — never a second
hand-maintained enumeration (FR-034a, C2). All 34 `ARR-*` scenarios are `mapped` or `gate`
(SC-001); applicable `ACR-*` are `mapped`/`gate` or `non_applicable` with rationale (SC-002).
Because each acceptance-source map currently lives under an OpenSpec change dir that archives on
landing, the checker records each source's verified content digest in `realization-pin.yaml`
(below) so the required-set source remains content-addressed and reproducible post-archival (C2).

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
  acceptance_source_digests:                 # C2: content-addresses the required-set sources (survive change-dir archival)
    arr: <sha256>                            # avatar-reference-runtime-acceptance-map.yaml at realization
    acr: <sha256>                            # released contracts/avatar-client/acceptance-map.yaml
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
