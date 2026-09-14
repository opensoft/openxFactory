# Staged: Hermes Stack Topology per Client (company Hermes, domain stacks, and where requests enter)

Status: staged
Kind: architecture
Summary: Settle how many Hermes installations a company actually has and what
each one is for — one single-layer company/business Hermes per company, plus
one three-layer stack per (company x licensed DomainxFactory) — and decide
whether request intake/admission is realized at the existing Tenant Hermes
(cheap, contract-aligned) or waits on standing up a second domain stack.
Carries the verified cardinality constraints, the Omnigent multiplication
rule, and the one fixture that contradicts the per-client-stack reading.
Topics: hermes-topology, company-hermes, domain-stack, per-client-instantiation,
omnigent-instantiation, request-intake, admission-gate, licensing, opsxfactory-install
Repository context: openxFactory (neutral topology + intake contract) +
installs/hermes-install (runtime) + xFactories/OpsxFactory (consumer) +
codexFactory (consumer)
Staging ID: openxFactory:staging:hermes-stack-topology-per-client
Source: 2026-08-08 session — the council-clearance canary exposed that the
ratified "Client Hermes is the source of truth for outcome and client
communication" has no realization; scoping OpsxFactory's installability then
surfaced the cardinality constraints below.

## Verified facts (checked against contracts and the live stack, not recalled)

1. **A stack holds exactly one Tenant(client) + exactly one Domain + one or more
   Subject(customer) layers.** `three-layer-hermes-runtime` rejects a manifest
   declaring more than one Client or Domain layer *before any state is mutated*.
2. **Therefore one stack cannot serve two client companies, and cannot serve two
   domains.** Two companies = two stacks. Two DomainxFactories for one company =
   two stacks. This is the structural basis for "one 3-layer Hermes per
   (company x licensed domain)".
3. **A stack is pinned to one domain factory**: `stack_registration.domain_id`
   plus `domain_stack_pin.repository/commit/digest`. Layer content arrives as
   digest-pinned `overlay_manifest_pin`s read from that repo — so the domain
   definition is SINGULAR (one repo) and its INSTANCES are per-stack.
4. **Omnigent multiplies with the stack, not with the definition.** The neutral
   contract states the split verbatim: "core omnigent + per-domain overlay +
   per-tenant instantiation", and `omnigent-install-manifest` pins the Hermes
   runtime manifest as "the single stack identity, exactly one domain overlay
   (one tenant / one domain / N subject workloads)".
5. **The xFactory Hermes runtime cannot express a single-layer Hermes.** A
   manifest without a Domain layer or without at least one Subject layer fails
   validation. A company/business Hermes is therefore NOT an xFactory stack — it
   is the separate single-layer product (`FarHeap/Hermes-Install`), which the
   aggregation README already marks as deliberately distinct and never to be
   repointed.
6. **The live opensoft QA stack is three-layer, not single-layer**: Tenant
   `opensoft-company-policy`, Domain `codexfactory-software-engineering`,
   Subjects `project-alfa` + `project-bravo`. It already IS "codexFactory
   instantiated for the opensoft tenant".
7. **No licensing model exists in the contracts.** Searching openxFactory finds
   licence references only in ontology source metadata. "Licensed client" is a
   commercial concept with no contract, no record kind, and no gate today.

## The contradiction — RESOLVED 2026-08-08 (Brett): each client gets its own stack

RULED: a client company is a **Tenant**, and each licensed client gets its own
stack. Onboarding a client is therefore a STACK INSTALL, not a layer provision.

