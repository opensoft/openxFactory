# Design: bump-openspec-cli-pin-to-1.12

Status: draft
Date: 2026-09-05

The bump itself is four scalars. Everything worth designing is the DISPOSITION
GRAMMAR that the ratified pin requirement forces this packet to invent, because
that requirement demands "`validate --all --strict` reporting zero failures for
every repository the bump reaches" and this corpus cannot report zero without
either reverting canon or writing down an exception.

## 1. The disposition grammar

```yaml
dispositions:
  - repo: openxFactory                       # scope
    item: add-composed-view-authoring        # the report's `id`
    path: ideation-dashboard/spec.md         # the report's issue `path`
    level: ERROR                             # human-facing; the tool reconciles ERROR
    finding: '…the report message, verbatim…' # the report's issue `message`
    why: >-                                  # one line, mandatory
      …
    cited_to:                                # non-empty list, mandatory
      - openspec/specs/doc-health/spec.md:1770 — …
      - PR #444 — …
    ratified_by: 'Brett Heap, 2026-09-05, "take exit 2"'   # or recorded_by:
    retires_when: >-                         # the condition that makes it stale
      …
```

### Why it lives in the pin and not in a second file

`health/dispositions.yaml` — the aggregation's doc-health disposition register —
is the obvious model, and its SHAPE is mirrored here deliberately: a per-entry
`repo`, a per-entry path, a MANDATORY citation, and audit fields the matcher
ignores. What is NOT mirrored is its LOCATION. A doc-health disposition is about
a document in some repository and belongs beside the other cross-repository
health state. A CLI disposition is about a specific version of a specific tool:
it is only meaningful while that version is pinned, it must be re-derived when
the version moves, and it must be deleted when the version rolls back. Anything
with that lifetime belongs in the file whose lifetime it shares. Put it in a
second file and the first bump that forgets to update it grants exceptions in
the name of a version nobody is running.

### Why matching is on (repo, item, path, finding) and on nothing looser

The pinned CLI's `--json` verdict — the same shape in `1.2.0` and `1.12.0`,
verified by running both — gives per item `id`, `type`, `valid` and
`issues[{level, path, message}]`. Three of those are stable identity and one is
the finding itself:

- **`id`** names the change or spec. Not unique on its own: one change routinely
  carries several findings.
- **`path`** names the delta file inside it. Also not unique: several
  requirements live in one spec file.
- **`message`** is the verdict. It is matched WHOLE, remedy sentence included,
  after collapsing whitespace and nothing else.

Whitespace is normalized because folding a 290-character `finding:` across lines
in this YAML file is a FORMATTING act, and a formatting act must not change what
a disposition covers. Everything else in the message is substantive: the
requirement title it quotes and the scenario titles it names are exactly what is
being accepted. **A prefix match, or a match on the requirement title alone,
would let one written exception silently absorb a second, different finding that
no human ever read** — which is the failure mode of every suppression list that
ever rotted.

Matching the whole message also makes UPGRADE-COUPLING a mechanism rather than a
promise. A later CLI that rewords this message matches nothing, so the finding
becomes undispositioned (exit 1, named) AND the disposition becomes stale
(exit 2). Both fire on the first run at the new version, which is the run at
which somebody is already deciding whether the exception still holds.

### Why a citation is mandatory, and refused rather than ignored

An exception with no citation is an uncited exception. This estate refuses those
everywhere else they appear — `doc-health`'s uncited-resolution rule turns a
contested finding that resolves without a citation into an ERROR, and
`health/dispositions.yaml`'s runner requires a non-empty `cite`. The only new
decision here is what to do with a malformed entry, and the answer is REFUSE the
whole run rather than skip the entry: skipping would re-fail a finding somebody
believed was settled, at some later moment, with no explanation of why the
exception stopped working.

## 2. Why an unmatched DISPOSITION refuses while an unmatched FINDING fails

This asymmetry is the design's load-bearing decision, so it is argued rather
than asserted.

| | it means | whose remedy | verdict |
| --- | --- | --- | --- |
| finding with no disposition | somebody wrote something the pinned tool rejects | the author's — fix it, or disposition it with a citation | **exit 1** (deltas invalid) |
| disposition with no finding | an exception outlived the condition it was granted for | this repository's — delete the entry | **exit 2** (the pin cannot be trusted) |

The exit codes already carry that distinction. `1` has always meant "the pin
held and your deltas are invalid"; `2` has always meant "the pin could not be
trusted". A stale disposition IS the pin asserting something about the corpus
that is no longer true, and its remedy — edit `contracts/openspec-cli-pin.yaml` —
is the remedy every other exit 2 already names. **A third exit code was
considered and rejected**: it would silently reclassify the run for every caller
that branches on 0/1/2, `.github/workflows/openspec-cli-pin-gate.yml` included,
which is a compatibility break bought for a distinction the refusal CODE
(`pin-disposition-stale`) already draws inside exit 2.

