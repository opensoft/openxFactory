---
code_surface: openxFactory (`scripts/doc_health/pin_class.py` — the FOUR expressions that build a pin site, each binding its value group to `([0-9a-f]{40})` with a leading key boundary and no trailing hexadecimal boundary: `_field_re` at `:194-205` with its value group at `:204`, `_VOCAB_RE` at `:977-980` with its value group at `:980`, and the two PROSE class members' own declared patterns at `:347` and `:406`, which `PinMember.regex` at `:289-290` compiles directly; `LOOSE_SHA_RE` at `:159` is the guard that already states the rule and is NOT edited, only carried. `experiments/avatar-brokered-call/src/avatar_f0/cli.py` — `_git_file_commit` at `:43-51` (its `"unknown"` returns at `:49` and `:51`) and `_git_head` at `:54-62` (`:60` and `:62`), four emission sites across two functions, of which `:49` fires on two conditions because `subprocess.run` is called with no `check` and its return code is never read. `scripts/ideation_dashboard/snapshot_registry.py:283` — `self.source_revision or "unknown"` in `index_entry`, whose MEMBER does not change and whose LITERAL does. `scripts/doc_health/pin_sentinels.py` — the `emitters` tuples of `UNCOMMITTED_WORKTREE`, `UNCOMMITTED` and `UNKNOWN`, which are measured by test and must follow the split. Plus regressions under `tests/doc-health/` (`test_pin_reachability.py`, `test_sentinel_vocabulary.py`). NO change is proposed to the declared `PIN_CLASS` rows, `PIN_KEY_VOCABULARY`, `NON_MEMBERS`, the ref set consulted, `KNOWN_LOSSES` or its discharge mechanism, `repair_route()`, the retention namespace, the sentinel `CONDITIONS` map or the set of declared members, the deterministic check family registry `scripts/doc_health/families.py`, the family enumeration or its numerals, `health/dispositions.yaml`, or one byte of any committed artifact.)
target_release: none — no contract bundle is owed, and this is established by PARSE rather than by `grep`. `contracts/releases/contract-v2.0.digests.yaml` is the declared bundle (`contracts/manifest.yaml:3`); it was loaded and its 192 entries walked into their member paths, and NOT ONE path under `scripts/doc_health/`, `scripts/ideation_dashboard/` or `experiments/` appears in it. The inventory carries exactly 22 `scripts/` members: 18 under `scripts/hermes_runtime_validation/` and four top-level validators, one of which — `scripts/validate-ideation-dashboard-contracts.py` — is a NEIGHBOUR of the lane this packet edits and is not the file it edits. So no schema moves, no digest set changes, and no release tag is owed. THE SIBLING PACKET OF THE SAME COMMISSIONED SET IS THE OPPOSITE CASE, and separating them is why this one can archive on its own evidence: `fix-content-resolution-conflation` edits `scripts/hermes_runtime_validation/release.py`, which IS a non-editorial member of that same inventory, and therefore owes an additive cut. The archive gate here is merge-plus-green on main: `python3 -m pytest tests/doc-health` green under `set -o pipefail`, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and the declared pin class reporting `clean` with its site count, its outcome split and its sentinel classification unchanged except where this packet's own realization moved them. The change ships ACTIVE and archives only after that.
Status: ratified
Ratified: 2026-08-28 by Brett — in-session selection of the orchestrating session's recommended option, verbatim: "lets do all 3 in order". The recommendation this selected was the orchestrating session's own wording, "the measured-latents bundle", and the two voices are kept apart deliberately rather than merged into one quotation. THE CITATION COVERS THE DECISION TO FILE AND NOTHING ELSE: the five decisions in § Orchestrator decisions below — including the split of the approved three-defect set into TWO packets — were taken by the authoring session under standing patterns, are NOT covered by this citation, and are flagged there for veto, as are the four questions in § Open Questions. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, and clears its three-way floor on all three axes: approver (`by Brett`), date (`2026-08-28`), and a resolvable record path (this file, § Orchestrator decisions and § Open Questions).
Proposed: 2026-08-28
Origin: Two defects the corpus already measured and deliberately declined to fix in the packet that found them. `declare-sentinel-pin-vocabulary` § 5.5 recorded the trailing-boundary gap at its filing and carried it untouched through realization and archive, on the stated ground that folding a silent mis-parse fix into a vocabulary packet would hide it. Its § 5.6 was raised at that packet's own realization: `"unknown"` measured as one spelling doing three jobs, and the vocabulary absorbed it as the weakest member while naming the split as owed. Both were re-measured here on the day of filing, and both measurements moved.
---

# Proposal: fix-pin-value-boundary-and-sentinel-split

## Why

Two defects with evidence already on the record, in the same surface, pointing
in the same direction: **the verification and the generators disagree with the
artifacts about what a value says.**

**The verification can invent a pin.** Four expressions in the pin class bind a
value to forty hexadecimal characters with a boundary in front of the KEY and
none after the VALUE. A longer hexadecimal run under a swept key therefore
yields a forty-character string that is the truncated prefix of something the
artifact never claimed, and that string is then carried through the whole
verification as if it were the artifact's provenance claim — reachability
answered against it, retention computed from it, a verdict reported about it.
The guard against precisely this lives ten lines above the first of the four,
with a comment explaining why it is needed, and was never carried across.

**The generators can under-claim.** The promoted sentinel vocabulary landed with
`"unknown"` declared as its WEAKEST member and an explicit instruction attached:
a generator that CAN tell which stronger condition held must write that stronger
member instead. The sites emitting `"unknown"` today can tell. One of them,
measured here rather than inherited, cannot even tell WITHIN ITSELF — a single
`return` serves both "this file has never been committed" and "git could not be
run", because the `subprocess.run` above it is called with no `check` and its
return code is never read.

Neither is live. Both are measured. Both were named by the same archived packet,
and this is the packet that was named as their home.

## What was measured

All measurements taken 2026-08-28 in a fresh worktree off `origin/main` at
`6612d3239cbc99b73eb32cf76a861929aa901276`, against the modules as committed.

### 1. The truncation, constructed and run

A sixty-four-character value — twenty-four `a` then forty `b`, chosen so the
fabricated prefix is visibly a splice of two runs — placed under a swept key and
matched by each of the four site-building expressions:

| expression | site | result |
| --- | --- | --- |
| `_field_re("source_revision")` | `pin_class.py:204` | fabricated `aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbb`, length 40 |
| `_field_re("commit")` (JSON form) | `pin_class.py:204` | fabricated, length 40 |
| `_VOCAB_RE` (YAML and JSON) | `pin_class.py:980` | fabricated, length 40 |
| prose member `ideation/cross-reference.md` | `pin_class.py:347` | fabricated, length 40 |
| prose member gate-action record | `pin_class.py:406` | fabricated, length 40 |
| `LOOSE_SHA_RE` on the same line | `pin_class.py:159` | **no match** — the guard works |

`FULL_SHA_RE.match()` then accepts the fabricated prefix as a whole object name,
so nothing downstream can tell it from a pin the artifact carries.

**THE ARCHIVED RECORD NAMED TWO EXPRESSIONS AND THERE ARE FOUR.** § 5.5 of
`declare-sentinel-pin-vocabulary` names `_field_re` and `_VOCAB_RE`. The two
PROSE members declare their own `pattern` strings, and `PinMember.regex` at
`:289-290` compiles those directly to build sites — same defect, same shape, not
previously written down. This is recorded as a CORRECTION to the inherited
record rather than smoothed into agreement with it, because the count is what a
later reader will check the fix against.

**IT IS LATENT, AND THAT IS MEASURED TOO.** Every committed file the class
sweeps was scanned for a run of 41 or more hexadecimal characters under any
vocabulary key: **1116 swept files, 0 hits.** The declared class at this
revision reports **66 declared pin sites across 23 class members — 50 reachable,
0 orphaned, 1 lost (declared unrecoverable, 0 awaiting a superseding record), 0
inconclusive; 0 uncovered, 0 vanished, 0 future members now carrying pins; 7
legal non-pins, 0 undeclared non-commit values, 3 recognized legacy absences, 0
unused vocabulary members** — `clean` true.

**WHAT WOULD REACH IT.** A generator stamping a content digest under a key the
vocabulary already sweeps (`derived_from`, `generated_from`, `contract_ref`,
`snapshot_rev_seen` are all in it, and `sha256:`-prefixed digests are the house
idiom one convention change away from bare); an artifact from a repository using
git's sha256 object format, where a commit name IS sixty-four characters; or a
hand-written value with a typo'd extra character. None of the three is exotic,
and none announces itself: the run stays green, and the finding it emits — if it
emits one — names a value nobody wrote.

**AND WHAT THE VALUE DOES ON THE OTHER PATH TODAY**, which § 5.5 recorded at the
sentinel packet's realization and which still holds: the WIDE regexes extract
the whole scalar, so the same sixty-four-character value is ALSO reported by the
non-commit classification as an undeclared value — at the same time as the pin
path makes its bogus pin. Two readings of one value, one of them fabricated.
Refusing the site is what leaves the correct reading standing alone.

### 2. The `"unknown"` sites, re-read

`declare-sentinel-pin-vocabulary` § 5.6 names three sites. Re-reading them found
**five**, spanning **three** conditions, and one site doing two jobs by itself:

| site | condition, measured | declared member that fits |
| --- | --- | --- |
| `snapshot_registry.py:283` (`index_entry`) | index entry with no recorded revision; the repository is readable and the emitter cannot say why | `unestablished-revision` — **`"unknown"` is correct here** |
| `cli.py:49` (`_git_file_commit`, `git log` exited 0, empty output) | the path has no commit history: readable repository, real content held by no commit | `dirty-worktree` → `uncommitted-worktree` |
| `cli.py:49` (`_git_file_commit`, `git log` exited non-zero, empty output) | git ran and failed; nothing was established | `unreadable-repository` → `uncommitted` |
| `cli.py:51` (`_git_file_commit`, `except Exception`) | git could not be run at all — `OSError`, timeout | `unreadable-repository` → `uncommitted` |
| `cli.py:60` (`_git_head`, empty output) | `rev-parse HEAD` produced nothing, which on this command means it failed | `unreadable-repository` → `uncommitted` |
| `cli.py:62` (`_git_head`, `except Exception`) | git could not be run at all | `unreadable-repository` → `uncommitted` |

**`:49` IS THE SITE THE INHERITED RECORD COULD NOT HAVE NAMED**, and it is the
reason the split is not a search-and-replace. `subprocess.run` is called there
with no `check` and `out.returncode` is never read, so `out.stdout.strip() or
"unknown"` fires identically on a successful run that found no commit and on a
failed run that found nothing because it failed. No assignment of a stronger
member to that `return` can be correct until the branch above it exists.

**`snapshot_registry.py:283` IS ALREADY RIGHT, and saying so corrects the
record.** § 5.6 lists all three sites as owing a split. Measured against the
promoted vocabulary, the projector's condition IS `unestablished-revision`: the
snapshot's own `generation.source_revision` was absent, unfetchable or
unrecorded, the repository is perfectly readable, and the emitter genuinely
cannot say which stronger condition held. What changes there is not the member
but the LITERAL — the declaration exists so that a generator imports the
spelling rather than retyping it, which is, in the vocabulary's own words, "the
whole difference between a vocabulary and a habit".

**NO COMMITTED ARTIFACT CARRIES `"unknown"`.** The class reports 7 legal
non-pins: six `uncommitted-worktree` and one `not-applicable-ad-hoc`. So the
split moves no committed bytes, and `unknown` survives the split as a declared
member with a live emitter rather than becoming an unused one.

### 3. The canon that already governs the split

`ideation-cross-reference`, promoted 2026-08-28, "A generator that cannot
truthfully pin a commit writes a declared sentinel, never a commit name",
scenario *The generator cannot read repository state at all*: "**AND** the
condition it names MUST be the one that actually held, so a reader can tell an
ad-hoc derivation from an unreadable repository." The vocabulary module states
the same duty from the other side, in the `unestablished-revision` condition
itself: "a generator that CAN tell an unreadable repository from uncommitted
content from an ad-hoc derivation MUST write that stronger member instead".

Four of the five sites can tell and do not. That is a conformance gap against
promoted canon, not a gap IN promoted canon — which is why this half of the
packet proposes no requirement (OD-3).

### 4. The bundle question, answered by parse

`contracts/releases/contract-v2.0.digests.yaml` loaded with a YAML parser and
its 192 entries walked into member paths. `scripts/doc_health/*`: **0 members**.
`scripts/ideation_dashboard/*`: **0 members**. `experiments/*`: **0 members**.
The 22 `scripts/` members are 18 under `scripts/hermes_runtime_validation/` plus
four top-level validators. **No cut is owed.**

## What this changes

1. **One ADDED requirement on `doc-health`**: a pin site is built only from a
   value that is a whole object name. Four scenarios, covering the truncation,
   the collision case, the untouched conforming path, and the rule that the
   boundary belongs on every expression that builds a site.
2. **The four expressions gain the trailing boundary** the module's own
   standalone scanner already carries. Measured against the fix: the
   sixty-four-character value matches none of them, and every conforming shape —
   bare, quoted, JSON, sequence-item, comment-trailed, prose — still matches and
   still yields the same site.
3. **The `"unknown"` sites are split onto the conditions they mean**, under
   canon that already obliges it. `_git_file_commit` gains a return-code branch
   it does not have; four sites move to the stronger member that fits; the
   projector keeps `unknown` and gains the imported constant.
4. **`pin_sentinels.SENTINELS` emitter tuples follow the split**, because they
   are measured by test rather than believed, and a member whose declared
   emitters no longer emit it is the drift the declaration exists to catch.

## What this deliberately does not change

* **No committed artifact is edited.** No pin value, no manifest, no evidence
  record, no gate record. The corpus at this revision carries nothing the fix
  reclassifies — measured, not assumed.
* **No declared member, key, exclusion, condition or sentinel spelling is added,
  removed or renamed.** The vocabulary is used, not extended.
* **No deterministic check family is added**, and the family enumeration and its
  numerals are untouched and unrestated.
* **No new outcome, no new report section, no new severity.** A refused value
  reaches the classification that already exists for it.
* **No contract bundle.** Measured by parse, § What was measured 4.

### Named follow-ups, out of scope here

1. **The other unrepaired generators.** `declare-sentinel-pin-vocabulary` § 5.1
   holds `_head_sha()`, `git_head_revision()` and above all
   `RealGit.head_sha()` — the widest-fanout pin source in the repository, whose
   cleanliness check would move six record families at once. Untouched here.
2. **Whether a composed projection should carry a pin key at all** — § 5.3 of
   the same packet, a schema question, unmoved.
3. **The preflight half of the enforcement home** — § 5.4 of the same packet,
   unmoved.
4. **Whether a generator must IMPORT a declared spelling rather than retype it.**
   Raised by this packet's own realization of the projector site and recorded as
   Q3 below rather than legislated here.

## Orchestrator decisions flagged for veto

Every decision below was taken by the AUTHORING SESSION under standing patterns.
Brett's citation authorizes the FILING and reaches none of them.

**OD-1 — THE APPROVED THREE-DEFECT SET IS FILED AS TWO PACKETS, SPLIT ON THE
CONTRACT-BUNDLE BOUNDARY.** This packet carries defects 1 and 3;
`fix-content-resolution-conflation` carries defect 2 and cites the same origin
act. THE REASON IS THE ARCHIVE GATE, and it is measured rather than argued.
Defect 2's only surface, `scripts/hermes_runtime_validation/release.py`, is a
non-editorial `type: validator` member of `contract-v2.0`'s digest inventory
whose recorded digest `sha256:660e55ca…` is exactly what the tree carries today,
so touching one byte of it owes an additive bundle cut — and the `contract-v1.44`
precedent records that the cut's final acts, `verify-promotion` and the annotated
tag, are explicitly NOT the authoring session's (that packet's tasks § 4.5
discharged them partially, by decision). This packet's three files are members of
no inventory at all. Bundling them would hold two zero-cost fixes behind a
human-gated contract tag for no benefit either half gets.
**REJECTED ALTERNATIVE — ONE PACKET FOR ALL THREE**, and it has real arguments.
Multi-capability packets are house-normal. The three defects share a theme —
values a verification or a generator reports without having read them — and one
origin act producing one packet is tidier than one act cited twice. Declined on
the archive-gate arithmetic above, and on a second measurement: the two halves
share NO file, NO capability and NO test module. Defects 1 and 3 are
`doc-health` plus `ideation-cross-reference` over `scripts/doc_health/`,
`scripts/ideation_dashboard/` and `experiments/`; defect 2 is
`shared-contract-ownership` over `scripts/hermes_runtime_validation/`. The
sentinel packet was CONSTITUTED as one packet from two items on the explicit
ground that they were "the same idea (honest non-pins)"; read the same way,
defects 1 and 3 are one idea — what a pin value may be, and what a sentinel must
name — and defect 2 is a different one on a different surface.
**THE COST OF THE SPLIT, STATED RATHER THAN BURIED:** Brett said "in order", and
the split re-sequences the approved 1, 2, 3 as {1, 3} then {2}. The authoring
session reads "in order" as governing the SET rather than the filing shape, and
flags the reading here so it can be overruled cheaply — the two packets can be
merged into one before either is reviewed.

