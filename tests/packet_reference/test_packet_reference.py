"""A PACKET REFERENCE RESOLVES BY IDENTITY, NOT BY PATH (issue #833,
`add-declared-former-id` §§ 5.1, 5.1a, 5.2, 5.2a).

WHAT THE SUBJECT IS FOR, MEASURED RATHER THAN ASSERTED. Every packet in this
corpus relocates exactly once — `openspec/changes/<id>/` becomes
`openspec/changes/archive/<YYYY-MM-DD>-<id>/` — and every record that cited it
by path goes stale at that moment, by an act nobody thinks of as breaking
anything. The estate already has a reader that REFUSES on such a path
(`scripts/validate-pin-registrations.py`'s `check_citations`, landed for issue
#840), and on the tree this suite was written against SIX of its in-tree
referents point into FOUR ACTIVE packets — `prepare-openspec-1-12-readiness`
(x2), `add-chain-attestation`,
`disposition-codexfactory-floor-relocation-retitle`, and
`disposition-codexfactory-regular-pr-council-clearance-archive` (x2). The next
of those four to archive turns a lawful act into an exit-1 refusal of a gate
nobody touched. `scripts/packet_reference.py` is the reader that answers by
IDENTITY instead, and this file is its lane.

THE FOUR OUTCOMES ARE SEPARATED HERE, ONE TEST EACH, because a resolver that
collapses any two of them is the defect rather than the fix:

  * RESOLVED — the id stands somewhere (active, archived, or declared as a
    former identity by some packet) AND that packet carries the cited file.
    A reference that resolves owes the citing record NO EDIT.
  * DANGLING at the IDENTITY half — the id stands nowhere at all. A defect of
    the citing record.
  * DANGLING at the FILE half — the id stands, and the packet it stands in does
    not carry the remainder the citation names. Reported AGAINST THE FILE and
    never against the packet, because resolving the identity alone would accept
    a citation to a file deleted, renamed or never written.
  * AMBIGUOUS — the id would stand in more than one place. Never settled by
    preferring a candidate, and the defect belongs to the DECLARATION that made
    one identity resolve twice rather than to the citing record.

AND A FIFTH ANSWER THAT IS NOT AN OUTCOME AT ALL: a path that addresses no
packet is left to the caller's own path resolution, unchanged. That boundary is
load-bearing and has its own tests — `openspec/changes/README.md` is a real file
whose second segment is not a packet id, and a resolver that read it as one
would report this corpus's own README dangling.

THE CROSS-REPOSITORY CASE IS NOT DECIDED HERE, on purpose (§ 5.2). This module
resolves against THE ROOT IT IS GIVEN and holds no repository vocabulary at all;
the classification that keeps another repository's packet out of scope lives in
the caller (`read_citation`'s `qualified` kind) and § 5.2 leaves it exactly
where it is. `test_a_reference_to_another_repository_is_out_of_scope` pins that
boundary from this side: the same path answers differently against two roots, so
the resolver is structurally incapable of making that call.

FIXTURES ARE BUILT IN `tmp_path`, on `tests/pin_registrations/`'s stated
precedent: a committed broken packet is a file every other sweep has to be
taught to ignore, while a scratch tree is read by this test alone. THE ONE
EXCEPTION IS THE CORPUS SWEEP — `test_every_packet_in_this_corpus_resolves_to_
exactly_itself` — which reads the 47 active and 167 archived packets this
repository really carries, because a resolver proved only against invented trees
is proved against the author's imagination.

Hermetic: no network, no `nlm`/`gh`/`omp`, no subprocess at all. The subject is
loaded by location, the way `tests/pin_registrations/` loads its own — it is a
sibling of a hyphenated script and reaches one.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SUBJECT = REPO_ROOT / "scripts" / "packet_reference.py"
SUPPORT = REPO_ROOT / "scripts" / "proposal-support.py"

#: The four active packets the live pin cites into, measured on the tree this
#: suite was written against. Named rather than counted, so that a citation
#: retargeted away from one of them reds HERE — with its reason — instead of
#: quietly emptying the claim this module's docstring makes.
CITED_ACTIVE_PACKETS = (
    "add-chain-attestation",
    "disposition-codexfactory-floor-relocation-retitle",
    "disposition-codexfactory-regular-pr-council-clearance-archive",
    "prepare-openspec-1-12-readiness",
)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader, f"cannot load {path}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pr = _load("packet_reference_under_test", SUBJECT)
support = _load("proposal_support_for_packet_reference", SUPPORT)


# --------------------------------------------------------------------------
# Fixture builders
# --------------------------------------------------------------------------

def _packet(root: Path, rel: str, *, files=("proposal.md",),
            former_ids=None, packet_yaml: dict | None = None) -> Path:
    """One packet directory under `root`, with its `.openspec.yaml`.

    `former_ids` is written as a TOP-LEVEL SIBLING of `origin:` — the position
    `former_id_problems` calls normative — so a fixture can never accidentally
    assert against a declaration the estate's own reader would refuse.
    """
    directory = root / rel
    directory.mkdir(parents=True, exist_ok=True)
    for name in files:
        member = directory / name
        member.parent.mkdir(parents=True, exist_ok=True)
        member.write_text(f"# {name}\n", encoding="utf-8")
    document: dict = packet_yaml if packet_yaml is not None else {
        "schema": "spec-driven",
        "created": "2026-09-14",
        "origin": {"kind": "adhoc", "id": "openxFactory:adhoc:fixture"},
    }
    if former_ids is not None:
        document[support.FORMER_IDS_KEY] = list(former_ids)
    (directory / ".openspec.yaml").write_text(
        yaml.safe_dump(document, allow_unicode=True, sort_keys=False),
        encoding="utf-8")
    return directory


def _tree(tmp_path: Path) -> Path:
    (tmp_path / "openspec" / "changes" / "archive").mkdir(parents=True)
    return tmp_path


def _outside_packet(tmp_path: Path, name: str, *, files=("proposal.md",),
                     former_ids=None) -> Path:
    """A packet directory built OUTSIDE `tmp_path`, so a fixture can link a
    tree entry to it and measure what a reader that followed the link would
    see. Sibling of `_packet`, deliberately rooted somewhere the subject is
    never handed as `root` — a directory next to `tmp_path` rather than under
    it, which pytest's own base temp directory makes free to use without
    reaching past it into anything this suite does not own.
    """
    outside_root = tmp_path.parent / f"{tmp_path.name}-outside"
    return _packet(outside_root, name, files=files, former_ids=former_ids)


# --------------------------------------------------------------------------
# The six scenarios of `A packet reference resolves by identity, not by path`
# --------------------------------------------------------------------------

def test_a_cited_path_naming_a_packet_that_has_since_archived_resolves_by_id(
        tmp_path) -> None:
    """Scenario: *A cited path names a packet that has since archived*.

    The one act every packet performs exactly once, and the reason this
    requirement exists at all.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/archive/2026-09-01-add-a-thing",
            files=("proposal.md", "evidence/run.md"))

    resolution = pr.resolve(root, "openspec/changes/add-a-thing/evidence/run.md")

    assert resolution.status == pr.RESOLVED, resolution.report
    assert not (root / "openspec/changes/add-a-thing/evidence/run.md").exists()
    assert resolution.identity == "add-a-thing"
    assert resolution.remainder == "evidence/run.md"
    assert resolution.location.rel == (
        "openspec/changes/archive/2026-09-01-add-a-thing")
    assert resolution.location.kind == pr.ARCHIVED
    assert resolution.resolved_rel == (
        "openspec/changes/archive/2026-09-01-add-a-thing/evidence/run.md")
    assert resolution.relocated is True


