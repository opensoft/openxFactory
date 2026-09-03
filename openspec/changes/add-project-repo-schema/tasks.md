# Tasks: add-project-repo-schema

Status: draft

**NOTHING IS TICKED THAT DID NOT LAND IN THIS PULL REQUEST.** Slices 1–5 are
complete and their evidence — command lines and outcomes — is recorded beside
each task. Slices 6–9 are open: three of them are successor changes in other
repositories, and one of them is the convener's act.

**Ratification is the convener's.** No task below may be read as having decided
that.

---

## Slice 1 — the packet

- [x] **1.1** Author `proposal.md` with `code_surface:` and `target_release:`
      front-matter per `release-realization`. `target_release: implemented`, with
      the measurement that establishes it recorded in the field itself: neither
      artifact is a registered row in `contracts/manifest.yaml` (measured: zero
      occurrences of `project-register`) or in
      `contracts/releases/contract-v3.0.digests.yaml` (zero), so no bundle number
      is spent, and `docs/contract-versioning-policy.md` forbids reserving one
      before merge order is known.
- [x] **1.2** Author `design.md` — thirteen decisions, each with its alternatives
      REJECTED and named, drawn from the fragment's Q1–Q12; the five convener
      rulings recorded as rulings with dates rather than re-argued; the two
      defects the pilot found and how the standard now handles them; and two open
      items (OI-1 topic administration, OI-2 whether the `schema` value set is
      ever closed) recorded rather than discovered later.
- [x] **1.3** Author the ADDED delta
      `specs/project-repo-schema/spec.md` — eleven requirements, each with SHALL
      on the first body line and each carrying at least two scenarios (31 in
      total).
- [x] **1.4** Author the MODIFIED delta `specs/ideation-dashboard/spec.md` over
      the promoted "Project grouping hierarchy" requirement, carrying canon's
      body VERBATIM and all five original scenarios, with the additions marked in
      place and six new scenarios. Checked first that no ACTIVE change writes
      that requirement, so no `Modified over` marker is owed and no ordering
      obligation is raised: `grep -rn "Requirement: Project grouping hierarchy"
      openspec/` resolves to canon plus two ARCHIVED changes only.
- [x] **1.5** Declare the origin. `scripts/proposal-support.py . transition`
      wrote the `staged` origin (`openxFactory:staging:project-repo-schema`);
      the `reason`, `approved_by` and `approved_on` pair recording Brett Heap's
      2026-09-02 instruction was appended beside it, on the
      `split-openxwallet-repo` precedent for a staged origin that also records
      its approval. `python3 scripts/proposal-support.py . verify
      add-project-repo-schema` → `proposal support verification ok`.

## Slice 2 — promotion mechanics (FULL promotion: no file remains staged)

- [x] **2.1** Move the primary fragment into `supporting-docs/` with history
      preserved: `python3 scripts/proposal-support.py . transition
      add-project-repo-schema ideation/staging/project-repo-schema --date
      2026-09-02 --apply`. The tool rewrote the header to `Status: draft` +
      `Proposed by: add-project-repo-schema` (the lifecycle's promoted-fragment
      form, as `add-trust-anchor` and `add-identity-brokering` carry), rewrote
      the relative link to the sibling topic, wrote `manifest.yaml` and the
      `source-snapshots/` copy.
- [x] **2.2** Remove the `project-repo-schema` row AND its `## project-repo-schema`
      detail section from `ideation/staging/INDEX.md` — full promotion, so
      nothing remains there (measured after: zero occurrences of the topic id in
      that file).
- [x] **2.3** Add the pointer to `ideation/README.md`'s "Active proposals
      promoted from staging" list, which is where the lifecycle puts it on FULL
      promotion.
- [x] **2.4** Add the change to the openxFactory README "OpenSpec Records"
      block's active list.
- [ ] **2.5** DELIBERATELY NOT DONE: the promoted fragment's own body is NOT
      edited to add a pilot note. It is PROVENANCE — a faithful record of what
      was staged at `c0270d2` — and `supporting-docs/manifest.yaml` records its
      digest, so an edit would either break `proposal-support.py verify` or
      require re-cutting the manifest over a provenance record. The temporary-pilot
      framing the convener ruled on 2026-09-02 is carried in the documents that
      speak in this change's voice instead: `proposal.md` § Realization evidence,
      `design.md` § D12, `docs/project-repo-schema.md` § The pilot on record, and
      this file's slice 5. Left unticked because it is a recorded NON-act, not a
      completed one.

## Slice 3 — the doctrine document