**OD-2 — THE DELTA IS SINGLE-CAPABILITY AND ALL ADDED: ONE REQUIREMENT ON
`doc-health`.** `doc-health` owns the pin verification — the promoted
"Derivation-pin reachability is verified across a declared artifact class" and
both promoted sentinel requirements live there — and it is the capability whose
code produces the fabricated pin. It stands at 38 requirements; this makes 39.
No `MODIFIED` block is issued: the promoted classification requirement already
says an undeclared non-commit value is a defect naming the value, and this
requirement adds the obligation NOT to manufacture a second, shorter reading of
the same value beside it. Two active changes carry `doc-health` deltas —
`add-nightly-dashboard-refresh` (7 ADDED) and `add-unclassified-finding-class`
(1 ADDED) — both all-ADDED, neither touching any requirement named here, so
there is no collision in either direction. **Rejected:** a `MODIFIED` block over
the classification requirement, which would restate promoted prose wholesale to
add one sentence, and put canon at the mercy of archive order for no gain.

**OD-3 — THE `"unknown"` SPLIT SHIPS AS REALIZATION UNDER EXISTING CANON, WITH NO
REQUIREMENT OF ITS OWN.** The promoted `ideation-cross-reference` generator
requirement already says the condition named must be the one that actually held,
and the promoted vocabulary already says a generator that can distinguish must
reach for the stronger member. Both were promoted on 2026-08-28. Four sites
violate them. A requirement restating an obligation whose text already decides
the case is canon inflation, and this capability carries a promoted family whose
whole purpose is to police exactly that kind of restatement.
**THIS IS NOT A DELTA-LESS PACKET AND THE DISTINCTION IS THE POINT.**
`supersede-lost-pin-baseline` OD-3 declined a delta-less shape on a measurement
— every archived change in this repository carried a spec delta — and that
measurement was re-taken here: **112 of 112 archived changes carry one today.**
This packet carries one, from defect 1. What OD-3 decides is only that defect 3
does not need a SECOND one. **Rejected:** an ADDED requirement saying "one
emission site, one condition", which is the same sentence promoted canon already
carries with a scenario attached.

