# Research report: clinical bodies — verified 2026-08-09

Run against live primary sources, answering
`medx-clinical-bodies-research-prompt.md`.

## Executive conclusion

**Register nothing. Record `no_clean_equivalent` for all eleven workers.
Rely on display labels alone.** The brief said that outcome was acceptable
and possibly correct; the evidence supports it.

Medx is the only domain that fails on **both** axes. The other four failed
on licensing while a category fit existed. Here neither holds.

**Category failure.** Every major clinical taxonomy names one of two things,
and these workers are neither:

- **Humans with clinical standing** — NUCC provider taxonomy, HL7 FHIR
  PractitionerRole, O*NET healthcare occupations.
- **Clinical content** — SNOMED CT, LOINC, ICD, CPT.

The medx workers are reasoning agents producing hypotheses and challenges
*for a clinician to act on*. Nothing examined names clinical reasoning work
at that granularity.

**Licence failure, including the one good candidate.** GRADE is the
certainty-of-evidence framework adopted by Cochrane, WHO, NICE and 110+
organisations, and it genuinely names *appraisal activity* — the closest
category fit found anywhere. It is published **CC BY-NC-ND 4.0**:
NonCommercial excludes our use, NoDerivs excludes adaptation. Doubly barred.

SNOMED CT requires a vendor **Affiliate Licence**: organisations distributing
products that include or access SNOMED CT must be Affiliates, with fees in
non-member territories by World Bank Territory Band, annual renewal, and
sub-licensing and reporting obligations.

No licence-clean clinical-reasoning competency framework was found. AMIA and
national clinical-informatics frameworks exist but describe human
informatics practitioners, and their reuse terms were not established.

## What was done instead

Display labels for all eleven workers, six job types, nine stop conditions
and seven routing classes — the readability goal met without a crosswalk.

Plus **one machine-readable safety statement**: every worker records
`no_clean_equivalent` against the **provider taxonomy specifically**. That is
deliberate. The provider mapping is the one a future contributor would
plausibly reach for, and it is the dangerous one: a provider role asserts
clinical standing and legal accountability these agents must never appear to
hold, in the single domain where that misrepresentation could contribute to
patient harm. Recording the refusal as data is worth more than any crosswalk
would have been.

## Per-worker

All eleven: `no_clean_equivalent`. Each note states what the worker actually
does and why a provider role would misdescribe it — e.g. `test_utility_agent`
assesses test utility as analysis, whereas *ordering* a test is a clinician
act; `safety_agent` raises concerns for a clinician to act on rather than
itself safeguarding a patient.

## Sources

- SNOMED licensing: https://www.snomed.org/licensing
- SNOMED vendor licensing guide: https://docs.snomed.org/snomed-ct-practical-guides/vendor-introduction-to-snomed-ct/7-licensing
- GRADE certainty-of-evidence (CC BY-NC-ND): https://www.jclinepi.com/article/S0895-4356(16)30703-X/fulltext
- CC BY-NC-ND 4.0: https://creativecommons.org/licenses/by-nc-nd/4.0/
- AMIA competencies: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3534470/
