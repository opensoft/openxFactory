# ideation-dashboard

## ADDED Requirements

### Requirement: The outline tab renders the staged-topic template
The doxBench outline tab SHALL render a conforming staged topic's primary fragment as its templated sections rather than as undifferentiated prose, so the surface a human iterates a topic in shows the same structure the template contract requires. Section identity SHALL come from the fragment's own headings and its `xspec:` marker fences — the addressing grammar the template already uses — and the tab MUST NOT infer sections by content-sniffing or by fabricating headings the fragment does not carry.

The tab SHALL offer an add-section affordance. A section added through it SHALL be written by the existing `edit-document` path on the topic's branch session, scoped by the section it targets — the heading, or the `xspec:candidate` fence where the section is a proposal-element block — as the patch's addressing key. It MUST NOT introduce a second write verb: section-scoped patching is a patch-TARGETING detail, not a different kind of action, and `edit-document` already supplies the branch-scoped, committed, reviewable machinery.

(AMENDED 2026-08-15, Brett: "amend to edit-document". As ratified this named `edit-apply`, carried from the topic's Q4. `edit-apply` is the gate console's MAIN-RESIDENT redline verb — it requires a `change_id` and applies to change documents — so it cannot write a staged topic's fragment on a session branch, and the two states are mutually exclusive besides: a fragment whose topic has an owning change has already moved out of staging. `edit-document` is the session content verb the buffer contract already uses. Q4's intent is unchanged; only the verb name was wrong.) Every section added this way SHALL carry its `Added-by:` provenance, whether the author is the human or an agent.

The tab SHALL degrade rather than refuse on a NON-CONFORMING fragment. Topics staged before the template ratifies are conformant only opt-in, so the tab MUST render what is present, MUST NOT report a pre-existing topic as broken, and MUST NOT rewrite a fragment into conformance as a side effect of opening it. Conformance is earned when a human next works the topic, never by the act of viewing it.

Rendering the template MUST NOT change the outline buffer's existing seeding, hashing, dirty-state, or Save semantics. The buffer contract governs how the outline is loaded and written; this requirement governs only how its content is presented and how a new section is addressed.

#### Scenario: A conforming topic is opened in the outline tab
- **WHEN** the outline tab opens a primary fragment carrying the template
- **THEN** its required sections MUST be rendered as identified sections
- **AND** section identity MUST come from headings and `xspec:` fences, never from content-sniffing

#### Scenario: A human adds a section
- **WHEN** the add-section affordance is used
- **THEN** the write MUST go through `edit-document` scoped to the targeted section
- **AND** the added section MUST carry `Added-by:` provenance
- **AND** no second write verb MUST be introduced

#### Scenario: A pre-template topic is opened
- **WHEN** the outline tab opens a fragment staged before ratification that carries none of the required sections
- **THEN** it MUST render what is present without reporting the topic as broken
- **AND** it MUST NOT rewrite the fragment into conformance on open

#### Scenario: The gate capability is absent
- **WHEN** the outline tab renders on a plane with no gate capability
- **THEN** the add-section affordance MUST NOT be offered as a live control
- **AND** no write path MUST be reachable from the page
