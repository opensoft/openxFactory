# Feature Specification: openxwallet deprecation minor (P2.5)

**Feature Branch**: `018-openxwallet-deprecation-minor`

**Created**: 2026-08-27

**Status**: Draft

**Input**: User description: "P2.5 deprecation minor of split-openxwallet-repo: mark the eight openxwallet manifest rows `relocating:` to opensoft/openXwallet@wallet-v1.1, record the migration note, teach check-openxfactory-pin.py to warn a consumer pinned to a relocating bundle, and cut the minor with its own digests inventory — realizes tasks.md group 5"

**Realizes**: `openspec/changes/split-openxwallet-repo` — `tasks.md` §5 (P2.5), ten
tasks. Governing design decisions **D5** (the `relocating:` marker and its
emitter) and **D6** (two separately published bundles, each owing its own digests
inventory). Clarification **N2**. Governing procedure:
`docs/contract-versioning-policy.md` (the deprecating-minor class at `:246-248`,
merge-order numbering at `:30-31`, the breaking-path precondition at `:250-252`).

## Why this feature exists (the precondition it discharges)

P3 of `split-openxwallet-repo` DELETES the eight openxwallet rows from
`contracts/manifest.yaml`. `docs/contract-versioning-policy.md:250-252` classes a
removed shape as **BREAKING (major)** and requires, before it, "at least one full
minor release where the old shape produced deprecation warnings."

This feature IS that minor. Without it P3 is an illegal cut. It changes nothing
about what the eight artifacts are or where their bytes live — it changes only
what the manifest SAYS ABOUT THEIR FUTURE, and it makes that statement reach the
one live consumer as a warning rather than as prose nobody reads.

## Clarifications

### Session 2026-08-27

No blocking ambiguity was found: design **D5** fixes the marker's key, nesting and
sub-keys and names the emitter; **D6** fixes the cut mechanics; **N2** records why
both were open and are now closed; and `docs/contract-versioning-policy.md` fixes
the numbering rule and the changelog obligations. Two decisions were RESOLVED from
authority rather than asked, and are recorded here because each departs from — or
sharpens — a literal in the ratified text:

- Q: `relocating.tag` — D5 and `tasks.md` 5.1 write `wallet-v1.0`; is that still
  the successor tag? → A: **No — `wallet-v1.1`.** Both literals predate P2b. The
  same `tasks.md`'s preamble says "openxFactory's pin at P3 records
  `wallet-v1.1`", and `proposal.md`'s `code_surface` calls `wallet-v1.1` "the tag
  openxFactory actually pins". `wallet-v1.1` was tagged on `opensoft/openXwallet`
  2026-08-26. A relocation notice names the tag a consumer MIGRATES TO, so
  naming `wallet-v1.0` would send migrators to a tag that is not the target. Every
  other element of D5's shape is taken verbatim.
- Q: Is the removal version written as an unnumbered "next major bundle" or as
  `contract-v2.0`? → A: **`contract-v2.0`, concretely.** `tasks.md` 5.2 permits
  naming the next MAJOR where naming the next MINOR is forbidden, and all three
  existing entries in "Deprecations Currently In Force" write `removal target
  contract-v2.0`. The precedent is more useful to a migrator.

Both are flagged in the pull-request body so a reviewer can overturn either
without reading this file.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - The manifest and changelog state the relocation (Priority: P1)

A consumer maintainer reads `contracts/manifest.yaml` to learn what they are
pinning. Today the eight openxwallet rows say nothing about the fact that their
canonical home is moving to a different repository. After this story each of the
eight rows carries a machine-readable statement of where the artifact is going,
under which tag, and from which bundle the statement is in force; and
`contracts/CHANGELOG.md` carries the two facts the deprecating-minor class
requires by name — the removal version and the migration path.

**Why this priority**: This is the policy precondition itself. The warning
(Story 2) and the cut (Story 3) both carry this statement; neither has anything
to carry without it. It is also the only story that a consumer who never runs a
checker can still act on.

**Independent Test**: Read the eight rows and the changelog entry. The rows each
declare a relocation target, tag, and in-force bundle; the changelog names the
removal version and the migration path. Fully testable by inspection plus the
existing manifest-digest and doc-health gates staying green.

**Acceptance Scenarios**:

1. **Given** `contracts/manifest.yaml` at this feature's commit, **When** the
   eight openxwallet rows are read, **Then** each carries a relocation
   declaration naming target repository `opensoft/openXwallet`, the successor
   tag, and the bundle from which the declaration is in force, **And** every
   other byte of those eight rows — `id`, `path`, `source_path`, `type`,
   `schema_version`, `sha256`, `compatibility`, `adapter_owner`,
   `consumption_rule` — is unchanged.
