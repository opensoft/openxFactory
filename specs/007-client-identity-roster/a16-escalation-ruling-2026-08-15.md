# A-16 escalation ruling — the multi-surface reader example

Date: 2026-08-15. Seat: architect. Trigger: task 0.1 (the A-16 precondition)
FAILED with clause 2 affirmatively falsified — full evidence at the
implementing agent's escalation record (candidates table:
`ESCALATION-0.1.md` in the session baseline dir; substance restated here).

## The facts (verified twice, independently)

1. No provider-native permission or role reaching BOTH `business_central` and
   `exchange` read surfaces is cited anywhere in the estate.
2. The estate affirmatively documents NARROWER paths: an Exchange-only
   read permission (Graph `Mail.Read` bounded to one mailbox by a
   provider-enforced application access policy —
   OpsxFactory `openspec/specs/exchange-administration/spec.md:46-56`, with
   attempted-overreach proof), and a ratified statement that Business Central
   has NO read-only path at all
   (`openspec/specs/business-central-administration/spec.md:93-101`).
3. The ratified roster delta's forced-breadth requirement is CONDITIONAL
   ("WHEN the narrowest available permission reaches more than one admission
   surface…") — it mandates behavior IF such a permission exists and asserts
   none does. Only the Speckit-level packaged-example mandate (FR-019 fourth
   case, SC-002 fourth positive) is blocked.
4. The known real multi-surface identity class
   (`microsoft_managed_node_inventory_reader`) spans only surfaces ratified
   answer 5 excludes from the v1 vocabulary.

## Ruling

A governed packaged example is a TRUTHFUL worked case; within the v1
two-surface vocabulary no truthful provider-forced multi-surface reader
exists, and synthesizing one is exactly what this contract exists to forbid.
Therefore:

1. **The packaged fourth positive is RELOCATED, not synthesized.**
   `examples/client-identity-roster/` carries THREE worked cases (the BC
   two-admission-act entry, the duty-separated pair, the `planned` entry) —
   all truthful. The multi-surface reader becomes a REPRESENTABILITY FIXTURE
   in the test corpus (`tests/` side, wherever Cluster C homes positives),
   with an explicit header: synthetic; no in-vocabulary provider-forced
   multi-surface permission exists as of 2026-08-15 (clause-2 falsification
   cited); exists to prove killed-flaw (a) representability — a
   spanned-surfaces entry with declared forced breadth validates with ZERO
   findings — and to stand ready for vocabulary growth.
2. **All machinery stays.** `spanned_surfaces[]`, `declared_excess` forced
   breadth, the reach rules, and every named negative remain exactly as
   specified — the ratified conditional requires the capability to exist even
   while no in-vocabulary instance does.
3. **Amend FR-019 / SC-002 / task references** (spec.md, plan.md, tasks.md,
   and any checklist items counting four packaged positives): fourth case =
   representability fixture, reason recorded with both citations from fact 2.
   The killed-flaw acceptance obligation (multi-surface reader passes clean)
   is satisfied by the fixture; killed-flaw fixtures were never required to
   be packaged examples.
4. **Task 1.2's `exchange` member description proceeds** — its own escalation
   clause does not trigger (act and scoping mechanism are ratified and
   live-verified).
5. **VERIFICATION OBLIGATION (cross-model, before encoding):** the applying
   agent sweeps the ratified packet for any text that mandates a PACKAGED
   multi-surface example (as opposed to the conditional behavior and the
   Speckit artifacts' own case lists). If any ratified line does, STOP —
   the ruling then needs Brett, not the architect. (The escalation record
   already states the delta is conditional; verify independently.)

## Jurisdiction correction and outcome (2026-08-15)

The item-5 verification obligation FIRED: packet `tasks.md:61-66` (task 2.3)
— ratified verbatim 2026-08-14, and named "the authority for scope" by the
Speckit spec — mandates case (ii) as PACKAGED. Relocating it reduces a
ratified line, so the authority was Brett's, not the architect's. The
substance of this ruling was then put to Brett as Decision C with three
options (relocate / keep-packaged-marked-hypothetical / widen vocabulary).

**Decision C (Brett, 2026-08-15): RELOCATE TO FIXTURE** — amend the ratified
packet: task 2.3's case (ii) becomes the synthetic representability fixture
per items 1–3 above; packaged set = three truthful cases; all forced-breadth
machinery, rules, and negatives stay; the ratified conditional requirement is
untouched. Recorded via sibling amendment record per the packet's
record-immutability discipline (tasks.md itself is the living task list and
is edited in place; the amendment RECORD is the sibling).
