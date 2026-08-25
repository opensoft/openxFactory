## Context

`cleanup-abandoned-branch` currently reuses `ProposalState`, whose purpose is to decide whether a tile has a *live* proposal. That state recognizes only an active change joined through a current possibles-register pick edge. Cleanup therefore deadlocks after archival, after an executed demotion removes the active change and withdraws its pick, for staged origins recorded only in `.openspec.yaml`, and for cluster/possible/orphaned tiles that can never carry an active staged-topic proposal.

The repository already holds most of the evidence needed to decide safely: change `.openspec.yaml` files retain staged origins after archival; demotion transition manifests name an exact destination; returned draft workspaces and round-trip provenance show legacy execution; and `abandon-session` records prove that a session ended intentionally. What is missing is a cleanup-specific retention model and, for future demotions and deliberate discard/supersession cases, a durable record of the act that releases the branch's final evidence custody.

## Goals / Non-Goals

**Goals:**

- Let a human clean an abandoned local branch once its evidence is preserved by an active proposal, archived change, or executed demotion.
- Give cluster, possible, missing, renamed, and otherwise orphaned tiles a reasoned human release path when no exact proposal lineage can preserve the exploration.
- Keep exact branch ownership, non-liveness, no-attached-worktree, and durable abandonment proof as mandatory preconditions.
- Make the deletion auditable after the branch is gone by recording the branch tip, scope, abandonment proof, and retention-release evidence.
- Reuse one staged-origin resolution rule across active and archived change discovery.

**Non-Goals:**

- Automatic cleanup, remote-branch deletion, pull-request closure, or cleanup during `propose`, archive, or demote.
- Treating a missing worktree, missing tile, absent change folder, stale report, or demotion plan as proof that content is safe to discard.
- Changing OpenSpec archive/demotion semantics or allowing a live/unabandoned session branch to be deleted.
- Semantically comparing documents to guess that one topic supersedes another.

## Decisions

### 1. Cleanup gets a retention-disposition model separate from live proposal state

Introduce a cleanup-specific value such as `RetentionReleaseEvidence(kind, scope_kind, scope_id, change_id, references)`. `ProposalState` continues answering whether a proposal is live for open/resume/propose mutual exclusion. Cleanup MUST NOT broaden that live-state answer to archived or demoted changes, because doing so would incorrectly make a completed proposal block new staging work.

The existing staged-origin reader becomes a shared, non-private resolution primitive used by snapshot generation, live-proposal detection, and cleanup evidence discovery. Declared `.openspec.yaml` origin wins over a surviving pick edge, matching the existing demotion precedence.

Alternative rejected: broaden `ProposalState.proposal_id` to include archived changes. It fixes deletion but breaks D20 by treating historical proposals as live.

### 2. Machine-resolved retention release is a closed evidence set

Cleanup may resolve one of these preservation proofs for the exact staged-topic id:

1. `active-proposal`: an active change whose staged origin or current pick resolves to the tile;
2. `archived-change`: an archived change whose own `.openspec.yaml` records `origin.kind: staged` and whose origin path resolves to the tile; or
3. `executed-demotion`: a demotion whose destination resolves to the tile and whose execution is durably proved.

Multiple matching changes are not ambiguous for retention: each independently proves that the exploration crossed into governed custody. The response records the deterministically sorted evidence chosen. A change with an ad-hoc origin, a mismatched staged origin, or only a dispatched proposal commission proves nothing for this tile.

Alternative rejected: infer safety from an absent active change folder. Both an archive and an interrupted authoring attempt have that shape.

### 3. A demotion plan is not an executed demotion

New demotion executions write a durable main-resident execution receipt after `execute_demotion_plan` successfully returns. The receipt names the change id, exact staged destination, execution time, and the returned artifacts; a failed execution writes no receipt. Cleanup accepts that receipt together with the existing transition manifest.

For pre-change demotions, a compatibility resolver may accept the transition manifest only when an exact returned-topic artifact corroborates execution: the generated `openspec/INDEX.md`, the demotion README entry, or populated round-trip provenance must name the same change and destination. A plan/manifest by itself remains insufficient.

Alternative rejected: accept every transition manifest. The dashboard writes that manifest while merely planning a demotion and explicitly performs no corpus transition at that stage.

### 4. Explicit human retention release handles true orphans

When no machine-resolved preservation proof exists, `cleanup-abandoned-branch` gains an explicit-release form requiring a nonblank reason. This is the lane for cluster/possible sessions, deleted or renamed tiles, duplicate/superseded drafts, and other cases whose content was deliberately discarded or preserved outside mechanically linkable proposal lineage.

The action writes a main-resident `cleanup-abandoned-branch` gate-action record before deletion. Its target names the ref and the appropriate existing scope field (`topic_id`, `cluster_id`, or `possible_id`); its artifacts/evidence name the exact pre-delete head, the prior `abandon-session` proof, and any operator-supplied superseding reference. If deletion fails, the new cleanup record is unwound so it cannot attest to a deletion that did not occur.

