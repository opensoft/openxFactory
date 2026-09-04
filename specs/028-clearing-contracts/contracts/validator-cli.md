# Interface contract: `scripts/validate-clearing-dispatch.py`

**Feature**: 028-clearing-contracts | **Date**: 2026-09-03

The canonical validator IS the control, not a description of one. This file is
its external interface: what it is invoked as, what it prints, what it returns,
and the CLOSED set of refusal codes it may emit — each traced to the ratified
sentence it discharges.

## Invocation

```text
python3 scripts/validate-clearing-dispatch.py [REPO_PATH] [--strict]
```

- No argument: SELF-TEST ONLY. Adjudicate the packaged corpus at
  `contracts/clearing/examples/` — every positive validates clean, every
  negative fails for its declared `# expected_failure:` code, and every closed
  refusal code is red-proven by at least one fixture.
- `REPO_PATH`: additionally sweep that tree for real artifacts whose top-level
  `kind` is one of the five family kinds, and validate them. Zero real artifacts
  is the EXPECTED state until a clearing implementation writes its first record,
  and it is reported as a note rather than a finding.
- `--strict`: warnings become errors.

## Output and exit codes

Lines are printed notes first, then warnings, then errors, then a one-line
summary:

```text
note  <fact about the run>
WARN  [<code>] <message>
ERROR [<code>] <message>

validate-clearing-dispatch: N error(s), M warning(s)
```

| exit | meaning |
|---|---|
| `0` | no errors (and, under `--strict`, no warnings) |
| `1` | findings |
| `2` | harness failure — schemas unloadable, the pinned openXwallet gitlink absent, a path that does not exist |

A harness failure is `2` and never `0`: an unreadable dependency is not a check
that passed. The pinned reader's absence prints the remedy verbatim
(`git submodule update --init openXwallet`) and REFUSES rather than deriving keys
with arithmetic of its own — one derivation, one place.

## Notes the CI gate asserts POSITIVELY

A green check that opened nothing is a vacuous pass, so the gate greps for facts
the run can only print if it did the work:

```text
note  pinned openXwallet decoders read from openXwallet/scripts/validate-openxwallet.py
note  permitted-operations register read: contracts/clearing/permitted-operations.registry.yaml (1 registered operation)
note  self-test: N packaged record(s) validated, M negative fixture(s) refused
note  K/K closed refusal codes red-proven
note  repo scan (<path>): N artifact(s) checked
```

## Closed refusal codes

The validator's `REFUSAL_CODES` constant. Each MUST be probed by a packaged
negative fixture; `clearing-refusal-code-without-probe` fires otherwise.

| code | ratified basis |
|---|---|
| `clearing-manifest-field-missing` | *"a missing or empty declared field MUST refuse the request with the field named"* — the ten-field completeness rule. |
| `clearing-manifest-file-hash-missing` | *"a bundle carrying selected files without their hashes … is refused"*. |
| `clearing-manifest-hash-not-byte-tagged` | `add-cpc-clearing-boundary`: *"a per-file content hash … using the canonical JSON construction … MUST be refused as a category error"*. |
| `clearing-manifest-expired` | *"A request whose expiration has passed is refused rather than served"* — *"recorded as an expiry refusal rather than a transient failure"*. |
| `clearing-manifest-digest-construction` | *"it MUST use the digest construction already in force for the estate; a new construction MUST NOT be defined"* — a manifest digest whose `construction` is not `xfc-jcs-sha256-1` or whose `subject` is not the admitted manifest subject. |
| `clearing-unregistered-operation` | *"a sealed request declares an operation id with no entry in the register … refused with the unknown operation named"*. |
| `clearing-lane-not-permitted` | *"a sealed request's declared runner group or dispatch label is not one the operation's register entry permits"*. |
| `clearing-bundle-disagrees-with-register` | `add-cpc-clearing-boundary`: *"Where a bundle's copy disagrees with the register entry, THE REGISTER GOVERNS: the request SHALL be refused and the disagreement recorded"*. |
| `clearing-origin-signature-missing` | `add-cpc-clearing-boundary`: a registered producer presenting hosted provenance alone — *"the refusal MUST name the missing origin signature rather than report field (10) as present"*. |
| `clearing-origin-signature-invalid` | *"the origin signature is absent, malformed, or does not verify against the registered key → the request MUST be refused"*. |
| `clearing-origin-signature-partial` | *"a partial signature MUST NOT be reported as a signed manifest"* — `covered_fields` short of all ten. |
| `clearing-register-member-unratified` | *"ADDING AN OPERATION SHALL BE A GOVERNED CONTRACT CHANGE … and SHALL NOT be a workflow edit"* — the closure refusal. |
| `clearing-register-entry-incomplete` | the entry-declaration list: id, semantics, class constraints, worker profile, lanes, output schema, repository-affecting output. |
| `clearing-readonly-entry-claims-effect` | *"An operation that declares NO repository-affecting output SHALL be prevented from having one"*. |
| `clearing-report-carries-a-verdict` | design D9 / *"The report is mistaken for a readiness decision → it MUST be refused"*. |
| `clearing-report-environment-not-allowlisted` | *"The environment echo SHALL be a name allowlist and SHALL NOT be a wholesale environment dump"*. |
| `clearing-report-lane-reported-as-observed` | *"the group and label MUST be reported as DECLARED rather than as observed group membership"*. |
| `clearing-record-refusal-ground-unknown` | *"a ground absent from that enumeration MUST be added by a governed change rather than recorded as free text"*. |
| `clearing-record-cleared-with-refusal` | the shape's own consistency: a cleared dispatch carrying a refusal ground, or a refused one carrying none. |
| `clearing-record-disposal-unattested` | `add-cpc-clearing-boundary`: *"A dispatch record whose disposal field is absent or empty SHALL NOT be read as evidence of a clean host"*. |
| `clearing-record-policy-field-reported-verified` | *"those fields MUST be reported as policy-checked against the register AND they MUST NOT be reported as provider-verified"*; and the origin-signature outcome *"MUST NOT be reported inside the provider-verified set"*. |
| `clearing-attestation-expected-set-not-per-group` | *"THE EXPECTED ALLOWLIST SHALL BE COMPUTED PER GROUP, not once for the estate"*. |
| `clearing-attestation-dark-lane-as-breach` | *"AN ENUMERATED MEMBER WITH NO OBSERVED ALLOWLIST ENTRY is NOT a breach … Treating an unreachable lane as a breach would make the attestation red for a condition that is strictly safer"*. |
| `clearing-attestation-overclaims-completeness` | *"the claim MUST be stated at the strength that attestation supports, distinguishing the pre-admission narrower claim from the post-admission full claim"*. |
| `clearing-schema-identity-missing` | house rule: every schema in a family declares its dialect and an absolute `$id`. |
| `clearing-refusal-code-without-probe` | house rule: a closed refusal code with no packaged fixture is a code nobody has seen fire. |
| `clearing-negative-wrong-reason` | house rule: a negative fixture that fails for a code other than the one it declares. |

## What the validator deliberately does NOT do

- It does not contact a provider API. Provider-side resolution is the CLEARING
  IMPLEMENTATION's obligation (`opensoft/xFactory`); the neutral validator checks
  that a record CARRIES the resolved value beside the claimed one and that a
  policy-checked field is not reported as provider-verified. Asserting a live API
  answer from a contract validator would be a second implementation of a check
  the ratified text places on the clearing workflow.
- It does not evaluate revocation at the moment of clearing. The factory-identity
  register declares that unrealizable until a projection path exists, and any
  statement to the contrary is refused by that capability's own scenario. The
  validator reads the register's declared `revocation_staleness_bound` and reports
  it as a note.
- It does not verify a sealed RETURN. No return shape ships in this realization.
