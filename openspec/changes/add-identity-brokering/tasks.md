# Tasks: add-identity-brokering

Phase 1 is THIS change's realization surface, and it is NOT being
implemented now — the proposal is `Status: draft` and phase 2 is the gate.
Phases 4 and 5 are named successor changes, listed so the sequencing and
the ownership are agreed here rather than negotiated later; they are not
executed by this change.

Dependency order: gate (2) blocks ratification; ratification blocks
phase 1; phase 1's released bundle blocks every successor in phase 4.

## 1. Contract (openxFactory — THIS CHANGE)

- [ ] 1.1 NEW `contracts/identity-brokering/persona-assertion.schema.yaml`
      (`kind: persona_assertion`, `schema_version`): the issuing broker
      instance id, the stable opaque subject, the display name, the linked
      upstream identities (provider id + upstream subject only — never a
      credential), the organization memberships, and the assertion time.
      Property set is a CLOSED ALLOW-LIST: there is no place in the shape
      to put a role, a group, a grant, a project, a stack, a layer, or a
      domain, so the never-mirror rule is enforced by the shape rather
      than by review (spec R3, design D2 and its risk).
- [ ] 1.2 NEW `contracts/identity-brokering/broker-organization.schema.yaml`
      (`kind: broker_organization`): organization id, company role
      (`tenant` | `served` — the ratified `layer-vocabulary` spelling),
      routed domains, federated upstream provider references, and EXACTLY
      ONE optional resolvable reference to the governed record the
      organization corresponds to. One reference, `maxItems`-bounded and
      singular by shape — the pointer-not-projection line of design D2
      lives here (spec R2, R3).
- [ ] 1.3 NEW `contracts/identity-brokering/actor-subject-reference.schema.yaml`
      (`kind: actor_subject_reference`): the reference a governed record
      embeds — issuer (broker instance), opaque subject,
      `display_name_at_record`, and a provenance discriminator separating
      a broker-asserted persona from a pre-broker bare username and from a
      mapped historical actor. Structured, per the OQ-3 recommendation;
      the consuming gate-console change confirms or overrides it against a
      real record before the bundle cuts (spec R5).
- [ ] 1.4 NEW `contracts/identity-brokering/identity-link-record.schema.yaml`
      (`kind: identity_link_record`): mode (`self_link` | `admin_merge`),
      the initiating persona or the approving administrator, the subjects
      involved, the surviving subject, the time, and an evidence
      reference. `mode` requires its actor by shape — a self link without
      an initiator and a merge without an approver are both
      unrepresentable — and the record carries every pre-merge subject so
      the resolvability obligation has a source (spec R4, design D4).
- [ ] 1.5 NEW `contracts/identity-brokering/broker-client-declaration.schema.yaml`
      (`kind: broker_client_declaration`): the service client, the surface
      it serves, the stated reason OIDC tokens are required, its
      `credential-contracts` requirement reference, and the transport
      assertion. No organization-membership-as-authority field exists, and
      the shape carries no actor role at all (spec R6, R7).
- [ ] 1.6 NEW `contracts/identity-brokering/surface-adoption.schema.yaml`
      (`kind: broker_surface_adoption`): the surface, its declared
      authorization posture (`authenticated_persona` |
      `resolved_authorization`), whether it offers governed write actions,
      the governed decision point when it does, and the retired
      credential reference when adoption replaces a shared static secret
      (spec R7, R9, design D8 and D9).
- [ ] 1.7 `contracts/identity-brokering/README.md`: the family, the
      single-persona rule, organizations as company boundaries, the
      pointer-not-projection line, merge safety, the actor-subject
      contract, the workloads-are-not-personas rule, custody by
      composition, isolation by instance with silence on count, and the
      named consumers (the OpsxFactory administration workflow, the
      install repo, the dashboard swap, the gate console).
- [ ] 1.8 Packaged examples under
      `contracts/identity-brokering/examples/`. Positives: a persona with
      two linked upstream identities and two organization memberships; a
      tenant organization and a served organization, one federating its
      own provider with domain routing; a self-link record; an
      admin-merge record with both pre-merge subjects; a governed actor
      reference; a pre-broker actor reference and its mapped counterpart;
      a service-client declaration; a read-only surface adoption
      retiring a shared secret; and a dedicated-instance adoption.
      Negatives under `negative/`, each naming the rule it violates:
      `persona-assertion-carries-roles`,
      `persona-assertion-carries-project-scope`,
      `organization-projects-governed-record` (copied contents, not a
      pointer), `organization-carries-multiple-graph-refs`,
      `second-persona-for-same-human-in-instance`,
      `link-record-auto-matched-on-email`,
      `link-record-without-initiator-or-approver`,
      `merge-record-drops-pre-merge-subject`,
      `actor-reference-uses-display-name-as-id`,
      `actor-reference-bare-username-as-persona`,
      `workload-declared-as-persona`,
      `service-client-recorded-as-actor`,
      `service-client-membership-as-authority`,
      `configuration-export-carries-client-secret`,
      `idp-credential-committed-in-manifest`,
      `adoption-leaves-shared-secret-live`,
      `isolation-by-persona-partition-in-shared-instance`,
      `write-action-under-authenticated-persona-posture`.
- [ ] 1.9 Implement `scripts/validate-identity-brokering.py` (canonical
      validator, repo-path argument like the other canonical validators):
      schema checks plus the rules the shapes cannot express —
      (a) persona-assertion and organization properties validated against
      a CLOSED ALLOW-LIST, so an unrecognized property fails rather than
      passing unnoticed (never a denylist of forbidden names);
      (b) one persona per human per broker instance across a fixture set;
      (c) every link/merge record resolves an explicit initiator or
      approver, and every pre-merge subject in a merge record resolves to
      the surviving persona; (d) no actor reference carries a display
      name, address, or upstream account name in the identifier position,
      and provenance is never `broker_asserted` for a bare username;
      (e) credential-value detection BY CLASS across every example and
      export fixture, with chunk reassembly, so a secret cannot be
      smuggled through a free-text field; (f) a surface declaring write
      actions must declare `resolved_authorization` and name its governed
      decision point; (g) an adoption that names a replaced shared
      credential must mark it retired.
