# Tasks: disposition-codexfactory-floor-relocation-retitle

Status: ratified
Ratified by: disposition-codexfactory-floor-relocation-retitle — 2026-09-10, Brett Heap, "go A, ratify the disposition entry as encoded" (record `review/ratification-2026-09-10.md`)
Kind: tasks

**NOTHING IS TICKED THAT DID NOT LAND.** Every ticked box below is a diff in
this pull request or a run recorded verbatim in
`evidence/codexfactory-floor-relocation-2026-09-10.md`. Group 5 is OWED work
that belongs to OTHER repositories and OTHER packets, and is deliberately
unticked, each box naming whose it is.

**RATIFICATION HAPPENED BEFORE THIS FILE WAS WRITTEN, WHICH IS WHY 5.4 IS
TICKED AND THE HEADER SAYS `ratified`.** Brett Heap's word of 2026-09-10,
verbatim *"go A, ratify the disposition entry as encoded"*, carried both the
exit and the ratification of this text in one sentence. The merge is a further,
separate act and is NOT ticked anywhere in this file.

---

## 1. The entry, quoted rather than paraphrased

- [x] 1.1 (2026-09-10) The finding was PRODUCED, not transcribed from a report
      someone else ran: `python3 scripts/validate-openspec-cli-pin.py --all
      --repo <codexFactory@32743fb7>` at `1.12.0`, exit 1 before the edit,
      `Totals: 26 passed, 3 failed (29 items)`. The message is copied WHOLE
      from that run's own output into `finding:`, which is what the matcher
      compares after whitespace normalization.
- [x] 1.2 (2026-09-10) `contracts/openspec-cli-pin.yaml` gains ONE entry,
      `repo: codexFactory`, with `item: relocate-review-authority-floor`,
      `path: repository-gate-floor/spec.md`, `level: ERROR`, the whole finding
      text, a `why:` that says what the retitle did and what restoring the old
      title would reinstate, a non-empty `cited_to:` (8 citations) and
      `ratified_by: 'Brett Heap, 2026-09-10, "go A, ratify the disposition
      entry as encoded"'` carrying the recording comment's URL.
- [x] 1.3 (2026-09-10) `retires_when:` names the archive of the codexFactory
      change, says which tree refuses on that day (codexFactory's `--all`,
      `pin-disposition-stale`), and says why it is not near — the change is
      ratified but ACTIVE and its archive is Brett's, unscheduled.
- [x] 1.4 (2026-09-10) Nothing else in the pin moved: `package`,
      `source_repository`, `version`, `revision_kind`, `integrity`, `shasum`,
      `tarball`, `lockfile`, `lockfile_integrity`, `lockfile_packages`,
      `rollback:`, `binary:`, `verify_pin:`, `consumer_entrypoint:`,
      `pinned_invocation:` and `resync_runbook:` are byte-identical, and NO
      existing `dispositions[]` entry is edited.

## 2. The pin's prose made true again

- [x] 2.1 (2026-09-10) "THE FOUR ENTRIES ARE TWO PAIRS AND THEY NEVER MIX"
      becomes a statement about GROUPS rather than a count, so the sentence
      stays true as the list grows.
- [x] 2.2 (2026-09-10) The 2026-09-05 narrative's "WHY THE LIST IS NOW FOUR AND
      NOT TWO" becomes "WHY THE LIST WENT FROM TWO TO FOUR": a dated record
      now reads as one instead of claiming a present count it no longer has.
- [x] 2.3 (2026-09-10) A NEW dated paragraph records how the third codexFactory
      finding arrived — the #318 archive, the promotion it performed, the
      retitle it made visible, the measured totals, and Brett's word.
- [x] 2.4 (2026-09-10) The rollback note's "four entries below" becomes "five",
      and the block above `dispositions:` says five findings in TWO GROUPS —
      two openxFactory, three codexFactory — naming each group's ruling.
- [x] 2.5 (2026-09-10) The 2026-09-05 comment block above the first
      codexFactory pair is left UNEDITED. It is that change's dated record of
      what arrived that day and stays true of those two entries.

## 3. The tests, tightened rather than renumbered

- [x] 3.1 (2026-09-10) The count-pinning test moves 4 -> 5, KEEPING the
      per-repository split (`(repo, item, path)` triples in order) the
      precedent tightened it into, and is renamed to say what it now pins.
- [x] 3.2 (2026-09-10) `test_every_real_disposition_cites_canon_and_names_who_
      granted_it` is TIGHTENED from two shared literals to PER-ITEM maps: the
      measurement each entry rests on, and the authority date its word carries.
      A sixth entry fires it again. `design.md` § 4 records why loosening was
      refused.
- [x] 3.3 (2026-09-10) `python3 -m pytest tests/openspec_cli_pin
      tests/pin_registrations tests/sequenced_after -q` green; verbatim in the
      evidence file.

## 4. The runs, both directions

- [x] 4.1 (2026-09-10) BEFORE, on codexFactory's #318 tree: exit 1, ONE
      UNDISPOSITIONED failure named, the standing pair APPLIED. Recorded so the
      after-run is a change and not a coincidence.
- [x] 4.2 (2026-09-10) AFTER, on codexFactory's #318 tree: exit 0,
      `Totals: 26 passed, 3 failed (29 items)` UNCHANGED, `DISPOSITIONED
      FINDINGS in codexFactory (3 applied)`, and the honest trailer `THIS IS
      NOT A CLEAN TREE`.
- [x] 4.3 (2026-09-10) On codexFactory `main`: the new entry is **STALE and the
      run REFUSES** `pin-disposition-stale` (exit 2) — measured, not assumed,
      and NOT the "neither applied nor stale" an earlier draft of this box
      claimed. The entry is IN SCOPE there (the repository is codexFactory) and
      in scope with no matching finding is the definition of stale; the pinned
      CLI reports the item `"valid": true` with an INFO on `main` and
      `"valid": false` with an ERROR on #318's merged tree, and only a BLOCKING
      finding is reconciled. This is the live coupling of evidence § 3/§ 3b and
      it fixes an ORDER — #318 first, codexFactory's pin advance second — not a
      defect in this entry.
- [x] 4.4 (2026-09-10) AFTER, on openxFactory's own tree — the gate's literal
      invocation, `--all --no-cache`: exit 0, its own two applied, all three
      codexFactory entries neither applied nor stale.
- [x] 4.5 (2026-09-10) The pinned CLI validates THIS packet `--strict` with
      `skip_specs: true` and no `specs/` directory.
- [x] 4.6 (2026-09-10) **THE MARKER'S IRRELEVANCE TO THE TOOL, FALSIFIED AND
      SURVIVED.** codexFactory PR #339 landed the reserved `Merged into` marker
      mid-authoring (main `9b1b0a21`), so the claim was re-run rather than
      argued: over #318's head merged with that main (`89ee5e84`), the finding
      is BYTE-IDENTICAL to the pre-marker run, the pre-edit pin still exits 1
      with it UNDISPOSITIONED, and this pin exits 0 with `Totals: 27 passed,
      3 failed (30 items)` and 3 applied. The entry's recorded `finding:` also
      normalizes EQUAL to the measured message, checked in code.
- [x] 4.7 (2026-09-10) **THE WHOLE PAIR RE-TAKEN AT COMMIT TIME, BECAUSE `main`
      MOVED AGAIN.** A second author in this lane re-ran all four measurements
      against codexFactory `main` `2e744d4b` and #318's head merged with THAT
      main (`8effa57a`, one declared `README.md` conflict resolved `--ours`,
      nothing under `openspec/` conflicting): merged tree, pre-edit pin →
      exit 1 UNDISPOSITIONED; merged tree, this pin, in the gate's own CI form
      `--repo … --all --no-cache` → exit 0, `Totals: 26 passed, 3 failed
      (29 items)`, 3 applied, 0 undispositioned; `main`, pre-edit pin → exit 0;
      `main`, this pin → exit 2 `REFUSE pin-disposition-stale`. The `cited to:`
      line printed by the AFTER run is the line the COMMITTED pin renders, so
      the transcript in evidence § 2/§ 3b and the YAML are the same text — the
      one check a re-worded citation would have failed.

## 5. Owed, and not this packet's to tick

- [ ] 5.1 **codexFactory's declared openxFactory pin advances** to a commit AT
      OR AFTER this change's merge. An earlier pin resolves a pin file without
      this entry and codexFactory `validate` stays red on #318's tree. It is
      codexFactory's act, in codexFactory's own pull request, coordinated on
      codexFactory #333 (`change/advance-openxfactory-pin-b91af6ea`), which as
      it stands targets `b91af6ea` — BEFORE this change — so a further advance
      is owed. **AND THE ORDER IS FIXED BY MEASUREMENT**: the advance must
      follow codexFactory PR #318's merge, or codexFactory `main` refuses
      `pin-disposition-stale` on this entry (evidence § 3).
- [ ] 5.2 **The reserved `Merged into` marker on the relocate block.**
      **DONE 2026-09-10T14:33:55Z — codexFactory PR #339 → main `9b1b0a21`**, at
      `openspec/changes/relocate-review-authority-floor/specs/repository-gate-floor/spec.md:15`,
      dated note at that packet's `tasks.md:384`. Landed in codexFactory's own
      pull request, not this one, so this box stays UNTICKED under this file's
      own rule. The disposition was lawful without it and cites it at its path;
      the marker is what puts the declaration where a reader of that block
      looks. **And it changed nothing about the tool, measured** — box 4.6.
- [ ] 5.3 **codexFactory #318's archive going green** is a codexFactory
      verdict, not this one. This packet removes ONE of the reasons its
      `validate` is red and claims nothing about the others.
- [x] 5.4 (2026-09-10) **Ratified.** Brett Heap, first-hand to lane
      `openxfactory-2`, verbatim **"go A, ratify the disposition entry as
      encoded"**, recorded on openxFactory #745 (comment 5619833296) and
      codexFactory #232 (comment 5619832944). Record at
      `review/ratification-2026-09-10.md` — a diff in this pull request, which
      is what lets this box be ticked under the rule at the top of this file.
      **THE MERGE IS A SEPARATE ACT AND IS NOT COVERED BY THIS WORD.**
- [ ] 5.5 **Watch `Fission-AI/OpenSpec#1793`** — filed 2026-09-05, NOT fixed.
      If a release honours a declared rename, the next pin bump re-derives the
      list against it, ALL FIVE entries match nothing, and the pin REFUSES
      `pin-disposition-stale` until every one is deleted. That refusal is the
      INTENDED RETIREMENT PATH and not a regression. Nobody owns noticing it
      yet; this box says so, exactly as the precedent's 5.5 does, and does not
      claim the precedent's box as discharged.
