# §7 Authoring Inputs — grounded recommendations memo, and the rulings it carried

Status: draft
Proposed by: qualify-avatar-live-voice
Kind: decision memo
Summary: The per-input research memo behind `qualify-avatar-live-voice` tasks.md
§7.1-§7.6 — the concrete vault for the internal-live broker server key, the
numeric spend ceilings, the server-key rotation cadence and triggers, the usage
meter's alerting channel and page target, the minimum sample count per gated
latency cell, and the canary exit criteria. Each section carries the task's own
constraint text verbatim, a RECOMMENDATION grounded in artifacts that exist,
honest alternatives, and the evidence a later verifier would need so the value
cannot become unfalsifiable. Brett ruled all six on 2026-08-27, adopting every
recommendation as written; this memo is the grounding those rulings cite.
Topics: avatar-client, live-voice, credential-custody, spend-cap, rotation-policy, alerting, latency-slo, sample-size, canary-exit, gpt-realtime-2.1, AVC-09, AVC-10
Repository context: openxFactory — supporting material for the active `qualify-avatar-live-voice` change. The memo mutates no contract, schema, acceptance map or interface lock; the artifacts that carry its ruled values are named in "Where the rulings landed" below.
Source: this session's per-input research over a read-only clone of `opensoft/openxFactory`, a survey of the `opensoft/xFactory` aggregation tree (hermes-install, omnigent-install, codexFactory, OpsxFactory), the F0 brokered-call feasibility evidence in `openspec/changes/archive/2026-08-09-qualify-avatar-brokered-call-feasibility/`, the ratified `credential-contracts` capability, and the provider's published Realtime rate card.

## How to read the paths in this memo

Every path below is repo-relative to the openxFactory root unless it is marked
`[aggregation]`, in which case it is relative to the root of the `opensoft/xFactory`
aggregation checkout, or it is given as a URL.

**Sanitization note.** This committed copy is the artifact of record. The memo was
drafted as a working file and named its clone locations and the aggregation
checkout by their absolute paths on the authoring machine; those are replaced
here with the repository identities they stood for, because the constitution
forbids committed host-absolute paths and a machine-local path is not evidence a
later reader can follow anyway. No claim, citation, line reference or
recommendation was changed by that substitution.

## Provenance of the rulings

**RULED 2026-08-27 by Brett Heap**, in session, on all six inputs — every
recommendation below adopted as written, with two clarifications recorded at the
time of ruling:

1. **§7.1 splits across two repositories by canon.** `credential-contracts`
   forbids a contract artifact hard-coding a vault operator, a vault product or
   a secret value, so the openxFactory side stays vault-agnostic — a credential
   REFERENCE plus an owner plus a rotation policy — and the concrete Azure Key
   Vault reference lands in the consuming install's `credentials/` tree as a
   separate, install-owned act.
2. **§7.4's Azure Monitor alternative is pilot-hardening work, named now and
   not built now.** The ruled channels are the provider project's own native
   budget alerts plus `gh issue create` on the doc-health pattern.

Nothing in the body below was edited when the rulings landed: it stands as the
decision aid it was, so a later reader can see what was in front of the ruler.
Where the body says "recommendation, not a ruling", read it as the state of the
document *before* 2026-08-27.

## Amended 2026-08-28 — two values were re-ruled the day after they landed

**Both summary tables below, and the six sections after them, are left as they were
written on 2026-08-27.** Two of the values they record have since been re-ruled by Brett,
in session on 2026-08-28, and the dated amendment notes at the head of §7.2 and §7.6
carry the reasoning:

| Section | Ruled 2026-08-27 | RE-RULED 2026-08-28 |
| --- | --- | --- |
| **7.2** | $750/month provider-project cap (hard), alerts at 50% ($375) / 80% ($600) | **$100/month**, alerts at **50% ($50)** / **80% ($80)** |
| **7.2** | $150/tenant/month metered budget | **$40/tenant/month** |
| **7.6** | 200 completed canary sessions, ≥50 from COHORT-02 | **100 sessions**, **≥25** from COHORT-02 |

Everything else in §7 is UNCHANGED — the per-session ceilings (15 min / 300 units /
$3.00), the 14-day soak on ≥10 distinct days, the ≤2% / ≤5% abnormal rates, and both
additional exit criteria. Read every figure below as the 2026-08-27 record; the live
values are in `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml` and
`contracts/avatar-client/usage-metering-and-alerting.yaml`.

## Where the rulings landed

| Input | Ruled value | Artifact carrying it |
| --- | --- | --- |
| 7.1 | AKV `kv-opensoft-xfactory-qa` via the broker's AKS workload identity (CSI) — install side; a vault-agnostic reference here | `contracts/avatar-client/broker-server-key-binding.template.yaml`; the concrete binding is the named install-side act in tasks.md 6.1.1 |
| 7.2 | 15 min + $3.00 per session (hard, broker); $150/tenant/month (metered only); $750/month project cap (hard) with 50%/80% alerts | `openspec/changes/qualify-avatar-live-voice/tasks.md` §7.2; the trip points in `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml` ROLLBACK-B/C |
| 7.3 | `max_key_age_days: 90` plus three added triggers, inheriting the global `require_rotation_on` list | `contracts/avatar-client/broker-server-key-rotation-policy.yaml` |
| 7.4 | Provider-native budget alerts at 50%/80% + `gh issue create` on the doc-health pattern; page target = the §7.7 kill-switch holder | `openspec/changes/qualify-avatar-live-voice/tasks.md` §7.4, cited from 6.1.4 |
| 7.5 | n >= 100 per gated cell, declared before measuring, spread over >=3 runs on >=2 days | `contracts/avatar-client/latency-sample-minimum.yaml` — a SIBLING of the acceptance map, not a block inside it: the map is a published digest-pinned bundle member and an authoring input does not earn a contract-release cut |
| 7.6 | 14-day soak on >=10 distinct days; >=200 sessions; <=2% overall / <=5% trailing-50 abnormal; >=1 rehearsed ROLLBACK-B trip; zero open ROLLBACK-A | `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml` `canary_exit_criteria` |

---

## The six recommendations at a glance

| # | Input | RECOMMENDATION | New infra? |
| --- | --- | --- | --- |
| **7.1** | Vault for the internal-live server key | **Azure Key Vault `kv-opensoft-xfactory-qa`**, fetched by the broker's own AKS workload identity via CSI; concrete values in the install's `credentials/` binding, never in `contracts/` | **No** — this vault already custodies a model-provider token fetched by reference |
| **7.2** | Numeric ceilings | **15 min** + **$3.00** per session (hard, broker); **$150/tenant/month** (metered only); **$750/month** provider-project cap (hard), alerts at 50%/80% | No |
| **7.3** | Rotation cadence + trigger | **`max_key_age_days: 90`** in an `xfactory_credential_rotation_policy` override + 3 added triggers, inheriting the global `require_rotation_on` list | No |
| **7.4** | Alerting channel / thresholds / page target | **Provider-native project budget alerts** (50%/80%) + **`gh issue create`** following the doc-health pattern; page target = a named human who is also the §7.7 kill-switch holder | ⚠️ **See flag** — no alerting plane exists; this recommendation deliberately avoids building one |
| **7.5** | Minimum samples per gated latency cell | **n ≥ 100** per cell, declared before measuring; n < 100 records but does not gate; samples spread over ≥3 runs on ≥2 days | No |
| **7.6** | Canary exit criteria | **14 days** soak (sessions on ≥10 days); **200 sessions** (≥50 from COHORT-02, ≥3/scenario class); **≤2%** abnormal overall / **≤5%** trailing-50; plus ≥1 live ROLLBACK-B trip and zero open ROLLBACK-A | No |

**The one loud flag:** §7.4. The org operates **no alerting infrastructure of any kind**.
The recommendation routes around that rather than through it; the "proper" answer (Azure
Monitor Action Group) is named as pilot-hardening work, not ring work.

---

## Reading this memo

Each of the six sections carries:

1. **The task's own constraint text**, verbatim — §7's text scopes each question and is
   the only thing that is already ratified about it.
2. **RECOMMENDATION** with grounding in artifacts that exist.
3. **Alternatives** with honest tradeoffs.
4. **What a later verifier would need** — the evidence that would prove the value was
   honoured, so the ruling does not become unfalsifiable.

**Loud flags for net-new infrastructure** are marked ⚠️ **NEW CAPABILITY**. There is
exactly one such flag, in §7.4, and it is unavoidable.

A structural note that governs §7.1 and §7.3 and is easy to get wrong: the ratified
`credential-contracts` capability **forbids naming a vault product in a contract
artifact**. See §7.1 "The canon constraint that shapes the answer". The §7 values are
authored into an *install binding* and a *policy record*, not into a neutral contract.

---

