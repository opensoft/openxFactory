# release-realization

**ONE `## MODIFIED` BLOCK, WRITTEN OVER CANON.** No active change writes
`(release-realization, The estate's repositories are enumerated in a governed
inventory)` — checked at filing by `grep -rl` over every active delta — so the
block is SOLE, its basis is the requirement exactly as
`archive/2026-09-23-add-estate-repository-inventory` promoted it, and
`proposal.md` declares `sequenced_after: []`. Every paragraph and every
scenario below is canon's own bytes EXCEPT the `gitlink` bullet, which is
replaced and named in the block's own `Removed from canon by` marker, and the
two paragraphs, three scenarios and `**AMENDED BY**` note this packet adds.
*A declared repository is judged for membership against the estate inventory*
is NOT modified: a leg's row is a `pinned` row, which that requirement already
passes, and its bound on where the evidence lives defers to this requirement's
terms (`design.md` D6).

## MODIFIED Requirements

### Requirement: The estate's repositories are enumerated in a governed inventory
openxFactory SHALL carry a machine-readable inventory of the estate's
repositories, ONE ROW PER REPOSITORY, and every row SHALL carry the repository's
`<owner>/<name>` address, its BARE NAME, its ROLE in the layer model, its
GOVERNANCE CLASS, and the ADMISSION EVIDENCE that puts it in the estate. The
file SHALL carry `schema_version` and `kind` like every other governed YAML in
this repository, and a house validator SHALL read it.

THE INVENTORY RECORDS AN ADMISSION TAKEN ELSEWHERE AND PERFORMS NONE, and that
is the answer to the authority question the successor was filed on: who admits a
repository to the estate. Nobody admits one BY WRITING A ROW. A repository joins
the estate when a governed tree NAMES it, and the row is the record of that
naming. So every row SHALL carry `admitted_by:` naming at least one NAMING SITE
and the kind of act it is, and the admissible kinds SHALL be exactly these five,
because they are exactly the ways this estate has ever named a repository:

- `gitlink`: a GOVERNED ESTATE REPOSITORY's `.gitmodules` carries the submodule,
  and the evidence SHALL NAME THE REPOSITORY THAT CARRIES IT. This is the
  estate's own act of admission and the widest class. THE AGGREGATION
  REPOSITORY IS THE WIDE CASE AND NOT THE ONLY ONE: the estate also places a
  repository as a NESTED DESCENDANT of a governed DomainxFactory rather than as
  an aggregation sibling, and a `gitlink` read as the aggregation's alone would
  leave every nested member admitted by nothing at all. A PINNED ASSEMBLY
  ROOT's `.gitmodules` IS A CARRIER TOO, read AT THE COMMIT openxFactory's own
  `pin` of that root names: there the act of admission is openxFactory's pin,
  and the root's gitlink is the site that pin reaches. Naming the carrier is
  what keeps the evidence checkable, a reader being unable to look in a tree the
  row does not name.
- `pin`: an openxFactory file under `contracts/` names the repository as the
  source of a commit-and-digest pin. This is openxFactory's act, for a product
  PINNED rather than governed.
- `workflow`: an openxFactory workflow dispatches into the repository, or
  checks it out, at a named ref.
- `root`: the aggregation repository ITSELF, which no `.gitmodules` can name
  because a superproject is not its own submodule, and which would otherwise be
  the one member of the estate no evidence admits.
- `change`: a RATIFIED change in this repository whose realization CREATES the
  repository. This kind exists because a code surface is FORWARD-LOOKING: it
  names where a change WILL write, so a repository the estate is creating is
  declared before any gitlink, pin or workflow can name it. THE INVENTORY SHALL
  CARRY THAT ROW and SHALL NOT omit it at an author's discretion; a
  `change`-admitted row is PROVISIONAL, and SHALL say so.

A `change`-ADMITTED ROW SHALL NOT REMAIN PROVISIONAL FOREVER. When its change
ARCHIVES, one of the other four kinds is owed, because the repository the
realization created now exists and a governed tree can name it. THE GOVERNED
TREE THAT NAMES IT IS COMMONLY THE DOMAINxFACTORY THE REALIZATION NESTED IT
UNDER, which is the measured reason `gitlink` is not read as the aggregation's
alone: a realization that creates a repository and nests it would otherwise
discharge into no kind, and the provisional row it opened could never be closed.
A row still admitted only by an ARCHIVED change SHALL be a finding, on the same
terms as a row whose evidence has gone: the provisional admission outlived the
act that justified it.

