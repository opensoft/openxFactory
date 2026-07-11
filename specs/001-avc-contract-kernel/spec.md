# Feature Specification: AVC Contract Kernel

**Feature Branch**: `001-avc-contract-kernel`

**Created**: 2026-07-11

**Status**: Draft

**Input**: OpenSpec change `define-avatar-client-contract-kernel` — publish the
canonical, provider-neutral avatar-client (AVC) contract kernel: eight
YAML-serialized JSON Schema (draft 2020-12) contracts under
`contracts/avatar-client/`, shared definitions, closed registries, three
neutral consent purposes, canonical fixtures, an avatar-client validator, a
stable acceptance map (ACR-*/SCO-*/RBG-* identifiers), and content-addressed
release governance.

## Clarifications

### Session 2026-07-11

- Q: Which files constitute the content-addressed released bundle? → A: The
  digested, manifest-registered bundle is the full consumed set — the 8 schemas,
  shared definitions, all closed registries, the consent-purpose registry, the
  canonical fixtures, the acceptance map, the interface lock, and the
  consolidated evidence/disposition register — each with its own SHA-256 digest;
  `scripts/validate-avatar-client.py` ships at the release commit as reproducible
  reference tooling, not a pinned semantic artifact.
- Q: For AVC-07/AVC-08, ship schemas only or instances too? → A: Ship schema +
  conformance fixtures only; no live persona/retention instances, extra examples,
  or domain templates (domains own concrete persona and retention content).
- Q: How is redaction / secret-exclusion enforced? → A: Both structural schema
  exclusion (secret/SDP/raw-media fields structurally invalid where prohibited)
  and a committed-content denylist scan over fixtures and evidence; synthetic
  test sentinels MUST be explicitly bounded so they cannot become a bypass for
  real secret patterns.
- Q: What evidence artifact covers manual/live_f0/successor scenarios? → A: One
  consolidated, content-addressed evidence/disposition register under
  `contracts/avatar-client/` — automated scenarios name fixture evidence; manual
  scenarios carry a recorded result plus reviewer/disposition fields; `live_f0`
  and successor scenarios name the owning change and the fail-closed default that
  remains active; the validator checks completeness, allowed status transitions,
  and referenced-artifact existence.
- Q: How is cross-language consumer conformance defined? → A: Through
  language-neutral, self-describing fixtures — each declares its target
  schema/registry, expected valid/invalid result, and stable scenario/evidence
  ID — executable by any draft-2020-12 implementation; the Python validator is
  the reference runner, not a required consumer dependency.
- Q: Who owns the F0 evidence schemas the gate consumes? → A: The F0 sibling
  `qualify-avatar-brokered-call-feasibility` owns and versions
  `f0-results.schema.yaml` and `f0-interface-impact.schema.yaml`; the kernel
  publication gate pins the exact F0 source commit and both schema digests,
  validates the evidence instances against those pinned schemas, then reads
  `PASS` / variance dispositions, and fails closed on a missing schema, digest
  mismatch, validation failure, unknown status, or unknown variance field. The
  kernel does not duplicate or co-own the F0 schemas.
- Q: Is tag publication inside this feature's Definition of Done? → A: Two
  completion states. The Speckit feature may reach "implementation complete,
  publication pending F0" once all kernel artifacts and validators are merged and
  green and the publication gate is enforced; the OpenSpec change stays active
  and its publication/handoff tasks remain incomplete until F0 is `PASS`, all
  variances are dispositioned, the annotated tag is published, and release
  digests are recorded. The release is not called realized at the earlier
  milestone.

## User Scenarios & Testing *(mandatory)*

<!--
  The "users" of this feature are governance and integration stakeholders:
  contract consumers (clients, brokers, workflow services, DomainxFactories),
  the release owner who publishes bundles, the sibling implementation changes
  that consume the frozen interface baseline and released registries, and the
  governance reviewers who verify acceptance-map traceability. This feature
  delivers the neutral contract kernel only; it does not build the broker,
  the Flutter client, the F0 harness, or the avatar-first UI assets.
-->

### User Story 1 - Publish the neutral AVC contract kernel (Priority: P1)

A contract consumer (a future client, session broker, workflow service, or
DomainxFactory) needs one provider-neutral avatar protocol to build against
before any reusable client, reference broker, or domain overlay can be built
safely. This story publishes the eight AVC contracts, their shared
definitions, the closed registries, and the three neutral consent purposes as
the single canonical source of avatar-session meaning.

