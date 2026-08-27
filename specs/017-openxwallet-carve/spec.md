# Feature Specification: P2 — carve and scaffold `opensoft/openXwallet`

**Feature Branch**: `017-openxwallet-carve`

**Created**: 2026-08-26

**Status**: Draft

**Input**: User description: "P2 of split-openxwallet-repo: carve opensoft/openXwallet from openxFactory over the twelve ratified path sets with full history, scaffold it as a governed repo, prove byte-identity against the named carve commit, bootstrap its ruleset, tag wallet-v1.0 — realizes tasks.md group 3."

**Realizes**: `openspec/changes/split-openxwallet-repo` group 3 (tasks 3.1–3.31),
ratified 2026-08-26 by Brett Heap, merged to `main` at `5ef6d8d2` (PR #391).
The ratified proposal, design (D7, D8, D12–D14), clarifications (N1, N3, N8) and
the LOCKED rulings R1–R8 are this feature's binding inputs; nothing here reopens
them.

**Scope boundary**: P2 only. `wallet-v1.1` (P2b), the openxFactory deprecating
minor (P2.5), the consume-and-shed (P3) and everything after are named
successors, explicitly out of scope. **openxFactory sheds nothing in P2.**

## Clarifications

### Session 2026-08-26

No critical ambiguity was found in this specification: the ratified change decided
every open question before the feature existed. Three points of FACT about the
current openxFactory tree diverged from what the ratified design and the launching
brief assumed, and each was resolved without blocking. Full record:
[`clarify-questions.md`](./clarify-questions.md).

- Q: openxFactory's manifest row for `contracts/schemas/hermes-job-envelope.schema.yaml` carries no `sha256` — so what digest does the CONSUMED row carry? → A: the digest COMPUTED over the vendored bytes at the named carve commit, with the absence of a recorded upstream digest noted on the row (the artifact is content-addressed by commit from `opensoft/Omnigent-Install`).
- Q: openxFactory's own row names `adapter_owner: Omnigent-Install`, not `openxFactory` — which wins? → A: the ratified `adapter_owner: openxFactory`, with the two-hop upstream chain carried as a comment and as `source_path`.
- Q: does the new ruleset require one token or two? → A: both `wallet-validation` and `pytest-suite`, mirroring ruleset 21538893's actual current shape and satisfying task 3.27's named minimum.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The wallet standard exists as its own governed product (Priority: P1)

A neutral-product consumer — today LedgerxFactory, tomorrow any domain
descendant — needs the wallet standard (its two contract families, its corpus,
its validator, its syntax gate) to live in a repository that publishes it as a
product, rather than as a subdirectory of the factory-layer repository that also
happens to be one of its consumers. P2 delivers that repository with the full
path history of every file it takes.

**Why this priority**: Nothing else in the wave can start. P2b needs a repo to
land its minor in; P3 needs a tag to pin; P5b needs an address to repoint to.

**Independent Test**: Clone `opensoft/openXwallet`, run its two checks offline,
and read the history of any carved file back to its original openxFactory
commit. The value — a governed, self-validating wallet repository — is delivered
even if no consumer ever pins it.

**Acceptance Scenarios**:

1. **Given** openxFactory at the NAMED CARVE COMMIT, **When** the carve runs
   over exactly the twelve ratified path sets, **Then** the carved repository's
   tracked-file listing equals the carve commit's listing filtered to those
   twelve prefixes, with an empty diff of the two sorted listings.
2. **Given** the carved repository, **When** any carved file's history is read,
   **Then** its commits are the original openxFactory commits that touched it —
   not a single squashed import.
3. **Given** the carved repository, **When** `scripts/validate-openxwallet.py`
   and `scripts/wallet-yaml-syntax-gate.py` are run over its own tree, **Then**
   both exit zero, and `--strict` also exits zero.

---

### User Story 2 - The move is provably empty, so it can be bisected (Priority: P1)

A reviewer of the later atomic consume-and-shed needs to know that the bytes
openxFactory stops holding are the same bytes openXwallet starts holding. A move
whose diff is not provably empty cannot be bisected against, and it is that
property — not trust — that makes P3 safe to merge.

**Why this priority**: The byte-identity floor is the ratified precondition of
tagging `wallet-v1.0` at all (tasks 3.23–3.24, 3.28). Without the proof there is
no tag, and without the tag there is no P2b and no P3.

**Independent Test**: With only the carved repository and an openxFactory clone
at the named carve commit, reproduce both halves of the proof from the recorded
commands; every recomputed digest and every diff must land where the evidence
record says it lands.

**Acceptance Scenarios**:

1. **Given** the eight digested artifacts, **When** each one's `sha256sum` in the
   carved tree is compared against the `sha256:` recorded in openxFactory's
   `contracts/manifest.yaml` at the carve commit, **Then** all eight match.
2. **Given** the carved tree, **When** it is diffed against the carve commit over
   both contract families, the validator, the syntax gate, the gate's tests, the
   three Speckit sets and the archive packet, **Then** the diff is EMPTY.
3. **Given** each of the two promoted specs, **When** it is diffed against the
   carve commit, **Then** the diff is limited to lines `:4` and `:8` — the
   `## Purpose` placeholder and the requirement subject — asserted line by line,
   and nothing else in either file changes.
4. **Given** a carve that flattened or renamed an `examples/` prefix, **When** the
   corpus exclusion is evaluated, **Then** the 36 intended-invalid negatives are
   re-adjudicated as live records — so identical relative `examples/` paths are an
   acceptance line, not a hope.

---

### User Story 3 - The new repository gates itself from day one (Priority: P2)

The wallet repository must refuse a bad change on its own, without depending on
openxFactory's gates. That means its two checks run on every pull request, its
branch protection requires them, and its one vendored foreign artifact is
digest-verified before the validator that reads it runs.

**Why this priority**: A repository that publishes a standard but cannot refuse a
change to it is a directory with a remote. But it is P2 rather than P1 because
the carve and the proof are what the rest of the wave consumes.

**Independent Test**: Open a pull request in the new repository and observe both
checks report; then read branch protection back and see them required.

**Acceptance Scenarios**:

1. **Given** a fresh repository where no check has ever reported, **When**
   branch protection is created, **Then** it is created in EVALUATE mode —
   because a check that has never reported cannot be required — and the
   impossibility of day-one REQUIRED is recorded as unachievable rather than
   promised.
2. **Given** one trivial pull request has reported both checks green, **When**
   branch protection is promoted to ACTIVE, **Then** reading
   `rules/branches/main` back shows the required status checks.
3. **Given** the vendored envelope schema matches its recorded digest, **When**
   the validation workflow runs, **Then** the verify step passes and logs the
   verification BEFORE the validator step starts.
4. **Given** the vendored envelope schema is deliberately mutated, **When** the
   verify step runs, **Then** it FAILS CLOSED and its refusal names both
   `git submodule update --init openXwallet` and `docs/pin-resync-runbook.md`.

---

### User Story 4 - An operator can take, and reverse, every step (Priority: P2)

The operator running the cutover needs the procedure written before it is taken,
with a rollback per phase, so that a phase that goes wrong is a reversal rather
than an improvisation.

**Why this priority**: Ratified as P2's own artifact (task 3.2, proposal
§ "The cutover runbook"). It is P2 rather than P1 only because the carve is what
consumers wait on.

