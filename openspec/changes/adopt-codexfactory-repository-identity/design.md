# Design: adopt-codexfactory-repository-identity

## 0. Convener brief

Ten lines, for the read that decides whether to ratify.

1. Brett ruled on 2026-09-07 that `opensoft/codexFactory` moves to the
   `codeXfactory` organization and stays private, and that `openxFactory`
   becomes public. **Nothing has moved yet.**
2. openxFactory names the repository **281 times across 150 files** (measured at
   `origin/main` `64aad02e`, 2026-09-07) — nine times what the MedxSoft exemplar
   faced.
3. **123 across 60 rename. 78 across 54 are frozen. 80 across 36 belong to other
   lanes and to ideation and are not swept.** The arithmetic closes exactly.
4. **44 of the frozen occurrences cannot be respelled at all**: they sit inside
   ed25519-signed blocks whose private key exists nowhere in this repository.
5. **The origin identity is an authorization scope**, not a label: the transfer
   revokes codexFactory's clearing dispatch until the identity records are
   re-issued, on a surface that is permanently human-only.
6. **The bytewise-sorted regression denominator reorders**, and it reorders
   differently depending on whether the MedxSoft change lands first — which is
   the load-bearing reason for `sequenced_after`.
7. Eight renamed files are `contract-v3.4` inventory members, so a bundle cut is
   owed and is sequenced inside this change.
8. This packet **does not author** `contracts/policies/repository-identity.yaml`;
   the exemplar does, and this adds one row to it.
9. OQ-1 (Enterprise membership) and OQ-2 (Apache-2.0) were **ruled the same
   day**; OQ-3 .. OQ-6 remain for the convener.
10. **Nothing here is performed.** The operational ceremony is a runbook and an
    issue; this is the governed half and it carries `Status: draft`.

## 1. Decision provenance

The ruling of 2026-09-07 — *"move codeXfactory to the new org. openXfactory
should be public and codeXfactory private."* — settles the destination and the
two visibilities. It settles nothing else, and this packet claims nothing else
from it.

**The structural difference from the exemplar is the tense.**
`adopt-medxsoft-repository-identity` was authored on 2026-08-27 about a transfer
that had already happened on 2026-08-26; its operational half was done, correctly
and outside OpenSpec, and its governed half was the only half left. Here the
governed half is authored FIRST, while the ordering is still free. That is worth
more than tidiness: three of this packet's findings are constraints on the ORDER
of the ceremony, and every one of them would have been an incident report rather
than a precondition if the transfer had gone first.

Everything below the ruling is proposal. Six open questions are named rather
than answered; two of the six were ruled the same day and are recorded at their
original numbers.

## 2. Why the exemplar's method needs one change: enumeration does not scale

The exemplar listed all thirty of its occurrences by file and line, in the
proposal's `code_surface`, in `tasks.md`, and again in a freeze-verification
task. At thirty that is the right instrument: a reviewer can hold the list in
their head and check it.

At **281 across 150** the same instrument becomes a liability, in three
measurable ways:

- **It is stale before review ends.** The corpus moves daily; 32 of the 150
  files are other lanes' unmerged packets, and 74 of the occurrences live in
  them.
- **It invites checking the list instead of the tree.** A reviewer who verifies
  that the diff matches a hand list has verified the list, not the disposition.
- **The `code_surface` front-matter field would become unreadable** — a
  single scalar of several hundred paths, which is exactly the shape the strict
  front-matter loader has a 65,536-byte ceiling for.

So this change replaces the hand enumeration with **a rule over path classes,
plus a recorded machine sweep whose output is the evidence.** The rule is small
enough to review, the sweep is reproducible, and the arithmetic closes:

| class | hits | files | disposition |
| --- | ---: | ---: | --- |
| `contracts/**` except `signed-execution-chain/` | 30 | 23 | RENAME |
| `tests/**` | 23 | 8 | RENAME |
| `.github/**` | 16 | 4 | RENAME |
| `governance/**` | 6 | 3 | RENAME (human-only surface) |
| `scripts/**` | 5 | 3 | RENAME |
| `docs/**` except `docs/decisions/` | 35 | 18 | RENAME |
| `README.md` | 8 | 1 | RENAME |
| **rename subtotal** | **123** | **60** | |
| `contracts/signed-execution-chain/**` | 44 | 34 | FROZEN — cryptographic |
| `openspec/changes/archive/**` | 15 | 10 | FROZEN — immutable |
| `specs/**` | 18 | 9 | FROZEN — dated verification |
| `docs/decisions/**` | 1 | 1 | FROZEN — dated decision |
| **frozen subtotal** | **78** | **54** | |
| active change packets (not archive) | 74 | 32 | NOT SWEPT — owning lanes |
| `ideation/**` | 6 | 4 | NOT SWEPT — pre-governance |
| **not-swept subtotal** | **80** | **36** | |
| **TOTAL** | **281** | **150** | |

The sweep command that produces these numbers is recorded verbatim in
`tasks.md` § 2 so the count is reproducible by anyone, at any commit, without
this table.

## 3. The freeze boundary, stated as a test — with a second arm

The exemplar's arbitration question stands unchanged and is used here for every
occurrence:

> **Does this string assert what IS, or does it record what WAS READ?**

- A regression denominator entry, a decision-core pin, a negative fixture, an
  installation example, a README enumeration and a document's prose all assert
  what IS. **Rename.**
- An archived packet, a dated decision record, a dated verification table and a
  dated ratification record all record what was read at a stated moment.
  **Leave verbatim.**

**This change adds a second, independent arm**, because one class of occurrence
here is frozen whether or not the first arm would have frozen it:

> **Are these bytes covered by a signature or a digest this repository cannot
> reproduce?**

If yes, the surface is frozen BY CONSTRUCTION. The disposition is not a policy
choice and cannot be overridden by a ruling that the string "asserts what IS",
because the alternative is not a worse record — it is a corpus that fails its own
validator with no available repair.

Two occurrences sit outside both arms and are handled explicitly:

- **`tests/hermes_runtime_contracts/test_domain_regression.py` `PINNED_TABLE`**
  looks like a test constant and is really a **pin of a live fixture**, row for
  row and in document order. It renames AND reorders with the fixture, in the
  same commit, or the suite goes red — the mechanism working, not a cost. The
  same is true of `tests/review_lane_pin/test_floor_snapshot.py`
  `PINNED_REPOSITORY` and `tests/review_lane_pin/test_review_lane_caller.py`
  `PINNED_REPOSITORY` against `contracts/review-lane-pin.yaml`.
- **`tests/clearing/test_origin_signature.py` lines 200-217 and 356** assert
  against the **LIVE register**, by design — the file's own comment says this is
  "what keeps the live path from being untested". Those assertions move with the
  register row in § 5's commit, not with the rest of the test sweep.

## 4. The three consequences nobody would guess

### 4.1 Thirty-four signed examples cannot be respelled, and cannot be re-signed

`contracts/signed-execution-chain/examples/` carries 44 occurrences across 34
files, every one of them at

```yaml
  out_of_pipeline:
    performed_out_of_pipeline: true
    ground_ref: opensoft/codexFactory hermes/domain/review-councils/records/2026-08-28-gate-rules-openxfactory-substantive-classes.md
```

which is nested **inside `signed_ratification`**. Three facts then compose:

1. `chain_identity` is declared as `construction: xfc-jcs-sha256-1`,
   `subject: signed_ratification` — a digest over the canonical bytes of that
   block, and `scripts/validate-signed-execution-chain.py` **recomputes it**
   (check `chain_identity_recomputes`, refusal `orphan_chain_identity`).
2. `ratification_signature` declares `signed_over: signed_ratification` and the
   validator **verifies the ed25519 signature over `canonical.serialize(signed)`**
   (check `ratification_signature_verifies`, refusal
   `ratification_signature_invalid`).
3. The corpus header states, in capitals, that **the fixture key's private half
   exists nowhere in this repository**; only the public half, the digests and
   the signatures are packaged, and the corpus is self-checking precisely
   because the validator recomputes each one.

Changing one character of `ground_ref` therefore changes the JCS serialization,
which changes `chain_identity`, which orphans the inception leaf that commits to
it, and invalidates a signature **that cannot be regenerated**. A rename here
does not produce a stale example; it produces 34 broken ones and no repair path.

