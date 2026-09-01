"""The declared derivation-pin class, and reachability verified across it
(`govern-derived-pin-reachability`).

WHAT IT ANSWERS. A committed artifact that records "I was derived from this
repository at commit X" makes a claim a reader can check — reconstruct the
repository at X, re-derive, compare. When no ref reaches X the claim stops being
checkable BY ANYONE: there is no state to reconstruct, so the sentence is not
stale, it is unanswerable. The promoted `doc-health` obligation this module
serves already covers exactly ONE artifact (the cross-reference index, whose
unreachable pin fails the readiness derivation proof). This module carries the
CLASS that obligation did not reach, and verifies reachability across it.

THE CLASS IS DECLARED RATHER THAN PATTERN-DISCOVERED, and the reason is
measured rather than aesthetic (packet `design.md` § 4). A scanner keyed on
`source_revision` finds most of the class and misses two members whose pin is
PROSE: `ideation/cross-reference.md`'s rendered `- Source revision:` line, and a
gate-action record whose pin sits inside a `notes:` string as
`… at source_revision d09d5820…`. It would also silently stop covering any
artifact whose generator renamed its key, and a silent loss of coverage is
indistinguishable from a clean run. So `PIN_CLASS` below is the authority, and
`NON_MEMBERS` states — with a reason each — every place a pin-shaped value
legitimately appears without being a member. Anything in NEITHER is reported:
that is the half of the obligation a declaration alone cannot give.

THE TWO DIRECTIONS ARE BOTH CHECKED, because a declaration drifts both ways:

1. **A pin site no declared member covers** is reported, naming the artifact and
   the key. This is the direction that catches the arrival of a new generator.
2. **A declared member whose artifact has vanished** is reported. This is the
   direction that catches a registry row left behind by a deletion, and it is
   why `presence` distinguishes a member that has committed instances TODAY from
   one whose schema requires a pin but whose first instance has not landed.

A VALUE THAT IS NOT A COMMIT NAME IS CLASSIFIED RATHER THAN SKIPPED
(`declare-sentinel-pin-vocabulary`, 2026-08-27). Until that change this module
bound every value group to forty hex characters, so a sentinel produced NO SITE:
not reachable, not orphaned, not lost, and not uncovered either. The run reported
a fully verified class over seven archived artifacts whose central provenance
claim nothing had read. Now a non-commit value under a declared pin key is a
LEGAL NON-PIN where `pin_sentinels` declares it — a fifth outcome that does NOT
hold `fully_verified` open, because an artifact carrying an honest sentinel is
conforming — or a DEFECT where it does not. The commit-shaped path is untouched
by all of it: same regexes, same ref set, same verdicts, and a commit-shaped
value is skipped by the classification pass entirely.

THE REF SET CONSULTED IS `main` PLUS `refs/retention/pins/<full-sha>`, AND NO
MORE (delta requirement 4). Both halves matter:

* Reachability is judged against REFS, never against a clone's object store. A
  commit that survives locally because garbage collection has not reached it is
  NOT reachable — that survival is an accident of one machine. This is not a
  hypothetical distinction in this repository: in an agent worktree sharing an
  object store with the checkout that created them, all three of the orphans
  this class found answer `commit` to `git cat-file -t` while no ref reaches
  them, so a probe written against `cat-file` reports this repository clean.
* A ref OUTSIDE the retention namespace does not green a pin, however
  conveniently it points at one. A `refs/heads/keepalive`, a leftover
  remote-tracking ref from a since-deleted remote (this checkout has two), or a
  retention ref under some other name are all refused, because a ref whose name
  a reader cannot derive from the pin is not predictably reachable. The
  namespace is COMPUTED from the pin (`retention_ref`), never enumerated.

A CONSEQUENCE WORTH KNOWING BEFORE YOU REGENERATE SOMETHING. `main` means the
PUBLISHED branch, so an artifact regenerated on a branch and pinned to one of
that branch's OWN unlanded commits reports as orphaned until the branch lands.
That is the requirement read literally and it is the behaviour the landing rule
asks for — re-derive at a REACHABLE revision — and it is what house practice
already does: `harden-ideation-readiness-check` re-pinned the index to
`4e57009c`, a commit already on `main`, rather than to its own branch tip. The
ref set is deliberately not widened to include the revision under test, because
"main plus whatever branch I happen to be on" is not a ref set a reader can
reason about.

THE RETENTION HALF IS A REMOTE QUESTION, and that is stated rather than hidden.
Retention refs are published on the repository's own remote and are NOT fetched
by any default refspec, so a fresh clone does not carry them. The consult order
is: the local `refs/retention/pins/<pin>` first, then `git ls-remote origin`.
Where neither can be performed — no remote, no network — the pin is
INCONCLUSIVE and reported as a skip naming what could not be consulted. Never a
pass: an unaskable question is not an affirmative answer.

AN UNRECOVERABLE LOSS IS DISCHARGED BY A SUPERSEDING RECORD, NEVER BY DELETING
THE ROW (`supersede-lost-pin-baseline`, 2026-08-27). Where retention is
impossible, no code repair exists: the pinned object is gone, the record's bytes
may not be edited, and the resolution is the governance act
`ideation-cross-reference` requirement 2 names — a superseding record stating
the loss, what the original evidence still verifies, and what it cannot. This
module holds the class INCOMPLETELY VERIFIED while that act is owed, and stops
holding it when the record lands: `KNOWN_LOSSES` rows carry the record's path,
`discharging_record` goes to committed state to find it there and requires it to
NAME the pin, and `PinClassReport.lost_awaiting_record` is what
`fully_verified` consults. The loss itself is reported for ever either way —
restoring full verification by removing a row would be silencing, which is the
one resolution this module refuses.

THIS ADDS NO DETERMINISTIC CHECK FAMILY (packet OD-2, cleared 2026-08-27), and
that is structural here rather than promised: this module imports nothing from
`families` and defines no `fam_*` function, so it cannot be registered by
accident. Reachability is not deterministic in the sense that requirement means
— the same corpus at the same revision answers differently in a shallow clone
and a complete one — and every family added owes a wholesale restatement of the
enumeration requirement, which is a hazard `add-modified-block-currency-check`
exists to police. The verification rides the readiness-proof surface instead;
`ideation_readiness.verify_pin_reachability` is the entry point.

THE SEED INVENTORY IS THIS MODULE'S OWN MEASUREMENT, NOT THE PACKET'S TABLE, and
the discrepancy is recorded rather than smoothed over. `proposal.md` § The
pin-carrying artifact inventory reports 9 pins / 8 artifacts / 4 generators in
scope, swept by `git grep` over a key-name list. Re-measured at realization over
committed structured state — every 40-hex token in every committed `.yaml` /
`.yml` / `.json`, resolved against the object database — the repo-local class is
substantially larger, and the packet's sweep missed whole generator families
(the proposal-support transition manifests above all, 31 files) plus a THIRD
ORPHANED PIN the packet never saw. That third orphan is now retained. Both facts
are the argument for this module existing: a hand-swept inventory is exactly the
artifact that drifts.
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# THE DECLARED SENTINEL VOCABULARY. Imported as a sibling where this module is
# loaded as part of its package, and BY PATH where it is not — which is not a
# hypothetical fallback. `tests/review_lane_pin/test_review_lane_caller.py`
# loads this file with `spec_from_file_location` under a private name and NO
# package, deliberately, so that it does not have to duplicate the doc-health
# conftest's `sys.path` insert from a second directory; its docstring states the
# constraint that this module stays stdlib-only and importable that way. A bare
# relative import raises `ImportError: attempted relative import with no known
# parent package` there, which is how this was measured rather than predicted.
try:                                          # normal package import
    from . import pin_sentinels
except ImportError:                           # loaded by path, no package
    _spec = importlib.util.spec_from_file_location(
        "_pin_sentinels_by_path", Path(__file__).with_name("pin_sentinels.py"))
    pin_sentinels = importlib.util.module_from_spec(_spec)
    # Registered before exec for the same reason the caller test registers this
    # module before exec: `@dataclass` resolves a field's annotation through
    # `sys.modules[cls.__module__].__dict__`.
    sys.modules[_spec.name] = pin_sentinels
    _spec.loader.exec_module(pin_sentinels)

# --------------------------------------------------------------- the namespace

RETENTION_NAMESPACE = "refs/retention/pins"

FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

# THE WHOLE-OBJECT-NAME BOUNDARY, stated ONCE and carried by every expression
# that builds a pin site (`fix-pin-value-boundary-and-sentinel-split`).
#
# `(?![0-9a-fA-F])` rather than `\b`, because `\b` treats a hex digit boundary
# inside a longer hex run as a word boundary — so a sha256 digest under a
# declared pin key would yield a spurious "pin" that is the truncated first
# forty characters of a value nobody wrote. A fabricated pin is the one value
# this verification must never produce: it reports ORPHANED against an artifact
# whose recorded value is intact, or — worse — COLLIDES with a real object and
# certifies a provenance claim the artifact never made.
#
# Named as a constant rather than retyped four times so that the rule has one
# home; the structural test over this module asserts every site-building
# expression carries it, which is what stops a future prose member declaring an
# unguarded `pattern`.
HEX_BOUNDARY = r"(?![0-9a-fA-F])"

# A 40-hex token standing alone — not a prefix of a 64-hex sha256, not a suffix
# of one. Both directions here, because this one scans free text where a hex
# run may precede the token as well as follow it.
LOOSE_SHA_RE = re.compile(
    r"(?<![0-9a-fA-F])[0-9a-f]{40}" + HEX_BOUNDARY)


def retention_ref(pin: str) -> str:
    """The one retention ref name for `pin` — COMPUTED, never chosen.

    Q3, ruled 2026-08-27: `refs/retention/pins/<full-sha>`, one ref per retained
    commit, named for the full forty-character object name of the commit it
    retains. Deriving the name is what makes the repair mechanical: a repairer
    who computes it cannot get it wrong, and a reader resolving a record's pin
    computes the same name without a second lookup that could drift from it."""
    if not FULL_SHA_RE.match(pin or ""):
        raise ValueError(
            f"a retention ref is named for a FULL forty-character object name; "
            f"{pin!r} is not one")
    return f"{RETENTION_NAMESPACE}/{pin}"


# ------------------------------------------------------------- the declaration

TOOL_DEFINED = "tool-defined"      # a generator re-derives the body; reproduction
                                   # is byte-for-byte comparable at a new pin
MEASURED = "measured"              # no generator re-derives it; a re-pin owes a
                                   # NAMED measurement instead of bytes

REPO_LOCAL = "repo-local"          # a commit of THIS repository
CROSS_REPOSITORY = "cross-repository"   # state in another repository, answered
                                        # against another remote by another authority

# The spellings that mean THIS repository where an artifact names the repository
# a pin belongs to. Both are committed today: the routing records say
# `openxFactory`, the hermes handoff receipt says `opensoft/openxFactory`.
OWN_REPOSITORY_SPELLINGS = frozenset({"openxfactory", "opensoft/openxfactory"})


def _field_re(key: str) -> re.Pattern:
    """`key: <sha>` in YAML and `"key": "<sha>"` in JSON, with a REAL key
    boundary in front.

    The leading `(?<![A-Za-z0-9_])` is load-bearing and was added on evidence:
    without it the key `commit` matches the tail of `consumer_commit`, and the
    first real-repository run reported the hermes handoff receipt's
    CROSS-REPOSITORY consumer pin as a repo-local orphan. A substring match on a
    key name is not a key.

    The trailing `(?![0-9a-fA-F])` is `HEX_BOUNDARY` and is equally
    load-bearing: without it a sixty-four-character digest under this key
    yields a FABRICATED forty-character prefix — a value nobody wrote, judged
    for reachability as though the artifact had claimed it. The guard is copied
    from `LOOSE_SHA_RE` rather than invented, so the module states the rule
    once. No LEADING guard is added: the value group is already anchored by
    `\\s*"?` after the colon, so a leading guard could never fire, and an inert
    guard beside a live one reads as live to the next editor."""
    return re.compile(
        rf'(?<![A-Za-z0-9_])"?{re.escape(key)}"?\s*:\s*"?'
        rf'([0-9a-f]{{40}}){HEX_BOUNDARY}"?')


# WHAT A NON-COMMIT VALUE LOOKS LIKE, and why this regex is stricter about the
# KEY than `_field_re` is rather than looser about the value.
#
# `_field_re` gets away with a bare key boundary because its value group can
# only match forty hex characters, and a sentence almost never contains one in
# the position after a colon. Widen the value to "any scalar" and that safety
# net is gone: measured over this repository at 45ba637a, a naive widening
# reported two sites that are not mapping keys at all — `Live commit:path
# resolution of the five supported DomainxFactory…` inside a folded `detail: >-`
# block, and a `` `commit:` above `` inside a YAML comment. Both are PROSE
# QUOTING A KEY NAME, which is exactly the hazard `NON_MEMBERS` already excludes
# whole markdown files for.
#
# So the key must stand at a MAPPING POSITION: the start of a line (after
# indentation and any number of YAML sequence dashes) or immediately after a
# `{`, `,` or `[` — which is where a key stands in compact JSON. Comment lines
# are dropped by the callers. Both false positives fail the anchor structurally
# rather than by their value's shape, which matters because a value's shape is
# precisely what this path may not judge on.
_MAPPING_KEY_ANCHOR = r'(?:^|[{,\[])\s*(?:-\s+)*'

# The value: a quoted scalar, or a bare one running to the next separator or
# comment. `[^\s,#\]}]` for the first character keeps an empty value out and
# stops the match at a line that is only a key (`generation:`), whose value is
# the block beneath it rather than anything on the line.
_SCALAR_VALUE = (r'(?P<value>"[^"]*"|\'[^\']*\'|'
                 r'[^\s,#\]}][^,#\]}]*?)\s*(?=$|[,\]}]|\s#)')


def _wide_field_re(key: str) -> re.Pattern:
    return re.compile(_MAPPING_KEY_ANCHOR + r'"?' + re.escape(key)
                      + r'"?\s*:\s*' + _SCALAR_VALUE)


def _scalar(raw: str) -> str:
    """The value a wide match found, unquoted and untrimmed of meaning."""
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value.strip().strip("`")


def is_comment_line(line: str) -> bool:
    """A whole-line YAML comment. JSON has none, so this only ever fires on the
    serialization that has them."""
    return line.lstrip().startswith("#")


CURRENT = "current"                # committed instances carry real pins today
FUTURE = "future"                  # a schema requires the pin; no committed
                                   # instance holds a real one yet


@dataclass(frozen=True)
class PinMember:
    """One declared member of the derivation-pin class.

    `paths` are committed-path globs (`*` stops at `/`, `**` crosses it — see
    `_glob_re`). `key` is the field name, or for `key_form="prose"` the marker a
    rendered line carries. `pattern` is the regex that lifts the pin out of a
    matching line; it is derived from `key` for field members and stated
    explicitly for prose ones."""
    id: str
    paths: tuple[str, ...]
    key: str
    key_form: str                  # "field" | "prose"
    generator: str
    reproduction: str              # TOOL_DEFINED | MEASURED
    locality: str                  # REPO_LOCAL | CROSS_REPOSITORY
    presence: str                  # CURRENT | FUTURE
    note: str
    pattern: str = ""              # prose members state their own
    locality_from: tuple[str, ...] = ()
    # Whether an artifact matching this member is EXPECTED to carry the key.
    # Only meaningful for the absent-key report (`declare-sentinel-pin-
    # vocabulary`, Q2): absence is a recognized legacy state where the class
    # expects a pin, and is simply the normal shape where the key is optional.
    # Default True because every member but one writes the key unconditionally;
    # a False is a MEASUREMENT and states it.
    key_expected: bool = True

    def line_re(self) -> re.Pattern:
        if self.pattern:
            return re.compile(self.pattern)
        return _field_re(self.key)

    def value_re(self) -> re.Pattern:
        """The WIDE form of `line_re` — same key, any scalar value.

        Field members only: a prose member's pin has no field to hold a
        non-commit value, and a sentence is not a mapping. Used exclusively by
        the non-pin classification; the commit-shaped path still runs
        `line_re()` and is untouched by it."""
        return _wide_field_re(self.key)


@dataclass(frozen=True)
class NonMember:
    """A place a pin-shaped value legitimately appears without being a member.

    Declared rather than silently skipped: an exclusion nobody can read is
    indistinguishable from a coverage gap, and the reason is what a later
    reader needs in order to decide whether it still holds."""
    paths: tuple[str, ...]
    reason: str


# THE MEMBERS. Seeded from the realization's own measurement over committed
# state at `origin/main` — see the module docstring on why the packet's table is
# not the seed. Ordered by the capability that owns each artifact.
PIN_CLASS: tuple[PinMember, ...] = (
    # ---- the cross-reference index and its rendered twin -------------------
    PinMember(
        id="cross-reference-index",
        paths=("ideation/cross-reference.yaml",),
        key="source_revision",
        key_form="field",
        generator="scripts/bootstrap-ideation-cross-reference.py "
                  "(git_generation)",
        reproduction=TOOL_DEFINED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="`generation.source_revision`. The one member whose reproduction "
             "is byte-comparable today: the bootstrap re-derives the body and "
             "the strict index validator checks it, which is the mechanism "
             "`harden-ideation-readiness-check` used to prove its own re-pin "
             "at three revisions.",
    ),
    PinMember(
        id="cross-reference-rendered",
        paths=("ideation/cross-reference.md",),
        key="Source revision",
        key_form="prose",
        generator="scripts/bootstrap-ideation-cross-reference.py (renderer)",
        reproduction=TOOL_DEFINED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="THE PROSE MEMBER a key-name scanner misses. The pin is the "
             "rendered line `- Source revision: `<sha>``, in a markdown "
             "projection of the yaml index; it must agree with its twin.",
        # `HEX_BOUNDARY`: a prose member's own pattern builds a site, so it
        # carries the whole-object-name guard exactly as the field forms do.
        pattern=r"Source revision:\s*`?([0-9a-f]{40})" + HEX_BOUNDARY + r"`?",
    ),
    # ---- immutable derivation and readiness evidence -----------------------
    PinMember(
        id="ideation-readiness-run",
        paths=("health/ideation-readiness/*/*.yaml",),
        key="source_revision",
        key_form="field",
        generator="the readiness lane (doc_health.ideation_readiness)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="`status: record`, so an orphaned pin here is repaired by "
             "RETENTION and never by editing the record (requirement 2). Two "
             "of this repository's three orphans are these records, and both "
             "now resolve through the retention namespace with their original "
             "pins UNEDITED.",
    ),
    PinMember(
        id="derive-possibles-run",
        paths=("health/derive-possibles/*/*.yaml",),
        key="source_revision",
        key_form="field",
        generator="the possibles-derivation lane "
                  "(doc_health.derive_possibles)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="`status: record`; same repair route as the readiness records.",
    ),
    # ---- the dashboard gate console ---------------------------------------
    PinMember(
        id="gate-transition-manifest",
        paths=("ideation/dashboard/gate-records/**/*.transition-manifest.yaml",),
        key="source_revision",
        key_form="field",
        generator="the dashboard gate console "
                  "(scripts/ideation_dashboard, transition manifests)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="The manifest records the revision a promotion or demotion moved "
             "files at. Nothing re-derives it, so a re-pin owes a named "
             "measurement rather than bytes.",
    ),
    PinMember(
        id="gate-action-record",
        paths=("ideation/dashboard/gate-records/**/*.gate-action.yaml",),
        key="source_revision (inside a prose `notes:` / `recipe:` string)",
        key_form="prose",
        generator="the dashboard gate console (gate-action records)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="THE SECOND PROSE MEMBER, and the wrinkle that forced the class "
             "to be declared: the pin has no field of its own — it sits in a "
             "sentence, `… recipe: checked none · pinned none · at "
             "source_revision <sha>`. One of the 25 committed gate-action "
             "records carries one today.",
        # `HEX_BOUNDARY`: see the sibling prose member above.
        pattern=r"source_revision\s+`?([0-9a-f]{40})" + HEX_BOUNDARY + r"`?",
    ),
    # ---- spec traceability -------------------------------------------------
    PinMember(
        id="spec-traceability",
        paths=("specs/*/traceability.yaml",),
        key="source_revision",
        key_form="field",
        generator="the spec traceability lane",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="Four traceability files are committed; one carries a pin.",
        # MEASURED at 45ba637a rather than assumed, because the absent-key
        # report is only honest where the key is genuinely expected. Three
        # traceability files are committed and ONE carries `source_revision`
        # (008), where it sits inside an optional per-feature verification
        # block rather than at the top level; 007 and 009 have no such block at
        # all, and no schema requires the key. So absence here is the normal
        # shape of the artifact, not a legacy state of the corpus, and
        # reporting it would be the launch noise the seeding clause warns
        # against.
        key_expected=False,
    ),
    # ---- the proposal-support transition tool ------------------------------
    PinMember(
        id="proposal-support-manifest",
        paths=("openspec/changes/*/supporting-docs.manifest.yaml",
               "openspec/changes/*/supporting-docs/*manifest.yaml",
               "openspec/changes/archive/*/supporting-docs.manifest.yaml",
               "openspec/changes/archive/*/supporting-docs/*manifest.yaml"),
        key="source_revision",
        key_form="field",
        generator="the proposal-support transition tool "
                  "(scripts/proposal_support)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="THE GENERATOR FAMILY THE PACKET'S SWEEP MISSED ENTIRELY — 31 "
             "committed manifests, the largest member of the class, and the "
             "carrier of this repository's THIRD orphaned pin "
             "(74022ea5, at 2026-08-22-add-doxbench-editing-phase-b, retained "
             "2026-08-27 at realization). A manifest inside an ARCHIVED packet "
             "is not editable and nothing re-derives it, so retention is its "
             "only route too.",
    ),
    # ---- the avatar-client kernel and its lab ------------------------------
    PinMember(
        id="avatar-client-f0-pin",
        paths=("contracts/avatar-client/interface-lock.yaml",
               "contracts/avatar-client/kernel-handoff.yaml"),
        key="f0_source_commit",
        key_form="field",
        generator="the avatar-client kernel realization "
                  "(F0 publication gate)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="The commit F0 published its evidence schemas at. Repo-local: "
             "the F0 change lives in this repository.",
    ),
    PinMember(
        id="avatar-client-f0-evidence",
        paths=("openspec/changes/*/evidence/f0-*.yaml",
               "openspec/changes/*/evidence/f0-*.json",
               "openspec/changes/archive/*/evidence/f0-*.yaml",
               "openspec/changes/archive/*/evidence/f0-*.json"),
        key="source_commit",
        key_form="field",
        generator="the F0 feasibility evidence lane",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="The F0 results and interface-impact records each pin the commit "
             "they were taken at.",
    ),
    PinMember(
        id="avatar-client-lab-transcription",
        paths=("contracts/avatar-client-lab/capability-scenario-register.yaml",),
        key="openxfactory_commit",
        key_form="field",
        generator="the avatar-client-lab transcription "
                  "(read-only consult of a spec delta)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="`source.openxfactory_commit` — the commit a verbatim "
             "transcription was taken from.",
    ),
    PinMember(
        id="avatar-client-lab-delta-touch",
        paths=("contracts/avatar-client-lab/capability-scenario-register.yaml",),
        key="spec_delta_last_touched_commit",
        key_form="field",
        generator="the avatar-client-lab transcription",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="`source.spec_delta_last_touched_commit` — the second pin in the "
             "same file, which is why a member is a (path, key) pair rather "
             "than a path.",
    ),
    # ---- cross-factory ideation routing -----------------------------------
    PinMember(
        id="ideation-routing-source",
        paths=("ideation/brainstorm/**/routing.yaml",),
        key="revision",
        key_form="field",
        generator="the cross-factory ideation routing capture",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="Every routing record's `sources[].revision`, "
             "`destination.revision` and `evidence_refs[].revision` pins the "
             "commit a cited passage was read at, and each names its own "
             "`repository:` beside it — a hub record routing a Ledgerx "
             "brainstorm pins LEDGERX commits. So locality is read PER SITE "
             "out of the artifact; five of the eleven sites committed today "
             "are cross-repository and must not be answered against this "
             "repository's refs.",
        locality_from=("repository",),
    ),
    # ---- the hermes-runtime contract handoff ------------------------------
    PinMember(
        id="hermes-consumer-handoff-provider",
        paths=("openspec/changes/*/evidence/hermes-install-g0-handoff.yaml",
               "openspec/changes/archive/*/evidence/"
               "hermes-install-g0-handoff.yaml"),
        key="commit",
        key_form="field",
        generator="the hermes-runtime consumer handoff receipt",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="`provider.commit`, repo-local because `provider.repository` IS "
             "this repository — read out of the artifact rather than asserted. "
             "The receipt's `consumer_commit` in the same file is "
             "CROSS-REPOSITORY and is declared separately below: ONE FILE, TWO "
             "LOCALITIES, which is the case the delta's locality clause exists "
             "for.",
        locality_from=("repository",),
    ),
    PinMember(
        id="hermes-provider-verification-contract-ref",
        paths=("openspec/changes/*/evidence/provider-verification.yaml",
               "openspec/changes/archive/*/evidence/"
               "provider-verification.yaml"),
        key="expected_contract_ref",
        key_form="field",
        generator="the hermes-runtime provider verification lane",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="The openxFactory commit every domain's stack was verified "
             "against.",
    ),
    PinMember(
        id="hermes-provider-verification-us3-baseline",
        paths=("openspec/changes/*/evidence/provider-verification.yaml",
               "openspec/changes/archive/*/evidence/"
               "provider-verification.yaml"),
        key="us3_baseline_commit",
        key_form="field",
        generator="the hermes-runtime provider verification lane "
                  "(the US3 checkpoint baseline)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="THE KEY THE VOCABULARY DID NOT KNOW, and the reason a renamed "
             "key is a coverage hole rather than an inconvenience: this pin "
             "was invisible to the packet's sweep AND to this module's first "
             "draft, because the generator spelled `commit` with a prefix "
             "nobody had enumerated. It is the class's ONE UNRECOVERABLE "
             "orphan — see KNOWN_LOSSES, which carries the measurement and the "
             "governance act still owed.",
    ),
    # ---- declared CROSS-REPOSITORY members --------------------------------
    # Not verified against this repository's refs. Declared anyway, because an
    # undeclared cross-repository pin and an uncovered repo-local one look
    # identical to a sweep, and the delta requires the declaration to
    # distinguish them.
    PinMember(
        id="omnigent-install-source-compatibility",
        paths=("contracts/manifest.yaml",),
        key="source_commit",
        key_form="field",
        generator="the contract bundle release "
                  "(source_compatibility_ref)",
        reproduction=MEASURED,
        locality=CROSS_REPOSITORY,
        presence=CURRENT,
        note="`source_compatibility_ref.source_commit`, whose sibling key "
             "says `repo: opensoft/Omnigent-Install`. Answered against that "
             "remote by that repository's authority; this pin does not resolve "
             "here and must not be reported as an orphan.",
    ),
    PinMember(
        id="hermes-consumer-handoff-consumer",
        paths=("openspec/changes/*/evidence/hermes-install-g0-handoff.yaml",
               "openspec/changes/archive/*/evidence/"
               "hermes-install-g0-handoff.yaml"),
        key="consumer_commit",
        key_form="field",
        generator="the hermes-runtime consumer handoff receipt",
        reproduction=MEASURED,
        locality=CROSS_REPOSITORY,
        presence=CURRENT,
        note="`consumer_repository: opensoft/xFactory-Hermes-Install`.",
    ),
    PinMember(
        id="hermes-provider-verification-domain",
        paths=("openspec/changes/*/evidence/provider-verification.yaml",
               "openspec/changes/archive/*/evidence/"
               "provider-verification.yaml"),
        key="commit",
        key_form="field",
        generator="the hermes-runtime provider verification lane",
        reproduction=MEASURED,
        locality=CROSS_REPOSITORY,
        presence=CURRENT,
        note="`domains[].commit`, each beside its own `repository:` naming a "
             "DomainxFactory. Seven sites today; locality is read per site so "
             "an openxFactory row in the same list would be verified here.",
        locality_from=("repository",),
    ),
    PinMember(
        id="neutrality-drift-baseline",
        paths=("health/neutrality-drift/baseline/*.yaml",
               "health/neutrality-drift/baseline/*.json"),
        key="commit",
        key_form="field",
        generator="the neutrality-drift lane's baseline record",
        reproduction=MEASURED,
        locality=CROSS_REPOSITORY,
        presence=CURRENT,
        note="THE SITE THE FIRST REAL-REPOSITORY RUN FOUND UNCOVERED, which is "
             "the coverage half of requirement 4 working on its first outing "
             "rather than in a fixture: `status: record`, `repo: codexFactory`, "
             "and a `commit:` naming that repository's post-shed tip. Locality "
             "is read from the artifact's own `repo:` key, so an openxFactory "
             "baseline landing here would be verified against this "
             "repository's refs.",
        locality_from=("repo", "repository"),
    ),
    # ---- the neutral-product pin: ONE artifact, TWO localities -------------
    # `contracts/openxwallet-pin.yaml` (split-openxwallet-repo P3) is the first
    # artifact in this repository that pins ANOTHER repository's bytes and, in
    # the same file, names the openxFactory commit those bytes were taken at. So
    # it is TWO members rather than one, and the split is not cosmetic: one of
    # the two values must resolve here and the other must never be expected to.
    # A single member could only have declared one locality, and whichever it
    # declared would have made the other value either a false orphan or an
    # unverified pin.
    PinMember(
        id="openxwallet-pin-carve-commit",
        paths=("contracts/openxwallet-pin.yaml",),
        key="carve_commit",
        key_form="field",
        generator="authored with the pin (split-openxwallet-repo P3, feature "
                  "023-openxwallet-consume-shed)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=CURRENT,
        note="THE NAMED CARVE COMMIT — an openxFactory commit, and the one "
             "value in this file that MUST stay reachable here. It is the "
             "byte-identity referent for the whole extraction: the eight "
             "`sha256` digests below it are the values `contracts/manifest.yaml` "
             "recorded AT THIS COMMIT, and the claim that the move was "
             "byte-identical is checkable only while the commit can be "
             "reconstructed. `carve_commit` was a key this vocabulary did not "
             "know; declaring the member is what teaches it, since "
             "`PIN_KEY_VOCABULARY` is the union of the declared field keys.",
    ),
    PinMember(
        id="openxwallet-pin-product-commit",
        paths=("contracts/openxwallet-pin.yaml",),
        key="commit",
        key_form="field",
        generator="authored with the pin (split-openxwallet-repo P3, feature "
                  "023-openxwallet-consume-shed)",
        reproduction=MEASURED,
        locality=CROSS_REPOSITORY,
        presence=CURRENT,
        note="`source_repository: opensoft/openXwallet` — the PINNED PRODUCT'S "
             "commit, at tag label `wallet-v1.1`. It does not resolve in this "
             "repository and must not be reported as an orphan; it is answered "
             "by openXwallet's own authority and, locally, by "
             "`scripts/verify-openxwallet-pin.py`, which compares it against "
             "BOTH the recorded gitlink and the checked-out revision of the "
             "`openXwallet/` submodule and recomputes the eight digests. That "
             "verifier is a stronger reachability guarantee than a ref here "
             "could give, which is why the cross-repository declaration is not "
             "a gap. Locality is declared on the member rather than read per "
             "site: this key is ALWAYS the product's, and `carve_commit` above "
             "is ALWAYS this repository's.",
    ),
    # ---- the pinned decision core: executable governance, not a bundle -----
    # `contracts/review-lane-pin.yaml` (feature 025-openxfactory-review-lane-caller)
    # pins the codexFactory commit whose Merge Master decision core judges this
    # repository's pull requests. ONE member, not two: unlike the neutral-product
    # pin above, this file carries exactly ONE commit-shaped value, and the test
    # for that feature asserts it stays exactly one — the diverging xFactory pin
    # is named in the caller's header comment instead, because `.github/` is
    # outside SCAN_ROOTS while `contracts/**` is inside them.
    PinMember(
        id="review-lane-pin-core-commit",
        paths=("contracts/review-lane-pin.yaml",),
        key="core_commit",
        key_form="field",
        generator="authored with the pin (add-substantive-review-lane task 5.1, "
                  "feature 025-openxfactory-review-lane-caller)",
        reproduction=MEASURED,
        locality=CROSS_REPOSITORY,
        presence=CURRENT,
        note="`repository: opensoft/codexFactory` — the DECISION CORE'S commit. "
             "It does not resolve in this repository and must not be reported "
             "as an orphan; codexFactory answers for it, and locally "
             "`.github/workflows/merge-master-approval.yml` compares this "
             "recorded value against BOTH its own literal `ref:` and the commit "
             "`actions/checkout` actually produced, refusing the run on any "
             "disagreement. What is pinned is EXECUTABLE GOVERNANCE rather than "
             "contract bytes, so there is no digest set to check and the commit "
             "is the whole referent. `core_commit` was a key this vocabulary "
             "did not know, and it is deliberately not `commit`: that name is "
             "already bound to `openxwallet-pin-product-commit` above, so "
             "reusing it here would have left this site UNCOVERED. Declaring "
             "the member is what teaches the key, since `PIN_KEY_VOCABULARY` is "
             "the union of the declared field keys.",
    ),
    # ---- FUTURE members: schema-declared, no committed real pin yet --------
    # Declared now rather than on discovery. The day the first instance lands
    # committed its pins join the class automatically, which is precisely the
    # case the declaration exists to catch: nobody will remember to add them.
    PinMember(
        id="ideation-dashboard-snapshot",
        paths=("health/ideation-dashboard/*snapshot.json",
               "health/ideation-dashboard/*snapshot.yaml"),
        key="source_revision",
        key_form="field",
        generator="the ideation dashboard snapshot builder",
        reproduction=TOOL_DEFINED,
        locality=REPO_LOCAL,
        presence=FUTURE,
        note="`contracts/schemas/ideation-dashboard-snapshot.schema.yaml` "
             "REQUIRES `generation.source_revision`. No committed instance "
             "today; the only instances are examples.",
    ),
    PinMember(
        id="ideation-dashboard-snapshot-index",
        paths=("health/ideation-dashboard/*snapshot-index.json",
               "health/ideation-dashboard/*snapshot-index.yaml"),
        key="source_revision",
        key_form="field",
        generator="the ideation dashboard snapshot index builder",
        reproduction=TOOL_DEFINED,
        locality=REPO_LOCAL,
        presence=FUTURE,
        note="`ideation-dashboard-snapshot-index.schema.yaml` requires a "
             "`source_revision` per entry, and derives each entry's "
             "`generated_at` from that revision's commit date — so an "
             "unreachable pin there loses a timestamp as well as a provenance "
             "claim.",
    ),
    PinMember(
        id="ideation-workbench",
        paths=("ideation/workbench/**/*.yaml",
               "ideation/workbench/**/*.json"),
        key="source_revision",
        key_form="field",
        generator="the ideation workbench",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=FUTURE,
        note="`ideation-workbench.schema.yaml` requires `source_revision` on a "
             "seeded recipe — the snapshot revision the recipe was last "
             "evaluated against.",
    ),
    PinMember(
        id="organizer-recommendations",
        paths=("health/ideation-organizer/**/*.yaml",),
        key="source_revision",
        key_form="field",
        generator="the ideation organizer lane "
                  "(doc_health.organizer)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=FUTURE,
        note="`xfactory-ideation-organizer-recommendations.schema.yaml` lists "
             "`source_revision` as required.",
    ),
    PinMember(
        id="gate-intent-snapshot-rev",
        paths=("ideation/dashboard/intents/**/*.yaml",),
        key="snapshot_rev_seen",
        key_form="field",
        generator="the dashboard gate console (gate intents)",
        reproduction=MEASURED,
        locality=REPO_LOCAL,
        presence=FUTURE,
        note="`gate-intent.schema.yaml` carries `snapshot_rev_seen` for "
             "optimistic concurrency. It pins repository state like every "
             "other member, so it is declared; no committed instance today.",
    ),
)


# WHERE A SUPERSESSION RECORD STANDS. One filename, in the packet that issues
# it, resolvable both before and after that packet archives — the same live-plus-
# archive glob pair every hermes evidence member above is declared with, because
# a citation that breaks when the packet archives is not a citation.
SUPERSESSION_RECORD_PATHS: tuple[str, ...] = (
    "openspec/changes/*/evidence/pin-loss-supersession.yaml",
    "openspec/changes/archive/*/evidence/pin-loss-supersession.yaml",
)


@dataclass(frozen=True)
class KnownLoss:
    """A repo-local pin whose object is UNRECOVERABLE, measured and declared.

    Requirement 2's other branch. Where an orphaned commit still exists
    somewhere, retention repairs it and the row does not belong here. Where it
    exists nowhere, the record's bytes still stand and no repair is available at
    all: the resolution is a SUPERSEDING RECORD naming the loss and what can no
    longer be verified, plus a disposition for the standing finding. Until that
    governance act lands, the honest report is "this pin is orphaned, the object
    is gone, and here is what was measured" — not silence, and not a red on a
    condition nobody can fix from a code change.

    `owed` names the act still outstanding. `measured` is the evidence, and it
    is RE-MEASURED by test: the day the object turns out to be recoverable, this
    row is stale and retention is the route, so the test fails and says so.

    A ROW IS NEVER DELETED AND NEVER SILENCED. `superseding_record` names where
    the discharging record stands — path globs, live and archived, so the
    citation survives its packet's archive — and `discharged` states what that
    record established. Both are read rather than believed: `discharging_record`
    goes to committed state, finds the record at one of those paths, and
    requires it to NAME the lost pin, so a citation of a record nobody committed
    discharges nothing. A discharged loss still reports LOST with its full
    measurement; what changes is that the class stops calling itself
    incompletely verified over an obligation somebody has since met
    (`supersede-lost-pin-baseline`, 2026-08-27)."""
    pin: str
    path: str
    key: str
    measured: str
    owed: str
    superseding_record: tuple[str, ...] = ()
    discharged: str = ""


KNOWN_LOSSES: tuple[KnownLoss, ...] = (
    KnownLoss(
        pin="66b14064bbd50d1af4e9585d10f8150f2bc352f0",
        path="openspec/changes/archive/2026-08-27-add-hermes-customer-subject-"
             "runtime-contract/evidence/provider-verification.yaml",
        key="us3_baseline_commit",
        measured="2026-08-27, at origin/main. `git cat-file -t` fails in the "
                 "shared aggregation object store; the pin appears in NONE of "
                 "the 566 refs `git ls-remote origin` advertises (403 of them "
                 "`refs/pull/*`); and `git fetch origin "
                 "66b14064bbd50d1af4e9585d10f8150f2bc352f0` is refused by the "
                 "server with `upload-pack: not our ref`, which is the "
                 "strongest available statement that the remote cannot reach "
                 "it either. The branch it was taken on, "
                 "`005-customer-subject-runtime`, is gone from the remote. "
                 "Retention is therefore IMPOSSIBLE rather than merely not yet "
                 "performed.",
        owed="A superseding evidence record for "
             "`add-hermes-customer-subject-runtime-contract` naming the loss "
             "and what is no longer verifiable at that baseline, plus a "
             "disposition for the standing finding. Both are governance acts "
             "with a named authority; neither is a code change, and this "
             "realization deliberately performs neither. The record's own note "
             "argues the pin is not load-bearing for it — \"Evidence is bound "
             "to canonical content, not to its own commit\" — which is exactly "
             "the claim a superseding record should state and cite rather than "
             "leave in a comment.",
        superseding_record=(
            "openspec/changes/supersede-lost-pin-baseline/evidence/"
            "pin-loss-supersession.yaml",
            "openspec/changes/archive/*-supersede-lost-pin-baseline/evidence/"
            "pin-loss-supersession.yaml"),
        discharged="SUPERSEDED 2026-08-27 by `supersede-lost-pin-baseline`, "
                   "commissioned by Brett that day. THE MEASUREMENT ABOVE WAS "
                   "RE-RUN BEFORE THE RECORD WAS WRITTEN and its answer did not "
                   "move: 0 matches, now across 573 advertised refs rather than "
                   "566, the remote having gained seven refs in a day. THE "
                   "OBJECT IS STILL GONE "
                   "and this row stays declared and re-measured; what the "
                   "record supplies is the standing the archived evidence "
                   "keeps without it, and the NAMED MEASUREMENT that "
                   "establishes it. The US3 checkpoint's CONTENT survives "
                   "under a rewritten object name — "
                   "`8f7c99f0db065fb153b7d9498eb1e16b3c3c306b`, an ancestor of "
                   "`main` and the parent of "
                   "`e8ae366cda7b5814b73942891837175b5c43d929`, the commit "
                   "that added the record — and the identification is "
                   "corroborated by all three counts the record itself states "
                   "against its baseline, each re-measured at both commits: "
                   "catalog members 34 -> 39, schema members 27 -> 32, fixture "
                   "cases 79 -> 110. What is permanently lost is the OBJECT "
                   "NAME the record carries, so no reader can prove tree "
                   "equality against it; the equivalence is corroboration, and "
                   "the record says so rather than claiming recovery.",
    ),
)


def known_loss(pin: str) -> KnownLoss | None:
    for row in KNOWN_LOSSES:
        if row.pin == pin:
            return row
    return None


def discharging_record(repo, rev: str, loss: KnownLoss, *,
                       paths: list[str] | None = None) -> str | None:
    """The committed superseding record that DISCHARGES `loss`, or None.

    MEASURED, NEVER TRUSTED, and that is the whole point of reading committed
    state here rather than believing the row. The row names where the record
    stands; this goes and looks, at the revision under test, and additionally
    requires the record to NAME the pin it claims to supersede. So a row citing
    a record nobody committed, a record deleted later, or a stub that never
    mentions the lost object discharges nothing, and the loss keeps holding
    `fully_verified` open — which is the same reasoning that makes the loss
    itself re-measured rather than declared once and believed."""
    if not loss.superseding_record:
        return None
    paths = paths if paths is not None else committed_paths(repo, rev)
    for path in sorted(paths):
        if not path_matches(path, loss.superseding_record):
            continue
        text = committed_text(repo, rev, path)
        if text is not None and loss.pin in text:
            return path
    return None


# WHERE THE COVERAGE SWEEP LOOKS. Governance artifacts live under these roots;
# a pin-shaped value anywhere in them is a candidate site.
SCAN_ROOTS: tuple[str, ...] = (
    "ideation/**", "health/**", "specs/**", "contracts/**", "openspec/**",
)

# ...and in which serializations. A pin recorded as a FIELD is recorded in one
# of these; markdown is prose (see NON_MEMBERS) and everything else in the scan
# roots is either a binary blob or a script, neither of which is an artifact
# making a provenance claim about itself.
SCAN_SUFFIXES: tuple[str, ...] = (".yaml", ".yml", ".json")

# WHAT THE SWEEP LOOKS FOR. The union of every declared field key plus the
# sibling names a generator might plausibly reach for — the packet's own sweep
# vocabulary, kept so a renamed key still lands as an UNCOVERED site rather
# than as silence.
PIN_KEY_VOCABULARY: tuple[str, ...] = tuple(sorted({
    *(m.key for m in PIN_CLASS if m.key_form == "field"),
    "source_revision", "source_commit", "source_rev", "source_ref",
    "corpus_revision", "revision", "commit", "commit_sha", "base_commit",
    "pinned_commit", "head_commit", "git_commit", "derived_from",
    "generated_from", "contract_ref", "snapshot_rev_seen",
    # Added on evidence, not on speculation: `us3_baseline_commit` is a real
    # committed pin this vocabulary did not know, found by enumerating every key
    # name that carries a 40-hex value in committed structured state rather than
    # by guessing which names a generator might pick. That enumeration is the
    # honest way to seed this tuple and is pinned by test.
    "us3_baseline_commit",
}))

# `HEX_BOUNDARY` on the value for the same reason `_field_re` carries it: this
# is a SITE-BUILDING expression, and a longer hexadecimal run under a
# vocabulary key must fail to match here rather than yield a truncated prefix.
_VOCAB_RE = re.compile(
    r'(?<![A-Za-z0-9_])"?(' + "|".join(re.escape(k) for k in sorted(
        PIN_KEY_VOCABULARY, key=len, reverse=True))
    + r')"?\s*:\s*"?([0-9a-f]{40})' + HEX_BOUNDARY + r'"?')

# The same key set with the value widened, for the non-commit classification.
# Its key anchor is the mapping-position one rather than `_VOCAB_RE`'s bare
# boundary — see `_MAPPING_KEY_ANCHOR` for the two prose sites that measured
# that difference into existence.
_WIDE_VOCAB_RE = re.compile(
    _MAPPING_KEY_ANCHOR + r'"?(?P<key>' + "|".join(
        re.escape(k) for k in sorted(PIN_KEY_VOCABULARY, key=len, reverse=True))
    + r')"?\s*:\s*' + _SCALAR_VALUE)


# WHAT THE SWEEP DELIBERATELY DOES NOT TREAT AS A MEMBER. Each row states its
# reason, because an exclusion nobody can read is a coverage gap in disguise.
NON_MEMBERS: tuple[NonMember, ...] = (
    NonMember(
        paths=("**/examples/**", "examples/**", "**/*.example.yaml",
               "**/*.example.yml", "**/*.example.json"),
        reason="instantiation stubs and sample data. Some carry values copied "
               "from real records and therefore resolve, which is exactly why "
               "they must be excluded by DECLARATION rather than by whether "
               "they happen to resolve: an example is not an artifact making a "
               "provenance claim about itself.",
    ),
    NonMember(
        paths=("**/*.template.yaml", "**/*.template.yml",
               "**/*.template.json"),
        reason="INSTANTIATION TEMPLATES — the same category as the examples "
               "above, and declared here on evidence rather than by analogy. "
               "Three are committed inside the scan roots and none carries a "
               "forty-character value, so this row is inert for the "
               "reachability sweep; what it excludes is a non-commit value, "
               "and one is committed: `document-catalog.template.yaml:42` "
               "holds `revision: <current full commit>`, a placeholder telling "
               "an instantiator what to write. A template is not an artifact "
               "making a provenance claim about itself, its placeholder names "
               "no condition so it cannot be declared a sentinel, it has no "
               "generator to correct, and it sits inside an archived packet so "
               "its bytes may not be edited — the declaration is the only "
               "route the seeding obligation leaves open, and it is the same "
               "route the examples row already takes.",
    ),
    NonMember(
        paths=("**/negative/**", "**/*.negative.yaml", "**/*.negative.yml",
               "**/*.negative.json"),
        reason="negative-case sample data, deliberately invalid.",
    ),
    NonMember(
        paths=("**/fixtures/**", "tests/**"),
        reason="test fixtures. Their pins are synthetic (`dddd…`, `1111…`) or "
               "frozen sample data; a fixture is the subject of a test, not a "
               "record of a derivation.",
    ),
    NonMember(
        paths=("contracts/schemas/**",),
        reason="schemas DECLARE the keys; they carry no pins of their own. A "
               "schema whose required `source_revision` has no committed "
               "instance yet is a FUTURE member above, not a site here.",
    ),
    NonMember(
        paths=("contracts/review-lane-floor-snapshot.yaml",),
        reason="A VENDORED BYTE COPY OF ANOTHER REPOSITORY'S DOCUMENT — "
               "codexFactory's `openxfactory-review-authority-floor.yaml` at "
               "the commit `contracts/review-lane-pin.yaml` pins, carried here "
               "so a REQUIRED check can assert this repository's promoted "
               "OpenSpec canon against it offline. Its generated block's "
               "header carries `generated_at`, an openxFactory commit that "
               "DOES resolve here, which is exactly why the exclusion must be "
               "DECLARED rather than left to whether it resolves — the same "
               "ground the examples row states. Two facts make a member the "
               "wrong answer, both measured. (1) The generator writes that "
               "value into a YAML COMMENT: the commit-shaped pass reads every "
               "line and finds it, the non-commit pass skips comment lines by "
               "design and does not, so one member classifies this file twice. "
               "(2) `PIN_KEY_VOCABULARY` is the union of declared field keys, "
               "so declaring `generated_at` widens the sweep over 21 files in "
               "the scan roots whose `generated_at` is an ISO timestamp. And "
               "the file may not be edited to suit either pass: it is a "
               "witness, verified byte for byte, and an edited witness proves "
               "nothing. THE PROVENANCE IS NOT UNGUARDED. "
               "`contracts/review-lane-pin.yaml` declares the copy's `sha256` "
               "and `tests/review_lane_pin/test_floor_snapshot.py` compares "
               "the bytes to the authoritative document whenever the pinned "
               "core is on disk — a stronger guarantee than a reachability "
               "verdict, since a drifted `generated_at` could only arrive "
               "inside bytes that failed both. The claim this file makes is "
               "codexFactory's, not this repository's about itself, which is "
               "the line every row here draws.",
    ),
    NonMember(
        paths=("**/*.schema.yaml", "**/*.schema.yml", "**/*.schema.json"),
        reason="THE SAME REASON AS THE ROW ABOVE, AT THE PATHS THAT ROW'S GLOB "
               "DOES NOT REACH — and found by measurement rather than by "
               "tidiness. 114 committed schema files sit inside the scan roots "
               "outside `contracts/schemas/`, and the widened value check "
               "reported one of them: "
               "`specs/002-avc-f0-feasibility/contracts/"
               "f0-interface-impact.schema.yaml:34` holds `source_commit: "
               "{type: string, minLength: 1}`, which is a key DECLARATION in "
               "JSON-Schema and not a value at all. A schema states what a pin "
               "must look like; it never makes a derivation claim about "
               "itself. Inert for the reachability sweep — no committed schema "
               "in the scan roots carries a forty-character value — so this "
               "row only ever excludes a type declaration being read as a "
               "spelling.",
    ),
    NonMember(
        paths=("**/*.md",),
        reason="PROSE, and the one line this module cannot draw mechanically. "
               "Governance prose quotes pins constantly — a proposal narrating "
               "a landing, a migration-evidence file listing twelve manifests, "
               "an archive record naming a merge commit — and none of those is "
               "the quoting file's own derivation claim. A markdown file that "
               "genuinely carries its own pin is DECLARED "
               "(`ideation/cross-reference.md` is the one today) and verified "
               "like any other member. THE TRADE IS STATED: a future markdown "
               "projection that pins its source and is never declared would go "
               "unswept, where a yaml one would be caught. That is the cost of "
               "prose being unparseable, and it is the reason the class is a "
               "declaration in the first place.",
    ),
    NonMember(
        paths=("openspec/changes/*/.openspec.yaml",
               "openspec/changes/archive/*/.openspec.yaml"),
        reason="origin declarations. Their `reason` fields narrate the acts "
               "that created a change and quote pins as evidence — the "
               "`govern-derived-pin-reachability` origin block quotes both "
               "readiness orphans. A quotation of a pin is not a pin.",
    ),
    NonMember(
        paths=SUPERSESSION_RECORD_PATHS,
        reason="PIN-LOSS SUPERSESSION RECORDS, whose SUBJECT is a pin. Such a "
               "record exists to name a commit declared unrecoverable, to say "
               "what can and cannot still be verified without it, and to cite "
               "the surviving state a named measurement identified — so every "
               "pin-shaped value in one is a citation of another artifact's "
               "derivation claim, and none is the record's own. DECLARED here "
               "rather than dodged by choosing a key nobody enumerated, which "
               "is the coverage hazard `us3_baseline_commit` already proved: a "
               "pin-shaped value in a swept root is declared as a member or as "
               "a non-member with a reason, or it is a silent gap. THE TRADE "
               "IS STATED: a supersession record makes no derivation claim "
               "about itself today, and a future one that did would go "
               "unswept here.",
    ),
)


# --------------------------------------------------------------- glob matching

def _glob_re(glob: str) -> re.Pattern:
    """POSIX-path glob -> regex, with `**` crossing separators and `*` not.

    Written out rather than delegated to `fnmatch`, whose `*` crosses `/` — so
    `openspec/changes/*/evidence/f0-*.yaml` would silently match an arbitrarily
    deep path there and a member's scope would be wider than it reads."""
    out, i = ["^"], 0
    while i < len(glob):
        ch = glob[i]
        if glob.startswith("**/", i):
            out.append(r"(?:[^/]+/)*")
            i += 3
        elif glob.startswith("**", i):
            out.append(r".*")
            i += 2
        elif ch == "*":
            out.append(r"[^/]*")
            i += 1
        elif ch == "?":
            out.append(r"[^/]")
            i += 1
        else:
            out.append(re.escape(ch))
            i += 1
    out.append("$")
    return re.compile("".join(out))


