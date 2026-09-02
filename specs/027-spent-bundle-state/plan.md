# Implementation Plan: the third state — a SPENT bundle

**Branch**: `027-spent-bundle-state` | **Date**: 2026-09-02 |
**Spec**: [spec.md](./spec.md)

**Realizes**: `openspec/changes/declare-spent-bundle-state` § 2 (2.1–2.9).
Ratified 2026-09-02; merged as PR #578, squash
`f4fddf7cbc3b4fe805c8b75ee8e2a9c5e0e297ef`, which is this branch's base and
branch point.

**Why Speckit and not `/opsx:apply`**: the ratified packet says so in terms —
*"OpenSpec ratifies; Spec Kit builds. Group 2 is ONE Spec Kit feature: the
reader, the ladder, the two emits, the `contract-v2.6` declaration and the
tests are a single vertical slice, and splitting them would produce halves
neither of which is green alone — a reader with no declaration to read leaves
the `error` standing, and a declaration with no reader is a sentence in a
changelog."*

## Summary

Four files move. `contracts/CHANGELOG.md` gains ONE reserved line inside a
subsection that already exists. `scripts/doc_health/release_tag_publication.py`
gains a pure reader over the changelog bytes, four action constants, a
per-bundle finding path, and a refusal ladder placed in the ABSENT arm after
the three tag-exists branches. `tests/doc-health/test_release_tag_publication.py`
gains 13 scenario tests, 11 reader tests and 3 report-integration tests over
the file's real-git fixtures — which now carry a real changelog, because the
declaration is read from a BLOB and a fixture that handed the reader a string
would not exercise the read at all. `docs/doc-health.md` gains the third state
in the family's own note, with the family-count sentences untouched.

## Technical context

**Language**: Python 3.12, stdlib only. The `doc_health` package imports no
third-party module and this feature adds none (`dataclasses.replace` is
stdlib).
**Testing**: pytest, with REAL git repositories as fixtures — this family's
whole subject is the difference between an annotated tag and a lightweight
ref, and between a published ref and a local one, distinctions that exist in
git and nowhere else.
**Constraints**: `blobs_at` answers RAW BYTES (the release inventory's identity
rule is computed over them), so every reader in this family takes bytes.
`Finding.match_key()` is `(family, repo, path)` and ignores rule text, which
dictates the path choice.

## Constitution check

* **Deterministic evidence over assertion** — every claim in
  [`evidence/`](./evidence/) is a recorded command and its output, including
  the one claim that cannot be made in-branch (SC-001) which is proved against
  a simulated post-merge origin.
