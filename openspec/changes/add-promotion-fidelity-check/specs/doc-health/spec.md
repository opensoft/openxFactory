# doc-health Specification Delta

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement eighteen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, client
identity roster composition, and promotion fidelity. Every check in this pass
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
an advisory report. Four of the eighteen — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
fourteen families and every corpus census, word count, canon-share figure,
shared-inventory entry, and catalog record SHALL be computed from the
governed corpus alone and MUST NOT move because the lifecycle scan set
exists. The promotion fidelity family reads archived spec DELTAS and promoted
SPECS — bodies rather than headers — and therefore takes neither the governed
corpus nor the lifecycle scan set as its document list; it moves no census,
word count, canon-share figure, inventory entry, or catalog record either.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** ideation routing MUST additionally inspect the aggregation root placement boundary and resolve explicitly referenced pinned repositories as its owning requirement defines
- **AND** proposal origin MUST validate active and archived proposal packets, support manifests, and staging-header linkage as its owning requirements define
- **AND** client identity roster composition MUST assemble the per-client roster fragments published by each pinned domain repository as its owning requirement in `client-identity-roster` defines
- **AND** promotion fidelity MUST compare each repository's archived spec deltas against its promoted specs as its owning requirement below defines
- **AND** status validity, standard backing, ratified provenance, and succession integrity MUST additionally read the declared lifecycle scan set, reporting a finding against the document's own path exactly as they do for a governed-corpus document
- **AND** a family or reference check that cannot run (for example notebook drift without credentials or an unavailable external checkout) MUST be reported as skipped, never silently omitted

## ADDED Requirements

### Requirement: Promotion fidelity of archived spec deltas
The promotion fidelity family SHALL compare every archived spec delta against
the promoted specification it was ratified to reach, and report a finding
where the delta's requirement did not arrive — reporting against the archived
delta's own path and naming the promoted spec it failed to reach.

