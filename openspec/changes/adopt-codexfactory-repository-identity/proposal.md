---
code_surface: >-
  openxFactory (RENAME at realization, `opensoft/codexFactory` ->
  `codeXfactory/codexFactory`: 123 occurrences across 60 files, measured at
  origin/main `64aad02e` on 2026-09-07 and enumerated by PATH CLASS rather than
  by occurrence, because at this size a hand list is a liability — see
  `design.md` § 2. The classes: `contracts/**` excluding
  `contracts/signed-execution-chain/**` (30 across 23 — the supported-domain
  regression inventory fixture and its three negative fixtures,
  `contracts/hermes-runtime/README.md`, the review-lane decision-core pin
  `contracts/review-lane-pin.yaml` and `contracts/review-lane-repin-binding.template.yaml`,
  six clearing examples, six omnigent manifest fixtures, two hermes-domain-overlay
  examples, and the clearing factory-identity fixture register); `tests/**` (23
  across 8 — `tests/hermes_runtime_contracts/test_domain_regression.py`
  `PINNED_TABLE` respelled AND REORDERED, `tests/factory_identity/test_validator.py`,
  `tests/clearing/test_origin_signature.py` and `test_attestation.py`,
  `tests/review_lane_pin/` three files, `tests/factory_identity/test_mint_script.py`);
  `.github/**` (16 across 4 — `workflows/merge-master-approval.yml` twelve,
  `workflows/review-lane-repin.yml` two, `workflows/pytest-suite.yml` one,
  `merge-approval-envelope.yml` one); `governance/factory-identity/**` (6 across
  3 — `register.yaml`, `grants/grant-origin-codexfactory-0001.yaml`,
  `wallets/wal-origin-codexfactory-0001.yaml`, all on a PERMANENTLY HUMAN-ONLY
  surface); `scripts/**` (5 across 3 — `mint-factory-origin-key.py` `TARGET_REPO`,
  `review_lane_repin.py` `SOURCE_REPOSITORY`, `doc_health/pin_class.py`);
  `docs/**` excluding `docs/decisions/**` (35 across 18); and `README.md` (8).
  ADD the codexFactory row to `contracts/policies/repository-identity.yaml`,
  which this change does NOT author — `adopt-medxsoft-repository-identity`
  authors it at its task 1.1 and this packet declares `sequenced_after` on it.
  RE-ISSUE the factory-origin identity records so the origin grant's holder and
  object narrowing name the current identity. NO change to any schema, field
  name, `$id`, `contract_id`, `contract_schema_version`, digest-identity rule,
  validator behaviour, check family or check-family numeral; no file is renamed
  or moved; no domain repository's `stack.yaml` is touched; NO Ed25519 key is
  re-minted; and NOT ONE BYTE of the 78 occurrences across 54 files listed under
  § What this deliberately does not change, nor of the 80 across 36 files left
  to their owning lanes.
target_release: >-
  next additive contract bundle (allocated at realization per
  `docs/contract-versioning-policy.md` § Bundle Realization Order; NO minor is
  reserved here, the policy forbidding a proposal to reserve one before merge
  order is known). A BUNDLE IS OWED AND THE REASON IS MEASURED: EIGHT of the 60
  renamed files are members of the declared `contract-v3.4` digest inventory
  (283 entries) — `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`,
  its three negative fixtures under `fixtures/regression/`,
  `contracts/hermes-runtime/README.md`, `docs/contract-versioning-policy.md`,
  `docs/terminology-and-repo-topology.md` and
  `docs/xfactory-domain-factory-model.md`. The ROOT `README.md` is NOT a member
  (only `contracts/README.md` and `contracts/hermes-runtime/README.md` are,
  which a substring search conflates), so the proposing commit's OpenSpec
  Records entry moves no inventoried blob. NONE of the eight is in `scripts/doc_health/release_inventory.py`'s
  three-path `EDITORIAL` set, so each moved blob is an `ERROR`-severity
  `release-inventory-drift` finding and a red `verify-commit` on a non-editorial
  member until the cut re-baselines the inventory. The change class is ADDITIVE
  (minor): a repository's OWNER segment moves, no shape moves, and every pinned
  consumer of `contract-v3.4` keeps resolving byte-identically because a
  published bundle is never rewritten.
sequenced_after: [adopt-medxsoft-repository-identity]
Status: ratified
Proposed: 2026-09-07
Ratified: >-
  2026-09-07, Brett Heap (convener), verbatim "accept all [A] and ratify 763",
  posted 2026-09-07T22:21:44Z on openxFactory PR #763
  (https://github.com/opensoft/openxFactory/pull/763#issuecomment-5576174434);
  ratified head `5bfdcf3c06478167bd7509f1576db3528ce4ede1`; record
  `review/ratification-2026-09-07.md`. The same word rules OQ-3 via the
  ideation-split decision sheet's four dispositions (see the record's ledger);
  OQ-4 and OQ-6 remain open and are not answered by this ratification.
Origin: >-
  Convener ruling, Brett Heap, 2026-09-07, verbatim "move codeXfactory to the
  new org. openXfactory should be public and codeXfactory private." The GitHub
  organization `codeXfactory` exists and is empty; nothing has been transferred.
  Unlike the exemplar this packet follows, the operational half has NOT happened
  and is not governed here: it is an operator ceremony with its own runbook
  (`~/session-prompts/runbook-codexfactory-org-transfer.md`) and its own tracking
  issue, recorded rather than performed. This packet exists for the half that
  OpenSpec owns — repository identity inside governed contract content — and for
  the sequencing constraints the ceremony must respect.
---

# Proposal: adopt-codexfactory-repository-identity

## Why

**A governed repository is about to move organizations, and openxFactory's
contract content names it at its current address 281 times.** On 2026-09-07 the
convener ruled that `opensoft/codexFactory` moves to the `codeXfactory`
organization and stays private, and that `openxFactory` becomes public. The
operational half — remotes, `.gitmodules`, the aggregation's lockstep pins,
GitHub App installations, secrets, container namespaces, SonarCloud — is an
operator ceremony and is not governed here.

The half that OpenSpec owns is not operational. `opensoft/codexFactory` is a
**normative value** in openxFactory, and in more roles than the exemplar faced:

| where | what it is |
| --- | --- |
| `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml:37` | the canonical repository key of one of five entries in the supported-domain regression DENOMINATOR that gates every bundle publication — currently the LAST entry in a bytewise-sorted list |
| `fixtures/regression/{digest-mismatch,duplicate-repository,missing-exclusion-reason}.yaml` | the same key inside three negative fixtures that prove the denominator's failure modes |
| `contracts/review-lane-pin.yaml:47` | `repository:` of the DECISION CORE — the repository openxFactory checks out at an exact commit to obtain its Merge Master decision |
| `governance/factory-identity/register.yaml:146`, `grants/grant-origin-codexfactory-0001.yaml`, `wallets/wal-origin-codexfactory-0001.yaml` | the ORIGIN IDENTITY of the estate's first originating repository: `holder_ref`, `holder_id`, and the grant's single-element `objects:` narrowing. This identity is an AUTHORIZATION SCOPE, not a label |
| `.github/workflows/merge-master-approval.yml` (12) | the decision-core checkout, the App-installation diagnostics, and two summary tables |
| `.github/workflows/review-lane-repin.yml`, `scripts/review_lane_repin.py:62` | `SOURCE_REPOSITORY` of the re-pin lane |
| `contracts/clearing/examples/**` (6 files) | `verified_subject_pin`, `observed_repositories`, and the widening finding's `subject:` in the single-door attestation corpus |
| `contracts/omnigent/examples/fixtures/**` (6 files) | `repository:` of a domain overlay in six manifest fixtures |
| `tests/**` (8 files, 23 occurrences) | `PINNED_TABLE`, `PINNED_REPOSITORY`, the live-register assertions in `tests/clearing/test_origin_signature.py`, and the validator's default holder |
| eighteen live governance documents plus `README.md` | the repository named as the engineering domain's canonical home, the decision core, and the mint target |

**The redirect is a grace period, not an identity.** GitHub redirects the old
owner and stops the moment `opensoft` reuses the name — and `opensoft` will
still exist, still be actively used, and still hold the aggregation repository
that names `codexFactory` in eight workflows. Governed content whose
correctness depends on nobody creating a repository is not content a contract
may rest on. **Two of this estate's surfaces do not even get the grace period**:
a cross-organization `uses:` reference to a reusable workflow in a PRIVATE
repository is not covered by any redirect and is an outright break (OQ-1), and a
`ghcr.io/<org>/...` package namespace is per-organization and does not redirect
at all (OQ-4).

**And 78 of the 281 occurrences MUST NOT be touched — 44 of them for a reason
the exemplar never met.** `contracts/signed-execution-chain/examples/` contains
34 files whose `out_of_pipeline.ground_ref` names `opensoft/codexFactory`
INSIDE the `signed_ratification` block. That block is covered by an ed25519
`ratification_signature` and is the subject of `chain_identity`, an
`xfc-jcs-sha256-1` digest over its canonical bytes, both recomputed and verified
by `scripts/validate-signed-execution-chain.py`. The corpus header states that
**the fixture key's private half exists nowhere in this repository.** Respelling
one character there does not merely falsify a record — it makes 34 self-verifying
positive and negative examples fail with `ratification_signature_invalid` and
`chain_identity_recomputes`, and **there is no key with which to re-sign them.**
The freeze is not a policy choice on that arm; it is arithmetic.

## The precedent this follows, cited

`adopt-medxsoft-repository-identity` (authored 2026-08-27, `Status: draft`,
still active on `main`) is the controlling exemplar, itself following
`adopt-subject-tenant-domain-vocabulary` (archived 2026-07-23). This packet
mirrors it deliberately:

- It renames the LIVE normative surfaces and FREEZES the recorded spellings,
  arbitrating per occurrence with one question: *does this string assert what
  IS, or record what WAS READ?*
- It publishes `contracts/policies/repository-identity.yaml` so a frozen former
  spelling stays machine-interpretable rather than merely stale.
- It states that a transfer moves the OWNER segment only, so bare names,
  commits, repository-relative paths and blob digests are untouched.

**This packet does NOT re-author that policy file.** The file does not exist on
`main`; the exemplar authors it at its task 1.1 and registers it in
`contracts/manifest.yaml` at task 1.3. Authoring it twice would produce two
files claiming to be the mapping. This change therefore declares
`sequenced_after: [adopt-medxsoft-repository-identity]` and ADDS the
codexFactory row to the mapping the exemplar creates. The dependency is not
bookkeeping — it is load-bearing twice over, and § 4 of `design.md` shows why.

## Where the precedent does not reach, and what replaces it

Three things are genuinely new here, and each is why this packet adds
requirements rather than merely re-running the exemplar.

1. **Enumeration does not scale.** The exemplar listed all thirty occurrences by
   file and line. At 281 across 150 a hand list is stale before review ends and
   invites a reviewer to check the list instead of the tree. This change
   declares the disposition as a RULE OVER PATH CLASSES and commits to a
   RECORDED MACHINE SWEEP whose output is the evidence.
2. **A former identity can be frozen by cryptography rather than by policy.**
   The exemplar's freeze protected records from being falsified. Here 34 files
   additionally CANNOT be respelled, because the bytes are signature-covered and
   the signing key is absent by design.
3. **A repository identity can BE an authorization scope.** The origin grant's
   `objects:` list is exactly `[opensoft/codexFactory]`, and its own header
   forbids widening it. After the transfer that grant evidences origination for
   an identity that no longer exists, and `scripts/validate-clearing-dispatch.py`
   compares a sealed request's `origin.repository` against the register. The
   transfer therefore REVOKES the clearing lane for codexFactory until the
   identity records are re-issued — and that surface is declared PERMANENTLY
   HUMAN-ONLY, so no council verdict and no autonomous merge path may perform
   the re-issuance.

## What Changes

- **Add four requirements to the `repository-identity` capability** (ADDED only,
  no MODIFIED block against any promoted capability; the capability itself is
  created by the exemplar): cryptographic freeze; identity-as-authorization-scope
  re-issuance; disposition-by-rule-plus-recorded-sweep; and cross-organization
  reachability of a governed reference.
- **Add the codexFactory row** to `contracts/policies/repository-identity.yaml`
  — `former: opensoft/codexFactory`, `current: codeXfactory/codexFactory`,
  `transferred_on`, and the redirect note — beside the exemplar's two rows.
- **Rename the 123 live occurrences across 60 files**, at realization and not in
  this proposal, class by class, with the fixture-and-its-pin pairs committed
  together.
- **Re-issue the factory-origin identity records** so the register row, the
  wallet and the grant name the current identity, WITHOUT re-minting the key:
  the transfer moves the owner segment, and neither the key material, its
  custody, nor its fingerprint moves with it.
- **Re-cut the contract bundle**, because eight renamed files are members of the
  declared `contract-v3.4` digest inventory. Allocated late per the versioning
  policy.
- **Record, and do not perform, the operational ceremony**: the transfer, the
  visibility flips, the aggregation lockstep, the App installations, the
  container namespaces and SonarCloud all live in the operator runbook.

## What this deliberately does not change

**78 occurrences across 54 files keep their recorded spelling** and are read
through the mapping:

- **`contracts/signed-execution-chain/examples/**` — 44 across 34.** Frozen by
  construction, not by policy. See § Why. This is also why NO occurrence in that
  tree is counted toward the release-surface arithmetic: nothing there moves.
- **`openspec/changes/archive/**` — 15 across 10.** An archived packet is
  immutable. This is the rule `supersede-lost-pin-baseline` refused to break for
  a pin nobody could resolve, and it is not broken here for a name that still
  resolves.
- **`specs/**` — 18 across 9.** Dated Speckit plans and point-in-time
  verification tables (`specs/025-openxfactory-review-lane-caller/`,
  `specs/029-admit-deliberation-realization/`,
  `specs/011-council-feature-clearance/`, and three
  `specs/005-customer-subject-runtime/` tables carrying commit SHAs and stack
  digests). Rewriting the repository column would state that a verification ran
  against an address that did not exist when it ran.
- **`docs/decisions/0002-xfactory-aggregation-repo.md:88`.** A dated decision
  record stating the clone URL as it was decided.

**A further 80 occurrences across 36 files are NOT SWEPT BY THIS CHANGE**, which
is a different disposition from freezing and is stated separately because
conflating the two would be dishonest:

- **Other lanes' in-flight change packets — 74 across 32.** Editing another
  lane's unmerged `proposal.md`, `design.md`, `tasks.md` or ratification record
  is a lane-collision, and a ratification record is a dated record besides. Each
  owning lane respells its own packet at its next touch, or the packet archives
  carrying the former spelling and is frozen there. The mapping resolves it
  either way. **This is a deliberate departure from a corpus-wide sweep and is
  recorded as such**, because a sweep that reaches into 32 unmerged packets
  would be a merge conflict machine and a protocol breach.
- **`ideation/**` — 6 across 4.** Brainstorm and staging fragments are
  pre-governance free-form input; the lifecycle explicitly permits contradiction
  there. They are not normative surfaces and are not corrected.

Also unchanged: no schema, no field name, no `$id` or `contract_id`, no
`contract_schema_version`, no digest-identity rule, no validator behaviour, no
check family and no family numeral. No file is renamed or moved. No domain
repository's `stack.yaml` is touched. **No Ed25519 key is re-minted** and no
`FILL-IN-AT-MINT` sentinel is reintroduced.

## Capabilities

### Modified Capabilities

- `repository-identity`: four ADDED requirements. The capability is CREATED by
  `adopt-medxsoft-repository-identity`; this change extends it and is sequenced
  after it.

## Impact

- **Affected specs:** `repository-identity` (ADDED requirements only). No
  MODIFIED block against any promoted capability. `release-surface-integrity`,
  `repo-boundary-governance`, `signed-execution-chain`, `factory-origin-identity`
  and `workflow-gate-contract` are CITED rather than restated or widened.
- **Affected contracts:** `contracts/policies/repository-identity.yaml` (one row
  added to a file this change does not create), `contracts/review-lane-pin.yaml`,
  `contracts/review-lane-repin-binding.template.yaml`, the hermes-runtime
  regression fixtures, the clearing examples, the omnigent manifest fixtures, the
  hermes-domain-overlay examples, `contracts/manifest.yaml`,
  `contracts/CHANGELOG.md`, and a new `contracts/releases/<bundle-tag>.digests.yaml`
  at the cut.
- **Affected governance records:** `governance/factory-identity/register.yaml`,
  `wallets/wal-origin-codexfactory-0001.yaml`,
  `grants/grant-origin-codexfactory-0001.yaml`, and the custody attestation
  beside them. **This surface is permanently human-only**, so the pull request
  that carries it cannot be cleared by any autonomous or council path.
- **Affected workflows and scripts:** `.github/workflows/merge-master-approval.yml`,
  `review-lane-repin.yml`, `pytest-suite.yml`, `.github/merge-approval-envelope.yml`,
  `scripts/review_lane_repin.py`, `scripts/mint-factory-origin-key.py`,
  `scripts/doc_health/pin_class.py`.
- **Affected tests:** eight files, and two of them pin an ORDER as well as a
  spelling — see `design.md` § 4.
- **Affected docs:** eighteen live documents plus `README.md` (prose, the
  OpenSpec Records block and the doc index).
- **Predicted check movement:** `release-inventory-drift` gains EIGHT
  `ERROR`-severity findings the moment the renames land and returns to zero at
  the cut; that transient is why the cut is sequenced inside this change.
  `openspec validate --all --strict` moves from 97 passed / 1 failed to 98
  passed / 1 failed — the one pre-existing failure being
  `disposition-codexfactory-declared-renames`, a deltaless disposition packet
  unrelated to this change and not repaired by it.
- **Operational rewiring: NOT YET DONE, AND NOT GOVERNED HERE.** The transfer,
  the two visibility flips, the aggregation's lockstep commit, the App
  installations, the environment and secret inventory, the container namespace
  move and the SonarCloud rebind are an operator ceremony, ordered in
  `~/session-prompts/runbook-codexfactory-org-transfer.md` and tracked on the
  codexFactory tracking issue. This proposal neither performs nor blesses that
  work; it states the constraints the governed half places on its ORDER.

### Cross-repository follow-ons, named and out of scope

- **`installs/hermes-install` — 181 occurrences across 84 files**, concentrated
  in `tests/unit/test_subject_pin_guard.py` (36) and
  `config/clients/opensoft/overlay.yaml` (5). That repository consumes
  openxFactory BY PIN and is unaffected until its pin bump. **This is a
  correction to the exemplar's disposition, not a copy of it**: the exemplar
  named hermes-install as an un-performed follow-on for ONE negative fixture. At
  181 occurrences, including a live client overlay and a guard suite, deferring
  to "the next pin bump" would leave a live install naming a dead identity for
  an unbounded period. The runbook schedules it as a step of the ceremony with
  its own test-count proof, and the tracking issue carries it.
- **`opensoft/xFactory` (aggregation) — 25 across 14.** The `.gitmodules` URL,
  the gitlink, the review-lane `uses:` path, the two `MIGRATION_PIN` checkouts
  and their two pin tests are a LOCKSTEP that must move in ONE commit; eight
  further `uses:` paths point at `@main`. No aggregation-level OpenSpec act is
  owed, but the lockstep is a hard ordering constraint on the ceremony.
- **`opensoft/OpsxFactory` — 16 across 13**, including the MCP contract-service
  hosting plan. That plan's task 4.2 is **APPROVED by digest** (Brett Heap,
  `2026-09-05T23:06Z`, *"approve 4.2, merge #221"*, digest `4e1a4b76…`), so the
  move's amendment **revokes the approval and owes a re-approval** under the
  plan's requirement 2. The ordering that spends exactly one re-approval and no
  second acceptance is in `design.md` § 7.2.1.
