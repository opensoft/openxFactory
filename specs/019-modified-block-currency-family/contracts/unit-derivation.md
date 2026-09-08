# Contract: the normative unit derivation

**Module**: `scripts/doc_health/modified_block_currency.py`
**Realizes**: FR-004 – FR-010; `dh:84-110` (the delta's own normative
derivation) and `dh:99-103` (masking before any split).

The derivation is NORMATIVE in the ratified delta, so this contract is a
transcription of it plus the three mechanical readings research.md records
(R4, R6, R9). One function runs over BOTH documents; a derivation defect is
therefore symmetric and cannot invent a finding.

---

## `normalize(text: str) -> str`

Collapse every run of whitespace to a single space; strip leading and trailing
whitespace. **Nothing else.**

| in | out |
| --- | --- |
| `"a  b\n  c "` | `"a b c"` |
| `"A B"` | `"A B"` (case preserved — deliberately unlike `promotion_fidelity.norm`) |
| `"  "` | `""` |

**Postconditions**: idempotent; never casefolds; never touches punctuation or
backticks. A pinning test asserts `normalize("A") != promotion_fidelity.norm("A")`
so the two can never be silently merged.

---

## `mask_code_spans(text: str) -> str`

Return a string of the SAME LENGTH as `text` in which the INTERIOR of every
CommonMark code span is replaced by a filler character that is neither
whitespace nor `.`/`?`/`!`.

**CommonMark rule applied**: a run of N backticks opens a span; the closer is
the next run of EXACTLY N backticks. An unterminated run is literal text and
masks nothing. The backtick characters themselves are left in place (only the
interior is filled), so the mask's length equals the input's.

| in | masked (filler shown as `·`) |
| --- | --- |
| `` see `.openspec.yaml` here `` | `` see `··············` here `` |
| ``a ``x`.`y`` b`` | ``a ``·····`` b`` (outer fence of 2 wins) |
| `` unclosed ` tail. `` | unchanged |

**Postconditions**: `len(out) == len(text)`; no `.`/`?`/`!` survives inside a
span; the function is pure.

**Why length-preserving**: sentence boundaries are found on the mask and the
emitted text is sliced from the ORIGINAL. A shorter mask loses the offsets; a
mask applied to the emitted text puts filler in a finding a human reads.

---

## `fenced_regions(lines: Sequence[str]) -> set[int]`

Return the indices of every line inside a fenced code block, the fence lines
themselves included. A fence opens on a line whose first non-space characters
are a run of three or more backticks (or tildes) and closes on the next line
whose run is at least as long. An unclosed fence runs to the end of the block.

**RULED 2026-08-27**: those lines are neither units nor markers, in canon or in
a block. The delta does not say so and did not have to notice — but its OWN
written-out marker examples live inside a fenced block (`dh:187-190`), which
promotes into canon with the requirement. Without this rule those two lines
parse as COMPLETE markers (a real change id, a real ISO date, a closing colon)
and the requirement that defines the marker declares two of its own units
removed. The same class applies to every fenced example the corpus writes.

**Postcondition**: masked lines never appear in a `Unit.text` and never reach
`parse_marker`.

---

## `split_sentences(paragraph: str) -> list[str]`

Split at a `.`, `?` or `!` that is followed by whitespace or the end of the
paragraph, with boundaries computed on `mask_code_spans(paragraph)` and every
returned string sliced from `paragraph`. The terminator stays with the sentence
it ends. Empty results are dropped.

| in | out |
| --- | --- |
| `"One. Two."` | `["One.", "Two."]` |
| `` "Reads `.openspec.yaml` now. Then stops." `` | ``["Reads `.openspec.yaml` now.", "Then stops."]`` |
| `"No terminator"` | `["No terminator"]` |
| `"a.b"` | `["a.b"]` (no whitespace after the period) |

**Postconditions**: concatenating the outputs with the whitespace between them
reproduces the paragraph; no boundary falls inside a code span.

---

## `is_dated_bold_note(paragraph: str) -> bool`

True where `normalize(paragraph)` begins with a `**`-opened bold run AND that
bold run contains an ISO `YYYY-MM-DD` date.

**Precondition**: `parse_marker(paragraph)` has already returned `None`. The
two forms overlap by construction — a marker is also a dated bold paragraph —
and the marker test must win (R5).

| in | out |
| --- | --- |
| `**CORRECTED 2026-08-25 ON BRETT'S RULING — ...** rest of note.` | `True` |
| `**Removed from canon by add-x (2026-08-27):** …` | `True` — which is why the marker test runs first |
| `**Emphasis** leading an ordinary paragraph.` | `False` (no date in the bold run) |
| `Plain prose from 2026-08-25 onwards.` | `False` (no bold run) |

