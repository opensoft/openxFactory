# Implementation Plan: The Register and Its Reader (S4)

**Branch**: `014-register-and-reader` | **Date**: 2026-08-25 | **Spec**: [spec.md](./spec.md)

**Input**: Tasks §5.1–5.3, §5.5 of ratified `add-wallet-carried-review-authority`.

## Summary

The capability's own ratification condition lands: the intake register (one
kindless file at a fixed path, ONE MVP row) and its reader, together, inside
the ALREADY-required `wallet-validation` check - plus the first root
review-authority grant that makes the row something other than "documentation
that confers nothing". The reader enforces the shape D11 declined to schema-ize:
strict row fields, wallet/grant resolution and reconciliation, COMPUTED expiry
(N8 - stored state is never truth), act-tier attestation coupling (013's
recorded obligation), a minimal-shape bound, and the inverted headline: an
active REVIEW-class grant with no backing active row refuses. Absent register
with no review grants stays clean, so every not-yet-cold-started consumer repo
remains conformant.

## Technical Context

**Language/Version**: Python 3 stdlib + PyYAML (existing validator deps; nothing added)

**Primary Dependencies**: `scripts/validate-openxwallet.py` (extended);
`.github/workflows/wallet-validation.yml` (S1's REQUIRED check runs it);
`governance/review-authority/{wallets,attestations}/` from 013

**Storage**: two new live instances (`register.yaml`, `grants/grant-mrc-0001.yaml`)
+ reader code. No contract bytes (D11).

**Testing**: layer-1 self-test gains EIGHT synthesized-tree probes (a kindless
register cannot be a packaged-corpus fixture - the synthetic trees ARE the
negative coverage); live mutation probe through production wiring (run once,
restored); full sweep; pytest syntax gate; openspec strict.

**Constraints**: reader strictness IS the schema; empty `rows` must NOT early-return
(the headline obligation still evaluates); absent-register semantics split by
review-grant presence; base drifted +5 commits since branch point (#340 et al.)
with ZERO overlap on touched files.

**Scale/Scope**: one validator section (~200 lines incl. self-test block), three
governance files, eight packet documents. Zero contract/workflow edits.

## Constitution Check

| Principle | Verdict | Notes |
|---|---|---|
| I. Contract-first neutral core | PASS | Consumes shipped schemas + custody registry; adds none (D11) |
| II. Governed change flow | PASS | Realizes §5 of the RATIFIED change; operator rulings recorded |
| III. Document lifecycle/status | PASS | Packet under specs/014-register-and-reader/ |
| IV. Schema & artifact discipline | PASS | Kindless register enforced by reader; instances outside examples/ |
| V. Validation gates | PASS by construction | Sweep + 8 probes + live mutation + pytest + openspec |
| VI. Versioned releases | PASS | No manifest entry, no CHANGELOG line, no bundle cut |
| VII. Fail-closed boundaries | PASS | Unparseable/malformed refuse loudly; computed expiry over stored state |

## Project Structure

### Documentation (this feature)

```text
specs/014-register-and-reader/
├── spec.md · plan.md · research.md · data-model.md
├── quickstart.md · tasks.md · implementation-notes.md
└── checklists/requirements.md
```

### Source (repository root)

```text
scripts/validate-openxwallet.py                     # rule (u) + check_register
                                                    # + _load_attestations +
                                                    # repo_scan wiring + probes
governance/review-authority/register.yaml           # FR-001/002 — kindless
governance/review-authority/grants/grant-mrc-0001.yaml   # FR-003 — first root grant
```

**Avoid touching**: `contracts/**`, `.github/**`, existing wallets/attestations,
README active-changes list.

## Implementation Sequence

Reader first (self-test probes prove every code before any live artifact
depends on it) → live register + grant → production-wiring mutation probe →
full gates → PR.

## Key Technical Decisions

1. **Ride the existing required check** (req 2 explicitly blesses "or the
   register's own validator" living in the named validator): extending
   `validate-openxwallet.py` gives the reader S1's required-check status for
   free - zero new workflow plumbing.
2. **Strict field-set equality per row**: without a schema, unknown fields are
   how drift smuggles semantics past the reader; refusal names
   missing-vs-unknown so authors fix precisely.
3. **Empty `rows` does not early-return**: the headline obligation must
   evaluate against an empty register (caught by probe during development -
   the early-return variant silently skipped it).
4. **Inverse obligation as CI form of "fail the convening"**: CI cannot see
   convenings; an active REVIEW-class grant with no backing active row is
   exactly "admitting authority the register never granted".
5. **Attestation coupling fail-loud**: missing OR malformed ⇒ explicit error,
   never silent degrade to the unattested cap (013's recorded S4 obligation).
6. **Absent-register posture splits on review-grant presence**: consumer repos
   stay conformant; cold-started trees cannot lose their register quietly.
