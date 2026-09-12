# Tasks: gate-code-surface-declarations

Status: draft
Kind: tasks

`code_surface: openxFactory`, `target_release: implemented`. The realization
group is § 3 and it is **NOT IN THIS PULL REQUEST**: this filing carries the
PACKET ONLY. The tasks are individually executable, so under
`release-realization`'s decomposition rule this packet realizes through its own
task list rather than through a feature DAG — in a LATER pull request, on a
LATER word.

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a measurement recorded verbatim in this packet and
reproducible from the commands named beside it.

**§ 1 (RATIFICATION) IS ENTIRELY OPEN AND IS THE ASK.** Taking openxFactory
issue #1013 — an unclaimed residue another lane filed — commissioned the
AUTHORING and decided no wording. Four decisions are put for veto: `design.md`
D1, D2, D3 and D4.

**§ 5 (ARCHIVE) IS ENTIRELY OPEN.** `code_surface` is non-empty, so under
`release-realization` this packet SHALL NOT archive on landing. **THIS PACKET'S
OWN WORD ON ITS OWN ARCHIVE, WRITTEN HERE SO NO LATER READER HAS TO INFER IT:
this change archives only when § 3's realization pull request has MERGED into
`main` AND a `pytest-suite` run at the tree that merge carries is GREEN, and not
before — merged-plus-green at canon's grain, never archive-on-landing.**
openxFactory #1013 closes THERE and at no earlier pull request.

**§ 6 IS UNTICKED ON PURPOSE**: residue, measured and deliberately not taken.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RULE `design.md` D1 — what "off-vocabulary" means when the value is
      prose.** Option 1 (RECOMMENDED): GATE THE GRAMMAR — a declared head
      (`none`, or repository identifiers separated by `,` / ` and ` / ` + `)
      followed by a REQUIRED gloss opener, with the head judged and the gloss
      never, and NO membership check. Option 2: judge only the FIRST TOKEN, as
      the sibling does — measured cost: it refuses 2 of the 7 and passes the
      other 5, including a head whose second and third "repositories" are the
      words `the` and `PROJECT`, and it cannot read a multi-repository
      declaration at all. Option 3: resolve each identifier against a repository
      inventory — measured cost: this repository defines none, so the gate would
      refuse all 41 non-`none` declarations on the day it landed.
- [ ] 1.2 **RULE `design.md` D2 — the shape of the remedy.** Option 1
      (RECOMMENDED): an ADDED requirement, a house validator and a CLOSED
      register, following `gate-realization-axis-vocabulary`. Option 2: the
      requirement alone, with a bare refusal and no register — cost: it cannot
      land unless D3 option 3 lands with it, coupling two independent decisions
      into one word. Option 3: an ADVISORY gate — cost: an advisory gate refuses
      nothing, which is the state #1013 filed about.
- [ ] 1.3 **RULE `design.md` D3 — the disposition of the SEVEN pre-existing
      non-conformers.** Option 1 (RECOMMENDED): REGISTER ALL SEVEN, sweep none.
      Option 2: sweep the six whose correction carries no judgment and register
      the one that does. Option 3: sweep all seven. The reason this departs from
      the sibling's ruled sweep is written out in D3 and is two things: a head
      correction RE-PUNCTUATES another lane's ratified prose rather than
      replacing one token whose meaning the author's own gloss supplied, and for
      `split-opendox-two-layer-product` it is a judgment about what counts as a
      repository. **Note the structural difference too:** the sibling swept "in
      this PR" because its realization was in that same pull request; here any
      sweep lands in § 3's LATER pull request, so the population must be
      re-measured there in any case.
- [ ] 1.4 **RULE `design.md` D4 — whether `scope_globs:`'s machinery is
      reusable.** Option 1 (RECOMMENDED): reuse it as the CONSUMER and NARROW
      `scripts/scope_globs.py`'s `code_surface_repositories` to the declared
      head, with the rule SHALLed in the delta. Option 2: leave the extractor and
      name a successor — cost: the field is then read two ways, strictly by the
      new gate and permissively by the authorization check. Option 3: leave the
      extractor and register the 27 — cost: it registers 27 packets for a defect
      that is in the reader, not in any of their declarations.
