"""THE REGISTRATION CHECKER GETS A LANE (issue #776, second assertion).

`scripts/validate-pin-registrations.py` walks `contracts/manifest.yaml`'s
`type: pin` rows and asserts that the registration is internally coherent: the
registered `path` is in the tree, the pin's own `consumer_entrypoint:` resolves
to a file, and the row's `consumption_rule` names that same path. Its docstring
carries the failure mode and the canon those three assertions come from.

WHY THIS FILE EXISTS AT ALL, AND WHY IT IS THE HALF THAT MATTERS. The defect
issue #776 names is not that the register is wrong today — it is green today —
but that NOTHING ASKS. A checker invoked by no workflow and no test catches
drift only when a human remembers to run it, which is the same failure mode one
level up; `tests/manifest_digests/test_manifest_digest_sweep.py` was written for
exactly that reason about the digest sweeper and says so in its own docstring.
This module is that lane for the registration sweeper, and it needs no workflow
edit: `.github/workflows/pytest-suite.yml` already runs
`python3 -m pytest tests/ -q -m "not postgres"` as a required check, so a test
directory here IS the wiring.

THE POSITIVE test runs the real checker as a subprocess from the repository
root — the `Run:` line of its own docstring, unmodified — rather than the
imported function, because what must be pinned is that the documented invocation
succeeds and prints what a reader of its output depends on.

AND THE POSITIVE TEST IS NOT ALLOWED TO BE VACUOUS. A sweep over ZERO rows exits
0 and prints a cheerful summary, indistinguishable from a sweep that measured
something; so `test_the_live_register_carries_at_least_one_pin_row` pins the
corpus fact that there IS a registered pin, and names it. That assertion, not
the checker, is what reds if the one registered row is deleted — deliberately,
because canon obliges no manifest to CARRY a pin row and a checker that refused
an empty register would be enforcing a rule canon does not carry.

THE NEGATIVE tests prove the lane can go RED on each assertion separately, not
only that it stays green today. A positive-only test would pass identically
whether the checker still compared anything or had been reduced to
`sys.exit(0)` — indistinguishable from the defect this whole issue is about. So
the module is loaded by path (it is `validate-pin-registrations.py`, hyphenated
and therefore unimportable — the reason `tests/manifest_digests/` and
`tests/openxwallet_pin/` load their own subjects the same way) and its
module-level `ROOT`/`MANIFEST` are monkeypatched onto a throwaway register built
in `tmp_path`. FOUR fixtures, one per case the checker exists to separate: a
coherent row; a row whose `path` is missing; a pin whose `consumer_entrypoint:`
names a script that is not there; and a row whose `consumption_rule` is silent
about the entrypoint. Each asserts the FINDING TEXT, because a checker that
fails without saying which of the three assertions failed is the very thing
`tasks.md` § 5.4 refused when it placed this checker beside
`release-inventory-drift` rather than inside it.

TWO GROUPS WERE ADDED FROM THE REVIEW BENCH, and both assert the SAME defect
class the rest of the file does — a comparison that passes without measuring.
CONTAINMENT: an absolute registered path, a `..` escape, an absolute entrypoint
and a non-string path. The absolute-path fixtures deliberately name a REAL,
EXISTING host file (`pytest.ini` by absolute path), because the defect is
precisely that `Path(root) / "/abs"` discards the root and the host's copy makes
`.is_file()` say yes. WHOLE-PATH NAMING: Codex's case verbatim — the pin says
`scripts/tool.py`, a stale rule says `scripts/tool.py.old` — plus the
deliberate allowance for a leading `/` (the same entrypoint named through the
pinned checkout directory) and its refusal for a leading name character, and the
predicate stated directly at its boundaries.

THE FIXTURES ARE BUILT IN `tmp_path`, NOT COMMITTED. On
`tests/manifest_digests/`'s precedent: a committed broken manifest is a file
some other sweep has to be taught to ignore, while a scratch tree is read by
this test alone. Where a fixture needs a path that really exists, it uses
`pytest.ini` — small, stable, and already the file the digest lane borrows.

A FOURTH ASSERTION JOINED THE CHECKER AND ITS OWN GROUP JOINED THIS FILE
(issue #840): a `dispositions[].cited_to` citation must RESOLVE. The pin's
header rests its whole exception mechanism on the citation and nothing opened
one, so PR #834's rename left two citations naming a path that is gone while
`--all --no-cache` exited 0 either way. That group's fixtures, its live-corpus
anti-vacuity pin, its named assertion about #834's rename in BOTH directions,
and the reader stated at its boundaries are at the foot of this file, with the
reasoning beside them — and beside them the review bench's own two findings on
that arm, each one a test that is red on the arm as first written.

Hermetic: no network and no `nlm`/`gh`/`omp` (`tests/hermeticity.py`'s guarded
set). The subprocess in the positive test is `sys.executable` plus a script
path, the shape `tests/manifest_digests/` already uses; every other test touches
only `tmp_path`. Nothing here skips, on purpose: `pytest-suite.yml` pins SKIPPED
exactly, and a self-skipping guard in a new directory would move that pin.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CHECKER = REPO_ROOT / "scripts" / "validate-pin-registrations.py"
MANIFEST = REPO_ROOT / "contracts" / "manifest.yaml"

# The entrypoint the one registered pin names today. Written out rather than
# read from the pin, so this file states the fact it is pinning instead of
# restating the checker's own comparison and proving nothing.
LIVE_PIN_ID = "openspec-cli-pin"
LIVE_PIN_PATH = "contracts/openspec-cli-pin.yaml"
LIVE_ENTRYPOINT = "scripts/validate-openspec-cli-pin.py"


def _load_checker() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "validate_pin_registrations_under_test", CHECKER)
    assert spec and spec.loader, f"cannot load checker at {CHECKER}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_case(tmp_path: Path, *, row: dict, pin: dict | None,
                pin_relpath: str | None) -> Path:
    """Build a throwaway register (and optionally its pin) under `tmp_path`."""
    if pin is not None and pin_relpath is not None:
        pin_file = tmp_path / pin_relpath
        pin_file.parent.mkdir(parents=True, exist_ok=True)
        # `allow_unicode=True` because a citation's `—` is load-bearing grammar
        # and the default emitter would write it as an escaped `"\u2014"` inside
        # a quoted scalar, which is not a line the corpus ever carries.
        pin_file.write_text(yaml.safe_dump(pin, allow_unicode=True),
                            encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [row]}), encoding="utf-8")
    return manifest


def _run_over(module: ModuleType, monkeypatch, tmp_path: Path,
              manifest: Path) -> int:
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "MANIFEST", manifest)
    return module.main()


# --------------------------------------------------------------------------
# The live corpus
# --------------------------------------------------------------------------

def test_the_real_register_coheres_run_the_documented_way() -> None:
    """The command this lane actually gives CI: the checker as a subprocess,
    over the committed `contracts/manifest.yaml`, from the repository root."""
    result = subprocess.run(
        [sys.executable, str(CHECKER)],
        cwd=str(REPO_ROOT), capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "OK contracts/manifest.yaml:" in result.stdout, result.stdout
    assert "pin registration(s) cohere" in result.stdout, result.stdout


def test_the_live_register_carries_at_least_one_pin_row() -> None:
    """The anti-vacuity pin. A sweep over zero rows exits 0 and says so
    cheerfully; this is the assertion that tells the two apart, and it names the
    row rather than counting one, so deleting THIS registration reds here."""
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    pin_rows = [row for row in doc["contracts"] if row.get("type") == "pin"]
    assert pin_rows, (
        "contracts/manifest.yaml registers no `type: pin` row, so the "
        "registration sweep measures nothing — if a pin was deliberately "
        "de-registered, move this pin WITH the reason")
    ids = {row.get("id") for row in pin_rows}
    assert LIVE_PIN_ID in ids, sorted(ids)
    row = next(row for row in pin_rows if row.get("id") == LIVE_PIN_ID)
    assert row["path"] == LIVE_PIN_PATH
    assert LIVE_ENTRYPOINT in row["consumption_rule"]


def test_the_live_pin_and_row_name_the_same_entrypoint() -> None:
    """The comparison itself, stated once against the real files — the thing
    issue #776 measured as made by nothing: the MANIFEST ROW against the PIN,
    not `proposal-support`'s constant against the pin."""
    doc = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    row = next(row for row in doc["contracts"] if row.get("id") == LIVE_PIN_ID)
    pin = yaml.safe_load(
        (REPO_ROOT / row["path"]).read_text(encoding="utf-8"))
    entrypoint = pin["consumer_entrypoint"]
    assert entrypoint == LIVE_ENTRYPOINT
    assert (REPO_ROOT / entrypoint).is_file()
    assert entrypoint in row["consumption_rule"]


