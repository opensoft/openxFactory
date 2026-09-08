# Planning Contract: Release And Consumer Pin

Status: draft

## Release Inventory

The realized inventory contains:

```yaml
schema_version: 1
kind: openxfactory-contract-release-digest-inventory
bundle_tag: contract-vX.Y
repository: opensoft/openxFactory
digest_algorithm: sha256
digest_source: raw_git_blob
path_order: bytewise_utf8
entries:
  - artifact_id: hermes-runtime-topology
    path: contracts/hermes-runtime/runtime-topology.schema.yaml
    type: schema
    git_mode: "100644"
    schema_id: hermes-runtime-topology
    schema_version: 2
    digest: sha256:<64-lowercase-hex>
```

The inventory excludes itself and does not contain its own commit. The annotated tag anchors the commit; the downstream compatibility manifest pins the inventory digest externally.

## Release Verifier

```text
scripts/validate-contract-release.py build --tag <tag> --output <path>
scripts/validate-contract-release.py verify-commit --commit <sha>
scripts/validate-contract-release.py verify-promotion --commit <sha> --remote origin --tag <tag>
scripts/validate-contract-release.py verify-tag --remote origin --tag <tag>
```

- `build` hashes candidate regular-file bytes and emits sorted membership.
- `verify-commit` ignores the working tree and reads mode/blob bytes from the exact commit.
- `verify-promotion` runs immediately before tagging and proves remote tag absence, next-version validity, candidate reachability from remote main, and unchanged manifest/changelog/inventory/release-surface blob IDs since review.
- `verify-tag` proves the remote ref is annotated, peels to the expected commit, is reachable from published `origin/main`, and agrees with manifest/changelog/inventory.

## Promotion Sequence

1. Fetch origin and tags; serialize release surfaces.
2. Rebase and recheck available bundle/tag immediately before allocation.
3. Update semantic files, manifest, changelog, README, and inventory atomically.
4. Commit candidate C; run complete gates and independent review on C.
5. Promote C to `origin/main` without rewriting when possible.
6. If promotion creates M, rerun every gate/review on M and make M the candidate.
7. Run `verify-promotion`; tag only the unchanged reviewed main-line candidate.
8. Push/verify the annotated tag and independently reproduce raw blob digests.

Published tags are immutable. A defect is superseded by a new release.

## Domain Regression Denominator

The schema-validated realized inventory lives at `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`, is indexed by `contracts/hermes-runtime/fixtures/index.yaml`, and pins these exact published `stack.yaml` blobs; all currently pin openxFactory `3d51c3ed5854d112bcc049e1ef7f70863b993fa3`, schema version 1:

| Repository | Commit | Digest |
|---|---|---|
| `opensoft/AdxFactory` | `d0e42622d1da51a3aa6475e2df076df4e55e7918` | `sha256:b5ab723eac7395523a7988468076048e4d0426e03b556231dfb4c282bb8b3fc9` |
| `opensoft/LedgerxFactory` | `1b2ca4c1e66b5e90c9e983a7d0aad11c1ab5ae1c` | `sha256:85d67c54a07f3d4e31943257cf43cb19e0fc400f39a0c719591ed30eeb140ab9` |
| `opensoft/MedxFactory` | `280fdbb5aee8cd83f5c75defd652c1a60039cd0e` | `sha256:02e4b34528217870e982462dde4ff8624c29a7b9e61f3ab405f4710307ff6622` |
| `opensoft/OpsxFactory` | `beed3481fb7f500695bcc4394bb686fab125ad71` | `sha256:3de89a6c7e8b9f112deb7074b8798dc17311425f819968f2f7e1c7e86c7e8fa0` |
| `opensoft/codexFactory` | `7bfa492f700de29cdeab31dc899420745546d982` | `sha256:06f88e192bfd17d42ea6519072e472b9f6d028d88ab0985065640e37c9719722` |

LegalxFactory is an explicit exclusion until it has a canonical `stack.yaml`. Tests accept explicit `--domain-repo` mappings or a mirror root whose canonical `owner/repo` resolves only to `<root>/<owner>/<repo>` or `<root>/<owner>/<repo>.git`, read only exact Git objects, and generate duplicate-Customer negatives without modifying domain repos. Ambiguous roots, missing objects, or inaccessible required repositories fail release with exit 2.

## Hermes Install Closure Packet

The downstream packet is `evidence/gates/g0/<bundle-tag>.yaml`, validated in Hermes Install by `config/schemas/g0-closure-evidence.schema.yaml`, and records:

- openxFactory repository, annotated tag object, peeled commit, manifest/inventory paths and digests;
- every consumed contract ID/path/schema version/digest;
- exact landed Hermes Install commit;
- repository-relative compatibility-manifest, checker, runtime-binding, and evidence paths/digests;
- positive online/offline and deliberate-drift command results plus evidence digests;
- strict OpenSpec and Speckit-analysis results.

openxFactory records only `openspec/changes/archive/2026-08-27-add-hermes-customer-subject-runtime-contract/evidence/hermes-install-g0-handoff.yaml`, validated against `contracts/hermes-runtime/consumer-handoff-receipt.schema.yaml`, after the downstream feature lands in canonical repository `opensoft/xFactory-Hermes-Install`. The schema fixes `consumer_repository` to that value, and indexed negative fixture `contracts/hermes-runtime/fixtures/pins/consumer-receipt-wrong-repository.yaml` proves that `FarHeap/Hermes-Install` fails with `HGR-HANDOFF-CONSUMER-REPOSITORY`. Validation requires an explicit `--consumer-repo opensoft/xFactory-Hermes-Install=<checkout-or-mirror>` or deterministic consumer root and independently reads the packet plus every recorded path as exact `commit:path` Git objects at the receipt's landed commit. Missing/unfetchable objects exit 2; working-tree receipt claims are insufficient. Receipt validation is required before OpenSpec task 5 closure. This feature does not edit Hermes Install.
