# ideation-dashboard

## ADDED Requirements

### Requirement: A created document may carry an authored body
The create verb SHALL accept an OPTIONAL authored BODY and write it below the header it generates, in the same write and the same commit, because a drafted fragment arrives whole and becomes one document. A body SHALL NOT be required: a create with none behaves exactly as it does today.

The header SHALL remain the create's own, generated from its fields, so a body cannot restate `Status:`, `Topics:` or any other header field with a value the create did not record. The verb SHALL remain create-only — an existing target still refuses and is never overwritten — and SHALL remain human-only.

The body SHALL be text the human wrote. Nothing about this requirement authorises generating one, and the drafted markers a seed leaves are prompts to the human rather than claims by the machine.

#### Scenario: A drafted fragment lands as one document
- WHEN a human creates a document from a lens draft and has edited its body
- THEN the created file carries the generated header followed by that body
- AND it is one commit, with no state in which the header exists without the body

#### Scenario: A body cannot contradict the header
- WHEN a body restates a header field
- THEN the header the create generated is what the document carries

#### Scenario: A create without a body is unchanged
- WHEN no body is supplied
- THEN the document is the header-compliant skeleton it is today
