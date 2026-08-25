Reviewer: QA Lead — alignment review against openxFactory ratified requirements. Date: 2026-08-22.
Subject: `openspec/changes/add-assembly-plane-separation/proposal.md`

# QA Lead review — `add-assembly-plane-separation`

**Reviewed against:** promoted specs in `openspec/specs/` (there is indeed no `docs/requirements/`), the ratified-but-active `add-substantive-review-lane` delta, `contracts/openxwallet/`, `contracts/omnigent/`, and the live codexFactory artifacts on `origin/main`.

**Headline:** the external-citation accuracy is unusually good — I spot-checked ~30 line-anchored citations and the codexFactory-side ones (the 35-pattern floor, `CODEOWNERS:29`, LS-A3, the convening-lane comment block, the import-root test) all resolve exactly. The failures are concentrated in three places: **the proposal contradicts itself on the constitutional floor**, **the delegation instrument's doctrinal reconciliation does not actually hold**, and **the change packet is structurally non-conformant** (no `specs/`, no `tasks.md`, no `origin:` block; `openspec validate --strict` fails).

---

## 1. Requirement citation accuracy

Verified accurate (no action): `add-substantive-review-lane/specs/roles-authority-model/spec.md:155` ("a pull request's diff is software regardless of the domain" — the sentence begins on :154, ends on :155); the constitutional floor at `:323`+ with the human-only clause at `:336-337`, quoted verbatim; `openxwallet/spec.md:25`, `:28-35`, `:43-47`, `:113-125`, `:121-125`, `:133-153`; `openxwallet-agent-profile/spec.md:50-68`; `openxwallet-grant.schema.yaml` `audience` `:49-58`, `scope` `:59-79`, `parent_grant_ref` `:91-94` (quote exact), `revocation` `:98-105`; `omnigent-domain-overlay.schema.yaml:16-17` and `:403-406`; `docs/roles-and-authority.md:74` (the Owns/Decides table row) and `:260-268`; `repo-boundary-governance:41-58`; `shared-contract-ownership:33-44`; `ideation/staging/INDEX.md:68` and `:70` (both quotes exact, `contract-v1.31` confirmed); `codexFactory .github/CODEOWNERS:29` and its `:11-20` note; the 35-pattern floor at `:59-127` with `"scripts/**"` at `:61`; `tests/merge-master/test_generalized_core.py` (fn at :507, docstring :508); `council-convening-lane.yml:36-45` and `:47-53`; LS-A3 at `lead-security.md:154-160`. Also verified true: the three "silence" greps (`spec owner`/`code owner`, `rule-setting`/`rule-applying`, CODEOWNERS-read-by-a-validator) all return nothing today.

**Finding 1.1** — The proposal states `codexfactory-routine-code-clearance` "is mid-activation with **five gate entries outstanding**"; the ratifying record it cites says the activation gate was extended from five entries to **fourteen**, of which ratification satisfies exactly one.
**Requirement source:** codexFactory `hermes/domain/review-councils/records/2026-08-22-gate-rules-regular-pr-council-clearance.md` — "`activation_gate.requires` extended from five entries to fourteen" (amendment R10), and §3 Verdict: "ratification satisfies exactly one of the activation gate's entries"; the additions table lists nine new conditions ("The five entries the rule shipped with stand unchanged; these nine are added").
**Proposal reference:** Q5 — Migration path and ordering.
**Fix:** "…is mid-activation with **thirteen of fourteen** activation-gate entries outstanding (five as shipped plus nine added by the 2026-08-22 amendments R10; ratification discharged one)."
**Severity:** MISMATCH

**Finding 1.2** — The proposal claims the rule-setter ≠ rule-applier rationale "has never been promoted requirement text," but the sibling change it declares it must archive behind promotes exactly that phrase.
**Requirement source:** `add-substantive-review-lane/specs/roles-authority-model/spec.md:236` — "preserving the rule-setting/rule-applying separation," inside the ADDED requirement "Company-policy seat participation in per-PR councils."
**Proposal reference:** "What this creates that does not exist" — the "general rule that a body may not review its own machinery" bullet.
**Fix:** Restate as "…lives only in a YAML comment and design prose today; `add-substantive-review-lane` promotes the phrase as *rationale* inside its company-policy-seat requirement but states no general rule, so the general rule remains a silence after that change archives."
**Severity:** MISMATCH

**Finding 1.3** — The "single shared reviewing home" citation `:149-163` stops short of the scenario that actually makes it enforceable.
**Requirement source:** `add-substantive-review-lane/specs/roles-authority-model/spec.md:176-182`, Scenario "No second persona home is instantiated."
**Proposal reference:** ## Why, second paragraph.
**Fix:** Cite `:149-182`, or `:152-157` for the clause plus `:176-182` for the scenario.
**Severity:** MISMATCH (minor)

---

## 2. The doctrinal conflicts — the load-bearing claim does **not** hold

Locations first. **"Authority never transfers"** is at `openspec/specs/doc-health/spec.md:572-575` ✓ — but it is a **`#### Scenario:` heading**, not requirement text, sitting under "Candidates become staged proposals under human approval" (:557), and its body is scoped entirely to the neutrality-drift lane ("content authority stays with the owning factory"). **"Ownership confers no authority"** is at `docs/client-infrastructure-liaison.md:73-77` ✓. The **anti-stand-in fixture** quote at `:12-14` ✓ is exact, though the fixture says laundering onto *the audience*, not "the owner."

**Finding 2.1 (the central one)** — "Act as itself under a recorded grant, never as the owner" reconciles with the anti-stand-in fixture but **does not touch** "Authority never transfers," because the two statements are on different axes. The fixture governs **attribution** (who the audit record names as actor); doc-health's scenario governs **conferral** (whether authority moves at all). The proposal's formulation answers the attribution question and then presents that answer as settling both. A delegate acting as itself under its own grant has still *received an authority it did not previously hold* — which is precisely what "Authority never transfers" denies in its own frame.
**Requirement source:** `openspec/specs/doc-health/spec.md:572-575` vs. `contracts/openxwallet/examples/negative/exercise-attributed-to-a-wallet-not-presenting-its-key.yaml:12-14` (requirement OXW-R5, `openspec/specs/openxwallet/spec.md:93-111`).
**Proposal reference:** ## What Changes, bullet 6; ## One capability or two, "must overturn two standing statements."
**Fix:** Split the reconciliation into two arguments rather than one. For the fixture: keep "acts as itself under its own attenuated grant" — it is correct and sufficient. For doc-health: the reconciling argument is **scoping, not attribution** — doc-health's scenario bars a *reporting lane* from acquiring editing authority *implicitly, by discovery*; a recorded, audience-named, expiring, revocable grant is *explicit conferral by the holder*, a different act. State that as the scoping argument and say so in the specs phase.
**Severity:** MISMATCH

**Finding 2.2** — "Ownership confers no authority" is not merely doc prose; it is **promoted requirement text**, so scoping or amending it requires a `client-infrastructure-liaison` MODIFIED delta the proposal does not declare and does not mention in its otherwise careful "adjacent capability not declared" bookkeeping.
**Requirement source:** `openspec/specs/client-infrastructure-liaison/spec.md:17-30` — Requirement "Coordination, execution, and validation separation," Scenario "Ownership does not confer authority" (:28-30). (`docs/client-infrastructure-liaison.md` carries `Status: ratified` / `Ratified by: add-client-infrastructure-liaison`.)
**Proposal reference:** "What this creates that does not exist," delegation bullet; ## Impact, "Adjacent capability not declared as modified, deliberately."
**Fix:** Cite the promoted spec (`client-infrastructure-liaison/spec.md:28-30`) alongside the doc, and add a third entry to the Impact bookkeeping stating whether a `client-infrastructure-liaison` MODIFIED delta is contingent or explicitly unnecessary — with the reason. The available reason is strong: under that requirement authority already comes from *the binding's approved execution owner and grant*, never from ownership, so a delegated code owner whose authority is entirely in its grant **conforms** to the liaison doctrine rather than overturning it.
**Severity:** GAP

**Finding 2.3** — The proposal names two governance roles "spec **owner**" and "code **owner**" while the corpus reserves "ownership" for a relation that explicitly confers no authority, and then says the delegated code owner is "a reviewer with real standing." The vocabulary collision is avoidable and will re-litigate itself at every future reading.
**Requirement source:** `openspec/specs/client-infrastructure-liaison/spec.md:28-30`; reinforced structurally at `docs/client-infrastructure-liaison.md:79-82` ("`execution_binding.actor_ref` is never equal to `approval.authority_ref` nor to the coordinating creator").
**Proposal reference:** ## What Changes, bullet 5; ## Capabilities, `role-delegation-instrument`.
**Fix:** Rename to *spec authority* / *code authority* (or *spec steward* / *code steward*), and state that the standing is carried by the grant, not by the ownership label. Additionally check the delegated code authority against the three-parties-never-collapsed rule: a delegate that both reviews and approves collapses `actor_ref` into `authority_ref`.
**Severity:** MISMATCH

**Finding 2.4** — The proposal simultaneously says it "must overturn" `doc-health`'s statement and declares no `doc-health` MODIFIED capability; under the ratified explicit-delta rule an unmarked contradiction of a promoted spec is a health finding.
**Requirement source:** `openspec/specs/document-lifecycle/spec.md:96-113` — Requirement "Explicit delta rule" and Scenario "Prose contradicts a promoted spec" ("health tooling MUST report unmarked contradictions as findings").
**Proposal reference:** ## One capability or two, ¶1.
**Fix:** Replace "must overturn two standing statements" with "must reconcile with two standing statements by scoping" (the honest and, per 2.1, achievable position), and record in ## Impact that neither `doc-health` nor `client-infrastructure-liaison` needs a MODIFIED delta *because* the reconciliation is by scoping — or declare the deltas.
**Severity:** GAP

**Finding 2.5** — The claim that a role delegation "is expressible in that vocabulary today" understates what the grant vocabulary obliges. `scope` **requires** `authority_tier` (an identifier from a registry the proposal never names); `audience` **requires** a `wallet_ref`, so every delegate must hold a wallet with a declared custody model; and every *exercise* must carry proof of possession and a key-attributed record. A delegated code owner casting a GitHub review produces no wallet-signed exercise.
**Requirement source:** `contracts/openxwallet/openxwallet-grant.schema.yaml:59-61` (`required: [acts, authority_tier]`), `:53-57`; `openspec/specs/openxwallet/spec.md:49-69` (proof of possession), `:71-91` (custody caps authority), `:93-111` (every exercise key-attributed).
**Proposal reference:** ## One capability or two, ground 2.
**Fix:** Add to that paragraph: the composing capability must state which `authority_tier` identifiers the delegation uses, that every delegate is a wallet holder with a declared custody model, and what constitutes an *exercise* of a delegated role (and therefore what carries the proof of possession and the key-attributed record) — or explicitly scope the delegation instrument as a grant that is *recorded* but whose exercise is evidenced by the existing council/enforcement audit trail, naming that as a deviation.
**Severity:** GAP

---

## 3. `consent-instrument` as prior art

The sole-operator passage verifies exactly: Requirement "Authority Basis Is First-Class" (`:100-105`) and its Scenario (`:107-113`) carry "one person controls multiple rungs of an engagement (the Meds Rx case)" and "a shared signer across rungs is a recorded SHOULD deviation, not a silent one." The proposal's characterisation of it — a *disclosure* answer, not a *structural* one — is fair and correctly stated as the opposite of what it proposes.

