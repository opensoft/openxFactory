# Phase 1 data model: occurrences, classes and gates

**Feature**: `030-realize-codexfactory-repository-identity` | **Date**: 2026-09-08

This feature's "data" is the corpus itself. The entities below are the ones a
reviewer must be able to name in order to check the disposition against the
tree rather than against a list.

---

## Occurrence

One literal, case-insensitive match of `opensoft/codexfactory`.

| field | source | notes |
| --- | --- | --- |
| `path` | `git grep -in` | repo-relative, never host-absolute (constitution IV) |
| `line` | `git grep -in` | volatile; the packet's own line numbers have already shifted |
| `path_class` | derived from `path` by the design § 2 pathspec table | exactly one of RENAME, FROZEN, NOT SWEPT |
| `gating_class` | derived by the plan's safe-now test | `safe-now` or `gated:<runbook step>`; **only defined when `path_class` is RENAME** |
| `verdict` | the records-and-assertions test, applied per line where a file is mixed | RENAME or FROZEN; a mixed file (`README.md`) carries a verdict per line, not per file |

**Invariant**: `path_class` is a function of the path alone. `gating_class` is a
function of what resolves the string at run time. The two axes are independent,
which is why the packet's single axis was not enough once the realization was
authorized ahead of the transfer.

## Path class

One row of the design § 2 table. Measured at `e8021fed`:

| class | pathspec | hits | files | disposition |
| --- | --- | ---: | ---: | --- |
| contracts-live | `contracts/` `:!contracts/signed-execution-chain/` | 30 | 23 | RENAME |
| tests | `tests/` | 23 | 8 | RENAME |
| workflows | `.github/` | 16 | 4 | RENAME |
| governance | `governance/` | 6 | 3 | RENAME (human-only) |
| scripts | `scripts/` | 5 | 3 | RENAME |
| docs-live | `docs/` `:!docs/decisions/` | 35 | 18 | RENAME |
| readme | `README.md` | 9 | 1 | RENAME, 3 lines FROZEN |
| **RENAME subtotal** | | **124** | **60** | |
| signed-chain | `contracts/signed-execution-chain/` | 44 | 34 | FROZEN — cryptographic |
| archive | `openspec/changes/archive/` | 15 | 10 | FROZEN — immutable |
| specs | `specs/` | 18 | 9 | FROZEN — dated verification |
| decisions | `docs/decisions/` | 1 | 1 | FROZEN — dated decision |
| **FROZEN subtotal** | | **78** | **54** | |
| active-packets | `openspec/changes/` `:!openspec/changes/archive/` | 106 | 36 | NOT SWEPT — owning lanes |
| ideation | `ideation/` | 19 | 13 | NOT SWEPT — pre-governance |
| **NOT SWEPT subtotal** | | **125** | **49** | |
| **TOTAL** | `.` | **327** | **163** | |

**Reconciliation to the 2026-09-07 baseline (281 / 150 = 123/60 + 78/54 + 80/36),
drift attributed cause by cause:**

