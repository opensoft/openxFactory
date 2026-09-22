## ADDED Requirements

### Requirement: Making a neutral product standalone moves no corpus, no governance instance and no check family
Making an extracted neutral product standalone SHALL NOT move the publishing
repository's governed corpus, its OpenSpec instance, its corpus-operations check
families, its adapter column, its intent-plane schemas or the integration tests
that exercise the composition — the arc REVERSES A DIRECTION and does not
relocate a boundary. The publisher keeps what it authored and what reads what it
authored; what the extracted product gains is the ability to stand up without
it. A standalone arc that proposes taking a publisher-side artifact SHALL name
the requirement the taking discharges, and where the artifact is corpus-specific
the answer is a generic implementation on the neutral side or a declared seam,
never the publisher's own copy.

#### Scenario: A standalone arc proposes taking a corpus-operations check family
- **WHEN** an arc that makes a neutral product standalone proposes moving a check family that reads the publishing repository's own corpus, statuses or governance nouns
- **THEN** the move is refused under RULING C2, because the family is corpus operations rather than tooling, and a descendant's user would read the publisher's words

#### Scenario: The neutral product needs a capability the publisher's tooling provides
- **WHEN** the extracted product needs a capability that exists today only as publisher-side, corpus-specific code
- **THEN** the product grows its own generic implementation or declares a seam the publisher's code implements, rather than the publisher's copy being relocated

#### Scenario: A reach is removed by deleting the other side
- **WHEN** a reach from the neutral product into the publisher or the consumer is closed by deleting the far side's module rather than by reversing the direction
- **THEN** the closure is refused, because the far side's need did not stop existing and the direction is what the rule is about

### Requirement: A neutral product imports with no consumer, no publisher and no host present
Every module of a neutral product SHALL import successfully in a checkout where
only that product and its declared third-party dependencies are installed — no
consumer package, no publishing repository and no host application on the import
path. An import-time reach into a package that exists only in the publishing
repository is the extraction's unfinished half, not a runtime dependency: the
routes, verbs and names it re-exported travel through the product's declared
route-extension and subcommand-extension seams, contributed by whoever owns
them. A product whose own test suite collects only with its root `conftest`
disabled, or only over a named subset of its files, SHALL have that exclusion
REPORTED AS AN OPEN EXTRACTION rather than recorded as test configuration.

#### Scenario: A server module imports a package only the publisher has
- **WHEN** a neutral product's server or CLI module imports, at module level, a package that exists only in the publishing repository
- **THEN** the import is reported as an unfinished extraction, and the names it re-exported are contributed through the product's declared extension seam instead

#### Scenario: The suite is green only with the root conftest disabled
- **WHEN** a product's own required check runs its suite with the root `conftest` disabled, or over an enumerated file list shorter than the suite
- **THEN** the exclusion is reported as an open extraction with the count it hides, rather than passing as a green check

#### Scenario: Every module is imported by the product's own suite
- **WHEN** the import-time reaches are closed
- **THEN** a test in the product's own suite imports EVERY module of the product in a checkout with no sibling installed, and fails naming the first module that still needs one

### Requirement: A neutral product ships a default profile for its own domain, and the composition point stays open
A neutral product whose entry points require a registered domain profile SHALL
ship a DEFAULT PROFILE for its own neutral domain and SHALL start on it with no
host present, while the composition point REMAINS OPEN for any host to register
a different profile. Shipping a default is not owning the composition point: the
default describes the product's own domain — documents and ideas — and a host,
a consumer layer or a domain descendant registers its own and replaces it. Where
the product already SHIPS a neutral vocabulary for its own shape, that vocabulary
is the default profile's and SHALL NOT be re-authored by this arc: a standalone
product that already says what it does in plain words has the thing the arc is
for, and changing those words would be designing a workflow rather than opening
a door. What
a core may not carry is ANOTHER domain's profile, which is why the publisher's
profile was deleted at the carve rather than travelling; the absence of any
default, however, leaves a product that cannot start, and that is a defect
rather than a discipline.

