# Tasks: add-openspec-cli-pin

Status: draft

**NOTHING IS TICKED THAT DID NOT LAND.** Slices 1–4 landed in the proposing pull
request and their evidence — command lines and outcomes, measured on the branch —
is recorded beside each task. Slice 5 is successor work in this repository and
slice 6 is successor work in five other repositories; neither is ticked and each
names its owner. **AMENDED 2026-09-08:** SLICE 5 IS COMPLETE. 5.1 was
ticked 2026-09-05 (PR #687) and 5.2 is ticked here by
`pin-openspec-cli-dependency-closure`, each in its own pull request with its own
green run, which is what those tasks demanded. Slice 6 is ticked for 6.1 and
6.3–6.5 (four consuming repositories wired); 6.2 (OpsxFactory) and 3.3 remain.
Was: **AMENDED 2026-09-05:** 5.1 is now ticked — it landed in its own pull
request, which is what the task itself demanded — and its evidence is recorded
beside it in the same form. The rest of slice 5 and all of slice 6 are untouched
and still owed.

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

- [x] **5.1** **(DONE 2026-09-05, PR #687 — its own diff and its own green run,
      exactly as this task required.)** `.github/workflows/pytest-suite.yml`'s
      literal `npm install -g @fission-ai/openspec@1.2.0` is replaced by
      `scripts/install-pinned-openspec-cli.py --cache-dir "${RUNNER_TEMP}/openspec-cli-pin"`,
      a standard-library INSTALLER that loads
      `scripts/validate-openspec-cli-pin.py` by path and calls its own
      `read_pin`/`resolve_pinned`/`assert_reported_version` — no second parser,
      no second copy of the version or the integrity — then appends the verified
      executable's directory to `$GITHUB_PATH`. It is NOT a `--verify-only` mode
      of the verifier: that mode is forbidden by `neutral-product-pin` and this
      task does not reopen the decision, so a green here means "the pinned bytes
      are on PATH" and never a verdict about the corpus, which still comes only
      from `validate-openspec-cli-pin.py --all`. Eleven new tests in
      `tests/openspec_cli_pin/` (81 → 92): the workflow's non-comment bytes carry
      neither the version, nor the integrity, nor `@fission-ai/openspec@` at all;
      the installer's `$GITHUB_PATH` append, its exit-2 refusal, and the absence
      of any scan-target option. Was: **Owner: openxFactory.** Deliberately not
      done here — that workflow is this repository's most load-bearing required
      check, and a change to how it obtains the CLI deserves its own diff and its
      own green run.
- [x] **5.2** **(DONE 2026-09-08, by `pin-openspec-cli-dependency-closure` —
      its own packet, its own diff and its own green run, on a ruling.)** The
      four exits were put to Brett Heap in session and he chose one, verbatim
      *"Vendor a lockfile (Recommended)"* (2026-09-08T14:14:49Z, first-hand;
      the other three — enumerate the resolved tree in the pin, vendor the built
      tree as one artifact by digest, accept the shortfall as declared — are
      recorded with their reasons in that packet's `design.md` § 1).
      `contracts/openspec-cli-pin.1.12.0.package-lock.json` is committed beside
      the pin: `lockfileVersion: 3`, 42,613 bytes, **80 packages**, every one
      carrying a `resolved` URL and an `integrity`, and its entry for
      `@fission-ai/openspec` carrying this pin's own referent character for
      character. The pin records it as `lockfile:` (a bare name resolving beside
      the pin), `lockfile_integrity:` and `lockfile_packages:`;
      `scripts/validate-openspec-cli-pin.py` hashes the committed file BEFORE any
      registry round trip, refuses the new `pin-lockfile-mismatch` on digest
      drift, on a lockfile locking another artifact than the pin, and on a tree
      of the wrong size, and INSTALLS THROUGH IT with `npm ci --ignore-scripts`
      in a staging project whose `package.json` is DERIVED from the lockfile's
      own root entry — never `npm install`. The reuse cache is keyed on the
      lockfile's digest as well as the artifact's.
      `scripts/install-pinned-openspec-cli.py` gains the closure by CALLING
      `pinned_lockfile`/`verify_lockfile` and carries no second copy of anything.
      Thirty new tests (93 → 123); the gate run is exit 0 through the lockfile
      path with the installed tree walked and compared entry by entry against the
      lockfile (80 = 80, zero version mismatches). `--ignore-scripts` stays, now
      as defence in depth over a KNOWN tree. WHAT STAYS OPEN, named there rather
      than implied: trust-on-first-use of the 79 registry integrity values, the
      regeneration obligation at every bump (written into the pin's header and
      enforced by the verifier's first-run refusal), and the `1.2.0` rollback
      entry, which is declared UNCOVERED in the pin itself. Was: Decide the
      dependency closure (design OI-1). **Owner: openxFactory.** The referent
      addresses the CLI's bytes and not its nine caret-ranged dependencies;
      `--ignore-scripts` mitigates and does not repair.

## Slice 6 — successor work in consuming repositories (not this packet)

Each is a change in that repository, because each has its own CI, its own
validator conventions and its own `stack.yaml`.

- [x] **6.1** **(DONE 2026-09-06, via four landings.)** `codexFactory` — wire
      the pinned entrypoint into CI; pin the consumed `openxFactory` version in
      `stack.yaml`. codexFactory #216 `prepare-openspec-1.12-readiness`
      (`06935a4a`, merged 2026-09-05) authored four real Purposes and declared
      the council-clearance rename with the `Merged into` marker, measuring
      23 passed / 2 declared-rename findings of 25 under the pinned 1.12.0.
      openxFactory #697 `disposition-codexfactory-declared-renames`
      (`724a2a4f`, merged 2026-09-05) recorded the two `repo: codexFactory`
      entries in `contracts/openspec-cli-pin.yaml`, ratified "ratify 697".
      xFactory (aggregation) #275 (`5deaf90`, merged 2026-09-05) moved the
      openxFactory submodule pointer `3d7b8f3b` → `724a2a4f`, so the doc-health
      nightly resolves the four-entry pin. codexFactory #227
      `adopt-openspec-cli-pin-gate` (`bb66d85c`, merged 2026-09-06) wired
      `scripts/validate-docs.sh` to run `validate-openspec-cli-pin.py --all`
      fail-closed in CI from the pinned checkout, pinned Node to 24.18.0, moved
      `stack.yaml`'s `xfactory.contract_ref` `bbbbeda9` → `724a2a4f`, and added
      `tests/test_openspec_cli_pin_gate.py`; ratified "ratify 227", merged on
      "merge 227 when the pilot is green". CI's gate at that pin:
      `openspec-cli-pin: @fission-ai/openspec@1.12.0 … verified`,
      `DISPOSITIONED FINDINGS in codexFactory (2 applied)`,
      `0 UNDISPOSITIONED failures`.
- [ ] **6.2** `OpsxFactory` — same. Its corpus is the one measured at
      `34 passed, 10 failed (44 items)` under 1.12.0, so it is where the pin's
      value is felt first.
- [x] **6.3** **(DONE 2026-09-08, via two landings.)** `MedxFactory` — same;
      it has no workflows at all today, so this would be its first OpenSpec
      gate. MedxSoft/MedxFactory #25 `prepare-openspec-1.12-readiness`
      (`3d8cef76`, merged) took its gate reading from `9 passed, 4 failed` to
      `14 passed, 0 failed`: three real Purposes authored, and the two
      `patient-snapshot-ledger-custody` requirements that had sat under a
      hand-written `## Modified by …` heading since 2026-08-06 brought back
      inside `## Requirements`, where the pinned CLI can see them. Admitted to
      the queue on Brett Heap's 2026-09-06 word "go", ratified and merged on
      his 2026-09-07 word "ratify and merge". MedxSoft/MedxFactory #28
      `adopt-openspec-cli-pin-gate` (`9884668d`, merged) pins `stack.yaml`'s
      `xfactory.contract_ref` at `724a2a4fb3dc0fb996bb5f3736634eecc8f829c3` —
      this change's own merge commit, resolved through the aggregation's
      openxFactory pointer — and wires `.github/workflows/validate.yml`
      (new) to mint a downscoped openxfactory App installation token, check
      openxFactory out at that pin, and run `make validate` with the CLI-pin
      gate as one of its legs; the same PR's Sonar `Scan` job also reads
      openxFactory through the App now, on Brett Heap's 2026-09-08 word "do
      option 1". CI's gate at that pin: `Totals: 15 passed, 0 failed`. Merged
      on Brett Heap's first-hand 2026-09-08 word "merge all 3" (~13:14Z),
      heard by lane codeXfactory-1. The per-repository secrets
      `OPENXFACTORY_APP_ID` / `OPENXFACTORY_APP_PRIVATE_KEY` were provisioned
      by lane codeXfactory-1 on Brett's word on 2026-09-07; MedxFactory does
      not need the App installed on its own org — the mint is against the
      App's opensoft installation for openxFactory. No disposition owed in
      `contracts/openspec-cli-pin.yaml`: no MODIFIED deltas, no markers, no
      scenario-currency findings. Was: `MedxFactory` — same; it has no
      workflows at all today, so this would be its first OpenSpec gate. That
      claim was already stale by the time this box ticks — `sonarcloud.yml`
      and `session-open-pr.yml` existed in MedxFactory before either PR
      landed — but the part that held is narrower and true: neither workflow
      ran an OpenSpec gate, and #28 is the first that does.
- [x] **6.4** **(DONE 2026-09-08, via two landings.)** `LedgerxFactory` —
      same. ledgerXfactory/LedgerxFactory #32 `prepare-openspec-1.12-readiness`
      (`8c2ffe29`, merged while the repository still lived at
      `opensoft/LedgerxFactory`) took its gate reading from `5 passed, 11
      failed` to `17 passed, 0 failed`: eleven Purposes written for the
      promoted specs, plus a protected-surface re-pin. Admitted to the queue
      on Brett Heap's 2026-09-06 word "go", ratified and merged on his
      2026-09-07 word "ratify and merge". The repository itself moved twice
      in the interim, both on 2026-09-07 and both redirecting from the old
      path: `opensoft/LedgerxFactory` → `LedgerXcorp/LedgerxFactory` →
      `ledgerXfactory/LedgerxFactory`. #34 `adopt-openspec-cli-pin-gate`
      (`0f265d8c`, merged at the settled `ledgerXfactory/LedgerxFactory`
      address) pins `stack.yaml`'s `xfactory.contract_ref` at
      `724a2a4fb3dc0fb996bb5f3736634eecc8f829c3` and wires this repository's
      FIRST workflow, `.github/workflows/validate.yml`, to mint a downscoped
      openxfactory App installation token, check openxFactory out at that
      pin, and run `scripts/validate-openspec-cli-pin.py --all --no-cache`.
      CI's gate at that pin: `18 passed, 0 failed`, and all 19 of
      LedgerxFactory's validators now run in CI. Merged on Brett Heap's
      first-hand 2026-09-08 word "merge all 3" (~13:14Z), heard by lane
      codeXfactory-1. Same secret provisioning as 6.3 (`OPENXFACTORY_APP_ID`
      / `OPENXFACTORY_APP_PRIVATE_KEY`, lane codeXfactory-1, 2026-09-07); no
      App install needed on LedgerxFactory's own org. No disposition owed in
      `contracts/openspec-cli-pin.yaml`.
- [x] **6.5** **(DONE 2026-09-08, via two landings.)** `AdxFactory` — same.
      opensoft/AdxFactory #7 `prepare-openspec-1.12-readiness` (`fea04fee`,
      merged) took its gate reading from `1 passed, 2 failed` to `4 passed, 0
      failed`: two Purposes written for the promoted specs. Admitted to the
      queue on Brett Heap's 2026-09-06 word "go", ratified and merged on his
      2026-09-07 word "ratify and merge". opensoft/AdxFactory #8
      `adopt-openspec-cli-pin-gate` (`a9deb245`, merged) pins `stack.yaml`'s
      `xfactory.contract_ref` at `724a2a4fb3dc0fb996bb5f3736634eecc8f829c3`
      and wires this repository's FIRST workflow,
      `.github/workflows/validate.yml`, to mint a downscoped openxfactory
      App installation token, check openxFactory out at that pin, and run
      `scripts/validate-openspec-cli-pin.py --all --no-cache`. CI's gate at
      that pin: `5 passed, 0 failed`. Merged on Brett Heap's first-hand
      2026-09-08 word "merge all 3" (~13:14Z), heard by lane codeXfactory-1.
      Same secret provisioning as 6.3 (`OPENXFACTORY_APP_ID` /
      `OPENXFACTORY_APP_PRIVATE_KEY`, lane codeXfactory-1, 2026-09-07); no
      App install needed on AdxFactory's own org. No disposition owed in
      `contracts/openspec-cli-pin.yaml`.

## Slice 7 — archive preflight

- [x] **7.1** **(DONE 2026-09-04.)** Ratification by Brett Heap, recorded in
      `review/ratification-2026-09-04.md` — verbatim "ratify 667", heard
      first-hand by session opsxfactory-fb, relay path recorded. Was: recorded in
      `review/ratification-<date>.md`. Not sought by this packet's landing.
- [ ] **7.2** `OPENSPEC_TELEMETRY=0 openspec validate add-openspec-cli-pin
      --strict` and `--all --strict` green at the archive gate, re-run at that
      time rather than trusted from authoring.
- [ ] **7.3** Realization evidence per `release-realization`: merged, with the
      `openspec-cli-pin-gate` check green on a pull request. `target_release` is
      `none`, so no bundle cut is owed.