| class | delta | attributed cause |
| --- | ---: | --- |
| RENAME | +1 hit, +0 files | `README.md` 8 → 9: this packet's OpenSpec Records entry, landed by PR #763 |
| FROZEN | 0, 0 | none — the frozen set is byte-identical, which is itself the first freeze evidence |
| active-packets | +32 hits, +4 files | **+29 / +4 is this packet's own directory**, now on `main` (`.openspec.yaml` 1, `design.md` 16, `proposal.md` 7, `tasks.md` 5); other lanes' = 77 / 32, +3 hits at unchanged file count |
| ideation | +13 hits, +9 files | the OQ-3 ideation split (openxFactory #771/#772/#785/#786) rewrote and re-pointed `ideation/`; still pre-governance, still not swept |
| **TOTAL** | **+46 / +13** | fully attributed; **no occurrence fails to classify under the published rule**, so packet task 2.2 records no finding |

**Self-reference note**: `evidence/codexfactory-identity-sweep-2026-09-08.md`
lands inside the `active-packets` class and adds its own occurrences to it. The
sweep is therefore taken and recorded **before** the evidence file is written,
and the file states its own contribution so a later re-run reads a known delta
rather than an unexplained one.

## Gating class

The second axis, defined only over the 124 RENAME occurrences.

| gate | hits | files | slice | pull request |
| --- | ---: | ---: | --- | --- |
| `safe-now` | 8 | 8 | A | normal |
| `gated:1.2` — pin, workflows, operator tools | 41 | 15 | B1 | draft |
| `gated:1.2` — origin identity (**human-only**) | 35 | 14 | B2 | draft |
| `gated:1.2` — the eight inventoried members | 12 | 9 | B3 | draft |
| `gated:1.2` — remaining prose | 28 | 14 | B4 | draft (25 respelled, 3 frozen) |
| `gated:1.2` — the mapping row | 0 | 1 | B5 | draft, **BLOCKED** |
| **total** | **124** | **60** | | |

Runbook step **1.2** is *"OPERATOR. Confirm the destination and the visibility:
`gh api repos/codeXfactory/codexFactory --jq '{full_name,private,visibility}'`
MUST read `codeXfactory/codexFactory`, `private: true`."* It is named as the gate
because it is the first step at which the new address is proved to exist.
Measured at this head: that call returns **HTTP 404**, and
`gh api repos/opensoft/codexFactory` returns
`{"full_name":"opensoft/codexFactory","private":true,"visibility":"private"}`.

## Mapping row

One entry of `transfers:` in `contracts/policies/repository-identity.yaml` — a
file this feature does **not** create. Fields, with the packet task that fixes
each:

| field | value | task |
| --- | --- | --- |
| `former` | `opensoft/codexFactory` | 1.1 |
| `current` | `codeXfactory/codexFactory` | 1.1, and OQ-6 fixes the spelling |
| `transferred_on` | filled from runbook step 1.2 | 1.1, R-6 |
| `redirect` | note: the provider redirect lapses if `opensoft` reuses the name, which it may — `opensoft` remains active and holds the aggregation repository | 1.1 |
| `owner_case` | note: this estate compares the owner segment CASE-SENSITIVELY though the provider does not | 1.2 |
| `derived_container_namespace` | `ghcr.io/codexfactory/codexfactory` — lowercased by GHCR; the same identity under a different spelling, not a second identity | 1.2, OQ-6 |
| `redirect_does_not_cover` | reusable-workflow `uses:` paths, container package namespaces, federated-credential subject strings | 1.3 |

**No second registration is owed** (task 1.4): the `contracts/manifest.yaml`
entry and its `consumption_rule` are created by the exemplar's task 1.3, and
adding a row does not add an entry — but the manifest's per-file `sha256` for
this policy **moves with the row and is recomputed, never hand-edited**.

## Origin identity record set

Read together by `scripts/validate-factory-identity.py`, consumed by
`scripts/validate-clearing-dispatch.py`.

| artifact | field that moves | field that MUST NOT move |
| --- | --- | --- |
| `governance/factory-identity/register.yaml` | `holder_ref` (line 146); the header sentence about concurrent active rows (line 113) | the row's identity — **one row respelled, never a second row** |
| `wallets/wal-origin-codexfactory-0001.yaml` | `holder_id` (line 50) | `key_id`, the multibase public half, the fingerprint, `holder_class` |
| `grants/grant-origin-codexfactory-0001.yaml` | `audience.holder_ref`, the single-element `scope.objects`, the "THE SCOPE IS ONE REPOSITORY" paragraph | the cardinality of `objects` (**never widened to carry both identities**), `expires_at` (`issued_at` + 90 days — a separate governed question) |
| `attestations/custody-attest-wal-origin-codexfactory-0001.yaml` | **nothing** — it carries no owner segment (R-10) | everything |
| filenames throughout | **nothing** — `wal-origin-codexfactory-0001`, `grant-origin-codexfactory-0001`, `attest-custody-…` are BARE names (task 6.4) | all of them |

**State transition**: `active(opensoft/codexFactory)` →
`active(codeXfactory/codexFactory)`. There is no intermediate state in which
both are active, by construction: the register's reader refuses a concurrent
active row for the same repository, which is why D-1 rules the re-issuance a
respell rather than a new wallet, grant and row.

## Inventoried member

A file present in `contracts/releases/contract-v3.4.digests.yaml` (283 entries).
Eight of the 60 renamed files are members, re-verified at this head; none of the
other 52 is. None of the eight is in `scripts/doc_health/release_inventory.py`'s
three-path `EDITORIAL` set, so each moved blob is an `ERROR`-severity
`release-inventory-drift` finding and a red `verify-commit` from the moment
slice B3 lands until the cut re-baselines the inventory.

| member | slice |
| --- | --- |
| `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` | B3 |
| `contracts/hermes-runtime/fixtures/regression/digest-mismatch.yaml` | B3 |
| `contracts/hermes-runtime/fixtures/regression/duplicate-repository.yaml` | B3 |
| `contracts/hermes-runtime/fixtures/regression/missing-exclusion-reason.yaml` | B3 |
| `contracts/hermes-runtime/README.md` | B3 |
| `docs/contract-versioning-policy.md` | B3 |
| `docs/terminology-and-repo-topology.md` | B3 |
| `docs/xfactory-domain-factory-model.md` | B3 |
