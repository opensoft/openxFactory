# Phase 0 Research: F1 — the modified-block-currency family module

**Feature**: `019-modified-block-currency-family` | **Date**: 2026-08-27

The ratified delta decides WHAT this family checks, down to the unit
derivation and the marker grammar. What was still open was HOW that text lands
inside an existing package that already has twenty-one families, four readers
of the same headings, and a house pattern for an advisory launch. Every item
below is one of those, resolved against the code that exists and the delta's
own lines — never invented.

Line references of the form `dh:NN` are
`openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`.
`tasks:NN` is that change's `tasks.md`.

---

## R1 — The reader is a plain `Path` root, not a tree abstraction

**Decision**: read the checked-out tree directly, as `family_enumeration.py`
does (`_delta_statements(tree_root: Path)`), with one `Path.glob` for active
deltas and one `read_text` per promoted spec.

**Rationale**: `promotion_fidelity.WorkingTree` / `GitRefTree` exist because
that family has TWO ruled measurement bases, and its own promoted requirement
obliges every run to say which one it measured. This family has ONE basis by
contract — `dh:206-210`, "This family SHALL measure the checked-out tree" —
and the delta explains that a live-`main` reading would be actively wrong here,
because an active change lives on a branch. Wiring the abstraction in would
advertise a switch the family must never have, and would put a `basis_notes`
entry in `FAMILY_NOTES` that says nothing (`families.py`:1091-1093 keeps that
table at one entry deliberately). Both existing readers are also
archive-shaped: `WorkingTree.archive_changes` and `.delta_specs` resolve under
`openspec/changes/archive/`, which is precisely the directory this family
excludes.

**Alternatives considered**: (a) extend `WorkingTree` with active-change
methods — rejected: it edits a module whose tests must stay byte-green
(decision 5) and gives this family a git-ref path it must not have; (b) a new
tree class of this family's own — rejected as an abstraction over one
implementation.

---

## R2 — One heading grammar, two block readers, one derivation

**Decision**: reuse `promotion_fidelity.parse_delta` unchanged for the DELTA
side; add ONE new reader, `parse_spec_requirements`, for the PROMOTED side,
built on `promotion_fidelity`'s imported `_REQUIREMENT` and `_SCENARIO`
regexes; and derive units from raw block lines through a SINGLE function used
by both sides.

**Rationale**: `parse_delta` already returns exactly what the delta side needs
— operation, title, scenario titles, the raw body lines "in file order and
unmodified", and the `RENAMED` pairs title resolution requires — and its
docstring records why the body is carried at all (`duplicate_packet` needed the
bytes). The promoted side cannot reuse `parse_promoted`, which returns only
`{requirement: [scenario titles]}`; this family needs bodies and bullets. What
must NOT be duplicated is the HEADING grammar: `promotion_fidelity`'s own
docstring names the lesson (`align-status-reader-to-real-lines`) that two
readers of one document come to disagree about whether it says something. So
the new reader imports the regexes rather than restating them, in the shape
`duplicate_packet.py`:142-144 already imports private names from that module.
The property that actually protects the comparison is that ONE `derive_units`
runs over canon's block and the delta's block, so a derivation bug is symmetric
and cannot invent a finding.

**Alternatives considered**: extending `parse_promoted` to return bodies —
rejected: it changes a function `promotion_fidelity` and its 1026-line test
file depend on, and decision 5 forbids touching that family's behaviour.

---

## R3 — TWO normalizations, named apart, and the reason each exists

**Decision**: `normalize(text)` in the new module collapses runs of whitespace
to one space and strips the ends, and does NOTHING else — no casefolding.
`promotion_fidelity.norm` (whitespace + casefold) is reused ONLY for the
requirement-title resolution key and the disposition key.

**Rationale**: `dh:84-90` is explicit — "matched in full after whitespace
normalization ... no normalization beyond it applies" — and `dh:91-97` forbids
containment and similarity in the same breath. Casefolding is "normalization
beyond it", so unit comparison is case-SENSITIVE and `norm` cannot be reused
for units. The opposite holds for the two KEYS: the disposition mechanism keys
on `norm(requirement)` in `promotion_fidelity.disposed`, and an entry written
for one family must key the same way for another or the shared
`health/dispositions.yaml` stops being one file; requirement-title resolution
is a lookup ("which requirement does this block target"), which the corpus
already treats as case-insensitive because "a title's case is a rendering
choice no reader acts on differently" (`norm`'s own docstring).

