# ideation-dashboard

## ADDED Requirements

### Requirement: Register-edit fulfilment lane
The dashboard runtime SHALL provide a fulfilment lane for dispatched `project-register-edit` commissions that applies each recorded edit to the aggregation-owned project register, validates the result against the pinned schema BEFORE writing, stamps the descriptor `delivered` with when and by what, and then commits only the register file and pushes — refusing and reporting (descriptor left `dispatched`) whenever the live register can no longer satisfy the commission or the write cannot land. The lane SHALL be runnable once, as a watching job, and from a loopback-only human-gated serve route behind a header affordance that appears whenever pending commissions exist; only recorded commissions are ever applied.

#### Scenario: A pending commission is applied
- WHEN the lane runs with a dispatched create-project or edit-project descriptor whose edit the live register can satisfy
- THEN the register file gains exactly that edit, the pinned validator passes before the write, the descriptor flips to `delivered` with `delivered_at` and `delivered_by`, and the register commit carries only the register file

#### Scenario: A stale commission refuses and reports
- WHEN a descriptor's edit can no longer be satisfied (the project vanished, a member conflict arose) or validation fails
- THEN the register is unchanged, the descriptor stays `dispatched`, and the run's report names the commission and its reason

#### Scenario: The button applies on demand
- WHEN a human clicks the apply affordance on the loopback gate console
- THEN the serve runs the same lane code once and reports what was applied and what was skipped
- AND the affordance is absent off the gate capability and when nothing is pending

#### Scenario: The watcher fulfils unattended
- WHEN the lane runs in watch mode beside a serve
- THEN each polling tick fulfils whatever commissions have been recorded since the last, with the same validation and refusal semantics
