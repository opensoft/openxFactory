# Design: govern-archived-record-edits

Status: draft
Lane: opsXfactory-1

Eight decisions — **D-1** through **D-8** — each with the alternative it
rejects and the measured reason. Brett Heap's F.3 ruling came in TWO comments on
OpsxFactory PR #248 and chose two things: the rule's SHAPE
(*"Header/bookkeeping edits only + re-derive pins"*, comment 5563099832,
2026-09-06T23:42Z) and its HOME (*"Both at once"*, comment 5571629298,
2026-09-07T13:51Z). It chose nothing below. Every decision here is the authoring
session's and is a veto point.

§ *Readings not taken* at the end records the three whole positions this
packet declines, so a reviewer can overturn the packet without first having to
reconstruct what it decided against.

## Context

`document-lifecycle` is the promoted capability that governs governance
documents across openxFactory and every DomainxFactory. It already carries the
two facts that make an archived byte load-bearing:

1. *Ratified spec deltas reach the promoted specification* makes "the MOST
   RECENT archived delta that touches it, and that one alone" the AUTHORITY for
   a promoted requirement. Canon is checked against archived bytes.
2. *Proposal packets carry the lifecycle header* ends its discharge clause
   with "Backfilling a header onto an archived packet is an archived-record
   edit and **takes the route archived-record edits take**" — a forward
   reference to a route the corpus does not contain.

Both sentences were written by `govern-openspec-corpus-membership`, whose
archive commit `01ff3434` is authored **2026-08-23T23:06:12-04:00 =
2026-08-24T03:06:12Z**. OpsxFactory's `57fd9fd2` is authored
**2026-08-24T04:08:48-04:00 = 2026-08-24T08:08:48Z**. **They fall on the same
day IN UTC and on different days in the authoring clock**, and the coincidence
is stated with its clock rather than left to be discovered — five hours apart,
same UTC date, one calendar day apart at `-04:00`. On that same UTC day,
`57fd9fd2` did the thing the second sentence gestures at — a 55-defect lifecycle-header discharge — under a local
convention that asked only for a bookkeeping note, wrote 16 files under that
repository's archive tree, and broke three executed consent instruments'
custody pins. The dangling reference and the breakage are one gap seen from two
sides.

## D-1. The home is `document-lifecycle`, not a new capability and not `release-realization`

**Decision.** Both new requirements land on the promoted `document-lifecycle`
capability, beside the two requirements named above.

**Why.** The coupling is not thematic, it is textual. This capability's own
requirement forward-references the route; this capability's own requirement
makes archived bytes the authority for canon; and this capability's own
taxonomy defines `record` as "CAPTURED ONCE", which is exactly the property an
archived packet has and the property an in-place edit destroys. A new
capability would hold a rule whose every premise lives somewhere else.

**Rejected:** `release-realization` — it governs the ARCHIVE GATE (when a
change may archive) rather than what an archived record is afterwards, and
extending it would make the rule sound like an archiving condition, which is
precisely the misreading that produced `FR-072`'s over-extension. A new
capability, e.g. `archived-record-integrity` — a two-requirement capability
whose motivation is entirely in another capability's text is a capability in
name only, and the estate has one already (`doc-health`) that would then have
three homes to consult.

## D-2. Two ADDED requirements, not one

**Decision.** The archive rule and the pinned-target rule are stated as SEPARATE
requirements.

**Why, and it is measured.** Their failures are invisible to each other, and one
of the three breakages proves it: the broken pin on
`add-managed-node-inventory`'s target sits in a change directory that has NEVER
been archived. A single requirement scoped to `openspec/changes/archive/`
would have reported itself satisfied while that pin stayed broken. And the
converse holds: an archived `design.md` that no pin names can be rewritten
substantively without any content address moving. Two failures, two
requirements — the same reasoning the capability already applies to *Ratified
spec deltas reach the promoted specification* and *A ruling is discharged once*,
which it states separately for the same stated reason.

**Rejected:** one requirement with two clause-groups (the archive scope would
read as governing both halves, which is the error above); three requirements
splitting the recording obligation from the re-derivation obligation (the
recording IS the obligation — see D-6 — so the third would be empty).

## D-3. Add a `## MODIFIED` block closing the dangling reference