**Independent Test**: Read the runbook alone and take each phase; each phase
names its rollback before it is taken.

**Acceptance Scenarios**:

1. **Given** the runbook, **When** any phase is read, **Then** its rollback is
   stated in the runbook before the phase's own steps.
2. **Given** the runbook, **When** the provenance of the carve is sought, **Then**
   the NAMED CARVE COMMIT is one 40-hex sha, never "HEAD".

---

### Edge Cases

- **A case-variant name already exists.** GitHub repository names are
  case-insensitive-unique, so `openxwallet`, `OpenXWallet` or any other casing —
  in the org or in a fork — collides with `openXwallet`. Checked and recorded
  BEFORE the carve, because discovering it after costs the carve. On a hit: stop
  and report; do not carve.
- **`git filter-repo` is not installed.** The carve stops before it starts, and
  the install path taken is recorded rather than assumed.
- **A `--path` glob or a `--path-rename` slips into the carve.** Rejected by
  construction: one `--path` per set, exact paths, no globs, no renames — a
  rename re-adjudicates 36 negatives inside a check that becomes REQUIRED.
- **A shorthand loses a subtree.** Two counts are asserted explicitly rather than
  inferred: 7 files under `specs/006-openxwallet-contracts/` (its `evidence/`
  included) and 36 under `contracts/openxwallet/examples/negative/`.
- **The vendored schema arrives via the carve.** It must not: it is added by the
  SCAFFOLD commit, so the validator's `ENVELOPE_SCHEMA_PATH` needs no edit and
  the empty-diff proof survives.
