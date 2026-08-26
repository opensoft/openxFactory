# Subject Recall & Consent Path: per-query consent for a person-subject — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Details the hardest governance path in the knowledge base — recalling a
subject's private memory when the subject is a *person* (a Medx patient), where
consent is checked **per query**, not just at ingest. The subject owns its
consent model (who / what / why / how-long / where), the default is deny, and a
`recall` must declare a **purpose**; the path matches consent grants, filters to
the **minimum necessary** for that purpose, returns consented context-packets
plus an explained denial list, and audits every recall (granted or denied) to a
subject-visible log. Revocation and erasure take effect immediately at query
time. A break-glass emergency exception exists for life-critical domains — but
audited and dual-authorized, never a silent bypass. The machinery is neutral
(gateway consent contracts); the person-subject is the stress case (codex's
repo-subject barely exercises it). Parent:
`hermes-retrieval-primitives-contract.md`; subject layer:
`project-layer-scaffold.md`.
Topics: memory-retrieval, subject-hermes, consent, recall, private-memory, per-query-consent,
purpose-binding, data-minimization, revocation, erasure, break-glass,
patient-advocate, memory-gateway, medx
Repository context: openxFactory (neutral consent path; person-subject is the stress case, e.g. MedxFactory)
Captured: 2026-07-21

## Possible feats

- **`subject_consent_model` schema** composing the ratified `consent-profile`.
- **Governed `recall` path** — purpose-bound, minimized, fail-closed, audited.
- **Break-glass emergency exception** — dual-authorized + mandatory audit.
- **Subject transparency log** — the subject sees who recalled what.

## Why the subject layer is the hardest case

The other layers' retrieval is over operational/expert knowledge; the subject
layer's `recall` can be over *a person's private memory*. When the subject is a
Medx patient, consent is not a one-time ingest checkbox — it is checked on
**every recall**, scoped to purpose, revocable at any moment, and legally
load-bearing (the Legal & Compliance Counsel's data-protection constraints
apply). codex's repo-subject barely exercises this (a repo has no consent to
give); Medx exercises all of it. So the path is designed for the person-subject
and degrades gracefully to the artifact-subject.

## The subject consent model

The subject owns its consent (or its rights-advocate acts for it); it composes
the ratified gateway `consent-profile`:

```yaml
schema_version: 1
kind: subject_consent_model
consent:
  default: deny                       # fail-closed
  advocate_ref: <rights-advocate>     # e.g. Patient Advocate — may act for the subject
  revocable: true
  minimization: minimum_for_purpose   # return only what the purpose needs
  grants:
    - grantee: <role | caller class>  # WHO
      categories: [<memory categories>]  # WHAT (per-category, not all-or-nothing)
      purpose: [<bound purposes>]        # WHY (recall must declare one)
      expires: <duration | null>         # HOW LONG
      recipients: [<layers | tenants>]   # WHERE it may flow
  break_glass:                        # domain-specific exception (Medx)
    allowed: false
    requires: [emergency_declaration, dual_authorization]
    audit: mandatory
    notify_subject: after_the_fact
```

Consent is **granular**: a patient may consent to recalling medication history
*for care coordination* but not *for research*, and to the care team but not to
the operator's analytics.

## The governed recall path

```text
recall(subject_ref, {purpose, requested_scope, caller_context})
  → {granted: [context_packet], denied: [{scope, reason}]}
```

Check sequence (fail-closed — any unmatched scope is denied, with a reason):

1. **Identity** — authenticate the caller and its role.
2. **Tenant / ACL** — the subject's tenant + the row visibility (from ingestion).
3. **Consent match** — for each requested category: is there a grant matching
   grantee **and** category **and** the declared purpose, not expired, with the
   caller as a permitted recipient? No match → denied.
4. **Minimization** — filter the matched set to the minimum the purpose needs
   (data-minimization; a GDPR/HIPAA principle, enforced not assumed).
5. **Return** — consented context-packets + an explained denial list (so the
   caller knows what it *could* request with the right purpose/consent).
6. **Audit** — a gateway `usage-event` for granted **and** denied recalls,
   written to a **subject-visible transparency log** (the subject can see who
   recalled what, when, and why).

The defining property: **purpose binding**. An authorized caller with a valid
role is still denied if its declared purpose isn't among the consented purposes —
authority is necessary but not sufficient; purpose-fit is also required.

## Revocation & erasure — immediate at query time

Consent `revocation` and `erasure` (both ratified gateway contracts) take effect
at the next recall: a revoked grant no longer matches (future recalls denied),
and erased memory is not returned and is purged from the store. There is no
cache that can serve revoked content — the consent match is evaluated live.

## Break-glass (life-critical domains only)

For emergencies (a Medx clinical example: an unconscious patient), a domain may
enable a break-glass exception — but it is an **audited, dual-authorized
exception, never a silent bypass**: it requires an emergency declaration + a
second authorizer, logs mandatorily, and notifies the subject after the fact.
Default `allowed: false`; a domain that turns it on owns that decision through
its Legal & Compliance constraints. codex has no break-glass (no life-critical
recall).

## The rights-advocate

For a person-subject, the subject-layer **rights & consent advocate** (Patient
Advocate in Medx) may set, scope, and revoke consent on the subject's behalf,
and is the escalation target when a recall is denied but arguably in the
subject's interest. This is the neutralization-gradient's "rights & consent
advocate" slot — central in Medx, near-empty in codex.

## Cross-layer honoring

The subject owns consent; the client (operator) and domain must honor it. In
particular, a subject's private memory **never** promotes to the domain's
cross-client `domain_learning` without explicit consent **and** de-identification
— the tenant-isolation + promotion gate from the memory-boundaries drafts, made
strict for person-subjects.

## Open questions

- **Purpose vocabulary** — a neutral controlled list of purposes, or
  domain-defined (Medx: care/billing/research/legal)?
- **Consent capture UX** — who collects and maintains a subject's consent (the
  advocate, an onboarding flow, an external consent system reached via an
  adapter)?
- **Minimization enforcement** — is "minimum for purpose" a policy the
  synthesizer applies, or a hard filter in the executor (leaning: hard filter)?
- **Transparency-log access** — how does a subject (patient) actually see their
  recall log, and through which layer's surface?
- **Break-glass scope** — domain-gated only, or also client-policy-gated (an
  operator that forbids break-glass even where the domain allows it)? Note the
  ratified gateway already ships a `break-glass-profile` schema — compose it,
  don't redefine it.
- **Transparency-log contract** — the ratified contracts cover `audit-event` and
  `usage-event`, but a *subject-visible* recall log is an extension: is it a new
  neutral contract (a projection of audit events scoped to the subject), and
  which layer serves it?