_GLOB_CACHE: dict[str, re.Pattern] = {}


def path_matches(path: str, globs) -> bool:
    for glob in globs:
        pat = _GLOB_CACHE.get(glob)
        if pat is None:
            pat = _GLOB_CACHE[glob] = _glob_re(glob)
        if pat.match(path):
            return True
    return False


def non_member_reason(path: str) -> str | None:
    """The declared reason `path` is not swept, or None if it is swept."""
    for row in NON_MEMBERS:
        if path_matches(path, row.paths):
            return row.reason
    return None


# ------------------------------------------------- per-site locality, read out
# of the artifact where the artifact itself declares it

_REPOSITORY_VALUE_RE = re.compile(
    r'(?<![A-Za-z0-9_])"?(?P<key>[A-Za-z0-9_]+)"?\s*:\s*"?(?P<value>[^"\s,]+)"?')


def _key_indent(line: str) -> int:
    """The column a mapping key starts at, counting a YAML sequence dash as
    part of the indentation — `  - repository: x` and `    revision: y` are
    siblings in the same mapping and both answer 4."""
    stripped = line.lstrip(" ")
    indent = len(line) - len(stripped)
    if stripped.startswith("- "):
        return indent + 2
    return indent


def _is_item_start(line: str) -> bool:
    return line.lstrip(" ").startswith("- ")


