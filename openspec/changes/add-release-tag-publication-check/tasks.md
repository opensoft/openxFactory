# Tasks: add-release-tag-publication-check

Status: draft

Nothing below group 3 has been done. Group 2 is the realization plan and every
box in it is open; group 3 records what the authoring session measured before
the packet was put up, which is evidence rather than implementation.

Build with Speckit, not `/opsx:apply`. OpenSpec ratifies; Spec Kit builds. This
change is ONE Spec Kit feature — group 2 — because the new module, its
registration, the enumeration sites it moves and the tests that hold it are a
single vertical slice, and splitting them would produce two features neither of
which is green alone: a registered family whose count sites have not moved
reddens `family-enumeration` on its own landing, which is group 2.3's whole
point. Group 5 is the archive act, last, and open until the merge it follows
exists.

## 1. Ratification

- [ ] 1.1 Brett rules the packet. The commissioning ("take 528") authorized
      BUILDING A CHECK and nothing else; five design decisions are flagged for
      veto in the proposal's § Orchestrator Decisions and are NOT covered.
- [ ] 1.2 **D3's threshold N is a governance number and needs a ruling.** The
      packet proposes FIVE first-parent landings only so the scenarios have
      something concrete to say. Calibration evidence: `contract-v2.3` sat
      untagged across six first-parent landings before a human noticed; the
      August three sat for weeks. A number is owed before group 2.2 can write
      the threshold.
- [ ] 1.3 **D2 is the shape veto.** If Brett prefers a finding class inside
      `Release-inventory drift` to a twenty-third family, the delta changes
      shape: the ADDED requirement folds into that requirement as a MODIFIED
      block with all eight of ITS scenarios restated and its resolution
      sentence amended, and groups 2.3 and 2.4 disappear. Cheaper, and it
      couples two different resolution acts in one family — the proposal argues
      against it and does not pretend the argument is free.

## 2. Realization — ONE Spec Kit feature

- [ ] 2.1 `scripts/doc_health/release_tag_publication.py` — the module: its own
      severity and action constants, a pure function answering the question from
      a declared bundle plus the repository's tag refs, and
      `fam_release_tag_publication(ctx)`. Follows `release_inventory.py` and
      `family_enumeration.py` in owning its own module rather than growing
      `families.py`.
- [ ] 2.2 The distance grading and its threshold, once 1.2 rules N. Distance is
      FIRST-PARENT COMMITS ON PUBLISHED `main` since the earliest declaring
      commit — never wall time, which punishes a quiet week.
- [ ] 2.3 **Registration and the count ripple, IN THE SAME COMMIT.**
      `scripts/doc_health/__init__.py` (the registered set),
      `scripts/doc_health/families.py` (dispatch, and `FAMILY_SUMMARIES` /
      `FAMILY_RESOLUTION` if the family carries a summary line and a resolution
      class), and every site stating the count: `docs/doc-health.md:28`
      ("twenty-two families"), `scripts/doc_health/modified_block_currency.py:1634`,
      `scripts/doc_health/report.py:300`, `tests/doc-health/test_suite.py:767`,
      `tests/doc-health/test_modified_block_currency_reporting.py:777`,
      `tests/doc-health/test_modified_block_currency_self_gate.py:26` and `:93`.
      Split across two commits and `family-enumeration` reddens on the first.
- [ ] 2.4 The promoted requirement's numerals are moved by the MODIFIED block in
      this packet's delta, so 2.3's code registry and canon agree at the landing
      rather than one lagging.
- [ ] 2.5 `tests/doc-health/test_release_tag_publication.py` — the ten scenarios
      of the delta as behavioural tests over fixture repositories carrying REAL
      annotated tags, real lightweight refs and a real misplaced tag. A fixture
      that fakes a tag as a string in a manifest tests nothing this family does.
- [ ] 2.6 A self-gate probe over this repository, in the pattern the other
      self-gating families use, with its positive control: the probe must be
      shown to FIRE on a constructed absence, not merely to read zero.
- [ ] 2.7 `docs/doc-health.md` — the family's row and its action line, pinned
      verbatim in this family's own suite per the action-line pin convention
      landed by #448.
- [ ] 2.8 `python3 -m pytest tests/doc-health` green;
      `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.

## 3. Evidence measured before the packet went up

- [x] 3.1 The obligation's exact wording read from
      `docs/contract-versioning-policy.md`: "a bundle is not published until its
      tag exists"; "the tag SHALL point to that realized commit"; and the clause
      forbidding any lapse being read as an exception.
- [x] 3.2 **No enforcement anywhere**, measured four ways: no workflow calls the
      release validator; `verify_tag` is exercised only by unit tests over
      synthetic repositories; `release-surface-integrity` deliberately does not
      anchor on tags; `tag-hygiene` is `document-lifecycle`'s prose-tag grammar
      over document text.
- [x] 3.3 The recurrence: `contract-v1.33`/`v1.35`/`v1.39` discharged only on
      Brett's ruling of 2026-08-25; `contract-v2.3` and `contract-v2.4` found by
      hand on 2026-08-31.
- [x] 3.4 The #526 cut wrote a `contract-v2.3` disposition subsection and said
      nothing about its own tag — the observation that makes the gap structural
      rather than careless. Repaired by hand in #532.
- [x] 3.5 The retro-publication rule reproduces a live control: it returns
      `8ccfb67b` for `contract-v2.2`, and that bundle's published tag peels to
      exactly that commit.
- [x] 3.6 The day-one prediction: ZERO findings. 46 published tags against 53
      changelog entries, the seven absences all in the `contract-v1.0`–`v1.6`
      legacy sequence, and `contract-v2.5` — the current declared bundle — tagged.
- [x] 3.7 The enumeration ripple's sites located and listed at 2.3, and the
      promoted requirement measured as scenario-complete at eight scenarios
      before restating it.

## 4. Recorded, not fixed

- [ ] 4.1 **#338 stands and this packet routes around it** (D5). `verify_tag`
      cannot distinguish "not fetched" from "unreachable from `main`"; observed
      live, it fails identically on `contract-v2.2`, whose tag is correct. If
      #338 lands first, D5 is worth revisiting — reusing the canonical verifier
      is otherwise the better shape than a second peel-and-compare.
- [ ] 4.2 **This family does not prove the target is the EARLIEST declaring
      commit** (D4). A tag on a later declaring commit passes it and remains a
      defect under the policy. Disclosed in the requirement's own text rather
      than left for a reader to discover.
- [ ] 4.3 The policy's standing sentence — "Every bundle from `contract-v1.7` …
      is now tagged" — is true again today and has been false twice. This family
      does not check that sentence, and nothing does; whether canon should
      carry a claim no check defends is a question this packet raises and does
      not answer.

## 5. Archive

- [ ] 5.1 Archive on merge-plus-green, following `add-family-enumeration-check`
      and `add-unclassified-finding-class`: no contract bundle is cut by this
      surface, so no tag is owed BY the change that checks tags.
