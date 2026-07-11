# Quickstart & Validation Guide: AVC Contract Kernel

**Feature**: 001-avc-contract-kernel | **Date**: 2026-07-11

A validation/run guide proving the kernel works end-to-end. It references
[data-model.md](./data-model.md) and [contracts/README.md](./contracts/README.md)
rather than duplicating artifact detail. No implementation code here.

## Prerequisites

- Python 3 with `jsonschema` and `PyYAML` (already repo dependencies — see the
  existing `scripts/validate-*.py`). No new dependency is added.
- Run everything from the feature worktree root:
  `/workspace/projects/xFactory/openxFactory-worktrees/001-avc-contract-kernel`.
- Do **not** touch the root checkout or shared release metadata except at the
  serialized realization step.

## 1. Author-time loop (kernel maintainer)

```bash
# Validate the whole kernel: schemas, $ref resolution, registry parity,
# fixtures, acceptance-map parity, evidence register, redaction, digests, F0 gate.
python3 scripts/validate-avatar-client.py --strict
```

**Expected while F0 is pending** (completion state: *implementation complete,
publication pending F0*): the validator reports the semantic surface GREEN and
prints that the publication/tag step is BLOCKED pending F0 `PASS`. Exit code 0
for the non-release checks; the release/tag action is gated separately.

**Expected failures (each must FAIL closed):**
- an unknown member added to any closed registry, or a schema enum drifting from
  its registry file (§D3);
- a denial/terminal fixture carrying an SDP answer or credential (SC-005);
- a committed file containing a real secret pattern, or a synthetic sentinel that
  is not the declared bounded form (SC-008);
- an acceptance-map scenario with no evidence-register entry, or a manual entry
  with no recorded result, or a deferred entry with no owner + fail-closed
  default (SC-003);
- an illegal evidence-register status transition (§D5).

## 2. Acceptance-map / evidence traceability check

```bash
python3 scripts/validate-avatar-client.py --strict   # includes the parity checks
```
Confirm: 17 requirements / 72 scenarios; 0 unmapped, duplicated, renamed, or
evidence-free; every scenario resolves to fixture evidence, a recorded manual
result, or a named owner + fail-closed default (SC-003).

## 3. Consumer conformance (any language, e.g. the Dart Flutter client)

A consumer does **not** need the Python validator (SC-009). Given a pinned
release (exact commit + per-file digests):

1. Verify each pinned file's SHA-256 matches the manifest digest.
2. Read `contracts/avatar-client/fixtures/index.yaml`.
3. For each fixture-case: load `instance`, validate it against the named
   `target` schema/registry with any conformant **draft 2020-12** implementation,
   and assert the case's `expect` (`valid`/`invalid`).
3. A consumer PASSES when 100% of cases meet their declared `expect`; its own
   models validating against the same schemas prove non-drift (SCO-001-S04).

Expected: a tag-only pin (no commit + digests) FAILS conformance (SC-006).

## 4. F0 publication gate (realization prerequisite)

The gate reads F0 evidence but the F0 sibling **owns** its schemas. Before
honoring `PASS` the validator (per `interface-lock.yaml` → `f0_evidence_pin`):

1. resolves pinned `f0-results.schema.yaml` / `f0-interface-impact.schema.yaml`
   from the F0 change path;
2. checks the F0 source commit + both schema SHA-256 digests match the pins;
3. validates the consumed evidence instances against those pinned schemas;
4. reads `PASS` and confirms every interface variance is dispositioned.

Fails closed (tag blocked) on missing schema, digest/commit mismatch, instance
validation failure, unknown status, or unknown variance field (SC-007/SC-010).

## 5. Realization (only after F0 PASS) — serialized final step

```bash
# 1. Allocate next minor after contract-v1.6 → contract-v1.7 (never reserved early)
# 2. Atomically update shared release metadata:
#      contracts/manifest.yaml  (avatar-client entries + per-file sha256)
#      contracts/CHANGELOG.md   (contract-v1.7 entry)
#      contracts/README.md      (avatar-client family in doc index)
# 3. Re-run the gate green, then publish the annotated tag from the realized commit:
python3 scripts/validate-avatar-client.py --strict
#      git tag -a contract-v1.7 -m "avatar-client contract kernel v1.7"
# 4. Record per-file digests + handoff (release tag, commit, digests,
#      interface-lock digest, acceptance-map digest) for the siblings.
```

Completion state becomes *realized*; only then may the OpenSpec change archive
(FR-034). Before publication, rollback = delete the unreleased contracts; after
publication, rollback = a new additive/breaking release under the versioning
policy.

## 6. Gate integration (constitution Principle V)

`validate-avatar-client.py --strict` MUST pass before any push, alongside
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict` and `git diff --check`.
Installed DomainxFactory validators are compatibility observations: a regression
introduced by this change is blocking; dated pre-existing domain debt is not.