def _block_range(lines: list[str], idx: int) -> range:
    """The mapping block `lines[idx]` belongs to.

    Bounded by the first shallower line in each direction, and — going down —
    by the next sequence item at the same depth, so a pin in one list entry
    never reads the NEXT entry's `repository:`. That boundary is the whole
    reason this is a block walk rather than a file-wide search: a routing record
    lists several entries whose repositories differ, and answering with the
    wrong one would report a domain repository's commit against this
    repository's refs."""
    depth = _key_indent(lines[idx])
    lo = idx
    while lo - 1 >= 0:
        prev = lines[lo - 1]
        if not prev.strip() or prev.lstrip().startswith("#"):
            lo -= 1
            continue
        if _key_indent(prev) < depth:
            break
        lo -= 1
        if _key_indent(prev) == depth and _is_item_start(prev):
            break                      # this line OPENS the entry
    hi = idx
    while hi + 1 < len(lines):
        nxt = lines[hi + 1]
        if not nxt.strip() or nxt.lstrip().startswith("#"):
            hi += 1
            continue
        if _key_indent(nxt) < depth:
            break
        if _key_indent(nxt) == depth and _is_item_start(nxt):
            break                      # the NEXT entry begins
        hi += 1
    return range(lo, hi + 1)


def site_locality(member: PinMember, lines: list[str], idx: int
                  ) -> tuple[str, str]:
    """`(locality, why)` for one pin site.

    Most members are wholly repo-local or wholly cross-repository and say so.
    Some artifacts declare it PER ENTRY — a routing record's `sources[]` and
    `evidence_refs[]` name a `repository:` beside each `revision:`, a neutrality
    baseline names a `repo:` beside its `commit:` — and for those the member
    declares `locality_from` and the answer is read out of the artifact instead
    of guessed. That is the delta's locality clause implemented where the truth
    actually lives: one file can carry both kinds, and the hermes handoff
    receipt does."""
    if not member.locality_from:
        return member.locality, "declared on the class member"
    depth = _key_indent(lines[idx])
    for i in _block_range(lines, idx):
        if _key_indent(lines[i]) != depth:
            continue
        found = _REPOSITORY_VALUE_RE.search(lines[i])
        if found is None or found.group("key") not in member.locality_from:
            continue
        value = found.group("value").strip().rstrip(",")
        own = value.lower() in OWN_REPOSITORY_SPELLINGS
        return ((REPO_LOCAL if own else CROSS_REPOSITORY),
                f"the artifact declares {found.group('key')}: {value}")
    return member.locality, (
        f"no {'/'.join(member.locality_from)} declared in this block; fell "
        f"back to the class member's own locality")


