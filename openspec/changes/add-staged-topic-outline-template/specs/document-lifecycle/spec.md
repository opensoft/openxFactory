# document-lifecycle

## ADDED Requirements

### Requirement: Staged topic primary-fragment template
A staged topic's primary fragment SHALL follow a fixed template so that its live state is extractable by a reader or a parsing tool without opening the rest of the topic folder. The primary fragment is the file `primaryFragmentPath` already selects deterministically and path-only; this requirement adds no second candidate file and MUST NOT change that selection. Every other file in a topic folder stays free-form.

A conforming primary fragment SHALL carry three required sections — pre-document non-documented idea notes, conflicts, and open questions — in addition to its proposal-element sections. Each open question SHALL carry four sub-fields in this fixed order: Context, Recommended answer, Explanation, Disposition status. A question MUST NOT be recorded as a bare question: the template requires a recommendation and the reasoning for it even while the disposition itself remains open, so that an undecided question still carries a proposal to disagree with.

Sections beyond the required set MAY be added by either a human or an AI, and each added section SHALL carry an `Added-by:` line naming the person or agent and the date. Attribution is required because the document accumulates content nobody commissioned in advance.

The proposal-element sections SHALL be wrapped in the ratified `xspec:candidate` / `xspec:supersedes` prose-tagging marker grammar rather than a second addressing mechanism. That prose IS the candidate text an eventual OpenSpec change would carry, and the marker grammar already exists for exactly that content.

**Round-trip on demote.** When a topic that reached proposal is demoted back to staging — by the demote verb, or by a failed or reverted push — its proposal-element sections SHALL be refreshed to the ACTUAL text of the last attempted `proposal.md`, tagged with the change id and the dates raised and demoted, together with the demote reason. They MUST NOT be reset to their pre-proposal aspirational text. Nothing learned while the change was in flight may be lost by falling back to staging.

Conformance SHALL be REQUIRED for any topic staged after this requirement ratifies, and OPT-IN for topics staged before it — rewritten only when a topic is next actively touched. Doc-health SHALL report non-conformance of a pre-existing topic at warning tier as a nudge and MUST NOT treat it as a gate-blocking finding, because a mechanical rewrite of dormant, complete, or externally blocked topics produces busywork without advancing any live decision.

#### Scenario: A topic is staged after ratification
- **WHEN** a new staged topic's primary fragment is authored
- **THEN** it MUST carry the three required sections and the four-sub-field shape for every open question
- **AND** a bare question with no recommended answer MUST be rejected as non-conforming

#### Scenario: A proposal is demoted back to staging
- **WHEN** a topic that reached proposal is demoted
- **THEN** its proposal-element sections MUST carry the last attempted `proposal.md` text, the change id, the raised and demoted dates, and the demote reason
- **AND** they MUST NOT be reset to the pre-proposal text

#### Scenario: An AI adds a section
- **WHEN** a section beyond the required set is added by a human or an agent
- **THEN** it MUST carry an `Added-by:` identity and date

#### Scenario: A topic staged before ratification is untouched
- **WHEN** doc-health evaluates a pre-existing topic that does not conform
- **THEN** it MUST report at warning tier
- **AND** it MUST NOT block a gate on that finding

#### Scenario: The template would require a second selected file
- **WHEN** a proposed change would make a file other than the deterministically selected primary fragment the topic's outline
- **THEN** it MUST be rejected, because the one-path selection rule is preserved rather than extended
