# The council-convening activation runbook — pause, drain, switch, rehearse, activate, roll back

Status: ratified
Ratified by: renew-resolved-council-protocol
Kind: runbook
Repository context: openxFactory

This runbook is the owner's procedure for moving the producer and the consumer
of a council convening from the legacy council protocol to the replacement,
`xfc-resolved-council-1`, together, and for rolling the pair back together. It
realizes design D5 of the ratified change
[`renew-resolved-council-protocol`](../openspec/changes/renew-resolved-council-protocol/design.md)
(ratified 2026-10-03 by Brett Heap): *"During the coordinated change, stop new
commissioning, drain or explicitly cancel old in-flight convenings, switch both
bindings, run the complete conformance rehearsal, then resume commissioning.
Rollback stops intake and restores both prior versions/configurations together;
never interpret new records as old or enable both shapes on one active binding."*
Speckit feature 035 wrote it as task T062, beside the two shapes it uses:
[`protocol-selection.schema.yaml`](../contracts/council-convening/protocol-selection.schema.yaml)
(data-model E11) and
[`activation-evidence.schema.yaml`](../contracts/council-convening/activation-evidence.schema.yaml)
(data-model E12), both in the
[council-convening contract family](../contracts/council-convening/README.md).

**Every act here is an owner act, and this document performs none of them.**
Each act is recorded as one activation-evidence record whose `act` names it. A
record that passes this family's checks is evidence for the owner, never the
act itself.

## What this runbook does not do

- It allocates, publishes and tags no release. The deprecation minor and the
  removal major are their own cuts, and each annotated tag is the owner's act.
- It advances no successor pin, provisions no broker, credential, environment or
  binding, and deploys nothing.
- It gives no command that switches, activates or rolls back anything. Every
  command below reads records and exits; none writes a configuration.
- A green local test run, a green corpus run in one repository, or a record that
  passes `check` is never reported as publication, deployment, activation or the
  other side's conformance (spec User Story 3, scenario 4).

## Before the first act

- **The replacement must be eligible before anything activates.** An `active`
  replacement selection is refused as `replacement_not_admission_eligible` until
  the protocol registry makes the replacement `admission_eligible`, which happens
  at the removal major. Until then a side may select the replacement only in
  `mode: rehearsal`, so steps 1 to 4 can be rehearsed dormant at any reviewed
  provider commit, and step 5 cannot run for real.
- **Both sides pin one provider.** Each side's selection names the same
  openxFactory commit, the same bundle tag, and the same raw SHA-256 of
  `contracts/council-convening/conformance/index.json` at that commit, the corpus
  digest.
- **The bindings are provisioned, one per seat.** Under Brett Heap's ruling (A)
  on the consumer's change `admit-resolved-council-protocol` (Hermes feature
  025), *"Per-seat environments (Recommended)"* (opensoft/brett-wip
  `lanes/log/codeXfactory-2.md`, RULED 2026-10-09T01:20:43Z), every council seat
  runs in its own GitHub environment, which holds no root seat key.
  The OIDC subject names the environment, and the consumer's governed runtime
  configuration maps environment to seat to binding. So the consumer's
  configured binding set is its commission binding plus one producer binding per
  seat. The owner provisions the environments, the federated credentials and the
  binding instances. Each binding's `broker` member records whether the broker's
  capability is verified, and against what evidence.

## The record of each act

Every record has `act`, `recorded_at` and `provider` (`{commit, bundle,
corpus_index_sha256}`). Each act is closed to its own members: a member that
belongs to another act is malformed, so nothing is carried unchecked. No record
carries broker state of its own.

| Act | Its members, beside `act`, `recorded_at` and `provider` |
|---|---|
| `pause` | `owner_word` |
| `drain` | `intake`, `in_flight` |
| `switch` | `owner_word`, `intake`, `producer`, `consumer` |
| `rehearsal` | `producer`, `consumer`, `rehearsal`, and `intake` when `rehearsal.mode` is `matched` |
| `activation` | `owner_word`, `intake`, `producer`, `consumer`, `rehearsal_ref`, `binding_refs` |
| `rollback` | `owner_word`, `intake`, `producer`, `consumer`, `rollback` |
| `resume` | `owner_word`, `producer`, `consumer`, `rehearsal_ref`, `binding_refs` |