# ------------------------------------------------------------- git, refs only

class GitUnavailable(RuntimeError):
    """The repository could not be asked. Never silently a pass."""


def _git(repo, *args, check: bool = False):
    """`git -C <repo> …`, decoded with `errors="replace"` rather than strictly.

    Not a nicety: the scan roots hold committed BINARY blobs (a gzipped
    artifact under `openspec/`), and a strict decode raises `UnicodeDecodeError`
    from inside `subprocess` — a crash where the honest answer is "this blob
    carries no pin". `SCAN_SUFFIXES` keeps binaries out of the sweep; this keeps
    an unexpected one from taking the run down."""
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, check=check,
        text=True, encoding="utf-8", errors="replace")


def is_truncated(repo) -> tuple[bool, str]:
    """Whether the clone's history is truncated, OBSERVED not conjectured.

    Returns `(truncated, what-was-observed)`. Shallow and partial (filtered)
    clones both answer a reachability question about themselves rather than
    about an artifact, which is the split the promoted readiness requirement
    already draws and this module reuses rather than re-spells."""
    shallow = _git(repo, "rev-parse", "--is-shallow-repository")
    if shallow.returncode == 0 and shallow.stdout.strip() == "true":
        return True, ("`git rev-parse --is-shallow-repository` is true for "
                      f"{repo}")
    promisor = _git(repo, "config", "--get-regexp", r"^remote\..*\.promisor")
    if promisor.returncode == 0 and promisor.stdout.strip():
        return True, (f"{repo} is a partial clone "
                      f"({promisor.stdout.strip().splitlines()[0]})")
    return False, (f"`git rev-parse --is-shallow-repository` is false for "
                   f"{repo} and it declares no promisor remote")


