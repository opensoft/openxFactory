# Staged: Roles And Authority Split (DTN-013)

Status: staged
Kind: architecture
Repository context: openxFactory
Source: [Domain Neutralization Candidate Register](../../../docs/domain-neutralization-candidate-register.md)
entry DTN-013 (`split`, P0).
Target capability: new `roles-authority-model` (delta: ADDED).
Evidence: `docs/roles-and-authority.md` self-describes as the model "for the
AI software development factory" and embeds engineering machinery: the
Omnigent execution lead table (LA/LE/LC/LQ/LI/LS), an escalation routing
table keyed to those roles, and Hermes profile/group YAML naming
`opensoft/omnigent-engineering`. The reconcile change already moved Spec
Kit/PR policy pointers to codexFactory; the role instantiation remained.

## Claims (the split)

1. Neutral doc keeps: authority layers, architecture language (generalized),
   Hermes-level governance roles (PO/PM/CA/PA/Merge Council/Merge Master —
   cross-factory), escalation principles, domain execution ownership,
   external enforcement authority concepts, and the requirement that each
   DomainxFactory instantiate its execution lead roles.
2. codexFactory gains `docs/engineering-roles-and-authority.md`: the
   execution lead table, the role-keyed escalation routes, the
   profiles/groups YAML (engineering groups), and the engineering half of
   the rule-of-thumb.
3. Stale personal-path provenance (`/home/brett/projects/Agents/...`) is
   replaced with repo references.
4. codexFactory declares `specializes` for the roles doc (second use).

## Exit

Satisfied by
[split-roles-authority](../../../openspec/changes/archive/2026-07-09-split-roles-authority/proposal.md)
(2026-07-09). Register DTN-013: `adopted`.