#### Scenario: An entry point is built with no host registration
- **WHEN** the product's parser or server is built in a process where no host has registered a domain profile
- **THEN** it builds on the product's OWN default profile and starts, rather than refusing

#### Scenario: The default profile carries the publisher's vocabulary
- **WHEN** a neutral product's default profile names the publishing repository's status taxonomy, its change/spec/delta nouns or its act verbs
- **THEN** the profile is refused under RULING C2 and DIRECTION Q5, and those words stay in the declaration of the domain they belong to

#### Scenario: The product already ships a neutral vocabulary
- **WHEN** the neutral product already carries plain words for its own shape, rendered by a shell that is visibly not rendering a domain's
- **THEN** those words are the default profile's vocabulary unchanged, and the arc neither re-authors them nor designs a new workflow around them

#### Scenario: A host registers its own profile
- **WHEN** a host, consumer layer or domain descendant registers a profile
- **THEN** the registered profile replaces the default for that process, so the default is a fallback and never a privileged path

### Requirement: A neutral product produces its own primary artifact with no consumer installed
A neutral product SHALL produce the primary artifact its own verbs serve — for a
document product, the document snapshot its server reads — in a checkout where
the CONSUMER layer is not installed. A product that serves an artifact it cannot
generate is not standalone however complete its serving half is: the user who
installs it alone gets a reader with nothing to read. Where the generator lives
today in the consumer because it was written against the publisher's corpus, the
neutral product SHALL grow its OWN generator over the corpus interface it already
declares, and the consumer SHALL KEEP its governed generator and contribute it
through a DECLARED GENERATOR SEAM. That seam is distinct from the corpus-read
interface and SHALL BE DECLARED BY THIS ARC, naming the operation it hands over,
the registration point, and what a conformant implementation must satisfy — a
closed corpus-read interface carries no generator handoff, and "the same seam"
SHALL NOT be asserted of an interface whose members do not include one, because
two incompatible implementations could then both claim conformance. A generator that carries the publisher's governance
vocabulary, or that imports the publisher's own check families, SHALL NOT BE
RELOCATED into the neutral product: relocating it trades one wrong-way dependency
for a deeper one, and the neutral core ends up importing the very tooling
`corpus-adapter-seam` forbids it to import. **A mechanism that leaves the neutral
product unable to generate when installed alone SHALL NOT be treated as
satisfying this requirement either**, however lawful the direction it produces —
declaring a protocol the consumer implements reverses the DIRECTION and is
required, but on its own it converts a missing-module error into a well-worded
refusal and leaves the product with nothing to read.

#### Scenario: The product serves a snapshot it cannot generate
- **WHEN** a product's server reads a snapshot whose generator resolves only through the consumer layer
- **THEN** the product is reported as NOT standalone, and the refusal names the consumer as today's remedy, which is the state this requirement closes

#### Scenario: A snapshot is generated over plain documents
- **WHEN** the product is pointed at a corpus of plain documents carrying none of the publishing repository's governance vocabulary, with no consumer installed
- **THEN** a snapshot is generated and it names no publisher noun

#### Scenario: The consumer's own corpus is projected
- **WHEN** the consumer layer IS installed and points the product at the publisher's governed corpus
- **THEN** the projection is unchanged from today's behaviour, because the arc reverses a direction and removes no capability from the consumer

#### Scenario: The consumer's generator carries the publisher's vocabulary
- **WHEN** the generator that exists is written against the publisher's corpus — its governance nouns in its paths, and the publisher's check families among its imports
- **THEN** it is NOT relocated into the neutral product; the neutral product grows its own projection over its declared corpus interface, and the consumer contributes its governed generator through a generator seam this arc declares
- **AND** the neutral product's projection is judged by what it can read alone, not by what the consumer's can read

