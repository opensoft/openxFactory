# ideation-dashboard Delta: Lens Set-Builder Gate Verbs

## ADDED Requirements

### Requirement: Lens set-builder gate verbs
The gate console SHALL offer two human-only verbs that execute a keyword-lens plan through the existing tested engines as recorded dispatches, enforced at the route so the lens plan panel, the CLI, and a direct request are gated identically. `lens-save-recipe` SHALL execute a save-recipe plan verbatim: the `ideation-workbench` manifest is written through the workbench engine (gitignored, schema-validated at write, reasoned-override guard intact) together with a gate-action record. `lens-add-as-cluster` SHALL execute an add-as-cluster plan: the recipe-seeded manifest plus the `pending_review` human-seen submission into the cross-reference queue, with the full evidence contract enforced BEFORE persistence, together with a gate-action record; the generated cross-reference index MUST NOT be written — acceptance remains the disposing authority's governed act outside these verbs. Every refusal the engines already define SHALL surface as a route refusal that persists nothing: a reasonless override, a duplicate set name, a submission lacking evidence, a validation failure (reject-and-report, prior state intact). When the gate capability is live the lens plan panel SHALL offer an execute affordance posting the confirmed plan to the verb route; when it is absent the panel SHALL stay plan-only, exactly as the read-only posture renders today. Agent invocations MUST be rejected and reported, like every gate action.

#### Scenario: A save-recipe plan is executed
- **WHEN** a human confirms a save-recipe plan and executes it through the gate
- **THEN** the workbench manifest is written exactly as the plan displayed — recipe line, members, reasoned overrides — and a gate-action record is persisted
- **AND** the write is schema-validated before landing

#### Scenario: An add-as-cluster plan is executed
- **WHEN** a human confirms an add-as-cluster plan and executes it through the gate
- **THEN** the recipe-seeded manifest and a `pending_review` human-seen entry are persisted, and a gate-action record is written
- **AND** the generated cross-reference index is not modified

#### Scenario: The engine would refuse
- **WHEN** the plan carries a reasonless override, a duplicate set name, a submission lacking its evidence contract, or fails validation
- **THEN** the route MUST refuse with the engine's reason and persist nothing, leaving prior state intact

#### Scenario: The gate capability is off
- **WHEN** the lens renders on a surface without the gate capability
- **THEN** the plan panel MUST render the plan-only confirmation with no execute affordance

#### Scenario: An agent invokes a lens verb
- **WHEN** any agent or automated path calls either verb
- **THEN** the call MUST be rejected and reported, like every gate action
