# Design: add-promotion-fidelity-check

Status: ratified
Ratified by: add-promotion-fidelity-check

The decisions this change had to take, and the measurements each rests on.
Every number below was taken against this repository's archive at
`origin/main` on 2026-08-24 (89 archived changes carrying spec deltas, 478
distinct capability/requirement pairs) before the code was written, not
after.

## D1 — A new family, not a separate checker

The check could have been a standalone `scripts/validate-*.py`, of which this
repository has 37. It is a doc-health family instead, and the reason is what a
finding needs to be worth having:

- It gets a **report section** and a **ranked-plan line** by registration
  alone, in the same schema every other finding uses, so a session working a
  report's plan sees it beside the rest rather than in a second artifact.
- It gets the **disposition mechanism** and the **regression diff** for free,
  which is the whole apparatus this class needs — the remedy is a governance
  act and the record of a deliberate non-promotion has to live somewhere the
  tooling reads.
- It gets **`--single-repo` self-gating**, so a domain factory can run the
  check over its own archive in a PR without an aggregation checkout. That is
  how a domain repository would have caught the codex gap on the PR that
  archived the change.

A standalone validator would have needed all four rebuilt, and would have been
the 38th thing a contributor has to know to run.

## D2 — Latest writer wins, and how ties are broken

**The rule.** For a (capability, requirement title) pair, the most recent
archived delta touching it is the authority and the only thing checked.

**Why it is not optional.** Measured over this repository:

| measurement | value |
| --- | --- |
| distinct (capability, requirement) pairs in archived deltas | 478 |
| pairs written by more than one archived change | 59 |
| most writers on one pair (`doc-health` / "Deterministic check families") | 10 |
| findings WITHOUT latest-writer-wins | 20 |
| findings WITH it | 2 |

The 18 suppressed are superseded text. `doc-health`'s own "Deterministic check
families" requirement was rewritten by ten ratified changes between 2026-07-09
and 2026-08-24; canon carries the tenth, which is canon being correct. A check
that reported the other nine would be reporting the corpus for working.

**The tie-break, and why it is archive-commit order.** 19 pairs are written
twice or more on their LATEST date, so the tie-break decides an authority
rather than decorating one. Three of those 19 are load-bearing — the choice
changes whether a finding fires.

