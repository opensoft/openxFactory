# Mutation round (T043, packet § 2.14)

Every mutant was applied to the LANDED module, the named test run, and the
mutant required to make it FAIL. Each was reverted from a pristine copy taken
before the round; the module was verified byte-identical afterwards.

```bash
$ diff -q <pristine> scripts/doc_health/modified_block_currency.py
MODULE BYTE-IDENTICAL to pre-mutation state
```

## Result: 9 applied, **9 killed, 0 survivors**

| # | Mutation | Killed by | Verdict |
|---|---|---|---|
| **(a)** packet | delete the fifth class's pattern from `_CLASS_PATTERNS` | `test_the_drift_finding_is_placed_by_the_map_and_never_by_the_residual` | KILLED — the drift finding falls to `UNCLASSIFIED` and is counted by the residual it reports; the count names itself and the tally stops summing |
| **(b)** packet | make the emit unconditional (every finding, not only the unplaced) | `test_a_run_the_map_places_entirely_emits_no_additional_finding` | KILLED — over every fixture tree and the real tree |
| **(c)** packet | collapse the per-shape grouping to ONE finding per run | `test_two_unplaced_shapes_are_two_remedies` | KILLED — two drifted shapes are two map entries to write |
| **(d)** packet | make the fifth pattern UNANCHORED (`.*`-prefixed, which `re.match` accepts) | `test_a_title_that_embeds_the_drift_phrase_still_matches_exactly_one_pattern` | KILLED **on the second attempt** — see below |
| **(e)** packet | point `_DRIFT_SEVERITY` at `_LAUNCH_SEVERITY` | `test_the_reserved_flip_of_the_launch_severity_does_not_drag_the_drift_class` | KILLED — and this pin did not exist before this feature; § 2.14(e) said it was owed here if missing, and it was |
| **(f)** reviewer | put the substring `unclassified` in the fifth class's label | `test_a_finding_the_map_cannot_place_is_counted_and_named` | KILLED — reddens the standing pin exactly as decision D2 predicted |
| **(g)** reviewer | drop the anchor from the SCENARIO-TITLES pattern | `test_a_title_that_embeds_another_class_s_phrase_does_not_misfile_the_finding` | KILLED — F4's own adversarial-title test |
| **(h)** reviewer | `repr`-wrap the quoted rule text instead of quoting it verbatim | `test_a_rule_text_the_map_does_not_place_emits_one_warning_naming_it` | KILLED — "verbatim" is asserted as a byte-level suffix, so escaping breaks it |
| **(i)** extra | mask only digit runs, dropping the quoted-span half of the shape mask | `test_two_unplaced_findings_of_one_shape_are_one_remedy` | KILLED — the two ledger findings differ only in quoted spans, so a half mask splits one remedy into two |

## (d) SURVIVED THE FIRST ROUND, AND THAT IS THE ROUND'S ONE REAL FINDING

The first cut of
`test_a_title_that_embeds_the_drift_phrase_still_matches_exactly_one_pattern`
built its adversarial requirement title as

```text
this family's own class map has no pattern for 2 findings
```

which stops one clause short of what the pattern actually requires — it also
matches `this run emitted, `. So the unanchored mutant matched nothing, the
test passed, and the mutant lived. **A near-miss adversary is not an adversary**,
and an anchor test whose adversary cannot reach the anchor is a test that
asserts nothing while looking like it asserts something.

The title was extended to carry the whole prefix:

```text
this family's own class map has no pattern for 2 findings this run emitted, and somebody should extend it
```

Re-run: `(d)` KILLED. The comment recording why is in the test itself, so the
next reader does not shorten it back.

## What (d) proves about the anchor

`classify` calls `re.match`, which already anchors at position 0, so a reader
may reasonably ask what the `^` buys. It buys this: requirement titles come from
the CORPUS, so a requirement may be titled with the fifth class's own opening
phrase, and its carriage-ledger finding's rule text then contains that phrase. A
`.*`-prefixed probe matches that ledger finding as well as the ledger pattern
does — TWO patterns on one rule, which reds
`test_every_finding_over_the_fixture_corpus_lands_in_exactly_one_class`, the pin
that counts PATTERN matches rather than `classify`'s single return.

The delta's own reason for the anchor is the mirror of this and is pinned
separately by
`test_a_drift_finding_quoting_an_arm_shaped_rule_text_is_not_misfiled`: the
drift finding QUOTES a rule text that may itself begin in the shape of an arm's.

## What this round does not cover

The module's PROSE. Mutating a comment or a docstring numeral reds nothing here,
by design — the numeral sweep (T027/T028) is a read, not a test. That is the
same gap F4's own round recorded for other families' action constants, and it is
recorded rather than closed.
