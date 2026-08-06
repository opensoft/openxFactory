# Design: Project CRUD Commission + Project-Scoped Selection

## Context

Brett's 2026-08-06 decision round on staging topic
`dashboard-project-scoping` locked seven decisions (D1–D7, recorded in the
topic's primary doc). This change realizes the exit-1 slice; its design
restates only what this slice needs.

## Decisions

### D2 (inherited) — create-project is a commission, not a write
`project-register.yaml` lives in the AGGREGATION repo; every dashboard write
to date is confined to the served checkout. Rather than extend write
authority across a repository boundary, the verb records what every other
generative act records: a `workflow-job` descriptor + gate-action record,
fulfilled externally. The descriptor carries everything the fulfilment
needs — proposed `project_id`, display name, member repository ids — so the
edit is mechanical for the fulfilling session and, later, a lane.

### D-a — The proposed project id is orchestration-derived
The id is slugged from the name at commission time (collision-refused
against the register's existing ids), so the descriptor is complete and the
fulfilment never invents identity — the same authority posture as the
derivation lane's minted ids.

### D-b — Member validation reads the snapshot-index roster
The selector's roster (the snapshot index) is the serving plane's own list
of repository ids; a commissioned member outside it is refused at the
console. The SINGLE-PARENT rule (a repository belongs to at most one
project — the register schema's validator-side reading of D10) is enforced
at commission time against the register projection, and re-checked by the
fulfilment against the live register, which is authoritative.

### D-c — Selection scoping is a view concern over a served register projection
The snapshot INDEX is a locator and deliberately carries no grouping (its
schema refuses projection data), so the picker reads a read-only REGISTER
PROJECTION served at `/project-register.json` — the register stays the one
grouping roster, discovered upward from the checkout exactly as the
generator finds it. The picker then filters the existing selector roster
client-side; the active snapshot stays a single `(repository, ref)` key and
nothing downstream of selection changes. A static image (or a checkout with
no reachable register) 404s the route and the picker hides. This is
deliberate: exit 2 owns the merged view, and this change must not pre-build
half of it.

### D5 (inherited) — Authority declaration
Stated in the capability delta so the runtime twin
(`tenant-project-catalog-and-workstation-cache`) and this surface cannot
fork: the local register is development-plane-authoritative only until a
tenant project catalog exists, then becomes a derived workstation cache.

## Risks / Trade-offs

- **Undelivered create-project commissions accumulate** (no lane yet) —
  same posture and same mitigation as the wheel verbs: the descriptor
  status field is human-editable and the duplicate refusal names the
  blocking descriptor.
- **The register can drift from commissions** (a human edits the file
  directly while a commission is in flight). The fulfilment validates
  against the live register and refuses a stale commission rather than
  merging blind.

## Open Questions

None — the topic's decision round closed all five; this slice inherits its
answers.
