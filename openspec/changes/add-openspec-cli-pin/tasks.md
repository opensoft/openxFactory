# Tasks: add-openspec-cli-pin

Status: draft

**NOTHING IS TICKED THAT DID NOT LAND.** Slices 1–4 landed in the proposing pull
request and their evidence — command lines and outcomes, measured on the branch —
is recorded beside each task. Slice 5 is successor work in this repository and
slice 6 is successor work in five other repositories; neither is ticked and each
names its owner.

**RATIFICATION HAS NOT HAPPENED.** Brett Heap authorized the DRAFT on 2026-09-04
(*"draft the openxFactory pin change, pinned at 1.2.0"*). Task 7.1 records
ratification when it happens and nothing below decides it.

---

## Slice 1 — the pin

- [x] **1.1** Author `contracts/openspec-cli-pin.yaml` — `schema_version: 1`,
      `kind: pinned_contract_manifest` reused unchanged, `package:
      "@fission-ai/openspec"`, `version: "1.2.0"` as the LABEL,
      `revision_kind: package_integrity`, and the REFERENT
      `integrity: "sha512-2XDmPZcVY0Bs014lP9aoxe3VoEU8hFvqaBFxQaiJO2nhC8vTKCyo6sT/5YpQcOTfR/a64Hht2anTyqLR4eNhlg=="`
      with the registry's legacy `shasum: "0fd5333520c8846f0ac51727379b8812e2f13c1b"`
      and `tarball:` beside it. Header note argues tag-versus-referent exactly as
      `contracts/openreposhape-pin.yaml` does, and states the dependency-closure
      shortfall rather than leaving it to be discovered.
- [x] **1.2** Verify the recorded referent against the live registry rather than
      transcribing it. `npm view @fission-ai/openspec@1.2.0 dist --json` returns
      the integrity and shasum above; `npm pack @fission-ai/openspec@1.2.0`
      followed by a local SHA-512/SHA-1 recomputation over the 204,816-byte
      tarball reproduces BOTH exactly. The referent is a measurement, not a copy
      of a web page.
- [x] **1.3** Declare the consumer obligation IN the pin —
      `consumer_entrypoint:`, `pinned_invocation:` and `binary:` — so a
      repository reading the pin learns from the pin which command it owes.

## Slice 2 — the verifier and consumer entrypoint

- [x] **2.1** Author `scripts/validate-openspec-cli-pin.py` — standard library
      only, fail-closed, five ordered checks, five named refusal codes
      (`pin-tag-only`, `pin-no-target`, `pin-unresolvable`,
      `pin-integrity-mismatch`, `pin-version-mismatch`) and ONE fixed
      remediation trailer, on the sibling verifiers' shape.
- [x] **2.2** The artifact is fetched and BOTH digests recomputed BEFORE the CLI
      is installed and before it is invoked, per `neutral-product-pin`'s ordering
      rule. `npx` is not trusted to have resolved the right bytes.
- [x] **2.3** The default mode never consults `PATH`; `--path-mode` refuses
      `pin-version-mismatch` unless the local binary reports exactly the pin.
      Pinned positively by
      `test_the_default_mode_never_consults_path`, which places a wrong-version
      binary on `PATH` and asserts the run still passes AND that `shutil.which`
      was asked only for `npm`.
- [x] **2.4** No `--verify-only`; `--strict` accepted as a no-op; no
      `--no-strict`. A target-less invocation refuses `pin-no-target` BEFORE any
      registry round trip is spent — asserted by
      `test_no_scan_target_refuses_rather_than_self_testing`, which requires the
      recorded npm call list to be empty.

## Slice 3 — the gate

- [x] **3.1** Author `.github/workflows/openspec-cli-pin-gate.yml` mirroring
      `openreposhape-pin-gate.yml`: pull requests to `main`, `contents: read`,
      Python 3.12 and Node 22, no `pip install`, one invocation —
      `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`.
- [x] **3.2** The version appears NOWHERE in the workflow. The verifier reads the
      pin with its own parser, so there is one place the referent is written;
      `test_the_gate_workflow_reads_the_pin_and_carries_no_fourth_copy` asserts
      the absence against the workflow's own non-comment bytes.
