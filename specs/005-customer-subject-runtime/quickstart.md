# Quickstart: Neutral Hermes Customer-Subject Runtime Contracts

Status: draft

Run every command from the feature worktree root inside the repository's `py-bench`. Do not run build/test commands through host Python, and do not copy container-absolute paths into committed files.

## 1. Confirm The Feature Checkout

```bash
cd "$(git rev-parse --show-toplevel)"
git status -sb
git branch --show-current
```

Expected branch: `005-customer-subject-runtime`.

## 2. Prepare The Isolated Validation Environment

```bash
uv venv .venv
uv pip sync --python .venv/bin/python requirements/hermes-runtime-contracts.lock
```

The `.venv` is local and ignored. Do not mutate the shared bench environment.

Prepare exact-object mirrors/checkouts for the five repositories named in
`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`. Set the
root outside the repository; canonical `owner/repo` names resolve only to
`<root>/<owner>/<repo>` or `<root>/<owner>/<repo>.git`:

```bash
: "${DOMAIN_REPO_ROOT:?set DOMAIN_REPO_ROOT to the prepared canonical mirror root}"
```

## 3. Run Governance And Static Compatibility Gates

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
.venv/bin/python scripts/validate-hermes-runtime-contracts.py \
  --strict \
  --domain-repo-root "$DOMAIN_REPO_ROOT"
.venv/bin/python -m pytest tests/hermes_runtime_contracts -m 'not postgres' -q
```

Expected:

- all OpenSpec changes/specs valid;
- every required family schema and fixture indexed;
- the two-Customer topology and domain-neutral examples pass;
- all declared negative cases fail for their expected stable finding codes;
- supported DomainxFactory stacks and unchanged v1 message fixtures remain valid.

## 4. Run PostgreSQL 15/16 Conformance

Refresh and review the committed image lock only before candidate freeze:

```bash
./scripts/run-hermes-runtime-postgres-tests.sh --update-image-lock
```

Normal/release runs use only the resulting `postgres@sha256:...` entries in `tests/hermes_runtime_contracts/postgres/images.lock.yaml`:

```bash
./scripts/run-hermes-runtime-postgres-tests.sh
```

The runner must:

- resolve and record the exact PostgreSQL 15/16 image digests;
- start isolated throwaway containers with no published ports;
- apply canonical v2 DDL directly;
- exercise roles/RLS/scope pooling, authority races, artifacts/approvals/traces, migration/reconciliation, quarantine, DDL drift, and crash/retry;
- clean every volume/container on success, failure, or interruption.
- generate its ephemeral password in memory without printing or persisting it;
- assert that no database port is published and no credential appears in evidence.

Docker or image unavailability is a failed required gate, not a skip.

## 5. Inspect One Fixture Or Machine Result

```bash
.venv/bin/python scripts/validate-hermes-runtime-contracts.py \
  --case topology-operational-two-customers \
  --json
```

Expected result contains the case ID, `pass`, no finding codes, and its evidence ID.

For a negative fixture:

```bash
.venv/bin/python scripts/validate-hermes-runtime-contracts.py \
  --case topology-operational-zero-customers \
  --json
```

The harness exits successfully only when the case produces its declared primary finding code. Running the invalid document directly without the fixture expectation exits with findings.

## 6. Build A Release Candidate Inventory

Do not choose a version until final rebase and the remote release surfaces have been refreshed.

```bash
git fetch origin --tags
git rebase origin/main

bundle_tag=contract-vX.Y
.venv/bin/python scripts/validate-contract-release.py build \
  --tag "$bundle_tag" \
  --output "contracts/releases/${bundle_tag}.digests.yaml"

OPENSPEC_TELEMETRY=0 openspec validate --all --strict
.venv/bin/python scripts/validate-hermes-runtime-contracts.py \
  --strict \
  --require-candidate \
  --domain-repo-root "$DOMAIN_REPO_ROOT"
./scripts/run-hermes-runtime-postgres-tests.sh
```

Replace `X.Y` only with the next available additive version verified at that time.

## 7. Verify The Exact Candidate Commit

After explicitly staging the reviewed release surfaces and committing candidate C:

```bash
candidate_commit="$(git rev-parse HEAD)"
.venv/bin/python scripts/validate-contract-release.py verify-commit \
  --commit "$candidate_commit"
```

Run the complete gate suite and independent expert review on this exact commit. If promotion creates a different main-line commit, rerun every gate/review on that commit before tagging.

Immediately before tag creation:

```bash
.venv/bin/python scripts/validate-contract-release.py verify-promotion \
  --commit "$candidate_commit" \
  --remote origin \
  --tag "$bundle_tag"
```

This fails if the tag now exists, the version is no longer next, the candidate is not on remote main, or any reviewed release-surface blob drifted.

## 8. Verify Published Main-Line And Tag Evidence

After the exact reviewed commit is reachable from published `origin/main` and the annotated tag is pushed:

```bash
git fetch origin --tags
.venv/bin/python scripts/validate-contract-release.py verify-tag \
  --remote origin \
  --tag "$bundle_tag"
.venv/bin/python scripts/validate-hermes-runtime-contracts.py \
  --strict \
  --require-realization \
  --domain-repo-root "$DOMAIN_REPO_ROOT"
```

Expected verification proves:

- annotated tag object and peeled commit;
- commit reachability from `origin/main`;
- manifest, changelog, tag, version, and inventory agreement;
- raw Git blob digest parity for every required semantic member;
- no host-absolute release metadata.

## 9. Downstream Gate G0 Handoff

Hand the published provider evidence to the existing Hermes Install feature. Do not edit that repository from this feature. Hermes writes `evidence/gates/g0/<bundle-tag>.yaml` under its own closure schema. After that exact revision lands, validate the openxFactory receipt:

```bash
: "${HERMES_INSTALL_REPO:?set HERMES_INSTALL_REPO to a checkout or bare mirror containing the landed commit}"
.venv/bin/python scripts/validate-hermes-runtime-contracts.py \
  --handoff-receipt \
  openspec/changes/add-hermes-customer-subject-runtime-contract/evidence/hermes-install-g0-handoff.yaml \
  --consumer-repo "opensoft/xFactory-Hermes-Install=$HERMES_INSTALL_REPO" \
  --strict
```

The receipt contains the exact landed Hermes commit and the digests of its compatibility manifest, checker, runtime binding, closure evidence, and positive/negative results. Validation independently reads the packet and every recorded downstream artifact as `commit:path` Git objects from that exact commit; missing or inaccessible objects exit 2.

Do not archive this OpenSpec change or declare G0/T009 complete until that external evidence has landed and been independently reproduced.
