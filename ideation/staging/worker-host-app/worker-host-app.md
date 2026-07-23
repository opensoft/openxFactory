# Staged: xFactory Worker Host App

Status: staged
Kind: architecture
Summary: An Intune-delivered application (Win32 package, SYSTEM context) that
converts a managed Windows machine into a governed Omnigent worker host by
reconciling a declarative `worker_host_manifest` — enabling WSL2 + a container
engine, creating sealed worker identities with escrow-at-birth, installing
runner services and durable heartbeat publishers, materializing credential
profiles from vaultrefs, and pre-pulling digest-pinned workBench containers
verified against bench manifests — replacing the hand-built pilot host state
whose failure cost the 2026-07-22/23 recovery. First consumer: the idle
Omni-001 Cloud PC, migrating the rider fleet off the operator's personal
machine.
Topics: worker-host-app, worker-host-manifest, bench-manifest, tech-benches,
intune, wsl, omnigent-install, opsxfactory, cloudpc, omni-001, heartbeat,
credential-escrow, dtn-candidate
Repository context: openxFactory (eventual neutral `worker-host-manifest` +
`bench-manifest` contracts; first-consumer drafts live in Omnigent-Install);
Omnigent-Install (app behavior, manifests, heartbeat integration);
OpsxFactory (Intune packaging, WSL enablement policy, assignment group);
bench sources + platform ACR pipeline (owner TBD, see open questions)
Staging ID: openxFactory:staging:worker-host-app
Source: `ideation/brainstorm/tech-stack-benches.md` (2026-07-23) organized
here per Brett Heap's build decision 2026-07-23 ("we need the app that will
be put onto the omni-001 by intune... get wsl running, install the
workBenches containers and setup with manifests"); motivating incident: the
2026-07-22/23 CPC recovery (session-loop publishers dead since 7-19,
unescrowed local passwords, stale scripts, seat lapse); prescription
precedent: `Omnigent-Install docs/runbooks/cloudpc-named-worker-licensing.md`
("installs are device-scoped Intune artifacts (SYSTEM context); nothing
depends on the seat holder's session").

## Target capability and delta

- ADDED (eventually neutral) `worker-host-manifest`: the declarative record
  of what a worker host runs — workers (runner identity, pool/group, labels,
  profiles + versions, heartbeat parameters), sealed identities, credential
  profile vaultrefs, bench inventory (ids + digests), substrate requirements
  (WSL distro, engine), policy version. First-consumer draft in
  Omnigent-Install; graduates via DTN once proven (clients-tree precedent).
- ADDED `bench-manifest` (`kind: xfactory_tech_bench`): bench id, image ref +
  digest, stack, tool inventory (name/version), capabilities, credential
  statement (tools-only, never credentialed), refresh policy. Feeds the
  ratified overlay's `toolchain_bindings` payload refs.
- ADDED realization: the Worker Host App in Omnigent-Install; Intune
  packaging + policies in OpsxFactory.

## Claims

1. **Reconcile, don't script.** The app converges the host toward the
   manifest and emits evidence records per reconcile (hermes-install
   evidence vocabulary); drift is reported, not silently reapplied. A
   rerun on a healthy host is a byte-identical no-op.
2. **Intune is the delivery plane** (OpsxFactory-owned, per the
   GitHub-administration managed-platform precedent): Win32 `.intunewin`
   assigned to an `xfactory-worker-hosts` device group, SYSTEM context,
   detection rules on app version + manifest digest. No dependence on any
   interactive session.
3. **Substrate: WSL2 + container engine inside the distro.** The Cloud PC
   8-vCPU SKU supports nested virtualization. Engine leaning: docker-ce
   inside WSL (fidelity with the operator's existing benches; no Docker
   Desktop per-seat licensing). Reboot orchestrated via Intune Win32
   restart semantics.
4. **Sealed identities, passwordless-first.** Workers run under virtual
   service accounts where the runner supports it; any password-bearing
   account is generated directly into Key Vault (escrow-at-birth — the
   2026-07-23 lesson made mandatory). Interactive/RDP logon denied
   post-bootstrap, enforced not just documented.
5. **Heartbeats are app-owned and durable**: scheduled tasks (boot trigger +
   3-minute repetition + restart-on-failure) publishing from within each
   worker context; heartbeat contract deltas land in publisher + service +
   evaluator together (pinned by the parity-test pattern). The heartbeat
   gains a bench inventory section (ids + digests) so readiness can gate on
   bench presence.
6. **Benches are digest-pinned governed artifacts**: pulled from a platform
   ACR, verified against their bench-manifest before advertisement; no
   mutable tags; no credentials baked in — auth profiles materialize at
   runtime per the existing pattern (`xfactor-001`).
7. **First consumer is Omni-001** (`CPC-Omni0-P5AJB`, provisioned 2026-07-10,
   idle, Intune-compliant): stood up entirely by the app, then the rider
   runner-group registrations swap over and the operator's personal CPC
   (`CPC-brett-TUBV0`) retires from fleet duty. `omni002+` become
   assignment-group membership, zero-touch.

## Draft manifest sketches (to ratify via OpenSpec)

```yaml
schema_version: 1
kind: xfactory_worker_host_manifest
host:
  host_id: cpc-omni01
  device: CPC-Omni0-P5AJB
  policy_version: artifact-worker-v1
substrate:
  wsl_distro: ubuntu-24.04            # pinned
  container_engine: docker-ce          # inside WSL, systemd on
workers:
  - worker_id: xfactory-coding-rider-cpc-omni01
    runner_name: xfactory-coding-cpc-omni01
    runner_group: xfactory-execution-lane-workers
    labels: [self-hosted, omnigent, artifact-only, rider, coding-patch, host-coding-cpc-omni01]
    dispatch_label: host-coding-cpc-omni01
    profiles: {coding-patch-worker: "1"}
    identity: {kind: virtual_service_account}   # or local+vaultref
    auth_profile: vaultref://kv-opensoft-xfactory-qa/secrets/xfactor-001-claude-credentials-json
    heartbeat: {interval: PT3M, execution_lane: artifact_only,
                tenant_boundary: opensoft, data_boundary: opensoft-internal,
                handling_classes: [internal-engineering]}
benches:
  - bench_id: python-bench
    image: <platform-acr>/benches/python@sha256:<digest>
    manifest: vaultref-or-repo-path   # bench-manifest location, see open questions
```

```yaml
schema_version: 1
kind: xfactory_tech_bench
bench_id: python-bench
stack: python
image: {repository: <platform-acr>/benches/python, digest: sha256:<...>}
tools:
  - {name: python, version: "3.12.x"}
  - {name: uv, version: "..."}
  - {name: pytest, version: "..."}
capabilities: [unit-test, lint, package-build]
credentials: none            # constitutional: benches are tools-only
refresh: {policy: rebuild-on-base-cve, cadence: monthly}
```

## Decisions to take

- **Container engine**: docker-ce in WSL (leaning) vs Podman (rootless).
- **App implementation v1**: PowerShell module + supervisor scheduled task
  (leaning — fast, auditable, no toolchain on the host) vs compiled service;
  v2 grows into the full enrollment-handshake agent (device-cert-backed
  identity, Hermes registration approval).
- **ACR pull identity**: per-host scoped ACR token escrowed in KV (v1
  leaning) vs device-certificate-backed Entra credential (v2).
- **Bench registry + build pipeline owner**: platform ACR
  (rg-os-platform-ai-factory-prod?) — OpsxFactory or codexFactory CI builds
  benches and emits digest + manifest per build. Bench sources today live on
  the operator's workstation; which repo owns them going forward?

## Open questions

- Local-admin path on Omni-001: does the Windows 365 provisioning policy
  grant admin to the assigned user, or does everything ride SYSTEM via
  Intune (preferred)? Inventory needed (one device-code Graph session with
  DeviceManagementConfiguration.Read.All).
- Runner under a virtual service account: does actions-runner service
  support `NT SERVICE\*` logon, or do runners stay on escrowed local
  accounts while heartbeat/bench duties go passwordless?
- Where bench manifests live: alongside bench Dockerfiles in the bench
  source repo, mirrored into overlays by pin, or attached as OCI artifacts
  next to the image?
- Heartbeat bench-inventory contract delta: neutral heartbeat contract +
  omnigent-install service + codexFactory evaluator in one coordinated
  change (three-places rule).
- WSL servicing: who patches the distro/engine — the app on reconcile, or
  Intune servicing policy?
- LLM-vault consolidation interaction: app materializes auth profiles from
  the master provider vault (`kv-os-llmfact-prod-01`) or the env vault?
  Consolidation should land before or with first Omni-001 install.

## Exit

An openxFactory OpenSpec change ratifying `worker-host-manifest` +
`bench-manifest` (or blessing the first-consumer drafts pending DTN), an
Omnigent-Install realization change for the app (validate/reconcile/verify
with evidence, dry-run default), and an OpsxFactory realization change for
packaging + WSL policy + assignment group. The topic archives only when
Omni-001 reaches green readiness (fresh heartbeats with bench inventory)
entirely via the app, a governed lane run executes against an Omni-001
worker, and the operator-CPC rider registrations are retired.
