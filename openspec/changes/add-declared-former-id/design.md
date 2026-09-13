# Design: add-declared-former-id

Status: draft

**WHAT THIS DOCUMENT IS FOR.** Five decisions in this packet could reasonably
have gone the other way, and each is put below as a question with the
recommendation FIRST and the cost of the alternatives written out beside it, so
a veto costs one section rather than a re-author. Everything else is measurement.

Every figure here was taken in this packet's authoring session on a clone of
`main` at `9378eca5`, and the command that produced it is named where it is
stated.

## D0 — The measurements, taken before the design

**M1 — the two silences git answers with the same value.** A fixture repository
carrying the #1003 chain (`ratify r -> rename+un-ratify r->s -> rename s->t
while draft -> ratify t`) was cloned with `git clone --filter=blob:none
--no-checkout` and its promisor remote made unreachable, on git 2.43.0. At a
commit where a path is PRESENT in the tree but its blob is not locally
available, against the same path GENUINELY ABSENT at that commit:

| read | present, blob unavailable | genuinely absent |
| --- | --- | --- |
| `git ls-tree --name-only <rev> -- <path>` | **the row, exit 0** | **nothing, exit 0** |
| `git cat-file -e <rev>:<path>` | exit 128 | exit 128 |
| `git show <rev>:<path>` | exit 128 | exit 128 |

`ls-tree` separates the two. `cat-file -e` and `show` do not — and those are the
two reads this estate's packet-at-a-ref lookups are built on
(`proposal-support.git_show_text`, `sequenced_after._blob_exists_at_ref`). PR
#1024 measured the same distinction and recorded it at its
[FREEZE](https://github.com/opensoft/openxFactory/pull/1024#issuecomment-5651182318);
this is the re-measurement, so the figure this design rests on is one taken
here.

**M2 — the substrate loses exactly the hop that matters.** On the same pair of
checkouts, at the hop that renames `change-r` to `change-s` AND un-ratifies it
in one commit:

* full clone — `git log --follow --find-renames --name-status --format=%H -1
  <hop> -- openspec/changes/change-s/proposal.md` reports
  `R075 openspec/changes/change-r/proposal.md openspec/changes/change-s/proposal.md`;
* the partial clone — the same command reports **no record at all**.

Rename pairing below an exact match is computed from content, so a checkout that
cannot read content reports no rename. The lost hop is the dangerous one by
construction: an un-ratifying rename is a rename that also EDITS, which is
exactly what puts it below the exact-match threshold. On that same checkout
`git ls-tree` still names the predecessor. **A declaration is read from the
tree.**

**M3 — a sibling key does not enter the frozen origin comparison.**
`proposal-support.origin_block_lines` was loaded from the shipped script and run
over a real `.openspec.yaml` body with and without a top-level `former_ids:`
list appended: it returns the IDENTICAL seven-line block both times, because it
starts collecting at the `origin:` line and stops at the first line that is
neither blank nor indented. So a top-level sibling of `origin:` is outside the
declaration the archive gate freezes at ratification. Nothing in the repository
refuses an unknown top-level key in `.openspec.yaml`: `load_packet` parses the
file and returns the mapping, and no validator enumerates its keys.

**M4 — the dangling-citation population.** Over every tracked file except
`openspec/changes/archive/` (frozen record), `tests/` and `specs/` (fixtures and
Spec Kit feats), every `openspec/changes/<id>/<file>` token was extracted and
resolved against the working tree: **94** distinct references resolve to
nothing, of which **58** resolve BY ID against
`openspec/changes/archive/<YYYY-MM-DD>-<id>/<file>`. The remaining 36 are not
classified here and are deliberately not claimed as defects — they include
cross-repository citations spelled `codexFactory openspec/changes/…`, which do
not resolve on this tree BY DESIGN, along with example and fixture ids. The
reference #833 named is among the 58:
`openspec/changes/bump-openspec-cli-pin-to-1.12/specs/neutral-product-pin/spec.md`,
cited at `openspec/changes/disposition-codexfactory-declared-renames/design.md`,
now standing at
`openspec/changes/archive/2026-09-09-bump-openspec-cli-pin-to-1.12/specs/neutral-product-pin/spec.md`.

**M5 — ONE thing checks a citation's destination, and it checks the RAW PATH.**
This measurement was taken twice: the first reading said nothing checks, and the
bench's third round found the consumer it missed. Corrected here rather than
quietly, because the corrected fact is stronger than the original claim.

`scripts/validate-openspec-cli-pin.py` requires `cited_to:` to be non-empty,
refuses `pin-disposition-malformed` when it is not, and PRINTS the members in
its disposition report — it never opens one. But
`scripts/validate-pin-registrations.py`'s `check_citations` DOES, and it was
landed for exactly this defect (issue #840, after PR #834 renamed a change
directory and left two live citations naming the old id while every run still
exited 0). Its own docstring states the rule: "a path that is absent — or
absolute, or `..`-escaping — is a named finding and exit 1".

Run on this tree, it reports: *"6 disposition(s) carry 40 citation(s) naming 36
referent(s) — 17 name a path in this tree, 0 a URL, 7 a forge reference, 12 a
path qualified to another repository; 4 citation(s) name no machine referent
[…]; every in-tree path resolves"*. **SIX of those in-tree referents point INTO
AN ACTIVE PACKET**, across four packets — `prepare-openspec-1-12-readiness`
(twice), `add-chain-attestation`,
`disposition-codexfactory-floor-relocation-retitle` and
`disposition-codexfactory-regular-pr-council-clearance-archive` (twice). Each of
those four will archive, each archive moves the path and keeps the id, and this
gate resolves the RAW PATH — so the next of those archives turns a lawful act
into an exit-1 refusal of a gate nobody touched. That is the dangling-cited-path
defect with a date on it rather than a hypothesis, and the resolution rule below
is what makes the archive survivable.

The `doc-health` half of the original claim stands: no family reads where a
citation points, which is why the reference at M4 appears nowhere in the control
run of `scripts/doc-health.py --single-repo .` — that run reports the archived
packet only for an unrelated ratification-record finding.

**M6 — the delta is unsequenced.** `## MODIFIED Requirements` blocks over
`release-realization` titles across all active changes:
`add-structured-scope-substrate` and `add-target-release-deferred-allocation`
both hold *Realization axis declaration*, and the second also holds *Realization
axis vocabulary is gated*. **No active change holds a block over *Origin
retention at archive***; the only other occurrence of that title under
`openspec/changes/*/specs/` is one line of prose in
`add-structured-scope-substrate`'s delta, mirroring the requirement for its own
scope declaration. So this packet's MODIFIED block is declared against CANON and
`sequenced_after: []` is correct rather than merely empty.

