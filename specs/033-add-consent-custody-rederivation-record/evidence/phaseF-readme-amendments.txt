PHASE F — Q8's README amendments (T055-T059). 2026-09-09.

WHAT WAS WRITTEN, and where. Two amendment blocks, both in the `3b530009` form
— superseded sentence block-quoted in place, never deleted; un-superseded
neighbour NAMED and re-verified; marker `AMENDED 2026-09-09`.

  T056  README.md, this packet's own OpenSpec Records row (the row runs
        847-944 before the amendment; the block is appended at its end).
        Superseded: "RATIFICATION PERFORMS NO REALIZATION — no schema byte
        moves, no contract version is cut, no consumer file is edited, and all
        46 boxes in `tasks.md` stay unticked."
        Neighbour NAMED and left standing: "no consumer file is edited".
        Substrate: this packet's standing row-3 claim 5571680388 (2026-09-07),
        plus the lane's row-3 note 5603344475 (2026-09-09), both cited inline.

  T057  README.md, the `govern-archived-record-edits` row, the F.1
        disposition's parenthesis (pre-amendment lines 3022-3024).
        Superseded in its FIRST CLAUSE ONLY: "that packet is a ratified
        PROPOSAL with all 46 boxes unticked".
        Neighbour NAMED and left standing: "the three pins are still broken",
        and "discharged" would still overclaim. F.1 stays ADDRESSED.

  T058  README.md, the same row, the TRANSITION CLAUSE'S OWN PREMISE
        (pre-amendment lines 2991-2993): "the consent family's is PROPOSED only
        (`contract_schema_version: 2`, no `custody_rederivations` property,
        `contract-v3.4`, 46/46 boxes unticked)" — false on all four counts.
        Neighbour NAMED and left standing: the register home
        `models/content-address-families.yaml` exists on neither side.

  T059  RECORDED, NOT EDITED. The past-tense "left its 46" and the dated
        "measured 2026-09-09 UTC at `main` `6cc06288`" are TRUE-WHEN-WRITTEN
        and are left byte-unchanged; the decision and its reasoning are written
        into the T057/T058 block. A dated measurement is not falsified by a
        later act.

T057, T058 and T059 are THREE EDITS TO ONE ROW, so they are carried by ONE
appended block rather than three (panel F9), and the substrate note covers the
row once.

TWO CLAIMS WERE RE-MEASURED RATHER THAN ASSUMED, which is what "re-verified"
has to mean if the form is to be worth anything:
  * "no consumer file is edited" — the whole realization diff is inspected for
    an OpsxFactory path and contains none; the two repositories are separate
    and nothing here reaches across.
  * "the register home exists neither on OpsxFactory's `main` nor on the branch
    proposing it" — a read-only API fetch of
    `repos/opensoft/OpsxFactory/contents/models/content-address-families.yaml`
    returns **404** at the default branch, 2026-09-09. The amendment states the
    measurement it made rather than restating the whole claim as verified.

A COORDINATE THAT MOVES IS NOT AN IDENTIFIER. The amendment inserts lines above
the sentences it cites, so the line numbers it quotes are labelled as
PRE-AMENDMENT and the sentences are identified by their quoted words.

GATES, raw with return codes:
$ python3 -m pytest tests/doc-health tests/sequenced_after tests/scope_globs -q -m "not postgres"
1955 passed, 7 warnings in 368.73s (0:06:08)
rc=0
$ python3 scripts/validate-openspec-cli-pin.py --change add-consent-custody-rederivation-record --strict
Totals: 1 passed, 0 failed (1 items)
rc=0
$ python3 scripts/validate-sequenced-after.py .
archive-date agreement passed; archive-date-vs-commit agreement passed (12 dispositions in force)
rc=0
$ python3 scripts/validate-sequenced-after.py . --ledger-diff
per-change sweep ledger consistent with the corpus (189 rows).
rc=0
