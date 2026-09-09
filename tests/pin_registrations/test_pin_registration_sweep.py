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
and the classifier stated at its boundaries are at the foot of this file, with
the reasoning beside them.

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
        pin_file.write_text(yaml.safe_dump(pin), encoding="utf-8")
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
# --------------------------------------------------------------------------

DASH = "—"


def _pin_with_citations(citations: list, entrypoint: str = "scripts/tool.py") -> dict:
    return {
        "kind": "pinned_contract_manifest",
        "consumer_entrypoint": entrypoint,
        "dispositions": [{
            "repo": "scratchFactory",
            "item": "a-declared-change",
            "path": "some-capability/spec.md",
            "level": "ERROR",
            "finding": "the tool's message, matched whole",
            "why": "the estate declared the narrowing",
            "cited_to": citations,
            "ratified_by": "a human, on a date, in their own words",
        }],
    }


def _case_with_citations(tmp_path: Path, citations: list) -> Path:
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir(exist_ok=True)
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    return _write_case(
        tmp_path,
        row={"id": "scratch-pin", "path": "contracts/scratch-pin.yaml",
             "type": "pin",
             "consumption_rule": f"Invoke `{entrypoint}` from the checkout."},
        pin=_pin_with_citations(citations, entrypoint),
        pin_relpath="contracts/scratch-pin.yaml")


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
    pin = yaml.safe_load(
        (REPO_ROOT / LIVE_PIN_PATH).read_text(encoding="utf-8"))
    citations = [c for entry in pin["dispositions"] for c in entry["cited_to"]]
    assert citations, "the live pin records no citations at all"
    in_tree = []
    for citation in citations:
        text = module.as_citation_text(citation)
        assert text is not None, citation
        kind, referent = module.classify_citation(text)
        if kind == "tree-path":
            in_tree.append(referent)
    assert len(in_tree) >= 2, in_tree
    missing = [p for p in in_tree if not (REPO_ROOT / p).exists()]
    assert not missing, f"citations naming paths that are gone: {missing}"


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


# ---- fixture 1: every citation form the live pin uses, all coherent ----

