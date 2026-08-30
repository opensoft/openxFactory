# Contract: Resolved Council-Convening Envelope

Status: draft planning contract

## Purpose

Define the neutral, versioned artifact a trusted DomainxFactory producer submits
before a consumer may admit a per-candidate council. The contract standardizes
the resolved roster and reproducible provenance, not candidate-domain rules,
provider APIs, orchestration storage, or signing implementation.

The realization target is:

`contracts/council-convening/resolved-council-convening.schema.yaml`

## Required Shape

```yaml
schema_version: 1
kind: resolved-council-convening
convening_id: candidate-123-council
required_seats:
  - domain-policy
  - client-interest
  - customer-protection
required_seats_provenance:
  candidate:
    repository: example/candidates
    pull_request: 123
    head_revision: 0123456789abcdef0123456789abcdef01234567
  governed_rule:
    repository: example/governed-rules
    path: candidate-classes/ordinary.yaml
    revision: 89abcdef0123456789abcdef0123456789abcdef
    matched_class: ordinary-change
  normalized_facts:
    touches_company_policy: false
  resolution:
    standing_seats:
      - domain-policy
      - client-interest
      - customer-protection
    conditional_seats:
      - seat: company-policy
        condition_ref: pull-in-company-policy
        required: false
```

Example names and facts are illustrative domain data, not neutral enumerations.

## Normative Validation

1. Validate the complete document against the closed Draft 2020-12 schema.
2. Resolve `governed_rule` at its exact 40-hex revision. Resolution must produce
   exactly one governed rule object and its matched class.
3. Obtain the authoritative current head for the named candidate and require it
   to equal `candidate.head_revision`.
4. Validate normalized facts against the cited rule's fact requirements.
5. Independently evaluate every declared conditional seat. Require the producer
   `required` value to match the independent result.
6. Build the expected set from all standing seats plus independently true
   conditional seats.
7. Require `required_seats` to be unique, declared, and set-equal to the expected
   set. Preserve producer order after validation.
8. Freeze the complete roster and provenance atomically before issuing jobs.

The portable openxFactory validator performs steps 1, 6, and 7 directly and
executes steps 2 through 5 against deterministic fixture-supplied rule/head
resolvers. A production consumer supplies its own independent immutable-object
resolver and domain evaluator; it does not call producer implementation code.

## Refusal Semantics

Validation refuses rather than defaults, infers, or reconstructs when:

- the roster is absent, empty, malformed, duplicated, unknown, or incomplete;
- provenance supplies a conclusion without exact rule/candidate/fact inputs;
- the immutable rule cannot be loaded uniquely;
- a consumed condition fact is absent or invalid;
- current candidate head differs from the recorded head;
- producer and independent condition outcomes differ;
- final and independently reproduced roster sets differ.

Stable primary finding codes are defined in `data-model.md` and pinned by the
conformance index. Additional diagnostics may be emitted but cannot replace the
declared primary code.

## Non-Goals

- Standardizing candidate-class identifiers, fact names, or condition syntax.
- Fetching GitHub or another provider from the neutral validator.
- Defining Hermes database tables or codexFactory workflow jobs.
- Carrying private keys, OIDC tokens, credentials, or raw provider payloads.
- Accepting an obsolete payload or reconstructing `required_seats` after cutover.
