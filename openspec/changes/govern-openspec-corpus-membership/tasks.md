# Tasks: govern-openspec-corpus-membership

Nothing below §1 may start before §1 completes. This change proposes a
measurement rule and a scope boundary; until the six open questions are
ruled, there is no way to know which of three options the code implements.

The ordering constraint that is easy to get wrong: **§5 discharges the 68
standing violations, and §2's landing commit MUST NOT merge before §5 is
complete or explicitly dispositioned.** A gate that goes red on the commit
that introduces it teaches everyone to route around the gate.

## 1. Ratification (Brett)

- [ ] 1.1 Brett reads `proposal.md` — the measurement section especially,
      since the recommendation rests on numbers rather than on principle —
      and rules OQ-1 through OQ-6.
- [ ] 1.2 Brett ratifies or declines. On ratification, flip `Status: draft` →
      `Status: ratified` in `proposal.md` front matter and add the citation
      line in the spelling `docs/document-lifecycle.md` § Status Claim Rules
      selects: `Ratified by:` if an approving OpenSpec change is named,
      otherwise `Ratified:` naming an approver, a date, or a resolvable
      record. Keep it inside the fifteen-real-line header window — this
      change of all changes should not repeat the roster-device defect.
- [ ] 1.3 If OQ-1 is ruled **(a) full membership**, this proposal's spec
      deltas do not describe the ruling: replace them with a single
      `GOVERNED_ROOTS` widening, and carry the 573-finding, 13-point,
      123-test cost into §5 as the work it becomes.
- [ ] 1.4 If OQ-1 is ruled **(c) test-only**, delete
      `specs/doc-health/spec.md`'s ADDED requirement and the whole of
      `specs/document-lifecycle/spec.md` from this change — a standing test
      asserts nothing about promoted capability — and reduce §2 to a single
      test module.
- [ ] 1.5 If OQ-3 rules a different family set, amend the four family names
      in BOTH places they appear in `specs/doc-health/spec.md` (the MODIFIED
      requirement body and the "A run executes the check families" scenario)
      and in the ADDED requirement's scenarios. Three places, one list; the
      dropped-scenario lesson applies to lists too.
- [ ] 1.6 If OQ-6 rules the pre-contract-legacy grandfather, record the
      contract date Brett sets — the date itself is a ruling, not a
      derivation, and `proposal-origin`'s 2026-08-07 is a precedent for the
      shape and not for the value.

## 2. Realization (openxFactory main line)

- [ ] 2.1 `scripts/doc_health/corpus.py`: add `LIFECYCLE_SCAN`, a tuple of
      explicit glob patterns (`openspec/changes/**/proposal.md`,
      `openspec/changes/**/review/*.md` as ruled), and
      `load_lifecycle_docs(repo_name, repo_path)` beside `load_docs`. Reuse
      `_excluded`, `parse_status` and `parse_kind` — do not write a second
      header reader; `align-status-reader-to-real-lines` exists because the
      corpus grew seven of those.
- [ ] 2.2 `scripts/doc_health/runner.py`: one new `Context` field,
      `lifecycle_docs`, populated in `build_context` for every repo in scope
      by the same loop that builds `docs`. It MUST NOT feed
      `inventory`, `catalog_root`, the per-stage census, or the canon-share
      computation.
- [ ] 2.3 `scripts/doc_health/families.py`: `fam_status_validity`,
      `fam_standard_backing`, `fam_ratified_provenance` and
      `fam_succession_integrity` iterate `ctx.docs` plus
      `ctx.lifecycle_docs`. Introduce one shared accessor rather than four
      copies of the concatenation, so a fifth reader is a one-line opt-in
      and an audit can find every reader by call site.
