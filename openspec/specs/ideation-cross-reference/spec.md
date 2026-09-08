# ideation-cross-reference Specification

## Purpose

Govern the generated cross-stage index over ideation — organized by topic
cluster rather than by file, with brainstorm, staging and archived members
bootstrapped from `Topics:` and `Target capabilities:` headers — and the
canonical possibles register it consolidates from `Possible feats:`
declarations: one entry per possible, held in `latent`, `picked`, `rejected`
or `superseded` state, with many-to-many edges to every cluster claiming it
and a reason plus citation on any terminal transition. Carry the judgements
about a cluster beside its members: the extension-fit note naming a promoted
capability or explicitly stating there is none, and the three independent
Hermes-tier readiness scores — domain, company, project — whose minimum
drives the "propose for authorization" flag. Hold every producer writing
here to the same evidence contract and to recommendation rather than action:
human-seen cluster intake, the bounded AI derivation lane, and the nightly
readiness pass write only the index and their own evidence artifacts,
orchestration owns every identifier and hash, derived possibles stay a
visibly distinct class until a human disposes them one way, and nothing in
this capability moves, promotes or proposes a document. Keep committed
derivation pins resolvable from `main` or the retention namespace so an
artifact's claim about the corpus state it was derived from stays
verifiable.
## Requirements
### Requirement: Possibles register consolidation
The cross-reference index SHALL consolidate every `Possible feats:`
declaration into the canonical possibles register, one register entry per
possible with explicit many-to-many edges to its claiming topic clusters —
the same bootstrap posture as the index's tag sources, with no third
standalone register file. Each possible SHALL carry exactly one state:
`latent` (enumerated, unpicked — backlog, not failure), `picked` (citing
the staged topic's staging ID and inheriting the change ID at the proposal
gate), `rejected`, or `superseded`; `rejected` and `superseded` SHALL
require a recorded reason plus a citation, mirroring the contested-finding
disposition rule.

#### Scenario: Declarations are consolidated
- **WHEN** the index pass runs over documents carrying `Possible feats:` sections
- **THEN** the register carries one canonical entry per possible with edges to every claiming cluster

#### Scenario: A possible is rejected without citation
- **WHEN** a register entry transitions to `rejected` or `superseded` without a recorded reason and citation
- **THEN** strict register validation MUST fail the transition

#### Scenario: A picked possible's topic crosses the proposal gate
- **WHEN** the staged topic cited by a `picked` possible becomes an OpenSpec change
- **THEN** the pick citation inherits the change ID while retaining the original staging ID

### Requirement: Human-seen cluster intake
An ad-hoc workbench reference set matching no machine cluster SHALL be
accepted as a human-seen cluster proposal into the same recommendation
queue as machine clustering, carrying the full evidence contract already
used by the panel's scores — committed source revision, passage hash and
section reference, rationale, confidence, alternatives, and
`pending_review` disposition. Human-seen submissions MUST NOT bypass
review: they are recommendations disposed by the same authorities as
machine suggestions.

#### Scenario: A human submits an ad-hoc set
- **WHEN** a workbench user submits a reference set as a human-seen cluster
- **THEN** the submission enters the recommendation queue with the full evidence contract and `pending_review` disposition

#### Scenario: A submission lacks evidence
- **WHEN** a human-seen submission arrives without the complete evidence contract
- **THEN** it MUST be rejected before persistence

#### Scenario: A human-seen cluster is accepted
- **WHEN** the disposing authority accepts a human-seen cluster
- **THEN** it becomes a topic cluster in the index like any machine-derived cluster, recording its human-seen provenance

### Requirement: Derived possible register entry and provenance
Every possibles-register entry the derivation lane proposes SHALL carry
`origin: ai-derived`, a `derivation` block naming the worker run (correlation
id, worker profile, and prompt-contract version), and machine
`disposition: pending_review`, and SHALL cite the source material it was derived
from through the register's existing evidence fields — at least one
`claiming_clusters` topic-cluster edge and at least one `supporting_evidence`
passage pin — so a derived possible is never an unsourced assertion.

