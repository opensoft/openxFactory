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

## § F — bot round 2, and the guard's repair becomes STRUCTURAL rather than another exclusion

| # | escape (source) | on head `24be0ce9` | after | test |
|---|---|---|---|---|
| R2-1 | an underline-SHAPED line that underlined NOTHING is paragraph text, so the run below it IS a heading — round 1's fix excluded it ON SYNTAX and lost the boundary (Codex P1) | `## contract-v3.0` / `===` / `---` → `entry='contract-v3.0'`, **ACCEPTED** | `entry=None` | boundary-table rows `[an underline-SHAPED line that underlined NOTHING…]` and `[but a run below an underline that really DID underline…]` |
| R2-2 | the live-corpus anti-over-read guard spliced at a BYTE OFFSET into the fence opener line, so the reserved opener landed mid-line and the assertion passed whatever the fence rule did — a VACUOUS test (Copilot) | `text[fence:fence+30]` = `'```yaml\n    relocating:\n      '` — spliced after ` ```y ` | spliced as a real line at the start of the fenced content, **and the non-vacuity itself asserted**: the same line with the fence opener removed MUST be read | `test_this_repositorys_live_declaration_survives_every_boundary_rule` |

**R2-1 IS THE THIRD TIME ON THIS GUARD THAT A FIX HAS BEEN THE NEXT FINDING'S
CAUSE** (PR #584 saw it twice), and it is why this round's repair is structural.
`_setext_content` is GONE. In its place `_paragraph_line(line, closes, opaque)`
takes the boundary decision the caller has already made, and the loop carries a
BOOLEAN forward instead of the previous line's text — so `_entry_boundary(line,
after_paragraph, in_fence)` cannot be handed a syntax question in place of a
state one. An underline that really underlined sets `closes` and therefore ends
the paragraph; one that only looked like an underline does not. The class of bug
is now unrepresentable in the signature rather than absent from the body.

All five Setext-family shapes measured together rather than one at a time, which
is what the previous two rounds each failed to do:

| shape | after |
|---|---|
| `===` / `---` | `entry=None` — the boundary is caught |
| `Title` / `===` / `---` | `entry=None` — closed by the first; the second is not a second heading |
| `***` / `---` | `entry='contract-v3.0'` — both thematic breaks, correctly contained |
| blank / `-----` | `entry='contract-v3.0'` — thematic break |
| `\| a \| b \|` / `\|---\|---\|` | `entry='contract-v3.0'` — a table rule is not an underline |

**R2-2 is the more instructive of the two about test quality**: the guard was
added in round 1 to answer a Copilot finding, and it could not fail. The
non-vacuity assertion added here is the one that would have caught it, and it
fails loudly for any future splice landing somewhere unreadable — which is a
better answer than fixing the offset.

Counts after round 2: family file **78 passed**, `tests/doc-health`
**1443 passed, 0 failed**.

## § G — bot round 3: `\s` is a Python fact, not CommonMark's

| # | escape (source) | on head `0aa59945` | after | test |
|---|---|---|---|---|
| R3-1 | Python's `\s` matches U+00A0 and the other Unicode spaces; CommonMark's ATX opening sequence admits only a SPACE, a TAB or end of line. `##<U+00A0>contract-v3.0` is paragraph text to every renderer and opened a FICTITIOUS entry here (Codex P1) | `entry='contract-v3.0'` — **ACCEPTED under a heading that does not exist** | `entry='contract-v2.9'`, the real containing entry, so the declaration is refused | five boundary-table rows: the fictitious open, the same line closing nothing, an incomplete token, and TWO TAB CONTROLS |

Fixed in all three patterns and in BOTH space classes of the entry heading —
the separator after `##`, because a Unicode space there means the line is no
heading at all, and the one after the version token, so a name followed by
U+00A0 is not a complete token.

**THE REGRESSION TESTS ARE AIMED AT THE HOLE THIS FIX COULD OPEN, not only at
the one it closes** — the discipline three rounds on this guard have earned,
and the orchestrator's standing instruction from 2026-09-02. Narrowing `\s`
invites narrowing it too far, so a TAB separator is a row of its own and must
still OPEN (`##\tcontract-v3.0` → `contract-v3.0`), and a tab-separated H1 must
still CLOSE.

