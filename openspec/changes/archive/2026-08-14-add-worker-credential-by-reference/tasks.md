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
- [x] 2.2 (DONE 2026-08-14 — operator provisioned per §11: fetch identity + KV Secrets User on the setup-token-class secret + the two versionless bindings; confirmed by the §11.4 smokes.) Operator: mint the `setup-token`-class secret into the vault
      (`xfactor-001-claude-credentials` successor, token class NOT the
      session file), provision the fetch identity, set the two repo
      bindings (secret URI variable + fetch client id variable).
- [x] 2.3 (DONE — xFactory 0af326a: fetch step ahead of the seats, OIDC → vault-scope exchange → versionless GET → masked into job env; the hermetic invocation consumes it unchanged; unset bindings = named degraded-mode notice (verified live: post-change smoke ran degraded and green, so the wiring is inert-safe); token source logged vault-vs-degraded for the verify and rotation reads.) Wire ONE lane first (council-deliberation worker's deliberate
      job): fetch step (OIDC → vault get via curl/python, value masked,
      exported only to the job env) ahead of the existing hermetic
      invocation; the service-scoped env var becomes the documented
      fallback until all lanes migrate.
- [x] 2.4 (DONE 2026-08-14 — §11.4 smokes, operator-confirmed: token source VAULT with SMOKE OK, then a vault-write rotation and the next run consuming the new version with ZERO host access — the contract's archive-gate scenario proven on the lane's own seat invocation; the deliberate job runs the byte-identical fetch step, so the next natural clearance is confirmatory.) Live evidence: one deliberation run consuming the vault-fetched
      token end to end; then rotate the vault secret and show the NEXT run
      consumes the new version with zero host access — the rotation
      scenario proven live.
- [x] 2.5 (DONE 2026-08-14 — lane half at xFactory 6758046; HOST HALF
      operator-confirmed: the artifact runner's .env deleted (it held only
      CLAUDE_CODE_OAUTH_TOKEN), machine/user/process token scopes verified
      absent on both runners, both stale profile .credentials.json deleted
      permanently, services restarted and online. Final smoke run
      31833019258: token source VAULT, sk-ant-oat* recognized, SMOKE OK —
      CPC-BRETT01 is fully host-credential-free; the degraded-mode gap on
      this install is CLOSED and vault deletion is the single kill switch.)
      Migrate review-lane and doc-health-analysis to the same fetch
      step; remove the service-scoped env var from the host (closing the
      degraded-mode gap on this install); record it.

## 3. Closeout

- [x] 3.1 (DONE 2026-08-14 — archived; code surface green: vault fetch live on all three lanes, rotation scenario proven, host credential-free end state reached.) Tick with evidence; archive (code surface green per the
      release-realization rule); note the pattern as the worked example the
      per-client stack topology topic's onboarding story consumes.
