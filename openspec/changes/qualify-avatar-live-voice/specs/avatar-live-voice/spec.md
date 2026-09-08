# avatar-live-voice (delta) — qualify-avatar-live-voice

## ADDED Requirements

### Requirement: AVC-09 avatar voice adapter descriptor
openxFactory SHALL publish AVC-09, the avatar voice adapter descriptor, as a
YAML-serialized JSON Schema under `contracts/avatar-client/` carrying the
identifier and `contract_schema_version` discipline every avatar-client
contract carries, sharing definitions through
`shared-definitions.schema.yaml`, and registered in `contracts/manifest.yaml`
under the repository contract changelog policy.

AVC-09 SHALL distinguish server and client adapter components and SHALL
record adapter identifier and version, provider, supported profiles,
requested model alias or snapshot, provider-resolved model, prompt, policy,
voice and turn configuration versions, capability and event mapper versions,
authorization mode, sideband readiness, direct-media requirement, contract
compatibility, region and data controls, and experimental, candidate,
approved or retired status. The descriptor SHALL carry adapter STATUS and
recorded latency evidence references; it MUST NOT carry a numeric latency
budget field, because the gating latency rule is the neutral
relative-regression SLO rather than a per-profile ceiling frozen into a
neutral contract. AVC-09 MUST NOT carry a provider key, an ephemeral client
secret, raw session content, or any other secret material.

The descriptor's authorization mode for the internal-live ring SHALL record
that the session broker holds the provider server key end-to-end and that no
standard provider API key and no ephemeral client secret is issued to the
client. The descriptor SHALL be the single home for the ring's declared
region and data-control values.

#### Scenario: An adapter descriptor is authored for the internal-live ring
- **WHEN** `gpt-realtime-2.1` is described for internal-live qualification
- **THEN** AVC-09 MUST record its provider, resolved model, authorization mode, sideband readiness, direct-media requirement, region and data controls, and candidate status
- **AND** the descriptor MUST reference its measured latency evidence rather than restating a numeric budget

#### Scenario: A numeric latency budget is proposed as a descriptor field
- **WHEN** a per-profile absolute latency ceiling is offered as an AVC-09 field
- **THEN** the addition MUST be refused, because latency gating lives in the neutral relative-regression SLO and the measured numbers live in AVC-10 samples

#### Scenario: Secret material is offered to the descriptor
- **WHEN** a descriptor instance would carry a provider key, an ephemeral client secret, or raw session content
- **THEN** contract validation MUST fail and the instance MUST NOT be published

### Requirement: AVC-10 avatar voice latency sample
openxFactory SHALL publish AVC-10, the avatar voice latency sample, as a
YAML-serialized JSON Schema under `contracts/avatar-client/` carrying the
same identifier, version, shared-definition and manifest-registration
discipline as every other avatar-client contract.

AVC-10 SHALL carry sample, session, media-leg and turn identity, adapter and
profile, platform, network, region, clock source and clock quality, monotonic
markers, derived intervals, direct-or-brokered reference classification, and
a reproducible fixture reference. Markers SHALL cover broker request,
provider call, sideband ready, media connected, speech, first audio,
playback, interruption, command, tool outcome, recovery, and teardown. A
sample MUST contain no raw content and no secrets.

The direct-or-brokered reference classification SHALL be the field that
distinguishes a direct-provider reference sample from a governed-adapter
sample, and the relative-regression SLO SHALL be evaluated only between
samples whose platform, network, and region agree.

#### Scenario: A latency sample is recorded for a governed adapter run
- **WHEN** the governed adapter completes an instrumented internal-live session
- **THEN** AVC-10 samples MUST carry the monotonic markers and derived intervals for that session classified as brokered, with a reproducible fixture reference

#### Scenario: A regression is computed across mismatched conditions
- **WHEN** an adapter sample on one platform is compared with a reference sample from another platform, network, or region
- **THEN** the comparison MUST be refused as evidence, because the SLO is defined only within a matching cell

#### Scenario: A sample would carry content
- **WHEN** a latency sample would embed transcript text, media, SDP, or a credential
- **THEN** validation MUST fail and the sample MUST NOT be published

### Requirement: Internal-live activation gate is the kernel's four-element ring
The internal-live activation gate for a live provider profile SHALL be the
kernel's four-element ring and nothing wider: live provider qualification
plus secret scan, telemetry-redaction verification, kill-switch proof, and
measured latency evidence. Those four elements SHALL be the binding exit
contract, each with a stable acceptance-map entry naming its owning task,
evidence identifier, release ring, and status.

