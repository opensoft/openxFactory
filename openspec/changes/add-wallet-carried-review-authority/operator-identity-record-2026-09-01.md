# Operator identity record — Packet 2 / R5 — SIGNED 2026-09-01

    Status: record (SIGNED by the Operator 2026-09-01, in-session; this is the scratchpad copy — NOT YET committed to a governed repository; the register act carries it there)
    Drafted: 2026-08-31, by the Opus soak executor, at the coordinator's direction
    Signed: 2026-09-01, by the Operator (Brett Heap), in-session — see §8
    THIS RECORD WAS PERFORMED AND SIGNED BY THE OPERATOR ON 2026-09-01. It was
    drafted 2026-08-31 so that the Operator could perform each verification
    act; every field the drafter could not evidence was marked
    OPERATOR-VERIFICATION-PENDING with the place it is read back, and each
    such field now carries the Operator's read-back (EXE-3, EXE-5, SEM-1,
    2026-09-01) or the live-run evidence harvested for it (EXE-4, EXE-6 from
    xFactory run 33513966619; EXE-1, EXE-2 from run 33577170272). The
    drafter's own limits (§2.2, §3.1, §3.2) are retained as history of what
    the draft could and could not assert; nothing in this record is asserted
    on the drafter's authority.

## 0. Why this record exists, and what blocks on it

The register act's citation is fixed at three things (run-2 record §12.3): the
activation ruling, the roster-change record, and **this record — "the Operator
identity record, still owed per R5"**. R5's own closing sentence:

> **What makes R5 enforceable:** the Operator identity record itself — the
> Packet 2 record carrying semantic identity, execution identity, ratification-
> time and execution-time evidence, and the Operator's signature. A plane
> ruling is not an identity record; until that record exists, governed issuance
> and activation stay blocked exactly as report §7 states.

**Governing constraint, quoted because the whole record turns on it:**

> The plane is the RULED TARGET; the transport is not the evidence for it.
> Claude Code can be configured atop Bedrock, Vertex or Foundry, so invoking
> Claude Code establishes no plane at all.

Accordingly **this record makes the plane claim only as §3 evidences it, by
read-back: the DIRECT ANTHROPIC plane (§3.5, signed §7–§8).** §3 states what
evidences the plane and who read it back.

---

## 1. Record identity

| Field | Content |
| --- | --- |
| Record ID | `s5-operator-identity-2026-09-01` — **RULED 2026-09-01 by the Operator**; assigned in advance of signature, dated to the day the §3 verification acts were performed |
| Seats covered | `lead-quality`, `lead-security`, `lead-integration` (domain); `company-policy-lead` (tenant) |
| Operator | **Brett Heap** — signature slot at §8 |
| Decision date | **2026-09-01** — the §3 read-backs EXE-3/EXE-5/SEM-1 were performed by the Operator that day; EXE-4/EXE-6 evidenced from the same day's runs |
| Review expiry | **2027-06-30** — **RULED by the Operator**: bound to the earliest PINNED component's retirement floor (`claude-sonnet-5`, "Not sooner than June 30, 2027", SEM-1 confirmed 2026-09-01); `claude-haiku-4-5-20251001`'s **2026-10-15** is earlier but is NOT a pinned component (§2.3); Anthropic's ≥60-day retirement notice (SEM-1) is the interim trigger |
| Drafter | Opus soak executor. **The drafter is not the Operator and signs nothing.** |

---

## 2. Semantic identity — EVIDENCED (survey) + EVIDENCED (live resolution)

### 2.1 The two pinned models

Identifiers spelled exactly as the surveyed first-party documentation spells
them. Survey source: the merged S5 research report's **Candidate Evidence
Register** (§2A), which states its own limits — lifecycle floors are published
earliest-retirement dates, not commitments about behavior.

| Field | `claude-opus-5` | `claude-sonnet-5` |
| --- | --- | --- |
| Provider | Anthropic | Anthropic |
| Exact published ID | `claude-opus-5` | `claude-sonnet-5` |
| Class | Snapshot (dateless but pinned) | Snapshot (dateless but pinned) |
| Alias that must NEVER be recorded as the pin | the transport selector `opus` | the transport selector `sonnet` |
| Published mutation semantics | *"Anthropic does not update the weights or configuration of an existing model ID. When an updated version is available, it ships under a new model ID."* | as above |
| Retirement floor | **not sooner than 2027-07-24**; at least 60 days of notice | **not sooner than 2027-06-30** |
| Pinnability note | strongest published guarantee in the survey and the longest horizon; the guarantee covers **weights**, while serving infrastructure *"can change over time"* | as above |
| Documentation source | **EVIDENCED (SEM-1)** — see §2.2 |

**Seat assignment** (`hermes/domain/agent-mixes.yaml`, `selector_kind:
exact_provider_version`, `pin_status: pinned` on all four):
`lead-quality` → `claude-sonnet-5`; `lead-security` → `claude-opus-5`;
`lead-integration` → `claude-opus-5`; `company-policy-lead` → `claude-sonnet-5`
(tenant-declared, `authority_ref` `hermes/client/role-overrides.yaml`).

### 2.2 The one semantic-identity gap the drafter cannot close

The template requires **"source URL or document, source access date"**. The
research report is a *survey* of first-party documentation, not the
documentation. **The drafter did not access Anthropic's model documentation and
must not cite it as if he had.**

> **EVIDENCED (SEM-1).** Access date 2026-09-01; the Operator confirmed the
> lines on screen. **Note the docs domain moved:**
> `docs.anthropic.com` now 301-redirects to `platform.claude.com` — the live
> URLs are recorded below.
>
> 1. `https://platform.claude.com/docs/en/about-claude/model-deprecations` —
>    "Model status" table: `claude-opus-5 | Active | N/A | Not sooner than
>    July 24, 2027`; `claude-sonnet-5 | Active | N/A | Not sooner than June
>    30, 2027`. "Notifications": *"at least 60 days' notice before model
>    retirement for publicly released models."*
> 2. `https://platform.claude.com/docs/en/docs/about-claude/models/overview`
>    — "Compare models" table, Retirement row: same two dates; Claude API ID
>    row: `claude-opus-5`, `claude-sonnet-5`; footnote: *"Every Claude model
>    ID is a pinned snapshot, including the dateless IDs used from the 4.6
>    generation on."*
> 3. `https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions`
>    — "Dateless IDs are pinned snapshots": *"Anthropic does not update the
>    weights or configuration of an existing model ID. When an updated
>    version is available, it ships under a new model ID."*; "Model weights
>    versus serving infrastructure": *"Model weights are fixed for a given
>    ID, but the serving infrastructure around the model can change over
>    time."*
>
> All three lifecycle facts this record carries at §2.1 are CONFIRMED
> unchanged by these first-party pages. **Read back at:** the three URLs
> above. A survey row is not a documentation capture — this is the capture.

