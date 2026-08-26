# Phase 1 Data Model: split-openxwallet-repo §1 bookkeeping

**Feature**: `016-openxwallet-split-bookkeeping` | **Date**: 2026-08-26

This feature has no runtime data model. Its "entities" are the four **edit
sites** — each with a fixed before-state, a fixed after-state taken from ratified
text, an authority citation, and invariants a reviewer can check. Modelling them
this way is what makes the implementation mechanically verifiable: every site
below is a closed comparison, not a judgment.

---

## E1 — `docs/openxdox-naming.md` § Amendment 2 (new section)

| Attribute | Value |
|-----------|-------|
| Repository | openxFactory |
| Path | `docs/openxdox-naming.md` |
| Site | appended after line 109 (end of file, after Amendment 1) |
| Operation | **ADD** — a new final section |
| Authority | `openspec/changes/split-openxwallet-repo/proposal.md:234-258` |
| Realizes | task 1.11(a); FR-001, FR-002, FR-003 |

**Before**: file ends with Amendment 1's closing paragraph
("… the live-mode edge validators fail until that reissue lands, by design.").

**After**: same, plus a blank line and the new section, whose required content is:

- **Heading**: `## Amendment 2 — openXwallet leaves the exception list (2026-08-26)`
- **Paragraph 1** — the ruling: `openxWallet` becomes `openXwallet`, the house
  `openX<type>` capital-X form; Brett's ruling of 2026-08-26 (R1 of
  `split-openxwallet-repo`); taken because the product is getting its own
  repository and brand at `opensoft/openXwallet`, and a brand created under a
  spelling this record lists as an exception would ratify the exception a second
  time.
- **Paragraph 2** — the label and the registered name: the wire label stays
  LOWERCASE (`openxwallet` capability ids, the `xfactory_wallet_*` kind prefix,
  paths and finding codes untouched), because that is this record's own rule —
  the brand and the label differ by design and this is not a spelling to
  reconcile; and `openXwallet-Install` is registered as a NAME here with no
  repository created (Q4).
- **Paragraph 3** — the amend-not-rewrite closing: `openxWallet` was genuinely a
  family exception when the form was locked on 2026-08-13, the short-handle
  argument that cited it still holds, and only the brand moved.

**Invariants**:

- Body text is byte-identical to the proposal's blockquote with `> ` markers
  stripped; only line wrapping may differ.
- Section is the file's last; nothing is inserted between Amendment 1 and it.
- Prose is body prose, not a blockquote (Amendment 1's shape).

---

## E2 — `docs/openxdox-naming.md` § Decision inline pointer

| Attribute | Value |
|-----------|-------|
| Repository | openxFactory |
| Path | `docs/openxdox-naming.md` |
| Site | lines 23-25, the `- **Capability name:**` bullet |
| Operation | **REPLACE** — one parenthetical, rewritten as a sentence |
| Authority | `proposal.md:261-265` (quoted before *and* after) |
| Realizes | task 1.11(b); FR-004 |

**Before** (verbatim, 3 lines):

```text
- **Capability name:** `openXdox` — house `openX<type>` capital-X form (the
  lowercase `openxFactory` / `openxWallet` spellings are the family
  exceptions, not the rule).
```

**After** — the parenthetical becomes "(the lowercase `openxFactory` spelling is
the family exception, not the rule; `openXwallet` left this list in Amendment 2)",
re-wrapped to the file's width.

**Invariants**:

- Singular throughout: `spelling`, `is`, `exception`.
- The `openXdox` / `openX<type>` lead clause is unchanged.
- `openxFactory` survives as the one named exception.
- Exactly one site: before the edit the record contains exactly one
  `openxWallet` occurrence (line 24), so after the edit the record body above
  Amendment 2 contains **zero**. Amendment 2 itself legitimately names the
  retired spelling twice, as history — that is the ratified text and must stay.

---

## E3 — xFactory `CLAUDE.md` § "Working rules" item 1

| Attribute | Value |
|-----------|-------|
| Repository | `opensoft/xFactory` (aggregation superproject) |
| Path | `CLAUDE.md` |
| Site | lines 61-62 |
| Operation | **REPLACE** — rule 1 only |
| Authority | `proposal.md:266-283`, replacement text at `:276-279` |
| Realizes | task 1.12; FR-006, FR-007, FR-008, FR-009 |

**Before** (verbatim, 2 lines):

```text
1. Domain-neutral contracts live ONLY in `openxFactory`; domain repos pin the
   openxFactory version they consume in their `stack.yaml`.
```

**After** (verbatim from the proposal, 4 lines):

```text
1. Domain-neutral contracts live in `openxFactory` or in a neutral `open*`
   product repository that `openxFactory` pins by commit and digest; domain
   repos never author neutral contracts, and every consumer pins the
   openxFactory version it consumes in its `stack.yaml`.
```

**Invariants**:

- `## Working rules` heading unchanged; rules 2 onward byte-identical.
- No other file in the aggregation repo is modified — in particular no
  `.gitmodules`, no gitlink, no submodule pin.
- Delivered as an **open** pull request; never merged by this feature.

**State transition**: the rule moves from *false-as-written-once-P4-lands* to
*true across the whole wave*, at the cost of being permissive before the neutral
product repository exists. The ratified proposal dispositions that interim
window explicitly, so it is an accepted state, not a defect.

---

## E4 — `openspec/changes/split-openxwallet-repo/tasks.md` §1 ledger

| Attribute | Value |
|-----------|-------|
| Repository | openxFactory |
| Path | `openspec/changes/split-openxwallet-repo/tasks.md` |
| Sites | line 37 (task 1.1's trailing clause); line 88 (task 1.10's box + note); line 91 (task 1.11's box + note); line 103 (task 1.12's box + note) |
| Operation | **REPLACE** (1.1's clause) and **TICK + ANNOTATE** (1.10, 1.11, 1.12) |
| Authority | the ratified proposal header for 1.1; this feature's own evidence for the ticks |
| Realizes | tasks 1.1, 1.10; FR-010 through FR-014 |

**Sub-entity E4a — task 1.1's trailing clause**

- **Before**: `` … the successors named. `Status: draft`. ``
- **After**: a clause naming the header's real state — `Status: ratified` with
  its `Ratified:` provenance line — and noting that `draft` described the header
  as authored, superseded by the ratification recorded at 1.13.
- **Invariants**: R1–R8 not renumbered; the LOCKED constraint block untouched;
  only the trailing clause changes.

**Sub-entity E4b — task 1.10's box and evidence note**

- **Before**: `- [ ] 1.10 …`
- **After**: `- [x] 1.10 …` plus an evidence note carrying the R5 measurement:
  the two commits compared (`5ef6d8d2^1` = `64486a51` and `5ef6d8d2`), both
  finding counts (5/6/41/4 → 5/7/41/4), and the single differential finding named
  by family (`location-conformance`), path
  (`ideation/staging/openxwallet-neutral-home/…`) and class (`contested`), with
  the statement that it falls outside 1.10's stated scope and outside §1's
  authority to remedy.
- **Invariants**: the note reports the measurement, not a verdict; it must not
  read as an unconditional green.

**Sub-entity E4c — tasks 1.11 and 1.12's boxes and evidence notes**

- **Before**: `- [ ] 1.11 …`, `- [ ] 1.12 …`
- **After**: ticked, each with a trailing note naming the file changed and the
  commit or PR carrying it, in the shape §1's already-ticked entries use
  (e.g. `(PR #391, 2026-08-26)`).

**Invariants across E4**:

- Not one box in §2–§12 is ticked; no successor's text changes.
- Every §1 box is ticked when the feature completes (SC-005).
- Each newly ticked box's note resolves to a file and a commit or PR without
  asking the author (SC-006).

---

## Cross-entity relationships and ordering

```text
E1 ─┐
    ├─(both in docs/openxdox-naming.md, one commit)─→ recorded by ─→ E4c (1.11)
E2 ─┘

E3 (separate repo, separate PR) ──────────────────→ recorded by ─→ E4c (1.12)

R5 measurement (Phase 0, already performed) ──────→ recorded by ─→ E4b (1.10)

Proposal header (already ratified) ───────────────→ corrected in ─→ E4a (1.1)
```

- **E1 and E2 are one file and land together** in a single edit pass; splitting
  them would leave the record momentarily self-contradictory (a pointer naming
  two exceptions beside an amendment saying there is one).
- **E3 is independent of E1/E2.** Different repository, different PR, no ordering
  dependency either way. This is why the spec's two P1 stories are each
  independently valuable.
- **E4 is strictly last**, because it records the outcomes of E1–E3 and must cite
  their commit or PR.

## Validation rules (derived from requirements)

| Rule | Source | Check |
|------|--------|-------|
| Amendment 2 body matches ratified text | FR-001, SC-002 | diff against `proposal.md:236-258` with `> ` stripped |
| Inline pointer matches ratified "after" | FR-004, SC-002 | diff against `proposal.md:264-265` |
| Record amended, not rewritten | FR-005, SC-003 | `git diff` shows only an append plus the E2 bullet |
| Lifecycle header untouched, one citation line | FR-005, R2 | header lines byte-identical; no `Amended:` added |
| Working rule matches ratified replacement | FR-006, SC-004 | diff against `proposal.md:276-279` |
| Aggregation diff is one file, one rule | FR-009, SC-004 | `git diff --stat` shows `CLAUDE.md` only |
| Successors untouched | FR-013, SC-005 | no `- [x]` appears in §2–§12 |
| Ticks carry resolvable evidence | FR-012, SC-006 | each new note names a file and a commit/PR |
| OpenSpec strict-validates | FR-015, SC-007 | `openspec validate --all --strict` → 0 failed |
| No new doc-health finding | FR-016, SC-007 | counts equal the base commit's for affected families |
| Both PRs open | FR-017, SC-008 | `gh pr view` state `OPEN` on each |
