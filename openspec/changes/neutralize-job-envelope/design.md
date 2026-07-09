# Design: Neutralize Job Envelope

## Decision 1: Loosen-in-place, not fork

A parallel "neutral" schema beside the engineering one would make every
consumer choose and would orphan the existing examples. Loosening the
canonical schemas in place keeps one contract; strictness returns as a
domain overlay — the split pattern DTN-003 was classified for.

## Decision 2: Overlay re-tightens, never redefines

The engineering overlay may only add constraints over the neutral core
(required-ness, enums); it may not rename or re-type fields. This keeps
allOf composition sound and lets neutral tooling read any domain's jobs.

## Decision 3: Pin-lag is not drift

omnigent-install's copies match its declared ref; the contract-copy family
measures against declared refs (this change writes that down as a
requirement scenario) so neutralization does not manufacture findings
against correctly pinned consumers.
