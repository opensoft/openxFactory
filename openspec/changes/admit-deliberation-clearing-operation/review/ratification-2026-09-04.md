# Proposal Ratification: admit-deliberation-clearing-operation

Status: ratified
Decision date: 2026-09-04
Ratifier: Brett Heap (repository owner) — in-session, on the recorded word
Ratified: 2026-09-04 by Brett Heap (repository owner) — in-session at
2026-09-04T12:37Z, verbatim: *"D10 A, D13 A, ratify #645"*.
Ratified baseline: head `22afb198049652ab30afd74eee62ce3c308da930` — "Review
round 2: put D13's ruling question last in its section (no substantive
change)" — `proposal.md`, `design.md`, `tasks.md`, `.openspec.yaml`, and
`specs/clearing-dispatch-boundary/spec.md` (ONE ADDED requirement, seven
scenarios) as they stood at that commit.
Recorded at: https://github.com/opensoft/openxFactory/pull/645#issuecomment-5540528358
Lane: `hermes-wallet-exercise`, session `45aa0e5f-e855-4bd3-bed3-5b4275dc70f9`

## Decision

**RATIFY. THE MERGE IS A SEPARATE WORD, AND IT WAS NOT GIVEN.** Unlike
`add-cpc-clearing-boundary`, whose ratifying word carried both acts in one
instruction (*"Ratify + merge openxFactory #560"*,
`review/ratification-2026-09-02.md`), this word ratifies and rules and says so
in terms: the ruling comment closes *"Merge is a separate word."* This record
therefore records a ratification and nothing else — no merge, no draft-state
change, no realization.

**The word carried THREE acts, and this record carries all three.** Two
rulings that had been PUT as questions at review round 2 — design D10 and
design D13, each stated with both readings and the cost of each under a `THE
QUESTION, PUT FOR RULING` heading — were ruled **A**, the packet's own
reading, in the same sentence that ratified the packet. **Nothing substantive
in the packet moves as a result**, which is exactly what a ruling for A means
here: both questions were written so that A is the text as it stands and B is
an executable edit. B was not chosen, so no edit is owed.

## What is ratified

**ONE ADDED requirement on the capability `clearing-dispatch-boundary`** —
*"deliberation is register entry number two and returns evidence only"*, with
seven scenarios — written over the basis
`add-clearing-dispatch-boundary`'s RATIFIED (2026-09-01), REALIZED (PR #628,
`0d5e1ba9`) but UNARCHIVED `## ADDED Requirements` block. The pairing is
declared in PROSE rather than with `govern-sibling-added-modified-deltas`'
reserved marker, because that marker is a MODIFIED-block form and this is an
ADDED one — the reading the sibling `add-cpc-clearing-boundary` already ships
(markers on its three MODIFIED requirements, none on its ADDED block).

**This packet is the governed change the ratified basis demands by name.** The
basis's requirement *"The permitted-operations register is closed"* holds that
"ADDING AN OPERATION SHALL BE A GOVERNED CONTRACT CHANGE with a spec delta and
a reviewer, and SHALL NOT be a workflow edit"; the realized register instance
says `deliberation` "IS NOT HERE ON PURPOSE … a LATER GOVERNED CHANGE" and
uses the name as the fixture proving the refusal fires. codexFactory PR #165
(`adopt-bundle-shaped-deliberation`) carries it as tasks.md **1.6** on design
**D13**'s finding that "leg 3 has no legal home until this lands".

**The entry's ratified facts**, as the requirement fixes them: **ARTIFACT LANE
ONLY** (`xfactory-artifact-workers` / `host-rider-cpc-brett01` /
`xfactory-artifact-cpc-brett01`; a coding-lane request is refused
`lane_not_permitted`); `checks_out_code` / `writes` / `may_reference_secrets`
all **false**; `token_scopes: [actions:read]`; `worker_profile:
council-deliberation-worker`; `data_handling: internal-governance`;
`repository_affecting_output: false` — the return is EVIDENCE, the verdict is
computed by the runtime, and no seat key is ever on the host. The declared
`output_schema_ref` is a NEW NEUTRAL
`contracts/clearing/deliberation-return.schema.yaml` of the ratified kind
`xfactory_clearing_deliberation_return`.

## The two rulings

### D10 — RULED A (2026-09-04)

*The question put:* does the basis's requirement *"Routing a route through the
clearing lane retires the old route"* — and its scenario *"WHEN a change adds a
clearing operation for work an existing direct route still performs THEN the
change MUST be refused as leaving a dormant second door"* — reach THIS
admission, or only the act that declares the host job?