## D1 — RECOMMENDED: the declaration lives in the packet's own `.openspec.yaml`, as a SIBLING of `origin:`

**Option (a), recommended — a top-level `former_ids:` key in
`openspec/changes/<id>/.openspec.yaml`.** Three properties decide it.

* **It is the file the gate already reads at both ends.** The archive gate reads
  `.openspec.yaml` from the working tree and from the ratifying commit. A
  declaration anywhere else would add a second file to the same read, at a path
  that would itself have to be resolved across the move.
* **It is the packet's identity record.** `origin:` already answers "where did
  this packet come from" in the ideation sense. `former_ids:` answers it in the
  identity sense, and they belong beside each other.
* **A SIBLING, never a member — and this is a requirement, not a preference.**
  The origin declaration is frozen at ratification and any post-ratification edit
  to it is a mutation needing an explicit disposition. A former-id entry is
  written by the very act that MOVES the packet, and that act happens after
  ratification BY CONSTRUCTION: a draft that moves owes no declaration, because
  the gate never refuses a draft's rename. Putting the list inside `origin:`
  would therefore make every lawful move a mutation of a frozen declaration and
  would need a disposition for each one — a mechanism whose ordinary use
  requires an exception. M3 measures that a top-level sibling is outside the
  frozen block.

**Option (b) — a field inside `origin:`.** Costs the disposition-per-move above.
Rejected on M3.

