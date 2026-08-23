---
code_surface: openxFactory (a NEW `contracts/worker-enrollment/` family — enrollment request, enrollment grant, lease, lease renewal, enrollment policy, and enrollment audit-record schemas — plus packaged positive/negative examples and the canonical `scripts/validate-worker-enrollment.py`; registration in `contracts/manifest.yaml` + `contracts/CHANGELOG.md` at the next additive bundle cut). The broker SERVICE, the Omnigent-Install registration/renewal integration, and the OpsxFactory custody/policy/runner-group work are successor realization changes named in the impact map, not this change's surface.
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified: 2026-07-26 by Brett Heap — D1-D10 recommendations adopted as decided; phase-1 contract realization authorized, recorded in commit e535a3a and on the Approved line below
---

# Proposal: add-worker-enrollment-broker

Approved: 2026-07-26 by Brett Heap — D1-D10 recommendations adopted as
decided; phase-1 contract realization authorized.

## Why

The Worker Host App can build a worker host but cannot legitimately
register one. Its `runner_services` step refuses fail-closed today
because the only way to hand a host a runner registration token is to
put minting authority — an administration-tier GitHub App key — on the
host, which the ratified `roles-authority-model` App identity tiers
forbid and the per-domain App convention narrows further. That parked
decision blocked PRs #36/#37.

Brett resolved it on 2026-07-26 by widening the question rather than
answering it narrowly. His driving scenario: "what if we install this
installer app on just any engineer's workstation... turn their
workstation into a temp worker." Temp workers are wanted NOW, wanted
LONG-LIVED (months, not an afternoon), and wanted staff-common. That
turns a fleet credential problem into a two-estate enrollment problem:

- The **fleet** is Intune-managed. Its hosts have per-host identity, its
  packages are pinned, and Intune detection rules force our app current.
- A **volunteer workstation** is somebody's laptop. Nothing off-machine
  can force our app current on it, no per-host secret should ever land
  on it, and its hardware is not trusted with the same work as fleet
  metal.

Both estates need exactly one thing from the platform — permission to
become a worker — and today there is no place that grants it. This
change ratifies that place as a CONTRACT before any of the three
realizations are built, so the broker, the host app, and OpsxFactory are
implementing an agreed protocol rather than negotiating one through
code.

The governing insight is Brett's ruling 4: enrollment grants a **lease**,
not a registration. A registration is permanent and can only be undone by
reaching the machine; a lease expires unless something re-grants it. On
unmanaged metal that inversion is the whole control surface. Staleness,
revocation, trust, and audit all become properties of a renewal decision
the platform makes, not properties of a host we hope to reach.

## What Changes

- **NEW capability `worker-enrollment-broker`** — the neutral contract
  for how a machine becomes a governed worker and stays one:

  - **One enrollment point, two authentication modes.** A fleet host
    authenticates with per-host identity provisioned in an Opsx Key
    Vault (broker ACCESS, never minting authority); a volunteer
    workstation authenticates as the ENGINEER through an interactive
    device-code flow, and no standing secret is ever written to that
    machine. The protocol, the request shape, and the response shape are
    the same for both — the estate difference is who authenticates and
    where the manifest comes from, not what the exchange looks like.
  - **Enrollment yields a lease plus a short-lived registration token.**
    The lease carries an id, a TTL, a trust tier, and a runner group;
    the registration token is short-lived, single-use, and never
    persisted or logged anywhere.
  - **Minting authority lives only in the broker.** The opsxfactory
    administration-tier App key is held under the ratified
    `credential-contracts` custody shapes, in the broker and nowhere
    else. Remove-token brokering for drift repair rides the same
    authority and the same audit path.
  - **Renewal is the governance surface.** The supervisor renews on a
    cadence; every renewal response carries the current minimum app
    version and the lease state.
  - **Fail-closed staleness.** A below-floor worker, or one whose lease
    is refused, expired, or revoked, stops its runner services and
    reports `update_required` (or the refusing lease state) in its
    heartbeat until the engineer updates or the host re-enrolls.
    Revocation is expressed as REFUSING the next renewal — it needs no
    reach into the machine.
  - **Estate policy split for the runner package.** Fleet manifests hard
    pin the runner (version + sha256, `--disableupdate`) and bumps ride
    manifest rollouts; temp-worker enrollments run runner self-update
    with the observed version informational only.
  - **Segregation.** Volunteer leases bind to a dedicated runner group
    with temp labels, never the standing execution lanes, and carry a
    trust tier a lane can use to decline volunteered hardware.
  - **Audit with redaction.** Every enrollment, renewal, refusal, and
    revocation emits a record; no token value or key material is ever
    recorded in it.

- **Schemas + validator (this change's code surface)**: a
  `contracts/worker-enrollment/` family (request, grant, lease, renewal,
  policy, audit record), packaged positive and negative examples, and
  `scripts/validate-worker-enrollment.py` as the canonical validator,
  published as a versioned additive bundle so all three realizations pin
  a release rather than copying a shape.

- **NOT in this change**: the broker service itself (its home and
  hosting are design D1, unresolved), the Omnigent-Install
  registration/renewal integration, and the OpsxFactory custody, policy,
  runner-group, and eligibility work. Each is a named successor change.

## Capabilities

### New Capabilities

- `worker-enrollment-broker`: the neutral enrollment and lease contract
  for governed worker hosts across both estates — enrollment exchange,
  lease lifecycle, minimum-version floor with fail-closed enforcement,
  revocation by refusal, estate package policy, trust-tier segregation,
  and audited decisions.

## Impact

- **New code (this change)**: six schemas, packaged examples, one
  canonical validator. No runtime behavior changes here; nothing needs
  un-building, because `runner_services` already refuses fail-closed and
  the broker call drops into that existing seam.
- **Unblocks**: the Worker Host App's registration step (the PRs #36/#37
  parked decision), and with it the Omni-001 migration off the
  operator's personal machine.
- **Successor realization changes** (each pins the released bundle):
  1. the broker service — repo and hosting per design D1, which is the
     first decision to take;
  2. Omnigent-Install — registration-via-broker in `runner_services`,
     lease renewal in the hourly supervisor, and the fail-closed stop
     path;
  3. OpsxFactory — App key custody, the minimum-version policy
     instance, the temp runner group, and engineer eligibility.
- **Coordinated contract delta elsewhere**: lease state and
  `update_required` reaching the readiness evaluator is a heartbeat
  change that must land in publisher, service, and evaluator together
  (the three-places rule); it rides the pending bench-inventory
  heartbeat delta or its own coordinated change, not this one.
- **Relies on ratified work**: `roles-authority-model` (GitHub App
  identity tiers and administration-tier credential custody),
  `credential-contracts` (requirement/binding/grant/audit record
  shapes), the per-domain App convention (opsxfactory is the
  administration-tier identity; openxfactory is content-only and
  codexfactory is code-PR-only, both ruled out here).
- **Provenance**: staged topic
  `openxFactory:staging:worker-enrollment-broker` (its exit 1), which
  records the seven binding rulings taken with Brett on 2026-07-26;
  parent topic `openxFactory:staging:worker-host-app`.
