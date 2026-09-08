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

**CORRECTED 2026-08-25 ON BRETT'S RULING — this block is now
SCENARIO-COMPLETE.** As first written it restated only ONE of this
requirement's scenarios. OpenSpec's `MODIFIED` REPLACES A REQUIREMENT
WHOLESALE rather than merging into it, so promoting that block would have
dropped the seven scenarios it did not restate — `Lifecycle conformance checks
fire`, `A register carries staged status`, `Drift checks fire`, `Catalog
conformance checks fire`, `Routing conformance checks fire`, `Origin
conformance checks fire`, and `Roster composition is checked across domains` —
silently, because the file-level scenario count would have stayed at 98: the
seven lost exactly offset the seven this change's ADDED requirement brings.
Caught by the byte-for-byte promotion verification at archive time, before
anything was committed. The seven are restored below VERBATIM from the promoted
spec; only the first scenario differs from canon, and it differs by TWO `AND`
bullets rather than one — only the second is this change's. The first names
`promotion fidelity`, and it is INHERITED: this delta was written on top of
`add-promotion-fidelity-check`'s text, on the assumption that the sibling would
land first. That assumption is why canon now says "nineteen check families"
while `promotion fidelity`'s own owning requirement is still inside that active
change, so the bullet's "as its owning requirement below defines" is a FORWARD
REFERENCE until the sibling archives, at which point it resolves on its own.
Recorded in issue #329 rather than papered over; it is an ordering dependency,
not a defect in either change.

**THE ORDERING DEPENDENCY RESOLVED, 2026-08-25 — appended, with the paragraph
above left exactly as ratified.** `add-promotion-fidelity-check` archived
(`560e0bd5`), so two sentences above are now historical rather than current, and
they are corrected here rather than edited in place. First: the `promotion
fidelity` bullet's "as its owning requirement below defines" is no longer a
forward reference — that requirement is promoted canon, and the bullet resolves
against it. Second: this block no longer differs from canon by TWO `AND`
bullets. Canon absorbed the inherited one when the sibling archived, so exactly
ONE bullet here is new, and it is this change's own — `duplicate packet`.
Verified at this archive gate scenario-by-scenario: 8 of canon's 8 scenarios
restated, 7 byte-identical, and the eighth differing by that single bullet and
nothing else. This change is the third and last of the three siblings that each
restated this requirement, so the chain closes here — the enumeration reaches
twenty and no further active change is left holding a version of it.

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

#### Scenario: Lifecycle conformance checks fire
- **WHEN** a governance document violates a `document-lifecycle` rule — a free-form or missing `Status:` value, an unbacked `standard` claim, a `ratified` document whose lifecycle header carries no ratification citation in either sanctioned spelling, a dangling `Ratified by:` reference, a record-citing `Ratified:` line naming none of an approver, a date, or a resolvable record path, a `ratified` document whose lifecycle header carries more than one ratification citation (one of each spelling, or the same spelling twice), a `superseded` doc without a successor, a `brainstorm` doc outside `ideation/brainstorm/`, a `staged` doc that is outside `ideation/staging/` and is not a candidate register (`Kind: register`), or a content edit to a `record` doc after capture
- **THEN** the run MUST emit a finding naming the check family, the repo, the path, and the violated rule

#### Scenario: A register carries staged status
- **WHEN** a candidate register (`Kind: register`) carries `Status: staged` outside `ideation/staging/`
- **THEN** location conformance MUST NOT emit a finding — registers are a promoted organized-state home per the `document-lifecycle` capability

#### Scenario: Drift checks fire
- **WHEN** a submodule pin lags its remote main, a contract copy diverges from its canonical source, or the lifecycle notebook projection dry-run reports nonzero add/update/delete operations
- **THEN** the run MUST emit a drift finding identifying what diverged and from which source of truth

#### Scenario: Catalog conformance checks fire
- **WHEN** governed-document coverage, catalog identity, freshness, taxonomy, provenance, override standing, or record immutability violates the promoted catalog contract
- **THEN** the run MUST emit a `document-catalog` finding with the violated requirement and evidence

#### Scenario: Routing conformance checks fire
- **WHEN** a routed idea, claim, destination, proposal manifest, repository ID or gitlink, or aggregation placement violates the promoted routing contract
- **THEN** the run MUST emit an `ideation-routing` finding with the violated requirement and evidence

#### Scenario: Origin conformance checks fire
- **WHEN** a proposal packet, support manifest, or staging-header linkage violates the promoted origin contract
- **THEN** the run MUST emit a `proposal-origin` finding with the violated requirement and evidence

#### Scenario: Roster composition is checked across domains
- **WHEN** two or more pinned domain repositories publish client identity roster fragments for the same client
- **THEN** the roster composition family assembles them and reports shared identity material or undeclared cross-domain reach
- **AND** intra-repo entry conformance is NOT reported here, because it fails the owning domain's gate instead
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

**This family SHALL be enforcing, in both halves of what that means.** Every
finding it emits SHALL carry `error` severity, so a run configured to fail on
`error` fails on a ruling discharged twice; and the family SHALL be classified
`contested`, so a finding that stops being reported without a recorded citation
becomes an `error` under this capability's uncited-resolution rule. The two
SHALL move together and MUST NOT be taken apart: severity alone gates the
family without the discipline that makes a disappearing finding accountable,
and the contested class alone gates it through `uncited-resolution` under a
family name that does not say what happened.

The family SHIPPED ADVISORY and was flipped by ruling, which is the sequence
this requirement records rather than a history it has replaced. At launch every
finding carried `warning` and the family was deliberately unclassified, because
no run had yet measured what any archive outside this repository would say and
a `contested` advisory family would have gated through the back door on the
first duplicate anyone withdrew. The flip SHALL be taken as one decision by
ruling, never as a judgement call inside an implementation, and SHALL follow a
measurement showing the population it will gate is discharged rather than
precede it — a gate that goes red on the commit introducing it teaches everyone
to route around the gate. The measurement SHALL be taken on the basis this
family enforces on, which is the checked-out tree; a zero measured on some
other tree is a fact about that tree.

#### Scenario: Two packets discharge one ruling with no account of each other
- **WHEN** two archived packets state the same capability and requirement title with requirement bodies identical after trailing-whitespace normalization, and neither packet's `proposal.md` names the other's change id
- **THEN** the run MUST emit an `error` finding against the later packet's archived delta path, naming both packets, the requirement, the capability, and a digest of the restated block
- **AND** the finding MUST cause a run configured `--fail-on error` to fail, and MUST NOT cause a run configured `--fail-on critical` to fail
- **AND** the finding MUST carry the `contested` resolution class

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

#### Scenario: A reported duplicate stops being reported
- **WHEN** a finding this family reported in a previous report is absent from a later report, and the family actually ran in that later run
- **THEN** the disappearance MUST be reported under the uncited-resolution rule unless a citation records the governance act that closed it
- **AND** a run CONFIGURED not to execute this family MUST NOT have that family's absent findings read as resolved, a family that never ran having looked at nothing

#### Scenario: No repository in scope carries an archive
- **WHEN** no repository in the run's scope has an `openspec/changes/archive/` directory
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted
