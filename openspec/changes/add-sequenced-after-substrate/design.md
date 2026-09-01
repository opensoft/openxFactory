# Design: add-sequenced-after-substrate

## 0. CONVENER BRIEF — what is being ratified, and the one thing to rule on

1. **What.** One new OPTIONAL front-matter field on a change proposal —
   `sequenced_after:` — a list of parent change ids, or `[]` meaning "I am a
   chain root". It is the machine-readable half of the ordered-delta sequencing
   this capability already obliges in prose. Nine ADDED requirements, thirty
   scenarios, `release-realization`.
2. **Why now.** It is dependency **0.5** of codexFactory's
   `realize-provenance-gated-autonomous-merge` — named MISSING and BLOCKING —
   and your ruling **R1** requires that verifier to walk the ordered-delta chain
   MECHANICALLY. There is no walkable link today: prose, whole-token id mentions
   and the `Sequenced-after:` header (3 occurrences, all archived) are all
   unwalkable.
3. **Symmetry.** This is the second half of the block `scope_globs:` opened. Same
   artifact shape, same validator pattern, same trust-root-floor doc, same
   fail-closed absence rule.
4. **What it deliberately does NOT decide.** No depth ceiling, no fan-out cap, no
   composition operator, and no co-modifier cross-check. Those are the consuming
   gate's policy (the cap of 4 and INTERSECTION stay in codexFactory), and the
   cross-check's key is a per-repository corpus fact a neutral field cannot carry.
5. **Corpus reality, measured.** 152 changes; at requirement granularity **104
   are co-modified** — real ordered deltas that would each owe a
   `sequenced_after:` — and **48 are sole modifiers** that would declare `[]`. Of
   the 30 ACTIVE changes, **19 are chains and 11 are roots**. Adoption is opt-in
   and no migration pass is proposed.
6. **THE ONE OPEN QUESTION THAT NEEDS YOU (OQ-1).** The strict-loader requirement
   reaches `scope_globs:` as well as `sequenced_after:`, because the shipped
   `scripts/scope_globs.py` uses a PERMISSIVE parser (`yaml.safe_load`)
   that resolves DUPLICATE KEYS silently, last-wins — so two
   `scope_globs:` blocks show a reviewer the FIRST and authorize the LAST, and the
   consuming verifier already refuses that. **Fix it here, in this change
   (recommended), or file a separate successor?** Fixing it here means this packet
   repairs its ratified sibling's shipped code; recommended because a strict loader
   with a hole in one field of the same block is not a strict loader.