**Why this priority**: Nothing else in the avatar-client program — feasibility,
reference runtime, or UI standard — can proceed against a stable interface
until this neutral surface exists. It is the minimum viable deliverable.

**Independent Test**: Confirm that the eight contract files, the shared
definitions module, the closed registries, and the consent-purpose registry
exist under `contracts/avatar-client/`; that every contract declares a contract
identifier and contract schema version; that every cross-reference resolves;
and that each closed registry enumerates exactly the ratified members.

**Acceptance Scenarios**:

1. **Given** a consumer pinned to the same contract major, **When** it reads a
   fixture that adds a supported optional field, **Then** it preserves or
   ignores the field per compatibility policy without changing canonical
   behavior. *(traces ACR-001-S01)*
2. **Given** a consumer that cannot satisfy the required contract major,
   **When** it evaluates compatibility, **Then** session preflight fails before
   media or governed commands are enabled. *(traces ACR-001-S02)*
3. **Given** an unknown command, authority-bearing event, confirmation
   decision, or lifecycle state, **When** a consumer encounters it, **Then** the
   transition is rejected and no permissive meaning is inferred. *(traces
   ACR-001-S03)*
4. **Given** the AVC-02 result contract, **When** a denial or terminal result
   attempts to carry SDP, an SDP answer, or a credential, **Then** schema
   validation fails and the result cannot be produced. *(traces ACR-002-S09)*

---

### User Story 2 - Prove conformance with fixtures, validator, and acceptance map (Priority: P2)

A governance reviewer and any pinning consumer need machine-checkable proof
that the published contracts mean what the ratified change says, and that every
normative requirement and scenario is traceable to evidence. This story adds
the canonical fixtures, the `scripts/validate-avatar-client.py` validator, and
the acceptance map keyed by stable ACR-*/SCO-*/RBG- identifiers.

**Why this priority**: Contracts without conformance evidence are assertions.
This story makes the kernel verifiable and gives consumers the fixtures they
run in their own CI to prove they have not drifted.

**Independent Test**: Run the validator against the published contracts and
fixtures; confirm it passes on canonical valid fixtures, rejects invalid,
adversarial, and redaction-violating fixtures, and fails when any normative
requirement or scenario is unmapped, duplicated, renamed, or evidence-free.

**Acceptance Scenarios**:

1. **Given** the full set of canonical fixtures, **When** the validator runs,
   **Then** it passes every valid fixture and rejects every invalid, boundary,
   unknown-field, unknown-authority, redaction-violation, and adversarial
   fixture.
2. **Given** the acceptance map, **When** a normative requirement or scenario is
   omitted, duplicated, renamed, or references missing evidence, **Then** the
   validator fails and the owning task remains incomplete. *(traces ACR-012-S03)*
3. **Given** a telemetry, log, or fixture artifact, **When** it contains a
   credential, SDP, raw transcript, raw media, or a prohibited high-cardinality
   identifier, **Then** validation fails and the artifact is not published.
   *(traces ACR-011-S01)*

---

### User Story 3 - Govern a content-addressed contract release (Priority: P3)

A consumer must be able to pin the kernel safely and reproducibly, and the
release owner must publish a single coherent bundle identity. This story
ratifies openxFactory as the canonical owner and defines the coordinated
release identity — one matching manifest version, changelog entry, annotated
tag, exact release commit, and per-file digests — plus the content-addressed
pinning consumers must use.

**Why this priority**: Without a coherent, content-addressed release, consumers
cannot pin deterministically and a movable tag would masquerade as a
compatibility guarantee. It depends on P1/P2 existing to release.

**Independent Test**: Confirm that a released bundle's manifest version,
changelog entry, annotated tag, release commit, and per-file digests all
identify the same realized bundle; that a consumer pin recorded as a tag alone
fails conformance; and that the version is allocated only at realization.

**Acceptance Scenarios**:

1. **Given** a proposed release, **When** the manifest version, changelog
   release, annotated tag, release commit, or file digests do not identify the
   same realized bundle, **Then** release validation fails and consumers are not
   told to upgrade. *(traces SCO-001-S02)*
2. **Given** a consumer that records only a bundle tag, **When** it omits the
   exact commit and required per-file digests, **Then** consumer conformance
   fails because a tag alone is not a content-addressed pin. *(traces SCO-001-S03)*
3. **Given** a consumer's own models, **When** they fail the canonical fixture
   suite of the pinned release, **Then** the consumer's release validation
   fails. *(traces SCO-001-S04)*

---

### User Story 4 - Gate publication on F0 feasibility while allowing parallel work (Priority: P4)

