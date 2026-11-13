# Dispatch Bootstrap Composition

Status: draft; source implementation commissioned for isolated testing only
Baseline: openXwallet #59 at `948ea81d7cdce35f5d006c747680a6b9fde37a29`;
factory grammar in `prepare-protected-runtime-qualification`

## Static commitment

Use `openxfactory-dispatch-selection-internal-v1`. Its closed bounded UTF-8 JSON
has exactly `profile` and `configuration`. The configuration follows the existing
runtime grammar except `launch` omits exactly `run_id` and `run_attempt`. Commit
all other fields: source/dependency/composition digests, case, time window,
environment, subject/audience, services, authority, state and lifecycle refs.
Unknown/missing fields, supplied run fields, pending inputs and invalid types
refuse. Existing RFC 8785 canonical SHA-256 includes the wrapper/profile.
This separate static input is not executable runtime config. The runtime
validator still requires both run fields and its original full digest/profile.

## Independent bootstrap boundary

Dispatch supplies accepted commit, selection digest and an opaque selected
preauthorization reference. The trusted host independently supplies the approved
selection digest, expected bootstrap principal and authenticated bounded reader.
Validate exact source/repository/manual context before invoking that capability;
the dispatch digest cannot approve itself.

Readback binds principal, preauthorization, selection digest, accepted source,
repository ID, case, actual run/attempt, full config digest, operation grant and
observation/expiry. Require a fresh observation during the request, at most 60
seconds of validity, and earliest deadlines through subsequent blocking admission.
Refuse worker bootstrap identity, wrong source/selection/config/case/grant,
changed run/attempt, stale/revoked/missing readback and clock regression. Errors
are fixed and safe; raw provider/credential data never escapes.

The separately administered authority authenticates the actual GitHub run/source
outside worker/dispatch control. It atomically binds one preauthorization to one
run/attempt and refuses concurrent reuse or replay. Same-run refresh cannot grant
a different run/attempt. This slice provides a trusted interface and isolated
reference behavior, not a deployed authority or authentication API. Distinct
principal strings and fixture callbacks do not establish deployed separation.

The independently approved full config must project to the exact static
commitment and match readback case/digest. Existing admission still verifies
actual run fields, current protection/source/grant, scheduler and active lease.
Bootstrap and admission both pass before any environment/ready output. Repeat
both after environment approval; prior-job outputs are not authority. Admission
retains contents-read only and no OIDC.

## Migration and remaining gates

Caller/local reusable migrate together. Old `config_digest`/`operation_grant_ref`
dispatch inputs and their environment variables are not aliases. Existing
internal `WorkflowContext`, full `config_digest` and operation grants retain
their meanings; introduce a distinct dispatch context and bootstrap bindings.
Old callers must explicitly migrate; old run grants never authorize a new run.

Default operational bindings continue to refuse before outputs/OIDC. Actual
GitHub authentication, atomic grant consumption, hosting clients, setup/dispatch,
live qualification/cleanup, protected receipts and consumer acceptance remain
separately gated. Tests exercise actual canonical validation/admission with
synthetic independent authority and cannot qualify live administration.
