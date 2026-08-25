# Design: add-client-identity-roster

## Decision 1 — The axis is admission surface, not product name

Rejected: enumerating identities against provider product names (Business
Central, SharePoint, Teams, Exchange, CRM). Provider boundaries overlap in
ways that make "one identity per product" indeterminate — collaboration
channel files *are* content-workload sites, and a single directory-family
permission can reach groups, chat and their sites at once. An implementer
could re-slice product names until any identity became conformant, making the
rule unfalsifiable.

Adopted: an **admission surface** is whatever owns an independent admission
act and its own scoping mechanism. This is falsifiable (the act either exists
separately or it does not), and it makes the axis and the second-key concept
one taxonomy instead of two.

## Decision 2 — Uniqueness admits per-unit and per-duty identities

Rejected (first draft): exactly one identity per (workload, authority class),
with a second entry for the same pair being a finding. The cross-model review
demonstrated this fails against reality twice over:

- OpsxFactory's BC identity holds a per-environment application user in
  Sandbox1 with **no Production application user** — the strongest structural
  bound in the whole evidence chain. A ceiling of one identity per (workload,
  class) forbids a second, Production-scoped identity, forcing reuse across
  environments and mandating exactly the structural→logical degradation this
  change exists to expose.
- LedgerxFactory deliberately separates `-poster` from `-provisioner` inside
  one surface and class as a duty separation, and the GitHub plane's
  post-incident answer was two Apps (content vs administration) in one
  surface and class. The rule would have declared both correct designs
  invalid.

Adopted: uniqueness on (domain, admission surface, authority class,
blast-radius unit, duty), plus an explicit **structural-before-logical**
requirement so the freedom to add per-unit identities becomes an obligation
where the provider offers them.

## Decision 3 — Provider-forced breadth is declared, never prohibited

Rejected: "no identity spans surfaces." `microsoft_managed_node_inventory_reader`
is a ratified, deliberately narrow class holding Entra, Intune and Windows 365
read scopes on one identity with `exact_effective_scopes: true`, because the
provider offers nothing narrower. A prohibition would invalidate ratified
correct work and, worse, would push implementers to re-define surfaces until
the rule stopped biting.

Adopted: forced breadth is conformant when declared with the provider reason
and a gate obligation; undeclared breadth is the finding. This is the same
treatment scope excess already receives — one failure class (provider coarser
than governance), one mechanism.

## Decision 4 — No destructive identity class

Rejected: authority classes `observe|mutate|destructive`. The ratified
precedent says the opposite of what a destructive slot implies: destructive
requirement classes carry `access_mode: external_authorized_actor`,
`opsx_provider_identity: prohibited`, `minimum_scopes: []`,
`max_grant_minutes: 0` — the family holds **no** identity for destructive
acts. A schema slot invites one. And no provider surface examined offers a
mutate-but-not-destructive application permission (write includes delete), so
a destructive entry would either stay empty or duplicate the mutate entry's
permissions with a false appearance of separation.

Adopted: classes `observe|mutate`; destructive stays an action class at the
gate with the ratified external-actor default, admissible as an identity only
on a demonstrated delete-scoped permission distinct from write.

## Decision 5 — Residency is a declared model, not a rule with an escape

Rejected: "single-tenant client-resident, multi-tenant only by exception."
Two problems the review established. First, "resident" is ambiguous exactly
where it matters: a vendor-homed multi-tenant registration's service
principal *lands in the client tenant at consent* — LedgerxFactory's ratified
naming registry says so verbatim — so an implementer could declare
client-residency for a vendor-homed app and pass. Second, the multi-tenant
shape is the *decided product architecture* for at least two providers
(an ISV connect app; a GitHub App is structurally one registration with N
installations), so the default would be honoured by hand-built beta
identities and bypassed by everything that ships.

Adopted: declare identity kind, registration home tenant, and principal
locations; then declare a residency model with per-model obligations. The
multi-tenant model is governed rather than exceptional — allow-list enforced
at token validation, per-client authorization state and revocation evidence,
an explicit cross-client credential-span statement, and a consent amendment
per affected client (a transition, per `consent-instrument`), because a
shared identity means one client's compromise reaches another and that is a
change in the disclosed access shape.

## Decision 6 — Verification evidence is part of admission

Rejected: recording the admission act as an assertion. For six days the BC
Entra grants existed and the API returned 401; a roster written in that window
would have declared admission and been wrong. Assertions about provider access
are fiction until measured.

Adopted: each admission act carries evidence of a successful call and the time
it was verified; an unverified act is a distinct state excluded from effective
reach. The evidence records this pattern needs already exist in the shape
required, so the cost is bookkeeping, and it makes the contract's central
claim self-enforcing.

## Decision 7 — Blocking where it must be, reporting where it can only report

Rejected: putting all roster conformance in doc-health as report-only. That
is right for provider-side mutation (automated remediation in a client tenant
would need a broadly privileged identity there — the same chicken-and-egg as
enrollment) but wrong as a blanket: an advisory nightly warning for a `mutate`
identity with no ratified capability guts the traceability requirement.

Adopted: intra-repo entry conformance is a **blocking** canonical check in the
`domain-conformance-checks` pack; cross-domain composition is a **reporting**
doc-health family; and an open drift finding **refuses grant issuance** for
that identity through the existing `issuance_preconditions` mechanism —
withholding our own credential is the lever we own and is not a mutation of
the client's estate.

## Decision 8 — Neutral home, beneath the two existing capabilities

`credential-contracts` fixes credential record shapes; `consent-instrument`
fixes the authority root; neither covers which identities exist. Two domains
already hold identities in one client tenant, so a domain-local rule cannot
work. The tension with `add-github-installation-policy`'s decision to avoid a
sibling capability resolves the other way here: that change governed one
domain's plane, while this spans domains.

Consequence accepted: this change modifies `consent-instrument` (cascade
reaches identities) and `doc-health` (sixteenth family). The first draft
claimed no modified capabilities, which was wrong on both counts.

## Open question carried to the ratifier

Enrollment cost. Per-client, per-surface, per-class, per-unit, per-duty
identities are the safe topology and the expensive one, with automation
refused on principle. The entry lifecycle (`planned|enrolled|retired`) makes a
roster a projection over time rather than a day-one enrollment bill, but it
does not make the bill smaller. If cost proves prohibitive at N clients, the
governed lever is the vendor-tenant-multi residency model with its full
obligations — not a quiet relaxation of the axis.