The sibling F0 feasibility change measures the brokered-call protocol before
the kernel commits to it. This story lets kernel schema and fixture
implementation proceed concurrently against the frozen `avatar-client-parallel-v1`
baseline, but blocks the bundle tag until F0 evidence is `PASS` and every
reported interface variance is dispositioned, freezing the realized decisions in
an interface-lock artifact.

**Why this priority**: It preserves parallelism across the four workstreams
while ensuring the published contract is backed by real feasibility evidence.
It sequences only the final publication, not the concurrent authoring.

**Independent Test**: Confirm that schema and fixture files can be authored and
validated while F0 is pending, but that the annotated tag cannot be published
when F0 evidence is absent, `FAIL`, or `INCONCLUSIVE`, or when any interface
variance is undispositioned.

**Acceptance Scenarios**:

1. **Given** incomplete or non-passing F0 evidence, **When** contract
   publication and annotated tagging are requested, **Then** they remain blocked
   while parallel implementation continues against the recorded provisional
   baseline. *(traces ACR-012-S02)*
2. **Given** an interface variance reported by F0 or a sibling, **When** it is
   undispositioned, **Then** the bundle tag remains blocked until it is
   dispositioned and the interface-lock is updated only in this change.
3. **Given** deterministic-lab evidence is incomplete, **When** live
   qualification is attempted, **Then** it remains blocked. *(traces ACR-012-S01)*

---

### User Story 5 - Ratify repository and reference boundaries for successors (Priority: P5)

Successor changes need clear ownership boundaries: where the reusable client
lives, what it may never hold, and how aggregation and web-console integration
are deferred. This story ratifies the future private `xfactory-avatar-client`
repository boundary, the internal-live release-evidence gate, and the deferral
of aggregation and web-console integration to separately approved changes.

**Why this priority**: These are governance ratifications that unblock and
constrain successor changes; they carry no runtime code and can be verified last
without blocking the contract kernel itself.

**Independent Test**: Confirm the repo-boundary delta ratifies a private,
independently released client repository forbidden from holding provider keys or
server tool handlers; that client release-evidence obligations activate at the
internal-live gate; and that aggregation and web-console integration are
deferred to dedicated changes.

**Acceptance Scenarios**:

1. **Given** the successor creates `xfactory-avatar-client`, **When** boundary
   validation runs, **Then** it must be private and independently releasable,
   name openxFactory as contract and server-control owner, and contain no
   provider keys or server tool handlers. *(traces RBG-001-S01)*
2. **Given** privileged provider code is proposed in the client, **When**
   boundary validation runs, **Then** it is rejected and routed to the server
   trust boundary. *(traces RBG-001-S02)*
3. **Given** a proposal to pin `xfactory-avatar-client` into the aggregation or
   to start a web operations console, **When** it is raised, **Then** it must be
   a dedicated change with its own path, pin, and rollback record. *(traces
   RBG-003-S01, RBG-003-S02)*

---

### Edge Cases

- **Reserved identifiers**: AVC-09 and AVC-10 remain reserved and their
  identifiers are never reused; AVC-03 (capabilities) is absorbed inline on
  AVC-02 grants and AVC-05 (transcript segment) is a registered AVC-04 payload.
- **Reserved speech gate**: a policy resolving to `pre_speech_review` fails
  preflight into an approved text or human-handoff fallback rather than
  streaming unreviewed audio. *(traces ACR-008-S03)*
- **Reserved retention classes**: full transcript, audio, video, and independent
  transcription are forbidden in this kernel and ratifiable only by a successor
  change. *(traces ACR-010-S02)*
- **Memory-consent misuse**: a memory-gateway consent profile offered as media
  authority without a consent-authority adapter proving the avatar purpose IDs
  is refused. *(traces ACR-008-S02)*
- **Bundle-identity disagreement**: any mismatch among manifest version,
  changelog, tag, commit, and digests fails release validation. *(traces
  SCO-001-S02)*
- **Tag-only pin**: a consumer that pins a tag without commit and digests fails
  conformance. *(traces SCO-001-S03)*
- **Push-to-talk request**: a profile requesting push-to-talk fails preflight
  because the required provider events are outside the two-event client
  allowlist. *(traces ACR-003-S08)*
- **Bounded test sentinel**: a synthetic secret/SDP sentinel used inside a
  fixture must stay within its declared bounded form; a sentinel that widens into
  a real credential/SDP pattern fails the content scan rather than bypassing it.
