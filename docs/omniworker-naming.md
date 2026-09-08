# omniWorker — Product And Machine Naming Record

Status: ratified
Ratified by: implement-omniworker-install-repo
Kind: reference
Repository context: openxFactory
Purpose: fix the name of the worker-host product, the repository that will
carry it, and the Cloud PC machine-name template — so that the split of the
host material out of `Omnigent-Install`, the reprovision of the first Cloud
PC, and every consumer re-pin all build on one settled term instead of three
spellings settled separately.
Amended: 2026-09-08 by Brett Heap — one dated amendment, "A1 — the Cloud PC
template requires `%RAND:5%`" (§ Amendments below, with dated file-forward
pointers under each affected heading): Windows 365 requires a random
`%RAND:y%` segment in every provisioning-policy device-name template — measured
`%RAND:2%` rejected, `%RAND:5%` accepted — and does not rename a Cloud PC after
provisioning, so the template ruled below,
`CPC-OXF-%USERNAME:7%`, is unreachable and `CPC-OXF-Omni001` was never an
attainable name; the template in force is `%USERNAME:7%-%RAND:5%` and the first
host rendered `Omni001-XEAON`, ruled ACCEPTED 2026-09-05 ~22:50Z, verbatim
"Accept Omni001-XEAON" (opensoft/openxFactory#591). AUTHORIZED 2026-09-08
~03:23Z by Brett Heap, in-session, verbatim "archive
add-manifests-root-parameter and fix the naming record", recorded on the same
issue. No ratified text is rewritten by it: `Status: ratified` and `Ratified
by:` above are unchanged, and the product name, the repository name and the
machine keys are untouched.

**This record is `Status: ratified` as of 2026-09-05.** The decision below is LOCKED — it is
Brett Heap's, taken in session on 2026-09-05 — and its lifecycle ratification is his word
"ratify 680 and merge 16" on openxFactory PR #680 (head `91866619`), the PR of
[`implement-omniworker-install-repo`](../openspec/changes/implement-omniworker-install-repo/proposal.md),
the change that performs the split; `Ratified by:` names that change and its landing carries
this record. The record was authored `Status: draft` naming a change that had not landed,
the same shape `docs/openxdox-naming.md` used at its own authoring and for the same reason:
the ruling is the authority, the change is the record.

## Decision (LOCKED — Brett Heap, 2026-09-05)

> **Amended 2026-09-08 — the MACHINE-NAME clause of the quoted words only; see
> Amendments § A1.** Brett's words below stay exactly as he spoke them and are
> not edited. The product name `omniWorker`, the repository name
> `OmniWorker-Install` and the machine keys `omniworker` all stand unchanged.
> Only "name the machines CPC-OXF-Omni001" was later superseded — by Brett's
> own ruling of 2026-09-05 ~22:50Z, "Accept Omni001-XEAON", after Windows 365
> proved that name unreachable by any supported means.

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

> **Amended 2026-09-08 — this heading and the template it names are
> SUPERSEDED; see Amendments § A1. Do not configure the template below.**
> Windows 365 rejects a device-name template that carries no random segment —
> `CPC-OXF-%USERNAME:7%` included — and rejected `%RAND:2%` as too short; it
> does not rename a Cloud PC after provisioning either. The template in force
> is `%USERNAME:7%-%RAND:5%`; the
> first host is `Omni001-XEAON`, Entra device
> `cf287ce7-7f73-4da7-adfb-c501bd7dd670`. The text of this section is left as
> ratified and is not edited.

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

> **Amended 2026-09-08 — see Amendments § A1.** Two findings in this section
> stand unchanged: the fifteen-character limit, and `XFACTORY-OMNI001` as a
> sixteen-character name that was never applied to any machine. What does not
> stand is the implication that `CPC-OXF-%USERNAME:7%` replaces the default
> template's random suffix — the template actually in force,
> `%USERNAME:7%-%RAND:5%`, carries a random suffix of its own, because Windows
> 365 requires one.

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

> **Amended 2026-09-08 — this section's premise is SUPERSEDED in full; see
> Amendments § A1.** A random segment is MANDATORY, and the template in force
> carries `%RAND:5%`, so: uniqueness rests on the random suffix, not on the
> one-Cloud-PC-per-Omni-user convention; one account no longer renders one
> name, and a name is not predictable before its Cloud PC provisions; and the
> seven-character collision boundary described below never arises. The fleet
> convention *one numbered Omni user, one Windows 365 license, one Cloud PC*
> still governs the ACCOUNT mapping — it simply no longer carries the name's
> uniqueness.

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

> **Amended 2026-09-08 — the rule stands and is stronger than stated; the
> reprovision it anticipates HAS HAPPENED. See Amendments § A1.** Windows 365
> will not rename a provisioned Cloud PC at all: Intune's `setDeviceName` does
> not exist on Graph v1.0 and returned HTTP 400 on beta when the rename was
> attempted on Brett's word against this company-owned, MDM-enrolled,
> Entra-joined Cloud PC. Reprovisioning is the ONLY way a Cloud PC's name
> changes, and omni001 was reprovisioned 2026-09-05 ~22:24Z.

A Windows 365 provisioning policy's device-name template is read **at
provision time**. Changing it renames nothing. `CPC-Omni0-P5AJB` keeps its
name until the Cloud PC is reprovisioned.

**omni001 is to be reprovisioned** (Brett's ruling, 2026-09-05). It is empty —
no runner was ever registered on it and no pilot ever ran — so the reprovision
costs nothing but the provisioning time, and it is the cheapest moment this
fleet will ever have to correct its naming.

### The reprovision yields a NEW Entra device id, and the fleet must be re-attested

> **Amended 2026-09-08 — PERFORMED, and the OWED act below is DISCHARGED; see
> Amendments § A1.** The reprovision ran 2026-09-05 ~22:24Z: device
> `08829330-2098-461c-a950-0047e163f2b1` is gone from Entra and the key is now
> `cf287ce7-7f73-4da7-adfb-c501bd7dd670` (Intune
> `ff367aaf-3d42-429a-a939-42f1f5d6d327`). The re-attestation this section
> records as OWED has LANDED — opensoft/OpsxFactory#233 → merge commit
> `83a91c58`. This section's central rule is UNCHANGED and is now more
> load-bearing than when it was written: the device id is the canonical key,
> and a name that carries five characters nobody can predict before provision
> time is an alias in a way it was not before.

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

Amendments to this record are appended here, dated, each naming the
ruling and the act that carries it — never by rewriting the text above, on
`docs/openxdox-naming.md`'s own rule: what was true when the name was locked
stays on the page, and only the amended fact moves.

*This section opened with the word `None.` until 2026-09-08. Striking that one
word — a state, not a claim, and one that would contradict the entry directly
beneath it — is the ONLY deletion amendment A1 makes anywhere in this record.
The convention sentence above is otherwise byte-unchanged; everything else A1
does is appended, exactly as the convention requires.*

### A1 — 2026-09-08 · The Cloud PC template requires `%RAND:5%`, and `Omni001-XEAON` is accepted

**Authority for this amendment.** Brett Heap, 2026-09-08 ~03:23Z, in session,
verbatim:

> archive add-manifests-root-parameter and fix the naming record

recorded on opensoft/openxFactory#591. The correction it commissions was named
as OWED, with the content it owes, in
[`implement-omniworker-install-repo`](../openspec/changes/implement-omniworker-install-repo/tasks.md)
§ 8 — the packet that ratified this record; that naming landed as
opensoft/openxFactory#773 → squash `bd263dca` (2026-09-08T00:22Z). This
amendment is that act and nothing wider.

**What was ruled, and why it could not be applied.** This record ruled the
device-name template `CPC-OXF-%USERNAME:7%`, rendering `CPC-OXF-Omni001` at
fifteen characters exactly. Measured against Microsoft Graph on 2026-09-05,
Windows 365 **requires a random `%RAND:y%` segment in every
provisioning-policy device-name template, and rejects a template that carries
none** — failing policy validation with `parameterValidationFailed` regardless
of prefix or `%USERNAME%` width:

| Template tried | Result |
|---|---|
| `CPC-OXF-%USERNAME:7%` — the template this record ruled | rejected |
| `OXF-%USERNAME:7%-%RAND:2%` | rejected |
| `CPC-OXF-Omni001` — the literal name, no parameters | rejected |
| `CPC-%USERNAME:4%-%RAND:5%` | accepted |
| `%USERNAME:7%-%RAND:5%` | accepted |

**What the measurement establishes, and what it does not.** It establishes that
a template with no random segment is refused, that `%RAND:2%` is too short, and
that `%RAND:5%` is accepted. **No template with a random segment LONGER than
five was tried**, so nothing here says `%RAND:6%` or wider would be refused —
the platform rule this record states is a MINIMUM random length, not the
literal token `%RAND:5%`. `implement-omniworker-install-repo` § 8 phrased the
constraint as "the specific token"; that phrasing is narrowed here to what the
measurement supports, and the acts it records are unaffected. Five is simply
what was applied, and `%USERNAME:7%-%RAND:5%` is the template in force.

Nor could the name be reached the other way round, by provisioning first and
renaming after: the rename was attempted on Brett's word and **refused** —
Intune's `setDeviceName` action does not exist against Graph v1.0 and returned
HTTP 400 against the beta endpoint, on a company-owned, MDM-enrolled,
Entra-joined, synced Cloud PC. **`CPC-OXF-Omni001` was therefore not attainable
by any supported means, neither by template nor by rename.** Both measurements
are recorded in `docs/omni-fleet-identity.md` in opensoft/CloudPC-Install, via
opensoft/CloudPC-Install#18 → squash `349d539d` (2026-09-05T23:39Z).

**What was applied, and what rendered.** The template in force on the
provisioning profile governing this fleet is:

```text
%USERNAME:7%-%RAND:5%
```

omni001 was reprovisioned 2026-09-05 ~22:24Z under it and rendered:

```text
Omni001-XEAON            "openXfactory omniWorker 001, rendered"
```

Thirteen characters — seven for `%USERNAME:7%`, one hyphen, five for
`%RAND:5%`. The new Cloud PC is Entra device
`cf287ce7-7f73-4da7-adfb-c501bd7dd670` (registered 22:01:56Z; Intune id
`ff367aaf-3d42-429a-a939-42f1f5d6d327`); the prior Cloud PC `CPC-Omni0-P5AJB`
and its Entra device `08829330-2098-461c-a950-0047e163f2b1` no longer exist.
The Entra account was renamed `Omni-001@opensoft.one` → `Omni001@opensoft.one`
so that `%USERNAME:7%` renders `Omni001` with no hyphen to be truncated into.

**The ruling.** Brett Heap, 2026-09-05 ~22:50Z, in session, recorded on
opensoft/openxFactory#591 (comment of 22:56Z), verbatim:

> Accept Omni001-XEAON

The reprovisioned Cloud PC keeps its template-rendered name. The Entra device
id is the key.

**What that does to this record's claims.** Every row below is a claim made
above; the text above is not edited and each affected section carries a dated
file-forward pointer to this entry.

| Claim as ratified | Standing after this amendment |
|---|---|
| The device-name template is `CPC-OXF-%USERNAME:7%` (§ heading and code block) | **SUPERSEDED.** The template in force is `%USERNAME:7%-%RAND:5%` |
| It renders `CPC-OXF-Omni001` | **SUPERSEDED.** It rendered `Omni001-XEAON` |
| "Fifteen characters exactly" | **NO LONGER HOLDS** as a description of the name: `Omni001-XEAON` is thirteen. The fifteen-character *limit* is unchanged and still binding |
| "The ruled template carries **no `%RAND%` segment**" | **INVERTED.** A random segment is mandatory. `%RAND:2%` was rejected as too short and `%RAND:5%` accepted, so the platform rule is a MINIMUM random length, not the literal token: `%RAND:5%` is what the template in force carries, not the only spelling Windows 365 would take |
| The template "renders **one name per account**" | **NO LONGER HOLDS.** The suffix is random, so a name is neither one-per-account nor predictable before the Cloud PC provisions |
| Uniqueness rests on *one numbered Omni user, one license, one Cloud PC* | **NARROWED.** Uniqueness of the NAME rests on `%RAND:5%`. The convention still governs the account mapping; it no longer carries name uniqueness |
| Two accounts agreeing in seven characters would collide (`omni0010`/`omni0011`) | **DOES NOT ARISE** under a mandatory random suffix |
| A template change applies to new provisions only | **STANDS**, and is stronger: a provisioned Cloud PC cannot be renamed at all, so reprovisioning is the only way a name changes |
| The Entra device id is the canonical key; names are mutable aliases | **UNCHANGED, and now load-bearing.** It is the only stable handle on the machine — recorded again in opensoft/CloudPC-Install#18 |
| The OpsxFactory fleet re-attestation is OWED | **DISCHARGED** — opensoft/OpsxFactory#233 → merge commit `83a91c58` |
| `XFACTORY-OMNI001` was sixteen characters and never applied to any machine | **STANDS.** That finding is what prompted the correction and is untouched by it |

**Casing: the Entra account and the host id are different names.** `Omni001` —
capital O, no hyphen — is the ENTRA ACCOUNT's display name and UPN prefix, and
it is what `%USERNAME:7%` actually renders into the machine name. Lowercase
`omni001` remains the **Omnigent host id**, a role identifier that survives
both rename and reprovision, and the machine keys stay lowercase exactly as
this record's three-casings table already rules. Spell every later Omni account
`Omni002`, `Omni003`, … before its first provision, or the number will not
render legibly. Recorded in opensoft/CloudPC-Install#18.

**What this amendment does NOT touch — read it narrowly.** It reaches ONE fact:
the Windows 365 device-name template and the name it renders. Unaffected, and
not to be read as amended by it:

- **The product name `omniWorker`**, the repository name `OmniWorker-Install`,
  and the machine keys `omniworker` — including `svc-omniworker` and
  `installs/omniworker-install`. The three casings above are exactly as
  ratified.
- **Brett's LOCKED words of 2026-09-05**, which stay verbatim on the page. The
  ruling recorded here supersedes their machine-name clause; it does not edit
  them.
- **"What the name does NOT cover"** in full — `Omnigent-Install` keeps its
  name, and the neutral `contracts/omnigent/` family, the
  `omnigent-domain-overlay` and `omnigent-install-manifest` specifications and
  the five domain `omnigent/` overlays are untouched.
- **"Why a split and not a rename"**, and the open question on the GitHub
  runner label `omnigent`, which this amendment neither answers nor moves.

**Where else this is recorded.**

| Record | Act | What it carries |
|---|---|---|
| `openspec/changes/implement-omniworker-install-repo/tasks.md` § 5 (and § 8) | opensoft/openxFactory#773 → squash `bd263dca` | 5.1 and 5.5 SUPERSEDED BY RULING, 5.2 by a recorded DISPOSITION; § 8 names this correction as owed |
| `openspec/changes/implement-omniworker-install-repo/proposal.md` § Origin item 2 (the machine ruling) | the same commit | a dated file-forward note beneath the ratified item, which is itself left unedited |
| `docs/omni-fleet-identity.md` in opensoft/CloudPC-Install | opensoft/CloudPC-Install#18 → squash `349d539d` | the mandatory `%RAND:5%`, the rejected-template measurements, `Omni001-XEAON`, and the host-id vs Entra-account casing rule |
| The OpsxFactory fleet-registration record | opensoft/OpsxFactory#233 → merge commit `83a91c58` | the fleet re-attested to device `cf287ce7-7f73-4da7-adfb-c501bd7dd670` |
| The ruling itself | opensoft/openxFactory#591, 2026-09-05 ~22:50Z (recorded 22:56Z) | "Accept Omni001-XEAON" |
