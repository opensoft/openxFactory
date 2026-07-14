# Release Candidate Review — contract-v1.9

Status: record

**Change**: add-hermes-customer-subject-runtime-contract
**Feature**: 005-customer-subject-runtime · Task T080
**Candidate commit C**: 64cc000e9a2c24922050df73ec37958dbf5cfca4
**Bundle**: contract-v1.9 · **Date**: 2026-07-14

## Candidate identity

Candidate C is the provider-side realization of the neutral Hermes
customer-subject runtime family, rebased cleanly onto `origin/main` at
`e4b3c7e` (13 feature commits replayed; zero conflicts; the branch and the
advanced main are disjoint in the files they touch). C is
`git rev-parse HEAD` in an isolated realization worktree; nothing is pushed at
review time and no `contract-v1.9` tag exists on the remote.

## Gates on the exact candidate C (all green)

- `openspec validate --all --strict`: 26 passed, 0 failed.
- `validate-hermes-runtime-contracts.py --strict`: 0 findings — 39 contracts,
  32 schemas, 110 fixtures, 17 requirements, 85 scenarios, 803 tests collected.
- `validate-hermes-runtime-contracts.py --require-candidate --domain-repo-root
  <offline mirrors>`: exit 0 (the realized inventory reproduces and the five
  supported DomainxFactory `stack.yaml` blobs resolve at their pinned commits).
- `validate-contract-release.py verify-commit --commit 64cc000`: pass (every
  inventory member reproduces from the committed tree; ignores the working
  tree).
- Non-PostgreSQL pytest: 485 passed, 0 failed.
- `git diff --check`: clean. `black --check` on the two candidate-changed
  Python files: clean.

## PostgreSQL evidence

Unchanged from the US4 checkpoint. The realization touched only release
metadata (`manifest.yaml`, `CHANGELOG.md`, `README.md`, the realized
`releases/contract-v1.9.digests.yaml`, one evidence-register node id, two
realized-state test modules, and the T079/T080 evidence docs). None intersects
the 78-member PostgreSQL evidence source inventory, so the both-majors matrix
is not re-run; source identity `sha256:b2ef44a9…` and matrix digest
`sha256:032f80fa…` are preserved.

## Independent review

The full US4 provider surface underwent a four-lens adversarial review with
per-finding verification before the checkpoint (dispositions in
`specs/005-customer-subject-runtime/us4-provider-handoff/us4-review-findings.md`):
3 findings confirmed, 2 P2 fail-opens fixed with regression tests, 1 P3
(latent) deferred. The realization adds only additive release metadata and the
realized digest inventory over that reviewed surface; it introduces no new
contract, schema, or semantic behavior. The realized-state test adjustments
were re-derived from the observed post-realization CLI behavior and re-verified
green.

## Disposition

Candidate C is APPROVED for promotion. The exact unchanged commit
`64cc000e9a2c24922050df73ec37958dbf5cfca4` is to land on published
`origin/main`; only then may the matching annotated `contract-v1.9` tag be
published. If promotion creates any different main-line commit, every gate and
this review are re-run on that commit before tagging.

Gate G0 remains OPEN after publication: closure additionally requires the exact
downstream `opensoft/xFactory-Hermes-Install` consumer pin and its
independently reproduced digests, owned by that repository's feature (T082+).

---

# Release Candidate Review — contract-v1.10 (supersedes the v1.9 review above)

Status: record

