---
code_surface: codexFactory apps/avatar-client-lab contract-pin resync (contract_pin.yaml + vendored assets swap; interim P10 checklist guard retirement)
target_release: contract-v1.12
Status: ratified
Ratified: 2026-07-16 — record: the archive act, commit `10181df` "Archive adopt-avatar-client-lab-candidates: v1.12 realization complete (codexFactory PR #17)", which applied this change's spec delta into `openspec/specs/avatar-first-ui/spec.md`, `openspec/specs/avatar-lab-evidence/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. The commit body records both the gate and the promotion in words: "Realization gate satisfied: PR #17 merged by Brett (Tier-1 approval) at 0fed12c (2026-07-16) ... Applies the avatar-lab-evidence capability (new) and the avatar-first-ui deterministic-acceptance modification to openspec/specs/". The change's own tasks.md 4.1 records product-owner sign-off on the candidate's six OPEN QUESTIONS, not on the change, so it corroborates and is not the citation. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".
---

# Proposal: adopt-avatar-client-lab-candidates

## Why

The avatar stack's layer-2 evidence system has seven verified-but-unlanded
artifacts. The `002-avatar-client-lab` flutterBench Bench-B lane drafted, and
independently panel-confirmed (fresh 2-lens adversarial panels, evidence in
that feature's `upstream-drafts/STATUS.md`), candidates for every open
upstream prerequisite in the governing change's P-ledger — including the two
ESCALATIONS that today have **no owning openxFactory task at all**: the P1
neutral avatar-state derivation table (until it lands, gate (vi) and the
gate (ix)(a) combination half run on interim invariants) and the P10
22-capability-scenario register (until it lands, gate (ix)(b) runs on an
asymmetric, app-side vendored-checklist stopgap). The five fixture-set
candidates (P7 intake breadth, P8 takeover/recovery, P11
`interrupted`/`handoff`, P12/P13 kernel `media.state` coverage) close the
state-reachability denominator, which the released seeds today evidence
almost nowhere via kernel fields. Settled law forbids the app from
self-serving any of these; a factory change must own the landing. This change
is that owner.

## What Changes

- **Becomes the new owning task for P1** (per its escalation memo): lands the
  neutral avatar-state derivation table as
  `contracts/avatar-client-lab/avatar-state-derivation-table.{md,yaml}`,
  total over the axis combinations, embedding the normative invariants,
  ratifying the candidate's six open questions (OQ-1..OQ-6), manifest-
  registered and content-addressed; adds the
  `check_avatar_state_derivation_table` fail-closed parity check to
  `scripts/validate-avatar-client.py`.
- **Becomes the new owning task for P10** (per its escalation memo): lands the
  22-capability-scenario register with stable per-scenario IDs and verbatim
  `#### Scenario:` titles, machine-checked fail-closed against the promoted
  capability spec (9 requirements / 22 scenarios, byte-exact, in order).
  Landing form (Option A: extend the P2 map vs Option B: distinct
  `capability-scenario-register.yaml`) is ratified in design.md — Bench B
  recommends Option B.
- **Lands the five confirmed fixture sets** into
  `examples/avatar-first-ui/fixtures/deterministic/`: P7 intake-set remainder
  (5 fixtures), P8 lease/epoch-takeover + snapshot-barrier recovery (4), P11
  `interrupted`/`handoff` (2), P12/P13 non-control `media.states` +
  `control_degraded` (9), with acceptance-map / evidence-register wiring so
  every new fixture's evidence ids resolve (validator parity).
- **Cuts `contract-v1.12`** (next additive release): manifest membership for
  the new artifacts, changelog, tag — and, per `implement-avatar-client-lab`
  task 4.4's release-time convention, registers
  `contracts/avatar-client/evidence-register.implement-avatar-client-lab.yaml`
  in the manifest so the SCO-001-S05 `planned → evidenced` discharge can
  become effective.
- **Realization (code surface)**: the codexFactory lab re-runs
  `sync_contracts` against `contract-v1.12`, swaps the interim P10 vendored
  checklist for the pinned upstream register, retires the interim
  faithfulness guard, un-skips the BLOCKED-on-P8 assertions, and proves the
  nine offline gates green on the resynced pin.

Source candidates: `specs/002-avatar-client-lab/upstream-drafts/` on
codexFactory branch `002-avatar-client-lab` @ `3a8fbd5` (7/7 panel-confirmed;
provenance in that folder's STATUS.md). Titles, counts, and revision
arithmetic were adversarially re-verified there; landing here re-runs the
upstream validators as the authoritative check.

## Capabilities

### New Capabilities
- `avatar-lab-evidence`: the neutral, content-addressed client-lab acceptance
  artifacts — the avatar-state derivation table (total, invariant-embedding,
  gate-(vi)/(ix)(a) source) and the capability-scenario register (stable-ID,
  verbatim-title, gate-(ix)(b) source) — plus their fail-closed validator
  checks and manifest/release registration obligations.

### Modified Capabilities
- `avatar-first-ui`: the "Deterministic UI acceptance" requirement changes in
  two ways — (a) presentation-state derivation is normatively bound to the
  landed neutral derivation table (replacing the interim invariant-only
  posture; the invariants remain embedded in the table), and (b) the
  deterministic fixture corpus obligation extends to the full closed
  `media.states` denominator and the intake/takeover/interrupted/handoff
  scenario families, evidenced via kernel fields only.

## Impact

- **openxFactory**: `contracts/avatar-client-lab/` (+2 artifacts, or +1 if
  Option A), `examples/avatar-first-ui/fixtures/deterministic/` (+20
  fixtures), acceptance maps / evidence registers touched additively,
  `scripts/validate-avatar-client.py` (+2 checks), `contracts/manifest.yaml`
  + changelog at release cut (`contract-v1.12`). Released `contract-v1.7` /
  `v1.8` bundles remain byte-identical (additive-only release).
- **codexFactory (realization)**: `apps/avatar-client-lab/` pin resync;
  retires the interim P10 guard; un-skips two P8-blocked tests; no reducer/UI
  changes expected (fixtures replay through existing seams).
- **Downstream unblocked**: `implement-avatar-client-lab` §9 realization and
  archive; gate (ix) completeness without tracked gaps; the MedxFactory
  patient-intake demo pack (consumes the landed intake scenario family).
- **Not touched**: kernel message schemas, registries, interface-lock (no
  vocabulary change anywhere in this change).
