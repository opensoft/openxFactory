# Tasks — add-worker-credential-by-reference

## 1. Ratification

- [x] 1.1 (DONE 2026-08-14 — ratified verbatim; direct-from-tasks realization confirmed.) Present for review; record the ruling. (The ownership split was
      pre-ruled 2026-08-11 — neutral contract, operator as binding; this
      change realizes that ruling as contract text.)
- [x] 1.2 (DONE — single + --all strict green 58/58; README listed; topic pointer added.) Strict-validate (single + `--all`); list in the README OpenSpec
      Records block; follow-through pointer in the
      `hermes-stack-topology-per-client` staging topic.

## 2. Realization (archives the change; xFactory + operator)

- [x] 2.1 (DONE — xFactory 0af326a, runbook §11: narrowest identity yet (KV read on one secret, no Hermes scopes, no GitHub write), worker-credentials environment created main-only, setup-token-class secret with the session-file secret named non-conforming, versionless-URI bindings, rotation as the verify scenario.) Runbook §11 (xFactory registration runbook): the fetch identity —
      one Entra workload identity per install, standard-subject FIC on a
      `worker-credentials` GitHub environment (main-only policy; the
      flexible-FIC outage interim and upgrade trigger apply), Key Vault
      Secrets User on exactly the lane token secret, no Hermes scopes, no
      GitHub write.
- [ ] 2.2 Operator: mint the `setup-token`-class secret into the vault
      (`xfactor-001-claude-credentials` successor, token class NOT the
      session file), provision the fetch identity, set the two repo
      bindings (secret URI variable + fetch client id variable).
- [x] 2.3 (DONE — xFactory 0af326a: fetch step ahead of the seats, OIDC → vault-scope exchange → versionless GET → masked into job env; the hermetic invocation consumes it unchanged; unset bindings = named degraded-mode notice (verified live: post-change smoke ran degraded and green, so the wiring is inert-safe); token source logged vault-vs-degraded for the verify and rotation reads.) Wire ONE lane first (council-deliberation worker's deliberate
      job): fetch step (OIDC → vault get via curl/python, value masked,
      exported only to the job env) ahead of the existing hermetic
      invocation; the service-scoped env var becomes the documented
      fallback until all lanes migrate.
- [ ] 2.4 Live evidence: one deliberation run consuming the vault-fetched
      token end to end; then rotate the vault secret and show the NEXT run
      consumes the new version with zero host access — the rotation
      scenario proven live.
- [ ] 2.5 Migrate review-lane and doc-health-analysis to the same fetch
      step; remove the service-scoped env var from the host (closing the
      degraded-mode gap on this install); record it.

## 3. Closeout

- [ ] 3.1 Tick with evidence; archive (code surface green per the
      release-realization rule); note the pattern as the worked example the
      per-client stack topology topic's onboarding story consumes.
