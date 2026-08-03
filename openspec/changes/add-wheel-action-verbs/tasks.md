# Tasks: add-wheel-action-verbs

## 1. Contracts (openxFactory)

- [x] 1.1 Extend `gate-intent.schema.yaml`: `promote-to-staging`,
      `derive-possibles`, `research-brief` in the verb enum; `cluster_id` on
      `target`; conditionals `promote-to-staging → target.possible_id`,
      `research-brief → target.possible_id`, `derive-possibles →
      target.cluster_id`. Document in the header comment that `demote` is
      unchanged (already enumerated, `change_id` target).
- [x] 1.2 Extend `gate-action-record.schema.yaml`: the same three actions in
      the action enum; `cluster_id` on the `target` $def; conditionals
      requiring each action's target field AND an `artifacts contains
      workflow-job` companion (the propose/kickoff pattern).
- [x] 1.3 Keep the additive posture explicit: no `contract_schema_version`
      bump, no `additionalProperties: false`, header notes naming this change
      as the growth source; confirm every packaged example still validates.
- [x] 1.4 Validate: the delegated dashboard-contract validator
      (`scripts/validate-ideation-dashboard-contracts.py`) plus
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`.
- [x] 1.5 Contract registration (`contracts/manifest.yaml`,
      `contracts/CHANGELOG.md`) at the next additive bundle cut, per
      `docs/contract-versioning-policy.md`.
      Realized 2026-08-02 in the `contract-v1.28` candidate together with
      `add-ideation-intent-plane` 2.4 and `add-worker-enrollment-broker`
      1.11: gate-intent first registration, gate-action-record digest refresh,
      README index update, changelog entry, and closed release digest inventory.
- [x] 1.6 Bundle-cut side repair carried by the same registration commit
      (a6e7563/10d5165/5a1cdc8): the two doxBench wire schemas published at
      `contract-v1.27` re-typed from Hermes semantic members (`type: schema`,
      `semantic_member: true`) to closed release members
      (`type: release-schema`, `semantic_member: false`), `release-schema`
      added to the release-digest-inventory type enum, and the bundle
      verifier widened so release-only schemas carry raw digests AND catalog
      version pins. Wire-schema bytes unchanged; recorded here so the
      catalog-membership correction has an OpenSpec trail (it was previously
      only CHANGELOG prose).

## 2. Engine + routes (codexFactory — Speckit-side realization)

- [ ] 2.1 `gate_console.py`: `ACTION_PROMOTE_TO_STAGING`,
      `ACTION_DERIVE_POSSIBLES`, `ACTION_RESEARCH_BRIEF`;
      `build_gate_action_record` grows `cluster_id`.
- [ ] 2.2 `gate_console.py`: promotability predicate over the possibles
      register — `latent` + (human-authored | accepted human disposition)
      promotable; `pending_review` / `rejected` / `superseded` / `picked`
      refused with the state as the reason (design D3).
- [ ] 2.3 `kickoff.py`: generalize the undelivered-commission scan into one
      index keyed by (verb, target id), replacing
      `dispatched_propose_topics` with the shared helper (propose keeps its
      behaviour).
- [ ] 2.4 `kickoff.py`: `promote_to_staging()` — human-only, register-entry
      existence + promotability guards, duplicate refusal, `workflow-job`
      descriptor (workflow `staging-fragment-authoring`, `possible_id`
      target, optional proposed topic slug) + gate-action record; NO register
      mutation (design D4).
- [ ] 2.5 `kickoff.py`: `derive_possibles()` — human-only, cluster existence
      guard against the snapshot, duplicate refusal, `workflow-job`
      descriptor (workflow `derive-possibles`, `cluster_id` target) +
      gate-action record.
- [ ] 2.6 `kickoff.py`: `research_brief()` — human-only, register-entry
      existence guard, duplicate refusal, legal while the possible is
      undisposed, `workflow-job` descriptor (workflow
      `possible-research-brief`, `possible_id` target) + gate-action record;
      never disposes and never edits the entry.
- [ ] 2.7 `gate_routes.py`: `EXECUTING_VERBS` gains `demote`,
      `promote-to-staging`, `derive-possibles`, `research-brief`; four
      handlers with the dispose-possible response discipline (structured
      refusal, `message` = engine reason, nothing persisted). `demote`
      requires `reason` and returns the recorded plan path — it does NOT
      execute the plan (design D1).
- [ ] 2.8 `cli.py`: `gate promote-to-staging <possible-id>` (`--topic`,
      `--note`), `gate derive-possibles <cluster-id>` (`--note`),
      `gate research-brief <possible-id>` (`--note`); update the existing
      `gate demote` help to name the executing route as its dashboard peer.
- [ ] 2.9 `GateConsole` delegates for the three new verbs, mirroring
      `GateConsole.propose`.

## 3. Wheel action rows (codexFactory — Speckit-side realization)

- [ ] 3.1 `views/wheel-model.js` `WHEEL_ACTIONS`: `clusters` gains
      `derive-possibles`; `possibles` gains `promote-to-staging` (visible
      only when the item is promotable) and `research-brief` (visible while
      undisposed); the change-bearing column gains `demote`. Every row keeps
      the `!!env.gate && !env.commissioned` shape so a commissioned verb
      retires for the session.
- [ ] 3.2 `views/wheel.js` `ACTION_MOUNTERS`: one mounter per new verb;
      `demote` collects the required reason before dispatch; refusals render
      in the refusal panel textContent-only; success decorates the tile as a
      session-local overlay (the snapshot is never mutated).
- [ ] 3.3 Pure-model tests for `actionsFor` across the three columns
      (promotable vs pending vs rejected possible, cluster, change tile,
      gate off, already-commissioned).

## 4. Verification

- [ ] 4.1 Engine + route tests green: accept path per verb, missing target,
      non-promotable possible (each refused state), undisposed-possible
      research brief ACCEPTED, duplicate commission, unreasoned demote,
      agent-path rejection, and demote leaving the corpus untouched.
- [x] 4.2 Schema conformance tests: one valid intent and one valid record per
      new verb; a record missing its `workflow-job` companion rejected; a
      `derive-possibles` record without `cluster_id` rejected.
      (Realized 2026-08-02 in openxFactory as
      `tests/ideation_dashboard/test_wheel_action_contracts.py`: per-verb
      positive intent/record cases, workflow-job-companion rejection, and the
      `cluster_id` rejection, all against the packaged examples/negatives.)
- [ ] 4.3 Live browser check on the local dashboard: each button renders on
      its column's expanded tile under the gate capability with the actor
      resolved, and does not render with the capability off; zero page
      errors.
- [ ] 4.4 First real commission of each verb by Brett recorded end-to-end
      (descriptor + record in the checkout), and one dashboard demote planned
      + executed as two deliberate steps.
