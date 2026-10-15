# Agent Instructions

Use the shared OpenSpec/Speckit workflow from:

- `$HOME/.agents/AGENTS.md`
- `$HOME/.agents/protocols/openspec-speckit-workflow.md`
- `$HOME/.agents/protocols/project-agent-bootstrap.md`

Repository documents remain authoritative for openxFactory product facts,
contract ownership, validation, versioning, and release constraints.

## Governed invariants

Read by `/speckit-tasks` and `/speckit-analyze` (shared protocol, "Build Tiers"): a task whose `files:` touch any path below is never `[H]`. The protocol's own rule applies beside this list: any file in this repository that records a pin, a digest or a measured value is governed whether or not it is listed.

- `openspec/` — governed text in every repository; here the required `former-id-arrival-gate` also refuses a commit that moves a ratified change packet without declaring `former_ids:`, and the required `pytest-suite` checks every tracked `openspec/specs` path against the vendored review-lane floor.
- `.github/workflows/` — CI workflow definitions, governed in every repository; here they also carry the tokens of the required checks and the counts and test names those checks pin, and they are routed to a code owner.
- `.github/CODEOWNERS` — routes the gate surfaces to a code owner, and the branch ruleset requires code-owner review, so an edit moves who must approve a pin, gitlink, workflow or envelope change.
- `.github/merge-approval-envelope.yml` — the only grant of autonomous approval in this repository (its candidate class and path allowlist), read from the base branch by `merge-master-approval.yml`; its exact shape is asserted under `tests/review_lane_pin/`.
- `.gitmodules` — submodule URLs, governed in every repository and routed to a code owner.
- `installs/omnigent-install` — submodule gitlink, governed in every repository.
- `openXwallet` — submodule gitlink; it must equal `commit:` in `contracts/openxwallet-pin.yaml`, and the required `wallet-validation` and `signed-execution-chain-gate` run the reader it pins.
- `openXdox` — submodule gitlink; it must equal `commit:` in `contracts/openxdox-pin.yaml` and the aggregation's own `openXdox` gitlink, and the required `openxdox-consumer-gate` verifies it.
- `openDox` — submodule gitlink; it must equal `commit:` in `contracts/opendox-pin.yaml` (itself in lockstep with openXdox's own openDox pin) and the aggregation's own `openDox` gitlink, and the required `openxdox-consumer-gate` verifies it.
- `contracts/manifest.yaml` — declares `contract_bundle_version`, which names the release inventory that must describe the tree, and the per-file `sha256` rows the required `pytest-suite` recomputes; it moves only with a release cut, and a pull request touching it is judged by the required `release-tag-gate`.
- `contracts/releases/` — the release digest inventories, the SHA-256 of every release member at each cut, written by the cut and never by hand; a pull request touching them is judged by the required `release-tag-gate`.
- `contracts/*-pin.yaml` — the commit and digest pins of openDox, openXdox, openXwallet, openRepoShape, the OpenSpec CLI and the review-lane decision core, each verified by its gate or suite; the decision-core commit must equal the `ref:` in `pytest-suite.yml` and `merge-master-approval.yml`.
- `contracts/openspec-cli-pin.*.package-lock.json` — the pinned OpenSpec CLI's install tree, content-addressed by `lockfile_integrity:` in `contracts/openspec-cli-pin.yaml`.
- `contracts/review-lane-floor-snapshot.yaml` — a byte copy of the pinned decision core's floor, digest-pinned in `contracts/review-lane-pin.yaml`; the required `pytest-suite` checks OpenSpec coverage against it and its freshness against the core in tests it watches by name.
- `contracts/` — every other file is a published contract artifact (schema, contract document, policy or conformance corpus); the versioning policy commits the manifest and changelog atomically with contract files, so an edit here is a contract change that only a release cut records.
- `governance/` — the human-only review-authority and factory-identity registers with their wallets, grants and attestations; the required `wallet-validation` check reads them and asserts literal key and row counts that move only with an edit to its workflow.
- `requirements/` — the hash-pinned Python lock and its input, installed with `--require-hashes` by `pytest-suite`, `former-id-arrival-gate` and `openxdox-consumer-gate`; both files are release members.
- `pytest.ini` — the required `pytest-suite`'s rootdir anchor, option-free by design; an option here changes what every required pytest run collects, and so the counts `pytest-suite.yml` pins.
- `scripts/verify-*-pin.py` — the pin verifiers the required `wallet-validation`, `signed-execution-chain-gate` and `openxdox-consumer-gate` run before they trust a gitlink.
- `scripts/validate-*-pin.py` — the OpenSpec CLI pin gate (the required `openspec-cli-pin`) and the openRepoShape pin gate; the first is vendored byte-identical into sibling repositories.
- `scripts/install-pinned-openspec-cli.py` — installs, through the pin verifier's own code, the OpenSpec CLI the required `pytest-suite` drives.
- `scripts/validate-signed-execution-chain.py` — the required `signed-execution-chain-gate`.
- `scripts/signed_execution_chain/` — the chain reader the required `signed-execution-chain-gate` runs.
- `scripts/validate-former-id-arrival.py` — the required `former-id-arrival-gate`.
- `scripts/former_id_arrival.py` — the reader the required `former-id-arrival-gate` runs.
- `scripts/validate-factory-identity.py` — the factory-identity register reader inside the required `wallet-validation` check.
- `scripts/validate-release-tag-gate.py` — the required `release-tag-gate`.
- `scripts/doc_health/release_tag_publication.py` — the release-tag-publication family the required `release-tag-gate` runs.
- `scripts/validate-manifest-digests.py` — recomputes every manifest `sha256` row for the required `pytest-suite`.
- `tests/*_pin/` — the pin verifiers' own suites: the required `openxdox-consumer-gate` runs the openDox and openXdox suites with an exact skip count and named verdicts, and `tests/review_lane_pin/` holds the floor tests the required `pytest-suite` watches by name and the envelope-shape and pin-equals-`ref:` assertions.
- `tests/*_consumer_gate/` — pin the consumer-gate workflows' own invocation and assertion bytes.
- `tests/manifest_digests/` — the required-suite sweep that recomputes every manifest `sha256` row.
- `tests/ideation-dashboard/test_lens.py` — holds a test the required `openxdox-consumer-gate` watches by name.
- `tests/sequenced_after/corpus-ledger.yaml` — the machine-derived per-change sweep ledger, rewritten only by `scripts/validate-sequenced-after.py --seed-ledger`; the required `pytest-suite` fails when it disagrees with the OpenSpec corpus.
- `scripts/hermes_runtime_validation/` — the release verifier and a member of the declared bundle: an edit leaves the digest recorded for it under `contracts/releases/` stale, which doc-health's nightly `release-inventory-drift` reports as an error and the versioning policy remedies only with a release cut (no merge gate compares it).
- `scripts/intent_compliance/` — release member: an edit leaves its recorded digest stale until a release cut.
- `tests/intent-compliance/` — release member: an edit leaves its recorded digest stale until a release cut.
- `tests/clearing/` — release member: an edit leaves its recorded digest stale until a release cut.
- `tests/hermes_runtime_contracts/postgres/images.lock.yaml` — the digest-pinned PostgreSQL image lock and a release member.
- `scripts/__init__.py` — release member: an edit leaves its recorded digest stale until a release cut.
- `scripts/hermes-runtime-dataset-digest.py` — release member (a named validator): an edit leaves its recorded digest stale until a release cut.
- `scripts/validate-clearing-dispatch.py` — release member (the clearing validator): an edit leaves its recorded digest stale until a release cut.
- `scripts/validate-contract-release.py` — the release CLI and a release member: an edit leaves its recorded digest stale until a release cut.
- `scripts/validate-hermes-runtime-contracts.py` — release member (a named validator): an edit leaves its recorded digest stale until a release cut.
- `scripts/validate-intent-compliance.py` — release member (the intent validator): an edit leaves its recorded digest stale until a release cut.
- `docs/contract-versioning-policy.md` — the versioning policy and a release member: an edit leaves its recorded digest stale until a release cut.
- `docs/terminology-and-repo-topology.md` — normative document and release member: an edit leaves its recorded digest stale until a release cut.
- `docs/xfactory-domain-factory-model.md` — normative document and release member: an edit leaves its recorded digest stale until a release cut.
- `docs/opendox-carve-manifest.yaml` — the carve manifest: the carve commit and a `sha256` for every carved path, through whose rows `scripts/carved_reach.py` resolves every carved import.
- `ideation/cross-reference.yaml` — generated readiness index pinning `generation.source_revision` and passage digests, bot-custodied under the merge-approval envelope; a required-suite test reproduces it at the pinned revision.
- `ideation/cross-reference.md` — generated projection of `ideation/cross-reference.yaml`, never edited by hand.
- `ideation/dashboard/` — append-only, bot-custodied intent and gate-action records under the merge-approval envelope; the intents carry digests.
- `health/` — generated lane run records pinned to a source revision, and a measured neutrality baseline.
- `scripts/ideation_dashboard/doxbench_contracts.py` — records `CONTRACT_REF` and `SCHEMA_DIGESTS`, the release commit and schema digests it verifies consumer bytes against.
- `scripts/code_surface.py` — `CLOSED_REGISTER` pins the digest of each excepted OpenSpec packet declaration.
- `examples/avatar-first-ui/fixtures/deterministic/` — fixtures whose registered files carry per-file `sha256` rows in `contracts/manifest.yaml`, recomputed by the required `pytest-suite`.
- `scripts/apply-domain-starter.py` — the domain-factory starter: every file it scaffolds or upgrades in a DomainxFactory repository is stamped with its `STARTER_VERSION`, and OpsxFactory pins the validator it generates by digest.
- `.specify/memory/constitution.md` — the versioned constitution every Constitution Check reads; it is amended only through an OpenSpec change with a version bump.
- `.specify/integrations/` — records the SHA-256 of every installed Speckit file.
- `.specify/extensions/.registry` — records the git extension's manifest hash.
- `README.md` — its `## OpenSpec Records` block records every OpenSpec change with its ratification and landing, and is a shared substrate under the lane protocol.

`[H]` plausibly fits a pattern-copying change that touches none of these paths and no file whose `Status:` header reads `ratified`, `standard` or `record`: a test module that mirrors its siblings and adds no skip (both required pytest runs pin their skipped count exactly), an example under `examples/` beside its siblings, a `Status: draft` document or ideation note, or a helper under `scripts/` that no gate runs.
