# omniWorker — Product And Machine Naming Record

Status: draft
Ratified by: implement-omniworker-install-repo
Kind: reference
Repository context: openxFactory
Purpose: fix the name of the worker-host product, the repository that will
carry it, and the Cloud PC machine-name template — so that the split of the
host material out of `Omnigent-Install`, the reprovision of the first Cloud
PC, and every consumer re-pin all build on one settled term instead of three
spellings settled separately.

**This record is `Status: draft` and it is draft on purpose.** The decision
below is LOCKED — it is Brett Heap's, taken in session on 2026-09-05, and
nothing here is offered for reconsideration. What is not yet true is the
lifecycle ratification: `Ratified by:` names
[`implement-omniworker-install-repo`](../openspec/changes/implement-omniworker-install-repo/proposal.md),
the change that performs the split, and this header flips to
`Status: ratified` when that change lands. Naming a change that has not landed
is the same shape `docs/openxdox-naming.md` used at its own authoring, and for
the same reason: the ruling is the authority, the change is the record.

## Decision (LOCKED — Brett Heap, 2026-09-05)

The **worker-host product** — the Worker Host App, the CloudPC worker pack,
the worker profiles and prompt packs, the host manifests, and the host
runbooks — is named **omniWorker**.

Brett's words, verbatim, in session on 2026-09-05:

> i want to rename the project to omniWorker and name the machines
> CPC-OXF-Omni001 for openXfactory omniWorker 001

and, on the question of what the name covers, his ruled selection:

> The worker-host product only

and, on what that does to the repository:

> so omnigent-install repo would become omniWorker-install -right?

— answered under the ruled scope as a **SPLIT, not a rename**: the host
material leaves `opensoft/Omnigent-Install` for a NEW repository
`OmniWorker-Install`, and `Omnigent-Install` keeps its name and its
orchestrator half.

### The three casings, and which surface each one owns

| Spelling | Surface | Why this case |
|---|---|---|
| `omniWorker` | The product and brand — prose, proposals, docs, this record's title | Brett's own casing, above. It is the name of the thing, not a label |
| `OmniWorker-Install` | The GitHub repository `opensoft/OmniWorker-Install` | This estate capitalizes install repositories: `CloudPC-Install`, `Keycloak-Install`, `OpenXPKI-Install`, `Omnigent-Install`. A repository named `omniWorker-install` would be the only lowercase-initial one, and the aggregation's `.gitmodules` URL basenames are the closed vocabulary OpsxFactory's `models/code-surface-repositories.yaml` checks proposals against — a spelling exception there is a spelling exception in a validator |
| `omniworker` | Machine keys — the local service account `svc-omniworker`, the aggregation submodule path `installs/omniworker-install`, any lowercase-on-the-wire label | Already true and already deployed: `svc-omniworker` is the service-rider host's local account today. Lowercase machine keys are `docs/openxdox-naming.md`'s own established rule — the brand and the label differ by design, and that is not a spelling to reconcile |

The service account **does not move and does not change**: `svc-omniworker`
was already correct before this record existed, which is part of why the name
is the right one — it is the spelling the estate had already reached for.

## Machine names: `CPC-OXF-%USERNAME:7%`

Cloud PC machine names are set by a **Windows 365 provisioning-policy device
name template**. The ruled template is:

```text
CPC-OXF-%USERNAME:7%
```

which renders, for the account `omni001`, as:

```text
CPC-OXF-Omni001          "openXfactory omniWorker 001"
```

Fifteen characters exactly: `CPC-OXF-` is eight, `%USERNAME:7%` supplies
seven.

### The 15-character constraint, and the illegal name it replaces

**A Windows computer name may not exceed 15 characters.** This is the
NetBIOS-era limit that Windows still enforces on the machine account.

`installs/cloudpc-install/docs/omni-fleet-identity.md` has, since it was
written, declared the convention `XFACTORY-OMNI001`. **That name is SIXTEEN
characters and could never have been applied.** It was not applied: no Cloud
PC in this tenant has ever carried it. Windows 365 fell back to its DEFAULT
device-name template —

```text
CPC-%USERNAME:5%-%RAND:5%
```

— which is where the two names the fleet actually carries come from:

| Account | Actual Cloud PC name | Rendered from |
|---|---|---|
| `omni001` | `CPC-Omni0-P5AJB` | `CPC-` + first 5 of the account + `-` + 5 random |
| Brett's workstation seat | `CPC-brett-TUBV0` | the same default template |

So the doc did not describe a name that drifted; it described a name that
never existed. The fix is not to edit the string to fit — it is to state the
template, because the template is what actually names the machine.

### Uniqueness rests on the one-Cloud-PC-per-Omni-user convention

The ruled template carries **no `%RAND%` segment**, which is what buys the
name its readability. The default template spends five of its fifteen
characters on randomness precisely so that two Cloud PCs provisioned for the
same user cannot collide.

`CPC-OXF-%USERNAME:7%` therefore renders **one name per account**, and
uniqueness is a consequence of the already-ratified fleet convention: *one
numbered Omni user, one Windows 365 license, one Cloud PC.* That convention is
load-bearing under this template in a way it was not before. Two Cloud PCs
provisioned to `omni001` would render the same name and the second would fail
to join.

