# Tasks: declare-sentinel-pin-vocabulary

§ 1 records the filing and what was measured before anything was written. § 2 is
the implementation, unstarted. § 3 is the existing sentinel inventory and what
happens to each site. § 4 is the archive gate. § 5 carries the follow-ups this
change deliberately does not write.

**READ THIS FIRST IF YOU ARE ABOUT TO REALIZE THIS PACKET.** Two things in it are
easy to get backwards. **A legal non-pin does NOT hold full verification open** —
an artifact carrying an honest sentinel is conforming, and reporting it as an
open item punishes the behaviour this packet exists to require. **And the seven
committed sentinel values are NOT to be edited** — every one sits inside an
archived packet, and normalizing their spellings is the content edit this
capability's own rule refuses. The vocabulary absorbs them; they do not move.

**THE VETO WINDOW CLOSED 2026-08-27 AND THE RULINGS ARE RECORDED IN PLACE**, at
§ 1.12 with the delta text they moved. Three of them bind realization directly:
Q1 settles § 2.1 and § 2.6, Q3 adds a seeding obligation that § 2.3 must satisfy
before the defect branch runs, and Q4 makes § 2.7 unconditional. The paragraphs
above are unchanged by all of it — nothing ruled licenses deleting a member or
editing a committed manifest.

## 1. Filing and admission

- [x] 1.1 ORIGIN AND APPROVAL ARE RECORDED FROM THE COMMISSION ITSELF, on the
      `govern-derived-pin-reachability` / `supersede-lost-pin-baseline`
      instruction-as-origin-act shape rather than the blank-pair shape. Brett
      commissioned the filing on 2026-08-27, verbatim: "file the
      sentinel-vocabulary follow-up change". `approved_by` / `approved_on` are
      filled from that act, and both state in their own text that THE CITATION
      COVERS THE DECISION TO FILE AND NOTHING ELSE.
- [x] 1.2 THE EARLIER RULING THAT CONSTITUTED THE PACKET IS RECORDED AS A
      SEPARATE ACT, because it authorized something different. At the
      `govern-derived-pin-reachability` archive the same day, Brett selected
      verbatim: "Named follow-up (Recommended): Record it beside the §5.3
      git_generation() follow-up — they're the same idea (honest non-pins) and
      should be one future packet". That ruling fixed the packet's SCOPE — two
      deferred items, one packet — and explicitly deferred the substantive
      question to the future packet. It did not order the filing; the commission
      at § 1.1 did.
- [x] 1.3 `kind: staged` was checked before being declined. `ideation/staging/`
      and its `INDEX.md` carry nothing on derivation pins, non-pin values or
      generator provenance. **The word "sentinel" DOES occur there and is a false
      positive**, recorded so a later reader does not chase it: in
      `recurrence-crystallization` it is the statistical sense — a sentinel
      fraction, `sentinel_epsilon_start`, `sentinel_epsilon_floor`, sentinel
      sampling rates. `kind: ad_hoc` is unavailable-otherwise rather than
      preferred.
- [x] 1.4 THE `git_generation()` DEFECT WAS RE-CONFIRMED ON CURRENT MAIN rather
      than inherited from the record.
      `scripts/bootstrap-ideation-cross-reference.py:144-154` runs
      `rev-parse HEAD`, writes it as `generation.source_revision`, and carries no
      `status --porcelain`, no `diff --quiet`, no sentinel branch and no fallback;
      `check=True` means a git failure raises rather than degrading.
- [x] 1.5 THE SENTINEL SITES WERE RE-COUNTED FROM THE DECLARED GLOBS, not from
      the archived count. Enumerating the four `proposal-support-manifest` path
      globs yields **34 manifests: 24 real forty-character pins, 6
      `"uncommitted-worktree"`, 1 `"not-applicable-ad-hoc"`, 3 with no
      `source_revision` key**. The archived count is confirmed exactly. **All ten
      non-pin manifests are ARCHIVED; not one is active.**
- [x] 1.6 THE INHERITED PREMISE WAS FALSIFIED AND THE CORRECTION RECORDED RATHER
      THAN SMOOTHED. `govern-derived-pin-reachability` § 5.1 and the README entry
      derived from it state the proposal-support generator "already refuses to
      write a pin it cannot mean". **It does not.**
      `git log -S"uncommitted-worktree" -- scripts/` is EMPTY across all history,
      as is the same search for `"not-applicable-ad-hoc"`; neither string has ever
      existed in any script. `scripts/proposal-support.py:175-180`
      `repo_revision()` returns `rev-parse HEAD` or the bare string
      `"uncommitted"` — a third spelling — and only on a NON-ZERO EXIT, never on a
      dirty tree. The seven sentinel values were hand-written. Corroborated by the
      manifests themselves, which carry a prose `source_state` key the generator
      never writes and a null `source_path` where it always writes a real one.
      Recorded in `.openspec.yaml`, `proposal.md` § What was measured, and OD-4.
