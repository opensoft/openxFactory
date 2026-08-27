---
code_surface: openxFactory, openAvatar (the extraction happened 2026-08-03 as DTN-022 → opensoft/openAvatar; recognized by Brett's 2026-08-27 ruling) (openxFactory — the ADDED AVC-09 voice-adapter-descriptor and AVC-10 voice-latency-sample schemas under `contracts/avatar-client/` with their positive and negative examples, the `interface-lock.yaml` unreservation of exactly those two identifiers, the acceptance-map entries for every requirement and scenario below, `scripts/validate-avatar-client.py`'s rules for the two new contracts and for the neutral relative-regression SLO entry, and the credential-binding record for the broker's server key; openAvatar — the private, independently releasable client repository ALREADY EXTRACTED from codexFactory `apps/avatar-client-lab/`, its live `avc_adapters_live` transport realizing the `SessionTransport` port, and its AVC-10 latency instrumentation on the gated platforms). NOT this change's surface: admitting `openAvatar` to the xFactory aggregation, which was a separate reviewed act under `repo-boundary-governance` and is already recorded in the aggregation's `.gitmodules`; creating `openAvatar-server`, the named future home for deployable avatar server code, which only the change that first ships such code may create; the GPT-Live-1 default swap; and every item this proposal names as deferred to `avatar-pilot-hardening`.
target_release: implementation_pending — the requirements land now; realization runs post-ratification against a NAMED INTERNAL-LIVE RELEASE, not the plain main line, because this change's whole content is a release-ring qualification. This surface also moves contract bytes: AVC-09 and AVC-10 are new schemas under `contracts/avatar-client/`, so realization cuts the next additive contract bundle per `docs/contract-versioning-policy.md` and the bundle number is fresh-counted at realization rather than allocated here. The archive gate is merge-plus-green internal-live realization evidence — the four-element ring closed with real evidence (secret scan, telemetry-redaction verification, kill-switch proof, and measured latency evidence from the real Flutter client on the gated platforms) — never on landing alone.
Status: ratified
Ratified: 2026-08-27 by Brett Heap — in-session, ruled "ratify avatar" after the eight fork/latent rulings of 2026-08-26 landed as this change's locked decisions (PR #31, PR #384).
---

# Proposal: qualify-avatar-live-voice

## Why

**This is the change that turns on real voice.** Everything before it was
built to prove that it could be turned on without turning it on. The offline
client lab answered *does the interaction work for the user* against replayed
fixtures with no live model. The F0 brokered-call spike answered *is the
OpenAI-brokered WebRTC handshake feasible* — and answered it under disposable
lab conditions with generated audio, no tenant data, and a boundary written
into its own spec refusing to let its PASS enable anything. The contract
kernel deliberately left AVC-09 and AVC-10 reserved, left latency as
structured logging, and named this change as the owner of the formal latency
contract, the production deployment home, and live-profile promotion.

So the seam is clean and every predecessor has pointed at this door. What has
been missing is not evidence — it is **decisions**. The staged topic declared
itself "not yet ready to propose" behind five forks, each of which had to be
ruled before a single requirement could be written: where the broker's server
key lives and whether a cost cap fails a session closed; which percentiles
gate against which matrix at what magnitude of regression; whether the
eight-condition GPT-Live-1 activation gate binds a candidate it was not
written for; whether qualification audio may ever be real; and how a canary is
cohorted and rolled back. A staged decision memo researched all five against
the sources and surfaced three latent decisions the rulings would implicate.

**Brett Heap ruled all eight on 2026-08-26.** That is what unblocks this
change, and this proposal exists to carry those rulings into contract text
before the shape of them is lost.

There is also a fact the rulings force into the open: the client's ratified
home is codexFactory `apps/avatar-client-lab/`, the standalone-repository
wording activates at the internal-live gate, and **no change had ever been
named as the extractor**. Latent decision 1 names this one. Without that
ruling the internal-live gate would have opened against a repository boundary
that canon requires and nobody owns.

Origin: staged topic `openxFactory:staging:qualify-avatar-live-voice`, its
Exit, executed on the 2026-08-26 rulings recorded in its
`fork-decision-memo.md`.

## What Changes

- **ADD the neutral `avatar-live-voice` capability** — nine requirements: the
  AVC-09 adapter descriptor; the AVC-10 latency sample; the internal-live
  activation gate as the kernel's four-element ring with the eight conditions
  reused as its mapped checklist; the neutral relative-regression latency SLO;
  the fresh client-side direct-provider reference baseline; broker-held
  credential custody with layered fail-closed spend containment; synthetic
  evaluation audio with a strictly ephemeral consented canary; the canary
  cohort and the recorded revoke-versus-block rollback policy; and the named
  deferrals the pilot-hardening successor carries.

- **MODIFY three `avatar-client-runtime` requirements.** The kernel
  requirement releases AVC-09 and AVC-10 from the reserved set — and only
  those two, leaving AVC-03 and AVC-05 reserved. The model-profile requirement
  records that approved promotion evidence qualifies `gpt-realtime-2.1` for
  the internal-live ring ONLY and never makes it the production default. The
  telemetry requirement records that AVC-10 now exists and that internal-live
  latency evidence is judged by the neutral relative-regression rule against a
  same-platform client-side reference — never against F0's harness figures.

- **MODIFY the two repository-boundary requirements the extraction ruling
  touches.** `repo-boundary-governance`'s avatar-client boundary named
  `implement-avatar-client-lab` as the repository's creator; that change
  archived without creating it, having ratified the codexFactory lab home
  instead. This change is named as the extractor at the internal-live gate,
  and `avatar-client-lab`'s ownership requirement records the same move from
  the lab side. Aggregation admission stays a separate reviewed change,
  unchanged.

- **Two reserved identifiers move, and nothing else does.** No retention class
  is unreserved. The frozen consent-purpose count of three does not change.
  No new consent purpose, no new credential family, no new kill switch, no
  second workflow session, and no media proxy.

## The eight locked decisions

Each was RULED 2026-08-26 by Brett Heap in session, recorded in the staged
`fork-decision-memo.md` (now this change's `supporting-docs/fork-decision-memo.md`).
They are inputs to this proposal, not open questions, and this change does not
re-litigate them. A ruling on an option also ratified that option's named-gap
assumptions as the memo recorded them per fork.

**F1 — Credential custody and spend cap: Option C, layered hard-closed.**
The broker's server key is vaulted under the promoted credential-binding
shape, broker-resolved, never in a repository; the client carries no provider
key and no ephemeral client secret is issued for this ring. Spend fails closed
at two independent layers: session hard-kill in the broker on the ALREADY
MODELED duration-and-quota terminal outcome plus kill switches and lease
revocation, and a dedicated spend-capped internal-live provider project — 
distinct from the F0 lab project — as the hard per-tenant and per-ring stop.
Asynchronous usage metering and alerting carry visibility. The durable
synchronous per-tenant cumulative-spend counter is an EXPLICIT deferral: it
has no home in any current contract and would be net-new infrastructure the
reference runtime deliberately does not have.

**F2 — Latency budget derivation: Option C, two-tier, with the materiality
threshold RATIFIED AS PROPOSED.** A neutral relative-regression SLO is the
hard gate; per-profile measured numbers are recorded in AVC-10 and surfaced in
AVC-09 as evidence, not as a gating budget field. The ratified number: a
percentile is a material regression when it exceeds the same-platform
direct-provider reference by more than **15 percent relative OR more than 150
milliseconds absolute, whichever is greater**, on
first-playable-after-authorized and sideband-ready. Hard gate = p50 and p95 on
Windows desktop and web canvas at nominal network. p99 and teardown are
recorded, not gated.

**F3 — Activation-gate scope: Option C.** The kernel's four-element ring is
the binding exit contract. Conditions 1-5, 7 and 8 are reused as the mapped
preflight and canary checklist exactly per the memo's per-condition
classification; condition 6 is reinterpreted as "no material regression
against the direct-provider reference" with the number owned by F2; every
replace-the-primary semantic is reserved to the GPT-Live adoption change.

**F4 — Consent and data control for evaluation audio: Option C.** The
evaluation corpus is synthetic. The opt-in canary MAY carry real consented
users on the single candidate with strictly ephemeral processing —
`ephemeral_presentation` and `structured_record` only — nothing retained,
nothing shadowed to a second model. The retained-real corpus and the
retention-class unreservation are deferred.

**F5 — Canary cohorting and rollback: Option B.** Cohort is the vendor
organization plus ONE internally-staffed domain sandbox, synthetic or
internally-consented audio only. The written revoke-versus-block policy is
ratified as a three-way split: hard safety and integrity breaches auto-abort
WITH active-lease revocation; latency-budget breaches auto-block-new and let
in-flight legs drain; quality and cost breaches are operator-triggered.
Rollback target is disable-voice into text or handoff — `gpt-realtime-2.1` is
the first qualified profile, so no model fallback exists.

**Latent 1 — This change owns the extraction, and it is already done.**
`qualify-avatar-live-voice` owns the client extraction from codexFactory
`apps/avatar-client-lab`; no predecessor change is required. Brett's ruling of
2026-08-27 records that the extraction ALREADY HAPPENED, on 2026-08-03, as
DTN-022's subtree split into `opensoft/openAvatar` with full history — so this
change recognizes `openAvatar` as the extracted client rather than creating a
second repository, and canon's earlier `xfactory-avatar-client` name (which
predates openAvatar becoming a first-class product) is amended to it. Adding
the repository to the aggregation was likewise a separate reviewed act, already
recorded in the aggregation's `.gitmodules`.

**Latent 2 — `avatar-pilot-hardening` carries the deferrals.** Confirmed as
the carrier of both F1's durable per-tenant counter and F4's retention-class
unreservation with its retained-real corpus.

**Latent 3 — No auto-promotion to production default.** Internal-live
qualification yields a selectable, internal-live-only profile. Promotion to
the production default primary is a separate future ruling, consistent with
F3's reservation of replace-the-primary semantics.

## Capabilities

### New Capabilities

- `avatar-live-voice`: the neutral internal-live qualification contract for a
  live avatar voice provider — the AVC-09 adapter descriptor and AVC-10
  latency sample as defined contracts, the four-element activation ring with
  the eight-condition list demoted to its evidence-producing checklist, a
  relative-regression latency SLO enforced through the acceptance map rather
  than a frozen numeric budget, broker-held custody with two independent
  fail-closed spend layers, synthetic evaluation audio with an ephemeral
  single-model consented canary, a written revoke-versus-block rollback
  policy with disable-voice as the only rollback target, and the deferrals
  named rather than implied.

### Modified Capabilities

- `avatar-client-runtime`: three MODIFIED requirements — the reserved-set
  release of AVC-09 and AVC-10, the internal-live-only reading of approved
  promotion evidence, and the latency-evidence rule that refuses F0's figures
  as the reference. Each restates its promoted canon in full and amends only
  the sentences the rulings touch.
- `repo-boundary-governance`: one MODIFIED requirement — the avatar-client
  repository boundary, whose repository is named `openAvatar` and whose
  creation is recorded as DTN-022's 2026-08-03 extraction per latent decision
  1 and Brett's 2026-08-27 ruling, and which now records `openAvatar-server`
  as the named future home for deployable avatar server code. The
  deferred-aggregation requirement is renamed with the rest of canon and
  otherwise NOT touched.
- `avatar-client-lab`: one MODIFIED requirement — the ownership boundary,
  recording that the codexFactory home held until extraction and that DTN-022
  performed that extraction into `openAvatar`.

## Impact

- **New contract bytes**: AVC-09 and AVC-10 schemas, their examples, the
  interface-lock unreservation, acceptance-map entries, and validator rules.
  Realization cuts the next additive contract bundle; the number is
  fresh-counted at realization.
- **Recognized repository, not a new one**: `openAvatar`, private and
  independently releasable, extracted from codexFactory
  `apps/avatar-client-lab/` on 2026-08-03 under DTN-022, holding
  no provider key and no server tool handler. Its release evidence
  obligations activate AT this gate, not at creation. The parked empty
  `opensoft/xfactory-avatar-client` repository was deleted 2026-08-27 with
  nothing referencing it. `openAvatar-server` is recorded as the NAMED FUTURE
  HOME for deployable avatar server code; it is created only by whichever
  change first ships such code, and not by this one.
- **Consumes as preconditions, does not re-prove**: the released, code-signed
  Flutter client from `implement-avatar-client-lab` with its fail-closed
  `SessionTransport` seam; the contract kernel pinned at exact commit,
  per-file digest and interface-lock digest; and the recorded F0 overall PASS
  with its accepted threat model. The client release is a REALIZATION-evidence
  gate, not a proposal gate.
- **Unchanged by construction**: the four reserved retention classes stay
  forbidden; the consent-purpose count stays frozen at three; the two kill
  switches are used, not multiplied; the live plane adds no media proxy and no
  second workflow session; and Hermes authority is never traded for latency.
- **Explicitly NOT this change**: aggregation admission of the client
  repository (separate reviewed change under `repo-boundary-governance`); the
  GPT-Live-1 default swap and every replace-the-primary semantic; and the
  `avatar-pilot-hardening` deferrals — durable per-tenant spend enforcement,
  the retained-real corpus with its retention-class unreservation, the
  structural non-shadowing flag, and hard p99, teardown, degraded-network and
  per-turn latency gates.
- **Successor gated on this change**: `avatar-pilot-hardening`, which cannot
  propose until this change publishes a qualified live profile.

## Authoring inputs to pin before realization

The rulings settled the posture; they deliberately left a set of values the
memo classified as authoring inputs rather than reopened forks. Each is a
named task in `tasks.md` §7 and each must carry a value before the ring
opens: the concrete vault choice for the internal-live server key; the numeric
per-session and per-tenant ceilings and the provider-project cap amount; the
rotation cadence and trigger for the server key; the alerting channel,
thresholds and page targets; the minimum sample count per gated latency cell;
the canary's soak duration, session count and tolerated error rate; the
operator surface that fires the kill switches; the session-outcome token each
rollback path emits; and the declared region and data-control values recorded
in AVC-09. None of these reopens a ruled fork; leaving any of them unset would
open the ring on an unstated assumption.
