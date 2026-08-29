# Tasks: add-subject-establishment

Governance-level and dependency-ordered. **This change is not implemented
here**: § Admission and § Implementation are done at authoring, and everything
after them belongs to a later ruling round, to the named successor, and to
consuming repositories. Every fact quoted below was measured on 2026-08-28 in a
fresh worktree off `origin/main` at `3cebf83e` and re-measured after
`origin/main` was merged in at `571e64d5`; a task citing a line number owes a
re-read at realization rather than a copy of the number. **One number moved at
that merge and is corrected rather than left standing**: the declared contract
bundle went `contract-v2.0` → `contract-v2.1` under this branch, so
`proposal.md`'s `target_release` parse was rerun against
`contracts/releases/contract-v2.1.digests.yaml` — 192 entries, none of them a
path this change writes.

## Admission

- [x] A.1 Origin recorded: staged topic `subject-establishment`, taking its OWN
      declared exit path on Brett's ruling of 2026-08-28, verbatim
      "Progress both". `.openspec.yaml` carries `origin.kind: staged` with the
      topic's staging id and path, the ruling as the instruction that triggered
      the exit, and the two voices kept apart — the Group-4 recommendation was
      the orchestrating session's wording, the selection was Brett's.
- [x] A.2 Both of the topic's declared exit gates verified CLEAR rather than
      assumed. **Gate 1 — LedgerxFactory reaching proposal — CLEARED
      2026-08-04**, verified read-only in the LedgerxFactory checkout
      (`git ls-tree origin/main openspec/changes/archive/`): three packets
      archived that day —
      `2026-08-04-add-ledgerx-company-provisioning-and-setup-audit`,
      `2026-08-04-add-ledgerx-msbc-company-realization`,
      `2026-08-04-modify-ledgerx-ap-intake-for-onboarding-readiness`. The gate
      asked for "reaching proposal"; it reached archive. **Gate 2 — a second
      domain naming its instance — CLEARED 2026-07-28** by Brett's decision of
      codexFactory new-project, recorded in the topic's own open question 4 and
      in the register's DTN-017 section.
- [x] A.3 Capability-name collision check, by enumeration rather than by
      assumption: no directory under `openspec/specs/` is named
      `subject-establishment`, and enumerating every `specs/<capability>/`
      directory across every non-archived change under `openspec/changes/`
      returns no match. Re-measure before merge — active changes land daily.

## Implementation

- [x] I.1 `specs/subject-establishment/spec.md` — ELEVEN ADDED requirements, 37
      scenarios, ADDED-only with no MODIFIED block anywhere: the neutral
      pipeline over two artifact kinds; provenance-graded facts; the
      vendor-free neutral design; the one-system-per-realization artifact; the
      reference-archetype lifecycle; conformance tiering as the ratified
      escalation ladder; the cross-factory handoff; verify-by-read-back; the
      two authority classes; the audit-lift mirror; layer ownership without
      storage.
- [x] I.2 Verify no active change touches a requirement this delta touches.
      Measured: this is a NEW capability, so no promoted requirement exists to
      collide with, and no active change carries a
      `specs/subject-establishment/` directory. The three capabilities this
      delta CONSUMES — `deployment-handoff-boundary`, `roles-authority-model`,
      `governed-derived-model` — are cited and unmodified; the delta writes no
      file under their spec directories.
- [x] I.3 `OPENSPEC_TELEMETRY=0 openspec validate add-subject-establishment
      --strict` and `--all --strict` green.
- [x] I.4 `proposal.md` § Orchestrator decisions — six decisions, each stated
      with the cost of vetoing it, and OD-1 additionally carrying the live
      counter-precedent that the same call went the other way in
      `add-credential-escrow-checkout` on the same day.
- [x] I.5 `proposal.md` § Open Questions — six questions, each with a
      recommendation and NO decision, and the delta authored so that no ruling
      is forced by implication.
- [x] I.6 `design.md` — six sections: why the generalization is real, why the
      schemas are deferred (argued against the counter-precedent), the
      cross-factory seam, why the dial is the escalation ladder, what read-back
      costs, and the boundary this refuses to cross; plus five recorded risks.

## Bookkeeping (this change)

- [x] B.1 Topic exit executed with the repository's own tool rather than by
      hand: `python3 scripts/proposal-support.py . transition
      add-subject-establishment ideation/staging/subject-establishment --apply`,
      which moves the topic's one file into `supporting-docs/` and rewrites its
      header and pointer.
