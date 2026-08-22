# Design: add-roster-device-admission-surface

This change admits ONE new member — `device` — into the closed
`admission_surface` vocabulary of `client-identity-roster`, through the
extension route the capability defines: "The closed surface vocabulary SHALL
be extended only by the change that governs a new surface." Node-inventory is
that governing surface, and the extension is proposed on its realization
evidence. Four rulings fix the shape of the member; each is recorded with its
rationale and the alternative it rejects.

## Ruling 1 — The surface token is `device` (const)

**Adopted.** The new `oneOf` const member is `device`. It mirrors the shape of
the two existing members `business_central` and `exchange`: a lowercase,
single-token const naming the surface by its admission act, not by a product
or marketing name.

**Rationale.** `device` is the realized enum fact. The ratified
`microsoft_managed_node_inventory_reader` credential requirement and the
downstream OpsxFactory roster entry name this surface `device`
(`admission_surface: device`). The roster's entry-naming convention keys on
the admission act, and the token that the realized artifacts already carry is
`device`. The vocabulary is a machine key: it must match the fact the
producers emit, verbatim.

**Rejected: `node-inventory` / `managed-node-inventory`.** These are the
GOVERNANCE-PROSE spellings of the concern (the capability is
`add-managed-node-inventory`; the workflow is `managed-node-inventory`). But
the roster vocabulary is not prose — it is a closed set of machine keys that a
domain fragment sets literally and the canonical validator compares for
equality. The realized enum fact is `device`. Adopting a prose spelling would
create a token no producer emits, forcing a rename of ratified artifacts to
match a vocabulary that exists to describe them.

## Ruling 2 — ONE surface, not three

**Adopted.** `device` is a SINGLE read surface: one admission act and one
scoping mechanism. The three provider areas it reaches — Entra registered
devices, Intune managed devices, Windows 365 Cloud PCs — are named ONLY in the
member's admission-act/scoping `description` prose (Ruling 3), NOT as three
separate `admission_surface` members and NOT as any structured
`spanned_surfaces`/`declared_excess` breadth field on the consuming entry.

**Rationale.** An admission surface is defined extensionally as a provider-side
surface owning ONE independent admission act and ONE scoping mechanism (the
promoted requirement). Node-inventory read has exactly one admission act (admin
consent for the three read roles on one identity) and one scoping mechanism
(tenant-wide read, no narrower selector) — so it is one surface by the ratified
definition, not three. Roster Decision 3's own worked example is this identity:
"`microsoft_managed_node_inventory_reader` is a ratified, deliberately narrow
class holding Entra, Intune and Windows 365 read scopes on one identity with
`exact_effective_scopes: true`, because the provider offers nothing narrower."
That tenant-wide read is NOT excess to be declared away: for the `device`
surface the GOVERNED UNIT is the whole tenant device estate — a complete tenant
device inventory is node-inventory's very purpose — so tenant-wide read IS the
governed scope, carried with `exceeds_governed_unit: false` and NO
`declared_excess` block (see the Adversarial fix (F1) note below).

**Rejected: three surfaces (`entra_devices`, `intune_managed_devices`,
`windows_365_cloud_pcs`).** Modelling the provider areas as three surfaces
would contradict the extensional surface definition (they share one admission
act, so they are one surface, exactly like `business_central`'s two acts are
one surface), and it would re-introduce from the other direction the failure
Decision 3 rejects: it would re-slice a deliberately narrow, ratified identity
into a false appearance of three separately admissible surfaces. Modelling
them as ONE surface whose governed unit is the tenant device estate records the
shape truthfully — the tenant-wide read is the governed scope, not excess to be
carried in a breadth field.

**Boundary.** Endpoint-MUTATION (Intune write/remediation) and
Entra-DIRECTORY are SEPARATE future surfaces, listed in the schema's own
extension-route text as arriving with their own governing changes
("endpoint/Intune, Windows 365 and Entra-directory arrive with theirs"). This
change admits only the read surface `device`. It does not admit any mutation
surface and does not pre-empt the directory surface.

**Adversarial fix (F1).** An earlier draft of this ruling described the three
provider areas as the entry's declared `spanned_surfaces` / "provider-forced
breadth." That framing was a vestige of surface-SPANNING and is
schema-impossible: `spanned_surfaces[]` items `$ref` the `admission_surface`
vocabulary (they must be surface consts), and the three provider areas are not
vocabulary members, so the schema would refuse them; and per this ruling
`device` is ONE surface, which spans no OTHER surface. Corrected to the
governed-tenant-scope framing: for the `device` surface the governed unit IS
the tenant device estate, so a conformant `device` entry carries
`exceeds_governed_unit: false`, NO `declared_excess` block, and empty/omitted
`spanned_surfaces`. The tenant-wide device read is the governed scope, not
excess to be declared.