- **`opensoft/codexFactory` itself — 532 across 211.** Its own governed content
  is its own act, in its own repository, and is not authored here.

## Open questions

Six were opened with this packet; **FOUR ARE NOW RULED** — OQ-1, OQ-2 and OQ-5
the same day this packet was authored, and OQ-3 by the ratification of
2026-09-07 (`review/ratification-2026-09-07.md`) — and are kept at their
numbers with the ruling recorded, so the record shows what was asked as well
as what was answered. **OQ-4 and OQ-6 remain open and owe a convener word.**
Full text in `design.md` § 8 (unchanged by this ratification; the OQ-3 entry
below and `review/ratification-2026-09-07.md`'s ledger are the current record).

- **OQ-1 — RULED, 2026-09-07, Brett Heap (convener).** *Add the `codeXfactory`
  organization to the Opensoft GitHub Enterprise*, so codexFactory's reusable
  workflows stay callable cross-organization at access level `enterprise` while
  the repository stays private. The alternatives — vendoring the reusable
  workflows into the aggregation (which would break the three-site lockstep
  invariant) and making codexFactory public (which the same ruling forbids) —
  are recorded as NOT TAKEN rather than foreclosed. **The enterprise-owner act
  is Brett's**, it is the FIRST operator step of the ceremony, and it is a
  precondition of the transfer rather than a follow-on: the runbook opens by
  verifying `gh api orgs/codeXfactory --jq .plan.name` reads `enterprise`.
- **OQ-2 — RULED, 2026-09-07, Brett Heap (convener).** *Apache-2.0*, for BOTH
  `openxFactory` and `openXwallet`. **The LICENSE files are added by a separate
  lane's pull request and are NOT part of this change's code surface.** What
  this packet records is the consequence for ORDER: `LICENSE` present at the
  repository root is a PRECONDITION of the openxFactory public flip, not a
  cleanup after it, because a repository published without a licence is
  published under no grant at all and the first clone is the one that cannot be
  taken back.
- **OQ-3 — RULED, 2026-09-07, Brett Heap (convener), via the ideation-split
  decision sheet** (`~/session-prompts/ideation-split-decision-2026-09-07.md`,
  "accept all [A]", 2026-09-07T22:21Z; ledger in
  `review/ratification-2026-09-07.md`). *Accept publication of `ideation/`
  (326 files), `governance/`, `health/`, `experiments/`, `.claude/`, `.codex/`
  and `.specify/` with openxFactory — GATED on four moves landing first:* Q1
  redact the two sensitive files (real addresses) to role placeholders; Q2
  editorially split `staging/treatment-options-engine/treatment-options-engine.md`
  — the neutral remainder stays here, the clinical half moves to
  MedxSoft/MedxFactory `ideation/staging/treatment-plan-generation/`; Q3
  delete `staging/campaign-memory-fill-maintenance-mapping/campaign-marketing.md`
  as stale scaffolding; Q4 three receiving pull requests (codexFactory 14
  files, MedxFactory 9, LedgerxFactory 1) plus one openxFactory removal pull
  request, with the cross-reference bootstrap re-run and the README/INDEX
  pointers updated. The mirror alternative (excluding those trees behind a
  private fork) is recorded as NOT TAKEN.
- **OQ-4 — OPEN.** When does the `ghcr.io` namespace move, relative to the
  bench-image allowlist flip and to the MCP contract-service hosting plan's
  **live, digest-bound approval** — which the move's amendment revokes and which
  then owes a re-approval? (Shaped by two lanes' measured constraints — see
  `design.md` § 7.)
- **OQ-5 — RULED, 2026-09-07, Brett Heap (convener).** **EXERCISE the
  `MIGRATION_PIN` re-point ceremony as part of the move — do NOT ride GitHub's
  redirect.** The recommendation is adopted as given, and the alternative (leave
  the pin on the `opensoft` URL under the redirect for a bounded period) is
  recorded as NOT TAKEN rather than foreclosed. The ceremony's shape is the one
  codexFactory `add-regular-pr-council-clearance` task **5.1** performed and
  recorded — `[xFactory][OPERATOR] Re-point ceremony … performed on the record,
  with the prior SHA recorded as the rollback target` — gated on **2.19** (the
  golden characterization suite re-proved green, nightly decisions byte-identical
  pre and post), **3.3** (the vendored aggregation envelope fixture re-validates
  unchanged against the schema and the hand-rolled mirror, matching the same pull
  requests), and **4.16** (the nightly lane re-proved green end to end on a live
  run), with **5.2** confirming the live decisions still match the golden
  baseline afterwards. **This is a RE-RUN of a discharged ceremony, not a
  re-opening of it**: rows 5.1 and 5.2 are ticked for the generalized-core
  re-point, and the org move is a second exercise of the same recorded shape
  against a new pinned ref. Ordering consequence: the ceremony's three gates run
  INSIDE the transfer window rather than at leisure, which is the cost the
  ruling accepts.
- **OQ-6 — OPEN.** Is the canonical owner segment spelled `codeXfactory` (capital
  X), and is the GHCR lowercasing consequence accepted and recorded in the
  mapping? (Recommended: yes to both.)
