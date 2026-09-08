# Quickstart: Intent Compliance Contract

## Validate the family during development

```bash
python3 scripts/validate-intent-compliance.py
python3 -m pytest tests/intent-compliance -q
OPENSPEC_TELEMETRY=0 openspec validate add-standing-policy-compliance-contract --strict
```

Expected result: every positive record and static registry-head probe passes; every negative
fixture fails for its declared reason; command exit status is zero.

## Validate a consumer repository

```bash
python3 scripts/validate-intent-compliance.py --trusted-repository ../trusted-checkout --trusted-repository-id OWNER/REPO --trusted-commit FULL_40_HEX_COMMIT ../consumer-repository
python3 scripts/validate-intent-compliance.py --strict --trusted-repository ../trusted-checkout --trusted-repository-id OWNER/REPO --trusted-commit FULL_40_HEX_COMMIT ../consumer-repository
```

## Prepare the additive release

After refreshing `origin/main` and remote tags, allocate the next free additive
bundle. This realization allocated `contract-v2.3` after verifying that release
name was still free:

```bash
python3 scripts/validate-manifest-digests.py
python3 scripts/validate-contract-release.py build \
  --tag contract-v2.3 \
  --output contracts/releases/contract-v2.3.digests.yaml
python3 scripts/validate-contract-release.py verify-commit --commit "$(git rev-parse HEAD)"
```

Generate the v2.3 inventory only after every release-member byte and PostgreSQL
evidence file has stabilized. Do not create it during metadata reconciliation.

Run the repository-wide validator suite and OpenSpec strict validation before
publication. Verify promotion and the annotated remote tag only against the
exact merged commit; record those outputs in realization evidence before
archive.
