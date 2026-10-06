# Contract: `health/dispositions.yaml`, exceptions in git

Status: draft

**Feature**: 038 · **Authority**: R2Q22 (a) (openDox-spec schema 3); box 14.8
("EXCEPTIONS LIVE IN GIT, NOT THE STORE"); answer R2Q10 (a) for the key. **RULED
with the plan** (`#656` `6013547504`, as recommended: OQ-H-13, OQ-H-14, OQ-H-15,
N-14).

**Where it lands.** T040 authors the schema in openDox-spec; T060 pins and cuts
it; T054 copies it into openDox-code's copy record at the pinned commit (after
T047), and implements `health accept`.

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
  next run. An accepted id is never a DISAPPEARANCE either: when a baseline run
  had it and a later run suppresses it, the later run reports nothing for it,
  since the finding is accepted, not gone (data-model.md § the baseline;
  Copilot's review of `2076f24b`).
- **Who and when** are git's: the commit that added the entry.
- **One entry per finding id.** `finding` ids are UNIQUE in the file, so
  removing an entry always re-opens its finding (FR-014). `health accept` of an
  id the file already holds refuses by name, writing nothing and naming the
  existing entry's reason; to change a reason, the user edits the entry. A file
  with a repeated id, written by hand, is refused like any malformed file
  (below) (Copilot's review of `abd28ba2`).
- **`health accept --finding <id> --reason <text>`** appends one entry. In a
  checkout it writes the working tree, and the user commits it (F14.1 asserts
  `git status --porcelain` shows the file). With no working tree, it writes a
  draft on a branch that lands through `land` (OQ-H-14).
- **Which file a run reads** (the spec's deferred edge case, `spec.md:534-536`;
  review round 1, C4): the one in what the run reads. A default-tip or branch
  run reads the committed file; a working-state run reads the working tree's, so
  an uncommitted `accept` suppresses in a working-state run, and in no commit run
  until it is committed.
- **Survives a reset.** `runtime reset` drops the store; the file is in git, so
  no exception is lost (SC-006; F14.1).
- **Refusals by name.** A file at this path with another `kind` (for example
  the aggregation's own `health/dispositions.yaml`, plan.md Conflicts C-7); an
  entry with no `reason`; a malformed `finding` id; a `finding` id that appears
  twice; an unknown key. A refused
  file suppresses nothing, and the refusal is an install-level finding.
- **Not a document.** This file and `health/packs.yaml` join the
  settings-document exclusion, so no family reports on them (OQ-H-15).
