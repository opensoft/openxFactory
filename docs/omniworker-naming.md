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
Amended: 2026-09-08 by Brett Heap — two dated amendments (§ Amendments below,
with dated file-forward pointers under each affected heading). "A1 — the Cloud
PC template requires a random `%RAND:y%` segment": every Windows 365
provisioning-policy device-name template must carry one — `%RAND:2%` measured
too short, `%RAND:5%` accepted, longer never tried — and a Cloud PC is not
renamed after provisioning, so the template ruled below,
`CPC-OXF-%USERNAME:7%`, is unreachable and `CPC-OXF-Omni001` was never an
attainable name; the template in force is `%USERNAME:7%-%RAND:5%` and the first
host rendered `Omni001-XEAON`, ruled ACCEPTED 2026-09-05 ~22:50Z, verbatim
"Accept Omni001-XEAON" (opensoft/openxFactory#591). AUTHORIZED 2026-09-08
~03:23Z by Brett Heap, in-session, verbatim "archive
add-manifests-root-parameter and fix the naming record", recorded on the same
issue. "A2 — the machine key `omniworker` is also a GitHub runner label;
`omnigent` retained pending retirement": the open question raised below is
ANSWERED by a RULING that `omniworker` IS TO BE registered beside `omnigent` on
every registration surface, with `omnigent` kept registered until a later,
separately worded retirement — a ruling and a declaration, not a completed
rollout; putting the label on the already-running runners is an operator act
still owed. Nothing in the xFactory aggregation selects on either label, so no
lane loses its dispatch path while the two halves are sequenced. AUTHORIZED 2026-09-08 by
Brett Heap, in-session, verbatim "do 794, 795 and 796", recorded on the same
issue and claimed against this act at 14:40Z on opensoft/openxFactory#795;
it carries exit 3 of that issue. No ratified text is rewritten by either
amendment: `Status: ratified` and `Ratified by:` above are unchanged, and the
product name, the repository name and the machine keys are untouched.

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
>
> **The fleet-name table below is HISTORICAL as of 2026-09-05 and must not be
> read as an inventory.** It says "the two names the fleet actually carries",
> which was true when it was written and is not true now: `omni001` was
> reprovisioned that evening and its `CPC-Omni0-P5AJB` — Entra device
> `08829330-2098-461c-a950-0047e163f2b1` — **no longer exists**. The current
> name is **`Omni001-XEAON`**, Entra device
> `cf287ce7-7f73-4da7-adfb-c501bd7dd670`, which is the key; the table is left
> as ratified because it is the measurement that found `XFACTORY-OMNI001` had
> never been applied. Brett's workstation-seat row is untouched by this
> amendment. **Never select a machine from this table — read the name back off
> the Entra device object.**

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
> carries `%RAND:5%`, so: name uniqueness rests on the random suffix, not on
> the one-Cloud-PC-per-Omni-user convention; one account no longer renders one
> name, and a name is not predictable before its Cloud PC provisions; and the
> seven-character collision boundary described below is no longer DETERMINISTIC
> — two independent random suffixes can still coincide, so it is an improbable
> event to confirm at provision time rather than a certainty to design around.
> The fleet convention *one numbered Omni user, one Windows 365 license, one
> Cloud PC* still governs the ACCOUNT mapping — it simply no longer carries the
> name's uniqueness.

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

> **Amended 2026-09-09 — `omnigent` is RETIRED from every repository's
> registration material and documentation; see Amendments § A3.** The
> separately worded retirement A2 (below) left owed has now been given: the
> DECLARED label sets in opensoft/OmniWorker-Install, opensoft/CloudPC-Install
> and opensoft/Omnigent-Install no longer name `omnigent`, and `omniworker` is
> the sole common label going forward. No live runner is re-labelled by this
> amendment — that removal is Brett Heap's own operator act, owed, and A3
> names the exact command.

> **Amended 2026-09-08 — this open question is ANSWERED, and the answer is
> ADDITIVE; see Amendments § A2.** `omniworker` is to be registered as a SECOND
> runner label beside `omnigent`, and `omnigent` is NOT retired by that act —
> it stays registered until a later, separately worded retirement. A runner may
> hold both labels, which is why the two halves can be sequenced instead of
> cut over. **The DECLARED label set carries both spellings from A2 onward; the
> LIVE runners carry the second one only after Brett Heap's operator act, which
> A2 records as owed** — no change in any repository re-labels a running
> runner, and in the interval the difference is exactly one label that nothing
> selects on. The measurement below is re-taken and unchanged in A2: nothing in
> the xFactory aggregation selects on the label.
>
> **The ratified text below is left byte-unchanged** — including the sentence
> "This record does not change it, and does not rule on it", which was true
> when it was ratified and which A2 is the change it anticipated. This pointer
> stands beside that text rather than editing it, exactly as A1's pointer does
> under § "Machine names".

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

### A1 — 2026-09-08 · The Cloud PC template requires a random `%RAND:y%` segment, and `Omni001-XEAON` is accepted

> **Precision note, 2026-09-08 (opensoft/openxFactory#787 → squash
> `7fa12108`; the residue two Codex threads on #787 named and left open as
> scope-declines, closed here by this dated sub-note):** two phrasings below
> over-claim what this amendment's own measurement supports. "MINIMUM random
> length" reads as a tested lower bound; the evidence is only that a
> template with no random segment at all is refused, that `%RAND:2%` was
> rejected as too short, and that `%RAND:5%` was accepted — lengths 3 and 4
> were never tried, so no minimum is established,
> only that a random `%RAND:y%` segment is required and `%RAND:5%` is what
> was observed to work. Likewise "not the only spelling Windows 365 would
> take" positively asserts that some other width is accepted; no width other
> than five was ever tested to be accepted, so nothing below licenses
> picking another one. Read every "MINIMUM" and "not the only spelling"
> below as "observed accepted," not as a tested bound. Per this record's own
> amendment convention, this note does not edit the sentences below — it
> stands beside them.

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

Every row is a template that was actually submitted to policy validation, not a
template anyone proposed to run. In particular `CPC-%USERNAME:4%-%RAND:5%` is a
PROBE — it varies the username width to test whether the refusal turned on that
rather than on the random segment — and is neither the Windows 365 default
(`CPC-%USERNAME:5%-%RAND:5%`, quoted earlier in this record) nor the template
adopted. Only the last row was applied.

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
`cf287ce7-7f73-4da7-adfb-c501bd7dd670` (Entra registration timestamp
22:01:56Z; Intune id `ff367aaf-3d42-429a-a939-42f1f5d6d327`); the prior Cloud
PC `CPC-Omni0-P5AJB` and its Entra device
`08829330-2098-461c-a950-0047e163f2b1` no longer exist.

**The two times above are NOT a reconciled timeline, and neither is a key.**
"~22:24Z" is the reprovision as recorded in
`implement-omniworker-install-repo` tasks.md § 5.2; 22:01:56Z is the Entra
registration timestamp read off the new device object and recorded on
opensoft/openxFactory#591. The registration therefore reads EARLIER than the
reprovision it belongs to. Both figures are reproduced here as their records
state them, and this amendment does not reconcile them — it has no measurement
that would let it, and inventing an order is worse than naming the gap. Nothing
in this record depends on either value: the machine is identified by Entra
device id, which is why that is the key.
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
| Uniqueness rests on *one numbered Omni user, one license, one Cloud PC* | **NARROWED.** Name uniqueness now rests on `%RAND:5%` — probabilistically, not by construction. The convention still governs the account mapping; it no longer carries name uniqueness |
| Two accounts agreeing in seven characters would collide (`omni0010`/`omni0011`) | **NO LONGER DETERMINISTIC.** The random suffix breaks the CERTAIN collision the ruled template created. It does not make collision impossible — two independent `%RAND:5%` draws can coincide — so this is now an improbable event to confirm at provision time, not a boundary to design around |
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

**Confirm the rendered name; do not predict it.** `%RAND:5%` is unknown until
a Cloud PC actually provisions, so no rendered name may be written into this
record, a registration record or a preflight table ahead of that event — and
because two independent draws can coincide, a name is not guaranteed unique by
construction either. Read the actual name back off the Entra device object at
provision time. That is the operating rule `docs/omni-fleet-identity.md` in
opensoft/CloudPC-Install states, and it is the mitigation for the collision
class this amendment narrows rather than eliminates.

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

### A2 — 2026-09-08 · The machine key `omniworker` is also a GitHub runner label, and `omnigent` is retained pending retirement

**Authority for this amendment.** Brett Heap, 2026-09-08, in session, verbatim:

> do 794, 795 and 796

recorded on opensoft/openxFactory#591. The middle number is
opensoft/openxFactory#795 — **OQ-5**, the runner-label question — named as OWED,
with the content it owes, in
[`implement-omniworker-install-repo`](../openspec/changes/archive/2026-09-08-implement-omniworker-install-repo/tasks.md)
§ 8.3, the packet that ratified this record, so that the box would tick on a
recording rather than stay open forever. The lane claimed that issue on this
word at 14:40Z and recorded the claim there.

**The reading is the lane's, and is disclosed.** Brett Heap's words name three
issue numbers; they do not spell an exit. Reading "do 795" as authority to take
**that issue's own RECOMMENDED exit** — and no wider act — is the lane's
reading, disclosed on opensoft/openxFactory#591. Nothing beyond exit 3 is
attributed to him, and in particular no retirement of `omnigent` is.

**What the open question asked, and why this record could not answer it.**
§ "Open question — the GitHub runner label `omnigent`" above records that every
self-hosted runner in the fleet registers `omnigent`; that under *"Omnigent
orchestrates; omniWorker hosts"* the label means "the machine that executes";
and that it was therefore the one live machine key still spelled the old way
after the three casings were fixed. It then says, in terms: **"This record does
not change it, and does not rule on it."** A1 left it alone for the same reason,
and said so. #795 is where it was put to Brett Heap.

**The three exits #795 put, and the one taken.**

| Exit | What it does | Standing |
|---|---|---|
| 1 | change `omnigent` → `omniworker` on the runners | **not taken** |
| 2 | keep `omnigent` | **not taken** |
| 3 | **ADD `omniworker` as a SECOND label, and retire `omnigent` later** | **TAKEN** — and it was the issue's own recommendation |

Exit 3 is cheap for one structural reason, which is why the packet recommended
it: **a GitHub runner may hold both labels at once.** There is therefore no
cutover, no window in which a runner is mislabelled, and no lane to sweep
first. The retirement of `omnigent` becomes a separate, later act that is free
once nothing names the old spelling — and it is **not** performed here.
`omnigent` stays registered.

**The measurement, RE-TAKEN before the act rather than quoted.** #795's central
claim — corrected once, in the direction that made the ruling cheaper — is that
nothing in the aggregation selects on the label. Re-measured 2026-09-08 over
every workflow file in `opensoft/xFactory/.github/workflows/`, each `runs-on`
read rather than inferred from a runbook's label list:

| Measurement | Value |
|---|---|
| workflow files | 23 |
| `runs-on` entries naming `omnigent` | **0** |
| self-hosted jobs (a `runs-on:` block with a runner `group:`) | 12, across 10 files |
| — selecting by `group` + `labels: ${{ inputs.dispatch_label }}` | 8 |
| — selecting by `group` + a literal per-host label (`host-coding-cpc-brett01`, `host-rider-cpc-brett01`) | 2 (`clearing-dispatch.yml`) |
| — selecting by `group` ALONE, with no `labels:` at all | 2 (`council-deliberation-worker.yml`) |
| runner groups in use | `xfactory-artifact-workers` (10 jobs), `xfactory-execution-lane-workers` (2) |
| `dispatch_label` inputs carrying a default that could fall back to a common label | **0** — `required: true`, no default, in every reusable workflow that declares it |

The claim holds: **zero**. The textual `omnigent` occurrences in those
workflows are the `Omnigent-Install` repository name, the `OMNIGENT_WORKER`
repository variable, prose about the orchestrator, and one comment that
*describes* the registered label set. So no aggregation act falls out of this
amendment, and the earlier "selected on by at least seven lanes" reading stays
retracted.

**What this amendment changes.** One fact: the machine key `omniworker` is also
a **GitHub runner label** — RULED to be registered beside `omnigent`, and
declared as such in every label set this estate authors. It is a ruling plus a
declaration; on the runners already running it is not yet true, and the
paragraph after next says so. In the three-casings table above, `omniworker`'s surface already
read "any lowercase-on-the-wire label"; this names the label that surface was
waiting for, and adds no fourth casing.

**Declared is not yet live, and the record says which is which.** The acts below
move DESIRED state: manifests, profiles, fixtures, runbooks and registration
scripts. **A runner's label set lives server-side at GitHub**, not in a file any
of these acts can write — the Worker Host App says so itself, in terms
("labels and the runner group live server-side … `.runner` carries neither"),
which is why it keeps a sidecar of what it configured. So a runner that is
already registered keeps its existing label set until an operator changes it at
GitHub, and between the acts landing and the operator act below a live runner
carries `omnigent` and not `omniworker` — a difference nothing selects on. The
acts that carry the declaration:

| Repository | What moves |
|---|---|
| opensoft/OmniWorker-Install | the committed host manifest's two worker `labels:` lists, six locally authored `workers/profiles/*.yaml` `runner_labels`, the host app's bootstrap-volunteer `manifest_labels`, the published readiness example and heartbeat fixture corpus, the runbooks' label lists, and a new runbook section stating that both labels are to be registered, which surfaces are desired state, and why |
| opensoft/CloudPC-Install | both registration-convention label blocks, the runbook `config.cmd --labels` value, the two rider bootstrap scripts' `$labels`, the two heartbeat publishers' attested `runner_labels`, and the non-shipping ruled rider identity record |
| opensoft/openxFactory | this amendment, and the dated file-forward pointer under the open-question heading |

**What this amendment does NOT touch — read it narrowly.**

- **`omnigent` is not retired, anywhere.** It stays a registered label on every
  runner. Its retirement needs its own separately worded ruling, and until then
  a consumer outside the aggregation — a codexFactory lane, an operator's
  ad-hoc dispatch — is not swept and does not need to be.
- **No workflow changes**, in this repository or in the aggregation. Nothing
  selected on the old label, so nothing gains the new one.
- **"What the name does NOT cover" in full.** `Omnigent-Install` keeps its name;
  the neutral `contracts/omnigent/` family, the `omnigent-domain-overlay` and
  `omnigent-install-manifest` specifications and the five domain `omnigent/`
  overlays are untouched. A runner label is "the machine that executes"; every
  one of those is "the thing that decides".
- **The product name `omniWorker`, the repository name `OmniWorker-Install`,
  and the machine keys** — including `svc-omniworker` and
  `installs/omniworker-install` — are exactly as ratified. So is A1's single
  fact, the Windows 365 device-name template.
- **The Hermes worker capability string `omnigent`** in
  `OmniWorker-Install/scripts/register-worker.sh`, and every `OMNIGENT_*`
  environment variable. Those are not GitHub runner labels; the exit taken
  reaches the label and stops.
- **One label set that IS a runner label and still does not move:**
  `workers/profiles/coding-patch-worker.yaml` and
  `rendered/effective-profiles/coding-patch-worker.yaml` in
  `OmniWorker-Install` are byte-verbatim, digest-pinned projections of
  `omnigent/profiles/coding-patch-worker.yaml` in **opensoft/codexFactory**
  (digest `f2f70eb2…`, source commit `e3507ab4`, `mode: byte_verbatim`; the
  renderer fails closed on a mismatch). Editing them outside codexFactory would
  fork a governed projection, so that one is a **codexFactory** act — an
  overlay change, a re-digest and a re-render — and it is named here rather
  than performed.

**Owed to Brett Heap: putting the label on the live runners.** A runner's label
set lives server-side at GitHub, so **no change in any repository re-labels a
running runner.** It is an operator act, owed, and deliberately not attempted by
the acts above. It is NOT, however, a re-registration:

- **`omniworker` is a CUSTOM label, and a custom label can be added to a live
  runner in place.** `POST /orgs/{org}/actions/runners/{runner_id}/labels` (or
  Settings → Actions → Runners → the runner → Labels) adds one without
  downtime, without a removal token and without touching the runner service.
  It needs organization-admin authority, and the credential shape matters: a
  classic OAuth/PAT needs the `admin:org` scope; a fine-grained token needs the
  organization's **Self-hosted runners** permission at **write** — GitHub's
  fine-grained permissions reference lists this endpoint there, available to
  fine-grained PATs and marked NOT available to GitHub App installation tokens;
  an organization owner acting through the UI needs no token at all. Only
  READ-ONLY labels — `self-hosted`, the OS and the architecture — are beyond the
  endpoint, and `omniworker` is not one of those. *This corrects a claim an earlier revision of this
  amendment made, that a label set is fixed at `config.cmd` time: `config.cmd
  --labels` sets the set at REGISTRATION, and is not the only way to change it
  afterwards. The correction came from review and is recorded rather than
  quietly swapped.*
- **On a rider** (`cpc-brett01`) that in-place addition is the whole act, paired
  with the same addition to the ACL-protected heartbeat data configuration so
  the attestation and the runner agree. The remove-and-re-register sequence the
  CloudPC-Install runbook spells out is the FALLBACK, not the prescribed path —
  and note that `config.cmd --replace` REPLACES the label set, so a label left
  out of that command is a label removed.
- **On the brokered fleet host** (`cpc-omni01` / `Omni001-XEAON`) the in-place
  addition is NOT sufficient, and the reason is structural rather than a
  platform limit: the manifest's labels are ADVISORY, the enrollment lease's
  `binding.labels` decide, and the Worker Host App compares its own sidecar of
  what it configured against that desired set. An addition made only at GitHub
  changes neither the lease nor the sidecar, so the two halves would disagree;
  and once the lease binding gains `omniworker`, the app finds sidecar drift,
  plans a reconfigure, and under an ACTIVE lease refuses it — `blocked`, then
  `enrollment_refused`, naming "revoke the lease" as the operator action,
  because the local token-minting path was deleted by design. So there the
  governed act is the broker-side per-estate enrollment-policy change plus a
  lease revoke-and-re-enroll.

Until the operator act happens, the one difference between what a host attests
and what GitHub holds is the single extra label `omniworker` — and nothing
selects on it, so nothing dispatches differently either way.

**Where else this is recorded.**

| Record | Act | What it carries |
|---|---|---|
| `docs/runbooks/cloudpc-worker-pack.md` § Runner Labels, in opensoft/OmniWorker-Install | opensoft/OmniWorker-Install#8 | the ruling, the re-measurement, the desired-vs-live distinction, the lease-decides caveat and the codexFactory carve-out |
| `docs/omni-fleet-identity.md` § Registration Convention and `docs/doc-analysis-worker-host.md`, in opensoft/CloudPC-Install | opensoft/CloudPC-Install#20 | both label blocks, the `config.cmd --labels` value, and the exact re-registration step owed to the operator |
| The issue that put the question, its three exits and its measurement | opensoft/openxFactory#795 | OQ-5, owed by `implement-omniworker-install-repo` § 8.3 / design § D6 |
| The ruling itself, and this lane's disclosed reading of it | opensoft/openxFactory#591, 2026-09-08 | "do 794, 795 and 796" |

The three acts land as independent pull requests; their squash commits are
gathered on opensoft/openxFactory#795 rather than restated here, because a
merge commit written into this record before it exists would be exactly the
kind of predicted value A1's own closing rule forbids.

### A3 — 2026-09-09 · `omnigent` retired from registration material and documentation

**Authority for this amendment.** Brett Heap, 2026-09-09, in session, verbatim:

> do all of these 8 that you can do. all approved

recorded on opensoft/openxFactory#591. The CLAIM comment posted by lane
openxfactory-3 (~15:45Z) named eight items; this retirement is item 7 of that
list. Unlike A2, this word does not merely authorize taking an issue's own
recommended exit — it directly approves the retirement A2 left owed, in
terms: *"`omnigent` is not retired, anywhere. Its retirement needs its own
separately worded ruling."* This is that separately worded ruling.

**What A2 left owed, and what this amendment discharges.** A2 ADDED
`omniworker` beside `omnigent` and explicitly declined to retire `omnigent`,
naming the retirement as "a separate, later act that is free once nothing
names the old spelling." This amendment is that act: every piece of
REGISTRATION MATERIAL and DOCUMENTATION in opensoft/OmniWorker-Install,
opensoft/CloudPC-Install and opensoft/Omnigent-Install that declared or
instructed registering `omnigent` as a runner label now declares or instructs
`omniworker` alone. Historical narrative describing the A2 decision (why
`omniworker` was added beside `omnigent`, the 2026-09-08 ruling quote, the
2026-09-08 and 2026-09-09 point-in-time measurements of the live runner's
label set) is left byte-unchanged where it records what was true when it was
written, on this record's own rule — only the DECLARED, forward-looking
statements moved.

**The measurement, unchanged from A2.** Nothing in the xFactory aggregation
ever selected on `omnigent`; that was true at A2 and remains true, so this
retirement changes no workflow anywhere (none was edited) and no lane loses a
dispatch path. The measurement re-taken once more before this amendment,
2026-09-09, against every workflow file across
opensoft/OmniWorker-Install/.github/workflows/, opensoft/CloudPC-Install/.github/workflows/,
opensoft/Omnigent-Install/.github/workflows/, opensoft/xFactory/.github/workflows/
and opensoft/openxFactory/.github/workflows/: **zero** `runs-on` entries,
`dispatch_label` values or required-label probes name `omnigent` anywhere.
`gh search code 'omnigent' --owner opensoft` over the rest of the
organization turns up only the product name, the `Omnigent-Install`
repository, the `contracts/omnigent/` family, `OMNIGENT_*` environment
variables, worker/compose service ids such as `omnigent-coder-worker`, and
prose about the domain — none of it a runner-label selector.

**What this amendment changes.** The DECLARED (not live) label sets:

| Repository | What moved |
|---|---|
| opensoft/OmniWorker-Install | the committed host manifest's two worker `labels:` lists, six locally authored `workers/profiles/*.yaml` `runner_labels`, the host app's bootstrap-volunteer `manifest_labels`, its paired test fixture, the published readiness example and heartbeat fixture corpus, `tests/test_artifact_lane_contract.py`'s common-label-only test, and the runbooks' label lists and prescriptive prose |
| opensoft/CloudPC-Install | the coding-rider heartbeat publisher and both rider bootstrap scripts' `$labels`, the non-shipping ruled rider identity record, and the registration-convention docs |
| opensoft/Omnigent-Install | the codexFactory execution-lane runbook's runner-label references |

**What this amendment does NOT touch — read it narrowly.**

- **No live runner is re-labelled.** A runner's label set lives SERVER-SIDE at
  GitHub. Every act above moves DESIRED state only; a runner already
  registered keeps `omnigent` until an operator REMOVES it there. That removal
  is Brett Heap's own operator act, not performed by any change in this
  amendment or the pull requests it describes. `omnigent` is a CUSTOM label,
  so the removal is an in-place call —
  `gh api -X DELETE /orgs/opensoft/actions/runners/<runner_id>/labels/omnigent`
  (or Settings → Actions → Runners → the runner → Labels) — no downtime, no
  removal token, no runner-service churn. The reverse call,
  `gh api -X POST /orgs/opensoft/actions/runners/<runner_id>/labels -f 'labels[]=omnigent'`,
  restores it if the retirement needs to be undone.
- **No workflow changes**, in any of the five repositories measured above.
  Nothing selected on `omnigent`, so nothing loses a label to select on.
- **`opensoft/OmniWorker-Install`'s `workers/profiles/coding-patch-worker.yaml`
  and `rendered/effective-profiles/coding-patch-worker.yaml` are untouched.**
  They are byte-verbatim digest-pinned projections of
  `omnigent/profiles/coding-patch-worker.yaml` in opensoft/codexFactory (A2's
  own carve-out); editing them here would fork a governed projection, so
  their label set's retirement is a **codexFactory** act, out of scope here
  and not performed.
- **`opensoft/OmniWorker-Install`'s `hostapp/tests/fixtures/worker-enrollment/`
  corpus is untouched**, on the same rule A2 recorded: it is machine-produced
  against the CI fake broker and its own README forbids hand-editing it. It
  still reads `omnigent` alone (it never gained `omniworker` at A2 either),
  and stays that way until the corpus is next regenerated through the module.
- **`opensoft/xFactory`'s one textual `omnigent` mention** — a comment in
  `.github/workflows/dashboard-image-worker.yml` describing the registered
  label set — is unchanged. This lane does not edit workflow files; if that
  comment is to track the retirement it is a separate, reported act.
- **The GitHub runner label `omniworker` is unaffected.** It remains the
  fleet's registered common label, declared everywhere `omnigent` used to be
  declared alongside it.

**Where else this is recorded.**

The three acts land as independent pull requests against
opensoft/OmniWorker-Install, opensoft/CloudPC-Install and
opensoft/Omnigent-Install, branch `chore/retire-omnigent-runner-label` (the
CloudPC-Install branch additionally carries the unrelated `OMNIGENT_ROOT`
deprecating-fallback removal from `packs/service-rider/selftest/check_heartbeat_contract.py`,
branch `chore/retire-omnigent-label-and-omnigent-root-fallback`, cited on
opensoft/CloudPC-Install#19). Their PR numbers and squash commits are not
restated here before they exist, on A1's own closing rule; they are recorded
on opensoft/openxFactory#591 (lane openxfactory-3's CLAIM/report comments)
instead.
