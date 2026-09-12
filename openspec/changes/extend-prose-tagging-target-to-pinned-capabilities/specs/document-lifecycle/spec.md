# document-lifecycle — spec delta

## MODIFIED Requirements

### Requirement: Prose tagging marker hygiene
All `xspec:` markers SHALL be machine-checkable contract surface: every
occurrence of the literal string `xspec:` in governance Markdown MUST parse
against the canonical grammar (`xspec:candidate` open fence,
`/xspec:candidate` close fence, `xspec:supersedes` inline marker, with
space-separated unquoted `key=value` attributes), every marker target MUST
resolve, and candidate blocks MUST be properly fenced — no nesting, no
crossing of Markdown heading boundaries, and no unmatched open or close
fence. Deterministic health tooling SHALL report violations as findings.

A marker target resolves in ONE of two forms. The IN-TREE form names a spec
capability id under `openspec/specs/`, or a capability in an active change's
`specs/` while it is pre-promotion. The PINNED form, `pinned:<pin-id>/<capability>`,
names a capability of a NEUTRAL PRODUCT THIS REPOSITORY PINS: `<pin-id>` is the
identifier of a pin record the repository carries, and `<capability>` is the
capability name as the pinned product holds it. The literal prefix `pinned:` is
RESERVED and is the discriminator between the two forms; a capability id MUST
NOT contain a colon.

THE PINNED FORM'S LEXICAL GRAMMAR IS CLOSED, AND IT IS CHECKED BEFORE ANY PATH
IS BUILT. The value after `pinned:` SHALL be exactly TWO components separated by
exactly ONE `/`, and each component SHALL match `[a-z0-9]+(-[a-z0-9]+)*` — so a
component can carry no `/`, no `.`, no `:`, no whitespace and no upper-case
letter, and cannot be empty. A pinned value that does not match this grammar —
an extra `/` segment, a dotted or traversal component, an empty component — MUST
be reported as a malformed pinned target, and the deterministic pass MUST make
that judgement BEFORE it constructs any pin-record path, performs any pin
lookup, or reads any file for it. The marker regexes accept any non-whitespace
attribute value and are NOT the guard; this grammar is. The PINNED form is admitted in an `xspec:candidate`
marker's `target=` attribute ONLY. An `xspec:supersedes` marker's
`spec=<capability>/<requirement-slug>` value MUST NOT carry the `pinned:`
prefix, and a `spec=` value that carries it MUST be reported: the spelling is
RESERVED AND REFUSED rather than merely undefined, because a `spec=` value
already carries a separator of its own and no pinned parse for it is defined —
a deferred form fails closed.

A PINNED target resolves when its `<pin-id>` resolves to a NEUTRAL-PRODUCT pin
record the RESOLUTION ROOTS carry — a `contracts/<pin-id>-pin.yaml` declaring
`kind: pinned_contract_manifest`, the shape `neutral-product-pin` requires for
an external neutral product. A pin-shaped record of another kind, such as
`kind: pinned_workflow`, MUST NOT resolve a pinned target: it pins executable
governance code rather than a product whose units are capabilities, so it has
no capability set for the name to be about. THE KIND ALONE IS A LABEL, NOT A
PIN: the record MUST also be COMPLETE FOR ITS OWN RECORD SHAPE. THE SHAPE IS
THE UNIT OF THAT JUDGEMENT AND THE `revision_kind` ALONE IS NOT: two records
may declare `revision_kind: commit` and be complete on DIFFERENT member sets,
so a single required-member list keyed on the revision kind would refuse one of
them for carrying the other's shape.

AND THE MEMBER SET OF A SHAPE IS THE SHAPE'S SHAPE-GUARD-REQUIRED SET: EXACTLY
THE TOP-LEVEL MEMBERS THAT SHAPE'S IN-TREE PIN VERIFIER REFUSES-WHEN-ABSENT IN
ITS PURE, SOURCE-FREE SHAPE GUARDS — the refusals whose ONLY INPUT IS THE
RECORD, which is what the verifiers' reader and guard functions run before any
checkout, any `git` call and any network read — MEASURED FROM THE VERIFIER
SCRIPTS. This grammar RESTATES no shape and OWNS no field list.
`neutral-product-pin`'s ratified requirement *An external neutral product is
pinned by commit and digest, never by tag* supplies members WHERE IT NAMES THEM,
and it does not name them everywhere: it is SILENT on the whole-tree digest
shape and on the published artifact's `package` and `binary`, so the
shape-guard-required set COMPLETES it rather than competing with it.

