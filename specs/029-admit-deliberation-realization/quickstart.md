# Quickstart: verifying this realization

**Feature**: [spec.md](./spec.md) | **Lane**: `hermes-wallet-exercise`

Everything below runs from the repository root of a checkout of this branch.

## 0. The one prerequisite

```bash
git submodule update --init openXwallet
python3 -c "import yaml, jsonschema, rfc3339_validator"
```

The canonical clearing validator REFUSES (exit 2) without the pinned openXwallet
decoders rather than deriving keys with arithmetic of its own.

## 1. The register now holds two operations

```bash
python3 scripts/validate-clearing-dispatch.py . | grep 'registered operation'
```

Expected:

```
note  permitted-operations register read: contracts/clearing/permitted-operations.registry.yaml (2 registered operations)
```

## 2. The whole family is clean, and every closed refusal is still red-proven

```bash
python3 scripts/validate-clearing-dispatch.py .
```

Expected tail: `26/26 closed refusal codes red-proven` and
`validate-clearing-dispatch: 0 error(s), 0 warning(s)`. **26 is not a typo and
must not move**: the new negative fixture declares the family's SHAPE refusal
`schema`, which is deliberately not a member of the closed set.

## 3. The new return schema does what the entry says it does

```bash
# the positive example validates clean
python3 scripts/validate-clearing-dispatch.py contracts/clearing/examples/deliberation-return.example.yaml
```

## 4. The family's own tests

```bash
python3 -m pytest tests/clearing -q
```

## 5. The full suite (what CI runs)

```bash
python3 -m pytest tests/ -q -m "not postgres"
```

Two modules outside `tests/clearing/` gate this change and are easy to forget:

```bash
python3 -m pytest tests/intent-compliance/test_release_boundary.py -q   # the bundle-number enum
python3 -m pytest tests/manifest_digests -q                             # every registered row's digest
```

## 6. OpenSpec

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

## 7. Prove each frozen copy fails ALONE (ratified task 2.6)

Five reverts, one at a time, each expected RED:

```bash
# (a) the validator's frozen set
#     RATIFIED_OPERATIONS -> frozenset({"readiness-diagnostic"})
python3 scripts/validate-clearing-dispatch.py . ; git checkout -- scripts/validate-clearing-dispatch.py

# (b) the test's INDEPENDENT copy
#     RATIFIED -> frozenset({"readiness-diagnostic"})
python3 -m pytest tests/clearing/test_register_closure.py -q ; git checkout -- tests/clearing/test_register_closure.py

# (c) the instance — drop entry two
python3 -m pytest tests/clearing -q ; git checkout -- contracts/clearing/permitted-operations.registry.yaml

# (d) the CI gate's literal grep -> "(1 registered operation)"
python3 -m pytest tests/clearing/test_clearing_gate_wiring.py -q ; git checkout -- .github/workflows/clearing-dispatch-gate.yml

# (e) the test that pins (d)'s literal from a second file
python3 -m pytest tests/clearing/test_clearing_gate_wiring.py -q ; git checkout -- tests/clearing/test_clearing_gate_wiring.py
```

And the three pinned numerals D9 names: the schema-filename list
(`tests/clearing/test_schemas.py`), the manifest row count and the moved row
digests (`tests/clearing/test_clearing_manifest_rows.py`).

## 8. What is NOT verifiable here

- The `deliberation` HOST JOB. It does not exist; this slice authorizes it and
  does not declare it.
- The retirement of `council-deliberation-worker.yml`. That is the clearing
  repository's act, in the same commit as the host job.
- The annotated `contract-v3.4` tag. The repository owner's act at the LANDED
  sha, after `verify-commit` is re-run there.