**Finding 3.1** — The lifecycle-grammar citation `(:30-47)` is attached to five elements, four of which live elsewhere in the file, and the lifecycle it quotes is incomplete in a way the spec explicitly forbids.
**Requirement source:** `openspec/specs/consent-instrument/spec.md` — revocation right with SLA at `:6-13`; authority-chain root at `:30-47`; the lifecycle enum at `:69-98`, which is `draft → pending_signatures → executed → amended → terminated` **plus `withdrawn` as a DISTINCT second terminal state that "MUST NOT be declared as an alias of `terminated`"**; amendments-as-transitions at `:115-126`; termination cascade at `:150-174`.
**Proposal reference:** "What this creates that does not exist," final bullet.
**Fix:** Replace the single `(:30-47)` with the five real anchors, and write the lifecycle as the full six-state enum including `withdrawn`.
**Severity:** MISMATCH

**Finding 3.2 (assessment, and the more serious half)** — "Model the instrument on `consent-instrument`" and "express the instrument in the openxwallet grant vocabulary" are **mutually incompatible recommendations**, and the proposal makes both. `consent-instrument` requires that an amendment be a *status transition on the existing instrument* and declares "a new instrument referencing a parent is nonconformant." The openxwallet grant model narrows *only* by deriving a new grant carrying `parent_grant_ref`. The two lifecycles are also different closed enums (`draft/pending_signatures/executed/amended/terminated/withdrawn` vs. the schema's `state: [active, expired, revoked]`). Modelling on one while realizing as the other produces precisely the "parallel authority vocabulary" that is a declared validation failure.
**Requirement source:** `openspec/specs/consent-instrument/spec.md:115-118` ("Amendments Are Transitions, Never New Instruments") and `:69-78`; `contracts/openxwallet/openxwallet-grant.schema.yaml:91-94` and `:95-97`; `openspec/specs/openxwallet-agent-profile/spec.md:50-68` ("a parallel authority vocabulary is a validation failure").
**Proposal reference:** "What this creates that does not exist," final bullet vs. ## One capability or two, ground 2.
**Fix:** Drop the "modelled on `consent-instrument`" recommendation and keep the grant realization. **My assessment on your question:** the delegation instrument is **genuinely separate** — `consent-instrument` governs subject consent between *party-ladder rungs of a client engagement*, with signed-original custody, execution-evidence kinds, and third-party estate hosts; an internal governance-role delegation has no consenting subject and no party ladder, so MODIFYING that capability would force an ill-fitting framing onto it. Keep `consent-instrument` as a *named non-precedent* (the proposal already does this well for the sole-operator case), and take the lifecycle grammar from openxwallet, which the proposal has already correctly identified as the realization vocabulary. The proposal **over-claims** the overlap: what it borrows from `consent-instrument` is a shape openxwallet already supplies. Note also `consent-instrument:176` ("The Signed Original Never Enters A Product Repo") — an obligation the "modelled on" route would import into a change whose entire subject is which repository things live in.
**Severity:** MISMATCH

---

## 4. Acceptance criteria / testability

Testable as written: bullet 2 (one declared assembly repository — a count over a registry); bullet 3 (given a candidate in the assembly repo, no council-verdict check-run may satisfy its review gate); bullet 7 (`execute_final_action` is already `const: false` at schema level and enforced).

**Finding 4.1** — The Q4 "external reviewer" test does not exclude the failure mode it was written to exclude. A **fork** of the assembly repository is a different repository with an independent pin, and satisfies both prongs while sharing 100% of the packet builder, seat prompts and gate machinery — the exact thing the proposal says "shares the failure mode whatever weights it runs." "Different codebase" is also undefined against forking, vendoring, and copy-at-a-different-path.
**Requirement source:** the enforceable primitives already exist and are unused here — `openspec/specs/openxwallet-agent-profile/spec.md:6-26` ("An agent holder declares its composition … as a hash over a declared component set … model version, prompt contract, tool manifest, policy version, parameters, and retrieval corpus"), and `openspec/specs/shared-contract-ownership/spec.md:84-91` and `:101-103` (content-addressed pinning: "the tag alone is not a content-addressed pin").
**Proposal reference:** Q4.
**Fix:** State the test content-addressably: a reviewer is external to assembly repository *A* at commit *c* iff **(i)** its declared agent-composition component set (per `openxwallet-agent-profile`) shares no component whose content digest appears in *A*'s manifest at *c* — which excludes a fork — **and (ii)** it resolves its own machinery from a pin naming a different repository *and* a disjoint digest set. Say explicitly that a fork fails prong (i).
**Severity:** GAP

**Finding 4.2** — Bullet 5 ("spec owner and code owner become distinct roles by construction") has no observable. The proposal itself establishes there is no role-owns-artifact concept in the corpus and that no validator anywhere reads CODEOWNERS, so nothing records who either owner *is*, and "distinct by construction" cannot be checked.
**Requirement source:** by absence — no promoted requirement carries a role↔artifact ownership record (verified; `roles-authority-model:113` and `docs/roles-and-authority.md:179` use "code-owner" only as GitHub path scoping).
**Proposal reference:** ## What Changes, bullet 5.
**Fix:** Name the carrier and the check. The natural home is the per-repo `stack.yaml` (the corpus's existing machine-readable declaration surface, already carrying `specializes` / `promoted_from`), with the check being "the declared spec-authority holder and code-authority holder of a governed unit resolve to records in different repositories."
**Severity:** GAP

**Finding 4.3** — Bullet 6 ("independently delegable by a written, recorded, revocable instrument") names no location, no registry, and no validator, and the proposal declines a schema. As written there is no artifact a test could assert on.
**Requirement source:** `openspec/specs/release-realization/spec.md:22-32` — a change with a code surface archives only on realization evidence; an unlocatable instrument produces none.
**Proposal reference:** ## What Changes, bullet 6; ## One capability or two, ground 1.
**Fix:** Even with no new schema, the specs phase must fix (a) the delegation record's repository and path, (b) which existing validator reads it, and (c) the revocation check performed at exercise (`openxwallet/spec.md:113-119` requires checking revocation *at exercise*, not at issuance). Add these as three named obligations of the `role-delegation-instrument` capability.
**Severity:** GAP

**Finding 4.4** — Bullet 1 ("every governed unit is declared to split across three repository planes") has no declaration carrier; bullet 8's retirement trigger ("a green convening runs entirely from the new home") has no artifact that evidences "entirely from the new home."
**Proposal reference:** ## What Changes, bullets 1 and 8.
**Fix:** For bullet 1, name `stack.yaml` (or the aggregation `.gitmodules` plus a plane field) as the carrier. For bullet 8, define the evidence as a council record whose provenance field names the assembly repository at a pin, and say a convening record lacking that field does not discharge the retirement gate.
**Severity:** GAP

---

## 5. Requirement coverage — in-scope requirements not addressed

**Finding 5.1 (highest severity in this review)** — The proposal contradicts itself on the constitutional floor. ## Impact asserts "The floor stays exactly as ratified; the assembly plane inherits it whole" and ## Out of scope says the floor is "untouched" — but ## What Changes bullet 3 permits "an AI reviewer demonstrably NOT assembled from it" to review the assembly plane, and ## Capabilities re-expresses the floor's "gate or workflow definitions" clause as a repository predicate. The assembly plane holds "the council reusable workflows … and the gate-rule machinery" — i.e. gate and workflow definitions — which the ratified floor makes **permanently human-only regardless of unanimity**, with no AI exception of any kind.
**Requirement source:** `add-substantive-review-lane/specs/roles-authority-model/spec.md:335-337` and Scenario "Permanently human-only surfaces" (:352-357): "no verdict under it SHALL ever produce an autonomous approval."
**Proposal reference:** ## What Changes bullet 3; ## Capabilities → Modified; ## Impact final bullet; ## Out of scope bullet 4.
**Fix:** Choose one and make the whole document consistent. The honest reading of the ratified floor is that Q4's answer is **already decided**: the assembly plane is permanently human-only, and no "demonstrably external AI" clause is available without a declared floor amendment. Either (a) delete the "or an AI reviewer demonstrably NOT assembled from it" clause and reframe Q4 as "what enforceable definition of external would a *future* floor amendment need?", or (b) declare the floor amendment openly in the MODIFIED `roles-authority-model` delta and delete the "no existing gate is weakened" and "floor untouched" claims.
**Severity:** MISMATCH

**Finding 5.2** — Re-expressing the floor's "gate or workflow definitions" clause as a **repository** predicate is a substantive weakening, not a re-expression. Every CODE-plane repository keeps its own caller workflows, ruleset config and code-ownership map; openxFactory keeps `contracts/` (contract bytes) and credential templates. Under a repository predicate those cease to be floored. codexFactory's own live rule is direct counter-evidence: `.github/**` was added to the never-clearable floor precisely because "this directory holds the workflows, the envelope config and the code-ownership map that define the gate itself."
**Requirement source:** `add-substantive-review-lane/specs/roles-authority-model/spec.md:335-337`; codexFactory `scripts/merge_master/codexfactory-routine-code-clearance.yaml:70-79`.
**Proposal reference:** ## Capabilities → Modified Capabilities, `roles-authority-model`.
**Fix:** Make it **additive**: the repository predicate is a *second, structural* floor member ("any candidate in the assembly repository"), and the four path-shaped clauses stand unchanged. Say "gains a repository predicate" rather than "is re-expressed as a repository predicate."
**Severity:** MISMATCH

**Finding 5.3** — The proposal cites the **wrong** `repo-boundary-governance` requirement as the template for a new repository, and misses the two that actually govern the act.
**Requirement source:** `openspec/specs/repo-boundary-governance/spec.md:29-40` ("Install repository scope") is about `Hermes-Install`/`Omnigent-Install` being scoped to install/ops/backup/restore/upgrade/DR — it is not a template for declaring a new repository's scope. The real precedents are `:113-137` ("Neutral avatar-client repository boundary" — a private, independently released repository created by a named successor change, with an explicit from-creation ownership list and an explicit MUST-NOT-contain list) and `:165-181` ("Deferred aggregation and web-console integration" — "Adding … to the top-level xFactory aggregation SHALL require a separate reviewed change that records path, remote, visibility, exact validated commit, checkout, compatibility, update, and rollback behavior"), with `:90-111` ("Neutral installer repository integration") as the generic pinning shape.
**Proposal reference:** ## Impact, "Adjacent capability not declared as modified, deliberately."
**Fix:** Replace the `:29-40` citation with `:113-137` as the scope-declaration template and `:165-181` as the binding obligation on the aggregation-submodule act; note that `:165-181` already imposes the eight-element record (path, remote, visibility, exact validated commit, checkout, compatibility, update, rollback) on the Q1-contingent submodule admission, so that work is *specified* even before Q1 is ruled.
**Severity:** MISMATCH

**Finding 5.4** — `repo-boundary-governance`'s stop-condition rule is unaddressed, and the assembly move trips it on two counts.
**Requirement source:** `openspec/specs/repo-boundary-governance/spec.md:59-76` — "Guarded pilot execution": "Later dogfood migration features SHALL keep the same stop conditions," and Scenario "Dogfood migration feature reaches a stop condition" — "WHEN a dogfood migration feature proposes deleting source docs, **moving runtime code, changing submodule pointers**, or touching generated state THEN the feature MUST stop and return to Hermes approval before implementation continues."
**Proposal reference:** Q5; ## Impact, downstream realization bullet.
**Fix:** Add to Q5: "the physical move is a declared stop condition under `repo-boundary-governance:74-76` on two counts (runtime-code movement, submodule pointer change), so each realization successor MUST carry a recorded Hermes approval before implementation, in addition to the copy-first discipline already cited."
**Severity:** GAP

**Finding 5.5** — Q3 proposes extending `shared-contract-ownership`'s "Contract version pinning" but declares no MODIFIED delta for it and gives it no contingency note, unlike the careful notes written for `repo-boundary-governance` and `openxwallet`. The requirement as promoted binds only *install repositories* pinning *contracts*, and says nothing about a code/assembly pin.
**Requirement source:** `openspec/specs/shared-contract-ownership/spec.md:33-44`; the better-fitting shape the proposal misses is `:84-91` and `:101-103`, which already require "the exact openxFactory commit and per-file digests" and rule that a tag alone is not a content-addressed pin — exactly the strength Q3's "consumer pin" and Q4's "independent pin" both need.
**Proposal reference:** Q3; ## Impact.
**Fix:** Add a third entry to the "adjacent capability not declared as modified" bookkeeping stating that a `shared-contract-ownership` MODIFIED delta generalizing "Contract version pinning" beyond install-repos-and-contracts is contingent on Q3, and cite `:84-91`/`:101-103` as the content-addressed pin shape rather than `:33-44` alone.
**Severity:** GAP

**Finding 5.6** — The change packet has **no `origin:` block**, which strict proposal validation must fail.
**Requirement source:** `openspec/specs/document-lifecycle/spec.md:304-332` — "Proposal origin declaration": "Every OpenSpec change proposal SHALL declare exactly one origin in its `.openspec.yaml`," with Scenario "The proposal gate rejects a malformed origin" — "WHEN a proposal's origin is missing … THEN strict proposal validation MUST fail." Reinforced by `openspec/specs/release-realization/spec.md:97-116` ("Origin retention at archive").
**Proposal reference:** `openspec/changes/add-assembly-plane-separation/.openspec.yaml` — contains only `schema: spec-driven` and `created: 2026-08-22`.
**Fix:** Add an `ad_hoc` origin block modelled on the sibling's (`add-substantive-review-lane/.openspec.yaml`): `kind: ad_hoc`, `id: openxFactory:adhoc:2026-08-22-add-assembly-plane-separation`, `reason`, `approved_by: Brett Heap`, `approved_on: 2026-08-22`. The proposal body already contains the reason and the approval provenance — it just is not in the machine-readable slot. Fix before ratification: the origin is immutable once fixed, and it cannot be added later without a mutation the archive gate rejects.
**Severity:** GAP

**Finding 5.7** — The packet is the only active change in the repo with no `specs/` and no `tasks.md`; `OPENSPEC_TELEMETRY=0 openspec validate add-assembly-plane-separation --strict` fails with "Change must have at least one delta." The frontmatter also refers to realization "tracked in `tasks.md`" — a file that does not exist.
**Requirement source:** `openspec/config.yaml` (`schema: spec-driven`); all 18 other active changes carry `proposal.md + specs/ + tasks.md`.
**Proposal reference:** frontmatter, `code_surface:`; ## Impact.
**Fix:** Expected if this is a deliberate proposal-first review stage — but say so in the Status line, and either create `tasks.md` or change the frontmatter to "named in ## Impact and tracked in `tasks.md` **when the specs phase runs**."
**Severity:** GAP

**Finding 5.8** — The sequencing remedy the proposal chooses is not the one the ratified requirement prescribes. `release-realization` says a later proposal touching a requirement an active ratified change already modifies **declares its deltas relative to that change's outcome** — available now, and it dissolves the archive-ordering constraint entirely. The proposal treats archive-ordering as primary and restatement as a fallback.
**Requirement source:** `openspec/specs/release-realization/spec.md:64-74` — "Ordered deltas and branch vocabulary," Scenario "Two changes touch one requirement": "THEN the later proposal MUST reference the earlier change and declare its deltas relative to that change's outcome."
**Proposal reference:** ## Impact, first bullet.
**Fix:** Invert the framing: "Per `release-realization:64-74` this change declares its deltas relative to `add-substantive-review-lane`'s outcome, which is the ratified requirement rather than an option; the archive-ordering note below is a consequence, not the remedy." The proposal's diagnosis is right and well flagged — only the prescription is off.
**Severity:** MISMATCH (minor)

**Clean:** `Status: draft` in the proposal body conforms to `document-lifecycle:33-37`'s controlled taxonomy. (`target_release: none` is not one of the two values `release-realization:6-12` admits — `implemented` or a named release — but ~70 archived changes and the ratified sibling use the same spelling, so this is a corpus-wide condition, not this proposal's defect.)

---

## 6. Capabilities contract

**Finding 6.1** — `role-delegation-instrument` defining two new neutral governance roles collides with `roles-authority-model`'s promoted ownership of exactly that.
**Requirement source:** `openspec/specs/roles-authority-model/spec.md:9-14` — "Requirement: Neutral authority model ownership": "`openxFactory` SHALL own the cross-factory authority model: the authority layers, **Hermes-level governance roles** (project ownership, sequencing, system and project architecture, merge readiness and merge authority), escalation principles, and external enforcement concepts."
**Proposal reference:** ## Capabilities → New Capabilities, `role-delegation-instrument`.
**Fix:** Split along the seam that already exists in the corpus. The **role definitions** (spec authority, code authority, and where they sit in the Owns/Decides table at `docs/roles-and-authority.md:67-74`) belong in the `roles-authority-model` MODIFIED delta the proposal already declares. The **instrument mechanics** stay in the new capability — best shaped as an openxwallet *composing profile*, the structural seam the proposal itself correctly identifies via `openxwallet-agent-profile`. This preserves the separability argument (which is otherwise sound: either half is independently ratifiable, and the doctrinal argument does deserve its own review) while respecting the ownership requirement.
**Severity:** GAP

**Finding 6.2** — The MODIFIED `roles-authority-model` delta description mixes a genuine requirement change with a mischaracterisation. "The lane's single-shared-reviewing-home requirement gains its structural counterpart" is a real requirement change and correctly stated. "The constitutional floor's 'gate or workflow definitions' clause is re-expressed as a REPOSITORY predicate rather than a candidate-class path predicate" is a *narrowing* presented as a re-expression — see 5.2 — and it directly contradicts the Out-of-scope bullet ("the constitutional floor and the candidate classes are untouched").
**Requirement source:** `add-substantive-review-lane/specs/roles-authority-model/spec.md:335-337`, `:352-357`.
**Proposal reference:** ## Capabilities → Modified Capabilities; ## Out of scope, bullet 4.
**Fix:** Per 5.2, restate as additive, and delete or qualify the Out-of-scope bullet so the document does not both claim and disclaim a floor change.
**Severity:** MISMATCH

**Clean:** `assembly-plane-separation` maps cleanly to real spec-delta obligations (topology declaration, single-assembly-repository rule, disqualification-by-construction, external-reviewer definition, consumer-pin obligation) — no content or execution work masquerading as a capability. The two-way split is justified on the separability test as stated, subject to 6.1's boundary correction. The no-schema argument is sound on both grounds and the rule-of-three precedent at `INDEX.md:68` is quoted exactly and applies directly. The `openxwallet`-not-declared-as-modified paragraph is the strongest piece of bookkeeping in the document: verified accurate against `INDEX.md:70`, the chain mechanics did ship at `contract-v1.31`, and what was deferred was indeed a consumer rather than the primitive.

---

## Summary of severities

| # | Dimension | Severity |
|---|---|---|
| 5.1 | Floor: AI-reviewer clause contradicts "floor untouched" | **MISMATCH — blocking** |
| 5.2 | Floor: repository predicate under-covers the path predicate | **MISMATCH — blocking** |
| 2.1 | "Act as itself" does not reconcile with "Authority never transfers" | **MISMATCH — blocking** |
| 3.2 | "Model on consent-instrument" ⊥ "express as an openxwallet grant" | **MISMATCH** |
| 5.6 | No `origin:` block — strict validation must fail | **GAP — fix before ratification** |
| 5.3 | Wrong `repo-boundary-governance` requirement cited for a new repo | MISMATCH |
| 4.1 | Q4 "external" test does not exclude a fork | GAP |
| 1.1 | Five vs. fourteen activation-gate entries | MISMATCH |
| 2.2, 2.3, 2.4, 2.5 | Liaison doctrine: status, vocabulary, delta, grant prerequisites | GAP / MISMATCH |
| 4.2, 4.3, 4.4 | Bullets 1, 5, 6, 8 have no verifiable artifact | GAP |
| 5.4, 5.5, 5.7 | Stop conditions; `shared-contract-ownership` delta; missing packet files | GAP |
| 1.2, 1.3, 3.1, 5.8 | Citation precision and sequencing framing | MISMATCH (minor) |