**Consequence, stated rather than discovered**: a block that restates a
scenario title with different capitalization WILL be reported by the
scenario-title arm. That is the delta's rule, not an accident, and it is
consistent with the arm's purpose: promotion writes the block's bytes into
canon, so a case change is a text change.

**Alternatives considered**: casefolding units for "fewer false positives" —
rejected, it is exactly the "normalization beyond it" the delta forbids, and
the same argument would license stripping punctuation, which is how the codex
gap (`tier-2` → `tier 2`) hid inside a scenario body.

---

## R4 — Backtick masking is length-preserving, and the reported text is the original

**Decision**: `mask_code_spans(text) -> str` returns a string of the SAME
LENGTH with the interior of every CommonMark code span replaced by a filler
character that is neither a sentence terminator nor whitespace. Sentence
boundaries are computed on the masked string; every emitted unit is sliced from
the ORIGINAL at those offsets.

**Rationale**: `dh:99-103` requires masking "before any sentence split" so a
period inside `` `.openspec.yaml` `` never ends a sentence; the review measured
118 backticked tokens with internal periods in canon's requirement bodies. A
mask that changes length would make offsets unusable, and a mask applied to the
REPORTED text would put filler characters in a finding a human reads. Code-span
recognition follows CommonMark: a run of N backticks opens and the next run of
exactly N closes; an unterminated run is literal text and masks nothing.

**Alternatives considered**: masking by regex substitution into a new string —
rejected, offsets are lost; splitting on the original and repairing fragments
afterwards — rejected, that is the noise arm the review predicted.

---

## R5 — Paragraph, sentence, bullet: the three shapes, and their order

**Decision**: within a region (body, or one scenario), a PARAGRAPH is a
blank-line-delimited run of consecutive non-bullet lines; a BULLET is a line
whose first non-space characters are a list marker (`-`, `*`, `+`, or an
ordered marker) followed by whitespace. A paragraph is classified in this
order: (1) reserved-marker form → not a unit at all; (2) dated bold note → ONE
undivided unit; (3) otherwise → split into sentences at `.`, `?` or `!`
followed by whitespace or the end of the paragraph, the terminator staying with
the sentence it ends.

**Rationale**: the order is forced. A marker is itself a dated bold paragraph
(`**Removed from canon by <id> (<date>):**` opens a bold run and carries an ISO
date), so testing "dated bold note" first would swallow every marker and the
declaration mechanism would silently vanish. `dh:109-110` puts marker-form
paragraphs outside both unit kinds explicitly, and `dh:179-183` requires it in
both directions.

**Alternatives considered**: treating an indented continuation line as its own
unit — rejected, a wrapped bullet is one bullet and the delta's whitespace
normalization exists precisely so wrapping is not semantic.

---

## R6 — What a "dated bold note" is (the delta's one under-specified predicate)

**Decision**: a paragraph is a dated bold note where, after normalization, it
BEGINS with a `**` bold run and that bold run contains an ISO `YYYY-MM-DD`
date. Recognized only after the marker test has already returned None.