**And one hole the fix opened in the TEST rather than the code, closed with
it.** Three of those rows turn on a literal U+00A0 in the test file, which an
editor, a formatter or a copy-paste can normalise to an ordinary space — after
which they would pass for the WRONG REASON, exercising a plain
`## contract-v3.0` heading and proving nothing about the rule they exist for.
They are written `f"##{NBSP}…"` against a named `NBSP = " "` now, with the
reason stated at the constant, because an escape cannot be normalised silently.

Latent, not live: `contracts/CHANGELOG.md` carries zero ATX lines using
non-space/tab whitespace.

Counts after round 3: family file **83 passed**, `tests/doc-health`
**1448 passed, 0 failed**.

## § H — bot round 4: the line SPLITTER, which is round 1's class one layer down

| # | escape (source) | on head `8219cb3e` | after | test |
|---|---|---|---|---|
| R4-1 | `str.splitlines()` breaks on EIGHT separators CommonMark does not, so an INVALID backtick opener like ```` ```bad<U+2028>`info ```` — one line to CommonMark, its info string carrying a backtick — was handed to the reader as a VALID opener plus content, putting it one fence out of phase again (Codex P1) | `entry='contract-v3.0'` — **ACCEPTED**, for all eight of U+2028, U+2029, U+0085, VT, FF, FS, GS, RS | nothing read, for all eight | `test_only_commonmarks_line_endings_break_a_line`, parametrized over the eight |

Fixed by splitting on `\r\n|\r|\n` and nothing else.

**THE CONTROL IS AIMED AT THE HOLE THIS FIX OPENS**, which on this guard is not
hypothetical: narrowing the splitter invites narrowing it to `\n` alone, and a
CRLF document would then carry a stray `\r` at the end of every line — where it
defeats the fence closer's `[ \t]*$`, the ATX lookahead's `[ \t]|$` and the
Setext underline's anchor ALL AT ONCE AND SILENTLY.
`test_the_three_line_endings_commonmark_does_recognise_still_work` pins LF, CRLF
and lone CR, in BOTH directions under each (a contained declaration must be
read, a fenced one must not), because a splitter that broke only the reading half
would look correct from the accepting half.

Two smaller things carried with the fix:

* `_lines` drops a single trailing empty element, so a document ending in a
  newline keeps the line count a human repairing a declaration would count —
  `SpentDeclaration.line` is read against an editor's gutter.
* The eight separators are NAMED in a `SPLITLINES_ONLY` table rather than typed
  as literals, for the same reason `NBSP` was named in round 3: a literal
  U+2028 in a source file is a character a tool can normalise, after which those
  rows would pass over an ordinary newline and prove nothing. The test file
  carries ZERO literal exotic characters, checked.

Latent, not live: the changelog carries none of the eight.

Counts after round 4: family file **94 passed**, `tests/doc-health`
**1459 passed, 0 failed**.

### The pattern, stated because it is the finding above the findings

**Four of the five Codex P1s on this branch were found ON THE FIX FOR THE LAST**
— PR #584 saw the same thing twice before it — and every one has been on
containment. The shape is consistent: each fix was correct about the case it
answered and stated the rule in a slightly wrong *alphabet*. Round 1 fixed the
fence opener's info string; round 4 found the line splitter feeding it. Round 1
excluded underline-shaped lines by syntax; round 2 found that syntax was the
wrong question and moved it to state. Round 3 narrowed `\s` to `[ \t]`; the
control against narrowing it to `" "` alone was written in the same commit.

**What has actually converged is the SHAPE of the repair rather than the count
of rules.** The boundary decision is carried as state (round 2), the reader
splits and fences per CommonMark rather than per Python (rounds 1 and 4), and
the character classes are CommonMark's rather than the regex engine's
(round 3). Since round 3 every fix has shipped with a test aimed at the hole the
FIX could open, not only at the hole it closes — which is the discipline this
sequence earned and the orchestrator made standing on 2026-09-02.

