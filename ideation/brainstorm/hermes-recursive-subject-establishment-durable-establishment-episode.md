# Durable Subject-Establishment Episode — Brainstorm

Status: brainstorm
Kind: architecture
Summary: Subject establishment should be a durable, event-driven episode composed of bounded Hermes recursive-inference passes rather than one continuous model session or one batch import.
Topics: hermes-recursive-subject-establishment, durable-establishment-episode, subject-establishment, subject-hermes, workflow
Repository context: openxFactory neutral Subject Hermes lifecycle with domain-specific intake and maintenance profiles
Captured: 2026-07-30

## Possible feats

- **Subject-establishment episode record** — persist purpose, state, evidence
  frontier, budgets, waits, reviews, readiness, and terminal disposition across
  many bounded runs.
- **Event-driven resume** — reopen reasoning when a requested record, source
  update, correction, consent change, or review result arrives.

## Focus

A company intake may wait on contracts and vendor confirmations for weeks. A
patient intake may wait on several clinics, an insurer, an imaging center, and
a pathology lab. One inference request cannot safely remain live for that
period, and a single batch import cannot adapt when each received record
reveals another source.

The durable unit should therefore be a `subject_establishment_episode`.
Individual Recursive Language Model (RLM) passes remain finite and replayable;
the episode supplies continuity.

## Proposed model

```text
seeded
  -> discovering
  -> acquiring / waiting
  -> processing
  -> reconciling
  -> review_ready
  -> provisionally_established | established_with_gaps | established
  -> maintaining
```

The state machine is not strictly linear. New evidence can move an episode
from review back to discovery or reconciliation. A consent revocation can
invalidate pending acquisition or degrade an established snapshot.

Each bounded pass consumes:

- the episode purpose and current authorization;
- the latest evidence-estate manifest;
- unresolved frontier items and evidence obligations;
- prior trajectory and spend totals;
- reviews, corrections, and newly arrived sources.

It emits a proposed state transition, updated frontier, bounded work requests,
and a reason to continue, wait, stop, or escalate. Long waits contain no live
model process.

## Interfaces and boundaries

The episode owns orchestration state, not source bytes, credentials, or an
authoritative domain record. It references immutable or versioned source
objects and candidate model artifacts. Subject Hermes owns the episode and
decides whether its result is ready for admission.

The existing neutral subject-establishment flow covers facts, neutral design,
platform realization, review, apply, and verification. This episode is a
possible evidence-establishment companion beneath its fact-set step; it does
not replace system-of-record realization.

Maintenance may reuse the same mechanism for refresh and reconciliation, but
an implementation could choose a separate maintenance episode family if
establishment and steady-state operating controls diverge too much.

## Alternatives and tensions

- One long agent session is cognitively simple but operationally fragile,
  expensive, hard to revoke, and impossible to audit cleanly across waits.
- Independent stateless jobs are easy to operate but lose the question-and-gap
  continuity that makes recursive establishment useful.
- One episode covering establishment and maintenance preserves lineage; two
  episode families may produce clearer budgets, readiness semantics, and
  retention rules.

## Open questions

- Is `maintaining` a terminal handoff or a continuing episode state?
- Which state transitions require Subject Hermes, a human, or a domain expert?
- How are episode budgets renewed after an external wait?
- What invalidates a previous readiness decision when later evidence arrives?

## Relationships

The episode hosts the [recursive evidence frontier](hermes-recursive-subject-establishment-recursive-evidence-frontier.md),
uses the [Hermes control and execution boundary](hermes-recursive-subject-establishment-hermes-control-and-execution-boundary.md),
and terminates through [coverage, gap, and readiness](hermes-recursive-subject-establishment-coverage-gaps-and-readiness.md).