The `origin` and `derivation` fields are an ADDITIVE, forward-compatible delta to
the `ideation-possibles-register` kernel, modelled one-for-one on the topic
entry's `origin` + `human_seen` intake pair: a human-authored possible carries no
`origin` (defaulting to human-authored) and is unaffected, so the delta requires
no `contract_schema_version` bump. The worker-run identity lives in the
`derivation` block, not in `ingestion_provenance`, which keeps its `Possible
feats:` meaning; a derived entry's required `provenance` cites the primary source
member document and the cluster context it was derived from.

#### Scenario: A possible is derived
- **WHEN** the lane proposes a candidate possible from a topic cluster
- **THEN** the register entry MUST carry `origin: ai-derived`, a `derivation` block naming the worker run, `disposition: pending_review`, at least one `claiming_clusters` edge, and at least one `supporting_evidence` pin

#### Scenario: A derived entry omits its worker run
- **WHEN** a proposed derived entry lacks the `derivation` worker-run identity or its `pending_review` disposition
- **THEN** it MUST be rejected before persistence and no register entry is created

#### Scenario: A derived entry cites no source
- **WHEN** a proposed derived entry carries neither a `claiming_clusters` edge nor a `supporting_evidence` pin
- **THEN** it MUST be rejected as an unsourced possible

#### Scenario: A human-authored possible is unaffected
- **WHEN** the register holds a human-authored possible with no `origin` field
- **THEN** it remains valid and defaults to human-authored without a `derivation` block

### Requirement: Orchestration-authoritative identifiers and hashes
The tool-less model worker MUST NOT compute, invent, or transcribe any
machine-precision value — register ids, correlation ids, content or passage
hashes, revisions, or counts — in its proposed possibles; orchestration SHALL
compute every such value and treat its own values as authoritative, and any
worker-supplied precision value that disagrees with the orchestration-computed
value SHALL void the affected proposals rather than persist a corrupted entry.

This carries the document-cataloger lane's contract forward: a worker that
mis-copied a single hex character of a content hash voided twenty-five
classifications. The worker proposes titles, claims, and rationale prose only;
identity and evidence pins are stamped by orchestration.

#### Scenario: Worker output contains a precision value
- **WHEN** worker output includes a register id, hash, revision, or count
- **THEN** orchestration MUST discard the worker value and substitute its own computed value

#### Scenario: A worker value disagrees with orchestration
- **WHEN** a worker-supplied precision value does not match the orchestration-computed value for the same entry
- **THEN** the affected proposals MUST be voided and reported, never persisted

### Requirement: One-way derived-possible disposition on the gate console
A derived possible SHALL remain `pending_review` until a human authority disposes
it on the gate console, and its disposition SHALL be one-way — accepted,
rejected, or deferred — never edited back to `pending_review` and never
auto-promoted by the lane.

An accepted derived possible becomes a first-class register possible in `latent`
state, retaining its `origin: ai-derived` provenance exactly as an accepted
human-seen cluster retains `origin: human-seen`, and thereafter follows the
normal pick lifecycle. A rejected derived possible is recorded in `rejected`
state with the required reason and citation drawn from the disposition,
preserving its audit trail so the same candidate is never silently re-derived; a
previously rejected possible that becomes viable again is a NEW entry with a new
`id`, never a resurrection. The lane itself creates no proposal, moves no
document, and changes no lifecycle state.

#### Scenario: A derived possible is accepted
- **WHEN** a human authority accepts a `pending_review` derived possible on the gate console
- **THEN** it becomes a `latent` register possible retaining `origin: ai-derived`
- **AND** proposing remains a deliberate authorized step outside this lane

#### Scenario: A derived possible is rejected
- **WHEN** a human authority rejects a `pending_review` derived possible
- **THEN** it is recorded `rejected` with the disposition's reason and citation
- **AND** it MUST NOT re-enter `pending_review` and MUST NOT be silently re-derived

#### Scenario: The lane never promotes
- **WHEN** the derivation lane runs
- **THEN** it MUST NOT accept, pick, or promote any possible autonomously — every disposition is a human act on the gate console

### Requirement: Bounded derivation worker, immutable evidence, and concurrency-protected merge
The derivation worker SHALL run as a distinct, bounded, read-only
artifact-in/artifact-out Omnigent lane with its own worker profile, prompt, and
output schema, receiving no repository credentials and no write authority, and
its output MUST NOT block deterministic work: an offline, unauthorized, partial,
invalid, timed-out, or failed worker run MUST leave the deterministic pass and
its report unaffected and the possibles register unchanged.

