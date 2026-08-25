---
code_surface: openxFactory (`scripts/doc_health/release_inventory.py` — a new module owning the nineteenth deterministic family: the declared-bundle reader, the inventory parser, the per-member blob comparison, and the editorial/non-editorial split; `scripts/doc_health/corpus.py` — one new `RealGit` reader returning a blob's RAW BYTES at a commit, because every existing reader decodes to text and the inventory's identity rule names text canonicalization an invalid digest source; `scripts/doc_health/families.py` — one registration line in `FAMILIES` and the note recording why the family is deliberately absent from `FAMILY_RESOLUTION`; `scripts/doc_health/__init__.py` — one entry in `FAMILY_IDS` so the family gets its own report section; `tests/doc-health/test_release_inventory.py` plus fixtures — the regression fixture reconstructing the `contract-v1.36` true positive, today's editorial-only negative, the no-bundle and unreadable-history skips, and a structural pin on the raw-bytes rule; `tests/doc-health/conftest.py` — `FakeGit` gains the matching shim. `docs/contract-versioning-policy.md` is RATIFIED by this change (`Status: draft` -> `ratified`), gains the paragraph documenting what a red `verify-commit` at HEAD means between cuts, and carries four corrections the ratification read-through found — see § Ratifying the versioning policy. NO change to the governed corpus, the lifecycle scan set, any existing family's behaviour, the report schema, the regression-diff rule, or any threshold.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle: no schema under `contracts/schemas/` changes, no digest set moves, and no release tag is owed. Note the asymmetry deliberately: this change is ABOUT the release surface and touches none of it. The archive gate is therefore merge-plus-green on main, following `add-promotion-fidelity-check` and `govern-openspec-corpus-membership` exactly — `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose severity counts move by exactly the amount this proposal predicts and in no other line.
Status: ratified
Ratified: Brett Heap, 2026-08-24 — the route (a new capability), both
  verdict levels, the editorial set's membership, the versioning-policy
  ratification fold, and the record-only disposition of the contract-v1.36 tag
  breach were all ruled in session on that date.
Proposed: 2026-08-24
Sequenced-after: add-promotion-fidelity-check (both changes MODIFY `doc-health`'s "Deterministic check families"; that one takes the count seventeen -> eighteen and this one eighteen -> nineteen, so this delta is written against its outcome and must land after it)
Origin: issue #312, filed 2026-08-24 from the `add-doxbench-editing-phase-b` §12 / issue #263 work, where a session ran `verify-commit` by hand for an unrelated reason and found it already red.
---

# Proposal: add-release-inventory-drift-check

## Why

`scripts/validate-contract-release.py verify-commit` **fails at `origin/main`
today**, and has since the `contract-v1.40` tag. It is not failing because a
digest is wrong. It is failing because main has drifted from the inventory it
still declares, and **no gate in any session's set runs the check**, so the
state was invisible until a session ran it by hand for an unrelated reason.

A release-inventory gate that nothing runs is a gate in name only.

The same defect class has been caught here exactly once, at the
`contract-v1.36` cut, whose `contract_bundle_version` was left at the previous
release. It was caught only because the versioning policy's landing sequence
happens to include a manual tag-verify step and someone performed it. Nothing
would have caught it otherwise, and nothing catches the next one.

## What is actually true on main today — measured, not assumed

Every one of the declared bundle's 190 inventory members was compared against
its blob at `origin/main`:

| | |
|---|---|
| declared bundle | `contract-v1.40` |
| inventory members | 190 |
| members matching | **188** |
| editorial drift | **2** — `contracts/CHANGELOG.md`, `contracts/manifest.yaml` |
| **non-editorial drift** | **0** |
| members missing from HEAD | 0 |

**Today's main is editorial-only drift: a bounded, expected state, not a
defect.** Three commits since the tag touched those two files — `525ac8be`,
`38f7b6b6`, and `ba07a0e7` (issue #263's own `consumption_rule` edit, whose
no-release adjudication this measurement independently confirms).

Two things that measurement also settled, both of which shaped the design:

1. **Two normative schemas DID change after the tag** —
   `contracts/client-content/client-overlay.schema.yaml` and
   `contracts/openxwallet/openxwallet-grant.schema.yaml` — and neither is a
   MEMBER of the v1.40 inventory, because membership is scoped to the release
   surface that release touched. They are therefore invisible to this family by
   construction. They are NOT unguarded: `contracts/manifest.yaml` carries a
   per-file digest for both, `validate-manifest-digests.py` verifies all 150 of
   those every session, and both currently match. The two mechanisms answer
   different questions and this proposal does not conflate them — see § What
   this family does not cover.
2. **The `contract-v1.36` defect is detectable by this rule at the commit.**
   Running the same comparison at `08c5aa9` — the commit whose bundle version
   was left at v1.35 — reports `NON-EDITORIAL drift: 1`,
   `contracts/schemas/gate-action-record.schema.yaml`. So the "forgot to bump
   the bundle" class is not a separate detection problem needing tag access: it
   MANIFESTS as non-editorial drift, pre-tag, at HEAD. One rule catches both.

## What changes

1. **A NEW CAPABILITY, `release-surface-integrity`, gains the obligation** —
   "The declared bundle describes the release surface", with the editorial
   members named and the no-tag case handled. Brett ruled 2026-08-24 that this
   gets its own capability rather than joining `release-realization`, which
   governs the proposal/archive lifecycle and says nothing about contract
   bundles. The obligation is stated before any checker enforces it, because a
   checker with no promoted rule behind it is a rule invented in Python — the
   ordering `add-promotion-fidelity-check` states and follows.
2. **`doc-health` gains the nineteenth family**, `release-inventory-drift`,
   which checks that obligation by reference and defines only the checking.
3. **`docs/contract-versioning-policy.md` is RATIFIED**, gains the paragraph
   stating what a red `verify-commit` at HEAD means between cuts, and is
   corrected in four places the ratification read-through found. The paragraph
   is issue #312's option 2: today a session that runs `verify-commit` and sees
   red has nothing to consult, and the obvious wrong move — hand-editing an
   inventory so the check passes — is exactly the one the policy most needs to
   forbid in writing.

## What this family does not cover, stated so nobody reads it as wider

Inventory membership is closed over *the release surface a given release
touched*, not over every contract in the repository. A contract the declared
release never touched is not a member, so this family has no opinion about it
— by construction, not by omission. That gap is covered by a different
mechanism with a different question: `contracts/manifest.yaml`'s 150 per-file
digests, verified every session by `validate-manifest-digests.py`, which asks
"does the digest recorded beside this contract match the file?" This family
asks "does the bundle this commit DECLARES describe this commit's bytes?"

Neither subsumes the other, and this proposal does not claim the family closes
the manifest-digest gap or vice versa.

## Why an OpenSpec change rather than plain tooling

Four grounds, three of them the corpus stating the rule about itself:

- **The family count is enumerated in the promoted spec.** "The doc-health
  deterministic pass SHALL implement seventeen check families" is normative
  text listing them by name. An eighteenth or nineteenth cannot arrive without
  a MODIFIED delta. Both recent precedents did exactly this: sixteen → seventeen
  (`govern-openspec-corpus-membership`), seventeen → eighteen
  (`add-promotion-fidelity-check`).
- **The package says so.** `scripts/doc_health/__init__.py`'s module docstring:
  "The contract (check families, severities, thresholds, report schema) is
  owned by docs/doc-health.md and the `doc-health` spec; this package
  implements it in the same repository. **Changes to WHAT the checks are happen
  through the contract; this package follows.**"
- **The promoted spec installs the requirement on changes like this one.**
  `Governed corpus membership and the lifecycle scan set` ends: "Widening
  either set is a governed change: a promoted OpenSpec change SHALL record the
  new membership together with the measured effect on finding counts by family,
  on the canon-share headline, and on the existing test suite."
- **Both fresh precedents took this route for this exact act** — commissioning
  a new deterministic family — and both split the obligation from the checker
  across two capabilities.

## Design decisions taken by the drafting session

Each was the drafting session's call under standing patterns. D1 was overridden
by ruling and is kept for the record; D2–D4 stand as taken and were not
separately ruled on, so they remain open to veto.

- **D1 — SUPERSEDED BY RULING.** The drafting session proposed putting the
  obligation in `release-realization` as the nearest owner, reasoning that
  minting a capability for one requirement is heavier than the decomposition
  scale rule favours. Brett ruled a new capability instead
  (`release-surface-integrity`). The ruling is the better reading and the
  drafting note is kept rather than deleted so the alternative stays visible:
  `release-realization` governs the proposal and archive lifecycle, and none of
  its six requirements mentions a bundle, an inventory, or a release surface —
  "nearest" was adjacency, not subject.
- **D2 — the split is error / info, not error / warning.** Editorial drift is
  not a lesser defect, it is the expected steady state between cuts; `warning`
  reads as "drift or first-stage aging" and would put a permanent yellow row in
  every report for a condition nobody should act on. `info` is the severity for
  inventory and metrics, which is what this is.
- **D3 — the family is deliberately absent from `FAMILY_RESOLUTION`.** Both of
  its findings are resolved by a release cut, which is what makes them vanish
  between reports; a `contested` finding that vanishes without a citation is
  re-emitted as an `error` under the uncited-resolution rule, so classifying it
  `contested` would turn every correct release cut into a new error. This is
  `add-promotion-fidelity-check`'s reasoning applied to a family whose
  resolution act is even more routine.
- **D4 — raw bytes, and a skip rather than a working-tree fallback.** The
  inventory's identity rule names text canonicalization an invalid digest
  source, so the new reader returns bytes. And an unreadable history yields a
  skip rather than a fall back to the working tree, because an uncommitted edit
  is not drift from the declared bundle and reporting it as such would train
  people to ignore the family.

## Brett's rulings, 2026-08-24

All four questions this packet raised were ruled in session. They are recorded
as answers rather than deleted, because the alternatives were real and a later
reader should see what was decided against.

- **OQ-1 — where the obligation belongs: A NEW CAPABILITY.** The drafting
  session recommended `release-realization`; Brett overrode it.
  `release-surface-integrity` owns the obligation. The override is the better
  reading: `release-realization`'s six requirements govern the proposal and
  archive lifecycle and none of them mentions a contract bundle, a digest
  inventory, or a release surface, so putting this there would have widened a
  capability by adjacency rather than by subject.
- **OQ-2 — the editorial verdict: `info`, not `warning`.** A condition nobody
  should act on must not hold a permanent yellow row in every report.
- **OQ-3 — `contracts/README.md` IS in the editorial set.** By ruling rather
  than by observation: it had not drifted in the measured window, so its
  inclusion is a decision about what may legitimately move between cuts.
- **OQ-4 — the versioning policy is RATIFIED BY THIS CHANGE.** See below; the
  read-through it required found four defects, which this change corrects
  rather than ratifying as-is.

## Ratifying the versioning policy

`docs/contract-versioning-policy.md` has carried `Status: draft` since it was
written, while being cited as decisive — by this change, by issue #312, and by
PR #314's contract-class adjudication. Brett ruled it ratified here.

Ratification required reading it end to end against today's repository rather
than stamping it, and that read found **four defects**. Each is corrected in
this change; none is a rewrite of the policy's intent.

1. **THREE MODERN BUNDLES HAVE NO PUBLISHED TAG, and the policy says that
   cannot happen.** It states "a bundle is not published until its tag exists",
   requires manifest version, changelog heading and tag to match, and records
   that mandatory annotated-tag publication *began* after the legacy sequence.
   Measured against the remote: `contract-v1.33`, `contract-v1.35` and
   `contract-v1.39` each have a changelog entry and no tag. (`v1.0`–`v1.6` are
   the acknowledged legacy sequence and are not at issue.) The rule is NOT
   softened to match practice — that would ratify the gap away. The rule stands
   and the three exceptions are recorded in the policy as a named, undischarged
   gap awaiting disposition.
2. **The legacy-baseline paragraph is stale in the present tense.** It reads
   "with `contract-v1.6` as the manifest baseline"; the manifest baseline has
   been `contract-v1.40` since 2026-08-22. Corrected to past tense so the
   sentence describes the recovery it is about rather than today's state.
3. **The deprecation entry names a superseded vocabulary as canonical.** It
   says the flat `hermes` keys are "replaced by `hermes.layers` with canonical
   roles customer/client/domain". The canonical layer vocabulary has been
   Subject / Tenant / Domain since `adopt-subject-tenant-domain-vocabulary` was
   ratified 2026-07-23; `customer|client|domain` survive only as FROZEN MACHINE
   KEYS. Corrected to say exactly that and to cite
   `contracts/policies/layer-vocabulary.yaml` for the mapping.
4. **What a red `verify-commit` at HEAD means was undocumented** — the gap
   issue #312 named. Added, with the remedy stated and the wrong move named:
   the fix is a release cut, never a hand-edit of an inventory to make the
   check pass.

## Filed elsewhere

**Issue #318 — a drafted-but-unapproved packet has no lawful origin shape.**
`ad_hoc` requires `approved_on`, which does not exist before approval, and
omitting the origin block is itself an error; this packet carried that error
for the whole window it was awaiting rulings, and two other draft packets carry
it now. Not fixed here: inventing an approval date to quiet a check is the move
this change's own policy correction forbids in writing.

## Recorded, not fixed

- **The `contract-v1.36` tag was moved, which the policy forbids.**
  `docs/contract-versioning-policy.md` § Immutable Tag Correction: "A published
  annotated tag is immutable: it is never moved, deleted, or re-tagged, **not
  even for a defective release**", and the sanctioned correction is a
  superseding release. During the v1.36 landing the tag was published at
  `c465b3e` → `08c5aa9`, then deleted and force-pushed to `42c7696` →
  `d37cfa1` to correct the un-bumped bundle version. The re-point is recorded
  in `d37cfa1`'s own commit message. **DISPOSITION — RECORD ONLY (Brett, 2026-08-24).** The tag STAYS AS IT IS: a
  second move would compound the breach rather than repair it, and the
  sanctioned remedy — a superseding release — would spend a version number to
  correct provenance that this record already carries accurately. The breach,
  its reasoning, and this disposition live here, in the change record, which is
  the durable form the ruling takes. No further action is owed and none should
  be taken by a later session reading the policy and noticing the mismatch.
