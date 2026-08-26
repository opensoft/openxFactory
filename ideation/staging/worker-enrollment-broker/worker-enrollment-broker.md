# Staged: Worker Enrollment Broker

Status: staged
Kind: architecture
Summary: A standalone broker service that owns worker enrollment for both
estates — the Intune-provisioned fleet (per-host identity) and staff
workstations volunteering as long-lived temp workers (engineer
device-code identity, self-service install). The broker centrally holds
the runner registration-token minting authority (opsxfactory admin-tier
App key — never on any host), grants renewable leases instead of
permanent registrations, and enforces a minimum-app-version floor at
lease renewal: below-floor workers fail closed (runner services stop,
heartbeat reports update_required) until the engineer updates.
Fleet runner packages are hard-pinned via manifest rollouts; temp-worker
runners self-update (GitHub enforces runner currency); the app-version
floor is the broker's job because no Intune detection rule exists on a
volunteer workstation.
Topics: worker-enrollment, broker, temp-worker, runner-registration,
lease, credential-escrow, worker-host-app, opsxfactory, intune,
github-apps, trust-tier
Repository context: openxFactory (the neutral enrollment/lease contract);
broker service home TBD (standalone by ruling — own repo/hosting
decision open); Omnigent-Install (Worker Host App: registration action
learns the broker call; supervisor learns lease renewal; the
`runner_services` registration path today refuses fail-closed, so
nothing needs un-building); OpsxFactory (opsxfactory App key custody,
minimum-version policy, temp runner group, engineer eligibility policy)
Staging ID: `openxFactory:staging:worker-enrollment-broker`
Source: clarifying session with Brett Heap 2026-07-26 at the
worker-host-app runner_services gate (PRs #36/#37), resolving the
registration-credential parked decision; Brett's driving scenario:
"what if we install this installer app on just any engineer's
workstation... turn their workstation into a temp worker" — temp
workers wanted NOW, long-lived (months), staff-common.

## Rulings already taken (Brett, 2026-07-26 — binding inputs, not open)

1. **Broker-first architecture, standalone service** (not a hermes-install
   route, not an OpsxFactory function): the broker is its own deployment.
2. **Two estates, two auth modes, one enrollment point**: fleet hosts
   authenticate with per-host identity (per-host secret in an Opsx KV —
   the Intune-managed standard — as *broker access*, never minting
   authority); temp workstations authenticate as the ENGINEER
   (device-code; no standing secret ever lands on the machine).
3. **Minting authority never on hosts**: the broker holds the opsxfactory
   admin-tier App key (per-domain App convention: openxfactory read-only
   and codexfactory code-PR-only are ruled out). Registration AND
   remove tokens come from the same authority.
4. **Lease, not registration**: enrollment grants a renewable lease; the
   supervisor renews on a cadence. Months-lived temp workers = months of
   renewals; revocation = refuse the next renewal.
5. **Minimum-app-version floor, fail-closed**: the renewal response
   carries the current floor; a below-floor worker's runner services
   STOP, heartbeat reports `update_required`, the engineer re-runs the
   installer (v1; broker-served digest-verified self-update is the v2
   convenience). Rationale: GitHub enforces runner-binary currency by
   itself, but nothing off-machine can force OUR app current on an
   unmanaged workstation except the broker.
6. **Runner package policy split**: fleet = hard pin (v2.336.0,
   win-x64 sha256 `d59123a43003e357b0805b5d0f611d0bd2f65ab67d51bd070dd4e7a0f685c162`,
   `--disableupdate`; bumps ride manifest rollouts → Intune re-runs);
   temp workers = self-update ON, observed version informational.
7. **Temp workers are segregated**: own runner group and labels, never
   the standing lanes; a trust tier so lanes can decline to dispatch
   sensitive work to volunteered hardware.

## Claims

1. **One enrollment point serves both estates.** The difference between
   a fleet host and a volunteer workstation is WHO authenticates and
   WHERE the manifest comes from (Intune package vs broker-served at
   enrollment) — not the protocol.
2. **The lease is the governance surface.** Enrollment approval, TTL,
   trust tier, version floor, revocation, and audit all attach to the
   lease lifecycle; Hermes approval integrates here (the worker-host-app
   topic's v2 "enrollment-handshake agent, Hermes registration approval"
   arrives through this door).
3. **Fail-closed staleness beats managed updates on unmanaged metal.**
   We do not chase volunteer workstations with update machinery; we
   refuse leases until a human updates — the same control Intune
   detection gives the fleet, expressed as denial-of-work.
4. **The Worker Host App is already shaped for this.** Registration is a
   fail-closed refusal today; the broker call drops into that seam. The
   supervisor task (hourly) is the natural lease-renewal carrier.

## Open questions

1. Broker home: repo + hosting target (container app? AKS alongside the
   QA cluster? owner per per-domain conventions) + its own credential
   custody and rotation story.
2. Lease cadence and grace window (daily renewal? how many missed
   renewals before fail-closed? clock-skew tolerance).
3. Minimum-version policy home: OpsxFactory-owned policy file the broker
   consumes (leaning) vs broker-local config; who may raise the floor.
4. Enrollment approval flow: auto-approve by Entra-group eligibility in
   v1 with recorded evidence, or a human/Hermes approval gate from day
   one? (Brett's driving scenario implies low-ceremony; the trust tier
   may carry the difference.)
5. Temp-worker manifest: what a volunteer machine gets (which workers,
   which profiles, benches or not), how it's rendered/served by the
   broker, and its policy_version identity.
6. Engineer eligibility: which Entra group(s) may volunteer a machine;
   per-engineer worker cap.
7. Teardown: voluntary uninstall vs lease expiry vs revocation — what
   each removes (uninstall semantics ruled for the fleet: escrows stay;
   volunteers likely want fuller cleanup of their own machines).
8. Trust tier mechanics: how lanes express "no temp workers" (label
   convention? readiness attestation field? profile constraint?).
9. Per-host secret provisioning for the fleet's broker access (Opsx KV
   standard) — issuance at Intune enrollment time, rotation cadence.