The obvious rule, folder name ascending, is deterministic and needs no
history. It was MEASURED against real archive-commit order across all 19
groups and **disagreed on six of them**. It happens to agree on all three
load-bearing ones, which is a fact about today's corpus and not a rule: this
corpus has already paid once for leaving a rule resting on the observation
that nothing occupied the gap (`govern-openspec-corpus-membership`'s
`EVIDENCE_PARTS` note — "the first cut disclosed that gap and left it open on
the measurement that nothing occupied it; that was the wrong reading of a
MUST").

So the rule is the true one: the packets' archive-commit order, read from
version control, with folder-name order as the DISCLOSED fallback for a
checkout that has no history to read. The fallback is not asserted to be
harmless — `test_the_name_order_fallback_disagrees_and_is_therefore_load_bearing`
runs the same fixture both ways and asserts the two runs DISAGREE, which is
what makes the ordering rule a rule rather than a comment.

The cost is bounded: `first_commit_timestamp` is resolved lazily and memoized,
and only for the changes a tie actually involves. A full sweep would spend one
`git log` per archived packet on every run to answer a question 19 pairs ask.

**`RENAMED` is part of the same rule.** `openspec archive` applies RENAMED
before MODIFIED — the `2026-08-02-add-workbench-integrated-editor-chat` packet
says so in its own delta, quoting the abort message it measured. A rename
therefore legitimately retires a title, and without handling it,
`ideation-dashboard`'s "Staging workbench scoped view" fires against all THREE
of its earlier writers.

## D3 — The exemption is a header the corpus already carries

The commission said to detect the C5 class "however the record actually marks
it … not on an invented marker". The record marks it twice, and only one of
the two is machine-readable:

1. `docs/archive-record-discrepancies.md` C5's prose, which says the four
   capabilities "were deliberately not promoted and stay unpromoted".
2. The packet's own `proposal.md`, which carries `Status: draft` — backfilled
   on 2026-08-23 by C5's supersession addendum for exactly this reason:
   "`draft` records the honest value this folder has always supported: never
   ratified, archived by Brett's own PR #28 with `--skip-specs`, retaining the
   four spec deltas as archived design evidence rather than promoting them."

The second is the marker, and it is a good one for three reasons. It is
already governed — `govern-openspec-corpus-membership` made every archived
`proposal.md` a lifecycle-scan-set document eleven days ago, and
`fam_status_validity` already reports one carrying no status. It is read
through `corpus.parse_status`, the ONE lifecycle header reader, so this family
does not become the eighth reader of a header seven readers already disagreed
about. And it is precisely tuned rather than convenient: **88 of this
repository's 89 delta-carrying archived changes read `ratified`, and exactly
one reads `draft`.** The exemption exempts 12 would-be findings, all of them
C5's, and nothing else.

The reasoning is also honest rather than mechanical: the obligation to promote
attaches to a claim of approval. A packet that never claimed ratification never
incurred it.

**A packet with no `proposal.md`, or none with a status, is also not checked.**
That is the conservative direction and it is not a silent hole:
`fam_status_validity` already reports the missing header over the lifecycle
scan set, so the packet is reported — by the family that owns headers, once.

### D3 REVISED 2026-08-24 (Brett, task 4.1's four-question round, PR #315)

**The paragraph directly above was wrong, and measurement is what showed it.**
The question this rule asks is now inverted: archiving a packet is PRESUMED to
be ratification of its deltas, and the exemption applies only where the header
EXPLICITLY declares `draft` or a lower taxonomy standing.

The original spelling — "checked only where the status reads exactly
`ratified`" — was tuned against openxFactory's archive, where it is precisely
narrow, and it stayed narrow there. Read across the family it was a
FALSE-NEGATIVE CHANNEL with two mouths:

1. **An annotated ratification.** `corpus.STATUS_RE` captures the whole rest
   of the header line, so hermes-install's `Status: ratified (approved at
   commit 5ace969). Amendment A1 …` is not the string `ratified`. Twenty-three
   requirements went unexamined for a packet that declares its ratification as
   plainly as any in the corpus.
2. **A missing header.** Three packets — hermes-install's
   `2026-07-22-add-seed-layer-content` and medx-roottruth-install's two —
   carry no `Status:` at all, and thirty-one more requirements went with them.
   A corpus that can buy silence by omitting a header has an exemption nobody
   granted.

Two repositories therefore reported 0 findings at 0% and 57.8% coverage, and
reported it as health.

**The direction of conservatism moved with the evidence.** When the rule was
written, "not checked" looked like the safe default — a wrongly reported
delta accuses a governance act. But a wrongly reported delta is an advisory
WARNING that a `draft` header or a cited disposition retires in one line,
while an unexamined ratified delta is a governance gap that reports itself
healthy indefinitely. The second is the failure this whole family exists to
end, so the presumption belongs on the side of examining.

**The cost was measured before the ruling and re-measured on realization**
(tasks §3.10): openxFactory 2 findings before, 2 after, across 89
delta-carrying packets; +54 requirements newly examined across the family;
+0 findings anywhere. C5 stays quiet because its own header says `draft` —
which is the proof that this narrowing kept the record it was built to
implement.

**One reader, applied symmetrically.** `declared_standing` takes the header
value's leading token, strips the punctuation the corpus wraps headers in, and
returns it only if the taxonomy knows it. So an annotated `draft` declares
`draft` for exactly the reason an annotated `ratified` declares `ratified`. A
rule that read annotations only when they made a packet louder would be two
rules wearing one name. An unrecognized value returns None and the packet is
examined; the invalid header itself remains `fam_status_validity`'s finding.

## D4 — Advisory at launch, in both of its halves

**Severity.** Every finding is `warning`. `runner.main`'s gate is `{CRITICAL}`
or `{CRITICAL, ERROR}`, so a warning family publishes without failing anything.
`staged-topic-template` is the house precedent for exactly this shape — "This
family reports non-conformance and DELIBERATELY NEVER BLOCKS A GATE … Escalating
this family to ERROR needs a new ruling, not a judgement call."

**Resolution class, which is the half that is easy to lose.** The semantically
attractive label is `contested`: the remedy is a governance act. But
`report.uncited_resolutions` turns a contested finding that VANISHES between
reports into an `error` under the `uncited-resolution` family. Register this
family as contested and the nightly goes red the first time anyone actually
promotes a delta it reported — enforcement arriving through the back door, on
the very run that proves the advisory launch worked, under a family name that
does not even say what happened.

`auto-fixable` is also defensible on its merits, not merely convenient.
codexFactory PR #85 demonstrated the remedy is a byte-level application of
already-ratified text: "the packet's delta hashed identical to the archived
delta, and the requirement block extracted from canon after promotion diffs
identical to the delta's." No new judgement about CONTENT is needed. The
judgement — apply, or record a deliberate non-promotion — is the choice the
finding's action line puts in front of a reader, and a reader acts on the
action line.

**The flip is one decision, taken once.** `tasks.md` §4 carries it as an open
box, and it raises severity to `error` AND adds the `FAMILY_RESOLUTION`
contested entry together, because taking either half alone produces a
half-enforcing family nobody chose.

## D5 — The finding lands on the delta, not on the promoted spec

Both are defensible. The delta wins on three counts: it is the document that
made the claim that went unmet; its path is stable because an archived record
does not move, where a promoted spec is edited constantly; and a disposition
has to key on something that will still be there next month. The promoted spec
is named in the rule text, which is what a reader acts on and what tells them
where to go.

The consequence is that several findings can share one path — one per
unpromoted requirement in a multi-requirement delta file. That is why the
disposition vocabulary gained an optional `requirement:` key: an entry without
it disposes the whole file, which is the coarser behaviour every other
family's entry already has.

## D6 — Normalization is deliberately narrow

Titles compare after whitespace collapse and casefolding, and nothing else. A
wider rule — stripping backticks, punctuation, trailing periods — would forgive
the exact class of drift this family exists to report. The codex gap itself
carried a `tier-2`-to-`tier 2` normalization inside a scenario body; a rule
loose enough to ignore punctuation in a title is one that would have ignored
that. Casefolding survives because a title's case is a rendering choice no
reader acts on differently.

## D7 — The measurement basis, added 2026-08-24 by ruling (PR #315)

Every other family in this suite measures the aggregation checkout: openxFactory
plus each `xFactories/*` submodule at the pin the aggregation committed. That is
the right basis for almost every question doc-health asks, because the pin IS
what the aggregation currently consumes.

**It is the wrong basis for this one.** A promotion gap is a fact about a
repository's own `main`. Read through a pin, this family reports the state of
the pin — and the corpus-wide run that produced 4.1's evidence showed exactly
what that costs: coverage collapsed to 0% in three repositories, and the family
could not see the #301 gap itself while the codexFactory pin lagged behind the
repository that contained it. A check that reports "clean" about a tree nobody
is working in is worse than one that does not run, because it is believed.

So the nightly measures live `origin/main`s FOR THIS FAMILY, and every other
family keeps the pinned tree. Three properties make that safe to state:

**The narrowness is structural, not conventional.** The option is one field
(`Context.promotion_fidelity_basis`) that only `promotion_fidelity.py` and the
`runner.py` that plumbs the flag can even name; a test greps the package and
fails if a third module learns the word. And the workflow step that makes the
basis available is a `git fetch` — it updates `refs/remotes/origin/main` and
the object store, and moves no file — so the checkout every other family reads
is byte-identical to what it was. A test asserts that step contains no
`checkout`, `reset`, `merge` or `submodule update`.

**The reading is done through the ref, not through a working tree.** A
`GitRefTree` answers the same four questions `WorkingTree` does, from one
`git ls-tree -r` plus a `git show` per file. Both go through one set of rules —
the alternative, a second traversal for the second basis, is how two readers of
one archive come to disagree about what it says. The tie-break walks the SAME
ref the statements came from, because a tie decided from HEAD's history about
statements read from `origin/main` is two readers of two trees agreeing by
accident.

**The report says which basis it measured, always.** In the headline as a
non-default-configuration line, and under the family's own heading as a per
repository list — including on a clean run, because "No findings." is a verdict
and a verdict about an unnamed tree is exactly the confusion this ruling was
taken to prevent. Where a repository's live `main` cannot be read the run
measures its checkout and the note says `FELL BACK` by name: refusing to
measure it would trade a stale true positive for silence, and silence is the
failure mode the ruling exists to close.

**Where it lives.** `doc-health-reusable.yml` is owned by THIS repository and
the aggregation's `doc-health-nightly.yml` is a thin caller that passes inputs
and owns no run step — so both halves of the realization land here and no
aggregation-side edit is owed.

## What was considered and not done

- **Comparing bodies, not just titles.** A delta's requirement body and its
  scenario bullet text could be compared too. Not done: it would report
  formatting and wrapping differences as governance defects on day one, and
  the title-plus-scenario-title comparison already catches the whole
  historical class (the codex gap was four missing scenario TITLES; the
  openxFactory gap is one missing title and one missing requirement).
- **Fixing the two openxFactory findings in this change.** Applying a ratified
  delta to canon is a governance act; codexFactory PR #85 was its own change,
  and so should this be.
- **Adding row 18 to `docs/doc-health.md`'s check-family table.** That table
  stopped at twelve five families ago. Repairing it here would put unrelated
  families' output on this feature's evidence, which is the reasoning
  `scripts/doc_health/__init__.py` already records for the sectionless
  `proposal-origin` family. Recorded in `tasks.md` §5 instead.
- **Making the live basis the default** (D7). Rejected: a developer's
  `--single-repo` self-gate would then measure a tree they are not editing and
  report their own unpushed fix as a standing gap, and a fresh or shallow clone
  would silently take the fall-back path on every run. The nightly is the run
  that needs the live basis and the nightly is the run that asks for it.
- **Skipping a repository whose live `main` cannot be read** (D7). Rejected:
  it converts a stale true positive into no statement at all, and a family
  whose whole purpose is to end an unreported class must not acquire a second
  way to report nothing. The fall-back measures the checkout and says so.
- **Fetching the live mains into the checkout** — `submodule update --remote`
  or a checkout of `origin/main` per repository. Rejected: it would move every
  other family's basis with it, which is the one thing 4.1's ruling explicitly
  did not authorize. A `git fetch` plus a ref-reading tree keeps the change to
  the one family that was ruled on.