# --------------------------------------------------------------------------
# Fixture 1 — a coherent row
# --------------------------------------------------------------------------

def test_a_coherent_row_passes_and_names_what_agreed(
        tmp_path, monkeypatch, capsys) -> None:
    module = _load_checker()
    entrypoint = "scripts/some-entrypoint.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    manifest = _write_case(
        tmp_path,
        row={
            "id": "scratch-pin",
            "path": "contracts/scratch-pin.yaml",
            "type": "pin",
            "adapter_owner": "openxFactory",
            "consumption_rule": (
                "CHECK OUT, NEVER COPY. Invoke `scripts/some-entrypoint.py` "
                "from the pinned checkout."),
        },
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": entrypoint},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "OK scratch-pin:" in captured.out, captured.out
    assert "names that same path" in captured.out, captured.out
    assert "OK contracts/manifest.yaml: 1 pin registration(s) cohere" in (
        captured.out), captured.out


# --------------------------------------------------------------------------
# Fixture 2 — the registered path is not in the tree
# --------------------------------------------------------------------------

def test_a_registered_pin_that_is_not_in_the_tree_is_reported(
        tmp_path, monkeypatch, capsys) -> None:
    module = _load_checker()
    manifest = _write_case(
        tmp_path,
        row={
            "id": "scratch-pin",
            "path": "contracts/moved-away-pin.yaml",
            "type": "pin",
            "consumption_rule": "Invoke `scripts/some-entrypoint.py`.",
        },
        pin=None, pin_relpath=None)

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert ("FAIL scratch-pin: the row registers "
            "`contracts/moved-away-pin.yaml` but no such file is in this tree"
            ) in captured.out, captured.out
    assert "publishes a pin a consumer cannot read" in captured.out, captured.out
    assert "FAIL 1 finding(s) over 1 pin registration(s)" in captured.out, (
        captured.out)


# --------------------------------------------------------------------------
# Fixture 3 — `consumer_entrypoint:` names a script that is not there
# --------------------------------------------------------------------------

def test_an_entrypoint_that_names_a_missing_script_is_reported(
        tmp_path, monkeypatch, capsys) -> None:
    """The rename half of the failure mode: the pin and the row agree with each
    other and BOTH name a path that is gone, so a comparison alone would pass."""
    module = _load_checker()
    entrypoint = "scripts/renamed-away.py"
    manifest = _write_case(
        tmp_path,
        row={
            "id": "scratch-pin",
            "path": "contracts/scratch-pin.yaml",
            "type": "pin",
            "consumption_rule": f"Invoke `{entrypoint}` from the pinned checkout.",
        },
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": entrypoint},
        pin_relpath="contracts/scratch-pin.yaml")
    assert not (tmp_path / entrypoint).exists()

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert ("FAIL scratch-pin: the pin names "
            "`consumer_entrypoint: scripts/renamed-away.py` but no such file is "
            "in this tree") in captured.out, captured.out
    assert "falls through to the ambient tool" in captured.out, captured.out


# --------------------------------------------------------------------------
# Fixture 4 — the row's `consumption_rule` is silent about the entrypoint
# --------------------------------------------------------------------------

def test_a_rule_silent_on_the_entrypoint_is_reported(
        tmp_path, monkeypatch, capsys) -> None:
    """D2's residual coupling, made a check: the pin names an entrypoint that
    really exists, and the published rule never names the ACTUAL command."""
    module = _load_checker()
    entrypoint = "scripts/some-entrypoint.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    manifest = _write_case(
        tmp_path,
        row={
            "id": "scratch-pin",
            "path": "contracts/scratch-pin.yaml",
            "type": "pin",
            "consumption_rule": (
                "CHECK OUT, NEVER COPY. Invoke the entrypoint this pin names in "
                "its `consumer_entrypoint:` field from that checkout."),
        },
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": entrypoint},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert ("FAIL scratch-pin: the row's `consumption_rule` never names "
            "`scripts/some-entrypoint.py`") in captured.out, captured.out
    assert "name the ACTUAL command for each governed act" in captured.out, (
        captured.out)


def test_a_row_with_no_consumption_rule_is_reported(
        tmp_path, monkeypatch, capsys) -> None:
    """The same assertion's absent case, separated from the silent one: a row
    that states no rule at all names no command for ANY governed act."""
    module = _load_checker()
    entrypoint = "scripts/some-entrypoint.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin"},
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": entrypoint},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert ("FAIL scratch-pin: the row carries no `consumption_rule`"
            ) in captured.out, captured.out


# --------------------------------------------------------------------------
# The boundaries: what is measured, and what refuses
# --------------------------------------------------------------------------

def test_a_pin_naming_no_entrypoint_is_reported_as_inapplicable_not_silent(
        tmp_path, monkeypatch, capsys) -> None:
    """Canon obliges no pin to carry `consumer_entrypoint:`. Where it does not,
    the two entrypoint assertions do not apply — and the line says so, so a
    reader can tell an inapplicable assertion from an unmade one."""
    module = _load_checker()
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin", "consumption_rule": "CHECK OUT, NEVER COPY."},
        pin={"kind": "pinned_contract_manifest", "commit": "0" * 40},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "the entrypoint assertions do not apply" in captured.out, captured.out


def test_non_pin_rows_are_not_measured(tmp_path, monkeypatch, capsys) -> None:
    """The sweep is scoped to `type: pin`. A schema row whose path is absent is
    another checker's finding, and claiming it here would make this checker's
    output unable to say which question failed."""
    module = _load_checker()
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [
        {"id": "a-schema", "path": "contracts/schemas/absent.schema.yaml",
         "type": "schema"},
    ]}), encoding="utf-8")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "0 pin registration(s) cohere" in captured.out, captured.out


def test_a_missing_manifest_is_a_harness_error_not_a_clean_corpus(
        tmp_path, monkeypatch, capsys) -> None:
    """Fail closed on the register's absence: exit 2, never an empty pass."""
    module = _load_checker()
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "MANIFEST", tmp_path / "no-such-manifest.yaml")

    exit_code = module.main()

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "is missing" in captured.err, captured.err
    assert "harness error" in captured.err, captured.err


def test_an_unparseable_manifest_is_a_harness_error(
        tmp_path, monkeypatch, capsys) -> None:
    module = _load_checker()
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text("contracts: [\n  - id: unterminated\n", encoding="utf-8")
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "MANIFEST", manifest)

    exit_code = module.main()

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "does not load" in captured.err, captured.err


def test_a_nested_pin_row_is_still_measured(
        tmp_path, monkeypatch, capsys) -> None:
    """The walk is recursive on `validate-manifest-digests.py`'s precedent, so a
    row moved under a future grouping key is measured rather than silently
    dropped — the failure mode a top-level-only loop would reintroduce."""
    module = _load_checker()
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"families": {"pins": [
        {"id": "nested-pin", "path": "contracts/absent-pin.yaml", "type": "pin"},
    ]}}), encoding="utf-8")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "FAIL nested-pin:" in captured.out, captured.out


# --------------------------------------------------------------------------
# Containment — taken from the bench (Copilot and Codex, independently)
# --------------------------------------------------------------------------

def test_an_absolute_registered_path_is_refused_even_though_it_exists(
        tmp_path, monkeypatch, capsys) -> None:
    """`Path(root) / "/abs"` DISCARDS the root. The fixture names a REAL,
    EXISTING host file on purpose — `pytest.ini` by absolute path — so a
    checker that merely joined and asked `.is_file()` would report it present
    while no consumer's checkout carries it."""
    module = _load_checker()
    absolute = str(REPO_ROOT / "pytest.ini")
    assert Path(absolute).is_file()
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": absolute, "type": "pin"},
        pin=None, pin_relpath=None)

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "is an ABSOLUTE path" in captured.out, captured.out
    assert "publishes bytes no consumer's checkout contains" in captured.out, (
        captured.out)


