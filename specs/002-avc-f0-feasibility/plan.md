# Implementation Plan: Avatar Brokered-Call F0 Feasibility Experiment

**Branch**: `002-avc-f0-feasibility` | **Date**: 2026-07-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-avc-f0-feasibility/spec.md`, the registered
protocol (`openspec/changes/qualify-avatar-brokered-call-feasibility/supporting-docs/f0-brokered-call-spike-protocol.md`)
and result schema (`.../f0-results.schema.yaml`), and `.specify/memory/constitution.md`.

## Summary

Build a disposable, tenant-data-free Python lab harness under
`experiments/avatar-brokered-call/` that empirically measures whether an OpenAI-brokered
WebRTC call can be created, held under sideband + in-harness control authorization until
media is authorized, and terminated within the required bounds — running the six
authoritative trial groups (F0-A…F0-F, 70 trials) with monotonic instrumentation, an
allowlisted redacting result writer, and a digest-verified read of the baseline acceptance
map for concrete `ACR-*` variance IDs. The harness emits schema-valid, redacted evidence
(`f0-results.json`, `f0-results.md`, `f0-interface-impact.yaml`) solely under the change's
`evidence/` directory, classified `PASS | FAIL | INCONCLUSIVE`. Per the encoded
clarifications, feature completion requires the harness, offline self-tests, redaction
tests, and a schema-valid terminal record — `INCONCLUSIVE` without a lab key is a valid
terminal state, a live `PASS` is not required for completion, and completion never
represents provider qualification.

## Technical Context

**Language/Version**: Python 3.12 (pinned via `.python-version`; the exact minor is fixed in
the dependency lock digest that feeds the candidate profile).

**Primary Dependencies**: `aiortc` (WebRTC peer + audio track + data channel), `websockets`
(sideband WSS control), `httpx` (brokered `/v1/realtime/calls` creation), `jsonschema`
(Draft 2020-12 evidence validation), `PyYAML` (config, acceptance-map, and YAML evidence),
and a pinned offline speech synthesizer for the deterministic audio fixture. All third-party
deps are hash-pinned in a committed lock under `experiments/avatar-brokered-call/`.

**Storage**: Files only. Committed evidence is written directly and atomically under
`openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/`. No database, no local
persistence of provider content, no standing state.

**Testing**: `pytest`. An offline suite (runs with no lab key) covers config rejection,
timing math, cleanup registry, the redaction allowlist, evidence schema validation,
acceptance-map digest gating, fixture determinism, and trial-group/assertion accounting. A
live suite is gated on `OPENAI_API_KEY` presence and is skipped (→ `INCONCLUSIVE`) when
absent.

**Target Platform**: Linux dev/container host with outbound network to the lab provider.
Disposable; no deployment, no listening socket, no standing service.

**Project Type**: Single-project Python CLI experiment harness (owned surface:
`experiments/avatar-brokered-call/` plus the change's `evidence/` directory only).

**Performance Goals**: The harness measures — it does not set — the neutral architecture
thresholds: baseline sideband-verification p95 ≤ 3,000 ms (no trial > 5,000 ms), first
playable output after media authorization p95 ≤ 2,000 ms, revocation terminal-observation
≤ 5,000 ms. Harness instrumentation overhead must stay negligible against these bounds
(monotonic-nanosecond markers, no blocking I/O on the timing path).

**Constraints**: env-only `OPENAI_API_KEY` (never in args/tracked files/evidence); no tenant
data / tools disabled / non-lab profile rejected at preflight; readiness default 3,000 ms /
hard ceiling 5,000 ms; exactly six trial groups (70 trials); deterministic trial IDs;
in-harness simulated control/lease stub (no Hermes/external control plane); one deterministic
digest-pinned audio fixture per harness revision; evidence redaction is fail-closed
(redaction failure ⇒ `FAIL`, no commit); acceptance-map missing/mismatched ⇒ `INCONCLUSIVE`;
all code under `experiments/avatar-brokered-call/`, all committed evidence under the change's
`evidence/` directory.

**Scale/Scope**: One bounded lab workload per run — 70 trials across six groups (F0-A 20;
F0-B…F0-F 10 each). ~12 monotonic offsets recorded per trial (13 timing points from t=0).
Three evidence artifacts per run.

## Constitution Check

*GATE: evaluated pre-Phase 0 and re-checked post-Phase 1 design. Result: **PASS** (two
justified entries in Complexity Tracking).*

| Principle | Assessment | Verdict |
|-----------|------------|---------|
| I. Contract-First, Domain-Neutral Core | F0 defines no canonical contract and no domain content. It reads the baseline acceptance map read-only, records observations and variances, and uses an internal probe envelope it never publishes as a contract. Neutral meaning stays with the sibling contract kernel. | PASS |
| II. Governed Change Flow (OpenSpec before implementation) | The OpenSpec change `qualify-avatar-brokered-call-feasibility` (validated `--strict`) governs this single Speckit feature; `code_surface: openxFactory`, archives only on merged + green evidence. Speckit `tasks.md` (a later phase) owns implementation tasks; the OpenSpec `tasks.md` is the governance handoff — not duplicated here. | PASS |
| III. Document Lifecycle & Status Discipline | The spec is `Draft`; emitted F0 evidence is `record`-class terminal experiment output. No document claims `standard`. No silent status edits. | PASS |
| IV. Schema & Artifact Discipline | The YAML evidence artifact `f0-interface-impact.yaml` and its schema carry `schema_version` + `kind`; JSON-Schema-in-YAML files follow `$schema`/`$id` (see Complexity #2). No raw credentials anywhere. Committed files use repo-relative paths only. | PASS (see Complexity #2) |
| V. Validation Gates (NON-NEGOTIABLE) | Behavior is proven with deterministic, reviewable evidence: an offline test suite + fixtures + schema validation + redaction scans, plus `openspec validate --all --strict` and repo-local validators run before any push. F0 touches no repo-local validator's domain. | PASS |
| VI. Versioned, Content-Addressed Releases | F0 cuts no contract release and allocates no contract version; it only gates the sibling kernel's publication. | PASS (non-goal) |
| VII. Fail-Closed Authority Boundaries | Preflight rejects unrecognized/unsafe config; acceptance-map absence/mismatch fails closed to `INCONCLUSIVE`; provider output is observed, not authoritative — the in-harness control stub owns authorization; committed evidence is redacted by an allowlist. | PASS (strongly aligned) |
| Repo Constraints — shared-tree / worktree mode | Work runs in the feature worktree; commits stage explicit paths only; commit-here-first submodule discipline respected. | PASS |
| Repo Constraints — "runtime code out of scope … nothing deploys, listens on a socket, or holds provider keys" | The harness IS runtime code but is explicitly ratified by the OpenSpec change as a disposable lab experiment. It opens only **outbound** client connections (no listening socket), creates **no** standing service/deployment, and never stores a provider key in the tree (env-only, redacted out of all evidence). | PASS (see Complexity #1) |
| Workflow & Quality Gates | Lifecycle order followed (specify → clarify → **plan** → checklist → tasks → analyze → implement); clarifications encoded (Session 2026-07-11); analyze must be clean before implement. | PASS |

## Project Structure

### Documentation (this feature)

```text
specs/002-avc-f0-feasibility/
├── plan.md              # This file (/speckit-plan output)
├── spec.md              # Clarified feature specification
├── clarify-questions.md # Clarification Q&A record (Accepted Answers)
├── research.md          # Phase 0 output — decisions + rationale
├── data-model.md        # Phase 1 output — entities, fields, state transitions
├── quickstart.md        # Phase 1 output — runnable validation guide
├── contracts/           # Phase 1 output — CLI, evidence, acceptance-map, interface-impact schema
│   ├── cli-interface.md
│   ├── evidence-outputs.md
│   ├── acceptance-map-input.md
│   └── f0-interface-impact.schema.yaml
├── checklists/
│   └── requirements.md  # Spec quality checklist (already passing 16/16)
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (owned surface — created during implementation, not by this plan)

