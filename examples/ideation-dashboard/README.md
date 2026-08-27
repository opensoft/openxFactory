# Ideation-Dashboard Examples

Status: draft

Reference examples for the ideation-area dashboard contract schemas under
`contracts/schemas/` (`add-ideation-dashboard` change, task 2.4, plus the
sibling schemas from tasks 2.6/2.8). These are static reference material, not
runtime state — see `../README.md` for the placement policy this directory
follows. The strict validator is
`scripts/validate-ideation-dashboard-contracts.py`; running it with no argument
self-tests every file here (valid pass, each negative fails for its intended
reason, each transition pair matches its declared expectation) and then scans
the checkout for real instances and committed workbench manifests.

## Layout

```text
ideation-dashboard/
├── README.md                                          # this index
├── ideation-dashboard-snapshot.example.yaml           # complete snapshot (multi-cluster possible,
│                                                       #   cited rejection, pick-edge inheritance, option set)
├── snapshot-index.example.yaml                        # (repository, ref) locator: 4 repos incl. a
│                                                      #   sparse install repo + an aggregate view
├── ideation-workbench-cluster-seeded.example.yaml     # cluster-seeded set + recipe (pinned ⊆ checked)
├── ideation-workbench-adhoc-human-seen.example.yaml   # ad-hoc human-seen cluster submission
├── possibles-register.example.yaml                    # register section (source-of-truth twin of the snapshot possibles)
├── derived-possible-register.example.yaml             # AI-derived possibles (origin + derivation delta; add-possibles-derivation-lane)
├── project-register.example.yaml                      # repo → project → group hierarchy (multi-repo project)
├── gate-action-record-ratify.example.yaml             # ratify action + ratification-record artifact
├── gate-action-record-kickoff.example.yaml            # kickoff action + workflow-job artifact (needs ratified context)
├── gate-action-record-demote.example.yaml             # demote action + reason
├── gate-action-record-dispose-possible.example.yaml   # dispose-possible + outcome + register-update artifact
├── gate-action-record-edit-document.example.yaml      # BRANCH SESSION: document + ref + commit artifact
├── gate-action-record-open-pr.example.yaml            # BRANCH SESSION: ref + pull-request artifact (no commit)
├── gate-action-record-abandon-session.example.yaml    # BRANCH SESSION: ref + reason (no artifact kind required)
├── gate-action-record-cleanup-abandoned-branch.example.yaml # BRANCH SESSION: exact head + abandon/release evidence
├── demotion-execution-receipt.example.yaml            # DEMOTION: post-execution proof for an exact staged return
├── gate-intent-pending.example.yaml                   # INTENT PLANE: pending dispose request
├── gate-intent-applied.example.yaml                   # INTENT PLANE: applied request + record link
├── gate-intent-promote-to-staging.example.yaml        # WHEEL: accepted-possible staging commission
├── gate-intent-derive-possibles.example.yaml           # WHEEL: cluster-scoped derivation commission
├── gate-intent-research-brief.example.yaml             # WHEEL: pre-verdict research commission
├── gate-action-record-promote-to-staging.example.yaml # WHEEL: possible target + workflow-job
├── gate-action-record-derive-possibles.example.yaml    # WHEEL: cluster target + workflow-job
├── gate-action-record-research-brief.example.yaml      # WHEEL: possible target + workflow-job
├── gate-action-record-approve-model.example.yaml       # MODEL INTAKE: declaration target + grant accountability
├── workbench-model-catalog-local.example.yaml         # doxBench WIRE: local catalog entry
├── workbench-model-catalog-empty.example.yaml         # doxBench WIRE: the editor-only SUCCESS posture
├── workbench-model-catalog-hosted-zero-retention.example.yaml  # doxBench WIRE: hosted badge
├── workbench-model-catalog-routing-rule.example.yaml  # doxBench WIRE: an `auto` ROUTING RULE (contract-v1.38)
├── workbench-model-catalog-routing-rule-wider-than-a-non-resolved-member.example.yaml  # rule 5': lawful, and the point of the ruling
├── workbench-chat-turn-unsaved-edits.example.yaml     # doxBench WIRE v1: dirty buffer as turn input
├── workbench-chat-turn-outline-only.example.yaml      # doxBench WIRE v1: null active_document_path (G-1)
├── workbench-chat-turn-prose-only.example.yaml        # doxBench WIRE v1: success, conversation only
├── workbench-chat-turn-both-proposals.example.yaml    # doxBench WIRE v1: success, unique targets
├── workbench-chat-turn-v2-loaded-set.example.yaml     # doxBench WIRE v2: outline + N documents, DECLARED binding
├── workbench-chat-turn-v2-success.example.yaml        # doxBench WIRE v2: record naming the bound buffer + selected model
├── workbench-chat-turn-v2-reduced-context.example.yaml # doxBench WIRE v2: the DEGRADED posture, stated (contract-v1.40)
├── workbench-chat-turn-v2-full-context.example.yaml   # doxBench WIRE v2: the ordinary posture, stated explicitly
├── workbench-chat-turn-v2-provider-retry.example.yaml # doxBench WIRE v2: the turn that cost two paid calls, and says so
├── negative/                                          # one violation per file
│   ├── snapshot-dangling-document-edge.yaml           #   edge → missing document id
│   ├── snapshot-dangling-claiming-cluster.yaml        #   claiming_clusters → missing cluster id
│   ├── snapshot-dangling-option-set-member.yaml       #   option_set member → missing possible id
│   ├── snapshot-bad-date-format.yaml                  #   FormatChecker: date is not ISO
│   ├── snapshot-index-duplicate-repo-ref.yaml         #   same (repository, ref) pair twice
│   ├── snapshot-index-carries-projection-data.yaml    #   locator carrying projection data (D3)
│   ├── workbench-override-without-reason.yaml         #   manual-include member without reason
│   ├── workbench-excluded-without-reason.yaml         #   excluded entry without reason
│   ├── workbench-pinned-not-checked.yaml              #   pinned keyword not in checked (W1)
│   ├── workbench-candidate-in-members.yaml            #   new_candidates overlaps members (W2)
│   ├── register-uncited-rejection.yaml                #   rejected without citation (named case)
│   ├── register-picked-without-pick.yaml              #   picked without pick edge
│   ├── register-missing-provenance.yaml               #   entry without provenance
│   ├── register-duplicate-id.yaml                     #   id repeated within the register
│   ├── register-derived-missing-derivation.yaml       #   ai-derived with no derivation block at all (schema + validator)
│   ├── register-derived-missing-worker-run.yaml       #   ai-derived derivation without worker_run (schema layer)
│   ├── register-derived-unsourced.yaml                #   ai-derived with no cluster edge / evidence pin (validator layer)
│   ├── register-derived-bad-disposition.yaml          #   ai-derived machine disposition ≠ pending_review (schema + validator)
│   ├── project-empty-project.yaml                     #   project with zero repositories
│   ├── project-empty-group.yaml                       #   group with zero projects
│   ├── project-duplicate-id.yaml                      #   duplicate project id
│   ├── project-dangling-group-member.yaml             #   group references missing project
│   ├── project-multi-parent-repo.yaml                 #   repository in two projects (single-parent)
│   ├── gate-demote-without-reason.yaml                #   demote without reason
│   ├── gate-ratify-without-ratification-artifact.yaml #   ratify without ratification-record
│   ├── gate-kickoff-without-workflow-job.yaml         #   kickoff without workflow-job
│   ├── gate-kickoff-unratified-target.yaml            #   kickoff target not ratified (context-dependent)
│   ├── gate-dispose-rejected-uncited.yaml             #   rejected disposition without reason + citation
│   ├── gate-action-edit-document-no-commit-artifact.yaml  # edit-document without a commit artifact
│   ├── gate-action-edit-document-no-ref.yaml          #   edit-document naming no session branch
│   ├── gate-action-open-pr-no-pull-request-artifact.yaml  # open-pr without a pull-request artifact
│   ├── gate-action-abandon-session-unreasoned.yaml    #   abandon-session without a reason
│   ├── gate-action-approve-model-without-approval-block.yaml #   approve-model with no grant accountability
│   ├── gate-action-approve-model-shared-install-without-consent.yaml # shared install, no consent instrument
│   ├── gate-action-cleanup-explicit-release-without-reason.yaml # explicit cleanup release without its reason
│   ├── intent-applied-without-record.yaml             # applied intent without its record link
│   ├── intent-refused-without-reason.yaml             # refused intent without its reason
│   ├── intent-promote-to-staging-without-possible-id.yaml # wheel intent missing possible target
│   ├── intent-derive-possibles-without-cluster-id.yaml    # wheel intent missing cluster target
│   ├── intent-research-brief-without-possible-id.yaml     # wheel intent missing possible target
│   ├── gate-action-promote-to-staging-without-workflow-job.yaml # wheel record missing job
│   ├── gate-action-derive-possibles-without-workflow-job.yaml    # wheel record missing job
│   ├── gate-action-derive-possibles-without-cluster-id.yaml      # wheel record missing cluster
│   ├── gate-action-research-brief-without-workflow-job.yaml      # wheel record missing job
│   ├── workbench-model-catalog-exposed-credential.negative.yaml  # credential in a public field
│   ├── workbench-model-catalog-raw-endpoint.negative.yaml        # raw provider endpoint
│   ├── workbench-model-catalog-plain-entry-resolves-elsewhere.negative.yaml # plain entry, routing field
│   ├── workbench-model-catalog-routing-badge-gap.negative.yaml   # rule missing a routed model's badge
│   ├── workbench-model-catalog-routing-dangling-target.negative.yaml # routes to an id nothing offers
│   ├── workbench-model-catalog-routing-rule-chained.negative.yaml # rule routing to another rule
│   ├── workbench-model-catalog-routing-rule-unavailable-resolution.negative.yaml # available rule, unavailable resolution
│   ├── workbench-model-catalog-routing-rule-wider-than-its-resolution.negative.yaml # rule wider than the model that ANSWERS
│   ├── workbench-model-catalog-routing-badge-inverted-substring.negative.yaml # review A: badge states the INVERSE
│   ├── workbench-model-catalog-routing-badge-incidental-word.negative.yaml # review D: badge word matched by accident
│   ├── workbench-model-catalog-routing-badge-holds-the-separator.negative.yaml # routed badge holds " / "
│   ├── workbench-model-catalog-routing-resolved-outside-routes-to.negative.yaml # review B: resolved id not in routes_to
│   ├── workbench-model-catalog-routing-self-reference.negative.yaml # rule names itself in routes_to
│   ├── workbench-chat-turn-escaping-path.negative.yaml           # buffer path escaping the checkout
│   ├── workbench-chat-turn-hash-mismatch.negative.yaml           # declared content_hash ≠ recomputed
│   ├── workbench-chat-turn-identity-subject.negative.yaml        # identity-shaped working_subject
│   ├── workbench-chat-turn-over-budget.negative.yaml             # buffers over the model input limit
│   ├── workbench-chat-turn-unknown-model.negative.yaml           # model_id outside the catalog
│   ├── workbench-chat-turn-untyped-proposal.negative.yaml        # replacement content with no target
│   ├── workbench-chat-turn-v2-unbound-buffer.negative.yaml       # bound_buffer naming no supplied buffer
│   ├── workbench-chat-turn-v2-reserved-key-path.negative.yaml    # document path claiming a reserved key
│   ├── workbench-chat-turn-v2-context-reduced-without-reason.negative.yaml # a reduction nobody can read
│   ├── workbench-chat-turn-v2-context-reason-on-full.negative.yaml # `full` carrying a reduction reason
│   ├── workbench-chat-turn-v2-context-unknown-posture.negative.yaml # a third posture the vocabulary has no rule for
│   ├── workbench-chat-turn-v2-context-extra-field.negative.yaml  # a fourth fact on the closed posture object
│   ├── workbench-chat-turn-v2-provider-retry-carries-a-token.yaml # a fourth fact on the closed re-mint object
│   ├── workbench-chat-turn-v2-context-empty-reason-on-full.negative.yaml # `full` + a BLANK reason: the key is present
│   └── workbench-chat-turn-v2-context-null-reason-on-full.negative.yaml  # `full` + a NULL reason: still present
└── transitions/                                       # register (old, new) pairs; valid-* pass, invalid-* fail
    ├── valid-pick-and-reject.{before,after}.yaml      #   latent→picked, latent→rejected, plus a new entry
    ├── valid-derived-disposition.{before,after}.yaml  #   derived accept→latent (origin retained) + reject→rejected
    ├── invalid-resurrection.{before,after}.yaml       #   rejected→picked (terminal / no resurrection)
    ├── invalid-wrong-target.{before,after}.yaml       #   picked→rejected (must be superseded)
    ├── invalid-deletion.{before,after}.yaml           #   an entry was removed
    ├── invalid-reused-id.{before,after}.yaml          #   id re-used for a different possible
    ├── invalid-derived-undispose.{before,after}.yaml  #   disposed→undisposed (one-way disposition)
    └── invalid-derived-origin-launder.{before,after}.yaml # origin ai-derived→human-authored (fixed origin)
```