A watchdog SHALL report and cancel a derivation child queued longer than ten
minutes or running longer than thirty minutes. Validated derivation output SHALL
be persisted as immutable evidence under the factory identity and SHALL merge
into `ideation/cross-reference.yaml`'s `possibles_register` only through a later
main run, under concurrency protection that refuses a stale overwrite of a
register a concurrent run has already advanced. The merge preserves register
`id` uniqueness and never edits a disposed entry.

#### Scenario: The worker is offline
- **WHEN** the derivation worker is unavailable or fails
- **THEN** the deterministic pass and its report MUST land unaffected and no derived possible is persisted

#### Scenario: A child exceeds its bounds
- **WHEN** a derivation child is queued beyond ten minutes or runs beyond thirty minutes
- **THEN** the watchdog MUST report and cancel it

#### Scenario: Output merges on a later run
- **WHEN** a derivation child returns after its dispatching run has closed
- **THEN** its immutable evidence MUST be merged by a later main run and the closed run's records MUST NOT be edited

#### Scenario: A concurrent run advanced the register
- **WHEN** a merge would overwrite a `possibles_register` a concurrent run has already advanced
- **THEN** the merge MUST refuse the stale overwrite rather than clobber the newer state

### Requirement: Derived possibles are a distinct class until disposed
Undisposed derived possibles SHALL be contractually and visually distinct from
human-picked possibles wherever the index is consumed: their cross-class edges
SHALL carry a non-`indexed` edge class (`inferred` or `synthesized`) in the
dashboard/WHEEL realization data contract, and no consumer SHALL render or count
an undisposed derived possible as human-picked, indexed data.

Real derived possibles populating the register replace the WHEEL's
synthesized-and-demo-marked placeholders (the "possibles honesty rule"); once a
derived possible is disposed accepted it MAY be treated as real register data,
but until then it is never confusable with indexed edges.

#### Scenario: The WHEEL renders derived possibles
- **WHEN** the WHEEL renders a possibles column containing undisposed derived possibles
- **THEN** their possible-to-cluster edges MUST carry a non-`indexed` class and be visually distinct from indexed human-picked edges

#### Scenario: A consumer counts possibles
- **WHEN** a consumer reports possible counts or a ranked plan
- **THEN** undisposed derived possibles MUST be excluded from human-picked totals and from any ranked plan

### Requirement: Non-mutating derivation bound
The derivation lane SHALL be non-mutating over source content: it writes and
updates only the cross-reference index (the `possibles_register` section) and its
evidence artifacts. It MUST NOT edit, move, promote, or delete any brainstorm,
staging, or archived document; archived material is read-only reference for
deriving candidates, and no third standalone possibles file is created.

#### Scenario: The lane runs
- **WHEN** a derivation pass completes and merges
- **THEN** the only repository writes are the `possibles_register` section of the index and the lane's evidence artifacts

#### Scenario: The lane observes a source defect
- **WHEN** the lane observes a defect in a member document while deriving
- **THEN** it records the observation in evidence and MUST NOT modify the document

### Requirement: Cross-reference index contract
openxFactory SHALL maintain one unified cross-stage cross-reference index at
the ideation level (`ideation/cross-reference.md`), organized by topic
cluster rather than by file. Each topic entry SHALL list every related
document across `ideation/brainstorm/`, `ideation/staging/`, and archived
change material, each member carrying a stage column value. Cluster
membership SHALL bootstrap from the `Topics:` and `Target capabilities:`
header fields already required by the document lifecycle; controlled
`document-cataloging` tags SHALL be folded in as an additional membership
source once that capability realizes, and the index MUST NOT block on the
catalog. The index is a generated projection over governed documents;
`ideation/staging/INDEX.md` remains the staged-file inventory, and the two
files MUST NOT duplicate each other's purpose.

#### Scenario: A topic spans stages
- **WHEN** related material exists in brainstorm, staging, and an archived change
- **THEN** the index MUST carry one topic entry listing every member with its stage value, not one entry per stage

#### Scenario: The catalog realizes later
- **WHEN** `document-cataloging` tags become available
- **THEN** they join header fields as an additive membership source without a schema break
- **AND** entries built from headers alone remain valid

#### Scenario: The inventory and the index are confused
- **WHEN** a staged file is added, removed, or promoted
- **THEN** `staging/INDEX.md` is updated under its own maintenance rule and the cross-reference index is regenerated
- **AND** neither file restates the other's content beyond member references

