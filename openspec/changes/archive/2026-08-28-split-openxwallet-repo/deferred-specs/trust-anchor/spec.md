# trust-anchor Specification

Deltas here are declared RELATIVE TO the OUTCOME of the active ratified change
`add-trust-anchor`: `trust-anchor` is NOT in `openspec/specs/`, and the
requirement below is one of that change's eight `ADDED` requirements. Per
`openspec/specs/release-realization/spec.md:64-79`'s ordered-delta rule the delta
references that change and restates the target requirement's full text as that
change will promote it, plus this change's modification. **One honesty note on
that rule:** its letter covers a requirement already MODIFIED by an active
ratified change, and these requirements are ADDED — so the rule is applied by
PARITY, and the parity is declared here rather than implied.

The modification is a DANGLING CROSS-CORPUS REFERENCE, not a code change: after
`split-openxwallet-repo`'s shed, the composition clause names a capability this
corpus no longer holds and supplies no resolution path. The code that realizes
the amended text is P3's surface, not the requirement's own words
(`scripts/validate-trust-anchor.py:322-323` resolving the registry from the pin,
and rule (f) at `:1146-1176` failing closed in place of today's bare file-absent
exit at `:2582-2586`). The composition is otherwise unchanged: two registries,
one custody question, still checked at run time.

## MODIFIED Requirements

_Declared relative to `add-trust-anchor`'s ADDED text (parity with `release-realization`'s ordered-delta rule, as the proposal states)._

### Requirement: Declared chain custody bounds what a certificate evidences

openxFactory SHALL require every anchor and certificate record to DECLARE
the custody of its private key from a defined set, and SHALL derive what
the certificate EVIDENCES from that declaration rather than from the
certificate's own contents, composing with the `openxwallet` capability's
ratified rule, consumed from `opensoft/openXwallet` at the pin recorded in
`contracts/openxwallet-pin.yaml`, that custody caps what a signature evidences
instead of restating a second custody model. A key readable by the host that uses it evidences that the
HOST acted; only custody isolating the key from that host evidences that
the named holder acted. A certificate whose declared custody is host-held
SHALL NOT be presented as, or accepted for, an assurance that requires
hardware-bound custody, and raising assurance is a custody change rather
than a claim.

#### Scenario: a host-held key is offered for hardware-bound assurance

- WHEN a certificate declaring host-held custody is offered for an authority requiring hardware-bound custody
- THEN the request is refused with the custody ceiling named
- AND the refusal names custody rather than the certificate's contents

#### Scenario: custody is undeclared

- WHEN a certificate record carries no custody declaration
- THEN it evidences the weakest member of the defined set
- AND it may not hold authority above that member

#### Scenario: the audit says what was evidenced

- WHEN an act authenticated by a certificate is audited
- THEN the record carries the custody in force at the time of the act
- AND a reader can tell whether the holder or its host was evidenced

#### Scenario: the pinned wallet checkout cannot answer the custody question

- WHEN the pinned openXwallet checkout is uninitialized or its custody-registry digest disagrees with the pin
- THEN the custody question is refused rather than resolved
- AND the refusal names the pin file and the initializing command, rather than reporting an empty custody set
