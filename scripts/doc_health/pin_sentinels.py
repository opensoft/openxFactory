"""The declared sentinel vocabulary for derivation pins
(`declare-sentinel-pin-vocabulary`).

WHAT IT ANSWERS. `pin_class` next door declares WHICH artifacts and WHICH keys
carry a derivation pin, and verifies that the commit each one names is still
reachable. This module declares what a value in one of those keys may say when
it is NOT a commit name — because a generator that cannot truthfully pin a
commit must write something, and the two available failures are both worse than
a declaration. Stamping `HEAD` over content no commit held produces a pin that
RESOLVES and LIES: reachability answers pass, retention has nothing to retain,
and a reader who checks it is misled precisely because it looks healthy.
Inventing a local spelling produces a value every consumer guarding on some
other lane's spelling reads as a commit name.

WHY IT IS A REGISTRY MODULE. Ruled for the pin class itself and copied here
(packet `design.md` § 3): the vocabulary is read by the verification, by every
generator that stamps a pin, and by every consumer that guards on a pin value,
so it has to be IMPORTABLE. A contract artifact would owe a schema and a
release-bundle question; a table in the promoted spec would be prose a check has
to parse, and would make the vocabulary a thing that changes only by OpenSpec
change — wrong for a list whose whole job is to absorb a new condition the day a
generator meets one. This module has no dependency beyond the standard library,
so the standalone scripts can import it without dragging a package in.

ONE CONDITION, ONE CANONICAL SPELLING; A SECOND SPELLING IS A SECOND CONDITION
UNTIL MEASUREMENT SAYS OTHERWISE. Every member below states the condition it
stands for and whether it is canonical for new output or a legacy spelling
retained for committed state. `standing` is not decoration: a legacy member
without that marking is indistinguishable from a second canonical spelling,
which is the drift the declaration exists to stop rather than to bless. And the
legacy marking applies ONLY WITHIN one condition — two spellings that look like
variants are sometimes two conditions wearing similar words, and folding the
second into the first would silently restate every artifact carrying it.

THE FIVE COMMITTED SPELLINGS ARE ABSORBED AS THEY STAND, NEVER REWRITTEN. Seven
values act as sentinels in committed artifacts today and every one of them sits
inside an ARCHIVED packet. A content edit to captured material after capture is
a finding in its own right, and a value edited to a spelling the run did not
write makes the artifact state something that did not happen. This is the same
ordering that makes retention rather than re-pinning the repair for an orphaned
record pin: when the record cannot move, the declaration is what accommodates
it. Those hand-written values are also the argument — nobody designed this
practice; seven times an author confronted with content no commit held wrote
down which condition applied instead of stamping a commit that would have
resolved and lied.

ABSENCE IS RECOGNIZED AND IS NOT A MEMBER (Q2, ruled 2026-08-27). See
`ABSENT_KEY` below. An artifact carrying no pin key at all makes no claim,
honest or otherwise, and converting one into a sentinel after the fact would
assert a condition nobody recorded.

WHAT MEASURED `"unknown"` INTO A CONDITION OF ITS OWN, decided at realization
under the same-condition rule the delta states, because the packet left exactly
this point open. Three call sites emit it and they do not name one condition:

* `ideation_dashboard/snapshot_registry.py:283` — `self.source_revision or
  "unknown"` while projecting an INDEX ENTRY about a snapshot whose own
  `generation.source_revision` was absent, unfetchable or unrecorded. The
  repository is perfectly readable here; what is missing is the entry's record
  of a revision.
* `experiments/.../avatar_f0/cli.py:60` (`_git_head`) — `rev-parse HEAD`
  returned nothing, or the call raised. That IS the unreadable-repository
  condition, spelled `"uncommitted"` by `proposal-support.py`.
* `experiments/.../avatar_f0/cli.py:51` (`_git_file_commit`) — `git log -1 --
  <path>` returned nothing. On a SUCCESSFUL git run that means the path has no
  commit history at all: the repository is readable, `HEAD` resolves, and the
  named content has simply never been committed.

So `"unknown"` does not measure as one condition, and it therefore CANNOT be
folded in as a second spelling of `"uncommitted"`'s. Folding it would make every
artifact carrying it assert "the repository could not be read at all", which is
FALSE at two of the three sites. It is declared instead as the weakest member of
the vocabulary — the revision was not established and the emitter cannot say
which stronger condition held — and the declaration says outright that a
generator able to distinguish must reach for the stronger member instead. THE
FOLLOW-UP IS NAMED RATHER THAN PERFORMED: those three call sites deserve to be
split onto the three conditions they actually mean, which is a change to three
generators' output in two lanes and is not this packet's one instance.
"""

