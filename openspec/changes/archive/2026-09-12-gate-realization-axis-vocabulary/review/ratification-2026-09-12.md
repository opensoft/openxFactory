# Proposal Ratification: gate-realization-axis-vocabulary

Status: ratified
Kind: report
Decision date: 2026-09-12
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-12 by Brett Heap (openxFactory operator authority) — lane
`openxfactory-1` (display `openXfactory-1`), THREE INDEPENDENT MULTIPLE-CHOICE
RULINGS over `design.md`'s three declared veto points with the recommendation
presented first in each: **D1 verbatim *"Keep and gate"***, **D2 verbatim
*"Sweep in this PR"*** and **D3 verbatim *"Resolve against the registry that
exists"***, given in session and recorded on openxFactory PR
[#963](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5646922493)
at **2026-09-12T15:45:19Z** (comment `5646922493`). **ALL THREE ARE THE OPTIONS
THIS PACKET HAD ALREADY ENCODED, SO THE WORDING STANDS UNCHANGED AND NOTHING
WAS SUBSTITUTED, RESTORED OR DELETED.**

**THE DATE IS STATED RATHER THAN INFERRED.** The recording comment is
timestamped `2026-09-12T15:45:19Z` and carries the utterance's own time,
2026-09-12T15:45Z — one UTC minute, one UTC day. So `Decision date:`,
`approved_on`, this file's name and its sibling capture's name are all
**2026-09-12**, with no boundary to reconcile. Every timestamp in this packet is
UTC, as `proposed_on`, `created` and the commissioning word of
2026-09-11T12:08:24Z are.

## 1. The two words, and exactly what each decided

**THE COMMISSIONING WORD IS NOT AN APPROVAL AND IS NOT READ AS ONE.** Brett
Heap's word of 2026-09-11T12:08:24Z, verbatim *"land each when green, archive
both when landed, claim 955 and 956"*, commissioned the AUTHORING of this
packet under its "claim 956" clause. It named no wording, resolved no veto
point and admitted no text to canon. `.openspec.yaml`'s `origin:` block was
authored under it in the lawful unapproved shape `add-drafted-proposal-origin`
(issue #318) defined — `proposed_by` + `proposed_on`, no approval pair — and
**that block is kept byte-unmoved by this ratification**, its drafting tense
included (its `reason:` describes the unapproved state the packet was authored
in, and describing that state truthfully is what it is for). The approval pair
is an ADDITION beside it, measured in `review/verification-2026-09-12.md` § 9 as
`46 0` on `git diff --numstat`, with lines 1–94 hashing identically before and
after.

**THE RATIFYING WORD IS THE SECOND ONE**, quoted in full because it is short:

> do all as recomended

It was given in the lane's window in answer to the orchestrator's list of open
rulings, each put with its recommendation first, and recorded by the
orchestrator on this pull request at 2026-09-12T15:45:19Z with the three
rulings written out item by item. It reaches **D1, D2 and D3** — the three
decisions `design.md` declared as veto points — and takes the RECOMMENDED
option of each. It is one utterance over three independent questions, which is
why this record names all three labels and never merges them into a single
paraphrase.

## 2. D1 — RULED *"Keep and gate"*, as encoded

**TAKEN**: keep the two-value `target_release:` vocabulary exactly as
`release-realization` ratified it, and GATE it by ADDING one requirement.
**NOT TAKEN**: *"Admit none"* (amend *Realization axis declaration* to admit a
third value) and *"Rule none a synonym"* (canon reads an off-vocabulary value
on an empty code surface as `implemented`).

As encoded, and unmoved by the ruling: one `## ADDED Requirements` block,
*Realization axis vocabulary is gated*, with ten scenarios; **no `## MODIFIED`
block**, so no collision with the ACTIVE ratified `add-structured-scope-substrate`
and no `sequenced_after` hold; the house validator pair
`scripts/target_release.py` + `scripts/validate-target-release.py`; and
`scripts/target-release-register.yaml`, the CLOSED 21-entry grandfather
register whose entries may be REMOVED and never ADDED. The two alternatives
carried a `## MODIFIED` block over a title another active change already
modifies, and with it the archive-order hold; option 3 additionally did not
reach its own subject, all five active `none` carriers declaring a NON-EMPTY
`code_surface`. Both are retained in `design.md` D1 as the record of what was
put and declined, not as work owed.

**THE CLOSURE OF THE REGISTER IS PART OF WHAT WAS RULED, AND IT BOUND THIS
LANE WITHIN THE HOUR**: when the merge from `main` brought in a sixth
off-vocabulary carrier, registering it was not available and the sweep was
(§ 3 below, `design.md` D2a).

## 3. D2 — RULED *"Sweep in this PR"*, as encoded, and what it reached

**TAKEN**: the existing non-conforming spellings across the corpus are swept in
this same pull request, one value token per file, every prose gloss preserved
verbatim. **NOT TAKEN**: *"Each owning lane sweeps"* (the gate lands ADVISORY
until the last one is done — which is the state openxFactory #956 filed about)
and *"Register all 26"* (a standing exception for a defect a one-token edit
removes).

**A SWEEP'S POPULATION IS A FACT ABOUT A TREE, SO IT WAS RE-MEASURED AT THE
HEAD THE SWEEP LANDS ON** — the merge of `origin/main` `1f068646`, merge commit
`fb55c9e9`. It is **SIX** carriers, not the five `design.md` D2 was drafted
against:

| change | before | after |
| --- | --- | --- |
| add-composed-view-authoring | `none` | `implemented` |
| add-cpc-clearing-boundary | `none (no contract-bundle involvement — …` | `implemented (…` |
| add-lens-document-selection | `none` | `implemented` |
| add-substantive-review-lane | `none (no contract-bundle involvement — …` | `implemented (…` |
| register-gate-rules-council-seats | `none — no contract bundle is cut …` | `implemented — …` |
| amend-kill-switch-to-declared-test-companion | `a code surface (in codexFactory), so per …` | `implemented — a code surface (in codexFactory), so per …` |

The sixth landed on `main` with pull request #959 at 2026-09-11T17:19:09Z,
AFTER D2 was drafted against a corpus that did not contain it. Its defect is a
different one: it wrote no token at all — the declaration opens as a running
sentence, so the VALUE TOKEN is the article `a` — and the gate named exactly
that. The correction supplies no judgment, because the author's own gloss
already says what `implemented` means: *"No contract bundle is cut, nothing
under `contracts/` moves, no `contract_bundle_version` is spent, no openxFactory
CONTRACT digest set moves and NO RELEASE TAG IS OWED."* Registering it instead
was refused by D1's ruled closure. `design.md` D2a and `tasks.md` § 3.18 carry
the account, the custody check and the four regression tests the class earned.

Re-measured after the sweep: **0** active declarations outside the vocabulary
(exit 0; 41 active, 17 `implemented`, 3 a named release, 21 named by the
register). The live-corpus race is DISCLOSED and not closed: a proposal landing
on `main` before this packet merges can add a seventh, and the remedy is the
same one-token correction re-measured at that head.

## 4. D3 — RULED *"Resolve against the registry that exists"*, as encoded

**TAKEN**: a value token counts as a named release when
`contracts/releases/<token>.digests.yaml` is present in the SCANNED tree, with
the release-identifier shape `^contract-v[0-9]+(?:\.[0-9]+){1,2}$`
(`RELEASE_ID_RE`) accepted on its own — and SAID OUT LOUD in the run's output —
only where the scanned tree carries no `contracts/releases/` at all.
**NOT TAKEN**: *"Resolve literally"* against the aggregation repository, which
defines no releases and carries no tags, so `contract-v1.45` and both
`contract-v3.0` declarations would be refused on day one; and *"Accept any
release-shaped token"*, under which `contract-v<next minor>` and any invented
version number pass and the gate stops distinguishing a release from a wish.

At this ratified head the registry the gate resolves against carries **55**
digest inventories, two of them — `contract-v3.7` and `contract-v4.0` —
arriving with the same merge from `main`. That is the ruled option behaving as
ruled: the gate follows the registry rather than a frozen list. The divergence
between that registry and the promoted sentence's *"aggregation repository"* is
recorded as a successor and deliberately not repaired here (`tasks.md` § 6.2),
because repairing it means editing a promoted sentence — option 2's `MODIFIED`
block and its sequencing hold, for a wording fix.

## 5. D0 and D4 through D7 were carried and none was vetoed

Each was written out with its alternative and its cost and each was available
to be vetoed in the same ruling: **D0** the measurement taken before the
design; **D4** the code surface — a sibling validator reading the shipped
strict loader, three exit codes, and the register's home outside `contracts/`;
**D5** why an OpenSpec change and not a patch; **D6** sequencing and the
sibling search, pasted; **D7** what is measured and deliberately not taken. The
ruling named none of them and none of them moves.

## 6. What this ratification did NOT do

- **NOTHING IS PROMOTED.** This pull request edits no file under
  `openspec/specs/`. The ADDED requirement enters canon at the ARCHIVE, § 5.1.
- **NOTHING IS ARCHIVED, AND NO ISSUE IS CLOSED.** `code_surface` is NON-EMPTY,
  so under `release-realization` this packet archives on MERGED-PLUS-GREEN
  REALIZATION EVIDENCE at canon's grain — this pull request merged into `main`
  and a green `pytest-suite` run at the tree that merge carries — on its own
  later pull request and on a separate word. openxFactory
  [#956](https://github.com/opensoft/openxFactory/issues/956) closes THERE and
  at no earlier landing; `closingIssuesReferences` on this pull request is `[]`
  and stays so.
- **`tasks.md` § 5 (archive) AND § 6 (residue) STAY ENTIRELY OPEN**, § 6's
  named successors included: whether canon admits a deferred allocation as a
  third value (§ 6.1, the twelve register entries that retire on it), the
  *"aggregation repository"* wording (§ 6.2), `code_surface:` not being gated
  (§ 6.3), the archived 61 left frozen (§ 6.4), and no other estate repository
  swept or registered (§ 6.5).
- **NO REGISTER ENTRY WAS ADDED.** The register stands at 21 entries, closed.

## 7. The bench at ratification

**TEN ROUNDS, ALL COPILOT.** Rounds 1–9 were disposed before the ruling and are
recorded round by round in `design.md` D8 through D8i and `tasks.md` § 3.7–§ 3.17;
the FREEZE at head `fbe3ffac` (PR #963 comment `5636792384`, 2026-09-11T15:31Z)
recorded **25 threads, 0 unresolved**, every finding TAKEN and none refused,
and states in its own words that *"Nothing in D1/D2/D3 was reopened or
re-litigated"*. A TENTH round arrived at 2026-09-11T15:32Z, one minute after
that freeze, with four threads, and none of them reopens D1, D2 or D3 either.
TWO of the four are already answered by this ratification's own work: § 4.6's
stale `39 active / 9 declaring` capture and § 4.9's stale `200 rows` figure,
both re-measured at the merged head to `41 / 11` and `204 rows`. The other two
— a `Path.is_file()` symlink escape on the PROPOSAL discovery path, the same
class as the registry escapes rounds 7 and 9 closed, and a stale test count in
the pull-request description — are taken in the fix commit that follows this
one on this pull request, and are recorded there in `design.md` D8j and
`tasks.md` § 3.19.

**CODEX: ABSENCE, RECORDED VERBATIM.** Requested once at 2026-09-11T12:43:28Z
(PR #963 comment `5634604106`). The reply eight seconds later, comment
`5634605700`, was:

> You have reached your Codex usage limits for code reviews. You can see your
> limits in the [Codex usage dashboard](https://chatgpt.com/codex/cloud/settings/usage).
> To continue using code reviews, you can upgrade your account or add credits
> to your account and enable them for code reviews in your
> [settings](https://chatgpt.com/codex/cloud/settings/code-review).

No second request was made, at ratification or in any earlier round. Sourcery
posted its guide/summary stub only (comment `5634576211`) and no finding.

## 8. What is owed after this ratification

1. **The landing**, under the standing word *"land each when green"* — the
   orchestrator's act, not this record's.
2. **The realization evidence, then the archive** (§ 5.1): merged-plus-green at
   canon's grain, on a separate pull request and a separate word, where the
   ADDED requirement is promoted byte-for-byte into `openspec/specs/` and
   openxFactory #956 closes (§ 5.2).
3. **`tasks.md` § 4.10**, the full-suite count, whose authoritative figure is
   this pull request's own required `pytest-suite` run, and **§ 4.12**, the bot
   bench, which ticks when a review round returns with nothing left to take.
4. **§ 6's named successors**, each of which is a separate packet and a
   separate word.

The gate set re-derived on the ratified tree is
`review/verification-2026-09-12.md` (`Status: record`); later bench rounds
record their own re-runs in `tasks.md` § 3.x rather than rewriting it.

## 9. Addendum — the archive word, recorded after this ratification and appended rather than edited into it

**ADDED AT THE ARCHIVE (PR #1014), NOT PART OF THE ORIGINAL RATIFICATION
ABOVE.** § 8 above already named what remained owed: the landing, the
realization evidence, the archive, and § 6's named successors. What follows
completes that record without touching a word above it.

**THE LANDING.** This ratification pull request (#963) merged into `main` as
`68ff88b4091ece46f0ad269643aa316924aa8c65` at **2026-09-12T19:03:47Z** (LANDED
comment
[issuecomment-5648037759](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5648037759)).

**THE REALIZATION EVIDENCE.** `main`'s OWN `pytest-suite` run at that exact
tree — run
[34713047890](https://github.com/opensoft/openxFactory/actions/runs/34713047890),
`headSha` `68ff88b4091ece46f0ad269643aa316924aa8c65` (byte-identical to the
merge commit itself), conclusion **success**, created 2026-09-12T19:03:52Z,
completed 2026-09-12T19:23:11Z — a decided run at the tree the merge carries,
so no tree-equality argument is owed.

**THE ARCHIVE WORD.** Brett Heap, **2026-09-12T22:25:43Z**, verbatim
**"archive both"** (this packet and `report-stale-grandfather-dispositions`),
given in answer to the orchestrator's statement that each of the two remaining
code-surface packets requires its own separate archive word under its own
`tasks.md` § 5/§ 6, with the invitation "Say 'archive both' or name one" —
recorded on this pull request (#963) at
[issuecomment-5649094500](https://github.com/opensoft/openxFactory/pull/963#issuecomment-5649094500)
and mirrored on openxFactory
[#956](https://github.com/opensoft/openxFactory/issues/956#issuecomment-5649094591).

**THE ARCHIVE ITSELF.** Performed in
[PR #1014](https://github.com/opensoft/openxFactory/pull/1014): the ONE
`## ADDED Requirements` block (*Realization axis vocabulary is gated*)
promoted byte-for-byte into `openspec/specs/release-realization/spec.md`
(8,569 bytes, sha256 `204368c0fb73f7638c5264ba345d7814f2920e5c3e54ae0d24cee5832749d9d5`
both sides), the packet moved to
`openspec/changes/archive/2026-09-12-gate-realization-axis-vocabulary/`, and
openxFactory #956 closed by that pull request's own `Closes #956` line —
nowhere else.

**§ 4.10 AND § 4.12**, left unticked at this ratification per § 8 item 3
above, were done (the required `pytest-suite` was green at merge; the bench
froze at 36 threads, 0 unresolved) and left unticked — the same bookkeeping
defect `tasks.md` § 3.9(c) already names for § 4.9/§ 4.11 at an earlier round.
Ticked at the archive, citing the CI runs directly rather than re-deriving them.

**§ 6'S NAMED SUCCESSORS.** § 6.1 and § 6.2 name
`add-structured-scope-substrate` (ACTIVE, ratified, already cited in this
packet's own `.openspec.yaml` `related:` block and design.md D7) — re-verified
unmoved at the archive. § 6.3 had no successor named anywhere in this packet
or the corpus; openxFactory
[#1013](https://github.com/opensoft/openxFactory/issues/1013) is filed for it,
UNCLAIMED, at the archive. § 6.4 and § 6.5 owe no successor, per their own
ratified text, and none is filed for them.