The honest reading is also the correct one under arm 1: `ground_ref` names the
out-of-pipeline ground of a ratification act performed at
`2026-08-30T10:00:00Z`. It records what was read. **Frozen twice over, and the
mapping is the only resolver.**

### 4.2 The sorted denominator moves — and how far depends on merge order

`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` lists its
five entries bytewise sorted by repository, and
`tests/hermes_runtime_contracts/test_domain_regression.py:259` asserts exactly
that:

```python
assert repositories == sorted(repositories, key=lambda value: value.encode("utf-8"))
```

Today the order is `opensoft/AdxFactory`, `opensoft/LedgerxFactory`,
`opensoft/MedxFactory`, `opensoft/OpsxFactory`, `opensoft/codexFactory` — the
transferring entry is **LAST**. `c` is `0x63` and `o` is `0x6F`, so
`codeXfactory/codexFactory` sorts **BEFORE every `opensoft/…` row**: the entry
moves from position five to position one, and `PINNED_TABLE` moves with it in the
same commit.

**And the destination depends on the exemplar.** `M` is `0x4D`, so if
`adopt-medxsoft-repository-identity` lands first, `MedxSoft/MedxFactory` takes
position one and `codeXfactory/codexFactory` takes position two:

| landing order | resulting head of `entries` |
| --- | --- |
| this change alone | `codeXfactory/codexFactory`, then the four `opensoft/…` |
| MedxSoft first, then this | `MedxSoft/MedxFactory`, `codeXfactory/codexFactory`, then three |
| this first, then MedxSoft | same final order, but the exemplar's own task 2.1 — written as "move that entry to the head" — becomes false and must be re-derived |

**This is the load-bearing reason for `sequenced_after: [adopt-medxsoft-repository-identity]`**,
and it is a stronger reason than the shared policy file. Two independent renames
into one bytewise-sorted list, each with a hand-written "move it to the head"
task, is a merge-order trap. Declaring the order makes the second author's
correct action derivable rather than remembered. The second reason is the
ordinary one: the exemplar creates
`contracts/policies/repository-identity.yaml` and registers it in
`contracts/manifest.yaml`; this change adds a row to it and must not create it a
second time.

The three negative fixtures under `fixtures/regression/` are respelled for
consistency; their ordering is asserted by no test, and the deliberate duplicate
in `duplicate-repository.yaml` is `opensoft/AdxFactory`, so no reorder can
disturb what those fixtures prove.

One further consequence is recorded rather than left to be discovered: release
engineers resolving the denominator pass
`--domain-repo <canonical-repo>=<checkout>`, `test_domain_regression.py:410`
pins that resolver against `opensoft/codexFactory`, and **the key to pass for the
engineering domain becomes `codeXfactory/codexFactory`** from that bundle
forward. It is a migration note, not a deprecation: no shape accepts both
spellings, and a consumer on an older bundle keeps using the older key with the
older bundle, which still verifies at its own tag.

### 4.3 The origin identity is an authorization scope, on a human-only surface

`governance/factory-identity/` holds the estate's FIRST origin identity, and the
repository name is not a label there:

- `grants/grant-origin-codexfactory-0001.yaml` carries
  `audience.holder_ref: opensoft/codexFactory` and
  `scope.objects: [opensoft/codexFactory]`, and its own header says **"THE SCOPE
  IS ONE REPOSITORY … A second originating repository is a NEW wallet, a NEW
  grant and a NEW row — never a widened `objects` list here."**
- `register.yaml:146` carries the backing row's `holder_ref`, and the file's
  header records that **a concurrent active row for the same repository is
  refused by the reader**.
- `wallets/wal-origin-codexfactory-0001.yaml:50` carries `holder_id`.

The consuming path is live: codexFactory's sealed-request producer writes
`origin.repository` into the sealed manifest and
`scripts/validate-clearing-dispatch.py` checks it against this register. **After
the transfer, a sealed request originating from `codeXfactory/codexFactory` finds
no row and the clearing lane refuses it.** The transfer does not degrade the
origin identity gracefully; it revokes it.

Two properties of this surface decide how it is treated:

- **It is PERMANENTLY HUMAN-ONLY.** The register's header states that no council
  verdict and no autonomous or council-cleared approval path may ever land a
  change to this file or the records beside it, and that
  `governance/factory-identity/` is entered BY NAME in codexFactory's
  never-clearable floor. **So the pull request realizing this change cannot be
  cleared autonomously** — it needs a human merge word, and the runbook says so.
