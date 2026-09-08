# Feature Specification: repository identity — `opensoft/codexFactory` becomes `codeXfactory/codexFactory` in governed content

**Feature Branch**: `030-realize-codexfactory-repository-identity`

**Created**: 2026-09-08

**Status**: Draft

**Input**: User description: "realize adopt-codexfactory-repository-identity groups 1-8: mapping row, recorded classification sweep, rename slices split by transfer-gating, origin-identity re-issuance packet, freeze verification, contract bundle cut, corpus bookkeeping"

**Lane**: `provenance-autonomous-merge`

## Context and authority

**THIS FEATURE IS A REALIZATION, NOT A PROPOSAL. It authors no requirement, adds
no spec delta, and settles nothing the ratified text left open.** Where the
ratified text is silent, this feature takes the most conservative reading
available and records it in [research.md](./research.md) as a stated assumption
with its source, rather than deciding it silently.

Its authority is ONE ratified OpenSpec change:

- **`adopt-codexfactory-repository-identity`** — RATIFIED 2026-09-07T22:21:44Z
  by Brett Heap (convener), verbatim *"accept all [A] and ratify 763"*, at
  ratified head `5bfdcf3c06478167bd7509f1576db3528ce4ede1`; record
  `openspec/changes/adopt-codexfactory-repository-identity/review/ratification-2026-09-07.md`.
  Merged as openxFactory PR **#763**, merge commit `eb30db7a`, 2026-09-08T03:38:07Z.
  Its `tasks.md` **groups 1–8** are this feature's build list, item for item;
  its `specs/repository-identity/spec.md` fixes the four ADDED requirements;
  its `design.md` § 2 fixes the path-class disposition rule, § 3 the two-arm
  freeze test, § 4.1 the cryptographic freeze, § 4.2 the sorted denominator,
  § 4.3 decisions **D-1** (respell, not re-mint) and **D-2** (the re-issuance is
  inside this change), and § 5 the bundle arithmetic.

Group **0** is discharged (ratification). Group **9** is **NOT PERFORMED** by
this feature and nothing below ticks it: it names the operator ceremony
(`~/session-prompts/runbook-codexfactory-org-transfer.md`) and the four
cross-repository follow-ons — `installs/hermes-install` (181/84), the
`opensoft/xFactory` aggregation lockstep (25/14), `opensoft/OpsxFactory` (16/13)
and codexFactory's own 532/211.

### The operator ceremony has NOT happened, and that is the load-bearing fact

The GitHub transfer is Brett's act and is unperformed at this feature's head.
**GitHub redirects OLD→NEW after a transfer and never NEW→OLD before it.** So
this feature does not treat "rename the 123 occurrences" as one act. Every
occurrence in the packet's RENAME classes is additionally classified on a second
axis:

- **(a) DECLARATIVE** — the string is content that is true of the estate's
  intent and resolves nothing at run time. Correct to land today.
- **(b) LIVE REFERENCE** — the string is resolved by a machine at run time (a
  workflow `repository:` checkout, a `gh api repos/<x>` call, a register the
  clearing validator compares a live sealed request against, a mapping row
  asserting a transfer date, a command an operator pastes into a terminal).
  Landing it today **breaks a live surface**, so it lands only in the transfer
  window at the runbook step named on its pull request.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — the recorded sweep, so the disposition is reviewable rather than enumerated (Priority: P1)

A reviewer or a later lane needs to know, at any commit, how many occurrences of
the former identity exist and which published class each falls in. The packet
replaced hand enumeration with a rule over path classes plus a recorded machine
sweep. This story produces that sweep at the realization head, closes the
arithmetic against the 2026-09-07 baseline, and classifies every occurrence that
appeared since by the published rule rather than by fresh judgment.

**Why this priority**: nothing else in the feature is reviewable without it. The
rename slices are defined BY the sweep's classes, and the freeze verification of
User Story 5 is a diff against the sweep's frozen set. It is also the only story
that is safe to land with zero dependency on any other.

