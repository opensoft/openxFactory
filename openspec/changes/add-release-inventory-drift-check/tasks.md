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

## 3. Implementation — the FOLLOW-ON SLICE, not this packet

- [ ] 3.1 `scripts/doc_health/corpus.py` — one new `RealGit` reader returning a
      blob's RAW BYTES at a commit. Every existing reader decodes to text, and
      the inventory's identity rule names text canonicalization an invalid
      digest source, so an existing reader cannot be reused.
- [ ] 3.2 `scripts/doc_health/release_inventory.py` — the family: declared
      bundle, inventory parse, per-member comparison, editorial split.
- [ ] 3.3 The two registrations — `families.FAMILIES` and `__init__.FAMILY_IDS`
      — and DELIBERATELY NOT `FAMILY_RESOLUTION`, with the reason recorded at
      the registration site.
- [ ] 3.4 `tests/doc-health/conftest.py` — the `FakeGit` shim for the new
      reader.

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

## 5. Acceptance evidence, both directions — the FOLLOW-ON SLICE

- [ ] 5.1 True positive from history: a fixture reconstructing `08c5aa9` fires
      one `error` naming `gate-action-record.schema.yaml`.
- [ ] 5.2 True negative on today's tree: `origin/main` produces `info` findings
      only and reddens no gate.
- [ ] 5.3 The editorial split is load-bearing: a mutation moving a
      non-editorial member proves the two bands are not the same code path.
- [ ] 5.4 The raw-bytes rule is pinned by a member whose bytes are not pure
      ASCII, so a text-mode reader would compute a different digest and fail.
- [ ] 5.5 Both skips are exercised: no declared bundle, and unreadable history.
- [ ] 5.6 Suite counts move by exactly the predicted amount and in no other
      line.

## 6. Archive

- [ ] 6.1 Archive ONLY after merge with green realization evidence. This change
      ships ACTIVE, following both precedents.

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
