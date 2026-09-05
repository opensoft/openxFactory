---
code_surface: opensoft/OmniWorker-Install (a NEW private repository that does not exist — this change AUTHORS the boundary and the plan; the repository is created by Brett Heap and the tree is populated by copy-first migration under tasks §3), opensoft/Omnigent-Install (paths RETIRED only after every consumer is re-pinned, tasks §6 — nothing is deleted by this packet), xFactory (aggregation `.gitmodules` gains `installs/omniworker-install`; four workflow comments re-point), OpsxFactory (`models/code-surface-repositories.yaml` closed vocabulary gains one entry), CloudPC-Install (`packs/service-rider/selftest/check_heartbeat_contract.py` `OMNIGENT_ROOT` seam), openxFactory (this change's own records, `docs/omniworker-naming.md`, and the seven contract/spec files that name `Omnigent-Install` paths). **In openxFactory itself this packet touches ONLY documents and records** — one new `docs/` record, this change directory, and one README line.
target_release: repository-bootstrap — the `implement-keycloak-install-repo` / `implement-openxpki-install-repo` precedent for a repository-creation act. **No contract bundle is cut by this change and no contract schema moves**: the neutral `contracts/omnigent/` family, `omnigent-domain-overlay` and `omnigent-install-manifest` are untouched by Brett's ruling. Realization lands on `opensoft/OmniWorker-Install`'s own `main` plus one PR per consumer repository, and under `release-realization` this change archives ONLY on merged plus green realization evidence across those repositories — never on landing.
---

# Proposal: implement-omniworker-install-repo

Status: draft
Proposed: 2026-09-05 — Brett Heap's in-session rulings of ~14:15Z, quoted
verbatim under "Origin" below. Not the exit of a staged topic; the origin
declaration is `ad_hoc` and says why.
Lane: `openXfactory-3` (formerly `openxfactory-f2`).

## Origin — Brett Heap's rulings of 2026-09-05

**These are constraints on this proposal, not questions in it.**

1. **Scope of the name `omniWorker`** — ruled selection, verbatim:

   > The worker-host product only

   with the earlier framing, verbatim:

   > i want to rename the project to omniWorker and name the machines
   > CPC-OXF-Omni001 for openXfactory omniWorker 001

   and, on the repository:

   > so omnigent-install repo would become omniWorker-install -right?

   Answered under the ruled scope as a **SPLIT, not a rename**: the host
   material leaves `opensoft/Omnigent-Install` for a NEW repository
   `OmniWorker-Install`, under the ratified `repo-boundary-governance`
   capability. **Omnigent remains the orchestrator's name.** The neutral
   `contracts/omnigent/` vocabulary, the `omnigent-domain-overlay` and
   `omnigent-install-manifest` specifications, and the five domain
   `omnigent/` overlay directories are UNTOUCHED.

2. **Machines** — Cloud PC names become `CPC-OXF-Omni001` ("openXfactory
   omniWorker 001") via the Windows 365 provisioning-policy device-name
   template `CPC-OXF-%USERNAME:7%`, fifteen characters exactly. **omni001 is
   to be reprovisioned now** — it is empty, no runner was ever registered and
   no pilot ever ran — which yields a NEW Entra device id and therefore
   requires the OpsxFactory fleet-registration snapshot to be re-attested
   afterwards. **That re-attestation is NOT this change** and is recorded as
   owed.

Everything below that is not inside a quote is this packet's proposal or its
declared open question, and the two are labelled.

## Why

**The repository holds two products and can only be named after one of
them.** Measured on `Omnigent-Install` at `9e4fe4e9` (2026-09-05), the tree
carries an ORCHESTRATOR — `compose/`, `containers/`, `k8s/`,
`hermes_service/`, `memory_service/`, `intent_inbox/`, `dox_auth/`,
`dispatch_token_minter/`, `manager_review/`, `agents/`, `pilot-flows/`,
`live-pilot/`, `speckit/`, the Omnigent server and Polly install docs, and
the `omnigent-install-manifest` realization — and a HOST: `hostapp/` (a
PowerShell module, six deploy scripts and two test harnesses), `workers/`
(the CloudPC worker pack, fourteen profiles, four prompt sets, the artifact
heartbeat schema and its nine fixtures), the CloudPC runbooks, the
worker-host manifests, and the heartbeat publisher. They ship on different
cadences to different operators and they fail independently. One repository
name cannot be true of both, which is exactly the condition
`repo-boundary-governance` exists to resolve.

**Renaming would name the orchestrator after the host.** The ruled scope is
"the worker-host product only". `Omnigent-Install` → `OmniWorker-Install` as
a rename would hand the whole orchestrator half a name that describes the
half it is not. The split is what the ruling actually asks for, and it is the
act `split-openxwallet-repo` (2026-08-26) and `split-opendox-two-layer-product`
(ratified 2026-09-05) already performed twice in this estate under this same
capability.

**The name was already half-adopted, which is the tell.** The service account
on the service-rider host is `svc-omniworker` today. Nobody chose that under a
naming record; the estate reached for the word because it is the right one for
the thing. A record that ratifies a spelling the deployment already uses costs
nothing and prevents the second spelling.

**And there is a genuinely broken fact underneath, found while measuring
this.** `CloudPC-Install/docs/omni-fleet-identity.md` declares the Cloud PC
naming convention `XFACTORY-OMNI001`. That is SIXTEEN characters against a
fifteen-character Windows limit — **a name that could never have been
applied, and never was.** Windows 365 silently fell back to its default
template `CPC-%USERNAME:5%-%RAND:5%`, which is where the fleet's two actual
names come from: `CPC-Omni0-P5AJB` and `CPC-brett-TUBV0`. The governed doc has
been describing a machine that does not exist. Brett's template ruling fixes
the convention; the doc fix ships as a sibling PR against CloudPC-Install
because that is where the doc lives.

**The cheap moment is now, and it closes.** omni001 is empty. No runner, no
pilot, no state. Reprovisioning it under the new template costs provisioning
time and nothing else — and the moment it carries a registered runner, the
same act costs a fleet re-attestation, a runner re-registration, and a lane
outage.

## What Changes

- **Author the boundary.** ONE `repo-boundary-governance` requirement —
  *"OmniWorker install repository boundary"* — in the family style its four
  siblings already use ("Install repository scope", "Copy-first migration",
  "Install repo scope links", "Neutral installer repository integration"). It
  fixes what `OmniWorker-Install` owns, what it MUST NOT contain, that
  `Omnigent-Install` remains the orchestrator repository, and that aggregation
  admission is a separate reviewed act.

- **Author the naming record.** `docs/omniworker-naming.md` on the
  `docs/openxdox-naming.md` precedent: the LOCKED decision with Brett's
  verbatim words, the three casings (`omniWorker` brand /
  `OmniWorker-Install` repository / `omniworker` machine keys), the
  machine-name template and the fifteen-character constraint, what the name
  does NOT cover, and an Amendments section. `Status: draft` until this
  change lands.

- **Plan the split directory by directory**, with each assignment marked as
  RULED by Brett, JUDGED from content by this packet, or OPEN. Design § D2
  carries the table; § D6 carries the ten open questions. **This packet
  guesses nothing** — an item whose owner is not obvious from its content is
  an open question, not a quiet assignment.

- **Plan the pin choreography.** Create → copy → re-pin every consumer, each
  as its own PR → retire the source paths LAST. Design § D3. Copy-first is
  not a preference: the ratified "Copy-first migration" requirement already
  says the source copy is deleted only after the replacement and its
  validation path exist.

- **State the rule for the in-flight change**, and do not decide it.
  `Omnigent-Install`'s `add-worker-enrollment-broker-integration` (PR #40) is
  an ACTIVE change against `hostapp/` — the exact material that moves. Design
  § D5 states the two lawful sequences and their costs and puts the choice to
  Brett.

- **Record what is owed and not done here**: the OpsxFactory fleet
  re-attestation after omni001's reprovision (new Entra device id), and the
  runner-label question.

**Nothing is created, moved, deleted, or re-pinned by this packet.** No
repository exists at the end of it. In `openxFactory` it touches one new
`docs/` record, this change directory, and one README line.

## Capabilities

### Modified Capabilities

- `repo-boundary-governance`: exactly ONE delta, an `ADDED` requirement
  *"OmniWorker install repository boundary"*. **No existing requirement is
  MODIFIED** — in particular the "Install repository scope" enumeration is
  left alone, on `implement-keycloak-install-repo`'s own reasoning: the
  enumeration is an index, its refresh is already booked elsewhere, and two
  changes that share one requirement collide at archive time. Adding a
  sibling requirement instead of widening a shared one is this capability's
  established collision-avoidance.

No new capability. No contract family. No schema. No contract bundle.

## Impact

- **Relies on ratified work**: `repo-boundary-governance` (the four sibling
  requirements this delta joins, and the copy-first rule the migration
  obeys — [promoted spec](../../specs/repo-boundary-governance/spec.md)),
  `release-realization` (the `code_surface` / `target_release` declaration
  above and the merged-plus-green archive gate), `document-lifecycle` (the
  origin declaration, the `Status:` headers, the naming record's shape).

- **Precedents followed, not invented**:
  [`implement-keycloak-install-repo`](../implement-keycloak-install-repo/proposal.md)
  and [`implement-openxpki-install-repo`](../implement-openxpki-install-repo/proposal.md)
  for the repository-creation act and its `target_release: repository-bootstrap`;
  `split-openxwallet-repo` (archived 2026-08-28) and
  [`split-opendox-two-layer-product`](../split-opendox-two-layer-product/proposal.md)
  (ratified 2026-09-05) for a two-product split out of one repository;
  [`docs/openxdox-naming.md`](../../../docs/openxdox-naming.md) for the naming
  record's shape.

- **Consumers that must move, each its own reviewed PR** (design § D3
  sequences them): the xFactory aggregation `.gitmodules`
  (`installs/omnigent-install` gains a SIBLING `installs/omniworker-install`;
  it is not renamed until retirement), four xFactory workflow comments naming
  `installs/omnigent-install/workers/profiles/*.yaml`, OpsxFactory's
  `models/code-surface-repositories.yaml` closed vocabulary, CloudPC-Install's
  `OMNIGENT_ROOT` seam in `packs/service-rider/selftest/check_heartbeat_contract.py`
  (which reaches for `workers/schemas/artifact-worker-heartbeat.schema.json`
  and `scripts/publish_artifact_worker_heartbeat.py` — both of which move),
  the openxFactory files naming `Omnigent-Install` paths, and the NotebookLM
  ideation book.

- **A consumer that does NOT move, contrary to first appearance** —
  `xFactory/.github/workflows/intent-apply.yml` reads
  `repos/<owner>/Omnigent-Install/contents/config/intent-inbox-allowlist.json`
  over the API. `config/` is ORCHESTRATOR material and stays. Measured, not
  assumed: no xFactory workflow checks out the submodule at all, and
  `dashboard-image-worker.yml`'s Omnigent-Install references are to the
  dashboard image pin PR, also orchestrator. Design § D4 records the
  measurement.

- **Aggregation admission — NOT this change.** Pinning
  `installs/omniworker-install` records path, remote, visibility, exact
  validated commit, checkout, compatibility, update, and rollback. The ADDED
  requirement's own scenario says this change MUST NOT be accepted as that
  record — the same separate-reviewed-act discipline `Keycloak-Install` and
  `OpenXPKI-Install` were held to.

- **The fleet re-attestation — NOT this change.** Reprovisioning omni001
  destroys Entra device `08829330-2098-461c-a950-0047e163f2b1`, today the
  only endpoint in OpsxFactory's `fleet_scope` live targeting. The
  registration record must be re-attested with the new device id in its own
  governed act, and OpsxFactory's own rule is explicit that a bound value
  changes by a new OpenSpec change and never by an in-place edit.

- **What is deliberately NOT touched**: `contracts/omnigent/` (every schema,
  every `contract_id`, every digest), `openspec/specs/omnigent-domain-overlay/`,
  `openspec/specs/omnigent-install-manifest/` and its realization, the five
  domain `omnigent/` overlay directories, the five worker archetypes and the
  Omnigent permission matrix, and the GitHub runner label `omnigent` (design
  § D6 OQ-5 puts that one to Brett rather than assuming it).

## Ratification

**NOT RATIFIED.** `Status: draft`. Brett Heap's rulings of 2026-09-05 are the
authority for the NAME, the SCOPE, the TEMPLATE and the REPROVISION — all
four are quoted above and carried as locked constraints — but he has not
ratified this packet, and this packet asks for more than those four things:
a boundary requirement, a directory-by-directory split, a consumer
choreography, and answers to ten open questions.

Ratification, when it comes, would authorize exactly this: **the
`repo-boundary-governance` boundary for ONE new repository
`opensoft/OmniWorker-Install`, the naming record, and the copy-first migration
plan.** It would authorize **no repository creation** (that is Brett's own
act, tasks §2), **no deletion from `Omnigent-Install`** (tasks §6, and only
after every consumer is re-pinned), **no aggregation admission**, **no fleet
re-attestation**, and **no runner-label change**.

Rule 6 (landing window) applies at merge: this packet adds an
`openspec/changes/` directory. Rule 7: the README "OpenSpec Records" block is
substrate row 3, claimed for this change on `opensoft/openxFactory` issue #630.