WHY THE SHAPE GUARD AND NOT THE FULL VERIFIER. This resolver judges whether a
NAME resolves to a pin record OF AN ADMITTED SHAPE; it NEVER judges whether the
pin is FAITHFUL TO ITS SOURCE. SO THE COMPLETENESS CHECK IS NECESSARY FOR THE
SHAPE'S FULL VERIFIER AND DELIBERATELY NOT SUFFICIENT FOR IT, AND THAT IS BY
DESIGN, on two grounds stated once. FIRST, on a landed tree every record
ALREADY passes its full verifier, those verifiers being required checks, so
nothing the full verifier would catch can reach this resolver on a landed tree
at all; what the check defends is the OFFLINE JUDGEMENT over arbitrary trees —
a fixture tree, an aggregate of repositories, an added `contracts/evil-pin.yaml`
— where no verifier has run. SECOND, a SOURCE-DEPENDENT check cannot be part of
an offline, tree-local resolver without reproducing the verifier's I/O, which is
exactly the checkout, `git` and network work this pass is forbidden.
`scripts/validate-openreposhape-pin.py`'s `pin-surface-undeclared` (`:515-530`)
is the measured example of a full-verifier check that stays OUTSIDE this
contract: it compares the record's declared surface against the files the
RESOLVED SOURCE carries (`source.paths()`, `:520`), so it can refuse a record
that no shape guard can fault, and reproducing it here would mean resolving the
source. What the set DOES close is the other direction: a resolver that ACCEPTED
what the shape's own GUARD REFUSES would, on exactly those trees, admit a record
the repository's own gate rejects at its first shape check. Where the ratified
text names a member NO guard refuses-when-absent — `pinned_by_commit_only:` is
the one such member measured — that is the text's obligation on the pin's
AUTHOR, enforced by `neutral-product-pin`'s own machinery, and it is NOT a
resolution prerequisite here; the set is neither narrower nor wider than the
guards, and an equivalence test named below holds it there.

Measured over every `pinned_contract_manifest` record this tree carries — five,
on `origin/main` — there are THREE shapes.

(a) THE ENUMERATED COMMIT-PINNED SOURCE PIN. Shape-guard-required:
`revision_kind`
(`scripts/verify-openxwallet-pin.py:219`,
`scripts/validate-openreposhape-pin.py:239`), `commit` (`:227`, `:247`),
`files` (`:392`, `:438`), and EXACTLY ONE PRODUCT-IDENTITY MEMBER, whose
spelling differs with how the product is mounted: `submodule_path` for a
submodule-mounted product (`scripts/verify-openxwallet-pin.py:194`) and
`source_repository` for one resolved from its host
(`scripts/validate-openreposhape-pin.py:258`). AT THE RECORD GRAIN the table
resolves to exactly that record's verifier's set — neither the union of the two
(which would refuse `contracts/openxwallet-pin.yaml` for lacking
`source_repository`) nor their intersection (which would admit a record with no
product identity at all). `files:` entries are MAPPINGS carrying a `path` and
its `sha256` (`contracts/openxwallet-pin.yaml:70,80-95`;
`contracts/openreposhape-pin.yaml:134,135-196`), and a `files:` list that is
absent or empty is refused (`scripts/verify-openxwallet-pin.py:392-397`,
`scripts/validate-openreposhape-pin.py:438-443`). THAT refusal reads THE RECORD
ALONE — `pin.get("files")`, a type test and a non-empty test, consulting no
source — and so belongs to the set; it nonetheless sits INSIDE `verify()`,
behind that verifier's source checks, so it cannot be CALLED source-free, and
the equivalence test below pins it by a MEASURED CITATION instead of by calling
it. It is the only member of any shape in that position, measured.
`pinned_by_commit_only:` is NOT in the shape-guard-required set: both verifiers
read it with an absent-is-empty default and refuse it only when it is PRESENT
and not a list (`scripts/verify-openxwallet-pin.py:443-448`,
`scripts/validate-openreposhape-pin.py:487-491`). It is nonetheless of a
DIFFERENT FORM from `files:` and MUST NOT be judged by one rule with it: its
entries are PATH-ONLY STRINGS carrying no digest of their own
(`contracts/openxwallet-pin.yaml:104-110`;
`contracts/openreposhape-pin.yaml:201-246`), the publisher having published no
per-file digest for those members, so requiring a `sha256` of them would
require an invented row.

