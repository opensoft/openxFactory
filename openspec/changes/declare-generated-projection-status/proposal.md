---
code_surface: openxFactory (`scripts/doc_health/__init__.py` — one value added to `TAXONOMY`, with the re-derivation test that distinguishes it from `record` in a comment; `scripts/doc_health/promotion_fidelity.py` — one value added to `RATIFIED_OR_BEYOND`, because that split's two sets are asserted to EXHAUST the taxonomy and a ninth standing forgotten there would land in the presumed-ratified bucket in silence; `scripts/sync-notebooklm-books.py` — the closed `STATUS_RE` alternation gains the value, so a projection is skipped by RULE (it is absent from `PROJECTED_STATUSES`, as `record` is) rather than by a regex that never heard of it; `contracts/schemas/ideation-dashboard-snapshot.schema.yaml` — the `lifecycle_status` enum, which fails snapshot validation on a value it does not carry; `scripts/render-ideation-cross-reference.py` — the one line that EMITS the header, so regeneration cannot reintroduce `record`; `ideation/cross-reference.md` — regenerated, a one-line diff; `docs/document-lifecycle.md` — the taxonomy table gains a row, the "generated evidence is always `record`" bullet is corrected to say CAPTURED ONCE, and the Gates-In-Practice line gains its clause; `tests/doc-health/test_families.py` — one added test asserting both halves, that the value is CONTROLLED and that it is NOT a record, with the negative-then-positive pairing. NO change to `fam_record_immutability` itself, to `fam_status_validity`, to the family registry, to the family enumeration or its numerals, to any family's scope or basis, to `health/dispositions.yaml`, to the report schema, or to any threshold. NO family is skipped and NO finding is suppressed.)
target_release: implemented — the openxFactory main line. This surface cuts NO contract bundle, measured rather than assumed: `contracts/schemas/ideation-dashboard-snapshot.schema.yaml` is the one edited file under `contracts/`, and it is a member of NO `contracts/releases/*.digests.yaml` inventory — grepped across all 48, zero hits, as for every other path this change touches. The inventories are confined to the hermes-runtime contract surface. So no digest set moves and no release tag is owed. The archive gate is therefore merge-plus-green on main: `python3 -m pytest tests/doc-health` green, `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green, and a doc-health single-repo run whose `record-immutability` count falls by exactly one and whose every other family is unmoved. THE REALIZATION RIDES IN THE PROPOSING PULL REQUEST: the code is six one-line edits and one regenerated projection, and the argument for the value is inseparable from the value. ONE ACT IS OWED IN ANOTHER REPOSITORY and it is NOT owed by this pull request — see § The disposition this owes elsewhere. The change ships ACTIVE and archives only after the merge AND that act.
Status: draft
Proposed: 2026-08-28
---

# Proposal: declare-generated-projection-status

## Why

`ideation/cross-reference.md` says, on line 8, **"GENERATED FILE — do not edit
by hand."** It says, on line 3, `Status: record`.

Those two lines cannot both be honoured. `record` means immutable evidence, and
`record-immutability` reports "record document changed after capture" as a
CRITICAL. But the file is a deterministic rendering of
`ideation/cross-reference.yaml`, rewritten in place by
`scripts/render-ideation-cross-reference.py` — so the ONLY correct way to update
it is the very act the family reports as a defect. Five commits on `main` touch
it — `acbc98fe` created it and the other four RE-RENDERED it — and the critical
has stood through them, named as pre-existing by three separate archived
packets rather than fixed.

**And promoted canon already agrees the header is wrong.**
`openspec/specs/ideation-cross-reference/spec.md:449-452`:

> - **WHEN** the orphaned pin is carried by a generated artifact that is not a
>   `record` — **the cross-reference index and its rendered twin among them**
> - **AND** the record-retention route is not owed for it, because nothing about
>   a regenerable projection is immutable evidence

"Its rendered twin" is this file. Canon says it is not a record. The file says
it is. That contradiction is promoted, live, and citable, and no change has ever
ruled the other way.

The root cause is a conflation dating to the vocabulary's first day. The
original migration mapping (`archive/2026-07-09-add-document-lifecycle-vocabulary/design.md:67`)
mapped "generated simulation report / generated runbook / simulated reviews" to
`record` — all one-shot captures. **Being generated was taken to be what makes a
document a record.** It is not. Being CAPTURED is. In 2026-07-09 no re-derived
projection existed, so the distinction was never drawn.

## What was measured

Measured 2026-08-28 in a fresh worktree off `origin/main` at `6d100e51`.

**THE CLASS IS EXACTLY ONE DOCUMENT.** Every `*.md` under the five governed
roots was scanned for a GENERATED / do-not-edit marker inside the header window.
`ideation/cross-reference.md` is the only hit. This change therefore widens the
taxonomy for a class of one — stated plainly rather than dressed up, and
addressed in OD-2.

**THE ADJACENT ARTIFACTS THAT MUST NOT MOVE, AND DO NOT.**
`health/ideation-readiness/*/*.yaml`, `health/derive-possibles/*/*.yaml` and the
dated `health/reports/YYYY-MM-DD.md` are all generated and all correctly
`record`: each is written ONCE to a dated path, and a second run writes a
different path. `openspec/specs/doc-health/spec.md:171-183` mandates `Status:
record` for the run's own report, and that requirement is neither touched nor
contradicted — the line this change draws is re-derived-in-place versus
captured-once, and every one of those falls on the `record` side.

**THE CONSUMER CHECK, run before the value was chosen.** Every reader of
`ideation/cross-reference.{md,yaml}` was enumerated and asked whether it reads
the `Status:` header:

| Consumer | Reads the status? | Effect |
| --- | --- | --- |
| `scripts/validate-ideation-cross-reference.py` | **No** — keys on the YAML `kind:` field | none |
| `scripts/doc_health/pin_class.py` (both registry rows) | **No** — reads only the pin line / `Source revision:` | none |
| `scripts/doc_health/document_catalog.py` | No branch on this path | none |
| `scripts/ideation_dashboard/{register,lens,intent_apply_lane}.py` | **No** — read the YAML index | none |
| `scripts/doc_health/inventory.py` | Records the literal value, no branch | the row's value changes |
| `scripts/doc_health/corpus.py` → `ctx.docs` | **Yes** | the file leaves the `record` stage census |
| `scripts/sync-notebooklm-books.py` | **YES — load-bearing** | see below |
| `contracts/releases/*.digests.yaml` | **Zero hits** across all 48 | no bundle |

**`ideation/cross-reference.yaml` carries no status field at all** — zero
occurrences of the string `status` in 12,058 lines — and is unreachable by
doc-health regardless, because `corpus.iter_doc_paths` globs `*.md`. **The whole
problem lives in the `.md` alone**, so the YAML is not touched.

**THE ONE LOAD-BEARING CONSUMER, AND WHY THE VALUE HAD TO BE NEW.**
`sync-notebooklm-books.py` projects a document into a NotebookLM book only if
its status is in `PROJECTED_STATUSES` — `{brainstorm, staged, draft, ratified,
standard}`. `record` is excluded, which is why a 4,797-line generated index has
never been pushed into a book. **Every existing non-projected value was tried
against meaning and every one fails**: `superseded` and `retired` are false
about a live file, and `draft`, `ratified`, `standard`, `staged` and
`brainstorm` would all START projecting the index into a book. There is no
existing value that is both honest and inert. That is the measurement that
forced a ninth standing rather than a reuse, and it is recorded here because it
is the argument OD-1 rests on.

**THE EXTENSION POINT IS BUILT AND TESTED.** A ninth standing is not an
intrusion into this taxonomy; the repository already has a test whose docstring
anticipates one. `tests/doc-health/test_promotion_fidelity.py:635-643`:

> "A ninth standing added to `doc_health.TAXONOMY` and forgotten here would land
> in the presumed-ratified bucket in silence, which is the class of silence this
> ruling closed. This test is how it cannot."

It asserts `PRE_RATIFICATION | RATIFIED_OR_BEYOND == TAXONOMY`. The new value is
placed in `RATIFIED_OR_BEYOND`, where `record` already sits, for the same
reason: neither is a proposal standing, and that split's only question is
whether a packet declared a standing BELOW ratification.

**THE RESULT.**

| Family | Before | After |
| --- | --- | --- |
| `record-immutability` | **5 critical** | **4 critical** |
| `status-validity` | unchanged | unchanged |
| `promotion-fidelity` | 0 | 0 |
| `ratified-provenance` | 0 | 0 |

`ideation/cross-reference.md` leaves the list. The other four criticals —
`docs/archive-record-discrepancies.md`, `docs/domain-ontology-adoption-handoff.md`,
`docs/domain-ontology-pilot-report.md`,
`docs/notebook-projection-migration-evidence-2026-08-24.md` — are genuine
hand-maintained `record` documents, are untouched, and still fire.

**AND THE REGENERATION IS PROVEN DETERMINISTIC.** Before changing the emitter,
the renderer was run against the committed YAML into a scratch path and diffed
against the committed `.md`: **byte-identical**. After changing it, the
regenerated file differs from the committed one in **exactly one line**. So the
new header is the only thing this change writes into that file, and the
generator is demonstrably the file's only author.

## The mechanism, stated exactly

1. **`projection` joins the controlled taxonomy** as the ninth value. Its
   definition is not "generated" — a `record` is generated too. It is
   **RE-DERIVED IN PLACE from a declared source of truth**, and the test canon
   states is whether re-running the generator over the same path is the correct
   way to update the document.
2. **The generator emits it.** `render_markdown()` is the single line that
   writes the header, and all three writers of this file — the renderer, the
   bootstrap script, and the nightly `ideation_readiness` lane — funnel through
   it, so one edit covers every path and **regeneration cannot reintroduce
   `record`.** Canon pins that obligation in its own scenario.
3. **`record-immutability` is not touched.** It skips the file at its existing
   first statement, `if doc.status != "record": continue`, because the file is
   no longer a record. No allowlist, no path exception, no disposition, no
   `--skip-family`. **The family's behaviour is byte-for-byte what it was**, and
   it still reports all four real records.
4. **The three other vocabularies that would silently disagree are moved in the
   same commit** — the promotion-fidelity split, the NotebookLM regex, the
   dashboard snapshot enum — each with the reason in a comment at the site.

## The disposition this owes elsewhere

**This is the one obligation this pull request does NOT discharge, and it is
stated rather than left to be discovered.**

**REASSIGNED 2026-08-28, NOT DISCHARGED.** Brett's ruling of that day directs
that both pull requests merge on green and that **the entry described below is
written by the ORCHESTRATING SESSION as part of the merge sequence.** It is
still owed, still keyed exactly as stated, still in `opensoft/xFactory`, and
this packet still does not archive until it lands — the ruling names the
performer, not a waiver. The description that follows is kept unchanged, since
it is the specification the performing session works from.

`record-immutability` is in the CONTESTED resolution class. When a contested
finding present in the previous report is absent from the current one,
`report.uncited_resolutions` re-emits it as an
`uncited-resolution` ERROR — "contested record-immutability finding resolved
without citation" — unless an entry keyed `(family, repo, path)` disposes it.
So the nightly, which runs with `--previous-report`, will manufacture an error
the first time it sees this finding gone.

`health/dispositions.yaml` **does not exist in openxFactory**; it lives only at
the aggregation root. So the entry is owed in `opensoft/xFactory`, keyed
`(record-immutability, openxFactory, ideation/cross-reference.md)` and citing
this change. It is named in `tasks.md` § 5 as an act owed at realization in
another repository, and this packet does not archive until it lands.

**Not a workaround for anything.** The finding really is resolved, by a cited
change, which is exactly the case the disposition instrument exists to record.

## What this changes

- **The correct act stops being a critical finding.** Regenerating a projection
  is how a projection is maintained.
- **Canon stops contradicting itself.** `ideation-cross-reference` already said
  this file is not a record; now the file agrees.
- **The conflation is named and corrected.** "Generated" was never the property
  that makes a document immutable; "captured once" is.
- **The next projection has a home.** The class is one today; the rule is
  general, and the generator obligation means the next one cannot drift back.

## What this deliberately does not change

- **`fam_record_immutability`, `fam_status_validity`, or any family's code.**
  Not one line. The finding clears because the DOCUMENT changed class, which is
  what the ruling required.
- **`health/dispositions.yaml`, in this repository or by silencing.** The
  aggregation entry named above cites a change; it does not suppress a family.
- **The four other `record-immutability` criticals.** All genuine records, all
  still firing.
- **`ideation/cross-reference.yaml`.** No status field, unreachable by
  doc-health, and the source of truth rather than a projection of one.
- **`openspec/specs/doc-health/spec.md`'s health-report contract.** The dated
  run report is a one-shot capture and keeps `record`; the requirement is
  neither restated nor MODIFIED.
- **The family registry, the enumeration, the numerals, the report schema, any
  threshold.**

## Orchestrator decisions, cleared 2026-08-28 (authored: flagged for veto)

**CLEARED 2026-08-28**, by a multi-choice put to Brett by the orchestrating
session and relayed to this session the same day. The selections that reach
this packet: **the `projection` SPELLING IS APPROVED** — OD-1's departure from
the commission's first word stands as authored — and **both pull requests merge
on green**, which confirms OD-2's premise that this packet lands on its own
gate rather than folded into its sibling. On both he took the packet's own
recommendation, so **the clearance moves nothing**: not one of the seven sites
carrying the value is renamed, and the delta is untouched. OD-3 and OD-4 were
not put to him and are NOT covered; they stand as authored, still flagged.
**AND ONE OBLIGATION IS REASSIGNED, NOT DISCHARGED:** the aggregation
disposition entry § The disposition this owes elsewhere names is now the
ORCHESTRATING SESSION's to write as part of the merge sequence. It is still
owed, still keyed the same way, still in another repository — only the
performer changes, and this packet's archive still depends on it landing.
No verbatim wording of the ruling reached this session, so none is quoted —
the approver, the date, the mechanism and the selections are recorded instead.
**THE ORIGINAL FLAGGED TEXT IS KEPT BELOW AS MARKED HISTORY** rather than
rewritten: OD-1's argument is the reason the spelling is what it is, and a
later reader deciding what to call a tenth standing needs the argument, not the
verdict. This act is DISTINCT from the commission recorded in `.openspec.yaml`:
that one admitted the packet, this one closed the veto window on its spelling.



**OD-1 — THE VALUE IS SPELLED `projection`, NOT `generated`.**
**RULED 2026-08-28: `projection` APPROVED.** Brett was given the spelling, the
canon-legibility argument for it, and the mechanical-rename remedy, and
selected the packet's own recommendation. **Nothing moves**: `TAXONOMY`, the
promotion-fidelity split, the NotebookLM alternation, the dashboard enum, the
generator line, the regenerated file and the delta all keep the word they were
written with. The paragraphs below are kept EXACTLY as authored, because they
are the reason the taxonomy now distinguishes CAPTURED from RE-DERIVED, and a
later reader naming a tenth standing needs that reasoning. The veto branch this
decision named for itself was NOT taken. AS AUTHORED, kept: the commission
named "a `generated`/derived class", offering a shape rather than fixing a
spelling, and this takes the latitude deliberately — so it is flagged.
**The reason is canon legibility, and it is concrete.**
`docs/document-lifecycle.md` carries the bullet "Generated evidence … is always
`record`", which must SURVIVE, because one-shot captures do stay records. A
status literally named `generated` would put "generated evidence is always
`record`" one page from "`generated` is a status that is not `record`", and a
reader would have to reconstruct the distinction every time. `projection` states
the distinguishing property instead of the misleading one, and it is the word
**promoted canon already uses** for exactly this file — "a generated
projection", "a regenerable projection"
(`openspec/specs/ideation-cross-reference/spec.md:450-452`). **Alternative not
taken:** `generated`, matching the file's own banner and the commission's first
word. **If Brett prefers the ruled spelling this is the decision to veto** —
*and he did not; see the ruling marker at the head of this decision* — the
remedy is a mechanical rename across the seven sites listed in `code_surface`
plus the delta, and nothing about the argument changes.

**OD-2 — A NEW TAXONOMY VALUE FOR A CLASS OF ONE.** Measured: exactly one
governed document declares itself generated in its header. Widening a
controlled vocabulary for a single instance deserves an explicit defence, and
here it is. **Every existing value was tried and every one fails** (§ What was
measured): the five projected statuses would start pushing a 4,797-line index
into a NotebookLM book, and `superseded`/`retired` are false about a live file.
**And the two alternatives that avoid a new value were both rejected on the
ruling itself.** Silencing `record-immutability` for this path, or exempting it
by a `Kind:` read, would clear the finding by making the checker look away —
which the ruling explicitly forbade ("NOT because the family was silenced").
Leaving it and dispositioning it annually is what three prior packets already
did, and is why the critical is still standing. **Alternative not taken:**
keeping the taxonomy at eight and accepting the standing critical forever.

**OD-3 — THE TAXONOMY IS "CLOSED", AND THIS EXTENDS IT. THE TWO ARE NOT IN
TENSION, AND THE SIBLING PACKET PROVES IT.** Brett ruled the same day, on
`clean-doc-health-floor` W1, that `docs/notebooklm-sync-open-item.md`'s
free-form `open (operational)` maps INTO the vocabulary with the taxonomy
staying closed. Read together: **closed means no ad-hoc value may appear in a
document without a governed change admitting it** — not that the vocabulary can
never grow. This packet IS that governed change, and it admits exactly one value
with a stated test for membership, while the sibling refuses one that has no
such change behind it. Recorded as a decision because the two rulings could be
read as conflicting, and a later reader should find the reconciliation written
down rather than have to infer it.

**OD-4 — THE MODIFIED BLOCK RESTATES THE WHOLE REQUIREMENT, INCLUDING SEVEN
SCENARIOS IT DOES NOT TOUCH.** `Controlled document status taxonomy` is the
longest requirement in the capability — the full ratification-citation
apparatus lives inside it — and only the vocabulary line and one scenario
change. The MODIFIED-block currency rule requires the block to restate the
requirement as canon currently states it, so all of it is carried, the
`A generated artifact is stored` scenario is split into a captured-once case
and a re-derived case, and one scenario is added binding the GENERATOR to emit
the value. **Alternative not taken:** an ADDED requirement declaring the
`projection` standing beside the taxonomy. Declined because the taxonomy
requirement ENUMERATES the vocabulary in its first sentence; leaving that
sentence at eight values while a second requirement described a ninth would put
canon in exactly the contradiction this packet exists to end.

## Open Questions

**Q1 — Should a `projection` document be REQUIRED to declare its generator and
source in machine-readable form?** Canon now says a projection "SHALL name its
generator and its source", and `ideation/cross-reference.md` does — in prose, in
its banner paragraph. Nothing checks it, so a future projection could carry the
status while naming nothing. **RECOMMENDATION: leave it prose-only for now, and
say so.** A `Generated-by:` header would be a second new vocabulary item and a
new check, for a class that currently has one member; the rule-of-three has not
fired. Worth revisiting the day a second projection appears — which is also when
the check would have something to compare.

**Q2 — Should `record-immutability` gain a positive guard so a projection cannot
be quietly re-classed back to `record` to silence a real edit?** The status is
now the whole of what the family reads, so anyone editing a projection by hand
and flipping it to `record` would get a fresh capture and no finding — the
mirror image of the defect being fixed. **RECOMMENDATION: not in this packet,
and named as the sharper follow-up.** The honest check is not on the status but
on whether the committed bytes match what the declared generator produces —
`--check`-mode regeneration in CI — which is a real capability, is testable, and
would subsume the question. It deserves its own change rather than a guard
bolted to a family whose scope this packet deliberately did not touch.

## Impact

- **Affected specs:** `document-lifecycle` (one MODIFIED requirement; no ADDED,
  no REMOVED, no family enumeration change).
- **Affected code:** `scripts/doc_health/__init__.py`,
  `scripts/doc_health/promotion_fidelity.py`,
  `scripts/sync-notebooklm-books.py`,
  `scripts/render-ideation-cross-reference.py`,
  `contracts/schemas/ideation-dashboard-snapshot.schema.yaml`,
  `tests/doc-health/test_families.py`.
- **Affected documents:** `docs/document-lifecycle.md`,
  `ideation/cross-reference.md` (regenerated, one line), one README entry.
- **Contract bundle:** none owed, measured against all 48 inventories.
- **Owed elsewhere:** ONE disposition entry at the aggregation root
  (§ The disposition this owes elsewhere). This packet does not archive until
  it lands.
- **Sibling:** `clean-doc-health-floor` carries the other two ruled
  workstreams. The two packets share no file but `README.md`.
