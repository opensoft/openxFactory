# Tasks — add-omnigent-domain-terminology

## 1. Direction and ratification

- [x] 1.1 Direction 2026-08-09 by Brett Heap: keep the neutral cross-domain
      spine, but render all user notices and logs in domain best-practice,
      well-adopted terminology so domain experts can read them. Analysis
      recorded in the proposal: annotate, never rename — renaming would point
      each domain at a different framework and churn load-bearing ids.
- [x] 1.2 **RATIFIED 2026-08-26** by Brett Heap — in-session instruction,
      verbatim: "do the omnigent-terminology ratification" (the act itself,
      same class as the `add-dashboard-account-menu` and
      `add-family-enumeration-check` precedents: an in-session instruction
      naming this change IS the ratifying act). Ratifies exactly what this
      task named and what the proposal's Impact section scopes as its three
      ADDED requirements: the optional `terminology` block, the
      descriptive-crosswalk rule (`standards_alignment`, including the
      `no_clean_equivalent`-requires-a-note discipline), and the
      human-facing rendering requirement. READ-BACK — what this unblocks:
      the contract layer's standing is settled; §2's schema, semantic
      validator checks, and `contracts/policies/standards-bodies.yaml`
      registry (already realized on main under `target_release: implemented`)
      now rest on a ratified rule rather than a draft one, and any domain is
      free to start populating its own `terminology` block. READ-BACK — what
      this does NOT unblock, because ratifying the RULE is not realizing it
      per domain: §3's five domain populations (3.1–3.5) stay open, each its
      own change in its own repo, with the crosswalk framework chosen per
      domain at realization (task 5.3 — explicitly out of this change's
      scope, not this ratification's to decide); 3b.5d, the APQC written
      licence confirmation, stays unobtained — this specifically gates
      LedgerxFactory and AdxFactory, whose PCF 8.0/3.0 crosswalks were
      pulled from their shipped overlays pending exactly this licence
      (3b.5b), not MedxFactory, which registers no APQC/PCF mapping at all
      by design (3b.5i: patient-safety framing outranks terminology, all
      eleven medical worker classes record `no_clean_equivalent` against the
      provider taxonomy on purpose); 3b.5f, the ledgerx UN/CEFACT+BIAN and
      adx marketing brief results, stays unapplied; and §4's consumer
      follow-up (OpsxFactory's own adjudication-refusal vocabulary, outside
      this overlay entirely) stays unaddressed. Front matter `Status:` moves
      to `ratified` with a record-citing `Ratified:` line, since no
      approving OpenSpec change exists to name this act.

## 2. Contract (drafted, validator-green)

- [x] 2.1 `contracts/omnigent/omnigent-domain-overlay.schema.yaml`: optional
      `terminology` block (workers with `display_label` + optional
      `standards_alignment`; `job_types`, `stop_conditions`, `routing` as
      label maps via the new `label_map` $def). Additive and optional —
      all five existing overlays verified still valid.
- [x] 2.2 `scripts/validate-omnigent-contracts.py`: semantic checks — orphan
      terminology keys, duplicate display labels within a vocabulary,
      `no_clean_equivalent` without a note (per body), and crosswalk body ids
      resolving to the canonical registry.
- [x] 2.2b MULTI-BODY revision (Brett 2026-08-09: "if there are well adopted
      multiple standards, then we should have multiple mappings: one for each
      large body"). `standards_alignment` changed from a single object to a
      map keyed by standards-body id — at most one entry per body, multiple
      bodies expected. Revised while still draft, before ratification.
- [x] 2.2c `contracts/policies/standards-bodies.yaml` — canonical registry of
      recognized bodies (id, steward, `names`, scope, attribution note).
      `names` is load-bearing: bodies name different KINDS of thing
      (practices / processes / skills / roles / controls / competencies /
      clinical concepts), and a crosswalk is only honest if the kind is
      visible. Seeded with the cross-domain and per-domain menu; SOURCING
      CAVEAT recorded in the file — term spellings and framework versions are
      from working knowledge and MUST be verified against each body's current
      publication before a domain commits its crosswalk (task 3.x).
- [x] 2.3 Positive example extended to demonstrate terminology + both
      crosswalk shapes (a mapped term and an honest `no_clean_equivalent`).
      Note: authoring this caught its own bug — the first draft referenced
      ids the example does not declare, and the new orphan-key check
      rejected it, which is the check working.
- [x] 2.4 Three negative fixtures with `# expect:` markers (one per rule):
      `overlay-terminology-orphan-label.yaml`,
      `overlay-terminology-unmapped-without-note.yaml`,
      `overlay-terminology-unknown-body.yaml`. All rejected as expected;
      full contract-family check green.

## 3. Domain follow-ups (each its own change, in its own repo)

- [ ] 3.0 Per domain, VERIFY the chosen bodies' current terms and versions
      against each body's own publication before committing a crosswalk (the
      registry's sourcing caveat). A wrong term is worse than none.
- [ ] 3.1 Populate `terminology` in OpsxFactory. Candidate bodies: `itil4`
      (practices), `sfia` (skills — closest to worker shape), `apqc_pcf` 7.0
      (processes), `cobit_2019` (audit-facing), `nist_csf` (security-adjacent
      reviewers). `no_clean_equivalent` expected for `blast_radius_reviewer`
      and `credential_grant_reviewer`, which have no clean counterpart in a
      process framework.
- [ ] 3.2 Populate `terminology` in LedgerxFactory. Candidate bodies:
      `apqc_pcf` 8.0 (processes — 8.2 AP, 8.3 AR, 8.4 general accounting),
      `coso_icif` (controls — the natural home for the segregation-of-duties
      boundary), `ima_mac` (competencies), `aicpa` (standards/competencies).
      NOT GAAP/IFRS: those are REPORTING standards governing what the books
      say, not what a worker is — ledgerx's reporting-standard grounding
      already lives in the subject books-design layer.
- [ ] 3.3 Populate `terminology` in AdxFactory. Candidate bodies:
      `apqc_pcf` 3.0 (processes), `iab` (ad-tech specs/taxonomies — fits the
      media and audience classes, not the creative or compliance ones),
      `cim` (competencies), `ama_marketing` (concept definitions).
- [ ] 3.4 Populate `terminology` in codexFactory. Candidate bodies:
      `swebok` (knowledge areas), `sfia` (skills), `iso_iec_ieee_12207`
      (life-cycle processes), `apqc_pcf` 2.0.
- [ ] 3.5 Populate `terminology` in MedxFactory — WITH CARE. The provider
      taxonomies (`nucc_taxonomy`, `hl7_fhir_practitionerrole`) describe
      humans holding CLINICAL STANDING; medical Omnigent workers are
      reasoning agents and hold none. Mapping a reasoning agent onto a
      provider role would imply standing it must never appear to have, so
      `no_clean_equivalent` is expected to be the honest answer for most
      medical worker classes. `snomed_ct` fits artifact/job_type labels (the
      clinical CONTENT reasoned about), never the worker roles.

## 3b. Regional coverage (Brett 2026-08-09: "do we have a different set for asia and specifically china?")

- [x] 3b.1 GAP CONFIRMED from the artifact: all 17 registered bodies are
      Anglo-American and the registry carries no region/jurisdiction field,
      so the skew is invisible in the data.
- [x] 3b.2 First live-source verification RETURNED (accounting/China):
      `LedgerxFactory .../supporting-docs/china-accounting-bodies-research-report.md`
      — 13 registry-shaped entries, mainland/HK/Taiwan/Macau kept separate,
      every candidate confirmed/corrected/rejected, all 14 worker roles
      crosswalk-analysed with authority caveats. It CORRECTED committed work
      (see 3b.3) and confirmed the reporting-standard exclusion holds in all
      four jurisdictions.
- [x] 3b.3 DEFECT FOUND AND FIXED: APQC category numbers are
      version-sensitive (PCF 8.0 puts finance at 9.0; the 8.x numbering is
      the 7.0.5-era layout, which is also the current public Mandarin
      version). Our ledgerx and adx mappings had combined a current body
      reference with superseded numbering. Versions are now pinned in every
      APQC mapping, the opsx header no longer claims an APQC mapping it does
      not assert, and the registry's apqc_pcf entry records the
      version-pinning rule plus APQC's attribution terms so the error cannot
      recur silently.
- [x] 3b.4 LANDED 2026-08-09: all 13 verified entries integrated; registry
      now holds 30 bodies. `jurisdiction` added to EVERY body (not just the
      new ones) — without it the regional coverage stays invisible in the
      data, which was the original defect: mainland_china 9, macau 2,
      hong_kong 1, taiwan 1, united_states 6, united_kingdom 1,
      international 10. Verified entries carry the report's
      current_version / status / source_url / term_list_availability /
      confidence and its inline reasoning verbatim; the original 17 lack
      them, and the header now states that asymmetry rather than hiding it.
      `gb_t_46704_financial_shared_services` registered as recommended
      shared-service GUIDANCE, explicitly not a Chinese APQC equivalent.
      YAML parses, ids unique, contract family and all five overlays green.
- [x] 3b.5a US ACCOUNTING CLEANED AND LOCKED 2026-08-09. Registry 30 -> 41
      bodies. Verdicts applied: `apqc_pcf` corrected (PCF 8.0, published
      2026-02-27); `coso_icif` confirmed; `ima_mac` corrected to the 2025 IMA
      Competency Framework; the compound `aicpa` REJECTED and split into
      `aicpa_professional_standards` + `aicpa_foundational_competencies`,
      with `cgma_competency_framework` separate — the same split the CICPA
      research forced. Added: COSO ERM, IIA IPPF + IIA competency framework,
      PCAOB, IRS Circular 230, NASBA/UAA, BLS SOC, O*NET 30.3, AICPA Trust
      Services Criteria. SOX 404 REJECTED as a taxonomy, recorded so it is
      not re-proposed.
- [x] 3b.5b APQC HIERARCHY REMOVED FROM SHIPPED OVERLAYS (ledgerx, adx).
      Two reasons, the second decisive: (1) the numbers were wrong in EVERY
      version — 7.0.5 also used 9.x finance numbering, so the earlier
      "fix" pinned 8.x numbers to a version that never used them, which read
      as verified while being false; (2) APQC's terms prohibit shipping a
      copied PCF hierarchy in product configuration without written licence
      confirmation, and a domain overlay IS product configuration. Correct
      PCF 8.0 references are recorded in the report (9.6 AP, 9.3 general
      accounting, 9.9 taxes, with stable element IDs) for re-adding once
      licensed. COSO and IAB crosswalks retained.
- [x] 3b.5c O*NET 30.3 ADOPTED in the accounting overlay 2026-08-09
      (LedgerxFactory): 14/14 workers crosswalked with the report's verified
      SOC codes, CC BY 4.0 attribution carried in the overlay header
      (including the required "USDOL/ETA has not endorsed these
      modifications"), and the human-job-vs-artifact-only authority gap
      recorded per worker — `bookkeeper` most sharply, since the human
      occupation includes posting. Three workers recorded
      `no_clean_equivalent`. This is the licence-clean replacement for the
      APQC layer: the terms permit exactly this use, provided attribution
      is stated.
- [ ] 3b.5d Obtain APQC written licence confirmation if PCF element names or
      numbers are ever to ship in product configuration.
- [x] 3b.5e BRIEFS WRITTEN for every remaining domain (2026-08-09). Adx's
      lives in its own repo (it has an active change);
      opsx/codex/medx briefs live here in `research/` because codex and
      medx have no active omnigent change to attach to and this change owns
      the commissioning task. All four lead with REUSE RIGHTS framed as
      "may we embed element names in a YAML file shipped in a public repo",
      forbid guessed identifiers, and state that "no equivalent" and "do not
      register" are useful answers. FOLDER RULED (2026-08-22, Brett,
      in-session multiple choice, recommended option adopted): these briefs
      were authored in place by this change — no staging source, no
      transition — so they do not live under `supporting-docs/`, whose
      manifest is a transition artifact (`proposal-support verify` was
      failing on the manifest's absence, and writing one by hand would have
      invented a staging source). They live in `research/` instead; the
      reserved folder name keeps meaning material the forward transition
      MOVED, with source hashes.
      Per-domain risk each brief targets:
      - opsx (`opsx-it-operations-bodies-research-prompt.md`): 9 shipped
        ITIL 4 / SFIA crosswalks, none verified. Licence risk is real on
        BOTH — ITIL is PeopleCert property and SFIA operates a commercial
        licensing scheme — so this domain may face the APQC problem twice.
      - codex (`codex-engineering-bodies-research-prompt.md`): no
        terminology block at all, so this is from-scratch population. The
        sharp question is the Scrum Guide's CC BY-SA: share-alike could
        oblige our own configuration file to be CC BY-SA, which would decide
        whether Scrum vocabulary is usable at all. Also flags
        `scrum_master_worker` sharing a name with a human role holding
        authority over people.
      - medx (`medx-clinical-bodies-research-prompt.md`): patient-safety
        framing OUTRANKS terminology. Provider taxonomies describe humans
        with clinical standing and legal accountability; labelling a
        reasoning agent with one would imply standing it must never appear
        to have. The brief states plainly that "register nothing; record
        no_clean_equivalent for all eleven and rely on display labels" is an
        acceptable and possibly correct outcome.
- [x] 3b.5g OPSX BRIEF RUN 2026-08-09 against live primary sources. RESULT:
      BOTH shipped bodies fail the reuse test — the APQC problem twice over.
      SFIA is prohibited outright ("you cannot sub-licence SFIA to others
      through your products"; Partner Licence required for commercial product
      use); ITIL is PeopleCert property, all rights reserved, with no
      third-party citation permission establishable from primary sources.
      COBIT assessed and rejected (ISACA requires a licence to incorporate
      into software given to third parties). Both removed from the shipped
      opsx overlay and replaced with O*NET at occupation level (six verified
      SOC codes) under CC BY 4.0 with attribution carried in the overlay.
      NIST CSF 2.0 registered as licence-clean (US Govt work, public domain,
      published 2024-02-24) BUT its Function names could not be enumerated
      from the pages fetched, so no function-level mapping was authorised —
      recorded rather than guessed. Report:
      `research/opsx-it-operations-bodies-research-report.md`.
      PATTERN NOW THREE FOR THREE: every commercially stewarded body checked
      (APQC, SFIA, ITIL, COBIT) has failed the product-configuration reuse
      test, and every licence-clean answer has been O*NET. That is a finding
      about the approach, not four coincidences.
- [x] 3b.5h CODEX BRIEF RUN 2026-08-09. Same result a fourth time: SWEBOK v4
      needs IEEE permission for commercial republication, SFIA is prohibited
      (opsx round), ISO/IEC/IEEE 12207 is sold. The Scrum Guide's CC BY-SA
      question is ANSWERED: bare role/event names are very likely outside
      copyright, but share-alike could oblige our own configuration to be
      CC BY-SA if definitional text were reproduced — asymmetric risk for a
      label we can write ourselves, so assessed and DECLINED, recorded in the
      registry so the reasoning is not relitigated. codex terminology built
      from scratch (11 workers, 12 job types, 6 stop conditions, 6 routing
      classes) on O*NET at occupation level, 8 mapped and 3
      no_clean_equivalent. `scrum_master_worker` is deliberately unmapped AND
      its display label avoids the term, because "Scrum Master" is a human
      role holding facilitation authority over PEOPLE — a sharper version of
      the bookkeeper-includes-posting hazard. Report:
      `research/codex-engineering-bodies-research-report.md`.
- [x] 3b.5i MEDX BRIEF RUN 2026-08-09. The only domain to fail on BOTH
      category and licence. Category: every clinical taxonomy names either
      humans with clinical standing (NUCC, FHIR PractitionerRole, O*NET
      healthcare) or clinical content (SNOMED, LOINC, ICD, CPT); reasoning
      agents are neither. Licence: GRADE — the one body genuinely naming
      appraisal ACTIVITY, adopted by Cochrane/WHO/NICE — is CC BY-NC-ND 4.0,
      so NonCommercial and NoDerivs both bar it; SNOMED CT needs a vendor
      Affiliate Licence with fees and sub-licensing duties.
      OUTCOME: no crosswalk body registered. Display labels only, PLUS one
      machine-readable safety statement — all eleven workers record
      `no_clean_equivalent` against the PROVIDER taxonomy specifically,
      because that is the mapping a contributor would reach for and it is
      the dangerous one. Recording the refusal in data was worth more here
      than a crosswalk. Report:
      `research/medx-clinical-bodies-research-report.md`.
- [x] 3b.5j ALL FIVE DOMAINS VERIFIED. Result across the family: every
      commercially stewarded body assessed — APQC, SFIA, ITIL, COBIT,
      SWEBOK, ISO/IEC/IEEE 12207, GRADE, SNOMED CT — fails the
      product-configuration reuse test. O*NET (CC BY 4.0) is the only
      licence-clean crosswalk in four domains, and medx registers none. The
      registry was seeded from what practitioners TALK ABOUT rather than
      what a product may LAWFULLY EMBED, and those are different sets.
- [ ] 3b.5f Apply the results of the remaining brief (ledgerx UN/CEFACT +
      BIAN, and the adx marketing round) as they return. (ledgerx
      UN/CEFACT+BIAN, adx marketing, opsx, codex, medx) as they return.

## 4. Consumer follow-up (named, not assumed)

- [ ] 4.1 Domain surfaces that render human-facing vocabulary OUTSIDE the
      overlay — e.g. OpsxFactory's fixed-order adjudication refusals, which
      name internal check ids (`tenant_managed`, `environment_operable`) in
      messages a human reads — adopt the same render-the-domain-label
      principle in their own contracts. The principle is not scoped to
      omnigent alone.

## 5. Explicitly out of scope

- [ ] 5.1 Renaming any worker class id, archetype, permission, or credential
      family — the whole point is that presentation changes and identity
      does not.
- [ ] 5.2 Asserting conformance with or certification by any named framework.
- [ ] 5.3 Choosing each domain's crosswalk framework (that is 3.1–3.4, per
      domain, with the domain's owner).
