"""`add-estate-repository-inventory` § 3: the estate inventory, its reader and
validator, and the membership arm.

THE PACKET NAMES THIS DIRECTORY AND NO OTHER, AND THAT IS WHY THE MEMBERSHIP
ARM'S CASES ARE HERE TOO. `tasks.md` § 3.5 owes "`tests/estate_inventory/`
(NEW): one case per scenario class of both ADDED requirements and of the
MODIFIED paragraph", and `tasks.md` § 3.6 says "NO OTHER FILE MOVES … every
existing test … untouched", which `proposal.md`'s `code_surface:` declaration
repeats ("no existing test is edited, renamed, flipped or deleted"). So the arm
added to `scripts/validate-code-surface.py` is exercised FROM HERE, by running
that validator as a subprocess over a tree built in a tmpdir, and
`tests/code_surface/test_code_surface_gate.py` is not touched by one byte.

EVERY TREE HERE IS BUILT IN A TMPDIR AND JUDGED AGAINST AN INVENTORY AND A
REGISTER BUILT BESIDE IT, so a test can never be made green by editing the
repository's own inventory, and the corpus tests at the end are the only ones
that read the real one.

THE THREE SUBJECTS THIS FILE PINS, by the delta's own titles: *The estate's
repositories are enumerated in a governed inventory* (the five admission kinds,
the three governance classes, unique bare names, current addresses only, the
bound on the evidence re-check and the carrier verification the ruling added),
*A declared repository is judged for membership against the estate inventory*
(fail-closed, the external refusal, the former-address report, the registered
declaration, the stale row, the archive), and the ONE PARAGRAPH the `## MODIFIED`
block moves — the grammar arm judging SHAPE while membership is judged by the
arm the second requirement defines, both reporting in ONE run.

FAILS-THEN-PASSES. Every case here is written to fail against the tree without
§ 3.1–§ 3.4: the module under test does not exist there, the inventory file does
not exist there, and `validate-code-surface.py` has no `--inventory` flag and no
membership block to assert on. The realization pull request records both runs.
"""
from __future__ import annotations

import datetime
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "scripts" / "estate_inventory.py"
INVENTORY = ROOT / "scripts" / "estate-repository-inventory.yaml"
INVENTORY_VALIDATOR = ROOT / "scripts" / "validate-estate-inventory.py"
SURFACE_VALIDATOR = ROOT / "scripts" / "validate-code-surface.py"
REGISTER = ROOT / "scripts" / "code-surface-register.yaml"


def _load(name: str, path: Path):
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ei = _load("estate_inventory", MODULE)


# --- tree builders ------------------------------------------------------------


def _row(repository: str, name: str | None = None, *,
         governance: str = "governed",
         admitted_by: list[dict] | None = None,
         role: str = "a role in the layer model",
         provisional: bool | None = None) -> dict:
    """One well-formed inventory row, serialized rather than hand-spelled.

    `safe_dump` is the writer for every WELL-FORMED fixture; the MALFORMED ones
    below are spelled by hand on purpose, because a malformed file is the thing
    under test and a dumper would refuse to produce some of them.
    """
    row = {
        "repository": repository,
        "name": name if name is not None else repository.split("/")[-1],
        "role": role,
        "governance": governance,
        "admitted_by": admitted_by if admitted_by is not None
        else [{"kind": "gitlink", "carrier": "opensoft/xFactory"}],
    }
    if provisional is not None:
        row["provisional"] = provisional
    return row


def _carrier_row(address: str) -> dict:
    """A `governed` row for a repository some other row names as its CARRIER.

    `opensoft/xFactory`'s is spelled with `kind: root`, which is the one
    admission that address may carry and the one no `.gitmodules` can give it.
    """
    if address == ei.AGGREGATION_ROOT:
        return _row(address, role="the aggregation root",
                    admitted_by=[{"kind": "root"}])
    return _row(address, role="a governed carrier",
                admitted_by=[{"kind": "gitlink",
                              "carrier": ei.AGGREGATION_ROOT}])


def _inventory(root: Path, rows: list[dict], name: str = "inventory.yaml",
               head: dict | None = None, bind_carriers: bool = True) -> Path:
    """A well-formed inventory file at `root`.

    THE CARRIERS ARE BOUND UNLESS A CASE IS TESTING THE BINDING. `load_inventory`
    requires every `gitlink` carrier to resolve to a `governed` row OF THIS SAME
    INVENTORY — the kind's own words being "a GOVERNED ESTATE REPOSITORY's
    `.gitmodules`" — so a fixture naming a carrier it does not carry is refused,
    correctly and uninterestingly, in every case whose subject is something
    else. The rows are APPENDED, never prepended, so `rows[0]` is still the row
    the case wrote. `bind_carriers=False` opts out, and the cases that exercise
    the binding itself pass it.
    """
    rows = list(rows)
    if bind_carriers:
        # TO A FIXED POINT, because an appended carrier row names a carrier of
        # its own and the binding is only satisfied when nothing is left owing.
        carried = {row["repository"] for row in rows}
        while True:
            owed = [
                admission["carrier"]
                for row in rows for admission in row.get("admitted_by", [])
                if isinstance(admission, dict)
                and admission.get("kind") == "gitlink"
                and isinstance(admission.get("carrier"), str)
                and admission["carrier"] not in carried]
            if not owed:
                break
            for carrier in dict.fromkeys(owed):
                rows.append(_carrier_row(carrier))
                carried.add(carrier)
    document = {"schema_version": 1, "kind": "estate-repository-inventory"}
    if head is not None:
        document.update(head)
    document["repositories"] = rows
    path = root / name
    path.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=True,
                       width=10_000),
        encoding="utf-8")
    return path


def _proposal(root: Path, change: str, front: str, archived: bool = False,
              body: str = "# Proposal\n", status: str | None = None) -> Path:
    """A proposal at `openspec/changes[/archive]/<change>/proposal.md`.

    `status` writes the lifecycle `Status:` HEADER LINE, which is what a
    `change` admission's re-check reads (the kind admits a RATIFIED change and
    not a directory). It is left ABSENT by default, because most cases here are
    about the grammar and a helper that ratified every fixture silently would
    hide the one constraint that matters at the sites that do care.
    """
    where = root / "openspec" / "changes"
    if archived:
        where = where / "archive"
    folder = where / change
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "proposal.md"
    header = f"Status: {status}\n\n" if status is not None else ""
    path.write_text(f"---\n{front}\n---\n\n{header}{body}",
                    encoding="utf-8")
    return path


def _register(root: Path, entries: str = "register: []\n") -> Path:
    path = root / "register.yaml"
    path.write_text(entries, encoding="utf-8")
    return path


def _entry_text(change: str, declaration: str) -> str:
    entry = {
        "change": change,
        "declaration": declaration,
        "class": "list-runs-into-prose",
        "why": "a reason",
        "cited_to": ["a document § a section"],
        "retires_when": "an event",
    }
    return yaml.safe_dump({"register": [entry]}, sort_keys=False,
                          allow_unicode=True, width=10_000)


def _transfer_map(root: Path, transfers: list[dict]) -> Path:
    """A minimal `contracts/policies/repository-identity.yaml`.

    The shape is the live file's — `transfers:` of mappings carrying `former`,
    `current` and `transfer_state` — and nothing else is needed, because the
    reader takes nothing else from it.
    """
    folder = root / "contracts" / "policies"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "repository-identity.yaml"
    path.write_text(
        yaml.safe_dump({"schema_version": 1, "kind": "repository_identity",
                        "transfers": transfers},
                       sort_keys=False, allow_unicode=True, width=10_000),
        encoding="utf-8")
    return path


def _worktree(root: Path, origin: str, submodules: list[str] | None = None,
              name: str = "carrier") -> Path:
    """A real git working tree that ASSERTS an identity through its origin URL.

    A REAL `git init` AND A REAL REMOTE, not a stubbed reader: the whole content
    of the ruling this exercises is that a PATH IS AN ASSERTION AND NOT AN
    IDENTITY, and a test that mocked the identity read would be testing the mock.
    """
    tree = root / name
    tree.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(tree)], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(tree), "remote", "add", "origin", origin],
                   check=True, capture_output=True)
    if submodules is not None:
        (tree / ".gitmodules").write_text(
            "".join(
                f'[submodule "{address.split("/")[-1]}"]\n'
                f'\tpath = {address.split("/")[-1]}\n'
                f'\turl = git@github.com:{address}.git\n'
                for address in submodules),
            encoding="utf-8")
    return tree


def _run_inventory(root: Path, inventory: Path, *extra: str):
    return subprocess.run(
        [sys.executable, str(INVENTORY_VALIDATOR), str(root),
         "--inventory", str(inventory), *extra],
        capture_output=True, text=True)


def _run_surface(root: Path, inventory: Path | None, register: Path):
    argv = [sys.executable, str(SURFACE_VALIDATOR), str(root),
            "--register", str(register)]
    if inventory is not None:
        argv += ["--inventory", str(inventory)]
    return subprocess.run(argv, capture_output=True, text=True)


def _tree_inventory(root: Path, rows: list[dict]) -> Path:
    """An inventory at the path the SCANNED TREE carries it at, so the run
    resolves it with no flag at all."""
    (root / "scripts").mkdir(parents=True, exist_ok=True)
    return _inventory(root, rows,
                      name=str(Path("scripts") / ei.INVENTORY_PATH.name))


# ==============================================================================
# *The estate's repositories are enumerated in a governed inventory*
# ==============================================================================


