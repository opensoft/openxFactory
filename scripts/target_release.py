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

A REPEATED DECLARATION IS REFUSED RATHER THAN HALF-READ. `target_release:` is a
PROSE header, so the shared loader joins a repeat into one raw string instead of
refusing it as the duplicate key a STRUCTURED field's repeat would be. A block
declaring `implemented` and then `none` would tokenize as `implemented`, showing
a reviewer two declarations and authorizing the first — so `declaration` refuses
the repeat by name, on the value the loader returned, without writing a second
front-matter parser.

NOTHING AUTHOR-CONTROLLED BECOMES A PATH BEFORE IT IS SHAPE-CHECKED, and the
two places where it could are guarded at the point the value is read rather
than at the point it is used: a proposal's VALUE TOKEN must match
`RELEASE_ID_RE` before the release-registry lookup is built (`resolves_as_release`,
in EVERY branch), and a register entry's `change:` must match `CHANGE_ID_RE`
before `load_register` returns it, because every consumer resolves that name
under `openspec/changes/`. Likewise, every field the requirement has an entry
carry — including the CITATION and the CLASS — is enforced by the loader and not
only by a test over the register this repository happens to carry, so a
consuming tree gets the same refusals this one does.

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
CHANGES_DIR = Path("openspec") / "changes"

#: A release identifier's SHAPE, and THE FIRST TEST A TOKEN FACES. A token is
#: read from a proposal's front matter, which is author-controlled text, and the
#: only way it could reach the filesystem is by being interpolated into the
#: registry lookup below. So the shape is checked BEFORE any path is built, in
#: EVERY branch — with a registry and without one — and a token that does not
#: match is refused on its shape and never becomes a path component. Checking it
#: only on the no-registry branch (as this module first did) would have let
#: `../../elsewhere/thing` escape `contracts/releases/`, or let a non-release
#: word resolve because somebody planted `<word>.digests.yaml` beside the
#: inventories: either way the registry boundary is the thing that stops holding.
#:
#: THE PATTERN IS THE ESTATE'S OWN, RESTATED RATHER THAN INVENTED.
#: `contracts/releases/release-digest-inventory.schema.yaml` `$defs.bundle_tag`
#: is where this estate DEFINES the shape of a release tag, and this literal is
#: that pattern; `test_the_release_id_shape_is_the_estates_own` reads the schema
#: and asserts the two are equal, so a drift is a test failure. It is restated
#: rather than read at import because this module must judge a consuming tree
#: that carries no `contracts/` at all, and a reader that needed the schema to
#: be present would refuse such a tree for the wrong reason.
#:
#: IT ADMITS TWO AND THREE COMPONENTS (`contract-v1.45`, `contract-v1.2.3`).
#: The two-component-only form this module first carried was harmless while the
#: shape was consulted ONLY where no registry exists — and became a live
#: refusal of a release the estate's own schema admits the moment the shape
#: became the first test in EVERY branch. Measured 2026-09-11: no
#: three-component inventory is on disk today, so the defect was latent rather
#: than standing; the next one cut would have found it at the gate.
RELEASE_ID_RE = re.compile(r"^contract-v[0-9]+(?:\.[0-9]+){1,2}$")

#: Where that pattern is DEFINED, for the test that keeps the two equal.
RELEASE_ID_SCHEMA = (
    Path("contracts") / "releases" / "release-digest-inventory.schema.yaml")

#: A register entry's `change:` IS A DIRECTORY NAME AND NEVER A PATH. It is
#: resolved under `openspec/changes/` by every consumer of the register (the
#: corpus test that proves each entry names a live active change does exactly
#: that), so — same class as the token above — it is shape-checked where the
#: register is loaded rather than at each use: one segment, no separator, no
#: leading dot, so neither `..` nor `a/b` can be written into the register and
#: reach a path.
CHANGE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")

_TRAILING = ".,;:"