- [x] 1.7 THE LATENT DRIFT FAULT WAS RUN, NOT PREDICTED. Three guards in
      `scripts/proposal-support.py` (`:184`, `:632`, `:737`) compare against the
      literal `"uncommitted"`. Executed against this worktree:
      `git_blob_sha256(root, "uncommitted-worktree", "README.md")` raises
      `SupportError: invalid repository revision: uncommitted-worktree`, while
      `"uncommitted"` returns `None`. LATENT only because the crashing guard is on
      the active-support path and all seven sentinel manifests are archived.
- [x] 1.8 THE INVISIBILITY WAS MEASURED AT THE REGEX, not inferred from the
      report. `scripts/doc_health/pin_class.py` binds the value group of both
      `_field_re` and `_VOCAB_RE` to `([0-9a-f]{40})`, so a sentinel value creates
      no `PinSite`: not reachable, not orphaned, not lost, **and not uncovered**.
      The probe at `b5fb03f3` reports **65 declared pin sites across 22 class
      members — 50 reachable, 0 orphaned, 1 lost (declared unrecoverable, 0
      awaiting a superseding record), 0 inconclusive; 0 uncovered, 0 vanished, 0
      future members now carrying pins** — a fully verified class over seven
      artifacts whose provenance claim nothing has read.
- [x] 1.9 THE OTHER SPELLINGS WERE SWEPT RATHER THAN GUESSED. Six exist:
      `"uncommitted"` (`proposal-support.py:180`), `"uncommitted-worktree"` and
      `"not-applicable-ad-hoc"` (hand-written), `"unknown"`
      (`ideation_dashboard/snapshot_registry.py:283`;
      `experiments/avatar-brokered-call/src/avatar_f0/cli.py:51,60`), `"composed"`
      (`snapshot_registry.py:647`), beside the adjacent verdict constant
      `pin_class.NOT_APPLICABLE`. **`"unknown"` and `"composed"` appear in no
      governance document at all**, which is Q3.
- [x] 1.10 THE CAPABILITY COLLISION CHECK WAS RUN BEFORE CHOOSING ALL-ADDED. The
      only active change touching `doc-health` is `add-nightly-dashboard-refresh`
      (seven ADDED requirements, all about the refresh lane); no active change
      touches `ideation-cross-reference`. Canon stands at 36 `doc-health`
      requirements and 16 `ideation-cross-reference` requirements. No `MODIFIED`
      block is written in either capability and no promoted requirement is
      restated.
- [x] 1.11 FILING GATE GREEN.
      `OPENSPEC_TELEMETRY=0 openspec validate declare-sentinel-pin-vocabulary
      --strict` passes, `--all --strict` passes, and
      `python3 -m pytest tests/doc-health -q` under `set -o pipefail` reports
      **1209 passed** — unchanged from the baseline measured on this worktree
      before anything was written, as it must be for a delta-only filing.
- [x] 1.12 THE VETO WINDOW IS CLOSED, 2026-08-27. All five § Orchestrator
      decisions CLEARED AS AUTHORED and all four § Open Questions RULED, by a
      four-question multi-choice put to Brett by the orchestrating session and
      relayed the same day. He took the packet's recommendation on every question,
      so **the clearance moved nothing** — OD-1 through OD-5 stand exactly as
      written — but **three of the four rulings MOVED DELTA TEXT**, which the
      clearance did not: Q1 (declare BOTH spellings with DISTINCT meanings —
      `"uncommitted-worktree"` canonical for a dirty tree, `"uncommitted"` its own
      member meaning unreadable repository), Q2 (an absent key is NOT an honest
      non-pin; declared a recognized legacy state, never a member) and Q3
      (`"unknown"` and `"composed"` JOIN, so the undeclared-value-is-a-defect
      clause cannot flag the snapshot registry's own committed output at
      realization). Q4 RULED: the `proposal-support.py` guard repair is IN SCOPE
      for this realization. Scenario counts moved 8/8 → 9/10, additively; the
      requirement count is unchanged at four. **THIS IS A THIRD ACT, DISTINCT FROM
      BOTH THE COMMISSION (§ 1.1) AND THE CONSTITUTING RULING (§ 1.2).** No
      verbatim wording reached this session, so none is quoted — approver, date,
      mechanism and selections are recorded instead.
- [x] 1.13 THE MERGE IS APPROVED ON GREEN AND IS NOT THIS SESSION'S TO PERFORM.
      The orchestrating session merges; this session records the rulings, pushes
      and stops. Recorded because a packet that says "archives only after green"
      should also say who does it.

## 2. Implementation — REALIZED 2026-08-27