- **The key does not move.** A transfer moves the owner segment. The Ed25519
  private half lives in codexFactory's `worker-credentials` environment secret
  `FACTORY_ORIGIN_SIGNING_KEY` and travels with the repository; the public half,
  the `key_id`, the multibase encoding and the fingerprint are unchanged by a
  transfer, and the disjointness rule in `scripts/validate-factory-identity.py`
  is over key material, not over holder strings.

**Decision D-1: the re-issuance is a RESPELL OF THE EXISTING RECORDS, not a new
wallet, a new grant, a new row or a re-mint.** The grant header's "a second
originating repository is a NEW wallet" clause governs a SECOND repository; this
is one repository under a new address, with the same key, the same custody and
the same fingerprint. Minting a second identity would put two origin rows in a
register whose reader refuses concurrent active rows, and would spend a ninety-day
expiry ceiling for nothing. The alternative — a full governed re-issuance per
`docs/governed-reissuance-runbook.md` — is recorded as considered and not taken,
and remains available if the convener reads the holder change as a new identity
rather than a new address for the same one. **The `expires_at` ceiling is NOT
extended by this act**, because renewal is a separate governed question and
riding it on an identity respell would be exactly the "second change riding a
first" the exemplar refused.

**Decision D-2: the re-issuance belongs INSIDE this change, not in a sequenced
sibling.** Three reasons, in order of weight. (a) The artifacts live in
openxFactory's governed tree, so there is no repository boundary to cross. (b)
`tests/clearing/test_origin_signature.py` asserts the live register by design;
splitting the row from the test that pins it produces a red suite in the window
between the two changes, which is the same defect the exemplar's one-commit rule
exists to prevent. (c) The identity claim being re-issued — *"this request
originated in this repository"* — is repository identity itself; it is the
subject of this capability and not an adjacent concern. What is NOT inside is
the operator half: verifying that the environment secret survived the transfer,
and re-attesting custody if it did not.

## 5. Version treatment, derived rather than assumed

**Eight** of the sixty renamed files are members of the declared
`contract-v3.4` digest inventory (283 entries):
`contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml`; its three
negative fixtures `digest-mismatch.yaml`, `duplicate-repository.yaml`,
`missing-exclusion-reason.yaml`; `contracts/hermes-runtime/README.md`;
`docs/contract-versioning-policy.md`; `docs/terminology-and-repo-topology.md`;
and `docs/xfactory-domain-factory-model.md`.

**The root `README.md` is NOT a member, and it takes one sentence to say so**
because a substring search says otherwise: the inventory carries
`contracts/README.md` and `contracts/hermes-runtime/README.md`, and matching
`README.md` as a substring finds both. Membership was re-measured by EXACT path
after the first count said nine. It is also why the proposing commit's OpenSpec
Records entry moves no inventoried blob and owes no cut of its own. **None** of
the eight is in
`scripts/doc_health/release_inventory.py`'s `EDITORIAL` set, which holds exactly
`contracts/CHANGELOG.md`, `contracts/manifest.yaml` and `contracts/README.md`.

Two rules then decide the treatment, and neither leaves discretion:

1. `docs/contract-versioning-policy.md` § "What a red `verify-commit` at HEAD
   means" — a mismatch on a non-editorial member "is a defect: a normative
   contract's bytes moved while the repository went on declaring a bundle that
   describes different bytes". **The remedy is a release cut, never a
   hand-edit**, and the same section forbids adjusting `contract_bundle_version`
   to make a comparison succeed.
2. The change class is **Additive (minor)**: values move, no required field is
   added, no shape is removed, and no role or vocabulary SEMANTICS change.
   `contract_schema_version` stays at 1.

So: the next available additive minor after `contract-v3.4`, **allocated at
realization** through the policy's Bundle Realization Order. No number is
reserved here, because the policy forbids reserving one before merge order is
known — and this packet has a live ordering dependency besides.

**Note what is NOT a member and therefore owes nothing**: the entire
`contracts/signed-execution-chain/examples/` tree is frozen, so no byte of it
moves and it contributes no drift whether or not it is inventoried. The clearing
examples, the omnigent fixtures and the hermes-domain-overlay examples are not
inventory members.