def test_a_registered_path_that_walks_out_of_the_tree_is_refused(
        tmp_path, monkeypatch, capsys) -> None:
    """Same defect through `..`: the escape target is created for real, so the
    refusal cannot be mistaken for a missing-file finding."""
    module = _load_checker()
    outside = tmp_path.parent / "outside-pin.yaml"
    outside.write_text("kind: pinned_contract_manifest\n", encoding="utf-8")
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "../outside-pin.yaml", "type": "pin"},
        pin=None, pin_relpath=None)

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "contains a '..' segment" in captured.out, captured.out


def test_an_absolute_entrypoint_is_refused(
        tmp_path, monkeypatch, capsys) -> None:
    """The same containment on the pin's own field: a host path is unreachable
    from the pinned checkout the recipe tells the consumer to make."""
    module = _load_checker()
    absolute = str(REPO_ROOT / "pytest.ini")
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin",
             "consumption_rule": f"Invoke `{absolute}` from the checkout."},
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": absolute},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "is an ABSOLUTE path" in captured.out, captured.out
    assert "unreachable there" in captured.out, captured.out


def test_a_non_string_registered_path_is_refused_rather_than_raising(
        tmp_path, monkeypatch, capsys) -> None:
    module = _load_checker()
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [
        {"id": "scratch-pin", "path": 17, "type": "pin"},
    ]}), encoding="utf-8")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "is not a non-empty string path" in captured.out, captured.out


def test_a_non_string_entrypoint_is_refused_rather_than_stringified(
        tmp_path, monkeypatch, capsys) -> None:
    """The bench's second round: coercing the field with `str()` BEFORE the
    containment helper turned `consumer_entrypoint: 17` into the string "17"
    and reported it as a merely-missing file, swallowing the helper's own
    non-string refusal. The raw YAML value is the claimed path."""
    module = _load_checker()
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin", "consumption_rule": "CHECK OUT, NEVER COPY."},
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": 17},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "is not a non-empty string path" in captured.out, captured.out
    # And the rule assertion does NOT also fire: `consumption_rule` is compared
    # against a PATH, and there is no path to compare against.
    assert "never names" not in captured.out, captured.out
    assert "FAIL 1 finding(s) over 1 pin registration(s)" in captured.out, (
        captured.out)


def test_an_empty_entrypoint_is_refused_as_a_non_path(
        tmp_path, monkeypatch, capsys) -> None:
    """`Path("")` is `Path(".")`, a directory — so an empty field would have
    reported as a missing FILE rather than as the absent value it is."""
    module = _load_checker()
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin", "consumption_rule": "CHECK OUT, NEVER COPY."},
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": "   "},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "is not a non-empty string path" in captured.out, captured.out


# --------------------------------------------------------------------------
# The rule names a WHOLE path — taken from the bench (Codex, P2)
# --------------------------------------------------------------------------

def test_a_rule_naming_a_longer_path_does_not_count_as_naming_the_entrypoint(
        tmp_path, monkeypatch, capsys) -> None:
    """Codex's case, verbatim: the pin says `scripts/tool.py` while a stale rule
    says `scripts/tool.py.old`. A substring test calls that coherent, and the
    rename drift this whole lane exists to catch rides through."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin",
             "consumption_rule": "Invoke `scripts/tool.py.old` from the checkout."},
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": entrypoint},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert ("never names `scripts/tool.py` as a whole path") in captured.out, (
        captured.out)


def test_a_rule_naming_the_entrypoint_through_the_checkout_directory_counts(
        tmp_path, monkeypatch, capsys) -> None:
    """The deliberate allowance, asserted so it is a decision and not an
    accident: a LEADING `/` names the same entrypoint through the checkout
    directory the recipe tells the consumer to make."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin",
             "consumption_rule": "Run `.openxfactory-pin/scripts/tool.py`."},
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": entrypoint},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out


def test_a_rule_naming_a_different_directory_does_not_count(
        tmp_path, monkeypatch, capsys) -> None:
    """The other side of that allowance: a leading NAME character is a different
    file, not the same entrypoint reached through a checkout."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin",
             "consumption_rule": "Run `myscripts/tool.py`."},
        pin={"kind": "pinned_contract_manifest", "consumer_entrypoint": entrypoint},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "as a whole path" in captured.out, captured.out


def test_the_delimiter_rule_is_stated_directly() -> None:
    """The predicate itself, at its boundaries — the live rule's own backticked
    form included, so the shape the corpus actually uses is pinned."""
    module = _load_checker()
    names = module.rule_names_entrypoint
    assert names("invokes `scripts/tool.py` from that checkout", "scripts/tool.py")
    assert names("run scripts/tool.py", "scripts/tool.py")
    assert names("run scripts/tool.py, then stop", "scripts/tool.py")
    assert names("run .pin/scripts/tool.py", "scripts/tool.py")
    assert not names("run scripts/tool.py.old", "scripts/tool.py")
    assert not names("run scripts/tool.py2", "scripts/tool.py")
    assert not names("run scripts/tool.py/inner.py", "scripts/tool.py")
    assert not names("run myscripts/tool.py", "scripts/tool.py")
    assert not names("run the entrypoint the pin names", "scripts/tool.py")
    # A rule that names BOTH — the stale longer path first — still counts,
    # because one delimited occurrence is the whole claim.
    assert names("scripts/tool.py.old, corrected to `scripts/tool.py`",
                 "scripts/tool.py")


def test_more_than_one_failed_assertion_is_reported_per_assertion(
        tmp_path, monkeypatch, capsys) -> None:
    """A reader told only the first failure has to re-run to learn the rest."""
    module = _load_checker()
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin"},
        pin={"kind": "pinned_contract_manifest",
             "consumer_entrypoint": "scripts/renamed-away.py"},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "but no such file is in this tree" in captured.out, captured.out
    assert "the row carries no `consumption_rule`" in captured.out, captured.out
    assert "FAIL 2 finding(s) over 1 pin registration(s)" in captured.out, (
        captured.out)


# --------------------------------------------------------------------------
# A disposition's `cited_to` resolves — issue #840, the fourth assertion
#
# THE DEFECT, MEASURED. PR #834 renamed `prepare-openspec-1.12-readiness` to
# `prepare-openspec-1-12-readiness`; two `dispositions[].cited_to` citations in
# the live pin went on naming the old path; `validate-openspec-cli-pin.py --all
# --no-cache` exited 0 before AND after the rename, printing both stale
# citations into the disposition report a reviewer reads. The pin's header rests
# the entire exception mechanism on the citation — "A DISPOSITION WITHOUT A
# CITATION IS REFUSED, not ignored" — and nothing opened one.
#
# THE FIXTURES ARE THE FOUR CASES THE ARM EXISTS TO SEPARATE, on the same
# `tmp_path` discipline as the groups above: a coherent set of citations in
# every form the live pin uses; a citation naming a path that is not in the
# tree; a citation whose path is MALFORMED as a repo-relative reference (the
# host-absolute and `..` cases, with a REAL host file named, so a checker that
# merely joined and asked would report it present); and a pin carrying no
# `dispositions:` at all, where the assertion does not apply and says so.
#
# AND A FIFTH GROUP CAME FROM THE REVIEW BENCH, which found the arm's first
# version reading `yaml.safe_load`'s VALUE where the pin's grammar carries the
# LINE, and taking that value's LAST TOKEN as the referent. Three lines of the
# live pin come back TRUNCATED from that parser (a ` #` is a comment) and two
# come back single-key MAPPINGS (a bare `: ` is a separator), so citations that
# name a path could classify as prose and never be opened — this arm's own
# silence, in the shape it exists to end. Those are `test_…_still_has_its_path_
# opened` and `test_…_prose_in_front_…` below, each of them red on the arm as
# first written.
# --------------------------------------------------------------------------

DASH = "—"


def _pin_with_citations(citations: list, entrypoint: str = "scripts/tool.py",
                        repo: str = "scratchFactory") -> dict:
    return {
        "kind": "pinned_contract_manifest",
        "consumer_entrypoint": entrypoint,
        "dispositions": [{
            "repo": repo,
            "item": "a-declared-change",
            "path": "some-capability/spec.md",
            "level": "ERROR",
            "finding": "the tool's message, matched whole",
            "why": "the estate declared the narrowing",
            "cited_to": citations,
            "ratified_by": "a human, on a date, in their own words",
        }],
    }


def _case_with_citations(tmp_path: Path, citations: list,
                         repo: str = "scratchFactory") -> Path:
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    return _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin",
             "consumption_rule": f"Invoke `{entrypoint}` from the checkout."},
        pin=_pin_with_citations(citations, entrypoint, repo),
        pin_relpath="contracts/scratch-pin.yaml")


def _raw_case(tmp_path: Path, citation_lines: list[str], *,
              repo: str = "scratchFactory") -> Path:
    """A pin whose `cited_to:` lines are written as RAW BYTES, not dumped.

    The bench's two findings are both about what a general YAML parser makes of
    bytes the pin's own line-based reader takes whole, so a fixture that went
    through `yaml.safe_dump` would quote the defect away before the arm ever saw
    it. These fixtures write the line.
    """
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    pin_file = tmp_path / "contracts" / "scratch-pin.yaml"
    pin_file.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(f"      - {line}\n" for line in citation_lines)
    pin_file.write_text(
        "kind: pinned_contract_manifest\n"
        f"consumer_entrypoint: {entrypoint}\n"
        "dispositions:\n"
        f"  - repo: {repo}\n"
        "    item: a-declared-change\n"
        "    cited_to:\n" + body,
        encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [
        {"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
         "type": "pin",
         "consumption_rule": f"Invoke `{entrypoint}` from the checkout."}]}),
        encoding="utf-8")
    return manifest


# ---- the live corpus, and the rename this arm was written for ----

def test_the_live_pin_carries_citations_and_every_in_tree_path_resolves(
) -> None:
    """The anti-vacuity pin for the citation arm, on `_carries_at_least_one_pin_row`'s
    precedent: a sweep over a pin with no in-tree citations exits 0 and prints a
    cheerful count, indistinguishable from one that opened something. This names
    the corpus fact instead — the live pin DOES carry citations that resolve
    here — so deleting the last one reds this test rather than quietly emptying
    the assertion."""
    module = _load_checker()
    text = (REPO_ROOT / LIVE_PIN_PATH).read_text(encoding="utf-8")
    pin = yaml.safe_load(text)
    declared = module.repository_qualifiers(pin)
    assert "codexfactory" in declared and "openxfactory" in declared, declared
    lines = module.citation_lines_in(text)
    assert lines, "the live pin records no citations at all"
    in_tree = [referent
               for line in lines
               for kind, referent in module.read_citation(line, declared)
               if kind == "tree-path"]
    assert len(in_tree) >= 2, in_tree
    missing = [p for p in in_tree if not (REPO_ROOT / p).exists()]
    assert not missing, f"citations naming paths that are gone: {missing}"


def test_the_live_pins_citation_bytes_align_with_its_parsed_structure() -> None:
    """The alignment the arm proves before it classifies anything, asserted
    against the real file: the `cited_to:` LINES and the parsed citations are
    one-to-one and in the same order, so a finding can name the entry it belongs
    to while the text it reads is the line the pin's own reader admits."""
    module = _load_checker()
    text = (REPO_ROOT / LIVE_PIN_PATH).read_text(encoding="utf-8")
    pin = yaml.safe_load(text)
    lines = module.citation_lines_in(text)
    parsed = list(module.parsed_citations_of(pin["dispositions"]))
    assert len(lines) == len(parsed), (len(lines), len(parsed))
    # And the join is the right way round: each line belongs to the entry whose
    # parsed citation sits at the same index.
    for (index, item, _citation), line in zip(parsed, lines):
        entry = pin["dispositions"][index - 1]
        assert entry.get("item", "unnamed") == item
        assert any(line == module.yaml_reading_of(c) or line.startswith(str(c))
                   for c in entry["cited_to"]), (item, line)