- [x] **3.1** Write `docs/project-repo-schema.md`, `Status: draft`,
      `Kind: standard`, `Proposed by: add-project-repo-schema`. It carries the
      doctrine and NOT the mechanics: the confers-nothing sentence and the four
      places it is restated, the three legs and the per-project-root ruling, the
      naming families and the claim-needs-a-referent ruling, the double pin and
      the measured lockstep defect, the manifest-is-the-source rule, the
      bootstrap contract and its verbatim degrade line, the overlay rule, the
      four-way ownership split and the narrowing it states, the new-organisation
      flow, and the pre-ratification election rule with the pilot on record.
- [x] **3.2** Link it from the openxFactory README's "Core domain-neutral docs"
      index.
- [ ] **3.3** On ratification, move the header to `Status: ratified` +
      `Ratified by: add-project-repo-schema`, per the document lifecycle. **The
      convener's act, and not this packet's.**

## Slice 4 — the openRepoShape pin and its running code

- [x] **4.1** Author `contracts/openreposhape-pin.yaml` in the
      `neutral-product-pin` shape: `kind: pinned_contract_manifest` reused
      unchanged, `revision_kind: commit`, commit
      `deacbdcce4f52af427bcb4edd075fcc992e3dabe` (40 hex), SIXTEEN per-file
      `sha256` rows and EIGHTEEN `pinned_by_commit_only:` members. **Every digest
      was computed from the real bytes at that commit**, from a clone checked out
      at `deacbdc`, never transcribed. The two lists cover all 34 files present
      at the commit, so no artifact appears in neither — which
      `neutral-product-pin`'s own scenario calls "an undeclared consumption, not
      a permitted omission".
- [x] **4.2** Author `scripts/validate-openreposhape-pin.py` — standard library
      only, fail-closed, six refusal codes and ONE fixed remediation trailer,
      five ordered checks (shape, revision, digests, presence, surface
      completeness). It has no gitlink comparison because openxFactory CITES the
      standard rather than mounting it; it resolves bytes from `--checkout` or
      `--from-gh` and REFUSES `pin-unresolvable` given neither, an unanswerable
      question never being an implicit pass.
- [x] **4.3** Run it against the REAL openRepoShape bytes, both ways.
      `--checkout` (a clone at `deacbdc`) and `--from-gh` (the host API at the
      pinned commit) each printed:
      `OK openreposhape-pin verified: opensoft/openRepoShape@deacbdcce4f52af427bcb4edd075fcc992e3dabe … 16 digest(s) recomputed, 18 member(s) present, 34 file(s) declared with none undeclared`,
      exit 0. With no source: `REFUSE pin-unresolvable`, exit 2.
- [x] **4.4** Wire it into CI as `.github/workflows/openreposhape-pin-gate.yml`,
      on the `openxwallet-consumer-gate.yml` pattern — checkout openRepoShape at
      the commit READ OUT OF THE PIN (never hard-coded; a workflow with its own
      copy of the sha would be the very lockstep defect this capability writes
      down), then one verifier invocation. No App token and no submodule init,
      each a fact about the product rather than a shortcut, and both stated in
      the file.
- [x] **4.5** Tests: `tests/openreposhape_pin/test_pin_verifier.py`, 21 tests,
      one per check and one per refusal code, plus the ordering assertion that a
      stale source is reported as a revision mismatch rather than as sixteen
      digest failures. `python3 -m pytest tests/openreposhape_pin/ -q` →
      `21 passed`.
- [ ] **4.6** Make the `openreposhape-pin` check REQUIRED on the default branch.
      **An operator act on an organisation ruleset, not a change's act** — and a
      check is not selectable until a workflow has reported under it once, which
      is why the workflow lands first.

## Slice 5 — the register election

- [x] **5.1** Extend `contracts/schemas/project-register.schema.yaml`: optional
      per-project `schema`, optional `reference`, optional `repository_roles`
      list of `{repository, role}` with `role` closed to `spec|code|assembly`.
      `repositories` items stay STRINGS — the one thing that had to not change,
      because `scripts/ideation_dashboard/register.py` and every renderer
      downstream read them as strings.
- [x] **5.2** Restate the confers-nothing posture for the new fields in the
      schema's own `description`, so it stands in the register, the requirement,
      the doctrine document and the assembly manifest — four places, because a
      posture stated once is a posture the second reader does not meet.
- [x] **5.3** Add the four cross-field rules the shape cannot express to
      `scripts/validate-ideation-dashboard-contracts.py`'s
      `check_project_register_rules`, via a new
      `check_project_schema_election`: a role naming a repository the project
      does not list (`project-role-unknown-repository`), a repository given a
      role twice (`project-duplicate-repository-role`), more than one
      `role: assembly` (`project-multiple-assembly-roles`), and a `reference`
      with no `schema` (`project-reference-without-schema`).
