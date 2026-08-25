# doc-health Specification Delta

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twenty-one check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, client
identity roster composition, promotion fidelity, release-inventory drift,
duplicate packet, and family enumeration.
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
an advisory report. Four of the twenty-one — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
seventeen families and every corpus census, word count, canon-share figure,
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
none of those figures either. The family enumeration family reads THIS
REQUIREMENT and the code registry that satisfies it — a promoted spec and a
Python dict, neither of them a governed-corpus document — so it likewise takes
neither document list and moves none of those figures.

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

**FOURTH RESTATEMENT, AND THE FIRST ONE A CHECK VERIFIED — appended
2026-08-25, with every paragraph above left exactly as promoted.** The three
notes above record three separate repairs of this one requirement, all three
caught by a human. This block is the fourth restatement of it, and it is the
first written under `add-family-enumeration-check`: its own delta half read
this block, resolved every name here against `families.FAMILIES`, and checked
all three numerals before the change could be committed. The enumeration
reaches twenty-one and the counts are derived rather than re-typed. That the
check policing this requirement had to restate this requirement to add itself
to it is deliberate, and it is the acceptance test — a wrong restatement here
could not have landed, because the thing it would corrupt was standing at the
gate.

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
- **AND** family enumeration MUST verify this requirement's own family enumeration and counts against the code registry as its owning requirement below defines
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

### Requirement: The family enumeration is derived, not restated on trust
The doc-health suite SHALL verify that the family enumeration and the counts
stated by the "Deterministic check families" requirement agree exactly with the
code registry of families the suite actually runs, and report every divergence
naming precisely what diverged.

The requirement being checked is this capability's own, which is the point: it
NAMES every check family and COUNTS them three times in prose, and every new
family must restate that whole requirement to add itself. A requirement whose
text every new family must restate is a requirement every new family can
truncate. Three changes in three days truncated it, and all three were caught
by a human rather than by a check.

The registry SHALL be the mapping of family ids the suite iterates when it
runs — not the reporting list, which is a separate declaration and is allowed
to be a subset. The reporting list SHALL NOT promise a report section for a
family the registry does not register.

The verification SHALL cover BOTH the promoted requirement AND every ACTIVE
change delta that restates it:

- **A promoted enumeration** SHALL name exactly the registered families, each
  once, and its numerals SHALL be arithmetically true of that set: the stated
  total equals the number registered, a stated subset-of-total agrees with that
  total, and a stated remainder equals the total minus the stated subset.
- **An active change delta restating the requirement** SHALL carry the complete
  enumeration, consistent with the registry in its own tree. A change that
  registers a new family states that family in its delta, so the two are
  self-consistent before promotion and the incomplete restatement is reported
  at authoring time rather than at an archive gate.
- **The promoted requirement SHALL be exempt from the count comparison while
  an active delta restates it**, because a change that registers family N+1
  leaves canon stating N until it archives. Canon is pending there, not
  divergent, and the delta is what carries the obligation.
- Where more than one active delta restates the requirement, EACH SHALL be
  checked independently against the registry, because a `MODIFIED` requirement
  replaces its promoted counterpart wholesale and whichever change archives
  last is the one canon keeps.

A prose family name SHALL resolve to a registry id by a mechanical
normalization plus a declared alias set, and a name that resolves to no
registered family SHALL be reported rather than guessed at. The alias set
SHALL be minimal — an alias that is no longer needed is itself a defect.

**This family SHALL be advisory at launch.** Every finding it emits carries
`warning` severity, so it publishes into the report and the ranked plan without
failing any run configured to fail on `error` or `critical`, and it is
deliberately NOT classified `contested`, because a contested finding that
resolves without a citation becomes an `error` under this capability's
uncited-resolution rule — which would make the family gate-blocking through the
back door on the first divergence anyone corrected. Raising the severity and
adding the contested classification are ONE later decision taken together by
ruling, and SHALL follow a measurement of the population the gate would red
rather than precede it.

#### Scenario: The promoted enumeration omits a registered family
- **WHEN** no active change delta restates the requirement, and the promoted enumeration does not name a family the registry registers
- **THEN** the run MUST emit a `warning` finding against the promoted spec's path, naming the omitted families and the registered total
- **AND** the finding MUST NOT cause a run to fail under `--fail-on error` or `--fail-on critical`

#### Scenario: The promoted enumeration carries a stale numeral
- **WHEN** no active change delta restates the requirement, and the stated total differs from the number of registered families, or a stated remainder does not equal the stated total minus the stated subset
- **THEN** the run MUST emit a finding naming the stated numeral, the derived one, and which sentence carried it

#### Scenario: The promoted enumeration names an unregistered family
- **WHEN** the enumeration names a family that resolves to no registered family id
- **THEN** the run MUST report that name and the id it resolved to, rather than ignoring it or matching it approximately

#### Scenario: An active delta restates the requirement incompletely
- **WHEN** an active change's `doc-health` delta restates the requirement and its enumeration omits a registered family, names an unregistered one, or carries a numeral inconsistent with the registry in its own tree
- **THEN** the run MUST emit a finding against that delta's own path, so the incomplete restatement is reported before it can be promoted

#### Scenario: A change adds a family and canon has not moved yet
- **WHEN** an active change registers a new family and restates the requirement completely for its own tree, while the promoted requirement still states the previous total
- **THEN** the promoted requirement MUST NOT be reported, its statement being pending promotion rather than divergent
- **AND** the active delta MUST be reported if ITS restatement is incomplete

#### Scenario: Two active deltas both restate the requirement
- **WHEN** two or more active changes each restate the requirement
- **THEN** each delta MUST be checked independently against the registry, neither one excusing the other

#### Scenario: The reporting list promises a section for no family
- **WHEN** the reporting list names an id the registry does not register
- **THEN** the run MUST report it, a report section for a family that never runs being invisible to every other check
- **AND** a registered family absent from the reporting list MUST NOT be reported by this family, that being a separate declaration this requirement does not govern

#### Scenario: No promoted doc-health specification is in scope
- **WHEN** no repository in the run's scope carries a promoted `doc-health` specification
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted
