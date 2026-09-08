# Phase 1 data model — P2 carve and scaffold

**Feature**: `017-openxwallet-carve` · **Date**: 2026-08-26

The entities here are FILES AND FIELDS, not database records. Each is given its
exact shape, because the acceptance criteria are field-level.

## E1. `CARVE_COMMIT`

| Property | Value |
| --- | --- |
| Value | `30565e48ffe3d8a9773e10af33425701845e10f6` |
| Form | exactly 40 lowercase hex characters |
| Source | `opensoft/openxFactory` `origin/main`, resolved once from a fresh clone |
| Lifetime | FROZEN for the whole feature |

**Recorded in three places** (D7), one of them machine-read:

1. `contracts/manifest.yaml` → `carved_from: {repository, commit}` — the
   machine-read record.
2. `docs/openxwallet-cutover-runbook.md` — the procedure.
3. openxFactory's `contracts/openxwallet-pin.yaml` → `carve_commit:` — **at P3,
   not here.**

**Forbidden**: a bare `CARVE_COMMIT` file. An unschema'd file nothing reads is
the failure class of a governance floor whose source of truth is loose markdown.

## E2. The twelve path sets (the carve surface)

Ordered as ratified. `--path` takes each verbatim; no globs, no `--path-rename`.

| # | Path | Files at carve commit |
| --- | --- | --- |
| 1 | `contracts/openxwallet/` | 55 |
| 2 | `contracts/openxwallet-agent-profile/` | 8 |
| 3 | `scripts/validate-openxwallet.py` | 1 |
| 4 | `scripts/wallet-yaml-syntax-gate.py` | 1 |
| 5 | `tests/wallet_yaml_syntax_gate/` | 1 |
| 6 | `.github/workflows/wallet-validation.yml` | 1 |
| 7 | `openspec/specs/openxwallet/` | 1 |
| 8 | `openspec/specs/openxwallet-agent-profile/` | 1 |
| 9 | `openspec/changes/archive/2026-08-08-add-openxwallet/` | 6 |
| 10 | `specs/006-openxwallet-contracts/` | 7 |
| 11 | `specs/010-wallet-validator-ci/` | 9 |
| 12 | `specs/012-wallet-issuer-anchor/` | 9 |
| | **Total** | **100** |

**Invariants**

- `INV-1` (completeness): the sorted listing at the carve commit filtered to
  these twelve prefixes EQUALS the carved repository's sorted tracked listing.
- `INV-2` (counts): `specs/006-openxwallet-contracts/` = 7 (its `evidence/`
  included); `contracts/openxwallet/examples/negative/` = 32;
  `contracts/openxwallet-agent-profile/examples/negative/` = 4; the two together
  = **36** — the ratified figure, carried in the form the shorthand collapsed.
- `INV-3` (examples-prefix preservation): both `contracts/openxwallet*/examples/`
  directories exist at IDENTICAL relative paths, because the corpus exclusion
  keys on `"examples" in path.parts` AND a part in
  `("openxwallet", "openxwallet-agent-profile")`.

## E3. `contracts/manifest.yaml` — the owned rows (8)

Header:

```yaml
schema_version: 1
kind: contract_manifest
contract_bundle_version: wallet-v1.0
carved_from:
  repository: opensoft/openxFactory
  commit: 30565e48ffe3d8a9773e10af33425701845e10f6
```

Each owned row carries the publisher's **nine** fields, unchanged from the carve
commit except `source_path`:

| Field | Rule |
| --- | --- |
| `id` | VERBATIM from openxFactory |
| `path` | VERBATIM — R2 forbids path renames in v1 |
| `source_path` | REWRITTEN `openxFactory/…` → `openXwallet/…` (it names the repository a consumer vendors from, and that repository changed) |
| `type` | VERBATIM (`schema` or `registry`) |
| `schema_version` | VERBATIM (`1`) |
| `sha256` | VERBATIM — **this is the floor** |
| `compatibility` | VERBATIM (`canonical_openxfactory_contract`) — the token names the contract's CLASS, not its host repository |
| `adapter_owner` | VERBATIM (`openxFactory`) — see note |
| `consumption_rule` | VERBATIM prose |

The eight rows:

| # | `id` | `path` | `sha256` |
| --- | --- | --- | --- |
| 1 | `openxwallet-record` | `contracts/openxwallet/openxwallet-record.schema.yaml` | `2012ef432616e73ddaead17c5e79aefacef712c2049ff649c15d7230b1d4eb08` |
| 2 | `openxwallet-custody-registry-schema` | `contracts/openxwallet/openxwallet-custody-registry.schema.yaml` | `df72638497a7f90c2a4dff47c429cb794bc4b6e270ce2dd2b17116478ae3b51a` |
| 3 | `openxwallet-custody-registry` | `contracts/openxwallet/openxwallet-custody.registry.yaml` | `94d631d6ee76dab015628a1856afd82582b98d6a3733622c9afe8b13b5278539` |
| 4 | `openxwallet-grant` | `contracts/openxwallet/openxwallet-grant.schema.yaml` | `fde433c5821e2e6f62926a72c58a67a784961d2e9e27e9f2b3520fcc8e738e88` |
| 5 | `openxwallet-grant-exercise` | `contracts/openxwallet/openxwallet-grant-exercise.schema.yaml` | `f16ad31246186cec36e142ae39bd831d98fbc5c0afd48685057bc39e113c8858` |
| 6 | `openxwallet-distinct-holder-constraint` | `contracts/openxwallet/openxwallet-distinct-holder-constraint.schema.yaml` | `c2a6d2fd23fb3743fdaf0e165dabc4cb1dff24e52a8262a38c86ed1482374b25` |
| 7 | `openxwallet-subject-attestation` | `contracts/openxwallet/openxwallet-subject-attestation.schema.yaml` | `d29eca519462aff7871de3786f19c820e9fc3b95115ce30e57d1f1cc2bc0c0b2` |
| 8 | `openxwallet-agent-composition` | `contracts/openxwallet-agent-profile/openxwallet-agent-composition.schema.yaml` | `aed3978e8ae952f3ff5b3de1f672bba5da350d5aaeb442feafaa870b4de4be91` |

**Note on `adapter_owner: openxFactory` for owned rows.** The field records who
owns the ADAPTER obligation for this contract class in the family's history; R2
freezes machine keys in v1, so rewriting it would be a rename inside a move whose
safety rests on an empty diff. It is revisited by a later change in openXwallet,
never here.

**The content-addressed-by-commit note** is carried alongside: the packaged
corpus (`contracts/openxwallet*/examples/`), the strict validator, the syntax
gate and both family READMEs are content-addressed by commit with no per-file
digest — the possibles-register and ideation-routing precedent.

## E4. `contracts/manifest.yaml` — the CONSUMED row (1)

The publisher's nine fields PLUS three declared fields (N8):

```yaml
- id: hermes-job-envelope
  path: contracts/schemas/hermes-job-envelope.schema.yaml
  source_path: openxFactory/contracts/schemas/hermes-job-envelope.schema.yaml
  type: schema
  schema_version: 1
  sha256: 8ce2c89903a2f5a68ce3d73a7b8eb4f47cdef913da038b9a68e22735ee96cb7c
  compatibility: canonical_openxfactory_contract
  adapter_owner: openxFactory
  consumption_rule: >-
    …read-only, at the pinned digest; rule (g) reads the approval-scope
    vocabulary out of it…
  member_class: consumed
  release_surface: false
  pinned_openxfactory_bundle: contract-v1.44
```

**Why these three fields and not a path heuristic.** `release_surface: false` and
`member_class: consumed` are how the wallet's release tooling excludes this member
from `wallet-vN.M.digests.yaml`: exclusion by DECLARED FIELD. A
`contracts/schemas/` path heuristic breaks the day openXwallet publishes a schema
of its OWN there (task 3.13).

**Why the row exists at all.** `shared-contract-ownership:142` requires all
publisher markers together. Recording this file as OWNED would falsely claim an
openxFactory contract; omitting it leaves the marker test unmet. The consumed row
is the third option, and it is the ratified one.

**The digest is computed, not copied** — openxFactory's own row carries no
`sha256` (see `research.md` R5). Recorded on the row.

## E5. `contract_pin.yaml`

