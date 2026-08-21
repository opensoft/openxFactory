# Tasks: add-identity-brokering

Phase 1 is THIS change's realization surface, and it is NOT being
implemented now — the proposal is `Status: draft` and phase 2 is the gate.
Phases 4 and 5 are named successor changes, listed so the sequencing and
the ownership are agreed here rather than negotiated later; they are not
executed by this change.

Dependency order: gate (2) blocks ratification; ratification blocks
phase 1; phase 1's released bundle blocks every successor in phase 4.

## 1. Contract (openxFactory — THIS CHANGE)

- [x] 1.1 DONE 2026-08-21 — realized by Speckit feature `008-identity-brokering-contracts`; the property set is a closed allow-list at every depth AND the validator re-derives that allow-list from the schema, so an unrecognised property is refused by name (never a denylist). NEW `contracts/identity-brokering/persona-assertion.schema.yaml`
      (`kind: persona_assertion`, `schema_version`): the issuing broker
      instance id, the stable opaque subject, the display name, the linked
      upstream identities (provider id + upstream subject only — never a
      credential), the organization memberships, and the assertion time.
      Property set is a CLOSED ALLOW-LIST: there is no place in the shape
      to put a role, a group, a grant, a project, a stack, a layer, or a
      domain, so the never-mirror rule is enforced by the shape rather
      than by review (spec R3, design D2 and its risk).
- [x] 1.2 DONE 2026-08-21 — `governed_record_refs` is `maxItems: 1` with a closed reference object, and `company_role: tenant | served` bridges to the canonical layers (`tenant` -> `tenant`, `served` -> `subject`) whose ids and reserved terms the validator READS from `contracts/policies/layer-vocabulary.yaml` at run time. NEW `contracts/identity-brokering/broker-organization.schema.yaml`
      (`kind: broker_organization`): organization id, company role
      (`tenant` | `served` — the ratified `layer-vocabulary` spelling),
      routed domains, federated upstream provider references, and EXACTLY
      ONE optional resolvable reference to the governed record the
      organization corresponds to. One reference, `maxItems`-bounded and
      singular by shape — the pointer-not-projection line of design D2
      lives here (spec R2, R3).
- [x] 1.3 DONE 2026-08-21 — the structured reference, with the three provenance classes' wrong combinations UNREPRESENTABLE (a `pre_broker_username` admits no issuer or subject; `presented_as_persona` is a required constant `false`) and OQ-1/OQ-3 recorded as settled in `specs/008-identity-brokering-contracts/research.md`. NEW `contracts/identity-brokering/actor-subject-reference.schema.yaml`
      (`kind: actor_subject_reference`): the reference a governed record
      embeds — issuer (broker instance), opaque subject,
      `display_name_at_record`, and a provenance discriminator separating
      a broker-asserted persona from a pre-broker bare username and from a
      mapped historical actor. Structured, per the OQ-3 recommendation;
      the consuming gate-console change confirms or overrides it against a
      real record before the bundle cuts (spec R5).
- [x] 1.4 DONE 2026-08-21 — mode requires its actor by shape (a self link without an initiator and a merge without an approver are both unrepresentable), the admissible bases are READ OUT OF THE SCHEMA at run time so `attribute_match` is refused by the contract rather than by a second list, and every pre-merge subject carries the survivor it remains resolvable to. NEW `contracts/identity-brokering/identity-link-record.schema.yaml`
      (`kind: identity_link_record`): mode (`self_link` | `admin_merge`),
      the initiating persona or the approving administrator, the subjects
      involved, the surviving subject, the time, and an evidence
      reference. `mode` requires its actor by shape — a self link without
      an initiator and a merge without an approver are both
      unrepresentable — and the record carries every pre-merge subject so
      the resolvability obligation has a source (spec R4, design D4).
- [x] 1.5 DONE 2026-08-21 — the transport assertion is THREE required constants (`is_transport: true`, `actor_of_governed_acts: false`, `organization_membership_as_authority: false`), so the claim is always made and only the conformant value is representable; the validator additionally refuses a declared client's subject appearing as a persona or as a governed record's actor. NEW `contracts/identity-brokering/broker-client-declaration.schema.yaml`
      (`kind: broker_client_declaration`): the service client, the surface
      it serves, the stated reason OIDC tokens are required, its
      `credential-contracts` requirement reference, and the transport
      assertion. No organization-membership-as-authority field exists, and
      the shape carries no actor role at all (spec R6, R7).