(b) THE WHOLE-TREE DIGEST COMMIT-PINNED SOURCE PIN. Shape-guard-required, and
the two verifiers agree member for member: `submodule_path`
(`scripts/verify-opendox-pin.py:215`, `scripts/verify-openxdox-pin.py:257`),
`revision_kind` (`:226`, `:276`), `commit` (`:234`, `:284`),
`digest_algorithm` (`:246`, `:307`), `digest_definition` (`:253`, `:314`) and
`digests` as a MAPPING (`:262`, `:322`) carrying `tree_sha256` (`:269`,
`:329`), with NEITHER `files:` NOR `pinned_by_commit_only:`
(`contracts/opendox-pin.yaml:92-95,108-110`;
`contracts/openxdox-pin.yaml:76-79,92-94`). `digest_algorithm` and
`digest_definition` are not decoration: each verifier refuses a value other
than the one it implements, because a definition it cannot compute is an
unanswerable question rather than a finding about the tree. ONE digest over the
whole tree leaves no member undeclared, which is the ground on which the
published-artifact shape needs no enumeration either
(`openspec/specs/neutral-product-pin/spec.md:59-61`).

(c) THE PUBLISHED-ARTIFACT PIN. Shape-guard-required — NINE members, all from
`scripts/validate-openspec-cli-pin.py`: `revision_kind` (`:592`), `version`
(`:601`), `integrity` (`:619`), `shasum` (`:646`), `package` (`:658`),
`lockfile` (`:698`), `lockfile_integrity` (`:708`), `lockfile_packages`
(`:731`) and `binary` (`:748`)
(`contracts/openspec-cli-pin.yaml:282,289,297,299,308,328-330,370`). The
ratified text reaches six of the nine — the artifact's digest as the referent
with `revision_kind` declared accordingly (`:46-48`), NEITHER per-file list
(`:55-56`), "every field the consumer's verifier checks — including any
secondary address the registry publishes" (`:62-65`), and the vendored
resolution *A pinned artifact that resolves dependencies at install time
carries a vendored lockfile, and the install runs through it* obliges, "a
lockfile … addressed by a digest over its exact bytes recorded in the pin,
together with the size of the tree it locks" (`:669-673`), which is `lockfile`,
`lockfile_integrity` and `lockfile_packages` and not `lockfile` alone. It does
NOT reach `package` or `binary`, which name the product the referent is OF and
the executable it installs; the verifier refuses a record without either
(`:657-663`, `:747-754`), so the set carries them. `dispositions:` is NOT in
the set: it is read with an absent-is-empty default (`:801-803`).