2. **Given** the same commit, **When** `contracts/CHANGELOG.md`'s newest section
   is read, **Then** it states the change class as deprecating (minor), names the
   removal version as the next major bundle, and gives the migration path.
3. **Given** the same commit, **When** the per-file digest checker runs over the
   manifest, **Then** all recorded digests still verify — the marker changes no
   contract file's bytes.
4. **Given** the same commit, **When** `docs/contract-versioning-policy.md`'s
   "Deprecations Currently In Force" list is read, **Then** this deprecation
   appears there, matching the precedent set at `contract-v1.34`.

---

### User Story 2 - A pinned consumer is warned, not failed (Priority: P2)

A DomainxFactory repository pins an openxFactory bundle. When that bundle carries
relocating rows, the consumer's own conformance run tells them so — naming each
relocating artifact, the target repository, and the tag — and **stays green**. A
consumer pinned to a bundle with no relocating rows sees nothing new.

**Why this priority**: The policy clause the precondition rests on is
"produced deprecation warnings". A marker no tool reads leaves the window
unobserved and the precondition a formality. It is P2 rather than P1 because the
statement must exist before anything can warn about it.

**Independent Test**: Run the pin checker against a fixture consumer pinned to a
bundle carrying relocating rows and against one pinned to a bundle without them.
The first prints a relocation warning and exits 0; the second prints no
relocation line and exits 0. Fully testable in the repository's own test suite
without any consumer repository present.

**Acceptance Scenarios**:

1. **Given** a consumer whose declared contract reference resolves to a bundle
   whose manifest carries relocating rows, **When** the pin check runs, **Then**
   it emits a WARN-tier relocation notice naming every relocating artifact id
   with its target repository and tag, **And** the process exit code is
   unchanged from what it would have been without the notice.
2. **Given** a consumer pinned to a bundle whose manifest carries no relocating
   rows, **When** the pin check runs, **Then** no relocation notice is emitted.
3. **Given** a consumer whose pin is divergent from the aggregation pointer (the
   pre-existing ERROR case), **When** the pin check runs, **Then** the ERROR
   verdict and its nonzero exit are preserved, **And** a relocation notice, if
   any applies, is additional rather than substituted.
4. **Given** a checkout where the pinned bundle's manifest cannot be read at all,
   **When** the pin check runs, **Then** it reports no relocation notice and does
   not fail — an unanswerable question is not a finding.
5. **Given** the pre-existing pin verdicts (equal, stale-behind, divergent,
   outside-aggregation), **When** the existing tests run, **Then** all still
   pass unchanged.

---

### User Story 3 - The minor is a properly published bundle (Priority: P3)

The deprecation is not a loose edit: it is a numbered bundle with its own release
surface record, so that the "one full minor release" the breaking path requires
is a thing that exists and can be pointed at.

**Why this priority**: A cut with no inventory is a non-conformant release under
`release-surface-integrity`, and P5a.2 (the LedgerxFactory bump that observes the
warning) has nothing to pin until the number exists. It is last because the
number is only correct relative to merge order.

**Independent Test**: The declared bundle version, the changelog heading, and the
release inventory file name agree; the inventory verifies against the commit's
bytes; the release-inventory drift check reports no findings.

**Acceptance Scenarios**:

1. **Given** this feature's commit, **When** the declared bundle version, the
   newest changelog heading, and the release inventory file name are compared,
   **Then** all three name the same bundle.
2. **Given** this feature's commit, **When** the release-inventory drift check
   runs, **Then** it reports no error-class finding.
3. **Given** this feature's commit, **When** the release surface is enumerated,
   **Then** `contracts/manifest.yaml` is among its members and the manifest it
   digests still carries all eight openxwallet rows — this minor removes nothing.
   (The eight artifact files are not themselves inventory members and never have
   been; see FR-017 and `research.md` R11.)
4. **Given** the bundle number authored here, **When** another bundle lands on
   the base branch first, **Then** the number is reallocated before merge rather
   than merged as authored.

---

### Edge Cases

- **A row already carrying a relocation declaration** — re-marking must be
  idempotent in effect; the eight rows have none today.
- **A relocation declaration whose nested keys collide with digest-walking
  tooling** — the per-file digest checker walks every nested mapping that has
  both a path and a digest key; the relocation declaration must not present that
  shape, or it would be mistaken for an artifact entry.