**Rationale**: `dh:103-107` makes the note ONE undivided unit and gives the
reason ("a note being a single editorial statement whose sentences mean nothing
apart") but does not state the recognition predicate. This reading is the
corpus's own convention in all five of the instances the review examined —
`**CORRECTED 2026-08-25 ON BRETT'S RULING — ...**`,
`**THE ORDERING DEPENDENCY RESOLVED, 2026-08-25 — ...**`,
`**FOURTH RESTATEMENT, AND THE FIRST ONE A CHECK VERIFIED — appended
2026-08-25 ...**` — and the marker's own two forms are members of the same
family of shapes, which is why the ordering in R5 is load-bearing.

**THIS IS THE ONE PLACE F1 SUPPLIES A RULE THE DELTA DOES NOT WRITE**, and it
is called out rather than absorbed. It is pinned against the REAL notes the
corpus carries (a test reads `openspec/specs/doc-health/spec.md`'s own notes
and asserts each is one unit), so the reading is measured rather than asserted.
A veto here changes unit counts and therefore the ledger's predicted +11, which
is why it is named in plan.md's decision list.

**Alternatives considered**: (a) any paragraph opening a bold run, dated or not
— rejected, it would swallow ordinary emphasis-led prose and under-report;
(b) requiring the WHOLE paragraph to be bold — rejected, the corpus's notes
close the bold run mid-paragraph and continue in plain prose.

---

## R7 — Marker form: what "COMPLETE prefix" means, and what "resolvable" means

**Decision**: the form test anchors at the start of the normalized paragraph on
one of exactly two patterns: `**Removed from canon by <id> (<ISO>):**` and
``**Merged into `<destination>` by <id> (<ISO>):**``. `<id>` matches the
corpus's change-id token grammar (`[a-z0-9][a-z0-9-]*`); `<ISO>` is
`\d{4}-\d{2}-\d{2}`. The REASON is optional: a marker with no ` — <reason>` is
still of marker form.

**Rationale**: `dh:125-133` makes the anchor load-bearing and says why — this
requirement's own text and `document-lifecycle`'s both set out the two
templates in prose that promotes into canon, and a looser test would read them
as markers and exempt them from carriage, "the check quietly declining to check
the paragraphs that define it". A paragraph that merely quotes a template does
not BEGIN with a complete prefix, because the quoted form carries
`<change-id>` and `<YYYY-MM-DD>` placeholders rather than a real id and a real
date. That is the whole mechanism, and it only works if the id and the date are
matched as VALUES.

"A resolvable change-id" (`dh:127`) is read as "matches the change-id token
grammar", NOT as "names a change that currently exists". Requiring existence
would make every marker rot the moment the change that wrote it archives — the
delta's own durability argument (`dh:179-183`: a marker promotes into canon
with the requirement) requires the opposite. This is a genuine ambiguity in the
delta and is recorded as such; the safer reading is also the one the delta's
other sentences need.

The reason being optional follows from the anchor plus the delta's own
written-out example, whose `Merged into` line (`dh:189`) carries no reason at
all, and from `dh:142-146` defining the reason as "everything after the last
code span's following ` — `" — a definition that yields the empty string
rather than a parse failure.

**Alternatives considered**: requiring the reason — rejected, it would make the
delta's own example invalid; resolving the change id against the tree —
rejected for the durability reason above, and it would make the marker's
validity depend on a directory listing.

---

## R8 — Code-span extraction is CommonMark's, including the longer fence

