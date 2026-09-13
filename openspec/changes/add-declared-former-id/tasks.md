# Tasks: add-declared-former-id

Status: draft

**NOTHING BELOW IS TICKED, AND THAT IS THE STATE OF THE WORK RATHER THAN AN
OVERSIGHT.** This pull request files a proposal. It edits no file under
`openspec/specs/`, adds no script, no validator, no register and no test, and
changes no behaviour of anything that runs. § 1 is decided by a ratification act
that has not happened; § 2 through § 5 are realization slices that follow it.

## 1. Ratification — OWED, NOT GIVEN

- [ ] 1.1 **RULE `design.md` D1 — where the declaration lives.** Recommended:
      a top-level `former_ids:` key in the packet's own `.openspec.yaml`, a
      SIBLING of `origin:` and never a member of it. The alternatives and their
      costs are written out in D1; option (c), an estate-level register in the
      shape of `contracts/policies/repository-identity.yaml`, is the one a
      reader is most likely to prefer and the reasons it is not taken are
      stated there.
- [ ] 1.2 **RULE `design.md` D2 — the declaration names change IDS, not paths**,
      ordered oldest first and appended to rather than rewritten.
- [ ] 1.3 **RULE `design.md` D3 — the fail-closed refusal is taken by a house
      validator at the landing**, not by the archive gate and not as a
      `doc-health` finding, with the two refusal statuses, the two arms and the
      archive-relocation exception as D3 states them.
- [ ] 1.4 **RULE `design.md` D4 — no `doc-health` delta in this packet**, the
      reporting sweep being a successor with its own numeral. A veto here adds
      a `## MODIFIED Requirements` block over *Deterministic check families*
      and a registry edit, and D4 prices both.
- [ ] 1.5 **RULE `design.md` D5 — *Origin retention at archive* is MODIFIED**
      rather than left standing beside an ADDED requirement that contradicts it.
- [ ] 1.6 **RATIFY THE TEXT, OR NAME WHAT MOVES.** Ratification is Brett Heap's
      word and is a separate act from this landing. The record is a
      `review/ratification-<date>.md` carrying the verbatim word and its
      recording URL, and `.openspec.yaml` then takes `approved_by` and
      `approved_on` ADDED BESIDE the drafting provenance, `kind` and `id`
      unmoved.

## 2. The declaration and its reader — REALIZATION

- [ ] 2.1 **WRITE THE GRAMMAR.** `former_ids:` — a top-level sequence of change
      ids in `openspec/changes/<id>/.openspec.yaml`, oldest first. Refuse: a
      scalar where a sequence is required; an entry that is not a change id by
      the grammar `ratifying_commit` already enforces
      (`[A-Za-z0-9][A-Za-z0-9._-]*`); an entry equal to the packet's own id; a
      duplicate entry; an entry nested inside `origin:` rather than beside it.
- [ ] 2.2 **PIN THE SIBLING PROPERTY WITH A TEST**, not with a comment: a
      `.openspec.yaml` carrying `former_ids:` must yield an
      `origin_block_lines` reading identical to the same file without it, so a
      lawful move is never a mutation of the frozen origin declaration. The
      authoring measurement is `design.md` M3; the test is what keeps it true.
- [ ] 2.3 **REFUSE A DECLARED ID THAT STILL STANDS.** A former id carried by a
      live packet directory at the commit that declared it is a claim to be the
      move of something that did not move; refuse naming both ids.
- [ ] 2.4 **BIND EVERY NEWLY ADDED ENTRY TO THE MOVE THAT COMMIT PERFORMS.**
      Absence of a live directory is NOT proof of predecessorship — an archived
      id and an id that never existed both lack one — so the entry a commit adds
      must be exactly the source of the move that commit performs, and a commit
      that adds a former id while moving nothing into this packet is refused.
      Fixtures: a standing packet appending an archived id; a standing packet
      appending an id that never existed.
- [ ] 2.5 **ENFORCE APPEND-ONLY ACROSS COMMITS, NOT ONLY WITHIN ONE.** Compare
      the list against the one the packet carried at the commit's parent and
      refuse a commit that removes, reorders or respells an established entry,
      whether or not that commit moves anything. Fixtures: a declaration deleted
      the day after a lawful move (the attack that would hand the archive gate
      the later ratification under the current id, in a commit no arrival check
      looks at); an entry reordered; an entry respelled.
- [ ] 2.6 **REFUSE A FORMER IDENTITY CLAIMED TWICE.** Two packets declaring the
      same former id, or an id that is at once a live packet id and a declared
      former id, is refused naming every claimant — an identity claimed twice
      resolves to a set, and a baseline chosen from a set is chosen by the
      resolver rather than by an author. Fixture: two claimants; a live id also
      declared as somebody's former id.

## 3. The archive gate — REALIZATION

- [ ] 3.1 **RESOLVE THE BASELINE ACROSS THE DECLARED IDENTITIES.**
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
- [ ] 3.1a **REFUSE AN IDENTITY THAT RESOLVES TWICE.** Where the current id or a
      declared former id matches more than one candidate location in the tree
      being read, refuse CANNOT RUN naming the candidates rather than taking the
      first sorted one. The estate's own `archived_change_dirs` already states
      the rule — it returns a LIST because "two archive dates for one id is an
      AMBIGUITY the resolver must be able to report, not a collision to resolve
      by taking the newest" — and `proposal_path_at_ref` does not carry it at a
      ref.
