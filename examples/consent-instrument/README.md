# Consent-Instrument Examples

Status: draft

Reference examples for the consent-instrument contract schemas under
`contracts/schemas/` (`add-consent-instrument` change, task 1.3). These are
static reference material, not runtime state — see `../README.md` for the
placement policy this directory follows; REAL instrument instances never live
here (record placement is declared domain policy, ruling D9, and signed
originals never enter a product repo at all). The strict canonical validator
is `scripts/validate-consent-instruments.py`; running it with no argument
self-tests every file here across THREE buckets (valid pass, each negative fails
for its intended finding, each WITHHELD fixture yields the third outcome, two
purpose probes — one resolution, one refusal) and a path argument scans a
checkout for real instances.

**Corpus, MEASURED by listing the directories:** 9 valid examples (7
instruments, 1 class registry, 1 purpose model), 21 indexed negatives, 1
withheld fixture, 2 purpose probes.

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
├── consent-instrument-withdrawn.example.yaml          # WITHDRAWN: the second terminal state, with a
│                                                      #   governed_identity dependent carrying complete
│                                                      #   cascade evidence — credential, identity removal
│                                                      #   AND admission withdrawal (R8)
├── consent-instrument-class-registry.example.yaml     # domain-owned CLOSED class registry (D2): evidence
│                                                      #   kinds, signature_phase declarations, the
│                                                      #   active -> executed status alias
├── consent-purpose-model.example.yaml                 # domain purpose model (D4): resolves_to chains the
│                                                      #   validator's purpose probes walk
├── consent-instrument-custody-chain-header-only.example.yaml
│                                                      # TWO-entry custody chain, both header_only /
│                                                      #   lifecycle_header_edit; locators equal throughout
├── consent-instrument-custody-archive-move.example.yaml
│                                                      # archive_move / path_only: locators DIFFER, digests
│                                                      #   IDENTICAL — the case a single-locator rule cannot
│                                                      #   admit (C-6a)
├── consent-instrument-custody-chain-two-entry.example.yaml
│                                                      # the real repair's shape: e1 archive_move/path_only,
│                                                      #   e2 lifecycle_header_edit/header_only — and the
│                                                      #   EQUAL-TIMESTAMP boundary, admitted
├── withheld/                                          # THE THIRD BUCKET: correct records that WITHHOLD
│   └── custody-content-class-withheld.yaml            #   content-class entry, every internal leg sound →
│                                                      #     neither a pass nor an error; exit 3 for a REAL
│                                                      #     instrument, exempt in the packaged self-test
└── negative/                                          # one violation per file
    ├── embedded-original-content.yaml                 #   custody carries the signed original's content (R9)
    ├── undeclared-lifecycle-skip.yaml                 #   executed with no pending_signatures under a
    │                                                  #     signature_phase-true class (R4/D3)
    ├── class-without-evidence-kind.yaml               #   registry class omits execution_evidence_kind (R3)
    ├── amendment-as-child-instrument.yaml             #   parent_ref record → schema-rejected (R6/D7)
    ├── purpose-unresolvable.yaml                      #   scope purpose absent from the purpose model (R7)
    ├── identity-cascade-incomplete-on-terminated.yaml #   governed_identity with CREDENTIAL-ONLY evidence
    │                                                  #     on a terminated instrument (R8)
    └── identity-cascade-incomplete-on-withdrawn.yaml  #   the same half-cascade on withdrawn — the pair is
                                                       #     what proves both events raise the obligation