from __future__ import annotations

from dataclasses import dataclass

# --------------------------------------------------------------- the conditions
# Named separately from the spellings, because the whole point of the
# declaration is that a condition can have more than one spelling while a
# spelling may never have more than one condition.

DIRTY_WORKTREE = "dirty-worktree"
UNREADABLE_REPOSITORY = "unreadable-repository"
OUTSIDE_REPOSITORY = "outside-repository"
COMPOSED_PROJECTION = "composed-projection"
UNESTABLISHED_REVISION = "unestablished-revision"

CONDITIONS: dict[str, str] = {
    DIRTY_WORKTREE:
        "The generator read content from a working tree carrying uncommitted "
        "changes to that content. The content is REAL and is held by no "
        "commit, so no commit name describes it and `HEAD` would name a tree "
        "the generator did not read.",
    UNREADABLE_REPOSITORY:
        "The repository's own revision could not be read at all — `rev-parse "
        "HEAD` failed, `HEAD` is unborn, or the path is not a repository. "
        "Nothing about the content was established from git, which is a "
        "different and weaker statement than the dirty-tree condition.",
    OUTSIDE_REPOSITORY:
        "The derivation was performed outside any repository context, so no "
        "revision applies rather than one being unavailable. An ad-hoc "
        "derivation is a fact a reader can act on; an unreadable repository is "
        "an accident that may repair itself.",
    COMPOSED_PROJECTION:
        "The artifact is a projection composed from several sources, each with "
        "its own revision and no single one describing the whole. There is "
        "nothing to pin, as opposed to something that could not be read.",
    UNESTABLISHED_REVISION:
        "The revision was not established and the emitter cannot say which of "
        "the stronger conditions held. THE WEAKEST MEMBER OF THIS VOCABULARY: "
        "a generator that CAN tell an unreadable repository from uncommitted "
        "content from an ad-hoc derivation MUST write that stronger member "
        "instead, because a reader meeting this one learns only that nobody "
        "wrote down which condition applied.",
}

CANONICAL = "canonical"     # the spelling new generator output uses
LEGACY = "legacy"           # legal where already committed, never written afresh


@dataclass(frozen=True)
class SentinelMember:
    """One declared member of the sentinel vocabulary.

    `condition` is a key of `CONDITIONS`; a member without one is a magic
    string, which is why `declaration_defects()` refuses it. `emitters` names
    the code that writes the value — declared so that a member no committed
    artifact carries can be told apart from a member nothing writes at all, and
    MEASURED by test rather than believed. `qualified_prefix`, where a member
    declares one, admits the QUALIFIED form its emitter actually writes: it is a
    declared form, not a near-miss match, and the difference is that the prefix
    is written down here rather than guessed at the comparison."""
    value: str
    condition: str
    standing: str                     # CANONICAL | LEGACY
    emitters: tuple[str, ...]
    note: str
    qualified_prefix: str = ""

    def matches(self, value: str) -> bool:
        if value == self.value:
            return True
        return bool(self.qualified_prefix
                    and value.startswith(self.qualified_prefix))