**Option (c) — a separate estate-level register, one file mapping former ids to
current ids, in the shape of `contracts/policies/repository-identity.yaml`.**
That file is the closest precedent in this estate and its reasoning transfers in
part: *"a frozen former identity is resolved BY LOOKUP HERE, never through a
provider redirect"* is the same argument this packet makes against rename
detection. It is rejected for a different reason: a repository transfer is an
ESTATE-WIDE event whose record must be readable by every consuming repository,
while a packet move is LOCAL to one repository's corpus and its record must
travel with the packet — through the archive relocation, and into the archived
directory where the origin-retention gate reads it. A central register would
have to be read at a ref, would become a second thing to keep in step with the
corpus, and would put one file in the path of every lane's merges.

## D2 — RECOMMENDED: the declaration names change IDS, and the path is derived

**Option (a), recommended — `former_ids:` is a list of CHANGE IDS.** Decided
from how this estate addresses a packet today, read rather than assumed:

* `proposal-support.ratifying_commit(root, change)` takes an ID and DERIVES the
  path: `rel = f"openspec/changes/{change}/proposal.md"`.
* `sequenced_after.proposal_path_at_ref(repo_root, ref, change_id)` takes an ID
  and resolves it to whichever path it occupied AT THAT REF — the active
  location first, then any `openspec/changes/archive/<YYYY-MM-DD>-<id>/` — and
  RAISES, naming the id, the ref and both paths tried, when neither exists.
* `doc_health.corpus.change_ids` unions active and archived ids, and
  `families._resolve_change` resolves a reference against that union.

The id is the address; the path is derived from it. So an id is declared ONCE per
identity change and both of the paths that id can occupy follow mechanically.

**Option (b) — declare former PATHS.** Rejected: a path declaration would have
to restate the archive-directory convention in every packet that ever moved, and
would have to be RE-declared when the packet archives — which is not an identity
change at all, so the declaration would record a non-event and the list would
stop meaning "the identities this packet has had".

**Ordering, and what it does not decide.** The list is ordered OLDEST FIRST and
appended to, never rewritten. The gate's ANSWER does not depend on the order:
the baseline is the EARLIEST commit at which the current id or any declared
former id declares `Status: ratified`, so a mis-ordered list cannot produce a
later baseline — it can only be a worse record, which a reader sees. Earliest is
the property that matters because the defect is a baseline that is too LATE.

## D3 — RECOMMENDED: the fail-closed refusal is taken by a house validator at the landing, not by the archive gate

**Where the refusal belongs.** The archive gate runs at ARCHIVE. A rename that
sheds a ratification does its damage at the RENAME, and the packet may not
archive for weeks. The ruling states the timing and the reason together: the
refusal is taken *"at that hop's landing (each hop is one commit when it lands,
so no chain-walking is ever needed)"*.

**Option (a), recommended — a new house validator run as a required check**, in
the shape `gate-realization-axis-vocabulary` established and this repository
already runs: a reader module under `scripts/`, a validator CLI beside it, and a
test suite exercising it over the live corpus. It reads the pull request's own
commit range and, for each commit, asks whether a change packet directory
arrived by a move from another change packet directory.

**What it refuses and what it prints.** Status `former-id-undeclared`, exit 1,
naming the commit, the source path, the destination path, and the one repair —
declare the source id in the destination packet's `former_ids:` IN THE SAME
COMMIT. A second status, `former-id-arrival-unreadable`, exit 2, CANNOT RUN,
names the read that could not be performed. **No bypass flag**, for the reason
#690 established for the sibling gate: a flag would be the declaration nobody
writes.

