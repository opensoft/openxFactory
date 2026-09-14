"""`release-realization` § *An undeclared rename arrival is refused at its
landing* — the landing validator, over real git history.

`add-declared-former-id` `tasks.md` § 2.4 and § 4. Every scenario the
requirement states is realized by a test below whose docstring NAMES it, and
every tree is built in a `TemporaryDirectory` — the rule
`tests/target_release/test_target_release_gate.py` states for its own gate —
so no test here can be made green by editing this repository. The two corpus
tests at the end are the only ones that read the real one, and they read it
without writing to it.

WHY THESE FIXTURES ARE REPOSITORIES AND NOT DIRECTORIES OF FILES. The question
this gate answers is *did a change packet directory arrive HERE by a move from
another change packet directory* — a fact about a commit and its parent, which
only git holds. A fixture that stubbed the pairing would test the gate's
arithmetic and not its reads, and the reads are where the two fail-closed arms
live.

THE TWO FAIL-CLOSED FIXTURES ARE REAL PARTIAL CLONES, and the asymmetry they
rest on is measured rather than assumed (`design.md` M1, re-measured here on
git 2.43.0). In a `--filter=blob:none --no-checkout` clone whose promisor
remote is unreachable:

* `git ls-tree` prints the row and exits 0 for a path whose blob is
  unavailable — so PRESENCE is still answerable;
* `git show <rev>:<path>` exits 128 — so CONTENT is not;
* `git diff-tree -M` exits 128 the moment INEXACT rename detection needs a
  blob, and exits 0 pairing an EXACT rename it can settle from tree OIDs
  alone.

That last line is what lets ONE recipe drive BOTH refusals: an inexact packet
move makes the PAIRING the unreadable read, and an exact one lets the pairing
succeed so the RATIFICATION LOOKUP is the read that fails. Each test asserts
its own precondition before asserting the refusal, so a git whose behaviour
differs FAILS the test rather than passing it vacuously.
"""
from __future__ import annotations

import contextlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE = REPO_ROOT / "scripts" / "former_id_arrival.py"
VALIDATOR = REPO_ROOT / "scripts" / "validate-former-id-arrival.py"


def _load(name: str, path: Path):
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


fia = _load("former_id_arrival", MODULE)
cli = _load("validate_former_id_arrival", VALIDATOR)

#: The exceptions are reached THROUGH the module under test, never through a
#: second load of `proposal-support.py`: two live copies of that module would
#: give two distinct `FormerIdError` classes and an `assertRaises` here would
#: be asserting about the wrong one.
support = fia.support


# --------------------------------------------------------------------------
# FIXTURE HELPERS
# --------------------------------------------------------------------------

PROPOSAL = "---\nStatus: {status}\n---\n\n## Why\n\n{body}\n"
MANIFEST = "schema: spec-driven\ncreated: 2026-09-14\n"


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], check=True,
                          capture_output=True, text=True)


def commit_all(root: Path, message: str) -> str:
    git(root, "add", "-A")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.com",
        "commit", "-q", "-m", message)
    return head_of(root)


def head_of(root: Path) -> str:
    return git(root, "rev-parse", "HEAD").stdout.strip()


def new_repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q", ".")
    git(root, "config", "user.name", "Test")
    git(root, "config", "user.email", "test@example.com")
    # The blobless clone the fail-closed fixtures take needs the server side
    # to allow a filtered fetch; harmless everywhere else.
    git(root, "config", "uploadpack.allowFilter", "true")
    return root


def packet(root: Path, change: str, *, ratified: bool = False,
           manifest: bool = True, archived: str | None = None,
           body: str = "A fixture packet.") -> Path:
    """A change packet directory, active or under a dated archive folder."""
    where = root / "openspec" / "changes"
    if archived:
        where = where / "archive" / f"{archived}-{change}"
    else:
        where = where / change
    where.mkdir(parents=True, exist_ok=True)
    (where / "proposal.md").write_text(
        PROPOSAL.format(status="ratified" if ratified else "draft", body=body),
        encoding="utf-8")
    if manifest:
        (where / ".openspec.yaml").write_text(MANIFEST, encoding="utf-8")
    return where


def set_status(directory: Path, status: str) -> None:
    path = directory / "proposal.md"
    text = path.read_text(encoding="utf-8")
    for known in ("draft", "ratified"):
        text = text.replace(f"Status: {known}", f"Status: {status}", 1)
    path.write_text(text, encoding="utf-8")


def declare(directory: Path, *ids: str) -> None:
    """Rewrite the packet manifest with `former_ids:` as a TOP-LEVEL SIBLING.

    Written whole rather than appended so a test can also take an entry AWAY,
    which is what the append-only rule exists to refuse.
    """
    body = MANIFEST
    if ids:
        body += "former_ids:\n" + "".join(f"  - {i}\n" for i in ids)
    (directory / ".openspec.yaml").write_text(body, encoding="utf-8")


def blobless_clone(source: Path, destination: Path) -> Path:
    """A partial clone that can read TREES and not BLOBS — `design.md` M1."""
    subprocess.run(
        ["git", "-c", "protocol.file.allow=always", "clone", "-q",
         "--filter=blob:none", "--no-checkout", "--no-local",
         f"file://{source}", str(destination)],
        check=True, capture_output=True, text=True)
    git(destination, "remote", "set-url", "origin", "/nonexistent-promisor")
    return destination


def _exit(root: Path, revision: str, *args: str) -> int:
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True).returncode


@contextlib.contextmanager
def no_event():
    """THE AMBIENT `GITHUB_EVENT_NAME`, REMOVED FOR THE CORPUS-ARM TESTS.

    Given no `--base`/`--head`, the CLI derives its range from the event it is
    running under — and the runner that runs this suite IS a `pull_request`
    event, which sets `GITHUB_EVENT_NAME` for every step of it. Without this
    the tests below would ask the CLI to resolve `HEAD^1..HEAD^2` inside a
    two-commit fixture repository, it would refuse CANNOT RUN, and assertions
    that mean "exit 1, a refusal" would read exit 2.

    MEASURED, and the reason this helper exists rather than a comment:
    `python3 -m pytest tests/former_id_arrival` passed on a developer machine
    while pytest-suite run 34846423535 failed four of these same tests with
    `AssertionError: 2 != 1`. Reproduced locally with
    `GITHUB_EVENT_NAME=pull_request python3 -m pytest tests/former_id_arrival`,
    which also failed `test_the_live_corpus_passes_this_gate` — a test that
    PASSED on the runner, because there `HEAD^1..HEAD^2` does resolve. A test
    whose answer depends on where it runs is a test that can pass for the wrong
    reason, and one of these did.
    """
    saved = os.environ.pop("GITHUB_EVENT_NAME", None)
    try:
        yield
    finally:
        if saved is not None:
            os.environ["GITHUB_EVENT_NAME"] = saved


