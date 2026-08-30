# Quickstart: Resolved Council Seats

Status: draft

Run commands from the `026-add-resolved-council-seats` feature worktree root in
the repository's declared isolated environment. Do not copy container-absolute
or host-absolute paths into committed artifacts.

## 1. Confirm The Feature Checkout

```bash
GIT_MASTER=1 git status -sb
GIT_MASTER=1 git branch --show-current
```

Expected branch: `026-add-resolved-council-seats`.

## 2. Prepare The Isolated Contract Environment

Use the repository's existing contract dependency lock; the plan introduces no
new runtime dependency:

```bash
uv venv .venv
uv pip sync --python .venv/bin/python requirements/hermes-runtime-contracts.lock
```

The `.venv` is local and ignored. The neutral validator performs no live network
lookup; immutable rules and candidate-head observations come from fixtures.

## 3. Run Governance And Provider Gates

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
.venv/bin/python scripts/validate-council-convening.py --strict
.venv/bin/python -m pytest tests/council_convening -q
```

Expected:

- all OpenSpec changes/specifications validate strictly;
- the schema validates against Draft 2020-12;
- every fixture is indexed exactly once and every index target exists;
- both positive rosters reproduce exactly;
- every negative case refuses for its declared primary finding;
- the complete indexed corpus validates in under 30 seconds;
- no artifact contains credentials, private key material, or absolute paths.

## 4. Inspect Individual Cases

```bash
.venv/bin/python scripts/validate-council-convening.py \
  --case standing-roster \
  --json

.venv/bin/python scripts/validate-council-convening.py \
  --case candidate-head-stale \
  --json
```

The positive result reports `accept` with no finding codes. The negative harness
run exits successfully only when the invalid input reports
`candidate_head_stale` as its declared primary finding.

## 5. Verify Traceability

Review `specs/026-add-resolved-council-seats/contracts/acceptance-map.yaml` and
the realized fixture index together. Expected parity is:

- 3 governed requirements;
- 11 governed scenarios;
- 14 feature functional requirements;
- 7 measurable outcomes;
- no missing, duplicate, dangling, or skipped required evidence.

## 6. Build The Release Candidate

Do not reserve a bundle version during planning. Immediately before candidate
freeze, refresh the remote release surfaces and allocate the next available
additive version under `docs/contract-versioning-policy.md`:

```bash
GIT_MASTER=1 git fetch origin --tags

bundle_tag=contract-vX.Y
.venv/bin/python scripts/validate-contract-release.py build \
  --tag "$bundle_tag" \
  --output "contracts/releases/${bundle_tag}.digests.yaml"

OPENSPEC_TELEMETRY=0 openspec validate --all --strict
.venv/bin/python scripts/validate-council-convening.py --strict
.venv/bin/python -m pytest tests/council_convening -q
```

Release validation must prove manifest/changelog/tag/inventory agreement and raw
Git blob digest parity for every semantic member. Commit, promotion, and tagging
require explicit authorization and are not part of this quickstart's local gate.

## 7. Run Downstream Successor Gates

After the provider bundle is published, each downstream repository pins the
exact bundle and runs the shared corpus independently.

Hermes evidence must prove:

- independent immutable-rule evaluation and stale-head refusal;
- snapshot freeze before exactly one job per seat;
- unlisted/missing return behavior and rich outcome unanimity;
- PostgreSQL persistence, verdict-less failure, and open-run recovery regression.

codexFactory evidence must prove:

- exact GitHub facts and immutable governed-rule provenance;
- standing-only and conditional-seat parity with the shared corpus;
- one job-local ephemeral Ed25519 key per seat, no shared/root private key;
- governed reusable-workflow OIDC binding.

These gates run in their owning feature worktrees. Do not edit either downstream
repository from the openxFactory feature.

## 8. Rehearse The Hard Cutover

Before live activation, record the pinned provider bundle, exact downstream
commits, activation order, paired rollback versions, and evidence paths. Activate
producer emission and consumer requirement together. A failed ordering parks new
convenings; it does not enable obsolete payload reconstruction.

Do not mark live GitHub OIDC, deployment, image, merged-commit, bundle release,
or rollback evidence complete until an authorized operator performs and verifies
the corresponding act.