**What stale-refusal actually buys, concretely.**
`add-composed-view-authoring` has ONE open task box left — 3.2, a Brett act. On
the day he takes it and the change archives, that change leaves the `--all`
corpus, its finding stops occurring, and its disposition would otherwise sit in
this pin forever, granting a standing exemption for a class of finding nobody
re-examines. Refusing makes THE ARCHIVE ITSELF the event that forces the
re-reading. The cost is one red run and a two-line deletion; the alternative is
a suppression nobody can see.

## 3. Why a disposition is scoped by repository

One pin file governs the whole estate, and this entrypoint is invoked with
`--repo` against consuming trees. `add-chain-attestation` is absent from
OpsxFactory's corpus because it was never there. `add-composed-view-authoring`
will be absent from openxFactory's corpus because it archived. **Only the second
may refuse**, and no property of the report can tell them apart — so the
disposition declares `repo:` and the run resolves the validated tree's identity.

That identity is read from `git config --get remote.origin.url`, **not** from
the directory name, because every change in this estate is authored in a
`git worktree` whose directory is named for its branch. A basename rule would
read openxFactory's own corpus as a repository called `oxf-bump` and place every
disposition silently out of scope — a suppression failure that produces a GREEN
run, which is the worst kind. Where dispositions are declared and no origin can
be read, the run refuses `pin-repo-unidentified` rather than guessing which half
of the file applies. A pin declaring NO disposition never asks the question, so a
checkout with no remote keeps working exactly as it did.

## 4. Why `--json` replaces the stream, and what is done to keep the log honest

Reconciliation needs the findings as data, and the CLI offers `--json`. Two
alternatives were weighed:

- **Run the CLI twice**, once streamed and once as JSON. Faithful, and it
  doubles a minute-long corpus validation to preserve bytes that can be
  reproduced.
- **Parse the human output.** Rejected outright: a gate that depends on the
  wording of a foreign tool's console rendering is a gate that breaks on a
  cosmetic release.

So the run is `--json` and `render_findings` re-prints every finding — ERROR,
WARNING and INFO alike — in the CLI's own `LEVEL path: message` shape, followed
by the `Totals:` line derived from `summary.totals`. **A pin that declares no
disposition does not take this path at all**: no `--json`, no parsing, no
identity call, the CLI's own exit code as the verdict. The 1.2.0-era behaviour
is not "preserved by care"; it is the branch that runs.

`parse_report` accepts both array keys the pinned tool emits — `items` (a single
target, or a bulk run without `--report`) and `itemFindings` (`--report
findings`) — and a leading banner line, and NOTHING else. Both keys are covered
by CAPTURED REAL BYTES in `tests/openspec_cli_pin/fixtures/`, so the parser is
tested against what the tool actually printed rather than against a shape
invented to match the parser.

**One shape guard is not obvious and is worth naming.** If the CLI exits
non-zero and its report names no ERROR-level finding, the run refuses
`pin-report-unreadable`. Reconciliation reads the REPORT; a failure the report
does not carry would otherwise be silently dispositioned away by an empty match
set.

## 5. Why the pin's narrow reader was widened, and by exactly how much

`read_pin` parses the pin's own language and refuses everything else, on the
argument that a line a narrow reader does not understand must stop the run. Two
forms were admitted:

- **a one-level nested list** (`cited_to:` with `      - ` items), because an
  exception rests on more than one act and flattening citations into one
  delimited string would make the reader guess a delimiter a citation could
  itself contain;
- **the folded scalar `>-`**, because a `why:` forced onto one physical line is
  a sentence nobody reviews in a diff, and `>-` is the form the rest of this
  estate's YAML already writes prose in (`.openspec.yaml`'s `reason:`).

`|`, `|-` and `>+` are **not** admitted. Their whitespace semantics differ, and
a reader that guessed between them would be guessing at the content of a
citation; a pin using one is `pin-unreadable`, which is the correct answer to a
form this reader does not implement. Both widenings are pinned by tests,
including a negative one.

## 6. What this packet deliberately does not do

- **It does not modify the ratified requirement** *"A pinned CLI version bump is
  one human-only act that lands its target-version evidence in the same change"*.
  That requirement is carried by the still-ACTIVE `add-openspec-cli-pin` delta
  and is not yet in promoted canon, so a `## MODIFIED` block here would target a
  header no promoted spec carries and would collide with a sibling packet's own
  block. It also does not need modifying: its third paragraph already says
  "Where the target version's failures are pre-existing conditions, the change
  SHALL either remedy them or DECLARE each one with its owner; silence about a
  known failure is not evidence of its absence." **The dispositions ARE that
  declaration**, made machine-checkable. The ADDED requirement in this packet
  states what such a declaration must carry, and adds nothing that contradicts
  the sentence it serves.
- **It does not repair the pin's declared dependency-closure shortfall.** That
  remains stated in the pin's header and named as successor work, unchanged by
  the version move.
- **It does not touch `.github/workflows/pytest-suite.yml`'s literal
  `@fission-ai/openspec@1.2.0`.** That line is #667's open task 5.1; it now
  disagrees with the pin, which is exactly the defect #667 named and exactly why
  it is a separate diff over the repository's most load-bearing required check.
  Recorded here so it is not discovered later.
- **It does not file the upstream issue.** Drafted, not posted. Brett decides.