def test_a_cited_path_naming_a_declared_former_id_resolves_to_that_packet(
        tmp_path) -> None:
    """Scenario: *A cited path names an id a packet declares as a former id*.

    AND THE DECLARATION IS WHAT AUTHORIZES IT, A PATH SIMILARITY NEVER BEING
    ONE: the neighbour below carries a name that merely LOOKS like the cited id
    and declares nothing, and it is not the packet the reference resolves to.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/add-the-new-name",
            files=("proposal.md", "tasks.md"),
            former_ids=["add-the-old-name"])
    _packet(root, "openspec/changes/add-the-old-name-ish",
            files=("proposal.md", "tasks.md"))

    resolution = pr.resolve(root, "openspec/changes/add-the-old-name/tasks.md")

    assert resolution.status == pr.RESOLVED, resolution.report
    assert resolution.location.rel == "openspec/changes/add-the-new-name"
    assert resolution.location.kind == pr.DECLARED
    assert support.FORMER_IDS_KEY in resolution.location.why
    assert "add-the-old-name-ish" not in resolution.report


def test_a_cited_path_resolving_to_no_identity_at_all_is_dangling(
        tmp_path) -> None:
    """Scenario: *A cited path resolves to no identity at all*.

    No active directory, no dated archive directory, no declared former id —
    and the report says all three were asked, because a reader repairing the
    citation needs to know the identity was looked for and not merely the path.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/add-something-else")

    resolution = pr.resolve(root, "openspec/changes/add-a-ghost/proposal.md")

    assert resolution.status == pr.DANGLING, resolution.report
    assert resolution.half == pr.IDENTITY_HALF
    assert resolution.location is None
    assert "add-a-ghost" in resolution.report
    assert support.FORMER_IDS_KEY in resolution.report
    assert "archive" in resolution.report


