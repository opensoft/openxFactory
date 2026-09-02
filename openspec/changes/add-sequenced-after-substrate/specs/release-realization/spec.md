# release-realization Specification Delta

This delta ADDS a machine-readable ORDERED-DELTA PARENT declaration — the
optional front-matter field `sequenced_after:` — as a sibling of the existing
`code_surface:` / `target_release:` / `scope_globs:` realization-axis
declarations, so that the ordered-delta chain this capability already REQUIRES
authors to sequence in prose becomes WALKABLE by a machine.

THE DELTA IS ALL-ADDED, AND THAT IS A MEASURED CHOICE RATHER THAN A STYLE.
Two ACTIVE ratified changes write this specification today, and both of the
requirements a MODIFIED block here would naturally have taken are among them:
`add-structured-scope-substrate` holds an active `## MODIFIED Requirements`
block over "Realization axis declaration", and
`govern-sibling-added-modified-deltas` holds one over "Ordered deltas and branch
vocabulary". Under that second change's own ratified rule, a MODIFIED block over
either title would have to be declared relative to the sibling's outcome AND
would incur its archive-order hold. An ALL-ADDED delta over NOVEL requirement
titles owes neither, restates no promoted text, drops none, and therefore owes no
`Modified over`, `Removed from canon by` or `Merged into` marker. The measurement
is recorded in `proposal.md` § The sibling rule, measured.

NOTHING PROMOTED IS CHANGED. "Ordered deltas and branch vocabulary" keeps its
prose sequencing obligation intact and unaltered: an author who references the
earlier change in prose still satisfies it. `sequenced_after:` is an ADDITIONAL,
OPTIONAL, machine-readable declaration whose ABSENCE leaves every existing change
— all 151 in the corpus — validating and archiving exactly as it does today.

## ADDED Requirements

### Requirement: Machine-readable ordered-delta parent declaration
A change proposal's OPTIONAL front-matter field `sequenced_after:` SHALL carry a
SEQUENCE of ordered-delta PARENT change references, and the empty sequence
`sequenced_after: []` SHALL be a POSITIVE, RATIFICATION-COVERED DECLARATION that
the change is a chain ROOT rather than a formatting artifact. Declaring the field
is OPTIONAL; declaring it MALFORMED is not.
The field exists because this capability's "Ordered deltas and branch vocabulary"
requirement obliges a change to sequence explicitly against an earlier change's
outcome, and that obligation is discharged today only in PROSE — which a machine
cannot walk. A prose `Sequenced-after:` header, a whole-token occurrence of a
sibling change id anywhere in a proposal's text, a change-folder name, a commit
timestamp, and a `created:` date SHALL NOT constitute a machine-readable parent
declaration: none of them can distinguish a parent from a mention, none can
express a fork, and each is author-mutable in the same document the author writes.

ABSENCE IS FAIL-CLOSED AND IS NOT A ROOT CLAIM. A change that omits
`sequenced_after:` SHALL be treated as having made NO declaration about its
position in any chain — never as a declared root, and never as a change with no
parent. This is the same fail-closed posture the `scope_globs:` sibling takes,
where absence means "not provenance-eligible" rather than "all paths": a field
whose absence carries an authorizing meaning is a field that rewards omission.
Existing changes that declare no `sequenced_after:` SHALL be grandfathered with
NO migration pass, and the prose sequencing obligation SHALL remain sufficient
for every purpose other than a mechanical walk.

#### Scenario: A change declares its ordered-delta parent
- **WHEN** a proposal modifies a requirement whose basis is an active ratified change and its realization seeks a mechanically walkable chain
- **THEN** it MAY declare `sequenced_after:` naming that change, and the declaration is the walkable link
- **AND** the prose reference the "Ordered deltas and branch vocabulary" requirement already obliges remains owed and is not replaced by it

#### Scenario: A change declares itself a root
- **WHEN** a proposal is the oldest writer of every requirement it touches and its author asserts root status
- **THEN** it declares `sequenced_after: []`, and that empty sequence is a positive claim covered by the change's ratification

#### Scenario: A change omits the field entirely
- **WHEN** a proposal declares no `sequenced_after:` at all
- **THEN** it validates and archives exactly as before, and no consumer may read the absence as a root claim or as an assertion that the change has no parent

