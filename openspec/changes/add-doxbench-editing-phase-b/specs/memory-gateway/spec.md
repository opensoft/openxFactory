# memory-gateway

One ADDED requirement, and the honest reason it is needed rather than avoided.

The gateway's M0 set is written for consumers that have a CUSTOMER SUBJECT and
a CREDENTIALED PROVIDER: consent profiles, the subject-safety rail, provider
bindings and short-lived grants, provider mapping between canonical Customer
Hermes objects and provider refs. A governed retrieval consumer with neither —
an authoring surface assembling bounded context packets over its own repository
corpus, backed by an in-process local index — can today only claim conformance
while quietly skipping half of M0, or decline the contract and lose its
vocabulary. Both readings are worse than the truth. This requirement makes the
inapplicability DECLARED and auditable. It grants no exemption, relaxes no
rail, and is refused to any consumer that holds a provider credential or
acquires a subject scope.

## ADDED Requirements

### Requirement: Subject-Free Local Consumers Declare Their Inapplicable Rails

The system SHALL permit a governed memory consumer that has NO customer subject
and NO credentialed provider to declare itself a SUBJECT-FREE LOCAL CONSUMER
CLASS, and that declaration SHALL NAME every rail it declares inapplicable
together with the reason, so an inapplicable rail is a recorded decision rather
than an unexplained absence. The declaration SHALL NOT reduce what remains
applicable: such a consumer SHALL still route governed access through the
gateway, run its rails before provider I/O, express its retrieval backends as
provider profiles behind canonical product-neutral ports, bound its runtime
memory in context packets that declare purpose, sources, scope, and expiry,
keep worker-local or harness-local memory separate and non-authoritative, and
promote only through explicit review. The declaration SHALL be REFUSED to any
consumer that holds or can read a provider credential, that addresses a
customer subject, or that routes to a networked provider — for those the full
tier applies, and a consumer whose scope later acquires any of them SHALL LOSE
the declaration and satisfy the tier before it may continue. Where such a
consumer's promotion target is not a Hermes memory layer, the promotion
requirement SHALL be satisfied by the reviewed act that creates the target
object, and the declaration SHALL name that act — promotion stays explicit and
reviewed, and what changes is the target, never the gate. A subject-free
consumer SHALL NOT be treated as conformant to a tier whose requirements it
declares inapplicable: it declares the tier it meets and the rails it does not
carry, and conformance validation SHALL read the declaration rather than infer
conformance from silence.

#### Scenario: An authoring surface declares the class

- **WHEN** an authoring surface assembles bounded context packets over its own
  repository corpus using an in-process local index, with no customer subject
  and no provider credential anywhere in its path
- **THEN** it MAY declare the subject-free local consumer class, naming consent,
  subject-safety, provider bindings and grants, and provider mapping as
  inapplicable with the reason
- **AND** it MUST still bound its packets, run its rails before I/O, express its
  backends as provider profiles behind the canonical ports, and promote only
  through review

#### Scenario: A declared rail is skipped without being named

- **WHEN** a consumer declares the class but does not name a rail it is not
  running
- **THEN** validation MUST fail — the class exists to make the absence
  auditable, and an unnamed absence is the thing it replaces

#### Scenario: The consumer acquires a credential or a subject

- **WHEN** a declared subject-free consumer gains a provider credential, a
  networked provider route, or a customer-subject scope
- **THEN** it MUST lose the declaration and MUST satisfy the applicable tier's
  requirements before continuing
- **AND** the previously declared inapplicability MUST NOT survive as a
  standing exemption

#### Scenario: Promotion targets an object outside the Hermes layers

- **WHEN** a subject-free consumer promotes a finding into a reviewed object
  that is not a Hermes memory layer
- **THEN** the promotion requirement is satisfied by that reviewed act, which
  the declaration MUST name
- **AND** automatic durability without review MUST remain refused

#### Scenario: Conformance is inferred from silence

- **WHEN** a consumer presents no declaration and no failing rail
- **THEN** validation MUST NOT infer conformance — a tier claim is read from the
  declaration, never from the absence of a complaint