- [x] **5.4** Tests: `tests/ideation_dashboard/test_project_schema_election.py`,
      13 tests over both halves — the shape (the three fields exist and are
      optional, `role` is closed, `repositories` items are still strings, the
      posture is restated) and the relations (one per rule, plus the assertion
      that a project declaring NOTHING is accepted, which is the ratified
      doctrine expressed as a test). `python3 -m pytest
      tests/ideation_dashboard/ tests/openreposhape_pin/ -q` → `95 passed`.
- [x] **5.5** Confirm the existing register instances and packaged examples are
      untouched by the addition:
      `python3 scripts/validate-ideation-dashboard-contracts.py` →
      `0 error(s), 0 warning(s)`, 42 valid and 80 negative examples confirmed.

## Slice 6 — realization evidence (the pilot, which is TEMPORARY)

- [x] **6.1** Record the pilot run as this change's realization evidence for the
      pre-ratification election rule. **`MedxSoft/MedxScribe` IS A TEMPORARY
      PILOT AND NOT A REAL PROJECT** — Brett Heap, 2026-09-02: *"MedxScribe is
      only a temp pilot project right? it is not a real project. make sure it
      noted as pilot to test the openRepoShape"*. It was scaffolded on 2026-09-02
      solely to run `opensoft/openRepoShape` end to end, is not a MedxSoft
      product, is not "the first project", and MAY BE DELETED once this standard
      is ratified; the three repositories carry `PILOT (temporary): …`
      descriptions and the topics `pilot` and `openreposhape-pilot`, and the
      assembly root's README carries a banner. **The evidence is the RUN, and
      the run is recorded here and in `proposal.md` § Realization evidence:**
      `./setup.sh --project MedxScribe --visibility private --yes` against
      upstream `deacbdc` created `MedxSoft/MedxScribe` (`07060d4`),
      `MedxSoft/MedxScribe-spec` (`52c96cb`) and `MedxSoft/MedxScribe-code`
      (`023a27f`), set `xf-project-medxscribe` on all three, mounted the legs,
      wrote the shape pin, recorded the election by `brettheap` with the staged
      fragment as its `reference`, and recorded that `MedxScribe` also matches
      the descendant form with no referent pin. Bootstrap after
      `git clone --recurse-submodules` left both legs on `main` at their pins,
      the naming, manifest and lockstep-pin validators green, the shape copy pin
      (9 files) green, and printed `authority is not wallet-carried in this org`
      verbatim. **This record does not depend on the pilot repositories
      continuing to exist**, and the standard's own `tests/test_scaffold_e2e.py`
      re-runs the same path into bare repositories on every openRepoShape pull
      request.
- [ ] **6.2** On ratification, if the pilot has served its purpose, DELETE the
      three pilot repositories. Optional, the convener's call, and it retracts
      nothing: 6.1's record stands on its own.

## Slice 7 — successor: the codexFactory engineering overlay

- [ ] **7.1** Open a codexFactory change realizing the ENGINEERING OVERLAY on the
      neutral scaffold — the review-lane caller and engineering CI a scaffolded
      project may opt into — and recording that
      `add-wallet-carried-review-authority`'s task 8.4 is satisfied by
      overlay-plus-offer rather than by codexFactory hosting the neutral shape.
- [ ] **7.2** In that change, state the narrowing from codexFactory's own side,
      so the ratified sentence's reading is reconciled in BOTH repositories and
      not only in this one.

## Slice 8 — successor: OpsxFactory organisation administration

- [ ] **8.1** Open an OpsxFactory change realizing organisation-level naming
      enforcement and repository-topic administration for `xf-project-<id>`, in
      the GitHub administration plane where the two exit changes of the
      `github-administration-plane` topic located it.
- [ ] **8.2** Decide OI-1 there: what happens to a repository whose topic drifts
      from its register row. This packet states the drift RULE (the register
      wins, the others are reported) and no enforcement mechanism.

## Slice 9 — ratification and archive

- [ ] **9.1** **RATIFICATION — the convener's act.** Record it as
      `review/ratification-<date>.md` and move `Status:` to `ratified` with the
      citation, per the promoted lifecycle rule.
- [ ] **9.2** Before archive, re-verify the pin against openRepoShape at the
      recorded commit and re-run the four validator lines in slices 4 and 5, so
      the archive gate promotes deltas over a tree that still holds.
- [ ] **9.3** Package `supporting-docs/` into the deterministic bundle with its
      readable manifest (`proposal-support.py package`), per
      `release-realization`'s proposal-support archive gate.