# The resolution order for `main`, the ONE branch half of the ref set. THE
# REMOTE-TRACKING SPELLING COMES FIRST, and that order was chosen on evidence
# rather than by taste: the shared aggregation checkout's `refs/heads/main` sat
# at 26e1e021 while `refs/remotes/origin/main` was at 0417e9b5, and consulting
# the local branch reported a pin that HAD landed as orphaned. `main` in the
# requirement means the PUBLISHED branch, so the published spelling is
# authoritative and the local one is the fallback for a clone that has no
# remote-tracking ref (a fixture repository, a bare mirror).
#
# A STALE remote-tracking ref can still under-report, and the report says which
# ref and which sha it consulted so a reader can tell — a `git fetch` and a
# re-run is the answer, not a disposition.
MAIN_REF_ORDER = ("refs/remotes/origin/main", "refs/heads/main")


def resolve_main(repo) -> tuple[str, str] | None:
    """`(ref, sha)` for the `main` half of the ref set, or None."""
    for ref in MAIN_REF_ORDER:
        got = _git(repo, "rev-parse", "--verify", "--quiet", ref)
        if got.returncode == 0 and got.stdout.strip():
            return ref, got.stdout.strip()
    return None


def reachable_from_main(repo, pin: str, main_ref: str) -> bool:
    """`git merge-base --is-ancestor <pin> <main_ref>` — git's own ancestry
    relation, nothing invented. NOT `cat-file`: an object surviving in this
    clone's store is not reachability (see the module docstring)."""
    return _git(repo, "merge-base", "--is-ancestor", pin, main_ref
                ).returncode == 0


