# Cross-model decision review: add-client-identity-roster

Status: record
Date: 2026-08-14
Protocol: standing cross-model review of architect rulings (reviewer model ≠
deciding model). Deciding seat: architect. Reviewer: Opus, over the pre-review
draft (commit 19d5b21), one pass, positions forced per decision.

## Verdicts on the first draft

`disagree` on D1 (axis) and D6 (cross-domain uniqueness) — both HIGH, both
fixes to the decision rather than the wording. `agree_insufficient` on D2,
D3, D4, D5, D8. `agree` on D7 (neutral home) with two consequential gaps.
Per the asymmetric-signal rule the two disagreements are the strong evidence;
both were verified against the tree before adoption.

## Verified before adoption (a finding is not authoritative because it is a finding)

| Claim | Verified against | Result |
|---|---|---|
| A ratified class deliberately spans workloads | OpsxFactory `credentials/requirements.yaml` | TRUE — `microsoft_managed_node_inventory_reader` holds Entra `Device.Read.All` + Intune `DeviceManagementManagedDevices.Read.All` + W365 `CloudPC.Read.All` on one identity with `exact_effective_scopes: true` |
| Destructive holds no factory identity | same | TRUE — `access_mode: external_authorized_actor`, `opsx_provider_identity: prohibited`, `minimum_scopes: []`, `max_grant_minutes: 0` |
| BC's structural bound is a per-environment principal | `tenants/farheap-bc-observer-identity-evidence-v1.yaml` | TRUE — `environment: Sandbox1`, `production_application_user: absent` |
| A second domain holds identities in the same client tenant | LedgerxFactory tenants/ + prompts | TRUE — `ledgerx-farheap-bc-poster`, `-provisioner` with capability evidence |
| A multi-tenant app's principal lands in the client estate | LedgerxFactory `docs/naming.md` | TRUE — verbatim: "the multi-tenant app whose service principal lands in each client estate at consent" |
| doc-health fixes the family count | openxFactory `openspec/specs/doc-health/spec.md` | TRUE — "SHALL implement fifteen check families" |

## Blocking findings, and what changed

1. **D1 axis (rewritten).** "One identity per (workload, class)" (a) forbade a
   per-blast-radius-unit identity — mandating the structural→logical
   degradation the change exists to expose; (b) invalidated the ratified
   multi-workload reader above; (c) admitted a `destructive` class that
   inverts the ratified no-identity position; (d) was unverifiable, since the
   record carried no granted permissions; (e) contradicted the GitHub
   precedent it cited (content vs administration Apps are one surface, one
   class, split by duty). → Axis re-keyed to (domain, admission surface,
   class, blast-radius unit, duty); classes reduced to observe|mutate;
   structural-before-logical added; provider-forced breadth declared rather
   than prohibited; `granted_permissions[]` added so the axis is falsifiable.
2. **D6 composition (rewritten).** The old rule admitted NO conformant
   configuration for the real FarHeap tenant: two domains' BC readers are the
   same (workload, class) pair → finding; sharing one identity → finding;
   LedgerxFactory's duty pair → finding. Day one would have produced three
   findings against ratified, correct designs. → Findings narrowed to shared
   identity material and undeclared reach; per-domain fragments plus
   aggregation-level assembly named.

## Non-blocking findings adopted

- Admission became a verified LIST (the singular field could not represent
  the BC worked example's two acts with different scopes); unverified acts
  are a distinct state; effective reach is the union.
- `authority_class_intended` vs `_achieved` derived from granted permissions,
  reusing the domain's ratified `declared_credential_excess` mechanism —
  closing the "purpose says read-only while permissions can delete an
  environment" fiction.
- Gate obligations must resolve to a real gate AND name a refusal test.
- Residency: distinguish identity kind / home tenant / principal locations;
  vendor-tenant-multi becomes a governed model with obligations including a
  consent amendment per affected client, rather than an escape hatch.
- Entry lifecycle + standing-credential attestation (the `-v7` hygiene
  incident class had nowhere to become visible).
- `consent_ref` required alongside `ratified_by`; MODIFIED
  `consent-instrument` so termination cascades reach identities and their
  provider-side admission.
- Blocking vs reporting split (domain-conformance-checks vs doc-health) and
  drift refusing grant issuance via `issuance_preconditions`.
- MODIFIED `doc-health` (sixteenth family) — the first draft's "Modified
  Capabilities: none" was wrong on two counts.
- Full neutral-contract realization pattern added (validator, packaged
  examples, manifest row + sha256, CHANGELOG, bundle bump, declared
  placement), `xfactory-` schema prefix, `design.md` added inside the packet,
  and this review record created at the path tasks.md cites.

## Not adopted

The reviewer's framing that the rival axis is per-blast-radius-unit *instead
of* per-surface was declined: the two are not exclusive, and making them
exclusive is what broke the first draft. Both are elements of the uniqueness
tuple, with structural-before-logical making per-unit mandatory where the
provider offers it. The reviewer's own analysis agrees a second app would not
have cured the tenant-wide admin-center reach.

## Judgment carried to the ratifier

Enrollment cost at N clients (design.md's open question). The permissive axis
is safer and more expensive; automation is refused on principle; the governed
lever if cost bites is the vendor-tenant-multi model with full obligations,
never a quiet relaxation of the axis.
