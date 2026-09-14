# Ratification: disposition-codexfactory-regular-pr-council-clearance-archive

Status: ratified
Kind: report
Decision date: 2026-09-12
Ratifier: Brett Heap (openxFactory convener)
Ratified: 2026-09-12 by Brett Heap (openxFactory convener) — TWO WORDS, twenty-two minutes apart: "ratified_by — ratify the entries as encoded" (03:04:29.167Z, the two pin ENTRIES; recorded at https://github.com/opensoft/openxFactory/issues/745#issuecomment-5643056862) and "ratify the openxFactory disposition change when it's up" (03:26:21.850Z, THIS PACKET, bare and conditional; recorded on the estate's lane registry, opensoft/brett-wip commit 1c27a188bb772c69b15d9acb94821b6e8122a1ab, lanes/LANES.md, row provenance-autonomous-merge)

## Decision

**RATIFIED by Brett Heap — in two acts, which this record keeps apart because
they cover different things and were given at different moments.**

* **The two new `contracts/openspec-cli-pin.yaml` disposition entries** are
  ratified **as encoded**, by word one.
* **This packet — `proposal.md`, `design.md`, `tasks.md` and this record** — is
  ratified **as disclosed**, by word two, whose condition was satisfied when the
  DRAFT pull request was created.

**THE MERGE IS NEITHER.** The pull request stays DRAFT and lands under
lane-collision Rule 6, on the orchestrator's own act.

---

## Word one — the ENTRIES

Brett Heap's instruction, verbatim: **"ratified_by — ratify the entries as
encoded"** — given **2026-09-12T03:04:29.167Z**, first-hand, in session, to lane
`provenance-autonomous-merge` (session `codeXfactory-3`), as a **selection in a
multiple-choice round** rather than a typed sentence. The label above is the
option text, quoted exactly; the minute is recorded to the millisecond because
the lane's registry row carries it that way
(`~/projects/xFactory/LANES.md`, row `provenance-autonomous-merge`, entry
`WORDS 2026-09-12T03:04:29.167Z`).

**THE QUESTION IT ANSWERS WAS THE AUTHORITY SPELLING.** This pin admits two, and
they are not the same claim: `ratified_by:` is a convener's act, `recorded_by:`
the weaker claim a lane may make where a human ruling is RECORDED rather than
given (`scripts/validate-openspec-cli-pin.py`,
`DISPOSITION_AUTHORITY = ("ratified_by", "recorded_by")`). The draft carried
**`recorded_by:`**, on the ground that Brett's earlier ordering ruling — *"This
change first"*, codexFactory
`hermes/domain/review-councils/records/2026-09-11-gate-rules-provenance-axis-declaration.md:656-659` —
is a ruling about WHICH PACKET RE-DERIVES WHEN, whose own § 8 says on its face
that it is *"recorded for provenance and NOT disposed by this section"*. That
reading was put to him with the alternative, and **the word supersedes it**:
`ratified_by:` is what stands, and the entries are ratified as encoded.

**What word one covers**

* **The FOURTH and FIFTH `repo: codexFactory` entries** in
  `contracts/openspec-cli-pin.yaml` —
  `item: extend-merge-master-envelope-to-floor-bot-lanes` and
  `item: relocate-review-authority-floor`, both
  `path: merge-master-approval/spec.md`, both `level: ERROR` — accepting one
  ERROR-level finding each by its WHOLE message text, with eight and nine
  citations, a `why:` stating that canon moved under a still-active delta by a
  ruled ordering, and a `retires_when:` naming the sibling's re-derivation or its
  archive plus the live second staleness condition on codexFactory `main`.
* **Their text AS ENCODED** in this packet's diff, which is what *"as encoded"*
  names.

**What word one does NOT cover.** ~~It is not a ratification of this packet's own
documents; `proposal.md`, `design.md` and `tasks.md` carry `Status: draft`.~~ —
**STRUCK, NOT DELETED.** That was true and correct for the twenty-two minutes
between the two words and for the eleven hours this packet sat uncommitted after
them. Word two is the upgrade this record's earlier revision explicitly named as
costing "one further word and one line per document"; it arrived, and the strike
records that the narrower reading was held rather than skipped.

**IT REMAINS TRUE THAT WORD ONE IS NOT THE DELETION'S AUTHORITY.** The deletion
of the `add-regular-pr-council-clearance / merge-master-approval/spec.md` entry
needs no ruling: the pinned verifier REFUSES `pin-disposition-stale` until it is
gone and prints the remedy itself, and the entry's own `retires_when:` named this
day in these words. A human word is what ADDS an exception; the tool is what
removes one.

---

## Word two — the PACKET

Brett Heap's instruction, verbatim: **"ratify the openxFactory disposition
change when it's up"** — given **2026-09-12T03:26:21.850Z**, first-hand, in
session, to lane `provenance-autonomous-merge`.

**WHERE IT IS RECORDED, AND WHY THAT MATTERS HERE.** The authoring session was
interrupted (the Claude Code process exited at approximately 03:45Z) before this
packet was ever committed, so the word outlived the session that received it.
The estate's own machinery is what carried it: the lane-collision protocol's
registry (Rule 4 / Amendment 2). It stands at **`opensoft/brett-wip` commit
`1c27a188bb772c69b15d9acb94821b6e8122a1ab`** (committed 2026-09-11 23:26:24
-0400 = 2026-09-12T03:26:24Z, three seconds after the word), file
`lanes/LANES.md`, row `provenance-autonomous-merge`, and independently in the
lane handoff at
`~/session-prompts/handoff-2026-08-28-provenance-program.md:1035`. Both records
carry the same UTC and the same verbatim text. **This encode is taken from those
records and cites them**, rather than from any relay.

**IT IS BARE.** It answers no question stated in its own text — no option label,
no fork, no A/B. A bare word ratifies what is in front of it and resolves
nothing it does not name.

**IT IS CONDITIONAL, and the condition is named in the word itself.** *"when
it's up"* — the DRAFT PULL REQUEST must exist. It did not when the word was
given. **The condition was satisfied at PR
[#1004](https://github.com/opensoft/openxFactory/pull/1004)'s creation,
2026-09-12T14:57:26Z**, over first commit `a77b57112f3d481814edef92069d1ee6acc2cda4`.
That is why the ratification is a **SECOND commit on the same branch** rather
than a rewrite of the first: the packet was genuinely `draft` when it was
written and pushed, and genuinely `ratified` afterwards, and the history says so.

### RATIFIED AS DISCLOSED

A bare word resolves nothing it does not name, so **every position this packet
states is ratified AS IT STANDS**, and each stated open item lands at the
default the packet recommends and remains **FLAGGED rather than resolved**:

| disclosed item | where | lands at | status |
| --- | --- | --- | --- |
| codexFactory's openxFactory pin advance | `tasks.md` 6.1 | lane `codeXfactory-1` carries it, sequenced after their #435 → #433, never before #434 | **open** |
| codexFactory PR #434's own `validate` going green | `tasks.md` 6.2 | a codexFactory verdict; this packet removes one reason and claims nothing about the others | **open** |
| the two sibling re-derivations | `tasks.md` 6.3 | each packet's own act under *"This change first"*; each retires its entry here | **open** |
| the upstream watch, `Fission-AI/OpenSpec#1793` | `tasks.md` 6.5 | still filed, still not fixed; reaches the four marker-blindness entries and NEITHER new one | **open** |
| no spec delta, declared | `.openspec.yaml` `skip_specs: true`, `design.md` § 3 | stands as written | ratified as stated |
| the authority SPELLING left unpinned per entry in the tests | `design.md` § 4 | stands as written | ratified as stated |
| the 2026-09-05 pin comment block left UNEDITED | `design.md` § 5 | stands as written | ratified as stated |

**Nothing in `tasks.md` § 6 is ticked by this word except 6.6, which records the
word itself.**

---

## Ruled in the same exchange, recorded here for provenance

* **The codexFactory pin advance is lane `codeXfactory-1`'s** — verbatim
  *"codeXfactory-1 carries it"*, 2026-09-12T03:04:29.167Z — sequenced after that
  lane's **#435 → #433**, and codexFactory PR **#434** lands **together with or
  after** the advance, never before it. The measured reason is
  `evidence/codexfactory-regular-pr-council-clearance-archive-2026-09-11.md` § 5.
