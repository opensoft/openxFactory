# Ideation-Dashboard Examples

Status: draft

Reference examples for the five ideation-area dashboard contract schemas under
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
├── ideation-workbench-cluster-seeded.example.yaml     # cluster-seeded set + recipe (pinned ⊆ checked)
├── ideation-workbench-adhoc-human-seen.example.yaml   # ad-hoc human-seen cluster submission
├── possibles-register.example.yaml                    # register section (source-of-truth twin of the snapshot possibles)
├── project-register.example.yaml                      # repo → project → group hierarchy (multi-repo project)
├── gate-action-record-ratify.example.yaml             # ratify action + ratification-record artifact
├── gate-action-record-kickoff.example.yaml            # kickoff action + workflow-job artifact (needs ratified context)
├── gate-action-record-demote.example.yaml             # demote action + reason
├── negative/                                          # one violation per file
│   ├── snapshot-dangling-document-edge.yaml           #   edge → missing document id
│   ├── snapshot-dangling-claiming-cluster.yaml        #   claiming_clusters → missing cluster id
│   ├── snapshot-dangling-option-set-member.yaml       #   option_set member → missing possible id
│   ├── snapshot-bad-date-format.yaml                  #   FormatChecker: date is not ISO
│   ├── workbench-override-without-reason.yaml         #   manual-include member without reason
│   ├── workbench-excluded-without-reason.yaml         #   excluded entry without reason
│   ├── workbench-pinned-not-checked.yaml              #   pinned keyword not in checked (W1)
│   ├── workbench-candidate-in-members.yaml            #   new_candidates overlaps members (W2)
│   ├── register-uncited-rejection.yaml                #   rejected without citation (named case)
│   ├── register-picked-without-pick.yaml              #   picked without pick edge
│   ├── register-missing-provenance.yaml               #   entry without provenance
│   ├── register-duplicate-id.yaml                     #   id repeated within the register
│   ├── project-empty-project.yaml                     #   project with zero repositories
│   ├── project-empty-group.yaml                       #   group with zero projects
│   ├── project-duplicate-id.yaml                      #   duplicate project id
│   ├── project-dangling-group-member.yaml             #   group references missing project
│   ├── project-multi-parent-repo.yaml                 #   repository in two projects (single-parent)
│   ├── gate-demote-without-reason.yaml                #   demote without reason
│   ├── gate-ratify-without-ratification-artifact.yaml #   ratify without ratification-record
│   ├── gate-kickoff-without-workflow-job.yaml         #   kickoff without workflow-job
│   └── gate-kickoff-unratified-target.yaml            #   kickoff target not ratified (context-dependent)
└── transitions/                                       # register (old, new) pairs; valid-* pass, invalid-* fail
    ├── valid-pick-and-reject.{before,after}.yaml      #   latent→picked, latent→rejected, plus a new entry
    ├── invalid-resurrection.{before,after}.yaml       #   rejected→picked (terminal / no resurrection)
    ├── invalid-wrong-target.{before,after}.yaml       #   picked→rejected (must be superseded)
    ├── invalid-deletion.{before,after}.yaml           #   an entry was removed
    └── invalid-reused-id.{before,after}.yaml          #   id re-used for a different possible
```

## Schema → example map

| Schema | Valid example(s) | Negative example(s) |
| --- | --- | --- |
| `ideation-dashboard-snapshot.schema.yaml` | `ideation-dashboard-snapshot.example` | `snapshot-dangling-document-edge`, `snapshot-dangling-claiming-cluster`, `snapshot-dangling-option-set-member`, `snapshot-bad-date-format` |
| `ideation-workbench.schema.yaml` | `ideation-workbench-cluster-seeded`, `ideation-workbench-adhoc-human-seen` | `workbench-override-without-reason`, `workbench-excluded-without-reason`, `workbench-pinned-not-checked`, `workbench-candidate-in-members` |
| `ideation-possibles-register.schema.yaml` (`#/$defs/possibles_register`) | `possibles-register.example` + `transitions/valid-*` | `register-uncited-rejection`, `register-picked-without-pick`, `register-missing-provenance`, `register-duplicate-id`, `transitions/invalid-*` |
| `project-register.schema.yaml` | `project-register.example` | `project-empty-project`, `project-empty-group`, `project-duplicate-id`, `project-dangling-group-member`, `project-multi-parent-repo` |
| `gate-action-record.schema.yaml` | `gate-action-record-ratify`, `gate-action-record-kickoff`, `gate-action-record-demote` | `gate-demote-without-reason`, `gate-ratify-without-ratification-artifact`, `gate-kickoff-without-workflow-job`, `gate-kickoff-unratified-target` |

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
python3 scripts/validate-ideation-dashboard-contracts.py --strict

# One file (kind auto-detected):
python3 scripts/validate-ideation-dashboard-contracts.py \
    examples/ideation-dashboard/ideation-dashboard-snapshot.example.yaml

# Register transition legality:
python3 scripts/validate-ideation-dashboard-contracts.py --transition \
    examples/ideation-dashboard/transitions/valid-pick-and-reject.before.yaml \
    examples/ideation-dashboard/transitions/valid-pick-and-reject.after.yaml
```