```yaml
schema_version: 1
kind: pinned_contract_manifest
source_repository: opensoft/openxFactory
revision_kind: commit
commit: "30565e48ffe3d8a9773e10af33425701845e10f6"
pinned_bundle: contract-v1.44
verify_pin: scripts/verify-contract-pin.py
files:
  - path: contracts/schemas/hermes-job-envelope.schema.yaml
    sha256: "8ce2c89903a2f5a68ce3d73a7b8eb4f47cdef913da038b9a68e22735ee96cb7c"
pinned_by_commit_only: []
```

**Field rules**

- `revision_kind: commit` and an exact 40-hex `commit` — a movable branch or tag
  is not a compatibility pin (Constitution VI).
- `verify_pin` NAMES the verifier, so the pin is not an obligation stated in
  prose (N3: both directions must be running code).
- `pinned_by_commit_only: []` is present and EMPTY: exactly one file is pinned and
  it carries a per-file digest, so nothing is commit-only. The key exists so the
  distinction is declared rather than absent.
- **Fail-closed pre-sync** (openAvatar's doctrine): an empty/absent `commit`
  rejects (not content-addressed), and a recomputed digest can never equal an
  empty recorded digest → drift → fail before any test.

## E6. `scripts/verify-contract-pin.py`

| Property | Value |
| --- | --- |
| Invocation | `python3 scripts/verify-contract-pin.py` (no arguments) |
| Reads | `contract_pin.yaml` and the files it names — **nothing else** |
| Network | never |
| Exit 0 | every named file present AND recomputed sha256 == recorded |
| Exit 1 | drift, a missing file, a missing/empty recorded digest, a missing/empty `commit`, or an unparseable pin |
| Exit 2 | usage/environment failure (pin file absent, PyYAML absent) |

**Refusal contract (N1).** Every non-zero exit prints, on its own lines, the
finding AND a remediation trailer naming both:

```
  remediation: git submodule update --init openXwallet
  remediation: see docs/pin-resync-runbook.md
```

The exit is in the message, not in tribal memory.

## E7. The two workflows

| | `wallet-validation.yml` | `pytest-suite.yml` |
| --- | --- | --- |
| Job id (the ruleset token) | `wallet-validation` | `pytest-suite` |
| Job display name | **none** — a display name silently de-advises the gate | none |
| Trigger | `pull_request` → `main` | `pull_request` → `main` |
| Permissions | `contents: read` | `contents: read` |
| Steps | checkout → setup-python 3.12 → pip → **`verify-contract-pin.py`** → syntax gate → validator | checkout → setup-python 3.12 → pip → `python3 -m pytest tests/ -q` |
| Provenance | CARVED, verify step prepended (the only post-carve edit to a carved file) | SCAFFOLD |

**Step ORDER is the requirement**, not a preference: the validator checks only
`ENVELOPE_SCHEMA_PATH.is_file()` — presence, not identity — while rule (g) reads
the approval-scope vocabulary out of that file. An unverified swap would silently
redefine the vocabulary the gate enforces.

## E8. The promoted specs — the two-line carve-out

| Line | Before | After |
| --- | --- | --- |
| `:4` | `TBD - created by archiving change add-openxwallet. Update Purpose after archive.` | a real Purpose sentence for that family |
| `:8` (and every requirement body) | `openxFactory SHALL …` | `openXwallet SHALL …` |

**Everything else in both files is byte-identical.** The diff is asserted line by
line, which is the declared scope of the one carve-out rather than a described one.

## E9. The byte-identity proof record

`docs/byte-identity-wallet-v1.0.md` in openXwallet, mirrored into
`specs/017-openxwallet-carve/evidence/byte-identity.md` here.

| Part | Assertion | Evidence form |
| --- | --- | --- |
| Completeness | `INV-1` | diff of two sorted listings, empty; total 100 |
| Counts | `INV-2` | 7 / 32 / 4 / 36 |
| Prefixes | `INV-3` | both `examples/` dirs at identical relative paths |
| One | 8 recomputed digests == 8 recorded | eight-row table |
| Two (a) | tree diff EMPTY over the floor | per-path `diff -r` result |
| Two (b) | each promoted spec differs in exactly 2 lines | the literal diff |
| Declared edit | `wallet-validation.yml` gained the verify step | the one-hunk diff, named |

**Reproducibility rule**: every command in the record uses repo-relative paths
and a `$` placeholder for checkout locations. No host-absolute path is committed
(Constitution IV).
