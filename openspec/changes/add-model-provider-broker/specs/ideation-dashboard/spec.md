# ideation-dashboard

## ADDED Requirements

### Requirement: Model capability is reached through a credential broker
The dashboard SHALL obtain any model capability by invoking a configured credential BROKER, and SHALL NOT contact a provider itself. No provider SDK, endpoint, credential or secret name SHALL appear in this repository — the boundary the doxBench slice holds today does not move because a model became available, it moves only in WHO answers.

The broker invocation SHALL be declared by configuration rather than written into code, because the broker (openProfiler) is not yet built and a command line this repository cannot verify must not be frozen into it. When the broker's surface changes, the configuration changes and no code does.

#### Scenario: A model turn reaches the broker
- WHEN a model-backed affordance dispatches a turn and a broker binding is configured
- THEN the dashboard invokes the declared broker command and never a provider endpoint

#### Scenario: No binding is configured
- WHEN no broker binding exists
- THEN the existing `model_capability_unavailable` refusal is returned unchanged, and the human is told that no model provider is configured

### Requirement: The dashboard holds bindings and never secrets
Settings SHALL store a model-provider BINDING — an id, a label, the credential reference the broker resolves, the authentication kind, and the broker invocation — and SHALL NOT store the API key or OAuth token itself. A binding is safe to read, log and commit; a secret is none of those, and the standing rule for this workspace is that machinery holds grant and binding templates only.

When a human supplies a credential, the dashboard SHALL hand it to the broker and retain nothing: the value SHALL NOT be written to any file, held in any state that outlives the request, echoed in any response, or included in any error. What the dashboard keeps is the reference the broker returns.

#### Scenario: A human sets an API key
- WHEN a key is entered in settings
- THEN it is passed to the broker's standard input and the dashboard stores only the returned reference
- AND the key appears in no response, no log line, no snapshot and no file in the checkout

#### Scenario: A binding is inspected
- WHEN settings are read back
- THEN the binding's fields are disclosed and no credential material exists to disclose

### Requirement: A broker that cannot answer refuses honestly
A broker that is absent, unconfigured, unreachable, slow, or that returns a malformed answer SHALL produce the same fixed, redacted refusal the model seam already defines, and SHALL state the reason to the human rather than only to a log. A failure SHALL NOT be reported as an empty result, because an empty list of model-proposed subjects is indistinguishable from a model that had nothing to say.

#### Scenario: The broker fails
- WHEN the broker exits non-zero, times out, or returns unparseable output
- THEN the affordance reports that the model could not be reached, distinctly from a model that answered with nothing

#### Scenario: A provider-shaped error never reaches the wire
- WHEN the broker's output carries provider detail
- THEN the refusal disclosed to the browser remains the fixed redacted shape
