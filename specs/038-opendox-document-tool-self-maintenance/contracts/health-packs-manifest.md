# Contract: `health/packs.yaml`, the check-pack manifest

Status: draft

**Feature**: 038 · **Authority**: R2Q22 (a) (openDox-spec schema 2), R2Q21 (a)
(this file is authoritative for what the engine runs), R2Q18 (a), R2Q16 (a);
boxes 15.1a, 15.1b, 15.6, 15.6a. **RULED with the plan** (`#656`
`6013547504`, as recommended: OQ-H15-5, -10, -11, -12, -14, -19, -21). Review
round 1 removed the per-entry budget and bounds (lane 3's bwrap-facts FIX),
added the `commit` refusal for a
corpus-relative source (lane 3's T047 FIX), hardened the git transport (ADV-21)
and completed the canary (lane 3's T055 FIX).

**Where it lands.** T040 authors the schema in openDox-spec; T060 pins and cuts
it; T047 copies it into openDox-code's copy record at the pinned commit (after
T041), and implements the reader.

## Shape: exactly 15.1a's fields

```yaml
schema_version: 1
kind: opendox-health-packs
packs:
  - id: house-style                    # ^[a-z0-9-]+$, unique in this file; "opendox" is reserved (15.7)
    version: 1.4.0                     # MUST equal the pack's own declaration (15.2)
    source: tools/packs/house-style    # corpus-relative: NO commit (15.1a)
    digest:
      algorithm: sorted-ls-tree-r-v1
      value: <64-hex>
  - id: shared-rules
    version: 2.0.0
    source: https://example.invalid/packs/shared-rules.git   # a git URL: commit REQUIRED
    commit: <40-hex>
    digest:
      algorithm: sorted-ls-tree-r-v1
      value: <64-hex>
```

`sorted-ls-tree-r-v1` is the source-tree digest `neutral-product-pin` defines over
a commit (`contracts/opendox-pin.yaml:122-134` in openxFactory). Applied here to
the tree-ish `<commit>:<source>` with relative paths, which is a reading of that
definition for a subtree, stated so (OQ-H15-12). For a corpus-relative source,
`<commit>` is the corpus commit the run reads; in a working-state run it is HEAD,
and the pack is taken from HEAD's tree, so an uncommitted edit to a pack never
runs (the manifest itself is read from HEAD in that run too).

## Rules

- **Pinning** (15.1a). A pack runs only if its tree's digest equals
  `digest.value`, checked before a single line of it is imported. A git-URL
  source MUST carry `commit`; a corpus-relative source that carries one is
  REFUSED (it would name a commit the corpus cannot check). A gitlink inside a
  pack is refused.
- **Fetching** (OQ-H15-14; ADV-21). The ENGINE, never the pack, fetches a git-URL
  source at `health run`, into a cache under `OPENDOX_STATE_DIR`, over `https://`
  or `ssh://` (and scp-like `user@host:path`) only. A `file://`, `ext::` or local
  path source is refused; a URL carrying a credential is refused; the fetch
  reuses the runtime push's hardened transport rules (`protocol.ext.allow=never`,
  and the repository-local command-config refusal of
  `runtime/repository_act.py:1335-1372`). Offline, the entry gets a finding
  against it.
- **What a pack may import** (R2Q18 (a); N-3). The standard library and
  `opendox.health_contract` only. The sandbox binds, read-only, the install's
  interpreter, its standard library and that one module, never `site-packages`.
- **The sandbox** (15.1b, R2Q16 (a)). Packs run only inside `bwrap` at a fixed
  system path, proved live by the per-run canary (OQ-H15-9, -21): no network, no
  write outside its tmpfs, no view outside the exported tree (R2Q19 (a)), its own
  `/proc`, `--clearenv` with the allowlist `PATH`, `LANG`, `PYTHONNOUSERSITE=1`,
  and `close_fds`. The canary the engine plants before spawning is a CANARY
  environment variable and a CANARY descriptor (15.6a); `fixture-escaping-pack`
  hunts both, through its environment and `/proc/self/fd`, and follows a planted
  symlink, and every attempt must fail. With no live sandbox, no pack runs and ONE
  install-level finding says why. A host's in-process check is not a pack and
  never appears here.
- **Budget and bounds are the engine's** (15.6). The per-pack time budget is
  `health run --timeout` (default 60 seconds, ceiling 600). The other bounds are
  engine constants, declared in the engine and here, never read from the corpus:
  address space, CPU seconds, file size, the `--size` tmpfs and a stdout byte
  cap through rlimits and `bwrap`; and the process count through a cgroup's
  `pids.max` where a cgroup is delegated. `RLIMIT_NPROC` is NOT used as a
  per-pack bound: setrlimit(2) counts it per real user, not per sandbox, so it
  would count the user's other processes (lane 3's bwrap-facts FIX). Where no
  cgroup is delegated, the process count is bounded by the PID namespace and the
  time budget, which ends the whole tree (15.1b). T056 measures the defaults
  against `pack-corpus` before they are fixed (ADV-22).
- **A pack's failure is a finding** (15.6). A timeout or bound hit, a crash, a
  non-JSON stdout or a stdout over the cap is a finding against THAT pack; the
  run continues. stderr is dropped, except a bounded tail in that finding
  (OQ-H15-11).
- **The pack's output.** One JSON document on stdout: `{"findings": [ … ]}`, each
  a finding in `contracts/health-finding.md`'s shape without `id`, `pack_id`,
  `pack_version` or `baseline_class` (the engine stamps those), and optionally a
  `patch`: a unified diff, and nothing else (15.2; data-model.md § Patch).
- **Refusals by name.** A file of another `kind`; a duplicate or reserved id; a
  version that differs from the pack's declaration, or a declaration with no
  version; a missing digest; an unknown key (a budget or bound key included).
  Each refusal is a finding against its entry, and that entry's pack does not run.
- **Labels.** A pack's labels enter the display facet as a health role family
  keyed by pack and family id; a host profile's labels win (OQ-H15-15).
