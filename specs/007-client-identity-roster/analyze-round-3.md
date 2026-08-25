# Analyze round 3 — 007-client-identity-roster

Date: 2026-08-14. Same scope and dimensions, run fresh against the
post-round-2 artifacts. This round re-attacks round 2's own fixes as hard as it
attacks the artifacts — one of them over-reached and is reverted here — and
sweeps the sites the earlier rounds' fixes should have touched but did not.

Newly verified this round: `scripts/doc_health/runner.py:203` declares
`--repo-root` (aggregation checkout), and the script is `scripts/doc-health.py`
INSIDE the openxFactory repo — so from an aggregation root the path is
`openxFactory/scripts/doc-health.py`.

## Findings

### F-027 — MEDIUM — 4.2's own verification line repeats the miscount round 1 fixed at 1.2 and 2.3

*Artifact*: tasks.md 4.2 ("*Verification*: one negative per closed set plus
both legend cases").

Round 1's F-004 corrected the two verification lines that said "six vocabulary
negatives in 4.2"; 4.2's own line makes the same claim from the other side —
it presents its five vocabulary negatives as "one negative per closed set",
when the sixth closed set (authority class) is refused by 4.1's
`destructive-authority-class.yaml`. The line also omits
`evidence-ref-malformed.yaml`, which 4.2 authors but which is neither a
vocabulary nor a legend case.

*Fix applied*: 4.2's verification now states the split (five here + 4.1's
destructive negative = one per closed set, six), and names the `evidence_ref`
shape negative as FR-037's probe.

### F-028 — MEDIUM — round 2's F-022 fix over-reached: `ratified_by` RESOLUTION is not required, and repurposing fixture 2 dropped a ratified measurement

*Artifacts*: spec.md FR-014, plan.md Cluster B / Cluster C fixture 2 / coverage
row 9 / decision 19, research.md Decision 7, tasks.md 2.9 and 4.5 — all as
edited in round 2.

Re-read of the ratified text: FR-014 and the roster delta attach the resolution
clause to the INSTRUMENT citation alone — "and the **instrument citation** SHALL
resolve to an instrument in force". Neither requires the capability citation to
resolve against the target repo's promoted capability set, and the delta's own
scenario ("declares `mutate` authority and **names no** ratified capability")
is an ABSENCE test.

Round 2 nonetheless added `ratified_by` resolution AND repurposed repo fixture 2
from the absence case to a non-resolution case. That was wrong twice: it invents
a requirement the ratified text does not carry (the same defect class this loop
exists to catch), and it removed the only GATE-EXIT probe for the delta's own
scenario — leaving "the owning domain's conformance gate fails" measured by a
packaged finding alone, which proves a finding and not an exit.

The `consent_ref` half of the finding stands unchanged: FR-014's resolution
clause is explicit, was implemented nowhere, and now has repo fixture 6.

*Fix applied*: `ratified_by` resolution withdrawn from spec.md FR-014, plan.md
Cluster B and decision 19, research.md Decision 7 and tasks.md 2.9 — the
capability citation is checked for presence and domain-qualification, and
spec.md now says so explicitly so the omission is a recorded reading rather
than a gap. Repo fixture 2 restored to the ABSENCE case (mutate entry naming no
ratified capability → nonzero, the delta's gate-exit scenario), with its
packaged sibling annotated as the record-internal finding and the repo fixture
as the exit-level probe — the original plan's own framing. The probe count is
unaffected (27 packaged + 4 refusing repo fixtures + 1 doc-health = 32); its
composition sentence is corrected.

### F-029 — LOW — the plan's green bar omits the feature's own test package

*Artifact*: plan.md green bar step 3 (`pytest tests/conformance-gate
tests/doc-health tests/credential_contracts`).

`tests/client-identity-roster/` — which carries the six repo fixtures, the
SC-002 discrimination assertion (4.6), the SC-013 source-level assertion (4.7)
and 1.5's field-list assertion — is absent from the plan's green bar, though
tasks 10.4 runs it. The green bar is the list SC-010 is read off.

*Fix applied*: step 3 now includes `tests/client-identity-roster`.

### F-030 — LOW — two tasks invoke `doc-health.py` on a path that does not exist from the cwd they name

*Artifacts*: tasks.md 6.4 and 10.3 (`python3 scripts/doc-health.py --repo-root
<agg>` … "from the aggregation root").

From an aggregation checkout the script is `openxFactory/scripts/doc-health.py`
— which is exactly how plan.md green bar step 7 writes it. As written, both
tasks' verification commands fail with a missing file before measuring
anything.

*Fix applied*: both task lines corrected to
`python3 openxFactory/scripts/doc-health.py --repo-root <aggregation checkout>`,
matching the plan.

## Rounds 1–2 findings re-checked

Round 1's fifteen and round 2's eleven all hold, except F-022 whose
`ratified_by` half is reverted above (F-028) and whose `consent_ref` half is
unchanged. Re-verified this round: no "FIVE repo" remnant survives the fixture
recount; no hyphenated member spelling survives outside prose and kebab-case
file names; the legend rule set is still exactly FR-034's two findings with two
negatives; and the `tests/` sweep exclusion is stated identically in plan.md,
research.md and tasks.md.

## Escalations

None.
