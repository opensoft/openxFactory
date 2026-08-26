# avatar-client-runtime (delta) — qualify-avatar-live-voice

## MODIFIED Requirements

### Requirement: Versioned neutral avatar-client contract kernel
openxFactory SHALL publish the avatar-client contract kernel under
`contracts/avatar-client/` as YAML-serialized JSON Schema (draft 2020-12)
files: AVC-01 avatar session request, AVC-02 avatar session result (a
discriminated grant, denial, or terminal outcome, with resolved runtime
capabilities inline on grants), AVC-04 avatar session event (with
transcript segments as a registered payload schema), AVC-06 structured
confirmation, AVC-07 avatar retention profile, AVC-08 avatar persona profile,
AVC-11 avatar session command, and AVC-12 avatar state snapshot. AVC-03 and
AVC-05 are absorbed as described; AVC-09 avatar voice adapter descriptor and
AVC-10 avatar voice latency sample are published as defined contracts by the
live-qualification successor change `qualify-avatar-live-voice` under these
same rules, no other reserved identifier is released with them, and no
identifier is ever reused.

Every contract SHALL declare its contract ID and `contract_schema_version`,
share definitions through a single `shared-definitions.schema.yaml`
referenced by `$ref`, and register in `contracts/manifest.yaml` under the
repository contract changelog policy. Realization SHALL allocate the next
available minor bundle version, update the manifest and changelog atomically,
and publish an annotated tag with that version. Consumers SHALL pin the exact
openxFactory commit and per-file digest; a tag alone is insufficient. Shared
definitions SHALL cover actor, client, subject, workflow purpose, consent
record reference/version/required purpose IDs, trace, session epoch, media
leg, media attempt, server-derived SDP-offer fingerprint, state revision,
last-event sequence, session outcomes, retention class, redaction, and the
retry-equivalence rule. Retry equivalence SHALL be canonical-form equality
across every non-volatile request field plus the exact offer fingerprint; only declared
client-observed timestamps MAY be volatile. Provider DTOs, model identifiers,
client widget state, and secrets MUST NOT be required neutral fields.

An unknown command, authoritative event, lifecycle state, or confirmation
decision MUST fail closed. Provider-specific unknown observations MUST remain
non-authoritative until a reviewed mapper handles them. Additive optional
fields SHALL follow the declared compatibility policy.

#### Scenario: Compatible binding reads an additive contract
- **WHEN** a consumer pinned to the same contract major receives a fixture containing a supported additive optional field
- **THEN** it MUST preserve or ignore the field according to contract policy without changing canonical behavior

#### Scenario: Consumer receives an incompatible major
- **WHEN** a client or broker cannot satisfy the required contract major
- **THEN** session preflight MUST fail before media or governed commands are enabled

#### Scenario: Consequential vocabulary is unknown
- **WHEN** a consumer receives an unknown command, authority-bearing event, confirmation decision, or lifecycle state
- **THEN** it MUST reject the transition, request a current snapshot or handoff, and MUST NOT infer a permissive meaning

#### Scenario: A live contract identifier leaves the reserved set
- **WHEN** `qualify-avatar-live-voice` publishes AVC-09 and AVC-10
- **THEN** the interface lock MUST move exactly those two identifiers from `reserved_identifiers` into `frozen.contracts`, leaving AVC-03 and AVC-05 reserved
- **AND** a request to release any further reserved identifier MUST be refused as outside this change

### Requirement: Server-owned model profiles and session-fixed persona
The client SHALL request logical capabilities and SHALL branch only on the
grant's resolved capabilities and canonical state; model and provider
identifiers stay in server profiles. Profile promotion SHALL be
configuration-controlled, human-approved, and new-session-only, recording
requested and provider-resolved model per session. `gpt-realtime-2.1` SHALL be
the initial F0 candidate but MUST remain disabled for internal-live and
production sessions until `qualify-avatar-live-voice` records approved
promotion evidence. This kernel therefore defines no qualified live provider
profile. Recorded approved promotion evidence SHALL qualify `gpt-realtime-2.1`
for the internal-live ring only: the profile becomes selectable in that ring
and MUST NOT thereby become the production default primary, which stays a
separate ruling reserved to the GPT-Live adoption change. All other profiles, including `gpt-live-1`, SHALL remain disabled
pending supported API contracts and their own qualification. Once a qualified
profile exists, rollback SHALL select the last qualified profile; if none
exists, rollback SHALL disable voice and offer text or handoff. A running media
leg MUST NOT silently change model, voice, adapter, or immutable provider
configuration.

Persona SHALL be selected at session start from the domain catalog and
remain fixed for the logical session; changing persona SHALL end the session
and start a new one. Voice SHALL be fixed per media leg. Mid-session persona
rotation is deferred.

#### Scenario: Qualified default model changes
- **WHEN** a new provider profile passes promotion
- **THEN** new sessions MUST use the approved profile without model-name branches in client widgets or neutral reducers

#### Scenario: Candidate model has not passed live qualification
- **WHEN** an internal-live or production session requests `gpt-realtime-2.1` before approved promotion evidence exists
- **THEN** preflight MUST keep live voice disabled and offer the approved text or handoff fallback

#### Scenario: Future model lacks API support
- **WHEN** a target model has no supported deployment API or required control behavior
- **THEN** its profile MUST remain disabled and the system MUST use the last qualified profile or disable voice when no qualified profile exists

#### Scenario: User asks to change persona mid-session
- **WHEN** an active logical session receives a persona-change request
- **THEN** the client MUST offer to end the session and start a new one with the requested persona and MUST NOT rotate persona in place

#### Scenario: Internal-live qualification is read as production promotion
- **WHEN** approved internal-live promotion evidence exists for `gpt-realtime-2.1` and a production session requests it as the default primary
- **THEN** the request MUST be refused, because internal-live qualification confers a selectable internal-live profile and no production default

### Requirement: Redacted telemetry and latency evidence
Telemetry SHALL support end-to-end correlation across client, broker,
sideband, authority stub, and provider references without persisting raw
media, transcript content, SDP, credentials, arbitrary subject identifiers,
or unbounded high-cardinality payloads; a log, trace, metric, crash report,
or support bundle containing such content MUST fail validation and MUST NOT
be published. Latency evidence in this kernel SHALL be structured logging
with monotonic timestamps for broker setup, sideband attach, media
connected, and recovery, informed by the F0 spike; the formal AVC-10 latency
contract and pilot latency budgets belong to the live-qualification
successor change `qualify-avatar-live-voice`, and a live pilot MUST NOT
proceed without approved measured budgets from that change. Internal-live
latency evidence SHALL be AVC-10 samples measured against a same-platform
client-side direct-provider reference and judged by the neutral
relative-regression rule that change publishes; the F0 spike's harness
distributions MUST NOT serve as that reference.

#### Scenario: Telemetry attempts to include protected content
- **WHEN** a telemetry artifact contains a credential, SDP, raw transcript, raw media, or prohibited identifier
- **THEN** validation MUST fail and the artifact MUST NOT be published

#### Scenario: Live pilot is proposed without budgets
- **WHEN** no approved measured latency and recovery budgets exist
- **THEN** the live pilot gate MUST remain blocked

#### Scenario: F0 spike figures are offered as the latency reference
- **WHEN** internal-live latency evidence names the F0 harness distributions as its direct-provider reference
- **THEN** the evidence MUST be rejected and a same-platform client-side reference MUST be measured instead
