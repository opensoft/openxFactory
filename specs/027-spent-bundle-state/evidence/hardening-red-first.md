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
