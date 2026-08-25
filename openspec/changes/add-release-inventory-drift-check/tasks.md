# Tasks — add-release-inventory-drift-check

**THIS PACKET IS A DRAFT AND NOTHING IN §2 ONWARD MAY BE EXECUTED YET.** Brett
assigned the SCOUT AND DRAFT of this change, not its construction. §1 is the
scouting that has been done; everything after it waits on the § Open Questions
being ruled, and on the change being ratified.

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

## 2. Ratification — BLOCKED, awaiting Brett

- [ ] 2.1 Rule OQ-1: where the obligation belongs (`release-realization`, a new
      capability, or a document reference).
- [ ] 2.2 Rule OQ-2: `info` or `warning` for editorial drift.
- [ ] 2.3 Rule OQ-3: whether `contracts/README.md` joins the editorial set.
- [ ] 2.4 Rule OQ-4: whether `docs/contract-versioning-policy.md` stays a draft.
- [ ] 2.5 Ratify the change, or rule that the check is not wanted and take only
      §4's documentation half.

## 3. Implementation — BLOCKED on §2

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

## 4. The documentation half — takeable whatever §2 rules

- [ ] 4.1 `docs/contract-versioning-policy.md` gains a paragraph stating that a
      red `verify-commit` at HEAD between cuts is EXPECTED under editorial
      drift, that the reference point is the inventory file rather than a tag,
      and that the remedy is a release cut and never a hand-edit of an
      inventory to make the check pass. This is issue #312's option 2 and it is
      worth landing even if the family is never built.

## 5. Acceptance evidence, both directions — BLOCKED on §3

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

## 6. Archive — BLOCKED

- [ ] 6.1 Archive ONLY after merge with green realization evidence. This change
      ships ACTIVE, following both precedents.

## 7. Recorded, not fixed

- [ ] 7.1 The `contract-v1.36` tag was moved, which
      `docs/contract-versioning-policy.md` § Immutable Tag Correction forbids
      outright ("never moved, deleted, or re-tagged, not even for a defective
      release"; the sanctioned correction is a superseding release). Recorded
      in the proposal with the evidence. The remedy is Brett's to rule and is
      NOT taken here.
- [ ] 7.2 Two schemas changed after the v1.40 tag without a cut
      (`client-overlay.schema.yaml`, `openxwallet-grant.schema.yaml`). Both are
      tracked and currently matching in the manifest's per-file digests, so
      this is not a live integrity defect — but whether a normative schema may
      change between cuts at all is a policy question this packet does not
      answer.
