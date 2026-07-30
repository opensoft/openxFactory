## MODIFIED Requirements

### Requirement: Context Packets Bound Runtime Memory
The system SHALL provide bounded context packets for Hermes and Omnigent
runtime use instead of exposing unrestricted Subject Hermes memory,
unrestricted expert knowledge DB access, or an unrestricted domain ontology
corpus. When semantic classification, normalization, retrieval, or inference
is included, the packet SHALL identify the exact bounded semantic-context
artifact and its kernel, domain ontology, and approved tenant-binding pins.

#### Scenario: Context packet created for active workflow
- **WHEN** Hermes requests context for an active workflow
- **THEN** the gateway MUST use workflow purpose, subject-safety profile, consent, privacy, authority, current state snapshot refs, redaction policy, source trace refs, and any required pinned semantic context to build the context packet

#### Scenario: Omnigent receives memory context
- **WHEN** Omnigent needs customer-subject context for an approved job
- **THEN** Omnigent MUST receive a bounded context packet from Hermes or xFactory rather than direct unrestricted provider access

#### Scenario: Omnigent receives expert knowledge context
- **WHEN** Omnigent needs expert knowledge context for an approved job
- **THEN** Omnigent MUST receive a bounded expert context packet from xFactory rather than direct unrestricted DB, vector index, graph, source workspace, or ontology-corpus access

#### Scenario: Semantic context is included
- **WHEN** a context packet contains domain terms, mappings, classifications, or semantic relations
- **THEN** it MUST carry the exact semantic-context ID and digest plus the kernel and domain ontology package identities used to interpret them
- **AND** a packet whose semantic context fails digest verification, names a package the installation does not pin, or references a retired package MUST be rejected before provider I/O

#### Scenario: Context packet expires
- **WHEN** a context packet's declared TTL has elapsed
- **THEN** the packet MUST be invalid as workflow input and a new packet request MUST re-run the rails

#### Scenario: Context packet used for a different purpose
- **WHEN** a context packet issued for one workflow purpose is presented as input to a different workflow or purpose
- **THEN** the consuming surface MUST reject the packet and request a new packet for the actual purpose

#### Scenario: Packet-derived worker memory inherits redaction class
- **WHEN** an Omnigent worker stores content derived from a context packet in worker-local memory such as AgentMemory
- **THEN** the stored derivative MUST inherit the packet's redaction class and subject refs, and storing packet-derived content above its redaction class MUST be treated as a rail violation

#### Scenario: Ontology inference suggests a permitted operation
- **WHEN** semantic context classifies or infers a relationship that could affect retrieval, routing, promotion, or external action
- **THEN** the gateway MUST still run the existing consent, privacy, source-authority, binding, grant, purpose, redaction, promotion, and audit rails and MUST NOT treat the inference as authority