**Decision.** *Proposal packets carry the lifecycle header* is restated in full
and TWO PASSAGES ARE INSERTED. The dangling "takes the route archived-record
edits take" sentence is left BYTE-IDENTICAL and a paragraph after it names the
route and says that where the backfilled file is also a pinned target the second
requirement attaches as well, the two obligations being independent. And one
scenario is added, *A header defect is discharged on an archived packet*, which
is the `57fd9fd2` act stated as a rule.

**Why.** A forward reference to a rule that now exists and does not name it is
a reference nobody can follow. And leaving it would leave the packet's own
motivating act — a header backfill on archived packets — governed only by
inference from a requirement it is not mentioned in.

**The restatement was verified, not asserted.** The block is extracted
programmatically from `openspec/specs/document-lifecycle/spec.md` and diffed
against it. **Canon's block is 5,815 characters and the delta block is 7,186;
the 1,371-character difference is entirely INSERTED** — the slice runs from the
requirement heading to the next one with trailing newlines stripped on both
sides, and the earlier draft of this sentence reported 7,186 as though it were
the size of the change rather than of the block. All six promoted scenarios are
carried and there are exactly two hunks of difference — BOTH PURE INSERTIONS. **The first draft of this block
REWORDED the dangling sentence in place, and doc-health's
`modified-block-currency` arm caught it**: that arm reads body units at SENTENCE
granularity, so a rewritten sentence is a body unit canon states and the block
does not carry, reported (info, contested) as a divergence the arm "CANNOT
distinguish from a deliberate rewording". The finding was real and the fix is
strictly better governance — canon's own words survive and the new statement
sits beside them. Nothing is deleted, so no
``**Removed from canon by …**`` marker is owed, which is the currency rule
*A MODIFIED requirement block restates the requirement as canon currently
states it* demands. That rule also demands CURRENCY CONTINUOUSLY: if canon
moves under this block while the change is active, task 4.2 brings it forward
before archive.

**Rejected:** an ADDED-only packet leaving the sentence dangling (cheaper, and
it leaves the corpus asserting a route by name that the corpus does not
define); rewording the sentence to delete the forward reference (that would
delete the very evidence that the rule was known to be missing).

## D-4. The bookkeeping class is defined BY EFFECT, not by a list of files

**Decision.** A bookkeeping correction is one that adds or repairs the packet's
own STANDING METADATA and nothing the packet ASSERTS. The test is whether the
edit changes what the archived record asserts.

**Why a list of filenames fails.** `proposal.md` carries BOTH classes: its
`Status:` header is standing metadata and its § *What Changes* is an assertion.
A rule keyed to paths — "`proposal.md` and `review/` may be edited" — licenses
a substantive rewrite inside a file the list called safe, and refuses a
correction to an index row in a file the list omitted. The estate has the same
argument on record in the `document-lifecycle` taxonomy itself, which decides
`record` versus `projection` by asking what re-running the generator would mean
rather than by naming directories.

**Rejected:** an allowlist of files; an allowlist of LINE PATTERNS (a
`Ratified:` line inserted by `57fd9fd2` matches such a pattern perfectly and
still broke three pins, so the pattern is not the risk); a size threshold (the
measured breach was one line per file).

## D-5. The ruling is recorded BEFORE the edit, and the note is not the ruling

**Decision.** A ruling naming ruler, date and the class of edit authorized is
recorded before the edit; the bookkeeping note the local convention requires is
carried IN ADDITION.

**Why both, and why in that order.** The note records WHAT changed. The ruling
records THAT IT MAY BE. OpsxFactory's convention required only the note, and
the note was written — the 16 files carry it — and the note is exactly why
nothing looked wrong for thirteen days: a conforming record of an unauthorized
act. A convention discharged by the note alone authorizes every edit its author
believed was bookkeeping, which is indistinguishable from authorizing every
edit.

**Rejected:** ruling-after-the-fact (an edit already landed is a fait accompli,
and every ruling on one is asked under pressure to bless it); a standing
class-level ruling that covers all future header backfills (the measured breach
IS a header backfill under a standing permission — that is the failure mode,
not a mitigation of it); note-only, which is the status quo and is § *Readings
not taken* item 3.

## D-6. The obligation is the RECORDING; the detection is the gates'

**Decision.** The pinned-target requirement obliges a change that edits a
pinned target to carry the re-derivation. It does NOT oblige an author to
DISCOVER an unnoticed pin unaided.

