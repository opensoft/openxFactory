# Canonical validator CLI: `scripts/validate-council-convening.py`

**Feature**: [spec.md](../spec.md) · **Plan**: [plan.md](../plan.md) · House conventions: 028 research R6

## Invocation

```text
python3 scripts/validate-council-convening.py [--strict]
python3 scripts/validate-council-convening.py check [--historical] [--strict] PATH...
python3 scripts/validate-council-convening.py select --producer FILE --consumer FILE
python3 scripts/validate-council-convening.py corpus [--json]
```

The modes:

- **No subcommand: the self-test.** It loads every family schema with `Draft202012Validator` and `FormatChecker` through a `referencing.Registry`, checks that both registries are closed, checks corpus index closure and digests, and adjudicates every vector with `scripts/council_convening/`. It also checks coverage at the commit (refusal codes, finding codes, the `coverage_floor` requirements and the `registry_status` rule), and runs `generate --check`.
- **`check`.** Dispatches each record by `kind`. A protocol-carrying record (E2, E4–E8), or one with no family `kind`, is classified first (data-model E1); registries, bindings, selections and activation evidence are judged by kind alone. Each record is then validated against its shape and every offline rule: identifiers, digests, roster composition from the record's own projection, signing-context reconstruction and signature verification where a record carries one, and binding derivation against `repository-identity.yaml`. Rules that need an environment oracle cannot run offline. They are reported as `note: not checkable offline: <rule>`, never passed. So a `check` that exits 0 says only that the record passed every **offline-checkable** rule; it is never evidence of admission, which also needs the oracle-dependent rules (governed history and tip, facts, the live head, verified claims and issued state). A legacy record is routed, never passed. A replacement record of a kind whose schema has not landed yet is an ERROR. `--historical` (Phase 6) classifies each record by its recorded protocol and verifies only under that protocol.
- **`select`** (Phase 6). Compares two E11 selections and checks the replacement's admission eligibility.
- **`corpus`.** Prints the index summary: totals, the agreement-set count, and the index's raw SHA-256. `--json` prints it machine-readably for successor tooling.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | No ERROR and no routed record. WARNs are allowed unless `--strict` is set. For `check`, this covers the offline-checkable rules only; each rule it could not run is a `note: not checkable offline` line, not a pass. |
| 1 | Findings: at least one ERROR, or a WARN under `--strict`. |
| 2 | Harness or dependency failure: a schema that does not load, a missing reused module, an unreadable path. |
| 3 | `check` only: at least one record was routed to the legacy verifier and nothing was an ERROR. This family gave that record no verdict, so a run that exits 3 is never a pass. The self-test never exits 3: a route vector whose route matches `expected` is a correct adjudication, and the self-test exits 0. |

Exits 2 and 3 are never reported as a pass. Exit 2 is never reported as a finding. The 0/1/2 convention is the one `validate-contract-release.py` and `validate-clearing-dispatch.py` hold. Exit 3 follows the house precedent in `scripts/validate-consent-instruments.py`, `EXIT_NEEDS_DECISION = 3`, which Brett Heap ruled on 2026-09-09 as "Exit 3 = needs a human decision (Recommended)". Here it means that this family cannot give the verdict and another verifier must.

## Output

Each finding is one line, `ERROR [code] message` or `WARN  [code] message`; each proof-of-work line is `note  message`. Codes are kebab-case and family-scoped. A record refusal surfaces as `council-convening-<refusal-code with _ replaced by ->`. For example, `roster_mismatch` becomes `council-convening-roster-mismatch`. Messages name members and never echo a value that a secret detector matches.

## Validator-level finding codes

| Code | When |
|---|---|
| `council-convening-schema` | A record fails its schema. The record's malformed refusal is also named. |
| `council-convening-kind-unknown` | A replacement record of a kind whose schema has not landed at this commit. |
| `council-convening-registry-closure` | A registry gains, loses or renames an entry against the set as landed at this commit. |
| `council-convening-index-closure` | A corpus file is unindexed, an indexed file is missing, a `case_id` is repeated, or a row is out of order. |
| `council-convening-index-digest` | A row's `sha256` does not match the file's bytes. |
| `council-convening-vector-outcome-mismatch` | The reference implementation's outcome, refusal, finding or `derived` value differs from `expected`. |
| `council-convening-vector-registry-status-missing` | A vector whose outcome reads a registry status carries no `registry_status` override. |
| `council-convening-refusal-code-without-probe` | A refusal code in the enumeration at this commit has no vector. |
| `council-convening-finding-code-without-probe` | A finding code in the enumeration at this commit has no vector. |
| `council-convening-requirement-without-probe` | A requirement in the index's `coverage_floor` is cited by no vector. |
| `council-convening-generator-drift` | `generate --check` differs from the committed corpus. |
| `council-convening-legacy-protocol-routed` | A note on the record, with exit 3: a legacy record routed to the legacy verifier. |
| `council-convening-legacy-protocol-deprecated` | WARN, beside the route, while the legacy status is `deprecated`. An ERROR under `--strict`. |
| `council-convening-not-offline-checkable` | A note, never an error. |

## Proof-of-work notes, asserted by the CI gate

These notes are printed from Phase 1. The gate asserts every one of them:

```text
note  schemas loaded: <n> (family) + digest-construction
note  protocol registry closed: 2 entries
note  corpus index: <n> vectors, <m> both-sides, sha256:<hex>
note  vectors adjudicated: <n>/<n>
note  refusal codes probed: <k>/<k>
note  finding codes probed: <f>/<f>
note  requirements probed: <the coverage_floor at this commit>
note  generator reproduced corpus byte-for-byte
```

This note is printed from Phase 2, when the predicate registry lands. T032 adds it to the gate's assertion:

```text
note  predicate registry closed: 2 predicates, 2 input contracts
```

The gate step fails when any asserted note is absent, as well as on any ERROR (R17).
