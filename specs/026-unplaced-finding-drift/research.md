# Research — F5, the fifth finding class

Phase 0. Seven questions this design turned on. Each records what was decided,
why, and what else was on the table. Nothing here re-opens the packet's D1–D3.

## R1 — The drift finding's rule-text grammar, and why it must not reuse the residual row's wording

**Decision.** The rule text is

```text
this family's own class map has no pattern for {n} finding{s} this run emitted, which share one rule shape the map has drifted behind; the first of them in this family's own report order reads, verbatim: {rule}
```

with `{rule}` the first instance's rule text included PLAIN (see R1b).

**Rationale.** Three constraints meet here. (1) The delta requires the count,
the verbatim first rule text, and — as `Finding` fields — the first instance's
repo and path. (2) The opening phrase must be distinct from the residual row's
`"findings this family emitted that its own class map does not place"`, because
F3's fourth probe (packet § 2.10) asserts its probe string IS the module's own
wording before asserting the class reads zero; a probe that matched BOTH the
residual line constant and the drift rule would make the positive control pass
against the wrong constant, which is the exact vacuity the three existing probes
were written to avoid. (3) The opening phrase must be a fixed prefix followed by
a variable part, so the class pattern can anchor past the variable part in the
shape `_BLOCK_HEAD` established.

**Alternatives considered.** Reusing "does not place" — rejected on (2).
Leading with the count (`"2 findings of this run carry a rule text…"`) —
rejected because the anchored pattern would then have to begin with `\d+`, which
is a weaker anchor and reads worse in a ranked plan sorted by rule text.

### R1b — `verbatim` means plain, not `repr`

`{rule!r}` escapes quotes and backslashes, so the quoted text would not be
byte-equal to the rule it names and `first.rule in drift.rule` would be false.
The delta says "verbatim". Plain inclusion, at the END of the rule text after a
colon, so no delimiter has to be invented and nothing after it can be mistaken
for the family's own prose.

## R2 — Why the anchor is load-bearing when `re.match` already anchors at position 0

**The question.** `classify` iterates `_CLASS_PATTERNS` and calls
`pattern.match(finding.rule)`, which already anchors at position 0. So what does
the `^` in `_BLOCK_HEAD` — and in the new pattern — actually buy?

**Measured answer.** The anchor is load-bearing in the OTHER direction, and the
case is real rather than defensive. Requirement titles come from the corpus. A
requirement titled

```text
this family's own class map has no pattern for 2 findings
```

produces a carriage-ledger finding whose rule text CONTAINS the drift class's
opening phrase. Measured on this tree:

| drift pattern | patterns matching that ledger finding |
|---|---|
| anchored (`^this family's own class map has no pattern for \d+ findings? this run emitted, `) | 1 — `carriage-ledger` |
| unanchored (`.*` prefixed) | 2 — `carriage-ledger` AND `unplaced` |

