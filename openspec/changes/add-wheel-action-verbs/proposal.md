---
code_surface: codexFactory (gate-console verbs + engine guards, executing loopback routes, CLI entrypoints, the wheel's WHEEL_ACTIONS / ACTION_MOUNTERS expanded-tile rows), openxFactory (gate-intent + gate-action-record additive enum/target extension)
target_release: next additive contract bundle (allocated at realization per docs/contract-versioning-policy.md)
---

# Proposal: add-wheel-action-verbs

## Why

The wheel grew an expanded-tile action row (2026-07-25) and `propose`
(`add-propose-verb`) is the only verb mounted in it. The row is the
dashboard's action surface from here on, and it is empty on three of the
four columns a human actually works: a cluster tile offers nothing, a
possible tile offers only the dispose tray's verdict buttons, and a
proposal tile still cannot be sent back — `demote` has existed in the
gate-console engine since the dashboard landed but was scoped
descriptor-only when the local action center shipped
(`add-ideation-intent-plane` task 3.1 executed `dispose-possible` and
`ratify` only; `propose` joined later).

Brett ruled four verbs into the row on 2026-07-25. Two shapes cover them.
`demote` is an EXISTING engine capability that only lacks transport: it
plans and records the reverse transition and never touches the live corpus
(the corpus mutation is a separate human-run execution step), so promoting
it costs a route and a button, not new semantics. The other three are
GENERATIVE — organizing a possible into a staging fragment, deriving new
possibles from a cluster, researching a possible before the human rules on
it. None of them is a mechanical write the dashboard could perform, so
none of them may BE the work; each must COMMISSION it, exactly as
`propose` commissions proposal authoring: the gate records a
`workflow-job` descriptor plus a `gate-action-record`, a lane or session
fulfils it, and the dashboard never authors.

Without this the action row stays a one-verb demo and every generative
step remains a terminal-only act with no governed trace of who asked for
it.

## What Changes

- ADD gate-console verb `promote-to-staging` (possibles wheel): a
  human-only recorded dispatch that commissions the organization of one
  ACCEPTED possible into `ideation/staging/<topic>/` as a fragment —
  `workflow-job` descriptor (default workflow `staging-fragment-authoring`,
  target `possible_id`, optional proposed topic slug) plus a gate-action
  record. It authors no fragment and mutates no register: the possible's
  `latent → picked` pick edge lands when the commissioned fragment is
  delivered, never at commission time.
- ADD gate-console verb `derive-possibles` (clusters wheel): a human-only
  recorded dispatch that commissions a CLUSTER-SCOPED run of the ratified
  possibles-derivation lane (`add-possibles-derivation-lane`) —
  `workflow-job` descriptor (workflow `derive-possibles`, target
  `cluster_id`) plus a gate-action record. The lane's contract is unchanged
  and not restated here: derived entries still arrive `pending_review` with
  `origin: ai-derived`, still merge on a later run, and still require a
  human disposition. The verb only scopes and records a run.
- ADD gate-console verb `research-brief` (possibles wheel): a human-only
  recorded dispatch that commissions an evidence brief for a possible
  BEFORE the human rules on it — sources, prior art, and overlap with
  existing capabilities and specs — whose output lands as
  staging-compatible material accompanying the possible. It never disposes,
  never edits the register entry, and is never a precondition for a
  disposition.
- PROMOTE `demote` from descriptor-only to an executing dashboard verb:
  `POST /actions/gate/demote` plus an expanded-tile button on the wheel
  column whose tiles carry a change id, under the same capability gate as
  `propose` (loopback + real checkout + resolved actor locally; hosted
  clicks ride `add-ideation-intent-plane`'s intent transport unchanged).
  The route plans and records — transition manifest, executable plan,
  register-update note, gate-action record, `reason` required — and the
  file moves stay the separate human-run execution step the engine already
  implements.
- EXTEND (additive, no `contract_schema_version` bump)
  `gate-intent.schema.yaml` and `gate-action-record.schema.yaml`: the three
  new verbs join the verb/action enums, `target` grows `cluster_id`, and
  per-verb conditionals require `promote-to-staging → target.possible_id`,
  `research-brief → target.possible_id`, `derive-possibles →
  target.cluster_id`, and (record-side) a `workflow-job` companion artifact
  for all three — the same lockstep growth `propose` performed for
  `topic_id`. `demote` needs no schema change: it is already in both enums
  with its `change_id` target and required `reason`.
- GUARDS (every verb): human-only (HumanGate); target existence in the
  pinned checkout / snapshot; structured refusal that persists nothing; no
  duplicate commission — a second dispatch is refused while an earlier
  `workflow-job` for the same verb and the same target remains undelivered.
  `promote-to-staging` additionally refuses a possible that is not
  promotable: promotion presupposes an accepted disposition, so a
  `pending_review` derived possible must be disposed first, and a
  `rejected` / `superseded` / already-`picked` possible is refused.

## Impact

- Affected specs: `ideation-dashboard` (four ADDED requirements, one per
  verb). No MODIFIED requirement: the executing-verb set is nowhere a
  stated requirement (it was scoped in `add-ideation-intent-plane`'s task
  3.1, not in its delta), and the dashboard delta's "Human gate console"
  requirement already reads demote as a governed-tooling reverse transition
  — this change only fixes WHERE the human clicks it and records that the
  execution half is the second step the engine already separates (see
  design D1).
- Affected schemas: `contracts/schemas/gate-intent.schema.yaml`,
  `contracts/schemas/gate-action-record.schema.yaml` (additive only; every
  existing record and intent stays valid).
- Affected code (codexFactory, Speckit-side): `gate_console.py` (verb
  constants, `build_gate_action_record` gains `cluster_id`, promotability
  guard), `kickoff.py` (three commission dispatches + a generalized
  undelivered-commission index), `cli.py`, `gate_routes.py`
  (`EXECUTING_VERBS` gains all four), `views/wheel-model.js`
  (`WHEEL_ACTIONS` rows for `clusters`, `possibles`, and the change-bearing
  column) and `views/wheel.js` (`ACTION_MOUNTERS`), tests.
- NOT in scope: the three fulfilment lanes themselves (the workflows the
  job descriptors name — `staging-fragment-authoring`,
  `possible-research-brief`, and the cluster-scoped entrypoint of the
  existing `derive-possibles` lane). Until they exist a dispatched job is a
  recorded, visible commission a terminal session fulfils by hand — the
  same interim posture `propose` carries today and `kickoff` carried before
  its realization workflow ran.
- Compatibility: no verb removed, no existing verb's semantics narrowed,
  no `schema_version` bump; the hosted plane needs no contract change
  because the new verbs ride the intent transport as ordinary verbs under
  the inbox's per-actor allowlist.
