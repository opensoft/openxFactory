---
code_surface: openxFactory
target_release: implementation_pending
---
# Proposal: add-client-identity-roster

Status: ratified
Ratified: 2026-08-14 by Brett Heap — in-session, verbatim "a, ratified",
answering clarify round 1 (`clarify-questions.md`): residency
class-independent, blocking scope all three as drafted, enrollment as
drafted, scope contract + both MODIFIED wirings, and first-release
`admission_surface` vocabulary limited to surfaces with a promoted
capability (`business_central`, `exchange`).
Amended: 2026-08-14 by Brett Heap — Decisions A and B, both "amend the
change", after the cross-model adversarial review of the Speckit clarify
rulings found two capabilities modified in substance but undeclared here
(`review/amendment-record-2026-08-14.md`): the conformance pack grows to four
checks, and the neutral credential-contracts schema gains an
`issuance_preconditions` vocabulary. Both are declared below.
Proposed 2026-08-14 and substantially revised the same day after a
cross-model decision review
(`review/decision-review-2026-08-14.md`) found the first draft's axis would
have invalidated ratified, deliberately-narrow identities and admitted no
conformant configuration for the one real client tenant in the estate.

## Why

xFactory governs credential shapes and grants (`credential-contracts`) and
the authority-chain root (`consent-instrument`). It does not govern the
**identity layer** those credentials belong to: which app registrations and
service principals stand inside a paying client's tenant, on what axis, with
what verified reach, justified by what. Three measured inputs make that gap
load-bearing now.

**1. Provider consent is not provider admission — measured, not assumed.**
The OpsxFactory Business Central investigation (2026-08-08..14) held four
admin-consented Business Central application permissions for six days and
still received `401` from the admin-center API. Access appeared only after a
**separate authorization act inside the Business Central admin center**
(evidence `xFactories/OpsxFactory/tenants/farheap-bc-sandbox1-verify-probe-evidence-v3`
through `-v7`; Microsoft documents consent and admin-center authorization as
jointly required). Every provider surface has such a second key, each one
different. An identity record that captures only the Entra grant records a
fiction — and the only reason anyone knows this is that a probe measured it,
which is why verification evidence is a requirement here, not a nicety.

**2. Some second keys silently convert structural bounds into logical ones.**
The BC admin-center authorization has no scope selector: it reaches every
environment in the tenant. Before it, "sandbox only" was enforced by the
credential itself — the identity had a per-environment application user in
Sandbox1 and **none in Production**. After it, that bound survives only in
gate logic. A degradation of this kind must be a declared, checkable,
tested fact.

**3. The identity axis is a product decision arriving now.** A client buying
OpsxFactory governance expects coverage across Business Central, collaboration
and mail surfaces, and the Dataverse/CRM family. One broad identity for all
of them fails on a mechanism, not on taste: **the identity is the unit of
grant for every provider-side scoping mechanism**, so one identity forces the
broadest permission variant everywhere it reaches, destroys the client's own
provider-side attribution, makes revocation all-or-nothing, and turns consent
into a dialog no administrator can meaningfully approve. The family already
paid for that lesson once — the 2026-07-10 incident behind OpsxFactory's
`add-github-installation-policy` was a too-broad content App holding org-wide
`contents:write` and bypassing branch protection.

But the opposite error is equally real, and the review caught the first draft
committing it: a roster axis that is *too* prescriptive invalidates
deliberately narrow identities the family has already ratified.
`microsoft_managed_node_inventory_reader` holds Entra, Intune and Windows 365
read scopes on ONE identity with `exact_effective_scopes: true`, precisely
because the provider offers nothing narrower. A rule forbidding
cross-workload identities would have declared that ratified class invalid.
So provider-forced breadth is declared here, never prohibited.

Two domain factories (OpsxFactory, and LedgerxFactory's
`ledgerx-farheap-bc-*`) already hold identities in the same client tenant, so
this cannot be a domain-local rule.

## What Changes

- **`client-identity-roster` (ADDED capability)** — the neutral contract:
  1. **Admission surfaces, not product names.** Identities are enumerated
     against provider-side administrative surfaces that own an independent
     admission act and scoping mechanism. This dissolves the overlap problem
     (collaboration channel files *are* content-workload sites) by keying on
     the act rather than the brand, and unifies the axis with the second-key
     concept below.
  2. **Uniqueness on (domain, surface, class, blast-radius unit, duty).**
     Classes are `observe` and `mutate`. Per-unit and duty-separated
     identities are *permitted* — the first draft's stricter key would have
     forbidden a per-environment identity (the one structural bound BC
     actually offers) and penalised LedgerxFactory's deliberate
     poster/provisioner separation.
  3. **Structural before logical.** Logical enforcement may be declared only
     after declaring that no principal scoped to the blast-radius unit exists
     at that surface, with the provider reason. Where one exists it must be
     used.
  4. **Provider-forced breadth is declared, not prohibited** — spanned
     surfaces or achieved class, with the provider reason and a gate
     obligation. Undeclared breadth is the finding.
  5. **No destructive identity class.** Destructive authority stays an action
     class at the gate whose ratified default is an externally authorized
     actor with no factory-held identity (`opsx_provider_identity:
     prohibited`, `max_grant_minutes: 0`). A destructive identity is
     admissible only where the provider demonstrably offers a delete-scoped
     permission distinct from write.
  6. **Admission is a verified LIST.** Each act declares surface, act,
     achieved scope, provider- or logic-enforced, and evidence of a
     successful call with its verification time. Consent alone is never
     access; an unverified act is a distinct state and excluded from
     effective reach; effective reach is the union (BC needs two acts with
     different scopes — the first draft's singular field could not represent
     its own worked example).
  7. **Achieved class derived from granted permissions**, with excess
     declared and bounded — reusing the mechanism OpsxFactory already
     ratified (`declared_credential_excess`, `no_narrower_role_reason`,
     `bound_mechanism`). An identity may not describe itself as narrower
     than it achieves.
  8. **Gate obligations must resolve and be tested** — to an existing gate in
     the owning domain's workflow records, naming a test proving refusal of
     an out-of-unit target. Otherwise the contract merely documents the
     degradation it exists to prevent.
  9. **Residency as a declared model**, distinguishing registration home
     tenant from principal locations. Vendor-tenant-multi is a governed model
     with obligations (tenant allow-list at token validation, per-client
     authorization state and revocation evidence, cross-client credential-span
     statement, and a consent amendment per affected client) rather than a
     rule plus an escape hatch every shipping product takes.
  10. **Entry lifecycle** (`planned|enrolled|retired`) plus a
      standing-credential attestation, so a roster is a projection over time
      and the measured hygiene failure class (an undeleted credential after a
      falsely attested revoke, `-v7`) has somewhere to become visible.
  11. **Both roots cited** — the domain-qualified ratified capability AND the
      consent instrument in force; our own ratification never by itself
      justifies standing in another party's tenant.
  12. **Report-only drift that withholds our own credential.** No automated
      remediation in a client tenant (it would need a broadly privileged
      identity there), but an open drift finding refuses grant issuance for
      that identity — the one lever we own, using the existing
      `issuance_preconditions` mechanism.
  13. **Cross-domain composition from published fragments**, with findings
      limited to genuinely shared identity material and undeclared reach.