Every box below carries the evidence under it. Two decisions the packet left
open were settled by measurement and both are written where they were made:
`"unknown"` is its OWN condition rather than a second spelling of
`"uncommitted"`'s (§ 2.2), and `repo_revision()` is deliberately NOT given a
dirty-tree branch because this mover already refuses rather than lying (§ 2.7).
The second diverges from the instruction that reached the realizing session and
is flagged there for review rather than folded in quietly.

- [x] 2.1 Q1 IS SETTLED AND THE BLOCK IS LIFTED, 2026-08-27. **Both spellings are
      members with DISTINCT meanings**: `"uncommitted-worktree"` canonical for the
      DIRTY-TREE condition, `"uncommitted"` its own member meaning UNREADABLE
      REPOSITORY. Neither is legacy relative to the other, because they name
      different conditions. This determines what `git_generation()` writes
      (§ 2.6 — the dirty-tree member), what the declaration may mark legacy
      (§ 2.2 — only within one condition), and what the guards are reconciled
      against (§ 2.7). **The box is ticked because the ruling is the task**; the
      code it unblocks is § 2.2 onward and stays unticked.
- [x] 2.2 DECLARE THE VOCABULARY beside `scripts/doc_health/pin_class.py`, in the
      registry-module form Q1 of `govern-derived-pin-reachability` ruled for the
      class itself. Every member states its condition and whether it is canonical
      for new output or a legacy spelling retained for committed state.
      **THE RULED MEMBERSHIP, from the 2026-08-27 rulings**: the dirty-tree
      condition (`"uncommitted-worktree"`, canonical), the unreadable-repository
      condition (`"uncommitted"`, Q1; `"unknown"`, Q3), the outside-a-repository
      condition (`"not-applicable-ad-hoc"`), and the composed-projection condition
      (`"composed"`, Q3). **ONE POINT NEITHER RULING SETTLES AND THIS PACKET DOES
      NOT INVENT**: `"unknown"` also stands for an unreadable revision, so whether
      it is a second spelling of `"uncommitted"`'s condition — and if so which of
      the two is canonical for it — or a condition of its own is resolved at
      realization under the same-condition rule the delta states. **AND ABSENCE IS
      NOT A MEMBER** (Q2): the declaration recognizes it as a legacy state and
      refuses it membership.
      **DONE 2026-08-27** — `scripts/doc_health/pin_sentinels.py`, a registry
      module beside the class, importing nothing outside the standard library so
      the two hyphenated standalone scripts can consult it rather than respell
      it. Five conditions in `CONDITIONS`, five members in `SENTINELS`, each
      stating its condition, its standing and its emitters;
      `declaration_defects()` refuses a member without them and refuses a
      condition with anything but exactly one canonical spelling. Absence is
      declared in `ABSENT_KEY` as a recognized legacy state and is NOT a member.
      **THE CARRIED POINT IS DECIDED AND `"unknown"` IS ITS OWN CONDITION, ON
      MEASUREMENT.** The same-condition rule folds two spellings only where
      measurement shows ONE condition, and the three emitters show three:
      `snapshot_registry.py:283` writes it while projecting an index entry whose
      recorded revision is absent — the repository perfectly readable;
      `avatar_f0/cli.py:60` (`_git_head`) writes it when `rev-parse HEAD`
      answers nothing, which IS the unreadable-repository condition;
      `avatar_f0/cli.py:51` (`_git_file_commit`) writes it when `git log -1 --
      <path>` SUCCEEDS and finds no commit, which means the repository is
      readable, `HEAD` resolves, and the named content has never been committed.
      Folding it into `"uncommitted"` would make every artifact carrying it
      assert "the repository could not be read at all", which is FALSE at two of
      the three. It is declared instead as `unestablished-revision` — the
      weakest member, carrying the instruction that a generator able to
      distinguish must reach for a stronger one. Pinned by
      `test_unknown_is_not_folded_into_the_unreadable_repository_condition`,
      which re-reads both emitter sites. Splitting those three call sites onto
      the conditions they mean is recorded as a NAMED FOLLOW-UP in the module
      docstring, not performed.
      **AND `"composed"` IS DECLARED WITH THE QUALIFIED FORM ITS EMITTER
      ACTUALLY WRITES.** `compose_snapshots` seeds `composed` and then replaces
      it with `composed:<repo>@<ref>:<sha>,…`; declaring only the bare spelling
      would have left the lane's real output undeclared, which is precisely what
      Q3's seeding ruling forbids. The prefix is declared ON THE MEMBER, so it
      is a declared form rather than the near-miss matching the delta refuses.