10. Heartbeat/readiness integration: `update_required` and lease state
    in the heartbeat → readiness evaluator (rides the pending
    bench-inventory heartbeat delta or its own coordinated change —
    three-places rule).

## Exit

**Exit 1 PROPOSED 2026-07-26** as
[`add-worker-enrollment-broker`](../../../openspec/changes/add-worker-enrollment-broker/proposal.md)
(`code_surface`: openxFactory only — the `contracts/worker-enrollment/`
schema family, packaged examples, and `scripts/validate-worker-enrollment.py`;
`target_release`: next additive contract bundle). The change ratifies the
CONTRACT and names the three realizations as successor changes; the
seven rulings above are carried as decided context in its `design.md`,
and all ten open questions below are carried there as decisions D1–D10
with recommendations — D1 (broker home + hosting) is the one that blocks
the first realization. The heartbeat/readiness projection (question 10)
is deliberately excluded from the contract delta and left to a
coordinated three-places change.

An openxFactory OpenSpec change (`add-worker-enrollment-broker`)
ratifying the neutral enrollment/lease contract (enrollment request/
response, lease renewal, version floor, revocation, trust tier), plus
realization changes: the broker service (home per open question 1),
Omnigent-Install (registration-via-broker in `runner_services`, lease
renewal in the supervisor, fail-closed stop path), OpsxFactory (App key
custody, policy file, temp runner group, eligibility). Acceptance test
named by Brett's scenario: an engineer workstation — first volunteer =
Brett's own machine, which doubles as the NT SERVICE fact-check host —
goes download → install → device-code enroll → segregated runner group →
executes a lane job → survives lease renewals → fails closed when the
floor is raised past its version → recovers by reinstall.