- **A consumed artifact is recorded as owned.** The manifest would then claim
  ownership of an openxFactory contract; it is recorded as a CONSUMED member with
  declared fields instead, and release tooling excludes it by DECLARED FIELD, not
  by a `contracts/schemas/` path heuristic.
- **The tag is pushed before the proof.** Forbidden: `wallet-v1.0` is tagged only
  after both halves of the byte-identity proof are green.

## Requirements *(mandatory)*

### Functional Requirements

**The pre-carve gate**

- **FR-001**: The case-variant repository-name check MUST run and be RECORDED
  before the carve, over the plausible casings of `openxwallet` in `opensoft` and
  over an org-scoped repository search. Any hit stops P2.
- **FR-002**: `docs/openxwallet-cutover-runbook.md` MUST be authored before the
  carve it describes, carry a rollback per phase written before that phase is
  taken, carry the two-part byte-identity proof table, and name the carve commit.
- **FR-003**: The carve commit MUST be one 40-hex openxFactory sha, recorded in
  the runbook; **never "HEAD"**, which is no referent across a multi-PR wave.

**The carve**

- **FR-004**: The carve MUST use `git filter-repo` with one `--path` per set,
  exact paths, NO globs and NO `--path-rename`, over exactly these twelve sets:
  `contracts/openxwallet/`, `contracts/openxwallet-agent-profile/`,
  `scripts/validate-openxwallet.py`, `scripts/wallet-yaml-syntax-gate.py`,
  `tests/wallet_yaml_syntax_gate/`, `.github/workflows/wallet-validation.yml`,
  `openspec/specs/openxwallet/`, `openspec/specs/openxwallet-agent-profile/`,
  `openspec/changes/archive/2026-08-08-add-openxwallet/`,
  `specs/006-openxwallet-contracts/`, `specs/010-wallet-validator-ci/`,
  `specs/012-wallet-issuer-anchor/` — with full path history.
- **FR-005**: The carve MUST COPY: it deletes nothing from openxFactory, and
  openxFactory's tree is not modified by this feature at all.
- **FR-006**: A completeness check MUST show the carve commit's tracked listing
  over the twelve paths, sorted, EQUAL to the carved repository's tracked listing,
  sorted — evidence being the empty diff of the two sorted listings.
- **FR-007**: Two counts MUST be asserted explicitly: **7** files under
  `specs/006-openxwallet-contracts/` and **36** under
  `contracts/openxwallet/examples/negative/`.
- **FR-008**: Both `contracts/openxwallet*/examples/` directories MUST exist at
  IDENTICAL relative paths in the carved tree.

**The scaffold**

- **FR-009**: `README.md` MUST state what the repository is, name the two contract
  families, carry a doc index, carry the pin relationship in both directions, carry
  the "Domain descendants: pin and profile, never fork" rule in openAvatar's shape,
  and state the byte-identity claim naming the carve commit.
- **FR-010**: `CLAUDE.md` and `AGENTS.md` MUST point at the user-global
  OpenSpec/Speckit protocol in the house form.
- **FR-011**: `.github/CODEOWNERS` MUST cover the validator, the syntax gate,
  `contracts/`, `contract_pin.yaml` and `.github/workflows/`.
- **FR-012**: `contracts/manifest.yaml` MUST declare `contract_bundle_version:
  wallet-v1.0` and carry the EIGHT owned rows with the publisher's nine fields and
  their `sha256` values UNCHANGED from the carve commit, plus the
  content-addressed-by-commit note for the validator, the gate, both `examples/`
  trees and both family READMEs.
