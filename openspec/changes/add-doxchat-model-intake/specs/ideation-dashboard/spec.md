# ideation-dashboard Specification (delta)

Authored relative to the outcome of `add-doxbench-distilled-abstract`
(`release-realization/spec.md:64-74`): the `doxBench model catalog and provider
boundary` block below is THAT change's block — current canon plus its
EVERY-MODEL-CONSUMER widening, its entrypoint-declaration and stateful-adapter
clauses, and its four scenarios — with THIS change's four additions folded in
(the one-non-model-INTAKE-affordance paragraph, the widened `The browser loads
model choices` bullet, the `The intake affordance is submitted as a model`
scenario, and the hosted-plane intake-affordance-absence bullet).

The fold used to run the other way. It was REVERSED on 2026-08-26: this change
has 0/22 tasks done and a real code surface, so it cannot archive for a long
time, and `add-doxbench-distilled-abstract` — realized, with its operator run on
record — archives FIRST. Carrying this change's text inside that one would have
promoted an UNBUILT intake affordance into canon. So that change now carries only
its own additions, and this change, as the LATER archiver, declares relative to
its outcome, which is the direction `release-realization/spec.md:64-74` asks for.
Re-verify this block against canon before archiving.

## MODIFIED Requirements

### Requirement: doxBench model catalog and provider boundary
The dashboard backend SHALL expose a same-origin workbench model catalog whose entries carry a stable opaque model id, human label, provider class, input/output limits, availability, and a human-readable data-handling badge. The catalog MUST NOT expose a provider credential, raw secret, raw endpoint, secret environment-variable name, or provider request template, and the browser MUST NOT call any model provider directly. EVERY MODEL CONSUMER on this surface — a chat turn, and any further consumer such as a per-document derivation — SHALL accept only a model id present and available in the current catalog and SHALL resolve that id through a server-side injected model-provider port whose member surface SHALL remain exactly the three declared members — the adapter-declared timeout, the catalog, and the single opaque dispatch — so that per-turn model selection, harness session handling, and any adapter-internal routing are performed INSIDE an adapter and MUST NOT be added as a fourth provider verb. A catalog entry MAY name a ROUTING RULE this capability owns rather than a single provider model — an `auto` entry that maps a turn to a model by declared role — and such an entry SHALL declare itself as a routing rule with the data-handling badge of the models it may route to, because an entry that hid a routing decision behind a model-shaped id would report a handling posture it does not control. Provider credentials MUST come only from the deployment's approved server-side credential mechanism and MUST NOT enter browser storage, a request body, response body, dashboard snapshot, chat transcript, thread file, log, gate record, git artifact, or exception detail; an adapter that reaches a hosted provider SHALL obtain its credential through the ratified broker lane and MUST NOT hold or read a raw secret of its own. A hosted fallback MAY be offered only when the deployment explicitly enables it and its configured data-handling policy meets the catalog badge; otherwise the model MUST be unavailable. The model catalog and EVERY model-consuming route SHALL be offered only on a loopback human console with a real checkout, resolved actor, and demonstrated console presence; the hosted/read-only plane MUST offer NONE of them. A NEW model consumer SHALL reach the provider through this same seam and MUST NOT be added as a fourth provider verb, MUST NOT open a second provider path, and MUST NOT be smuggled through the chat-turn envelope: a consumer whose request is not a conversation SHALL carry its own request shape and its own declared purpose. The port MUST also be DECLARED AT AN ENTRYPOINT for any consumer to reach a provider at all; where no entrypoint declares one, every consumer's honest posture is an absent capability rather than an error. Where the declared adapter is STATEFUL — a supervised harness child holding per-thread sessions — the declaration SHALL resolve to ONE instance for the life of the served process, and the per-request accessor SHALL return that same instance rather than constructing a new one, because an adapter rebuilt per request cannot hold the one-session-per-document-thread correspondence this capability requires elsewhere and would restart a child on every call.

