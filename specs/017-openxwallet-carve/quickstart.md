# Quickstart — reproduce P2's proof from scratch

**Feature**: `017-openxwallet-carve` · **Date**: 2026-08-26

A third party with `git`, `git filter-repo`, Python 3.12 and read access to both
repositories can reproduce every claim P2 makes. No host-absolute path appears
below; set `$WORK` to any scratch directory.

## Prerequisites

```sh
git --version            # >= 2.40
git filter-repo --version
python3 --version        # 3.12
python3 -m pip install pyyaml jsonschema rfc3339-validator pytest
export WORK=<any scratch dir>
export CARVE_COMMIT=30565e48ffe3d8a9773e10af33425701845e10f6
```

## 1. The control: the recorded digests already describe the carve commit

```sh
git clone git@github.com:opensoft/openxFactory.git "$WORK/openxFactory-src"
git -C "$WORK/openxFactory-src" checkout -q "$CARVE_COMMIT"
```

Recompute each of the eight `sha256:` values in
`contracts/manifest.yaml` over the file its row names.
**Expected: 8/8 match.** This is the control — without it, a post-carve match
would prove the manifest stale rather than the carve faithful.

## 2. Completeness

```sh
git clone git@github.com:opensoft/openXwallet.git "$WORK/openXwallet"
git -C "$WORK/openXwallet" ls-files | sort > "$WORK/actual.txt"
git -C "$WORK/openxFactory-src" ls-tree -r --name-only "$CARVE_COMMIT" -- \
  contracts/openxwallet/ contracts/openxwallet-agent-profile/ \
  scripts/validate-openxwallet.py scripts/wallet-yaml-syntax-gate.py \
  tests/wallet_yaml_syntax_gate/ .github/workflows/wallet-validation.yml \
  openspec/specs/openxwallet/ openspec/specs/openxwallet-agent-profile/ \
  openspec/changes/archive/2026-08-08-add-openxwallet/ \
  specs/006-openxwallet-contracts/ specs/010-wallet-validator-ci/ \
  specs/012-wallet-issuer-anchor/ | sort > "$WORK/expected.txt"
```

`diff "$WORK/expected.txt" "$WORK/actual.txt"` — note that the carved repository
also holds the SCAFFOLD files, so compare `expected.txt` against `actual.txt`
filtered to the twelve prefixes. **Expected: empty diff; 100 carved files.**

## 3. The counts

**Expected**: 7 under `specs/006-openxwallet-contracts/`; 32 under
`contracts/openxwallet/examples/negative/`; 4 under
`contracts/openxwallet-agent-profile/examples/negative/`; 36 together.

## 4. Part one of the proof — eight digests

Recompute the eight in the CARVED tree. **Expected: 8/8 equal to §1's values.**

## 5. Part two — the empty diff

```sh
for p in contracts/openxwallet contracts/openxwallet-agent-profile \
         tests/wallet_yaml_syntax_gate specs/006-openxwallet-contracts \
         specs/010-wallet-validator-ci specs/012-wallet-issuer-anchor \
         openspec/changes/archive/2026-08-08-add-openxwallet; do
  diff -r "$WORK/openxFactory-src/$p" "$WORK/openXwallet/$p"
done
for f in scripts/validate-openxwallet.py scripts/wallet-yaml-syntax-gate.py; do
  diff "$WORK/openxFactory-src/$f" "$WORK/openXwallet/$f"
done
```

**Expected: no output at all.**

## 6. The two promoted specs — exactly two changed lines each

```sh
for s in openxwallet openxwallet-agent-profile; do
  diff "$WORK/openxFactory-src/openspec/specs/$s/spec.md" \
       "$WORK/openXwallet/openspec/specs/$s/spec.md"
done
```

**Expected**: line 4 (the `## Purpose` placeholder → a real Purpose) and the
`openxFactory SHALL` → `openXwallet SHALL` subject rewrite. Nothing else.

## 7. The one declared post-carve edit to a carved file

```sh
diff "$WORK/openxFactory-src/.github/workflows/wallet-validation.yml" \
     "$WORK/openXwallet/.github/workflows/wallet-validation.yml"
```

**Expected**: exactly one added step — `python3 scripts/verify-contract-pin.py`
— placed before the syntax gate. This file is NOT in the byte-identity floor
(task 3.24 enumerates the floor without it); the edit is declared here so it is
never mistaken for drift.

## 8. The gates, offline

```sh
cd "$WORK/openXwallet"
python3 scripts/verify-contract-pin.py      # expect: OK, exit 0
python3 scripts/wallet-yaml-syntax-gate.py .
python3 scripts/validate-openxwallet.py .
python3 scripts/validate-openxwallet.py . --strict
python3 -m pytest tests/ -q
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
```

**Expected: every one exits 0.**

## 9. The verifier actually refuses (V8)

```sh
printf '\n# tamper\n' >> contracts/schemas/hermes-job-envelope.schema.yaml
python3 scripts/verify-contract-pin.py ; echo "exit=$?"   # expect exit=1
git checkout -- contracts/schemas/hermes-job-envelope.schema.yaml
```

**Expected**: exit 1, a drift finding, and both remediation lines. A verifier that
has never refused is not known to refuse.

## 10. Branch protection and the tag

```sh
gh api repos/opensoft/openXwallet/rules/branches/main
git -C "$WORK/openXwallet" tag -l -n99 wallet-v1.0
```

**Expected**: the required status checks present with the ruleset ACTIVE; the tag
annotated and naming `$CARVE_COMMIT`.