- **FR-013**: The same manifest MUST carry a CONSUMED-member row for the vendored
  envelope schema: the publisher's nine fields with `compatibility:
  canonical_openxfactory_contract`, `adapter_owner: openxFactory` and a `sha256`
  identifying the pinned openxFactory bytes — COMPUTED over the vendored copy at
  the carve commit, because openxFactory's own row for that artifact records no
  per-file digest — plus `member_class: consumed`,
  `release_surface: false` and `pinned_openxfactory_bundle: contract-v<pinned>`.
- **FR-014**: Release tooling MUST select `member_class: owned` ONLY for a
  `wallet-vN.M.digests.yaml` release surface — exclusion by DECLARED FIELD, never
  by a `contracts/schemas/` path heuristic.
- **FR-015**: `contracts/manifest.yaml` MUST carry `carved_from: {repository,
  commit}` as the machine-read provenance record. No bare `CARVE_COMMIT` file.
- **FR-016**: `contracts/CHANGELOG.md` MUST carry a `wallet-v1.0` entry recording a
  byte-identical carve from openxFactory `<carve_commit>`, the twelve path sets,
  the two prose edits, and no content change.
- **FR-017**: The vendored copy MUST sit at EXACTLY
  `contracts/schemas/hermes-job-envelope.schema.yaml`, byte-identical to
  openxFactory's at the carve commit, and MUST be added by the SCAFFOLD commit and
  not by the carve.
- **FR-018**: `contract_pin.yaml` MUST follow openAvatar's model — `kind:
  pinned_contract_manifest`, source repository, the carve commit as a `commit`
  revision, the vendored file with its sha256, an empty `pinned_by_commit_only:` —
  and MUST name a `verify_pin` that FAILS CLOSED pre-sync, with the pinned
  openxFactory bundle identified.
- **FR-019**: `scripts/verify-contract-pin.py` MUST recompute the vendored file's
  sha256, compare it against `contract_pin.yaml`, exit non-zero on any drift or
  absence, and carry a refusal that names `git submodule update --init openXwallet`
  and `docs/pin-resync-runbook.md` (N1).
- **FR-020**: `docs/pin-resync-runbook.md` MUST exist from day one on openAvatar's
  shape: Preconditions, Checklist, re-verify the pin offline, re-run the offline
  gate suite.
- **FR-021**: `.github/workflows/wallet-validation.yml` MUST keep job id
  `wallet-validation` and MUST run the vendored-schema verify step BEFORE the
  validator, because the validator checks only `.is_file()` — presence, not
  identity — while rule (g) reads the approval-scope vocabulary out of that file.
- **FR-022**: `.github/workflows/pytest-suite.yml` MUST exist with job id
  `pytest-suite`, running the carved `tests/wallet_yaml_syntax_gate/`.
- **FR-023**: `openspec/` MUST be initialised with `config.yaml` carrying `schema:
  spec-driven`, and both promoted specs carried under `openspec/specs/`.

**The two prose edits, and nothing else**

- **FR-024**: Prose edit one: `openxFactory SHALL` → `openXwallet SHALL` at line 8
  of `openspec/specs/openxwallet/spec.md` and
  `openspec/specs/openxwallet-agent-profile/spec.md`, across the eleven moved
  requirement bodies.
- **FR-025**: Prose edit two: the `## Purpose` placeholder at line 4 of each
  promoted spec ("TBD - created by archiving change add-openxwallet…") MUST be
  written, because a moved spec whose Purpose names another repository's archiving
  change is not a pure move either.
- **FR-026**: No other content in either promoted spec may change.

**The proof**

- **FR-027**: Part one: for each of the eight digested artifacts, `sha256sum` in
  the carved tree EQUALS the `sha256:` recorded at the NAMED CARVE COMMIT —
  evidence being an eight-row table in the runbook and in this feature's evidence.
- **FR-028**: Part two: `git diff` EMPTY over both contract families, the
  validator, the syntax gate, `tests/wallet_yaml_syntax_gate/`, the three Speckit
  sets and the archive packet, against the carve commit — AND
  diff-limited-to-two-lines over each promoted spec, asserted line by line at
  `:4` and `:8`.
- **FR-029**: `docs/byte-identity-wallet-v1.0.md` MUST record both halves with the
  commands that produced them, so a third party can reproduce the proof.

**The operator acts**

- **FR-030**: `opensoft/openXwallet` MUST be created private.
- **FR-031**: The ruleset MUST be created in EVALUATE enforcement, mirroring
  openxFactory ruleset 21538893's shape, and the impossibility of day-one REQUIRED
  MUST be recorded in the runbook as unachievable.
- **FR-032**: ONE trivial pull request MUST land so both checks report once and
  become selectable.
- **FR-033**: The ruleset MUST then be promoted to ACTIVE, with `GET
  repos/opensoft/openXwallet/rules/branches/main` captured as evidence.
- **FR-034**: `wallet-v1.0` MUST be tagged ONLY after FR-027 and FR-028 are green,
  annotated, and naming the carve commit.
- **FR-035**: A red run with a deliberately mutated vendored copy MUST be
  captured (V8) — a verifier that has never refused is not known to refuse.

**The bookkeeping**

- **FR-036**: `openspec/changes/split-openxwallet-repo/tasks.md` group 3 MUST be
  ticked with evidence (repository URL, carve commit, run ids, ruleset id, tag),
  and NOTHING else in openxFactory may be modified by this feature beyond that
  file and this feature directory.