def test_the_live_pin_carries_lines_the_two_readers_read_differently() -> None:
    """THE MEASUREMENT THE DESIGN RESTS ON, pinned so it cannot quietly stop
    being true. Reading `yaml.safe_load`'s value instead of the line is not a
    theoretical risk on this corpus: some citations come back TRUNCATED at a
    ` #` (a YAML comment) and some come back single-key MAPPINGS (a bare `: `),
    and at least one of them loses a referent the LINE keeps. If a successor's
    governed re-vendor ever quotes these scalars, this test reds and the WARN
    class it justifies can be retired with it."""
    module = _load_checker()
    text = (REPO_ROOT / LIVE_PIN_PATH).read_text(encoding="utf-8")
    pin = yaml.safe_load(text)
    declared = module.repository_qualifiers(pin)
    lines = module.citation_lines_in(text)
    parsed = list(module.parsed_citations_of(pin["dispositions"]))
    truncated = [(citation, line)
                 for (_i, _item, citation), line in zip(parsed, lines)
                 if isinstance(citation, str) and citation != line]
    mapped = [line for (_i, _item, citation), line in zip(parsed, lines)
              if isinstance(citation, dict)]
    assert truncated, "no citation is truncated by the parser any more"
    assert mapped, "no citation reads as a single-key mapping any more"
    lost = [(citation, line) for citation, line in truncated
            if not module.read_citation(citation, declared)
            and module.read_citation(line, declared)]
    assert lost, (
        "no truncated citation loses a referent the line keeps — the arm may "
        "still be right to read the line, but this is no longer the evidence")


def test_the_renamed_readiness_evidence_is_cited_at_its_landed_path() -> None:
    """#834's rename, pinned by name in both directions, because the drift it
    caused is the whole reason this arm exists: the dotted path must be gone from
    every `cited_to` this repository owns, and the dotless one must be there."""
    text = (REPO_ROOT / LIVE_PIN_PATH).read_text(encoding="utf-8")
    landed = ("openspec/changes/prepare-openspec-1-12-readiness/evidence/"
              "openspec-1.12-readiness-2026-09-05.md")
    assert (REPO_ROOT / landed).is_file(), landed
    citation_lines = [line for line in text.splitlines()
                      if line.startswith("      - openspec/changes/prepare-")]
    assert len(citation_lines) == 2, citation_lines
    for line in citation_lines:
        assert landed in line, line
    # The dotted spelling survives ONLY where it is another repository's path or
    # a name in prose — never as a path this tree is asked to resolve.
    for line in text.splitlines():
        if line.startswith("      - ") and "prepare-openspec-1.12-readiness" in line:
            assert line.startswith("      - codexFactory "), line


# ---- the review bench's two findings, each one a test ----

def test_a_path_with_prose_in_front_of_it_is_this_trees_and_is_opened(
        tmp_path, monkeypatch, capsys) -> None:
    """THE BENCH'S FIRST FINDING. The arm as first written reserved "another
    repository's" for any path with a word in front of it, so `the packet at
    openspec/…` was called foreign and never opened, and a rename under it
    exited 0. A qualifier is a DECLARED repository name and nothing else."""
    module = _load_checker()
    manifest = _raw_case(tmp_path, [
        f"the packet at openspec/changes/gone/tasks.md {DASH} the measurement",
    ])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "cites `openspec/changes/gone/tasks.md`" in captured.out, captured.out


def test_a_declared_repository_name_is_what_makes_a_path_foreign(
        tmp_path, monkeypatch, capsys) -> None:
    """The other half of the same finding: a path qualified by a repository the
    pin ITSELF declares in a `repo:` field is not this tree's to resolve, and
    that is why it passes — not because it has two tokens."""
    module = _load_checker()
    manifest = _raw_case(tmp_path, [
        f"codexFactory openspec/changes/gone/spec.md {DASH} another tree's path",
    ], repo="codexFactory")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "1 a path qualified to another repository" in captured.out, captured.out


def test_a_line_the_parser_reads_as_a_mapping_still_has_its_path_opened(
        tmp_path, monkeypatch, capsys) -> None:
    """THE BENCH'S SECOND FINDING, in its own example. `openspec/gone.md: false`
    is a citation the pin's line reader takes whole; `yaml.safe_load` makes it
    `{'openspec/gone.md': False}`, and the arm's first version rebuilt that as
    `openspec/gone.md: False`, took `False` as the referent, called it prose and
    exited 0 with the dangling path unopened. The line is read now, so the path
    is opened."""
    module = _load_checker()
    manifest = _raw_case(tmp_path, ["openspec/gone.md: false"])
    raw = yaml.safe_load(
        (tmp_path / "contracts/scratch-pin.yaml").read_text(encoding="utf-8"))
    citation = raw["dispositions"][0]["cited_to"][0]
    assert citation == {"openspec/gone.md": False}, (
        "the fixture is only a fixture while PyYAML still reads this as a map "
        "with a coerced value")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "cites `openspec/gone.md`" in captured.out, captured.out
    assert "single-key MAPPING" in captured.out, captured.out


