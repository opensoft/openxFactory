---
code_surface: openxFactory (schema/contract)
target_release: implementation_pending
---
# Proposal: add-roster-directory-admission-surface

Status: draft
Proposed: 2026-08-22 on the realization evidence of OpsxFactory
`add-managed-service-inventory` §1–§6, per its ratified F1 ordering — that
change's own ratification records the openxFactory `directory`
admission-surface vocab extension as a PREREQUISITE of its §7 live sweep,
"proposed and justified on the DETERMINISTIC discovery contract landed by §1–6
— NOT on a live snapshot (there is none yet)". §1–§6 are all ticked and merged
(OpsxFactory `main` `824f8ef`, PR #52, 2026-08-22), so the deterministic
contract this extension is proposed on exists.

THE SCHEMA/BUNDLE REALIZATION (tasks §1–§5) RUNS POST-RATIFICATION. No schema,
validator, example, or bundle edit lands with this proposal itself.

## Why

The promoted `client-identity-roster` capability enumerates governed
identities against a CLOSED `admission_surface` vocabulary holding exactly
three members today — `business_central`, `exchange` and `device` — the
client-tenant Entra-homed surfaces whose governing capabilities are PROMOTED.
The schema's own extension-route text states both the rule and the surface
still to arrive: "a surface enters with the promotion of the capability that
governs it (endpoint MUTATION / Intune write and **Entra-directory** arrive
with theirs)". The `device` change's ratified F2 conscious-acceptance note says
the same thing from the other side: `device` is the READ surface for
Entra/Intune/Windows 365 devices, while "Entra-DIRECTORY remains a SEPARATE
FUTURE surface with its own governing change." THIS is that change, arriving
exactly as anticipated.

OpsxFactory `add-managed-service-inventory` is that governing capability:
RATIFIED 2026-08-21 (7 ADDED requirements) and REALIZED §1–§6 (merged
2026-08-22, OpsxFactory `main` `824f8ef`) — the read-only tenant
service-surface DISCOVER capability. Its realized reader class
`microsoft_service_discovery_reader` (OpsxFactory
`credentials/requirements.yaml`) is an app-only workload identity carrying
`admission_surface: directory`, read-only directory/service-enumeration Graph
scopes (`Organization.Read.All`, `Application.Read.All`, `Domain.Read.All` —
the exact EFFECTIVE set pinned at grant time), `exact_effective_scopes: true`
and `reject_write_or_destructive_scopes: true`, minted through the promoted
`tenant-reader-grant-pipeline`. Its `issuance_preconditions` refuse issuance
without an admission-verified roster entry — and no member of the closed
vocabulary admits that entry, because the surface it belongs to, `directory`,
is not yet in the vocabulary.

The cross-repo dependency is already named on the OpsxFactory side, not
invented here. The archived `add-tenant-reader-grant-pipeline` (ratified,
promoted) deliberately DECLINED to define this reader class and deferred it
"to the service-discovery change, which pins its exact read scopes and rides
the openxFactory directory admission-surface vocab extension" — language that
survives in its promoted spec, its design, and its task 2.2 deferral note.

This change admits `directory` — the service-discovery read surface — into the
closed `admission_surface` vocabulary through the exact extension route the
capability defines: the change that governs the new surface adds the member, on
the realization evidence of the deterministic contract. That unblocks
OpsxFactory's `directory` roster entry and the whole of
`add-managed-service-inventory` §7 downstream.

## What Changes

- Admit the single admission surface `directory` (const token) into the closed
  `admission_surface` vocabulary of `client-identity-roster`. `directory` is
  ONE tenant-wide READ surface: one admission act (admin consent for the
  read-only directory/service-enumeration application roles on one Entra app
  registration) and one scoping mechanism (tenant-wide read, no narrower
  provider selector). The provider areas it reads — organization profile,
  subscribed service plans, service principals/applications, verified domains
  — are named ONLY in the member's admission-act and scoping `description`
  prose, NOT as several surfaces and NOT as a structured breadth field.
- For the `directory` surface the governed unit is the TENANT DIRECTORY AND
  SERVICE ESTATE, so tenant-wide read IS the governed scope
  (`exceeds_governed_unit: false`, no `declared_excess`, no
  `spanned_surfaces`), not provider-forced excess: a complete tenant
  service-surface inventory is service discovery's very purpose.
- The READ/MUTATE slice the `device` change opened stays sliced: `directory` is
  the READ surface for directory and service-estate ENUMERATION. Entra-directory
  MUTATION (user, group and application administration) remains a SEPARATE
  FUTURE surface arriving with its own governing change, exactly as endpoint
  MUTATION does. Neither is admitted here.
- The realization (post-ratification, tasks §1–§5): add the `directory`
  `oneOf` const member to `$defs.admission_surface` in
  `contracts/schemas/xfactory-client-identity-roster.schema.yaml`, keep the
  validator's `EXTENSION_ROUTE["admission_surface"]` refusal string in sync
  (the validator DERIVES the vocab from the schema — no vocab-constant edit),
  add a packaged `directory` example entry on the governed-tenant-scope shape,
  and bump the contract bundle contract-v1.38 → contract-v1.39 (schema-row
  `sha256` recompute, CHANGELOG, regenerated release digests). Adding a
  `oneOf` const member is back-compatible for existing rosters, so no
  `contract_schema_version` bump.

## Impact

- **Modified Capabilities:** `client-identity-roster` — the "Identities are
  enumerated by admission surface, not by product name" requirement's closed
  vocabulary gains `directory` (spec delta below). That ONE requirement is the
  whole promotion: the delta restates it verbatim (heading + body + all three
  promoted scenarios, including the `device` scenario added at contract-v1.35)
  and adds exactly one scenario. No other promoted requirement changes; the
  discovery reader declares no forced breadth (its governed unit IS the tenant
  directory/service estate, so `exceeds_governed_unit: false` and no
  `declared_excess`), so the "Provider-forced breadth is declared" requirement
  applies unchanged and needs no edit.
- **Contract surface (ALL of it waits until ratification):**
  `contracts/schemas/xfactory-client-identity-roster.schema.yaml`
  (`$defs.admission_surface` gains one member),
  `scripts/validate-client-identity-roster.py` (refusal-string sync only),
  `examples/client-identity-roster/` (one added example), and the bundle
  (`contracts/manifest.yaml`, `contracts/CHANGELOG.md`,
  `contracts/releases/`).
- **Downstream unblock (CONSUMERS, not in scope):** OpsxFactory's FarHeap
  `directory` roster entry (`add-managed-service-inventory` task 7.2) and
  therefore the whole of that change's §7 live sweep — the reader grant mint,
  the authorized sweep, and the sealed snapshot — which its ratified F1
  ordering blocks behind this vocab extension (task 7.1). Those are downstream
  consumers of the extended vocabulary, authored in OpsxFactory under its own
  governance; this change governs only the neutral surface admission and
  authorizes no live provider act.