* **Fail closed** — every state is entered by a record that exists and refused
  by a record that does not. The one guard that could not be checked in-branch
  (the successor's published tag) is a git question and is answered by the same
  helper the family already uses.
* **No scope nobody granted** — `docs/contract-versioning-policy.md` is NOT
  edited (see § Routing), `health/dispositions.yaml` is not touched, and
  `test_this_repository_reads_zero_and_the_probe_can_fire` is not edited: it
  goes green as a CONSEQUENCE.

## Design decisions

### D1 — the ladder's PLACEMENT is the scope rule

The requirement says *"THE SPENT STATE REACHES THE ABSENT-TAG ARM AND NOTHING
ELSE."* That could be implemented with a condition, or with a position. It is
implemented with a POSITION: the ladder sits after the `ok`, `lightweight` and
`misplaced` branches, each of which `continue`s, so no declaration can reach a
bundle whose tag exists. The scope rule then holds BY CONSTRUCTION rather than
by care, and a future edit that wanted to break it would have to move code
rather than delete a condition.

### D2 — the reader is PURE and the judgment is NOT in it

`read_spent_declarations(bytes) -> {bundle: SpentDeclaration}` says what the
line contains and what it is missing. `spent_refusal(declaration, subject, cut)`
answers every acceptance question a changelog read can answer. `check_repo`
answers the one that needs git (is the successor's tag published) and is the
only place that can turn an unlistable ref into a skip. Split three ways so
that the parse is testable without a repository and the ladder is testable
without a parser — 11 of the new tests need no git at all.

### D3 — REJECT, never skip, on a malformed line

A line beginning with the reserved opener is a declaration BY CONSTRUCTION. If
it does not complete the form it comes back carrying `missing` or `defect` and
is REFUSED. The alternative — falling back to "not a declaration" — would make
a typo in the record indistinguishable from no record, which is the failure
mode this state exists to refuse.

### D4 — the ` — ` separator is RESERVED WITHIN the line

A CAUSE carrying the separator splits into a segment the form does not define,
and that is reported as MALFORMED rather than guessed at. The alternative
(greedy backtracking to the last valid split) would make the family's reading
of a record depend on the record's punctuation, which is exactly what OD-2
rejected when it declined a free-prose read.

### D5 — the CHANGELOG guard sits after the declared-bundle skips

Both reads are in ONE `blobs_at` call at ONE commit — that is the "joins the
manifest read" the packet asks for, and it is what makes it impossible to
accept a declaration about a bundle the manifest had already moved past. The
GUARD, though, is placed after `declared is None` and the version-shape check:
a repository declaring no bundle is better described by its own reason than by
a changelog it was never going to be asked about, and the scenario asks only
for *"a skip naming that read"*. Disclosed rather than left to be discovered.

**A CONSEQUENCE THAT IS STATED RATHER THAN HIDDEN**: a repository that declares
a bundle and holds no `contracts/CHANGELOG.md` now SKIPS where it previously
reported. That is the ratified fail-closed rule (*"not fetched is not an
answer, in either direction"*), and it is why `_declare` seeds a changelog into
every fixture in the test file: a fixture with no changelog is a fixture the
family declines to judge, which would make every other assertion in that file
vacuous.

### D6 — two residues, both disclosed

1. **A line whose SUBJECT cannot be read** names no bundle, so no per-bundle
   inventory exists to land it on. It is reported at `error` on
   `contracts/CHANGELOG.md` — the only path available — and shares that path
   with the orphan-subject `warning`. The requirement designates exactly one
   changelog-path finding; this is a second, forced by the reserved-opener rule
   (a line beginning with the opener is never prose). Named here rather than
   left for a reviewer to find.
2. **The declared-bundle refusal's path** is `inventory_path(declared)`, which
   is CONSTRUCTED and may not yet exist on disk if the same cut writes it. A
   finding's path is its identity, and a constructed path is unique per bundle,
   which is what identity needs.

## Routing — OpenSpec tasks § 3.1, and why it is NOT discharged here

`docs/contract-versioning-policy.md` is artifact
`docs-contract-versioning-policy.md` in
`contracts/releases/contract-v3.0.digests.yaml` and is NOT one of the three
editorial members, so any edit to it between cuts raises a
`release-inventory-drift` **ERROR**. PR #577 (merged `2898b104`, 2026-09-02)
already made such an edit — recording `contract-v2.6`'s supersession as
instance SIX — so that error is ALREADY on `main` and OD-6's cost argument is
spent: the INCREMENTAL cost of adding the SPENT-state paragraph is zero.

**The owner ruled on 2026-09-02 that #577's existing drift CARRIES TO THE NEXT
CUT, and that the pre-authorized scope of this realization is "editorial
member; no drift."** So the obligation-side paragraph — the versioning policy
naming SPENT as a state and its reserved declaration form, so a consumer
reading the pinned policy can find the state without reading doc-health —
STAYS OWED at the next cut. Tasks § 3.1 is left UNTICKED with a dated
one-sentence note recording the routing. What #577 already discharges (the
consumer-facing half: the bundle is superseded and not dischargeable) MUST NOT
be re-authored — *"two records of one measurement is how they drift apart."*

## Phases

* **Phase 0 — research** ([research.md](./research.md)): six questions, each
  answered by reading the code rather than by preference.
* **Phase 1 — design** ([data-model.md](./data-model.md)): the declaration
  entity, the four action constants, the path rule and the three outcomes.
* **Phase 2 — the declaration FIRST** (T001–T003), because the packet says
  2.1 is first and not silently, and because the red-first proof needs
  something to remove.
* **Phase 3 — RED tests** (T004–T018) before the module moves.
* **Phase 4 — the module** (T019–T024).
* **Phase 5 — docs, evidence, gates** (T025–T035).

See [tasks.md](./tasks.md).

## Branch point and merge base

Branch point `f4fddf7cbc3b4fe805c8b75ee8e2a9c5e0e297ef` (PR #578's squash). No
catch-up merge was needed: `origin/main` did not advance during the feature.

## What this feature does NOT change

`Finding`, `report.render`, the finding or ranked-plan grammars,
`health/dispositions.yaml` or its readers, the threshold (five), the
enforcement floor (`contract-v1.7`), `release-inventory-drift`, `verify_tag`,
`contracts/manifest.yaml`, `contracts/releases/contract-v2.6.digests.yaml`, the
`## contract-v2.6` changelog entry, any other family, or the count of families.
