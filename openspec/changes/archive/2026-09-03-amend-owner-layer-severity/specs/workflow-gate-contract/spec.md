# workflow-gate-contract — amend-owner-layer-severity deltas

## MODIFIED Requirements

### Requirement: Owner layer constraint
Gate and workflow `owner_layer` values SHALL be canonical role names
(`customer`, `client`, `domain`, `xfactory`, or the domain's Omnigent
layer) or a layer id declared in that domain's `stack.yaml` Hermes layers;
any other value SHALL be reported as a validator error.

#### Scenario: A gate names an undeclared layer
- **WHEN** a gate's `owner_layer` matches neither a canonical role nor a declared stack layer id
- **THEN** the validator MUST report an error identifying the gate and the unknown layer