#: A SECOND `target_release:` HEADER INSIDE THE ONE THIS READER WAS HANDED.
#: `target_release:` is a PROSE HEADER, and the shared loader JOINS a repeated
#: prose header into one raw string rather than refusing it as the duplicate key
#: a STRUCTURED field's repeat would be — measured: a block declaring
#: `target_release: implemented` and then `target_release: none` comes back as
#: `'implemented\ntarget_release: none'`. Tokenizing that judges the FIRST
#: declaration and silently ignores the rest, which is exactly the
#: show-one-authorize-another defect the strict loader exists to close. The
#: loader's returned value has its own leading header stripped, so a match here
#: can only be a REPEAT — the check is on the value the loader returned and is
#: not a second front-matter parser.
#:
#: ANCHORED AT COLUMN 0, WHICH IS THE LOADER'S OWN NOTION OF A HEADER LINE
#: (`frontmatter_strict._TOP_LEVEL`, `^([A-Za-z_][A-Za-z0-9_-]*):`). An INDENTED
#: line is a CONTINUATION of the gloss, not a declaration, so a gloss line that
#: happened to read `  target_release: the main line` must pass — the
#: requirement says judge the token and NEVER the gloss, and a guard that
#: allowed leading whitespace would have refused exactly the prose the
#: requirement protects.
_REPEATED_HEADER_RE = re.compile(rf"(?m)^{FIELD}[ \t]*:")

#: THE REGISTER'S CLOSED BASELINE — the `(change, token)` pairs the register
#: carries at this gate's landing, and the whole of what it may ever carry.
#:
#: WHY A BASELINE AND NOT A COUNT OR AN HONOUR SYSTEM. The requirement makes the
#: register CLOSED — removable, never addable — and the register file says so in
#: its own header, but a rule stated in two prose headers and checked by nobody
#: is the defect this whole packet is about. Without this, a later pull request
#: could append an entry and make any off-vocabulary declaration pass while the
#: gate stayed green, which is the ratchet failing silently in the one direction
#: that matters. An entry the baseline does not carry is REFUSED, so admitting
#: one takes a second, deliberate, reviewable edit HERE, in the module, beside
#: the reason — which is the visible canon-shaped act the requirement asks for,
#: rather than a line appended to a data file.
#:
#: A BASELINE MAY BE A STRICT SUPERSET, AND USUALLY WILL BE: removal is lawful
#: (a corrected declaration or an archived packet retires its entry, and
#: `Report.stale` REFUSES until the entry is deleted), so a pair stays here
#: after its entry goes. This is a ceiling, never a floor.
#:
#: IT BINDS THE HOUSE REGISTER ONLY. `--register PATH` exists so the tests can
#: put a known register in front of a known tree and so a consuming tree can
#: name its own; those registers are not this one and are not measured by this
#: baseline. `load_register` applies it when, and only when, it is reading the
#: register this repository carries, and a caller may pass its own.
CLOSED_REGISTER = (
    ("add-chain-attestation", "THE"),
    ("add-clearing-dispatch-boundary", "THE"),
    ("add-consent-custody-rederivation-record", "THE"),
    ("add-credential-escrow-checkout", "THE"),
    ("add-requirement-ref-resolution-integrity", "THE"),
    ("add-identity-brokering", "next"),
    ("add-standing-policy-compliance-contract", "next"),
    ("add-trust-anchor", "next"),
    ("add-worker-enrollment-broker", "next"),
    ("adopt-medxsoft-repository-identity", "next"),
    ("admit-deliberation-clearing-operation", "the"),
    ("declare-client-standing-policy-contract", "contract-v<next"),
    ("add-nightly-dashboard-refresh", "implementation_pending"),
    ("add-roster-directory-admission-surface", "implementation_pending"),
    ("qualify-avatar-live-voice", "implementation_pending"),
    ("split-opendox-two-layer-product", "implementation_pending"),
    ("implement-keycloak-install-repo", "repository-bootstrap"),
    ("implement-openxpki-install-repo", "repository-bootstrap"),
    ("admit-review-lane-repin-to-merge-approval-envelope", "a"),
    ("amend-mirror-floor-regeneration-merge-authority", "a"),
    ("extend-merge-master-envelope-to-floor-bot-lanes", "a"),
)

