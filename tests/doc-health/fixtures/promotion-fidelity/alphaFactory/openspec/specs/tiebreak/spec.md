# tiebreak Specification

## Purpose
Fixture canon for the same-date tie: it carries the text of the packet that
was ARCHIVED last, which is NOT the packet whose folder name sorts last.

## Requirements
### Requirement: Contested on one date
The rule SHALL be the later one.

#### Scenario: The later statement holds
- **WHEN** two packets are archived on one date
- **THEN** the later archive act MUST be the authority
