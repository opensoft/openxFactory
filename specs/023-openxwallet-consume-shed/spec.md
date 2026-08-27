# Feature Specification: openxFactory consumes openXwallet and sheds the wallet paths (P3)

**Feature Branch**: `023-openxwallet-consume-shed`

**Created**: 2026-08-27

**Status**: Draft

**Input**: User description: "P3: openxFactory pins opensoft/openXwallet at wallet-v1.1 via a nested gitlink + contracts/openxwallet-pin.yaml with a fail-closed verifier, runs the pinned validator as the REQUIRED wallet-validation check over its own tree, repoints trust-anchor, and sheds the twelve carved path sets in one atomic PR that cuts contract-v2.0 — realizes tasks.md group 7 of ratified change split-openxwallet-repo"

**Realizes**: `openspec/changes/split-openxwallet-repo` — `tasks.md` §7 (P3), 33
tasks. Governing design decisions **D1** (the pin file's shape), **D2** (the
fail-closed verifier and the one remediation trailer), **D3** (the consumer gate,
its auth and the test that pins its invocation), **D4** (openxFactory's first pin
is `wallet-v1.1`), **D6** (this cut is the MAJOR), **D9**–**D14** as they reach
openxFactory. Clarifications **N1**, **N4**, **N5**, **N7**. Governing procedure:
`docs/contract-versioning-policy.md` (the breaking class at `:250-254`,
merge-order numbering at `:30-31`).

## Why this feature exists

The wallet is one product filed as features of a factory layer. `P2` carved it
into `opensoft/openXwallet` — a COPY; nothing was deleted from openxFactory — and
`P2b` published `wallet-v1.1`, the tag that adds the nested-repository prune the
openxFactory sweep depends on. `P2.5` cut `contract-v1.47`, the deprecating minor
that `docs/contract-versioning-policy.md:250-254` requires before a shape may be
removed.

This feature is the load-bearing half: openxFactory stops OWNING the wallet
family and starts CONSUMING it at a pinned commit, and the twelve carved path
sets leave its tree. It is **one atomic pull request** because
`scripts/validate-trust-anchor.py` exits 2 when the openxWallet custody registry
is absent — no ordering of two commits leaves a green intermediate.

The required gate survives by **alias**, not by repoint: org ruleset 21538893
pins the token `wallet-validation`, which is a JOB ID and not a filename, so the
renamed workflow keeps `jobs: wallet-validation:` and no operator act stands
between this pull request and merge.

## Clarifications

### Session 2026-08-27

- Q: which App token reaches the private `opensoft/openXwallet` from openxFactory
  Actions? → A: the repository's own content App (`OPENXFACTORY_APP_ID` /
  `OPENXFACTORY_APP_PRIVATE_KEY`, App `4253636`, installation `145372182`,
  `repository_selection: all`). The org secret `XFACTORY_APP_ID` that
  `doc-health-reusable.yml` names is visibility-`selected` and openxFactory is
  NOT among its two repositories, so the PATTERN of
  `doc-health-reusable.yml:140-158` is adopted while the SECRET NAMES are the
  ones this repository actually holds.
- Q: `submodules: true` on the checkout, or a scoped init step? → A: a scoped
  `git submodule update --init openXwallet`, per `tasks.md` 7.13 and 7.16
  ("`submodules: true` alone is NOT sufficient and is explicitly not the fix")
  and D3's rejection of `--recursive`. A blanket `submodules: true` would also
  initialize `installs/omnigent-install`, which no gate here reads.
- Q: does the aggregation's second scoped init reach a nested gitlink that does
  not exist in a pre-P4 checkout? → A: it is guarded on the nested
  `.gitmodules` declaring `submodule.openXwallet.path`, so the widened filter is
  inert until P4 bumps the aggregation's openxFactory pin and never fails a
  nightly for the ordering.
- Q: the bundle number. → A: `contract-v2.0` is authored here and RE-VERIFIED at
  merge order per `docs/contract-versioning-policy.md:30-31`; it is the one next
  major, which the policy permits naming where it forbids reserving a minor.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The pinned reader runs, and the register was actually opened (Priority: P1)

A contributor opens a pull request against openxFactory's default branch. The
REQUIRED `wallet-validation` check clones the pinned `openXwallet` at the exact
commit the pin file names, refuses to proceed if any of the eight digests
disagrees, and then runs the PINNED validator over openxFactory's own tree — the
tree that still holds `governance/review-authority/`.

**Why this priority**: this is the requirement being REPLACED. A live ruleset
requires this token today; if the check cannot report green on this pull request's
own head, the pull request is unmergeable and the wave stops.

