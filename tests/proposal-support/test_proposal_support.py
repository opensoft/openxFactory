"""Proposal supporting-document lifecycle tests."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "proposal-support.py"
spec = importlib.util.spec_from_file_location("proposal_support", SCRIPT)
support = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = support
spec.loader.exec_module(support)


class ProposalSupportTests(unittest.TestCase):
    def fixture(self, root: Path) -> None:
        (root / "openspec/changes/change-a").mkdir(parents=True)
        topic = root / "ideation/staging/topic-a"
        topic.mkdir(parents=True)
        (root / "ideation/brainstorm").mkdir(parents=True)
        (root / "ideation/brainstorm/source.md").write_text(
            "# Source\n\nStatus: brainstorm\n"
        )
        (topic / "one.md").write_text(
            "# One\n\nStatus: staged\nKind: architecture\n\n"
            "[source](../../brainstorm/source.md)\n"
        )
        (topic / "two.md").write_text(
            "# Two\n\nStatus: record\nKind: report\n"
        )

    def test_dry_run_does_not_move(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            manifest = support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, False,
            )
            self.assertEqual(len(manifest["files"]), 2)
            self.assertTrue((root / "ideation/staging/topic-a/one.md").exists())
            self.assertFalse((root / "openspec/changes/change-a/supporting-docs").exists())

    def test_complete_transition_updates_status_links_and_manifest(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], "nlm-1",
                "2026-07-09", False, True,
            )
            destination = root / "openspec/changes/change-a/supporting-docs"
            text = (destination / "one.md").read_text()
            self.assertIn("Status: draft", text)
            self.assertIn("Proposed by: change-a", text)
            self.assertIn("../../../ideation/brainstorm/source.md", text)
            self.assertIn("Status: record", (destination / "two.md").read_text())
            manifest = support.load_manifest(destination / "manifest.yaml")
            self.assertEqual(manifest["notebook_workspace"], "nlm-1")
            self.assertEqual(manifest["remaining_paths"], [])
            source = "# One\n\nStatus: staged\nKind: architecture\n\n" \
                "[source](../../brainstorm/source.md)\n"
            self.assertEqual(
                manifest["files"][0]["source_sha256"],
                hashlib.sha256(source.encode()).hexdigest(),
            )
            self.assertNotEqual(
                manifest["files"][0]["source_sha256"],
                manifest["files"][0]["sha256"],
            )
            snapshot = destination / manifest["files"][0]["source_snapshot_path"]
            self.assertEqual(snapshot.read_text(), source)
            self.assertFalse((root / "ideation/staging/topic-a").exists())
            self.assertEqual(support.verify_active_support(destination.parent), [])

    def test_committed_source_checksum_is_verified(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c",
                 "user.email=test@example.invalid", "commit", "-qm",
                 "fixture"], cwd=root, check=True,
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            destination = root / "openspec/changes/change-a/supporting-docs"
            manifest_path = destination / "manifest.yaml"
            manifest = support.load_manifest(manifest_path)
            manifest["files"][0]["source_sha256"] = "0" * 64
            manifest_path.write_text(support.manifest_text(manifest))
            errors = support.verify_active_support(destination.parent)
            self.assertTrue(any(
                "staging source checksum mismatch" in error
                for error in errors
            ))

    def test_source_snapshot_verifies_when_git_revision_is_unavailable(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=Test", "-c",
                 "user.email=test@example.invalid", "commit", "-qm",
                 "fixture"], cwd=root, check=True,
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            destination = root / "openspec/changes/change-a/supporting-docs"
            manifest_path = destination / "manifest.yaml"
            manifest = support.load_manifest(manifest_path)
            manifest["source_revision"] = "f" * 40
            manifest_path.write_text(support.manifest_text(manifest))
            self.assertEqual(support.verify_active_support(destination.parent), [])

    def test_tampered_source_snapshot_is_rejected(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            destination = root / "openspec/changes/change-a/supporting-docs"
            manifest = support.load_manifest(destination / "manifest.yaml")
            snapshot = destination / manifest["files"][0]["source_snapshot_path"]
            snapshot.write_text("tampered")
            errors = support.verify_active_support(destination.parent)
            self.assertTrue(any(
                "source snapshot checksum mismatch" in error for error in errors
            ))

    def test_partial_transition_leaves_remainder(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            manifest = support.transition(
                root, "change-a", "ideation/staging/topic-a", ["one.md"],
                None, "2026-07-09", False, True,
            )
            self.assertTrue((root / "ideation/staging/topic-a/two.md").exists())
            self.assertEqual(
                manifest["remaining_paths"],
                ["ideation/staging/topic-a/two.md"],
            )

    def test_rejects_unsafe_and_broken_sources(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            with self.assertRaises(support.SupportError):
                support.transition(
                    root, "change-a", "ideation/staging/topic-a", ["../x"],
                    None, "2026-07-09", False, False,
                )
            (root / "ideation/staging/topic-a/one.md").write_text(
                "# One\n\nStatus: staged\n\n[missing](missing.md)\n"
            )
            with self.assertRaises(support.SupportError):
                support.transition(
                    root, "change-a", "ideation/staging/topic-a", ["one.md"],
                    None, "2026-07-09", False, False,
                )

    def test_archived_transition_preserves_superseded_status(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            archive = root / "openspec/changes/archive/2026-07-09-change-a"
            archive.mkdir(parents=True)
            topic = root / "ideation/staging/topic-a"
            topic.mkdir(parents=True)
            (topic / "history.md").write_text(
                "# History\n\nStatus: superseded\nKind: reference\n"
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", True, True,
            )
            self.assertIn(
                "Status: superseded",
                (archive / "supporting-docs/history.md").read_text(),
            )

    def test_package_is_reproducible_and_verifiable(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            directory = root / "openspec/changes/change-a"
            first, _ = support.deterministic_bundle(directory / "supporting-docs")
            second, _ = support.deterministic_bundle(directory / "supporting-docs")
            self.assertEqual(first, second)
            support.package(
                root, "change-a", "2026-07-09", False, False, True
            )
            self.assertEqual(support.verify_archive(directory), [])
            bundle = directory / "supporting-docs.tar.gz"
            bundle.write_bytes(bundle.read_bytes() + b"corrupt")
            self.assertTrue(support.verify_archive(directory))

    @unittest.skipUnless(shutil.which("openspec"), "openspec CLI required")
    def test_archive_wrapper_preserves_bundle(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(
                ["openspec", "init", str(root), "--tools", "none"],
                check=True, capture_output=True, text=True,
            )
            subprocess.run(
                ["openspec", "new", "change", "change-a"], cwd=root,
                check=True, capture_output=True, text=True,
            )
            change = root / "openspec/changes/change-a"
            (change / "proposal.md").write_text(
                "## Why\n\nTest archive support.\n\n"
                "## What Changes\n\n- Add test capability.\n\n"
                "## Capabilities\n\n### New Capabilities\n\n"
                "- `test-capability`: test\n\n"
                "### Modified Capabilities\n\n- None.\n\n"
                "## Impact\n\n- Tests only.\n"
            )
            (change / "design.md").write_text(
                "## Context\n\nTest.\n\n## Goals / Non-Goals\n\n"
                "**Goals:** archive.\n\n**Non-Goals:** none.\n\n"
                "## Decisions\n\nUse support bundle.\n\n"
                "## Risks / Trade-offs\n\nNone.\n"
            )
            spec_dir = change / "specs/test-capability"
            spec_dir.mkdir(parents=True)
            (spec_dir / "spec.md").write_text(
                "## ADDED Requirements\n\n"
                "### Requirement: Archive fixture\n"
                "The fixture SHALL archive.\n\n"
                "#### Scenario: Archive\n"
                "- **WHEN** the change archives\n"
                "- **THEN** the fixture MUST remain\n"
            )
            (change / "tasks.md").write_text(
                "## 1. Test\n\n- [x] 1.1 Complete fixture\n"
            )
            topic = root / "ideation/staging/topic-a"
            topic.mkdir(parents=True)
            (topic / "source.md").write_text(
                "# Source\n\nStatus: staged\nKind: reference\n"
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-07-09", False, True,
            )
            support.archive_change(
                root, "change-a", "2026-07-09", False, True
            )
            archived = list((root / "openspec/changes/archive").glob(
                "????-??-??-change-a"
            ))
            self.assertEqual(len(archived), 1)
            self.assertTrue((archived[0] / "supporting-docs.tar.gz").is_file())
            self.assertEqual(support.verify_archive(archived[0]), [])

    def test_a_status_line_inside_a_code_fence_is_an_example_not_the_status(self):
        """REGRESSION, 2026-08-15. The first fragment this mover ever moved
        carried a copy-pasteable template skeleton whose fenced example header
        read `Status: staged`. The verifier's multiline regex matched the
        EXAMPLE and failed a bundle whose real header the mover had already
        transitioned to `draft` — which would have blocked the archive gate on
        a bundle that was correct."""
        fenced = (
            "# Topic\n\nStatus: draft\nKind: reference\n\n"
            "Copy this skeleton:\n\n"
            "```markdown\n# Staged: <title>\n\nStatus: staged\nKind: reference\n```\n"
        )
        self.assertFalse(support._declares_staged_status(fenced))

        # ...and the real thing is still caught, outside any fence.
        real = "# Topic\n\nStatus: staged\nKind: reference\n"
        self.assertTrue(support._declares_staged_status(real))

        # An unclosed fence must not swallow a later real header.
        unclosed = "# Topic\n\n```\nexample\n```\n\nStatus: staged\n"
        self.assertTrue(support._declares_staged_status(unclosed))

    def test_a_moved_fragment_carrying_a_fenced_example_still_verifies(self):
        """The same defect end to end: transition a fragment whose body holds a
        fenced `Status: staged` example, then verify the bundle."""
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            topic = root / "ideation/staging/topic-a"
            (topic / "source.md").write_text(
                "# Source\n\nStatus: staged\nKind: reference\n\n"
                "```markdown\nStatus: staged\n```\n"
            )
            support.transition(
                root, "change-a", "ideation/staging/topic-a", [], None,
                "2026-08-15", False, True,
            )
            moved = root / "openspec/changes/change-a/supporting-docs/source.md"
            self.assertIn("Status: draft", moved.read_text())
            self.assertEqual(
                support.verify_active_support(root / "openspec/changes/change-a"), [])


class AuthorshipRecordTests(unittest.TestCase):
    """`refine-demote-round-trip-mechanics` part 3: the proposal gate records its
    authorship ONCE PER DOCUMENT, not once per attempt.

    A document may legitimately reach proposal, be demoted, be worked, and reach
    proposal again — the round-trip guarantee exists precisely so that lap is
    normal. Appending a fresh `Proposed by:` line each time turns a normal lap
    into an ambiguous record: several lines each claiming to name the proposing
    change say nothing about which one is current.
    """

    def rendered(self, root: Path, text: str, change: str = "change-b") -> str:
        path = root / "doc.md"
        path.write_text(text, encoding="utf-8")
        return support.proposed_content(path, path, {}, root, change).decode("utf-8")

    def test_a_first_lap_adds_the_authorship_line(self):
        with TemporaryDirectory() as td:
            out = self.rendered(Path(td), "# One\n\nStatus: staged\nKind: reference\n")
        self.assertEqual(
            out, "# One\n\nStatus: draft\nProposed by: change-b\nKind: reference\n")

    def test_a_second_lap_updates_the_line_rather_than_adding_another(self):
        """The shape a demoted document comes back in: the demote restores
        `Status: staged` and correctly leaves the authorship line alone, so the
        next transition sees both."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td),
                "# One\n\nStatus: staged\nProposed by: change-a\nKind: reference\n")
        self.assertEqual(
            out, "# One\n\nStatus: draft\nProposed by: change-b\nKind: reference\n")
        self.assertEqual(out.count("Proposed by:"), 1)

    def test_a_third_lap_still_leaves_exactly_one_line(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            once = self.rendered(root, "# One\n\nStatus: staged\nKind: reference\n",
                                 "change-a")
            twice = self.rendered(root, once.replace("Status: draft", "Status: staged"),
                                  "change-b")
            thrice = self.rendered(root, twice.replace("Status: draft", "Status: staged"),
                                   "change-c")
        self.assertEqual(
            [line for line in thrice.splitlines() if line.startswith("Proposed by:")],
            ["Proposed by: change-c"])

    def test_the_update_preserves_a_crlf_documents_line_endings(self):
        """`.*$` would eat the `\\r` and leave the one rewritten line LF in a CRLF
        file — the same corpus-integrity class the demote's move arm was fixed for.
        Only the authorship value changes; every other byte after it survives."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td),
                "# One\r\n\r\nStatus: staged\r\nProposed by: change-a\r\n"
                "Kind: reference\r\n\r\nbody\r\n")
        self.assertIn("Proposed by: change-b\r\n", out)
        self.assertIn("Kind: reference\r\n\r\nbody\r\n", out)

    def test_the_status_flip_still_happens_when_a_line_already_exists(self):
        """The status flip itself is unchanged by this part — the update arm must
        not become an arm that forgets to flip."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td), "# One\n\nStatus: staged\nProposed by: change-a\n")
        self.assertIn("Status: draft", out)
        self.assertNotIn("Status: staged", out)

    def test_a_non_staged_document_is_left_alone(self):
        """The gate only writes authorship on the staged->draft flip; a `record`
        document carrying its own historical line is not rewritten."""
        with TemporaryDirectory() as td:
            out = self.rendered(
                Path(td), "# One\n\nStatus: record\nProposed by: change-a\n")
        self.assertIn("Proposed by: change-a", out)

    def test_the_end_to_end_round_trip_shape_carries_one_line(self):
        """Driven through `transition`, not just the renderer."""
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "openspec/changes/change-b").mkdir(parents=True)
            topic = root / "ideation/staging/topic-a"
            topic.mkdir(parents=True)
            (topic / "one.md").write_text(
                "# One\n\nStatus: staged\nProposed by: change-a\nKind: reference\n",
                encoding="utf-8")
            support.transition(root, "change-b", "ideation/staging/topic-a", [],
                               None, "2026-08-19", False, True)
            moved = (root / "openspec/changes/change-b/supporting-docs/one.md"
                     ).read_text(encoding="utf-8")
        self.assertEqual(
            [line for line in moved.splitlines() if line.startswith("Proposed by:")],
            ["Proposed by: change-b"])


if __name__ == "__main__":
    unittest.main()
