# Phase 0 Research: split-openxwallet-repo §1 bookkeeping

**Feature**: `016-openxwallet-split-bookkeeping` | **Date**: 2026-08-26

No `NEEDS CLARIFICATION` markers existed in the spec, so Phase 0 is not a
decision phase. Its work is to **locate and pin every source text** so
implementation is transcription with a citable origin, and to establish the
doc-health baseline that task 1.10's evidence note depends on.

All line references are against openxFactory `main` at `5ef6d8d2` (the merge of
PR opensoft/openxFactory#391).

---

## R0 — The authority chain, and what it forecloses

**Decision**: `openspec/changes/split-openxwallet-repo/proposal.md` at `5ef6d8d2`
is the sole authority for every text this feature writes. Its header carries
`Status: ratified` and `Ratified: 2026-08-26 by Brett Heap (openxFactory operator
authority) — in-session ruling on PR #391 after both required checks passed`,
plus the direction that realization proceeds "per tasks.md through Speckit
features, §1 and P5a.1 first".

**Rationale**: the proposal quotes both amendments in full, in a section titled
"What this change RATIFIES (its own diff)", explicitly so "the bench reviews text
rather than intent". That authorial choice is a constraint on this feature: the
diff is meant to be checkable against text, so any deviation — however
stylistically better — destroys the property the ratification was granted on.

**Alternatives considered**:

- *Re-derive the amendment wording from R1 and the design's dispositions.*
  Rejected: it would produce a text no reviewer could diff against anything, and
  it re-opens a ratified decision.
- *Ask Brett to confirm the wording before writing.* Rejected: the wording is
  already his ratified ruling. A confirmation round would add latency and invite
  drift, and the assignment forbids blocking on a human here.

**Also confirmed — the edits are inside the declared code surface.** The
proposal's `code_surface` front-matter names `docs/openxdox-naming.md` under
openxFactory (item 2) and `CLAUDE.md` under "The xFactory aggregation" (item 4).
Neither edit exceeds what the ratification authorized.

---

## R1 — Amendment 2's verbatim text and its insertion point

**Location of the source**: `proposal.md:234-258`, introduced by
"4. **Amendment 2 to `docs/openxdox-naming.md`**, in Amendment 1's shape
(`:84-100`)" and carried as a blockquote.

**Insertion point**: `docs/openxdox-naming.md` is 109 lines. `## Amendment 1 —
the public host (2026-08-14)` begins at line 84 and runs to end of file, so
Amendment 2 is **appended after line 109** — the file's new final section. This
matches the proposal's instruction "appended after Amendment 1".

**Decision**: transcribe the three quoted paragraphs under the heading
`## Amendment 2 — openXwallet leaves the exception list (2026-08-26)`,
un-blockquoting them (the `> ` prefixes are the proposal's quoting mechanism, not
part of the text) and preserving paragraph breaks, emphasis and code spans
exactly. Wrap prose at the file's prevailing ~79-column width.

**The three paragraphs carry three distinct facts**, all required by FR-002:

1. The ruling — `openxWallet` → `openXwallet` on the house `openX<type>` form, by
   R1 of `split-openxwallet-repo`, Brett's ruling of 2026-08-26, with the reason
   (a brand created under a spelling this record calls an exception would ratify
   the exception a second time).
2. The wire label stays lowercase, by this record's own brand-versus-label rule —
   and, in the same paragraph, `openXwallet-Install` registered as a NAME with no
   repository created (Q4).
3. The "amended rather than rewritten" closing paragraph.

**Rationale for un-blockquoting rather than nesting**: Amendment 1 is body prose,
not a blockquote. "In Amendment 1's shape" therefore means body prose. A nested
blockquote would render as a quotation of the record inside the record.

---

## R2 — Amendment 1 as the shape precedent, including what it did *not* do

**Decision**: follow Amendment 1 (`docs/openxdox-naming.md:84-109`) on four
points: a `## Amendment N — <subject> (<date>)` heading with an em dash and a
parenthesised ISO-ish date; a bolded lead sentence stating the substantive change;
body prose stating the ruling's origin and reasoning; and a closing paragraph
beginning "The record above is amended rather than rewritten:" that says why the
earlier text still stands.

**The load-bearing negative**: Amendment 1 changed **no line of the lifecycle
header**. It added no `Amended:` line, no second `Ratified by:`, no date field.
The header still reads `Status: ratified` / `Ratified by:
add-dispatch-credential-contract`.

**Rationale — this is required, not merely precedented.**
`docs/document-lifecycle.md` § "Status Claim Rules" states that a `ratified`
header "names its ratification on exactly ONE citation line in the lifecycle
header … never two lines (not one of each spelling, and not the same spelling
twice)", because "two lines each claiming to name the ratification say nothing
about which is current". Adding an `Amended:`/`Ratified:` line for Amendment 2
would therefore *create* a doc-health finding on a file this feature is supposed
to leave finding-free (FR-005, FR-016).

**Alternatives considered**:

- *Add `Amended: 2026-08-26 by split-openxwallet-repo` to the header.* Rejected —
  see above; it risks a second-citation violation, and Amendment 1 sets the
  contrary precedent. The dated section heading already carries the provenance.
- *Change `Ratified by:` to name `split-openxwallet-repo`.* Rejected: it would
  falsify the record's actual ratification (`add-dispatch-credential-contract`,
  which ratified the *name*), and an amendment is not a re-ratification.

