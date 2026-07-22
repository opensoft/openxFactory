# Medical Omnigent Harness Adaptation — Brainstorm

Status: brainstorm
Kind: architecture
Summary: The Omnigent harness was built for software engineering; this doc
maps exactly where its software assumptions live, shows that the worker
fleet of every domain decomposes into the same six neutral archetypes
(frame → generate → verify → challenge → assemble-for-admission → hand off
to enforcement), generalizes codexFactory's six-boolean permission matrix
into a domain-neutral one, and gives the seam-by-seam software→medical
projection. Companion artifact: a machine-readable draft of the MedxFactory
Omnigent overlay staged at
`MedxFactory/ideation/staging/medical-omnigent-overlay/`.
Topics: omnigent, medical-harness, worker-archetypes, permission-matrix,
artifact-only-lane, review-lanes, source-trace, external-enforcement,
omnigent-core-domain-split, medxfactory
Repository context: openxFactory (spans installs/omnigent-install,
xFactories/codexFactory, xFactories/MedxFactory)
Captured: 2026-07-22

## What the harness is (research findings, 2026-07-22)

- The Omnigent runtime is a multi-executor tool (Claude Code `claude-sdk` +
  Codex behind an `executor.harness` field). Around it, omnigent-install
  provides worker containers, subscription auth profiles (no raw API keys to
  workers), a capability/pool/role dispatcher, the `HERMES_EVENT_JSON` event
  bridge, and Hermes approval gates. None of this core knows about software.
- The software assumptions concentrate in identifiable seams: the job-envelope
  schema in omnigent-install hard-enums SWE `job_type` values (`speckit_*`,
  `branch_review`, `merge_council`) and requires git `repository` fields;
  the coder profile hardcodes worktree/branch templates; Spec Kit is a
  required scaffold; the branch-review prompt set names SWE review lanes.
  (The canonical `neutral-job-envelope` spec already makes `job_type` a
  domain-owned string — only the install schema and its overlay lag.)
- Maturity poles: codexFactory has a real machine-readable overlay (9 agent
  classes, six-boolean permission matrix, credential families, golden path,
  validators). MedxFactory has the richest worker-layer *thinking*
  (specialist pods each containing evidence-retrieval, Bayesian, skeptic,
  test-utility, and safety sub-agents; dream layer; root-truth tiers; hard
  write-time invariants) but zero machine-readable worker definitions.
  omnigent-install has no domain tier at all (see
  `ideation/staging/omnigent-core-domain-split/`).

## Six neutral worker archetypes

codex agent classes and Medx pods are the same pipeline wearing different
clothes. Strip the domain nouns and every Omnigent worker fleet decomposes
into:

frame → generate → verify → challenge → assemble-for-admission → hand off
to external enforcement.

| Archetype | codexFactory | MedxFactory |
| --- | --- | --- |
| frame | engineering_decomposer, spec_planner | case framing, corpus query pack |
| generate | coding_agent, documentation_agent | dream/hypothesis generation, evidence retrieval, draft documentation |
| verify | test_agent, security_agent | test-utility, simulation, base-rate, data reverification |
| challenge | branch_review_agent | skeptic, must-not-miss safety |
| assemble-for-admission | pr_admission_agent, merge_readiness_agent | convergence packet / decision foundation report |
| external enforcement | GitHub branch protection + merge | clinician sign-off + chart/CPOE order signing |

The archetype row belongs in the *neutral* contract (candidate delta to the
future `omnigent-domain-overlay` contract from omnigent-core-domain-split);
the domain overlay names, prompts, and tools them. Side effect: it reconciles
codexFactory's two disconnected role vocabularies (the machine agent-class
enum vs the prose LA/LE/LC/LQ/LI/LS lead roles) by anchoring both to
archetypes.

## Neutral permission matrix

