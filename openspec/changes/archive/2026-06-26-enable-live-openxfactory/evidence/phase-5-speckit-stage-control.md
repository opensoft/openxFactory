# Phase 5 Evidence: Spec Kit Stage Control And Clarification Routing

Change: `enable-live-openxfactory-factory`
Phase: 5
Date: 2026-06-26
Decision: PASS

## Scope Verified

Phase 5 verified that Omnigent can run Spec Kit stage control under the canonical ownership model and Hermes approval gates.

The existing implementation in `opensoft/Omnigent-Install` commit `c53f190` was sufficient; no install repo code change was required for this phase.

## Canonical Ownership

The canonical Project Alfa roster defines full role ownership:

| Spec Kit stage | Owner | Consulted / reviewed / executor |
|---|---|---|
| `/speckit.specify` | `LE` | `PO`, `PM`, `CA` |
| `/speckit.clarify` | `LE` | routed by question category; final approval by Hermes |
| `/speckit.plan` | `LE` | `CA`, `LA`, `LC`, `LQ`, `LI`, `LS` |
| `/speckit.tasks` | `LC` | reviewed by `LE`, `LQ` |
| `/speckit.analyze` | `LE` | reviewed by `CA`, `LA`, `LQ`, `LS` |
| `/speckit.implement` | `LC` | executor `coder_agents` |

The reduced Project Alfa smoke maps canonical roles into a smaller first-test roster:

| Reduced agent | Canonical role coverage |
|---|---|
| `M1` | `PO`, `PM` |
| `A1` | light `CA`, `LA`, light `LI`, light `LS` |
| `E1` | `LE` |
| `C1` | `LC`, coder agent |
| `Q1` | `LQ` |

This keeps the first live test small while preserving the authority boundaries.

## Clarification Routing

The full Project Alfa routing map covers the live-factory categories:

| Question category | Routed authority |
|---|---|
| product scope / user-visible behavior | `PO` |
| priority / milestone | `PM` |
| cross-system architecture / canonical data ownership / product-wide contracts | `CA` |
| subsystem architecture / local data model / local tech stack / module boundary | `LA` |
| security / tenant isolation | `LS` |
| test strategy / test evidence | `LQ` |
| merge sequencing / integration | `LI` |
| implementation feasibility / coding approach | `LC` |

The reduced clarify smoke routes these categories to the folded Project Alfa agents while keeping the coder role out of product, architecture, security, and test-policy decisions.

## Commands Run

From `opensoft/Omnigent-Install`:

```bash
python3 scripts/validate_speckit_control.py
./scripts/smoke-speckit-control.sh
python3 scripts/validate_first_test.py
./scripts/smoke-hermes-approval.sh
./scripts/smoke-non-doc-stage-gates.sh
```

Results:

```text
OK Spec Kit control fixtures
OK Spec Kit control smoke
OK Project Alfa first-test clarify routing artifacts
OK Hermes approval smoke
OK non-doc pilot contracts
OK non-doc stage-gate contracts
OK non-doc stage-gates smoke
```

## Acceptance Checks

| Requirement | Result | Evidence |
|---|---:|---|
| All Spec Kit stages have explicit owners | PASS | `validate_speckit_control.py` and `stage-routing.example.yaml` |
| Clarification questions route to mapped authority roles | PASS | `validate_first_test.py`, Project Alfa roster |
| Answer packets require Hermes approval before application | PASS | `smoke-hermes-approval.sh`, `smoke-non-doc-stage-gates.sh` |
| Project Alfa clarify test runs with reduced agent set | PASS | `validate_first_test.py` and Hermes clarify approval smoke |
| Coder agent does not decide product, architecture, security, or test policy | PASS | Reduced roster routes those categories to `M1`, `A1`, or `Q1`; `C1` is limited to implementation/coding feasibility. |

## Stop Conditions Checked

| Stop condition | Result |
|---|---|
| Continue before Hermes approval | PASS |
| Spec Kit stage without artifact | PASS |
| Missing approval request | PASS |
| Missing traceability from feature to Spec Kit artifact | PASS |
| Coder assigned policy decision category | PASS |

## Remaining Work

Phase 5 proves stage control and routing. Later phases still need to run the live Project Alfa pilot through branch, PR admission, Merge Council, Merge Master, CloudPC worker packaging, auth restore, memory helper integration, and DR.
