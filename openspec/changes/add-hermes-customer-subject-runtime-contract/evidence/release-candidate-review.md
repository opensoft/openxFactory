# Release Candidate Review — contract-v1.9

Status: record

**Change**: add-hermes-customer-subject-runtime-contract
**Feature**: 005-customer-subject-runtime · Task T080
**Candidate commit C**: 64cc000e9a2c24922050df73ec37958dbf5cfca4
**Bundle**: contract-v1.9 · **Date**: 2026-07-14

## Candidate identity

Candidate C is the provider-side realization of the neutral Hermes
customer-subject runtime family, rebased cleanly onto `origin/main` at
`e4b3c7e` (13 feature commits replayed; zero conflicts; the branch and the
advanced main are disjoint in the files they touch). C is
`git rev-parse HEAD` in an isolated realization worktree; nothing is pushed at
review time and no `contract-v1.9` tag exists on the remote.

## Gates on the exact candidate C (all green)

- `openspec validate --all --strict`: 26 passed, 0 failed.
- `validate-hermes-runtime-contracts.py --strict`: 0 findings — 39 contracts,
  32 schemas, 110 fixtures, 17 requirements, 85 scenarios, 803 tests collected.
- `validate-hermes-runtime-contracts.py --require-candidate --domain-repo-root
  <offline mirrors>`: exit 0 (the realized inventory reproduces and the five
  supported DomainxFactory `stack.yaml` blobs resolve at their pinned commits).
- `validate-contract-release.py verify-commit --commit 64cc000`: pass (every
  inventory member reproduces from the committed tree; ignores the working
  tree).
- Non-PostgreSQL pytest: 485 passed, 0 failed.
- `git diff --check`: clean. `black --check` on the two candidate-changed
  Python files: clean.

## PostgreSQL evidence

Unchanged from the US4 checkpoint. The realization touched only release
metadata (`manifest.yaml`, `CHANGELOG.md`, `README.md`, the realized
`releases/contract-v1.9.digests.yaml`, one evidence-register node id, two
realized-state test modules, and the T079/T080 evidence docs). None intersects
the 78-member PostgreSQL evidence source inventory, so the both-majors matrix
is not re-run; source identity `sha256:b2ef44a9…` and matrix digest
`sha256:032f80fa…` are preserved.

## Independent review

The full US4 provider surface underwent a four-lens adversarial review with
per-finding verification before the checkpoint (dispositions in
`specs/005-customer-subject-runtime/us4-provider-handoff/us4-review-findings.md`):
3 findings confirmed, 2 P2 fail-opens fixed with regression tests, 1 P3
(latent) deferred. The realization adds only additive release metadata and the
realized digest inventory over that reviewed surface; it introduces no new
contract, schema, or semantic behavior. The realized-state test adjustments
were re-derived from the observed post-realization CLI behavior and re-verified
green.

## Disposition

Candidate C is APPROVED for promotion. The exact unchanged commit
`64cc000e9a2c24922050df73ec37958dbf5cfca4` is to land on published
`origin/main`; only then may the matching annotated `contract-v1.9` tag be
published. If promotion creates any different main-line commit, every gate and
this review are re-run on that commit before tagging.

Gate G0 remains OPEN after publication: closure additionally requires the exact
downstream `opensoft/xFactory-Hermes-Install` consumer pin and its
independently reproduced digests, owned by that repository's feature (T082+).
