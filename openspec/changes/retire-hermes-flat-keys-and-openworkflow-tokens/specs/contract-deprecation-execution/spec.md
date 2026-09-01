# contract-deprecation-execution Specification (delta)

## ADDED Requirements

### Requirement: A deprecation is EXECUTED at the major it targets, or its entry is RESTATED with the reason it stays
A deprecation entry in `docs/contract-versioning-policy.md` § Deprecations Currently In Force SHALL, at the release that reaches its declared removal target, either EXECUTE — the removal lands and the entry moves to § Deprecations Executed — or be RESTATED, carrying a new removal target that lies ahead of the declared bundle together with the recorded reason the removal was not taken. An entry MUST NOT survive its own removal target unchanged, and MUST NOT be deleted.

The mechanism already forbids deletion, and states why: *"a deprecation
silently disappearing from a policy document is indistinguishable from one that
was never honoured."* This requirement adds the case the mechanism has no
vocabulary for. Today the section spells only two states — `Warned since X;
removal target Y` for an entry in force, `Deprecated at X, removed at Y` for one
executed — and there is no third spelling for an entry that reached its target
and was deliberately not executed. Three entries have been in exactly that state
since `contract-v2.0` shipped on 2026-08-27, and the absence of a spelling is why
nothing said so.

THE RESTATED FORM PRESERVES THE PARSEABLE TAIL. Every bullet in the section ends
in the same `removal target contract-vX.Y` formula, a convention
`018-openxwallet-deprecation-minor` deliberately preserved, and a restatement
SHALL preserve it, so a later reader — human or check — recovers a target from
every bullet. A restatement that leaves no parseable target converts a
deprecation into an unenforceable one, which the *Deprecating (minor)* class
already forbids by requiring the removal version to be stated.

THE REASON IS PART OF THE ENTRY, NOT A COMMIT MESSAGE. The reason a removal was
not taken is read by a consumer deciding whether to migrate, at a version the
commit that made the decision is invisible from. `health/dispositions.yaml` is
NOT the place for it: that file lives at the aggregation root, suppresses
doc-health findings by path, and is unreachable by a consumer reading a pinned
policy document.

#### Scenario: The removal lands at the target
- **WHEN** a release cut removes the shape a deprecation entry announced, at the version that entry named
- **THEN** the entry MUST move from § Deprecations Currently In Force to § Deprecations Executed
- **AND** the Executed row MUST carry the shape removed enumerated, the version it was REMOVED at, which release served the full minor of warnings, how the conformance-validator clause is discharged, a migration path a post-removal reader can still follow, and the closing `Deprecated at X, removed at Y.`

#### Scenario: The target arrives and the removal is not taken
- **WHEN** the declared bundle reaches or passes a deprecation entry's removal target and the removal has not landed
- **THEN** the entry MUST be restated in the same cut: a new removal target ahead of the declared bundle, in the section's `removal target contract-vX.Y` formula, plus the recorded reason
- **AND** leaving the entry naming the spent target MUST be treated as a defect of that cut rather than as a neutral omission

#### Scenario: An entry is quietly dropped
- **WHEN** a cut would delete a deprecation entry from the section without landing its removal
- **THEN** it MUST be refused, because a deleted entry and a dishonoured one read identically to a consumer upgrading across the version

#### Scenario: A restatement states no target
- **WHEN** a restatement leaves a bullet from which no `removal target contract-vX.Y` parses
- **THEN** the restatement is incomplete, because the *Deprecating (minor)* class requires the removal version to be stated and an unstated one is unenforceable

### Requirement: A deprecation entry is written from the REFUSAL LIST, and an unwarned shape is not phased
A deprecation entry SHALL enumerate every shape the announced removal would refuse, read off the code that will do the refusing rather than off the prose that announced it; and where a shape the removal would refuse has produced NO deprecation warning against any supported consumer, that shape MUST NOT be removed at the next major, because the Breaking class's "at least one full minor release where the old shape produced deprecation warnings" is unmet for it.

An entry written from memory rather than from the refusal list under-declares
its own scope, and a consumer reading it cannot tell which of its own bytes the
major will refuse. `add-binding-consumer-identity` articulated this and guarded
against it in its own entry: *"The entry is written from the REFUSAL LIST rather
than from memory: every shape the current major accepts and the next one refuses
owes its minor of warnings, and without that a reader at the major cannot
demonstrate this section's own precondition was met and the requiredness becomes
unauditable."* This requirement promotes that rule out of one entry's prose.

A WARNING THAT CANNOT FIRE IS NOT A WARNING SERVED. The precondition is about
what consumers were TOLD, not about what a validator contains. Where the branch
carrying the warning is unreachable for the whole supported population, the
population was never warned, and manufacturing the precondition retroactively —
by asserting that the warning existed in the source — is the failure the clause
exists to prevent. The remedy is a deprecating minor that makes the warning
actually fire, and only then a major that refuses.

#### Scenario: The entry names fewer shapes than the code refuses
- **WHEN** a deprecation entry enumerates a subset of the shapes the removal's own refusal list carries
- **THEN** the entry MUST be rewritten from the refusal list before the removal lands
- **AND** the rewrite is owed whether or not the removal is taken, because the under-declaration is a defect of the entry rather than of the cut

#### Scenario: The warned shape and the refused shape are the same
- **WHEN** every shape a removal would refuse is a shape the deprecation warning has actually fired on across a full minor
- **THEN** the Breaking class's phasing precondition is served and the removal MAY be taken at the next major, with the serving release named in the Executed row

#### Scenario: The warning is dead code for the supported population
- **WHEN** the branch that emits a deprecation's warning is unreachable for every supported consumer, measured by running the validator against each of them
- **THEN** the shape that branch was meant to warn about MUST NOT be refused at the next major
- **AND** the entry MUST record that measurement as the reason it stays in force, and MUST name the deprecating minor it owes — a cut that makes the warning fire on the shape a later removal would refuse

#### Scenario: A removal is proposed on a warning that exists only in source
- **WHEN** the case for a removal's phasing rests on the warning being PRESENT in the validator rather than on it having been EMITTED
- **THEN** the case is insufficient, and the measurement — the validator run against every supported consumer — is what settles it

### Requirement: The `hermes` flat-key FALLBACK READ is removed at contract-v3.0 and the co-resident flat KEYS are not
The `hermes` flat-key FALLBACK READ in the canonical domain-factory conformance validator — the branch that resolves layer overlays and display names from flat keys under `hermes:` when `hermes.layers` is absent — SHALL be removed at `contract-v3.0`, and openxFactory's own domain-starter generator SHALL stop emitting the deprecated flat keys into newly instantiated domain repositories; the CO-RESIDENT flat keys themselves SHALL NOT be refused at that major, and their entry SHALL remain in force, restated, with the reason recorded.

TWO RETIREMENTS WERE AVAILABLE AT VERY DIFFERENT PRICES AND EXACTLY ONE IS
TAKEN. The fallback read is the compatibility surface: it exists so a
`layers`-less stack still resolves. The refused shape is precisely the warned
shape — a stack with no `hermes.layers` is the only stack the warning fires on —
so the Breaking clause's precondition is served, forty-plus minors over, and the
removal refuses nobody: all five supported consumers declare `hermes.layers`.

The KEYS are the other retirement and it is not taken. All five supported
consumers carry flat keys ALONGSIDE `hermes.layers`, and that co-resident shape
has never produced a warning against any of them, because the warning sits in
the `else` branch taken only when `layers` is absent. Refusing the keys would
therefore be an unphased narrowing owing its own deprecating minor first.

THE ENTRY IS REWRITTEN FROM THE REFUSAL LIST IN THE SAME CUT, whichever half
executes. The policy text names five keys; the validator's legacy map carries
nine; the starter emits three more that appear in neither list. An entry that
under-declares its own scope by seven keys is a defect independent of the split.

#### Scenario: A stack declaring `hermes.layers` meets the new major
- **WHEN** a domain `stack.yaml` declaring `hermes.layers` is validated at `contract-v3.0`
- **THEN** it MUST validate exactly as it did before, with no new error and no new warning
- **AND** this MUST hold for every supported consumer, because all five declare `layers` and none exercises the removed fallback

#### Scenario: A stack with no `hermes.layers` meets the new major
- **WHEN** a domain `stack.yaml` carrying only flat keys under `hermes:` and no `hermes.layers` is validated at `contract-v3.0`
- **THEN** it MUST be refused, where at the prior bundle it produced a legacy-flat-keys warning and resolved through the fallback
- **AND** a consumer still pinned below `contract-v3.0` MUST keep validating unchanged, because compatibility flows from the domain repo and no new release retroactively invalidates an old pin

#### Scenario: A stack carries `hermes.layers` and redundant flat keys together
- **WHEN** a domain `stack.yaml` declares `hermes.layers` and ALSO carries flat keys that agree with it
- **THEN** it MUST still validate at `contract-v3.0` — no refusal, and no new warning, the co-resident shape being exactly the one whose refusal is not phased
- **AND** the flat keys remain inert: no code reads them while `layers` is present

#### Scenario: The starter generates a new domain repository
- **WHEN** the domain-starter generator instantiates a new domain repository at `contract-v3.0` or later
- **THEN** the generated `stack.yaml` MUST carry no deprecated flat key, and no comment naming a spent removal target
- **AND** an already-generated repository MUST NOT be edited by this change, because nothing refuses what it carries

#### Scenario: The In Force entry after the cut
- **WHEN** `contract-v3.0` lands
- **THEN** the flat-key entry MUST remain in § Deprecations Currently In Force, enumerating every key the refusal list would carry, carrying a restated removal target ahead of the declared bundle, and carrying the recorded reason — the warning has been dead code for the whole supported population, so the refusal is unphased and owes a deprecating minor first
- **AND** § Deprecations Executed MUST carry a separate row for the fallback read, which did execute

#### Scenario: A realization DELETES the fallback arm instead of replacing it
- **WHEN** a realization removes the flat-key fallback arm without putting an explicit refusal in its place
- **THEN** it MUST be rejected, because the missing-role errors sit INSIDE the branch taken when `hermes.layers` IS declared, so a `layers`-less stack would fall through with an empty layer map and produce no finding at all
- **AND** that outcome is a silent WIDENING at a major — the opposite of the retirement — which is why the removal of a compatibility read owes a stated replacement behaviour and not merely a deletion

#### Scenario: The refusal list is written by key NAME rather than by key PATH
- **WHEN** the flat-key refusal list is enumerated as bare key names rather than as keys under the `hermes:` block
- **THEN** it MUST be rejected, because `domain_overlay` is also a live, non-deprecated key under `omnigent:` that every supported consumer declares and the validator reads
- **AND** a list that swept it in would refuse, at a major and with no warning ever served, a shape the whole supported population legitimately carries

#### Scenario: A later cut proposes to refuse the keys without the owed minor
- **WHEN** a change proposes refusing the co-resident flat keys at a major without a preceding minor in which the warning fired on the co-resident shape
- **THEN** it MUST be refused, and the restated entry's recorded reason is what makes the refusal citable

### Requirement: The `openworkflow`-prefixed layer/owner token compatibility surface is removed at contract-v3.0
The compatibility branch that gives an `owner_layer` token beginning `openworkflow` its own deprecated-naming warning in the canonical domain-factory conformance validator SHALL be removed at `contract-v3.0`, together with the validator docstring line that advertises it, so that from that major forward such a token carries NO special handling and is evaluated by the same rule as any other `owner_layer` token; and the entry's declared shape SHALL be corrected to the prefix the code actually matches before the removal lands.

THE ENTRY UNDER-DECLARES ITS OWN SHAPE, THE SAME DEFECT AS ENTRY 1 AND ONE
CHARACTER WIDE. The policy entry and the validator docstring both write
`openworkflow_`, with a trailing underscore. The code writes
`token.startswith("openworkflow")`, with none. So `openworkflow`, `openworkflowx`
and `openworkflow-legacy` all take the branch today and are all refused by the
removal, and not one of them is the shape the entry declares. The refusal-list
rule applies here exactly as it applies to the flat keys.

The replacement token is `xfactory`, introduced by `contract-v1.1`, and the
migration was completed years of minors ago: across ten reachable repositories
there is not one `openworkflow`-prefixed `owner_layer` token in a workflow gate.
Every live occurrence of the string is prose — the validator's own deprecation
code, the deprecation records themselves, ideation about the openWorkflow
lineage, archived change packets, and one council record quoting the policy
section. The refused shape is exactly the warned shape, phased since
`contract-v1.1`, so no new deprecation window is owed.

THE BRANCH SHADOWS AS WELL AS WARNS, AND REMOVING IT MOVES TWO CASES IN OPPOSITE
DIRECTIONS. It is an `if` that precedes the general `elif`, so today ANY token
beginning `openworkflow` takes it — including one that resolves perfectly well to
a declared layer. Removing it therefore narrows the unresolvable case and widens
the resolvable one, and both consequences are stated here rather than discovered
later.

THE SEVERITY OF THE GENERAL RULE IS RECORDED AND NOT SETTLED HERE. Promoted
canon states that an `owner_layer` resolving to nothing SHALL be reported as a
validator WARNING; the shipped validator has reported it as an ERROR since
2026-07-03, six days before that requirement was promoted. This change does not
resolve that divergence, because resolving it would move every unresolvable token
and not merely the retired prefix, and that is a different change's subject.

#### Scenario: A gate names an `openworkflow_` token that resolves to nothing
- **WHEN** a workflow gate's `owner_layer` begins `openworkflow` and matches no canonical role and no declared layer id, and is validated at `contract-v3.0`
- **THEN** it MUST no longer receive the deprecated-naming warning, and MUST be reported by the general undeclared-layer rule at whatever severity that rule carries
- **AND** the shape refused is exactly the shape warned since `contract-v1.1`, so no new deprecation window is owed

#### Scenario: A gate names an `openworkflow_` token that IS a declared layer
- **WHEN** a workflow gate's `owner_layer` begins `openworkflow` and its normalized form equals a declared Hermes layer's normalized display name
- **THEN** it MUST validate silently at `contract-v3.0`, where the shadowing branch previously warned it
- **AND** this widening MUST be stated in the Executed row rather than left to be discovered, because a removal that quietly accepts something it used to flag is still a change of behaviour

#### Scenario: A gate names `xfactory`
- **WHEN** a workflow gate's `owner_layer` is the replacement token `xfactory`
- **THEN** it MUST validate exactly as before, unchanged by this removal

#### Scenario: A consumer pinned below the major
- **WHEN** a domain repository pinned below `contract-v3.0` is validated from the checkout it pins
- **THEN** the `openworkflow` branch is still present there and still warns, because a pinned consumer stays valid at its pin and nothing in a new release reaches backwards

#### Scenario: A token carries the prefix WITHOUT the underscore the entry declares
- **WHEN** a workflow gate's `owner_layer` normalizes to `openworkflow`, `openworkflowx` or any form carrying the prefix without a following underscore
- **THEN** it takes the compatibility branch today and is refused by this removal, even though the policy entry and the validator docstring both declare the shape as `openworkflow_`
- **AND** the entry MUST be corrected to the prefix the code matches before the removal lands, under the refusal-list rule, so that a consumer at the major can tell which of its own tokens the major refuses

#### Scenario: The Executed row for the token surface
- **WHEN** `contract-v3.0` lands
- **THEN** § Deprecations Executed MUST carry the row: the token shape removed, `contract-v3.0` as the version it was REMOVED at, `contract-v1.1` named as the release that served the warnings, how the conformance-validator clause is discharged, the migration to `xfactory`, and `Deprecated at contract-v1.1, removed at contract-v3.0.`
- **AND** the entry MUST leave § Deprecations Currently In Force in the same cut
