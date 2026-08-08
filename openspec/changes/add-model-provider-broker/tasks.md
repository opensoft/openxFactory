# Tasks: add-model-provider-broker

## 0. Ratification (blocking)

- [ ] 0.1 Brett answers the three open questions in the proposal — chiefly
      whether openProfiler DISPATCHES the provider call or VENDS a token.
      The binding shape and the whole trust story follow from that one.
- [ ] 0.2 openProfiler declares its CLI surface. Nothing below hardcodes it;
      the binding carries the argv template precisely so this can land first.

## 1. The binding (implementable now)

- [ ] 1.1 A `model-provider-binding` record: id, label, credential reference,
      auth kind (`api_key` | `oauth`), broker invocation. No secret field
      exists in the shape — not optional, ABSENT, so no code path can
      populate one.
- [ ] 1.2 Settings surface: list, add, edit, remove bindings. Read-back
      discloses the binding and states plainly that the credential lives in
      the broker.
- [ ] 1.3 A credential hand-off that retains nothing: value to the broker's
      stdin, reference back, and a test that greps the whole checkout and
      every response for the value afterwards.

## 2. The port (implementable now, inert until 0.2)

- [ ] 2.1 A broker-backed `WorkbenchModelPort` that shells out to the
      declared invocation for `catalog()` and, once the port grows one, for
      dispatch.
- [ ] 2.2 Wire `serve.py`'s `model_port_factory` to build it from the
      configured binding; unconfigured stays exactly the posture it is now.
- [ ] 2.3 Map every broker failure — missing, non-zero, timeout, malformed,
      oversize — onto the existing fixed redacted refusal, distinct from an
      empty answer.

## 3. Verification

- [ ] 3.1 No provider SDK import, endpoint, credential or secret name enters
      this repository (the existing structural test extends to the new code).
- [ ] 3.2 The unconfigured posture is byte-for-byte what it is today.