- [ ] **3.3** Select `openspec-cli-pin` as a REQUIRED check on the organisation
      ruleset. **OPERATOR ACT, Brett Heap** — not this packet's to take, and not
      possible before the workflow has reported once.

## Slice 4 — tests and proof

- [x] **4.1** Author `tests/openspec_cli_pin/test_openspec_cli_pin.py` on
      `tests/openreposhape_pin/`'s shape: a synthetic pin written as TEXT (so the
      narrow reader is exercised every time) whose recorded address is the REAL
      digest of a payload the test holds, and a fictional registry installed at
      the subprocess boundary. `verify_artifact` does real SHA-512 and SHA-1 work
      on real bytes; only the registry is fictional. No test reaches the network.
      **`python3 -m pytest tests/openspec_cli_pin/ -q` → `41 passed`.**
- [x] **4.2** No `conftest.py` is added to the new directory, deliberately:
      `tests/hermeticity.py`'s `CONFTEST_HOOKUPS` is a pinned set, and a new
      conftest would have to join it and carry the slot claim. The directory is
      guarded through `tests/conftest.py`, which the repo-root `pytest.ini`
      rootdir anchor guarantees. No test skips, so `pytest-suite.yml`'s exact
      `EXPECT_SKIPPED: "21"` is untouched and its two FLOORS only rise.
- [x] **4.3** Prove the entrypoint end-to-end ONCE for real, against the live
      registry. `python3 scripts/validate-openspec-cli-pin.py --all --strict`
      fetched `@fission-ai/openspec@1.2.0`, verified the integrity, installed it
      into a private prefix, and reported
      `Totals: 90 passed, 0 failed (90 items)` — the same totals the local binary
      reports, exit 0.
- [x] **4.4** Measure the upgrade cost rather than assert it.
      `npx -y @fission-ai/openspec@1.12.0 validate --all --strict` on this branch
      → `Totals: 49 passed, 41 failed (90 items)`. The 41 failures are unchanged
      from the pre-packet measurement of `48 passed, 41 failed (89 items)`, so
      THIS PACKET IS CLEAN AT BOTH VERSIONS and adds nothing to the backlog an
      upgrade must clear.

## Slice 5 — successor work in THIS repository (not this packet)

- [ ] **5.1** Replace `.github/workflows/pytest-suite.yml:400`'s literal
      `npm install -g @fission-ai/openspec@1.2.0` with a read of the pin file.
      **Owner: openxFactory.** Deliberately not done here — that workflow is this
      repository's most load-bearing required check, and a change to how it
      obtains the CLI deserves its own diff and its own green run.
- [ ] **5.2** Decide the dependency closure (design OI-1). **Owner:
      openxFactory.** The referent addresses the CLI's bytes and not its nine
      caret-ranged dependencies; `--ignore-scripts` mitigates and does not repair.

## Slice 6 — successor work in consuming repositories (not this packet)

Each is a change in that repository, because each has its own CI, its own
validator conventions and its own `stack.yaml`.

- [ ] **6.1** `codexFactory` — wire the pinned entrypoint into CI; pin the
      consumed `openxFactory` version in `stack.yaml`.
- [ ] **6.2** `OpsxFactory` — same. Its corpus is the one measured at
      `34 passed, 10 failed (44 items)` under 1.12.0, so it is where the pin's
      value is felt first.
- [ ] **6.3** `MedxFactory` — same; it has no workflows at all today, so this
      would be its first OpenSpec gate.
- [ ] **6.4** `LedgerxFactory` — same.
- [ ] **6.5** `AdxFactory` — same.

## Slice 7 — archive preflight

- [ ] **7.1** Ratification by Brett Heap, recorded in
      `review/ratification-<date>.md`. Not sought by this packet's landing.
- [ ] **7.2** `OPENSPEC_TELEMETRY=0 openspec validate add-openspec-cli-pin
      --strict` and `--all --strict` green at the archive gate, re-run at that
      time rather than trusted from authoring.
- [ ] **7.3** Realization evidence per `release-realization`: merged, with the
      `openspec-cli-pin-gate` check green on a pull request. `target_release` is
      `none`, so no bundle cut is owed.