#: EVERY KEY A REGISTER ENTRY SHALL CARRY, AND THE SHAPE IT SHALL CARRY IT IN.
#: The ADDED requirement *Realization axis vocabulary is gated* has each standing
#: entry name "the value token as it stands, the class of divergence, the reason,
#: a citation, and the event that retires the entry" — five things — so all five
#: are enforced here, at the load, and not merely asserted by a test over the
#: register this repository happens to carry. `cited_to` is the one that is a
#: LIST: a divergence can stand on more than one written reason, and an entry
#: with no citation would grandfather an off-vocabulary declaration on nobody's
#: word, which is the failure the register exists to prevent.
_REQUIRED_ENTRY_KEYS = {
    "change": "text",
    "token": "text",
    "class": "text",
    "why": "text",
    "cited_to": "list",
    "retires_when": "text",
}

#: THE CLOSED CLASS SET. The requirement makes the register CLOSED and puts a
#: new admission in the SPECIFICATION rather than in this file, so the classes a
#: divergence may be filed under are enumerated here — beside the loader that
#: enforces them — rather than only in a test over the live register. Same class
#: of defect as the citation: a constraint the requirement states, checked by one
#: corpus test and by no loader, is a constraint a consuming tree does not have.
REGISTER_CLASSES = (
    "deferred-allocation",
    "realization-state",
    "non-bundle-target",
    "answers-another-question",
)


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
    raw = front[FIELD]
    text = raw if isinstance(raw, str) else str(raw)
    if _REPEATED_HEADER_RE.search(text):
        raise TargetReleaseError(
            f"declares `{FIELD}:` more than once in one front-matter block. "
            "The block is prose headers, so the shared loader JOINS the "
            "repeats into one value instead of refusing them as the duplicate "
            "key a structured field's repeat would be, and a reader that "
            "tokenized the join would judge the FIRST declaration and silently "
            "ignore the rest. Declare it once")
    return True, value_token(raw)


def _registry_present(repo_root: Path) -> bool:
    """Whether `contracts/releases/` exists as a REAL, UNESCAPED path under
    `repo_root` — no symlink ANYWHERE between `repo_root` and the registry
    directory itself, not only at the registry directory's own name.

    `Path.is_dir()` FOLLOWS SYMLINKS, so a committed `contracts/releases`
    DIRECTORY SYMLINK — including one pointing outside this tree — would
    otherwise be treated as an estate-defined registry, and every file
    reached through it would resolve as though this repository defined it.
    The candidate-file guard (`is_file() and not is_symlink()`) does not
    catch this on its own: a REGULAR file reached through a symlinked
    parent directory is not itself a symlink.

    CHECKING ONLY THE LEAF DIRECTORY'S OWN symlink-ness (`releases.is_symlink()`,
    this function's first cut) closes the escape at that ONE component, but an
    ANCESTOR being the symlink — `contracts/` itself, say, pointing outside
    this tree — reaches the identical escape through a LEAF that is a
    perfectly ordinary, unsymlinked directory: `contracts/releases` is then a
    regular path, and so is whatever candidate file sits inside it, because
    ordinariness is a property of the ONE PATH COMPONENT checked and says
    nothing about what carried a reader there. So the test is not "is the leaf
    a symlink" but "does resolving every symlink between here and `repo_root`
    land you back where a symlink-free tree would have put you": the
    registry's fully resolved real path must equal `repo_root`'s own resolved
    real path with the literal `contracts/releases` suffix appended, with no
    substitution anywhere in between. This subsumes the leaf-only check
    (a symlinked `releases` itself also fails the equality) rather than
    sitting beside it as a second guard.

    Every caller that needs to know whether the registry is present uses THIS
    function — never a bare `.is_dir()` and never only `.is_symlink()` on the
    leaf — so `Report.registry_present` can never say something
    `resolves_as_release` did not itself act on.
    """
    registry = repo_root / RELEASE_REGISTRY_DIR
    if not registry.is_dir():
        return False
    try:
        resolved_registry = registry.resolve(strict=True)
        resolved_root = repo_root.resolve(strict=True)
    except OSError:
        return False
    return resolved_registry == resolved_root / RELEASE_REGISTRY_DIR