## 6. Why ADDED requirements on `repository-identity` and no new capability

`repository-identity` is the right home and it already exists in proposal form.
The exemplar created it precisely so that naming rules would not be bolted onto
`repo-boundary-governance` — whose requirements are about WHICH repository holds
WHICH authority, so that an identity rule placed there would make every future
transfer read as a boundary change.

The four requirements added here are the ones the exemplar's transfer did not
need and could not have discovered:

- **Cryptographic freeze.** The exemplar's freeze protects records from
  falsification. This one protects a corpus from an unrepairable failure, and it
  binds even where the first arm would have said "rename".
- **Identity as authorization scope.** Nothing in the promoted corpus says what
  happens when a repository's identity is the object narrowing of a live grant.
  `factory-origin-identity` says one registered origin identity per originating
  repository; it does not say that a transfer revokes one.
- **Disposition by rule plus recorded sweep.** The exemplar's per-occurrence
  enumeration is a method, and at this scale the method fails. Writing the
  replacement down is what keeps the next transfer from either hand-listing 500
  occurrences or sweeping blind.
- **Cross-organization reachability.** A `uses:` path is not covered by the
  redirect that covers `git clone`, and a GHCR namespace is not covered at all.
  This is the requirement that turns OQ-1 from a nice-to-have into a
  precondition.

`release-surface-integrity`, `repo-boundary-governance`,
`factory-origin-identity`, `signed-execution-chain` and `workflow-gate-contract`
are CITED, never restated or widened. No check family is added, removed or
renumbered.

## 7. The ceremony's ordering constraints, measured, and who supplied them

The transfer is an operator ceremony. This packet does not govern it, but the
governed half constrains its ORDER, and two other lanes supplied measured
constraints during authoring. They are recorded here with attribution because
they are evidence, not opinion, and because a runbook step whose provenance is
lost is a step nobody can re-derive.

### 7.1 From lane `browser-ui-repair` (session codeXfactory-4)

1. **codexFactory PR #275 (slice 3, in final round) must LAND BEFORE any
   namespace change.** It edits `scripts/browser_ui_repair/ci/resolve_bench_image.py`
   and `tests/browser-ui-repair/test_ci_policy.py` — the exact files the move
   touches.
2. **The bench image is allowlisted BY PREFIX**, verified in the tree:
   `resolve_bench_image.PERMITTED_REPOSITORY_PREFIX = "ghcr.io/opensoft/codexfactory/build/"`,
   and the resolver refuses any other repository; the record
   `scripts/browser_ui_repair/ci/project-bench-image-v1.yaml` carries
   `image_repository` plus a digest. The required order is therefore:
   **(a)** `publish-project-bench.yml` pushes to the NEW namespace first while
   the old package stays live, so both resolve, with the new organization's GHCR
   package PUBLIC (DR-2 forbids `docker login` in the daemon jobs);
   **(b)** ONE reviewed pull request flips `PERMITTED_REPOSITORY_PREFIX`, the
   record's `image_repository` and digest (a re-pin, digest copied from the
   trusted publish run), the immutability tests, and the nine literal references
   in `test_ci_policy.py` **together** — CI is fail-closed in between;
   **(c)** retire the old package after.
3. **The bench digest move is a reviewed RECORD change, not an identity
   recompute.** The renderer identity closure covers renderer source and
   dependencies, not the bench image, so no baseline regeneration is expected;
   the profile's `image_reference` is the Playwright renderer image and is
   untouched.
4. **SonarCloud:** the PR-level quality gate must exist under the new Sonar
   organization BEFORE the first post-move pull request. **Accepted-issue
   dispositions do NOT carry over** — 71 acceptances on #241 plus earlier ones,
   plus this lane's four re-accept/close history. The new project's first `main`
   analysis becomes the baseline, and the runbook says so explicitly so nobody
   chases "reopened" findings that were never carried.
5. `docs/browser-ui-repair-reference-loop-runbook.md` and the LANES/claim URLs
   name `opensoft/codexFactory` — mechanical follow-through.

### 7.2 From lane `hermes-wallet-exercise` (session codeXfactory-2)

