---
code_surface: openxFactory (`scripts/doc_health/promotion_fidelity.py` — a new module owning the eighteenth deterministic family: the archived-delta parser, the promoted-spec reader, the latest-writer resolution and its tie-break, the ratification exemption, and the disposition read; `scripts/doc_health/families.py` — one registration line in `FAMILIES` and the note recording why the family is deliberately absent from `FAMILY_RESOLUTION`; `scripts/doc_health/__init__.py` — one entry in `FAMILY_IDS` so the family gets its own report section; `scripts/doc_health/corpus.py` — one new `RealGit` method, `first_commit_timestamp`, because `first_commit_date`'s day resolution cannot break a tie between two packets archived on the same day; `tests/doc-health/test_promotion_fidelity.py` plus `tests/doc-health/fixtures/promotion-fidelity*/` — the regression fixture reconstructing the historical true positive, the three known negatives, the structural pins on the advisory launch, and the tie-break's two-run disagreement; `tests/doc-health/conftest.py` — `FakeGit` gains the matching shim; `tests/doc-health/test_lifecycle_scan_set.py` — the eighteenth family classified as a non-reader of the lifecycle scan set, which is the loud failure that test was built to produce. NO change to the governed corpus, the lifecycle scan set, any existing family's behaviour, the report schema, the regression-diff rule, or any threshold. EXTENDED 2026-08-24 by task 4.1's two non-gate rulings (PR #315): `promotion_fidelity.py` gains the relaxed exemption (`declared_standing` / `_is_exempt_from_promotion`) and the two tree readers (`WorkingTree` / `GitRefTree`) the live-main basis needs; `corpus.py` gains `resolve_ref`, `ls_tree_paths` and `show_blob`, and an optional `ref` on `first_commit_timestamp`; `runner.py` gains the `--promotion-fidelity-basis` flag, the `Context` field, and the deviation line; `families.py` gains a one-entry `FAMILY_NOTES` registry; `__init__.py` gains `RunResult.notes`; `report.py`'s `render` gains an optional `family_notes` that prints under a family's own heading; `.github/workflows/doc-health-reusable.yml` gains a non-mutating live-main fetch step and passes the flag to the reporting run; `tests/doc-health/fixtures/promotion-fidelity-presumption/` and the new cases in `test_promotion_fidelity.py` / `test_workflow_contract.py` carry the evidence. STILL no change to the governed corpus, the lifecycle scan set, any OTHER family's behaviour or measurement basis, the report schema's finding and ranked-plan grammars, the regression-diff rule, or any threshold.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. The archive gate is therefore merge-plus-green on main, following `govern-openspec-corpus-membership` exactly: `python3 -m pytest tests/doc-health` green, `python3 -m pytest tests/ideation-dashboard -k workbench` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts and in no other line. The change therefore ships ACTIVE and archives only after the merge, which is the same sequence that change followed (its enforcement landed in `7157fa3e`/`bf0bda01` and its archive act was a separate later commit, `01ff3434`, titled for the merge it followed).
Status: ratified
Ratified: 2026-08-24 by Brett — in-session commissioning, verbatim: "commission the archived-delta-vs-promoted-spec check". The citation covers the DECISION TO BUILD THIS CHECK and nothing else; the four design decisions in § Orchestrator Decisions below were taken by the orchestrating session under standing patterns, are NOT covered by this citation, and are flagged there for veto. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing its three-way floor on two axes rather than the one it needs: approver (`by Brett`) and date (`2026-08-24`).
Proposed: 2026-08-24
Origin: `docs/archive-record-discrepancies.md` § FU-DOM-CODEX, the 2026-08-24 RESOLVED addendum's last sentence — "What does NOT close: no check yet compares archived deltas to promoted specs, so the class stays unreported. That prevention question is scoped to openxFactory's neutral tooling and recorded both in the packet and in PR #85's body — named, not dropped."
---

# Proposal: add-promotion-fidelity-check

## Why

**A ratified requirement can archive and silently never reach canon, and
every check in this corpus will report the repository healthy.** That is not
a hypothesis. codexFactory's archived
`2026-08-08-activate-nightly-sweep-council-clearance` ratified a MODIFIED
requirement, "Tier-2 ships inactive with report-only classification", carrying
SIX scenarios. The promoted `openspec/specs/merge-master-approval/spec.md`
carried the title with TWO. The four activation scenarios — "Activation
requires a freshly accepted record", "Active without a verdict still parks",
"Active with exact-head unanimous-ready evidence clears", "Removing verdict
visibility fails closed" — were absent from canon, and the archive commit never
touched that file. The gap survived from 2026-08-08 to 2026-08-24, was found by
a human re-deriving an unrelated discharge, and was closed by codexFactory
PR #85.

The register states why nothing caught it, in the sentence this change exists
to retire:

> No check reports this class (`openspec --strict` does not compare archived
> deltas to promoted specs; the lifecycle families read headers, not bodies).

And it left the prevention open by name rather than dropping it:

> What does NOT close: no check yet compares archived deltas to promoted
> specs, so the class stays unreported. That prevention question is scoped to
> openxFactory's neutral tooling and recorded both in the packet and in PR
> #85's body — named, not dropped.

**openxFactory has the same defect, right now, in its own archive.** The
implementation in this change was run against this repository before the
proposal was written, and it reports two findings — both against
`2026-08-01-add-workbench-branch-sessions`, both ratified, neither promoted:

| what the archived delta ratified | what `openspec/specs/lifecycle-notebook-projection/spec.md` carries |
| --- | --- |
| ADDED `Branch-session notebooks`, 5 scenarios | the requirement is absent entirely |
| MODIFIED `Corpus scan scope`, 4 scenarios | 3 of the 4; `A canon book is offered a branch session's drafts` is absent |

That is the same class, in the neutral repository, found by the check on its
first run. It is reported and deliberately NOT fixed here — applying a ratified
delta to canon is a governance act belonging to its own change, which is
exactly what codexFactory PR #85 was and exactly what this family's action line
tells a reader to do.

## What Changes

- **`document-lifecycle` gains the obligation.** ONE ADDED requirement stating
  that a ratified spec delta reaches its promoted spec, that a delta whose own
  proposal does not claim ratification is archived design evidence instead, and
  that the most recent archived delta is the authority for a requirement. The
  obligation had to be stated somewhere before a checker could enforce it, and
  it is a lifecycle rule about what archiving a ratified change means — the
  sibling of that capability's own "Proposal packets carry the lifecycle
  header".
- **`doc-health` gains the eighteenth check family.** One MODIFIED requirement
  (seventeen families becomes eighteen; the promotion-fidelity family reads
  neither the governed corpus nor the lifecycle scan set, so no census, word
  count, canon-share figure, inventory entry, or catalog record moves) and one
  ADDED requirement defining the check: the three resolution rules, the
  disposition mechanism, and the advisory launch.
- **The implementation lands in this change**, per the precedent this proposal
  follows: `scripts/doc_health/promotion_fidelity.py`, its registration, one
  new `RealGit` reader, and 27 tests over a fixture corpus that fires the
  historical true positive and stays quiet on all three known negatives.

## Impact

- **Affected specs**: `doc-health` (MODIFIED + ADDED), `document-lifecycle`
  (ADDED).
- **Affected code**: `scripts/doc_health/` (one new module, three one-line
  registrations, one new git reader), `tests/doc-health/`.
- **Measured effect on this repository's own health run**: `+2 warning`, and
  no other line moves. 0 critical, 0 error, 0 info; the canon-share headline,
  the per-stage census, the inventory and the catalog are untouched because
  the family reads neither document set. A run configured `--fail-on error` or
  `--fail-on critical` is unaffected by construction.
- **Measured effect on every other repository**: unknown until an aggregation
  run, and deliberately so. The family is advisory precisely because nobody
  has measured what the domain factories' archives will say, and the launch
  that reports first and gates later is the one this program has already ruled
  for domain findings.

## Orchestrator Decisions — FLAGGED FOR VETO

The commissioning ruling covers the decision to build this check. It does not
cover the four decisions below, which the orchestrating session took under
standing patterns. They are named here the way codexFactory PR #83 named its
two dispositions: taken, applied, and reversible on a word.

**D2's revision and D5 are RULINGS, not orchestrator decisions**, and are not
flagged for veto: both were taken by Brett on 2026-08-24 in task 4.1's
four-question round (PR #315), and both are recorded verbatim in that task.
They sit in this section because it is where a reader of D2 will look.

**D1 — Latest writer wins, with archive-commit order as the tie-break.**
For a given (capability, requirement title), only the most recent archived
delta is authoritative. Measured over this repository: 478 distinct
(capability, requirement) pairs, 59 written by more than one archived change,
and one — `doc-health`'s own "Deterministic check families" — written by TEN
between 2026-07-09 and 2026-08-24. Checking every writer instead of the latest
fires 20 findings where the latest-writer rule fires 2; the other 18 are
superseded text that canon is CORRECT to have moved past. Ties are real: 19
(capability, requirement) pairs are written twice or more on their latest date.
The tie is broken by the packets' archive-commit order from version control,
because folder-name order was MEASURED against it across all 19 groups and
disagreed on six. Folder name ascending remains the documented fallback for a
checkout without history; the fallback's cost is measured by a test that runs
the same fixture both ways and asserts they disagree.

**D2 — The exemption is the archived proposal's own `Status:` header.**
A delta is checked for arrival only where its own `proposal.md` claims
`Status: ratified`. This is not an invented marker: it is how the C5 decision
is actually recorded. `2026-06-26-enable-live-openxfactory` was archived by
Brett's own PR #28 with `--skip-specs`, and its 2026-08-23 supersession
addendum backfilled exactly one line to say so in the corpus's vocabulary —
`Status: draft`, "the honest value this folder has always supported: never
ratified, archived … retaining the four spec deltas as archived design
evidence rather than promoting them". The exemption is as narrow as the record
it implements: of this repository's 89 archived changes carrying spec deltas,
88 read `ratified` and exactly ONE reads `draft` — C5's. It exempts twelve
would-be findings, all four of C5's capabilities, and nothing else. The second
exemption is the existing `health/dispositions.yaml` mechanism, extended with
an optional `requirement:` key in the shape the neutrality lane's
`content_sha256` already set.

**D2 REVISED 2026-08-24 by ruling (Brett, task 4.1's four-question round,
PR #315) — the exemption relaxes to explicit-draft-only.** The rule now asks
the opposite question: archiving is PRESUMED to be ratification, and a delta is
exempt only where its packet's header explicitly declares `draft` or a lower
taxonomy standing. The original spelling was precisely narrow on openxFactory
and a false-negative channel everywhere else — an annotated ratification
(`Status: ratified (approved at commit 5ace969)…`) is not the string
`ratified`, and a packet with no header at all could buy silence by omission.
Four packets across hermes-install and medx-roottruth-install were exempt for
a decision nobody took, and with them 54 requirements; both repositories
reported zero findings at 57.8% and 0% coverage. The relaxation was measured
before it was ruled and re-measured on realization: openxFactory gives exactly
the same two findings under both spellings, +54 requirements are newly examined
across the family, and +0 findings appear anywhere. (The ruling's record says
57, from a run at a different reference point; the four packets are the same
ones. Both counts are kept — tasks §4.1.) C5 stays quiet because its own header says
`draft`. Reasoning and evidence: design D3 REVISED, tasks §3.8 and §3.10.

**D5 — The nightly measures live `main`s FOR THIS FAMILY (ruled 2026-08-24,
PR #315).** Measured against the aggregation's committed pins this family's
coverage collapsed — 0% in three repositories — and it could not see the #301
gap while the codexFactory pin lagged behind the repository that had it. A
promotion gap is a fact about a repository's own `main`. So the reusable
workflow fetches each governed submodule's `origin/main` (a fetch moves no
file) and passes `--promotion-fidelity-basis live-main` to the reporting run;
every other family still measures the pinned checkout, structurally — no other
module can name the option, and a test enforces that. The report states the
basis in the headline and per repository under the family's own heading,
including on a clean run, and names any repository whose live `main` could not
be read as having fallen back. Reasoning: design D7; evidence: tasks §3.9.

**D3 — Report-only at launch, and BOTH halves of that.** Every finding is
`warning`, so no `--fail-on` configuration can red on this family. The less
obvious half: the family is deliberately absent from `FAMILY_RESOLUTION`, so
its findings are NOT classified `contested`. A `contested` finding that
vanishes between reports becomes an `error` under this capability's
uncited-resolution rule — which would mean the nightly went red the first time
anyone actually promoted a delta this family reported: enforcement arriving
through the back door on the very run that proved the advisory launch worked.
`auto-fixable` is also the honest label for the remedy, which PR #85
demonstrated is a byte-level application of already-ratified text (its delta
hashed identical to the archived delta, and the requirement block extracted
from canon after promotion diffed identical). The governance judgement is
whether to apply or to record a deliberate non-promotion, and that judgement
is in the action line a reader acts on. **The flip to enforcing is an open
task box in `tasks.md`, not a silent later commit, and it raises severity and
adds the contested classification TOGETHER.**

**D4 — The finding lands on the archived delta's path, not the promoted
spec's.** The delta is the document that made the claim that went unmet, its
path is stable because it is an archived record, and it is what a disposition
needs to key on. The promoted spec it failed to reach is named in the rule
text, which is what a reader acts on.

## What this proposal does NOT claim

It does not claim the two findings it raises against this repository are new
defects: both predate it and were invisible only because no check compared the
two documents. It does not fix them — that is a governance act and belongs to
its own change, exactly as codexFactory PR #85 was. It does not claim to have
measured the domain factories: this change's evidence is openxFactory's own
archive and a fixture corpus, and what the pinned domains' archives will say
is the reason the launch is advisory rather than a claim this proposal makes.
And it does not touch `docs/doc-health.md`'s check-family table, which stopped
at twelve families five families ago; repairing another capability's
registration inside this change would put unrelated report output on this
feature's evidence, and the gap is recorded in `tasks.md` §5 instead.
