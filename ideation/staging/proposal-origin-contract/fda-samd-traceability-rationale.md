# FDA SaMD Traceability Rationale

Status: staged
Kind: regulatory rationale
Repository context: openxFactory
Staging ID: openxFactory:staging:proposal-origin-contract
Regulatory review date: 2026-07-09
Target: proposal-origin contract and a follow-up regulated-traceability profile

## Conclusion

The proposal-origin contract is a necessary first traceability edge, but it is
not by itself sufficient to establish FDA compliance for Software as a Medical
Device (SaMD) or another device software function. It preserves why a change
entered the controlled process and prevents an undocumented bypass of staging.
FDA-facing traceability must continue from that origin through intended use,
requirements, risks, design, implementation, verification, validation, the
exact released version, and postmarket records.

The implementable design is therefore:

1. openxFactory owns neutral identifiers, typed trace links, lifecycle gates,
   immutable release baselines, and evidence-package rules.
2. A domain repository such as MedxFactory activates an FDA device-software
   profile that makes the applicable regulatory records and approvals
   mandatory.
3. codexFactory validates the neutral graph and the selected profile, but the
   device manufacturer remains responsible for intended-use classification,
   risk acceptance, quality approval, regulatory decisions, and maintaining
   the validated state of the tooling.

This is an FDA-aligned control design, not a declaration that the repository or
product is compliant. Compliance requires implementation under the
manufacturer's quality management system (QMS), approved procedures, trained
personnel, validated tools, controlled records, and evidence from the actual
device and release.

## Regulatory Basis

The reasoning uses the following current primary sources:

- [21 CFR Part 820, Quality Management System Regulation](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-820)
  applies to the design and manufacture of finished devices. As of February 2,
  2026, the QMSR incorporates ISO 13485:2016 and Clause 3 of ISO 9000 by
  reference. The applicable manufacturer must maintain access to the
  incorporated standards and map this process into its controlled QMS.
