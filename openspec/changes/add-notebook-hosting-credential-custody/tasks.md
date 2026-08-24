# Tasks: add-notebook-hosting-credential-custody

Status: draft

NOTHING BELOW RUNS BEFORE RATIFICATION. This change's own diff is the spec
deltas and these records. **No task here creates, moves, or reads a live
secret**: putting the password into the vault is an operator's act under the
landed rule, evidenced per `credential-contracts`, and it is listed in §4 as
that operator act rather than as work this change performs.

## 1. The hosting record declares its custody

- [ ] 1.1 Add a `custody:` block to `examples/notebook-projection-hosting.yaml`
  carrying a BY-REFERENCE pointer only: the binding's identifier, the secret
  reference, and what the custody covers. No password, recovery code, TOTP
  seed, session cookie, or exported profile — in this file or any other.
- [ ] 1.2 State the custody's honest reach in the record itself: which secrets
  the binding holds, and that the sign-in's interactive step remains. A
  reference that implies unattended access invites a reader to plan on it.
- [ ] 1.3 Leave `self_hosted` declarations free of the obligation, matching the
  two-case model: no operator, no obligation.

## 2. The validator enforces by-reference-only

- [ ] 2.1 Teach `scripts/validate-notebook-projection-hosting.py` the custody
  rule: an operator-hosted declaration carries a custody reference; a
  self-hosted one need not.
- [ ] 2.2 REFUSE anything secret-shaped in the record — a `password`,
  `totp`/`otp_seed`, `recovery_code`, `cookie`, `session` or `profile` field,
  and any value that looks like credential material rather than a reference.
  The refusal message names the binding as the remedy, not redaction in place.
- [ ] 2.3 Tests for both directions, and a test that a reference alone is
  insufficient to obtain anything.

## 3. Documentation

- [ ] 3.1 `docs/lifecycle-notebook-projection.md` §12: the custody story — where
  the credential lives, that each consuming system reaches it through its own
  binding, and that custody is not automation.
- [ ] 3.2 `docs/notebook-projection-migration-runbook.md`: the custody step in
  sequence, and what an operator does when the interactive login is needed
  anyway.
- [ ] 3.3 Record the session-class rule where a reader will hit it: the `nlm`
  profile is refreshable session state and is NOT a custody subject, on the
  same grounds `credential-contracts` already refuses distributing that class.

## 4. The bindings — one per consuming system

- [ ] 4.1 OPTIONAL, and decide explicitly: a packaged reference fixture under
  `examples/credential-contracts/` showing the two-consuming-system shape. If
  taken, the self-test count string asserted in
  `tests/credential_contracts/test_dispatch_credential_contract.py` ("3
  positive + 5 negative") MUST be updated in the same commit or the suite
  fails. If declined, say so and rely on the requirement text.
- [ ] 4.2 NOT AN OPENXFACTORY SURFACE: the live xFactory sync-lane binding is
  declared in the install's `credentials/` tree, per the residency rule in
  `contracts/manifest.yaml` ("openxFactory ships no instance records"). Named
  here as the successor act; the shape is `provider`, `vault`, `secret_ref`,
  `owner`, `rotation_policy` with its own owner and its own access identity.
- [ ] 4.3 NOT THIS CHANGE: the openXdox binding is its own successor packet in
  its own lane, per Brett's ruling — openXdox pins openxFactory's contracts and
  declares its own binding, with its own access identity, grant, rotation
  visibility and audit trail.
- [ ] 4.4 OPERATOR ACT, not a task this change performs: the password (and any
  TOTP seed) is placed into `kv-opensoft-xfactory-qa` by Brett or an operator,
  under the landed custody rule, evidenced per `credential-contracts`. Nothing
  in this repository performs or witnesses that write.

## 5. Validate green

- [ ] 5.1 Gates: `pytest tests/ideation-dashboard`, `pytest
  tests/ideation_dashboard`, `pytest tests/doc-health`, plus
  `pytest tests/notebooklm` and `pytest tests/credential_contracts` for the
  surfaces this change touches; `OPENSPEC_TELEMETRY=0 openspec validate --all
  --strict`; doc-health zero-new against a fresh same-clock `origin/main`
  baseline; `scripts/validate-notebook-projection-hosting.py` and
  `scripts/validate-credential-contracts.py .` both clean.
- [ ] 5.2 Assert `contracts/` untouched and no bundle cut. `target_release:
  none` — the binding-template shape is already published.

## 6. Bookkeeping

- [ ] 6.1 README OpenSpec Records: move this change from active to archived
  when it archives.
- [ ] 6.2 Reconcile with `add-notebook-projection-identity` at ITS archive: the
  generalization these requirements presume promotes then, and the two changes'
  `credential-contracts` text should be read together once both are promoted.

## 7. NOT part of this change

- Automated Google login. It is future work gated on proving the browser flow
  end to end, and custody does not advance it.
- Any change to the residency model that would let live binding instances live
  in openxFactory. If the ratifier wants the instances here, that rule changes
  first, in its own change.
- Rotating, replacing, or reading the account's credential.