- **Evidence register gap**: a manual scenario with no recorded result or a
  disposition that skips an allowed status transition fails validation as
  evidence-free.
- **F0 evidence shape mismatch**: an `f0-results` or `f0-interface-impact`
  instance that fails validation against the pinned F0 schema, or whose source
  commit or schema digest does not match the pinned values, blocks the tag
  (fail-closed) even if it claims `PASS`.

## Requirements *(mandatory)*

### Functional Requirements

#### Contract kernel surface (traces ACR-001, ACR-002, ACR-008)

- **FR-001**: The feature MUST publish exactly eight neutral avatar-client
  contracts under `contracts/avatar-client/` — AVC-01 session request, AVC-02
  discriminated session result, AVC-04 session event, AVC-06 structured
  confirmation, AVC-07 retention profile, AVC-08 persona profile, AVC-11 session
  command, and AVC-12 state snapshot — each declaring its contract identifier and
  contract schema version. For AVC-07 and AVC-08 the feature MUST ship the schema
  plus conformance fixtures only and MUST NOT ship live persona/retention
  instances, illustrative examples, or `.template.yaml` stubs, which remain
  domain-owned. *(Q2)*
- **FR-002**: The feature MUST absorb AVC-03 (capabilities inline on AVC-02
  grants) and AVC-05 (transcript segment as a registered AVC-04 event payload),
  and MUST keep AVC-09 and AVC-10 reserved with their identifiers never reused.
- **FR-003**: All contracts MUST share one common definitions module referenced
  by cross-reference, covering at minimum actor/client/subject context, workflow
  purpose, consent reference/version/required purpose IDs, trace, session epoch,
  media leg and attempt, the server-derived SDP-offer fingerprint, state
  revision, last-event sequence, media authorization, session outcomes, retention
  class, redaction, and the retry-equivalence rule.
- **FR-004**: The feature MUST publish closed, versioned registries for
  session-result reasons, events, commands, retention classes, capabilities,
  interaction modes, session outcomes, and fallback modes; the session-result
  reason registry MUST contain exactly the fifteen enumerated reasons
  (`identity_denied`, `consent_missing`, `policy_denied`,
  `contract_incompatible`, `profile_disabled`, `interaction_mode_unsupported`,
  `quota_blocked`, `second_instance_denied`, `idempotency_conflict`,
  `media_readiness_timeout`, `provider_unavailable`, `grant_consumed`,
  `attempt_expired`, `attempt_abandoned`, `attempt_revoked`).
- **FR-005**: The feature MUST publish the neutral consent-purpose registry
  containing exactly `avatar.media_capture`, `avatar.provider_processing`, and
  `avatar.structured_record`, carrying only consent record reference, version,
  and required purpose IDs in the contracts. *(traces ACR-008)*
- **FR-006**: Provider DTOs, model identifiers, client widget state, and secrets
  MUST NOT be required neutral fields in any contract.
- **FR-007**: The AVC-02 contract MUST discriminate `grant`, `denial`, and
  `terminal` results and MUST make it structurally invalid for a denial or
  terminal result to carry SDP, an SDP answer, or a credential. *(traces
  ACR-002-S09)*
- **FR-008**: Unknown commands, authoritative events, lifecycle states, and
  confirmation decisions MUST fail closed, and additive optional fields MUST
  follow the declared compatibility policy. *(traces ACR-001-S01, ACR-001-S03)*

#### Encoded session and authority semantics (traces ACR-002 – ACR-011)

- **FR-009**: The contracts MUST encode authenticated, purpose-bound session
  semantics — request idempotency identity, exact server-derived offer-fingerprint
  retry equivalence, held offer-bound answers on grants, and credential-free
  non-grant outcomes — such that canonical fixtures for the ACR-002 scenarios
  validate and adversarial fixtures are rejected.
- **FR-010**: The contracts MUST encode brokered-media and sideband-before-answer
  ordering as expressible fields — media-authorization state, readiness-timeout
  bounds (1,000–5,000 ms), and offer-fingerprint binding — traceable to ACR-003,
  with the executable broker owned by the reference-runtime sibling.
- **FR-011**: The contracts MUST encode single-log command, event, and snapshot
  authority — one sequenced authoritative log, observation-versus-authoritative
  producer classification, revision guards, and the snapshot barrier with
  `last_event_sequence` — traceable to ACR-004.
- **FR-012**: The contracts MUST encode leased-control and deterministic-recovery
  fields — heartbeat interval (>0 and ≤5,000 ms), lease ceilings (≤10,000 ms after
  grant or heartbeat), session epoch, and last-applied sequence — traceable to
  ACR-005.