### Requirement: Repository-qualified parent-reference syntax
Every `sequenced_after:` entry SHALL be either a BARE `<change-id>`, meaning a
change in the DECLARING repository's own corpus, or a QUALIFIED
`<repository>:<change-id>`, and a qualified entry naming the declaring repository
SHALL be equivalent to the bare form. The syntax is explicit because two rules a
consumer needs — "the chain is walked within one repository's own corpus" and
"an unresolvable reference refuses" — otherwise COLLIDE on a single input, an
entry naming another repository: read as bare it is unresolvable, and read as
out-of-scope it is silently skipped, which would fabricate a root out of a
declaration that says the opposite. A `<change-id>` SHALL match
`[a-z0-9][a-z0-9-]*` and SHALL NOT contain `/`, so a reference can never name a
nested path; a `<repository>` token SHALL match `[A-Za-z0-9_.-]+`, the same
repository-token grammar the origin-id declarations already use.

A FOREIGN-REPOSITORY ENTRY SHALL BE DECLARABLE, and its DISPOSITION SHALL BE THE
CONSUMER'S. This substrate defines what a cross-repository reference LOOKS like
and requires that it be well-formed; it does NOT decide whether a walk crosses
repositories. A consumer that walks within one corpus SHALL refuse such an entry
under a named identifier rather than skip it. The cross-repository "realizes the
neutral doctrine" relation between a domain change and an openxFactory change is
a PROSE relation, SHALL NOT be expressed as a `sequenced_after:` entry, and is
therefore never a hop.

#### Scenario: A bare entry names a change in the same repository
- **WHEN** an entry is a bare `<change-id>`
- **THEN** it references the declaring repository's own corpus and is resolved there

#### Scenario: An entry is qualified with the declaring repository
- **WHEN** an entry is `<repository>:<change-id>` and `<repository>` is the declaring repository
- **THEN** it is treated exactly as the bare `<change-id>` form

#### Scenario: An entry names a foreign repository
- **WHEN** an entry is qualified with a repository other than the declaring one
- **THEN** the declaration is still well-formed and validates
- **AND** a consumer that walks a single repository's corpus MUST refuse it under a named refusal identifier rather than skip it, because skipping would read as a root the declaration explicitly denies

#### Scenario: A prose relation to a neutral doctrine change
- **WHEN** a domain change realizes an openxFactory doctrine change
- **THEN** that relation is recorded in prose and MUST NOT be declared as a `sequenced_after:` entry

### Requirement: Strict loading of the realization-axis front-matter block
Every STRUCTURED field of the realization-axis front-matter block SHALL be read
by a STRICT loader that REFUSES, rather than silently resolves, each of:
duplicate keys at ANY level; YAML anchors (`&`); aliases (`*`); merge keys
(`<<:`); non-UTF-8 bytes; and a document over a declared size ceiling. This
requirement reaches `sequenced_after:` and `scope_globs:` alike, because a strict
loader that covers one structured field of a block and not the other is not a
strict loader — it is a loader with a documented hole in a trust-root surface.

THE HAZARD IS PRESENT IN SHIPPED CODE AND IS NAMED RATHER THAN GESTURED AT.
`scripts/scope_globs.py` parses the field's sub-block with `yaml.safe_load`, which
applies LAST-DUPLICATE-KEY-WINS SILENTLY. A proposal carrying two `scope_globs:`
blocks therefore shows a human reviewer the FIRST and authorizes the LAST, and
the same defect applied to `sequenced_after:` would show a reviewer one parent and
walk another. The downstream provenance-tie verifier ALREADY refuses these forms
on its own path, so a permissive loader here does not merely under-enforce: it
makes the neutral validator and the consuming verifier disagree about what the
same bytes mean, and a corpus that passes validation would refuse at the gate
while a corpus that fails validation could pass it.

#### Scenario: A proposal declares the same structured field twice
- **WHEN** a proposal's front matter carries two `sequenced_after:` blocks, or two `scope_globs:` blocks
- **THEN** the loader MUST refuse the document, naming the duplicated key
- **AND** it MUST NOT resolve the duplicate by last-wins or first-wins

#### Scenario: A declaration uses an anchor, alias, or merge key
- **WHEN** a structured realization-axis field is expressed using `&`, `*`, or `<<:`
- **THEN** the loader MUST refuse the document, naming the construct it refuses

#### Scenario: A declaration is well-formed under the strict loader
- **WHEN** every structured field appears exactly once, uses no anchor, alias, or merge key, and the document is UTF-8 and within the ceiling
- **THEN** the loader accepts it and validation proceeds to the shape and grammar checks