### Requirement: Extension-fit citation
Every topic entry SHALL carry an extension-fit note stating whether a
promoted capability already exists that the cluster would extend. A fit
note MUST name the specific promoted spec or capability; a pointer to an
archived change folder alone does not satisfy the citation. Where no
promoted fit exists, the note SHALL say so explicitly rather than being
omitted.

#### Scenario: A promoted fit exists
- **WHEN** a topic cluster would extend a promoted capability
- **THEN** its fit note MUST name that spec or capability and how the cluster extends it

#### Scenario: A fit note cites only an archive folder
- **WHEN** a fit note points at an archived change folder without naming the promoted spec or capability
- **THEN** the readiness lane MUST emit an `ideation-readiness` finding against the entry

#### Scenario: No promoted fit exists
- **WHEN** nothing promoted relates to the cluster
- **THEN** the entry MUST state that explicitly, distinguishing "no fit" from "fit check not performed"

### Requirement: Hermes-tier readiness panel
Three independent reviewers SHALL score every topic cluster from 1 to 10
for proposal readiness, one per tier: the domain tier is the owning
DomainxFactory's Domain Hermes authority; the company tier is the
openxFactory ratify authority; the project tier is the engineering
buildability lens — whether codexFactory's feature decomposition could turn
the cluster into a buildable Spec Kit feature DAG today. Each tier score
SHALL carry the same evidence-backed recommendation contract the
document-cataloger and ideation-organizer already use — committed source
revision, passage hash and section reference, rationale, confidence,
alternatives, and `pending_review` disposition; the panel MUST NOT
introduce a divergent rationale format. A tier that cannot score a cluster
SHALL be recorded as unscored with its reason.

#### Scenario: A cluster is scored
- **WHEN** the readiness pass evaluates a topic cluster
- **THEN** the entry MUST carry three tier scores, each with its own evidence-contract rationale
- **AND** each score cites the committed source revisions it judged

#### Scenario: A tier cannot score
- **WHEN** a tier's authority cannot be resolved for a cluster (for example no owning domain)
- **THEN** the entry records that tier as unscored with the reason
- **AND** the recommendation gate MUST NOT fire for that cluster

#### Scenario: Worker output violates the evidence contract
- **WHEN** a tier score arrives without a complete evidence-contract rationale
- **THEN** the score MUST be rejected before persistence and the entry left at its prior state

### Requirement: Readiness recommendation gate
A topic SHALL be flagged "propose for authorization" only when the minimum
of the three tier scores is at least 8. The flag SHALL always be a
recommendation carrying `pending_review` disposition — never an autonomous
action: the pass MUST NOT create proposals, move documents, or change any
lifecycle state. A wide spread between tier scores SHALL be surfaced as a
flagged conflict even when the minimum stays below the threshold.

#### Scenario: All tiers agree the cluster is ready
- **WHEN** every tier scores a cluster 8 or higher
- **THEN** the entry MUST be flagged "propose for authorization" as a `pending_review` recommendation for the disposing authority

#### Scenario: One tier disagrees
- **WHEN** two tiers score 10 and one scores below 8
- **THEN** the gate MUST NOT fire — no tier can be outvoted into silence

#### Scenario: Tiers diverge below threshold
- **WHEN** tier scores spread widely while the minimum stays below 8
- **THEN** the entry MUST carry a flagged conflict recording the divergence as signal

#### Scenario: A recommendation is disposed
- **WHEN** a human authority accepts or rejects a flagged recommendation
- **THEN** the disposition is recorded against the entry and proposing remains a deliberate, authorized step outside this capability

### Requirement: Non-mutating execution bound
The readiness pass SHALL be non-mutating over source content: it writes and
updates only the cross-reference index and its evidence artifacts. It MUST
NOT edit, move, promote, or delete any brainstorm, staging, or archived
document; archived material is read-only reference for the extension-fit
check.

#### Scenario: The pass runs
- **WHEN** a readiness pass completes
- **THEN** the only repository writes are the index file and its evidence artifacts

#### Scenario: A source document needs correction
- **WHEN** the pass observes a defect in a member document
- **THEN** it records the observation in the entry's evidence and MUST NOT modify the document

