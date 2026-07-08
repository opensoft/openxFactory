# Design: Document Lifecycle Vocabulary

## Decision 1: One spine, two projections

The lifecycle is a single ordered spine for governance *content*:

```text
captured     free-form thinking exists (ideation/brainstorm/)
organized    pieces identified, deduped, targeted (ideation/staging/,
             candidate registers)
proposed     an OpenSpec change exists
ratified     the change is approved
implemented  the artifact (doc, schema, validator, template) is built
promoted     canonical — the contract/spec layer owns it
adopted      consumers re-pinned; local duplicates retired
superseded   replaced by a later delta, provenance retained
retired      withdrawn without replacement
```

Exits at any pre-promoted state: `rejected` (will not proceed) and `deferred`
(parked with a reason). Devolution reuses the same spine in reverse.

Two projections consume the spine:

1. **Document `Status:` headers** — the per-file view (Decision 2).
2. **Register statuses** — the per-concept view. The domain-neutralization
   candidate register's `seed -> staged -> openspec -> implemented -> adopted`
   maps to `captured/organized -> organized -> proposed/ratified ->
   implemented -> adopted`; the register keeps its compact aliases but each
   alias is defined in terms of the spine.

## Decision 2: Status is state, not genre

The ~25 wild `Status:` values conflate document *state* ("draft", "planned")
with document *kind* ("concept architecture", "generated runbook",
"simulation report"). The taxonomy separates them:

- `Status:` MUST be one of:
  `brainstorm | staged | draft | ratified | standard | superseded | retired |
  record`
- `Kind:` (optional, free-but-recommended vocabulary):
  `architecture | plan | process | runbook | report | register | template |
  reference`

Status semantics:

| Status | Lifecycle state | Meaning |
| --- | --- | --- |
| `brainstorm` | captured | Non-normative; contradiction legal; lives in `ideation/brainstorm/` |
| `staged` | organized | Structured toward a proposal; not yet policy |
| `draft` | proposed (or awaiting proposal) | Normative intent, not yet ratified |
| `ratified` | ratified/implemented | Backed by an approved OpenSpec change |
| `standard` | promoted | Backed by a promoted spec or canonical contract; only status allowed to claim shared-standard authority |
| `superseded` | superseded | Kept for provenance; header MUST name the successor |
| `retired` | retired | Withdrawn; header SHOULD name the reason or decision record |
| `record` | (out of band) | Immutable evidence artifact (generated reports, simulations, audits); never subject to prose-to-spec conversion |

## Decision 3: Migration mapping for existing headers

Applied by a follow-up sweep (task 4); docs are grandfathered until swept.

| Existing value (count) | New header |
| --- | --- |
| `concept architecture` (20) | `Status: draft` + `Kind: architecture` (or `brainstorm` if genuinely exploratory — sweep judges per doc) |
| `shared xFactory standard` (14) | `Status: draft` until a promoted spec backs it, then `standard`. No silent grandfathering of authority claims |
| `implementation plan` / `implementation contract` / `implementation architecture` | `Status: draft` + `Kind: plan` |
| `generated simulation report` / `generated runbook` / simulated reviews | `Status: record` + `Kind: report` or `Kind: runbook` |
| `draft — to be ratified through an OpenSpec change` | `Status: draft` (this change is that ratification path) |
| `seed backlog` | `Status: staged` + `Kind: register` |
| `exploration note` | `Status: brainstorm` |
| `planned` / `v1 operating plan` / `v1 scaffold decision` | `Status: draft` + `Kind: plan` |
| `organized — ...` (ideation) | `Status: staged`, with the organized-into pointer kept in the body |
| prose sentences ("the initial repo-boundary pilot is complete...") | move the sentence into the body; pick the true status |

The demotion of the 14 "shared xFactory standard" docs to `draft` is
deliberate and is the single most valuable honesty gain in this change: after
the sweep, every authority claim in a header is machine-checkable against the
spec layer.

## Decision 4: Ratify process docs by reference, not duplication

`docs/domain-to-neutral-promotion-process.md` and `ideation/README.md` remain
the how-to texts. The spec requirements state the invariants (gated
transitions, non-normativity of brainstorm, explicit-delta rule, adoption
completion); the process docs carry the mechanics. This avoids restating
process prose inside the spec — the exact failure mode this capability
exists to prevent.

## Alternatives considered

- **Per-repo vocabularies** — rejected: the health checker must run
  family-wide, and cross-repo promotion moves documents between repos
  mid-lifecycle.
- **Encoding kind into status** (e.g. `draft-architecture`) — rejected:
  multiplies the controlled list, and state transitions would look like kind
  changes.
- **YAML frontmatter instead of `Status:` lines** — deferred: the `Status:`
  header convention already exists in 77 docs; the taxonomy rides the
  existing convention. Frontmatter remains open as a doc-health pipeline
  question.