- **FR-013**: The contracts MUST encode effect-bound confirmation — an AVC-06
  challenge bound to confirmation ID, version, scope, effect summary, risk class,
  policy/consent versions, expiry, and issuing revision, with the AVC-11 decision
  carrying only confirmation ID, version, decision, and command ID, and no binding
  digest required — traceable to ACR-006.
- **FR-014**: The contracts MUST encode server-owned model-profile indirection and
  session-fixed persona — logical capabilities requested, no model or provider
  identifiers as required neutral fields, immutable per-session persona — traceable
  to ACR-007.
- **FR-015**: The contracts MUST encode consent-before-capture and speech-gate
  semantics — the three consent purposes, the reserved `pre_speech_review` gate,
  and consent-revocation fields — traceable to ACR-008.
- **FR-016**: The contracts MUST encode disposable provider context and
  reference-only attachments (opaque authorized attachment reference and
  display-safe metadata only) traceable to ACR-009.
- **FR-017**: The contracts MUST encode minimal retention classes with reserved,
  forbidden classes (full transcript, audio, video, independent transcription) and
  no local persistence of sensitive session data, traceable to ACR-010.
- **FR-018**: The feature MUST enforce redaction in two layers: (1) **structural**
  — the schemas make a credential, SDP, raw transcript, raw media, or prohibited
  high-cardinality identifier structurally invalid wherever prohibited, so a
  secret-carrying artifact cannot validate; and (2) **content scan** — the
  validator scans committed fixtures and evidence against a denylist of
  credential, SDP, raw-payload, transcript/media, and prohibited
  high-cardinality-identifier patterns. Synthetic test sentinels MUST be
  explicitly bounded so they cannot become a bypass for real secret patterns.
  *(traces ACR-011; Q3)*

#### Conformance, fixtures, and traceability (traces ACR-012)

- **FR-019**: The feature MUST provide canonical valid, invalid, boundary,
  compatibility, unknown-field, unknown-authority, redaction, and adversarial
  fixtures for every schema and for every ACR-*, SCO-*, and RBG-* scenario owned
  by this change. Fixtures MUST be language-neutral and self-describing — each
  declaring its target schema or registry, its expected valid or invalid result,
  and its stable scenario/evidence ID — so that any conformant JSON Schema draft
  2020-12 implementation can execute them without additional coordination.
  *(traces ACR-012; Q5)*
- **FR-020**: The feature MUST provide `scripts/validate-avatar-client.py`, which
  validates schemas, cross-references, closed registries, fixtures, acceptance-map
  parity, evidence-register completeness and status transitions, secret exclusion
  (structural plus content scan per FR-018), and interface-lock consistency, and
  MUST fail on any missing, duplicate, renamed, or evidence-free normative
  requirement or scenario. The validator is the reference runner for the
  self-describing fixtures; it is reproducible reference tooling and MUST NOT be a
  required dependency for a consumer to prove conformance. *(traces ACR-012-S03;
  Q4, Q5)*
- **FR-021**: The feature MUST publish a complete acceptance map using stable
  ACR-*, SCO-*, and RBG-* identifiers, each naming its owning task, fixture or
  manual evidence ID, release ring, and status, covering every normative
  requirement and scenario across the three capability deltas. *(traces ACR-012)*
- **FR-032**: The feature MUST publish one consolidated, content-addressed
  evidence/disposition register under `contracts/avatar-client/` that resolves
  every acceptance-map scenario to evidence: `automated` scenarios name their
  fixture evidence; `manual` scenarios carry a recorded result plus
  reviewer/disposition fields; and `live_f0` and successor scenarios name the
  owning change plus the fail-closed default that remains active until that owner
  lands. The validator MUST check the register for completeness, allowed status
  transitions, and referenced-artifact existence, and MUST fail on a missing or
  evidence-free entry. *(traces ACR-012; Q1, Q4)*

#### Release governance and ownership (traces SCO-001, SCO-002)

- **FR-022**: openxFactory MUST be ratified as the canonical owner of the AVC
  contract kernel; each published bundle MUST have one matching manifest version,
  changelog entry, annotated tag, exact release commit, and per-file digests, all
  identifying the same realized bundle, or release validation fails. The digested,
  manifest-registered bundle MUST comprise the full consumed set — the eight
  schemas, the shared definitions, every closed registry, the consent-purpose
  registry, the canonical fixtures, the acceptance map, the interface lock, and
  the consolidated evidence/disposition register (FR-032) — with a per-file
  SHA-256 digest on each entry; `scripts/validate-avatar-client.py` MUST ship at
  the release commit as reproducible reference tooling but MUST NOT be a pinned
  semantic artifact. *(traces SCO-001-S02; Q1)*