```text
experiments/avatar-brokered-call/          # 002's owned code surface
├── pyproject.toml / requirements.lock      # pinned Python + hash-locked deps (feeds profile digest)
├── .python-version
├── README.md                               # run/redaction/safety notes
├── src/avatar_f0/
│   ├── config.py         # run config model + preflight rejection (FR-001/003)
│   ├── candidate.py      # immutable pinned candidate profile + digest (FR-002)
│   ├── credential.py     # env-only OPENAI_API_KEY loader + safeguards (FR-001)
│   ├── acceptance_map.py # digest-verified baseline map read → ACR IDs (FR-018)
│   ├── clock.py          # monotonic markers (FR-011)
│   ├── control_stub.py   # in-harness simulated control/lease authorization (FR-007)
│   ├── sideband.py       # WSS sideband client
│   ├── broker.py         # /v1/realtime/calls creation + call registry
│   ├── media.py          # WebRTC peer, audio track, held-answer gate
│   ├── fixture.py        # deterministic audio fixture generator + byte digest (FR-002)
│   ├── trials/           # F0-A…F0-F group runners + cross-cutting cleanup/interrupt
│   ├── assertions.py     # ordering / timing / retry / revocation / redaction checks
│   ├── classify.py       # PASS|FAIL|INCONCLUSIVE derivation (FR-016)
│   ├── redaction.py      # allowlist writer + prohibited-content scan (FR-017)
│   ├── evidence.py       # writes results.json / results.md / interface-impact.yaml
│   ├── cleanup.py        # bounded termination of every known call ID (FR-005)
│   └── cli.py            # entrypoint
├── schemas/
│   ├── f0-results.schema.yaml           # 002-owned; digest-matched to the registered copy
│   └── f0-interface-impact.schema.yaml  # 002-owned; newly authored (schema_version + kind)
└── tests/
    ├── offline/          # config, timing, cleanup, redaction, schema, map-digest, fixture
    └── live/             # OPENAI_API_KEY-gated; skipped ⇒ INCONCLUSIVE

openspec/changes/qualify-avatar-brokered-call-feasibility/evidence/   # 002's only evidence home
├── f0-results.json
├── f0-results.md
└── f0-interface-impact.yaml
```

