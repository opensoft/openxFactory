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
- [x] 3.0a DISCHARGED FOR OPSX AND CODEX 2026-08-26 (3.0 itself stays open —
      it is a standing per-domain obligation and three domains have not run
      it). All thirteen registered O*NET occupation codes and titles across
      `onet_it_occupations` and `onet_engineering_occupations` were re-read
      against the body's own current publication and match verbatim; no term
      was corrected, which is the outcome a verification is allowed to have.
      THE VERSION DID NOT SURVIVE. O*NET ships quarterly and the current
      production database is 31.0 (August 2026), superseding the 30.3 (May
      2026) release pinned at the 2026-08-09 run. Codes and titles are
      unchanged across it, so nothing shipped in any domain is wrong today —
      but a `current_version` that has quietly moved is the exact APQC
      failure mode 3b.3 named (a body reference reading as verified while its
      numbering has moved), and the reason that entry's version-pinning rule
      exists is so it is caught rather than inherited. The two entries this
      run verified are corrected to 31.0 with the verification date.
      FLAGGED FOR LEDGERX, deliberately NOT corrected here:
      `onet_accounting_occupations` carries the same stale 30.3 pin, and the
      ledgerx overlay's CC BY attribution names "the O*NET 30.3 Database" BY
      VERSION (3b.5c) — pin and attribution must move together in one act by
      that domain, so the entry carries a flag comment instead of an edit.
      The opsx and codex overlays credit "the O*NET Database" without a
      version, so their attribution stays true across releases and the
      verified-against version is recorded separately in each overlay header.
      STILL OUTSTANDING for both domains and unclaimed anywhere: TASK-LEVEL
      verification. Every mapping in both overlays is at OCCUPATION level;
      only 11-3021.00 and 27-3042.00 ever had task statements read verbatim,
      and no note in either overlay asserts a task-statement match.
- [x] 3.1 **OPSX POPULATED AND VERIFIED.** Population authored at OpsxFactory
      `1b118c9` (the O*NET replacement, 2026-08-09) and its 3.0 verification
      at `2d3e5ad` on branch `change/omnigent-terminology-population`; both
      land via that domain PR, unmerged as of this tick. READ-BACK — what
      shipped: `terminology` covers every id the overlay declares — 9 workers,
      5 job_types, 8 stop_conditions, 6 routing classes — with 6 workers
      mapped and 3 recording `no_clean_equivalent`
      (`blast_radius_reviewer`, `change_documentation_agent`,
      `admission_packet_agent`). The crosswalk body is `onet_it_occupations`
      alone. READ-BACK — the candidate list above did NOT survive contact
      with the licences, and this task's own body is the record of what was
      expected rather than what is true: 3b.5g found `itil4` and `sfia` both
      fail the product-configuration reuse test and `cobit_2019` requires an
      ISACA licence for incorporation into software given to third parties;
      `apqc_pcf` was already barred by 3b.5b. `nist_csf` is registered
      licence-clean but its Function names were never enumerated from a
      primary source, so no function-level mapping was authorised and none
      shipped — recorded rather than guessed. The expected
      `no_clean_equivalent` pair is NOT the shipped pair: swapping the body
      moved the unmapped set, because `credential_grant_reviewer` has an
      honest counterpart in 15-1212.00 Information Security Analysts where it
      had none in a process framework. That the unmapped set moves with the
      body is the crosswalk behaving descriptively (5.2) rather than as an
      identity; worker ids, archetypes, permissions and credential tiers are
      byte-identical across the swap (5.1 held). READ-BACK — 3.0 for this
      domain: all six registered codes re-read verbatim on O*NET OnLine
      2026-08-26. FLAGGED: the O*NET Database moved 30.3 -> 31.0 (August
      2026) since the 2026-08-09 run; codes and titles are unchanged, the
      registry entry is corrected here, and the overlay now records the
      version it was verified against. Task-level verification remains
      OUTSTANDING and unclaimed — mappings are occupation-level only.