def test_a_line_the_parser_truncates_at_a_comment_still_has_its_path_opened(
        tmp_path, monkeypatch, capsys) -> None:
    """The same finding's other loss class, and the one that is live in the pin
    today: a ` #` is a COMMENT to a general YAML parser, so `see #444
    openspec/gone.md` comes back as `'see'` — every referent after the hash
    gone. Three citations of the live pin are truncated this way."""
    module = _load_checker()
    manifest = _raw_case(tmp_path, [
        f"see #444 openspec/gone.md {DASH} the landed change",
    ])
    raw = yaml.safe_load(
        (tmp_path / "contracts/scratch-pin.yaml").read_text(encoding="utf-8"))
    assert raw["dispositions"][0]["cited_to"][0] == "see", (
        "the fixture is only a fixture while PyYAML still truncates at ` #`")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "cites `openspec/gone.md`" in captured.out, captured.out
    assert "at the ` #` it reads as a comment" in captured.out, captured.out


def test_a_path_the_line_continues_past_is_still_opened(
        tmp_path, monkeypatch, capsys) -> None:
    """THE ROOT BOTH FINDINGS SHARED, isolated from either of their vectors. This
    citation round-trips through `yaml.safe_load` losslessly — the value is a
    string and the rejoin restores the bytes — and the arm as first written still
    missed it, because it read the region's LAST TOKEN and the line continues
    past its path. A lossless reconstruction was never the fix; reading every
    token is."""
    module = _load_checker()
    manifest = _raw_case(tmp_path, ["openspec/gone.md: gone with the rename"])
    raw = yaml.safe_load(
        (tmp_path / "contracts/scratch-pin.yaml").read_text(encoding="utf-8"))
    citation = raw["dispositions"][0]["cited_to"][0]
    assert citation == {"openspec/gone.md": "gone with the rename"}
    assert (f"{list(citation)[0]}: {list(citation.values())[0]}"
            == "openspec/gone.md: gone with the rename"), (
        "the fixture is only a fixture while the rejoin is byte-exact")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "cites `openspec/gone.md`" in captured.out, captured.out


def test_every_path_a_line_names_is_opened_not_only_the_last(
        tmp_path, monkeypatch, capsys) -> None:
    """One citation, two paths, both opened: the pin admits a citation as one
    line of prose that may CONTAIN a referent and never says where in the line it
    sits, so the arm reads every token rather than betting on a position."""
    module = _load_checker()
    manifest = _raw_case(tmp_path, [
        f"openspec/changes/gone-one/spec.md and openspec/changes/gone-two/spec.md "
        f"{DASH} both of them",
    ])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "cites `openspec/changes/gone-one/spec.md`" in captured.out
    assert "cites `openspec/changes/gone-two/spec.md`" in captured.out
    assert "FAIL 2 finding(s) over 1 pin registration(s)" in captured.out, (
        captured.out)


# ---- the alignment, proved rather than assumed ----

def test_bytes_and_structure_that_disagree_about_the_count_refuse_the_field(
        tmp_path, monkeypatch, capsys) -> None:
    """A citation written as a nested SEQUENCE yields two list-item lines and one
    parsed citation, so no line can be attributed to an entry with confidence.
    The arm refuses the whole field with one finding instead of classifying
    anything: an off-by-one would attach every finding to the wrong item, and a
    citation the pin's own line reader cannot admit either is not a form to
    guess about."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    pin_file = tmp_path / "contracts" / "scratch-pin.yaml"
    pin_file.parent.mkdir(parents=True)
    pin_file.write_text(
        "kind: pinned_contract_manifest\n"
        f"consumer_entrypoint: {entrypoint}\n"
        "dispositions:\n"
        "  - repo: scratchFactory\n"
        "    item: a-declared-change\n"
        "    cited_to:\n"
        "      - - openspec/changes/gone/spec.md\n"
        "        - a second line of one citation\n",
        encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [
        {"id": "scratch-pin", "path": "contracts/scratch-pin.yaml", "type": "pin",
         "consumption_rule": f"Invoke `{entrypoint}` from the checkout."}]}),
        encoding="utf-8")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "cannot say WHICH disposition a line belongs to" in captured.out, (
        captured.out)
    assert "nothing classified" in captured.out, captured.out


def test_a_flow_sequence_of_citations_is_refused_rather_than_read(
        tmp_path, monkeypatch, capsys) -> None:
    """`cited_to: [a, b]` parses to two citations and carries no list-item line
    at all — a form the pin's own reader does not admit. Refused loudly, not
    read halfway."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    pin_file = tmp_path / "contracts" / "scratch-pin.yaml"
    pin_file.parent.mkdir(parents=True)
    pin_file.write_text(
        "kind: pinned_contract_manifest\n"
        f"consumer_entrypoint: {entrypoint}\n"
        "dispositions:\n"
        "  - repo: scratchFactory\n"
        "    item: a-declared-change\n"
        "    cited_to: [openspec/changes/gone/spec.md, council LA-A1]\n",
        encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [
        {"id": "scratch-pin", "path": "contracts/scratch-pin.yaml", "type": "pin",
         "consumption_rule": f"Invoke `{entrypoint}` from the checkout."}]}),
        encoding="utf-8")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "0 `cited_to:` line(s) in its bytes and 2 parsed citation(s)" in (
        captured.out), captured.out


# ---- fixture 1: every citation form the live pin uses, all coherent ----

def test_citations_in_every_form_pass_and_the_count_says_what_was_measured(
        tmp_path, monkeypatch, capsys) -> None:
    module = _load_checker()
    (tmp_path / "openspec" / "specs" / "some").mkdir(parents=True)
    (tmp_path / "openspec/specs/some/spec.md").write_text("# canon\n",
                                                          encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/a-record.md").write_text("# a record\n", encoding="utf-8")
    manifest = _raw_case(tmp_path, [
        f"openspec/specs/some/spec.md:1770 {DASH} the promoted requirement",
        f"docs/a-record.md {DASH} the record, cited whole",
        f"council LA-A1 {DASH} the ruling that reserved the marker forms",
        f"PR #444 {DASH} the landed change",
        f"https://example.invalid/upstream {DASH} the upstream note",
        f"codexFactory openspec/changes/not-here/spec.md {DASH} another tree",
    ], repo="codexFactory")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert ("OK scratch-pin: 1 disposition(s) carry 6 citation(s) naming 5 "
            "referent(s) — 2 name a path in this tree, 1 a URL, 1 a forge "
            "reference, 1 a path qualified to another repository; 1 citation(s) "
            "name no machine referent") in captured.out, captured.out
    assert "every in-tree path resolves" in captured.out, captured.out


def test_a_citation_naming_a_directory_resolves(
        tmp_path, monkeypatch, capsys) -> None:
    """`.exists()` and not `.is_file()`: a citation legitimately names a change
    packet's directory, and refusing one would be this checker inventing a rule
    the pin does not carry."""
    module = _load_checker()
    (tmp_path / "openspec" / "changes" / "a-packet").mkdir(parents=True)
    manifest = _raw_case(tmp_path, [
        f"openspec/changes/a-packet {DASH} the packet, cited as a whole",
    ])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)
    assert exit_code == 0, capsys.readouterr().out


# ---- fixture 2: the citation names a path that is not in the tree ----

def test_a_citation_naming_a_path_that_is_gone_is_reported(
        tmp_path, monkeypatch, capsys) -> None:
    """#834's drift, reproduced: the citation is well formed, the disposition is
    ratified and cited, and the path it names was renamed away."""
    module = _load_checker()
    manifest = _raw_case(tmp_path, [
        f"openspec/changes/prepare-openspec-1.12-readiness/evidence/measured.md "
        f'§ "The two refusals" {DASH} the measurement',
    ])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert ("FAIL scratch-pin: dispositions[1] (a-declared-change) cites "
            "`openspec/changes/prepare-openspec-1.12-readiness/evidence/"
            "measured.md`, but no such path is in this tree") in captured.out, (
        captured.out)
    assert "a suppression with a footnote" in captured.out, captured.out
    # And the row's OK line is withheld: a row with a dangling citation does not
    # cohere, whatever its entrypoint does.
    assert "OK scratch-pin: `contracts/scratch-pin.yaml` is present" not in (
        captured.out), captured.out
    assert "MEASURED scratch-pin:" in captured.out, captured.out


