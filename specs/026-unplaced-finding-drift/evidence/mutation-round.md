# Mutation round (T043, packet § 2.14)

Every mutant was applied to the LANDED module, the named test run, and the
mutant required to make it FAIL. Each was reverted from a pristine copy taken
before the round; the module was verified byte-identical afterwards.

```bash
$ diff -q <pristine> scripts/doc_health/modified_block_currency.py
MODULE BYTE-IDENTICAL to pre-mutation state
```

## Round 3 (2026-08-28, after Brett's shape amendment): 15 applied, **15 killed, 0 survivors**

Four mutants added for the amended shape rule; `(i)` retired, its subject (the
quoted-spans-only mask) now being the whole of `T1`.

| # | Mutation | Killed by | Verdict |
|---|---|---|---|
| **T1** | revert `_shape` to the quoted-spans-only mask — the rule as first ratified | `test_the_drift_grain_is_one_finding_per_arm_template` | KILLED — the real tree goes 1 → 6 |
| **T2** | drop the fail-closed fallback: merge texts no template claims into a template's bucket | `test_a_rule_text_no_template_claims_falls_back_and_is_never_merged` | KILLED |
| **T3** | match the templates against RAW text, skipping the repr mask | `test_a_title_that_embeds_another_arm_s_template_prose_matches_one_template` | KILLED **on the second attempt** — see below |
| **T4** | let an arm build its rule text inline again instead of rendering through its template | `test_the_arm_templates_are_the_only_place_the_prose_lives` | KILLED |

### T3 survived TWICE, and the second survival is the more interesting one

**First survival: no pin existed.** Matching templates against raw text still
resolved every finding on every tree correctly, because no corpus title carries
another arm's fixed prose today. A pin had to be constructed — which is exactly
when a rule is worth pinning, and the same argument F4 made for its own
adversarial-title test.

**Second survival: the pin was built in the wrong DIRECTION.** The first
construction was a SCENARIO-TITLES finding whose requirement title embedded the
carriage-ledger prose. Raw, both templates match — but `_ARM_TEMPLATES` is
ordered and first match wins with `scenario-titles` FIRST, so the unmasked build
still answered `scenario-titles` and the assertion passed. The pin has to run
the ordering AGAINST the answer: a CARRIAGE-LEDGER finding whose title embeds the
titles prose resolves, unmasked, to `scenario-titles` — the wrong template. Both
directions are now asserted, and the test carries a guard that fails if the
registry order ever stops putting the wrong template first, so it cannot quietly
stop biting.

**RETIRED: `(i)`, "mask only digit runs".** Its subject was the quoted-span half
of a mask that no longer decides shape on its own; `T1` covers the whole of the
old rule in one mutant.

## Round 2 (2026-08-28, after the combined review): 12 applied, **12 killed, 0 survivors**

Three mutants were added and one retired. The table below is round 2's; round
1's nine are unchanged in it, and the round-1 narrative for `(d)` is kept because
it is why `(d)` is written the way it is.

| # | Mutation | Killed by | Verdict |
|---|---|---|---|
| **M8** | delete the family's sort entirely, so grouping reads an unsorted list | `test_the_drift_finding_names_the_first_instance_in_report_order_and_is_deterministic` | KILLED |
| **M9** | emit BEFORE the sort (group over an unsorted list, then sort) | same | KILLED |
| **B2** | restore the global `re.sub` quoted-span mask — the bug this build shipped with | `test_two_unresolved_blocks_differing_only_in_capability_are_one_shape` | KILLED |

**RETIRED: "drop the trailing `findings.sort(key=_report_order)`".** It survived
round 1 because the line it mutated could not change any output:
`runner.run_suite` sorts the whole result by `Finding.sort_key` and
`report.render` sorts again before printing, so the order this family RETURNS in
reaches no reader. The ruling was to DELETE the line rather than pin it — a line
no test can fail is a line that will later be trusted for a guarantee it does not
give — so there is nothing left to mutate. What remains load-bearing is the sort
BEFORE the emit, which decides which finding each drift warning names; M8 and M9
are what hold it.

**WHY M9 COULD NOT BE KILLED BEFORE.** The first fixture tree had ONE change
directory, so its emission order (by normalized requirement title) and its report
order (severity, repo, PATH, rule) agreed, and grouping before or after the sort
named the same finding. A second change directory, `add-a-drift-case/`, was added
to make the two orders disagree: the ledger shape's first-in-report-order is now
ZETA and its first-in-emission-order is ALPHA. The pin now asserts the
disagreement itself, so it cannot silently stop biting.

## Round 1: 9 applied, **9 killed, 0 survivors**

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

## Gate re-runs after round 3

| gate | round 2 | round 3 |
|---|---|---|
| `python3 -m pytest tests/doc-health -q` | 1230 passed | **1236 passed**, 7 warnings |
| CI shape (clean `git archive` extraction) | 7 failed, 1214 passed | 7 failed, **1220 passed** — the same seven history-dependent tests as at the branch point, and 1199 → 1220 is the same +21 |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` | 78 / 0 | **78 passed, 0 failed** |
| full-report movement diff | one line | still **exactly one line**: `- unplaced-finding drift: 0 (\`warning\`)` |
| `git diff --stat <merge-base> -- .github/ openspec/` | empty | **empty** |

**The amendment moved no run's output.** It changes how unplaced findings GROUP,
and there are none wherever the map is complete — which is every run today. That
is why the movement diff is unchanged at one line across all three rounds.
