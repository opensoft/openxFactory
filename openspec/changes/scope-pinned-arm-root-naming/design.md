# Design — scope-pinned-arm-root-naming

Status: ratified
Kind: design

Three decisions, each put with the recommendation first. `proposal.md` § *The
decision, put for a veto* carries them as one multiple choice (OQ-1); this file
carries the reasoning and the measurements. RATIFIED 2026-09-16 by Brett
Heap, verbatim "ratify 1052 when green, then 1050" — openxFactory #1047,
comment https://github.com/opensoft/openxFactory/issues/1047#issuecomment-5698480379.
D-1 stands AS FILED (OQ-1 option (a)); D-2 and D-3 remain refused, exactly
as filed. See `proposal.md` for the ratifying word in full and
`review/ratification-2026-09-16.md` for the record.

## D-1 — THE READING (RECOMMENDED, AND WHAT THE DELTA ENCODES)

**The root-naming obligation is an obligation of findings that REACH ROOT
SELECTION; the two findings emitted before it name what they judged.** Canon's
sentence gives its own reason for existing — "under two roots a bare 'no pin
record' sentence cannot be acted on and under one root the named root is what
makes the difference readable" — and both halves speak about a RESOLUTION
ATTEMPT. A root is what makes an attempt readable; it says which tree was
searched and therefore which tree the remedy belongs in. Two of the arm's
fifteen findings are reached before any attempt exists:

| finding | measured at | names | why no root |
| --- | --- | --- | --- |
| malformed pinned value | `scripts/doc_health/families.py:1573-1576`, refused at `:1572` | THE VALUE | the grammar check precedes `value.split("/", 1)` (`:1578`) and `_pin_roots(...)` (`:1580`); canon requires that order at `:241-245` and in the scenario at `:587-590` |
| no resolution root in the run | `:1587-1592`, reached at `:1580-1581` | THE REPOSITORY | `_pin_roots` returned an EMPTY LIST — the empty root set is the finding's whole subject |

The other thirteen already name a root: `:1606-1611` (`root {name}`),
`:1618-1625` (through the `rule` built at `:1617-1622`), `:1634-1638`
(`under root(s) {', '.join(searched)}`), and all ten of `_judge_pinned_record`
(`:1653-1736`, `in root {root}`). So the clarified sentence refuses nothing the
realized arm emits and demands nothing it does not do.

**THE DELTA IS THE ROOT-NAMING SENTENCE, ONE CLAUSE OF A SIBLING SCENARIO'S
WHEN, AND ONE SCENARIO — AND EVERY ONE OF THE THREE IS A SCOPING RATHER THAN A
DELETION.** The obligation's first half (the root set is the run's INPUT, not
the arm's choice) and its whole rationale clause are carried word for word;
what moves in the body is the quantifier — `EVERY finding … emits` becomes
`EVERY finding … emits AFTER ROOT SELECTION` — with the two exceptions named
together with what each names instead, so the sentence can be checked against
the code rather than read against it.

THE SECOND MOVE IS NARROWER STILL, AND IT EXISTS TO REPAIR A COLLISION THE
FIRST MOVE CREATED. The restated scenario *A pinned target names a pin no
resolution root carries* keeps its THEN and both its other AND bullets
untouched, and its WHEN gains ONE clause: "…and at least one resolution root
was selected for the run". Unscoped, that WHEN — "no pin record for
`<pin-id>` exists under any root of the run's precedence" — is ALSO true where
the run selected NO root at all, which is exactly the case the new scenario
below names with a DIFFERENT outcome (no root required, by design, since none
was selected). Left as canon states it, the two scenarios would give the
empty-root case two outcomes; the one clause gives it back to exactly one.

