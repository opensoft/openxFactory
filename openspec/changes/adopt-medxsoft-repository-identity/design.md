# Design: adopt-medxsoft-repository-identity

## 1. Decision provenance

The transfer of `opensoft/MedxFactory` and `opensoft/MedxEHR` to `MedxSoft`
happened on 2026-08-26 and is not a decision this packet takes or reopens. The
operational rewiring — git remotes, the aggregation `.gitmodules`, and the
`medx-roottruth-install` deploy manifests and pins at `d028336` — landed the
same day, outside OpenSpec, correctly: none of it is contract-governed content.

What this packet decides is the treatment of the remaining, governed half, and
the per-surface disposition set (rename / add mapping / leave verbatim) was
settled before authoring and relayed to the authoring session. No verbatim
wording reached it, so none is quoted; `.openspec.yaml` records approver, date
and mechanism instead.

## 2. Why the layer-vocabulary pattern, and not a sweep

`adopt-subject-tenant-domain-vocabulary` (archived 2026-07-23) solved the same
class of problem: a name in wide use across the corpus had to change, some of
its occurrences could not be edited, and a naive sweep would either break pinned
consumers or falsify records.

Its answer had three moving parts, and all three transfer directly:

| that change | this change |
| --- | --- |
| rename the LIVE surfaces to Subject / Tenant / Domain | rename the twenty live occurrences to `MedxSoft/MedxFactory` |
| FREEZE released machine spellings byte-stable (`customer_subject_ref`, role kinds, `$id`s) | FREEZE the ten occurrences in archives, a dated decision record, dated verification tables, and one incident narrative |
| publish `contracts/policies/layer-vocabulary.yaml` so a frozen spelling resolves by lookup | publish `contracts/policies/repository-identity.yaml` so a former identity resolves by lookup |

The differences are worth stating, because they are what makes this the smaller
change of the two. There is **no machine-identifier freeze problem here**: no
schema, field name, `$id` or `contract_id` encodes the owner segment, so nothing
is deferred to a major bundle and nothing waits on `contract-v2.x`. And the
frozen set here is frozen for a DIFFERENT reason — not because a consumer pins
it, but because a record must keep saying what was true when it was written.

## 3. The freeze boundary, stated as a test

The line between "rename" and "leave verbatim" is not a judgment call per file;
it is one question asked of each occurrence:

> **Does this string assert what IS, or does it record what WAS READ?**

- A regression denominator entry, a negative fixture, an installation example, a
  README enumeration and a document's prose all assert what IS. They are wrong
  the moment the assertion stops being true. **Rename.**
- An archived packet's `evidence/`, a dated decision record, and a dated
  verification table pinning `(repository, commit, path, digest)` all record what
  was read at a stated moment. Editing them makes them assert something the run
  that wrote them did not read. **Leave verbatim.**

Two occurrences sit outside both arms and are handled explicitly:

- **`tests/hermes_runtime_contracts/test_domain_regression.py:67`** looks like a
  test constant and is really a **pin of a live fixture**. It asserts what the
  fixture IS, row for row. It renames with the fixture, in the same commit, or
  the suite goes red — which is the mechanism working, not a cost.
- **`scripts/ideation_dashboard/session_pr.py:209` and the three occurrences in
  `tests/ideation-dashboard/test_session_confinement.py`** are an arbitrary
  example `GH_REPO=` value inside prose about a recorded confinement incident.
  The string is not repository identity at all — any repository name would serve
  — so neither arm applies and the honest treatment is to leave the narrative
  alone.

## 4. The consequence nobody would guess: the sort order moves

`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` lists its
five entries bytewise sorted by repository, and
`tests/hermes_runtime_contracts/test_domain_regression.py:259` asserts exactly
that:

```python
assert repositories == sorted(repositories, key=lambda value: value.encode("utf-8"))
```

`M` is `0x4D` and `o` is `0x6F`, so `MedxSoft/MedxFactory` sorts BEFORE
`opensoft/AdxFactory`. The renamed entry **moves from third position to first**,
and `PINNED_TABLE` — which is compared to the fixture by `zip` in document order
— moves with it in the same commit. A rename that respells without reordering
leaves the fixture schema-valid and the suite red.