The eight-condition GPT-Live-1 activation list SHALL be reused as the mapped
preflight and canary checklist that PRODUCES that evidence, and SHALL NOT
itself become the exit contract. Conditions 1, 2, 3 (topology), 4, and the
deterministic halves of 5 and 7 SHALL be hard preflight blockers; the live
domain-voice evaluation in condition 5, the live cross-domain safety,
exact-value, consent, handoff and blocked-state evaluations in condition 7,
the measured latency figure in condition 3, and the opt-in canary in
condition 8 SHALL be canary-time checks; the kill switches and rollback
machinery underlying condition 8 SHALL be hard preflight blockers, because
they must exist before any canary traffic.

Condition 6 SHALL be reinterpreted for this ring: rather than "meet or
improve on the `gpt-realtime-2.1` baseline", which is circular when
`gpt-realtime-2.1` is the candidate, the internal-live analogue SHALL be "no
material regression against the direct-provider reference" as defined by the
neutral relative-regression SLO. Every replace-the-current-primary and
default-swap semantic in the eight-condition list SHALL remain reserved to
the separately approved GPT-Live adoption change, and passing this gate MUST
NOT be read as promoting a profile to the production default.

#### Scenario: The eight-condition list is offered as the exit contract
- **WHEN** a reviewer proposes that all eight GPT-Live-1 conditions literally bind internal-live qualification
- **THEN** the proposal MUST be refused, because the binding exit contract is the four-element ring and the eight conditions are the checklist that produces its evidence

#### Scenario: A canary opens before the kill switches exist
- **WHEN** canary traffic is proposed while the all-new-session and per-model-profile kill switches or the rollback path are unproven
- **THEN** the gate MUST remain closed, because kill-switch proof is a hard preflight element of the ring

#### Scenario: Condition 6 is applied literally to the candidate
- **WHEN** the gate is evaluated with condition 6 read as a comparison against `gpt-realtime-2.1` itself
- **THEN** the evaluation MUST use the no-material-regression-against-the-direct-provider-reference reading instead

#### Scenario: Passing the gate is read as a default swap
- **WHEN** a qualified internal-live profile is proposed as the production primary on this gate's evidence alone
- **THEN** the proposal MUST be routed to the GPT-Live adoption change, which owns all replace-the-primary semantics

### Requirement: Neutral relative-regression latency SLO gates internal-live
A neutral relative-regression SLO SHALL be the hard latency gate for the
internal-live ring, enforced through the acceptance map rather than through a
per-profile numeric budget carried in a neutral contract.

A governed-adapter percentile SHALL be a MATERIAL REGRESSION when it exceeds
the same-platform direct-provider reference percentile by more than 15
percent relative OR by more than 150 milliseconds absolute, whichever is
greater. The rule SHALL be evaluated on the first-playable-after-authorized
and sideband-ready intervals at the p50 and p95 percentiles. The gated
delivery matrix SHALL be Windows desktop and web canvas at nominal network;
Linux CI SHALL be reference-generation only and SHALL NOT be a gated delivery
platform. A material regression on any gated cell SHALL fail promotion to the
internal-live ring.

The p99 percentile, teardown and hangup-to-terminal latency, degraded-network
conditions, and steady-state per-turn speech-to-first-audio latency SHALL be
RECORDED as informational tail evidence and SHALL NOT gate the internal-live
ring; they are candidates to become hard gates at the pilot ring when sample
volume supports them. The five-second revocation bound SHALL remain a
pass-or-fail requirement rather than a budgeted percentile.

#### Scenario: The governed adapter adds a material setup regression
- **WHEN** the adapter's p95 first-playable-after-authorized on a gated cell exceeds the same-platform direct-provider reference by more than 15 percent relative and by more than 150 milliseconds absolute
- **THEN** internal-live promotion MUST fail

#### Scenario: A small absolute regression on a fast interval
- **WHEN** the adapter's p50 exceeds the reference by 18 percent relative but by only 40 milliseconds absolute
- **THEN** the cell MUST pass, because materiality takes the greater of the two thresholds

#### Scenario: A p99 tail moves
- **WHEN** the adapter's recorded p99 or teardown latency regresses
- **THEN** the finding MUST be recorded as informational tail evidence and MUST NOT by itself fail the internal-live gate

#### Scenario: Evidence is offered from a degraded network
- **WHEN** internal-live latency evidence is produced under degraded or jittered network conditions
- **THEN** it MAY be recorded but MUST NOT substitute for the nominal-network gated cells, and no claim of adverse-network validation may be made for this ring

### Requirement: A fresh client-side direct-provider reference is measured before gating
The direct-provider reference baseline SHALL be measured afresh on the real
Flutter client on the gated delivery platforms before any relative-regression
gate is evaluated. The F0 brokered-call feasibility distributions MUST NOT
serve as that reference: they were produced by a single Python and aiortc
harness with no region, on neither gated platform, and the feasibility change
records them as inputs and sanity checks rather than production baselines or
budgets.

