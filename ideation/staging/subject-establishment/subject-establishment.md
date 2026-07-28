# Staged: Subject Establishment — facts to a correctly configured subject, in any domain

Status: staged
Kind: capability-proposal
Summary: Every DomainxFactory has the same motion at the start of a subject's
life: establish the facts about a newly admitted subject, design the
best-practice way that subject should be set up **in domain terms**, decide
which external system of record it will live in, map the design into that
system, review and approve, apply, and verify. Today each domain is
inventing this separately — Ledgerx is building it now for a new client
company, and Medx's new patient, codex's new engineering project, Opsx's new
managed estate, and Adx's new campaign are the same shape with different
nouns. Brett named the generalization 2026-07-28: *"this concept of intake is
also a general startup. it is the same as new patient or new engineering
project. there is a setup of facts and then the best practice way to setup
that subject in that domain. some of this neutral concept should be elevated
to openXfactory."*
Topics: subject-onboarding, intake, neutral-design, platform-realization, reference-archetype, conformance-tiering, setup-audit, provisioning, dtn
Repository context: openxFactory owns the neutral contracts; LedgerxFactory is the first full instantiation (`ideation/staging/company-provisioning/`, MSBC company setup); Medx/codex/Opsx/Adx are the named second consumers
Staging ID: `openxFactory:staging:subject-establishment`
Source: LedgerxFactory's company-provisioning topic (2026-07-28) — the MSBC rehearsal hit an unconfigured client company and the design work that followed produced a layered model (neutral books design, then platform realization) that is visibly not accounting-specific
Target capabilities: a NEW neutral capability (`subject-establishment` or similar) + DTN-017; consumers instantiate rather than re-derive
DTN candidate: DTN-017

## The neutral shape

Strip the accounting nouns from LedgerxFactory's
`company-provisioning/layered-books-design.md` and this remains:

1. **Subject fact set** — what is true about this subject, assembled from
   authoritative registries, self-report, and observation, with a
   **provenance grade per fact** (a fact from a state registry and a fact a
   client typed into a wizard are not the same evidence).
2. **Neutral setup design** — how this subject SHOULD be established, in
   domain terms, naming no external product. Elements carry **semantic
   roles**, not vendor identifiers, which is precisely what makes step 5
   possible.
3. **Reference archetype** — the domain keeps versioned archetype-level
   designs that per-subject research STARTS from. The subject design stays
   authoritative; the archetype is an accelerator and the conformance
   yardstick.
4. **System-of-record selection** — the tenant layer decides which external
   system this subject will live in (and which estate/instance of it).
5. **Platform realization** — a per-platform overlay mapping every neutral
   element to concrete objects in that system, authored by that platform's
   specialist. A second platform is a second overlay of the same design.
6. **Review with conformance tiering** — conforming designs auto-approve
   under a standing envelope; deviating ones escalate to the domain's
   licensed/expert human. Deviation resolutions are harvested back into the
   archetype, so the auto-approve share grows.
7. **Apply, then verify by read-back** — the application is a granted act
   against external enforcement; conformance is proven by reading the
   resulting state and diffing against intent. An unverified apply is not
   green.
8. **The audit mirror** — read an existing subject's configuration, **lift it
   to the neutral representation**, diff against the design the research
   would have produced, propose a migration, human-approve, apply, verify.

## The same motion in five domains

| Domain | Subject | Neutral design is… | System of record | Realization is… |
|---|---|---|---|---|
| Ledgerx | new client company | chart of accounts as semantic roles, posting-group taxonomy, accounting policies | MSBC / QuickBooks / Xero | G/L numbers, posting-group matrices, number series, tax setup |
| Medx | new patient | problem list, care-plan structure, medication reconciliation, care-team roles, consent posture | the clinic's EHR | chart sections, order sets, encounter templates, flowsheets |
| codex | new engineering project | branch/review policy, environment topology, quality gates, release discipline | GitHub / GitLab | rulesets, workflows, environments, required checks |
| Opsx | new managed estate | identity model, endpoint baseline, backup/monitoring posture, patch policy | M365 / Intune / Azure | conditional access, configuration profiles, policy assignments |
| Adx | new campaign subject | audience/measurement model, funnel stages, attribution policy | GA4 / Meta / Ads | properties, conversions, audience definitions |

The columns differ; the pipeline does not. That is the DTN test.

## Claims

1. **The design/realization split is the load-bearing neutral idea**, and it
   is the same idiom the stack already uses one level up (neutral contract +
   per-domain overlay). Here it is neutral subject design + per-platform
   realization. The payoff is identical: portability (the design survives a
   platform migration), reviewability (an expert reviews domain judgment,
   not vendor trivia), and a second platform costs a mapping, not a
   redesign.