- [x] 2.3 CLASSIFY THE VALUE in `pin_class.py`. A non-commit value under a
      declared pin key becomes a site with one of two outcomes — legal non-pin
      (declared) or defect (undeclared) — rather than no site at all. The
      commit-shaped path is untouched: same regexes for pins, same ref set, same
      verdicts.
      **DONE 2026-08-27** as a SEPARATE PASS over the same inventory rather than
      a widening of the pin path: `_field_re` and `_VOCAB_RE` are byte-unchanged,
      and the new `_wide_field_re` / `_WIDE_VOCAB_RE` skip any value
      `FULL_SHA_RE` matches, so no site can be classified twice and no
      reachability verdict is reachable through the new code
      (`test_a_commit_shaped_value_is_untouched_by_the_classification`,
      `test_the_pin_counts_did_not_move_and_no_site_is_classified_twice`).
      **THE WIDE REGEX ANCHORS THE KEY WHERE THE OLD ONE DID NOT HAVE TO.**
      `_field_re` gets away with a bare key boundary because forty hex
      characters almost never follow a colon inside a sentence; widen the value
      and that accident is gone. A naive widening measured over the real
      repository reported two sites that are not mapping keys at all — `Live
      commit:path resolution…` inside a folded `detail: >-` block, and a
      `` `commit:` above `` inside a YAML comment. So `_MAPPING_KEY_ANCHOR`
      requires the key to stand at a mapping position and whole-line comments
      are dropped; both false positives fail STRUCTURALLY rather than on their
      value's shape, which matters because a value's shape is exactly what this
      path may not judge on
      (`test_a_key_name_quoted_in_prose_or_a_comment_is_not_a_site`).
      **THE SEEDING OBLIGATION IS DISCHARGED AND COST TWO DECLARED EXCLUSIONS,
      both measured and both inert for the commit path.** The widened sweep over
      committed state at 45ba637a found exactly two non-commit values that name
      no condition, and neither has a generator to correct: `revision: <current
      full commit>` in `document-catalog.template.yaml:42` (an instantiation
      placeholder inside an ARCHIVED packet, so its bytes may not be edited) and
      `source_commit: {type: string, minLength: 1}` in
      `specs/002-avc-f0-feasibility/contracts/f0-interface-impact.schema.yaml:34`
      (a JSON-Schema key DECLARATION, not a value). Both are resolved the only
      way left open — a `NON_MEMBERS` row with a stated reason, on the same
      ground the examples and `contracts/schemas/**` rows already stand on. Both
      rows are inert for reachability: no committed `*.template.*` and no
      committed `*.schema.*` file inside the scan roots carries a
      forty-character value, and the probe's site and member counts did not move
      (66 / 23 before and after).
- [x] 2.4 REPORT THE FIFTH OUTCOME. `PinClassReport` gains the legal-non-pin
      collection and the undeclared-value collection; `clean` consults the second
      and NOT the first; `summary()` states both counts so a reader sees the split
      in one line. **A legal non-pin must not hold `fully_verified` open.**
      **DONE 2026-08-27.** `PinClassReport.non_pins` carries the classified
      results and splits into `legal_non_pins` / `undeclared_values`; `clean`
      consults `undeclared_values`, `uncovered_non_pins` and
      `declaration_defects` and NOT `legal_non_pins` or `absent_keys`, so an
      artifact carrying an honest sentinel is conforming and holds nothing open.
      `summary()` states all four counts on its one line and `render()` gives
      each its own marker. `ideation_readiness.verify_pin_reachability` now
      fails on `not report.clean` rather than on the four defect collections it
      hard-coded, so the new defect actually reddens the probe instead of being
      reported and ignored; its headline says in its own words that a DECLARED
      sentinel is not among the things it is failing on.
- [x] 2.5 CHECK THE DECLARATION IN BOTH DIRECTIONS, over the pin class's own
      inventory and its declared exclusions: a corpus spelling the vocabulary
      lacks is reported, and a declared member nothing carries is reported as
      unused. Reporting a stale member is not deleting it.
      **DONE 2026-08-27.** Corpus-against-declaration is `undeclared_values`;
      declaration-against-corpus is `unused_sentinels()`, which reports a member
      no committed artifact carries AND no declared generator emits — the
      delta's own wording, and the clause that keeps the report from reading as
      an instruction to delete a member whose generator has not landed. It is
      ADVISORY and does not hold the class open, for the same reason
      `presence=FUTURE` exempts a pin member: three of the five spellings have
      no committed instance today and reddening on that would have made the
      declaration impossible to land. `emitters` is MEASURED rather than
      believed — `test_the_declared_emitters_are_measured_rather_than_believed`
      opens each declared location and requires it to still reach for the value
      by the literal or by the module's own constant — so a phantom emitter
      cannot keep a stale member alive. Both directions run over the pin class's
      own inventory: same roots, same suffixes, same `NON_MEMBERS`.
