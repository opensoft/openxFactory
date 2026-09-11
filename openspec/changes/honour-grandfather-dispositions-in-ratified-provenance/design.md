# Design: honour-grandfather-dispositions-in-ratified-provenance

Status: draft
Kind: design

**EVERY DECISION THIS AUTHORING SESSION TOOK IS HERE, WITH ITS ALTERNATIVE AND
THE ALTERNATIVE'S COST.** Brett Heap's word of 2026-09-11 — verbatim
**"Commission the packet"** — commissioned the authoring and took none of them.
**D1 and D2 are the declared veto points.**

## 0. The brief

openxFactory [#939](https://github.com/opensoft/openxFactory/issues/939):
`fam_ratified_provenance` does not read `health/dispositions.yaml`, so the
fifteen archived openxFactory ratification records grandfathered on
[#877](https://github.com/opensoft/openxFactory/issues/877) and codexFactory's
three stay `critical` in the report-only nightly. The remedy is one `##
MODIFIED` block and one last pass in one family, realized in the same pull
request.

## D0 — the measurement, taken before the design

**Nothing below rests on a number anybody typed.** An aggregation checkout was
assembled from `opensoft/xFactory` @ `bc84d325` with `openxFactory` @
`96b4835b` and `codexFactory` @ `a67fb0ae` materialized under it, and the
family was run against the REAL `health/dispositions.yaml` that checkout
carries.

**THE FILE, AS IT STANDS:** 40 entries across 8 families —
`ratified-provenance` **18**, `location-conformance` 10, `record-immutability`
4, `modified-block-currency` 4, and one each of `semantic-contradiction`,
`semantic-normative-prose`, `uncited-resolution`, `document-catalog`. All
eighteen of this family's entries carry a `date` (2026-09-10) and a non-empty
`cite`; **fifteen name `openxFactory` and three name `codexFactory`**; and
**all eighteen name a path under `openspec/changes/archive/`**.

**THE FAMILY, BEFORE AND AFTER** (`--family ratified-provenance`):

| | rows | critical | info |
| --- | ---: | ---: | ---: |
| before | 41 | 41 | 0 |
| after | 41 | 23 | 18 |

- The **key sets are equal** — same 41 `(repo, path)` pairs on both sides. No
  row is added and none is withheld.
- The set that moves is **exactly** the eighteen disposition keys. Asserted as a
  SET EQUALITY (`moved == disposition key set → True`), not as a count that
  happens to agree.
- The remaining **twenty-three rows are byte-identical** in severity, rule,
  action and resolution class.
- **THE WHOLE DIFF BETWEEN THE TWO REPORTS IS 74 LINES AND THEY ARE ALL THE
  SAME EIGHTEEN FINDINGS PLUS ONE HEADLINE**, counted rather than characterised:
  the report renders every finding TWICE — once under `## Findings By Family`
  and once under `## Ranked Plan` — so the eighteen account for 36 lines on
  each side, and the seventy-fourth is the headline that sums the bands,
  `41 critical, 0 error, 0 warning, 0 info` → `23 critical, 0 error, 0 warning,
  18 info`. No other line of either rendering differs, and the Ranked Plan
  keeps all 41 rows: an `info` row is re-banded there, not dropped.
- **TWO of the family's five arms are covered by the eighteen**, which is why
  the downgrade is a LAST PASS and not a branch inside one arm: **fifteen** of
  the moved rows carry the SUBJECT-arm rule (`Status: record` on a ratification
  record — the #878 shape, and all fifteen are the openxFactory #877 records)
  and **three** carry
  *"ratified header carries no citation in either sanctioned spelling"* (all
  three of codexFactory's, which are `Status: ratified` records predating the
  two-spelling convention). A branch per arm would have had to be written twice
  and would have missed the other three arms entirely.
- The downgraded row **still parses**: `report.plan_line(f, strict=True)` →
  `report.PLAN_RE` matches, `report.unparsed_plan_rows` returns `[]`.

**THE SINGLE-REPO SCOPE IS UNAFFECTED AND THAT IS MEASURED TOO.**
`health/dispositions.yaml` lives at the AGGREGATION root and a `--single-repo`
run has `Context.agg_root is None`, so `python3 scripts/doc-health.py
--single-repo .` — this repository's own gate — reports every finding of this
family at `critical` exactly as it does today.

## D1 — VETO POINT: an `info` ROW carrying the citation, NOT silence

**RECOMMENDED: report the grandfathered finding at `info`, with the recorded
citation quoted, keeping its family, repo and path.**

**THE ALTERNATIVE IS THE PRECEDENT, WHICH IS WHY THIS IS A VETO POINT.** All
four sibling requirements that carry a *A finding is dispositioned* scenario
SUPPRESS: *"findings on that path MUST be suppressed"* (promotion fidelity,
duplicate packet, modified-block currency, and the sibling-addition pairing
class). Choosing `info` is a DIVERGENCE from four promoted requirements and
must be argued, not assumed.

**THE ARGUMENT IS THE SUBJECT, NOT THE MECHANISM.** Those four dispose a
finding whose subject **can still be repaired** — an archived DELTA that could
be promoted, an active block that could be rewritten. A suppressed row there is
a closed question: somebody decided not to act, and if the decision is revisited
the finding comes back because the defect is still reachable. Here the subject
is an **IMMUTABLE archived record** and the defect is **permanent**: the header
will carry the wrong status for as long as the archive exists, and no future act
short of a governed archived-record edit can change it. Suppressing it would
delete a standing population of eighteen from the artifact a reader reads and
leave the reason for the silence legible only in a YAML file in a different
repository.

**AND THE ROW IS THE ONLY PLACE THE TWO FACTS MEET.** The report is where a
reader learns what the corpus carries; the dispositions file is where the owner
records a ruling. An `info` row is the one artifact that says BOTH — *this
record is out of contract* and *the owner ruled that nothing is owed, here is
the word* — in the place a reader is already looking.

**COST OF THE VETO, WRITTEN OUT.** Suppressing instead of downgrading is a
smaller diff (drop the finding rather than rebuild it) and makes this family
read exactly like its four neighbours. It costs: the eighteen records vanish
from the report with no trace; the count of grandfathered records becomes
uncountable from the artifact; a disposition entry that goes stale — a record
repaired, an entry left behind — becomes invisible instead of showing as an
`info` row nobody can explain; and a reader who wonders why a known-bad record
draws nothing has no thread to pull. **A veto of D1 is a veto of the BAND
alone.** Everything else in this packet — the archived-only boundary, the
delegated admission rule, the scenario's other three arms — stands unchanged
under either answer, and the delta edit is one THEN bullet.

**WHY NOT `warning`, THE THIRD OPTION.** `warning` is the band for something a
reader should act on. Nobody may act on these. `info` is the band this corpus
already spends on *"true, recorded, and not yours to fix"* —
`release_inventory`'s editorial members, `modified_block_currency`'s carriage
ledger and its marker-defect class, `ideation_routing`'s unavailable external
path. It is the existing vocabulary rather than a new one.

## D2 — VETO POINT: the boundary is `openspec/changes/archive/`, and nothing else

**RECOMMENDED: a disposition downgrades a finding ONLY where the path is under
`openspec/changes/archive/`. A finding against an ACTIVE packet's record stands
at `critical` however the file names it.**

**THE GROUND OF THE GRANDFATHER IS IMMUTABILITY, NOT INCONVENIENCE.** An
archived record is beyond a plain fix by ruling — `record-immutability`,
`govern-archived-record-edits` — so the owner rules because the owner cannot
edit. An ACTIVE packet's record is one commit away from correct. Honouring an
entry there would convert the mechanism from *"the owner ruled on something
nobody can repair"* into *"the owner ruled on something nobody got round to
repairing"*, which is a deferral with a governance record stapled to it.

**THE PREFIX IS THE WHOLE TEST, AND DELIBERATELY WIDER THAN `review/`.** The
ground covers every file in an archived packet, not only its ratification
record: an archived `proposal.md` with a defective citation is as unrepairable
as an archived `review/` record, and three of the forty-one rows measured in D0
are exactly that. Narrowing the test to `review/ratification-*.md` would encode
the POPULATION rather than the RULE.

**COST OF THE VETO.** Admitting active paths costs one `and` in the predicate
and one bullet in the scenario. It costs the distinction between a ruling and a
deferral, and it makes an entry a way to stop a `critical` on a file somebody
could fix this afternoon — the exact failure mode `uncited-resolution` exists
to prevent elsewhere. **A veto of D2 is a veto of the BOUNDARY alone** and
leaves D1 standing.

## D3 — `health/dispositions.yaml`, NOT a new file and NOT a new key

**RECOMMENDED: the EXISTING file, the EXISTING `(family, repo, path)` key, and
the EXISTING reader.**

**THE FILE IS ALREADY THE ESTATE'S ANSWER TO THIS QUESTION, FOUR TIMES OVER.**
`runner.main` loads it for the uncited-resolution rule.
`promotion_fidelity.load_dispositions` reads it for promotion fidelity,
duplicate packet and modified-block currency under each family's own name. The
`neutrality-drift` lane reads it directly, extended with a `content_sha256`
(`docs/doc-health.md`, *Dispositions keying*). **And it is already where these
eighteen rulings live**: the openxFactory fifteen were written there by
`opensoft/xFactory` PR #420 → `5bfa1fe4` on #877, and codexFactory's three by
PR #412 on codexFactory issue #341 / PR #342. A new file would be a second home
for decisions that are already recorded, and the migration would be a governance
act nobody asked for.

**THE ADMISSION RULE IS DELEGATED RATHER THAN COPIED.** `_grandfather_cites`
calls `promotion_fidelity.load_dispositions(ctx, "ratified-provenance")` for the
key set and re-reads the file for one thing that reader does not return — the
citation TEXT. `families.py` already imports `promotion_fidelity`, and
`promotion_fidelity` imports nothing from `families`, so there is no new
dependency and no cycle. **The alternative considered and rejected** was a
self-contained loader in `families.py` with a test pinning agreement against the
shared reader: cheaper to read, and it makes a SECOND rule about which entries
are live, held together by a fixture. Two readers of one file that can disagree
is the drift this estate has written about twice (`report.unparsed_plan_rows`,
`doc_health.lines`); it is not worth twenty lines.

**ONE EXTENSION IS DECLINED.** A `requirement:` narrowing means nothing for a
ratification record, which has no requirement grain. Rather than reject such an
entry (silently disposing nothing) the arm IGNORES the key and admits the entry
on `(repo, path)`, and the scenario and a test say so.

**THE CITATION IS QUOTED AS A BOUNDED SINGLE LINE.** A ranked-plan row is one
line that `report.PLAN_RE` reads back anchored; the eighteen cites run 700–1,100
characters. The excerpt collapses whitespace (a literal-block `|-` entry would
otherwise split the row into two lines that match no parser — issue #474's shape
at a different field), cuts at a word boundary at 240 characters, and appends an
ellipsis. The entry's own key is the lookup into the file, so the excerpt
identifies the ruling rather than reproducing it — which the scenario says with
a **MAY**, so a later act may widen or narrow it without amending canon.

## D4 — `doc-health` is amended; `document-lifecycle` is NOT

**RECOMMENDED: leave `document-lifecycle` exactly as it stands.**

The obligation — *A review record records a ratification*: a `review/` record
whose subject is the ratification MUST carry `Status: ratified` and one citation
— is **unchanged and unweakened by this packet**. The eighteen records are still
out of contract, and this packet says so on every one of them, in the report, at
`info`. What changes is only how **doc-health REPORTS** a violation nobody may
repair.

**THE ALTERNATIVE WOULD HAVE BEEN A GRANDFATHER CLAUSE IN THE LIFECYCLE RULE** —
"a record written before <date> is exempt". It is rejected on three grounds.
It puts a DATE in a rule, which every record written after it then has to be
checked against, and dates in rules rot. It makes the eighteen records
CONFORMANT, which is false — they are non-conformant records nobody may repair,
and the distinction is the whole content of the ruling. And it moves the remedy
into a capability whose contract is about what a DOCUMENT must carry, when the
question is what a CHECKER should report, which is this capability's own
subject. The `Removed from canon` / marker machinery is likewise untouched: no
promoted unit is removed, so there is nothing to declare.

## D5 — the sibling search, pasted

Performed 2026-09-11 before authoring, on the lane-collision protocol's
claim-before-author rule. Recorded on #939 at filing and re-run at the start of
this packet:

```text
$ gh api /repos/opensoft/openxFactory/pulls --jq '.[] | "#\(.number) \(.head.ref)"'
#942 fix/openxdox-verifier-index-read          #941 register/grc-0002-reissue
#940 change/split-opendox-section-5-shed       #937 change/amend-repo-boundary-governance-scope-first-line
#934 change/retire-corpus-adapter-replica      #921 change/state-header-window-budget
#888 doc-health/derive-possibles               #594 rescue/worker-fleet-health-monitoring
#518 docs/add-usage-controlled-evidence-chain

$ for n in 921 934 937 940 942; do gh api .../pulls/$n/files --jq '.[].filename' \
      | grep -E 'doc_health|doc-health'; done
(no output — NO open pull request touches scripts/doc_health/ or openspec/specs/doc-health/)

$ grep -rn "Governed corpus membership and the lifecycle scan set" openspec/changes/ | grep -v archive/
openspec/changes/honour-grandfather-dispositions-in-ratified-provenance/specs/doc-health/spec.md:5
(this packet alone — NO two-writers collision on the requirement)

$ ls -d openspec/changes/*/specs/doc-health
add-nightly-dashboard-refresh   (7 ADDED requirements, none this one)
settle-aging-staging-topics     (1 MODIFIED: "Aging threshold defaults")
honour-grandfather-dispositions-in-ratified-provenance
```

Open issues matching `grandfather`, `dispositions` and `ratified-provenance`
were listed: **#939 is the only one naming a grandfather disposition for this
family**. `ideation/staging/` was enumerated (30 topic folders) and `INDEX.md`
read: no topic names doc-health severity policy, the disposition mechanism or
ratification-record rules — the one `grandfather` hit is the credential-escrow
registry's ruling C, a different mechanism in a different capability. Hence
`kind: ad_hoc` (`.openspec.yaml`).

## D6 — what is NOT taken here, measured and deliberately left

- **The other seven families' dispositions are untouched.** The file carries 22
  entries for `location-conformance`, `record-immutability`,
  `modified-block-currency`, `document-catalog` and the three semantic/uncited
  families. Whether any of THOSE should be downgraded rather than suppressed (or
  read at all, in the case of the families that read nothing) is a separate
  question about a different subject, and answering it here would widen a
  ruled remedy into an unruled sweep.
- **The eighteen cites are not re-verified.** This packet reads them as records
  of a ruling. Whether each ground is sound was the lifecycle owner's act at
  `opensoft/xFactory` PR #420 and PR #412, and re-litigating it in a checker is
  not this family's authority (`doc-health`, *Semantic finding disposition
  authority*).
- **No stale-entry check is added.** An entry naming a path that no longer
  exists, or a record since repaired, produces no `info` row and no complaint —
  the entry simply matches nothing. A family that reported stale dispositions
  would be a new finding class with its own severity and its own population, and
  it is named here as a successor rather than smuggled in. Measured today: all
  eighteen entries match a live finding, so the population of that successor is
  ZERO and there is nothing to lose by deferring it.
- **`docs/doc-health.md` is not edited.** Its *Dispositions keying* paragraph
  describes the neutrality lane's `content_sha256` extension and is accurate
  about it; this arm adds no key and no extension. The contract prose that would
  need to move — the family table's row 3 one-liner — is a documentation sweep
  rather than this packet's act, and is named as residue in `tasks.md` § 7.
- **The `--single-repo` scope is left without dispositions.** Giving a
  single-repo run a way to point at an aggregation dispositions file is a CLI
  surface, an argument, a contract line and a test matrix; the self-gate's job
  is to report this repository's own defects and it is CORRECT for it to report
  all eighteen.