### Requirement: Parent-declaration validation
When `sequenced_after:` is present, house validation SHALL enforce its shape,
its entry grammar, and the RESOLVABILITY of every bare entry, and SHALL fail with
a message naming the offending entry and the rule it breaks. The shape SHALL be a
sequence — possibly empty — of non-empty strings, with no null members, no nested
collections, and no duplicate entries. Each entry SHALL conform to the
repository-qualified parent-reference syntax. Every BARE entry SHALL RESOLVE to
exactly one change in the declaring repository's own corpus under the ordered-delta
identity rules, so a dangling parent reference is a validation failure rather than
a defect discovered at a gate months later. A QUALIFIED FOREIGN entry SHALL NOT be
required to resolve, because the neutral validator cannot read another
repository's corpus; it SHALL be required only to be well-formed.

VALIDATION SHALL REFUSE A CYCLE and SHALL IMPOSE NEITHER A DEPTH LIMIT NOR A
FAN-OUT LIMIT. A cycle is refused because a chain that revisits a change id can
never reach a root under ANY consumer's policy, which makes it a well-formedness
defect rather than a policy judgement. A depth limit and a fan-out limit are
withheld for the opposite reason: both are authorization policy of a consuming
gate, and a number baked into the neutral field would either bind repositories
that never adopt the consuming axis or drift from the gate that enforces it. In
particular a MULTI-ENTRY declaration SHALL validate: an honest change with two
parents must be able to say so, because a substrate that forbade the second entry
would force under-declaration on a trust-root surface and would make a consumer's
fork refusal unreachable. This is the same posture the `scope_globs:` sibling
takes toward over-declaration, where a scope naming a floor path validates and the
verifier's floor override parks it at check time.

#### Scenario: A malformed parent declaration is validated
- **WHEN** `sequenced_after:` is not a sequence, holds a null or empty member, holds a nested collection, holds a duplicate entry, or holds an entry that breaks the reference grammar
- **THEN** validation MUST fail with a message naming the offending entry and the rule it breaks

#### Scenario: A bare entry names no change in the corpus
- **WHEN** a bare `<change-id>` entry resolves to no change directory in the declaring repository's active or archived corpus
- **THEN** validation MUST fail, because a dangling parent reference is unwalkable

#### Scenario: A declaration forms a cycle
- **WHEN** following `sequenced_after:` from a change revisits a change id already seen
- **THEN** validation MUST fail, naming the repeated id, because no consumer's policy can resolve a cycle to a root

#### Scenario: A change declares two parents
- **WHEN** `sequenced_after:` names two resolvable parents
- **THEN** validation accepts the declaration
- **AND** whether a two-parent chain is WALKABLE is the consuming gate's policy, which MUST refuse it under a named identifier if its walk admits only one parent

#### Scenario: A deep chain is validated
- **WHEN** a resolvable chain is longer than any consuming gate would walk
- **THEN** validation accepts it, because the depth ceiling belongs to the gate and not to the field

### Requirement: Ordered-delta identity survives archival
The CHANGE ID SHALL be the durable identity of an ordered-delta hop, and a
`sequenced_after:` entry SHALL remain resolvable after the change it names is
ARCHIVED. Archival MOVES a change directory and DATE-PREFIXES it, so a resolution
rule that searched only the active corpus would make every ordered-delta chain
SELF-DISABLE over time — and it would do so in the worst possible order, because
the ROOT of a chain is its oldest change and therefore the FIRST to archive.
Resolution SHALL therefore consider EXACTLY TWO locations:
`openspec/changes/<change-id>/`, and any directory matching the ANCHORED pattern
`openspec/changes/archive/<YYYY>-<MM>-<DD>-<change-id>/` where the date part is
exactly `\d{4}-\d{2}-\d{2}` and the remainder equals the change id EXACTLY. The
anchoring is required on BOTH sides: a prefix strip or a split on the first hyphen
would mis-resolve a change id that itself contains digits and hyphens, and an
unanchored active side would admit a nested `openspec/changes/<id>/openspec/changes/<id2>/`.

The UNION across both locations SHALL contain EXACTLY ONE directory: zero is
UNRESOLVABLE and two or more is AMBIGUOUS, and neither SHALL be resolved by
preference — one id matching two directories on a surface that authorizes
anything is not a case to decide by precedence. An ARCHIVED hop's declarations —
its lifecycle `Status`, its `scope_globs:`, and its `sequenced_after:` — SHALL be
read from the ARCHIVED directory, which carries the frozen ratified text.
ARCHIVAL SHALL NOT REWRITE PARENT DECLARATIONS: the archive gate SHALL NOT
rewrite, date-prefix, re-point or otherwise normalize any `sequenced_after:`
entry, so a chain's declared shape at ratification is the shape it still has years
later.