def test_an_identity_that_resolves_with_a_missing_file_names_the_file_half(
        tmp_path) -> None:
    """Scenario: *The identity resolves and the cited file does not*.

    § 5.1a's two fixtures, both of them: a LIVE id with a deleted remainder, and
    an ARCHIVED id whose remainder moved INSIDE the packet. Resolving the
    identity alone would accept both, which is the defect this half exists to
    find — spelled at a finer grain than the one the archive relocation breaks.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/add-a-live-one",
            files=("proposal.md", "tasks.md"))
    _packet(root, "openspec/changes/archive/2026-09-02-add-a-moved-one",
            files=("proposal.md", "evidence/2026/run.md"))

    deleted = pr.resolve(root, "openspec/changes/add-a-live-one/design.md")
    assert deleted.status == pr.DANGLING, deleted.report
    assert deleted.half == pr.FILE_HALF
    assert deleted.location.rel == "openspec/changes/add-a-live-one"
    assert "design.md" in deleted.report

    moved = pr.resolve(root, "openspec/changes/add-a-moved-one/evidence/run.md")
    assert moved.status == pr.DANGLING, moved.report
    assert moved.half == pr.FILE_HALF
    assert moved.location.rel == (
        "openspec/changes/archive/2026-09-02-add-a-moved-one")
    assert "evidence/run.md" in moved.report


def test_a_reference_to_another_repository_is_out_of_scope(tmp_path) -> None:
    """Scenario: *A reference names another repository's packet*.

    § 5.2: the cross-repository case is OUT OF SCOPE ON THE TREE BEING READ, and
    THIS MODULE IS STRUCTURALLY INCAPABLE OF DECIDING IT — which is the property
    asserted here rather than a behaviour asserted about a foreign path. The
    same reference answers RESOLVED against one root and DANGLING against
    another, so nothing about a tree that does not carry a packet is evidence
    about the reference; and the module holds no repository vocabulary and no
    module-level root with which it could think otherwise. The classification
    that keeps a foreign packet out is `read_citation`'s `qualified` kind, in
    the caller, and § 5.2 leaves it there.
    """
    ours = _tree(tmp_path / "ours")
    theirs = _tree(tmp_path / "theirs")
    _packet(ours, "openspec/changes/add-a-shared-name", files=("proposal.md",))
    _packet(theirs, "openspec/changes/add-a-different-one")

    cited = "openspec/changes/add-a-shared-name/proposal.md"
    assert pr.resolve(ours, cited).status == pr.RESOLVED
    assert pr.resolve(theirs, cited).status == pr.DANGLING

    assert not hasattr(pr, "ROOT"), (
        "a module-level root would make the answer depend on which checkout "
        "happens to be installed rather than on the tree the caller is reading")
    vocabulary = [name for name in dir(pr)
                  if "REPOSITOR" in name.upper() or "QUALIFI" in name.upper()]
    assert vocabulary == [], vocabulary


def test_an_id_resolving_twice_is_ambiguous_and_never_preferred(
        tmp_path) -> None:
    """Scenario: *An id resolves to more than one packet*.

    TWO DATED ARCHIVE DIRECTORIES FOR ONE ID — the case this estate already
    draws the line on, in `identity_paths_at`'s own words: two locations for one
    id is "an AMBIGUITY the resolver must be able to REPORT, not a collision to
    settle by taking the first sorted one".

    NEVER PREFERRED, PROVED BY SYMMETRY. The answer must not move when the
    candidates' sort order moves, so the same pair is asked with the FILE
    present in the first-sorted candidate and then with it present only in the
    last — a resolver that silently picked one would answer RESOLVED for one of
    the two and its verdict would be a fact about `sorted()`.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/archive/2026-09-01-add-a-twin",
            files=("proposal.md", "tasks.md"))
    _packet(root, "openspec/changes/archive/2026-09-08-add-a-twin",
            files=("proposal.md",))

    first = pr.resolve(root, "openspec/changes/add-a-twin/tasks.md")
    assert first.status == pr.AMBIGUOUS, first.report
    assert first.location is None
    assert first.half is None
    assert len(first.candidates) == 2
    assert {claim.rel for claim in first.candidates} == {
        "openspec/changes/archive/2026-09-01-add-a-twin",
        "openspec/changes/archive/2026-09-08-add-a-twin"}

    _packet(root, "openspec/changes/archive/2026-09-08-add-a-twin",
            files=("proposal.md", "design.md"))
    last = pr.resolve(root, "openspec/changes/add-a-twin/design.md")
    assert last.status == pr.AMBIGUOUS, last.report
    assert last.location is None


