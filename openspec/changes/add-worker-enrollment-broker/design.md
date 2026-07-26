# Design: Worker Enrollment Broker — one enrollment point, leases over registrations

## Context

The Worker Host App reconciles a machine into a worker host, and then
stops: `runner_services` refuses fail-closed because there is no
legitimate way to give a host a runner registration token. Minting a
token requires an administration-tier GitHub App key, which the ratified
`roles-authority-model` tiering says must not do ordinary work and must
not sprawl, and which the per-domain App convention says belongs to the
opsxfactory identity alone. Putting that key on hosts would trade a
build problem for a governance breach. That is the parked decision
behind PRs #36/#37.

Brett resolved it on 2026-07-26 by making the question bigger. His
scenario — "what if we install this installer app on just any engineer's
workstation... turn their workstation into a temp worker" — adds a second
estate with none of the fleet's affordances: no Intune, no per-host
secret we would be willing to plant, no detection rule to force our app
current, and hardware nobody has vetted. Temp workers are wanted now,
wanted for months at a time, and expected to be staff-common.

Two estates, one need: permission to become a worker. This change
ratifies that permission as a contract before three separate repositories
try to implement it.

### Rulings already taken (Brett, 2026-07-26 — decided inputs, not open)

These are inputs to the design, not decisions this document reopens.

1. **Broker-first architecture, standalone service.** The broker is its
   own deployment — not a hermes-install route, not an OpsxFactory
   function.
2. **Two estates, two auth modes, one enrollment point.** Fleet hosts
   authenticate with per-host identity (per-host secret in an Opsx key
   vault, the Intune-managed standard) as broker ACCESS, never minting
   authority; volunteer workstations authenticate as the ENGINEER by
   device code, and no standing secret ever lands on the machine.
3. **Minting authority never on hosts.** The broker holds the opsxfactory
   administration-tier App key; registration AND remove tokens come from
   that one authority.
4. **Lease, not registration.** Enrollment grants a renewable lease the
   supervisor renews on a cadence; a months-lived temp worker is months
   of renewals, and revocation is refusing the next one.
5. **Minimum-app-version floor, fail-closed.** The renewal response
   carries the floor; a below-floor worker's runner services STOP and its
   heartbeat reports `update_required` until the engineer re-runs the
   installer. (v1 is reinstall; broker-served digest-verified self-update
   is the v2 convenience.) Rationale: GitHub keeps the runner BINARY
   current by itself, but nothing off-machine can force OUR app current
   on an unmanaged workstation except the broker.
6. **Runner package policy split.** Fleet = hard pin (v2.336.0, win-x64
   sha256 `d59123a43003e357b0805b5d0f611d0bd2f65ab67d51bd070dd4e7a0f685c162`,
   `--disableupdate`; bumps ride manifest rollouts so Intune re-runs);
   temp workers = self-update on, observed version informational.
7. **Temp workers are segregated.** Own runner group and labels, never
   the standing lanes, plus a trust tier so lanes can decline to dispatch
   sensitive work to volunteered hardware.

### Why the lease inversion is the whole design

A registration is a fact on a machine: it exists until someone reaches
the machine and removes it. A lease is a decision the platform re-takes
on a cadence: it lapses unless the platform re-grants it. On managed
metal the difference is bookkeeping. On a laptop that spends weekends
off-network and may quit the company on a Friday, the difference is
whether control exists at all. Every other control in this contract —
version floor, revocation, trust tier, audit — is expressed as a
property of the renewal decision, which is why they all work on hardware
we do not manage.

## Goals / Non-Goals

**Goals**: one enrollment protocol both estates use; minting authority in
exactly one place; a lease lifecycle that makes staleness, revocation,
and trust enforceable off-machine; a package policy that respects what
each estate can actually guarantee; segregation that lanes can rely on;
an audit record that never carries a secret; and a schema family the
three realizations can pin instead of negotiating shapes in code.

**Non-Goals**: the broker service implementation and its hosting (D1
below decides the home; the build is a successor change); the
Omnigent-Install and OpsxFactory realizations; the heartbeat/readiness
contract delta (D10 — three places, its own coordinated change); v2
broker-served app self-update; any Hermes approval machinery beyond
naming the door it arrives through.

## Decisions

Each decision below corresponds to an open question in the staged topic.
Where the topic carried a leaning, it is stated as a recommendation.
APPROVAL 2026-07-26: Brett approved this change with the D1-D10
recommendations adopted as decided ("add-worker-enrollment-broker is
approved", clarifying session, same day as the rulings). The markers
below are updated accordingly; D1's adopted answer (Opsx-owned repo,
container app off the QA cluster) unblocks realization 2.

