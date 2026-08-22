# Design: add-roster-directory-admission-surface

This change admits ONE new member — `directory` — into the closed
`admission_surface` vocabulary of `client-identity-roster`, through the
extension route the capability defines: "The closed surface vocabulary SHALL
be extended only by the change that governs a new surface." OpsxFactory
`add-managed-service-inventory` (service-surface DISCOVER) is that governing
surface, and the extension is proposed on its realization evidence. Five
rulings fix the shape of the member; each is recorded with its rationale and
the alternative it rejects.

This is the sibling of `add-roster-device-admission-surface`
(archived 2026-08-22, cut as contract-v1.35): same extension route, same
one-surface reasoning, same additive versioning class, same downstream-consumer
fence. Where this change departs from that precedent it says so and says why.

## Ruling 0 — The proposal's timing is fixed by the governing change's ratified F1 ordering

**Adopted.** This extension is proposed NOW, on the DETERMINISTIC contract
landed by `add-managed-service-inventory` §1–§6 (all ticked; merged 2026-08-22
as OpsxFactory `main` `824f8ef`), and NOT on a live snapshot.

**Rationale.** That change's adversarial review found its §7 live-sweep runbook
circularly ordered (grant ← roster entry ← `directory` vocab ← live snapshot ←
grant). The ratified F1 fix broke the cycle in exactly one direction: "the
MAP-stage openxFactory `directory` admission-surface vocab extension is now
stated as a PREREQUISITE of the whole §7 sweep, justified on the DETERMINISTIC
§1–6 contract (never a live snapshot) and fronted in the §7 ordering". Its task
7.1 restates the rule as a blocking prerequisite — "Nothing else in §7 may
proceed before the openxFactory vocab admits `directory`" — and its
conscious-acceptance note 1 adds that the extension "gates the live
realization — not the landing of this change". Brett's ratification of that
ordering is this proposal's authority to exist before any FarHeap read has
happened.

**Rejected: waiting for a live snapshot.** That is the circular ordering F1
removed. The discovery reader's grant cannot be minted without an
admission-verified `directory` roster entry, and that entry cannot exist until
the vocabulary admits `directory` — so a vocab extension that waited for live
evidence would wait forever. The deterministic contract (reader class, workflow,
adapter/enumeration contract, snapshot kind, fixtures) is sufficient evidence of
what the surface IS; the live sweep is evidence of what one tenant HAS, which
the vocabulary does not need.

## Ruling 1 — The surface token is `directory` (const)

**Adopted.** The new `oneOf` const member is `directory`. It mirrors the shape
of the three existing members `business_central`, `exchange` and `device`: a
lowercase, single-token const naming the surface by its admission act, not by a
product or marketing name.

**Rationale.** `directory` is the realized enum fact. The realized
`microsoft_service_discovery_reader` credential requirement carries
`admission_surface: directory` (OpsxFactory `credentials/requirements.yaml`,
`main` `824f8ef`), and the promoted `tenant-reader-grant-pipeline` spec, the
service-inventory design, and the service-inventory §7 runbook all name the
surface `directory` in prose. The vocabulary is a machine key: it must match
the fact the producers already emit, verbatim.

