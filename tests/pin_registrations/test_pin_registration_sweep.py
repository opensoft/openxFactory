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