### Requirement: A deferred reach into the publisher or the consumer resolves through the declared seam
A neutral product's DEFERRED reach — an import written inside a function body so
that module import succeeds and the failure waits for the call — SHALL resolve
through the adapter, extension or registry the product itself declares, and
SHALL NOT name a publisher-side or consumer-side package by module name. A
deferred reach is the more dangerous class precisely because it passes the
import test: the product looks installable, and the verb fails in front of a
user. Where a verb genuinely needs an implementation the product does not carry,
it SHALL resolve the REGISTERED implementation through its own seam, and where
none is registered it SHALL REFUSE NAMING THE SEAM AND THE REMEDY rather than
raising a module-not-found error from an import line inside a function.

#### Scenario: A verb imports the publisher's adapter by module name
- **WHEN** a neutral product's verb imports the publishing repository's corpus adapter by package name inside a function body
- **THEN** the reach is reported, because module-level import health hides a call-time failure the import test cannot see

#### Scenario: A verb needs the home corpus
- **WHEN** a verb needs to resolve a document against the home corpus
- **THEN** it resolves the REGISTERED corpus adapter through the product's own seam, so that any conformant adapter answers and none is reached by name

#### Scenario: No implementation is registered
- **WHEN** a verb's seam has no registered implementation in the running process
- **THEN** the verb refuses, naming the seam and what would satisfy it, rather than raising a module-not-found error

### Requirement: A neutral product carries a health check over its own documents, and corpus-operations families stay with the corpus
A neutral product that manages documents SHALL carry a health check it can run
over ITS OWN documents from its own checkout, and the publishing repository's
CORPUS-OPERATIONS check families SHALL stay with the corpus they read. The two
are not in tension: what makes a family corpus operations is that it reads one
corpus's statuses, nouns and lifecycle, and what makes a check generic is that
it reads a document. Where a single module carries both — a generic traversal
wrapped around corpus-specific classification — the generic part SHALL BE
SEPARATED BEFORE EITHER SIDE MOVES, which is `corpus-adapter-seam`'s relocation
rule applied inside a module rather than between two packages.

The results that check produces are DERIVED DATA and SHALL NOT BE COMMITTED INTO
THE CORPUS THEY DESCRIBE: they live in the product's own disposable store, are
recomputable from the documents at any time, and their loss SHALL cost a
recomputation rather than a document. The check SHALL read documents AS DOCUMENTS
— broken internal links, documents nothing links to, near-duplicates, missing
neutral front matter, a declared stage that disagrees with where the document
sits, and stale or empty stubs — SHALL be BASELINE-RELATIVE so that new findings
get attention while persistent ones stay quiet and an uncited disappearance is
re-raised, SHALL report where the human is already working rather than by filing
into an external tracker, and SHALL run any model-assisted check ONLY where a
model is configured.

#### Scenario: A module mixes generic traversal with corpus-specific classification
- **WHEN** a check module carries both a generic document traversal and classification against one corpus's governance vocabulary
- **THEN** the generic part is relocated into a module both sides depend on before either side moves, and the whole module does not travel

#### Scenario: The document product can report on nothing
- **WHEN** a product delivered as document-management tooling has no health check it can run over its own documents
- **THEN** the tooling is reported as undelivered, because a document product that cannot report on its own documents has not shipped the thing it is named for

#### Scenario: Health results are written into the corpus
- **WHEN** a product's health results are committed into the repository whose documents they describe
- **THEN** the write is refused: results are DERIVED DATA, recomputable from the corpus, and committing them makes the corpus carry its own opinion of itself

#### Scenario: Health results need somewhere to live
- **WHEN** a product that keeps a datastore computes health results
- **THEN** they live in that DISPOSABLE store rather than in the corpus, and losing the store costs a recomputation and no document

#### Scenario: A closed schema must gain a table
- **WHEN** derived results require a table a ratified CLOSED list does not name
- **THEN** it arrives as an ADDITIVE migration that never edits the canonical one, and the declaration that closes the list moves in the SAME change, so the boundary is re-drawn in the open rather than widened quietly

#### Scenario: A family reads the publisher's status taxonomy
- **WHEN** a check family reads the publishing repository's `Status:` taxonomy or its change/spec/delta nouns
- **THEN** it stays with that corpus under RULING C2, and the neutral product's own health check reads its own declaration instead

