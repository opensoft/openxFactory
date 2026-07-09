# Design: Refine Promotion Provenance

## Decision 1: Standalone change, not folded into a DTN execution

The staged fragment proposed folding these rules into the first DTN change.
Reversed: prior changes are all archived (no delta stacking on the modified
requirement), the rules are candidate-agnostic process policy, and settling
them first lets every DTN change execute against stable rules. The staged
topic records the reversal.

## Decision 2: Drafting ownership mirrors the family split

codexFactory workers execute (drafting is doc engineering); the originating
domain's Hermes owns approval of surrendered meaning. No new authority
concept is introduced — this instantiates the existing execution/authority
split for the promotion path specifically.

## Decision 3: Provenance as optional stack fields, verified at `adopted`

`promoted_from` and `specializes` are optional so existing stacks stay valid
and adoption is incremental. Enforcement attaches to the register: an
`adopted` entry with provenance declared must resolve — checked by the
doc-health run, not by schema requiredness. This keeps the schema change
backward compatible (versioning policy: additive optional fields).

## Decision 4: Mid-promotion tiebreaker is the register, not git state

Consumers cannot be asked to inspect branch topology to know which copy
rules. The register entry status (`seed` … `adopted`) is a single, already-
governed pointer; "domain-local authoritative until re-pin completes" turns
the register into the interim authority signal with no new mechanism.
