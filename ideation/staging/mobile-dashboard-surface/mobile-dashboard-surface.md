# Staged: Mobile Dashboard Surface — the avatar-first app's operational face

Status: staged
Kind: client-surface
Summary: A mobile app realization of the ratified `avatar-first-ui`
standard: the dashboard surface for the xFactory family, honoring the
Hermes-layer surface defaults (subject users default avatar-first,
tenant staff default hybrid, domain authority conventional-with-
copilot), and hosting per-domain org-connect onboarding flows (first:
LedgerxFactory's MSBC connect — see ledgerx:staging:
external-client-connect).
Topics: avatar-first-ui, mobile, dashboard, client-surface, onboarding, admin-consent, hermes-layers
Repository context: openxFactory owns the neutral surface standard (avatar-first-ui, ratified) and this topic; the client shell lives with the avatar-client track (private openAvatar repo); per-domain connect flows live in the DomainxFactory repos
Staging ID: openxFactory:staging:mobile-dashboard-surface
Source: team-010 LedgerxFactory session 2026-07-26 — Brett: the mobile dashboard is part of the avatar-first mobile app plan, with per-layer UI defaults (subject company user vs tenant-level user); confirmed against the ratified `avatar-first-ui` "Hermes-layer surface defaults" requirement
Target capabilities: avatar-first-ui (MODIFIED or realization evidence) + avatar-client track realization (post `avatar-pilot-hardening`)

## Claims

1. **The defaults are already ratified — this topic realizes, not
   redecides.** `avatar-first-ui` "Hermes-layer surface defaults":
   Customer/Subject Hermes surfaces default avatar-first; Client/Tenant
   Hermes surfaces default hybrid (conventional work surface primary
   for dashboards, queues, approvals); Domain Hermes conventional with
   an avatar copilot. One app, sign-in determines the layer, the layer
   determines the default; per-DomainxFactory overrides carry the
   ratified override fields (user set, workflow need, risk class,
   accessibility fallback, authority boundary).
2. **Dashboards are the tenant-staff face** — per the ratified
   "Client operator performs repeated work" scenario, the conventional
   surface stays primary there, with avatar guidance available; subject
   users get the avatar-first intake/consent/comprehension flows.
3. **Org-connect onboarding is a hosted per-domain flow**: the app can
   carry each domain's connect ceremony (Ledgerx MSBC first: Entra
   admin-consent webview + BC Admin Center extension install + setup
   API), always as Microsoft-native ceremonies in a system browser —
   the app never builds custom credential UI and never holds standing
   credentials.
4. **Reads ride governed surfaces**: dashboard data comes through
   token-gated read surfaces (worker-readiness-surface precedent), per
   layer and per client scope — never raw platform credentials on the
   device.

## Desktop target and test-phase bring-up (Brett, 2026-07-26)

The client app targets **mobile AND desktop** — preferably one codebase
with a desktop build target rather than a separate app (this weights
open question 1 toward a cross-platform shell). Desktop is also the
easiest test channel: a downloadable binary on **GitHub Releases**, no
store gatekeeping. Phases:

- **T1 — dashboard-first cut, no avatar**: sign-in, Hermes-layer
  detection (party-ladder role → default surface), governed-surface
  reads (the live worker-readiness surface is the day-one data source).
  Artifacts on GitHub Releases: desktop binaries + Android APK
  (sideload); iOS testing goes through TestFlight when it joins —
  stated honestly, GitHub cannot carry installable iOS builds.
- **T2 — connect flows**: the Ledgerx MSBC connect ceremony driven from
  the app against a test estate, using the GitHub-released PTE build of
  the BC extension (ledgerx:staging:external-client-connect T4 — the
  two topics' test phases meet here).
- **T3 — avatar layer joins** post `avatar-pilot-hardening`, upgrading
  subject-layer surfaces from conventional-fallback to their ratified
  avatar-first default.

Each phase lands bring-up evidence per the usual discipline.

## Open questions

1. Shell platform: does the avatar-client kernel (frozen AVC ports,
   contract-v1.7) host the mobile shell directly, or is the dashboard a
   second shell beside the avatar runtime? (Pilot-hardening is the last
   staged successor — this topic must not fork authority work.) The
   desktop target requirement weights this toward a cross-platform
   shell with mobile + desktop builds from one codebase.
2. Sequencing vs `avatar-pilot-hardening`: dashboard-first (readiness
   surface data, no avatar) as an early cut, avatar layer joins after
   the pilot?
3. Distribution: store presence timing, and whether the connect flows
   ship in v1.

## Exit path

Either realization evidence under `avatar-first-ui` plus a client-track
work order, or a small ADDED requirement if the dashboard surface needs
contract language of its own. Per-domain connect flows exit through
their DomainxFactory topics (first: LedgerxFactory
external-client-connect).