### Requirement: A neutral product validates its own documents from a single checkout
A neutral product SHALL carry a validator and the schemas that validator reads
in ONE checkout, so that validating a document requires no second repository on
disk. A validator whose schemas are split across checkouts is not a validator
anyone can run: the split is discoverable only by trying it, and the failure it
produces names a missing path rather than a missing product. The validator's INPUT SET SHALL BE
NARROWED TO THE PRODUCT'S OWN DOCUMENT KINDS before any schema is acquired: a
standalone validator validates what the product itself defines, and a schema
governing the publisher's or the consumer's artifacts belongs to their
validators. Only where a schema the publishing repository OWNS is genuinely
needed by one of the product's own verbs SHALL it arrive as the DIGEST-PINNED
VENDORED COPY `neutral-product-pin` admits — registered as a CONSUMED manifest
member, never an owned one, naming the publisher contract version it pins — and
never by a path literal into a sibling checkout. **That route SHALL NOT reach a
schema the first requirement of this capability keeps with the publisher**: an
intent-plane or governance schema is not made portable by vendoring it, and a
product that appears to need one has an input set it has not yet narrowed. Vendoring is what makes the
one-checkout rule satisfiable rather than in tension with the pin: the pinned
bytes are IN the checkout, and the pin is what says which bytes they are.

#### Scenario: No checkout carries the whole schema set
- **WHEN** a validator's schemas are split so that no single checkout carries the set it reads
- **THEN** the split is reported, and each validator names the checkout its schemas are read from

#### Scenario: A user validates a document in the product's own checkout
- **WHEN** a user runs the product's validator over a document in a checkout holding only that product
- **THEN** the validation runs and returns a verdict, rather than failing on an unresolvable schema path

#### Scenario: A publisher-owned schema is needed
- **WHEN** a validation genuinely needs a schema the publishing repository owns, and that schema is not one the first requirement keeps with the publisher
- **THEN** the schema travels as the DIGEST-PINNED VENDORED COPY `neutral-product-pin` already admits — registered in the product's own manifest as a CONSUMED member, never an owned one, naming the publisher contract version it pins — so that the product's checkout carries what its validator reads
- **AND** it is never reached by a path literal into a sibling checkout, which is the failure this requirement exists to close

#### Scenario: The validator's input set reaches a schema the publisher keeps
- **WHEN** a standalone validator's declared input set includes an intent-plane or governance schema the first requirement keeps with the publishing repository
- **THEN** the input set is narrowed rather than the schema vendored, because vendoring a schema this capability elsewhere refuses to move would satisfy one requirement by breaching another
- **AND** if the product genuinely cannot validate its own documents without it, that is reported as a finding about the boundary, not resolved by a copy

### Requirement: An extracted product's own spec instance governs its requirements before the product is called standalone
Requirements a carve assigns to an extracted product SHALL be re-promoted in
that product's OWN spec instance before the product is declared standalone, and
an instance that has promoted nothing SHALL NOT be treated as governing the
product it is named for. An empty instance is not a neutral state: the carve's
per-requirement map becomes the only record of what the product owes, the
promotion-fidelity checker has no successor key to find the requirements under,
and no delta that MODIFIES them can be authored anywhere, because the target
spec exists nowhere. Until the re-promotion lands, work on the extracted product
SHALL be authored where its target specs live, and the reason SHALL be recorded
in the change that does so.

#### Scenario: A destination instance has promoted none of its assigned requirements
- **WHEN** a carve's ratified per-requirement map assigns requirements to a destination repository and that destination's promoted specs are empty
- **THEN** the requirements are governed nowhere, and the map is reported as the only record of them

#### Scenario: A change must MODIFY a requirement the destination has not promoted
- **WHEN** a change needs a MODIFIED delta against a requirement assigned to an extracted product whose instance has promoted nothing
- **THEN** the change is authored in the instance where the target spec lives, and it records that the destination instance was not yet operable for this delta

#### Scenario: The destination has promoted its assigned set
- **WHEN** the extracted product's instance has promoted the requirements the map assigned it
- **THEN** subsequent work scoped to that product is authored in its own instance, and the interim arrangement ends