- [ ] 3.2 **LEAVE THE UNDECLARED REFUSAL EXACTLY WHERE IT IS.** PR #846's
      `origin-retention-path-moved` refusal stands unchanged for a packet that
      declares nothing; what changes is that a packet which DOES declare now has
      a lawful answer.
- [ ] 3.3 **DO NOT MOVE THE COMPARISON.** The origin block must still equal the
      declaration at the resolved baseline exactly; the support manifest's
      repeated origin fields are still measured against it; an accepted mutation
      still takes the explicit disposition. Add the test that proves a declared
      move carrying an origin edit is refused as a MUTATION — the laundering
      case.
- [ ] 3.4 **FAIL CLOSED ON EVERY READ BEHIND THE BASELINE.** Presence read from
      the tree; content read separately; a read that could not be performed
      raised as CANNOT RUN naming the read and the identity it was for. Never
      report an unreadable history as an unratified one. `design.md` M1 is the
      measurement; PR #1024's retained branch `2bc60386` carries a worked
      version of this half and is a candidate to lift.

## 4. The landing validator — REALIZATION

- [ ] 4.1 **BUILD THE READER AND THE CLI** in the shape
      `gate-realization-axis-vocabulary` established: a module under `scripts/`,
      a validator CLI beside it, a test suite over the live corpus.
- [ ] 4.2 **REFUSE THE UNDECLARED ARRIVAL, QUALIFIED BY THE SOURCE'S HISTORY.**
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
- [ ] 4.2a **READ THE SOURCE'S WHOLE DECLARED LINEAGE, NOT ITS ID ALONE.** The
      "ever ratified" test covers the source packet's own id TOGETHER WITH every
      id it declares in `former_ids:` at the commit's parent — otherwise a
      packet that already moved once lawfully (X ratified, X→Y declared and
      returned to draft, then Y→Z) passes its second landing on Y's own empty
      history and stands with no lineage. This is ONE blob at ONE commit and not
      a history walk. Fixture: the three-id chain, refused at the second hop.
- [ ] 4.2b **REQUIRE THE ARRIVING LIST TO BE THE SOURCE'S LIST PLUS THE SOURCE
      ID**, in the source's own order. A move that drops an entry the source
      declared sheds a lineage, which is the same defect as never declaring one.
      Fixture: a declared move whose destination omits an inherited entry.
- [ ] 4.3 **EXCEPT THE ARCHIVE RELOCATION BY ID.**
      `openspec/changes/<id>/` to `openspec/changes/archive/<YYYY-MM-DD>-<id>/`
      with the id unchanged passes with no declaration.
- [ ] 4.4 **FAIL CLOSED ON THE ARRIVAL READ.** Where the pairing cannot be
      computed AND the tree shows both a packet directory arriving and one
      leaving in that commit, refuse `former-id-arrival-unreadable`, exit 2,
      CANNOT RUN, naming the read. Do NOT pair from the tree: a commit that
      withdraws one packet and creates an unrelated other has the same shape.
- [ ] 4.5 **REGISTER IT AS A REQUIRED CHECK** and record the run it adds.

## 5. The reference resolver and the documents — REALIZATION

- [ ] 5.1 **RESOLVE A PACKET REFERENCE BY IDENTITY.** By change id — against the
      location that id occupies now, active or archived, and against any packet
      declaring it as a former id — reaching citations written as
      `openspec/changes/<id>/<file>` paths, whose second segment names the
      packet. A reference that resolves owes the citing record no edit.
- [ ] 5.2 **LEAVE THE CROSS-REPOSITORY CASE OUT OF SCOPE ON THE TREE BEING
      READ**, a reference to another repository's packet being no evidence about
      that reference.
- [ ] 5.1a **RESOLVE BOTH HALVES OF A PACKET-RELATIVE CITATION.** The location
      the identity resolves to must also carry the remainder the citation names;
      an identity that resolves to a packet not carrying the cited file is
      DANGLING, reported against the FILE and not against the packet. Resolving
      the identity alone would accept a citation to a file deleted, renamed or
      never written. Fixtures: a live id with a deleted remainder; an archived id
      whose remainder moved inside the packet.
- [ ] 5.2a **REPORT AN AMBIGUOUS REFERENCE RATHER THAN RESOLVING IT.** An id
      that would resolve to more than one candidate is AMBIGUOUS, and the defect
      belongs to the declaration that made one identity resolve twice rather
      than to the citing record. Never settle it by sort order.
- [ ] 5.3 **AMEND `docs/document-lifecycle.md`.** Its sentence *"Renaming a
      ratified change is therefore blocked until a change declares a FORMER ID
      (issue #833, a successor packet)"* is the sentence this packet answers; it
      must then say what a declared move requires instead of saying the act is
      blocked. Nothing else in that paragraph moves.
- [ ] 5.4 **RE-MEASURE THE DANGLING-CITATION POPULATION ON THE REALIZATION
      TREE** and record it there. `design.md` M4's figures (94 dangling, 58
      resolvable by id) were taken at `9378eca5` and are history by the time the
      resolver lands.

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
- [ ] 7.2 **THE GOVERNING ISSUE CLOSES AT THE ARCHIVE PULL REQUEST AND NOWHERE
      ELSE — AND ONLY ON BRETT HEAP'S WORD.** openxFactory #1003 stays OPEN by
      his ruling of 2026-09-13; whether and when it closes is his call and not
      this packet's. No commit message, body or reply on this packet's branches
      carries a closing keyword against it in any form.
