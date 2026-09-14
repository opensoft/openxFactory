# Staged: Context Compression Runtime

Status: staged
Kind: architecture
Summary: Adopt Headroom (github.com/chopratejas/headroom, PyPI
`headroom`, evaluated at v0.32.0) as an optional context-compression
stage in the Omnigent worker lane — between the agent harness and the
LLM provider — cutting provider token spend 60–95% on tool output.
Headroom is worker-lane INFRASTRUCTURE, not a domain capability: it is
a pinned third-party dependency of the worker container (like the
Claude Code / Codex harnesses), never a submodule. Adoption requires
three policy positions this topic stages: (1) the worker-local CCR
reversible-compression store is RAM-only — headroom has NO PHI/PII
exclusion, so nothing it touches may persist on the worker host;
(2) sensitive-data exclusion is an UPSTREAM obligation enforced at the
Hermes/xFactory ingress boundary, never assumed of the compressor;
(3) audit is three-tier — Hermes envelope (ingress/authorization),
lane harness transcript (execution; holds all uncompressed originals,
joinable to compression markers by content hash), and an optional
per-domain egress-capture sidecar (disclosure accounting) that is also
the external enforcement point (NetworkPolicy: provider egress only
via the sidecar).
Topics: context-compression, headroom, ccr, omnigent-worker,
token-economics, audit-tiers, egress-capture, disclosure-accounting,
phi-handling, worker-lane-infrastructure, external-enforcement
Repository context: openxFactory (neutral capability + audit-tier
contract); Omnigent-Install (pilot wiring, worker profiles, sidecar
container); codexFactory (pilot lane); MedxFactory/LedgerxFactory
(tier-3 consumers when activated)
Staging ID: openxFactory:staging:context-compression-runtime
Source: Headroom evaluation session (2026-07-25/26, Brett Heap) —
source audit of the CCR store and PHI handling in the headroom
codebase reshaped the audit design from "durable CCR audit backend"
to "RAM-only cache + three-tier audit"; named positions ratified in
that session ("lets go with in memory only holding", "maybe we move
our audit to that level").
Target capabilities: ADDED `context-compression-runtime` (neutral
worker-lane capability: compression stage contract, RAM-only local
store rule, upstream-exclusion obligation, three-tier audit model,
egress-capture activation knob on the omnigent domain overlay /
worker profile)

## Target capability

A neutral contract making context compression a governed, per-lane
opt-in with a fixed safety envelope, so any DomainxFactory can turn it
on according to its data-sensitivity posture without re-deriving the
analysis. The contract owns four positions:

1. **Placement.** Compression is worker-lane infrastructure between
   the harness and the provider (proxy/wrap mode). It is configured by
   the worker profile, pinned by version in the container build, and
   invisible to the domain layer. It is NOT a submodule and NOT a
   domain capability.
2. **Local-store rule.** Any reversible-compression store on the
   worker host is RAM-only (in-memory backend, or SQLite on a
   tmpfs/emptyDir mount when multi-process resilience is needed).
   Worker-host disk persistence of compressed-content originals is
   prohibited; nothing depends on session-end cleanup.
3. **Upstream-exclusion obligation.** The compressor is assumed
   sensitive-data-blind. PHI/PII exclusion, redaction, or
   pseudonymization is enforced at the Hermes/xFactory ingress
   boundary (tier 1) before content enters the lane. Domains that
   cannot yet enforce it do not enable compression outside
   engineering-grade lanes.
4. **Three-tier audit.** Tier 1: Hermes-reviewed job envelope —
   what data and authority were admitted to the lane. Tier 2: lane
   harness transcript — full execution record including every
   uncompressed tool output, captured as job evidence. Tier 3
   (per-domain knob, default off): egress-capture sidecar — the exact
   bytes disclosed to the provider, for disclosure-accounting-grade
   domains.

## Evidence: headroom v0.32.0 source audit (2026-07-25)

Findings from reading the code (not the README), pinned at upstream
commit `4bd1214` (2026-07-25):

| Finding | Source | Consequence |
| --- | --- | --- |
| CCR retrieval key is `sha256(original)[:24]`, embedded LLM-visibly in the compressed block (`[... Retrieve more: hash=…]`) | `headroom/cache/compression_store.py`, `transforms/*.py` | Original↔compressed join is content-addressed and re-derivable from any retained original; tamper-evident for free |
| Stored entry holds `original_content` + `compressed_content` + `tool_name` + `tool_call_id` + strategy | `CompressionEntry` dataclass | The pair an auditor wants exists — but only inside the cache lifetime |
| Default store: SQLite at `workspace_dir()/ccr_store.db`, TTL 1800s, `max_entries=1000` LRU; `HEADROOM_CCR_BACKEND=memory` opts out of disk; `HEADROOM_CCR_SQLITE_PATH` relocates | `cache/backends/sqlite.py`, `compression_store.py` | Disk write exists ONLY for proxy-restart survival and multi-uvicorn-worker sharing — a session-scale correctness cache, not a ledger. RAM-only is a supported first-class mode |
| **No PHI/PII detection, exclusion, or redaction anywhere in the compression path** | full-tree search; only secret-regex redaction of retrieval LOG previews, and `tag_protector` (shields XML tags from compressors, detects nothing) | Exclusion must be upstream; CCR's disk default writes a second plaintext copy of whatever the lane saw — hence the RAM-only rule |
| `headroom_retrieve` round-trips and proactive Context Tracker expansions are handled inside the proxy — "the client never sees CCR tool calls" | `ccr/response_handler.py`, `ccr/context_tracker.py` | The harness transcript cannot show WHEN a full original was re-disclosed to the provider — the gap tier 3 exists to close |
| No production request log — Prometheus counters + a dev-only mitmproxy differential-capture harness | `proxy/server.py`, `capture/`, `wiki/network-diff-capture.md` | Egress evidence is our sidecar, not a headroom feature; their dev harness validates the mitmproxy-tee pattern |
| Compression output is not reproducible post hoc (learned TOIN state, config, version) | `cache/compression_feedback.py`, wiki | "Exact prompt reconstruction" audits need tier 3; information-content audits are satisfied by tier 2 |
| `headroom learn` mines sessions and writes corrections to local files; cross-agent memory subsystem | CLI, `memory/` | Collides with Hermes memory ownership — disabled in worker profiles unconditionally |
| Upstream provider URL is operator-pinnable | `proxy/server.py` (`_normalize_api_url`, operator-pinned upstreams) | The tier-3 sidecar chains in without forking headroom |

## Claims

1. **Compression is lane infrastructure, not domain content.** It
   carries no contracts, no domain interpretation, and no authority;
   it belongs in the worker container build + worker profile, at the
   same layer as the harness binaries. (Placement analysis,
   2026-07-25.)
2. **The reversibility cache and the audit ledger must be different
   stores.** The cache wants short retention on the worker host
   (PHI hygiene); the audit wants long retention under governance.
   Merging them (a "durable CCR audit backend") puts PHI on the wrong
   host under the wrong access model and duplicates evidence tier 2
   already holds. The content-addressed hash is what joins them.
3. **Tier 2 already holds every original.** In proxy/wrap mode the
   harness records full tool outputs BEFORE compression touches them;
   the transcript is a superset of everything disclosed. Recomputing
   `sha256(original)[:24]` over transcript content resolves any
   `hash=…` marker with no store at all — and a mismatch is evidence
   of tampering.
4. **Only disclosure accounting needs tier 3.** "What information
   could the provider have seen" is answered by tier 2. "Exactly
   which bytes left, and when" (Medx/Ledgerx grade) needs the egress
   tee — and making the sidecar the pod's only permitted provider
   egress (NetworkPolicy) turns capture from observation into
   enforcement: an uncaptured disclosure is a connection that cannot
   happen. Fail-closed where required; per-domain knob because for
   codexFactory it is pure cost.
5. **The sidecar preserves the worker permission constitution.** It
   is lane infrastructure in the credential path (like headroom
   itself), so worker `access_secrets: false` is unaffected; it
   redacts Authorization headers from captures (no raw credentials at
   rest) while capturing content verbatim — content is the point.

## Pilot posture (Omnigent-Install, codexFactory lane)

- Pinned `headroom` (PyPI, ==0.32.0) in the omnigent-worker image
  behind a build arg; activation via worker-profile block, wrap/proxy
  mode only.
- Mandatory env: `HEADROOM_CCR_BACKEND=memory`; `headroom learn`,
  cross-agent memory, and telemetry beacon disabled.
- Tier 3 NOT in pilot (no compliance driver in codexFactory); tiers
  1–2 are the existing envelope + evidence flows, unchanged.
- Pilot exit metric: measured token reduction on real lane traffic
  vs. compression latency and any retrieval-miss-driven quality
  regressions (proxy crash orphans markers → degraded answer, not a
  compliance event — acceptable).

## Idea notes (pre-document, non-documented)

None recorded at staging.

## Conflicts

No conflicts recorded.

## Open questions

1. **Contract home for the tier-3 knob** — omnigent domain overlay
   field, worker-profile field, or both (overlay declares the domain
   requirement, profile realizes it)?
2. **Sidecar implementation** — productionized mitmproxy (their dev
   pattern) vs. Envoy tap filter; SSE reassembly and capture-volume
   handling; where captures land in the audit plane and under which
   retention schedule per domain.
3. **Does the three-tier audit model deserve its own neutral spec**
   (it generalizes beyond compression to any lane middleware that
   transforms provider traffic) or does it ride inside
   `context-compression-runtime`?
4. **Upstream-exclusion mechanics** — pre-redaction/pseudonymization
   at the Hermes boundary vs. tagging sensitive spans for
   `tag_protector` passthrough; likely its own topic once Medx-grade
   lanes are in scope.
5. **Version-tracking cadence** — headroom moves fast (their
   changelog shows breaking config surface churn); who re-audits the
   safety-relevant surfaces (CCR backend default, learn/memory
   default-on drift, telemetry) on version bumps?

## Deferral with a named gate (recorded 2026-08-28)

**DEFERRED. The gate is the pilot, and the pilot is behind the worker chain.**
The design is locked (source audit of headroom v0.32.0, RAM-only CCR, the
three-tier audit model), and the exit change is gated on the codexFactory-lane
pilot in Omnigent-Install producing MEASURED savings. That pilot runs in the
omnigent-worker image on a governed worker host, so it sits behind the same
three acts the `worker-host-app` topic is deferred on, verified as of
2026-08-28: **Omnigent-Install PR #40** (phase 3 — enrollment-broker client,
leases, fail-closed floor; raised 2026-07-28, still OPEN), then OpsxFactory
`add-worker-enrollment-broker-service` **task 8.1** (Brett's hosting-target
gate) and **task 8.2** (Brett's deployment-credential gate), both unticked.
The proximate gate is therefore the pilot's measured savings; the reason no
one can schedule it is the chain above it.

**This deferral is a schedule, not a standing.** It changes no `Status:`, and
it does NOT stop the topic ageing in doc-health — see the same paragraph in
the `worker-host-app` topic for why no `deferred` state was invented to make
it stop.

## Exit path

Pilot evidence in Omnigent-Install (proof-harness scope, no canonical
policy) → OpenSpec change ADDING `context-compression-runtime`
(neutral capability + audit-tier contract + overlay/profile knob),
`code_surface: installs/omnigent-install`, realization gated on the
pilot lane running green with measured savings. Tier-3 sidecar spec
delta rides the same change or a follow-on, whichever open question 3
resolves to.