def remote_retention_refs(repo, remote: str = "origin"
                          ) -> tuple[dict[str, str] | None, str]:
    """`({refname: sha}, detail)` for the WHOLE namespace, in ONE `ls-remote`.

    One call rather than one per pin, because the namespace is small and a
    network round trip per unreachable pin is what turns a cheap verification
    into a slow one. None on failure, with the reason — never an empty dict,
    which would be indistinguishable from "the namespace is empty" and would
    silently convert an unaskable question into an answer."""
    listed = _git(repo, "ls-remote", remote, f"{RETENTION_NAMESPACE}/*")
    if listed.returncode != 0:
        return None, (f"`git ls-remote {remote} {RETENTION_NAMESPACE}/*` could "
                      f"not be performed: "
                      f"{listed.stderr.strip() or listed.returncode}")
    found: dict[str, str] = {}
    for line in listed.stdout.strip().splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            found[parts[-1].strip()] = parts[0].strip()
    return found, f"{len(found)} ref(s) advertised by {remote}"


def retention_holder(repo, pin: str, *, remote: str = "origin",
                     allow_remote: bool = True,
                     remote_index: dict[str, str] | None = None,
                     remote_error: str | None = None) -> tuple[str | None, str]:
    """Whether `refs/retention/pins/<pin>` exists AND names `pin`.

    Returns `(where, detail)` with `where` one of `"local"`, `"remote"`, or
    None. A ref must point AT the commit its name states: a retention ref named
    for X that points at Y retains nothing, and this is checked rather than
    assumed. `detail` explains a None — including the case where the remote
    could not be consulted, which the caller reports as INCONCLUSIVE rather
    than as an orphan.

    `remote_index` is an already-fetched namespace listing (see
    `remote_retention_refs`); `remote_error` is the reason there is none. Pass
    neither and this function does its own single-ref lookup."""
    ref = retention_ref(pin)
    local = _git(repo, "rev-parse", "--verify", "--quiet", ref)
    if local.returncode == 0 and local.stdout.strip():
        if local.stdout.strip() == pin:
            return "local", f"local {ref}"
        return None, (f"local {ref} points at {local.stdout.strip()} rather "
                      f"than at the commit its name states")
    if not allow_remote:
        return None, (f"no local {ref}, and the remote namespace was not "
                      "consulted (allow_remote=False)")
    if remote_index is None and remote_error is None:
        remote_index, remote_error = remote_retention_refs(repo, remote)
        if remote_index is not None:
            remote_error = None
    if remote_index is None:
        return None, f"no local {ref}, and {remote_error}"
    if ref in remote_index:
        if remote_index[ref] == pin:
            return "remote", f"{remote} {ref}"
        return None, (f"{remote} {ref} points at {remote_index[ref]} rather "
                      f"than at the commit its name states")
    return None, f"no {ref} on {remote} and none locally"


# --------------------------------------------------------- committed pin sites

@dataclass(frozen=True)
class PinSite:
    """One pin found in committed state: which artifact, which key, which pin."""
    path: str
    key: str
    pin: str
    line: int
    member_id: str | None      # None for a site no declared member covers
    locality: str = REPO_LOCAL
    locality_why: str = ""

    def named(self) -> str:
        return f"{self.path}:{self.line} ({self.key}) -> {self.pin}"


def committed_paths(repo, rev: str = "HEAD") -> list[str]:
    """Every path committed at `rev`. Committed state, never a working tree —
    the read point `harden-ideation-readiness-check` promoted, and the reason a
    concurrent edit in a shared checkout cannot move this verdict."""
    listed = _git(repo, "ls-tree", "-r", "--name-only", rev)
    if listed.returncode != 0:
        raise GitUnavailable(
            f"cannot list committed paths at {rev} in {repo}: "
            f"{listed.stderr.strip() or listed.returncode}")
    return [p for p in listed.stdout.split("\n") if p]


def committed_text(repo, rev: str, path: str) -> str | None:
    shown = _git(repo, "show", f"{rev}:{path}")
    return shown.stdout if shown.returncode == 0 else None


def _sites_in(text: str, member: PinMember, path: str) -> list[PinSite]:
    found, pat = [], member.line_re()
    lines = text.splitlines()
    for n, line in enumerate(lines, start=1):
        for m in pat.finditer(line):
            locality, why = site_locality(member, lines, n - 1)
            found.append(PinSite(path, member.key, m.group(1), n, member.id,
                                 locality, why))
    return found


def member_sites(repo, rev: str = "HEAD",
                 *, paths: list[str] | None = None) -> list[PinSite]:
    """Every pin every declared member actually carries at `rev`."""
    paths = paths if paths is not None else committed_paths(repo, rev)
    out: list[PinSite] = []
    for member in PIN_CLASS:
        for path in paths:
            if not path_matches(path, member.paths):
                continue
            text = committed_text(repo, rev, path)
            if text is None:
                continue
            out.extend(_sites_in(text, member, path))
    return out


def swept_sites(repo, rev: str = "HEAD",
                *, paths: list[str] | None = None) -> list[PinSite]:
    """Every vocabulary site inside the scan roots, minus declared non-members.

    The safety net over the declaration: a generator that renames its key, or a
    whole new artifact family, lands here as an UNCOVERED site rather than as
    silence."""
    paths = paths if paths is not None else committed_paths(repo, rev)
    out: list[PinSite] = []
    for path in paths:
        if not path.endswith(SCAN_SUFFIXES):
            continue
        if not path_matches(path, SCAN_ROOTS):
            continue
        if non_member_reason(path) is not None:
            continue
        text = committed_text(repo, rev, path)
        if text is None:
            continue
        for n, line in enumerate(text.splitlines(), start=1):
            for m in _VOCAB_RE.finditer(line):
                out.append(PinSite(path, m.group(1), m.group(2), n, None))
    return out


def covering_member(path: str, key: str) -> PinMember | None:
    for member in PIN_CLASS:
        if member.key_form != "field" or member.key != key:
            continue
        if path_matches(path, member.paths):
            return member
    return None


def uncovered_sites(repo, rev: str = "HEAD",
                    *, paths: list[str] | None = None) -> list[PinSite]:
    """Swept sites no declared member covers — requirement 4's second half."""
    return [s for s in swept_sites(repo, rev, paths=paths)
            if covering_member(s.path, s.key) is None]


# ------------------------------------------------------- the non-commit value
# `declare-sentinel-pin-vocabulary`. Everything from here to the report is the
# FIFTH OUTCOME and its defect twin, and it is deliberately a separate pass over
# the same inventory rather than a widening of the pin path. The commit-shaped
# path above keeps its regexes, its ref set and its verdicts exactly as they
# were: a value that IS a commit name is skipped here, so no site can be
# classified twice and no reachability verdict can be reached through this code.

@dataclass(frozen=True)
class NonPinSite:
    """A NON-COMMIT value standing under a declared pin key.

    Invisible before this existed, and invisibly so: the value regexes bound the
    value to forty hex characters, so a sentinel produced no site at all — not
    reachable, not orphaned, not lost, and not UNCOVERED either. The artifact was
    swept, the key was declared, the member was in good standing, and the value
    was skipped, which is how a run could report a fully verified class over
    seven artifacts whose central provenance claim nothing had read."""
    path: str
    key: str
    value: str
    line: int
    member_id: str | None      # None for a site no declared member covers

    def named(self) -> str:
        return f"{self.path}:{self.line} ({self.key}) -> {self.value!r}"


@dataclass(frozen=True)
class NonPinResult:
    """One classified non-commit value: a LEGAL NON-PIN or a DEFECT.

    Exactly two outcomes and no third, because leaving such a value
    unclassified is the state this whole pass replaces. `sentinel` is the
    declared member where the value is declared and None where it is not; `how`
    states the condition for the first and what is owed for the second."""
    site: NonPinSite
    sentinel: object | None    # pin_sentinels.SentinelMember | None
    how: str

    @property
    def legal(self) -> bool:
        return self.sentinel is not None


@dataclass(frozen=True)
class AbsentKey:
    """A member artifact carrying NO pin key at all.

    A recognized legacy state of the corpus, never a vocabulary member and never
    filled in (`pin_sentinels.ABSENT_KEY`). Reported so the state is visible to
    a reader rather than falling outside both the pin path and the sentinel
    path — an artifact that carries no key looks identical, from every other
    report, to one that was never swept."""
    path: str
    key: str
    member_id: str


def classify_value(site: NonPinSite) -> NonPinResult:
    """The two outcomes, and no guessing between them.

    A value neither commit-shaped nor declared is a DEFECT naming the artifact,
    the key and the value — and the classification does NOT try to tell an
    invented spelling from a truncated object name from a member drifted by one
    character, because the remedy is identical for all three and because a
    near-miss match is precisely the condition under which every consumer
    guarding on an exact string already fails."""
    member = pin_sentinels.declared(site.value)
    if member is not None:
        statement = pin_sentinels.CONDITIONS.get(member.condition, "")
        return NonPinResult(
            site, member,
            f"declared sentinel ({member.standing}) for the "
            f"{member.condition} condition: {statement}")
    return NonPinResult(
        site, None,
        "UNDECLARED: this value is neither a commit name nor a member of the "
        "declared sentinel vocabulary. Declare it in "
        "`doc_health.pin_sentinels` where it names a real condition, or "
        "correct the generator that wrote it where it does not. It is NOT "
        "matched to the nearest declared member: a near-miss spelling is the "
        "condition under which every consumer guarding on the exact string "
        "already fails.")


