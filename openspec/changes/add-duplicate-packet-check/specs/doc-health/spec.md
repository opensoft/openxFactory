# doc-health Specification Delta

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twenty check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, client
identity roster composition, promotion fidelity, release-inventory drift, and
duplicate packet.
Every check in this pass
MUST be
deterministic — identical inputs produce identical findings, with no model
calls; semantic analysis belongs to the agentic semantic sweep and the separate
document-cataloger and ideation-organizer lanes their owning capabilities
define. Check families SHALL implement promoted spec wording; staged ideation
fragments are inputs to contracts, never check definitions. The client
identity roster composition family SHALL cover only the CROSS-DOMAIN
concerns — assembling per-client fragments published by each domain and
reporting shared identity material or undeclared cross-domain reach —
because intra-repo roster conformance is a blocking domain gate rather than
an advisory report. Four of the twenty — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
sixteen families and every corpus census, word count, canon-share figure,
shared-inventory entry, and catalog record SHALL be computed from the
governed corpus alone and MUST NOT move because the lifecycle scan set
exists. The promotion fidelity family reads archived spec DELTAS and promoted
SPECS — bodies rather than headers — and therefore takes neither the governed
corpus nor the lifecycle scan set as its document list; it moves no census,
word count, canon-share figure, inventory entry, or catalog record either. The
release-inventory drift family reads CONTRACT ARTIFACT BYTES — a release digest
inventory and the blobs it names — and likewise takes neither document list,
and it moves no census, word count, canon-share figure, inventory entry, or
catalog record. The duplicate packet family reads archived spec deltas ONLY
AGAINST EACH OTHER — never against canon, which by construction cannot show
that a ruling was discharged twice — and takes neither document list and moves
none of those figures either.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** ideation routing MUST additionally inspect the aggregation root placement boundary and resolve explicitly referenced pinned repositories as its owning requirement defines
- **AND** proposal origin MUST validate active and archived proposal packets, support manifests, and staging-header linkage as its owning requirements define
- **AND** client identity roster composition MUST assemble the per-client roster fragments published by each pinned domain repository as its owning requirement in `client-identity-roster` defines
- **AND** promotion fidelity MUST compare each repository's archived spec deltas against its promoted specs as its owning requirement below defines
- **AND** release-inventory drift MUST compare each repository's declared bundle inventory against the blobs it names as its owning requirement below defines
- **AND** duplicate packet MUST compare each repository's archived spec deltas against each other as its owning requirement below defines
- **AND** status validity, standard backing, ratified provenance, and succession integrity MUST additionally read the declared lifecycle scan set, reporting a finding against the document's own path exactly as they do for a governed-corpus document
- **AND** a family or reference check that cannot run (for example notebook drift without credentials or an unavailable external checkout) MUST be reported as skipped, never silently omitted

## ADDED Requirements

### Requirement: One ruling, one discharge, across archived packets
The duplicate packet family SHALL compare every archived spec delta against
every other archived spec delta in the same repository, and report where two
packets state the same capability and requirement title with content-identical
requirement bodies and neither packet's proposal names the other — reporting
against the later packet's own delta path and naming the earlier packet it
restates.

