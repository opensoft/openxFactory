# Contract: `health/packs.yaml`, the check-pack manifest

Status: draft

**Feature**: 038 · **Authority**: R2Q22 (a) (openDox-spec schema 2), R2Q21 (a)
(this file is authoritative for what the engine runs), R2Q18 (a), R2Q16 (a).
Boxes 15.1a, 15.1b, 15.6. **A PROPOSAL until Brett rules the plan** (OQ-H15-5,
-10, -12, -14, -19, -21).

**Where it lands.** T040 authors the schema in openDox-spec; T047 copies it
into openDox-code with its digest checked and implements the reader.

## Shape

```yaml
schema_version: 1
kind: opendox-health-packs
packs:
  - id: house-style                    # ^[a-z0-9-]+$, unique in this file; "opendox" is reserved (15.7)
    version: 1.4.0                     # MUST equal the pack's own declaration (15.2)
    source:
      path: tools/packs/house-style    # corpus-relative; OR
      # git: https://example.invalid/packs.git   with  commit: <40-hex>
    digest:
      algorithm: sorted-ls-tree-r-v1   # over <commit>:<source> with relative paths (OQ-H15-12)
      value: <64-hex>
    timeout_seconds: 30                # optional; the declared default applies
    bounds:                            # optional; PROPOSED defaults shown (OQ-H15-5); T048 fixes them after running pack-corpus under them
      address_space_mb: 512
      cpu_seconds: 20
      processes: 16
      file_size_mb: 16
      tmpfs_mb: 64
      stdout_kb: 1024
```

## Rules

- **Pinning.** A pack runs only if its tree's digest equals `digest.value`; a
  git source also needs `commit`, and the ENGINE fetches it at `health run` into
  a cache under `OPENDOX_STATE_DIR`, never the pack (OQ-H15-14). Offline, the
  entry gets a finding against it. A gitlink inside a pack is refused.
- **What a pack may import.** The standard library and `opendox.health_contract`
  only (R2Q18 (a), decision N-3). The digest plus the install's version pin
  everything that runs.
- **The sandbox** (15.1b, R2Q16 (a)). Packs run only inside `bwrap` at a fixed
  system path, proved live by the per-run canary (OQ-H15-9, -21): no network,
  no write outside its tmpfs, no view outside the exported tree (R2Q19 (a)),
  rlimits always and cgroups where delegated. With no live sandbox, no pack
  runs and ONE install-level finding says why. A host's in-process check is
  not a pack and never appears here.
- **Bounds.** A timeout or bound hit, a crash, a non-JSON stdout or a stdout
  over `stdout_kb` is a finding against THAT pack (15.6); the run continues.
  stderr is dropped, except a bounded tail in that finding (OQ-H15-11).
- **The pack's output.** One JSON document on stdout: `{"findings": [ … ]}`,
  each a finding in `contracts/health-finding.md`'s shape without `id`,
  `pack_id` or `pack_version` (the engine stamps those).
- **Refusals by name.** A file of another `kind`; a duplicate or reserved id; a
  version that differs from the pack's declaration; a missing digest; an
  unknown key. Each refusal is a finding, and no pack from a refused file runs.
- **Labels.** A pack's labels enter the display facet as a health role family
  keyed by pack and family id; a host profile's labels win (OQ-H15-15).