- **FR-023**: Consumers MUST pin the exact openxFactory commit plus per-file
  digests and prove conformance by executing the canonical fixtures of the pinned
  release with any conformant JSON Schema draft 2020-12 implementation; a tag-only
  pin MUST fail conformance, and proving conformance MUST NOT require the kernel's
  Python validator. *(traces SCO-001-S03, SCO-001-S04; Q5)*
- **FR-024**: The contract bundle version MUST be allocated only at realization
  (next available minor after merge order is known), with `contracts/manifest.yaml`,
  `contracts/CHANGELOG.md`, and `contracts/README.md` updated atomically and the
  annotated tag published from the realized release commit.
- **FR-025**: The feature MUST ratify reference and overlay ownership boundaries:
  canonical contracts and non-deployable reference modules belong to openxFactory;
  the distributable client MUST NOT hold provider keys, server tool handlers, or
  server provider configuration; and DomainxFactory overlays MUST NOT fork the
  neutral protocol, authority rules, or canonical vocabulary. *(traces SCO-002)*

#### Repository-boundary governance (traces RBG-001, RBG-002, RBG-003)

- **FR-026**: The feature MUST ratify the future reusable client boundary as a
  private, independently released `xfactory-avatar-client` repository created by a
  successor change, forbidden from holding provider keys, server tool handlers, or
  unpinned copied schemas. *(traces RBG-001)*
- **FR-027**: The feature MUST define client release-evidence obligations that
  activate at the internal-live gate — pinned contract, fixture conformance,
  dependency lock, secret scan, client-integrity evidence, test evidence, and
  rollback target. *(traces RBG-002)*
- **FR-028**: The feature MUST defer aggregation integration and the web operations
  console to separately approved changes, each recording its own path, pin,
  verification, and rollback behavior. *(traces RBG-003)*

#### Publication gate and interface baseline (traces ACR-012, workstream plan)

- **FR-029**: Kernel schema and fixture implementation MAY proceed concurrently
  with F0, but the contract bundle tag MUST remain blocked until F0 evidence is
  `PASS` and every reported interface variance is dispositioned; `FAIL`,
  `INCONCLUSIVE`, or an undispositioned variance blocks the tag but not parallel
  coding. *(traces ACR-012-S02)*
- **FR-030**: The realized field, registry, ordering, timeout, lease, and
  closed-default decisions MUST be frozen in an interface-lock artifact; a baseline
  correction is made only in this change and published to siblings through the
  variance protocol.
- **FR-031**: Before contract publication and annotated tagging, the registered
  threat model MUST be accepted and the F0 protocol MUST produce passing
  machine-readable evidence for answer ordering, sideband-failure containment,
  readiness timing, and five-second hangup; F0 MUST NOT qualify a live model.
- **FR-033**: The F0 evidence schemas `f0-results.schema.yaml` and
  `f0-interface-impact.schema.yaml` are owned and versioned by the F0 sibling
  `qualify-avatar-brokered-call-feasibility`; the kernel MUST NOT duplicate or
  co-own them. The kernel publication gate MUST pin the exact F0 source commit and
  both schema digests, validate the consumed evidence instances against those
  pinned schemas before reading `PASS` or variance dispositions, and fail closed
  on a missing schema, a digest mismatch, a validation failure, an unknown status,
  or an unknown variance field. *(traces ACR-012-S02; Q6)*
- **FR-034**: The feature MUST distinguish two completion states. It MAY reach
  "implementation complete, publication pending F0" once all kernel artifacts and
  validators are merged and green and the publication gate is enforced. It reaches
  "realized" only when F0 is `PASS`, all variances are dispositioned, the
  annotated tag is published, and the release digests are recorded; the OpenSpec
  change MUST remain active — with its publication and handoff obligations
  incomplete — and MUST NOT be treated as realized or archived at the earlier
  milestone. *(traces ACR-012; Q7)*

### Key Entities

- **AVC contract kernel**: the eight neutral avatar-client contracts (AVC-01,
  -02, -04, -06, -07, -08, -11, -12) that define the canonical avatar-session
  meaning.
- **Shared definitions module**: the single common-definitions artifact
  referenced by every contract, holding the enumerated shared shapes.
- **Closed registries**: versioned enumerations of session-result reasons,
  events, commands, retention classes, capabilities, interaction modes, session
  outcomes, and fallback modes that reject unrecognized values.