def test_each_dangling_citation_is_reported_separately(
        tmp_path, monkeypatch, capsys) -> None:
    module = _load_checker()
    manifest = _raw_case(tmp_path, [
        f"openspec/changes/gone-one/spec.md {DASH} one",
        f"openspec/changes/gone-two/spec.md {DASH} two",
    ])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "cites `openspec/changes/gone-one/spec.md`" in captured.out
    assert "cites `openspec/changes/gone-two/spec.md`" in captured.out
    assert "FAIL 2 finding(s) over 1 pin registration(s)" in captured.out, (
        captured.out)


# ---- fixture 3: the reference is malformed as a repo-relative path ----

def test_a_host_absolute_citation_is_refused_even_though_it_exists(
        tmp_path, monkeypatch, capsys) -> None:
    """The containment group's argument, on the citation field: the fixture names
    a REAL host file by absolute path, so a checker that merely joined and asked
    `.exists()` would report it present while no consumer's checkout carries
    it — and Article IV refuses a committed host path on its own terms."""
    module = _load_checker()
    absolute = str(REPO_ROOT / "pytest.ini")
    assert Path(absolute).is_file()
    manifest = _raw_case(tmp_path, [f"{absolute} {DASH} the host's own copy"])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "is an ABSOLUTE path" in captured.out, captured.out
    assert "a citation is opened from the pinned checkout" in captured.out, (
        captured.out)


def test_a_citation_that_walks_out_of_the_tree_is_refused(
        tmp_path, monkeypatch, capsys) -> None:
    module = _load_checker()
    outside = tmp_path.parent / "outside-cited.md"
    outside.write_text("# outside\n", encoding="utf-8")
    manifest = _raw_case(tmp_path, [
        f"../outside-cited.md {DASH} a path out of the tree",
    ])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "contains a '..' segment" in captured.out, captured.out


# ---- fixture 4: no dispositions, so the assertion does not apply ----

def test_a_pin_with_no_dispositions_is_reported_as_inapplicable_not_silent(
        tmp_path, monkeypatch, capsys) -> None:
    """Canon obliges no pin to carry `dispositions:` — the two sibling pins carry
    none — and the line says the assertion did not apply, so a reader can tell an
    inapplicable assertion from an unmade one."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin",
             "consumption_rule": f"Invoke `{entrypoint}` from the checkout."},
        pin={"kind": "pinned_contract_manifest",
             "consumer_entrypoint": entrypoint},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert ("carries no `dispositions:`, so the citation assertion does not "
            "apply") in captured.out, captured.out


def test_a_disposition_with_no_cited_to_is_left_to_the_pins_own_verifier(
        tmp_path, monkeypatch, capsys) -> None:
    """`cited_to:`'s PRESENCE is `validate-openspec-cli-pin.py`'s refusal
    (`pin-disposition-malformed`), in its own words. Restating another checker's
    finding in different words is what § 5.4 refused when it kept these
    questions in separate families — so this arm counts it and says whose it
    is."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    pin = _pin_with_citations([], entrypoint)
    del pin["dispositions"][0]["cited_to"]
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin",
             "consumption_rule": f"Invoke `{entrypoint}` from the checkout."},
        pin=pin, pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "1 disposition(s) carry no `cited_to:` list" in captured.out, (
        captured.out)
    assert "pin-disposition-malformed" in captured.out, captured.out


# ---- the two grammars, measured and named for a successor ----

def test_the_readers_divergence_is_warned_and_moves_no_verdict(
        tmp_path, monkeypatch, capsys) -> None:
    """MEASURED ON THE LIVE PIN, and reported rather than repaired. Quoting these
    scalars changes what the pin's line-based reader CAPTURES (its production
    takes the remainder of the line, quotes included) in a file vendored
    byte-identical into three sibling repositories: a governed repair with a
    re-vendor cost, not a path a plain fix may take. `WARN` names it and does not
    move the exit code — and the classification is done on the LINE, so no
    verdict rests on the divergence either way."""
    module = _load_checker()
    (tmp_path / "openspec" / "specs").mkdir(parents=True)
    (tmp_path / "openspec/specs/spec.md").write_text("# canon\n", encoding="utf-8")
    manifest = _raw_case(tmp_path, [
        f"openspec/specs/spec.md {DASH} the measurement, `Totals: 23 passed, "
        f"2 failed (25 items)`",
    ])
    raw = yaml.safe_load(
        (tmp_path / "contracts/scratch-pin.yaml").read_text(encoding="utf-8"))
    assert isinstance(raw["dispositions"][0]["cited_to"][0], dict), (
        "the fixture is only a fixture while PyYAML still reads this as a map")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "WARN scratch-pin: dispositions[1] (a-declared-change)" in (
        captured.out), captured.out
    assert "single-key MAPPING (rejoined byte for byte)" in captured.out, (
        captured.out)
    assert "1 read as a single-key mapping" in captured.out, captured.out
    assert "GOVERNED REPAIR, NOT THIS ARM'S" in captured.out, captured.out
    assert "1 name a path in this tree" in captured.out, captured.out


def test_the_yaml_reading_is_reported_never_relied_on() -> None:
    module = _load_checker()
    line = ("openspec/specs/spec.md — the measurement, `Totals: 23 passed, "
            "2 failed (25 items)`")
    parsed = yaml.safe_load(f"cited_to:\n  - {line}\n")["cited_to"][0]
    assert not isinstance(parsed, str)
    assert module.yaml_reading_of(parsed) == line
    assert module.yaml_reading_of("plain") == "plain"
    assert module.yaml_reading_of(["a", "b"]) is None
    assert module.yaml_reading_of(17) is None
    assert module.yaml_reading_of({"a": 1, "b": 2}) is None
    # The rejoin is a REPORT of what the parser saw, not a source of referents:
    # a coerced value comes back with the coercion visible, and nothing is
    # classified from it.
    assert module.yaml_reading_of({"openspec/gone.md": False}) == (
        "openspec/gone.md: False")


def test_the_citation_lines_are_read_from_the_bytes() -> None:
    module = _load_checker()
    text = ("dispositions:\n"
            "  - repo: scratchFactory\n"
            "    cited_to:\n"
            "      - first — one\n"
            "      - second — two\n"
            "    ratified_by: a human\n"
            "  - repo: other\n"
            "    cited_to:\n"
            "      - third — three\n")
    assert module.citation_lines_in(text) == [
        "first — one", "second — two", "third — three"]
    # `yaml.safe_dump` writes a sequence at its key's own column, which is the
    # shape every dumped fixture in this file has.
    dumped = yaml.safe_dump({"dispositions": [{"cited_to": ["a/b.md", "c"]}]},
                            allow_unicode=True)
    assert module.citation_lines_in(dumped) == ["a/b.md", "c"]
    assert module.citation_lines_in("dispositions: []\n") == []


def test_the_repository_vocabulary_is_the_pins_own_repo_fields() -> None:
    module = _load_checker()
    assert module.repository_qualifiers(
        {"dispositions": [{"repo": "codexFactory"}, {"repo": "openxFactory"},
                          {"repo": " codexFactory "}, {"item": "no repo"},
                          "not a mapping", {"repo": 17}]}) == frozenset(
        {"codexfactory", "openxfactory"})
    assert module.repository_qualifiers({}) == frozenset()


def test_own_repository_spellings_agree_with_doc_healths_committed_set() -> None:
    """The restated constant, pinned equal to the one it was taken from. This arm
    is a standalone script and does not import the doc-health package (which
    reaches for git), so the set is written out — and a divergence reds here
    rather than drifting into two dialects for one question."""
    module = _load_checker()
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    try:
        from doc_health import pin_class
    finally:
        sys.path.pop(0)
    assert module.OWN_REPOSITORY_SPELLINGS == pin_class.OWN_REPOSITORY_SPELLINGS


# ---- the arm runs even where the entrypoint assertions are terminal ----

def test_a_dangling_citation_is_reported_beside_a_terminal_entrypoint_refusal(
        tmp_path, monkeypatch, capsys) -> None:
    """The ordering decision, asserted so it is a decision and not an accident:
    `consumer_entrypoint: 17` is terminal for the row, and running the citation
    arm afterwards would hide every dangling citation behind that one finding."""
    module = _load_checker()
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin", "consumption_rule": "CHECK OUT, NEVER COPY."},
        pin=_pin_with_citations(
            [f"openspec/changes/gone/spec.md {DASH} the measurement"], 17),
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "is not a non-empty string path" in captured.out, captured.out
    assert "cites `openspec/changes/gone/spec.md`" in captured.out, captured.out
    assert "FAIL 2 finding(s) over 1 pin registration(s)" in captured.out, (
        captured.out)