A record that matches NO admitted shape, and a record that matches one shape
but LACKS a member THAT SHAPE requires — no `revision_kind`, a `revision_kind`
without its referent, or a required member of that shape missing or malformed —
is an INVALID PIN: it MUST be reported with a finding NAMING THE SHAPE TRIED
AND THE FAILING MEMBER, and MUST NOT resolve a pinned target, so neither a file
added to `contracts/` carrying only `kind:` nor one carrying a kind and a
partial member set can make an arbitrary pinned target resolve. A record
carrying BOTH a whole-tree `digests.tree_sha256` AND a `files:` list matches
neither (a) nor (b) and MUST be reported on that ground: `neutral-product-pin`'s
ratified text is SILENT on the whole-tree shape — the spellings
`digest_definition`, `digests` and `tree_sha256` occur nowhere under
`openspec/specs/`, (b) being a REALIZED record shape rather than a spec-named
one — so the mixed form is admitted by no text and fails closed on that
capability's own refusal rule (`openspec/specs/neutral-product-pin/spec.md:89`)
rather than resolving on the strength of whichever half is complete.
WHERE THAT LIST COMES FROM IS THE POINT, AND IT IS NOT THIS
GRAMMAR: THE CODE-FIXED VALIDATOR HOLDS A PER-SHAPE REQUIRED-MEMBER TABLE,
reviewed with the resolver at authoring time, covering every RECORD SHAPE this
tree's `pinned_contract_manifest` records carry today (the three above,
measured over all five records) — `neutral-product-pin`'s ratified text where
that text names members, COMPLETED BY THE SHAPE'S SHAPE-GUARD-REQUIRED SET
where it is silent. That table is not a SECOND, independently-authored list — it is
not restated as PROSE in this requirement, where a restatement could drift
unreviewed. AND IT SHALL BE PINNED TO THE VERIFIERS BY AN EQUIVALENCE TEST
rather than by a promise, IN TWO LEGS. THE RECORD LEG, over each real
`pinned_contract_manifest` record on the tree: the adapter ACCEPTS the record;
for every member `m` IN the table for that record's shape, the adapter REFUSES
the record with `m` removed and NAMES `m`; and for every top-level member of
that record NOT in the table AND NOT THE `kind:` DISCRIMINATOR, the adapter
still ACCEPTS the record without it — so the table is neither WIDER nor
NARROWER than declared. `kind:` is EXEMPT from that second arm and is not a
table member of any shape, because `kind: pinned_contract_manifest` is the
PRECONDITION this grammar gates on BEFORE any shape is selected: a record
without it is not a record of the kind a pinned target may name, so removing it
asks a question about a different record rather than about the table. THE GUARD LEG, which
is what holds the table to the VERIFIERS rather than to itself: where the
shape's verifier exposes an IMPORTABLE, SOURCE-FREE guard for a table member,
that guard SHALL be called on the record with `m` removed and asserted to
refuse; and where a member's refusal is reachable only inside `verify()` and
cannot run source-free, the table entry SHALL instead carry a MEASURED CITATION
in the adapter's own source — the script, the line and the refusal text quoted —
and the test SHALL assert that the cited line of the cited script still holds
that text, a READ of the verifier rather than a run of it. A table that drifted
NARROWER than its guards would admit a record the repository's own gate refuses
at its first shape check; one that drifted WIDER would refuse a record the gate
admits; either leg fails, so the table cannot part from the verifiers without a
red check. Of two INDEPENDENTLY-AUTHORED lists the
WEAKER is always the one that admits, which is why this requirement fixes the
SOURCE of the table and then pins it to running code rather than forbidding the
table. A record declaring a `revision_kind` the
table does not recognize, and a record whose member set matches no shape the
table holds, MUST each be reported as an invalid pin: an unrecognized kind and
an unrecognized shape are both deferred cases, and Principle VII requires each
fail closed rather than resolve on the strength of an unfamiliar label.

THE COMPLETENESS JUDGEMENT SHALL BE REACHED THROUGH A CODE-FIXED ROUTE, AND
THE PASS SHALL NOT EXECUTE, IMPORT OR OPEN ANY PATH SELECTED BY THE RECORD
UNDER JUDGEMENT. A pin record is DATA the pass is judging; a member of it —
`verify_pin:` or any other — is NEVER a dispatch key, an import target or a
path to run, because a record that chooses which code judges it is a record
that judges itself, and an added `contracts/<anything>-pin.yaml` could then
select any path in the checkout. THE ROUTE SHALL BE ONE SHARED, PURE,
NON-EXECUTING ADAPTER for `pinned_contract_manifest` records — fixed at
authoring time and reviewed with the resolver, living either in the resolver's
own module or in one shared helper module beside it — which HOLDS the per-shape
table, READS THE RECORD AND NOTHING ELSE, and NEVER EDITS OR CALLS the five
per-product pin verifiers, whose `verify()` routines need a checkout, `git` or
the network. A `verify_pin:` value is data the adapter MAY compare and MUST NOT
follow: a value differing from what the adapter holds for that record is itself
a controlled finding rather than a redirection. `verify_pin:` is therefore NOT a
prerequisite of resolution and NOT part of the shape this grammar requires; it
is a member today's five records happen to carry, and the pass may compare it
but MUST NOT follow it. THE JUDGEMENT IS ALSO OFFLINE AND IS A CONTROLLED
FINDING: it reads the resolution roots' trees and MUST NOT perform a fetch or a
remote comparison, and a record that fails is an unresolved pinned target
reported as a finding, never an exception that takes the run down, on the same
terms as the corrupt-record rule below.