- **Neutral consent-purpose registry**: the three ratified avatar consent
  purposes (`avatar.media_capture`, `avatar.provider_processing`,
  `avatar.structured_record`).
- **Canonical fixtures**: language-neutral, self-describing valid, invalid,
  boundary, compatibility, unknown-field, unknown-authority, redaction, and
  adversarial examples — each declaring its target schema/registry, expected
  result, and stable scenario/evidence ID — that consumers run under any
  draft-2020-12 implementation to prove conformance.
- **Avatar-client validator**: `scripts/validate-avatar-client.py`, the reference
  runner and checker for schemas, fixtures, registries, acceptance-map parity, the
  evidence/disposition register, structural-plus-scan secret exclusion, and
  interface-lock consistency; reproducible tooling, not a pinned artifact or a
  required consumer dependency.
- **Acceptance map**: the traceability spine keyed by stable ACR-*/SCO-*/RBG-*
  identifiers, linking each requirement and scenario to task, evidence, release
  ring, and status.
- **Evidence/disposition register**: the consolidated, content-addressed record
  under `contracts/avatar-client/` that resolves each acceptance-map scenario to
  fixture evidence, a recorded manual result with reviewer/disposition, or a named
  owning change plus fail-closed default; carries allowed status transitions the
  validator enforces.
- **Contract bundle release**: the coordinated, content-addressed release identity
  — manifest version, changelog entry, annotated tag, exact commit, and per-file
  digests over the full consumed set (schemas, shared definitions, registries,
  consent-purpose registry, fixtures, acceptance map, interface lock, and evidence
  register).
- **Interface lock**: the frozen record of realized field/registry/ordering/
  timeout/lease/closed-default decisions for the `avatar-client-parallel-v1`
  baseline.
- **F0 feasibility evidence** *(external dependency)*: the sibling
  `qualify-avatar-brokered-call-feasibility` result (`f0-results` and
  `f0-interface-impact` instances) consumed as the publication gate, validated
  against F0-owned schemas the kernel pins by commit and digest.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All eight contracts, the shared definitions module, and the closed
  registries are published under `contracts/avatar-client/` with 100% of
  cross-references resolving (0 unresolved references).
- **SC-002**: The validator passes on 100% of canonical valid fixtures and rejects
  100% of invalid, boundary, unknown-field, unknown-authority, adversarial, and
  redaction-violation fixtures.
- **SC-003**: Every normative requirement and scenario across the three capability
  deltas (17 requirements and 72 scenarios) has exactly one acceptance-map entry
  and a resolving evidence/disposition-register entry (fixture evidence, recorded
  manual result, or named owner plus fail-closed default) — 0 unmapped,
  duplicated, renamed, or evidence-free entries.
- **SC-004**: Every closed registry rejects 100% of unrecognized values; the
  session-result reason registry contains exactly 15 reasons and the
  consent-purpose registry exactly 3 purposes.
- **SC-005**: 0 denial or terminal result fixtures that carry SDP, an SDP answer,
  or a credential pass validation.
- **SC-006**: A released bundle's manifest version, changelog entry, annotated tag,
  release commit, and per-file digests all identify the same realized bundle, every
  file in the full consumed set (schemas, shared definitions, registries,
  consent-purpose registry, fixtures, acceptance map, interface lock, evidence
  register) carries a per-file digest, and a pin recorded as a tag alone fails
  conformance in 100% of checks.
- **SC-007**: 0 bundle tags are published while F0 evidence is absent, `FAIL`, or
  `INCONCLUSIVE`, any interface variance is undispositioned, or the F0 evidence
  fails validation against the pinned F0 schema, source commit, or schema digest.
- **SC-008**: 0 committed contract, fixture, or evidence files pass validation while
  containing credentials, raw provider payloads, SDP, or prohibited
  high-cardinality identifiers, whether via a prohibited field or an unbounded
  synthetic sentinel that widens into a real secret pattern.
- **SC-009**: A consumer pinned to the released kernel can validate its own models
  against the canonical fixtures using only the published commit and per-file
  digests and any conformant draft-2020-12 implementation, with 0 additional
  coordination and without the kernel's Python validator.
- **SC-010**: The publication gate fails closed in 100% of adverse F0 cases — a
  missing pinned schema, digest mismatch, evidence-validation failure, unknown
  status, or unknown variance field — and never treats the change as realized
  before the annotated tag and release digests exist.

## Out of Scope