- [FDA Content of Premarket Submissions for Device Software Functions (June 2023)](https://www.fda.gov/media/153781/download)
  recommends risk-based Basic or Enhanced documentation, traceable software
  requirements, risk-control verification, software testing evidence, version
  history, and risk-based disposition of unresolved anomalies.
- [FDA General Principles of Software Validation](https://www.fda.gov/media/73141/download)
  describes bidirectional traceability among system requirements, software
  requirements, risk analysis, design, source code, and tests.
- [FDA/IMDRF SaMD Clinical Evaluation](https://www.fda.gov/files/medical%20devices/published/Software-as-a-Medical-Device-%28SAMD%29--Clinical-Evaluation---Guidance-for-Industry-and-Food-and-Drug-Administration-Staff.pdf)
  identifies valid clinical association, analytical validation, and clinical
  validation as the three clinical-evaluation evidence components for SaMD.
- [21 CFR Part 11, Electronic Records and Electronic Signatures](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
  applies when electronic records or signatures are used for records required
  by FDA regulations. Its controls include system validation, accurate and
  complete copies, retention and retrieval, access restriction, audit trails,
  sequencing and authority checks, training, and documentation change control.
- [FDA Computer Software Assurance for Production and Quality Management
  System Software (February 2026)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/computer-software-assurance-production-and-quality-management-system-software)
  recommends risk-based assurance that QMS automation is fit for intended use
  and remains in a validated state throughout its lifecycle.
- [FDA Cybersecurity in Medical Devices (February 2026)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket)
  adds lifecycle and submission expectations when the device has cybersecurity
  risk, including the statutory requirements applicable to cyber devices.

FDA guidance documents contain nonbinding recommendations. The applicable law,
device classification, submission pathway, special controls, recognized
standards, and FDA feedback for a specific product can add or alter the needed
evidence.

## Traceability Claim

The controlled record must support traversal in both directions across this
graph:

```text
brainstorm or ad-hoc decision
  -> staged-origin ID
  -> OpenSpec change ID
  -> intended use and user/patient need IDs
  -> system and software requirement IDs
  -> hazard, hazardous-situation, and risk-control IDs
  -> architecture and software design IDs
  -> source commit and build identifiers
  -> unit, integration, system, usability, and security test IDs/results
  -> analytical and clinical evidence IDs, when applicable
  -> approval and unresolved-anomaly disposition IDs
  -> immutable spec baseline + product version + build digest
  -> submission/authorization and distributed-release IDs
  -> complaint, correction, CAPA, and postmarket monitoring IDs
```

The FDA software guidance gives a concrete risk-control example that links an
identified hazard to SRS and SDS requirements and then to unit, integration,
and system tests. It permits the links to be presented in a separate artifact
when the many-to-many relationship is cumbersome. Accordingly, xFactory may
store the graph as structured metadata and generate a human-readable matrix;
the graph, not a manually maintained duplicate table, is the source of truth.

Each edge must identify the relationship, not merely mention another record.
At minimum the relation vocabulary must distinguish `derived_from`,
`implements`, `controls`, `verified_by`, `validated_by`, `released_as`,
`supersedes`, `forward_ported_to`, and `resulted_in`.

## Minimum Neutral Contract

The proposal packet should keep the proposed `origin` block and add a neutral
compliance declaration. A non-applicable decision must be explicit and
reviewable; silence is not equivalent to non-applicability.

```yaml
origin:
  kind: staged
  id: openxFactory:staging:proposal-origin-contract
  path: ideation/staging/proposal-origin-contract

compliance:
  profiles:
    - id: fda-device-software
      version: 1
      applicability: applicable
      rationale_ref: records/regulatory-applicability.md

traceability:
  record_set_id: medxFactory:trace:<product>:<change-id>
  links_ref: records/trace-links.yaml
```

The neutral contract must validate identifier uniqueness, allowed relation
types, resolvable targets, bidirectional traversal, baseline immutability, and
evidence-package integrity. It must not encode a conclusion about whether a
product is a medical device.

## FDA Device-Software Profile

When `fda-device-software` is applicable, the domain profile must require
references to controlled records for:

```yaml
regulatory:
  intended_use_ref: records/intended-use.md
  device_classification_ref: records/device-classification.md
  submission_pathway_ref: records/submission-pathway.md
  software_documentation_level: basic | enhanced | not_yet_determined
  risk_management_plan_ref: records/risk-management-plan.md
  risk_assessment_ref: records/risk-assessment.yaml
  risk_management_report_ref: records/risk-management-report.md
  clinical_evaluation_ref: records/clinical-evaluation.md
  cybersecurity_applicability_ref: records/cybersecurity-applicability.md
  qms_record_class: design-development
  retention_policy_ref: qms://record-retention/device-design

release:
  product_line_id: <durable product identity>
  development_line: <mutable branch name>
  spec_baseline: <immutable spec tag and commit>
  software_version: <marketed version>
  source_commit: <immutable commit>
  build_digest: <immutable artifact digest>
  prior_authorized_version_ref: <record or null>
  submission_or_authorization_ref: <record or null>

approvals:
  design_owner_ref: <approval record>
  quality_ref: <approval record>
  regulatory_ref: <approval record>
  electronic_signature_record_ref: <Part 11 system record when applicable>
```

The referenced trace-link set must cover, as applicable:

- user and patient needs, intended use, and software requirements
- hazards, hazardous situations, harms, initial risk, risk controls, residual
  risk, benefit-risk decisions, and introduced-risk analysis
- architecture, detailed design, source, and configuration items
- expected results, actual results, objective pass/fail outcomes, failures,
  corrections, regression analysis, and regression tests
- valid clinical association, analytical validation, and clinical validation
- threat modeling, security requirements, controls, testing, and postmarket
  cybersecurity plans for devices with cybersecurity risk
- all unresolved anomalies and their safety/effectiveness dispositions
- the exact tested, approved, built, released, and, where relevant, authorized
  versions

## Lifecycle Gates

### Brainstorm and Staging

Brainstorm material remains non-normative. Moving into staging assigns the
durable origin ID and requires an initial regulatory-applicability assessment.
This assessment may be `undetermined`, but a proposal affecting intended use,
clinical logic, patient-facing behavior, risk controls, data inputs, model
behavior, security, or released-device maintenance cannot remain
`undetermined` at ratification.

### Proposal

The proposal gate requires origin, compliance profile selection, intended-use
impact, affected product/release lines, initial risk impact, and links to every
affected existing requirement, hazard, risk control, and postmarket record.
An ad-hoc origin records urgency or provenance; it never waives a regulated
review or evidence requirement.

### Ratification

Ratification requires designated design, Quality, and Regulatory approvals for
an applicable device-software change. Requirements must be complete,
unambiguous, objectively verifiable, uniquely identified, and linked to user
needs and risk analysis. Risk acceptability criteria must come from the
approved risk-management process, not from the proposal author.

### Implementation and Verification

Implementation records the source commits and configuration items that
implement each requirement and risk control. Verification records expected and
actual results and objective pass/fail decisions. Failed tests, changes made in
response, regression analysis, regression tests, and unresolved anomalies must
remain visible and receive risk-based disposition.

### Validation and Release

Validation establishes objective evidence that the software satisfies user
needs and intended uses in the actual or simulated use environment. For SaMD,
the release evidence must also reference the applicable clinical-evaluation
components. Release is blocked until the trace graph has no unexplained orphan
or broken links, required approvals are complete, and residual-risk and anomaly
decisions apply to the exact candidate build.

The release record must bind an immutable specification baseline, source
commit, test evidence set, build digest, and marketed software version. A Git
branch is a mutable development line; it is not release evidence. A tag may
serve as an immutable baseline pointer only when repository controls prevent
movement or deletion and the archived record also preserves the resolved
commit and artifact digest.

Parallel supported versions remain separate record sets. A patch to version A
creates a new A release record and an explicit impact/forward-port decision for
B, C, and D. Later lines do not inherit a safety fix merely because Git can
rebase or merge it. Each affected line must record whether the change was
applied, independently implemented, already present, or not applicable, and
must produce its own verification and release evidence.

### Archive and Postmarket

The archived proposal package must remain readable, searchable, reproducible,
and linked to the released record set. Compression is acceptable for storage,
but a manifest must expose record IDs, paths, hashes, retention class, and the
exact release identities without requiring historical guesswork.

Complaints, corrections, removals, CAPA, servicing where applicable, and
postmarket monitoring must link back to the affected distributed version and
forward to the resulting risk, requirement, implementation, verification, and
release records.

## Electronic Records and Tool Assurance

Git history provides useful change provenance but does not, by itself,
demonstrate Part 11 compliance or make a Git author field an electronic
signature. When these repositories hold required electronic records:

- the manufacturer must define which system is the authoritative record
  system and whether Part 11 applies
- access, identity, approval authority, signature meaning, audit trail,
  retention, backup, retrieval, and inspection-copy procedures must be
  controlled
- prior entries must not be obscured by force-push, tag movement, history
  rewrite, or archive replacement
- required approvals must reference a compliant signature record when an
  electronic signature is used
- xFactory/codexFactory automation must have an intended use, risk assessment,
  assurance plan, test evidence, change control, and periodic/continuous
  evidence that it remains in a validated state

The QMS may designate a different validated document/e-signature system as the
authoritative record and treat Git/OpenSpec as a controlled authoring and
evidence-generation system. In that case the archive must include durable
references and reconciliation evidence between the two systems.

## Acceptance Criteria

An FDA-profiled release is traceability-ready only when automated checks and
independent review demonstrate all of the following:

1. Every released software requirement has an approved source, implementation,
   and verification result; every released implementation item traces back to
   an approved requirement or documented infrastructure rationale.
2. Every identified risk control traces to its hazard or hazardous situation,
   requirement/design implementation, effectiveness verification, and exact
   release; introduced-risk analysis is present.
3. All safety- and effectiveness-critical requirements have complete
   bidirectional links through system testing and applicable validation or
   clinical evidence.
4. No required record target is missing, ambiguous, or mutable without an
   audit trail. Duplicate and orphan identifiers are rejected.
5. Test failures and unresolved anomalies have approved risk-based dispositions
   for the candidate release, not only for another branch or version.
6. The tested, approved, released, distributed, and authorized versions are
   identical, or every difference has a documented safety/effectiveness impact
   assessment and approval.
7. The evidence package can produce accurate, complete, human-readable and
   electronic copies and can be retrieved for its entire retention period.
8. Applicable Quality, Regulatory, design, and Part 11 approval records resolve
   and are bound to the immutable evidence package.

## Current Gaps and Required Follow-Up

The current origin proposal satisfies only the first graph edge. Before this
process is used as FDA compliance evidence, a separate OpenSpec change should
ratify a `regulated-traceability` capability with:

- the neutral record and link schemas
- an applicability decision and profile-selection contract
- release/version baseline rules for parallel supported versions
- FDA device-software profile requirements in the domain repository
- profile-aware proposal, ratification, implementation, release, and archive
  validators
- generated trace matrix and orphan/broken-link reports
- Part 11/QMS record-system integration requirements
- codexFactory computer-software-assurance evidence and regression tests

The recommended sequence is to complete `add-proposal-origin-contract`, then
organize this rationale into a distinct staged topic named
`regulated-traceability-profile`. The origin proposal must not claim to solve
the full regulated traceability problem.