`owner_word` quotes the owner's first-hand word verbatim, with its author, its
UTC time and a citation of where it is recorded. `producer` and `consumer` each
carry a side's repository, revision and E11 selection, and the two selections
must agree on `mode`, `protocol`, `provider_commit`, `provider_bundle` and
`corpus_index_sha256`. A record whose two sides differ on any one of them is
refused as `pair_mismatched`.

The records are checked in the activation order:

1. `activation_evidence_malformed`: the record breaks its schema.
2. `activation_evidence_incomplete`: a member its act requires is missing;
   `rollback.new_records_retained` is `false`; an activation or resume has no
   passing matched rehearsal behind `rehearsal_ref`, or one whose provider or
   matched values differ from its own; or its `binding_refs` omits a binding the
   consumer configures.
3. For an activation or resume, each `binding_refs` entry in order:
   `binding_unresolved` when the consumer configures no binding of that id, then
   `broker_capability_insufficient` when that binding's broker is not verified or
   names no evidence.
4. `pair_mismatched`.
5. `historical_reinterpretation_refused`: a rollback whose retained new records
   would be read under a protocol other than the replacement.

To check a record offline:

```sh
python3 scripts/validate-council-convening.py check path/to/record.json
python3 scripts/validate-council-convening.py select --producer producer-selection.json --consumer consumer-selection.json
```

`check` runs every rule the record alone can answer. It cannot resolve
`rehearsal_ref`, and it does not hold the consumer's configured binding set, so
it reports both as `not checkable offline` and never passes them. The consumer
runs the full order with its configured binding set before it admits a
convening under the activated pair. `select` checks the two sides' selections as
a pair.

## 1. Pause commissioning

Stop new commissioning on both sides. Nothing else in this runbook happens while
new convenings can still start.

Record a `pause` record carrying the owner's word.

## 2. Drain or explicitly cancel in-flight convenings

Every convening in flight at the pause is either drained, run to completion
under the protocol it started under, or explicitly cancelled. None is left
running into the switch, and none is moved to another protocol.

Record a `drain` record: `intake.paused_at` from step 1, and `in_flight`, with
the `disposition` (`drained` or `cancelled`) and the `convening_id` of every
convening it disposed of.

## 3. Switch both selections to one value set

Write each side's selection into its governed configuration, both naming one
protocol, one provider commit, one bundle and one corpus digest, in the same
mode. A selection names exactly one protocol and no fallback.

Run `select` over the two selections; it must exit 0. Record a `switch` record
carrying the owner's word, `intake`, and both sides.

## 4. Matched rehearsal: both sides run the full corpus at one index digest

Each side runs its own corpus adapter over every vector whose `applies_to` names
it, at the corpus digest its selection pins, with each vector's oracles injected
and each vector's `evaluation_time`. Every vector's outcome, refusal and findings
must match its `expected`; matching counts are not agreement. Before the removal
major, both selections are in `mode: rehearsal`.

Record a `rehearsal` record with `rehearsal.mode: matched`, the
`corpus_index_sha256` both sides ran, the `outcome`, and a reference to the
evidence. A matched rehearsal also carries `intake`. A dormant rehearsal, one
side alone, is recorded the same way with `mode: dormant` and backs no
activation.

**Keep the passing rehearsal record's exact bytes.** Step 5 names it by
`rehearsal_ref`, the raw SHA-256 of those bytes, so a re-serialized copy, even
one that parses to the same value, names nothing.

## 5. Activate or resume only on a matched, verified pair

Only after the removal major, and only on the owner's word, the sides switch
their selections to `mode: active` and commissioning resumes under the
replacement.

Record an `activation` record, or a `resume` record when commissioning resumes
after a rollback. It carries the owner's word, both sides, and:

- `rehearsal_ref`, naming the passing matched rehearsal of step 4. That
  rehearsal's provider must be this record's, and each side's selection in it
  must equal this record's on `protocol`, `provider_commit`, `provider_bundle`
  and `corpus_index_sha256`. `mode` is the one matched value that differs,
  because a rehearsal runs in `rehearsal` and an activation in `active`.
  Otherwise the record is `activation_evidence_incomplete`.
- `binding_refs`, the `binding_id` of every binding the activated consumer will
  use: its commission binding and each seat's binding. It must equal the
  consumer's configured binding set. A configured binding it leaves out is
  `activation_evidence_incomplete`, and an entry the consumer does not configure
  is `binding_unresolved`.
- An `activation` also carries `intake`, the pause it ends.

