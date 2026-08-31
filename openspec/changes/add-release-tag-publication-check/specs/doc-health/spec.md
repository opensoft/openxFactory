# doc-health Specification Delta

## ADDED Requirements

### Requirement: Release-tag publication
The release-tag-publication family SHALL report, for every repository in scope that declares a contract bundle at or above the version where mandatory tag publication begins, whether that bundle has a published ANNOTATED tag, and whether that tag peels to a commit that declares the bundle.

The obligation being checked belongs to `docs/contract-versioning-policy.md` —
"a bundle is not published until its tag exists", and "the tag SHALL point to
that realized commit". This requirement defines only how doc-health checks it,
in the same by-reference relationship `tag-hygiene` already has with
`document-lifecycle`'s marker grammar and `Release-inventory drift` has with
`release-surface-integrity`.

THE FAMILY SHALL BE DISTANCE-GRADED RATHER THAN IMMEDIATE, because the declaring
commit and the tag are two acts by two actors and the interval between them is
legitimate. A cut declares the bundle; the repository owner publishes the tag
afterwards. A family that fired the moment the manifest moved would redden every
correctly performed release, and a family nobody can leave green is a family
that gets configured away. Distance SHALL be measured in FIRST-PARENT COMMITS ON
PUBLISHED `main` since the earliest commit declaring the bundle, never in wall
time, because landings are what the policy's own retro-publication rule counts
and wall time punishes a quiet week.

THE THRESHOLD SHALL DEFAULT TO FIVE FIRST-PARENT LANDINGS, ruled by Brett Heap on
2026-08-31. It is a threshold default in the sense this capability already gives
that term, configurable in the same place the aging defaults are, and the ruled
number is what an unconfigured run uses. The calibration it answers to:
`contract-v2.3` sat untagged across six first-parent landings before a human
noticed it, so a threshold above five would have stayed silent through the
recurrence this family exists to catch.

THE TWO FAILURE STATES SHALL BE REPORTED IN DIFFERENT WORDS AND AT DIFFERENT
SEVERITIES. An ABSENT tag is an incomplete release — the common case, and the
one the window above exists to tolerate for a while. A tag that exists and peels
to a commit NOT declaring the bundle is a MISPLACED tag: it satisfies every
check that asks only whether a tag exists, it is what consumers will pin, and it
is worse than absence because it looks like completion. Reporting them alike
would let the common one hide the serious one.

THE FAMILY SHALL NOT FIRE BELOW THE ENFORCEMENT LINE. `contract-v1.0` through
`contract-v1.6` predate mandatory annotated tags and carry none by design, as
the changelog's own legacy baseline note records. A family that reported them
would emit seven permanent findings nobody may act on, which is how a report
teaches its readers to stop reading it.

A LIGHTWEIGHT TAG SHALL NOT SATISFY THE OBLIGATION. The policy requires an
ANNOTATED tag; a lightweight ref carries no tagger, no date and no message, and
accepting one would let the weaker object silently discharge the stronger
requirement.

The family SHALL be reported as skipped, never silently omitted, where a
repository declares no bundle at all, or where version control cannot answer —
an unavailable git dependency, tag refs that cannot be listed, or a declaring
commit that does not resolve. THE SKIP IS RESERVED FOR "THE QUESTION COULD NOT
BE ASKED": a declared bundle whose tag is simply absent is an ANSWER, and is
reported by the scenarios below rather than skipped.

THIS FAMILY DOES NOT PROVE THE TARGET IS THE EARLIEST DECLARING COMMIT, and the
residue is disclosed rather than hidden. The policy's target is "the EARLIEST
FIRST-PARENT COMMIT on published `main` that DECLARES the bundle and at which
`verify-commit` PASSES"; the second conjunct is a digest verification per
candidate and is out of scope here. A tag on a LATER declaring commit therefore
passes this family and remains a defect under the policy.

#### Scenario: The declaring commit is still the published tip
- **WHEN** a repository declares a bundle at or above the enforcement line, that bundle has no published annotated tag, and the earliest commit declaring it is still the tip of published `main`
- **THEN** the family MUST emit no finding, because the cut has only just landed and the owner's tag act legitimately follows it
- **AND** the family MUST NOT record this as a pass that discharges the obligation, which remains owed