**Why the distinction is load-bearing rather than a hedge.** A rule that
required discovery would be discharged by diligence and breached by
inattention, which makes it unenforceable and unfalsifiable at once. What is
enforceable is that the visible act carries its record, and what makes the
INVISIBLE act visible is a running gate: OpsxFactory's citation gate (live on
its `main` since PR #248) and its proposed `add-content-address-integrity-gate`.
Brett's F.3 ruling and F.2 ruling are the two halves of exactly this split, and
this packet does not collapse them.

**The consequence is stated rather than hidden:** a repository with no such
gate owes this obligation exactly as much and has nothing but review to catch a
breach. That is a real exposure and it is named in the requirement text.

**Rejected:** building a checker in this packet (a rule and its checker landing
in one act is how the estate has repeatedly shipped a rule the checker's shape
quietly narrowed — this packet would then state only what its own checker could
see); making the rule conditional on a gate existing (a rule that switches off
where it is hardest to enforce).

## D-7. Re-derivation is PER FAMILY, and an undeclared family is REPORTED until it declares

**Decision.** The requirement names no re-derivation procedure. It obliges the
pin's FAMILY to declare one — in the declaring repository's content-address
register or in the neutral contract that owns the family — and obliges the
editing change to follow it. **Where no rule is declared, the edit is REPORTED,
naming the family, the target and the home that owes the rule, and is NOT
refused on that ground; it becomes a refusal for that family the day that family
declares.** This heading and this decision said "refused until one is" through
two drafts, contradicting the transition clause the rest of this section argues
for — the refusal reading is the RECORDED VETO below, never the decision.

**Why not one procedure.** A consent instrument's custody chain, an evidence
digest, a plan-acceptance desired-state reference and a contract-bundle digest
re-derive and record differently — `add-consent-custody-rederivation-record`'s
own C-6 chain rule runs to seven legs and is specific to custody. A neutral
requirement that specified one procedure would either be wrong for most
families or so general as to say nothing.

**Why refusal rather than a default.** "Re-derive by whatever means" is a
promise nobody can check and nobody can repeat, and an ad-hoc re-derivation
performed for the occasion cannot be re-run by the next reviewer. Refusing puts
the cost on declaring the rule once, which is where the estate wants it.

**BUT THE REFUSAL ARRIVES WITH THE DECLARATION, NOT WITH THIS REQUIREMENT, AND
THAT WAS A DEFECT FOUND BY REVIEW RATHER THAN A NUANCE DESIGNED IN.** The first
draft of this packet said the edit "MUST be refused until one is declared", full
stop. Measured, that reading freezes the estate on the day this change lands:
NO family anywhere has a declared rule — the consent family's is proposed only
(`contract_schema_version: 2`, no `custody_rederivations` property,
`contract-v3.4`, 46/46 boxes unticked) and the register home
`models/content-address-families.yaml` exists neither on OpsxFactory's `main`
nor on the branch that proposes it, where authoring it is task 2.1 — and this
change carries `code_surface: none`, so it archives ON LANDING with nothing to
sequence behind. Every pinned-target edit in the estate would be refused from
that moment, including the routine lifecycle-header discharge the neighbouring
requirement and *Proposal packets carry the lifecycle header* both require, and
including the F.1 and F.2 repairs themselves. So the requirement now REPORTS an
edit whose family has declared no rule — naming the family, the target, and the
home that owes the rule — and becomes a REFUSAL for that family the day it
declares.

**THE REFUSE-OUTRIGHT READING IS BRETT HEAP'S VETO POINT, and it is coherent.**
It says: no pin without a rule, starting now, and the cost is that the estate's
corrective work stops until the first family declares. Taking it is a one-clause
edit to this requirement plus the removal of one scenario. It is recorded here
so that choosing it is a decision rather than a rediscovery, and it is flagged
at task 1.2.

**A SECOND-ORDER FIND, RECORDED BECAUSE IT WAS NEARLY MISSED.** The domain
twin's review caught that this requirement's FIRST BODY LINE did not carry
SHALL — the keyword sat on line two, and the OpenSpec parser reads only line one
when checking. The identical defect was present HERE and was not separately
reported; it was found by running the same check over this delta rather than by
assuming the twin's finding was local. The keyword now leads and the definition
of a pinned target follows it, in both repositories. The lesson generalizes: a
finding raised against one half of a matched pair is a hypothesis about the
other half until measured.

