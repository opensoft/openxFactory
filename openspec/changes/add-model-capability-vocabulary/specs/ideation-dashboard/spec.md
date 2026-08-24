# ideation-dashboard (delta) — add-model-capability-vocabulary

## ADDED Requirements

### Requirement: A catalog entry declares the input modalities it accepts, from a closed vocabulary
A workbench model catalog entry's INPUT MODALITIES SHALL be declarable from a CLOSED vocabulary whose members are exactly `text` and `image`, and the declaration SHALL be optional. It exists so that a routing decision can ask whether a candidate can carry what a turn actually contains, rather than inferring capability from a model's name or from its byte limits — which describe how MUCH a model accepts, never WHAT KIND.

Its ABSENCE SHALL NOT be read as a capability claim in either direction: an entry that declares nothing is a producer that predates this vocabulary, and a reader SHALL treat it as text-only for routing purposes while recording that the entry made no declaration. This mirrors the handling-posture rule the chat-turn family already promotes, where absence means "a producer older than the field" rather than a stated posture. Requiring the field instead would break every catalog released before it, which an additive growth must not do.

Where declared, the set SHALL be non-empty and SHALL contain `text`. A model that cannot accept text is not a model this catalog can route a chat turn to, so an image-only declaration describes something the surface has no use for and SHALL be refused rather than stored.

THE VOCABULARY IS CLOSED, AND EXTENDED ONLY BY THE CHANGE THAT GOVERNS A NEW MEMBER. A modality enters when a real consumer needs it — the same rule this family already applies to the client-identity roster's admission surfaces, where a member enters with the ratified change that governs it rather than because a capability is imaginable. `image` enters here because a turn carrying an image is the named near-term consumer; audio, video, tool-calling, structured output, latency class and cost class do NOT enter, because nothing consumes them yet and a vocabulary guessed ahead of its consumers is one nothing validates against.

The declaration SHALL describe INPUT acceptance only. Output modality, tool-calling and structured-output support are different questions with different consumers, and folding them into one set would produce a field whose members mean different things to different readers.

#### Scenario: An entry declares that it accepts images
- **WHEN** a catalog entry declares modalities `text` and `image`
- **THEN** the declaration is valid and a router may treat the model as a candidate for a turn carrying an image

#### Scenario: An entry declares nothing
- **WHEN** a catalog entry carries no modality declaration
- **THEN** the entry is valid, is treated as text-only for routing, and is recorded as having made no declaration
- **AND** its silence is not reported as a claim that it rejects images

#### Scenario: A modality outside the vocabulary is declared
- **WHEN** an entry declares a modality that is not `text` or `image`
- **THEN** the catalog is refused, naming the closed vocabulary
- **AND** the remedy is the change that governs the new modality, not a wider field

#### Scenario: An entry declares images but not text
- **WHEN** an entry declares a modality set that omits `text`
- **THEN** it is refused: a chat turn always carries text, so a model that cannot accept text is not routable here

#### Scenario: A consumer needs a modality the vocabulary lacks
- **WHEN** a real consumer requires a modality outside the closed set
- **THEN** the vocabulary is extended by the change that governs that consumer, additively
- **AND** the extension names the consumer, rather than enumerating capabilities that might one day be wanted

### Requirement: The catalog type enforces every bound the released schema enforces
The server-side catalog type SHALL refuse every catalog the RELEASED SCHEMA would refuse on a bound it declares. A type gate weaker than the wire gate lets a catalog be constructed and dispatched in-process that `GET /workbench/model-catalog` then refuses to serve, because the route validates the projected envelope against the released schema — a divergence this capability has already had to close once, for a routing rule's target list.

Specifically, the type SHALL hold the entry count and the entry identifier to the released bounds: a catalog SHALL NOT exceed the released maximum number of entries, and a `model_id` SHALL satisfy the released length and character bounds — the same bounds already applied to the id-bearing REFERENCE fields, applied now to the identifier those references name.

Where a bound is restated in the type rather than read from the schema, the restatement SHALL name the released bound it mirrors, so a later reader can see the two are meant to agree and can find the other one.

#### Scenario: A catalog exceeds the released entry maximum
- **WHEN** a catalog is constructed with more entries than the released schema permits
- **THEN** construction is refused, naming the measured count and the released maximum
- **AND** the refusal happens at construction rather than at the moment the route declines to serve it

#### Scenario: An identifier exceeds the released bounds
- **WHEN** an entry is constructed with a `model_id` longer than the released maximum, or outside the released character pattern
- **THEN** construction is refused on the same bounds the released schema states
- **AND** the refusal matches what the reference-bearing fields already enforce for the same values