**Independent Test**: from a clean checkout, run the gate's literal invocation and
assert the log carries the `repo scan:` note and the `intake register read:` NOTE
and carries neither `no intake register at this tree` nor any `register-*`
finding code.

**Acceptance Scenarios**:

1. **Given** the submodule is initialized at the pinned commit, **When** the gate
   runs, **Then** the pin verifier exits 0, the syntax gate exits 0, the pinned
   validator exits 0, and the register-read conjunction holds.
2. **Given** the pinned validator is invoked with no path argument, **When** the
   invocation test runs, **Then** it FAILS — a target-less invocation is a green
   check that opened no register.
3. **Given** a deliberately malformed row under
   `governance/review-authority/`, **When** the gate runs, **Then** it goes RED
   with a `register-*` finding naming the full path.

### User Story 2 - The pin is checkable, and a stale checkout is refused by name (Priority: P1)

An operator or a reviewer can answer "which reader ran?" from the tree alone. The
pin file names the repository, the submodule path, the 40-hex commit, the bundle
tag as a LABEL, the carve commit, eight per-file sha256 digests and the members
the publisher declares content-addressed by commit. One script checks all of it
and every refusal names itself and prints the same remediation.

**Why this priority**: the pin is the only thing that makes "which reader ran" an
auditable fact rather than a trust assumption, and the floor codexFactory widens
in the same wave protects exactly this file and this gitlink.

**Independent Test**: `python3 scripts/verify-openxwallet-pin.py` exits 0 on a
correctly initialized tree; each of the six refusal classes is reproducible in a
fixture and exits 2 with its named code and the remediation trailer.

**Acceptance Scenarios**:

1. **Given** an uninitialized submodule, **When** the verifier runs, **Then** it
   exits 2 with `pin-submodule-uninitialized` and the remediation trailer.
2. **Given** a checked-out revision that differs from the RECORDED gitlink,
   **When** the verifier runs, **Then** it exits 2 with `pin-checkout-mismatch` —
   distinct from `pin-gitlink-mismatch`, because only one comparison catches each
   case.
3. **Given** a `files:` member whose bytes changed, **When** the verifier runs,
   **Then** it exits 2 with `pin-digest-mismatch` naming the member.
4. **Given** a pin whose `revision_kind` is not `commit`, **When** the verifier
   runs, **Then** it exits 2 with `pin-tag-only`.
5. **Given** an aggregation checkout, **When** the verifier runs with
   `--aggregation-root <path>`, **Then** it compares the root gitlink against the
   nested gitlink and refuses a disagreement with the same vocabulary.

### User Story 3 - The trust-anchor family reads the wallet through the gitlink (Priority: P1)

`scripts/validate-trust-anchor.py` composes with the canonical openxWallet
custody registry at run time. After the shed that registry is not an openxFactory
file, so the validator reads it through the `openXwallet/` gitlink and refuses
with an IDENTIFIED code instead of a bare "not found" when the submodule is
uninitialized or the digest disagrees with the pin.

**Why this priority**: this is why the pull request is atomic. The validator's
hard exit is what forbids a two-commit ordering.

**Independent Test**: `python3 scripts/validate-trust-anchor.py .` exits 0 on an
initialized tree; `python3 -m pytest tests/trust-anchor/ -q` collects and passes,
including two new cases for the uninitialized-submodule and digest-disagreement
refusals.

**Acceptance Scenarios**:

1. **Given** an initialized submodule, **When** the validator runs, **Then** its
   composition note names the resolved path under `openXwallet/`.
2. **Given** an uninitialized submodule, **When** the validator runs, **Then** it
   exits 2 with the verifier's named refusal and the remediation trailer.
3. **Given** any trust-anchor test module, **When** pytest COLLECTS it, **Then**
   collection succeeds — `OPENXWALLET_REGISTRY_PATH` stays a module-scope plain
   `Path` built by pure string join, because two test modules read it at setup and
   any import-time resolution that can fail kills the whole directory.

### User Story 4 - The shed is a properly published MAJOR (Priority: P2)

A domain repo pinning `contract-v1.47` stays conformant. A domain repo upgrading
past this cut is told, in the CHANGELOG, that the eight shapes are gone, where
they went, and how to consume them.

**Independent Test**: `contracts/releases/contract-v2.0.digests.yaml` is
byte-reproducible from `scripts/validate-contract-release.py build --tag
contract-v2.0`, and the release inventory verify passes.

**Acceptance Scenarios**:

1. **Given** the eight manifest rows are deleted, **When** the CHANGELOG is read,
   **Then** it carries a MAJOR entry with the removal and the migration path.
