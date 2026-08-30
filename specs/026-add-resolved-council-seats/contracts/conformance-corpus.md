# Contract: Resolved Council-Convening Conformance Corpus

Status: draft planning contract

## Purpose

Provide one portable indexed corpus that the neutral provider, Hermes consumer,
and codexFactory producer run independently. The corpus proves semantic parity
without sharing runtime evaluator code or relying on mutable network state.

## Realization Layout

```text
contracts/council-convening/fixtures/
├── index.yaml
├── positive/
│   ├── standing-roster.yaml
│   └── conditional-seat-required.yaml
└── negative/
    ├── roster-absent.yaml
    ├── roster-duplicate.yaml
    ├── roster-unknown-seat.yaml
    ├── roster-mismatch.yaml
    ├── provenance-opaque.yaml
    ├── rule-revision-unavailable.yaml
    ├── fact-missing.yaml
    └── candidate-head-stale.yaml
```

## Fixture Record

Every YAML document carries `schema_version` and `kind`. The index entry records:

| Field | Meaning |
|---|---|
| `case_id` | Stable unique case identifier |
| `class` | `positive` or `negative` |
| `path` | Repository-relative fixture path |
| `requirement_ids` | Feature FRs proved by the case |
| `scenario_ids` | Governed RCS scenario IDs proved by the case |
| `input` | Convening plus deterministic immutable-rule/head resolver objects |
| `expected_outcome` | `accept` or `refuse` |
| `expected_primary_finding` | Empty for accept; one stable code for refuse |
| `evidence_id` | Stable evidence-register key |

No fixture may be unindexed, and no index path may be missing, duplicated, or
escape the family directory. Positive fixtures produce zero findings. A negative
fixture passes only when refused for its declared primary finding.

## Required Cases

| Case | Expected result | Primary coverage |
|---|---|---|
| `standing-roster` | accept | standing seats only; freeze-before-jobs handoff |
| `conditional-seat-required` | accept | conditional pull-in; exact facts and rule provenance |
| `roster-absent` | refuse / `roster_absent` | hard cutover; no reconstruction |
| `roster-duplicate` | refuse / `roster_duplicate` | uniqueness |
| `roster-unknown-seat` | refuse / `roster_unknown_seat` | declared-seat closure |
| `roster-mismatch` | refuse / `roster_mismatch` | independent reproduction |
| `provenance-opaque` | refuse / `provenance_opaque` | conclusion-only evidence rejected |
| `rule-revision-unavailable` | refuse / `rule_revision_unavailable` | immutable rule fail-closed |
| `fact-missing` | refuse / `fact_missing` | consumed fact completeness |
| `candidate-head-stale` | refuse / `candidate_head_stale` | exact candidate revision binding |

Successor-only tests extend this corpus with job issuance, snapshot persistence,
return admission, rich outcome comparison, private-key isolation, and existing
failure/recovery regression evidence. Those artifacts remain in their owning
repositories and cite the provider bundle and fixture IDs.

## Validator CLI

The planned `scripts/validate-council-convening.py` interface is:

```text
validate-council-convening.py --strict [--case CASE_ID] [--json]
```

- default: validate schema, index parity, and every fixture;
- `--case`: run one indexed case by exact ID;
- `--json`: emit a deterministic machine result;
- exit `0`: requested suite matches every declared expectation;
- exit `1`: conformance finding or expectation mismatch;
- exit `2`: invocation, missing dependency, unavailable input, or harness error.

Machine output includes the case ID, expected and actual outcome, ordered finding
codes, evidence ID, and contract version. It contains no local absolute path.