# The spellings themselves, as importable constants — a generator writing one of
# these imports the name rather than retyping the string, which is the whole
# difference between a vocabulary and a habit.
UNCOMMITTED_WORKTREE = "uncommitted-worktree"
UNCOMMITTED = "uncommitted"
NOT_APPLICABLE_AD_HOC = "not-applicable-ad-hoc"
COMPOSED = "composed"
UNKNOWN = "unknown"


SENTINELS: tuple[SentinelMember, ...] = (
    SentinelMember(
        value=UNCOMMITTED_WORKTREE,
        condition=DIRTY_WORKTREE,
        standing=CANONICAL,
        emitters=(
            "scripts/bootstrap-ideation-cross-reference.py (git_generation)",
        ),
        note="THE SIX COMMITTED SITES, and the spelling the corpus chose "
             "before any tooling did. All six sit in proposal-support "
             "manifests inside ARCHIVED packets, hand-written by authors whose "
             "generator has never emitted such a value — which is what makes "
             "them evidence rather than debris. Canonical for the dirty-tree "
             "condition on that authority: it is the only spelling any "
             "committed artifact uses for it.",
    ),
    SentinelMember(
        value=UNCOMMITTED,
        condition=UNREADABLE_REPOSITORY,
        standing=CANONICAL,
        emitters=("scripts/proposal-support.py (repo_revision)",),
        note="NOT A LEGACY SPELLING OF THE MEMBER ABOVE, and Q1 ruled it so on "
             "2026-08-27 after measuring what its emitter means. "
             "`repo_revision()` returns it on a NON-ZERO EXIT from `rev-parse "
             "HEAD` and on nothing else — never on a dirty tree — so it names "
             "the unreadable-repository condition and is canonical for that "
             "one. The resemblance to `uncommitted-worktree` is a resemblance "
             "of words, not of conditions: one says the content is real and "
             "unreconstructible, the other says nothing about the content was "
             "established. No committed artifact carries this spelling today.",
    ),
    SentinelMember(
        value=NOT_APPLICABLE_AD_HOC,
        condition=OUTSIDE_REPOSITORY,
        standing=CANONICAL,
        emitters=(),
        note="ONE COMMITTED SITE, also hand-written and also inside an "
             "archived packet. NO GENERATOR EMITS IT, which is recorded rather "
             "than smoothed over: the member is carried by committed state, so "
             "it is not an unused declaration, but nothing in the tooling can "
             "produce it and a lane that meets this condition would have to "
             "reach for the constant deliberately.",
    ),
    SentinelMember(
        value=COMPOSED,
        condition=COMPOSED_PROJECTION,
        standing=CANONICAL,
        emitters=(
            "scripts/ideation_dashboard/snapshot_registry.py "
            "(compose_snapshots)",
        ),
        qualified_prefix="composed:",
        note="THE QUALIFIED FORM IS DECLARED BECAUSE IT IS WHAT THE EMITTER "
             "ACTUALLY WRITES. `compose_snapshots` seeds the key with the bare "
             "`composed` and then, where the members carried revisions, "
             "replaces it with `composed:<repo>@<ref>:<sha>,…` — the "
             "constituent revisions listed rather than discarded, which is "
             "strictly more useful to a reader. Declaring only the bare "
             "spelling would have left the lane's real output undeclared and "
             "the defect branch would have flagged its own committed "
             "projections the day it was switched on, which is exactly what "
             "Q3's seeding ruling forbids. Whether a composed view should "
             "carry a pin key at all is a schema question this packet leaves "
             "open (tasks § 5.3).",
    ),
    SentinelMember(
        value=UNKNOWN,
        condition=UNESTABLISHED_REVISION,
        standing=CANONICAL,
        emitters=(
            "scripts/ideation_dashboard/snapshot_registry.py (index_entry)",
            "experiments/avatar-brokered-call/src/avatar_f0/cli.py "
            "(_git_file_commit, _git_head)",
        ),
        note="CANONICAL FOR ITS OWN CONDITION, decided at realization on the "
             "measurement recorded in this module's docstring rather than on "
             "the resemblance to `uncommitted`. Its three call sites span "
             "three conditions — an entry with no recorded revision, an "
             "unreadable `HEAD`, and content that has never been committed — "
             "so it measures as more than one condition and cannot be folded "
             "into any single stronger member. It is declared as the weakest "
             "claim in the vocabulary and carries the instruction that goes "
             "with that: a generator that can distinguish must not reach for "
             "it. Splitting those three call sites onto the conditions they "
             "mean is a named follow-up, not this packet's work.",
    ),
)


