# neutral-product-pin — delta

ONE `## ADDED` REQUIREMENT, and no existing requirement is modified. The
capability already obliges a consuming repository to RUN strict validation
through the pin's `consumer_entrypoint:` rather than off `PATH` (*A consuming
repository runs OpenSpec validation only through the pinned entrypoint, so a
PATH binary cannot affect the gate*). That requirement settles WHICH BINARY
ANSWERS, and its reason is that an ambient installation must not be able to
change a verdict.

**IT DOES NOT SETTLE WHICH VERDICT IS THE REPOSITORY'S, AND THE TWO COMMANDS DO
NOT RETURN THE SAME ONE.** The entrypoint reconciles the tool's report against
the pin's own ratified `dispositions:`; the raw tool cannot, and so returns a
FALSE RED on a finding this corpus has already adjudicated. A repository can
satisfy the existing requirement completely and still write a gate step that can
never go green. This delta adds the rule for what a WRITTEN ASSERTION must name,
and it is placed in this capability because the pin, the entrypoint and the
dispositions are all this capability's own.

Nothing about the disposition mechanism changes. It works, and the requirement
leans on it.

## ADDED Requirements

### Requirement: A claim of corpus-wide OpenSpec validation names the adjudicated entrypoint, never the raw tool
A GATE STEP, TASK BOX, CHECKLIST ITEM, RUNBOOK STEP, REVIEW RECORD, AGENT INSTRUCTION OR OTHER EVIDENCE RECORD that asserts CORPUS-WIDE OpenSpec validation SHALL name the consuming repository's `consumer_entrypoint:` invocation — for `openxFactory`, `scripts/validate-openspec-cli-pin.py --all` — and SHALL NOT name the raw `openspec validate --all --strict`.

THE TWO COMMANDS ARE NOT TWO ROUTES TO ONE VERDICT, and this is the whole
reason. The pinned CLI is a FOREIGN JUDGMENT about a LOCAL corpus. Where the two
genuinely disagree because the tool cannot read a convention this corpus has
RATIFIED, the disagreement is recorded as an enumerated, cited, authority-granted
DISPOSITION in the pin file, and THE ENTRYPOINT IS THE ONLY READER THAT APPLIES
IT. The raw tool has no access to the pin, does not know the disposition exists,
and reports the finding as a blocking ERROR. Its verdict is therefore not a
weaker form of the repository's verdict but a DIFFERENT ONE, taken by a reader
the repository has not authorized to take it.

A BOX THAT NAMES THE RAW COMMAND IS UNSATISFIABLE BY CONSTRUCTION FOR AS LONG AS
ANY RATIFIED DISPOSITION STANDS, and that is a defect in the box and not in the
corpus. Read literally it demands a green exit the adjudicated gate does not
owe; the only edit that would produce one is to revert the ratified decision the
disposition protects. So the box asks for an act the corpus forbids, while the
repository's actual gate is green — and a reader who trusts the box concludes
the corpus is broken.

THE OBLIGATION IS ON THE ASSERTION, NOT ONLY ON THE RUN. A consuming repository
already SHALL invoke strict validation only through the entrypoint; this
requirement reaches what a gate, a task list, a runbook step, a review record or
an agent instruction WRITES DOWN as the thing to run and as the evidence of a
green corpus. The two are separable and both are owed: a repository whose
continuous integration calls the entrypoint correctly, while its task boxes name
the raw command, has a correct gate and an undischargeable record of it.

A NARROWED CLAIM IS NOT A CORPUS-WIDE ONE and is not reached by this
requirement. A record naming the validation of ONE change states something about
that change; only a claim about the WHOLE corpus asserts the adjudicated gate's
verdict. A narrowed run STILL APPLIES the dispositions it matches — the
requirement that governs them says so — and what it cannot do is decide
STALENESS, because "this finding no longer occurs" is a claim about the whole
corpus. Its green is therefore evidence about the items it opened and never an
audit of the list.

WHERE A LITERAL RAW INVOCATION IS ALREADY WRITTEN INTO RATIFIED OR ARCHIVED TEXT
IT IS NOT EDITED BY THIS REQUIREMENT. An archived packet's record is frozen and a
ratified clause is amended only by its own instrument, so the remedy for an
existing box is the one its own packet's contingency provides — the reserved
DEFERRED marker, naming the live disposition as its reason — and this requirement
governs what is WRITTEN NEXT.

#### Scenario: A task box asserts a green corpus by naming the raw command
- **WHEN** a gate step or task box records corpus-wide OpenSpec validation as its evidence and names `openspec validate --all --strict`
- **THEN** the box is defective, because that command cannot read the pin's dispositions and therefore cannot return the repository's own verdict
- **AND** the remedy is to name the `consumer_entrypoint:` invocation, never to delete the disposition, loosen it, or revert the ratified decision it protects

#### Scenario: A box naming the raw command meets a standing disposition
- **WHEN** such a box is read while a cited, ratified disposition stands against a finding the pinned tool still reports
- **THEN** the box is unsatisfiable by construction, the only edit producing its green exit being one the corpus forbids
- **AND** the adjudicated gate's green verdict at the same head is the repository's verdict, and the box's red is a fact about the box

#### Scenario: A reader asks whether naming the wrapper lowers the bar
- **WHEN** it is objected that naming the entrypoint substitutes a suppressor for a check
- **THEN** the objection is answered by the entrypoint's own refusals: a finding no in-scope disposition covers FAILS the run, and a disposition matched by no finding in a whole-corpus scan REFUSES it as stale
- **AND** those are the standing properties of *A dispositioned finding is cited, upgrade-coupled, and refused when stale* rather than new tolerances, so the adjudicated verdict is strictly MORE INFORMATIVE than the raw one, and more permissive in EXACTLY ONE respect and no other — the findings this corpus has itself NAMED, CITED AND RATIFIED against, which is the whole purpose of the mechanism and not a leak in it

#### Scenario: A record names the validation of one change
- **WHEN** an evidence line records that a single named change validated strictly
- **THEN** it is a narrowed claim and this requirement does not reach it
- **AND** a narrowed run decides no staleness and is never reported as an audit of the corpus

#### Scenario: A gate is correct while its task list is not
- **WHEN** a repository's required check invokes the pinned entrypoint but its task boxes and runbook steps name the raw command
- **THEN** the obligation is unmet, the requirement reaching the written assertion and not only the executed run
- **AND** the correct gate is not a defence, because the record is what a later reader acts on