### Requirement: Each repository of a split product runs its own suite to green in its own checkout
Each repository of a split product SHALL run its own test suite to green in its
own checkout with no sibling repository present, and a required check that runs
only over a named subset of the suite's files SHALL declare the exclusion, its
size and the reason. A behaviour that genuinely needs both repositories is an
INTEGRATION test: it SHALL declare both, name the pin it composes at, and live
where the composition is declared — it SHALL NOT be dropped from both suites, which
is how an assembled surface comes to be exercised by nobody while both legs
report green.

#### Scenario: A required check names a file list
- **WHEN** a leg's required check enumerates the test files it runs, or disables collection, so that the suite it reports on is smaller than the suite in the tree
- **THEN** the difference is declared with its count and its reason, and it is reported as an open extraction

#### Scenario: A behaviour needs both legs
- **WHEN** a behaviour can be exercised only with both repositories present
- **THEN** it is an integration test naming both repositories and the pin it composes at, rather than being removed from both suites

#### Scenario: Both legs are green alone
- **WHEN** both legs run their full suites green in isolation
- **THEN** the assembled surface is additionally exercised by an integration run, so that what only the composition produces is still measured

### Requirement: A neutral product declares one entry point that starts the whole product
A neutral product SHALL declare ONE documented entry point that starts the
product its users were promised, and a product whose only console script starts
a SUBSYSTEM SHALL be reported as having no entry point. The test is a user's:
after installing the product and reading its own README, a user runs one
documented command and reaches the running product, including whatever browser
surface it ships. An assembly root whose targets bootstrap, validate and pin the
repositories SHALL NOT be treated as an entry point, because assembling the
sources is not starting the product, and a product that can only be assembled is
one nobody outside its authors can run.

#### Scenario: The only console script starts a subsystem
- **WHEN** a product's packaging declares console scripts for one subsystem and none for the surface the product is named for
- **THEN** the product is reported as having no entry point, whatever the subsystem's own health

#### Scenario: A user follows the documented start
- **WHEN** a user installs the product and runs the single command its README documents
- **THEN** the product starts and serves its own browser surface, with no sibling repository installed

#### Scenario: The assembly root's targets are treated as the entry point
- **WHEN** an assembly root offering only bootstrap, validation and pin targets is offered as the way to start the product
- **THEN** the offer is refused, because assembling sources is not starting a product

### Requirement: A session's work leaves the local repository through a declared submission protocol with a neutral default
A neutral product SHALL move a session's work out of the local repository through
a DECLARED SUBMISSION PROTOCOL carrying a NEUTRAL DEFAULT that works on a plain
git repository, and SHALL NOT bind that protocol to one hosting platform's
command-line tool. A pull request is a HOSTING-PLATFORM artifact and a push is a
git one: a product whose only submission implementation opens pull requests has
no submission path at all for the plain local repository its own install story
describes. The protocol governs how work LEAVES the local repository; what may
then be done with it is settled elsewhere. The neutral default SHALL push the session branch to the attached
remote where one exists, and where none exists SHALL SAY SO PLAINLY — never a
silent failure, never a reported success it did not achieve. A governed host
contributes its own implementation through the SAME injection seam the product's
other contributed implementations use, so the host's existing flow is unchanged.

LANDING AUTHORITY FOLLOWS WHOEVER GOVERNS THE REPOSITORY, and the neutral product
SHALL ASK the repository rather than hard-coding either answer. Where a
GOVERNANCE EXISTS OUTSIDE THE TOOL, the governed host RESERVES landing and routes
it to that governance's own instrument, so separation of duties is unchanged;
where the OWNER IS THE GOVERNANCE, the product MAY land, because a rule that
forbids it protects nobody from anybody. THREE GUARDRAILS HOLD IN EVERY MODE and
are not configurable: a merge SHALL BE AN EXPLICIT HUMAN ACT and never automatic;
a CONFLICT SHALL BE SHOWN to the human and never silently resolved; and a merge
SHALL BE A COMMIT, so that it can be reverted. Together they keep the purpose the
absolute prohibition served — no tool merging behind its governance's back —
while dropping its letter exactly where the user IS the governance.

