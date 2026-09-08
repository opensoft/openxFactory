# Staged: Avatar Pilot Hardening — real Hermes, domain overlays, and the gated live pilot

Status: staged
Kind: architecture
Summary: Replace the reference runtime's static fail-closed authority stub with
real Hermes control + delegation behind the frozen ports, add per-domain
overlays/personas, commission the formal accessibility audit, stand up the
operations/telemetry plane, and run a staged live pilot with an operational
rollback — closing the threat-model items the kernel deferred to pilot.
Topics: avatar-client, hermes, delegation, domain-overlays, personas, accessibility, wcag-audit, operations, telemetry, sbom, license-review, pilot, rollback, kill-switch, threat-model-closure
Repository context: openxFactory owns the neutral `avatar-pilot-hardening` capability, the domain-overlay contract, and the pilot-gate acceptance; real Hermes adapters land in `installs/hermes-install`; per-domain overlays/personas in the DomainxFactory repos (`xFactories/*`); the live client stays in the private `openAvatar` repo
Staging ID: openxFactory:staging:avatar-pilot-hardening
Source: named the last successor in the avatar-client parallel-workstream plan ("Successors"); the deferred-to-pilot items in the avatar-client threat model (lines 89–90 real Hermes/domain consent, line 57 TM-03 client-integrity, lines 87–88 privacy review/pen test/production authorization); and the reference authority stub in `xfactory/avatar_runtime/` (`authority.py`/`consent.py`/`operations.py` behind `ports.py`)
Target capabilities: avatar-pilot-hardening (ADDED)

The avatar-client kernel (`contract-v1.7`), the avatar-first UI standard
(`contract-v1.8`), and the non-deployable reference runtime
(`xfactory/avatar_runtime/`) are realized, and two successors are in flight:
`avatar-client-lab` proves the offline interaction and authority model, and
`qualify-avatar-live-voice` qualifies a live voice profile with a real model and
provider. Neither runs against real authority. The reference runtime is, by
construction, a deterministic contract proof — it exposes exactly seven injected
ports (`ports.py`), and the reference `PolicyResolver`, `ConsentGate`, and
`OperationRunner` (`authority.py`/`consent.py`/`operations.py`) are **static,
fail-closed fixture adapters** behind them; the package loads no credential,
opens no listener, and MUST NOT become a service. The threat model records the
consequence directly: "the reference authority implementation uses fixtures;
real Hermes and domain consent integrations remain blocked until
`avatar-pilot-hardening`."

This topic — the last successor in the parallel-workstream plan — is that
integration and the gated first live pilot. It replaces the static stub with
real Hermes control and delegation behind the frozen ports, adds per-domain
overlays and personas above the neutral kernel, commissions the formal
accessibility audit the lab deferred, stands up the operations/telemetry plane
the reference runtime deliberately omits, and closes the threat-model items the
kernel deferred to pilot — all behind a staged rollout with an operational
rollback. The load-bearing constraint is that real Hermes **tightens the
protocol, it does not change it**: the AVC envelopes, invariants, and acceptance
IDs stay frozen; only the decisions behind the ports become real.

## Claims

1. **Real Hermes plugs into the frozen ports; it tightens, it does not change,
   the protocol.** The seven injected port Protocols — including `PolicyPort`,
   `ConsentPort`, `OperationPort`, and the privileged provider-tool sideband —
   are the runtime's only external surface. The reference implementation
   supplies static fixture adapters that fail closed (unknown/unavailable →
   deny). Pilot-hardening supplies real Hermes-backed adapters behind the *exact
   same* Protocols — real policy resolution, real consent bindings, real
   confirmation, real tool execution — so every AVC envelope, invariant, and
   acceptance ID from `contract-v1.7` is unchanged. The only observable
   difference is that decisions the fixture bundle granted may now be denied. A
   live adapter that widens the protocol (a new envelope, a relaxed invariant, a
   weakened redaction rule) is out of scope and fails the pilot gate.

2. **Delegation is the Customer / Client / Domain Hermes layering made real.**
   The static fixture returns a single `PolicyBundle`; real Hermes derives
   policy, consent, and confirmation across the three canonical layers and
   delegates authority downward, so the runtime's `resolve`/`binding`/`is_valid`
   calls resolve against actual truth/intent/policy/consent state. The neutral
   avatar purpose registry maps to real Hermes consent per TM-13, and the
   fail-closed FR-030 rule is preserved verbatim: the memory-gateway consent
   schema is **never** treated as media authority — only the domain `ConsentPort`
   is, now backed by Hermes rather than a fixture.

3. **Domain overlays and personas sit above the neutral kernel, never inside
   it.** Each DomainxFactory (Med / Ledger / Ops / Ad / codex) supplies a
   persona, disclosure text, and a mapping of the three neutral consent-purpose
   IDs and four authoritative UI axes to its domain interpretation and Hermes
   policy binding — as **overlays that consume the frozen registries**, never as
   edits to the neutral contract. openxFactory owns the neutral overlay contract
   and its conformance; each domain repo owns its overlay instance. This keeps
   domain-neutral discipline: no domain forks the AVC contract to carry its
   persona.

4. **The formal accessibility audit upgrades the lab's baseline into audited
   evidence and disposes of the web exception.** `avatar-client-lab` ships the
   eleven avatar-first UI baseline capabilities plus keyboard-only F1–F4 on
   desktop, with a documented WCAG exception register for canvas-rendered web
   (which cannot pass WCAG 2.2 AA today). Pilot-hardening commissions an
   independent WCAG 2.2 AA audit with real assistive-technology / screen-reader
   testing that either closes the web exception register or ratifies each
   residual as a scoped, pilot-visible exception. The audit is a named,
   gate-blocking pilot artifact — not a self-attestation.