THE PASS RESOLVES A PIN RECORD AGAINST EXACTLY THE ROOT PRECEDENCE THE
IN-TREE ARM ALREADY USES, AND NAMES THE ROOT IT USED. Capability resolution
today reads the DOCUMENT'S OWN REPOSITORY ROOT FIRST AND THE `openxFactory`
ROOT SECOND (`scripts/doc_health/families.py:1317-1321`, over
`Context.repo_paths`, `scripts/doc_health/runner.py:39`); a single-repository
run has one root and no fallback. The pinned arm SHALL use that precedence
UNCHANGED and SHALL invent none of its own, so the ORDER IS UNCHANGED AND
DETERMINISTIC FOR THE ROOTS PRESENT in the run — the document's own repository
root first, then the `openxFactory` root where the run is an aggregate whose
roots differ. WHAT IS GUARANTEED IS THAT ORDER AND NOT AN IDENTICAL OUTCOME
ACROSS INVOCATION SCOPES: a single-repository run has ONE root and no fallback,
so a marker whose pin record lives only in the `openxFactory` root resolves in
an aggregate run and is an UNRESOLVED pinned target in a single-repository run
of another repository. That difference is a difference of THE ROOT SET THE RUN
WAS GIVEN, not of a precedence the arm invented, and the arm SHALL NOT widen
its root set to close it; and EVERY finding the pinned arm emits SHALL NAME THE
ROOT OR ROOTS it resolved against, or failed to, since under two roots a bare
"no pin record" sentence cannot be acted on and under one root the named root
is what makes the difference readable. THE RECORD MUST ALSO BE A FILE OF THAT ROOT'S `contracts/`
DIRECTORY, RESOLVED: the pass MUST
resolve the candidate path and refuse to read it unless the resolved path stays
inside that root's `contracts/` directory, and a symlink that leaves it MUST be
refused rather than
followed — the lexical grammar stops a `..` in the marker, and only resolved
containment stops a committed symlink. AND THE BOUNDARY ITSELF MUST BE CHECKED
BEFORE ANY CANDIDATE IS, because a boundary that can be redirected is not a
boundary: the pass SHALL require that root's `contracts` BE A REAL,
NON-REDIRECTING DIRECTORY INSIDE THE ROOT — it is a directory, it is not a
symlink, and its RESOLVED path equals its LEXICAL path — and SHALL make that
judgement BEFORE it resolves any candidate pin path. Where `contracts` is a
symlink, to another directory inside the repository or to one outside it, the
PINNED ARM REFUSES FOR THAT ROOT as a whole with a controlled finding NAMING
THE ROOT, and NO candidate is resolved and NOTHING is read. Comparing a
candidate against a RESOLVED `contracts` directory would otherwise accept and
read a file outside the lexical registry the boundary names, the redirection
having moved the boundary rather than been caught by it. A pin record that EXISTS but
cannot be read as a mapping carrying a `kind` — invalid YAML, a non-mapping
document, or no `kind` member — MUST be reported as an unreadable pin record
and MUST NOT resolve a pinned target, and the pass MUST complete rather than
abort: a corrupt record in the registry is a controlled finding, never an
exception that takes the run down with it. The `<capability>` segment MUST be well formed, and it MUST
additionally appear in the pin record's own capability enumeration WHERE THAT
RECORD CARRIES ONE; where the record carries no such enumeration, resolution
rests on the pin alone and the capability name is taken as declared. A PIN
RECORD'S CAPABILITY ENUMERATION IS ONE NAMED MEMBER AND NOT A SEARCH: a
top-level `capabilities:` sequence of capability names on the pin record. A
record without that member carries no enumeration for this purpose, and the
pass MUST NOT read capability names out of any other member — a file list, a
digest list or a member list is not a capability list, and inferring one from
them is non-deterministic. The enumeration SHALL be NON-EMPTY: an empty
sequence is not a statement that the product has no capabilities, it is a
broken member, and it MUST NOT be read as a valid enumeration nor as an absent
one. A `capabilities:` member that is PRESENT but is not a NON-EMPTY sequence of
well-formed capability names — including an empty sequence, a null value, a
scalar, a mapping, or a sequence carrying an item that is not a capability-shaped
name — MUST be reported as a malformed enumeration against the pin record, and MUST NOT be read as an absent
enumeration; while it is malformed, a pinned target naming that record does NOT
resolve. THAT OBLIGATION IS REACHED THROUGH THE MARKER AND NOT BY A SWEEP: the
pass reads a pin record because a live marker names it, and this capability
imposes NO registry-wide scan of pin records no live marker references. A pin
record's own well-formedness, unreferenced, is `neutral-product-pin`'s business
and not the marker grammar's. A deferred or broken enumeration fails closed rather than degrading
open. Whether a pin record may carry `capabilities:` is owned by
`neutral-product-pin`, not by this capability. This
conditional arm is deliberate: it binds automatically, with no further grammar
delta, as soon as a pin record enumerates capabilities. It is NOT a licence to
read the pinned product over the network — the deterministic pass reads the
resolution roots' trees and nothing else.