#### Scenario: Landings have accumulated on an untagged declared bundle
- **WHEN** the bundle has no published annotated tag and further first-parent commits have landed on published `main` above the earliest commit declaring it, up to and including the configured threshold
- **THEN** the family MUST emit a `warning` naming the bundle, the declaring commit, and how many first-parent landings have accumulated
- **AND** the action MUST name publishing the annotated tag at the commit the policy's rule identifies, never editing the manifest, the changelog or the inventory to match the absence

#### Scenario: An untagged declared bundle passes the threshold
- **WHEN** the accumulated first-parent landings exceed the configured threshold
- **THEN** the family MUST emit an `error`, because a bundle being consumed while unpublished is the state the policy calls a breach rather than an exception
- **AND** the finding MUST say that the bundle is NOT PUBLISHED in the policy's own terms, so no reader infers from its presence in the manifest that it was released

#### Scenario: The declared bundle carries an annotated tag on a declaring commit
- **WHEN** the bundle has a published annotated tag and that tag peels to a commit whose manifest declares that same bundle
- **THEN** the family MUST emit no finding

#### Scenario: A tag exists but peels to a commit that does not declare the bundle
- **WHEN** the bundle has a published annotated tag and the commit it peels to does not declare that bundle
- **THEN** the family MUST emit an `error` in DIFFERENT WORDS from the absent-tag findings, naming it a MISPLACED tag and naming both the commit it peels to and the bundle that commit actually declares, if any
- **AND** this MUST NOT be graded by distance, because a misplaced tag is not a release in progress and no interval makes it correct

#### Scenario: The published tag is lightweight rather than annotated
- **WHEN** a ref of the bundle's tag name exists but is not an annotated tag object
- **THEN** the family MUST emit an `error` naming the ref as lightweight, never treat it as satisfying the obligation, and never report it in the absent-tag words

#### Scenario: A bundle below the enforcement line
- **WHEN** the declared bundle is below the version at which mandatory tag publication begins
- **THEN** the family MUST emit no finding, and MUST NOT report the legacy sequence's untagged bundles at any severity

#### Scenario: A repository declares no bundle
- **WHEN** a repository in scope carries no declared contract bundle at all
- **THEN** the family MUST report a skip naming the reason, never an empty pass

#### Scenario: Version control cannot answer
- **WHEN** the git dependency is unavailable, the repository's tag refs cannot be listed, or the declaring commit cannot be resolved
- **THEN** the family MUST report a skip naming which of those it was, never a finding
- **AND** the family MUST NOT read a tag's existence from a local ref alone where the published refs could not be consulted, because an unpushed local tag is not a published tag

## MODIFIED Requirements

<!-- Restated WHOLE, per the archive rule that a MODIFIED delta wholesale-
replaces the requirement it names: all eight scenarios are carried unchanged and
only the enumeration moves. The numerals and the list are what `family
enumeration` measures against the code registry, and that family exists because
this exact restatement was left incomplete three times in three days, all three
catches human. -->

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement twenty-three check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, client
identity roster composition, promotion fidelity, release-inventory drift,
duplicate packet, family enumeration, modified-block currency, and release-tag
publication.
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
an advisory report. Four of the twenty-three — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
nineteen families and every corpus census, word count, canon-share figure,
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
neither document list and moves none of those figures. The modified-block
currency family reads ACTIVE CHANGE DELTAS, the promoted SPECS they have not yet
replaced, and each active change's own `proposal.md` — the last read only to
resolve whether one active writer declares its deltas relative to another, which
`release-realization` governs — so it likewise takes neither the governed corpus
nor the lifecycle scan set as its document list, and it moves no census, word
count, canon-share figure, inventory entry, or catalog record either.
The release-tag publication family reads the DECLARED BUNDLE and the
repository's PUBLISHED TAG REFS — a manifest field and a set of git refs,
neither of them a governed-corpus document — so it likewise takes neither the
governed corpus nor the lifecycle scan set as its document list, and it moves no
census, word count, canon-share figure, inventory entry, or catalog record
either.

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
- **AND** modified-block currency MUST compare each active change's `## MODIFIED Requirements` blocks against the promoted requirements they replace as its owning requirement below defines
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
