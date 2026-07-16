# Design: adopt-avatar-client-lab-candidates

## Context

The governing change `implement-avatar-client-lab` is implementation-complete
on its codexFactory code surface (106/106 tasks, nine offline gates green,
feature branch merging to main) but its P-ledger names seven upstream
prerequisites that no openxFactory task owns. All seven exist as
panel-confirmed candidates under codexFactory
`specs/002-avatar-client-lab/upstream-drafts/` @ `3a8fbd5`, each folder
carrying a README with sources, verification evidence, and the exact factory
ask; P1 and P10 additionally carry escalation memos with ready-to-paste task
text. Constraints in force: settled law L2 (the app never self-serves neutral
artifacts), the additive-release convention (released bundles stay
byte-identical; new artifacts join the manifest only when the next version is
cut), and locked decision 7 (deferred evidence discharges only via successor
registers). The openxFactory checkout is shared with concurrent ideation-lane
sessions (disjoint paths; discipline still applies).

## Goals / Non-Goals

**Goals:**
- Give P1 and P10 their owning tasks and land all seven candidates as neutral,
  content-addressed artifacts with fail-closed validation.
- Close the gate (ix) evidence gaps (state-reachability denominator +
  capability-scenario enumeration) at their upstream source.
- Cut `contract-v1.12` so the lab can consume everything via one pin resync,
  and so the SCO-001-S05 successor-register discharge becomes effective.

**Non-Goals:**
- No kernel vocabulary change (schemas, registries, interface-lock untouched).
- No live-seam work (that is `qualify-avatar-live-voice`).
- No domain (MedxFactory) content — the patient-intake demo pack consumes this
  change's outputs but is its own change.
- No app-side code changes beyond the realization pin resync.

## Decisions

**D1 — New owning change, not a delta on `implement-avatar-client-lab`.**
The P1 memo prefers adding a task to the existing change if open. Rejected
here, with the memo's own alternative taken instead: the existing change is
archive-shaped (only §9 realization remains) and its realization *consumes*
this change's release (pin resync at its task 9.3). Folding authorship of
seven artifacts plus a release cut into it would couple its archive to new
work and invert the dependency. One dedicated adoption change keeps the
sequencing acyclic: adopt → release v1.12 → lab resync → governing change
realizes and archives.

**D2 — P10 lands as Option B: a distinct register.**
`contracts/avatar-client-lab/capability-scenario-register.yaml` with its own
`kind`, `expected_requirement_count: 9` / `expected_scenario_count: 22`, and a
dedicated fail-closed validator check mirroring
`check_client_lab_acceptance_map` (byte-exact titles, document order, no
fabricated/renamed/dropped/reordered entries against the promoted
`openspec/specs/avatar-client-lab/spec.md` once that change archives — until
then, against its change-delta copy with the check pinned to re-verify at
promotion). Rationale over Option A (extend the P2 map): provenance separation
of the inherited-42 vs capability-22 enumeration sources; the P2 map's
count self-checks describe the 42 only; the candidate lands with minimal
transformation. Cost accepted: the app pins two `vendored_evidence_inputs`.

**D3 — P1 lands under `contracts/avatar-client-lab/`, not as a standard
section.** `avatar-state-derivation-table.md` (normative prose) +
`avatar-state-derivation-table.yaml` (machine-readable, registry-convention
`kind`), manifest-registered, with a `check_avatar_state_derivation_table`
parity check: outputs set == the six FR-019 states; `media_states` set == the
closed ten; every landed deterministic seed resolves to its stated avatar
state under the table's precedence rules; the named reachability combinations
are exactly what gate (ix)(a) consumes. Rationale: the candidate is already
authored to this shape; `docs/avatar-first-ui-standard.md` §15 stays the
axis-ownership law and gains only a pointer, keeping the standard stable.

**D4 — OQ ratification is a gated task, not a design-time decision.**
The P1 candidate's §8 enumerates OQ-1..OQ-6 (handoff/interrupted signal
binding, terminal→listening, gate wiring, `governed_action_pending`→`thinking`,
unknown-enum fail-closed target). Each is ratified in-task against cited
sources with the default posture: the normative invariants win; any unsourced
mapping (OQ-6's `blocked` target explicitly) is ratified with a citation or
replaced. Product-owner sign-off required before the table is marked landed.

**D5 — Fixture anchoring is additive rows + validator parity, no new
mechanism.** The candidates already carry evidence ids that resolve against
existing acceptance-map rows (panel-verified). Where a fixture discharges a
scenario currently `deferred`/successor-routed, the wiring is an additive
evidence-register entry — never an in-place flip (locked decision 7). The
upstream validators are the arbiter: landing is complete only when
`validate-avatar-client.py` and `validate-avatar-first-ui.py` (baseline +
realization) pass with the new artifacts present.

**D6 — Status-header transformation at landing.** Drafts carry
`Status: draft-for-factory-handoff`; landed copies adopt the released
deterministic-seed header convention with a provenance line (source branch +
commit + panel evidence pointer). Byte-content otherwise lands verbatim from
`3a8fbd5`; any rework found necessary goes back through a fix + re-validation
cycle, never silent edits.

## Risks / Trade-offs

- [Title/count drift between candidate register and the capability spec while
  `implement-avatar-client-lab` is still active] → the fail-closed title check
  runs at landing against the current delta AND is re-run at that change's
  promotion; any drift fails the release cut, not the consumer.
- [Revision-arithmetic or schema regressions sneaking in during
  transformation] → land verbatim from the confirmed commit; upstream
  validators re-run as the authoritative gate; no hand edits outside the
  Status-header swap (D6).
- [Manifest/release collision with concurrent changes in the shared checkout]
  → the in-flight ideation changes touch no `contracts/` paths; re-check
  `git status -sb` + `openspec list` immediately before the release-cut task;
  explicit-path staging throughout.
- [Option B adds a second pinned evidence input to the app] → accepted;
  retiring the interim guard (a whole checklist + split-locus faithfulness
  mechanism) is a net simplification.
- [OQ ratification could stall the whole change] → OQs gate only the P1
  artifacts; fixture landings and P10 are independent and sequenced first.

## Migration Plan

Additive-only; no rollback machinery needed. Order: fixtures (P7/P8/P11,
P12/P13) → P10 register → P1 table (OQ gate) → validator extensions → release
cut `contract-v1.12` (manifest + changelog + successor-register registration)
→ realization: codexFactory pin resync + guard retirement + gates green →
SCO-001-S05 flip effective → `implement-avatar-client-lab` free to realize
and archive.

## Open Questions

- None blocking start. D2 (Option B) and D1 (dedicated change) are recorded
  as product-owner-ratifiable at proposal review; flag disagreement before
  the release-cut task, after which they are settled.