def resolves_as_release(token: str, repo_root: Path) -> tuple[bool, bool]:
    """`(resolved, registry_present)` for a token read as a named release.

    THE SHAPE IS CHECKED FIRST, IN BOTH BRANCHES, AND BEFORE ANY PATH EXISTS.
    The token comes out of author-controlled front matter; a token that is not
    a release identifier is refused on that alone and is never interpolated into
    a lookup, so `../…` cannot climb out of `contracts/releases/` and a planted
    `<anything>.digests.yaml` cannot make a non-release word resolve.

    Then, where the release registry exists, a token counts only when the
    registry carries its digest inventory — a name that resolves to nothing is
    not a named release. Where no registry exists (a consuming tree that defines
    no releases of its own), the shape is the whole test and the run says so,
    because refusing every release name in a tree that cannot define one would
    make the validator unusable outside this repository.

    NO PATH FROM `repo_root` TO THE CANDIDATE INVENTORY MAY CROSS A SYMLINK —
    not the registry directory, not an ANCESTOR of it, and not the candidate
    file itself. `Path.is_file()` and `Path.is_dir()` both follow symlinks, so
    a committed `contract-vX.Y.digests.yaml` symlink, a committed
    `contracts/releases` DIRECTORY symlink, OR a committed `contracts/`
    symlink one level further up — any of them, including one pointing
    outside this tree — would otherwise be treated as an estate-defined
    release: checking only the leaf directory closes the escape at that ONE
    component while leaving every ancestor open, because a file reached
    through ANY symlinked ancestor is a perfectly ordinary, unsymlinked leaf
    itself. `_registry_present` therefore does not ask "is the registry
    directory a symlink" but "does resolving every symlink between here and
    `repo_root` land you back where a symlink-free tree would have put you",
    which closes the escape at every component in one test rather than one
    component at a time as each is found. This module's sibling
    `scripts/hermes_runtime_validation/release.py` already excludes symlinked
    inventories for exactly this reason (`RepoSource.exists`,
    `list_release_inventories`); the same guard is RESTATED here rather than
    imported, because this module must judge a tree that carries no
    `scripts/hermes_runtime_validation/` at all — and it is restated more
    broadly than that sibling's, because the sibling module's tree never
    faced a symlinked ANCESTOR directory holding a genuine leaf.
    """
    registry = repo_root / RELEASE_REGISTRY_DIR
    present = _registry_present(repo_root)
    if not RELEASE_ID_RE.match(token):
        return False, present
    if not present:
        return True, False
    candidate = registry / f"{token}.digests.yaml"
    return candidate.is_file() and not candidate.is_symlink(), True


