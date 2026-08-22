# client-identity-roster (delta) — add-roster-directory-admission-surface

## MODIFIED Requirements

### Requirement: Identities are enumerated by admission surface, not by product name
Governed identities in a client tenant SHALL be enumerated against
**admission surfaces**, where an admission surface is defined extensionally
as a provider-side administrative surface that owns an independent admission
act and its own scoping mechanism. A roster SHALL NOT enumerate identities
against product or marketing names, because provider boundaries overlap
(channel files in a collaboration workload are sites in a content workload)
while admission acts do not. The closed surface vocabulary SHALL be extended
only by the change that governs a new surface, and each surface entry SHALL
name the admission act and scoping mechanism that make it a surface.

#### Scenario: Two product names share one admission act
- **WHEN** two provider product names are administered through a single admission act with a single scoping mechanism
- **THEN** they are one admission surface in the roster
- **AND** an identity serving both is not a spanning identity

#### Scenario: One product name has two admission acts
- **WHEN** a provider product is admitted through two independent admission acts with different scoping mechanisms
- **THEN** each act is its own admission surface

#### Scenario: The device (node-inventory) surface is admitted
- **WHEN** the ratified node-inventory capability governs the device read surface (Entra registered devices, Intune managed devices and Windows 365 Cloud PCs read on one identity, and the provider offers nothing narrower)
- **THEN** `device` enters the closed admission-surface vocabulary
- **AND** its entry names the admission act (admin-consented `Device.Read.All`, `DeviceManagementManagedDevices.Read.All` and `CloudPC.Read.All` on one identity) and the scoping mechanism (tenant-wide read, exact effective scopes, and no narrower provider selector)

#### Scenario: The directory (service-inventory) surface is admitted
- **WHEN** the ratified service-inventory (`managed-service-inventory`) capability governs the directory read surface (the tenant directory and service estate — organization profile, subscribed service plans, applications and domains — read on one identity, and the provider offers nothing narrower)
- **THEN** `directory` enters the closed admission-surface vocabulary
- **AND** its entry names the admission act (admin-consented read-only `Organization.Read.All`, `Application.Read.All` and `Domain.Read.All` on one identity) and the scoping mechanism (tenant-wide read, exact effective scopes, and no narrower provider selector)
