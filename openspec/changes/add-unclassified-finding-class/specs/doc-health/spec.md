# doc-health Specification Delta

## ADDED Requirements

### Requirement: A modified-block-currency finding its own class map cannot place is itself a finding
The modified-block-currency family SHALL emit exactly ONE ADDITIONAL `warning`
finding per run where its own class map does not place one or more of the
findings that run emitted, naming how many such findings there are and,
verbatim, the rule text of the first of them in the family's own report order,
carrying that finding's repository and delta path and the action line "extend
the class map, or fix the rule text drift". Where the map places every finding
the family emits, no such finding SHALL be emitted.

**A RESIDUAL THE REPORT STATES ONLY IN PROSE IS OUTSIDE EVERY MECHANISM THIS
CAPABILITY HAS.** The family's report block already renders a named residual row
when its class map cannot place a finding, and that row is honest as far as it
goes — it states the count and says the counts above are short by it. But it is
TEXT. It carries no severity, so no `--fail-on` configuration can reach it; it
is not a finding, so "Health report contract"'s requirement that every finding
appear in the ranked plan as a ready-to-stage work item with severity, repo,
path and suggested action does not reach it either; and a report a session works
by its ranked plan is a report in which that row is never worked. The residual
means the family's arms and the map that describes them have drifted apart —
which is a defect in this capability's own tooling, discovered by that tooling,
and it is the one class of report content that currently cannot be handed to
anybody.

**THE ROW STAYS.** This requirement adds a finding beside the residual row and
replaces nothing: the row is what makes the tally sum to the rows it is printed
above, which is the reason it exists, and a reader who has the block in front of
them must not have to reconstruct it from the ranked plan.

**THE NEW FINDING SHALL ITSELF BE PLACED BY THE MAP, in a FIFTH class of the
family's own class registry.** A finding about unplaced findings that were
itself unplaced would be counted by the residual it reports, so the count would
name itself, the next run would report a drift the map had just been extended to
describe, and the tally would still not sum. The fifth class carries the
`warning` band and this requirement's action line, and it is a CLASS rather than
an ARM: it compares no document pair, and "Currency of an active change's
MODIFIED requirement blocks" still states three arms and is untouched by this.

**THE FIFTH CLASS'S PATTERN SHALL BE ANCHORED AT THE START OF THE RULE TEXT.**
This finding QUOTES a rule text the map does not recognize, and that quoted text
may itself begin in the shape of another class — an arm's rule text that drifted
by one word is the likeliest thing the map will fail to place. An unanchored
probe would file this finding under whichever class its quotation resembles,
which is the misfiling the family's existing anchor exists to prevent, on the one
line a reader is asked to trust instead of counting.

**ONE FINDING PER RUN, NOT ONE PER REPOSITORY.** The drift is a single defect in
a single class map compiled once per process, and its remedy is one edit to that
map; emitting it per repository would put the same remedy in an aggregation
run's ranked plan once for every repository in scope while the map is exactly as
wrong as it was. The repository and path it carries are the FIRST unplaced
finding's, so a reader has a document to open, and they are evidence rather than
the subject.

**THE BAND IS `warning`, AND THE FAMILY REMAINS ABSENT FROM
`FAMILY_RESOLUTION`.** `warning` is the band this family's gate-bearing arm
already carries, so a run configured `--fail-on error` or `--fail-on critical` is
unaffected by construction and the family's advisory launch is unchanged. The
absence is load-bearing here rather than incidental: this finding is DESIGNED to
disappear the moment somebody extends the map, and a `contested` classification
would turn that disappearance into an `error` under this capability's
uncited-resolution rule — the check reddening the run that proves it was
answered.

**THIS ADDS NO DETERMINISTIC CHECK FAMILY.** The finding is emitted by the
modified-block-currency family, inside the family's own section, under the
family's own id; the enumeration and its numerals in the "Deterministic check
families" requirement are deliberately untouched and unrestated, and no
`## MODIFIED Requirements` block is owed on any promoted requirement by this
change.

#### Scenario: Every finding the family emits is placed by its map
- **WHEN** a run of the modified-block-currency family emits findings and the class map places every one of them
- **THEN** no additional finding MUST be emitted, the map and the arms agreeing being the state this requirement exists to leave alone
- **AND** the family's rendered class counts MUST still sum to the rows the report prints for it

#### Scenario: A rule text the class map does not place
- **WHEN** a run of the modified-block-currency family emits one or more findings whose rule text no pattern of its class map matches
- **THEN** the run MUST emit exactly one additional `warning` finding naming the number of such findings and, verbatim, the rule text of the first of them in the family's own report order
- **AND** that finding MUST carry the repository and delta path of that first unplaced finding, and the action line "extend the class map, or fix the rule text drift"
- **AND** that finding MUST itself be placed by the map into the fifth class, so that it is never counted by the residual it reports and the rendered counts still sum to the rows

#### Scenario: The warning is worked from the ranked plan
- **WHEN** a report is rendered for a run that emitted the additional finding
- **THEN** the finding MUST appear in the ranked plan as a ready-to-stage work item stating its severity, repository, path and action, on the same terms as every other finding
- **AND** the family's residual row MUST still render in the family's own report block, the row and the finding being two readings of one fact rather than alternatives

#### Scenario: The class map grows the pattern the drift named
- **WHEN** the class map is extended with a pattern that places the rule text the finding named, and the family is run again over the same tree
- **THEN** the additional finding MUST NOT be emitted, and the residual row MUST NOT render
- **AND** the disappearance MUST NOT be reported as an uncited resolution, the family being deliberately absent from `FAMILY_RESOLUTION` and its findings therefore never classified `contested`
