# Ratification — 2026-09-10

Status: record

## Decision

RATIFIED by Brett Heap.

## Authority, and that it is first-hand

Brett Heap, repository owner, ruled **first-hand, in session**, to lane
`codexfactory-1` (session window `codeXfactory-1`), at **2026-09-10T11:31:31Z**
— the timestamp of the last `### RULING —` heading in that lane's own
session-handoff record, `session-handoff-2026-09-05-lane-codeXfactory-1.md`
(xFactory aggregation repo). Verbatim:

> **"ratify 886, 0.2 as narrowed, 0.3 pure moves"**

— over head **`f36d2bc2`**, on openxFactory draft PR
[#886](https://github.com/opensoft/openxFactory/pull/886) (branch
`change/accept-sequenced-after-header-line`, change
`accept-sequenced-after-header-line`).

The hearing was first-hand and was recorded contemporaneously by the same
lane, in the same session, in the handoff document cited above. This record
is authored by that lane's writer subagent FROM the lane's own brief and that
contemporaneous record — not from a second human's retelling, and not from
any agent's own paraphrase of what Brett Heap said. The verbatim quoted above
is copied byte-for-byte from the handoff heading and from the writer's brief,
which agree.

## The earlier ruling, and why it was not this one

**Brett Heap, first-hand, in session, 2026-09-10 ~02:10Z**, verbatim **"do
door b"**, on codexFactory issue
[#268](https://github.com/codeXfactory/codexFactory/issues/268) — choosing
between two named alternatives: (a) fence the whole codexFactory corpus, or
(b) teach the openxFactory reader the unfenced header form. **That ruling
authorized the AUTHORING and settled the VEHICLE; it ratified no text.**
`proposal.md`, `design.md` and `.openspec.yaml`'s `origin.approved_by` have
said so throughout, and `tasks.md` Group 0 was left open to hold the gap.
This record closes it. Two words, one operator, ~9h21m apart, two
different decisions — the first chose the door, the second ratifies the
packet built behind it — and both are recorded because both happened.

## The text ratified

The packet **at head `f36d2bc2`**, i.e. every commit on
`change/accept-sequenced-after-header-line` as of this ratification:

1. `498ae2cb` — Propose `accept-sequenced-after-header-line`: a lifecycle
   header line declares what the fenced key declares.
2. `d41cf88b` — Realize it: the reader learns the header-line site, and no
   proposal byte moves.
3. `f78a1e83` — Index `accept-sequenced-after-header-line` in the README
   OpenSpec Records block.
4. `12f9b9f6` — Move this change's own row in the per-change sweep ledger.
5. `f36d2bc2` — Take Copilot's finding: an opened-but-unclosed fence declares
   nothing on EITHER path.

**In substance, what is ratified:**

- **Two ADDED requirements on `release-realization`, seven scenarios, no
  MODIFIED block** (`specs/release-realization/spec.md`): "Equivalent
  declaration sites for the ordered-delta parent declaration" (four
  scenarios) and "One parent declaration across both sites, and its
  retention" (three scenarios).
- **The reader realization, in this same pull request**:
  `scripts/frontmatter_strict.py` (`split_real_lines`, `fence_span`,
  `HEADER_WINDOW_LINES = 15`, `read_header_line`, the `NO_HEADER_LINE`
  sentinel) and `scripts/sequenced_after.py` (`read_header_line`,
  `read_declaration` routed through both sites), proved by
  `tests/sequenced_after/test_header_line.py`.
- **The README "OpenSpec Records" active-changes row** for
  `accept-sequenced-after-header-line` — moved DRAFT → RATIFIED by this same
  commit (house style, alongside this record).
- **The BEFORE/AFTER measurement** in `proposal.md` § The measurement:
  `declaring` 0 → 3 over codexFactory main `2ade133`, deepest resolved chain
  0 → 2 hops; all three admitted carriers RETAINED against their own ratified
  heads.

Nothing else moves in the ratifying commit. No contract byte, no realization
byte, no digest, no test.

## The two dispositions ruled at this sitting

Both given in the same word, **"ratify 886, 0.2 as narrowed, 0.3 pure
moves"**, 2026-09-10T11:31:31Z.

### 0.2 — the narrowing: RULED AS NARROWED

`add-sequenced-after-substrate`'s ADDED requirement "Machine-readable
ordered-delta parent declaration" holds that "a prose `Sequenced-after:`
header … SHALL NOT constitute a machine-readable parent declaration."
`proposal.md` § The ratified sentence this change narrows asked that this
sentence be read as narrowed to that legacy PROSE spelling alone, leaving
room for a DIFFERENT, validated construct to declare.

