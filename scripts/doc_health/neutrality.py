"""Neutrality-drift stage-1 pre-filter (add-neutrality-drift-lane; change
task 1.1).

Realizes the deterministic half of the doc-health delta "Neutrality drift is
scouted nightly" (design D2, "Two-stage detection"): pure-code candidate
signals over each pinned `xFactories/*` domain repo, no model calls, cheap
every night. The model scout (`neutrality_dispatch.py`) judges only this
pre-filter's survivors plus content changed since the lane's last recorded
run. Four signals, each transcribing one clause of the delta:

1. **near_duplicate** — the file's content is a near-duplicate of a file in
   the openxFactory tree. This GENERALIZES the `contract-copy-drift` family's
   copy-vs-canonical question (families.fam_contract_copy_drift asks it at
   pin identity; this signal asks it at content identity) using token-set
   Jaccard similarity with a documented threshold
   (`NEAR_DUPLICATE_SIMILARITY`).
2. **lexicon_absence** — a schema (`*.schema.yaml|json`) or script
   (`*.py|sh`) with ZERO case-insensitive hits of the domain's own lexicon.
   The lexicon derives from the repo's own identity: repo-name stems
   (medx/ledgerx/opsx/adx/codex), the `stack.yaml` domain block, and the
   repo's domain ontology (`hermes/**/ontology/concepts.yaml`, the
   MedxFactory/codexFactory declaration shape). When no ontology resolves,
   the lexicon falls back to name stems and the signal note SAYS SO.
3. **cross_repo_consumer** — another pinned repo's tracked text references
   the file's path (the DTN-019 pattern: the consumer already lives
   elsewhere).
4. **uninventoried_tooling** — a `scripts/` tree file absent from the repo's
   `stack.yaml` required-artifact surface (the DTN-018/023 pattern: tooling
   mass the domain never declared as domain inventory).

FROZEN RECORDS ARE EXCLUDED SUBJECTS structurally, not just by prompt rule
(delta scenario "A neutral-shaped artifact appears in a domain repo" judges
live content): `openspec/changes/archive/`, `specs/` (Speckit evidence),
`council/` records, and `ideation/brainstorm/` never become candidates.
Paths already cited by the DTN candidate register are skipped too — an open
register entry (e.g. DTN-023's `scripts/review_lane/`) is already in the
promotion queue and re-filing it would be noise.

INCREMENTAL STATE (design D6) lives in the lane's own files under the
openxFactory checkout, following the `catalog_baseline` convention of a
dedicated `health/<lane>/` tree: `health/neutrality-drift/state.yaml`
records, per repo, the last-run commit and the content digests of everything
the scout has already judged; `health/neutrality-drift/baseline/<repo>.yaml`
is the recorded, immutable baseline marker type (task 1.6 records the
2026-08-03 manual codexFactory sweep as that repo's marker). Selection for
stage 2 takes only survivors whose content is new or changed against that
state, bounded by the dispatch batch; the remainder carries over simply by
staying unjudged.

This module never invokes a model, never writes outside the two state
surfaces above (and only through its explicit `record_state` /
`record_baseline` writers), and never constructs a doc-health `Finding` —
stage-1 candidates are dispatch input, not findings (design D4).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import zlib
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

# The lane id: the report/ranked-plan family string, the dispositions-file
# `family:` key (the EXISTING health/dispositions.yaml vocabulary, extended
# with a `content_sha256` field for this lane — never a parallel file), and
# the runner's uncited-resolution exclusion key.
LANE_ID = "neutrality-drift"

# State home (the catalog_baseline convention of one dedicated
# health/<lane>/ tree, homed in the openxFactory checkout like the
# derive-possibles lane's evidence dir — openxFactory owns the lane, its
# state, and its recorded baselines).
STATE_DIR = Path("health") / "neutrality-drift"
STATE_NAME = "state.yaml"
BASELINE_SUBDIR = "baseline"
SEEDS_SUBDIR = "seeds"

STATE_KIND = "xfactory_neutrality_drift_state"
# The recorded baseline marker type (task 1.1/1.6): an immutable record that
# a full neutrality sweep covered one repo up to `commit`, so the lane's
# first incremental run there reviews only later changes.
BASELINE_KIND = "xfactory_neutrality_baseline"
SCHEMA_VERSION = 1

# --- near-duplicate similarity (signal 1) ------------------------------------
#
# Token-set Jaccard similarity threshold. Chosen at 0.85 so a copied artifact
# with light local edits — the class every 2026-08-03 sweep hit belonged to
# (renamed identifiers, a tweaked header, a domain noun swapped in a comment)
# — still trips, while genuinely reworked material sharing only vocabulary
# does not. Token SETS (not sequences) make the measure order-insensitive
# and cheap; the sketch prefilter below keeps the nightly cost linear-ish.
NEAR_DUPLICATE_SIMILARITY = 0.85
# Files below this many distinct tokens produce noisy Jaccard scores (two
# tiny boilerplate stubs look "similar"); they are compared only by exact
# basename match.
MIN_COMPARE_TOKENS = 40
# Cheap MinHash-style sketch: the K smallest CRC32 token hashes. Two files
# whose sketches overlap in fewer than SKETCH_MIN_OVERLAP positions cannot
# plausibly reach the Jaccard threshold, so the expensive full comparison is
# skipped (deterministic — CRC32, never the seeded builtin hash).
SKETCH_K = 16
SKETCH_MIN_OVERLAP = 6

MAX_FILE_BYTES = 400_000

TEXT_SUFFIXES = frozenset({".md", ".yaml", ".yml", ".json", ".py", ".sh",
                           ".txt"})
SCHEMA_SUFFIXES = (".schema.yaml", ".schema.json")
SCRIPT_SUFFIXES = (".py", ".sh")

EXCLUDED_PARTS = frozenset({".git", "node_modules", "__pycache__", ".venv",
                            "installs"})
# Frozen records are excluded subjects (spec refusal rule, enforced
# structurally here as well as in the prompt contract).
FROZEN_PREFIXES = ("openspec/changes/archive/", "specs/",
                   "ideation/brainstorm/", "council/")

SIGNAL_NAMES = ("near_duplicate", "lexicon_absence", "cross_repo_consumer",
                "uninventoried_tooling")

_TOKEN_RE = re.compile(r"[a-z0-9_]+")
_PATH_TOKEN_RE = re.compile(r"[\w.-]+(?:/[\w.-]+)+")


@dataclass(frozen=True)
class Signal:
    name: str  # one of SIGNAL_NAMES
    note: str  # human-readable evidence for the report/prompt payload


@dataclass(frozen=True)
class Candidate:
    """One stage-1 survivor: a domain-repo file at least one signal
    selected, identified by content digest so state/disposition suppression
    keys on (repo, path, sha256)."""
    repo: str
    path: str            # repo-relative POSIX path
    content_sha256: str
    signals: tuple       # tuple[Signal, ...]

    def sort_key(self):
        return (self.repo, self.path)


@dataclass(frozen=True)
class Lexicon:
    stems: tuple        # substring-matched (case-insensitive)
    terms: tuple        # word-boundary-matched phrases (case-insensitive)
    source_note: str    # provenance surfaced in every lexicon_absence note


@dataclass
class ScanResult:
    repo: str
    candidates: list = field(default_factory=list)   # [Candidate]
    signal_counts: dict = field(default_factory=dict)
    lexicon_note: str = ""
    register_cited_skipped: int = 0
    scanned_files: int = 0


# --- file walking --------------------------------------------------------------

def _frozen(rel_posix: str) -> bool:
    return rel_posix.startswith(FROZEN_PREFIXES)


def _excluded_parts(rel: Path) -> bool:
    """VCS/vendor parts plus ANY dot-tree part: dot-directory scaffolding
    (`.claude/`, `.agents/`, `.specify/`, `.github/`, `.codex/` agent-harness
    and CI plumbing replicated into every repo by workspace bootstrap) is
    workspace plumbing, not factory content — excluded as subjects AND as
    comparison sources, or every repo's skill/harness copies would flood the
    near-duplicate signal with non-promotable noise (proven on the first
    stage-1 dry run, 2026-08-04)."""
    return any(part in EXCLUDED_PARTS or part.startswith(".")
               for part in rel.parts)


def iter_text_files(repo_path: Path, *, include_frozen: bool = False):
    """Yield (rel_posix, absolute_path) for every eligible text file, in
    sorted order. Excludes VCS/vendor/dot-tree parts, frozen-record
    prefixes (unless asked), non-text suffixes, and oversized files."""
    repo_path = Path(repo_path)
    out = []
    for abs_path in repo_path.rglob("*"):
        if not abs_path.is_file():
            continue
        rel = abs_path.relative_to(repo_path)
        if _excluded_parts(rel):
            continue
        if abs_path.suffix not in TEXT_SUFFIXES:
            continue
        rel_posix = rel.as_posix()
        if not include_frozen and _frozen(rel_posix):
            continue
        try:
            if abs_path.stat().st_size > MAX_FILE_BYTES:
                continue
        except OSError:
            continue
        out.append((rel_posix, abs_path))
    return sorted(out)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256_bytes(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --- domain lexicon (signal 2) ---------------------------------------------------

_GENERIC_IDENTITY_TOKENS = frozenset({"factory", "xfactory", "the", "and"})


def _identity_tokens(*values) -> list[str]:
    tokens = []
    for value in values:
        if not isinstance(value, str):
            continue
        for token in re.split(r"[^A-Za-z0-9]+", value):
            token = token.casefold()
            if len(token) >= 3 and token not in _GENERIC_IDENTITY_TOKENS:
                tokens.append(token)
    return tokens


def _ontology_file(repo_path: Path) -> Path | None:
    """The repo's domain ontology concept registry, if it declares one the
    way MedxFactory/codexFactory do (`hermes/domain/ontology/concepts.yaml`);
    `docs/**/ontology/concepts.yaml` is accepted as an alternate home."""
    for root in ("hermes", "docs"):
        base = repo_path / root
        if not base.is_dir():
            continue
        found = sorted(base.glob("**/ontology/concepts.yaml"))
        if found:
            return found[0]
    return None


def _ontology_terms(path: Path) -> list[str]:
    if yaml is None:  # pragma: no cover - pyyaml is a suite requirement
        return []
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return []
    terms: list[str] = []
    if isinstance(loaded, dict):
        for concept in loaded.get("concepts") or []:
            if not isinstance(concept, dict):
                continue
            label = concept.get("label")
            if isinstance(label, str) and label.strip():
                terms.append(" ".join(label.split()).casefold())
            cid = concept.get("id")
            if isinstance(cid, str) and "/" in cid:
                tail = cid.rsplit("/", 1)[1].replace("_", " ").strip()
                if tail:
                    terms.append(tail.casefold())
    return terms


def derive_lexicon(repo_name: str, repo_path: Path) -> Lexicon:
    """Derive the domain's lexicon from the repo's OWN identity (task 1.1):
    repo-name stems, the stack.yaml domain block, and the domain ontology
    concept registry when one resolves. With no resolvable ontology the
    lexicon falls back to name stems and the source note says so — every
    lexicon_absence signal carries that note, so a weak lexicon is never a
    silent one."""
    repo_path = Path(repo_path)
    stems = {repo_name.casefold()}
    lowered = repo_name.casefold()
    if lowered.endswith("factory") and len(lowered) > len("factory"):
        stems.add(lowered[: -len("factory")])

    stack_tokens: list[str] = []
    stack_path = repo_path / "stack.yaml"
    if yaml is not None and stack_path.is_file():
        try:
            stack = yaml.safe_load(stack_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            stack = None
        domain = (stack or {}).get("domain") \
            if isinstance(stack, dict) else None
        if isinstance(domain, dict):
            stack_tokens = _identity_tokens(
                domain.get("id"), domain.get("product_name"),
                domain.get("display_name"), domain.get("category"))
    stems.update(stack_tokens)

    ontology = _ontology_file(repo_path)
    terms = _ontology_terms(ontology) if ontology is not None else []
    if terms:
        source_note = (f"name stems + stack.yaml identity + ontology "
                       f"{ontology.relative_to(repo_path).as_posix()} "
                       f"({len(terms)} terms)")
    else:
        source_note = ("name stems only (no domain ontology resolvable "
                       "under hermes/ or docs/)")
    return Lexicon(stems=tuple(sorted(stems)),
                   terms=tuple(sorted(set(terms))),
                   source_note=source_note)


def zero_lexicon_hits(text: str, lexicon: Lexicon) -> bool:
    """True when the text contains NO case-insensitive hit of any lexicon
    stem (substring — `codex` must hit `codexFactory`/`codex-tenant`) or
    ontology term (word-boundary phrase — `care plan` must not fire inside
    an unrelated identifier)."""
    lowered = text.casefold()
    for stem in lexicon.stems:
        if stem in lowered:
            return False
    for term in lexicon.terms:
        pattern = r"\b" + re.escape(term).replace(r"\ ", r"\s+") + r"\b"
        if re.search(pattern, lowered):
            return False
    return True


# --- openxFactory near-duplicate index (signal 1) --------------------------------

def _tokens(text: str) -> frozenset:
    return frozenset(_TOKEN_RE.findall(text.casefold()))


def _sketch(tokens: frozenset) -> frozenset:
    return frozenset(sorted(zlib.crc32(t.encode()) for t in tokens)
                     [:SKETCH_K])


@dataclass
class NeutralIndex:
    """The openxFactory comparison tree: per-file token sets plus an
    inverted sketch index so a night's scan stays cheap."""
    entries: list = field(default_factory=list)  # (path, name, tokens)
    by_name: dict = field(default_factory=dict)  # basename -> [entry idx]
    by_hash: dict = field(default_factory=dict)  # sketch hash -> [entry idx]