## Schema → example map

| Schema | Valid example(s) | Negative example(s) |
| --- | --- | --- |
| `ideation-dashboard-snapshot.schema.yaml` | `ideation-dashboard-snapshot.example` | `snapshot-dangling-document-edge`, `snapshot-dangling-claiming-cluster`, `snapshot-dangling-option-set-member`, `snapshot-bad-date-format` |
| `ideation-dashboard-snapshot-index.schema.yaml` | `snapshot-index.example` | `snapshot-index-duplicate-repo-ref`, `snapshot-index-carries-projection-data` |
| `ideation-workbench.schema.yaml` | `ideation-workbench-cluster-seeded`, `ideation-workbench-adhoc-human-seen` | `workbench-override-without-reason`, `workbench-excluded-without-reason`, `workbench-pinned-not-checked`, `workbench-candidate-in-members` |
| `ideation-possibles-register.schema.yaml` (`#/$defs/possibles_register`) | `possibles-register.example`, `derived-possible-register.example` + `transitions/valid-*` | `register-uncited-rejection`, `register-picked-without-pick`, `register-missing-provenance`, `register-duplicate-id`, `register-derived-missing-derivation`, `register-derived-missing-worker-run`, `register-derived-unsourced`, `register-derived-bad-disposition`, `transitions/invalid-*` |
| `project-register.schema.yaml` | `project-register.example` | `project-empty-project`, `project-empty-group`, `project-duplicate-id`, `project-dangling-group-member`, `project-multi-parent-repo` |
| `gate-intent.schema.yaml` | `gate-intent-pending`, `gate-intent-applied`, `gate-intent-promote-to-staging`, `gate-intent-derive-possibles`, `gate-intent-research-brief` | `intent-applied-without-record`, `intent-refused-without-reason`, `intent-promote-to-staging-without-possible-id`, `intent-derive-possibles-without-cluster-id`, `intent-research-brief-without-possible-id` |
| `xfactory-workbench-model-catalog.schema.yaml` | `workbench-model-catalog-local`, `workbench-model-catalog-empty`, `workbench-model-catalog-hosted-zero-retention`, `workbench-model-catalog-routing-rule`, `workbench-model-catalog-routing-rule-wider-than-a-non-resolved-member` | `workbench-model-catalog-exposed-credential`, `workbench-model-catalog-raw-endpoint`, `workbench-model-catalog-plain-entry-resolves-elsewhere`, `workbench-model-catalog-routing-badge-gap`, `workbench-model-catalog-routing-dangling-target`, `workbench-model-catalog-routing-rule-chained`, `workbench-model-catalog-routing-rule-unavailable-resolution`, `workbench-model-catalog-routing-rule-wider-than-its-resolution`, `workbench-model-catalog-routing-badge-inverted-substring`, `workbench-model-catalog-routing-badge-incidental-word`, `workbench-model-catalog-routing-badge-holds-the-separator`, `workbench-model-catalog-routing-resolved-outside-routes-to`, `workbench-model-catalog-routing-self-reference` |
| `xfactory-workbench-chat-turn.schema.yaml` (v1 family, DEPRECATED at `contract-v1.34`) | `workbench-chat-turn-unsaved-edits`, `workbench-chat-turn-outline-only`, `workbench-chat-turn-prose-only`, `workbench-chat-turn-both-proposals` | `workbench-chat-turn-escaping-path`, `workbench-chat-turn-hash-mismatch`, `workbench-chat-turn-identity-subject`, `workbench-chat-turn-over-budget`, `workbench-chat-turn-unknown-model`, `workbench-chat-turn-untyped-proposal` |
| `xfactory-workbench-chat-turn.schema.yaml` (widened `-v2` family, `contract-v1.34`; the record's CONTEXT POSTURE at `contract-v1.40`; the MID-TURN RE-MINT at `contract-v1.45`) | `workbench-chat-turn-v2-provider-retry`, `workbench-chat-turn-v2-loaded-set`, `workbench-chat-turn-v2-success` (which states NO posture, and is still valid — that is the v1.40 additive claim), `workbench-chat-turn-v2-reduced-context`, `workbench-chat-turn-v2-full-context` | `workbench-chat-turn-v2-unbound-buffer`, `workbench-chat-turn-v2-reserved-key-path`, `workbench-chat-turn-v2-context-reduced-without-reason`, `workbench-chat-turn-v2-context-reason-on-full`, `workbench-chat-turn-v2-context-unknown-posture`, `workbench-chat-turn-v2-context-extra-field`, `workbench-chat-turn-v2-context-empty-reason-on-full`, `workbench-chat-turn-v2-context-null-reason-on-full`, `workbench-chat-turn-v2-provider-retry-carries-a-token` |
| `gate-action-record.schema.yaml` | `gate-action-record-ratify`, `gate-action-record-kickoff`, `gate-action-record-demote`, `gate-action-record-dispose-possible`, `gate-action-record-edit-document`, `gate-action-record-open-pr`, `gate-action-record-abandon-session`, `gate-action-record-cleanup-abandoned-branch`, `gate-action-record-promote-to-staging`, `gate-action-record-derive-possibles`, `gate-action-record-research-brief`, `gate-action-record-approve-model` | `gate-demote-without-reason`, `gate-ratify-without-ratification-artifact`, `gate-kickoff-without-workflow-job`, `gate-kickoff-unratified-target`, `gate-dispose-rejected-uncited`, `gate-action-edit-document-no-commit-artifact`, `gate-action-edit-document-no-ref`, `gate-action-open-pr-no-pull-request-artifact`, `gate-action-abandon-session-unreasoned`, `gate-action-cleanup-explicit-release-without-reason`, `gate-action-promote-to-staging-without-workflow-job`, `gate-action-derive-possibles-without-workflow-job`, `gate-action-derive-possibles-without-cluster-id`, `gate-action-research-brief-without-workflow-job`, `gate-action-approve-model-without-approval-block`, `gate-action-approve-model-shared-install-without-consent` |
| `demotion-execution-receipt.schema.yaml` | `demotion-execution-receipt` | runtime and focused tests cover malformed or mismatched receipts |

## Named cases from task 2.4

- **Multi-cluster possible** — `pos-set-builder` in the snapshot and register
  examples is claimed by two clusters.
- **Cited rejection** — `pos-abandoned-autolayout` (rejected + reason + citation).
- **Uncited rejection failing** — `negative/register-uncited-rejection.yaml`.
- **Pick-edge inheritance** — `pos-cluster-canvas`'s `pick` carries both the
  `staging_id` cited at the organize gate and the `change_id` inherited at the
  proposal gate; `transitions/valid-pick-and-reject` shows the latent→picked move.
- **Ad-hoc human-seen cluster submission** —
  `ideation-workbench-adhoc-human-seen.example.yaml`.

## AI-derived possibles (add-possibles-derivation-lane)

The kernel's additive `origin` + `derivation` delta (a derive-possibles worker
PROPOSES candidate possibles that humans dispose on the gate console) is
exercised here without a `contract_schema_version` bump:

- **Valid** — `derived-possible-register.example.yaml`: an undisposed derived
  possible (`origin: ai-derived`, worker-run identity, machine `pending_review`,
  sourced by a cluster edge + an evidence pin), an accepted derived possible
  (retains `origin: ai-derived`, carries the `human_disposition` mirror), and a
  human-authored possible (no `origin`) coexisting unaffected.
- **`register-derived-missing-derivation.yaml`** — SCHEMA + VALIDATOR layers:
  `origin: ai-derived` with no `derivation` block at all — the top-level allOf
  conditional (`if origin: ai-derived then required: [derivation]`) and the
  delegated validator both reject it (distinct from the missing-worker-run case,
  which has a derivation block).
- **`register-derived-missing-worker-run.yaml`** — SCHEMA layer: a `derivation`
  block that omits its required `worker_run`.
- **`register-derived-unsourced.yaml`** — VALIDATOR layer: schema-valid by design
  (the kernel does not require a citation), rejected by the delegated register
  validator because a derived entry cites no cluster edge and no evidence pin.
- **`register-derived-bad-disposition.yaml`** — SCHEMA + VALIDATOR layers: a
  well-formed, sourced derived entry whose machine `derivation.disposition` reads
  `accepted` — the `const: pending_review` and the delegated validator both reject
  it (the human verdict belongs in `derivation.human_disposition`).
