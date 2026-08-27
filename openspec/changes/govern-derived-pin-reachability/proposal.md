---
code_surface: openxFactory (`scripts/doc_health/ideation_readiness.py` — the pinned-revision resolution point the sibling `harden-ideation-readiness-check` just made honest, which is where a class-wide reachability verification joins rather than a second spelling of the same probe; a declared pin-class table, whose home is Q1 and which is NOT pre-placed here; `scripts/bootstrap-ideation-cross-reference.py` — `git_generation()` at `:144-154`, READ ONLY as the reference generator whose `source_revision` stamp defines the reproduction obligation, with NO change proposed to it by this packet; plus regressions under `tests/doc-health/`. NO change is proposed to `derive_clusters`, the derivation prompt or evidence contracts, the index schema, the gate constants, the readiness lane's severity or disposition, the deterministic check family registry `scripts/doc_health/families.py`, or the family enumeration and its numerals.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle, and that is measured rather than assumed: `grep`ing every `contracts/releases/*.digests.yaml` inventory for the named files returns nothing, so no schema moves, no digest set changes, and no release tag is owed. The archive gate is therefore merge-plus-green on main, PLUS one piece of evidence the code alone cannot give — a resolution for the two live orphaned pins § What was measured names, because the verification this change proposes turns both of them red and the change would otherwise land red on its own gate. THAT PIECE IS ALREADY DISCHARGED, 2026-08-27: Q2 was ruled "publish first, independently" and executed, and `git ls-remote origin 'refs/retention/*'` returns `refs/retention/pins/da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` and `refs/retention/pins/f13a3b6007736292e1e157febef1ac733e534de9`, each at the commit its name states, so both records are conforming with their original pins UNEDITED. AS AUTHORED this sentence read "Whether that resolution rides this change or lands before it is Q2" — now historical; it landed before, which is what the recommendation asked for and why the garbage-collection window is closed rather than merely noted. Concretely: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a scratch-clone run of the class-wide verification that reports the class fully covered. THE CHANGE SHIPS ACTIVE and archives only after that.
Status: ratified
Ratified: 2026-08-27 by Brett — in-session commissioning of the filing, verbatim: "file the pin-governance follow-up change". The citation covers THE DECISION TO FILE THIS CHANGE AND NOTHING ELSE; the five decisions in § Orchestrator decisions below were taken by the authoring session under standing patterns and are NOT covered by it, nor are the three questions in § Open Questions. The record this citation resolves against is this file, § Orchestrator decisions and § Open Questions. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, and clears its three-way floor on all three axes rather than on the one it needs: approver (`by Brett`), date (`2026-08-27`), and a resolvable record path. AS FIRST WRITTEN this line ended at "a resolvable record path" with the decisions and questions still live — that was true at authoring and is now historical on both halves: Brett cleared all five decisions as authored and ruled all three questions the same day, by a SEPARATE four-question multi-choice recorded in full at § Orchestrator decisions and question by question at § Open Questions. THE TWO ACTS STAY DISTINCT ON PURPOSE, because they authorized different things: this citation ADMITTED the packet, the later ruling CLOSED the veto window and disposed Q1, Q2 and Q3 — and unlike the clearance, the Q2 and Q3 rulings CHANGED the packet. No verbatim wording of the later ruling reached this session, so none is quoted; approver, date, mechanism and selected option are stated instead.
Proposed: 2026-08-27
Origin: The follow-up two archived packets named and declined to write. `harden-ideation-readiness-check` made an unreachable pin loud and repaired one instance; `fix-release-reachability-race` recorded the same orphaned pin as its family's stale operand. Neither stated the rule that would have prevented the instance. This packet states it, and finds two more instances still standing on `main` while doing so.
---

# Proposal: govern-derived-pin-reachability

## Why

On `main` today, two committed artifacts pin commits that no ref in this
repository reaches. Neither pin can be resolved by any reader. Both artifacts
exist to say what state a run derived its content from, and about both of them
that sentence is now uncheckable — not out of date, but unanswerable.

They are the residue of one landing. Pull request #322 regenerated
`ideation/cross-reference.yaml` on a branch, correctly pinning the branch commit
`da9bf3b7`; the pin was then moved by hand to the branch tip `f13a3b60` with no
regeneration of the body; and the branch landed REWRITTEN as `4e57009c`, which
orphaned both commits at once. `harden-ideation-readiness-check` repaired the
index and made the consequence loud — an unresolvable pin now fails a proof
instead of skipping it — and named the governance rule as a future packet.
`fix-release-reachability-race`, filed the same week, put the same orphaned pin
in its family table as the stale operand of a sibling defect. Neither packet
stated the rule.

The rule is worth stating on its own evidence, because the consequence of not
having it was not one bad pin. It was seven proofs that never ran. The index's
orphaned pin made the readiness derivation proof `pytest.skip` in every fresh
clone for the packet's entire life, with a stated reason ("shallow clone?") that
was false in the one place it fired; isolated clones moved from 889 passed / 7
skipped to 920 passed / 0 skipped when the pin was repaired. An orphaned pin is
not cosmetic. It silently removes verification.

## The record that defers this rule, cited exactly

Both citations were read in the archive rather than recalled, and ONE OF THEM
DOES NOT SAY WHAT THIS PACKET WAS COMMISSIONED BELIEVING IT SAYS. The
discrepancy is recorded here rather than smoothed over, because a packet whose
first act is to cite a record inaccurately has no standing to demand that pins
be verifiable.

**`openspec/changes/archive/2026-08-27-harden-ideation-readiness-check/` DOES
defer this rule by name, twice.** `proposal.md` § Named follow-ups, out of scope
here, first bullet: "The governance rule that an index pin must be rewritten
when a branch lands rebased or squashed is a SEPARATE FUTURE PACKET and is
deliberately not proposed here… it is about how packets land, it would bind
every generator that records a `source_revision`, and it interacts with the
house rule against squash merges (`4e57009c` is itself a squash). That packet
should be raised on its own evidence." And `tasks.md` § 5.2, unticked at the
archive: "THE FOLLOW-UP PACKET, NAMED AND NOT WRITTEN: the governance rule that
a `source_revision` recorded on a branch must be re-derived when that branch
lands rewritten." Its § Orchestrator decisions OD-1 additionally records that an
index-side requirement in `ideation-cross-reference` was CONSIDERED AND DECLINED
there, in these words: "an index-side obligation is close enough to the deferred
governance packet above to risk pre-empting it." This packet is that packet, and
it takes the index-side requirement that decline reserved.

**`openspec/changes/archive/2026-08-26-fix-release-reachability-race/` DOES NOT
defer this rule by name, and the commission's description of it is corrected
here.** Its § Named follow-ups carries three bullets — the unswept sibling
modules under `scripts/hermes_runtime_validation/`, the eleven-minute exposure
window, and whether a verification may consult the network at all — and none is
about pins. What that packet DOES carry is § Family relation, whose table names
"an index pin (`source_revision`) no ref reaches" as the STALE OPERAND of the
one defect family both packets belong to: "a verification that answers a
question about LIVE state using PINNED or STALE state, and reports the mismatch
as a fact about the subject rather than about itself." That is a real and useful
citation, and it is the one made here. Searched to establish the absence:
`defect in its own right`, `lands rebased`, `rebas`, `squash`, `orphan` and
`unreachable from main` return no match anywhere in that packet's four files.

## What was measured

All measurements 2026-08-27, in a fresh worktree off `origin/main` at
`42662b70`, in this repository.

**Two orphaned pins still stand on `main`.** Both are readiness-run evidence
records left over from the same landing:

| artifact | pin | reachable from any ref | status header |
| --- | --- | --- | --- |
| `health/ideation-readiness/2026-08-24/brainstorm-packet-migration-20260824.yaml:5` | `da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` | **no** | `record` |
| `health/ideation-readiness/2026-08-24/brainstorm-packet-migration-final-20260824.yaml:5` | `f13a3b6007736292e1e157febef1ac733e534de9` | **no** | `record` |

For each: `git branch -a --contains <pin>` returns EMPTY, `git ls-remote origin
| grep -c <pin>` returns `0`, and `git merge-base --is-ancestor <pin>
origin/main` is false. `f13a3b60` is the same commit the sibling packet repaired
out of the index — it repaired the index and left this record, which is exactly
the coverage gap this packet's third requirement is about. `da9bf3b7` is the
CORRECTLY GENERATED branch pin, orphaned by the rewrite through no fault of the
generator, which is why the landing rule cannot be reduced to "do not move pins
by hand".

**Both objects are still recoverable today, and that is time-bound.**
`git cat-file -t` returns `commit` for both in this worktree's shared object
store, so a retention ref is publishable now. Neither is on the remote, so the
window closes when garbage collection reaches the last clone holding them. This
is the measurement the second requirement obliges a packet to take before
choosing a route, taken here.

> **THE WINDOW WAS ACTED ON THE SAME DAY, AND THE TWO ROWS ABOVE ARE NOW
> HISTORICAL ON THEIR LAST COLUMN.** Q2 was ruled "publish first, independently"
> and executed on 2026-08-27, and this session verified the result rather than
> taking it on report: `git ls-remote origin 'refs/retention/*'` returns exactly
> two rows —
> `refs/retention/pins/da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` at
> `da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` and
> `refs/retention/pins/f13a3b6007736292e1e157febef1ac733e534de9` at
> `f13a3b6007736292e1e157febef1ac733e534de9` — so `git ls-remote origin |
> grep -c <pin>` now returns `1` for both pins where the table above records
> `0`. **BOTH RECORDS ARE NOW CONFORMING WITH THEIR ORIGINAL PINS UNEDITED**,
> which is requirement 2's whole claim demonstrated on the two instances that
> forced it. `merge-base --is-ancestor origin/main` is STILL false for both, and
> that is the point rather than a residue: the pins resolve through the retention
> namespace, not through `main`. The measurements above are kept exactly as taken
> because they are the evidence the rule was needed, and a table rewritten to
> show the repaired state would erase the defect it was written to prove.

**The landing was a rewrite, confirmed at the object.** `git log --format='%H %p
%s' -1 4e57009c` gives a SINGLE parent `700c1a19` and the subject "Migrate
brainstorms into three-tier packets (#322)" — a squashed landing, not a merge
commit, which is what made `da9bf3b7` unreachable rather than merely
non-tip.

**The index itself is now conforming.** `ideation/cross-reference.yaml:10` and
`ideation/cross-reference.md:9` both pin `4e57009c`, which IS an ancestor of
`origin/main`. The sibling's repair holds.

**Every other real pin in the repository resolves.** Reachability was measured
for all of them, not sampled; the results are the inventory below.

## The pin-carrying artifact inventory

Swept by `git grep` over committed files for `source_revision` and for the
sibling key names a generator might plausibly use (`source_commit`, `commit`,
`commit_sha`, `revision`, `source_rev`, `git_commit`, `derived_from`,
`base_commit`, `pinned_commit`, `source_ref`, `generated_from`, `head_commit`,
`corpus_revision`), then every hit carrying a full hexadecimal object name was
resolved against `origin/main`.

**IN SCOPE — committed artifacts recording a repo-local commit pin as their
derivation source (9 pins, 8 artifacts):**

| artifact | key | pin | ancestor of `origin/main` |
| --- | --- | --- | --- |
| `ideation/cross-reference.yaml:10` | `generation.source_revision` | `4e57009c` | yes |
| `ideation/cross-reference.md:9` | `Source revision:` | `4e57009c` | yes |
| `health/ideation-readiness/2026-08-24/brainstorm-packet-migration-20260824.yaml:5` | `source_revision` | `da9bf3b7` | **NO** |
| `health/ideation-readiness/2026-08-24/brainstorm-packet-migration-final-20260824.yaml:5` | `source_revision` | `f13a3b60` | **NO** |
| `health/derive-possibles/2026-07-23/derive-possibles-30000105423-1.yaml:5` | `source_revision` | `3e6784f5` | yes |
| `health/derive-possibles/2026-07-26/derive-possibles-30186143362-1.yaml:5` | `source_revision` | `41e005ff` | yes |
| `ideation/dashboard/gate-records/add-council-clearance-rule-template/demote-20260805T111527Z.transition-manifest.yaml:17` | `source_revision` | `b8ef31ab` | yes |
| `ideation/dashboard/gate-records/ideation-staging-consent-instrument-contract-consent-instrument-design-decisions/create-document-20260731T231323Z.gate-action.yaml:24` | inside a `recipe:` prose string | `d09d5820` | yes |
| `specs/008-identity-brokering-contracts/traceability.yaml:495` | `source_revision` | `5f59a32f` | yes |

Four distinct generators produce these: the cross-reference bootstrap
(`scripts/bootstrap-ideation-cross-reference.py` `git_generation()`, plus its
renderer for the `.md` twin), the readiness lane, the possibles-derivation lane,
and the dashboard gate console. A fifth pin sits inside a prose `recipe:` string
rather than in a field of its own, which is a genuine wrinkle for any scanner and
is why the class is DECLARED rather than pattern-discovered in the third
requirement.

**Contract-declared but not yet committed anywhere as a real pin:** the
`ideation-dashboard-snapshot`, `ideation-dashboard-snapshot-index`,
`ideation-workbench` and `xfactory-ideation-organizer-recommendations` schemas
all require a `source_revision`, and `gate-intent.schema.yaml` carries
`snapshot_rev_seen` for optimistic concurrency. No committed instance of any of
them holds a real repository commit today — the only instances are examples and
fixtures — so they are future members of the class rather than current ones.
That is precisely the case the declared-class check exists to catch: the day a
snapshot index lands committed, its pins join the class, and nobody will
remember to add them.

**OUT OF SCOPE, and named so the boundary is not left to inference:** every
pin naming state in a DIFFERENT repository. The aggregation repo's submodule
gitlinks and the workflow-pin lockstep rule that governs them (xFactory
`CLAUDE.md` working rule 2); `pinned_contract_manifest` entries and the
`neutral-product-pin` grammar; `contracts/releases/*.digests.yaml` blob digests
and the `release-surface-integrity` obligations over them; container image
digests. Their reachability question is answered against another remote by
another authority, and folding them in here would put four capabilities' rules
in one requirement. Also out: every `commit:` value under
`contracts/*/fixtures/` and `examples/`, which are synthetic (`dddd…`, `1111…`)
or deliberately frozen sample data and are not derivation pins of this
repository.

## What this changes

Four requirements, all ADDED, across three capabilities. Sixteen scenarios. No
requirement is MODIFIED anywhere.

1. **`ideation-cross-reference` — a committed derivation pin stays resolvable.**
   The substantive rule: an orphaned pin is a defect in the artifact, a
   reachable-but-old pin is not. Reachability is judged against REFS rather than
   against a clone's object store, so a commit surviving locally is not a
   defence. Scope is stated in the requirement: repo-local commit pins;
   cross-repository pins are elsewhere's.

2. **`ideation-cross-reference` — an orphaned pin on an immutable record is
   repaired by retention, never by editing the record.** The rule the two live
   instances forced into existence. A `record` cannot be re-pinned without
   falsifying it and without tripping record immutability, so the COMMIT moves,
   not the record: publish `refs/retention/pins/<full-sha>` on the repository's
   own remote, the namespace Q3 ruled and Q2's execution already used, with the
   ref name COMPUTED from the pin rather than chosen. Where the object is gone, a
   superseding record plus a disposition, never a silent rewrite. And a packet
   must MEASURE recoverability before choosing, because the window closes.

3. **`release-realization` — a history-rewriting landing re-derives the pins its
   rewrite orphans.** The landing obligation, with re-pinning DEFINED BY
   REPRODUCTION: byte-for-byte at the new pin where the artifact's tooling
   defines derivation, a named measurement otherwise, and never a hand-moved pin
   — which is the exact act that produced `f13a3b60`. It also reaches artifacts
   the branch never touched, because a rewrite can orphan a commit that a
   previously landed artifact pins.

4. **`doc-health` — derivation-pin reachability is verified across a declared
   artifact class.** The enforcement, extending the sibling's index-only
   obligation to the class, with the class DECLARED and the declaration itself
   checked against what the repository carries. The two live orphans are the
   proof that a per-artifact obligation does not generalize on its own.

## What this deliberately does not change

- **No new deterministic check family.** The "Deterministic check families"
  requirement, its enumeration and its three numerals are untouched and
  deliberately unrestated. Two reasons, argued in the delta and in `design.md`
  § 3: reachability is not deterministic in that requirement's sense, because
  identical corpus inputs give different answers at different clone depths; and
  every added family owes a wholesale restatement of that requirement, which is
  how three changes in three days truncated it. **THE SECOND ARGUMENT WAS
  RE-CHECKED AGAINST A MOVING TARGET AND SURVIVED IT, 2026-08-27.** As authored
  it said `add-family-enumeration-check` is ACTIVE and holds the `MODIFIED`
  block. That packet ARCHIVED the same day, promoting the twenty-one enumeration,
  so for a few hours no active change held one — and the hazard did not go with
  it: `add-modified-block-currency-check` is now active, adds the TWENTY-SECOND
  family, and OWES that same `MODIFIED` block at its realization, restating
  canon's twenty-one to reach twenty-two. A family added here would have to
  restate the same requirement beside it and reach twenty-three, with canon's
  list decided by whichever archived last. The argument is stronger than when it
  was written, not weaker, and it is stated in the delta in the durable form —
  about the mechanism rather than about which change happens to hold the block
  today.
- **Nothing about the sibling's three promoted requirements moves.** The
  readiness proof's resolution order, its committed-state read point, and its
  unreachable-pin failure rule stand exactly as promoted. This change extends
  the third one's REACH by adding a class-wide obligation beside it; it does not
  restate or narrow it.
- **The generator is not touched.** `git_generation()` is read as the reference
  definition of a derivation stamp and nothing else. It did nothing wrong in the
  #322 landing: the pin it wrote was correct for the tree it ran on.
- **The house rule against squash merges is not re-litigated.** The rule that
  produced this defect's forcing instance is `--rebase`-only house practice, and
  `4e57009c` is a squash that predates nothing and violates nothing this packet
  owns. Requirement 3 binds ANY history-rewriting landing without ruling on
  which kinds are permitted.
- **The two live orphans are not repaired by this file.** A proposal is not a
  repair. The route is § 3 of `tasks.md` and the choice between riding this
  change and landing first is Q2. **STILL TRUE AS WRITTEN, AND NOW ALSO
  SETTLED**: Q2 was ruled "publish first, independently" and executed on
  2026-08-27 by the orchestrating session, so the repair happened OUTSIDE this
  file exactly as this bullet said it would — two published refs, not a commit
  here. `tasks.md` § 3 records the discharge with the verification.

### Named follow-ups, out of scope here

- **The generator's behaviour on a dirty tree.** `git_generation()` pins
  `rev-parse HEAD` regardless of whether the working tree is clean, so an index
  can record a provenance claim about content no commit holds. This is the
  sibling packet's own § 5.3 follow-up, observed on 2026-08-26 in the shared
  checkout, and it is a DISTINCT defect: it is about a pin that was never true,
  where this packet is about a pin that stopped being resolvable. A rule
  requiring reachability does not make a dirty-tree stamp honest, and a rule
  requiring a clean tree does not survive a rebase. Both are needed; they are
  not the same one.
- **The cross-repository pin families.** The aggregation gitlink and workflow-pin
  lockstep rule, `neutral-product-pin`, the release digest inventories, image
  digests. Different pin family, answered against a different remote, and for
  the gitlink rule a different repository entirely. Named in § The pin-carrying
  artifact inventory as out of scope rather than left implicit.
- **~~Whether a retention ref namespace should exist at all.~~ RULED AND NO
  LONGER A FOLLOW-UP.** Q3 was ruled on 2026-08-27: the namespace is formalized
  as `refs/retention/pins/<full-sha>`, and requirements 1, 2 and 4 now name it.
  AS AUTHORED this bullet read "Requirement 1 admits a 'retained ref the artifact
  or its owning contract declares' and requirement 2 obliges retention to be
  published, but neither invents a namespace, a naming grammar, or a retention
  lifetime." Two-thirds of that is now false and one-third stands: **retention
  LIFETIME is still unstated, deliberately**, and it is the only part of Q3 that
  survives as a real open question. The delta's reasoning is that a retained
  commit is retained because a committed record names it, so the ref outlives the
  record and a duration would need a rule for what happens at its end.
- **The three sibling resolver spellings.** The sibling's own § 5.1, ruled LEFT
  OPEN deliberately by Brett on 2026-08-27. Untouched here.

## Orchestrator decisions, cleared 2026-08-27 (authored: flagged for veto)

**ALL FIVE CLEARED 2026-08-27, THE SAME DAY THEY WERE FLAGGED — Brett approved
every one as authored, and none was vetoed.** The ruling came as a
four-question multi-choice put to Brett by the orchestrating session and relayed
to this session the same day; on the decisions question he cleared all five as
authored: **OD-1** the three-capability all-ADDED shape, **OD-2** the
no-new-check-family enforcement home, **OD-3** re-pinning defined by
reproduction, **OD-4** record repair by retention, **OD-5** the change name.
No verbatim wording of the ruling reached this session, so none is quoted — the
approver, the date, the mechanism and the option selected are stated instead,
which is what this repository's own precedent asks for and how this packet's own
admission is recorded. OD-1 through OD-5 are items 1 through 5 below, in that
order.

**NOTHING IN THE PACKET MOVES BECAUSE OF THE CLEARANCE ITSELF.** All five
decisions stand exactly as authored, so the clearance required no edit to a
requirement, a delta, a task or a design entry — the same shape openxFactory
PR #307 recorded when Brett cleared the two codex dispositions there ("the
approval required no repo edit"), and the shape both sibling packets recorded
for their own four. This record exists so the veto window is legibly CLOSED
rather than merely un-exercised: an unrecorded clearance and an unnoticed flag
look identical six weeks later. The SEPARATE rulings on Q1, Q2 and Q3 in the
same act DID move the packet, and those edits are recorded against their own
questions below.

**`.openspec.yaml`'s ORIGIN BLOCK IS DELIBERATELY NOT EDITED, and that is a
ruling-respecting choice rather than an oversight.** Its `approved_by` still
ends by saying the five decisions "are NOT covered by this authorization and are
flagged for veto in the proposal's § Orchestrator decisions" — a pointer that
now lands the reader on this clearance, which is why leaving it costs nothing.
What editing it would cost is real: `release-realization`'s "Origin retention at
archive" requires the archive gate to verify the origin declaration is UNCHANGED
from ratification and to FAIL on a mutation, making any rewrite a
contested-class act. A veto clearance is not origin provenance, so it is
recorded where the flagging lives instead.

**THE CLEARANCE COVERS EXACTLY THESE FIVE DECISIONS.** The same ruling
separately disposed all three open questions, and the two are not the same act:
this clearance CLOSED THE VETO WINDOW, while the question rulings CHANGED THE
PACKET — Q3's namespace ruling edited two requirements and three scenarios, and
Q2's ruling was executed before it was recorded. Each is recorded against its
own question below.

**HISTORY, KEPT SO THE RESOLUTION IS LEGIBLE.** The paragraph below is this
section's original preamble, unchanged. It was true when written and is now
superseded by the clearance above; it is preserved rather than erased for the
same reason the sibling packets preserve theirs.

> This packet was authored by a delegated session against Brett's instruction to
> file it. That instruction is the origin act and covers THE FILING; every
> decision below was taken by the authoring session under standing patterns and
> is flagged for reversal. Reverting any one of them is an edit to this change,
> not a new one.

1. **Four requirements across THREE capabilities, all ADDED, none MODIFIED.**
   The artifact rule and the record-repair rule go to
   `ideation-cross-reference`, which owns both the index and the immutable
   derivation evidence the two live orphans are; the landing rule goes to
   `release-realization`, which owns the archive and realization gates and
   already carries the ordering and origin-retention obligations a landing
   discharges; the enforcement goes to `doc-health`. Collisions were checked
   rather than assumed: no active change carries a delta for
   `ideation-cross-reference` or `release-realization` at all, and the two
   active `doc-health` deltas (`add-family-enumeration-check`,
   `add-nightly-dashboard-refresh`) touch no requirement this one adds.
   Rejected: one cross-cutting requirement in `document-lifecycle`. It would
   have read as a single rule but would have put a landing obligation, an
   evidence-record obligation and a verification obligation in one requirement,
   and `document-lifecycle` is additionally touched by the active
   `add-ideation-intent-plane`.

2. **Enforcement rides the existing readiness-proof surface, and adds no check
   family.** Recorded with its two rejected alternatives in `design.md` § 3.
   This is the decision the packet flagged as most likely to be vetoed, and
   Brett CLEARED IT AS AUTHORED. Its argument was: a family would owe a
   restatement of a requirement that was divergent between canon (twenty) and
   the code registry (twenty-one, `family_enumeration.py` already registered),
   with an active change holding the reconciling block. **THAT PREMISE MOVED
   WITHIN A DAY AND THE CONCLUSION HELD.**
   `add-family-enumeration-check` archived 2026-08-27, so canon and registry
   agree at twenty-one and the divergence is gone; but
   `add-modified-block-currency-check` is now active, adds the twenty-second
   family, and owes the same `MODIFIED` block at realization. A family added
   here would restate that requirement beside it and reach twenty-three, with
   canon's list decided by archive order — which is precisely what the newly
   promoted currency obligation exists to police. The volatility of the premise
   over twenty-four hours is itself the argument for the decision.

3. **Re-pinning is defined by REPRODUCTION rather than by reachability.**
   Recorded with its rejected alternatives in `design.md` § 2. The consequence
   is deliberate: a re-pin that cannot be reproduced is refused even when the
   new pin is perfectly reachable, because the #322 hand-move produced exactly
   that shape and passing it would ratify the act that caused the defect.

4. **The record-repair route is RETENTION, not re-pinning.** Recorded with its
   three rejected alternatives in `design.md` § 1. This decision is what makes
   requirement 2 exist as its own requirement rather than as a clause of
   requirement 1.

5. **The change name and the branch.** `govern-derived-pin-reachability` on
   `change/govern-derived-pin-reachability`, following `govern-openspec-corpus-membership`
   as the house's `govern-*` precedent for a rule-stating packet. The
   commission called it "the pin-governance follow-up change"; no name was
   given, so one was chosen.

## Open Questions

**ALL THREE RULED 2026-08-27**, by the same four-question multi-choice that
cleared the five decisions above, put to Brett by the orchestrating session and
relayed the same day. On each question he took the recommendation the packet
offered. No verbatim wording reached this session, so none is quoted — the
approver, the date, the mechanism, and the option selected are stated instead.
Unlike the decisions clearance, TWO OF THESE RULINGS MOVED THE PACKET, and each
entry records what moved. Each question's original text is kept unchanged below
its ruling, because a recommendation that was accepted is the argument for the
rule now in the delta.

**Q1 — where does the declared pin class live? RULED: the registry module, as
recommended.** The declaration is a registry module beside
`scripts/doc_health/families.py`, so the declaration is itself checked, mirroring
the derived-not-restated shape `add-family-enumeration-check` establishes for
exactly this problem. Recorded at `tasks.md` § 2.1 and § 2.2, which move from
"settle Q1 first" to the settled home. **NO DELTA TEXT CHANGED, deliberately**:
requirement 4 obliges a declared class and checks the declaration, and it does
not name a file path, because a promoted spec that pins an implementation path
has to be MODIFIED the next time the module moves. The ruling is recorded where
implementation decisions are recorded. AS ASKED: Requirement 4 obliges a
declared class and checks the declaration, but does not say whether the
declaration is a contract artifact under `contracts/`, a table in the promoted
`doc-health` spec, or a registry module beside `families.py`. Each has a
different failure mode: a contract artifact is schema-checkable but adds a
schema; a spec table is readable but is prose a check must parse; a registry
module is exact but is code that canon then restates. RECOMMENDATION: the
registry module, mirroring `families.py` and the derived-not-restated shape
`add-family-enumeration-check` establishes for exactly this problem.

**Q2 — do the two live orphan repairs ride this change? RULED: publish first,
independently, as recommended — AND ALREADY EXECUTED.** The orchestrating
session published both retention refs on 2026-08-27, before this packet merged
and independently of its fate. VERIFIED HERE rather than taken on report:
`git ls-remote origin 'refs/retention/*'` returns exactly two rows,
`refs/retention/pins/da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` at
`da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` and
`refs/retention/pins/f13a3b6007736292e1e157febef1ac733e534de9` at
`f13a3b6007736292e1e157febef1ac733e534de9` — each ref pointing at the very
commit its name states. `git ls-remote origin | grep -c <pin>` now returns `1`
for both pins where it returned `0` at authoring. **THE GARBAGE-COLLECTION
WINDOW IS CLOSED**, which was the whole reason the recommendation was to go
first: the two objects are now on the remote and no longer depend on one
machine's object store surviving a `gc`. **THE CONSEQUENCE FOR THIS PACKET IS
THAT ITS TWO LIVE INSTANCES ARE NOW CONFORMING RATHER THAN REPAIRED-PENDING** —
both records still carry their original pins, unedited, and both pins now
resolve through the retention namespace, which is precisely the branch of
requirement 1 that admits a retention ref. The archive gate at `tasks.md` § 4.5
is discharged by this, and § 3.2 with it. AS ASKED: The sibling packet ruled its
own equivalent question by riding (its OD-4: "splitting it would land
requirement 3 red on its own gate"), and the same logic applies here — the
verification requirement 4 proposes will report both records. Against it: the
repair for a `record` is a PUBLISHED REF, which is a remote-state act rather
than a commit, so it does not land in a pull request the way a one-line index
re-pin did, and the recoverability window makes it urgent in a way this packet's
own timeline is not. RECOMMENDATION: publish the retention refs FIRST, on their
own, before the window closes and independently of this packet's fate; let the
packet's realization prove them.

**Q3 — is a retention ref namespace owed? RULED: yes, formalize it, and it is
the namespace Q2's execution used — `refs/retention/pins/<full-sha>`.** This is
the ruling that MOVED THE MOST TEXT, and the movement is recorded rather than
folded in silently. Requirement 1 previously admitted "a retained ref the
artifact or its owning contract itself declares"; it now names the namespace and
states that a retention ref outside it does NOT satisfy the requirement, because
a ref whose name cannot be derived from the pin is not predictably reachable.
Requirement 2's retention paragraph now obliges publishing
`refs/retention/pins/<full-sha>` on the repository's own remote, with the ref
name COMPUTED from the pin rather than chosen. Requirement 4 now states the ref
set a verification consults — `main` plus that namespace, and no more. Three
scenarios moved with them: requirement 1's retained-ref scenario is renamed and
now names the namespace and refuses any other name, and requirement 2's
still-recoverable scenario names the ref the repair publishes. Requirement and
scenario counts are unchanged at four and sixteen; no requirement was added,
split, or MODIFIED. The one thing the ruling did NOT settle is retention
LIFETIME, and the delta deliberately states none: a retained commit is retained
because a committed record names it, so the ref outlives the record, and a rule
naming a duration would need a rule for what happens at its end. AS ASKED: If
retention is the repair route, somebody must decide what the ref is called and
how long it lives, and an undeclared `refs/heads/...` left lying around is its
own kind of debt. The requirement deliberately admits any declared retained ref
rather than inventing a grammar. RECOMMENDATION: decide it with Q2, because the
first two retention refs this repository publishes will set the convention
whether or not anyone declares one.

## Impact

- Affected capabilities: `ideation-cross-reference` — two ADDED requirements,
  eight scenarios; `release-realization` — one ADDED requirement, four
  scenarios; `doc-health` — one ADDED requirement, four scenarios. No
  requirement MODIFIED in any of the three.
- Affected code at realization: `scripts/doc_health/ideation_readiness.py`, a
  declared pin-class registry module beside `scripts/doc_health/families.py`
  (Q1, RULED 2026-08-27), and regressions under `tests/doc-health/`.
- Affected repository state: **DONE 2026-08-27, ahead of this packet** —
  `refs/retention/pins/da9bf3b7d0ee1d86d2d437d42a715c238dddce4b` and
  `refs/retention/pins/f13a3b6007736292e1e157febef1ac733e534de9` are published
  on `origin` and verified by `ls-remote`, each at the commit its name states.
  The superseding-record route this line originally offered as the alternative
  is not needed: the window closed with both objects retained rather than lost.
- Risk: LOW on semantics, MODERATE on process. Nothing about what counts as
  reachable is invented — requirement 1 restates git's own ancestry relation.
  The process risk is requirement 3, which puts an obligation on a landing, and
  a landing is performed by humans and merge buttons rather than by a checker;
  it is stated as an obligation with a contested-class escape rather than as a
  gate for exactly that reason.
- Sequencing: none owed. Every delta here is ADDED and no active change carries
  a version of any requirement this one adds, so this packet composes with
  `add-family-enumeration-check`, `add-nightly-dashboard-refresh` and
  `add-ideation-intent-plane` in any archive order. The deliberate non-restatement
  of "Deterministic check families" is what makes that true, and it is the
  reason decision 2 matters beyond its own merits.
