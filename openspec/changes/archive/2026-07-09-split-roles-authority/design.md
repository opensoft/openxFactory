# Design: Split Roles And Authority

## Decision 1: Hermes-level roles stay neutral

PO/PM/CA/PA/Merge Council/Merge Master govern portfolio, architecture, and
admission across every domain; their table remains in the neutral doc.
Execution leads (LA/LE/LC/LQ/LI/LS) exist per-domain and move.

## Decision 2: Escalation splits by altitude

The neutral doc keeps WHAT must escalate (the boundary conditions); the
role-keyed routing table (WHO is consulted) moves with the roles it names.

## Decision 3: Groups YAML is deployment instantiation

The profiles/groups examples name engineering GitHub orgs; the neutral doc
keeps the one-install/many-groups concept in prose, the YAML moves.
