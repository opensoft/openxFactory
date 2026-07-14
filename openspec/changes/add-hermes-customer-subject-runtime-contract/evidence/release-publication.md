# Release Publication — contract-v1.9

Status: record

**Change**: add-hermes-customer-subject-runtime-contract
**Feature**: 005-customer-subject-runtime · Task T081
**Bundle**: contract-v1.9 · **Date**: 2026-07-14

## Published identity

- **Repository**: `opensoft/openxFactory` (`git@github.com:opensoft/openxFactory.git`)
- **Published commit** (on `origin/main`): `64cc000e9a2c24922050df73ec37958dbf5cfca4`
- **Annotated tag**: `contract-v1.9` (annotated tag object; peels to the
  published commit)
- **Realized inventory**: `contracts/releases/contract-v1.9.digests.yaml`
  (179 members; raw Git blob SHA-256; bytewise-utf8 path order; self-excluded;
  no commit field)

## Promotion record

1. The candidate was rebased onto `origin/main` twice as main advanced under
   concurrent changes: first onto `8d37f6c`, then onto `e4b3c7e` (two
   ideation-dashboard schema commits landed mid-realization). Both rebases were
   clean — the feature branch and the advanced main are disjoint in the files
   they touch. Every gate was re-run on the final rebased commit `64cc000`.
2. Version was re-confirmed at promotion time: `contract-v1.7` and
   `contract-v1.8` were already published by other features; `contract-v1.9`
   was absent and is the next available additive version.
3. The exact reviewed commit `64cc000` was pushed to published `origin/main`
   as a fast-forward (no merge commit; the reviewed commit is the published
   commit — the branch-protection PR rule was bypassed under the maintainer's
   permission, consistent with the direct-commit history of `contract-v1.7` and
   `contract-v1.8`).
4. `validate-contract-release.py verify-promotion --commit 64cc000 --remote
   origin --tag contract-v1.9`: **pass** (remote tag absent, version next,
   candidate reachable from remote main, no reviewed-blob drift).
5. The annotated tag `contract-v1.9` was created on `64cc000` and pushed.
6. `validate-contract-release.py verify-tag --remote origin --tag
   contract-v1.9`: **pass** (annotated tag object; peels to the published
   commit; reachable from published `origin/main`; manifest/changelog/tag/
   version/inventory agree).
7. `validate-hermes-runtime-contracts.py --require-realization
   --domain-repo-root <offline mirrors>`: **pass** (realized release metadata,
   published remote commit/tag evidence, and reproduced DomainxFactory digests
   all validate).

## Scope of this publication

Provider publication only. Gate G0 / OpenSpec task 5 / T009 remain **OPEN**.
Closure additionally requires the exact downstream
`opensoft/xFactory-Hermes-Install` consumer feature to land and its
compatibility manifest / checker / runtime-binding / evidence digests to be
independently reproduced against this bundle (T082–T084). No consumer receipt
is claimed here; no downstream repository was edited.