def test_the_ambiguity_belongs_to_the_declaration_and_not_to_the_citing_record(
        tmp_path) -> None:
    """Scenario: *An id resolves to more than one packet*, second THEN.

    A LIVE DIRECTORY AND SOMEBODY'S DECLARED FORMER ID — the collision a
    declaration creates rather than one the archive created. The citing record
    is sound: the path it names exists, exactly as written. The requirement
    still refuses to resolve it, and names the DECLARING packet as the owner of
    the repair — "CORRECTING A RECORD IS NOT THE REMEDY THIS REQUIREMENT
    IMPOSES".
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/add-a-contested-id",
            files=("proposal.md", "tasks.md"))
    _packet(root, "openspec/changes/add-the-claimant",
            former_ids=["add-a-contested-id"])

    cited = "openspec/changes/add-a-contested-id/tasks.md"
    assert (root / cited).exists(), "the citing record's own path is sound"

    resolution = pr.resolve(root, cited)

    assert resolution.status == pr.AMBIGUOUS, resolution.report
    assert {claim.rel for claim in resolution.candidates} == {
        "openspec/changes/add-a-contested-id",
        "openspec/changes/add-the-claimant"}
    declaring = [c for c in resolution.candidates if c.kind == pr.DECLARED]
    assert [c.rel for c in declaring] == ["openspec/changes/add-the-claimant"]
    assert "add-the-claimant" in resolution.report
    assert "declaration" in resolution.report
    assert "no edit" in resolution.report


def test_a_reference_that_resolves_owes_the_citing_record_no_edit(
        tmp_path) -> None:
    """The requirement's own remedy sentence, asserted as behaviour.

    "Where a reference resolves by identity, it is not a defect and nothing is
    owed; the reader resolves it." So a resolution is not a finding, carries no
    instruction to rewrite the path, and SAYS SO — and the resolver offers no
    corrected spelling for a caller to write back, because offering one is how a
    reader becomes an editor.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/archive/2026-09-03-add-a-landed-one",
            files=("proposal.md", "tasks.md"))

    resolution = pr.resolve(root, "openspec/changes/add-a-landed-one/tasks.md")

    assert resolution.status == pr.RESOLVED
    assert resolution.ok is True
    assert resolution.half is None
    assert "no edit" in resolution.report
    for word in ("rewrite", "update the citation", "correct the citation"):
        assert word not in resolution.report.lower(), resolution.report


# --------------------------------------------------------------------------
# BOTH HALVES, AND WHICH ONE FAILED — the requirement's own sentence
# --------------------------------------------------------------------------

