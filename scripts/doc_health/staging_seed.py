"""STAGING-QUEUE seeds drafted from a set of documents the human selected.

The work queue is `ideation/staging/<topic>/` (CLAUDE.md): each topic folder
is a feat-spec-shaped fragment declaring target capability, delta type,
claims, open questions, and exit path. Getting a topic INTO that queue has
always been hand work — read the corpus, notice that several documents keep
meeting, write the fragment. The ideation dashboard's keyword lens is where
that noticing now happens (the radar puts every document carrying the checked
terms in one ring), so this module turns a selection on that radar into the
fragment's scaffold.

A SCAFFOLD, and deliberately not more. What can be computed is computed: the
documents, their repositories, the terms they all share, the terms only some
carry, and the staging id. What cannot be computed is left as explicit
`TO WRITE` prompts — the summary, why the topic is staged NOW, the claims,
the open questions and the exit path. A drafter that argued its own case
would be the machine deciding what is worth staging, which is the human's
call and the reason the queue exists.

SEED-FIRST, NEVER A WRITE — like `shared_identity`, what this produces is
TEXT. Nothing here creates a directory, and the human places the fragment.

DETERMINISTIC — no model call, no network, no clock (the date is passed in).
The same selection over the same corpus state drafts the same bytes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

#: The queue's home, repo-relative.
STAGING_DIR = "ideation/staging"
#: The queue's own index, which a merged fragment also needs a row in.
STAGING_INDEX = "ideation/staging/INDEX.md"
#: What an unwritable section says. One marker, so a reviewer can grep the
#: draft for everything still owed.
TODO = "TO WRITE"

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


@dataclass
class StagingSeed:
    """The drafted fragment: where it goes and what it says."""
    topic: str
    path: str
    text: str
    staging_id: str = ""
    documents: list = field(default_factory=list)
    shared: list = field(default_factory=list)
    partial: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"topic": self.topic, "path": self.path, "text": self.text,
                # the BRANCH SESSION's scope id. It was only ever in the
                # fragment's prose, which would have made the browser parse a
                # document to learn the name it must send back.
                "staging_id": self.staging_id,
                "documents": list(self.documents),
                "shared": list(self.shared), "partial": list(self.partial)}


def _slug(text: str) -> str:
    return _SLUG_STRIP.sub("-", str(text).lower()).strip("-")


def topic_slug(shared, documents, existing=None) -> str:
    """The folder name. Built from the terms every selected document carries —
    that IS what the topic is about — and falling back to the documents
    themselves when they share no term. Never collides with a topic already in
    the queue: an existing name gets a `-2`, `-3`, … suffix, because a seed
    that silently targets an occupied folder invites a human to overwrite
    someone else's staged work.
    """
    taken = {str(name) for name in (existing or [])}
    if shared:
        base = "-".join(_slug(term) for term in list(shared)[:3])
    elif documents:
        stem = str(documents[0]).rsplit("/", 1)[-1]
        base = _slug(stem.rsplit(".", 1)[0])
    else:
        base = ""
    base = base or "untitled-convergence"
    if base not in taken:
        return base
    n = 2
    while f"{base}-{n}" in taken:
        n += 1
    return f"{base}-{n}"


def _terms(document) -> list:
    raw = document.get("topics")
    if not isinstance(raw, list):
        return []
    return [str(t) for t in raw if t]


def convergence(documents) -> tuple:
    """`(shared, partial)` — the terms EVERY selected document carries, and
    the terms only some do. The first is the topic's spine; the second is what
    a human has to decide about, which is why the draft prints both rather
    than flattening them into one list."""
    rows = [d for d in (documents or []) if isinstance(d, dict)]
    if not rows:
        return ([], [])
    sets = [set(_terms(d)) for d in rows]
    every = set.intersection(*sets) if sets else set()
    some = set.union(*sets) - every if sets else set()
    return (sorted(every), sorted(some))


def draft_staging_seed(documents, *, project: str, as_of: str,
                       repository: str = "openxFactory",
                       existing=None,
                       source: str = "the ideation dashboard's keyword lens"
                       ) -> StagingSeed:
    """Draft ONE staging fragment covering the selected documents.

    `documents` are the snapshot's OWN document records (each with `id`/`path`
    and `topics`), resolved by the caller from the serve's snapshot — never
    evidence supplied by a client.
    """
    rows = [d for d in (documents or []) if isinstance(d, dict)]
    if not rows:
        raise ValueError("a staging seed needs at least one document")
    shared, partial = convergence(rows)
    topic = topic_slug(shared, [r.get("path") or r.get("id") for r in rows],
                       existing)
    path = f"{STAGING_DIR}/{topic}/{topic}.md"
    repos = sorted({str(r.get("repository")) for r in rows if r.get("repository")})

    lines = [
        f"# Staged: {TODO} — the capability this convergence is about",
        "",
        "Status: staged",
        "Kind: capability-proposal",
        f"Summary: {TODO} — what this topic would deliver, in one paragraph. "
        f"Drafted {as_of} from {source} over `{project}`: "
        f"{len(rows)} document" + ("" if len(rows) == 1 else "s")
        + " were selected together"
        + (f" because they all carry {', '.join('`' + t + '`' for t in shared)}"
           if shared else " (they share no single term — say what connects them)")
        + ".",
        "Topics: " + (", ".join(shared + partial) if (shared or partial)
                      else f"{TODO} — this selection carries no declared term"),
        "Repository context: "
        + (", ".join(repos) if repos else repository)
        + f" — {TODO}: which repository OWNS the neutral capability, and which "
        "are consumers.",
        f"Staging ID: {repository}:staging:{topic}",
        f"Source: selected on the ideation dashboard {as_of} "
        f"(project `{project}`); the documents are listed below.",
        f"Target capabilities: {TODO} — ADDED/MODIFIED, and against which "
        "existing capability.",
        "",
        "## The convergence (computed)",
        "",
        f"{len(rows)} document" + ("" if len(rows) == 1 else "s")
        + " selected on the radar:",
        "",
    ]
    for row in rows:
        identity = str(row.get("path") or row.get("id") or "")
        terms = _terms(row)
        where = f" ({row.get('repository')})" if row.get("repository") else ""
        carries = ", ".join("`" + t + "`" for t in terms) if terms \
            else "no declared term"
        lines.append(f"- `{identity}`{where} — {carries}")
    lines += [
        "",
        ("Carried by every one of them: "
         + ", ".join("`" + t + "`" for t in shared) + "."
         if shared else
         "No term is carried by all of them — this selection is a human "
         "judgment, and the fragment has to say what the connection is."),
    ]
    if partial:
        lines += [
            "",
            "Carried by some: " + ", ".join("`" + t + "`" for t in partial)
            + ". Each of these is a decision — in scope for this topic, or "
            "evidence that the selection is really two topics.",
        ]
    lines += [
        "",
        f"## Why this is staged now — {TODO}",
        "",
        "A brainstorm is promoted by a consumer, not by enthusiasm. Name what "
        "changed that makes this worth staging today.",
        "",
        f"## Claims — {TODO}",
        "",
        "What this topic asserts, each one checkable.",
        "",
        f"## Open questions — {TODO}",
        "",
        "What must be decided before an OpenSpec change can be written.",
        "",
        f"## Exit path — {TODO}",
        "",
        "The change this becomes, and what ratifies it.",
        "",
        "---",
        "",
        f"Drafted by {source}; nothing was written. Place this file, finish "
        f"every `{TODO}` section, and add its row to `{STAGING_INDEX}`.",
    ]
    return StagingSeed(topic=topic, path=path, text="\n".join(lines) + "\n",
                       staging_id=f"{repository}:staging:{topic}",
                       documents=[str(r.get("path") or r.get("id") or "")
                                  for r in rows],
                       shared=shared, partial=partial)
