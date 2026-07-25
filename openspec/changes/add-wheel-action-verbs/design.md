# Design: Wheel Action-Row Verbs

## Context

The wheel's expanded tile (2026-07-25) mounts its action row from ONE pure
table — codexFactory `views/wheel-model.js` `WHEEL_ACTIONS[wheelKey]` with a
`visible(item, env)` predicate — plus ONE DOM mounter per verb in
`views/wheel.js` `ACTION_MOUNTERS`. `propose` (`add-propose-verb`) is the
only row in it. The engine side already has the shapes both new kinds of
verb need: `gate_console.demote` plans + records a reverse transition
without touching the corpus, and `kickoff` / `propose` write a
`workflow-job` descriptor plus a gate-action record for work that runs
elsewhere. So this change is transport + guards + two additive schema
enums, not new machinery.

Brett's four rulings (2026-07-25) split cleanly: ONE existing engine verb
needs a route and a button; THREE new verbs are generative and therefore
recorded commissions.

## Goals / Non-Goals

**Goals**: every wheel column a human works offers its next legal act in
the action row; each act leaves a governed trace naming the human who asked
for it; generative work is commissioned, never performed by the dashboard;
schema growth stays additive so no existing intent or record is invalidated.

**Non-Goals**: the three fulfilment lanes (out of scope — a dispatched job
is fulfilled by a terminal session in the interim, `propose`'s posture); any
change to the ratified possibles-derivation lane contract; any new write
authority on the hosted plane (the verbs ride the existing intent
transport); edit-apply (a multi-step redline flow, still descriptor-only).

## Decisions

### D1 — demote: the button moves, the semantics do not
`demote` is already in both schema enums with a `change_id` target and a
required `reason`, and the engine already separates PLAN+RECORD (the console
action) from EXECUTE (`execute_demotion_plan`, run by a human). Promoting it
to an executing route therefore adds no semantics: the route writes the
transition manifest, executable plan, register-update note, and gate-action
record, and the file moves stay the second, human-run step.

This is compatible with the dashboard delta's "Human gate console"
requirement ("the reverse transition executes via the governed tooling") —
the executable plan IS that governed tooling, run deliberately — so no
MODIFIED requirement is needed; the ADDED requirement states the split
explicitly so no future reader mistakes the click for the move.

**Affordance column** (confirm at realization): the ruling named "the
staged wheel", but `demote`'s target is a change id and a staged tile has no
change to demote — a staged pick is already in staging. The button is
therefore specified on the wheel column whose tiles carry a change id (the
proposals column), whose demotion RETURNS the change to the staged column.
If Brett intended the staged tile to host a same-topic "pull the proposal
back" shortcut, that is an affordance placement change only — same verb,
same route, same record.

### D2 — Three commissions, one mechanic
`promote-to-staging`, `derive-possibles`, and `research-brief` all follow
`propose`: a `workflow-job` descriptor (verb-specific workflow id + the
target id) plus a gate-action record whose `artifacts` contains that
descriptor. The dashboard authors nothing. This keeps ONE audit shape across
kickoff/propose and the three new verbs, and it keeps the console's
authority boundary intact — commissioning is a record, not a mutation.

Duplicate-commission refusal generalizes `propose`'s undelivered-job scan
(`dispatched_propose_topics`) into one index keyed by (verb, target id), so
each verb's refusal is the same rule rather than three copies.

### D3 — Promotion presupposes an accepted disposition
Promotion is the organize-gate act, and the register kernel already fixes
what is promotable: an ai-derived possible stays `pending_review` until a
human disposes it, and an ACCEPTED one becomes a first-class `latent`
possible that "thereafter follows the normal pick lifecycle"
(`add-possibles-derivation-lane`). So the guard is state-derived, not new
policy: `latent` is promotable (a human-authored possible is accepted by
construction; an ai-derived one must carry an accepted human disposition);
`pending_review` is refused with "dispose it first"; `rejected` /
`superseded` are refused (a revived candidate is a NEW entry with a new id,
per that same ratified rule); already-`picked` is refused as a duplicate of
its own pick edge.

This makes `dispose-possible` a strict upstream of `promote-to-staging` —
the same relationship `ratify` has to `kickoff` — enforced as a console
precondition across records, not as a schema shape.

### D4 — The commission does not move the register
`promote-to-staging` records a commission; it does NOT write the
`latent → picked` pick edge. The pick edge requires `pick.staging_id` — the
staging topic that does not exist until the fragment is authored — so
writing it at commission time would either fabricate an id or leave an
invalid entry. The fulfilling lane/session delivers the fragment and the
pick edge together, and until then the possible stays `latent` with a
visible dispatched commission. Same reason `propose` does not stamp a
`change_id` on the staged tile.

### D5 — derive-possibles scopes a run, it does not re-specify the lane
The lane is already ratified (bounded read-only worker, versioned prompt,
orchestration-authoritative identifiers, `pending_review` candidates,
concurrency-protected next-run merge, evidence commits). The verb adds
exactly one thing: a human-initiated, cluster-scoped invocation with a
governed record of who asked. The requirement therefore REFERENCES the lane
contract and restates only the invariants a reader of the dashboard
capability must not lose (candidates arrive `pending_review`; nothing
auto-promotes). New `cluster_id` target field, mirroring `propose`'s
`topic_id` addition.

### D6 — research-brief is pre-verdict and non-binding
The brief exists to make a disposition better informed, so it is
commissionable while the possible is still undisposed — the one commission
verb whose legal window is BEFORE a human ruling. Two guardrails follow:
the brief may not touch the register entry (no autonomous evidence pins, no
disposition), and it may never become a precondition for disposing (a human
can always rule without one). Output lands as staging-compatible material
accompanying the possible so that, if the possible is later promoted, the
brief is already in the shape the staging fragment wants.

### D7 — Fulfilment lanes deliberately out of scope
Three job kinds are dispatched with no worker behind them
(`staging-fragment-authoring`, `possible-research-brief`, and a
cluster-scoped entrypoint for the existing `derive-possibles` lane). This is
the accepted interim: a recorded commission a terminal session fulfils by
hand is strictly better than an unrecorded terminal act, and it is exactly
how `kickoff` and `propose` shipped. Each lane exits later on its own
change, with the descriptor it must consume already contracted.

## Risks / Trade-offs

- **Undelivered commissions accumulate.** Nothing marks a job delivered
  until a fulfilment lane exists, so the duplicate-refusal guard can lock a
  target after a manually fulfilled commission. Mitigation: the descriptor's
  status field is human-editable in the checkout, and the refusal message
  names the blocking descriptor path.
- **Promotability is computed from the register, which the snapshot mirrors
  with bake latency.** A stale view can offer a promote button on a possible
  disposed moments ago; the engine revalidates against the checkout and
  refuses, and the hosted path adds the intent plane's stale-view refusal.
- **Four buttons on three columns raises the accidental-click surface.** The
  gate capability (loopback + real checkout + resolved actor) and the
  session retirement of a commissioned verb keep the row honest; `demote`
  additionally cannot fire without a typed reason.

## Open Questions

1. `demote`'s host column (D1) — proposals column as specified, or a
   staged-tile shortcut as the ruling's wording could be read. Cheap to
   change; no contract impact.
2. The staging-fragment workflow's topic-slug policy: does the human name
   the destination topic at commission time (optional arg, as specified) or
   does the fulfilling lane propose it? Both fit the descriptor.
3. Whether `research-brief` output should be indexed as evidence for the
   possible once a human reviews it — deferred to the brief lane's change,
   which owns the material's shape.