**This is the one predicate the delta does not spell out** (R6). It is pinned
against the real notes `openspec/specs/doc-health/spec.md` carries.

---

## `derive_units(lines: Sequence[str]) -> tuple[list[Unit], list[Marker]]`

The single derivation. `lines` are the raw lines of ONE requirement block,
BELOW its `### Requirement:` header — exactly what
`promotion_fidelity.parse_delta` puts in `DeltaRequirement.body`, and exactly
what the promoted-side reader collects.

**Algorithm** (order is normative):

0. Compute `fenced_regions(lines)` and DROP those lines from everything below.
   A fence is neither a unit nor a marker, and this step is first because a
   fenced block can contain anything — including two lines that would otherwise
   parse as markers.
1. Split the surviving lines into the BODY region (everything above the first
   `#### Scenario:`) and one region per scenario.
2. In each region, group consecutive lines into BULLETS (a line whose first
   non-space characters are `-`, `*`, `+`, or `<digits>.` followed by
   whitespace, plus its indented continuation lines) and PARAGRAPHS
   (blank-line-delimited runs of the rest).
3. For each PARAGRAPH, in this order:
   a. `parse_marker` → a `Marker`; emit NO unit.
   b. `is_dated_bold_note` → ONE unit, undivided.
   c. otherwise → one unit per `split_sentences` result.
4. For each BULLET, strip the list marker and emit ONE unit (R9 — applied on
   both sides, so it cannot mask a deletion).
5. Kinds: body region → `body`; a `#### Scenario:` heading → `scenario-title`
   carrying the title text only; a bullet inside a scenario region →
   `scenario-bullet` with `scenario` set to the normalized owning title. A
   PARAGRAPH inside a scenario region that is not a bullet is a `body` unit —
   scenarios in this corpus are bullet lists, and prose smuggled under a
   scenario heading is still requirement text somebody must carry.

**Postconditions**

- Every emitted `Unit.text` is `normalize`d and non-empty.
- No unit's text spans a marker paragraph.
- `derive_units` is pure and deterministic; two calls on equal input return
  equal lists in the same order.
- Order is document order, which is what makes a ledger finding readable.

**Worked example**

Input block (canon side):

```text
The pass SHALL do X. It reads `.openspec.yaml` first.

- a body bullet obligation

**CORRECTED 2026-08-25 — one note. Two sentences.**

#### Scenario: A run executes
- **WHEN** a run executes
- **THEN** it MUST do X
```

Output units:

| kind | text |
| --- | --- |
| body | `The pass SHALL do X.` |
| body | `` It reads `.openspec.yaml` first. `` |
| body | `a body bullet obligation` |
| body | `**CORRECTED 2026-08-25 — one note. Two sentences.**` |
| scenario-title | `A run executes` |
| scenario-bullet | `**WHEN** a run executes` (scenario: `a run executes`) |
| scenario-bullet | `**THEN** it MUST do X` (scenario: `a run executes`) |

Seven units, and the note is one of them rather than two.

Add a fenced block to that input:

````text
```
**Removed from canon by add-example-change (2026-08-27):** `a unit`
```
````

and the unit count stays SEVEN. The fenced line is not a unit and is not a
marker, so nothing is declared removed — which is the whole point of the rule.

---

## `carried(canon_units, block_units) -> list[Unit]`

Return the canon units that are NOT carried, in canon order. A canon unit is
carried iff some block unit has the same `kind` AND the same `key`.

**Forbidden**: substring containment in either direction; similarity; any
per-kind exception. A pinning test widens a block bullet at both ends around
canon's bullet verbatim and asserts canon's bullet is STILL returned as
uncarried (FR-009 — #351's widening mechanism).

**Bullet pooling**: because equality is `(kind, key)` and `scenario` is not
part of it, block bullets are pooled across every scenario automatically. That
is FR-012's "compared against ALL bullets of ALL scenarios", and the pooling is
asserted by a test that moves a bullet under a different scenario title and
expects silence.
