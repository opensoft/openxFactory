from __future__ import annotations

import os
import unittest
from collections.abc import Sequence
from pathlib import Path
from typing import override
from unittest.mock import patch

from notebooklm_sync.corpus import DesiredState

from tests.notebooklm.typed_sync_contracts import load_typed_sync

sync = load_typed_sync()


def bare_stem_derivation(
    documents: Sequence[tuple[str, str, tuple[str, ...]]],
) -> dict[str, str]:
    return {rel: segs[-1] for rel, _repo, segs in documents}


def one_level_derivation(
    documents: Sequence[tuple[str, str, tuple[str, ...]]],
) -> dict[str, str]:
    return {rel: "/".join(segs[-2:]) for rel, _repo, segs in documents}


class TitleCorpus(unittest.TestCase):
    @staticmethod
    def write(root: Path, rel: str, status: str) -> None:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_text(
            f"# {Path(rel).stem}\n\nStatus: {status}\n", encoding="utf-8"
        )

    @classmethod
    def world(cls, root: Path) -> None:
        (root / "openxFactory").mkdir(parents=True, exist_ok=True)
        for grounding in sync.GROUNDING:
            cls.write(root, grounding, "standard")
        for _book, rel, status, _before, _after in TITLE_MIGRATION:
            cls.write(root, rel, status)
        for rel, status, _title in TITLE_UNMOVED:
            cls.write(root, rel, status)
        cls.write(root, *RECORD_NAMESAKE)
        promoted = root / "openxFactory/openspec/specs/ideation-dashboard"
        promoted.mkdir(parents=True, exist_ok=True)
        _ = (promoted / "spec.md").write_text(
            "# Spec\n\nStatus: ratified\n", encoding="utf-8"
        )

    @staticmethod
    def documents(root: Path) -> list[tuple[str, str, tuple[str, ...]]]:
        desired, _specs = sync.scan(root)
        rels = {rel for book in desired.values() for rel in book}
        out: list[tuple[str, str, tuple[str, ...]]] = []
        for rel in sorted(rels):
            parts = Path(rel).parts
            repo = parts[1] if parts[0] == "xFactories" else parts[0]
            out.append((rel, repo, sync.title_segments(Path(rel))))
        return out

    def assert_injective(self, desired: DesiredState) -> None:
        self.assertTrue(
            desired, "a fixture that derives nothing proves injectivity vacuously"
        )
        for book, items in desired.items():
            self.assertEqual(
                len(set(items.values())),
                len(items),
                f"book {book} derives fewer titles than it has documents: the shortfall is documents the book cannot hold",
            )


class HostingIsolation(unittest.TestCase):
    @override
    def setUp(self) -> None:
        super().setUp()
        previous = dict(os.environ)
        self.addCleanup(os.environ.update, previous)
        self.addCleanup(os.environ.clear)
        _ = os.environ.pop(sync.HOSTING_ENV, None)
        real = sync.profile_account

        def only_from_a_named_home(
            profile: str, home: Path | None = None
        ) -> str | None:
            if home is not None:
                return real(profile, home=home)
            return None

        guard = patch.object(sync, "profile_account", only_from_a_named_home)
        _ = guard.start()
        self.addCleanup(guard.stop)