Two accounts whose first seven characters agree would also collide
(`omni0010` and `omni0011` both render `CPC-OXF-Omni001`). The three-digit
Omni numbering keeps the fleet inside seven characters through `omni999`, so
this is a boundary to know rather than a problem to solve.

### Template changes apply to NEW provisions only

A Windows 365 provisioning policy's device-name template is read **at
provision time**. Changing it renames nothing. `CPC-Omni0-P5AJB` keeps its
name until the Cloud PC is reprovisioned.

**omni001 is to be reprovisioned** (Brett's ruling, 2026-09-05). It is empty —
no runner was ever registered on it and no pilot ever ran — so the reprovision
costs nothing but the provisioning time, and it is the cheapest moment this
fleet will ever have to correct its naming.

### The reprovision yields a NEW Entra device id, and the fleet must be re-attested

The Entra **device id is the canonical key**; names are mutable aliases. That
is not a preference here — it is what OpsxFactory's
`workflows/endpoint-management.yaml` `fleet_scope` is built on, and what
CloudPC-Install PR #13 recorded.

Reprovisioning omni001 destroys the Cloud PC and creates another. The Entra
device object `08829330-2098-461c-a950-0047e163f2b1` — today the ONLY endpoint
in OpsxFactory's live fleet targeting scope — **will not survive it.** A new
device id is issued.

Therefore: **the OpsxFactory fleet-registration snapshot must be re-attested
after the reprovision, with the new device id, before live targeting is
correct again.** That is a separate governed act against the registration
record, not an in-place edit, and it is **not** performed by
`implement-omniworker-install-repo`. It is recorded here as OWED so that it
cannot be lost between the ruling and the reprovision.

## What the name does NOT cover

**Omnigent remains the orchestrator's name.** The ruled scope is "the
worker-host product only", and the boundary is worth stating as a list of
things this record leaves alone, because the tempting reading — that a
product rename sweeps a vocabulary — is the wrong one:

- **`opensoft/Omnigent-Install` keeps its name.** It is the orchestrator's
  install repository and it is not renamed, not deprecated, and not emptied.
- **The neutral `contracts/omnigent/` family is untouched** — every schema,
  every `contract_id`, every digest. A contract id is a machine key with
  consumers that pin it.
- **The promoted specifications `omnigent-domain-overlay` and
  `omnigent-install-manifest` are untouched**, including
  `omnigent-install-manifest`'s realization, which stays with the
  orchestrator.
- **The five domain `omnigent/` overlay directories are untouched** —
  codexFactory, MedxFactory, LedgerxFactory, OpsxFactory, AdxFactory each
  carry one, digest-pinned.
- **The five worker archetypes and the Omnigent permission matrix are
  untouched.** They are the orchestrator's vocabulary for what a bounded
  worker may do; the host is what a worker runs ON.

The rule to carry: **Omnigent orchestrates; omniWorker hosts.** Where a name
today says `omnigent` and means "the thing that decides", it stays. Where it
says `omnigent` and means "the machine that executes", it is a candidate — and
a candidate is not a rename until a change moves it.

## Why a split and not a rename

Under the ruled scope, `Omnigent-Install` today holds two products:

- **the orchestrator** — `compose/`, `containers/`, `k8s/`, `hermes_service/`,
  `memory_service/`, `agents/`, `pilot-flows/`, `live-pilot/`, `speckit/`, the
  Omnigent server and Polly install docs, the `omnigent-install-manifest`
  realization; and
- **the host** — `hostapp/`, `workers/`, the CloudPC runbooks, the worker-host
  manifests, the heartbeat publisher.

Renaming the repository would give the ORCHESTRATOR the host's name, which is
the opposite of the ruled scope. Splitting gives each product its own name,
its own release line, and its own boundary — the same act
`split-openxwallet-repo` performed for the wallet and
`split-opendox-two-layer-product` ratified for openDox, under the same
`repo-boundary-governance` capability and its copy-first migration rule.

## Open question — the GitHub runner label `omnigent`

Every self-hosted runner in this fleet registers the label `omnigent`:

```text
GitHub labels:  self-hosted, omnigent, cloudpc, omni001
GitHub labels:  self-hosted, omnigent, artifact-only, doc-analysis, rider, ...
```

Under "Omnigent orchestrates; omniWorker hosts", that label means "the machine
that executes" and is therefore a candidate to become `omniworker`.

**Measured before it was assumed, and the measurement changed the answer.** No
xFactory workflow selects on `omnigent` at all. All ten self-hosted lanes
dispatch by runner GROUP plus a per-host or per-lane label —
`group: xfactory-artifact-workers` or `xfactory-execution-lane-workers`, with
`labels: ${{ inputs.dispatch_label }}` or a literal `host-rider-cpc-brett01` /
`host-coding-cpc-brett01`. `omnigent` is a label the runners REGISTER and
nothing in the aggregation SELECTS. Renaming it is therefore a runner
re-registration plus a doc sweep, not a workflow sweep, and no lane loses its
dispatch path while it happens — materially cheaper than it looks from the
label lists in the runbooks.

**This record does not change it, and does not rule on it.** It is raised in
`implement-omniworker-install-repo`'s design as an open question for Brett.

## Amendments

None. Amendments to this record are appended here, dated, each naming the
ruling and the act that carries it — never by rewriting the text above, on
`docs/openxdox-naming.md`'s own rule: what was true when the name was locked
stays on the page, and only the amended fact moves.