*Ruled:* **A, the packet's reading.** Admitting the register entry with no host
job declared in any repository is **NOT a second door**: nothing can be
dispatched through it, and the grandfathered direct route
(`council-deliberation-worker.yml` in `xfactory-artifact-workers`, `cpc_jobs`
`deliberate` and `smoke-seat`, `allowlist_entry: present`) remains the only
route. The basis scenario therefore reaches **the change that DECLARES the
`deliberation` host job**, onto which this requirement binds the retirement of
that worker's host jobs, its workflow-allowlist entry and its
grandfather-enumeration row, **in the same act**.

*What it settles:* the forward binding stated in design D10 and encoded as the
requirement's seventh scenario ("The host job lands while the direct route
still stands") is the ratified reading. **Nothing in the packet moves.** The
alternative — Reading B, holding the admission until the retiring xFactory
change lands beside it — was declined; it was coherent only as a single act
across two repositories in one reviewed window, because codexFactory #165
design D13 makes the xFactory change unauthorable ahead of the admission it
depends on.

### D13 — RULED A (2026-09-04)

*The question put:* three refusal grounds now, or two?

*Ruled:* **A, the packet's reading.** **EXACTLY THREE** record grounds are
admitted to `contracts/clearing/dispatch-record.schema.yaml`'s CLOSED
`refusal_ground` enumeration by this ratified text — `lane_not_permitted`,
`output_schema_failure`, `origin_scoped_credential` — carrying that
enumeration from two members to five. They are the three of the record's nine
awaited grounds that this entry's landing makes emittable, each a rendering of
a name the record's own description already awaits in prose, in the identifier
form the two seeded members carry; no concept is coined and **no finding code
is minted**.

*What it settles:* a realizer may not widen a closed enumeration on their own
authority, and scenario six's refusal is recordable rather than free text.
**Nothing in the packet moves.** Reading B — admit only two and leave
`origin_scoped_credential` to the change that declares the host job — was
declined; it would have been executed by striking one bullet from the
requirement, one member from task 2.9, and one row from the proposal's fact
table.

## Standing of the two earlier acts this ratification rests on

Neither is ratification of content, and this record does not restate them as
such:

- **The clearing-boundary ruling of 2026-09-01** (Brett Heap; operator
  workspace `cpc-clearing-boundary-ruling-2026-09-01.md`; `opensoft/codexFactory`
  issue #156) — the ruling that made the register CLOSED and admission a
  governed change.
- **The OQ1 ruling of 2026-09-04**, verbatim *"Ruling OQ1: new neutral
  deliberation-return schema"*, recorded as a Lane Collision Protocol Rule 2
  ruling comment on codexFactory PR #165
  (https://github.com/opensoft/codexFactory/pull/165#issuecomment-5535775096),
  naming its target as this lane's Rule 1 claim on the `deliberation` register
  member
  (https://github.com/opensoft/codexFactory/pull/165#issuecomment-5535747335).
  It is authorization to author, and it is encoded as design D4.

## Review history

**Two adversarial rounds ran on 2026-09-04**, both recorded in the packet, and
this record carries their verdicts rather than re-litigating them.

1. **Round 1** — `review/adversarial-round-1-2026-09-04.md`, entered at head
   `a47bdb6d`. **Nothing was refused.** Its blocking finding **P1-1** was a
   closed enumeration left for a realizer to widen: the scenario "The return
   does not validate against the declared neutral schema" required the refusal
   ground to be "a member of the closed refusal enumeration, added by a
   governed change rather than recorded as free text" — and named no ground.
   The cure was to NAME the grounds in ratified text, which is what created
   the D13 question. Round 1 also produced the record kind
   `xfactory_clearing_deliberation_return` and the no-code-is-minted sentence.
   Closed at `47f3e2f5` with all seven required checks green
   (https://github.com/opensoft/openxFactory/pull/645#issuecomment-5536332388).
2. **Round 2** — `review/adversarial-round-2-2026-09-04.md`, entered at
   `47f3e2f5`, after a catch-up merge (`ef65be6c`, merging `origin/main`
   `342bee51`). **Its subject was what round 1 ADDED**, new ratified text being
   what a second pair of eyes owes attention. **Nothing was refused.** Every
   finding was fixed in place except the two only the operator could rule,
   which were unchanged in substance and were **PUT as questions** rather than
   only flagged — the change that made this ruling possible. No round 3 was
   owed: round 2 refused nothing and surfaced no third question.

**The packet authors NO contract byte at the ratified head.** At `22afb198`,
`git diff origin/main --stat` is the packet directory, the README's OpenSpec
Records block, and one `tests/sequenced_after/corpus-ledger.yaml` row.

## Check state at the ratified head

**All seven required checks green at `22afb198`** — recorded in the round-2
close comment
(https://github.com/opensoft/openxFactory/pull/645#issuecomment-5540480383):
`clearing-dispatch-gate`, `lane-line`, `merge-master-approval`,
`openreposhape-pin`, `pytest-suite` (21m04s), `signed-execution-chain-gate`,
`wallet-validation`. Re-verified from the lane's main session at 12:35Z on the
pushed head: `openspec validate admit-deliberation-clearing-operation
--strict` valid; `openspec validate --all --strict` 89 passed / 0 failed;
`pytest tests/clearing tests/sequenced_after` 334 passed. The branch was
current with `main` (`342bee51`) and `mergeStateStatus` was BLOCKED on the
code-owner gate only.

## What this ratification authorizes

**Realization, and it does not perform it.** The contract bytes are a SEPARATE
SPECKIT SLICE (`tasks.md` Phases 2–4), and the archive gate is
`release-realization`'s merged-plus-green realization evidence, ORDERED AFTER
`add-clearing-dispatch-boundary` archives — this packet's addition rests on
that packet's unarchived one.

Authorized, none of it done here:

1. **`contracts/clearing/permitted-operations.registry.yaml` gains ENTRY
   NUMBER TWO**, together with the **FIVE frozen copies** of the member set
   that must move in the same reviewed diff (design D9): the validator's
   `RATIFIED_OPERATIONS`, the independent copy in
   `tests/clearing/test_register_closure.py`, the register instance,
   `.github/workflows/clearing-dispatch-gate.yml`'s literal
   `(1 registered operation)`, and `tests/clearing/test_clearing_gate_wiring.py`'s
   assertion pinning that same literal from a second file.
2. **The NEW neutral `contracts/clearing/deliberation-return.schema.yaml`** of
   kind `xfactory_clearing_deliberation_return`, with a positive example and at
   least one negative fixture, registered in `SCHEMA_FILENAMES` and
   `KIND_TO_SCHEMA`, and the verdict scan extended to reach that kind.
3. **The `refusal_ground` widening by exactly the three members D13 ruled**,
   and no others.
4. **The fixture re-point to `coding`** so the closure refusal keeps a live
   probe, and the manifest, CHANGELOG and README rows at the next ADDITIVE
   minor — allocated at realization by merge order, never reserved.
5. **The consumer's dependency tick**: codexFactory #165 tasks.md 1.6 is a
   DEPENDENCY task on this change (`tasks.md` 1.7), to be reported there with
   the ratified head and, when it exists, the merge sha.

**What this ratification does not do:**

- **It does not move a contract byte.** The register instance still holds
  exactly one member on this branch, the validator's frozen set still holds one
  name, and `clearing-dispatch-gate` still asserts "1 registered operation".
- **It does not merge PR #645**, and the ruling says so: *"Merge is a separate
  word."*
- **It does not declare the `deliberation` host job**, in this repository or
  any other. Under D10's ruling that is the act the retirement obligation
  binds, and it is an `opensoft/xFactory` change this packet cannot author.
- **It does not re-open D2, D3, D5, D6, D7, D8, D9 or D11.** Each was flagged
  for veto in the ordinary way and none was vetoed; ratifying the text carries
  them as drafted.

## Open questions

**None are carried open.** OQ1 was SETTLED by Brett Heap on 2026-09-04 and is
encoded as design D4, not as an open question (`tasks.md` 1.5). OQ2 was
RESOLVED BY MEASUREMENT in design D11 — the live pin is the per-change ledger,
this packet adds exactly ONE row, flips no partner, and owes no MOVEMENT LOG
entry (`tasks.md` 1.6). D10 and D13, the only two questions still standing at
the ratified head, are ruled above.

## Verification (at the recording head, over the ratified baseline)

- `OPENSPEC_TELEMETRY=0 openspec validate admit-deliberation-clearing-operation
  --strict`: valid, zero issues.
- `OPENSPEC_TELEMETRY=0 openspec validate --all --strict`: 89 passed, 0 failed.
- `python3 scripts/proposal-support.py . verify`: ok.
- `python3 scripts/doc-health.py --single-repo .`: exit 0, unchanged against
  the pre-recording baseline (6 critical / 4 error / 27 warning / 16 info, 0
  new regressions), and **no finding names any path of this packet** —
  `ratified-provenance` included, this record and the proposal each carrying
  exactly one ratification citation line.
- `python3 -m pytest tests/sequenced_after -q`: 162 passed. A `Status` flip
  moves no ledger row, and the measurement confirms it.

## Next

1. **The recording acts of this ratification** — this record, `Status:
   ratified` and the `Ratified:` line on `proposal.md`, D10/D13 marked ruled in
   `design.md`, `tasks.md` 1.1 ticked, and the README OpenSpec Records row
   moved off "awaiting Brett's ratification word" — land on top of the ratified
   head as one commit.
2. **Merge of `opensoft/openxFactory#645`** awaits a separate word from Brett
   Heap. `mergeStateStatus` is BLOCKED on the code-owner gate.
3. **Realization** per `tasks.md` Phases 2–4, as a Speckit slice, after the
   merge.
4. **Archive** per `release-realization`: merged plus green realization
   evidence, and ORDERED AFTER `add-clearing-dispatch-boundary` archives.
