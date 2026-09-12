#!/usr/bin/env python3
"""Verify `docs/opendox-carve-manifest.yaml` — FLOOR PART 1 of the RULED
four-part floor for the openDox/openXdox carve.

WHAT THIS FILE IS. `split-opendox-two-layer-product` § D6 (RULING OQ-1, `#656`
comment `5547060378`) replaced the openXwallet extraction's byte-identity floor,
which is unavailable here, with a four-part floor whose FIRST part is a mapping
manifest: one row per file under the moved paths, carrying its `openxFactory`
path, its `sha256` at the NAMED CARVE COMMIT, its destination repository and
path, and one of exactly three dispositions. The ruling's own sentence is the
whole requirement this file enforces — **"a file in no row, or an edit in no
class, is an UNDECLARED MOVEMENT and the carve REFUSES"** — and a manifest that
nothing checks is a claim, not a floor.

THE MANIFEST DOES NOT EXIST YET, AND THAT IS NOT A FAILURE. It is authored AT
the carve commit (the § 6 ceremony) and lands after it, so this validator is
landed BEFORE its subject. Given no manifest AT THE DEFAULT PATH it
prints `NO MANIFEST <path> (nothing to validate)` and exits 0. That is a
deliberate seat-holding pass and the one place here that is not fail-closed: the
alternative is a red suite for every pull request between this file and the
carve, which would train the lane to ignore it. It applies to the DEFAULT path
ONLY — a `--manifest` the caller NAMED and that is not there refuses
(`carve-unreadable`), because otherwise the one not-fail-closed branch in this
file is the branch a typo selects and a mistyped path is green forever.
Everything after the manifest appears is fail-closed.

SIX ORDERED CHECKS, FIRST FAILURE WINS (the scout memo § 1.3, 2026-09-08).
Two of them read the revision under test and therefore read `phase:` — see
"THE TWO PHASES" below; the other four are phase-blind.

  1. SHAPE — `schema_version` (the INTEGER 1, so neither `true` nor `1.0`
     passes), `kind`, the three consts, a 40-lowercase-hex `carve_commit`, a
     label `carve_tag`, the closed maps and lists, the CLOSED top-level and
     per-disposition key sets, and the per-disposition required keys
     (`carve-shape-invalid`). Two arms here carry their own codes because the
     defect they name is not a typo: `re_destined:` on a `not_moved` row is
     `carve-re-destined-not-moved` — there is no arrival to re-place — and a
     `re_destined:` without `ruling:` is `carve-re-destined-unruled`, RULED Q6
     having scoped the form to a RULED mis-placement only.
  2. REVISION — `carve_commit` must name a COMMIT OBJECT THIS REPOSITORY
     CARRIES (not an annotated tag's object id, which is also 40 hex and which
     git would peel silently) and be an ANCESTOR of the REVISION UNDER TEST
     (`HEAD`, or `--at <sha>`), by `git merge-base --is-ancestor`
     (`carve-revision-mismatch`). Identity is the trivial ancestor case, so
     the ceremony's own run at the carve commit still passes. What this
     refuses is a referent the tested revision does not descend from —
     another tree's commit, against which every comparison below would be
     measuring two unrelated histories.
  3. DIGEST — TWO comparisons per moved row, in TWO passes over the rows, and
     the order between them is itself a finding. PASS 1, at `carve_commit` (the
     referent the row claims): recompute the sha256 of the RAW GIT BLOB and
     compare it and the `git_mode` the tree carries against what the row
     records (`carve-digest-mismatch`); a path the referent does not carry is
     `carve-path-absent`. That is the manifest lying about its OWN referent — a
     document defect its author fixes, and it outranks anything the tree did
     afterwards. PASS 2, at the revision under test: the blob and the mode
     there must still be the referent's (`carve-digest-mismatch`, worded
     CHANGED SINCE THE CARVE), and a path deleted since the carve is
     `carve-path-absent` worded the same way. Pass 2 IS the memo's § 6 step 3 —
     "a file changed on main between the manifest and the move surfaces as
     `carve-digest-mismatch` on the next pull request" — and it is where that
     pressure lives now that check 2 no longer demands identity. The referent
     blob is in hand from pass 1, so `edits[].lines` are also bounded by its
     line count (`carve-shape-invalid`): a line past EOF at the carve commit is
     not the falsifiable claim the line numbers are carried for.
  4. SURFACE COMPLETENESS — walk `git ls-tree -r` under every `moved_paths:`
     prefix at BOTH revisions. At `carve_commit`: every prefix must match at
     least one file (`carve-surface-vacuous`), every file there must appear in
     EXACTLY one row, no row may name a path outside that surface
     (`carve-path-absent`), and no two rows may arrive at one destination path
     (`carve-file-undeclared` / `carve-file-duplicated`). Then the same
     completeness question at the revision under test, which is the tree the
     carve would actually run against: a file that has APPEARED under the
     surface since the carve is in no row and refuses as
     `carve-file-undeclared`, and a ROW whose path has been DELETED since the
     carve refuses as `carve-path-absent` — the latter is what catches a
     `not_moved` row, which the digest loop never reads. This is
     `validate-openreposhape-pin.py`'s check 5 re-aimed, and it is the ruling's
     "a file in no row" sentence as running code — the one failure mode per-file
     digests cannot see, because they say nothing about a file nobody listed.
  5. CLOSED VOCABULARIES — `disposition`, `edits[].class`, `destination`,
     `also_replicated_to[]`, `re_destined.from`, `re_destined.to` and `reason`
     are each membership-tested against a closed list
     (`carve-vocabulary-unknown`).
  6. DISPOSITION CONSISTENCY — `moved_with_declared_edit` with no `edits:` is
     `moved_verbatim` mislabelled; `moved_verbatim` with `edits:`, or
     `not_moved` with `edits:` under any reason but
     `replicated_at_destination`, is a contradiction
     (`carve-disposition-inconsistent`); so is a moved row that lists its OWN
     `destination` in `also_replicated_to:`, and so is a `re_destined:` whose
     `from`/`from_path` are not the row's own `destination`/`destination_path`
     or whose `to` equals its `from`. A row whose `(to, to_path)` is another
     row's `(from, from_path)` is a CHAIN and refuses
     `carve-re-destined-chain`. Then the rows' file order must equal their
     bytewise-UTF-8 sort, which is what the const `path_order: bytewise_utf8`
     claims (`carve-path-order-violation`).

THE TWO PHASES, AND WHY THE DECLARATION IS IN THE MANIFEST (`phase:`). This
document outlives the tree it describes by exactly one act: § 5.2, the shed,
deletes every MOVED row's source path and the one `deleted_at_carve` row — 319
paths of the 456 — and from that commit onward checks 3 and 4 are asking a
question the tree can no longer answer. As written they REFUSE it, twice and by
name (`carve-path-absent` from check 3 pass 2 for the 318 moved rows, and from
check 4's `vanished` arm for all 319), which is correct while the shed has not
been ruled and useless the moment it is.

`phase:` is the OPTIONAL top-level key that says which of the two questions
this manifest is asking. Absent, or `carve`, is the file as landed: every row's
source path is still here. `post-shed` says § 5.2 has run, and it changes
EXACTLY two arms:

  * check 3 pass 2, for a MOVED row: absence is the declared outcome, and
    PRESENCE is the finding (`carve-shed-incomplete`).
  * check 4, for the whole surface: the shed set — derived from the rows
    themselves, never from a second list — is excluded from `vanished` and
    required to be absent by its own mirror arm.

EVERYTHING ELSE IS UNTOUCHED IN BOTH PHASES, and that is the point of putting
the switch this narrow. Check 2 still requires `carve_commit` to be a commit
object this repository carries and an ANCESTOR of the revision under test — the
shed deletes files from a tree, it does not delete a commit from a history, so
`git cat-file blob b075fd91:<path>` answers after the shed exactly as before.
Check 3 PASS 1 therefore still recomputes all 318 digests from the referent's
real bytes and still bounds all 910 declared lines against them; check 4 still
walks the referent for completeness, still refuses a file that has APPEARED
under the surface, and still requires every `stays_*` and
`replicated_at_destination` row to be PRESENT; checks 1, 5 and 6 never read the
tree at all. The manifest keeps `carve_commit: b075fd91…` and `carve_tag:
opendox-carve-0`, every `sha256` and every disposition: `post-shed` is not a
re-cut and moves no digest.

WHAT `post-shed` GIVES UP, STATED PLAINLY, because a floor that overstates its
reach is worse than one that does not reach. For the 318 MOVED rows only, it
stops asking "has this file drifted on `main` since the carve" — the memo's § 6
step 3 pressure. It cannot be asked of a deleted file by any tool, and the
answer it was buying is discharged once and elsewhere: at the four
destinations, by `verify-carve-arrival.py`, against blobs read at
`carve_commit` from this repository's own history — which the shed does not
touch. The 137 rows that stay keep every guarantee they had.

AND THE DECLARATION IS SYMMETRIC, which is what makes it a floor rather than a
mute. A `post-shed` manifest over a tree that still carries a moved row refuses
`carve-shed-incomplete`. So the phase cannot be flipped ahead of the deletions
to buy quiet, and the deletions cannot land ahead of the phase without
refusing: runbook § 8's "no ordering of two commits leaves a green
intermediate" stops being a discipline the lane is asked to keep and becomes
the thing this file checks.

TWO GRAMMAR EXTENSIONS, RULED Q-L7 (a) (Brett Heap, 2026-09-10, verbatim "rule
Q-L7 (a)"; `#656` comment `5618683833`). Carve leg 1 landed and measured two
facts the grammar as first written could not hold, both about the SAME pair of
test-layout files, and the ruling amends the grammar once rather than twice:

  * `also_replicated_to: [<destination key>, …]` ON A MOVED ROW. A row was
    either MOVED (to exactly one destination) or REPLICATED (at every
    destination, naming none). `tests/ideation-dashboard/conftest.py` is one of
    the replica rows and arrives at BOTH `-code` legs; it imports
    `session_fixtures` unconditionally (`:106`), and
    `tests/ideation-dashboard/session_fixtures.py` is a MOVED row to
    `opendox_code` alone — so collecting `tests/` at openXdox-code would fail
    at import, on a file no row placed there. The optional list says the row's
    bytes ALSO arrive, as a replica on RULED OQ-A's terms, at the destinations
    it names. It adds NO arrival path: a replica's placement is the leg's
    (RULED OQ-C — "this manifest declares what LEAVES, not what the destination
    assembles") and is declared to `verify-carve-arrival.py` with
    `--replica-at`, which is why check 4's arrivals map is untouched by it.
  * `edits:` ON A `replicated_at_destination` ROW. A replica was byte-identical
    by construction and declared no line. The same conftest replica arrives at
    `tests/conftest.py`, ONE DIRECTORY SHALLOWER than its source, so its `:25`
    `REPO_ROOT = HERE.parent.parent` points outside the destination repository
    (391 node-gated errors, measured in leg 1's full suite) and must read
    `HERE.parent` at every replica. The lines are the carve commit's, bounded
    by the source blob at `carve_commit` in check 3 exactly as a moved row's
    are, and the class vocabulary is the same closed three. The edit is
    APPLIED IDENTICALLY AT EVERY REPLICA — a claim about lines, which is what
    this grammar can bound; see `verify-carve-arrival.py`'s own docstring for
    what that does and does not prove at the destination.

  It is NOT the FLOOR PART 2 field. RULING OQ-K's clause (b)
  (`split-opendox-two-layer-product` design § D6 (2)) owes FLOOR PART 1 a field
  on a TEST-BEARING replica row naming the set of REPOSITORIES its copies land
  in, including the retained openxFactory one, so that
  `Σ over replicated rows of (m − 1) × row_test_count` is computable. The
  packet names no spelling for it and this amendment does not author it: both
  files here carry ZERO `def test_` at `carve_commit` (measured), so neither
  enters that Σ and neither clause is realized by this act. `also_replicated_to`
  names `destinations:` KEYS for arrival admission; the owed field names
  repositories for an arithmetic. They can coexist on one row without either
  meaning the other.

THE THIRD GRAMMAR EXTENSION, RULED Q6 (Brett Heap, 2026-09-12, by interactive
multi-choice; `#656` comment `5648044785`, adopting verbatim the RECOMMENDED
answer of openDox-spec `docs/front-end-package-boundary.md` § 6 Q6 at
`7d12428c`). It is THE FIRST EXTENSION ABOUT PLACEMENT, which is exactly why it
needed a ruling of its own and could not be assumed from Q-L7 (a)'s precedent —
that ruling's own sentence about its two fields is "neither of them a fourth
disposition and NEITHER OF THEM A PLACEMENT".

  `re_destined: {from, from_path, to, to_path, ruling, note}` ON A MOVED ROW,
  OPTIONAL. It says: this row's bytes were placed at `from:from_path` by the
  carve, a RULING has since moved that placement, and the arrival the floor
  now asks about is `to:to_path`. `from` is the row's own `destination` and
  `from_path` its own `destination_path` — the row keeps both, unedited, so
  the manifest never stops recording where the carve actually put the file —
  and `to` is a `destinations:` key that is NOT `from`.

  WHAT DOES NOT MOVE, and the list is the ruling's: `carve_commit`,
  `carve_tag`, every `sha256`, every `git_mode`, the row's `disposition`, its
  `edits[]` and the lines they name. A digest is a claim about the SOURCE blob
  at `b075fd91…` and where the file now lives says nothing about it; a
  declared line is bounded by that same blob in check 3 and is untouched here.
  An import rewrite the new leg needs is an ORDINARY declared line under the
  existing `import rewrites` class, so `edit_classes` stays closed at three,
  `destinations:` stays closed at five and the disposition list stays three.

  WHAT S8 NEEDS IT FOR. § 1.2(d) of the boundary note measured 23 test files at
  openXdox-code naming a `views/<name>.js` path under a directory openXdox-code
  does not have: RULED OQ-G's TEST HOMES rule placed them by a rule about
  imports and they landed where nothing can run them. Re-homing such a file is
  a change of DESTINATION on an already-arrived row, and no field of the row
  grammar could express it — `edits: [{class, lines[]}]` is a claim about BYTES
  ON A LINE, never about placement, which the manifest's own amendment records
  say three times. Slice S6 met the same wall on ONE file and withdrew rather
  than work round it (openXdox-code `657c821b`); S8 is forty-eight.

  WHY NOT A RE-CUT. Runbook § 11 re-cuts at a NEW `carve_commit` with every
  digest RECOMPUTED and re-emits the manifest "at that commit, as the last
  thing on that tree" — and this manifest is `phase: post-shed`, so a manifest
  re-emitted at a post-shed commit would carry NO MOVED ROWS AT ALL. It would
  be a different document, not a re-cut. Three costs stand even setting that
  aside: re-cutting is Brett Heap's own act (§ 12 act 5); § 11 step 6
  re-verifies EVERY already-arrived leg, because a leg proved against a
  superseded referent is proved against nothing; and § 11's trigger is a
  SOURCE-SIDE fact — "if `main` moves under the carve", with the digests wrong
  — while S8's fact is destination-side and is a correction to a RULED
  placement. Correcting a ruling is DECLARED, not re-cut, and a re-homed file
  never leaves its row, which is what keeps the floor's own sentence true.

  THE FIVE REFUSALS, AND WHICH CHECK OWNS EACH. `re_destined:` on a `not_moved`
  row is `carve-re-destined-not-moved` in check 1 — a row that declares no
  destination has no arrival to re-place, and the reasoning is
  `also_replicated_to:`' own one level down. A `re_destined:` with no `ruling:`
  is `carve-re-destined-unruled`, also in check 1: the ruling's scope answer is
  that the form serves a RULED mis-placement and nothing else, so the citation
  is the one field whose absence is a governance defect rather than a typo, and
  it is required PRESENT and non-empty — its FORM is not constrained, because a
  citation may legitimately be a comment id, a `#656` reference or a pull
  request URL and refusing one of those would be this file inventing a rule the
  ruling did not make. `from`/`to` outside `destinations:` is check 5's
  `carve-vocabulary-unknown`, the same membership test and the same reason a
  row's own `destination` gets one. `from`/`from_path` disagreeing with the
  row's own destination, and `to == from`, are check 6's
  `carve-disposition-inconsistent` — a row contradicting itself. And a CHAIN —
  a row whose `(to, to_path)` is another row's `(from, from_path)` — is check
  6's `carve-re-destined-chain`: a row already re-destined is AMENDED IN PLACE,
  never re-destined twice, so one row never needs two readings and no reader
  has to compose two hops to learn where a file is.

  CHECK 4 READS THE EFFECTIVE ARRIVAL AND CHECK 3 DOES NOT. The duplicate-
  arrival map is keyed on `(repository, leg, path)` at the destination the row
  arrives at TODAY, because that is the collision it exists to refuse: without
  it, a row re-destined AWAY from a path would go on reserving it — so a
  second row moving to the vacated path would refuse as a duplicate — while a
  re-destined row landing on an occupied path would pass in silence, which is
  the two errors this check exists to prevent, in both directions at once. The
  SURFACE walk is untouched: it is a claim about SOURCE paths, and a
  re-destination moves nothing at the source.

WHY CHECK 2 IS ANCESTRY AND NOT IDENTITY (AMENDED 2026-09-09, before the
manifest was authored). As landed, check 2 required the revision under test to
RESOLVE TO `carve_commit`, on the § 6 ceremony's own sentence that the manifest
is "the LAST thing on that tree". That is UNSATISFIABLE in every run this
validator actually gets: a pull request's CI checks out a synthetic MERGE REF,
a commit no manifest can ever name, and the manifest's own landing makes
`main`'s tip the manifest's squash — also never `carve_commit`. The manifest's
own pull request could therefore never have gone green, and the § 8.2 seat
(`test_the_real_repository_answers_at_the_ruled_path`, which asserts `OK` from
the moment the file exists) would have redded the required suite for every lane
from the moment it landed.

The ceremony's intent is not identity. It is that a file which moves between
the manifest and the carve must REFUSE, BY NAME. Identity was one way to buy
that, and it bought it by refusing every revision as well — a gate that cannot
tell a changed file from a changed repository is a stopped clock, right twice
and never usefully. Ancestry, plus check 3's pass 2 and check 4's second walk,
buys exactly the refusal and nothing else: `carve_commit` must be in the tested
revision's history, and every declared path must still be — byte for byte and
mode for mode — what the manifest says it was at the carve. A tree that has
moved UNDER THE SURFACE still refuses, naming the file; a tree that has moved
anywhere else does not.

THE MANIFEST'S OWN LANDING CANNOT TRIP CHECK 4. The manifest lives at
`docs/opendox-carve-manifest.yaml` and `docs/` is not a `moved_paths:` prefix —
the surface is `scripts/ideation_dashboard/`, `tests/ideation-dashboard/` and
their siblings (memo § 2.1). So the commit that adds the manifest adds a file
OUTSIDE the surface, which check 4 does not walk and no row needs to declare.
That the ruled path is outside its own surface is load-bearing for the
ceremony rather than merely tidy: a manifest inside the surface it declares
would be, the instant it landed, a file under the surface no row declares.

WHY THE VOCABULARIES ARE CLOSED IN CODE AND NOT IN A SCHEMA UNDER `contracts/`.
The three dispositions and the three edit classes are Brett Heap's ruling,
verbatim, and `edit_classes:` is asserted EQUAL to `EDIT_CLASSES` below rather
than merely read from the file — a manifest that declares its own fourth class
would otherwise validate against itself. The packet had proposed a fourth class
("vocabulary parameterization"); the ruling does not carry it, so it is not here.
`not_moved_reasons:` is the one vocabulary the ruling did NOT author (RULED OQ-C,
2026-09-09: the disposition list stays three and the REASON carries the nuance),
so the file declares its own list and this validator requires it to be a SUBSET
of `KNOWN_NOT_MOVED_REASONS` — declared-and-known, so neither a typo nor a
silently widened vocabulary passes.

WHY NO SCHEMA FILE SHIPS WITH THIS. A new artifact under `contracts/` fires
`release-tag-gate` and the digest inventory; this validator is one file with its
shape checks in code, which is also the precedent
`validate-openreposhape-pin.py` sets for a pin-like claim with exactly one
instance.

THE DIGEST FIELD IS `sha256: "<64 hex>"` AND THE PRECEDENT'S IS
`digest: sha256:<hex>`. The divergence originates in the scout memo § 1.2, whose
row example this validator implements verbatim; the two documents' digest fields
are therefore NOT interchangeable, and this is recorded rather than corrected
because the manifest author follows the memo (a change of field shape is the
memo's to make, not this validator's).

TWO `destinations:` KEYS SHARING ONE `{repository, leg}` BODY DO NOT REFUSE ON
THEIR OWN (S8, RE-VERIFICATION of `d97371d1`, 2026-09-09, which asked the
question). A redundant alias is harmless BY ITSELF: `destinations:` is a
document-level fact, and nothing about the document alone says whether any row
ever exercises both keys in a way that collides at the destination. Whether it
does is a claim about the ROWS' arrivals — check 4's question — and refusing it
in check 1 would decide check 4's question with check 1's information, on the
same reasoning check 5 and not check 1 owns whether a row's `destination` names
a real key at all. It would also make check 4's own fix UNREACHABLE: check 1
always runs first, so a shape-level refusal on the body alone would mean no
manifest carrying two same-body keys ever reaches `check_surface`'s arrivals
check again, leaving that check's fix — keying the duplicate-arrival check on
the real `(repository, leg, destination_path)` rather than on the alias
`(destination, destination_path)`, which is the S8 fix itself — provably
correct but permanently untested by any subprocess run of this file, which is
how every behavioural test in `tests/carve_manifest/test_carve_manifest.py` is
required to run. The fix stays in `check_surface`, where the question it
answers actually lives.

WHERE THE MANIFEST LIVES. `docs/opendox-carve-manifest.yaml`, the path § 3.1 and
§ D6 name verbatim, RULED OQ-E (2026-09-09) after the scout measured that `docs/`
holds no other machine-validated YAML in this repository. The break with the
convention is honoured, not corrected, and the manifest's own `header:` records
it.

Exit codes:
  0  the manifest verifies, or there is no manifest yet
  2  ANY refusal, and any environment failure

  There is deliberately NO exit 1, on `validate-openreposhape-pin.py`'s
  reasoning: the gate's only question is "may this carve proceed", and the answer
  is the same for "a digest drifted" and "the bytes could not be read". A
  two-valued failure invites a caller that treats one of them as a warning.

Run: `python3 scripts/validate-carve-manifest.py`; driven on every required-suite
pass by `tests/carve_manifest/test_carve_manifest.py`, which is the § 8.2 seat.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, NamedTuple

try:
    import yaml
except ImportError:  # pragma: no cover - the repository ships PyYAML
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

# THE FLOOR'S ONE DEFINITION OF A LINE (RULED Q-L8 (c)), shared with
# `verify-carve-arrival.py` so that a declared line number means the same thing
# where it is BOUNDED and where it is CHECKED. `scripts/` goes on the path
# because both tools are hyphenated entry points their own tests load by
# `spec_from_file_location`, where Python inserts nothing; GUARDED and therefore
# idempotent, on `scripts/proposal-support.py`'s idiom and for its stated
# reason — a test module that loads this file more than once in one process
# would otherwise prepend a duplicate entry each time and move import
# precedence under everything else in the session.
_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import carve_lines  # noqa: E402
# `_git()` below reuses `carved_reach._sanitized_git_environment()` — safe to
# import bare for the same reason `carve_lines` is: both live directly in
# `scripts/`, which the block above already guarantees is on `sys.path` in
# every context this file is loaded from, invoked-as-script or
# `spec_from_file_location`.
import carved_reach  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# The ruled path, § 3.1 and design.md § D6 verbatim (RULED OQ-E). Relative, so
# `--repo` moves the whole question to another tree without moving the path.
MANIFEST_RELPATH = "docs/opendox-carve-manifest.yaml"

SCHEMA_VERSION = 1
KIND = "opendox-carve-manifest"

# The three consts of the row grammar, borrowed from the release-digest
# inventory (`contracts/releases/release-digest-inventory.schema.yaml:19-42`) so
# a reader of one document already knows how to read the other.
CONSTS: dict[str, str] = {
    "digest_algorithm": "sha256",
    "digest_source": "raw_git_blob",
    "path_order": "bytewise_utf8",
}

# RULED, three and not four. Order included: "the ruling's own, VERBATIM".
EDIT_CLASSES: tuple[str, ...] = ("import rewrites", "path constants",
                                 "adapter calls")

# THE TWO PHASES OF THIS DOCUMENT'S OWN LIFE, declared IN the manifest and not
# on a command line. The manifest is the floor's referent, and a phase passed
# by a caller would mean the same tree verifies or refuses depending on which
# job invoked the tool — the one property a floor may not have. Declared here,
# the check is self-describing: the file says which semantics it is asking for,
# every caller of every kind reads the same answer, and the flip is a reviewable
# line in the same diff as the deletions it licenses (runbook § 8's "one atomic
# pull request", enforced rather than asked for).
#
#   `carve` (the DEFAULT, and what an absent key means) — the tree still
#   carries every row's source path. This is the file as landed at #865.
#
#   `post-shed` — § 5.2 has run. Every MOVED row's source path, and the one
#   `deleted_at_carve` row's, is ABSENT at the revision under test BY
#   DECLARATION; every `stays_*` and `replicated_at_destination` row's is still
#   PRESENT, and still checked exactly as before.
#
# IT IS SYMMETRIC, WHICH IS WHY IT IS A FLOOR AND NOT A MUTE. Under `post-shed`
# a moved row whose file is STILL THERE refuses `carve-shed-incomplete`, so the
# declaration cannot be flipped ahead of the deletions to buy silence: a
# half-shed tree refuses in exactly the way a pre-shed tree with a post-shed
# manifest does. Pass 1 of check 3 is untouched in both phases — the carve
# commit is still in this repository's history after the shed, so all 318
# digests are still recomputed from the referent's real bytes and the manifest
# is still held to the tree it NAMES. What `post-shed` gives up is precisely
# what deleting the files makes unaskable: "the source has not drifted since
# the carve", for the moved rows only. That guarantee is discharged elsewhere
# and once — at the four destinations, by `verify-carve-arrival.py`, before the
# shed may be declared at all.
PHASE_CARVE = "carve"
PHASE_POST_SHED = "post-shed"
PHASES: tuple[str, ...] = (PHASE_CARVE, PHASE_POST_SHED)

DISPOSITIONS: tuple[str, ...] = ("moved_verbatim", "moved_with_declared_edit",
                                 "not_moved")
MOVED_DISPOSITIONS: tuple[str, ...] = ("moved_verbatim",
                                       "moved_with_declared_edit")

# The ONE `not_moved` reason that means the bytes DO arrive somewhere — a copy
# at each destination, retained here (RULED OQ-A/OQ-C). It is the only reason
# under which check 6 admits `edits:` on a `not_moved` row (RULED Q-L7 (a)):
# every other reason describes a file that arrives nowhere, and a carve edit to
# a file that arrives nowhere is the contradiction check 6 exists to name. The
# three `stays_openxfactory_governance` rows that record an import rewrite in
# their EVIDENCE prose (RULING OQ-B's `tests/notebooklm/*`) are unchanged by
# this: they stay HERE and take their rewrite in openxFactory, so they have no
# replica for a declared line to be applied at.
REPLICA_REASON = "replicated_at_destination"

# RULED OQ-C. The manifest declares its own subset of these; it may not declare
# a reason that is not here.
KNOWN_NOT_MOVED_REASONS: tuple[str, ...] = (
    "stays_openxfactory_adapter",
    "stays_openxfactory_governance",
    "deleted_at_carve",
    "superseded_by_split",
    "replicated_at_destination",
)

# The refusal vocabulary, FIXED, COMPLETE and ordered by the check that raises
# it. Other code may branch on the CODE, so no failure path here may invent one
# — and completeness is asserted rather than asserted-in-prose:
# `tests/carve_manifest/test_carve_manifest.py` scans this file's own
# `CarveRefusal(...)` sites and fails if any code is missing from this tuple.
#
# `carve-unreadable` IS in the vocabulary, which is a correction. It was left
# out on the reasoning that it "describes an environment in which no finding can
# be reached at all", and four of its five raise sites are exactly that — no
# git, no resolvable HEAD, a failed `ls-tree`, bytes that cannot be read. But a
# closed vocabulary whose stated purpose is that callers branch on the code may
# not have a value outside itself; and the fifth site was a DOCUMENT defect
# wearing the environment's name (an unparseable manifest), which now refuses as
# `carve-shape-invalid` with the parser's own position. The split this tuple now
# carries: `carve-unreadable` is the ENVIRONMENT and the ENCODING — the bytes
# never became a document — and every other code is a manifest that disagrees
# with the tree it claims.
#
# FOUR MEMBERS HAVE BEEN ADDED SINCE, AND DELIBERATELY. `carve-shed-incomplete`
# joined this tuple with the manifest's `phase:` key (RULED (a), Brett Heap,
# 2026-09-10, `#656` comment `5625573095`). The post-shed phase asserts an
# ABSENCE, and a tree that still carries the file is a finding no existing code
# named: `carve-path-absent` is its exact opposite, and `carve-digest-mismatch`
# would be a claim about bytes nobody compared. "FIXED, COMPLETE" is a statement
# about what this vocabulary owes a caller — every code a check can raise is in
# it, and nothing raises a code outside it — and not a promise never to extend
# it. THE OTHER THREE joined with the `re_destined:` row form (RULED Q6, Brett
# Heap, 2026-09-12, `#656` comment `5648044785`), and each names a defect no
# landed code named: `carve-re-destined-not-moved` (a row with no arrival
# declaring a new one), `carve-re-destined-unruled` (the citation the ruling's
# own scope answer requires, absent) and `carve-re-destined-chain` (a
# re-destination of a re-destination, which the ruling forbids in favour of
# amending the one row in place). They keep the `carve-` prefix every code in
# this vocabulary carries — `verify-carve-arrival.py`'s docstring reads that
# prefix as the OWNERSHIP split between the two tools ("every `carve-*` code is
# a manifest that disagrees with openxFactory"), so a bare `re-destined-*` here
# would be a manifest finding outside the namespace that sentence describes.
# Extending it is a ruled act, it is visible in the diff that does it, and
# `RATIFIED_CODES` in `tests/carve_manifest/test_carve_manifest.py` restates the
# tuple as a literal, so no member can be added, removed or reordered in silence.
REFUSAL_CODES: tuple[str, ...] = (
    "carve-shape-invalid",
    "carve-revision-mismatch",
    "carve-digest-mismatch",
    "carve-path-absent",
    "carve-file-undeclared",
    "carve-file-duplicated",
    "carve-surface-vacuous",
    "carve-vocabulary-unknown",
    "carve-disposition-inconsistent",
    "carve-path-order-violation",
    "carve-shed-incomplete",
    "carve-re-destined-not-moved",
    "carve-re-destined-unruled",
    "carve-re-destined-chain",
    "carve-unreadable",
)

REMEDIATION = (
    "Remediation: re-cut the manifest AT the carve commit — recompute every "
    "sha256 from the real bytes (`git cat-file blob <carve_commit>:<path> | "
    "sha256sum`), never edit a digest to make this pass — or, where the tree "
    "has moved since, name a NEW carve_commit and recompute the whole file: "
    "the § 6 ceremony re-cuts, it never carries digests forward. Verify at a "
    "specific revision with `--at <sha>`. Under `phase: post-shed` the "
    "remedy for `carve-shed-incomplete` is the opposite one: the manifest "
    "declares the shed DONE and the tree still carries the file, so either "
    "the deletion is missing from this commit or the phase was flipped "
    "early — the shed and the flip land together or not at all. A "
    "`carve-re-destined-*` refusal is not a re-cut either: amend the one "
    "row's own `re_destined:` block in place, citing the ruling that ordered "
    "the move — a row already re-destined is AMENDED, never re-destined twice."
)

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
TAG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
REPO_RE = re.compile(r"^[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
MODE_RE = re.compile(r"^(100644|100755|120000)$")
EDIT_KEYS = {"class", "lines", "note"}

# `re_destined:`' OWN KEY SET, CLOSED to exactly these six (RULED Q6). Five are
# REQUIRED — the placement is not expressible without all four of
# `from`/`from_path`/`to`/`to_path`, and `ruling:` is required because the
# ruling's scope answer is that the form serves a RULED mis-placement only, so
# a re-destination with no citation is the quiet convenience move the ruling
# refuses. `note:` is the one optional key, prose, exactly as an `edits[]`
# entry's is.
RE_DESTINED_KEYS = frozenset({"from", "from_path", "to", "to_path", "ruling",
                              "note"})

# A `destinations:` KEY is a label, never a referent — a row's own
# `destination` is always a string (`_require_str` enforces it on every
# row), so a key this pattern would not match can never be legitimately
# referenced by any row at all. Copilot review, PRRT_kwDOTAvnrs6guuUN,
# 2026-09-09: an unquoted numeric key (`1:`) parses under PyYAML as the
# int 1, not a string, and used to pass this check silently — surviving
# all the way to `check_vocabularies`' `sorted(destinations)`, where a
# document mixing an int key with a str key raises `TypeError` (`'<' not
# supported between instances of 'str' and 'int'`) and the process exits
# 1, which is not one of the two exit codes this file's docstring promises.
DESTINATION_KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")

# A destination entry's key set, CLOSED to exactly these two — an unknown key
# is a typo the closed grammar the module docstring promises must not admit,
# and a missing one is caught by `_require_str` naming the same two names.
DESTINATION_KEYS = frozenset({"repository", "leg"})

# The three legs of the `openRepoShape` project shape this carve targets
# (split-opendox-two-layer-product, "AMENDED 2026-09-05 (repository shape)":
# each layer is an assembly root plus a `-spec` and a `-code` leg). A
# destination is exactly one of them.
LEGS: tuple[str, ...] = ("code", "spec", "assembly")

# The DOCUMENT's key set, CLOSED. `header:` and `phase:` are the two optional
# keys: `header:` is prose recording RULED OQ-E's convention break, and
# `phase:` absent means `carve` (see "THE TWO PHASES" above) — every other
# key here is required by check 1. Closed because the schema the three consts
# are borrowed from is `additionalProperties: false`, and because an open top
# level means a mistyped `moved_path:` is ignored in silence while the key it
# failed to be is the one that carries the whole surface.
TOP_LEVEL_KEYS = frozenset({
    "schema_version", "kind", "header", "phase", "carve_commit", "carve_tag",
    "source_repository", "digest_algorithm", "digest_source", "path_order",
    "destinations", "edit_classes", "not_moved_reasons", "moved_paths", "rows",
})

# THE ROW GRAMMAR, PER DISPOSITION AND IN ONE PLACE. The memo's § 1.2 moved row
# is `source_path + git_mode + sha256 + disposition + destination +
# destination_path`, and its `not_moved` row is `source_path + disposition +
# reason + evidence` — "no digest", and by the same reasoning no destination: a
# `not_moved` row carrying one reads at the destination as "this file goes
# there" while its own disposition says it does not, and today's `destination`
# would even be validated against `destinations:` on its way past.
#
# `edits` is grammatically legal on EVERY disposition, deliberately: whether an
# edit list AGREES with the disposition is check 6's question, and check 6
# answers it as `carve-disposition-inconsistent` — a more precise finding, for a
# row all of whose keys are real ones, than "unknown key". Under RULED Q-L7 (a)
# check 6 now ADMITS it on a `not_moved / replicated_at_destination` row, which
# is a change in that check and not in this grammar.
#
# `re_destined` is on the MOVED dispositions ONLY (RULED Q6), for the reason
# `also_replicated_to` is: a `not_moved` row declares no destination, so there
# is no arrival for a ruling to re-place. That refusal is its own arm in
# `_check_row_shape` under its own code — `carve-re-destined-not-moved` — and
# not the generic "carries a destination" message, because a row asking to be
# re-destined is asking a coherent question with an incoherent premise.
#
# `also_replicated_to` is on the MOVED dispositions ONLY (RULED Q-L7 (a)). A
# `not_moved` row declares no destination at all, so it cannot declare an
# ADDITIONAL one: a replica row is already replicated at every destination that
# needs it and names none of them, and a `stays_*` or `deleted_at_carve` row's
# bytes arrive nowhere. That refusal is a shape finding with its own arm in
# `_check_row_shape`, not the generic "carries a destination" message, because
# the key it names is a different claim from `destination:`.
ROW_KEYS_BY_DISPOSITION: dict[str, frozenset[str]] = {
    "moved_verbatim": frozenset({
        "source_path", "disposition", "git_mode", "sha256", "destination",
        "destination_path", "edits", "also_replicated_to", "re_destined"}),
    "moved_with_declared_edit": frozenset({
        "source_path", "disposition", "git_mode", "sha256", "destination",
        "destination_path", "edits", "also_replicated_to", "re_destined"}),
    "not_moved": frozenset({
        "source_path", "disposition", "reason", "evidence", "edits"}),
}

# What ANY row may carry at all. A row whose `disposition` is outside the three
# is checked against this union, because the vocabulary miss belongs to check 5
# and a shape refusal here would hide which check did the work.
ROW_KEYS: frozenset[str] = frozenset().union(*ROW_KEYS_BY_DISPOSITION.values())


class CarveRefusal(Exception):
    """A named, remediable refusal.

    Carries the machine-readable `code` separately from the human `detail`, so a
    caller can branch on the code without parsing prose.

    `render(manifest)` is the ONE place the human message is assembled — code,
    detail and the fixed remediation trailer — and `main()` prints exactly that
    and nothing else, so the trailer cannot be dropped by a caller that forgot
    it exists. It is a method rather than `__str__` because the message names
    the manifest that failed, which the exception does not carry: every check
    below can be raised from a nested helper that has no idea which file it is
    reading, and threading the path through all of them to satisfy `__str__`
    would put the same string in several hands.
    """

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(code, detail)

    def render(self, manifest: Path) -> str:
        """Render the human message; always printable, even over a non-UTF-8
        tree path. `self.detail` can interpolate a `tree_at()` path decoded
        with `surrogateescape` (Copilot review `5155397957`, 2026-09-09,
        `scripts/validate-carve-manifest.py:280`): this is safe printed to
        `sys.stderr` because CPython pins stderr's error handler to
        `backslashreplace` regardless of what `PYTHONIOENCODING` requests, so
        the surrogate is escaped rather than raising — measured across 14 runs
        (3 refusal paths × 5 stdio configurations, plain and `--json`), all
        exit 2, none a traceback.
        """
        return f"FAIL {manifest}: {self.code} — {self.detail}\n{REMEDIATION}"


# --------------------------------------------------------------------------
# git
# --------------------------------------------------------------------------

def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    """git, capturing BYTES — blob contents must not go through a decoder.

    Runs `--no-replace-objects` against a SANITIZED environment (register
    item, `#656` comment `5638315691`): every `resolve_revision`, `tree_at`
    and `cat-file blob <commit>:<path>` read below goes through this one
    helper, and without this an ambient `GIT_DIR`, alternate object
    directory, indexed `GIT_CONFIG_KEY/VALUE_N`, or replace-ref could resolve
    a read from a DIFFERENT object store than the one `repo` names — reading
    a commit the tested revision does not actually carry. Same fix, same
    reason, as `scripts/carved_reach.py`'s `_git_object_id` (commit
    `c7d290da`) and `scripts/hermes_runtime_validation/content.py`'s `_git`;
    `carved_reach._sanitized_git_environment()` is REUSED rather than a third
    copy of its scrub list — see the `import carved_reach` comment above for
    why that import is safe here.
    """
    try:
        return subprocess.run(
            ["git", "--no-replace-objects", "-C", str(repo), *args],
            capture_output=True, check=False,
            env=carved_reach._sanitized_git_environment(),
        )
    except OSError as exc:  # pragma: no cover - no git on the host
        raise CarveRefusal("carve-unreadable",
                           f"git could not be run in {repo}: {exc}") from exc


def resolve_revision(repo: Path, at: str | None) -> str:
    """The revision this run is asking about: `--at <sha>` or `HEAD`."""
    ref = at if at is not None else "HEAD"
    done = _git(repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    if done.returncode != 0 or not done.stdout.strip():
        if at is not None:
            raise CarveRefusal(
                "carve-revision-mismatch",
                f"--at {at!r} does not resolve to a commit in {repo}; the "
                "manifest's digests are taken at exactly one revision and an "
                "unresolvable one is not that revision")
        raise CarveRefusal(
            "carve-unreadable",
            f"{repo} has no resolvable HEAD; this validator reads the carve "
            "commit's tree out of a real git repository")
    return done.stdout.decode("utf-8", "replace").strip()


class TreeEntry(NamedTuple):
    """One blob at one revision: the file mode, and git's own object id.

    THE OID IS CARRIED BECAUSE CHECK 3 NOW COMPARES ONE PATH AT TWO REVISIONS.
    Two blobs are the same bytes exactly when git named them the same object —
    the id is a hash of the content that git itself computed, in this one
    repository, under this one algorithm — so "did this file change since the
    carve" is answerable without reading either blob. On a ~430-row manifest
    that is ~430 `cat-file` invocations not spent per extra revision; the bytes
    are still read for the one row whose ids differ, so the refusal can name
    the sha256 the reader is being asked to compare.
    """

    mode: str
    oid: str


def tree_at(repo: Path, commit: str) -> dict[str, TreeEntry]:
    """`{path: TreeEntry(mode, oid)}` for every BLOB at `commit`.

    One `ls-tree` for the whole tree rather than a call per row: the modes and
    ids are needed for check 3 and the path set for check 4, and all of them
    come out of the same listing. `-z` because a path is bytes and git quotes
    unusual ones otherwise; `--full-tree` because the answer must not depend on
    where this process was started.
    """
    done = _git(repo, "ls-tree", "-r", "-z", "--full-tree", commit)
    if done.returncode != 0:
        raise CarveRefusal(
            "carve-unreadable",
            f"`git ls-tree -r {commit[:12]}` failed in {repo}: "
            + done.stderr.decode("utf-8", "replace").strip())
    tree: dict[str, TreeEntry] = {}
    for record in done.stdout.decode("utf-8", "surrogateescape").split("\0"):
        if not record:
            continue
        meta, _, path = record.partition("\t")
        fields = meta.split(" ")
        if len(fields) != 3:  # pragma: no cover - git's format is stable
            raise CarveRefusal("carve-unreadable",
                               f"unparseable ls-tree record {record!r}")
        mode, kind, oid = fields
        if kind == "blob":
            tree[path] = TreeEntry(mode, oid)
    return tree


def blob_at(repo: Path, commit: str, path: str) -> bytes | None:
    """The RAW bytes of `path` at `commit`, or None where it is not a blob."""
    done = _git(repo, "cat-file", "blob", f"{commit}:{path}")
    if done.returncode != 0:
        return None
    return done.stdout


# --------------------------------------------------------------------------
# reading
# --------------------------------------------------------------------------

def read_manifest(path: Path) -> dict[str, Any]:
    """The manifest as a document, with its two failure kinds kept APART.

    READING is `carve-unreadable`: an I/O error, or bytes that are not UTF-8 at
    all — the environment, in which no finding about a document can be reached
    because there is no document. PARSING is `carve-shape-invalid`: an
    unparseable manifest is not an environment, it is a DOCUMENT DEFECT a
    reviewer acts on, in the same place and the same way as the empty manifest
    three lines below (which parses to `None` and has always been
    `carve-shape-invalid`). They used to get codes from two different
    vocabularies — one unclosed bracket handed a code-branching caller a value
    the vocabulary said did not exist — so the parser's own position is reported
    under the document code instead.
    """
    try:
        text = path.read_text(encoding="utf-8")
    # `ValueError` covers `UnicodeDecodeError`: a manifest that is not valid
    # UTF-8 is unreadable, and it must reach the reader as this named exit-2
    # refusal rather than as a traceback and exit 1.
    except (OSError, ValueError) as exc:
        raise CarveRefusal("carve-unreadable",
                           f"the manifest could not be read: {exc}") from exc
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        at = (f" at line {mark.line + 1} column {mark.column + 1}"
              if mark is not None else "")
        raise CarveRefusal(
            "carve-shape-invalid",
            f"the manifest is not parseable YAML{at}: {exc}") from exc
    if not isinstance(doc, dict):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"the manifest is not a mapping (parsed as {type(doc).__name__})")
    return doc


def _require_str(doc: dict, key: str, where: str) -> str:
    value = doc.get(key)
    if not isinstance(value, str) or not value.strip():
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} declares `{key}: {value!r}`; a non-empty string is "
            "required")
    return value


def _require_closed_relative_path(doc: dict, key: str, where: str) -> str:
    """`_require_str`, plus: refuse a value `scripts/carved_reach.py` could
    not safely join onto a leg's mount.

    Copilot review, `PRRT_kwDOTAvnrs6hjzVm`, 2026-09-11: `destination_path`
    was type-checked as a non-empty string only; an absolute value or a
    `../` segment would let the resolver's `mount / destination_path` join
    escape the pinned leg. This is the VALIDATOR-SIDE half — the
    resolver-side half is `carved_reach._closed_relative_path`, the same
    predicate, kept in step here because this script cannot import that
    module's package (`scripts.carved_reach` needs the repository root on
    `sys.path`; this script is loaded by `spec_from_file_location` with only
    `scripts/` on it, the same reason `carve_lines` above is a bare import).

    NOT restricted to an ASCII alphabet: `destination_path` may legitimately
    carry any Unicode filename
    (`test_the_row_order_is_bytewise_and_not_by_code_point` exercises one
    with U+E000) — only the segment shape that would let a join escape its
    mount is refused.
    """
    value = _require_str(doc, key, where)
    if (value.startswith("/") or value.startswith(":") or "\\" in value
            or any(ord(character) < 32 or ord(character) == 127 for character in value)):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} declares `{key}: {value!r}`, which is not a canonical "
            "relative path (absolute, drive-letter-shaped, or backslashed)")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} declares `{key}: {value!r}`, which contains a `.`, "
            "`..` or empty segment — exactly what would let this row's "
            "destination escape its own mount")
    return value


# --------------------------------------------------------------------------
# check 1 — shape
# --------------------------------------------------------------------------

def check_shape(doc: dict[str, Any]) -> None:
    """Everything answerable from the document alone, before any git call.

    THE `edits[]` ENTRY GRAMMAR IS ENFORCED HERE and the memo lists it under
    check 6. It is moved forward deliberately: it is a property of the document
    and of nothing else, and check 5 must read `edits[].class` before check 6
    runs — a vocabulary check that first had to defend itself against a
    malformed entry would be two checks wearing one name. Check 6 keeps what is
    actually its own: whether the entries AGREE with the disposition.
    """
    version = doc.get("schema_version")
    if (not isinstance(version, int) or isinstance(version, bool)
            or version != SCHEMA_VERSION):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`schema_version: {version!r}`; this validator reads the INTEGER "
            f"{SCHEMA_VERSION} only. `true` and `1.0` are both EQUAL to 1 in "
            "Python, and the first assertion of a fail-closed chain may not be "
            "satisfied by a bool")
    if doc.get("kind") != KIND:
        raise CarveRefusal("carve-shape-invalid",
                           f"`kind: {doc.get('kind')!r}`, not {KIND!r}")
    stray = sorted(set(doc) - TOP_LEVEL_KEYS, key=repr)
    if stray:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"the manifest carries the unknown top-level key(s) {stray!r}; the "
            "document grammar is closed (`header:` and `phase:` are its two "
            "optional keys; every other key is required), so a mistyped "
            "`moved_path:` refuses here rather than being ignored in silence — "
            "and it is the surface list that a stray key is most likely to be "
            "a misspelling of")
    for key, expected in CONSTS.items():
        if doc.get(key) != expected:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`{key}: {doc.get(key)!r}` is not the const {expected!r}; "
                "the row grammar is the release-digest inventory's and its "
                "consts are not a per-manifest choice")

    # `phase:` IS CHECK 1'S, not check 5's. Check 5 owns the closed vocabularies
    # of a ROW — `disposition`, `edits[].class`, `destination`, `reason` — and
    # this is a document-level const in the same family as `digest_algorithm`,
    # answerable before any git call. Reporting it under check 5 would also mean
    # a mistyped phase reached checks 3 and 4 first and refused there, under a
    # code naming a file, for a defect in one word of the header.
    phase = doc.get("phase", PHASE_CARVE)
    if phase not in PHASES:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`phase: {phase!r}` is not one of {list(PHASES)!r}. The key is "
            f"OPTIONAL and its absence means {PHASE_CARVE!r} — the phase this "
            "file was authored in — so a manifest that never mentions it reads "
            "exactly as it did before the key existed; a manifest that does "
            "mention it must name a phase this validator implements, because "
            "the phase decides whether a deleted source path is a refusal or "
            "the declared outcome")

    commit = doc.get("carve_commit")
    if not isinstance(commit, str) or not COMMIT_RE.match(commit):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`carve_commit: {commit!r}` is not 40 lowercase hex characters; "
            "the carve's referent is a commit, and an abbreviation, a branch "
            "name or a tag is a movable name rather than a referent")
    tag = _require_str(doc, "carve_tag", "the manifest")
    if not TAG_RE.match(tag):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`carve_tag: {tag!r}` is not a label; the tag is a HUMAN LABEL "
            "beside the commit and never the referent")
    source = _require_str(doc, "source_repository", "the manifest")
    if not REPO_RE.match(source):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`source_repository: {source!r}` is not `owner/name`")

    destinations = doc.get("destinations")
    if not isinstance(destinations, dict) or not destinations:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`destinations:` is not a non-empty mapping ({destinations!r}); "
            "a row's `destination` is a KEY here, because one typo otherwise "
            "ships a file to a repository nobody declared")
    # Two keys sharing one `{repository, leg}` body are NOT refused here —
    # deliberate, and explained in the module docstring (S8) rather than here:
    # it is check 4's question, not this one's.
    for key, entry in destinations.items():
        # THE KEY'S OWN SHAPE, CHECKED FIRST — before descending into what
        # its entry carries, on the same first-failure-wins discipline every
        # other check in this file keeps: a malformed key is a more
        # fundamental defect than anything inside a well-formed entry, and
        # reporting it under a code that names the entry's OWN contents
        # would hide which part of the row actually failed. `not
        # isinstance(key, str)` is required and not implied by the regex
        # match below — `DESTINATION_KEY_RE.match` on a non-str argument
        # raises `TypeError` itself, which is exactly the failure mode this
        # check exists to keep out of this file.
        if not isinstance(key, str) or not DESTINATION_KEY_RE.match(key):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`destinations` carries the key {key!r}, which is not a "
                "lowercase label matching `^[a-z][a-z0-9_]*$`. A row's own "
                "`destination` is always a STRING — `_require_str` enforces "
                "that on every row — so a key this pattern rejects can never "
                "be legitimately referenced by any row at all. PyYAML "
                "parses an unquoted numeric key such as `1:` as the int 1 "
                "rather than the label its author meant, and that used to "
                "pass this check in silence and surface only when "
                "`check_vocabularies`' `sorted(destinations)` met a "
                "document mixing that int with a str key — a raw "
                "`TypeError`, exit 1, not one of the two exit codes this "
                "file's docstring promises")
        if not isinstance(entry, dict):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`destinations.{key}` is not a mapping ({entry!r})")
        stray = sorted(set(entry) - DESTINATION_KEYS, key=repr)
        if stray:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`destinations.{key}` carries the unknown key(s) {stray!r}; "
                "an entry is closed to exactly `repository` and `leg`, which "
                "is what makes the module docstring's \"closed maps\" true of "
                "the destinations too, not only of the rows")
        repository = _require_str(entry, "repository", f"`destinations.{key}`")
        if not REPO_RE.match(repository):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`destinations.{key}.repository: {repository!r}` is not "
                "`owner/name`")
        leg = _require_str(entry, "leg", f"`destinations.{key}`")
        if leg not in LEGS:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`destinations.{key}.leg: {leg!r}` is not one of "
                f"{list(LEGS)!r}")

    classes = doc.get("edit_classes")
    if not isinstance(classes, list) or tuple(classes) != EDIT_CLASSES:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`edit_classes: {classes!r}` is not the RULED list "
            f"{list(EDIT_CLASSES)!r}, verbatim and in order. The list is "
            "closed: an edit is expressible as one of these three or it is not "
            "a carve edit at all")

    reasons = doc.get("not_moved_reasons")
    if not isinstance(reasons, list) or not reasons:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`not_moved_reasons:` is not a non-empty list ({reasons!r})")
    unknown = [r for r in reasons if r not in KNOWN_NOT_MOVED_REASONS]
    if unknown:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`not_moved_reasons:` declares {unknown!r}, which this validator "
            f"does not know; the known set is {list(KNOWN_NOT_MOVED_REASONS)!r} "
            "(RULED OQ-C). The reason vocabulary carries the nuance the three "
            "dispositions cannot, so it is declared AND known — a file may not "
            "widen it by declaring it")

    moved_paths = doc.get("moved_paths")
    if not isinstance(moved_paths, list) or not moved_paths:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`moved_paths:` is not a non-empty list ({moved_paths!r}); it is "
            "the SURFACE the completeness check walks, and an empty surface "
            "declares nothing")
    for entry in moved_paths:
        if not isinstance(entry, str) or not entry.strip():
            raise CarveRefusal(
                "carve-shape-invalid",
                f"`moved_paths:` holds a non-path entry ({entry!r})")

    rows = doc.get("rows")
    if not isinstance(rows, list) or not rows:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"`rows:` is not a non-empty list ({rows!r})")
    for index, row in enumerate(rows):
        _check_row_shape(index, row, moved_paths)


def _check_row_shape(index: int, row: Any, moved_paths: list[str]) -> None:
    where = f"rows[{index}]"
    if not isinstance(row, dict):
        raise CarveRefusal("carve-shape-invalid",
                           f"{where} is not a mapping ({row!r})")
    stray = sorted(set(row) - ROW_KEYS, key=repr)
    if stray:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} carries the unknown key(s) {stray!r}; the row grammar is "
            "closed, so a field nobody validates is a field nobody reads")
    source_path = _require_str(row, "source_path", where)
    if not in_surface(source_path, moved_paths):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} declares `source_path: {source_path!r}`, which lies "
            "under no `moved_paths:` prefix; the manifest declares what LEAVES "
            "the surface, and a row outside it makes the completeness check "
            "answer a different question from the one it asks")

    disposition = row.get("disposition")
    if not isinstance(disposition, str) or not disposition:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} ({source_path}) declares `disposition: {disposition!r}`; "
            "a string is required")
    # A disposition OUTSIDE the three is left to check 5, which owns the closed
    # vocabularies: refusing it here would report a vocabulary miss under a
    # shape code and hide which check is doing the work.
    if disposition in MOVED_DISPOSITIONS:
        mode = row.get("git_mode")
        if not isinstance(mode, str) or not MODE_RE.match(mode):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{where} ({source_path}) declares `git_mode: {mode!r}`; a "
                "quoted git file mode is required (a mode flip is what a blob "
                "digest does not see, and an unquoted 100644 parses as an int)")
        digest = row.get("sha256")
        if not isinstance(digest, str) or not SHA256_RE.match(digest):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{where} ({source_path}) declares `sha256: {digest!r}`, which "
                "is not 64 lowercase hex characters")
        _require_str(row, "destination", f"{where} ({source_path})")
        _require_closed_relative_path(row, "destination_path", f"{where} ({source_path})")
        if "also_replicated_to" in row:
            _check_also_replicated_shape(where, source_path,
                                         row["also_replicated_to"])
        if "re_destined" in row:
            _check_re_destined_shape(where, source_path, row["re_destined"])
        for key in sorted(ROW_KEYS - ROW_KEYS_BY_DISPOSITION[disposition]):
            if key in row:
                raise CarveRefusal(
                    "carve-shape-invalid",
                    f"{where} ({source_path}) is `{disposition}` and carries "
                    f"`{key}:`; a reason, and the evidence for it, answer why a "
                    "file did NOT move")
    elif disposition == "not_moved":
        _require_str(row, "reason", f"{where} ({source_path})")
        _require_str(row, "evidence", f"{where} ({source_path})")
        # ITS OWN ARM, ahead of the generic loop below (which would reach it
        # first, `also_replicated_to` sorting before `destination`): the key is
        # a DIFFERENT claim from `destination:` and the generic message —
        # "nothing arrives" — is false of a replica row, whose bytes do arrive
        # at every destination that needs them. Reported precisely instead.
        if "re_destined" in row:
            raise CarveRefusal(
                "carve-re-destined-not-moved",
                f"{where} ({source_path}) is `not_moved` and carries "
                "`re_destined:`. RULED Q6 puts that field on a MOVED row, to "
                "say that a RULING has moved a placement the carve made; a "
                "`not_moved` row placed nothing, so there is no arrival to "
                "re-place. A row that STAYS, or was deleted at the carve, "
                f"arrives nowhere; a `{REPLICA_REASON}` row's copies are "
                "placed by the leg and declared to `verify-carve-arrival.py` "
                "with `--replica-at` (RULED OQ-C), so a re-destination of one "
                "would be re-pointing a placement this manifest never made. "
                "If the ruling really moves a file this manifest says stays, "
                "that is a change of DISPOSITION and a re-cut question, not "
                "this field")
        if "also_replicated_to" in row:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{where} ({source_path}) is `not_moved` and carries "
                "`also_replicated_to:`. RULED Q-L7 (a) puts that key on a "
                "MOVED row, to say that bytes which move to one destination "
                "are ALSO replicated at another; a `not_moved` row declares no "
                "destination at all, so it cannot declare an additional one. A "
                f"`{REPLICA_REASON}` row is already replicated at every "
                "destination that needs it and names none of them — placement "
                "is the leg's (RULED OQ-C) — and a row that stays, or was "
                "deleted at the carve, arrives nowhere to be replicated")
        for key in sorted(ROW_KEYS - ROW_KEYS_BY_DISPOSITION["not_moved"]):
            if key in row:
                raise CarveRefusal(
                    "carve-shape-invalid",
                    f"{where} ({source_path}) is `not_moved` and carries "
                    f"`{key}:`; a digest, a mode or a DESTINATION at the carve "
                    "commit is the claim that these bytes arrive somewhere, and "
                    "nothing arrives. The memo's § 1.2 `not_moved` row is "
                    "`source_path + disposition + reason + evidence`, and a "
                    "destination on it would be validated against "
                    "`destinations:` on its way past — arriving at the "
                    "destination as `this file goes there` over a disposition "
                    "that says it does not")

    edits = row.get("edits")
    if edits is not None:
        _check_edits_shape(where, source_path, edits)


def _check_edits_shape(where: str, source_path: str, edits: Any) -> None:
    if not isinstance(edits, list):
        raise CarveRefusal("carve-shape-invalid",
                           f"{where} ({source_path}) declares `edits:` as "
                           f"{edits!r}; a list is required")
    for position, edit in enumerate(edits):
        at = f"{where}.edits[{position}] ({source_path})"
        if not isinstance(edit, dict):
            raise CarveRefusal("carve-shape-invalid",
                               f"{at} is not a mapping ({edit!r})")
        stray = sorted(set(edit) - EDIT_KEYS, key=repr)
        if stray:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{at} carries the unknown key(s) {stray!r}; an edit is "
                "`{class, lines, note?}` and nothing else")
        if not isinstance(edit.get("class"), str) or not edit["class"]:
            raise CarveRefusal("carve-shape-invalid",
                               f"{at} declares `class: {edit.get('class')!r}`")
        lines = edit.get("lines")
        if not isinstance(lines, list) or not lines:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{at} declares `lines: {lines!r}`; at least one line number "
                "at the carve commit is required. Without them "
                "`moved_with_declared_edit` is only a label — the line numbers "
                "are what make the claim falsifiable at the destination")
        for line in lines:
            if not isinstance(line, int) or isinstance(line, bool) or line < 1:
                raise CarveRefusal(
                    "carve-shape-invalid",
                    f"{at} declares the line {line!r}; line numbers are "
                    "positive integers")
        if "note" in edit and (not isinstance(edit["note"], str)
                               or not edit["note"].strip()):
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{at} declares `note: {edit['note']!r}`; a note is prose or "
                "it is absent")


def _check_also_replicated_shape(where: str, source_path: str,
                                 value: Any) -> None:
    """`also_replicated_to:` is a NON-EMPTY list of distinct destination labels.

    Shape only. WHETHER each label is a key of `destinations:` is check 5's
    question — the same check that owns `destination` — and whether the row
    lists its OWN destination is check 6's, because that is a row contradicting
    itself rather than a document mis-shaped. Reported in three places on
    purpose: a reader of a refusal should be able to tell a typo from an
    unknown destination from a self-reference without reading this file.

    AN EMPTY LIST REFUSES. `also_replicated_to: []` declares no replica while
    looking in review like a row that declares one, and the absent key says
    the same thing unambiguously — `moved_paths:`' own reasoning, one level
    down. A REPEATED label refuses for the reason `--replica-at`'s repeated key
    does at the destination: one replica lands once per destination, and a
    duplicate is either a typo for a second destination or a claim made twice.
    """
    if not isinstance(value, list) or not value:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} ({source_path}) declares `also_replicated_to: {value!r}`;"
            " a non-empty list of `destinations:` labels is required. An empty "
            "list declares no replica while reading in a diff like a row that "
            "declares one, and the absent key says that unambiguously")
    seen: set[str] = set()
    for position, entry in enumerate(value):
        if not isinstance(entry, str) or not entry.strip():
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{where}.also_replicated_to[{position}] ({source_path}) is "
                f"{entry!r}; a destination label is a non-empty string, and a "
                "row's replica destinations are KEYS of `destinations:` for the "
                "reason its own `destination` is one — one typo otherwise "
                "replicates a file to a repository nobody declared")
        if entry in seen:
            raise CarveRefusal(
                "carve-shape-invalid",
                f"{where} ({source_path}) lists {entry!r} twice in "
                "`also_replicated_to:`; one replica lands once per "
                "destination, so a repeat is either a typo for a second "
                "destination or the same claim made twice")
        seen.add(entry)


def _check_re_destined_shape(where: str, source_path: str, value: Any) -> None:
    """`re_destined:` is a CLOSED mapping of five required strings and one
    optional note (RULED Q6).

    SHAPE ONLY, and the split is the one `also_replicated_to:` already keeps.
    WHETHER `from` and `to` are keys of `destinations:` is check 5's question,
    the same check that owns a row's own `destination`. WHETHER `from` is the
    row's own destination, whether `to` differs from it, and whether the row
    chains off another row's re-destination are check 6's — a row contradicting
    itself, or two rows contradicting each other, rather than a document
    mis-shaped.

    THE MISSING `ruling:` IS NOT `carve-shape-invalid`, and that is deliberate.
    Every other absent key here is a typo; this one is the whole scope answer
    of the ruling that created the field — "require a `ruling:` field naming
    the comment that ordered it, validated present, so the form cannot become a
    quiet way to move a file after the carve is closed" — so it gets a code a
    reader can branch on and a message that says what is actually wrong.

    THE CITATION'S FORM IS NOT CONSTRAINED. A ruling is cited in this estate as
    a comment id (`5648044785`), as `#656` plus a comment reference, or as a
    pull request URL, and the ruling asked for the field to be PRESENT, not for
    one of those spellings. A pattern here would refuse a legitimate citation
    and teach the author to write whatever the pattern wanted.

    THE TWO PATHS GO THROUGH `_require_closed_relative_path`, exactly as
    `destination_path` does: `to_path` is joined onto a leg's mount by
    `carved_reach`, and `from_path` is the path `verify-carve-arrival.py`
    requires ABSENT at the losing leg — an absolute or `../` value would ask
    either question about a file outside the tree it is about.
    """
    if not isinstance(value, dict):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} ({source_path}) declares `re_destined: {value!r}`; a "
            "mapping of `{from, from_path, to, to_path, ruling, note?}` is "
            "required (RULED Q6)")
    stray = sorted(set(value) - RE_DESTINED_KEYS, key=repr)
    if stray:
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} ({source_path}) declares `re_destined:` with the "
            f"unknown key(s) {stray!r}; the field is closed to "
            f"{sorted(RE_DESTINED_KEYS)!r}, so a field nobody validates is a "
            "field nobody reads")
    if "ruling" not in value or not isinstance(value.get("ruling"), str) \
            or not value["ruling"].strip():
        raise CarveRefusal(
            "carve-re-destined-unruled",
            f"{where} ({source_path}) declares `re_destined:` with "
            f"`ruling: {value.get('ruling')!r}`. RULED Q6 scoped this form to "
            "a RULED mis-placement and required the citation PRESENT — "
            "without it the field is a quiet way to move a file after the "
            "carve is closed, which is the one use the ruling refused. Name "
            "the comment that ordered the move (a `#656` comment id, or the "
            "pull request URL that carries the ruling); the form of the "
            "citation is yours, its presence is not")
    for key in ("from", "to"):
        _require_str(value, key, f"{where} ({source_path}) `re_destined`")
    for key in ("from_path", "to_path"):
        _require_closed_relative_path(
            value, key, f"{where} ({source_path}) `re_destined`")
    if "note" in value and (not isinstance(value["note"], str)
                            or not value["note"].strip()):
        raise CarveRefusal(
            "carve-shape-invalid",
            f"{where} ({source_path}) declares `re_destined.note: "
            f"{value['note']!r}`; a note is prose or it is absent")


def effective_arrival(row: dict[str, Any]) -> tuple[Any, Any]:
    """`(destination key, destination path)` a moved row's bytes arrive at
    TODAY — `re_destined.to`/`to_path` where a ruling has moved the placement,
    else the row's own `destination`/`destination_path` (RULED Q6).

    THE SAME PREDICATE LIVES IN `scripts/verify-carve-arrival.py`, and the two
    are kept in step here rather than shared through a module, on the precedent
    `_require_closed_relative_path` sets for `carved_reach._closed_relative_path`
    — this script is loaded by `spec_from_file_location` with only `scripts/` on
    `sys.path`, and the other tool is a hyphenated entry point that cannot be
    imported at all.
    `tests/carve_arrival/test_verify_carve_arrival.py::test_both_tools_read_the_effective_arrival_identically`
    loads both files and compares them over a table of rows, so "kept in step"
    is asserted rather than hoped for — the lesson RULED Q-L8 (c) taught about
    two tools and one definition.

    GUARDED AT EVERY LEVEL for the reason `_also_replicated_labels` is guarded
    at the destination: check 1 has already proved the shape by the time any
    caller here runs, but a helper that would raise on a mis-shaped document is
    a helper that decides check 1's finding for it.
    """
    re_destined = row.get("re_destined")
    if isinstance(re_destined, dict):
        to = re_destined.get("to")
        to_path = re_destined.get("to_path")
        if isinstance(to, str) and isinstance(to_path, str):
            return to, to_path
    return row.get("destination"), row.get("destination_path")


def in_surface(path: str, moved_paths: list[str]) -> bool:
    """Is `path` under one of the declared prefixes (or named exactly)?

    Segment-aware: `scripts/ideation_dashboard` does not swallow
    `scripts/ideation_dashboard_old/x.py`, which a bare `startswith` would.
    """
    for entry in moved_paths:
        prefix = entry.rstrip("/")
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False


# --------------------------------------------------------------------------
# checks 2-6
# --------------------------------------------------------------------------

def check_revision(repo: Path, doc: dict, at: str | None) -> str:
    """The REVISION UNDER TEST, returned. `carve_commit` must be its ANCESTOR.

    ANCESTRY AND NOT IDENTITY — the module docstring carries why, at length:
    identity is unsatisfiable on a pull request's merge ref and on `main` after
    the manifest lands, so as landed this check could never pass in a real run.
    Two questions survive here, and only two. Is `carve_commit` a commit THIS
    repository carries — a referent nobody can resolve is a claim about
    nothing, and a fetch too shallow to reach it is the same finding as a wrong
    one. And is it in the tested revision's HISTORY — a referent outside it
    describes some other tree, and checks 3 and 4 would be comparing two
    unrelated histories file by file and reporting the difference as drift.

    What identity used to buy — "a file changed on `main` between the manifest
    and the move REFUSES" — is checks 3 and 4's second comparison now, per file
    and by name, which is the form the memo's § 6 step 3 asks for anyway.
    """
    resolved = resolve_revision(repo, at)
    carve_commit = doc["carve_commit"]
    asked = f"--at {at}" if at is not None else "HEAD"
    known = _git(repo, "rev-parse", "--verify", "--quiet",
                 f"{carve_commit}^{{commit}}")
    peeled = known.stdout.decode("utf-8", "replace").strip()
    if known.returncode != 0 or not peeled:
        raise CarveRefusal(
            "carve-revision-mismatch",
            f"the manifest names carve_commit {carve_commit}, which {repo} "
            "DOES NOT CARRY as a commit. The referent must survive into the "
            "tree the gate reads, so a digest taken at a commit this "
            "repository cannot resolve is unverifiable here — whether the "
            "commit is wrong or the checkout is too shallow to reach it, the "
            "answer this validator can give is the same")
    # THE REFERENT MUST BE THE COMMIT OBJECT ITSELF, not something that peels
    # to one. `^{commit}` resolves an ANNOTATED TAG's object id too, and a tag
    # object id is 40 lowercase hex — so it passes check 1's grammar, and
    # `merge-base`, `ls-tree` and `cat-file` would all peel it silently and
    # verify the whole manifest against a referent the ceremony forbids: "the
    # tag is a LABEL, never the referent". The landed identity check refused
    # this as a side effect (a tag sha can never equal a `rev-parse
    # HEAD^{commit}`), so ancestry has to refuse it on purpose. Copilot review
    # `3972445078`, 2026-09-09.
    if peeled != carve_commit:
        raise CarveRefusal(
            "carve-revision-mismatch",
            f"carve_commit {carve_commit} is not a COMMIT object in {repo}: "
            f"it PEELS to {peeled}. A 40-hex object id that has to be peeled "
            "to reach a commit is an annotated tag, and the tag is a human "
            "LABEL beside the commit and never the referent — `carve_tag:` is "
            f"where a label belongs. Record the commit id itself: {peeled}")
    ancestor = _git(repo, "merge-base", "--is-ancestor",
                    carve_commit, resolved)
    if ancestor.returncode != 0:
        raise CarveRefusal(
            "carve-revision-mismatch",
            f"carve_commit {carve_commit[:12]} is NOT AN ANCESTOR of {asked} "
            f"in {repo} ({resolved}); the manifest's digests are taken on a "
            "tree this revision does not descend from, so every comparison "
            "below would be measuring two unrelated histories against each "
            "other and calling the difference drift. Verify the carve's own "
            f"line with `--at {carve_commit[:12]}`, or re-cut the manifest at "
            "a commit this revision carries")
    return resolved


def check_digests(repo: Path, doc: dict, referent: dict[str, TreeEntry],
                  tested: dict[str, TreeEntry], verified_at: str,
                  phase: str = PHASE_CARVE) -> int:
    """Check 3's two comparisons, in TWO PASSES, and in that order.

    PASS 1 asks whether the manifest is true about the tree it NAMES. PASS 2
    asks whether that tree is still the one the carve would run against.

    TWO PASSES RATHER THAN BOTH COMPARISONS INSIDE ONE ROW LOOP, because the
    order between the two KINDS of finding is a finding in itself. A manifest
    that lies about its own referent is a DOCUMENT defect its author fixes by
    recomputing a digest; a file that changed on `main` afterwards is a TREE
    fact whose remedy is the § 6 re-cut. The first must be reported even when
    some other row also moved on main, and a per-row loop would instead report
    whichever of the two rows happened to sort first — which is to say, it
    would hand the reader a remedy chosen by filename.
    """
    commit = doc["carve_commit"]
    recomputed = 0
    for index, row in enumerate(doc["rows"]):
        if row.get("disposition") not in MOVED_DISPOSITIONS:
            # A REPLICA ROW MAY NOW DECLARE LINES (RULED Q-L7 (a)) and they are
            # bounded here, where every other declared line is bounded. It
            # costs one `cat-file` per such row — one, in the landed manifest —
            # because a `not_moved` row carries no digest for pass 1 to have
            # read the blob for.
            _check_replica_edit_lines(repo, index, row, referent, commit)
            continue
        path = row["source_path"]
        if path not in referent:
            raise CarveRefusal(
                "carve-path-absent",
                f"rows[{index}] records a sha256 for {path}, which "
                f"{doc['source_repository']}@{commit[:12]} does not carry as a "
                "file; a digest of nothing is not a digest")
        if referent[path].mode != row["git_mode"]:
            raise CarveRefusal(
                "carve-digest-mismatch",
                f"{path}: MODE DRIFT — the manifest records git_mode "
                f"{row['git_mode']} and the tree at {commit[:12]} carries "
                f"{referent[path].mode}. A mode flip is the one change a blob "
                "digest cannot see, which is why the mode is carried")
        content = blob_at(repo, commit, path)
        if content is None:  # pragma: no cover - ls-tree already said blob
            raise CarveRefusal(
                "carve-path-absent",
                f"{path} could not be read as a blob at {commit[:12]}")
        actual = hashlib.sha256(content).hexdigest()
        recomputed += 1
        if actual != row["sha256"]:
            raise CarveRefusal(
                "carve-digest-mismatch",
                f"{path}: DIGEST DRIFT\n"
                f"  recorded   {row['sha256']}\n"
                f"  recomputed {actual}\n"
                f"the bytes at {commit[:12]} are not the bytes this row "
                "promises the destination")
        _check_edit_lines(index, path, row, content, commit)

    # PASS 2 — THE MEMO'S § 6 STEP 3. Pass 1 has now proved, for every moved
    # row, that the recorded `sha256` and `git_mode` ARE the referent's; so
    # comparing the tested revision against the referent is the same question
    # as comparing it against the manifest, asked without a second blob read.
    # It runs unguarded even when the two revisions coincide: `tested` IS
    # `referent` then (one `ls-tree`, see `validate`), so every comparison here
    # is an identity and the pass is a no-op by construction rather than by a
    # branch nobody exercises.
    for index, row in enumerate(doc["rows"]):
        if row.get("disposition") not in MOVED_DISPOSITIONS:
            continue
        path = row["source_path"]
        # THE ONE PLACE THE PHASE CHANGES WHAT A MOVED ROW MEANS. Under
        # `post-shed` the absence IS the declaration and the presence is the
        # finding, which is this arm read in the mirror; everything above —
        # pass 1's digest, mode and declared-line bound at the carve commit —
        # ran unchanged for this same row moments ago.
        if phase == PHASE_POST_SHED:
            if path in tested:
                raise CarveRefusal(
                    "carve-shed-incomplete",
                    f"{path}: STILL PRESENT UNDER A POST-SHED MANIFEST — "
                    f"rows[{index}] declares it `{row['disposition']}` at "
                    f"{commit[:12]}, the manifest declares "
                    f"`phase: {PHASE_POST_SHED}`, and {verified_at[:12]} "
                    "still carries it as a file. A moved row's bytes left for "
                    "the destination; the phase says openxFactory has let go "
                    "of them. Either this commit is missing the deletion, or "
                    "the phase was flipped ahead of the shed — and a phase "
                    "that could be flipped early would buy silence for every "
                    "row at once, which is why it refuses here instead")
            continue
        if path not in tested:
            raise CarveRefusal(
                "carve-path-absent",
                f"{path}: DELETED SINCE THE CARVE — rows[{index}] declares it "
                f"`{row['disposition']}` at {commit[:12]}, and "
                f"{verified_at[:12]} no longer carries it as a file. The "
                "carve ships the bytes at the carve commit, so a source the "
                "tree has since dropped is a move nobody can review at the "
                "destination: re-cut the manifest at a new carve commit, or — "
                f"if this is § 5.2 — declare `phase: {PHASE_POST_SHED}` in the "
                "SAME commit as the deletions")
        if tested[path].mode != referent[path].mode:
            raise CarveRefusal(
                "carve-digest-mismatch",
                f"{path}: MODE DRIFT SINCE THE CARVE — the manifest records "
                f"git_mode {row['git_mode']} at {commit[:12]} and "
                f"{verified_at[:12]} carries {tested[path].mode}. A mode flip "
                "is the one change a blob digest cannot see, and one that "
                "happened after the carve is the § 6 pressure exactly: re-cut "
                "the manifest at a new carve commit")
        if tested[path].oid == referent[path].oid:
            continue
        content = blob_at(repo, verified_at, path)
        # `tested` came from `ls-tree`, which already said blob, so the
        # `<unreadable>` arm is unreachable outside a racing checkout.
        moved_to = (hashlib.sha256(content).hexdigest()
                    if content is not None
                    else "<unreadable>")  # pragma: no cover
        raise CarveRefusal(
            "carve-digest-mismatch",
            f"{path}: CHANGED SINCE THE CARVE\n"
            f"  at carve_commit {commit[:12]}  {row['sha256']}\n"
            f"  at {verified_at[:12]}              {moved_to}\n"
            "the file has moved on since the manifest was cut, so the bytes "
            "the carve would ship are not the bytes this row promises the "
            "destination. This is the § 6 ceremony's intended pressure "
            "and not a defect in it: re-cut the manifest at a new carve "
            "commit and recompute every digest")
    return recomputed


def _check_replica_edit_lines(repo: Path, index: int, row: dict[str, Any],
                              referent: dict[str, TreeEntry],
                              commit: str) -> None:
    """A `replicated_at_destination` row's declared lines, bounded by the SOURCE
    BLOB at `carve_commit` (RULED Q-L7 (a)).

    THE SAME BOUND AS A MOVED ROW'S, from the same bytes, under the same code.
    A replica carries no `sha256` — the row grammar gives a `not_moved` row
    none — so nothing above has read its blob and the read happens here.

    IT KEYS ON THE REASON, not merely on `not_moved` with `edits:`. Under any
    OTHER reason an edit list is check 6's `carve-disposition-inconsistent` —
    a file that arrives nowhere takes no carve edit — and bounding its lines
    here first would report the wrong finding for the same row.

    A PATH THE REFERENT DOES NOT CARRY RETURNS. That is check 4's
    `carve-path-absent` (the surface walk is what reads a `not_moved` row's
    path at all), and a second refusal for it here would depend on which check
    ran first for its code.
    """
    if (row.get("disposition") != "not_moved"
            or row.get("reason") != REPLICA_REASON
            or not row.get("edits")):
        return
    path = row["source_path"]
    if path not in referent:
        return
    content = blob_at(repo, commit, path)
    if content is None:  # pragma: no cover - ls-tree already said blob
        return
    _check_edit_lines(index, path, row, content, commit)


def _check_edit_lines(index: int, path: str, row: dict[str, Any],
                      content: bytes, commit: str) -> None:
    """`edits[].lines` must name lines the blob at `carve_commit` HAS.

    The blob is already in hand from the digest recompute, so the upper bound is
    free. The line numbers are carried for exactly one reason — the memo's, that
    they make the claim "falsifiable at the destination" — and a line past EOF at
    the carve commit is falsifiable here, for nothing.

    `carve-shape-invalid` rather than a code of its own: the `edits[]` entry
    grammar is check 1's (declared there and moved forward deliberately), the
    predicate is the same one — `1 <= line <= <bound>` — with the blob supplying
    the bound that the document alone cannot, and the reader's action is
    identical to every other malformed edits entry. A second code for the same
    action would ask a caller to learn a distinction that changes nothing it does.

    THE BOUND IS COUNTED BY `scripts/carve_lines.py` (RULED Q-L8 (c)) and no
    longer by an expression spelled out here. The count is UNCHANGED — the
    module's `records()` is the same arithmetic, pinned as equal to the old
    expression by `tests/carve_manifest/test_carve_manifest.py` — but it is now
    the SAME implementation `verify-carve-arrival.py` numbers the destination
    with, which is the whole point: this tool issued line numbers in one
    numbering and that one read them in another, and six declared lines over
    two `U+2028`-bearing rows were unappliable at the destination as a result.
    """
    total = carve_lines.count(content)
    for position, edit in enumerate(row.get("edits") or []):
        for line in edit["lines"]:
            if line > total:
                raise CarveRefusal(
                    "carve-shape-invalid",
                    f"rows[{index}].edits[{position}] ({path}) names line "
                    f"{line}, and the blob at {commit[:12]} carries "
                    f"{total} line(s); a declared edit at a line the file does "
                    "not have cannot be checked at the destination, which is "
                    "the whole reason the lines are recorded")


def check_surface(doc: dict, referent: dict[str, TreeEntry],
                  tested: dict[str, TreeEntry], verified_at: str,
                  phase: str = PHASE_CARVE) -> int:
    """Every file under the declared prefixes appears in EXACTLY one row — at
    the referent AND at the revision under test.

    The referent walk proves the manifest COMPLETE about the tree it names; the
    second walk proves it complete about the tree the carve would actually run
    against. The second is the only part of check 2's old identity requirement
    that was ever about a file, and it is the half worth keeping.
    """
    commit = doc["carve_commit"]
    destinations = doc["destinations"]

    # THE PREFIX LIST FIRST. The completeness check below is only as good as
    # `moved_paths:`, and a mistyped prefix (`scripts/ideation_dashbord`)
    # contributes an EMPTY surface while looking like coverage in review — the
    # silent case being the typo and its rows dropped together, which is exactly
    # the hand-editing error a ~430-row manifest invites. Its own code rather
    # than `carve-shape-invalid` because the document is well formed: this is a
    # claim about the TREE, which is why check 1 cannot make it, and the remedy
    # is to re-derive the prefix from the tree rather than to fix a grammar.
    # KEYED ON THE REFERENT, deliberately: `moved_paths:` is a claim about the
    # tree the digests were taken at, and a prefix that has since been emptied
    # on `main` is a DELETION the row-level checks report file by file, not a
    # manifest that declared nothing.
    for entry in doc["moved_paths"]:
        if not any(in_surface(path, [entry]) for path in referent):
            raise CarveRefusal(
                "carve-surface-vacuous",
                f"`moved_paths:` declares {entry!r}, which matches NO file at "
                f"{commit[:12]}. A prefix that names nothing declares nothing, "
                "and the completeness check cannot report a file that no prefix "
                "reaches — so a dead prefix reads as coverage and provides none")
    surface = {p for p in referent if in_surface(p, doc["moved_paths"])}

    seen: dict[str, int] = {}
    for index, row in enumerate(doc["rows"]):
        path = row["source_path"]
        if path in seen:
            raise CarveRefusal(
                "carve-file-duplicated",
                f"{path} appears in rows[{seen[path]}] AND rows[{index}]; a "
                "file has exactly one disposition and exactly one destination, "
                "and a file with two rows has neither")
        seen[path] = index

    # The DESTINATION side of the same question. `seen` guarantees completeness
    # and uniqueness on the SOURCE side only, so two source files may otherwise
    # claim one destination path — at which point one overwrites the other at
    # the destination and the manifest, read as the carve's instruction sheet,
    # does not say which arrives.
    #
    # Keyed on the REAL arrival — `destinations[key]`'s `(repository, leg)`
    # body plus `destination_path` — and NOT on the row's `destination` ALIAS.
    # `destinations:` may legally carry two keys with an identical
    # `{repository, leg}` body (check_shape does not refuse that — see its own
    # comment for why), so two rows naming the two DIFFERENT keys with one
    # shared `destination_path` used to pass silently, keyed as two distinct
    # aliases rather than as the one real destination they are — exactly the
    # "one of them overwrites the other" outcome `carve-file-duplicated`
    # exists to refuse (S8, RE-VERIFICATION of `d97371d1`, 2026-09-09). A
    # `destination` that names no key of `destinations:` is check 5's
    # `carve-vocabulary-unknown` (check 4 runs first): fall back to keying on
    # the alias itself rather than crash ahead of it, in a shape (a 1-tuple)
    # that can never collide with a resolved `(repository, leg, path)` key.
    #
    # AND KEYED ON THE EFFECTIVE ARRIVAL (RULED Q6): where a row carries
    # `re_destined:`, the path it collides at is the one it arrives at TODAY,
    # not the one the carve placed it at. Keying on the original would be
    # wrong in both directions at once — a row re-destined AWAY from a path
    # would go on reserving it, so a second row moving to the vacated path
    # would refuse as a duplicate; and a re-destined row landing on an
    # occupied path would pass in silence, which is exactly the overwrite this
    # check exists to refuse. The SURFACE walk below is untouched by the
    # field: it is a claim about SOURCE paths, and a re-destination moves
    # nothing at the source.
    #
    # WHAT THIS DOES NOT ASK, stated because a floor that overstates its reach
    # is worse than one that does not reach: whether a row re-destined AWAY
    # from a path leaves it free. Keying a SECOND map on the original arrivals
    # would refuse the lawful case this field exists for — one row vacating a
    # path and another moving into it is two rows agreeing, not colliding — so
    # a row re-destined off a path some other row still occupies is answered
    # at the destination instead, where the file either is or is not there:
    # `verify-carve-arrival.py`'s `arrival-not-vacated`.
    arrivals: dict[tuple[str, ...], int] = {}
    for index, row in enumerate(doc["rows"]):
        if row.get("disposition") not in MOVED_DISPOSITIONS:
            continue
        dest_key, dest_path = effective_arrival(row)
        dest_entry = destinations.get(dest_key)
        if dest_entry is not None:
            arrival = (dest_entry["repository"], dest_entry["leg"], dest_path)
            where = f"{dest_entry['repository']} ({dest_entry['leg']})"
        else:
            arrival = (dest_key,)
            where = dest_key
        if arrival in arrivals:
            raise CarveRefusal(
                "carve-file-duplicated",
                f"rows[{arrivals[arrival]}] AND rows[{index}] both send a file "
                f"to the DESTINATION {where}:{dest_path}; two "
                "sources arriving at one real destination path means one of "
                "them overwrites the other, and the manifest does not say "
                "which — even across two DIFFERENT `destination` keys that "
                "declare the same repository and leg, and counting a "
                "`re_destined:` row at the placement it arrives at TODAY "
                "rather than the one the carve made")
        arrivals[arrival] = index

    undeclared = sorted(surface - set(seen))
    if undeclared:
        raise CarveRefusal(
            "carve-file-undeclared",
            f"the carve surface at {commit[:12]} carries {len(undeclared)} "
            "file(s) that NO row declares: "
            + ", ".join(undeclared[:10])
            + (" …" if len(undeclared) > 10 else "")
            + " — a file in no row is an UNDECLARED MOVEMENT and the carve "
              "refuses (RULING OQ-1)")
    absent = sorted(set(seen) - surface)
    if absent:
        raise CarveRefusal(
            "carve-path-absent",
            f"the manifest declares {len(absent)} row(s) for path(s) the "
            f"carve surface at {commit[:12]} does not carry: "
            + ", ".join(absent[:10]) + (" …" if len(absent) > 10 else ""))

    # THE SAME TWO QUESTIONS AT THE REVISION UNDER TEST. Both are no-ops when
    # the two revisions coincide — `tested` IS `referent` then, so the two set
    # differences below are the two already taken above, and both were empty or
    # this line is unreachable.
    tested_surface = {p for p in tested if in_surface(p, doc["moved_paths"])}
    appeared = sorted(tested_surface - surface)
    if appeared:
        raise CarveRefusal(
            "carve-file-undeclared",
            f"{len(appeared)} file(s) have APPEARED under the carve surface "
            f"since {commit[:12]} and no row declares them at "
            f"{verified_at[:12]}: "
            + ", ".join(appeared[:10])
            + (" …" if len(appeared) > 10 else "")
            + " — a file in no row is an UNDECLARED MOVEMENT and the carve "
              "refuses (RULING OQ-1). The manifest describes a surface the "
              "tree has grown past: re-cut it at a new carve commit")
    # THE SHED SET, derived from the rows and never from a second list. Under
    # `post-shed` these paths are the ones the § 5.2 shed deletes BY
    # CONSTRUCTION — every moved row, plus the one `deleted_at_carve` row — so
    # the manifest computes its own expected absence set and nothing has to be
    # kept in step with it by hand. Under `carve` the set is empty and both
    # arms below read exactly as they did.
    shed_set: set[str] = set()
    if phase == PHASE_POST_SHED:
        shed_set = {row["source_path"] for row in doc["rows"]
                    if row.get("disposition") in MOVED_DISPOSITIONS
                    or row.get("reason") == "deleted_at_carve"}

    vanished = sorted((surface - tested_surface) - shed_set)
    if vanished:
        raise CarveRefusal(
            "carve-path-absent",
            f"{len(vanished)} row(s) name path(s) DELETED SINCE THE CARVE — "
            f"under the surface at {commit[:12]}, absent at "
            f"{verified_at[:12]}: "
            + ", ".join(vanished[:10])
            + (" …" if len(vanished) > 10 else "")
            + ". Check 3 reports this for a MOVED row, with its digest; this "
              "is what reports it for a `not_moved` row, which the digest "
              "loop never reads at all"
            + (". Under `phase: post-shed` a MOVED row and the "
               "`deleted_at_carve` row are EXPECTED to be gone and are not "
               "counted here — every row named above is a row that STAYS, and "
               "the shed does not reach it"
               if phase == PHASE_POST_SHED else ""))

    # THE MIRROR ARM, and it exists for the `deleted_at_carve` row alone —
    # check 3's own post-shed arm has already refused every MOVED row that is
    # still present, and it runs first. That is the same split this check
    # already keeps in the other direction: the digest loop never reads a
    # `not_moved` row, so its absence, and now its presence, is reported here.
    if phase == PHASE_POST_SHED:
        still_here = sorted(shed_set & tested_surface)
        if still_here:
            raise CarveRefusal(
                "carve-shed-incomplete",
                f"the manifest declares `phase: {PHASE_POST_SHED}` and "
                f"{verified_at[:12]} still carries {len(still_here)} of the "
                "path(s) the shed removes: "
                + ", ".join(still_here[:10])
                + (" …" if len(still_here) > 10 else "")
                + ". The phase and the deletions are one act (runbook § 8) "
                  "and this is that sentence as running code")
    return len(surface)


def check_vocabularies(doc: dict) -> None:
    destinations = doc["destinations"]
    declared_classes = doc["edit_classes"]
    declared_reasons = doc["not_moved_reasons"]
    for index, row in enumerate(doc["rows"]):
        where = f"rows[{index}] ({row['source_path']})"
        disposition = row["disposition"]
        if disposition not in DISPOSITIONS:
            raise CarveRefusal(
                "carve-vocabulary-unknown",
                f"{where} declares `disposition: {disposition!r}`; the list is "
                f"CLOSED at {list(DISPOSITIONS)!r} (RULED OQ-C — three, and "
                "the `not_moved` reason carries any nuance the three cannot)")
        destination = row.get("destination")
        if destination is not None and destination not in destinations:
            raise CarveRefusal(
                "carve-vocabulary-unknown",
                f"{where} declares `destination: {destination!r}`, which is "
                f"not a key of `destinations:` ({sorted(destinations)!r})")
        # THE SAME MEMBERSHIP TEST, for the same reason, on the row's replica
        # destinations (RULED Q-L7 (a)): `destinations:` is closed because one
        # typo otherwise ships a file to a repository nobody declared, and a
        # replica of a moved row is shipped by exactly the same act.
        for position, key in enumerate(row.get("also_replicated_to") or []):
            if key not in destinations:
                raise CarveRefusal(
                    "carve-vocabulary-unknown",
                    f"{where}.also_replicated_to[{position}] declares "
                    f"{key!r}, which is not a key of `destinations:` "
                    f"({sorted(destinations)!r}). The row says these bytes "
                    "ALSO arrive there as a replica, and an arrival at a "
                    "destination nobody declared is the typo the closed map "
                    "exists to refuse")
        # THE SAME MEMBERSHIP TEST AGAIN, on a re-destination's two ends
        # (RULED Q6). `to` is where the floor now asks for the file, so a key
        # nobody declared sends it to a repository nobody declared; `from` is
        # where `verify-carve-arrival.py` requires it ABSENT, so an unknown key
        # there is a vacation nobody can check. Check 6 is what holds `from` to
        # the row's OWN destination — this is only the closed map.
        re_destined = row.get("re_destined")
        if isinstance(re_destined, dict):
            for key in ("from", "to"):
                value = re_destined.get(key)
                if value is not None and value not in destinations:
                    raise CarveRefusal(
                        "carve-vocabulary-unknown",
                        f"{where}.re_destined.{key} declares {value!r}, which "
                        "is not a key of `destinations:` "
                        f"({sorted(destinations)!r}). A re-destination moves "
                        "an arrival between two DECLARED destinations; one "
                        "typo otherwise re-homes a file to a repository "
                        "nobody declared")
        for position, edit in enumerate(row.get("edits") or []):
            if edit["class"] not in declared_classes:
                raise CarveRefusal(
                    "carve-vocabulary-unknown",
                    f"{where}.edits[{position}] declares "
                    f"`class: {edit['class']!r}`, which is not one of "
                    f"{list(EDIT_CLASSES)!r}. An edit in no class is an "
                    "UNDECLARED MOVEMENT and the carve refuses (RULING OQ-1)")
        reason = row.get("reason")
        if reason is not None and reason not in declared_reasons:
            raise CarveRefusal(
                "carve-vocabulary-unknown",
                f"{where} declares `reason: {reason!r}`, which the manifest's "
                f"own `not_moved_reasons:` ({list(declared_reasons)!r}) does "
                "not carry")


def _check_re_destined_consistency(where: str, row: dict[str, Any]) -> None:
    """A re-destination must agree with the row it sits on (RULED Q6).

    `from`/`from_path` ARE THE ROW'S OWN `destination`/`destination_path`, and
    the row keeps both unedited — which is the whole reason this is a FIELD and
    not an edit of the two it names. The manifest goes on recording where the
    carve actually put the file, `verify-carve-arrival.py` knows which path to
    require ABSENT at the losing leg, and a reader can see the correction and
    the thing corrected in one row. A `from` naming some third destination is
    therefore not a harmless restatement: it would ask the vacation question of
    a leg this row never placed anything at.

    `to` MAY NOT EQUAL `from`. A re-destination that lands where it started
    declares nothing and would make every arrival question below read twice for
    one answer; and since `from` is the row's own destination, the ruling's
    "`to` (a `destinations:` key ≠ from)" is the same sentence as "a
    re-destination moves the file to another leg". A file that moves to a new
    PATH at the same leg is not this form — nothing about its destination
    changed, and the row's own `destination_path` is the field that says where
    it lands.
    """
    re_destined = row.get("re_destined")
    if not isinstance(re_destined, dict):
        return
    source_path = row["source_path"]
    for key, own in (("from", "destination"), ("from_path", "destination_path")):
        if re_destined.get(key) != row.get(own):
            raise CarveRefusal(
                "carve-disposition-inconsistent",
                f"{where} declares `re_destined.{key}: "
                f"{re_destined.get(key)!r}` where its own `{own}:` is "
                f"{row.get(own)!r}. A re-destination names the placement it "
                "CORRECTS, and the placement this row made is its own "
                f"`{own}:` — a `{key}` naming anything else asks the floor "
                "about an arrival this row never declared. The row keeps "
                "`destination`/`destination_path` unedited on purpose: the "
                "manifest goes on recording what the carve did, and "
                "`re_destined:` records what a ruling did afterwards")
    if re_destined.get("to") == re_destined.get("from"):
        raise CarveRefusal(
            "carve-disposition-inconsistent",
            f"{where} declares `re_destined:` from {re_destined.get('from')!r} "
            "to the same destination. RULED Q6 makes `to` a `destinations:` "
            "key that is NOT `from`: a re-destination that lands where it "
            "started declares nothing, and it would make every arrival "
            "question read the row twice for one answer. If only the PATH "
            f"changes at {re_destined.get('from')!r}, that is not this form — "
            "the row's own `destination_path:` is what says where the file "
            f"lands at its destination, and {source_path} has not been "
            "re-homed at all")


def _check_re_destined_chains(doc: dict) -> None:
    """No row's `(to, to_path)` may be another row's `(from, from_path)`.

    RULED Q6, verbatim: "refuses a chain (a row already re-destined is AMENDED
    in place, never re-destined twice, so one row never needs two readings)".

    WHAT A CHAIN ACTUALLY LOOKS LIKE, since one row cannot carry two
    `re_destined:` blocks. Row A is re-destined from X to Y at path P, and row
    B is re-destined FROM Y at that same P — so the arrival A created is the
    arrival B moves on. A reader then has to compose two hops across two rows
    to learn where ONE file is, the vacation checks at Y disagree with each
    other (A's arrival requires the file PRESENT there, B's vacation requires
    it ABSENT), and the ruling that ordered the second move is recorded on a
    row that is not the file's. The remedy is the ruling's own: amend row A's
    `re_destined:` in place to name the destination the file actually ends at,
    citing the later ruling.

    KEYED ON `(destination key, path)` AND NOT ON THE KEY ALONE: two files may
    lawfully be re-destined off one leg, and two more onto it. What may not
    happen is a second re-destination LEAVING the exact arrival a first one
    CREATED.
    """
    origins: dict[tuple[str, str], int] = {}
    for index, row in enumerate(doc["rows"]):
        re_destined = row.get("re_destined")
        if not isinstance(re_destined, dict):
            continue
        origin = (re_destined.get("from"), re_destined.get("from_path"))
        if all(isinstance(part, str) for part in origin):
            origins.setdefault(origin, index)  # type: ignore[arg-type]
    for index, row in enumerate(doc["rows"]):
        re_destined = row.get("re_destined")
        if not isinstance(re_destined, dict):
            continue
        arrival = (re_destined.get("to"), re_destined.get("to_path"))
        other = origins.get(arrival)  # type: ignore[arg-type]
        if other is None or other == index:
            continue
        raise CarveRefusal(
            "carve-re-destined-chain",
            f"rows[{index}] ({row['source_path']}) is re-destined TO "
            f"{arrival[0]}:{arrival[1]}, which rows[{other}] "
            f"({doc['rows'][other]['source_path']}) is re-destined FROM. That "
            "is a CHAIN, and RULED Q6 refuses it: a row already re-destined is "
            "AMENDED IN PLACE, never re-destined twice, so one row never needs "
            "two readings. As written the two rows also contradict each other "
            "at that destination — one requires the file PRESENT there and the "
            "other requires it ABSENT. Amend the earlier row to name the "
            "destination the file actually ends at, citing the later ruling")


def check_disposition_consistency(doc: dict) -> None:
    for index, row in enumerate(doc["rows"]):
        where = f"rows[{index}] ({row['source_path']})"
        disposition = row["disposition"]
        edits = row.get("edits") or []
        reason = row.get("reason")
        if disposition == "moved_with_declared_edit" and not edits:
            raise CarveRefusal(
                "carve-disposition-inconsistent",
                f"{where} is `moved_with_declared_edit` with no `edits:`; that "
                "is `moved_verbatim` mislabelled, and a manifest whose "
                "dispositions do not distinguish is the label without the "
                "floor")
        if disposition == "moved_verbatim" and edits:
            raise CarveRefusal(
                "carve-disposition-inconsistent",
                f"{where} is `moved_verbatim` and declares {len(edits)} "
                "edit(s); verbatim means the destination's bytes equal this "
                "digest, which a declared edit contradicts")
        # RULED Q-L7 (a): the ONE reason under which a `not_moved` row's edits
        # are not a contradiction. A replica's bytes DO arrive — a copy at each
        # destination, retained here — so a line the copy must differ on is a
        # declarable carve edit, applied identically at every replica. Under
        # every other reason the bytes arrive nowhere and the old finding
        # stands, which is what keeps RULING OQ-B's three
        # `stays_openxfactory_governance` rows recording their rewrite in
        # EVIDENCE rather than in `edits:`.
        if disposition == "not_moved" and edits and reason != REPLICA_REASON:
            raise CarveRefusal(
                "carve-disposition-inconsistent",
                f"{where} is `not_moved / {reason}` and declares {len(edits)} "
                "edit(s); a file that arrives nowhere takes no carve edit. "
                f"RULED Q-L7 (a) admits `edits:` on a `{REPLICA_REASON}` row "
                "ONLY, because that is the one reason whose bytes do arrive — "
                "a copy at each destination, where a declared line is applied "
                "identically. A file that STAYS and is rewritten HERE records "
                "the rewrite in its `evidence:` (RULING OQ-B's "
                "`tests/notebooklm/*` rows), because openxFactory's own tree "
                "is not a carve destination")
        own = row.get("destination")
        for key in row.get("also_replicated_to") or []:
            if key == own:
                raise CarveRefusal(
                    "carve-disposition-inconsistent",
                    f"{where} moves to `destination: {own!r}` and lists that "
                    "same key in `also_replicated_to:`. The row already places "
                    "the file there, at its own `destination_path` — ALSO "
                    "means somewhere else, and a row replicating a file at the "
                    "destination it moves to would let `--replica-at` re-point "
                    "an arrival the manifest has already declared, which is "
                    "the one thing the manifest is for")
        _check_re_destined_consistency(where, row)

    _check_re_destined_chains(doc)

    # `path_order: bytewise_utf8` is a claim about THIS document, and a const
    # nothing enforces is a comment. Bytewise on the UTF-8 encoding, not on
    # Python's code points, because that is what the const names and what git
    # and `sort` agree on.
    paths = [row["source_path"] for row in doc["rows"]]
    # `surrogateescape` on the ENCODE, not only on the decode that produced
    # these strings: a path is bytes, and a repository carrying a non-UTF-8 one
    # would otherwise raise `UnicodeEncodeError` out of this comparison and end
    # the process with a traceback and exit 1 — the exit code this file's
    # docstring says does not exist. The refusal must stay a refusal even for
    # the paths git can name and Unicode cannot.
    ordered = sorted(paths, key=lambda p: p.encode("utf-8", "surrogateescape"))
    if paths != ordered:
        first = next(i for i, (a, b) in enumerate(zip(paths, ordered)) if a != b)
        raise CarveRefusal(
            "carve-path-order-violation",
            f"the rows are not in `path_order: bytewise_utf8`; rows[{first}] "
            f"is {paths[first]!r} where the bytewise order puts "
            f"{ordered[first]!r}. A ~430-row manifest is reviewed by diff, and "
            "a diff of an unsorted file hides a moved row inside a reordering")


# --------------------------------------------------------------------------
# the run
# --------------------------------------------------------------------------

def validate(manifest_path: Path, repo: Path,
             at: str | None) -> dict[str, Any]:
    """The six checks in order, first failure wins.

    TWO REVISIONS travel through checks 3 and 4: the REFERENT the manifest
    names, and the revision UNDER TEST that check 2 proved descends from it.
    """
    doc = read_manifest(manifest_path)
    check_shape(doc)
    # READ AFTER CHECK 1 and never before it: check 1 is what has just proved
    # this is one of the two phases, and a value read ahead of its own
    # validation is the branch a typo selects.
    phase = doc.get("phase", PHASE_CARVE)
    verified_at = check_revision(repo, doc, at)
    commit = doc["carve_commit"]
    referent = tree_at(repo, commit)
    # ONE `ls-tree` when the two revisions coincide — the ceremony's own run at
    # the carve commit, and every `--at <carve_commit>`. The second listing
    # would be the first, record for record, and sharing the object makes every
    # comparison against it an identity rather than a branch to be trusted.
    tested = referent if verified_at == commit else tree_at(repo, verified_at)
    recomputed = check_digests(repo, doc, referent, tested, verified_at, phase)
    surface = check_surface(doc, referent, tested, verified_at, phase)
    check_vocabularies(doc)
    check_disposition_consistency(doc)

    counts = {d: 0 for d in DISPOSITIONS}
    for row in doc["rows"]:
        counts[row["disposition"]] += 1
    shed = sum(1 for row in doc["rows"]
               if row.get("disposition") in MOVED_DISPOSITIONS
               or row.get("reason") == "deleted_at_carve")
    # COUNTED AND PRINTED ON EVERY RUN (RULED Q6), in both the JSON and the
    # human line and whether the number is 0 or 48: a placement corrected by a
    # ruling is the one thing in this document that is not the carve's own act,
    # and a reader of a CI log must be able to see how many of them the
    # manifest now carries without opening it. Zero is the state the file
    # landed in and is as much a fact as any other.
    re_destined = sum(1 for row in doc["rows"]
                      if isinstance(row.get("re_destined"), dict))
    return {
        "result": "ok",
        "manifest": str(manifest_path),
        "phase": phase,
        "shed_rows": shed if phase == PHASE_POST_SHED else 0,
        "carve_commit": commit,
        "verified_at": verified_at,
        "carve_tag": doc["carve_tag"],
        "source_repository": doc["source_repository"],
        "rows": len(doc["rows"]),
        "dispositions": counts,
        "digests_recomputed": recomputed,
        "surface": surface,
        "re_destined": re_destined,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate-carve-manifest.py",
        description=("Verify docs/opendox-carve-manifest.yaml — FLOOR PART 1 "
                     "of the RULED four-part floor (split-opendox § D6)."),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--manifest", metavar="PATH", default=None,
        help=f"the manifest to verify (default: <repo>/{MANIFEST_RELPATH})")
    parser.add_argument(
        "--repo", metavar="DIR", default=None,
        help="the git repository the digests are taken in (default: this one)")
    parser.add_argument(
        "--at", metavar="SHA", default=None,
        help=("verify against this revision instead of HEAD; the manifest's "
              "carve_commit must be an ANCESTOR of it"))
    parser.add_argument(
        "--json", action="store_true",
        help="print one JSON object on stdout instead of the human line")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve() if args.repo else ROOT
    # A RELATIVE `--manifest` is resolved against `--repo`, not the caller's
    # CWD: the help text already says "default: <repo>/…", and a relative
    # override that silently changed referent to CWD would point at the wrong
    # file the moment `--repo` names a tree other than the one the caller is
    # standing in. An ABSOLUTE `--manifest` is untouched — there is no `repo`
    # to resolve it against. Either way the result is `.resolve()`d, so every
    # message below — `NO MANIFEST`, `OK`, a refusal's render, `--json` —
    # prints the one absolute path that was actually read, not a caller-typed
    # fragment a reader would have to re-derive the CWD to interpret.
    if args.manifest:
        manifest_arg = Path(args.manifest)
        manifest_path = (manifest_arg if manifest_arg.is_absolute()
                         else repo / manifest_arg).resolve()
    else:
        manifest_path = (repo / MANIFEST_RELPATH).resolve()

    # THE SEAT-HOLDING PASS, and the one place here that is not fail-closed.
    # See the module docstring: this validator lands BEFORE its subject.
    #
    # IT KEYS OFF `args.manifest is None`, not off the file's absence alone. The
    # pass is right for the DEFAULT path and wrong for a NAMED one: a job that
    # typos `--manifest docs/carve-manifest.yaml`, or the memo's own one-shot
    # step in the carve PR after the file is renamed, would otherwise select the
    # single not-fail-closed branch in this file and go green forever — for a
    # manifest nobody validated. A named absent path is `carve-unreadable`
    # (below, inside the refusal handler): the environment could not hand this
    # program a document, which is that code's half of the split.
    if args.manifest is None and not manifest_path.is_file():
        if args.json:
            print(json.dumps({"result": "no-manifest",
                              "manifest": str(manifest_path)}))
        else:
            print(f"NO MANIFEST {manifest_path} (nothing to validate)")
        return 0

    try:
        if not manifest_path.is_file():
            raise CarveRefusal(
                "carve-unreadable",
                f"--manifest {args.manifest!r} names {manifest_path}, which is "
                "not a file. The seat-holding pass covers the DEFAULT path "
                f"({MANIFEST_RELPATH}) only, before the § 6 ceremony authors "
                "it; it does not extend to a manifest the caller named, because "
                "a typo must not be indistinguishable from `not yet written`")
        summary = validate(manifest_path, repo, args.at)
    except CarveRefusal as exc:
        if args.json:
            print(json.dumps({"result": "refused", "code": exc.code,
                              "detail": exc.detail,
                              "manifest": str(manifest_path)}))
        else:
            print(exc.render(manifest_path), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(summary))
    else:
        counts = summary["dispositions"]
        # BOTH REVISIONS ARE NAMED WHEN THEY DIFFER, and only then: the carve
        # commit alone is the whole answer on the ceremony's own run, and a
        # reader of a pull-request log needs to know that `OK` was reached at
        # the merge ref and not only at the referent.
        where = (f"{summary['source_repository']}@"
                 f"{summary['carve_commit'][:12]} ({summary['carve_tag']})")
        if summary["verified_at"] != summary["carve_commit"]:
            where += f", verified at {summary['verified_at'][:12]}"
        # THE PHASE IS PRINTED ON EVERY RUN, in both phases and not only in
        # the new one. A reader of a CI log must be able to tell WHICH
        # semantics answered `OK` without opening the manifest, and a line
        # that says nothing under the default would make the default the one
        # state no log records. It is also what lets the § 8.2 seat assert
        # that the run took the branch the file declares rather than merely
        # exiting 0.
        shed_note = (f"; {summary['shed_rows']} shed row(s) absent at source "
                     "as declared"
                     if summary["phase"] == PHASE_POST_SHED else "")
        # THE RE-DESTINATION COUNT IS A CLAUSE OF ITS OWN and not a suffix on
        # the disposition counts: a re-destined row keeps its disposition, so
        # adding it there would double-count a row that is still exactly one
        # `moved_verbatim` or `moved_with_declared_edit`.
        re_destined_note = (
            f"; {summary['re_destined']} row(s) RE-DESTINED by ruling "
            "(RULED Q6)" if summary["re_destined"] else "")
        print(f"OK {manifest_path}: phase {summary['phase']}, "
              f"{summary['rows']} row(s) at "
              f"{where} — "
              f"{counts['moved_verbatim']} moved_verbatim, "
              f"{counts['moved_with_declared_edit']} moved_with_declared_edit, "
              f"{counts['not_moved']} not_moved; "
              f"{summary['digests_recomputed']} digest(s) recomputed; "
              f"{summary['surface']} file(s) in the declared surface with none "
              "undeclared" + shed_note + re_destined_note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