class ArrivalRefusalTests(unittest.TestCase):
    """The arrival question itself — one commit read, never a chain."""

    def judge(self, root: Path, commit: str | None = None) -> list:
        return fia.judge_commit(root, commit or head_of(root))

    def statuses(self, findings: list) -> list:
        return [f.status for f in findings]

    # ---- the refusal ----------------------------------------------------

    def test_a_ratified_packet_renamed_with_no_declaration_is_refused(self):
        """Scenario: *A ratified packet is renamed with no declaration*.

        The commit moves a change packet directory to a new id and the
        arriving packet declares no former id, so the landing is refused.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r")
            commit_all(root, "create the packet")
            set_status(directory, "ratified")
            commit_all(root, "record the ratification")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(changes / "change-r"),
                str(changes / "change-s"))
            moved = commit_all(root, "rename the ratified packet")

            findings = self.judge(root, moved)
            self.assertEqual(self.statuses(findings), [fia.UNDECLARED],
                             [f.message for f in findings])
            self.assertIn("openspec/changes/change-r/", findings[0].message)
            self.assertIn("openspec/changes/change-s/", findings[0].message)

    def test_the_refusal_names_the_commit_both_paths_and_the_one_repair(self):
        """*THE REFUSAL SHALL NAME THE REMEDY* — the commit, the source path,
        the destination path, and the one repair, which is the whole of what
        an author needs to fix it in the commit they are still standing in."""
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename it")

            message = self.judge(root, moved)[0].message
            self.assertIn(moved[:12], message)
            self.assertIn("`openspec/changes/change-r/`", message)
            self.assertIn("`openspec/changes/change-s/`", message)
            self.assertIn("THE ONE REPAIR", message)
            self.assertIn("former_ids:", message)
            self.assertIn("IN THE SAME COMMIT", message)
            self.assertIn("['change-r']", message)
            # …and it names the identity that QUALIFIED the move, so the
            # author can see WHY the refusal reached this rename.
            self.assertIn("`change-r` HAS declared `Status: ratified`",
                          message)

    def test_the_declared_move_lands(self):
        """Scenario: *The declared move lands*.

        The moving commit carries the source id in the destination packet's
        `former_ids:`, so the landing passes and the identity continuity is on
        the record where the archive gate will read it.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            declare(changes / "change-s", "change-r")
            moved = commit_all(root, "rename and declare the move")

            self.assertEqual(self.judge(root, moved), [])
            self.assertEqual(
                support.declared_former_ids_in_tree(root, "change-s"),
                ["change-r"])

    # ---- the qualification ----------------------------------------------

    def test_a_never_ratified_draft_rename_passes_with_no_declaration(self):
        """Scenario: *A never-ratified draft is renamed*.

        The move is an ordinary authoring act and a refusal reaching it would
        make the mechanism cost more than the defect —
        `docs/document-lifecycle.md` promises as much in as many words.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r")
            commit_all(root, "create the draft")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename the draft")

            self.assertEqual(self.judge(root, moved), [])

    def test_a_once_ratified_packet_moved_while_back_in_draft_is_refused(
            self):
        """Scenario: *A once-ratified packet is moved while back in draft*.

        The identity declared `Status: ratified` earlier in its history and
        does not at this commit. The landing is refused unless the arriving
        packet declares the source id — and the declared variant of the same
        tree passes, so the refusal has not simply replaced one wall with
        another.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            set_status(directory, "draft")
            commit_all(root, "return the packet to draft")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename it while back in draft")

            findings = self.judge(root, moved)
            self.assertEqual(self.statuses(findings), [fia.UNDECLARED],
                             [f.message for f in findings])

            declare(changes / "change-s", "change-r")
            declared = commit_all(root, "declare the move after the fact")
            # The DECLARATION is owed in the moving commit; a later one does
            # not repair the landing that already happened, and § 2.4 refuses
            # the entry the later commit adds.
            self.assertEqual(self.judge(root, moved)[0].status,
                             fia.UNDECLARED)
            self.assertTrue(self.judge(root, declared))

    def test_the_ever_test_is_the_whole_history_and_never_the_parent_blob(
            self):
        """*The qualification is EVER, read over the source identity's whole
        history up to that commit, and never its blob at the parent.*

        The crux, asserted directly rather than through the refusal: at the
        commit's PARENT the source's own `proposal.md` declares `draft`, and
        `ever_ratified` still answers True. A packet renamed and un-ratified
        in ONE commit is back in draft for every later hop, so a test taken at
        the parent would exempt exactly the shape this refusal exists to
        catch.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            set_status(directory, "draft")
            parent = commit_all(root, "return the packet to draft")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename it while back in draft")

            at_parent = support.git_show_text(
                root, parent, "openspec/changes/change-r/proposal.md")
            self.assertFalse(support.declares_ratified(at_parent))
            self.assertTrue(fia.ever_ratified(root, moved, "change-r"))
            self.assertTrue(self.judge(root, moved))

    def test_a_live_packet_id_that_begins_with_a_date_keeps_its_whole_id(self):
        """THE ARCHIVE DATE MEANS THE ARCHIVE AND NOTHING ELSE.

        `CHANGE_ID_RE` admits `2026-09-14-example` as an ACTIVE change id, and
        a reader that strips a date prefix wherever it sees one hands this gate
        a source identity no packet ever carried: `ever_ratified` walks the
        wrong pathspecs, answers "never ratified", and the undeclared rename
        passes. So the strip happens only under the archive root, and this test
        asserts the identity BOTH directly and through the refusal.
        (Copilot, PR #1039.)
        """
        self.assertEqual(
            fia.change_id_of_dir("openspec/changes/2026-09-14-example"),
            "2026-09-14-example")
        self.assertEqual(
            fia.change_id_of_dir(
                "openspec/changes/archive/2026-09-14-example"),
            "example")

        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "2026-09-14-example", ratified=True)
            commit_all(root, "create a ratified packet whose id reads as a date")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename it with no declaration")

            self.assertTrue(fia.ever_ratified(root, moved, "2026-09-14-example"))
            findings = self.judge(root, moved)
            self.assertEqual(self.statuses(findings), [fia.UNDECLARED],
                             [f.message for f in findings])
            self.assertIn("`2026-09-14-example` HAS declared", findings[0].message)
            self.assertIn("['2026-09-14-example']", findings[0].message)

    def test_a_rename_chain_is_refused_at_its_first_hop_and_no_chain_is_walked(
            self):
        """Scenario: *A rename chain is attempted one hop at a time*.

        `r` ratified, renamed to `s` and un-ratified in one commit, renamed to
        `t` while draft, ratified under its third id — each hop its own
        commit. THE FIRST UNDECLARED HOP IS REFUSED AT ITS OWN LANDING, so no
        later hop is ever reached; the first hop qualifies because its SOURCE
        had declared `Status: ratified`, whatever the destination declares at
        that commit (here it declares `draft`, in that same commit).

        AND NO CHAIN IS WALKED TO REACH THAT ANSWER: the refusal is asserted
        against a repository whose HEAD **is** the first hop, so the later
        hops do not exist when the question is asked.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            set_status(changes / "change-s", "draft")
            first = commit_all(root, "rename r to s and un-ratify in one")

            # ASKED BEFORE THE CHAIN EXISTS: nothing after `first` is written.
            self.assertEqual(
                [f.status for f in self.judge(root, first)],
                [fia.UNDECLARED])
            self.assertIn("`change-r` HAS declared", self.judge(
                root, first)[0].message)

            git(root, "mv", str(changes / "change-s"),
                str(changes / "change-t"))
            second = commit_all(root, "rename s to t while draft")
            set_status(changes / "change-t", "ratified")
            commit_all(root, "ratify t under its third name")

            # The first hop still refuses with the whole chain in place…
            self.assertEqual(
                [f.status for f in self.judge(root, first)],
                [fia.UNDECLARED])
            # …and the SECOND hop does not, which is the point: `change-s`'s
            # own identity never declared `ratified` and it declares no
            # lineage, so the refusal must land on the hop that sheds the
            # ratification or it lands nowhere at all.
            self.assertEqual(self.judge(root, second), [])

    def test_an_undeclared_rename_chain_now_refuses_at_its_landing(self):
        """THE SECOND HALF OF THE #1027 FLIP, taken here rather than in the
        fixture it closes.

        `tests/proposal-support/test_proposal_support.py::
        test_an_undeclared_rename_chain_is_the_landing_validators_to_refuse`
        builds this exact history — ratify `r`, mutate the origin, rename
        `r`→`s` and un-ratify in one commit, rename `s`→`t` while draft,
        ratify `t` — and pins today's ACCEPTANCE at the archive gate, because
        nothing in history connects `change-t` to `change-r` and
        `ratifying_commit` cannot reach the `r`→`s` hop. Its own docstring
        names this validator as the closure and says the fixture gains its
        refusal when this lands.

        THE REFUSAL IS THE VALIDATOR'S AND NOT `ratifying_commit`'S, and this
        test asserts both halves over ONE tree so the division of labour is on
        the record: the archive gate still reads no refusal for `change-t`,
        and the landing gate refuses the `r`→`s` hop that would have created
        the history in the first place.

        THE RENAME OF THAT FIXTURE TO
        `test_an_undeclared_rename_chain_now_refuses_at_its_landing` — the
        house convention `2dd54b8e` set when #999 flipped
        `test_an_unratifying_rename_escapes_the_guard_a_stated_gap` — IS NOT
        TAKEN HERE. `tests/proposal-support/test_proposal_support.py` and
        `scripts/proposal-support.py` (whose `ratifying_commit` docstring
        names the old fixture) both belong to a sibling slice in flight, and
        editing a file two authors hold is the collision this estate's lane
        protocol exists to prevent. The rename is owed, and it is named as
        owed rather than performed.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            set_status(changes / "change-s", "draft")
            first = commit_all(root, "rename r to s and un-ratify in one")
            git(root, "mv", str(changes / "change-s"),
                str(changes / "change-t"))
            commit_all(root, "rename s to t while draft")
            set_status(changes / "change-t", "ratified")
            head = commit_all(root, "ratify t under its third name")

            # THE ARCHIVE GATE STILL READS NOTHING — unchanged, deliberately.
            self.assertEqual(
                support.declared_former_ids_in_tree(root, "change-t"), [])
            self.assertEqual(support.ratifying_commit(root, "change-t"), head)
            self.assertEqual(
                support.origin_retention_errors(
                    root, changes / "change-t", change="change-t"), [])

            # THE LANDING GATE REFUSES THE HOP THAT CREATED IT.
            findings = self.judge(root, first)
            self.assertEqual([f.status for f in findings], [fia.UNDECLARED])
            self.assertIn("openspec/changes/change-r/", findings[0].message)

    def test_a_packet_that_already_moved_lawfully_is_refused_on_its_second_move(
            self):
        """Scenario: *A packet that already moved lawfully moves again*.

        `X` ratified, moved to `Y` with the move DECLARED and the header
        returned to draft, then moved to `Z`. The "ever ratified" test must
        reach the id the packet declares as its former identity — `Y`'s own id
        never declared `Status: ratified`, so a test over `Y` alone would pass
        the second landing and `Z` would stand with no lineage at all.

        AND THE ARRIVING LIST MUST BE THE SOURCE'S LIST WITH THE SOURCE ID
        APPENDED, which the refusal states as the repair.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-x", ratified=True)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-y"))
            set_status(changes / "change-y", "draft")
            declare(changes / "change-y", "change-x")
            lawful = commit_all(root, "move x to y, declared, back to draft")
            self.assertEqual(self.judge(root, lawful), [])

            git(root, "mv", str(changes / "change-y"),
                str(changes / "change-z"))
            second = commit_all(root, "move y to z with no declaration")

            findings = self.judge(root, second)
            self.assertEqual([f.status for f in findings], [fia.UNDECLARED],
                             [f.message for f in findings])
            message = findings[0].message
            # The qualification came from the DECLARED former identity, not
            # from the source's own id.
            self.assertIn("`change-x` HAS declared `Status: ratified`",
                          message)
            self.assertIn("['change-x', 'change-y']", message)
            self.assertFalse(fia.ever_ratified(root, second, "change-y"))

    def test_a_move_that_drops_an_inherited_entry_is_refused(self):
        """Scenario: *A move drops an entry the source declared*.

        The destination omits an id the source packet carried in its own
        `former_ids:`. A move that sheds a lineage is the same defect as never
        declaring one, and the refusal says which entries were shed.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-x", ratified=True)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-y"))
            set_status(changes / "change-y", "draft")
            declare(changes / "change-y", "change-x")
            commit_all(root, "move x to y, declared")

            git(root, "mv", str(changes / "change-y"),
                str(changes / "change-z"))
            declare(changes / "change-z", "change-y")      # `change-x` shed
            second = commit_all(root, "move y to z, shedding the lineage")

            findings = self.judge(root, second)
            # TWO TRUE STATEMENTS ABOUT ONE COMMIT, and neither is the
            # other's corollary: the ARRIVAL is undeclared (the list is not
            # the source's plus the source id), and the LIST is rewritten
            # rather than appended to. A shed lineage is refused from both
            # sides, which is what the requirement says it is — "the same
            # defect as never declaring one".
            self.assertEqual([f.status for f in findings],
                             [fia.UNDECLARED, None],
                             [f.message for f in findings])
            self.assertIn("SHEDS the lineage ['change-x']",
                          findings[0].message)
            self.assertIn("APPEND-ONLY ACROSS COMMITS", findings[1].message)
            self.assertIn("REMOVED 'change-x'", findings[1].message)

            # …and the same move declaring the WHOLE list lands.
            git(root, "reset", "-q", "--hard", "HEAD~1")
            git(root, "mv", str(changes / "change-y"),
                str(changes / "change-z"))
            declare(changes / "change-z", "change-x", "change-y")
            whole = commit_all(root, "move y to z, declaring the whole list")
            self.assertEqual(self.judge(root, whole), [])

    # ---- the one exception ----------------------------------------------

    def test_the_archive_relocation_passes_with_no_declaration(self):
        """Scenario: *A packet archives*.

        `openspec/changes/<id>/` relocating to
        `openspec/changes/archive/<YYYY-MM-DD>-<id>/` with the id unchanged
        preserves the identity rather than changing it. THE EXCEPTION IS BY
        ID AND IS THE ONLY ONE: the same relocation under a DIFFERENT id is
        still a move and is still refused.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            archive = root / "openspec" / "changes" / "archive"
            archive.mkdir(parents=True)
            git(root, "mv", str(directory),
                str(archive / "2026-09-14-change-r"))
            archived = commit_all(root, "archive the packet")
            self.assertEqual(self.judge(root, archived), [])

            git(root, "reset", "-q", "--hard", "HEAD~1")
            archive.mkdir(parents=True, exist_ok=True)
            git(root, "mv", str(directory),
                str(archive / "2026-09-14-change-s"))
            renamed = commit_all(root, "archive it under a different id")
            findings = self.judge(root, renamed)
            self.assertEqual([f.status for f in findings], [fia.UNDECLARED],
                             [f.message for f in findings])

    def test_a_fork_by_copy_is_not_a_move_and_is_not_refused(self):
        """Scenario: *A fork by copy declares nothing*.

        A new packet authored as a COPY of a ratified one, the source still
        standing. It declares no former id, carries its own origin and is
        baselined at its own first ratification — and the gate MUST NOT refuse
        it, the source having not moved. Copy detection is deliberately not
        requested (`diff_at`'s docstring says why), so git reports the
        destination as an ADD and this gate sees no move at all.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            packet(root, "change-s", ratified=False)
            forked = commit_all(root, "fork the packet by copy")

            self.assertEqual(self.judge(root, forked), [])
            self.assertTrue(
                (root / "openspec/changes/change-r/proposal.md").is_file())

    def test_a_file_moved_between_two_standing_packets_is_not_an_arrival(self):
        """A FILE THAT CROSSES TWO STANDING PACKETS IS NOT A PACKET MOVING.

        One `design.md` relocated out of a ratified packet into another packet
        that also stands is a file-level rename git pairs across two packet
        directories — and it is not an arrival: the tree shows no directory
        leaving and no directory arriving, so there is nothing a declaration
        could record. A gate that refused it would red an ordinary edit nobody
        can repair by declaring anything. The pairing is asserted first, so
        this test cannot pass because git failed to report the rename.
        (Copilot, PR #1039.)
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            source = packet(root, "change-r", ratified=True)
            destination = packet(root, "change-s")
            (source / "design.md").write_text("d" * 900, encoding="utf-8")
            commit_all(root, "two standing packets, one carrying a design")
            git(root, "mv", str(source / "design.md"),
                str(destination / "design.md"))
            moved = commit_all(root, "move one file between two packets")

            parent = fia.commit_parents(root, moved)[0]
            diff = fia.diff_at(root, parent, moved)
            self.assertIn(
                ("openspec/changes/change-r/design.md",
                 "openspec/changes/change-s/design.md"), diff.renames)
            self.assertEqual(
                fia.moves_at(diff),
                [("openspec/changes/change-r", "openspec/changes/change-s")])
            # …and the tree says neither directory left and neither arrived.
            self.assertEqual(fia.relocations_at(
                diff, fia.packet_dirs_at(root, parent),
                fia.packet_dirs_at(root, moved)), [])
            self.assertEqual(self.judge(root, moved), [])

    # ---- the pairing itself ---------------------------------------------

    def test_the_pairing_is_read_from_every_file_and_not_from_the_proposal_alone(
            self):
        """A MOVE THAT REWRITES THE PROPOSAL AS IT TRAVELS IS STILL A MOVE.

        Measured on this fixture: git pairs `.openspec.yaml` at R100 and
        reports `proposal.md` as a plain D plus A, because the rewritten
        proposal falls below the similarity threshold. A gate keyed on the
        proposal alone would have seen no move, so the pairing is aggregated
        over every file of the packet. The precondition is asserted first, so
        a future git that pairs the proposal too does not make this test pass
        for the wrong reason — it makes it fail.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True,
                               body="x" * 40)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            proposal = changes / "change-s" / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8") + ("y" * 4000) + "\n",
                encoding="utf-8")
            moved = commit_all(root, "rename and rewrite the proposal")

            parent = fia.commit_parents(root, moved)[0]
            diff = fia.diff_at(root, parent, moved)
            paired = {destination for _source, destination in diff.renames}
            self.assertNotIn("openspec/changes/change-s/proposal.md", paired)
            self.assertIn("openspec/changes/change-s/.openspec.yaml", paired)

            self.assertEqual([f.status for f in self.judge(root, moved)],
                             [fia.UNDECLARED])

    def test_a_hostile_diff_config_cannot_switch_the_pairing_off(self):
        """A REPOSITORY CONFIGURATION MUST NOT BE ABLE TO DISARM THE GATE.

        `diff.renames=false` and `diff.renameLimit=1` are the two knobs that
        make git stop reporting a pairing. `-M` and `-l0` are passed on the
        command line, which overrides both — the same property
        `renamed_from`'s own fixture pins for the archive-gate guard, spelled
        here for this one.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            git(root, "config", "diff.renames", "false")
            git(root, "config", "diff.renameLimit", "1")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename under a hostile config")

            self.assertEqual([f.status for f in self.judge(root, moved)],
                             [fia.UNDECLARED])

    def test_a_merge_commit_performs_no_move_of_its_own(self):
        """A MERGE IS SKIPPED, and that is a correctness rule.

        A merge's diff against its first parent is every change the merged
        branch carried, so judging one would re-adjudicate commits that either
        sit in this same range under their own author or are already on the
        base branch. A required gate that reds a pull request for history it
        did not write is worse than no gate. The move commit ITSELF is still
        refused, which is what keeps the skip from being a hole.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            base = commit_all(root, "create the ratified packet")
            git(root, "checkout", "-q", "-b", "side")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename the ratified packet")
            git(root, "checkout", "-q", "-")
            (root / "unrelated.md").write_text("side by side\n",
                                               encoding="utf-8")
            commit_all(root, "an unrelated commit on the base branch")
            git(root, "-c", "user.name=Test", "-c",
                "user.email=test@example.com", "merge", "-q", "--no-ff",
                "-m", "merge the rename", "side")
            merge = head_of(root)

            self.assertEqual(len(fia.commit_parents(root, merge)), 2)
            report = fia.Report()
            self.assertEqual(
                fia.judge_commit(root, merge, report=report), [])
            self.assertEqual(report.commits_skipped_merges, 1)
            self.assertEqual([f.status for f in self.judge(root, moved)],
                             [fia.UNDECLARED])

            # AND THE SKIP IS ON THE RECORD, not silent. Over the whole range
            # the merge is dropped by `rev-list --no-merges`, the move commit
            # inside it is still read and still refused, and the run's own
            # report COUNTS what it did not read — a gate that quietly skips
            # commits and prints a clean range is a vacuous pass.
            whole = fia.scan(root, base=base, head=merge, env={})
            self.assertEqual(whole.commits_skipped_merges, 1)
            self.assertEqual(whole.commits_read, 2)
            self.assertEqual([f.status for f in whole.findings],
                             [fia.UNDECLARED])
            self.assertIn("1 merge commit(s) skipped", whole.range_note)


class FailClosedTests(unittest.TestCase):
    """*A silence that cannot be distinguished from an answer is not an
    answer.* Both reads, on real partial clones."""

    def test_an_unpairable_arrival_with_a_departure_refuses_cannot_run(self):
        """Scenario: *The pairing read cannot be performed*.

        The checkout cannot produce what the arrival pairing is computed from
        and the TREE at that commit shows a packet directory arriving and one
        leaving, so the gate refuses as CANNOT RUN naming the read — and it
        does NOT report that no arrival was found, and it does NOT pair them
        from the tree.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td) / "src")
            directory = packet(root, "change-r", ratified=True,
                               body="x" * 40)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            proposal = changes / "change-s" / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8") + ("y" * 4000) + "\n",
                encoding="utf-8")
            moved = commit_all(root, "rename, rewriting as it travels")
            partial = blobless_clone(root, Path(td) / "partial")

            # PRECONDITIONS, measured rather than assumed.
            self.assertEqual(
                0, _exit(partial, moved, "ls-tree", "--name-only", moved,
                         "--", "openspec/changes/"))
            self.assertNotEqual(
                0, _exit(partial, moved, "diff-tree", "-r", "-M", "-l0",
                         "--name-status", f"{moved}^", moved))

            with self.assertRaises(fia.ArrivalCannotRun) as caught:
                fia.judge_commit(partial, moved)
            message = str(caught.exception)
            self.assertIn(fia.UNREADABLE, message)
            self.assertIn("git diff-tree", message)
            self.assertIn("ARRIVING", message)
            self.assertIn("LEAVING", message)
            self.assertIn("openspec/changes/change-s", message)
            self.assertIn("openspec/changes/change-r", message)
            self.assertIn("does NOT pair them from the tree", message)

    def test_an_unpairable_arrival_with_no_departure_is_not_refused(self):
        """THE OTHER HALF OF THE SAME RULE, and the reason the tree is never
        used to PAIR.

        The same unreadable checkout, at a commit that CREATES a packet
        directory and removes none. The pairing is just as unavailable, and
        the gate does not refuse: an arrival with no departure cannot be a
        move of anything, and refusing it would turn every new packet authored
        on a partial checkout into a red gate.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td) / "src")
            packet(root, "change-r", ratified=True)
            (root / "docs").mkdir()
            (root / "docs" / "a.md").write_text("a" * 800, encoding="utf-8")
            commit_all(root, "create the ratified packet and a document")
            packet(root, "change-n")
            git(root, "mv", str(root / "docs" / "a.md"),
                str(root / "docs" / "b.md"))
            (root / "docs" / "b.md").write_text("b" * 4000, encoding="utf-8")
            created = commit_all(root, "create a packet; rewrite a document")
            partial = blobless_clone(root, Path(td) / "partial")

            self.assertNotEqual(
                0, _exit(partial, created, "diff-tree", "-r", "-M", "-l0",
                         "--name-status", f"{created}^", created))
            before = fia.packet_dirs_at(partial, f"{created}^")
            after = fia.packet_dirs_at(partial, created)
            self.assertEqual([d for d in before if d not in after], [])
            self.assertEqual([d for d in after if d not in before],
                             ["openspec/changes/change-n"])

            self.assertEqual(fia.judge_commit(partial, created), [])

    def test_an_unreadable_ratification_lookup_refuses_cannot_run(self):
        """Scenario: *The ratification lookup cannot be performed*.

        A SECOND READ AND NOT A COROLLARY OF THE FIRST. The move here is an
        EXACT rename, which git pairs from tree OIDs alone, so the pairing
        SUCCEEDS on the partial checkout — and the read that then fails is the
        one that would say whether the source identity has ever declared
        `Status: ratified`. The gate refuses CANNOT RUN naming that identity
        and that read, and never resolves the unreadable history to "never
        ratified", which is what would pass an undeclared landing on the one
        checkout where nothing can be proved.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td) / "src")
            # NO `.openspec.yaml`: the lineage read is then answered from the
            # TREE alone (the path is absent, which is an ANSWER), so the
            # first read this checkout cannot perform is the ratification
            # lookup itself rather than the declaration beside it.
            directory = packet(root, "change-r", manifest=False)
            commit_all(root, "create the packet")
            set_status(directory, "ratified")
            commit_all(root, "record the ratification")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename the ratified packet exactly")
            partial = blobless_clone(root, Path(td) / "partial")

            # PRECONDITIONS: the pairing IS readable here, and the blob is not.
            self.assertEqual(
                0, _exit(partial, moved, "diff-tree", "-r", "-M", "-l0",
                         "--name-status", f"{moved}^", moved))
            self.assertNotEqual(
                0, _exit(partial, moved, "show",
                         f"{moved}^:openspec/changes/change-r/proposal.md"))

            with self.assertRaises(fia.ArrivalCannotRun) as caught:
                fia.judge_commit(partial, moved)
            message = str(caught.exception)
            self.assertIn(fia.UNREADABLE, message)
            self.assertIn("the ratification lookup for identity `change-r`",
                          message)
            self.assertIn("git show", message)
            self.assertIn("never ratified", message)

    def test_a_pull_request_run_without_its_range_refuses_cannot_run(self):
        """A CHECKOUT WITHOUT HISTORY MUST REFUSE RATHER THAN PASS BLIND.

        `fetch-depth: 0` is what makes `HEAD^1..HEAD^2` resolve on a
        `pull_request` run. Where it does not, the gate cannot read the range
        it judges, and a gate that cannot read its range and reports a pass is
        a gate that confers nothing. (This is NOT `tasks.md` § 6.4's
        not-taken shallow-checkout refusal class, which is about a commit at a
        GRAFTED BOUNDARY inside a range that did resolve; that case still
        answers "no parent, no pairing" and takes no refusal.)
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            with self.assertRaises(fia.ArrivalCannotRun) as caught:
                fia.resolve_range(root, None, None,
                                  env={"GITHUB_EVENT_NAME": "pull_request"})
            self.assertIn("fetch-depth: 0", str(caught.exception))
            self.assertIn(fia.UNREADABLE, str(caught.exception))

            # …and outside such a run there is simply no range, which the
            # report SAYS rather than reporting a clean one it never read.
            report = fia.scan(root, env={})
            self.assertIn("no commit range", report.range_note)
            self.assertEqual(report.findings, [])

    def test_a_present_manifest_that_does_not_parse_is_refused_not_read_as_empty(
            self):
        """AN UNREADABLE MANIFEST IS NOT A PACKET THAT DECLARES NOTHING.

        `proposal_support.load_packet` answers None for three states — absent,
        unparseable YAML, and a top-level that is not a mapping — and only the
        first is an answer. The corpus arm used to hand all three to
        `former_id_problems` as a packet with no declaration, so a malformed
        `.openspec.yaml` was swallowed by the parser that could not reach it
        and the sweep reported a clean corpus. The commit-range arm always drew
        the distinction; this is that rule over the working tree.
        (Copilot, PR #1039.)
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-a", ratified=True)
            (directory / ".openspec.yaml").write_text(
                "former_ids: [change-b\nschema: spec-driven\n",
                encoding="utf-8")
            commit_all(root, "a manifest that is not parseable YAML")

            # PRECONDITION: the shared reader cannot tell this from an absent
            # manifest, which is exactly why this arm must.
            self.assertIsNone(support.load_packet(directory))
            problems = fia.corpus_problems(root)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("is PRESENT and did not read as a mapping",
                          problems[0])
            self.assertIn("change-a", problems[0])
            with no_event():
                self.assertEqual(cli.main([str(root)]), 1)

            # A top-level that parses but is not a mapping is the same state.
            (directory / ".openspec.yaml").write_text(
                "- former_ids\n", encoding="utf-8")
            commit_all(root, "a manifest whose top level is a sequence")
            self.assertIn("did not read as a mapping",
                          fia.corpus_problems(root)[0])

            # …and a packet with NO manifest at all is still simply silent.
            (directory / ".openspec.yaml").unlink()
            commit_all(root, "remove the manifest")
            self.assertEqual(fia.corpus_problems(root), [])

    def test_a_manifest_that_is_not_a_mapping_is_refused_by_the_range_arm_too(
            self):
        """THE SAME STATE, REFUSED BY BOTH ARMS — the corpus sweep's answer and
        the commit range's answer to one broken `.openspec.yaml` must agree.

        `yaml.safe_load` answers None for an empty document and a list for a
        sequence; handing either on as "no packet" gives
        `declared_former_ids` exactly what an ABSENT manifest gives it, so a
        DRAFT RENAME carrying a broken manifest passed the range arm while the
        corpus arm refused the identical tree. The read now refuses, naming
        what it parsed as. (Copilot, PR #1039.)
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r")
            (directory / ".openspec.yaml").write_text(
                "- former_ids\n", encoding="utf-8")
            commit_all(root, "a draft whose manifest is a sequence")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            moved = commit_all(root, "rename the draft")

            with self.assertRaises(support.FormerIdError) as caught:
                fia.judge_commit(root, moved)
            message = str(caught.exception)
            self.assertIn("did not read as a mapping", message)
            self.assertIn("it parsed as a list", message)
            self.assertIn("openspec/changes/change-r/.openspec.yaml", message)

            # …and the CLI reports it and exits 1 — a malformed declaration is
            # a refusal of the packet, not the CANNOT RUN of a checkout.
            refused = subprocess.run(
                [sys.executable, str(VALIDATOR), str(root),
                 "--base", f"{moved}^", "--head", moved],
                capture_output=True, text=True)
            self.assertEqual(refused.returncode, 1, refused.stdout)
            self.assertIn("did not read as a mapping", refused.stdout)

            # AN EMPTY MANIFEST IS THE SAME STATE UNDER ANOTHER SPELLING,
            # and it is named as what it is.
            (changes / "change-s" / ".openspec.yaml").write_text(
                "\n", encoding="utf-8")
            empty = commit_all(root, "empty the manifest")
            with self.assertRaises(support.FormerIdError) as caught:
                fia.declared_at(root, empty, "openspec/changes/change-s",
                                "change-s")
            self.assertIn("an empty document", str(caught.exception))

            # …and a commit that moves NOTHING reports the unreadable
            # declaration as a finding rather than raising out of the run, so
            # the rest of the range is still judged. (The finding names the
            # list at the parent, which is the first of the two reads that
            # could not be made sense of.)
            findings = fia.judge_commit(root, empty)
            self.assertEqual(len(findings), 1, [f.message for f in findings])
            self.assertIn("did not read as a mapping", findings[0].message)

    def test_a_manifest_that_cannot_be_read_at_all_is_refused_not_skipped(
            self):
        """A READ THAT RAISES IS STILL A READ THAT FAILED.

        Two states `is_file()` plus `load_packet` used to let through: bytes
        that are not UTF-8, which `load_packet` decodes and therefore RAISES
        over (it catches only `YAMLError`), leaving this gate with an exit its
        own contract does not name; and a `.openspec.yaml` that is PRESENT and
        is not a regular file, which `is_file()` reads as absent. Both are now
        refusals that name the packet, and the ownership sweep — which
        re-reads every manifest in a module this slice imports and does not
        edit — is caught rather than allowed to raise through the CLI.
        (Copilot, PR #1039.)
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-a", ratified=True)
            (directory / ".openspec.yaml").write_bytes(
                b"former_ids:\n  - \xff\xfe not utf-8\n")
            commit_all(root, "a manifest that is not UTF-8")

            with self.assertRaises(UnicodeDecodeError):
                support.load_packet(directory)          # PRECONDITION
            problems = fia.corpus_problems(root)
            self.assertTrue(problems, problems)
            self.assertIn("could not be read at all", problems[0])
            self.assertIn("change-a", problems[0])
            # …the sweep's own re-read of the same file is a refusal and not
            # a traceback, so the run still ends in the documented exit 1.
            self.assertTrue(any("ownership sweep" in p for p in problems),
                            problems)
            with no_event():
                self.assertEqual(cli.main([str(root)]), 1)

            # A PATH THAT IS PRESENT AND IS NOT A REGULAR FILE is the same
            # defect wearing a different shape.
            (directory / ".openspec.yaml").unlink()
            (directory / ".openspec.yaml").mkdir()
            self.assertIsNone(support.load_packet(directory))
            problems = fia.corpus_problems(root)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("did not read as a mapping", problems[0])
            self.assertIn("not a regular file", problems[0])

    def test_a_symlink_is_refused_and_is_never_read_through(self):
        """WHAT `ls-tree` CANNOT SEE, THIS ARM DOES NOT READ.

        Git stores a symlink as a BLOB whose content is a path, so the
        commit-range and fail-closed arms — which read `git ls-tree` — see no
        packet directory at a symlinked path and no manifest at a symlinked
        one. A working-tree walk that follows links would adjudicate a tree no
        commit carries, possibly outside the checkout; and because `exists()`
        follows links, a DANGLING manifest link would read as no manifest at
        all, which is the silence this arm exists to refuse. Both are refused,
        and the content behind the link is never read. (Copilot, PR #1039.)
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td) / "repo")
            outside = Path(td) / "outside"
            (outside / "change-x").mkdir(parents=True)
            (outside / "change-x" / ".openspec.yaml").write_text(
                MANIFEST + "former_ids:\n  - change-from-outside\n",
                encoding="utf-8")
            packet(root, "change-a", ratified=True)
            changes = root / "openspec" / "changes"
            (changes / "change-linked").symlink_to(outside / "change-x")
            commit_all(root, "a symlink where a packet directory would be")

            problems = fia.corpus_problems(root)
            self.assertEqual(len(problems), 2, problems)
            self.assertIn("is a SYMLINK where a change packet directory",
                          problems[0])
            self.assertIn("change-linked", problems[0])
            # THE TARGET IS NEVER READ BY THIS ARM…
            self.assertNotIn("change-from-outside", problems[0])
            # …AND THE OWNERSHIP SWEEP IS NOT RUN OVER A TREE THIS ARM HAS
            # REFUSED, because that sweep walks the working tree in a shared
            # reader this slice imports and does not edit. PR #1038 (merged
            # to main at `701c8fde`) added the same containment guard to
            # that reader, so it no longer follows THIS link either —
            # measured directly below, so the claim stays measured rather
            # than stale. The skip is kept anyway: this arm's own refusal
            # should not start depending on staying in step with a guard a
            # module it does not review happens to carry today.
            self.assertIn("ownership sweep over this corpus was NOT run",
                          problems[1])
            self.assertEqual(list(support.former_identity_claimants(root)),
                             ["change-a"])

            # A SYMLINKED MANIFEST, and a DANGLING one, are the same rule one
            # level down.
            (changes / "change-linked").unlink()
            manifest = changes / "change-a" / ".openspec.yaml"
            manifest.unlink()
            manifest.symlink_to(outside / "change-x" / ".openspec.yaml")
            commit_all(root, "a symlinked manifest")
            problems = fia.corpus_problems(root)
            self.assertEqual(len(problems), 2, problems)
            self.assertIn("is a SYMLINK", problems[0])
            self.assertNotIn("change-from-outside", problems[0])

            manifest.unlink()
            manifest.symlink_to(outside / "gone.yaml")
            self.assertFalse(manifest.exists())      # PRECONDITION: dangling
            problems = fia.corpus_problems(root)
            self.assertEqual(len(problems), 2, problems)
            self.assertIn("is a SYMLINK", problems[0])
            with no_event():
                self.assertEqual(cli.main([str(root)]), 1)

    def test_a_symlinked_corpus_root_is_refused_before_anything_is_walked(
            self):
        """THE SAME RULE AT THE ANCESTORS, asked BEFORE `is_dir()`.

        A symlinked `openspec/` or `openspec/changes/` moves the WHOLE corpus
        somewhere no commit carries: every per-packet check would then read
        files the tree arm cannot see, while never seeing a symlink itself,
        because `is_dir()` and `iterdir()` both follow links. The run says the
        corpus was not read rather than reporting what it found down there.
        (Copilot, PR #1039.)
        """
        for level in ("openspec", "openspec/changes"):
            with self.subTest(level=level):
                with TemporaryDirectory() as td:
                    root = new_repo(Path(td) / "repo")
                    outside = Path(td) / "outside"
                    elsewhere = outside / "openspec" / "changes" / "change-x"
                    elsewhere.mkdir(parents=True)
                    (elsewhere / ".openspec.yaml").write_text(
                        MANIFEST + "former_ids:\n  - change-from-outside\n",
                        encoding="utf-8")
                    link = root / level
                    link.parent.mkdir(parents=True, exist_ok=True)
                    link.symlink_to(outside / level)
                    self.assertTrue(link.is_dir())    # PRECONDITION: followed

                    problems = fia.corpus_problems(root)
                    self.assertEqual(len(problems), 1, problems)
                    self.assertIn(f"`{level}/` is a SYMLINK", problems[0])
                    self.assertNotIn("change-from-outside", problems[0])
                    self.assertIn("no declaration, no standing id and no "
                                  "ownership question was answered",
                                  problems[0])

    def test_a_grafted_boundary_takes_no_refusal(self):
        """`tasks.md` § 6.4, NOT TAKEN, asserted so it stays not taken.

        At a shallow checkout's grafted boundary git reports no parents and
        therefore no pairing. Refusing every such checkout outright is a new
        refusal class on a gate with NO BYPASS FLAG and belongs to a change
        that says so; until then the honest answer is that a commit with no
        parent brought nothing in by a move.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            packet(root, "change-r", ratified=True)
            first = commit_all(root, "create the ratified packet")
            self.assertEqual(fia.commit_parents(root, first), [])
            self.assertEqual(fia.judge_commit(root, first), [])


class BoundEntryTests(unittest.TestCase):
    """§ 2.4 and § 2.5 — *AN ENTRY IS ADDED ONLY BY THE COMMIT THAT PERFORMS
    THE MOVE IT RECORDS*, and the list is append-only ACROSS commits."""

    def standing(self, root: Path) -> Path:
        directory = packet(root, "change-a", ratified=True)
        commit_all(root, "create a standing ratified packet")
        return directory

    def test_a_former_id_appended_by_a_commit_that_moves_nothing_is_refused(
            self):
        """Scenario: *A former id is appended by a commit that moves
        nothing*.

        A standing packet adds a former id in a commit that performs no move
        of that id into it. The declaration is refused, naming the id and the
        commit.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = self.standing(root)
            declare(directory, "change-b")
            added = commit_all(root, "append a former id, moving nothing")

            findings = fia.judge_commit(root, added)
            self.assertEqual(len(findings), 1,
                             [f.message for f in findings])
            message = findings[0].message
            self.assertIn("'change-b'", message)
            self.assertIn(added[:12], message)
            self.assertIn("performs NO move into that packet", message)
            self.assertIn("AN ENTRY IS ADDED ONLY BY THE COMMIT THAT PERFORMS "
                          "THE MOVE IT RECORDS", message)

    def test_an_archived_id_appended_by_a_standing_packet_is_refused(self):
        """*ABSENCE OF A LIVE DIRECTORY IS NOT PROOF OF PREDECESSORSHIP*, and
        an ARCHIVED id is the first of the two ways to have none.

        Without this rule a standing packet could append an archived
        identity in an ordinary edit, acquire that identity's ratification as
        its baseline, and capture every reference written under it.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = self.standing(root)
            packet(root, "change-old", ratified=True, archived="2026-01-01")
            commit_all(root, "carry an archived packet in the corpus")
            declare(directory, "change-old")
            added = commit_all(root, "append the ARCHIVED id")

            findings = fia.judge_commit(root, added)
            self.assertEqual(len(findings), 1,
                             [f.message for f in findings])
            self.assertIn("'change-old'", findings[0].message)
            self.assertIn("an id that has archived", findings[0].message)

    def test_an_id_that_never_existed_appended_by_a_standing_packet_is_refused(
            self):
        """…and an id that NEVER EXISTED is the second way to have no live
        directory. The two are refused by the same rule, which is why the rule
        is about the MOVE and not about the directory."""
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = self.standing(root)
            declare(directory, "change-never-existed")
            added = commit_all(root, "append an id that never existed")

            findings = fia.judge_commit(root, added)
            self.assertEqual(len(findings), 1,
                             [f.message for f in findings])
            self.assertIn("'change-never-existed'", findings[0].message)
            # The corpus reader would not refuse this on its own: an entry
            # naming an id that resolves nowhere is not a SHAPE defect, which
            # is exactly why the binding rule needs a commit range.
            self.assertEqual(
                support.former_id_problems(
                    "change-a", support.load_packet(directory)), [])


class MultiSourceTests(unittest.TestCase):
    """A DESTINATION BROUGHT IN FROM MORE THAN ONE SOURCE, bound to every one
    of them and to none of them BY NAME.

    Git can pair files from two source packets into one newly created
    destination. A mapping that kept one source per destination kept the
    LEXICALLY LAST, so § 2.4's question — which newly added former id is bound
    to a move this commit performed — was answered by the alphabet: the same
    tree with `change-a` and `change-b` swapped gave a different verdict.
    (Copilot, PR #1039.)
    """

    def dissolve(self, root: Path, declared: list[str]) -> str:
        """Two ratified packets dissolved into one new one, in one commit."""
        first = packet(root, "change-a", ratified=True)
        second = packet(root, "change-b", ratified=True)
        (first / "a.md").write_text("a" * 600, encoding="utf-8")
        (second / "b.md").write_text("b" * 600, encoding="utf-8")
        commit_all(root, "two ratified packets")
        changes = root / "openspec" / "changes"
        third = changes / "change-c"
        third.mkdir()
        git(root, "mv", str(first / "a.md"), str(third / "a.md"))
        git(root, "mv", str(second / "b.md"), str(third / "b.md"))
        git(root, "mv", str(first / "proposal.md"), str(third / "proposal.md"))
        git(root, "rm", "-q", str(first / ".openspec.yaml"),
            str(second / "proposal.md"), str(second / ".openspec.yaml"))
        declare(third, *declared)
        return commit_all(root, "dissolve two packets into one")

    def test_a_two_source_arrival_is_judged_the_same_whichever_id_is_declared(
            self):
        """THE SAME TREE, THE SAME VERDICT, WHATEVER THE PACKETS ARE CALLED.

        Declaring either source leaves exactly ONE refusal — the arrival from
        the source that went undeclared — and no `bound to no move` finding
        against the entry that IS a source of this commit's moves. Measured on
        the parent commit: declaring `change-a` produced TWO findings and
        declaring `change-b` produced ONE, over the identical history.
        """
        for declared in (["change-a"], ["change-b"]):
            with self.subTest(declared=declared):
                with TemporaryDirectory() as td:
                    root = new_repo(Path(td))
                    head = self.dissolve(root, declared)

                    parent = fia.commit_parents(root, head)[0]
                    diff = fia.diff_at(root, parent, head)
                    self.assertEqual(
                        fia.relocations_at(
                            diff, fia.packet_dirs_at(root, parent),
                            fia.packet_dirs_at(root, head)),
                        [("openspec/changes/change-a",
                          "openspec/changes/change-c"),
                         ("openspec/changes/change-b",
                          "openspec/changes/change-c")])

                    findings = fia.judge_commit(root, head)
                    self.assertEqual([f.status for f in findings],
                                     [fia.UNDECLARED],
                                     [f.message for f in findings])
                    # …and the refusal names the OTHER source, which is the
                    # move that went undeclared.
                    other = ("change-b" if declared == ["change-a"]
                             else "change-a")
                    self.assertIn(f"`openspec/changes/{other}/`",
                                  findings[0].message)

    def test_an_entry_no_source_carried_is_still_bound_to_nothing(self):
        """AND THE RULE § 2.4 STATES IS STILL ENFORCED over both sources: an
        entry that neither source carried and neither source is remains an
        entry bound to no move, and the refusal says so naming every source.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            head = self.dissolve(root, ["change-a", "change-gone"])

            findings = fia.judge_commit(root, head)
            bound = [f for f in findings if f.status is None]
            self.assertEqual(len(bound), 1, [f.message for f in findings])
            self.assertIn("'change-gone'", bound[0].message)
            self.assertIn("MORE THAN ONE packet directory", bound[0].message)
            self.assertIn("`openspec/changes/change-a`", bound[0].message)
            self.assertIn("`openspec/changes/change-b`", bound[0].message)


class ConsumedReaderTests(unittest.TestCase):
    """THE FOUR READERS SLICE 1 LANDED AND NOBODY CALLED, EACH PROVED CALLED.

    `former_id_problems`, `append_only_problems`,
    `standing_former_id_problems` and `former_identity_ownership_problems`
    were referenced only inside their own definitions and their own tests when
    this slice began — measured, and named in `design.md` D11(2) as the defect
    this realization must not repeat. Each test below patches the reader with
    a wrapper around the real one and asserts BOTH that the call fired and
    that the refusal this validator prints is the reader's own words.
    """

    def test_the_shape_refusals_are_reported_by_this_validator(self):
        """§ 2.1, and the proof that `former_id_problems` is CALLED."""
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-a", ratified=True)
            (directory / ".openspec.yaml").write_text(
                MANIFEST + "former_ids: change-b\n", encoding="utf-8")
            commit_all(root, "declare a scalar where a sequence is required")

            with mock.patch.object(
                    support, "former_id_problems",
                    wraps=support.former_id_problems) as spy:
                problems = fia.corpus_problems(root)
            self.assertTrue(spy.called)
            self.assertTrue(problems)
            self.assertIn("a SEQUENCE of change ids is required",
                          problems[0])

            # …and the CLI reports it and exits 1.
            with no_event():
                self.assertEqual(cli.main([str(root)]), 1)

    def test_the_append_only_rule_is_enforced_by_this_validator(self):
        """§ 2.5, and the proof that `append_only_problems` is CALLED.

        THE ATTACK IT CLOSES: a lawful move declared at its landing and the
        declaration DELETED the day after, in a commit no arrival check ever
        looks at — which would hand the archive gate the later ratification
        under the current id, the very baseline this mechanism exists to keep
        it away from.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-r", ratified=True)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            declare(changes / "change-s", "change-r")
            commit_all(root, "move and declare it lawfully")
            declare(changes / "change-s")
            deleted = commit_all(root, "delete the declaration the day after")

            with mock.patch.object(
                    support, "append_only_problems",
                    wraps=support.append_only_problems) as spy:
                findings = fia.judge_commit(root, deleted)
            self.assertTrue(spy.called)
            self.assertEqual(len(findings), 1,
                             [f.message for f in findings])
            self.assertIn("APPEND-ONLY ACROSS COMMITS", findings[0].message)
            self.assertIn("REMOVED 'change-r'", findings[0].message)

            # A REORDER is the same defect by another author mistake, and is
            # named separately.
            git(root, "reset", "-q", "--hard", "HEAD~1")
            declare(changes / "change-s", "change-r", "change-q")
            commit_all(root, "append a second entry")
            declare(changes / "change-s", "change-q", "change-r")
            reordered = commit_all(root, "reorder the established entries")
            self.assertIn("REORDERED",
                          fia.judge_commit(root, reordered)[0].message)

    def test_a_declared_id_that_still_stands_is_refused_by_this_validator(
            self):
        """§ 2.3, and the proof that `standing_former_id_problems` is CALLED.

        Scenario: *A declared former id still stands in the tree*. A packet
        that still stands was COPIED and not moved, and a copy is a new packet
        with its own origin — refused naming BOTH ids, because the repair is a
        choice between them.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            packet(root, "change-r", ratified=True)
            forked = packet(root, "change-s")
            declare(forked, "change-r")
            commit_all(root, "declare a former id that still stands")

            with mock.patch.object(
                    support, "standing_former_id_problems",
                    wraps=support.standing_former_id_problems) as spy:
                problems = fia.corpus_problems(root)
            self.assertTrue(spy.called)
            # TWO REFUSALS OVER ONE TREE, and the second is the requirement's
            # own other half: an id that is AT ONCE a live packet id and some
            # packet's declared former id is an identity with two claimants,
            # which the ownership sweep refuses naming both.
            self.assertEqual(len(problems), 2, problems)
            self.assertIn("STILL STANDS in this tree", problems[0])
            self.assertIn("change-r", problems[0])
            self.assertIn("change-s", problems[0])
            self.assertIn("EXACTLY ONE OWNER", problems[1])
            self.assertIn("claimed by 2 packets", problems[1])

    def test_two_packets_claiming_one_former_identity_are_refused(self):
        """Scenario: *Two packets claim the same former identity*, and the
        proof that `former_identity_ownership_problems` is CALLED over a tree
        where it has something to say.

        An identity claimed twice resolves to a SET, and a baseline chosen
        from a set is a baseline chosen by the resolver rather than by an
        author. The refusal names EVERY claimant and settles nothing.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            first = packet(root, "change-s")
            second = packet(root, "change-t")
            declare(first, "change-gone")
            declare(second, "change-gone")
            commit_all(root, "two packets claim one former identity")

            with mock.patch.object(
                    support, "former_identity_ownership_problems",
                    wraps=support.former_identity_ownership_problems) as spy:
                problems = fia.corpus_problems(root)
            spy.assert_called_once_with(root)
            self.assertEqual(len(problems), 1, problems)
            self.assertIn("claimed by 2 packets", problems[0])
            self.assertIn("EXACTLY ONE OWNER", problems[0])
            with no_event():
                self.assertEqual(cli.main([str(root)]), 1)

    def test_the_ownership_sweep_runs_over_the_live_corpus(self):
        """PLAN Q3, RECOMMENDATION (a), TAKEN: the sweep's ONE caller is this
        validator's corpus arm, and it runs over THIS repository.

        `former_identity_ownership_problems` is a whole-corpus check that had
        no caller at all. It is called here, with this repository's own root,
        and this repository passes it — which is the reading that has to stay
        true for the sweep to be worth running. `proposal-support.py verify`
        is deliberately NOT a second caller: two callers for one sweep is two
        places to keep in step.
        """
        with mock.patch.object(
                support, "former_identity_ownership_problems",
                wraps=support.former_identity_ownership_problems) as spy:
            problems = fia.corpus_problems(REPO_ROOT)
        spy.assert_called_once_with(REPO_ROOT)
        self.assertEqual(problems, [])
        self.assertEqual(support.former_identity_ownership_problems(
            REPO_ROOT), [])


class RangeTests(unittest.TestCase):
    """`base..head` — THE PULL REQUEST'S OWN COMMITS AND NOTHING ELSE.

    Every other test here asks ONE commit. This one asks the range, which is
    what CI actually runs: `design.md` D3 says the gate *"reads the pull
    request's own commit range and, for each commit, asks whether a change
    packet directory arrived by a move from another change packet directory"*,
    so the range's two properties are load-bearing in their own right — every
    commit INSIDE it is judged, and no commit outside it is. A gate that read
    one commit too few would miss the landing it exists for; a gate that read
    one too many would red a pull request for history it did not write.
    """

    def history(self, root: Path) -> dict:
        """One repository carrying every kind of landing at once: an
        undeclared rename BEFORE the base, a declared move, an archive
        relocation, and an undeclared rename at the head."""
        t = {}
        packet(root, "change-p", ratified=True)
        packet(root, "change-x", ratified=True)
        t["a"] = commit_all(root, "create two ratified packets")
        changes = root / "openspec" / "changes"
        git(root, "mv", str(changes / "change-p"), str(changes / "change-q"))
        t["b"] = commit_all(root, "rename p to q with no declaration")
        git(root, "mv", str(changes / "change-q"), str(changes / "change-r"))
        declare(changes / "change-r", "change-q")
        t["c"] = commit_all(root, "move q to r and declare the move")
        archive = changes / "archive"
        archive.mkdir(parents=True)
        git(root, "mv", str(changes / "change-r"),
            str(archive / "2026-09-14-change-r"))
        t["d"] = commit_all(root, "archive r under its own id")
        git(root, "mv", str(changes / "change-x"), str(changes / "change-y"))
        t["e"] = commit_all(root, "rename x to y with no declaration")
        return t

    def test_the_range_arm_judges_base_to_head_and_nothing_outside_it(self):
        """THE RANGE IS THE UNIT CI RUNS, and it is asserted as one.

        Over `b..e` the gate judges three commits and refuses exactly one —
        the undeclared rename at the head. The declared move and the archive
        relocation inside the same range pass, so the single refusal is not a
        gate that refuses everything; and the undeclared rename at `b`, which
        is already on the base branch, is NOT reported, because it is not this
        pull request's to repair.

        ANTI-VACUITY: that same `b` is asserted refusable in its own range, so
        its silence over `b..e` is the RANGE and never the gate failing to see
        it.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td) / "src")
            at = self.history(root)

            report = fia.scan(root, base=at["b"], head=at["e"], env={})
            self.assertEqual(report.commits_read, 3)
            self.assertEqual([f.status for f in report.findings],
                             [fia.UNDECLARED],
                             [f.message for f in report.findings])
            self.assertEqual(report.findings[0].commit, at["e"])
            self.assertIn("`openspec/changes/change-x/`",
                          report.findings[0].message)
            self.assertIn("`openspec/changes/change-y/`",
                          report.findings[0].message)
            self.assertIn("3 commit(s) of", report.range_note)
            # …and the two lawful landings were SEEN rather than missed: three
            # moves paired, one of them excepted as an archive relocation.
            self.assertEqual(report.moves_seen, 3)
            self.assertEqual(report.moves_excepted_archive, 1)

            # THE COMMIT BEFORE THE BASE IS REFUSABLE — it is simply not in
            # this range.
            before = fia.scan(root, base=at["a"], head=at["b"], env={})
            self.assertEqual([f.status for f in before.findings],
                             [fia.UNDECLARED])
            self.assertEqual(before.findings[0].commit, at["b"])

            # THE DECLARED MOVE AND THE ARCHIVE RELOCATION PASS AS A RANGE,
            # not only as single commits.
            lawful = fia.scan(root, base=at["b"], head=at["d"], env={})
            self.assertEqual(lawful.findings, [])
            self.assertEqual(lawful.commits_read, 2)

    def test_the_cli_reads_the_same_range_and_exits_on_it(self):
        """THE EXIT CODE IS THE WHOLE OF WHAT A REQUIRED CHECK READS, so the
        range arm is driven as a SUBPROCESS too: exit 1 over a range carrying
        the undeclared rename, exit 0 over the range that carries only lawful
        landings, and exit 2 where a read in that range cannot be performed at
        all.

        The unreadable case is the same history on a blobless clone
        (`design.md` M1): the declared move rewrote `.openspec.yaml` as it
        travelled, so its rename is INEXACT, so the pairing needs a blob the
        checkout cannot produce — and the gate refuses CANNOT RUN over the
        range rather than reporting a clean one.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td) / "src")
            at = self.history(root)

            refused = subprocess.run(
                [sys.executable, str(VALIDATOR), str(root),
                 "--base", at["b"], "--head", at["e"]],
                capture_output=True, text=True)
            self.assertEqual(refused.returncode, 1, refused.stdout)
            self.assertIn(fia.UNDECLARED, refused.stdout)
            self.assertIn("3 commit(s) of", refused.stdout)

            passed = subprocess.run(
                [sys.executable, str(VALIDATOR), str(root),
                 "--base", at["b"], "--head", at["d"]],
                capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stdout)
            self.assertIn("former-id arrival gate passed", passed.stdout)
            self.assertIn("1 archive relocation(s) excepted by id",
                          passed.stdout)

            partial = blobless_clone(root, Path(td) / "partial")
            cannot = subprocess.run(
                [sys.executable, str(VALIDATOR), str(partial),
                 "--base", at["b"], "--head", at["e"]],
                capture_output=True, text=True)
            self.assertEqual(cannot.returncode, 2, cannot.stdout)
            self.assertIn(fia.UNREADABLE, cannot.stdout)
            self.assertIn("CANNOT RUN", cannot.stdout)


class CliTests(unittest.TestCase):
    """The validator CLI: its statuses, its exits, and the flag it has not
    got."""

    def test_there_is_no_bypass_flag(self):
        """*A FLAG WOULD BE THE DECLARATION NOBODY WRITES* (#690, and
        `design.md` D3 in as many words).

        Asserted over the parser's OWN option strings rather than over the
        prose, so a flag added later fails this test whatever the docstring
        says. `--base` and `--head` NAME the range: they cannot silence a
        refusal taken over the commits they name, the corpus arm runs
        regardless of them, and the workflow passes neither.
        """
        options: set[str] = set()
        for action in cli.parser()._actions:
            options.update(action.option_strings)
        self.assertEqual(options, {"-h", "--help", "--base", "--head"})

        banned = ("allow", "bypass", "skip", "force", "ignore", "override",
                  "exempt", "no-verify", "disable", "waive", "grandfather")
        for source in (MODULE, VALIDATOR):
            text = source.read_text(encoding="utf-8")
            for token in text.split():
                if not token.startswith("--"):
                    continue
                flag = token.strip("\"',.`)(").lower()
                for word in banned:
                    self.assertNotIn(
                        word, flag,
                        f"{source.name} names a flag `{flag}` that reads as a "
                        f"bypass")

        # …and the corpus arm cannot be turned off by the range flags: a
        # degenerate range still sweeps the tree and still refuses.
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            forked = packet(root, "change-s")
            packet(root, "change-r", ratified=True)
            declare(forked, "change-r")
            head = commit_all(root, "a copy declaring a standing id")
            self.assertEqual(
                cli.main([str(root), "--base", head, "--head", head]), 1)

    def test_the_cli_exits_one_for_a_refusal_and_two_for_cannot_run(self):
        """The statuses `design.md` D3 ruled, as exit codes a ruleset can see.

        `former-id-undeclared` exit 1, `former-id-arrival-unreadable` exit 2,
        and a clean range exit 0 — driven as a SUBPROCESS, because the exit
        code is the whole of what a required check reads.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td) / "src")
            directory = packet(root, "change-r", ratified=True,
                               body="x" * 40)
            commit_all(root, "create the ratified packet")
            changes = root / "openspec" / "changes"
            git(root, "mv", str(directory), str(changes / "change-s"))
            proposal = changes / "change-s" / "proposal.md"
            proposal.write_text(
                proposal.read_text(encoding="utf-8") + ("y" * 4000) + "\n",
                encoding="utf-8")
            moved = commit_all(root, "rename with no declaration")

            refused = subprocess.run(
                [sys.executable, str(VALIDATOR), str(root),
                 "--base", f"{moved}^", "--head", moved],
                capture_output=True, text=True)
            self.assertEqual(refused.returncode, 1, refused.stdout)
            self.assertIn(fia.UNDECLARED, refused.stdout)
            self.assertIn("FAILED", refused.stdout)

            partial = blobless_clone(root, Path(td) / "partial")
            cannot = subprocess.run(
                [sys.executable, str(VALIDATOR), str(partial),
                 "--base", f"{moved}^", "--head", moved],
                capture_output=True, text=True)
            self.assertEqual(cannot.returncode, 2, cannot.stdout)
            self.assertIn(fia.UNREADABLE, cannot.stdout)
            self.assertIn("CANNOT RUN", cannot.stdout)

            # THE CLEAN RANGE IS ITS OWN REPOSITORY, and deliberately: a
            # declaration added by a LATER commit does not repair the landing
            # that already happened, so the same tree cannot be walked into a
            # pass — § 2.4 refuses the later entry as one bound to no move.
            lawful = new_repo(Path(td) / "lawful")
            directory = packet(lawful, "change-r", ratified=True)
            commit_all(lawful, "create the ratified packet")
            git(lawful, "mv", str(directory),
                str(lawful / "openspec" / "changes" / "change-s"))
            declare(lawful / "openspec" / "changes" / "change-s", "change-r")
            declared = commit_all(lawful, "rename and declare the move")
            passed = subprocess.run(
                [sys.executable, str(VALIDATOR), str(lawful),
                 "--base", f"{declared}^", "--head", declared],
                capture_output=True, text=True)
            self.assertEqual(passed.returncode, 0, passed.stdout)
            self.assertIn("former-id arrival gate passed", passed.stdout)

    def test_a_run_without_pyyaml_refuses_rather_than_sweeping_vacuously(
            self):
        """A GREEN CHECK THAT PROVES NOTHING WAS READ IS NOT A PASS.

        Without PyYAML `load_packet` answers None for every packet and
        `former_id_problems` then has nothing to refuse, so the whole-tree
        sweep would report a clean corpus it never read. The reader refuses at
        the source rather than leaving the property to the workflow that
        installs the dependency — the same anti-vacuity posture
        `signed-execution-chain-gate.yml` writes an assertion step for.
        """
        with TemporaryDirectory() as td:
            root = new_repo(Path(td))
            directory = packet(root, "change-a", ratified=True)
            (directory / ".openspec.yaml").write_text(
                MANIFEST + "former_ids: change-b\n", encoding="utf-8")
            commit_all(root, "declare a scalar where a sequence is required")

            with no_event(), mock.patch.object(support, "yaml", None):
                with self.assertRaises(fia.ArrivalCannotRun) as caught:
                    fia.scan(root, env={})
                # EXIT 2 FOR THE RIGHT REASON: `no_event()` is what keeps this
                # from reading the CANNOT RUN of an unresolvable range as the
                # CANNOT RUN of a missing parser.
                self.assertEqual(cli.main([str(root)]), 2)
            self.assertIn("PyYAML is not available", str(caught.exception))
            self.assertIn(fia.UNREADABLE, str(caught.exception))

            # …and with it, the same tree refuses the DECLARATION rather than
            # the run, which is the difference the guard protects.
            with no_event():
                self.assertEqual(cli.main([str(root)]), 1)

    def test_the_live_corpus_passes_this_gate(self):
        """THE CORPUS ARM, OVER THIS REPOSITORY'S OWN PACKETS.

        The sweep every other test here proves the arithmetic of, run against
        the real tree: every active and archived packet read for the shape of
        its `former_ids:`, for a declared id that still stands, and for an
        identity claimed twice. Exit 0, and the run says what it scanned.
        """
        # THE ENVIRONMENT IS STATED RATHER THAN INHERITED: with the runner's
        # `GITHUB_EVENT_NAME=pull_request` this invocation would judge the
        # pull request's range as well, so what it asserted would differ
        # between a runner and a developer machine. The corpus arm is what
        # this test is about, so it is the only arm it runs.
        environment = {k: v for k, v in os.environ.items()
                       if k != "GITHUB_EVENT_NAME"}
        done = subprocess.run(
            [sys.executable, str(VALIDATOR), str(REPO_ROOT)],
            capture_output=True, text=True, env=environment)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        self.assertIn("no commit range", done.stdout)
        self.assertIn("corpus sweep:", done.stdout)
        self.assertIn("former-id arrival gate passed", done.stdout)

        report = fia.scan(REPO_ROOT, env={})
        self.assertEqual(report.findings, [])
        # ANTI-VACUITY: the sweep is not passing because it read nothing.
        self.assertGreater(report.active_packets, 20)
        self.assertGreater(report.archived_packets, 100)


if __name__ == "__main__":
    unittest.main()