2. **Given** the cut, **When** `docs/contract-versioning-policy.md`'s
   "Deprecations Currently In Force" list is read, **Then** the openxWallet entry
   is recorded EXECUTED rather than in force.
3. **Given** the pin, **When** the conformance validator for this family is
   named, **Then** it is the pinned `openXwallet/scripts/validate-openxwallet.py`
   at the digest the pin records — the move IS the `:253-254` update.

### Edge Cases

- **The register row expires 2026-11-23.** Past that instant `check_register`
  raises `register-row-expired` as an ERROR and reds the REQUIRED gate on every
  later pull request, this one included. Landing before 2026-11-01 is the chosen
  control (task 7.1).
- **A shared-tree collision on `contracts/manifest.yaml`.** The declared freeze is
  unenforceable; the pull request REBASES and re-verifies the eight digests
  immediately before merge, and that re-verification is what the evidence row
  carries.
- **A pre-P3 checkout.** The verifier refuses with a named code and the
  remediation trailer rather than falling back to an in-tree validator — an
  unanswerable question is never an implicit pass.
- **Records must not be rewritten.** The archived `2026-08-08-add-openxwallet`
  packet and `docs/archive-record-discrepancies.md` are ANNOTATED. The two
  promoted specs empty when `openspec archive` applies the ratified REMOVED
  deltas, not here.
- **`governance/review-authority/` must not move.** All four files stay; nothing
  under that directory is touched.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The repository SHALL declare a nested submodule at path
  `openXwallet` with url `git@github.com:opensoft/openXwallet.git`, recorded at
  commit `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705` (`wallet-v1.1`).
- **FR-002**: `contracts/openxwallet-pin.yaml` SHALL carry `kind:
  pinned_contract_manifest` unchanged, `submodule_path: openXwallet`,
  `revision_kind: commit`, a 40-hex `commit`, `contract_bundle_tag: wallet-v1.1`
  as a LABEL, `carve_commit:
  30565e48ffe3d8a9773e10af33425701845e10f6`, eight `files:` members each with a
  `sha256`, and a `pinned_by_commit_only:` list of path-only members.
- **FR-003**: `scripts/verify-openxwallet-pin.py` SHALL perform six ordered
  checks and SHALL exit 2 with one of `pin-submodule-uninitialized`,
  `pin-gitlink-mismatch`, `pin-checkout-mismatch`, `pin-digest-mismatch`,
  `pin-member-missing`, `pin-tag-only`.
- **FR-004**: Every fail-closed refusal added by this feature SHALL print the one
  fixed remediation trailer naming `git submodule update --init openXwallet` and
  `openXwallet/docs/pin-resync-runbook.md`.
- **FR-005**: `scripts/verify-openxwallet-pin.py --aggregation-root <path>` SHALL
  compare the aggregation's root gitlink for `openXwallet` against the nested
  gitlink and refuse a disagreement in the same vocabulary.
- **FR-006**: `OPENXWALLET_REGISTRY_PATH` SHALL remain a module-scope plain
  `Path` produced by pure string join with NO I/O, rebased onto the pin's
  `submodule_path`.
- **FR-007**: `scripts/validate-trust-anchor.py`'s bare file-absent exit SHALL be
  replaced by a call to the verifier inside `main()`, never at import.
- **FR-008**: `.github/workflows/openxwallet-consumer-gate.yml` SHALL define
  `jobs:` key EXACTLY `wallet-validation`, trigger on `pull_request` to `main`,
  and run, in order: app token → global `insteadOf` rewrite → checkout → scoped
  `git submodule update --init openXwallet` → `verify-openxwallet-pin.py` →
  `python3 openXwallet/scripts/wallet-yaml-syntax-gate.py .` → `python3
  openXwallet/scripts/validate-openxwallet.py .` → the positive register
  assertion.
- **FR-009**: A test collected by the REQUIRED `pytest-suite` SHALL load the
  workflow YAML and assert `jobs` contains `wallet-validation` and that one step's
  `run` is EXACTLY `python3 openXwallet/scripts/validate-openxwallet.py .`.
- **FR-010**: The gate's register assertion SHALL be POSITIVE: the captured log
  carries the `repo scan:` note AND the `intake register read:` NOTE AND carries
  neither `no intake register at this tree` nor any `register-*` finding code.
- **FR-011**: `.github/workflows/pytest-suite.yml` SHALL gain the same app-token,
  `insteadOf` and scoped-init pattern, SHALL pin a TRIPLE (collected, passed,
  skipped) read from the JUnit XML attributes, and SHALL name the renamed
  workflow at all three of its references.
- **FR-012**: `.github/workflows/doc-health-reusable.yml` SHALL widen BOTH
  governed-submodule init filters with a second scoped init for the nested
  `openXwallet` gitlink, guarded so it is inert where the nested gitlink is not
  declared, and NOT `--recursive`.