def test_a_repository_is_admitted_by_a_gitlink_that_NAMES_ITS_CARRIER(tmp_path):
    """Scenario *A repository is admitted to the estate by a gitlink*.

    "the inventory SHALL carry a row for it whose `admitted_by:` names that
    gitlink AND the repository that carries it" — so a `gitlink` with no
    carrier is refused at the LOAD and not tolerated as an admission nobody can
    check. The carrier is what makes the evidence checkable at all: a reader
    cannot look in a tree the row does not name.
    """
    good = _inventory(tmp_path, [
        _row("opensoft/openxFactory",
             admitted_by=[{"kind": "gitlink", "carrier": "opensoft/xFactory"}]),
    ])
    loaded = ei.load_inventory(good)
    admission = loaded.rows[0].admitted_by[0]
    assert admission.kind == "gitlink"
    assert admission.carrier == "opensoft/xFactory"

    bad = _inventory(tmp_path, [
        _row("opensoft/openxFactory", admitted_by=[{"kind": "gitlink"}]),
    ], name="carrierless.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(bad)
    assert "carrier" in str(refusal.value)


def test_a_NESTED_gitlink_names_the_DomainxFactory_that_carries_it(tmp_path):
    """The same scenario's wide/nested distinction, which is the whole reason
    the kind was widened at the review of PR #1101: "the aggregation
    repository's in the wide case, a governed DomainxFactory's where the estate
    nested the repository rather than sibling-linking it". A row whose carrier
    is a DomainxFactory loads on exactly the same terms."""
    path = _inventory(tmp_path, [
        _row("opensoft/openChart",
             admitted_by=[{"kind": "gitlink", "carrier": "opensoft/MedxChart"}]),
    ])
    assert ei.load_inventory(path).rows[0].admitted_by[0].carrier == \
        "opensoft/MedxChart"


def test_a_pinned_product_that_is_NO_submodule_is_admitted_by_its_pin(tmp_path):
    """Scenario *A neutral product is pinned but is no submodule*.

    "the inventory SHALL carry a row for it admitted by that pin, with
    governance class `pinned` … the absence of a gitlink is not an absence of
    membership, the pin being an admission in its own right." The row carries
    no gitlink at all, and its evidence is re-checked in THIS tree on every run.
    """
    (tmp_path / "contracts").mkdir()
    (tmp_path / "contracts" / "thing-pin.yaml").write_text(
        "source_repository: opensoft/openRepoShape\n", encoding="utf-8")
    path = _inventory(tmp_path, [
        _row("opensoft/openRepoShape", governance="pinned",
             admitted_by=[{"kind": "pin", "path": "contracts/thing-pin.yaml"}]),
    ])
    inventory = ei.load_inventory(path)
    assert inventory.rows[0].governance == "pinned"
    verdicts = ei.evidence_verdicts(inventory, tmp_path)
    assert [v.verdict for v in verdicts] == [ei.NAMED]
    assert _run_inventory(tmp_path, path).returncode == 0


def test_a_repository_a_ratified_change_is_creating_is_a_PROVISIONAL_row(tmp_path):
    """Scenario *A repository a ratified change is creating*, first clause.

    "the inventory MUST carry a PROVISIONAL row admitted by that change, marked
    as provisional and naming the change id." Both halves of the marking are
    enforced, in both directions: a `change` admission that does not say
    `provisional: true` is refused, because what expires at that change's
    archive is exactly this admission; and a `provisional: true` admitted by no
    `change` is refused, because PROVISIONAL is what a `change` admission IS.
    """
    (tmp_path / "openspec" / "changes" / "create-a-thing").mkdir(parents=True)
    good = _inventory(tmp_path, [
        _row("opensoft/NewThing", governance="pinned", provisional=True,
             admitted_by=[{"kind": "change", "change": "create-a-thing"}]),
    ])
    row = ei.load_inventory(good).rows[0]
    assert row.provisional is True
    assert row.admitted_by[0].change == "create-a-thing"

    unmarked = _inventory(tmp_path, [
        _row("opensoft/NewThing", governance="pinned",
             admitted_by=[{"kind": "change", "change": "create-a-thing"}]),
    ], name="unmarked.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(unmarked)
    assert "provisional" in str(refusal.value)

    groundless = _inventory(tmp_path, [
        _row("opensoft/NewThing", provisional=True),
    ], name="groundless.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(groundless)
    assert "provisional" in str(refusal.value)


def test_an_inventory_MISSING_the_change_row_REFUSES_the_ratified_packet(tmp_path):
    """Scenario *A repository a ratified change is creating*, second clause —
    and one of the TWO cases `tasks.md` § 3.5 names because the rulings created
    them.

    "the membership arm is UNCONDITIONAL and still FAILS CLOSED for that
    identifier — the row is what makes the declaration resolve, so an absent row
    refuses a ratified packet inside the forward-looking window rather than
    excusing it." **Ruled by Brett Heap, 2026-09-18, verbatim "MAY becomes
    MUST".** The obligation sits on the INVENTORY (§ 3.1 owes the row) and the
    arm takes no exception for the window: WITHOUT the row the lawful ratified
    declaration is REFUSED, WITH it the same declaration passes, and nothing
    about the arm changed between the two runs.
    """
    _proposal(tmp_path, "create-a-thing",
              "code_surface: opensoft/NewThing — created by this change\n"
              "target_release: implemented\n",
              status="ratified")
    register = _register(tmp_path)

    without = _inventory(tmp_path, [_row("opensoft/openxFactory")],
                         name="without.yaml")
    refused = _run_surface(tmp_path, without, register)
    assert refused.returncode == 1, refused.stdout
    assert "membership validation FAILED" in refused.stdout
    assert "opensoft/NewThing" in refused.stdout

    with_row = _inventory(tmp_path, [
        _row("opensoft/openxFactory"),
        _row("opensoft/NewThing", governance="pinned", provisional=True,
             admitted_by=[{"kind": "change", "change": "create-a-thing"}]),
    ], name="with.yaml")
    admitted = _run_surface(tmp_path, with_row, register)
    assert admitted.returncode == 0, admitted.stdout


def test_the_aggregation_repository_itself_is_admitted_by_ROOT(tmp_path):
    """Scenario *The aggregation repository itself*.

    "it SHALL carry a row for the aggregation repository, admitted by `root` …
    the row exists precisely because a superproject is not its own submodule, so
    no gitlink can admit it." `root` names NO FILE, so it is re-checked on every
    run and is always NAMED — and an author who writes a site on it is refused,
    because the site would be a file this kind does not have.
    """
    path = _inventory(tmp_path, [
        _row("opensoft/xFactory", admitted_by=[{"kind": "root"}]),
    ])
    inventory = ei.load_inventory(path)
    verdicts = ei.evidence_verdicts(inventory, tmp_path)
    assert [v.verdict for v in verdicts] == [ei.NAMED]
    assert "superproject is not its own submodule" in verdicts[0].detail

    bad = _inventory(tmp_path, [
        _row("opensoft/xFactory",
             admitted_by=[{"kind": "root", "path": "contracts/x.yaml"}]),
    ], name="rootpath.yaml")
    with pytest.raises(ei.EstateInventoryError):
        ei.load_inventory(bad)


def test_two_rows_sharing_a_BARE_NAME_refuse_the_inventory_naming_BOTH(tmp_path):
    """Scenario *Two rows share a bare name*.

    "the validator MUST REFUSE the inventory, naming both rows and the shared
    name … it MUST NOT resolve the bare spelling to either row, an ambiguous
    resolution being how an authorization lands in the wrong repository." The
    refusal is at the LOAD, so no caller ever receives an index it could pick
    from: a reader that returned one and let a caller decide would have already
    picked.
    """
    path = _inventory(tmp_path, [
        _row("opensoft/openChart", name="openChart"),
        _row("MedxSoft/openChart", name="openChart"),
    ])
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(path)
    message = str(refusal.value)
    assert "openChart" in message
    assert "opensoft/openChart" in message and "MedxSoft/openChart" in message
    assert "rows 1" in message and "2" in message

    result = _run_inventory(tmp_path, path)
    assert result.returncode == 2, result.stdout
    assert "CANNOT RUN" in result.stdout


def test_a_rows_IN_TREE_evidence_that_names_nothing_is_a_finding(tmp_path):
    """Scenario *A row's in-tree admission evidence names nothing*.

    "a pin, a workflow or a change that THIS repository's own working tree does
    not carry … MUST report a finding against that row, on every run,
    deterministically and with no network call, the evidence being a file in
    the tree it is already reading." THREE SHAPES OF ABSENCE ARE TESTED, because
    a check that asked only `is_file()` would pass the second: the file is gone;
    the file is present but no longer NAMES the repository; and the change
    directory is absent.
    """
    absent = _inventory(tmp_path, [
        _row("opensoft/Thing", governance="pinned",
             admitted_by=[{"kind": "pin", "path": "contracts/gone-pin.yaml"}]),
    ], name="absent.yaml")
    result = _run_inventory(tmp_path, absent)
    assert result.returncode == 1, result.stdout
    assert "carries no `contracts/gone-pin.yaml`" in result.stdout

    (tmp_path / "contracts").mkdir(exist_ok=True)
    (tmp_path / "contracts" / "repointed-pin.yaml").write_text(
        "source_repository: opensoft/SomethingElse\n", encoding="utf-8")
    repointed = _inventory(tmp_path, [
        _row("opensoft/Thing", governance="pinned",
             admitted_by=[{"kind": "pin",
                           "path": "contracts/repointed-pin.yaml"}]),
    ], name="repointed.yaml")
    result = _run_inventory(tmp_path, repointed)
    assert result.returncode == 1, result.stdout
    assert "no longer names" in result.stdout

    missing_change = _inventory(tmp_path, [
        _row("opensoft/Thing", governance="pinned", provisional=True,
             admitted_by=[{"kind": "change", "change": "never-existed"}]),
    ], name="missingchange.yaml")
    result = _run_inventory(tmp_path, missing_change)
    assert result.returncode == 1, result.stdout
    assert "no change `never-existed`" in result.stdout


def test_a_PROVISIONAL_row_whose_change_has_ARCHIVED_is_refused(tmp_path):
    """The enumeration requirement's expiry clause: "A row still admitted only
    by an ARCHIVED change SHALL be a finding, on the same terms as a row whose
    evidence has gone: the provisional admission outlived the act that
    justified it", and `tasks.md` § 3.3's "refuses … a still-provisional row
    whose change has archived".

    THE ARCHIVED DIRECTORY IS DATED, so the change id is a SUFFIX of the
    directory name and not the name — a check that compared the name would
    report every archived change as absent, which is the plain-absence finding
    wearing the wrong face and would name the wrong remedy.
    """
    archived = (tmp_path / "openspec" / "changes" / "archive"
                / "2026-09-18-create-a-thing")
    archived.mkdir(parents=True)
    path = _inventory(tmp_path, [
        _row("opensoft/NewThing", governance="pinned", provisional=True,
             admitted_by=[{"kind": "change", "change": "create-a-thing"}]),
    ])
    result = _run_inventory(tmp_path, path)
    assert result.returncode == 1, result.stdout
    assert "has ARCHIVED" in result.stdout
    assert "PROVISIONAL rows whose change has ARCHIVED" in result.stdout


def test_a_gitlink_row_is_NOT_RECHECKED_when_no_tree_was_supplied(tmp_path):
    """Scenario *A gitlink row is re-checked only against a supplied tree*,
    first clause.

    "the validator MUST report that row as NOT RE-CHECKED and MUST count it,
    and MUST NOT pass it silently, MUST NOT fail it, and MUST NOT fetch the
    carrying repository." The run exits 0 — the row is NOT failed — and the
    report says so in words a reader can act on.
    """
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_inventory(tmp_path, path)
    assert result.returncode == 0, result.stdout
    assert "NOT RE-CHECKED" in result.stdout
    assert "1 NOT RE-CHECKED" in result.stdout
    assert "no working tree was supplied for the carrier opensoft/xFactory" \
        in result.stdout


def test_a_VERIFIED_supplied_tree_rechecks_the_gitlink_both_ways(tmp_path):
    """Scenario *A gitlink row is re-checked only against a supplied tree*,
    second clause.

    "when that working tree IS supplied as a path input, it MUST FIRST be
    verified as a checkout of the carrier the row names … and only then MUST the
    row's `.gitmodules` evidence be re-checked in it, its absence there being a
    finding against the row." Both directions are taken in one test because the
    pair is the whole claim: a tree that CARRIES the submodule names the row,
    and the same verified tree WITHOUT it fails the row.
    """
    carried = _worktree(tmp_path, "git@github.com:opensoft/xFactory.git",
                        submodules=["opensoft/openxFactory"])
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_inventory(tmp_path, path,
                            "--estate-tree", f"opensoft/xFactory={carried}")
    assert result.returncode == 0, result.stdout
    assert "1 named in a VERIFIED supplied tree" in result.stdout

    empty = _worktree(tmp_path, "https://github.com/opensoft/xFactory",
                      submodules=[], name="empty-carrier")
    result = _run_inventory(tmp_path, path,
                            "--estate-tree", f"opensoft/xFactory={empty}")
    assert result.returncode == 1, result.stdout
    assert "VERIFIED as that carrier and its `.gitmodules` does NOT carry" \
        in result.stdout


def test_a_tree_that_is_a_DIFFERENT_repository_leaves_the_row_NOT_RECHECKED(
        tmp_path):
    """Scenario *A gitlink row is re-checked only against a supplied tree*,
    third clause — and the FIRST of the two cases `tasks.md` § 3.5 names because
    the rulings created them.

    **Ruled by Brett Heap, 2026-09-18, verbatim "Bind the carrier identity".** "a
    supplied tree that FAILS that verification leaves the row reported NOT
    RE-CHECKED and COUNTED, neither passed nor failed, the report naming the
    carrier the row expects and what the tree actually is, a path being an
    assertion and not an identity."

    THE TREE HANDED OVER CARRIES THE SUBMODULE, which is what makes this a real
    test of the BINDING rather than of the `.gitmodules` read: an arm that
    trusted the path would find the evidence and report the row NAMED. It is
    reported NOT RE-CHECKED instead, and the run does not fail — a caller's typo
    is not converted into a finding against the inventory (`design.md` D1.2's
    declined alternative).
    """
    impostor = _worktree(tmp_path, "git@github.com:opensoft/SomeoneElse.git",
                         submodules=["opensoft/openxFactory"])
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_inventory(tmp_path, path,
                            "--estate-tree", f"opensoft/xFactory={impostor}")
    assert result.returncode == 0, result.stdout
    assert "1 NOT RE-CHECKED" in result.stdout
    assert "is a checkout of opensoft/SomeoneElse, not of opensoft/xFactory" \
        in result.stdout
    assert "0 named in a VERIFIED supplied tree" in result.stdout


def test_a_tree_at_the_carriers_FORMER_address_VERIFIES_through_the_map(
        tmp_path):
    """The parenthesis of the same § 3.5 case: "(and a tree at the carrier's
    FORMER address, resolved through the transfer map, VERIFIES)".

    `design.md` D1.2's second source: "the carrier's record in
    `contracts/policies/repository-identity.yaml`, which is where this estate
    already states that a FORMER address resolves to a current one — so a
    carrier supplied at a former address verifies through the map rather than
    being refused for a name the estate itself moved."

    AND A `pending` ROW DOES NOT VERIFY IT, which is the transfer map's own
    `pending_row_rule` and not a strictness invented here: a pending row
    declares an identity change that HAS NOT HAPPENED, so it is not a
    resolution instruction for a live reference — and a working tree is as live
    a reference as there is.
    """
    _transfer_map(tmp_path, [{"former": "opensoft/codexFactory",
                              "current": "codeXfactory/codexFactory",
                              "transferred_on": datetime.date(2026, 9, 9),
                              "transfer_state": "complete"}])
    former = _worktree(tmp_path, "git@github.com:opensoft/codexFactory.git",
                       submodules=["opensoft/Nested"])
    path = _inventory(tmp_path, [
        _row("opensoft/Nested",
             admitted_by=[{"kind": "gitlink",
                           "carrier": "codeXfactory/codexFactory"}]),
    ])
    result = _run_inventory(
        tmp_path, path,
        "--estate-tree", f"codeXfactory/codexFactory={former}")
    assert result.returncode == 0, result.stdout
    assert "1 named in a VERIFIED supplied tree" in result.stdout

    _transfer_map(tmp_path, [{"former": "opensoft/codexFactory",
                              "current": "codeXfactory/codexFactory",
                              "transferred_on": None,
                              "transfer_state": "pending"}])
    result = _run_inventory(
        tmp_path, path,
        "--estate-tree", f"codeXfactory/codexFactory={former}")
    assert result.returncode == 0, result.stdout
    # NAMED ON THE ROW AND NOT ON A WHOLE-FILE COUNT: the carrier binding means
    # this inventory also carries the carriers' own rows, whose gitlinks nobody
    # supplied a tree for and which are NOT RE-CHECKED for that ordinary
    # reason. The subject here is THIS row and the pending map, so this is what
    # is asserted.
    assert "0 named in a VERIFIED supplied tree" in result.stdout
    assert "opensoft/Nested (gitlink in codeXfactory/codexFactory):" \
        in result.stdout
    assert "is a checkout of opensoft/codexFactory, not of " \
        "codeXfactory/codexFactory" in result.stdout


def test_the_inventory_carrying_a_FORMER_address_reports_the_current_one(
        tmp_path):
    """Scenario *The inventory carries a former address*.

    "MUST report a finding against that row, naming the current address the
    transfer map resolves … the remedy is the respelling, the inventory
    carrying current addresses only." REPORTED, not refused: the run exits 0 and
    the current address is printed, so the remedy needs no lookup.
    """
    _transfer_map(tmp_path, [{"former": "opensoft/codexFactory",
                              "current": "codeXfactory/codexFactory",
                              "transferred_on": datetime.date(2026, 9, 9),
                              "transfer_state": "complete"}])
    path = _inventory(tmp_path, [
        _row("opensoft/codexFactory", name="codexFactory"),
    ])
    result = _run_inventory(tmp_path, path)
    assert result.returncode == 0, result.stdout
    assert "FORMER address" in result.stdout
    assert "codeXfactory/codexFactory" in result.stdout


def test_the_five_kinds_and_the_three_classes_are_CLOSED(tmp_path):
    """The requirement's two closed sets, enforced at the LOAD and not merely
    asserted by a test over the inventory this repository happens to carry — so
    a consuming tree gets the same refusals this one does.

    "the admissible kinds SHALL be exactly these five, because they are exactly
    the ways this estate has ever named a repository"; "it SHALL be one of
    three: `governed` … `pinned` … `external`".
    """
    kind = _inventory(tmp_path, [
        _row("opensoft/Thing",
             admitted_by=[{"kind": "handshake", "path": "contracts/x.yaml"}]),
    ], name="kind.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(kind)
    assert "handshake" in str(refusal.value)

    klass = _inventory(tmp_path, [
        _row("opensoft/Thing", governance="vendored"),
    ], name="class.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(klass)
    assert "vendored" in str(refusal.value)
    assert ei.GOVERNANCE_CLASSES == ("governed", "pinned", "external")
    assert ei.ADMISSION_KINDS == ("gitlink", "pin", "workflow", "root",
                                  "change")


def test_nothing_author_controlled_becomes_a_path_before_it_is_shape_checked(
        tmp_path):
    """The house rule, restated for this file's two path-bearing kinds and its
    one id-bearing kind. A `change:` that is a path, a `pin:` path that is
    absolute or climbs out with `..`, and a `pin:` filed under another kind's
    directory are all refused at the LOAD, because every consumer resolves them
    under the scanned tree.
    """
    for row, needle in (
        (_row("opensoft/Thing", governance="pinned", provisional=True,
              admitted_by=[{"kind": "change", "change": "../../etc"}]),
         "change-directory name"),
        (_row("opensoft/Thing", governance="pinned",
              admitted_by=[{"kind": "pin", "path": "/etc/passwd"}]),
         "repository-relative"),
        (_row("opensoft/Thing", governance="pinned",
              admitted_by=[{"kind": "pin", "path": "contracts/../../x.yaml"}]),
         "repository-relative"),
        (_row("opensoft/Thing", governance="pinned",
              admitted_by=[{"kind": "pin",
                            "path": ".github/workflows/x.yml"}]),
         "not under `contracts/`"),
    ):
        path = _inventory(tmp_path, [row], name=f"p{abs(hash(needle))}.yaml")
        with pytest.raises(ei.EstateInventoryError) as refusal:
            ei.load_inventory(path)
        assert needle in str(refusal.value)


def test_an_inventory_reached_through_a_SYMLINK_is_refused_unread(tmp_path):
    """`code_surface.load_register`'s guard, mirrored exactly rather than
    approximated. `Path.is_file()` and `Path.read_text()` BOTH follow symlinks,
    so without this a committed link would let the gate resolve membership
    against bytes from outside the checkout, silently and differently per
    runner. BOTH POSITIONS are taken: the leaf, and an ANCESTOR directory whose
    own leaf is an entirely ordinary file.
    """
    real = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    leaf = tmp_path / "linked.yaml"
    leaf.symlink_to(real)
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(leaf)
    assert "symlink" in str(refusal.value)

    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    (elsewhere / "inventory.yaml").write_text(
        real.read_text(encoding="utf-8"), encoding="utf-8")
    linkdir = tmp_path / "linkdir"
    linkdir.symlink_to(elsewhere, target_is_directory=True)
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(linkdir / "inventory.yaml")
    assert "symlink" in str(refusal.value)


def test_a_malformed_inventory_REFUSES_rather_than_reading_short(tmp_path):
    """An inventory that cannot be USED refuses rather than being ignored:
    ignored, every declared identifier would resolve against nothing and a
    fail-closed arm would refuse the whole corpus while the defect is one
    unreadable file. The strict loader's own refusals are CONSUMED here (an
    anchor, an alias, a duplicate key), not re-implemented.
    """
    for text, needle in (
        ("schema_version: 2\nkind: estate-repository-inventory\n"
         "repositories: []\n", "schema_version: 1"),
        ("schema_version: 1\nkind: something-else\nrepositories: []\n",
         "kind: estate-repository-inventory"),
        ("schema_version: 1\nkind: estate-repository-inventory\n"
         "repositories: []\n", "non-empty top-level `repositories:` list"),
        ("schema_version: 1\nkind: estate-repository-inventory\n"
         "repositories:\n  - &a {repository: a/b}\n", "anchor"),
        ("schema_version: 1\nkind: estate-repository-inventory\n"
         "kind: estate-repository-inventory\nrepositories: []\n",
         "duplicate key"),
    ):
        path = tmp_path / f"m{abs(hash(needle))}.yaml"
        path.write_text(text, encoding="utf-8")
        with pytest.raises(ei.EstateInventoryError) as refusal:
            ei.load_inventory(path)
        assert needle in str(refusal.value), (needle, str(refusal.value))


# ==============================================================================
# *A declared repository is judged for membership against the estate inventory*
# ==============================================================================


def test_a_head_naming_a_repository_the_inventory_CARRIES_passes(tmp_path):
    """Scenario *A head names a repository the inventory carries*."""
    _proposal(tmp_path, "a-change",
              "code_surface: opensoft/openxFactory — the surface\n")
    path = _inventory(tmp_path, [
        _row("opensoft/openxFactory"),
        _row("opensoft/openDox", governance="pinned"),
    ])
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 0, result.stdout
    assert "1 carried by the estate inventory" in result.stdout


def test_a_head_naming_a_PLAUSIBLE_MISSPELLING_fails_closed(tmp_path):
    """Scenario *A head names a plausible misspelling*.

    "MUST fail, naming the proposal's path, the identifier, and the inventory it
    was resolved against … MUST NOT admit the identifier on the strength of its
    shape, and MUST NOT resolve it by asking the provider." `openxFactorie` is a
    head the GRAMMAR admits — it is a well-shaped bare name — which is exactly
    why the grammar arm cannot catch it and this arm must.
    """
    _proposal(tmp_path, "a-change", "code_surface: openxFactorie\n")
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 1, result.stdout
    assert "membership validation FAILED" in result.stdout
    assert "openxFactorie" in result.stdout
    assert "openspec/changes/a-change/proposal.md" in result.stdout
    assert path.name in result.stdout
    assert "FAILS CLOSED" in result.stdout


def test_a_head_written_as_a_BARE_NAME_resolves_to_the_row(tmp_path):
    """Scenario *A head is written as a bare repository name*.

    "the validator resolves it to that row and passes, both spellings being ones
    the corpus writes." Measured at the authoring: 30 of the 33 occurrences in
    the live corpus are bare.
    """
    _proposal(tmp_path, "a-change", "code_surface: openxFactory\n")
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 0, result.stdout
    assert ei.resolve(ei.load_inventory(path), "openxFactory").how == ei.BY_NAME


def test_a_head_naming_an_EXTERNAL_row_is_refused_NAMING_THE_CLASS(tmp_path):
    """Scenario *A head names an external repository*.

    "MUST fail, naming the governance class rather than reporting the identifier
    as unknown … the distinction is the point of carrying the row at all." An
    `external` row exists so KNOWN-BUT-NOT-OURS is distinguishable from UNKNOWN,
    which is a distinction no validator can draw from absence.
    """
    _proposal(tmp_path, "a-change", "code_surface: Fission-AI/OpenSpec\n")
    path = _inventory(tmp_path, [
        _row("opensoft/openxFactory"),
        _row("Fission-AI/OpenSpec", governance="external",
             admitted_by=[{"kind": "pin",
                           "path": "contracts/openspec-cli-pin.yaml"}]),
    ])
    (tmp_path / "contracts").mkdir(exist_ok=True)
    (tmp_path / "contracts" / "openspec-cli-pin.yaml").write_text(
        "source_repository: Fission-AI/OpenSpec\n", encoding="utf-8")
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 1, result.stdout
    # THE ASSERTION IS ON THE REFUSAL LINE AND NOT ON THE WHOLE RUN, because
    # "does not carry" is also the ordinary wording of the archive count line —
    # and the claim under test is about WHICH refusal this is, not about a
    # phrase appearing nowhere in the output.
    refusal = [line for line in result.stdout.splitlines()
               if "a-change/proposal.md" in line]
    assert len(refusal) == 1, result.stdout
    assert "EXTERNAL" in refusal[0]
    assert "does not carry" not in refusal[0]


def test_a_head_naming_a_FORMER_address_is_REPORTED_and_never_refused(tmp_path):
    """Scenario *A head names a former address*.

    "MUST report a finding and MUST NOT refuse the proposal, the identifier
    being interpretable … the finding names the current address, so the remedy
    is a respelling the author can take without a lookup." `design.md` D5's
    declined alternative was REFUSE, costed as redding "a required check on a
    packet whose declaration everybody can read" — so the exit code is 0.
    """
    _transfer_map(tmp_path, [{"former": "opensoft/codexFactory",
                              "current": "codeXfactory/codexFactory",
                              "transferred_on": datetime.date(2026, 9, 9),
                              "transfer_state": "complete"}])
    _proposal(tmp_path, "a-change", "code_surface: opensoft/codexFactory\n")
    path = _inventory(tmp_path, [
        _row("codeXfactory/codexFactory", name="codexFactory"),
    ])
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 0, result.stdout
    assert "FORMER address" in result.stdout
    assert "codeXfactory/codexFactory" in result.stdout
    assert "membership validation FAILED" not in result.stdout


def test_an_inventory_row_NOTHING_NAMES_reports_and_does_not_fail_the_arm(
        tmp_path):
    """Scenario *An inventory row nothing names*.

    "it MUST be reported as a finding against the row, and MUST NOT fail the
    declaration arm … the remedy is to retire the row in the pull request that
    made it stale." The asymmetry is the closed register's own and the
    requirement names it as such: an identifier the inventory does not carry
    FAILS (exit 1), a row nothing names REPORTS (exit 2, the register's own
    stale disposition) — and the DECLARATION is not what failed, which the
    report says in words.
    """
    _proposal(tmp_path, "a-change", "code_surface: openxFactory\n")
    path = _inventory(tmp_path, [
        _row("opensoft/openxFactory"),
        _row("opensoft/Gone", governance="pinned",
             admitted_by=[{"kind": "pin", "path": "contracts/gone-pin.yaml"}]),
    ])
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 2, result.stdout
    assert "no longer carries" in result.stdout
    assert "never against a declaration" in result.stdout
    assert "membership validation FAILED" not in result.stdout


def test_a_gitlink_row_reaches_the_membership_arm_as_NOT_RECHECKED(tmp_path):
    """The same scenario's second clause: "a row admitted by a `gitlink` whose
    carrying tree was not supplied, or whose supplied tree does not verify as
    the carrier the row names, MUST be reported as NOT RE-CHECKED instead, the
    evidence living in a tree this checkout does not contain."

    AND THE ARM TAKES NO TREE ARGUMENT AT ALL (`tasks.md` § 3.4), so from here
    EVERY gitlink row is NOT RE-CHECKED, on every machine, always — which is
    what makes the required check's verdict machine-independent.
    """
    _proposal(tmp_path, "a-change", "code_surface: openxFactory\n")
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 0, result.stdout
    assert "1 NOT RE-CHECKED" in result.stdout
    assert "--estate-tree" in result.stdout
    assert "takes no tree argument" in result.stdout


def test_a_REGISTERED_declaration_is_not_judged_and_there_is_NO_FALLBACK(
        tmp_path):
    """Scenario *A registered declaration reaches the membership arm*.

    "membership MUST NOT be judged for that proposal … the arm MUST NOT fall
    back to the whole declaration, to the gloss, or to an empty set." The
    registered declaration below NAMES `openxFactorie` inside its unreadable
    text: a whole-declaration fallback would resolve that word and FAIL, and an
    empty-set fallback would pass it for a reason nobody stated. It is counted
    as registered-and-not-judged, and neither happens.
    """
    declaration = ("openxFactorie's surface, and openxFactory too")
    _proposal(tmp_path, "a-change", f"code_surface: {declaration}\n")
    register = _register(tmp_path, _entry_text("a-change", declaration))
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_surface(tmp_path, path, register)
    assert result.returncode == 0, result.stdout
    assert "1 registered and not judged" in result.stdout
    assert "0 readable heads" in result.stdout
    assert "membership validation FAILED" not in result.stdout


def test_the_empty_surface_and_an_absent_declaration_resolve_nothing(tmp_path):
    """Scenario *A proposal declares the empty surface or declares nothing*.

    "there is no identifier to resolve and the membership arm passes." Both
    carriers are put in one tree, because the two are the same fact — the
    promoted doc-only default — reached by writing it and by omitting it.
    """
    _proposal(tmp_path, "declares-none",
              "code_surface: none — a doc-only change\n")
    _proposal(tmp_path, "declares-nothing", "target_release: implemented\n")
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 0, result.stdout
    assert "0 readable heads naming 0 distinct identifiers" in result.stdout


def test_an_ARCHIVED_proposal_naming_an_uncarried_repository_is_never_a_finding(
        tmp_path):
    """Scenario *An archived proposal names a repository the inventory does not
    carry*.

    "it MUST NOT be a finding, the archived record being frozen … the run
    reports how many such records the archive carries." An archived packet's
    front matter is beyond a plain fix (`record-immutability`,
    `govern-archived-record-edits`), so a gate demanding an edit nobody may make
    would be a standing finding with no remedy — the defect this estate disposes
    of rather than creates. THE SAME TEXT IS PUT IN AN ACTIVE PACKET TOO, so the
    test proves the archive is EXEMPT rather than that the identifier is
    harmless.
    """
    _proposal(tmp_path, "a-retired-change",
              "code_surface: opensoft/LongGone\n", archived=True)
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    register = _register(tmp_path)
    result = _run_surface(tmp_path, path, register)
    assert result.returncode == 0, result.stdout
    assert "1 records name a repository the inventory does not carry" \
        in result.stdout

    _proposal(tmp_path, "a-live-change", "code_surface: opensoft/LongGone\n")
    result = _run_surface(tmp_path, path, register)
    assert result.returncode == 1, result.stdout
    assert "opensoft/LongGone" in result.stdout


# ==============================================================================
# The `## MODIFIED` paragraph: SHAPE is the grammar arm's, MEMBERSHIP is this
# arm's, and both report in ONE run
# ==============================================================================


def test_the_grammar_judges_SHAPE_and_the_membership_arm_judges_MEMBERSHIP(
        tmp_path):
    """The one paragraph the `## MODIFIED` block moves.

    "THE GRAMMAR ARM SHALL JUDGE THE IDENTIFIER'S SHAPE AND SHALL NOT JUDGE ITS
    MEMBERSHIP, the two being separate questions with separate remedies: a head
    the grammar refuses is re-punctuated by its author, and a head naming a
    repository the estate does not carry is either corrected or the repository
    is admitted. MEMBERSHIP SHALL BE JUDGED, by the arm … against the
    enumeration …"

    THE TWO ARMS ARE PROVED SEPARATE BY PUTTING ONE CARRIER OF EACH IN ONE TREE
    and requiring BOTH blocks in ONE run's output. `parse_head` — the grammar —
    still admits the misspelling, which is the half of the sentence that did NOT
    move; the membership arm refuses it, which is the half that did.
    """
    cs_module = _load("code_surface", ROOT / "scripts" / "code_surface.py")
    assert cs_module.parse_head("openxFactorie").repositories == \
        ("openxFactorie",)

    _proposal(tmp_path, "shape-defect",
              "code_surface: openxFactory's surface\n")
    _proposal(tmp_path, "membership-defect", "code_surface: openxFactorie\n")
    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_surface(tmp_path, path, _register(tmp_path))
    assert result.returncode == 1, result.stdout
    assert "code_surface validation FAILED" in result.stdout
    assert "membership validation FAILED" in result.stdout
    assert "code_surface:" in result.stdout and "membership:" in result.stdout


def test_the_inventory_is_the_SCANNED_TREES_or_it_is_NOTHING(tmp_path):
    """THE DEFECT THIS REPOSITORY ALREADY NAMED, CLOSED FOR THE INVENTORY TOO.

    `tests/code_surface/test_code_surface_gate.py`'s
    `test_a_scanned_tree_with_NO_register_is_NOT_judged_against_the_HOUSE_one`
    put it for the closed register: "A tree was then judged against exceptions
    it does not carry, silently, in a message that named an entry and told its
    author to delete it from a file they do not have." An inventory falls to the
    same failure wearing a worse face — the arm FAILS CLOSED, so a tree judged
    against an enumeration it does not carry is refused for not belonging to an
    estate it is no part of, and EVERY declaration in EVERY other tree would
    red.

    THE ABSENCE IS REPORTED AND NEVER SILENT, because a membership gate that
    quietly judged nothing is the gate not running.
    """
    _proposal(tmp_path, "a-change", "code_surface: NotOfThisEstate\n")
    register = _register(tmp_path)
    assert not (tmp_path / "scripts").exists()

    result = _run_surface(tmp_path, None, register)
    assert result.returncode == 0, result.stdout
    assert "membership: NOT JUDGED" in result.stdout
    assert "membership validation FAILED" not in result.stdout
    assert "NotOfThisEstate" not in result.stdout

    # AND A TREE THAT DOES CARRY ONE IS JUDGED AGAINST ITS OWN, with no flag.
    _tree_inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_surface(tmp_path, None, register)
    assert result.returncode == 1, result.stdout
    assert "membership validation FAILED" in result.stdout
    assert "NotOfThisEstate" in result.stdout


def test_a_scanned_tree_inventory_that_CANNOT_BE_USED_refuses_not_falls_back(
        tmp_path):
    """The named flag's semantics, for the file the tree carries whether or not
    an operator typed its path — the sibling's rule exactly
    (`test_a_scanned_tree_register_that_CANNOT_BE_USED_refuses_not_falls_back`).
    The direction that matters is the one the fallback would take: not to
    nothing, but to the inventory BESIDE THIS VALIDATOR, which would judge a
    foreign tree against this estate.
    """
    _proposal(tmp_path, "a-change", "code_surface: openxFactory\n")
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / ei.INVENTORY_PATH.name).write_text(
        "repositories: [this is not a closed sequence\n", encoding="utf-8")
    result = _run_surface(tmp_path, None, _register(tmp_path))
    assert result.returncode == 2, result.stdout
    assert "membership validation CANNOT RUN" in result.stdout
    assert "does NOT fall back" in result.stdout
    assert "Traceback" not in result.stderr, result.stderr


def test_a_NAMED_inventory_that_is_missing_REFUSES_rather_than_not_judging(
        tmp_path):
    """The asymmetry between the flag and the default, which is the register's
    own: an operator who NAMES a file asked for that file, so its absence
    REFUSES; a tree that merely carries none is not judged. Collapsing the two
    would let a typo'd `--inventory` read as "no inventory here" and pass.
    """
    _proposal(tmp_path, "a-change", "code_surface: openxFactorie\n")
    result = _run_surface(tmp_path, tmp_path / "absent.yaml",
                          _register(tmp_path))
    assert result.returncode == 2, result.stdout
    assert "membership validation CANNOT RUN" in result.stdout
    assert "does not exist" in result.stdout


def test_an_inventory_that_cannot_be_used_STOPS_the_run(tmp_path):
    """An inventory that cannot be used REFUSES rather than being ignored.

    Ignored, every declared identifier would resolve against nothing and the
    fail-closed arm would refuse EVERY declaration in the corpus — reporting a
    whole-corpus failure where the defect is one unreadable file. The grammar
    report is still printed, so a run that cannot judge membership still says
    what it did judge.
    """
    _proposal(tmp_path, "a-change", "code_surface: openxFactory\n")
    result = _run_surface(tmp_path, tmp_path / "absent.yaml",
                          _register(tmp_path))
    assert result.returncode == 2, result.stdout
    assert "membership validation CANNOT RUN" in result.stdout
    assert "code_surface: 1 active proposals" in result.stdout


# ==============================================================================
# the live corpus
# ==============================================================================


def test_corpus_estate_inventory_validates():
    """THE GATE. This repository's own inventory is well-shaped and every
    in-tree admission it records is named by this working tree. A row whose pin,
    workflow or change has gone reds the required `pytest-suite` with no
    workflow edit."""
    result = subprocess.run(
        [sys.executable, str(INVENTORY_VALIDATOR), str(ROOT)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr


def test_corpus_code_surface_and_membership_validate():
    """THE OTHER GATE, AND IT IS ONE RUN. Every active declaration's head is
    admitted by the grammar or by a live register entry, AND every identifier a
    readable head names is carried by the estate inventory."""
    result = subprocess.run(
        [sys.executable, str(SURFACE_VALIDATOR), str(ROOT)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "membership:" in result.stdout


def test_the_live_corpus_REDS_when_a_declaration_names_an_uncarried_repository(
        tmp_path):
    """`tasks.md` § 3.5's LIVE-CORPUS case, put as the event rather than as an
    assertion about today: a declaration naming a repository no row carries REDS
    `pytest-suite`.

    IT IS JUDGED AGAINST THE REAL INVENTORY AND THE REAL REGISTER, not against a
    fixture, which is what makes it a statement about the gate this repository
    actually runs. The tree is a tmpdir carrying ONE proposal, so the case is
    the arm's verdict and not a fact about the rest of the corpus.
    """
    _proposal(tmp_path, "a-change",
              "code_surface: opensoft/NotInTheEstate — a surface nobody admitted\n")
    result = subprocess.run(
        [sys.executable, str(SURFACE_VALIDATOR), str(tmp_path),
         "--inventory", str(INVENTORY), "--register", str(REGISTER)],
        capture_output=True, text=True)
    assert result.returncode == 1, result.stdout
    assert "opensoft/NotInTheEstate" in result.stdout


def test_every_live_row_resolves_by_BOTH_spellings():
    """Over the real file: every row is reachable by its address and by its bare
    name, which is the pair of spellings the corpus writes and the pair the arm
    must resolve. A row reachable by only one would be a row half the corpus
    could not name."""
    inventory = ei.load_inventory(INVENTORY)
    assert len(inventory.rows) == len({r.name for r in inventory.rows})
    for row in inventory.rows:
        assert ei.resolve(inventory, row.repository).row is row, row.repository
        assert ei.resolve(inventory, row.name).row is row, row.name


def test_every_live_declared_identifier_is_CARRIED_by_the_inventory():
    """The measurement `design.md` D0.3 took and `tasks.md` § 2.4 ticked, held
    as a TEST rather than as a recorded number: every identifier every readable
    active head names resolves, so the membership arm refuses nothing in this
    corpus. This is the property that makes the arm landable, and it is the one
    that would break first if a lane declared a surface in a repository the
    inventory does not carry."""
    cs_module = _load("code_surface", ROOT / "scripts" / "code_surface.py")
    inventory = ei.load_inventory(INVENTORY)
    transfers, transfer_findings = ei.load_transfers(ROOT)
    assert transfer_findings == (), transfer_findings
    register = {(e["change"], e["declaration"])
                for e in cs_module.load_register()}
    unresolved = []
    for proposal in cs_module._proposals(ROOT, archived=False):
        try:
            present, text = cs_module.declaration(proposal)
        except cs_module.CodeSurfaceError:
            continue
        if not present or text is None:
            continue
        try:
            head = cs_module.parse_head(text)
        except cs_module.CodeSurfaceError:
            assert (proposal.parent.name, text) in register, proposal.parent.name
            continue
        for identifier in head.repositories:
            if not ei.resolve(inventory, identifier, transfers).resolved:
                unresolved.append((proposal.parent.name, identifier))
    assert not unresolved, unresolved


def test_the_live_inventory_records_every_admission_kind_it_defines():
    """The five kinds are CLOSED because they are exactly the ways this estate
    has named a repository — so every one of them is exercised by the file
    itself, and a kind nothing used would be a kind the measurement did not
    find."""
    inventory = ei.load_inventory(INVENTORY)
    kinds = {a.kind for row in inventory.rows for a in row.admitted_by}
    assert kinds == set(ei.ADMISSION_KINDS)
    classes = {row.governance for row in inventory.rows}
    assert classes == set(ei.GOVERNANCE_CLASSES)


def test_the_live_inventory_stays_under_the_strict_loaders_byte_ceiling():
    """The inventory is read through the same ceiling every front-matter block
    is, and it grows by a row every four days (`design.md` D0.6). Measured
    rather than assumed, with the headroom named: a future row that would cross
    the ceiling is a fact the gate should surface here rather than at a run."""
    size = len(INVENTORY.read_text(encoding="utf-8").encode("utf-8"))
    ceiling = importlib.import_module("frontmatter_strict").CEILING_BYTES
    assert size < ceiling, (size, ceiling)


def test_the_live_codexFactory_row_is_admitted_by_gitlink_and_workflow_only():
    """`design.md` D0.2 row 3 also named `pin (review-lane-pin.yaml)`, which
    this loader's OWN closed `pin` kind cannot lawfully hold:
    `contracts/review-lane-pin.yaml` is `kind: pinned_workflow`, a
    commit-only pin of EXECUTABLE GOVERNANCE CODE with no digest set, and the
    row is `governance: governed` rather than `pinned` — row 3 failed both of
    the kind's own clauses. RULED by Brett Heap, 2026-09-21, verbatim "Drop
    the pin admission on row 3": the row now carries its `gitlink` (this
    aggregation) and its real `workflow` evidence
    (`.github/workflows/merge-master-approval.yml`) and nothing else. The
    packet's own D0.2 row 3 is amended on the same word, in a separate
    change; this loader's `pin` kind and its definition are UNCHANGED.
    """
    inventory = ei.load_inventory(INVENTORY)
    resolution = ei.resolve(inventory, "codeXfactory/codexFactory")
    assert resolution.resolved is True
    row = resolution.row
    assert row is not None
    assert {a.kind for a in row.admitted_by} == {ei.GITLINK, ei.WORKFLOW}
    assert row.governance == "governed"
    workflow_paths = {a.path for a in row.admitted_by if a.kind == ei.WORKFLOW}
    assert workflow_paths == {".github/workflows/merge-master-approval.yml"}


# ==============================================================================
# THE REVIEW ROUND OF PR #1119: ten hardening cases, one per finding
#
# EACH IS WRITTEN TO FAIL AGAINST THE TREE WITHOUT ITS FIX, on the same
# fails-then-passes obligation `tasks.md` § 3.5 puts on every case above, and
# each names the hole in the pre-fix reader rather than describing the fix. The
# subject of all ten is the same sentence read strictly: an admission is
# CHECKABLE AGAINST THE TREE, so every part of the evidence — the host an origin
# URL names, the carrier a gitlink names, the whole of an address, the exact
# archived directory, the ratification of a change, the symlink under a path —
# is part of what is checked, and anything left unchecked is a place a row can
# be admitted on evidence nobody looked at.
# ==============================================================================


def test_an_origin_on_A_FOREIGN_HOST_is_not_this_estates_carrier(tmp_path):
    """The ruling verifies a tree BY ITS OWN ORIGIN URL, and a URL's HOST is
    part of it.

    A normalization that kept the `<owner>/<name>` PATH and discarded the HOST
    made `git@attacker.example:opensoft/xFactory.git` verify as this estate's
    aggregation, so a tree nobody here wrote could discharge — or condemn — a
    row. That is the substitution "Bind the carrier identity" refuses, arriving
    one field to the left of the path it was ruled about.
    """
    assert ei.normalize_origin("git@github.com:opensoft/xFactory.git") == \
        "opensoft/xFactory"
    assert ei.normalize_origin("https://github.com/opensoft/xFactory") == \
        "opensoft/xFactory"
    assert ei.normalize_origin(
        "git@attacker.example:opensoft/xFactory.git") is None
    assert ei.normalize_origin(
        "https://gitlab.example/opensoft/xFactory.git") is None

    impostor = _worktree(tmp_path, "git@attacker.example:opensoft/xFactory.git",
                         submodules=["opensoft/openxFactory"])
    check = ei.carrier_identity(impostor, "opensoft/xFactory")
    assert check.verified is False
    assert check.observed is None

    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_inventory(tmp_path, path,
                            "--estate-tree", f"opensoft/xFactory={impostor}")
    assert result.returncode == 0, result.stdout
    assert "0 named in a VERIFIED supplied tree" in result.stdout
    assert "no origin URL could be read" in result.stdout


def test_a_gitlink_CARRIER_must_resolve_to_a_GOVERNED_row(tmp_path):
    """"a GOVERNED ESTATE REPOSITORY's `.gitmodules`" is the kind's own first
    clause, and it is the clause the loader did not enforce.

    A carrier was accepted on its SHAPE alone, so a row could claim evidence
    from a repository this inventory carries no row for at all, or from one it
    carries as `pinned` or `external` — and a supplied checkout of that
    repository would then discharge the row. Membership would rest on a tree
    nobody in this estate writes.
    """
    unknown = _inventory(tmp_path, [
        _row("opensoft/Thing",
             admitted_by=[{"kind": "gitlink", "carrier": "opensoft/Nowhere"}]),
    ], name="unknown.yaml", bind_carriers=False)
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(unknown)
    assert "CARRIES NO ROW FOR" in str(refusal.value)

    ungoverned = _inventory(tmp_path, [
        _row("opensoft/Thing",
             admitted_by=[{"kind": "gitlink",
                           "carrier": "Fission-AI/OpenSpec"}]),
        _row("Fission-AI/OpenSpec", governance="external",
             admitted_by=[{"kind": "pin", "path": "contracts/cli-pin.yaml"}]),
    ], name="ungoverned.yaml", bind_carriers=False)
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(ungoverned)
    assert "governance: external" in str(refusal.value)

    # AND THE LAWFUL SHAPE STILL LOADS, so the guard refuses the carrier it
    # should and nothing else.
    lawful = _inventory(tmp_path, [_row("opensoft/Thing")], name="lawful.yaml")
    assert len(ei.load_inventory(lawful).rows) == 2


def test_evidence_naming_a_LONGER_address_does_not_discharge_a_shorter_row(
        tmp_path):
    """"`<pin path>` names `<repository>`" was answered by a SUBSTRING test, and
    a substring is not a naming.

    `opensoft/openXwallet` contains the characters of `opensoft/open`, so a pin
    that names only the first discharged a row for the second — an admission
    re-checked as NAMED on evidence that is about a different repository. The
    address is matched on its own boundaries instead, and the ordinary lawful
    spellings (a bare address, one inside a URL, one with a `.git` suffix) still
    discharge.
    """
    contracts = tmp_path / "contracts"
    contracts.mkdir(parents=True, exist_ok=True)
    (contracts / "wallet-pin.yaml").write_text(
        "source_repository: opensoft/openXwallet\n", encoding="utf-8")
    path = _inventory(tmp_path, [
        _row("opensoft/open", governance="pinned",
             admitted_by=[{"kind": "pin", "path": "contracts/wallet-pin.yaml"}]),
    ])
    verdicts = ei.evidence_verdicts(ei.load_inventory(path), tmp_path)
    prefix = [v for v in verdicts if v.row.repository == "opensoft/open"]
    assert [v.verdict for v in prefix] == [ei.GONE]
    assert "no longer names `opensoft/open`" in prefix[0].detail

    (contracts / "dox-pin.yaml").write_text(
        "# mounts the assembly root\n"
        "source_url: https://github.com/opensoft/openDox.git\n"
        "# `opensoft/openDox-code` carries no migrations directory yet\n",
        encoding="utf-8")
    urls = _inventory(tmp_path, [
        _row("opensoft/openDox", governance="pinned",
             admitted_by=[{"kind": "pin", "path": "contracts/dox-pin.yaml"}]),
    ], name="urls.yaml")
    named = [v for v in ei.evidence_verdicts(ei.load_inventory(urls), tmp_path)
             if v.row.repository == "opensoft/openDox"]
    assert [v.verdict for v in named] == [ei.NAMED]


def test_an_archived_id_that_merely_ENDS_WITH_the_change_is_not_that_change(
        tmp_path):
    """A PROVISIONAL row expires at ITS OWN change's archive and at no other's.

    `endswith` made every id that ends with another id answer for it, so
    `2026-09-18-recreate-a-thing` reported `create-a-thing` as archived — a live
    provisional row told to retire on an act that was some other change's. The
    dated separator is what makes the id's first character a boundary, so it is
    required.
    """
    archive = tmp_path / "openspec" / "changes" / "archive"
    (archive / "2026-09-18-recreate-a-thing").mkdir(parents=True)
    path = _inventory(tmp_path, [
        _row("opensoft/NewThing", governance="pinned", provisional=True,
             admitted_by=[{"kind": "change", "change": "create-a-thing"}]),
    ])
    verdict = [v for v in ei.evidence_verdicts(ei.load_inventory(path),
                                               tmp_path)
               if v.admission.kind == ei.CHANGE][0]
    assert verdict.verdict == ei.GONE
    assert "carries no change `create-a-thing`, active or archived" \
        in verdict.detail
    assert "has ARCHIVED" not in verdict.detail

    # AND ITS OWN DATED DIRECTORY STILL ANSWERS FOR IT.
    (archive / "2026-09-18-create-a-thing").mkdir(parents=True)
    verdict = [v for v in ei.evidence_verdicts(ei.load_inventory(path),
                                               tmp_path)
               if v.admission.kind == ei.CHANGE][0]
    assert "has ARCHIVED" in verdict.detail


def test_ROOT_admits_the_aggregation_row_and_no_other(tmp_path):
    """`root` NAMES NO FILE, so it is the one admission no run can contradict —
    which is why it means ONE repository.

    `evidence_verdicts` marks a `root` admission NAMED unconditionally, and
    correctly: the aggregation is real and a superproject is not its own
    submodule. Accepted on ANY row, that made it the estate's open door — write
    `kind: root` on any address and the row walks in on evidence nobody is able
    to look at.
    """
    interloper = _inventory(tmp_path, [
        _row("opensoft/Interloper", admitted_by=[{"kind": "root"}]),
    ], name="interloper.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(interloper)
    assert "admits `opensoft/xFactory` and no other repository" \
        in str(refusal.value)

    lawful = _inventory(tmp_path, [
        _row(ei.AGGREGATION_ROOT, admitted_by=[{"kind": "root"}]),
    ], name="lawful-root.yaml")
    assert [v.verdict for v in
            ei.evidence_verdicts(ei.load_inventory(lawful), tmp_path)] == \
        [ei.NAMED]


def test_a_bare_name_that_is_not_the_address_FINAL_SEGMENT_is_refused(
        tmp_path):
    """The two columns are ONE repository written two ways, and they are held to
    agree.

    `name:` was checked for repository-name SYNTAX and never against
    `repository:`, so a row could read `repository: opensoft/openxFactory,
    name: trusted` — making the bare head `trusted` authorize that repository
    while `openxFactory`, the spelling the corpus actually writes, resolved to
    nothing at all.
    """
    mislabelled = _inventory(tmp_path, [
        _row("opensoft/openxFactory", name="trusted"),
    ], name="mislabelled.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(mislabelled)
    assert "final segment" in str(refusal.value)

    lawful = _inventory(tmp_path, [_row("opensoft/openxFactory")],
                        name="lawful-name.yaml")
    inventory = ei.load_inventory(lawful)
    assert ei.resolve(inventory, "openxFactory").resolved is True


def test_a_supplied_carriers_SYMLINKED_gitmodules_is_refused_unread(tmp_path):
    """A SUPPLIED TREE IS THE ONE TREE THIS REPOSITORY DID NOT WRITE, so the
    module's own no-symlink rule reaches it too.

    `Path.is_file()` and `Path.read_text()` both FOLLOW LINKS, so a carrier
    presenting `.gitmodules` as a symlink had the validator re-check a row
    against bytes from wherever that link points. The tree VERIFIES as the
    carrier and its `.gitmodules` is still not read: the verdict is NOT
    RE-CHECKED, which is the one this arm has for evidence it could not look at.
    """
    outside = tmp_path / "outside" / "planted-gitmodules"
    outside.parent.mkdir(parents=True, exist_ok=True)
    outside.write_text('[submodule "openxFactory"]\n'
                       '\tpath = openxFactory\n'
                       '\turl = git@github.com:opensoft/openxFactory.git\n',
                       encoding="utf-8")
    carrier = _worktree(tmp_path, "git@github.com:opensoft/xFactory.git")
    (carrier / ".gitmodules").symlink_to(outside)

    assert ei.carrier_identity(carrier, "opensoft/xFactory").verified is True
    assert ei.gitmodules_addresses(carrier) is None

    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    result = _run_inventory(tmp_path, path,
                            "--estate-tree", f"opensoft/xFactory={carrier}")
    assert result.returncode == 0, result.stdout
    assert "its `.gitmodules` could not be read" in result.stdout
    assert "0 named in a VERIFIED supplied tree" in result.stdout

    # A REAL FILE IN THE SAME PLACE STILL DISCHARGES THE ROW.
    (carrier / ".gitmodules").unlink()
    (carrier / ".gitmodules").write_text(outside.read_text(encoding="utf-8"),
                                         encoding="utf-8")
    result = _run_inventory(tmp_path, path,
                            "--estate-tree", f"opensoft/xFactory={carrier}")
    assert "1 named in a VERIFIED supplied tree" in result.stdout


def test_a_DRAFT_change_admits_nothing_and_only_a_RATIFIED_one_does(tmp_path):
    """"the change MUST BE RATIFIED (an author cannot admit a repository by
    drafting)" — `design.md` D1.1, on the one kind whose evidence an author
    controls completely.

    The re-check asked only whether a DIRECTORY existed under
    `openspec/changes/`, so any draft — one written this morning — admitted any
    repository to the estate. The proposal's lifecycle `Status:` is read through
    the shipped strict loader, so this reader and the house checker cannot
    disagree about what a document's standing is.
    """
    path = _inventory(tmp_path, [
        _row("opensoft/NewThing", governance="pinned", provisional=True,
             admitted_by=[{"kind": "change", "change": "create-a-thing"}]),
    ])

    _proposal(tmp_path, "create-a-thing", "code_surface: none\n",
              status="draft")
    verdict = [v for v in ei.evidence_verdicts(ei.load_inventory(path),
                                               tmp_path)
               if v.admission.kind == ei.CHANGE][0]
    assert verdict.verdict == ei.GONE
    assert "`Status: draft`" in verdict.detail
    assert "AN AUTHOR CANNOT ADMIT A REPOSITORY BY DRAFTING ONE" \
        in verdict.detail

    _proposal(tmp_path, "create-a-thing", "code_surface: none\n")
    verdict = [v for v in ei.evidence_verdicts(ei.load_inventory(path),
                                               tmp_path)
               if v.admission.kind == ei.CHANGE][0]
    assert verdict.verdict == ei.GONE
    assert "no `Status:` header at all" in verdict.detail

    _proposal(tmp_path, "create-a-thing", "code_surface: none\n",
              status="ratified")
    verdict = [v for v in ei.evidence_verdicts(ei.load_inventory(path),
                                               tmp_path)
               if v.admission.kind == ei.CHANGE][0]
    assert verdict.verdict == ei.NAMED
    assert "carries `Status: ratified`" in verdict.detail


def test_a_SYMLINKED_archive_child_is_not_an_archived_change(tmp_path):
    """The archive walk obeys the same no-symlink rule as every other path this
    module opens.

    `Path.is_dir()` FOLLOWS LINKS, so a link named like an archived change —
    pointed at any directory at all — reported a live PROVISIONAL row as having
    expired, on a name somebody wrote and bytes living outside the tree being
    judged.
    """
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    archive = tmp_path / "openspec" / "changes" / "archive"
    archive.mkdir(parents=True)
    (archive / "2026-09-18-create-a-thing").symlink_to(
        elsewhere, target_is_directory=True)

    path = _inventory(tmp_path, [
        _row("opensoft/NewThing", governance="pinned", provisional=True,
             admitted_by=[{"kind": "change", "change": "create-a-thing"}]),
    ])
    verdict = [v for v in ei.evidence_verdicts(ei.load_inventory(path),
                                               tmp_path)
               if v.admission.kind == ei.CHANGE][0]
    assert verdict.verdict == ei.GONE
    assert "has ARCHIVED" not in verdict.detail
    assert "carries no change `create-a-thing`, active or archived" \
        in verdict.detail
    assert "2026-09-18-create-a-thing" not in ei._archive_children(tmp_path)


def test_a_SYMLINKED_scripts_directory_is_REFUSED_and_not_reported_absent(
        tmp_path):
    """A SILENT `NOT JUDGED` IS THE WORSE OF THE TWO VERDICTS, because it
    passes.

    The default probe asked `is_symlink() or exists()`. For a symlinked
    `scripts/` whose target carries no inventory — and for a dangling one —
    BOTH are false: `is_symlink()` answers for the LEAF and `exists()` FOLLOWS
    the link. The run then reported membership NOT JUDGED, which reads as "this
    tree carries no inventory" when what is true is "this tree reaches its
    inventory through a link nobody here may follow". The probe uses `os.lstat`
    semantics and the refusal is `load_inventory`'s own, where it is written
    down.
    """
    _proposal(tmp_path, "a-change", "code_surface: openxFactory\n")
    register = _register(tmp_path)
    (tmp_path / "planted").mkdir()
    (tmp_path / "scripts").symlink_to(tmp_path / "planted",
                                      target_is_directory=True)

    result = _run_surface(tmp_path, None, register)
    assert result.returncode == 2, result.stdout
    assert "membership validation CANNOT RUN" in result.stdout
    assert "reached through a symlink" in result.stdout
    assert "membership: NOT JUDGED" not in result.stdout
    assert "Traceback" not in result.stderr, result.stderr

    # AND A TREE THAT SIMPLY HAS NO `scripts/` IS STILL NOT JUDGED, so the
    # probe refuses the link and not the ordinary absence.
    (tmp_path / "scripts").unlink()
    result = _run_surface(tmp_path, None, register)
    assert result.returncode == 0, result.stdout
    assert "membership: NOT JUDGED" in result.stdout


# ==============================================================================
# THE SECOND REVIEW ROUND OF PR #1119: the carrier read itself
# ==============================================================================


def test_an_ambient_GIT_DIR_cannot_flip_the_carrier_binding(tmp_path,
                                                            monkeypatch):
    """THIS READ IS THE BINDING, so the environment it runs in is part of it.

    `GIT_DIR`, `GIT_COMMON_DIR` and `GIT_WORK_TREE` MOVE THE REPOSITORY OUT FROM
    UNDER `-C`, so a checkout of one repository read under an ambient `GIT_DIR`
    answers with ANOTHER repository's origin and verifies as a carrier it is
    not. A caller controls its own environment and CI is an environment; a
    binding a variable can flip is not a binding. The estate's own scrub list is
    applied, and this case sets the variable that demonstrably flipped it.
    """
    innocent = _worktree(tmp_path, "git@github.com:opensoft/Innocent.git",
                         name="innocent", submodules=["opensoft/openxFactory"])
    planted = _worktree(tmp_path, "git@github.com:opensoft/xFactory.git",
                        name="planted")

    monkeypatch.setenv("GIT_DIR", str(planted / ".git"))
    assert ei.tree_origin(innocent) == "opensoft/Innocent"
    check = ei.carrier_identity(innocent, "opensoft/xFactory")
    assert check.verified is False
    assert check.observed == "opensoft/Innocent"


def test_an_ambient_GIT_CONFIG_is_scrubbed_from_the_carrier_read(tmp_path,
                                                                 monkeypatch):
    """`GIT_CONFIG` is the one entry `GIT_DIR`'s round did not carry.

    MEASURED, NOT ASSUMED, so the claim this test locks in is precise: on the
    git this branch tests against, `remote get-url` and `rev-parse` — the only
    two calls `_git` makes — do not themselves consult `GIT_CONFIG` (it
    redirects `git config`'s OWN default file and nothing else reads it), so
    the FIRST assertion below — the observed identity is unmoved — holds even
    on the PRE-FIX code. The SECOND assertion is the actual fix and is what
    fails there: `GIT_CONFIG` was not on `_SCRUBBED_GIT_ENVIRONMENT`, so
    `_sanitized_git_environment` passed it straight through. It is dropped
    on the same ground the rest of the list already stands on: a caller
    controls its own environment, and a binding that rests on one git
    version's undocumented non-effect — rather than on what this reader
    itself refuses to hand its subprocess — is not a binding.
    """
    carrier = _worktree(tmp_path, "git@github.com:opensoft/xFactory.git")
    evil = tmp_path / "evil.gitconfig"
    evil.write_text(
        '[remote "origin"]\n'
        '\turl = git@attacker.example:opensoft/xFactory.git\n',
        encoding="utf-8")

    monkeypatch.setenv("GIT_CONFIG", str(evil))
    assert ei.tree_origin(carrier) == "opensoft/xFactory"
    assert "GIT_CONFIG" not in ei._sanitized_git_environment()


def test_a_BARE_repo_and_a_SUBDIRECTORY_are_not_a_carriers_working_tree(
        tmp_path):
    """"a carrying repository's WORKING TREE" is the mode's own ratified word,
    and `git remote get-url origin` does not establish one.

    A BARE REPOSITORY answers it perfectly well, so a bare repo with a
    `.gitmodules` planted beside its refs would discharge a row while being no
    checkout at all. A SUBDIRECTORY of a real checkout answers too, because git
    discovers upward — and there `.gitmodules` is absent where the caller
    pointed, so the row would be reported GONE: CONDEMNED on a caller's
    imprecise path, which is the outcome `design.md` D1.2 retained and DECLINED.
    Both leave the row NOT RE-CHECKED instead.
    """
    bare = tmp_path / "bare.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(bare), "remote", "add", "origin",
                    "git@github.com:opensoft/xFactory.git"], check=True,
                   capture_output=True)
    (bare / ".gitmodules").write_text(
        '[submodule "openxFactory"]\n\tpath = openxFactory\n'
        '\turl = git@github.com:opensoft/openxFactory.git\n', encoding="utf-8")
    assert ei.tree_origin(bare) is None
    assert ei.carrier_identity(bare, "opensoft/xFactory").verified is False

    carrier = _worktree(tmp_path, "git@github.com:opensoft/xFactory.git",
                        submodules=["opensoft/openxFactory"])
    inside = carrier / "sub"
    inside.mkdir()
    assert ei.tree_origin(inside) is None
    assert ei.carrier_identity(inside, "opensoft/xFactory").verified is False
    # AND THE ROOT ITSELF STILL VERIFIES AND STILL DISCHARGES THE ROW.
    assert ei.tree_origin(carrier) == "opensoft/xFactory"

    path = _inventory(tmp_path, [_row("opensoft/openxFactory")])
    for supplied in (bare, inside):
        result = _run_inventory(tmp_path, path,
                                "--estate-tree", f"opensoft/xFactory={supplied}")
        assert result.returncode == 0, result.stdout
        assert "0 named in a VERIFIED supplied tree" in result.stdout
        assert "it is not the ROOT of a non-bare git working tree" \
            in result.stdout
    result = _run_inventory(tmp_path, path,
                            "--estate-tree", f"opensoft/xFactory={carrier}")
    assert "1 named in a VERIFIED supplied tree" in result.stdout


# ==============================================================================
# THE THIRD REVIEW ROUND OF PR #1119: a gap round 2's own sanitization left,
# and a gap in the ROOT binding round 1 never closed
# ==============================================================================


def test_a_ROOT_row_must_declare_governance_GOVERNED(tmp_path):
    """`root` NAMES NO FILE EITHER, so nothing downstream ever looks at a tree
    to re-check it — `evidence_verdicts` marks a `root` admission NAMED
    unconditionally, correctly, because the aggregation is real. That made
    `governance:` the one clause round 1's ROOT binding left unchecked, and
    the membership arm (`scripts/validate-code-surface.py`) refuses only
    `governance: external`, waving a `pinned` row through unrefused.

    `root` denotes the aggregation repository ITSELF, which this estate
    authors directly rather than pins or stands outside of, so a `root` row
    declaring anything but `governed` would let a code surface name the
    aggregation as a repository the estate does not author — authorized by
    the one admission no run can ever contradict.
    """
    pinned_root = _inventory(tmp_path, [
        _row(ei.AGGREGATION_ROOT, governance="pinned",
             admitted_by=[{"kind": "root"}]),
    ], name="pinned-root.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(pinned_root)
    assert "governance: pinned" in str(refusal.value)

    external_root = _inventory(tmp_path, [
        _row(ei.AGGREGATION_ROOT, governance="external",
             admitted_by=[{"kind": "root"}]),
    ], name="external-root.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(external_root)
    assert "governance: external" in str(refusal.value)

    # AND THE LAWFUL SHAPE — the live inventory's own shape — STILL LOADS, so
    # the guard refuses the malformed row and nothing else.
    lawful = _inventory(tmp_path, [
        _row(ei.AGGREGATION_ROOT, admitted_by=[{"kind": "root"}]),
    ], name="lawful-root.yaml")
    assert ei.load_inventory(lawful).rows[0].governance == "governed"


# ==============================================================================
# THE FOURTH REVIEW ROUND OF PR #1119: structural evidence, not prose
# ==============================================================================


def test_a_PIN_admission_is_named_by_its_STRUCTURAL_field_and_not_by_prose(
        tmp_path):
    """"the repository … NAMES THE REPOSITORY" was answered by scanning the
    whole file's TEXT for the address, bounded so a substring of a longer
    address would not match — and a boundary on THAT match still let PROSE
    discharge an admission, because prose is text too.

    Measured against the live corpus: `contracts/openspec-cli-pin.yaml`'s own
    `source_repository:` is `Fission-AI/OpenSpec`, and its header commentary
    names `codeXfactory/codexFactory` more than a dozen times documenting
    THAT repository's own use of the pinned CLI. This fixture is that shape,
    narrowed to the one field and the one comment that matter.
    """
    contracts = tmp_path / "contracts"
    contracts.mkdir(parents=True, exist_ok=True)
    (contracts / "cli-pin.yaml").write_text(
        "schema_version: 1\n"
        "kind: pinned_contract_manifest\n"
        "# codeXfactory/codexFactory ran this CLI over its own readiness\n"
        "# packet (codeXfactory/codexFactory PR #216).\n"
        "source_repository: Fission-AI/OpenSpec\n",
        encoding="utf-8")

    prose_only = _inventory(tmp_path, [
        _row("codeXfactory/codexFactory", governance="pinned",
             admitted_by=[{"kind": "pin", "path": "contracts/cli-pin.yaml"}]),
    ], name="prose-only.yaml")
    verdicts = [v for v in
               ei.evidence_verdicts(ei.load_inventory(prose_only), tmp_path)
               if v.row.repository == "codeXfactory/codexFactory"]
    assert [v.verdict for v in verdicts] == [ei.GONE]
    assert "no longer names `codeXfactory/codexFactory`" in verdicts[0].detail

    # AND THE FILE STILL DISCHARGES THE ROW ITS STRUCTURAL FIELD ACTUALLY NAMES.
    structural = _inventory(tmp_path, [
        _row("Fission-AI/OpenSpec", governance="external",
             admitted_by=[{"kind": "pin", "path": "contracts/cli-pin.yaml"}]),
    ], name="structural.yaml")
    named = [v for v in
            ei.evidence_verdicts(ei.load_inventory(structural), tmp_path)
            if v.row.repository == "Fission-AI/OpenSpec"]
    assert [v.verdict for v in named] == [ei.NAMED]


def test_a_WORKFLOW_admission_is_named_by_USES_or_WITH_REPOSITORY_and_not_by_prose(
        tmp_path):
    """The same defect, on the other IN-TREE kind. A workflow's `run:` step, an
    `echo`, an `::error::` message can all spell a repository's address in
    PROSE without the workflow itself dispatching into it; only a step's
    `uses:` (a reusable workflow or action PINNED at that repository) or a
    step's `with.repository:` (an `actions/checkout`-shaped input — row 3's
    own real site, `.github/workflows/merge-master-approval.yml`) is the
    workflow's own structural claim.
    """
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    (workflows / "dispatch.yml").write_text(
        "name: dispatch\n"
        "on: push\n"
        "jobs:\n"
        "  run:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: prose only\n"
        "        run: |\n"
        "          echo 'this step only TALKS ABOUT codeXfactory/codexFactory'\n"
        "      - name: real checkout\n"
        "        uses: actions/checkout@v4\n"
        "        with:\n"
        "          repository: opensoft/openxFactory\n",
        encoding="utf-8")

    prose_only = _inventory(tmp_path, [
        _row("codeXfactory/codexFactory", governance="governed",
             admitted_by=[{"kind": "workflow",
                          "path": ".github/workflows/dispatch.yml"}]),
    ], name="prose-only.yaml")
    verdicts = [v for v in
               ei.evidence_verdicts(ei.load_inventory(prose_only), tmp_path)
               if v.row.repository == "codeXfactory/codexFactory"]
    assert [v.verdict for v in verdicts] == [ei.GONE]

    # `with.repository:` DISCHARGES — row 3's own real site.
    with_repository = _inventory(tmp_path, [
        _row("opensoft/openxFactory",
             admitted_by=[{"kind": "workflow",
                          "path": ".github/workflows/dispatch.yml"}]),
    ], name="with-repository.yaml")
    named = [v for v in
            ei.evidence_verdicts(ei.load_inventory(with_repository), tmp_path)
            if v.row.repository == "opensoft/openxFactory"]
    assert [v.verdict for v in named] == [ei.NAMED]

    # `uses:` ALSO DISCHARGES — the reusable-workflow/action site, `@<ref>`
    # and any path past the address stripped before the comparison.
    (workflows / "reusable.yml").write_text(
        "name: reusable\n"
        "on: push\n"
        "jobs:\n"
        "  call:\n"
        "    steps:\n"
        "      - uses: codeXfactory/codexFactory/.github/workflows/x.yml@deadbeef\n",
        encoding="utf-8")
    via_uses = _inventory(tmp_path, [
        _row("codeXfactory/codexFactory", governance="governed",
             admitted_by=[{"kind": "workflow",
                          "path": ".github/workflows/reusable.yml"}]),
    ], name="via-uses.yaml")
    named_uses = [v for v in
                 ei.evidence_verdicts(ei.load_inventory(via_uses), tmp_path)
                 if v.row.repository == "codeXfactory/codexFactory"]
    assert [v.verdict for v in named_uses] == [ei.NAMED]


def test_the_live_codexFactory_workflow_admission_survives_a_115KB_file(
        ):
    """`_names_repository`'s `workflow` branch reads through
    `frontmatter_strict.StrictLoader` directly rather than through
    `strict_load`, because `strict_load`'s byte ceiling is sized for a
    front-matter document and this estate's own
    `.github/workflows/merge-master-approval.yml` — row 3's real workflow
    evidence — is over 115KB on its documentation prose alone. MEASURED, not
    assumed: this asserts the live file is still bigger than the ceiling
    `strict_load` would apply, so the case is not accidentally testing a file
    that has shrunk under it, and that the live row is NAMED anyway.
    """
    workflow_path = ROOT / ".github" / "workflows" / "merge-master-approval.yml"
    size = len(workflow_path.read_text(encoding="utf-8").encode("utf-8"))
    ceiling = importlib.import_module("frontmatter_strict").CEILING_BYTES
    assert size > ceiling, (size, ceiling)

    inventory = ei.load_inventory(INVENTORY)
    resolution = ei.resolve(inventory, "codeXfactory/codexFactory")
    assert resolution.resolved is True
    verdicts = [v for v in ei.evidence_verdicts(inventory, ROOT)
               if v.row is resolution.row and v.admission.kind == ei.WORKFLOW]
    assert [v.verdict for v in verdicts] == [ei.NAMED]


# ==============================================================================
# THE FIFTH REVIEW ROUND OF PR #1119: the transfer map's own complete-row
# contract, and the job-level reusable-workflow site
# ==============================================================================


def test_a_MALFORMED_transfer_row_is_refused_and_reported_not_resolved(
        tmp_path):
    """`field_rules.transfer_state` carries the map's own MUST: "`pending`
    while `transferred_on` is `null`; `complete` once it is set. The two
    fields move together and a reader MUST treat any disagreement between
    them as a malformed row." A first cut of `load_transfers` checked only
    `transfer_state == "complete"` and never looked at `transferred_on` at
    all — so a row edited to add `transfer_state: complete` with
    `transferred_on` left `null` (or any non-date value) resolved as an
    authoritative identity change on the strength of two string fields alone,
    which is exactly the bypass of the membership arm's fail-closed path
    Copilot's review named.
    """
    # `transfer_state: complete` with `transferred_on: null` — the shape named.
    _transfer_map(tmp_path, [{"former": "opensoft/Bogus",
                              "current": "opensoft/Real",
                              "transferred_on": None,
                              "transfer_state": "complete"}])
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {}
    assert len(findings) == 1
    assert "transfer_state: complete" in findings[0]
    assert "transferred_on" in findings[0]

    # AND THE RESOLVER DOES NOT ADMIT THE FORMER SPELLING: the malformed row
    # never entered the map, so `opensoft/Bogus` resolves to NOTHING rather
    # than to `opensoft/Real`.
    path = _inventory(tmp_path, [_row("opensoft/Real")])
    resolution = ei.resolve(ei.load_inventory(path), "opensoft/Bogus",
                            transfers)
    assert resolution.resolved is False

    # `transfer_state: complete` with `transferred_on` a STRING, not a date —
    # the same disagreement, a different wrong type.
    _transfer_map(tmp_path, [{"former": "opensoft/Bogus",
                              "current": "opensoft/Real",
                              "transferred_on": "not-a-date",
                              "transfer_state": "complete"}])
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {}
    assert len(findings) == 1

    # `transfer_state` itself outside the closed pair.
    _transfer_map(tmp_path, [{"former": "opensoft/Bogus",
                              "current": "opensoft/Real",
                              "transferred_on": None,
                              "transfer_state": "in-progress"}])
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {}
    assert len(findings) == 1
    assert "neither `pending` nor `complete`" in findings[0]

    # AND THE LAWFUL SHAPE STILL RESOLVES, so the guard refuses the malformed
    # row and nothing else.
    _transfer_map(tmp_path, [{"former": "opensoft/Bogus",
                              "current": "opensoft/Real",
                              "transferred_on": datetime.date(2026, 9, 9),
                              "transfer_state": "complete"}])
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {"opensoft/Bogus": "opensoft/Real"}
    assert findings == ()


def test_a_reusable_workflow_called_at_JOB_LEVEL_names_its_repository(
        tmp_path):
    """GitHub Actions calls a reusable workflow two ways: a STEP's `uses:`
    inside an ordinary job, or the JOB ITSELF written as `jobs.<job_id>.uses:`
    — which is how a caller dispatches to an entire reusable workflow with NO
    `steps:` of its own (the called workflow's steps run in its place). A
    first cut of `_workflow_names_repository` only ever looked inside
    `steps[*]`, so a workflow admission whose real site is a job-level `uses:`
    read GONE even though the file's own structural field names the
    repository plainly.
    """
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True, exist_ok=True)
    (workflows / "job-level.yml").write_text(
        "name: job-level\n"
        "on: push\n"
        "jobs:\n"
        "  call-it:\n"
        "    uses: codeXfactory/codexFactory/.github/workflows/x.yml@deadbeef\n"
        "    secrets: inherit\n",
        encoding="utf-8")

    path = _inventory(tmp_path, [
        _row("codeXfactory/codexFactory", governance="governed",
             admitted_by=[{"kind": "workflow",
                          "path": ".github/workflows/job-level.yml"}]),
    ])
    verdicts = [v for v in
               ei.evidence_verdicts(ei.load_inventory(path), tmp_path)
               if v.row.repository == "codeXfactory/codexFactory"]
    assert [v.verdict for v in verdicts] == [ei.NAMED]


# ==============================================================================
# THE SIXTH REVIEW ROUND OF PR #1119: the pin kind's second clause, at load
# ==============================================================================


def test_a_PIN_admission_on_a_GOVERNED_row_is_refused(tmp_path):
    """The promoted spec's own words: "`pin`: an openxFactory file under
    `contracts/` names the repository as the source of a commit-and-digest
    pin. This is openxFactory's act, for a product PINNED rather than
    governed." The post-pass bound `root` and `gitlink` but skipped every
    `pin` admission without checking this second clause — exactly the shape
    row 3 (`codeXfactory/codexFactory`) carried until Brett Heap ruled it out
    ("Drop the pin admission on row 3"): `governance: governed` AND admitted
    by a `pin`. Unchecked, a malformed inventory could reintroduce that same
    mismatch on any row, and the membership arm would accept it — it refuses
    only `governance: external`.
    """
    pinned_on_governed = _inventory(tmp_path, [
        _row("opensoft/Something", governance="governed",
             admitted_by=[{"kind": "pin", "path": "contracts/x-pin.yaml"}]),
    ], name="bad.yaml")
    with pytest.raises(ei.EstateInventoryError) as refusal:
        ei.load_inventory(pinned_on_governed)
    assert "governance: governed" in str(refusal.value)
    assert "admitted by a `pin`" in str(refusal.value)

    # AND THE TWO LAWFUL CLASSES STILL LOAD — `pinned` and `external`, the
    # only two classes any real `pin`-admitted row in this estate carries
    # (rows 12-14, 16 `pinned`; row 26 `external`).
    for governance in ("pinned", "external"):
        lawful = _inventory(tmp_path, [
            _row("opensoft/Something", governance=governance,
                 admitted_by=[{"kind": "pin", "path": "contracts/x-pin.yaml"}]),
        ], name=f"lawful-{governance}.yaml")
        assert len(ei.load_inventory(lawful).rows) == 1


# ==============================================================================
# THE SEVENTH REVIEW ROUND OF PR #1119: the transfer-record loader's three
# remaining edges — an unparseable date, a subclass that slips an `isinstance`
# check, and two complete rows that disagree with each other
# ==============================================================================


def test_an_IMPOSSIBLE_calendar_date_in_transferred_on_is_a_finding_not_an_exception(
        tmp_path):
    """PyYAML's timestamp constructor raises a bare `ValueError` — not
    `yaml.YAMLError`, which `fm.strict_load`'s existing guards already catch
    — on a scalar that LOOKS like a date but names a day the calendar does
    not have. `2026-02-30` is exactly that: February never reaches the 30th.
    A first cut of `load_transfers` caught `OSError`, `UnicodeDecodeError`
    and `fm.StrictFrontMatterError` around the parse but not `ValueError`, so
    this one class of malformed content crashed the whole reader — an
    uncaught exception out of a function every caller in this module treats
    as returning, never raising — instead of being reported as a finding the
    way every OTHER malformed row in this map is.
    """
    folder = tmp_path / "contracts" / "policies"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "repository-identity.yaml"
    path.write_text(
        "schema_version: 1\n"
        "kind: repository_identity\n"
        "transfers:\n"
        "  - former: opensoft/Bogus\n"
        "    current: opensoft/Real\n"
        "    transfer_state: complete\n"
        "    transferred_on: 2026-02-30\n",
        encoding="utf-8")
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {}
    assert len(findings) == 1
    assert "could not be parsed" in findings[0]

    # AND A LAWFUL FILE BESIDE IT IS UNAFFECTED — the guard is scoped to the
    # unparseable file, not to every call this process ever makes.
    _transfer_map(tmp_path, [{"former": "opensoft/Bogus",
                              "current": "opensoft/Real",
                              "transferred_on": datetime.date(2026, 9, 9),
                              "transfer_state": "complete"}])
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {"opensoft/Bogus": "opensoft/Real"}
    assert findings == ()


def test_a_TIMESTAMP_transferred_on_is_refused_not_accepted_as_a_plain_date(
        tmp_path):
    """`datetime.datetime` SUBCLASSES `datetime.date`, so
    `isinstance(v, datetime.date)` accepts a timestamp exactly as readily as
    a plain date. `field_rules.transfer_state` means the bare `YYYY-MM-DD`
    scalar a real row carries — which PyYAML parses to `datetime.date` — and
    never a scalar with a time-of-day component. A first cut of the
    `complete`-row check used `isinstance` alone, so a `transferred_on`
    written as an ISO timestamp would have resolved as if it were the plain
    date `field_rules.transfer_state` requires.
    """
    folder = tmp_path / "contracts" / "policies"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "repository-identity.yaml"
    path.write_text(
        "schema_version: 1\n"
        "kind: repository_identity\n"
        "transfers:\n"
        "  - former: opensoft/Bogus\n"
        "    current: opensoft/Real\n"
        "    transfer_state: complete\n"
        "    transferred_on: 2026-09-09T00:00:00\n",
        encoding="utf-8")
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {}
    assert len(findings) == 1
    assert "not a plain date" in findings[0]

    # AND THE PLAIN DATE THAT SAME SCALAR WOULD NAME STILL RESOLVES.
    _transfer_map(tmp_path, [{"former": "opensoft/Bogus",
                              "current": "opensoft/Real",
                              "transferred_on": datetime.date(2026, 9, 9),
                              "transfer_state": "complete"}])
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {"opensoft/Bogus": "opensoft/Real"}
    assert findings == ()


def test_a_DUPLICATE_former_across_two_COMPLETE_rows_refuses_the_whole_file(
        tmp_path):
    """Two rows both `transfer_state: complete` naming the same `former`
    address do not fail any PER-ROW shape check — each is individually
    well-formed — so a first cut of the loop let `resolved[former] = current`
    silently OVERWRITE: whichever row the loop reached LAST won, with no
    finding raised at all. A map caught disagreeing with itself about where
    one address went cannot be trusted for any OTHER `former` it names
    either, so this refuses resolution for the WHOLE FILE — not merely the
    colliding pair — and names both rows.
    """
    _transfer_map(tmp_path, [
        {"former": "opensoft/Bogus", "current": "opensoft/First",
         "transferred_on": datetime.date(2026, 9, 1),
         "transfer_state": "complete"},
        {"former": "opensoft/Elsewhere", "current": "opensoft/Other",
         "transferred_on": datetime.date(2026, 9, 2),
         "transfer_state": "complete"},
        {"former": "opensoft/Bogus", "current": "opensoft/Second",
         "transferred_on": datetime.date(2026, 9, 3),
         "transfer_state": "complete"},
    ])
    transfers, findings = ei.load_transfers(tmp_path)
    # THE WHOLE FILE IS REFUSED — including the unrelated, individually
    # lawful `opensoft/Elsewhere` row, not merely the colliding pair.
    assert transfers == {}
    assert len(findings) == 1
    assert "opensoft/Bogus" in findings[0]
    assert "row 1" in findings[0]
    assert "row 3" in findings[0]

    # AND WITH THE COLLISION REMOVED, BOTH SURVIVING ROWS RESOLVE.
    _transfer_map(tmp_path, [
        {"former": "opensoft/Bogus", "current": "opensoft/First",
         "transferred_on": datetime.date(2026, 9, 1),
         "transfer_state": "complete"},
        {"former": "opensoft/Elsewhere", "current": "opensoft/Other",
         "transferred_on": datetime.date(2026, 9, 2),
         "transfer_state": "complete"},
    ])
    transfers, findings = ei.load_transfers(tmp_path)
    assert transfers == {"opensoft/Bogus": "opensoft/First",
                         "opensoft/Elsewhere": "opensoft/Other"}
    assert findings == ()
