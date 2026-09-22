# domain-mapping-declaration Specification

A NEW capability. It does not exist in `openspec/specs/` and no active change
carries a delta on it, so there is no collision and no basis marker is owed.

**WHY IT IS `openxFactory`'s.** RULING C2 (`opensoft/openxFactory` issue #656,
2026-09-04T17:47Z) is that **openXdox is the domain-mapping core, PARAMETERIZED
by a domain profile that a descendant supplies** — it holds typed artifact kinds,
a governed lifecycle engine (statuses, gates, roles, evidence) and the
dispatch/apply lane, and *"a clinician using `MedxDox` never sees the word
'requirement'"*. The PROFILE is therefore the one artifact a `<Domainx>Dox`
descendant actually contains, which is what gives
`domain-descendant-boundary`'s "pin and profile, never fork" something concrete
to mean one level down. WHAT a descendant must declare is xFactory-layer
doctrine — it is the same question `layer-vocabulary`, `roles-authority-model`
and `governed-derived-model` already answer for other axes — so it is
`openxFactory`'s, and its ENFORCEMENT is openXdox's.

**The extraction this is written from.** Three domain mappings were worked
explicitly, as DIRECTION Q5 required — MedxFactory (patient management and
research), LedgerxFactory (financial simulations and accounting questions) and
AdxFactory (marketing analysis) — against
`docs/domain-instantiation-pre-run-questionnaire.md`,
`contracts/policies/layer-vocabulary.yaml` and `docs/governed-derived-model.md`.
The five declaration axes below are what the three have in common with different
nouns. `design.md` § D4 carries the mappings and the seven machineries the
extraction found.

## ADDED Requirements

### Requirement: A domain descendant declares its mapping, and the neutral layer ships no domain's vocabulary
A `<Domainx>Dox` descendant SHALL carry a DOMAIN MAPPING DECLARATION and the
neutral layer SHALL be parameterized by it rather than shipping any one domain's
words. The declaration SHALL cover exactly five axes: the domain's ARTIFACT
KINDS; the LIFECYCLE VOCABULARY each kind travels — its statuses, the legal
transitions between them, and the point at which a record becomes
immutable-with-addenda; the ACTS and the GATE each act passes; the EVIDENCE
CLASSES a derived statement must cite; and the PROMOTING AUTHORITIES, named as
roles rather than as people. A neutral layer that hardcodes one domain's status
words, artifact nouns or act verbs SHALL be reported, because every other
descendant then forks it — which is the failure DIRECTION Q5 was given to
prevent.

#### Scenario: A descendant carries no mapping declaration
- **WHEN** a `<Domainx>Dox` descendant is created with no domain mapping declaration
- **THEN** it is an empty boundary under `domain-descendant-boundary`, because the declaration is the profile artifact that makes it a descendant rather than a directory

#### Scenario: The neutral layer hardcodes a domain's status words
- **WHEN** the domain-mapping core reads or writes a status vocabulary it did not receive from a declaration
- **THEN** the hardcoding is reported, and the vocabulary moves into the declaration of the domain it belongs to

#### Scenario: openxFactory's own vocabulary is treated as neutral
- **WHEN** `openxFactory`'s nine-word `Status:` taxonomy, its change/spec/delta nouns or its doc-health families are placed in the neutral layer rather than in the engineering descendant's declaration
- **THEN** the placement is refused under RULING C2, because a clinician using a descendant would then see the word "requirement"

### Requirement: A lifecycle declaration names its transitions and the authority each one requires
A domain mapping declaration's LIFECYCLE axis SHALL name, for each artifact kind:
the closed status vocabulary; every legal transition as an ordered pair; the
AUTHORITY each transition requires, named as a role the declaration's authority
axis also carries; and the status at which the record becomes immutable, with
addenda as the only lawful later writes. A transition with no declared authority
SHALL be refused rather than defaulted to "any actor", and a vocabulary with no
declared immutability point SHALL be refused rather than defaulted to "never",
because both defaults are the permissive answer to a question the domain was
asked precisely because permissiveness is unsafe.

#### Scenario: A transition declares no authority
- **WHEN** a lifecycle declaration names a transition without naming the authority it requires
- **THEN** the declaration is refused, and the transition is not treated as open to any actor

#### Scenario: A status outside the closed vocabulary appears
- **WHEN** an artifact carries a status the declaration's closed vocabulary does not contain
- **THEN** the artifact is reported against its declaration rather than silently accepted

#### Scenario: Three domains declare the same shape with different words
- **WHEN** a clinical note (drafted, attested, filed, immutable-with-addenda), an accounting question (raised, researched, concluded, professionally reviewed, filed) and a campaign brief (drafted, brand-reviewed, spend-approved, launched, measured, retired) are each declared
- **THEN** all three are expressible in one engine, because they differ in their words and not in their shape

### Requirement: A mapping declaration names the truth store its derived models may never write
A domain mapping declaration SHALL name, for every derived-model family the
domain declares under `governed-derived-model`, the TRUTH STORE the model may
never write and the EXTERNAL ENFORCEMENT point that store sits behind — the
clinical chart for a care domain, the ledger for an accounting domain, the ad
platform for a marketing domain, the repository and its branch protection for an
engineering domain. A derived-model family declared with no named truth store
SHALL be refused, because `governed-derived-model`'s constitutional invariant
that a model is non-authoritative by construction is unenforceable when nothing
names what it is non-authoritative ABOUT.

#### Scenario: A derived-model family names no truth store
- **WHEN** a domain declares a model and scenario pair without naming the truth store the model may never write
- **THEN** the declaration is refused, because the read-only invariant has no subject

#### Scenario: A model proposes a write to the named truth store
- **WHEN** a scenario's output would write the declared truth store
- **THEN** the write is refused and the output stays within the declared enum, the model having no action authority by construction

#### Scenario: The external enforcement point is unreachable
- **WHEN** the enforcement point a declaration names cannot be reached
- **THEN** the acts that gate on it refuse, rather than proceeding on the neutral layer's own verdict alone