Reference and adapter samples SHALL be produced under the same client build,
platform, network class, and region, and SHALL be recorded as AVC-10 samples
carrying the direct-or-brokered classification. The minimum sample count per
gated cell SHALL be declared before measurement begins and recorded with the
evidence, so a percentile is never claimed from a sample too small to support
it.

#### Scenario: F0 numbers are proposed as the baseline
- **WHEN** the F0 harness distributions are offered as the direct-provider reference for the regression gate
- **THEN** they MUST be refused and a same-platform client-side reference MUST be measured on the real client

#### Scenario: A percentile is claimed from an undeclared sample count
- **WHEN** gated latency evidence reports a p95 without a pre-declared minimum sample count recorded alongside it
- **THEN** the evidence MUST be treated as incomplete and the gate MUST remain closed

### Requirement: Broker-held custody with layered fail-closed spend containment
The provider server key for the internal-live ring SHALL be custodied as a
credential binding under the promoted `credential-contracts` binding-template
shape, declaring provider, vault, secret reference, owner, and rotation
policy, resolved only by the session broker, and MUST NOT exist in any
repository in plaintext. The client SHALL never carry a standard provider API
key, and no ephemeral client secret SHALL be issued for the internal-live
ring: the broker holds the server key end-to-end and issues only the
short-lived AVC-02 grant the reference runtime already destroys on connect,
expiry, abandonment, or revocation.

Spend SHALL fail closed at two independent layers. At the SESSION layer the
broker SHALL hard-kill a runaway session synchronously using the already
modeled duration and quota terminal outcome together with the kill switches
and lease revocation, emitting an auditable termination whose reason
distinguishes a cost-triggered kill from an ordinary duration or quota
terminal. At the TENANT and RING layer a dedicated, spend-capped provider
project reserved to internal-live — distinct from the F0 lab project — SHALL
be the hard stop that fails all sessions closed at budget exhaustion.

Asynchronous usage metering and threshold alerting SHALL supply per-tenant
visibility. A durable synchronous per-tenant cumulative-spend counter SHALL
NOT be built by this change; it is an explicit deferral, and until it exists
the provider-project cap SHALL be the only per-tenant hard stop, which SHALL
be recorded as a stated limit of this ring rather than left implied.

#### Scenario: A single session runs away
- **WHEN** an internal-live session exceeds its configured session ceiling
- **THEN** the broker MUST terminate it synchronously through the duration-or-quota terminal outcome with lease revocation, and the record MUST identify the termination as cost-triggered

#### Scenario: The ring exhausts its provider budget
- **WHEN** the dedicated internal-live provider project reaches its configured cap
- **THEN** all further sessions on that project MUST fail closed rather than continue under monitoring

#### Scenario: A client is offered a provider key
- **WHEN** a design would issue a standard provider API key or an ephemeral client secret to the client for the internal-live ring
- **THEN** it MUST be refused, because the broker holds the server key end-to-end for this ring

#### Scenario: Granular per-tenant enforcement is assumed
- **WHEN** a reader assumes hard synchronous per-tenant cumulative-spend enforcement exists at this ring
- **THEN** the record MUST show it deferred, with the provider-project cap named as the only per-tenant hard stop

### Requirement: Evaluation audio stays synthetic and canary audio stays ephemeral
The model-versus-model evaluation corpus for this qualification SHALL be
synthetic. No live audio SHALL be shadowed to a second model, and no
retained-real evaluation corpus SHALL be created by this change.

The opt-in canary MAY carry real consented users on the SINGLE candidate
profile, with processing strictly ephemeral: captions and transcript deltas
fall under the `ephemeral_presentation` class and decisions, consent versions
and outcomes under `structured_record`, and no `full_transcript`, `audio`,
`video`, or `independent_transcription` instance SHALL be created. The four
reserved retention classes SHALL remain forbidden and this change SHALL NOT
unreserve any of them.

Consent SHALL ride the existing three neutral purposes —
`avatar.media_capture`, `avatar.provider_processing`, and
`avatar.structured_record` — with an optional stricter domain purpose
reference; the frozen purpose count SHALL NOT change. Withdrawal SHALL map
onto the existing revoked session outcome and SHALL remain reachable during a
session. Because no schema field today forbids a second-model shadow, the
single-model, ephemeral, never-retained guarantee SHALL be recorded as an
operational control of this ring with the enforcing contract flag named as
deferred work rather than claimed as built.

#### Scenario: A second model is proposed for comparison on live audio
- **WHEN** a design would shadow consented canary audio to a second model for comparison
- **THEN** it MUST be refused; model-versus-model comparison MUST use the synthetic corpus

#### Scenario: A retention class is requested for the evaluation corpus
- **WHEN** the qualification would retain audio, a full transcript, or an independent transcription
- **THEN** the request MUST be refused as a reserved forbidden class, unchanged by this change

