# Design

## Context

The provider base is `a883bbf64f42b2a371ab01c3245945b3a9293397`; its manifest declares `contract-v4.0`. This is observed authoring evidence, not a release reservation or runtime pin. The old candidate on branch `026-add-resolved-council-seats` is preserved, not a provider dependency. See [proposal.md](proposal.md).

## Goals / Non-Goals

Deliver one membership answer that survives admission, assignment and completion, with independently checked inputs and independently held seat authority. Domain predicates remain domain-owned; runtime admission remains consumer-owned. Verdict meaning, policy vetoes, ordinary review, human gates, once-per-pin and touched-object guards are preserved.

## Decisions

### D1. One versioned record, not a roster assertion

The new family carries a closed `council_convening` record: existing council identity, subject pin and packet references; explicit protocol identifier; `required_seats`; and `required_seats_provenance`. The provenance contains candidate repository, positive pull number and lowercase full head; governed rule repository, normalized relative path and immutable full revision; matched class; predicate identifier and typed parameters; normalized facts actually consumed. Reject extra keys, duplicate seats, reordered results, empty membership, traversal paths, unavailable Git objects and secret-bearing facts. Reuse the provider's existing digest construction by reference; do not mint another canonicalization.

The consumer fetches the cited immutable rule, verifies that it is an admitted governed rule, independently authenticates the candidate/fact source, and reproduces its roster. An existing Git commit is insufficient authority. The closed predicate registry and input type contracts are shared specifications and vectors; independent implementations are required. No importing codexFactory's evaluator into Hermes, opaque Boolean conclusion, mutable branch reference or digest-only rule reference.

### D2. Membership is checked before transactionally frozen assignment

Admission validates the ordered roster and candidate head before creating the convening, immutable provenance snapshot, or any assignment. The transaction creates exactly one assignment for every required seat and no others; a unique `(convening, seat)` constraint handles simultaneous retries. Idempotent repeats return the existing identical assignment; conflicting repeats refuse. Completion reads the stored roster and protocol, never today's rule or council membership.

A new rule or PR head does not mutate an admitted snapshot. A later head requires another convening; a verdict for an earlier head never authorizes the new head. Keep existing independently resolved subject-pin verification: the producer's immediate pre-submit recheck is an additional guard, not its replacement.

### D3. Registration proves the assignment holder, not a caller label

Each assignment is bound by runtime-held configuration to an independently authenticated job principal, council, candidate pin, permitted signing operation and short lifetime. The trusted dispatcher binds the assignment to verified execution evidence; a bearer principal that can choose arbitrary seat ids is insufficient. GitHub's workflow ref alone cannot distinguish seats. For GitHub-backed jobs the consumer verifies signed issuer/audience/expiry, immutable repository identity, permitted reusable workflow/ref/sha and the runtime's pre-bound job evidence. For governed-host jobs the existing broker must provide equivalent independently verified assignment authority; no general runtime token or all-seat grant is delivered to a seat worker.

The seat job mints one ephemeral Ed25519 key in memory, registers only the public half with proof of possession bound to assignment, council, pin, protocol and key fingerprint, then signs its own return over the same context and canonical return digest. Registration checks the authenticated assignment holder and unique key fingerprint across seats. A signature by an unbound key, a caller-selected seat label, cross-seat replay, reused key, expired authority or a root-key authorization object refuses. Proof of possession alone does not establish the seat's authority. The return uses the existing digest construction and a distinct versioned signing context to prevent cross-protocol replay.

Root keys remain governed authority records where existing wallet policy needs them; this proposal removes root-key material and root-authorization messages from the new seat-worker registration path, not the entire wallet trust chain. Long-lived keys, shared convening keys and key files/artifact transport were rejected because they let one execution act as another seat.

### D4. Workflow claims and OIDC subjects are different fields

The producer binding derives current repository identity from `contracts/policies/repository-identity.yaml`. Its allowed reusable workflow is codexFactory's `council-lane-reusable.yml` at the governed ref and immutable code revision. GitHub exposes `job_workflow_ref` separately from `sub`; the old draft conflated them. See [GitHub's OIDC reference](https://docs.github.com/en/actions/reference/security/oidc).

Bindings must name the actual verified subject template and workflow/job claims; validate them at the identity broker before minting narrowed runtime authority. No unverified JWT decoding, alternate former-owner spelling, configuration wildcard or silent environment-only substitute is accepted. The existing Entra workaround is not claimed to satisfy the stronger lock; if the chosen provider cannot enforce it, activation parks until the broker enforces the full binding and its tests prove it. Identity provisioning is an operator act.

### D5. Deprecate first; then perform a coordinated removal

The provider's current versioning policy requires at least one full minor release with old-shape deprecation warnings before a removal major. Realization allocates the versions under the release lock and regenerates manifest/changelog/inventory from the actual candidate; this proposal reserves no numbers. Successors can implement the new protocol dormant against a reviewed provider commit, but activation waits for published compatible pins and the removal release.

The active binding selects exactly one protocol by configured release and explicit protocol identifier; it never guesses from payload shape or falls back after refusal. Historical records retain their original protocol for audit and verification. During the coordinated change, stop new commissioning, drain or explicitly cancel old in-flight convenings, switch both bindings, run the complete conformance rehearsal, then resume commissioning. Rollback stops intake and restores both prior versions/configurations together; never interpret new records as old or enable both shapes on one active binding. Separate versioned endpoints during a deprecation release do not confer dual-protocol acceptance on the active replacement binding.

## Risks / Trade-offs

- Independent evaluation can drift: one provider corpus, separate implementations, exact corpus digest/pin and rejection agreement before activation.
- Rules or facts cannot be retrieved: fail closed with a named reason; cache only verified immutable objects, never stale mutable heads.
- Job identity does not establish seat scope: require independently verified assignment binding before key registration; this is a release blocker.
- Assignment writes race: transaction plus unique constraint and replay tests.
- Migration interrupts service: documented commissioning pause, explicit old-job disposition and rehearsed paired rollback.

## Migration Plan

Ratify the three linked packets; each then creates exactly one Speckit feature. Realize and publish the provider deprecation release, independently implement and verify successors, publish the removal major, advance successor pins through their normal process, provision verified seat bindings, rehearse, and record coordinated activation. Contract publication, deploying and activating are distinct acts. Archive only on the evidence declared in the proposal.

## Ratification gate

The recommended decisions D1–D5 are fully disclosed in [decision-packet.md](decision-packet.md). No runtime or contract code is authorized by a fabricated ratification record. Implementation task checkboxes belong to the future Speckit features; this packet's tasks cover governance and handoff only.