WHEN A TARGET CAPABILITY EXITS THE CORPUS, the marker SHALL either take the
pinned form naming the product that now holds the capability, or the block
SHALL be unfenced. A stale target MUST NOT be silently retargeted to a
different capability, and MUST NOT be silently deleted: retargeting makes the
marker name a capability the tagged prose is not about, and deleting the marker
drops the block out of the conversion queue without a record that it was
dropped. Unfencing is a lawful outcome that is CHOSEN and visible in the diff,
not the thing that happens when nobody decides.

#### Scenario: A marker is malformed or unknown
- **WHEN** the string `xspec:` occurs in a governance document but does not parse as a canonical `xspec:candidate`, `/xspec:candidate`, or `xspec:supersedes` marker
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A marker target does not resolve
- **WHEN** a marker names an IN-TREE `target=<capability>` or `spec=<capability>/<requirement-slug>` — a value carrying no `pinned:` prefix — that does not exist under `openspec/specs/` or in an active change's spec deltas
- **THEN** the deterministic health pass MUST report it as a hygiene finding
- **AND** a target carrying the `pinned:` prefix is NOT judged by this scenario, which would otherwise report every well-formed pinned target

#### Scenario: A marker names a capability of a pinned neutral product
- **WHEN** a marker names a lexically well-formed `target=pinned:<pin-id>/<capability>`, `<pin-id>` resolves under the in-tree arm's root precedence to a pin record whose path stays inside that root's `contracts/` directory when resolved, which declares `kind: pinned_contract_manifest` AND carries every member required by the RECORD SHAPE it matches — a shape `neutral-product-pin`'s ratified text obliges or this tree's measured records realize — and which EITHER carries no `capabilities:` member OR carries a well-formed non-empty one in which `<capability>` appears
- **THEN** the target MUST resolve
- **AND** where the record carries no `capabilities:` member, resolution MUST rest on the pin alone and the pass MUST NOT read the pinned product over the network
- **AND** a malformed enumeration, and a well-formed enumeration in which `<capability>` does not appear, are OUTSIDE this scenario and are judged by their own scenarios below

#### Scenario: A pinned capability is absent from the pin record's enumeration
- **WHEN** a marker names `target=pinned:<pin-id>/<capability>`, the record for `<pin-id>` carries a well-formed non-empty `capabilities:` member, and `<capability>` does not appear in it
- **THEN** the deterministic health pass MUST report it as a hygiene finding naming the enumeration
- **AND** the target MUST NOT resolve

#### Scenario: A pinned target names a record that is not a neutral-product pin
- **WHEN** a marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` declares a kind other than `pinned_contract_manifest`
- **THEN** the deterministic health pass MUST report it as a hygiene finding
- **AND** the target MUST NOT resolve on the strength of that record

#### Scenario: A pinned target is lexically malformed
- **WHEN** a marker names a `target=pinned:…` value that is not exactly two `[a-z0-9]+(-[a-z0-9]+)*` components separated by one `/`
- **THEN** the deterministic health pass MUST report it as a malformed pinned target
- **AND** the pass MUST NOT construct a pin-record path, perform a pin lookup, or read any file for that value

#### Scenario: A pin record's capability enumeration is malformed
- **WHEN** a live marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` carries a `capabilities:` member that is not a NON-EMPTY sequence of well-formed capability names, an empty sequence among those shapes
- **THEN** the deterministic health pass MUST report a malformed-enumeration finding against that pin record
- **AND** that pinned target MUST NOT resolve while the enumeration is malformed
- **AND** the pass MUST NOT treat the malformed member as an absent enumeration
- **AND** the pass MUST NOT be required to scan pin records that no live marker names: this obligation is reached through the marker

