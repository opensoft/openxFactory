# Contract: the self-gate's tests, their subjects and their RED forms

One row per test in `tests/doc-health/test_modified_block_currency_self_gate.py`.
The **RED** column is how the test was shown failing before it passed (FR-020);
the observed output is recorded in `../evidence/self-gate.md`.

`M#` in the last column names the mutation-round mutant this test is the intended
killer for (`../evidence/self-gate.md` § Mutation round).

---

## Group 1 — the resolver guard (FR-002, FR-003)

| test | asserts | RED form | kills |
| --- | --- | --- | --- |
| `test_the_repository_under_test_is_the_tree_this_test_file_lives_in` | the resolved root equals `Path(__file__).parents[2]`; both markers present; `git rev-parse --show-toplevel` equals the root | assert the root equals the worktrees CONTAINER (`root.parent`) — fails naming both paths | M2 |
| `test_the_resolver_fails_on_a_checkout_it_cannot_confirm_and_never_walks_up` | passing `root.parent` (which carries no `openspec/changes/`) raises, with a message naming both markers and the path searched; and the *aggregation* checkout, if reachable, is likewise refused | invert to `pytest.raises` around the good root — fails because the good root resolves | M2 |

**Why the second test is kept rather than discarded after going green.** It is
the permanent assertion that there is no ancestor walk. `harden-ideation-readiness-check`'s
defect was exactly a resolver that *succeeded* on the wrong tree; a gate that only
proves the right tree resolves cannot tell the two apart.

---

## Group 2 — the discovery floor (FR-004, FR-005)

| test | asserts | RED form | kills |
| --- | --- | --- | --- |
| `test_the_family_examined_at_least_one_modified_block_over_the_real_tree` | `len(active_blocks(root)) >= 1`; message names the root, the glob and the change/capability counts | assert `>= 10_000` — fails with the real population in the message | M1 |
| `test_the_family_returns_findings_and_not_a_skip_over_a_tree_that_carries_changes` | the return value is a `list`, not a `Skip`; asserted apart from emptiness, per the family's own "cannot run" ≠ "found nothing" rule | assert `isinstance(out, Skip)` — fails | — |

---

## Group 3 — the named subjects (FR-006, FR-007, FR-008)

| test | asserts | RED form | kills |
| --- | --- | --- | --- |
| `test_the_scenario_arm_names_the_composed_view_rename_and_nothing_else` | exactly one `warning`; its change is `add-composed-view-authoring`, capability `ideation-dashboard`, requirement `Composed views are read-only with a repository jump`, omitted scenario `Gate verbs hide on a composed view` | assert the omitted scenario is the rename DESTINATION `Tile-bound gate verbs hide on a composed view` — fails, and demonstrates that a containment reading would have passed | M1 |
| `test_every_carriage_ledger_finding_over_the_real_tree_is_named` | the set of nine `(change, capability, requirement)` triples, compared with `==` | drop one triple from the expected set — fails naming the unexpected finding; add a fabricated triple — fails naming the missing one. Both directions run. | M1 |
| `test_the_resolution_ordering_and_marker_classes_read_zero_over_the_real_tree` | no finding matches the unresolved rule text (`resolves to no promoted requirement`) or the marker action (`_MARKER_ACTION`); each class named separately. **AMENDED 2026-09-05:** the ordering class (`the ordering of MODIFIED blocks for`) no longer reads zero over this tree — `split-opendox-two-layer-product`'s ratification made it the second ACTIVE RATIFIED writer of `neutral-product-pin`'s *An external neutral product is pinned by commit and digest, never by tag* beside `add-openspec-cli-pin` — and it is asserted against the NAMED EXACT SET `_ORDERING_SUBJECTS`, on `_LEDGER_SUBJECTS`' discipline, rather than as an empty band | invert one to `assert len(...) == 1` — fails; and a positive control asserts the three rule-text probes are the module's own strings, so a typo'd probe cannot read zero vacuously | — |

