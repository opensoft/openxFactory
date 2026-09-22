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
neutral product SHALL grow its OWN generator over the adapter interface it
already declares, and the consumer SHALL KEEP its governed generator and hand it
in through that same seam. A generator that carries the publisher's governance
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
- **THEN** it is NOT relocated into the neutral product; the neutral product grows its own projection over its declared adapter interface, and the consumer injects its governed generator through the same seam
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

#### Scenario: A module mixes generic traversal with corpus-specific classification
- **WHEN** a check module carries both a generic document traversal and classification against one corpus's governance vocabulary
- **THEN** the generic part is relocated into a module both sides depend on before either side moves, and the whole module does not travel

#### Scenario: The document product can report on nothing
- **WHEN** a product delivered as document-management tooling has no health check it can run over its own documents
- **THEN** the tooling is reported as undelivered, because a document product that cannot report on its own documents has not shipped the thing it is named for

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