## § I — bot round 5: raw HTML blocks, and WHY THE CLASS TERMINATES HERE

| # | escape (source) | on head `6390f1e4` | after | test |
|---|---|---|---|---|
| R5-1 | a ```-shaped line inside a RAW HTML BLOCK is HTML content; treating it as a fence delimiter put the reader one fence out of phase for a THIRD time (Codex P1) | `entry='contract-v3.0'` — **ACCEPTED**, for all EIGHT of `<pre>`, `<script>`, `<!--`, `<?`, `<!DOCTYPE`, `<![CDATA[`, `<div>` and any complete tag | nothing read, for all eight | `test_a_fence_shaped_line_inside_raw_html_opens_no_fence`, parametrized over the eight kinds |
| R5-2 | the carried evidence transcripts published PR #584's gate counts unmarked, so the evidence set read as internally inconsistent — 85 vs 84 `openspec` items, 32 vs 31 active changes (Copilot) | `gates.md` read as this branch's record | each carried transcript carries a provenance banner naming its BASE, and a table of the three readings that differ by base rather than by disagreement | n/a — evidence, not code |

**THE FIX IS ONE STATE MACHINE, not two side by side**, and that is load-bearing:
a fenced block and a raw HTML block are MUTUALLY EXCLUSIVE in CommonMark — a
fence-shaped line inside an HTML block is content, an HTML opener inside a fence
is code — so two machines would each be wrong about the other's region.
`_opaque_state(line, state, after_paragraph)` decides both, and
`test_a_fenced_block_is_opaque_to_html_openers_and_the_reverse` pins both
directions.

**AND OVER-APPROXIMATION IS ITS OWN ESCAPE, in the same silent direction** —
which is the hole this fix could open, and the reason matching CommonMark is the
criterion rather than maximising suppression. A line of prose read as HTML
content would make a region opaque, swallow a real `## Notes` boundary, and
leave a declaration below it holding an entry it is not inside. So kind 6 is
CommonMark's own tag list and nothing wider, kind 7 demands a COMPLETE tag alone
on its line and may not interrupt a paragraph, and `<not a tag` opens nothing.
Five rows pin that direction, plus CommonMark's kind-6/kind-7 asymmetry, plus
the case where over-closing would REFUSE A CORRECTLY CONTAINED declaration (a
`## Notes` inside a real `<div>` block is content, so the declaration after the
block's blank line really is inside the entry).

### WHY THIS CLASS TERMINATES HERE, stated because three rounds of it have not

A phase error needs a line the reader calls a fence delimiter and CommonMark
does not, **at column 0 to 3**. Every construct that can hold such a line is now
accounted for:

| construct | how it is handled |
|---|---|
| another fenced block | this machine's own state |
| a raw HTML block | the eight kinds, this round |
| an indented code block | its content is at column 4+, which the `^ {0,3}` in every pattern here excludes |
| a block quote or a list item | its content carries the marker, so a bare fence at column 0 is a new block at document level — and a fence cannot be lazily continued |

Nothing else remains. **And the REVERSE error — missing a REAL fence at column 0
to 3 — cannot happen either**, because `_fence_opener` now rejects exactly what
CommonMark rejects there (a backtick fence whose info string carries a
backtick, and nothing else). The two halves together are what closes the class
rather than its fifth instance.

Counts after round 5: family file **110 passed**, `tests/doc-health`
**1475 passed, 0 failed**.

## § J — bot round 6: two holes ROUND 5's FIX opened, found by both bots independently

| # | escape (source) | on head `794675a0` | after | test |
|---|---|---|---|---|
| R6-1 | a kind 1 to 5 HTML block may open AND close on ONE line; returning the new state without testing that line kept it open past its own close (Codex P1, and Copilot the same) | `<!-- first -->` … `## Notes` … `<!-- second -->` → `entry='contract-v3.0'`, **ACCEPTED** — the first comment stayed open THROUGH the real heading and used the SECOND as its delayed close. Reproduced for comment, declaration, processing instruction, CDATA and `<pre>` | `entry=None` for all five | `test_an_html_block_that_closes_on_its_opening_line_swallows_nothing`, parametrized over the five |
| R6-2 | a shared kind-1 closer let `</script>` end a `<pre>` block, after which lines CommonMark still reads as `<pre>` content stopped being opaque (Codex P1, and Copilot the same) | `entry='contract-v3.0'` — **ACCEPTED** | nothing read; the state carries the tag that opened the block | `test_a_type_one_html_block_ends_only_on_its_own_closing_tag`, over all four tags |

**BOTH BOTS FOUND BOTH FINDINGS INDEPENDENTLY, within twenty-five minutes of
each other**, which is worth recording: the two reviewers agreeing on a precise
mechanism is a much stronger signal than either alone, and both were on the
round-5 fix rather than on anything older.

**And both fixes ship with the control for the hole THEY could open**, per the
standing discipline:

* requiring the MATCHING closer risks a `<pre>` block that never closes
  swallowing the rest of the document — pinned as
  `test_an_unclosed_type_one_block_is_opaque_to_the_end_and_that_is_safe`,
  which also records WHY that is acceptable: an unclosed block loses every
  boundary after it, but loses every declaration too, so the superseded `error`
  stands rather than being quieted. The trade is a decision, not an accident.
* closing on the opening line risks closing too eagerly — pinned by the case
  where a boundary AFTER a mismatched closer is still `<pre>` CONTENT, so a
  declaration below the real `</pre>` is still inside the entry. Over-closing
  there would REFUSE a correctly contained declaration.

Counts after round 6: family file **117 passed**, `tests/doc-health`
**1482 passed, 0 failed**.

## § K — the DIFFERENTIAL, and the escape that a bot round PUT THERE

After round 8 the reader's boundary decisions were run as a **differential
against a reference CommonMark implementation** (markdown-it-py 3.0.0), over
**31 constructs — every shape this branch has touched**. The question asked of
both, per document: *is this line a heading?* — which is exactly the question
containment turns on.

markdown-it-py is a **measuring instrument in a scratch probe only**. It is not
imported by `doc_health`, which is stdlib-only, it is not added to any test, and
it is not a dependency of this repository.

### The instrument had to be fixed before it could be trusted

The first harness searched for the literal text `## Notes` and split documents
with Python's `splitlines()`. It reported **six** disagreements, of which
**five were its own**: `splitlines()` broke on U+2028 and shifted the line
index, and `.strip().startswith("## Notes")` missed `##\tNotes` and `# Notes`.
Worse, two probe files had been written with LITERAL U+00A0 and U+2028 that
were **normalised to plain spaces on write** — so those rows tested nothing
they claimed to. That is the round-3 lesson (`NBSP` named rather than typed)
arriving a second time, in the probes rather than the tests. The corrected
harness is index-based and uses escapes.

**A measuring instrument that can report a disagreement it invented is worth
less than none**, and the correction is recorded rather than quietly applied.

### What the corrected differential found: 31 constructs, 3 disagreements

| disagreement | verdict |
|---|---|
| `### subsection` does not close an entry | **DELIBERATE and load-bearing.** This repository's live declaration sits inside a ``### `contract-v2.6` disposition`` subsection of the `contract-v3.0` entry; a rule that closed on `###` would refuse the declaration that makes `main` green. Documented at `_ATX_BOUNDARY` since round 0. |
| `<pre<U+00A0>x>` opens a block for markdown-it but not here | **NOT A DEFECT, and the two reference implementations disagree with each other.** markdown-it uses `\s`, which admits U+00A0; CommonMark's *whitespace character* is space, tab, newline, VT, FF or CR, and cmark-gfm — **which is what renders this document on GitHub** — follows the letter. This reader agrees with the spec and with the renderer, and the direction is OVER-closing (a false refusal), not an accept. It is the same call as round 7's refused half, now with a sharper measurement. |
| **`</script>` does not end a `<pre>` block** | **A REAL ESCAPE, LIVE IN THE PUSHED HEAD, AND A BOT ROUND PUT IT THERE.** |

### The third one, in full, because it is the finding above every other finding

CommonMark's end condition for a kind-1 HTML block reads, in words:

> *line contains an end tag `</script>`, `</pre>`, `</style>`, or `</textarea>`
> (case-insensitive; **it need not match the start tag**).*

**Round 6 shipped the opposite.** Codex and Copilot INDEPENDENTLY asked for a
matching closer, twenty-five minutes apart, and § J recorded their agreement as
*"a much stronger signal than either alone"*. **Both were wrong on the
specification, and the fix they asked for INTRODUCED the very escape class it
claimed to close**: requiring `</pre>` made this reader MORE OPAQUE than
CommonMark, so a real `## Notes` heading after a `</script>` was swallowed and
the declaration below it was **ACCEPTED** under an entry it is not inside.

Measured at the pushed head `9a6902ad`:

```text
## contract-v2.6 — an earlier cut

## contract-v3.0 — a cut

<pre>
</script>          <- CommonMark ENDS the block here
## Notes           <- ...so this really is a heading
</pre>

**SPENT BUNDLE:** `contract-v2.6` — SUPERSEDED BY `contract-v3.0` — …
```

`entry='contract-v3.0'` — **ACCEPTED**. After the revert: `entry=None`,
refused, and the superseded `error` stands.

**What it cost to find: nothing a bot round produced.** Both bots had reviewed
that fix on two later heads and neither retracted it. It surfaced only under the
differential. **Bot agreement is not evidence about a specification.** The
matching-closer rule is reverted, the test that asserted it is replaced by one
that asserts the spec's rule over all sixteen opener/closer pairs, and the
control that the block still runs on when there is no end tag at all ships with
it.

**This is the decision point for variant B, and it is a stronger argument than
the tail's length was.** The case against hand-modelling CommonMark here is no
longer *"the edge cases keep coming"* — it is that **a round of this tail
introduced a containment escape that two independent reviewers endorsed**, and
that only an oracle outside the review loop caught it. Variant B needs no such
oracle: it recognizes a raw-HTML opener and refuses, so a construct the reader
cannot parse can never quiet a finding, whatever a renderer makes of it.

## § L — raw HTML: FAIL CLOSED BY RULING

*(Lettered L rather than K because § K above — the differential — already took
that letter when the revert landed.)*

**THE RULING, VERBATIM.**

> RULING for lane openxfactory-1d's PR #589: **VARIANT B — fail closed on raw
> HTML.** The reader parses NO raw-HTML blocks. Fenced code (``` / ~~~) stays
> the ONLY opaque region. A top-level raw-HTML block opener in
> `contracts/CHANGELOG.md` (any CommonMark kind 1–7 start condition, at ≤3
> leading spaces, outside a fence) makes the family emit ONE `contested`
> `error` on the changelog naming the line ("unparseable construct: raw HTML;
> the SPENT reader refuses to read past it"), read NO declaration below that
> line, and leave declarations ABOVE it standing; the
> superseded-and-never-published `error` for any bundle whose declaration was
> below the opener stands beside it.
>
> — Brett Heap, 2026-09-03

### The probe: an opener stops the read, and the superseded `error` stands

Seven documents, each ending in the SAME well-formed and correctly contained
declaration, read at the pushed head `e19bb2a4` (the fidelity reading, with the
§ K revert in it) and at this head:

| # | document | at `e19bb2a4` | at this head |
|---|---|---|---|
| P1 | the § K escape — `</script>` ends a `<pre>`, so `## Notes` is a real heading | `entry=None` (refused, post-revert) | **read stops at line 5 `'<pre>'`** — nothing read |
| P2 | round 5's out-of-phase document — a ```-shaped line inside `<pre>` | nothing read | **read stops at line 3 `'<pre>'`** — nothing read, and now REPORTED |
| P3 | a plain `<div>` block above the declaration | `entry='contract-v3.0'` — ACCEPTED | **read stops at line 3 `'<div>'`** — nothing read |
| P4 | `<!doctype html>` above the declaration | `entry='contract-v3.0'` — ACCEPTED | **read stops at line 3** — nothing read |
| P5 | a bare `<mytag>` below paragraph content | `entry='contract-v3.0'` — ACCEPTED | **read stops at line 4** — nothing read |
| P6 | *control* — an opener shown inside a FENCE | `entry='contract-v3.0'` | `entry='contract-v3.0'`, read not stopped |
| P7 | *control* — prose that merely names `` `<pre>` `` | `entry='contract-v3.0'` | `entry='contract-v3.0'`, read not stopped |

**P3 TO P5 ARE THE COST, AND THEY ARE NOT DEFECTS BEING FIXED — they are
documents this family now refuses that CommonMark reads.** Stated plainly
because the ruling's whole claim is about DIRECTION, not about fidelity: P3 is a
declaration a renderer really does place inside its entry, and the family now
declines to read it. What that buys is that no arrangement of raw HTML can
produce the other error, the silent one — a declaration read under an entry it
is not in. The repair is one line long (move the declaration above the HTML, or
take the HTML out) and the finding says so.

**And the refusal is REPORTED**, which is the other half. Both findings, measured
on a fixture whose changelog is `<div>` + blank + the declaration:

```text
[error] contracts/CHANGELOG.md   resolution=contested
    contracts/CHANGELOG.md line 7 carries an UNPARSEABLE CONSTRUCT: RAW HTML
    ('<div>') — this family reads the changelog as CommonMark PROSE and does not
    model raw HTML blocks, so the SPENT reader REFUSES TO READ PAST it rather
    than guess at what a renderer makes of the lines below. No SPENT declaration
    below this line is read, which means any bundle a declaration there would
    have quieted goes on being reported
[error] contracts/manifest.yaml   resolution=auto-fixable
    contract-v2.6 was cut and SUPERSEDED without ever being published: …
```

**ONE changelog `error`, `contested`, naming the line — and the superseded
`error` standing beside it.** That is the ruling's shape exactly, and
`test_raw_html_is_one_contested_error_on_the_changelog` asserts all of it
including the absence of any `info`: nothing was quieted.

### What came out, and what went in

**REMOVED — 11 test functions, 29 parametrized cases, of CommonMark
raw-HTML-fidelity behaviour.** They tested a machine that no longer exists;
keeping them would have been keeping the parser.

| removed test | what it pinned |
|---|---|
| `test_a_fence_shaped_line_inside_raw_html_opens_no_fence` (×8) | § I R5-1 — the eight-kind opacity table |
| `test_over_approximating_an_html_block_is_its_own_escape` (×5) | § I — the over-approximation direction |
| `test_kind_7_cannot_interrupt_a_paragraph_and_kind_6_can` | CommonMark's kind-6/kind-7 asymmetry |
| `test_a_declaration_inside_a_raw_html_block_is_not_a_record` | the declaration-inside-`<pre>` rule |
| `test_a_fenced_block_is_opaque_to_html_openers_and_the_reverse` | fence/HTML mutual exclusion |
| `test_an_html_block_that_closes_on_its_opening_line_swallows_nothing` (×5) | § J R6-1 — the single-line block |
| `test_a_type_one_html_block_ends_on_ANY_of_the_four_end_tags` (16 pairs) | § K — the spec's own kind-1 end condition |
| `test_an_unclosed_type_one_block_is_opaque_to_the_end_and_that_is_safe` | the unclosed-block-to-EOF trade |
| `test_a_type_one_opener_admits_every_commonmark_space` (×4) | round 7 — VT and FF in the kind-1 opener |
| `test_a_unicode_space_after_a_type_one_tag_opens_no_block` | round 7's refused half — U+00A0 |
| `test_a_kind_four_declaration_needs_an_uppercase_letter` | round 7 — GFM 0.29's uppercase kind 4 |

The code they covered went with them: `_HTML_TYPE1_OPEN`, `_HTML_OPENERS`,
`_HTML_CLOSERS`, `_HTML_TYPE7`, `_html_opener`, `_html_closed` and the unified
`_opaque_state`. `_fence_state` — which `_opaque_state` had absorbed in round
5 — is restored, because fences are again the only region there is.

**ADDED — 7 test functions, 22 cases, of fail-closed behaviour**: a twelve-row
opener table each row carrying its own control (the identical declaration
WITHOUT the opener is accepted, so each row is about the HTML and not about the
fixture), a five-row not-an-opener table, the fenced-example rule,
declarations-above-the-opener, the reported `error` with the superseded `error`
beside it, the kind-7 widening, and **a live check that this estate's changelog
carries no raw HTML at all** — which is what makes the refusal free today and
red the day it would stop being.

### Two narrowings this branch had already made are REVERSED, deliberately

Both were taken as findings; both are given back, because the direction of the
safe error inverted under the ruling and an opener this reader fails to
recognize is one it reads PAST.

| narrowing | round | why it was right | why it is now wrong |
|---|---|---|---|
| kind 4 needs an UPPERCASE letter (GFM 0.29) | 7 | accepting `<!doctype` made the reader MORE OPAQUE than GitHub's renderer, which swallowed boundaries silently | if cmark-gfm moves to CommonMark 0.30 — which relaxed the rule — an uppercase-only reader reads PAST a real block. The superset is the safe side now, and it is written as an explicit `[A-Za-z]` rather than left to the `re.I` flag |
| kind 7 may not interrupt a paragraph | 5 | a line of prose ending in a bare tag is prose, and calling it a block swallowed the boundary below | knowing whether a paragraph is open is parser state, which this reading gives up. The cost is one more VISIBLE error (P5); the cost of the alternative was a SILENT accept |

The patterns are still CommonMark's wherever CommonMark is unambiguous — a
finding a reader cannot predict is its own defect — and the five-row
not-an-opener table pins that a changelog merely MENTIONING `` `<pre>` `` in a
sentence is never refused.

Counts after the ruling: family file **120 passed** (127 → 120: −29 removed,
+22 added), `tests/doc-health` **1485 passed, 0 failed** — collected 1492 → 1485
for the same −7. The total sits above § J's 1482 because `main` has advanced
under this branch and its own suite grew, not because this PR added seven: on
`origin/main` at `642ac147` the same two commands read **1411** and **46**, and
1411 − 46 + 120 = 1485 exactly.

## § M — bot round 11: the blank-line test was still Python's

**Copilot, on the ruling's head `218b63a7`, and it is ROUND 3'S LESSON ARRIVING
IN A PREDICATE RATHER THAN IN A PATTERN.** Round 3 replaced `\s` with
CommonMark's own class in the ATX and fence patterns; `_paragraph_line`'s
blankness test was still `not line.strip()`, and `str.strip()` strips every
Unicode space.

CommonMark's blank line is *"a line containing no characters, or a line
containing only spaces (U+0020) or tabs (U+0009)"*. A line holding only U+00A0
is therefore **paragraph content**, the run of `=` below it is a Setext
underline, and that heading CLOSES the entry.

| # | escape (source) | on head `218b63a7` | after | test |
|---|---|---|---|---|
| R11-1 | a line of Unicode space read as BLANK, so `after_paragraph` went false and the `===` below it stopped being a Setext underline (Copilot) | `entry='contract-v3.0'` — **ACCEPTED**, for U+00A0, U+2028, VT and FF, and for each of them INSIDE a paragraph as well as alone | `entry=None` for all eight | `test_a_line_of_unicode_space_is_paragraph_content_not_a_blank_line`, parametrized over the four |

**It is an UNDER-CLOSING escape**, which is the direction this whole guard
exists to close, and it survived ten rounds because it hid in the one predicate
nobody had re-read after round 3 — the pattern audit found the patterns.

**And the fix ships with the control for the hole IT could open**, per the
standing discipline: a blankness test narrowed past CommonMark would make an
indented empty line paragraph content, so a `===` below one would close an entry
CommonMark keeps open — a FALSE REFUSAL of a correctly contained declaration.
`strip(" \t")` is exactly CommonMark's class and nothing narrower, pinned by
`test_a_line_of_spaces_or_tabs_is_still_a_blank_line` over empty, spaces, tabs
and a mixture.

**Note the asymmetry with `_lines`, which is not an inconsistency**: VT and FF
are not line endings (§ H, round 4) and they are not blank-line characters
either — so a VT-only line is ONE line, and it is a PARAGRAPH.

Counts after round 11: family file **128 passed** (120 → 128), `tests/doc-health`
**1493 passed, 0 failed**.