### Requirement: Nightly scheduling and snapshot consistency
The readiness pass SHALL run as a nightly doc-health lane after the
deterministic pass, consuming that run's document inventory so every score
cites the same corpus snapshot the report describes. A skipped or failed
readiness pass MUST be reported as skipped, MUST NOT affect deterministic
results, and MUST NOT cause prior recommendations to be treated as
resolved.

#### Scenario: The nightly run executes
- **WHEN** the nightly doc-health run completes its deterministic pass
- **THEN** the readiness lane runs against exactly that pass's inventory
- **AND** the dated report links the updated index and evidence

#### Scenario: The lane is unavailable
- **WHEN** the readiness worker is skipped, offline, or fails
- **THEN** the run reports the lane as skipped and deterministic results land unaffected
- **AND** recommendations absent only because the lane did not run are not treated as disposed

### Requirement: A committed derivation pin stays resolvable
A committed artifact SHALL pin, as its derivation source, only a repository
commit reachable from `main` or from a published retention ref, at all times
that the artifact stands on `main`.

THE RETENTION NAMESPACE IS `refs/retention/pins/<full-sha>`: one ref per
retained commit, named for the full forty-character object name of the commit it
retains, published on the repository's own remote. Naming the namespace rather
than admitting any declared ref is what makes the repair act DETERMINISTIC — a
reader resolving a pin knows exactly one place to look, a verification knows
exactly one ref set to consult beside `main`, and the ref's own name states
which commit it exists to keep so that no separate declaration can drift from
it. A retention ref outside that namespace does not satisfy this requirement,
because a ref nobody can predict the name of is not reachable in the sense a
reader needs.

An unreachable pin is a DEFECT IN THE ARTIFACT, not staleness in it, and the
distinction is the whole of this requirement. A pin naming an older commit that
`main` still reaches is legal and expected: the artifact says "I was derived
from the corpus as it stood at X", a reader reconstructs the corpus at X, and
the provenance claim is verifiable even when the corpus has since moved. That
is the ordinary condition of every generated projection between regenerations,
and nothing here makes it a finding. A pin naming a commit no ref reaches makes
the same sentence unverifiable BY ANYONE: there is no state to reconstruct, so
the artifact's central claim about itself cannot be checked, confirmed, or
refuted. Reporting that as staleness understates it by a category.

The pinned commit's reachability SHALL be judged against refs, not against a
particular clone's object store. A commit an ancestor walk from `main` reaches
is conforming even in a clone that has not fetched it; a commit no ref reaches
is non-conforming even while it survives in some working clone's object store,
because that survival is an accident of local garbage collection rather than a
property of the repository.

The class this requirement reaches is REPO-LOCAL COMMIT PINS: a commit of the
same repository the artifact is committed to, recorded by that repository's own
generators as the state the artifact was derived from. `generation.source_revision`
on the cross-reference index and `source_revision` on this capability's
derivation and readiness evidence records are the members this capability owns.
Cross-repository pins are OUT and are governed elsewhere: an aggregation
gitlink, a `pinned_contract_manifest` entry, a release digest, and a container
image digest all name state in a repository other than the one recording them,
and their reachability question is answered against a different remote by a
different authority.

#### Scenario: The pin names an older commit that main still reaches
- **WHEN** a committed artifact pins a commit that is an ancestor of `main` but is no longer its tip
- **THEN** no finding is emitted under this requirement, because the pinned state is still reconstructible and staleness between regenerations is legal
- **AND** the artifact's provenance claim MUST be treated as verifiable rather than as merely old

#### Scenario: The pin names a commit no ref reaches
- **WHEN** a committed artifact standing on `main` pins a commit that is reachable from no ref, local or remote
- **THEN** it MUST be reported as a defect in that artifact, naming the artifact and the pinned commit
- **AND** it MUST NOT be reported as staleness, deferred to a regeneration schedule, or excused as an environment condition

#### Scenario: The pin resolves only through a retention ref
- **WHEN** a committed artifact pins a commit that `main` does not reach, and a published `refs/retention/pins/<full-sha>` ref names that commit
- **THEN** the artifact is conforming, because the pinned state remains reconstructible by a reader who resolves the pin's own object name in that namespace
- **AND** a retention ref carried under any other name MUST NOT satisfy this requirement, because a ref whose name cannot be derived from the pin is not predictably reachable

