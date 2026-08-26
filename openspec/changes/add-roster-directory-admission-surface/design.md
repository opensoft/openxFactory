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
successor. Brett's ratification record states the ruling as: "admitting `device`
reslices the schema's extension-route prose so `device` is the READ surface for
Entra/Intune/Windows 365, while endpoint-MUTATION and Entra-DIRECTORY remain
SEPARATE FUTURE surfaces with their own governing changes" (archived
`add-roster-device-admission-surface`, `review/ratification-2026-08-19.md`,
conscious-acceptance note 2 — "Accepted"). That change's own design states the
same F2 flag and specifies the mutation half further, as endpoint mutation
covering Intune write and remediation. This change is that Entra-directory
arrival — and it arrives on the READ half only, so the axis F2 established is
preserved rather than crossed. The evidence that the read half is genuinely
severable is in the realized reader class itself:
`reject_write_or_destructive_scopes: true` with `exact_effective_scopes: true`
over three `*.Read.All` roles. Note that OpsxFactory's long-standing
`entra_directory_admin` credential class (delegated OAuth,
`directory.readwrite.all`, human approval required) is the LATENT MUTATION
identity on the other half of this axis: it stands in
`credentials/requirements.yaml` at OpsxFactory `main` `824f8ef` — the same
commit this change's evidence is drawn from, so the citation is pinned rather
than dated — and is deliberately NOT admitted by this change, because no
ratified capability governs an Entra-directory mutation surface yet.

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

- **Admission act:** ADMIN CONSENT for the read-only application roles
  `Organization.Read.All`, `Application.Read.All` and `Domain.Read.All` on ONE
  Entra app registration — the organization profile and its subscribed service
  plans, the tenant's service principals/applications, and its verified
  domains. Those three roles ARE the admission act, hard-enumerated: the exact
  EFFECTIVE set is pinned at CLASS REALIZATION, and that realization is already
  merged — `microsoft_service_discovery_reader` carries exactly those three as
  its `minimum_scopes` under `exact_effective_scopes: true` (OpsxFactory
  `credentials/requirements.yaml`, `main` `824f8ef`). Per-entry provider
  fidelity is still recorded on the roster entry's `granted_permissions[]`; the
  member description states the act.
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

**The three roles are hard-enumerated, exactly as `device`'s are — no role
family.** The `device` member enumerates its three roles as THE admission act
because the node-inventory reader's effective set is exactly those three. The
`directory` member does the same, for the same reason: the service-discovery
reader's effective set is exactly `Organization.Read.All`,
`Application.Read.All` and `Domain.Read.All`. There is no open pin to keep the
prose loose for. The governing change's Decision 2 says the exact effective
scope set is "pinned when the class is realized" — pinned at CLASS REALIZATION,
NOT at grant time — and that realization is MERGED: `minimum_scopes` is those
three roles under `exact_effective_scopes: true` (OpsxFactory `main`
`824f8ef`). Business Central presence is detected from the service-plan signal
this same `directory` read already returns, so it adds no fourth role. Member
prose, spec-delta scenario and realized class therefore all say the same three
things, which is the only arrangement in which the schema's description is a
truthful account of the act.

**And the enumeration carries a boundary the schema can state nowhere else.**
The member description must also EXCLUDE the broader directory-wide read roles:
`Directory.Read.All` is not within this surface's admission act, because it
reads the already-admitted `device` surface too (Entra registered devices are
directory objects). Admitting it under `directory` would collapse two
separately-consented, separately-scoped and separately-revocable surfaces onto
one act — which is what Ruling 2 rejects on the vocabulary and what the
governing change's Decision 2 rejected on the credential. A role FAMILY phrased
as "read-only directory and service-enumeration application roles" would
silently INCLUDE `Directory.Read.All` on its face, which is the concrete cost of
the family wording. The neutral layer cannot enforce this exclusion mechanically
— the schema header rules that it NEVER infers a provider fact from a token, so
no validator can know that one Graph role subsumes another surface's estate. The
member `description` is the only place the boundary can be stated at all, which
is precisely why it must be stated there.

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
CLOSED-ON-PURPOSE header says "Growth takes a `contract_schema_version` bump",
having just named the two MAP-shaped properties (`legend.*` and
`per_unit_principal_available`) that close their KEY SPACE with `propertyNames`.
So the coupling must be NAMED, not denied: `per_unit_principal_available`
closes its key space with `propertyNames: {$ref: "#/$defs/admission_surface"}`,
which means admitting `directory` to the vocabulary DOES widen that closed key
space — a `directory` key becomes legal where it was refused. Any argument that
this change touches no `propertyNames`-closed key space is simply false, and an
argument resting on it would collapse on inspection.

The correct reading of the bump condition is about WHAT IT PROTECTS. A
`contract_schema_version` bump signals to a consumer that an EXISTING RECORD
now means something different, or that a consumer must do something new to stay
conformant. The growth that triggers it is growth of that kind: a new property
on an `additionalProperties: false` object that records must now carry or
account for, or a key-space change that re-reads existing keys. What lands here
is a `oneOf` const admission, plus the key-space widening it IMPLIES in
`per_unit_principal_available` by way of that `$ref` — and that implied widening
is purely PERMISSIVE and purely DERIVED. It requires nothing new of any
existing record: every fragment naming `business_central`, `exchange` or
`device` validates byte-identically, no key it already carries is reinterpreted,
and no key becomes required. A record can only encounter the widening by
CHOOSING to write a `directory` key it had no reason to write before. The
versioning policy's additive test — a domain repo on the same major version
stays conformant without changes — is met by every existing roster in the
corpus.

Note also that "the two map-shaped properties" is imprecise as a statement of
what this change reaches: `legend.*`'s sub-maps (`blast_radius_units`,
`duties`) close on `free_token`, not on `admission_surface`, so they are
entirely unaffected. Exactly ONE of the two is coupled to the vocabulary.

This is the same reading the `device` admission was ratified on (its Ruling 4)
and cut on (contract-v1.35, CHANGELOG heading "additive"), and the repair above
is a repair to an argument INHERITED VERBATIM from that ratified design — this
is its second landing, and the defeating clause went unremarked the first time.
The outcome does not change: no `contract_schema_version` bump. The reasoning
now survives the objection instead of walking into it.

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

**And landing it does not by itself unblock task 7.2.** OpsxFactory pins
contract-v1.35 (`stack.yaml` `contract_ref`
`78f8e016fbddcf1125c11b7f11234fb2478b0415`) and keeps its own local copy of the
vocabulary: `ROSTER_ADMITTED_SURFACE_VOCAB = frozenset({"business_central",
"exchange", "device"})` at `scripts/validate-domain-factory.py:1501`, enforced
at :1670 by a refusal that names `directory` as riding its governing change.
While that pin and that fence stand, a `directory` roster entry is refused by
OpsxFactory's OWN validator regardless of what this vocabulary admits. The first
downstream act is therefore an OpsxFactory CONTRACT RE-PIN to the bundle this
realization cuts, together with the matching local-fence update — and only then
7.2. The precedent is exact: `device` did not become usable in OpsxFactory when
contract-v1.35 admitted it either; the re-pin and fence widening landed
separately, as OpsxFactory PR #45 (`77f4b82`). Stating this here so the
cross-repo ordering is not overclaimed on the neutral side: this change removes
the UPSTREAM blocker, which is a necessary and not a sufficient condition for
the live sweep.