- [x] 2.6 FIX `git_generation()`. On a dirty tree — measured with
      `status --porcelain` or `diff --quiet`, decided at realization — emit the
      declared sentinel rather than `HEAD`. **On a clean tree the behaviour is
      byte-identical to today**, and a test must pin that direction as hard as the
      dirty one. The three sites that already do this right are the reference:
      `ideation_dashboard/record_binding.py:202-210`,
      `intent_apply_lane.py:560`, `register_edit_lane.py:223`.
      **DONE 2026-08-27, WITH BOTH OPEN CHOICES DECIDED ON EVIDENCE.**
      *`status --porcelain`, not `diff --quiet`*: `diff` cannot see an UNTRACKED
      file, and a brand-new brainstorm document is read by `collect()`, changes
      the index, and is held by no commit — the dirty condition in its purest
      form (`test_git_generation_sees_an_untracked_corpus_document`).
      *SCOPED to the corpus, not the whole tree*: two of the three reference
      sites are path-scoped, and a whole-tree check would emit a sentinel while
      the corpus was perfectly committed and some unrelated file was open in an
      editor — throwing away a true pin, which the delta forbids in as many
      words. `CORPUS_PATHSPECS` spells `collect()`'s own two globs, and `:(glob)`
      magic is load-bearing: git's default pathspec `*` crosses `/`, so without
      it a dirty file under `ideation/brainstorm/inbox/` — which `collect()` does
      NOT read — would discard the pin
      (`test_git_generation_ignores_a_file_the_derivation_never_reads`). The
      scope is `source_revision`'s referent read literally: it claims the
      CORPUS, and `generator_version` beside it already claims the generator.
      The clean direction is pinned as hard as the dirty one — same `rev-parse
      HEAD`, same key, same three keys out
      (`test_git_generation_writes_the_real_pin_on_a_clean_corpus`).
      **THE UNREADABLE-REPOSITORY BRANCH IS NOT ADDED HERE**, honestly and
      deliberately: `check=True` still raises if git fails, which writes no
      false pin and is therefore not the defect this task repairs. § 5.1's rule
      binds it; this task's one instance is the dirty branch.
- [x] 2.7 RECONCILE THE `proposal-support.py` GUARDS against the declaration
      rather than the literal `"uncommitted"`. **RULED IN SCOPE 2026-08-27 (Q4)**,
      so the conditional is gone: all three comparisons (`:184`, `:632`, `:737`)
      consult the vocabulary, and the latent `SupportError` raise measured at
      § 1.7 closes with them. Q1 sharpens rather than complicates this — the guards
      are not learning a synonym, they are learning that the condition they test
      for has more than one member.
      **DONE 2026-08-27, AND THE CRASH IS CLOSED AT THE MEASUREMENT.** All three
      call `is_declared_sentinel(revision)`. Before:
      `git_blob_sha256(root, "uncommitted-worktree", "README.md")` raised
      `SupportError: invalid repository revision`, as did `not-applicable-ad-hoc`,
      `unknown` and `composed`; only `"uncommitted"` answered None. After: all
      five answer None, the qualified `composed:<…>` form answers None, a real
      commit still resolves to its blob digest, and an undeclared value STILL
      raises — the repair widens the guards to the DECLARATION, not to anything
      that is not a commit
      (`test_the_guards_recognize_every_member_and_not_just_one_spelling`,
      `test_an_undeclared_revision_still_raises`). The vocabulary is IMPORTED
      rather than copied: `pin_sentinels` is a sibling under `scripts/` with no
      dependency outside the standard library, and the path insertion covers
      being loaded by `spec_from_file_location` as the tests do. That is the
      same conversion `bootstrap-ideation-cross-reference.py` already made, and
      it is why `manifest_rel`'s deliberate duplication is left alone rather
      than treated as precedent.
      **`repo_revision()` IS DELIBERATELY NOT GIVEN A DIRTY-TREE BRANCH, and the
      reason is a measurement rather than a scope quibble — FLAGGED FOR REVIEW.**
      The instruction that reached this session read "dirty tree ->
      uncommitted-worktree" for this function too. It is not written, because
      this mover has no untrue pin to repair: it stamps `HEAD`, and then
      `move()` compares EVERY source file's sha256 against the committed blob at
      that revision and RAISES `staging source is not committed at source
      revision` rather than writing a manifest whose pin the content
      contradicts. It already satisfies the generator obligation, by refusing.
      Adding the branch would convert that refusal into a recorded sentinel —
      loosening a live safety guard, and permitting a transition of uncommitted
      sources that nothing in the packet or the rulings asks for. So the
      spelling `repo_revision` writes keeps meaning exactly what Q1 ruled it
      means: returned on a NON-ZERO EXIT from `rev-parse HEAD` and on nothing
      else, which is the unreadable-repository condition
      (`test_repo_revision_still_means_the_unreadable_repository`). If the
      loosening IS wanted, it is a behaviour change owed its own decision.
