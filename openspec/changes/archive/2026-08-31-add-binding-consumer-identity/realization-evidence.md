# Realization evidence — add-binding-consumer-identity

**REALIZED IN TWO ACTS. Act one: PR #516, squash `5e8a33cf` — the schema, the
validator's warning channel, the packaged corpus, the generator sweep. Act two:
THIS CUT, `contract-v2.4`.** This file is the working record of act two: the
fresh count the number was allocated by, the two drift findings the cut
discharges, the gate outputs measured at the branch tip, the `contract-v2.3`
measurement taken alongside, and the things a CHANGELOG entry has no place for.
The `contract-v2.4` entry in `contracts/CHANGELOG.md` is the published version
of the same facts.

The change does NOT archive with the cut. It carries a code surface, so the
archive gate (`docs/release-realization-flow.md`) wants the merge and a green
run first; §7.1 stays open until then, and §7.2's mechanical assertion runs at
that archive rather than here.

## The bundle number, fresh-counted at the cut

§5.3 declines to number the release in the packet ON PURPOSE: allocation is by
MERGE ORDER, and a number written before the merge is a number the next packet
to land would have to renumber. So it was counted at the branch tip, not
inherited:

* `contracts/CHANGELOG.md` top entry: `contract-v2.3`, 2026-08-29.
* `contracts/releases/`: inventory files present through `contract-v2.3`.
* `git tag -l 'contract-v2*'`: `contract-v2.0`, `contract-v2.1`, `contract-v2.2`
  — and NOT `contract-v2.3`.
* No Unreleased block pending: `grep -i unreleased contracts/CHANGELOG.md`
  returns only historical prose inside older entries.

`contract-v2.3` is therefore SPENT — declared by a manifest version, a changelog
entry and an inventory file, and consumed as a number — but untagged. The next
available additive number is **`contract-v2.4`**, and this cut takes it. The
spent-but-untagged state is not a licence to reuse the number: see the
disposition below.

## The two findings this cut discharges, quoted

Before the cut, doc-health's `release-inventory-drift` family reported exactly
two members of the standing `contract-v2.3` inventory whose bytes had moved
under #516:

```text
- severity=error family=release-inventory-drift repo=openxFactory
  path=docs/contract-versioning-policy.md
  rule="bytes differ from the digest 'contract-v2.3' records"
  action="cut a release through the bundle realization order; never hand-edit an
  inventory or contract_bundle_version to make this comparison pass"
  class="auto-fixable"
- severity=info family=release-inventory-drift repo=openxFactory
  path=contracts/manifest.yaml
  rule="bytes differ from the digest 'contract-v2.3' records (editorial member —
  expected between cuts)"
  action="cut a release through the bundle realization order; never hand-edit an
  inventory or contract_bundle_version to make this comparison pass"
  class="auto-fixable"
```

THE REMEDY LINE IS THE INSTRUCTION THIS CUT FOLLOWED, and the one thing it
forbids is the shortcut: hand-editing an inventory or the
`contract_bundle_version` to make the comparison pass. §6.3 was therefore left
UNTICKED at act one with the reason measured rather than ticked with an excuse,
and it closes here BY §5.3, in the same act.

## doc-health, same-clock, both directions

Two checkouts, **both named exactly `openxFactory`** — the finding identity is
`(family, repo, path)` and the repo is the basename, so a differently-named
baseline manufactures phantom findings — one at `origin/main` (`1d7e9bd2`) and
one at this branch, run in the same session at `--as-of 2026-08-30` with
`python3 scripts/doc-health.py --single-repo <path>`:

| | critical | error | warning | info | findings | `release-inventory-drift` |
| --- | --- | --- | --- | --- | --- | --- |
| baseline `origin/main` | 4 | 5 | 38 | 12 | 59 | **2** |
| branch (this cut) | 4 | 4 | 38 | 11 | 57 | **0** |

The set difference was taken in BOTH DIRECTIONS over the machine block, not
inferred from the headline. Findings present on the branch and absent from the
baseline: **none, of any family**. Findings present on the baseline and absent
from the branch: exactly the two quoted above. Every other family is identical
on both sides — staged-topic-template 26, register-lifecycle-consistency 10,
modified-block-currency 8, tag-hygiene 4, record-immutability 4,
staged-candidate-aging 3, ideation-routing 1, document-catalog 1.

A NOTE ON THE NUMBERS §6.3 RECORDED EARLIER. That box quotes a baseline of
4/4/28/12 and a branch of 4/5/28/13. Both were true and neither is now: they
were measured while the branch was UNMERGED, so the two drift findings sat on
the branch side. #516 has since landed, so on `main` they are the baseline's,
and the cut removes them. The delta is the same two findings either way — what
moved is which side of the comparison holds them.

## The inventory, built LAST

```text
python3 scripts/validate-contract-release.py build \
    --tag contract-v2.4 --output contracts/releases/contract-v2.4.digests.yaml
release build: pass
  bundle_tag=contract-v2.4
  entries=283
```

