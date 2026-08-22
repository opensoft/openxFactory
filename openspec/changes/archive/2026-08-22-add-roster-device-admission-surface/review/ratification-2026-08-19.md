# Proposal Ratification: add-roster-device-admission-surface

Status: ratified
Decision date: 2026-08-19
Ratifier: Brett (repository owner)
Ratified baseline: this change as committed in the ratification commit carrying
this record (proposal.md, design.md, tasks.md,
specs/client-identity-roster/spec.md — validated `--strict` and `--all --strict`,
64/64).

## Decision

Brett ratified the extension of the client-identity-roster closed
admission_surface vocabulary to admit the `device` (node-inventory) surface,
after a clarify round (four architect rulings) and a cross-model adversarial
review (F1 fixed pre-ratification; F2 accepted). This ratification authorizes
the realization tasks §1–§5 (schema member + bundle bump + example + digest);
it lands no schema, bundle, or merge by itself.

## What was ratified

- **`device` as ONE tenant-wide read admission surface** covering Entra
  registered devices + Intune managed devices + Windows 365 Cloud PCs (not
  three surfaces). Its governed unit is the tenant device estate, so
  tenant-wide read is the GOVERNED scope — `exceeds_governed_unit: false`, no
  `declared_excess`, no `spanned_surfaces` — not provider-forced excess.
  Admission act: admin consent for the read-only application roles
  `Device.Read.All` + `DeviceManagementManagedDevices.Read.All` +
  `CloudPC.Read.All` on one registration; `enforcement_mode: logic_enforced`
  (no provider scoping selector like Exchange's RestrictAccess); read-only.
- **The spec delta is archive-faithful:** the promoted requirement "Identities
  are enumerated by admission surface, not by product name" is restated
  VERBATIM (heading + body + both existing scenarios, diff-confirmed) with
  ONLY one added scenario, "The device (node-inventory) surface is admitted."
  No other promoted requirement changes.
- **Additive:** adding a `oneOf` const is back-compatible — no
  `contract_schema_version` bump; the realization bumps the bundle
  contract-v1.34 → contract-v1.35 with a digest refresh.

## Conscious-acceptance notes (Brett, at ratification)

1. `device` as one surface (vs three) — grounded in the roster's own design
   Decision 3 (provider-forced breadth is one narrow identity, not multiple
   surfaces); here refined to "governed tenant-device-estate scope, not
   excess."
2. **F2 — read/mutate taxonomy:** admitting `device` reslices the schema's
   extension-route prose so `device` is the READ surface for
   Entra/Intune/Windows 365, while endpoint-MUTATION and Entra-DIRECTORY remain
   SEPARATE FUTURE surfaces with their own governing changes. Accepted.

## Adversarial review

Cross-model review (2026-08-19): per-requirement archive fidelity verified by
byte diff (clean); one-surface coherence, additivity, validator interaction
(a `device` entry with `per_unit_principal_available: {device: false}` +
`logic_enforced` acts validates cleanly), downstream negative integrity
(`sharepoint` stays the out-of-vocab negative), and scope fence all survived.
One MAJOR — F1, the schema-impossible `spanned_surfaces` framing in
design/proposal/tasks — was FIXED before ratification (re-expressed as governed
tenant-device-estate scope). One MINOR — F2 — accepted (above).

## Next

Realization (tasks §1–§5): add the `device` `oneOf` member to
`contracts/schemas/xfactory-client-identity-roster.schema.yaml`, keep the
validator's `EXTENSION_ROUTE` refusal string in sync (the vocab is derived
from the schema — no vocab-constant edit), add a packaged `device` example
(the governed-tenant-scope shape), bump the bundle to contract-v1.35 with a
digest refresh + CHANGELOG, validate green. Then the change PR merges, and
OpsxFactory's node-inventory device roster entry + its §6 consent ceremony
(closing managed-node-inventory 5.x) become unblocked downstream.
