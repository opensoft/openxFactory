# Quickstart: proving the council-convening family

**Feature**: [spec.md](spec.md) · **Plan**: [plan.md](plan.md) · **Tasks**: [tasks.md](tasks.md)

This guide is for running and validating the family. It does not implement it: implementation steps are in [tasks.md](tasks.md). Commands run from the openxFactory repository root, inside the declared py-bench container, in the phase's own worktree.

## Prerequisites

- Python 3.12 with the hash-locked set installed: `pip install --require-hashes -r requirements/hermes-runtime-contracts.lock`. This provides `jsonschema`, `PyYAML` and `cryptography`.
- No submodule and no network are needed for this family's tests or validator.
- The governing packet is in `main` (#1267, `80f47483`), and this plan, #1268, has landed before PR-1 opens.

## Per phase: the proof that a phase is done

1. **Tests first, red.** Before the phase's implementation tasks run, the new tests fail, every failure is an absent name or file, and the failure count is recorded in `evidence.md`:

   ```sh
   python3 -m pytest tests/council_convening -q -m "not postgres"
   ```

2. **Green.** The phase's tests pass, and the validator self-test is clean:

   ```sh
   python3 -m pytest tests/council_convening -q -m "not postgres"
   python3 scripts/validate-council-convening.py
   ```

   The self-test prints every proof-of-work note listed in [contracts/validator-cli.md](contracts/validator-cli.md) for the phase, and exits 0.

3. **Corpus reproducible.**

   ```sh
   python3 -m scripts.council_convening.generate --check
   python3 scripts/validate-council-convening.py corpus
   ```

   The first command reports no drift. The second prints the totals and the index digest for `evidence.md`.

4. **Repository gates.**

   ```sh
   python3 scripts/validate-openspec-cli-pin.py --all --strict
   python3 scripts/doc-health.py --single-repo . --report-out <scratch>/doc-health-head.md
   python3 -m pytest tests/ -q -m "not postgres"
   ```

   - The OpenSpec run exits 0 with no undispositioned failure.
   - The doc-health head report adds no finding beyond the base report of the same day for the phase's paths.
   - The suite clears the `pytest-suite` floors, with `skipped` equal to its pinned `EXPECT_SKIPPED`.
   - **Phase 1 only**, because it widens `digest_subject`: also run the two validators that consume it, and the suites around it.

     ```sh
     python3 scripts/validate-signed-execution-chain.py
     python3 scripts/validate-clearing-dispatch.py
     python3 -m pytest tests/signed_execution_chain tests/clearing tests/code_surface tests/intent-compliance tests/manifest_digests -q
     ```

5. **The PR's scope (implementation phases).** No commit of a phase PR touches a surface this feature must not edit. The base is the PR's own merge base:

   ```sh
   git diff --name-only origin/main...HEAD -- governance/review-authority openXwallet openspec/changes/renew-resolved-council-protocol
   ```

   The output is empty.

6. **Release phases only (7 and 8).**

   ```sh
   python3 scripts/validate-contract-release.py build --tag <allocated> --output contracts/releases/<allocated>.digests.yaml
   python3 scripts/validate-contract-release.py verify-commit --commit <candidate>
   python3 scripts/validate-contract-release.py verify-promotion --commit <candidate> --remote origin --tag <allocated>
   ```

   - The release-tag gate is green.
   - After the owner publishes the tag, `verify-tag --remote origin --tag <allocated>` passes from an independently refreshed checkout.
   - These steps are evidence for the owner's act; they are not the act.

## Checking one record

```sh
python3 scripts/validate-council-convening.py check path/to/record.json
python3 scripts/validate-council-convening.py check --historical path/to/legacy-or-new-record.json
python3 scripts/validate-council-convening.py select --producer producer-selection.json --consumer consumer-selection.json
```

`check` runs the offline rules only. A rule that needs live state is reported as not offline-checkable, never as passed. A legacy record is routed to the legacy verifier, and the run exits 3, which is never a pass.

## For a successor: pin and run the corpus

1. Pick the openxFactory commit. After Phase 7, pick the published bundle's commit.
2. Read `contracts/manifest.yaml` at that commit and record the `sha256` of `contracts/council-convening/conformance/index.json`. That is the corpus digest. Before Phase 7 there is no row: compute the raw SHA-256 yourself and label it unpublished.
3. Run your own adapter over every vector whose `applies_to` names your side, at its `evaluation_time`, with its oracles injected. Compare each outcome with `expected`, exactly ([contracts/conformance-corpus.md](contracts/conformance-corpus.md)).
4. Record the commit, the digest, the per-area counts and the exits in your own evidence (049 T013; 025 tasks once they exist). Matching counts are not agreement: every vector's outcome, refusal and finding must match.

## What these commands never prove

They do not prove publication, a pin advance, broker capability, deployment or activation. Each of those is a separately evidenced owner act (spec User Story 3, scenario 4). A green corpus run in one repository is not the other side's conformance.
