---
code_surface: openxFactory (a shared line primitive in `scripts/doc_health/lines.py`; the DETERMINISTIC PASS and the dashboard readers of a governed document's lifecycle header scan real lines through it — this is the boundary the delta itself draws (its requirement is titled "The deterministic pass reads a document's lifecycle header by real lines"; the purpose clause is about what THE PASS reports), not an unqualified claim over every text-scanner in the corpus that happens to touch a `Status:` line; `tasks.md` §7 records the readers this scope does not reach, and why — `scripts/doc_health/corpus.py` (`parse_status`, `parse_kind`), `scripts/doc_health/families.py` (`_header_line`, `_scan_lines`), `scripts/doc_health/inventory.py` (`_header_value`), `scripts/doc_health/organizer_dispatch.py` (`_header_value`), `scripts/doc_health/ideation_readiness.py` (`_parse_header`), `scripts/ideation_dashboard/doxbench_packet.py` (`lifecycle_status`), `scripts/ideation_dashboard/authoring.py` (`missing_required_headers`), `scripts/ideation_dashboard/generator.py` (`_header_value`), `scripts/ideation_dashboard/completeness.py` (`_Prepared.lines`); its standalone twin `scripts/bootstrap-ideation-cross-reference.py` (`parse_header`), converted alongside it and pinned to agree by a companion test; `scripts/ideation_dashboard/round_trip.py` imports the primitive instead of carrying its own copy; tests/doc-health/ and tests/ideation-dashboard/test_round_trip.py)
target_release: implemented — merged on the openxFactory main line as PR #222 (merged 2026-08-20T01:24:14Z, rebase-merge; the branch's commits landed on main as `e6e3ae5`, `1644d86`, `175e972`, `42cc321`, `50bfee2`, `c379a09`) and green there, re-verified at `7312c25` rather than taken from the PR run: `openspec validate --all --strict` 64/64 exit 0, `tests/doc-health` 691 items with no genuine failure, `tests/ideation-dashboard` + `tests/proposal-support` 3729 passed / 14 skipped exit 0. No contract bundle was cut — the surface is code-only. Authored as `implementation_pending — the requirement lands now; the change archives only on merged code with green realization evidence, because its whole content is a reader correction`, and that merge-plus-green condition is what PR #222 discharged; rewritten 2026-08-22 by `archive-register-rulings` off this change's own tasks.md §6.2 and banner (register C1)
Status: ratified
Ratified: 2026-08-19 by Brett Heap — in-session, verbatim: "merge and ratify both", after reading the drafted proposal on PR #218. Same-day scope ruling (in-session multiple choice, recommended option adopted): the read-side fix owns its own change rather than riding the demote fixes, so doc-health's shared reader carries its own baseline diff. A second same-day scope ruling (in-session multiple choice, recommended option adopted, 2026-08-19), made after an adversarial review of this change's realization returned FIX-FIRST over a spec contradiction the review surfaced: the delta's every-reader clause governs over the narrower code_surface enumeration above's first draft; all six remaining pseudo-line readers convert in this change, on a measured zero baseline cost (1227 files, 0 movement). A focused re-verify of that realization (2026-08-19) returned FIX-FIRST once more over four mechanical items (no new ruling needed — the fourth, `completeness.py`, falls under the already-ruled wide scope): the shared primitive now also covers `completeness.py`'s header read, a coverage gap in four of the six converted readers' tests is closed, a stale comment about a JavaScript-side implementation detail is corrected, and three prose spots overclaiming the Python line-split side was fully unified are softened to name `families._template_gaps` as a deliberately deferred exception (tasks.md §7.2). A second focused re-verify (2026-08-19), running the sweep method `corpus.py`'s own comment now prescribes (bare `splitlines()` over document text, not just the `[:N]`-windowed idiom), found one more true survivor — `doc_health.ideation_readiness._parse_header` (finding F5, also under the already-ruled wide scope) and its standalone twin `scripts/bootstrap-ideation-cross-reference.py`'s `parse_header`, both converted — plus a mis-pointing docstring on an unconverted copy of the pre-conversion `families._scan_lines` (finding F6, `doc_health.ideation_routing._scan_lines`, recorded beside `_template_gaps` in tasks.md §7 rather than converted, since it is not a lifecycle-header reader either) and a ruled-out borderline case (`families._staged_exit_changes`, reasoning recorded in tasks.md §2c.3). The prose is corrected again: `_template_gaps` and `ideation_routing._scan_lines` are now named together as the deliberately deferred exceptions, plural, not "the one."
---

# Proposal: align-status-reader-to-real-lines

> **REALIZED AND ARCHIVED 2026-08-21.** The code is merged on the implemented
> target as PR #222 (merged 2026-08-20T01:24:14Z, rebase-merge; the branch's
> commits landed on main as `e6e3ae5`, `1644d86`, `175e972`, `42cc321`,
> `50bfee2`, `c379a09`) and green there: `openspec validate --all --strict`
> 64/64 exit 0, `tests/doc-health` 691 items with no genuine failure,
> `tests/ideation-dashboard` + `tests/proposal-support` 3729 passed / 14 skipped
> / exit 0. Task 5.3's own success criterion — a doc-health report identical to
> its baseline, because a moved finding would mean the zero-exotic-separator
> measurement had gone stale — was discharged on the branch and confirmed
> byte-identical across every branch tip by the adversarial review, recorded there
> rather than re-derived here. `scripts/doc_health/lines.py`
> exists, and every reader named in `code_surface:` above —
> `corpus.parse_status`/`parse_kind`, `families._header_line`/`_scan_lines`,
> `inventory._header_value`, `organizer_dispatch._header_value`,
> `ideation_readiness._parse_header`, `doxbench_packet.lifecycle_status`,
> `authoring.missing_required_headers`, `generator._header_value`, and
> `completeness._Prepared.lines` — scans real lines through it, as does its
> standalone twin `bootstrap-ideation-cross-reference.py`'s `parse_header`;
> `round_trip.py` imports the primitive rather than carrying its own copy. Task
> detail, the gate evidence, and the readers this change's boundary deliberately
> does not reach are in `tasks.md`.
>
> This block REPLACED the release-realization approved-but-unrealized banner
> rather than carrying it through the rename, following
> `align-demote-to-round-trip-rule` (archived 2026-08-19), which established that
> precedent for the same reason: archiving a record whose first paragraph says the
> code is unmerged would state something false about a realized change.

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

**Re-measured at the wide ruling (2026-08-19).** The adversarial review of this
change's first (narrow) realization re-ran the same zero-exotic-separator
measurement across the full aggregation corpus at that moment — 1227 governed
files, still zero exotic separators, zero window differences, zero value changes
— to confirm the WIDE conversion (every reader, not just `corpus.parse_status`/
`parse_kind`) costs nothing either. The count differs from the figure above
because it is a later count of a corpus that grows over time, not a
re-measurement disagreeing with the first; both say the same thing about their
own moment: zero movement.

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