**OD-4 — THE REMEDY IS A TRAILING HEXADECIMAL BOUNDARY, NOT A WHOLE-VALUE
REWRITE.** The four expressions gain `(?![0-9a-fA-F])` after the value group —
the identical construction `LOOSE_SHA_RE` already carries, so the module states
the rule once and applies it consistently. Verified against the fix: the
sixty-four-character case matches nothing (no backtracking route exists, because
`\s*"?` cannot consume a hexadecimal character to re-anchor the group), and all
six conforming shapes tested still match. **Rejected:** re-anchoring the value
group to "the whole scalar, then test its shape", which is what the WIDE regexes
already do on the classification path. It would work, and it would make the
narrow path a second implementation of the wide path's scalar grammar — two
grammars to keep in agreement where one boundary character suffices. A leading
`(?<![0-9a-fA-F])` is NOT added: `\s*"?` already anchors the group's start, so it
would be inert, and an inert guard reads as a live one.

**OD-5 — THE INHERITED RECORD IS CORRECTED ON TWO COUNTS RATHER THAN RESTATED.**
§ 5.5 named two fabricating expressions; there are four. § 5.6 named three
`"unknown"` sites all owing a split; there are five, one of them fires on two
conditions, and one of them is already correct. Both corrections are stated in
§ What was measured with the measurement behind them, because a packet that
inherits a count and repeats it teaches the next reader to trust the count
rather than the file. **Rejected:** filing on the inherited numbers and noting
the difference at realization, which is how a filing's own premise goes
unmeasured.

