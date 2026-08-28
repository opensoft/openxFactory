# Tasks: add-provenance-gated-autonomous-merge

Dependency-ordered. This change is DOCTRINE-ONLY in openxFactory (Group 1). The
realization groups are downstream and are NOT performed by this change — they are
tracked here so the follow-on has a fixed target. No push/merge is performed by
this change.

## Group 1 — openxFactory doctrine (this change)

- [x] 1.1 Author `proposal.md` (orthogonal axis, interim criterion (1)–(4),
  verifier, successor, interactions, Q3 honesty) with `code_surface`/
  `target_release` front-matter and an `ad_hoc` origin in `.openspec.yaml`.
- [x] 1.2 Author the `roles-authority-model` spec delta: MODIFY "Constitutional
  floor for autonomous clearance" to the orthogonal either-or axis (deltas
  declared relative to `add-substantive-review-lane`'s outcome); ADD the
  provenance-completeness eligibility, the provenance-tie verifier contract, the
  floor-primacy / per-repo-floor requirement, and the full-pipeline-green
  successor + sunset.
- [x] 1.3 Author `design.md` (decisions D1–D6, risks, migration, open questions)
  and `clarifications.md` (alignment + council outcomes, disposition, open
  questions).
- [x] 1.4 `OPENSPEC_TELEMETRY=0 openspec validate add-provenance-gated-autonomous-merge --strict` and `--all --strict` pass.
- [ ] 1.5 Convener ratification read (resolve Open Questions 1–4). Human-gated.
- [ ] 1.6 On ratification: set `Status: ratified` + `Ratified by:`; list in the
  openxFactory README "OpenSpec Records" block.

## Group 2 — Preconditions (downstream, human-gated; NOT this change)

- [ ] 2.1 Structured path-scope substrate (D6): a `code_surface` schema amendment
  or a new sibling field carrying a glob path allowlist on ratified changes.
  Human-gated `openspec/`-touching change; hard precondition for any
  provenance-eligible code class.
- [ ] 2.2 Confirm `add-repo-enrollment`'s enrollment front door is deployed with a
  live enrollment canary (dashboard/intake), so criterion (1) has a satisfying
  instance.

## Group 3 — codexFactory realization (separate dependent change; NOT this change)

- [ ] 3.1 Build the provenance-tie verifier per the contract: base-read
  corroboration; currency re-resolution; signed ratification record; glob
  scope-containment; SHA pinning to the verdict; fail-closed with a legible park
  record. Scope against codexFactory `origin/main`.
- [ ] 3.2 Ordered-delta MODIFIED on `merge-master-approval`'s definition-time
  `clearable`-eligibility predicate to admit a provenance-eligible, non-docs
  `clearable` class WITHOUT weakening the floor, stating explicitly which
  enforcement is primary for the provenance axis.
- [ ] 3.3 Class-floor guard in `scripts/merge_master/council_clearance.py` routing
  provenance-eligible classes through the same union-judged floor walk; negative
  fixtures proving a class reaching `scripts/**` / `openspec/changes/**` (and the
  repo's gate/workflow/credential/governance/record surfaces) is refused at
  definition time.
- [ ] 3.4 Publish a tree-validated never-clearable floor for the pilot repository
  covering its own decision core, gate, workflow, credential, governance, and
  council-record surfaces.
- [ ] 3.5 `gate_rules_council` record declaring the first provenance-eligible
  candidate class with rationale.
- [ ] 3.6 Enroll the pilot via the `add-repo-enrollment` owner-verified,
  machine-prepared PR route against base-branch
  `.github/merge-approval-envelope.yml` — never bypassed.
- [ ] 3.7 Archive the realization change only on merged + green realization
  evidence per `release-realization`.

## Group 4 — Pilot and successor (downstream; NOT this change)

- [ ] 4.1 Run a pilot of the interim provenance path and gather evidence.
- [ ] 4.2 Raise the NAMED full-pipeline-green successor change on that evidence,
  setting the supersession evidence bar; it retires the interim criterion.