- **`transitions/valid-derived-disposition`** — accept keeps the entry `latent`
  retaining origin; reject moves it to `rejected` with reason + citation.
- **`transitions/invalid-derived-undispose`** — a disposed derived possible
  edited back to undisposed (one-way disposition lifecycle).
- **`transitions/invalid-derived-origin-launder`** — `origin` laundered from
  `ai-derived` to human-authored in place (a possible's origin is fixed).

The one-way disposition lifecycle and the derived-entry shape rules are enforced
by `scripts/validate-ideation-dashboard-contracts.py` (the C3 delegated register
validator); `scripts/validate-ideation-cross-reference.py` delegates them, not
duplicating the checks.

## Branch sessions (add-workbench-branch-sessions)

The gate-action record's session growth (design D13) is exercised here without a
`contract_schema_version` bump: `action` gained `edit-document`, `open-pr`, and
`abandon-session`; the artifact `kind` enum gained `commit` and `pull-request` as
first-class kinds; and `target` gained an OPTIONAL `ref` naming the session
branch. Each per-action conditional constrains ONLY its own new action, which is
why the growth invalidates no existing record.

- **Valid** — `gate-action-record-edit-document.example.yaml`: `document` + `ref`
  + a `commit` artifact whose `reference` is the action's own STAMP rather than a
  sha (a commit cannot contain its own sha, so the referenced commit is the one
  that introduced the record file on the branch).
- **Valid** — `gate-action-record-open-pr.example.yaml`: `ref` + a
  `pull-request` artifact, and deliberately NO `commit` artifact — the record is
  main-resident and the action adds no commit to the branch.
- **Valid** — `gate-action-record-abandon-session.example.yaml`: `ref` +
  `reason`, with the branch carried as an `other` artifact only to satisfy
  `artifacts.minItems`; no artifact KIND is required of this action.
- **`gate-action-edit-document-no-commit-artifact.yaml`** — SCHEMA layer: the
  one-commit-per-gate-action rule, missing its `commit` artifact.
- **`gate-action-edit-document-no-ref.yaml`** — SCHEMA layer: a session edit
  naming no session branch. `target.ref` is optional in general and REQUIRED
  here; this file is what proves the conditional bites.
- **`gate-action-open-pr-no-pull-request-artifact.yaml`** — SCHEMA layer: a save
  record that references a commit instead of the pull request it opened.
- **`gate-action-abandon-session-unreasoned.yaml`** — SCHEMA layer: the
  unreasoned-demotion rule applied to the session's other ending.

There is deliberately NO negative for "`create-document` without a `commit`
artifact": that action pre-dates branch sessions and is legitimately performed
outside one, where no commit is produced, so the commit-per-action rule is a
ROUTE obligation for it and never a schema conditional (D13). For the same
reason `target.ref` stays optional even though the route populates it for every
in-session action.

## Wheel action commissions (add-wheel-action-verbs)

The three generative wheel verbs extend both gate schemas additively without a
`contract_schema_version` bump. `promote-to-staging` and `research-brief`
target `possible_id`; `derive-possibles` targets the new optional
`cluster_id`. Every corresponding action record must contain a `workflow-job`
artifact because the dashboard commissions the work and never performs it.
`demote` is unchanged: it was already represented by `change_id` plus a
required `reason`.

- **Valid intents** — `gate-intent-promote-to-staging`,
  `gate-intent-derive-possibles`, and `gate-intent-research-brief` prove the
  target mapping while remaining ordinary pending requests.
- **Valid records** — the three matching `gate-action-record-*` examples each
  carry the governed `workflow-job` descriptor and no authored result.
- **Target negatives** — the three `intent-*-without-*` examples plus
  `gate-action-derive-possibles-without-cluster-id` prove that the new
  conditionals bite only for their own verbs.
- **Artifact negatives** — each new action has a
  `gate-action-*-without-workflow-job` example proving that a narrative or
  other artifact cannot stand in for the dispatched job.

Both schema objects remain open: unknown properties are still accepted for
forward-compatible additive growth, and every pre-wheel packaged positive
continues to validate through the same delegated validator.

## The register is an envelope-less kernel

`ideation-possibles-register.schema.yaml` is a pure `$defs` kernel embedded into
the cross-reference index (there is no third standalone register file). Its
examples wrap a register instance under a plain `possibles_register:` container
key — that wrapper is a container for these files only, not part of the schema.
Its `supporting_evidence` items `$ref` the snapshot schema's `evidence_pin`, so
the validator loads all five schemas into one registry for cross-file `$ref`
resolution.

## Cross-file consistency

`possibles-register.example.yaml` is the source-of-truth twin of the snapshot
example's `possibles` projection: identical ids and field values, plus the
register-only `provenance`. The `gate-action-record-*` examples use the snapshot
example as ratification context — `gate-action-record-kickoff.example.yaml`'s
target (`add-ideation-dashboard`) is ratified there, satisfying the D17 kickoff
precondition.

## The absent-repository case is legal

Task 2.6 also names "ungrouped repository": a repository absent from the project
register is valid and renders ungrouped as its own implicit project (a generator
behavior, task 3.8), so there is deliberately no negative for it.

## Validating locally

```bash
# Self-test all fixtures + scan the checkout for real instances / committed manifests:
python3 scripts/validate-ideation-dashboard-contracts.py

# …and the same sweep with warnings treated as errors. NOT the self-test command
# since contract-v1.34: the four packaged v1 chat-turn fixtures are instances of
# a DEPRECATED envelope family, so the validator warns on each one (by design —
# that warning is what the deprecating change class requires) and `--strict`
# therefore exits 1 on them, and will keep doing so until the removal target
# contract-v2.0 retires the fixtures with the family. Use it to FIND deprecated
# and otherwise-warned shapes, not to gate this directory:
python3 scripts/validate-ideation-dashboard-contracts.py --strict

# One file (kind auto-detected):
python3 scripts/validate-ideation-dashboard-contracts.py \
    examples/ideation-dashboard/ideation-dashboard-snapshot.example.yaml

# Register transition legality:
python3 scripts/validate-ideation-dashboard-contracts.py --transition \
    examples/ideation-dashboard/transitions/valid-pick-and-reject.before.yaml \
    examples/ideation-dashboard/transitions/valid-pick-and-reject.after.yaml
```