#### Scenario: A truncated clone cannot resolve a conforming pin
- **WHEN** a clone's history is shallow or otherwise truncated and cannot resolve a pin that `main` reaches
- **THEN** the condition MUST be reported against the clone rather than against the artifact
- **AND** the artifact MUST NOT be recorded as carrying an unreachable pin on the strength of a local absence

### Requirement: An orphaned pin on an immutable record is repaired by retention, never by editing the record
An orphaned derivation pin on an artifact whose status is `record` SHALL be
repaired by making the pinned commit reachable again, and MUST NOT be repaired
by editing the pin the record carries.

Two rules meet here and only one ordering of them is coherent. This
capability's derivation evidence is persisted as IMMUTABLE evidence, and
`document-lifecycle` makes a content edit to a `record` after capture a
finding in its own right. So the repair that works for a generated projection
— re-derive the body, re-pin, commit — is unavailable for a record: rewriting
the pin would replace one defect with another and would additionally falsify
the record, which exists to say what a run actually read. The pinned commit is
therefore what moves, not the record.

Retention SHALL publish `refs/retention/pins/<full-sha>` on the repository's own
remote, where `<full-sha>` is the full forty-character object name of the
orphaned commit being retained. A local ref does not satisfy this: a pin whose
reachability depends on one machine's object store is unreachable by every other
reader, and the requirement above is not satisfied by it. Deriving the ref's name
from the pin is what makes the repair mechanical — the repairer computes the ref
name rather than choosing it, and a reader resolving the record's pin computes
the same name without consulting anything else. Retention is
also TIME-BOUND in a way no other repair in this repository is: an orphaned
commit survives only until garbage collection reaches it in the last clone
holding it, so a retention that is possible today may be impossible next week.
A packet that observes an orphaned pin on a record SHALL therefore establish
whether the object is still recoverable BEFORE proposing a route, and SHALL
record the answer it measured.

Where the pinned object is no longer recoverable anywhere, the record's bytes
still stand. The resolution SHALL be a SUPERSEDING record that names the loss
and what can and cannot now be verified, plus a disposition for the finding the
unrecoverable pin will keep producing. Silently rewriting the pin, deleting the
record, or leaving the finding unresolved and uncited are all refused: the
first falsifies the record, the second destroys the evidence the record is,
and the third converts a known defect into background noise.

#### Scenario: A record's pin is orphaned and the object is still recoverable
- **WHEN** an artifact with `status: record` carries a derivation pin no ref reaches, and the pinned object is still present in at least one clone
- **THEN** the repair MUST publish `refs/retention/pins/<full-sha>` on the repository's remote for that commit, leaving the record's own bytes unchanged
- **AND** the record MUST NOT be edited to name a different commit

#### Scenario: A record's pin is orphaned and the object is unrecoverable
- **WHEN** the pinned object is present in no clone and cannot be published
- **THEN** the resolution MUST be a superseding record naming the loss and what is no longer verifiable, together with a disposition for the standing finding
- **AND** the original record MUST NOT be edited or deleted to make the finding disappear

#### Scenario: A generated projection's pin is orphaned
- **WHEN** the orphaned pin is carried by a generated artifact that is not a `record` — the cross-reference index and its rendered twin among them
- **THEN** re-deriving the body and re-pinning it is the available repair, under the reproduction obligation the landing rule states
- **AND** the record-retention route is not owed for it, because nothing about a regenerable projection is immutable evidence

#### Scenario: A record's pin is edited in place
- **WHEN** a change edits the `source_revision` a captured record carries, for any reason including repairing an orphaned pin
- **THEN** the edit MUST be reported as a content edit to a `record` after capture
- **AND** the edit MUST NOT be accepted as the repair for the orphaned pin, because it makes the record state something the run did not read

### Requirement: A generator that cannot truthfully pin a commit writes a declared sentinel, never a commit name
A generator recording a repo-local derivation pin SHALL write a commit name ONLY
where that commit describes the content being recorded, and where it cannot, it
MUST write a value drawn from a DECLARED shared sentinel vocabulary — never a
commit name that never described the content, and never an undeclared free-form
string of the generator's own invention.

