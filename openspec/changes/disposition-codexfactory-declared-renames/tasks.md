# Tasks: disposition-codexfactory-declared-renames

Status: draft

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a run recorded verbatim in
`evidence/codexfactory-dispositions-2026-09-05.md`. Group 5 is OWED work that
belongs to OTHER packets and is deliberately unticked, each box naming whose it
is — or, for 5.5, saying plainly that nobody owns it yet. **5.4 IS THE ONE
EXCEPTION AND IT IS TICKED**: ratification was this packet's own to receive, it
was received on 2026-09-05, and its record is a diff in this pull request.

**RATIFICATION HAS NOT HAPPENED.** Brett Heap ruled *"use recommended name, go
on 3 repo shape"* on 2026-09-05, deciding that codexFactory takes the same exit
openxFactory took and in what order. That settles the substance and does not
ratify this text; task 5.4 records ratification when it happens.

---

## 1. The two entries, quoted rather than paraphrased

- [x] 1.1 (2026-09-05) The findings were produced, not transcribed from a
      report someone else ran: `python3 scripts/validate-openspec-cli-pin.py
      --all --repo <codexFactory@b2a6af34>` at `1.12.0`, exit 1 before the edit,
      `Totals: 23 passed, 2 failed (25 items)`. Both messages are copied WHOLE
      from that run's own output into `finding:`, which is what the matcher
      compares after whitespace normalization.
- [x] 1.2 (2026-09-05) `contracts/openspec-cli-pin.yaml` gains two entries, both
      `repo: codexFactory`, each with `item:`, `path:`, `level: ERROR`, the
      whole finding text, a `why:` that says what the retitle did, a non-empty
      `cited_to:` (6 and 7 citations) and
      `ratified_by: 'Brett Heap, 2026-09-05, "use recommended name, go on 3 repo shape"'`.