Built AFTER every other member was final — the manifest bump, the changelog
entry, the policy resolution, the README row, and the boundary pin below — and
never hand-edited. It was built twice for that reason: once after the four
editorial members, then DISCARDED AND REBUILT when the suite forced a fifth
member to move. "Inventory built last" means last, not first-drafted.

MEMBERSHIP IS UNCHANGED: 283 entries in `contract-v2.3`, 283 in `contract-v2.4`,
zero added and zero removed. That is what an ADDITIVE release looks like in an
inventory — the growth is in what a member ASSERTS, not in which members exist.
Exactly five digests move, and each is a file this cut edited:
`contracts/CHANGELOG.md`, `contracts/README.md`, `contracts/manifest.yaml`,
`docs/contract-versioning-policy.md`, and
`tests/intent-compliance/test_release_boundary.py`.
`contracts/releases/contract-v2.3.digests.yaml` is untouched.

## The one pin the bump forced, and why it was advanced rather than broadened

The suite's first run at the cut reported **2 failed**, both the same guard:

```text
FAILED tests/intent-compliance/test_release_boundary.py::test_release_membership_when_registration_changes_then_transition_is_atomic
FAILED tests/intent-compliance/test_release_boundary.py::test_release_inventory_when_registration_changes_then_schema_pins_are_atomic
E   Failed: unsupported release state: contract-v2.4
```

THE TRIPWIRE WORKED. That file holds the intent-compliance family's release
membership and its manifest registration together across the boundary its
introducing release created, and it classifies the bundle from an ENUM OF NAMED
VALUES — `contract-v2.1` before the family existed, `contract-v2.3` at its
introducing release — failing loudly on any bundle it has not been told about.
Nothing else would have caught the bump: the library floor is
`INTENT_RELEASE_FLOOR = (2, 3)` and the membership rule is an AT-OR-AFTER
comparison, so `release_membership` accepted `contract-v2.4` silently and
correctly. The enum is where a human is required to say which side a new bundle
falls on.

`contract-v2.4` is past the floor, the family is registered in
`contracts/manifest.yaml`, and the family's files are present — so it is
classified WITH the introducing release and asserts exactly the same membership.

**ADVANCED, NOT BROADENED, and the difference is the whole value of the guard.**
The tempting fix is to replace the enum with the library's own `>= (2, 3)`
comparison, which would make this and every future bump pass silently. That
would delete the only mechanism in the estate that forces a conscious
classification at a cut. So the enum gains one named member,
`FEATURE_SUCCESSOR = "contract-v2.4"`, handled by the same match arm as the
introducing release, and the next bundle trips it again. No test is added,
removed, renamed, weakened or skipped: 13 tests in that file before, 13 after,
all passing.