- **`consent-instrument` (MODIFIED)** — governed identities standing in the
  consenting party's tenant join the first-class dependent-artifact
  references, so termination cascades reach the identity and its provider-side
  admission, not only its credential grants. Without this, withdrawal revokes
  a credential while the identity keeps standing, still admitted.

- **`doc-health` (MODIFIED)** — a sixteenth family covering only the
  CROSS-DOMAIN roster concerns; intra-repo entry conformance is a blocking
  domain gate, not an advisory nightly report.

- **`domain-conformance-checks` (MODIFIED, Decision A)** — the neutral pack's
  exhaustive enumeration of three scripts grows to four, admitting
  `scripts/validate-client-identity-roster.py`, because pack membership is the
  only promoted mechanism that confers blocking status on a canonical check.
  In a target repo publishing no roster fragment the check passes with an
  explicit notice: this release enforces no completeness rule, so absence is
  never a finding.

- **`credential-contracts` (MODIFIED, Decision B)** — the neutral schema gains
  an `issuance_preconditions` vocabulary whose roster-drift member gives the
  ratified refusal a neutral home. Without it the refusal exists only as a
  domain-local extra key riding a neutral schema that neither declares nor
  forbids it, and the ratified blocking clause has nothing neutral to stand
  on.

## Capabilities

### New Capabilities

- `client-identity-roster`: governed identity topology for client tenants.

### Modified Capabilities

- `consent-instrument`: dependent-reference cascade reaches governed
  identities.
- `doc-health`: sixteenth deterministic family, cross-domain scope only.
- `domain-conformance-checks`: the pack grows to four checks, admitting the
  canonical roster check as blocking (Decision A, 2026-08-14).
- `credential-contracts`: the neutral schema gains an `issuance_preconditions`
  vocabulary carrying the roster-drift member (Decision B, 2026-08-14).

## Impact

- Neutral records: `contracts/schemas/xfactory-client-identity-roster.schema.yaml`
  (prefix per the family convention), a packaged `examples/` instantiation,
  a canonical `scripts/validate-client-identity-roster.py`, a
  `contracts/manifest.yaml` row with sha256 and consumption rule, a
  `contracts/CHANGELOG.md` entry, and a contract-bundle bump — the full
  neutral-contract realization pattern, which the first draft omitted and
  without which domains cannot consume it through their pinned
  `xfactory.contract_ref`.
- Intra-repo conformance ships as a canonical check in the
  `domain-conformance-checks` pack (blocking); the cross-domain family lands
  in doc-health (reporting).
- Declared placement for domain roster instances, so an instance cannot land
  where `validate-credential-contracts.py` skips it as out of scope and no
  validator covers it.
- Domain follow-ups (named, not performed): OpsxFactory declares its entries
  including the three findings this investigation surfaced — the
  `opsx-farheap-bc-observer` name/purpose mismatch now that it achieves more
  than observation, the inert Microsoft Graph delegated scope absent from its
  identity record, and the tenant-wide admin-center excess with its gate
  obligation; LedgerxFactory declares its `ledgerx-farheap-bc-*` entries,
  exercising the composition and duty rules against a real two-domain tenant.
- No change to credential record shapes, grant neutrality, or the JIT
  discipline. No client-tenant act is authorized by this change.

## Out of scope, deliberately

- **Enrollment automation.** Creating identities inside a client tenant would
  itself require a broadly privileged identity there — the same chicken-and-egg
  that makes automated drift remediation unacceptable. Enrollment stays a
  consented human act per client, following the pattern already proven in
  tree (a bounded sysadmin prompt returning an evidence block with
  zero-credential post-conditions).
- The per-surface admission procedures themselves (provider documentation
  plus a domain runbook each).
- Any decision to grant, widen, or narrow a live client identity.
- Non-Entra provider identities (a client-org GitHub App installation is
  roster-shaped but is routed by `client-infrastructure-liaison` today); the
  surface vocabulary starts Entra-homed and its extension is named as a
  successor so two capabilities cannot both claim that ground.