- [x] 2.8 REGRESSIONS under `tests/doc-health/`, covering at minimum: dirty tree
      yields a sentinel and not `HEAD`; clean tree yields the real pin unchanged;
      a declared sentinel reports as a legal non-pin and does not hold
      `fully_verified` open; an undeclared non-commit value reports as a defect
      naming artifact, key and value; a near-miss spelling is NOT matched to the
      nearest declared member; a declared member nothing carries reports as
      unused; and the real repository's seven sentinel sites all classify as legal
      non-pins. **PLUS the three the 2026-08-27 rulings added**: two spellings
      naming two conditions are both members and neither is marked legacy (Q1); an
      artifact with no pin key reports as a recognized legacy absence and is
      neither a member nor filled in (Q2); and the defect branch reports nothing
      against the snapshot registry's and the avatar F0 lane's existing committed
      output, which is the seeding obligation Q3's ruling turned into a
      requirement. **The existing 53 tests in `test_pin_reachability.py` must stay
      green unchanged** — none of them asserts anything about a non-commit value
      today, which is itself the coverage gap.
      **DONE 2026-08-27** — `tests/doc-health/test_sentinel_vocabulary.py`, 33
      tests, every one pinned to a measured defect and none to a fix. All ten
      required cases are covered, plus the two the widening itself created (a
      key name quoted in prose or in a comment is not a site; a sentinel under
      an uncovered key is TWO findings rather than one masking the other) and
      the guard repair's own pair. **The 53 tests in `test_pin_reachability.py`
      are green and UNCHANGED — not one line of that file is edited.**
- [x] 2.9 NO DETERMINISTIC CHECK FAMILY. The test that pins `pin_class` out of the
      family registry stays green, and the family enumeration and its numerals are
      not touched.
      **HELD 2026-08-27.** `FAMILY_IDS` and `families.FAMILIES` are byte-
      unchanged; `pin_sentinels` defines no `fam_*` and is not reachable from
      `families.py`; the existing exclusion test is green
      (`test_no_deterministic_check_family_is_added` asserts the same three-way
      shape for the new module).

## 3. The existing sentinel inventory — seven values, ten non-pin manifests

- [x] 3.1 THE SIX `"uncommitted-worktree"` SITES, all archived, all inside the
      declared `proposal-support-manifest` member's globs, all invisible today:
      `2026-07-13-align-avatar-first-ui-standard/supporting-docs/manifest.yaml:14`,
      `2026-07-13-define-avatar-client-contract-kernel/supporting-docs/manifest.yaml:64`,
      `2026-07-13-implement-avatar-reference-runtime/supporting-docs/manifest.yaml:14`,
      `2026-07-14-add-document-cataloging/supporting-docs/manifest.yaml:29`,
      `2026-08-06-add-cross-factory-ideation-routing/supporting-docs.manifest.yaml:34`,
      `2026-08-09-qualify-avatar-brokered-call-feasibility/supporting-docs.manifest.yaml:39`.
      **Declared, never edited.**
      **CONFIRMED 2026-08-27**: all six classify as legal non-pins for the
      dirty-worktree condition, at the same six paths and line numbers, and not
      one manifest byte is edited — `git diff` touches no file under
      `openspec/changes/archive/`.
- [x] 3.2 THE ONE `"not-applicable-ad-hoc"` SITE:
      `2026-07-10-add-xfactory-installer-repository/supporting-docs.manifest.yaml:22`.
      Archived. **Declared, never edited.** **CONFIRMED 2026-08-27**: classifies
      as a legal non-pin for the outside-repository condition. Its member is the
      one declared with NO emitter — nothing in the tooling can produce it — and
      that is recorded on the member rather than smoothed over.
- [x] 3.3 THE THREE MANIFESTS WITH NO `source_revision` AT ALL:
      `2026-07-29-add-crystallizer-contracts`, `2026-07-29-add-pattern-ledger`,
      `2026-07-30-add-capability-steward`. All archived, all visibly truncated
      stubs — `add-pattern-ledger` carries only `change_id` and `files`. **An
      absent key is a fourth state and this packet does not convert it.**
      **RULED 2026-08-27 (Q2), as recommended**: absence is declared a RECOGNIZED
      LEGACY STATE — visible, reported once, repaired never — and is NOT a
      vocabulary member. None of the three is filled in with a sentinel.
      **CONFIRMED 2026-08-27**: the probe reports exactly three recognized legacy
      absences, at exactly those three paths, all under
      `proposal-support-manifest`, none filled in, and none holding `clean` or
      `fully_verified` open — there is nothing for a red to ask for when the
      repair is `never`. **A FOURTH SHAPE WAS MEASURED AND DECLARED OUT rather
      than reported as noise**: `specs/*/traceability.yaml` also has two files
      without the key, and there the key is NOT expected — 008 carries
      `source_revision` inside an optional per-feature verification block that
      007 and 009 do not have at all, and no schema requires it. So
      `spec-traceability` declares `key_expected=False` with that measurement
      written beside it, and absence there is the artifact's normal shape rather
      than a legacy state of the corpus. That the remaining three are EXACTLY
      the three this task names is the corroboration.
