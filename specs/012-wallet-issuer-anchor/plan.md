# Implementation Plan: Wallet Issuer Anchor (S2)

**Branch**: `012-wallet-issuer-anchor` | **Date**: 2026-08-24 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/012-wallet-issuer-anchor/spec.md`

## Summary

First real enforcement of the grant `issued_by` field, scoped to the
review-authority class the ratified intake defines: a named validator constant for
the canonical review act token (`review`) decides class membership from
`scope.acts` content alone; a review-class grant with no `issued_by` fails
`issuer-unrecorded`; a ROOT review-class grant whose issuer is not exactly the
anchored operator token (`Brett Heap`, citing the Human Escalation Contract) fails
`root-issuer-unanchored` with detail pins distinguishing machine-named issuers from
other unanchored values (the legacy org string `opensoft` every existing example
carries does NOT grandfather). Three negative specimens join the packaged corpus,
two new requirement rows (`OXWR-R1`, `OXWR-R2`) keep coverage closure closed in
both directions, and a self-test boundary guard proves non-review grants are
untouched. No schema file, manifest entry, CHANGELOG line, or bundle version is
touched — a composing-capability restriction enforced in the validator only.

## Technical Context

**Language/Version**: Python 3 stdlib + PyYAML + jsonschema (existing validator deps; nothing added)

**Primary Dependencies**: `scripts/validate-openxwallet.py` (canonical two-layer validator); packaged corpus `contracts/openxwallet/examples/` (+ profile); S1's CI wiring (`wallet-validation` pull_request check, made required by operator act post-merge)

**Storage**: N/A (specimens are packaged fixtures; no register exists until S4)

**Testing**: Layer-1 self-test (positives clean, each negative fails for exactly its declared reason, per-requirement coverage closure) + boundary-guard assertion; `pytest tests/wallet_yaml_syntax_gate/` regression; `openspec validate --all --strict`

**Target Platform**: Same checkout CI as S1 — the gate already runs this validator on every PR

**Project Type**: Validator rules-as-code widening + packaged specimens

**Performance Goals**: None beyond existing sweep duration

**Constraints**: Class detection reads scope content ONLY (no other trigger); exact-match anchor, fail-closed, no normalization; child-grant issuer semantics stay with existing attenuation logic (no new child rule); the five packaged positives must pass unchanged; counts asserted at implementation recorded as evidence (SC-002)

**Scale/Scope**: One validator module edit (constants, one check function section, REQUIREMENTS map, docstring rule letter, boundary guard), three specimen YAMLs, spec artifacts. Nothing else.

## Constitution Check

*GATE: PASS before Phase 0; re-checked after Phase 1 design.*

| Principle | Verdict | Notes |
|---|---|---|
| I. Contract-first neutral core | PASS | No schema bytes change; restriction composes on the optional `issued_by` field the schema already declares |
| II. Governed change flow | PASS | Implements ratified substrate item S2 of `add-wallet-carried-review-authority` (its tasks §3.1 scope restrictions honored verbatim) |
| III. Document lifecycle/status | PASS | Spec artifacts under specs/012-wallet-issuer-anchor/; no standing-doc claims altered |
| IV. Schema & artifact discipline | PASS | Specimens follow the negative-fixture header contract (`expected_failure` / optional detail pin / required `requirement:`) |
| V. Validation gates | PASS by construction | Self-test rehearsal is the evidence: negatives fail for their declared reasons; coverage closure asserts 13/13 |
| VI. Versioned releases | PASS | No contracts/ bundle change, no manifest entry, no CHANGELOG line |
| VII. Fail-closed boundaries | PASS | Missing issuer refused; unanchored root refused; whitespace/case drift refused without normalization |

## Project Structure

### Documentation (this feature)

```text
specs/012-wallet-issuer-anchor/
├── spec.md                  # authored & clarified (this branch, landed)
├── clarify-questions.md     # clarify record (landed)
├── implementation-notes.md  # grounding facts + durable relay obligation (landed)
├── checklists/requirements.md
├── plan.md                  # this file
├── research.md              # validator/corpus facts behind the rulings
├── data-model.md            # constants, codes, REQ rows, specimen headers
├── quickstart.md            # run the sweep; author a review-class fixture
└── tasks.md                 # dependency-ordered task list
```

### Source Code (repository root)

```text
scripts/validate-openxwallet.py          # constants beside CUSTODY_REGISTRY_PATH;
                                         # issuer rules in check_grant(); REQUIREMENTS
                                         # += OXWR-R1/R2; self-test boundary guard;
                                         # module docstring gains rule (t)
contracts/openxwallet/examples/negative/
├── grant-review-authority-omits-issued-by.yaml    # OXWR-R1 probe
├── grant-review-root-issuer-is-a-machine.yaml     # OXWR-R2 probe (machine pin)
└── grant-review-root-issuer-says-opensoft.yaml    # OXWR-R2 probe (legacy pin)
```

**Avoid touching**: any `*.schema.yaml`, `manifest`/bundle files, CHANGELOG, the five packaged positives, custody registry.

## Implementation Sequence

FR-001+FR-002 (constants + class detection) → FR-003 (`issuer-unrecorded`) → FR-004 (root anchor + pins) → FR-006 (REQ map rows) → FR-005 (specimens, needs codes live to fail-for-reason) → FR-008 (boundary guard) → FR-007 regression proof (full sweep green, counts recorded).

## Key Technical Decisions

1. **Class marker = vocabulary membership, not naming**: `REVIEW_ACT_TOKEN = "review"` checked against `_hashable_set(scope.get("acts"))`. Presence triggers class membership by design; authors of unrelated grants must not borrow the token (spec edge case).
2. **Anchor as constant + citation, not duplication**: `ROOT_ISSUER_OPERATOR_TOKEN = "Brett Heap"` carries the HEC citation `docs/roles-and-authority.md:103-140` in its comment block — the code points at the standing record.
3. **Detail pins prove branches, not just values**: machine-shaped issuers (resolve to a packaged wallet id OR match a machine-token shape) get the machine-token message; the literal legacy string gets its own wording; everything else gets the generic unanchored refusal. Specimens pin the subject token (machine branch) and the word `legacy` (legacy branch) so each probe proves ITS branch fired.
4. **Missing vs unanchored are sequential, not nested**: absent/falsy `issued_by` reports `issuer-unrecorded` and skips the anchor comparison — an absent value cannot be compared against an anchor.
5. **REQ-ID family `OXW*` precedent**: core `OXW-R*`, profile `OXWA-R*`, now intake `OXWR-R*` — two rows, one per independently probed invariant.