1. **The MCP hosting plan forces an amendment, and the amendment REVOKES a LIVE
   APPROVAL.** OpsxFactory `tenants/opensoft-codexfactory-mcp-hosting-plan.yaml`
   names `opensoft/codexFactory`, so the move forces a plan amendment, the plan
   digest moves, and requirement 2 (*a material amendment to an approved plan
   revokes the approval and owes re-approval*) bites.

   **A CORRECTION THIS PACKET GOT WRONG ONCE AND IS RECORDING RATHER THAN
   QUIETLY FIXING.** An earlier draft of this section read the plan FILE's
   `status:` field (line 108, `registered_awaiting_operations_domain_approval`)
   and the OpsxFactory README line ("APPROVAL (task 4.2) NOT GIVEN") and
   concluded that no approval existed to revoke. **That was wrong, and it was
   wrong for an instructive reason.** Task 4.2 IS approved:
   `openspec/changes/host-codexfactory-mcp-contract-service/tasks.md` carries it
   as `- [x] 4.2 … **APPROVED 2026-09-05**`, Brett Heap, `2026-09-05T23:06Z`,
   verbatim *"approve 4.2, merge #221"*, over plan digest
   `4e1a4b763cf911134ac222e0ee7ee52afb2f902b36fabc1dbe4b3e2d7ac9f992`, recorded
   at `https://github.com/opensoft/OpsxFactory/pull/229#issuecomment-5555392080`.
   **The plan file's `status:` stays unedited BY DESIGN** — the tick says so in
   as many words: *"The plan's bytes are NOT edited by this tick — editing them
   would move the approved digest, which requirement 2 treats as a material
   amendment revoking this approval."* The approval lives in the tick and the
   ruling, not in a field inside the approved bytes.

   **This is the same class of mistake as the substring match in § 5**, and it
   is the second one this packet made: reading a state from the artifact that
   the state deliberately cannot live in. It is recorded here because a
   digest-approval regime makes exactly this error attractive, and the next
   author deserves the warning more than this packet deserves a clean page.

   **So the approve → amend → revoke → re-approve cycle is REAL and must be
   walked.** The ordering recommendation is unchanged; its reason is now the
   correct one. Order: **move first** → amend the plan's GITHUB-repository
   references to `codeXfactory/codexFactory` → **Brett re-approves 4.2 over the
   new digest** → 4.4/4.5 acceptance → the 5.1 pin → the edge act for
   `mcp.codexfactory.opensoft.dev` (hostname unchanged, and it depends on 4.5/5.1
   so it is strictly after the move). Doing 4.5/5.1 before the move would force a
   SECOND acceptance on top of the re-approval; moving first spends one
   re-approval and no second acceptance.

   *Observation for the OpsxFactory lane, not a claim by this packet:* the 4.2
   tick names `4e1a4b76…` as the APPROVED digest while also naming
   `8abb0e962a5893dd5d6b124a5083f5f79cf207b889340fa42465addd12c82273` as "the
   digest offered by codexFactory", and the plan file's own `plan_digest` block
   (line 904) carries the latter, after two post-registration amendments
   (`0d2bd86d`, `a83e1d95` — "digest re-registered"). Whether those two digests
   are meant to be the same value is that lane's question and is flagged, not
   answered, here.

   **A second measured correction, which STANDS:** the plan's image path is
   `acropensoftxfactoryqa.azurecr.io/opensoft/codexfactory-mcp` (plan line 189) —
   an **Azure Container Registry** repository path, in which `opensoft/` is an
   ACR path segment and NOT a GitHub organization. It does NOT move with a GitHub
   org transfer and is not covered by OQ-4; only the GHCR bench image is
   organization-bound, and only the plan's GITHUB references move. Renaming the
   ACR path for consistency is a separate, optional act.
   **A second measured correction:** the plan's image path is
   `acropensoftxfactoryqa.azurecr.io/opensoft/codexfactory-mcp` — an **Azure
   Container Registry** repository namespace, not a GitHub organization
   namespace. It does NOT move with a GitHub org transfer and is not covered by
   OQ-4; only the GHCR bench image is organization-bound. Renaming the ACR path
   for consistency is a separate, optional act.
