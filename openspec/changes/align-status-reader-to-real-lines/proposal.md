---
code_surface: openxFactory (a new shared line primitive in `scripts/doc_health/lines.py`; `scripts/doc_health/corpus.py` — `parse_status` and `parse_kind` scan REAL lines through it; `scripts/ideation_dashboard/round_trip.py` imports it instead of carrying its own copy; tests/doc-health/ and tests/ideation-dashboard/test_round_trip.py)
target_release: implementation_pending — the requirement lands now; the change archives only on merged code with green realization evidence, because its whole content is a reader correction
Status: draft
Ruling: 2026-08-19 by Brett Heap — in-session multiple choice, all recommended options adopted. The read-side fix owns its own change rather than riding the demote fixes, so doc-health's shared reader carries its own baseline diff.
---

# Proposal: align-status-reader-to-real-lines

## Why

`align-demote-to-round-trip-rule` closed half of a divergence and its own review
recorded the other half as still open. This is that half.

`_flip_status` — the WRITER that stamps a lifecycle status when a demote returns a
document — used `str.splitlines(keepends=True)`, which breaks not only on the three
real line endings but also on `\x0b`, `\x0c`, `\x1c`-`\x1e`, `\x85`, U+2028 and
U+2029. Two damages followed, both demonstrated: a form feed inside a `Status:` line
made the writer invent a line boundary and weld the remainder onto the new value,
and a header carrying enough exotic separators pushed a real `Status:` past the
15-line window so the flip silently did nothing. The writer now counts REAL lines
and both are closed.

**`corpus.parse_status` still counts pseudo-lines.** It scans
`text.splitlines()[:STATUS_SCAN_LINES]`, and so does `parse_kind` beside it. So the
divergence is now asymmetric in the most confusing possible direction: the demote
writes a correct `Status: staged`, and doc-health's reader can fail to see it and
report `status-validity`'s "missing status header" about a document that plainly has
one. That is a FALSE FINDING rather than corruption, which is worse for trust than a
crash — it accuses a correct document, and the operator's only recourse is to
disbelieve the checker.

A second shape is recorded in the archived change's §7.2 and is the one place the
two sides disagree about CONTENT: `Status: draft<SEP>Kind: x` with an exotic
separator. Pre-fix the writer produced `Status: stagedKind: x`, which the reader
parsed as the invalid status `'stagedKind: x'`; post-fix the writer treats the whole
real line as the header and replaces its value, so `Kind: x` goes with it and the
reader sees a valid `'staged'`. Better, and still a divergence: the reader would
have seen a `Kind:` the writer no longer believes exists.

**Measured baseline: this moves ZERO findings today.** 1079 governed markdown files
under this repository carry no exotic separator anywhere — not in a header window,
not in the body — and there is no file where the pseudo-line and real-line header
windows even differ. So the value is not a corpus cleanup. The value is that a
reader and a writer over the same documents stop disagreeing about what a line is,
before something in the corpus makes the disagreement visible.

That measurement is also the reason this is its own change rather than a rider on
`refine-demote-round-trip-mechanics`: `parse_status` sits behind sixteen
deterministic check families, so a change to it should present its own baseline diff
where a reviewer can see zero movement, not have that diff mixed into a demote fix's.

## What Changes

**One shared line primitive, in one place.** The rule for "what a line is in a
governed document" becomes a named module that both the reader and the writer
import. `round_trip.py` currently carries its own copy — correct, and the third such
implementation in this corpus after `doc_health.families` and
`web/views/outline-model.js`. This change reduces the Python side to one.

**`parse_status` and `parse_kind` count real lines** through that primitive, so the
15-line header window means fifteen lines of the document rather than fifteen
fragments of it.

## Capabilities

### Modified Capabilities

- `doc-health`: how the deterministic pass READS a governed document's lifecycle
  header — currently unspecified, so the delta is ADDED rather than MODIFIED.

## Impact

**WHERE THE PRIMITIVE LIVES, decided on the measured dependency direction rather
than on taste.** Module-level imports run `ideation_dashboard` → `doc_health` at
five call sites (`authoring.py`, `corpus_root.py`, `generator.py` twice,
`gate_console.py`). `doc_health` reaches back the other way only LAZILY, inside two
functions, each marked `# lazy: house guard`. So the clean direction is the one that
already exists, and the primitive goes in **`doc_health`** — a new
`scripts/doc_health/lines.py` — with `ideation_dashboard.round_trip` importing it.

Putting it in `ideation_dashboard` and having `corpus.py` import it at module level
would invert the only clean direction and put doc-health, the checker layer, downstream
of the dashboard runtime for a text helper. It would also make the lazy back-reference
in `derive_possibles.py` and `ideation_readiness.py` load-bearing rather than
incidental.

A dedicated `lines.py` rather than folding it into `corpus.py`: neither the reader
nor the writer owns the definition of a line, and this corpus has already paid for
one three-implementation scanning hazard. A named home is how a fourth
implementation gets prevented instead of discovered.

- **Affected capabilities:** `doc-health` (one ADDED requirement).
- **`document-lifecycle` was considered as the owner and declined.** It defines the
  `Status:` header contract — the taxonomy, the obligation to carry one — but not how
  a reader locates it. The scanning rule is the deterministic pass's own behavior, so
  it belongs with the pass.
- **The JavaScript side stays a separate implementation and that is not fixable
  here.** `web/views/outline-model.js` cannot import a Python module, so the corpus
  keeps two implementations of the fence/line rules rather than one. The existing
  three-way agreement test is what holds them together, and this change reduces what
  it has to hold from three to two.
- **Expected baseline movement: none.** The change should present a doc-health run
  identical to its baseline. A finding that MOVES is a signal to stop and explain,
  not to accept — a corpus file carrying an exotic separator would mean the
  measurement above has gone stale.
- **Not in scope:** any widening of `STATUS_SCAN_LINES` itself, and any change to
  what a valid status value is. This is about counting lines, not about the taxonomy.