**Change**: add-hermes-customer-subject-runtime-contract
**Feature**: 005-customer-subject-runtime · Task T080 (re-run for the
superseding candidate)
**Candidate commit C**: 203fff0 ("Realize contract-v1.10 release candidate
(T079)") · **Bundle**: contract-v1.10 · **Date**: 2026-07-14

## Why a superseding candidate exists

contract-v1.9 was published (immutable tag on origin, peeled `64cc000`).
After publication, two governed review hardenings changed release-surface
member bytes — `c6f5d6d` (US4 review F-U3: membership closure in release.py
plus six release fixtures) and `0c1e1b6` (US3 review backlog F-4/F-7..F-9:
migration digest surface) — so the frozen v1.9 inventory no longer
reproduces the tree. Per the Immutable Tag Correction policy, contract-v1.10
supersedes v1.9; the v1.9 tag and `releases/contract-v1.9.digests.yaml`
remain as provenance. Membership set is byte-identical to v1.9's
(179 members).

## Candidate identity

C = `203fff0` on `005-customer-subject-runtime` = `origin/main` (`c6f5d6d`)
+ `0c1e1b6` + C. Final fetch/rebase completed before realization
(`git cherry` confirmed all prior branch work already equivalent-present on
`origin/main`; the rebase replayed only the hardening commit, zero
conflicts). Nothing pushed at review time; no `contract-v1.10` tag exists
locally or on the remote. This review record is committed as a record-only
commit on top of C; it is not a release member and alters no member bytes —
the realized inventory reproduces identically from C and from the record
commit.

## Gates rerun against the exact candidate commit (all green)

- Candidate mode (`--require-candidate --strict --domain-repo-root
  <offline-mirror-root>`): exit 0 — the realized inventory reproduces all
  179 members from C's Git objects and the five supported DomainxFactory
  `stack.yaml` blobs resolve at their pinned commits from offline mirrors.
- Strict contract validator, plain and with live domain resolution: pass,
  0 findings — 39 contracts, 32 schemas, 110 fixtures, 17 requirements,
  85 scenarios, 825 tests collected.
- Non-PostgreSQL pytest: 487 passed, 0 failed. OpenSpec strict: 27/27.
- PostgreSQL evidence: exact and untouched by the release surface — source
  identity `sha256:979137d3…` (78 members), 171 tests per major, pass on
  both digest-pinned majors.
- Hygiene: `git diff --check` clean.

## Independent expert review (three Opus lenses + skeptic verification)

- **release-policy — APPROVE, 0 findings.** contract-v1.10 independently
  confirmed as the next available additive version (local and remote tags
  checked read-only); the Immutable Tag Correction policy licenses the
  superseding re-realization; manifest/CHANGELOG/README changes match the
  policy and the T079 task text exactly.
- **audit-soundness — APPROVE-WITH-NOTES, 0 confirmed findings.** The
  FR-042 removal claim (no supported consumer reads
  `source_compatibility_ref.local_source_path`) independently re-derived
  against all validators, runtime modules, and the five consumer
  `stack.yaml` files; exactly one field removed; repo + `source_commit`
  provenance retained. One P3 note raised and REFUTED under skeptic
  verification: consumer `contract_ref` pins are per-consumer
  (codexFactory pins `f2caf05d…` while the other four pin `3d51c3ed…`) —
  the audit's per-consumer assertion contains no falsehood and the removal
  justification is unaffected.
- **inventory-integrity — APPROVE, 0 findings.** Scratch rebuild against C
  byte-identical; member digests hand-verified via `git cat-file`;
  post-F-U3 closure rules (mandatory auxiliaries unconditional;
  semantic_member ⇒ release_member) hold; v1.9 inventory untouched; no
  host-absolute paths.

Zero confirmed findings. The candidate is approved UNCHANGED — no
post-review edits; the reviewed identity `203fff0` is the exact promotion
candidate.

## Disposition

Candidate C (`203fff0`) is APPROVED for promotion. Promotion lands the
reviewed content on published `origin/main`; only then may the matching
annotated `contract-v1.10` tag be published, verified from an independently
refreshed checkout. If promotion creates any different main-line commit,
every gate and this review are re-run on that commit before tagging.
T081 (promotion + tag) is parked at Brett's gate — outward, irreversible
actions. Gate G0 remains OPEN after publication pending the external
`opensoft/xFactory-Hermes-Install` consumer pin (T082+).

## Promotion addendum (2026-07-14, Brett approved T081)

Between review and promotion, `origin/main` advanced by five commits
(avatar-client-lab work + document-cataloging ticks); none touches any of
the 179 release members. Per the disposition's own rule, the candidate was
rebased onto the latest `origin/main` — the reviewed content replayed
byte-identically as realization commit `3f051ca` (review-record commit
`b2e7344` on top) — and EVERY gate was rerun green on the exact rebased
tip: candidate mode with live domain resolution pass/0 findings
(39/32/110/17/85, 825 collected), `verify-commit` pass (all 179 members
reproduce), OpenSpec 27/27, non-PostgreSQL pytest 487 passed, plus the five
upstream avatar-client tests (13 passed). The member bytes and the realized
inventory are identical to the reviewed candidate; only ancestry hashes
changed. Promotion and the annotated `contract-v1.10` tag proceed on this
verified tip with Brett's explicit T081 approval.