Measured through the family's own `derive_units`: canon 209 units (unchanged —
canon is not edited), this block 215 (unchanged — a bullet's TEXT moved, not
its count), TWO uncarried units (the body sentence, and the sibling
scenario's original WHEN bullet) and EIGHT new ones (the body sentence's
successor, the sibling scenario's narrowed WHEN bullet, and the new scenario's
title and its five bullets). The unified diff against canon's block is THREE
hunks — the sentence, the one WHEN clause, and the appended scenario, each at
a different place in the file — and `git diff --numstat` against canon's block
reads 18 added / 5 removed (17/4 before this clause moved). **NO `Removed from
canon` OR `Merged into` MARKER IS OWED**: both uncarried units have a
successor in the same block that says MORE and never less, so nothing is
deleted and a marker would declare a loss that did not happen.

**AND THE SUPERSEDES REFUSAL IS OUTSIDE THIS SENTENCE, BEFORE AND AFTER.** The
reserved-prefix refusal for an `xspec:supersedes` `spec=` value
(`scripts/doc_health/families.py:1806-1811`) is emitted by `fam_tag_hygiene`,
not by `_pinned_arm`, and has its own promoted scenario (`:672-675`). It names
no root today, it is not "a finding the pinned arm emits", and this delta
neither reaches it nor changes that.

## D-2 — WHY NOT WIDEN THE ARM INSTEAD (NOT TAKEN)

**For the empty-root-set finding, widening is IMPOSSIBLE, and that alone
settles the option.** The finding exists BECAUSE the run's `repo_paths` carries
no root for the document's repository (`_pin_roots` at `:1548-1567` returning
`[]`). There is no root to name; a name written there would be a root the run
does not have, which is an invented fact and worse than the silence it fills.

**For the malformed value, widening is possible and still wrong.** Nothing
stops the arm from calling `_pin_roots` before the grammar check — it reads
`ctx.repo_paths` and builds no pin path, so canon's "BEFORE it constructs any
pin-record path, performs any pin lookup, or reads any file" (`:241-245`) is
not by itself the obstacle, and this design says so plainly rather than
overstating the refusal. The obstacles are these:

1. **THE SENTENCE'S TWO LIMBS WOULD BOTH BE FALSE OF IT.** A root may be named
   as the one the finding "resolved against" or the one it "failed to" resolve
   against. A malformed value is refused before either act, so a root named
   beside it was neither resolved against nor failed against — the finding
   would describe an attempt that never happened.
2. **IT ADDS NOTHING A READER CAN ACT ON.** The remedy for this finding is a
   spelling (`spell a pinned target pinned:<pin-id>/<capability>`, `:1575-1576`);
   it is the same remedy in a one-root run, a two-root run and a no-root run.
   The root is what makes a RESOLUTION failure locatable, and this is not one.
3. **IT COSTS A CODE SURFACE FOR A CLARIFICATION.** Hoisting root selection
   above the grammar check, or re-reading `ctx.repo_paths` inside the refusal
   branch, edits a shipped, gated module and turns a doc-only packet into one
   that archives on merged-plus-green realization evidence — paid so that a
   finding may carry a field nobody reads. The realized arm's own comment says
   the order "is the point" (`:1528-1534`).

**SO THE CANON MOVES AND THE CODE DOES NOT.** Where a promoted sentence and a
reviewed implementation disagree about a case neither considered, the packet
that fixes the sentence is the cheaper and the more honest of the two — and
here the implementation is what canon's own ordering rule demands.

## D-3 — ALTERNATIVE REJECTED — DELETE THE SENTENCE

**The sentence is load-bearing for the thirteen findings that DO reach a root,
and two promoted scenarios depend on it.** *A pinned target's record lives only
in the root a single-repository run does not have* (`:654-658`) requires that
"the finding MUST NAME the root it searched, so the difference from the
aggregate run reads as a difference of root set rather than of precedence", and
*A pinned target names a pin no resolution root carries* (`:666-670`) requires
that "the finding MUST name the root or roots searched". Deleting the general
clause would leave those two obligations standing alone as scenario bullets,
with the body clause that generalizes them gone — the shape
`document-lifecycle` calls an obligation moved into scenario prose where
neither carriage arm can see it.