The file is a release-inventory member (`tests/intent-compliance/` is inside the
family's membership), which is why the inventory was rebuilt after this edit
rather than before it.

## THE ASYMMETRY A REVIEWER WILL ASK ABOUT

`contracts/schemas/xfactory-credential-contracts.schema.yaml` — the file this
whole change edits — is **registered in `contracts/manifest.yaml` and is NOT a
release-inventory member.** Its absence from the 283 is not an omission and not
a coverage gap:

* the POLICY DOCUMENT's bytes are the inventory's business, which is why
  `docs/contract-versioning-policy.md` is the ERROR-band member that drifted;
* the SCHEMA's identity travels by its manifest row `sha256`,
  `d0e936fc7377dc5346d9863a5cec74b4edb5b73300c17b66843798bf96a47028`, which
  `scripts/validate-manifest-digests.py` verifies with the other 149 rows and
  `tests/credential_contracts/test_manifest_row_digest.py` recomputes from the
  file on disk, scoped to this one row so it reds for THIS capability's reason
  and cannot be greened by an unrelated row.

That row-digest test is §5.4's built invariant, and it is the coordination
mechanism with `add-credential-escrow-checkout` — a RATIFIED, frozen sibling
that owes an additive minor on this same schema file and mentions this change
nowhere. Telling "whichever cuts second" to re-read binds only the packet that
wrote the instruction; the digest test binds every writer, including `main`.
Verified green at this cut: recomputed from disk, matches the row.

## Gates at the branch tip

| gate | result |
| --- | --- |
| `validate-contract-release.py verify-commit --commit <tip>` | `release verify-commit: pass`, `inventory=contracts/releases/contract-v2.4.digests.yaml`, exit 0, zero findings |
| `validate-contract-release.py verify-promotion --remote origin --tag contract-v2.4` | 6 findings, ALL reachability-from-`main`: `HGR-RELEASE-CANDIDATE-UNREACHABLE` + 5 × `HGR-RELEASE-SURFACE-DRIFT`. EXPECTED pre-merge; see below |
| `validate-manifest-digests.py` | `OK contracts/manifest.yaml: 150 per-file digest(s) verify` |
| `validate-credential-contracts.py .` | `self-test: 6 positive + 16 negative + 10 warning example(s) confirmed, 8 deprecation code(s) probed`; `openxFactory: 0 contract(s) checked, 0 skipped, 0 warning(s), 0 error(s) -> PASS` |
| `verify-openxwallet-pin.py` | `OK openxwallet-pin verified: openXwallet@6b248d4050e1f88b3ca75c1290ad2c81f465300c (tag label wallet-v1.3), gitlink read from HEAD, 8 digest(s) recomputed` |
| `openspec validate add-binding-consumer-identity --strict` | `Change 'add-binding-consumer-identity' is valid` |
| `openspec validate --all --strict` | `Totals: 78 passed, 0 failed (78 items)` |
| `pytest tests/ -q -m "not postgres"` | `8230 passed, 21 skipped, 338 deselected, 9 warnings, 46 subtests passed`, **0 failed / 0 errors**, exit 0. Selected 8251; skipped exactly 21 — no pin moved a count |

`verify-promotion` IS REPORTED, NOT CHASED. Every one of its six findings is the
same class: the candidate is not an ancestor of published `main` because it is
not merged, and the five release-surface blobs differ from `main` for exactly
that reason. It reports NO `HGR-RELEASE-TAG-EXISTS` — the `contract-v2.4` name
is free on the remote — and no finding from the inventory-and-version-agreement
check at the commit, which is the half that measures the cut itself. The class
clears on merge.

## `contract-v2.3`, measured

Taken at this cut because the fresh count surfaced it, and recorded as a
MEASUREMENT rather than as a decision.

`contract-v2.3` is declared on `main` by three artifacts — the manifest's
`contract_bundle_version` (until this cut moved it), its `contracts/CHANGELOG.md`
entry, and `contracts/releases/contract-v2.3.digests.yaml` — and its annotated
tag was never published. `docs/contract-versioning-policy.md` § Untagged Bundles
After Enforcement Began — DISCHARGED 2026-08-25 names the remedy class for
exactly this shape: RETRO-PUBLICATION, NOT RE-DATING, at

> the EARLIEST FIRST-PARENT COMMIT on published `main` that DECLARES the bundle
> and at which `verify-commit` PASSES.

Both halves were measured. Walking `git rev-list --first-parent origin/main` and
reading `contract_bundle_version` at each commit, the bundle is declared at
`1d7e9bd2`, `5e8a33cf`, `698073f7` and `ec8be5aa`, and the commit below
`ec8be5aa` (`afe29561`) declares `contract-v2.2` — so the earliest is
**`ec8be5aa62179713f37ee12dab53a948d791e147`**, the PR #514 merge. And:

```text
python3 scripts/validate-contract-release.py verify-commit \
    --commit ec8be5aa62179713f37ee12dab53a948d791e147
release verify-commit: pass
  inventory=contracts/releases/contract-v2.3.digests.yaml
```

exit 0, zero findings. The candidate satisfies the rule as written.

**TAG PUBLICATION IS THE REPOSITORY OWNER'S ACT AND IS PENDING.** This packet
measures; it does not publish, and it does not treat its own measurement as the
act. Nothing in `contract-v2.4` consumes `contract-v2.3` as a published bundle,
and the discharged subsection's own closing clause still binds: no reader may
cite it, or the period it narrates, to treat an untagged bundle as released.

## The `unpublished:` sweep

`grep -rn 'unpublished' contracts/ docs/ scripts/` over `*.yaml`, `*.md` and
`*.py` returns sixteen hits and **no sentinel needing resolution**. Every hit is
prose: CHANGELOG entries and `scripts/ideation_dashboard/doxbench_contracts.py`
comments NARRATING sentinels that were real at the time, plus the policy's
legacy-sequence sentence and the ontology README's pending-revision rule.
`doxbench_contracts.py`'s `CONTRACT_REF` stays at `contract-v2.2`
(`8ccfb67bc0fabfa728d709a2efa0cd87b14656fb`), correctly: its two pinned schema
files — the model catalog and the chat-turn family — have byte-identical content
at this cut, and a pin names ONE release for both files. Re-verified here, as
that file's own comment demands: NO `unpublished:` VALUE IS ASSIGNED ANYWHERE.

## What is NOT here

* **The `contract-v2.4` tag.** Steps 1–2 of the versioning policy allocate the
  version and build the inventory at realization; step 5 publishes the annotated
  tag against the commit that actually LANDS. Until this branch merges there is
  nothing honest to name, and publication is the owner's act regardless.
* **The `contract-v2.3` retro-publication.** Measured above, owner's act.
* **The archive.** §7.1 moves this change from active to archived in the README
  OpenSpec Records at the archive PR, after the merge and a green run — never
  with the cut. §7.2's mechanical `grep` assertion over
  `openspec/specs/credential-contracts/spec.md` runs there too.
* **Any new manifest row.** The cut registers nothing; the
  `credential-contracts` row already existed and already carried #516's digest.
* **Anything belonging to `change/realize-signed-execution-chain` (PR #524).**
  It is open and driven separately, touches neither `contracts/manifest.yaml`
  nor `contracts/CHANGELOG.md`, and its family is deliberately NOT registered
  here.