- [x] 3.2 **LEDGERX POPULATED WITH THE PROCESS LAYER, AND THE O*NET PIN
      MOVED.** Authored at LedgerxFactory `ded4a0128f9e` on branch
      `change/apqc-terminology-and-onet-pin`, landing via that domain's PR,
      unmerged as of this tick. READ-BACK — what shipped: `apqc_pcf` is back
      in the overlay as a THIRD body beside `onet_accounting_occupations`
      (unchanged, 14/14 workers) and `coso_icif` (unchanged, 5 workers), so
      the same 14 workers now carry 28 crosswalks across three bodies naming
      three different kinds of thing. PCF: 6 workers mapped
      (`invoice_coder`, `bookkeeper`, `reconciliation_specialist`,
      `close_accountant`, `tax_preparation_assistant`, `books_designer`), 3
      recording `no_clean_equivalent` (`document_intake_processor`,
      `document_fact_reader`, `posting_admission_agent`), 5 OMITTED.
      READ-BACK — the crosswalk is BOUNDED to what 3b.5b preserved, and the
      omissions are the shape of that bound rather than an oversight. Only
      9.3 (10730), 9.6 (10733) and 9.9 (10736) and their sub-elements were
      restored; every `no_clean_equivalent` note says in its own text that it
      is scoped to those three and is not a claim about thirteen categories.
      The five omitted workers have plausible PCF homes OUTSIDE the preserved
      set — 9.1 (10728) for `scenario_modeler`, 9.2 (10729) for
      `counterparty_analyst`, 9.8 (10735) for `controller_reviewer` and
      `compliance_reviewer` — and the overlay names them as such. Widening
      past the preserved set was not this act's to decide, so it did not, and
      the overlay's own OMISSION-IS-NOT-no_clean_equivalent discipline is
      what makes the difference readable. A LATER ACT MAY WIDEN IT; nothing
      here forecloses that.
      READ-BACK — 5.1 and 5.2 held: worker ids, archetypes, permissions and
      credential tiers are byte-identical across the change (the diff touches
      only the terminology block's comments and `standards_alignment`), and
      every note that names an approval, payment, posting or filing node
      names it as REFUSED — 9.6.1.4 Approve payments (10872) and 9.6.1.8
      Process payments (10876) for `invoice_coder`, 9.3.2.9 (10827) excluded
      from `close_accountant` because a node cannot be half-claimed.
      `bookkeeper` is the sharpest case and now diverges twice over: both the
      human occupation AND PCF 9.3.2.2 Process journal entries (10820)
      include posting, and the worker cannot post.
      READ-BACK — the licence condition is discharged in the artifact, not
      just in the registry: APQC's mandatory paragraph rides in the overlay
      header verbatim with its ® marks intact, and the grant's scope limit is
      honoured — names, hierarchy numbers and element IDs are quoted and NO
      process definition text is, not even paraphrased.
      FLAGGED, and it is the one thing this act could not close: PCF 8.0 is
      the pinned version, apqc.org answers HTTP 403 to automation and no 8.0
      mirror is public, so the names, numbers and IDs shipped were
      text-extracted from the primary 7.4 PDF and 8.0's NUMBERING WAS NOT
      RE-READ. The five-digit element IDs are APQC's stable identifiers and
      carry the citations; the decimal numbers are 7.4's and the overlay says
      so. This is 3b.3's failure mode held at arm's length rather than
      eliminated, and closing it needs the same browser act that closed
      3b.5d.
      READ-BACK — 3.0a's flag DISCHARGED: the ledgerx O*NET pin and its
      by-version attribution moved together as that flag required. The
      overlay's CC BY block now carries onetcenter.org's version-stamped 31.0
      wording (including "has not approved, endorsed, or tested these
      modifications") and `onet_accounting_occupations` in
      `contracts/policies/standards-bodies.yaml` moves 30.3 -> 31.0 in this
      same commit, gaining the `reuse_licence` /
      `redistribution_permitted_in_product_config` / `attribution_required`
      triple the opsx and codex entries already carried. Every SOC code is
      unchanged across the release, so no mapping shifted. Task-level
      verification remains OUTSTANDING and unclaimed here as everywhere.
      ORIGINAL TASK TEXT (2026-08-09, with its 2026-08-26 corrections) kept
      below, because the read-back is only checkable against what was asked:
      Populate `terminology` in LedgerxFactory. Candidate bodies:
      `apqc_pcf` 8.0 (processes — 9.6 AP, 9.3 general accounting, 9.9 taxes; the 8.x numbering originally written here was the legacy finance layout, per the correction note below),
      `coso_icif` (controls — the natural home for the segregation-of-duties
      boundary), `ima_mac` (competencies), `aicpa` (standards/competencies).
      NOT GAAP/IFRS: those are REPORTING standards governing what the books
      say, not what a worker is — ledgerx's reporting-standard grounding
      already lives in the subject books-design layer.
      TWO CORRECTIONS TO THE CANDIDATE LIST ABOVE, which is 2026-08-09 text:
      the PCF numbers in it are the wrong-for-every-version ones 3b.5b
      caught — use 9.3 general accounting, 9.6 AP and 9.9 taxes with their
      element IDs. And the licence bar that pulled PCF out is lifted (3b.5k,
      3b.5d): `apqc_pcf` may ship again, carrying APQC's attribution
      paragraph verbatim, alongside `onet_accounting_occupations` rather than
      instead of it — process-level and role-level are different claims. The
      stale O*NET 30.3 pin and the by-version attribution in the ledgerx
      overlay move in this same act (3.0a).
- [x] 3.3 **ADX POPULATED, AND ITS BRIEF FINALLY RUN.** Authored at
      AdxFactory `02d022cefb34` on branch `change/terminology-population`,
      landing via that domain's PR, unmerged as of this tick. READ-BACK —
      what shipped: all 10 workers now carry a crosswalk where 3 did before,
      against THREE bodies — `onet_marketing_occupations` (new, 10 entries: 5
      mapped, 5 `no_clean_equivalent`), `apqc_pcf` (new, 10 entries: 6
      mapped, 4 `no_clean_equivalent`) and `iab` (3 entries, carried forward
      unchanged). `job_types`, `stop_conditions` and `routing` labels are
      untouched. The seven workers that carried display labels only now carry
      at least one crosswalk each.
      READ-BACK — THIS DOMAIN IS WHERE THE MULTI-BODY DESIGN (2.2b) PAYS FOR
      ITSELF, and it is worth recording because the other four domains
      shipped a single body and could not demonstrate it. The two workers
      with NO honest occupation have clean PROCESS homes: `media_planner` ->
      3.2.3.4 Select channels for target segments (10128) with 3.2.5.6
      (16854); `lifecycle_marketer` -> 3.2.6 Design and manage customer
      loyalty program (18924) with 3.3.6.4 (16616). A single-body crosswalk
      would have written both off as unmappable. The reverse case is
      `compliance_reviewer`: a clean occupation (13-1041.00 with 13-1041.07)
      and no home inside PCF category 3.0 — and its note NAMES 11.0 as the
      real home rather than implying none exists.
      READ-BACK — the registry's recorded gaps were RE-TESTED, not inherited,
      which is the whole point of 3.0. The entry records "O*NET has no title
      match for 'media planner' or 'media buyer'"; this act read 11-2011.00
      Advertising and Promotions Managers directly and confirmed none of its
      ten Reported Job Titles is either, and read 13-1161.00 for
      `lifecycle_marketer` and found nothing lifecycle, retention, CRM or
      email. BOTH RESOLVED TO `no_clean_equivalent` RATHER THAN A PARTIAL:
      the schema expresses partiality only as a mapping string plus a note,
      and using one here would have named a manager occupation carrying
      media-buying and budget authority these workers must never appear to
      hold. 27-1011.00 Art Directors lists "Creative Director" as a verbatim
      Reported Job Title, which is what makes that mapping clean rather than
      approximate.
      READ-BACK — 3b.5e's adx brief RAN, seventeen days after it was written,
      and it found what it predicted. Two findings, both recorded in the
      overlay and NEITHER acted on, because both are registry decisions this
      task does not own: (1) the Audience Taxonomy page names IAB TECH LAB as
      steward throughout, not the Interactive Advertising Bureau the registry
      names — the brief asked whether `iab` should split the way CICPA and
      AICPA did, and on this evidence it should; (2) THE REUSE TEST WAS NEVER
      RUN ON IAB — its taxonomy page publishes no licence text and no licence
      link, so the one body in this overlay that predates the licence
      discipline is the one body still shipping on an assumption. Current
      version read: Audience Taxonomy 1.1 (October 2020). The three IAB
      mappings are carried forward MARKED PROVISIONAL, and the OpenRTB
      citation for `media_planner` is narrowed in place rather than removed:
      a bidding protocol names the plumbing a plan executes through, not the
      planning work — the brief's own QUESTION THREE, answered.
      READ-BACK — 5.1 and 5.2 held: no worker id, archetype, permission or
      credential tier changed, and every occupation or node carrying the
      launch/spend act is named as refused (3.3.4.5 Execute promotional
      activities (10169) for `creative_director`; 3.3.2 Establish marketing
      budgets (10149) for `campaign_strategist`; 3.2.6.2 (18925) for
      `lifecycle_marketer`).
      SAME FLAG AS 3.2, same cause: PCF element names, numbers and IDs were
      text-extracted from the primary 7.4 PDF because 8.0 is unreachable to
      automation, so 8.0's numbering was not re-read. This act DID close half
      of the old adx note's open question — 3.0 Market and Sell Products and
      Services (10004) is confirmed against a primary source as 7.4's number,
      superseding the 7.0.5 pin that note carried — and left the other half
      open honestly. Task-level verification remains OUTSTANDING.
      ORIGINAL TASK TEXT (2026-08-09, with its 2026-08-26 prerequisite note)
      kept below, because the read-back is only checkable against what was
      asked:
      Populate `terminology` in AdxFactory. Candidate bodies:
      `apqc_pcf` 3.0 (processes), `iab` (ad-tech specs/taxonomies — fits the
      media and audience classes, not the creative or compliance ones),
      `cim` (competencies), `ama_marketing` (concept definitions).
      PREREQUISITE LANDED 2026-08-26, task still open: adx had no role-level
      body registered at all — three of its ten worker classes carry an IAB
      crosswalk and seven carry display labels only — so
      `onet_marketing_occupations` is now registered in
      `contracts/policies/standards-bodies.yaml` (O*NET 31.0, CC BY 4.0,
      spanning SOC families 11-0000, 13-0000, 15-0000 and 27-0000 rather than
      one, which is why its `source_url` is the database page and not a
      family listing). Six occupation codes are recorded on the entry with
      the gaps named — O*NET has no title match for "media planner" or "media
      buyer" — but WHICH adx worker maps to WHICH code is this task's act and
      nothing here asserts it. The `apqc_pcf` bar is also lifted (3b.5k), so
      the process-level layer is available beside the role-level one. The adx
      marketing brief (`supporting-docs/marketing-bodies-research-prompt.md`
      in AdxFactory) is written but has still never been run; it is the
      natural vehicle for this task.
- [x] 3.4 **CODEX POPULATED AND VERIFIED.** Population authored at
      codexFactory `54ccc9b` (2026-08-09, from scratch — codex had no
      terminology block at all) and its 3.0 verification at `d5f5f3c` on
      branch `change/omnigent-terminology-population`; both land via that
      domain PR, unmerged as of this tick. READ-BACK — what shipped:
      `terminology` covers every id the overlay declares — 11 workers, 12
      job_types, 6 stop_conditions, 6 routing classes — with 8 workers mapped
      and 3 recording `no_clean_equivalent` (`pr_admission_agent`,
      `merge_readiness_agent`, `scrum_master_worker`). The crosswalk body is
      `onet_engineering_occupations` alone. READ-BACK — none of the candidate
      bodies above shipped, and 3b.5h is the record of why: `swebok` needs
      IEEE permission for commercial republication, `sfia` was already
      prohibited outright by the opsx round, `iso_iec_ieee_12207` is sold by
      ISO, and `apqc_pcf` was barred by 3b.5b. The Scrum Guide's CC BY-SA
      question was answered and DECLINED — bare role names are very likely
      outside copyright, but share-alike could oblige this configuration to
      be CC BY-SA if definitional text were reproduced, which is asymmetric
      risk for a label we can write ourselves. `scrum_master_worker` is the
      sharpest 5.1/5.2 case in the family and is handled twice over: it is
      deliberately unmapped AND its display label avoids the term, because
      "Scrum Master" names a human role holding facilitation authority over
      PEOPLE. READ-BACK — 3.0 for this domain: all seven registered codes
      re-read verbatim 2026-08-26 (27-3042.00 on its own summary page, the
      rest on the family listing). FLAGGED: the same 30.3 -> 31.0 version
      move as 3.1, corrected in the registry entry here and recorded in the
      overlay. Task-level verification remains OUTSTANDING and unclaimed.
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
- [x] 3b.5d DISCHARGED 2026-08-26 — no written confirmation is needed,
      because APQC already published one. The PCF's own PDF carries, on page
      2, a perpetual, worldwide, royalty-free grant to use, copy, publish,
      modify and create derivative works of the PCF, conditional on one
      attribution paragraph reproduced verbatim. Brett downloaded PCF 8.0 —
      the pinned version — and read that page in a browser on 2026-08-26,
      confirming the grant and the paragraph are present; that act is what
      this task was actually waiting on, and 3b.5k is its record. PCF element
      names and numbers MAY ship in product configuration provided the
      attribution paragraph rides with them. Closed by a published licence,
      not by correspondence. NOT discharged by this: process DEFINITIONS,
      which ship in separate APQC documents whose front matter has not been
      read.
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
- [x] 3b.5k APQC VERDICT CORRECTED 2026-08-26 — the bar came off the wrong
      document. WHAT WAS RE-TESTED: the PCF's own licence page, which is page
      2 of the PCF PDF under the heading COPYRIGHT AND ATTRIBUTION and is not
      anything on apqc.org. It carries a self-contained grant — "APQC hereby
      grants you a perpetual, worldwide, royalty-free license to use, copy,
      publish, modify, and create derivative works of the PCF" — conditional
      on one mandatory attribution paragraph carried verbatim. The paragraph
      was text-extracted from three independently hosted primary PDFs (7.4,
      7.3.1, 7.3.0) and appears in APQC-hosted 7.2.1 industry PDFs, so it is
      APQC's standard licence page rather than a one-version quirk. PCF 8.0,
      the pinned version, is unreachable to automation (apqc.org answers HTTP
      403 to every fetch and no 8.0 mirror is public), so BRETT DOWNLOADED
      PCF 8.0 AND READ PAGE 2 IN A BROWSER on 2026-08-26 and confirmed the
      grant and the paragraph are present. That act is the 8.0 record; the
      7.4 mirrors are the machine-verifiable copies. Both provenances are
      recorded on the registry entry.
      WHY THE 2026-08-09 VERDICT DIFFERED: it read apqc.org's site Terms of
      Service, which govern that portal's Online Resources ("shall not be
      publicly distributed or displayed, reproduced, published, licensed,
      transferred, sold, or incorporated in derivative works without the
      express written permission of APQC"), and never the licence printed
      inside the artifact. APQC was also never run through the
      product-configuration reuse test itself: it was barred earlier, at
      3b.5b, and that verdict was inherited as already-settled by 3b.5g,
      3b.5h and 3b.5j. The one body judged on a site ToS is the one body the
      test never saw.
      3b.5b IS SUPERSEDED, NOT REWRITTEN. It and the ledgerx report
      `usa-accounting-bodies-research-report.md` are record-class evidence
      with a 2026-08-09 evidence cutoff; they stay exactly as written and
      this task is the correction. 3b.5b's OTHER finding is untouched and
      still stands: the 8.x finance numbering shipped in those overlays was
      wrong for every version, so the re-added references must be the
      corrected ones 3b.5b preserved (9.3 general accounting, 9.6 AP, 9.9
      taxes, with their element IDs).
      3b.5j NARROWS FROM NINE TO EIGHT. "Every commercially stewarded body
      assessed fails the product-configuration reuse test" becomes eight of
      nine. The other eight bars stand unchanged, each tested against its own
      licence text: SFIA, ITIL 4, COBIT 2019, SWEBOK v4, ISO/IEC/IEEE 12207,
      GRADE, SNOMED CT, and the declined CC BY-SA Scrum Guide. What weakens
      is the escalation to "a finding about the approach, not four
      coincidences" — its founding data point was the one body judged on the
      wrong document.
      SCOPE LIMIT, recorded rather than assumed: the grant is over "the PCF",
      the document holding element names, hierarchy numbers and five-digit
      element IDs. Process DEFINITIONS ship in separate "Process Definitions
      and Key Measures" documents whose front matter has not been read, so
      nothing here authorises embedding definition text.
      APPLIED HERE: `apqc_pcf` in `contracts/policies/standards-bodies.yaml`
      now carries the grant as `reuse_licence`,
      `redistribution_permitted_in_product_config: yes_with_conditions` with
      the attribution condition, the mandatory paragraph verbatim with its
      registered marks intact, and the licence-page provenance; the
      superseded ToS-based bar in the section header above it is marked
      superseded in place rather than deleted. NOT APPLIED: 3.2 and 3.3 stay
      open. Re-adding PCF to the ledgerx and adx overlays is each domain's
      own act in its own repo.
- [x] 3b.5l IAB REUSE TEST RUN 2026-08-26, AND THE ENTRY REGISTERED. This
      discharges BOTH body-level findings 3.3 recorded as flagged-not-acted —
      the two the adx overlay header carried and this change kept open as
      "registry decisions this task does not own". Ruled by Brett
      2026-08-26: investigate the licence first, register afterward on
      evidence. The investigation ran on primary sources by the same method
      3b.5k used on APQC — hunt the ARTIFACTS for their own embedded grant,
      not the site terms.
      VERDICT: **CC BY 3.0, `yes_with_conditions`.** The taxonomies ARE usable
      in shipped product configuration, with attribution. Finding (2), "the
      reuse test was never run and its taxonomy page publishes no licence
      text", was a FALSE NEGATIVE and is now reversed — the landing pages
      genuinely publish none, which is why the earlier round was right about
      the page and wrong about the body. The grant lives one hop away, on the
      artifacts: page 2 of the Content Taxonomy 3.0 Implementation Guide PDF
      names the TAXONOMY as the licensed work ("Content Taxonomy by the IAB
      Tech Lab's Taxonomy Working Group is licensed under a Creative Commons
      Attribution 3.0 License"), and the Taxonomies repo README carries the
      same grant, corroborated verbatim by an independent mirror. The site
      ToU's all-caps redistribution ban does not govern, because the ToU
      itself defers to any "Separate License" — which CC BY 3.0 is.
      Finding (1), the STEWARD, is CONFIRMED and corrected: IAB Technology
      Laboratory, Inc. is a separate 501(c)(6) (EIN 47-3384874, New York,
      established 2015) from the Interactive Advertising Bureau trade
      association the entry named. The `iab` id is KEPT rather than split the
      way CICPA and AICPA were — the AdxFactory overlay resolves against it,
      and only `steward`, `name` and `scope` move.
      APPLIED HERE: `iab` in `contracts/policies/standards-bodies.yaml` now
      carries the corrected steward, the grant quoted verbatim as
      `reuse_licence` with its `licence_page` provenance,
      `redistribution_permitted_in_product_config: yes_with_conditions` with
      the CC BY §4(a)/§4(b) conditions as `attribution_required`, and version
      pins. It is the second body in this registry to pass the reuse test on
      a grant printed inside the artifact rather than published as a page,
      after APQC — which is now a pattern worth reading as one, not a
      coincidence: 3b.5j's "every commercially stewarded body fails" NARROWS
      AGAIN, from eight of nine to eight of ten.
      GAPS PRESERVED, NOT RESOLVED, because a registration that quietly
      launders them is worse than none: (a) the best-scoped grant sits on a
      PDF cover-stamped "Released for Public Comment" and no final-stamped
      taxonomy artifact carrying the same block was found; (b) only Content
      Taxonomy is named by that grant — Audience and Ad Product coverage
      rests on the README's blanket "applicable taxonomies" wording plus the
      ToU deferral, sound but one notch weaker; (c) TWO OF THREE VERSION
      DATES ARE CONTESTED between the steward's own surfaces (Audience
      Taxonomy 1.1: standards page October 2020 vs the steward's own XLSX
      upload path 2020/07; Ad Product Taxonomy 2.0: GitHub release
      AP2-202310 published 2023-10-18 vs standards page November 2024) and
      the entry records BOTH readings on each, resolving neither in either
      direction; (d) there is no LICENSE file and the .tsv files carry no
      notice, so licence scanners will read the repo as unlicensed and
      attribution cannot be inherited — it must be authored into every
      consuming overlay; (e) the IPR Policy PDF is gated behind an
      acknowledgment form and was NOT read, assessed non-blocking because it
      is scoped to Submissions by MEMBERS.
      NOT APPLIED, and deliberately: the outward-facing follow-up — asking
      IAB Tech Lab in a public issue to fix the README's stale "OpenRTB
      Specification" sentence and add a LICENSE file — is recorded on the
      registry entry and held on Brett's desk rather than done here. Promoting
      the three adx crosswalks from PROVISIONAL and authoring the CC BY
      attribution into that overlay is AdxFactory's own act in its own repo,
      landing alongside this.
- [x] 3b.5f Apply the results of the remaining brief (ledgerx UN/CEFACT +
      BIAN, and the adx marketing round) as they return. (ledgerx
      UN/CEFACT+BIAN, adx marketing, opsx, codex, medx) as they return.
      CLOSED 2026-08-26. The ledgerx UN/CEFACT + BIAN round — the last of
      the five this task tracked — was RUN on 2026-08-26 against live
      primary sources, on Brett's in-session ruling that it still runs
      despite its premise having lapsed. Report:
      `research/ledgerx-international-process-bodies-research-report.md`,
      the sibling of the opsx/codex/medx reports that the adx round never
      got. The brief itself stays in LedgerxFactory rather than being copied
      here; it is record-class evidence in its own repo.
      THE RULING, recorded because it changed what was asked: 3b.5k had
      already lifted the APQC bar and 3.2 had already put PCF 8.0 back, so
      the gap the brief was written to fill was closed before it ran. Brett
      ruled run it anyway, against the narrowed question this task's body
      states — whether either body adds INTERNATIONAL PROCESS vocabulary
      BEYOND cross-industry PCF 8.0. A widening question, not gap-filling.
      OUTCOME — NEITHER ADOPTED, and the decisive ground is category, not
      licence. UN/CEFACT names DATA: its finance ontology module declares
      five OWL classes (FinanceAgreement, Payment, Account, Insurance,
      PaymentMeans) plus properties, the whole seven-domain vocabulary is
      classes/properties/SKOS code lists, and the Cross Industry Invoice is
      an invoice document schema. It adds zero process vocabulary, so it
      cannot add process vocabulary beyond PCF. BIAN names a bank's own
      SERVICES: Service Domains are capability partitions, and the brief's
      domain-fit prior is CONFIRMED rather than refuted in BIAN's own words
      — Financial Accounting "lives in the accounting world of the bank",
      Accounts Receivable handles "invoices issue [sic] by the bank", Regulatory
      Reporting meets "the bank's" obligations. ledgerx keeps books FOR
      CLIENT COMPANIES. Fourteen of fourteen workers record no honest
      counterpart against each body.
      NO ADOPTION FOLLOW-UP IS FLAGGED. This closes fully: no registry entry
      is proposed, `contracts/policies/standards-bodies.yaml` is untouched,
      and the ledgerx overlay is untouched. The scope rule that would have
      deferred an adoption to a separate act never triggered.
      TWO LICENCE FINDINGS KEPT ANYWAY, because they are true and cost the
      work to establish. BIAN: `github.com/bian-official/public` carries a
      root LICENSE containing verbatim Apache-2.0 over 259 release-14.0.0
      Service Domain specifications, so BIAN Service Domain NAMES at the
      current release are lawfully embeddable — the APQC lesson running the
      other way, since bian.org itself says only "© 2026 BIAN. All rights
      reserved." The Service Landscape HIERARCHY at 14.0 is not in any
      Apache-2.0 artefact; the hierarchy that is Apache-2.0 sits in
      `bian-official/artefacts`, last committed 2021-10-06, ~six releases
      stale. UN/CEFACT: CONTRADICTORY AT PRIMARY SOURCE and unresolved.
      `vocabulary.uncefact.org/terms` — the licence page of the site that
      serves BSP element names — grants use "for the User's personal,
      non-commercial use, without any right to resell or redistribute them
      or to compile or create derivative works therefrom", while five
      UNECE-operated deliverable sites footer "All UN/CEFACT standards are
      free to use under CC By 4.0 license" with no deed, no attribution
      formula, and no LICENSE file anywhere in the UN-hosted source repo.
      The UN/CEFACT IPR Policy that would settle it is unreachable —
      unece.org answers HTTP 403 to every automated fetch — so a human must
      read it in a browser before any UN/CEFACT term is embedded for any
      purpose. Recorded as a gap, not guessed.
      AND THE MOTIVATION ITSELF LAPSED: the international-reach argument was
      an artefact of the removed premise. PCF 8.0 is registered
      `jurisdiction: international` and APQC's own mandatory attribution
      paragraph scopes it "regardless of industry, size, or geography".
      STATE AS OF 2026-08-26, counted rather than assumed. All FIVE briefs
      this task tracks have now been run and applied: opsx (3b.5g), codex
      (3b.5h), medx (3b.5i), adx marketing (run and applied in 3.3), and —
      as of the later 2026-08-26 tick below — **ledgerx UN/CEFACT+BIAN**. Its findings landed in two places and neither is a
      report file: the crosswalks themselves went into AdxFactory
      `02d022cefb34`, and its two body-level findings (the IAB steward is
      IAB Tech Lab, not the trade association; IAB's taxonomy page publishes
      no licence text, so the reuse test was never run on it) are recorded in
      that overlay's header as flagged-not-acted, because both are registry
      decisions. NO REPORT FILE WAS WRITTEN for the adx round — the prompt at
      AdxFactory
      `openspec/changes/adopt-neutral-omnigent-overlay/supporting-docs/marketing-bodies-research-prompt.md`
      still has no sibling report, unlike opsx/codex/medx which have one each
      under `research/` here. That asymmetry is a real gap in the evidence
      trail and is named rather than glossed.
      WHAT THIS TASK STILL OWES: the ledgerx UN/CEFACT + BIAN round, and
      only that. Its brief is written and has NEVER been run — LedgerxFactory
      `openspec/changes/adopt-neutral-omnigent-overlay/supporting-docs/apqc-replacement-candidates-verification-prompt.md`,
      `Status: record`, prepared 2026-08-09, with no report anywhere in that
      repo.
      ITS PREMISE HAS CHANGED, which is the honest thing to say about it. The
      brief exists to fill "a **process-layer gap** over the operational
      accounting workers" that APQC's removal opened, ideally with the
      international reach O*NET lacks. 3b.5k lifted that removal and 3.2 put
      the process layer back, so the gap the brief was commissioned to fill
      is closed. What survives is narrower and optional: whether UN/CEFACT or
      BIAN adds international process vocabulary BEYOND cross-industry PCF,
      which is a widening question rather than a gap-filling one. Running it
      is still worthwhile; treating it as a blocking dependency would be
      false, and leaving it unmarked would let it read as pending for a
      reason that no longer holds.

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