#### Scenario: A new consent purpose is proposed for evaluation
- **WHEN** an evaluation-specific consent purpose is proposed to cover qualification audio
- **THEN** it MUST be refused for this ring, which reuses `avatar.provider_processing` with an optional stricter domain purpose reference

#### Scenario: A canary user withdraws consent mid-session
- **WHEN** a consented canary participant withdraws during an active media leg
- **THEN** capture and playback MUST stop, the lease MUST be revoked, the leg MUST terminate to the revoked outcome, and only policy-required records MUST survive

### Requirement: Canary cohort and the recorded revoke-versus-block rollback policy
The internal-live canary cohort SHALL be bounded to the vendor organization's
own internal accounts plus exactly ONE internally-staffed domain sandbox,
using synthetic or internally-consented audio only, with no real external
tenant admitted. Opt-in SHALL be a server-side capability resolution gated to
an allowlisted internal cohort, with the per-session opt-in recorded in the
AVC-01 request context; it SHALL NOT be a client-visible toggle.

The recorded policy the kernel requires for kill-switch scope SHALL be
written and SHALL split three ways. A hard safety or integrity breach — a
revocation-bound violation, a failed blocked-state, exact-value, consent or
handoff safety evaluation, a redaction or secret-scan finding, or a
media-authorization ordering violation — SHALL auto-abort WITH revocation of
active leases. A latency-budget breach under the relative-regression SLO, or
an elevated error or quota condition, SHALL auto-block-new WITHOUT revoking
active leases, letting in-flight legs drain. A quality or cost concern SHALL
be operator-triggered. The operator surface that fires the kill switches
SHALL be named before the canary opens.

Because `gpt-realtime-2.1` is the FIRST qualified live profile, rollback SHALL
disable voice and offer text or human handoff; no model fallback exists and
none SHALL be implied. A rollback SHALL end media only: the workflow
projection is authority-owned and orthogonal to the media plane, so the
canonical logical session and its policy-required records SHALL survive every
abort, and the session outcome each abort path emits SHALL be declared in
advance rather than inferred.

#### Scenario: A safety evaluation fails during the canary
- **WHEN** a blocked-state, exact-value, consent, or handoff evaluation fails, or a redaction or secret-scan finding lands
- **THEN** the canary MUST auto-abort and active leases MUST be revoked under the recorded policy

#### Scenario: The latency budget is breached during the canary
- **WHEN** a gated percentile crosses the material-regression threshold
- **THEN** new sessions on the profile MUST be blocked and in-flight legs MUST be allowed to drain rather than revoked

#### Scenario: Rollback is executed with no prior qualified profile
- **WHEN** the profile is withdrawn and no earlier qualified live profile exists
- **THEN** voice MUST be disabled and text or human handoff MUST be offered, and no model fallback may be presented

#### Scenario: A mid-qualification abort is read as ending the workflow
- **WHEN** a media leg is aborted mid-qualification
- **THEN** the logical session's authority-owned workflow projection and its policy-required records MUST survive, and only the media plane MUST end

#### Scenario: A real external tenant is proposed for the cohort
- **WHEN** admission of a real external customer tenant to the canary is proposed
- **THEN** it MUST be refused and routed to the pilot ring, which owns data-handling review and real-tenant scale

### Requirement: Named deferrals carried by the pilot-hardening successor
The work this ring deliberately does not do SHALL be carried by the
`avatar-pilot-hardening` successor and SHALL be named rather than implied.
That successor SHALL carry the durable synchronous per-tenant cumulative-spend
counter, the retained-real evaluation corpus with the retention-class
unreservation and the evaluation consent surface it requires, the enforcing
contract flag that would make the single-model non-shadowing guarantee
structural rather than operational, and the promotion of p99, teardown,
degraded-network and per-turn conversational latency from recorded evidence
to hard gates.

No deferral in this list SHALL be treated as satisfied by this change, and no
claim of pilot readiness SHALL rest on this ring's evidence: a later ring
requires the prior ring's evidence, and the pilot ring separately owns
threat-model closure, data-handling review, accessibility evidence, and
rollback rehearsal.

#### Scenario: A deferred item is claimed as delivered
- **WHEN** durable per-tenant spend enforcement, a retained-real corpus, a structural non-shadowing flag, or a hard p99 gate is claimed on this change's evidence
- **THEN** the claim MUST be refused and routed to `avatar-pilot-hardening`

#### Scenario: Pilot readiness is asserted from internal-live evidence
- **WHEN** the pilot ring is proposed on this ring's evidence alone
- **THEN** it MUST remain blocked until the pilot ring's own threat-model closure, data-handling review, accessibility evidence, and rollback rehearsal exist
