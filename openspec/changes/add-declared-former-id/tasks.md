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

## 3. The archive gate — REALIZATION

- [ ] 3.1 **RESOLVE THE BASELINE ACROSS THE DECLARED IDENTITIES.**
      `proposal-support.ratifying_commit` takes the current id and every
      declared former id, resolves each to the path it occupies at the commit
      being read by the rule `sequenced_after.proposal_path_at_ref` already
      implements, and returns the EARLIEST commit at which any of them declares
      `Status: ratified`.
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
- [ ] 4.2 **REFUSE THE UNDECLARED ARRIVAL.** Status `former-id-undeclared`,
      exit 1, naming the commit, the source path, the destination path and the
      one repair. **No bypass flag** (#690).
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