**Structure Decision**: Single Python project confined to `experiments/avatar-brokered-call/`.
The two owned JSON schemas live under `experiments/avatar-brokered-call/schemas/`; the harness
validates its outputs against them, and an offline drift test asserts `f0-results.schema.yaml`
is byte-identical (sha256 `a52f2abe…`) to the registered supporting-docs copy so the owned
source and the OpenSpec-registered snapshot never diverge. Committed run evidence is written
only under the change's `evidence/` directory. These are the only two locations any run writes.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Runtime code (a harness making live WebRTC/WSS/provider calls) under `experiments/`, against "runtime code is out of scope … nothing deploys, listens on a socket, or holds provider keys" | F0's whole purpose is to measure empirical provider behavior that schemas/mocks cannot prove; this is explicitly ratified by the `qualify-avatar-brokered-call-feasibility` OpenSpec change | A mock/schema-only harness cannot answer the feasibility question. The constraint's intent (no deployments, no listening sockets, no keys stored in-tree) is fully honored: outbound-client only, disposable, env-only key redacted from all evidence. |
| JSON-Schema-in-YAML files (`f0-results.schema.yaml`, `f0-interface-impact.schema.yaml`) use `$schema`/`$id` instead of the `schema_version` + `kind` YAML header from Principle IV | The result schema is already registered upstream in this exact JSON Schema form (digest-pinned); the interface-impact schema must match its sibling's convention to validate the same way | Adding `schema_version`/`kind` headers would break JSON Schema tooling and diverge from the registered `f0-results.schema.yaml`. The evidence YAML that these schemas validate (`f0-interface-impact.yaml`) DOES carry `schema_version` + `kind`, satisfying the principle where it applies. |
