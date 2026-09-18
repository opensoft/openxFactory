# Proposal Ratification: harden-path-escape-helpers-against-symlink-loops

Status: ratified
Kind: report
Decision date: 2026-09-18
Ratifier: Brett Heap (openxFactory repository owner)
Ratified: 2026-09-18, approximately 09:55Z by Brett Heap (openxFactory
repository owner), verbatim: *"Ratify; land when green"* — given in the
lane's terminal as a MULTIPLE-CHOICE answer to a menu lane `openxfactory-5`
(display `openXfactory-5`, session `651195c7`) offered there, over
`proposal.md` § *The decision, put for a veto* (OQ-1; `design.md` D1 through
D4), and recorded in full here. **NO GITHUB COMMENT CARRIES THIS WORD**: the
channel was the terminal, not a review thread, and this record is how the
word survives.
**THE WORD NAMES NO ALTERNATIVE LETTER, SO IT TAKES THE RECOMMENDATION ON
ALL FOUR: OQ-1 = (a).** That is the option the packet already encoded, so
**THE DELTA'S WORDING STANDS UNCHANGED AND NOTHING WAS SUBSTITUTED, RESTORED
OR DELETED.**

## 1. The word, and what it reaches

**"Ratify; land when green" IS TWO INSTRUCTIONS IN ONE ANSWER: a
ratification of OQ-1 as filed, and a standing authorization to merge once
checks are green.** It was given at approximately 2026-09-18T09:55Z and is
recorded, with that instant, on every document this ratification touches —
`proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`
(`approved_by`/`approved_on`, added beside the unmoved `proposed_by`/
`proposed_on` pair the `add-drafted-proposal-origin` (issue #318) shape
defined), the README OpenSpec Records entry, and this record.

**THE INSTANT IS RECORDED TO THE PRECISION IT WAS GIVEN AT AND NO FINER.**
The word was taken in session, not read off a timestamped comment, so it is
written "approximately 09:55Z" rather than to a minute nobody confirmed;
inventing a false precision would be inventing evidence.

**THE RATIFICATION IS APPLIED BY LEAVING THE DELTA TEXT ALONE, AND THAT IS
VERIFIED BY DIFF RATHER THAN ASSERTED.**
`git diff --stat -- openspec/changes/harden-path-escape-helpers-against-symlink-loops/specs/`
across the ratification commit is **empty (0 files)** — the two `## ADDED`
requirements over `release-realization` are ratified exactly as authored.

## 2. The decision, as put and as ruled

| OQ | `design.md` | Put | Ruled |
| --- | --- | --- | --- |
| **OQ-1** | D1 | Which capability and delta kind | **(a) — two `## ADDED` requirements over `release-realization`**, against a `## MODIFIED` block over either realization-axis title (owes `sequenced_after` on the active `add-target-release-deferred-allocation` and inherits its archive-order hold) or a new capability of its own |
| **OQ-1** | D2 | How many acts | **(a) — ONE act across all four sites in all three modules**, against three riders on three owning packets (leaves the mirror claim false in the tree between the first and the last) or fixing only the three reachable sites |
| **OQ-1** | D3 | `_registry_present`, which no tree state reaches | **(a) — widen it too, and declare its proof a test of the CLAUSE**, against leaving it and naming a successor (re-opens the mirror defect inside one module) |
| **OQ-1** | D4 | The scope of the obligation | **(a) — the containment ROLE**, against every `except OSError:` in the three modules (would absorb real defects out of reads/writes/subprocesses) or naming the four clauses literally (rots on the next line move) |

**EVERY SUB-DECISION TAKES ITS RECOMMENDED OPTION.** No requirement text was
rewritten, no delta directory was renamed, and `sequenced_after: []` still
holds as a corroborated root claim.

## 3. What this word admits, and what it does not

**ADMITTED.** The two `## ADDED` requirements on `release-realization`
exactly as authored: *A containment guard answers every resolution failure
and raises none* (six scenarios, D1/D2/D4) and *A symlink-loop proof is
built at test time and never committed* (four scenarios, D5, not itself put
for a veto). The packet's own correction of openxFactory #1074's text
stands: `_registry_present` is a CLAUSE-LEVEL, RACE-ONLY case, not a tree
state (D0.5, D3).

**NOT ADMITTED, AND NOT BY THIS WORD.**

- **Nothing reaches `openspec/specs/`.** This ratification edits no promoted
  file. Promotion happens at archive, which `tasks.md` § 5 holds behind
  merged-plus-green realization evidence and a separate word.
- **The REALIZATION (`tasks.md` § 3) is not performed here.** The word
  authorizes it to be AUTHORED, as a later pull request in this repository;
  it is not carried in this commit and no clause moves today.
- **No symlink is added to the tracked tree**, here or by anything this word
  authorizes.
- **openxFactory #1074 stays OPEN.** `code_surface` is non-empty, so the
  archive is a separate act on merged-plus-green realization evidence and a
  separate word, and the issue closes THERE, never at this landing.
- **The other ELEVEN `except OSError`-family clauses** (`tasks.md` § 6.1) and
  the wider sweep and house-helper questions (§ 6.2, § 6.3) are read,
  enumerated and left as successors; this word does not commission any of
  them.

## 4. What is owed after this word

- **§ 3 (realize) may now be authored**, as a LATER pull request under this
  lane: `except (OSError, RuntimeError):` at three clauses, `except (OSError,
  ValueError, RuntimeError):` at the fourth, one test per clause (four tests
  in three packages) built at test time under `tmp_path`, and five
  docstrings amended to name `RuntimeError`. It does not ride in this pull
  request.
- **§ 4 (verification) is taken at the realization head**, not here.
- **§ 5 (archive) stays entirely open**, held behind merged-plus-green
  realization evidence and a separate word; openxFactory #1074 closes only
  there.
- **Merge of THIS pull request is authorized by "land when green"** once its
  checks are green, as a separate act performed by whoever holds it — this
  lane refreshed the packet and does not merge it. Rule 6 (the
  landing-window protocol for a PR touching `openspec/changes/` and the
  README OpenSpec Records block) applies at landing.

## 5. Provenance of this record

Written in the ratification commit itself, by lane
`openxfactory-5` (display `openXfactory-5`). It carries `Status: ratified`
because `document-lifecycle`'s *A review record records a ratification*
governs a `review/ratification-*` file. Every path in this file is
repo-relative.