#### Scenario: A pin record declares the kind but is incomplete for its record shape
- **WHEN** a live marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` declares `kind: pinned_contract_manifest` but matches no admitted record shape, or matches one and lacks a member THAT SHAPE requires — no `revision_kind`, a `revision_kind` without its required referent, a required member of that shape missing or malformed, or the members of two shapes mixed in one record
- **THEN** the deterministic health pass MUST report it as an invalid pin, naming the shape tried, the failing member and the root it resolved against
- **AND** the target MUST NOT resolve on the strength of the declared kind
- **AND** the pass MUST reach that judgement through ONE shared, pure, non-executing adapter — a PER-SHAPE required-member table read from `neutral-product-pin`'s ratified text where that text names members and completed by the shape's SHAPE-GUARD-REQUIRED SET where it is silent, reviewed with the resolver and held in the adapter rather than restated as prose in this requirement

#### Scenario: The per-shape table and the shape's own guards disagree
- **WHEN** the per-shape required-member table is checked against a real `pinned_contract_manifest` record, member by member over that record's own top-level members
- **THEN** the RECORD LEG MUST hold: the adapter accepts the record; it refuses the record with any member of the table removed and NAMES that member; and it still accepts the record with any top-level member removed that is neither in the table nor the `kind:` discriminator, that discriminator being the precondition gated on before any shape is selected rather than a member of any shape's table
- **AND** the GUARD LEG MUST hold: where the shape's verifier exposes an importable, source-free guard for a table member, that guard MUST be called on the record with the member removed and MUST refuse
- **AND** where a table member's refusal is reachable only inside the verifier's full `verify()` and cannot be run source-free, the table entry MUST instead carry a MEASURED CITATION in the adapter's source — script, line and refusal text quoted — and the test MUST assert that the cited line of that script still holds that text, reading the verifier rather than running it
- **AND** a table NARROWER than its guards MUST fail that test, since it would admit on a fixture or side run a record the repository's own required check refuses at its first shape check
- **AND** a table WIDER than its guards MUST fail it too, since it would refuse a record that gate admits
- **AND** the equivalence MUST be asserted by a test over each real record rather than stated as an intention, the table being code that can drift from the guards it tracks
- **AND** the equivalence MUST NOT be claimed to make the adapter's judgement SUFFICIENT for the shape's full verifier: a source-dependent check such as `pin-surface-undeclared` stays outside this contract, the adapter being NECESSARY and by design not sufficient

#### Scenario: A pin record addresses its whole tree by one digest
- **WHEN** a live marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` declares `kind: pinned_contract_manifest` with `revision_kind: commit`, a `commit`, a `submodule_path`, a `digest_algorithm`, a `digest_definition` and a `digests` mapping carrying `tree_sha256`, and carries neither `files:` nor `pinned_by_commit_only:`
- **THEN** the record MUST be judged COMPLETE against that shape and the target MUST resolve on it, one digest over the whole tree leaving no member undeclared
- **AND** the pass MUST NOT report the absent per-file lists as missing members, the enumeration those lists provide being supplied here by the tree digest
- **AND** a record carrying both that tree digest and a `files:` list MUST be reported as an invalid pin naming both shapes tried, no ratified text admitting the mixture

#### Scenario: A source pin enumerates its members in two different forms
- **WHEN** a live marker names a record whose `files:` entries are mappings carrying a `path` and its `sha256` and whose `pinned_by_commit_only:` entries are path-only strings
- **THEN** both forms MUST be accepted as declared, a `pinned_by_commit_only:` entry carrying no `sha256` being the valid form rather than a malformed member
- **AND** a `files:` entry carrying no `sha256`, and a `pinned_by_commit_only:` entry that is a mapping rather than a path string, MUST each be reported as a malformed member naming the list it came from
- **AND** an ABSENT `pinned_by_commit_only:` MUST NOT be reported as a missing member, both of this shape's verifiers reading it with an absent-is-empty default and refusing it only when it is present and not a list