# ---- the reader, stated directly at its boundaries ----

def test_the_citation_grammar_is_stated_directly() -> None:
    """The grammar the PIN documents, and not one character more. Its header says
    of the field exactly "`cited_to:` is required and must be non-empty", and its
    own reader admits a list of non-empty LINES whose members it never parses. So
    every token of a line's referent region is read, the form decides the kind,
    and every referent this tree does not own is recognised-and-unresolved rather
    than a finding."""
    module = _load_checker()
    declared = frozenset({"codexfactory", "openxfactory"})
    read = lambda text: module.read_citation(text, declared)

    # An unqualified repo-relative path is THIS tree's, and it is resolved —
    # wherever in the line it sits.
    assert read(f"openspec/specs/doc-health/spec.md {DASH} canon") == [
        ("tree-path", "openspec/specs/doc-health/spec.md")]
    assert read(f"openspec/specs/doc-health/spec.md:1770 {DASH} canon") == [
        ("tree-path", "openspec/specs/doc-health/spec.md")]
    assert read(f"the packet at openspec/changes/a/tasks.md {DASH} the work") == [
        ("tree-path", "openspec/changes/a/tasks.md")]
    # The `§` section and a trailing parenthetical are cut with the gloss.
    assert read(f'openspec/changes/a/evidence/m.md § "The two refusals" {DASH} '
                f"the measurement") == [
        ("tree-path", "openspec/changes/a/evidence/m.md")]
    assert read(f"codexFactory PR #216 (prepare-openspec-1-12-readiness, head "
                f"b2a6af34) {DASH} the packet") == [("reference", "#216")]

    # A QUALIFIER puts the path in another context, so this tree does not
    # resolve it — and the qualifier is a DECLARED repository name, immediately
    # in front of the path, not merely a preceding word.
    assert read(f"codexFactory openspec/changes/a/spec.md {DASH} another tree") \
        == [("qualified", "openspec/changes/a/spec.md")]
    assert read(f"codexFactory hermes/domain/records/r.md §5.1/§12.0 {DASH} a "
                f"ruling") == [("qualified", "hermes/domain/records/r.md")]
    # This repository's own name qualifies nothing away.
    assert read(f"openxFactory openspec/specs/x.md {DASH} this tree") == [
        ("tree-path", "openspec/specs/x.md")]
    # A repository the pin never declares is not in the vocabulary, so its path
    # is read as this tree's and reported missing. Stated because it is a
    # boundary and not an accident: a loud finding a reader answers by declaring
    # the repository, over a silent pass on a path nobody opened.
    assert read(f"MedxFactory openspec/specs/x.md {DASH} an undeclared tree") \
        == [("tree-path", "openspec/specs/x.md")]

    # A `#` or a `://` means the referent is not a path.
    assert read(f"PR #444 {DASH} the landed change") == [("reference", "#444")]
    assert read(f"#673 {DASH} the readiness issue") == [("reference", "#673")]
    assert read(f"opensoft/openxFactory#840 {DASH} the issue") == [
        ("reference", "opensoft/openxFactory#840")]
    assert read(f"https://example.invalid/x {DASH} upstream") == [
        ("url", "https://example.invalid/x")]

    # No machine referent: read as prose and never reported missing.
    assert read(f"council LA-A1 {DASH} the ruling") == []
    assert read(f"1.12.0 {DASH} the version this was measured at") == []
    assert read(f"{DASH} a gloss and nothing else") == []
    assert read("") == []
    assert read("   ") == []

    # The line may continue past its path, and the path is still read.
    assert read("openspec/gone.md: gone with the rename") == [
        ("tree-path", "openspec/gone.md")]
    assert read(f"see #444 openspec/gone.md {DASH} both referents") == [
        ("reference", "#444"), ("tree-path", "openspec/gone.md")]

    # The `:<line>` suffix is a reading aid: stripped, and deliberately NOT
    # checked, because a line number drifts with every edit above it while the
    # citation still names the right document — and the pin documents no line
    # grammar to enforce either way.
    assert read(f"docs/a.md:999999 {DASH} a line far past EOF") == [
        ("tree-path", "docs/a.md")]

    # The gloss is not scanned, and the reason is that prose carries slashes
    # that are not paths.
    assert read(f"docs/a.md {DASH} measured and/or re-derived on 2026/09/09") \
        == [("tree-path", "docs/a.md")]
    assert module.referent_region(
        f"docs/a.md {DASH} the gloss") == "docs/a.md"


# --------------------------------------------------------------------------
# The reader is STRUCTURAL — issue #851, from the bench on PR #842
#
# Two findings, and the first of them is the one the arm's global-count
# alignment could not see. A `cited_to:`/`- …` pair written inside a folded
# `why: >-` was admitted as structure while a `#` comment between two real items
# ENDED the real list; the two errors CANCEL, the counts agree, `zip` pairs the
# wrong lines, and a dangling citation after the comment is never opened while
# the run exits 0 — this arm's own silence, in the shape it exists to end. The
# second is the unquoting rule: the production reader passes every item through
# `_unquote`, so quoting a scalar (the repair this arm NAMES for a successor, for
# the ` #` and `: ` ambiguities it measures) would leave a permanent divergence
# warning behind if this reader kept the quotes — a repair that cannot clear the
# warning it was made for.
#
# The fixtures are written as RAW BYTES for the same reason the bench's earlier
# group is: `yaml.safe_dump` would quote the defect away before the arm saw it.
# --------------------------------------------------------------------------

def _decoy_and_comment_pin(tmp_path: Path) -> Path:
    """Codex's scenario, verbatim: a folded `why:` quoting the field's own
    grammar, a comment between two real items, and a DANGLING citation after
    that comment. The decoy names a path that EXISTS, so the arm as first
    written exits 0 on this tree — which is what makes the fixture a fixture."""
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    (tmp_path / "openspec" / "specs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "openspec/specs/spec.md").write_text("# canon\n", encoding="utf-8")
    (tmp_path / "openspec" / "decoy").mkdir(parents=True, exist_ok=True)
    (tmp_path / "openspec/decoy/never-opened.md").write_text(
        "# not a citation\n", encoding="utf-8")
    pin_file = tmp_path / "contracts" / "scratch-pin.yaml"
    pin_file.parent.mkdir(parents=True, exist_ok=True)
    pin_file.write_text(
        "kind: pinned_contract_manifest\n"
        f"consumer_entrypoint: {entrypoint}\n"
        "dispositions:\n"
        "  - repo: scratchFactory\n"
        "    item: a-declared-change\n"
        "    why: >-\n"
        "      The reason, which quotes the field's own grammar because that is\n"
        "      what a disposition about this checker would have to do:\n"
        "      cited_to:\n"
        "        - openspec/decoy/never-opened.md — quoted prose, not structure\n"
        "    cited_to:\n"
        f"      - openspec/specs/spec.md {DASH} the real first citation\n"
        "      # the ratification thread, noted between the items\n"
        f"      - openspec/changes/gone/spec.md {DASH} the dangling one\n"
        "    ratified_by: a human, on a date, in their own words\n",
        encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [
        {"id": "scratch-pin", "path": "contracts/scratch-pin.yaml", "type": "pin",
         "consumption_rule": f"Invoke `{entrypoint}` from the checkout."}]}),
        encoding="utf-8")
    return manifest


def test_a_folded_decoy_and_a_comment_no_longer_cancel_each_other_out(
        tmp_path, monkeypatch, capsys) -> None:
    """THE BENCH'S CASE, END TO END. The arm as first written read the folded
    decoy as one citation line and stopped the real list at the comment, so two
    lines met two parsed citations, the counts agreed, and the citation AFTER the
    comment — the dangling one — was never classified at all. It is classified
    now, and the decoy is not."""
    module = _load_checker()
    manifest = _decoy_and_comment_pin(tmp_path)

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert ("dispositions[1] (a-declared-change) cites "
            "`openspec/changes/gone/spec.md`") in captured.out, captured.out
    # The decoy is prose inside a block scalar and is never read as structure —
    # neither opened, nor counted, nor named.
    assert "never-opened" not in captured.out, captured.out
    assert "2 citation(s)" in captured.out, captured.out