2. **The aggregation lockstep grows.** At transfer it is ONE commit covering:
   `.gitmodules` `url`; the `xFactories/codexFactory` gitlink; `review-lane.yml`'s
   pinned `uses: opensoft/codexFactory/.github/workflows/review-lane-reusable.yml@2527c1de…`;
   the two `MIGRATION_PIN` checkouts (`merge-master-approval.yml:139`,
   `council-convening-lane.yml:296`); and the two pin tests
   (`tests/test_review_lane_workflow.py`, `tests/test_merge_master_workflows.py`,
   six occurrences). **Measured addition:** there are EIGHT further `uses:` paths
   at `@main` in `council-authorization-trigger.yml`,
   `council-convening-lane.yml`, `council-deliberation-worker.yml` (four),
   `council-verdict-emit.yml`, `council-wedge-recovery.yml` and
   `execution-lane.yml`, plus `README.md` and
   `docs/council-lane-app-registration.md` — the latter containing a federated
   credential claim `job_workflow_ref` that names the organization inside the
   claim string. **Do NOT rely on GitHub redirects for reusable-workflow `uses:`
   paths — treat them as a break.**
3. **Origin identity re-issuance.** Sequenced WITH the move, and it belongs
   INSIDE this change — see § 4.3, decisions D-1 and D-2.
4. **Federated credential subjects.** codexFactory #165 task 1.7a (two
   federated-credential subjects, e.g.
   `repo:opensoft/codexFactory:environment:council-deliberation`) is NOT done;
   do it AFTER the move with the new organization string, and the same for every
   FIC/OIDC subject naming `opensoft/codexFactory`.
5. **#271 / feature 042.** `image.repository` is a BUILD INPUT and never a
   producer constant (design D7), so the contract survives; only the input and
   the 040 fixtures' example string change.
6. **Organization-scoped installations to redo on `codeXfactory`:** the
   merge-master GitHub App installation, the environment `worker-credentials`
   and its secrets (verify they transfer), branch protection and rulesets with
   their required checks (`lane-line`, `validate`, `merge-master-approval`), and
   the SonarCloud project binding. **CODEOWNERS is organization-independent.**

## 8. Open questions

**OQ-1 — Cross-organization reachability of a private reusable workflow.**
*RULED 2026-09-07 by Brett Heap (convener): add the `codeXfactory` organization
to the Opensoft GitHub Enterprise.* codexFactory's reusable-workflow access
policy is `organization` (opensoft only), and a cross-organization call to a
PRIVATE repository's reusable workflow requires both organizations in ONE GitHub
Enterprise with access level `enterprise`; `codeXfactory` is on the free plan
today. The two alternatives — vendoring the reusable workflows into the
aggregation, which would change the three-site lockstep invariant, and making
codexFactory public, which the same ruling forbids — are recorded as NOT TAKEN
rather than foreclosed. **The enterprise-owner act is Brett's and it is the FIRST
operator step**, verified by `gh api orgs/codeXfactory --jq .plan.name` reading
`enterprise` BEFORE the transfer.

**OQ-2 — Licence for the repositories going public.** *RULED 2026-09-07 by Brett
Heap (convener): Apache-2.0, for BOTH `openxFactory` and `openXwallet`.* Neither
carries a `LICENSE` file today, and `openXwallet` was already made public earlier
on 2026-09-07 without one. **The LICENSE files are added by a separate lane's
pull request and are NOT part of this change's code surface.** What this packet
records is the ordering consequence: `LICENSE` present at the repository root is
a PRECONDITION of the openxFactory public flip, not a cleanup after it — a
repository published without a licence is published under no grant, and the first
clone is the one that cannot be taken back.

**OQ-3 — What becomes public with openxFactory.** OPEN. The flip publishes
`ideation/` (326 files of brainstorm and staging, the one place in the lifecycle
where contradiction is legal), `governance/` (including the factory-identity
register, its wallets, grants and custody attestations — public keys, digests
and fingerprints only, no secret name, which the register enforces by refusal),
`health/`, `experiments/`, and the agent-configuration trees `.claude/`,
`.codex/`, `.specify/`. **Pre-flight measured:** secret-pattern hits over full
history are all test fixtures and examples (`ghp_EXAMPLE…`, a
`-----BEGIN OPENSSH PRIVATE KEY-----` inside a note string, detector lists).
Recommended: **accept publication.** The alternative — excluding those trees via
a separate public mirror — forks the corpus, gives doc-health two trees to
reconcile, and breaks every intra-repository link from a public document into
`ideation/`; it is by a wide margin the expensive answer. What publication costs
is a knowing acceptance that unfinished thinking is readable, which is what
`Status:` headers exist to signal.