- [x] 3.4 THE TWO SPELLINGS NO GOVERNANCE DOCUMENT MENTIONS — `"unknown"` and
      `"composed"` — are inventoried here rather than left to the realization to
      discover. **RULED 2026-08-27 (Q3): BOTH JOIN the declared vocabulary**, and
      the reason the ruling gave is a constraint on § 2.3 rather than a
      preference — left out, the undeclared-value-is-a-defect branch would flag
      the snapshot registry's own committed output the day it was switched on.
      The seeding obligation now stated in the `doc-health` classification
      requirement is what generalizes that.
      **BOTH JOINED 2026-08-27**, and the seeding obligation was discharged more
      widely than the two: the widened sweep over the whole corpus found FOUR
      distinct non-commit spellings, not two. `"uncommitted-worktree"` (6) and
      `"not-applicable-ad-hoc"` (1) are declared members already carried; the
      other two — a template placeholder and a JSON-Schema type declaration —
      name no condition and have no generator, and are resolved by declared
      exclusions with stated reasons (see § 2.3). `"unknown"` and `"composed"`
      are declared but carried by NOTHING in committed state; they join on their
      emitters' behalf, which is exactly the case Q3's reasoning describes, and
      the qualified `composed:<…>` form joins with them because that is what the
      lane actually writes.
- [x] 3.5 AFTER REALIZATION, RE-RUN THE PROBE AND RECORD THE SPLIT. The expected
      shape is the same site and member counts with the sentinel sites moved from
      invisible to legal non-pins, `0 uncovered` unchanged, and the class still
      fully verified — because every one of them is conforming.
      **RE-RUN 2026-08-27 at 45ba637a, AND THE EXPECTED SHAPE HELD EXACTLY.**
      BEFORE: `66 declared pin sites across 23 class members: 50 reachable, 0
      orphaned, 1 lost (declared unrecoverable, 0 awaiting a superseding
      record), 0 inconclusive; 0 uncovered site(s), 0 vanished member(s), 0
      future member(s) now carrying pins` — `clean=True fully_verified=True`.
      AFTER: every one of those numbers unchanged, plus `7 legal non-pin(s), 0
      undeclared non-commit value(s), 3 recognized legacy absence(s), 0 unused
      vocabulary member(s)` — `clean=True fully_verified=True`. The seven sites
      moved from INVISIBLE to legal non-pins and nothing that was reachable
      changed class.

