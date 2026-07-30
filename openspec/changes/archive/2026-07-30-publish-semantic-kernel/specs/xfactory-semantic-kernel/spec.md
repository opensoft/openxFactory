# xfactory-semantic-kernel — publish-semantic-kernel deltas

## MODIFIED Requirements

### Requirement: Neutral semantic kernel ownership
openxFactory SHALL define a domain-neutral semantic kernel that identifies
shared cross-factory concepts and relation primitives while leaving
domain-specific meaning to the owning DomainxFactory. The kernel SHALL
distinguish ontology from taxonomy, record schema, policy, evidence, and
instance knowledge, and it SHALL reference rather than redefine the contracts
that own runtime shape, authority, consent, approval, isolation, and
traceability. Every kernel term SHALL name the contract that owns its runtime
shape. A published kernel term SHALL record cross-factory adoption evidence —
at least two independent resolvable adopters, each an exact DomainxFactory
package identity or shared-subsystem contract identity that specializes or
references the term. The bootstrap window is CLOSED: the kernel's initial
publication is complete (`xf/core` 1.0.0, every term's adoption evidenced
under an accountable governed release), and the active kernel line SHALL
NOT regress to a pending-adoption state. In subsequent kernel revisions a
NEW draft term MAY record pending adoption while the revision is
unpublished, and kernel publication SHALL fail for any term still lacking
its adopters. openxFactory SHALL own kernel revision classification; no
DomainxFactory classifies a kernel change. The kernel's stewardship policy
IS openxFactory's own change governance: the package-level
stewardship-policy document (council, telemetry triggers, quality gate)
remains a Domain Hermes artifact and is deliberately NOT required of the
kernel, whose revisions are gated instead by per-term adoption evidence,
compatibility discipline, and ratified OpenSpec review — the domain
quality-signal vocabulary measures domain telemetry the kernel does not
generate. A kernel-level quality gate MAY be introduced by a future
revision if kernel-level telemetry (for example, cross-domain kernel-term
request pressure) gains governed plumbing worth measuring.

#### Scenario: The kernel publishes without a stewardship-policy document
- **WHEN** the governed kernel release runs and the package inventories no stewardship policy
- **THEN** the quality gate is vacuously satisfied by explicit scoping — not omission — and publication is gated by adoption evidence, the per-term steward act, and the accountable council identity
- **AND** a DomainxFactory package remains subject to the full stewardship-policy machinery unchanged

#### Scenario: A domain specializes a neutral concept
- **WHEN** MedxFactory declares Patient as a specialization of the neutral Subject concept and Treatment as a specialization of Focal Item
- **THEN** the domain package validates without adding either domain term to the xFactory kernel

#### Scenario: The kernel attempts to own a domain term
- **WHEN** a kernel term reaches publication with fewer than two independent resolvable adopters, or names a clinical, accounting, marketing, operations, or engineering meaning with no cross-factory neutral role
- **THEN** kernel publication MUST reject the term with a stable finding
- **AND** review MUST move the term to the owning DomainxFactory rather than admit it under a promise of future adoption

#### Scenario: A kernel revision proposes a new term after first publication
- **WHEN** a kernel revision drafts a new neutral term after the 1.0.0 publication
- **THEN** the term MAY record pending adoption only while the revision is unpublished, and the revision MUST NOT publish until the term's two independent adopters resolve
- **AND** the published kernel line never regresses to a pending-adoption state
