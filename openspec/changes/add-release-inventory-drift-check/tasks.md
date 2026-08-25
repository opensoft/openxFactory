# Tasks — add-release-inventory-drift-check

**RATIFIED 2026-08-24. The CHECKER is a follow-on realization slice and is not
built here.** This packet carries the scouting (§1), the four rulings and the
versioning-policy ratification that landed with them (§2, §4), and the
implementation plan the follow-on slice executes (§3, §5).

## 1. Scouting and route adjudication — DONE

- [x] 1.1 The route is adjudicated from the record: an OpenSpec change IS
      required. The promoted `doc-health` spec ENUMERATES its families by name
      and by count, the package's own docstring says "Changes to WHAT the
      checks are happen through the contract; this package follows", the
      promoted corpus-membership requirement installs a governed-change
      obligation on exactly this act, and both fresh precedents
      (`govern-openspec-corpus-membership` 16→17,
      `add-promotion-fidelity-check` 17→18) took this route for it.
- [x] 1.2 The obligation is separated from the checker, in that order —
      `release-realization` states what must be true, `doc-health` states only
      how it is checked. This follows `add-promotion-fidelity-check` 1.2: "a
      checker with no promoted rule behind it is a rule invented in Python".
- [x] 1.3 Today's drift is measured, not assumed: 190 members, 188 matching,
      2 editorial (`CHANGELOG.md`, `manifest.yaml`), **0 non-editorial**, 0
      missing. Today's main is a bounded expected state and the family would
      launch GREEN on the error band.
- [x] 1.4 The `contract-v1.36` class is proven detectable at the commit: the
      same comparison at `08c5aa9` reports one non-editorial drift,
      `contracts/schemas/gate-action-record.schema.yaml`. The "forgot to bump
      the bundle" case needs no tag access and no separate rule.
- [x] 1.5 The coverage boundary is established and written into the proposal:
      inventory membership is scoped to the release surface a release touched,
      so two schemas that changed after the tag are non-members and invisible
      to this family — and are covered instead by the manifest's 150 per-file
      digests, which verify every session and currently match.
