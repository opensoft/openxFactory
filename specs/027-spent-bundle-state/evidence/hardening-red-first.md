# The containment hardening, MEASURED — before and after, per escape

Lane: openxfactory-1d. Branch `fix/spent-state-containment-hardening`, cut from
`origin/main` at `47f90080` (which is at or after `3fa222f3`, the squash of
PR #587). Probed 2026-09-02.

**WHY THIS FILE EXISTS SEPARATELY FROM [`red-log.md`](./red-log.md).** That file
records the realization's red, and records honestly that the module and its
tests were authored in one pass so the strict test-first order was not the order
worked in. THIS file has no such deviation to disclose: every escape below was
probed **against `main`'s code, through `main`'s own functions**, before one line
of the fix was written — a checkout of `origin/main`, the reader called directly,
the answer recorded. The "after" column is the same probe against the same
inputs at this branch's head.

**WHAT AN "ACCEPT" COSTS, so the table is read for what it is.** Every row
marked *wrongly ACCEPTED* is a route by which a SPENT declaration is attributed
to a changelog entry that did not write it. The declaration then matches the
bundle it names, the containment check passes, and the
superseded-and-never-published `error` — the finding this family exists to raise
— is replaced by an `info`. Seven of the ten are that class.

## § A — the probe against `main` (RED)

Probe: `parse_spent_declarations` over a document whose base entry is
`## contract-v2.9`, one candidate line, then the reserved declaration naming
`contract-v3.0` as superseding. `entry == "contract-v3.0"` is the wrong answer
and the accept; `entry is None` is containment refused.

```text
F1 non-release ## heading                     -> ACCEPTED-as-v3.0
F2a ## contract-v3.0.1                        -> ACCEPTED-as-v3.0
F2b ## contract-v3.0-notes                    -> ACCEPTED-as-v3.0
F7 level-one # heading                        -> ACCEPTED-as-v3.0
F9a heading inside a fence                    -> ACCEPTED-as-v3.0
F9b indented ATX heading                      -> ACCEPTED-as-v3.0
L2 Setext ===                                 -> ACCEPTED-as-v3.0
L2b Setext ---                                -> ACCEPTED-as-v3.0
L3 empty ATX ##                               -> ACCEPTED-as-v3.0
control: ### subsection does NOT close        -> ACCEPTED-as-v3.0
control: correct entry                        -> ACCEPTED-as-v3.0

LIVE read: [('contract-v2.6', 'contract-v3.0', ())]
```

**The last two lines are the CONTROLS and they must not change**, which is what
makes the other nine measurements mean something: `main` already answers
correctly for a `###` subsection (the shape this repository's own declaration
sits in) and for a declaration directly inside its entry, and a "fix" that
closed on everything would have destroyed both.

The three that are not reader escapes, probed through `check_repo` over real git
fixtures and shims:

```text
F8 below-floor repo, no changelog -> SKIP: alphaFactory: contracts/CHANGELOG.md
   could not be read at the published tip 23e36c6fb, so a SPENT declaration
   could not be looked for — which is not the same fact as there being none
F11 batch-read failure -> alphaFactory: version control could not be consulted
   for contracts/manifest.yaml
L4 below-floor subject -> [('warning', 'contracts/CHANGELOG.md',
   'a SPENT declaration in contracts/CHANGELOG.md (line 5) names contract-v1.3
   as the bundle i…')]
```

## § B — the same probes at this branch's head (GREEN)

```text
F1 non-release ## heading                     -> entry=None
F2a ## contract-v3.0.1                        -> entry=None
F2b ## contract-v3.0-notes                    -> entry=None
F7 level-one # heading                        -> entry=None
F9a heading inside a fence                    -> entry='contract-v2.6'
F9b indented ATX heading                      -> entry=None
L2 Setext ===                                 -> entry=None
L2b Setext ---                                -> entry=None
L3 empty ATX ##                               -> entry=None
control: ### subsection does NOT close        -> ACCEPTED-as-v3.0
control: correct entry                        -> ACCEPTED-as-v3.0

LIVE read: [('contract-v2.6', 'contract-v3.0', ())]

F8 below-floor repo, no changelog -> findings=[]
F11 batch-read failure -> alphaFactory: version control could not be consulted
   for contracts/manifest.yaml or contracts/CHANGELOG.md — the whole batch read
   failed, so NEITHER document was obtained
L4 below-floor subject -> []
```

**F9a's after-answer is `contract-v2.6`, not `None`, and that is the right
answer.** The fenced `## contract-v3.0` no longer reopens anything, so the
declaration is still inside the entry it was actually written in —
`## contract-v2.6`'s — and is refused for naming `contract-v3.0` while sitting
in v2.6's entry. The escape is closed by the declaration landing where it really
is, which is a better outcome than landing nowhere.

**Both controls and the LIVE read are byte-identical across § A and § B.** The
live declaration at `contracts/CHANGELOG.md` line 389 still reads as contained
by the `contract-v3.0` entry under every tightened rule, which is the condition
the whole hardening was designed against: over-closing is the fail-closed error
and under-closing is not, but a rule tightened past the live document would
refuse the declaration that makes `main` green.

## § C — the escape table, with the test that pins each

| # | escape | reproduced on `main`? | effect there | test |
|---|---|---|---|---|
| F1 | a non-release `##` heading does not close the entry | YES | wrongly ACCEPTED | `…entry_is_pinned[a non-release H2 closes…]`, and end-to-end in `test_a_declaration_under_a_non_release_heading_is_refused_end_to_end` |
| F2 | `## contract-v3.0.1` / `-notes` open `contract-v3.0`'s entry | YES | wrongly ACCEPTED | `…entry_is_pinned[a longer name is not the v3.0 entry…]`, `[nor is a suffixed one]`, control `[but contract-v3.01 IS a well-formed name…]` |
| F7 | a level-one `#` heading does not close the entry | YES | wrongly ACCEPTED | `…entry_is_pinned[a level-one heading closes too…]`, `[including an empty one]` |
| F9a | a heading inside a fenced code block reopens/closes an entry | YES (`main` documents "NO FENCE TRACKING, deliberately") | wrongly ACCEPTED | `test_a_fenced_block_is_opaque_to_headings_and_to_declarations` |
| F9b | an indented ATX heading (1–3 spaces) is missed | YES | wrongly ACCEPTED | `…entry_is_pinned[two leading spaces is still a heading…]`, controls `[three too, and it still opens]`, `[FOUR is an indented code block…]` |
| L2 | Setext headings do not close an entry | YES (and on PR #584's head too) | wrongly ACCEPTED | `…entry_is_pinned[a Setext H1 closes…]`, `[and a Setext H2]`, controls `[but a run of dashes after a BLANK line…]`, `[and a table rule is not an underline either]`, `[a Setext heading CLOSES and never OPENS…]` |
| L3 | an empty ATX heading (`##` alone) is not a boundary | YES (and on PR #584's head too) | wrongly ACCEPTED | `…entry_is_pinned[and an empty H2, which is a legal ATX heading]`, control `[nor an empty H3]` |
| F8 | a below-floor repo with no `contracts/CHANGELOG.md` is SKIPPED entirely | YES (the guard sat above `parse_bundle`) | silent "not checked" | `test_a_below_floor_repository_with_no_changelog_is_not_newly_skipped`, whose positive control is the same shim declaring `contract-v1.7` |
| F11 | the batch-read skip names only the manifest | YES | misleading skip | `test_a_failed_batch_read_names_both_members_it_asked_for` |
| L4 | a below-floor SUBJECT raises an orphan warning | YES (and on PR #584's head too) | spurious warning | `test_a_below_floor_subject_raises_no_orphan_warning`, whose positive control is a wrong-SHAPE subject that must still raise it |

**Ten of ten reproduced on `main`. None was skipped.**

Two findings from PR #584's rounds are deliberately NOT in this table, and the
reason is that they do not exist on `main`: F3 (a current-bundle refusal
promising a companion finding that does not exist) — `main` phrases that
refusal conditionally; and F10 (the orphan sweep losing the read-failure skip)
— `main`'s guard is unconditional and early, and F10 was a hole PR #584's own
F8 fix opened. F12/F13 (an empty-backtick superseding bundle; `RULED BYE` read
as a ruling) are likewise absent: `main` computes the reason in
`_declaration_state`.

### Test counts, re-counted from collected runs rather than accumulated

| | `tests/doc-health/test_release_tag_publication.py` | `tests/doc-health` |
|---|---|---|
| `origin/main` `47f90080` | **46 passed** | **1411 passed**, 0 failed |
| this branch | **73 passed** | **1438 passed**, 0 failed |

`+27`: 21 parametrized boundary-table rows and 6 scenario tests. **Zero tests
were deleted and zero were edited to pass** — one fixture was extended
(`test_an_unreadable_changelog_at_the_published_tip_skips`'s shim now answers
`ls_tree_paths`, because the guard it exercises deliberately moved below the
inventory listing) and its assertions were kept and one added.

**THE SELF-GATE IS GREEN ON `main` AND STAYS GREEN HERE.** `main`'s
`tests/doc-health` reads `1411 passed, 0 failed` — the declaration is live and
`test_this_repository_reads_zero_and_the_probe_can_fire` passes — so unlike
PR #584 this branch has no declared red to carry, and any failure in that file
would be this branch's own. The live-read test added here is the second, sharper
guard on the same fact: it reads `contracts/CHANGELOG.md` from disk and reds if
a heading is ever inserted above the reserved line.

## § D — gates, at this branch's head

| gate | result |
|---|---|
| `pytest tests/doc-health` | **1438 passed, 0 failed** (`main`: 1411 passed, 0 failed) |
| `pytest tests/doc-health/test_release_tag_publication.py` | **73 passed** (`main`: 46 passed) |
| `pytest tests/sequenced_after` | **118 passed** |
| `validate-sequenced-after.py .` | passed — 31 active changes, 1 declaring. NO pin moved: this branch adds no OpenSpec change and moves no change directory |
| `openspec validate --all --strict` | **84 passed, 0 failed** |
| `proposal-support.py . verify declare-spent-bundle-state` | `proposal support verification ok` |
| `validate-contract-release.py verify-commit --commit HEAD` | exactly TWO mismatches, `contracts/CHANGELOG.md` and `docs/contract-versioning-policy.md` — **byte-identical to the same command at `origin/main`**, therefore INHERITED and not this branch's. This branch edits no inventory member |
| doc-health `--single-repo`, base vs head, same `--as-of 2026-09-02` | **54 findings on both sides, and the two finding lists are BYTE-IDENTICAL** — `6 critical, 5 error, 29 warning, 14 info` unchanged. The whole report diff is 20 lines: canon share 34.3% → 34.4% and the `standard` stage's word count 14482 → 14675, from the one paragraph added to `docs/doc-health.md`. **No new finding on the live corpus, and no finding removed** |

**The live-corpus read is the one that matters most here, and it is the ACCEPTED
`info` itself**: the head report carries

```text
severity=info family=release-tag-publication repo=… path=contracts/releases/contract-v2.6.digests.yaml
rule="contract-v2.6 is declared SPENT: … The record is contracts/CHANGELOG.md § contract-v3.0 —
RULED BY Brett Heap, 2026-09-02; MEASUREMENT: PR #565 comment `5502452624`. …" class="contested"
```

— which is `main`'s answer, unchanged, read through every tightened boundary
rule. The hardening refuses more and accepts exactly what it accepted before.

## § E — bot round 1 on PR #589, and the two findings it added to the table

Two more escapes, both MEASURED before fixing.

| # | escape (source) | on head `bf3f8c23` | after | test |
|---|---|---|---|---|
| R1-1 | a backtick fence whose INFO STRING carries a backtick opens no CommonMark fence, so the reader runs ONE FENCE OUT OF PHASE: the next bare fence closes its fictitious block while opening a real one (Codex P1) | `[('contract-v2.6', 'contract-v3.0')]` — read from inside a real code block, under `## Notes`, and **ACCEPTED** | `no declaration read` | `test_a_backtick_in_a_backtick_fences_info_string_opens_no_fence`, with a tilde control and a prose control |
| R1-2 | a run of dashes below a THEMATIC BREAK was read as a Setext underline, refusing a correctly contained declaration (Codex P2) | `entry=None` — a **false refusal** | `entry='contract-v3.0'` | boundary-table rows `[nor after a THEMATIC BREAK…]` and `[in any of the three break characters]` |

**R1-1 is the more serious of the two by a wide margin**, and it is the one case
where being fence-AWARE was worse than `main`'s "no fence tracking": a reader
out of phase with the document swallows real boundaries as code AND reads code
as a record. Both halves of the containment rule fell to one line. The fix
splits the opener in two, because the rule is not shared — a backtick fence's
info string may not contain a backtick, a tilde fence's may — and the test
carries controls on both sides, since a one-sided fix stops tilde fences opening
at all and hands the escape back.

**R1-2's broader ask was REFUSED with a measurement**, and the refusal has a
direction: every block form added to `_setext_content`'s exclusion list moves
the reader toward UNDER-CLOSING, whose failure is silence about the finding this
family exists to raise, where over-closing's failure is one `error` standing
beside the superseded `error` and quieting nothing. Indented code is the clearest
case against a blanket exclusion — an indented line cannot interrupt a
paragraph, so it is lazy continuation and the dashes below it genuinely ARE an
underline. The residue is stated in `_setext_content`'s own docstring.

Neither shape is present in the live `contracts/CHANGELOG.md`: zero thematic
breaks, zero backtick fence lines CommonMark would decline to open. Latent, and
recorded as latent rather than banked as harmless.

**Copilot round 1** — the live-read test asserted `len(read) == 1`, which reds
for the wrong reason the day a second number is spent. TAKEN: the declaration is
now looked up BY SUBJECT, and the anti-over-read half that the count was
standing in for is stated properly instead of implied — the reserved form
spliced INSIDE the live document's own fenced block must add no declaration,
which is future-proof and is a real positive control for the fence rule against
the live bytes.

Counts after round 1: family file **76 passed**, `tests/doc-health`
**1441 passed, 0 failed**.