- **The pinned bundle's manifest is absent or unparseable** — treated as "the
  question could not be asked": no notice, no failure.
- **The consumer's pin is a commit, not a tag** — the relocation question is
  asked of the manifest AT THAT COMMIT, because a bundle need not have a tag at
  the moment a consumer pins it.
- **A bundle lands ahead of this one** — the authored number becomes wrong; it is
  re-verified at merge, never reserved.
- **Rollback after publication** — a published bundle is not unpublished. The
  only honest reversal is a FOLLOWING minor that removes the marker.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each of the eight openxwallet rows in `contracts/manifest.yaml`
  MUST carry exactly one added sibling key declaring the relocation, as a nested
  mapping naming the target repository, the successor tag, and the bundle since
  which the declaration is in force.
- **FR-002**: The eight rows MUST carry NO removal-version key. The removal
  version lives in the changelog, per `docs/contract-versioning-policy.md:246-248`.
- **FR-003**: Every byte of the eight rows other than the added key MUST be
  unchanged, and no file under `contracts/openxwallet/` or
  `contracts/openxwallet-agent-profile/` may be modified — the byte-identity
  floor.
- **FR-004**: No manifest row may be REMOVED by this feature. Removal is P3.
- **FR-005**: `contracts/CHANGELOG.md` MUST gain a section for this bundle
  declaring the change class as deprecating (minor) and stating BOTH required
  facts: the removal version (the next major bundle) and the migration path.
- **FR-006**: `docs/contract-versioning-policy.md`'s "Deprecations Currently In
  Force" list MUST record this deprecation, following the `contract-v1.34`
  precedent.
- **FR-007**: `scripts/check-openxfactory-pin.py` MUST emit a WARN-tier notice
  when the bundle a consumer pins carries relocating rows, naming each relocating
  artifact id with its target repository and tag.
- **FR-008**: That notice MUST NOT change the script's exit-code semantics: WARN
  exits 0, ERROR exits nonzero, exactly as today.
- **FR-009**: The relocation notice MUST be additive to the existing pin verdict,
  never a replacement for it; the existing `classify()` contract and its four
  verdicts MUST remain intact.
- **FR-010**: When the pinned bundle's manifest cannot be resolved or read, the
  check MUST emit no relocation notice and MUST NOT fail.
- **FR-011**: `scripts/validate-domain-openxfactory-pins.py` MUST NOT be made an
  emitter, and the reason MUST be recorded: it has no warning tier, so emitting
  there would make a relocation notice an ERROR and red every domain pinning this
  minor — the exact failure the manifest-carried marker was chosen to avoid.
- **FR-012**: `scripts/validate-openxwallet.py` MUST NOT be edited by this
  feature.
- **FR-013**: The new behavior MUST be covered by tests in the existing test
  location and style for this script, including the no-relocation, relocation,
  ERROR-preserved, and unreadable-manifest cases.
- **FR-014**: `contracts/manifest.yaml`'s declared bundle version MUST be bumped
  to the new minor, and a release inventory MUST exist for that bundle at
  `contracts/releases/<bundle>.digests.yaml`.
- **FR-015**: The release inventory MUST be produced by the repository's release
  tooling, never hand-authored.
- **FR-016**: The declared bundle version, the newest changelog heading, and the
  inventory file name MUST agree.
- **FR-017**: The release surface MUST still contain the eight openxwallet
  registrations — this minor removes nothing.
  **CORRECTED DURING IMPLEMENTATION** (see `research.md` R11): the inventory's
  membership is CATALOG-DRIVEN, from `contracts/hermes-runtime/contract-index.yaml`
  via `release._collect_members`, and it has **never** included the eight
  artifact FILES — not at `contract-v1.45`, not at any earlier bundle. D6's phrase
  "a release surface that STILL CONTAINS the eight artifacts" therefore cannot be
  read as inventory file-membership. The containment that actually exists, and
  that this requirement is checked against, is TRANSITIVE: `contracts/manifest.yaml`
  IS a digested inventory member, it still carries all eight rows, and the
  inventory records the digest of exactly that manifest. The checkable form is:
  (a) no openxwallet row was removed from the manifest, (b) the manifest is an
  inventory member, and (c) the inventory's recorded manifest digest is the digest
  of the eight-row manifest at this commit.
- **FR-018**: The annotated bundle tag MUST NOT be created by this feature. Tag
  creation is an operator act performed at merge on the realized commit.
- **FR-019**: The bundle number MUST be presented as subject to re-verification
  at merge order, per `docs/contract-versioning-policy.md:30-31`.
