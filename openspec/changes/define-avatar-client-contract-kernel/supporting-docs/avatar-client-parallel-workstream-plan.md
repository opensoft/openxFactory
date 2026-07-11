# Avatar Client Parallel Workstream Plan

Status: proposed
Kind: proposal support
Captured: 2026-07-10
Proposed by: define-avatar-client-contract-kernel
Supersedes implementation decomposition in: define-avatar-client-runtime

## Purpose

The reviewed avatar-client architecture remains one system, but its realization
is split into four OpenSpec changes with exclusive write surfaces. All four may
be implemented concurrently. Realization is ordered only at the final contract
pin and release gates.

## Workstreams

| Change | Owns | Must not edit | Realization gate |
| --- | --- | --- | --- |
| `qualify-avatar-brokered-call-feasibility` | `experiments/avatar-brokered-call/` and its own evidence | Canonical contracts, reference runtime, UI standard | Publishes `PASS`, `FAIL`, or `INCONCLUSIVE` plus an interface-impact report; never qualifies a live profile |
| `define-avatar-client-contract-kernel` | `contracts/avatar-client/`, its validator, canonical fixtures, registries, release metadata | Reference runtime and avatar-first UI assets | Contract release/tag requires F0 `PASS` and disposition of every reported interface variance |
| `implement-avatar-reference-runtime` | `xfactory/avatar_runtime/` and `tests/avatar_runtime/` | Canonical contracts, F0 harness, UI assets | Final conformance requires the exact released kernel commit and digests |
| `align-avatar-first-ui-standard` | Avatar-first standard, profile schema, template, examples, and validator | Canonical AVC files, F0 harness, reference runtime | Final cross-check requires the exact released kernel purpose and capability registries |

Parallel implementation branches do not edit shared release files. The kernel
change updates `contracts/manifest.yaml`, `contracts/CHANGELOG.md`, and
`contracts/README.md` for the kernel release. After rebasing to that release,
the UI alignment change updates the same files only in its final serialized
profile-schema release. These three integration files are the sole intentional
write overlap; neither change reserves a version before its merge order is
known.

## Parallel Interface Baseline

Parallel work begins from interface baseline `avatar-client-parallel-v1`,
defined by the reviewed `avatar-client-runtime` delta, the threat model, and
the stable `ACR-*` acceptance IDs in this proposal. The baseline fixes:

- the eight AVC contract identifiers and reserved identifiers;
- AVC-02 `grant | denial | terminal` result semantics;
- exact-offer retry identity and credential boundaries;
- sideband-before-answer and authoritative `media_authorized` ordering;
- one sequenced event log, snapshot barrier, epoch, lease, and heartbeat rules;
- the three neutral consent-purpose IDs;
- the four authoritative UI axes and client-local presentation mode; and
- fail-closed defaults for every deferred feature.

A child change may create a local test-only adapter for this baseline inside
its exclusive paths. It MUST NOT copy a provisional artifact into
`contracts/avatar-client/`, present it as canonical, or publish it as a
compatible release.

## Variance Protocol

When F0 or a child implementation discovers an interface problem, the owning
change writes an `interface-impact.yaml` evidence artifact containing the
baseline item, observation, severity, proposed correction, affected acceptance
IDs, and whether work can continue behind the closed default. Only the kernel
change may alter neutral contract meaning. Siblings consume the accepted
kernel correction; they do not edit one another's files.

`FAIL` or `INCONCLUSIVE` F0 evidence blocks contract publication, not parallel
coding. A material interface correction invalidates only the affected child
tests and mappings. Unaffected work remains valid.

## Integration DAG

```text
F0 feasibility ---------------------> contract publication gate
contract kernel implementation -----> contract release commit + digests
reference runtime implementation ---> pin released kernel -> realize
UI standard implementation ---------> pin released registries -> realize
```

The four implementation branches may start together. The kernel may merge its
non-release implementation before F0 completes, but it MUST NOT publish the
contract bundle or annotated tag until F0 is `PASS`. Runtime and UI branches
may complete their provisional suites in parallel. Runtime final realization
disables its provisional adapter and pins the kernel release. UI final
realization rebases to the kernel release, verifies the registries, allocates
the next available bundle version for its profile-schema change, and updates
shared release metadata atomically.

## Successors

The split does not absorb the existing successor changes:

- `implement-avatar-client-lab` creates the private Flutter client;
- `qualify-avatar-live-voice` performs internal-live provider qualification;
- `avatar-pilot-hardening` integrates Hermes, domains, accessibility evidence,
  operations, and pilot rollback; and
- separately approved changes own push-to-talk, offline drafts, attachments,
  multi-device takeover, web-console integration, and GPT-Live adoption.