- [x] B.2 FULL promotion bookkeeping, per the maintenance rule at
      `ideation/staging/INDEX.md` § Maintenance rule: no staged file remains,
      so the topic's ROW and DETAIL SECTION are DELETED from the index and the
      pointer lands in `ideation/README.md`'s "Active proposals promoted from
      staging" list, in the `qualify-avatar-live-voice` entry's format.
- [x] B.3 DTN-017's register row moved `staged` → **`openspec`**, which is the
      value the register's own status lifecycle prescribes for a filed change:
      "`seed` -> `staged` -> `openspec` -> `implemented` -> `adopted`", with
      `openspec` glossed there as "proposed/ratified"
      (`docs/domain-neutralization-candidate-register.md`, § Candidate List).
      `implemented` is NOT taken, because it maps to "implemented/promoted" and
      nothing is promoted until this change archives. The DTN-017 detail
      section gains a dated line naming this change.
- [x] B.4 Repository README "OpenSpec Records" active entry.
- [x] B.5 `ideation/cross-reference.*` DELIBERATELY NOT REGENERATED, and the
      reason is a measurement rather than a preference. The index is NOT
      produced by a mechanical script: `scripts/bootstrap-ideation-cross-reference.py`
      is a ONE-TIME SEED whose own help text says the real clustering and
      scoring is realized by the codexFactory readiness worker, and the landed
      index carries `Generator: ideation-xref-scorer-0.1.0` with a pinned
      `generation.source_revision`. Running the bootstrap here was TRIED and
      REVERTED: it produced a 3177-line deletion, dropped the corpus from 290
      clusters to 287, regressed the generator id to
      `ideation-xref-bootstrap-0.1.0`, and replaced the pinned source revision
      with `uncommitted-worktree` — a destructive downgrade of the scorer's
      output, not a regeneration of it. The correct regenerator is the nightly
      readiness lane (`scripts/ideation-readiness-nightly.py`, an LLM dispatch),
      which is not this packet's to run. **AND THE INDEX IS NOT STALENED BY THIS
      CHANGE**, which is the load-bearing fact: the index is REVISION-ADDRESSED
      and is proved against the corpus AT ITS OWN PIN rather than against HEAD,
      a property `6f9d9e0c` established on purpose. Verified rather than
      asserted — `tests/doc-health/test_pin_reachability.py`,
      `test_ideation_readiness.py` and `test_readiness_proof_resolution.py`, 126
      passed, after the topic file moved. The index's one membership row naming
      `ideation/staging/subject-establishment/subject-establishment.md` is
      correct AS OF ITS PIN and is superseded at the next nightly lane run.
- [x] B.6 Test and doc-health measurements recorded before and after, with the
      families that legitimately move named in advance and every other family
      asserted unmoved.
- [x] B.7 Re-baseline the PIN-SITE SELF-GATE in the same commit that moves it.
      `tests/doc-health/test_sentinel_vocabulary.py::test_the_pin_counts_did_not_move_and_no_site_is_classified_twice`
      asserts an exact site count, and this packet's
      `supporting-docs/manifest.yaml` carries a `source_revision` pin, so the
      count goes 66 → 67. **This is the gate working, not a test edited to
      pass**: the count moves by design on every full promotion, the assertion
      exists so that nobody adds a pin site without a human looking at it, and
      the edit carries a comment recording exactly which site arrived and why.
      Enumerated rather than inferred — `pin_class.verify()` was run and the
      single new site is this packet's manifest, joining the EXISTING
      `proposal-support-manifest` member class, which is why the member-count
      assertion beside it is unchanged at 23.

## Verification

- [x] V.1 `OPENSPEC_TELEMETRY=0 openspec validate add-subject-establishment
      --strict` — valid.
- [x] V.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — green.
- [x] V.3 `set -o pipefail; python3 -m pytest tests/doc-health
      tests/proposal-support tests/ideation_routing tests/document_catalog -q`
      — 1455 passed, rc 0, BEFORE; 1455 passed, rc 0, AFTER, once B.7's pin-site
      self-gate was re-baselined. The intermediate state is recorded rather than
      hidden: the first after-run was 1 failed / 1454 passed on exactly that
      gate, which is how B.7 was found. No client-identity doc-health failure
      appeared in this worktree.
