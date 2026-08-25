# doc-health Specification Delta

## MODIFIED Requirements

### Requirement: Deterministic check families
The doc-health deterministic pass SHALL implement nineteen check families over
the whole factory family's governance corpus: status validity, standard
backing, ratified provenance, succession integrity, staged-topic template,
location conformance,
record immutability, staged/candidate aging, register-lifecycle consistency,
tag hygiene, submodule pin drift, contract-copy drift, notebook projection
drift, document catalog, ideation routing, proposal origin, client
identity roster composition, promotion fidelity, and release-inventory drift.
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
an advisory report. Four of the nineteen — status validity, standard backing,
ratified provenance, and succession integrity — SHALL additionally read the
lifecycle scan set this capability declares, so that a lifecycle header
carried by a document outside the governed corpus is still checked; the other
fifteen families and every corpus census, word count, canon-share figure,
shared-inventory entry, and catalog record SHALL be computed from the
governed corpus alone and MUST NOT move because the lifecycle scan set
exists. The promotion fidelity family reads archived spec DELTAS and promoted
SPECS — bodies rather than headers — and therefore takes neither the governed
corpus nor the lifecycle scan set as its document list; it moves no census,
word count, canon-share figure, inventory entry, or catalog record either. The
release-inventory drift family reads CONTRACT ARTIFACT BYTES — a release digest
inventory and the blobs it names — and likewise takes neither document list,
and it moves no census, word count, canon-share figure, inventory entry, or
catalog record.


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
spec; only the first scenario differs from canon, by the one `AND` bullet this
change adds for the new family.

#### Scenario: A run executes the check families
- **WHEN** a doc-health run executes
- **THEN** every check family MUST run over every family repo the aggregation repo pins (openxFactory and each DomainxFactory), plus the per-repo validators as a preflight
- **AND** document catalog MUST validate the shared inventory plus promoted specs and the aggregation-hosted catalog snapshots as its owning requirement defines
- **AND** ideation routing MUST additionally inspect the aggregation root placement boundary and resolve explicitly referenced pinned repositories as its owning requirement defines
- **AND** proposal origin MUST validate active and archived proposal packets, support manifests, and staging-header linkage as its owning requirements define
- **AND** client identity roster composition MUST assemble the per-client roster fragments published by each pinned domain repository as its owning requirement in `client-identity-roster` defines
- **AND** promotion fidelity MUST compare each repository's archived spec deltas against its promoted specs as its owning requirement below defines
- **AND** release-inventory drift MUST compare each repository's declared bundle inventory against the blobs it names as its owning requirement below defines
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

### Requirement: Release-inventory drift
The release-inventory drift family SHALL compare, for every repository in
scope that declares a contract bundle, each member of that bundle's release
digest inventory against the blob the repository carries at the checked commit,
and report where they differ.

THE COMPARISON SHALL COVER THE RECORDED `git_mode` AS WELL AS THE DIGEST. An
inventory entry records both, and a mode-only change — an executable bit set or
cleared on a validator — leaves the blob bytes and therefore the digest
identical. A family that compared digests alone would report a validator whose
executability had changed as MATCHING, which is the silent-drift class this
whole capability exists to close. The canonical verifier already distinguishes
them (`HGR-RELEASE-DIGEST-MISMATCH` and `HGR-RELEASE-MODE-MISMATCH`); this
family SHALL NOT be weaker than the verifier whose gap it exists to cover.

The obligation being checked belongs to `release-surface-integrity` ("The
declared bundle describes the release surface"), the capability this change
adds; this requirement defines only how doc-health checks it, in the same
by-reference relationship tag hygiene already has with `document-lifecycle`'s
marker grammar.

THE FAMILY SHALL SPLIT ITS FINDINGS IN TWO, because the two states are
different facts and reporting them alike would make the common one hide the
serious one. NON-EDITORIAL drift — any member other than the changelog, the
manifest and the README — SHALL be reported at `error`, because a normative
contract's bytes moved while the repository went on declaring a bundle that
describes different bytes. EDITORIAL drift — those three members and nothing
else — SHALL be reported at `info`, because it is the expected bounded state
between cuts and the next cut re-baselines it. Both verdicts are Brett's ruling
of 2026-08-24: `info` rather than `warning`, so a condition nobody should act on
does not hold a permanent yellow row in every report.

DIGESTS SHALL BE COMPUTED OVER RAW BYTES, never over decoded text. The
inventory's own identity rule is the SHA-256 of raw Git blob bytes and names
text canonicalization as an invalid digest source, so a family that read the
blob as text would compute a different number and report drift that does not
exist on any file whose bytes are not pure ASCII.

THE FAMILY SHALL NOT BE CLASSIFIED `contested`, and the reason is structural
rather than a taste call. Both of its findings are RESOLVED BY A RELEASE CUT,
which is exactly the act that makes them vanish between reports — and a
`contested` finding that vanishes without citing a change or a disposition
against its finding id is re-emitted as an `error` under the uncited-resolution
rule. Classifying this family `contested` would therefore turn every correctly
performed release cut into a new error, which is an enforcement channel
arriving through the back door on precisely the runs that prove the family
working. Severity and resolution class are one later decision, taken together
by ruling.

The family SHALL be reported as skipped, never silently omitted, where a
repository declares no bundle, where the declared bundle's inventory file is
absent, or where version control cannot answer for the blobs.

#### Scenario: A non-editorial member has drifted
- **WHEN** a member other than the changelog, the manifest or the README differs from the digest the declared bundle's inventory records
- **THEN** the family MUST emit an `error` finding naming that member and the declared bundle
- **AND** the action MUST name a release cut through the bundle realization order, never a hand-edit of the inventory

#### Scenario: Only editorial members have drifted
- **WHEN** the only differing members are the changelog, the manifest and the README
- **THEN** the family MUST emit `info` findings only, and the run MUST NOT redden under a gate set to `error` or `critical`

#### Scenario: The tree matches the declared bundle exactly
- **WHEN** every inventory member matches its recorded digest
- **THEN** the family MUST emit no finding

#### Scenario: A repository declares no bundle
- **WHEN** a repository in scope carries no declared contract bundle at all
- **THEN** the family MUST report a skip naming the reason, never an empty pass

#### Scenario: A declared bundle has no inventory
- **WHEN** a repository DECLARES a bundle and that bundle's inventory file is absent
- **THEN** the family MUST emit an `error`, never a skip — a declaration naming an inventory that does not exist is an INVALID RELEASE DECLARATION, not an absent capability, and it is what a mistyped bundle name or a half-created release looks like
- **AND** the canonical verifier already reports this condition as `HGR-RELEASE-INVENTORY-MISSING` rather than declining to answer

#### Scenario: An inventory member is absent at the commit
- **WHEN** a member the declared bundle's inventory names does not exist at the checked commit
- **THEN** the family MUST report it as NON-EDITORIAL DRIFT at `error`, never as a skip — a deleted normative member is the strongest form of the drift this family exists to catch, and a skip would make deletion indistinguishable from unavailability
- **AND** this MUST hold even where the underlying blob read degrades to a null result, so the family MUST distinguish "this path is absent at this commit" from "version control could not be consulted"

#### Scenario: Version control cannot answer at all
- **WHEN** the git dependency is unavailable, or the checked commit itself cannot be resolved
- **THEN** the family MUST report a skip rather than fall back to working-tree bytes, because an uncommitted edit is not drift from the declared bundle
- **AND** the skip MUST NOT be used for any per-member absence, which the scenario above governs
