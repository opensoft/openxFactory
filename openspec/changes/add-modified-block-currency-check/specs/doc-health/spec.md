# doc-health Specification Delta

## ADDED Requirements

### Requirement: Currency of an active change's MODIFIED requirement blocks
The modified-block currency family SHALL compare every ACTIVE change's
`## MODIFIED Requirements` block against the requirement as the promoted
specification CURRENTLY states it, and report what the block does not carry —
reporting against the active delta's own path, while the change can still be
edited.

The obligation being checked belongs to `document-lifecycle` ("A MODIFIED
requirement block restates the requirement as canon currently states it"); this
requirement defines only how doc-health checks it, in the same by-reference
relationship promotion fidelity and duplicate packet already have with that
capability's obligations.

**This family answers a question the promotion fidelity family cannot, and it
asks it at the only time the answer is cheap.** That family compares an
ARCHIVED delta to canon, and after an archive act canon IS the delta — a block
that dropped seven scenarios and canon that now lacks them agree perfectly, so
that family reports nothing. The comparison that can see the class is between
an ACTIVE delta and the canon it has not yet replaced, which is a different
document pair read at a different moment, and is why this is a separate family
rather than a wider reading of that one. It is also why the loss is not caught
by counting: the file-level scenario count can stay flat while a requirement
goes from eight scenarios to one, because a change's own ADDED requirement
offsets what its MODIFIED block drops.

The family SHALL implement three comparison arms over one document pair, and
SHALL report them as distinct finding classes so that a precise signal is never
buried in an editorial one:

- **Scenario-title completeness.** Every `#### Scenario:` title the promoted
  requirement carries SHALL appear as a scenario title in the block. This arm
  reports DELETION at the granularity the defect actually occurs at, its inputs
  are short titled strings rather than prose, and it is the arm that carries
  this family's gate.
- **The carriage ledger.** Every body sentence of the promoted requirement, and
  every bullet of a scenario the block restates, SHALL be reported where the
  block does not carry it verbatim after whitespace normalization. This arm
  CANNOT distinguish a deliberate rewording from stale text, and SHALL NOT be
  read as claiming it does: it is the list a reviewer reads to confirm that each
  divergence is one the change intended. It SHALL emit at most one finding per
  requirement, listing the units, rather than one finding per unit.
- **Title resolution and the two-writers rule.** A MODIFIED block whose
  capability and requirement title resolve to no promoted requirement SHALL
  resolve instead to a requirement an active sibling change ADDS or RENAMES, and
  that sibling SHALL be referenced by the modifying change's own proposal, as
  `release-realization`'s "Ordered deltas and branch vocabulary" already
  requires. Where a title resolves to neither canon nor an active sibling, the
  block SHALL be reported. Where two active changes carry a MODIFIED block for
  ONE promoted requirement, the later SHALL be measured against the earlier
  change's outcome rather than against canon, and the earlier change's
  additions SHALL be present in the later block.

**Matching SHALL be verbatim after whitespace normalization, and by nothing
else.** A unit is carried where it appears in the block character-for-character
once runs of whitespace are collapsed to a single space and leading and
trailing whitespace is stripped — the normalization that makes a re-wrapped
paragraph compare equal to the same paragraph wrapped differently, and no
normalization beyond it. A similarity or near-match rule MUST NOT be used: it
would silently accept a clause whose meaning had been reversed, which is one of
the defects on this family's record, and the corpus has already ruled against
resemblance as an identity test in the duplicate packet family.

**A deliberate deletion SHALL be declared in the delta, and the declaration
SHALL be read there.** A dated bold note inside the MODIFIED block, naming each
deleted scenario by its exact title and quoting each deleted body unit,
suppresses exactly the units it names and nothing else. That is not a new
marker invented for the rule: the corpus already writes dated bold notes inside
MODIFIED blocks naming lost scenarios verbatim in backticks — the `CORRECTED
2026-08-25 ON BRETT'S RULING` note in `doc-health`'s own "Deterministic check
families" is one — and this makes an existing convention machine-read rather
than adding a second one. A recorded disposition in the aggregation checkout's
`health/dispositions.yaml` naming THIS family, with a `cite`, optionally
narrowed to one requirement, SHALL suppress the findings it names; an entry
naming another family MUST NOT suppress this family's findings. Nothing else
suppresses.

**This family SHALL measure the checked-out tree.** The live-`main` basis this
capability defines applies to the promotion fidelity family alone, and it would
be actively wrong here: an active change lives on a branch, so a family that
read `main` would measure a delta that `main` does not carry against canon that
the branch may have moved.

**This family SHALL be advisory at launch, in both halves of what that means.**
Every finding it emits carries `warning` severity for the scenario-completeness
and title-resolution arms and `info` for the carriage ledger, so no `--fail-on`
configuration reds on it; and the family is deliberately absent from
`FAMILY_RESOLUTION`, so its findings are NOT classified `contested` — a
contested finding that resolves without a citation becomes an `error` under this
capability's uncited-resolution rule, which would gate the family through the
back door on the first block anyone corrected. Raising the scenario-completeness
arm to `error` and adding the contested classification are ONE later decision
taken together by ruling, and SHALL follow the discharge of the standing
population rather than precede it. **No flip is proposed for the carriage
ledger.** Its population is standing by construction — every legitimate
MODIFIED block edits something — so it is an editorial band and not a gate in
waiting, and saying so is what keeps a permanently yellow row from teaching
readers to skip the section.

#### Scenario: An active block drops a scenario the requirement keeps
- **WHEN** an active change's MODIFIED block restates a promoted requirement and omits a scenario title that requirement currently carries, with no declaration naming it
- **THEN** the run MUST emit a `warning` finding against the active delta's own path, naming each omitted scenario title and the promoted spec it was read from
- **AND** the finding MUST NOT cause a run configured `--fail-on error` or `--fail-on critical` to fail

#### Scenario: A deletion is declared in the delta
- **WHEN** the MODIFIED block carries a dated note naming a scenario by its exact title, or quoting a body unit, as deliberately deleted
- **THEN** that scenario or unit MUST NOT be reported
- **AND** the suppression MUST extend to exactly the units named and to no others

#### Scenario: A block does not carry canon's body text
- **WHEN** an active MODIFIED block does not carry a body sentence of the promoted requirement, or a bullet of a scenario it restates, verbatim after whitespace normalization
- **THEN** the run MUST emit one `info` finding for that requirement listing every uncarried unit
- **AND** the finding MUST NOT assert that the divergence is unintended, the arm having no means to distinguish a rewording from stale text

#### Scenario: Two active changes modify one requirement
- **WHEN** two or more active changes carry a MODIFIED block for the same capability and requirement title
- **THEN** the later change's proposal MUST reference the earlier change, and its block MUST be measured against that change's outcome rather than against canon
- **AND** an addition the earlier block makes that the later block does not carry MUST be reported against the later delta's path

#### Scenario: A MODIFIED title resolves to an active sibling's addition
- **WHEN** a MODIFIED block names a requirement canon does not carry, and an active sibling change ADDS or RENAMES that title, and the modifying change's proposal references that sibling
- **THEN** the block MUST NOT be reported, the promoted requirement being pending rather than absent

#### Scenario: A MODIFIED title resolves to nothing at all
- **WHEN** a MODIFIED block names a capability and requirement title carried neither by the promoted spec nor by any active change's ADDED or RENAMED block
- **THEN** the run MUST emit a finding naming the unresolved title, a block modifying nothing being a block whose promotion adds text nobody reviewed as an addition

#### Scenario: A finding is dispositioned
- **WHEN** `health/dispositions.yaml` carries an entry naming this family, a repository, an active delta path, and a `cite`
- **THEN** findings on that path MUST be suppressed, or only the named requirement's findings where the entry carries a `requirement` key
- **AND** an entry without a `cite`, or an entry naming another family, MUST suppress nothing

#### Scenario: No active change in scope carries a spec delta
- **WHEN** no repository in the run's scope has an active change carrying a `## MODIFIED Requirements` block
- **THEN** the family MUST be reported as skipped with its reason, never silently omitted