def test_the_report_names_which_half_failed(tmp_path) -> None:
    """"BOTH HALVES SHALL RESOLVE, AND A FAILURE SHALL SAY WHICH HALF FAILED."

    Asserted as a DISCRIMINATION and not as two substrings: the identity-half
    report must not read like the file-half report and vice versa, because a
    reader repairing a citation does something different in each case — one is
    a wrong id, the other a wrong file inside the right packet.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/add-a-standing-one", files=("proposal.md",))

    identity = pr.resolve(root, "openspec/changes/add-a-vanished-one/x.md")
    afile = pr.resolve(root, "openspec/changes/add-a-standing-one/x.md")

    assert identity.half == pr.IDENTITY_HALF
    assert afile.half == pr.FILE_HALF
    assert identity.report != afile.report
    assert pr.IDENTITY_HALF in identity.report.lower()
    assert pr.FILE_HALF in afile.report.lower()
    # The file half names the packet the identity DID resolve to; the identity
    # half has no packet to name and says the id resolves to nothing.
    assert "openspec/changes/add-a-standing-one" in afile.report
    assert "nothing" in identity.report.lower()


# --------------------------------------------------------------------------
# The boundary: what is NOT a packet reference is left to the path
# --------------------------------------------------------------------------

def test_a_path_under_openspec_changes_that_addresses_no_packet_is_left_to_the_path(
        tmp_path) -> None:
    """`openspec/changes/README.md` is a real file in this repository whose
    second segment is not a packet id, and a resolver that read it as one would
    report this corpus's own README dangling. So a path whose identity is
    claimed by NOTHING, where the path itself is present, is handed back to the
    caller's own path resolution rather than judged here.
    """
    root = _tree(tmp_path)
    (root / "openspec" / "changes" / "README.md").write_text(
        "# changes\n", encoding="utf-8")

    present = pr.resolve(root, "openspec/changes/README.md")
    assert present.status == pr.NOT_A_PACKET_REFERENCE, present.report
    assert present.ok is True

    absent = pr.resolve(root, "openspec/changes/NOTES.md")
    assert absent.status == pr.DANGLING, absent.report
    assert absent.half == pr.IDENTITY_HALF


def test_a_path_that_is_not_under_openspec_changes_is_not_a_packet_reference(
        tmp_path) -> None:
    """The resolver answers about PACKETS and about nothing else. A citation
    naming a script, a contract or a doc is the caller's path question, and the
    caller's existing resolution is left exactly where it is."""
    root = _tree(tmp_path)
    for claimed in ("scripts/tool.py", "contracts/manifest.yaml",
                    "openspec/specs/release-realization/spec.md",
                    "openspec/changes", "openspec/changes/archive",
                    "openspec/changes/archive/not-dated/proposal.md"):
        assert pr.packet_reference(claimed) is None, claimed
        assert pr.resolve(root, claimed).status == pr.NOT_A_PACKET_REFERENCE


def test_the_resolver_never_walks_out_of_the_tree(tmp_path) -> None:
    """Containment, restated at this reader's own door.

    `scripts/validate-pin-registrations.py`'s `resolve_in_tree` refuses an
    absolute or `..`-escaping path and this resolver is reached THROUGH it
    today — but a library that trusted its caller's containment would hand the
    next caller a file read outside the repository. A path that escapes is not
    a packet reference here either, so it falls to whatever containment the
    caller has.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/add-a-real-one")
    for claimed in ("/openspec/changes/add-a-real-one/proposal.md",
                    "../openspec/changes/add-a-real-one/proposal.md",
                    "openspec/changes/../changes/add-a-real-one/proposal.md",
                    "openspec/changes/add-a-real-one/../../../etc/passwd"):
        assert pr.packet_reference(claimed) is None, claimed


def test_an_archived_spelling_resolves_by_id_when_the_archive_date_moves(
        tmp_path) -> None:
    """A citation may name the ARCHIVED spelling, and the date in it is part of
    the spelling rather than part of the identity.

    This estate corrects an archive directory's date — `proposal-support.py`
    carries `assert_archived_directory_date` for exactly that — and a citation
    written against the old date names the same packet afterwards. The id is
    read out of the dated directory name by `change_id_of`, the estate's own
    rule, and never by a second regex written here.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/archive/2026-09-09-add-a-redated-one",
            files=("proposal.md", "tasks.md"))

    resolution = pr.resolve(
        root, "openspec/changes/archive/2026-09-04-add-a-redated-one/tasks.md")

    assert resolution.status == pr.RESOLVED, resolution.report
    assert resolution.location.rel == (
        "openspec/changes/archive/2026-09-09-add-a-redated-one")
    assert resolution.relocated is True
    assert pr.packet_reference(
        "openspec/changes/archive/2026-09-04-add-a-redated-one/tasks.md"
    ) == ("add-a-redated-one", "tasks.md")


