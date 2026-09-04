# Feature Specification: `deliberation` — register entry number two and its neutral return schema

**Feature Branch**: `029-admit-deliberation-realization`

**Created**: 2026-09-04

**Status**: Draft

**Input**: User description: "Build the REALIZATION of the ratified openxFactory change `admit-deliberation-clearing-operation` — the `deliberation` entry in the closed permitted-operations register, the new neutral `contracts/clearing/deliberation-return.schema.yaml`, the three admitted refusal grounds, and the bookkeeping that moves with them."

**Lane**: `hermes-wallet-exercise`

## Context and authority

**THIS FEATURE IS A REALIZATION, NOT A PROPOSAL. It authors no requirement, adds
no spec delta, and settles nothing the ratified text left open.** Where the
ratified text is silent, this feature takes the most conservative reading
available and records it in [research.md](./research.md) as a stated assumption
with its source, rather than deciding it silently.

Its authority is ONE ratified OpenSpec change:

- **`admit-deliberation-clearing-operation`** — RATIFIED 2026-09-04 at 12:37Z by
  Brett Heap (repository owner), verbatim *"D10 A, D13 A, ratify #645"*, at
  ratified head `22afb198`; record
  `openspec/changes/admit-deliberation-clearing-operation/review/ratification-2026-09-04.md`.
  Merged as PR **#645**, merge commit `3cf917b7`. Its `tasks.md` **Phase 2** is
  this feature's build list, item for item; its
  `specs/clearing-dispatch-boundary/spec.md` fixes every fact of the entry; its
  `design.md` D4 rules the schema, D8 the fixture re-point, D9 the five frozen
  copies, D10 and D13 the two questions ruled A, and D11 the ledger.

It stands ON, and restates nothing of, the basis it extends:

- **`add-clearing-dispatch-boundary`** — RATIFIED 2026-09-01, merged PR #555
  (`ab0bb2dd`), REALIZED in `contracts/clearing/` by PR #628 (`0d5e1ba9`) at
  `contract-v3.3`, and **NOT YET ARCHIVED**. The capability
  `clearing-dispatch-boundary` therefore lives in that change's
  `## ADDED Requirements` block and in no promoted specification; the ratified
  delta this feature realizes is written OVER it, in prose, as
  `govern-sibling-added-modified-deltas` requires of an ADDED block.
- **`add-cpc-clearing-boundary`** — RATIFIED 2026-09-02, merged `c0270d28`.

**The claim** (Lane Collision Protocol Rule 1) is posted on openxFactory PR #645
as the comment beginning `CLAIMED — lane hermes-wallet-exercise … for the
REALIZATION`. The packet's own Rule 1 and Rule 7 claims are recorded in its
`tasks.md` items 1.3 and 1.4.

## User Scenarios & Testing *(mandatory)*