# 7.1 — The concrete vault for the internal-live server key

### The task's own constraint text (tasks.md:676–677)

> - [ ] 7.1 The concrete vault for the internal-live server key. F0's mode-600
>       local file plus age escrow is explicitly NOT a deployment source.

Supporting constraint, Fork 1 named gap 1
(`openspec/changes/qualify-avatar-live-voice/supporting-docs/fork-decision-memo.md:266–270`):

> No source names the concrete secret store/vault for the internal-live server key
> (Azure Key Vault / AWS Secrets Manager / Opensoft-hosted vault). The binding shape
> supports any provider, and merge-master used a CI Actions secret, but the internal-live
> pick is unmade; F0's mode-600 local file + age escrow is explicitly "not a deployment
> source."

And task 6.1.1 (`tasks.md:377–381`) requires the binding be authored under
`xfactory_credential_binding_template` — "provider, vault, secret_ref, owner,
rotation_policy — resolved only by the broker."

### The canon constraint that shapes the answer

Two ratified requirements in `openspec/specs/credential-contracts/spec.md` constrain
*where the answer may be written*, and they pull in opposite directions from a naive
reading of §7.1:

- **"The credential vault operator is an execution binding, never contract content"**
  (spec.md:133–135): *"Contract artifacts, lane definitions, and domain repositories
  SHALL NOT hard-code a vault operator, a vault product, or any secret value."*
- **"Worker credentials are distributed by reference into ephemeral job scope"**
  (spec.md:109–111): a model-provider token *"SHALL be distributed by reference: the
  secret is held in a vault as a LONG-LIVED, NON-ROTATING headless token, the lane
  fetches it per job using the runner's own federated workload identity, and the fetched
  value lives only in ephemeral job scope … never written to host state, never persisted
  past the job."*

So §7.1 is **not** asking "which vault product goes into the neutral contract" — that
would be rejected by spec.md:180–182. It is asking **which concrete vault this
particular internal-live install binds to**. The right home for the answer is a
`credential_bindings` instance in the install's `credentials/` tree, and the neutral
side stays an opaque reference plus a fetch identity.

`add-notebook-hosting-credential-custody/design.md:99–107` already worked this exact
split out and says so plainly: concrete values are legitimate in a packaged fixture
because "a packaged fixture is a fixture; the no-hard-coding rule binds contract
artifacts, lane definitions and domain repositories."

### What the org actually operates today

`docs/credential-access-model.md:117–126` lists the approved provider families
(Azure Key Vault, AWS Secrets Manager, GCP Secret Manager, 1Password/Bitwarden
enterprise vaults, customer-owned vaults, Opensoft-hosted vaults, OAuth delegated
consent stores, workload identity providers). All the candidates below are inside
policy; the question is which one this install picks. Three mechanisms are **operated**,
one is **built but not confirmed live**:

| Mechanism | Status | Evidence | Fit for a broker server key |
| --- | --- | --- | --- |
| **Azure Key Vault `kv-opensoft-xfactory-qa`** via AKS CSI + workload identity | **OPERATED** | `[aggregation] installs/hermes-install/deploy/kubernetes/overlays/aks-qa/secretproviderclass.yaml` is a live `SecretProviderClass` — `keyvaultName: "kv-opensoft-xfactory-qa"`, `useVMManagedIdentity: "true"`, `userAssignedIdentityID: "d4c433e7-…"` (the AKS `azureKeyvaultSecretsProvider` addon identity) — materialising `hermes-db-username/password/dsn`; a sibling `secretproviderclass-readiness.yaml` does the same for the readiness tokens. Live probe recorded: `az keyvault show -n kv-opensoft-xfactory-qa` → *"Pass: exact tenant; RBAC authorization enabled"* (`installs/hermes-install/docs/evidence/dispatch-junction-validation-2026-07-30.md:134`), and *"2 SecretProviderClasses. Rollout: successfully rolled out"* (`…/manager-review-gate-deploy-2026-08-13.md:107`). | **Best fit — see the decisive precedent below.** |
| **Azure Key Vault via GitHub OIDC federation** (`worker-credentials` environment) | **OPERATED** | `[aggregation] .github/workflows/review-lane-worker.yml:37–86` | **Decisive.** See below. |
| **SOPS + age**, age identity in 1Password, runtime copy `flux-system/sops-age` | **OPERATED** (QA) | `docs/credential-access-model.md:55–57`; real committed ciphertext under `[aggregation] installs/omnigent-install/clients/opensoft/k8s/azure/*/overlays/qa/secret.sops.yaml` decrypted by the QA cluster's Flux `Kustomization/workloads` (`…/clusters/qa/flux-system/gotk-sync.yaml`, `provider: sops`, `secretRef.name: sops-age`). | Works, but see Alternative 1. |
| **GitHub Actions protected secret** — the merge-master precedent (`MERGE_MASTER_APP_KEY`) | ⚠️ **BUILT, NOT CONFIRMED OPERATING** | `[aggregation] .github/workflows/merge-master-approval.yml:86–103` — the workflow's own preflight prints *"merge-master App not configured … **pre-registration state**; no approval attempted"*, and the survey found no bot-authored approval evidence. | **Poor fit, and weaker precedent than the fork memo implies.** |

### The decisive precedent: this exact credential class already rides Key Vault

`[aggregation] .github/workflows/review-lane-worker.yml:37–86` fetches **a
model-provider token** — `CLAUDE_CODE_OAUTH_TOKEN` — from Key Vault, by reference, using
the runner's own federated workload identity. The step is literally titled *"Fetch the
model-provider token by reference"*; it exchanges the Actions OIDC assertion for a
`scope=https://vault.azure.net/.default` token via
`client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer`, reads the
secret from `WORKER_CREDENTIALS_SECRET_URI`, masks it, and emits
`::notice::token source: vault (by reference; rotation is a vault write)`.

This is the realization of `credential-contracts` spec.md:109–111 for **the same credential
class §7.1 is asking about** — a model-provider token — and it shipped:
`openspec/changes/archive/2026-08-14-add-worker-credential-by-reference/tasks.md:14`
records it DONE with *"narrowest identity yet (KV read on one secret, no Hermes scopes,
no GitHub write), worker-credentials environment created main-only"*. The workflow even
implements the spec's degraded mode by name: with the bindings unset it prints
*"token source: degraded (service env) — worker-credentials bindings unset"*, matching
spec.md:128–131's permitted-and-recorded fallback.

So the recommendation below is not a new pattern for this org. It is the *second*
instance of a pattern that already carries a model-provider token in production.

**Note on the merge-master precedent.** Fork 1's recommendation leans on it as the
"concrete realization today" (fork-decision-memo.md:145–155, 216–219). The design decision
is real and ratified, but the survey found the workflow describes its own uncredentialed
state as "pre-registration" and no evidence of a live bot approval exists in the corpus.
Worth telling Brett plainly: **the credential-by-reference worker lane is the better and
demonstrably live precedent; merge-master is a design precedent, not an operating one.**

### RECOMMENDATION

**Bind the internal-live broker server key to Azure Key Vault `kv-opensoft-xfactory-qa`,
resolved at call time by the broker's own AKS workload identity through CSI, with the
concrete values written into the install's `credentials/` binding — not into
`contracts/`.**

Concretely, the binding instance would read:

```yaml
credential_bindings:
  avatar_broker_openai_internal_live:
    provider: azure_key_vault
    vault: kv-opensoft-xfactory-qa
    secret_ref: avatar-broker-openai-internal-live
    owner: opensoft-platform          # openxFactory avatar platform maintainers
    rotation_policy: <see §7.3>
```

Grounding for each field:

- `provider` / `vault` — the vault is already operated (live `az keyvault show` probe,
  two `SecretProviderClass` objects successfully rolled out backing the serving
  FastAPI+Postgres stack), already in the AKS QA estate the broker would deploy into, and
  **already the custodian of a model-provider token fetched by federated identity**
  (`review-lane-worker.yml`). Choosing it adds **zero new infrastructure** — it adds one
  secret and one `SecretProviderClass` entry to an estate that already does exactly this.
- `secret_ref` — a NEW secret, distinct from anything else in the vault, matching the
  "distinct binding" discipline that `credential-contracts` spec.md:147–148 requires of
  the dispatch/content pair. It must **not** reuse the F0 lab key: task 6.1.2
  (`tasks.md:382–384`) requires a "DEDICATED spend-capped internal-live provider
  project, distinct from the F0 lab project", so a distinct key follows.
- `owner` — `docs/sops/openai-realtime-f0-lab-credential.md` Credential Record already
  assigns "openxFactory avatar platform maintainers" as owner of the F0 key; carrying
  the same owner forward keeps rotation accountability where it already sits.
