# Avatar-Client (AVC) Contract Kernel — Family Index

Status: draft
Kind: avatar-client-contract-family
Ratified by: define-avatar-client-contract-kernel (pending F0 realization)

> This is the **family contract index** for the neutral avatar-client kernel.
> It is distinct from `contracts/README.md` (the repository release-metadata
> index) and the repo-root `README.md` (the repository document index into which
> this family is linked at realization). See plan Design Note 4.

## Canonical contracts (YAML-serialized JSON Schema draft 2020-12)

| ID | File | Purpose |
|----|------|---------|
| — | `shared-definitions.schema.yaml` | Common `$defs` (+ closed speech-gate enum) referenced by every contract |
| AVC-01 | `avc-01-session-request.schema.yaml` | Session request |
| AVC-02 | `avc-02-session-result.schema.yaml` | Discriminated grant / denial / terminal result |
| AVC-04 | `avc-04-session-event.schema.yaml` | Immutable session event (AVC-05 transcript payload) |
| AVC-06 | `avc-06-structured-confirmation.schema.yaml` | Effect-bound confirmation challenge |
| AVC-07 | `avc-07-retention-profile.schema.yaml` | Retention classes (reserved classes forbidden) |
| AVC-08 | `avc-08-persona-profile.schema.yaml` | Session-fixed persona |
| AVC-09 | `avc-09-voice-adapter-descriptor.schema.yaml` | Voice adapter descriptor (server + client components; NO latency budget) |
| AVC-10 | `avc-10-voice-latency-sample.schema.yaml` | Voice latency sample (raw markers, derived intervals, direct-or-brokered) |
| AVC-11 | `avc-11-session-command.schema.yaml` | Sole client→control mutation envelope |
| AVC-12 | `avc-12-state-snapshot.schema.yaml` | Recovery/state snapshot |

AVC-03 (capabilities) is absorbed inline on the AVC-02 grant; AVC-05 (transcript
segment) is an AVC-04 event payload. Both stay RESERVED and are never reused.

AVC-09 and AVC-10 were reserved by this kernel and PUBLISHED at
`contract-v1.46` by `qualify-avatar-live-voice`, from the reserved shapes
unchanged. AVC-09 carries no numeric latency-budget field and no secret
material; AVC-10 carries no raw content. Latency GATING lives in
`acceptance-map.yaml` as exactly one neutral relative-regression SLO entry
(`ALV-SLO-001`) at the ratified threshold — more than 15 percent relative OR
more than 150 ms absolute, whichever is GREATER, on p50 and p95 of
first-playable-after-authorized and sideband-ready, for Windows desktop and web
canvas at nominal network. p99, teardown, degraded and jittered network, and
steady-state per-turn latency are RECORDED and gate nothing; Linux CI is
reference-generation only and is never a gated delivery platform.

## Closed registries

`registries/` holds nine closed vocabularies (session-result-reasons [15],
events, commands, retention-classes, capabilities, interaction-modes,
session-outcomes, fallback-modes, consent-purposes [3]). Each schema enum is
parity-checked set-equal against its registry file. The speech-gate vocabulary
is a closed enum in `shared-definitions.schema.yaml`, not a registry (analyze A3).

## Conformance

- `fixtures/index.yaml` — language-neutral, self-describing fixture suite. Any
  conformant draft 2020-12 implementation can execute it (no Python required).
- `acceptance-map.yaml` — 26 requirements / 107 scenarios (ACR-*/SCO-*/RBG-*/ALV-*)
  plus the single `latency_slo` entry.
- `evidence-register.yaml` — resolves every scenario to fixture evidence, a
  recorded manual result, or a named owner + fail-closed default.
- `scripts/validate-avatar-client.py` — reference runner (reproducible tooling,
  NOT a pinned artifact and NOT a required consumer dependency).

## Consumer pinning (content-addressed)

A consumer MUST pin the **exact openxFactory commit plus the per-file SHA-256
digests** of the released bundle and prove conformance by executing the canonical
fixtures.

- A pin recorded as an **annotated tag alone** (without the commit + per-file
  digests) is NOT a content-addressed pin and MUST fail conformance
  (SCO-001-S03).
- The bundle identity (manifest version, changelog entry, annotated tag, release
  commit, per-file digests) must all identify the same realized bundle
  (SCO-001-S02); a disagreement fails release validation.
- The digested semantic set is: the 10 schemas, `shared-definitions`, the 9
  registries, `fixtures/index.yaml`, `acceptance-map.yaml`, `interface-lock.yaml`,
  and `evidence-register.yaml` (plus any successor deferral-discharge register). The validator and `redaction/` config ship in the
  release commit as tooling but are not per-file-pinned semantic artifacts.

## Completion states

- **implementation complete, publication pending F0** — all artifacts and the
  validator are merged and green and the publication gate is enforced.
- **realized** — F0 is `PASS`, all interface variances are dispositioned, the
  registered threat model is accepted, the annotated `contract-v<minor>` tag is
  published, and the per-file digests are recorded.

The OpenSpec change remains active until *realized*.
