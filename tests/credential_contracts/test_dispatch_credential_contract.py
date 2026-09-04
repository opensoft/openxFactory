"""The credential-contracts validator's dispatch-credential self-test gates the
packaged examples (add-dispatch-credential-contract task 2.2): the positives are
schema-valid with no semantic finding, and each negative raises its intended
code — dispatch-scope-ceiling, shared-secret-identity, baked-secret.

add-binding-consumer-identity adds two channels beside those two. `warning/`
holds a probe per deprecation code, because a warning fixture placed among the
positives failed the self-test as "unexpectedly invalid" and one placed in
`negative/` failed it as "has no registered expectation" — so the deprecation
the next major depends on had nowhere to hold its proof. `support/` holds
records the validator INDEXES for reference resolution and adjudicates for
nothing, because a qualified requirement reference needs something to resolve
AT.

THE BY-NAME INVENTORY BELOW IS THE CONTROL, AND IT IS NOT OPTIONAL. The verbatim
count string is redundant beside it — the inventory catches every drop AND says
which — and the count is ruled DERIVE in its own test-hygiene issue. Deriving it
is safe on exactly ONE condition: every fixture a change adds joins the
inventory in the SAME COMMIT. Deriving without that is the fail-open version and
would silently accept a shrinking corpus of security probes.

Matches the repo's validator-gating pattern: invoke the script, assert exit 0.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate-credential-contracts.py"
EXAMPLES = ROOT / "examples" / "credential-contracts"

POSITIVES = (
    "openxdox-dispatch.requirements.example.yaml",
    "openxdox-dispatch.binding-template.example.yaml",
    "roster-drift.requirements.example.yaml",
    # add-binding-consumer-identity: the two-consumer shape the predecessor had
    # to DECLINE, and the stub the domain-starter generator emits.
    "two-consumer-operated-identity.requirements.example.yaml",
    "two-consumer-operated-identity.binding-template.example.yaml",
    "instantiation-stub.binding-template.example.yaml",
    # add-requirement-ref-resolution-integrity § 4.3 (OQ-4): the SILENT
    # direction as its own file, so a regression in it names itself. Two
    # bindings sharing no secret, each reference resolving to exactly one
    # requirement — the fixture a check that fired on every declared reference
    # would fail.
    "resolving-requirement-ref.binding-template.example.yaml",
    # add-consumer-identity-namespace: THE CLEARING DIRECTION. Two tenants of
    # one provider whose principals share a name, distinguished by the
    # namespace that issued each — the record that was a false refusal before
    # the member existed, packaged so the silence has a probe of its own.
    "two-tenant-identity-namespace.binding-template.example.yaml",
)

NEGATIVES = (
    "dispatch-reuses-content-secret.yaml",
    "dispatch-grants-contents.yaml",
    "baked-secret-in-binding.yaml",
    "issuance-precondition-out-of-vocabulary.yaml",
    "issuance-precondition-valued-false.yaml",
    # add-binding-consumer-identity: one per named refusal.
    "dispatch-content-pair-declares-sharing.yaml",
    "consumer-shared-holder-reference.yaml",
    "consumer-one-sided-acknowledgment.yaml",
    "consumer-acknowledgment-valued-false.yaml",
    "consumer-requirement-ref-unresolvable.yaml",
    "consumer-requirement-ref-ambiguous.yaml",
    "consumer-requirement-ref-escapes-tree.yaml",
    "consumer-shared-authority-identity.yaml",
    "three-bindings-two-share-authority.yaml",
    "consumer-holder-ref-raw-secret.yaml",
    "consumer-fetch-identity-raw-secret.yaml",
    # add-consumer-identity-namespace: the two shapes the namespace must NOT
    # clear — one namespace on both sides, and a namespace on one side only —
    # plus the third free string joining the raw-secret screen.
    "consumer-shared-authority-same-namespace.yaml",
    "consumer-shared-authority-one-sided-namespace.yaml",
    "consumer-identity-namespace-raw-secret.yaml",
)

WARNINGS = (
    "consumer-identity-undeclared.yaml",
    "live-values-in-stub-named-file.template.yaml",
    "consumer-block-incomplete.yaml",
    "consumer-block-locally-shaped.yaml",
    "consumer-block-unknown-member.yaml",
    "consumer-member-grammar.yaml",
    "consumer-token-not-true.yaml",
    "consumer-binding-key-grammar.yaml",
    "consumer-access-mode-vocabulary.yaml",
    "consumer-requirement-ref-grammar.yaml",
    # add-requirement-ref-resolution-integrity § 4.1 / § 4.2: one probe per code
    # of the SECOND family, each on a binding that shares its secret with
    # nobody — which is the scope the codes exist to widen.
    "requirement-ref-unresolved.yaml",
    "requirement-ref-ambiguous.yaml",
    # add-consumer-identity-namespace § the ninth shape: one probe for the one
    # code, without which the ninth deprecation would ship unevidenced.
    "consumer-identity-namespace-grammar.yaml",
)

SUPPORT = (
    "ambiguous-requirement-ids.requirements.yaml",
)


def _run() -> subprocess.CompletedProcess[str]:
    # the validator runs its self-test on every invocation; the positional arg
    # is the (here empty) domain-repo scan target.
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(ROOT)],
        capture_output=True,
        text=True,
    )


def test_selftest_passes_on_the_packaged_examples() -> None:
    result = _run()
    assert result.returncode == 0, result.stdout + result.stderr
    # The counts grew by add-client-identity-roster (Decision B): one positive
    # declaring the roster-drift issuance precondition, and two negatives for
    # the closed vocabulary's two failure shapes. They grew again by
    # add-binding-consumer-identity, which adds the two-consumer positive its
    # predecessor had to decline, the stub the generator emits, eleven negatives
    # (one per named refusal) and a `warning/` channel carrying one probe per
    # deprecation code. They grew a third time by
    # add-requirement-ref-resolution-integrity: two warning probes (one per code
    # of the resolution-integrity family) and ONE positive proving the SILENT
    # direction — 6 -> 7 positive, 10 -> 12 warning, negatives unmoved at 16.
    # They grew a FOURTH time by add-consumer-identity-namespace: one positive
    # (the clearing direction), three negatives (same namespace both sides, a
    # namespace on one side only, and the third free string under the raw-secret
    # screen) and one warning probe for the ninth deprecation code —
    # 7 -> 8 positive, 16 -> 19 negative, 12 -> 13 warning.
    assert (f"self-test: {len(POSITIVES)} positive + {len(NEGATIVES)} negative + "
            f"{len(WARNINGS)} warning example(s) confirmed") in result.stdout


def test_the_example_files_are_present() -> None:
    # guards against a self-test that passes vacuously because a rename dropped
    # the fixtures out of the glob.
    for positive in POSITIVES:
        assert (EXAMPLES / positive).is_file(), positive
    for negative in NEGATIVES:
        assert (EXAMPLES / "negative" / negative).is_file(), negative
    for warning in WARNINGS:
        assert (EXAMPLES / "warning" / warning).is_file(), warning
    for support in SUPPORT:
        assert (EXAMPLES / "support" / support).is_file(), support


def test_the_inventory_is_the_whole_corpus_and_not_a_sample() -> None:
    """The inventory dominates a count only while it is EXHAUSTIVE. A fixture on
    disk and absent from the list above would be a probe no drop could be
    detected against."""
    assert sorted(p.name for p in EXAMPLES.glob("*.example.yaml")) == sorted(POSITIVES)
    assert sorted(p.name for p in (EXAMPLES / "negative").glob("*.yaml")) == sorted(NEGATIVES)
    assert sorted(p.name for p in (EXAMPLES / "warning").glob("*.yaml")) == sorted(WARNINGS)
    assert sorted(p.name for p in (EXAMPLES / "support").glob("*.yaml")) == sorted(SUPPORT)