#### Scenario: A chain's root has archived
- **WHEN** a change's declared parent has since been archived to `openspec/changes/archive/<date>-<parent-id>/`
- **THEN** the bare entry still resolves, to that archived directory
- **AND** the parent's `Status`, `scope_globs` and `sequenced_after` are read from the archived directory's frozen text

#### Scenario: One change id matches two directories
- **WHEN** a change id resolves to both an active directory and an archived one, or to two archived directories under different dates
- **THEN** resolution MUST fail as ambiguous, and MUST NOT prefer either

#### Scenario: An archive directory name only shares a prefix
- **WHEN** an archived directory's name after the date part is a longer string that merely starts with the change id
- **THEN** it MUST NOT resolve, because the match is anchored and exact on both the date and the remainder

#### Scenario: A change archives
- **WHEN** a change carrying a `sequenced_after:` declaration passes its archive gate
- **THEN** the declaration's entries are carried through byte-unchanged, and the gate MUST NOT rewrite or re-point them to archived paths

### Requirement: Root status is proved and never inferred from absence
A consumer of `sequenced_after:` SHALL NOT infer root status from the ABSENCE of
the field, and SHALL NOT treat an explicit `sequenced_after: []` as sufficient on
its own where a mechanical cross-check can contradict it. This is stated as
NEUTRAL DOCTRINE, at the substrate, because the alternative reading is a
fail-OPEN default that every future consumer would otherwise rediscover: before
the field is adopted no change carries it, so "absence is the root" makes every
chain read as a depth-one root and silently authorizes on the terminal change's
own declarations, with the refusal it was supposed to raise UNREACHABLE because a
chain is undetectable. After adoption the same reading makes declaration
AUTHOR-OPT-IN, and under any narrowing composition it PENALIZES honest
declaration and REWARDS omission. A control that rewards omission is not a
control.

ROOT STATUS SHALL BE ESTABLISHED BY EITHER an explicit `sequenced_after: []`
covered by the change's ratification, OR a MECHANICAL CO-MODIFIER CROSS-CHECK
finding no other change in the corpus that declares a delta on the same
requirements — and where NEITHER holds, a consumer SHALL REFUSE under a named
identifier rather than read the change as a root. THE CROSS-CHECK ITSELF IS THE
CONSUMER'S TO IMPLEMENT AND ENFORCE, and this substrate deliberately does not
define it: its key is a PER-REPOSITORY CORPUS FACT — the promoted
`openspec/specs/<capability-id>/spec.md` a delta's requirement titles resolve
against — and a neutral field cannot carry it. A consumer SHALL keep the
cross-check IN FORCE AFTER adopting the field, so that `sequenced_after: []`
plus a detected co-modifier still refuses; declaring root status must never buy
authority that omitting the field would not.

#### Scenario: A consumer meets a change with no declaration
- **WHEN** a consumer walks a chain and reaches a change carrying no `sequenced_after:` field
- **THEN** it MUST NOT treat the change as a root
- **AND** it MUST either prove root status by its own co-modifier cross-check or refuse under a named identifier

#### Scenario: A root claim is contradicted by a co-modifier
- **WHEN** a change declares `sequenced_after: []` and a consumer's cross-check finds another change declaring a delta on a requirement it also modifies
- **THEN** the consumer MUST refuse, because an honest declaration must not be worth less than an omission

#### Scenario: A root claim is corroborated
- **WHEN** a change declares `sequenced_after: []` and a consumer's cross-check finds no co-modifier
- **THEN** root status is proved and the walk terminates there

### Requirement: Trust-root integrity of the parent declaration
The `sequenced_after:` declaration SHALL hold the same four trust-root properties
this capability already obligates for the structured scope declaration, because a
chain walk is only as trustworthy as the links it follows. It SHALL be BASE-READ
— a consumer reads it only from the base branch of an enrolled repository, never
from a pull-request head, so a pull request can never present the check that
authorizes it with a chain of its own choosing. It SHALL be
RATIFICATION-COVERED — the declaration's bytes live in `proposal.md` front
matter, are part of the ratified change artifact, and are covered by that change's
ratification, so a chain cannot be re-shaped post-ratification. It SHALL be
NON-AUTHOR-MUTABLE — the `openspec/changes/` surface that carries the declaration
SHALL be a never-clearable floor member of every repository enrolled for an
autonomous-merge axis that consumes it, and no autonomous merge SHALL write to
it, which closes the self-authorization recursion in which an earlier autonomous
merge could author the chain a later decision corroborates against. And it SHALL
be FROZEN AFTER RATIFICATION, per the "Parent-declaration retention at archive"
requirement.

