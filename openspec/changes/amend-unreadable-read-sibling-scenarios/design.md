# Design: amend-unreadable-read-sibling-scenarios

Status: ratified
Ratified by: amend-unreadable-read-sibling-scenarios — 2026-09-05, Brett Heap, "ratify 688, land it when green" (record `review/ratification-2026-09-05.md`)
Date: 2026-09-05
Kind: design

## 0. The brief

`amend-published-tip-unreadable-scenario` (openxFactory PR **#678**, merged
`87c15baa`, archived by **#685**) replaced ONE clause in `doc-health`'s
*Release-tag publication*. Its own `tasks.md` § 4.2 records that the identical
clause was written a second time over `contracts/CHANGELOG.md`, that widening a
ratified packet after the word that ratified it would be a different change, and
that the sibling is therefore **an owed successor** — with one reading owed
first: *"the changelog read has no presence probe of its own, it inherits the
manifest read's."*

This document takes that reading and the three decisions that follow from it.

## D0 — the sweep, and what it found

Three angles over `openspec/specs/`, run on the tree this packet is authored on:

1. the retired phrase — `commonest cause`;
2. the fact it misnames — `not fetched` / `unfetched` / `has not fetched`;
3. the shape it sits in — `answers nothing` / `cannot be read`.

**ONE live sibling.** `openspec/specs/doc-health/spec.md:2818`, the `WHEN` of
*The changelog cannot be read at the published tip*. Everything else the sweep
raised is a false positive and each is named in `tasks.md` § 2 with its reason —
including `spec.md:2715`, which is #678's own `Removed from canon by` MARKER and
carries the retired manifest clause as the quoted unit it declares. **A marker
is not a scenario and must not be edited**: it is the record of the removal, its
durability is required by the same requirement that defines it, and rewriting
the quoted unit would leave the marker naming a unit that was never in canon.

## D1 — the promoted `THEN` and the `WHEN`-side placement are INHERITED, not re-taken

#678's D1 decided that the establishing obligation is written as a `WHEN`-side
`AND` rather than a `THEN`-side `MUST`, and its D2 decided that the promoted
`THEN` (*"report a skip naming that read"*) is carried byte-identical even
though the widened `WHEN` makes it looser.

**Both are ratified canon now and this packet re-opens neither.** The sibling
scenario is written in the same shape for the same reasons, and the cost #678
recorded — a `WHEN`-side obligation is weaker as a compliance hook — is
inherited with it. Re-litigating a decision the ratifier already took, in a
packet whose whole point is that the two siblings should read alike, would be
the opposite of what the successor is for. **The remedy if that cost is ever
judged too high is one change over BOTH scenarios**, not a divergence introduced
here.

## D2 — the third bullet is IN, and it makes this a code surface

**The question, and it is this packet's veto point.** #678's shape has three
moving parts: two facts in the `WHEN`, a `WHEN`-side establishing `AND`, and a
`THEN`-side `AND` requiring the held-and-empty case to be answered in its own
words and to STATE THE PRESENCE. The first two are satisfied by the family as it
stands. The third is not: the changelog read has one skip and it says only that
the file *"could not be read at the published tip"*.

**Option A — write two bullets, keep `code_surface: none`.** The delta stays
prose-only and archives on landing. **Rejected.** It would leave canon
permitting the exact answer #612 was filed against — a tip the checkout HOLDS,
reported in words a reader is entitled to read as a fetch defect — and it would
make the two sibling scenarios say different things about the same class for no
reason a later reader could reconstruct.

**Option B — write three bullets and leave the code owing.** Canon out-runs the
machinery by one `MUST`. **Rejected**, and it is rejected on this repository's
own lesson: #678 was explicitly *"canon catching up with the checker"*, and a
successor that inverts that in the same requirement, in the same week, is worse
than the defect it fixes.

**Decision: option C — write three bullets AND make the third true here.** One
`Skip` reason and the comment above it in
`scripts/doc_health/release_tag_publication.py`, one test added, and
`code_surface: openxFactory` declared rather than dodged. **The cost, said
plainly:** under `release-realization` this packet no longer archives on
landing; it archives on merged-plus-green realization evidence, which its own
pull request produces. That is a slower path than #678's for a two-line edit,
and it is the honest one.

## D3 — the probe is NOT added, and the reason is written into the scenario

The amended `WHEN`-side `AND` says the family has established which fact holds
*"here by INHERITANCE and completely"*. That clause is doing real work and is
not decoration:

- `check_repo` runs `obtain_commit(tip)` before any read (PR #646,
  `2177b2a2`), and both `manifest is None` arms return before the changelog is
  consulted;
- `blobs_at` sends `<commit>:<path>` to `cat-file --batch`, which reports EVERY
  spec of a commit the clone does not hold as *missing* — so a manifest that
  read is proof the commit is held;
- therefore, at the changelog guard, the unfetched fact is **excluded**, not
  merely improbable.

Writing that into the scenario is what stops a later reader concluding the
changelog read needs a second `obtain_commit` of its own. **A second probe would
be a redundant round trip justified by nothing, and this is the packet where
somebody would otherwise add it.**

## D4 — the code edit is a WORDING edit and touches no control flow

The guard's position, its `in_scope` gate, its return type and the state it
answers are all unchanged; a below-floor repository with no changelog still
returns `[]`. What changes is the reason string and the comment above it. The
three substrings the existing suite pins — `contracts/CHANGELOG.md could not be
read at the published tip`, `not the same fact as there being none`, and the
in-scope bundle name — are all still carried, deliberately, so the existing
assertion keeps its meaning and the new assertions are added beside it rather
than replacing it.

**The new skip is also pinned NEGATIVELY**, against the manifest arm's *"a
bounded fetch of exactly that commit was attempted and did not obtain it"*. Two
skips that are only positively pinned can drift into each other's words, which
is the defect class this whole family of amendments exists to close.

**AND THE WORDING SAYS ONLY WHAT THE PRESENCE PROVES** (PR #688 adversarial
review, P3). The first draft of this skip said the commit *"IS present and
carries no `contracts/CHANGELOG.md`"*, and the second half of that is a claim
about the TREE which the read cannot support. `blobs_at`'s per-path None is
answered for a THIRD state as well as the two the scenario names: a store that
holds the commit AND its trees but not the blob object. It is not hypothetical —
remove the loose object from a store and `cat-file --batch` answers `<spec>
missing` for a path `ls-tree` still lists. So the skip is written as the read it
has, *"the commit is held in this store and no readable `contracts/CHANGELOG.md`
blob is reachable at it"*, which is TRUE OF BOTH held states; the amended `WHEN`
folds that third state into its held arm rather than claiming an exhaustiveness
it does not have; and the over-claiming form is pinned against NEGATIVELY in the
same test, so it cannot come back.

## D5 — one unit is dropped, so the marker is owed and is carried

Exactly as #678's D3. The block REPLACES a bullet, so under `doc-health`'s
*Currency of an active change's MODIFIED requirement blocks* the dropped canon
unit is reported unless a reserved marker declares it. The block carries:

```
**Removed from canon by amend-unreadable-read-sibling-scenarios (2026-09-05):**
``<the old changelog WHEN bullet, verbatim>`` — <reason>
```

The unit is quoted as a code span with the list marker stripped, in a
DOUBLE-backtick span because the unit itself contains a single-backtick code
span (`` `contracts/CHANGELOG.md` ``) — CommonMark closes a run of N backticks
only on a run of exactly N, which is the rule
`modified_block_currency.extract_code_spans` implements. **It is a REPLACEMENT,
not a deletion**, and the marker's reason says so.

#678's own marker and amendment note are canon units of this requirement now.
They are **carried byte-identical and are not restated, reworded or merged**;
the new note is added below them so the two amendments read in the order they
happened.

## D6 — the skip STILL SUPPRESSES the grading, and that is left to the successor

**The finding (PR #688 adversarial review, P2), stated at full strength.** The
amended `WHEN`-side `AND` establishes that the only fact reachable at this arm
is a HELD tip carrying no readable `contracts/CHANGELOG.md`. The promoted `THEN`
carried byte-identical then says the family *"MUST NOT treat the absence of a
declaration it could not look for as the absence of a declaration"* — which
presumes the family COULD NOT LOOK. At this arm it could: the commit is held,
and a file that is provably not there is not a read that failed.

**And the code still answers it as one.** The `if changelog is None:` guard
stands ABOVE the `in_scope` loop and RETURNS, so a held tip with an in-scope
bundle and no changelog is answered with a skip INSTEAD OF the tag findings the
loop would have emitted. Measured on a shim: tag absent and no changelog blob →
one `Skip`; the same shim with an EMPTY changelog → one `error` naming the
untagged bundle. A provably absent changelog SUPPRESSES a finding an empty one
does not.

**Decision: this packet stops at wording, and the successor is named.**

- It is **NOT A REGRESSION.** The identical shim answers identically at
  `origin/main`; the position, the gate and the return are carried unchanged
  (D4), and the packet moves one string and one comment.
- It is **NOT THIS PACKET'S TO FIX.** Moving that return decides WHICH FINDINGS
  an in-scope repository receives. That is a behaviour change: it needs its own
  scenarios (what the family reports for a bundle whose SPENT state genuinely
  could not be read, versus one where the document is simply not there), its own
  severity reading, and its own measurement over the nightly. A packet whose
  whole claim is *"one skip's TEXT, for one reachable state"* cannot carry it
  without becoming the thing #678's lesson warns against — a scope that grew
  after the reading that justified it.
- It is **NOT SILENTLY CARRIED.** The cost is written into `proposal.md`
  § What this proposal does NOT claim as a named carve-out, and `tasks.md` § 6
  names the successor as OWED, in the same shape #678 used to name this packet.

**What the successor owes**, so it is not re-derived: split the arm on the fact
the read already has. A held tip with no readable changelog is an ANSWER — no
SPENT declaration exists — and the loop should run with no declarations rather
than be skipped past; a tip that could not be read at all keeps the skip. The
`THEN` bullet carried here is what that successor amends, and it is the reason
this packet did not rewrite it.