**The two arms, and why there are two.** The PRIMARY arm is git's own rename
pairing at that commit, which is what names a source for a destination. The
FAIL-CLOSED arm is the tree: `git ls-tree` alone answers whether a packet
directory exists at a commit and at its parent, needs no blob, and is available
on exactly the checkouts where the pairing is not (M1, M2). So where the pairing
read cannot be performed AND the tree shows both a packet directory arriving and
a packet directory leaving in that commit, the validator refuses CANNOT RUN. It
does not PAIR them from the tree — a commit that withdraws one packet and
creates an unrelated other has the same tree shape — it refuses to answer, which
is the honest reading of a checkout that cannot read its own history.

**The one exception, recognized by id.** `openspec/changes/<id>/` relocating to
`openspec/changes/archive/<YYYY-MM-DD>-<id>/` with the id unchanged is the
archive wrapper's own act. It is recognized from the ids alone, needs no
declaration, and is the only exception.

**Option (b) — put the refusal in the archive gate.** Rejected: it would leave
the corpus carrying a laundered rename until the packet archived, and the author
who could repair it cheaply — the one who made the move — would be long gone.

**Option (c) — a `doc-health` finding.** Rejected: `doc-health` reports and does
not refuse, and the ruling's word is "refused".

## D4 — RECOMMENDED: no `doc-health` delta in this packet, and the reasoning is the cost

**The question.** #833's dangling-cited-path finding is swept in by the ruling.
Does reporting the unresolvable remainder need a requirement in
`openspec/specs/doc-health/spec.md`?

**Option (a), recommended — no `doc-health` delta.** Three reasons, in order of
weight.

1. **What the mechanism repairs is a RESOLUTION RULE, and that rule belongs with
   the identity it resolves.** The third ADDED requirement states it in
   `release-realization`, where `former_ids:` is defined: a reference resolves by
   id, against the location the id occupies now and against any packet declaring
   it as a former id, and is dangling only when it resolves to nothing under that
   rule. M4 measures what that rule alone repairs: **58 of the 94** dangling
   references, every one of them broken by the ARCHIVE RELOCATION, which moves
   the path and preserves the id. The former-id half is what
   keeps the rule total once a packet's id itself changes, which no packet in
   this corpus has ever done, because the gate blocks it: that is the deadlock
   #833 named and this packet ends.
2. **Reporting the remainder is a second governed surface with its own numeral.**
   A `doc-health` check in this repository is a REGISTERED FAMILY named in a
   promoted enumeration that reads *"twenty-three check families"* and lists them
   (`openspec/specs/doc-health/spec.md` § *Deterministic check families*), gated
   by the family-enumeration family, which refuses a delta whose enumeration
   omits a registered family, names an unregistered one, or carries a numeral
   inconsistent with the registry in its own tree. A twenty-fourth is therefore a
   `## MODIFIED Requirements` block over that whole enumeration plus a registry
   edit plus a numeral — a change about doc-health's family set, not about packet
   identity. Folding it in here would widen a ruled remedy into an unruled one.
3. **The alternative home is worse and is measured.** The existing
   `proposal-origin` family enforces *"the promoted origin requirements of
   `document-lifecycle` and `release-realization` by reference"*, which would fit
   — except that its own promoted text fixes its classes: *"The family's finding
   classes are therefore SEVEN, named: …"*. An eighth class is a MODIFIED block
   over that requirement too, and the class would be about CITATIONS rather than
   about proposal origins, which is not what that family is.

**What is owed instead, and it is named rather than implied.** The reporting
sweep is a successor, and `tasks.md` § 6.1 records it with the figures this
packet measured so the successor does not have to re-derive them.

**Option (b) — add the twenty-fourth family here.** Costs the MODIFIED
enumeration, the registry edit, the numeral, and a second set of severity
decisions this packet has no ruling for. Rejected on cost, not on merit.