def _non_pin_in(text: str, key: str, pattern: re.Pattern, path: str,
                member_id: str | None) -> tuple[list[NonPinSite], bool]:
    """`(non-commit sites, the key was seen at all)` for one artifact."""
    found: list[NonPinSite] = []
    seen = False
    for n, line in enumerate(text.splitlines(), start=1):
        if is_comment_line(line):
            continue
        for m in pattern.finditer(line):
            value = _scalar(m.group("value"))
            if not value:
                continue
            seen = True
            if FULL_SHA_RE.match(value):
                continue           # the commit path owns this one
            found.append(NonPinSite(path, key, value, n, member_id))
    return found, seen


def member_non_pin_sites(repo, rev: str = "HEAD",
                         *, paths: list[str] | None = None
                         ) -> tuple[list[NonPinSite], list[AbsentKey]]:
    """Non-commit values under a DECLARED member's key, plus the absences.

    FIELD MEMBERS ONLY. A prose member's pin sits inside a sentence and has no
    field a non-commit value could stand in, and widening a prose pattern to
    accept any scalar would make every sentence quoting the marker a site.
    FUTURE members are skipped for the absence half by construction — having no
    committed instance is what `presence=FUTURE` states."""
    paths = paths if paths is not None else committed_paths(repo, rev)
    sites: list[NonPinSite] = []
    absent: list[AbsentKey] = []
    for member in PIN_CLASS:
        if member.key_form != "field":
            continue
        pattern = member.value_re()
        for path in paths:
            if not path_matches(path, member.paths):
                continue
            text = committed_text(repo, rev, path)
            if text is None:
                continue
            found, seen = _non_pin_in(text, member.key, pattern, path,
                                      member.id)
            sites.extend(found)
            if (not seen and member.key_expected
                    and member.presence == CURRENT):
                absent.append(AbsentKey(path, member.key, member.id))
    return sites, absent


def swept_non_pin_sites(repo, rev: str = "HEAD",
                        *, paths: list[str] | None = None) -> list[NonPinSite]:
    """Non-commit values under any vocabulary key inside the scan roots.

    The same inventory, the same roots, the same serializations and the same
    declared exclusions as `swept_sites` — stated rather than inferred, because
    a vocabulary checked over a wider or narrower set than the pins it qualifies
    would report gaps the pin class does not have and miss gaps it does."""
    paths = paths if paths is not None else committed_paths(repo, rev)
    out: list[NonPinSite] = []
    for path in paths:
        if not path.endswith(SCAN_SUFFIXES):
            continue
        if not path_matches(path, SCAN_ROOTS):
            continue
        if non_member_reason(path) is not None:
            continue
        text = committed_text(repo, rev, path)
        if text is None:
            continue
        for n, line in enumerate(text.splitlines(), start=1):
            if is_comment_line(line):
                continue
            for m in _WIDE_VOCAB_RE.finditer(line):
                value = _scalar(m.group("value"))
                if not value or FULL_SHA_RE.match(value):
                    continue
                out.append(NonPinSite(path, m.group("key"), value, n, None))
    return out


def non_pin_sites(repo, rev: str = "HEAD",
                  *, paths: list[str] | None = None
                  ) -> tuple[list[NonPinSite], list[NonPinSite],
                             list[AbsentKey]]:
    """`(classified sites, uncovered non-pin sites, absences)`.

    The uncovered half is returned SEPARATELY as well as being classified,
    because a sentinel standing under a key no declared member covers is TWO
    findings: the class has a coverage gap, and the value has a classification.
    Letting either mask the other would leave one of them unreported."""
    paths = paths if paths is not None else committed_paths(repo, rev)
    covered, absent = member_non_pin_sites(repo, rev, paths=paths)
    known = {(s.path, s.key, s.line) for s in covered}
    uncovered = [s for s in swept_non_pin_sites(repo, rev, paths=paths)
                 if (s.path, s.key, s.line) not in known
                 and covering_member(s.path, s.key) is None]
    return covered + uncovered, uncovered, absent


def unused_sentinels(sites) -> tuple:
    """Declared members that no committed artifact carries AND no code emits.

    THE SECOND DIRECTION, and the unobvious one. Corpus-against-declaration
    catches a generator inventing a spelling — the failure everybody expects.
    Declaration-against-corpus catches a vocabulary accumulating entries nobody
    writes, which is slower and more corrosive: a reader looks up a value, finds
    a plausible-sounding condition, and believes something about an artifact no
    generator has ever produced.

    A DECLARED EMITTER EXEMPTS A MEMBER, and that is not a loophole. Reporting a
    stale member is not deleting it: a condition may be declared before its
    first committed instance lands, exactly as the pin class declares FUTURE
    members, and a member whose generator exists but whose output has not been
    committed yet is in that state rather than stale. `emitters` is measured by
    test rather than believed, so a phantom emitter cannot hold a stale member
    alive."""
    carried = {s.value for s in sites}
    return tuple(m for m in pin_sentinels.SENTINELS
                 if not m.emitters
                 and not any(m.matches(v) for v in carried))


# THE REPOSITORY THIS DECLARATION DESCRIBES. `PIN_CLASS` is a statement about
# openxFactory's own artifacts, so the ABSENCE of a declared artifact only means
# something here. Run over a fixture repository or any other checkout, every row
# would "vanish" and the report would be noise. Two markers rather than one,
# because a single common path is easy to create by accident.
DECLARATION_SUBJECT_MARKERS: tuple[str, ...] = (
    "contracts/manifest.yaml", "ideation/cross-reference.yaml",
)


def is_declaration_subject(paths) -> bool:
    present = set(paths)
    return all(marker in present for marker in DECLARATION_SUBJECT_MARKERS)


def vanished_members(repo, rev: str = "HEAD",
                     *, paths: list[str] | None = None) -> list[PinMember]:
    """Declared CURRENT members whose artifact no committed path matches.

    The other direction of declaration drift: a registry row left behind by a
    deletion or a rename. FUTURE members are exempt by construction — having no
    committed instance is what `presence=FUTURE` states, and an arrival is
    reported by `arrived_future_members` instead.

    Answered ONLY for the repository the declaration describes: see
    `DECLARATION_SUBJECT_MARKERS`."""
    paths = paths if paths is not None else committed_paths(repo, rev)
    if not is_declaration_subject(paths):
        return []
    gone = []
    for member in PIN_CLASS:
        if member.presence != CURRENT:
            continue
        if not any(path_matches(p, member.paths) for p in paths):
            gone.append(member)
    return gone


def arrived_future_members(repo, rev: str = "HEAD",
                           *, paths: list[str] | None = None
                           ) -> list[tuple[PinMember, list[PinSite]]]:
    """FUTURE members that now carry committed pins — the arrival this
    declaration exists to catch. Reported so the row is promoted to CURRENT
    deliberately rather than left describing a state that has moved."""
    paths = paths if paths is not None else committed_paths(repo, rev)
    arrived = []
    for member in PIN_CLASS:
        if member.presence != FUTURE:
            continue
        sites: list[PinSite] = []
        for path in paths:
            if not path_matches(path, member.paths):
                continue
            text = committed_text(repo, rev, path)
            if text is not None:
                sites.extend(_sites_in(text, member, path))
        if sites:
            arrived.append((member, sites))
    return arrived


# ------------------------------------------------------------- the verdicts

PASS = "pass"
ORPHAN = "orphan"
LOST = "lost"                  # orphaned AND unrecoverable; declared in
                               # KNOWN_LOSSES, with the superseding act either
                               # still owed or discharged by a cited record
INCONCLUSIVE = "inconclusive"
NOT_APPLICABLE = "not-applicable"


@dataclass(frozen=True)
class PinResult:
    site: PinSite
    verdict: str               # PASS | ORPHAN | INCONCLUSIVE | NOT_APPLICABLE
    how: str                   # which half of the ref set answered, or why not
    discharge: str | None = None    # LOST only: the committed superseding
                                    # record found at this revision, or None
                                    # while the governance act is still owed


@dataclass(frozen=True)
class PinClassReport:
    rev: str
    main_ref: str | None
    main_sha: str | None
    truncated: bool
    truncation: str
    results: tuple[PinResult, ...]
    uncovered: tuple[PinSite, ...]
    vanished: tuple[PinMember, ...]
    arrived: tuple[tuple[PinMember, tuple[PinSite, ...]], ...]
    # `declare-sentinel-pin-vocabulary`. Defaulted so a caller constructing a
    # report by hand — the existing tests do — keeps working unchanged.
    non_pins: tuple[NonPinResult, ...] = ()
    uncovered_non_pins: tuple[NonPinSite, ...] = ()
    absent_keys: tuple[AbsentKey, ...] = ()
    unused_sentinels: tuple = ()
    declaration_defects: tuple[str, ...] = ()

    @property
    def legal_non_pins(self) -> list[NonPinResult]:
        """Declared sentinels — the FIFTH OUTCOME, and a conforming one.

        It sits beside reachable, orphaned, lost and uncovered rather than
        inside any of them. Not reachable (no commit, so reporting it as
        reachable would claim a resolution nobody performed); not orphaned or
        lost (those say a NAMED commit cannot be found, and here none was
        named, so a repair route would be offered for a defect that does not
        exist); not uncovered (the key IS declared and the sweep DID read the
        site, so a coverage finding would send the next reader to widen a
        declaration that is already correct); not inconclusive (the clone
        answered perfectly, and the answer is "no commit here")."""
        return [r for r in self.non_pins if r.legal]

    @property
    def undeclared_values(self) -> list[NonPinResult]:
        """Non-commit values the vocabulary does not declare — the defect."""
        return [r for r in self.non_pins if not r.legal]

    @property
    def orphans(self) -> list[PinResult]:
        return [r for r in self.results if r.verdict == ORPHAN]

    @property
    def lost(self) -> list[PinResult]:
        return [r for r in self.results if r.verdict == LOST]

    @property
    def lost_awaiting_record(self) -> list[PinResult]:
        """Declared losses whose SUPERSEDING RECORD has not been found in
        committed state — the ones with a governance act still outstanding.

        The split is between "declared loss with a superseding record" and
        "unresolved loss", and it is the only thing a landed record changes. A
        discharged loss is still reported, still carries its measurement, and is
        still re-measured by test; deleting the row was never the resolution and
        is not one now."""
        return [r for r in self.lost if r.discharge is None]

    @property
    def inconclusive(self) -> list[PinResult]:
        return [r for r in self.results if r.verdict == INCONCLUSIVE]

    @property
    def verified(self) -> list[PinResult]:
        return [r for r in self.results if r.verdict == PASS]

    @property
    def clean(self) -> bool:
        """No REPAIRABLE defect stands. A declared, re-measured, unrecoverable
        loss is excluded deliberately: it is a standing governance obligation
        with no code repair available, and reddening every unrelated change on
        it would be enforcement arriving through the back door — the same
        reasoning four doc-health families launched advisory over a standing
        population under. `fully_verified` is the property that stays False.

        AN UNDECLARED NON-COMMIT VALUE IS A REPAIRABLE DEFECT AND IS CONSULTED
        HERE; A DECLARED SENTINEL IS NOT. The second half is the deliberate
        part: an artifact carrying an honest sentinel is CONFORMING — it did
        what the generator obligation asks — and holding verification open on
        it would punish exactly the behaviour the vocabulary exists to require,
        which is the fastest way to teach the next generator author to stamp
        `HEAD` and stay quiet. A recognized legacy absence is likewise reported
        and not held against the class: it is repaired never, so there is
        nothing for a red to ask for."""
        return not (self.orphans or self.uncovered or self.vanished
                    or self.arrived or self.undeclared_values
                    or self.uncovered_non_pins or self.declaration_defects)

    @property
    def fully_verified(self) -> bool:
        """The class is fully verified only when nothing was left unanswered:
        no defect, no declared loss awaiting its superseding record, and no pin
        the clone or the remote could not be asked about.

        READ THE DOCSTRING'S OWN WORDS: what holds this False for a loss is the
        superseding record being AWAITED, not the loss existing. A loss whose
        record has landed is answered — the record states what the archived
        evidence still verifies and what it cannot, which is precisely the
        question this property asks — so it stops blocking, while the loss
        itself stays declared, reported and re-measured for ever
        (`supersede-lost-pin-baseline`, 2026-08-27). Restoring it any other way
        would mean deleting a row, and deleting the row is how a known defect
        becomes background noise."""
        return (self.clean and not self.lost_awaiting_record
                and not self.inconclusive)

    def summary(self) -> str:
        by_member = len({r.site.member_id for r in self.results})
        awaiting = len(self.lost_awaiting_record)
        return (f"{len(self.results)} declared pin sites across {by_member} "
                f"class members at {self.rev[:12]}: {len(self.verified)} "
                f"reachable, {len(self.orphans)} orphaned, "
                f"{len(self.lost)} lost (declared unrecoverable, {awaiting} "
                f"awaiting a superseding record), "
                f"{len(self.inconclusive)} inconclusive; "
                f"{len(self.uncovered)} uncovered site(s), "
                f"{len(self.vanished)} vanished member(s), "
                f"{len(self.arrived)} future member(s) now carrying pins; "
                f"{len(self.legal_non_pins)} legal non-pin(s), "
                f"{len(self.undeclared_values)} undeclared non-commit "
                f"value(s), {len(self.absent_keys)} recognized legacy "
                f"absence(s), {len(self.unused_sentinels)} unused vocabulary "
                f"member(s)")