This is deliberately stronger than treating the original abandon reason as sufficient. Abandon ends live work but currently promises to retain the branch as evidence; the later retention release is the separate human decision that the evidence may now be destroyed.

### 5. Current tile absence does not erase identity, and does not prove disposition

The human supplies scope kind/id and ref. Existing branch-family and cross-tile exclusion checks continue to prove ownership. Cleanup evidence must independently resolve to that exact identity. The tile need not still appear in the current snapshot or staging directory, because archival and organization legitimately remove tiles; its absence alone contributes no positive evidence.

### 6. Every successful cleanup reports durable proof

Both the machine-evidence and explicit-release lanes write the additive cleanup action record and return its path, the pre-delete head, the verified abandon proof, and the selected retention-release evidence. The gate-action schema grows additively; no existing record is invalidated. The CLI and HTTP route remain human-only and local cleanup continues to delete no remote ref.

### 7. Machine evidence is correlated to the abandonment and exact branch head

An `abandon-session` record captures the abandoned branch head, and machine-resolved retention evidence carries a durable recording time. Cleanup accepts machine evidence only when it is at least as recent as the abandonment and the branch still points at the recorded abandoned head. Older evidence can describe an earlier lifecycle for the same tile and therefore cannot release newer abandoned work. Legacy abandonment records without an exact head, and uncommitted or otherwise undated lifecycle evidence, remain eligible only through a fresh explicit human retention release.

Alternative rejected: treat tile identity alone as sufficient correlation. Tile ids are intentionally reused across staging, proposal, archive, and later sessions, so identity does not prove that historical evidence preserved the branch being deleted.

### 8. Executed demotion receipts prove complete, exact execution

Before mutating the corpus, demotion execution verifies that every planned source artifact exists. An `executed` receipt is emitted only when every planned move occurred, every exact destination artifact exists, the source change folder was removed, and all recorded repository paths remain contained below the repository root. Receipt validation compares the receipt to its transition manifest rather than trusting matching change and destination ids alone.

Alternative rejected: accept zero or partial returned files as an executed demotion. Such a receipt can be syntactically valid while preserving none of the proposal material cleanup is meant to protect.

### 9. Cleanup is a collision-safe prepared/completed transaction

Cleanup records are keyed by the exact ref as well as the tile, created exclusively, and move from `prepared` to `completed` only after deletion. The transaction runs under the repository session-action lock, verifies that the human gate and Git service address the same checkout, and uses atomic file replacement for completion. A failed completion write restores the branch at the expected head when possible; a surviving `prepared` record never claims that deletion succeeded.

Alternative rejected: a second-resolution tile-only filename with overwrite semantics. Concurrent or repeated cleanups can otherwise overwrite another attempt and one caller can unlink the other caller's successful record.

### 10. Branch deletion uses an expected-value ref transaction

Cleanup deletes `refs/heads/<branch>` with Git's expected-old-value semantics after checking worktree and ownership constraints. If another process advances the ref between validation and deletion, the delete fails instead of destroying the newer ref. Contract schemas, examples, manifest digests, changelog, and release inventory advance together in the next available contract bundle.

## Risks / Trade-offs

- **Legacy demotions may lack enough corroborating output** → keep them blocked on the machine lane and require an explicit human retention-release reason rather than guessing execution.
- **Origin metadata can be malformed or duplicated** → fail closed on malformed entries, require exact normalized staged-topic identity, and select evidence deterministically.
- **Historical evidence can share a tile id with newer work** → require post-abandon evidence and an unchanged abandoned branch head for machine release; otherwise require a fresh explicit release.
- **An explicit release can discard genuinely unique work** → require prior abandonment, console presence, a fresh nonblank reason, the exact head SHA, and a durable main-resident record before deletion.
- **Writing a record before deleting can overstate a failed cleanup** → distinguish prepared from completed state, use exclusive ref-keyed records, and restore the expected ref if finalization fails.
- **Scanning all archived changes and demotion records adds work** → confine the scan to an explicitly invoked destructive cleanup and keep it deterministic; no nightly or render path changes.

## Migration Plan

1. Add cleanup evidence types/readers and tests without changing the deletion path.
2. Add demotion execution receipts and compatibility detection for existing returned drafts.
3. Add the cleanup gate-action schema/action writer and explicit-release input.
4. Switch the cleanup precondition to the new resolver and update CLI/HTTP/runbook surfaces.
5. Exercise active, archived, demoted, orphaned, mismatch, plan-only, live-session, and deletion-failure cases in scratch repositories.

Rollback is code-only: restore the active-proposal-only resolver. Cleanup records and demotion execution receipts are additive governed evidence and remain valid even if no longer consumed.

## Open Questions

None required for proposal readiness. The implementation should use the existing gate-record vocabulary fields where possible and add only the minimum evidence fields needed to make the cleanup record independently auditable.