#### Scenario: The only submission implementation shells out to one platform
- **WHEN** a neutral product's only implementation of its submission protocol invokes one hosting platform's command-line tool, defaulting to that platform's host
- **THEN** it is reported as having no submission path for a plain local repository, which is the install its own ruling describes

#### Scenario: A session is submitted on a plain repository with a remote
- **WHEN** a session is submitted on a plain git repository that has a remote attached
- **THEN** the neutral default pushes the session branch to that remote and reports where the work went

#### Scenario: No submission target exists
- **WHEN** a session is submitted on a repository with no remote attached
- **THEN** the product reports plainly that there is nowhere to submit, rather than failing opaquely or reporting a success it did not achieve

#### Scenario: A governance exists outside the tool
- **WHEN** the product runs in an install whose repository is governed by an authority outside the product
- **THEN** the governed host RESERVES landing and routes it to that governance's own instrument, and the product itself lands nothing

#### Scenario: The owner is the governance
- **WHEN** the product runs standalone on a repository its own user owns, with no outside governance to defer to
- **THEN** the product may land the work, because the prohibition existed to protect a governance that is not present

#### Scenario: A merge is attempted without a human
- **WHEN** any code path would land work without an explicit human act
- **THEN** it is refused in EVERY mode, because "explicit and human" is a guardrail and not a setting

#### Scenario: A merge meets a conflict
- **WHEN** landing meets a conflict
- **THEN** the conflict is SHOWN to the human and never silently resolved, in every mode

#### Scenario: A landed merge must be undoable
- **WHEN** work is landed
- **THEN** it lands AS A COMMIT, so that it can be reverted by the ordinary means, in every mode

#### Scenario: A governed host contributes its own submission implementation
- **WHEN** a governed host needs its own platform flow
- **THEN** it registers its implementation through the same injection seam the product's other contributed implementations use, and the host's existing flow is unchanged


### Requirement: A standalone install brings its own datastore, and the product keeps one dialect
A neutral product that requires a datastore SHALL SHIP THAT DATASTORE WITH ITS
STANDALONE INSTALL, so that a user installs the product and not a database, and
SHALL KEEP EXACTLY ONE DIALECT. A second dialect added for the convenience of a
local install is refused: it doubles every migration and every schema test
forever, in exchange for a convenience the install can provide by bundling. Where
the product separates a PRIVILEGED connection from a LEAST-PRIVILEGED one, both
SHALL SURVIVE the bundling — a single-user install is not a reason to serve from
the migrating credential — and neither SHALL be defaulted from the other, because
a silent fallback grants the serving path the schema authority the split exists
to withhold.

#### Scenario: A local install asks the user to provide a database
- **WHEN** a standalone install requires the user to obtain, install or configure a database before the product will start
- **THEN** it is reported as an incomplete install, because the product was promised as the thing that installs

#### Scenario: A second dialect is proposed for local convenience
- **WHEN** an embedded or file-backed dialect is proposed so that the local install can avoid the bundled one
- **THEN** it is refused, and the bundling is done instead: one dialect is what keeps one migration set honest

#### Scenario: The privileged and serving connections are collapsed
- **WHEN** a single-user install serves from the migrating connection, or defaults one connection setting from the other
- **THEN** it is refused, because the split withholds schema authority from the serving path and a silent fallback hands it back

### Requirement: A standalone install has a named local identity mode, and a hosted install cannot fall into it
A neutral product whose hosted mode authenticates through an external identity
broker SHALL OFFER A NAMED LOCAL SINGLE-USER MODE that requires no broker, and
the HOSTED MULTI-USER MODE SHALL KEEP its broker and its pinned issuer unchanged.
The local mode SHALL BE SELECTED EXPLICITLY and SHALL NOT BE REACHABLE BY
OMISSION: a hosted install whose issuer setting is absent SHALL REFUSE TO START,
naming the setting, rather than degrading into single-user operation. A mode that
can be entered by forgetting to configure something is not a mode, it is a
failure that looks like a feature — and the failure it looks like is an
unauthenticated multi-user install.

