# Proposal Ratification: state-header-window-budget

Status: ratified
Kind: report
Decision date: 2026-09-11
Ratifier: Brett Heap (openxFactory operator authority)
Ratified: 2026-09-11T01:44Z by Brett Heap (openxFactory operator authority) —
first-hand, in session, to lane `codexfactory-1` (window `codeXfactory-1`),
verbatim: *"ratify 921"*, over verified head `29f22114`, recorded on
openxFactory PR
[#921](https://github.com/opensoft/openxFactory/pull/921#issuecomment-5628429288)
(comment 5628429288). This header block is per `document-lifecycle`'s
*A review record records a ratification*; the prose sections below keep the
fuller account.

## Decision

RATIFIED by Brett Heap. The word was bare, so the text stands exactly as the
bench reviewed it.

## Authority, and that it is first-hand

Brett Heap — openxFactory operator authority, and the estate's sole operator
— ruled **first-hand, in session**, to lane `codexfactory-1` (session window
`codeXfactory-1`), at **2026-09-11T01:44Z**. Verbatim:

> **"ratify 921"**

There is **no relay**. The word was heard in the session that acts on it, by
the lane that authored the packet, and recorded contemporaneously in that
lane's own handoff document,
`session-handoff-2026-09-05-lane-codeXfactory-1.md` (xFactory aggregation
repo), under its `WORD —` line. It was carried into this repository by the
lane's own writer FROM that brief and that contemporaneous record — not from
a second human's retelling and not from any agent's paraphrase. The verbatim
above is copied byte-for-byte from both.

The word is recorded on the pull request itself before this record was
written, at
[comment 5628429288](https://github.com/opensoft/openxFactory/pull/921#issuecomment-5628429288),
so the ruling is legible to a reader who never sees the handoff.

## The head the word was given over, and which sha is authoritative

The word was given over verified head
**`29f2211437b9f5e0fd9960f45e83f8ca8de91bb7`**. That is the value

```
git ls-remote origin refs/heads/change/state-header-window-budget
```

returns — what the branch actually points at, and what a merge would take.
**THE GIT REF IS AUTHORITATIVE.**

GitHub's PR object reported `headRefOid` **`5dfa1831`** for hours before the
ruling and still reported it when the ruling was recorded. That is a stale
projection of the same branch, not a second head, and it is written down here
rather than quietly reconciled because a reader comparing the two months from
now is owed the explanation. `29f22114` is a merge of `origin/main`
`72c0fa6c` over `5dfa1831`, and it moves **no byte of this packet**:

```
git diff --quiet 5dfa1831 29f22114 -- openspec/changes/state-header-window-budget/ ; echo $?
0
```

So the text ratified is identical at the two shas and nothing in the ruling
turns on which one a reader resolves.

**THE RATIFYING COMMIT IS LATER THAN BOTH, AND CARRIES THE SAME PACKET
BYTES.** `origin/main` moved to `96b4835b` while the packet awaited the word,
so the branch was merged up **before** the ratification was encoded — its own
commit, no conflict, and no file this packet writes was touched by the merge.
The same proof was re-run across it: `git diff --quiet 5dfa1831 <merged head>
-- openspec/changes/state-header-window-budget/` exits **0**. Every figure in
this record is therefore derived on a tree that already carries current main,
and no merge-and-re-measure is owed at landing.

## The text ratified

One `## MODIFIED Requirements` block on the promoted `release-realization`
requirement **"Equivalent declaration sites for the ordered-delta parent
declaration"**:

- **One paragraph added**, stating that the bounded lifecycle header window
  is counted from the document's own **line 1**, and that a leading `---`
  fence's lines **consume that budget** rather than being excluded from it —
  they are unavailable as declaration sites while still counting.
- **One scenario added**, *"Fence lines consume the header window budget"*.

Every existing sentence, bullet and scenario of the requirement is carried
**verbatim**. Nothing is reworded, reordered or removed, so no
`Removed from canon` marker is owed — machine-diffed against the promoted
spec with the two additions stripped out, clean (`tasks.md` § 2.1).

The rule is not new behaviour. `scripts/frontmatter_strict.py` already counts
the window this way (`read_header_line`, whose own docstring reads "FENCE
LINES ARE SKIPPED BUT STILL COUNT toward the window"), and the packet
re-verified it **empirically on the branch** rather than trusting the
docstring's word: real line 15 behind a four-line fence reads; real line 19
behind the same fence is refused. What is ratified here is the **prose
catching up with the running code**, which is what the Copilot finding on
PR #906 asked for.

## Origin of the amendment

Routed from a Copilot review comment on openxFactory PR #906 — the archive of
`accept-sequenced-after-header-line` — at
`openspec/specs/release-realization/spec.md:440`
([discussion_r3981305715](https://github.com/opensoft/openxFactory/pull/906#discussion_r3981305715)).
Lane `codexfactory-1` answered on that thread **as itself and not as a
ruling** ([discussion_r3981322763](https://github.com/opensoft/openxFactory/pull/906#discussion_r3981322763)),
agreed the reading was correct, and **declined to fix it there** because
editing an archive's promoted text with no ruling behind the edit would break
the sha256 byte-identity that archive's own evidence rests on. It named this
packet's shape instead — "a one-clause MODIFIED on this requirement making
the window-budget rule explicit". **This packet is that amendment**, and the
ruling above is the ratification that reply said was owed.

## The word was bare, and what that rules

**"ratify 921" names no wording to change, so none was changed.** The packet
declared four authoring decisions (`design.md` D1–D4) and carried them to the
bench with their alternatives written out; the word vetoed none of them, so
all four are ratified **as the packet states them**, not separately ruled.

This is applied by **leaving the text alone, and that is verified by diff
rather than asserted**:

```
git diff 5dfa1831 HEAD -- openspec/changes/state-header-window-budget/specs/
(empty)
```

## What ratification changes, and what it does not

**CHANGES** — all in the single ratifying commit:

- `proposal.md`: `Status: draft` → `Status: ratified`, plus **exactly one**
  citation line, spelled `Ratified:`.
- `.openspec.yaml`: the ratification **added** to `origin.approved_by`.
- `tasks.md`: Group 0 OPEN → CLOSED; **0.3 ticked**; 0.1 and 0.2 annotated
  and **left unticked**.
- `README.md`: the "OpenSpec Records" row moved **DRAFT → RATIFIED**.
- This record.

**DOES NOT CHANGE.** No promoted canon is touched by this commit — the
measurement is `git diff --quiet HEAD -- openspec/specs/` taken against the
pre-ratification head, which exits **0** — and no script, test, contract,
schema, workflow or Speckit build record moves. **The comparison is stated
against the pre-ratification head and not against `5dfa1831` on purpose,
because against `5dfa1831` it would be FALSE and the false version is the
tempting one to write:** `git diff 5dfa1831 HEAD -- openspec/specs/` exits
**1**, showing `doc-health/spec.md` and `neutral-product-pin/spec.md` moved.
Neither is this packet's doing — both arrived in the merge of `origin/main`
`96b4835b`, promotions belonging to other lanes' changes — and attributing
them here by quoting the wider diff would credit this ratification with
canon it never touched. No ledger row moves. No archived
change is touched. No other active change's files are touched.

**AND IT IS NEITHER A MERGE NOR AN ARCHIVE.** `code_surface: none`, so this
packet archives **on landing** — `tasks.md` § 3.1, a SEPARATE act on a
separate word, performed by whichever lane holds that word and **left
unticked here**. The merge word has **not** been given. This lane encodes and
freezes; the Rule 6 `LANDING`/`LANDED` post belongs to the landing lane on
that separate word, and openxFactory `main` additionally requires `--admin`
or Merge Master approval.

## The two written rules this ratification had to satisfy in its own commit

**1. THE CITATION SITS INSIDE THE WINDOW THIS PACKET IS ABOUT.** The
`Ratified:` line is `proposal.md` **line 10** — inside the fifteen-line
lifecycle header window **counted from line 1 with the front-matter fence's
five lines (1–5) included**. That is the packet's own rule applied to the
packet that states it, and it is not a coincidence worth leaving unremarked:
had the fence been treated as free, the same header would have read as line 5
of the window instead of line 10, and a longer citation would have slipped
out of a budget its author believed was intact. The whole lifecycle header —
fence, title, `Status:`, citation, `Authored:` — closes inside the budget.

The spelling is `Ratified:` and not `Ratified by:` because **no approving
OpenSpec change exists to name**; `document-lifecycle` § Status Claim Rules
makes the record-citing spelling the legal one in exactly that case, and
requires at least one of an approver, a date, or a resolvable record path.
This line carries all three, with the approver in the recognized `by <Name>`
form.

**2. THE APPROVAL PAIR IS AN ADDITION, IN THIS COMMIT, NEVER A REWRITE.**
`document-lifecycle` § *Proposal origin declaration* states both halves:
*"APPROVAL IS AN ADDITION, NEVER A REWRITE"* and *"APPROVAL SHALL APPEAR WHEN
A STATUS CLAIMS IT — a proposal whose own `Status:` declares `ratified` …
SHALL carry approval provenance in its origin."* The archive gate reads this
packet's `.openspec.yaml` blob **at the ratifying commit** as its permanent
baseline (`scripts/proposal-support.py`, `ratifying_commit` /
`origin_retention_errors`), so an approval added in any LATER commit is a
post-ratification mutation needing an explicit disposition. It is therefore
written here, in the flip itself.

**THE HONEST COMPLICATION, STATED RATHER THAN SMOOTHED.** This packet's
`origin` already carried an `approved_by`/`approved_on` pair when it was
authored — but that pair records the **authorization to author** (the resume
ruling *"fan out wide"*) and **explicitly disclaims being a ratification of
content**. So the slot the rule points at was occupied by a field that says,
in its own words, that it is not the thing the rule is asking for. Both
duties were kept:

- Every existing sentence is **byte-unmoved**, and so are `kind`, `id`,
  `reason` and `related`. The disclaimer stands as written; it is
  time-indexed (*"At the time this field is written…"*), which is precisely
  what makes a later clause beside it coherent rather than contradictory.
- The ratification is **appended** to the same field, dated and attributed,
  under its own heading sentence — an addition, in the ratifying commit.
- **`approved_on` is left at `2026-09-10` deliberately, not overlooked.** It
  dates the authorization recorded above it; rewriting it would destroy that
  record and would be exactly the mutation the rule forbids. It is not false
  of the ratification either: 2026-09-11T01:44Z is 2026-09-10 21:44 in the
  timezone this repository's own commits are stamped in (`-0400`), the same
  calendar date. The ratification's UTC instant is carried three times over —
  in the appended prose, in the `Ratified:` citation, and in this record.

Mechanically this changes nothing that was already passing: the pair was
complete before and is complete now, so `origin_errors` and the nightly
`proposal-origin` family's class-7 rule (a ratified status over a
drafting-only origin) were and are silent. The addition is for the **reader
of the record**, who would otherwise find a ratified packet whose only
approval provenance denies being one.

## Convention followed, and where it comes from

The encoding mirrors this repository's own recent ratifications rather than
inventing a shape: `208f88d4` (`accept-sequenced-after-header-line` — this
same lane, this same requirement family, and the packet this one is
`sequenced_after`), `93ba99f0`, `705cecef` and `d6877c00`. From them: the
status flip plus one citation line in `proposal.md`; a
`review/ratification-<date>.md` record carrying `Status: ratified`; the
ratify-encoding box ticked while the owner's own boxes are not; and the
README row moved DRAFT → RATIFIED. From `d6877c00` specifically: the approval
pair added to `.openspec.yaml` beside frozen drafting provenance, in the
ratifying commit, with the origin's drafting tense deliberately not retensed.

**THE DATE BOUNDARY, NAMED.** `d6877c00` could record that its word, its
record file name and its `approved_on` all fell on one date "with no boundary
to reconcile". Here there **is** one: the word fell at 2026-09-11T01:44Z,
which is 2026-09-10 locally. This record is named for the **UTC** date, which
is how every word in this lane's handoff is stamped and how the `Ratified:`
line reads; `approved_on` stays on the local-calendar date it was authored
with, for the reason given above. Both dates are correct for what they date,
and neither is guessed.

## Gates, re-run on the ratified tree

Every figure below was measured **after** the encode, on the merged tree, with
this record itself inside the lifecycle scan set — not carried forward from
the pre-ratification verification. Exit codes are quoted because an exit code
is the gate; a count that drifts as the corpus grows is labelled as such.

**1. The pinned CLI, this change.**
`OPENSPEC_TELEMETRY=0 python3 scripts/validate-openspec-cli-pin.py --change
state-header-window-budget --strict` → `@fission-ai/openspec@1.12.0` verified
against its content address, `Totals: 1 passed, 0 failed (1 items)`,
**exit 0**.

**2. The pinned CLI, the whole corpus, against a fresh control.**
`… --all --no-cache` on this branch → `99 passed, 2 failed (101 items)`,
**exit 0**. The same command in a **fresh `origin/main` worktree at
`96b4835b`** → `98 passed, 2 failed (100 items)`, **exit 0**. The pin
entrypoint exits 0 on BOTH sides because both failures are accepted,
dispositioned exceptions, and it says so in as many words rather than
reporting a clean tree.

**THE INVARIANT IS THE RELATIONSHIP, NOT THE TOTALS** — the totals drift as
other lanes land, exactly as `tasks.md` § 2.3 warned. Checked by diffing the
two failing-item sets **by item id out of `--json`, not by eyeballing
totals**:

- branch failures: `{add-chain-attestation, add-composed-view-authoring}`
- control failures: `{add-chain-attestation, add-composed-view-authoring}`
- **new failures introduced by this branch: NONE (the set difference is
  empty)**
- items present only on the branch: `{state-header-window-budget}` — exactly
  one, this packet, and it **passes**

So branch = main + 1 item, the same two pre-existing failures on both sides,
zero new. (Run directly, the pinned binary exits **1** on both sides, since
two items fail on both; the disposition posture that turns that into 0 is
identical on both sides too.)

**3. Doc-health, the four families that could reach this act.**
`python3 scripts/doc-health.py --single-repo . --family <F>`, run once per
family because `--family` takes one choice:

| family | exit | findings naming this packet |
| --- | --- | --- |
| `status-validity` | **0** | 0 |
| `ratified-provenance` | **0** | 0 |
| `proposal-origin` | **0** | 0 |
| `modified-block-currency` | **0** | 0 |

And the full sweep with **no** `--family` filter — every family in one run —
**exit 0**, zero findings naming this packet, `Findings: 32 critical, 5
error, 47 warning, 16 info. New regressions vs previous report: 0.` Those
four severity counts are the corpus's standing state, not this packet's
doing; the figures that belong to this act are the **zero** findings naming
it and the **zero** new regressions.

`ratified-provenance` is the family with teeth here, and its silence is the
point: it reads the header window with the shared real-line rule, counts
citation lines across BOTH sanctioned spellings, and holds a `Ratified:`
line to the approver/date/record floor. One citation, in window, clearing the
floor on all three axes — so the family that would report a bare or duplicated
or out-of-window claim reports nothing.

**4. The archive gate's origin arms, run ahead of the archive that will run
them for real.** `scripts/proposal-support.py`:

- `origin_errors(root, packet, strict=True)` → `[]`, no errors. The ad-hoc
  origin declares a complete approval pair, its `reason` is present, and its
  durable id still matches the grammar it was minted under.
- `origin_retention_errors(root, packet)` → `[]`, no errors, printing
  **`ORIGIN RETAINED state-header-window-budget (declaration unchanged since
  the ratifying commit …)`**. The arm was run **twice, deliberately**. Before
  the flip was committed it refused, correctly: *"not ratified — no commit in
  history carries `Status: ratified` … Commit the ratification before
  archiving."* That refusal is the arm working — its baseline is the packet's
  `.openspec.yaml` blob at the ratifying commit, read from HISTORY, which is
  the one copy an edit at archive time cannot reach, and before the commit
  there was no such blob. Re-run after the commit, `ratifying_commit`
  resolves to **this commit** (a genuine FLIP, whose parent does not already
  declare `ratified`, which is the assertion that arm makes before trusting a
  candidate) and the tree equals its baseline exactly. **No sha is quoted
  here, because a commit cannot contain its own; the PR comment recording
  this run names it.**

  The addition-not-a-rewrite shape is also true **numerically**, not only in
  prose: `git show --numstat` for `.openspec.yaml` in the ratifying commit
  reads **`33  0`** — thirty-three lines added, **zero deleted**.

**5. The test slice.**
`python3 -m pytest tests -q -k "sequenced or frontmatter or
release_realization"` → **278 passed**, 11174 deselected, **exit 0** — the
same 278 the pre-ratification verification measured, so the encode moved no
test outcome.

## Limits

This record performs **no merge**, ticks **no owner's box**, and closes **no
issue**. It records one word and what that word reached. Its own claims about
gate results are the measurements in the section below, taken on the ratified
tree; where a figure is a count that drifts as the corpus grows, the record
says so rather than pinning a number the next lane will find stale.
