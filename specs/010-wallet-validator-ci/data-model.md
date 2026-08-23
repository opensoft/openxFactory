# Data Model — 010-wallet-validator-ci

No persisted entities are created or modified by this feature. This file records the
logical entities the check observes and produces, for shared vocabulary between spec,
plan, tasks, and review.

## Entities

### WalletArtifact (observed, not modified)

A YAML document in the repository whose `kind` is one of the openxwallet family kinds.
Two populations exist:

- **Live artifacts**: anywhere in the tree; validated by validator layer 2 sweeps;
  a malformed one is an ERROR (check fails).
- **Packaged examples**: under `contracts/openxwallet/examples/`; conforming
  `*.example.yaml` specimens are asserted valid, and the `negative/` subcorpus is
  asserted to fail — both by validator layer 1.

Fields of interest (read-only): `kind`, grant scope fields (`audience`,
`scope.acts`, `scope.objects`, `scope.authority_tier`, `expires_at`, `issued_by`,
`parent_grant_ref`) — governed by existing schemas this feature does not touch.

### NegativeSpecimen (observed, load-bearing)

A file under `contracts/openxwallet/examples/negative/` carrying self-describing
expectation headers:

- `# expected_failure: <code>` (required)
- `# expected_failure_detail: <substring>` (optional pin)
- `# requirement: <REQ-ID>` (required attribution)

29 such specimens exist. Layer 1 fails if any of them passes or fails with the wrong
code — this is the FR-004 self-test and it is validator-native.

### CheckResult (produced)

The GitHub check run named **`wallet-validation`**:

| State | Meaning | Trigger |
|---|---|---|
| green | tree conforms; negatives proven failing | exit 0 from validator |
| red + attribution | malformed live artifact | validator errors name file + rule (FR-003) |
| red malfunction | crash / missing dependency / 10-min budget exhausted | fail-closed (FR-006) |

Relationships: one CheckResult per PR; derived exclusively from one validator
invocation over the checkout root; warnings in output never change state (FR-010).

## State transitions

None. The check is stateless per run; branch-protection consumption of the check is an
operator configuration act outside this feature's diff.
