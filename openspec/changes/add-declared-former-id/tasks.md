# Tasks: add-declared-former-id

Status: ratified
Ratified by: add-declared-former-id — 2026-09-13T22:48Z, Brett Heap, verbatim "ratify 1028 as encoded" (record `review/ratification-2026-09-13.md`)

**AMENDED 2026-09-14 AT THE FIRST REALIZATION LANDING AND AGAIN 2026-09-15 AT
THE LAST: EVERY BOX IN §§ 2, 3, 4 AND 5 IS NOW TICKED EXCEPT § 4.5, AND
§ 5.3/§ 5.4 ARE PERFORMED BY THE PULL REQUEST THIS AMENDMENT RIDES IN.**
`design.md` D7's six slices, each with its merge sha:

* slices 1, 2 and 3 — PR **#1038**, merge **`701c8fde`** (2026-09-14T21:09:31Z):
  the declaration and its reader (§ 2.1, 2.2, 2.3, 2.5, 2.6), the archive
  gate's baseline resolution (§ 3.1, 3.1a, 3.2, 3.3) and the fail-closed reads
  behind it (§ 3.4);
* slice 5 — PR **#1037**, merge **`8f393758`** (2026-09-15T19:02:27Z): the
  reference resolver and the named consumer it was built for (§ 5.0, 5.1, 5.1a,
  5.2, 5.2a);
* slice 4 — PR **#1039**, merge **`92d519b0`** (2026-09-15T19:15:01Z): the
  landing validator (§ 2.4 — the one § 2 task that reads a COMMIT RANGE and
  therefore belongs here rather than to the declaration's reader — and § 4.1,
  4.2, 4.2a, 4.2b, 4.2c, 4.3, 4.4);
* slice 6 — the documents and these ticks, the pull request this amendment
  rides in (§ 5.3, § 5.4).

The evidence sits under each box and it is a FACT THAT SURVIVES THE SESSION —
a merged commit, a merge sha, a reader named, a fixture named — never an
intention and never a workflow file standing in for a ruleset state.

