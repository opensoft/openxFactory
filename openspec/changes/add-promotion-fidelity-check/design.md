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
