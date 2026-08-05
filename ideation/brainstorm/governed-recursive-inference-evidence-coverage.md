# Recursive Evidence and Coverage — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Recursive results need a coverage ledger over the admitted corpus and provenance-preserving reductions so cited findings reveal not only what supports them but also what material was examined, skipped, failed, or left unresolved.
Topics: governed-recursive-inference, evidence-coverage, provenance, source-trace, audit, traceability, validation, source-authority, feat-request
Repository context: openxFactory (neutral coverage and evidence records); DomainxFactory repos (domain completeness and source-authority rules)
Captured: 2026-07-30

## Possible feats

- **Coverage ledger contract** — record the disposition of every in-scope
  shard or declared sampling unit.
- **Provenance-preserving reducer** — require aggregate claims to retain child
  evidence and source identity through fan-in.
- **Coverage-mode vocabulary** — distinguish targeted, sampled, partitioned,
  and complete analysis.
- **Independent coverage verifier** — compare the final result and ledger
  against the capsule manifest and task requirement.

## Focus

Citations answer "What supports this claim?" They do not answer "Did the
system inspect everything it claimed to cover?" Recursive inference can select
promising fragments and still miss an entire region of the corpus.

For xFactory use cases such as "find every incompatible contract," "assess all
repositories," or "reconcile every transaction," coverage is a separate
evidentiary property.

## Coverage modes

Candidate vocabulary:

| Mode | Meaning |
| --- | --- |
| `targeted` | inspect selected material relevant to a bounded question; no completeness claim |
| `sampled` | inspect a declared sample under a named method and denominator |
| `partitioned` | assign every required partition, while allowing item-level exclusions with reasons |
| `complete` | every required unit reaches an accepted terminal disposition |

The job or output contract selects the mode. The root cannot downgrade
`complete` to `targeted` because the corpus is difficult.

## Coverage ledger

The capsule manifest provides the denominator. A ledger could record per shard
or partition:

```text
not_required
queued
inspected
processed
excluded_by_policy
unreadable
failed
timed_out
superseded
duplicate_of
unresolved
```

Each disposition carries:

- capsule, shard, and range identity;
- child task and result refs;
- operation or transformation applied;
- validation status;
- exclusion or failure reason;
- source authority and sensitivity class;
- timestamps and attempt lineage.

The final coverage summary derives from this ledger rather than a root-model
statement such as "I reviewed all files."

## Provenance through reduction

Fan-in is where evidence commonly disappears:

```text
shards
  -> child claims with source refs
  -> deduplication
  -> aggregation
  -> final narrative
```

Candidate reduction rules:

- every atomic claim retains supporting and conflicting source refs;
- deduplication preserves all contributing child results;
- counts name the item set and exclusions used as the denominator;
- conflict is represented, not silently averaged away;
- low-authority evidence cannot become high-authority through repetition;
- synthesized prose links to structured claim and coverage records;
- unsupported reducer output fails validation.

## Independent verification

A coverage verifier should not depend only on the root's narrative. It can
deterministically check:

- manifest units equal processed plus permitted excluded/failed units;
- every mandatory partition has a terminal result;
- no child read a shard outside its declared view;
- all final claims resolve to child evidence;
- all source digests match;
- complete-mode outputs have no unresolved required units;
- sampling method and denominator match the declared plan.

A challenge worker may then inspect semantic gaps: suspiciously uniform
findings, missed contradiction classes, reducer bias, or unsupported
conclusions.

## Coverage versus correctness

Complete coverage does not guarantee correct interpretation. Every shard may be
processed by a weak prompt or model. Conversely, a targeted run can produce a
correct answer to a narrow question.

Evaluation needs separate dimensions:

```text
coverage completeness
schema validity
claim correctness
source support
conflict recall
calibration
```

The final artifact should avoid collapsing these into one confidence score.

## Handling oversized and volatile corpora

For a corpus that changes during execution:

- complete coverage should bind to one immutable manifest version;
- newly arriving material belongs to a new capsule or incremental follow-up;
- live brokered sources need read-version or timestamp evidence;
- unreadable or revoked items remain explicit ledger dispositions;
- partial completion may be useful, but cannot inherit a complete claim.

For massive corpora, a hierarchical coverage tree may aggregate leaf
dispositions while preserving drill-down.

## Alternatives and tensions

- Item-level coverage is auditable but expensive for millions of records.
- Shard-level coverage reduces overhead but can hide missed items inside a
  coarse shard.
- Model-authored coverage reports are cheap but not trustworthy enough for
  completeness claims.
- Complete coverage may encourage wasteful processing when a statistically
  valid sample would answer the decision question.
- Retaining detailed source refs improves audit but may expose sensitive
  metadata unless access is controlled.

## Open questions

- What is the neutral coverage unit: shard, record, semantic section, or
  task-declared item?
- Which outputs require `complete` rather than `targeted` or `sampled`?
- Can a deterministic validator certify coverage without access to sensitive
  shard contents?
- How should duplicate and superseded items affect denominators?
- What coverage evidence belongs in normal audit versus enhanced regulated
  disclosure records?
- Can a cached child result satisfy current coverage after revalidation?

## Relationships

- [Recursive Context Capsule](governed-recursive-inference-context-capsule.md)
  supplies the manifest denominator.
- [Trajectory and Replay](governed-recursive-inference-trajectory-and-replay.md)
  records how each disposition was produced.
- [Safety and Data Boundaries](governed-recursive-inference-safety-and-data-boundaries.md)
  constrains sensitive evidence retention.
- [Synthesis: Evidence and Safety](governed-recursive-inference-synthesis-evidence-and-safety.md)
  combines coverage, audit, and containment.