- [x] 1.6 Feasibility is precedented: doc-health families already read git
      through the injected `ctx.git` façade (`proposal_origin`, and
      `add-promotion-fidelity-check`'s new `first_commit_timestamp` reader),
      with the house rules — never `subprocess` from a family module, always a
      `RealGit` method, always degrade to `None`, always a deterministic
      fallback or an honest skip.
- [x] 1.7 The `contested` trap is identified before it is walked into: both
      findings are resolved by a release cut, and a `contested` finding that
      vanishes uncited is re-emitted as an `error`, so the family must stay out
      of `FAMILY_RESOLUTION`.

## 2. Ratification — DONE (Brett, 2026-08-24)

- [x] 2.1 OQ-1 RULED: a NEW CAPABILITY, `release-surface-integrity`, overriding
      the drafting session's `release-realization` recommendation. The delta is
      restructured onto it; the promoted spec directory is created at archive.
- [x] 2.2 OQ-2 RULED: `info` for editorial drift, not `warning`.
- [x] 2.3 OQ-3 RULED: `contracts/README.md` IS in the editorial set.
- [x] 2.4 OQ-4 RULED: `docs/contract-versioning-policy.md` is ratified BY THIS
      CHANGE, and the read-through it required found four defects — see §4.
- [x] 2.5 The change is ratified. The checker is a follow-on realization slice.

## 3. Implementation — DONE

- [x] 3.1 `scripts/doc_health/corpus.py` — TWO new `RealGit` readers, not one:
      `blobs_at` (raw bytes, one `cat-file --batch` for the whole member set)
      and `tree_modes` (one `ls-tree -r`). The second was not in the plan and is
      required by the tightened delta's `git_mode` clause. Both degrade to
      `None` only on a git failure; per-path ABSENCE is data, which is the
      distinction the taxonomy turns on.
- [x] 3.2 `scripts/doc_health/release_inventory.py` — the family.
- [x] 3.3 Registered in `families.FAMILIES` and `__init__.FAMILY_IDS`, and
      DELIBERATELY NOT in `FAMILY_RESOLUTION`, with the structural reason at
      the registration site.
- [x] 3.4 `tests/doc-health/conftest.py` — the `FakeGit` shim for both readers,
      including `git_unavailable=True` as the only way to reach the skip arm.
- [x] 3.5 NOT IN THE PLAN, required by an exhaustive registry:
      `tests/doc-health/test_lifecycle_scan_set.py` classifies every family as a
      lifecycle-scan reader or non-reader. The new family is a NON-READER
      (it reads contract artifact bytes, no lifecycle header at all), and the
      count literal follows the corpus: nineteen families, fifteen non-readers.

## 4. The versioning policy — DONE, landed with this change

- [x] 4.1 `docs/contract-versioning-policy.md` gains § "What a red
      `verify-commit` at HEAD means": editorial drift between cuts is expected,
      the reference is the inventory file rather than a tag, a mismatch on any
      other member is a defect, and the remedy is a release cut and NEVER a
      hand-edit of an inventory or of `contract_bundle_version` to make a check
      pass. Issue #312's option 2, landed.
- [x] 4.2 RATIFIED: `Status: draft` -> `ratified`, `Ratified by:` this change.
- [x] 4.3 CORRECTION — three bundles allocated after mandatory tagging began
      (`contract-v1.33`, `contract-v1.35`, `contract-v1.39`) carry a changelog
      entry and no published tag, which the policy's own rule forbids. Recorded
      as a named undischarged gap in a new subsection; the rule is NOT relaxed
      to accommodate it, and the disposition is left open because retro-tagging
      requires establishing which commit each bundle realized at.
- [x] 4.4 CORRECTION — the legacy-baseline paragraph claimed `contract-v1.6`
      IS the manifest baseline; it was, in 2026. Rewritten to past tense.
- [x] 4.5 CORRECTION — the deprecation entry called `customer/client/domain`
      the "canonical roles". They are FROZEN MACHINE KEYS; the canonical
      vocabulary has been Subject / Tenant / Domain since
      `adopt-subject-tenant-domain-vocabulary` (ratified 2026-07-23). Corrected
      and pointed at `contracts/policies/layer-vocabulary.yaml`.

## 5. Acceptance evidence, both directions — DONE (24 tests)

- [x] 5.1 True positive: the forgot-to-bump shape fires one `error` on the
      schema the cut changed. SYNTHESIZED rather than pointed at `08c5aa9`, per
      this task list's own instruction — a test depending on a real sha stops
      testing anything the day someone prunes or rewrites it.
- [x] 5.2 **SATISFIED, VIA A RELEASE CUT — and the route there is the record
      worth keeping.** The criterion was "`origin/main` produces `info` findings
      only and reddens no gate", measured 188/2/0/0 when the packet was drafted.
      By realization time main was 187/2/1/0: the family reported ONE `error`,
      on `docs/contract-versioning-policy.md`, because the single commit to
      touch that member since the `contract-v1.40` tag was `57c26e1a` — PR #319,
      **the change that commissioned this check**. The member is in the
      inventory because the membership clause covers "every modified normative
      contract **or versioning document**".
      A TRUE POSITIVE, proven both directions rather than argued: run at the
      `contract-v1.40` tag the family reported 0 errors and 0 info; run at main
      it named exactly the one member that had moved.
      Two remedies existed and ONE WAS REFUSED: reclassifying the policy into
      the editorial set would have been the "hand-edit to make the check pass"
      that the ratified policy forbids in writing. **Brett ruled 2026-08-25: cut
      a release.** Done as `contract-v1.41` (additive, no schema bytes), and the
      family now reports **0 error, 0 info** at branch HEAD — every one of the
      190 members re-baselined.
      The `#312` symptom resolves with it: `verify-commit --commit HEAD` PASSES
      for the first time since the v1.40 tag, while `origin/main` remains red on
      all three drifted members.
- [x] 5.3 The editorial split is load-bearing: both bands are driven at once and
      neither promotes nor demotes the other.
- [x] 5.4 The raw-bytes rule is pinned by a BYTE-DISTINGUISHING fixture, and
      the distinction matters: a non-ASCII member is NOT one. `é` encodes and
      decodes through a UTF-8 text-mode round trip to the identical bytes, so
      the obvious fixture would pass with the very reader the rule forbids
      (PR #319, Codex). The fixture SHALL be a committed blob containing CRLF
      line endings, because Python's universal-newline text mode rewrites
      `\r\n` to `\n` and therefore yields different bytes and a different
      digest than the blob holds. The test SHALL assert the raw reader
      DIRECTLY — that it returns the CRLF bytes — rather than only asserting
      that the family reports no drift, so the pin fails on a text-mode reader
      instead of merely happening to agree with one.
- [x] 5.5 Both skips are exercised, and ABSENCE IS TESTED AGAINST
      UNAVAILABILITY in one test, because their conflation is the defect the
      review tightening fixed.
- [x] 5.6 Suite counts: `tests/doc-health` 771 -> 795 (+24, all this family's).
      doc-health's own report moves by exactly the family's findings and no
      other line: 4/8/82/3 -> 4/9/82/5. The two `info` findings are NOT
      regressions — `report.regressions` filters to critical/error — so the
      only new regression is the one true positive 5.2 records.

## 6. Archive

- [ ] 6.1 Archive ONLY after merge with green realization evidence. This change
      ships ACTIVE, following both precedents. NOTE the extra item this change's
      realization carries: `contract-v1.41`'s annotated tag is cut AT THE SQUASH
      after landing, per the ratified realization order — the bundle is
      allocated and its inventory shipped in the cut commit, and CHANGELOG
      presence is the availability test, not tag presence.

## 7. Recorded, not fixed

- [x] 7.1 The `contract-v1.36` tag was moved, which
      `docs/contract-versioning-policy.md` § Immutable Tag Correction forbids
      outright ("never moved, deleted, or re-tagged, not even for a defective
      release"; the sanctioned correction is a superseding release).
      **DISPOSITION — RECORD ONLY (Brett, 2026-08-24).** The tag stays as it
      is: a second move would compound the breach, and a superseding release
      would spend a version number to correct provenance this record already
      carries accurately. No further action is owed, and a later session
      noticing the mismatch should read this line rather than act.
      **ALSO RECORDED IN THE POLICY ITSELF** — `docs/contract-versioning-policy.md`
      § "contract-v1.36 Was Moved", added because this packet archives out of
      the path of anyone running `verify-tag` and landing on the immutability
      rule (PR #319 review, P2-1). The packet record is kept as the reasoning;
      the policy subsection is the one a discoverer will actually hit.
- [x] 7.2 Two schemas changed after the v1.40 tag without a cut
      (`client-overlay.schema.yaml`, `openxwallet-grant.schema.yaml`). Both are
      tracked and currently matching in the manifest's per-file digests, so
      this is not a live integrity defect — but whether a normative schema may
      change between cuts at all is a policy question this packet does not
      answer. Recorded; no action taken here.

- [x] 7.3 A drafted-but-not-yet-approved change packet has NO lawful origin
      shape: `ad_hoc` requires `approved_on`, which does not exist before
      approval, and omitting the origin block is itself an error. Both other
      draft packets in this repository sit in the identical state. Filed as
      **issue #318** rather than worked around by inventing an approval date.
