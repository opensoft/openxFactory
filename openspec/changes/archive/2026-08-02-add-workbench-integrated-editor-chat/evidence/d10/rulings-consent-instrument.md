# Consent-Instrument Open-Question Rulings — Brett, 2026-07-31 (live D10 session)

Binding rulings on the four standing open questions of
`ideation/staging/consent-instrument-contract/consent-instrument-contract.md`,
made during the D10 acceptance sitting. To be recorded in the doc itself
(item-level UPPERCASE resolution tokens) through the Step D branch session;
this file is the session-evidence copy.

1. **Delta shape — RULED: new capability + declared mapping.** A new neutral
   `consent-instrument` capability with its own schema under
   `contracts/schemas/`, plus a DECLARED mapping to the consent-profile
   family: the instrument authorizes ACTION, the profile governs DATA.
   (Doc's leaning; Medx's recorded position.)

2. **Signature/execution modeling — RULED: authority-basis first-class.**
   The neutral schema carries the authority basis as first-class; signer and
   execution mechanics belong to domain policy, with
   distinct-signers-across-rungs a SHOULD for related-party cases.
   (Medx's recorded position.)

3. **Amendment lifecycle — RULED: transitions with deltas.** Amendments are
   status transitions carrying deltas on the existing instrument, not new
   instruments referencing a parent. (Medx's position; fits Ledgerx's
   "AR by amendment" first case.)

4. **Executed-instrument check home — RULED: new standalone validator.**
   A new `validate-consent-instruments.py`, hostable outside
   credential-contracts (Medx constraint: no broker).

All four align with the Medx §Feedback positions from the archived
`add-patient-consent-instrument` (2026-07-30) — the second-instantiation
evidence the exit condition required.

## Surfaced unlisted questions (Brett: "surface them for me") — all RULED 2026-07-31

Grounded in divergences between the packet, the Medx canonical spec
(`patient-consent-instrument`), and the real Ledgerx record
(`tenants/ledgerxcorp/clients/medsrx/consent-record.yaml`):

5. **Instrument-class registry — RULED: domain-owned under neutral
   constraints.** Each domain declares its own CLOSED class registry; the
   neutral schema constrains what every class must declare (custody-anchor
   kind, execution-evidence kind). Medx's four medical classes and
   Ledgerx's `internal_beta_authorization` both conform as-is.

6. **Lifecycle — RULED: closed neutral enum + declared aliases.** The
   five-state enum is normative; domain spellings map via a DECLARED alias
   at conformance time (Ledgerx `active` → `executed`); non-signature
   classes (e.g. portal acceptance) may enter `executed` directly —
   class-appropriate skipping, never silent.

7. **Scope-coverage semantics — RULED: purpose-level check; shapes stay
   technical.** The neutral executed-instrument check verifies the
   requested PURPOSE resolves into the record's purposes, which resolve
   into a domain-declared purpose model (Medx pattern). Technical access
   shapes on delegation clauses remain credential-contracts enforcement,
   not re-checked by the consent validator.

8. **Termination/withdrawal cascade — RULED: first-class dependent refs.**
   The record carries declared dependent-artifact references (derived
   consent profiles, credential grants, adapter activations), each governed
   by the record's revocation SLA + evidence obligation; cascade mechanics
   stay in the owning families.

9. **Real-record placement — RULED: originals out; record placement is
   domain policy.** Neutrally mandatory: the signed original never enters a
   product repo (opaque locator + sha256 only). Where the record INSTANCE
   lives (repo tenant tree vs governed store) is declared domain policy
   driven by data sensitivity (Medx: PHI-adjacent → store; Ledgerx:
   corporate → tenant tree acceptable).

When recorded in the packet doc, items 5-9 are ADDED as already-resolved
enumerated items (UPPERCASE resolution tokens), so the doc carries the full
question surface honestly without raising the standing count.
