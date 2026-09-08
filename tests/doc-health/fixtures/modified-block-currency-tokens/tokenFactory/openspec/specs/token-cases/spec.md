# token-cases Specification

## Purpose
SYNTHESIZED. Backticked tokens with internal periods, a body bullet list, and a
four-sentence dated bold note.

## Requirements

### Requirement: Tokens with internal periods never end a sentence
The jump SHALL read `.openspec.yaml` for its repository name. The disposition
reader SHALL be the one `promotion_fidelity.py` already implements. A consumer
SHALL pin `contract-v1.45` exactly rather than a movable tag.

- a reader MUST resolve the repository id before it reads the pin
- a reader MUST refuse a movable tag
- a reader MUST record which contract release it resolved

**CORRECTED 2026-08-27 ON A RULING — this note is ONE unit. It carries four
sentences. The third sentence is the one an amendment edits, and it says that a
reader MUST NOT treat a note as several units. The fourth sentence exists so
that an edit to the third is not an edit to the last.**

#### Scenario: A token is read
- **WHEN** the reader opens `.openspec.yaml`
- **THEN** it MUST resolve the repository id
