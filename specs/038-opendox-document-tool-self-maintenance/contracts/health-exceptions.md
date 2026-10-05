# Contract: `health/dispositions.yaml`, exceptions in git

Status: draft

**Feature**: 038 · **Authority**: R2Q22 (a) (openDox-spec schema 3); box 14.8
("EXCEPTIONS LIVE IN GIT, NOT THE STORE"); answer R2Q10 (a) for the key.
**A PROPOSAL until Brett rules the plan** (OQ-H-13, OQ-H-14, OQ-H-15).

**Where it lands.** T040 authors the schema in openDox-spec; T054 copies it
into openDox-code with its digest checked and implements `health accept`.

## Shape

```yaml
schema_version: 1
kind: opendox-health-dispositions
exceptions:
  - finding: opendox.orphan.9a0b1c2d3e4f5a6b   # a finding id (contracts/health-finding.md)
    reason: kept as an unlinked appendix on purpose
```

## Rules

- **Effect.** An accepted finding is SUPPRESSED: a run neither stores nor lists
  it. It is not downgraded (OQ-H-13). Removing its entry re-opens it on the
  next run.
- **Who and when** are git's: the commit that added the entry.
- **`health accept --finding <id> --reason <text>`** appends one entry. In a
  checkout it writes the working tree, and the user commits it (F14.1 asserts
  `git status --porcelain` shows the file). With no working tree, it writes a
  draft on a branch that lands through `land` (OQ-H-14).
- **Survives a reset.** `runtime reset` drops the store; the file is in git, so
  no exception is lost (SC-006; F14.1).
- **Refusals by name.** A file at this path with another `kind` (for example
  the aggregation's own `health/dispositions.yaml`, plan.md Conflicts C-7); an
  entry with no `reason`; a malformed `finding` id; an unknown key. A refused
  file suppresses nothing, and the refusal is an install-level finding.
- **Not a document.** This file and `health/packs.yaml` join the
  settings-document exclusion, so no family reports on them (OQ-H-15).
