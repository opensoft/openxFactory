# Staged: Worker Host WSL Install and Setup

Status: staged
Kind: architecture
Summary: The WSL substrate of the Worker Host App in one place — manifest
surface (pinned distro, systemd flag), the three observed truths and the
exact commands behind them, the convergence action set (feature install,
distro install, idempotent wsl.conf systemd enablement), the fail-closed
reboot semantics, and the WSL-specific open questions (SYSTEM-context
distro registration, servicing owner, kernel updates, resource limits)
that must resolve before Omni-001 goes live.
Topics: worker-host-app, wsl, wsl2, systemd, substrate, ubuntu, intune,
omnigent-install, opsxfactory, omni-001
Repository context: Omnigent-Install (the `substrate_wsl` step of the
Worker Host App — implemented, PR #33 `2bc5054`; `substrate_container_engine`
depends on it, PR #34 `28ac7ec`); OpsxFactory (WSL enablement policy,
Win32 packaging, reboot orchestration); openxFactory (the `substrate:`
block of the eventual neutral `worker-host-manifest`)
Staging ID: `openxFactory:staging:worker-host-app`
Source: split out of [worker-host-app.md](worker-host-app.md) 2026-07-25
(Brett: the topic needs a doc focused only on the WSL install and setup);
semantics recorded from the implemented step, not re-designed here.

## Scope

Covers the WSL layer only: Windows feature enablement, pinned distro
provisioning, systemd bring-up inside the distro, reboot behavior, and
servicing. The container engine inside the distro is the NEXT step
(`substrate_container_engine`, docker-ce from Docker's apt repo; refuses
`prerequisite_unconverged` while the distro is absent) and Windows-side
worker identities are a later step — neither is re-specified here.

## Manifest surface

The manifest's `substrate:` block pins the WSL layer declaratively:

```yaml
substrate:
  wsl_distro: ubuntu-24.04   # pinned, lower-case manifest form
  container_engine: docker-ce
  systemd: true              # required for the engine's systemd service
```

- Manifests carry ONLY the lower-case form (`ubuntu-24.04`). The WSL
  registry name (`Ubuntu-24.04`) is derived at observe time
  (`ConvertTo-XFWWslDistroName`); registry-form strings never appear in
  manifests or evidence inputs.
- `systemd: true` is what the container-engine step relies on (docker-ce
  runs as a systemd service); a manifest without it accepts a distro
  with no systemd probe.

## Observed truth (three booleans, in dependency order)

Observation is read-only and runs through the injectable `-CommandRunner`
seam (CI drives a fake host; real hosts execute `wsl.exe`):

1. `wsl_present` — `wsl.exe --status` exits 0.
2. `distro_present` — `wsl.exe --list --quiet` contains the registry
   name. `wsl.exe` emits UTF-16, so captured output is NUL-stripped
   before matching.
3. `systemd_ready` — `wsl.exe -d <distro> -- test -d /run/systemd/system`
   exits 0. Observed truth is systemd RUNNING in the distro, not merely
   configured: a `/etc/wsl.conf` edit alone does NOT count until the
   distro has restarted. If the manifest does not ask for systemd, a
   present distro is already ready.

A host where these commands cannot be asked at all is *unobservable* —
see fail-closed rules below.

## Convergence actions (only the missing ones, in order)

1. WSL feature absent → `wsl.exe --install --no-distribution --no-launch`
2. Pinned distro absent → `wsl.exe --install -d <RegistryName> --no-launch`
3. systemd required but not ready → two actions:
   - an idempotent root shell in the distro that appends `[boot]` /
     `systemd=true` to `/etc/wsl.conf` ONLY where absent (grep-guarded;
     re-running it never duplicates lines), then
   - `wsl.exe --terminate <distro>` so the next start boots systemd.

A converged host produces an empty action list: plan says
`would_converge`-nothing-pending and a committed reconcile is a no-op
with an evidence record saying so (same manifest + same host state =
byte-identical no-op).

## Fail-closed rules (the reboot story lives here)

- Unobservable host ⇒ plan reports `unknown` (never `would_converge`);
  apply refuses `host_unobservable` BEFORE any mutation.
- Actions that ran without the re-observation converging report the step
  `failed`, never `changed`. This is the honest encoding of the real
  WSL behavior: a fresh WSL feature install typically requires a reboot,
  so the first committed reconcile on a virgin host reports `failed`
  with a remediation category — the reboot itself is owned by the
  delivery plane (Intune Win32 restart semantics, OpsxFactory packaging
  change), after which the next reconcile converges.
- The app never schedules or forces the reboot itself.

## Execution context

Delivered by Intune as a Win32 package in SYSTEM context to the
`xfactory-worker-hosts` device group. The Cloud PC 8-vCPU SKU supports
nested virtualization (claim 3 of the primary doc); Omni-001
(`CPC-Omni0-P5AJB`) is the first consumer.

## Verification

- CI: fake-host runner (`New-FakeWslRunner` in
  `hostapp/tests/Invoke-HostAppTests.ps1`) answers exactly the argv
  shapes above; install actions mutate fake state so re-observation
  proves convergence.
- Real host: the `Verify` verb refuses until the real acceptance check
  (a `readiness_only` lane dispatch evaluating green) is wired; Omni-001
  green readiness entirely via the app is the topic's exit criterion.

## Open questions (WSL-specific)

1. **SYSTEM-context distro registration (raised by this doc, needs the
   Omni-001 fact-check)**: WSL registers distros per-user in the
   invoking user's registry hive. The app runs as SYSTEM, so the pinned
   distro would register under SYSTEM's profile — but runner services
   and benches must reach docker inside that distro from the worker
   identities. Whether SYSTEM-registered distros are reachable from
   service-account sessions (and whether `wsl.exe` is even on SYSTEM's
   path pre-reboot) is untested — the fake-host suite cannot see this
   class. Fold into the existing Omni-001 inventory fact-check.
2. **Servicing owner** (carried from the primary doc): who patches the
   distro and engine — the app on reconcile, or Intune servicing policy?
3. **WSL kernel updates**: `wsl --update` is unmanaged today; decide
   whether it joins the reconcile surface or the servicing policy.
4. **Resource limits**: `.wslconfig` (memory / vCPU caps for the WSL VM)
   is not in the manifest; decide whether `substrate:` grows fields for
   it or the host default stands.

## Exit

This fragment folds into the same OpenSpec exits as the primary doc (the
`worker-host-manifest` `substrate:` block, the Omnigent-Install app
change, the OpsxFactory packaging + WSL policy change); it archives with
the topic.
