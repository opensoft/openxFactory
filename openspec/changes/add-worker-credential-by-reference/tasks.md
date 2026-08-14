# Tasks — add-worker-credential-by-reference

## 1. Ratification

- [ ] 1.1 Present for review; record the ruling. (The ownership split was
      pre-ruled 2026-08-11 — neutral contract, operator as binding; this
      change realizes that ruling as contract text.)
- [ ] 1.2 Strict-validate (single + `--all`); list in the README OpenSpec
      Records block; follow-through pointer in the
      `hermes-stack-topology-per-client` staging topic.

## 2. Realization (archives the change; xFactory + operator)

- [ ] 2.1 Runbook §11 (xFactory registration runbook): the fetch identity —
      one Entra workload identity per install, standard-subject FIC on a
      `worker-credentials` GitHub environment (main-only policy; the
      flexible-FIC outage interim and upgrade trigger apply), Key Vault
      Secrets User on exactly the lane token secret, no Hermes scopes, no
      GitHub write.
- [ ] 2.2 Operator: mint the `setup-token`-class secret into the vault
      (`xfactor-001-claude-credentials` successor, token class NOT the
      session file), provision the fetch identity, set the two repo
      bindings (secret URI variable + fetch client id variable).
- [ ] 2.3 Wire ONE lane first (council-deliberation worker's deliberate
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