The selector MAY additionally offer exactly ONE non-model INTAKE affordance, whose behaviour this capability's intake requirements govern. That affordance is not a catalog entry: it carries no model id, it can never be submitted as one, and a chat turn naming it MUST refuse exactly as a turn naming any absent model id refuses. The catalog's own contents remain SERVER-DECLARED — the intake affordance opens a governed path to a new declaration and MUST NOT become one.

#### Scenario: The browser loads model choices
- **WHEN** local doxBench opens with one or more allowed providers configured
- **THEN** the selector MUST show exactly the available catalog entries and their data-handling badges, plus at most the single intake affordance
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

#### Scenario: The intake affordance is submitted as a model
- **WHEN** a chat request names the intake affordance's selector value rather than a catalog model id
- **THEN** the server MUST refuse with the same fixed refusal an absent model id produces, before any provider call
- **AND** no intake-specific failure code MUST be added, because the affordance is not a model and the existing refusal already states the truth

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
- **AND** the intake affordance MUST be absent with them, because a plane that may not run a turn may not enrol a provider either

#### Scenario: A second model consumer is added
- **WHEN** a capability adds a model consumer that is not a chat turn
- **THEN** it MUST resolve its model through the same server-side injected port under the same loopback-console gate
- **AND** the port's member surface MUST remain exactly the three declared members

#### Scenario: A non-conversation request is offered as a chat turn
- **WHEN** a model consumer whose request carries no human message, transcript, or buffer set would ride the chat-turn envelope
- **THEN** it MUST be rejected and MUST carry its own request shape and declared purpose

#### Scenario: No entrypoint declares a model port
- **WHEN** a served process is started by an entrypoint that declares no model-provider port
- **THEN** every model consumer MUST report an absent capability and MUST NOT fail as an error

#### Scenario: A stateful adapter is resolved twice in one process
- **WHEN** two requests in one served process each resolve the model port
- **THEN** both MUST receive the SAME adapter instance
- **AND** no adapter child process MUST be started a second time by the act of resolving

## ADDED Requirements

### Requirement: The model selector offers intake first and defaults to it when nothing is approved

The model selector SHALL render its intake affordance as the FIRST option, ahead of every catalog entry, and SHALL make it the DEFAULT selection when the catalog discloses no available entry. When at least one entry is available the default selection MUST remain a model rather than the intake affordance, because a human who already has an approved model is trying to chat, not to enrol.

The empty-catalog default MUST NOT change what the send control does. Selecting intake is not selecting a model: the send control stays refused for the reason it is refused today, and the rail's existing sentence continues to state that no approved model is configured. Replacing that sentence with an invitation to enrol would trade a true statement of posture for a call to action, and the posture is the fact the human needs.

The intake affordance MUST NOT be offered when the catalog could not be READ. An unreadable catalog and an empty one are different facts with different remedies — the dashboard already distinguishes them — and offering enrolment as the cure for a stale console token or an unreadable answer would send a human to buy a subscription for a bug.

#### Scenario: The catalog is empty

- WHEN the model catalog answers successfully with no entries
- THEN the selector's first option is the intake affordance and it is the selected option
- AND the send control remains refused with the existing no-approved-model sentence unchanged

#### Scenario: An approved model exists

- WHEN the catalog discloses one or more available entries
- THEN the intake affordance remains the first option and an available model is the default selection
- AND choosing a model never requires passing through the intake affordance

#### Scenario: The catalog could not be read

- WHEN the catalog route refuses, or its answer cannot be read
- THEN the intake affordance is not offered
- AND the existing distinguished failure sentence is shown unchanged

### Requirement: Model intake hands the credential to the broker and keeps only a binding

An intake flow that accepts provider authentication SHALL pass the supplied value directly to the declared credential broker and SHALL retain only the reference the broker returns. The dashboard MUST NOT write the value to any file, hold it in any state outliving the request that carried it, echo it in any response, include it in any error or log line, or place it in a snapshot, transcript, gate record, or git artifact. What persists is a binding of the shape `credential-contracts` already owns — provider, secret reference, owner, rotation policy — and a binding is safe to read, log, and commit precisely because it names a secret it does not contain.