- [x] V.4 doc-health single-repo run before and after at a common `--as-of`, so
      a day boundary cannot be mistaken for an effect. Families expected to
      move and why: `staged-candidate-aging` −1 (the topic folder leaves
      staging), `staged-topic-template` −1 (its primary fragment leaves
      staging). `location-conformance` is expected UNMOVED — measured at
      authoring, this topic carried none of its three findings. Every other
      family asserted unmoved, and any movement reported rather than explained
      away. **MEASURED, at a common `--as-of 2026-12-31`, single-repo**:
      headline 4 critical / 50 error / 99 warning / 14 info BEFORE, 4 / 49 / 98
      / 14 AFTER. Exactly the two predicted families moved —
      `staged-candidate-aging` 114 → 113 and `staged-topic-template` 27 → 26 —
      and all twenty-three other families are byte-identical in count,
      `location-conformance` (3 → 3), `modified-block-currency` (10 → 10),
      `proposal-origin` (0 → 0), `promotion-fidelity` (0 → 0) and
      `release-inventory-drift` (0 → 0) among them.

## Archive gate

- [ ] G.1 **The gate is merge plus green PLUS the ruling round (OD-6), which is
      deliberately stricter than what `code_surface: none` alone would
      require.** All six § Orchestrator decisions ruled and all six § Open
      Questions answered. The change stays ACTIVE until then, because a
      promoted capability carrying unruled questions is canon with invisible
      holes in it.
- [ ] G.2 If OD-1 is VETOED, this gate grows: the schema surface, its
      validator, its packaged fixtures, and the additive contract cut all land
      before archive, and `code_surface` / `target_release` are rewritten to
      declare them.

## Open

- [ ] O.1 **Named successor `add-subject-establishment-contracts`** (OD-1, if
      it stands): `contracts/schemas/xfactory-subject-design.schema.yaml`,
      `contracts/schemas/xfactory-platform-realization.schema.yaml`,
      `scripts/validate-subject-establishment.py`, and packaged positive and
      negative fixtures for the refusals requirements 1, 3, 4, 6, 8 and 9 name.
      To be authored AGAINST a domain instantiation, not ahead of one.
- [ ] O.2 **RULED OQ1's measurement pass**, owned by the successor: is "system
      of record" new neutral vocabulary or the existing estate /
      `client-infrastructure-request` execution-binding vocabulary generalized?
      The answer changes a field, not a requirement, which is why it travels
      with the schema.
- [ ] O.3 **CROSS-REPO FOLLOW-UP, OWNED BY LedgerxFactory, NOT FIXED HERE.**
      The first instantiation of this pipeline is LedgerxFactory's three
      packets archived 2026-08-04, and they cite NOTHING neutral — because on
      2026-08-04 there was nothing neutral to cite. That is not a defect in
      those packets. It is also not fixable from here: they are ARCHIVED
      records in a repository this change holds no authority over, and editing
      an archived record is refused by `record-immutability` on principle
      before it is refused by repository boundaries. The follow-up is a
      LedgerxFactory ACT — record its company-provisioning capability's
      conformance to `subject-establishment` in a NEW record once this
      capability promotes — and it belongs on that repository's queue, not on
      this packet's gate. Named here so it is not lost, and owned there so it
      is not mistaken for work this change deferred.
- [ ] O.4 **codexFactory second-consumer instantiation.** The mapping is
      decided and tabled; no codexFactory change instantiates it. Its
      realization artifact must be handoff-shaped under requirement 7, crossing
      to OpsxFactory's `github-administration-workflow` as a
      `client_infrastructure_request`. If it cannot express itself in these
      eleven requirements, the requirements are wrong and this is where that is
      discovered.
- [ ] O.5 **OpsxFactory as a consumer in its own right** (OQ6) — its
      new-managed-estate motion, distinct from its role as codex's applier.
- [ ] O.6 **Re-express requirement 5's archetype harvest through DTN-015's
      correction→promotion loop** once DTN-015 leaves `seed`. Requirement 5
      states the harvest's invariants and names no mechanism precisely so that
      this is a refinement rather than a contradiction (OQ2).
- [ ] O.7 **MedxFactory new-patient as the third consumer**, named in the
      staged topic as the richest consent and custody case, and the natural
      place to prove OQ5's composition with `consent-instrument` (DTN-016).
