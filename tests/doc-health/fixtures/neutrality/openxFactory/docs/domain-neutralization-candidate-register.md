# Domain Neutralization Candidate Register

Status: staged
Kind: register
Repository context: openxFactory
Purpose: fixture register for the neutrality-drift lane tests — the same
row/section grammar as the real register, with two existing candidates
(the drafted next free id follows the highest number below).

## Candidate List

Status lifecycle: `seed` -> `staged` -> `openspec` -> `implemented` ->
`adopted`, or `rejected` / `deferred` at any point.

| ID | Topic | Decision | Priority | Status | Likely openxFactory artifact |
| --- | --- | --- | --- | --- | --- |
| DTN-001 | Neutral sample envelope | `promote` | P0 | `adopted` | `contracts/schemas/xfactory-sample-envelope.schema.yaml` |
| DTN-002 | Legacy cited tool | `split` | P2 | `seed` | neutral checker skeleton |

## Candidate Details

### DTN-001: Neutral sample envelope

Adopted fixture candidate.

Evidence:

- `contracts/schemas/xfactory-sample-envelope.schema.yaml`

Domain-local exclusions: none.

### DTN-002: Legacy cited tool

Open fixture candidate whose evidence already cites a domain path — the
lane must never re-file a register-cited subject.

Evidence:

- `xFactories/MedxFactory/scripts/legacy/cited-tool.py`

Domain-local exclusions: the legacy invocation wrapper.
