# workstation-intake Specification

## Purpose

Define the product and authority boundary for xFactory workstation intake:
device eligibility, recorded owner and tenant authorization, the handoff
into a supported Microsoft enrollment experience, verification by the owning
tenant that management and compliance actually took, and installer release
evidence. Fix which repository owns which part, so that an independently
released public installer never absorbs canonical policy or tenant authority
— openxFactory owns the intake, consent, enrollment-routing and evidence
contracts, the neutral installer repository owns the implementation and its
own build, certification and release lifecycle, OpsxFactory owns tenant
Intune and Graph administration, and CloudPC-Install owns host eligibility
and required end state. Keep the shipped product honest about what it is and
what it holds: it inspects only authorized non-secret device facts, never
presents itself as an MDM authority, never carries reusable tenant
enrollment authority or credential material in its package, and every
release states truthfully which product state it has reached alongside its
source revision, contract compatibility, validation evidence, distribution
channel and signing authority.
## Requirements
### Requirement: Neutral workstation-intake product boundary
The xFactory workstation-intake implementation SHALL live in an independently
versioned neutral installer repository. openxFactory SHALL own canonical intake,
consent, enrollment-routing, and evidence contracts; OpsxFactory SHALL own
tenant Intune and Graph administration; and CloudPC-Install SHALL own host
eligibility and required end state.

#### Scenario: Workstation-intake behavior is implemented
- **WHEN** application code, packaging, Store metadata, or client validation is introduced
- **THEN** it MUST live in the neutral installer implementation repository
- **AND** it MUST reference rather than redefine the owning openxFactory contract

#### Scenario: Tenant administration is required
- **WHEN** enrollment needs an Intune policy, Graph grant, compliance assignment, remediation, or tenant credential
- **THEN** the operation MUST remain under OpsxFactory or the authorized tenant administrator
- **AND** the installer repository MUST NOT contain the credential material

### Requirement: Enrollment handoff authority
The workstation-intake product SHALL inspect only authorized non-secret device
facts, record owner and tenant authorization, and hand enrollment to supported
Microsoft experiences. It MUST NOT present itself as an MDM authority or embed
reusable tenant enrollment authority in a public application package.

#### Scenario: Eligible unmanaged workstation is accepted
- **WHEN** device, owner, tenant, platform, and handling checks authorize intake
- **THEN** the product MUST select and launch the approved Microsoft enrollment route
- **AND** completion MUST remain pending until the owning tenant verifies management and compliance

#### Scenario: Enrollment credential would enter the package
- **WHEN** a build attempts to include a bulk token, Graph application secret, signing private key, or tenant administrator credential
- **THEN** release validation MUST fail

### Requirement: Truthful product and release state
The installer repository SHALL distinguish repository bootstrap, application
prototype, tested package, Store candidate, and released product states. Every
release SHALL identify its source revision, contract compatibility, validation
evidence, distribution channel, and signing authority without storing secrets.

#### Scenario: Bootstrap repository is pinned
- **WHEN** xFactory first pins the installer repository
- **THEN** the repository MUST report bootstrap status and MUST NOT claim that a WinUI application or Store package exists

#### Scenario: Distribution artifact is released
- **WHEN** an installer artifact is published through Microsoft Store or direct download
- **THEN** its evidence MUST identify source revision, version, channel, validation result, and external signing authority