**WHAT IS STILL OPEN, AND WHOSE ACT EACH ONE IS. § 4.5 IS BRETT HEAP'S
OPERATOR ACT AND IS OUTSTANDING**, re-measured live at 2026-09-15T19:41Z and
written under the box; § 6 is residue taken nowhere, § 6.1's successor filed
after this pull request lands (**Q5 RULED**, verbatim *"File it after #1041
lands"*); and § 7 is the archive and the closing of #1003, which Brett Heap
ruled may proceed with § 4.5 open, as a disposition plus a carry-forward issue
(**Q2 RULED**, verbatim *"Yes, with disposition + carry-forward issue"*). Each
is written under its own box with the ruling's recording URL.
**WHAT THIS AMENDMENT TOUCHED, AND NOTHING ELSE: the boxes, the dispositions
beneath them, and this header.** The paragraph below is left exactly as the
ratification landing wrote it, because
it was true when written and its point was that it was true then; read it as
the state at PR #1028 and the ticks as the record of what has happened since.

**§ 1 IS TICKED AND NOTHING ELSE IS, AND THAT IS THE STATE OF THE WORK RATHER
THAN AN OVERSIGHT.** This pull request filed a proposal and now carries its
ratification. It still edits no file under `openspec/specs/`, adds no script,
no validator, no register and no test, and changes no behaviour of anything
that runs. § 1 was decided by a ratification act that has now happened —
Brett Heap, 2026-09-13T22:48Z, verbatim "ratify 1028 as encoded"; § 2 through
§ 5 are realization slices that follow it and stay entirely open, § 6 is
residue taken nowhere, and § 7 (archive) is held behind merged-plus-green
realization evidence and a further word.

## 1. Ratification — GIVEN 2026-09-13, Brett Heap's and nobody else's

- [x] 1.1 **RULE `design.md` D1 — where the declaration lives.** Recommended:
      a top-level `former_ids:` key in the packet's own `.openspec.yaml`, a
      SIBLING of `origin:` and never a member of it. The alternatives and their
      costs are written out in D1; option (c), an estate-level register in the
      shape of `contracts/policies/repository-identity.yaml`, is the one a
      reader is most likely to prefer and the reasons it is not taken are
      stated there. **RULED (a)** — Brett Heap, 2026-09-13T22:48Z, verbatim
      "ratify 1028 as encoded" (`proposal.md` § Rulings;
      `review/ratification-2026-09-13.md`).
- [x] 1.2 **RULE `design.md` D2 — the declaration names change IDS, not paths**,
      ordered oldest first and appended to rather than rewritten. **RULED (a)**
      on the same word; the path is DERIVED from the id, which is how this
      estate already addresses a packet.
- [x] 1.3 **RULE `design.md` D3 — the fail-closed refusal is taken by a house
      validator at the landing**, not by the archive gate and not as a
      `doc-health` finding, with the two refusal statuses, the two arms and the
      archive-relocation exception as D3 states them. **RULED (a)** on the same
      word; the validator is a § 4 realization slice and is built nowhere here.
- [x] 1.4 **RULE `design.md` D4 — no `doc-health` delta in this packet**, the
      reporting sweep being a successor with its own numeral. A veto here adds
      a `## MODIFIED Requirements` block over *Deterministic check families*
      and a registry edit, and D4 prices both. **RULED (a)** on the same word;
      no veto was taken, so no such block exists in this packet and § 6.1
      keeps the successor's figures.
- [x] 1.5 **RULE `design.md` D5 — *Origin retention at archive* is MODIFIED**
      rather than left standing beside an ADDED requirement that contradicts it.
      **RULED (a)** on the same word; the MODIFIED block stands exactly as
      frozen at `1e57643d`, every promoted sentence and all three promoted
      scenarios carried verbatim.
- [x] 1.6 **RATIFY THE TEXT, OR NAME WHAT MOVES.** Ratification is Brett Heap's
      word and is a separate act from this landing. The record is a
      `review/ratification-<date>.md` carrying the verbatim word and its
      recording URL, and `.openspec.yaml` then takes `approved_by` and
      `approved_on` ADDED BESIDE the drafting provenance, `kind` and `id`
      unmoved. **DONE in the ratification commit**: the text is ratified AS
      ENCODED and NOTHING MOVES — `git diff --stat` over
      `openspec/changes/add-declared-former-id/specs/` across that commit is
      empty (0 files). `Status: draft` → `Status: ratified` on `proposal.md`,
      `design.md` and this file, one citation line each; `design.md`'s five
      `## D1 … D5` headers each gained an inline `— RULED (a),
      2026-09-13T22:48Z` marker and no other byte of that file moved; the
      record is `review/ratification-2026-09-13.md` (`Status: ratified`),
      carrying the word verbatim and its recording URL; `.openspec.yaml` gained
      `approved_by` + `approved_on` beside an unmoved `kind`, `id`, `reason`,
      `proposed_by` and `proposed_on`. The instant is written `22:48Z`, the
      precision the word was taken at, never invented finer.

## 2. The declaration and its reader — REALIZATION

- [x] 2.1 **WRITE THE GRAMMAR.** `former_ids:` — a top-level sequence of change
      ids in `openspec/changes/<id>/.openspec.yaml`, oldest first. Refuse: a
      scalar where a sequence is required; an entry that is not a change id by
      the grammar `ratifying_commit` already enforces
      (`[A-Za-z0-9][A-Za-z0-9._-]*`); an entry equal to the packet's own id; a
      duplicate entry; an entry nested inside `origin:` rather than beside it.
      **BUILT** — `former_id_problems` in `scripts/proposal-support.py`, with
      `declared_former_ids` / `declared_former_ids_of` / `load_packet_at`
      beside it; commit `59232b37`, landed in PR #1038 at merge `701c8fde`.
      Every refusal has a fixture in `DeclaredFormerIdTests`
      (`tests/proposal-support/test_proposal_support.py`):
      `test_a_scalar_where_a_sequence_is_required_refuses`,
      `test_a_mapping_where_a_sequence_is_required_refuses`,
      `test_an_entry_that_is_not_a_change_id_refuses`,
      `test_an_entry_that_is_not_a_string_refuses`,
      `test_an_entry_equal_to_the_packets_own_id_refuses`,
      `test_a_duplicate_entry_refuses`,
      `test_a_declaration_nested_inside_origin_refuses`, and
      `test_every_problem_is_reported_rather_than_the_first`. A SEVENTH
      refusal the bench added on the same pull request:
      `test_an_entry_naming_the_reserved_archive_segment_refuses` (commit
      `30d40c1c` — `archive` is the one slug under `openspec/changes/` that
      is not a packet id). A malformed declaration RAISES rather than reading
      short (`test_a_malformed_declaration_raises_rather_than_reading_short`,
      `test_a_missing_yaml_parser_is_not_an_absent_declaration`).
- [x] 2.2 **PIN THE SIBLING PROPERTY WITH A TEST**, not with a comment: a
      `.openspec.yaml` carrying `former_ids:` must yield an
      `origin_block_lines` reading identical to the same file without it, so a
      lawful move is never a mutation of the frozen origin declaration. The
      authoring measurement is `design.md` M3; the test is what keeps it true.
      **PINNED BY A TEST AND NOT BY A COMMENT** —
      `test_the_declaration_is_outside_the_frozen_origin_block` and
      `test_a_declaration_before_the_origin_block_is_still_outside_it` compare
      `origin_block_lines` for a `.openspec.yaml` carrying `former_ids:`
      against the same file without it, above the block and below it, and
      require the two readings to be identical. Commit `59232b37`, merge
      `701c8fde`.
- [x] 2.3 **REFUSE A DECLARED ID THAT STILL STANDS.** A former id carried by a
      live packet directory at the commit that declared it is a claim to be the
      move of something that did not move; refuse naming both ids.
      **BUILT** — `standing_former_id_problems`, commit `59232b37`, merge
      `701c8fde`; fixtures
      `test_a_declared_former_id_that_still_stands_refuses_naming_both` and
      `test_a_declared_former_id_with_no_live_directory_passes`. **ITS
      PRODUCTION CALLER LANDED WITH SLICE 4**, `scripts/former_id_arrival.py`'s
      corpus arm (PR #1039, merge `92d519b0`, 2026-09-15T19:15:01Z): on `main`
      today this reader IS called by that arm, on every pull request, through
      `.github/workflows/former-id-arrival-gate.yml`. **WHAT IS STILL PENDING
      IS ONLY § 4.5** — the branch-rule registration that would make the
      call's refusal block a merge — so the call runs and a refusal is
      reported today, but enforces nothing until that registration happens;
      this distinction is stated here rather than left for a reader to
      discover.
- [x] 2.4 **BIND EVERY NEWLY ADDED ENTRY TO THE MOVE THAT COMMIT PERFORMS.**
      Absence of a live directory is NOT proof of predecessorship — an archived
      id and an id that never existed both lack one — so the entry a commit adds
      must be exactly the source of the move that commit performs, and a commit
      that adds a former id while moving nothing into this packet is refused.
      Fixtures: a standing packet appending an archived id; a standing packet
      appending an id that never existed.
      **BUILT** — `_declaration_findings` in `scripts/former_id_arrival.py`
      reads the destination packet's list at the commit against the list it
      carried at the commit's PARENT and hands every entry that commit ADDS to
      `_bound_entry_finding`, which refuses unless that same commit performs a
      move into the packet FROM exactly that id; commit `00a638de`, landed in
      PR #1039 at merge `92d519b0` (2026-09-15T19:15:01Z). It reads a COMMIT
      RANGE, which is why this one § 2 task lives in the landing validator and
      not in the declaration's reader. **THE REFUSAL CARRIES NO STATUS TOKEN
      AND NONE IS INVENTED FOR IT**: `Finding.status` is `None` for the
      declaration refusals because the requirement they belong to names no
      token (`scripts/former_id_arrival.py:292-295`, `:310-321`); it is exit 1
      with `former-id-undeclared`'s siblings. Fixtures in `BoundEntryTests`
      (`tests/former_id_arrival/test_former_id_arrival.py`):
      `test_a_former_id_appended_by_a_commit_that_moves_nothing_is_refused`,
      `test_an_archived_id_appended_by_a_standing_packet_is_refused`,
      `test_an_id_that_never_existed_appended_by_a_standing_packet_is_refused`
      — the two fixtures this box asked for, plus the no-move case — and, in
      `MultiSourceTests`, `test_an_entry_no_source_carried_is_still_bound_to_nothing`
      and `test_a_two_source_arrival_is_judged_the_same_whichever_id_is_declared`,
      which prove the binding is to a SOURCE and not to a name.
- [x] 2.5 **ENFORCE APPEND-ONLY ACROSS COMMITS, NOT ONLY WITHIN ONE.** Compare
      the list against the one the packet carried at the commit's parent and
      refuse a commit that removes, reorders or respells an established entry,
      whether or not that commit moves anything. Fixtures: a declaration deleted
      the day after a lawful move (the attack that would hand the archive gate
      the later ratification under the current id, in a commit no arrival check
      looks at); an entry reordered; an entry respelled.
      **BUILT** — `append_only_problems` (compared against the list the packet
      carried at the commit's PARENT, read through `load_packet_at`), commit
      `59232b37`, merge `701c8fde`. All three attacks have fixtures —
      `test_append_only_refuses_a_removed_entry`,
      `test_append_only_refuses_a_reordered_entry`,
      `test_append_only_refuses_a_respelled_entry` — beside the two lawful
      shapes (`..._accepts_an_appended_entry`, `..._accepts_an_unchanged_list`)
      and the named attack itself,
      `test_a_declaration_deleted_the_day_after_a_move_is_refused`. An
      UNREADABLE parent declaration is not an empty one
      (`test_an_unreadable_parent_declaration_is_not_an_empty_one`,
      `test_load_packet_at_reads_none_for_a_path_absent_at_the_ref`). **ITS
      PRODUCTION CALLER LANDED WITH SLICE 4'S** per-commit arm (PR #1039,
      merge `92d519b0`): it runs on `main` today through the same workflow,
      under the same § 2.3 caveat — § 4.5's branch-rule registration is what
      still remains pending, not the call itself.
- [x] 2.6 **REFUSE A FORMER IDENTITY CLAIMED TWICE.** Two packets declaring the
      same former id, or an id that is at once a live packet id and a declared
      former id, is refused naming every claimant — an identity claimed twice
      resolves to a set, and a baseline chosen from a set is chosen by the
      resolver rather than by an author. Fixture: two claimants; a live id also
      declared as somebody's former id.
      **BUILT** — `former_identity_claimants` (the index) and
      `former_identity_ownership_problems` (the corpus sweep), commit
      `59232b37` hardened by `cce09fdd`, `018a65d3`, `e6ff63fa`, `fac01b29`
      and `256fe07a` on the same pull request; merge `701c8fde`. Fixtures:
      `test_two_packets_claiming_one_former_identity_refuse`,
      `test_a_live_id_also_declared_as_a_former_id_refuses`,
      `test_an_archived_packets_declaration_still_claims_its_lineage`,
      `test_one_owner_per_identity_reports_nothing`,
      `test_a_symlinked_archive_cannot_import_an_identity_from_outside`,
      `test_an_uncontained_live_directory_cannot_hide_an_archived_lineage` —
      and the live corpus is swept by
      `test_this_corpus_claims_no_identity_twice_today` and
      `test_every_packet_in_this_corpus_reads_its_declaration_cleanly`, which
      pass over this repository's own active and archived packets today.
      **ITS PRODUCTION CALLER LANDED WITH SLICE 4'S** corpus arm —
      `scripts/former_id_arrival.py` calls `former_identity_ownership_problems`
      on every run (PR #1039, merge `92d519b0`, 2026-09-15T19:15:01Z), so the
      sweep runs on every pull request today; what is still outstanding is
      § 4.5, the required-check registration, not the caller.

## 3. The archive gate — REALIZATION

- [x] 3.1 **RESOLVE THE BASELINE ACROSS THE DECLARED IDENTITIES.**
      `proposal-support.ratifying_commit` takes the current id and every
      declared former id, resolves each to the path it occupies at the commit
      being read by the two-candidate RULE `sequenced_after.proposal_path_at_ref`
      states — the active location, then a dated archive directory carrying the
      same id — and returns the EARLIEST commit at which any of them declares
      `Status: ratified`. **THE RULE, NEVER THAT FUNCTION'S BOOLEAN PROBES**:
      `_blob_exists_at_ref` asks `git cat-file -e`, which exits non-zero for a
      missing blob and for an unreadable one alike, and
      `_archive_dir_names_at_ref` returns an empty list on ANY read failure — so
      reusing them would make an unreadable former identity read as absent and
      let the walk take a later baseline, which is exactly what § 3.4 refuses.
      **BUILT** — `ratifying_baseline` (ONE `git log --full-history
      --topo-order --reverse` walk over the UNION of every identity's
      pathspecs, returning the commit, the identity and the path, EARLIEST
      ratification wins and no dates are compared), with `ratifying_commit`
      thinned to a wrapper over it; commit `2a9cfbda`, merge `701c8fde`. THE
      RULE AND NOT THE BOOLEAN PROBES: the resolution goes through
      `identity_paths_at` / `proposal_path_at` over `_tree_rows`, and
      `_blob_exists_at_ref` and `_archive_dir_names_at_ref` are not reused for
      it. Fixtures:
      `test_a_declared_move_resolves_the_baseline_to_the_first_ratification`,
      `test_the_declaration_is_what_makes_the_difference`,
      `test_a_declared_rename_chain_is_baselined_at_the_first_ratification`
      (the #1003 chain, declared, baselined at the FIRST ratification),
      `test_an_identity_resolves_to_its_archived_location`,
      `test_the_declared_lineage_is_read_from_an_archived_packet_too`,
      `test_a_preserved_dated_archive_id_is_enumerated_by_the_walk`.
- [x] 3.1a **REFUSE AN IDENTITY THAT RESOLVES TWICE.** Where the current id or a
      declared former id matches more than one candidate location in the tree
      being read, refuse CANNOT RUN naming the candidates rather than taking the
      first sorted one. The estate's own `archived_change_dirs` already states
      the rule — it returns a LIST because "two archive dates for one id is an
      AMBIGUITY the resolver must be able to report, not a collision to resolve
      by taking the newest" — and `proposal_path_at_ref` does not carry it at a
      ref.
      **BUILT** — `identity_paths_at` returns a LIST of every candidate
      location at the ref and `proposal_path_at` refuses CANNOT RUN naming the
      candidates rather than taking the first sorted one; commit `2a9cfbda`,
      with the archive-directory reading corrected by `b90fc7f6` and
      `fac01b29` on the same pull request; merge `701c8fde`. Fixtures:
      `test_an_identity_resolving_to_two_locations_refuses_cannot_run`,
      `test_an_identity_matching_two_archive_directories_still_refuses`,
      `test_an_identity_holding_a_packet_in_two_places_refuses_the_lineage`,
      `test_an_archive_directory_that_merely_ends_with_the_id_is_not_it`,
      `test_an_active_id_that_begins_with_a_date_keeps_it`,
      `test_an_archived_dated_directory_does_not_guess_its_own_identity`.
- [x] 3.2 **LEAVE THE UNDECLARED REFUSAL EXACTLY WHERE IT IS.** PR #846's
      `origin-retention-path-moved` refusal stands unchanged for a packet that
      declares nothing; what changes is that a packet which DOES declare now has
      a lawful answer.
      **HELD** — `_refuse_an_undeclared_move` carries PR #846's refusal to the
      sentence, silent only for the declared move; commit `2a9cfbda`, merge
      `701c8fde`. Every #846 and #999 fixture is unchanged and green —
      `test_a_ratified_change_renamed_afterwards_refuses_the_walk`,
      `test_a_ratified_packet_copied_to_a_new_id_refuses_too`,
      `test_an_unratifying_rename_now_refuses_the_walk`,
      `test_a_ratified_packet_copied_as_a_draft_and_ratified_later_is_not_refused`,
      `test_renaming_a_draft_and_ratifying_it_afterwards_is_not_refused`,
      `test_a_git_config_cannot_switch_the_guard_off` — and the new
      `test_an_undeclared_source_is_still_refused_when_another_is_declared`
      proves a declaration does not buy silence for an UNDECLARED move beside
      it. `test_the_guard_refuses_nothing_on_this_repository_today` still
      passes over the live corpus.
- [x] 3.3 **DO NOT MOVE THE COMPARISON.** The origin block must still equal the
      declaration at the resolved baseline exactly; the support manifest's
      repeated origin fields are still measured against it; an accepted mutation
      still takes the explicit disposition. Add the test that proves a declared
      move carrying an origin edit is refused as a MUTATION — the laundering
      case.
      **HELD, AND THE LAUNDERING CASE IS PINNED** — `origin_retention_errors`
      reads the baseline declaration under the BASELINE IDENTITY rather than
      under the id the packet carries now, and compares exactly as before;
      commit `2a9cfbda`, merge `701c8fde`. The laundering fixture is
      `test_a_mutation_riding_in_the_declared_move_is_still_a_mutation` (the
      refusal names *"under the declared former identity change-r"*), beside
      `test_a_declared_move_with_no_mutation_retains_its_origin`. The
      disposition channel is unmoved and still measured against the accepted
      declaration (`test_an_accepted_disposition_moves_the_baseline_and_archives`,
      `test_the_support_manifest_is_measured_against_the_accepted_origin`,
      `test_an_accepted_mutation_does_not_license_the_next_one`), and
      `test_the_archive_subcommand_offers_no_bypass_flag` still passes.
- [x] 3.4 **FAIL CLOSED ON EVERY READ BEHIND THE BASELINE.** Presence read from
      the tree; content read separately; a read that could not be performed
      raised as CANNOT RUN naming the read and the identity it was for. Never
      report an unreadable history as an unratified one. `design.md` M1 is the
      measurement; PR #1024's retained branch `2bc60386` carries a worked
      version of this half and is a candidate to lift.
      **BUILT** — presence is read from the tree (`_tree_rows`, which returns
      `None` on ANY non-zero exit and never an empty list), content is a
      SECOND read (`_text_at_a_present_path`), and a read that could not be
      performed raises `OriginRetentionError` CANNOT RUN naming the read and
      the identity it was for (`_unreadable_read_refusal`, `_rows_or_refuse`);
      commit `5859f053`, extended to the undeclared-move probe's own two reads
      by `da9297e0`, to the commit enumeration by `ef022a83`, and to the
      lineage header by `7568c9f1`; merge `701c8fde`. Fixtures:
      `test_an_unreadable_baseline_read_refuses_cannot_run`,
      `test_an_unreadable_archive_listing_refuses_cannot_run`,
      `test_a_present_path_whose_blob_is_unavailable_is_not_read_as_absent`,
      `test_a_genuinely_absent_path_is_still_read_as_absent`,
      `test_the_refusal_names_the_read_and_the_identity_it_was_for`,
      `test_an_unreadable_commit_enumeration_is_not_an_unratified_packet`,
      `test_an_unreadable_move_probe_refuses_rather_than_concluding_no_move`,
      `test_the_move_probes_source_header_read_refuses_where_it_stands`,
      `test_an_unresolvable_candidate_commit_refuses_at_the_gate_door`,
      `test_a_header_that_stands_and_does_not_parse_is_not_an_empty_lineage`,
      `test_an_unreadable_ratification_blob_cannot_authorise_an_acceptance`.
      `design.md` M1's partial checkout is the shape they reproduce; PR
      #1024's branch was NOT lifted, the half being rewritten against this
      packet's own readers.

## 4. The landing validator — REALIZATION

- [x] 4.1 **BUILD THE READER AND THE CLI** in the shape
      `gate-realization-axis-vocabulary` established: a module under `scripts/`,
      a validator CLI beside it, a test suite over the live corpus.
      **BUILT** — the module `scripts/former_id_arrival.py` (1713 lines), the
      CLI `scripts/validate-former-id-arrival.py` (140) beside it, and the
      suite `tests/former_id_arrival/test_former_id_arrival.py` (2126, 53
      tests) with `tests/former_id_arrival/test_former_id_arrival_gate_wiring.py`
      (194, 9 tests) beside it; commit `68a00c1c` and the twenty-two review and
      drift commits after it, landed in PR #1039 at merge `92d519b0`
      (2026-09-15T19:15:01Z). The live corpus IS swept, not only fixtures:
      `test_the_live_corpus_passes_this_gate` (`CliTests`) runs the gate over
      this repository, and `scripts/validate-former-id-arrival.py .` reads 46
      active and 168 archived packets at this commit. Every other fixture is a
      real git repository built in a `TemporaryDirectory` — the rule
      `tests/target_release/test_target_release_gate.py` states for its own
      gate — so no test here can be made green by editing this repository. The
      workflow that RUNS the CLI is `.github/workflows/former-id-arrival-gate.yml`
      (commit `abf2cfc4`), and what a workflow file is and is not evidence of
      is § 4.5's business, below.
- [x] 4.2 **REFUSE THE UNDECLARED ARRIVAL, QUALIFIED BY THE SOURCE'S HISTORY.**
      Status `former-id-undeclared`, exit 1, naming the commit, the source path,
      the destination path and the one repair. **No bypass flag** (#690). **The
      refusal reaches a move whose SOURCE IDENTITY HAS EVER DECLARED
      `Status: ratified`, read over that identity's whole history up to the
      commit and never off its blob at the parent** — a packet renamed and
      un-ratified in one commit is back in draft for every later hop, so a test
      taken at the parent would exempt the shape this exists to catch. A move of
      a packet that has NEVER been ratified passes with no declaration, which is
      what `docs/document-lifecycle.md` already promises: *"renaming a DRAFT
      change, and a single commit that renames a draft and ratifies it, are
      unaffected"*. Fixtures on both sides of the qualification.
      **BUILT** — `judge_commit` pairs the move through `relocations_at` and
      refuses through `_undeclared_finding`; the qualification is `ever_ratified`,
      which walks the source identity's WHOLE history up to the commit rather
      than reading its blob at the parent; commit `68a00c1c`, with the pairing
      qualified against the tree by `1c4d0131` and the raw-byte decode by
      `c892968a`, landed in PR #1039 at merge `92d519b0`
      (2026-09-15T19:15:01Z). Status `former-id-undeclared`, **exit 1**, the
      message naming the commit, the source path, the destination path and the
      one repair (`scripts/former_id_arrival.py:289`, `:1008`). **NO BYPASS
      FLAG**, asserted over the parser's OWN option strings rather than over
      prose: `test_there_is_no_bypass_flag` (`CliTests`). Fixtures on both
      sides of the qualification (`ArrivalRefusalTests`):
      `test_a_ratified_packet_renamed_with_no_declaration_is_refused` and
      `test_the_refusal_names_the_commit_both_paths_and_the_one_repair` against
      `test_a_never_ratified_draft_rename_passes_with_no_declaration`; the
      un-ratifying hop `test_a_once_ratified_packet_moved_while_back_in_draft_is_refused`
      with `test_the_ever_test_is_the_whole_history_and_never_the_parent_blob`
      proving the EVER reading is what catches it;
      `test_a_rename_chain_is_refused_at_its_first_hop_and_no_chain_is_walked`
      (asked of a repository whose HEAD *is* the first hop, so the later hops
      do not exist when the question is put);
      `test_the_declared_move_lands`; and, for the shapes that are not moves at
      all, `test_a_fork_by_copy_is_not_a_move_and_is_not_refused`,
      `test_a_file_moved_between_two_standing_packets_is_not_an_arrival`,
      `test_a_merge_commit_performs_no_move_of_its_own` and
      `test_a_hostile_diff_config_cannot_switch_the_pairing_off`.
- [x] 4.2a **READ THE SOURCE'S WHOLE DECLARED LINEAGE, NOT ITS ID ALONE.** The
      "ever ratified" test covers the source packet's own id TOGETHER WITH every
      id it declares in `former_ids:` at the commit's parent — otherwise a
      packet that already moved once lawfully (X ratified, X→Y declared and
      returned to draft, then Y→Z) passes its second landing on Y's own empty
      history and stands with no lineage. This is ONE blob at ONE commit and not
      a history walk. Fixture: the three-id chain, refused at the second hop.
      **BUILT** — `ever_ratified` is asked about the source's own id TOGETHER
      WITH every id `declared_at` reads from its `.openspec.yaml` at the
      commit's PARENT: one blob at one commit, never a history walk; commit
      `68a00c1c`, landed in PR #1039 at merge `92d519b0`. Fixture:
      `test_a_packet_that_already_moved_lawfully_is_refused_on_its_second_move`
      (`ArrivalRefusalTests`) — X ratified, X→Y declared and returned to draft,
      then Y→Z, refused at the second hop on Y's inherited lineage rather than
      passing on Y's own empty history — beside
      `test_an_undeclared_rename_chain_now_refuses_at_its_landing`, which
      rebuilds #1003's own chain and asserts BOTH halves over one tree: the
      archive gate still silent on it by § 3.2's rule, and this gate refusing
      the hop that would have created the history in the first place.
- [x] 4.2c **FAIL CLOSED ON THE RATIFICATION LOOKUP TOO, NOT ONLY ON THE
      PAIRING.** Deciding whether the source lineage has ever declared
      `Status: ratified` is a SECOND historical read, and on a checkout that
      cannot produce those blobs it returns the same silence as a lineage that
      was never ratified — passing an undeclared landing on the one checkout
      where nothing can be proved. Distinguish ABSENT from UNREADABLE on the
      same terms as § 3.4 and refuse CANNOT RUN naming the identity and the
      read. Fixture: the partial checkout of `design.md` M1, asked the
      qualification question.
      **BUILT** — `ever_ratified` reads presence from the tree
      (`_tree_rows_or_refuse`) and content as a SECOND read
      (`_git_show_bytes`), raising `ArrivalCannotRun` — `former-id-arrival-unreadable`,
      **exit 2** — naming the identity and the read rather than answering
      "never ratified"; commit `68a00c1c`, with the strict decode and the
      ambiguous archived source added by `d8385882` and the raise-is-a-failed-read
      case by `d053b38e`; landed in PR #1039 at merge `92d519b0`. Fixtures in
      `FailClosedTests`: `test_an_unreadable_ratification_lookup_refuses_cannot_run`
      (a real `--filter=blob:none --no-checkout` clone whose promisor is
      unreachable — `design.md` M1's shape, and it asserts its own precondition
      so a git that behaves differently FAILS rather than passing vacuously),
      `test_a_corrupted_ratification_proof_refuses_rather_than_garbles`,
      `test_a_historical_manifest_with_invalid_utf8_is_refused_not_garbled`,
      `test_a_present_manifest_that_does_not_parse_is_refused_not_read_as_empty`,
      `test_a_manifest_that_is_not_a_mapping_is_refused_by_the_range_arm_too`,
      `test_a_manifest_that_cannot_be_read_at_all_is_refused_not_skipped`,
      `test_a_symlink_is_refused_and_is_never_read_through` and
      `test_a_symlinked_corpus_root_is_refused_before_anything_is_walked`;
      and in `ArrivalRefusalTests`,
      `test_a_move_from_an_ambiguous_archived_source_refuses_cannot_run`.
- [x] 4.2b **REQUIRE THE ARRIVING LIST TO BE THE SOURCE'S LIST PLUS THE SOURCE
      ID**, in the source's own order. A move that drops an entry the source
      declared sheds a lineage, which is the same defect as never declaring one.
      Fixture: a declared move whose destination omits an inherited entry.
      **BUILT** — `judge_commit` requires the arriving list to equal the
      source's list at the parent with the source id appended, in the source's
      own order, and refuses the shed lineage as an undeclared arrival; commit
      `68a00c1c`, landed in PR #1039 at merge `92d519b0`. Fixture:
      `test_a_move_that_drops_an_inherited_entry_is_refused`
      (`ArrivalRefusalTests`).
- [x] 4.3 **EXCEPT THE ARCHIVE RELOCATION BY ID.**
      `openspec/changes/<id>/` to `openspec/changes/archive/<YYYY-MM-DD>-<id>/`
      with the id unchanged passes with no declaration.
      **BUILT, AND IT IS THE ONLY EXCEPTION** — the exception is taken on the
      ID and not on the shape of the path (`change_id_of_dir` strips the
      `YYYY-MM-DD-` prefix only under `ARCHIVE_ROOT`, the fix `1c4d0131` took
      after a live id that itself begins with a date read as an archived one);
      commit `68a00c1c`, corrected by `1c4d0131` and extended to the archived
      directory's OTHER reading by `24cd42a1`; landed in PR #1039 at merge
      `92d519b0`. Fixtures (`ArrivalRefusalTests`):
      `test_the_archive_relocation_passes_with_no_declaration` (and the same
      relocation under a DIFFERENT id is still refused),
      `test_archiving_a_packet_whose_id_is_already_dated_is_excepted_too`,
      `test_a_live_packet_id_that_begins_with_a_date_keeps_its_whole_id`,
      `test_ever_ratified_finds_the_EXACT_reading_of_a_dated_archived_id`, and
      in `ConsumedReaderTests`
      `test_an_archived_self_claim_under_its_OTHER_reading_is_refused`.
- [x] 4.4 **FAIL CLOSED ON THE ARRIVAL READ.** Where the pairing cannot be
      computed AND the tree shows both a packet directory arriving and one
      leaving in that commit, refuse `former-id-arrival-unreadable`, exit 2,
      CANNOT RUN, naming the read. Do NOT pair from the tree: a commit that
      withdraws one packet and creates an unrelated other has the same shape.
      **BUILT** — where `diff_at` cannot compute the pairing AND `packet_dirs_at`
      shows both a packet directory arriving and one leaving in that commit,
      `judge_commit` raises `ArrivalCannotRun` — `former-id-arrival-unreadable`,
      **exit 2** — naming the read; where nothing left, it does not refuse.
      The pairing is still GIT'S: `relocations_at` asks the tree one further
      question about a pairing `git diff-tree -M` already made, which is not
      the tree-pairing D3 declined. Commit `68a00c1c`, with the tree
      qualification added by `1c4d0131` and the two-source binding by
      `ff7fcb7c`; landed in PR #1039 at merge `92d519b0`. Fixtures
      (`FailClosedTests`): `test_an_unpairable_arrival_with_a_departure_refuses_cannot_run`
      and `test_an_unpairable_arrival_with_no_departure_is_not_refused` — the
      two halves of the rule — with `test_a_grafted_boundary_takes_no_refusal`
      holding § 6.4's line, and in `ArrivalRefusalTests`
      `test_the_pairing_is_read_from_every_file_and_not_from_the_proposal_alone`.
- [ ] 4.5 **REGISTER IT AS A REQUIRED CHECK** and record the run it adds.
      **OPEN, AND IT IS NOT AN AUTHOR'S TO CLOSE — BRETT HEAP'S OPERATOR ACT.**
      A merged workflow file is not evidence; the evidence is the LIVE RULESET
      STATE, on the terms `add-wallet-carried-review-authority` task 2.5 and
      `add-signed-execution-chain` § 4.5 established.
      **THE SHAPE IS RULED AND THE ACT IS NOT PERFORMED.** Brett Heap,
      2026-09-15T19:00Z, by multiple choice in this lane's window, verbatim
      ***"Dedicated required check"*** — the arrival gate stays a DEDICATED
      workflow and the context to require is the job id
      `former-id-arrival-gate`, which by house rule carries no `name:` display
      string so the check surfaces as exactly that literal
      (`.github/workflows/former-id-arrival-gate.yml`, pinned by
      `tests/former_id_arrival/test_former_id_arrival_gate_wiring.py::test_the_job_carries_no_display_name`).
      Recorded at
      https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5686436893.
      Q1 is therefore settled and the cheaper route — folding the validator
      into the already-required `pytest-suite` — is NOT taken.
      **RE-MEASURED LIVE 2026-09-15T19:41Z**, after slice 4 landed:
      `GET /repos/opensoft/openxFactory/rules/branches/main` returns the same
      three required-status-check rules and `former-id-arrival-gate` is in
      none of them — `{21957695: signed-execution-chain-gate, lane-line}`,
      `{22551797: openspec-cli-pin}`, `{21538893: wallet-validation,
      pytest-suite, lane-line, release-tag-gate}`. WHAT IS OWED, AND IT IS
      BRETT HEAP'S CONSOLE ACT AND NO AUTHOR'S: the context added to a ruleset
      targeting `openxFactory` `~DEFAULT_BRANCH` (a dedicated ruleset is the
      precedent, org ruleset 21957695), then BOTH a live read of
      `GET /orgs/opensoft/rulesets/<id>` and of
      `GET /repos/opensoft/openxFactory/rules/branches/main` showing the
      context, and a CANARY pull request
      carrying an undeclared rename of a ratified packet going red with
      exactly one named refusal (`former-id-undeclared`), reported BLOCKED,
      closed unmerged with its branch deleted — the shape of canary #549, run
      33455808456. UNTIL THEN THE GATE REFUSES NO LANDING: it RUNS on every
      pull request and a merge button beside its red check still works.
      **THE SELF-REPORT, AND WHERE IT ACTUALLY LIVES.**
      `add-signed-execution-chain`'s degraded case had three parts — canon
      saying the capability confers and refuses nothing until a named reader
      runs as a required check, a shipped declaration reading
      `is_required_in_ruleset: false`, and a reader that warns on every run.
      Here the statement is carried by the workflow itself and is cited rather
      than duplicated: `.github/workflows/former-id-arrival-gate.yml:13-21`
      (*"THIS FILE IS NOT EVIDENCE THAT THE CHECK IS REQUIRED … this gate
      refuses NOTHING"*) and `:23-32` (the live-ruleset-read-plus-canary
      evidence, *"and never this file"*). **MEASURED, AND THE DIFFERENCE IS
      NAMED RATHER THAN GLOSSED: the CLI itself emits no such warning** —
      `python3 scripts/validate-former-id-arrival.py .` prints its range note,
      its corpus sweep and its pass line and says nothing about the ruleset —
      so the self-report on this packet is the workflow header plus this
      disposition, one place fewer than the precedent had. Adding it to the
      reader would be an edit to slice 4's file and is not taken here.
      **THE PACKET MAY ARCHIVE WITH THIS ACT UNPERFORMED — RULED — AND THE
      BOX IS TICKED WITH A DISPOSITION AT THE ARCHIVE, NOT LEFT `[ ]`.** Brett
      Heap, 2026-09-15T19:00Z, verbatim ***"Yes, with disposition +
      carry-forward issue"*** (same record). The mechanism is fixed by the
      archive gate itself: `archive_change()` refuses any `tasks.md` line
      matching `^- [ ]` with `change has incomplete tasks`
      (`scripts/proposal-support.py`, the `incomplete tasks` check before the
      pin is resolved) and carries no per-section exception — so this box
      stays `[ ]` until the archive pull request, and THAT pull request ticks
      it `[x]` with the disposition written beneath (*not performed at the
      archive; carried as openxFactory#<carry-forward issue>*), exactly as
      `add-signed-execution-chain` carried its § 4.5 at issue #534 (filed
      2026-08-31 at its archive) so that an open operator act is not written
      down only inside an archived packet. No exception to the gate is built
      for this, and none is claimed. **THE CARRY-FORWARD ISSUE IS FILED BY THE ORCHESTRATOR AT THE
      ARCHIVE, ON HIS WORD — filing is a reserved act and no author on this
      lane performs it**, and until it exists this box and the archive pull
      request's own body are the only places the obligation stands.

## 5. The reference resolver and the documents — REALIZATION

- [x] 5.1 **RESOLVE A PACKET REFERENCE BY IDENTITY.** By change id — against the
      location that id occupies now, active or archived, and against any packet
      declaring it as a former id — reaching citations written as
      `openspec/changes/<id>/<file>` paths, whose second segment names the
      packet. A reference that resolves owes the citing record no edit.
      **BUILT** — `scripts/packet_reference.py`: `packet_reference()` reads the
      identity out of the second segment, `PacketIndex` claims every live and
      archived location plus every id a packet declares in `former_ids:`, and
      `resolve()` answers `RESOLVED` / `DANGLING` / `AMBIGUOUS` /
      `NOT_A_PACKET_REFERENCE`; commit `6b39004f`, with the containment rule
      added by `cac9a6fb`, the archived directory's two readings by `6ef8592c`
      and the unreadable marker by `b32e05aa`; landed in PR #1037 at merge
      `8f393758` (2026-09-15T19:02:27Z). Fixtures in
      `tests/packet_reference/test_packet_reference.py`:
      `test_a_cited_path_naming_a_packet_that_has_since_archived_resolves_by_id`,
      `test_a_cited_path_naming_a_declared_former_id_resolves_to_that_packet`,
      `test_a_cited_path_resolving_to_no_identity_at_all_is_dangling`,
      `test_a_reference_that_resolves_owes_the_citing_record_no_edit` (the
      requirement's own remedy sentence AS BEHAVIOUR — no corrected spelling is
      offered, because offering one is how a reader becomes an editor),
      `test_a_citation_naming_the_packet_directory_itself_resolves`,
      `test_an_archived_spelling_resolves_by_id_when_the_archive_date_moves`,
      and the corpus sweeps `test_every_packet_in_this_corpus_resolves_to_exactly_itself`
      and `test_the_index_claims_at_least_what_the_corpus_ownership_sweep_claims`.
- [x] 5.2 **LEAVE THE CROSS-REPOSITORY CASE OUT OF SCOPE ON THE TREE BEING
      READ**, a reference to another repository's packet being no evidence about
      that reference.
      **HELD** — a referent qualified to another repository is never handed to
      the resolver at all; commit `6b39004f`, consumer arm `34473ecd`, merge
      `8f393758`. Fixtures: `test_a_reference_to_another_repository_is_out_of_scope`
      (`tests/packet_reference/`) and, at the caller,
      `test_a_referent_qualified_to_another_repository_is_still_out_of_scope`
      (`tests/pin_registrations/test_pin_registration_sweep.py`), which is a
      SPY and proves the resolver is never asked rather than asserting it
      answered harmlessly. `test_a_path_that_is_not_under_openspec_changes_is_not_a_packet_reference`
      and `test_a_path_under_openspec_changes_that_addresses_no_packet_is_left_to_the_path`
      hold the other two out-of-scope shapes.
- [x] 5.0 **THE CONSUMER IS NAMED, AND IT ALREADY EXISTS.**
      `scripts/validate-pin-registrations.py`'s `check_citations` resolves every
      `dispositions[].cited_to` referent and refuses exit 1 on an absent path
      (landed for issue #840). It resolves the RAW PATH, and `design.md` D0 M5
      measures six live referents pointing into four ACTIVE packets — so the
      next of those four to archive turns a lawful act into an exit-1 refusal.
      That reader is updated to resolve by identity (§ 5.1) rather than by raw
      path, with its own tests: an archived-by-id referent PASSES where the raw
      path no longer exists, a referent qualified to another repository is still
      out of scope, and a referent whose identity resolves but whose file does
      not still REFUSES. Without this task the resolver would be a reader with
      no caller.
      **BUILT, AND THE READER HAS ITS CALLER** —
      `scripts/validate-pin-registrations.py`'s `check_citations` now asks
      `packet_reference.resolve(ROOT, referent, index=…)` for every referent it
      reads as a packet reference and falls back to `resolve_in_tree` only for
      the paths that address no packet
      (`scripts/validate-pin-registrations.py:774`, `:881-895`); commit
      `34473ecd`, with `fbc18db1` and `b32e05aa` correcting both call sites;
      landed in PR #1037 at merge `8f393758`. **THE DATED FAILURE IT
      PREVENTS, MEASURED**: six of the 17 live in-tree referents point into
      four ACTIVE packets, so the next of those four to archive would have
      turned a lawful act into an exit-1 refusal of a gate nobody touched.
      The run is unchanged today — `every in-tree path resolves`, exit 0 — and
      one new line appears only on the day the first of those four archives.
      Fixtures (`tests/pin_registrations/test_pin_registration_sweep.py`):
      `test_an_archived_by_id_referent_passes_where_the_raw_path_is_gone`,
      `test_a_referent_whose_identity_resolves_nowhere_still_refuses`,
      `test_a_referent_whose_identity_resolves_but_whose_file_does_not_still_refuses`,
      `test_an_ambiguous_referent_is_refused_against_the_declaration`,
      `test_a_citation_that_names_no_packet_is_still_resolved_as_a_path`,
      `test_the_checker_reaches_the_resolver_and_not_a_second_copy_of_the_rule`
      (the rule is not re-implemented at the caller) and the corpus test
      `test_the_live_pin_registration_citations_still_resolve`.
- [x] 5.1a **RESOLVE BOTH HALVES OF A PACKET-RELATIVE CITATION.** The location
      the identity resolves to must also carry the remainder the citation names;
      an identity that resolves to a packet not carrying the cited file is
      DANGLING, reported against the FILE and not against the packet. Resolving
      the identity alone would accept a citation to a file deleted, renamed or
      never written. Fixtures: a live id with a deleted remainder; an archived id
      whose remainder moved inside the packet.
      **BUILT** — `Claim.carries()` asks the resolved location for the
      remainder the citation names, and a location that resolves without it is
      DANGLING at the FILE half, reported against the file and not against the
      packet (`Resolution.half`); commit `6b39004f`, merge `8f393758`.
      Fixtures: `test_an_identity_that_resolves_with_a_missing_file_names_the_file_half`
      (both shapes this box asked for) and `test_the_report_names_which_half_failed`,
      which asserts the discrimination rather than two substrings; at the
      caller, `test_a_referent_whose_identity_resolves_but_whose_file_does_not_still_refuses`.
- [x] 5.2a **REPORT AN AMBIGUOUS REFERENCE RATHER THAN RESOLVING IT.** An id
      that would resolve to more than one candidate is AMBIGUOUS, and the defect
      belongs to the declaration that made one identity resolve twice rather
      than to the citing record. Never settle it by sort order.
      **BUILT** — `resolve()` answers `AMBIGUOUS` naming every candidate and
      never prefers one; commit `6b39004f`, with `b93e1fcf` correcting the
      report so an ambiguity with no declaration behind it is not blamed on a
      declaration; merge `8f393758`. Fixtures:
      `test_an_id_resolving_twice_is_ambiguous_and_never_preferred` — asked
      TWICE, with the cited file in the first-sorted candidate and then only in
      the last, so a resolver that quietly picked one cannot pass by symmetry —
      `test_the_ambiguity_belongs_to_the_declaration_and_not_to_the_citing_record`
      and `test_a_duplicate_packet_location_is_ambiguous_with_no_declaration_at_all`.
      **MEASURED ON THE LIVE CORPUS: AMBIGUOUS 0**, no packet in this tree
      declaring a `former_ids:` entry today.
- [x] 5.3 **AMEND `docs/document-lifecycle.md`.** Its sentence *"Renaming a
      ratified change is therefore blocked until a change declares a FORMER ID
      (issue #833, a successor packet)"* is the sentence this packet answers; it
      must then say what a declared move requires instead of saying the act is
      blocked. Nothing else in that paragraph moves.
      **PERFORMED** in this pull request, commit `1ef15e86`: the sentence now
      says a ratified change's directory MAY move and what the move owes — the
      top-level `former_ids:` declaration, a SIBLING of `origin:`, naming
      change IDS and never paths, oldest first, APPEND-ONLY ACROSS COMMITS,
      the entry added by the COMMIT THAT PERFORMS THE MOVE and the arriving
      list being the source's list with the source id appended; the archive
      gate resolving the baseline across every declared identity and taking
      the EARLIEST ratification, so a rename is not a way to launder a
      mutation; and the UNDECLARED arrival refused at the landing of the
      commit that performs it, with the rule and its enforcement said
      SEPARATELY: as re-measured 2026-09-15 at this landing the gate HAS now
      landed on `main` (§ 4.1–4.4, PR #1039 → `92d519b0`) and RUNS on every
      pull request, and it is named by no branch ruleset (§ 4.5, still
      outstanding), so the sentence says an undeclared arrival can still LAND
      meanwhile — a red check beside a merge button that works — with the
      archive refusal `origin-retention-path-moved` named as the one
      enforcement that does stand — a single undeclared hop, at the archive,
      never at the landing — rather than implying a protection this estate
      does not have.
      The citation also states the PACKET'S OWN state — ratified 2026-09-13,
      its `release-realization` delta promoting at § 7.1 and not before —
      because canon carries neither the amended sentence nor the one it
      replaces: `grep -rn "FORMER ID\|former_ids\|Renaming a ratified"
      openspec/specs/` is EMPTY, PR #846's passage having been document prose
      from the start.
      The promoted clause *"renaming a DRAFT change, and a single commit that
      renames a draft and ratifies it, are unaffected"* is carried verbatim,
      and nothing else in that paragraph moved. **Q4 IS RULED, AND THE
      AUTHORITY IS THIS BOX.** Brett Heap, 2026-09-15T19:00Z, by multiple
      choice in this lane's window, verbatim ***"Yes, task 5.3 is
      authority"***: the amendment of a document carrying `Status: standard`
      and ratified by PR #846's act rests on this packet's own ratified task,
      which commissions the edit by quoting the exact sentence, plus
      `proposal.md`'s `code_surface:`, which names the file — **no separate
      amendment route, and not deferred to promotion**. Recorded at
      https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5686436893.
      The question was asked rather than let pass silently, and it is answered
      here rather than in a pull-request body that archives with the packet.
- [x] 5.4 **RE-MEASURE THE DANGLING-CITATION POPULATION ON THE REALIZATION
      TREE** and record it there. `design.md` M4's figures (94 dangling, 58
      resolvable by id) were taken at `9378eca5` and are history by the time the
      resolver lands.
      **RE-MEASURED 2026-09-14 ON THE REALIZATION TREE**, over every tracked
      file except `openspec/changes/archive/`, `tests/` and `specs/`, at
      `main` `701c8fde` (the slices 1–3 landing) and identically on this
      branch:

      | | M4 @ `9378eca5` | 2026-09-14 @ `701c8fde` |
      | --- | --- | --- |
      | distinct dangling `openspec/changes/<id>/…` references | 94 | **104** |
      | of which resolve BY ID against the archive | 58 | **64** |
      | remainder, unclassified and NOT claimed as defects | 36 | **40** |

      **THE CAVEAT IS CARRIED RATHER THAN BURIED: this is a
      RE-IMPLEMENTATION of M4's stated recipe and not the authoring script,
      which was never committed**, so the delta is approximately — not
      exactly — comparable, and a reader who needs an exact delta must re-run
      both. The figures also move as packets archive, the archive relocation
      being what breaks a cited path in the first place. The population is
      REPORTED here and claimed as a defect nowhere: the reporting sweep is
      § 6.1's successor, which `design.md` D4 rules is a second governed
      surface, and these figures are recorded so that successor need not
      re-derive them.

      **DATED, AND NOT RE-ASSERTED AT THIS LANDING.** The three figures are the
      reading at `701c8fde` on 2026-09-14. The tree has moved twice since —
      slices 4 and 5 at `92d519b0` and `8f393758`, and the archive of
      `extend-prose-tagging-target-to-pinned-capabilities` at `8944758c`, an
      archive being exactly the act that relocates a path and so moves this
      population — so *"identically on this branch"* is the 2026-09-14 reading
      and is not claimed again here. **WHAT THE SUCCESSOR GAINS INSTEAD OF A
      THIRD RE-IMPLEMENTATION**: M4's authoring script was never committed and
      the 2026-09-14 re-implementation was not either, but § 5.1's resolver IS
      — `scripts/packet_reference.py`, landed at `8f393758`, tested, and able
      to separate the remainder further than either recipe could (the IDENTITY
      half from the FILE half, and AMBIGUOUS from both). A successor that
      adopts it measures something reproducible, and the figures it reads will
      NOT equal 104 / 64 / 40, because the extraction recipe differs and not
      because the corpus changed. Recording that difference is cheaper than
      discovering it.

## 6. Residue — named here, taken nowhere

- [ ] 6.1 **NOT TAKEN — THE REPORTING SWEEP FOR UNRESOLVABLE REFERENCES.**
      `design.md` D4 rules that a check family reporting the remainder is a
      second governed surface: a `## MODIFIED Requirements` block over
      `doc-health`'s *Deterministic check families*, whose promoted numeral
      reads *"twenty-three check families"*, plus a registry edit and a numeral,
      gated by the family-enumeration family. The figures the successor needs are
      measured here so it does not re-derive them: **94** dangling
      `openspec/changes/<id>/…` references, **58** of them resolvable by id, the
      other **36** unclassified and deliberately not claimed as defects. File it
      with a sibling search at the realization, not here.
      **STILL NOT TAKEN, AND THE FIGURES ABOVE ARE M4'S AT `9378eca5`.** § 5.4
      carries the 2026-09-14 re-measurement on the realization tree — 104
      dangling, 64 resolvable by id, 40 remaining — which is where the
      successor should start, together with § 5.4's note that the committed
      resolver `scripts/packet_reference.py` is now the reproducible way to
      take the reading. **WHEN IT IS FILED IS RULED**: Brett Heap,
      2026-09-15T19:0xZ, by multiple choice in this lane's window, verbatim
      ***"File it after #1041 lands"*** — the successor is filed AS A ROUTING
      RECORD and NOT CLAIMED, after slice 6 lands. Recorded at
      https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5686628685. FILING it,
      with the sibling search, is a reserved act: it is the orchestrator's on
      that word and no author on this lane performs it, which is why this box
      stays open at this landing rather than being ticked against an
      intention.
- [ ] 6.2 **NOT TAKEN — THE INTERIM DOCSTRING-AND-FIXTURE PIN.** Part 2 of the
      ruling, a plain fix on `fix/1003-interim-pin-multi-hop-gap`, deliberately
      not carried in this packet.
- [ ] 6.3 **NOT TAKEN — WHETHER A RE-RATIFICATION AFTER A RETURN TO DRAFT IS A
      NEW BASELINE.** PR #1024's stated gap. This mechanism reaches the MOVE
      rather than the ratification, so the undeclared move is refused whatever
      the blob says; the governance question behind it is not answered here.
- [ ] 6.4 **NOT TAKEN — A SHALLOW-CHECKOUT REFUSAL CLASS.** At a grafted
      boundary git reports no parents and therefore no pairing. Refusing every
      shallow checkout outright is a new refusal class on a gate with no bypass
      flag and belongs to a change that says so.
- [ ] 6.5 **NOT TAKEN — NO OTHER ESTATE REPOSITORY IS SWEPT.** Every rule here is
      scoped to the corpus of the repository being read; no other governed
      repository's corpus, register or CI is read, written or referenced.

## 7. Archive — owed on this packet's own terms

- [ ] 7.1 **PROMOTE THE ONE MODIFIED AND THREE ADDED REQUIREMENTS INTO CANON**,
      byte-for-byte, in a SEPARATE pull request on a separate word, AFTER § 1 is
      ruled and AFTER the realization evidence this packet's `target_release:`
      names. `code_surface` is NON-EMPTY, so under *Realization archive gate*
      this packet does not archive on landing and does not archive on
      ratification: it archives when the realization slices of § 2 through § 5
      are merged on the implemented target and `pytest-suite` has run green at
      the tree that merge carries. **Neither this pull request nor the
      ratification pull request may perform it.**
      **THE ARCHIVE MAY PROCEED WITH § 4.5 UNPERFORMED — RULED — BY TICKING
      § 4.5 WITH A DISPOSITION, NEVER BY LEAVING IT `[ ]`.** Brett Heap,
      2026-09-15T19:00Z, verbatim ***"Yes, with disposition + carry-forward
      issue"***, recorded at
      https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5686436893.
      `archive_change()` refuses every `^- [ ]` in `tasks.md` (`change has
      incomplete tasks`; `scripts/proposal-support.py`) with no per-section
      exception, so the archive pull request ticks § 4.5 `[x]` with its
      disposition beneath (*not performed; carried as openxFactory#<carry-
      forward issue>*) — the `add-signed-execution-chain` precedent, whose
      § 4.5 was carried at openxFactory issue #534 (filed 2026-08-31 at its
      archive) and whose requirement 9 reached canon MEETING ITS OWN DEGRADED
      CASE rather than evading it, the capability conferring and refusing
      NOTHING until a named reader runs as a required check. The same is true
      here: an unrequired arrival gate refuses no landing. **WHAT THE ARCHIVE
      PULL REQUEST STILL OWES**, beyond this file: the four realization merges
      by number and sha (#1038 → `701c8fde`, #1037 → `8f393758`,
      #1039 → `92d519b0`, and slice 6's own), `pytest-suite`'s own run ON EACH
      MERGE COMMIT cited by run id with its counts line, the four requirement
      titles grepped against canon (three absent, *Origin retention at
      archive* present and byte-identical to the MODIFIED block's restated
      half), and `openspec validate --all --strict` showing the two
      pre-existing failures and no third. **Filing the carry-forward issue is
      the orchestrator's act on Brett Heap's word, not an author's.**
- [ ] 7.2 **THE GOVERNING ISSUE CLOSES AT THE ARCHIVE PULL REQUEST AND NOWHERE
      ELSE — AND ONLY ON BRETT HEAP'S WORD.** openxFactory #1003 stays OPEN by
      his ruling of 2026-09-13; whether and when it closes is his call and not
      this packet's. No commit message, body or reply on this packet's branches
      carries a closing keyword against it in any form.
      **HE HAS NOW SAID WHEN, AND IT IS EARLIER THAN THIS BOX'S OWN WORDING —
      THE DEPARTURE IS NAMED RATHER THAN PAPERED OVER.** Brett Heap,
      2026-09-15T19:0xZ, by multiple choice in this lane's window, verbatim
      ***"Close when #1041 lands"***, recorded at
      https://github.com/opensoft/openxFactory/issues/1003#issuecomment-5686628685:
      the governing issue closes when slice 6 lands, and the § 4.5 ruleset act
      with its canary, plus the archive, are tracked on this packet and on the
      Q2 carry-forward issue. This box reads *"AT THE ARCHIVE PULL REQUEST AND
      NOWHERE ELSE"*; his ruling puts the closing at slice 6's landing, which
      is BEFORE the archive. It is his call — the box says so in its own second
      sentence — and it is written down here so a reader of the archived packet
      is not left to reconcile the two alone. **THE BOX STAYS OPEN**: the act
      has not happened, it is the orchestrator's on his word, and nothing on
      this branch carries a closing keyword against #1003 in any form.
