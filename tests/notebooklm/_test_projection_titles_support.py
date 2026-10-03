from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from tests.notebooklm.typed_sync_contracts import load_typed_sync

sync = load_typed_sync()
from tests.notebooklm._projection_test_support import (
    RECORD_NAMESAKE,
    TITLE_MIGRATION,
    TITLE_UNMOVED,
    TitleCorpus,
    bare_stem_derivation,
    legacy_stem,
    one_level_derivation,
)


class TitleUniquenessTests(TitleCorpus, unittest.TestCase):
    def scenario_the_fourteen_enumerated_titles_move_exactly_as_designed(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            desired, _specs = sync.scan(root)
            for book, rel, status, before, after in TITLE_MIGRATION:
                self.assertEqual(
                    f"[{status}] {before.split(']', 1)[1].split(':', 1)[0].strip()}: {legacy_stem(rel)}",
                    before,
                    f"the BEFORE column of {rel} is not what the replaced derivation produced",
                )
                self.assertIn(rel, desired[book], f"{rel} left book {book}")
                self.assertEqual(
                    desired[book][rel],
                    after,
                    f"{rel} did not land on design.md § 6's title",
                )
                self.assertNotEqual(
                    desired[book][rel], before, f"{rel} was enumerated as a rename"
                )

    def scenario_documents_outside_the_migration_keep_their_titles(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            desired, _specs = sync.scan(root)
            titles = {
                rel: title for book in desired.values() for rel, title in book.items()
            }
            for rel, _status, expected in TITLE_UNMOVED:
                self.assertEqual(titles[rel], expected)

    def scenario_every_book_derives_one_title_per_document(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            self.assert_injective(sync.scan(root)[0])

    def scenario_a_status_change_moves_no_other_title(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            before, _specs = sync.scan(root)
            before_titles = {
                rel: title for book in before.values() for rel, title in book.items()
            }
            moved = "openxFactory/examples/memory-gateway/README.md"
            self.write(root, moved, "standard")
            after, _specs = sync.scan(root)
            after_titles = {
                rel: title for book in after.values() for rel, title in book.items()
            }
            for rel, title in before_titles.items():
                if rel == moved:
                    continue
                self.assertEqual(
                    after_titles.get(rel),
                    title,
                    f"{rel} was retitled by another document's Status: header",
                )
            self.assertEqual(
                after_titles[moved],
                "[standard] openxFactory: examples/memory-gateway/README",
                "the moved document keeps its own qualifier; only its status prefix changes",
            )

    def scenario_a_unique_readme_still_carries_its_parent_directory(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            desired, _specs = sync.scan(root)
            titles = {
                rel: title for book in desired.values() for rel, title in book.items()
            }
            for rel, title in titles.items():
                if Path(rel).stem.lower() != "readme":
                    continue
                stem = title.split(": ", 1)[1]
                self.assertGreaterEqual(
                    len(stem.split("/")), 2, f"{rel} lost its parent-directory floor"
                )
                self.assertEqual(
                    stem.split("/")[-2:],
                    legacy_stem(rel).split("/"),
                    f"{rel}'s floor is not the title the replaced rule produced",
                )

    def scenario_the_spec_and_grounding_families_are_outside_the_scope(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            self.write(root, "openxFactory/docs/ideation-dashboard.md", "standard")
            desired, _specs = sync.scan(root)
            canon = desired["canon"]
            self.assertIn("[spec] openxFactory: ideation-dashboard", canon.values())
            self.assertEqual(
                canon["openxFactory/docs/ideation-dashboard.md"],
                "[standard] openxFactory: ideation-dashboard",
                "a `[spec]` title must not qualify a `[status]` one",
            )
            for family in sync.STEM_SCOPE_EXCLUDES:
                self.assertTrue(
                    any(t.startswith(family) for t in canon.values()),
                    f"the fixture must exercise the {family} family it claims to hold outside the scope",
                )
            grounding = [
                t
                for book in desired.values()
                for t in book.values()
                if t.startswith("[grounding]")
            ]
            self.assertTrue(grounding)
            for title in grounding:
                self.assertNotIn(
                    "/",
                    title.split(": ", 1)[1],
                    "the grounding set is keyed by a fixed document list, never qualified",
                )

    def scenario_a_record_document_qualifies_nobody(self) -> None:
        rel, _status = RECORD_NAMESAKE
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            desired, _specs = sync.scan(root)
            placed = [book for book, items in desired.items() if rel in items]
            self.assertEqual(placed, [], "a record document projects nowhere")
            self.assertEqual(
                desired["canon"]["openxFactory/docs/lifecycle-notebook-projection.md"],
                "[standard] openxFactory: lifecycle-notebook-projection",
            )

    def scenario_titles_are_derived_from_structure_not_from_a_rendered_path(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            documents = self.documents(root)
            segments = {rel: segs for rel, _repo, segs in documents}
            checklist = "openxFactory/specs/005-customer-subject-runtime/checklists/requirements.md"
            self.assertEqual(
                segments[checklist],
                (
                    "openxFactory",
                    "specs",
                    "005-customer-subject-runtime",
                    "checklists",
                    "requirements",
                ),
            )
            for rel, segs in segments.items():
                self.assertIsInstance(segs, tuple, f"{rel}")
                for part in segs:
                    self.assertIsInstance(part, str, f"{rel}")
                    self.assertNotIn("/", part, f"{rel}: a segment is a path")
                    self.assertNotIn("\\", part, f"{rel}: a segment is a path")
            stems = sync.derive_stems(documents)
            self.assertEqual(
                stems[checklist].split("/"),
                ["005-customer-subject-runtime", "checklists", "requirements"],
                "the qualifier is three segments deep because two segments still collide",
            )

    def scenario_reverting_the_rule_to_a_bare_stem_reds_the_injectivity_check(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            with patch.object(sync, "derive_stems", bare_stem_derivation):
                desired, _specs = sync.scan(root)
            with self.assertRaises(AssertionError):
                self.assert_injective(desired)
            offenders = {
                book: len(items) - len(set(items.values()))
                for book, items in desired.items()
                if len(set(items.values())) != len(items)
            }
            self.assertEqual(
                sorted(offenders),
                ["drafts", "ideation-medxfactory", "ideation-opsxfactory"],
                "the fixture must reproduce the three real collisions when the rule is reverted",
            )
            self.assertEqual(
                sum(offenders.values()),
                5,
                "five documents were displaced in the live books",
            )

    def scenario_a_one_level_qualifier_leaves_the_checklists_pair_colliding(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            self.world(root)
            with patch.object(sync, "derive_stems", one_level_derivation):
                desired, _specs = sync.scan(root)
            drafts = desired["drafts"]
            self.assertNotEqual(
                len(set(drafts.values())),
                len(drafts),
                "a one-level qualifier must still collapse the checklist pair",
            )
            self.assertEqual(
                drafts[
                    "openxFactory/specs/005-customer-subject-runtime/checklists/requirements.md"
                ],
                drafts[
                    "openxFactory/specs/007-client-identity-roster/checklists/requirements.md"
                ],
            )
            desired, _specs = sync.scan(root)
            drafts = desired["drafts"]
            self.assertEqual(len(set(drafts.values())), len(drafts))
