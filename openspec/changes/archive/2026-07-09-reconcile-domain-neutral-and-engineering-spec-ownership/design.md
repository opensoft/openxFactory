## Context

`openxFactory` has been narrowed toward a domain-neutral workflow substrate.
Current README and docs point engineering-specific behavior to `codexFactory`,
including Spec Kit execution, engineering feature decomposition, branch review,
PR admission, and merge readiness.

The promoted OpenSpec specs have not fully caught up. In particular,
`canonical-policy-migration` still says `openxFactory` owns canonical Spec Kit
stage ownership and PR admission policy. That made sense during copy-first
migration from install repos, but it is now too broad: it treats one domain
implementation as factory-wide policy.

The repo also has a completed memory-gateway change still active. Its tasks are
complete and validation passes, so its requirements should be promoted into
canonical specs and the change archived.

## Goals / Non-Goals

**Goals:**

- Make OpenSpec hard requirements match the current ownership model.
- Keep `openxFactory` domain-neutral while preserving its authority over shared
  gates, traceability, state vocabulary, source authority, and audit.
- Make `codexFactory` carry software engineering implementation policy through
  docs and machine-readable workflow YAML.
- Keep historical OpenSpec evidence and archived content auditable.
- Make strict domain validation pass for `codexFactory`.

**Non-Goals:**

- Do not redesign Spec Kit or the engineering flow itself.
- Do not move runtime code, generated workspaces, credentials, databases, or
  service manifests.
- Do not change submodule pins.
- Do not delete archived OpenSpec evidence.
- Do not require non-software DomainxFactories to adopt Spec Kit.

## Decisions

### Decision: Separate neutral policy from domain execution policy

`openxFactory` remains the canonical home for neutral workflow requirements:
approved intent, decomposition gate, execution gate, validation, review,
admission, external enforcement, traceability, role escalation, and audit.

DomainxFactories own their domain execution mechanics. For software,
`codexFactory` owns Spec Kit stage flow, engineering task artifacts,
deterministic code checks, branch review, PR admission packet implementation,
and merge readiness packet implementation.

Alternative considered: keep software policy canonical in `openxFactory` and
link other domains around it. That keeps one place for engineering, but it makes
`openxFactory` read as the software factory and makes medical, operations,
ledger, and marketing domains inherit irrelevant execution policy.

### Decision: Preserve existing docs as pointers when useful

Docs such as `spec-kit-stage-ownership.md` and `pr-admission.md` should remain
in `openxFactory` only as neutral concepts and pointers. The detailed mechanics
belong in the relevant DomainxFactory.

Alternative considered: delete the pointer docs. That would reduce files but
break existing links and make the migration harder to audit.

### Decision: Use YAML workflow gates for codexFactory conformance

The Markdown workflow files remain the readable operating manual. Matching YAML
files provide machine-readable gates for validators, dashboards, and future
workflow runners.

Alternative considered: make the validator parse Markdown. Markdown is better
for humans, but it is brittle as an execution contract.

### Decision: Archive memory-gateway after manual spec promotion

The memory-gateway change is complete and already validates. This implementation
will copy its delta requirements into a canonical `memory-gateway` spec, update
indexes, and move the change to the dated archive.

Alternative considered: leave the completed change active. That keeps the
current files stable but leaves consumers reading hard requirements from an
active change path.

## Risks / Trade-offs

- Spec drift can recur -> validators and docs should prefer canonical specs plus
  DomainxFactory-specific workflow YAML over prose-only policy.
- Pointer docs can become stale -> keep them short and make the owning repo path
  explicit.
- Manual archive/promotion can miss a requirement -> run `openspec validate
  --all --strict` after promotion and keep the archived change intact for audit.
- Strict domain validation can over-constrain early domains -> use explicit
  placeholders for scaffold-only capabilities rather than omitting required
  blocks.

## Migration Plan

1. Update the affected OpenSpec requirements through this change.
2. Narrow `openxFactory` role, traceability, admission, and stage docs.
3. Add `codexFactory` workflow YAML gates, tenant example, and memory gateway
   scaffold.
4. Promote and archive the completed memory-gateway change.
5. Run OpenSpec and domain validators.

Rollback is documentation-only: revert this change, restore the archived
memory-gateway directory to active if needed, and rerun validation.

## Open Questions

- None for this cleanup. Future work may decide whether every DomainxFactory
  needs a full workflow YAML catalog or whether placeholders are sufficient
  until that domain is implementation-ready.