5. **Operations and telemetry graduate from a redaction proof to a running
   plane.** The kernel proves redaction offline (allowlisted structured fields,
   drop-on-fail; TM-12, `telemetry.py`). Pilot-hardening stands up the
   production telemetry pipeline behind the *same, never-relaxed* redaction gate,
   plus latency SLOs, monitoring/alerting, on-call and incident-response
   runbooks, and endpoint management — the operational surface the reference
   runtime deliberately excludes (no network listener, no credential loading,
   non-deployable) and the mitigations the threat model assigns to the
   compromised-endpoint residual risk.

6. **Pilot rollout is staged and rollback is the fail-closed default made
   operational.** Bounded internal cohort → bounded external cohort, each behind
   the per-profile / all-session kill switch (FR-031, `killswitch.py`). Rollback
   introduces no new mechanism: flipping the kill switch blocks new sessions and
   (by policy) revokes active leases; the ≤5 s client-enforced revocation plus
   accepted provider hangup drains sessions in flight; and the pin reverts to the
   last-green contract/runtime commit. Because every deferred live feature
   already fails closed, disabling the live adapter reverts cleanly to the
   deterministic/offline posture with no data path left open.

7. **The pilot gate is a conjunction of external evidence, not a self-review.**
   Entry to any live cohort requires, all of: (a) a qualified live voice profile
   from `qualify-avatar-live-voice` — the kernel and F0 explicitly *never*
   qualify a live profile; (b) an SBOM; (c) a dependency-license review; (d) the
   formal WCAG 2.2 AA audit; and (e) the threat-model closure evidence the kernel
   deferred — client-integrity evidence (desktop signing or web
   deployment-integrity, the TM-03 precondition to internal live), a privacy
   review, and a penetration test, all explicitly outside F0's scope. Any missing
   artifact fails the gate closed.

## Open questions

1. **Hermes call site — synchronous inside preflight, or a pre-session
   attestation resolved before answer-release?** The reference ports are
   synchronous (`resolve` / `binding` / `is_valid`); real Hermes is a network
   authority whose latency must fit inside the sideband-before-answer ordering
   (TM-02) and the 3 s-default / 5 s-max readiness timer (TM-04) without ever
   releasing an answer early. *Lean:* resolve authority into a short-lived
   attestation *before* the media leg so the timed path stays local, and map a
   Hermes miss to the existing `AUTHORITY_UNAVAILABLE` denial. Confirm or
   override — blocking.

2. **One parameterized domain-overlay contract, or a full overlay capability per
   DomainxFactory?** Five domains each need a persona, disclosure text, and a
   consent-purpose / UI-axis mapping. One neutral parameterized schema keeps the
   conformance surface small but may not carry regulated-domain divergence (Med
   disclosure/consent obligations); five instances explode the surface. This
   decides what openxFactory owns versus each domain repo — blocking.

3. **Accessibility scope for the first pilot — desktop-only AA carrying the web
   exception, or block the pilot on web WCAG 2.2 AA?** The lab qualifies a11y on
   Windows desktop and keeps a documented web exception register. The formal
   audit forces the call: ship the first cohort desktop-only, or take on
   web-a11y remediation here. This gates cohort selection and the audit's pass
   criterion — blocking.

4. **First cohort and data-processing posture.** Internal-only-first is settled;
   the fork is which domain leads, whether an external design-partner cohort
   requires a signed DPA/BAA before any live media, and whether a regulated
   domain (Med — carrying the FDA-SaMD / privacy weight from the origin-contract
   rationale) or a lower-stakes domain (codex / Ops) is the safer first live
   cohort — blocking.

5. **Rollback granularity and kill-switch custody.** FR-031 gives all-session and
   per-profile kill switches; a multi-cohort pilot on one profile may need
   per-tenant / per-cohort disablement. It is also unresolved whether the
   kill-switch state is itself a Hermes-governed control or an ops-plane control
   — who may flip it, and whether the flip is audited/consented. Blocking for the
   rollback runbook.

6. **Ownership of the provider contractual / data-residency layer.** The threat
   model assigns provider contractual, privacy, and regional-processing controls
   to provider qualification (`qualify-avatar-live-voice`), but data-residency
   and the DPA sit at the pilot/operations boundary. Does pilot-hardening consume
   a fully-qualified provider profile that already carries these, or own the
   contractual/residency layer on top (deciding whether the pilot gate re-checks
   residency)? Fork.

## Exit

Create `avatar-pilot-hardening` (`code_surface: openxFactory,
openAvatar, installs/hermes-install, xFactories/*`;
`target_release: implemented`, or a named pilot release defined in the
aggregation repository at proposal time). It **cannot propose** until
`qualify-avatar-live-voice` publishes a
qualified live voice profile and `implement-avatar-client-lab` lands the client
it hardens — it is the last successor, and is blocked on both of those plus the
six forks above. At the proposal gate, move this fragment into that change's
`supporting-docs/`, preserving the staging origin; author the full
`avatar-pilot-hardening` (ADDED) spec deltas (real-Hermes-behind-frozen-ports
conformance, the domain-overlay contract, the pilot-gate artifact conjunction,
and the staged-rollout / rollback runbook); and record the pilot-gate artifacts
— the qualified live profile, SBOM, dependency-license review, formal WCAG 2.2
AA audit, client-integrity evidence (TM-03), privacy review, and penetration
test — as named, gate-blocking evidence. Per the release-realization capability,
the change archives only on merged + green + recorded pilot-gate evidence, not on
merge alone.