---

## R3 — The inline pointer: one site, and why a token patch fails

**Location of the source**: `proposal.md:261-265`, quoted in both directions.

**The site**: `docs/openxdox-naming.md:23-25`, in § Decision:

```text
- **Capability name:** `openXdox` — house `openX<type>` capital-X form (the
  lowercase `openxFactory` / `openxWallet` spellings are the family
  exceptions, not the rule).
```

**Bounding fact**: `grep -n 'openxWallet' docs/openxdox-naming.md` returns
**exactly one** line — line 24. Edit (b) is therefore a single-site edit with no
risk of a missed occurrence elsewhere in the record.

**Decision**: replace the parenthetical with the proposal's verbatim "after"
text — "(the lowercase `openxFactory` spelling is the family exception, not the
rule; `openXwallet` left this list in Amendment 2)" — re-wrapping the three-line
bullet as needed.

**Rationale**: three words change number together — `spellings` → `spelling`,
`are` → `is`, `exceptions` → `exception` — and a clause is appended pointing at
Amendment 2 so the record self-navigates. Deleting the `` / `openxWallet` ``
token alone would leave "the lowercase `openxFactory` spellings **are** the
family **exceptions**": plural agreement on a singular subject, inside a
`ratified` record. This is exactly the trap `tasks.md` 1.11(b) warns of ("A
mechanical substitution there leaves a `ratified` record ungrammatical").

**Alternatives considered**:

- *`sed 's| / `openxWallet`||'`.* Rejected — produces the ungrammatical result
  above. The edit must be a sentence rewrite.
- *Drop the parenthetical entirely.* Rejected: it deletes standing record text
  (violating amend-never-rewrite) and loses the `openxFactory` exception, which
  is still true.

---

## R4 — The working-rule replacement text

**Location of the source**: `proposal.md:266-283`, quoting the rule in both
directions.

**Target**: `/home/brett/projects/xFactory/CLAUDE.md` § "Working rules" item 1,
currently at lines 61-62 of that file (verified in the amendment worktree):

```text
1. Domain-neutral contracts live ONLY in `openxFactory`; domain repos pin the
   openxFactory version they consume in their `stack.yaml`.
```

**Decision**: replace with the proposal's verbatim replacement (`proposal.md:276-279`):

```text
1. Domain-neutral contracts live in `openxFactory` or in a neutral `open*`
   product repository that `openxFactory` pins by commit and digest; domain
   repos never author neutral contracts, and every consumer pins the
   openxFactory version it consumes in its `stack.yaml`.
```

**Rationale**: the rewrite is a falsifiability improvement, not a loosening. The
old rule stated one absolute (`ONLY in openxFactory`) that the shed makes false,
and left the actually-invariant prohibition implicit. The replacement drops the
false absolute, states the surviving prohibition explicitly ("domain repos never
author neutral contracts"), and generalizes the pin obligation from "domain
repos" to "every consumer" — which is what the neutral-product-pin capability
requires, since openxFactory itself becomes a consumer of openXwallet.

**Timing, recorded rather than discovered**: until P4 lands, the *old* rule is
the one in force and this change contradicts it. The proposal states this
deliberately ("stated here rather than discovered later"), so the amendment lands
now, at §1, and is not deferred to P4. This feature must not "improve" on that by
holding the edit back.

**Alternatives considered**:

- *Defer the edit until P4.* Rejected: §1 explicitly claims it as "THIS CHANGE'S
  OWN DIFF per the RATIFIES list", and the proposal already dispositioned the
  interim contradiction.
- *Edit the shared checkout `/home/brett/projects/xFactory` in place.* Rejected:
  a shared multi-session checkout. A dedicated worktree plus an explicit-pathspec
  commit is the repo's own documented discipline (working rule #2).

---

## R5 — Task 1.10's measurement: what "no new findings" actually resolves to

**Baseline established** (`python3 scripts/doc-health.py --single-repo .`, same
command both sides, single-repo scope):

| Tree | Commit | Findings |
|------|--------|----------|
| Before the packet | `5ef6d8d2^1` = `64486a51` | 5 critical, 6 error, 41 warning, 4 info |
| After the packet | `5ef6d8d2` | 5 critical, 7 error, 41 warning, 4 info |

**The differential is exactly one finding**, present after and absent before:

```text
severity=error family=location-conformance
path=ideation/staging/openxwallet-neutral-home/openxwallet-neutral-home.md
rule="staged material already cites proposal split-openxwallet-repo"
action="move selected material into the proposal supporting-docs folder"
class="contested"
```

**Decision**: tick 1.10, with an evidence note that records the counts, names
this finding, and states why it is outside 1.10's scope and outside §1's
authority to remedy. Do **not** claim an unconditional green, and do **not**
remedy the finding.

**Rationale**:

- *In scope, and clean.* Task 1.10's own wording bounds it to "no new finding
  attributable to **this change directory or the README entry**". The change
  directory `openspec/changes/split-openxwallet-repo/` draws zero findings, and
  the README entry added by task 1.9 draws zero. On its stated terms, 1.10
  passes.
- *Why the finding fires at all.* `scripts/doc_health/families.py:547-553`
  (`fam_location_conformance`) emits it when a `staged` document under
  `ideation/staging/` cites a change id that now exists on disk. It is the
  standard staged-topic-exit signal: the topic named its exit change, the change
  packet was created, so the checker asks that the selected material move into
  `supporting-docs/`. It is triggered by the packet's *existence*, not by any
  defect in it.
- *Why not remedy it here.* The remedy is a lifecycle act on a staged topic —
  moving material out of `ideation/staging/openxwallet-neutral-home/`. §1
  authorizes no such act, the topic is still the reference for successors §2–§12,
  and the finding's class is `contested`, which Principle V says is resolved "by
  a cited OpenSpec change or a recorded disposition, never by silent edits". An
  unauthorized move would be exactly the silent edit that rule forbids.
- *Why not leave 1.10 unticked.* An unticked box that was in fact measured is
  indistinguishable from work never done, which is the defect §1's ledger exists
  to prevent. The honest form is a tick whose note carries the real numbers and
  names the one finding.

**Alternatives considered**:

- *Move the staged material into `supporting-docs/` to force zero.* Rejected as
  out of scope and as a silent resolution of a contested finding.
- *Record a disposition in `health/dispositions.yaml`.* Rejected: that file does
  not exist in this tree (only `health/derive-possibles`,
  `health/ideation-readiness`, `health/neutrality-drift` do), and creating a
  dispositions register is a governance act well beyond §1.
- *Tick 1.10 saying "green".* Rejected as false-in-spirit: a reviewer reading
  "green" would not learn that the packet's landing moved the error count from 6
  to 7.

---

## R6 — Task 1.1's stale trailing clause

**The site**: `tasks.md:37` — task 1.1 ends "`Status: draft`." The proposal's
header now reads `Status: ratified` with a `Ratified:` provenance line and a
`## Ratification record, 2026-08-26`, as task 1.13 itself records two entries
below.

**Decision**: replace the trailing `` `Status: draft`. `` with a clause naming
the header's actual state — `Status: ratified` with its `Ratified:` provenance
line — noting that the clause described the header as authored and that the
ratification recorded at 1.13 superseded it.

**Rationale**: 1.1 is a description of what the proposal carries. Leaving a
falsified clause inside the ledger of a ratified change is the same defect class
as the naming record's contradiction — canon disagreeing with itself. The
correction touches only the trailing clause: R1–R8 are not renumbered and the
LOCKED block is untouched (FR-010).

**Alternatives considered**:

- *Leave it, as a historical artifact.* Rejected: `tasks.md` is a live ledger,
  not a frozen record; the assignment flags this clause explicitly as a leftover
  to fix.
- *Delete the clause.* Rejected: the status of the proposal is a fact 1.1 was
  written to carry. Correcting it preserves the information; deleting it loses it.

---

## R7 — Gate commands, fixed for reproducibility

**Decision**: the two gates this feature must show green, run from the feature
worktree root:

```bash
OPENSPEC_TELEMETRY=0 openspec validate --all --strict
python3 scripts/doc-health.py --single-repo .
```

**Baseline for the first**: already verified on the branch base — `Totals: 77
passed, 0 failed (77 items)`.

**Comparison rule for the second**: this feature's post-edit run is compared
against the run on its own base commit (`5ef6d8d2`, the R5 table's second row:
5 critical / 7 error / 41 warning / 4 info). Equality on every family this
feature's files belong to is the pass condition (FR-016, SC-007).

**Note on `scripts/validate-docs*`**: openxFactory has no `validate-docs.sh` —
that is codexFactory's validator. openxFactory's equivalents are
`scripts/validate-*.py`, none of which govern `docs/` prose or the README index;
this feature adds no new document to the doc tree, so the README-index rule
(Principle IV) does not fire and no README edit is expected (FR-014).
