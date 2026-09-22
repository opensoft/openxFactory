---
code_surface: none — MEASURED, not assumed, against `main` `ac50d70d`. The delta is requirement prose about what a WRITTEN ASSERTION must name, and the one enforced corpus-wide gate in this repository ALREADY NAMES IT: `.github/workflows/openspec-cli-pin-gate.yml`:101 is `python3 scripts/validate-openspec-cli-pin.py --all --no-cache`, and that file is deliberately the only step in the workflow. Evidence, each check run rather than asserted: (1) no script, validator, test or workflow changes — `scripts/validate-openspec-cli-pin.py` is NOT edited, its `reconcile()` is NOT edited, and `contracts/openspec-cli-pin.yaml` is NOT edited, which is the point: **the disposition mechanism works and this packet leans on it rather than touching it**; (2) the requirement's own subject is a class of TEXT, and the corpus's non-archived occurrences of the raw invocation are task boxes, plans, quickstarts and evidence lines under `openspec/changes/` and `specs/`, not code — a reader of those is a human or an agent, not a parser; (3) NO CHECKER IS PROPOSED and that is a declared decision, not an omission (`design.md` D4): the estate's own precedent for gating a prose header is a `scripts/validate-*.py` plus a corpus test, and the measurement that would justify one — how many live boxes the rule reaches, and whether a grep can tell an assertion from a citation of the defect — has not been taken, so proposing the gate now would be proposing an unmeasured surface. A successor may take it; this packet states the rule. THE ONE MECHANICAL CONSUMER of this delta is doc-health's own `modified-block-currency` family, which reads every active change's blocks by construction — a GATE OVER this packet, not a surface it changes. Under `release-realization` an empty code surface archives ON LANDING plus this task list rather than on merged-plus-green realization evidence.
target_release: implemented — the value `release-realization` names for a doc-only change. No contract bundle is cut, nothing under `contracts/` is edited, no digest set moves and no consumer's pin has to advance to receive this. The realization of a rule about what a record must name IS its promotion at archive.
sequenced_after: []
---

# Proposal: require-adjudicated-validation-entrypoint