## 4. Archive gate

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate declare-sentinel-pin-vocabulary
      --strict` and `--all --strict` green on the merged tree.
      **GREEN ON THE REALIZATION BRANCH 2026-08-27**: `Change
      'declare-sentinel-pin-vocabulary' is valid`, and `--all --strict` totals
      `76 passed, 0 failed (76 items)`. Left unticked because this arm asks for
      green ON THE MERGED TREE, which is not this session's to produce.
- [ ] 4.2 `python3 -m pytest tests/doc-health -q` green under `set -o pipefail`,
      with the count read out of the run rather than off a summary, and compared
      against the 1209 measured at filing plus whatever main has grown.
      **MEASURED ON THE REALIZATION BRANCH 2026-08-27**: baseline at
      `origin/main` 45ba637a was **1215 passed** (main grew six since the 1209
      at filing); after realization **1248 passed** — the same 1215 plus the 33
      new tests, none removed and none edited. Read out of the run under
      `set -o pipefail` with the exit code unmasked. Unticked for the same
      reason as § 4.1: the merged tree is where this arm closes.
- [ ] 4.3 The declared class reporting its sentinel sites as legal non-pins, the
      vocabulary check green in both directions, and `fully_verified` unchanged.
      **MEASURED 2026-08-27**, recorded in full at § 3.5: seven legal non-pins,
      zero undeclared values, zero unused members, zero declaration defects, and
      `fully_verified` True before and after. Unticked pending the merged tree.
- [x] 4.4 NO CONTRACT BUNDLE IS OWED, re-affirmed rather than re-assumed at the
      archive: no edited file is a member of any `contracts/releases/*.digests.yaml`
      inventory, and the act's own doc-health run reports `release-inventory-drift`
      at 0 findings before and after.
      **RE-AFFIRMED BY PARSE, NOT BY GREP, 2026-08-27.** All 40
      `contracts/releases/*.digests.yaml` inventories were loaded and walked for
      member paths — 192 distinct paths — and NONE of the seven files this
      realization touches appears in any of them. The check is not vacuous:
      `scripts/` files ARE bundle members (the `hermes_runtime_validation`
      package among them) and a `tests/` path is too, so a cut would have been
      owed had one of these been listed. `python3 scripts/doc-health.py
      --single-repo . --family release-inventory-drift` reports `0 critical, 0
      error, 0 warning, 0 info` with the change applied AND with it stashed.
- [x] 4.5 The five § Orchestrator decisions cleared or vetoed, and the four
      § Open Questions ruled, with approver, date and mechanism recorded whether
      or not verbatim wording reaches the session. **DISCHARGED 2026-08-27** —
      all five cleared as authored, all four ruled, recorded at § 1.12 and in
      `proposal.md` § Orchestrator decisions and § Open Questions. **This is the
      one arm of the gate a filing session can close**; the rest wait on
      realization.
- [ ] 4.6 Merged plus green on main, with the merge read out of git — parents and
      `merge-base --is-ancestor` — rather than off the pull request page.

## 5. Named follow-ups, out of scope and deliberately not written

- [ ] 5.1 **THE OTHER GENERATORS ARE BOUND BY THE RULE AND NOT REPAIRED BY THIS
      PACKET.** `_head_sha()` (`ideation_dashboard/nightly_lane.py:117`),
      `git_head_revision()` (`dashboard_refresh_lane.py:643`) and above all
      `RealGit.head_sha()` (`doc_health/corpus.py:534`) all run `rev-parse HEAD`
      with no cleanliness check. `corpus.py`'s seam is the widest-fanout pin source
      in the repository — readiness, possibles, organizer, neutrality, inventory
      and family lanes all draw from it — so a cleanliness check there changes six
      record families at once. That is a sweep with its own evidence; this packet
      states the rule it would be measured against and performs one instance.
- [ ] 5.2 **CROSS-REPOSITORY PINS STAY OUT**, exactly as
      `govern-derived-pin-reachability` § 5.2 left them. Whether a sentinel is even
      meaningful for a gitlink, a `pinned_contract_manifest` entry, a release
      digest or an image digest is a different question, answered against a
      different remote by a different authority.
- [ ] 5.3 **`"composed"` MAY NOT BELONG IN A PIN KEY AT ALL.** A composed view
      genuinely has no single source revision, which is a different fact from "I
      could not read one". Q3 recommends declaring it as a member; if that is
      wrong, the honest answer is a different KEY on the snapshot index, which is
      a schema change this packet does not make.
- [ ] 5.4 **THE PREFLIGHT HALF OF THE ENFORCEMENT HOME STAYS UNWIRED**, for the
      three reasons `govern-derived-pin-reachability` § 5.6 measured, none of which
      this packet changes. The classification rides inside a verification that is
      already pytest-plus-entry-point rather than nightly-gated.
- [ ] 5.5 **THE `_field_re` / `_VOCAB_RE` TRAILING-BOUNDARY GAP, FOUND WHILE
      MEASURING AND NOT FIXED HERE.** Both regexes have a leading key boundary and
      no trailing hex boundary, so a 64-hex sha256 under a vocabulary key yields a
      bogus 40-character "pin" — the exact hazard `LOOSE_SHA_RE`'s own comment
      guards against, never carried into the two regexes that actually build
      sites. Latent today: no vocabulary key holds a sha256 value in a swept root,
      and the real-repository coverage test is green. Adjacent to this packet's
      subject (both are about what the value regex accepts) but a different defect,
      and folding a silent mis-parse fix into a vocabulary packet would hide it.
      Recorded so the next reader does not have to rediscover it.
      **STILL OPEN AFTER REALIZATION, AND THE NEW CODE DOES NOT TOUCH IT.**
      `_field_re` and `_VOCAB_RE` are byte-unchanged, so the bogus 40-character
      pin is exactly as latent as it was. One interaction is worth writing down
      rather than leaving to be discovered: the WIDE regexes extract the whole
      scalar, so a 64-hex sha256 under a vocabulary key would be reported by the
      classification as an undeclared non-commit value AT THE SAME TIME as the
      pin path made its bogus pin. Inert today — no vocabulary key holds a
      sha256 in a swept root, re-measured at 45ba637a — and it is not a fix.
- [ ] 5.6 **RECORDED AT REALIZATION 2026-08-27, NOT AT FILING: THE THREE
      `"unknown"` CALL SITES SHOULD BE SPLIT ONTO THE CONDITIONS THEY MEAN.**
      Deciding the point § 2.2 carried required measuring them, and the
      measurement found one spelling doing three jobs:
      `snapshot_registry.index_entry` (an index entry with no recorded
      revision), `avatar_f0.cli._git_head` (an unreadable `HEAD`, which is
      `"uncommitted"`'s condition exactly) and `avatar_f0.cli._git_file_commit`
      (a readable repository whose named content has never been committed,
      closest to the dirty-tree condition). The vocabulary absorbs the spelling
      as it stands — declared for the weakest condition, the only one true of
      all three — but a generator that CAN distinguish should write the stronger
      member, and these three can. That is a change to two lanes' output in
      three places, each owing its own evidence, and § 5.1's rule binds it
      exactly as it binds the other unrepaired generators. NOT DONE HERE, and
      the declaration says so in its own note rather than implying the spelling
      is precise.
