Reviewer role: Stack Architect (alignment review, read-only) — 2026-08-22
Subject proposal: openspec/changes/add-assembly-plane-separation/proposal.md

# Stack Architect review — `add-assembly-plane-separation`

Worktree `oxf-topology`, branch `change/assembly-plane-separation`. Change is untracked; contents are `proposal.md` + `.openspec.yaml` only.

**Headline:** the proposal's *reasoning* is sound and its *citations* are unusually accurate — but it is not yet a validatable OpenSpec change (three hard gate failures), its central topology premise is contradicted by two ratified requirements it never cites, and its openxwallet sufficiency claim omits the one required property that carries the authority it wants to delegate.

---

## 1. Topology feasibility against the real workspace

**F1 — The submodule count is wrong by four.**
- **Source:** `/home/brett/projects/xFactory/.gitmodules` — 18 `[submodule]` entries (`git submodule status` agrees: 18). The README's "Current Submodules" list is stale at 13.
- **Proposal reference:** Q1.
- **Fix:** "A new repository is a **nineteenth** submodule of the aggregation repo (18 today per `.gitmodules`; the README's 13-entry `## Current Submodules` list is stale and the admission change must refresh it)."
- **Severity:** MISMATCH

**F2 — The three-plane premise is contradicted by openxFactory itself, twice, in promoted text the proposal never cites.**
- **Source:** `openspec/specs/shared-contract-ownership/spec.md:113-121` ("openxFactory SHALL own the deterministic broker/control reference modules, the fail-closed authority stub, the contract validator … all as non-deployable reference code under `xfactory/avatar_runtime/`") and `:139-146` ("Tooling hosted in the publisher verifies released bytes, not a declared pin" — neutral tooling deliberately hosted *inside* openxFactory, the relocation ratified 2026-08-03 by `adopt-neutral-tooling-home`).
- **Proposal reference:** ## What Changes, bullet 1.
- **Why it bites:** the universal claim "Every governed unit is declared to split across THREE REPOSITORY PLANES" is false of openxFactory as ratified — it is SPEC *and* CODE in one repository, and the house's most recent tooling-home ruling moved code **toward** the repo whose artifacts it reads, the opposite of the assembly move. This is the strongest available counter-precedent and it is undiscussed.
- **Fix:** add to ## What Changes bullet 1: "The planes are a topology statement about the REVIEW BOUNDARY, not a general rule that no repository may hold two planes: `shared-contract-ownership:113-121` and `:139-146` ratify openxFactory holding non-deployable reference code and neutral tooling alongside its specs, and `adopt-neutral-tooling-home` (2026-08-03) moved tooling INTO the publisher on purpose. The assembly plane separates only the code that ASSEMBLES A REVIEWER from the code it reviews; co-residence of spec and non-assembly code is untouched."
- **Severity:** MISMATCH

**F3 — "One shared assembly repo" collides with two canonical-ownership requirements over the *gate rules* it proposes to hold.**
- **Source:** `openspec/specs/repo-boundary-governance/spec.md:8-13` (openxFactory is canonical for "authority rules, role definitions, … **merge authority concepts**"; scenario `:16-17` names "**merge council behavior**"); `openspec/specs/canonical-policy-migration/spec.md:44-48` (openxFactory owns canonical neutral "merge authority … policy").
- **Proposal reference:** ## What Changes, bullet 2 ("the gate-rule machinery"); Q2.
- **Why it bites:** the merge-master *core* is machinery, but `codexfactory-routine-code-clearance.yaml` is rules-as-code — policy — and policy has a canonical home that is neither codexFactory nor a new repo. Q2's boundary question is asked as assembly-vs-product and never as machinery-vs-policy.
- **Fix:** add to Q2: "A third cut runs orthogonally to assembly-vs-product: the gate RULES are merge-authority policy, canonically openxFactory's under `repo-boundary-governance:8-13` and `canonical-policy-migration:44-48`, while the ENGINE that applies them is machinery. The specs phase must say whether the assembly repository holds rules, engine, or both, and how that is consistent with the canonical policy home."
- **Severity:** DRIFT

**F4 — Q5 states the migration discipline incompletely, omitting the stop condition its own realization trips.**
- **Source:** `openspec/specs/repo-boundary-governance/spec.md:59-64` and scenario `:74-76`: "WHEN a dogfood migration feature proposes deleting source docs, **moving runtime code, changing submodule pointers**, or touching generated state → THEN the feature MUST stop and return to Hermes approval before implementation continues," with `:62-64` requiring "a narrower exception for a specific feature."
- **Proposal reference:** Q5 (cites only `:41-58`, copy-first).
- **Why it bites:** the realization is precisely *moving runtime code* + *changing submodule pointers*. Saying repo-boundary-governance "already carries the discipline" while naming only copy-first understates the obligation by a whole gate.
- **Fix:** append to Q5: "Beyond copy-first, `repo-boundary-governance:59-64` and its scenario `:74-76` make 'moving runtime code' and 'changing submodule pointers' explicit stop conditions: the realization MUST return to Hermes for a narrower exception approved for that specific feature before implementation continues. That approval is a precondition of the move, not a formality after it."
- **Severity:** MISMATCH

**F5 — The wrong template is named for the new repository's scope declaration.**
- **Source:** `openspec/specs/repo-boundary-governance/spec.md:29-40` — "Install repository scope" is name-scoped to `Hermes-Install` and `Omnigent-Install` and to "subsystem install, operations, backup, restore, upgrade, verification, and disaster recovery." An assembly repository is none of those. The actual template for a non-install repository carved out of an existing tree is `:113-128`, "Neutral avatar-client repository boundary" (names the repo, what it owns from creation, what it pins, what it MUST NOT contain).
- **Proposal reference:** ## Impact, "Adjacent capability not declared as modified."
- **Fix:** replace with: "`repo-boundary-governance` carries **'Neutral avatar-client repository boundary'** (`:113-128`) — the template for declaring a NON-install repository's boundary: what it owns from creation, what it pins, and what it MUST NOT contain. 'Install repository scope' (`:29-40`) is not the model; it is name-scoped to the two install repos and to install/DR concerns."
- **Severity:** DRIFT

**F6 — Moving the decision core out of codexFactory needs a Domain-Hermes surrender gate that is nowhere named.**
- **Source:** `docs/domain-to-neutral-promotion-process.md:299-306` — "Authority is symmetric: the owning Domain Hermes approves surrendering or receiving a concept, boundary governance approves the neutral side, and both gates are OpenSpec changes, never bare commits."
- **Proposal reference:** Q1, Q5, ## Impact.
- **Fix:** add to Q5: "The move is a devolution/promotion act under `docs/domain-to-neutral-promotion-process.md:299-306`: codexFactory's Domain Hermes must approve SURRENDERING the decision core and the receiving side must approve receiving it, each as its own OpenSpec change. Neither gate is discharged by this proposal."
- **Severity:** DRIFT

---

## 2. Pattern alignment

**F7 — Every repository boundary in this corpus is a `repo-boundary-governance` delta, and the precedent declares the boundary BEFORE the repo exists — which refutes the stated reason for deferring.**
- **Source:** promoted `repo-boundary-governance` "Neutral installer repository integration" (`:90-95`), "Neutral avatar-client repository boundary" (`:113-128`), "Deferred aggregation and web-console integration" (`:165-173`); active `add-identity-brokering/specs/repo-boundary-governance/spec.md:5` (ADDED "Keycloak install repository boundary"), `add-trust-anchor/…:5` (ADDED "OpenXPKI install repository boundary"), plus `admit-install-repos-to-aggregation`, `implement-keycloak-install-repo`, `implement-openxpki-install-repo`. Eight instances, zero new capabilities. `add-identity-brokering` added the Keycloak boundary while the repository did not yet exist — created later by `implement-keycloak-install-repo`.
- **Proposal reference:** ## Impact, "Adjacent capability not declared as modified, deliberately" ("contingent on Q1 resolving to a new repository").
- **Fix:** replace the deferral with: "A `repo-boundary-governance` MODIFIED delta IS declared. The house declares a repository boundary before the repository exists — `add-identity-brokering` added 'Keycloak install repository boundary' for a repo `implement-keycloak-install-repo` created afterwards — so Q1's outcome selects the boundary's CONTENT (new repo vs annexation), not whether the delta is declared."
- **Severity:** DRIFT (strong — eight-instance precedent against)

**F8 — The spec-owner/code-owner "silence" claim is not clean: there is an archived change on exactly that reconciliation, and a promoted requirement already owning role definition.**
- **Source:** `openspec/changes/archive/2026-07-09-reconcile-domain-neutral-and-engineering-spec-ownership/` (subject: neutral SPEC ownership vs codexFactory's engineering/implementation ownership; landed as three MODIFIED deltas — `canonical-policy-migration`, `repo-boundary-governance`, `shared-contract-ownership` — and zero new capabilities), referenced at `docs/domain-to-neutral-promotion-process.md:302`; and `openspec/specs/canonical-policy-migration/spec.md:33-38` ("openxFactory SHALL own the canonical cross-factory role and authority model… their canonical responsibility, authority, and escalation boundaries MUST live in openxFactory").
- **Proposal reference:** ## What this creates that does not exist, bullet 1.
- **Fix:** rewrite as: "**Spec owner distinct from code owner AS A HELD ROLE** — absent. The adjacent prior art is REPOSITORY-grain, not role-grain: `2026-07-09-reconcile-domain-neutral-and-engineering-spec-ownership` settled which REPOSITORY owns neutral specs vs engineering implementation, and did so with three MODIFIED deltas and no new capability. What is genuinely absent is a NAMED, HELD, DELEGABLE role on either side. `canonical-policy-migration:33-38` already requires any such role's canonical authority to live in openxFactory."
- **Severity:** MISMATCH

**F9 — "The rule-setter ≠ rule-applier rationale lives only in a YAML comment and design prose" is false.**
- **Source:** `openspec/changes/add-substantive-review-lane/specs/roles-authority-model/spec.md:234` — "preserving the rule-setting/rule-applying separation," inside the ADDED requirement "Company-policy seat participation in per-PR councils," ratified 2026-08-22. (The proposal's grep over `openspec/specs/`, `docs/`, `contracts/` is correct as far as it goes — I reproduced zero hits — but it excluded the active ratified deltas the proposal elsewhere treats as authoritative.)
- **Proposal reference:** ## What this creates that does not exist, bullet 4.
- **Why it bites:** this change must archive *after* `add-substantive-review-lane`, so the rationale will be promoted requirement text before this change lands. The claim is stale on arrival.
- **Fix:** "…the rule-setter ≠ rule-applier rationale is **ratified requirement text awaiting promotion** (`add-substantive-review-lane/specs/roles-authority-model/spec.md:234`) and appears in no promoted spec today. Because this change archives after that one, the specs phase must treat it as promoted text and build on it rather than introduce it."
- **Severity:** MISMATCH

**F10 — ## Capabilities under-declares: reconciling the two contradicted statements requires deltas the section does not list.**
- **Source:** `openspec/specs/document-lifecycle/spec.md:96-108` (Explicit delta rule: any change to, contradiction of, or restatement of promoted policy must be an explicit change from current state; "accidental restatement… treated as a defect"). The two targets are `openspec/specs/doc-health/spec.md:572-575` and `docs/client-infrastructure-liaison.md:73-77` (governed by the `client-infrastructure-liaison` capability).
- **Proposal reference:** ## Capabilities; ## What this creates that does not exist, bullet 3.
- **Fix:** add under ### Modified Capabilities: "`doc-health`: the 'Authority never transfers' scenario (`:572-575`) is scoped to the semantic-sweep lane, so a recorded delegation instrument is outside it rather than an exception to it. A `client-infrastructure-liaison` delta is contingent on whether 'Ownership confers no authority' (`docs/client-infrastructure-liaison.md:73-77`) is scoped or amended; the specs phase declares it there."
- **Severity:** DRIFT

**F11 — Capability split: the role-definition half sits in a capability that already owns it.**
- **Source:** `openspec/specs/roles-authority-model/spec.md:9-14` (openxFactory owns "Hermes-level governance roles… escalation principles"); `openspec/specs/canonical-policy-migration/spec.md:33-38`; the realizing artifact is the `| ID | Role | Owns | Decides |` table at `docs/roles-and-authority.md:67-74`.
- **Proposal reference:** ### One capability or two, and why no schema.
- **Assessment:** the separability test is sound for the **instrument** — a revocable, attenuated, grant-composed delegation is genuinely new and mirrors the `openxwallet` / `openxwallet-agent-profile` seam correctly. It is not sound for "spec owner and code owner as distinct named roles," which is role definition, already owned, and already has a table to land in.
- **Fix:** add: "The two ROLES are added to `roles-authority-model` (the capability that owns Hermes-level role definition, `:9-14`, realized in `docs/roles-and-authority.md`'s Owns/Decides table) rather than to the new capability; `role-delegation-instrument` carries only the INSTRUMENT — the grant-composed, revocable delegation and its ceiling. The split is instrument-vs-role, not topology-vs-authority."
- **Severity:** DRIFT

---

## 3. The openxwallet composition claim

Field by field against `contracts/openxwallet/openxwallet-grant.schema.yaml`, every cited property is present at the cited lines: `audience` `:49-58` ✓, `scope.acts`/`scope.objects` `:59-79` ✓, `expires_at` `:88` ✓, `parent_grant_ref` with the exact quoted comment `:91-94` ✓, `revocation` with reason + `propagated_from` `:98-105` ✓. Spec citations `:25`, `:28-35`, `:43-47`, `:113-125`, `:121-125`, `:133-153` all exact. **The claim is right about what it enumerates.** It is incomplete about what the schema *requires*.

**F12 — `scope.authority_tier` is REQUIRED and closed-vocabulary, and the proposal's enumeration omits it — while its own ceiling requirement is an authority_tier claim.**
- **Source:** `contracts/openxwallet/openxwallet-grant.schema.yaml:61` (`required: [acts, authority_tier]`), `:79`, and the schema's own description `:25-27` ("`scope.authority_tier` is a tier from the custody registry's ladder"). The ladder is closed at four rungs: `attest`(0) / `request`(1) / `act`(2) / `act_unsupervised`(3) — `contracts/openxwallet/openxwallet-custody.registry.yaml:15-37`.
- **Proposal reference:** ### One capability or two, and why no schema, ground 2; ## What Changes, bullet "The delegable roles stop short of the terminal gate."
- **Why it bites:** "no delegated role discharges a terminal human gate" is exactly a statement about which rung a delegation grant may name. Stated in any other words it becomes the parallel authority vocabulary the proposal itself cites as barred (`openxwallet-agent-profile/spec.md:50-68`, verified exact). The vocabulary *can* carry it — `act` is "complete an effecting act, **with approval required before apply**" — but the proposal never says so.
- **Fix:** extend ground 2: "…carries `audience` (`:49-58`), `scope.acts`/`scope.objects` (`:59-79`), the REQUIRED `scope.authority_tier` (`:61`, `:79`) drawn from the closed four-rung ladder in `contracts/openxwallet/openxwallet-custody.registry.yaml:15-37`, `expires_at`, `parent_grant_ref` (`:91-94`) and `revocation` (`:98-105`). The ceiling this change asserts is expressed IN that vocabulary: a delegated owner's grant names `act` — 'complete an effecting act, with approval required before apply' — and never `act_unsupervised`. Saying it any other way would be the parallel vocabulary `openxwallet-agent-profile:50-68` forbids."
- **Severity:** MISMATCH

**F13 — Composition makes a wallet a prerequisite for holding a delegated governance role, and the delegate's custody model silently caps the delegation.**
- **Source:** `openxwallet-grant.schema.yaml:54-57` (`audience` requires `wallet_ref`; `holder_ref` is optional); `openspec/specs/openxwallet/spec.md:71-79` (custody caps authority); `openxwallet-custody.registry.yaml:52`, `:72`, `:94` (`holder_readable` and `isolated_invocable` both ceiling at `act`; only `isolated_per_use_authorized` reaches `act_unsupervised`). Cross-check `openspec/specs/openxwallet/spec.md:155-163` — wallets are meant to stay optional.
- **Proposal reference:** ## What Changes, bullet "Each of those roles is independently delegable…".
- **Assessment:** this is a gift the proposal leaves on the table — the custody ceiling enforces its own ceiling structurally, with no new rule. But it also means no wallet, no delegation.
- **Fix:** add: "Composition has a precondition and a bonus. Precondition: `audience.wallet_ref` is required (`:54-57`), so a delegate must hold a wallet with a declared custody model — delegation is unavailable to a party without one. Bonus: because custody caps authority (`openxwallet/spec.md:71-79`) and today's software custody ceilings at `act` (`openxwallet-custody.registry.yaml:52`, `:72`), an agent delegate CANNOT hold `act_unsupervised` — the terminal-gate ceiling is enforced by the custody registry, not only asserted here."
- **Severity:** DRIFT

**F14 — "Model it on consent-instrument" and "no new schema" are in direct tension: the grant schema cannot express an amendment.**
- **Source:** `openxwallet-grant.schema.yaml:95-97` (`state` enum is exactly `[active, expired, revoked]`), `:42` (`additionalProperties: false`), no amendment transition and no revocation-SLA field — against `openspec/specs/consent-instrument/spec.md:116-119` ("An amendment SHALL be a status transition carrying its delta on the existing instrument; a new instrument referencing a parent is **nonconformant**").
- **Proposal reference:** ## What this creates that does not exist, final bullet; ### One capability or two, and why no schema.
- **Why it bites:** under openxwallet, amending a delegation can only be revoke-and-reissue-as-derived — which `consent-instrument:116-119` calls nonconformant for instruments. The two recommendations cannot both be followed.
- **Fix:** add to the no-schema section: "One consent-instrument element is NOT expressible in the grant vocabulary: `state` is closed at `[active, expired, revoked]` (`:95-97`) under `additionalProperties: false` (`:42`), so an amendment can only be revoke-and-reissue-as-derived — which `consent-instrument:116-119` calls nonconformant for instruments. The specs phase must rule which grammar governs amendment, and 'model on consent-instrument' is therefore a recommendation about LIFECYCLE SHAPE, not about record structure."
- **Severity:** MISMATCH

**F15 (strengthening, not a defect)** — `distinct_holder_constraint_refs` (`:106-111`) is already the schema-level realization of spec-owner ≠ code-owner distinctness; the proposal cites the spec requirement (`openxwallet/spec.md:133-153`) but not the field that carries it. Naming it converts an assertion into a validated constraint. **DRIFT.**

---

## 4. The archive-ordering hazard

**Verified, and the proposal is right about the facts.** `openspec/specs/roles-authority-model/spec.md` carries exactly **11** requirements (`Neutral authority model ownership`, `Domain execution role instantiation`, `Human-attention escalation ladder`, `Interrupt legality`, `Non-interrupting conditions`, `Low-risk enforcement envelope`, `Parked-decision delivery`, `Structural parking in external enforcement`, `Domain instantiation of the ladder`, `GitHub App identity tiers`, `Administration-tier credential custody`) — none of them the floor or the pilot requirement. `add-substantive-review-lane/specs/roles-authority-model/spec.md` is a pure `## ADDED Requirements` delta of **10**, including both targets: "Pilot repository and reviewing domain" (`:149`) and "Constitutional floor for autonomous clearance" (`:323`). The hazard is real.

**F16 — The stated remedy is a disjunction where the ratified rule is a conjunction, and the first limb is not practically available.**
- **Source:** `openspec/specs/release-realization/spec.md:64-70` — "a proposal modifying a requirement already modified by an active ratified change **references that change AND declares its deltas relative to that change's outcome**" — with scenario `:72-74` making it a MUST. Separately, `add-substantive-review-lane` stands at 3 of 19 tasks complete with a three-repository `code_surface`, so under the Realization archive gate (`release-realization:22-32`) its archive is not near.
- **Proposal reference:** ## Impact, first bullet ("MUST archive after … **or** its delta must be restated").
- **Fix:** replace the "or" sentence with: "`release-realization:64-74` requires BOTH limbs, not a choice: this change MUST reference `add-substantive-review-lane` AND declare its deltas relative to that change's OUTCOME — i.e. against the requirement text as that delta will promote it, quoted in full in this change's own delta. Archive ordering is then an additional necessity, not a substitute: `add-substantive-review-lane` carries a three-repository code surface and stands at 3 of 19 tasks, so waiting on its archive is not a near-term option and the restatement is the operative mechanism."
- **Severity:** MISMATCH

Worth noting for the bench: the house already runs this pattern routinely — `implement-keycloak-install-repo` MODIFIES "Keycloak install repository boundary," a requirement ADDED by the still-active `add-identity-brokering`. So the hazard is normal and handled; it is only the either/or framing that is wrong.

---

## 5. Config-rule compliance

`openspec/config.yaml` contains exactly one line, `schema: spec-driven` — there are no `rules.proposal` or `rules.design` blocks to check. The binding rules are the promoted capabilities, and three of them fail.

**F17 — `.openspec.yaml` declares no origin. Strict validation MUST fail.**
- **Source:** `openspec/specs/document-lifecycle/spec.md:304-315` ("Every OpenSpec change proposal SHALL declare exactly one origin in its `.openspec.yaml`, fixed when the proposal is created"; ad-hoc requires `kind`, durable `id` of the form `<repo>:adhoc:<date>-<slug>`, `reason`, `approved_by`, `approved_on") and scenario `:330-332` ("WHEN a proposal's origin is **missing** … THEN strict proposal validation MUST fail"). Also `release-realization:97-103` (origin retention at archive) and `doc-health:641` (proposal-origin checks enforced by reference). Every peer complies: `add-substantive-review-lane`, `add-trust-anchor`, `admit-install-repos-to-aggregation`, `add-identity-brokering`. The subject's file is `schema` + `created` only.
- **Proposal reference:** `.openspec.yaml` (and the convener-direction sentence at proposal line 9, which is the reason text sitting in prose instead).
- **Fix:** add to `.openspec.yaml`:
  ```yaml
  origin:
    kind: ad_hoc
    id: openxFactory:adhoc:2026-08-22-add-assembly-plane-separation
    reason: >-
      Authored on direction from the convener the same day
      add-substantive-review-lane was ratified and the gate_rules_council
      returned its codexfactory-routine-code-clearance convening; this change
      acts on finding LS-A3 from that convening.
    approved_by: Brett Heap (openxFactory operator authority), 2026-08-22
    approved_on: 2026-08-22
  ```
- **Severity:** MISMATCH (hard gate)

**F18 — The change has no spec deltas, so `openspec validate --strict` fails outright; and the front-matter points at a `tasks.md` that does not exist.**
- **Source:** ran `OPENSPEC_TELEMETRY=0 openspec validate add-assembly-plane-separation --strict` → `✗ [ERROR] file: Change must have at least one delta. No deltas found.` Directory contains only `proposal.md` and `.openspec.yaml` — no `specs/`, no `tasks.md`, no `design.md`. Every peer active change carries all three.
- **Proposal reference:** front-matter line 2 ("tracked in `tasks.md`"); ## Capabilities (declares two new capabilities and one modified, none realized as deltas).
- **Fix:** either author `specs/assembly-plane-separation/spec.md`, `specs/role-delegation-instrument/spec.md`, `specs/roles-authority-model/spec.md` (+ `repo-boundary-governance` per F7) and `tasks.md` before circulating; or, if this is deliberately a proposal-only circulation, strike "and tracked in `tasks.md`" from the front-matter and state "spec deltas and tasks follow the bench's rulings on Q1–Q5."
- **Severity:** MISMATCH (hard gate)

**F19 — The realization-axis declaration is self-blocking for a spec-text-only change.**
- **Source:** `openspec/specs/release-realization/spec.md:7-12` (`code_surface:` is `none` or the repositories whose **runtime artifacts** it changes; `target_release:` is `implemented` or a **named release**; a proposal without declarations defaults to the doc-only pair) and `:14-16` ("WHEN a change alters only governance documents, schemas-as-documents, or contract prose → THEN its code_surface is `none`"). The archive gate at `:22-32` bars archive for a non-empty surface "until realization evidence exists: its code merged … and a green run of that surface."
- **Proposal reference:** front-matter `code_surface:` / `target_release:`; ## Impact bullet 3.
- **Why it bites:** the proposal declares `code_surface: openxFactory` while stating in the same sentence that it is "spec text only" and that every physical act is "downstream realization … each its own successor change." A non-empty surface therefore arms an archive gate this change can never discharge — or else pulls the successor changes' evidence back onto itself, contradicting bullet 3. Secondarily, `target_release: none` is outside the ratified vocabulary (the doc-only value is `implemented`); note `add-substantive-review-lane` and `add-model-provider-broker` share that slip, so the vocabulary point is habit, not novelty.
- **Fix:**
  ```
  code_surface: none — this change's own diff is spec text in openxFactory only …
    The physical work it authorizes but does NOT perform … is downstream
    realization named in ## Impact, each act its own successor change carrying
    its OWN code_surface and archiving on merged, green evidence per
    release-realization.
  target_release: implemented (the doc-only pair; no contract bundle is cut)
  ```
- **Severity:** MISMATCH (the `code_surface` half); DRIFT (the `target_release: none` vocabulary half)

**F20 — Not listed in the README OpenSpec Records block.**
- **Source:** `README.md:303-305` (`## OpenSpec Records` → `Active changes:`); peers listed at `:384`, `:471`, `:562`. House rule in `/home/brett/projects/xFactory/CLAUDE.md`. The change is still untracked, so this is pending rather than violated.
- **Fix:** add `- [add-assembly-plane-separation](openspec/changes/add-assembly-plane-separation/proposal.md)` with its one-line summary to the Active changes block in the same commit that adds the change folder.
- **Severity:** DRIFT

`Status: draft` (proposal line 8) is a legal value under `document-lifecycle:33` — clean.

---

## 6. Citation accuracy

**This dimension is close to clean, and both self-declared corrections check out.**

Both corrections **VERIFIED**:
- *"the floor is 35 patterns not 14"* — I counted `never_clearable_paths` in `codexfactory-routine-code-clearance.yaml` (branch `change/add-regular-pr-council-clearance`): 7 canonical (`:61-67`) + `.github/**` (`:79`) + 6 agent-instruction (`:83-88`) + 4 executable/attribute (`:98-102`) + 8 agent-tool markdown (`:110-117`) + 8 agent-tool dirs (`:118-125`) + `.sonarlint/**` (`:126`) = **exactly 35**, block spanning `:59-127`. `:61` is `- "scripts/**"  # the decision core's whole import root`, quoted verbatim. (14 was the pre-widening count — consistent with LS-A3's "seven canonical entries" probe set.)
- *"the import-root test moved to `test_generalized_core.py:504-521`"* — `test_every_import_root_of_the_core_is_covered_by_the_floor` is at that file, section banner `:504`, `def` `:507`, docstring "Computed at run time, so a NEW import root fails this test" `:508`, body through `:522`.

Seven further samples, all exact: `add-substantive-review-lane/specs/roles-authority-model/spec.md:155` and `:336-337`; `.github/CODEOWNERS:29` (`/scripts/ @brettheap`), `:11-20` (the `scripts/yaml.py` note, verbatim) and `:5-9`; `council-convening-lane.yml:36-45` (the migration-pin/foreign-repository reasoning, verbatim) and `:47-53` (three-identity separation); `lead-security.md:154-160` (LS-A3, including "A bench must not adopt a control on a description of an enforcement that does not enforce it" at `:158`); `omnigent-domain-overlay.schema.yaml:16-17` and `:403-406`; `doc-health/spec.md:572-575`; `client-infrastructure-liaison.md:73-77`; `consent-instrument/spec.md:100-113`; `ideation/staging/INDEX.md:68` and `:70`; the negative example `:12-14`. Two absence claims also verified true: no validator anywhere in `scripts/`, `openspec/specs/`, `contracts/` reads CODEOWNERS (zero hits), and "four of five seats" matches the five seat-return files and the ratification record's own line.

**F21 — Three range nits, none material.**
- `:323-338` for the constitutional floor stops mid-requirement; the requirement runs `:323-344`. → cite `:323-344`.
- `test_generalized_core.py:504-521` undershoots the assert message by one line. → cite `:504-522`.
- `consent-instrument/spec.md:30-47` is appended to a five-item list ("executed/amended/terminated lifecycle, revocation right with SLA, amendments as transitions, termination cascading, the instrument as authority-chain root") but covers only the last item; amendments-as-transitions is at `:116-119`. → cite per item, or move `(:30-47)` to sit only against "authority-chain root."
- **Severity:** DRIFT

---

## Summary

| # | Dimension | Severity |
|---|---|---|
| F1 | fifteenth → nineteenth submodule | MISMATCH |
| F2 | three-plane premise vs openxFactory's ratified spec+code co-residence | MISMATCH |
| F3 | gate RULES are canonically openxFactory's, not the assembly repo's | DRIFT |
| F4 | Q5 omits the moving-runtime-code / submodule-pointer stop condition | MISMATCH |
| F5 | wrong boundary template (install scope vs avatar-client boundary) | DRIFT |
| F6 | no Domain-Hermes surrender gate for the core's move | DRIFT |
| F7 | repo-boundary-governance delta deferred against an 8-instance precedent | DRIFT |
| F8 | spec-owner/code-owner "silence" overlooks archived prior art | MISMATCH |
| F9 | rule-setter ≠ rule-applier IS ratified requirement text | MISMATCH |
| F10 | ## Capabilities under-declares the doc-health reconciliation | DRIFT |
| F11 | role definitions belong in roles-authority-model, not a new capability | DRIFT |
| F12 | `scope.authority_tier` required + closed ladder, omitted | MISMATCH |
| F13 | wallet prerequisite + custody ceiling unsurfaced | DRIFT |
| F14 | consent-instrument amendments not expressible without a schema | MISMATCH |
| F15 | `distinct_holder_constraint_refs` unused | DRIFT |
| F16 | archive-ordering remedy is or-where-the-rule-is-and | MISMATCH |
| F17 | `.openspec.yaml` missing origin — strict validation MUST fail | MISMATCH |
| F18 | no spec deltas — `openspec validate --strict` fails; dangling tasks.md | MISMATCH |
| F19 | `code_surface: openxFactory` self-blocks archive; `target_release: none` off-vocabulary | MISMATCH / DRIFT |
| F20 | not in README OpenSpec Records | DRIFT |
| F21 | three citation range nits | DRIFT |

**Blocking before circulation:** F17, F18, F19 (the change cannot validate or archive as it stands). **Blocking before ratification:** F2, F9, F12, F14, F16 — each is a factual claim the bench would otherwise adopt on a false premise, which is precisely the failure mode the proposal's own LS-A3 quotation warns against.