#### Scenario: A pin record names the code that would judge it
- **WHEN** a live marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` carries a `verify_pin:` member naming an arbitrary path in the checkout
- **THEN** the deterministic health pass MUST NOT execute, import or open that path
- **AND** the completeness judgement MUST be made by ONE shared, pure, non-executing adapter — the resolver's own module or one shared helper module beside it — which reads the record and nothing else
- **AND** where the record's `verify_pin:` value differs from what that adapter holds for `<pin-id>`, the pass MUST report that disagreement as a finding rather than follow the record
- **AND** that finding MUST stand BESIDE the resolution rather than in place of it: `verify_pin:` is not a prerequisite of resolution, so a record complete for its record shape still resolves while the disagreement is reported

#### Scenario: A pin path resolves outside the contracts directory
- **WHEN** the candidate pin-record path for `<pin-id>` resolves outside the `contracts/` directory of the root it was resolved against, whether by symlink or otherwise
- **THEN** the deterministic health pass MUST refuse to read it
- **AND** the target MUST NOT resolve
- **AND** the refusal MUST be reported as a hygiene finding naming that root, rather than silently skipped

#### Scenario: A root's contracts directory is itself a symlink
- **WHEN** a resolution root's `contracts` is not a real, non-redirecting directory inside that root — it is a symlink to another directory inside the repository, a symlink to one outside it, or not a directory at all
- **THEN** the deterministic health pass MUST make that judgement BEFORE resolving any candidate pin path, and the pinned arm MUST refuse for that root without reading anything
- **AND** the refusal MUST be reported as a controlled finding naming that root
- **AND** no pinned target MUST resolve against that root, a boundary that can be redirected being no boundary: comparing a candidate against a resolved `contracts` directory would otherwise read a file outside the lexical registry

#### Scenario: A pinned target resolves under an aggregate run's second root
- **WHEN** a document in another repository carries a pinned target whose pin record exists only in the `openxFactory` root of an aggregate run
- **THEN** the target MUST resolve against that root, by the same precedence the in-tree capability arm uses — the document's own repository root first, the `openxFactory` root second
- **AND** where both roots carry a record for `<pin-id>`, the document's own repository's record MUST be the one read
- **AND** the pinned arm MUST invent no precedence of its own: the ORDER is unchanged and deterministic for the roots present, an aggregate run carrying a second root that a single-repository run does not have

#### Scenario: A pinned target's record lives only in the root a single-repository run does not have
- **WHEN** a single-repository doc-health run of another repository reads a document whose pinned target's pin record exists only in the `openxFactory` root
- **THEN** that run has ONE root and no fallback, so the target MUST NOT resolve and MUST be reported as an unresolved pinned target
- **AND** the finding MUST NAME the root it searched, so the difference from the aggregate run reads as a difference of root set rather than of precedence
- **AND** the pass MUST NOT widen its root set to reach that record, the root set being the run's input rather than the arm's choice

#### Scenario: A pin record named by a marker cannot be read
- **WHEN** a live marker names `target=pinned:<pin-id>/<capability>` and the record for `<pin-id>` exists but is not readable as a mapping carrying a `kind` — invalid YAML, a non-mapping document, or no `kind` member
- **THEN** the deterministic health pass MUST report it as a hygiene finding against that pin record
- **AND** the target MUST NOT resolve
- **AND** the pass MUST complete rather than abort

#### Scenario: A pinned target names a pin no resolution root carries
- **WHEN** a marker names `target=pinned:<pin-id>/<capability>` and no pin record for `<pin-id>` exists under any root of the run's precedence
- **THEN** the deterministic health pass MUST report it as a hygiene finding
- **AND** the finding MUST name the pin registry as the thing that failed to resolve, not `openspec/specs/`
- **AND** the finding MUST name the root or roots searched

#### Scenario: A supersedes marker carries the reserved pinned prefix
- **WHEN** an `xspec:supersedes` marker's `spec=` value begins with the reserved `pinned:` prefix
- **THEN** the deterministic health pass MUST report it as a hygiene finding
- **AND** the finding MUST state that the pinned form is admitted only in a candidate marker's `target=` attribute

#### Scenario: A target capability leaves the corpus
- **WHEN** a change removes a capability that live `xspec:` markers target
- **THEN** each affected marker MUST take the pinned form naming the product that now holds the capability, or its block MUST be unfenced
- **AND** the marker MUST NOT be retargeted to a different capability, nor deleted, as a way of clearing the finding

#### Scenario: A candidate block is structurally invalid
- **WHEN** an `xspec:candidate` block nests inside another candidate block, spans a Markdown heading, or lacks a matching open or close fence
- **THEN** the deterministic health pass MUST report it as a hygiene finding

#### Scenario: A supersedes marker never acquires a change id
- **WHEN** an `xspec:supersedes` marker persists without a `change=` attribute beyond the doc-health aging threshold
- **THEN** the health pass MUST report it as an aging finding rather than accepting it as a permanent state