```

## Schema → example map

| Schema | Valid example(s) | Negative example(s) | Withheld example(s) |
| --- | --- | --- | --- |
| `consent-instrument.schema.yaml` | `consent-instrument-engagement-letter`, `consent-instrument-portal-acceptance`, `consent-instrument-terminated`, `consent-instrument-withdrawn`, `consent-instrument-custody-chain-header-only`, `consent-instrument-custody-archive-move`, `consent-instrument-custody-chain-two-entry` | `embedded-original-content`, `undeclared-lifecycle-skip`, `amendment-as-child-instrument`, `purpose-unresolvable`, `identity-cascade-incomplete-on-terminated`, `identity-cascade-incomplete-on-withdrawn`, `custody-chain-unanchored-digest`, `custody-chain-unanchored-locator`, `custody-chain-broken-link`, `custody-chain-locator-gap`, `custody-chain-out-of-order`, `custody-pin-rewritten`, `custody-path-class-digests-differ`, `custody-diff-class-unknown`, `custody-reason-unknown`, `custody-entry-missing-ruling-ref`, `custody-entry-missing-recorded-by`, `custody-entry-eleventh-property`, `custody-ruling-ref-blob`, `custody-recorded-by-blob` | `custody-content-class-withheld` |
| `consent-instrument-class-registry.schema.yaml` | `consent-instrument-class-registry.example` | `class-without-evidence-kind` | — |
| `consent-purpose-model.schema.yaml` | `consent-purpose-model.example` | (model rules — dangling `resolves_to`, duplicate purposes — are validator findings; no packaged negative) | — |

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
- **Withdrawal is its own terminal state, never an alias** — the withdrawn
  example carries `status: withdrawn`, not `terminated`; the two are distinct
  events that both raise the cascade obligation, which is why the enum grew by
  a member rather than by an alias (add-client-identity-roster).
- **A governed identity's cascade needs both keys** — a standing identity in
  the consenting party's tenant is held by the identity AND its admission act,
  so its cascade is complete only when both are evidenced; the two
  `identity-cascade-incomplete` negatives are the same credential-only
  half-cascade on each terminal event, and the finding lands against the
  INSTRUMENT rather than the identity.
- **The Medx derivation is the reference** — the portal-acceptance example
  maps `data_consent` to a consent profile AND declares that profile as a
  dependent reference with its derivation basis; the engagement letter
  declares `mapping: none` explicitly (spec R10, D1).
- **A chain anchors to the pin in BOTH halves, or it is refused** —
  `negative/custody-chain-unanchored-digest.yaml` breaks the digest half and
  `…-locator.yaml` the path half, each with the other half sound; an instrument
  cannot acquire a new anchor, in bytes or in path, by declaring one.
- **A broken digest link is refused, not repaired** —
  `negative/custody-chain-broken-link.yaml`; the check does not fall back to
  comparing HEAD, because a chain whose middle is fiction is not evidence.
- **A locator gap is its own refusal** —
  `negative/custody-chain-locator-gap.yaml` links perfectly in the digests and
  not at all in the paths: the half of the chain an earlier draft of this
  contract could not express.
- **Recorded times may repeat but never decrease** —
  `negative/custody-chain-out-of-order.yaml` decreases and is refused, while
  `consent-instrument-custody-chain-two-entry.example.yaml` carries EQUAL
  timestamps and is admitted, because two entries written in one repair session
  share a recording moment.
- **The executed pin is never written back** —
  `negative/custody-pin-rewritten.yaml` advances `custody.sha256` to a digest
  the chain observed and is nonconformant EVEN THOUGH IT NOW VERIFIES; that is
  the point.
- **A class is a claim under review, not a label** —
  `negative/custody-path-class-digests-differ.yaml` declares `path_only` while
  its bytes moved; the entry is refused rather than silently re-classified.
- **The two enumerations are closed** —
  `negative/custody-diff-class-unknown.yaml` and
  `negative/custody-reason-unknown.yaml`: a novel member arrives as a contract
  question, never as an admitted string.
- **An uncited or unattributed acceptance is refused, and the entry is closed**
  — `negative/custody-entry-missing-ruling-ref.yaml`,
  `…-missing-recorded-by.yaml` and `…-eleventh-property.yaml`. The entry has TEN
  required fields, so the closure fixture carries an ELEVENTH property.
- **The blob guard FOLLOWED the custody facts to their new home** —
  `negative/custody-ruling-ref-blob.yaml` and `…-recorded-by-blob.yaml`. Siting
  the array outside `custody` put the entry's two unbounded free strings beyond
  the family's only "wherever it hides" walk, so the walk was extended over the
  whole entry minus its two digests.
- **The positive chain shapes are three** — an unmoved two-entry `header_only`
  chain, a pure `archive_move`/`path_only` relocation whose digests are equal on
  both sides, and the real repair's two-entry `archive_move` → header edit.
- **WITHHELD is a third outcome, and it is represented rather than merely
  mandated** — `withheld/custody-content-class-withheld.yaml` is CORRECT in
  every internal leg and still does not reach current: a `content` divergence
  means the referent moved, which is grounds for re-execution. A real instrument
  in that state exits **3**, "needs a human decision"; the packaged fixture is
  exempt, so this self-test still exits 0.
- **Purpose resolution passes and fails mechanically** — the validator
  self-test probes `reconcile-bank-feeds` (resolves via `bookkeeping`) and
  `payroll-support` (refuses) against the engagement-letter example under the
  purpose model (spec R7, D4). There is deliberately NO negative for a
  delegation clause's technical access shape: that is credential-contracts
  enforcement, one truth per concern.

## Validating locally

```bash
# Self-test all fixtures across the three buckets (positives pass, negatives
# fail for their declared finding, withheld fixtures yield the third outcome):
python3 scripts/validate-consent-instruments.py --strict

# Exit codes: 0 ok, 1 findings, 2 dependency/harness error, 3 withheld — needs a
# human decision. Errors dominate: an instrument that both withholds and errors
# exits 1, because a malformed record is not a decision for a human to take.

# Scan a checkout for real instances (registry + purpose model found in scope
# adjudicate the instruments beside them, matched by domain):
python3 scripts/validate-consent-instruments.py <repo-path>

# Check one requested purpose against every scanned instrument (spec R7):
python3 scripts/validate-consent-instruments.py <repo-path> --purpose reconcile-bank-feeds
```