**Read/mutate re-slice (F2 — for Brett's conscious acceptance at ratification).**
Admitting `device` re-slices the schema's extension-route prose along a
read/mutate axis: `device` is the READ surface for Entra, Intune and Windows
365, while endpoint-MUTATION (Intune write/remediation) and Entra-DIRECTORY
remain SEPARATE future surfaces, each with its own governing change. This
read/mutate cut is flagged for conscious acceptance at ratification; it does
not change the spec delta.

## Ruling 3 — Admission act and scoping prose (authored from node-inventory evidence)

**Adopted.** The `device` member declares, in the same shape as the two
existing members:

- **Admission act:** admin consent for the application read roles
  `Device.Read.All`, `DeviceManagementManagedDevices.Read.All` and
  `CloudPC.Read.All` on ONE identity. These are the three read roles the
  ratified `microsoft_managed_node_inventory_reader` requirement holds
  (`credentials/requirements.yaml`), together admitting the union of Entra
  registered devices, Intune managed devices and Windows 365 Cloud PCs.
- **Scoping mechanism:** TENANT-WIDE READ. `exact_effective_scopes: true` and
  no narrower provider selector — "the provider offers nothing narrower" (the
  roster's own motivating example, Decision 3). There is no provider scoping
  mechanism (unlike Exchange's `RestrictAccess`), so the admission act(s) run
  `enforcement_mode: logic_enforced`: the read is bounded by the exact
  read-only roles, not by a provider selector. The governed unit is the
  tenant-wide device estate (a `blast_radius_unit` token such as
  `tenant_device_estate`), so the tenant-wide read is the governed scope — not
  silently absorbed excess.
- **Authority class:** READ-ONLY. The requirement carries
  `reject_write_or_destructive_scopes: true`; the surface admits `observe`
  only. No mutation or destructive capability rides this member (endpoint
  mutation is a separate future surface — Ruling 2 boundary).

**Rationale.** The promoted requirement demands that "each surface entry SHALL
name the admission act and scoping mechanism that make it a surface." The two
existing members do exactly this in their `description`s (BC names its two
acts and their environment/tenant scoping; Exchange names the application
access policy and its mail-enabled security group). The `device` member's
prose is transcribed from ratified evidence, not invented, so the member
description is a truthful account of the surface it admits.

**Rejected: describing the surface with a narrower or aspirational scope.** A
member description that implied a per-device or per-environment selector would
be false to the provider and would let a consuming entry claim a
provider-enforced bound that does not exist — the exact
structural→logical degradation the roster capability was built to expose. The
member must record what the provider actually offers: tenant-wide read.

## Ruling 4 — Additive; no `contract_schema_version` bump, bundle bumps to contract-v1.35

**Adopted.** Adding a `oneOf` const member to `$defs.admission_surface` is
BACK-COMPATIBLE for every existing roster: a fragment that names
`business_central` or `exchange` still validates unchanged, and no existing
record is reinterpreted. So the schema file's `contract_schema_version` stays
`1`. The change to the schema file's BYTES does change its digest, so the
realization bumps the contract BUNDLE contract-v1.34 → contract-v1.35 with a
schema-row `sha256` recompute and regenerated release digests.

**Confirmation against the schema's own bump-condition comment.** The schema's
CLOSED-ON-PURPOSE header says "Growth takes a `contract_schema_version` bump."
Read in context, that sentence governs GROWTH OF THE CLOSED OBJECT SHAPES —
adding properties to objects that set `additionalProperties: false`, or
widening the key space of the two map-shaped properties closed with
`propertyNames`. Admitting a new VALUE into a closed `oneOf` const vocabulary
is a different, explicitly-named mechanism: the vocabulary's own EXTENSION
ROUTE text ("a surface enters with the promotion of the capability that
governs it") describes how a member is added and does NOT couple that to a
`contract_schema_version` bump. Adding an enum member does not change the
shape of any object or reinterpret any existing field; it admits a value that
was previously refused. This matches the versioning policy's additive class —
"new optional fields, new contracts, new validator warnings", whose test is
that a domain repo on the same major version stays conformant without changes
— which every existing roster does. Therefore: no `contract_schema_version`
bump; a bundle bump for the digest refresh only.

**Rejected: bumping `contract_schema_version` to 2.** A schema-version bump
signals to consumers that the record shape changed in a way that may require
their attention. Nothing about an existing roster's shape or interpretation
changes here, so a bump would be a false signal and would drag the two
kinds' `schema_version` const and the manifest row's mirrored value into an
unnecessary migration (the schema documents that both kinds declare
`schema_version: 1` and the row mirrors it). The additive path is correct.

## Downstream boundary (not a decision — a scope note)

The OpsxFactory side — the `device` roster entry and node-inventory §6 — is a
DOWNSTREAM CONSUMER of the extended vocabulary, authored in the OpsxFactory
repo under its own governance. It is not part of this change and does not land
with it. This change governs only the neutral surface admission.