- [x] 1.6 DONE 2026-08-21 — a write-offering surface cannot declare the weaker posture (schema conditional plus rule f), `resolves_in` and `satisfied_by` are single-member enumerations, `human_accounts_held_by_surface` is a required constant `false`, and a restricted population requires a `dedicated` instance while an unrestricted dedicated instance stays conformant (silence on count, both directions). NEW `contracts/identity-brokering/surface-adoption.schema.yaml`
      (`kind: broker_surface_adoption`): the surface, its declared
      authorization posture (`authenticated_persona` |
      `resolved_authorization`), whether it offers governed write actions,
      the governed decision point when it does, and the retired
      credential reference when adoption replaces a shared static secret
      (spec R7, R9, design D8 and D9).
- [x] 1.7 DONE 2026-08-21 — `Status: ratified` naming this change, the nine rules with their reasoning, custody by composition, isolation by instance with silence on count, the record-kind table, the named consumers, and the limits stated rather than implied. `contracts/identity-brokering/README.md`: the family, the
      single-persona rule, organizations as company boundaries, the
      pointer-not-projection line, merge safety, the actor-subject
      contract, the workloads-are-not-personas rule, custody by
      composition, isolation by instance with silence on count, and the
      named consumers (the OpsxFactory administration workflow, the
      install repo, the dashboard swap, the gate console).
