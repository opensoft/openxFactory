# Tasks: add-subject-establishment

Governance-level and dependency-ordered. **This change is not implemented
here**: § Admission and § Implementation are done at authoring, and everything
after them belongs to a later ruling round, to the named successor, and to
consuming repositories. Every fact quoted below was measured on 2026-08-28 in a
fresh worktree off `origin/main` at `3cebf83e` and re-measured after each of
the three merges of `origin/main` since — `571e64d5` (2026-08-28), `95c2cf6a`
and `56e12278` (both 2026-09-04); a task citing a line number owes a re-read at
realization rather than a copy of the number. **THE CONTRACT BUNDLE MOVES UNDER
THIS PACKET FASTER THAN ANY PROSE CAN NAME IT, WHICH IS ITSELF THE ARGUMENT FOR
`target_release: none`**: it was `contract-v2.0` at authoring, `contract-v2.1`
at the first merge, and **`contract-v3.2` as declared today**
(`contracts/manifest.yaml:3`) — four minors and a major. `proposal.md`'s
`target_release` parse has been rerun at each step and the CURRENT reading is
against `contracts/releases/contract-v3.2.digests.yaml`: **283 entries, none of
them a path this change writes**, with `contract-v3.1` and `contract-v3.0`
walked as well and reading the same. The superseded `contract-v2.1` measurement
(192 entries, same verdict) is retained in `proposal.md`'s front matter for
history and is deliberately not repeated here. The value stays `none`; it has
been re-measured, never retargeted.

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
      which is not this packet's to run. **AND THIS CHANGE DOES NOT MAKE THE INDEX
      STALE**, which is the load-bearing fact: the index is REVISION-ADDRESSED
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
      assertion beside it does not move.
      **THE COUNT HAS MOVED FOUR TIMES AND EVERY MERGE KEPT EVERY STEP.**
      This line conflicts on every catch-up merge, by design, and has been
      resolved ADDITIVELY every time rather than by overwrite — each step keeps
      its own comment, attributed to the packet that took it:
      66 → 67 the sibling `add-worker-enrollment-broker` promotion (2026-08-28,
      landed on `origin/main` first); 67 → 68 THIS packet (2026-08-28);
      then `main` moved twice more under the branch — 68 → 69 by
      `add-project-repo-schema`'s promotion manifest and 69 → 70 by
      `contracts/openreposhape-pin.yaml`'s `commit`, which is ALSO the one step
      that took the member count off 23 by declaring the new
      `openreposhape-pin-product-commit` member.
      **AS OF THE 2026-09-03 MERGE THE ASSERTION READS 70 SITES / 24 MEMBERS**,
      this packet's manifest being one of the seventy and its member one that
      already existed. RE-ENUMERATED with `pin_class.verify()` on the merged
      commit rather than by arithmetic at every step, since `pc.verify` reads the
      COMMITTED tree and answers the pre-merge number until the merge commit
      exists — which is why a promotion's own pre-commit run passes and CI is
      where the count lands.

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
      **RE-MEASURED ON THE MERGED HEAD**, after `origin/main` brought in the
      sibling `add-worker-enrollment-broker` full promotion: 4 / 47 / 97 / 14,
      with `staged-candidate-aging` 114 → 112, `staged-topic-template` 27 → 25
      and `location-conformance` 3 → 2. The extra −1 in each family is the
      SIBLING's promotion, not this one's — attributed rather than absorbed,
      because a merged number that silently doubles a claimed effect is worse
      than no number. This packet's own contribution is unchanged at −1 and −1,
      and it moves no `location-conformance` finding because the topic carried
      none.

## Archive gate

