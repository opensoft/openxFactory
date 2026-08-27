# Contract: the carve surface

**Feature**: `017-openxwallet-carve` · **Authority**: ratified design D7, task 3.5

## The invocation

```sh
git filter-repo \
  --path contracts/openxwallet/ \
  --path contracts/openxwallet-agent-profile/ \
  --path scripts/validate-openxwallet.py \
  --path scripts/wallet-yaml-syntax-gate.py \
  --path tests/wallet_yaml_syntax_gate/ \
  --path .github/workflows/wallet-validation.yml \
  --path openspec/specs/openxwallet/ \
  --path openspec/specs/openxwallet-agent-profile/ \
  --path openspec/changes/archive/2026-08-08-add-openxwallet/ \
  --path specs/006-openxwallet-contracts/ \
  --path specs/010-wallet-validator-ci/ \
  --path specs/012-wallet-issuer-anchor/ \
  --force
```

## What the contract forbids

| Forbidden | Why |
| --- | --- |
| `--path-glob` / `--path-regex` | a glob's surface is not reviewable; the twelve sets are ratified verbatim |
| `--path-rename` | a rename of an `examples/` prefix re-adjudicates 36 intended-invalid negatives as LIVE records inside a check that becomes REQUIRED |
| squashing / a fresh import | the openAvatar precedent requires full PATH HISTORY; a moved file whose history stops at the move is unbisectable |
| a thirteenth path | the surface is closed; anything else is a later change in openXwallet |
| running against the shared checkout | the carve reads a tree nobody else is editing — a fresh clone, always |

## The completeness contract

```sh
# in the openxFactory clone at CARVE_COMMIT
git ls-tree -r --name-only "$CARVE_COMMIT" -- <the twelve paths> | sort > expected.txt
# in the carved repository
git ls-files | sort > actual.txt
diff expected.txt actual.txt        # MUST be empty
wc -l < expected.txt                # MUST be 100
```

## The count contract

| Assertion | Expected |
| --- | --- |
| files under `specs/006-openxwallet-contracts/` (incl. `evidence/`) | 7 |
| files under `contracts/openxwallet/examples/negative/` | 32 |
| files under `contracts/openxwallet-agent-profile/examples/negative/` | 4 |
| both negative trees together (the ratified "36") | 36 |
| `contracts/openxwallet/examples/` exists at that exact relative path | yes |
| `contracts/openxwallet-agent-profile/examples/` exists at that exact relative path | yes |

## What the carve does NOT bring

`contracts/schemas/hermes-job-envelope.schema.yaml` is **not** a carved path. It
arrives in the SCAFFOLD commit, at the identical relative path, so the validator
needs no edit and the empty-diff proof is about carved bytes only.
