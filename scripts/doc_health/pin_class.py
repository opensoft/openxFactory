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

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

# --------------------------------------------------------------- the namespace

RETENTION_NAMESPACE = "refs/retention/pins"

FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

# A 40-hex token standing alone — not a prefix of a 64-hex sha256, not a suffix
# of one. `(?<![0-9a-fA-F])` / `(?![0-9a-fA-F])` rather than `\b`, because `\b`
# treats a hex digit boundary inside a longer hex run as a word boundary and a
# sha256 digest would then yield two spurious "pins".
LOOSE_SHA_RE = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{40}(?![0-9a-fA-F])")


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
    key name is not a key."""
    return re.compile(
        rf'(?<![A-Za-z0-9_])"?{re.escape(key)}"?\s*:\s*"?([0-9a-f]{{40}})"?')

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

    def line_re(self) -> re.Pattern:
        if self.pattern:
            return re.compile(self.pattern)
        return _field_re(self.key)


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
        pattern=r"Source revision:\s*`?([0-9a-f]{40})`?",
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
        pattern=r"source_revision\s+`?([0-9a-f]{40})`?",
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

_VOCAB_RE = re.compile(
    r'(?<![A-Za-z0-9_])"?(' + "|".join(re.escape(k) for k in sorted(
        PIN_KEY_VOCABULARY, key=len, reverse=True))
    + r')"?\s*:\s*"?([0-9a-f]{40})"?')


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
        population under. `fully_verified` is the property that stays False."""
        return not (self.orphans or self.uncovered or self.vanished
                    or self.arrived)

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
                f"{len(self.arrived)} future member(s) now carrying pins")


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

    return PinClassReport(
        rev=rev_sha, main_ref=main_ref, main_sha=main_sha,
        truncated=truncated, truncation=truncation,
        results=tuple(results),
        uncovered=tuple(uncovered_sites(repo, rev_sha, paths=paths)),
        vanished=tuple(vanished_members(repo, rev_sha, paths=paths)),
        arrived=tuple((m, tuple(s)) for m, s in
                      arrived_future_members(repo, rev_sha, paths=paths)),
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
