#!/usr/bin/env python3
"""Bootstrap the ideation cross-reference readiness index (add-ideation-cross-reference-readiness, task 2.4).

Generates the INITIAL `ideation/cross-reference.yaml` deterministically from the
current corpus headers, then renders `ideation/cross-reference.md` from it (via
`scripts/render-ideation-cross-reference.py`). One-time seed: the real clustering
+ scoring is realized by the codexFactory readiness worker (tasks 3.1-3.4). This
script's clustering rule is the PRECURSOR of that worker's task-3.3 design note —
kept deliberately simple and stated here so the worker can supersede it.

DETERMINISTIC CLUSTERING RULE (bootstrap):
  1. Sources. Parse every `ideation/brainstorm/*.md` and `ideation/staging/*/*.md`.
     From each header read `Topics:` (comma-separated subject tokens) and
     `Target capabilities:` (comma-/`and`-separated capability names, stripped of
     backticks and `(ADDED|MODIFIED|REMOVED)` markers), and `Status:` (the
     member's lifecycle stage).
  2. Token = cluster seed. Each distinct token's member set is the set of
     documents whose headers carry it; each (token, document) membership records
     which header field produced it (`topics-header` / `target-capabilities-header`).
  3. Multi-doc gate. Only tokens carried by TWO OR MORE documents form clusters —
     a cross-reference index surfaces RECURRENCE across docs/stages; a single-doc
     token is not a cross-reference.
  4. Co-extensive merge. Tokens with an IDENTICAL member set collapse into ONE
     cluster (indistinguishable as cross-stage signals; folds boilerplate
     co-travellers such as `doc-management`+`doc-workflow`). The cluster's
     `topics` lists all merged tokens, sorted.
  5. Stable identity + ordering. Cluster id = `cl-<seed>` where `<seed>` is the
     alphabetically-first token of the merged set (order-independent). Clusters
     are emitted sorted by id; members sorted by POSIX path; a member's
     `matched_tags` are the cluster tokens it carries (all of them, since a merge
     is co-extensive), sorted. `tag_sources` = the sorted union of header fields
     that produced the membership.

BOOTSTRAP POSTURE (honest placeholders, validated by task 2.3):
  - extension_fit: `has_promoted_fit: false` on EVERY entry with a statement that
    it is not yet assessed. The schema's fit flag is binary (no "unknown" state);
    bootstrap makes NO promoted-fit claim it cannot cite (citations need the
    scorer's evidence), so it records `false` + an explicit "not yet evaluated"
    statement. Even clusters that obviously relate to a promoted capability (e.g.
    the ideation-dashboard docs -> the promote-on-archive dashboard capability,
    which is NOT promoted yet) state this honestly rather than asserting a fit.
  - readiness: all three tiers UNSCORED with reason "bootstrap — scoring worker
    not yet realized"; NO recommendation flags (the min>=8 gate never fires at
    bootstrap).
  - possibles_register: ABSENT — its content arrives via the ideation-dashboard
    flows in a later wave; when present, its entries are validated by
    `validate-ideation-dashboard-contracts.py` (C3 ownership line).

Usage:
    python3 scripts/bootstrap-ideation-cross-reference.py [--repo REPO]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR PyYAML is required", file=sys.stderr)
    sys.exit(2)

# `doc_health` is a sibling package of this script (both live directly under
# `scripts/`), so Python's own `sys.path[0]` insertion — the invoked script's
# containing directory — already makes it importable with no extra path
# manipulation, whether this runs as `python3 scripts/bootstrap-ideation-
# cross-reference.py` from any cwd. Verified before relying on it (finding F5,
# align-status-reader-to-real-lines): unlike a script that genuinely cannot
# reach `doc_health` (which would keep a local copy joined to the shared rule
# by an agreement test instead), this one converts.
from doc_health.lines import split_keepends

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "scripts" / "render-ideation-cross-reference.py"
GENERATOR_VERSION = "ideation-xref-bootstrap-0.1.0"
UNSCORED_REASON = "bootstrap — scoring worker not yet realized"
FIT_STATEMENT = (
    "Bootstrap: extension-fit not yet evaluated. The readiness scoring worker "
    "(task 3.x, not yet realized) assesses promoted-fit with cited evidence; recorded "
    "as no-promoted-fit-claim pending that evaluation, not an asserted 'no fit exists' finding."
)

# A header line introduces a new field iff it looks like `Field Name:` (letters/
# spaces before the colon); anything else (lowercase prose, a backtick) continues
# the previous field. Header region = everything before the first `## ` body H2.
FIELD_RE = re.compile(r"^([A-Z][A-Za-z][A-Za-z ]*):\s?(.*)$")
CAP_TOKEN_RE = re.compile(r"^[a-z][a-z0-9-]*$")
SLUG_RE = re.compile(r"[^a-z0-9]+")


def parse_header(text: str) -> dict[str, str]:
    """Parse the contiguous header field block (H1 + blank skipped) up to the
    first `## ` body section, joining continuation lines onto their field —
    identical to `doc_health.ideation_readiness._parse_header`, and pinned to
    agree with it (`tests/doc-health/test_ideation_readiness.py`).

    Real lines (CR/LF/CRLF only — `doc_health.lines`), not `str.splitlines()`
    pseudo-lines (finding F5, align-status-reader-to-real-lines): this was
    the ONE-TIME bootstrap already run once (2026-07-14) to seed the corpus,
    but a rule that disagrees with its own twin is still worth correcting —
    if it is ever re-run, its clustering must not silently diverge from what
    the readiness worker would derive from the same documents now.
    """
    fields: dict[str, str] = {}
    current: str | None = None
    for body, _ending in split_keepends(text):
        if body.startswith("## "):
            break
        if body.startswith("# ") or not body.strip():
            continue
        m = FIELD_RE.match(body)
        if m:
            current = m.group(1).strip()
            fields[current] = m.group(2).strip()
        elif current is not None:
            fields[current] = (fields[current] + " " + body.strip()).strip()
    return fields


def topic_tokens(value: str) -> list[str]:
    return [t.strip() for t in value.split(",") if t.strip()]


def capability_tokens(value: str) -> list[str]:
    # Strip delta markers and backticks, split on commas and the word "and".
    cleaned = re.sub(r"\((?:ADDED|MODIFIED|REMOVED)\)", " ", value)
    cleaned = cleaned.replace("`", " ")
    pieces = re.split(r",|\band\b", cleaned)
    out: list[str] = []
    for p in pieces:
        tok = p.strip().strip(".").strip()
        if CAP_TOKEN_RE.match(tok):
            out.append(tok)
    return out


def slug(token: str) -> str:
    return SLUG_RE.sub("-", token.lower()).strip("-")


def git_generation(repo: Path) -> dict[str, str]:
    def _git(args: list[str]) -> str:
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, check=True,
            env={"TZ": "UTC", "PATH": __import__("os").environ.get("PATH", "")},
        ).stdout.strip()

    rev = _git(["rev-parse", "HEAD"])
    at = _git(["show", "-s", "--format=%cd", "--date=format-local:%Y-%m-%dT%H:%M:%SZ", "HEAD"])
    return {"source_revision": rev, "generated_at": at, "generator_version": GENERATOR_VERSION}


def collect(repo: Path) -> dict[str, dict]:
    """token -> {"docs": {path: {"stage": s, "sources": set()}}}."""
    tokens: dict[str, dict] = {}
    paths = sorted(
        list((repo / "ideation" / "brainstorm").glob("*.md"))
        + list((repo / "ideation" / "staging").glob("*/*.md"))
    )
    for path in paths:
        rel = path.relative_to(repo).as_posix()
        header = parse_header(path.read_text(encoding="utf-8"))
        stage = (header.get("Status") or "").strip().lower()
        topics = set(topic_tokens(header.get("Topics", "")))
        caps = set(capability_tokens(header.get("Target capabilities", "")))
        for tok in topics | caps:
            srcs: set[str] = set()
            if tok in topics:
                srcs.add("topics-header")
            if tok in caps:
                srcs.add("target-capabilities-header")
            entry = tokens.setdefault(tok, {"docs": {}})
            entry["docs"][rel] = {"stage": stage, "sources": srcs}
    return tokens


def build_index(repo: Path) -> dict:
    tokens = collect(repo)
    # Multi-doc gate + co-extensive merge: group tokens by their member-doc set.
    groups: dict[frozenset, list[str]] = {}
    for tok, data in tokens.items():
        docs = frozenset(data["docs"])
        if len(docs) < 2:
            continue
        groups.setdefault(docs, []).append(tok)

    entries = []
    for docset, toks in groups.items():
        toks_sorted = sorted(toks)
        seed = toks_sorted[0]
        cid = f"cl-{slug(seed)}"
        # tag_sources: union over all (token, member) memberships in this cluster.
        tag_sources: set[str] = set()
        for tok in toks:
            for meta in tokens[tok]["docs"].values():
                tag_sources |= meta["sources"]
        members = []
        for rel in sorted(docset):
            # a member's stage is consistent across the cluster's tokens
            stage = next(tokens[t]["docs"][rel]["stage"] for t in toks if rel in tokens[t]["docs"])
            members.append({
                "path": rel,
                "stage": stage,
                "matched_tags": list(toks_sorted),
            })
        entries.append({
            "id": cid,
            "name": seed.replace("-", " ").title(),
            "topics": list(toks_sorted),
            "tag_sources": sorted(tag_sources),
            "origin": "machine-derived",
            "members": members,
            "extension_fit": {"has_promoted_fit": False, "statement": FIT_STATEMENT},
            "readiness": {
                "tiers": [
                    {"tier": t, "unscored_reason": UNSCORED_REASON}
                    for t in ("domain", "company", "project")
                ]
            },
        })
    entries.sort(key=lambda e: e["id"])

    return {
        "schema_version": 1,
        "kind": "ideation-cross-reference",
        "repository": "openxFactory",
        "generation": git_generation(repo),
        "topic_entries": entries,
    }


HEADER_COMMENT = (
    "# GENERATED BOOTSTRAP — ideation cross-reference readiness index (source of truth).\n"
    "# Produced by scripts/bootstrap-ideation-cross-reference.py (add-ideation-cross-reference-readiness\n"
    "# task 2.4). Regenerate deterministically; ideation/cross-reference.md is a projection of THIS file.\n"
    "#\n"
    "# CLUSTERING RULE (bootstrap precursor of worker task 3.3): each Topics:/Target capabilities:\n"
    "# token is a cluster seed; a token carried by >= 2 docs forms a cluster; tokens with an\n"
    "# IDENTICAL member set are merged; cluster id = cl-<alphabetically-first token>; entries sorted\n"
    "# by id, members by path. See the script docstring for the full rule and the bootstrap posture\n"
    "# (all extension_fit unscored/no-claim, all tiers unscored, possibles_register absent).\n"
)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", type=Path, default=ROOT)
    args = ap.parse_args()
    repo = args.repo.resolve()

    index = build_index(repo)
    yaml_path = repo / "ideation" / "cross-reference.yaml"
    body = yaml.safe_dump(index, sort_keys=False, default_flow_style=False, width=100, allow_unicode=True)
    yaml_path.write_text(HEADER_COMMENT + body, encoding="utf-8")
    print(f"wrote {yaml_path} ({len(index['topic_entries'])} topic clusters)")

    md_path = repo / "ideation" / "cross-reference.md"
    rc = subprocess.run([sys.executable, str(RENDERER), str(yaml_path), str(md_path)]).returncode
    return rc


if __name__ == "__main__":
    sys.exit(main())