- [ ] 1.5 **D0 AND D5 THROUGH D8 ARE CARRIED BESIDE THEM** and are equally open
      to veto: D0 (the measurement and its method), D5 (the code surface, the
      three exit codes, the register's home outside `contracts/`), D6 (why an
      OpenSpec change and not a patch), D7 (sequencing and the sibling search),
      D8 (what is not taken).
- [ ] 1.6 **ON RATIFICATION**, `.openspec.yaml` gains `approved_by` and
      `approved_on` as a pure ADDITION beside a byte-unmoved drafting
      provenance — `kind` and `id` never move, which is the shape
      `add-drafted-proposal-origin` (issue #318) defined for this transition —
      and every document here moves to `Status: ratified` with one citation line
      naming the ruled labels. A ratification record is written under
      `review/`.

## 2. The measurement, taken before the design — DONE IN THIS PULL REQUEST

- [x] 2.1 **THE CORPUS WAS RE-MEASURED, NOT QUOTED.** Fresh clone and a
      worktree at `origin/main` `bcde1575`; the issue's method re-run over every
      top-level `openspec/changes/<change>/proposal.md`, read through the
      SHIPPED strict loader: **45** active proposals, **45** declaring
      `code_surface:`, **0** absent, **0** repeated, **0** refused by the
      loader. **4** declare `none` (the issue's 5 is stale by one) and **41**
      declare a non-`none` value.
- [x] 2.2 **THE GRAMMAR WAS DERIVED FROM THE POPULATION, NOT INVENTED.** Asking
      what FOLLOWS the declared head across the 45: an opening parenthesis
      **19**, an em dash **17**, a full stop **2** — **38 conforming** — against
      ordinary prose with no opener **5**, a possessive **1**, a YAML folding
      indicator **1** — **7 non-conforming**, in four classes (`design.md` D0
      names each by change and quotes its declaration).
- [x] 2.3 **`none` IS LAWFUL HERE, WHICH IS THE FIRST DIFFERENCE FROM THE
      SIBLING'S POPULATION.** *Realization axis declaration* names `none` as the
      `code_surface:` value for an empty surface and as the doc-only default, so
      all four carriers conform and the divergence lies entirely in the 41.
- [x] 2.4 **THE ARCHIVE WAS COUNTED AND NOT JUDGED**: **165** archived
      proposals, **119** declaring the field in their front matter, **3**
      outside the grammar. The plain `grep -l '^code_surface:'` returns **147**
      there — it over-counts by **28**, those being early packets that discuss
      the field in BODY prose at column 0, `2026-07-09-add-release-realization-flow`
      among them. The active side agrees exactly (45 = 45).
- [x] 2.5 **EXACTLY ONE MACHINE READER OF THE VALUE EXISTS**, confirmed by the
      issue's own command. `grep -rn code_surface scripts/ .github/` at
      `bcde1575`: seventeen lines, fourteen in `scripts/scope_globs.py` /
      `scripts/validate-scope-globs.py`, three in prose (one docstring, two
      comments), nothing in `.github/`. The display reader the sibling named for
      `target_release:` — `scripts/ideation_dashboard/generator.py` — **no
      longer exists**, removed with the five ideation-dashboard schemas at
      contract-v4.0 (`ce5c054e`).
- [x] 2.6 **THAT READER DERIVES ITS SET FROM THE GLOSS, AND THE WIDTH WAS
      MEASURED.** `scope_globs.code_surface_repositories` splits the whole
      declaration on `[\s,()/]+` and keeps every word that is not `none`:
      **3,421** distinct tokens across the 45; **767** from the widest single
      declaration; **27 of 45** yield an estate repository name their own head
      does not name; **3 of the 4** `none` carriers yield a non-empty set.
- [x] 2.7 **THE DEFECT IS LATENT, NOT STANDING, AND THE PACKET SAYS SO.**
      **0 of 45** active proposals declare `scope_globs:` at `bcde1575`, so the
      cross-consistency check is vacuous over the live corpus and bites the
      first time a `scope_globs:` lands.
- [x] 2.8 **THERE IS NO REPOSITORY INVENTORY TO RESOLVE AGAINST**, searched
      rather than assumed (`design.md` D1): `contracts/policies/repository-identity.yaml`
      is a former-to-current TRANSFER map carrying one row;
      `contracts/hermes-runtime/fixtures/domain-regression-inventory.yaml` is a
      five-row domain-factory FIXTURE that does not name `openxFactory`, the
      install repositories or the neutral products; `contracts/*-pin.yaml`
      carries one `source_repository:` each. The aggregation repository's
      `.gitmodules` does enumerate the estate and is not in this tree.
- [x] 2.9 **`kind: ad_hoc` IS CHECKED RATHER THAN ASSUMED.**
      `ideation/staging/` enumerated and `INDEX.md` read on 2026-09-12: no topic
      names the realization-axis front matter, the `code_surface` declaration, a
      repository-name grammar or a proposal front-matter validator.
- [x] 2.10 **NO SIBLING WRITES THESE REQUIREMENTS** (`design.md` D7, pasted
      there in full): of the eight open pull requests only #1014 touches this
      capability, and it ARCHIVES the sibling and promotes a different title;
      the three active changes with a `specs/release-realization/` delta write
      different requirement titles; the three titles added here appear nowhere
      in the corpus.

## 3. The realization — a house validator and a closed register, in a LATER pull request

**NONE OF § 3 IS IN THIS PULL REQUEST.** It is written here so ratification
knows exactly what it is ratifying, and so the realization pull request has a
task list rather than an intention.

- [ ] 3.1 `scripts/code_surface.py` (NEW) — the reader and judge. Reads the
      declaration through the SHIPPED strict loader
      `frontmatter_strict.read_front_matter`, adding no second parser; parses
      the DECLARED HEAD (`none`, or repository identifiers separated by `,` /
      ` and ` / ` + `); requires a GLOSS OPENER where a gloss follows; refuses a
      YAML folding indicator BY NAME; refuses a repeated declaration; loads and
      shape-checks the register; scans top-level active changes and counts the
      archive.
- [ ] 3.2 `scripts/validate-code-surface.py` (NEW) — the CLI, in
      `validate-scope-globs.py`'s shape. `[REPO_ROOT]` plus `--register PATH`
      (for the tests and for a consuming tree; the gate runs it with neither).
      Exit 0 clean, 1 an unreadable declaration, 2 an unusable or stale
      register; both present prints both and exits 1.
- [ ] 3.3 `scripts/code-surface-register.yaml` (NEW) — the standing divergences
      the same act does not correct, each with its declaration text as it
      stands, its class, its reason, its citation and the event that retires it.
      CLOSED: removable, never addable, with the closure ENFORCED by a baseline
      in the module (`design.md` D2). Not under `contracts/`, deliberately
      (`design.md` D5). **ITS POPULATION IS RE-MEASURED AT THE HEAD THE GATE
      LANDS ON** — seven at this packet's drafting, and a fact about that tree
      only.
- [ ] 3.4 **THE SEVEN DISPOSED OF AS § 1.3 RULES.** On the recommended option
      all seven are registered and none is swept. On option 2 the six are
      corrected — one re-punctuation each, every word of every gloss preserved
      verbatim — and one registered; on option 3 all seven are corrected. Under
      any option the population is re-measured at the landing head first, and a
      carrier that arrived after this drafting is disposed of there.
- [ ] 3.5 **NARROW `scripts/scope_globs.py`'s `code_surface_repositories`** to
      derive its set from the DECLARED HEAD, through the reader § 3.1 adds, so
      the field has one derivation and not two — **only if § 1.4 rules D4
      option 1**. Pinned by a test proving the function returns the head's
      identifiers and none of the gloss's, and by a before/after run of
      `python3 scripts/validate-scope-globs.py .` showing the live corpus
      unmoved (0 active proposals declare `scope_globs:`, § 2.7, so the change
      is unobservable there — which is what makes it landable without a sweep).
- [ ] 3.6 `tests/code_surface/test_code_surface_gate.py` (NEW) — the head parse
      and the opener requirement; the block-scalar refusal by name; the repeat
      refusal; absence as the promoted default and a present-but-empty value
      refused; both identifier spellings (`<name>` and `<owner>/<name>`); the
      list separators; `none` with and without a gloss; the archive read and
      never judged; the register's shape refusals, its closed baseline, and the
      stale-entry status; the derivation rule of § 3.5; and
      `test_corpus_code_surface_validates`, which runs the CLI over the LIVE
      tree so a new divergence reds the required `pytest-suite` with no workflow
      edit. **The test count is MEASURED at the realization and never carried
      from this task list.**
- [ ] 3.7 **NO WORKFLOW IS EDITED**, confirmed by running the suite rather than
      by reading the workflow: `pytest-suite` already runs everything under
      `tests/`, so a new test directory is collected with no registration
      anywhere.
- [ ] 3.8 **THE README ACTIVE ROW MOVES TO THE RATIFIED STANDING** in the same
      commit as § 1.6, and every figure it carries is re-measured at that
      commit rather than copied from here.

## 4. Verification — DONE IN THIS PULL REQUEST

**EVERY LINE BELOW IS A COMMAND THAT WAS RUN ON THIS TREE**, with its exit code
and its own output quoted. Nothing here anticipates § 3. The filing pull request
is openxFactory [#1018](https://github.com/opensoft/openxFactory/pull/1018),
opened as a DRAFT.

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate gate-code-surface-declarations
      --strict` (PATH CLI **1.2.0**) — **exit 0**, *"Change
      'gate-code-surface-declarations' is valid"*.
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **exit 1**,
      `Totals: 105 passed, 3 failed (108 items)`. The failure set is IDENTICAL
      to `origin/main` `bcde1575`'s, taken in the same shell from a worktree of
      it (`Totals: 104 passed, 3 failed (107 items)`):
      `change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle` and
      `change/disposition-codexfactory-regular-pr-council-clearance-archive`,
      all three failing on BOTH trees alike. This change is in neither set and
      the item count moves by exactly one.
- [x] 4.3 `python3 scripts/proposal-support.py . verify
      gate-code-surface-declarations` — **exit 0**, *"proposal support
      verification ok"*.
- [x] 4.4 `python3 scripts/validate-target-release.py .` — **exit 0**, *"46
      active proposals, 46 declaring — 22 `implemented`, 3 a named release, 21
      named by the register, 0 outside the vocabulary"*. This packet's own
      `target_release:` is judged by the sibling's live gate like every other
      active change, and the `+1` active over `origin/main`'s 45 is this
      packet's own `proposal.md`.
- [x] 4.5 `python3 scripts/validate-scope-globs.py .` — **exit 0**,
      *"scope_globs validation passed (all active changes conform)"*; and
      `python3 scripts/validate-sequenced-after.py .` — **exit 0**, *"46 active
      changes, 14 declaring the field"*, both archive-date arms passing.
- [x] 4.6 `python3 scripts/doc-health.py --single-repo .` — **exit 0** on this
      tree and on the `origin/main` `bcde1575` worktree alike, with the SAME
      band counts on both (**9** `severity=error`, **23** `severity=warning`)
      and **ZERO** findings naming this change. The comparison is of trees and
      not of runs, both taken in the same shell.
- [x] 4.7 **THE PER-CHANGE SWEEP LEDGER ROW**, seeded by the sanctioned tool and
      never hand-written: before the seed `--ledger-diff` reported the missing
      row and six derived-total mismatches, each moving by exactly one. SEEDED
      with `python3 scripts/validate-sequenced-after.py . --seed-ledger
      --moved-by '#1018'` — run AFTER the draft pull request existed, because
      the tool stamps `moved_by` with its number — *"wrote
      tests/sequenced_after/corpus-ledger.yaml (211 rows, 1 moved by #1018)"*.
      After it, `--ledger-diff` — **exit 0**, *"per-change sweep ledger
      consistent with the corpus (211 rows)"*.
- [x] 4.8 **README `## OpenSpec Records` ACTIVE ROW**, in house style, at the
      DRAFT standing — the drafting shape named outright (**`Status: draft` —
      NOT RATIFIED**), the ADDED-only shape and the absence of a
      `sequenced_after` hold, the D0 measurement, the one-reader finding, the
      four declared veto points, and the archive named as the separate act
      where #1013 closes.
- [ ] 4.9 **THE BOT BENCH**, taken and dispositioned item by item on the record.

## 5. Archive — OWED, NOT GIVEN

- [ ] 5.1 **PROMOTE THE THREE ADDED REQUIREMENTS INTO CANON**, byte-for-byte, in
      a SEPARATE pull request on a separate word, after § 1 is ruled and after
      the realization evidence this packet's `target_release` names.
      **THE PACKET'S OWN CLAUSE, IN ITS OWN WORDS:** `code_surface` here is NOT
      `none`, so *Realization archive gate* binds — this change SHALL NOT
      archive on landing and SHALL NOT archive on ratification. It archives when
      and only when § 3's realization pull request has MERGED into `main` and a
      `pytest-suite` run at the tree that merge carries is GREEN, both cited by
      reference in the archive pull request. An archive act that cites this
      filing's own green run as its realization evidence is citing the wrong
      run: this pull request realizes nothing.
- [ ] 5.2 **THE ORIGIN ISSUE IS CLOSED AT THE ARCHIVE PULL REQUEST AND NOWHERE
      ELSE**, by a closing keyword written THERE against openxFactory issue
      1013. No closing keyword appears in this pull request's body or in any
      commit message on this branch, in any form, quoted or otherwise.

## 6. Measured, and deliberately NOT taken here

- [ ] 6.1 **AN INVENTORY OF THE ESTATE'S REPOSITORIES.** Without one the gate
      judges a repository identifier's SHAPE and never its MEMBERSHIP, so a
      plausible misspelling passes. Building the inventory carries its own
      authority question — who admits a repository to the estate, and what a row
      means for a repository that is pinned rather than governed — and it is the
      successor that would lift `design.md` D1's stated bound.
- [ ] 6.2 **WHETHER `code_surface:` SHOULD BECOME A STRUCTURED FIELD.** Giving
      it `scope_globs:`'s shape would make a grammar unnecessary, because YAML
      would supply one. It is a `## MODIFIED` block over the title
      `add-structured-scope-substrate` holds, with the sequencing hold that
      carries, and it would obsolete a declaration form 45 active packets
      already write.
- [ ] 6.3 **THE ARCHIVE IS NOT TOUCHED.** The 3 archived declarations outside
      the grammar, and the 28 archived packets whose `code_surface:` line sits
      in body prose, are frozen record: read, counted, judged never.
- [ ] 6.4 **NO OTHER ESTATE REPOSITORY IS SWEPT OR REGISTERED.** The validator
      takes a `REPO_ROOT` and refuses a tree with no register rather than
      assuming an empty one; each repository's register would be its own act.
- [ ] 6.5 **WHETHER A `none` DECLARATION MAY CARRY A GLOSS AT ALL.** Three of
      the four carriers do, and this packet admits it. A stricter rule would
      refuse three lawful declarations for tidiness.
