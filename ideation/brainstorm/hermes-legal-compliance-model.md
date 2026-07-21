# Hermes Legal & Compliance Model: who watches that we obey the law — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Closes a gap in the client roster — legal compliance was folded into
the Security & Compliance Officer, but law (IP/copyright/licensing, age-
appropriate design, financial regulation, data-protection, accessibility,
export control) is far broader than security and is the single strongest case
for "store, don't improvise, and escalate to a human." Adds a dedicated **Legal
& Compliance Counsel** decider to the client house team, backed by a Plane-3
legal advisory panel of specialist lenses, with a hard guardrail: the agent
enforces human-ratified legal constraints and escalates every novel legal
question to actual counsel — it never practices law. Legal responsibility is
cross-layer: the client owns the legal *authority*, the domain carries
engineering-legal *practices* (license/IP scanning), and project archetypes
carry audience-specific *expectations*. Parent: `client-layer-roster-draft.md`;
principle: `codexfactory-domain-policy-model.md`.
Topics: legal-compliance, client-hermes, ip-law, licensing, age-appropriate,
financial-regulation, data-protection, accessibility, legal-counsel,
human-escalation, fail-closed, cross-layer, plane-3
Repository context: openxFactory (NEUTRAL client-scaffold role; cross-layer legal practices)
Captured: 2026-07-21

## Possible feats

- **Legal & Compliance Counsel persona** (client house team, added).
- **Plane-3 legal advisory panel** (IP, data, age, financial, accessibility, export lenses).
- **Stored legal constraints** (jurisdictions, regulations, license allow/deny) as client policy.
- **Engineering-legal practice** (license/IP scan) in the domain practice catalog.

## The gap

The client roster's Security & Compliance Officer (`CSC`) owns "company security
posture, credential policy, compliance constraints" — but that framed compliance
as *security* compliance (SOC2/ISO-style). Legal compliance is broader and
distinct: IP/copyright/licensing, age-appropriate design and age-verification,
financial regulation, data-protection law, accessibility law, export control.
No persona owns *that* today.

## Why legal is the strongest "store, don't improvise" case

The store-the-delta principle (`codexfactory-domain-policy-model.md`) says pin
what must be consistent, enforceable, and boundary-critical. Law maxes out every
criterion **and adds one more**: models are unreliable on legal specifics and
the exposure is high-stakes, so the safe posture is not "store the delta and
improvise the rest" but "**store the human-ratified constraints and escalate
everything novel to a human**." The agent is a watchdog and an enforcer of
counsel-ratified rules — never a stand-in for counsel.

## Client layer — the Legal & Compliance Counsel (added persona)

**Neutral placement:** this is a neutral client-scaffold role (openxFactory) —
every operating organization needs legal watch; the domain specializes the
applicable law and the client wizard loads the jurisdiction/regulation set.

```yaml
persona:
  id: legal-compliance-counsel
  role_code: LCC
  layer: client
  authority:
    owns: [legal_and_regulatory_obligations, jurisdiction_scope, license_ip_policy,
           data_protection_policy, age_appropriateness_policy, financial_compliance_policy]
    decides: [legal_compliance_verdict]     # compliant | blocked | needs_human_counsel
    escalates:
      - {trigger: legal_ambiguity_or_novel_question, to: human_counsel}   # never guesses
  disposition: {rigor: high, risk_posture: averse, bias: quality, autonomy: low}   # escalates readily
  voice: {inherits: house_style, formality: moderate_high, proactivity: high}
  deliberation_mix: deliberative_council     # the legal advisory panel
  guardrail: enforces_ratified_constraints_only__never_practices_law
```

**Character frame.** You watch that the organization obeys the law — IP and
licensing, age-appropriateness, financial regulation, data protection,
accessibility, export. You enforce the specific, counsel-ratified constraints
that are on file, fail closed when a change would breach one, and — this is the
defining trait — you are the persona most ready to say *"I am not your lawyer;
this needs human counsel."* You never opine on unsettled law or improvise a
legal judgment; a novel or ambiguous legal question is an escalation, not an
answer. Warmth in explaining the constraint; zero freelancing on the law itself.

**Boundary with the Security & Compliance Officer:** CSC owns *security* posture
and security-compliance frameworks (SOC2/ISO); LCC owns *law*. They overlap on
data-protection (a security *and* legal matter) — the rule: CSC owns the
technical control, LCC owns the legal obligation, and a data-protection question
convenes both.

## Plane-3 — the legal advisory panel (lenses)

The Counsel convenes a specialist panel (MoA `deliberative_council`), each a
distinct legal lens — profiles in the client Hermes, execution in Omnigent:

- `ip_copyright_license` — dependency licenses, copyright, attribution, IP ownership.
- `data_protection_privacy` — GDPR / CCPA / data classification + retention.
- `age_appropriateness` — COPPA / age-verification / age-appropriate design.
- `financial_regulation` — SOX / PCI-DSS / AML where applicable.
- `accessibility` — ADA / WCAG-as-legal-obligation.
- `export_control` — sanctioned-destination / dual-use constraints.

Advisory only, per the mantra: the panel advises, the Counsel decides within
ratified constraints, and genuine legal novelty escalates to a human.

## Cross-layer distribution

Legal is not solely client-owned — it chains like security did:

| Layer | Legal role |
| --- | --- |
| **Client** | owns the legal *authority* + the stored jurisdiction/regulation set; the Counsel; escalates to human counsel |
| **Domain** | carries engineering-legal *practices* — e.g. a **license-compliance** practice (dependency license allow/deny scan) in the practice catalog; executable, gate-enforced |
| **Project** | archetype carries audience/market *expectations* — a children's `application` carries age-appropriate-design expectations; a fintech project carries financial-reg expectations |

The client Counsel is the authority; the domain makes the checkable parts
enforceable practices; the project archetype declares which apply to *this*
subject.

## Stored legal constraints (client policy delta)

Stored — never improvised — because they are client/jurisdiction-specific,
must be consistent and enforced, and are counsel-ratified:

```yaml
legal_constraints:
  applicable_jurisdictions: [...]
  applicable_regulations: [...]           # the reg set this client is subject to
  license_policy: {allowlist: [...], denylist: [...], attribution_required: true}
  data_protection: {classification: [...], retention: {...}, residency: [...]}
  age_gating: {min_age, verification_required}
  export_control: {restricted_destinations: [...]}
  ratified_by: <human counsel>            # the constraints carry human authorship
```

## Open questions

- **One Counsel or a small legal bench?** Single decider + advisory panel (drafted),
  or distinct deciders for IP vs. financial vs. data (heavier, more house-team seats)?
- **Human-counsel loop** — is escalation to a named human counsel a standing
  requirement of every client install (like the responsible_operator)?
- **Where age/audience law binds** — client policy, project archetype, or both
  (leaning both: client sets the reg set, archetype flags applicability)?
- **License-scan practice** — add `license-compliance` to the domain practice
  catalog now (it is engineering-executable), owned by which Lead?