- **FR-020**: The rollback posture MUST be recorded before the cut: a published
  bundle is not unpublished; reversal is a following minor that removes the
  marker.
- **FR-021**: The completed items of `openspec/changes/split-openxwallet-repo`
  `tasks.md` §5 MUST be ticked with evidence notes, and items that complete only
  at merge MUST be left unticked with a note saying so. No other group's items
  may be touched.

### Key Entities

- **Relocation declaration**: the per-row statement that an artifact's canonical
  home is moving. Attributes: target repository, successor tag, bundle since
  which the declaration is in force. Carries no removal version and no digest.
- **The eight openxwallet rows**: `openxwallet-record`,
  `openxwallet-custody-registry-schema`, `openxwallet-custody-registry`,
  `openxwallet-grant`, `openxwallet-grant-exercise`,
  `openxwallet-distinct-holder-constraint`, `openxwallet-subject-attestation`,
  `openxwallet-agent-composition` — seven under `contracts/openxwallet/` and one
  under `contracts/openxwallet-agent-profile/`, at `contracts/manifest.yaml`
  lines 1999, 2017, 2030, 2043, 2056, 2069, 2082 and 2095.
- **The deprecation minor**: a numbered contract bundle whose only semantic
  content is the relocation statement. Owns a changelog section and a release
  inventory; its tag is cut at merge.
- **The relocation notice**: the WARN-tier output a pinned consumer sees.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All eight openxwallet artifacts remain registered and fully
  described after this feature — zero rows removed, zero contract bytes changed.
- **SC-002**: A maintainer reading any one of the eight rows can name the target
  repository and successor tag without consulting another file.
- **SC-003**: A consumer pinned to this bundle sees the relocation stated in
  their own conformance run output, and their run stays green.
- **SC-004**: A consumer pinned to the preceding bundle sees no new output.
- **SC-005**: Every pre-existing pin-check verdict behaves identically; the
  script's existing test set passes unchanged.
- **SC-006**: The repository's release-inventory consistency check reports no
  error-class finding for the new bundle.
- **SC-007**: `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes, and
  doc-health reports no NEW finding relative to the base commit.
- **SC-008**: P3 can be authored as a legal breaking cut, because exactly one
  full minor release carrying the deprecation warning now exists.

## Assumptions

- **The successor tag is `wallet-v1.1`, not `wallet-v1.0`.** `design.md` D5 and
  `tasks.md` 5.1 write the literal `wallet-v1.0`; both were authored before P2b
  existed. `tasks.md`'s own preamble says "openxFactory's pin at P3 records
  `wallet-v1.1`", and `proposal.md`'s `code_surface` names `wallet-v1.1` as "the
  tag openxFactory actually pins". `wallet-v1.1` is tagged on
  `opensoft/openXwallet` as of 2026-08-26. A relocation notice must name the tag
  the consumer should MOVE TO; naming `wallet-v1.0` would point migrators at a
  tag that is not the migration target. The `relocating:` key name, its nesting,
  its three sub-keys, the absence of a removal key, and the choice of emitter are
  all taken from D5 exactly as written.
- **The removal version is named concretely as `contract-v2.0`.** `tasks.md` 5.2
  permits naming the next major where naming the next minor is forbidden, and the
  three existing entries in "Deprecations Currently In Force" all write
  `removal target contract-v2.0`. Following the precedent is more useful to a
  migrator than the unnumbered phrasing.
- **The bundle is authored as the next sequential minor after the current
  declared bundle.** The number is correct only relative to merge order and is
  re-verified before merge; if another bundle lands first this feature is
  renumbered, not merged as authored.
- **The relocation question is asked of the manifest at the consumer's pinned
  commit**, read out of the publisher checkout's history, because the checker
  already runs from the pinned openxFactory checkout and a pinned bundle need not
  have a tag.
- **No manifest schema or strict-key validator exists** for
  `contracts/manifest.yaml` in this repository, so the added key needs no schema
  extension. The one tool that walks nested manifest mappings keys off the
  co-presence of a path and a digest field, which the relocation declaration does
  not have.
- **`docs/contract-versioning-policy.md` is a release-surface member**, so
  editing it moves its digest in this cut's inventory — which is why the
  inventory is generated last.
- The eight rows' `sha256` values and the packaged corpus are untouched; the
  byte-identity floor proven at `wallet-v1.0` is unaffected by this feature.
- Another pull request is concurrently ticking `tasks.md` §4; this feature ticks
  §5 only and expects a trivial rebase on that file.