## Open Questions

Each carries a RECOMMENDATION and no decision.

**Q1 — Should the refused value produce a distinct finding, or ride the existing
undeclared-non-commit defect?** Today a sixty-four-character value under a swept
key already produces the classification defect; after the fix it produces that
and nothing else. A distinct "malformed pin value" finding would tell a reader
that the value was *pin-shaped and rejected* rather than merely *not declared*.
**RECOMMENDATION: ride the existing defect.** The promoted classification
requirement already forbids the verification from telling a truncated object
name apart from an invented spelling — "the remedy is the same for all of them:
declare the value or fix the generator" — and adding a class the canon says not
to distinguish would contradict a requirement promoted this month.

**Q2 — Should `cli.py`'s return-code branch treat a non-zero `git log` as
`unreadable-repository`, or refuse to emit at all?** A generator that cannot run
git arguably should fail rather than record a sentinel.
**RECOMMENDATION: `unreadable-repository`.** That is precisely the condition the
member declares, the promoted requirement's scenario names omission and
placeholders as the wrong answers, and this is an experiment lane whose evidence
record is more useful with an honest condition in it than absent.

**Q3 — Should a generator be obliged to IMPORT the declared spelling rather than
retype the literal?** The vocabulary module says so in its own prose; no promoted
requirement does. `snapshot_registry.py` importing `pin_sentinels` also crosses a
package boundary (`scripts/ideation_dashboard/` → `scripts/doc_health/`), which
is a real coupling question rather than a style one.
**RECOMMENDATION: import it, and legislate nothing.** `pin_sentinels` is
stdlib-only by design, explicitly so that standalone scripts can import it
without dragging a package in. Do it here, and raise a requirement only if a
second generator retypes a literal — which is the evidence a rule would need.