These belong to sibling and successor changes and MUST NOT be built here:

- **Reference broker/control runtime, authority stub, provider-adapter shape**
  under `xfactory/avatar_runtime/` — owned by `implement-avatar-reference-runtime`.
- **F0 live-API spike, evidence, and interface-impact report** under
  `experiments/avatar-brokered-call/` — owned by
  `qualify-avatar-brokered-call-feasibility`.
- **Avatar-first UI standard, profile schema, template, and examples** — owned by
  `align-avatar-first-ui-standard`.
- **The private Flutter avatar client** (`xfactory-avatar-client`) — created by
  `implement-avatar-client-lab`.
- **Live provider qualification, deployment topology, and latency budgets** —
  owned by `qualify-avatar-live-voice`.
- **Hermes integration, domain adoption, accessibility audit, operations, and
  pilot rollback** — owned by `avatar-pilot-hardening`.
- **Push-to-talk, offline drafts, attachment byte paths, multi-device takeover,
  web-console integration, and GPT-Live adoption** — each a separately approved
  change.
- **Allocating a specific contract bundle version number** — allocated only at
  realization, not fixed by this specification.
- **Concrete persona/retention profile instances, examples, and `.template.yaml`
  stubs** for AVC-07/AVC-08 — domain-owned; the kernel ships only schemas and
  conformance fixtures.
- **Owning or duplicating the F0 evidence schemas** (`f0-results.schema.yaml`,
  `f0-interface-impact.schema.yaml`) — owned/versioned by
  `qualify-avatar-brokered-call-feasibility`; the kernel only pins and validates
  against them.

## Dependencies

- **F0 publication gate**: the annotated contract tag depends on
  `qualify-avatar-brokered-call-feasibility` producing `PASS` evidence and a
  disposition for every reported interface variance. That sibling owns and versions
  the `f0-results.schema.yaml` and `f0-interface-impact.schema.yaml` evidence
  schemas; the kernel pins the exact F0 source commit and both schema digests and
  validates evidence instances against them before honoring the gate. Concurrent
  kernel schema and fixture implementation does not depend on F0 completion.
- **Frozen interface baseline `avatar-client-parallel-v1`**: parallel work begins
  from this baseline (the reviewed `avatar-client-runtime` delta, the threat model,
  and the stable ACR-* identifiers); baseline corrections are made only in this
  change.
- **Repository contract-release policy and constitution Principle VI**: the
  content-addressed, versioned release model (manifest, changelog, annotated tag,
  commit, per-file digests) is inherited from existing openxFactory governance.
- **Registered threat model**: acceptance of `avatar-client-threat-model` is a
  precondition of publication.

## Assumptions

- The eight-contract composition, the absorption of AVC-03/AVC-05, and the reserved
  AVC-09/AVC-10 identifiers are fixed by the ratified OpenSpec change; this feature
  does not revisit contract membership.
- "YAML-serialized JSON Schema (draft 2020-12)" is the ratified artifact format
  (constitution Principle VI and the change), treated here as a binding governance
  requirement rather than a discretionary implementation choice.
- The reference runtime, F0 harness, and avatar-first UI assets are owned by
  sibling changes; this feature owns only the neutral contracts, shared
  definitions, registries, consent purposes, fixtures, the validator, the
  acceptance map, and the release metadata for the kernel bundle.
- The acceptance map's expected counts — 17 requirements and 72 scenarios — are the
  authoritative parity target for the validator.
- Content-addressed pinning (exact commit plus per-file digests over the full
  consumed set) is the sole compatibility mechanism; annotated tags identify a
  release but do not replace the pin, and the Python validator is reference tooling
  rather than a pinned artifact or a required consumer dependency.
- Conformance is portable: fixtures are self-describing and executable by any
  conformant JSON Schema draft 2020-12 implementation (including the Dart client),
  so no consumer needs the kernel's Python toolchain to prove conformance.
- The feature has two completion states; "implementation complete, publication
  pending F0" is a valid terminal state for the Speckit implementation window,
  while the OpenSpec change stays active until the tag and release digests exist.
- The three integration files (`contracts/manifest.yaml`, `contracts/CHANGELOG.md`,
  `contracts/README.md`) are the only intentional shared-write surface for the
  kernel release; the UI sibling touches them only later in its own serialized
  profile-schema release.
- Authoritative runtime behavior described by the encoded semantics (session
  authorization, media authorization, recovery) is exercised by the sibling
  reference runtime; this feature proves the contracts can express and constrain
  that behavior through fixtures and the validator, not by executing a broker.