Decisions marked **DECIDED (approval 2026-07-26)** were recommendations
adopted wholesale by that approval — the contract
in this change is deliberately written so none of them changes the
protocol, only its parameters and its home.

### D1 — Broker home and hosting **DECIDED (approval 2026-07-26)** (was the blocking decision; realization 2 unblocked)
**Recommendation**: a new dedicated repository owned by OpsxFactory's
domain (the estate-operations owner), deployed as a container app on the
existing platform subscription rather than into the QA AKS cluster —
because the broker is a production control-plane dependency for every
worker host, and hanging it off a QA cluster inherits QA's blast radius
and its lifecycle. Its own credential custody follows the ratified
administration-tier custody requirement: vaulted key, short-lived
workflow-scoped grants, approval before grant issuance, an audit record
per action, and a declared rotation cadence.

**Alternative considered**: fold it into hermes-install as another route.
Rejected by ruling 1 — and rightly: Hermes is the truth/consent plane,
not a token mint for machines, and coupling worker enrollment to Hermes
availability would make every host registration depend on the identity
plane being up.

The reason this is the FIRST decision is that the repository is where the
successor change lands; nothing else in phase 2 can start without it.

### D2 — Lease cadence and grace window **DECIDED (approval 2026-07-26)**
**Recommendation**: TTL 24 hours, renewal attempted hourly by the
existing supervisor task, grace of 12 hours past expiry before the lease
is treated as lapsed, and ±5 minutes of clock-skew tolerance on lease
expiry evaluation.

Rationale: the hourly supervisor already exists, so renewal is free; 24h
TTL with 12h grace means an ordinary overnight or a flaky VPN never fails
a worker closed, while a revoked laptop loses authority within a working
day at worst. Shorter TTLs buy tighter revocation at the cost of making
the broker a hard availability dependency of every running worker — a 24h
TTL means a broker outage is invisible for a day.

**Sensitivity**: the fail-closed bound in the contract is "cadence plus
grace"; tightening either later is a policy edit, not a contract change.

### D3 — Minimum-version policy home **DECIDED (approval 2026-07-26; topic leaning adopted)**
**Recommendation**: an OpsxFactory-owned policy instance the broker
CONSUMES, not broker-local config — matching the topic's leaning and the
managed-platform precedent that OpsxFactory owns estate policy. The
policy carries the floor per estate, the runner package pin per estate,
the eligibility groups, the trust-tier definitions, and its own
`policy_version`, which the audit record cites.

**Who may raise the floor**: raising the floor is a work-denying action
across the whole estate, so it takes the governed review lane (the
rules-as-code precedent) rather than an operator edit; the broker reads
the merged policy and never accepts a floor from an ad-hoc call.

This change ships the policy SCHEMA so the home decision is only about
where the instance lives and who reviews it.

### D4 — Enrollment approval flow **DECIDED (approval 2026-07-26)**
**Recommendation for v1**: auto-approve on Entra-group eligibility with
the evidence recorded (who, which group, which policy version), and let
the TRUST TIER carry the difference rather than a human gate. Brett's
driving scenario is explicitly low-ceremony — an engineer should be able
to volunteer a machine without filing anything — and the segregation
ruling already guarantees a volunteered machine cannot reach standing
lanes or sensitive work.

**The door for later**: the staged topic's claim 2 names this as where
Hermes registration approval arrives (the worker-host-app topic's v2
"enrollment-handshake agent"). Because approval is a property of the
LEASE decision, inserting a Hermes approval step later changes who
answers the enrollment call, not the protocol — no contract delta is
needed to add ceremony, only to add a tier that requires it.

### D5 — Temp-worker manifest content and serving **DECIDED (approval 2026-07-26)**
**Recommendation**: the broker SERVES the temp manifest at enrollment
(the fleet gets its manifest in the Intune package; the volunteer has no
delivery plane, so enrollment is the only door), rendered from the policy
for the temp estate and carrying its own `policy_version` identity so a
volunteer's manifest is as traceable as a fleet host's. Content leaning:
one worker, the general coding-patch profile, temp labels, no benches in
v1 — bench pre-pull is a multi-gigabyte imposition on somebody's laptop
and should be opt-in when temp workers have proven useful.

### D6 — Engineer eligibility **DECIDED (approval 2026-07-26)**
**Recommendation**: a single named Entra group for volunteers (start with
the engineering staff group rather than inventing a new one, so eligibility
is a membership fact rather than a second roster to maintain), with a cap
of one volunteered machine per engineer in v1 — the cap being enforceable
precisely because leases are per-machine records the broker holds.