### 2.3 LIVE RESOLUTION — EVIDENCED, 80 judgments

This is the strongest thing the drafter can put on the record, and it is
execution-time evidence of the *semantic* layer only.

Across **80 retained seat judgments** — 71 in run 1 (47 corrected-draw + 24
draw-1), 3 in run 2, 6 in run 3 — the runtime's `modelUsage` map was captured
verbatim in every case. Counts, computed from the retained envelopes:

| Identifier returned | Occurrences | `canonicalModel` | `contextWindow` |
| --- | --- | --- | --- |
| `claude-opus-5` | **54** | `claude-opus-5` | 1,000,000 |
| `claude-sonnet-5` | **26** | `claude-sonnet-5` | 1,000,000 |
| `claude-haiku-4-5-20251001` | **80 of 80** | `claude-haiku-4-5` | 200,000 |

* **The declared pin appeared in the served map in 80 of 80 judgments.** Every
  invocation declared an exact identifier (`--model claude-opus-5` or
  `--model claude-sonnet-5`), never an alias.
* **No substitution was observed in any judgment.** No returned identifier
  differed from the one declared, and the shipped floor's PROPERTY 3
  (`declared not in served` ⇒ refuse) was applied off-lane to every row and
  refused none.
* **`claude-haiku-4-5-20251001` executed in 80 of 80** and is **declared in no
  composition file** — R-IV. It is the CLI's internal helper (~1,000 input /
  ~16 output tokens per run) and **it carries the earliest retirement floor in
  the register, 2026-10-15**. **No fully-pinned-composition claim is made by
  this record**, and the helper's disposition — declared in the composition or
  refused at read-back — belongs to the R6–R12 change (2026-08-29 §6.1, P-1),
  not here.

**Read-back mechanism, stated so it can be checked:** the `modelUsage` map in
the runtime envelope returned by `claude -p --output-format json`, transcribed
verbatim (all eleven fields per entry) into each retained per-judgment file.

**What this evidence is NOT.** Every one of the 80 judgments ran
**workstation-direct**, not in the lane. See §3.

---

## 3. Execution identity — THE PLANE, EVIDENCED BY READ-BACK (EXE-1/EXE-2)

### 3.1 The drafter's runs cannot evidence the plane, and here is why

All 80 judgments were direct `claude -p` invocations on an operator
workstation. **The worker's `env -i` credential scrub was NOT reproduced** —
the same single named deviation carried by the 2026-08-22 corpus, the
2026-08-31 CSC-C1′ inventory and all three soak runs. Every one of those
records states the consequence and this one restates it rather than inheriting
it:

> **Nothing produced on that route may be read as evidence of the PROVIDER
> PLANE.** (LS-C1: *"This Council does not evidence the plane and must not
> appear to."*)

**The `provider: firstParty` field appears on all three identifiers in all 80
envelopes. It is recorded here as measured and is NOT offered as plane
evidence.** R5 requires the plane be evidenced by read-back of the *provider
selection and endpoint configuration*; a response field is neither, and R5's
own text forbids inferring the plane from the transport.

**The lane's own read-back is the other half of this record — supplied at
§3.3 (EXE-1/EXE-2) from the seat's print-back in xFactory run 33577170272.**

### 3.2 What the drafter CAN evidence statically — necessary, not sufficient

Verified against the committed tree at codexFactory `5def29ac`
(`council-deliberation-worker.yml`, sha256
`0581b1f3f0465ce7113e90720a4a73076f40c2a45047b482d798203aa707077d`):

1. **The seat invocation runs under `env -i` with an explicit six-variable
   allowlist.** Verbatim:

```
env -i PATH="$PATH" HOME="$HOME" LANG="${LANG:-C.UTF-8}" \
  ${USERPROFILE:+USERPROFILE="$USERPROFILE"} \
  ${APPDATA:+APPDATA="$APPDATA"} \
  ${CLAUDE_CODE_OAUTH_TOKEN:+CLAUDE_CODE_OAUTH_TOKEN="$CLAUDE_CODE_OAUTH_TOKEN"} \
  CLAUDE_CONFIG_DIR="${RUNNER_TEMP}/claude-cfg-${SEAT}" \
  CLAUDE_CODE_SKIP_PROMPT_HISTORY=1 \
  claude -p --model "$MODEL" ...
```

   `env -i` clears the environment and re-adds only those names. **Every
   provider-routing environment variable is therefore structurally absent from
   the seat's environment by construction rather than by configuration.**

2. **No provider-routing configuration appears anywhere in the committed
   `.github/` or `scripts/` trees.** A search for
   `CLAUDE_CODE_USE_BEDROCK|CLAUDE_CODE_USE_VERTEX|CLAUDE_CODE_USE_FOUNDRY|
   ANTHROPIC_BEDROCK|ANTHROPIC_VERTEX|AWS_REGION|GOOGLE_CLOUD_PROJECT|
   AZURE_OPENAI|ANTHROPIC_BASE_URL|ANTHROPIC_API_URL|ANTHROPIC_AUTH_TOKEN`
   returns **no match** in either tree.

**Why this is NECESSARY BUT NOT SUFFICIENT, stated rather than glossed:**
`env -i` preserves **`HOME`**, so `$HOME/.claude/settings.json` on the runner
remains readable by the CLI; administrator-managed (policy) settings are read
from system paths that `env -i` does not touch and `--safe-mode` does not
disable; and the runner image itself is not described by the committed tree.
**A static read of the repository cannot close the plane question. Only a
runtime read-back can.**

### 3.3 R5's four MUST items — status and read-back location

R5: *"The Operator record MUST therefore EVIDENCE the plane by READ-BACK rather
than assert it, capturing all of:"*

| # | R5 requirement | Status | Where it is read back |
| --- | --- | --- | --- |
| **R5-a** | provider-selection environment and configuration that would route Claude Code to Bedrock, Vertex or Foundry, shown **UNSET or absent** | **EVIDENCED** | **EVIDENCED (EXE-1).** Runtime read-back captured by the provider-plane print-back step (xFactory #196) inside the seat's own `env -i` subshell — opensoft/xFactory run 33577170272 (https://github.com/opensoft/xFactory/actions/runs/33577170272), council-deliberation-worker `smoke-seat` (`smoke=true`), dispatched from main at `1db16177`, conclusion SUCCESS, runner `xfactory-artifact-cpc-brett01` (group `xfactory-artifact-workers`, host `CPC-brett-TUBV0`, service account `svc-omniworker`), capture `printback.runner.utc=2026-09-02T00:53:46Z` (the Operator's decision date 2026-09-01 stands). Provider-routing environment, all UNSET/absent: `CLAUDE_CODE_USE_BEDROCK=<unset>, CLAUDE_CODE_USE_VERTEX=<unset>, CLAUDE_CODE_USE_FOUNDRY=<unset>, CLAUDE_CODE_SKIP_BEDROCK_AUTH=<unset>, CLAUDE_CODE_SKIP_VERTEX_AUTH=<unset>, ANTHROPIC_BASE_URL=<unset>, ANTHROPIC_BEDROCK_BASE_URL=<unset>, ANTHROPIC_VERTEX_BASE_URL=<unset>, ANTHROPIC_VERTEX_PROJECT_ID=<unset>, CLOUD_ML_REGION=<unset>, ANTHROPIC_FOUNDRY_BASE_URL=<unset>, ANTHROPIC_FOUNDRY_RESOURCE=<unset>, AWS_REGION=<unset>, AWS_PROFILE=<unset>, ANTHROPIC_MODEL=<unset>, ANTHROPIC_DEFAULT_OPUS_MODEL=<unset>, ANTHROPIC_DEFAULT_SONNET_MODEL=<unset>, ANTHROPIC_DEFAULT_HAIKU_MODEL=<unset>, ANTHROPIC_SMALL_FAST_MODEL=<unset>, ANTHROPIC_CUSTOM_HEADERS=set:no, CLAUDE_CODE_MAX_OUTPUT_TOKENS=<unset>, DISABLE_TELEMETRY=<unset>, HTTP_PROXY=set:no, HTTPS_PROXY=set:no, NO_PROXY=set:no, CLAUDE_CODE_OAUTH_TOKEN=set:yes, ANTHROPIC_API_KEY=set:no, ANTHROPIC_AUTH_TOKEN=set:no`. Resolved configuration surfaces (existence/size/mtime only, contents never read by design): user_settings PRESENT `/c/Users/svc-omniworker/.claude/settings.json` size=79 mtime=2026-07-10; user_settings_local ABSENT; user_claude_json PRESENT `/c/Users/svc-omniworker/.claude.json` size=37474 mtime=2026-08-10; config_dir_settings ABSENT (the seat's `CLAUDE_CONFIG_DIR` is a fresh `RUNNER_TEMP` dir); managed_windows ABSENT `C:\ProgramData\ClaudeCode\managed-settings.json`; managed_gitbash ABSENT; managed_posix ABSENT `/etc/claude-code/managed-settings.json`; workspace_settings ABSENT. CLI: `printback.cli.path=/c/Users/svc-omniworker/.local/bin/claude`, `printback.cli.version=2.1.206 (Claude Code)`. `claude config list`: `list_bytes=308, list_status=ok, keys=<no keys parsed>` (the listing's shape yielded no key names to the parser — recorded as-is, not as "no config"). **Note (c):** managed/policy settings — the surface §3.2 said a static read could not close — are ABSENT at all three probed paths. **Note (b):** a 79-byte `~/.claude/settings.json` exists under `svc-omniworker` (mtime 2026-07-10); its contents were deliberately not read by the print-back, and since the seat's effective config dir is the fresh `RUNNER_TEMP` dir, this file is not the resolved config surface for the seat — the Operator may inspect its 79 bytes out-of-band if desired. |
| **R5-b** | base-URL and endpoint configuration, **resolving to the direct Anthropic API** | **EVIDENCED** | **EVIDENCED (EXE-2).** Endpoint print-back from the same run (xFactory #196, run 33577170272, capture `printback.runner.utc=2026-09-02T00:53:46Z`): `printback.invocation.model_arg=opus` (smoke path; the real deliberation seats pass agent-mixes' exact pins), `printback.invocation.config_dir=C:\actions-runner-artifact\_work\_temp/claude-cfg`, `printback.api_version=<not exposed by CLI; negotiated per request>`, `printback.endpoint.routing_names_set=0`, `printback.endpoint.resolution=default-direct-anthropic-api`, `printback.status=complete` (read-only; no credential value printed). **Honesty note (a):** `default-direct-anthropic-api` is a statement about CONFIGURATION read back at run time in the seat's environment (every routing name unset), not a capture of the outbound request — the CLI exposes neither a resolved-endpoint command nor its negotiated API version. **Corroborating inference (d):** the same lane's earlier smoke (run 33513966619) authenticated successfully with an `sk-ant-oat*` token, which only the direct Anthropic plane accepts. |
| **R5-c** | Anthropic's opt-in server-side **`fallbacks` beta, asserted UNSET** | **ACCOUNT-LEVEL ABSENCE EVIDENCED (EXE-3); REQUEST-SIDE RESTS ON WORKFLOW TEXT** | **EVIDENCED (EXE-3)** — see §8.1. This is a request/account-level beta, **not an environment variable**, so `env -i` does not bear on it and no repository search alone could settle it. Read back at claude.ai's account and organization settings (swept 2026-09-01: no fallback setting exists on either surface) and at the request configuration (the worker's CLI invocation carries no fallback flag or beta header, though the CLI's internal request construction is not operator-inspectable from the workflow). R5: its absence is *"captured, never assumed"* — captured here from a named sweep, not assumed. |
| **R5-d** | **Claude Code version** and the **credential-binding reference** | **VERSION EVIDENCED; BINDING IDENTIFIED, LIVE MODE EVIDENCED (EXE-4, 2026-09-01)** | version: §4. binding: §3.4. |

### 3.4 The credential-binding reference — identified, mode EVIDENCED (EXE-4)

The worker fetches the model-provider token **by reference** before the seats
run. Two modes are committed, and which one is live is repository/organization
configuration the drafter cannot read:

* **Bound mode.** `vars.WORKER_CREDENTIALS_CLIENT_ID`,
  `vars.WORKER_CREDENTIALS_SECRET_URI` and `vars.HERMES_AZURE_TENANT_ID` are
  set; the step exchanges a GitHub Actions OIDC assertion at
  `login.microsoftonline.com/{tenant}/oauth2/v2.0/token` for a
  `https://vault.azure.net/.default`-scoped token, reads the secret at
  `WC_SECRET_URI` (`api-version=7.4`), and exports it as
  `CLAUDE_CODE_OAUTH_TOKEN`. Log line: *"token source: vault (by reference;
  rotation is a vault write)"*.
* **Degraded mode.** The bindings are unset; the step exits 0 with
  *"token source: degraded (service env) — worker-credentials bindings
  unset."* and the token comes from the service environment.

> **EVIDENCED (EXE-4).** Bound mode confirmed live: `token source: vault (by
> reference; rotation is a vault write)`, recorded in xFactory run 33513966619,
> 2026-09-01. Token shape `sk-ant-oat*` (setup-token OAuth), length 108; no
> on-disk credential persisted. See §8.1 EXE-4 for the full read-back
> (tenant, client ID, secret URI, all by reference).

### 3.5 The remaining execution-identity fields

| Template field | Status |
| --- | --- |
| Provider surface | **EVIDENCED (EXE-1/EXE-2)**: direct Anthropic API plane, claude.ai Business seat identity (EXE-5) |
| Account or tenant reference | **EVIDENCED (EXE-5)** — Operator read-back at claude.ai, 2026-09-01: account `xFactor-001@opensoft.one`; organization **Opensoft**; Organization ID `9a5409fe-5115-47e5-8bad-ad64c455c7c1`; plan: Business premium seat plan. See §8.1. |
| Project or subscription reference | **n/a — confirmed (EXE-5)**: the identity is a claude.ai Business organization seat, with no project axis on that plane |
| Region or location | **n/a — confirmed (EXE-5)**: the identity is a claude.ai Business organization seat, with no region axis on that plane |
| Endpoint | **EVIDENCED (EXE-2)**: default direct Anthropic API — no base-URL override in the seat's environment (configuration read-back; see note a) |
| Deployment or profile identifier | **n/a on the direct Anthropic plane** — this row is where a Bedrock inference profile or a Foundry deployment name would go, and its emptiness is a *consequence* of the plane finding, not evidence for it |
| API version | **EVIDENCED-AS-UNEXPOSED (EXE-2)** — not exposed by the CLI; negotiated per request (EXE-2 capture line quoted at §8.1) |
| Authentication binding reference | **EVIDENCED** (EXE-4) — see §8.1 EXE-4 |

---

## 4. Execution identity — the transport, EVIDENCED

| Field | Value | Evidence |
| --- | --- | --- |
| Claude Code version | **2.1.251** | `claude --version`, recorded at the start of all three soak runs; unchanged across runs 1, 2 and 3 |
| Invocation flags | `--tools "" --max-turns 4 --max-budget-usd 12 --no-session-persistence --no-chrome --safe-mode --output-format json --json-schema "$SCHEMA"` | byte-identical to the worker's seat step; `--max-budget-usd` read from the builder's `limits`, not restated |
| Declared model | the exact identifier, never an alias | `--model claude-opus-5` / `--model claude-sonnet-5` in 80 of 80 |
| Read-back mechanism | the `modelUsage` map in the `--output-format json` envelope | transcribed verbatim per judgment |
| Runtime | operator workstation, Linux 6.6.87.2-microsoft-standard-WSL2, Python 3.12.3 | **NOT `xfactory-artifact-workers`** — §3.1 |

**A version note the Operator must resolve:** the 2026-08-22 corpus ran CLI
**2.1.239**; every soak row cited by the activation ruling ran **2.1.251**.

> **EVIDENCED (EXE-6).** CLI version resolved in the worker: **2.1.206**
> (`claude --version`) on the artifact lane, xFactory run 33513966619,
> 2026-09-01. **Version-skew note:** the same day's coding lane resolved
> **2.1.207** — a skew between the two lane service accounts on the same
> host. Neither equals the soak's workstation 2.1.251. See §8.1 EXE-6.

---

## 5. Linkage — reference relationships, not composition binding

The template is explicit that this row *"is a reference relationship, not a
claim that the execution tuple is composition-bound."*

| Linkage | Reference | State |
| --- | --- | --- |
| Council selection record | `hermes/domain/review-councils/records/2026-08-29-gate-rules-s5-seat-model-selection.md` | landed |
| Roster-change record | `records/2026-08-31-enrolled-roster-model-pin-flip.md` | landed |
| Soak record — run 1 | `records/2026-08-31-s5-seat-model-soak-results.md` | landed |
| Soak record — run 2 | `records/2026-08-31-s5-seat-model-soak-run2.md` (evidence at `records/2026-08-31-s5-soak-run2-evidence/`) | landed, `5def29ac` |
| Soak record — run 3 (LA-C3 completion) | `hermes/domain/review-councils/records/2026-09-01-s5-seat-model-soak-run3.md` (evidence at `records/2026-09-01-s5-soak-run3-evidence/`) | landed, `fd4319aa` |
| Activation ruling | landing in **#155** | **LANDED.** codexFactory PR #155 merged, commit `fd4319aa` (2026-08-31T16:33:18Z), title "Record the S5 soak run 3: the LA-C3 completion round — 5 of 6, the C9 inverse clean, DA-3's question routed to #154"; record `hermes/domain/review-councils/records/2026-09-01-s5-seat-model-soak-run3.md`; the ruling itself sits at §12/§12.1 ("THE ACTIVATION RULING") of that record |
| Proposed composition digest | `agent-mixes.yaml` `rendered_set_digest` `sha256:751e03a203fd5cef59f0e4873fc910ef6c2c501e60472ea54791ad77fda7c92a`, recomputed and matched at `8c1ec5c6` and `5def29ac` | evidenced |
| Proposed issuance / grant reference | openxFactory `governance/review-authority/` — a **permanently human-only surface** | **PENDING** — the register act, which cites this record; no soak and no drafter reaches it |

---

## 6. Ratification-time and execution-time evidence

| Template row | Content |
| --- | --- |
| Provider documentation capture | **EVIDENCED (SEM-1)**, 2026-09-01 |
| Console or API read-back of configured execution identity | **EVIDENCED (EXE-1, EXE-2, EXE-3, EXE-5)** |
| Lifecycle check | survey rows at §2.1 evidenced; **first-party re-confirmation EVIDENCED (SEM-1)**, 2026-09-01 |
| Authorization and eligibility check | **EVIDENCED (EXE-4, EXE-5)** |
| Operator signature | **SIGNED 2026-09-01 — §8** |
| Request time | 2026-08-31, three runs; per-judgment windows recorded to the second in each run header |
| Declared and observed model fields | **EVIDENCED — 80 of 80, §2.3** |
| Deployment or profile fields | **n/a on the direct Anthropic plane**, subject to §3 |
| Response or job ID | each envelope's `session_id` and `uuid`, retained per judgment |
| Endpoint or region evidence | **EVIDENCED (EXE-2)**, 2026-09-02Z |
| Substitution or failure result | **EVIDENCED: no substitution in 80 of 80.** `is_error: false` on every judgment; zero floor refusals; zero schema failures |

---

## 7. Limits and fail-closed — carried verbatim from the template

**Limits.** *"Exact ID is not a cryptographic digest of served behavior and does
not freeze routing, safety, infrastructure, fallback, region, or output."* And
from the register: Anthropic's published guarantee covers **weights and
configuration under a model ID**, while serving infrastructure *"can change over
time"*. **No reviewed provider documentation supplies a universal cryptographic
digest for the served model artifact**, and the 80 read-backs above are
provider-reported fields, not attestations.

**Fail-closed.** *"Missing exact ID, missing required execution field, stale
lifecycle evidence, undocumented substitution, fallback, alias expansion, or
mismatched evidence refuses governed issuance or activation."*

**R5's plane fail-closed, quoted because it governs the signature:**

> FAIL CLOSED on mismatch. If the read-back shows a partner plane, the record
> REFUSES governed issuance and activation. It does NOT fall through to the
> partner-plane hazard tables and proceed under them: a plane change is a NEW
> Operator record and, per R6, a COMPOSITION change.

**AS SIGNED, THE FAIL-CLOSED CRITERION IS MET:** no required
execution field remains PENDING (EXE-1 through EXE-6 all EVIDENCED) and no
semantic field remains PENDING (SEM-1 EVIDENCED). **This record, signed with every required field EVIDENCED and the plane read back as the DIRECT ANTHROPIC plane, evidences the plane for the register act. It does not itself perform issuance or activation — the register act does, citing this record; a partner-plane read-back at any later verification refuses issuance and activation and requires a new Operator record.** The partner-plane hazard tables
**are** disapplied for this record, because R5 disapplies them exactly when the
plane is EVIDENCED direct-Anthropic — which §3.5 now records by read-back. A
later partner-plane read-back does not re-apply them: per R5's fail-closed
rule quoted above it REFUSES issuance and activation and requires a new
Operator record.

---

## 8. Operator verification acts and signature

The Operator performs each act below, records its result **in this record**, and
only then signs. Any act returning a partner plane triggers §7's refusal.

| ID | Act | Where it is read back | Result |
| --- | --- | --- | --- |
| **SEM-1** | Capture Anthropic's first-party documentation for both pins: URL, access date, lifecycle rows | Anthropic model documentation | **EVIDENCED** — Operator access 2026-09-01, confirmed the lines on screen. Docs domain moved: `docs.anthropic.com` now 301-redirects to `platform.claude.com`; live URLs recorded: (1) `platform.claude.com/docs/en/about-claude/model-deprecations` — "Model status" table: `claude-opus-5 \| Active \| N/A \| Not sooner than July 24, 2027`; `claude-sonnet-5 \| Active \| N/A \| Not sooner than June 30, 2027`; "Notifications": *"at least 60 days' notice before model retirement for publicly released models."* (2) `platform.claude.com/docs/en/docs/about-claude/models/overview` — "Compare models" table, Retirement row: same two dates; Claude API ID row: `claude-opus-5`, `claude-sonnet-5`; footnote: *"Every Claude model ID is a pinned snapshot, including the dateless IDs used from the 4.6 generation on."* (3) `platform.claude.com/docs/en/about-claude/models/model-ids-and-versions` — "Dateless IDs are pinned snapshots": *"Anthropic does not update the weights or configuration of an existing model ID. When an updated version is available, it ships under a new model ID."*; "Model weights versus serving infrastructure": *"Model weights are fixed for a given ID, but the serving infrastructure around the model can change over time."* All three lifecycle facts §2.1 carries are CONFIRMED unchanged by these first-party pages. See §2.2. |
| **EXE-1** | Print the seat step's effective environment and resolved CLI configuration inside `env -i`, incl. `$HOME/.claude/settings.json` and managed settings | the seat's own env -i shape via the provider-plane print-back step (xFactory #196), smoke path | **EVIDENCED** — opensoft/xFactory run 33577170272 (https://github.com/opensoft/xFactory/actions/runs/33577170272), council-deliberation-worker `smoke-seat` (`smoke=true`), dispatched from main at `1db16177` (which merged PR #196, "Provider-plane print-back (EXE-1/EXE-2)" — byte-identical in the `deliberate` and `smoke-seat` jobs, run inside the seat invocation's own `env -i` allowlist shape), conclusion SUCCESS, runner `xfactory-artifact-cpc-brett01` (group `xfactory-artifact-workers`, host `CPC-brett-TUBV0`, service account `svc-omniworker`), capture `printback.runner.utc=2026-09-02T00:53:46Z`. Provider-routing environment inside the seat's `env -i`, all UNSET/absent: `CLAUDE_CODE_USE_BEDROCK=<unset>, CLAUDE_CODE_USE_VERTEX=<unset>, CLAUDE_CODE_USE_FOUNDRY=<unset>, CLAUDE_CODE_SKIP_BEDROCK_AUTH=<unset>, CLAUDE_CODE_SKIP_VERTEX_AUTH=<unset>, ANTHROPIC_BASE_URL=<unset>, ANTHROPIC_BEDROCK_BASE_URL=<unset>, ANTHROPIC_VERTEX_BASE_URL=<unset>, ANTHROPIC_VERTEX_PROJECT_ID=<unset>, CLOUD_ML_REGION=<unset>, ANTHROPIC_FOUNDRY_BASE_URL=<unset>, ANTHROPIC_FOUNDRY_RESOURCE=<unset>, AWS_REGION=<unset>, AWS_PROFILE=<unset>, ANTHROPIC_MODEL=<unset>, ANTHROPIC_DEFAULT_OPUS_MODEL=<unset>, ANTHROPIC_DEFAULT_SONNET_MODEL=<unset>, ANTHROPIC_DEFAULT_HAIKU_MODEL=<unset>, ANTHROPIC_SMALL_FAST_MODEL=<unset>, ANTHROPIC_CUSTOM_HEADERS=set:no, CLAUDE_CODE_MAX_OUTPUT_TOKENS=<unset>, DISABLE_TELEMETRY=<unset>, HTTP_PROXY=set:no, HTTPS_PROXY=set:no, NO_PROXY=set:no, CLAUDE_CODE_OAUTH_TOKEN=set:yes, ANTHROPIC_API_KEY=set:no, ANTHROPIC_AUTH_TOKEN=set:no`. Resolved configuration surfaces (existence/size/mtime only, contents never read by design): user_settings PRESENT `/c/Users/svc-omniworker/.claude/settings.json` size=79 mtime=2026-07-10; user_settings_local ABSENT; user_claude_json PRESENT `/c/Users/svc-omniworker/.claude.json` size=37474 mtime=2026-08-10; config_dir_settings ABSENT (the seat's `CLAUDE_CONFIG_DIR` is a fresh `RUNNER_TEMP` dir); managed_windows ABSENT `C:\ProgramData\ClaudeCode\managed-settings.json`; managed_gitbash ABSENT; managed_posix ABSENT `/etc/claude-code/managed-settings.json`; workspace_settings ABSENT. CLI: `printback.cli.path=/c/Users/svc-omniworker/.local/bin/claude`, `printback.cli.version=2.1.206 (Claude Code)`. `claude config list`: `list_bytes=308, list_status=ok, keys=<no keys parsed>` (the listing's shape yielded no key names to the parser — recorded as-is, not as "no config"). Managed/policy settings — the surface §3.2 said a static read could not close — are ABSENT at all three probed paths. A 79-byte `~/.claude/settings.json` exists under `svc-omniworker` (mtime 2026-07-10); its contents were deliberately not read by the print-back, and since the seat's effective config dir is the fresh `RUNNER_TEMP` dir, this file is not the resolved config surface for the seat — the Operator may inspect its 79 bytes out-of-band if desired. See §3.3 R5-a. |
| **EXE-2** | Record the resolved base URL / endpoint and API version | the seat's own env -i shape via the provider-plane print-back step (xFactory #196), smoke path | **EVIDENCED** — same run (opensoft/xFactory 33577170272, capture `printback.runner.utc=2026-09-02T00:53:46Z`): `printback.invocation.model_arg=opus` (smoke path; the real deliberation seats pass agent-mixes' exact pins), `printback.invocation.config_dir=C:\actions-runner-artifact\_work\_temp/claude-cfg`, `printback.api_version=<not exposed by CLI; negotiated per request>`, `printback.endpoint.routing_names_set=0`, `printback.endpoint.resolution=default-direct-anthropic-api`, `printback.status=complete` (read-only; no credential value printed). Honesty note: `default-direct-anthropic-api` is a statement about CONFIGURATION read back at run time in the seat's environment (every routing name unset), not a capture of the outbound request — the CLI exposes neither a resolved-endpoint command nor its negotiated API version. Corroborating inference already on record: the same lane's earlier smoke (run 33513966619) authenticated successfully with an `sk-ant-oat*` token, which only the direct Anthropic plane accepts. See §3.3 R5-b. |
| **EXE-3** | Assert the server-side `fallbacks` beta UNSET | Anthropic account/organization settings + request configuration | **EVIDENCED** — Operator sweep at claude.ai, 2026-09-01, of BOTH the user profile settings for `xFactor-001@opensoft.one` AND the Opensoft organization/admin pages: no setting named fallback / fallbacks / model fallback exists anywhere on either surface; the model is selected at use time. This absence was CAPTURED from a named sweep of both surfaces, not assumed. Request-configuration half: the worker's invocation surface is the Claude Code CLI (`claude -p --model ...`, see xFactory `council-deliberation-worker.yml` smoke-seat above at EXE-4/EXE-6; deliberation seats use agent-mixes exact pins) with no fallback flag or beta header configured anywhere in the workflow text. Stated honestly: the CLI's internal request construction is not operator-inspectable from the workflow, so the request-side half of this assertion rests on the workflow text plus the account-level absence just captured, not on a direct read of the outbound request. |
| **EXE-4** | State the live credential-binding mode; if bound, record tenant/client/secret URI **by reference** | Actions *variables* config + the `token source:` notice | **EVIDENCED** — opensoft/xFactory run 33513966619 (https://github.com/opensoft/xFactory/actions/runs/33513966619), council-deliberation-worker smoke-seat (`smoke=true`, one synthetic seat invocation, no claim, no Hermes call), dispatched 2026-09-01T13:32:07Z by brettheap, conclusion SUCCESS, on runner `xfactory-artifact-cpc-brett01` (group `xfactory-artifact-workers`, host `CPC-brett-TUBV0`, service account `svc-omniworker`) — the FIRST live run of the worker's model invocation on the CPC, dispatched via the xFactory copy under the 2026-09-01 clearing-boundary ruling (the codexFactory-path attempt was cancelled unclaimable). **Bound mode**, verbatim at 13:32:16Z: `##[notice]token source: vault (by reference; rotation is a vault write)`. `WC_CLIENT_ID=ad24a6f1-282d-4dea-b2a8-be7a4d5e1fd1`, secret URI `https://kv-opensoft-xfactory-qa.vault.azure.net/secrets/xfactor-001-claude-setup-token`, fetched via OIDC federated credential to a vault-scoped token to the secret, delivered to the invocation only as `CLAUDE_CODE_OAUTH_TOKEN` env (masked). Token shape check: `token length: 108`, `token shape: sk-ant-oat* (setup-token OAuth)` — the correct subscription-auth kind, not an API key. On-disk credential state: `/c/Users/svc-omniworker/.claude/.credentials.json` ABSENT (no persisted credential); `/c/Users/svc-omniworker/.claude.json` present (config only, mtime 2026-08-10, 37474 bytes); `CLAUDE_CONFIG_DIR` unset in the service env, pointed at `RUNNER_TEMP/claude-cfg` for the invocation. |
| **EXE-5** | Record the Anthropic account/organization the token authenticates | claude.ai (the subscription plane — the CPC token is `sk-ant-oat*`, minted by `claude setup-token`; console.anthropic.com is the API-key plane and is NOT this token's identity surface) | **EVIDENCED** — Operator read-back at claude.ai, 2026-09-01: account `xFactor-001@opensoft.one`; organization **Opensoft**; Organization ID `9a5409fe-5115-47e5-8bad-ad64c455c7c1`; plan: Business premium seat plan. Project/subscription and region/location resolve n/a — confirmed: the identity is a claude.ai Business organization seat, with no project/region axis on that plane (§3.5). |
| **EXE-6** | Record the CLI version resolved **in the worker** | the same convening's log | **EVIDENCED** — same run (opensoft/xFactory 33513966619, council-deliberation-worker smoke-seat, 2026-09-01T13:32:07Z, runner `xfactory-artifact-cpc-brett01`, service account `svc-omniworker`): `claude` resolves to `/c/Users/svc-omniworker/.local/bin/claude`, `claude --version` returns `2.1.206 (Claude Code)`. Invocation exercised for real: `claude -p --model opus` against the synthetic packet returned `SMOKE OK: lead-quality ready` (structured output validated against the seat schema). **Version-skew note:** the same day's readiness-diagnostic (clearing-dispatch run 33512287539, ledger `cd-33512287539-1`) shows the artifact lane at `claude 2.1.206` (consistent with this run) but the CODING lane at `claude 2.1.207` — a version skew between the two lane service accounts (`svc-omniworker` vs `svc-omnicoder`) on the same host `CPC-brett-TUBV0`, worth carrying wherever this record's version-pinning/fallback discussion (§4) is read. |

### 8.1 Log-harvest attempt, 2026-08-31 — result: nothing to harvest, plus two worker gaps

Performed against the real `opensoft/codexFactory` repository (not the soak's
workstation-direct route), scoped to
`.github/workflows/council-deliberation-worker.yml`, current tree at `fd4319a`
(`origin/main`, which contains both `6edecaf1` the roster flip and `8c1ec5c6`
the packet-absence hardening). **This is a read-only harvest — no workflow
file was changed and no run was triggered.**

**Finding 1 — no qualifying run exists.** `gh run list --workflow
council-deliberation-worker.yml` shows **855 total runs**. Every run's `claim`
job calls the claim action against the live Hermes runtime; the `deliberate`
job (which contains the credential-fetch step, the `token source:` notice,
and every seat's `env -i … claude -p --model "$MODEL" …` invocation) runs
`if: needs.claim.outputs.claimed == 'true'`, and `claimed` was `false` in
every sampled run. Runs inspected directly: **33415162394** (commit
`fd4319a`, 2026-08-31T16:37:47Z), **33410101077** and **33406799845**
(commit `5def29ac`, 2026-08-31T15:43Z / 15:09Z), **33404051184** (commit
`8c1ec5c6`, 2026-08-31T14:40:48Z) — in each, `gh run view` shows `deliberate
in 0s` (skipped). A full-history duration scan (all 855 runs, via the REST
API's `run_started_at`/`updated_at`) found a **maximum run duration of 41
seconds** anywhere in the history — too short for the checkout, venv install,
Azure OIDC exchange and parallel `claude -p` calls the `deliberate` job would
require, corroborating that it has never actually executed. The workflow's
own committed comment (line ~772,
`council-deliberation-worker.yml`) independently states: *"NOT ONE
COMMISSIONED SOAK HAS RUN and no row exists (2026-08-29 §8.18)."* The single
`workflow_dispatch` run in the entire 855-run history, **33381257642**
(dispatched 2026-08-31T10:11:20Z with `smoke: true`, the one path that would
exercise a real credentialed seat invocation), has its `smoke-seat` job stuck
`queued` for 6+ hours with no runner ever assigned (the repo's registered-runner
list is empty) — even the smoke path has never completed. **Consequence:**
none of EXE-1, EXE-2, EXE-4, EXE-6 has a run log to read, because every log
line the harvest was asked to look for lives inside a job step that has never
executed.

**Finding 2 — two of the four items would stay unharvestable even from a
completed run, without a worker change (FLAG, no change made):**

* **EXE-1.** No `printenv`/environment-dump step, and no read of
  `$HOME/.claude/settings.json` or any managed/policy settings path, appears
  anywhere in `council-deliberation-worker.yml` (verified by grep across the
  whole file). A worker change adding an explicit environment/config
  print-back step inside the `env -i` subshell would be required to make this
  harvestable from a log.
* **EXE-2.** The only base-URL value the workflow ever prints or reads is
  `vars.HERMES_QA_BASE_URL` — the Hermes application endpoint, not the
  Anthropic API. No `ANTHROPIC_BASE_URL`, resolved API version, or any
  Anthropic-endpoint value is read or printed anywhere in the file. A worker
  change adding a step that prints the CLI's resolved base URL and API
  version would be required.

[Note, 2026-09-02: the clearing lane's readiness print-backs captured CLI
path/version only (EXE-6 corroboration); EXE-1/EXE-2 were evidenced by the
worker's own print-back step (xFactory #196), run 33577170272.]

**EXE-4 is different in kind — no worker change needed, just an actual run.**
The `token source: vault (by reference; rotation is a vault write)` /
`token source: degraded (service env) — worker-credentials bindings unset.`
notices are already coded into the credential-fetch step (lines ~230–262 of
`council-deliberation-worker.yml`, duplicated at ~1244–1275 for the
`smoke-seat` job) and would print as soon as that step runs; it has simply
never run. Likewise **EXE-6** needs no worker change beyond adding the
missing `claude --version` step noted above — the CLI is already invoked in
the job, it is only never asked to report its own version.

**EXE-3, EXE-5, SEM-1** were outside this 2026-08-31 repository harvest's
scope (console/docs items) and were harvested separately, 2026-09-01, by
Operator read-back — see the SEM-1, EXE-3 and EXE-5 rows above.

**Signature — Operator**

    I have performed each verification act above, recorded its result in this
    record, and read the results as evidencing the DIRECT ANTHROPIC plane. I
    understand that a partner-plane read-back refuses governed issuance and
    activation and requires a new Operator record.

    Operator: Brett Heap
    Signature: Brett Heap — signed in-session by dictation, verbatim word: "signed, date 2026-09-01" (recorded by the session)
    Date:      2026-09-01

**Signed by the Operator 2026-09-01 (in-session, dictated verbatim). Verification acts performed and recorded above. Not yet committed to a governed repository — the register act carries this record to its human-only surface (§5).**

---

## Addendum 2026-09-02 — Operator ruling: the version of record

**APPENDED, NOT EDITED. Nothing above this line was changed by a single byte.**
This record was SIGNED by the Operator on 2026-09-01 and a signed record is not
revised; a later act that resolves something it left open appends beneath the
signature and says so. The file above this heading is byte-identical to the
signed original (verified by digest at the time of the copy).

### The ruling, verbatim

> **"2.1.206 is the version of record"**
> — Brett Heap, Operator, in session, 2026-09-02

### What it resolves — §4's open note

§4 of this record carries, in terms, **"A version note the Operator must
resolve"**: the 2026-08-22 corpus ran CLI **2.1.239**; every soak row cited by
the activation ruling ran **2.1.251**; and the worker's own read-back (EXE-6)
resolved **2.1.206**. Three numbers, one seat family, and no rule saying which
one the seats are governed by. **That note is now resolved, and this is the
resolution:**

* **THE VERSION OF RECORD FOR THE SEATS IS THE WORKER-RESOLVED `2.1.206`.**
  Evidence: **EXE-6**, `claude --version` resolved **inside the worker**, on the
  **artifact lane**, under the service account **`svc-omniworker`**, xFactory run
  **33513966619**, 2026-09-01. It is the version of record because it is the
  version that **executes a seat** — the transport the governed lane actually
  runs, read back from inside it rather than asserted about it.
* **THE WORKSTATION SOAK'S `2.1.251` IS THE DRAFTER'S TRANSPORT, AND IT REMAINS
  ON RECORD AS THE SINGLE NAMED DEVIATION.** §3.1 of this record already says
  what it is: the drafter's runs executed on an operator workstation, **NOT** on
  `xfactory-artifact-workers`, and §3.1 is retained above precisely so the
  deviation stays legible. The ruling does not retire that disclosure and does
  not convert the soak rows into worker rows; it says that the number those rows
  carry is **not the version of record**.
* **THE 2026-08-22 CORPUS'S `2.1.239` IS LIKEWISE NOT THE VERSION OF RECORD.**
  It is the transport of an earlier corpus, recorded as history.
* **THE CODING LANE'S `2.1.207` SKEW IS CARRIED, NOT ERASED.** §8 EXE-6 records
  it: the same host's two lane service accounts resolved **2.1.206** (artifact)
  and **2.1.207** (coding) on the same day. The ruling names the artifact lane's
  number as the version of record; **the skew between the two lane service
  accounts stays on the record exactly as EXE-6 states it**, because a version
  of record that quietly absorbed a measured disagreement would be an assertion
  rather than a read-back.

**WHAT THIS RULING IS NOT.** It is not a pin. Nothing in this estate reads a CLI
version and refuses on it, the runtime is **not** one of the six declared
composition components (`docs/governed-reissuance-runbook.md` §0.2), and naming
a version of record neither adds a seventh component nor makes a reseed a
composition bump. It resolves an ambiguity in this record; it enforces nothing.

### This commit is this record's first governed home

Until this commit the record existed only as a **scratchpad copy** — its own
header says so, and that sentence is left standing above because it is part of
the signed text and records what was true when it was signed. **It is superseded
by this commit and by nothing else.**

The record was carried here by **the register act of 2026-09-02**, whose walk
record is
[`walk-2026-09-02-register-act.md`](walk-2026-09-02-register-act.md). That act
cites this record as the **third of its three citations** (the activation ruling
at codexFactory `records/2026-09-01-s5-seat-model-soak-run3.md` §12.1, the
roster-change record `records/2026-08-31-enrolled-roster-model-pin-flip.md`, and
this record), and R5's own closing sentence is why the carry had to happen
before the act rather than after it: *"until that record exists, governed
issuance and activation stay blocked."*

### §5's PENDING row is answered — and the row itself is not edited

§5's linkage table ends with **"Proposed issuance / grant reference"**, whose
state at signing was **PENDING** — *"the register act, which cites this record;
no soak and no drafter reaches it."*

**IT IS NOW ANSWERED: `grant-mrc-0002`**, at
`governance/review-authority/grants/grant-mrc-0002.yaml`, issued
`2026-09-02T13:33:48Z` by `Brett.Heap@opensoft.one`, expiring
`2027-06-30T00:00:00Z`, and backed by `row-mrc-0001` in
`governance/review-authority/register.yaml`, which was repointed onto it in the
same change. `grant-mrc-0001` was revoked for **DRIFT** at the same instant, on
the 2026-08-31 composition change.

**THE ROW IN §5 IS NOT EDITED.** It still reads PENDING, and it is correct that
it does: it records the state at the Operator's signature, which is the only
state a signed record may assert. The answer lives here, beneath the signature,
where a later fact belongs.