**Option (c) — put the reporting sweep in the `cited_to` gate.** Rejected for
scope, and the scope is now measured rather than guessed: that gate
(`validate-pin-registrations.py`'s `check_citations`, M5) already RESOLVES every
citation and refuses exit 1 on an absent path, so it needs no new reporting arm
— it needs the resolution rule, which it is named as the consumer of in
`tasks.md` § 5.1. What belongs to it and not here is everything else about that
field: its requirement lives in `neutral-product-pin`, a third capability, and
its dispositions are deliberately cross-repository — 12 of this tree's 36
referents are paths qualified to another repository and must not be refused
here, which is a rule that belongs to that validator's own design.

## D5 — RECOMMENDED: *Origin retention at archive* is MODIFIED, not left alone

**Option (a), recommended — MODIFY it.** The promoted requirement names the
baseline as *"the declaration present at ratification"*, and the whole defect is
that after a move the walk compares against a commit that is NOT the
ratification. Leaving the requirement untouched and adding a separate one would
put two rules over one gate, with the older one still saying the baseline is
found where it cannot be found. The block carries every promoted sentence and
all three promoted scenarios VERBATIM and only adds — verified by comparing the
restated text against `openspec/specs/release-realization/spec.md` lines 262–282
— so the modified-block-currency family's carriage arm has nothing to report and
this packet opens no ledger row. M6 measures that no active change holds this
title, so no `sequenced_after:` is owed.

**Option (b) — three ADDED requirements only.** Cheaper (an ADDED block costs no
carriage argument), and it is the shape `gate-code-surface-declarations` took for
a neighbouring sentence. Rejected here because that packet was ADDING a
constraint the promoted sentence did not speak to, while this one CHANGES where
the promoted sentence's own baseline is found.

## D6 — The relation to `disposition-codexfactory-declared-renames`, read and not assumed

That packet is ACTIVE and ratified. Its subject is `contracts/openspec-cli-pin.yaml`'s
`dispositions:` block — two entries scoped `repo: codexFactory`, each accepting
one ERROR-level finding of the pinned CLI's scenario-currency check — and its
own `design.md` § 4 records that it writes no spec delta because the rule it
exercises is already stated.

**"Declared renames" there means a RENAMED REQUIREMENT TITLE inside a spec
delta**, declared with the reserved `Merged into` marker, and the disposition
accepts the finding that marker-blind tooling raises. **"Declared former id"
here means a PACKET DIRECTORY's identity.** Both are declarations that an
identity continued across a rename, and neither is the other; this design says
so rather than leaving a later reader to collapse them.

**Nothing here edits that packet.** It carries the live dangling citation M4
found, and the repair is the resolution rule applied by the READER — its ratified
prose stays exactly as it stands, and no rewrite by the citing packet is owed.
Nothing in this packet's deltas contradicts its dispositions, its scoping, or
its refusal codes.

## D7 — The realization slices, in order

Each slice lands with its own tests and is independently green. The order is a
dependency order, not a preference.

1. **The declaration and its reader.** `former_ids:` grammar, the top-level
   sibling position, the shape refusals (not a list, an entry that is not a
   change id, an entry equal to the packet's own id, a duplicate entry, an entry
   naming a live directory).
2. **The archive gate.** `ratifying_commit` takes the declared identities and
   resolves the baseline across them, EARLIEST-wins, each identity's path
   resolved at each commit by the rule `proposal_path_at_ref` already
   implements. The refusal PR #846 wrote stays exactly where it is for the
   UNDECLARED case.
3. **The fail-closed reads.** Presence read from the tree, content read
   separately, a read that could not be performed raised as CANNOT RUN naming
   the read and the identity. PR #1024's branch (`2bc60386`, retained) carries a
   worked version of this half; it is a candidate to lift rather than a
   dependency.
4. **The landing validator.** The reader, the CLI, the two statuses, the archive
   exception, the two arms, and its registration as a required check.
5. **The reference resolver.** The by-identity resolution rule and its reader,
   with the cross-repository case explicitly out of scope on the tree being read.
6. **The documents.** `docs/document-lifecycle.md`'s origin-at-the-proposal-gate
   paragraph, whose sentence *"Renaming a ratified change is therefore blocked
   until a change declares a FORMER ID (issue #833, a successor packet)"* is the
   sentence this packet answers, and which must then say what a declared move
   requires instead of saying the act is blocked.

## D8 — What is measured and deliberately NOT taken here

* **The interim docstring-and-fixture pin** (part 2 of the ruling) is a separate
  plain-fix pull request on `fix/1003-interim-pin-multi-hop-gap`. It pins
  today's answer for the multi-hop gap while this mechanism is authored; keeping
  it out of this packet keeps a plain fix a plain fix.
* **Un-ratification in its OWN commit before the rename** — PR #1024's stated
  gap, where every hop moves a DRAFT so no hop answers the ratified question.
  This mechanism reaches it from the other side: the arrival refusal asks about
  the MOVE and not about the ratification, so an undeclared move of a
  once-ratified packet is refused whatever its blob says at that moment. Whether
  a re-ratification after a return to draft is lawfully a NEW baseline remains a
  governance question, and it is not answered here.
* **Shallow checkouts.** At a grafted boundary commit git reports no parents and
  therefore no pairing. The fail-closed arm's condition (a pairing read that
  could not be performed, plus a tree showing both an arrival and a departure)
  reaches the cases where it matters; refusing every shallow checkout outright
  is a new refusal class and belongs to a change that says so.
* **Other estate repositories.** Every rule here is scoped to the corpus of the
  repository being read. No other governed repository's corpus, register or CI is
  read, written or referenced by this packet.

## D9 — The bench's first round: nine threads, ALL NINE TAKEN

Posted on head `75ff1043` — three P1 findings from Codex and six from Copilot.
Every one of them is a real defect of the text as filed, every one is taken, and
four of them found the same class of hole from two directions. Recorded here
rather than only in replies, because four of the nine changed what the
requirements SAY and not merely how they read.

**(1) THE REFUSAL REACHED A LAWFUL DRAFT RENAME — a contradiction inside this
packet.** *An undeclared rename arrival is refused at its landing* was written
unconditionally over every packet-directory move, while *A moved packet declares
the identity it was ratified under* carries the scenario *A draft is renamed*
saying no declaration is owed, and the promoted realization record says
*"renaming a DRAFT change […] unaffected"*. A realization could not satisfy both.
**Taken:** the refusal is now qualified to a move whose SOURCE IDENTITY HAS EVER
DECLARED `Status: ratified`. The qualification is EVER, over that identity's
whole history up to the commit, and explicitly NOT its blob at the parent — a
packet renamed and un-ratified in one commit is back in draft at every later
hop, so a parent-blob test would exempt exactly the shape this refusal exists to
catch. Two scenarios added on either side of the line, plus an `AND` on the
chain scenario naming why its first hop qualifies. `tasks.md` § 4.2 carries the
same qualification, which it did not.

**(2) A STANDING PACKET COULD HAVE APPENDED AN IDENTITY IT NEVER HAD.** The only
test on a declared entry was that the id is not a LIVE directory — and an
archived id has no live directory either, nor does one that never existed. So an
ordinary edit could append an unrelated identity, inherit its ratification as
the baseline, and capture every reference written under it; no arrival check
would fire, because no arrival happened. **Taken:** an entry is added ONLY by the
commit that performs the move it records, and a commit that adds a former id
while moving nothing into this packet is refused. Scenario added, `tasks.md`
§ 2.4 added with both fixtures.

**(3) APPEND-ONLY WAS STATED AND UNENFORCEABLE.** The requirement said the list
is *"appended to rather than rewritten"* and a scenario repeated it, but the
arrival check only ever runs at a move, so a commit the day AFTER a lawful move
could delete the declaration and no gate would look. The archive resolver would
then fall back to the later ratification under the current id — precisely the
baseline this mechanism exists to keep it away from. **Taken:** append-only is
now normative ACROSS COMMITS and not only within one, refused whether or not the
commit moves anything, with a scenario and `tasks.md` § 2.5 naming the
day-after-deletion fixture.

**(4) ONE IDENTITY COULD RESOLVE TO A SET.** *A packet reference resolves by
identity, not by path* said "against any packet that declares that id", which
admits two claimants; the baseline resolution had the same hole from the other
end, and `proposal_path_at_ref` takes the FIRST SORTED archived directory when
an id matches more than one. Against this estate's own stated rule:
`sequenced_after.archived_change_dirs` returns a LIST rather than a path because
*"two archive dates for one id is an AMBIGUITY the resolver must be able to
report, not a collision to resolve by taking the newest"*. **Taken:** a former
identity has EXACTLY ONE OWNER (refusal naming every claimant); an identity that
resolves to more than one location at a commit refuses CANNOT RUN rather than
choosing; and an AMBIGUOUS reference is a third outcome beside resolved and
dangling, belonging to the declaration that made one identity resolve twice
rather than to the citing record. Three scenarios added across three
requirements, plus `tasks.md` § 2.6, § 3.1a and § 5.2a.

**(5) `proposal_path_at_ref`'S PROBES CONTRADICT THIS PACKET'S OWN FAIL-CLOSED
CLAUSE, and D0's M1 already measured why.** `tasks.md` § 3.1 said the baseline
resolver reuses that helper; its `_blob_exists_at_ref` asks `git cat-file -e`,
which M1 measures exiting 128 for a missing blob AND for an unreadable one, and
`_archive_dir_names_at_ref` returns an empty list on any read failure. Reusing
them would make an unreadable former identity read as absent and let the walk
take a later baseline — what § 3.4 refuses. **Taken:** the packet now names the
RULE (active location, then a dated archive directory carrying the same id) and
forbids reusing the boolean probes, in `tasks.md` § 3.1 and as a sentence of the
MODIFIED requirement itself: *"An EXISTING probe that collapses the two SHALL
NOT be reused for this read merely because it already resolves a packet by id."*

**Nothing was refused, and nothing was taken on the reviewer's word alone.** The
two factual claims each finding rested on were re-read in this session before
the edit: `sequenced_after.py`'s `archived_change_dirs` docstring and
`_blob_exists_at_ref`/`_archive_dir_names_at_ref` bodies, and
`docs/document-lifecycle.md`'s draft-rename sentence. The delta grew from
**twenty scenarios to twenty-seven** (7 + 8 + 7 + 5) and `tasks.md` from 29
boxes to 34, all unticked.

## D10 — The bench's second round: three threads, ALL THREE TAKEN

Posted on head `94a0e6cd`, the commit that took round one. Two of the three are
defects the round-one fixes CREATED or left half-closed, which is the reason a
second round is bench and not ceremony.

**(1) THE QUALIFICATION ROUND ONE ADDED COULD BE SHED BY MOVING TWICE.**
Round one narrowed the landing refusal to a source identity that has EVER
declared `Status: ratified`. Read over the source's OWN id alone, that admits a
three-id chain: X ratified; X moves to Y with the move DECLARED and the header
returned to draft; Y then moves to Z undeclared. Y's own id never declared
`ratified` — it was created already in draft — so the second landing would pass
and Z would stand with no lineage at all, which contradicts this packet's own
`tasks.md` § 4.2 and D8. **Taken:** the source identity is now the source
packet's WHOLE DECLARED LINEAGE — its own id together with every id it declares
in `former_ids:` at that commit's parent — and the packet says in the same
breath why this is not the history walk the ruling refuses: the source's
declaration is ONE blob at ONE commit, and each id it names is asked directly,
exactly as the baseline resolution asks them. The same finding's other half is
now normative too: the arriving packet's list SHALL be the source's list WITH
THE SOURCE ID APPENDED, in the source's own order, so a move cannot shed a
lineage by omission. Three scenarios added, `tasks.md` § 4.2a and § 4.2b.

**(2) THE REFERENCE RULE RESOLVED THE PACKET AND NOT THE FILE.** *A packet
reference resolves by identity, not by path* identified the packet by the second
path segment and defined dangling only as a failure to resolve an IDENTITY — so
`openspec/changes/<live-id>/deleted-file` would have been non-dangling. **Taken:**
both halves must resolve, the location the identity resolves to must carry the
remainder the citation names, and a failure SAYS WHICH HALF FAILED — reported
against the FILE where the identity resolved. Scenario *The identity resolves
and the cited file does not*, `tasks.md` § 5.1a with two fixtures. This is a
finer grain than the defect the archive relocation causes, and the rule is
better for reaching it.

**(3) THE README ROW'S OWN COUNT WAS STALE BY ONE.** The row said the MODIFIED
block added three scenarios; round one's ambiguity scenario made it four, and
the row's own total said seven. Corrected to FOUR, and the delta total restated
as **thirty** (7 + 8 + 9 + 6) after this round. A packet index that disagrees
with the packet is exactly the class of defect this packet is about.

**Nothing refused; the delta is twenty-seven scenarios to thirty and `tasks.md`
34 boxes to 37, all unticked.**

## D11 — The bench's third round: three threads, ALL THREE TAKEN, and one of them corrects a MEASUREMENT

Posted on head `f887fd78`. One of the three found a consumer this packet's own
D0 had recorded as not existing, which makes it the most valuable finding of the
three rounds: the corrected fact is stronger than the claim it replaces.

**(1) THE FAIL-CLOSED ARM COVERED ONE READ AND THE REQUIREMENT NEEDS TWO.**
Round one's qualification ("the source lineage has EVER declared
`Status: ratified`") is answered by reading HISTORY at every identity in that
lineage — a second read, beside the arrival pairing. On a checkout that cannot
produce those blobs it returns the same silence as a lineage that was never
ratified, so an undeclared landing would pass on the one checkout where nothing
can be proved, with the fail-closed arm looking on. **Taken:** the ratification
lookup now carries its own sentence, refusing CANNOT RUN and naming the identity
and the read, with scenario *The ratification lookup cannot be performed* and
`tasks.md` § 4.2c pointing its fixture at M1's partial checkout.

**(2) D0 M5 WAS WRONG, AND THE TRUTH IS A DATED FAILURE RATHER THAN A
HYPOTHESIS.** M5 said no arm of any validator reads where a citation points. It
missed `scripts/validate-pin-registrations.py`'s `check_citations`, which was
landed for exactly this defect (issue #840, after PR #834 renamed a change
directory and left two live citations naming the old id while every run still
exited 0) and whose own docstring says "a path that is absent — or absolute, or
`..`-escaping — is a named finding and exit 1". Re-measured on this tree, it
reports *"6 disposition(s) carry 40 citation(s) naming 36 referent(s) — 17 name
a path in this tree […]; every in-tree path resolves"* — and **six of those
in-tree referents point into four ACTIVE packets**
(`prepare-openspec-1-12-readiness` twice, `add-chain-attestation`,
`disposition-codexfactory-floor-relocation-retitle`, and
`disposition-codexfactory-regular-pr-council-clearance-archive` twice). Each of
the four will archive; each archive moves the path and keeps the id; the gate
resolves the RAW path. **Taken:** M5 is rewritten with the measurement, D4's
option (c) is restated against the corrected fact, `tasks.md` § 5.0 names that
reader as the CONSUMER of the resolution rule with its own tests, and the
proposal carries the consequence. The thread's own framing — "an unconnected
reader" — was the right diagnosis: § 5.1 built a resolver and named nobody to
call it.

**(3) THE PULL REQUEST DESCRIPTION STILL CARRIED ROUND ZERO'S COUNT.** Twenty
scenarios (6 + 5 + 5 + 4) where the packet now defines thirty-one. **Taken:** the
description is rewritten from the packet rather than patched, and the README
row's count re-derived with it. Twice in three rounds a stale count has been the
finding, which is itself the argument for deriving these numbers at each push
instead of carrying them.

**Nothing refused; thirty scenarios to thirty-one and `tasks.md` 37 boxes to
39, all unticked.**