def verify(repo, *, rev: str = "HEAD", remote: str = "origin",
           allow_remote: bool = True) -> PinClassReport:
    """Verify the whole declared class over committed state at `rev`.

    The ref set is `main` plus `refs/retention/pins/<full-sha>` computed from
    each pin, and no more. Cross-repository members are recorded
    NOT_APPLICABLE: their reachability is answered against another remote by
    another authority, and reporting them as orphans here would be a finding
    about the wrong repository."""
    resolved = _git(repo, "rev-parse", rev)
    if resolved.returncode != 0:
        raise GitUnavailable(f"cannot resolve {rev} in {repo}: "
                             f"{resolved.stderr.strip()}")
    rev_sha = resolved.stdout.strip()
    truncated, truncation = is_truncated(repo)
    main = resolve_main(repo)
    main_ref, main_sha = main if main else (None, None)

    paths = committed_paths(repo, rev_sha)
    # The retention namespace is listed ONCE for the whole run rather than once
    # per unreachable pin, and only if something actually needs it.
    remote_index: dict[str, str] | None = None
    remote_error: str | None = None
    listed_remote = False

    results: list[PinResult] = []
    for site in member_sites(repo, rev_sha, paths=paths):
        member = next(m for m in PIN_CLASS if m.id == site.member_id)
        if site.locality == CROSS_REPOSITORY:
            results.append(PinResult(
                site, NOT_APPLICABLE,
                f"cross-repository pin ({member.generator}); "
                f"{site.locality_why}; answered against another remote by "
                f"another authority"))
            continue
        if main_ref is None:
            results.append(PinResult(
                site, INCONCLUSIVE,
                f"no `main` in this clone (looked for "
                f"{', '.join(MAIN_REF_ORDER)}), so the branch half of the ref "
                f"set could not be consulted"))
            continue
        if reachable_from_main(repo, site.pin, main_ref):
            results.append(PinResult(site, PASS, f"ancestor of {main_ref}"))
            continue
        if allow_remote and not listed_remote:
            remote_index, remote_error = remote_retention_refs(repo, remote)
            if remote_index is not None:
                remote_error = None
            listed_remote = True
        where, detail = retention_holder(
            repo, site.pin, remote=remote, allow_remote=allow_remote,
            remote_index=remote_index, remote_error=remote_error)
        if where is not None:
            results.append(PinResult(site, PASS, f"retained: {detail}"))
            continue
        if truncated:
            results.append(PinResult(
                site, INCONCLUSIVE,
                f"TRUNCATED CLONE, observed not conjectured: {truncation}; "
                f"{detail}"))
            continue
        if "could not be performed" in detail:
            results.append(PinResult(
                site, INCONCLUSIVE,
                f"the retention namespace could not be consulted, so the "
                f"question was not answerable rather than answered: {detail}"))
            continue
        loss = known_loss(site.pin)
        if loss is not None:
            record = discharging_record(repo, rev_sha, loss, paths=paths)
            if record is None:
                results.append(PinResult(
                    site, LOST,
                    f"DECLARED UNRECOVERABLE: {loss.measured} "
                    f"OWED: {loss.owed}"))
            else:
                results.append(PinResult(
                    site, LOST,
                    f"DECLARED UNRECOVERABLE: {loss.measured} "
                    f"DISCHARGED: {loss.discharged} The superseding record "
                    f"stands at {record}, read from committed state at this "
                    f"revision and naming this pin. THE LOSS IS NOT SILENCED "
                    f"BY IT: this row is never deleted, and the day the object "
                    f"turns out to be recoverable, retention is the route and "
                    f"the re-measurement says so.",
                    discharge=record))
            continue
        results.append(PinResult(site, ORPHAN, detail))

    classified, uncovered_non_pins, absent = non_pin_sites(
        repo, rev_sha, paths=paths)

    return PinClassReport(
        rev=rev_sha, main_ref=main_ref, main_sha=main_sha,
        truncated=truncated, truncation=truncation,
        results=tuple(results),
        uncovered=tuple(uncovered_sites(repo, rev_sha, paths=paths)),
        vanished=tuple(vanished_members(repo, rev_sha, paths=paths)),
        arrived=tuple((m, tuple(s)) for m, s in
                      arrived_future_members(repo, rev_sha, paths=paths)),
        non_pins=tuple(classify_value(s) for s in classified),
        uncovered_non_pins=tuple(uncovered_non_pins),
        absent_keys=tuple(absent),
        unused_sentinels=unused_sentinels(classified),
        declaration_defects=pin_sentinels.declaration_defects(),
    )


# ----------------------------------------------------------- repair semantics

def repair_route(member: PinMember, *, status: str | None = None) -> str:
    """The route an orphaned pin on `member` is repaired by — named at the
    moment the finding fires, because that is the moment somebody has to choose
    (packet tasks § 2.8: the landing obligation is DISCOVERABLE where it binds).

    Two routes, and which one applies is a property of the artifact rather than
    a preference. An IMMUTABLE artifact — `status: record`, or a machine-written
    manifest inside an archived packet — is repaired by RETENTION: publish the
    computed `refs/retention/pins/<full-sha>` on the repository's own remote and
    leave the artifact's bytes exactly as captured, because re-pinning a record
    would make it state something the run did not read. A MUTABLE generated
    projection is repaired by REPRODUCTION: re-derive the body at a reachable
    revision and re-pin it, with the re-pin defined by the body reproducing
    there — a reachable-but-unreproduced re-pin is refused, because that is
    precisely the hand-move that produced this repository's second orphan."""
    immutable = (status == "record"
                 or member.id == "proposal-support-manifest")
    if immutable:
        return ("RETENTION: publish "
                f"{RETENTION_NAMESPACE}/<full-sha> on the repository's own "
                "remote, computed from the pin, and leave the artifact's bytes "
                "unchanged. Editing the pin is refused: it would make an "
                "immutable record state something the run did not read.")
    if member.reproduction == TOOL_DEFINED:
        return (f"REPRODUCTION: re-derive the body with {member.generator} at a "
                "reachable revision and re-pin it, then prove the committed "
                "body reproduces BYTE-FOR-BYTE at the new pin. A pin moved to "
                "a reachable value without regeneration is refused.")
    return (f"REPRODUCTION: nothing re-derives this artifact "
            f"({member.generator}), so a re-pin owes a NAMED MEASUREMENT that "
            "established equivalence at the new pin, or the artifact is "
            "regenerated so the question does not arise. Where the artifact "
            "cannot be edited at all, retention is the route instead.")


def tool_defined_members() -> tuple[PinMember, ...]:
    """The members whose reproduction is byte-comparable — the only ones a
    reproduction check can answer in bytes rather than in a recorded
    measurement."""
    return tuple(m for m in PIN_CLASS if m.reproduction == TOOL_DEFINED)


# --------------------------------------------------------------------- report

def render(report: PinClassReport) -> str:
    """A human-readable rendering, used by the probe's failure text and by
    anyone running this module directly."""
    lines = [report.summary(),
             f"  ref set: {report.main_ref or '(no main resolved)'} + "
             f"{RETENTION_NAMESPACE}/<full-sha>",
             f"  clone:   {report.truncation}"]
    for result in report.results:
        mark = {PASS: "ok  ", ORPHAN: "ORPH", LOST: "LOST",
                INCONCLUSIVE: "skip", NOT_APPLICABLE: "n/a "}[result.verdict]
        lines.append(f"  [{mark}] {result.site.named()} — {result.how}")
    for site in report.uncovered:
        lines.append(f"  [UNCOVERED] {site.named()} — no declared class member "
                     "covers this artifact and key")
    for member in report.vanished:
        lines.append(f"  [VANISHED] declared member {member.id} matches no "
                     f"committed path ({', '.join(member.paths)})")
    for member, sites in report.arrived:
        lines.append(f"  [ARRIVED] future member {member.id} now carries "
                     f"{len(sites)} committed pin(s); promote its row to "
                     "presence=current")
    for result in report.non_pins:
        mark = "non-pin" if result.legal else "UNDECLARED"
        lines.append(f"  [{mark}] {result.site.named()} — {result.how}")
    for site in report.uncovered_non_pins:
        lines.append(f"  [UNCOVERED] {site.named()} — no declared class member "
                     "covers this artifact and key. Reported beside the value's "
                     "own classification above rather than instead of it: a "
                     "coverage gap in the declaration and the meaning of the "
                     "value are separate findings.")
    for absence in report.absent_keys:
        lines.append(f"  [ABSENT] {absence.path} carries no `{absence.key}` "
                     f"where member {absence.member_id} expects one. "
                     f"{pin_sentinels.ABSENT_KEY}")
    for member in report.unused_sentinels:
        lines.append(f"  [UNUSED] vocabulary member {member.value!r} "
                     f"({member.condition}) is carried by no committed "
                     "artifact and emitted by no declared generator. This is "
                     "NOT an instruction to delete it — a condition may be "
                     "declared before its generator lands — but the state is "
                     "reported rather than assumed.")
    for defect in report.declaration_defects:
        lines.append(f"  [DECLARATION] {defect}")
    return "\n".join(lines)


def main(argv=None) -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="Verify derivation-pin reachability across the declared "
                    "artifact class.")
    parser.add_argument("--repo", default=str(Path(__file__).resolve()
                                              .parents[2]))
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--no-remote", action="store_true",
                        help="do not consult the retention namespace on the "
                             "remote; unresolved pins report INCONCLUSIVE")
    args = parser.parse_args(argv)
    report = verify(args.repo, rev=args.rev, remote=args.remote,
                    allow_remote=not args.no_remote)
    print(render(report))
    return 1 if not report.clean else 0


if __name__ == "__main__":   # pragma: no cover - module entry point
    raise SystemExit(main())
