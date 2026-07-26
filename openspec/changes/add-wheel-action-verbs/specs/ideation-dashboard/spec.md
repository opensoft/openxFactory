# ideation-dashboard Delta: Wheel Action-Row Verbs

## ADDED Requirements

### Requirement: Executing demote from the wheel action row
The gate console SHALL expose `demote` as an executing dashboard verb — a loopback-gated executing route and an expanded-tile action-row button on the wheel column whose tiles carry a change id — under the same capability gate as the other executing verbs (real checkout, resolved actor, human gate), and the dashboard invocation SHALL produce exactly the engine's existing demotion artifacts: the transition manifest, the executable plan, the register-update note, and a `demote` gate-action record carrying the required `reason`. The dashboard invocation MUST NOT mutate the live corpus — the file moves remain the separate, human-run execution step of the same governed tooling — and the console SHALL refuse a missing `reason`, a target change absent from the snapshot, and any agent-invoked call, persisting nothing on refusal.

#### Scenario: A proposal is sent back from the action row
- **WHEN** a human activates demote on an expanded tile for a change under the gate capability
- **THEN** the transition manifest, executable plan, register-update note, and `demote` gate-action record are written through the human gate
- **AND** no document in the live corpus is moved or edited by the dashboard call

#### Scenario: An unreasoned demote is refused
- **WHEN** demote is invoked without a reason
- **THEN** the console MUST refuse with the reason requirement and persist nothing

#### Scenario: The execution half stays human-run
- **WHEN** a demote has been planned and recorded from the dashboard
- **THEN** the corpus transition happens only when a human runs the recorded executable plan

#### Scenario: An agent invokes demote
- **WHEN** any agent or automated path calls the demote action
- **THEN** the call MUST be rejected and reported, like every gate action

### Requirement: Accepted-possible promotion to staging
The gate console SHALL offer a human-only `promote-to-staging` action on a possible that commissions the organization of that possible into `ideation/staging/<topic>/` as a fragment — a `workflow-job` descriptor naming the staging-fragment authoring workflow and targeting the possible's register id (optionally carrying a proposed topic slug), plus a `promote-to-staging` gate-action record — and the console MUST NOT author the fragment or mutate the possibles register: the possible's `latent → picked` pick edge is recorded only when the commissioned fragment is delivered, never at commission time. Promotion SHALL presuppose an accepted disposition — the console MUST refuse a derived possible still `pending_review` (it must be disposed first), a `rejected` or `superseded` possible, an already-`picked` possible, and a register id absent from the pinned checkout — and MUST refuse a duplicate commission while a dispatched `promote-to-staging` job for the same possible remains undelivered.

#### Scenario: An accepted possible is commissioned into staging
- **WHEN** a human runs promote-to-staging on an accepted (`latent`) possible
- **THEN** a `workflow-job` descriptor (target `possible_id`) and a `promote-to-staging` gate-action record are written through the human gate
- **AND** the possibles register is unchanged — no pick edge, no state transition

#### Scenario: An undisposed derived possible is refused
- **WHEN** promote-to-staging is invoked on a derived possible whose machine disposition is still `pending_review`
- **THEN** the console MUST refuse, citing the missing human disposition, and persist nothing

#### Scenario: A rejected or already-picked possible is refused
- **WHEN** promote-to-staging is invoked on a `rejected`, `superseded`, or already-`picked` possible
- **THEN** the console MUST refuse with the entry's state as the reason

#### Scenario: A duplicate promotion is refused
- **WHEN** promote-to-staging is invoked for a possible that already carries a dispatched, undelivered `promote-to-staging` workflow-job
- **THEN** the console MUST refuse, citing the existing dispatch

### Requirement: Cluster-scoped possibles-derivation commissioning
The gate console SHALL offer a human-only `derive-possibles` action on a topic cluster that commissions a cluster-scoped run of the promoted possibles-derivation lane as a recorded dispatch — a `workflow-job` descriptor naming the `derive-possibles` workflow and carrying the cluster id, plus a `derive-possibles` gate-action record — without deriving anything itself and without altering that lane's contract: the commissioned run stays bounded and read-only, its candidates arrive `origin: ai-derived` with machine disposition `pending_review`, they merge into the register only through the lane's own concurrency-protected merge, and every verdict on them remains a human act on the dispose tray. The console SHALL refuse a cluster id absent from the snapshot's cluster set and SHALL refuse a duplicate commission while a dispatched `derive-possibles` job for the same cluster remains undelivered.

#### Scenario: A cluster is commissioned for derivation
- **WHEN** a human runs derive-possibles on a cluster tile under the gate capability
- **THEN** a `workflow-job` descriptor (workflow `derive-possibles`, target `cluster_id`) and a `derive-possibles` gate-action record are written through the human gate
- **AND** no register entry is created by the console itself

#### Scenario: The commissioned run auto-promotes nothing
- **WHEN** the commissioned cluster-scoped run delivers candidates
- **THEN** they enter as `pending_review` derived possibles awaiting human disposition, exactly as a nightly lane run's candidates do

#### Scenario: An unknown cluster is refused
- **WHEN** derive-possibles is invoked for a cluster id the snapshot does not carry
- **THEN** the console MUST refuse with the reason and persist nothing

#### Scenario: A duplicate derivation is refused
- **WHEN** derive-possibles is invoked for a cluster that already carries a dispatched, undelivered `derive-possibles` workflow-job
- **THEN** the console MUST refuse, citing the existing dispatch

### Requirement: Pre-verdict research brief commissioning
The gate console SHALL offer a human-only `research-brief` action on a possible that commissions an evidence brief for that possible BEFORE the human rules on it — sources, prior art, and overlap with existing capabilities and specs — as a recorded dispatch: a `workflow-job` descriptor naming the research-brief workflow and targeting the possible's register id, plus a `research-brief` gate-action record. The commissioned brief SHALL be delivered as staging-compatible material accompanying the possible, and it MUST NOT dispose the possible, edit its register entry, or add evidence to it autonomously; a brief SHALL NOT be a precondition for any disposition. The console SHALL refuse a register id absent from the pinned checkout and SHALL refuse a duplicate commission while a dispatched `research-brief` job for the same possible remains undelivered.

#### Scenario: A pending possible is researched before the verdict
- **WHEN** a human runs research-brief on a possible awaiting disposition
- **THEN** a `workflow-job` descriptor (target `possible_id`) and a `research-brief` gate-action record are written through the human gate
- **AND** the possible's disposition state is untouched

#### Scenario: The brief informs, it never decides
- **WHEN** a commissioned brief is delivered
- **THEN** it lands as staging-compatible material referencing the possible and the human still disposes on the gate console

#### Scenario: Disposition never waits on a brief
- **WHEN** a human disposes a possible for which no brief was ever commissioned
- **THEN** the disposition proceeds unaffected

#### Scenario: A duplicate brief is refused
- **WHEN** research-brief is invoked for a possible that already carries a dispatched, undelivered `research-brief` workflow-job
- **THEN** the console MUST refuse, citing the existing dispatch