- [ ] 2.4 Severity handling for the pre-contract-legacy population, per OQ-6:
      the reduced-severity rule string must name the class in the finding
      text the way `proposal-origin` does ("pre-contract legacy, no recorded
      migration"), so the ranked plan distinguishes backlog from regression
      without a reader consulting a date table.
- [ ] 2.5 `docs/document-lifecycle.md` § Status Claim Rules: state that a
      change packet's `proposal.md` and its `review/` ratification records
      are governance documents, that the rest of the packet is not ruled,
      and that a `Ratifier:`/`Decision date:` pair accompanies a sanctioned
      citation rather than replacing it. Authors read this file, not the
      family source.
- [ ] 2.6 Update `corpus.py`'s module docstring, which today says governance
      Markdown "lives under docs/, templates/, contracts/, examples/, and
      ideation/" and stops there. After this change that sentence is true of
      the governed corpus and incomplete about what the pass reads.

## 3. Tests (mutation-validated)

- [ ] 3.1 Membership: the scan set contains a packet's `proposal.md` and its
      `review/*.md`, and does NOT contain `tasks.md`, `design.md`,
      `specs/*/spec.md`, `supporting-docs/**` (including
      `source-snapshots/**`), or `evidence/**`. Assert on the resolved path
      list, not on a count — a count passes for the wrong set.
- [ ] 3.2 Each of the four families fires over a scan-set document, with a
      fixture per rule: uncited `ratified`, out-of-window `Status:`,
      free-form status, unbacked `standard`, `superseded` without successor.
- [ ] 3.3 Each of the other twelve families does NOT fire over a scan-set
      document. Drive this from `FAMILIES` itself so a family added later is
      covered by construction, and fail loudly if a new family appears in
      neither list. This is the test that makes §2.3's "one-line opt-in"
      safe.
- [ ] 3.4 The invariance test, which is the load-bearing one: over a fixture
      corpus with a non-empty scan set, `ctx.docs`, the per-stage counts, the
      governance and canon word totals, the canon-share string, the shared
      inventory entries and the catalog snapshot bytes are identical to the
      same run with an empty scan set. Compare rendered bytes, not summed
      integers.
- [ ] 3.5 The two historical defects, as regression fixtures rather than as
      prose: phase-b's uncited `ratified` header must produce a
      `ratified-provenance` finding, and roster-device's line-41 header must
      produce a `status-validity` missing-header finding and NOT a
      `ratified-provenance` one. Both were replayed against the real pre-fix
      blobs (`02a71d6` and `280fc8b`) while authoring this proposal; the
      fixtures freeze that result.
- [ ] 3.6 Mutation-validate 3.1 through 3.5. At minimum: flip the scan set to
      the empty tuple (3.1–3.3, 3.5 must fail), flip it to bare `("openspec",)`
      (3.1 must fail — the glob boundary is the claim), remove one family from
      the reader list (3.2 must fail), and add one family to it (3.3 must
      fail). Record which mutation each test caught. Beware the platform-inert
      class: a mutation that leaves observable values unchanged on this
      platform proves nothing, so pin the boundary with a structural assertion
      on the declared pattern set, not only on the resulting counts.
- [ ] 3.7 Confirm `tests/doc-health` is 724 + N and that no pre-existing test
      changed meaning. If any existing test needs editing, that is a finding
      about the design, not a chore: say so before editing it.

## 4. Gates, index, archive

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate govern-openspec-corpus-membership --strict`
      and `--all --strict` green (69 items at authoring; re-check the total
      against whatever else has landed).
- [ ] 4.2 `python3 -m pytest tests/doc-health` green;
      `python3 -m pytest tests/ideation-dashboard -k workbench` at 140.
- [ ] 4.3 A doc-health single-repo run whose severity counts move by exactly
      the predicted amount and in no other line. With §5 complete the
      prediction is the unchanged baseline, 4 critical / 6 error / 68 warning
      / 4 info; with §5 dispositioned rather than discharged it is 24 / 54 /
      68 / 4. Any third number is a defect in §2, not a surprise to accept.
- [ ] 4.4 Re-run the corpus-shape measurement and assert the canon-share
      headline, documents examined, and governance word total are UNCHANGED
      from baseline. This is the claim that distinguishes the ruled option
      from the one that was rejected, so it is measured rather than asserted.
- [ ] 4.5 README Active row updated when the change lands, moved to the
      archived block on archive.
- [ ] 4.6 Archive on merged-plus-green per `target_release: implemented` —
      no contract bundle is cut, so no release tag is owed.
- [ ] 4.7 Tick `sanction-ratified-record-spelling` task 5.1 with a pointer to
      this change and to the option ruled, under the append discipline that
      change's own §5.2 established. That box is the reason this change
      exists and closing it is part of finishing.

## 5. Discharging the 68 standing violations

Blocks §2's merge. Each item below is a ruling to execute, not a judgement to
make here.

- [ ] 5.1 The 6 ACTIVE proposals whose `Ratified by:` names a record rather
      than a change (`add-composed-view-authoring`,
      `add-lens-document-selection`, `add-trust-anchor`,
      `admit-install-repos-to-aggregation`, `implement-keycloak-install-repo`,
      `implement-openxpki-install-repo`): rewrite to the spelling OQ-4
      selects. No archived-record rule is engaged; these are live documents.
- [ ] 5.2 The 11 ARCHIVED proposals in the same class
      (`2026-07-30-add-ontology-stewardship-hardening`,
      `2026-08-04-adopt-neutral-utility-pack`,
      `2026-08-06-add-opendox-project-header`,
      `2026-08-06-add-project-scoped-selection`,
      `2026-08-07-add-project-merged-projection`,
      `2026-08-07-add-register-edit-lane`, `2026-08-08-add-openxwallet`,
      `2026-08-09-add-project-visible-set`, `2026-08-09-add-repository-lens`,
      `2026-08-13-add-session-notebook-reconciliation`,
      `2026-08-15-add-subject-overlay-contract`): route through the
      register's citing-change-plus-ruling path. One ruling may cover the
      block; the citing change still has to exist and say so.
- [ ] 5.3 The 3 `review/` ratification records using the third vocabulary
      (`add-roster-directory-admission-surface/review/ratification-2026-08-22.md`,
      `add-substantive-review-lane/review/ratification-2026-08-22.md`,
      `archive/2026-08-22-add-roster-device-admission-surface/review/ratification-2026-08-19.md`):
      execute OQ-5. Each already names its ratifier and its decision date, so
      a conforming line invents nothing.
- [ ] 5.4 The 1 free-form status
      (`add-wallet-carried-review-authority/proposal.md`, whose `Status:`
      value runs on into a ratification clause): split the value from the
      clause. The taxonomy value and the citation are two headers.
- [ ] 5.5 The 47 headerless proposals (44 archived, 3 active): execute OQ-6.
      If the grandfather is ruled, the 3 ACTIVE ones are still current
      violations and get headers now; only the 44 archived ones take the
      reduced severity.
- [ ] 5.6 Re-measure after 5.1–5.5 and record the resulting counts in this
      file. The number §4.3 checks against is whatever this task measures,
      not whatever this proposal predicted.

## 6. Explicitly out of scope

- [ ] 6.1 Whether `tasks.md`, `design.md`, spec delta files,
      `supporting-docs/` or `evidence/` are governance documents. 488 of the
      536 `status-validity` fires under full membership are these files, so
      this is the largest single question in the area and it deserves its own
      measurement rather than a ride on this one.
- [ ] 6.2 Widening `STATUS_SCAN_LINES` beyond fifteen real lines. Shared by
      `corpus.parse_status`, `families._header_lines` and
      `ideation_dashboard.generator._header_value`; moving it moves all three.
- [ ] 6.3 `record-immutability` over `openspec/`. Zero fires over the scan
      set today, and the family's "revert the content edit" remedy
      contradicts the archived-record append discipline, so wiring it is a
      ruling rather than a freebie. See design.md Decision 3.
- [ ] 6.4 The `location-conformance` and `tag-hygiene` false positives
      measured under full membership. They are not defects to fix here —
      under the ruled option those families never see the documents — but
      they are on the record in `proposal.md` for whoever revisits option (a).