The obligation being checked belongs to `document-lifecycle` ("Ratified spec
deltas reach the promoted specification"); this requirement defines only how
doc-health checks it, in the same by-reference relationship tag hygiene already
has with that capability's marker grammar.

The family SHALL implement three resolution rules, each of which exists to
prevent a specific false positive rather than to narrow the check:

- **Latest writer wins.** For a given capability and requirement title, only
  the MOST RECENT archived delta touching it is authoritative. Ordering is by
  the archive folder's `YYYY-MM-DD` prefix; a folder carrying no such prefix
  never outranks one that does. Where two archived changes share a date, the
  tie SHALL be broken by the packets' archive-commit order, falling back —
  only where version-control history cannot answer — to folder name ascending,
  and then to statement order within one delta file.
- **A `RENAMED` block retires the title it names.** `openspec archive` applies
  RENAMED before MODIFIED, so a later rename legitimately removes an earlier
  delta's title from canon and MUST NOT be reported as a missing requirement.
- **Archiving is presumed to be ratification, and only an explicit
  pre-ratification standing exempts a delta.** An archived packet's deltas
  SHALL be checked unless its own `proposal.md` carries a `Status:` whose
  declared standing is `draft` or lower in this corpus's taxonomy
  (`brainstorm`, `staged`, `draft`); a packet carrying a ratified-or-later
  standing, an unrecognized value, no `Status:` header, or no `proposal.md`
  at all SHALL be checked. The declared standing is the header value's leading
  token, read the same way in both directions, so an annotated ratification
  (`Status: ratified (approved at ...)`) declares `ratified` for the same
  reason an annotated `draft` declares `draft`. The status SHALL be read
  through the same lifecycle header reader every other family uses, never
  through a second one; a missing or invalid header is the status-validity
  family's finding to report, not this one's.

A recorded disposition in the aggregation checkout's `health/dispositions.yaml`
— an entry naming this family with a `cite`, optionally narrowed to one
requirement — SHALL suppress the findings it names. Nothing else suppresses:
a label, a title, or a claim in prose is not a disposition.

**This family SHALL be advisory at launch.** Every finding it emits carries
`warning` severity, so it publishes into the report and the ranked plan without
failing any run configured to fail on `error` or `critical`, and it is
deliberately NOT classified `contested`, because a contested finding that
resolves without a citation becomes an `error` under this capability's
uncited-resolution rule — which would make the family gate-blocking through
the back door on the first finding anyone fixed. Raising the severity and
adding the contested classification are ONE later decision taken together by
ruling, never a judgement call inside an implementation.

#### Scenario: A ratified delta did not reach canon
- **WHEN** the authoritative archived delta for a capability and requirement ADDED or MODIFIED it, and the promoted `openspec/specs/<capability>/spec.md` lacks that requirement title, or lacks a scenario title the delta states under it
- **THEN** the run MUST emit a `warning` finding against the archived delta's path, naming the requirement, the promoted spec, and each absent scenario
- **AND** the finding MUST NOT cause a run to fail under `--fail-on error` or `--fail-on critical`

#### Scenario: A ratified removal did not reach canon
- **WHEN** the authoritative archived delta REMOVED a requirement and the promoted spec still carries it
- **THEN** the run MUST emit a `warning` finding naming the requirement and the promoted spec that still carries it

#### Scenario: A capability was never promoted at all
- **WHEN** an authoritative archived delta ADDED or MODIFIED a requirement for a capability with no promoted spec file
- **THEN** the run MUST report the requirement against the delta's path, stating that the capability has no promoted spec

#### Scenario: An earlier delta was superseded
- **WHEN** a later archived ratified change rewrote, renamed, or removed what an earlier archived delta stated
- **THEN** only the later delta MUST be checked, and the earlier one MUST NOT produce a finding

#### Scenario: A deliberate non-promotion was recorded
- **WHEN** an archived packet's own `proposal.md` declares a standing of `draft` or lower
- **THEN** its spec deltas MUST NOT be checked for arrival in canon
- **AND** an annotation after the standing MUST NOT change what it declares

#### Scenario: An archived packet declares no pre-ratification standing
- **WHEN** an archived packet's `proposal.md` declares a ratified-or-later standing, declares a standing the taxonomy does not recognize, carries no `Status:` header, or is absent altogether
- **THEN** its spec deltas MUST be checked for arrival in canon, archiving being presumed to be ratification
- **AND** the missing or invalid header itself MUST be left to the status validity family rather than reported here

### Requirement: The promotion fidelity measurement basis is declared
A doc-health run SHALL compare archived deltas against the checked-out tree by
default — the same tree every other check family measures — and MAY be
configured to compare them against each repository's own live `main` instead.
That option SHALL apply to the promotion fidelity family alone; no other
family's inputs change because it is set.

A run's report SHALL state which basis this family measured, in the family's
own report section, on every run and whether or not the family found anything.
Where a live basis is requested and a repository's live `main` cannot be read,
the run SHALL measure that repository from its checkout and SHALL name the
repository as having fallen back — a report that mixed the two bases without
saying which was which would invite a reader to act on a stale finding as a
current one.

The obligation being checked does not change with the basis. What changes is
which state of the repository the run is speaking about, and a reader can only
act on a finding if the report says which.

#### Scenario: A run declares the live basis
- **WHEN** a run is configured to measure this family against live `main`s
- **THEN** the promotion fidelity family MUST read each repository's archived deltas and promoted specs from that repository's own live `main`
- **AND** every other check family MUST measure the checked-out tree exactly as it does on a default run
- **AND** the report MUST state the basis, and the resolved `main` it read, in the promotion fidelity section

#### Scenario: A live main cannot be read
- **WHEN** the live basis is requested and a repository's live `main` is unavailable to the run
- **THEN** that repository MUST be measured from its checkout rather than skipped
- **AND** the report MUST name that repository as having fallen back to the checkout

#### Scenario: A run declares no basis
- **WHEN** a run is not configured with a basis
- **THEN** the family MUST measure the checked-out tree
- **AND** the report MUST say so in the family's section

#### Scenario: A finding is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an archived delta path, and a `cite`
- **THEN** findings on that path MUST be suppressed, or only the named requirement's finding where the entry carries a `requirement` key
- **AND** an entry without a `cite` MUST suppress nothing

#### Scenario: No repository in scope carries an archive
- **WHEN** no repository in the run's scope has an `openspec/changes/archive/` directory
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted
