# Contract: the reserved-marker parser

**Module**: `scripts/doc_health/modified_block_currency.py`
**Realizes**: FR-015 – FR-021; `dh:112-199` (the marker, its two forms, the
anchor, the fence rule, the destination exemption, the suppression rules, and
why the existing dated-note convention must NOT be reused).

The marker is the author's only instrument for a deliberate deletion. It is
recognized by FORM and never by prose, because the corpus's five existing dated
notes all record RESTORATIONS — one of them naming seven scenario titles in
backticks as restored — so a prose rule would read a faithful restatement of
`doc-health`'s own "Deterministic check families" as declaring seven deletions.

---

## The two forms, verbatim from the delta (`dh:187-190`)

```text
**Removed from canon by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`; ``an adapter that reaches a hosted provider SHALL obtain its credential through the `openxFactory` broker lane`` — the affordance is now tile-bound and the credential clause moved to its own requirement
**Merged into `Tile-bound gate verbs hide on a composed view` by add-example-change (2026-08-27):** `Gate verbs hide on a composed view`
```

Note what the second line proves: **a marker with no reason is still a
marker.**

Note also where those two lines LIVE in the delta: inside a fenced code block.
`fenced_regions` (see [unit-derivation.md](./unit-derivation.md)) drops them
before `parse_marker` ever sees them — otherwise the requirement that DEFINES
the marker would parse two complete markers of its own and declare two of its
own units removed. Ruled 2026-08-27; a `[TEST]` case uses these exact two lines.

---

## `extract_code_spans(text: str) -> list[tuple[int, int, str]]`

Scan left to right for CommonMark code spans; return `(start, end, content)`
for each, in order. A run of N backticks opens; the closer is the next run of
EXACTLY N. One leading and one trailing space are stripped from the content
where BOTH are present (CommonMark). An unterminated run yields nothing.

| in | contents |
| --- | --- |
| `` `a`; `b` `` | `["a", "b"]` |
| ``` ``an `openxFactory` clause`` ``` | ``["an `openxFactory` clause"]`` — the longer fence survives whole |
| `` ` `x` ` `` | `["x"]` (one space each side stripped) |
| `` `unclosed `` | `[]` |

**Forbidden**: a non-greedy `` `([^`]*)` `` regex. It truncates at the first
inner backtick and would make the marker name a fragment that is not a unit —
the defect `dh:135-142` exists to prevent, on a corpus where roughly a third of
body units and a sixth of bullets contain a backtick.

---

## `parse_marker(paragraph: str) -> Marker | None`

**Step 1 — normalize.** `p = normalize(paragraph)`. A marker wrapped across
several lines is therefore one marker (`dh:113-116`).

**Step 2 — anchor.** `p` must MATCH one of these at position 0, complete:

```text
^\*\*Removed from canon by (?P<id>[a-z0-9][a-z0-9-]*) \((?P<date>\d{4}-\d{2}-\d{2})\):\*\*
^\*\*Merged into (?P<dest>`+[^`]...`+) by (?P<id>[a-z0-9][a-z0-9-]*) \((?P<date>\d{4}-\d{2}-\d{2})\):\*\*
```

(The `dest` group is resolved by `extract_code_spans` over the bold run rather
than by a nested backtick regex, so a destination containing a backtick is
handled by the same fence rule as a name.)

Anything else returns `None` — including a paragraph that merely QUOTES the
form, because a quoted template carries `<change-id>` and `<YYYY-MM-DD>`
placeholders, not a real id and a real date. This is the anchor `dh:125-133`
calls load-bearing: this requirement's own text and `document-lifecycle`'s both
print the templates in prose that promotes into canon, and a looser test would
exempt them from carriage — "the check quietly declining to check the
paragraphs that define it".

`<id>` is matched as a change-id TOKEN, not resolved against the tree (R7): a
marker promotes into canon and must keep parsing after the change that wrote it
archives.

**Step 3 — names.** `extract_code_spans` over the remainder AFTER the closing
`:**`, in order, normalized. For `Merged into`, the destination span sits INSIDE
the bold prefix and is therefore never in this list (`dh:148-151` — otherwise
every valid merge marker reports itself).

**Step 4 — reason.** Take the text after the LAST name span. If it begins with
` — ` (space, em dash, space), the reason is the rest; otherwise the reason is
`None`. Never split on `;` or `-` (`dh:142-146`).

**Return**: a `Marker`, or `None`.

| paragraph | result |
| --- | --- |
| `**Removed from canon by add-x (2026-08-27):** `A`; `B` — because` | `removed`, names `[A, B]`, reason `because` |
| ``**Merged into `New` by add-x (2026-08-27):** `Old` `` | `merged`, dest `New`, names `[Old]`, reason `None` |
| `**Removed from canon by <change-id> (<YYYY-MM-DD>):** …` | `None` — a quoted template |
| `**Removed from canon by add-x (27-08-2026):** `A`` | `None` — not an ISO date |
| `**Removed from canon by add-x (2026-08-27)** `A`` | `None` — no closing colon |
| `Removed from canon by add-x (2026-08-27): `A`` | `None` — no bold run |
| `**CORRECTED 2026-08-25 — seven scenarios restored: `A` … **` | `None` — a dated note, and it declares NOTHING |

---

## `suppression(markers, canon_units, block_units) -> tuple[set[tuple[str, str]], list[Marker]]`

ONE function, TWO returns from ONE pass — `(suppressed, defective)` — because
the same per-name resolution answers both questions. **There is no separate
`marker_defects` function; an earlier draft of this contract named one and the
implementation review caught it.**

For each `Marker`, for each name:

1. Find the canon units whose `key` equals the name (any kind).
2. If none → nothing suppressed, nothing reported (R10; recorded as a
   deliberate non-obligation).
3. If the block CARRIES that unit (same kind, same key) → the marker goes into
   the `defective` list (FR-018: "a declaration that does not describe the
   block is a declaration no reader can rely on"). Nothing is suppressed by
   THAT NAME — see the per-name rule below.
4. Otherwise → `(kind, key)` joins the suppressed set.

Then the scenario-title extension (FR-019/020), applied ONLY where
`form == "removed"`:

- Let `new_titles` = block `scenario-title` keys that canon does not carry.
- If `new_titles` is EMPTY and a name resolved to an absent canon
  `scenario-title` T, then every canon `scenario-bullet` with `scenario == T` is
  also suppressed — **except** one that appears as a bullet anywhere in the
  block, which is carried and reported nowhere either way.
- If `new_titles` is NON-EMPTY, the extension does not apply at all: the shape
  is a retitle whatever the marker calls it, and `Merged into` is the author's
  instrument. Each such bullet must be carried somewhere in the block or named
  individually in a `Removed from canon` marker.

**The combination case is the one that matters** and it is why the two rules
are evaluated together rather than in separate branches: a `Removed from canon`
marker naming the old title PLUS a replacement scenario carrying two of the old
scenario's four bullets must report the other two. Suppressing them would let a
retitle relabelled as a removal drop obligations with nothing reported.

**Postconditions**

- Suppression is keyed on `(kind, key)`, so a marker can never silence a unit
  of a different kind that happens to share text.
- The `defective` list contains each offending marker at most once.
- **A MARKER IS VOIDED PER NAME, NOT WHOLLY (ruled 2026-08-27).** A marker
  naming three units, one of which the block still carries, is reported AND
  still suppresses the two that are genuinely absent. Voiding the whole marker
  would turn one wrong name into a cascade: the two sound declarations would be
  discarded and their units would surface as fresh carriage findings, so the
  author would see three problems where they made one mistake, and two rows they
  had already deliberated would come back. `dh:153-156` supports the per-name
  reading directly — suppression is defined per unit ("only the units it names
  AND that are in fact absent") while the reporting rule is about the marker
  rather than about its other names.
- A `Marker` never appears in `canon_units` or `block_units` (FR-007/021), so a
  promoted marker is not text a later block must restate.

---

## `_arm_marker_defects(repo, block, defective) -> list[Finding]`

**The emitter, added by ruling 2026-08-27.** `suppression`'s second return had no consumer in
the first cut of this plan — a producer for a requirement nothing would report,
which is how `dh:153-156`'s "SHALL itself be reported" ends up realized in a
docstring instead of in a run.

One finding per offending marker, at `_LEDGER_SEVERITY` (`info`, never `error`,
so the advisory launch holds in both halves), naming the marker's change id and
date and the unit it wrongly names:

```text
active MODIFIED block for '<title>' carries a `Removed from canon by
<change-id> (<date>)` marker naming `<unit>`, which the block still
restates — a declaration that does not describe the block
```

**It is a FOURTH finding class, not a fourth arm.** The delta's three arms are
three COMPARISONS between two documents; this is a defect in a DECLARATION, and
it deliberately does NOT inherit the ledger's hedge ("cannot distinguish a
rewording from stale text"), which would be false of it: a marker naming a
carried unit is wrong with certainty.
