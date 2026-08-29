---
code_surface: openxFactory (`scripts/doc_health/families.py` — four module-level helpers above `fam_staged_candidate_aging` (`_archived_change_ids`, `_exit_taken_lines`, `_index_section`, `_topic_outcome`) plus two constants, and in the family's staged-topic arm a `continue` on a recorded outcome and a corrected action line; no other arm of that family, no other family, no threshold, no `Finding` field, no report or ranked-plan grammar, and no new check family — `FAMILIES` is unchanged and the family enumeration and its counts do not move. `tests/doc-health/fixtures/staged-topic-outcomes/` — a new six-topic fixture tree at ONE age, so the only thing separating the topics is the outcome each records. `tests/doc-health/test_families.py` — three new tests and one moved action-line pin. The governed-corpus half is documentation: `ideation/staging/INDEX.md` (nine rows, one detail bullet) and eight staged fragments under `ideation/staging/`.)
target_release: implemented — the openxFactory main line. This surface cuts no contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, no release tag is owed. The archive gate is merge-plus-green on main, following `add-unclassified-finding-class` and `add-family-enumeration-check`: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount § Impact predicts and in no other line. The change ships ACTIVE and archives only after the merge.
Status: ratified
Ratified: 2026-08-28 by Brett — the four bulk rulings recorded in `.openspec.yaml`, given as answers to a read-only triage survey's multi-choice questions. The citation covers the DECISIONS THE RULINGS TOOK and nothing else; the five design decisions in § Orchestrator Decisions were taken by the authoring session under standing patterns, are NOT covered by it, and are flagged there for veto. No approving OpenSpec change exists to name, so this cites the record in the spelling `sanction-ratified-record-spelling` sanctioned for that case, clearing its three-way floor on two axes: approver (`by Brett`) and date (`2026-08-28`).
Proposed: 2026-08-28
Origin: the `staged-candidate-aging` population of the 2026-08-28 single-repo doc-health run — fourteen staged topics warning, surveyed read-only by the orchestrating session and put to Brett in four groups.
---

# Proposal: settle-aging-staging-topics

## Why

**The aging family reads one fact about a staged topic, and it is the wrong
one on its own.** `fam_staged_candidate_aging`'s staged-topic arm asks git for
the topic folder's last commit date and asks nothing else. It reads no
`Status:`, no register row, no exit record. So a topic whose work is FINISHED —
every exit change ratified, realized and ARCHIVED, the folder deliberately
retained as provenance because that is what the document lifecycle asks for —
ages exactly like a topic nobody has looked at, and the finding tells a reader
to "progress the topic to a proposal" that was raised, landed and closed weeks
ago.

**Six of the fourteen warnings on 2026-08-28 were that.** Not five, not a
suspicion: the survey resolved each one at its own archive tree.

| Topic | Exits, all archived | Verified at |
| --- | --- | --- |
| `github-administration-plane` | `2026-07-14-add-github-app-identity-tiers`; `2026-07-15-add-github-administration-workflow` | openxFactory; OpsxFactory |
| `client-layer-tuning` | `2026-07-24-add-client-layer-tuning-contracts`; `2026-07-24-add-client-layer-defaults`; `2026-07-24-add-client-tuning-and-seeding` | openxFactory; codexFactory; hermes-install |
| `codexfactory-domain-hermes-content` | `2026-07-22-add-domain-hermes-roles-and-policies`; `2026-07-23-add-domain-hermes-councils-and-memory` | codexFactory |
| `layer-content-materialization` | `2026-07-23-add-hermes-domain-overlay-contract`; `2026-07-23-add-layer-content-materialization` | openxFactory; hermes-install |
| `medxfactory-domain-hermes-content` | `2026-07-29-add-domain-hermes-roles-and-policies`; `2026-07-30-add-domain-hermes-councils-and-memory` | MedxFactory |
| `dashboard-repo-selector` (exit 1) | `2026-08-01-add-dashboard-repo-selector` | openxFactory |

**One of those six was ALREADY marked `superseded` and warned anyway.**
`github-administration-plane` has carried `Status: superseded` with a
`Superseded by:` line naming both archived exits since 2026-07-15. It kept
warning for forty-two days, which is the proof that the defect is in the
family's reading and not in the corpus's record-keeping — no amount of
diligent authoring could have silenced it.

**And the action line named an act that cannot be performed.** It read
"progress the topic to a proposal or mark it deferred". There is no `deferred`
value in the `document-lifecycle` taxonomy for a staged topic and there should
not be: a deferral is a schedule, not a standing. So the line offered a
remedy that half of its readers could not take, and the half who could take it
had already taken it.

**This is `clean-doc-health-floor`'s finding, arriving from the other side of
the same lifecycle.** That change (PR #465, merged 2026-08-28) fixed
`location-conformance` demanding that staged material "move into the proposal
supporting-docs folder" of packets that had ARCHIVED — a closed folder and an
impossible act. Same class here: a finding whose remedy names an act nobody
can perform is a finding with no conforming resolution. It fixed that by
splitting `corpus.active_change_ids` off the union; this reads the same split
from the other end.

## What Changes

**W1 — the family learns to read a recorded outcome** (`families.py`). Two
records stop a staged topic ageing, and no others:

1. its primary fragment carries `Status: superseded` or `Status: retired` —
   and `fam_succession_integrity` already requires the first to name a
   resolvable successor and the second a reason, so the silence cannot be
   bought by an empty claim;
2. an `Exit taken:` line, in the repository's staging-index entry for that
   topic or in the primary fragment itself, names a change that has ARCHIVED.

A citation of an ACTIVE change does NOT stop it: that topic's proposal is in
flight, its staged material is the move `location-conformance` is
concurrently reporting, and hiding the age would hide half of one live
obligation. `Exit taken:` inside a code fence is an EXAMPLE of the grammar and
stops nothing. The archived set is unioned and subtracted ACROSS repositories,
so an id active anywhere is archived nowhere; a single-repo run that cannot
see the other factory's tree resolves nothing and the topic keeps ageing,
which is the honest answer for a run that cannot read the evidence.

**W2 — the action line is corrected to what the family honours**, replacing
the unperformable "mark it deferred".

**W3 — the six completed topics record their outcomes** (R1). Four take
`Status: superseded` with a `Superseded by:` line naming every archived exit
and a new `## Outcome (recorded 2026-08-28)` section carrying the table;
`github-administration-plane` needed no edit at all and is silenced by W1
alone; `dashboard-repo-selector` takes the `Exit taken:` record instead of
`superseded`, because its exit 2 is unproposed and a `superseded` primary
fragment would close a topic that still holds live design (OD-1).

**W4 — five topics record a deferral with its gate named** (R2, R4).
`worker-host-app` and `context-compression-runtime` behind the worker chain;
`proposal-origin-contract` behind a regulated domain that needs the FDA SaMD
rationale; `layer-vocabulary-machine-migration` behind the next hermes-runtime
major; `ideation-action-plane` fragment 2 behind the unowned Drive↔NLM
markdown-ingestion spike. **None of these five is silenced, and each record
says so in its own text.** A deferral is a schedule; the topic keeps ageing.

**W5 — four bookkeeping refreshes** (R3, R4). `subject-establishment`'s
readiness line said its Ledgerx gate was "in flight" and its exit "gated on
Ledgerx reaching proposal"; that gate CLEARED on 2026-08-04. Fragment 1 of
`ideation-action-plane` is an ACTIVE change at 13/17 tasks, not merely
"raised". `dashboard-repo-selector`'s open questions 7–9 were closed by
Brett's rulings of 2026-07-26 and stood open in the fragment for a month.
`medxfactory-domain-hermes-content`'s row described change B as outstanding;
it archived 2026-07-30. And the AGGREGATION repository's `HANDOFFS.md` carries
a stale broker row — corrected text recorded in `tasks.md` § 6 for the
orchestrating session to land, because that file lives in a shared dirty
checkout this packet must not touch.

## Impact

**The rule's effect, measured at a COMMON as-of so a folder touched by this
change cannot be mistaken for a folder silenced by it.** Every edit in W3–W5
writes into a topic folder, which resets that folder's last commit date and
buys thirty days of silence that has nothing to do with the rule. Measuring
today would therefore flatter the change. Both trees were run at
`--as-of 2026-12-31`, by which date every one of the 33 topics is old enough
to fire under either reading:

| Run | staged-topic aging findings |
| --- | --- |
| `origin/main`, `--as-of 2026-12-31` | 33 |
| this branch, `--as-of 2026-12-31` | 27 |

The six that go quiet are exactly the six in § Why's table, and they go quiet
PERMANENTLY. Nothing else moves.

**The run as it stands today, RE-MEASURED on the merged head.** The first
numbers this section carried were taken against `e4bcbdb1`'s base and with
§ 4's corpus edits still UNCOMMITTED; both halves have since moved, neither
for a reason this change caused, and both are restated rather than left
standing. Single-repo, default as-of: `4 critical, 7 error, 41 warning, 13
info` → `4 critical, 7 error, 30 warning, 13 info`. Per family, before →
after: `staged-candidate-aging` 15 → 4 and EVERY OTHER FAMILY UNCHANGED —
`staged-topic-template` 27, `modified-block-currency` 9, `record-immutability`
4, `tag-hygiene` 4, `location-conformance` 3, `ideation-routing` 2,
`document-catalog` 1, before and after.

**Two corrections, each with its cause named.** The BASELINE moved because
main advanced: `record-immutability` went 5 criticals → 4 when
`declare-generated-projection-status` landed, and `modified-block-currency`
8 → 9 and `info` 12 → 13 from the same window. Not this change; the before
and after columns move together and the invariant they were written to state
— no family but `staged-candidate-aging` moves — holds unchanged. The AFTER
column moved because § 4's edits are now COMMITTED, which is precisely the
mtime reset § 5.3 predicted, arriving early: the five deferred topics fell
silent on merge rather than after it, so today's staged-topic warnings read
14 → 3 instead of 14 → 8.

**Which is why the load-bearing number is the other one, and it did NOT
move.** Re-run on the merged head, `--as-of 2026-12-31` still reads **33 →
27**, still exactly the six topics of § Why's table — that measurement was
built to be immune to the mtime reset, and it was.

**What the number will do next, said plainly.** The three topics warning
today are `client-credential-escrow-registry`, `subject-establishment` and
`worker-enrollment-broker`, which is correct — all three are live work. The
five this change WROTE INTO (`worker-host-app`, `context-compression-runtime`,
`proposal-origin-contract`, `layer-vocabulary-machine-migration`,
`ideation-action-plane`) are silent by MTIME RESET, not by rule, and they
return on 2026-09-27 still deferred and still unstarted.

**Tests**: `python3 -m pytest tests/doc-health tests/proposal-support
tests/ideation_routing tests/document_catalog` 1455 passed, zero failed on
the merged head.

## Orchestrator Decisions — FLAGGED FOR VETO

**OD-1. `dashboard-repo-selector` takes the exit record, not `superseded` —
five topics marked `superseded`, not six.** R1 named six topics and this
packet closes six, but not all by the same means. Exit 1 archived; exit 2 (the
runtime plane) has never been proposed and its gating design decision (open
question 3, what an "idea" IS as governed install content) is live. A
`superseded` primary fragment would declare a topic closed while it still
holds unproposed design, and `superseded` means "replaced by a later delta" —
nothing has replaced exit 2. The exit-taken record says the true thing (a
proposal was raised and archived) and produces the identical silencing, so the
count in § Impact is unaffected. **Veto → mark it `superseded` too**; nothing
else in the packet changes.

**OD-2. `Exit taken:` is a new line, and it is deliberately NOT a status.**
The alternative was a `deferred` value in the lifecycle taxonomy, which is
what the old action line implied existed. Rejected: a deferral is a schedule
and would silence the five W4 topics, which are precisely the topics that
should keep asking to be looked at. `Exit taken:` records a fact that already
happened rather than a wish about the future, needs no `document-lifecycle`
delta (that capability's header set is open — `Kind:`, `Ratifier:`,
`Decision date:`, `Staging ID:`, `Source:` all coexist), and adds no value to
the controlled taxonomy. **Veto → the record moves into
`document-lifecycle` as a governed header with its own delta.**

**OD-3. The index is read per-topic-section, not per-file.** `_index_section`
binds an `Exit taken:` line to the `## <topic>` heading above it. Read
file-wide, one topic's exit record would silence the entire register — a test
pins that boundary in both directions. **Veto → require the marker in the
primary fragment only, and drop the index reader**; two of the three silenced
topics would then need a fragment edit they do not need today.

**OD-4. A MODIFIED block on `Aging threshold defaults`, not an ADDED
requirement.** The promoted text pins the mtime-only reading in its own words
("staged topics … untouched 30 days are `warning` findings"), and it already
carries the exact analogue of this exclusion one clause later — "`routed`,
`rejected`, and explicitly `deferred` routing records SHALL NOT age as
unresolved work". An ADDED requirement would leave the pinned sentence
standing and contradicting it. Collision was checked: of the active changes
holding `doc-health` deltas, `add-nightly-dashboard-refresh` and
`fix-pin-value-boundary-and-sentinel-split` are ADDED-only, and
`clean-doc-health-floor`'s single MODIFIED is on a DIFFERENT requirement
(`Proposal supporting-document integrity checks`). No two MODIFIED blocks meet.
**Veto → restate as ADDED and accept the standing contradiction.**

**OD-5. The four `superseded` fragments cite cross-repository successors by
URL.** `fam_succession_integrity` resolves a `Superseded by:` target against
the DOCUMENT'S OWN repository, so a codexFactory or MedxFactory archive path
cannot resolve from openxFactory; the family treats an `http(s)` target as
resolved without checking it. Two fragments have an openxFactory-local path to
cite and cite it first; the codex and Medx ones have none and cite
`https://github.com/…` markdown links. **Veto → the successor citation
mechanism for cross-repository exits becomes its own change**, and these two
fragments keep `Status: staged` until it lands.

## Open questions — recorded with recommendations, not fixed here

1. **Should an exit record expire?** A topic whose exit 1 archived is silent
   forever, even if a live exit 2 sits behind an unscheduled gate —
   `dashboard-repo-selector` is exactly that shape today. RECOMMENDATION: no,
   not yet. The register's readiness cell carries the remaining fragment and
   the topic is genuinely not "untouched and unprogressed". Revisit if a topic
   parks a live fragment behind a landed exit for a quarter.
2. **`staged-topic-template` does not read `Status` either.** It emits a
   finding for `github-administration-plane`'s `superseded` fragment, and will
   now emit one for each of the four this change closes — 27 findings, none of
   which moved. RECOMMENDATION: the same skip belongs there, as its own
   change; deliberately out of scope here so this packet moves one family.
3. **Three repositories with staged topics keep no staging index.**
   MedxFactory (4 topics), OpsxFactory (7) and LedgerxFactory (6) have no
   `ideation/staging/INDEX.md`, so only the fragment-header form of the exit
   record is available to them. RECOMMENDATION: leave it; the fragment form is
   the portable one and was included for exactly this reason.
4. **DTN-017 still reads `staged`** in
   `docs/domain-neutralization-candidate-register.md` although
   `subject-establishment`'s Ledgerx gate cleared on 2026-08-04. FLAGGED, NOT
   FIXED, per R3: the agent filing that topic owns the row.

## What this proposal does NOT claim

- It does NOT claim the eight remaining warnings are wrong. Three are live
  work and five are deferred work; both should warn.
- It does NOT move the `worker-enrollment-broker` supporting-docs. That act
  collides on `ideation/staging/INDEX.md` and `ideation/cross-reference.md`
  and is dispatched separately after this lands (R2).
- It does NOT edit `subject-establishment` or
  `client-credential-escrow-registry` beyond one INDEX readiness line, and it
  edits neither topic's documents (R3). `client-credential-escrow-registry`
  received NO edit at all: its row's text was checked and found still true.
- It does NOT touch the aggregation repository's `HANDOFFS.md`. The corrected
  row text is recorded in `tasks.md` § 6 for the orchestrating session.
- It does NOT introduce a `deferred` lifecycle state, a new check family, a
  new severity, a new finding class, or a threshold.
