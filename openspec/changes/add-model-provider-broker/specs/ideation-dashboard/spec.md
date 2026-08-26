# ideation-dashboard

## ADDED Requirements

### Requirement: Model capability is reached with a broker-minted token
The dashboard SHALL obtain model capability by invoking a configured credential BROKER to MINT a short-lived, scoped token, and SHALL then call the provider with that token directly. The broker SHALL NOT stand in the request path: it holds custody and issues, because a broker between the console and the provider adds a hop to every turn and to every chunk of a streamed one, which is the wrong place to spend latency in an interactive authoring surface.

The broker invocation SHALL be declared by configuration rather than written into code, because the broker (openProfiler) is not yet built and a command line this repository cannot verify must not be frozen into it. When the broker's surface changes, the configuration changes and no code does.

#### Scenario: A model turn mints and calls
- WHEN a model-backed affordance dispatches a turn and a broker binding is configured
- THEN the dashboard invokes the declared broker command to mint a token, and calls the provider with it

#### Scenario: No binding is configured
- WHEN no broker binding exists
- THEN the existing `model_capability_unavailable` refusal is returned unchanged, and the human is told that no model provider is configured

### Requirement: The provider boundary narrows to one module rather than disappearing
Exactly ONE named module SHALL hold a provider endpoint, a provider SDK, or a minted token, and every other module in this repository SHALL remain free of all three. The structural check that today asserts no provider is contacted from anywhere SHALL be rewritten to assert this narrower boundary rather than removed, because a guard that is deleted the first time it becomes inconvenient was never a guard.

The browser SHALL NEVER receive a minted token. The provider call is made from the loopback console process; a token delivered to a page is exfiltratable by anything able to run script there, and the doxBench views hold no transport by construction, which is a property worth more than the hop it would save.

#### Scenario: A view cannot reach a provider
- WHEN any view module is inspected
- THEN it contains no provider endpoint, no provider SDK import, and no token

#### Scenario: A token never crosses to the browser
- WHEN a model-backed affordance runs
- THEN no response to the browser carries the minted token

### Requirement: The dashboard holds bindings, and a minted token outlives nothing
Settings SHALL store a model-provider BINDING — an id, a label, the provider name, the credential reference the broker resolves, the authentication kind, the principal who approved the credential, the provider route the minted token is presented at, and the broker invocation — and SHALL NOT store the API key or OAuth token itself. The provider route is the CONSUMER's declaration because the broker's own declared surface deliberately does not name one: a broker that named an endpoint would be accountable for it, and it refuses to be. A binding is safe to read, log and commit; a long-lived secret is none of those, and the standing rule for this workspace is that machinery holds grant and binding templates only.

When a human supplies a credential, the dashboard SHALL hand it to the broker and retain nothing: the value SHALL NOT be written to any file, held in any state that outlives the request, echoed in any response, or included in any error. What the dashboard keeps is the reference the broker returns.

A MINTED token SHALL live in process memory only. It SHALL NOT be written to any file, included in any response, recorded in any log or error, or survive the process that minted it, and it SHALL NOT be used past the expiry the broker declared.

#### Scenario: A human sets an API key
- WHEN a key is entered in settings
- THEN it is passed to the broker's standard input and the dashboard stores only the returned reference
- AND the key appears in no response, no log line, no snapshot and no file in the checkout

#### Scenario: A minted token expires
- WHEN a token passes the expiry the broker declared
- THEN it is discarded rather than retried, and a further call mints again

#### Scenario: A binding is inspected
- WHEN settings are read back
- THEN the binding's fields are disclosed and no credential material exists to disclose

### Requirement: A broker or provider that cannot answer refuses honestly
A broker that is absent, unconfigured, unreachable, slow, or that returns a malformed answer SHALL produce the same fixed, redacted refusal the model seam already defines, and SHALL state the reason to the human rather than only to a log. A provider that refuses, times out, or rejects the minted token SHALL map onto that same shape, so provider detail never reaches the wire.

A failure SHALL NOT be reported as an empty result, because an empty list of model-proposed subjects is indistinguishable from a model that had nothing to say. A refusal SHALL distinguish a missing capability from a failed call, so a human can tell "nothing is configured" from "it broke".

#### Scenario: The broker fails
- WHEN the broker exits non-zero, times out, or returns unparseable output
- THEN the affordance reports that no token could be minted, distinctly from a model that answered with nothing

#### Scenario: A provider-shaped error never reaches the wire
- WHEN the provider returns an error carrying provider detail
- THEN the refusal disclosed to the browser remains the fixed redacted shape