**An unverified broker parks the activation.** Broker capability is read only
from each named binding's `broker` member. One binding whose
`capability_verified` is `false`, or whose `evidence_ref` is `null`, refuses the
whole activation as `broker_capability_insufficient`, until the broker enforces
the full binding and its evidence is recorded (D4).

**`binding_refs` holds at most 16 bindings.** The estate's two councils, run per
seat, need 12: one commission binding and one binding per seat for the
merge-readiness council's four seats and the gate-rules council's six. A
configured set beyond 16 cannot be recorded, and two records naming part of the
set each are both refused, because each must name the whole set. Widening the
bound is a governed contract change.

## 6. Paired rollback, keeping the new records as audit evidence

A rollback stops intake and restores both sides together. It never re-reads new
records as old ones, and it never leaves one binding accepting both protocols.

**After an activation, both sides go back to their Release A pins.** Brett Heap
ruled this on 2026-10-09T13:22:16Z, *"Back to Release A pins (Recommended)"*
(opensoft/brett-wip `lanes/log/codeXfactory-2.md`, RULED line 259): a paired
rollback returns both sides to their pins at Release A, the deprecation minor,
where the legacy protocol is still `deprecated` and so still selectable, and
reselects legacy there. The new records are kept as audit evidence. That is
how this runbook reads D5's *"restores both prior versions/configurations
together"*. The consumer's own rollback returns its image to the same Release A
pin. A legacy selection at the removal major's pin, or any later one, would be
refused as `legacy_protocol_refused`, because the registry there holds the
legacy protocol `historical_only`.

1. Return each side's provider pin to the Release A commit and its bundle tag,
   and write each side's selection as the legacy protocol, `mode: active`, with
   that commit, that tag and the corpus digest at that commit.
2. Run `select` over the two restored selections from a checkout of the Release
   A commit, where the registry holds the legacy protocol `deprecated`; it must
   exit 0. A `select` run from the removal major's commit refuses the same pair,
   correctly, because there the legacy protocol is `historical_only`.

Record a `rollback` record carrying the owner's word and `intake`, because
intake stays paused until both sides' restorations are verified. Its `producer`
and `consumer` are the restored Release A configurations, the pair the rollback
leaves in force, and they must match like every other pair: a paired rollback
restores a matched pair, never one side. Its `rollback` member carries:

- `restored_producer` and `restored_consumer`: when each side's restored
  configuration was verified (`verified_at`), and the evidence (`evidence_ref`).
- `new_records_retained: true`. The records signed under the replacement stay as
  audit evidence; a rollback that drops them is `activation_evidence_incomplete`.
- `new_records_protocol`: the protocol those retained records stay verifiable
  under, which must be the replacement's `protocol_id`. Any other value is
  `historical_reinterpretation_refused`. A historical audit classifies every
  record by its recorded protocol and never reinterprets it:

  ```sh
  python3 scripts/validate-council-convening.py check --historical path/to/record.json
  ```

  That command routes a legacy record to the legacy verifier (exit 3, never a
  pass) and holds a replacement record to the replacement rules.

A rollback records no `binding_refs` and needs no rehearsal, because a broker
failure may be what caused it. Commissioning resumes only through step 5, as a
`resume` record.

## Ruled: a rollback after the removal major

Brett Heap ruled the rollback after activation on 2026-10-09T13:22:16Z, choosing
the recommended option, *"Back to Release A pins (Recommended)"* (opensoft/brett-wip
`lanes/log/codeXfactory-2.md`, RULED line 259). The question it answers came up
while this runbook was being written. Activation happens only after the removal
major, and at the removal major the legacy protocol becomes `historical_only`, so
a rollback could not restore the legacy pair as an active selection there.

Under the ruling, a paired rollback returns both sides to their Release A pins,
where the legacy protocol is still selectable, and reselects legacy there (step
6). The new records are kept as audit evidence, verifiable under the replacement.
The `rollback` record reads no registry status. It records the restored Release A
pair, matched, and the retained records. Whether the restored selections are
selectable is judged by `select` at the pin they name.

## The acts reserved to the owner

Every act below is the owner's, recorded with dated evidence:

- the commissioning pause, the drain or cancellation, the switch, the matched
  rehearsal, the activation, the rollback and the resume, each on the owner's
  first-hand word where the record carries `owner_word`;
- publishing each release and its annotated tag;
- the successors' pin advances;
- provisioning the per-seat environments, the federated credentials, the
  binding instances and the broker;
- deploying either side.