Status: ratified
Ratified: 2026-09-22 by Brett Heap (openxFactory operator authority) — in-session, verbatim *"ratify #1140 and #1141"*, at head `c36ff08c`; record at review/ratification-2026-09-22.md
Kind: proposal
Proposed: 2026-09-22, in lane `openxfactory-4` (display
`openXfactory-4-openDox_extraction`), on the measurement Brett Heap accepted and
ruled on the same day — `opensoft/openxFactory` issue
[#656](https://github.com/opensoft/openxFactory/issues/656) comments
[`5778300335`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5778300335)
(the read-only measurement) and
[`5778397686`](https://github.com/opensoft/openxFactory/issues/656#issuecomment-5778397686)
(**RULED 2026-09-22T14:33:02Z by Brett Heap, by multi-choice: § 8.9 clause (2)
READS LITERALLY; the tick becomes `[~]`**).
Origin: the ruling disposed of ONE BOX. The defect it disposed of is a CLASS, and
nothing in the corpus yet forbids the next box being written the same way. This
packet writes that rule down.

**THE DECISION IS BRETT HEAP'S AND THE ENCODING IS THIS LANE'S.** The ruling
settled that a task box naming the raw command means the raw command, and that
such a box cannot be ticked while a ratified disposition stands. This packet adds
no judgment to that; it states the general rule the particular ruling implies.
The word that SETTLED THE BOX (`5778397686`) and the word that RATIFIES THIS
PACKET (`5779511063`, 2026-09-22T15:45:54Z, verbatim *"ratify #1140 and #1141"*)
are two separate acts, and both are Brett Heap's.

**THE RATIFIED BASELINE IS `c36ff08c`, AND IT IS THE HEAD THE WORD NAMED.** No
commit moved this packet between the word and this record: the ratification
front-matter, the record at `review/ratification-2026-09-22.md` and the README
status line are the first changes after it, and none of them is requirement text.
*(The sibling `#1140` is NOT in that position and says so in its own record —
its head moved one second before the word, normatively, and re-ratification is
registered there as owed. The two packets are separate acts and this one inherits
nothing from that.)*

## Why

**Two commands over one tree return opposite verdicts, and only one of them is
this repository's.** Measured at this packet's own head, both run against the
same corpus:

| command | version that answered | verdict | exit |
| --- | --- | --- | ---: |
| `python3 scripts/validate-openspec-cli-pin.py --all --no-cache` — the pin's `consumer_entrypoint:` | `@fission-ai/openspec@1.12.0`, **verified against its recorded content address** | `Totals: 108 passed, 1 failed (109 items)`, **the 1 finding DISPOSITIONED and printed by name with its citation and granting authority** | **0** |
| `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — the raw tool | **1.13.1** on `PATH` — **not the pinned version at all** | `Totals: 108 passed, 1 failed (109 items)` | **1** |

**Same tree. Same finding. Opposite exit.** The finding is
`add-chain-attestation` / `signed-execution-chain/spec.md`, carrying
`ratified_by: 'Brett Heap, 2026-09-05, "take exit 2"'` in
`contracts/openspec-cli-pin.yaml`, with `retires_when:` recorded there as
expected to be **long-lived**.

### Why they differ, and why it is not a matter of strictness

The pinned CLI is a FOREIGN JUDGMENT about a LOCAL corpus. This corpus has a
PROMOTED scenario-rename grammar — the reserved
``**Merged into `<title>` by `<change>` (<date>):**`` marker, canon at
`openspec/specs/doc-health/spec.md`:1770 — and **1.12.0 cannot read it**. The
readiness evidence says so in as many words:
`openspec/changes/prepare-openspec-1-12-readiness/evidence/openspec-1.12-readiness-2026-09-05.md`
§ *The two refusals* — *"1.12.0's scenario-currency check is marker-blind. It
compares scenario title sets and cannot read the declaration this corpus
requires."* The only edit satisfying the tool would restore a scenario title
whose restoration reinstates the very permission council LA-A1 was raised to
close. **Refused** — and recorded, as a cited disposition, which is the
mechanism the capability already provides.

`scripts/validate-openspec-cli-pin.py` `reconcile()` applies those dispositions
and computes `verdict = 1 if undispositioned else 0`. **The raw tool has no
access to the pin file, does not know the disposition exists, and cannot reach
that verdict.** Its red is not a stricter reading of the same question; it is a
different reader answering a question the repository did not ask it.

### The worked example, and what it cost

`split-opendox-two-layer-product` § 8.9 clause (2) named
`OPENSPEC_TELEMETRY=0 openspec validate --all --strict`. Read literally — which
is how Brett Heap ruled it reads — **that box can never be ticked while the
`add-chain-attestation` disposition stands**, because the command it names exits
1 on a finding the corpus has ratified against. The adjudicated gate was green
on every pull request throughout (`openspec-cli-pin-gate` SUCCESS at `df7b0ca7`,
`c273cb39`, `8fa12dbc`). So the packet's own archive could not tick a box whose
subject was already true, and § 8.9 took the reserved `[~]` DEFERRED marker
naming the live disposition as its reason (RULED `5778397686`; final count
`67 [x] / 0 [ ] / 5 [~] of 72`).

**Nothing false was claimed and nothing ratified was edited — and the same box
written tomorrow would cost the same again.** That is the class this packet
closes.

## What changes

**ONE `## ADDED` requirement in `neutral-product-pin`. No existing requirement is
modified, no code moves, and the disposition mechanism is not touched.**

A gate step, task box, checklist item or evidence record asserting CORPUS-WIDE
OpenSpec validation SHALL name the consuming repository's `consumer_entrypoint:`
invocation and SHALL NOT name the raw command. Around that, four statements the
rule needs in order not to be read wider or narrower than it is:

1. **The obligation is on the ASSERTION, not only on the run.** The capability
   already obliges the RUN to go through the entrypoint. A repository whose CI
   calls the entrypoint correctly while its task boxes name the raw command has
   a correct gate and an undischargeable record of it.
2. **A narrowed claim is not reached.** A record naming the validation of ONE
   change says something about that change; only a whole-corpus claim asserts
   the adjudicated verdict. A narrowed run **still applies** the dispositions it
   matches — canon says so at `openspec/specs/neutral-product-pin/spec.md`:602-604
   — and what it cannot do is decide STALENESS. *(An earlier draft said such a
   run could not be reconciled against the dispositions "at all", which
   contradicted that ratified sentence. Caught by Copilot `r4073184083`; the
   restriction is now scoped to staleness, which is what canon restricts.)*
3. **Ratified and archived text is not edited by this requirement.** An archived
   record is frozen and a ratified clause is amended only by its own instrument.
   The remedy for an existing box is the one its own packet provides — the
   reserved `[~]` marker naming the live disposition — and this requirement
   governs what is written NEXT.
4. **The staleness property is why naming the entrypoint is safe.** It is
   carried as a scenario, deferring to the requirement that already owns it
   rather than re-legislating: a finding no in-scope disposition covers FAILS,
   and **a disposition matched by no finding in a whole-corpus scan REFUSES the
   run as `pin-disposition-stale`**. The adjudicated verdict is strictly more
   informative than the raw one and never more permissive.

## Which capability owns this, decided by reading

**`neutral-product-pin`, and the delta is `## ADDED`.** Every noun in the rule —
the pinned CLI, the `consumer_entrypoint:`, the `dispositions:`, the adjudicated
verdict — is this capability's own, and its `## Purpose` already claims the
neighbouring ground: *"The capability makes which reader ran an auditable
digest."* This requirement extends that from WHICH READER RAN to WHICH VERDICT
IS THE REPOSITORY'S.

**Why not `doc-health`.** It owns the `Merged into` marker at
`openspec/specs/doc-health/spec.md`:1770 — the convention whose unreadability
CAUSES the finding — but it owns neither the pin, nor the entrypoint, nor the
dispositions. Placing the remedy there would put it in a different capability
from the mechanism it depends on, and `doc-health` would acquire a rule about a
foreign tool's consumption that none of its other requirements touch.

**Why not a new capability.** It would split *run through the entrypoint*
(`neutral-product-pin`) from *name the entrypoint* (elsewhere) — a rule and its
sibling in two places. That is the same defect Brett Heap refused on this very
day in the sibling ruling `5777949892`: *"It leaves ONE rule in the corpus rather
than a rule and an exception."*

**And it is not already written.** The nearest requirement, *A consuming
repository runs OpenSpec validation only through the pinned entrypoint, so a
PATH binary cannot affect the gate*, governs WHICH BINARY ANSWERS, and its
reason is PATH-determinism: an ambient installation must not be able to change a
verdict. A reader can satisfy it completely while believing the two commands
return the SAME verdict by different routes. **They do not** — exit 0 against
exit 1 on one tree — and that difference, not the binary's provenance, is what
this requirement is about.

## The condition that would retire the class — registered, not proposed

**Stated so the record does not read as though the disposition were permanent,
and deliberately NOT written as a requirement.**

The marker-blindness class would be retired by an upstream CLI that can read
this corpus's declared scenario rename. **The CLI is CONSUMED, never vendored or
patched**: `contracts/openspec-cli-pin.yaml` names `package:
"@fission-ai/openspec"` and `source_repository: Fission-AI/OpenSpec`, and the
verifier fetches, digest-checks and installs the published artifact — there is no
fork in this estate to carry a patch. The pin stands at **`1.12.0`**
(`contracts/openspec-cli-pin.yaml`:318); **`1.13.1` is published upstream** and
is, as it happens, what sits on `PATH` at the workstation this packet was
authored on.

**Why this packet does not propose the bump.** Moving the pin is a HUMAN-ONLY
act that must land, in the same change, evidence that the governed trees validate
clean AT THE TARGET VERSION, and must RE-DERIVE every disposition against that
version's own findings — both already ratified requirements of this capability.
Whether `1.13.1` reads the marker is unmeasured here, and a bump proposed without
that measurement is exactly what those requirements refuse.

**And retiring the class would not retire this requirement.** The dispositions
mechanism is general: the pin file records a SECOND live class today (*canon
moved under an un-re-derived delta*), and any future disposition of any class
re-creates the divergence between the two commands. The rule is about what a
claim must name, not about one tool's defect.

## Impact

- **Specification:** `neutral-product-pin` — one ADDED requirement, five
  scenarios.
- **Code:** none. The enforced gate already names the entrypoint
  (`.github/workflows/openspec-cli-pin-gate.yml`:101).
- **Contracts:** none. `contracts/openspec-cli-pin.yaml` is not edited — **the
  disposition mechanism works and this packet leans on it.**
- **Existing text:** nothing ratified or archived is edited. § 8.9's own remedy
  was taken by its own packet under `5778397686`.
