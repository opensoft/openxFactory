# Consent-Instrument Examples

Status: draft

Reference examples for the consent-instrument contract schemas under
`contracts/schemas/` (`add-consent-instrument` change, task 1.3). These are
static reference material, not runtime state — see `../README.md` for the
placement policy this directory follows; REAL instrument instances never live
here (record placement is declared domain policy, ruling D9, and signed
originals never enter a product repo at all). The strict canonical validator
is `scripts/validate-consent-instruments.py`; running it with no argument
self-tests every file here (valid pass, each negative fails for its intended
finding, two purpose probes — one resolution, one refusal) and a path argument
scans a checkout for real instances.

## Layout

```text
consent-instrument/
├── README.md                                          # this index
├── consent-instrument-engagement-letter.example.yaml  # executed engagement letter (Ledgerx-shaped):
│                                                      #   estate host as a rung-3 party, free-shape
│                                                      #   delegation access block, revocation SLA,
│                                                      #   credential-grant dependent ref, data_consent none
├── consent-instrument-portal-acceptance.example.yaml  # signature_phase-false class entering executed
│                                                      #   DIRECTLY (D3); consent-profile mapping with
│                                                      #   derivation basis (the Medx pattern, R10)
├── consent-instrument-terminated.example.yaml         # terminated: amendment-as-transition history (D7)
│                                                      #   + cascade_evidence on every dependent ref (R8)
├── consent-instrument-class-registry.example.yaml     # domain-owned CLOSED class registry (D2): evidence
│                                                      #   kinds, signature_phase declarations, the
│                                                      #   active -> executed status alias
├── consent-purpose-model.example.yaml                 # domain purpose model (D4): resolves_to chains the
│                                                      #   validator's purpose probes walk
└── negative/                                          # one violation per file
    ├── embedded-original-content.yaml                 #   custody carries the signed original's content (R9)
    ├── undeclared-lifecycle-skip.yaml                 #   executed with no pending_signatures under a
    │                                                  #     signature_phase-true class (R4/D3)
    ├── class-without-evidence-kind.yaml               #   registry class omits execution_evidence_kind (R3)
    ├── amendment-as-child-instrument.yaml             #   parent_ref record → schema-rejected (R6/D7)
    └── purpose-unresolvable.yaml                      #   scope purpose absent from the purpose model (R7)
```

## Schema → example map

| Schema | Valid example(s) | Negative example(s) |
| --- | --- | --- |
| `consent-instrument.schema.yaml` | `consent-instrument-engagement-letter`, `consent-instrument-portal-acceptance`, `consent-instrument-terminated` | `embedded-original-content`, `undeclared-lifecycle-skip`, `amendment-as-child-instrument`, `purpose-unresolvable` |
| `consent-instrument-class-registry.schema.yaml` | `consent-instrument-class-registry.example` | `class-without-evidence-kind` |
| `consent-purpose-model.schema.yaml` | `consent-purpose-model.example` | (model rules — dangling `resolves_to`, duplicate purposes — are validator findings; no packaged negative) |

## Named cases from the spec

- **An estate host is a party, not a footnote** — the engagement-letter
  example carries `Northwind Estate Systems` at rung 3 with
  `authority_basis: delegated` (the Medxcorp pattern, spec R1).
- **A non-signature class enters executed directly** — the portal-acceptance
  example's class declares `signature_phase: false`, so its trace legally
  starts at `executed`; `negative/undeclared-lifecycle-skip.yaml` is the same
  move under a signature class, refused (spec R4, D3).
- **An amendment preserves the citation target** — the terminated example's
  amendment is a transition entry on `ci-demo-advisory-0003` itself;
  `negative/amendment-as-child-instrument.yaml` models it as a `parent_ref`
  child and is schema-rejected (spec R6, D7).
- **Termination raises the whole chain** — every dependent reference on the
  terminated example carries `cascade_evidence` (spec R8, D5).
- **The Medx derivation is the reference** — the portal-acceptance example
  maps `data_consent` to a consent profile AND declares that profile as a
  dependent reference with its derivation basis; the engagement letter
  declares `mapping: none` explicitly (spec R10, D1).
- **Purpose resolution passes and fails mechanically** — the validator
  self-test probes `reconcile-bank-feeds` (resolves via `bookkeeping`) and
  `payroll-support` (refuses) against the engagement-letter example under the
  purpose model (spec R7, D4). There is deliberately NO negative for a
  delegation clause's technical access shape: that is credential-contracts
  enforcement, one truth per concern.

## Validating locally

```bash
# Self-test all fixtures (positives pass, negatives fail for their declared finding):
python3 scripts/validate-consent-instruments.py --strict

# Scan a checkout for real instances (registry + purpose model found in scope
# adjudicate the instruments beside them, matched by domain):
python3 scripts/validate-consent-instruments.py <repo-path>

# Check one requested purpose against every scanned instrument (spec R7):
python3 scripts/validate-consent-instruments.py <repo-path> --purpose reconcile-bank-feeds
```
