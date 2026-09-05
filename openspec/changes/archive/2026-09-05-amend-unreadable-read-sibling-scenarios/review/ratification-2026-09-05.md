# Proposal Ratification: amend-unreadable-read-sibling-scenarios

Status: record
Kind: report
Decision date: 2026-09-05
Ratifier: Brett Heap (openxFactory operator authority) — in session
Ratified: 2026-09-05 by Brett Heap (openxFactory operator authority) —
in-session, verbatim: *"ratify 688, land it when green"*, given after a
presentation that carried `design.md` **D2** as the packet's veto point — the
third bullet, and with it `code_surface: openxFactory` — with options A and B
written out beside option C's cost. **D2 was not vetoed.**
Ratified baseline: this change as committed in the ratification commit carrying
this record — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml` and
`specs/doc-health/spec.md` (**ONE MODIFIED requirement**, *"Release-tag
publication"*, restated in full with all 30 promoted scenario titles and #678's
own amendment note and marker carried byte-identical, **ONE canon unit replaced**
and that unit declared by a reserved `Removed from canon by` marker) — together
with the CODE this packet's `code_surface` declares
(`scripts/doc_health/release_tag_publication.py`: one `Skip` reason and the
comment above it) and its test
(`tests/doc-health/test_release_tag_publication.py`: one test added), plus
`README.md` and `tests/sequenced_after/corpus-ledger.yaml`, with
`openspec validate amend-unreadable-read-sibling-scenarios --strict` and
`--all --strict` green and the verification run captured beside this file at
`verification-2026-09-05.md`.

**This record is CAPTURED AT MERGE, not at first push, and it was RE-DERIVED
PRE-CAPTURE.** `record-immutability` forbids editing a `Status: record` document
AFTER capture; capture is the merge of the pull request that establishes it, and
nothing is merged yet. Every number in `verification-2026-09-05.md` was
re-derived on the tree this record sits in, after this branch's SECOND merge from
`main` (`origin/main` `9b1888bb`). A commit cannot write its own hash into its
own tree, so the ratification commit is named by its subject and its position on
the branch rather than by a hash.

## 1. What was ratified, and what it says

**ONE requirement is MODIFIED and none is added.** `doc-health`'s promoted
*Release-tag publication* is restated in full — every body unit and all 30
promoted scenario titles, INCLUDING `amend-published-tip-unreadable-scenario`'s
own amendment note and its `Removed from canon by` marker, which promoted into
canon with the requirement and are CARRIED rather than restated — and exactly one
scenario changes, *The changelog cannot be read at the published tip*:

- its `WHEN` bullet is **REPLACED**, from naming one cause as commonest to naming
  **both facts** the single empty answer stands for — the commit not being in the
  checkout's object store, or the commit being HELD with no readable
  `contracts/CHANGELOG.md` blob reachable at it;
- an `AND` is **ADDED** on the `WHEN` side requiring that the family have
  **established which of the two holds** before choosing its words — and saying
  how it is established here: *by INHERITANCE and completely*, the manifest read
  at that same commit having already answered;
- a second `AND` is **ADDED** requiring that where the commit IS held, the skip
  say THAT and state the presence — and say it as the read it has, not as a file
  absence the held commit does not establish.

The promoted `THEN` and the closing *"not fetched is not an answer, in either
direction"* clause are carried **byte-identical**. No file is added under
`openspec/specs/`, so **no codexFactory floor advance** is owed.

**THE REPLACED UNIT IS DECLARED.** The block carries
`**Removed from canon by amend-unreadable-read-sibling-scenarios (2026-09-05):**`
naming the old `WHEN` verbatim in a DOUBLE-backtick span — double because the
unit itself contains a single-backtick span, and CommonMark closes a run of N
backticks only on a run of exactly N — with the reason, and saying it is a
REPLACEMENT rather than a deletion.

## 2. Why the packet exists, in one sentence and one measurement

**The clause `amend-published-tip-unreadable-scenario` retired was written twice,
and only one copy was removed.** #678 replaced the manifest read's *"the
commonest cause being a checkout that has not fetched that commit"* after
openxFactory **#612** measured it the wrong way round — on the aggregation
nightly the commit WAS fetched, and nine of the ten governed repositories simply
carry no `contracts/manifest.yaml` at all. The sibling scenario carried the
identical clause word for word over `contracts/CHANGELOG.md`. #678 found it AFTER
the word that ratified it, refused to widen its own ratified scope, and recorded
the sibling as an **owed successor** in its `tasks.md` § 4.2. This packet is that
successor.

## 3. The decision ratified knowingly

### D2 — the third bullet is IN, and it makes this a code surface

#678's shape has three moving parts. The first two are satisfied by the family as
it stands; the third is not — the changelog read had ONE skip and it said only
that the file *"could not be read at the published tip"*, the shape a reader is
entitled to read as a fetch defect, which is #612's cost one document over.

- **Option A — two bullets, `code_surface: none`, archives on landing.**
  Rejected: it leaves canon permitting the exact answer #612 was filed against,
  and makes two sibling scenarios say different things about one class.
- **Option B — three bullets, code left owing.** Rejected: canon out-runs the
  machinery by one `MUST`, inverting #678 — which was explicitly *"canon catching
  up with the checker"* — in the same requirement in the same week.
- **Option C, TAKEN and RATIFIED:** three bullets, and the third made true here —
  ONE `Skip` reason and the comment above it, one test added.

**The cost was put with the decision and is restated here so ratification cannot
be read as unaware of it:** under `release-realization` a non-empty code surface
means this packet **no longer archives on landing**; it archives on
merged-plus-green realization evidence, which this pull request produces. That is
a slower path than #678's for a two-line edit.

**Ratified as designed. The reversal was NOT taken.**

### D3 — no second presence probe, and the reason is written into the scenario

`check_repo` runs `obtain_commit(tip)` before any read (PR #646, `2177b2a2`), and
both `manifest is None` arms return before the changelog is consulted; `blobs_at`
sends `<commit>:<path>` to `cat-file --batch`, which reports every spec of a
commit the clone does not hold as missing. **A manifest that read is proof the
commit is held**, so at this arm the unfetched fact is EXCLUDED rather than
rarer. A second `obtain_commit` would be a round trip justified by nothing, and
the scenario says so in as many words to stop a later reader adding one.

## 4. The adversarial review, folded item by item BEFORE this record

An adversarial review of the pushed head raised three findings. **All three are
folded, in the commit immediately below this one on the branch, so the ratified
baseline is the folded text and not the text reviewed.**

### P2 — the held-and-absent skip STILL SUPPRESSES the grading. RATIFIED AS AN OWED SUCCESSOR, NOT AS FIXED.

The amended `WHEN`-side `AND` establishes that the only fact reachable at that
arm is a HELD tip carrying no readable changelog. The carried `THEN` then says
the family must not treat the absence of a declaration *"it could not look for"*
as the absence of a declaration — which presumes the family COULD NOT LOOK. At
this arm it could. And the code still answers it as though it could not: the
`if changelog is None:` guard stands ABOVE the `in_scope` loop and RETURNS.

**Measured, not asserted.** A shim with the tag ABSENT and no changelog blob at a
held tip returns one `Skip`; the SAME shim with an EMPTY `contracts/CHANGELOG.md`
returns one `error` — *"contract-v2.0 is declared and has no published annotated
tag more than 5 first-parent landings after the commit that declared it"*. A file
that is provably not there suppresses a finding that an empty one does not.

**It is NOT a regression** — the identical shim answers identically at
`origin/main` `9b1888bb` — **and it is NOT fixed here.** Moving a return that
decides which findings an in-scope repository receives is a behaviour change with
its own scenarios, its own severity reading and its own measurement to write; a
packet whose whole claim is *"one skip's TEXT, for one reachable state"* cannot
carry it without becoming the thing #678's lesson warns against. **Folded as:** a
named carve-out in `proposal.md` § What this proposal does NOT claim, decision
`design.md` **D6** (with what the successor owes, so it is not re-derived), and
an UNTICKED `tasks.md` § 6 — the same shape #678 used to name this packet. **The
carried `THEN` text and the skip's control flow are untouched.**

### P3 — the "two facts" framing was not exhaustive, and the skip mis-stated the third. FIXED HERE.

`blobs_at` (`scripts/doc_health/corpus.py`) also answers per-path None when the
commit AND its trees are held but the BLOB OBJECT is absent from the store.
**Reproduced rather than reasoned about:** remove the loose object and
`git cat-file --batch` answers `<spec> missing` for a path `ls-tree` still lists,
with `cat-file -e` reporting the commit and the tree both HELD. The skip's first
wording — *"the commit IS present and carries no contracts/CHANGELOG.md"* — is a
claim about the TREE that the read cannot support.

**Folded as:** the skip now reads *"the commit is held in this store and no
readable contracts/CHANGELOG.md blob is reachable at it"*, which is true of BOTH
held states; the delta's amended `WHEN` folds the third state into its held arm
rather than claiming an exhaustiveness it lacks; the added `AND` says the skip
must state the presence *without asserting a file absence the held commit does
not establish*; and the over-claiming form is now pinned against NEGATIVELY in
the test, beside the existing negative pin on the manifest arm's words. **Only
the units this block ADDS were edited** — the marker still declares the one
dropped canon unit and every carried canon unit stays byte-identical, which the
`modified-block-currency` mutation probe re-confirms both ways.

### P3 — one false positive the sweep's own grep raised was missing from the list. FIXED HERE.

`openspec/specs/ideation-cross-reference/spec.md:386` — *"a commit an ancestor
walk from `main` reaches is conforming even in a clone that has not fetched
it"* — is raised by angle 2 and was absent from `tasks.md` § 2. **Folded as**
`tasks.md` § 2.6, named with its reason: pin reachability, a different family,
where the phrase is used CORRECTLY to say that a local store's contents are not
the test.

### The "untested" item — the pull request body's numbers

The body's counts were taken at an older tree. They are refreshed against this
head and every one of them is re-derived in `verification-2026-09-05.md`.

## 5. Independent review, recorded including its absence

- **Codex: REFUSED, twice, and it is recorded rather than passed over.**
  `@codex review` was requested on this pull request at 17:55Z and the connector
  answered *"You have reached your Codex usage limits for code reviews"*; a
  second attempt at 18:20Z drew the same refusal. **No Codex round ran on this
  packet** — the continuation of the refusal run that also covered #668, #672
  and #678.
- **Sourcery:** the private-repo upsell stub, as on every packet in this arc.
- **Copilot: two rounds, and the second was right.**
  - **Round 1** (17:57Z, on the pre-merge head): **🟢 Approval recommended**,
    *"narrowly scoped to skip-message wording, internally consistent with the
    control-flow invariants, and backed by a targeted regression test."*
  - **Round 2** (18:24Z, on `3bb41b63`): **🟡 Changes recommended** — the new
    test asserted held-tip wording *without setting the `FakeGit` object-store
    precondition (`present_commits`) needed to model that state*. **It was
    right, and it is fixed in the fold commit:** `FakeGit`'s store is pessimistic
    by default, so the shim now sets `present_commits={"tip"}` and the test
    asserts `fetch_calls == []` — the held-tip words are pinned over a double
    that actually holds the tip, and holds it without a round trip. The point
    sharpens under the P3 narrowing, which makes the skip say MORE about the
    store rather than less.

## 6. The marker, and the probe that proves it is doing the work

`modified-block-currency` names this change **zero** times as it stands, which
alone cannot be distinguished from a block the family never read. So it was
probed **both ways on the folded tree**, and both fired:

- **marker removed** → *"does not carry **1** of the 222 body units and scenario
  bullets"*, naming exactly the retired changelog `WHEN` — one unit dropped, and
  the marker is what declares it;
- **a promoted scenario title mutated** → *"omits 1 of the **30** scenarios …
  'The published tag is lightweight rather than annotated'"*;
- **restored** → silent again.

## 7. Sequencing, and the ledger

`sequenced_after` is **ELECTIVE HERE AND IS NOT DECLARED.** All four other
writers of *Release-tag publication* — `add-release-tag-publication-check`,
`declare-spent-bundle-state`, `add-release-tag-gate` and
`amend-published-tip-unreadable-scenario` — are ARCHIVED, and no ACTIVE change
writes it. The ledger classes this row `co-modifier` on archived partners,
exactly as #678's was classed, so **no partner flips and no MOVEMENT LOG entry is
owed**. **Ratification moves no row**: a row's derived keys are `state`, `class`,
`declares`, `depth` and `prose`, none of which reads a lifecycle status, so a
`draft` → `ratified` transition is invisible to the ledger by construction —
confirmed by the `--ledger-diff` run in `verification-2026-09-05.md` § 5.

## 8. One repair carried in this pull request, and it is named

`README.md` carried an **ACTIVE row for `amend-published-tip-unreadable-scenario`
pointing at `openspec/changes/amend-published-tip-unreadable-scenario/proposal.md`
— a path #685 deleted when it archived that packet on 2026-09-05.** The row is
REMOVED in the fold commit. It is pre-existing on `main` and is not this packet's
defect; it is repaired here because this pull request is already editing that
block and leaving a dangling Active row beside a new one would be worse. The
archived row at the foot of the file is the live one and is untouched.

## 9. What lands, and what is still owed

**Lands with this ratification:** the delta, the code and its test, the README
row and the ledger row.

**Still owed, and NOT by this word:**

1. **The suppression successor (§ 4, P2 / `design.md` D6).** Split the arm on the
   fact the read already has: a held tip with no readable changelog is an ANSWER
   — no SPENT declaration exists — and the `in_scope` loop should run with no
   declarations rather than be skipped past; a tip that could not be read at all
   keeps the skip. The carried `THEN` bullet is what that successor amends.
2. **The archive act.** `code_surface: openxFactory` means this packet does NOT
   archive on landing: under `release-realization` it archives on merged-plus-green
   realization evidence, which this pull request produces. The archive is a
   separate pull request opened after this one merges, promoting the MODIFIED
   requirement into `openspec/specs/doc-health/spec.md` with its marker.