**The positive control matters.** An "absent from" assertion over a rule-text
probe is exactly the shape F1's mutation round caught: "the `FAMILY_RESOLUTION`
absence was documented in three places and asserted in none". So the zero-class
test also asserts that each probe string is present in
`modified_block_currency.py` — a misspelled probe then fails on the probe rather
than passing on the corpus.

---

## Group 4 — the own packet (FR-009 – FR-013)

| test | asserts | RED form | kills |
| --- | --- | --- | --- |
| `test_this_change_s_own_delta_is_among_the_blocks_the_family_examined` | `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md` is in the discovered set, with title `Deterministic check families` | assert a neighbouring packet's path that carries no doc-health delta — fails | M1, M3 |
| `test_the_own_delta_is_measured_against_canon_and_no_sibling_basis_exists` | `resolve(...)` returns status `canon` with basis `openspec/specs/doc-health/spec.md`; `add-family-enumeration-check` is absent from active changes and present under `archive/`; the ordering arm applies no basis override to this change | assert status `pending` — fails; assert the sibling is active — fails naming the archive path | M3 |
| `test_the_self_finding_quotes_this_change_s_two_stale_numeral_sentences` | exactly one `info` on the own delta path; its rule quotes both `twenty-one check families` and `Four of the twenty-one` | assert it quotes `twenty-two` (the block's own wording rather than canon's) — fails, which is the whole point: the finding names what CANON says and the block does not carry | M1 |
| `test_no_disposition_can_apply_in_the_single_repo_scope_the_gate_runs_in` | `load_dispositions(ctx, FAMILY)` is empty because `ctx.agg_root is None`; and the family's context surface is exactly `{repo_paths}` plus the `load_dispositions` handoff (FR-018) | assert the disposition set is non-empty — fails; add a fake `ctx.git` read to the probe's allowed set — fails | M4 |

---

## Group 5 — the movement pin (FR-014, FR-015)

| test | asserts | RED form | kills |
| --- | --- | --- | --- |
| `test_the_report_moves_only_in_this_family_s_lines` | two single-repo report runs of this checkout; `critical`/`error` movement 0; `warning`/`info` movement equal to the family's own per-severity counts **from the same tree**; every changed line falls in one of the four permitted classes; per-stage counts and every other family section byte-identical | run BOTH passes with `--skip-family modified-block-currency` — movement reads 0/0/0/0 while the family reports 1 warning and 9 info, so the pin fails | M5 |

**No literal totals.** `warning` movement is compared to
`len([f for f in findings if f.severity == WARNING])`, not to `1`. The numbers 1
and 9 do not appear in this test.

---

## Group 6 — the maintenance contract (FR-016)

| test | asserts | RED form | kills |
| --- | --- | --- | --- |
| `test_every_corpus_assertion_explains_what_to_do_when_the_corpus_moves` | each corpus-facing test's failure message (the shared `_moved()` helper) names the re-measure command, the "assert zero by the same mechanism" end state, and the resolved root | assert the message mentions a command that is not in it — fails | — |

This is the one test whose subject is the module's own text rather than the
corpus. It is here because SC-001 is a requirement about the failure message, and
a requirement about a message that nothing reads is a comment.

---

## What this contract deliberately does NOT cover

- **Anything F1 already pins.** The launch severities, the `FAMILY_RESOLUTION`
  absence, the `FAMILY_IDS` mirror, determinism, the skip/quiet pair and the
  no-basis structural guarantee are all asserted in
  `test_modified_block_currency.py`. This gate does not restate them. F1's
  hand-off is explicit that a second copy is the wrong move, and F2 followed the
  same rule.
- **Anything F2 already pins.** The #351 and #329 reconstructions, the
  tokenization fixture, the marker matrix and the name-ordering discriminator.
- **The report's rendering.** Whether the section distinguishes the three arms
  legibly is packet § 5.1 and F4's. This gate asserts only that the section's
  lines are the *only* lines that moved.
- **The eighteen-repository pass.** Packet § 7.4, F4's first instruction.