The "users" of this slice are: a CLEARING implementation that must decide whether
a `deliberation` dispatch may proceed; a PRODUCER (codexFactory PR #165) whose
leg 3 needs a legal home and whose leg 3/leg 4 return needs a neutral shape to be
validated against; a REVIEWER asked to approve an operation or a widening; and a
CONSUMER pinning a contract bundle version.

### User Story 1 - A deliberation dispatch has a lawful register entry (Priority: P1)

codexFactory PR #165 reshapes council deliberation into a four-leg, bundle-shaped
lane whose leg 3 runs the seats on the governed host. Under the closed register
there is no legal home for such a host job, and adding one by editing the
clearing workflow is explicitly non-conformant. This story ships the entry.

**Why this priority**: every other item in the slice is either a consequence of
the entry existing (the return schema it declares, the grounds its refusals need)
or bookkeeping that moves with it. Without the entry nothing else has a subject.

**Independent Test**: `python3 scripts/validate-clearing-dispatch.py .` reports
`2 registered operations` and exits 0; `tests/clearing/test_register_closure.py`
passes on an entry-two twin of every entry-one assertion.

**Acceptance Scenarios**:

1. **Given** the shipped register instance, **When** the canonical validator
   reads it, **Then** it reports exactly two registered operations and no
   `clearing-register-member-unratified` finding.
2. **Given** the shipped register instance, **When** the entry-two facts are read
   member by member, **Then** `checks_out_code`, `writes`,
   `may_reference_secrets` and `repository_affecting_output` are all `false`,
   `token_scopes` is exactly `["actions:read"]`, `timeout_minutes` is bounded,
   `worker_profile` is `council-deliberation-worker`, `data_handling` is
   `internal-governance`, and `output_schema_ref` is
   `contracts/clearing/deliberation-return.schema.yaml`.
3. **Given** the shipped register instance, **When** entry two's lanes are read,
   **Then** there is exactly ONE lane and it is
   `artifact` / `xfactory-artifact-workers` / `host-rider-cpc-brett01` /
   `xfactory-artifact-cpc-brett01`.
4. **Given** a register instance carrying a THIRD, unratified member, **When** the
   validator reads it, **Then** `clearing-register-member-unratified` fires and
   names the member.

### User Story 2 - A deliberation return has a neutral shape to be validated against (Priority: P1)

The register's own rule is that a return is validated against the DECLARED value
and never against a bundle's copy of it, and that the declared schema must not be
a path a producing repository owns. No neutral schema for the deliberation return
exists. This story ships one, of the ratified kind
`xfactory_clearing_deliberation_return`, and ROUTES that kind so the shape check
and the verdict scan exist at all.

**Why this priority**: an `output_schema_ref` pointing at a file that does not
exist is an entry that declares a check nobody can perform, and an unrouted kind
is not validated loosely — it is not validated at all.

**Independent Test**: the packaged positive example validates clean; a fixture
declaring `schema` fails the shape check; a fixture carrying a verdict-named
member is refused `clearing-report-carries-a-verdict`.

**Acceptance Scenarios**:

1. **Given** a well-formed deliberation return, **When** the validator adjudicates
   it, **Then** no finding is reported.
2. **Given** a deliberation return whose shape does not match the declared
   schema, **When** the validator adjudicates it, **Then** the family's SHAPE
   refusal `schema` fires — the closed finding-code set is not widened.
3. **Given** a deliberation return carrying a member whose name reads as a
   verdict, an eligibility, a decision, a go/no-go, an approval or a
   recommendation, **When** the validator adjudicates it, **Then**
   `clearing-report-carries-a-verdict` fires.
4. **Given** the family's schema list, **When** it is counted, **Then** it is SIX
   and the sixth is named in the pinned list rather than discovered by a glob.

### User Story 3 - A refusal of this operation can be written down (Priority: P2)

The dispatch record's refusal-ground enumeration is CLOSED and a ground absent
from it must be added by a governed change rather than recorded as free text.
Three of the nine grounds the record awaits become emittable when this entry
lands. This story admits exactly those three and writes down the rule by which
the remaining six will be rendered.

**Why this priority**: without it, the entry's own scenarios name refusals with
no lawful way to record them — the free-text hole the closed enumeration exists
to close. It is P2 only because nothing dispatches yet.

**Independent Test**: a packaged refused-dispatch record naming each of the three
grounds validates clean, while the free-text fixture still fires
`clearing-record-refusal-ground-unknown`.

**Acceptance Scenarios**:

1. **Given** the dispatch-record schema, **When** `$defs.refusal_ground.enum` is
   read, **Then** it holds exactly five members: the two seeded plus
   `lane_not_permitted`, `output_schema_failure`, `origin_scoped_credential`.
2. **Given** a refused dispatch record naming any one of the three new grounds,
   **When** the validator adjudicates it, **Then** no
   `clearing-record-refusal-ground-unknown` finding is reported.
3. **Given** a refused dispatch record naming a ground outside the enumeration,
   **When** the validator adjudicates it, **Then**
   `clearing-record-refusal-ground-unknown` still fires.

### User Story 4 - The closure refusal keeps a live probe (Priority: P2)

Two packaged negative fixtures use `deliberation` as the honest unratified
operation name. Admitting it would turn both green for the wrong reason and take
the closed register's refusal out of the red-proven set. This story re-points
them to `coding`.

**Why this priority**: the clearing gate asserts `N/N closed refusal codes
red-proven`, so a fixture that stopped firing turns a required-adjacent check
red. It is a consequence of Story 1 and lands in the same diff.

**Independent Test**: `clearing-register-member-unratified` and
`clearing-unregistered-operation` both still fire, now on `coding`, and the
validator still reports `26/26 closed refusal codes red-proven`.

**Acceptance Scenarios**:

1. **Given** the re-pointed register fixture, **When** the validator adjudicates
   it, **Then** `clearing-register-member-unratified` fires and names `coding`.
2. **Given** the re-pointed manifest fixture, **When** the validator adjudicates
   it, **Then** `clearing-unregistered-operation` fires.
3. **Given** each re-pointed fixture's header, **When** it is read, **Then** its
   prose argues about `coding` and not about `deliberation`.

### Edge Cases

- **The five frozen copies.** The register's member set is pinned in five places
  (validator constant, independent test constant, the instance, the CI gate's
  literal grep, and the test that pins that grep from a second file). Moving four
  and missing one is the failure mode; each is proven to fail ALONE.
- **The three pinned numerals.** The schema-filename list, the manifest row
  count, and the per-file row digests each move with the new schema and each
  fails loudly on its own.
- **A fixture that mints a code.** The new negative fixture declares the family's
  shape refusal `schema`, which
  `test_no_fixture_declares_a_code_outside_the_closed_set` excepts by name. No
  `clearing-…` code is minted, and the probed set is arithmetically untouched.
- **The free-text ground fixture.** `dispatch-record-with-a-free-text-refusal-ground.yaml`
  claims `deliberation` as its operation; its declared failure is a ground that
  stays outside the enumeration, so it keeps its own reason. Confirmed by running
  it, not by reading it.
- **A dormant second door.** Admitting the entry authorizes no host job. The
  route-retirement obligation binds the change in the clearing repository that
  declares one, and is carried forward rather than discharged here.

## Requirements *(mandatory)*

Every requirement below is a RESTATEMENT OF A RATIFIED FACT for traceability, not
a new rule. The authoritative text is the ratified delta.

- **FR-001** The register instance MUST hold exactly two members,
  `readiness-diagnostic` and `deliberation`, and MUST declare
  `registry_version: 2`.
- **FR-002** Entry two MUST declare every fact the closed-register requirement
  demands, with the values fixed in the ratified requirement.
- **FR-003** Entry two MUST declare THE ARTIFACT LANE AND ONLY THE ARTIFACT LANE,
  with all four lane members literal.
- **FR-004** A NEW NEUTRAL schema MUST exist at
  `contracts/clearing/deliberation-return.schema.yaml`, of kind
  `xfactory_clearing_deliberation_return`, closed to unknown members throughout,
  carrying seat identity, that seat's output, and the run identifiers binding the
  return to the convening job id, the verified subject pin and the inbound bundle
  digest — and NO verdict, eligibility, decision, go/no-go, approval or
  recommendation member.
- **FR-005** The new kind MUST be routed in `KIND_TO_SCHEMA`, and the
  `VERDICT_WORDS` scan MUST be applied to it, emitting the EXISTING code
  `clearing-report-carries-a-verdict`.
- **FR-006** The validator's closed finding-code set MUST NOT gain a member.
- **FR-007** `$defs.refusal_ground.enum` MUST gain exactly
  `lane_not_permitted`, `output_schema_failure`, `origin_scoped_credential`, and
  its description MUST carry the rendering rule by which the remaining six will
  be produced.
- **FR-008** The five frozen copies of the member set MUST move in ONE diff, and
  each MUST be proven to fail alone.
- **FR-009** The two `deliberation`-named negative fixtures and the refused
  dispatch-record example MUST be re-pointed to `coding`, comments included.
- **FR-010** `contracts/manifest.yaml`, `contracts/README.md`,
  `contracts/clearing/README.md` and `contracts/CHANGELOG.md` MUST move with the
  bytes, and the clearing header's negative-fixture count MUST be corrected to
  the MEASURED value rather than incremented from the written one.
- **FR-011** The new schema MUST be REGISTERED in `contracts/manifest.yaml` with
  its digest. **NO BUNDLE NUMBER IS RESERVED.** `contract-v3.4` was claimed on
  openxFactory issue #630 row 4 by lane `repo-shape` at 2026-09-04T12:40Z on the
  repository owner's word *"cut contract-v3.4"*, and Amendment 1 rule 7
  serializes contract-cut claims FIFO — so `contract_bundle_version` does not
  move here, no changelog entry is written, and no release inventory is built.
  The row records the CHANGE that registered it and leaves the number to the
  cutting session, which is the form the `chain-anchoring` and
  `chain-attestation` rows in this manifest already use and the form
  `docs/contract-versioning-policy.md` requires. See research.md § O7 —
  **LEFT FOR BRETT**.

### Key Entities

- **Register entry two (`deliberation`)** — a bundle-carrying, evidence-only
  operation on the artifact lane.
- **Deliberation return** — the neutral record of kind
  `xfactory_clearing_deliberation_return`: per-seat outputs plus the three
  binding identifiers.
- **Refusal ground** — a member of the dispatch record's CLOSED enumeration,
  snake_case and unprefixed; NOT the validator's hyphenated finding code.

## Success Criteria *(mandatory)*

- **SC-001** `python3 scripts/validate-clearing-dispatch.py .` exits 0, reports
  `2 registered operations`, and still reports `N/N closed refusal codes
  red-proven` with N unchanged at 26.
- **SC-002** `python3 -m pytest tests/ -q -m "not postgres"` is green.
- **SC-003** `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` passes.
- **SC-004** The doc-health single-repo run reports no finding naming a path this
  feature moved, and the `contract-v3.3` release inventory shows no NEW drift —
  measured member by member at this head and at the base, research.md § O8.
- **SC-005** Each of the five frozen copies and each of the three pinned numerals
  has been observed RED alone.
- **SC-006** No new member of `REFUSAL_CODES`; no fourth refusal ground; no
  register member beyond the two.

## Out of Scope

Carried from the ratified proposal's own "What this proposal does NOT do" and
Phase 4:

- **`opensoft/xFactory`'s `clearing-dispatch.yml`** — the `deliberation` host job,
  the registry-instance validation replacing the literal choice list (basis
  tasks.md § 3.7), and the RETIREMENT of `council-deliberation-worker.yml` in the
  same act. **Named, not done.**
- **`opensoft/codexFactory` PR #165's legs 1 and 4** and its own retirement half.
- **A `coding` operation.** It appears here only as a fixture name.
- **A hosted finalizer.** `repository_affecting_output: false` means none applies.
- **Any seat key, mint, or change to where signing happens.**
- **The three packaged attestation fixtures** that carry
  `council-deliberation-worker.yml` as a live allowlisted member. They stay
  correct until the retirement lands (Phase 4.2a).
- **THE WHOLE CONTRACT CUT** — the version line, the changelog entry, the release
  digest inventory and the annotated tag (the ratified `tasks.md` Phase 3, items
  3.1 – 3.4). `contract-v3.4` is another lane's on the owner's word; this feature
  registers rows and reserves no number. research.md § O7.
- **The openspec archive** of the change (its Phase 5), which is ordered after
  `add-clearing-dispatch-boundary` archives.
