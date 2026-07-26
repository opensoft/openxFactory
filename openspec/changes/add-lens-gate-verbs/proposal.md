---
code_surface: codexFactory (gate console routes for the two lens verbs, the lens plan panel's execute affordance, tests)
target_release: none
---

# Proposal: add-lens-gate-verbs

## Why

The keyword lens is the dashboard's set-builder: it assembles a keyword
recipe, a membership with reasoned overrides, and then — deliberately, on a
read-only serving layer — stops at a PLAN. Both of its outputs (`save
recipe`, `add as cluster`) render an on-screen confirmation of exactly what
would persist and go no further. The Python write-back engine that executes
those plans has been implemented and tested for weeks (`lens.py` recipe
evaluation + persistence, `workbench.py` manifest engine with the
reasoned-override guard, `human_seen.py` pending-review submission with the
full evidence contract) — but no gate route or CLI verb is wired to it, so
landing a plan today means a terminal call into the engine.

Brett's ruling (2026-07-25, dogfooding the lens): implement the last wire —
the buttons should actually land the manifest/proposal through the local
gate console, as recorded dispatches like propose and dispose.

## What Changes

- ADD two human-only gate-console verbs, enforced at the route so the
  browser button, the CLI, and a direct request are gated identically:
  - `lens-save-recipe` — executes a save-recipe plan verbatim through the
    tested workbench engine: writes the `ideation-workbench` manifest
    (gitignored session artifact, schema-validated at write) and a
    gate-action record. Refuses a reasonless override (the engine already
    does), a duplicate set name, and any validation failure —
    reject-and-report, prior state intact.
  - `lens-add-as-cluster` — executes an add-as-cluster plan: the
    recipe-seeded manifest PLUS the `pending_review` human-seen submission
    into the cross-reference queue (evidence contract enforced BEFORE
    persistence, exactly as `human_seen.py` specifies), and a gate-action
    record. The generated cross-reference index is NEVER written — the
    pending entry awaits the disposing authority, per the existing
    read-through contract.
- UPGRADE the lens plan panel: when the gate capability is live, the plan
  confirmation gains an execute affordance that posts the plan to the verb
  route; with the gate capability off (the deployed static image), the
  panel stays plan-only exactly as today.
- Agent invocations rejected and reported, like every gate action.

## Impact

- Affected specs: `ideation-dashboard` (one ADDED requirement). Stacks on
  the unpromoted `add-ideation-dashboard` capability alongside
  add-propose-verb, add-wheel-action-verbs, and add-staging-workbench —
  sequence the archives knowingly.
- One ADDITIVE schema touch (corrected at realization — the original
  "no schema change" missed it): `gate-action-record.schema.yaml`'s
  `action` enum gains the two verbs and `target` gains an optional `set`
  slug; every prior record stays valid. The artifact contracts themselves
  already exist (`ideation-workbench` manifests; the `human_seen` intake
  $def of `ideation-cross-reference.schema.yaml`).
- Affected code (codexFactory, realization): `gate_routes.py` (two verbs
  beside dispose/ratify/propose), thin glue into `lens.py` /
  `workbench.py` / `human_seen.py` (no engine changes), `views/lens.js`
  (execute affordance on the plan panel, capability-gated), `cli.py`
  parity verbs, tests.
- NOT in scope: an accept/fold verb for the pending human-seen entry (the
  generated index is owned by the cross-reference machinery and the
  dashboard never rewrites it — acceptance stays a governed human edit);
  any change to recipe semantics, override reasons, or the evidence
  contract.
