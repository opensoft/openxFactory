# Tasks: add-client-identity-roster

## 1. Ratification gate (BRETT)

- [ ] 1.1 `OPENSPEC_TELEMETRY=0 openspec validate add-client-identity-roster
      --strict` and `--all --strict` green; change listed in the README
      OpenSpec Records block.
- [ ] 1.2 Brett ratification of the four load-bearing decisions, each of
      which is contestable on cost grounds: (a) the axis is
      (workload × authority class) rather than one broad app; (b) governed
      identities are single-tenant and client-resident, multi-tenant only by
      ratified exception — this is the expensive one, it multiplies
      enrollment work per client; (c) achieved scope must be declared and the
      structural→logical degradation named; (d) drift detection is
      report-only. Cross-model decision review recorded in
      `review/decision-review-2026-08-14.md`. Everything below is parked
      behind this gate.

## 2. Neutral contract records

- [ ] 2.1 `contracts/schemas/client-identity-roster.schema.yaml`
      (`schema_version` + `kind`): per-client roster record — `client_ref`,
      `entries[]` each with `identity_ref` (no secrets), `workload`,
      `authority_class` (closed enum `observe|mutate|destructive`),
      `domain` (owning factory), `residency` (`client_tenant_single` or an
      exception ref), `ratified_by` (capability id), `admission` (the
      provider-side second key: surface, act, and `achieved_scope`),
      `blast_radius_unit`, `declared_excess` (with `gate_obligation` when
      achieved scope exceeds the unit).
- [ ] 2.2 Closed `workload` vocabulary with a declared extension path (a new
      workload arrives with the capability that governs it, never ad hoc).
- [ ] 2.3 `.example.yaml` instantiation stub — a two-domain client showing
      the composition rule and one declared-excess entry (the BC
      admin-center tenant-wide case is the worked example).
- [ ] 2.4 Cross-reference the record into `credential-contracts` and
      `consent-instrument` by reference only (identity layer beneath them;
      neither spec's requirements change).

## 3. Static conformance (doc-health family)

- [ ] 3.1 A `doc-health` family over roster records: entry without a
      ratified capability, ratified capability without an entry,
      cross-workload identity, combined authority classes, missing
      `admission`/`achieved_scope`, achieved excess without a
      `gate_obligation`, cross-domain overlap, non-client residency without
      an exception ref.
- [ ] 3.2 Severity and resolution classes assigned per finding in the
      established auto-fixable/contested scheme (an entry contradicting a
      ratified capability is contested — resolving it reverses a gate
      decision).
- [ ] 3.3 Deterministic fixtures: one positive two-domain roster, one
      negative per rule above.

## 4. Domain conformance (named, executed in the domain repos)

- [ ] 4.1 OpsxFactory declares its client-tenant entries against the neutral
      shape, including the Business Central pair and the three identity
      findings this investigation surfaced: the `opsx-farheap-bc-observer`
      name/purpose mismatch now that it holds tenant-wide admin-center
      authority, the inert Microsoft Graph delegated scope absent from its
      identity record, and the tenant-wide admin-center excess with its gate
      obligation.
- [ ] 4.2 LedgerxFactory declares its `ledgerx-farheap-bc-*` entries; the
      composition and overlap rules are exercised against a real two-domain
      client tenant.
- [ ] 4.3 Live drift detection remains a domain realization; record
      OpsxFactory's `add-github-installation-policy` as the reference
      implementation pattern and note that the client-tenant variant is its
      own domain change.

## 5. Validation and exit

- [ ] 5.1 `openspec validate --all --strict` green; the doc-health family
      green over the fixtures and over any real roster records that exist.
- [ ] 5.2 DTN candidate register updated if this contract warrants a
      register row (identity topology is neutral by construction).
- [ ] 5.3 Archive on realization evidence per `release-realization` (records
      + family landed and green; domain declarations are follow-ups, not
      archive blockers).