def _has_symlinked_ancestor(path: Path) -> bool:
    """Whether any directory between `path` and its own top is a symlink.

    `path.is_symlink()` answers only for the LEAF. `linkdir/register.yaml`,
    where `linkdir` is a symlink to an external directory, has an entirely
    ORDINARY leaf — `register.yaml` itself is a regular file — so the leaf
    check alone passes it, and `read_text()` still follows `linkdir` and
    reads bytes from wherever it points, silently and differently per
    runner. This is the same escape `_registry_present` and `_unescaped`
    close for the release registry and the proposal walk, generalized here
    WITHOUT a `repo_root` to anchor it: a register named on `--register` is
    deliberately allowed to live anywhere a test tree or a consuming
    repository puts it (`load_register`'s own docstring), so there is no
    boundary to check "outside of" the way `_unescaped` checks outside
    `repo_root`. The walk therefore climbs `path`'s OWN ancestors one
    directory at a time — stopping at `/` for an absolute path, or at `.`
    for a relative one, so a caller's working directory is no more
    implicated than `_unescaped` implicates `repo_root`'s own approach to
    it — rather than checking only the one directory immediately holding
    the leaf.
    """
    current = path.parent
    while True:
        if current.is_symlink():
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def load_register(path: Path = REGISTER_PATH,
                  closed: tuple[tuple[str, str], ...] | None = None
                  ) -> list[dict]:
    """The register entries, shape-checked, and measured against the CLOSED
    baseline where one applies.

    A register that cannot be used REFUSES rather than being ignored: ignoring
    a malformed exception file would silently re-fail every declaration it
    covers, or silently admit one it does not.

    `closed` is the baseline of `(change, token)` pairs the register may carry.
    Passing it binds ANY register; passing None binds the HOUSE register — the
    one beside this module — to `CLOSED_REGISTER` and leaves a register named
    on the command line unbaselined, because such a register belongs to a test
    tree or a consuming repository and its closure is that repository's own
    record to keep.

    THE SAME ESCAPE `_registry_present` AND `_unescaped` CLOSE, NAMED HERE FOR
    THE REGISTER ITSELF — AT EVERY PATH COMPONENT, NOT ONLY THE LEAF.
    `Path.is_file()` and `Path.read_text()` both follow symlinks, so a
    committed symlink AT the register path — the default beside this module,
    or one a caller names on the command line for a test tree or a consuming
    repository — would make the gate consume bytes outside the checkout,
    silently and differently per runner, unlike the symlink-boundary
    protections this module already applies to the release registry and the
    proposal walk. Checking only `path.is_symlink()` closes that at the LEAF
    but leaves an ANCESTOR open: `linkdir/register.yaml`, where `linkdir`
    is a symlink to an external directory, has an entirely ordinary leaf, so
    a leaf-only guard passes it and `read_text()` still follows `linkdir`.
    `_has_symlinked_ancestor` closes the ancestor walk; both checks run on
    `path` UNCONDITIONALLY, before `is_file()` or `read_text()` runs, so it
    is the same guard whether `path` is the default argument or one a
    caller supplies — no branch here treats the two differently, so no
    branch can forget one of them.
    """
    if yaml is None:  # pragma: no cover - pyyaml is a suite dependency
        raise TargetReleaseError("pyyaml is required to read the register")
    if path.is_symlink() or _has_symlinked_ancestor(path):
        raise TargetReleaseError(
            f"the register {path} is reached through a symlink, refused "
            "unread rather than followed: a committed symlink here — at "
            "the register's own name, or at any directory between it and "
            "the top — would let the gate consume bytes from outside the "
            "checkout and vary by runner. Replace it with a regular file "
            "at an ordinary, unsymlinked path")
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
    if closed is None and path.resolve() == REGISTER_PATH.resolve():
        closed = CLOSED_REGISTER
    entries: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for index, entry in enumerate(doc["register"], start=1):
        if not isinstance(entry, dict):
            raise TargetReleaseError(
                f"register entry {index} is not a mapping")
        for field, shape in _REQUIRED_ENTRY_KEYS.items():
            value = entry.get(field)
            if shape == "text":
                if not isinstance(value, str) or not value.strip():
                    raise TargetReleaseError(
                        f"register entry {index} ({entry.get('change')!r}) is "
                        f"missing a non-empty `{field}:`")
                continue
            if not isinstance(value, list) or not value:
                raise TargetReleaseError(
                    f"register entry {index} ({entry.get('change')!r}) is "
                    f"missing a non-empty `{field}:` list; the requirement has "
                    f"every standing entry carry a citation, and an entry "
                    f"without one grandfathers an off-vocabulary declaration "
                    f"on nobody's word")
            for position, item in enumerate(value, start=1):
                if not isinstance(item, str) or not item.strip():
                    raise TargetReleaseError(
                        f"register entry {index} ({entry.get('change')!r}) "
                        f"carries a `{field}:` item ({position}) that is not "
                        f"non-empty text")
        if not CHANGE_ID_RE.match(entry["change"]):
            raise TargetReleaseError(
                f"register entry {index} names `change: {entry['change']}`, "
                "which is not a change-directory name — one segment, no "
                "separator and no leading dot; the name is resolved under "
                "openspec/changes/, so a path written here would reach one")
        if entry["class"] not in REGISTER_CLASSES:
            raise TargetReleaseError(
                f"register entry {index} ({entry['change']}) declares "
                f"`class: {entry['class']}`, which is not one of "
                f"{', '.join(REGISTER_CLASSES)}; the register is CLOSED and a "
                "new class is a change to the specification, not a register "
                "edit")
        key = (entry["change"], entry["token"])
        if key in seen:
            raise TargetReleaseError(
                f"register entry {index} repeats {key[0]} / {key[1]!r}; one "
                "entry per declaration, so a stale entry cannot hide behind "
                "a live twin")
        if closed is not None and key not in closed:
            raise TargetReleaseError(
                f"register entry {index} names {key[0]} / {key[1]!r}, which "
                "the CLOSED baseline does not carry. The register is "
                "REMOVABLE, NEVER ADDABLE: an entry appended here would make "
                "an off-vocabulary declaration pass with the gate green and "
                "the ratchet would have failed in the one direction that "
                "matters. If the exception is genuinely owed, add the pair to "
                "`CLOSED_REGISTER` in the same pull request, where the diff "
                "shows the act for what it is")
        seen.add(key)
        entries.append(entry)
    return entries