- [x] G.1 **The gate is merge plus green PLUS the ruling round (OD-6), which is
      deliberately stricter than what `code_surface: none` alone would
      require.** All six § Orchestrator decisions ruled and all six § Open
      Questions answered. The change stays ACTIVE until then, because a
      promoted capability carrying unruled questions is canon with invisible
      holes in it. **DONE 2026-09-04**: Brett Heap, in session, recorded on
      PR #491, verbatim "accept all, recommendations stand" — all six OD-1 …
      OD-6 ACCEPTED AS PROPOSED and all six OQ1 … OQ6 RULED as their stated
      recommendations. Record: `review/ratification-2026-09-04.md`. The
      change archives on the merge of PR #491, per this estate's standing
      `code_surface: none` convention, not in this commit.
- [x] G.2 If OD-1 is VETOED, this gate grows: the schema surface, its
      validator, its packaged fixtures, and the additive contract cut all land
      before archive, and `code_surface` / `target_release` are rewritten to
      declare them. **MOOT as of the 2026-09-04 ruling**: OD-1 was ACCEPTED
      AS PROPOSED, not vetoed — the counter-precedent from PR #479 was
      disclosed to the owner and he accepted OD-1 anyway. This gate does not
      fire; `code_surface: none` and `target_release: none` stand unchanged.

## Open

**ARCHIVED 2026-09-04 VIA THE RECORDED ESCAPE, AND THE SEVEN BOXES BELOW ARE WHY.**
`python3 scripts/proposal-support.py . archive add-subject-establishment` was
tried FIRST and REFUSED — exit 1, `"change has incomplete tasks"`. Its gate is
`tasks.is_file() and re.search(r"^- \[ \]", tasks.read_text(), re.M)`
(`scripts/proposal-support.py:1079-1081`) — **unconditional on WHICH box**, and every
open box in this packet is in this section: O.1 … O.7 record OWED SUCCESSOR AND
CROSS-REPOSITORY WORK — the named successor `add-subject-establishment-contracts`
(OD-1, accepted as proposed on 2026-09-04), OQ1's measurement pass travelling
with it, a LedgerxFactory act over ARCHIVED records this repository holds no
authority to edit, the codexFactory and OpsxFactory consumer instantiations,
DTN-015's loop before it leaves `seed`, and MedxFactory as third consumer.
**NOT ONE OF THEM IS UNDONE WORK OF THIS CHANGE**, and ticking any of them to
satisfy the wrapper would be writing a false completion to get past a gate that
cannot tell "open by omission" from "open by design" apart. Both gate sections
above — § Verification and § Archive gate, G.1's merge-plus-green PLUS the
ruling round — are TRUE and ticked.
`OPENSPEC_TELEMETRY=0 openspec archive add-subject-establishment --yes` was run
instead, reporting `Task status: 22/29 tasks` and
`Warning: 7 incomplete task(s) found. Continuing due to --yes flag.` It created
`openspec/specs/subject-establishment/spec.md` (`+ 11 added`, `~ 0`, `- 0`) and
moved the packet to
`openspec/changes/archive/2026-09-04-add-subject-establishment/`.
**PRECEDENT, cited rather than invented**: `declare-spent-bundle-state`'s
§ 5.1 (PR #611, squash `7af2725c`, 2026-09-03), which took the same escape for
the same reason over its task 3.2, itself following
`govern-sibling-added-modified-deltas` (PR #571, squash `3bcde7e2`). The one
DIFFERENCE from #611 is worth stating: there the open box named a FUTURE EVENT
the act could not discharge; here the open boxes name OWED SUCCESSOR WORK owned
by other packets and other repositories. Both are "open by design"; neither is
this archive's to close.
**THE PROMOTION WAS BYTE-CHECKED, not trusted**: the requirement text of the
created `openspec/specs/subject-establishment/spec.md` was extracted from its
first `### Requirement:` line and diffed against the same extraction from the
archived delta at `specs/subject-establishment/spec.md` — IDENTICAL but for one
trailing blank line the archiver emits, with **11 requirements / 37 scenarios**
on both sides and no other file under `openspec/specs/` touched.

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
