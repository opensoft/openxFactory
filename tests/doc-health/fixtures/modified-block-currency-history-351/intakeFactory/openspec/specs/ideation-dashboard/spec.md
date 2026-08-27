# ideation-dashboard Specification

## Purpose
Canon as it stood on 2026-08-25, carrying ONLY the requirement under test.
Recovered verbatim at bcfc26a0 — see ../README.md.

## Requirements

### Requirement: doxBench model catalog and provider boundary
The dashboard backend SHALL expose a same-origin workbench model catalog whose entries carry a stable opaque model id, human label, provider class, input/output limits, availability, and a human-readable data-handling badge. The catalog MUST NOT expose a provider credential, raw secret, raw endpoint, secret environment-variable name, or provider request template, and the browser MUST NOT call any model provider directly. A chat turn SHALL accept only a model id present and available in the current catalog and SHALL resolve that id through a server-side injected model-provider port whose member surface SHALL remain exactly the three declared members — the adapter-declared timeout, the catalog, and the single opaque dispatch — so that per-turn model selection, harness session handling, and any adapter-internal routing are performed INSIDE an adapter and MUST NOT be added as a fourth provider verb. A catalog entry MAY name a ROUTING RULE this capability owns rather than a single provider model — an `auto` entry that maps a turn to a model by declared role — and such an entry SHALL declare itself as a routing rule with the data-handling badge of the models it may route to, because an entry that hid a routing decision behind a model-shaped id would report a handling posture it does not control. Provider credentials MUST come only from the deployment's approved server-side credential mechanism and MUST NOT enter browser storage, a request body, response body, dashboard snapshot, chat transcript, thread file, log, gate record, git artifact, or exception detail; an adapter that reaches a hosted provider SHALL obtain its credential through the ratified broker lane and MUST NOT hold or read a raw secret of its own. A hosted fallback MAY be offered only when the deployment explicitly enables it and its configured data-handling policy meets the catalog badge; otherwise the model MUST be unavailable. The model catalog and turn routes SHALL be offered only on a loopback human console with a real checkout, resolved actor, and demonstrated console presence; the hosted/read-only plane MUST offer neither route.

#### Scenario: The browser loads model choices
- **WHEN** local doxBench opens with one or more allowed providers configured
- **THEN** the selector MUST show exactly the available catalog entries and their data-handling badges
- **AND** no credential or raw provider endpoint MUST be present in the page or catalog response

#### Scenario: The menu offers a routing rule
- **WHEN** the catalog offers an `auto` entry that this capability resolves to a model by role
- **THEN** the entry MUST declare itself a routing rule and carry the handling badge of every model it may route to
- **AND** the resolved model MUST be recorded on the turn, so a transcript names the model that actually answered

#### Scenario: No model is configured
- **WHEN** the model catalog is empty
- **THEN** the chat rail MUST explain that no allowed model is configured
- **AND** every loaded editor MUST remain usable

#### Scenario: An unknown model id is submitted
- **WHEN** a chat request names a model id absent from or unavailable in the current catalog
- **THEN** the server MUST refuse before any provider call

#### Scenario: A fourth provider verb is proposed
- **WHEN** any realization would add a port member beyond the declared three to carry model switching, session handling, or harness control
- **THEN** it MUST be rejected — that behavior belongs inside an adapter, and a fourth member is a second provider verb by another name

#### Scenario: A browser attempts a direct provider call
- **WHEN** the dashboard bundle or runtime would contact a model endpoint other than the same-origin workbench routes
- **THEN** the renderer boundary MUST fail validation and the call MUST NOT ship

#### Scenario: Hosted doxBench is opened
- **WHEN** doxBench runs on the hosted plane
- **THEN** the model catalog and turn capabilities MUST be absent
- **AND** no chat or editor control implying unavailable authority MUST be reachable