def test_citations_in_every_form_pass_and_the_count_says_what_was_measured(
        tmp_path, monkeypatch, capsys) -> None:
    module = _load_checker()
    (tmp_path / "openspec" / "specs" / "some").mkdir(parents=True)
    (tmp_path / "openspec/specs/some/spec.md").write_text("# canon\n",
                                                          encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/a-record.md").write_text("# a record\n", encoding="utf-8")
    manifest = _case_with_citations(tmp_path, [
        f"openspec/specs/some/spec.md:1770 {DASH} the promoted requirement",
        f"docs/a-record.md {DASH} the record, cited whole",
        f"council LA-A1 {DASH} the ruling that reserved the marker forms",
        f"PR #444 {DASH} the landed change",
        f"https://example.invalid/upstream {DASH} the upstream note",
        f"codexFactory openspec/changes/not-here/spec.md {DASH} another tree's path",
    ])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert ("OK scratch-pin: 1 disposition(s) carry 6 citation(s) — 2 name a "
            "path in this tree, 1 a URL, 1 a forge reference, 1 a path "
            "qualified to another repository, 1 no machine referent; every "
            "in-tree path resolves") in captured.out, captured.out


def test_a_citation_naming_a_directory_resolves(
        tmp_path, monkeypatch, capsys) -> None:
    """`.exists()` and not `.is_file()`: a citation legitimately names a change
    packet's directory, and refusing one would be this checker inventing a rule
    the pin does not carry."""
    module = _load_checker()
    (tmp_path / "openspec" / "changes" / "a-packet").mkdir(parents=True)
    manifest = _case_with_citations(tmp_path, [
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
    manifest = _case_with_citations(tmp_path, [
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
    manifest = _case_with_citations(tmp_path, [
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
    manifest = _case_with_citations(tmp_path, [
        f"{absolute} {DASH} the host's own copy",
    ])

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
    manifest = _case_with_citations(tmp_path, [
        f"../outside-cited.md {DASH} a path out of the tree",
    ])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "contains a '..' segment" in captured.out, captured.out


def test_a_citation_that_is_not_a_readable_value_is_reported(
        tmp_path, monkeypatch, capsys) -> None:
    """Neither a string nor a single-key mapping: nothing to reconstruct, so
    nothing to open."""
    module = _load_checker()
    manifest = _case_with_citations(tmp_path, [["a", "b"]])

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 1, captured.out
    assert "neither a string nor a single-key mapping" in captured.out, (
        captured.out)


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


# ---- the two grammars, and the WARN class ----

def test_a_citation_the_two_readers_disagree_about_is_warned_not_failed(
        tmp_path, monkeypatch, capsys) -> None:
    """MEASURED ON THE LIVE PIN. Two citations quote the tool's own output
    (```Totals: 23 passed, 2 failed (25 items)```), and a bare `: ` inside a
    plain scalar makes the line a single-key MAPPING to `yaml.safe_load` while
    the pin's own line-based reader takes the whole line as one string. The arm
    reconstructs the line the pin reads, classifies THAT, and warns — because
    quoting the scalar changes what that line reader CAPTURES, in a file
    vendored byte-identical into three sibling repositories, which is a governed
    repair and not this checker's to force."""
    module = _load_checker()
    entrypoint = "scripts/tool.py"
    (tmp_path / "scripts").mkdir()
    (tmp_path / entrypoint).write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    (tmp_path / "openspec" / "specs").mkdir(parents=True)
    (tmp_path / "openspec/specs/spec.md").write_text("# canon\n", encoding="utf-8")
    pin_file = tmp_path / "contracts" / "scratch-pin.yaml"
    pin_file.parent.mkdir(parents=True, exist_ok=True)
    # Written as RAW YAML, not `safe_dump`: the defect is in the bytes, and a
    # dumper would quote it away.
    pin_file.write_text(
        "kind: pinned_contract_manifest\n"
        f"consumer_entrypoint: {entrypoint}\n"
        "dispositions:\n"
        "  - repo: scratchFactory\n"
        "    item: a-declared-change\n"
        "    cited_to:\n"
        "      - openspec/specs/spec.md — the measurement, `Totals: 23 passed"
        ", 2 failed (25 items)`\n",
        encoding="utf-8")
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(yaml.safe_dump({"contracts": [
        {"id": "scratch-pin", "path": "contracts/scratch-pin.yaml", "type": "pin",
         "consumption_rule": f"Invoke `{entrypoint}` from the checkout."}]}),
        encoding="utf-8")
    raw = yaml.safe_load(pin_file.read_text(encoding="utf-8"))
    assert not isinstance(raw["dispositions"][0]["cited_to"][0], str), (
        "the fixture is only a fixture while PyYAML still reads this as a map")

    exit_code = _run_over(module, monkeypatch, tmp_path, manifest)

    captured = capsys.readouterr()
    assert exit_code == 0, captured.out
    assert "WARN scratch-pin: dispositions[1] (a-declared-change)" in (
        captured.out), captured.out
    assert "reads as a single-key MAPPING" in captured.out, captured.out
    assert "1 reconstructed from a single-key mapping" in captured.out, (
        captured.out)


def test_the_reconstruction_restores_the_line_the_pin_reader_sees() -> None:
    module = _load_checker()
    line = ("openspec/specs/spec.md — the measurement, `Totals: 23 passed, "
            "2 failed (25 items)`")
    parsed = yaml.safe_load(f"cited_to:\n  - {line}\n")["cited_to"][0]
    assert not isinstance(parsed, str)
    assert module.as_citation_text(parsed) == line
    assert module.as_citation_text("plain") == "plain"
    assert module.as_citation_text(["a", "b"]) is None
    assert module.as_citation_text(17) is None
    assert module.as_citation_text({"a": 1, "b": 2}) is None


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


# ---- the classifier, stated directly at its boundaries ----

def test_the_citation_grammar_is_stated_directly() -> None:
    """The grammar the PIN documents, and not one character more. Its header says
    of the field exactly "`cited_to:` is required and must be non-empty", and its
    own reader admits a list of non-empty lines whose members it never parses. So
    a referent is read only where a citation names one unambiguously, and every
    other form is recognised-and-unresolved rather than a finding."""
    module = _load_checker()
    kind_of = lambda text: module.classify_citation(text)[0]
    referent_of = lambda text: module.classify_citation(text)[1]

    # An unqualified repo-relative path is THIS tree's, and it is resolved.
    assert kind_of(f"openspec/specs/doc-health/spec.md {DASH} canon") == "tree-path"
    assert referent_of(
        f"openspec/specs/doc-health/spec.md:1770 {DASH} canon") == (
            "openspec/specs/doc-health/spec.md")
    # The `§` section and a trailing parenthetical are cut with the gloss.
    assert referent_of(
        f'openspec/changes/a/evidence/m.md § "The two refusals" {DASH} the '
        f"measurement") == "openspec/changes/a/evidence/m.md"
    assert referent_of(
        f"codexFactory PR #216 (prepare-openspec-1-12-readiness, head b2a6af34) "
        f"{DASH} the packet") == "#216"

    # A QUALIFIER puts the path in another context, so this tree does not
    # resolve it — and the qualifier is why, not the path's absence.
    assert kind_of(
        f"codexFactory openspec/changes/a/spec.md {DASH} another tree") == (
            "qualified")
    assert kind_of(
        f"codexFactory hermes/domain/records/r.md §5.1/§12.0 {DASH} a ruling"
    ) == "qualified"

    # A `#` or a `://` means the referent is not a path at all.
    assert kind_of(f"PR #444 {DASH} the landed change") == "reference"
    assert kind_of(f"#673 {DASH} the readiness issue") == "reference"
    assert kind_of(f"opensoft/openxFactory#840 {DASH} the issue") == "reference"
    assert kind_of(f"https://example.invalid/x {DASH} upstream") == "url"

    # No machine referent: read as prose and never reported missing.
    assert kind_of(f"council LA-A1 {DASH} the ruling") == "prose"
    assert kind_of(f"1.12.0 {DASH} the version this was measured at") == "prose"
    assert kind_of(f"{DASH} a gloss and nothing else") == "prose"

    # Not a citation this arm can read at all.
    assert kind_of("") == "unreadable"
    assert kind_of("   ") == "unreadable"

    # The `:<line>` suffix is a reading aid: stripped, and deliberately NOT
    # checked, because a line number drifts with every edit above it while the
    # citation still names the right document — and the pin documents no line
    # grammar to enforce either way.
    assert referent_of(f"docs/a.md:999999 {DASH} a line far past EOF") == (
        "docs/a.md")