2. **Provenance-graded facts are neutral and already half-modelled.** The
   fact set overlaps `credential-contracts`' consent references, the
   `consent-instrument-contract` staging topic (DTN-016), and
   `governed-derived-model`'s conformance vocabulary. This capability should
   consume those rather than restate them.
3. **Conformance tiering is a neutral GOVERNANCE dial, not domain content.**
   "Conforming ⇒ standing envelope; deviating ⇒ expert review; resolutions
   harvested into the archetype" is the same machine as DTN-015's
   correction→promotion loop and `governed-derived-model`'s tiered
   conformance. Strong candidate to be expressed in terms of those rather
   than as a new mechanism.
4. **Verify-by-read-back belongs in the neutral contract**, because every
   domain applies through external enforcement it does not own (EHR, GitHub,
   Intune, MSBC) and every one of them can silently do something other than
   what was asked. Ledgerx already learned the sharp version of this: the
   platform may validate before it authorizes, so a probe that never reaches
   the authorization layer proves nothing.
5. **The audit mirror is the commercial half.** "Read what you have, lift it
   to neutral, tell you how it differs from best practice, migrate it on
   approval" is a product motion in every domain (chart audit, repo-hygiene
   audit, tenant security-posture audit, ad-account audit). Neutralizing the
   lift makes it one capability instead of five.
6. **The authority split generalizes exactly.** Establishing a NEW subject
   in an empty environment is low-risk (nothing to damage; wrong results are
   discarded by re-provisioning). MIGRATING an established subject with
   history is high-risk and is proposal → approval → apply → verify, always.
   These must not share a grant in any domain.
7. **Worker archetypes already exist for this.** The neutral omnigent
   archetypes (`frame`, `generate`, `verify`, `challenge`,
   `assemble_for_admission`) cover the whole pipeline: `generate` for the
   design and for the realization, `verify`/`challenge` for adversarial
   review, and the terminal apply belongs to external enforcement and its
   human authority, never an archetype — which is exactly the existing rule.
   No new archetype is needed; the contribution is the **pipeline shape**
   and the two artifact kinds.
8. **Layer ownership is already ratified vocabulary.** Subject layer holds
   the facts and the subject's design; tenant layer holds the archetype
   library, the standard, and the system-of-record decision; domain layer
   holds correctness criteria and commissions the research. This maps onto
   Subject/Tenant/Domain without strain, which is itself evidence the
   pattern is neutral.

## What is probably NOT neutral

Stated so the delta does not over-reach:

- The CONTENT of any design or archetype (a chart of accounts, a care-plan
  template, a branch-protection baseline) is irreducibly domain material and
  stays in the DomainxFactory.
- Which external systems are supported, and the mapping tables — per-domain
  overlays.
- The expert seat that reviews a deviating design (licensed accountant,
  clinician, staff engineer) — named by each domain's Hermes.
- Whether a domain even HAS a system of record to configure. Some subjects
  may be established entirely inside the factory.

## Open questions

1. **One capability or two?** Establishment and audit/migration differ by
   risk class (Claim 6). Ledgerx's topic already leans toward a pair — does
   the neutral layer mirror that split, or carry one capability with two
   authority classes?
2. **Is "system of record" a new neutral concept, or the existing
   `client-infrastructure` / estate vocabulary generalized?** Ledgerx's
   `ledgerx-ledger-estate` (binding dial: operator-hosted vs client-hosted,
   identity per estate) looks like a domain instance of something neutral,
   and Opsx's managed-estate model may be another. Worth checking before
   inventing.
3. **How much does this actually consume vs restate?** Candidate
   consumables: DTN-016 consent instrument, DTN-015 correction→promotion,
   `governed-derived-model` tiered conformance, `neutral-job-envelope`,
   `workflow-gate-contract`, `credential-contracts`. A good outcome is a
   thin capability that composes existing ones.
4. **Second-domain proof before promotion.** Which domain instantiates
   second — Medx new-patient (richest consent/custody constraints) or codex
   new-project (fastest to realize, and codexFactory already has
   governed-derived-model and GitHub administration in place)? The register
   convention wants a second consumer before neutralizing.
5. **Does the neutral design artifact belong in Hermes memory** (Ledgerx's
   ruling: subject design in Subject Hermes memory, archetypes + standard in
   Tenant Hermes memory, applied version's digest/locator in the grant
   evidence) — is that storage rule itself neutral, or a Ledgerx choice?

## Exit path

A neutral OpenSpec proposal in openxFactory carrying: the two artifact kinds
(neutral subject design, platform realization) with their schemas, the
provenance-graded fact set, the reference-archetype lifecycle, the
conformance-tiering dial expressed via existing capabilities where possible,
the apply-and-verify-by-read-back obligation, and the audit-lift mirror.
Gated on: LedgerxFactory's `company-provisioning` reaching proposal (first
instantiation, in flight), and a second domain naming its instance (open
question 4). Register as **DTN-017**.
