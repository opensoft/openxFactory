---
code_surface: openxFactory (schema/contract)
target_release: implementation_pending
---
# Proposal: add-roster-device-admission-surface

Status: staged
Staged: 2026-08-19 — awaiting Brett's ratification before the schema/bundle
realization runs. This change AUTHORS the vocabulary extension and its
realization plan; it does NOT edit the schema, the manifest bundle, or any
example (that is post-ratification realization work, tasks §1–§5). No code, no
bundle bump, and no merge land with this proposal.
Proposed: 2026-08-19 on the node-inventory realization evidence, per the
ratified reader-grant clarify decision Q4 (OpsxFactory
`add-tenant-reader-grant-pipeline`), which named the openxFactory
`client-identity-roster` `admission_surface` vocabulary extension for the
device surface as a cross-repo dependency, to be proposed on evidence and
bundled with the surface's governing change (node-inventory).

## Why

The promoted `client-identity-roster` capability enumerates governed
identities against a CLOSED `admission_surface` vocabulary whose first release
carries exactly two members — `business_central` and `exchange` — the two
client-tenant Entra-homed surfaces whose capabilities were promoted at
ratification. The schema's own extension-route text states the rule
verbatim: "The closed surface vocabulary SHALL be extended only by the change
that governs a new surface", and it names the surfaces still to arrive:
"endpoint/Intune, Windows 365 and Entra-directory arrive with theirs."

OpsxFactory now needs to enroll its node-inventory reader. The ratified
`microsoft_managed_node_inventory_reader` credential requirement
(`credentials/requirements.yaml`) holds `Device.Read.All`,
`DeviceManagementManagedDevices.Read.All` and `CloudPC.Read.All` with
`exact_effective_scopes: true` and `reject_write_or_destructive_scopes: true`
— a ratified, deliberately narrow read identity spanning Entra registered
devices, Intune managed devices and Windows 365 Cloud PCs, because the
provider offers no permission narrower than tenant-wide read for that concern.
This identity is the roster design's own MOTIVATING EXAMPLE for
provider-forced breadth (Decision 3 of `add-client-identity-roster`). To
enroll it, its roster entry must name an `admission_surface` — and no member
of the closed vocabulary admits it. The surface it belongs to, `device`, is
not yet in the vocabulary.

This change admits `device` — the node-inventory read surface — into the
closed `admission_surface` vocabulary through the exact extension route the
capability defines: the change that governs the new surface (node-inventory)
adds the member, on the realization evidence. That unblocks OpsxFactory's
node-inventory reader enrollment downstream.

## What Changes

- Admit the single admission surface `device` (const token) into the closed
  `admission_surface` vocabulary of `client-identity-roster`. `device` is ONE
  read surface — one admission act (admin consent for the application read
  roles on one identity) and one scoping mechanism (tenant-wide read, no
  narrower provider selector). The three provider areas it spans — Entra
  registered devices, Intune managed devices, Windows 365 Cloud PCs — are the
  member's admission-act and scoping prose, declared as provider-forced
  breadth on the entry (roster Decision 3), NOT three surfaces.
- Endpoint-mutation and Entra-directory remain SEPARATE future surfaces, each
  arriving with its own governing change per the schema's extension-route
  text. They are out of scope here.
- The realization (post-ratification, tasks §1–§5): add the `device` `oneOf`
  const member to `$defs.admission_surface` in
  `contracts/schemas/xfactory-client-identity-roster.schema.yaml`, keep the
  validator's `EXTENSION_ROUTE["admission_surface"]` refusal string in sync
  (the validator DERIVES the vocab from the schema — no vocab-constant edit),
  add a packaged `device` example entry, and bump the contract bundle
  contract-v1.34 → contract-v1.35 (schema-row `sha256` recompute, CHANGELOG,
  regenerated release digests). Adding a `oneOf` const member is
  back-compatible for existing rosters, so no `contract_schema_version` bump.

## Impact

- **Modified Capabilities:** `client-identity-roster` — the
  "Identities are enumerated by admission surface, not by product name"
  requirement's closed vocabulary gains `device` (spec delta below). No other
  promoted requirement changes; the "Provider-forced breadth is declared"
  requirement already governs the device reader's spanned-surface shape and
  needs no edit.
- **Contract surface:** `contracts/schemas/xfactory-client-identity-roster.schema.yaml`
  (`$defs.admission_surface` gains one member),
  `scripts/validate-client-identity-roster.py` (refusal-string sync only),
  `examples/client-identity-roster/` (one added example), and the bundle
  (`contracts/manifest.yaml`, `contracts/CHANGELOG.md`,
  `contracts/releases/`). ALL of this waits until ratification.
- **Downstream unblock (a CONSUMER, not in scope):** OpsxFactory's device
  roster entry and node-inventory §6, which unblock
  `add-managed-node-inventory` task 5.x. Those are downstream consumers of the
  extended vocabulary; this change governs only the neutral surface admission.