def build_neutral_index(openx_path: Path) -> NeutralIndex:
    index = NeutralIndex()
    for rel_posix, abs_path in iter_text_files(openx_path):
        tokens = _tokens(_read(abs_path))
        if len(tokens) < MIN_COMPARE_TOKENS:
            continue
        idx = len(index.entries)
        index.entries.append((rel_posix, Path(rel_posix).name, tokens))
        index.by_name.setdefault(Path(rel_posix).name, []).append(idx)
        for h in _sketch(tokens):
            index.by_hash.setdefault(h, []).append(idx)
    return index


def _jaccard(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def near_duplicate(name: str, tokens: frozenset,
                   index: NeutralIndex) -> tuple[str, float] | None:
    """The best openxFactory near-duplicate of one domain file, or None
    below the threshold. Same-basename entries are always compared; other
    entries only when the sketch prefilter says the full comparison could
    plausibly reach the threshold."""
    if len(tokens) < MIN_COMPARE_TOKENS:
        return None
    candidates: dict[int, int] = {}
    for h in _sketch(tokens):
        for idx in index.by_hash.get(h, ()):
            candidates[idx] = candidates.get(idx, 0) + 1
    compare = {idx for idx, overlap in candidates.items()
               if overlap >= SKETCH_MIN_OVERLAP}
    compare.update(index.by_name.get(name, ()))
    best: tuple[str, float] | None = None
    for idx in sorted(compare):
        path, _, entry_tokens = index.entries[idx]
        sim = _jaccard(tokens, entry_tokens)
        if sim >= NEAR_DUPLICATE_SIMILARITY and \
                (best is None or sim > best[1]):
            best = (path, sim)
    return best


# --- cross-repo consumer references (signal 3) ------------------------------------

@dataclass(frozen=True)
class RepoReferences:
    """One repo's outward evidence for the consumer signal: the path-like
    tokens its tracked text mentions, plus its OWN tracked file set (so a
    bare relative reference to a path the referencing repo itself carries —
    every repo mentions its own `omnigent/domain-overlay.yaml` — is never
    mistaken for a cross-repo consumer; proven noisy on the first stage-1
    dry run, 2026-08-04)."""
    refs: frozenset
    files: frozenset


def collect_path_references(repo_paths: dict) -> dict:
    """Per repo, a `RepoReferences` — computed in ONE pass per repo so
    consumer lookup is set membership. Frozen-record prefixes are excluded
    from the reference scan: a reference in an archived change is
    historical, not a live consumer."""
    refs: dict[str, RepoReferences] = {}
    for name, path in sorted(repo_paths.items()):
        path = Path(path)
        tokens: set[str] = set()
        for _rel, abs_path in iter_text_files(path):
            tokens.update(_PATH_TOKEN_RE.findall(_read(abs_path)))
        files = {p.relative_to(path).as_posix() for p in path.rglob("*")
                 if p.is_file()
                 and not _excluded_parts(p.relative_to(path))}
        refs[name] = RepoReferences(frozenset(tokens), frozenset(files))
    return refs


OPENX_REPO = "openxFactory"


def consumers_of(repo: str, rel_posix: str, refs: dict) -> list[str]:
    """The other repos whose tracked text references this file. A
    repo-QUALIFIED spelling always counts. A BARE relative path counts
    only when the referencing repo (a) does not itself carry that path (a
    bare reference to one's own local file is self-reference) and (b) is
    not openxFactory — the neutral home's guides state the domain-repo
    LAYOUT CONVENTION in bare relative form (`hermes/domain/overlay.yaml`,
    `tenants/README.md`, ...), so a bare openxFactory mention is a
    convention statement, never a consumer edge; a real neutral-home
    consumer (the DTN-019 pattern) is always repo-qualified. Both rules
    proven on the 2026-08-04 stage-1 dry run."""
    qualified = (f"{repo}/{rel_posix}", f"xFactories/{repo}/{rel_posix}")
    consumers = []
    for other, rr in refs.items():
        if other == repo:
            continue
        if any(q in rr.refs for q in qualified) or (
                other != OPENX_REPO
                and rel_posix in rr.refs and rel_posix not in rr.files):
            consumers.append(other)
    return sorted(consumers)


# --- register-cited suppression ----------------------------------------------------

def register_cited_paths(register_text: str) -> frozenset:
    """Every path-like token the DTN candidate register cites (evidence
    bullets, exclusions, resolutions). A candidate whose aggregation path is
    one of these — or lives under a cited directory — is ALREADY in the
    promotion queue and is not re-filed."""
    return frozenset(_PATH_TOKEN_RE.findall(register_text or ""))


def is_register_cited(repo: str, rel_posix: str, cited: frozenset) -> bool:
    full = f"xFactories/{repo}/{rel_posix}"
    for token in cited:
        clean = token.rstrip("/").rstrip(".,;:")
        if full == clean or full.startswith(clean + "/"):
            return True
    return False


# --- the per-repo scan ---------------------------------------------------------------

def _stack_text(repo_path: Path) -> str:
    stack = Path(repo_path) / "stack.yaml"
    try:
        return stack.read_text(encoding="utf-8") if stack.is_file() else ""
    except OSError:
        return ""


def scan_repo(repo: str, repo_path: Path, neutral_index: NeutralIndex, *,
              lexicon: Lexicon | None = None, register_text: str = "",
              consumer_refs: dict | None = None) -> ScanResult:
    """Run all four deterministic signals over one domain repo. Pure
    function of the trees it reads: no state, no model, no writes."""
    repo_path = Path(repo_path)
    lexicon = lexicon or derive_lexicon(repo, repo_path)
    cited = register_cited_paths(register_text)
    stack_text = _stack_text(repo_path)
    refs = consumer_refs or {}

    result = ScanResult(repo=repo, lexicon_note=lexicon.source_note,
                        signal_counts={name: 0 for name in SIGNAL_NAMES})
    for rel_posix, abs_path in iter_text_files(repo_path):
        result.scanned_files += 1
        if rel_posix == "stack.yaml":
            continue  # the inventory surface itself is never a subject
        text = _read(abs_path)
        signals: list[Signal] = []

        name = Path(rel_posix).name
        is_schema = name.endswith(SCHEMA_SUFFIXES)
        is_script = abs_path.suffix in SCRIPT_SUFFIXES
        if (is_schema or is_script) and zero_lexicon_hits(text, lexicon):
            signals.append(Signal(
                "lexicon_absence",
                f"zero domain-lexicon hits (lexicon: "
                f"{lexicon.source_note})"))

        dup = near_duplicate(name, _tokens(text), neutral_index)
        if dup is not None:
            signals.append(Signal(
                "near_duplicate",
                f"near-duplicate of openxFactory/{dup[0]} "
                f"(token-set similarity {dup[1]:.2f} >= "
                f"{NEAR_DUPLICATE_SIMILARITY})"))

        consumers = consumers_of(repo, rel_posix, refs)
        if consumers:
            signals.append(Signal(
                "cross_repo_consumer",
                "referenced by other pinned repo(s): "
                + ", ".join(consumers)))

        if is_script and rel_posix.startswith("scripts/") and \
                rel_posix not in stack_text and name not in stack_text:
            signals.append(Signal(
                "uninventoried_tooling",
                "scripts/ tooling absent from stack.yaml's "
                "required-artifact surface"))

        if not signals:
            continue
        if is_register_cited(repo, rel_posix, cited):
            result.register_cited_skipped += 1
            continue
        for signal in signals:
            result.signal_counts[signal.name] += 1
        result.candidates.append(Candidate(
            repo=repo, path=rel_posix,
            content_sha256=_sha256_bytes(abs_path),
            signals=tuple(signals)))
    result.candidates.sort(key=Candidate.sort_key)
    return result


# --- incremental state (task 1.1) ------------------------------------------------------

def _render(document: dict) -> str:
    """Byte-stable rendering — the same JSON-as-YAML-subset shape every
    doc-health lane artifact uses (catalog.render's convention)."""
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def state_path(root: Path) -> Path:
    return Path(root) / STATE_DIR / STATE_NAME


def load_state(root: Path) -> dict:
    """The lane's per-repo incremental state: `{repo: {"last_run_commit",
    "judged": {path: sha256}}}`. Missing or unreadable state is an empty
    dict — the lane then treats every survivor as new (fail open into
    review, bounded by the dispatch batch)."""
    path = state_path(root)
    if not path.is_file():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    repos = loaded.get("repos") if isinstance(loaded, dict) else None
    return repos if isinstance(repos, dict) else {}


def record_state(root: Path, repos: dict) -> Path:
    """Atomically persist the full per-repo state map. Mutable by design
    (unlike the baseline markers): each successful stage-2 run advances the
    judged-digest map and the last-run commit."""
    path = state_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {"schema_version": SCHEMA_VERSION, "kind": STATE_KIND,
                "repos": repos}
    fd, tmp_name = tempfile.mkstemp(dir=path.parent,
                                    prefix=path.name + ".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(_render(document))
    os.replace(tmp_name, path)
    return path


def baseline_path(root: Path, repo: str) -> Path:
    if not repo or "/" in repo or "\\" in repo or repo.startswith("."):
        raise ValueError(f"invalid baseline repo id: {repo!r}")
    return Path(root) / STATE_DIR / BASELINE_SUBDIR / f"{repo}.yaml"


def load_baseline(root: Path, repo: str) -> dict | None:
    path = baseline_path(root, repo)
    if not path.is_file():
        return None
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if isinstance(loaded, dict) and loaded.get("kind") == BASELINE_KIND:
        return loaded
    return None


def record_baseline(root: Path, repo: str, commit: str, *, evidence: str,
                    as_of: str) -> Path:
    """Record one repo's immutable baseline marker (the recorded baseline
    marker type, task 1.1): a full neutrality sweep covered the repo up to
    `commit`, citing its evidence. Exclusive write — a recorded baseline is
    never rewritten (re-baselining is a human act that removes the marker
    through review, not tooling)."""
    from . import catalog_baseline  # local import: shares _write_exclusive
    path = baseline_path(root, repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    catalog_baseline._write_exclusive(path, _render({
        "schema_version": SCHEMA_VERSION,
        "kind": BASELINE_KIND,
        "status": "record",
        "repo": repo,
        "commit": commit,
        "as_of": as_of,
        "evidence": evidence,
    }))
    return path


def changed_paths_since(repo_path: Path, commit: str) -> frozenset | None:
    """Paths changed in `repo_path` since `commit` (the incremental window
    a baseline marker or last-run commit opens). None when git cannot
    answer — the caller then treats every path as potentially changed
    (fail open into review, never a silent skip)."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_path), "diff", "--name-only",
             f"{commit}..HEAD"],
            capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return frozenset(line.strip() for line in proc.stdout.splitlines()
                     if line.strip())


# --- disposition suppression (task 1.3's key shape) ---------------------------------

def disposition_suppressions(entries) -> dict:
    """`{(repo, path): {sha256, ...}}` from health/dispositions.yaml
    entries carrying this lane's family — the EXISTING dispositions
    vocabulary extended with `content_sha256` (proposal: "a candidate Brett
    rejects gets a recorded disposition ... keyed by (repo, path, content
    digest)"). An entry without a cite records no decision and suppresses
    nothing."""
    out: dict[tuple, set] = {}
    for entry in entries or []:
        if not isinstance(entry, dict) or entry.get("family") != LANE_ID:
            continue
        if not entry.get("cite"):
            continue
        digest = entry.get("content_sha256")
        repo, path = entry.get("repo"), entry.get("path")
        if isinstance(digest, str) and isinstance(repo, str) \
                and isinstance(path, str):
            out.setdefault((repo, path), set()).add(digest)
    return out


def is_suppressed(candidate: Candidate, suppressions: dict) -> bool:
    """True while the rejected content is UNCHANGED (digest match); a
    changed digest re-files (delta scenario "A rejected candidate stays
    rejected": suppression holds only while the content is unchanged)."""
    return candidate.content_sha256 in suppressions.get(
        (candidate.repo, candidate.path), ())


# --- stage-2 selection ---------------------------------------------------------------

@dataclass
class Selection:
    """The bounded stage-2 batch plus the counts the report states."""
    subjects: list = field(default_factory=list)   # [Candidate]
    selected: int = 0        # queue length before the batch bound
    carried_over: int = 0    # queue - batch (re-qualifies next run)
    suppressed: int = 0      # disposition-suppressed (unchanged digest)
    baseline_skipped: int = 0  # covered by a recorded baseline marker


def select_for_review(scan_results, *, state, baselines, changed_paths,
                      suppressions, budget, baseline_repo=None) -> Selection:
    """Deterministic stage-2 selection (design D6): survivors whose content
    is new or changed against the lane's judged-digest state, minus
    disposition-suppressed unchanged rejections, minus paths a recorded
    baseline marker covers (unchanged since the baseline commit), bounded
    to `budget` in (repo, path) order. The remainder carries over by simply
    staying unjudged. `baseline_repo` (the manual full-sweep input) ignores
    that one repo's baseline-marker skip so the whole tree re-queues."""
    selection = Selection()
    queue: list[Candidate] = []
    for result in scan_results:
        judged = (state.get(result.repo) or {}).get("judged") or {}
        baseline = baselines.get(result.repo)
        changed = changed_paths.get(result.repo)
        for candidate in result.candidates:
            if is_suppressed(candidate, suppressions):
                selection.suppressed += 1
                continue
            if judged.get(candidate.path) == candidate.content_sha256:
                continue  # already judged, unchanged
            if (baseline is not None and result.repo != baseline_repo
                    and candidate.path not in judged
                    and changed is not None
                    and candidate.path not in changed):
                selection.baseline_skipped += 1
                continue  # covered by the recorded baseline sweep
            queue.append(candidate)
    queue.sort(key=Candidate.sort_key)
    selection.selected = len(queue)
    selection.subjects = queue[:budget]
    selection.carried_over = max(0, len(queue) - budget)
    return selection