The obligation being checked belongs to `document-lifecycle` ("A ruling is
discharged once"); this requirement defines only how doc-health checks it, in
the same by-reference relationship promotion fidelity already has with that
capability's promotion obligation.

**This family answers a question the promotion fidelity family cannot.** That
family compares an archived delta to CANON, and where one ruling has been
discharged twice canon holds exactly what both packets said it should hold — so
it reports zero either way. The comparison that can see the class is between the
archived deltas themselves, which is why this is a separate family rather than
a wider reading of that one.

The family SHALL implement one identity rule and one exemption, and the
exemption is what keeps the lawful remedy legal:

- **Content identity, not resemblance.** Two archived packets state the same
  thing only where their requirement bodies are byte-identical after trailing
  whitespace — per-line trailing spaces and trailing blank lines — is
  normalized, and after no other normalization. The requirement's own heading
  line is not part of the body compared, because the title is compared through
  the family's title normalization already. A similarity or near-match rule
  MUST NOT be used: revising a requirement is not restating it, and a rule
  loose enough to conflate the two would report the ordinary case.
- **A recorded remedial lineage is exempt.** Where either packet's own
  `proposal.md` names the other's change id — in the bare change-id spelling or
  as the archived folder that carries it, matched as a whole token so that one
  change id occurring inside a longer one buys no exemption — the pair SHALL
  NOT be reported. Applying an already-ratified delta byte-faithfully is the
  prescribed remedy for a promotion gap, and naming the packet whose ruling is
  being applied is what makes the second statement traceable to the first.
  The naming records LINEAGE, not authority: it does not establish that the
  restating packet had standing to restate, which is the ratified provenance
  family's question, and this family MUST NOT be read as deciding it.
- **The pre-ratification and disposition exemptions are the existing ones.** A
  packet whose own `proposal.md` declares a standing of `draft` or lower
  discharged no ruling and SHALL NOT be paired, read through the same
  lifecycle header reader the promotion fidelity family uses rather than a
  second one. A recorded disposition in the aggregation checkout's
  `health/dispositions.yaml` naming THIS family, with a `cite`, optionally
  narrowed to one requirement, SHALL suppress the findings it names; an entry
  naming another family MUST NOT suppress this family's findings.

The comparison SHALL be pairwise within each identity: three packets stating
one requirement identically are three pairs, and a pair carrying a recorded
lineage says nothing about a pair that does not.

**This family SHALL measure the checked-out tree.** The live-`main` basis this
capability defines applies to the promotion fidelity family alone, and a report
that said otherwise while this family read a pin would mislead every reader of
its basis line.

**This family SHALL be advisory at launch.** Every finding it emits carries
`warning` severity, so it publishes into the report and the ranked plan without
failing any run configured to fail on `error` or `critical`, and it is
deliberately NOT classified `contested`, because a contested finding that
resolves without a citation becomes an `error` under this capability's
uncited-resolution rule — which would make the family gate-blocking through the
back door on the first duplicate anyone withdrew. Raising the severity and
adding the contested classification are ONE later decision taken together by
ruling, never a judgement call inside an implementation.

#### Scenario: Two packets discharge one ruling with no account of each other
- **WHEN** two archived packets state the same capability and requirement title with requirement bodies identical after trailing-whitespace normalization, and neither packet's `proposal.md` names the other's change id
- **THEN** the run MUST emit a `warning` finding against the later packet's archived delta path, naming both packets, the requirement, the capability, and a digest of the restated block
- **AND** the finding MUST NOT cause a run to fail under `--fail-on error` or `--fail-on critical`

#### Scenario: A remedial packet names the ruling it applies
- **WHEN** an archived packet restates another archived packet's ratified delta byte-faithfully and its own `proposal.md` names that packet's change id
- **THEN** the pair MUST NOT be reported
- **AND** the change id MUST be matched as a whole token, so that a packet naming only itself gains no exemption because another packet's id is a fragment of its own

#### Scenario: Two remedials of one ruling do not name each other
- **WHEN** two archived packets each restate a third packet's ratified delta and each names that third packet, but neither names the other
- **THEN** the two pairs involving the original MUST NOT be reported
- **AND** the pair the two remedials form MUST be reported

#### Scenario: A requirement is revised rather than restated
- **WHEN** a later archived packet states a requirement title an earlier packet also stated, with any difference in the requirement body beyond trailing whitespace
- **THEN** the pair MUST NOT be reported, a revision not being a second discharge

#### Scenario: A pre-ratification packet restates another
- **WHEN** two archived packets state identical requirement bodies and either one's `proposal.md` declares a standing of `draft` or lower
- **THEN** the pair MUST NOT be reported, a packet that claimed no ratification having discharged no ruling

#### Scenario: A finding is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an archived delta path, and a `cite`
- **THEN** findings on that path MUST be suppressed, or only the named requirement's finding where the entry carries a `requirement` key
- **AND** an entry naming a different family MUST suppress nothing here

#### Scenario: No repository in scope carries an archive
- **WHEN** no repository in the run's scope has an `openspec/changes/archive/` directory
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted
