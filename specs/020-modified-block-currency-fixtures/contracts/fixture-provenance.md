# Contract: the fixture provenance note

**One `README.md` per fixture tree this feature adds.** It answers one
question — *where did this text come from?* — for a reader who found the
fixture years later and needs to know whether it reproduces a real defect or
illustrates a rule.

**Why a file and not a docstring.** The existing convention in this suite is a
paragraph in the test module's docstring
(`tests/doc-health/test_promotion_fidelity.py`: the fixture "is a
reconstruction and says so"). That convention stays. It cannot, however, carry
a runnable command, and the whole value of a reconstruction is that a reader
can re-derive it. Orchestrator decision 2 asks for the SHAs in the fixture's
README; this contract fixes the shape so the six notes are comparable.

**Not a governed document.** No `Status:` header, no `Ratified by:`, no entry
in any README index. `corpus.EXCLUDED_PARTS` contains `tests` and
`corpus.GOVERNED_ROOTS` does not cover it, so nothing under
`tests/doc-health/fixtures/` is read by `status-validity`,
`location-conformance`, `doc-catalog` or the lifecycle scan set. Verified
against `scripts/doc_health/corpus.py` rather than assumed.

---

## Template — a RECONSTRUCTION

```markdown
# Fixture: <one-line name>

**Reconstructed from this repository's git history. Not synthesized.**

Issue #<n>. <One or two sentences: what the block was holding, and how it was
caught.>

## Provenance

| file | recovered from |
| --- | --- |
| `<repo>/openspec/changes/<change>/specs/<cap>/spec.md` | `git show <sha>:openspec/changes/<change>/specs/<cap>/spec.md` |
| `<repo>/openspec/specs/<cap>/spec.md` | `git show <sha>:openspec/specs/<cap>/spec.md` |

- **recovered at** `<40 hex>` — <what that commit is, e.g. the parent of the
  repair>
- **the defect ended at** `<40 hex>` (<subject>), merged as `<40 hex>`
  (PR #<n>)
- `proposal.md` is scaffolding: a `Status:` line only, because `_standing()`
  reads it and nothing else in this fixture depends on a proposal.

## Scope of the verbatim guarantee

The **requirement** `<title>` is byte-identical to the recovered text. The
surrounding `# <cap> Specification`, `## Purpose` and `## Requirements` lines
are synthetic scaffolding: the real promoted spec is <size> and carries
requirements this fixture says nothing about, and the family reads per
requirement. <For a delta file, say whether it is whole or trimmed.>

## What the family reports here

<One line per arm, so a reader can tell whether a later change moved it.>

## Which rule this exists for

`add-modified-block-currency-check` § 3.<n>, audit row **A<n>**.
Test(s): `<test function names>`.
```

## Template — a SYNTHESIS

```markdown
# Fixture: <one-line name>

**SYNTHESIZED. This text is invented and reproduces no historical instance.**

## Which rule this exists for

`add-modified-block-currency-check` § 3.<n>, audit row **A<n>**.

> <the rule, quoted from the ratified delta>
> — `openspec/changes/add-modified-block-currency-check/specs/doc-health/spec.md`

## Why not a reconstruction

<Why no historical instance was used — for the four synthesized trees in this
feature: this corpus carries no instance of the shape, which is itself the
reason the rule is worth pinning before one arrives.>

## What the family reports here

<One line per requirement in the tree.>

Test(s): `<test function names>`.
```

---

## Rules

1. **A SHA is written in full 40 hex**, once, in the provenance table. A short
   SHA in a note that outlives the branch it was written on is a SHA a reader
   cannot resolve after the next collision.
2. **Every `git show` line is runnable as written.** No placeholders, no
   `<path>` left unexpanded, no shell continuation.
3. **A synthesis says the word "SYNTHESIZED" in its first two lines.** The
   failure mode this contract exists to prevent is a reader trusting an
   invented fixture as evidence about the corpus.
4. **The note records what the family reports on the tree.** Not the
   assertions — the outcome. A later change that moves the outcome then has a
   line to update, and a reviewer has something to compare against.
5. **No note claims a defect is closed.** These fixtures pin behaviour; they
   do not resolve issues. #330 in particular stays open (packet § 7.1).
