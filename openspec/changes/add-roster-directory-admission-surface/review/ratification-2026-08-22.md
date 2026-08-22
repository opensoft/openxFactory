# Proposal Ratification: add-roster-directory-admission-surface

Status: ratified
Decision date: 2026-08-22
Ratifier: Brett (repository owner)
Ratified baseline: this change as committed in the ratification commit carrying
this record (proposal.md, design.md, tasks.md,
specs/client-identity-roster/spec.md, .openspec.yaml — validated `--strict` and
`--all --strict`, 66/66; archive fidelity of the MODIFIED delta independently
byte-verified three times).

## Decision

Brett ratified the extension of the client-identity-roster closed
`admission_surface` vocabulary to admit the `directory` (service-inventory)
surface, after a cross-model adversarial review whose four MAJOR findings
(F1–F4) were fixed pre-ratification and five MINOR findings folded in. This
ratification authorizes the realization tasks §1–§5 (schema member + validator
refusal-string sync + packaged example + bundle bump contract-v1.38 →
contract-v1.39 with digest refresh); it lands no schema, bundle, or merge by
itself.

## What was ratified

- **`directory` as ONE tenant-wide READ admission surface** — the tenant's
  directory/service estate (organization profile, subscribed service plans,
  applications, domains), what read-only service-surface DISCOVERY reads. One
  admission act: admin consent for exactly the three read-only application
  roles `Organization.Read.All` + `Application.Read.All` + `Domain.Read.All` on
  one registration (hard-enumerated per F1, matching the device member's
  style), with an explicit exclusion: a broader directory-wide read role such
  as `Directory.Read.All` is OUTSIDE this surface's admission act because it
  also reads the already-admitted `device` surface. Governed unit = the tenant
  directory/service estate, so tenant-wide read is the governed scope:
  `exceeds_governed_unit: false`, no `declared_excess`, `enforcement_mode:
  logic_enforced`, `per_unit_principal_available: {directory: false}`.
- **The extension route is honored**: the closed vocabulary is extended only by
  the change that governs the new surface. The governing change is OpsxFactory
  `add-managed-service-inventory` (ratified 2026-08-21; §1–6 realized and
  merged at OpsxFactory main 824f8ef), and per its ratified F1 ordering this
  extension is proposed on the DETERMINISTIC §1–6 contract, never on a live
  snapshot. The device change's F2 note anticipated this arrival.
- **The spec delta is archive-faithful**: the promoted requirement "Identities
  are enumerated by admission surface, not by product name" restated VERBATIM
  (heading + body + all three existing scenarios, byte-diff-confirmed) with
  ONLY one added scenario, "The directory (service-inventory) surface is
  admitted." No other promoted requirement changes.
- **Read/mutate taxonomy stays sliced**: `directory` is the READ surface;
  Entra-directory MUTATION and endpoint MUTATION remain separate future
  surfaces with their own governing changes.
- **Additive**: a `oneOf` const admission — including the derived, purely
  permissive key-space widening in `per_unit_principal_available` (whose
  `propertyNames` $refs the vocabulary; named per F4, not denied) — requires
  nothing new of any existing record, so no `contract_schema_version` bump.
  Realization bumps the bundle contract-v1.38 → contract-v1.39.

## Adversarial review (2026-08-22, cross-model)

Archive fidelity, the cross-repo citation chain, taxonomy coherence,
realization-task correctness, and downstream consistency (OpsxFactory R-15)
all HELD. Four MAJOR findings fixed pre-ratification:
- **F1** — the "role family" admission-act framing rested on a misread (the
  scope set was pinned at CLASS REALIZATION, already merged) and would have
  admitted `Directory.Read.All` on its face; replaced with hard enumeration +
  the exclusion clause.
- **F2** — the `device` member's own description still called Entra-directory
  READ a future surface; realization task 1.4 amends it so the contract file
  cannot contradict itself.
- **F3** — the schema's "PROMOTED capabilities" grounding has been false since
  v1.35 (both governing changes are ratified-but-unarchived); task 1.3 rewords
  it to RATIFIED. The promoted requirement's change-based route text is met and
  untouched.
- **F4** — the no-bump argument conceded its own defeating clause; repaired to
  name the `per_unit_principal_available` coupling and argue from
  permissiveness (this also repairs the argument inherited verbatim from the
  ratified device design).
MINORs folded: the downstream-insufficiency fence (F5), quotation hygiene (F6),
findable capability naming in the promoted scenario (F7, heading aligned),
pinned citations (F8), the non-Entra successor clause preserved (F9).

## Conscious-acceptance notes (Brett, at ratification)

1. **Landing this change is necessary but NOT sufficient for OpsxFactory §7**:
   OpsxFactory must then re-pin its contract to v1.39 and widen its local
   `ROSTER_ADMITTED_SURFACE_VOCAB` (the device precedent was OpsxFactory
   PR #45), ahead of any `directory` roster entry or live sweep.
2. **Entra-directory MUTATION remains a separate future surface** (the
   `entra_directory_admin` class is deliberately NOT admitted here).
3. The ad-hoc origin's `approved_by` derives from the ratification of the
   governing change; ratification of THIS change is the separate act this
   record performs.

## Next

Realization (tasks §1–§5): the `directory` `oneOf` member (hard-enumerated
admission act + exclusion), the device-member and extension-route rewordings
(1.3/1.4, incl. PROMOTED→RATIFIED), validator refusal-string sync, packaged
example, bundle contract-v1.38 → contract-v1.39 with sha256 recompute +
CHANGELOG + release digests, strict validation. Then the change PR lands, and
the OpsxFactory re-pin + local vocab widening become the first downstream act.
