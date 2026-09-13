# Tasks: gate-code-surface-declarations

Status: ratified
Ratified by: gate-code-surface-declarations — 2026-09-13, Brett Heap, verbatim "ratify" (recorded at https://github.com/opensoft/openxFactory/pull/1018#issuecomment-5649742729)
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

**§ 1 (RATIFICATION) IS CLOSED: BRETT HEAP RULED ON 2026-09-13 AT 00:41Z**,
verbatim **"ratify"**, recorded at
[#1018](https://github.com/opensoft/openxFactory/pull/1018#issuecomment-5649742729).
**THE WORD IS BARE** — it ratifies the PACKET and names no option individually,
so each of `design.md`'s four declared veto points stands at the option this
packet encodes, the RECOMMENDED one in all four; no wording moved on the ruling.
Taking openxFactory issue #1013 — an unclaimed residue another lane filed —
commissioned the AUTHORING and decided no wording; that provenance is recorded
in `.openspec.yaml` and is untouched by this ratification, which adds the
approval pair beside it.

**§ 5 (ARCHIVE) IS ENTIRELY OPEN.** `code_surface` is non-empty, so under
`release-realization` this packet SHALL NOT archive on landing. **THIS PACKET'S
OWN WORD ON ITS OWN ARCHIVE, WRITTEN HERE SO NO LATER READER HAS TO INFER IT:
this change archives only when § 3's realization pull request has MERGED into
`main` AND a `pytest-suite` run at the tree that merge carries is GREEN, and not
before — merged-plus-green at canon's grain, never archive-on-landing.**
openxFactory #1013 closes THERE and at no earlier pull request.

**§ 6 IS UNTICKED ON PURPOSE**: residue, measured and deliberately not taken.

## 1. Ratification — GIVEN 2026-09-13

- [x] 1.1 **`design.md` D1 RULED — "GATE THE GRAMMAR"**, the RECOMMENDED and
      already-encoded option. The options as put: option 1, a declared head
      (`none`, or repository identifiers separated by `,` / ` and ` / ` + `)
      followed by a REQUIRED gloss opener, with the head judged and the gloss
      never, and NO membership check (recommended); option 2, judge only the
      FIRST TOKEN as the sibling does — measured cost: it refuses 2 of the 7 and
      passes the other 5, including a head whose second and third
      "repositories" are the words `the` and `PROJECT`, and it cannot read a
      multi-repository declaration at all; option 3, resolve each identifier
      against a repository inventory — measured cost: this repository defines
      none, so the gate would refuse all 41 non-`none` declarations on the day
      it landed.
- [x] 1.2 **`design.md` D2 RULED — "VALIDATOR PLUS CLOSED REGISTER PLUS ADDED
      REQUIREMENT"**, the RECOMMENDED and already-encoded option, so the
      register's closure stays SHALLed in the delta rather than left to the
      implementation. The options as put: option 1, an ADDED requirement, a
      house validator and a CLOSED register, following
      `gate-realization-axis-vocabulary` (recommended); option 2, the
      requirement alone with a bare refusal and no register — cost: it cannot
      land unless D3 option 3 lands with it, coupling two independent decisions
      into one word; option 3, an ADVISORY gate — cost: an advisory gate refuses
      nothing, which is the state #1013 filed about.
- [x] 1.3 **`design.md` D3 RULED — "REGISTER ALL SEVEN, SWEEP NONE"**, the
      RECOMMENDED and already-encoded option. **THE RULING FIXES THE
      DISPOSITION AND NEVER THE COUNT**: the population is a fact about a TREE
      and § 3.3 re-measures it at the head the gate lands on. The options as
      put: option 1, register all seven and sweep none (recommended); option 2,
      sweep the six whose correction carries no judgment and register the one
      that does; option 3, sweep all seven. The reason this departs from the
      sibling's ruled sweep is written out in `design.md` D3 and is two things:
      a head correction RE-PUNCTUATES another lane's ratified prose rather than
      replacing one token whose meaning the author's own gloss supplied, and for
      `split-opendox-two-layer-product` it is a judgment about what counts as a
      repository. The structural difference stands beside it: the sibling swept
      "in this PR" because its realization was in that same pull request, while
      here any sweep lands in § 3's LATER pull request.
- [x] 1.4 **`design.md` D4 RULED — "REUSE AS THE CONSUMER AND NARROW THE
      EXTRACTOR"**, the RECOMMENDED and already-encoded option, so § 3.5 is OWED
      rather than conditional. The options as put: option 1, reuse the
      `scope_globs:` machinery as the CONSUMER and narrow
      `scripts/scope_globs.py`'s `code_surface_repositories` to the declared
      head, with the rule SHALLed in the delta (recommended); option 2, leave
      the extractor and name a successor — cost: the field is then read two
      ways, strictly by the new gate and permissively by the authorization
      check; option 3, leave the extractor and register the 27 — cost: it
      registers 27 packets for a defect that is in the reader, not in any of
      their declarations.
- [x] 1.5 **THE RULING IS A BARE WORD AND IS RECORDED AS ONE.** Brett Heap's
      word of 2026-09-13T00:41Z is verbatim **"ratify"**; unlike the sibling's
      three labelled rulings it names no option individually. It ratifies the
      PACKET, and the packet encodes the recommended option at each of D1
      through D4, which is why § 1.1 through § 1.4 read as they do and why
      **nothing in the delta moved on the ruling**. Recorded at
      [#1018](https://github.com/opensoft/openxFactory/pull/1018#issuecomment-5649742729).
- [x] 1.6 **D0 AND D5 THROUGH D8 WERE CARRIED BESIDE THEM AND NONE WAS
      VETOED**, each with its alternative written out and each available to be
      vetoed in the same ruling: D0 (the measurement and its method), D5 (the
      code surface, the three exit codes, the register's home outside
      `contracts/`), D6 (why an OpenSpec change and not a patch), D7 (sequencing
      and the sibling search), D8 (what is not taken). The bare word reached the
      packet as a whole; it named none of the carried five and none of them
      moves.
- [x] 1.7 **THE RULING REACHES THE FIRST BENCH ROUND, ON ITS OWN WORDS**, which
      direct that the two confirmed findings be fixed *"before the record is
      cut, so the ratified packet includes them"*. Both are taken and both are
      in the ratified text: `none` reserved out of REPOSITORY IDENTIFIER with a
      tenth scenario, and the FAIL-CLOSED rule for a registered-exception packet
      that later declares `scope_globs:` with a fourth scenario on the
      derivation requirement. The third open thread is REFUSED as false on
      measurement. `design.md` D9 records all three; § 4.9 carries the ledger
      line.
- [x] 1.8 **THE RATIFICATION RECORD IS CUT IN THIS PUSH.** `.openspec.yaml`
      gains `approved_by` and `approved_on` as a pure ADDITION beside a
      byte-unmoved drafting provenance — `kind` and `id` never move, which is
      the shape `add-drafted-proposal-origin` (issue #318) defined for this
      transition — and `proposal.md`, `design.md` and this file carry
      `Status: ratified` with ONE citation each, the ruling comment URL, which
      is the record (estate rule of 2026-09-10). **THE FLIP IS NOT
      HEADER-ONLY**: the draft-voiced prose in all three documents is revised
      with it — the veto-point framing, the *what this packet does NOT do* list,
      § 1's own preamble, and the conditional in `proposal.md`'s `code_surface:`
      declaration that read "only if D4 is ruled as recommended" — because a
      header flip over unrevised draft language is the defect Opsx #397
      recorded on 2026-09-12.

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
      the DECLARED HEAD — EITHER the single token `none` OR a list of
      repository identifiers separated by `,` / ` and ` / ` + `, the two
      EXCLUSIVE, so a MIXED head such as `none, openxFactory` is REFUSED and no
      derived set is computed for it, in either order and wherever in the list
      the token sits (`design.md` D9 (a)); requires a GLOSS OPENER where a gloss
      follows; refuses a YAML folding indicator BY NAME; refuses a repeated
      declaration; loads and shape-checks the register; scans top-level active
      changes and counts the archive.
- [ ] 3.2 `scripts/validate-code-surface.py` (NEW) — the CLI, in
      `validate-scope-globs.py`'s shape. `[REPO_ROOT]` plus `--register PATH`
      (for the tests and for a consuming tree; the gate runs it with neither).
      Exit 0 clean, 1 an unreadable declaration, 2 an unusable or stale
      register; both present prints both and exits 1.
- [ ] 3.2a **NO PATH THIS GATE OPENS MAY BE REACHED THROUGH A SYMLINK**, the
      sibling's guard MIRRORED EXACTLY — imported from
      `scripts/target_release.py` or restated beside it, the realization's
      choice, but never APPROXIMATED, because a guard that is nearly the
      sibling's is a guard whose gaps nobody has measured. `Path.is_file()`
      and `Path.read_text()` BOTH FOLLOW SYMLINKS, so without this a committed
      link would make the gate read exception data, or declarations, from
      OUTSIDE THE CHECKOUT: silently, and differently per runner. There are
      TWO surfaces, the sibling guards them with two DIFFERENT semantics, and
      both are mirrored exactly rather than approximated.
      **(i) THE REGISTER IS REFUSED UNREAD** — the `--register PATH` of § 3.2
      and the default beside the module ALIKE — when the file ITSELF is a
      symlink OR when ANY directory between it and its own top is one, the
      check running UNCONDITIONALLY before `is_file()` or `read_text()`, so no
      branch treats a supplied path differently from the default and no branch
      can forget one of them. A leaf-only check does not close it:
      `linkdir/register.yaml` has a perfectly ORDINARY leaf and `read_text()`
      still follows `linkdir`. The ancestor walk is UNANCHORED — climbing to
      `/` for an absolute path and to `.` for a relative one — because a
      register named on the command line is deliberately allowed to live
      wherever a test tree or a consuming repository puts it, so there is no
      `REPO_ROOT` to check "outside of"; `scripts/target_release.py`'s
      `load_register` (line 448) and `_has_symlinked_ancestor` (line 417) are
      the exact shape. An unusable register is EXIT 2 by § 3.2, and the
      refusal names the remedy: a regular file at an ordinary, unsymlinked
      path.
      **(ii) EVERY DISCOVERED PROPOSAL PATH IS ADMITTED ONLY THROUGH THE
      ANCHORED TEST**, active and archived alike — the one
      `scripts/target_release.py`'s `_unescaped` (line 569) applies: resolve
      the candidate AND `REPO_ROOT` on BOTH sides and require the candidate to
      land exactly where a symlink-free tree would have put it, which closes
      every component in ONE comparison rather than one at a time as each is
      found. A path that fails it is NOT READ, NOT JUDGED and NOT COUNTED, and
      that is a DROP rather than an exit-1 finding, because the fact being
      reported would otherwise be a fact about another tree: a proposal read
      from outside `REPO_ROOT` would be judged and named in a finding as
      though this tree carried it, and a DANGLING link is the same defect
      wearing the other face — the proposal vanishes and the tree is judged on
      a corpus it does not have. Resolving `REPO_ROOT` on BOTH sides is what
      keeps a scratch tree reached through a symlinked `/tmp` from being
      mistaken for the escape.
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
      the field has one derivation and not two — **OWED, § 1.4 having ruled D4
      option 1**. Pinned by a test proving the function returns the head's
      identifiers and none of the gloss's, and by a before/after run of
      `python3 scripts/validate-scope-globs.py .` showing the live corpus
      unmoved (0 active proposals declare `scope_globs:`, § 2.7, so the change
      is unobservable there — which is what makes it landable without a sweep).
- [ ] 3.5a **FAIL CLOSED WHERE THE HEAD IS CARRIED BY THE REGISTER RATHER THAN
      READ BY THE GRAMMAR** (`design.md` D9 (b)). A proposal the register names
      has NO head-derived set, so `code_surface_repositories` SHALL NOT return
      one for it, and `validate_cross_consistency` SHALL REFUSE a registered
      proposal that also declares `scope_globs:`, naming BOTH the proposal and
      the register entry that carries its declaration. **THE TWO SUBSTITUTES
      ARE FORBIDDEN BY NAME AND EACH GETS ITS OWN REFUSAL TEST**: no fallback to
      a set derived from the whole declaration (it would re-admit the 3,421-token
      gloss surface), and no empty-set substitution (it would report the fault
      against the structured scope rather than against the code-surface
      declaration that causes it). The refusal message SHALL name the remedy —
      bring the declaration into the grammar, which retires the entry in the
      same act.
- [ ] 3.5b **§ 3.5a's REFUSAL MUST BE EXPRESSIBLE AT THE POINT OF ENFORCEMENT,
      AND ON THIS TREE IT IS NOT** — so the PROPOSAL IDENTITY and the REGISTER
      ENTRY travel the reader path, and not a bare set of tokens. Measured
      here rather than asserted: `scripts/validate-scope-globs.py:68` calls
      `sg.code_surface_repositories(front)` with the front-matter mapping
      ALONE, and `scope_globs.validate_cross_consistency` (line 391) receives
      a bare `Iterable[str]`, so at the moment of judgment NOTHING
      distinguishes a REGISTERED EXCEPTION from an EMPTY SURFACE — and the two
      values a narrowed derivation could hand it are exactly the two § 3.5a
      forbids by name: `None` SKIPS the cross-consistency check outright
      (`validate_scope_globs`'s `if code_surface_repos is not None`, line 414)
      and an empty set raises the GENERIC *"names repository … not in
      code_surface"* message against the structured scope. **NARROWING
      `code_surface_repositories` ALONE THEREFORE CANNOT REALIZE THE RATIFIED
      RULE, AND § 3.5 IS NOT FINISHED BY DOING IT.**
      **THE SHAPE IS CHOSEN HERE RATHER THAN LEFT TO THE IMPLEMENTER, AND IT
      IS THE ONE THE EXISTING CODE ALREADY SUPPORTS: THE DERIVATION RETURNS A
      TYPED CARRIER** — either the head-derived set, or the ABSENCE of one
      carrying the proposal id and the register entry that tolerates its
      declaration — **AND THAT CARRIER IS THREADED THROUGH
      `validate_scope_globs` INTO `validate_cross_consistency`, WHICH RAISES A
      `ScopeGlobsError` SUBCLASS NAMING BOTH.** `scripts/scope_globs.py`
      already carries both halves of that idiom: a frozen-dataclass result
      type (`ScopeGlobs`, line 235) and an error SUBCLASS for a distinct fact
      every existing caller keeps catching (`ScopeGlobsResolutionError`, line
      106). **THE WIDENING IS CHEAP, AND THE COST IS MEASURED RATHER THAN
      GUESSED**: `code_surface_repositories` has exactly ONE in-tree caller
      (`scripts/validate-scope-globs.py:68`) and `validate_cross_consistency`
      exactly one (`validate_scope_globs`, line 415), so neither signature
      owes a sweep; `validate_scope_globs` itself only PASSES THE CARRIER
      THROUGH, its own `code_surface_repos` parameter accepting EITHER form,
      and **A BARE ITERABLE SHALL KEEP WORKING** — read as a head-derived set
      carrying no registered-exception context — which is what keeps the
      shipped tests that call
      `validate_scope_globs(..., code_surface_repos={"R"})` with a plain set
      passing unedited. **THE CHEAPER ALTERNATIVE IS REJECTED ON THE RECORD**:
      raising from the derivation itself is fewer lines, but it moves the
      refusal UPSTREAM of the cross-consistency check the ratified requirement
      names as the refuser. The consumer owes nothing it does not already
      hold: `_validate_change` receives the `proposal` path whose
      `.parent.name` IS the change id, and `validate_corpus` already prefixes
      that id onto every problem it prints. Pinned by a test asserting the
      refusal names the PROPOSAL and its REGISTER ENTRY — § 3.6's two
      forbidden-substitute tests prove what the run must NOT say, and this one
      proves what it MUST.
- [ ] 3.6 `tests/code_surface/test_code_surface_gate.py` (NEW) — the head parse
      and the opener requirement; the block-scalar refusal by name; the repeat
      refusal; absence as the promoted default and a present-but-empty value
      refused; both identifier spellings (`<name>` and `<owner>/<name>`); the
      list separators; `none` with and without a gloss; **a MIXED `none`-plus-
      identifier head refused in either order and at every list position**; the
      archive read and never judged; the register's shape refusals, its closed
      baseline, and the stale-entry status; the derivation rule of § 3.5;
      **§ 3.5a's fail-closed rule, with one test per forbidden substitute — a
      registered proposal declaring `scope_globs:` refused, never granted a
      whole-declaration set and never granted an empty one**; and
      `test_corpus_code_surface_validates`, which runs the CLI over the LIVE
      tree so a new divergence reds the required `pytest-suite` with no workflow
      edit. **The test count is MEASURED at the realization and never carried
      from this task list.**
- [ ] 3.6a **§ 3.2a's TWO PATH-BOUNDARY REFUSALS GET THEIR OWN TESTS, BOTH
      SURFACES AND BOTH DEPTHS**, in § 3.6's own
      `tests/code_surface/test_code_surface_gate.py` and in the sibling's
      shape (`tests/target_release/test_target_release_gate.py` carries the
      pattern for every case named here). THE REGISTER: refused when the file
      named on `--register` is ITSELF a symlink, and refused again when it is an
      ordinary file reached through a symlinked ANCESTOR DIRECTORY — each
      proved END TO END through the CLI at exit 2, each also with the link
      pointing OUTSIDE the tree, and a DANGLING link refused AS A SYMLINK
      rather than crashing. THE CORPUS WALK: a discovered proposal NOT READ
      and NOT COUNTED when the `proposal.md` is a symlink, when an ordinary
      `proposal.md` sits inside a symlinked CHANGE DIRECTORY, and when the
      link dangles — on the ACTIVE arm and on the archive count alike. Beside
      them the NEGATIVE that keeps the guard from over-refusing: a `REPO_ROOT`
      reached through a symlink still finds every proposal it really carries.
- [ ] 3.7 **NO WORKFLOW IS EDITED**, confirmed by running the suite rather than
      by reading the workflow: `pytest-suite` already runs everything under
      `tests/`, so a new test directory is collected with no registration
      anywhere.
- [x] 3.8 **THE README ACTIVE ROW MOVED TO THE RATIFIED STANDING**, in the same
      commit as § 1.8 — the drafting-shape sentence replaced by the ruling, its
      date, its verbatim word and the recording comment, the bareness of the
      word named, the four veto points shown as RULED at the recommended option,
      and the bench round's two taken findings carried. **Every figure it
      carries was RE-MEASURED at that commit rather than copied**: the scenario
      count is read from the delta file (18 = 10 + 4 + 4) and the corpus figures
      re-derived. It is the one § 3 box this pull request closes, because the
      row is bookkeeping the ratification owes and not realization.
      (Re-numbered from the § 1.6 the drafting text cited; the ratification
      tasks are now § 1.1 through § 1.8.)

## 4. Verification — DONE IN THIS PULL REQUEST

**EVERY LINE BELOW IS A COMMAND THAT WAS RUN ON THIS TREE**, with its exit code
and its own output quoted. Nothing here anticipates § 3. The filing pull request
is openxFactory [#1018](https://github.com/opensoft/openxFactory/pull/1018),
opened as a DRAFT.

- [x] 4.1 `OPENSPEC_TELEMETRY=0 openspec validate gate-code-surface-declarations
      --strict` (PATH CLI **1.2.0**) — **exit 0**, *"Change
      'gate-code-surface-declarations' is valid"*.
- [x] 4.2 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` — **exit 1**,
      `Totals: 104 passed, 3 failed (107 items)`. The failure set is IDENTICAL
      to `origin/main` `bcde1575`'s, taken in the same shell from a worktree of
      it (`Totals: 104 passed, 3 failed (107 items)`):
      `change/disposition-codexfactory-declared-renames`,
      `change/disposition-codexfactory-floor-relocation-retitle` and
      `change/disposition-codexfactory-regular-pr-council-clearance-archive`,
      all three failing on BOTH trees alike, and this change is in neither set.
      **THE ITEM COUNT NOW MOVES BY ZERO, AND THE CAUSE IS THIS BRANCH'S OWN
      MERGE — RE-MEASURED AT THE HEAD RATHER THAN REASONED FROM THE OLD
      FIGURE**: at `df96018c`, one commit earlier, the same command in the same
      shell returned `Totals: 105 passed, 3 failed (108 items)` and the count
      moved by exactly one. `df230260` then merged `origin/main` `a1429885`,
      which ARCHIVED the sibling `gate-realization-axis-vocabulary` into
      `openspec/changes/archive/2026-09-12-gate-realization-axis-vocabulary` —
      ONE ACTIVE CHANGE OUT AS THIS PACKET PUTS ONE IN — so the totals now
      COINCIDE with the baseline's instead of exceeding them by one. A count is
      a fact about a tree and is never carried across a merge.
- [x] 4.3 `python3 scripts/proposal-support.py . verify
      gate-code-surface-declarations` — **exit 0**, *"proposal support
      verification ok"*.
- [x] 4.4 `python3 scripts/validate-target-release.py .` — **exit 0**, *"45
      active proposals, 45 declaring — 21 `implemented`, 3 a named release, 21
      named by the register, 0 outside the vocabulary"*. This packet's own
      `target_release:` is judged by the sibling's live gate like every other
      active change. **THE ACTIVE COUNT EQUALS `origin/main` `bcde1575`'s 45
      RATHER THAN EXCEEDING IT BY ONE, FOR THE REASON § 4.2 RE-MEASURES**: the
      merge archived `gate-realization-axis-vocabulary`, which itself declared
      `target_release: implemented`, so it carried one active proposal and one
      `implemented` OUT of the corpus — 46 to 45 and 22 to 21, the figures this
      box held at `df96018c` — exactly as this packet's own `proposal.md`
      carries one of each IN.
- [x] 4.5 `python3 scripts/validate-scope-globs.py .` — **exit 0**,
      *"scope_globs validation passed (all active changes conform)"*; and
      `python3 scripts/validate-sequenced-after.py .` — **exit 0**, *"45 active
      changes, 13 declaring the field"*, both archive-date arms passing. These
      two are `bcde1575`'s own counts for the same reason: the sibling the
      merge archived declared `sequenced_after: []`, so both figures came down
      by one with it from the 46 and the 14 this box held at `df96018c`.
- [x] 4.6 `python3 scripts/doc-health.py --single-repo .` — **exit 0** on this
      tree and on the `origin/main` `bcde1575` worktree alike, with the SAME
      band counts on both **AS OF 2026-09-13** (**9** `severity=error`,
      **26** `severity=warning`), a normalized finding-set diff between the
      two trees that is **EMPTY** — **87** findings each side, identical line
      for line once the `repo=` directory token is normalized, so every band
      and not only these two is unmoved — and **ZERO** findings naming this
      change. **THE WARNING BAND MOVED FROM 23 TO 26 AT THE UTC-MIDNIGHT AGING
      BOUNDARY AND NOT ON THIS BRANCH**, which is why the figure is quoted
      with its date: `doc-health` defaults `--as-of` to today UTC, three
      `staged-candidate-aging` thresholds crossed overnight on both trees
      alike (`contracts/avatar-client-lab/README.md` and
      `examples/avatar-first-ui/fixtures/README.md` reaching 60 days,
      `ideation/staging/openxdox-install-app-provisioning` reaching 30), and
      re-running THIS tree with `--as-of 2026-09-12` still returns the earlier
      **23**. Both sides were therefore re-taken on the SAME day rather than
      one being carried, and the comparison is of trees and not of runs, both
      taken in the same shell.
- [x] 4.7 **THE PER-CHANGE SWEEP LEDGER ROW**, seeded by the sanctioned tool and
      never hand-written: before the seed `--ledger-diff` reported the missing
      row and six derived-total mismatches, each moving by exactly one. SEEDED
      with `python3 scripts/validate-sequenced-after.py . --seed-ledger
      --moved-by '#1018'` — run AFTER the draft pull request existed, because
      the tool stamps `moved_by` with its number — *"wrote
      tests/sequenced_after/corpus-ledger.yaml (211 rows, 1 moved by #1018)"*.
      After it, `--ledger-diff` — **exit 0**, *"per-change sweep ledger
      consistent with the corpus (211 rows)"*.
- [x] 4.8 **README `## OpenSpec Records` ACTIVE ROW**, in house style. It first
      landed at the DRAFT standing in `5fe7a0c8` — the drafting shape named
      outright, the ADDED-only shape and the absence of a `sequenced_after`
      hold, the D0 measurement, the one-reader finding, the four declared veto
      points, and the archive named as the separate act where #1013 closes — and
      **MOVED TO THE RATIFIED STANDING BY THIS RATIFICATION** (§ 3.8), which is
      the only edit this round makes to it besides the re-measured scenario
      count.
- [x] 4.9 **THE BOT BENCH — ROUND 1, taken and dispositioned item by item on
      the record** (`design.md` D9). FIVE threads. TWO were taken before the
      ruling and are resolved: a scenario count overstated by one (`a5a707c7`)
      and a `§ 4` header reading DONE over unticked boxes (`83b13051`) — both
      the packet's own bookkeeping contradicting its own diff. Of the three
      standing at the ruling, **TWO ARE TAKEN INTO THE RATIFIED TEXT**: (a)
      `none` reserved out of REPOSITORY IDENTIFIER, the two head forms made
      EXCLUSIVE in the requirement's first line, with a tenth scenario refusing
      a mixed head; and (b) the FAIL-CLOSED rule for a registered-exception
      packet that later declares `scope_globs:`, with both substitutes forbidden
      by name and a fourth scenario on the derivation requirement. **ONE IS
      REFUSED AS FALSE, ON MEASUREMENT**: the corpus-ledger finding claims the
      row is absent, and the row is at
      `tests/sequenced_after/corpus-ledger.yaml:236` on this branch with the
      file in this pull request's diff, `--ledger-diff` exit 0, *"per-change
      sweep ledger consistent with the corpus (211 rows)"* — seeded by the
      sanctioned tool at `83b13051` exactly as § 4.7 records. A finding is not
      taken for having been made, and the refusal is recorded on that thread
      with the line number, the command and the exit code. **Later rounds, and
      the round the un-draft fires, are dispositioned the same way and are not
      claimed by this box.**

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
