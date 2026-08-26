# Research prompt: clinical terminology for medical WORK — expect mostly "no equivalent"

Status: record
Prepared: 2026-08-09 for a live-research AI (current web access required).
Serves: task 3b.5e. Results feed this registry and the MedxFactory overlay
(`xFactories/MedxFactory/omnigent/domain-overlay.yaml`).

Why, and read this before starting: medx has **no terminology block**, and
we expect this to be the domain where the honest answer is largely **"no
clean equivalent."** The medical worker classes are *reasoning agents* —
case framing, hypothesis generation, skepticism, safety challenge — while
every major clinical taxonomy we know of describes either **humans holding
clinical standing** (provider roles) or **clinical content** (findings,
procedures, labs). Neither is what these workers are. A brief that comes
back saying "register almost nothing" would be a good result, not a failed
errand.

---

## PROMPT (copy from here down)

Assess whether any authoritative body publishes a taxonomy that can honestly
name **medical reasoning WORK**, for an agent system that needs to display
internal worker-role names in terminology a clinician recognizes.

### QUESTION ZERO — the safety question that outranks the others

These workers are **artifact-only and hypothesis-only**. None diagnoses,
orders, prescribes, signs, writes the chart, or issues a clinical
conclusion. The terminal action belongs to the **clinician of record** and
the chart/CPOE signing path.

Provider taxonomies — **NUCC Health Care Provider Taxonomy**, **HL7 FHIR
PractitionerRole** and similar — describe humans who hold **clinical
standing and legal accountability**. Labelling a reasoning agent with a
provider role would imply standing it must never appear to have, in the one
domain where that misrepresentation could contribute to patient harm.

So: for every proposed mapping, state explicitly whether it risks implying
clinical standing, and prefer `no_clean_equivalent` whenever it does. We
would rather have no label than a dangerous one.

### QUESTION ONE — reuse rights

Not "is it free to obtain." This:

> May we embed the body's **element names and identifiers** verbatim inside a
> YAML configuration file shipped in a **publicly readable product
> repository** distributed to third parties, without a negotiated licence?

Clinical terminologies have unusually complex licensing, so be precise:

- **SNOMED CT** — licensing differs by country (member territories via a
  National Release Centre vs an Affiliate Licence elsewhere). Establish what
  applies to a commercial product distributed internationally, and whether
  citing a handful of concept names is treated differently from
  redistributing the terminology.
- **LOINC**, **ICD-10 / ICD-11**, **CPT** — CPT in particular is AMA
  copyright with fees. State which are usable and which are not.
- **NUCC taxonomy** and **HL7 FHIR** value sets — licence and attribution.

### QUESTION TWO — is there anything that names the WORK?

Our registered bodies name provider roles or clinical content. What we would
need is a taxonomy of **clinical reasoning activity** — differential
generation, evidence appraisal, base-rate reasoning, test-utility analysis,
safety challenge, documentation drafting. Assess:

- **O\*NET** (CC BY 4.0) — licence-clean and already adopted elsewhere in
  this project. Do its healthcare occupations' *task* and *detailed work
  activity* statements describe reasoning work at a useful granularity, or
  only whole clinician jobs? Be honest if it is only the latter.
- **Clinical decision support** vocabularies (CDS Hooks, Arden Syntax,
  clinical-pathway or guideline-development frameworks such as **GRADE**).
  GRADE in particular names *evidence appraisal* activity — assess whether
  it fits `base_rate_agent`, `evidence_retrieval_agent`, or `skeptic_agent`.
- **Evidence-based-medicine methodology** bodies (Cochrane, EQUATOR/PRISMA,
  AGREE II) — do any name reasoning activities usably, and what are their
  licences?
- **Patient-safety** frameworks (WHO patient-safety taxonomy, IHI) —
  relevant to `safety_agent`?
- Anything else authoritative. If nothing fits, say so plainly.

### The worker roles

| Worker | Archetype | What it does |
|---|---|---|
| case_framing_agent | frame | Frames the case into a bounded question set |
| evidence_retrieval_agent | generate | Retrieves governed patient evidence and literature |
| dream_hypothesis_agent | generate | Generates hypotheses — permanently non-authoritative |
| base_rate_agent | verify | Base-rate and prior-probability reasoning |
| test_utility_agent | verify | Assesses diagnostic-test utility |
| simulation_agent | verify | Simulates against an immutable truth snapshot |
| data_reverification_agent | verify | Re-verifies underlying data |
| skeptic_agent | challenge | Adversarially challenges hypotheses |
| safety_agent | challenge | Challenges on safety grounds |
| draft_documentation_agent | generate | Drafts documentation — never the chart |
| convergence_packet_agent | assemble_for_admission | Assembles a packet for clinician review |

Every output is a hypothesis or a draft for a clinician; nothing is a
diagnosis, an order, or a chart entry.

### Output format

Registry-shaped YAML **only** for bodies you would actually recommend:

```yaml
- id: <lowercase_snake_id>       # existing ids include nucc_taxonomy, hl7_fhir_practitionerrole, snomed_ct
  name: <official name>
  steward: <current maintaining organization>
  jurisdiction: <international | united_states | ...>
  names: <clinical_concepts | provider_roles | reasoning_activities | competencies | other:describe>
  scope: >-
    Coverage and which of the eleven workers it honestly fits.
  current_version: <version / date>
  status: <current | superseded_by:X | under_revision>
  source_url: <primary source>
  term_list_availability: <public | paywalled | licence_required>
  reuse_licence: <exact licence or terms, with link>
  redistribution_permitted_in_product_config: <yes | yes_with_conditions | no | unclear>
  clinical_standing_risk: <none | describe the risk of implying clinical standing>
  attribution_required: <verbatim text if any>
  attribution_note: <trademark and other constraints>
  confidence: <high | medium | low>   # with reasoning
```

Then prose: a per-worker fit table for all eleven, with an explicit
`no_clean_equivalent` list and reasons; and a recommendation. **"Register
nothing new; record no_clean_equivalent for all eleven and rely on display
labels alone" is an acceptable and possibly correct recommendation.** Say so
if that is what the evidence supports.

### Ground rules

- **Patient-safety framing first.** Where a mapping is defensible but could
  imply clinical standing, recommend against it and say why.
- **Primary sources only** for licence claims; clinical terminology
  licensing is frequently misdescribed in secondary sources.
- **Do not guess codes or concept identifiers.** A gap beats a wrong
  clinical citation, and in this domain the downside is materially worse.
- Distinguish verified fact from inference; give as-of dates.