**Q4 — Should the boundary be enforced structurally rather than by review?** A
future class member could declare a new prose `pattern` without the boundary,
and the requirement's fourth scenario would be violated silently.
**RECOMMENDATION: a test over the declaration, not a runtime check.** Assert that
every site-building expression in the module rejects an over-long hexadecimal
run — which pins the rule to behaviour rather than to the spelling of a regex,
and is the mutation-resistant shape this suite already prefers.

## Impact

* **Capabilities:** `doc-health` 38 → 39 requirements. `ideation-cross-reference`
  unchanged at 18 — defect 3 realizes its existing canon (OD-3).
* **Corpus:** no committed artifact edited. The declared pin class's report is
  expected byte-identical at realization apart from the module's own line
  numbers; that identity is the realization's check, not its assumption.
* **Consumers:** none. The four expressions are private to `pin_class.py`; the
  sentinel spellings moved are already declared, so a consumer using
  `pin_sentinels.is_declared_sentinel` keeps answering the same way.
* **Risk:** the fix is a refusal, so its failure mode is a MISSED pin rather than
  a false one. Guarded by the third scenario and by the class's own site count,
  which must not move at realization.
* **Sibling:** `fix-content-resolution-conflation`, the third defect of the same
  commissioned set, filed separately (OD-1).
