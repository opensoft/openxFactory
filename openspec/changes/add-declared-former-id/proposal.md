---
code_surface: openxFactory — MEASURED on the clone of `main` @ `9378eca5` this packet was authored against, and named as the surface a LATER realization pull request moves, nothing here being realized. (1) `scripts/proposal-support.py`: `ratifying_commit` gains the declared identities and resolves the baseline across them, its two history reads separate ABSENT from UNREADABLE, and `origin_retention_errors` refuses rather than skipping where the baseline read fails — today `ratifying_commit` derives one path from the id the tree spells (`rel = f"openspec/changes/{change}/proposal.md"`) and `git_show_text` returns `None` for both conditions alike. (2) A NEW reader and a NEW validator CLI for the landing refusal, in the shape `gate-realization-axis-vocabulary` established, run as a required check. (3) A NEW reader for the reference-resolution rule. (4) `tests/proposal-support/test_proposal_support.py` and a new test module for the validator. (5) `docs/document-lifecycle.md`, whose ratified sentence "Renaming a ratified change is therefore blocked until a change declares a FORMER ID (issue #833, a successor packet)" this packet answers. NOT THIS PACKET'S SURFACE AND NOT TOUCHED BY THIS PULL REQUEST: nothing under `openspec/specs/`, no workflow, no contract, no register, no script and no test — the diff is `openspec/changes/add-declared-former-id/**` and one README row.
target_release: implemented (the openxFactory main line). No contract bundle is cut, nothing under `contracts/` moves, no digest set changes, no `contract_bundle_version` is spent and no release tag is owed: `.openspec.yaml` is a change packet's own file, not a registered row in `contracts/manifest.yaml`, and it appears in no `contracts/releases/*.digests.yaml` inventory. `deferred-allocation` is deliberately NOT declared — `add-target-release-deferred-allocation` admits that value only where a bundle is cut, and none is. Under *Realization archive gate* a non-empty code surface archives on merged-plus-green realization evidence rather than on landing.
sequenced_after: []
---

# Proposal: add-declared-former-id