codexFactory's six booleans (`read_repo / write_repo / run_checks / open_pr /
merge_pr / access_secrets`) generalize to:

- `read_workspace` — bounded context via memory-gateway packets + the
  domain's workspace object
- `write_artifacts` — produce bounded, traceable artifacts only
- `run_validations` — deterministic checks (tests/CI in codex; source-trace,
  invariant, calculator, and simulation checks in Medx)
- `propose_admission` — assemble/submit the admission packet (PR admission;
  convergence packet to clinician review routing)
- `execute_final_action` — ALWAYS false for every worker in every domain
  (merge; order signing / chart write / truth-model mutation). This is the
  layer's constitutional boundary made machine-checkable.
- `access_secrets` — ALWAYS false (credential contracts: references only)

## The verification inversion

Software has cheap deterministic verification (compilers, tests, CI) and a
cheap terminal action (merge). Medicine has no compiler and a consequential,
human-owned terminal action. The medical harness therefore shifts weight
from "run checks" toward three things MedxFactory already invented:

1. **Provenance validation** — `source_trace` to Root Truth records with
   quality tiers; fully deterministic and machine-checkable (the medical
   analog of a failing required check).
2. **Structured adversarial review** — the branch-review-prompt-set
   mechanism (multi-model lanes with blocking criteria) re-lensed:
   evidence-support, base-rate/Bayesian, must-not-miss safety, test-utility,
   guideline-concordance lanes.
3. **A mandatory human gate** — clinician review routing owned by the
   tenant layer (Care Organization Hermes), terminal enforcement in the
   chart/CPOE system.

## Seam-by-seam software → medical projection

| Seam (software today) | Medical harness |
| --- | --- |
| `job_type` SWE enum | domain-owned vocabulary: `case_intake`, `dream_generation`, `differential_generation`, `test_utility_plan`, `simulation_run`, `convergence_packet` |
| `repository` + worktree/branch isolation | `workspace_ref` generalization; the immutable patient-truth snapshot IS the worktree (`truth_model_write_access: read_only`) |
| PR → merge council → branch protection | convergence packet → clinician review routing → chart/CPOE order signing as external enforcement |
| coder lane (write access) as default worker shape | the existing artifact-only lane (`max_repo_writes: 0`, structured output, `report_only`) is the default medical chassis; write-capable workers are the exception |
| branch-review prompt lanes | clinical review lane pack (same blocking-criteria mechanism, medical lane taxonomy) |
| tool packs: git, test runners, build images | per-profile tool/MCP allowlists: PubMed, ClinicalTrials.gov, terminology servers (SNOMED/RxNorm), interaction DBs, clinical calculators; clinical-tooling container layer on the same worker base |
| stop conditions: `secret_detected`, `unapproved_scope_detected` | `missing_source_trace`, `patient_fact_invention_detected`, `consent_scope_exceeded`, `phi_boundary_violation_detected`, `emergency_red_flag_raised` |
| credential families: `repo_read`, `branch_write`, `pr_write` | `case_context_read` (consent-bound), `draft_note_write`, `review_routing_submit`; `order_sign` and `truth_model_write` are never worker grants in any configuration |
| Spec Kit preseed | "CaseKit": the decision-foundation-loop as preseeded stage pipeline (frame → differential → test plan → simulate → converge → clinician review) |
| memory `source_authority_minimum: cited_source` | tiered minimums (`guideline`/`landmark`) per knowledge scope; consent-scoped patient packets; promotion-candidate-only writes |

## Delivery: overlay, not fork

Lands exactly on `omnigent-core-domain-split` (staging; core decisions
settled 2026-07-22): core omnigent stays domain-blind; MedxFactory authors
`omnigent/` (worker-profile deltas over the neutral archetypes, clinical
review-lane prompt pack, clinical tool/container bindings, source-trace and
invariant validators, CaseKit preseed) consumed by digest pin. That topic's
"second-domain proof — a MedxFactory params fixture that renders a medical
install without touching core" is the acceptance test for everything here.

## Exit path

1. The machine-readable Medx overlay draft (staged at
   `MedxFactory/ideation/staging/medical-omnigent-overlay/`) is the forcing
   artifact — it converts the prose expert layer into loadable config and
   surfaces the two neutral deltas it depends on.
2. Those neutral deltas (archetype row + generalized permission matrix in the
   `omnigent-domain-overlay` payload contract; relaxed install job-type enum)
   fold into the omnigent-core-domain-split OpenSpec change set rather than
   standing alone.
3. Promotion order: neutral payload contract → Medx OpenSpec change replacing
   `omnigent/domain-overlay.yaml` → omnigent-install second-domain fixture.