def test_a_citation_naming_the_packet_directory_itself_resolves(
        tmp_path) -> None:
    """A citation legitimately names a change packet's DIRECTORY — the reason
    `check_citations` opens its referents with `.exists()` and not `.is_file()`
    — so an empty remainder is a reference with one half to resolve and not a
    malformed one."""
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/archive/2026-09-05-add-a-whole-packet")

    for claimed in ("openspec/changes/add-a-whole-packet",
                    "openspec/changes/add-a-whole-packet/"):
        resolution = pr.resolve(root, claimed)
        assert resolution.status == pr.RESOLVED, resolution.report
        assert resolution.remainder == ""
        assert resolution.resolved_rel == (
            "openspec/changes/archive/2026-09-05-add-a-whole-packet")


# --------------------------------------------------------------------------
# The index, and the reader it is kept in step with
# --------------------------------------------------------------------------

def test_a_malformed_former_ids_declaration_is_left_to_its_own_reader(
        tmp_path) -> None:
    """A packet whose `former_ids:` cannot be read as one contributes NO claim,
    and the resolver does not restate the refusal.

    `former_identity_claimants` takes the same route and states the reason —
    "a malformed declaration is skipped rather than raised over: this is the
    corpus sweep, and `former_id_problems` is the reader that reports shape".
    A resolver that raised here would turn one packet's malformed declaration
    into a refusal of every citation in the corpus, which is a blast radius no
    requirement asks for.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/add-a-broken-declarer",
            former_ids="add-an-old-id")           # a scalar, not a sequence
    _packet(root, "openspec/changes/add-a-sound-declarer",
            files=("proposal.md", "tasks.md"),
            former_ids=["add-another-old-id"])

    assert pr.resolve(
        root, "openspec/changes/add-an-old-id/proposal.md"
    ).status == pr.DANGLING
    sound = pr.resolve(root, "openspec/changes/add-another-old-id/tasks.md")
    assert sound.status == pr.RESOLVED, sound.report
    problems = support.former_id_problems(
        "add-a-broken-declarer",
        yaml.safe_load((root / "openspec/changes/add-a-broken-declarer"
                        / ".openspec.yaml").read_text(encoding="utf-8")))
    assert problems, "the fixture must really be malformed to the estate reader"


def test_the_index_claims_at_least_what_the_corpus_ownership_sweep_claims(
        tmp_path) -> None:
    """THE TWO READERS ARE PINNED IN STEP, not left to drift.

    `former_identity_claimants` is the corpus sweep for OWNERSHIP of an
    identity; `PacketIndex` is the map for LOCATION of one. They read the same
    two claims — a live directory claims its own id, and any packet claims every
    id it declares — so the sweep's identities must all be claimed here, and a
    declaration either reader stopped seeing reds.

    THEY ARE NOT EQUAL, AND THE DIFFERENCE IS STATED RATHER THAN PAPERED OVER:
    the index ALSO claims an archived directory's own id, which the sweep
    deliberately does not read ("The ARCHIVED directories are read for their
    DECLARATIONS and not for their own ids"). Ownership of a former identity and
    the location a packet now occupies are different questions; resolution needs
    the second.
    """
    root = _tree(tmp_path)
    _packet(root, "openspec/changes/add-a-live-packet")
    _packet(root, "openspec/changes/add-a-declaring-packet",
            former_ids=["add-a-former-identity"])
    _packet(root, "openspec/changes/archive/2026-09-06-add-an-archived-packet",
            former_ids=["add-an-older-identity"])

    index = pr.PacketIndex(root)
    swept = set(support.former_identity_claimants(root))
    assert swept <= set(index.identities()), sorted(swept - set(index.identities()))
    assert "add-an-archived-packet" in index.identities()
    assert "add-an-archived-packet" not in swept
    for identity in ("add-a-former-identity", "add-an-older-identity"):
        assert identity in swept and identity in index.identities()

    live_swept = set(support.former_identity_claimants(REPO_ROOT))
    live_index = set(pr.PacketIndex(REPO_ROOT).identities())
    assert live_swept <= live_index, sorted(live_swept - live_index)
    assert len(live_index) > len(live_swept)


# --------------------------------------------------------------------------
# Symlink escape: the index must not follow a link out of `root` (Copilot
# review, PR #1037, `scripts/packet_reference.py:336`)
# --------------------------------------------------------------------------

def test_a_symlinked_archive_packet_pointing_outside_root_is_not_indexed(
        tmp_path) -> None:
    """A symlinked ARCHIVE packet directory pointing outside `root` must not
    be indexed, and a citation into it must resolve DANGLING rather than read
    the outside content.

    MEASURED AGAINST THE UNGUARDED READER (Copilot's finding). Before this
    guard: `PacketIndex` indexed the link (`Path.is_dir()` follows it to the
    outside target's own type), `Claim.carries` answered True for a file that
    exists only through it, and `resolve` reported RESOLVED while the bytes a
    caller would actually open came from outside the checkout — proved by
    reading them (`"outside content, not part of the checkout"`) before this
    commit. `check_citations` only containment-checks the CITED SPELLING
    (`openspec/changes/<id>/...`), and that spelling never itself crosses the
    link: the link sits at the ARCHIVE location the identity resolves TO, a
    path this module's own directory scan builds and the citing record never
    typed.
    """
    root = _tree(tmp_path)
    outside = _outside_packet(tmp_path, "add-a-linked-one",
                              files=("proposal.md", "evidence/run.md"))
    linked = root / "openspec/changes/archive/2026-09-10-add-a-linked-one"
    linked.symlink_to(outside, target_is_directory=True)

    index = pr.PacketIndex(root)
    assert "add-a-linked-one" not in index.identities()
    assert index.claims("add-a-linked-one") == ()

    resolution = pr.resolve(
        root, "openspec/changes/add-a-linked-one/proposal.md")
    assert resolution.status == pr.DANGLING, resolution.report
    assert resolution.half == pr.IDENTITY_HALF
    assert resolution.location is None


def test_a_symlinked_live_packet_pointing_outside_root_is_not_indexed(
        tmp_path) -> None:
    """The LIVE half of the same scan (`changes.iterdir()`, the sibling of the
    `archive.iterdir()` Copilot named at line 336) must refuse the identical
    link — the defect is in the SHAPE of the scan and not specific to the
    archive branch of it.
    """
    root = _tree(tmp_path)
    outside = _outside_packet(tmp_path, "add-a-linked-live-one")
    linked = root / "openspec/changes/add-a-linked-live-one"
    linked.symlink_to(outside, target_is_directory=True)

    index = pr.PacketIndex(root)
    assert "add-a-linked-live-one" not in index.identities()

    resolution = pr.resolve(
        root, "openspec/changes/add-a-linked-live-one/proposal.md")
    assert resolution.status == pr.DANGLING, resolution.report
    assert resolution.half == pr.IDENTITY_HALF


def test_a_symlinked_openspec_yaml_marker_is_not_read_through(
        tmp_path) -> None:
    """A REAL packet directory, standing legitimately inside `root`, whose own
    `.openspec.yaml` is a symlink to a file outside `root` must not have its
    `former_ids:` read through the link — `.is_file()` follows it exactly as
    `.is_dir()` follows one on a whole directory, and `declared_former_ids_of`
    would otherwise mint a claim from bytes this checkout never carried.
    """
    root = _tree(tmp_path)
    outside = _outside_packet(tmp_path, "outside-declarer",
                              former_ids=["add-an-outside-claimed-id"])

    directory = root / "openspec/changes/add-a-legit-directory"
    directory.mkdir(parents=True)
    (directory / "proposal.md").write_text("# proposal.md\n", encoding="utf-8")
    (directory / ".openspec.yaml").symlink_to(outside / ".openspec.yaml")

    index = pr.PacketIndex(root)
    assert "add-an-outside-claimed-id" not in index.identities()
    assert pr.resolve(
        root, "openspec/changes/add-an-outside-claimed-id/proposal.md"
    ).status == pr.DANGLING


def test_a_symlinked_file_inside_a_legitimate_packet_is_not_read_as_carried(
        tmp_path) -> None:
    """`Claim.carries` must not answer True for a remainder that only exists
    by following a symlink out of `root`, even where the PACKET DIRECTORY
    itself is real and stands legitimately inside it — the citation names a
    file inside a sound packet, and the file is the half that fails.
    """
    root = _tree(tmp_path)
    outside_dir = tmp_path.parent / f"{tmp_path.name}-outside-file"
    outside_dir.mkdir(parents=True)
    outside_file = outside_dir / "secret.md"
    outside_file.write_text("outside content, not part of the checkout\n",
                            encoding="utf-8")

    _packet(root, "openspec/changes/add-a-legit-packet", files=("proposal.md",))
    (root / "openspec/changes/add-a-legit-packet/linked.md").symlink_to(
        outside_file)

    resolution = pr.resolve(
        root, "openspec/changes/add-a-legit-packet/linked.md")
    assert resolution.status == pr.DANGLING, resolution.report
    assert resolution.half == pr.FILE_HALF


# --------------------------------------------------------------------------
# The live corpus — a resolver proved only against invented trees is proved
# against the author's imagination
# --------------------------------------------------------------------------

def test_every_packet_in_this_corpus_resolves_to_exactly_itself() -> None:
    """Every active and archived packet this repository carries resolves — by
    its own id, to its own directory, with its own `proposal.md` — and not one
    of them is AMBIGUOUS.

    The anti-vacuity pin for the whole module: a resolver that claimed nothing
    would pass every fixture above that asserts DANGLING and would fail here on
    the first packet. It is also the assertion that reds the day two archive
    directories carry one id, which is the corpus defect the AMBIGUOUS outcome
    exists to report.
    """
    changes = REPO_ROOT / "openspec" / "changes"
    index = pr.PacketIndex(REPO_ROOT)
    live = sorted(d.name for d in changes.iterdir()
                  if d.is_dir() and d.name != "archive")
    archived = sorted(d.name for d in (changes / "archive").iterdir()
                      if d.is_dir())
    assert len(live) >= 40 and len(archived) >= 150, (len(live), len(archived))

    ambiguous = []
    # `change_id_of` strips a date prefix only where the Path it is handed has
    # `archive` for a parent (main 701c8fde, so an ACTIVE id that merely looks
    # dated is read verbatim) — `n` alone is a bare leaf with no such parent,
    # so it is prefixed with the segment it was actually read from, exactly as
    # `packet_reference.py`'s own archive-spelling branch now must.
    for name in live + [support.change_id_of(Path("archive") / n)
                        for n in archived]:
        resolution = pr.resolve(REPO_ROOT,
                                f"openspec/changes/{name}/proposal.md",
                                index=index)
        if resolution.status == pr.AMBIGUOUS:
            ambiguous.append(resolution.report)
            continue
        assert resolution.status == pr.RESOLVED, resolution.report
        assert (REPO_ROOT / resolution.resolved_rel).is_file()
    assert ambiguous == [], ambiguous


def test_the_active_packets_the_live_pin_cites_are_still_active() -> None:
    """The corpus fact this module's reason-for-existing rests on, named rather
    than counted: the four packets the live pin's citations point INTO are
    active today, so each still has its archive relocation ahead of it.

    When one of them archives this test does NOT red — `_still_active` would be
    the wrong claim to pin — it is the resolution that must hold, and
    `tests/pin_registrations/test_the_live_pin_registration_citations_still_
    resolve` is where that is asserted. What reds here is the packet
    DISAPPEARING from the corpus altogether, which would mean the citation is
    dangling for a reason no resolver can repair.
    """
    changes = REPO_ROOT / "openspec" / "changes"
    index = pr.PacketIndex(REPO_ROOT)
    for name in CITED_ACTIVE_PACKETS:
        claims = index.claims(name)
        assert len(claims) == 1, [c.rel for c in claims]
        assert claims[0].path.is_dir()
        assert claims[0].rel.startswith("openspec/changes/")
        if claims[0].kind == pr.ACTIVE:
            assert (changes / name).is_dir()


if __name__ == "__main__":  # pragma: no cover - parity with the sibling suites
    raise SystemExit(pytest.main([__file__, "-q"]))
