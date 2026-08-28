---
code_surface: openxFactory (a declared sentinel vocabulary living beside `scripts/doc_health/pin_class.py` — the registry-module home Q1 of `govern-derived-pin-reachability` ruled for the pin class itself, whose exact placement is OD-2 and is NOT pre-placed by the delta; `scripts/doc_health/pin_class.py` — the sweep's value handling, which today matches `([0-9a-f]{40})` and therefore creates no site at all for a non-commit value, plus the report's fifth outcome and the two-direction declaration check; `scripts/bootstrap-ideation-cross-reference.py` — `git_generation()` at `:144-154`, the dirty-tree stamp this packet exists to fix; `scripts/proposal-support.py` — `repo_revision()` at `:175-180` and the three `== "uncommitted"` guards at `:184`, `:632` and `:737`, whose spelling drift is already a measured latent raise; plus regressions under `tests/doc-health/`. NO change is proposed to the declared `PIN_CLASS` rows, `PIN_KEY_VOCABULARY`, the ref set consulted, `KNOWN_LOSSES` or its discharge mechanism, `repair_route()`, the retention namespace, the deterministic check family registry `scripts/doc_health/families.py`, the family enumeration or its numerals, `health/dispositions.yaml`, or one byte of any committed manifest.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle, measured rather than assumed: `grep`ing every `contracts/releases/*.digests.yaml` inventory for `pin_class`, `bootstrap-ideation-cross-reference` and `proposal-support` returns nothing, so no schema moves, no digest set changes, and no release tag is owed. The archive gate is therefore merge-plus-green on main: `python3 -m pytest tests/doc-health` green under `set -o pipefail`, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and the declared class reporting its sentinel sites as legal non-pins with the vocabulary check green in both directions. THE CHANGE SHIPS ACTIVE and archives only after that.
Status: ratified
Ratified: 2026-08-27 by Brett — in-session commissioning of the filing, verbatim: "file the sentinel-vocabulary follow-up change". THE CITATION COVERS THE DECISION TO FILE THIS CHANGE AND NOTHING ELSE. AS FIRST WRITTEN this line continued "the five decisions in § Orchestrator decisions below were taken by the authoring session under standing patterns and are NOT covered by it, nor are the four questions in § Open Questions" — true at authoring and now historical: **a THIRD act, later the same day, disposed everything this citation did not reach.** All five § Orchestrator decisions were CLEARED AS AUTHORED and all four § Open Questions RULED on 2026-08-27, by a four-question multi-choice put to Brett by the orchestrating session and relayed the same day; he took the packet's recommendation on every question, and the merge was approved on green, to be performed by the orchestrating session rather than this one. **THE THREE ACTS STAY DISTINCT ON PURPOSE**: the earlier ruling CONSTITUTED the packet's scope, this citation ADMITTED it, and the later ruling CLOSED the veto window and moved delta text on Q1, Q2 and Q3. A separate and EARLIER ruling of the same day constituted the packet's scope rather than ordering it — selected verbatim as "Named follow-up (Recommended): Record it beside the §5.3 git_generation() follow-up — they're the same idea (honest non-pins) and should be one future packet" — and it is recorded in `.openspec.yaml` as a distinct act. The record this citation resolves against is this file, § Orchestrator decisions and § Open Questions. No approving OpenSpec change exists to name, so the citation takes the record spelling `sanction-ratified-record-spelling` sanctioned for exactly that case, and clears its three-way floor on all three axes rather than on the one it needs: approver (`by Brett`), date (`2026-08-27`), and a resolvable record path.
Proposed: 2026-08-27
Origin: The one follow-up two archived packets agreed was a single question. `harden-ideation-readiness-check` § 5.3 recorded that `git_generation()` pins `HEAD` on a dirty tree. `govern-derived-pin-reachability` § 5.1 carried that item forward, found the sentinel practice while realizing, and Brett ruled at that archive that the two are the same idea — honest non-pins — and belong in one future packet. This is that packet, and re-measuring its own premise on the day of filing changed what it is for.
---

# Proposal: declare-sentinel-pin-vocabulary

## Why

This repository has two ways to record where an artifact came from, and only one
of them is governed.

A pin that names a commit is now thoroughly governed: it must stay resolvable,
an orphan is a defect rather than staleness, the repair is retention rather than
editing the record, an unrecoverable loss is declared and discharged by a
superseding record, and a declared class of pin-carrying artifacts is swept and
verified every run. Three archived packets across two days built that, and the
class reports itself fully verified.

The other way is to write something that is honestly not a commit — because the
content came from a working tree nobody committed, because the artifact was
produced outside any repository, because the revision could not be read at all.
That practice EXISTS in this repository, in seven committed artifacts. It is
governed by nothing, declared nowhere, spelled six different ways, invisible to
the verification, and already the cause of one latent crash.

**AND THE UNGOVERNED HALF IS THE WORSE DEFECT OF THE TWO.** An orphaned pin was
true once: somebody derived the artifact from a real state and something later
made that state unreachable. A pin stamped from `HEAD` while the generator reads
a dirty tree was NEVER true. It names a commit that resolves perfectly and
describes content no commit ever held, so a reader who checks it gets an answer,
and the answer is wrong. There is no repair route because nothing is missing.
`git_generation()` does exactly this today.

## What was measured

Every number was measured on 2026-08-27 in a fresh worktree off `origin/main` at
`b5fb03f3`, and re-measured rather than copied from the archived records that
state some of them.

**THE `git_generation()` DEFECT STANDS, UNCHANGED.**
`scripts/bootstrap-ideation-cross-reference.py:144-154` runs `rev-parse HEAD`
and writes it as `generation.source_revision` into `ideation/cross-reference.yaml`.
There is no `status --porcelain`, no `diff --quiet`, no sentinel branch and no
fallback of any kind; `check=True` means a git failure raises rather than
degrading. Flagged at `harden-ideation-readiness-check` § 5.3, carried forward
unticked at `govern-derived-pin-reachability` § 5.1, and untouched by either.

**THE SENTINEL SITES, RE-COUNTED FROM THE DECLARED GLOBS.** Enumerating the four
`proposal-support-manifest` path globs the pin class declares yields 34 committed
manifests: **24 carry a real forty-character pin, six carry
`"uncommitted-worktree"`, one carries `"not-applicable-ad-hoc"`, and three carry
no `source_revision` key at all.** The archived count is confirmed exactly. All
ten non-pin manifests, and all seven sentinel-valued ones, sit inside ARCHIVED
packets; not one is active.

**THE CORRECTION THAT CHANGES WHAT THIS PACKET IS FOR.** The record this packet
inherits states that the proposal-support generator "already refuses to write a
pin it cannot mean" and that the sentinel is deployed behaviour awaiting
generalization. **Measured, it is not.** `git log -S"uncommitted-worktree" --
scripts/` is EMPTY across all history, and so is the same search for
`"not-applicable-ad-hoc"`: neither string has ever existed in any script in this
repository. The generator is `scripts/proposal-support.py:175-180`:

```python
def repo_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "uncommitted"
```

It emits a THIRD spelling, `"uncommitted"`, and only when `rev-parse` EXITS
NON-ZERO — no git, no repository, an unborn `HEAD`. **Never on a dirty tree.** It
carries the identical defect `git_generation()` does. The seven sentinel values
were written BY HAND into manifests, one packet at a time; the corroborating
evidence is in the manifests themselves, which carry a prose `source_state` key
the generator never writes and a null `source_path` where the generator always
writes a real one.

**THAT MAKES THE CASE STRONGER, NOT WEAKER**, and it is the reason this packet
files rather than shrinking. The practice is real and it was right seven times
out of seven. What it has never had is a generator, a declaration, or a consumer
— which is precisely the gap a shared declared vocabulary closes, and precisely
what a "generalize the deployed behaviour" framing would have understated.

**THE DRIFT IS ALREADY A LATENT FAULT, RUN RATHER THAN PREDICTED.** Three guards
in `scripts/proposal-support.py` — lines 184, 632 and 737 — compare the revision
against the literal `"uncommitted"`, so `"uncommitted-worktree"` is not
recognized by any of them and falls through into `git_blob_sha256`, whose strict
40-or-64-hex check raises. Executed against this worktree:

| Call | Result |
| --- | --- |
| `git_blob_sha256(root, "uncommitted-worktree", "README.md")` | raises `SupportError: invalid repository revision: uncommitted-worktree` |
| `git_blob_sha256(root, "uncommitted", "README.md")` | returns `None` |

It is LATENT rather than live for one reason only: the crashing guard is on the
active-support path, and all seven sentinel manifests are archived. The day a
packet writes `"uncommitted-worktree"` into an active manifest carrying a
`source_sha256`, the verify sweep raises instead of returning findings.

**THE SENTINELS ARE INVISIBLE TO THE VERIFICATION, AND INVISIBLE IS NOT
EXCLUDED.** `scripts/doc_health/pin_class.py` binds the value group of both site
constructors to a commit shape — `_field_re` builds
`…{key}"?\s*:\s*"?([0-9a-f]{40})"?` and `_VOCAB_RE` uses the same value group —
so a sentinel value produces **no `PinSite` at all**. It is not reachable, not
orphaned, not lost, and **not uncovered**. The file is swept, the key is
declared, the member is in good standing, and the value is skipped. The probe
run here at `b5fb03f3` reports:

> 65 declared pin sites across 22 class members — **50 reachable, 0 orphaned, 1
> lost (declared unrecoverable, 0 awaiting a superseding record), 0
> inconclusive; 0 uncovered sites, 0 vanished members, 0 future members now
> carrying pins**

A fully verified class, over seven committed artifacts whose central provenance
claim nothing has ever read. That is the silent-coverage shape the declared class
was built to end, arriving through the VALUE instead of through the key — and the
class does not close it, because it declares which keys carry pins and never what
a non-commit value in one of them means.

**SIX UNDECLARED SPELLINGS ALREADY EXIST**, found by sweeping every site that
stamps a revision into generated output rather than by guessing:

| Spelling | Where it is written | Condition it stands for |
| --- | --- | --- |
| `"uncommitted"` | `scripts/proposal-support.py:180` | `rev-parse` failed |
| `"uncommitted-worktree"` | hand-written, six archived manifests | content taken from an uncommitted tree |
| `"not-applicable-ad-hoc"` | hand-written, one archived manifest | derivation performed outside a repository context |
| `"unknown"` | `scripts/ideation_dashboard/snapshot_registry.py:283`; `experiments/avatar-brokered-call/src/avatar_f0/cli.py:51,60` | revision unavailable |
| `"composed"` | `scripts/ideation_dashboard/snapshot_registry.py:647` | a composed view with no single source revision |
| `"not-applicable"` | `scripts/doc_health/pin_class.py:1353` | a verdict constant, not a pin value — adjacent, and named so nobody assumes it is a member |

Six spellings, no shared declaration, and each invisible to every consumer
written against a different lane's spelling. `"unknown"` and `"composed"` are
mentioned in no governance document at all.

**AND THE OTHER GENERATORS HAVE THE SAME SHAPE.** `_head_sha()`
(`nightly_lane.py:117`), `git_head_revision()` (`dashboard_refresh_lane.py:643`)
and `RealGit.head_sha()` (`doc_health/corpus.py:534` — the widest-fanout pin
source in the repository, feeding the readiness, possibles, organizer,
neutrality, inventory and family lanes) all run `rev-parse HEAD` with no
cleanliness check. **Three sites already do it right**, which is the proof that
the rule is implementable rather than aspirational:
`ideation_dashboard/record_binding.py:202-210` requires the file committed at
`HEAD` **and** `diff --quiet HEAD -- <rel>` clean before binding;
`intent_apply_lane.py:560` refuses on `status --porcelain` output; and
`register_edit_lane.py:223` runs `diff --quiet` before pinning.

## What this changes

- **A generator that cannot truthfully pin a commit writes a declared sentinel**
  — one value per condition, shared across every generator, never a commit name
  that never described the content and never a free-form string.
- **`git_generation()` and every generator of its shape emit a sentinel on a
  dirty tree**; a clean tree keeps the real pin, unchanged.
- **The verification classifies a non-commit value** into exactly two outcomes: a
  declared sentinel is a LEGAL NON-PIN — a fifth outcome beside reachable,
  orphaned, lost and uncovered — and an undeclared one is a defect naming the
  artifact, the key and the value.
- **The vocabulary is declared beside the pin class and checked in both
  directions** over the pin class's own inventory: a spelling in the corpus that
  the declaration lacks is reported, and a declared member nothing carries is
  reported too.
- **The seven committed sentinels are grandfathered as they stand**, declared
  rather than rewritten, with one spelling per condition marked canonical and the
  rest marked legacy.

## What this deliberately does not change

- **The reachability rules, in either capability.** "A committed derivation pin
  stays resolvable" and "An orphaned pin on an immutable record is repaired by
  retention, never by editing the record" are neither restated nor MODIFIED, and
  neither is the promoted class-wide verification requirement. A sentinel is not
  a pin, so none of them reaches it; this delta answers only what happens where
  no commit is named.
- **`KNOWN_LOSSES`, the discharge mechanism, `repair_route()`, the retention
  namespace, the ref set.** A legal non-pin has no repair route because it has no
  defect, and offering one would be a category error.
- **The declared `PIN_CLASS` rows and `PIN_KEY_VOCABULARY`.** The scope of this
  check is the pin class's own inventory, deliberately — a vocabulary checked
  over a wider or narrower set than the pins it qualifies reports gaps the pin
  class does not have and misses gaps it does.
- **One byte of any committed manifest.** All seven sit in archived packets.
- **The deterministic check families and their numerals.** No family is added,
  removed or renumbered, and the enumeration requirement is not restated.
- **`health/dispositions.yaml`.** This verification registers no check family, so
  it emits no `(family, repo, path)` tuple for a disposition to match — the same
  measurement `supersede-lost-pin-baseline` made, and the same conclusion.
- **The three manifests with no `source_revision` at all.** An absent key is a
  fourth state, not a sentinel. **RULED 2026-08-27 (Q2): it stays that way** — the
  declaration RECOGNIZES absence as a legacy state so it is visible, and refuses it
  membership; no absent key is filled in with a sentinel after the fact.

### Named follow-ups, out of scope here

- **THE OTHER GENERATORS ARE NOT REPAIRED BY THIS PACKET, ONLY BOUND BY IT.**
  `git_generation()` is repaired because it is the named defect. `corpus.py`'s
  `head_sha()` seam feeds six lanes and a cleanliness check there changes six
  record families at once; that is a sweep with its own evidence, and this packet
  states the rule it would be measured against rather than performing it.
- **CROSS-REPOSITORY PINS STAY OUT**, exactly as `govern-derived-pin-reachability`
  § 5.2 left them. A gitlink, a `pinned_contract_manifest` entry, a release digest
  and an image digest all name state in another repository, and whether a
  sentinel is even meaningful for them is a different question with a different
  authority.
- **`"composed"` MAY NOT BE A SENTINEL AT ALL.** A composed view genuinely has no
  single source revision, which is a different fact from "I could not read one".
  Q3 recommends declaring it; if that recommendation is wrong, the honest answer
  is a different key rather than a vocabulary member, and that is a schema change
  this packet does not make.

## Orchestrator decisions, cleared 2026-08-27 (authored: flagged for veto)

**ALL FIVE CLEARED AS AUTHORED, 2026-08-27**, by a four-question multi-choice put
to Brett by the orchestrating session and relayed to this session the same day. On
every question he took the packet's own recommendation, so **the clearance moves
nothing**: OD-1 (the two-capability all-ADDED split), OD-2 (the vocabulary beside
the pin class with no path in canon), OD-3 (grandfather the committed spellings
rather than normalize them), OD-4 (file on the corrected premise) and OD-5 (no
deterministic check family) all stand exactly as written below. No verbatim
wording of the ruling reached this session, so none is quoted — the approver, the
date, the mechanism and the selections are recorded instead, which is what the
origin requirement asks for. **THE ORIGINAL FLAGGED TEXT IS KEPT BELOW AS MARKED
HISTORY** rather than rewritten, because what was flagged and why is the part a
later reader needs. **THIS IS A SECOND ACT, DISTINCT FROM THE COMMISSION**
recorded in § Ratified: that one admitted the packet, this one closed the veto
window and approved the merge on green.

Every decision below was taken by the authoring session under standing patterns.
The commission covers the decision to file and nothing else.

**OD-1 — TWO CAPABILITIES, FOUR REQUIREMENTS, ALL ADDED.**
**CLEARED 2026-08-27 as authored.**
`ideation-cross-reference` gets the two GENERATOR rules (write a sentinel rather
than an untrue commit; declare the committed spellings rather than rewrite them),
because it owns the repo-local commit-pin obligation and the record-immutability
ordering that refuses the tidying repair. `doc-health` gets the two VERIFICATION
rules (classify the value; check the declaration over the class's inventory),
because it owns the pin verification and the proposal-support integrity checks.
**Alternative not taken:** everything in `doc-health`, which would have been one
file and would have put a rule about what a GENERATOR writes inside the
capability that only reads. The split follows the shape
`govern-derived-pin-reachability` used for exactly this pair. **All ADDED, none
MODIFIED**, and the collision check was run rather than assumed: the only active
change touching `doc-health` is `add-nightly-dashboard-refresh`, whose delta is
seven ADDED requirements about the refresh lane, and no active change touches
`ideation-cross-reference` at all.

**OD-2 — THE VOCABULARY LIVES BESIDE THE PIN CLASS, AND THE DELTA DOES NOT NAME
THE PATH.**
**CLEARED 2026-08-27 as authored.** Q1 of `govern-derived-pin-reachability` ruled the registry module for
the pin class itself, on the derived-not-restated shape
`add-family-enumeration-check` established; a vocabulary that qualifies that class
belongs in the same place and the same form. The delta obliges "declared in the
same place and the same form as the declared pin class" and stops there, because
a promoted spec that pins an implementation path has to be MODIFIED the next time
the module moves — the same handling that ruling gave requirement 4. **Whether it
is a new module or new constants inside `pin_class.py` is left to realization**,
and either satisfies the delta.

**OD-3 — THE COMMITTED SPELLINGS ARE GRANDFATHERED, NOT NORMALIZED.**
**CLEARED 2026-08-27 as authored.**
`"uncommitted-worktree"` and `"not-applicable-ad-hoc"` enter the vocabulary as
they stand. Two reasons and the second is decisive. First, they are the practice
that proved the idea and a declaration that erased them deletes its own
justification. Second, all seven sit inside archived packets, and this
capability's own rule refuses a content edit to captured material — the same
ordering that makes retention rather than re-pinning the repair for an orphaned
record pin. **The cost is stated rather than hidden:** the vocabulary carries more
than one spelling for one condition, which is why the delta obliges a canonical
member and legacy markings rather than treating all members as equal.

**OD-4 — THE PACKET FILES ON A CORRECTED PREMISE, AND THE CORRECTION IS
RECORDED.**
**CLEARED 2026-08-27 as authored.** The archived record and the README entry derived from it both state
the generator already emits sentinels. It does not, and the measurement is in
§ What was measured. **Filing anyway is a decision**, and the argument for it is
that the correction strengthens the case: a practice that lives in seven
hand-written artifacts and no generator is more in need of a declaration than one
already deployed, and the vocabulary drift it produced is already a measured
latent raise. **The alternative was to file a smaller packet** that only fixed
`git_generation()` and left the vocabulary question to a later ruling, which
would have re-deferred the half Brett's earlier ruling explicitly joined to it.

**OD-5 — NO DETERMINISTIC CHECK FAMILY, AND THE ENUMERATION IS NOT RESTATED.**
**CLEARED 2026-08-27 as authored.**
Both sibling packets declined a family for reasons that hold here unchanged: the
verification this classification rides in already answers differently at
different clone depths, and the enumeration requirement is one every new family
must restate in full, so a `MODIFIED` block over it makes canon depend on archive
order. `add-family-enumeration-check` holds the active block. **The consequence is
stated:** the enforcement surface stays pytest plus the module's own runnable
entry point, and this packet does not wire the preflight half either — the three
reasons `govern-derived-pin-reachability` § 5.6 measured are unchanged.

## Open Questions, all four ruled 2026-08-27

All four were ruled by the same four-question multi-choice recorded in
§ Orchestrator decisions, and on all four Brett took the packet's recommendation.
No verbatim wording reached this session, so none is quoted — approver, date,
mechanism and the option selected are stated instead. **THREE OF THE FOUR MOVED
DELTA TEXT**, and each entry records exactly what moved; each question's original
text is kept unchanged beneath its ruling, because a recommendation that was
accepted is the argument for the rule now in the delta.

**Q1 — RULED 2026-08-27: DECLARE BOTH SPELLINGS, WITH DISTINCT MEANINGS.**
`"uncommitted-worktree"` is canonical for the DIRTY-TREE condition and
`"uncommitted"` is its own member meaning UNREADABLE REPOSITORY — two members,
each canonical for its own condition, neither legacy relative to the other. The
recommendation was taken as authored. **WHAT MOVED:** the
`ideation-cross-reference` grandfathering requirement gains a paragraph obliging
the declaration to ESTABLISH WHICH CONDITION EACH SPELLING NAMES BEFORE marking
any of them legacy — because folding a second condition into the first as a
legacy spelling would silently restate every artifact carrying it — plus one
scenario, "Two spellings turn out to name two conditions". The canonical/legacy
machinery is unchanged and now applies WITHIN a single condition rather than
across resemblances. **This unblocks `tasks.md` § 2.1**, which moves from "settle
Q1 first" to the settled answer. **ONE POINT NEITHER RULING SETTLES, recorded
rather than invented:** Q3 admits `"unknown"`, which also stands for an
unreadable revision, so whether it is a second spelling of `"uncommitted"`'s
condition (and therefore which of the two is canonical for it) or a distinct
condition is left to realization under the same-condition rule. Neither ruling
reached it and this session does not decide it.

**Q1 AS ASKED — WHICH SPELLING IS CANONICAL FOR THE DIRTY-TREE CONDITION?** Two candidates
and neither is free. `"uncommitted-worktree"` is the committed practice — six
artifacts — but is written by no code and is the exact string that raises in
`proposal-support.py`. `"uncommitted"` is written by the only generator that
writes anything, and is the string three live guards already compare against, but
it names the wrong condition: it fires on `rev-parse` failure, not on a dirty
tree. **RECOMMENDATION: declare both, with `"uncommitted-worktree"` canonical for
the dirty-tree condition and `"uncommitted"` declared as its own member for the
unreadable-repository condition, since those are two different facts and the
corpus already spells them differently.** The three guards are then reconciled
against the declaration rather than against one literal, which repairs the latent
raise as a consequence rather than as a separate act.

**Q2 — RULED 2026-08-27: AN ABSENT KEY IS NOT AN HONEST NON-PIN.** It is declared
a RECOGNIZED LEGACY STATE of the corpus and NOT a vocabulary member — the
recommendation taken as authored. **WHAT MOVED:** the `doc-health` declaration
requirement gains a paragraph obliging the declaration to name absence as a
legacy state so it is visible rather than falling outside both the pin path and
the sentinel path, while refusing it membership and refusing to fill an absent key
with a sentinel after the fact — absence records no condition to assert — plus one
scenario, "An artifact carries no pin key at all". The
`ideation-cross-reference` generator requirement gains the matching sentence for
the same reason. The two states are reported differently and neither is converted
into the other: a recognized legacy absence is reported once and repaired never,
where an undeclared spelling is a defect with a remedy.

**Q2 AS ASKED — IS AN ABSENT PIN KEY AN HONEST NON-PIN OR A DEFECT?** Three archived
manifests carry no `source_revision` at all, and they are visibly truncated
stubs — one carries only `change_id` and `files`. **RECOMMENDATION: absent is NOT
a sentinel and MUST NOT be converted into one.** A missing key says nothing:
it cannot be told from a generator that crashed, a schema that predates the key,
or a hand-written stub, where a sentinel names which condition applied. But that
leaves three sites outside the vocabulary and outside the check, so the
recommendation is to declare the absence a LEGACY STATE — reported once,
repaired never, because the artifacts are archived and immutable. **If Brett reads
an absent key as the same defect class, this is the question to rule the other
way**, and the cost is a schema obligation on a generator family whose committed
instances cannot be edited to satisfy it.

**Q3 — RULED 2026-08-27: BOTH JOIN THE DECLARED VOCABULARY.** `"unknown"` and
`"composed"` are members — the recommendation taken as authored, including the
harder half. **THE REASON THE RULING GAVE IS THE ONE THIS PACKET HAD NOT
STATED**, and it is recorded because it is a real constraint on realization: if
they stayed out, requirement 2's undeclared-value-is-a-defect clause would flag
the snapshot registry's OWN COMMITTED OUTPUT the day the branch was switched on.
**WHAT MOVED:** the `doc-health` classification requirement gains a paragraph
obliging that every non-commit spelling the corpus already carries be RESOLVED —
declared where it names a real condition, corrected at its generator where it does
not — before the defect branch runs, with the trade stated in the same breath so
it cannot be read as an amnesty: an unresolved spelling is a defect the moment the
branch runs. One scenario is added, "A spelling the corpus already carries is not
yet declared". **§ 5.3's caveat survives the ruling unchanged**: if `"composed"`
turns out to belong in a different KEY rather than a pin key, that is a schema
change to the snapshot index and still not this packet's to make.

**Q3 AS ASKED — DO `"unknown"` AND `"composed"` JOIN THE VOCABULARY?** Both stand in
`source_revision`-shaped fields today and neither is declared anywhere.
**RECOMMENDATION: `"unknown"` joins as a member** — it is a pin key's value
standing for an unreadable revision, which is exactly a condition the vocabulary
covers. **`"composed"` is the harder one and the recommendation is to declare it
too**, with its own condition ("a projection composed from several sources, with
no single source revision"), because leaving it undeclared reproduces exactly the
gap this packet closes. The alternative — that a composed view should carry a
different KEY rather than a sentinel value in a pin key — is cleaner and is a
schema change to the snapshot index, which is why it is a question rather than a
decision.

**Q4 — RULED 2026-08-27: YES, THE REPAIR IS IN SCOPE FOR THIS REALIZATION.** The
three literal-`"uncommitted"` guards are reconciled against the declaration — the
recommendation taken as authored, and the "against it" argument below is
overruled rather than quietly dropped: the code surface does widen into a tool
this packet otherwise only reads, and the ruling accepts that cost. **WHAT MOVED:**
no delta text, because the obligation was already stated — the
`ideation-cross-reference` consumer scenario already makes a guard that
recognizes one spelling a reported coverage gap. `tasks.md` § 2.7 moves from
conditional to unconditional and the `code_surface` line already named the three
guards. **AND Q1 SHARPENS THE REPAIR RATHER THAN COMPLICATING IT**: with
`"uncommitted"` ruled a member in its own right, the guards are not being taught a
new synonym — they are being taught that the condition they test for has more than
one member, which is exactly what consulting the declaration means.

**Q4 AS ASKED — DOES THE REALIZATION REPAIR THE `proposal-support.py` GUARD DRIFT?** The
three `== "uncommitted"` comparisons are a measured latent raise, caused by the
very vocabulary drift this packet declares away. **RECOMMENDATION: yes, in the
same realization.** A packet that declares a shared vocabulary while leaving a
live guard that crashes on one of its members is incoherent, the repair is small
(consult the declaration instead of a literal), and the delta already obliges it
— "a consumer that recognizes only one spelling" is a reported coverage gap.
**Against it:** it widens the code surface into a tool this packet otherwise only
reads, and the fault is not reachable today.

## Impact

- **Affected capabilities:** `ideation-cross-reference` — two ADDED requirements,
  **nine** scenarios; `doc-health` — two ADDED requirements, **ten** scenarios.
  **No requirement MODIFIED in either**, and no deterministic check family added,
  removed or renumbered. **AS AUTHORED the counts were eight and eight**; the
  2026-08-27 rulings on Q1, Q2 and Q3 added three scenarios and four paragraphs
  and removed nothing, so the growth is additive and the requirement count is
  unchanged at four.
- **Affected code:** a declared vocabulary beside `scripts/doc_health/pin_class.py`,
  the sweep's value handling and report in `pin_class.py`, `git_generation()` in
  `scripts/bootstrap-ideation-cross-reference.py`, the three drifted guards in
  `scripts/proposal-support.py` (Q4), and regressions under `tests/doc-health/`.
- **Affected records:** none issued, none edited. All seven sentinel-carrying
  manifests are archived and stay byte-identical.
- **Contract bundle:** none owed, measured.
- **Discharges:** `harden-ideation-readiness-check` § 5.3 and
  `govern-derived-pin-reachability` § 5.1 — the two items Brett ruled were one
  packet.
