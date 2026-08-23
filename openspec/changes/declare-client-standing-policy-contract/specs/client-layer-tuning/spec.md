# client-layer-tuning (delta) — declare-client-standing-policy-contract

## MODIFIED Requirements

### Requirement: Client content shapes are contract-validated
openxFactory SHALL define schemas for `client_policy_overrides`, `client_memory_boundaries`, `client_integration_boundaries`, and the seedable `hermes_client_overlay` (canonical path `config/clients/<client_ref>/overlay.yaml`, declared via the install repo's overlay descriptor, digest-pinned in the install's `client_overlays[]`), with self-testing packaged examples and intended-reason negatives.
The `hermes_client_overlay` schema SHALL additionally declare an OPTIONAL
tenant standing-policy pair — `client.policy_namespace` and `client.policies` —
so that a Tenant layer may carry freestanding company-wide policy and not only
deviations from the domain baseline. Both properties SHALL be optional and
`client.required` SHALL remain `[ref, display_name, policy_overrides]`, so an
overlay that declares neither takes exactly the verdict it took before the pair
existed. The pair SHALL be declared INLINE in the overlay schema rather than in
a per-kind sibling schema file, because neither entry is a self-identifying
sub-document carrying its own `kind` for the validator to dispatch on. The
canonical validator's self-test SHALL sweep every packaged positive example
rather than a hardcoded filename, so a packaged example cannot be published and
never validated.

#### Scenario: Positive examples validate, negatives fail for their reason
- **WHEN** the canonical validator runs its self-test
- **THEN** every packaged positive example — discovered, not hardcoded — passes against the packaged domain baseline, and every negative fails for its declared reason
- **AND** a packaged positive that is never swept is itself a failure of the self-test contract

#### Scenario: The client overlay carries the enforceable tenant slice
- **WHEN** a `hermes_client_overlay` is validated
- **THEN** it carries the client identity, the policy-overrides block with `relation_to_domain: stricter_only`, budget envelopes with the tracking-granularity contract, the approval matrix with its human-ratified auto-clear envelope reference, and the integration boundaries — with no raw secret anywhere
- **AND** it MAY additionally carry the optional standing-policy pair, which is orthogonal to the policy-overrides block in every direction: a document may carry either, both, or neither

#### Scenario: An overlay that declares no standing policy is unaffected
- **WHEN** a `hermes_client_overlay` that declares neither `client.policies` nor `client.policy_namespace` is validated
- **THEN** no standing-policy rule is reached and the verdict is exactly the verdict the document took before the pair was declared

## ADDED Requirements

### Requirement: Tenant standing policy is address-resolvable and validated
The `client.policies` mapping SHALL be keyed by policy id, and the canonical validator SHALL enforce the address rules the schema shape cannot express, so that `<policy_namespace>/<policy_id>` resolves to exactly one enforceable payload.
Specifically: every key MUST equal its entry's declared `policy_id`; every
entry MUST restate a `policy_namespace` equal to `client.policy_namespace`, so
a materialized row is address-resolvable without joining to a sibling row; no
two entries may claim one address; `client.policy_namespace` MUST be present
and non-empty when and only when `policies` is present; and the policy body
MUST remain open, because enumerating policy names is precisely what stops the
closed seven-key `client_policy_overrides` contract from carrying a named
standing policy. A tenant's standing policy is a POSITION rather than a
deviation, so the pair declares no `relation_to_*` field and is never compared
against the domain baseline.

#### Scenario: A named tenant policy resolves to one payload
- **WHEN** a client overlay declares `client.policy_namespace: N` and a `client.policies` entry keyed `P` whose body restates `policy_id: P` and `policy_namespace: N`
- **THEN** validation passes and the address `N/P` resolves to exactly that payload
- **AND** the payload is self-addressing, so no join to the identity record is needed to resolve it

#### Scenario: An address that disagrees with itself fails closed
- **WHEN** a `client.policies` key differs from its entry's `policy_id`, or an entry's `policy_namespace` differs from `client.policy_namespace`, or two entries claim the same `<policy_namespace>/<policy_id>`
- **THEN** validation fails with a finding naming the entry and the rule violated

#### Scenario: Standing policy without a declared namespace fails closed
- **WHEN** a client overlay declares `client.policies` but no non-empty `client.policy_namespace`
- **THEN** validation fails naming the missing namespace
- **AND** a `client.policy_namespace` declared with no `policies` is inert rather than a failure

### Requirement: A declared standing-policy block is never empty and never carries key material
A `client.policies` block that is DECLARED SHALL be refused when empty rather than treated as absent, and the canonical validator SHALL refuse domain-authority blocks and raw credential values within the `client.policies` subtree.
An empty map would materialize an empty `policy_position` row while readiness
clears on row PRESENCE, reporting a standing-policy veto seat as armed with
nothing behind it. A block that is present but of the wrong type MUST take a
distinct finding naming the real defect rather than the empty-block finding.
The prohibited-content scan SHALL be scoped to the `client.policies` subtree
and MUST NOT be widened to the whole document, because `hermes_client_overlay`
is a released contract and a whole-document scan would change the verdict of
overlays that use none of this block.

#### Scenario: A declared-but-empty block is refused
- **WHEN** a client overlay declares `client.policies: {}`, or declares `policies:` with nothing under it
- **THEN** validation fails naming the empty block and directing the author to omit it entirely to carry none

#### Scenario: A wrong-typed block says what is actually wrong
- **WHEN** `client.policies` is present but is a list or a scalar
- **THEN** validation fails with a finding naming the required mapping shape, distinct from the empty-block finding

#### Scenario: Key material inside the block is refused, however deep
- **WHEN** a credential-shaped key carries a value, or a raw-secret marker appears, anywhere beneath `client.policies`
- **THEN** validation fails naming the dotted path, because a tenant overlay carries policy and never key material
- **AND** reference-delivered credentials remain expressible, because no `*_ref` or `*_binding` key is prohibited

#### Scenario: The domain's enforceable slice cannot be legislated from the tenant seat
- **WHEN** `authority_boundaries`, `approval_scope_kinds`, or `required_approval_fields` appears anywhere beneath `client.policies`
- **THEN** validation fails naming the block as the Domain layer's enforceable slice
- **AND** an overlay that carries such a block OUTSIDE the standing-policy subtree keeps the verdict it had before this requirement existed
