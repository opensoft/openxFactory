# ideation-dashboard

## ADDED Requirements

### Requirement: Hosted actor surfaced additively on capabilities
The serving side SHALL include a `hosted_actor` field on the `/capabilities` response, resolved PER REQUEST from the gateway-stamped `X-Auth-Request-User` header, and `null` when that header is absent. The field is additive to the existing unversioned `/capabilities` shape — the same additive pattern the prior `model` and `repository` fields followed — so it introduces no version bump and existing consumers are unaffected. The field is DISPLAY-ONLY: the dox-auth gateway remains the identity authority, the dashboard's trust in the header rests on the NetworkPolicy boundary that lets only the gateway reach it, and the dashboard reads the header to present a name and never to authorize.

#### Scenario: The stamped header is present
- WHEN a request carrying `X-Auth-Request-User: alice` reaches the `/capabilities` route
- THEN the response's `hosted_actor` MUST be `alice`
- AND the value is resolved per request, beside the existing per-request `repository` field

#### Scenario: The header is absent
- WHEN `/capabilities` is requested on a local or loopback serve, or by an unauthenticated path that still reached the probe, with no `X-Auth-Request-User` header
- THEN `hosted_actor` MUST be `null`

#### Scenario: A client-supplied header on a direct request is not trusted differently
- WHEN a direct (non-gateway) request carries a client-supplied `X-Auth-Request-User`
- THEN the dashboard MUST treat it exactly as any other value of that header — as DISPLAY data only — and MUST NOT authorize any action on it, because trust rests on the NetworkPolicy boundary and the gateway, which strips client values before stamping its own, remains the identity authority

### Requirement: The dashboard authorizes nothing on the hosted actor
The dashboard SHALL treat `hosted_actor` as presentation data only and MUST NOT use it to grant, gate, or unlock any action. All existing write, gate, and edit gating stays exactly as-is — a loopback bind, a real checkout, a resolved local actor, and the per-serve console token — none of which consults `hosted_actor`. Recording the design-D16 boundary nuance explicitly: the credential-free dashboard now READS a stamped identity header for display, which does not make it a credential holder or an authorization authority.

#### Scenario: A hosted request with an actor still cannot write or gate
- WHEN a request is hosted (not loopback) and carries a stamped `hosted_actor`
- THEN every write, gate, and edit affordance MUST remain unavailable exactly as it is today
- AND the presence of `hosted_actor` MUST NOT change any capability verdict, because those capabilities are keyed on the loopback console verdict and never on identity presence

### Requirement: The user-account menu
The dashboard SHALL render a user-account control in the top-right corner header controls, beside the theme and settings buttons, that opens a dropdown showing the signed-in username, the session's access level, and a logout control. The username SHALL be `hosted_actor`. The access level SHALL be DERIVED from the existing `/capabilities.actions` map plus loopback state — read-only when no write, gate, or edit action is available, otherwise naming the granted capabilities — reusing existing capability flags and inventing no new authorization. The menu SHALL follow the established header-popover interaction contract: anchored under its button, closed on Escape and on outside click, keyboard-focusable, and DOM-safe with every dynamic value bound via `textContent` and never `innerHTML`.

#### Scenario: A hosted session opens the menu
- WHEN a viewer with a present `hosted_actor` opens the account menu
- THEN it MUST show that username, the derived access level, and an enabled logout control
- AND it MUST anchor under its button, close on Escape and outside click, and bind every dynamic value via `textContent`

#### Scenario: A local session opens the menu
- WHEN the menu opens with `hosted_actor` absent (local mode)
- THEN it MUST show the local actor if the serve resolved one, or a generic "local session" label otherwise
- AND it MUST show NO logout control, because there is no gateway session to end

#### Scenario: The access level reflects the capability verdict
- WHEN the menu renders its access level
- THEN it MUST read the level from the existing `/capabilities.actions` map plus loopback state, showing read-only when no write, gate, or edit action is available and otherwise naming the granted capabilities
- AND it MUST NOT introduce any new authorization flag

### Requirement: Logout delegates to the gateway
The logout control SHALL navigate the browser to the gateway-owned `/logout` route, which clears the session cookie and redirects to `/login`. The dashboard SHALL NOT implement session termination itself.

#### Scenario: Activating logout leaves for the gateway
- WHEN a viewer activates the logout control
- THEN the browser MUST navigate to `/logout`
- AND the dashboard MUST NOT clear any session or perform any termination of its own
