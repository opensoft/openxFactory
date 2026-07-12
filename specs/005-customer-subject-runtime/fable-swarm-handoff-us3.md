# Fable Swarm Handoff: Gate G0 US3 Migration

Status: record

## Handoff Boundary

The stable provider checkpoint is openxFactory commit
`6418fde6176877652fe11d90ed79bc5850ec3e20` on branch
`005-customer-subject-runtime`.

This checkpoint completes Speckit Foundation, US1, and US2 through T051. It
does not complete Gate G0. The Fable swarm starts with US3 T052 and stops at
the US3 checkpoint after T065. US4 publication and the external
`opensoft/xFactory-Hermes-Install` pin remain later work.

Authoritative locations:

- OpenSpec change: `openspec/changes/add-hermes-customer-subject-runtime-contract/`
- Speckit feature: `specs/005-customer-subject-runtime/`
- Executable tasks: `specs/005-customer-subject-runtime/tasks.md`
- Host worktree: `/home/brett/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime`
- `py-bench` worktree: `/workspace/projects/xFactory/openxFactory-worktrees/005-customer-subject-runtime`

Run repository commands inside `py-bench`. Do not write either absolute path
into committed repository content.

## Proven Checkpoint

- T001-T051 are checked complete.
- One static Customer role template produces multiple isolated runtime
  Customer instances, including the required two-Customer installation.
- Project, patient, and client-company aliases specialize the same neutral
  customer-subject contract.
- Principal, trust-anchor, grant, binding, artifact, approval, trace, and
  PostgreSQL isolation contracts are implemented.
- Trust-anchor, grant, and binding record digests are database-computed from
  their exact closed canonical records.
- Binding creation time is database-derived, and caller backdating cannot
  revive expired authority.
- An independent review found no unresolved P1 or P2 issue in the US2
  integrity tranche.

Verification at the checkpoint:

- Non-PostgreSQL suite: `275 passed`
- PostgreSQL runner contract: `10 passed`
- PostgreSQL 15 source-bound matrix: `61 passed`
- PostgreSQL 16 source-bound matrix: `61 passed`
- PostgreSQL source identity:
  `sha256:867015c448092693bd197be1b4f551f0dc608ced5b99103af95373e8f2b2c522`
- PostgreSQL matrix digest:
  `sha256:ca86746672e9b434e173bb528f7a4a1821996ff994c7ac9131c2824e241cc904`
- Strict runtime validator: 31 catalog members, 25 schemas, 75 fixtures,
  407 collected test nodes, 17 requirements, and 85 scenarios
- Strict OpenSpec validation, Black, compileall, POSIX shell syntax,
  ShellCheck, and `git diff --check`: passed

Evidence records:

- `tests/hermes_runtime_contracts/postgres/evidence/postgres-15.json`
- `tests/hermes_runtime_contracts/postgres/evidence/postgres-16.json`

US3 changes the production SQL and test inventory, so these evidence records
must be regenerated only after the US3 source surface is frozen.

## Ratified US3 Protocol

Implementation must preserve the four separate migration identities now
encoded in the OpenSpec design and migration requirement:

1. A detached mapping payload and `mapping_payload_digest` bind expected
   source content and mappings without authority references.
2. A detached authority envelope binds that payload to exact active
   `run_migration` authority without creating a digest cycle.
3. PostgreSQL derives a logical source boundary from the locked source
   identity, catalog, per-table counts, and dataset digest.
4. Each attempt records a database-derived physical cutover observation with
   actual snapshot/WAL evidence, time, authority, and reconciliation.

Retry identity is installation plus migration ID, mapping-payload digest, and
logical boundary. A physical snapshot may change after rollback only when the
logical source content is identical.

All rows from the twelve canonical v1 tables must receive exactly one
classification:

- Scoped, immutable, non-authorizing compatibility history for jobs, runs,
  events, workers, groups, profiles, memberships, and GitHub-team mappings.
- Structurally non-authoritative quarantine for legacy artifacts, approval
  requests, approvals, and traces that lack v2 integrity/authority evidence.

A successful cutover installs a durable v1 governed-write freeze while
preserving readable v1 history. Continuing writable v1 state requires a later
governed dual-write change.

The exact dataset profile is `xfactory-v1-dataset-binary-v1`; do not replace
its magic bytes, tags, unsigned 64-bit big-endian lengths, typed value
encodings, framed-primary-key ordering, or arbitrary-precision canonical JSON
with text concatenation or implementation-defined serialization.

## Swarm Execution Plan

Keep production SQL under one owner. Parallel lanes may create RED tests and
portable contracts, but they must not collide on shared integration files.

### Lane A: Mapping And Digest

- T053, T056, T057, and T058
- Owns the mapping schema, quarantine schema, migration semantics, digest CLI,
  and golden vectors.
- Proves detached payload/envelope digests, exact binary framing, authority,
  logical-boundary derivation, default-Customer proof, and PostgreSQL-major
  parity.

### Lane B: Readiness And Drift

- T052 and T061
- Owns RED clean-apply/drift tests, the read-only PostgreSQL fingerprint
  validator, and the locked apply boundary.
- Must prove preflight occurs before mutation or role repair and must cover
  both `fresh-v2` and `v1-cutover` profiles.
- Does not edit either production SQL file.

### Lane C: Migration, Recovery, And Quarantine

- T054, T055, T059, T060, and T062
- The sole PostgreSQL/migration owner edits
  `hermes-operational-postgres-v2.sql`, `migrations/v1-to-v2.sql`, and the
  dedicated migration runner.
- Implements the session lock, multi-transaction attempt lifecycle,
  fixed-order twelve-table locks, compatibility-history targets, quarantine
  boundary, reconciliation, crash/ack-loss behavior, and durable v1 freeze.

### Lane D: Integration

- T063, T064, and T065 after Lanes A-C are green.
- The catalog integrator alone edits `contract-index.yaml`, `fixtures/index.yaml`,
  `acceptance-map.yaml`, and `evidence-register.yaml`.
- Regenerates both PostgreSQL evidence records only after production SQL,
  runner, fingerprints, fixtures, and the source-path inventory are frozen.
- Runs the combined US1/US2/US3 strict gate and creates the US3 checkpoint
  commit.

## First Commands

From the `py-bench` worktree:

```sh
git status --short
git rev-parse HEAD
openspec status --change add-hermes-customer-subject-runtime-contract --json
openspec instructions apply --change add-hermes-customer-subject-runtime-contract --json
sed -n '128,170p' specs/005-customer-subject-runtime/tasks.md
```

The worktree must be clean and the initial revision must include the US2
checkpoint above plus this handoff record before the swarm edits files.

## Stop Conditions

Do not:

- Start US4 or allocate a release bundle version.
- Publish or tag openxFactory.
- Edit `opensoft/xFactory-Hermes-Install`.
- Mark OpenSpec acceptance or Gate G0 complete.
- Treat compatibility-history rows as executable jobs or authorizing evidence.
- Regenerate final PostgreSQL evidence while its declared source paths are
  still changing.

Pause the Fable swarm after T065 with a clean US3 checkpoint commit, exact
PostgreSQL 15/16 evidence, strict OpenSpec/validator results, and a list of any
remaining P1/P2 finding. Gate G0 remains active until US4 publication and the
external Hermes Install pin are independently proven.