#### Scenario: A student installs the product alone
- **WHEN** a single user installs the product for their own use and selects the local mode
- **THEN** it starts and is usable with no identity broker to run, configure or reach

#### Scenario: A hosted install is missing its issuer
- **WHEN** an install declared as hosted starts with no issuer configured
- **THEN** it REFUSES and names the missing setting, and does NOT fall back to local single-user operation

#### Scenario: The hosted mode's broker is unchanged
- **WHEN** the hosted multi-user mode runs
- **THEN** it authenticates through the same broker against the same pinned issuer as before, and a token from any other issuer is refused exactly as it is today

### Requirement: A health finding carries a resolution path, and every fix lands through the landing rule
A neutral product's health check SHALL offer a RESOLUTION PATH for every finding
it raises, reachable from the surface the human is already working in AND from
the command line with the same actions, reading the findings from the product's
own store and presenting them BASELINE-RELATIVE so that new findings come first
and persistent ones stay quiet. Detection without resolution is a list that grows.
Findings SHALL be resolved in THREE DECLARED CLASSES: MECHANICAL findings the
product can repair itself — a link whose target moved, front matter derivable
from the adapter, a stage that disagrees with the document's location; ASSISTED
findings where the product PROPOSES a repair a human then edits, with any
model-written proposal offered ONLY where a model is configured; and HUMAN-ONLY
findings where the product SHOWS THE EVIDENCE and the human repairs, removes, or
records an exception.

EVERY REPAIR, OF EVERY CLASS, SHALL BE WRITTEN AS A DRAFT ON A BRANCH AND NEVER
ONTO THE DEFAULT BRANCH, and SHALL REACH THE DEFAULT BRANCH ONLY THROUGH THIS
CAPABILITY'S LANDING RULE — so a standalone owner lands it in the product, a
governed repository receives the governance's own instrument instead, and in
every mode the landing is an explicit human act, conflicts are shown, and the
result is a revertible commit. **NOTHING SHALL LAND AUTOMATICALLY, not even a
one-line mechanical repair**: a fix small enough to seem safe is exactly the one
that gets applied without being read. Several repairs MAY be batched into one
draft so a human reviews them together.

#### Scenario: A finding has no resolution path
- **WHEN** a health check reports a finding a human cannot act on from the surface that reported it
- **THEN** it is reported as detection without resolution, because a list that only grows is not a health check

#### Scenario: A mechanical finding is repaired
- **WHEN** a finding is mechanical — a moved link target, derivable front matter, a stage that disagrees with the document's location
- **THEN** the product writes the repair itself, as a DRAFT ON A BRANCH, and never onto the default branch

#### Scenario: A repair needs judgement
- **WHEN** a finding is a near-duplicate or an empty stub
- **THEN** the product PROPOSES a repair the human edits in the draft, and offers a model-written proposal only where a model is configured

#### Scenario: A finding is not the product's to repair
- **WHEN** a finding requires a decision the product cannot make
- **THEN** it SHOWS THE EVIDENCE and the human repairs, removes, or records an exception — the product proposes nothing it cannot justify

#### Scenario: A one-line fix is applied automatically
- **WHEN** any repair, however small, would reach the default branch without an explicit human act
- **THEN** it is refused, because the guardrails hold for every landing and a fix small enough to seem safe is the one that gets applied unread

#### Scenario: Several repairs are reviewed together
- **WHEN** many findings are repaired in one sitting
- **THEN** they MAY be batched into a single draft for one review, and the batch lands under the same rule a single repair would

#### Scenario: The command line and the view disagree
- **WHEN** a resolution action exists in the product's own view but not from the command line
- **THEN** the gap is reported, because an install without a browser is the standalone install this capability exists to serve