The `ledgerx-client-company-hermes` fixture is stale, and LedgerxFactory's own
`stack.yaml` already says so independently: the subject layer "collided with the
canonical meaning of the client role (the firm). It is now `Engagement Hermes`
(client entities, ledgers, tax matters, engagements)" — `display_name:
Engagement Hermes`, role key `customer`. The word *client* was overloaded —
xFactory's client (the firm, the licensed tenant) versus the firm's clients (the
businesses whose books it keeps, which are engagements/subjects). The domain repo
was fixed; **the neutral contract was not**.

### The correction owed (a contract change, not a file edit)

The stale artifact is bound acceptance evidence, not a stray fixture:

| Artifact | Stale content |
|---|---|
| `contracts/hermes-runtime/fixtures/topology/ledgerx-client-company-hermes.yaml` | `display_name: Client Company Hermes`, `customer_subject.kind: client_company` |
| `contracts/hermes-runtime/fixtures/index.yaml` | case `topology-ledgerx-client-company-hermes` (class valid, pass), `EVIDENCE-FIXTURE-TOPOLOGY-LEDGERX-CLIENT-COMPANY-HERMES` |
| `contracts/hermes-runtime/acceptance-map.yaml` | HCS-002 / HCS-006 scenario lists |
| `contracts/hermes-runtime/evidence-register.yaml` | HCS-002-S03 titled "LedgerxFactory maps a client-company instance", `status: bound` |

Correcting it renames a RATIFIED scenario and re-binds its evidence, so it goes
through OpenSpec rather than a direct edit, and reconciles at the next contract
bundle cut (the tree already drifts from v1.31 on CHANGELOG.md and manifest.yaml,
so fixture drift riding a cut is the established pattern). Historical release
manifests are NOT rewritten — they truthfully record what those bundles held.

Sibling fixtures show the intended shape and are already correct: medx =>
`Patient Hermes`, codex => `Project Hermes`. Ledgerx should read
`Engagement Hermes` / `kind: engagement`.

## Installed inventory for opensoft (verified 2026-08-08)

**codexFactory is roughly two-thirds installed for opensoft**, and the missing
third is smaller and more specific than "deploy Omnigent".

| Component | State |
|---|---|
| **Hermes 3-layer stack** | **LIVE** on AKS behind `hermes-opensoft-qa.xforge.us`. Proven the same day: it admitted a convening, ran the governed lifecycle, and resolved a verdict. |
| **Omnigent instantiation** | **DECLARED** — `omnigent-install/config/omnigent-install-manifest.yaml` digest-pins the opensoft Hermes runtime manifest as `stack_identity` and pins `domain_id: codex` -> `opensoft/codexFactory`, `overlay_root: omnigent`. A second-domain manifest (`medx-second-domain.manifest`) shows the multi-domain pattern is already exercised. |
| **Omnigent execution (CPC runners)** | **RUNNING** — two self-hosted runners on CPC-BRETT01, both `online`: `xfactory-artifact-cpc-brett01` (labels `omnigent, artifact-only, rider, doc-analysis, document-cataloger, ideation-readiness, derive-possibles`) and `xfactory-coding-cpc-brett01` (labels `omnigent, artifact-only, rider, coding-patch`). They execute SEVEN worker workflows in xFactory: the four `doc-health-*-worker.yml`, `execution-lane-coding-worker.yml`, `ideation-organizer-worker.yml`, `review-lane-worker.yml`. |
| **xFactory layer** | **PRESENT and correctly NOT duplicated** — contract surface, not a runtime: one openxFactory, pinned by every consumer via `stack.yaml contract_ref`. |

### Correction to an earlier reading in this topic's source session

Omnigent was first reported "declared but dormant" because the probe looked for
an HTTP service endpoint and found none. That was the wrong probe: **this
Omnigent execution layer is runner-based, not a service.** The fleet is up and
doing real work — the doc-health nightly that repeatedly re-enabled its own held
workflow during the canary window was these very runners.

### What is actually missing: ONE worker lane, not a deployment

`merge_readiness_agent` IS defined in the codexFactory overlay (archetype
`assemble_for_admission`, `directed_by: lead-integration`, output
`merge_readiness_packet`, with the constitutional `execute_final_action: false`
/ `access_secrets: false`). But nothing dispatches it:

- **no worker workflow exists for it** — the only file referencing
  `merge_readiness_agent` is `council-convening-lane.yml`, which commissions and
  transports and explicitly never deliberates;
- **no runner carries a matching label** — there is no `council` or
  `merge-readiness` label on either CPC runner;
- **two referenced artifacts do not exist**:
  `omnigent/routing/council-deliberation.yaml` and the `council-lane` auth
  profile (both already flagged as unrealized in the lane registration runbook);
- **no worker is registered in the Hermes layer**, so `claim` finds no ready
  worker — the exact wall the 2026-08-08 canary hit.

Chain: the overlay defines the worker -> nothing dispatches it -> no runner
claims it. That is why the convening sat unclaimed and the deliberation was
hand-relayed by an operator agent. Not a credential gap and not a missing
deployment — a missing worker lane in a fleet that is otherwise up.

### Stale pins — RE-PINNED 2026-08-08 (omnigent-install `878d4a0`)

Both pins had drifted (Hermes runtime manifest 29 commits, codexFactory overlay
404 commits). Re-pinned to current heads, re-rendered with the repo's own
renderer rather than hand-edited, and verified with the fail-closed validator
(2 pins, 4 workloads, digest-verify + render-verify green).

What the drift actually contained — checked, not assumed, and much smaller than
the commit counts implied:

- The **Hermes runtime manifest is byte-identical** at the new commit (digest
  stays `3cba25fb`): 29 commits moved but that file never changed. A pure pin
  refresh with no content delta.
- The **codexFactory overlay manifest changed by exactly one line** — the
  `domain-overlay.yaml` digest — driven by two ADDITIVE `semantic_context`
  declarations on `test_agent` and `branch_review_agent` (contract-v1.23 wiring
  from `adopt-domain-ontology-package`). No worker class, permission, or
  archetype changed.
- `rendered/effective-profiles/coding-patch-worker.yaml` came out
  byte-identical (`f2f70eb26821`); only its provenance sidecar moved.

**CORRECTION — the `merge_readiness_agent` concern is closed.** This topic
previously speculated that the worker class "may not even exist in the version
the runners were provisioned from". It did: `merge_readiness_agent` is present
at the OLD pin (`469322b`) as well as the new one. The missing-worker-lane
diagnosis stands entirely on its own — nothing dispatches the class, no runner
label, no routing policy, no auth profile, no Hermes worker registration — and
does NOT depend on pin staleness.

**CORRECTION — the workload/subject skew is by design, not an oversight.** This
topic previously flagged "nothing found reconciles them". The install manifest
itself documents it verbatim: `dartwing-gatekeeper`, `ideation-dashboard` and
`hermes-readiness` have no matching subject layer in the pinned Hermes runtime
manifest (whose subjects are `project-alfa` / `project-bravo`), and
"Reconciling workload subjects with stack-identity subjects is exactly the skew
shared identity exists to surface." The validator reports it as a conformance
WARNING deliberately. It is a standing, named observation — not a defect, and
not blocking.

## Who EXECUTES, and therefore which session owns the work

The layer model answers *whether* (Hermes: policy, consent, approval), *where*
(xFactory layer: routing) and *how* (DomainxFactory: domain interpretation). The
ratified `deployment-handoff-boundary` answers the fourth question — **who
executes** — and it is decided by one test, not by convenience:

> "A release deployment SHALL be executed by the factory that manages the target
> surface, decided solely by the managed-subject test: does the deployment target
> resolve to a registered subject in the managing factory's service-subject
> model? A registered managed subject SHALL be reached only through a governed
> handoff to the managing factory."

`opensoft-aks-qa-hermes-stack` is a registered subject in **OpsxFactory's**
service-subject model. So deploying to it is OpsxFactory's execution act,
performed on OpsxFactory's own operator surface (cloud-bench) — never from the
producing factory's session.

### The correction this records (source session, 2026-08-08)

The `add-governed-job-approval-request` release was produced, requested and
approved from a codexFactory session, which then reported itself "blocked on
cloud-bench" because it lacked AKS run-command RBAC. That framing was wrong.
The producing session was not blocked — it was **complete and handed off**. A
codexFactory session that COULD reach the cluster directly would be the defect,
not the fix: the missing RBAC is the boundary working.

The producing side's own request record already said so — "the producing
factory's authority ends at the release ... Execution is OpsxFactory's under the
post-transfer operating model" — so the artifact was right and only the
narration drifted. Worth stating plainly here because the same confusion recurs
naturally: the agent that produced a release is the one holding all the context,
and is therefore the one most tempted to deploy it.

### Practical rule for this topic's follow-on work

| Work | Home |
|---|---|
| Neutral contracts (topology, intake/admission) | openxFactory session |
| Runtime implementation | xFactory-Hermes-Install session |
| Producing a release + the `cir-` request | the producing factory's session |
| **Executing any deploy to a managed subject** | **the managing factory's session, on its own operator surface** |
| Producing-side acceptance AFTER execution | back in the producing factory's session |

A corollary for the (a)/(b) fork below: standing up an Opsx stack (b) is itself
an OpsxFactory execution act. And (a) — realizing intake/admission at the Tenant
Hermes — is the mechanism that makes this routing explicit and auditable rather
than a convention agents have to remember.

## The (a)/(b) decision this topic exists to make

**(a) Realize intake + admission at the existing Tenant Hermes.** The promoted
`client-infrastructure-request` capability already says "Client Hermes remains
the source of truth for outcome and client communication; the execution system
becomes the source of truth for privileged execution only after it returns an
accepted work-item reference." Today that is unrealized: the `cir-` request is a
YAML file, its approval is a git commit, and the Client Hermes role was played
by an agent in a chat window. (a) means: an intake route, an admission gate that
kills or admits, a pending-request discovery surface, and a notifier — at the
Tenant layer that already exists. Cheap, contract-aligned, and it unblocks the
"all requests enter Hermes first" goal immediately.

**(b) Additionally stand up an OpsxFactory domain stack.** Per facts 2-4 this is
a second installation: its own control plane, Postgres, ingress, Entra
registrations, federated credentials, principal rows, plus a per-tenant Omnigent
instantiation. OpsxFactory's repo side is largely ready — domain implementation,
4 profiles, 13 tenant records, and a validator that went green 2026-08-08 — but
it has no runtime binding manifest and its broker reports
`production_authority not_realized, service not_deployed`.

**COST RE-ESTIMATE after the inventory above.** (b) was scoped as "deploy the
Omnigent layer"; that is wrong — the layer is already deployed and running for
opensoft. The autonomous-council gap is now four concrete items, each modelled
on lanes that already work: a `council-deliberation-worker.yml` in xFactory
shaped like the existing seven worker workflows; a `council` /
`merge-readiness` label on the artifact runner; the two missing artifacts
(`omnigent/routing/council-deliberation.yaml`, the `council-lane` auth
profile); and a worker registered in the Hermes layer so `claim` succeeds.
Re-pinning the two stale manifest pins is a separate, independent chore.
A SECOND domain (Opsx) remains a genuine second installation — but for
codexFactory the remaining work is a worker lane, not a deployment.

**(a) does not preclude (b), and (b) does not deliver (a).** Routing belongs to
the xFactory layer per the ratified layer model, so Hermes deciding *whether*
and the xFactory layer deciding *where* works with or without an Opsx stack.

## Worker-credential distribution — two-case principle (Brett, 2026-08-11)

The 2026-08-10/11 incident (a CPC worker's model-provider OAuth expired;
three lanes dark for two weeks; re-auth took multiple host-admin round
trips) exposed a missing pattern: worker credentials distributed BY
REFERENCE — a vault-held, long-lived headless token (`claude setup-token`
class, non-rotating; NEVER the refreshable session file, which the CLI
rewrites in place and which goes stale in the vault after the first
ephemeral refresh), fetched per-job via the runner's own GitHub-OIDC
federated identity into an ephemeral config dir. Zero host state, no
service restarts, rotation = one vault write.

BRETT'S RULING ON OWNERSHIP: two cases exist, so the pattern is NEUTRAL.
Usually the vault is operated by OpsxFactory — but a client may license
codexFactory WITHOUT OpsxFactory, and then the client's own IT channel
operates the vault. The fork already exists in the ratified model
(client-infrastructure-liaison operating models: opsxfactory_executed vs
client-managed, "no Opensoft identity performs the privileged change").
Therefore:

- the CONTRACT (vault-reference shape, fetch-identity requirements,
  ephemeral materialization, non-rotating-token class, audit-by-vault-log)
  belongs in openxFactory — likely an ADDED requirement on
  `credential-contracts` — never in OpsxFactory;
- the OPERATOR is a per-install execution binding: OpsxFactory when
  licensed, the client's sysadmin channel when not; the lane code is
  identical either way (vault URI + identity ride as bindings/variables);
- the bootstrap/runbook material must be reachable by a codexFactory-only
  client (the domain repo's install docs pin the neutral contract), not
  buried in OpsxFactory.

This is also another instance of this topic's open hosting question: "who
operates the client's estate" is one fork with many faces — stack hosting,
deploy execution, credential custody.

## Credential follow-through (2026-08-14)

The two-case worker-credential principle is now contract text:
`add-worker-credential-by-reference` (credential-contracts +2 requirements —
distribution-by-reference into ephemeral job scope with the session-file
class named non-conforming; vault operator as a per-install execution
binding). Archives on one lane fetching live; runbook §11 and the lane
fetch step are its realization tasks.

## The (a)/(b) fork — RULED 2026-08-14 (Brett): (a)-first, incrementally

Ratifying codexFactory `add-convening-autoclear-trigger` carried the fork
ruling per its task 1.1: intake/admission realizes INCREMENTALLY at the
existing Tenant-Hermes machinery — increment one being the governance-plane
auto-clear trigger that authorizes the ratified convening class by declaring
its class-invariant facts (the envelope remains the decider; unrecognized
requests stay parked for humans). The neutral `request-intake-and-admission`
capability in openxFactory remains the named successor and inherits that
lane as its first worked example; the successor also owns the still-open
pending-approvals discovery/notification surface. (b) — an OpsxFactory
domain stack — remains available later and is NOT precluded.

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

No conflicts recorded.

## Open questions

- Is the company/business Hermes in openxFactory's scope at all, or does it stay
  FarHeap's single-layer product with a defined seam between them?
- Where do client stacks run — the opensoft tenant, or the client's own
  infrastructure? Nothing models hosting today.
- Should "licensed for domain X" become a modelled record (entitlement) or stay
  commercial/out-of-band?
- Opsx layer naming: the instantiation runbook recommends "Operations Domain
  Hermes / IT Subject Hermes / Managed System Hermes"; OpsxFactory's ratified
  `opsx-hermes-layer-model` names "Domain Hermes / Organization IT Hermes / IT
  Service Subject Hermes". The ratified spec wins; the runbook example is stale.

## Exit path

Target capability: a new neutral `request-intake-and-admission` capability
(Tenant-layer intake, admission gate, discovery, notification) plus an amendment
to the topology contract making the per-client stack-vs-layer rule explicit.
Delta type: additive contract + runtime realization in installs/hermes-install;
OpsxFactory and codexFactory conform as consumers. Proposal should not start
until the fixture contradiction and the (a)/(b) decision are settled.
