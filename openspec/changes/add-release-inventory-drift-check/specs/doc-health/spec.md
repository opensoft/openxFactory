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
inventory and the blobs it names — and likewise takes neither document list and
moves no census, word count, canon-share figure, inventory entry, or catalog
record.

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

## ADDED Requirements

### Requirement: Release-inventory drift
The release-inventory drift family SHALL compare, for every repository in
scope that declares a contract bundle, each member of that bundle's release
digest inventory against the blob the repository carries at the checked commit,
and report where they differ.

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
- **WHEN** a repository in scope carries no declared contract bundle, or the declared bundle's inventory file is absent
- **THEN** the family MUST report a skip naming the reason, never an empty pass

#### Scenario: Version control cannot answer
- **WHEN** the blobs at the checked commit cannot be read from version control
- **THEN** the family MUST report a skip rather than fall back to working-tree bytes, because an uncommitted edit is not drift from the declared bundle