**OQ-4 — GHCR namespace sequencing.** OPEN, and now shaped by two lanes' measured
constraints (§ 7.1.2 and § 7.2.1). GHCR namespaces are per-organization and do
not redirect. The question for the convener is whether the bench-image
dual-publish window opens BEFORE the transfer (both packages live, prefix flip
in one reviewed pull request afterwards) or after it. Recommended: **before** —
the fail-closed window between publish and flip is then measured in minutes
rather than spanning the transfer itself. The MCP contract-service image is on
ACR and is out of scope for this question.

**OQ-5 — Is the `MIGRATION_PIN` re-point ceremony exercised?** OPEN.
`MIGRATION_PIN` is checked out at the aggregation's
`.github/workflows/merge-master-approval.yml` and `council-convening-lane.yml`
and held identical between them by `tests/test_merge_master_workflows.py`; it
advances only at the recorded re-point ceremony (`realize-provenance-gated-autonomous-merge`
task 5.1), gated on the golden characterization suite, the envelope
re-validation and the live lane re-prove. The alternative is to leave the pin on
the `opensoft` URL under GitHub's redirect for a bounded period.
**Recommended: exercised.** A redirect is not an identity — this packet's first
inherited requirement says so in as many words — and the ceremony's whole point
is that the two workflows and the gitlink never disagree about where the decision
core is. A pin resolving only through a redirect is a pin whose correctness
depends on nobody creating `opensoft/codexFactory`, which is exactly the
condition the exemplar refused to rest a contract on. The cost is that the
ceremony's gates must be run inside the transfer window rather than at leisure,
and that cost is stated rather than hidden.

**OQ-6 — Canonical spelling, and the GHCR lowercasing.** OPEN. The organization
is spelled `codeXfactory` (capital X) and the repository stays `codexFactory`, so
the canonical identity is `codeXfactory/codexFactory` — a string whose two halves
differ only in the case of one letter. GitHub resolves organization names
case-insensitively, so nothing breaks; what is at stake is which spelling the
mapping, the register row, the pins and 123 renamed literals carry, since several
are compared as EXACT STRINGS (`PERMITTED_REPOSITORY_PREFIX`,
`PINNED_REPOSITORY`, the origin register's `holder_ref`). **GHCR lowercases
package namespaces**, so the bench image becomes
`ghcr.io/codexfactory/codexfactory/build/…` regardless of the display case — a
divergence between the GitHub identity and the container identity that should be
recorded in the mapping rather than discovered by a fail-closed resolver.
Recommended: adopt `codeXfactory/codexFactory` as canonical, record the GHCR
lowercase form as a NOTE on the mapping row, and state in the mapping that the
owner segment is compared case-sensitively by this estate even though the
provider compares it case-insensitively.

## 9. Non-goals

- **Performing any part of the transfer.** No remote is repointed, no visibility
  is flipped, no pin is moved, no App is installed, no package is pushed and no
  Sonar project is created by this packet.
- **Authoring `contracts/policies/repository-identity.yaml`.** The exemplar
  authors and registers it; this adds a row.
- **Adding the LICENSE files.** Ruled Apache-2.0, authored by a separate lane.
- **Re-minting the factory-origin key**, extending its ninety-day ceiling, or
  reopening the custody-attestation question. The key, its fingerprint and its
  custody are unchanged by an owner-segment move.
- **Sweeping other lanes' in-flight packets or `ideation/`.** Stated as a
  disposition in the proposal, not as an omission.
- **Governing codexFactory's own 532 occurrences**, hermes-install's 181, the
  aggregation's 25 or OpsxFactory's 16. Each is its own repository's act; the
  runbook orders them and the tracking issue carries them.
- **Adding a check family.** No deterministic family is added, removed or
  renumbered. Whether a family should verify that no live surface names a mapped
  former identity is the same later question the exemplar left open at its task
  7.2 — and this change's recorded sweep is a second piece of the input such a
  family would need.
