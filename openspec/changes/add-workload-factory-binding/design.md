## Context

openXwallet owns no canonical contract; factory grant/trust/identity compositions
belong here. The openxFactory constitution excludes unratified keyholding or socket
runtime here. Existing neutral possession proof APIs remain owned by openWallet.
The source-selected pilot is blocked at T002; this candidate does not clear it.

## Goals / Non-Goals

Deliver current actor/wallet/key and bounded grant checks, exact workload identity,
separate artifact observation and durable one-use signing reservations as an
offline adapter candidate. Do not issue grants, execute operations, assert human
approval, deploy an observer or claim live GitHub qualification.

## Decisions

1. Place the candidate profile only in this change's supporting-docs. Existing
   wallet/grant field names and conservative `act` posture remain unchanged.
2. Put code/test-only processes in openXwallet, with its sole Speckit task list.
   The current commission permits this reviewable candidate, not ratification.
3. Require an operator-selected fresh issuer-key snapshot, exact caller and reusable
   workflow claims, and a separate trusted supervisor public key. No token-selected
   key URL or worker-carried grants.
4. Bind observation to token, challenge, request, policy revision, run and measured
   fixture composition. The observer reads its selected files/configuration.
5. Reserve issuer/token and issuer/challenge durably before opaque custody. Retain
   failed reservations. Recheck current state before returning a proof.
6. Inject the owning neutral API; do not fork it or silently advance its pin.

## Risks / Trade-offs

- Operator key/config authenticity and refresh remain trusted embedding duties.
- Reference artifact measurement does not establish model behavior, host integrity
  or a deployed independent supervisor. Same-user processes are not hostile OS isolation.
- Post-sign rechecks detect observed races but supply no distributed atomic revocation.
- Permanent replay reservations suit the bounded candidate; retention policy is
  a later operational concern. A new challenge/token is required after outage.
- Only same-wallet bounded `act` grant chains are supported; broader delegation,
  approval and unbounded scopes refuse rather than get inferred.

## Migration Plan

No migration, activation or published-contract change. Review candidate source and
isolated evidence first. Exact profile ratification, live GitHub/observer/custody
composition, independent human broker and protected pilot qualification remain
subsequent governed decisions.

## Open Questions

No question blocks the commissioned candidate. Owner ratification and deployment
qualification are deliberately unresolved acceptance gates.