**Rejected: `entra_directory` / `service_discovery` / `microsoft_graph`.**
`entra_directory` and `microsoft_graph` are provider-product spellings, which
the requirement itself forbids ("A roster SHALL NOT enumerate identities
against product or marketing names") and which would also mis-scope the member
— Graph is the transport for `device` too, and Entra-directory MUTATION is a
separate future surface (Ruling 3 boundary). `service_discovery` is the
GOVERNANCE-PROSE spelling of the consuming capability, not of the surface;
adopting it would create a token no producer emits and force a rename of a
merged, ratified credential class to match a vocabulary that exists to describe
it.

## Ruling 2 — ONE surface, not one per discovered service

**Adopted.** `directory` is a SINGLE read surface: one admission act and one
scoping mechanism. The provider areas it reads — the organization profile,
subscribed service plans (`subscribedSkus` / `assignedPlans`), service
principals and applications, and verified domains — are named ONLY in the
member's admission-act/scoping `description` prose (Ruling 4), NOT as several
`admission_surface` members and NOT as any structured
`spanned_surfaces`/`declared_excess` breadth field on the consuming entry.

**Rationale.** An admission surface is defined extensionally as a provider-side
surface owning ONE independent admission act and ONE scoping mechanism (the
promoted requirement). Directory/service enumeration has exactly one admission
act — admin consent for the read-only directory application roles on one Entra
app registration — and exactly one scoping mechanism, tenant-wide read with no
narrower selector. So it is one surface by the ratified definition, however
many object families the enumeration touches. And that tenant-wide read is NOT
excess to be declared away: for the `directory` surface the GOVERNED UNIT is
the whole tenant directory and service estate — a complete tenant
service-surface inventory is DISCOVER's very purpose — so tenant-wide read IS
the governed scope, carried with `exceeds_governed_unit: false`, NO
`declared_excess` block, and empty/omitted `spanned_surfaces`. This is the same
shape the `device` change's adversarial finding F1 established and its
ratification pinned.

**Rejected: one surface per discovered service (`exchange_service_plan`,
`sharepoint_service_plan`, `teams_service_plan`, …).** These are not surfaces.
They share one admission act, so by the extensional definition they are one
surface — exactly as `business_central`'s two acts are one surface and
`device`'s three provider areas are one surface. Worse, the services DISCOVER
detects are the very things whose own admission surfaces get enumerated LATER
by the MAP and ENROLL successors; minting a vocabulary member per detected
service would confuse the surface the READER is admitted on with the surfaces
the SNAPSHOT reports, and would put members in the closed vocabulary that no
governing capability has promoted. It is also schema-impossible in the
structured direction: `spanned_surfaces[]` items `$ref` the
`admission_surface` vocabulary, so a non-member service name could never
appear there.

**Rejected: widening `device` to cover directory reads.** The governing change
already rejected this on the OpsxFactory side, in its Decision 2: widening
`microsoft_managed_node_inventory_reader` to also enumerate directory services
"would collapse two admission surfaces onto one credential — breaking the
per-surface exact-effective-scopes contract, the 1:1 the roster keys on, and
per-surface revocation." The neutral side must not re-open on the vocabulary
what the domain side closed on the credential: `device` admits device-estate
READ under three device roles; `directory` admits directory/service-estate READ
under directory roles; the two are separately consented, separately scoped and
separately revocable, which is what makes them two surfaces.

## Ruling 3 — The read/mutate slice stays sliced

**Adopted.** `directory` is the READ surface for directory and service-estate
ENUMERATION. Entra-directory MUTATION — user, group and application
administration — remains a SEPARATE FUTURE surface, arriving with its own
governing change, exactly as endpoint MUTATION (Intune write/remediation) does.
This change admits no mutation surface.

**Rationale.** This is the `device` change's own F2 ruling applied to its named
successor. That ruling, accepted by Brett at ratification, held that admitting
`device` reslices the extension-route prose along a read/mutate axis: `device`
is the READ surface for Entra/Intune/Windows 365, "while endpoint-MUTATION
(Intune write/remediation) and Entra-DIRECTORY remain SEPARATE future surfaces,
each with its own governing change." This change is that Entra-directory
arrival — and it arrives on the READ half only, so the axis F2 established is
preserved rather than crossed. The evidence that the read half is genuinely
severable is in the realized reader class itself:
`reject_write_or_destructive_scopes: true` with `exact_effective_scopes: true`
over three `*.Read.All` roles. Note that OpsxFactory's long-standing
`entra_directory_admin` credential class (delegated OAuth,
`directory.readwrite.all`, human approval required) is the LATENT MUTATION
identity on the other half of this axis: it exists in
`credentials/requirements.yaml` today and is deliberately NOT admitted by this
change, because no promoted capability governs an Entra-directory mutation
surface yet.

**Rejected: admitting one `directory` surface covering read AND mutation.** A
single member would let a future mutation identity inherit an admission-surface
member ratified on read-only evidence, and would put a `mutate`
`authority_class` on a surface whose entire ratified description says the
provider's granted roles confer no write. The roster exists to expose exactly
that kind of silent widening.

**Boundary, restated for the schema text.** The realization (task 1.3) must
leave the extension route naming what is still to arrive: endpoint MUTATION
(Intune write) AND Entra-directory MUTATION. It removes only the
Entra-directory READ expectation that this change discharges.

## Ruling 4 — Admission act and scoping prose (authored from the service-inventory evidence)

**Adopted.** The `directory` member declares, in the same shape as the three
existing members:

- **Admission act:** ADMIN CONSENT for the read-only directory and
  service-enumeration application roles on ONE Entra app registration. The
  realized reader class carries `Organization.Read.All`,
  `Application.Read.All` and `Domain.Read.All` (OpsxFactory
  `credentials/requirements.yaml`, `main` `824f8ef`) — the organization
  profile and its subscribed service plans, the tenant's service
  principals/applications, and its verified domains. The exact EFFECTIVE set is
  pinned at grant time and recorded on the roster entry's
  `granted_permissions[]`, which is where per-entry provider fidelity belongs.
- **Scoping mechanism:** TENANT-WIDE READ. `exact_effective_scopes: true` and
  no narrower provider selector: the granted roles carry no directory-subset
  selector, so the exact effective scopes ARE the bound and the provider offers
  nothing narrower — unlike Exchange's per-group `RestrictAccess`, and exactly
  like `device`. There being no provider scoping mechanism, the admission act
  runs `enforcement_mode: logic_enforced`: the read is bounded by the exact
  read-only roles, not by a provider selector. `per_unit_principal_available`
  is FALSE for this surface — there is no per-directory-subset principal to
  use, because the governed unit is the whole estate. The governed unit is the
  tenant directory and service estate (a `blast_radius_unit` free token such as
  `tenant_directory_estate`, bound in the fragment's `legend`), so the
  tenant-wide read is the governed scope — not silently absorbed excess.
- **Authority class:** READ-ONLY. The requirement carries
  `reject_write_or_destructive_scopes: true`; the surface admits `observe`
  only. No mutation or destructive capability rides this member (directory
  mutation is a separate future surface — Ruling 3).
- **Identity kind:** an app-only WORKLOAD identity
  (`access_mode: workload_identity` on the reader class; an
  `entra_app_registration` in roster terms), presented by reference through
  the promoted `tenant-reader-grant-pipeline` — never a delegated user
  session.

**Rationale.** The promoted requirement demands that "each surface entry SHALL
name the admission act and scoping mechanism that make it a surface." All three
existing members do exactly this in their `description`s. The `directory`
member's prose is transcribed from merged, ratified evidence, not invented, so
the member description is a truthful account of the surface it admits.

**Rejected: describing the surface with a narrower or aspirational scope.** A
member description implying an administrative-unit, directory-scope or
per-service selector would be false to the provider and would let a consuming
entry claim a provider-enforced bound that does not exist — the exact
structural→logical degradation the roster capability was built to expose. The
member must record what the provider actually offers: tenant-wide read.

**Deliberate departure from the `device` member's prose.** The `device` member
enumerates its three roles as THE admission act because the node-inventory
reader's effective set is exactly those three. Here the member names the role
FAMILY (read-only directory and service-enumeration application roles) and
cites the three the realized class holds, because the governing change fixes
the exact EFFECTIVE set at grant time (its Decision 2: "pinned when the class is
realized", with Business Central presence detected through the service-plan
signal rather than a fourth role). The spec-delta scenario still names the three
concretely, so the promoted requirement is as concrete as `device`'s; the
schema member's prose is the place that records the family, because it must stay
true across a grant-time pin. FLAGGED for the architect: the alternative is to
hard-enumerate exactly three roles in the member description too, at the cost
of a schema edit if the pinned effective set differs.

## Ruling 5 — Additive; no `contract_schema_version` bump, bundle bumps to contract-v1.39

**Adopted.** Adding a `oneOf` const member to `$defs.admission_surface` is
BACK-COMPATIBLE for every existing roster: a fragment naming
`business_central`, `exchange` or `device` still validates unchanged, and no
existing record is reinterpreted. So the schema file's
`contract_schema_version` stays `1`. The change to the schema file's BYTES does
change its digest, so the realization bumps the contract BUNDLE contract-v1.38
→ contract-v1.39 with a schema-row `sha256` recompute and regenerated release
digests.

**Confirmation against the schema's own bump-condition comment.** The schema's
CLOSED-ON-PURPOSE header says "Growth takes a `contract_schema_version` bump."
Read in context, that sentence governs GROWTH OF THE CLOSED OBJECT SHAPES —
adding properties to objects that set `additionalProperties: false`, or
widening the key space of the two map-shaped properties closed with
`propertyNames`. Admitting a new VALUE into a closed `oneOf` const vocabulary
is a different, explicitly-named mechanism: the vocabulary's own EXTENSION
ROUTE text describes how a member is added and does NOT couple that to a
`contract_schema_version` bump. Adding an enum member changes the shape of no
object and reinterprets no existing field; it admits a value that was
previously refused. This matches the versioning policy's additive class, whose
test is that a domain repo on the same major version stays conformant without
changes — which every existing roster does. This is the same reading the
`device` admission was ratified on (its Ruling 4) and cut on
(contract-v1.35, CHANGELOG heading "additive").

**The current bundle is contract-v1.38** (`contracts/manifest.yaml`;
`contracts/CHANGELOG.md` heading "contract-v1.38 — 2026-08-21 (additive; the
doxBench model-catalog routing rule)"), so the next version is contract-v1.39.
The realization must re-read the manifest at the time it runs rather than trust
this line: three bundles were cut in the four days around the `device`
admission, and a bundle cut by another change between ratification and
realization moves the target.

**Rejected: bumping `contract_schema_version` to 2.** A schema-version bump
signals to consumers that the record shape changed in a way that may require
their attention. Nothing about an existing roster's shape or interpretation
changes here, so a bump would be a false signal and would drag the two kinds'
`schema_version` const and the manifest row's mirrored value into an
unnecessary migration. The additive path is correct.

## Downstream boundary (not a decision — a scope note)

The OpsxFactory side — the FarHeap `directory` roster entry
(`add-managed-service-inventory` task 7.2) and everything §7 gates behind it:
the consent ceremony, the grant mint, the authorized live sweep, the sealed
snapshot and its human acceptance, the revocation proof — is a DOWNSTREAM
CONSUMER of the extended vocabulary, authored in the OpsxFactory repo under its
own governance. None of it lands with this change, and this change authorizes no
live provider act. This change governs only the neutral surface admission.
