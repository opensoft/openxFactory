# capability-health Delta: Proofs, Sentinels, Drift, And Honest Accounting

## ADDED Requirements

### Requirement: The Proof Ladder Precedes Authority
A capability SHALL discharge its decision's proof obligations in order —
replay parity against the acceptance corpus, shadow parity dry-running
beside live AI solves, then a canary cutover — each stage a
workflow-gate-contract instance with rung-scaled profiles, before its
authority block may serve any instance.

#### Scenario: Replay comes before shadow

- **WHEN** a capability's corpus replay has not passed
- **THEN** no shadow stage may begin and the registry status stays
  `building`

#### Scenario: Proofs discharge the decision's obligations

- **WHEN** a funded decision declared `replay-parity` and
  `shadow-human-compared-14d`
- **THEN** the promotion gate MUST cite both discharged obligations

### Requirement: Demotion Triggers Arm At Promotion
Every promotion to authority SHALL ship an armed demotion trigger bundle
(post-condition breach rate, sentinel disagreement rate, fence-miss
surge, dependency advisory), and a capability serving without armed
triggers is nonconformant — authority without a wired exit is a gate
failure.

#### Scenario: No triggers, no authority

- **WHEN** a registry record reaches `active` with no demotion trigger
  bundle reference
- **THEN** the record is invalid and MUST be rejected

### Requirement: Disagreements Are Adjudicated Bidirectionally
Parity and sentinel disagreements SHALL be adjudicated through one shared
record kind whose verdict may fault the capability (consequence: a corpus
counterexample), the historical AI episode (consequence: an episode
relabel), or the spec (consequence: a spec revision) — a disagreement is
evidence, never an automatic strike against the capability.

#### Scenario: Sometimes the code is right

- **WHEN** adjudication finds the AI-path comparison run was the sloppy
  one
- **THEN** the consequence MUST be an episode relabel through the
  pattern ledger's outcome-label stream, not a capability finding

#### Scenario: Verdict and consequence pair

- **WHEN** an adjudication record's verdict is `capability_wrong` with a
  consequence other than a corpus counterexample
- **THEN** the record is invalid and MUST be rejected

### Requirement: Sentinels Are Mandatory While Authoritative
Every capability holding authority SHALL carry a sentinel policy routing
an ε fraction of its family's instances to the AI path — adaptive, with a
floor strictly above zero, a declared per-family mode (dual-run,
async-replay, or takeover), and its spend declared as exploration expense
— because drift detection, corpus freshness, and savings counterfactuals
all die without it.

#### Scenario: A zero floor is invalid

- **WHEN** a sentinel policy for a serving capability declares ε floor 0
- **THEN** the policy is invalid and MUST be rejected

#### Scenario: Sentinel runs are labeled

- **WHEN** an instance is routed to the AI path by the sentinel policy
- **THEN** its dispatch record carries fallback cause `sentinel` and its
  episode enters the pattern ledger like any other

### Requirement: Drift Responds Up A Cost-Ordered Ladder
Drift signals SHALL be answered by the cheapest adequate response in the
order observe → shrink fence → regenerate from a refreshed corpus →
demote rung → retire, with hysteresis (re-promotion thresholds stricter
than the demotion triggers that fired), and regeneration — never hand-
patching — is the default repair because the pipeline, not the artifact,
is the durable asset.

#### Scenario: The fence shrinks before the capability dies

- **WHEN** fence-miss and breach signals concentrate in one input region
- **THEN** the first response is retreating the fence to the proven core
  while misses fall back to the AI path

#### Scenario: Hysteresis prevents flapping

- **WHEN** a demoted capability seeks re-promotion
- **THEN** the re-promotion thresholds MUST be stricter than the trigger
  that demoted it

### Requirement: Findings Split Auto-Actionable And Contested
Capability-health findings SHALL carry one of two classes — auto-
actionable (fence shrink within policy, sentinel rate bump, regeneration
under budget) executed without approval, and contested (demotion,
retirement, anything spending beyond policy) requiring a cited decision
or disposition — doc-health's operational sibling.

#### Scenario: A contested finding waits for its disposition

- **WHEN** a health report proposes retirement
- **THEN** the finding is `contested` and no retirement occurs until a
  disposition or decision is cited

### Requirement: Disused Capabilities Retire With Lineage
A capability whose family has stopped recurring SHALL be proposed for
retirement on the disuse dial's clock, and retirement SHALL preserve the
registry record, provenance chain, and history — archived, never deleted,
because audit continuity outlives authority.

#### Scenario: A zombie is proposed, not deleted

- **WHEN** a capability is dormant beyond the disuse window
- **THEN** a contested retirement finding is filed
- **AND** on retirement the record and lineage remain resolvable

### Requirement: Savings Are Sentinel-Anchored And Predictions Are Scored
A savings entry SHALL be `verified` only against a fresh sentinel-
anchored counterfactual (a stale or missing anchor reports
`unverifiable`, never an estimate dressed as fact), full costs (build
amortization, maintenance, sentinel spend, dispatch overhead) SHALL be
netted out, and every ex-ante prediction — forecasts, build estimates,
half-lives — SHALL be scored at maturity with the scores feeding priors;
automation share is the headline portfolio metric.

#### Scenario: No self-graded savings

- **WHEN** a savings entry claims `verified` without a fresh sentinel
  anchor reference
- **THEN** the entry is invalid and MUST be rejected

#### Scenario: A matured prediction is graded

- **WHEN** a forecast or build estimate passes its maturity date
- **THEN** a calibration score MUST be recorded and marked as feeding
  the priors

### Requirement: Renewal Write-Backs Close The Flywheel
The steward's exhaust SHALL flow back to the pattern ledger as a
contractual obligation — fallback episodes with causes, sentinel episodes,
adjudication relabels, and calibration scores — and a deployment without
the renewal write-backs is nonconformant, not merely incomplete.

#### Scenario: Fallbacks become frontier evidence

- **WHEN** a fence-miss fallback is solved successfully by the AI path
- **THEN** its episode MUST enter the pattern ledger keyed to the family
  so fence widening has evidence

#### Scenario: A write-back gap is a conformance finding

- **WHEN** a steward deployment serves instances but writes no episodes,
  adjudications, or scores back to the ledger
- **THEN** the deployment is nonconformant regardless of its savings