**Decision**: `extract_code_spans(text) -> list[str]` scans for a run of N
backticks, takes the next run of exactly N as the closer, and returns the
interior with one leading and one trailing space stripped where BOTH are
present (CommonMark's rule). Names are the spans following the closing `:**`,
in order. For `Merged into`, the destination is the span INSIDE the bold prefix
and is excluded from the names.

**Rationale**: `dh:135-146` requires the longer fence and gives the
measurement — roughly a third of body units and a sixth of bullets contain a
backtick — and requires extraction "in order, per CommonMark", with the
explicit warning that punctuation splitting is not the mechanism. `dh:148-151`
makes the destination not a named unit, "or every valid merge marker reports
itself".

**Alternatives considered**: splitting on `` `...` `` with a non-greedy regex —
rejected, it truncates at the first inner backtick, which is the exact defect
the longer-fence rule exists to prevent; splitting the tail on `;` — rejected
by `dh:144-146`.

---

## R9 — List markers are stripped on scenario bullets too, and why that is safe

**Decision**: strip the list marker from BOTH body bullets and scenario
bullets.

**Rationale**: `dh:103-105` states stripping for the body bullet and `dh:107-109`
says only "each bullet line SHALL be one bullet unit" for the scenario bullet.
Stripping symmetrically is a gap-filling reading, and it is safe for a reason
that can be stated exactly: the SAME derivation runs on both sides of every
comparison, so stripping cannot make an absent unit look present — it can only
stop a change of list marker (`-` → `*`) from being reported as a lost
obligation. The asymmetric alternative reports a defect that is not one.

**Alternatives considered**: stripping only in the body, per the letter —
rejected on the above; stripping the `**WHEN**` / `**THEN**` bold lead as well
— rejected, that is content, and removing it would let a `WHEN` bullet match a
`THEN` bullet.

---

## R10 — What a marker name that matches nothing does

**Decision**: a marker name is resolved against canon's units by normalized
equality, any kind. A name matching an ABSENT canon unit suppresses it. A name
matching a canon unit the block still CARRIES makes the marker itself reported
(`dh:153-156`). A name matching NO canon unit at all suppresses nothing and is
not itself reported.

**Rationale**: the delta mandates exactly one reporting case for a marker — the
one naming a unit the block still restates — and a name that matches no canon
unit cannot buy silence, because suppression is keyed on the unit it names. So
the fail-closed behaviour is already the delta's, and reporting the dangling
name too would be an obligation this feature has no standing to add. Recorded
so a later ruling can add it deliberately rather than an implementation adding
it by accident.

**Alternatives considered**: reporting a dangling name as a malformed marker —
deferred, not built; it is a plausible later ruling and is named in plan.md's
residue.

---

## R11 — Ordering by declaration, the whole-token matcher, and three severities

**Decision**: (a) the declaration is read with `duplicate_packet._mention`,
imported rather than re-spelled; (b) the writer set for one
(capability, requirement title) is evaluated as a GROUP, and anything other
than exactly one declaration inside a group of two or more active RATIFIED
writers is reported; (c) the module names THREE severity constants —
`_LAUNCH_SEVERITY` (the scenario-title arm, `WARNING`),
`_RESOLUTION_SEVERITY` (title resolution / two-writers, `WARNING`) and
`_LEDGER_SEVERITY` (the carriage ledger, `INFO`).

**Rationale**: (a) `dh:71-74` names the matcher by reference — "the whole-token
match the duplicate packet family already uses" — and that function exists,
with the false-exemption channel it closes written into its docstring; a second
copy is the two-grammars defect this corpus keeps paying for. (b) `dh:262`
says "two or more" while the surrounding prose says "two", and the population
is zero today (`tasks:302-313`), so the group reading is both the delta's
scenario text and the conservative one. (c) `tasks:82-83` asks for
`_LAUNCH_SEVERITY` as a module constant "so the flip in § 7.2 is one line
beside one `FAMILY_RESOLUTION` row", while `tasks:333-339` reserves that flip
for the SCENARIO-TITLE arm alone. One constant for all three arms would drag
the title-resolution arm to `error` on that flip, which no ruling asked for.
Three constants satisfy both, and the flip-bearing one keeps the
`_LAUNCH_SEVERITY` name that `promotion_fidelity`, `duplicate_packet` and
`family_enumeration` all use — the grep that ties every reader of the launch
decision together (`duplicate_packet.py`:150-152).

**Alternatives considered**: one constant — rejected above; a per-finding
`severity=` argument with no constants — rejected, it deletes the grep and the
structural pin F2 will assert.

---

## R12 — The disposition read needs no refactor at all

**Decision**: import and call
`promotion_fidelity.load_dispositions(ctx, FAMILY)` and
`promotion_fidelity.disposed(dispositions, repo, path, title)`. Write nothing.

**Rationale**: `tasks:113-116` says "Reuse that reader; do not write a second
one", and the reader is ALREADY parameterized: `load_dispositions(ctx, family=
FAMILY)` takes the family name precisely so a sibling can read the same file
under its own name, and `duplicate_packet.py`:410-415 consumes it in exactly
this shape. So the orchestrator's contingency — "if reuse needs a small
refactor to a shared helper, that refactor is a task with its own test" — does
NOT trigger: there is no refactor, and `promotion_fidelity.py` is not edited by
this feature at all. The single-repo caveat is inherited and stated: the file
lives at the aggregation root, so a `--single-repo` self-gate applies no
disposition.

**Alternatives considered**: a shared `dispositions.py` module — rejected, it
moves code three families depend on for no behaviour change, and every one of
their tests would have to move with it.

---

## R13 — The § 2.1 commit: what it contains and what proves it

**Decision**: one commit carries the registration (`families.py`,
`__init__.py`), the module, its tests, the lifecycle-scan-set classification,
AND the `## MODIFIED Requirements` block on "Deterministic check families" in
`openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`.