A PINNED ROOT CARRIES A `gitlink` ONLY AS FAR AS openxFactory's OWN PIN REACHES,
AND ONE HOP FROM IT. The carrier's own row SHALL declare `governance: pinned`
and SHALL be admitted by EXACTLY ONE `pin`, because the commit that pin names is
the one revision the evidence is read at, and two pins of one root would make
that revision a pick. An `external` repository's `.gitmodules` SHALL admit
nothing, whatever openxFactory pins of it, an `external` repository being no
part of this estate. A `pinned` row that is not itself admitted by a `pin` —
every row this clause admits among them — SHALL carry no row's `gitlink`, so the
reach ends one hop from an openxFactory pin and never runs down a chain of roots.
A row admitted by a pinned root's `gitlink` SHALL NOT declare
`governance: governed`: openxFactory reaches it only through its pin of the
root, at the commit that pin fixes, and authors none of it, which is what a
`pin`-admitted row is too. An inventory whose `gitlink` names a carrier outside
these conditions SHALL be REFUSED, the evidence it records being evidence no
reader can check against a tree openxFactory consumes. NOTHING HERE PINS OR
MOUNTS A LEG: openxFactory files no pin for the repository the root carries and
adds no gitlink to it, that being the assembly root's own job, and the root's
pin is the whole of the evidence of reach.

**Removed from canon by admit-code-leg-under-pinned-root (2026-09-24):** `` `gitlink`: a GOVERNED ESTATE REPOSITORY's `.gitmodules` carries the submodule, and the evidence SHALL NAME THE REPOSITORY THAT CARRIES IT. This is the estate's own act of admission and the widest class. THE AGGREGATION REPOSITORY IS THE WIDE CASE AND NOT THE ONLY ONE: the estate also places a repository as a NESTED DESCENDANT of a governed DomainxFactory rather than as an aggregation sibling, and a `gitlink` read as the aggregation's alone would leave every nested member admitted by nothing at all. Naming the carrier is what keeps the evidence checkable, a reader being unable to look in a tree the row does not name. `` — the bullet defined the `gitlink` kind by a GOVERNED carrier alone, which left a code leg nested under a pinned assembly root admitted by none of the five kinds (openxFactory #1150). NOTHING IT SAID IS DROPPED: the replacing bullet above carries every one of its sentences word for word and adds ONE, naming the pinned assembly root as a second carrier read at its pinned commit, which the paragraph above bounds.

THE RE-CHECK OF ADMISSION EVIDENCE IS BOUNDED BY WHERE THE EVIDENCE LIVES, and
the bound is STATED rather than left for a reader to discover when the validator
cannot do what the requirement says. FOUR of the five kinds name evidence inside
THIS repository's working tree — `pin` a file under `contracts/`, `workflow` a
file under `.github/workflows/`, `change` a directory under `openspec/changes/`,
and `root` a constant naming no file at all — so a row carrying one of them
SHALL be re-checked on EVERY run, DETERMINISTICALLY and with NO NETWORK CALL.
`gitlink` is the ONE kind whose evidence lives in ANOTHER repository's tree,
which an openxFactory checkout does not contain. Its re-check SHALL therefore be
an EXPLICITLY INVOKED mode taking the carrying repository's working tree as a
PATH INPUT, and a run given no such path SHALL REPORT its `gitlink` rows as NOT
RE-CHECKED, with their count, rather than passing them silently or failing them.

A SUPPLIED TREE SHALL BE VERIFIED AS A CHECKOUT OF THE CARRIER THE ROW NAMES
BEFORE ITS `.gitmodules` EVIDENCE IS TRUSTED, and the verification SHALL be made
against the tree's own ORIGIN URL or against the carrier's record in
`contracts/policies/repository-identity.yaml`, those being the two places this
estate states a repository's identity. A PATH IS AN ASSERTION AND NOT AN
IDENTITY: a caller may pass the wrong checkout by typo, by a stale worktree, or
by a repository that merely sits at the expected path, and an unverified path
would let one repository's `.gitmodules` discharge — or condemn — another
repository's row, which is the same defect as resolving a name by asking the
provider. A supplied tree that FAILS that verification SHALL leave the row
reported NOT RE-CHECKED, COUNTED with the rows no tree was supplied for and
NEITHER PASSED NOR FAILED, and the report SHALL name the carrier the row expects
and what the tree actually is: a run that has looked in the wrong place has not
looked. Ruled by Brett Heap, 2026-09-18, verbatim: *"Bind the carrier
identity"*.
A validator that fetched the tree itself would make a required check depend on a
token and on read access to a private repository, which is the cost the derived
shape was refused for and which may not be readmitted at the reverse arm.

