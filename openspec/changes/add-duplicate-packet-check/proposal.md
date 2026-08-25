---
code_surface: openxFactory (`scripts/doc_health/duplicate_packet.py` — a new module owning the family: the content fingerprint, the identity grouping, the pairwise walk, the lineage exemption and its token matcher, the pinned-basis tree selection, and the disposition read; `scripts/doc_health/promotion_fidelity.py` — three additive seams and no behaviour change: `DeltaRequirement` gains `body` and `parse_delta` fills it (the raw block lines, requirement header excluded), `declares_pre_ratification` names the existing C5 exemption so a sibling can call it without a second reading of `Status:`, and the disposition readers become public and family-parameterized (`load_dispositions(ctx, family)` / `disposed`) so one reader of `health/dispositions.yaml` serves both families; `scripts/doc_health/families.py` — one import, one registration line in `FAMILIES`, one note recording why the family is deliberately absent from `FAMILY_RESOLUTION`, and the module docstring's owner list; `scripts/doc_health/__init__.py` — one entry in `FAMILY_IDS` so the family gets its own report section; `tests/doc-health/test_duplicate_packet.py` plus `tests/doc-health/fixtures/duplicate-packet*/` — the near-miss reconstruction, the three lawful negatives, the prefix-trap pair with its two-run disagreement, the content rule at its edges, the structural pins on the advisory launch and the pinned basis, and the disposition cases; `tests/doc-health/test_lifecycle_scan_set.py` — the family classified as a non-reader of the lifecycle scan set, which is the loud failure that test was built to produce. NO change to the governed corpus, the lifecycle scan set, any existing family's behaviour or measurement basis, the report schema, the regression-diff rule, or any threshold.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `add-promotion-fidelity-check` and `govern-openspec-corpus-membership` exactly: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts — which here is by nothing at all — and in no other line. The change therefore ships ACTIVE and archives only after the merge.
Status: ratified
Ratified: 2026-08-24 by Brett — in-session commissioning, verbatim: "commission the duplicate-packet check". The citation covers the DECISION TO BUILD THIS CHECK and nothing else; the four design decisions in § Orchestrator Decisions below were taken by the orchestrating session under standing patterns, are NOT covered by this citation, and are flagged there for veto. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing its three-way floor on two axes rather than the one it needs: approver (`by Brett`) and date (`2026-08-24`).
Proposed: 2026-08-24
Sequenced-after: add-promotion-fidelity-check, then add-release-inventory-drift-check (all three MODIFY `doc-health`'s "Deterministic check families"; that family's chain takes the count seventeen -> eighteen -> nineteen, and this delta is written against the outcome of both and takes it to twenty. A packet that archives out of that order restates a shorter list and drops a family from canon — which the eighteenth family would then report against whichever delta it silently superseded)
Origin: openxFactory PR #317's close comment, 2026-08-25 — "Closed unmerged as the duplicate of apply-branch-sessions-deltas (main 042df4e7), which landed mid-flight from a parallel session. Independent corroboration, for the record: both packets restate the same 2026-08-01 ratified delta byte-identically ... One ruling, one discharge: the landed packet is it."
---

# Proposal: add-duplicate-packet-check

## Why

**One ruling can be discharged TWICE, and every check in this corpus reports
the repository healthy.** The eighteenth family, landed hours earlier, asks
whether a ratified delta REACHED canon. Its neighbour asks the opposite
question of the same documents — whether canon was reached twice, by two
independent governance acts, neither of which knows about the other — and
nothing asks it.

**This corpus came twenty minutes from the defect.** openxFactory PR #317
proposed `apply-workbench-branch-sessions-delta`; the landed
`2026-08-25-apply-branch-sessions-deltas` (PR #316) proposed the same remedy
from a parallel session. Both restated the identical 2026-08-01
`add-workbench-branch-sessions` delta. Measured, not asserted: the two delta
files hash the same git blob, `63e615aa4119b6bba62685fb539660badf9ba73d`, and
PR #317's close comment records the corroboration independently — "both
packets restate the same 2026-08-01 ratified delta byte-identically (delta
file sha256 f6ffd39a…, Corpus scan scope block 99fa2a84…, Branch-session
notebooks block 107ede78…), and this branch's promoted spec diffs 0 lines
against main — two independent derivations produced the same canon from the
same ratified source."

A human closed #317 unmerged. Had the merge order gone the other way by those
twenty minutes, both packets would have archived and the record would carry
two discharges of one ruling with nothing saying so:

- `openspec --strict` validates each packet's SHAPE in isolation and has no
  view across packets at all.
- The four lifecycle families read a packet's HEADERS. Both packets' headers
  are impeccable — both ratified, both citing the same ruling.
- **The promotion-fidelity family reads 0 either way.** That is the load-bearing
  observation and it is why the class needs its own check rather than a wider
  version of the eighteenth: canon holds exactly what both packets said it
  should hold. The family whose whole job is comparing archived deltas to
  canon is, on this class, structurally blind.

The register already names the neighbourhood.
`docs/archive-record-discrepancies.md`'s PREVENTION addendum records the
eighteenth family landing and the class it retired; this is the class it did
not.

## What Changes

- **`document-lifecycle` gains the obligation.** ONE ADDED requirement:
  a ruling is discharged once, and an archived packet that restates another
  archived packet's ratified delta content names that packet in its proposal.
  The obligation had to be stated before a checker could enforce it, and it is
  a lifecycle rule about what archiving means — the sibling of the
  "Ratified spec deltas reach the promoted specification" requirement the
  eighteenth family's change added three days into the same campaign.
- **`doc-health` gains the check family.** One MODIFIED requirement (the count
  chain reaches twenty; the family reads neither the governed corpus nor the
  lifecycle scan set, so no census, word count, canon-share figure, inventory
  entry or catalog record moves) and one ADDED requirement defining the
  check: the content-identity rule, the lineage exemption, the borrowed C5 and
  disposition exemptions, the pinned basis, and the advisory launch.
- **The implementation lands in this change**, on the `add-promotion-fidelity-check`
  precedent: `scripts/doc_health/duplicate_packet.py`, its three registrations,
  three additive seams on the eighteenth family's module, and 25 tests over a
  fixture corpus that fires the reconstructed near-miss and stays quiet on
  every lawful pattern.

## Impact

- **Affected specs**: `doc-health` (MODIFIED + ADDED), `document-lifecycle`
  (ADDED).
- **Affected code**: `scripts/doc_health/` (one new module, three one-line
  registrations, three additive seams on `promotion_fidelity.py`),
  `tests/doc-health/`.
- **Measured effect on this repository's own health run**: **nothing moves.**
  A single-repo run at the branch point and the same run on this branch differ
  by four lines, and all four are the new family's own empty report section
  ("### duplicate-packet / Basis line absent by design / No findings."). The
  headline is `4 critical, 8 error, 73 warning, 4 info` before and after.
- **Measured effect on the real corpus, and it is the acceptance evidence that
  matters**: openxFactory's 91 archived packets yield 543 distinct
  (capability, requirement, content) identities. TWO of them are restated by
  more than one packet, and both are the original
  `2026-08-01-add-workbench-branch-sessions` and its landed remedial
  `2026-08-25-apply-branch-sessions-deltas` — the lawful pattern. The remedial's
  proposal names its original six times, so the lineage exemption clears both
  pairs and the family reports **0 findings**. Run with the lineage exemption
  disabled, the same corpus reports **2**. The exemption is not decoration:
  it is the only thing standing between this family and a false positive on
  the very remedy the eighteenth family's action line tells readers to perform.
- **Measured effect on every other repository**: unknown until an aggregation
  run, and deliberately so — the same reason the eighteenth family launched
  advisory.

## Orchestrator Decisions — FLAGGED FOR VETO

The commissioning ruling covers the decision to build this check. It does not
cover the four decisions below, which the orchestrating session took under
standing patterns. They are named here the way `add-promotion-fidelity-check`
named its own: taken, applied, and reversible on a word.

**D1 — What fires: content identity, never resemblance.** Two archived packets
fire only where they state the same `(capability, requirement title)` with
requirement bodies identical after trailing whitespace is normalized — per-line
trailing spaces and trailing blank lines — and in no other way. A re-wrapped
paragraph, a changed article, a reordered scenario: all different statements.
A content-SIMILARITY heuristic would be this family inventing judgement about
which two governance acts are "the same enough", which is exactly what a
deterministic family must not do, and the false positives it bought would land
on the ordinary case — 59 (capability, requirement) pairs in this repository
have more than one archived writer, and revising a requirement is not
restating it. The cost is a false NEGATIVE (a duplicate discharge that
re-wrapped one line goes unreported), which is the safe direction for an
advisory launch. The comparison is pairwise over all archived packets per
identity, so three restatements are three pairs and each is judged on its own.

**D2 — The lineage exemption, and it is what keeps the lawful remedy legal.**
The remedy for a promotion gap — codexFactory PR #85, and this repository's own
`apply-branch-sessions-deltas` — DELIBERATELY restates an original packet's
delta byte-faithfully, because applying already-ratified text is the point and
any edit would be new normative content smuggled in under an old ratification.
A family that fired on it would be reporting the fix its neighbour prescribes.
What separates the remedy from a double discharge is that the remedial packet
NAMES the original in its proposal, in either spelling the corpus uses (the
bare change id, or the archived folder). So: **a pair where either proposal
names the other's change id is a recorded remedial lineage and stays quiet.**
Two remedials of one original that do not name each other — tonight's shape —
fire against each other while both stay exempt against the original.

**THE NAMING IS LINEAGE-IN-THE-RECORD, NOT AN AUTHORITY CLAIM**, and the
distinction is load-bearing enough to state twice. Naming the original does not
make a restatement lawful; the ratification that makes it lawful is the
original's, and a packet claiming standing it does not have is the
`ratified-provenance` family's finding. What the naming does is make the second
statement TRACEABLE to the first, so a reader sees one ruling, one discharge,
and a recorded application of it — rather than two independent discharges that
happen to agree. This family reports untraceable restatement; it does not
adjudicate standing, and a build that let it start doing so would be
enforcement wearing an advisory label.

Two exemptions are borrowed rather than invented: a packet whose own proposal
declares a pre-ratification standing (the C5 rule, read through the eighteenth
family's own reader) discharged no ruling and can duplicate none; and
`health/dispositions.yaml` suppresses under the same contested-finding
discipline every other family applies.

**D3 — Report-only at launch, and BOTH halves of it.** Every finding is
`warning`, so no `--fail-on` configuration can red on this family. The less
obvious half: the family is deliberately absent from `FAMILY_RESOLUTION`, so
its findings are not classified `contested` — a contested finding that resolves
without a citation becomes an `error` under this capability's uncited-resolution
rule, which would red the nightly the first time anyone withdrew a duplicate
this family reported. The precedent is the eighteenth family's D3, taken for
exactly this reason four hours earlier. **The flip to enforcing is an open task
box in `tasks.md`, and it raises severity and adds the contested classification
TOGETHER.**

**D4 — Acceptance runs both directions, and the real corpus is one of the
directions.** The fixture reconstructs the near-miss (one original, two
byte-faithful remedials, each naming the original and neither naming the other)
and asserts it fires ONCE, on the remedial pair, never on the original. The
lawful patterns are asserted quiet: the PR #85 shape, successive MODIFIEDs with
different content, two pre-ratification packets restating one block. And the
REAL corpus at the branch point must read 0 through the lineage exemption,
which it does — measured, with the counterfactual measured beside it.

## Architecture: a sibling family, not a finding kind inside the eighteenth

The parsing is SHARED. This module owns no delta grammar, no status reader and
no disposition reader of its own; it reads archived deltas through
`promotion_fidelity.parse_delta`, the C5 exemption through
`promotion_fidelity.declares_pre_ratification`, and `health/dispositions.yaml`
through the same loader under its own family name. A second grammar for one
document's headings is how two readers of one document come to disagree about
what it says — the lesson that module already records about its own promoted
reader.

The FINDING is not shared, for a concrete reason rather than a taste.
Dispositions key on `(family, repo, path)`. Folding this class into
`promotion-fidelity` would let one disposition, recorded against a delta for a
promotion gap, silently suppress a duplicate-discharge finding on the same
delta — two different governance decisions bought with one citation, on a file
that is exactly the kind to attract both. The report's per-family counts would
conflate two questions whose remedies are opposite (apply the delta; withdraw
the packet), and the eighteenth family's one-line action text would be attached
to findings it does not describe. A test pins the separation.

**The basis differs deliberately.** The 2026-08-24 ruling (task 4.1, PR #315)
put the live-`main` basis on the promotion-fidelity family AND ON THAT FAMILY
ALONE, and its `basis_notes` tells every reader, on every run, that every other
family measures the checkout. This family keeps that sentence true by reading
the pinned checkout always, structurally — `_repo_trees` builds a `WorkingTree`
and nothing else, and a test asserts the module cannot even name the basis
option. The cost is bounded and the catch point is the right one anyway: a
duplicate arrives in the PULL REQUEST that adds the second packet, and a
repository's self-gate run reads its own tree at that tip. Moving this family
onto live mains is available as a ruling; it is not available as an
implementation detail.

## What this proposal does NOT claim

It does not claim this repository currently contains a duplicate discharge: it
measured, and it does not — the one restatement pair on record carries its
lineage. It does not claim the closed PR #317 was a defect; a human caught it,
and this change exists because the catch depended on the human. It does not
claim to have measured the domain factories: this change's evidence is
openxFactory's own archive and a fixture corpus, which is why the launch is
advisory rather than a claim this proposal makes. It does not adjudicate
whether a naming packet's restatement was WITHIN its authority — that is
`ratified-provenance`'s question and this family deliberately declines it. And
it does not touch `docs/doc-health.md`'s check-family table, which stopped at
twelve families six families ago; the gap is recorded in the eighteenth
family's `tasks.md` §5 and repairing it here would put unrelated report output
on this feature's evidence.
