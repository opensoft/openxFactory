# shared-contract-ownership Specification

## MODIFIED Requirements

### Requirement: Tooling hosted in the publisher verifies released bytes, not a declared pin
Neutral tooling hosted inside `openxFactory` SHALL verify the shared contract it consumes by the released BYTES it reads — digest equality against its pinned value, and parity against the consumed checkout's own `contracts/manifest.yaml` — and SHALL NOT require the hosting repository to declare a consumption pin, because the publisher declares no pin on itself. A declared-pin check exists so that a consumer can never read one release while its repository declares another; that gap is real for a domain repo reading a submodule pin and structurally absent for tooling shipping inside the release it reads, and a question the publisher cannot honestly be asked MUST NOT be able to refuse it.

A checkout SHALL be treated as a publisher release only when it carries all of `contracts/manifest.yaml`, `contracts/schemas/`, and the contract family's own validator. Requiring every marker together is what separates a coherent release from a directory that merely contains a file with the right name — the same distinction manifest parity draws for a single schema, applied to the checkout as a whole. A tree missing any marker is NOT a publisher and SHALL take the consumer path with its declared pin intact.

Dropping the declared-pin question MUST NOT weaken any other link. The byte chain SHALL run unchanged and per request, and SHALL refuse on the request that first sees a drifted digest or a manifest disagreeing with its own bytes. Verification remains fail-closed throughout: an unreachable checkout, an absent schema, a digest mismatch, and a manifest disagreement each mean nothing may be treated as contract-conformant, and none of them may resolve to an implicit pass.

Nothing here changes how a consuming repository pins. A domain or install repo SHALL continue to declare the openxFactory release it consumes in its own `stack.yaml`, and tooling reading a contract from a checkout other than its own host SHALL continue to require that declaration.

A THIRD case SHALL be read into the same rule where `openxFactory` is the CONSUMER of an EXTERNAL neutral product rather than the publisher of the contract it reads. There the DECLARED PIN is `contracts/<product>-pin.yaml` — a reverse-direction pin that the `stack.yaml` rule above does not reach, because `openxFactory` declares no `stack.yaml` consumption pin on a product it does not publish — and the byte chain, the fail-closed rule and the manifest-parity obligation SHALL run UNCHANGED against it: digest equality against the pin's recorded per-file `sha256`, parity against the pinned checkout's own `contracts/manifest.yaml`, and refusal on the request that first sees a drifted digest, an uninitialized checkout, or a manifest disagreeing with its own bytes. Shedding a contract family's own validator also removes a PUBLISHER MARKER for that family, so a tree that no longer carries it SHALL take the consumer path with its declared pin intact — which in this direction means the product pin, not `stack.yaml`.

#### Scenario: Tooling runs from a publisher checkout
- **WHEN** relocated neutral tooling loads a shared contract from the openxFactory checkout it is hosted in
- **THEN** the released bytes MUST be verified by digest and manifest parity
- **AND** the absence of a `stack.yaml` in that checkout MUST NOT refuse the load

#### Scenario: A consuming repository reads the same contract
- **WHEN** a domain or install repo consumes a shared contract from a pinned openxFactory checkout
- **THEN** its own declared `stack.yaml` consumption pin MUST still be required and MUST still be checked against the pinned release

#### Scenario: A release byte has drifted
- **WHEN** a consumed schema's bytes no longer hash to the pinned digest, or the checkout's manifest records a different digest than its own bytes
- **THEN** the load MUST refuse on the request that sees it
- **AND** publisher mode MUST NOT exempt it

#### Scenario: A tree only looks like a release
- **WHEN** the hosting repository carries some but not all of the publisher markers
- **THEN** it MUST NOT be treated as a publisher release
- **AND** the declared-pin requirement MUST apply to it unchanged

#### Scenario: A refusal reason cannot be established
- **WHEN** the consumed checkout cannot be resolved at all
- **THEN** verification MUST fail closed rather than treat the unanswered question as a pass

#### Scenario: openxFactory consumes an external neutral product
- **WHEN** neutral tooling in `openxFactory` reads a contract family published by an external neutral product repository that `openxFactory` pins
- **THEN** the DECLARED PIN it is checked against is `contracts/<product>-pin.yaml` rather than a `stack.yaml` consumption pin
- **AND** the byte chain, the fail-closed rule and the manifest-parity obligation apply unchanged, so the absence of a `stack.yaml` entry for that product MUST NOT be read as an exemption from any of them
