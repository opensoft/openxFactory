---
code_surface: openxFactory (serve.py `/capabilities` route adds a per-request `hosted_actor` field read from the gateway-stamped `X-Auth-Request-User` header; a new `web/views/account-menu.js` header-popover view following the settings.js pattern; `web/index.html` corner-controls wiring for a user-account button beside the theme and settings buttons; tests — a serve.py test for the hosted_actor field including its null case, and a node/DOM test for the menu)
target_release: none
Status: ratified
Ratified: 2026-08-21 by Brett Heap — record: the 2026-08-22 in-session ruling round captured in `docs/archive-record-discrepancies.md` (C7 and C3's account-menu half), in which Brett declared the ratification fact this change's own record never carried. No approving OpenSpec change exists to name and no contemporaneous quotation was written down, so this is the `Ratified:` record-citing spelling ten archived siblings already use, not `Ratified by: <change>`. The header read `draft` from proposal through archive; header, citation, and this change's `.openspec.yaml` were all added 2026-08-22 by `archive-register-rulings`. See tasks.md "Bookkeeping resolution".
Proposed: 2026-08-21
Origin: In hosted mode the dashboard sits behind the dox-auth gateway with a verified per-user identity, but the UI shows no account affordance and no way to sign out.
---

# Proposal: add-dashboard-account-menu

## Why

In hosted mode the dashboard is served behind the dox-auth gateway (in the
Omnigent-Install repo). The gateway does per-user authentication and STAMPS the
verified username into the `X-Auth-Request-User` request header on every
proxied request, having STRIPPED any client-supplied value first;
NetworkPolicies pin the dashboard so only the gateway can reach it. The gateway
also OWNS the `/logout` route — it clears the `__Host-dox_session` cookie and
redirects to `/login`.

So a verified per-user identity is already arriving on every request, and a
governed way to end the session already exists. The dashboard uses neither:
the UI shows no account affordance, no signed-in username, no access level, and
no way to sign out. A viewer cannot tell WHO they are signed in as, nor leave.

The identity is READ-ONLY presentation data. The gateway is the identity
authority; the dashboard's trust in the header rests entirely on the
NetworkPolicy boundary (only the gateway can reach the dashboard, and the
gateway strips any client value before stamping its own). Surfacing the
identity for DISPLAY does not make the credential-free dashboard a credential
holder or an authorization authority — the boundary the dashboard already
draws around every write, gate, and edit action is unchanged, and none of them
consults the header.

## What changes

- **The serve surfaces the hosted actor additively on `/capabilities`.** The
  route already builds `payload = dict(self.capabilities)` PER REQUEST and adds
  a per-request `repository` field; it gains a per-request `hosted_actor` field
  read from `X-Auth-Request-User`, `null` when the header is absent (local /
  loopback serving, or an unauthenticated path). It is additive to the
  unversioned `/capabilities` shape — the same additive pattern the `model`
  field and the `repository` field followed — so no version bump and existing
  consumers are unaffected.

- **The field is display-only.** The dashboard treats `hosted_actor` as
  presentation data. It MUST NOT grant, gate, or unlock any action on it; all
  existing write/gate/edit gating (loopback + real checkout + resolved local
  actor + per-serve console token) stays exactly as-is.

- **A user-account menu joins the corner controls.** A user-icon button sits in
  the top-right `.cornerbtns` span beside the theme and settings buttons, and
  opens a dropdown showing the signed-in username, the session's access level
  (DERIVED from the existing `/capabilities.actions` map plus loopback state,
  inventing no new authorization), and a logout control. It follows the
  established settings.js header-popover contract: an aside anchored under its
  button, Escape and outside-click close, keyboard-focusable, DOM-safe text
  binding via `textContent`.

- **Logout delegates to the gateway.** The logout control navigates the browser
  to the gateway-owned `/logout` route. The dashboard does NOT implement session
  termination itself.

## Impact

- Affected specs: `ideation-dashboard` (four ADDED requirements)
- Affected code: `scripts/ideation_dashboard/serve.py` (`/capabilities` route),
  a new `scripts/ideation_dashboard/web/views/account-menu.js`,
  `scripts/ideation_dashboard/web/index.html`, and tests under
  `tests/ideation-dashboard/`
- No schema, contract, or register change; the `/capabilities` shape grows
  additively with no version bump, matching the prior `model` and `repository`
  fields. The dashboard writes nothing new and authorizes nothing on the new
  field.
- Depends on infrastructure that is ALREADY LIVE: the dox-auth gateway already
  stamps `X-Auth-Request-User` and already owns `/logout`. This change adds no
  gateway work.