AN UNTRUE PIN IS WORSE THAN AN UNREACHABLE ONE, and the two defects are not the
same defect wearing different clothes. The promoted obligation next to this one
governs a pin that STOPPED being resolvable: the artifact's claim was true when
it was written, something later made the state unrecoverable, and the repair is
to make the state reachable again. That is not this. A pin stamped from `HEAD`
while the generator reads a dirty working tree names a commit that is perfectly
reachable and perfectly wrong — it says "I was derived from the corpus as it
stood at X" about content no commit ever held. A reader who resolves it gets an
answer, checks nothing, and is misled precisely because the pin looks healthy.
Neither the reachability rule nor its retention repair reaches this, because
nothing about the object is missing. Neither promoted requirement is restated or
modified here; this states the obligation that runs before either of them can
apply.

A SENTINEL IS A PROVENANCE CLAIM, NOT AN ABSENCE OF ONE. "This was taken from a
working tree that was not committed" is a statement a reader can act on: it says
the content is unreconstructible from the repository, names why, and stops the
reader from believing the artifact was derived from a state anybody can
reproduce. That is strictly more than a commit name that resolves to the wrong
tree, and strictly more than a key nobody wrote. The vocabulary therefore
carries one declared value PER CONDITION rather than a single "no pin" value:
content read from an uncommitted working tree, a derivation performed outside
any repository context, a repository whose state could not be read at all, and a
projection composed from several sources with no single source revision are four
different facts about how the artifact came to be, and collapsing them loses the
part a reader needs.

THE VOCABULARY IS SHARED ACROSS EVERY GENERATOR, and that is the whole of what
makes it a vocabulary rather than a habit. One condition SHALL have one declared
spelling, used by every generator that stamps a repo-local derivation pin, so
that a reader meeting the value in an artifact they have never seen knows what
it means without reading that artifact's generator, and so that a consumer
guarding on the value guards on the same string everywhere. A spelling invented
per lane is invisible to every consumer written against a different lane's
spelling, and a consumer that misses a sentinel treats it as a pin.

A SENTINEL IS NEVER A LICENCE TO SKIP A PIN THAT WAS AVAILABLE. Where the
generator can name a commit that truthfully describes the recorded content, it
SHALL write that commit; writing a sentinel to avoid resolving the question is a
provenance claim that is itself false, and the verification cannot tell it from
an honest one.

#### Scenario: The generator reads a working tree that is not committed
- **WHEN** a generator records a derivation pin for content it read from a working tree carrying uncommitted changes to that content
- **THEN** it MUST write the declared sentinel for that condition rather than the current `HEAD`, because `HEAD` would name a commit that never held the content being recorded
- **AND** the resulting artifact MUST NOT be treated as carrying a commit pin at all

#### Scenario: The working tree is clean
- **WHEN** a generator records a derivation pin for content that is committed at the revision it is reading
- **THEN** it MUST write that commit name exactly as before, and nothing in this requirement changes the pin, the key, or the artifact
- **AND** the reachability obligation applies to that pin unchanged

#### Scenario: The generator cannot read repository state at all
- **WHEN** the generator runs outside a repository, against an unborn `HEAD`, or where the revision cannot be resolved
- **THEN** it MUST write the declared sentinel for that condition rather than omitting the key, an empty string, or a placeholder of its own choosing
- **AND** the condition it names MUST be the one that actually held, so a reader can tell an ad-hoc derivation from an unreadable repository

#### Scenario: A generator invents its own spelling
- **WHEN** a generator writes a non-commit value into a derivation-pin key that the shared vocabulary does not declare
- **THEN** the value MUST be refused as an undeclared sentinel rather than accepted as a locally reasonable choice
- **AND** the remedy MUST be to declare the value in the shared vocabulary or to use the declared spelling for the condition, never to leave the spelling local to one generator

### Requirement: The sentinels already committed are declared as they stand, and are never rewritten to normalize them
Committed values that already act as sentinels SHALL be brought into the
declared vocabulary as the spellings the repository actually carries, and MUST
NOT be rewritten in place to make the vocabulary tidier.

THIS RULE EXISTS BECAUSE THE PRACTICE CAME FIRST. The sentinel idea was not
designed and then adopted; it was written by hand, one packet at a time, into
proposal-support manifests whose generator has never emitted such a value — and
it was right every time. Those hand-written values are the evidence that a
generator confronted with content it cannot pin reaches for an honest non-pin
rather than a false commit, and they are the reason this vocabulary is worth
declaring at all. A declaration that erased them to start from a clean sheet
would delete its own justification.