def test_the_folded_decoy_case_is_bound_line_by_line_to_its_entry(
        tmp_path) -> None:
    """The same fixture read directly, so the binding is asserted and not merely
    inferred from the finding above."""
    module = _load_checker()
    _decoy_and_comment_pin(tmp_path)
    text = (tmp_path / "contracts/scratch-pin.yaml").read_text(encoding="utf-8")
    assert module.citation_lines_by_entry(text) == [
        (1, f"openspec/specs/spec.md {DASH} the real first citation"),
        (1, f"openspec/changes/gone/spec.md {DASH} the dangling one")]
    parsed = list(module.parsed_citations_of(
        yaml.safe_load(text)["dispositions"]))
    assert [entry for entry, _line in module.citation_lines_by_entry(text)] == [
        index for index, _item, _citation in parsed]


def test_the_reader_walks_the_structure_and_binds_every_line_to_its_entry(
        ) -> None:
    """The three rules, stated directly: a block scalar's body is skipped whole,
    a comment or a blank line does not end a list, and every line comes back
    bound to the `dispositions[]` entry whose block carries it."""
    module = _load_checker()
    text = ("kind: pinned_contract_manifest\n"
            "dispositions:\n"
            "  - repo: scratchFactory\n"
            "    why: |\n"
            "      A literal block that happens to contain\n"
            "      cited_to:\n"
            "        - openspec/decoy/a.md — prose\n"
            "    cited_to:\n"
            "      - first — one\n"
            "\n"
            "      # a comment, and a blank line above it\n"
            "      - second — two\n"
            "    ratified_by: a human\n"
            "  - repo: other\n"
            "    cited_to:\n"
            "      - third — three\n"
            "notes: >-\n"
            "  a folded field AFTER the section, whose body is not structure:\n"
            "  cited_to:\n"
            "    - openspec/decoy/b.md — prose\n")
    assert module.citation_lines_by_entry(text) == [
        (1, "first — one"), (1, "second — two"), (2, "third — three")]
    assert module.citation_lines_in(text) == [
        "first — one", "second — two", "third — three"]


def test_equal_totals_that_fall_in_different_entries_refuse_the_field(
        tmp_path, monkeypatch, capsys) -> None:
    """EQUAL COUNTS ARE NOT AN ALIGNMENT, which is the whole of issue #851's
    first finding. Entry 1 carries a nested sequence — two list-item lines, one
    parsed citation — and entry 2 carries a flow sequence, which is one parsed
    citation and no line at all. The totals agree; the binding does not; the
    field is refused rather than classified against the wrong entry."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    pin_file = tmp_path / "contracts" / "scratch-pin.yaml"
    pin_file.parent.mkdir(parents=True)
    pin_file.write_text(
        "kind: pinned_contract_manifest\n"
        f"consumer_entrypoint: {entrypoint}\n"
        "dispositions:\n"
        "  - repo: scratchFactory\n"
        "    item: first-entry\n"
        "    cited_to:\n"
        "      - - openspec/changes/gone/spec.md\n"
        "        - a second line of one citation\n"
        "  - repo: scratchFactory\n"
        "    item: second-entry\n"
        "    cited_to: [council LA-A1]\n",
        encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [
        {"id": "scratch-pin", "path": "contracts/scratch-pin.yaml", "type": "pin",
         "consumption_rule": f"Invoke `{entrypoint}` from the checkout."}]}),
        encoding="utf-8")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "do not fall in the same `dispositions[]` entries" in captured.out, (
        captured.out)
    assert "bytes 1x2, structure 1x1, 2x1" in captured.out, captured.out
    assert "cannot say WHICH disposition a line belongs to" in captured.out, (
        captured.out)
    assert "nothing classified" in captured.out, captured.out


# ---- the production unquoting rule, applied here too ----

def test_a_quoted_citation_scalar_no_longer_diverges(
        tmp_path, monkeypatch, capsys) -> None:
    """THE REPAIR THIS ARM NAMES FOR A SUCCESSOR, MADE POSSIBLE. Quoting the
    scalar is what clears the ` #` and `: ` ambiguities the arm measures; the
    production reader passes every item through `_unquote`, so its semantic
    citation carries no quotes. This reader now applies the same rule, so the
    quoted line and the parsed string agree and no divergence WARN survives the
    repair. The path is still read out of the line, quotes and all."""
    module = _load_checker()
    (tmp_path / "openspec" / "specs").mkdir(parents=True)
    (tmp_path / "openspec/specs/spec.md").write_text("# canon\n", encoding="utf-8")
    manifest = _raw_case(tmp_path, [
        f'"openspec/specs/spec.md {DASH} the measurement, `Totals: 23 passed, '
        f'2 failed (25 items)`"',
        f"'openspec/specs/spec.md {DASH} PR #444, the landed change'",
    ])
    raw = yaml.safe_load(
        (tmp_path / "contracts/scratch-pin.yaml").read_text(encoding="utf-8"))
    assert all(isinstance(c, str) for c in raw["dispositions"][0]["cited_to"]), (
        "the fixture is only a fixture while quoting makes these plain strings")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "WARN" not in captured.out, captured.out
    assert "read differently" not in captured.out, captured.out
    assert "2 name a path in this tree" in captured.out, captured.out


def test_the_reader_unquotes_the_line_the_way_the_production_reader_does(
        ) -> None:
    module = _load_checker()
    text = ("dispositions:\n"
            "  - repo: scratchFactory\n"
            "    cited_to:\n"
            "      - \"Totals: 23 passed, 2 failed (25 items)\"\n"
            "      - 'PR #444 — the landed change'\n"
            "      - openspec/specs/spec.md — unquoted, and unchanged\n"
            "      - `a backquoted span` — not a YAML quote, and left alone\n")
    assert module.citation_lines_in(text) == [
        "Totals: 23 passed, 2 failed (25 items)",
        "PR #444 — the landed change",
        "openspec/specs/spec.md — unquoted, and unchanged",
        "`a backquoted span` — not a YAML quote, and left alone"]


def test_the_unquoting_rule_is_the_production_readers_own_rule() -> None:
    """The restated rule, pinned equal to the one it was taken from — the same
    discipline `OWN_REPOSITORY_SPELLINGS` is held to, and for the same reason:
    `scripts/validate-openspec-cli-pin.py` is hyphenated and unimportable, so the
    rule is written out here and a divergence must RED rather than drift."""
    module = _load_checker()
    spec = importlib.util.spec_from_file_location(
        "validate_openspec_cli_pin_for_parity",
        REPO_ROOT / "scripts" / "validate-openspec-cli-pin.py")
    assert spec and spec.loader
    production = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(production)
    for raw in ['"quoted"', "'quoted'", "plain", '"unbalanced', "mixed'",
                '"', "''", '""', "  padded  ", '"PR #444 — a citation"',
                "'openspec/a.md: gone'", "`backquoted`", "", "-",
                '"nested \'inner\' quotes"']:
        assert module._unquote(raw) == production._unquote(raw), raw


# ---- a failing row is never labelled OK — Copilot on PR #842 ----

def test_a_row_failing_on_a_citation_is_not_labelled_ok_where_it_names_no_entrypoint(
        tmp_path, monkeypatch, capsys) -> None:
    """The entrypoint branch returns the CITATION arm's verdict, so its line has
    to carry that verdict's label too: a row failing on a dangling citation must
    not print `OK` about the assertions that did not apply."""
    module = _load_checker()
    manifest = _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin", "consumption_rule": "CHECK OUT, NEVER COPY."},
        pin={"kind": "pinned_contract_manifest",
             "dispositions": [{
                 "repo": "scratchFactory", "item": "a-declared-change",
                 "cited_to": [f"openspec/changes/gone/spec.md {DASH} the "
                              f"measurement"]}]},
        pin_relpath="contracts/scratch-pin.yaml")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert ("MEASURED scratch-pin: `contracts/scratch-pin.yaml` is registered "
            "and present; it names no `consumer_entrypoint:`") in captured.out, (
        captured.out)
    assert "OK scratch-pin: `contracts/scratch-pin.yaml` is registered" not in (
        captured.out), captured.out
    # The inapplicability is still said, which is what the branch is for.
    assert "the entrypoint assertions do not apply" in captured.out, captured.out