Status: draft
Proposed: 2026-09-13, in lane `openxfactory-1` (display `openXfactory-1`),
session `3da6c3f9`, as the standing claim holder of openxFactory
[#1003](https://github.com/opensoft/openxFactory/issues/1003) (CLAIMED
2026-09-13T01:37:03Z).
Origin: Brett Heap's RULING of 2026-09-13 at approximately 03:0xZ, verbatim
**"option 2 on 1003 with the fix"**, recorded at
[issuecomment-5650519818](https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5650519818);
and openxFactory [#833](https://github.com/opensoft/openxFactory/issues/833),
whose "Remedy shape" paragraph named this mechanism as option (b) and called it
"a later packet".

**THE RULING SELECTS A REMEDY SHAPE AND RATIFIES NO WORDING.** It names the
mechanism — a declared former id over `release-realization`, fail-closed on the
undeclared case, with #833's dangling-cited-path finding swept in — and it
NOT-SELECTS two alternatives by name: a full rename-lineage walk and an
all-rename-chain interim guard, as "history-walking archaeology that cannot
carry the intent bit distinguishing rename-of-ratified from lawful
fork-by-copy". Every sentence below that the ruling did not give is this lane's
authoring, offered for veto; `design.md` puts the five decisions most worth one
as questions with the recommendation first.

## Why

**A GATE BLOCKS AN ACT AND NAMES THE PACKET THAT WOULD UNBLOCK IT.** The archive
gate compares a packet's origin declaration against *"the declaration present at
ratification"*, and it finds that ratification by walking one path derived from
the change id the tree spells today. A ratified packet whose directory is
renamed has no history under its new name before the rename, so the walk's first
ratified blob is the RENAME COMMIT — later than every mutation made in between,
and the gate printed `ORIGIN RETAINED` over it (measured on issue #777, filed as
issue #833). PR #846 closed that by REFUSING rather than re-basing, and its own
refusal text states why the refusal was the whole of the fix:

> Nothing in this corpus declares a FORMER ID, so the baseline cannot be
> established from history alone and this walk refuses rather than re-basing
> onto that commit: archive `<change>` under the id it was ratified with, or
> land the former-id declaration (a later packet) before renaming a ratified
> change.

`docs/document-lifecycle.md`, ratified by that same act and carrying
`Status: standard`, states the consequence as canon: *"Renaming a ratified
change is therefore blocked until a change declares a FORMER ID (issue #833, a
successor packet)"*. **This is that successor packet**, and the blocked act is
not hypothetical: issue #777's own second half left a change id dotted
(`bump-openspec-cli-pin-to-1.12`) on the ruling *"Rename the draft only now"*,
because the rename it wanted was of something already ratified.

**AND THE REFUSAL DOES NOT REACH A CHAIN.** Issue #1003, routed off PR #999's
review bench, reproduces `ratify r -> rename+un-ratify r->s -> rename s->t while
draft -> ratify t`. The walk for `t` begins at the `s->t` hop, whose former blob
is a draft and refuses nothing; the `r->s` hop that actually moved the ratified
packet is never enumerated, because the enumeration underneath is a path-limited
`git log` for the name the tree spells today and a path-limited `git log`
follows no rename. The later re-ratification is then taken as the baseline —
`ratified_under_a_former_path`'s own docstring already names the reason the
wider closure was not taken:

> The wider closure […] cannot separate "an already-ratified packet renamed and
> un-ratified in one commit" from "a NEW packet authored as a copy of a ratified
> one, entering as a draft and ratified later": both are, to history, "source
> ratified at the hop's parent, destination not ratified at the hop".

**THAT IS THE WHOLE ARGUMENT FOR A DECLARATION.** History records that two paths
are similar. It cannot record what the author MEANT by the similarity, and the
two meanings need opposite answers: a rename of a ratified packet must keep its
ratification, and a fork authored as a copy of a ratified packet must get its
own. No walk, of any depth, can tell them apart — and the gate has no bypass
flag by design (#690), so a walk that guesses wrong makes a lawful fork
permanently unarchivable.

**THE SUBSTRATE THAT WOULD HAVE TO CARRY THE GUESS LOSES THE HOP THAT MATTERS,
MEASURED RATHER THAN FEARED.** On git 2.43.0, against a `--filter=blob:none
--no-checkout` clone of the #1003 fixture whose promisor remote was made
unreachable:

| read, at the hop that renames AND un-ratifies in one commit | full clone | that clone |
| --- | --- | --- |
| `git log --follow --find-renames --name-status -1 <hop> -- <destination>` | `R075 <source> <destination>` | **no record at all** |
| `git ls-tree --name-only <hop>^ -- <source>` | the row, exit 0 | **the row, exit 0** |
| `git show <hop>^:<source>` | the blob, exit 0 | exit 128 |

The pairing is computed from content, so the checkout that cannot read content
reports no rename — and the hop it loses is the dangerous one by construction,
an un-ratifying rename being a rename that also edits. Meanwhile the TREE still
names the predecessor. A declaration is read from the tree.

**AND THE SAME SILENCE READS AS TWO DIFFERENT ANSWERS.** On that clone,
`git ls-tree --name-only` prints the row and exits 0 for a path present in the
tree whose blob is unavailable, and prints NOTHING and exits 0 for a path that
is genuinely absent; `git cat-file -e` and `git show` exit 128 for BOTH. So the
two reads this estate uses to ask "was the packet there" cannot tell "there is
nothing there" from "I cannot tell you", and a gate that reads the second as the
first switches itself off exactly where it can prove nothing. PR #1024 measured
the same distinction and recorded it at its
[FREEZE](https://github.com/opensoft/openxFactory/pull/1024#issuecomment-5651182318);
it is re-measured here so the figure is this packet's.

**THE CITED-PATH HALF OF #833 IS THE SAME DEFECT WITHOUT THE GATE.** #833's
closing paragraph found that `contracts/openspec-cli-pin.yaml`'s
`dispositions[].cited_to` paths and a citation at
`openspec/changes/disposition-codexfactory-declared-renames/design.md` *"would
keep paths a rename breaks — nothing validates that a cited path resolves"*.
Re-measured on `main` `9378eca5` over every tracked file except
`openspec/changes/archive/` (frozen record), `tests/` and `specs/` (fixtures and
Spec Kit feats): **94** distinct `openspec/changes/<id>/…` references resolve to
nothing, and **58** of them resolve BY ID against the archive — the path broke
and the identity did not. The one #833 named is among them:
`openspec/changes/bump-openspec-cli-pin-to-1.12/specs/neutral-product-pin/spec.md`
now stands at
`openspec/changes/archive/2026-09-09-bump-openspec-cli-pin-to-1.12/specs/neutral-product-pin/spec.md`.
Nothing broke it on purpose: the archive relocation is an act every packet
performs exactly once, and it moves the path while preserving the identity.

## What changes

Three obligations canon does not have, and one it has in a form that cannot be
met after a lawful move.

1. **A moved packet declares the identity it was ratified under** (ADDED). A
   top-level `former_ids:` list in the packet's own `.openspec.yaml`, a sibling
   of `origin:` and never a member of it, naming change IDS and never paths,
   ordered oldest first and APPEND-ONLY ACROSS COMMITS — a later commit that
   removes, reorders or respells an established entry is refused, whether or not
   it moves anything. An entry is added only by the commit that performs the
   move it records, so a standing packet cannot append an identity it never had.
   A former identity has EXACTLY ONE OWNER. The archive relocation is not a move
   under this requirement and is never declared. A declared former id that still
   stands as a live directory is refused — that shape is a copy.
2. **An undeclared rename arrival is refused at its landing** (ADDED). A commit
   that brings a packet directory in by a move from another packet directory
   WHOSE IDENTITY HAS EVER DECLARED `Status: ratified` is refused unless the
   arriving packet declares the source id in the SAME commit; a move of a packet
   that has never been ratified stays lawful and declares nothing, as the
   promoted realization record already promises. The test is EVER, over the
   source's whole DECLARED LINEAGE — its own id together with every id it
   declares — and never its blob at the parent: a packet renamed and un-ratified
   in one commit is back in draft at every later hop, and a packet that already
   moved once carries its ratification under an id its own header never bore.
   The arriving packet's list is the source's list with the source id appended,
   so no move sheds a lineage.
   A move lands as one commit, so one commit is read and no chain is ever
   walked. The arrival read fails closed: where the pairing cannot be computed
   and the tree shows both an arrival and a departure, the gate refuses CANNOT
   RUN rather than reporting no arrival. No bypass flag.
3. **A packet reference resolves by identity, not by path** (ADDED). A reference
   that addresses a packet resolves by its change id — against the location that
   id occupies now, active or archived, and against any packet declaring that id
   as a former id. BOTH HALVES of a packet-relative citation resolve: the
   location the identity resolves to must also carry the file the citation
   names, and a failure says which half failed. Resolution is to EXACTLY ONE
   packet or to nothing and never to a set: an id that would resolve twice is
   reported AMBIGUOUS, never settled by sort order. A reference is dangling only when it resolves to nothing under
   that rule, and a reference that resolves owes the citing record no edit.
4. **Origin retention at archive** (MODIFIED). The baseline is resolved across
   the current identity and every declared former identity together, taking the
   EARLIEST commit at which any of them declares `Status: ratified`; the
   resolution is by identity and never by rename detection; the comparison
   itself does not move, so a rename is not a way to acquire a later baseline
   and therefore not a way to launder a mutation; and every read behind the
   baseline fails closed, with ABSENT distinguished from UNREADABLE. Every
   promoted sentence and all three promoted scenarios are carried verbatim.

**THE INTENT BIT, SAID PLAINLY.** A declared former id is the author's statement
*this directory IS that ratified packet, moved*: it inherits that identity's
ratification and its origin-retention baseline. Its ABSENCE at a rename arrival
is a refusal, not a default — a mechanism that only reads declarations protects
the author who writes one, and the failure this exists to catch is a rename
whose author would not declare it. A fork-by-copy declares nothing, keeps its
own origin, is baselined at its own first ratification, and is never refused,
the source packet still standing.

## What this packet does NOT do

- **No history walk, of any kind.** Not a rename-lineage enumeration, not a
  hop-classified chain guard, not `--follow` over a packet's ancestry. The two
  candidates the ruling NOT-SELECTED are named here so a later reader does not
  re-propose them: option 1, the full rename-lineage walk (authored and measured
  as PR #1024, CLOSED in favour of this packet, branch retained at `2bc60386`),
  and option 3, an interim guard scoped to all-rename chains.
- **Nothing is realized here.** No script, validator, register, workflow or test
  is added or edited; `tasks.md` carries the realization slices unticked.
- **The interim pin is a separate pull request.** The multi-hop gap named in
  `ratifying_commit`'s docstring and pinned by a fixture — the #846 precedent,
  part 2 of the ruling — is a plain fix on `fix/1003-interim-pin-multi-hop-gap`
  and is deliberately not carried here.
- **No `doc-health` delta**, decided rather than omitted: `design.md` D4 records
  the reasoning and the measured cost.
- **Nothing anyone else authored is edited.** In particular
  `disposition-codexfactory-declared-renames`, which carries the live dangling
  citation, keeps its ratified prose exactly as it stands: the repair is a
  resolution rule applied by the reader, not a rewrite by the citing packet.

## Successors and relations

- **openxFactory #1003 stays OPEN.** Whether and when it closes is Brett Heap's
  word; it is referenced and never closed by this packet, and no commit message
  or body here carries a closing keyword.
- **openxFactory #833 no longer stands open**: PR #846 took its remedy shape (a).
  This packet takes shape (b), which that issue itself called "a later packet",
  and sweeps in the dangling-cited-path finding of its closing paragraph.
- **PR #1024 is CLOSED in favour of this packet**, recorded at
  [issuecomment-5651210736](https://github.com/opensoft/openxFactory/pull/1024#issuecomment-5651210736).
  Its branch is retained at `2bc60386` as the salvage reference: its fail-closed
  reads are candidates for this mechanism's realization, and its FREEZE comment
  records the partial-checkout measurements re-taken above.
- **Ratification is Brett Heap's word**, and it is a separate act from this
  landing. Realization and archive are two further acts on two further words.