7. **OQ-2 … OQ-5** carry recommendations and need no ruling unless you disagree:
   allow multi-parent declarations (recommend YES — a fork must be declarable for
   a consumer's fork refusal to be reachable); leave doc-health's whole-token
   ordering reader alone (recommend YES, migration is a named follow-on);
   validator refuses cycles but not depth (recommend YES); no council co-sign
   required (recommend convener ratification suffices, as for `scope_globs`).
8. **Blast radius if wrong.** Zero today. The field is absent everywhere, no
   consumer is built, and every existing change keeps validating and archiving
   unchanged. The first consumer is codexFactory's verifier, which is downstream
   and not built here.
9. **What ratification authorizes.** Speckit builds Groups 2–5 (schema + strict
   loader, validator, integrity/archive gate, corpus sweep + docs). It authorizes
   no autonomous merge by itself.
10. **What it does not authorize.** Nothing is pushed, nothing is merged, and no
    code exists yet. Group 0 is your gate and is the only human task here.

## Context

- **Consumer (ratified, downstream):** codexFactory
  `realize-provenance-gated-autonomous-merge` on branch
  `change/realize-provenance-gated-autonomous-merge` @ `834ce761`. Its
  **ruling R1** (Brett Heap, convener, 2026-08-28) requires the provenance-tie
  verifier to compose the ordered-delta chain MECHANICALLY; **design D14** is the
  chain walk and composition; **D21** is the proved-root rule; **D22** is archive
  resolution; **D23** is the closed refusal-identifier set; **tasks 2.7, 2.10,
  2.11, 2.12** are the enforcement; **task 0.5** is this change. The
  **mechanism memo** `specs/012-realize-provenance/design/mechanism-memo-2026-08-30.md`
  § 3 (Mechanism 2, "attestation ↔ walked chain binding") is where the walk is
  declared the TRUST ROOT for chain membership: *"the BASE TREE's
  `sequenced_after:` chain, walked by the verifier. Never the payload."*
- **Model sibling (ratified, ACTIVE):** openxFactory
  `add-structured-scope-substrate` — ratified 2026-08-28, realized in
  `scripts/scope_globs.py`, `scripts/validate-scope-globs.py`,
  `tests/scope_globs/`, and `docs/scope-globs-trust-root-floor.md`, landed via
  PR #525. This change mirrors its artifact shape, its front-matter discipline,
  its house-validator pattern, and its trust-root doc, and DECLARES IT AS THIS
  CHANGE'S OWN PARENT.
- **Amended capability:** `release-realization`
  (`openspec/specs/release-realization/spec.md`) — the neutral home of the
  realization-axis front-matter block and of "Ordered deltas and branch
  vocabulary", the prose sequencing obligation this field makes mechanical.

## Decisions

### S1 — A new OPTIONAL sibling field, `sequenced_after:`, not an amendment to any existing one
The prose obligation already exists ("Ordered deltas and branch vocabulary":
a proposal modifying a requirement an active ratified change already modifies
"references that change and declares its deltas relative to that change's
outcome"). What does not exist is a MACHINE-READABLE form of the reference. Three
candidate links were measured and all three fail:

| candidate | why it is not walkable |
| --- | --- |
| the prose obligation itself | mechanism-agnostic; no schema, no field, no reader |
| `Sequenced-after:` header | free text no schema validates; **3 occurrences, all in ARCHIVED proposals** (`add-duplicate-packet-check`, `add-doxbench-editing-phase-b`, `add-release-inventory-drift-check`) |
| doc-health's whole-token id match | `scripts/doc_health/modified_block_currency.py` resolves ordering by a whole-token occurrence of a sibling change id ANYWHERE in the declaring `proposal.md` — cannot distinguish a parent from a mention, cannot express a fork, author-mutable in the same document the author writes |

A new sibling is additive and non-breaking: all 152 changes keep validating and
archiving, and the prose obligation is untouched and still owed. Amending the
prose requirement into a structured one would be a flag-day break of the entire
corpus, which is the same reasoning that resolved `scope_globs` in favour of a
sibling over amending `code_surface`.

### S2 — The value is a SEQUENCE, and `[]` is a POSITIVE root claim
A mapping (as `scope_globs` uses) is wrong here: a chain position is an ordered
list of parents, not a per-repository partition. The empty sequence is given
meaning deliberately — it is the only way an author can make root status
DECLARABLE and therefore RATIFICATION-COVERED. Absence, by contrast, carries no
meaning at all: it is neither a root claim nor an assertion of no parent. That
asymmetry is the whole point of S6.

### S3 — Repository-qualified entry syntax, because two rules otherwise collide
Adopted verbatim from the consumer's resolution of its own round-2 condition 2
contradiction. A bare `<change-id>` means this repository; `<repository>:<change-id>`
is qualified; a self-qualified entry is the bare form. Without the syntax, a
consumer holding both "the chain is this repository's own corpus" and "an
unresolvable entry refuses" has two incompatible readings of ONE input, and the
dangerous reading — silently skipping a foreign entry — FABRICATES A ROOT out of a
declaration that says the opposite. Grammar: `<change-id>` is
`[a-z0-9][a-z0-9-]*` with no `/` (which also anchors the ACTIVE side of
resolution and forbids a nested `openspec/changes/<id>/openspec/changes/<id2>/`);
`<repository>` is `[A-Za-z0-9_.-]+`, the same token grammar
`scripts/doc_health/proposal_origin.py`'s origin-id regexes already use.
The substrate makes a foreign entry DECLARABLE and WELL-FORMED and leaves its
DISPOSITION to the consumer — which refuses it under `cross_repository_hop`.

### S4 — ONE STRICT LOADER over the whole realization-axis block, `scope_globs` included
This is the one decision that reaches beyond the new field, so the reasoning is
recorded in full. `scripts/scope_globs.py` reads the field's sub-block with
`yaml.safe_load`, which resolves DUPLICATE KEYS SILENTLY, LAST-WINS. The
consumer's task 2.10 names the consequence exactly: two `scope_globs:` blocks
"would show the council the FIRST and authorize the LAST", and its verifier
therefore refuses duplicate keys at any level, anchors (`&`), aliases (`*`),
merge keys (`<<:`), non-UTF-8 and over-ceiling documents on the provenance path.

If the substrate validator does not refuse the same forms, the failure is not
under-enforcement — it is DISAGREEMENT between the neutral validator and the
consuming verifier about what the same bytes mean, in both directions. A strict
loader that covers `sequenced_after:` and leaves `scope_globs:` on
`yaml.safe_load` is worse still: one front-matter block, two loaders, is exactly
the drift hazard the sibling's own D4 lockstep discipline exists to prevent. So
the requirement is written over the BLOCK rather than over the field, and the
retrofit of `scope_globs`'s reader is inside it. **Carried as OQ-1** because it
repairs a ratified sibling's shipped code and that is the convener's call, not
the author's.

### S5 — Archive-stable identity: two anchored locations, exactly one match, no rewrite on archive
Adopted from the consumer's D22, and generalized to the substrate because the
hazard is the substrate's. Archiving MOVES and DATE-PREFIXES a change directory.
The ROOT of an ordered-delta chain is its OLDEST change and therefore the FIRST to
archive — so an active-corpus-only resolution rule would make the mechanism
self-disable in exactly the wrong order. Measured in this repository: **122 of
152 changes are already archived**, so the archived case is the NORMAL case, not
an edge case. Resolution is therefore `openspec/changes/<change-id>/` OR the
anchored `openspec/changes/archive/<YYYY>-<MM>-<DD>-<change-id>/` with the date
exactly `\d{4}-\d{2}-\d{2}` and the remainder EXACTLY the id — never a prefix
strip, never a split on the first hyphen, because change ids themselves contain
digits and hyphens (`add-doxbench-editing-phase-b`,
`2026-08-25-add-release-inventory-drift-check`). The union must hold EXACTLY ONE
directory; zero is unresolvable and two or more is ambiguous, and neither resolves
by preference. And the archive gate SHALL NOT REWRITE a declaration on archival —
if archiving re-pointed entries to archived paths, the declaration's ratified
bytes would change at the gate that is supposed to freeze them, and the retention
check (S8) would be self-defeating.

### S6 — Root status is PROVED, never inferred from absence — stated neutrally, enforced by the consumer
The single most load-bearing decision, taken directly from the consumer's D21,
which found the fail-open read and the reasoning is worth restating at the
substrate so the next consumer cannot rediscover it:

- **Pre-adoption**, no change carries the field. "Absence is the root" therefore
  makes EVERY chain read as a depth-one root, authorizes on the terminal change's
  own declarations, and leaves the refusal it was supposed to raise UNREACHABLE,
  because a chain is undetectable.
- **Post-adoption**, the same reading makes declaration AUTHOR-OPT-IN. Under any
  NARROWING composition — and the consumer's is intersection — declaring your
  parent COSTS you authority while omitting it does not. A control that rewards
  omission is not a control.

So: root is proved by `[]` OR by a mechanical co-modifier cross-check, and
neither-holds REFUSES. **The cross-check is NOT defined here**, on purpose: its
key is the promoted `openspec/specs/<capability-id>/spec.md` that a delta's
REQUIREMENT titles resolve against — a per-repository corpus fact, normalized
(NFC, case-folded, whitespace-collapsed) and requirement-granular per the
consumer's round-3 condition 36. A neutral field cannot carry it, and a neutral
validator cannot evaluate another repository's corpus. What the substrate CAN and
does do is BIND every consumer: do not read absence as root, and keep the
cross-check in force after adoption so `[]` plus a co-modifier still refuses.

### S7 — Fan-out is DECLARABLE; the cap is the consumer's
A multi-entry declaration validates. Two reasons, both structural. First, an
honest change with two parents must be able to SAY SO; a substrate that forbade
the second entry would force under-declaration on a trust-root surface, which is
the S6 failure mode with a different mechanism. Second, a consumer's FORK refusal
must be REACHABLE — if a fork cannot be declared, the refusal is unreachable and
untestable, which is exactly the defect D21 found in the round-1 root rule. This
is the same posture the sibling takes on over-declaration: a `scope_globs` glob
naming a floor path VALIDATES, and the verifier's floor override parks it at check
time. Declare permissively, refuse at the gate, and keep the refusal reachable.

### S8 — Trust-root integrity and the archive freeze, mirroring the sibling's four properties
Base-read; ratification-covered; non-author-mutable; frozen after ratification.
The second property is already true by construction and is worth naming: the
declaration lives in `proposal.md` FRONT MATTER, which the consumer's mechanism 3
places in the FROZEN-at-ratification file set — its own spec says
"`scope_globs` and `sequenced_after:` are DIGEST-COVERED, because both live in
`proposal.md` front matter, which is frozen." The freeze is realized here as a
separate archive-gate requirement mirroring the shipped "Origin retention at
archive" and "Scope retention at archive", so mutation between ratification and
archive is a contested-class failure needing an explicit disposition. Under a
narrowing composition, a silent re-parent — or a silent promotion to root — is a
WIDENING, which is why the freeze is required rather than advisory.

### S9 — The substrate declares NO policy: no depth cap, no fan-out cap, no composition operator
The consumer's cap is FOUR hops inclusive of the terminal change and its operator
is INTERSECTION. Neither belongs here. Depth, fan-out and composition are the
authorization policy of the gate that ACTS on a chain; a number fixed in the
neutral field would bind repositories that never adopt any such gate while
drifting from the one gate that enforces it. The substrate owes WELL-FORMEDNESS
and WALKABILITY — resolvable, acyclic, unambiguous, frozen. A CYCLE is refused
BY the substrate, because a chain that revisits an id can never reach a root under
ANY policy, which makes it a well-formedness fact and not a policy judgement.

**And the bound must be MEASURED.** The consumer's own spec records that as at
2026-08-31 the deepest resolvable live chain is "ONE HOP, BY CONSTRUCTION" and
that this is "a measurement of ZERO evidence, not evidence that four is enough."
The substrate carries the measurement obligation forward: the first corpus sweep
after adoption records the deepest chain resolved, and raising any gate's ceiling
is a specification change with a recorded disposition — never an adjustment made
at the point a candidate refuses.

## Corpus sweep — measured 2026-09-01 on this worktree (`origin/main` @ `31fc2b6e`)

Method: for every change directory (active and archived, archive ids recovered by
the anchored `<YYYY>-<MM>-<DD>-` strip), derive its `### Requirement:` titles from
its own `specs/*/spec.md` delta files, normalized NFC + whitespace-collapsed +
case-folded, keyed by `(capability-id, requirement-title)`. Two changes sharing a
key are CO-MODIFIERS. This mirrors the consumer's requirement-granular
cross-check key (round-3 condition 36c), not the coarser capability-granular one.

| measure | count |
| --- | --- |
| change ids in corpus (30 active + 122 archived) | **152** |
| **co-modified — real ordered deltas, each would owe a `sequenced_after:`** | **104** |
| sole modifiers — each would declare `sequenced_after: []` | **48** |
| of the 30 ACTIVE changes: co-modified / sole | **19 / 11** |
| occurrences of the prose `Sequenced-after:` header (all archived) | **3** |
| occurrences of `sequenced_after:` today, anywhere | **0** |

At CAPABILITY granularity the picture is far starker — 136 of 152 co-modified,
with `ideation-dashboard` written by 34 changes and `doc-health` by 32 — which is
the measurement behind the consumer's condition 36(c): a capability-level key
"refuses essentially every honest tie into a MATURE capability while a tie into a
FRESH one passes." Recorded here because it is the reason the substrate leaves the
cross-check's key to the consumer rather than fixing a granularity neutrally.

**Consequence for adoption.** 104 of 152 changes are genuinely chains, so a
migration pass is NOT proposed: it would touch two thirds of the corpus, most of
it archived and frozen, to declare parents nothing reads yet. Adoption is opt-in
per change at authoring time, exactly as `scope_globs` adoption is. The corpus
sweep is instead a BUILD TASK (Group 5) that reports the population and records
the deepest declared chain, so the number is measured rather than assumed.

## This change is its own first instance, and that is the proof

`add-sequenced-after-substrate` declares `sequenced_after: [add-structured-scope-substrate]`
in its own `proposal.md` front matter. This is honest and it is also the
demonstration:

- It IS an ordered delta on that change. Its strict-loader requirement obligates
  the reader that change shipped, and it extends the same front-matter block.
- Its own ADDED requirement titles are NOVEL, so a requirement-granular
  co-modifier cross-check finds ZERO co-modifiers and would let this change claim
  ROOT at depth 1. **It declares the parent anyway.** That is S6's doctrine
  applied to its author: declaring must not be worth less than omitting.
- The field it declares is not yet validated by anything (Group 3 builds that),
  which is exactly what "additive and non-breaking" means in practice — and the
  Group 5 corpus sweep will find this declaration as its first datum.

## The sibling rule, measured

`govern-sibling-added-modified-deltas` (RATIFIED 2026-08-31, ACTIVE) holds a
`## MODIFIED Requirements` block over `release-realization`'s **"Ordered deltas
and branch vocabulary"**, and `add-structured-scope-substrate` (RATIFIED
2026-08-28, ACTIVE) holds one over **"Realization axis declaration"**. Those are
the two titles a MODIFIED delta here would naturally have taken — and under
`govern-sibling`'s own ratified rule, a MODIFIED block over a requirement an
ACTIVE ratified change also writes must be declared relative to that change's
outcome AND is held from archiving until the basis archives.

So the delta here is **ALL-ADDED**, over nine novel titles. It restates no
promoted text, drops none, and owes no `Modified over`, `Removed from canon by`
or `Merged into` marker. The prose obligation in "Ordered deltas and branch
vocabulary" is left exactly as `govern-sibling` will promote it, and the new field
is declared as an additional, optional affordance beside it. This is the same
discipline `add-requirement-ref-resolution-integrity` applied for the same reason.

## Risks / trade-offs

- **A second field on one front-matter block widens the block's surface.**
  Accepted: the block is already the trust-root surface (frozen, code-owned,
  floored), and one strict loader over the whole block (S4) is what keeps two
  fields from being two readers.
- **The substrate refuses cycles but not depth, so a pathological 40-hop chain
  validates.** Accepted and deliberate (S9): every gate refuses it, the refusal is
  named, and the alternative is a neutral number that drifts from the gate.
- **Multi-parent declarations validate but no gate walks them** (S7). Accepted:
  the fork refusal is reachable precisely because the fork is declarable.
- **The retrofit in S4 touches a ratified sibling's shipped code.** Held as OQ-1
  for the convener rather than executed as an authoring decision.
- **doc-health's whole-token ordering reader is left in place** and now coexists
  with a structured field that means the same thing. Accepted for v1: that reader
  serves an ADVISORY prose-currency finding, not an authorization decision, and
  migrating it is a named follow-on (OQ-3). The risk is the two readers
  disagreeing on one proposal, which is a doc-health finding rather than a gate
  decision.
- **Adoption is opt-in, so the corpus stays mostly undeclared** and any
  chain-consuming gate stays exercisable only on declared chains. Accepted: this
  is the same grandfathering `scope_globs` chose, and the consumer's fail-closed
  default already handles it.

## Open questions (carried for the convener ratification read, Group 0)

1. **THE ONE THAT NEEDS A RULING — the strict-loader retrofit (S4).** The
   requirement is written over the realization-axis BLOCK, so it obligates a
   strict loader for `scope_globs:` as well, repairing the `yaml.safe_load`
   duplicate-key hole in `scripts/scope_globs.py` that the consuming verifier
   already refuses. **Fix it inside this change (RECOMMENDED), or narrow the
   requirement to `sequenced_after:` and file the `scope_globs` repair as a
   separate successor?** Recommendation: fix here — one block, one loader; a
   strict loader with a hole in a trust-root surface is not one.
2. **Fan-out (S7): allow multi-entry declarations?** Recommendation: YES — an
   honest fork must be declarable or the consumer's fork refusal is unreachable
   and untestable, and forbidding it forces under-declaration on a trust-root
   surface.
3. **doc-health's whole-token ordering reader.** Leave it as the advisory
   currency reader it is and file its migration to `sequenced_after:` as a named
   follow-on (RECOMMENDED), or migrate it in this change? Recommendation: leave
   it — it is advisory, it has its own promoted contract, and migrating a
   doc-health family inside a substrate change couples two unrelated blast radii.
4. **Cycle refusal at validate time (S9).** Confirm the split is right: the
   substrate refuses a CYCLE (a well-formedness fact) but declares NO depth cap
   and NO composition operator (gate policy). Recommendation: as authored.
5. **Ratification authority.** Does a substrate change that defines an input an
   autonomous-merge path consumes need `gate_rules_council` sign-off in addition
   to convener ratification? Recommendation: NO — convener ratification suffices,
   the same disposition `add-structured-scope-substrate` received on 2026-08-28,
   because the doctrine that makes this block a trust-root floor surface was
   already council-ratified in the "B" change and this packet adds a field to it
   rather than new authority.