- [x] 1.8 DONE 2026-08-21 — 14 positives and 27 negatives [Amended by the adversarial-review hardening of 2026-08-21: the negative corpus is now 41, one new fixture per verified bypass, still 9/9 requirement coverage. Findings F1-F14 and their dispositions are recorded in `specs/008-identity-brokering-contracts/traceability.yaml` under `review_hardening`; the three that tightened the CONTRACT rather than a check (F5, F11, F12) are disclosed in that feature's research.md.]: the 18 named below plus 9 for ratified clauses that would otherwise have gone unproven (including the two that give requirement R2 a probe at all, which the named list left uncovered). Each negative declares `# expected_failure:`, a detail pin and a `# requirement:` attribution; coverage is closed in both directions at 9/9. Packaged examples under
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
- [x] 1.9 DONE 2026-08-21 — thirteen lettered rules (a)-(m) [Amended by the adversarial-review hardening of 2026-08-21: now FOURTEEN, (a)-(n) — rule (n), a membership names a declared organization — and the red proof covers 22 finding codes, not 19. Findings F1-F14 and their dispositions are recorded in `specs/008-identity-brokering-contracts/traceability.yaml` under `review_hardening`; the three that tightened the CONTRACT rather than a check (F5, F11, F12) are disclosed in that feature's research.md.]. All seven named clauses are implemented as written, plus the pointer bound, the workload collisions, the instance escalation, the layer vocabulary and the no-local-accounts claim. The allow-list is DERIVED FROM THE SCHEMA (local `$ref`s resolved, branches unioned) rather than written as a second list, and a recorded red proof shows all 19 finding codes load-bearing (`specs/008-identity-brokering-contracts/evidence/`; 22 after the hardening slice, the harness deriving its code set from the fixtures' own headers). Implement `scripts/validate-identity-brokering.py` (canonical
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
- [x] 1.10 DONE 2026-08-21 — `openspec validate add-identity-brokering --strict` valid and `--all --strict` 63/63; `validate-identity-brokering.py . --strict` 0 errors / 0 warnings over 14 positives and 27 negatives (re-verified 0/0 over 14 positives and 41 negatives after the 2026-08-21 review hardening); `validate-ideation-cross-reference.py` unchanged (its 3 errors are pre-existing, in an unmodified `tests/ideation-dashboard/fixtures/` document); doc-health single-repo run carries no finding against this change, its promoted supporting docs, the new family or the new validator. Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      add-identity-brokering --strict` and `--all --strict` green;
      `python3 scripts/validate-identity-brokering.py . --strict` green
      (0 errors, 0 warnings) over the packaged examples;
      `python3 scripts/validate-ideation-cross-reference.py` still 0
      errors; doc-health clean against the change and the promoted
      supporting docs.
- [x] 1.11 DONE 2026-08-21 — registered at **`contract-v1.36`** (bundle bumped from `contract-v1.35`; the minor number was allocated at realization, never reserved ahead of merge order, and the annotated tag is applied post-merge to the realized commit per the versioning policy's "Bundle Realization Order"). All SIX schemas carry a per-file `sha256` in `contracts/manifest.yaml` under a `contract-v1.36` registration block with a distilled `consumption_rule` each; `scripts/validate-manifest-digests.py` verifies 150 digests (was 135). The `contract-v1.36` CHANGELOG entry states the additive class against the no-changes-required test, records that no `contract_schema_version` is bumped anywhere, and carries the realization + review-hardening provenance. Index rows added to `contracts/README.md` (family + validator/corpus) and conformance bullets to the root `README.md`. Per the openxWallet and client-identity-roster precedent the packaged corpus, the family README and `scripts/validate-identity-brokering.py` are content-addressed by commit with NO per-file digest — so the "closed release-inventory membership" this task asked for is the release-surface rule of `docs/contract-versioning-policy.md` § Release Digest Inventory, exercised when `contracts/releases/contract-v1.36.digests.yaml` is built at promotion time (`scripts/validate-contract-release.py build`), which is a promotion-order step and not part of this registration. Register in `contracts/manifest.yaml` +
      `contracts/CHANGELOG.md` + the README contract index at the next
      additive bundle cut, per `docs/contract-versioning-policy.md`
      (registration-at-realization precedent). Every schema carries a
      manifest digest and closed release-inventory membership; the
      canonical validator and the example corpus are pinned by the exact
      release commit so successors pin a release rather than copy a shape.

## 2. Pre-ratification gate

- [x] 2.1 **GATE — the co-residence check (design OQ-5).** DISCHARGED 2026-08-21 — finding at `review/co-residence-finding-2026-08-21.md`: one population found (HealthLinc patients), pre-declared the first dedicated-instance client under D3. Produce a
      written finding, before ratification, on whether any current
      commitment implies a user population that must NOT co-reside in a
      shared broker instance. Name each candidate population and the
      commitment consulted — the Medx clinical surfaces and the Business
      Central / DaVinciSite tenant work are the two the topic names — and
      record the answer even when it is "none found". If one exists it
      becomes the first dedicated-instance client under design D3, and the
      contract's silence on instance count is exercised immediately
      rather than theoretically.
- [x] 2.2 DONE 2026-08-21 — Brett ratified proposal, design, and both spec deltas (recommendations adopted as written; see the proposal's Ratification section). Brett ratifies proposal, design, and both spec deltas, or rules
      the open design points differently. Ratification authorizes exactly
      one Speckit realization feature for phase 1 and creates no broker,
      realm, organization, credential, or persona.
- [x] 2.3 DONE 2026-08-21 — both settled BEFORE the schemas were authored and recorded in the realization feature's research: `specs/008-identity-brokering-contracts/research.md` § "Settlement 1 — the `actor_subject` field shape (change task 2.3, design OQ-3)" adopts the STRUCTURED REFERENCE (issuer + opaque subject + `display_name_at_record` + provenance discriminator) with the question, the reasoning and what the settlement does NOT do; § "Settlement 2 — pre-broker history (change task 2.3, design OQ-1)" adopts MARK THE BOUNDARY DATE, MAP ON DEMAND, NEVER BACKFILL, and records its structural half. Both are realized in `contracts/identity-brokering/actor-subject-reference.schema.yaml`, where the three provenance classes' wrong combinations are unrepresentable and `presented_as_persona` is a required constant `false`, so neither settlement can be undone by an instance author. Settle before the schemas are authored, and record the
      resolution in the realization feature's research: OQ-3 (the
      `actor_subject` field shape — recommendation: the structured
      reference) and OQ-1's history handling (recommendation: mark the
      boundary date, map on demand, never blanket-backfill). Both are
      shape decisions that cost a schema major if guessed wrong.

## 3. Promotion bookkeeping (with phase 1)

- [x] 3.1 DONE 2026-08-21 — moved with the canonical tool (`python3 scripts/proposal-support.py . transition add-identity-brokering ideation/staging/identity-brokering-plane --apply`), which moves the file, writes a byte-identical `source-snapshots/` copy, sets the promoted prose to `Status: draft` / `Proposed by: add-identity-brokering`, rewrites its relative links, and removes the emptied staging folder. The folder is gone. Move `ideation/staging/identity-brokering-plane/` into
      `openspec/changes/add-identity-brokering/supporting-docs/` per
      `document-lifecycle`, and remove the emptied staging folder so it
      leaves the organized-work queue.
- [x] 3.2 DONE 2026-08-21 — written as `supporting-docs/manifest.yaml`, which is the filename the ratified `document-lifecycle` spine and `proposal-support.py` use for an ACTIVE change ("each active support folder owns `manifest.yaml`"); `supporting-docs.manifest.yaml` is the ARCHIVED form written beside the compressed bundle at archive time, from this manifest. It carries every field named here — `origin_path`, `source_revision` (5f59a32), `transitioned_at`, per-file `sha256` plus the source hash and snapshot path, and the repeated `origin.kind`/`id`/`path`, which the tool verified against `.openspec.yaml` before moving anything. `proposal-support.py verify add-identity-brokering` reports ok. Finding recorded in `specs/008-identity-brokering-contracts/research.md`. Write `supporting-docs.manifest.yaml`: original staging path,
      source revision, transition date, per-file hashes, and the repeated
      `origin.kind` / `origin.id` / `origin.path` values, which MUST match
      `.openspec.yaml` exactly or strict proposal validation fails.
      Promoted prose carries `Status: draft` and names this change.
- [x] 3.3 DONE 2026-08-21 — FULL promotion, so the INDEX maintenance rule's full-promotion branch applies rather than an in-place edit: no staged file remains, so the row AND the detail section are DELETED from `ideation/staging/INDEX.md` and the pointer moves to `ideation/README.md`'s "Active proposals promoted from staging" list, where the exit is recorded as exit 1 of the topic's three (with exits 2 and 3 named as the remaining successors). Row/section parity re-verified afterwards: 33/33 -> 31/31, and neither retired slug appears in either list. The sibling `pki-trust-anchor-plane` row was NOT left untouched as this task's last clause anticipated — `add-trust-anchor` realized in the SAME `contract-v1.36` cut, so its task 6.2 retired it in the same pass, and both pointers now sit side by side in the README list. Retire the `identity-brokering-plane` row and detail section in
      `ideation/staging/INDEX.md`, recording the exit as
      "Proposed as add-identity-brokering (exit 1)"; leave the sibling
      `pki-trust-anchor-plane` row untouched.
- [x] 3.4 DONE 2026-08-21 — APPENDED a "### Realization landed — 2026-08-21" subsection to the "Exit executed" section of `ideation/brainstorm/keycloak-identity-brokering.md`, naming this change, Speckit feature `008-identity-brokering-contracts` and the `contract-v1.36` registration; recording which carried-forward open questions the realization settled (the subject id and `actor_subject` shape, pre-broker history, the co-residence check) and which stay deferred; naming the sibling `add-trust-anchor` in the same cut; and pointing at both fragments' current homes under `supporting-docs/`. Not one word of the existing rulings was rewritten. The doc's historical `../staging/` links are deliberately LEFT dangling and labelled as design history, matching the precedent already set by `ideation/brainstorm/ideation-dashboard.md` after its own full promotion. Annotate the origin brainstorm
      `ideation/brainstorm/keycloak-identity-brokering.md`: its
      "Exit executed" section names this change as exit 1's realization.
      Keep it as design history; do not rewrite its rulings.
- [x] 3.5 DONE 2026-08-21 — the entry was already in the openxFactory README "OpenSpec Records" block under "Active changes"; this pass APPENDS the realization to it — REALIZED 2026-08-21 by Speckit feature `008-identity-brokering-contracts`, the family/validator/corpus named, hardened by the two-panel adversarial review, registered at `contract-v1.36`. Two conformance bullets were also added to the README's validator list (identity brokering and trust anchors), mirroring the `validate-openxwallet.py` entry. The second clause — moving the entry from "Active changes" when the change archives — remains OPEN by design and is not this pass's work. List the change in the openxFactory README "OpenSpec Records"
      block on landing, and move the entry when it archives.
- [x] 3.6 DONE 2026-08-21 — cross-referenced in four places that a reader actually reaches: both README "OpenSpec Records" entries name each other as siblings, both `ideation/README.md` promoted-list pointers state that R1 and R7 were ruled ONCE across the two topics, and the brainstorm annotation names the sibling realization in the same `contract-v1.36` cut. CONFIRMED by inspection this pass: the two `repo-boundary-governance` deltas remain TWO DISTINCT ADDED REQUIREMENTS and never became a shared MODIFIED one — `openspec/changes/add-identity-brokering/specs/repo-boundary-governance/spec.md` carries `## ADDED Requirements` with the single requirement "Keycloak install repository boundary", and `openspec/changes/add-trust-anchor/specs/repo-boundary-governance/spec.md` carries `## ADDED Requirements` with the single requirement "OpenXPKI install repository boundary". Neither file contains a `## MODIFIED Requirements` section, so there is no shared requirement for the two changes to collide on at archive time (design D7). Cross-reference `add-trust-anchor` as the sibling proposal from
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