- The mode-600 local file (`$HOME/.ai-keys/openai.key`) and the age escrow copy in
  `xFactory-Agents-Credential-Registry` stay exactly as the SOP defines them —
  **developer-local convenience and supervised recovery material respectively, never a
  deployment source**, which is what §7.1's own sentence demands.

This satisfies spec.md:109–111 as written: long-lived headless token in a vault, fetched
by the runtime's own federated identity, ephemeral in process scope only.

### Alternative 1 — SOPS + age via Flux (`flux-system/sops-age`)

*Tradeoff:* it is the **first approved realization** in canon
(`credential-access-model.md:55–57`) and needs no Key Vault access grant, so it is the
lowest-permission path if KV RBAC is contentious. But it puts the provider key into a
committed ciphertext blob whose blast radius is "every secret that controller can
decrypt" (spec.md:83–84), and `credential-access-model.md:57` requires production use a
*different* recipient than QA — so an internal-live ring riding the QA recipient inherits
the QA blast radius. Against a cluster that already has KV+CSI wired, this is strictly
more coupling for no gain.

### Alternative 2 — openProfiler as the custodian

`openspec/changes/archive/2026-08-27-add-model-provider-broker/` (ratified 2026-08-26,
archived 2026-08-27) established openProfiler as **the** model-provider credential broker
for this org: it "holds the long-lived API key or OAuth grant and mints a SHORT-LIVED,
SCOPED token" (proposal.md:47–50), with a merged CLI declaration
(`docs/broker-cli.md`, openProfiler main `d0538c31`, PR #18) and a real
`openprofiler-broker` binary.

*Tradeoff:* it is the freshest and most on-point precedent in the corpus for exactly this
credential class, and reusing it would give one custody story for every model provider.
But its declared posture is a poor match here on two counts. First, on the `api_key`
path "the minted token IS the stored key verbatim" with `expires_at` as mere
"broker_bookkeeping" (proposal.md, answer to question 1) — so minting buys no real
scope reduction for an API-key provider, which is what this is. Second, openProfiler is
built as a **per-operator local custody surface for an interactive console**, not a
server-side vault for a long-running deployed broker. Using it would mean deploying
openProfiler into the AKS estate as a sidecar, which **is** net-new infrastructure and is
explicitly out of scope of the change that introduced it ("openProfiler itself is OUT of
scope and unbuilt" in that change's `code_surface`). Worth naming to Brett as a
deliberate *not now*, with a note that the two custody stories should converge later.

### What a later verifier would need

- The binding instance existing in the install's `credentials/` tree and validating
  against `contracts/schemas/xfactory-credential-contracts.schema.yaml`
  (`scripts/validate-credential-contracts.py` green).
- A `SecretProviderClass` naming `avatar-broker-openai-internal-live` in the broker's
  overlay, and a no-secret scan over the rendered manifest — the discipline
  `dox-aks-qa-kustomization.yaml:9–11` already applies ("no-secret scan over the render").
- Proof the broker resolves by reference at call time: no key in image, config, env
  baked at build, or log. This is RING-02's secret-scan condition.
- Confirmation that the F0 key was **not** reused — i.e. the internal-live provider
  project and its key are distinct from `openxfactory-realtime-f0-lab` (task 6.1.2).

---

# 7.2 — Numeric ceilings

> **AMENDED 2026-08-28 — the two dollar figures below were re-ruled, and this section is
> otherwise unchanged.** Brett re-ruled §7.2 in session on 2026-08-28: the
> provider-project HARD CAP is **$100 per calendar month** (was $750), with the
> provider's own native notifications at **50% ($50)** and **80% ($80)**; the METERED
> per-tenant budget is **$40 per calendar month** (was $150). The per-session ceilings —
> 15 minutes (900 s) and 300 billable units at 1 unit = 1 US cent (= $3.00), both hard
> and broker-enforced — are UNCHANGED, as is `uncountable_is: exhausted`, the
> metered-only posture of the per-tenant number and its §7.4 reader.
>
> **Why.** The $750 recommended and ruled below is a CEILING SIZED WITH HEADROOM: ~2.4×
> the ~$310 of whole-ring consumption modelled in the table further down. Brett re-sized
> it to ACTUAL EXPECTED SPEND, because the ring's tests are not expected to exceed ~$50.
> Note the two are not in conflict — the modelled ~$310 is the WHOLE qualification and
> the cap is PER CALENDAR MONTH — but the cap is now sized to the month it governs
> rather than to a runaway's outer bound. The per-tenant figure is a DEPENDENT value,
> not a second decision: a metered budget sitting above the hard cap is meaningless, so
> $150 could not survive a $100 cap. At $40, §7.10's two tenants carry $80 of metered
> exposure, still under the cap.
>
> The recommendation, grounding, alternatives and verifier notes below are left EXACTLY
> as written on 2026-08-27, because they are the record of what was recommended and what
> was ruled then. Read every dollar figure below as "recommended and ruled 2026-08-27";
> the live values are in `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml`
> and `contracts/avatar-client/usage-metering-and-alerting.yaml`.

### The task's own constraint text (tasks.md:678–679)

> - [ ] 7.2 Numeric ceilings: per-session duration and billable-unit limits, the
>       per-tenant budget, and the configured provider-project cap amount.

Fork 1 named gap 3 (fork-decision-memo.md:275–278):

> No numeric values are given anywhere: no per-session duration/billable-unit/dollar
> ceiling, no per-tenant budget, and no configured provider-project cap amount. F0
> recorded call counts (~183 short calls) but no cost figures or the cap value on
> `openxfactory-realtime-f0-lab`.

Fork 1 was ruled **Option C** — "session hard in broker, per-tenant hard at the provider
project, monitored counters for visibility" (fork-decision-memo.md:193–210). Task 6.1.5
(`tasks.md:391–394`) records the consequence: the durable synchronous per-tenant
cumulative-spend counter is **deferred, not built**, so "the provider-project cap is the
only per-tenant hard stop until it lands".

### The evidence base

**What F0 recorded — and did not.** `~183 short billed calls across the three rounds
(76 + 25 + 82)` on the dedicated spend-capped lab project
(`openspec/changes/archive/2026-08-09-qualify-avatar-brokered-call-feasibility/evidence/f0-terminal-pass-report-2026-07-12.md:92–93`).
**No dollar figure and no cap amount was ever recorded** — I checked all four F0 evidence
files; `f0d-revocation-rerun-notes-2026-07-12.md:110` says only "Total spend for the
session: bounded lab calls on the capped project". So F0 gives call *counts* but supplies
no measured cost to anchor to. The anchor has to be the provider's rate card.

**Provider rate card for the pinned candidate.** `gpt-realtime-2.1` is the candidate
pinned by the F0 contract (`docs/sops/openai-realtime-f0-lab-credential.md`, Credential
Record). Published rates (https://developers.openai.com/api/docs/pricing, "Realtime and
audio generation models"):

| Modality | Input /1M | Cached input /1M | Output /1M |
| --- | --- | --- | --- |
| Audio | $32.00 | $0.40 | $64.00 |
| Text | $4.00 | $0.40 | $24.00 |
| Image | $5.00 | $0.50 | — |

Token rates (https://developers.openai.com/api/docs/guides/realtime-costs): **user audio
= 1 token per 100 ms** (10 tok/s); **assistant audio = 1 token per 50 ms** (20 tok/s).
The same guide states the cost mechanic that makes a runaway expensive: *"The entire
conversation is sent to the model for each Response … turns later in the session will be
more expensive."* Caching cuts the re-sent history 80× ($32 → $0.40) but is
*"best-effort and not guaranteed."*

**Derived session-cost model** (my arithmetic from those two published sources; showing
it so Brett can move the assumptions):

Assume a 50/50 speaking split and a turn every ~20 s.

- Fresh tokens per conversational minute: 300 user audio tok ($0.0096) + 600 assistant
  audio tok ($0.0384) = **$0.048/min**.
- Re-sent history: accumulates ~900 tok/min; integrated over T minutes at the cached
  rate ≈ **$0.00054·T²**.

| Session length | Well-cached | Poorly-cached (history at full audio rate) |
| --- | --- | --- |
| 5 min | ~$0.25 | ~$1.3 |
| 10 min | ~$0.53 | ~$4.8 |
| 15 min | ~$0.84 | ~$10.4 |
| 30 min | ~$1.93 | ~$39 |

That quadratic right-hand column **is** the runaway Fork 1 exists to prevent, and it is
why a per-session ceiling has to be a cost ceiling and not only a duration ceiling.

**The enforcement point is real and already available.** The Realtime API returns a
`usage` block on every `response.done` event with `input_tokens`, `output_tokens`, and
`input_token_details.cached_tokens` broken out by modality
(realtime-costs guide, "Per-Response costs"). A broker can therefore accumulate
*actual* provider-attributed cost per session synchronously, turn by turn, and trip a
ceiling — no estimation and no new telemetry infrastructure needed.

**The house pattern for the field name — and an honesty correction.** The customer-memory
gateway carries `budget.max_billable_units` on `gateway_request` as a **synchronous
blocking rail** (`docs/customer-memory-gateway-architecture.md`, Rail Engine + Usage Meter
rows at lines 121/127, gateway_request budget block at 169–171, "budget gate when budget
can block" at line 905), cited in fork-decision-memo.md:137–144. The capability spec
formalises it — `openspec/specs/memory-gateway/spec.md:346–351`: *"WHEN a request exceeds a
configured hard budget limit for an operation class marked expensive … THEN the gateway
MUST deny the operation or route to an approved degraded mode **before provider I/O**"* —
with `expensive_operation_classes` in
`contracts/memory-gateway/provider-profile.schema.yaml` and the denial code
`budget_hard_limit` in `contracts/memory-gateway/vocabularies.yaml:89`.

**But it is not implemented.** `xfactory/memory_gateway.py` contains zero references to
`budget`, `max_billable_units`, or `max_latency_ms`, and the conformance fixture
`budget_hard_limit_denies_expensive_operation`
(`examples/memory-gateway/conformance-fixtures.yaml:214–220`) is **not** in
`SEMANTIC_FIXTURE_IDS` in `scripts/validate-memory-gateway.py`, so it is declared and
never executed. Fork 1's recommendation calls this "the house pattern … already makes
budget a synchronous blocking rail" (fork-decision-memo.md:228–229) — true of the
*contract*, not of any running code. **The vocabulary is worth borrowing; the
implementation does not exist to reuse.**

**The org's one genuinely code-enforced dollar ceiling** is codexFactory's
council-deliberation cap:
`[aggregation] xFactories/codexFactory/.github/workflows/scripts/deliberation_packet.py:101`
sets `SEAT_MAX_BUDGET_USD = 12`, passed to the worker as `--max-budget-usd`, and an
independent audit record confirms it is *"hard-enforced at the runtime"*
(`…/hermes/domain/review-councils/records/2026-08-22-seat-returns/company-policy-lead.md:42`).
Its **method** is directly transferable and is the model I follow below — the source
comment (lines 79–95) derives the ceiling explicitly:

```
worst-case input    250,000 x 4 = 1,000,000 tok @ $5.00/MTok  = $5.00
output cost         4 x 4,000  =    16,000 tok @ $25.00/MTok  = $0.40
worst-case seat     ................................... ~= $5.40
headroom (~2.2x)    ................................... ->  $12.00
```

One structural difference matters: codexFactory's worst case is *computable* because a
hard `MAX_PACKET_BYTES = 750_000` bounds the input. Here there is no equivalent bound —
best-effort caching means a session's history cost is not bounded within the duration
window — so the ceiling must be derived from the **expected** case with generous headroom
rather than from a computable worst case. That is why the headroom factor below is ~3.5×
rather than the precedent's 2.2×.

**The cohort that sets the scale.** `contracts/avatar-client/canary-cohort-and-rollback-policy.yaml`
`cohort:` — exactly two members: COHORT-01 the vendor organization's internal accounts,
COHORT-02 **exactly one** internally-staffed domain sandbox
(`cardinality: exactly_one`). So "per-tenant" divides by 2, not by N.

### RECOMMENDATION

| Value | Recommended | Enforcement |
| --- | --- | --- |
| **Per-session duration cap** | **15 minutes** (900 s) | HARD, synchronous, broker |
| **Per-session billable-unit cap** | **300 units, where 1 unit = 1 US cent of provider-attributed spend** (= $3.00) | HARD, synchronous, broker |
| **Per-tenant budget** | **$150 / calendar month per cohort member** | METERED + ALERTED only — *not* a hard stop (see below) |
| **Provider-project cap** | **$750 / calendar month**, alerts at 50% ($375) and 80% ($600) | HARD, at the provider project |

Grounding:

- **15 minutes.** The canary's sessions are scripted qualification scenarios — safety,
  exact-value, consent, handoff, blocked-state (task 6.2.1) — which run a few turns, and
  F0's calls were characterised as "short billed calls". 15 min is roughly 3× generous
  headroom against realistic scenario length, and it bounds the well-cached cost of a
  single session at ~$0.84. It also sits well inside the model's context window
  (gpt-realtime-2 context is 128,000 tokens; at ~900 tok/min a session would need ~140
  min to force truncation), so the cap never interacts with truncation semantics.
- **$3.00 per session.** Deliberately set ~3.5× the expected well-cached 15-minute cost
  ($0.84), so a normal session never trips it and the ceiling is not a nuisance — while
  still catching the poorly-cached runaway (~$10.40 at 15 min) at under a third of its
  course. The unit is cents rather than tokens because audio-out tokens cost 16× text-in
  tokens, so a token count is a bad cost proxy across modalities.
- **$150/tenant/month.** Two cohort members, sized so that the pair (~$300) sits
  comfortably under the project cap with room for the non-canary consumption below.
  **State plainly that this is a monitored threshold, not a rail** — Fork 1 Option C
  defers the durable cross-session counter (task 6.1.5), so nothing can hard-stop a
  single tenant. Recording it as hard would be false.
  **And give it a reader (see §7.4).** The org has already been bitten by a budget number
  nothing consumes: `[aggregation] xFactories/codexFactory/hermes/client/policy-overrides.yaml:24`
  carries `budget_envelopes: {}`, which a council reviewer flagged as *"no reader, no
  `spend_over_envelope` consumer, and no FAO seated… an unstated ~$456/day ceiling is not
  park-by-design"*
  (`…/records/2026-08-22-seat-returns/company-policy-lead.md:47–48`). A metered-only
  threshold with no alert wired to it is that same artifact.
- **Fail closed on an uncountable value.** The org's other real ceiling —
  `max_convenings_per_rolling_24h: 12` in
  `[aggregation] xFactories/codexFactory/scripts/merge_master/codexfactory-routine-code-clearance.yaml:279`,
  enforced in `…/merge_master/council_clearance.py:679–708` — encodes
  `uncountable_is: exhausted`: if the count cannot be determined, it is treated as spent.
  Recommend the same posture here, so a broker that cannot read its accumulated cost
  refuses the session rather than proceeding blind.
- **$750/month project cap.** Modelled against what the ring actually has to consume:

  | Ring consumer | Sessions | ~Cost |
  | --- | --- | --- |
  | §5 latency cells: 4 cells × 100 samples (see §7.5), setup-only ~$0.05 ea | 400 | ~$20 |
  | Re-runs / failed runs of the above | ~400 | ~$20 |
  | §6.2.1 eval corpus, 15 scenario classes, model-vs-model | ~300 | ~$100 |
  | §6.3 canary soak (see §7.6) | 200 | ~$110 |
  | Development, smoke, drills (F0 used ~183 such calls) | ~200 | ~$60 |
  | **Modelled total** | | **~$310** |

  $750 is ~2.4× the modelled consumption: ordinary operation never trips it, so it does
  not halt the qualification mid-run, but a genuine runaway is bounded at $750 instead of
  unbounded. This is the F0-proven pattern — SOP Provisioning Requirement 2 already
  mandates "configure project budget and rate controls before live trials" — with a
  number attached for the first time.

- **Also recommend, because task 6.1.3 asks for it** (`tasks.md:385–388`): a
  cost-triggered kill must carry "an auditable reason distinguishable from an ordinary
  duration or quota terminal". Since the broker reads real cost off `response.done`,
  the distinguishing reason code is cheap to emit and should be named now rather than
  discovered later. Fork 1 named gap 7 flags exactly this
  (fork-decision-memo.md:290–294).

### Alternative 1 — billable unit = 1,000 provider tokens instead of cents

*Tradeoff:* avoids embedding a rate card that the provider changes without notice, and
`max_billable_units` reads more naturally as a token count. But a token is a terrible
cost proxy here: 1k audio-output tokens cost $0.064 while 1k cached audio-input tokens
cost $0.0004 — a 160× spread. A token ceiling would either strangle short
audio-heavy sessions or fail to stop a long cache-missing one. If Brett prefers it, the
ceiling must be set against the *worst-case* modality mix, which makes it ~47,000 tokens
for the same $3.00 and correspondingly loose in the common case.

### Alternative 2 — lower, tighter numbers (10 min / $1.50 / $400 project cap)

*Tradeoff:* strictly safer on cost and closer to the "cannot run away" spirit, and it
would still cover the modelled ~$310 of ring consumption. But it leaves only ~$90 of
headroom, so one bad measurement day or one re-run of the §5 matrix exhausts the project
and **fails every session in the ring closed** — the hard stop firing on ordinary work
rather than on a runaway. Given the project cap is the ring's *only* per-tenant hard
stop, tripping it is expensive in schedule terms. Recommend against unless Brett wants
the ring deliberately short-leashed.

### What a later verifier would need

- The provider project's configured budget and rate controls **screenshotted or exported
  before first live trial**, showing the cap amount — the SOP already requires them set,
  but F0 never recorded the value, which is why this gap exists at all.
- The broker's session ceiling visible as configuration (duration + billable units), and
  a test proving a session that exceeds either terminates via the kernel's existing
  duration/quota terminal outcome (task 6.1.3 — "no new terminal is invented").
- A cost-triggered termination carrying its distinguishable reason code.
- Metering records showing per-tenant attribution against the two cohort members, so the
  $150 threshold has a subject (this depends on §7.10's "tenant" definition — see the
  coupling note at the end).

---

# 7.3 — Rotation cadence and trigger for the server key

### The task's own constraint text (tasks.md:680–682)

> - [ ] 7.3 Rotation cadence and trigger for the server key, written into the
>       binding's `rotation_policy`; the SOP gives the procedure but no
>       interval.

### What exists — a real structured precedent, and it is the only one

The `rotation_policy` **string** on a binding is an accountability label everywhere in
the corpus — `operator_managed`
(`examples/credential-contracts/openxdox-dispatch.binding-template.example.yaml:22,28`),
`client_managed` (`docs/domain-factory-starter-pack.md:810`), `tenant_managed`
(`docs/credential-access-model.md:225`), `opensoft_managed`, `firm_managed` — and the
schema permits nothing richer:
`contracts/schemas/xfactory-credential-contracts.schema.yaml:146` declares
`rotation_policy: {type: string}`.

**But the cadence lives in a separate, structured artifact**, and the survey found it:
`[aggregation] xFactories/OpsxFactory/credentials/policies/rotation-policy.yaml`
(`kind: xfactory_credential_rotation_policy`) carries the org's **only** numeric key-age
cadence *and* a ratified trigger vocabulary:

```yaml
rotation_policy:
  default_owner: client
  require_rotation_on:
    - client_offboarding
    - suspected_exposure
    - provider_policy_change
    - privileged_scope_change
  credential_overrides:
    github_administration_app:    {max_key_age_days: 90, additional_require_rotation_on: [administration_operator_change]}
    worker_enrollment_broker_app: {max_key_age_days: 90, ...}
    aks_workload_administration:  {max_key_age_days: 90, additional_require_rotation_on: [aks_administration_operator_change, namespace_scope_change]}
```

So: **90 days is the org's single stated maximum key age**, applied to exactly three
credentials, all Key Vault–held — the same custody shape §7.1 recommends. And the pattern
for triggers is established: a global `require_rotation_on` list, plus per-credential
`additional_require_rotation_on` entries. `ideation/staging/INDEX.md:517–518` independently
describes this as "the family's strictest existing tier (15-min grants, Key Vault, 90-day
max age, environment-gated)".

Symbolic 90-day tags also appear as free-text `rotation_policy` strings — e.g.
`rotated_90d_with_repository_and_scope_review` in
`[aggregation] xFactories/codexFactory/credentials/opensoft-self-client-bindings.yaml` —
but those carry no enforced override. The survey confirmed the tokens `"90d"`, `annual`
and `on_compromise` appear **nowhere** in the corpus, so there is no competing convention
to reconcile with.

The SOP supplies the **procedure** and nothing else —
`docs/sops/openai-realtime-f0-lab-credential.md` "Rotation and Revocation": create
replacement in the same project → install atomically or update the secret-manager version
→ run the non-disclosing auth check → revoke the old key at the provider → record owner,
date, reason, and logical reference, never the value. Plus a compromise path: if a key
appears in Git, chat, logs, evidence, screenshots or command history, treat it as
compromised, revoke immediately, replace, remove the artifact, scan, and record.

### A wording tension to rule on with eyes open

`credential-contracts` spec.md:111 says the vault-held worker credential is a
"**LONG-LIVED, NON-ROTATING** headless token". Read literally that forbids a cadence.
Read in context it does not: the same sentence continues "Rotation SHALL be a vault write
(effective the next job, no host administration)", and the phrase exists to contrast
against the *refused* class — "a refreshable session-state credential (one its consumer
rewrites in place) SHALL NOT be distributed by any channel". **"Non-rotating" means "not
self-refreshing", not "never rotated".** Worth stating in the ruling so a later reader
does not find the two clauses contradictory.

The practical consequence cuts toward a *shorter* cadence being affordable: if the
broker fetches per call through workload identity (the §7.1 recommendation), rotation is
one vault write with "no host access, no service restart, and no lane change"
(spec.md:113–116). If instead the degraded service-scoped mode is used, spec.md:128–131
requires the install record "rotation-requires-host-administration as an open gap" — and
then a tight cadence is real operational cost.

### RECOMMENDATION

Keep `rotation_policy: operator_managed` as the binding string (it is the value the two
live openxFactory bindings already use), and **carry the cadence in a
`xfactory_credential_rotation_policy` override, reusing the existing artifact's shape and
vocabulary verbatim**:

```yaml
credential_overrides:
  avatar_broker_openai_internal_live:
    max_key_age_days: 90
    additional_require_rotation_on:
      - avatar_platform_maintainer_change   # owning-group departure/role change
      - canary_cohort_change                # the cohort is the key's blast radius
      - release_ring_promotion              # never carry a qualification key into pilot
```

— inheriting the global `require_rotation_on` list unchanged
(`client_offboarding`, `suspected_exposure`, `provider_policy_change`,
`privileged_scope_change`), which already covers the SOP's compromise path via
`suspected_exposure`.

Grounding:

- **90 days** is not invented here: it is the org's **only** enforced key-age cadence,
  applied to the three Key Vault–held credentials in
  `[aggregation] xFactories/OpsxFactory/credentials/policies/rotation-policy.yaml`, and
  independently described as "the family's strictest existing tier"
  (`ideation/staging/INDEX.md:518`). Adopting it makes this a constrained instance of an
  existing tier rather than a new policy — the same move Fork 1's recommendation praises
  (fork-decision-memo.md:250–255).
- **The three added triggers follow the artifact's own established pattern** —
  `github_administration_app` adds `administration_operator_change`,
  `aks_workload_administration` adds `aks_administration_operator_change` and
  `namespace_scope_change`. Adding a maintainer-change and a scope-change trigger for
  this credential is the same idiom, not a new one.
- **90 days does not churn the evidence.** The recommended canary soak is 14 days
  (§7.6), so a 90-day cadence means **at most one rotation inside the ring**, and most
  likely zero. A 30-day cadence would risk a rotation mid-soak, which muddies the latency
  and error-rate evidence for no security gain at this blast radius.
- **The blast radius is already small**, which is what justifies 90 rather than 30: the
  key is scoped to a single dedicated spend-capped provider project (task 6.1.2), so a
  compromise is bounded by the §7.2 project cap ($750/month recommended) and cannot reach
  tenant data — the cohort's audio is synthetic or internally-consented only
  (`canary-cohort-and-rollback-policy.yaml` `audio_policy`).
- **Keeping `operator_managed` as the leading token** preserves compatibility with the
  two live bindings in the corpus and with spec.md:133–135's rule that the *operator* is
  a per-install binding — the cadence is a property of this install, the owner is not
  re-litigated.

### Alternative 1 — 30-day cadence

*Tradeoff:* materially tighter exposure window, and genuinely cheap **if** the
fetch-per-call workload-identity path is live, where rotation is one vault write
(spec.md:113–116). But if the install lands in the degraded service-scoped mode it means
12 host-administration events per year for a lab-grade key whose blast radius is one
capped provider project — friction with no proportionate gain — and it raises the chance
of a rotation landing inside the canary soak. Recommend only if the ring is expected to
run much longer than 14 days.

### Alternative 2 — event-triggered only, no interval

*Tradeoff:* it is the most literal reading of "LONG-LIVED, NON-ROTATING" (spec.md:111),
and it matches the *majority* of corpus bindings, which carry an owner label and no
numeric override. But it leaves this credential with **no interval — which is precisely
the gap §7.3 exists to close** — and it declines the one enforced tier the org actually
has. An unrotated key accumulates exposure across every operator who ever loaded it,
every evidence run, and every escrow round-trip. Recommend against; if chosen, record it
as a deliberate acceptance rather than an omission.

### What a later verifier would need

- A `max_key_age_days` override existing for this credential — not merely an owner label
  on the binding string — and the binding's `rotation_policy` naming an owner who exists.
- A rotation record — owner, date, reason, logical secret reference, never the value —
  per the SOP's step 5, for any rotation that occurs.
- Whether the install uses per-call fetch identity or the degraded service-scoped mode;
  if degraded, the open gap recorded per spec.md:128–131.
- Evidence that a rotation did **not** occur mid-soak, or if it did, that the latency
  cells were re-measured after it.

---

# 7.4 — Alerting channel, thresholds, and page targets for the usage meter

### The task's own constraint text (tasks.md:683–684)

> - [ ] 7.4 The alerting channel, thresholds and page targets for the usage
>       meter.

Task 6.1.4 (`tasks.md:389–390`): "Wire asynchronous usage metering and threshold
alerting for per-tenant visibility." Fork 1 named gap 6
(fork-decision-memo.md:286–289):

> No alerting channel or threshold is defined (who is paged, at what percentage of
> budget, with what latency). The memory gateway names a Usage Meter but no thresholds
> for this ring; Option B/C's "alerting" has no concrete wiring in the sources.

### ⚠️ NEW CAPABILITY — the honest finding

**This org operates no alerting plane. None.** A full survey of the aggregation tree
found no Prometheus, Grafana, Alertmanager, PagerDuty, Opsgenie, Azure Monitor Action
Group, Application Insights, SMTP alert, or Slack webhook wired into any running code
path. Specifically:

- **The one live service emits no metrics.** `hermes-install` exposes `/livez` and
  `/healthz`/`/readyz`
  (`[aggregation] installs/hermes-install/src/hermes_install/health/checks.py`), wired
  *only* to Kubernetes probes
  (`…/deploy/kubernetes/base/hermes-deployment.yaml:120–134`). That drives K8s
  self-healing; **it notifies no human**. There is no `/metrics` endpoint and no
  `prometheus_client` / `opentelemetry` import anywhere in the service or its deploy tree.
- **OpsxFactory's monitoring material is explicitly non-normative.**
  `[aggregation] xFactories/OpsxFactory/ideation/brainstorm/system-health-monitoring.md:1–4`
  carries `Status: brainstorm … Non-normative; nothing here changes promoted policy`, and
  its content is future-tense throughout ("If we ever adopt a managed backend, Azure
  Monitor is the natural fit"; "Grafana can be added later").
- **A notification controller is installed but unconfigured.** The QA cluster's vendored
  Flux bundle
  (`[aggregation] installs/omnigent-install/clients/opensoft/k8s/azure/clusters/qa/flux-system/gotk-components.yaml`)
  contains `alertmanager` / `opsgenie` / `pagerduty` / `slack` strings — but those are the
  **CRD enum** of provider types Flux *supports*. Zero `kind: Provider`, `kind: Alert`, or
  `kind: Receiver` resources exist anywhere in the tree. The capability is present; nothing
  points it at anyone.

**The only wired path that actually reaches a human is GitHub issue creation from CI**,
and it is used twice:

- `openxFactory/.github/workflows/doc-health-reusable.yml` — *"Open regression issue (one
  per run, contract regression rule)"*, running `gh issue create` when
  `new_count != '0'`, driven by the nightly cron in
  `[aggregation] .github/workflows/doc-health-nightly.yml`. It also auto-closes superseded
  issues.
- `[aggregation] .github/workflows/merge-master-approval.yml:807–842` — `gh issue create`
  with an `@brettheap —` mention in the body on a council-clearance event.

One adjacent capability *is* real and worth knowing: **Azure Monitor is already used to
measure dollar cost** — `[aggregation] xFactories/OpsxFactory/docs/farheap-sponsorship-to-opensoft-migration-runbook.md:36,83–84,145`
and the companion manifest record real measured Azure spend (~$490/month, ~$343/month,
$132.86/month) each tagged `measured: "2026-08-13 Azure Monitor…"`. So cost measurement
via Azure Monitor is an operated practice for infrastructure — just never for model/API
token spend, and never with an Action Group attached.

### RECOMMENDATION

**Two channels, neither of which builds new infrastructure:**

| Layer | Channel | Thresholds | Page target |
| --- | --- | --- | --- |
| **Primary — spend** | **The provider project's own native budget email alerts** on the dedicated internal-live project | **50% ($375) and 80% ($600)** of the §7.2 project cap; the cap itself is the hard stop | The named credential owner (openxFactory avatar platform maintainers) + the §7.7 kill-switch holder |
| **Secondary — org record** | **`gh issue create` from the metering job**, following the doc-health pattern verbatim (one issue per run, supersede-and-close prior) | Per-tenant metered spend crossing **$150/month** (§7.2); any cost-triggered session kill | The same named human, via `@`-mention as `merge-master-approval.yml` already does |

Why this shape:

- **The provider's own budget alerts are the only threshold mechanism that requires the
  org to build nothing**, and they sit directly on the dimension being metered. The SOP
  already mandates the underlying control — `docs/sops/openai-realtime-f0-lab-credential.md`
  Provisioning Requirement 2: *"Assign an owner and configure project budget and rate
  controls before live trials."* Turning on the notification thresholds that ship with
  that budget is a configuration step, not a project.
- **The GitHub-Issue channel is the org's only proven human-reaching path**, and it is
  proven twice, on a nightly cron, with supersede semantics already worked out. Reusing it
  keeps §7.4 a constrained instance of a working pattern.
- **50%/80%** because the §7.2 model puts expected ring consumption at ~$310 against a
  $750 cap: 50% ($375) fires just above expected total consumption — i.e. it means "this
  ring is running hotter than modelled", which is exactly when a human should look — and
  80% ($600) means "you have roughly one week of margin left".

**Name the page target as a person or rota, not a role.** This is the same gap as §7.7:
`canary-cohort-and-rollback-policy.yaml` `operator_surface.status: unnamed` warns that
"a canary opened without a named holder has an unfireable kill switch". An alert with no
named recipient fails the same way. **Recommend the alert recipient and the kill-switch
holder be the same named human**, so the person who learns about the spend is the person
who can stop it.

**A cautionary precedent worth putting in front of Brett.** The org has already been bitten
by a budget number nothing reads: `[aggregation] xFactories/codexFactory/hermes/client/policy-overrides.yaml:24`
carries `budget_envelopes: {}`, and a council reviewer flagged it by name —
*"`budget_envelopes: {}` with **no reader**, no `spend_over_envelope` consumer, and no FAO
seated… an unstated ~$456/day ceiling is not park-by-design"*
(`…/hermes/domain/review-councils/records/2026-08-22-seat-returns/company-policy-lead.md:47–48`).
The §7.2 per-tenant budget is metered-only by ruling (Fork 1 Option C defers the hard
counter), so **it will be exactly such a number unless §7.4 gives it a reader.** That is
the strongest argument for wiring the secondary channel rather than relying on the
provider alert alone.

### Alternative 1 — Azure Monitor Action Group on the AKS estate

*Tradeoff:* it is the "proper" answer, the subscription already exists, and Azure Monitor
is already used to measure real dollar spend in this org (the farheap migration records).
An Action Group can page email/SMS/webhook and would give the ring a real alerting plane
that later work could reuse. **But ⚠️ this is NEW CAPABILITY**: no Action Group, alert
rule, metric export, or `/metrics` endpoint exists today, and the broker would additionally
need to emit metrics it currently has no mechanism to emit. That is a meaningful project
sitting on the critical path of a qualification ring — precisely the "net-new
infrastructure" Fork 1's Option C ruling was chosen to avoid importing
(fork-decision-memo.md:231–243). Recommend as pilot-hardening work, named now, not built now.

### Alternative 2 — configure the Flux notification-controller that is already installed

*Tradeoff:* the controller is genuinely present in the QA cluster and its provider enum
includes Slack, PagerDuty, Opsgenie and generic webhooks, so a `kind: Provider` +
`kind: Alert` pair would be a small change rather than a deployment. **But it is the wrong
instrument**: Flux's notification controller reports on *GitOps reconciliation* events —
kustomization applied, health check failed — not on application-level spend counters. It
cannot see a usage meter. Mentioned because "Flux already has alerting" is a tempting and
wrong conclusion from grepping the tree.

### What a later verifier would need

- The provider project's budget notification thresholds configured and their recipient
  list exported, **before first live trial** — same evidence moment as §7.2's cap amount.
- A named human (not a role) recorded as the page target, matching §7.7's kill-switch
  holder.
- At least one **delivered** alert observed end-to-end before the canary opens — a
  threshold deliberately tripped low, or a test issue filed — because an untested alert
  path is indistinguishable from no alert path. This is the §7.4 analogue of RING-04's
  "exercised for real" discipline.
- The metering job's issue-creation step present and its supersede-and-close behaviour
  matching the doc-health pattern, so the ring does not accumulate stale open issues.

---

# 7.5 — Minimum sample count per gated latency cell

### The task's own constraint text (tasks.md:685)

> - [ ] 7.5 Minimum sample count per gated latency cell (feeds §5.2).

§5.2 (`tasks.md:356–357`):

> - [ ] 5.2 Declare the minimum sample count per gated cell BEFORE measuring,
>       and record it with the evidence (§7.5).

Fork 2 named gap 4 (fork-decision-memo.md:492–495):

> Minimum sample count / trial volume for statistically valid internal-live latency
> evidence is unspecified. F0 used 30-40 samples; nothing defines how many turns/sessions
> per platform cell the internal-live latency evidence needs, which directly bounds
> whether even p95 (let alone p99) is trustworthy.

### What "a cell" is, and how many there are

`contracts/avatar-client/acceptance-map.yaml` `latency_slo` (ALV-SLO-001) defines the
comparison: `comparison_cell.must_match: [platform, network_class, region]`, with
`reference_classification` separating the two sides, and *"A comparison whose two sides
do not share all three axes is REFUSED as evidence rather than evaluated."* The gated
set is `platforms: [windows_desktop, web_canvas]`, `network_class: nominal`,
`percentiles: [p50, p95]`, `intervals: [first_playable_after_authorized_ms,
sideband_ready_after_request_ms]`.

So the **sampling** cells are 2 platforms × 1 network class × 2 reference
classifications = **4 cells**. Both gated intervals come off the *same* session
(`contracts/avatar-client/avc-10-voice-latency-sample.schema.yaml:126–127` — both are
`derived_intervals` of one sample), so a cell's n serves both intervals and both
percentiles.

### The threshold the sample size has to serve

ALV-SLO-001 `materiality`: *"adapter > reference + max(0.15 × reference, 150)"*. Applied
to F0's own distributions (`f0-results.json` metrics block) the thresholds are:

| Interval | F0 p50 / p95 | Threshold at p50 | Threshold at p95 |
| --- | --- | --- | --- |
| `first_playable_after_authorized_ms` (n=40) | 603.63 / 643.488 (max 665.766) | 150 ms | 150 ms |
| `sideband_ready_ms` (n=30) | 772.37 / 1642.119 (max 1663.667) | 150 ms | 246 ms |

### The statistical argument, kept practical

The count of samples exceeding the true p95 is Binomial(n, 0.05):

| n | Expected above p95 | SD | What the p95 estimate actually is |
| --- | --- | --- | --- |
| 20 | 1.0 | 0.97 | the maximum — not a percentile |
| 30 (F0 sideband) | 1.5 | 1.19 | roughly the 2nd-largest value; one outlier moves it |
| 40 (F0 first-playable) | 2.0 | 1.38 | roughly the 2nd–3rd largest |
| **100** | **5.0** | **2.18** | **an interior order statistic, ~top 3–7** |
| 200 | 10.0 | 3.08 | ~top 7–13 |
| 500 | 25.0 | 4.87 | ~top 20–30 |

Translating into the two F0 distributions:

- **`first_playable` is tight.** p95→max spans only 22.3 ms across ~2 order statistics.
  So even n=40 gives a p95 stable to roughly ±20 ms — comfortably inside the 150 ms
  floor. This cell is not the problem.
- **`sideband_ready` is not.** p50→p95 spans **870 ms** — the distribution is broadly
  dispersed through its middle, so the region where p95 sits is steep. At n=30 the p95
  estimate is essentially "the 2nd-largest of 30", whose nonparametric 95% interval spans
  roughly order statistics 27–30, i.e. *"somewhere between the 4th-largest and the
  maximum."* That is a **maximum estimate wearing a percentile's name**, and its swing
  is plausibly comparable to the 246 ms threshold it is meant to test. This cell is why
  n=30 must not be carried forward.

**The cost argument removes the usual excuse.** 4 cells × 100 samples = 400 setup-only
sessions. Setup-interval measurement needs a session to connect, reach first-playable,
and hang up — the "short billed calls" class F0 ran ~183 of. At ~$0.05 each that is
**~$20**, against a recommended $750 project cap (§7.2). There is no meaningful cost
tension between the statistically defensible number and the affordable one, so the
defensible one should win.

### RECOMMENDATION

**n ≥ 100 completed, schema-valid AVC-10 samples per gated cell**, with three
accompanying rules:

1. **Declared before measuring** and recorded with the evidence — §5.2 already requires
   this; the value is 100.
2. **A cell with n < 100 is RECORDED but MUST NOT GATE.** This slots into ALV-SLO-001's
   existing refusal machinery: the map already refuses a comparison whose sides do not
   share platform/network/region, so "insufficient n" becomes a second refusal reason
   rather than a new mechanism.
3. **Samples must span at least 3 distinct measurement runs on ≥2 distinct days per
   cell.** F0's entire dataset came from one harness, one configuration, region `null`,
   in one sitting (`f0-results.json` environment block) — and single-configuration bias
   is the memo's core complaint about it (tasks.md:350–355). A minimum n taken all at
   once would repeat that mistake with a bigger number.

Also worth recording now, because it is a live misreading risk: **at n=100, p99 is
effectively the maximum** (1 expected sample above it). The acceptance map already keeps
p99 `recorded_not_gated` and calls it a candidate "to become [a] hard gate at the pilot
ring **when sample volume supports them**". Gating p99 would need n ≥ ~500 per cell.
Saying so now prevents someone at the pilot gate reading the recorded p99 as
gate-ready.

### Alternative 1 — n ≥ 50

*Tradeoff:* halves the measurement run and still keeps p95 interior (~2.5 expected
above). Defensible for `first_playable`, whose tight distribution means the estimate
barely moves. But it is **not** defensible for `sideband_ready`, where the dispersion
puts the estimate's interval in the same order of magnitude as the 246 ms threshold —
the gate would be reading noise. If Brett wants a cheaper option, the honest form is a
**split minimum** (n ≥ 50 for `first_playable`, n ≥ 100 for `sideband_ready`), not a flat
50 — though the ~$10 saved does not obviously justify a two-number rule.

### Alternative 2 — n ≥ 384 (the classic sample-size formula)

*Tradeoff:* it is the number people reach for, and it would make even p99 respectable.
But it is the **wrong formula** — n=384 bounds the margin of error on a *proportion* at
±5%, not on a latency *quantile*. Applying it here is cargo-cult rigor: it would cost
4 × 384 = 1,536 sessions and considerable wall-clock for a p95 estimate that is already
stable at 100 against a 150–246 ms threshold. Mentioned so the ruling can dismiss it
knowingly.

### What a later verifier would need

- The declared minimum recorded in the evidence *before* the measurement timestamps —
  §5.2's "BEFORE measuring" is the whole point and is checkable by ordering.
- Per-cell `n` reported alongside p50/p95 in `measured_evidence`, so a reader can
  recompute rather than trust.
- The raw AVC-10 samples retained and countable per cell, with their
  `platform` / `network_class` / `region` / `reference_classification` fields populated
  so cell membership is derivable, not asserted.
- Run and date spread per cell, to check rule 3.

---

# 7.6 — Canary exit criteria

> **AMENDED 2026-08-28 — the session count below was re-ruled, and nothing else in this
> section moved.** The minimum is **100 completed canary sessions** (was 200), with
> sub-floors of **≥25 from COHORT-02** (was ≥50) and **≥3 per evaluation scenario class**
> UNCHANGED. The 14-day soak on ≥10 distinct days, the ≤2% overall / ≤5% trailing-50
> rates, the definition of ABNORMAL and both additional criteria are UNCHANGED.
>
> **Why.** This is a DEPENDENT consequence of the same day's §7.2 re-ruling, not a new
> measurability judgment. The cost check at the end of this section's grounding —
> 200 sessions × ~$0.55 ≈ $110 — was written against a $750 project cap; against the
> re-ruled **$100** cap the same arithmetic hits the cap BEFORE the canary can exit, so
> the count had to follow the cap or the two would have been ruled to fight each other.
> At n=100 the §6.2.1 coverage floor (15 × 3 = 45) is still cleared with ~2.2× headroom
> and the tolerated rates are still countable thresholds: 2% is 2 sessions and 5% is 5.
> The COHORT-02 sub-floor keeps its one-quarter share of the count.
>
> The recommendation and grounding below stand as written on 2026-08-27; read their
> numbers as the 2026-08-27 record.

### The task's own constraint text (tasks.md:686–687)

> - [ ] 7.6 Canary exit criteria: soak duration, minimum session count, and
>       tolerated error rate.

The policy artifact records these as deliberately open —
`contracts/avatar-client/canary-cohort-and-rollback-policy.yaml:262–270`:

```yaml
canary_exit_criteria:
  owning_task: qualify-avatar-live-voice 7.6
  status: unset
  unset_values: [soak_duration, minimum_session_count, tolerated_error_rate]
  statement: >-
    Soak duration, minimum session count and tolerated error rate are §7
    authoring inputs and are NOT set by this policy. They are recorded as open
    so that a canary cannot be declared successful against criteria invented
    after the fact.
```

Fork 5 named gap 3 (fork-decision-memo.md:1179–1183) confirms no numeric canary
thresholds exist anywhere.

### What already sits either side of these criteria

- **Rollback *mechanism* rehearsal is already a PRE-canary gate, not an exit criterion.**
  `contracts/avatar-client/internal-live-activation-checklist.yaml` RING-04 requires both
  kill switches "exercised for real, each in BOTH block-new and revoke-active modes,
  **BEFORE any canary traffic**." So §7.6 must not duplicate it.
- **But the *detection wiring* is not covered by RING-04.** ROLLBACK-A and ROLLBACK-B
  both carry `detection_wiring_owner: qualify-avatar-live-voice 6.3.3`, and 6.3.3
  ("Build the auto-detection wiring … since Option B was chosen precisely for this
  rehearsal value", tasks.md:476–478) is unticked. The policy header states the rationale
  outright (lines 26–31): Option B was chosen over Option A *"precisely for its rehearsal
  value: Option A never exercises active-lease revocation outside the consent and control
  terminals, so it would arrive at the pilot gate with the revocation policy still
  untested, and the pilot ring requires rollback rehearsal."*
- **The scenario matrix that sets a coverage floor:** task 6.2.1 requires evaluation
  across "safety, exact-value, consent, handoff and blocked-state scenarios across
  generic, MedxFactory and LedgerxFactory" = **15 scenario classes**.
- **ROLLBACK-B needs a number anyway.** Its trigger list includes `elevated_error_rate`
  with no threshold defined — so §7.6's error rate and ROLLBACK-B's trip point should be
  ruled together or they will disagree.

### RECOMMENDATION

| Criterion | Recommended |
| --- | --- |
| **`soak_duration`** | **14 consecutive calendar days** of canary availability, with canary sessions occurring on **≥10 distinct days** |
| **`minimum_session_count`** | **200 completed canary sessions**, with sub-floors: **≥50 from COHORT-02** (the domain sandbox) and **≥3 per §6.2.1 evaluation scenario class** |
| **`tolerated_error_rate`** | **≤2% abnormal-session rate over the full soak**, AND **≤5% over any trailing 50-session window** (the latter doubling as ROLLBACK-B's `elevated_error_rate` trip) |

Plus two criteria beyond the three §7.6 names, which I recommend adding because without
them the ring's own stated rationale goes undelivered:

| Additional criterion | Why |
| --- | --- |
| **≥1 live ROLLBACK-B auto-trip proven end-to-end through the §6.3.3 detection wiring** (injected if it does not occur naturally), with in-flight legs observed draining and `revoke_active_leases: false` honoured | RING-04 proves the *switch* works; nothing otherwise proves the *detection* works. Option B was chosen for rehearsal value; an untripped detector is an unrehearsed detector. |
| **Zero unresolved ROLLBACK-A trips at exit** | A safety/integrity breach open at exit would promote a known-unsafe profile toward pilot. |

Grounding for the numbers:

- **200 sessions** is set by measurability, not by feel. The coverage floor alone is
  15 scenario classes × 3 = 45. But a "≤2%" criterion is unmeasurable at small n: at
  n=50, a single failure is already 2%, so the criterion cannot distinguish a good ring
  from a marginal one. At n=200, 2% = 4 sessions and 5% = 10 sessions — distinguishable
  counts, so the criterion can actually be evaluated. 200 also gives ~4× headroom over
  the coverage floor.
- **≥50 from COHORT-02** because the cohort has exactly two members
  (`cardinality: exactly_one` on the domain sandbox) and the domain sandbox is the only
  member that exercises DomainxFactory interpretation. Without a floor, 199 vendor-org
  sessions and 1 sandbox session would technically satisfy "200".
- **14 days** covers two full business weeks — the cohort is internal staff, so usage is
  weekday-shaped — and spans typical provider deploy cadence, so a provider-side change
  has a real chance of surfacing inside the ring rather than after it. F0's own campaign
  ran in three separate rounds (76 + 25 + 82,
  `f0-terminal-pass-report-2026-07-12.md:92`) and the later rounds surfaced behavior the
  first did not; a single-block soak repeats F0's single-configuration weakness.
- **≥10 distinct days** stops 200 sessions being run in two frantic afternoons, which
  would satisfy the count while defeating the soak's purpose.
- **2% / 5%** is anchored to observed provider behavior: across ~183 F0 calls, no
  provider-side failure class was recorded, and the one failed smoke was a *client
  harness* defect ("the live smoke test does not hang up its call on the failure path",
  `f0-live-run-notes-2026-07-12.md:88–93`). So 2% is generous against observed provider
  reliability while leaving headroom for harness flakiness; 5% over a trailing window is
  an unambiguous degradation worth auto-blocking new sessions on.
- **Cost check** (ties to §7.2): 200 sessions × ~$0.55 ≈ $110, comfortably inside the
  recommended $750 project cap.

**Define "abnormal" explicitly** or the rate is unfalsifiable. Recommended definition: a
session that fails to reach `first_playable_after_authorized`, **or** terminates to a
non-clean terminal that is not a deliberate test action (consent withdrawal drills,
injected rollback rehearsals, and operator-fired ROLLBACK-C are excluded and counted
separately).

### Alternative 1 — 7-day soak / 100 sessions / ≤3%

*Tradeoff:* reaches the internal-live exit roughly twice as fast, which matters if the
pilot ring is schedule-driven, and 100 sessions still clears the 45-session coverage
floor. But a 7-day soak covers one business week, so a weekly provider deploy cycle can
sit entirely outside it, and at n=100 a ≤3% criterion turns on 3 sessions — thin enough
that one bad afternoon decides the gate. Reasonable if Brett wants speed and accepts a
weaker claim.

### Alternative 2 — 30-day soak / 500 sessions / ≤1%

*Tradeoff:* a genuinely strong qualification claim, and it would additionally bring p99
into gateable sample territory for the pilot ring (see §7.5). But it costs ~$275 of
canary spend alone, needs a 90-day key rotation to be checked against the soak window
(§7.3), and — the real objection — internal-live is **qualification, not pilot**. The
cohort is two internal members with synthetic audio; a 30-day soak over that cohort
mostly re-measures the same two tenants rather than discovering anything new. Depth here
buys less than moving to the pilot ring, which owns real-tenant scale
(`canary-cohort-and-rollback-policy.yaml` `external_tenants`).

### What a later verifier would need

- Canary session records with timestamps, cohort-member attribution, and terminal
  outcome, so count / day-spread / per-member floors / error rate are all recomputable.
- Per-scenario-class session counts against the §6.2.1 matrix.
- Evidence of the ROLLBACK-B trip: the detection event, the block-new taking effect, and
  in-flight legs reaching their natural terminal without revocation.
- The `canary_exit_criteria` block in `canary-cohort-and-rollback-policy.yaml` moved from
  `status: unset` to the ruled values **before** the canary opens — the artifact's own
  statement says these exist "so that a canary cannot be declared successful against
  criteria invented after the fact", so the ordering is itself the evidence.

---

## Couplings the orchestrator should put to Brett together

These are not extra questions; they are places where two §7 answers must agree or one of
them has no subject.

1. **§7.2 ↔ §7.10 ("tenant").** The per-tenant budget has no subject until "tenant" is
   defined. `canary-cohort-and-rollback-policy.yaml` `tenant_definition_ref` records this
   as `status: unset` with the note that it "MUST agree with this cohort or the
   per-tenant spend and metering dimensions have no subject". Recommend defining tenant
   = cohort member (2 tenants), which is what §7.2's $150 figure assumes.
2. **§7.4 ↔ §7.7 (operator surface).** An alert with no named recipient and a kill switch
   with no named holder are the same gap seen twice.
   `canary-cohort-and-rollback-policy.yaml` `operator_surface.status: unnamed` warns that
   "a canary opened without a named holder has an unfireable kill switch". The alert page
   target and the kill-switch holder should be the same named person or rota.
3. **§7.4 is what makes §7.2's per-tenant budget real.** Because Fork 1 Option C defers the
   hard per-tenant counter, the $150 figure is metered-only — and a metered-only number
   with no alert wired to it is the `budget_envelopes: {}` failure the org has already had
   flagged in review. Ruling §7.2's per-tenant number without ruling §7.4's channel
   produces a value nothing reads.
4. **§7.6 ↔ ROLLBACK-B.** The tolerated error rate and ROLLBACK-B's undefined
   `elevated_error_rate` trigger must be ruled as one number, or the canary can pass its
   exit criterion while its auto-blocker is tripping (or vice versa).
5. **§7.5 ↔ §7.2.** The recommended n=100 × 4 cells is priced into the §7.2 project-cap
   model. Raising n materially raises the ring's spend.
