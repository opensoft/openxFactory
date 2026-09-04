# Quickstart: proving contracts/clearing

**Feature**: 028-clearing-contracts | **Date**: 2026-09-03

Run from the repository root of the `028-clearing-contracts` worktree.

## Prerequisites

```bash
git submodule update --init openXwallet   # the pinned key decoders; the validator REFUSES without it
pip install pyyaml jsonschema rfc3339-validator
```

The gitlink is pinned by `contracts/openxwallet-pin.yaml`. If it is absent the
validator exits `2` and prints the remedy — it never falls back to arithmetic of
its own.

## 1. The validator self-test (no argument = packaged corpus only)

```bash
python3 scripts/validate-clearing-dispatch.py
```

Expected: exit `0`, and notes proving work was done —

```text
note  pinned openXwallet decoders read from openXwallet/scripts/validate-openxwallet.py
note  permitted-operations register read: contracts/clearing/permitted-operations.registry.yaml (1 registered operation)
note  self-test: <N> packaged record(s) validated, <M> negative fixture(s) refused
note  <K>/<K> closed refusal codes red-proven

validate-clearing-dispatch: 0 error(s), 0 warning(s)
```

The refusal-code line is the one that matters: a closed code with no packaged
fixture is a code nobody has ever seen fire, and the run reports
`clearing-refusal-code-without-probe` rather than passing.

## 2. The whole-tree sweep

```bash
python3 scripts/validate-clearing-dispatch.py .
```

Expected: exit `0`, plus

```text
note  repo scan (<abs path>): 0 artifact(s) checked
```

**Zero is the expected state.** No clearing implementation writes a neutral
record yet — `opensoft/xFactory`'s clearing lane emits `key=value` ledger lines
that a later harvester will shape into these records. Zero artifacts is reported
as a fact, never as a pass with nothing behind it.

## 3. Prove the register is CLOSED

```bash
python3 - <<'PY'
import pathlib, yaml
p = pathlib.Path("contracts/clearing/permitted-operations.registry.yaml")
doc = yaml.safe_load(p.read_text())
doc["operations"].append({"operation_id": "deliberation"})
p.write_text(yaml.safe_dump(doc, sort_keys=False))
PY
python3 scripts/validate-clearing-dispatch.py ; echo "exit=$?"
git checkout -- contracts/clearing/permitted-operations.registry.yaml
```

Expected: exit `1` and

```text
ERROR [clearing-register-member-unratified] permitted-operations.registry.yaml: 'deliberation' is not in the ratified member set ...
```

`deliberation` is codexFactory #165's LATER governed change; the refusal is what
keeps it out of this cut.

## 4. Prove the digest construction is not duplicated

```bash
python3 -m pytest tests/clearing/test_digest_by_reference.py -q
```

Asserts that the manifest schema's digest members are structurally identical to
`signed-execution-chain`'s `$defs/digest`, that `sealed_bundle_manifest` is a
member of BOTH the schema enum and `scripts/signed_execution_chain/canonical.py`'s
`SUBJECTS` frozenset, and that no file under `contracts/clearing/` declares a
`construction_name` of its own.

## 5. Prove the origin signature verifies

```bash
python3 -m pytest tests/clearing/test_origin_signature.py -q
```

Covers all three ratified outcomes: a registered producer with a verifying
signature passes; a registered producer presenting hosted provenance alone is
refused with `clearing-origin-signature-missing`; an unregistered producer
presenting hosted provenance passes. The fixture keys are derived from labelled
sha256 digests where no signature must verify, and the one verifying signature
was produced by an ephemeral key whose private half was never written to the
repository.

## 6. The family's own tests, then the whole suite

```bash
python3 -m pytest tests/clearing -q
python3 -m pytest tests/ -q -m "not postgres"        # ~20 min
```

The full suite must show NO new skip: `.github/workflows/pytest-suite.yml` pins
`EXPECT_SKIPPED` exactly while the selected and passed counts are floors that may
only rise.

## 7. Registration surfaces

```bash
python3 scripts/validate-manifest-digests.py
python3 -m pytest tests/clearing/test_clearing_manifest_rows.py -q
python3 scripts/validate-contract-release.py verify-commit --commit "$(git rev-parse HEAD)"
```

The first two prove every `contracts/clearing/` schema carries a manifest row
whose `sha256` recomputes, in BOTH directions. The third verifies the new release
inventory at this commit.

**The annotated tag is NOT published from a branch.** Bundle Realization Order
step 5 publishes `contract-v3.3` at the exact LANDED commit, after `verify-commit`
is re-run there — skipping that re-run at the squash commit is precisely what made
`contract-v3.1` defective.

## 8. The governance gates

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
python3 scripts/proposal-support.py . verify
```

Both were green at this branch's base (`6a39d2ab`) and must stay green. This
feature adds no spec delta, so `openspec validate` should report the same 86
items it did before.