TITLE_MIGRATION = [
    (
        "canon",
        "openxFactory/contracts/memory-gateway/README.md",
        "standard",
        "[standard] openxFactory: memory-gateway/README",
        "[standard] openxFactory: contracts/memory-gateway/README",
    ),
    (
        "canon",
        "xFactories/LedgerxFactory/docs/company-provisioning.md",
        "ratified",
        "[ratified] LedgerxFactory: company-provisioning",
        "[ratified] LedgerxFactory: docs/company-provisioning",
    ),
    (
        "drafts",
        "openxFactory/examples/memory-gateway/README.md",
        "draft",
        "[draft] openxFactory: memory-gateway/README",
        "[draft] openxFactory: examples/memory-gateway/README",
    ),
    (
        "drafts",
        "openxFactory/specs/005-customer-subject-runtime/checklists/requirements.md",
        "draft",
        "[draft] openxFactory: requirements",
        "[draft] openxFactory: 005-customer-subject-runtime/checklists/requirements",
    ),
    (
        "drafts",
        "openxFactory/specs/007-client-identity-roster/checklists/requirements.md",
        "draft",
        "[draft] openxFactory: requirements",
        "[draft] openxFactory: 007-client-identity-roster/checklists/requirements",
    ),
    (
        "ideation-ledgerxfactory",
        "xFactories/LedgerxFactory/ideation/staging/company-provisioning/company-provisioning.md",
        "staged",
        "[staged] LedgerxFactory: company-provisioning",
        "[staged] LedgerxFactory: company-provisioning/company-provisioning",
    ),
    (
        "ideation-medxfactory",
        "xFactories/MedxFactory/ideation/staging/root-truth-grounding/topic.md",
        "staged",
        "[staged] MedxFactory: topic",
        "[staged] MedxFactory: root-truth-grounding/topic",
    ),
    (
        "ideation-medxfactory",
        "xFactories/MedxFactory/ideation/staging/root-truth-target-claims/topic.md",
        "staged",
        "[staged] MedxFactory: topic",
        "[staged] MedxFactory: root-truth-target-claims/topic",
    ),
    (
        "ideation-medxfactory",
        "xFactories/MedxFactory/ideation/staging/terminology-normalization/topic.md",
        "staged",
        "[staged] MedxFactory: topic",
        "[staged] MedxFactory: terminology-normalization/topic",
    ),
    (
        "ideation-medxfactory",
        "xFactories/MedxFactory/ideation/staging/treatment-plan-generation/topic.md",
        "staged",
        "[staged] MedxFactory: topic",
        "[staged] MedxFactory: treatment-plan-generation/topic",
    ),
    (
        "ideation-openxfactory",
        "openxFactory/ideation/brainstorm/codexfactory-domain-hermes-content.md",
        "brainstorm",
        "[brainstorm] openxFactory: codexfactory-domain-hermes-content",
        "[brainstorm] openxFactory: brainstorm/codexfactory-domain-hermes-content",
    ),
    (
        "ideation-openxfactory",
        "openxFactory/ideation/staging/codexfactory-domain-hermes-content/codexfactory-domain-hermes-content.md",
        "staged",
        "[staged] openxFactory: codexfactory-domain-hermes-content",
        "[staged] openxFactory: codexfactory-domain-hermes-content/codexfactory-domain-hermes-content",
    ),
    (
        "ideation-opsxfactory",
        "xFactories/OpsxFactory/ideation/brainstorm/exchange-execution-bringup.md",
        "staged",
        "[staged] OpsxFactory: exchange-execution-bringup",
        "[staged] OpsxFactory: brainstorm/exchange-execution-bringup",
    ),
    (
        "ideation-opsxfactory",
        "xFactories/OpsxFactory/ideation/staging/exchange-execution-bringup/exchange-execution-bringup.md",
        "staged",
        "[staged] OpsxFactory: exchange-execution-bringup",
        "[staged] OpsxFactory: exchange-execution-bringup/exchange-execution-bringup",
    ),
]

TITLE_UNMOVED = [
    (
        "xFactories/OpsxFactory/ideation/staging/opensoft-tenant-governance/topic.md",
        "staged",
        "[staged] OpsxFactory: topic",
    ),
    (
        "xFactories/OpsxFactory/ideation/README.md",
        "ratified",
        "[ratified] OpsxFactory: ideation/README",
    ),
    (
        "xFactories/OpsxFactory/README.md",
        "standard",
        "[standard] OpsxFactory: OpsxFactory/README",
    ),
    (
        "openxFactory/docs/lifecycle-notebook-projection.md",
        "standard",
        "[standard] openxFactory: lifecycle-notebook-projection",
    ),
]

RECORD_NAMESAKE = (
    "openxFactory/ideation/gate-records/lifecycle-notebook-projection.md",
    "record",
)


def legacy_stem(rel: str) -> str:
    """The derivation this change replaced, kept so the BEFORE column of
    TITLE_MIGRATION is produced rather than transcribed twice."""
    path = Path(rel)
    return (
        f"{path.parent.name}/{path.stem}"
        if path.stem.lower() == "readme"
        else path.stem
    )


def configure_hosting(root: Path, declaration_rel: str) -> None:
    """Write the workspace configuration naming `declaration_rel`."""
    config = root / sync.HOSTING_CONFIG_REL
    config.parent.mkdir(parents=True, exist_ok=True)
    _ = config.write_text(f"declaration_path: {declaration_rel}\n", encoding="utf-8")
