---
code_surface: codexFactory (propose dispatch in the kickoff module, gate-console verb + CLI + executing local route, staged-tile propose affordance in the wheel), openxFactory (gate-intent + gate-action-record additive enum/target extension)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
Status: ratified
Ratified: 2026-08-01 — record: the archive act, commit `583bd6e` "Archive add-propose-verb (promote the propose verb into ideation-dashboard)", which applied this change's spec delta into `openspec/specs/ideation-dashboard/spec.md`; a change whose spec deltas have PROMOTED is ratified by construction, the derivation `bdd09c2` records and `openspec/changes/archive/2026-08-22-add-doxbench-editing-phase-b/proposal.md` cites. STATED PRECISELY, because the register examined this record once already and left it headerless: this packet carries NO `.openspec.yaml` at all, and C2's finding stands word for word — "Nothing. Its front matter, its whole directory, its created and archive commits, and its README row name no ratifier and no ratification date"; task 4.3's "Brett sign-off same day" is a verification pass on the first real commission, not a ratification, and nothing here cites either. What C2 did not have is OQ-6's 2026-08-23 ruling and the phase-b derivation, which make the archive act itself the citable record. The date is the archive folder's own 2026-08-01; the commit carries the 2026-07-31 authoring date. Backfilled 2026-08-23 by `govern-openspec-corpus-membership` slice 5C under OQ-6's ruling that every headerless proposal is derived from its own record; no approving OpenSpec change exists to name, so this is the record-citing spelling. See tasks.md "Bookkeeping correction".
---

# Proposal: add-propose-verb

## Why

The gate console covers every lifecycle boundary EXCEPT the first one a
human actually drives: taking a staged topic to an OpenSpec proposal.
Today's verbs act on changes that already exist (demote / edit-apply /
ratify / kickoff) or on register possibles (dispose-possible); the
staging→proposal transition has no verb, no CLI, no button — it happens
only when someone opens a terminal session and authors the change by hand.
Brett's direction (2026-07-24, action-center session): the dashboard should
let a user take a staging tile to a proposal.

The step is NOT a mechanical write — a proposal means authored deltas,
design decisions, tasks, and strict validation. So the verb cannot BE the
authoring; it must COMMISSION it. The console already has exactly this
shape one boundary later: `kickoff` dispatches a recorded workflow job for
a ratified change without executing anything itself. `propose` is the same
recorded-dispatch mechanic pointed at the staging→proposal boundary.

## What Changes

- ADD gate-console verb `propose`: a human-only, recorded dispatch that
  commissions proposal authoring for one staging topic. It writes a
  `workflow-job` descriptor (default workflow `proposal-authoring`,
  targeting the topic's `staging_id`) plus a `gate-action-record`, exactly
  kickoff's mechanics; the authoring itself runs externally (an agent lane
  delivering via the rolling-PR pattern) and lands as an ordinary OpenSpec
  change for human review and ratification.
- EXTEND (additive, no schema_version bump) `gate-intent.schema.yaml` and
  `gate-action-record.schema.yaml`: `propose` joins the verb/action enums,
  `target` grows `topic_id`, and per-verb conditionals require
  `propose → target.topic_id` and (record-side) a `workflow-job` companion
  artifact — the same lockstep growth the schemas already document.
- ADD the dashboard affordance: a focused staged tile in the wheel offers
  "draft proposal" under the same capability gate as the dispose tray
  (loopback + resolved actor + real checkout locally; intent emission when
  the hosted plane lands — the verb rides `add-ideation-intent-plane`'s
  transport unchanged).
- GUARDS: human-only (HumanGate, like every gate verb); target existence
  (the staging topic directory must exist in the pinned checkout); no
  duplicate commission (an undelivered `propose` job for the same topic
  refuses a second dispatch).

## Impact

- Affected specs: `ideation-dashboard` (ADDED requirement: staged-topic
  proposal commissioning).
- Affected schemas: `contracts/schemas/gate-intent.schema.yaml`,
  `contracts/schemas/gate-action-record.schema.yaml` (additive).
- Affected code (codexFactory): `scripts/ideation_dashboard/kickoff.py`
  (propose dispatch), `gate_console.py` (constants + record builder
  `topic_id`), `cli.py` (`gate propose`), `gate_routes.py` (executing local
  route), wheel view (staged-tile affordance), tests.
- NOT in scope: the proposal-authoring lane itself (the workflow the job
  descriptor names). Until it exists, a dispatched job is a recorded,
  visible commission a terminal session fulfils — the same interim posture
  kickoff had before its realization workflow ran.