### D7 — Teardown semantics **DECIDED (approval 2026-07-26)**
**Recommendation**: three distinct outcomes, all audited.
- **Voluntary uninstall** (volunteer estate): full cleanup of the
  engineer's own machine — runner removed via a brokered remove token,
  services and tasks deleted, local worker state and materialized
  credential profiles wiped — and the lease is released. It is somebody's
  personal laptop; leaving artifacts behind is not acceptable there even
  though it is the fleet's ruled behavior (fleet uninstall keeps escrows).
- **Lease expiry**: work stops, nothing is deleted; a lapse is often
  transient (offline laptop) and destroying state on lapse would make
  every flaky network a reinstall.
- **Revocation**: work stops immediately at the refused renewal and the
  runner registration is removed by brokered remove token; local state
  removal is best-effort, because revocation must not depend on reaching
  the machine.

### D8 — Trust-tier mechanics **DECIDED (approval 2026-07-26)**
**Recommendation**: the trust tier is a first-class LEASE field (this
change's schema carries it), projected into two places — the runner
group/labels the lease binds (so GitHub-side targeting works today
without any evaluator change) and the worker's readiness attestation (so
lanes can express exclusion declaratively once D10 lands). Labels alone
were considered and rejected as the sole mechanism: a label is
host-assertable and therefore not a governance boundary, while a tier on
a broker-issued lease is.

### D9 — Fleet per-host secret provisioning **DECIDED (approval 2026-07-26)**
**Recommendation**: issue the per-host broker-access secret at Intune
enrollment time into the Opsx key vault under the escrow-at-birth rule
the worker-host-app topic already made mandatory, one secret per host,
rotated on the same cadence as other estate machine credentials and
rotatable without re-enrollment (the lease survives a secret rotation
because the lease is not derived from the secret). This is the only
standing secret in the design, it exists only on managed metal, and it
buys nothing but broker ACCESS.

### D10 — Heartbeat/readiness integration **DECIDED (approval 2026-07-26; sequencing as recommended)**
**Recommendation**: lease state and `update_required` reach the readiness
evaluator as a heartbeat delta that lands in publisher, service, and
evaluator TOGETHER — the three-places rule, pinned by the parity-test
pattern — either riding the pending bench-inventory heartbeat delta from
the worker-host-app topic (preferred: one coordinated change instead of
two) or as its own coordinated change if that one lands first.

This change deliberately does NOT grow the heartbeat contract. What it
does is make the states the heartbeat will need well-defined and named,
so the delta is a projection rather than a design.

## Risks / Trade-offs

- **The broker becomes a control-plane dependency.** If it is down, no
  new host can enroll and eventually no worker can renew. Mitigated by
  the 24h TTL of D2 (a day of outage is invisible to running workers) and
  by keeping the broker off the QA cluster (D1). Accepted: the
  alternative is distributed minting authority, which is the thing this
  change exists to prevent.
- **A single key, more concentrated than before.** Concentration is the
  point — one custodied, audited, rotatable location beats N hosts — but
  it raises the value of that one target. Mitigated by the ratified
  administration-tier custody requirements and by the audit record on
  every mint.
- **Volunteer machines are somebody's property.** Fail-closed denial of
  work, full cleanup on uninstall (D7), and no standing secret are the
  three properties that keep this defensible; if any of them erodes, the
  program should stop rather than negotiate.
- **v1 recovery is a reinstall.** A raised floor means every volunteer
  re-runs the installer. This is deliberate friction that keeps the v1
  broker from needing a software-distribution channel; the v2
  broker-served digest-verified self-update is the fix, and the cost is
  bounded because floors should rise rarely.
- **Two estates, one protocol, might over-generalize.** The mitigation is
  in the shape: the estate difference lives in the policy and the
  manifest source, not in the exchange, so if the estates diverge further
  it is a policy fork rather than a protocol fork.

## Open Questions

All ten of the staged topic's open questions are addressed above as D1–D10
with recommendations; each still needs Brett's ruling, and D1 (broker
home) is the one that blocks the first realization. Two further questions
are carried by the acceptance test rather than by the contract:

- **Does the actions-runner service support `NT SERVICE\*` logon?** The
  worker-host-app topic's open question; the volunteer-workstation
  acceptance run on Brett's machine is the fact-check (task 5.1).
- **Does the v2 broker-served self-update deserve its own change, or does
  it ride the broker's second increment?** Deferred until v1 has shown
  how often floors actually rise.
