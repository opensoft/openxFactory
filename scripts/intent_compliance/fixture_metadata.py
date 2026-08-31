from dataclasses import dataclass
from pathlib import Path

from .model import InputLimitError, bounded_yaml_text


@dataclass(frozen=True)
class NegativeFixtureMetadata:
    text: str
    expected_failure: str
    requirement: str


def read_fixture_metadata(path: Path) -> NegativeFixtureMetadata:
    text = bounded_yaml_text(path)
    lines = text.splitlines()
    failure_prefix = "# expected-failure: "
    if not lines or not lines[0].startswith(failure_prefix):
        raise InputLimitError(path, f"must begin with {failure_prefix.strip()}")
    failure = lines[0].removeprefix(failure_prefix).strip()
    if not failure:
        raise InputLimitError(path, "declares an empty expected failure code")
    requirement_prefix = "# requirement: "
    if len(lines) < 2 or not lines[1].startswith(requirement_prefix):
        raise InputLimitError(
            path, f"must declare {requirement_prefix.strip()} on line 2"
        )
    requirement = lines[1].removeprefix(requirement_prefix).strip()
    if not requirement:
        raise InputLimitError(path, "declares an empty requirement")
    return NegativeFixtureMetadata(text, failure, requirement)


def expected_failure_code(path: Path) -> str:
    return read_fixture_metadata(path).expected_failure


def expected_requirement(path: Path) -> str:
    return read_fixture_metadata(path).requirement
