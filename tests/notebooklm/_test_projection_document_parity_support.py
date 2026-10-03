from __future__ import annotations

import contextlib
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from notebooklm_sync.corpus import DesiredState
from notebooklm_sync.models import BookSpec

from tests.notebooklm._sync_test_support import FakeNlm
from tests.notebooklm.typed_sync_contracts import load_typed_sync

sync = load_typed_sync()
from tests.notebooklm._projection_test_support import TitleCorpus, bare_stem_derivation


class ParityProvesDocumentsTests(unittest.TestCase):
    def _run_parity(self, root: Path, fake: FakeNlm) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), patch.object(sync, "nlm", fake):
            code = sync.parity_report(root)
        return (code, out.getvalue())

    @staticmethod
    def _books_holding(
        root: Path, desired: DesiredState, specs: dict[str, BookSpec]
    ) -> FakeNlm:
        del root
        fake = FakeNlm(
            [
                {"id": f"nb{i}", "title": specs[k].title}
                for i, k in enumerate(sorted(desired))
            ]
        )
        for i, key in enumerate(sorted(desired)):
            fake.sources[f"nb{i}"] = [
                {"id": f"s{i}-{j}", "title": title}
                for j, title in enumerate(sorted(set(desired[key].values())))
            ]
        return fake

    def scenario_a_collapsed_title_fails_parity_though_the_title_sets_are_equal(
        self,
    ) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            TitleCorpus.world(root)
            with patch.object(sync, "derive_stems", bare_stem_derivation):
                desired, specs = sync.scan(root)
                fake = self._books_holding(root, desired, specs)
                for key, items in desired.items():
                    self.assertEqual(
                        {r.get("title") for r in fake.sources_of(specs[key].title)},
                        set(items.values()),
                        "the fixture must put the live book at TITLE-set equality, which is the state the old check passed",
                    )
                code, text = self._run_parity(root, fake)
        self.assertEqual(
            code,
            1,
            "a book missing five documents is not at parity, however equal its title sets are",
        )
        self.assertIn("carry more than one document", text)
        self.assertIn("COLLAPSED", text)
        self.assertIn(
            "xFactories/MedxFactory/ideation/staging/root-truth-grounding/topic.md",
            text,
        )

    def scenario_the_injective_derivation_proves_parity_over_documents(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            TitleCorpus.world(root)
            desired, specs = sync.scan(root)
            fake = self._books_holding(root, desired, specs)
            code, text = self._run_parity(root, fake)
        self.assertEqual(code, 0, text)
        self.assertIn("parity: PROVEN", text)
        self.assertIn("documents in", text)
        self.assertNotIn("COLLAPSED", text)
