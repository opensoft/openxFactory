from __future__ import annotations

import ast
import contextlib
import io
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tests.notebooklm._sync_test_support import REPO_ROOT, STAGED_DOC
from tests.notebooklm.typed_sync_contracts import load_typed_sync

sync = load_typed_sync()
from tests.notebooklm._root_product_test_support import root_product_world


class RootLevelGovernedProductTests(unittest.TestCase):
    def scenario_the_allowlist_matches_the_doc_health_authority(self) -> None:
        corpus_path = REPO_ROOT / "scripts" / "doc_health" / "corpus.py"
        source = corpus_path.read_text(encoding="utf-8")
        authority = None
        for node in ast.parse(source).body:
            if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name)
                and target.id == "ROOT_LEVEL_GOVERNED_PRODUCTS"
                for target in node.targets
            ):
                value = node.value
                if isinstance(value, ast.Tuple) and all(
                    isinstance(item, ast.Constant) and isinstance(item.value, str)
                    for item in value.elts
                ):
                    authority = tuple(
                        item.value
                        for item in value.elts
                        if isinstance(item, ast.Constant)
                        and isinstance(item.value, str)
                    )
                break
        self.assertIsNotNone(
            authority, f"{corpus_path} no longer declares the authority"
        )
        self.assertEqual(
            authority,
            sync.ROOT_LEVEL_GOVERNED_PRODUCTS,
            "the notebook sweep and doc-health routing disagree about which root-level repositories are governed",
        )
        self.assertEqual(
            sync.ROOT_LEVEL_GOVERNED_PRODUCTS, ("openAvatar", "openXwallet")
        )

    def scenario_a_pinned_and_present_root_product_is_found(self) -> None:
        with TemporaryDirectory() as td:
            root = root_product_world(Path(td))
            self.assertEqual(sync.pinned_root_product_paths(root), ["openXwallet"])

    def scenario_a_present_but_unpinned_root_product_is_not_found(self) -> None:
        with TemporaryDirectory() as td:
            root = root_product_world(Path(td), declare=())
            self.assertEqual(sync.pinned_root_product_paths(root), [])

    def scenario_a_pinned_but_absent_root_product_is_not_found(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            _ = (root / ".gitmodules").write_text(
                '[submodule "openXwallet"]\n\tpath = openXwallet\n\turl = https://example.invalid/openXwallet.git\n',
                encoding="utf-8",
            )
            self.assertEqual(sync.pinned_root_product_paths(root), [])

    def scenario_installs_are_never_admitted(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "installs" / "hermes-install").mkdir(parents=True)
            root = root_product_world(root, extra_pins=("installs/hermes-install",))
            found = sync.pinned_root_product_paths(root)
            self.assertEqual(found, ["openXwallet"])
            self.assertNotIn("installs/hermes-install", sync.governed_repo_paths(root))

    def scenario_no_gitmodules_admits_nothing(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "openXwallet").mkdir()
            self.assertEqual(sync.pinned_root_product_paths(root), [])

    def scenario_an_uninitialized_root_product_warns_instead_of_reading_empty(self) -> None:
        with TemporaryDirectory() as td:
            root = root_product_world(Path(td), initialize=False)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                found = sync.pinned_root_product_paths(root)
            self.assertEqual(found, ["openXwallet"])
            text = buf.getvalue()
            self.assertIn("openXwallet", text)
            self.assertIn("uninitialized submodule", text)
            self.assertIn("git submodule update --init openXwallet", text)

    def scenario_governed_repo_paths_puts_root_products_before_the_factories(self) -> None:
        with TemporaryDirectory() as td:
            root = Path(td)
            (root / "xFactories" / "codexFactory").mkdir(parents=True)
            root = root_product_world(root, extra_pins=("xFactories/codexFactory",))
            self.assertEqual(
                sync.governed_repo_paths(root),
                ["openXwallet", "xFactories/codexFactory"],
            )

    def scenario_scan_derives_the_openxwallet_ideation_book(self) -> None:
        with TemporaryDirectory() as td:
            root = root_product_world(Path(td))
            desired, specs = sync.scan(root)
        self.assertIn("ideation-openxwallet", desired)
        spec = specs["ideation-openxwallet"]
        self.assertEqual(spec.alias, "xf-ideation-openxwallet")
        self.assertEqual(spec.title, "xFactory Ideation — openXwallet")
        self.assertIn(
            "openXwallet/ideation/brainstorm/wallet-idea.md",
            desired["ideation-openxwallet"],
        )
        self.assertEqual(
            desired["ideation-openxwallet"][
                "openXwallet/ideation/brainstorm/wallet-idea.md"
            ],
            "[brainstorm] openXwallet: wallet-idea",
        )
        self.assertIn(f"openxFactory/{STAGED_DOC}", desired["ideation-openxfactory"])

    def scenario_scan_derives_the_openavatar_book_by_the_same_widening(self) -> None:
        with TemporaryDirectory() as td:
            root = root_product_world(Path(td), products=("openAvatar",))
            desired, specs = sync.scan(root)
        self.assertEqual(specs["ideation-openavatar"].alias, "xf-ideation-openavatar")
        self.assertIn(
            "openAvatar/ideation/brainstorm/wallet-idea.md",
            desired["ideation-openavatar"],
        )

    def scenario_a_root_product_with_no_ideation_document_derives_no_book(self) -> None:
        with TemporaryDirectory() as td:
            root = root_product_world(Path(td), products=())
            (root / "openXwallet" / "docs").mkdir(parents=True)
            _ = (root / "openXwallet" / "docs" / "a.md").write_text(
                "Status: ratified\n", encoding="utf-8"
            )
            _ = (root / ".gitmodules").write_text(
                '[submodule "openXwallet"]\n\tpath = openXwallet\n\turl = https://example.invalid/openXwallet.git\n',
                encoding="utf-8",
            )
            desired, specs = sync.scan(root)
        self.assertNotIn("ideation-openxwallet", desired)
        self.assertNotIn("ideation-openxwallet", specs)

    def scenario_session_repositories_keeps_its_stated_agreement_with_scan(self) -> None:
        with TemporaryDirectory() as td:
            root = root_product_world(Path(td))
            names = [name for name, _p in sync.session_repositories(root)]
        self.assertEqual(names, ["openxFactory", "openXwallet"])

    def scenario_the_workbench_sweep_sees_a_root_products_manifests(self) -> None:
        with TemporaryDirectory() as td:
            root = root_product_world(Path(td))
            (root / "openXwallet" / "ideation" / "workbench").mkdir(parents=True)
            dirs = sync.out_of_scope_workbench_dirs(root)
        self.assertIn("openXwallet", {p.parent.parent.name for p in dirs})
