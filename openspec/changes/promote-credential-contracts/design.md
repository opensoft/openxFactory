# Design: Promote Credential Contracts

## Decision 1: One schema file, kind-discriminated

The five kinds form one contract surface with one consumer set (broker,
validators, doc-health); five files would fragment the manifest for no
isolation gain. oneOf-by-kind keeps single-file pinning and copy semantics.

## Decision 2: Policy kinds stay out (for now)

Ops's approval/revocation/rotation policies are one domain's articulation;
with Ledgerx's parallel tree removed there is no convergent second source.
Skip-with-notice keeps them visible; promotion waits for a second domain or
a deliberate single-origin call, per the candidate rule.

## Decision 3: Shape here, semantics in the access model

Encoding "no raw secrets" as schema is false comfort — schemas cannot see
runtime behavior. The invariants stay in docs/credential-access-model.md
(and someday its enforcement lands in broker implementation conformance);
the schema guarantees the records that carry those obligations are
well-formed and accountable (issuer/approver/expiry/audit required).
