---
code_surface: openxFactory (this change's ONLY diff is the `release-realization` spec delta plus the follow-on house-validator work it specifies — a strict front-matter loader over the realization-axis block, a `sequenced_after:` schema and parser, a resolution/cycle/grammar validator, an archive-retention gate, and a corpus sweep — landing under openxFactory `scripts/`, `tests/`, `docs/` and `openspec/`. It amends the neutral realization-axis front-matter contract and its validation; it touches no domain repository's tree. The codexFactory provenance-tie verifier that CONSUMES `sequenced_after` — its chain walk, its depth cap of four, its INTERSECTION composition, its co-modifier cross-check and its closed refusal-identifier set — is downstream and explicitly NOT built here: it is the realization of `realize-provenance-gated-autonomous-merge`, tracked in that change's own tasks as Groups 2.7/2.10/2.11/2.12, not in this one.)
target_release: implemented (the affected repository's main line — openxFactory. Realization = the `sequenced_after:` field is schema-validated, resolution-checked, cycle-refused and strictly loaded by the house validator on every pull request, and is available for a chain-consuming gate to read; the change archives on merged-plus-green per `release-realization` once the validator work lands and its suite runs green. There is no aggregation-repo release bundle.)
sequenced_after: [add-structured-scope-substrate]
---

# Proposal: add-sequenced-after-substrate

Status: ratified
Ratified by: convener ruling of 2026-09-01 (Brett Heap) — see
§ Ratification record.
Authored: 2026-09-01, as dependency 0.5 of codexFactory
`realize-provenance-gated-autonomous-merge`.
Directed by: Brett Heap's convener ruling **R1** of 2026-08-28 on that packet —
that the provenance-tie verifier SHALL compose the ordered-delta chain
MECHANICALLY — together with that packet's dependency register, which names this
substrate as the missing, blocking precondition and prescribes it be "specified
and built in openxFactory SYMMETRICALLY with how `scope_globs` was added". The
derivation and its limits are recorded verbatim in `.openspec.yaml`
`origin.approved_by`: **that field records a DERIVED authorization to author and
is not ratification of any content.**
Authoring method: hand-authored per openxFactory OpenSpec conventions, mirroring
the ratified sibling `add-structured-scope-substrate` (PR #525). The
`opsx:propose` alignment-review + council-debate flow was NOT run in this
session; the design decisions it would surface are carried forward as
`design.md` § Open questions OQ-1 … OQ-5 for the convener read at Group 0, and
the authoring decisions it would challenge are enumerated as S1 … S9 in
`design.md` § Decisions and were flagged for veto when written.

**RATIFIED, AND THE BUILD IS AUTHORIZED.** Per the house rule — OpenSpec
ratifies, Speckit builds — the packet was authored first and carries proposal
artifacts plus the post-ratification realization named in its `code_surface`.
Group 0 of `tasks.md` was the ratification gate and is closed; Groups 2–5 are the
authorized build. **Nothing is pushed and nothing is merged by this change.**

> **CONVENER BRIEF:** a ten-line read of what was ratified, the one open
> question that needed a ruling, and the measured blast radius, is `design.md`
> § 0.

## Ratification record

Ratified: 2026-09-01 by Brett Heap (convener, openxFactory operator authority) —
**accepting the proposal AS AUTHORED**, nine ADDED requirements and thirty
scenarios over `release-realization`, with no amendment to the spec delta.

Open-question disposition, all five ruled at the same sitting:

- **OQ-1 — the strict-loader retrofit: FIX IT INSIDE THIS CHANGE** (the
  recommendation). The strict-loader requirement's reach into `scope_globs:`
  lands here: `scripts/scope_globs.py`'s `yaml.safe_load` duplicate-key hole is
  repaired by this change's own build, which therefore repairs a ratified
  sibling's shipped reader. ONE loader over the whole realization-axis block, for
  BOTH structured fields; a strict loader with a documented hole in one field of a
  trust-root surface is not a strict loader. **This ruling sets Group 2's scope
  and Group 4's test set**, and it carries a downstream consumer consequence
  recorded as a note at the head of Group 2 in `tasks.md`.
- **OQ-2 — fan-out: MULTI-PARENT DECLARATIONS ARE ALLOWED** (as recommended). A
  fork must be DECLARABLE at the substrate for a consuming gate's fork refusal to
  be reachable and testable; forbidding it would force under-declaration on a
  trust-root surface. The validator therefore imposes no fan-out limit.
- **OQ-3 — doc-health's whole-token ordering reader: UNTOUCHED** (as
  recommended). The `modified-block-currency` family keeps its own advisory
  whole-token resolution; its migration to `sequenced_after:` is a NAMED FOLLOW-ON
  and is not built here.
- **OQ-4 — the cycle/depth split: AS AUTHORED** (as recommended). The substrate
  refuses a CYCLE (a well-formedness fact) and declares NO depth cap, NO fan-out
  cap and NO composition operator — those being the consuming gate's authorization
  policy. No cap and no operator enter the substrate.
- **OQ-5 — ratification authority: NO COUNCIL CO-SIGN REQUIRED** (as
  recommended). Convener ratification suffices, the same disposition
  `add-structured-scope-substrate` received on 2026-08-28: the doctrine that makes
  this block a trust-root floor surface was already council-ratified in the "B"
  change, and this packet adds a field to it rather than new authority.

Authoring decisions S1 … S9 (`design.md` § Decisions) were confirmed as written;
none was vetoed.

## Why

**A ratified mechanism was ordered built, and the input it walks does not
exist.** codexFactory's `realize-provenance-gated-autonomous-merge` carries
convener ruling R1 (2026-08-28): the provenance-tie verifier must WALK the
ordered-delta chain from the tied change back to its ratified root and compose
the effective authorization over that walk, rather than reading a single change.
Its design D14 is that walk. Its dependency register records the consequence in
its own words:

> **0.5 (L) Machine-readable ORDERED-DELTA PARENT LINK — MISSING; BLOCKS the
> chain walk (Group 2.7) required by convener ruling R1.** […] There is TODAY no
> machine-readable parent link to walk.

**Three candidate links exist and all three were measured to fail.** This
capability's "Ordered deltas and branch vocabulary" requirement already obliges a
proposal that modifies a requirement an active ratified change modifies to
"reference that change and declare its deltas relative to that change's outcome"
— but it is MECHANISM-AGNOSTIC PROSE, with no field, no schema and no reader. The
`Sequenced-after:` header some proposals carry is FREE TEXT NO SCHEMA VALIDATES:
measured on this worktree, **three occurrences, all three in ARCHIVED
proposals**. And the one mechanical reader, the doc-health
`add-modified-block-currency-check` family
(`scripts/doc_health/modified_block_currency.py`), resolves ordering by a
WHOLE-TOKEN OCCURRENCE of a sibling change id anywhere in the declaring
`proposal.md` — which cannot distinguish a parent from a mention, cannot express
a fork, and is author-mutable in the very document the author writes. A prose
token match is not a walkable link.

**This is the SECOND HALF of the front-matter block `scope_globs` opened.** The
same program's CRITICAL #1 forced `add-structured-scope-substrate` into
openxFactory on 2026-08-28 as the machine-readable PATH scope; the consumer's
task 0.5 prescribes this field be built "SYMMETRICALLY" with it, and the
consumer's own spec already names them as a pair: "`scope_globs` and
`sequenced_after:` are DIGEST-COVERED, because both live in `proposal.md` front
matter, which is frozen." One field says WHICH PATHS a change's realization may
touch; this one says WHERE IN THE CHAIN that authority came from. Neither is
walkable without the other.

**And the corpus says the chain shape is the NORMAL shape, not an edge case.**
Measured 2026-09-01 at requirement granularity over all 152 change ids: **104 are
co-modified** — genuine ordered deltas — and only 48 are sole modifiers. Of the 30
ACTIVE changes, 19 are chains. A mechanism that could only handle single-change
ties would be unexercisable against this corpus, which is precisely why R1
ordered the walk.

## What Changes

This change MODIFIES nothing and ADDS nine requirements to the neutral
`release-realization` capability. It adds NO runtime behavior to any domain
repository; it defines the field, its syntax, its loader, its validation, its
archive-stable resolution and its trust-root integrity as neutral doctrine, and
leaves every WALK POLICY decision to the consuming gate.

- **A new, OPTIONAL, additive front-matter sibling field `sequenced_after:`** on a
  change's `proposal.md`, beside `code_surface:` / `target_release:` /
  `scope_globs:` — the same realization-axis block the archive gate, the origin
  retention gate and the ideation dashboard already read. Its value is a SEQUENCE
  of parent change references. **`sequenced_after: []` is a POSITIVE,
  RATIFICATION-COVERED root claim**, not a formatting artifact.

- **ABSENCE IS FAIL-CLOSED AND IS NOT A ROOT CLAIM.** A change with no
  `sequenced_after:` has declared NOTHING about its chain position — it is
  neither a declared root nor a change asserted to have no parent. This mirrors
  `scope_globs`, whose absence means "not eligible" rather than "all paths": a
  field whose absence carries an authorizing meaning is a field that rewards
  omission.

- **Repository-qualified entry syntax**, because two rules a consumer needs
  otherwise collide on one input. A bare `<change-id>` (`[a-z0-9][a-z0-9-]*`, no
  `/`) means THIS repository; `<repository>:<change-id>` is qualified; a
  self-qualified entry is the bare form. A FOREIGN entry is DECLARABLE and
  WELL-FORMED, and its disposition is the consumer's — which refuses it under a
  named identifier rather than SKIPPING it, because skipping fabricates a root
  out of a declaration that says the opposite. The cross-repository "realizes the
  neutral doctrine" relation stays a PROSE relation and is never a hop.

- **ONE STRICT LOADER over the whole realization-axis block.** Duplicate keys at
  any level, anchors (`&`), aliases (`*`), merge keys (`<<:`), non-UTF-8 and
  over-ceiling documents are REFUSED rather than silently resolved. **This
  reaches `scope_globs:` too, and that is deliberate:** the shipped
  `scripts/scope_globs.py` parses with `yaml.safe_load`, which resolves duplicate
  keys silently last-wins, so two `scope_globs:` blocks show a reviewer the FIRST
  and authorize the LAST — and the consuming verifier ALREADY refuses those forms
  on its own path. A permissive loader here is not under-enforcement; it is the
  neutral validator and the consuming verifier DISAGREEING about what the same
  bytes mean, in both directions. **Carried as OQ-1** for the convener, because
  this half repairs a ratified sibling's shipped code.

- **Validation of shape, grammar, resolvability and acyclicity.** The house
  validator refuses a non-sequence, a null/empty/nested/duplicate member, an
  entry breaking the reference grammar, a BARE entry that resolves to no change in
  the declaring repository's own corpus, and a CYCLE. It imposes **NO depth limit
  and NO fan-out limit**: a multi-parent declaration and a deep chain both
  VALIDATE.

- **Archive-stable identity.** The change id is the durable identity. Resolution
  considers EXACTLY TWO locations — `openspec/changes/<change-id>/` and the
  ANCHORED `openspec/changes/archive/<YYYY>-<MM>-<DD>-<change-id>/` — with the
  date exactly `\d{4}-\d{2}-\d{2}` and the remainder EXACTLY the id, never a
  prefix strip or a split on the first hyphen. The union must hold EXACTLY ONE
  directory: zero is unresolvable, two or more is ambiguous, and neither resolves
  by preference. **122 of 152 changes in this repository are already archived**,
  so this is the normal case; and because a chain's ROOT is its OLDEST change and
  therefore the FIRST to archive, an active-only rule would make the mechanism
  self-disable in exactly the wrong order. **The archive gate SHALL NOT rewrite a
  declaration on archival.**

- **Root status is PROVED, never inferred from absence — as neutral doctrine.**
  A consumer must not read absence as root, must not treat `[]` as sufficient
  where a mechanical co-modifier cross-check contradicts it, and must keep that
  cross-check IN FORCE after adopting the field, so `[]` plus a detected
  co-modifier still refuses. **The cross-check itself is the consumer's**, because
  its key is a per-repository corpus fact (the promoted
  `openspec/specs/<capability-id>/spec.md` a delta's REQUIREMENT titles resolve
  against, normalized and requirement-granular) that a neutral field cannot carry.
  Stating the prohibition neutrally is what stops the next consumer from
  rediscovering the fail-open read.

- **Trust-root integrity bound to ratification**, the same four properties the
  sibling obligates: BASE-READ (a consumer reads the field only from the base
  branch, never a pull-request head); RATIFICATION-COVERED (it lives in
  `proposal.md` front matter, in the frozen-at-ratification set); NON-AUTHOR-MUTABLE
  (the `openspec/changes/` surface is a never-clearable floor member of every
  enrolled repository, and no autonomous merge writes it); and FROZEN AFTER
  RATIFICATION (archive-gate retention, mirroring "Origin retention at archive"
  and "Scope retention at archive").

- **NO WALK POLICY.** The substrate declares no depth ceiling, no fan-out cap and
  no composition operator. The consumer's cap of FOUR hops inclusive of the
  terminal change and its INTERSECTION operator stay in codexFactory, where they
  are enforced and where they can be measured. The substrate instead carries the
  MEASUREMENT obligation: the deepest declared chain is recorded by a corpus
  sweep, and raising any gate's ceiling is a specification change with a recorded
  disposition — never an adjustment made at the point a candidate refuses.

Ratifying this doctrine unlocks no autonomous merge by itself. It makes
`sequenced_after` validated and walkable; codexFactory's provenance-tie verifier
is the first consumer.

## This change is its own first instance

`add-sequenced-after-substrate` declares `sequenced_after: [add-structured-scope-substrate]`
in its own front matter, above. It genuinely IS an ordered delta on that change —
it extends the same front-matter block and its strict-loader requirement
obligates the reader that change shipped. And its own ADDED requirement titles are
NOVEL, so a requirement-granular co-modifier cross-check would find ZERO
co-modifiers and would let this change claim ROOT at depth 1. **It declares the
parent anyway**, which is the substrate's own doctrine applied to its author:
declaring must never be worth less than omitting. **The validator this change
builds validates this change's own declaration** — the bare entry
`add-structured-scope-substrate` resolves to exactly one active change directory,
breaks no grammar rule and closes no cycle — so the first instance is not an
unexercised example but the corpus gate's first live subject.

## The sibling rule, measured

Two ACTIVE ratified changes write `release-realization` today, and both hold the
titles a MODIFIED delta here would naturally have taken:
`govern-sibling-added-modified-deltas` (ratified 2026-08-31) holds a
`## MODIFIED Requirements` block over **"Ordered deltas and branch vocabulary"**,
and `add-structured-scope-substrate` (ratified 2026-08-28) holds one over
**"Realization axis declaration"**. Under `govern-sibling`'s own ratified rule, a
MODIFIED block over either would have to be declared relative to that sibling's
outcome AND would be held from archiving until the basis archives.

**So this delta is ALL-ADDED**, over nine novel titles. It restates no promoted
text, drops none, and owes no `Modified over`, `Removed from canon by` or
`Merged into` marker. "Ordered deltas and branch vocabulary" is left exactly as
`govern-sibling` will promote it, and its prose sequencing obligation remains
owed and unaltered — the new field is an ADDITIONAL affordance beside it, not a
replacement. This is the same discipline
`add-requirement-ref-resolution-integrity` applied for the same reason.

## Corpus sweep, measured 2026-09-01

Requirement-granular, normalized (NFC + whitespace-collapsed + case-folded),
over `openspec/changes/` and `openspec/changes/archive/`, archive ids recovered by
the anchored date strip:

| measure | count |
| --- | --- |
| change ids (30 active + 122 archived) | **152** |
| **co-modified — real ordered deltas, each would owe a `sequenced_after:`** | **104** |
| sole modifiers — each would declare `sequenced_after: []` | **48** |
| ACTIVE changes: co-modified / sole | **19 / 11** |
| prose `Sequenced-after:` headers (all in archived proposals) | **3** |
| occurrences of `sequenced_after:` anywhere before this change | **0** |

**No migration pass is proposed.** Declaring parents on 104 changes — most of
them archived and frozen — to satisfy a reader that does not exist yet would be a
flag-day cost with no consumer. Adoption is OPT-IN per change at authoring time,
exactly as `scope_globs` adoption is; the sweep becomes a build task (Group 5)
that reports the population and records the deepest declared chain.

## Impact

- **Affected spec:** `release-realization` (nine ADDED requirements, thirty
  scenarios; NOTHING MODIFIED). Titles: machine-readable ordered-delta parent
  declaration; repository-qualified parent-reference syntax; strict loading of the
  realization-axis front-matter block; parent-declaration validation;
  ordered-delta identity survives archival; root status is proved and never
  inferred from absence; trust-root integrity of the parent declaration;
  parent-declaration retention at archive; chain-walk policy belongs to the
  consumer, and its bound SHALL be measured.

- **Affected code (this change's `code_surface`, built LATER via Speckit):** the
  strict front-matter loader, the `sequenced_after` schema/parser, the
  resolution/grammar/cycle validator wired into the house validate runner, the
  archive-retention gate, the corpus sweep, and the trust-root-floor doc — under
  openxFactory `scripts/`, `tests/` and `docs/`. Per the house rule this packet
  AUTHORS only; the code is built post-ratification via the Speckit features
  mapped one-per-group in `tasks.md`.

- **This change is NOT itself provenance-eligible.** It is an
  `openspec/`-touching, human-gated change; it declares no `scope_globs` of its
  own and seeks no autonomous merge. The substrate is authored by the human-gated
  route it protects.

- **Backward-compat: no flag-day, no migration.** All 152 existing changes keep
  validating and archiving unchanged. The prose sequencing obligation, the
  doc-health whole-token ordering reader, the three archived prose
  `Sequenced-after:` headers, `code_surface`, `target_release` and `scope_globs`
  are all untouched in contract. The ONE exception is OQ-1's retrofit, which
  changes how `scope_globs` is LOADED (strictly) without changing what it MEANS —
  a corpus with a duplicated key would begin to fail, and no change in the corpus
  has one.

- **Interactions.** The archive gate gains a third retention check beside origin
  and scope. The doc-health `modified-block-currency` family keeps its own
  whole-token resolution for its advisory currency finding; migrating it to the
  structured field is a NAMED follow-on (OQ-3), not this change. The `scope_globs`
  reader gains the strict loader (OQ-1). The consumer's verifier reads
  `sequenced_after[base]` at its walk step, applies its own root proof, archive
  resolution, depth cap and INTERSECTION composition, and refuses under its own
  closed identifier set.

- **Dependency ordering.** This change is INDEPENDENT of the consumer's
  codexFactory work and may be ratified and built in parallel; only the
  consumer's chain-walk realization (its Groups 2.7/2.11/2.12) depends on this
  landing. It is an ordered delta on `add-structured-scope-substrate`, which is
  already ratified and realized, so nothing here waits on that.

## Open questions

**ALL FIVE ARE RULED** — see § Ratification record for the dispositions. They are
kept in `design.md` § Open questions as authored, with their recommendations, so
the record shows what was asked as well as what was answered: OQ-1 the
strict-loader retrofit (ruled FIX INSIDE THIS CHANGE), OQ-2 fan-out (ALLOWED),
OQ-3 the doc-health whole-token reader (UNTOUCHED, named follow-on), OQ-4 the
cycle-refused / depth-unbounded split (AS AUTHORED — no cap and no operator in
the substrate), OQ-5 council co-sign (NOT REQUIRED).