The negative fixtures under `fixtures/regression/` are respelled for
consistency; their ordering is not asserted by any test and the validator does
not check order, and in `duplicate-repository.yaml` the deliberate duplicate is
`opensoft/AdxFactory`, so the reorder cannot disturb what those fixtures prove.
The `opensoft/LegalxFactory` exclusion row is untouched: that repository was not
transferred.

## 5. Version treatment, derived rather than assumed

Six of the fifteen edited files are members of the `contract-v2.0` digest
inventory: the regression inventory fixture, its three negative fixtures,
`contracts/hermes-runtime/README.md`, and `docs/contract-versioning-policy.md`
(a versioning document, and membership is closed over those). None is in
`scripts/doc_health/release_inventory.py`'s `EDITORIAL` set, which holds exactly
`contracts/CHANGELOG.md`, `contracts/manifest.yaml` and `contracts/README.md`.

Two rules then decide the treatment, and neither leaves discretion:

1. `docs/contract-versioning-policy.md` § "What a red `verify-commit` at HEAD
   means" — a mismatch on a non-editorial member "is a defect: a normative
   contract's bytes moved while the repository went on declaring a bundle that
   describes different bytes". **The remedy is a release cut, never a
   hand-edit**, and the same section forbids adjusting
   `contract_bundle_version` to make a comparison succeed.
2. The change class is **Additive (minor)**: values move, no required field is
   added, no shape is removed, and no role or vocabulary SEMANTICS change — the
   sense in which the policy's Breaking class uses "vocabulary" is the
   layer-role vocabulary, which this does not touch. `contract_schema_version`
   stays at 1.

So: the next available additive minor after `contract-v2.0`, **allocated at
realization** through the policy's Bundle Realization Order. No number is
reserved in this proposal, because the policy forbids reserving one before merge
order is known.

One operational consequence is recorded in the CHANGELOG at the cut rather than
left to be discovered: release engineers resolving the denominator pass
`--domain-repo <canonical-repo>=<checkout>`, and **the key to pass for the
medical domain becomes `MedxSoft/MedxFactory`** from that bundle forward. It is
a migration note, not a deprecation: there is no shape that could accept both
spellings, and a consumer on an older bundle keeps using the older key with the
older bundle, which still verifies at its own tag.

`contracts/policies/repository-identity.yaml` follows `layer-vocabulary.yaml`'s
registration exactly — a `contracts/manifest.yaml` entry of `type: policy` with a
per-file `sha256` and a `consumption_rule`. Whether it also becomes a digest
inventory member is settled at the cut by
`scripts/validate-contract-release.py build`, and the observed precedent is that
`contracts/policies/layer-vocabulary.yaml` is registered in the manifest and is
NOT a member of `contract-v2.0`'s inventory.

## 6. Why a new capability

Set out in the proposal and not repeated here. The one point worth keeping in
the design record: the alternative considered and rejected was hanging the rule
on `repo-boundary-governance`, which already spells `opensoft/…` three times.
It was rejected because that capability's requirements are about WHICH
repository holds WHICH authority, and an identity rule placed inside an
ownership boundary would make every future transfer read as a boundary change —
exactly the confusion `adopt-subject-tenant-domain-vocabulary` avoided by not
hanging layer naming on `hermes-domain-overlay`.

## 7. Non-goals

- **Renaming anything in `installs/hermes-install`.** It consumes openxFactory by
  pin; its `config/negative/duplicate-domain-layer.manifest.yaml` names the old
  owner and is a separate act in that repository at its next pin bump — the same
  disposition the vocabulary change gave the same repository.
- **Re-doing, blessing, or governing the operational rewiring** already landed on
  2026-08-26.
- **Sweeping the four untransferred DomainxFactory repositories**, whose
  identities did not move.
- **Adding a check family.** No deterministic family is added, removed or
  renumbered, and no family enumeration is restated. Whether a family should
  ever verify that no live surface names a mapped former identity is a later
  question; the mapping this change publishes is the input such a family would
  need, and building it here would be a second change riding a first.