**Why BOTH homes, and not only the register.** A family's rule may be declared
in the declaring repository's content-address register OR in the neutral
contract that owns the family. That is not a hedge: the consent family's rule is
a property of the INSTRUMENT SCHEMA and belongs in the contract wherever the
instrument is held — `add-consent-custody-rederivation-record` puts it there —
while a repository-local family has no contract to live in and needs the
register. Naming only the register would have made the estate's one nearly-ready
rule homeless.

**Rejected:** a neutral default procedure (recompute sha256 of the named path)
— C-6a of the sibling packet MEASURED that this fails: every OpsxFactory
custody locator carries an `opsx:opensoft/` scheme and three of four targets
resolve at NO ref under their literal path, so an inferred rewrite can
manufacture agreement with a file nobody pinned; and an unrecorded WARNING
where the rule is undeclared.

**That last rejection needs its line drawn, because this packet's own transition
clause could be mistaken for it.** A warning is an admission with a softer
voice: it names nothing in particular, is recorded nowhere durable, and expires
with the terminal buffer. **The REPORT this requirement makes is none of those.**
It NAMES the family, the pinned target, and the register or neutral contract
that owes the rule; it is a gate finding and lands in that gate's output; and it
CONVERTS to a refusal for that family the day the family declares. A warning
says "this might matter"; the report says "this family owes a rule, here is who
owes it, and the obligation binds the moment it arrives".

## D-8. Cross-boundary deferral is legitimate; within-repository deferral is not

**Decision.** "In the same change" is absolute inside one tree. Where the
dependent pin is held by a CONSUMING repository, the editing change records the
owed consumer act by name and the consumer's own change carries the
re-derivation.

**Why the asymmetry is principled and not a convenience.** Inside one tree the
bytes and the pin are in one commit and one review, so a deferral is a broken
pin with a promise attached. Across a boundary they cannot be — no commit can
move both — so the only honest form is a named owed act, which is the shape
`release-realization` and the estate's re-pin practice already use (this
packet's own sibling F.1 is exactly such a chain: openxFactory cuts, OpsxFactory
re-pins in lockstep with its worker-enrollment-broker).

**Rejected:** requiring a cross-repository atomic act (impossible); allowing
in-repository deferral to a successor change (that is the measured failure with
paperwork).

## Readings not taken

Three whole positions were available and are declined, each for a stated
reason. A reviewer who prefers one of them is overturning a decision, not
finding a gap.

**1. A STRICT READ-ONLY ARCHIVE — no edit of an archived byte, ever.** This is
the cleanest rule to state and the easiest to check, and it is what the two
OpsxFactory packets believed `FR-072` already said. **Declined**, for three
measured reasons. (a) It contradicts canon in force: *Proposal packets carry
the lifecycle header* states that the pre-existing population "SHALL be
discharged rather than grandfathered", that "a packet carrying no `Status:`
header is a current violation whenever it was authored", and — in the same
breath — that backfilling one onto an archived packet is an archived-record
edit with a route. A read-only archive makes that population permanently
unfixable, so the capability would demand a discharge it forbids. (b) The
corpus has already performed such edits legitimately: the C5 case named in
canon backfilled exactly one line onto `2026-06-26-enable-live-openxfactory` to
declare it never ratified — a correction that made the archive HONEST. (c)
Brett Heap's F.3 ruling selected *"Header/bookkeeping edits only + re-derive
pins"* over the stricter options put to him. Taking the strict read here would
overturn the ruling this packet exists to realize; it remains available to him
and would be a different change.

**2. KEEPING THE CURRENT CONVENTION — leave OpsxFactory's local rule as the
governance and state nothing estate-wide.** **Declined.** The convention has
been measured failing in the only way that matters: it was in force, it was
followed, its note was written, and three executed consent instruments broke
under it for thirteen days. It also reaches one repository, while the archive
tree, the archived-delta-as-authority rule and the content-address families
exist in every repository the capability governs. And leaving it would leave
canon's own forward reference pointing at nothing.

**3. ENFORCING VIA THE NOTE ALONE — keep the bookkeeping note as the whole
obligation and add nothing.** **Declined**, and this is the narrowest and most
tempting of the three, because the note is cheap, already conventional, and
already written. It fails on the measurement, not on principle: the note WAS
written for all 16 files of `57fd9fd2` and the breach still happened and still
went unnoticed. A note is a record of an act by the actor, in the actor's own
classification of it. It cannot distinguish an authorized edit from an
unauthorized one, because both actors write the same note. What the note lacks
is an authority OUTSIDE the edit (D-5) and a check outside the record (D-6),
and this packet supplies the first and points at the second.