### Requirement: An exception is a human decision and lives in the corpus, never in the derived store
A neutral product SHALL RECORD AN EXCEPTION — a human's decision that a finding
is accepted, not a defect — IN THE CORPUS, as a committed artifact, and SHALL NOT
keep it in the disposable store where the findings themselves live. The two are
different in kind: a finding is DERIVED and recomputable, while an exception is a
JUDGEMENT that exists nowhere else and can be recovered from nothing. A store
that may be discarded and rebuilt from the documents MUST NOT be the only home of
a decision the documents do not contain. An exception SHALL therefore SURVIVE A
RESET of the store, SHALL be readable and reviewable as an ordinary change to the
corpus, and SHALL cite what it is accepting, so that removing it re-opens the
finding it was suppressing.

#### Scenario: The derived store is reset
- **WHEN** the product's store is discarded and rebuilt from the corpus
- **THEN** every recorded exception still holds and its finding is NOT re-raised, because the exception was never in the store

#### Scenario: An exception is stored beside the findings
- **WHEN** an exception is written into the disposable store rather than committed to the corpus
- **THEN** it is refused, because the store is disposable by design and a judgement stored there is a judgement scheduled for deletion

#### Scenario: An exception is withdrawn
- **WHEN** a committed exception is removed
- **THEN** the finding it suppressed is raised again on the next run, so that suppression is a live claim rather than a permanent silence

### Requirement: Health checks extend through pinned packs, and the engine owns what must not vary
A neutral product's health check SHALL be EXTENSIBLE THROUGH CHECK PACKS declared
against a neutral contract the product itself owns, on the same pattern as its
corpus interface, so that a domain adds its own checks without forking the
product. A PACK SUPPLIES: check families, each with an id, a version and the
documents it applies to; findings in the NEUTRAL SHAPE, carrying a severity, a
resolution class and its evidence; optionally PROPOSED FIXES AS PATCHES; and its
own labels, resolved through the display facet rather than spelled in the
product's surface.

THE ENGINE OWNS, IDENTICALLY FOR EVERY PACK: the resolution surface and its
command-line parity; scheduling; the baseline logic; storage — results in the
derived store and exceptions in the corpus; and the fix loop with its landing
rule. **A PACK SHALL NOT REDEFINE THE RESOLUTION CLASSES, THE BASELINE RULES, OR
WHO MAY LAND WORK.** Those are the properties a user relies on being the same
whatever checks are installed, and a pack that could vary them would make every
guarantee in this capability conditional on which packs a given install happens
to carry.

EVERY FINDING SHALL CARRY THE ID AND THE VERSION OF THE PACK THAT RAISED IT, so
that a finding can be attributed, a pack can be upgraded without its history
becoming ambiguous, and a baseline can tell a genuinely new finding from one that
arrived with a new pack version.

#### Scenario: A pack writes to the tree
- **WHEN** a pack writes, commits or merges anything rather than returning findings and patches
- **THEN** it is refused, because only the engine's fix loop writes, and a pack that writes has escaped every guardrail the loop carries

#### Scenario: A pack is consumed without a pin
- **WHEN** a pack is installed without being pinned by commit and digest
- **THEN** it is refused, because an unpinned pack silently changes what a corpus is judged against

#### Scenario: A pack crashes or hangs
- **WHEN** a pack raises, or exceeds its time budget
- **THEN** the failure is reported AS A FINDING AGAINST THAT PACK and the other packs still run, because one broken pack must not take the health check down

#### Scenario: A pack tries to define its own resolution class
- **WHEN** a pack returns a finding in a class the engine does not declare, or declares its own baseline or landing rule
- **THEN** it is refused, because those are the properties that must not vary between installs

#### Scenario: A finding arrives with no provenance
- **WHEN** a finding is stored without the id and version of the pack that raised it
- **THEN** it is refused, because an unattributable finding cannot be upgraded, disputed, or told apart from a new pack's first run

#### Scenario: A pack's labels are spelled in the product's surface
- **WHEN** a pack's finding titles or family names are rendered as the pack spells them
- **THEN** they are resolved through the display facet instead, so a domain's words stay the domain's and the neutral surface keeps its own
