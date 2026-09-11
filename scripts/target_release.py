"""The house reader and judge for the `target_release:` realization-axis
declaration (release-realization / gate-realization-axis-vocabulary).

WHY THIS MODULE EXISTS. `release-realization`'s promoted requirement
*Realization axis declaration* admits exactly two values for `target_release:`
— `implemented` (the affected repositories' main lines) or a named release
defined in the aggregation repository — and nothing reads the field. Measured
at this module's authoring: no script, test or workflow in this repository
gates the value; the only reader is the ideation dashboard's DISPLAY
(`scripts/ideation_dashboard/generator.py` `_release_frontmatter`, rendered by
`web/views/wheel.js`), which prints whatever string it finds. A vocabulary
stated in prose and checked by nobody is a vocabulary the next proposal
re-diverges from, which is what the corpus shows.

THE DECLARATION IS A VALUE TOKEN FOLLOWED BY AN OPTIONAL PROSE GLOSS, and that
is the corpus's own form rather than a rule invented here: the house writes
`target_release: implemented (the openxFactory main line). No contract bundle is
cut …`. So this module judges the TOKEN — the first whitespace-delimited word of
the declaration, with trailing `.,;:` stripped — and never the gloss. A gloss is
where an author explains; a token is where an author declares.

ABSENCE IS LAWFUL AND IS NOT A FINDING. The promoted sentence makes a proposal
without the declarations a doc-only change (`code_surface: none`,
`target_release: implemented`) BY DEFAULT, so a proposal that declares nothing
declares the default and passes. Only a PRESENT declaration is judged.

ARCHIVED PROPOSALS ARE READ AND NEVER JUDGED. An archived packet's front matter
is frozen record — `record-immutability` and `govern-archived-record-edits` put
it beyond a plain fix — so the scan counts what the archive carries and reports
it, and refuses nothing there. Judging it would demand an edit no one may make.

THE DECLARATION IS READ THROUGH THE HOUSE STRICT LOADER
(`frontmatter_strict.read_front_matter`) rather than through a private scan, so
this gate and the loader refuse the same documents and no proposal can mean one
thing to one reader and another to the next. `target_release:` is a PROSE HEADER
of the realization-axis block and not one of its STRUCTURED fields, so this
module neither realizes nor contradicts `add-sequenced-after-substrate`'s ADDED
requirement *Strict loading of the realization-axis front-matter block*: it adds
no structured field and asks for no new strictness, and it CONSUMES that
loader's refusals — a document the loader refuses is reported here as a finding
against that document rather than crashing the run.

THE GRANDFATHER REGISTER IS A RATCHET, NOT AN AMNESTY. See
`scripts/target-release-register.yaml`'s own header for the measurement that
forced it and for the asymmetry it borrows from `contracts/openspec-cli-pin.yaml`
`dispositions:`: an UNMATCHED DECLARATION FAILS and an UNMATCHED ENTRY REFUSES.

Deterministic: text/YAML reads only, no model calls, no writes, no network.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - pyyaml is a suite dependency
    yaml = None

import frontmatter_strict as fm

#: The declaration this module reads.
FIELD = "target_release"

#: The one value the promoted sentence names outright.
IMPLEMENTED = "implemented"

#: The register, beside the validator that reads it.
REGISTER_PATH = Path(__file__).resolve().parent / "target-release-register.yaml"

#: Where the estate DEFINES its releases. The promoted sentence says "a named
#: release defined in the aggregation repository"; measured 2026-09-11, the
#: aggregation repository `opensoft/xFactory` defines no releases and carries no
#: tags, while every release the corpus actually names is defined HERE, as a
#: digest inventory under `contracts/releases/` and an annotated tag of this
#: repository. A gate that resolved the phrase literally would admit nothing and
#: refuse `contract-v1.45`, so resolution is against the registry that exists.
#: The divergence between the phrase and the estate is recorded as a successor
#: rather than repaired here, because repairing it means editing the promoted
#: sentence.
RELEASE_REGISTRY_DIR = Path("contracts") / "releases"

#: A release identifier's SHAPE. Used to resolve a token against the registry,
#: and — only where no registry is present, which is every consuming tree that
#: is not this one — as the acceptance test on its own, reported as such.
RELEASE_ID_RE = re.compile(r"^contract-v\d+\.\d+$")

_TRAILING = ".,;:"

_REQUIRED_ENTRY_KEYS = ("change", "token", "class", "why", "retires_when")


class TargetReleaseError(Exception):
    """A refusal this module raises: an unreadable proposal, or a register that
    cannot be used. Carries the message naming what was refused."""


@dataclass(frozen=True)
class Finding:
    """One active declaration the vocabulary does not admit."""
    change: str
    path: str
    token: str
    detail: str


@dataclass(frozen=True)
class Report:
    """The whole-corpus result. Counts are facts about the tree, not estimates."""
    active_total: int
    active_declaring: int
    inside_implemented: int
    inside_release: int
    grandfathered: tuple[tuple[str, str], ...]
    findings: tuple[Finding, ...]
    stale: tuple[str, ...]
    archived_total: int
    archived_off_vocabulary: int
    registry_present: bool


def value_token(raw: object) -> str | None:
    """The VALUE TOKEN of a declaration, or None when it declares no value.

    The first whitespace-delimited word, with trailing `.,;:` stripped. A
    declaration present but empty (`target_release:` alone) returns None, which
    is a finding rather than an absence: the author wrote the key.
    """
    if raw is None:
        return None
    text = raw if isinstance(raw, str) else str(raw)
    for word in text.split():
        token = word.rstrip(_TRAILING)
        return token or None
    return None


def declaration(proposal: Path) -> tuple[bool, str | None]:
    """`(present, token)` for one proposal.

    Raises `TargetReleaseError` when the document cannot be read at all — a
    strict-loader refusal, or bytes that are not UTF-8. Reported by the caller
    as a finding against the file, never as a traceback.
    """
    try:
        front = fm.read_front_matter(proposal)
    except fm.StrictFrontMatterError as exc:
        raise TargetReleaseError(str(exc)) from exc
    except OSError as exc:
        raise TargetReleaseError(f"cannot be read: {exc}") from exc
    if FIELD not in front:
        return False, None
    return True, value_token(front[FIELD])


def resolves_as_release(token: str, repo_root: Path) -> tuple[bool, bool]:
    """`(resolved, registry_present)` for a token read as a named release.

    Where the release registry exists, a token counts only when the registry
    carries its digest inventory — a name that resolves to nothing is not a
    named release. Where no registry exists (a consuming tree that defines no
    releases of its own), the SHAPE is accepted and the run says so, because
    refusing every release name in a tree that cannot define one would make the
    validator unusable outside this repository.
    """
    registry = repo_root / RELEASE_REGISTRY_DIR
    present = registry.is_dir()
    if not present:
        return bool(RELEASE_ID_RE.match(token)), False
    return (registry / f"{token}.digests.yaml").is_file(), True


def load_register(path: Path = REGISTER_PATH) -> list[dict]:
    """The register entries, shape-checked.

    A register that cannot be used REFUSES rather than being ignored: ignoring
    a malformed exception file would silently re-fail every declaration it
    covers, or silently admit one it does not.
    """
    if yaml is None:  # pragma: no cover - pyyaml is a suite dependency
        raise TargetReleaseError("pyyaml is required to read the register")
    if not path.is_file():
        raise TargetReleaseError(f"the register {path} does not exist")
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise TargetReleaseError(f"the register {path} cannot be read: {exc}")
    try:
        doc = fm.strict_load(raw, what=f"the register {path.name}")
    except fm.StrictFrontMatterError as exc:
        raise TargetReleaseError(f"the register {path.name} is refused: {exc}")
    if not isinstance(doc, dict) or not isinstance(doc.get("register"), list):
        raise TargetReleaseError(
            f"the register {path.name} must carry a top-level `register:` list")
    entries: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for index, entry in enumerate(doc["register"], start=1):
        if not isinstance(entry, dict):
            raise TargetReleaseError(
                f"register entry {index} is not a mapping")
        for key in _REQUIRED_ENTRY_KEYS:
            value = entry.get(key)
            if not isinstance(value, str) or not value.strip():
                raise TargetReleaseError(
                    f"register entry {index} ({entry.get('change')!r}) is "
                    f"missing a non-empty `{key}:`")
        key = (entry["change"], entry["token"])
        if key in seen:
            raise TargetReleaseError(
                f"register entry {index} repeats {key[0]} / {key[1]!r}; one "
                "entry per declaration, so a stale entry cannot hide behind "
                "a live twin")
        seen.add(key)
        entries.append(entry)
    return entries


def _proposals(changes: Path, archived: bool) -> list[Path]:
    if not changes.is_dir():
        return []
    if archived:
        archive = changes / "archive"
        if not archive.is_dir():
            return []
        return sorted(p for p in archive.glob("*/proposal.md") if p.is_file())
    found = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        proposal = child / "proposal.md"
        if proposal.is_file():
            found.append(proposal)
    return found


def scan(repo_root: Path, register: list[dict] | None = None) -> Report:
    """Judge every ACTIVE proposal in `repo_root`; count the archive."""
    if register is None:
        register = load_register()
    changes = repo_root / "openspec" / "changes"
    covered = {(e["change"], e["token"]): e for e in register}
    matched: set[tuple[str, str]] = set()

    findings: list[Finding] = []
    grandfathered: list[tuple[str, str]] = []
    inside_implemented = inside_release = 0
    active_declaring = 0
    registry_present = (repo_root / RELEASE_REGISTRY_DIR).is_dir()

    active = _proposals(changes, archived=False)
    for proposal in active:
        change = proposal.parent.name
        rel = str(proposal.relative_to(repo_root))
        try:
            present, token = declaration(proposal)
        except TargetReleaseError as exc:
            findings.append(Finding(
                change, rel, "<unreadable>",
                f"its front matter cannot be read — {exc}"))
            continue
        if not present:
            continue  # the promoted default; declaring nothing declares it
        active_declaring += 1
        if token == IMPLEMENTED:
            inside_implemented += 1
            continue
        if token is None:
            findings.append(Finding(
                change, rel, "",
                "declares `target_release:` with no value; the vocabulary is "
                "`implemented` or a named release, and an empty declaration is "
                "neither (omit the key to take the doc-only default)"))
            continue
        resolved, _ = resolves_as_release(token, repo_root)
        if resolved:
            inside_release += 1
            continue
        key = (change, token)
        if key in covered:
            matched.add(key)
            grandfathered.append(key)
            continue
        findings.append(Finding(
            change, rel, token,
            "is outside the ratified vocabulary — `implemented` or a release "
            f"this estate defines" + (
                f" (no `{RELEASE_REGISTRY_DIR}/{token}.digests.yaml`)"
                if RELEASE_ID_RE.match(token) else "")))

    stale = tuple(
        f"{change} / {token!r}" for (change, token) in covered
        if (change, token) not in matched)

    archived_paths = _proposals(changes, archived=True)
    archived_off = 0
    for proposal in archived_paths:
        try:
            present, token = declaration(proposal)
        except TargetReleaseError:
            continue  # read, never judged
        if not present or token == IMPLEMENTED or token is None:
            continue
        resolved, _ = resolves_as_release(token, repo_root)
        if not resolved:
            archived_off += 1

    return Report(
        active_total=len(active),
        active_declaring=active_declaring,
        inside_implemented=inside_implemented,
        inside_release=inside_release,
        grandfathered=tuple(sorted(grandfathered)),
        findings=tuple(findings),
        stale=tuple(sorted(stale)),
        archived_total=len(archived_paths),
        archived_off_vocabulary=archived_off,
        registry_present=registry_present,
    )