**Independent Test**: run the recorded command at the feature head, compare the
per-class table to the evidence file, and confirm the totals in the evidence file
reproduce byte-for-byte.

**Acceptance Scenarios**:

1. **Given** the realization head, **When** `git grep -ic "opensoft/codexfactory" -- .` runs, **Then** the evidence file records the same total and the same per-class split, and each class's pathspec is recorded beside its count so the number is reproducible without the evidence file.
2. **Given** the 2026-09-07 baseline of 281/150 = 123/60 + 78/54 + 80/36, **When** the arithmetic is closed at the realization head, **Then** every occurrence of the drift is attributed to a named cause and classified under the published rule, and any occurrence that does not so classify is recorded as a finding BEFORE any rename lands.
3. **Given** the evidence file itself lives inside an active change packet, **When** the sweep is re-run after the evidence file lands, **Then** the self-referential growth is stated in the file rather than being discovered as an unexplained drift.

---

### User Story 2 — the declarative renames, landable before the transfer (Priority: P1)

The occurrences that assert what IS and resolve nothing at run time are
respelled now, so the corpus stops describing the estate's engineering domain at
an address the convener has ruled away. This is the regression denominator and
its pinning test, the three negative fixtures, the hermes-runtime README
enumeration, the omnigent and hermes-domain-overlay example fixtures, sixteen
live documents and `README.md`.

**Why this priority**: it is the largest slice that carries no transfer
dependency, and it is the slice the contract bundle cut of User Story 6 waits
on — all eight inventoried members of `contract-v3.4` that move are in this
slice.

**Independent Test**: the affected validators and pytest subsets run green on
the renamed tree with no workflow, no pin, no register and no operator runbook
touched, and `git grep` shows the (b) set byte-unchanged.

**Acceptance Scenarios**:

1. **Given** the regression denominator is bytewise sorted by repository, **When** the codex entry is respelled to `codeXfactory/codexFactory`, **Then** the entry is moved to the position derived from the tree at the realization head — not to a position copied from the packet — and `PINNED_TABLE` is respelled AND reordered in the same commit so the value-for-value comparison and the `sorted(..., key=lambda value: value.encode("utf-8"))` assertion both pass.
2. **Given** each negative fixture exists to produce exactly one finding, **When** its `repository:` is respelled, **Then** it still produces exactly that finding and no other, and the deliberate duplicate in `duplicate-repository.yaml` remains `opensoft/AdxFactory`.
3. **Given** `README.md` line 1172 and 1184 narrate a completed dated act, **When** the records-and-assertions test is applied PER LINE, **Then** the outcome for each of the nine `README.md` occurrences is recorded in the evidence, including which lines were frozen rather than swept.
4. **Given** no CI job supplies `--domain-repo`, **When** the resolver key migrates to `codeXfactory/codexFactory`, **Then** no openxFactory workflow needs to change with it and the migration is recorded as a consumer-visible note in the bundle changelog.

---

### User Story 3 — the live machine surfaces, prepared and held (Priority: P2)

The workflow checkouts, the decision-core pin, the re-pin lane's
`SOURCE_REPOSITORY`, and the two operator runbooks whose lines an operator pastes
are respelled in a prepared, reviewed pull request that is held in draft until the
transfer has happened. The change is authored now so the transfer window is spent
merging a reviewed diff rather than writing one.

**Why this priority**: it is the slice with the highest cost of landing early —
two required checks (`pytest-suite`, `merge-master-approval`) resolve
`opensoft/codexFactory` by `actions/checkout` today — and the highest cost of
landing late, because the same two checks break the moment the transfer
completes. Prepared-and-held is the only ordering that is safe in both
directions.

**Independent Test**: the pull request exists, is a draft, names its runbook step,
and its diff touches exactly the (b) machine-surface files and nothing else; the
pin tests are shown to be red-by-construction if the pin and its assertions were
split.

**Acceptance Scenarios**:

1. **Given** `contracts/review-lane-pin.yaml` is asserted by `tests/review_lane_pin/test_floor_snapshot.py` and `test_review_lane_caller.py` row for row, **When** the pin's `repository:` is respelled, **Then** both `PINNED_REPOSITORY` constants and `tests/review_lane_pin/test_repin_lane.py` move in the SAME commit.
2. **Given** `merge-master-approval.yml` carries operator diagnostics telling a human which repository to grant App access to, **When** the file is respelled, **Then** all twelve occurrences move together, because a half-respelled diagnostic sends a human to the wrong organization.
3. **Given** the pull request is a draft, **When** a reviewer reads its body, **Then** it names the exact runbook step at which it lands and states that it is not for merge without Brett's word.

---

### User Story 4 — the origin identity re-issued, on a human-only surface (Priority: P2)

`governance/factory-identity/` holds the estate's first origin identity, and the
repository name there is an authorization scope, not a label. The re-issuance
respells the register row, the wallet's `holder_id`, and the grant's audience and
single-element `objects` narrowing — with the clearing corpus and the tests that
assert the live register in the same commit — and the pull request carrying it
declares that it needs a human merge word.

**Why this priority**: it is the act the transfer makes mandatory rather than
optional. `scripts/validate-clearing-dispatch.py` compares a sealed request's
`origin.repository` against this register, so after the transfer codexFactory's
dispatches are refused until the row names the new identity. It is P2 rather than
P1 only because it cannot land before the transfer without performing that same
revocation in the wrong direction.

**Independent Test**: `scripts/validate-factory-identity.py` and
`scripts/validate-clearing-dispatch.py` run green on the re-issued tree, and a
diff shows no `key_id`, no multibase public half, no fingerprint, no
`holder_class` and no `expires_at` moved.

**Acceptance Scenarios**:

1. **Given** the register's reader refuses a concurrent active row for the same repository, **When** the row is re-issued, **Then** exactly ONE active origin row exists for the repository — the existing row respelled, not a second row.
2. **Given** the grant's own header forbids widening `objects`, **When** the grant is re-issued, **Then** `scope.objects` remains a single element naming only the current identity, and `expires_at` is unchanged.
3. **Given** `governance/factory-identity/` is entered by name in codexFactory's never-clearable floor, **When** the pull request is opened, **Then** its body states in bold that it requires Brett's human merge word and that no council verdict and no autonomous or council-cleared path may land it.
4. **Given** the disjointness rule in `scripts/validate-factory-identity.py` is over key material and not over holder strings, **When** the re-issuance lands, **Then** the validator reports no `factory-identity-tier-unattested` regression and no `FILL-IN-AT-MINT` sentinel.

---

### User Story 5 — the freeze, verified by diff (Priority: P1)

The 78 occurrences across 54 files that are frozen — 44 of them by cryptography
rather than by policy — and the occurrences that are deliberately NOT SWEPT are
proved byte-unchanged by a diff, not by inspection, and the signed-execution-chain
validator is recorded green as the evidence that no corpus-wide `sed` was run.

**Why this priority**: it is the check that would catch the single most damaging
mistake available in this feature. A well-meaning corpus-wide substitution breaks
34 self-verifying examples whose signing key's private half exists nowhere in the
repository, with no repair path.

**Independent Test**: `git diff` restricted to the frozen and not-swept pathspecs
is empty across the whole feature, and `scripts/validate-signed-execution-chain.py`
exits 0 with `ratification_signature_verifies` and `chain_identity_recomputes`
passing for all 34 files.

**Acceptance Scenarios**:

1. **Given** the frozen classes, **When** the diff of the whole feature is restricted to `contracts/signed-execution-chain/**`, `openspec/changes/archive/**`, `specs/**` (excluding this feature's own directory) and `docs/decisions/**`, **Then** it is empty.
2. **Given** the not-swept classes, **When** the diff is restricted to other lanes' active change packets and `ideation/**`, **Then** it is empty, because a diff touching another lane's unmerged packet is a lane collision and is reverted rather than merged.
3. **Given** a transfer moves the OWNER segment only, **When** the diff is searched for edits to a BARE `codexFactory` name, **Then** none is found — bare member names, `--aggregate-members` lists, dashboard groupings, directory names, submodule paths and the wallet, grant and attestation FILENAMES are correct before and after.

---

### User Story 6 — the bundle cut, so the release surface returns to zero findings (Priority: P3)

Eight members of the declared `contract-v3.4` digest inventory move in this
feature, none of them in the `EDITORIAL` set, so `release-inventory-drift`
reports eight `ERROR`-severity findings and `verify-commit` goes red the moment
the renames land. The cut re-baselines the inventory at the next additive minor
and returns the family to zero.

**Why this priority**: it is a consequence of User Story 2 rather than an
independent slice, and by the versioning policy it is allocated LATE — after the
final integration point is known — so it cannot be completed before the renames
land on `main`.

**Independent Test**: at the candidate commit, `verify-commit` is clean and
doc-health reports `release-inventory-drift` at 0 findings; before the cut the
same family reports exactly the eight expected members.

**Acceptance Scenarios**:

1. **Given** the renames have landed, **When** doc-health runs, **Then** `release-inventory-drift` reports exactly EIGHT `ERROR` findings, naming the eight inventoried members and no others — the transient the packet predicts, and the family working.
2. **Given** the versioning policy's Bundle Realization Order, **When** the minor is allocated, **Then** it is allocated after rebasing onto the final integration point and re-checking availability, and no number was reserved by this feature in advance.
3. **Given** an existing inventory is never hand-edited to make a comparison pass, **When** the release digests file is produced, **Then** it is built by `scripts/validate-contract-release.py build --tag <tag>`.

---

### Edge Cases

- **The mapping file does not exist.** `contracts/policies/repository-identity.yaml` is absent from `main`; the packet's task 1.1 forbids creating it here because `adopt-medxsoft-repository-identity` authors it at ITS task 1.1. That change is active and unrealized, and task 0.2's conditional covers only *archived or withdrawn*. The mapping row is therefore authored against a file this feature does not create, and is blocked until the exemplar's group 1 lands.
- **The transfer date is unknown.** The mapping row's `transferred_on` records a completed act. A row carrying a date before the act asserts a falsehood, so the row cannot be finished until the transfer has happened.
- **An occurrence appeared since the baseline that the published rule does not classify.** It is recorded as a finding in the evidence file before any rename lands, and no fresh judgment is substituted for the rule.
- **The packet's own file counts have drifted.** Task 3.8 says six clearing files; there are seven, because a fifth negative arrived with `admit-deliberation-clearing-operation`. The rule classifies it; the count is corrected in the evidence and the correction is recorded rather than silently absorbed.
- **A task's premise is false at the realization head.** Task 5.4 says the custody attestation names the repository; it names `codexFactory` bare only, with no owner segment, so its respell half is a no-op under task 6.4 and only its validator half runs.
- **A rename would make a live surface resolve the new identity before the transfer.** It is held in a draft pull request naming its runbook step. This is the whole reason the (a)/(b) axis exists.
- **A rename would revoke a live authorization.** Re-issuing the origin register before the transfer refuses today's sealed requests from `opensoft/codexFactory`. The re-issuance is (b) for that reason and not merely for tidiness.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The feature MUST produce a recorded classification sweep at its own head, filed as `openspec/changes/adopt-codexfactory-repository-identity/evidence/codexfactory-identity-sweep-2026-09-08.md`, carrying the reproducing command, the per-class pathspec and count, the closed arithmetic against the 2026-09-07 baseline, and every drift attributed to a named cause. *(packet 2.1, 2.2, 2.3)*
- **FR-002**: The feature MUST classify every RENAME-class occurrence on a second axis — declarative (landable now) or live reference (landable only in the transfer window) — and MUST record the classification and its evidence per file, so a reviewer can check the tree rather than a list. *(the transfer is unperformed; packet `specs/repository-identity/spec.md:90`)*
- **FR-003**: The feature MUST land the declarative renames as ordinary pull requests and MUST prepare the live-reference renames as DRAFT pull requests, each naming the exact runbook step at which it lands. *(packet 3.5–3.7, 3.12, 4.5, group 5)*
- **FR-004**: The feature MUST keep every fixture in the same commit as the artifact that pins it — the regression denominator with `PINNED_TABLE`, the decision-core pin with both `PINNED_REPOSITORY` constants and the re-pin lane test, and the origin register with the clearing tests that assert it live. *(packet 3.1, 3.5, 5.5; design § 3)*
- **FR-005**: The feature MUST derive the regression denominator's new sorted position from the tree at its own head, and MUST NOT copy a position from the packet. *(packet 3.1; design § 4.2)*
- **FR-006**: The feature MUST re-issue the origin identity as a RESPELL of the existing register row, wallet and grant — one row, one wallet, one grant, `objects` unwidened, `expires_at` unextended, no key re-minted, no `key_id`, multibase public half, fingerprint or `holder_class` touched. *(design § 4.3 D-1)*
- **FR-007**: The pull request carrying `governance/factory-identity/` MUST declare, in bold in its body, that it requires Brett Heap's human merge word, that no council verdict and no autonomous or council-cleared approval path may land it, and that the directory is entered by name in codexFactory's never-clearable floor. *(design § 4.3; runbook 10.3)*
- **FR-008**: The feature MUST prove the freeze by diff over the frozen and not-swept pathspecs and MUST record `scripts/validate-signed-execution-chain.py` green with `ratification_signature_verifies` and `chain_identity_recomputes` passing for all 34 files. *(packet 6.1, 6.2, 6.3)*
- **FR-009**: The feature MUST confirm no BARE `codexFactory` name was edited anywhere, including wallet, grant and attestation filenames. *(packet 6.4)*
- **FR-010**: The feature MUST prepare the mapping row against `contracts/policies/repository-identity.yaml` — carrying `former`, `current`, `transferred_on`, the redirect-lapse note, the case-sensitivity divergence, the GHCR lowercasing (OQ-6, ruled 2026-09-08T03:51Z), and the three reference shapes the redirect does not cover — WITHOUT creating that file, and MUST record the dependency on `adopt-medxsoft-repository-identity` task 1.1. *(packet 1.1–1.4)*
- **FR-011**: The feature MUST prepare, and MUST NOT complete, the contract bundle cut: the eight moved inventoried members are named, the transient of eight `ERROR` findings is recorded as predicted-and-observed, and the minor is allocated only after the renames reach the final integration point. *(packet 7.1–7.5; design § 5)*
- **FR-012**: The feature MUST run `OPENSPEC_TELEMETRY=0 openspec validate adopt-codexfactory-repository-identity --strict` and `--all --strict` and record the result, expecting one pre-existing failure — `disposition-codexfactory-declared-renames`, a deltaless packet about declared SCENARIO retitles, unrelated to repository renames and neither caused nor repaired here. *(packet 8.2)*
- **FR-013**: The feature MUST run `python3 scripts/validate-sequenced-after.py . --ledger-diff` and record it green with this change resolving `adopt-medxsoft-repository-identity` and introducing no cycle. *(packet 8.3)*
- **FR-014**: The feature MUST NOT perform any group 9 act: no transfer, no remote repoint, no `.gitmodules` edit, no visibility flip, no GHCR publish or prefix flip, no SonarCloud act, no aggregation lockstep commit, no `installs/hermes-install` sweep, no OpsxFactory plan amendment, and no codexFactory-side rename. *(packet group 9; runbook ownership legend)*
- **FR-015**: The feature MUST NOT tick a packet task whose completion requires a merge to `main`, because this feature merges nothing; each such task MUST instead be recorded against the pull request that will tick it.

### Key Entities

- **Occurrence** — one literal, case-insensitive match of `opensoft/codexfactory` at a path and line. Carries a PATH CLASS (from design § 2) and, if it is in a RENAME class, a GATING CLASS: declarative or live reference.
- **Path class** — one row of the design § 2 disposition table: a pathspec, a count, and one of RENAME, FROZEN or NOT SWEPT.
- **Gating class** — the second axis this feature adds: `safe-now` or `gated:<runbook step>`.
- **Mapping row** — one entry of `transfers:` in `contracts/policies/repository-identity.yaml`: `former`, `current`, `transferred_on`, `redirect`, plus this change's case-sensitivity, GHCR-lowercasing and uncovered-reference-shape notes.
- **Origin identity record set** — the register row, the wallet, the grant and the custody attestation under `governance/factory-identity/`, read together by `scripts/validate-factory-identity.py` and consumed by `scripts/validate-clearing-dispatch.py`.
- **Inventoried member** — a file that appears in the declared `contract-v3.4` digest inventory; eight of them move here, none in the `EDITORIAL` set.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The sweep's arithmetic closes at the feature head with every class accounted for and every drift attributed, and the total is reproducible from the recorded command by a reader who never opens the evidence file.
- **SC-002**: All 60 RENAME-class files are assigned a gating class, and the two subtotals sum to the RENAME subtotal in both hits and files.
- **SC-003**: The frozen set of 78 occurrences across 54 files is byte-unchanged across every pull request this feature opens, verified by an empty diff and not by inspection.
- **SC-004**: The not-swept set is byte-unchanged, so no other lane's unmerged packet is touched and no lane collision is created.
- **SC-005**: No live surface resolves `codeXfactory/codexFactory` before the transfer: every pull request whose diff contains a run-time-resolved reference is a draft naming its runbook step.
- **SC-006**: After the transfer window's pull requests land, zero live occurrences of `opensoft/codexFactory` remain outside the frozen and not-swept sets.
- **SC-007**: The origin re-issuance leaves exactly one active origin row, an unwidened single-element `objects`, and no moved key material — provable by diff.
- **SC-008**: The pull requests this feature opens are reviewable independently: the safe-now rename pull request's checks are green, and each draft's diff is confined to its own gating class.
- **SC-009**: Every packet task this feature could not complete is named, with the reason and the act that would complete it, so the next lane resumes from the ledger rather than from the tree.

## Assumptions

- **The transfer is unperformed and its date is unknown.** Every judgment about landing order follows from this; if the transfer happens mid-feature, the draft pull requests become mergeable and nothing else changes.
- **`adopt-medxsoft-repository-identity` still authors the mapping file.** It is active on `main` and unrealized; task 0.2's premise therefore holds, and this feature adds a row rather than authoring a file. If the convener instead rules that this feature authors the file, only the mapping-row slice changes.
- **`disposition-codexfactory-declared-renames` is unrelated to this feature** despite the name. It disposes of OpenSpec CLI 1.12.0 scenario-currency findings over declared scenario RETITLES in codexFactory changes; it is deltaless, which is why it fails `--all --strict`. This feature neither causes nor repairs it, and the expected `--all` result stays `N passed / 1 failed`.
- **No CI job supplies `--domain-repo`**, measured at the feature head, so the resolver-key migration is a consumer-visible note rather than a workflow edit.
- **`governance/factory-identity/` exists only in openxFactory.** codexFactory's `origin/main` has no such tree, which is design § 4.3's own reason D-2(a); the human-only pull request is therefore an openxFactory pull request.
- **The bundle cut cannot complete in this feature** because the minor is allocated after the final integration point and this lane merges nothing. Group 7 is prepared and recorded, not performed.
- **`scripts/sync-notebooklm-books.py --apply` writes to a live external service** and is scheduled for after the doc changes land; it is recorded as owed rather than run against unmerged work.