**AND IT WOULD ANSWER A QUESTION NOBODY ASKED.** openxFactory #1047 reports a
quantifier that is too wide by two findings and proposes, in its own words, "a
small clarifying delta"; a repeal would spend a ratified obligation to close a
wording defect. A deletion would also owe a `Removed from canon` marker and
would leave the corpus with no statement of why a pinned finding names a root
at all.

## Measurement — how the block was produced

GENERATION — A ONE-TIME AUTHORING STEP, ITS SCRIPT NOT COMMITTED TO THIS
REPOSITORY. A script sliced the promoted requirement from
`openspec/specs/document-lifecycle/spec.md` whole (heading to the next
`### Requirement:`), asserted the target sentence occurred EXACTLY ONCE and
replaced it, asserted the sibling scenario's WHEN occurred EXACTLY ONCE and
narrowed it by the one clause above, appended the one scenario, and wrote the
delta at `specs/document-lifecycle/spec.md`. Say so plainly: that script is an
authoring tool, not part of the packet, and is not reproducible from the
committed tree alone. What follows IS.

VERIFICATION — REPRODUCIBLE FROM THE COMMITTED TREE ALONE (canon's spec, this
packet's own delta, and `scripts/doc_health/`, none of which this measurement
edits), independently of how the delta was produced:

1. Extract canon's block and this packet's block as plain text, into a
   shell-created temporary directory rather than a fixed host-absolute path
   (`.specify/memory/constitution.md` § IV, Schema and Artifact Discipline):
   ```
   tmp=$(mktemp -d)
   python3 -c "
   import pathlib
   text = pathlib.Path('openspec/specs/document-lifecycle/spec.md').read_text()
   title = '### Requirement: Prose tagging marker hygiene\n'
   start = text.index(title)
   end = text.index('\n### Requirement: ', start + len(title)) + 1
   pathlib.Path('$tmp/canon-block.txt').write_text(text[start:end].rstrip('\n') + '\n')
   "
   tail -n +5 openspec/changes/scope-pinned-arm-root-naming/specs/document-lifecycle/spec.md \
     > "$tmp/packet-block.txt"
   ```
2. `git diff --no-index --numstat "$tmp/canon-block.txt" "$tmp/packet-block.txt"`
   reads **18  5** (18 added, 5 removed); `diff -u "$tmp/canon-block.txt"
   "$tmp/packet-block.txt" | grep -c '^@@'` reads **3** — the sentence, the one
   WHEN clause, and the appended scenario, each at a different place in the
   file, and nothing else.
3. The `derive_units` comparison, through the modified-block-currency
   family's own derivation, over the live tree rather than the two extracted
   files:
   ```
   python3 -c "
   import sys, pathlib
   sys.path.insert(0, 'scripts')
   from doc_health import modified_block_currency as mbc
   from doc_health import promotion_fidelity as pf
   root = pathlib.Path('.').resolve()
   canon_req = mbc.promoted(root, 'document-lifecycle')[pf.norm('Prose tagging marker hygiene')]
   block = [b for b in mbc.active_blocks(root) if b.change == 'scope-pinned-arm-root-naming'][0]
   print('canon units:', len(canon_req.units))
   print('block units:', len(block.units))
   print('uncarried:', len(mbc.carried(canon_req.units, block.units)))
   have = {u.pair() for u in canon_req.units}
   print('new:', len([u for u in block.units if u.pair() not in have]))
   "
   ```
   reads `canon units: 209`, `block units: 215`, `uncarried: 2`, `new: 8`.
4. The same fact as a live finding rather than a script: `python3
   scripts/doc-health.py --single-repo . --as-of <today> --family
   modified-block-currency` reports the block "does not carry 2 of the 186
   body units and scenario bullets ... currently states for it", quoting both
   uncarried units by text.

All four commands were re-run against this commit and reproduce the numbers
stated above and in the pull request body exactly.

Base of measurement: `origin/main` @ `8944758c` (the archive of
`extend-prose-tagging-target-to-pinned-capabilities`, PR #1042, merged
2026-09-15T19:35:11Z).
