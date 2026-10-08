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

- **No subcommand: the self-test.** It loads every family schema with `Draft202012Validator` and `FormatChecker` through a `referencing.Registry`, checks that both registries are closed, checks corpus index closure and digests, and adjudicates every vector with `scripts/council_convening/`. It also checks refusal-code and requirement coverage, and runs `generate --check`.
- **`check`.** Validates real records by `kind` against shape and every offline rule: identifiers, digests, roster composition from the record's own projection, signing-context reconstruction and signature verification where a record carries one, and binding derivation against `repository-identity.yaml`. Rules that need an environment oracle cannot run offline. They are reported as `note: not checkable offline: <rule>`, never passed. `--historical` classifies each record by its recorded protocol and verifies only under that protocol (data-model E1).
- **`select`.** Compares two E11 selections and checks the replacement's admission eligibility.
- **`corpus`.** Prints the index summary: totals, the agreement-set count, and the index's raw SHA-256. `--json` prints it machine-readably for successor tooling.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | No ERROR. WARNs are allowed unless `--strict` is set. |
| 1 | Findings: at least one ERROR, or a WARN under `--strict`. |
| 2 | Harness or dependency failure: a schema that does not load, a missing reused module, an unreadable path. |

Exit 2 is never reported as a pass or as a finding. The same convention holds in `validate-contract-release.py` and `validate-clearing-dispatch.py`.

## Output

Each finding is one line, `ERROR [code] message` or `WARN  [code] message`; each proof-of-work line is `note  message`. Codes are kebab-case and family-scoped. A record refusal surfaces as `council-convening-<refusal-code with _ replaced by ->`. For example, `roster_mismatch` becomes `council-convening-roster-mismatch`. Messages name members and never echo a value that a secret detector matches.

## Validator-level finding codes

| Code | When |
|---|---|
| `council-convening-schema` | A record fails its schema. The record's malformed refusal is also named. |
| `council-convening-registry-closure` | A registry gains, loses or renames an entry against the frozen ratified set. |
| `council-convening-index-closure` | A corpus file is unindexed, an indexed file is missing, a `case_id` is repeated, or a row is out of order. |
| `council-convening-index-digest` | A row's `sha256` does not match the file's bytes. |
| `council-convening-vector-outcome-mismatch` | The reference implementation's outcome, refusal or `derived` value differs from `expected`. |
| `council-convening-refusal-code-without-probe` | A closed refusal code has no vector. |
| `council-convening-requirement-without-probe` | An FR-001–FR-012 or SC-001–SC-003 is cited by no vector. |
| `council-convening-generator-drift` | `generate --check` differs from the committed corpus. |
| `council-convening-legacy-protocol-deprecated` | WARN: a legacy-classified record, while the registry status is `deprecated`. |
| `council-convening-not-offline-checkable` | A note, never an error. |

## Proof-of-work notes, asserted by the CI gate

```text
note  schemas loaded: <n> (family) + digest-construction
note  protocol registry closed: 2 entries
note  predicate registry closed: 2 predicates, 2 input contracts
note  corpus index: <n> vectors, <m> both-sides, sha256:<hex>
note  vectors adjudicated: <n>/<n>
note  refusal codes probed: <k>/<k>
note  requirements probed: FR-001..FR-012, SC-001..SC-003
note  generator reproduced corpus byte-for-byte
```

The gate step fails when any of these is absent, as well as on any ERROR (R17).
