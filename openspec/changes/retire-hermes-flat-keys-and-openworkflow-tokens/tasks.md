# Tasks: retire-hermes-flat-keys-and-openworkflow-tokens

**AMENDED 2026-09-01, AFTER RATIFICATION: §§ 2, 3 AND 6 ARE PERFORMED AND ARE
NOW TICKED.** They were performed by a SEPARATE realization pull request from an
independent clone, against the packet as ratified, and the evidence sits under
each box. **§ 4 (the `contract-v3.0` cut), § 5 (post-cut verification) and § 7
(the archive gate) are untouched and remain OPEN** — the cut is its own act
under § Bundle Realization Order, it allocates its number late, and this
realization neither performs it nor claims a place in its ordering. **§ 1.6 is
also untouched: a Codex pass is still owed** (see the box for what the
realization's own attempt returned).

**WHAT THE ORIGINAL HEADER SAID, AND WHY IT STAYS TRUE.** It read: *"NOTHING
BELOW SECTION 1 IS PERFORMED BY THIS PROPOSAL, AND RATIFICATION DOES NOT CHANGE
THAT."* That sentence is about the PROPOSAL and the RATIFYING ACT, and it is
untouched — the packet is `Status: ratified` (Brett Heap, 2026-09-01, in
session, at pull request #551 tip `64907604`, landed as squash `59eb913e`;
record `review/ratification-2026-09-01.md`), and that act moved no validator
line, no policy row and no changelog row. What changed is that the later
commission it named has been carried out. The distinction is kept rather than
collapsed, because collapsing it would make the ratification look like the thing
that performed the retirements.

Sections 2-5 are the realization; § 7 is the archive gate that the realization
must clear before this change may archive at all.

**EVIDENCE CONVENTION**, the family's standard: a box closes on a FACT that
survives the session — a merged commit, a named run, a recorded command output,
a file path — never on an intention.

## 1. Proposal (this pull request)

- [x] 1.1 Author the packet — `proposal.md`, `design.md`, `tasks.md`,
      `.openspec.yaml`, and the `contract-deprecation-execution` delta — off
      `origin/main`, citing issue #522, Brett's 2026-09-01 ruling comment on it,
      and the measurement memo.
- [x] 1.2 Re-verify the memo's facts against the tree rather than carrying them.
      Recorded in `proposal.md` § "What the measurement found": FIVE findings the
      memo did not carry — the fallback retirement being a REPLACEMENT and not a
      deletion (a bare deletion widens silently at a major); the `openworkflow`
      branch's SHADOWING (it widens one case as well as narrowing another);
      entry 2's entry under-declaring its own prefix by one character, raised in
      review of this PR; the `Owner layer constraint` canon/code severity
      divergence; and the `hermes.domain_overlay` vs `omnigent.domain_overlay`
      path collision.
- [x] 1.3 Validate: `OPENSPEC_TELEMETRY=0 openspec validate
      retire-hermes-flat-keys-and-openworkflow-tokens --strict` and
      `--all --strict`, both green.
- [x] 1.4 List the change in README § OpenSpec Records.
- [x] 1.5 **RATIFIED by the repository owner** — Brett Heap, 2026-09-01, in
      session ("ratify #551 and #552"), at pull request #551 tip `64907604`, on
      an orchestrator's report of the two packets read together. Record:
      `review/ratification-2026-09-01.md`. Ratification authorizes the
      requirement text and performs none of the realization below.
- [ ] 1.6 **Adversarial review to convergence — STILL OPEN, and the order this
      box originally stated was INVERTED by events rather than met.** It was
      written as "review to convergence, THEN ratification"; what happened is
      that six Copilot rounds ran and every finding was taken, while **every one
      of four `@codex review` requests returned a PROVIDER USAGE-LIMIT REFUSAL
      and no verdict**. The absence was disclosed to Brett and he ratified
      against it. **A CODEX PASS REMAINS OWED and is blocked by nothing in this
      packet**; whatever it returns routes to the amendment lane, not to doubt
      about the ratification.
      **THE REALIZATION TRIED AGAIN AND WAS REFUSED AGAIN — FIVE MORE TIMES,
      NINE IN ALL, STILL ZERO VERDICTS.** On the realization pull request
      **#562**, the automatic request on each push plus three explicit
      `@codex review` comments each returned the same provider response and no
      review:

      | time (UTC), 2026-09-01 | head | response |
      |---|---|---|
      | 12:36:39 | `8731fea6` | *"You have reached your Codex usage limits for code reviews."* |
      | 12:36:46 | `8731fea6` | same |
      | 12:39:54 | `8731fea6` | same |
      | 13:49:59 | `5b026e4c` | *"You have reached your Codex usage limits."* |
      | 13:51:15 | `5b026e4c` | *"…usage limits for code reviews."* |

      **The refusal is the provider's usage ceiling, and it is neither a
      finding nor a silence basis.** No Codex review names any head of either
      branch. The pass stays OWED and stays unblocked; this box stays OPEN.
      **What DID run on #562: Copilot, one round, TWO findings, BOTH TAKEN** —
      the domain-starter subprocess now runs under `deterministic_environment()`
      with an explicit timeout, matching the rest of this package rather than
      inheriting the ambient environment; and the scaffolded-stack assertion is
      no longer `list(hermes) == ["layers"]`, an order-dependent test that would
      have failed the day the starter grew a new NON-deprecated hermes key
      — it asserts what the box is actually about, `layers` present and every
      deprecated key absent. **Copilot's SECOND round, against the fixed head
      `f259ca03`, generated NO NEW COMMENTS.** Its THIRD, against `22866c03`,
      generated ONE — **and it is the best finding of the arc, because it
      caught this packet's own § 2.1 hazard reproduced one file over by the
      realization itself.** The generated validator's
      `stack.get("hermes", {}).get("layers") or []` iterates NOTHING when
      `layers` is present but not a list, so it would skip every overlay-path
      check and report `OK` on a scaffold the CANONICAL validator refuses — a
      generated repository quietly validating less than it claims, which is the
      silent-widening shape this packet spends four paragraphs forbidding.
      TAKEN: the generated validator now ERRORS on the type before iterating,
      and a parametrized test drives all four non-list shapes — absent, `{}`, a
      string, an int — through BOTH validators and asserts each refuses.
      Its FOURTH, against `5b026e4c`, generated NO NEW COMMENTS. **Four
      rounds, three findings, three taken, none refuted, converged.** Sourcery
      returned an access-tier upsell, not a review, exactly as it did on #551.
      **AND THE INHERITED `main` RED THE RATIFICATION RECORD DISCLOSED IS
      GONE.** § 4 of that record names
      `tests/doc-health/test_modified_block_currency_self_gate.py::test_every_carriage_ledger_finding_over_the_real_tree_is_named`,
      PR #510's carriage-ledger subject, red on `main` at `1a69b7cb` and still
      at `1c1dcbbe`. It was fixed on `main` by **#557** (*"The ledger names its
      eighth subject"*, merged 2026-09-01T06:59Z) — AFTER that record was
      written. The full local suite on this branch passes it and does not list
      it, so this realization inherits no red and attributes none. Recorded
      here because the record's § 4 would otherwise read as current.

## 2. Speckit F1 — the validator retirements

**One feature, both retirements, because they are one file and one class.**

- [x] 2.1 `scripts/validate-domain-factory.py`: delete `LEGACY_HERMES_KEYS`
      (`:60-70`) and REPLACE the `else` arm of `check_hermes` (`:189-200`) —
      the warn line, the flat-key resolution loop, and the per-role
      `no overlay resolvable` check — **with an explicit error**.
      **DO NOT SIMPLY DELETE THE ARM.** The `hermes.layers missing required
      role` errors at `:186-188` sit INSIDE the `if isinstance(declared, list)`
      branch, so a bare deletion leaves a `layers`-less stack falling straight
      through to `for role, layer in layers.items()` with an EMPTY map and
      producing no finding at all — a silent WIDENING at a major, and the exact
      opposite of the retirement. The replacement is one error naming the
      missing or non-list `hermes.layers`.
      **DONE, AS A REPLACEMENT.** The nine-key map is gone; the `else` arm of
      `resolve_layers` — the function `proposal.md` calls `check_hermes`, which
      is the only name discrepancy between the packet and the tree — now holds
      exactly one line: `rpt.error("stack.yaml: hermes.layers is missing or is
      not a list; declare it with the canonical roles
      customer/client/domain (the legacy flat-key fallback read was removed at
      contract-v3.0)")`, with the reason for the replacement written as a
      comment above it so a later editor cannot re-delete it into silence.
      MEASURED both ways on a `layers`-less probe carrying six flat keys, the
      two validators run side by side:
      `WARN: stack.yaml: hermes uses legacy flat keys … / 0 error(s), 5
      warning(s) -> PASS` at `origin/main`, versus
      `ERROR: stack.yaml: hermes.layers is missing or is not a list … / 1
      error(s), 4 warning(s) -> FAIL` on this branch. **PASS became FAIL, not
      silence** — which is the whole of the box.
- [x] 2.2 `scripts/validate-domain-factory.py`: delete the
      `if token.startswith("openworkflow")` branch (`:309-311`), leaving
      `elif token not in allowed` (`:312-314`) as the only arm — which means
      converting it to an `if`. Delete the docstring line at `:26`.
      **DONE.** The branch and the docstring line are gone and the `elif` is now
      an `if`. One line the packet did not name went with them, because leaving
      it would have made the file lie about itself: docstring check 3's *"Legacy
      flat keys are accepted with deprecation warnings."*, which 2.1 falsified.
      It is REPLACED (not deleted) by *"A stack that declares no hermes.layers
      list is an error: the legacy flat-key fallback read was removed at
      contract-v3.0."*
- [x] 2.3 Verify the widening at 2.2 rather than assuming it: a gate whose
      `owner_layer` normalizes to a DECLARED layer's display name and begins
      `openworkflow` validates silently after the change and warned before it.
      This is a real behaviour change and it goes in the Executed row.
      **VERIFIED, NOT ASSUMED — both directions, two validators side by side on
      the same probe repositories.** A gate whose `owner_layer` is
      `OpenWorkflow Domain Hermes`, matching a DECLARED domain layer's display
      name: at `origin/main`
      `WARN: workflows/probe.yaml: gate probe_gate owner_layer 'OpenWorkflow
      Domain Hermes' uses deprecated openWorkflow naming; use 'xfactory'` and
      `0 error(s), 4 warning(s) -> PASS`; on this branch no line at all and
      `0 error(s), 3 warning(s) -> PASS`. **That is the WIDENING.** The
      narrowing, on `openworkflowx` — the shape the entry never declared:
      at `origin/main` the same deprecation WARN and `PASS`; on this branch
      `ERROR: … owner_layer 'openworkflowx' does not resolve to a declared layer`
      and `FAIL`. Both are in the Executed row at 3.1.
- [x] 2.4 `scripts/apply-domain-starter.py`: delete the comment at `:241` and
      the nine emitted flat keys at `:242-250` from the `stack.yaml` template.
      **Do not touch `omnigent.domain_overlay` at `:253`** — same key name,
      different block, not deprecated, and read by the validator at
      `scripts/validate-domain-factory.py:539-541`, which errors when the
      directory it names is missing.
      **DONE — AND THE GENERATOR NAMED THE FLAT KEYS IN THREE PLACES, NOT ONE.**
      This is the one place the packet's line-scoped text did not survive
      contact with the tree, and it is reported rather than absorbed. The
      `stack.yaml` template (the box's `:241-250`) is done exactly as written,
      and `omnigent.domain_overlay` is untouched. But the SAME generator also
      writes two other artifacts into every new domain repository that named the
      same deprecated keys, and a realization that moved only the template would
      have shipped a generated repository that is self-contradicting on day one:
      (a) `schemas/stack.schema.yaml` listed six of them under `required_paths`
      — a generated schema REQUIRING paths the generated `stack.yaml` no longer
      carries; that list now reads `hermes.layers` plus the untouched
      `omnigent.domain_overlay`. (b) The generated local validator resolved
      overlay directories through six flat-key reads that would now always
      return `None` — dead checks; it resolves them from `hermes.layers`
      overlays instead, which preserves the coverage exactly (the three
      agent-mixes files it also read are already in that validator's
      `REQUIRED_FILES`). Both are the packet's own
      replacement-not-deletion principle applied one file over. Proven by
      `test_the_scaffolded_repo_does_not_REQUIRE_what_it_no_longer_writes`,
      which walks every `required_paths` entry of the freshly generated schema
      against the freshly generated `stack.yaml`.
      **AND (b) TOOK TWO PASSES, WHICH IS THE LESSON OF THIS BOX.** The first
      version resolved overlays from `hermes.layers or []` — correct for a
      list, and SILENT for a non-list, skipping every overlay check and
      reporting `OK` on a scaffold the canonical validator refuses. That is
      § 2.1's hazard reproduced by the fix for it, in a file § 2.1 does not
      name. Copilot caught it (round 3, PR #562) and the generated validator
      now ERRORS on the type before iterating, with
      `test_the_generated_validator_REFUSES_a_non_list_hermes_layers` driving
      all four non-list shapes through BOTH validators.
- [x] 2.5 Tests: the fallback branch has NO existing coverage (grep for
      `LEGACY_HERMES_KEYS` outside the validator returns nothing). The
      realization adds coverage for the post-removal behaviour in both
      directions — a `layers`-declaring stack unchanged, a `layers`-less stack
      refused, a co-resident stack still accepted with no new warning — plus the
      two `openworkflow` cases, plus a starter-output assertion that no
      deprecated flat key is emitted.
      **DONE — a new module,
      `tests/hermes_runtime_contracts/test_domain_factory_deprecation_retirements.py`,
      20 tests, all green**, each running the REAL validator or the REAL
      generator as a subprocess rather than asserting about them. Every case the
      box names is there and is named after what it measures: a
      `layers`-declaring stack unchanged; a `layers`-less stack REFUSED
      (`test_a_layers_less_stack_is_REFUSED_and_not_silently_widened`, which
      asserts `returncode == 1` precisely so a future bare deletion reds here
      rather than passing); all four non-list shapes — absent, `{}`, a string, an
      int — reaching the same refusal; a co-resident stack accepted with its
      findings compared to a flat-key-free baseline, so "no NEW warning" is
      measured rather than "no warning at all"; the four `openworkflow` tokens
      the code actually matched (`openworkflow_legacy`, `openworkflow`,
      `openworkflowx`, `openworkflow-legacy`) falling to the general rule; the
      resolvable-token WIDENING, whose findings are compared against a gate
      naming an ordinary declared layer and must be indistinguishable from it;
      `xfactory` unchanged; `omnigent.domain_overlay` still live and still
      required while a co-resident `hermes.domain_overlay` draws no finding — the
      by-PATH precision, held by a test; the two retired surfaces absent from
      the validator source, so neither can quietly return; and five assertions
      over a repository generated by the real starter.
- [x] 2.6 Run `python3 scripts/validate-domain-factory.py <repo>` against all
      five supported consumers from the candidate checkout and record the output.
      The expected result is that nothing changes for any of them; a changed
      line in any one of them is a finding about this retirement, not about that
      consumer.
      **DONE. NO LINE MOVED FOR ANY OF THE FIVE.** Run before and after the
      change from the candidate checkout, against fresh `--depth 1` clones:
      codexFactory `8152686`, MedxFactory `fcafcc0`, AdxFactory `79f85b7`,
      LedgerxFactory `38743cf`, OpsxFactory `ef60375`. Verdicts, identical on
      both sides: codexFactory `0 error(s), 0 warning(s) -> PASS`; MedxFactory,
      AdxFactory and LedgerxFactory `0 error(s), 1 warning(s) -> PASS` (the
      memory_gateway scaffold notice); OpsxFactory `3 error(s), 24 warning(s) ->
      FAIL`, its three errors pre-existing and none of them ours
      (`tenancy.isolation.subject_context='per_subject'`, and two
      `profile.id missing`).
      **NOT ONE of the five emitted a legacy-flat-key warning on either side** —
      which is the measurement the record-why half at 3.3 rests on, reproduced
      independently rather than carried from the memo.
      ONE HONEST QUALIFICATION, because a diff that is not byte-empty must be
      explained rather than rounded off: under the default hash seed the
      OpsxFactory output differed in the ORDER of two `identifier near-miss`
      warnings. That is pre-existing set-iteration nondeterminism in
      `check_cross_ids`, not a behaviour change — re-running the unmodified
      validator four times produces both orders, and with `PYTHONHASHSEED=0` the
      before and after outputs are byte-identical for all five.

## 3. Speckit F2 — the policy rows

**The record-why is HERE, and it is the mechanism's own section — not
`health/dispositions.yaml`, which lives at the aggregation root, suppresses
doc-health findings by path, and is unreachable by a consumer reading a pinned
policy document.**

**AND THE ROWS LAND HERE, BEFORE THE CUT, WHICH IS WHAT § 7.1 REQUIRES.** § 7.1
is written as *"§§ 2 and 3 merged on `main`"* and § 7.2 as the tag, in that
order, so the policy rows are part of the realization and not part of the cut.
The consequence is stated rather than left to be noticed: between this merge and
the `contract-v3.0` tag, the declared bundle is `contract-v2.5` and these rows
name `contract-v3.0` as the version the shapes were REMOVED at. That is a
forward declaration of the same kind the In Force entry
`add-binding-consumer-identity` already carries (*"DECLARED at contract-v2.4 and
CONSTRAINED at contract-v3.0"*), and it is why `contracts/CHANGELOG.md`'s
`contract-v3.0` entry is § 4.1's and NOT ticked here: the changelog row is the
cut's own record and would be a claim about a released bundle.

- [x] 3.1 `docs/contract-versioning-policy.md` § Deprecations Executed: add the
      `openworkflow`-prefixed token row, **with its declared shape CORRECTED to
      the prefix the code matches** — the entry and the validator docstring both
      write `openworkflow_`, the code writes
      `token.startswith("openworkflow")`, so `openworkflow`, `openworkflowx` and
      `openworkflow-legacy` are all refused and none is declared. Carry all six
      elements the one exemplar row
      establishes — the shape removed enumerated, REMOVED at `contract-v3.0`,
      `contract-v1.1` named as the release that served the warnings, the
      conformance-validator clause's discharge, the migration to `xfactory` with
      a reference a post-removal reader can still follow, and the closing
      `Deprecated at contract-v1.1, removed at contract-v3.0.` **Include the
      widening from 2.3**; a row that recorded only the narrowing would be
      accurate about the wrong half.
      **DONE.** All six elements present: the shape enumerated AS THE CODE
      MATCHED IT (the prefix with no trailing underscore, with
      `openworkflow`/`openworkflowx`/`openworkflow-legacy` named and the
      one-character correction stated as a correction rather than made
      silently); REMOVED at `contract-v3.0`; `contract-v1.1` named as the
      release that served the warnings; the conformance-validator clause
      discharged in the validator itself, with the pinned consumer's position
      stated; the migration to `xfactory` with `contracts/CHANGELOG.md`
      § `contract-v1.1` as the reference a post-removal reader can still follow;
      and the closing `Deprecated at contract-v1.1, removed at contract-v3.0.`
      **The row carries BOTH directions** — the narrowing AND the widening from
      2.3, each labelled, with the shadowing `if`/`elif` explained as the reason
      one removal moves two cases in opposite directions.
- [x] 3.2 § Deprecations Executed: add the `hermes` flat-key FALLBACK READ row,
      with the same six elements, scoped explicitly to the fallback read and NOT
      to the keys.
      **DONE**, and the scoping is in the row's own title (*"the READ, and not
      the keys"*) and in a paragraph that names the In Force entry the keys stay
      in, so the two sections cannot be read as contradicting each other. The
      conformance-validator element is discharged AS A REPLACEMENT — the row
      states why a bare deletion would have widened silently — and the migration
      element names the `hermes.layers` shape plus the schema that requires it.
- [x] 3.3 § Deprecations Currently In Force: REWRITE the `hermes` flat-key entry.
      It (a) enumerates the refusal list by PATH — the nine keys under `hermes:`
      that `LEGACY_HERMES_KEYS` carries, plus the three the starter emitted
      (`domain_agent_mixes`, `client_agent_mixes_template`,
      `customer_agent_mixes_template`), explicitly excluding
      `omnigent.domain_overlay`; (b) records the reason it stays, in the
      mechanism's vocabulary and with the measurement behind it — the warning
      fires only when `hermes.layers` is absent, all five supported consumers
      declare `layers`, so the co-resident shape has never produced a warning
      and refusing it would be an unphased narrowing; (c) names the deprecating
      minor it owes; and (d) restates the removal target as
      `contract-v4.0`, preserving the section's `removal target contract-vX.Y`
      formula so a target still parses from the bullet.
      **DONE, all four.** (a) The refusal list is a TABLE of twelve rows, each
      written as a PATH under `hermes:`, with a second column recording which of
      them the old entry named — five of twelve — so the under-declaration is
      visible rather than merely repaired; `omnigent.domain_overlay` is named as
      EXCLUDED, in its own paragraph, with the reason. (b) The reason it stays is
      the measurement from 2.6, restated with the command that reproduces it.
      (c) The deprecating minor it owes is stated as a checkable property — a
      minor in which the validator warns on the co-resident shape *whether or
      not* `hermes.layers` is present, written from the full twelve-key list.
      (d) The tail reads `Warned since contract-v1.1; removal target RESTATED to
      contract-v4.0 — …`, which keeps `contract-vX.Y` adjacent to the words
      `removal target` so a target still parses, and makes the restatement
      VISIBLE per `design.md`'s third form. The restate-again loop is written
      into the bullet.
- [x] 3.4 § Deprecations Currently In Force: remove the `openworkflow_` bullet in
      the same cut that adds its Executed row. An entry MUST NOT sit in both.
      **DONE, in the same commit as 3.1.** The section now holds three bullets:
      the rewritten `hermes` flat-KEY entry, the doxBench chat-turn v1 family
      (the sibling packet's subject, untouched here), and
      `add-binding-consumer-identity`.
- [x] 3.5 Repair the stale `:250-254` citations in the existing Executed row and
      in the `contract-v2.0` changelog entry — cite the heading (§ Change
      Classes, *Breaking (major)*) rather than a line range. The clause now sits
      at `:301-305` and moved once already.
      **DONE, both, and a THIRD occurrence is reported and deliberately NOT
      touched.** Repaired: the openxWallet Executed row's two citations (`:250-254`
      on the served-minor clause, `:253-254` on the conformance-validator clause)
      and `contracts/CHANGELOG.md` § `contract-v2.0`'s *"lines 250-254"*. NOT
      repaired: `docs/contract-versioning-policy.md`'s In Force entry for
      `add-binding-consumer-identity` carries a third `:250-254`, and it sits
      inside a QUOTED sentence of that change's own ratified prose. This box
      names two sites; editing a third change's ratified quotation to fix a
      citation is not this packet's to take, and silently rewriting a quote is
      worse than leaving a stale one. It is raised in the pull request instead,
      as amendment-lane material for whoever next touches that entry.

## 4. The `contract-v3.0` cut (a SEPARATE act, listed for completeness)

- [x] 4.1 `contracts/CHANGELOG.md`: the `contract-v3.0` BREAKING entry —
      migration note, and the Breaking clause's three preconditions each
      discharged and each checkable, on the `contract-v2.0` entry's pattern.
      **DONE.** The entry opens with an EVERY-ACT table written in both
      directions — the eight acts that land, and the one that named this major
      and did NOT — and discharges the Breaking clause's three preconditions in
      a per-removal table rather than in aggregate, because the three removals
      served their warnings at three different releases (`contract-v1.1`,
      `contract-v1.1`, `contract-v1.34`). Migration notes are per removal under
      § *What is removed*. The `contract-v2.0` pattern is followed and extended
      in one place: that entry could discharge the conformance-validator clause
      by relocating a family, and these three discharge it in the validator
      itself, one by REPLACEMENT (the flat-key read), one through the general
      rule (the token branch), one by the closed `oneOf` with the deprecation
      READER deliberately kept (the chat-turn family).
- [x] 4.2 `contracts/manifest.yaml`: `contract_bundle_version`, and
      `contract_schema_version` per OQ-2's answer at the cut.
      **DONE. `contract_bundle_version: contract-v3.0`, and OQ-2 IS ANSWERED BY
      MEASUREMENT: NO `contract_schema_version` moves at this major.**
      The contract SET's `contract_schema_version` does NOT move —
      `scripts/validate-domain-openxfactory-pins.py:92` hard-codes
      `"contract_schema_version": 1` as the value every domain `stack.yaml` must
      declare and ERRORS on any other, and all five supported consumers declare
      `1`, so moving it would ERROR the entire supported population at a major
      with no warning minor ever served. That is the same unphased-narrowing
      test § 3.3's restatement turns on, applied to the publisher's own field,
      and `contract-v2.0` (the only previous major) moved it none either. The
      manifest ROW's `schema_version` does not move, and neither does the one
      contract FILE whose shape narrowed —
      `contracts/schemas/xfactory-workbench-chat-turn.schema.yaml`, the sibling
      packet's subject. **THE CUT BUMPED THAT FILE TO 2 AND WAS REFUSED BY TWO
      TESTS THE SIBLING'S REALIZATION LANDED**, which assert `== 1` with the
      reasoning beside them; the answer was already in the tree, in executable
      form, and a cut does not overturn a ratified realization's reasoned
      decision. This packet's own two retirements move NO contract file at all:
      they are validator-and-generator removals, which is why the question had
      two sides and why the answer is stated as a measurement rather than a
      rule.
- [x] 4.3 `contracts/releases/contract-v3.0.digests.yaml`: the cut's inventory.
      **DONE**, built by the canonical
      `python3 scripts/validate-contract-release.py build --tag contract-v3.0`
      AFTER every other member of the cut and never hand-edited, per § Release
      Digest Inventory and § *What a red `verify-commit` at HEAD means*'s
      *"THE REMEDY IS A RELEASE CUT, NEVER A HAND-EDIT."*
- [x] 4.4 Follow § Bundle Realization Order exactly: allocate late, move every
      release surface atomically with the code, run every gate against the
      unchanged candidate, land the exact reviewed commit, publish the annotated
      tag, verify from an independently refreshed checkout.
      **STEPS 1–3 DONE AT THIS CUT; STEPS 4 AND 5 ARE POST-MERGE AND ARE NOT
      TICKED HERE.** Step 1: branched off `origin/main` at `bbbbeda9`, re-fetched
      immediately before the inventory build, and the number FRESH-COUNTED there
      (manifest read `contract-v2.6`, inventories through v2.6, published tags
      through v2.5 with no v2.6, `refs/tags/contract-v3.0` empty). Step 2: every
      release surface moved atomically in ONE candidate commit with the
      inventory built last. Step 3: gates run against that unchanged candidate.
      **STEP 4 IS THE STEP WHOSE OMISSION KILLED `contract-v2.6`** — a squash
      promotion creates a different commit and a different TREE, so every gate
      and `verify-commit` rerun on the promoted commit BEFORE any tag; step 5
      then publishes the annotated tag at that commit and verifies it from an
      independently refreshed checkout. Both are enumerated as post-merge steps
      in the cut's pull request, and § 7.2 stays open until they are performed.
- [x] 4.5 Decide OQ-1 at the cut: whether this packet and
      `retire-doxbench-chat-turn-v1` ride the same major. Either is legal.
      **DECIDED: BOTH, and the decision was made for the cut by the merges
      rather than chosen freely.** `a951be76` (#562) and `6856f502` (#564)
      merged in the same minute, 2026-09-01T19:43Z, so from that point any
      bundle declared on `main` carries BOTH narrowings whether it names them or
      not. A cut naming one would have under-declared its own refusal list,
      which is the defect § 3's refusal-list rule exists to prevent.

## 5. Post-cut verification

- [ ] 5.1 From a refreshed checkout at the tag, run the validator against all
      five supported consumers again. Expected: identical output to 2.6.
- [ ] 5.2 Instantiate a domain repository from the starter and assert its
      `stack.yaml` carries no deprecated flat key and no spent-target comment.

## 6. Rides along regardless of ratification

- [x] 6.1 File the `Owner layer constraint` canon/code severity divergence as its
      own openxFactory issue — promoted canon says an unresolvable `owner_layer`
      is a WARNING, `scripts/validate-domain-factory.py:312-314` has made it an
      ERROR since `493fb33d` (2026-07-03), six days before the requirement was
      promoted at `a1a2802b` (2026-07-09). D4 keeps it out of this packet's
      scope; the issue is what keeps it from being lost.
      **FILED: openxFactory issue #561**, "Owner layer constraint: promoted
      canon says WARNING, the shipped validator has ERRORED since six days
      before the requirement was promoted". It carries both texts verbatim, both
      commits, why D4 keeps it out of scope, and what a disposition owes —
      including a measurement across the five supported consumers BEFORE the
      ruling, since if any of them carries an unresolvable `owner_layer` today
      the choice refuses somebody and owes its own phasing. It also records that
      the retirement's Breaking class does not depend on the answer, which is
      why 3.1's Executed row states the fall-through's severity as *"whatever
      the general rule carries"* — so #561 can move it without reopening the row.
      Late relative to the box's *"at proposal time"*: the proposal landed at
      `59eb913e` and this was filed with the realization. Recorded as a fact
      rather than smoothed over.

## 7. Archive gate

**This change has a CODE SURFACE, so under `release-realization` it archives
ONLY on merged plus green realization evidence — never on landing.** The
evidence set:

- [ ] 7.1 §§ 2 and 3 merged on `openxFactory` `main`, `pytest-suite` green on
      the merge commit.
- [ ] 7.2 The `contract-v3.0` bundle declared, and its annotated tag PUBLISHED
      and verified from an independently refreshed checkout — a bundle is not
      published until its tag exists, and this packet's target release is that
      bundle.
- [ ] 7.3 `OPENSPEC_TELEMETRY=0 openspec validate --all --strict` green.
- [ ] 7.4 The five-consumer validator run of 5.1 recorded, showing no line moved.