def _unescaped(repo_root: Path, relative: Path) -> Path | None:
    """`repo_root / relative`, but ONLY when it is a REAL, UNESCAPED path under
    `repo_root` — no symlink ANYWHERE between the two, not only at the leaf —
    and `None` otherwise.

    THIS IS `_registry_present`'S TEST, GENERALIZED TO ANY PATH THIS MODULE
    OPENS, AND IT IS HERE FOR THE SAME REASON. `Path.is_file()` FOLLOWS
    SYMLINKS, so a committed `openspec/changes/<id>/proposal.md` symlink — or an
    ordinary `proposal.md` inside a symlinked CHANGE DIRECTORY, or under a
    symlinked `openspec/` — would otherwise be read as an active proposal of the
    scanned tree, and `declaration()` would judge bytes that live outside it. A
    dangling link is the same defect wearing the other face: the proposal
    vanishes from the scan and the tree is judged on a corpus it does not have.
    Neither is a judgment about the scanned tree, which is the only thing this
    gate is entitled to make.

    The leaf's own `is_symlink()` does not settle it: a REGULAR file reached
    through a symlinked parent is not itself a symlink, and ordinariness is a
    property of the ONE component checked. So the test is the same one the
    registry uses — resolve everything, and require that you land where a
    symlink-free tree would have put you — which closes the escape at every
    component in one comparison rather than one component at a time as each is
    found. `repo_root` is resolved on BOTH sides, so a `repo_root` that is
    ITSELF reached through a symlink (a scratch tree under a symlinked
    `/tmp`, say) is not mistaken for the escape.
    """
    candidate = repo_root / relative
    try:
        resolved = candidate.resolve(strict=True)
        resolved_root = repo_root.resolve(strict=True)
    except OSError:
        return None
    if resolved != resolved_root / relative:
        return None
    return candidate


def _proposals(repo_root: Path, archived: bool) -> list[Path]:
    """Every `proposal.md` the scanned tree really carries, active or archived.

    EVERY PATH IS TAKEN THROUGH `_unescaped`, never through a bare `is_file()`:
    the discovery walk is exactly as much of an escape surface as the release
    registry was (D8g, D8i), and a proposal read from outside `repo_root` would
    be judged, counted and named in a finding as though it belonged to the tree.
    """
    changes = _unescaped(repo_root, CHANGES_DIR)
    if changes is None or not changes.is_dir():
        return []
    if archived:
        archive_rel = CHANGES_DIR / "archive"
        archive = _unescaped(repo_root, archive_rel)
        if archive is None or not archive.is_dir():
            return []
        found = []
        for child in sorted(archive.iterdir()):
            if not child.is_dir():
                continue
            proposal = _unescaped(
                repo_root, archive_rel / child.name / "proposal.md")
            if proposal is not None and proposal.is_file():
                found.append(proposal)
        return found
    found = []
    for child in sorted(changes.iterdir()):
        if not child.is_dir() or child.name == "archive":
            continue
        proposal = _unescaped(repo_root, CHANGES_DIR / child.name / "proposal.md")
        if proposal is not None and proposal.is_file():
            found.append(proposal)
    return found


def scan(repo_root: Path, register: list[dict] | None = None) -> Report:
    """Judge every ACTIVE proposal in `repo_root`; count the archive."""
    if register is None:
        register = load_register()
    covered = {(e["change"], e["token"]): e for e in register}
    matched: set[tuple[str, str]] = set()

    findings: list[Finding] = []
    grandfathered: list[tuple[str, str]] = []
    inside_implemented = inside_release = 0
    active_declaring = 0
    registry_present = _registry_present(repo_root)

    active = _proposals(repo_root, archived=False)
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

    archived_paths = _proposals(repo_root, archived=True)
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