**Rationale and mechanics**: canon still enumerates in prose, because
`add-family-enumeration-check` is active with code landed and delta unpromoted
(`tasks:314-320`, re-confirmed in this tree: `openspec/specs/doc-health/spec.md`
reads "twenty check families" and `FAMILIES` registers 21). A registration
without the block leaves canon naming a set the registry contradicts; a block
without the registration reds
`test_family_enumeration.py::test_the_real_corpus_reads_zero_on_both_halves`,
which was demonstrated, not assumed (`tasks:286-290`, three findings). The
block is written relative to `add-family-enumeration-check`'s OUTCOME — that
change's own delta at
`openspec/changes/add-family-enumeration-check/specs/doc-health/spec.md`, which
carries the requirement with 8 scenarios and the enumeration at twenty-one — and
moves exactly five things: `twenty-one` → `twenty-two`; the enumeration gains
`modified-block currency` as its last member; `Four of the twenty-one` →
`Four of the twenty-two`; `the other seventeen families` → `the other eighteen
families`; and one new sentence declaring this family's document lists, in the
shape the four preceding families' sentences already use. The eighth scenario,
`A run executes the check families`, gains one `AND` bullet. The other seven are
byte-identical.

Three consequences are carried rather than discovered:

1. `fam_family_enumeration` must read 0 against the resulting tree. Its name
   normalization is mechanical (`lower`, then `/` and whitespace to `-`), so
   `modified-block currency` resolves to `modified-block-currency` — which is
   the registry id, so no `ALIASES` entry is needed and none may be added
   (`test_every_alias_is_load_bearing` asserts every alias is still necessary).
2. `tests/doc-health/test_lifecycle_scan_set.py`:500 asserts
   `len(NON_READERS) == len(FAMILIES) - 4 == 17`; the literal becomes 18 and the
   family joins `NON_READERS` with the note the other non-readers carry.
   `test_family_enumeration.py`:295 asserts
   `len(FAMILY_IDS) == len(set(FAMILY_IDS)) == len(FAMILIES)`, satisfied by
   registering in both.
3. The block draws ONE carriage-ledger finding against this change's own delta —
   the two body sentences it changes by exactly the numerals this feature moves
   (`tasks:291-301`). It is expected, advisory, predicted in the packet's own
   table, and MUST NOT be dispositioned away: a disposition would suppress the
   evidence that the family reads its own packet.

**Alternatives considered**: land the registration first and the block second —
rejected, it reds the standing gate for the length of one commit and the packet
forbids it in capitals (`tasks:46`); wait for `add-family-enumeration-check` to
archive — rejected, it is a veto of D5 and a dependency this feature cannot
schedule.

---

## R14 — The advisory launch, in both halves, and what pins it

**Decision**: `warning`/`warning`/`info` per R11, and the family is ABSENT from
`families.FAMILY_RESOLUTION`, with the reason recorded beside its `FAMILIES`
registration in the shape the four preceding families' comments use.

**Rationale**: `dh:212-226`. The half that is easy to lose is the second one:
`report.uncited_resolutions` turns a `contested` finding that vanishes between
reports into an `error`, so a `contested` advisory family reds the nightly the
first time anyone fixes a block — enforcement through the back door, on the run
that proves the launch worked. `runner.py`:497-499 is the line that applies the
table (`FAMILY_RESOLUTION.get(f.family, f.resolution)`), so absence leaves the
`Finding` default `auto-fixable`, which is what the other advisory launches
carry.

**Alternatives considered**: none. No flip is in F1's scope and the packet
reserves it for a ruling.

---

## R15 — The scope guard, and how promotion-fidelity stays byte-green

**Decision**: F1 touches exactly six paths — the new module, its new test file,
`families.py`, `scripts/doc_health/__init__.py`,
`tests/doc-health/test_lifecycle_scan_set.py`, and the packet's own doc-health
delta — plus new fixture directories under
`tests/doc-health/fixtures/modified-block-currency*/`.

**Rationale**: decision 5 of the launching brief and `tasks:252-258`. Nothing
in `.github/workflows/` changes, because this family passes no per-family
option and must not (F4 owns the pin that says so). `report.py` is not touched:
a `FAMILY_IDS` entry is all a report section needs (`report.py`:252 iterates
`FAMILY_IDS + SEMANTIC_FAMILY_IDS + ["preflight"]`). `promotion_fidelity.py`
and `duplicate_packet.py` are IMPORTED and not edited, so their 1026-line and
604-line test files are untouched and must stay green byte-for-byte — which is
itself an F1 acceptance check, not an assumption.

**Alternatives considered**: none. Anything wider is another feature.

---

## Cost, briefly

The family reads 26 active change directories in this repository, their
`specs/*/spec.md` files, and one promoted spec per capability referenced,
cached. That is tens of file reads and no subprocess — cheaper than
`promotion-fidelity`'s pinned basis, which walks 89 archived packets. No
performance requirement is stated and none is needed.