- [ ] 1.10 Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      add-identity-brokering --strict` and `--all --strict` green;
      `python3 scripts/validate-identity-brokering.py . --strict` green
      (0 errors, 0 warnings) over the packaged examples;
      `python3 scripts/validate-ideation-cross-reference.py` still 0
      errors; doc-health clean against the change and the promoted
      supporting docs.
- [ ] 1.11 Register in `contracts/manifest.yaml` +
      `contracts/CHANGELOG.md` + the README contract index at the next
      additive bundle cut, per `docs/contract-versioning-policy.md`
      (registration-at-realization precedent). Every schema carries a
      manifest digest and closed release-inventory membership; the
      canonical validator and the example corpus are pinned by the exact
      release commit so successors pin a release rather than copy a shape.

## 2. Pre-ratification gate

- [ ] 2.1 **GATE — the co-residence check (design OQ-5).** Produce a
      written finding, before ratification, on whether any current
      commitment implies a user population that must NOT co-reside in a
      shared broker instance. Name each candidate population and the
      commitment consulted — the Medx clinical surfaces and the Business
      Central / DaVinciSite tenant work are the two the topic names — and
      record the answer even when it is "none found". If one exists it
      becomes the first dedicated-instance client under design D3, and the
      contract's silence on instance count is exercised immediately
      rather than theoretically.
- [ ] 2.2 Brett ratifies proposal, design, and both spec deltas, or rules
      the open design points differently. Ratification authorizes exactly
      one Speckit realization feature for phase 1 and creates no broker,
      realm, organization, credential, or persona.
- [ ] 2.3 Settle before the schemas are authored, and record the
      resolution in the realization feature's research: OQ-3 (the
      `actor_subject` field shape — recommendation: the structured
      reference) and OQ-1's history handling (recommendation: mark the
      boundary date, map on demand, never blanket-backfill). Both are
      shape decisions that cost a schema major if guessed wrong.

## 3. Promotion bookkeeping (with phase 1)

- [ ] 3.1 Move `ideation/staging/identity-brokering-plane/` into
      `openspec/changes/add-identity-brokering/supporting-docs/` per
      `document-lifecycle`, and remove the emptied staging folder so it
      leaves the organized-work queue.
- [ ] 3.2 Write `supporting-docs.manifest.yaml`: original staging path,
      source revision, transition date, per-file hashes, and the repeated
      `origin.kind` / `origin.id` / `origin.path` values, which MUST match
      `.openspec.yaml` exactly or strict proposal validation fails.
      Promoted prose carries `Status: draft` and names this change.
- [ ] 3.3 Retire the `identity-brokering-plane` row and detail section in
      `ideation/staging/INDEX.md`, recording the exit as
      "Proposed as add-identity-brokering (exit 1)"; leave the sibling
      `pki-trust-anchor-plane` row untouched.
- [ ] 3.4 Annotate the origin brainstorm
      `ideation/brainstorm/keycloak-identity-brokering.md`: its
      "Exit executed" section names this change as exit 1's realization.
      Keep it as design history; do not rewrite its rulings.
- [ ] 3.5 List the change in the openxFactory README "OpenSpec Records"
      block on landing, and move the entry when it archives.
- [ ] 3.6 Cross-reference `add-trust-anchor` as the sibling proposal from
      the same 2026-08-21 session (rulings R1 and R7 were made once for
      both), and confirm the two changes' `repo-boundary-governance`
      deltas remain two distinct ADDED requirements — never a shared
      MODIFIED one (design D7).

## 4. Successor changes (NOT this change)

- [ ] 4.1 **OpsxFactory `keycloak-administration`** — the governed
      administration workflow as a sibling of `exchange-administration`,
      `aks-administration-workflow`, `github-administration-workflow` and
      `business-central-administration`, expressed in this contract's
      vocabulary. Registers the new service-subject kind in LOCKSTEP:
      `customer-kinds` + the Hermes template + `stack.yaml` in one change,
      with grant ceilings in `credentials/requirements.yaml`. Developed in
      `OpsxFactory:staging:identity-pki-administration`, which covers both
      administration workflows because they share the registration work.
      Owns the merge-queue response time (design D4's risk).
- [ ] 4.2 **`implement-keycloak-install-repo`** — creates
      `opensoft/xFactory-Keycloak-Install` under the requirement this
      change adds, pins the released contract bundle, and lands the first
      generated `config/clients/opensoft/runtime-manifest.yaml` on the
      hermes-install precedent. Aggregation admission at
      `installs/keycloak-install` is its own separate reviewed change and
      MUST NOT ride the creation change.
- [ ] 4.3 **Dashboard oauth2-proxy swap** — oauth2-proxy or nginx
      external-auth in front of the workbench route, pointed at the
      broker; the htpasswd secret retires in the same change (spec R7),
      and the surface records an `authenticated_persona` adoption
      (spec R9). First adoption, and the cheapest proof of the broker in
      production.
- [ ] 4.4 **Gate-console `actor_subject` binding** — the gate-action
      record binds its actor to the broker-issued subject plus display
      name, closing the forgeable-actor and unauthenticated-`--actor`
      accepted risks and unblocking the server-side console phase. This
      change settles OQ-3 against a real record and, because the console
      gains a governed write action, must declare
      `resolved_authorization`.
- [ ] 4.5 **Editor-product login** — the editor authenticates through the
      same broker; the drive grants (Google / Microsoft OAuth tokens under
      `credential-contracts`) attach to the persona.
- [ ] 4.6 **Later, each on its own delta**: `hermes-readiness` bearer
      tokens (OQ-4 — after enrollment auth modes settle, and probably as a
      grant rather than a persona token); avatar-surface persona login;
      persona-scoped workbench filtering (organization membership crossed
      with the project register); and the per-action authorization delta
      that OQ-2 defers.

## 5. Acceptance (spans phase 4; closes the staged topic)

- [ ] 5.1 One human, two upstream providers, two organizations, one
      persona — demonstrated end to end on the dashboard adoption, with
      the second identity linked explicitly and no auto-link having
      occurred.
- [ ] 5.2 A gate action recorded with a broker-asserted actor subject that
      survives a display-name change, plus a pre-broker record that still
      reads correctly and is not presented as a persona.
- [ ] 5.3 A negative drill: an attempted email-match auto-link refused, a
      credential-bearing configuration export refused by the install
      repo's boundary validation, and a write action refused on a surface
      whose declared posture is authentication-only.
- [ ] 5.4 Evidence for 5.1–5.3 recorded against the released contract
      bundle version each successor pinned, and the staged topic's exit
      recorded as complete.