**Ruled: AS NARROWED, exactly the reading the packet proposed.** The
substrate's sentence stands — the legacy free-text `Sequenced-after:` header
(three archived openxFactory proposals carry it, prose after the ids) still
declares NOTHING, refused by name and by test, unchanged. Narrowed onto it:
the STRICT, schema-validated `sequenced_after:` header line — the field's own
name at column 0, inside the bounded fifteen-line lifecycle header window,
loaded by the same strict loader under the same sequence shape and entry
grammar as the front-matter form — DOES declare, equivalently to the
front-matter key. Task 0.2 is ticked on this word.

### 0.3 — OQ-H1, the five carriers beyond the window: RULED PURE LINE MOVES

Five of codexFactory's eight `sequenced_after:` header-line carriers sit at
real lines 20, 24, 33, 36 and 38 — beyond the fifteen-line window this change
admits. `design.md` recommended LEAVE THE BOUND (do not widen the window to
fit five documents) and left the remedy to codexFactory's own act.

**Ruled: LEAVE THE BOUND, and the remedy is PURE LINE MOVES.** The five
carriers are resolved by moving their existing `sequenced_after:` line into
the window — the codexFactory **#323** shape: pre-image and post-image are
the SAME MULTISET OF LINES, no text change, no fencing. This is codexFactory's
own act, not this pull request's: it registers at the archive-retention gate
as a contested-class mutation on each ratified carrier (per this packet's own
ADDED requirement, "reading a new site licenses no writing into it"), needing
the explicit recorded disposition that a pure line move is honest about
owing. **Successor: task 4.3** (`openspec/changes/accept-sequenced-after-header-line/tasks.md`
§ Group 4), owner lane `codeXfactory-1` in codexFactory, undertaken AFTER the
re-vendor and pin advance at task 4.1. Task 0.3 is ticked on this word; task
4.3 is NOT ticked by this record — it is successor work, unstarted.

## 0.4 and 0.5 — ratified as they stand, not separately ruled

The word **"ratify 886, 0.2 as narrowed, 0.3 pure moves"** names 0.2 and 0.3
by number and gives each its own disposition. It does not name 0.4 (OQ-H2:
`scope_globs:` stays untaught the header-line form) or 0.5 (authoring
decisions H-1 … H-7) individually, and **no separate ruling for either is
invented here.** "Ratify 886" ratifies the packet at head `f36d2bc2` as a
whole, including the two open questions and seven decisions the packet
itself already resolved with a stated recommendation and no dissent recorded
against them. **0.4 and 0.5 are therefore ratified AS THE PACKET STATES
THEM** — `design.md` § Open questions and § Decisions, `proposal.md`'s
matching text — under the same word, at the same sitting, and tasks.md marks
each with a one-line note to that effect rather than a tick, because neither
box asked a question the word answered by name.

## What ratification changes, and what it does not

**CHANGES:** `proposal.md`'s `Status:` header (`draft` → `ratified`) and its
new `Ratified:` citation line; `tasks.md`'s Group 0 lead paragraph and the
ticks on 0.1, 0.2, 0.3 and 0.6, each with a dated annotation quoting the
word; the one-line notes on 0.4 and 0.5; and the README "OpenSpec Records"
row's status text (DRAFT → RATIFIED). `design.md` and `.openspec.yaml` carry
no `Status:` header in this packet and are untouched — there is nothing on
either to flip.

**DOES NOT CHANGE:** anything normative. The two ADDED requirements in
`release-realization` are ratified **as written**, with no requirement text,
scenario, or spec-delta byte moving by this act. `.openspec.yaml` and the
realization code (`scripts/frontmatter_strict.py`, `scripts/sequenced_after.py`,
`tests/sequenced_after/test_header_line.py`) are untouched by this act.
Group 4 (codexFactory re-vendor and pin advance, the pure-line-move
disposition, other consumers' re-pins, the eventual archive) remains
UNTICKED and owed, exactly as `tasks.md` already declared successor work.

## What this ratification covers, as reviewed

The packet as it stands at head `f36d2bc2`: authored and realized in one
pull request per this repository's `release-realization` practice for a
reader-only code surface, 10 of 10 required checks green
(SonarCloud, `clearing-dispatch-gate`, `lane-line`, `merge-master-approval`,
`openreposhape-pin`, `openspec-cli-pin`, `pytest-suite`, `release-tag-gate`,
`signed-execution-chain-gate`, `wallet-validation`), including a live Copilot
review round that found a real defect (an opened-but-unclosed leading fence)
fixed fail-closed with its own regression test in the ratified head's last
commit.

## Limits

**This record performs no merge.** It ratifies one packet's text at one head.
It does not merge openxFactory PR #886, does not mark it ready for review by
itself (a separate, non-commit act performed alongside this record, done on
the strength of this ratification), does not advance any consuming
repository's pin, does not perform the codexFactory pure-line-move
disposition (task 4.3), and does not close codexFactory issue #268. A merge
follows on a **SEPARATE word** — this repository's Rule 6 landing-window
protocol applies, because this change touches `openspec/changes/`.
