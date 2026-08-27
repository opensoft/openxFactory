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
- [ ] 1.12 THE VETO WINDOW IS OPEN. Five § Orchestrator decisions stay FLAGGED and
      four § Open Questions stay UNRULED. Nothing in this packet may be realized
      on the assumption that OD-2 (the vocabulary's home), OD-3 (grandfathering)
      or Q1 (which spelling is canonical) resolved the way the packet recommends.

## 2. Implementation — unstarted

- [ ] 2.1 SETTLE Q1 FIRST. Which spelling is canonical for the dirty-tree
      condition determines what `git_generation()` writes, what the vocabulary
      declares as legacy, and whether the `proposal-support.py` guards change. No
      code before that ruling.
- [ ] 2.2 DECLARE THE VOCABULARY beside `scripts/doc_health/pin_class.py`, in the
      registry-module form Q1 of `govern-derived-pin-reachability` ruled for the
      class itself. Every member states its condition and whether it is canonical
      for new output or a legacy spelling retained for committed state.
- [ ] 2.3 CLASSIFY THE VALUE in `pin_class.py`. A non-commit value under a
      declared pin key becomes a site with one of two outcomes — legal non-pin
      (declared) or defect (undeclared) — rather than no site at all. The
      commit-shaped path is untouched: same regexes for pins, same ref set, same
      verdicts.
- [ ] 2.4 REPORT THE FIFTH OUTCOME. `PinClassReport` gains the legal-non-pin
      collection and the undeclared-value collection; `clean` consults the second
      and NOT the first; `summary()` states both counts so a reader sees the split
      in one line. **A legal non-pin must not hold `fully_verified` open.**
- [ ] 2.5 CHECK THE DECLARATION IN BOTH DIRECTIONS, over the pin class's own
      inventory and its declared exclusions: a corpus spelling the vocabulary
      lacks is reported, and a declared member nothing carries is reported as
      unused. Reporting a stale member is not deleting it.
- [ ] 2.6 FIX `git_generation()`. On a dirty tree — measured with
      `status --porcelain` or `diff --quiet`, decided at realization — emit the
      declared sentinel rather than `HEAD`. **On a clean tree the behaviour is
      byte-identical to today**, and a test must pin that direction as hard as the
      dirty one. The three sites that already do this right are the reference:
      `ideation_dashboard/record_binding.py:202-210`,
      `intent_apply_lane.py:560`, `register_edit_lane.py:223`.
- [ ] 2.7 RECONCILE THE `proposal-support.py` GUARDS against the declaration
      rather than the literal `"uncommitted"` — IF Q4 rules that the repair rides
      this packet. If it does not, the latent raise is carried to § 5 unticked
      rather than left unrecorded.
- [ ] 2.8 REGRESSIONS under `tests/doc-health/`, covering at minimum: dirty tree
      yields a sentinel and not `HEAD`; clean tree yields the real pin unchanged;
      a declared sentinel reports as a legal non-pin and does not hold
      `fully_verified` open; an undeclared non-commit value reports as a defect
      naming artifact, key and value; a near-miss spelling is NOT matched to the
      nearest declared member; a declared member nothing carries reports as
      unused; and the real repository's seven sentinel sites all classify as legal
      non-pins. **The existing 53 tests in `test_pin_reachability.py` must stay
      green unchanged** — none of them asserts anything about a non-commit value
      today, which is itself the coverage gap.
- [ ] 2.9 NO DETERMINISTIC CHECK FAMILY. The test that pins `pin_class` out of the
      family registry stays green, and the family enumeration and its numerals are
      not touched.

## 3. The existing sentinel inventory — seven values, ten non-pin manifests

- [ ] 3.1 THE SIX `"uncommitted-worktree"` SITES, all archived, all inside the
      declared `proposal-support-manifest` member's globs, all invisible today:
      `2026-07-13-align-avatar-first-ui-standard/supporting-docs/manifest.yaml:14`,
      `2026-07-13-define-avatar-client-contract-kernel/supporting-docs/manifest.yaml:64`,
      `2026-07-13-implement-avatar-reference-runtime/supporting-docs/manifest.yaml:14`,
      `2026-07-14-add-document-cataloging/supporting-docs/manifest.yaml:29`,
      `2026-08-06-add-cross-factory-ideation-routing/supporting-docs.manifest.yaml:34`,
      `2026-08-09-qualify-avatar-brokered-call-feasibility/supporting-docs.manifest.yaml:39`.
      **Declared, never edited.**
- [ ] 3.2 THE ONE `"not-applicable-ad-hoc"` SITE:
      `2026-07-10-add-xfactory-installer-repository/supporting-docs.manifest.yaml:22`.
      Archived. **Declared, never edited.**
- [ ] 3.3 THE THREE MANIFESTS WITH NO `source_revision` AT ALL:
      `2026-07-29-add-crystallizer-contracts`, `2026-07-29-add-pattern-ledger`,
      `2026-07-30-add-capability-steward`. All archived, all visibly truncated
      stubs — `add-pattern-ledger` carries only `change_id` and `files`. **An
      absent key is a fourth state and this packet does not convert it**; Q2.
- [ ] 3.4 THE TWO SPELLINGS NO GOVERNANCE DOCUMENT MENTIONS — `"unknown"` and
      `"composed"` — are inventoried here rather than left to the realization to
      discover. Q3.
- [ ] 3.5 AFTER REALIZATION, RE-RUN THE PROBE AND RECORD THE SPLIT. The expected
      shape is the same site and member counts with the sentinel sites moved from
      invisible to legal non-pins, `0 uncovered` unchanged, and the class still
      fully verified — because every one of them is conforming.

## 4. Archive gate

- [ ] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate declare-sentinel-pin-vocabulary
      --strict` and `--all --strict` green on the merged tree.
- [ ] 4.2 `python3 -m pytest tests/doc-health -q` green under `set -o pipefail`,
      with the count read out of the run rather than off a summary, and compared
      against the 1209 measured at filing plus whatever main has grown.
- [ ] 4.3 The declared class reporting its sentinel sites as legal non-pins, the
      vocabulary check green in both directions, and `fully_verified` unchanged.
- [ ] 4.4 NO CONTRACT BUNDLE IS OWED, re-affirmed rather than re-assumed at the
      archive: no edited file is a member of any `contracts/releases/*.digests.yaml`
      inventory, and the act's own doc-health run reports `release-inventory-drift`
      at 0 findings before and after.
- [ ] 4.5 The five § Orchestrator decisions cleared or vetoed, and the four
      § Open Questions ruled, with approver, date and mechanism recorded whether
      or not verbatim wording reaches the session.
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