These properties SHALL hold as a CONDITION of any repository enabling a gate that
reads the field, and a repository that cannot floor the declaration-carrying
surface within its own tree-validated floor SHALL NOT enable such a gate for any
non-docs class.

#### Scenario: A pull request re-shapes its own chain on its head
- **WHEN** a realization pull request edits `sequenced_after:` on its head to name a different or shorter chain
- **THEN** the consumer is unaffected, because it reads the declaration only from the base branch

#### Scenario: An autonomous merge would write a parent declaration
- **WHEN** a candidate pull request eligible for autonomous clearance would itself write or modify a `sequenced_after:` declaration
- **THEN** it MUST park for human review, because no autonomous merge writes a trust-root source

#### Scenario: The declaration surface is not floored in an enrolling repository
- **WHEN** a repository would enable a chain-consuming gate for a non-docs class without making the `openspec/changes/` declaration surface a never-clearable floor member
- **THEN** the class MUST NOT be enabled

### Requirement: Parent-declaration retention at archive
The archive gate SHALL verify that a change's `sequenced_after:` declaration is
unchanged from the declaration present at ratification, and mutation after
ratification SHALL be rejected at the archive gate. This mirrors the "Origin
retention at archive" and "Scope retention at archive" requirements and realizes
the FROZEN-AFTER-RATIFICATION property above: a ratified chain position is
auditable and immutable, so a change cannot silently re-parent itself — or
promote itself to a root — between ratification and archive, which under any
narrowing composition would be a widening. Accepting a mutated declaration SHALL
be a contested-class act requiring an explicit, recorded disposition.

#### Scenario: The declaration is unchanged at archive
- **WHEN** a change carrying `sequenced_after:` reaches its archive gate and the declaration matches the one present at ratification
- **THEN** the retention check passes and archiving proceeds

#### Scenario: The declaration was mutated after ratification
- **WHEN** the archive gate finds `sequenced_after:` differs from the declaration present at ratification
- **THEN** the archive MUST fail
- **AND** accepting the mutation requires an explicit recorded disposition

### Requirement: Chain-walk policy belongs to the consumer, and its bound SHALL be measured
This substrate SHALL declare NO depth ceiling, NO fan-out cap, and NO scope- or
authority-composition operator over a chain, and a consuming gate SHALL declare
its own and SHALL record them as OPERATIVE NUMBERS rather than leave them
implicit. The boundary is drawn here deliberately: depth, fan-out and composition
are AUTHORIZATION POLICY of the gate that acts on a chain, they differ between
gates, and a number fixed in the neutral field would bind repositories that never
adopt any such gate while drifting from the one gate that enforces it. What the
substrate owes instead is that the chain be WELL-FORMED and WALKABLE — resolvable,
acyclic, unambiguous, and frozen — which the preceding requirements provide.

A GATE'S DEPTH BOUND SHALL BE MEASURED AGAINST HONEST CHAINS RATHER THAN MERELY
ASSERTED, and the measurement SHALL be recorded. As at 2026-09-01 the field does
not exist in any corpus, so the deepest resolvable declared chain anywhere is
ZERO HOPS BY CONSTRUCTION and no gate's ceiling has ever bound a real chain: that
is a measurement of ZERO EVIDENCE, not evidence that any ceiling is sufficient,
and a specification SHALL say so rather than let its number read as validated.
The FIRST corpus sweep after adoption SHALL record the deepest chain it resolves,
and a raise of any gate's ceiling SHALL be a specification change with a recorded
disposition — never an operational adjustment made when a candidate refuses.

#### Scenario: A consuming gate declares its walk policy
- **WHEN** a gate consumes `sequenced_after:` to authorize anything
- **THEN** it MUST declare its own depth ceiling, its fan-out disposition, and its composition operator as operative numbers in its own specification

#### Scenario: A gate's ceiling has never bound a real chain
- **WHEN** a gate cites a depth ceiling and no honest chain has ever reached it
- **THEN** the specification MUST record that as an unmeasured bound rather than as a validated one, and MUST record the deepest chain actually resolved once a corpus sweep can measure it

#### Scenario: A candidate refuses on the depth ceiling
- **WHEN** an honest chain exceeds a gate's declared ceiling
- **THEN** raising the ceiling MUST be a specification change with a recorded disposition, and MUST NOT be an operational adjustment made at the point of refusal
