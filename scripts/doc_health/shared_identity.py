"""Cross-repository SHARED IDENTITY — the DTN candidate register's first
rule, computed (openxFactory `add-shared-identity-seeds`).

The promotion process states four ways a candidate is born
(`docs/domain-to-neutral-promotion-process.md`, "Candidate Rule"), and the
FIRST is the one no lane implements:

    "Two or more domain repos use the same structure with different domain
     nouns."

The neutrality-drift lane's four stage-1 signals ask adjacent questions —
`near_duplicate` compares a domain file against the OPENXFACTORY tree,
`cross_repo_consumer` looks for references, `lexicon_absence` and
`uninventoried_tooling` read one repo at a time. None of them asks whether
two DOMAIN repos carry the same thing. The ideation dashboard's composed
project view answers exactly that (topic D19–D21: a document identity's
CARRIER COUNT across a project's member repositories), so this module turns
that answer into the register's own intake artifact.

SEED-FIRST, NEVER A WRITE — the same discipline the neutrality lane records
(design D1/D4): what this module produces is TEXT in the register's format
that a human merges. Nothing here opens, edits, or appends to the register,
and the drafted number is read from the register's own numbering so a
drafted-but-unmerged gap never collides.

DETERMINISTIC — no model call, no network. The evidence IS the carrier set,
which is a fact about the pinned trees rather than a judgment about them, so
a seed drafted twice from one corpus state is byte-identical.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

#: Register-row vocabulary. Matches the neutrality lane's machine-drafted
#: seeds: a human raises priority at the register's own scoring step.
SEED_PRIORITY = "P2"
SEED_STATUS = "seed"
#: The rule this detector implements, quoted into every drafted seed so a
#: reviewer can check the claim against the process document.
CANDIDATE_RULE = ("Two or more domain repos use the same structure with "
                  "different domain nouns.")

DTN_ID_RE = re.compile(r"DTN-(\d+)")

#: The register's repo-relative home. MIRRORS `families.REGISTER_PATH` and is
#: pinned equal by test — restated here so a request-path caller can locate
#: the register without importing the whole family module.
REGISTER_PATH = "docs/domain-neutralization-candidate-register.md"

#: A shared identity is only a candidate when it is shared by at least this
#: many repositories — the rule's own threshold, stated once.
MINIMUM_CARRIERS = 2


@dataclass(frozen=True)
class SharedIdentity:
    """One document identity and the repositories that carry it."""
    identity: str
    repositories: tuple = ()

    @property
    def carrier_count(self) -> int:
        return len(self.repositories)


@dataclass
class SeedDraft:
    """The register addition, as TEXT. `row` belongs in the Candidate List
    table; `section` is the `### DTN-NNN:` detail block."""
    dtn: str
    row: str
    section: str
    identities: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"dtn": self.dtn, "row": self.row, "section": self.section,
                "identities": [
                    {"identity": s.identity, "repositories": list(s.repositories)}
                    for s in self.identities]}


def shared_identities(documents, *, repositories=None,
                      minimum: int = MINIMUM_CARRIERS, exactly=None) -> list:
    """Every identity carried by `minimum`+ of the given repositories.

    `documents` is the composed snapshot's document collection: each item
    carries its `repository` and a namespaced `id` whose tail is the
    cross-repository identity. `repositories`, when given, restricts the
    question to that member subset (the dashboard's VISIBLE set) so the
    answer matches what the human was looking at.

    `exactly` narrows further to identities whose carriers within that
    subset are EXACTLY the named combination — the lens's sector rule. It
    exists so a seed drafted from a region covers that region and nothing
    else: a row reading "carried by 3" must not draft a candidate spanning
    everything the wider set happens to share.
    """
    combination = None if exactly is None else {str(r) for r in exactly}
    wanted = None if repositories is None else {str(r) for r in repositories}
    carriers: dict[str, list] = {}
    for doc in documents or []:
        if not isinstance(doc, dict):
            continue
        repository = doc.get("repository")
        identity = _identity(doc)
        if not repository or not identity:
            continue
        repository = str(repository)
        if wanted is not None and repository not in wanted:
            continue
        seen = carriers.setdefault(identity, [])
        if repository not in seen:
            seen.append(repository)
    rows = [SharedIdentity(identity=identity, repositories=tuple(sorted(repos)))
            for identity, repos in carriers.items()
            if len(repos) >= minimum
            and (combination is None or set(repos) == combination)]
    # widest convergence first, then alphabetical — a stable review order
    rows.sort(key=lambda s: (-s.carrier_count, s.identity))
    return rows


def _identity(doc: dict) -> str:
    raw = doc.get("id")
    text = "" if raw is None else str(raw)
    at = text.find("::")
    tail = text[at + 2:] if at >= 0 else text
    return tail or str(doc.get("path") or "")


def next_dtn_id(register_text: str) -> str:
    """The next free `DTN-NNN`, from every id the register mentions (rows
    AND detail sections, so a drafted-but-unmerged gap never collides) —
    the neutrality lane's rule, restated here so this module can draft
    without importing the model-dispatch half."""
    numbers = [int(m) for m in DTN_ID_RE.findall(register_text or "")]
    return "DTN-%03d" % ((max(numbers) + 1) if numbers else 1)


def _cell(text: str, limit: int = 90) -> str:
    """One register-row cell: pipe-free, whitespace-collapsed, bounded."""
    clean = " ".join(str(text).replace("|", "/").split())
    return clean[:limit].rstrip() or "(unspecified)"


def topic_line(rows: list, project: str) -> str:
    """The row's Topic cell: what the convergence IS, in register voice."""
    repos = sorted({r for s in rows for r in s.repositories})
    if len(rows) == 1:
        return _cell(f"Shared across {len(repos)} factories: {rows[0].identity}",
                     limit=80)
    return _cell(f"{len(rows)} artifacts shared across {len(repos)} "
                 f"factories ({project})", limit=80)


def draft_seed(register_text: str, rows: list, *, project: str,
               as_of: str, source: str = "the ideation dashboard's "
               "repository lens") -> SeedDraft:
    """Draft ONE register seed covering a shared-identity finding.

    Returns TEXT only — the caller shows it to a human, who merges it. The
    seed states its own provenance, quotes the candidate rule it satisfies,
    and lists every identity with its carriers as evidence, because the
    carrier set IS the evidence for this rule.
    """
    if not rows:
        raise ValueError("a shared-identity seed needs at least one identity")
    dtn = next_dtn_id(register_text)
    topic = topic_line(rows, project)
    repos = sorted({r for s in rows for r in s.repositories})
    artifact = _cell("to be determined at staging (the shared surface, "
                     "neutralized once)")
    row = (f"| {dtn} | {topic} | `promote` | {SEED_PRIORITY} | "
           f"`{SEED_STATUS}` | {artifact} |")

    lines = [
        f"### {dtn}: {topic}",
        "",
        f"Deterministic seed drafted {as_of} from {source} over project "
        f"`{project}` — pending human approval; this candidate enters the "
        "register lifecycle only when the seed is merged. It satisfies the "
        f"promotion process's first candidate rule verbatim: “{CANDIDATE_RULE}”",
        "",
        f"{len(rows)} document "
        + ("identity is" if len(rows) == 1 else "identities are")
        + f" carried by {MINIMUM_CARRIERS} or more of the project's member "
        f"repositories ({', '.join(repos)}). The carrier set is the evidence: "
        "no model judged this, and a re-run over the same corpus state drafts "
        "the same seed.",
        "",
        "Evidence:",
        "",
    ]
    for shared in rows:
        lines.append(f"- `{shared.identity}` — carried by "
                     f"{shared.carrier_count} of {len(repos)}: "
                     + ", ".join(shared.repositories))
    lines += [
        "",
        "Domain-local exclusions: a shared PATH is not a shared CONTRACT — "
        "staging must read the carriers and separate the neutral structure "
        "from each factory's domain nouns before any promotion decision.",
    ]
    return SeedDraft(dtn=dtn, row=row, section="\n".join(lines) + "\n",
                     identities=list(rows))