REWRITING THEM IS ALSO REFUSED ON THE RULE THIS CAPABILITY ALREADY CARRIES.
Every such value sits inside an archived packet, and a content edit to captured
material after capture is a finding in its own right; a value edited to a
spelling the run did not write makes the artifact state something that did not
happen. The same ordering the retention rule settles for an orphaned pin settles
this: when the record cannot move, the declaration is what accommodates it.

MULTIPLE SPELLINGS FOR ONE CONDITION ARE THEREFORE LEGAL, AND EACH SHALL SAY
WHICH IT IS. Where the committed corpus carries more than one spelling of the
same condition, the declaration SHALL name one as canonical — the spelling new
generator output uses — and declare the others as legacy members that remain
legal in committed state and MUST NOT be written afresh. A legacy member without
that marking is indistinguishable from a second canonical spelling, which is the
drift this requirement exists to stop rather than to bless.

BUT THE DECLARATION SHALL ESTABLISH WHICH CONDITION EACH SPELLING NAMES BEFORE
MARKING ANY OF THEM LEGACY, because two spellings that look like variants of one
condition are sometimes two conditions wearing similar words, and collapsing them
destroys the distinction the vocabulary exists to carry. A value written when the
generator READ CONTENT IT COULD NOT PIN and a value written when the generator
COULD NOT READ THE REPOSITORY AT ALL are different facts with different
consequences for a reader: the first says the content is real and unreconstructible,
the second says nothing about the content was established. A declaration that
folded the second into the first as a legacy spelling would silently restate every
artifact carrying it. Where the conditions differ, BOTH spellings are members and
EACH is canonical for its own condition; the legacy marking applies only within a
single condition.

AND A KEY THAT IS SIMPLY ABSENT IS NOT A MEMBER OF THIS VOCABULARY. An artifact
carrying no pin key at all makes no claim, honest or otherwise: it cannot be
distinguished from a generator that crashed before writing, a schema that predates
the key, or a hand-written stub, where every sentinel names which condition
applied. Absence SHALL therefore be recognized as a legacy state of the corpus —
visible, reported once, and never repaired into a sentinel after the fact — rather
than declared as a spelling. Converting an absent key into a sentinel would assert
a condition nobody recorded, which is the same falsification as writing a commit
that was never true.

#### Scenario: Two spellings turn out to name two conditions
- **WHEN** the corpus carries two spellings that resemble one condition, and the conditions they were written for differ
- **THEN** both MUST be declared as members, each canonical for the condition it names, and neither marked legacy on the strength of the resemblance
- **AND** the declaration MUST state the two conditions separately, because folding them would restate every artifact carrying the absorbed spelling

AND THE DECLARATION IS WHERE THE CONSUMERS ARE RECONCILED. A guard that compares
a pin value against one spelling of a condition SHALL be reconciled against the
declared vocabulary rather than against whichever spelling its own lane happened
to write, because a consumer that recognizes only one member of a condition
treats every other member as a commit name and fails on it.

#### Scenario: A committed sentinel predates the vocabulary
- **WHEN** the declaration is written and the repository already carries values acting as sentinels in committed artifacts
- **THEN** those spellings MUST be declared as members of the vocabulary, each naming the condition it stands for
- **AND** the artifacts carrying them MUST NOT be edited to a different spelling

#### Scenario: Two spellings name one condition
- **WHEN** the committed corpus carries more than one spelling for the same condition
- **THEN** the declaration MUST name one canonical spelling for new output and mark the others as legacy members that stay legal where they are already committed
- **AND** a generator MUST NOT write a legacy spelling into new output

#### Scenario: A consumer recognizes only one spelling
- **WHEN** code that reads a derivation pin compares its value against a single sentinel spelling rather than against the declared vocabulary
- **THEN** that comparison MUST be reported as a coverage gap, because every unrecognized member of the vocabulary reaches that code as though it were a commit name
- **AND** the repair MUST be to consult the declaration rather than to add one more literal to the comparison

#### Scenario: Tidying is proposed as the repair
- **WHEN** a change proposes to normalize committed sentinel spellings by editing the artifacts that carry them
- **THEN** the edit MUST be refused for a captured artifact, on the same rule that refuses editing a captured pin
- **AND** the vocabulary MUST absorb the spelling instead, because the declaration is the thing that can change without falsifying a record

