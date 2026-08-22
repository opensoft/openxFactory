# Design: add-dashboard-account-menu

## The identity-ladder rule

The dashboard is served behind the dox-auth gateway (Omnigent-Install). The
gateway is the identity authority: it authenticates the per-user request,
STRIPS any client-supplied `X-Auth-Request-User`, and STAMPS the verified
username into that header on every proxied request. NetworkPolicies pin the
dashboard so ONLY the gateway can reach it, and the gateway OWNS the `/logout`
route (clears `__Host-dox_session`, redirects to `/login`).

The header name is the stable contract — the "identity-ladder rule". The
dashboard reads `X-Auth-Request-User` for DISPLAY and never anything more. It
does not verify a token, does not consult a directory, does not decide who may
do what. Trust in the header rests entirely on the NetworkPolicy boundary: a
direct (non-gateway) request cannot reach the dashboard, and if one somehow
did, the dashboard would still only DISPLAY the value and authorize nothing on
it, so a spoofed header buys nothing. The gateway remains the identity
authority; the dashboard is a reader of a stamped fact.

## Why an additive `/capabilities` field, not a new `/whoami` route

The identity could be surfaced by a dedicated `/whoami` route. It should not
be, for two reasons already true of the serve:

1. **`/capabilities` is already fetched once at startup.** The browser reads it
   to decide which affordances render (notebook, gate, refresh, session, edit).
   Adding the hosted actor to that response means the account menu needs NO
   second fetch on load — the identity arrives with the capability verdict the
   corner controls already wait on. A new route would add a round-trip for a
   fact that travels naturally with the one the client already requests.

2. **`/capabilities` already carries per-request fields.** The route does
   `payload = dict(self.capabilities); writable = self._session_repository();
   payload["repository"] = ...` PER REQUEST — it is already the place the serve
   states per-request facts on top of the startup verdict. `hosted_actor` is
   exactly that shape: a fact of THIS request (its stamped header), not of the
   serve's startup. It belongs beside `repository`, resolved the same way.

The `/capabilities` shape is UNVERSIONED and grows additively — the `model`
field and the `repository` field both landed this way, no version bump, and a
consumer that never reads the new key is unaffected. `hosted_actor` follows
that precedent: additive, optional, `null` when absent.

## The D16 boundary nuance

The interactivity-boundary requirement (design D16) draws the dashboard as a
credential-free surface: it holds no secret, and its write/gate/edit authority
is fenced by loopback + real checkout + resolved local actor + a per-serve
console token. Reading a stamped identity header for display does not breach
that. Recording the nuance explicitly so no reader over-reads it: the
dashboard now READS an identity header, which is NOT the same as HOLDING a
credential or BECOMING an auth authority. It authorizes nothing on the value.
Every existing gate, write, and edit stays fenced exactly as before, and none
of them consults `hosted_actor`. A hosted (non-loopback) request with a
stamped actor still gets no write/gate/edit affordance, because those
capabilities were never keyed on identity presence — they are keyed on the
loopback console verdict, which the hosted plane fails regardless.

## Local vs hosted mode behaviour

- **Hosted** (behind the gateway): `X-Auth-Request-User` is present, so
  `hosted_actor` is that username. The menu shows the username, the derived
  access level, and an ENABLED logout that navigates to `/logout`.
- **Local / loopback** (an operator's `generate-and-open`, or any bind not
  behind the gateway): no `X-Auth-Request-User`, so `hosted_actor` is `null`.
  There is no gateway session to end, so the menu shows NO logout. It shows the
  local actor if the serve resolved one (the existing `actor` field —
  `git config user.name` on a loopback real checkout), otherwise a generic
  "local session" label. The menu degrades gracefully; it never renders a dead
  logout that would 404.

## Access-level derivation from existing capability flags

The access level is DERIVED, never a new authorization field. It reads the
`/capabilities.actions` map (`gate`, `edit`, `session`, `notebook`, `refresh`)
plus the loopback/actor state the serve already reports, and names the posture
in plain words:

- When no write/gate/edit action is available (the hosted plane's normal
  state), the level reads "read-only".
- Otherwise it names the granted capabilities (for a loopback human console:
  the gate/edit/session posture).

This invents no new flag and consults no identity. It is a presentation of the
capability verdict the serve already computes — the same verdict the workbench
posture indicator already reads to state `read-only` vs the gate-bearing
posture. The access level and that indicator therefore cannot disagree, because
they read the same source.

## Dependencies (already live)

Both pieces of infrastructure this change leans on exist today in
Omnigent-Install:

- the dox-auth gateway already STAMPS `X-Auth-Request-User` (having stripped
  any client value), and
- the gateway already OWNS `/logout` (clears `__Host-dox_session`, redirects to
  `/login`).

This change adds no gateway work. It reads the header the gateway already
stamps and links to the route the gateway already serves.
