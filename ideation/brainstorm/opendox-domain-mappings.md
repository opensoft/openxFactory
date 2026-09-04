# openDox Domain Mappings — Medx, Ledgerx, Adx, and the Common Core — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Brett's Q5 direction of 2026-09-04 asks what is COMMON to how
MedxFactory (patient management and research), LedgerxFactory (financial
simulations and accounting questions) and AdxFactory (marketing analysis) would
each map onto the workbench — this document works those three mappings
explicitly against measured domain facts and finds a common core of seven
machineries that belong in openXdox (the corpus adapter, the lifecycle engine,
the gate and commission loop, the evidence-and-provenance surface, the
derived-model model/scenario pair, the role-and-authority projection, and the
review lane), a domain-specific residue that belongs in each descendant, and one
uncomfortable finding: the common core is NOT "the openxFactory corpus reader"
but the domain-mapping machinery, and today's dashboard implements the former
almost exclusively.
Topics: opendox, openxdox, medxdox, ledgerxdox, adxdox, codexdox,
domain-mappings, governed-derived-model, workflow-gate-contract,
roles-authority-model, document-lifecycle, domain-descendant-boundary,
ideation-dashboard, common-core, feat-request
Repository context: openxFactory owns every contract the common core would be
built on (`governed-derived-model`, `workflow-gate-contract`,
`roles-authority-model`, `document-lifecycle`, `consent-instrument`,
`neutral-job-envelope`); the machinery would live in `opensoft/openXdox` and the
per-domain mapping in each `<Domainx>Dox` descendant
Captured: 2026-09-04

## Possible feats

- **The domain-mapping contract** — what a descendant must declare to map its
  domain onto the workbench: artifact kinds, their lifecycle, the acts and their
  gates, the evidence classes, the promoting authorities.
- **openXdox as a mapping engine, not a corpus reader** — the machinery is
  parameterized by a domain declaration rather than hardcoded to
  openxFactory's tree.
- **The evidence surface** — one machinery for "this claim is traced to that
  source", serving a chart citation, a ledger tie-out and an attribution model
  alike.
- **The model/scenario workbench** — a first-class surface for
  `governed-derived-model` families (a `model` member plus a `scenario` member),
  which all three domains already declare and none can currently work in a UI.
- **A descendant profile schema** — the one artifact a `<Domainx>Dox` repository
  actually contains, so "pin and profile, never fork" has something concrete to
  mean.

## The direction this document answers