- **FR-037**: The rollback MUST be recorded before the step it reverses: nothing
  pins openXwallet yet, so the reversal is deleting the repository or leaving it
  unpinned; openxFactory is untouched either way.

### Key Entities

- **NAMED CARVE COMMIT**: one 40-hex openxFactory sha. The referent of every
  identity claim in P2, recorded in three places (the manifest's `carved_from:`,
  the runbook, and — at P3 — openxFactory's pin file).
- **The twelve path sets**: the exact carve surface. Six under `contracts/`,
  `scripts/`, `tests/` and `.github/`; three under `openspec/`; three Speckit
  feature directories.
- **The eight owned artifacts**: the schema and registry files that carry per-file
  digests. The validator, the syntax gate, both `examples/` trees and both family
  READMEs are content-addressed by commit instead.
- **The one consumed artifact**: `contracts/schemas/hermes-job-envelope.schema.yaml`
  — vendored, digest-pinned, never claimed as owned, never on the release surface.
- **`wallet-v1.0`**: the byte-identical pure move. Any content change the
  extraction wants is a later change in the new repository.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The two sorted tracked-file listings — the carve commit's over the
  twelve paths, and the carved repository's — differ by ZERO lines.
- **SC-002**: 8 of 8 digested artifacts recompute to the digest recorded at the
  carve commit.
- **SC-003**: The part-two diff is ZERO lines over every path in the floor, and
  EXACTLY two changed lines in each of the two promoted specs.
- **SC-004**: 7 files under `specs/006-openxwallet-contracts/` and 36 under
  `contracts/openxwallet/examples/negative/`, counted and recorded.
- **SC-005**: All four local gates exit zero in the new repository — the pin
  verify, the syntax gate, the validator (plain and `--strict`), and the test
  suite — plus a green strict OpenSpec validation.
- **SC-006**: Both checks report green on the trivial pull request, and reading
  branch protection back afterwards shows them required with the ruleset in
  ACTIVE enforcement.
- **SC-007**: The verify step is observed to REFUSE at least once, on a
  deliberately mutated vendored copy, with a refusal naming its remediation.
- **SC-008**: `wallet-v1.0` exists on the new repository's default branch and its
  message names the carve commit.
- **SC-009**: openxFactory's tree carries exactly two additions from this
  feature — `specs/017-openxwallet-carve/` and ticks in
  `openspec/changes/split-openxwallet-repo/tasks.md` — and zero deletions.

## Assumptions

- The ratified artifacts are binding and are not reopened here: the twelve path
  sets, the byte-identity floor and its ONE named prose carve-out, R1–R8, D7, D8,
  D12–D14, and N1/N3/N8. Where this feature's brief and the ratified artifacts
  differ, **the ratified artifacts win** and the divergence is recorded.
- The operator acts (repository creation, the push of carved history, the ruleset,
  the tag) are authorized by Brett's 2026-08-26 instruction.
- P5a.1 — LedgerxFactory's three-candidate finder, ratified to land before P2 —
  landed as LedgerxFactory PR #25 (MERGED), so P2's precondition is met.
- `docs/openxdox-naming.md` Amendment 2 landed via openxFactory PR #396 (MERGED),
  so `openXwallet` is the ratified spelling with no surviving exception.
- The carve commit is taken as `origin/main` of openxFactory at carve time and is
  then FROZEN as a literal 40-hex sha for the whole feature.
- The vendored envelope schema's pinned openxFactory bundle is whatever
  `contract_bundle_version` openxFactory's manifest declares at the carve commit.
- The new repository is private, matching the org's other governed repositories,
  and its ruleset is created by the same API surface openxFactory's uses.

## Dependencies

- `git filter-repo` on the operator's machine. If absent it is installed and the
  install path is recorded.
- `gh` authenticated against `opensoft` with repository-creation and ruleset
  write scope.
- Network access to `github.com:opensoft/openxFactory` for the fresh clone the
  carve runs against — the shared checkout is never carved from and never edited.

## Out of Scope

- **P2b (`wallet-v1.1`)**: the nested-repository prune and the register-read note.
- **P2.5**: openxFactory's deprecating minor and the eight `relocating:` rows.
- **P3 / P3b / P4 / P4b / P5a.2 / P5b**: the consume-and-shed and every repoint.
- Any content change to the wallet standard. `wallet-v1.0` is a pure move; a
  content change here would break the property the whole wave rests on.
- Any deletion from, or rewrite of, openxFactory. P2 only adds.
