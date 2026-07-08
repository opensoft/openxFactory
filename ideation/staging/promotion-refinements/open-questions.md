# Staged: Promotion Process Refinements

Status: staged
Kind: reference
Repository context: openxFactory
Source: [domain-to-neutral-promotion brainstorm](../../brainstorm/domain-to-neutral-promotion.md)
Target capability: `document-lifecycle` / promotion process binding (delta:
MODIFIED) plus a possible `xfactory-domain-stack` schema field addition.

## Claims (each still a decision to make, not yet policy)

1. Neutralization drafting ownership: default to codexFactory doc-engineering
   workers under the doc-health pipeline, with the originating domain's
   Hermes reviewing for surrendered meaning — mirrors the execution/authority
   split used everywhere else.
2. `stack.yaml` grows optional provenance fields: `promoted_from:` (repo +
   artifact a neutral contract originated in) and `specializes:` (neutral
   artifact a domain overlay refines) so promotion provenance is
   machine-readable and the health run can verify adopted candidates.
3. Mid-promotion pinning: while a concept exists in both a domain repo and
   openxFactory staging, the domain copy remains authoritative until the
   re-pin gate; the register entry's status is the tiebreaker consumers
   check. A `promotion_state:` note in the register entry covers the interim.

## Exit

Fold all three into the next promotion-related OpenSpec change (plausibly the
one that executes DTN-001/002) rather than a standalone change.