The flow SHALL support both authentication kinds a human may hold: a supplied API key, and a delegated OAuth authorization to a provider subscription. For the OAuth kind the dashboard MUST NOT be the party that receives the provider's tokens: it hands the human to the broker's own authorization flow and receives back a credential reference, never an access token and never a refresh token. A refresh token is a refreshable session-state credential, which this workspace's credential capability already refuses to distribute by any channel; keeping it in one custody is what makes the OAuth kind conformant rather than an exception to that rule.

An intake flow SHALL refuse rather than degrade when no broker is declared. A flow that collected a key with nowhere governed to put it would have to hold it somewhere, and every somewhere available to the dashboard is a place this workspace's standing rule forbids.

#### Scenario: A human supplies an API key

- WHEN a key is entered in the intake flow
- THEN it is passed to the declared broker and only the returned reference is stored
- AND the key appears in no response, no log line, no snapshot, and no file in the checkout

#### Scenario: A human authorizes an OAuth subscription

- WHEN the human chooses the OAuth kind
- THEN the dashboard hands them to the broker's authorization flow and receives back a credential reference
- AND no access token and no refresh token is ever delivered to the dashboard or to the browser

#### Scenario: No broker is declared

- WHEN the intake flow is opened on an install that declares no credential broker
- THEN the flow refuses and states that no credential custody is configured
- AND no field that would accept a secret is presented

#### Scenario: The captured value is searched for afterwards

- WHEN the checkout, the plane state, every response, and every log produced by the intake are searched for the supplied value
- THEN it is found nowhere

### Requirement: Intake proposes a model; approval stays a recorded human act

Completing an intake flow SHALL produce a PROPOSED model declaration and SHALL NOT by itself make a model available for turns. The catalog's `available` flag remains the deployment's statement that a model is approved for this console, and a flow that set it would let the act of supplying a payment credential double as the act of approving a provider for governed work. Those are different decisions and the second one is the one the placeholder's word "approved" names.

Approval SHALL be an explicit act by the resolved local human actor, recorded the way this dashboard records every other governed act: a gate action naming the model declaration it approved. Until that record exists the proposed declaration MUST be disclosed to the human as pending and MUST NOT appear as an available catalog entry.

The approval act SHALL carry the accountability the credential capability already requires of an issued grant — who issued, who approved, when it expires, and the audit reference — so that a model added through this flow is answerable in the same terms as any other credential-bearing capability in this workspace.

#### Scenario: An intake completes

- WHEN a human finishes the intake flow successfully
- THEN a proposed model declaration and its binding exist and are disclosed as pending
- AND the catalog discloses no new available entry

#### Scenario: The human approves the proposed model

- WHEN the resolved local human actor approves the pending declaration
- THEN a gate action record naming that declaration is persisted before the entry becomes available
- AND the record carries issuer, approver, expiry, and audit reference

#### Scenario: An agent attempts the approval

- WHEN an agent or automated caller invokes the approval
- THEN it is refused and reported, exactly as every other gate action refuses an agent invocation

#### Scenario: A pending declaration is submitted as a model

- WHEN a chat turn names a model id that is declared but not yet approved
- THEN the turn refuses before any provider call, because the entry is not available

### Requirement: The intake affordance ships with the flow behind it

The intake affordance SHALL NOT be released ahead of the flow it opens. An option that names an action and then does nothing, or opens a surface that cannot complete, is worse than an absent option: it converts a plainly-stated posture the human can act on elsewhere into a dead end inside the control they were told to use.

Where the flow's dependencies are not yet met, the selector SHALL keep its present behaviour unchanged rather than showing a disabled or explanatory intake option, because the rail already carries an honest sentence about the posture and a second, weaker statement of the same fact inside the selector adds nothing a human can use.

#### Scenario: The flow's dependencies are unmet

- WHEN the credential broker this flow requires is not available
- THEN the intake affordance is not rendered at all
- AND the selector and the send control behave exactly as they do before this change

#### Scenario: The flow is available

- WHEN the intake flow can be opened and completed
- THEN the intake affordance is rendered and choosing it opens the flow