# ------------------------------------------------- absence, recognized not held
# RULED 2026-08-27 (Q2). Declared here so a reader meets it in the same place as
# the members and can see that it is deliberately NOT one of them.

ABSENT_KEY = (
    "AN ABSENT PIN KEY IS A RECOGNIZED LEGACY STATE OF THE CORPUS AND IS NOT A "
    "MEMBER OF THIS VOCABULARY. An artifact carrying no pin key where its class "
    "member expects one makes no claim, honest or otherwise: it cannot be told "
    "apart from a generator that crashed before writing, a schema that predates "
    "the key, or a hand-written stub, where every sentinel above names which "
    "condition applied. It is therefore reported once, distinctly from an "
    "undeclared spelling, and REPAIRED NEVER — filling one in with a sentinel "
    "after the fact would assert a condition nobody recorded, which is the same "
    "falsification as writing a commit that was never true.")


# --------------------------------------------------------------------- lookups

def declared(value: object) -> SentinelMember | None:
    """The declared member `value` is, or None.

    EXACT, plus each member's own declared qualified form. Deliberately no
    normalization, no case folding and no nearest-match: a near-miss spelling is
    precisely the condition under which every consumer guarding on the exact
    string already fails, so guessing here would make this check agree with a
    consumer that crashes."""
    if not isinstance(value, str):
        return None
    for member in SENTINELS:
        if member.matches(value):
            return member
    return None


def is_declared_sentinel(value: object) -> bool:
    """Whether `value` is a declared honest non-pin.

    THE ONE PREDICATE CONSUMERS SHOULD CALL. A guard comparing a pin value
    against a single spelling recognizes one member of one condition and reads
    every other member as a commit name — which is not a hypothetical: three
    such comparisons in `proposal-support.py` raised `SupportError` on four of
    the five spellings above until this predicate replaced them."""
    return declared(value) is not None


def canonical_for(condition: str) -> SentinelMember | None:
    """The spelling NEW output uses for `condition`."""
    for member in SENTINELS:
        if member.condition == condition and member.standing == CANONICAL:
            return member
    return None


def members_for(condition: str) -> tuple[SentinelMember, ...]:
    return tuple(m for m in SENTINELS if m.condition == condition)


def declaration_defects() -> tuple[str, ...]:
    """Members declared without a condition or without a standing, plus any
    spelling declared twice.

    A member whose meaning is not written down is a magic string, and accepting
    one on the strength of its spelling being self-explanatory is how a reader
    ends up learning only that somebody chose not to write a commit."""
    out: list[str] = []
    seen: dict[str, str] = {}
    for member in SENTINELS:
        if member.condition not in CONDITIONS:
            out.append(f"{member.value!r} names no declared condition "
                       f"({member.condition!r})")
        if member.standing not in (CANONICAL, LEGACY):
            out.append(f"{member.value!r} declares no standing "
                       f"({member.standing!r}); a member must say whether it "
                       f"is canonical for new output or a legacy spelling")
        if not member.note.strip():
            out.append(f"{member.value!r} is declared without a note")
        if member.value in seen:
            out.append(f"{member.value!r} is declared twice")
        seen[member.value] = member.condition
    for condition in CONDITIONS:
        canonical = [m for m in members_for(condition)
                     if m.standing == CANONICAL]
        if len(canonical) != 1:
            out.append(f"condition {condition!r} has {len(canonical)} "
                       f"canonical spelling(s); exactly one is required so a "
                       f"generator knows which to write")
    return tuple(out)