A PINNED CARRIER'S EVIDENCE IS READ AT THE COMMIT ITS PIN NAMES, AND AT NO OTHER
REVISION. Where the carrier a `gitlink` row names is a `pinned` row, the tree
supplied for it SHALL first be verified as the carrier on exactly the terms
above, and the row's evidence SHALL then be the carrier's `.gitmodules` AS OF
THE COMMIT the carrier's `pin` names, read out of the supplied tree's own object
store — never out of its working files, and never at another revision, because
openxFactory consumes the root at that commit and at no other, and a leg the
root names at another revision is a leg of a tree openxFactory has not consumed.
THE READ SHALL MAKE NO NETWORK CALL. A verified tree whose object store cannot
produce that commit's `.gitmodules` without one — a partial clone missing the
object, a shallow clone, a checkout that never fetched the pinned commit — and a
carrier pin that names no commit to read at SHALL each leave the row reported
NOT RE-CHECKED, COUNTED and NEITHER PASSED NOR FAILED, the report naming the pin
and the commit: a run that has looked at the wrong revision has not looked.

THE GOVERNANCE CLASS SAYS WHAT A ROW MEANS FOR A REPOSITORY THAT IS PINNED
RATHER THAN GOVERNED, which is the second half of the same authority question,
and it SHALL be one of three: `governed`, the estate authors its contents;
`pinned`, openxFactory consumes it at a commit and digest and authors none of
it; `external`, it is pinned and is NOT of this estate at all. The three are
kept distinct because a consumer that collapsed them would authorize a change
to a repository nobody here may change. An `external` row is carried so that
KNOWN-BUT-NOT-OURS is distinguishable from UNKNOWN, which is a distinction no
validator can draw from absence.

A BARE NAME SHALL RESOLVE THROUGH THE ROW WHOSE BARE NAME IT MATCHES, and the
bare names SHALL BE UNIQUE ACROSS THE INVENTORY. The corpus writes both
spellings, so a reader must resolve both; two rows sharing a bare name would make
one spelling ambiguous, and the validator SHALL REFUSE THE INVENTORY rather than
pick a row, because picking is how an authorization lands in the wrong
repository.

A FORMER ADDRESS SHALL BE RESOLVED THROUGH
`contracts/policies/repository-identity.yaml` AND NEVER THROUGH A PROVIDER
REDIRECT. That file already states the reason in its own header: a redirect is a
grace period that stops the moment the former owner reuses the name, and
governed content whose correctness depends on nobody creating a repository is
not content a contract may rest on. The inventory SHALL carry CURRENT addresses
only, and the transfer map SHALL remain the one place a former address is read.

THE INVENTORY IS NOT A FILE UNDER `contracts/`, AND THE REASON IS MEASURED
RATHER THAN PREFERRED. A file under `contracts/` is a bundle surface whose change
owes a manifest entry, a recomputed digest and a bundle cut, and the fact this
inventory tracks moves often: the aggregation repository's `.gitmodules` took
NINETEEN commits between 2026-07-01 and 2026-09-12, almost all of them an
admission, a retirement or an owner transfer, which is one inventory-moving act
every four days. An enumeration that could not be corrected without cutting a
contract release would be corrected late or not at all, which is the reason
`scripts/code-surface-register.yaml` states for its own placement and the reason
this file takes the same one.

**AMENDED BY `admit-code-leg-under-pinned-root` (2026-09-24).** Every paragraph
and every scenario of this block is promoted canon's own bytes except the
`gitlink` bullet, which is REPLACED and named in the `Removed from canon by`
marker above, and TWO PARAGRAPHS and THREE SCENARIOS, which are ADDED: the
paragraph that bounds which pinned root may carry a `gitlink`, the paragraph
that reads such a carrier's evidence at its pinned commit, and one scenario for
each of those two and one for the refusal between them. THE CLOSED SET STAYS
FIVE KINDS AND NO KIND IS ADDED: a leg of a pinned root is named by a gitlink,
and what this amendment widens is who may carry one. No governance class, no
other kind, no resolution rule, no placement and no promoted scenario moves, and
*A declared repository is judged for membership against the estate inventory*
beside this requirement is untouched.

#### Scenario: A repository is admitted to the estate by a gitlink
- **WHEN** a governed estate repository's `.gitmodules` carries a submodule for a repository — the aggregation repository's in the wide case, a governed DomainxFactory's where the estate nested the repository rather than sibling-linking it
- **THEN** the inventory SHALL carry a row for it whose `admitted_by:` names that gitlink AND the repository that carries it
- **AND** the row's governance class states whether the estate authors its contents or consumes it at a pin

#### Scenario: A code leg is nested under a pinned assembly root
- **WHEN** a `pinned` row admitted by exactly one `pin` is an assembly root whose `.gitmodules`, at the commit that pin names, carries a submodule for a leg openxFactory neither pins nor mounts
- **THEN** the inventory SHALL carry a row for the leg whose `admitted_by:` names that gitlink AND the pinned root that carries it
- **AND** the leg's row SHALL NOT declare `governance: governed`, openxFactory reaching it only through its pin of the root
- **AND** no pin is filed for the leg and no gitlink to it is added to openxFactory, the root's pin being the whole of the evidence of reach