- [x] 1.3 (2026-09-05) Each `retires_when:` names the archive of ITS OWN
      codexFactory change, says which tree refuses on that day
      (codexFactory's `--all`, `pin-disposition-stale`), and says why it is not
      near — both changes carry `Status: draft` and their ratification is
      Brett's, unscheduled.
- [x] 1.4 (2026-09-05) Nothing else in the pin moved: `version`, `integrity`,
      `shasum`, `tarball`, `rollback:`, `binary:`, `verify_pin:`,
      `consumer_entrypoint:`, `pinned_invocation:` and `resync_runbook:` are
      byte-identical.

## 2. The pin's prose made true again

- [x] 2.1 (2026-09-05) "THE TWO DISPOSITIONS" → "THE DISPOSITIONS"; the
      re-measurement sentence now says the two remaining openxFactory findings
      are "the two openxFactory-scoped DISPOSITIONS below".
- [x] 2.2 (2026-09-05) A new header paragraph records how the second pair
      arrived — codexFactory's measurement, PR #216's marker conversion, Brett's
      ruling — and states that the four entries are two pairs that never mix.
- [x] 2.3 (2026-09-05) The rollback note's "two entries below" → "four", with
      the consequence stated: a rollback un-raises the findings in BOTH
      repositories at once, so it deletes all four with the version.
- [x] 2.4 (2026-09-05) The block above `dispositions:` no longer says "BOTH
      ENTRIES BELOW"; it names the two pairs, their two rulings, and that each
      pair is out of scope on the other's tree.

## 3. The tests, tightened rather than renumbered

- [x] 3.1 (2026-09-05) The count-pinning test moves 2 → 4 and now asserts the
      per-repository SPLIT — `(repo, item, path)` triples in order — instead of
      `{repo} == {"openxFactory"}`, which a growing fleet would loosen once and
      then forever. Renamed to say what it pins.
- [x] 3.2 (2026-09-05) New test
      `test_the_consumers_entries_are_out_of_scope_on_this_repositorys_own_tree`
      reconciles the REAL pin at identity `openxFactory` over the captured real
      1.12.0 report and asserts the codexFactory pair is in neither `applied`
      nor `stale` — the property that keeps this repository's own required gate
      green.
- [x] 3.3 (2026-09-05) `python3 -m pytest tests/openspec_cli_pin
      tests/sequenced_after -q` green; verbatim in the evidence file.

## 4. The runs, both directions

- [x] 4.1 (2026-09-05) BEFORE, on codexFactory's tree: exit 1, two
      UNDISPOSITIONED failures named. Recorded so the after-run is a change and
      not a coincidence.
- [x] 4.2 (2026-09-05) AFTER, on codexFactory's tree: exit 0,
      `Totals: 23 passed, 2 failed (25 items)`, `DISPOSITIONED FINDINGS in
      codexFactory (2 applied)`, and the honest trailer `THIS IS NOT A CLEAN
      TREE`. No `pin-disposition-stale` over openxFactory's pair.
- [x] 4.3 (2026-09-05) AFTER, on openxFactory's own tree — the gate's literal
      invocation, `--all --no-cache`: exit 0, its own two applied, the
      codexFactory pair neither applied nor stale.
- [x] 4.4 (2026-09-05) The pinned CLI validates THIS packet `--strict` with
      `skip_specs: true` and no `specs/` directory.

## 5. Owed, and not this packet's to tick

- [ ] 5.1 **Step 3 — `adopt-openspec-cli-pin-gate` in codexFactory**: the gate
      leg that runs `scripts/validate-openspec-cli-pin.py --all` in codexFactory
      CI. Not here; it belongs in codexFactory and cannot land before this
      change merges. **DONE 2026-09-06, codexFactory #227
      `adopt-openspec-cli-pin-gate` (`bb66d85c`).** Landed in codexFactory's
      own pull request, not this one, so this box stays UNTICKED under this
      file's own rule; recorded as ticked at `add-openspec-cli-pin` task 6.1.
- [ ] 5.2 **codexFactory's `stack.yaml` re-pin** to an openxFactory commit AT OR
      AFTER this change's merge. An earlier pin resolves a pin file without
      these two entries and the gate fails on its first run. Step 3's job.
      **DONE 2026-09-06, same pull request (codexFactory #227,
      `bb66d85c`):** `stack.yaml`'s `xfactory.contract_ref` moved to
      `724a2a4f` — this change's own merge commit, AT it rather than merely
      after. Landed in codexFactory's own pull request, so this box stays
      UNTICKED under this file's own rule.
- [ ] 5.3 **Task 6.1 of `add-openspec-cli-pin` and task 6.3 of
      `bump-openspec-cli-pin-to-1.12` stay UNTICKED.** They describe the WIRING,
      which is step 3. A tick that ran ahead of the act is the thing this estate
      refuses everywhere else.
- [x] 5.4 (2026-09-05) **Ratified.** Brett Heap, first-hand to this lane,
      verbatim **"ratify 697"**, given against head `bfc9451e` after every
      required check went green on it. `proposal.md` moves to
      `Status: ratified` with a `Ratified:` line, the draft-time paragraph kept
      under a dated note, and the record is
      `review/ratification-2026-09-05.md` — a diff in this pull request, which
      is what lets this box be ticked under the rule at the top of this file.
      **THE MERGE IS A SEPARATE WORD AND HAS NOT BEEN GIVEN.** The record says
      so, and says what this ratification does not cover.
- [ ] 5.5 **Watch exit 3 — `Fission-AI/OpenSpec#1793`, WHICH IS FILED.** It was
      filed 2026-09-05 on Brett Heap's word *"file the upstream issue"*, under
      his GitHub account by lane `codexfactory-0d`, and openxFactory #682
      (`ff31fc7f`) corrected #677's draft record from NOT FILED to FILED:
      *"`validate --strict`: scenario-currency check has no way to declare a
      deliberate scenario rename, so a narrowing reads as an omission"*. **This
      box is not the filing** — that is done, by another lane, and this packet
      does not tick another packet's act. It is the WATCH: if upstream lands a
      way to declare a rename, the next pin bump re-derives the list against the
      fixed release, ALL FOUR entries — openxFactory's two and codexFactory's
      two — are matched by no finding, and the pin REFUSES
      `pin-disposition-stale` until every one is deleted. That refusal is the
      INTENDED RETIREMENT PATH and not a regression, and nobody owns noticing it
      yet.
