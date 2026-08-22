# Tasks: add-dashboard-account-menu

## 1. The serve surfaces the hosted actor

- [ ] 1.1 `/capabilities` reports `hosted_actor`, resolved PER REQUEST from the
      `X-Auth-Request-User` header beside the existing per-request `repository`
      field, and `null` when the header is absent. Additive to the unversioned
      shape — no version bump, matching the prior `model` and `repository`
      fields.
- [ ] 1.2 The field is DISPLAY-ONLY: it feeds no capability verdict and no
      route consults it to authorize. Add the D16 boundary comment where the
      field is set, so no reader over-reads a stamped header as a credential.

## 2. The account-menu view

- [ ] 2.1 New `web/views/account-menu.js` following the settings.js header-
      popover pattern: an aside appended to `<body>`, anchored under its
      button, Escape and outside-click close, keyboard-focusable, every dynamic
      value bound via `textContent` (never `innerHTML`).
- [ ] 2.2 The menu renders the signed-in username from `hosted_actor`, the
      derived access level (read from `/capabilities.actions` + loopback state —
      read-only when no write/gate/edit action, otherwise naming the granted
      capabilities), and a logout control.
- [ ] 2.3 Graceful local mode: with `hosted_actor` absent, show the local actor
      if the serve resolved one, or a generic "local session" label, and render
      NO logout control.
- [ ] 2.4 Logout navigates the browser to the gateway-owned `/logout`; the view
      terminates no session itself.

## 3. index.html wiring

- [ ] 3.1 Add a user-account button to the `.cornerbtns` span beside the theme
      and settings buttons, with `aria-expanded` / `aria-controls` matching the
      settings button's accessibility shape, and wire it to the account-menu
      view.

## 4. Tests

- [ ] 4.1 A serve.py test for the `hosted_actor` field: present → the stamped
      username; absent → `null`; and a hosted request with a stamped actor
      still yields no write/gate/edit capability.
- [ ] 4.2 A node/DOM test for the account menu following the settings.js test
      pattern: open/close on button, Escape, and outside click; keyboard focus;
      username + access level render; local mode hides logout; logout targets
      `/logout`.

## 5. Docs

- [ ] 5.1 Add the active change to the openxFactory README "OpenSpec Records"
      block, matching the existing line format.

## 6. Verification

- [ ] 6.1 `OPENSPEC_TELEMETRY=0 openspec validate add-dashboard-account-menu
      --strict` and `--all --strict` both green.
- [ ] 6.2 Full dashboard suites green; live proof of the menu in hosted and
      local modes (username + access level shown; logout leaves for `/logout`
      hosted, absent local).