- **FR-013**: The twelve carved path sets SHALL be deleted from openxFactory with
  exactly three deliberate exceptions: the two promoted specs (emptied by
  `openspec archive`, not here) and the archived `2026-08-08-add-openxwallet`
  packet (annotated, never removed).
- **FR-014**: `contracts/manifest.yaml` SHALL lose the eight wallet rows, SHALL
  reword every incoming citation to the pin rather than deleting it, and SHALL
  declare `contract_bundle_version: contract-v2.0`.
- **FR-015**: `contracts/CHANGELOG.md` SHALL gain a MAJOR entry stating the
  removal and the migration path; `contracts/README.md` SHALL collapse its three
  wallet rows to ONE "consumed at pin" row;
  `contracts/releases/contract-v2.0.digests.yaml` SHALL be built by the house
  tool; `docs/contract-versioning-policy.md` SHALL record the openxWallet
  deprecation EXECUTED.
- **FR-016**: `README.md` SHALL be corrected at every wallet-bearing range the
  proposal names, with the archive-ledger `add-openxwallet` entry ANNOTATED and
  never rewritten.
- **FR-017**: `.github/CODEOWNERS` SHALL drop the two departing validator lines
  and SHALL gain `/contracts/openxwallet-pin.yaml`,
  `/scripts/verify-openxwallet-pin.py`, `/openXwallet` and `/.gitmodules`.
- **FR-018**: `docs/archive-record-discrepancies.md` row 7 SHALL gain a
  "carried to openXwallet" note; the four live-change references in
  `openspec/changes/add-wallet-carried-review-authority/tasks.md` SHALL be edited
  and an addendum SHALL record that task 2.6's red-proof is retargeted at the
  consumer gate and that S3/S5's core deltas are authored in openXwallet.
- **FR-019**: `governance/review-authority/` SHALL be untouched — all four files.
- **FR-020**: Ruleset 21538893 SHALL NOT be edited by this feature.

### Key Entities

- **`contracts/openxwallet-pin.yaml`** — the pin. `kind:
  pinned_contract_manifest`; the trusted referent is `commit` + the eight
  `sha256`s; `contract_bundle_tag` is a label beside them.
- **The `openXwallet` gitlink** — the bytes. Recorded gitlink and checked-out
  revision are compared separately.
- **`wallet-gate.log`** — the gate's captured output; the register conjunction is
  asserted against it.
- **`contract-v2.0`** — the MAJOR bundle whose release surface no longer contains
  the eight artifacts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `wallet-validation` check reports GREEN on this feature's own
  pull-request head, produced by the NEW workflow file, with ruleset 21538893
  unedited. That is the alias proof.
- **SC-002**: The gate log carries the `repo scan:` note and the `intake register
  read:` NOTE, and carries no `register-*` code and no
  `no intake register at this tree` line.
- **SC-003**: A deliberately malformed register row turns an openxFactory pull
  request RED with a `register-*` finding naming the full path (task 2.6's
  red-proof, retargeted).
- **SC-004**: `pytest-suite` reports GREEN with its pinned collected/passed/
  skipped triple under an initialized nested submodule.
- **SC-005**: `python3 scripts/verify-openxwallet-pin.py` exits 0, and each of
  the six refusal codes is reproducible.
- **SC-006**: `python3 scripts/validate-trust-anchor.py .` exits 0 and
  `tests/trust-anchor/` collects and passes.
- **SC-007**: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes.
- **SC-008**: `contracts/releases/contract-v2.0.digests.yaml` is byte-reproducible
  from the house build tool and the release inventory verify passes.
- **SC-009**: No `contracts/openxwallet/` path reference remains outside the pin
  file, the annotated records and the reworded citations.
- **SC-010**: `scripts/doc-health.py --single-repo .` reports no NEW findings.

## Assumptions

- `wallet-v1.1` = openXwallet commit `63f5a1adac89f017e70bab9a4ffe7cf02d6e6705`,
  verified through the tag object, and the eight digests at that tag equal the
  eight recorded in `contracts/manifest.yaml` today, verified byte for byte.
- The App behind `OPENXFACTORY_APP_ID` (App `4253636`, installation `145372182`)
  covers every repository in the `opensoft` organization
  (`repository_selection: all`), so no installation edit is needed to reach the
  private `opensoft/openXwallet`.
- `contract-v2.0` is the number at merge order; it is re-verified immediately
  before merge, along with the eight digests.
- Merge is an operator act and happens after P5a.2 lands. Tagging is an operator
  act. Neither is performed here.