#### Scenario: A gitlink names a carrier outside the two lawful forms
- **WHEN** a row is admitted by a `gitlink` whose carrier's row is `external`, or is `pinned` and admitted by no `pin` or by more than one, or the row itself declares `governance: governed` while a pinned root's gitlink admits it
- **THEN** the validator MUST REFUSE the inventory, naming the row, the carrier, and the condition that fails
- **AND** a row a pinned root's gitlink admits MUST NOT itself carry a further row's gitlink, the reach ending one hop from an openxFactory pin

#### Scenario: A neutral product is pinned but is no submodule
- **WHEN** an openxFactory file under `contracts/` names a repository as the source of a commit-and-digest pin, and no `.gitmodules` entry names it
- **THEN** the inventory SHALL carry a row for it admitted by that pin, with governance class `pinned`
- **AND** the absence of a gitlink is not an absence of membership, the pin being an admission in its own right

#### Scenario: A repository a ratified change is creating
- **WHEN** a RATIFIED active change declares a code surface in a repository its own realization creates, and no gitlink in any governed estate repository, no pin and no workflow names it yet
- **THEN** the inventory MUST carry a PROVISIONAL row admitted by that change, marked as provisional and naming the change id
- **AND** the membership arm is UNCONDITIONAL and still FAILS CLOSED for that identifier — the row is what makes the declaration resolve, so an absent row refuses a ratified packet inside the forward-looking window rather than excusing it
- **AND** once that change ARCHIVES, a row still admitted only by it MUST be reported as a finding, the repository being nameable by a governed tree from that point — commonly by the gitlink of the DomainxFactory the realization nested it under

#### Scenario: The aggregation repository itself
- **WHEN** the inventory enumerates the estate
- **THEN** it SHALL carry a row for the aggregation repository, admitted by `root`
- **AND** the row exists precisely because a superproject is not its own submodule, so no gitlink can admit it

#### Scenario: Two rows share a bare name
- **WHEN** the inventory carries two rows whose bare repository names are the same
- **THEN** the validator MUST REFUSE the inventory, naming both rows and the shared name
- **AND** it MUST NOT resolve the bare spelling to either row, an ambiguous resolution being how an authorization lands in the wrong repository

#### Scenario: A row's in-tree admission evidence names nothing
- **WHEN** a row's `admitted_by:` names a pin, a workflow or a change that THIS repository's own working tree does not carry
- **THEN** the validator MUST report a finding against that row, on every run, deterministically and with no network call, the evidence being a file in the tree it is already reading
- **AND** the remedy is to correct the evidence or to remove the row, never to widen what counts as evidence

#### Scenario: A gitlink row is re-checked only against a supplied tree
- **WHEN** the run reaches a row admitted by a `gitlink` and no working tree was supplied for the repository the row names as the carrier
- **THEN** the validator MUST report that row as NOT RE-CHECKED and MUST count it, and MUST NOT pass it silently, MUST NOT fail it, and MUST NOT fetch the carrying repository
- **AND** when that working tree IS supplied as a path input, it MUST FIRST be verified as a checkout of the carrier the row names — by the tree's own origin URL or by the carrier's record in `contracts/policies/repository-identity.yaml` — and only then MUST the row's `.gitmodules` evidence be re-checked in it, its absence there being a finding against the row
- **AND** a supplied tree that FAILS that verification leaves the row reported NOT RE-CHECKED and COUNTED, neither passed nor failed, the report naming the carrier the row expects and what the tree actually is, a path being an assertion and not an identity

#### Scenario: A pinned root's gitlink is re-checked at its pinned commit
- **WHEN** a working tree is supplied for a carrier whose row is `pinned`, and it verifies as that carrier
- **THEN** the validator MUST read the carrier's `.gitmodules` as of the commit the carrier's `pin` names, from the tree's own object store and with no network call, and MUST NOT read the tree's working files or any other revision
- **AND** the leg's absence from that `.gitmodules` MUST be a finding against the leg's row
- **AND** a verified tree that cannot produce that commit's `.gitmodules` without a network call, or a carrier pin that names no commit, MUST leave the row reported NOT RE-CHECKED and COUNTED, neither passed nor failed, the report naming the pin and the commit

#### Scenario: The inventory carries a former address
- **WHEN** a row's `repository:` is an address `contracts/policies/repository-identity.yaml` records as FORMER
- **THEN** the validator MUST report a finding against that row, naming the current address the transfer map resolves
- **AND** the remedy is the respelling, the inventory carrying current addresses only