Two hits reds `test_every_finding_over_the_fixture_corpus_lands_in_exactly_one_class`,
which asserts `len(hits) == 1` over the pattern list rather than over
`classify`'s return — the stronger property the combined review of 2026-08-27
installed for exactly this reason. So mutation § 2.14(d) ("make the pattern
unanchored") IS caught, by a pin this feature adds in F4's own idiom
(`test_a_title_that_embeds_another_class_s_phrase_does_not_misfile_the_finding`).

**And the delta's own reason still holds separately.** The drift finding QUOTES
an unrecognized rule text which may itself begin `active MODIFIED block for '…'
omits …`. The existing arms' anchors are what stop that quotation from filing
the drift finding under `scenario-titles`; the delta's fourth scenario pins it,
and this feature tests it directly.

## R3 — The shape mask, and the order of its two substitutions

**Decision.** `_shape(rule)` replaces every single-quoted span and every
double-quoted span with one fixed placeholder, then every run of digits with
another. Quoted spans FIRST.

**Rationale.** The delta states the rule; the packet notes it is the same
grammar `_CLASS_PATTERNS` is written in (`_TITLE_REPR` and `\d+`) so a reader
can check it by eye. Order is immaterial to the RESULT — a digit inside a quoted
span is masked either way, since the whole span is replaced — but quotes-first
is the order the delta states and the one that survives a reader's eye check.
The quoted-span pattern is `_TITLE_REPR`'s own alternation, reused rather than
re-spelled, so a change to the family's quoting admits both sides at once.

**Two placeholders, not one.** A single filler would make `'a'` and `1`
indistinguishable, so two rule texts differing by a quoted-span-versus-digit
substitution at the same offset would collapse. Cheap to avoid; measured
nowhere; kept because the mask is an identity function and identity functions
that lose information are the ones that bite later.

**Not `_FILLER`.** The module already has `_FILLER = "\x00"` for the code-span
mask in the DERIVATION. Reusing it would tie two unrelated masks together. The
shape mask uses its own placeholders and the packet's § 4.4 already records that
this rule is this family's, not the package's.

## R4 — Where the emit sits, and why the family sorts twice

**Decision.** The emit runs AFTER the arms and AFTER the family's existing
severity-first sort, then the family sorts again.

**Rationale.** "First" in the delta means "in the family's own report order", so
the grouping must read an already-sorted list or "first" is undefined. Grouping
into a dict preserves the sorted order of first appearance, which makes the
choice of representative deterministic; the second sort then places the new
`warning`s where the report-wide ordering puts them. Two sorts of a list this
size is free, and the alternative — sorting once and inserting by bisect —
would put the ordering rule in two places.

**The emit reads only findings.** It calls `classify`, which reads the rule text
and the module constants and nothing else. No context, no filesystem, no second
corpus read. That keeps the family's structural discipline test
(`test_the_family_reads_exactly_two_things_from_its_run_context`) true without
amendment.

## R5 — Why the monkeypatched pass must not index `by_id` with `UNCLASSIFIED`

`test_every_finding_carries_its_class_s_band_and_action` builds
`by_id = {klass.id: klass for klass in CLASSES}` and does `by_id[classify(f)]`.
`UNCLASSIFIED` is deliberately NOT a class id — that is the whole point of the
residual — so under an induced drift the arms' now-unplaced findings raise
`KeyError` there. A `KeyError` is a crash, not the assertion the pin exists to
make, and a pin that crashes is a pin a later session deletes.

**Decision.** The amended pass partitions explicitly: findings that classify as
`UNCLASSIFIED` are asserted about directly (they keep the band and action of the
arm that emitted them — the drift does not rewrite them), and everything else,
the drift finding included, goes through `by_id` exactly as before. The
`all(checked.values())` assertion then reads a MEASURED `unplaced` count rather
than a zero.

## R6 — Why the new tree is not one of F2's `NEW_TREES`

F2's provenance checker iterates `NEW_TREES` and requires each tree's README to
carry `audit row **A<n>**` and a `add-modified-block-currency-check § 3.<n>`
citation. This tree belongs to F5 and to neither of those. Adding it to
`NEW_TREES` would force a fabricated audit-row citation into a README — false
documentation, produced to satisfy a checker, in the feature whose whole subject
is a checker that catches false documentation.

**Decision.** The tree joins `ALL_TREES` by glob (which is what makes it
behavioural, and what F2's own comment says the glob is for), carries a README
to F2's convention with `SYNTHESIZED` on line 3, and is pinned by a test of THIS
feature. `NEW_TREES` keeps meaning what it says.

## R7 — Making the reserved § 7.2 flip falsifiable

**The problem.** `_DRIFT_SEVERITY = WARNING` and
`_DRIFT_SEVERITY = _LAUNCH_SEVERITY` are value-identical today. Every assertion
about the constants' values passes under both. The existing
separately-assignable pin (`test_the_three_launch_severities_are_named_apart`)
also passes under both: rebinding one module attribute never moves another, even
when both were bound from the same expression. So mutation § 2.14(e) survives
every pin in the suite as it stands — which is exactly what § 2.14(e) predicts
and asks to be fixed.

**Decision.** A simulated-flip pin. It reads the module's own source, replaces
the single line `_LAUNCH_SEVERITY = WARNING` with the package's `error`
constant, executes the result as a module in the `doc_health` package
namespace, and asserts that the scenario-title class's band moved to `error`
while the drift class's band is still `warning`. Verified to run:
`titles band: error`, and no import edit is needed because the substituted value
is a string literal.

**Alternatives considered.** `importlib.reload` under a patched package constant
— rejected, it would move every family's severities at once and prove nothing
about this one. A comment — rejected: the packet's § 2.1 says the drag "would
also be INVISIBLE", and the remedy for an invisible drag is a test, not a note.
