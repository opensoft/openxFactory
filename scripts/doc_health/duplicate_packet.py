"""Duplicate discharge of one ruling across two archived packets
(`add-duplicate-packet-check`).

THE TWENTIETH family registered in `families.FAMILIES`, behind
`release_inventory.py`'s nineteenth, which realized while this one was being
written. `FAMILIES` is the count, as its own module docstring says.

WHAT IT ANSWERS. The eighteenth family asks whether a ratified delta REACHED
canon. Its neighbour, discovered the night the eighteenth family's first
remedy was applied, asks the opposite question about the same documents:
whether ONE ruling was discharged TWICE. Two archived packets can restate the
same delta content — the same requirement, byte for byte, under the same
capability — and every check in this corpus reports the repository healthy.
`openspec --strict` validates each packet's SHAPE in isolation; the lifecycle
families read headers, not bodies; and promotion fidelity reads 0 either way,
because canon holds exactly what both packets said it should. A redundant
governance act leaves no trace anywhere.

THE CLASS IS NOT HYPOTHETICAL — it is a NEAR MISS on this repository's own
record, and the record is why the check exists. openxFactory PR #317 and the
landed `2026-08-25-apply-branch-sessions-deltas` both restated the identical
2026-08-01 `add-workbench-branch-sessions` delta; the two delta files hash the
same blob. #317 was closed unmerged twenty minutes later by a human who
noticed, and the close comment carries the finding verbatim: "Closed unmerged
as the duplicate of apply-branch-sessions-deltas (main 042df4e7), which landed
mid-flight from a parallel session … One ruling, one discharge: the landed
packet is it." Had the merge order gone the other way by those twenty
minutes, both packets would have archived and nothing would have said so.

THE RULE, AND THE ONE EXEMPTION THAT KEEPS THE LAWFUL REMEDY LEGAL:

1. **Content identity, not resemblance.** Two archived packets fire only where
   they state the same `(capability, requirement title)` with requirement
   bodies that are identical after trailing whitespace is normalized and in no
   other way. A content-SIMILARITY heuristic would be this family inventing
   judgement about which two governance acts are "the same enough", which is
   exactly the judgement a deterministic family must not make. See
   `fingerprint`.

2. **A recorded lineage is exempt.** The lawful remedy for a promotion gap —
   codexFactory PR #85, and this repository's own
   `apply-branch-sessions-deltas` — DELIBERATELY restates an original
   packet's delta byte-faithfully, because applying already-ratified text is
   the whole point and any edit would be new normative content smuggled in
   under an old ratification. What separates that from a double discharge is
   that the remedial packet NAMES the original in its proposal. So a pair
   where either proposal names the other's change id is a recorded remedial
   lineage and stays quiet. Two remedials of one original that do NOT name
   each other — the near-miss shape — fire against each other while both stay
   exempt against the original.

   THE NAMING IS LINEAGE-IN-THE-RECORD, NOT AN AUTHORITY CLAIM. Naming the
   original does not make a packet's restatement lawful; the ratification that
   makes it lawful is the original's, and a packet claiming otherwise is the
   `ratified-provenance` family's finding to report, not this one's. What the
   naming does is make the SECOND statement traceable to the first, so a
   reader can see one ruling with one discharge and a recorded application of
   it rather than two independent discharges that happen to agree. This
   family reports untraceable restatement; it does not adjudicate standing.

3. **The C5 exemption and dispositions, both borrowed rather than reinvented.**
   A packet whose own proposal declares a pre-ratification standing discharged
   no ruling, so it can neither fail to promote one nor discharge one twice;
   it is read out through the eighteenth family's own
   `declares_pre_ratification`. And `health/dispositions.yaml` suppresses under
   the same contested-finding discipline every other family already applies —
   an entry naming THIS family, with a `cite`, optionally narrowed to one
   requirement.

A SIBLING FAMILY, NOT A NEW FINDING KIND INSIDE THE EIGHTEENTH. The parsing
is shared — this module owns no grammar of its own, and reads archived deltas
through `promotion_fidelity.parse_delta` for the reason that module already
states about the promoted reader: a second grammar for one document's headings
is how two readers come to disagree about what it says. What is NOT shared is
the finding: dispositions key on `(family, repo, path)`, so folding this class
into `promotion-fidelity` would let one disposition recorded against a delta
for a promotion gap silently suppress a duplicate-discharge finding on the
same delta — two different governance decisions bought with one citation. The
report's per-family counts would conflate two questions with two different
remedies for the same reason.

THE BASIS IS THE PINNED CHECKOUT, deliberately and unlike its neighbour. The
2026-08-24 ruling (task 4.1, PR #315) put the live-`main` basis on the
promotion-fidelity family AND ON THAT FAMILY ALONE, and `basis_notes` states
in every report that every other family measures the checkout. This family
keeps that sentence true. The cost is bounded and the catch point is the right
one anyway: a duplicate arrives in the PULL REQUEST that adds the second
packet, and a repository's self-gate run reads its own tree at that tip.

THIS FAMILY IS ENFORCING, IN BOTH HALVES OF WHAT THAT MEANS. Every finding is
ERROR, so a run configured `--fail-on error` fails on a ruling discharged
twice; and the family is registered `contested` in
`families.FAMILY_RESOLUTION`, so a finding that stops being reported without a
recorded citation becomes an `error` under the uncited-resolution rule. The two
move TOGETHER and must not be taken apart: severity alone gates without the
discipline that makes a disappearing finding accountable, and the contested
class alone gates through `uncited-resolution` under a family name that does
not say what happened. `test_the_two_halves_cannot_drift_apart` fails by name
on a half-flip in either direction.

IT SHIPPED ADVISORY, and that is a sequence rather than a history this
docstring has replaced. At launch every finding carried WARNING and the family
was deliberately unclassified, because nobody had measured what any archive
outside this repository would say and a `contested` advisory family would have
gated through the back door on the first duplicate anyone withdrew. The flip
came by ruling — **Brett, 2026-08-25, verbatim: "flip the duplicate-packet
check to enforcing"** — and it was taken behind a corpus MEASURED AT ZERO
rather than over a standing population, on
`govern-openspec-corpus-membership`'s rule that "a gate that goes red on the
commit that introduces it teaches everyone to route around the gate". The
measurement is recorded in
`openspec/changes/add-duplicate-packet-check/tasks.md` §5.1.

WHAT THE FLIP DOES NOT SETTLE. §5.2's question — whether this family should
join promotion fidelity on the live-`main` basis — stays OPEN. This family
enforces on the PINNED CHECKOUT, which is the basis it was measured at zero on
and the basis it reads; moving it is still its own ruling, and enforcing on a
tree is not an argument for enforcing on a different one.

THE NEIGHBOUR'S CLASS STILL DOES NOT REACH THIS ONE, and now the reverse is
equally true. `runner` applies `FAMILY_RESOLUTION.get(f.family, f.resolution)`
on a finding's OWN family, so the two families' classes cannot cross even when
both report against the same archived delta — which matters in both directions
now that both are `contested`. Asserted, not assumed:
`test_enforcement_by_resolution_class` and
`test_a_disposition_for_the_neighbouring_family_disposes_nothing`.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from . import ERROR, Finding, Skip
from . import promotion_fidelity
from .promotion_fidelity import (CHECKED_OPS, WorkingTree, _archive_date,
                                 norm, parse_delta)

FAMILY = "duplicate-packet"

# This family's severity, named once. The NAME records where the value
# STARTED — the identifier is deliberately not renamed, because it is the grep
# that ties every reader of the launch decision together — and the VALUE
# records the ruling that moved it: ERROR now, so `runner.main`'s `--fail-on
# error` gate (`{CRITICAL, ERROR}`) reds on a ruling discharged twice. It was
# WARNING for the advisory launch.
#
# The family is ALSO registered `contested` in `families.FAMILY_RESOLUTION`,
# and that is the less obvious half of the SAME decision — the two cannot move
# apart, and `test_the_two_halves_cannot_drift_apart` fails by name if they do.
# FLIPPED 2026-08-25 by ruling (Brett, verbatim "flip the duplicate-packet
# check to enforcing"), on a corpus measured at zero at `d5f447e8`. Both
# halves, and what the flip deliberately leaves open, are in this module's
# docstring.
_LAUNCH_SEVERITY = ERROR

_ACTION = ("name the packet this one restates in its proposal, or withdraw "
           "the duplicate discharge")


def fingerprint(body: list[str]) -> str:
    """The comparison identity of one requirement BLOCK: sha256 of its bytes,
    with trailing whitespace normalized and NOTHING ELSE normalized.

    TRAILING WHITESPACE ONLY, and the boundary is deliberate. Per-line
    trailing spaces and trailing blank lines are invisible to every reader and
    are added or removed by editors nobody chose; a packet whose only
    difference from another is that its last requirement sits at end-of-file
    rather than above a following block is not a different statement. Every
    other difference counts: a re-wrapped paragraph, a changed article, a
    scenario reordered. Those are edits a human made to normative text, and a
    family that forgave them would be deciding that two governance acts are
    "close enough" to be one — a similarity heuristic wearing a normalizer's
    clothes.

    LEADING blank lines are NOT stripped, for the same reason: the one that
    sits between a requirement header and its prose is part of how the block
    is written, and this family's promise is byte-equality above the trailing
    rule, not a best effort at it. The cost is a false NEGATIVE (two packets
    differing only in a leading blank line stay quiet), which is the safe
    direction for an advisory launch.

    The digest rather than the text: findings name a short prefix of it, which
    is the spelling the near-miss record itself used ("delta file sha256
    f6ffd39a…, Corpus scan scope block 99fa2a84…"), and it keeps a whole
    requirement body out of a dictionary key.
    """
    lines = [line.rstrip() for line in body]
    while lines and not lines[-1]:
        lines.pop()
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def change_id(change: str) -> str:
    """The bare change id under an archived folder's `YYYY-MM-DD-` prefix.

    A proposal names its lineage in change-id vocabulary
    (`add-workbench-branch-sessions`), not in archive-folder vocabulary, and
    both spellings appear in the corpus — so `names_change` looks for both and
    this is how it gets the first one. A folder carrying no date prefix is its
    own id.
    """
    date = _archive_date(change)
    return change[len(date) + 1:] if date else change


def _mention(identifier: str) -> re.Pattern:
    """`identifier` as a whole token, never as a fragment of a longer one.

    THE FALSE-EXEMPTION CHANNEL this closes is real and cheap to fall into: a
    plain substring test would let `add-foo`'s id match inside a packet that
    only ever names ITSELF as `add-foo-extended`, and the exemption would be
    bought by a coincidence of naming. The boundaries are `[\\w-]` rather than
    `\\b` precisely because change ids are hyphenated: `\\b` treats the hyphen
    as a boundary and would match the fragment.
    """
    return re.compile(rf"(?<![\w-]){re.escape(identifier)}(?![\w-])")


class Statement:
    """One archived packet's statement of one requirement block."""

    __slots__ = ("change", "capability", "op", "title", "delta_rel", "digest")

    def __init__(self, change: str, capability: str, op: str, title: str,
                 delta_rel: str, digest: str):
        self.change = change
        self.capability = capability
        self.op = op
        self.title = title
        self.delta_rel = delta_rel
        self.digest = digest

    @property
    def order(self) -> tuple[str, str]:
        """Which of two packets discharged LATER, deterministically.

        The archive folder's date, then the folder name — and unlike the
        eighteenth family's tie-break, version-control history is deliberately
        NOT consulted. There, order decides WHICH statement canon must match,
        so a wrong answer is a wrong finding; here it decides only which of
        two packets already reported as a pair carries the finding's path and
        which is named in its text. A rule that needs no history is the right
        cost for a cosmetic ordering, and it keeps a fixture tree with no
        commits reporting exactly what a real checkout does.
        """
        return (_archive_date(self.change), self.change)


class _Proposals:
    """Memoized `proposal.md` bodies for one tree, read once per packet.

    The lineage question is asked once per PAIR, and a requirement restated
    across several packets asks it several times about the same two files.
    """

    __slots__ = ("_tree", "_cache")

    def __init__(self, tree):
        self._tree = tree
        self._cache: dict[str, str] = {}

    def text(self, change: str) -> str:
        if change not in self._cache:
            body = self._tree.read(
                f"openspec/changes/archive/{change}/proposal.md")
            self._cache[change] = body or ""
        return self._cache[change]

    def names_change(self, change: str, other: str) -> bool:
        """Does `change`'s proposal name `other` — as a change id, or as the
        archived folder that carries it?

        BOTH SPELLINGS, because the corpus uses both and often in the same
        paragraph. `apply-branch-sessions-deltas` names its original as the
        bare id on one line ("archived change `add-workbench-branch-sessions`")
        and as the archive path on the next
        ("openspec/changes/archive/2026-08-01-add-workbench-branch-sessions/").
        A reader accepts either; so does this.

        THE PROPOSAL, and only the proposal. A packet's `design.md` and
        `tasks.md` are working notes; the proposal is the packet's normative
        face and the document every other lifecycle family already reads to
        learn what a packet claims. Lineage recorded only in a task note is
        lineage a reader of the record does not see, which is the state this
        family exists to report.
        """
        text = self.text(change)
        if not text:
            return False
        return bool(_mention(change_id(other)).search(text)
                    or _mention(other).search(text))


def collect_statements(tree) -> dict[tuple[str, str, str], list[Statement]]:
    """Every archived requirement BLOCK in one repository, grouped by identity.

    The key is `(capability, normalized title, body digest)` — deliberately
    NOT including the operation. Two packets that state one requirement's body
    byte-identically under one title have made the same statement whether both
    spelled it `ADDED` or one spelled it `MODIFIED`; a later MODIFIED that
    reproduces an earlier block exactly modified nothing. Requiring the ops to
    match would be a narrower rule bought with a false-negative channel that
    a one-word edit opens.

    RENAMED writers carry no requirement block and are skipped: `parse_delta`
    returns renames separately, and `CHECKED_OPS` is the eighteenth family's
    own name for the three that state a body.

    An EMPTY body is skipped too. `openspec --strict` requires every
    requirement to carry a scenario so the corpus has none, but two packets
    whose blocks are both empty would otherwise be "identical" for a reason
    that says nothing about either.
    """
    groups: dict[tuple[str, str, str], list[Statement]] = {}
    for change in tree.archive_changes():
        deltas = tree.delta_specs(change)
        if not deltas or promotion_fidelity.declares_pre_ratification(
                tree, change):
            continue
        for rel in deltas:
            capability = rel.rsplit("/", 2)[-2]
            body = tree.read(rel)
            if body is None:
                continue
            requirements, _renames = parse_delta(body)
            for req in requirements:
                if req.op not in CHECKED_OPS:
                    continue
                digest = fingerprint(req.body)
                if digest == fingerprint([]):
                    continue
                key = (capability, norm(req.title), digest)
                groups.setdefault(key, []).append(
                    Statement(change, capability, req.op, req.title, rel,
                              digest))
    return groups


def duplicate_pairs(tree) -> list[tuple[Statement, Statement]]:
    """`(earlier, later)` for every restatement pair with no recorded lineage.

    PAIRWISE within each identity group, which is the honest shape: three
    packets restating one requirement are three separate pairs, and two of
    them being exempt says nothing about the third. Tonight's near-miss is
    exactly that arithmetic — an original and two remedials, both remedials
    naming the original, so the two lineage pairs stay quiet and the pair the
    record has no account of fires.

    Statements from ONE packet are never paired with each other. A packet
    stating one requirement twice in one file is a malformed packet, not a
    second discharge, and `openspec --strict` is the reader that owns it.
    """
    proposals = _Proposals(tree)
    pairs: list[tuple[Statement, Statement]] = []
    groups = collect_statements(tree)
    for key in sorted(groups):
        statements = sorted(groups[key], key=lambda s: s.order)
        for i, first in enumerate(statements):
            for second in statements[i + 1:]:
                if first.change == second.change:
                    continue
                if (proposals.names_change(first.change, second.change)
                        or proposals.names_change(second.change,
                                                  first.change)):
                    continue
                pairs.append((first, second))
    return pairs


def _repo_trees(ctx) -> list[tuple[str, WorkingTree]]:
    """`(repo, tree)` for every repository in scope that carries an archive.

    THE PINNED CHECKOUT, always — see this module's docstring. `WorkingTree`
    is the eighteenth family's reader for exactly that basis, reused rather
    than re-derived so a change to how an archive is enumerated moves both
    families at once.
    """
    out = []
    for repo, path in sorted(ctx.repo_paths.items()):
        tree = WorkingTree(Path(path))
        if tree.has_archive():
            out.append((repo, tree))
    return out


def fam_duplicate_packet(ctx):
    """Every archived restatement pair the record gives no account of.

    A finding lands on the LATER packet's delta path — the redundant
    discharge is the one a reader acts on, by naming what it restates or by
    withdrawing it, and the earlier packet is named in the rule text. The
    same reasoning the eighteenth family recorded for landing on the delta
    rather than the promoted spec: the finding belongs on the document that
    made the claim, whose path is stable because it is an archived record and
    is what a disposition keys on.
    """
    scoped = _repo_trees(ctx)
    if not scoped:
        return Skip(FAMILY, "no repository in scope carries an OpenSpec "
                            "change archive")

    dispositions = promotion_fidelity.load_dispositions(ctx, FAMILY)
    findings: list[Finding] = []
    for repo, tree in scoped:
        for earlier, later in duplicate_pairs(tree):
            if promotion_fidelity.disposed(dispositions, repo,
                                           later.delta_rel, later.title):
                continue
            same_op = earlier.op == later.op
            ops = (f"{later.op}" if same_op
                   else f"{later.op} against the earlier {earlier.op}")
            findings.append(Finding(
                _LAUNCH_SEVERITY, FAMILY, repo, later.delta_rel,
                f"archived packet `{change_id(later.change)}` restates the "
                f"{ops} requirement {later.title!r} of capability "
                f"{later.capability!r} byte-identically from "
                f"`{change_id(earlier.change)}` (block sha256 "
                f"{later.digest[:8]}), and neither packet's proposal names "
                f"the other — one ruling discharged twice",
                _ACTION))
    return findings