> "we need to make sure openXfactory brings in the core machinery to map to
> domains. we need to think how a patient managment and research maps to the
> openXdox. and how a finacial simulations or accounting questions would map in
> ledgerXfactory. same for marketing analysis in adXfactory. what is core to
> these that we pull out and put in openXdox. and what can pull up to openDox
> that does not rely on openXfactory."
> — Brett Heap, 2026-09-04 (DIRECTION Q5, issue #656)

Three layers, then: openDox useful alone to a student or a lab assistant;
openXdox the common domain-mapping machinery; the descendant the domain-specific
mapping.

## The measured domain facts

Not invented for this document — these are the ratified per-domain
interpretations in `docs/domain-instantiation-pre-run-questionnaire.md`,
`contracts/policies/layer-vocabulary.yaml` and `docs/governed-derived-model.md`.

| | MedxFactory | LedgerxFactory | AdxFactory | codexFactory |
| --- | --- | --- | --- | --- |
| Subject layer | Patient Hermes | Engagement Hermes | Advertiser Hermes | Project Hermes |
| Tenant layer | Care Organization Hermes | Firm Hermes | Marketing Organization Hermes | Engineering Organization Hermes |
| Domain objects | patient and care context | ledger, filing, report, transaction, obligation | campaign, audience, offer, channel, account | feature, repo, PR, release, incident |
| Sensitive acts | care-affecting action, patient privacy, clinical authority | money movement, filing accuracy, audit, compliance | brand risk, external send, paid spend, privacy, attribution | merge, deploy, data exposure, production impact |
| Derived-model family | Dream Object / Simulation Scenario (**ratified templates**, conforms at `governed`) | Counterparty Health Profile / Financial Scenario (staged) | Persona / Campaign Simulation (staged, conforms at `calibrated`) | — |
| Truth store the model may never write | patient truth model | the ledger | brand truth | the repository |

## Mapping 1 — MedxFactory: patient management and research

**The artifacts.** Clinical notes and case documents; care plans; research
protocols and their amendments; literature and evidence summaries; synthetic
library cases; the Dream Object and its Simulation Scenarios; consent
instruments.

**The lifecycle.** A clinical note is drafted, attested by a clinician, filed to
the chart, and thereafter immutable-with-addenda. A research protocol is
drafted, reviewed, approved by a board, amended by a versioned act. Both are
recognizably the openxFactory lifecycle with different words: a controlled
status vocabulary, a transition that requires an authority, and a record that
becomes immutable at a point.

**The acts and gates.** Care-affecting action gates on clinical authority. A
chart write gates on the clinician of record. Any cross-subject data movement
gates on `scope`/`isolation_boundary` review. External enforcement is the
clinical chart (openChart, through MedxChart), which is the analogue of branch
protection: the place where a governed decision becomes real and where an
ungoverned one is refused.

**The evidence.** Every derived assessment is evidence-traced to a source
document or declared as an assumption in a register. The `governed` tier's
invariant 2 is literally that. In research this is a citation; in care it is the
note the assessment reads.

**Research analysis is the part that most resembles openDox.** A lab assistant
reading twenty papers, clustering them by topic, asking a model to summarize
them, keeping a notebook, drafting a protocol — that is the openDox product with
no domain machinery at all. This is the single strongest confirmation of Brett's
"a student could use openDox" test: the research half of MedxFactory's own
mapping is mostly the neutral product.

## Mapping 2 — LedgerxFactory: financial simulations and accounting questions

**The artifacts.** Ledger entries and journals; filings and their supporting
workpapers; close packages; engagement letters; accounting-question memoranda
(a question, the authority consulted, the conclusion, the reasoning);
Counterparty Health Profiles; Financial Scenarios.

**The lifecycle.** An accounting question is raised, researched against
standards, answered with a cited conclusion, reviewed by a licensed
professional, and filed as a position the firm will defend. That is a
document lifecycle with a hard authority gate at the end — the closest
structural analogue in this whole comparison to an OpenSpec change's
ratification, and the reason `standards-body-registry` exists in openxFactory.

**The acts and gates.** Money movement gates on segregation of duties — this
domain has an actual promoted posting-SoD requirement and a distinct-holder
constraint enforced by wallets. Filing gates on professional licensure. Audit
gates on the immutability of the record. External enforcement is the ledger
itself.

**The evidence.** A tie-out: a number in a report traces to a journal entry
traces to a source document. Provenance here is not documentation hygiene, it is
the audit trail, and the failure mode is legal.

**Financial simulations are the model/scenario pair, exactly.** A Financial
Scenario exercises a Counterparty Health Profile and emits a hypothesis, never a
posting; invariant 5's output enum
(`hypothesis_proposed | no_signal | discarded`) is a perfect fit for "what if
this counterparty defaults". Ledgerx is the domain where the derived-model
machinery is most obviously a WORKBENCH need rather than a contract need — a
human wants to run the scenario, see the assumptions, and decide.

## Mapping 3 — AdxFactory: marketing analysis

**The artifacts.** Campaign briefs; audience and persona definitions; offers and
creative; channel plans; attribution analyses; Campaign Simulations; the brand
truth document.

**The lifecycle.** A brief is drafted, reviewed for brand risk, approved for
spend, launched, measured, and retired. The measurement step is what makes this
domain different: the lifecycle does not end at approval, it loops through
observed outcome back into the model. That is why Adx conforms at the
`calibrated` tier and Medx at `governed` — a calibration-writer workflow records
predicted-versus-actual, `confidence` is derived from calibration history and
never hand-set, and repeated refutation downgrades confidence and flags
re-modeling.

**The acts and gates.** External send gates on approval (an email to a real
audience is irreversible). Paid spend gates on a budget authority. Privacy gates
on `person_modeling` — Adx is the domain where `identified_persons_under_policy`
is a live setting and a domain policy document is a validator-checked
precondition. External enforcement is the ad platform.

**The evidence.** Attribution: a result traced to a channel traced to a spend.
Structurally the same tie-out Ledgerx needs, over different nouns, with a
statistical confidence Ledgerx does not have.

**Marketing analysis is the analysis half of openDox with a feedback loop.**
Clustering, summarizing, comparing, drafting — plus one thing openDox does not
have and arguably should not: the calibration loop that reads outcomes back.

## The common core — what belongs in openXdox

Seven machineries appear in all three mappings with the nouns changed and
nothing else:

1. **The corpus adapter implementation.** Each domain has documents somewhere —
   a chart, a firm's document store, a campaign repository — that must be
   listed, read, written back and checked. openDox declares the interface (Q4,
   ruled); openXdox implements the governed-corpus flavour of it; a descendant
   points it at the domain's actual store.
2. **The lifecycle engine.** A controlled status vocabulary, legal transitions,
   the authority each transition requires, and the point at which a record
   becomes immutable-with-addenda. All three domains have one. Only the WORDS
   differ, which is exactly what makes it parameterizable rather than
   hardcoded — and today it is hardcoded to a nine-word openxFactory taxonomy.
3. **The gate and commission loop.** Record the intent, name the human, gate on
   an authority, dispatch a fulfilment, land the change through external
   enforcement. `workflow-gate-contract` plus the `workflow-job` descriptor plus
   the gate-action record already generalize this; the dashboard's gate console
   is the only UI for it that exists.
4. **The evidence-and-provenance surface.** A claim, its traced sources, and a
   register of declared assumptions — a chart citation, a ledger tie-out and an
   attribution chain are one machinery. `governed-derived-model` invariant 2 is
   the contract; nothing renders it.
5. **The model/scenario workbench.** A `model` member and a `scenario` member, a
   scope and an isolation boundary, a truth store the model may never write,
   an output confined to `hypothesis_proposed | no_signal | discarded`, and a
   named human promoting authority. All three domains declare a family. None can
   work one in a UI today. **This is the largest genuinely missing piece of
   openXdox and it is not in the current 80K lines at all.**
6. **The role-and-authority projection.** Who may act, on what object, in which
   scope — clinician of record, licensed professional, launch approver. The
   contracts exist (`roles-authority-model`, the wallet-carried authority work);
   the workbench shows a per-serve console token and a loopback verdict.
7. **The review lane.** A substantive review with a named reviewer, a recorded
   verdict, and a merge that cannot clear without it. codexFactory has the only
   realized instance; every domain needs one.

Notice what is NOT on that list: reading `ideation/staging/`, parsing
`## ADDED Requirements`, running doc-health's twenty-three check families,
rendering the OpenSpec promotion funnel. Those are **codexFactory's mapping**,
not the common core — and they are approximately all of what the current reader
does.

## The uncomfortable finding

**Today's "integration layer" is a descendant, not a core.** The 15K lines this
packet's boundary document assigned to openXdox are almost entirely
openxFactory-and-OpenSpec-specific: the lifecycle taxonomy, the promotion
funnel, the change/spec/delta vocabulary, doc-health's families, the three lanes
that thaw a git corpus. Under Brett's three-layer test that content is the
`codexDox` mapping — openxFactory's own domain is software engineering, and its
corpus is the engineering domain's artifact store.

Which means the honest three-column assignment is not "app versus integration".
It is:

- **openDox** — the app, and more of it than the first cut assumed.
- **openXdox** — the seven machineries above, **most of which do not exist yet**,
  parameterized by a domain declaration.
- **codexDox** — most of what the first cut called openXdox.

That is a much bigger claim than the ruling made and it should be held as a
hypothesis, not a plan. It is recorded here because the alternative — building
openXdox as a rename of the current reader — would produce a layer that
MedxFactory and LedgerxFactory cannot use, which is precisely the failure the
direction was given to avoid.

## Contradiction, kept

- **The finding above contradicts this packet's own boundary document**, which
  assigns the projection, gates, lanes and lens to openXdox. Both readings are
  live: the boundary document's cut is what an extraction of TODAY's code would
  produce, and this document's cut is what the three-layer test implies. They
  disagree about roughly 15K lines.
- **It also contradicts the ruling's own framing** that openXdox is "openDox
  tuned for use with openXfactory". If openXdox is the domain-mapping core, then
  the openxFactory tuning is `codexDox`. If openXdox is the openxFactory tuning,
  then the domain-mapping core has no home and each descendant reinvents it.
  Brett's Q5 direction says "openXfactory brings in the core machinery to map to
  domains", which reads as the first — but the layer is named for the second.
  This is a naming tension worth surfacing before a repository is created.
- **Or the tension dissolves:** openxFactory IS the neutral layer, not a domain,
  and its corpus vocabulary (change, spec, delta, requirement) is genuinely
  neutral governance rather than engineering-specific. Under that reading the
  current reader IS the common core and Medx/Ledgerx/Adx map onto `ADDED
  Requirements` and `Status: ratified` as readily as codex does. This is the
  cheapest reading and it may be right; it deserves a real test rather than an
  assumption, and the test is whether a clinician would ever see the word
  "requirement".
