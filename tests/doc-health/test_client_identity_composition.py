"""The sixteenth family: client identity roster composition (task 6.6, 6.7).

**The trap this suite must not fall into (ruling A-9).** `conftest.make_ctx`
defaults `agg_root=None`, and this family's FIRST branch is
`ctx.agg_root is None -> Skip`. A test that calls `make_ctx` without passing
`agg_root` never reaches the family at all: it short-circuits into the skip and
passes vacuously, green while measuring nothing. **Every test below passes
`agg_root` explicitly**, and the single-repo-skip test passes `agg_root=None`
in the call so the omission can never be mistaken for the default. The
determinism assertion is the most exposed, because a vacuous skip satisfies
"identical findings across runs" trivially.

The fixture corpus (`fixtures/client-identity-composition/`) is FOUR repos and
five clients, each client a distinct discrimination:

  * `client-shared`   alpha + beta, the SAME `identity_ref`  -> disjunct (i)
  * `client-object`   gamma + delta, DIFFERENT `identity_ref` spellings and an
                      EQUAL `provider_object_ref`            -> disjunct (ii)
  * `client-spanning` alpha reaches exchange and publishes no entry for it,
                      beta publishes one                     -> reach, contested
  * `client-separate` alpha + beta, separate identities on one surface and
                      class in one client tenant             -> NOT a finding
  * `client-solo`     gamma alone                            -> nothing to add

Every fixture fragment is intra-repo CONFORMANT, which 6.7 measures with the
canonical roster validator. That is the whole point of ruling A-N4: the shared
identity passes the blocking domain gate, so the finding this family raises is
genuinely composition-only rather than a re-report of something the gate
already refused.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from conftest import AS_OF, FIXTURES, FakeGit, make_ctx

from doc_health import AUTO_FIXABLE, CONTESTED, DEFAULT_THRESHOLDS, Finding, Skip
from doc_health import corpus
from doc_health.families import FAMILIES
from doc_health.runner import Context

FAMILY = "client-identity-composition"
FAMILY_FIXTURES = FIXTURES / FAMILY
REPO_ROOT = Path(__file__).resolve().parents[2]
ROSTER_VALIDATOR = REPO_ROOT / "scripts" / "validate-client-identity-roster.py"

# Any aggregation path satisfies the family's first branch — it reads the
# pinned repos through `ctx.repo_paths`, never through the root itself. Passing
# the fixture directory keeps the value honest.
AGG_ROOT = FAMILY_FIXTURES

# The intra-repo codes this family MUST NEVER emit. They belong to the blocking
# canonical validator, and a duplicate here would turn a gate refusal into
# advice. Taken from the validator's own registered expectations so the list
# cannot drift away from the rules it names.
INTRA_REPO_CODES = (
    "duplicate-identity-key", "alias-pair-observationally-identical",
    "undeclared-reach", "undeclared-act-surface", "undeclared-scope-excess",
    "unverified-act-counted-as-access", "achieved-exceeds-intended-undeclared",
    "achieved-class-contradicts-permissions", "name-understates-achieved-authority",
    "unresolvable-gate-obligation", "missing-enforcement-test",
    "per-unit-principal-undeclared", "per-unit-principal-available-but-logical",
    "provider-enforced-without-per-unit-principal",
    "vendor-homed-declared-client-resident", "vendor-tenant-multi-missing-obligations",
    "mutate-without-ratified-capability", "false-standing-credential-attestation",
    "entry-without-consent-instrument", "unresolvable-consent-citation",
    "consent-instrument-not-in-force", "misplaced-roster-instance",
    "legend-token-missing", "legend-token-declared-twice",
    "consent-recorded-as-access", "evidence-ref-malformed",
)


def run_family(ctx):
    return FAMILIES[FAMILY](ctx)


def ctx_over(repos: list[str], agg_root=AGG_ROOT) -> Context:
    """A context over a SUBSET of the fixture repos.

    `make_ctx` always loads every repo directory under the family's fixture
    folder, and the nothing-to-compose skip is a statement about a corpus in
    which NO client is held by two or more domains — a shape the full corpus
    cannot express, because it deliberately holds four clients that are.
    """
    repo_paths = {name: FAMILY_FIXTURES / name for name in repos}
    docs, capabilities, change_ids = [], {}, {}
    for name, path in repo_paths.items():
        docs.extend(corpus.load_docs(name, path))
        capabilities[name] = corpus.spec_capabilities(path)
        change_ids[name] = corpus.change_ids(path)
    return Context(repo_paths=repo_paths, docs=docs, capabilities=capabilities,
                   change_ids=change_ids, git=FakeGit(),
                   thresholds=dict(DEFAULT_THRESHOLDS), as_of=AS_OF,
                   agg_root=agg_root, notebook_dryrun=lambda: None)


def findings() -> list[Finding]:
    got = run_family(make_ctx(FAMILY, agg_root=AGG_ROOT))
    assert isinstance(got, list), f"the family skipped instead of running: {got}"
    return got


def rules_for(client_marker: str) -> list[Finding]:
    return [f for f in findings() if client_marker in f.path]


# --------------------------------------------------------------------------
# the two finding classes
# --------------------------------------------------------------------------

def test_shared_identity_material_fires_on_the_same_identity_ref():
    """Disjunct (i). The finding names BOTH domains, because a shared identity
    is a fact about a pair and naming one of them would leave the reader
    hunting for the other."""
    got = [f for f in findings() if "client-shared" in f.path]
    assert len(got) == 1, got
    finding = got[0]
    assert finding.family == FAMILY
    assert "[shared-identity-material]" in finding.rule
    assert "identity_ref" in finding.rule and "shared-bc-observer" in finding.rule
    assert "alphaxfactory" in finding.rule and "betaxfactory" in finding.rule


def test_shared_identity_material_fires_on_an_equal_provider_object_ref_alone():
    """Disjunct (ii), the ONLY probe of the second disjunct (gate ruling G4).
    The two entries spell the identity differently, so disjunct (i) cannot be
    what fired — the shared provider-native OBJECT identifier is."""
    gamma = FAMILY_FIXTURES / "gammaxFactory" / "credentials" / "client-identity-roster"
    delta = FAMILY_FIXTURES / "deltaxFactory" / "credentials" / "client-identity-roster"
    import yaml
    g = yaml.safe_load((gamma / "client-object.yaml").read_text())["entries"][0]
    d = yaml.safe_load((delta / "client-object.yaml").read_text())["entries"][0]
    assert g["identity_ref"] != d["identity_ref"], "the fixture must not share a name"
    assert g["provider_object_ref"] == d["provider_object_ref"]

    got = [f for f in findings() if "client-object" in f.path]
    assert len(got) == 1, got
    assert "[shared-identity-material]" in got[0].rule
    assert "provider_object_ref" in got[0].rule
    assert "gammaxfactory" in got[0].rule and "deltaxfactory" in got[0].rule


def test_the_second_disjunct_does_not_fire_when_either_entry_omits_the_field():
    """An ABSENT declaration is not evidence of sharing. The shared-identity
    fixtures both declare it; the pair that declares it on one side only must
    stay clean, which is what the client-shared/client-separate corpus already
    proves — asserted here directly so the posture is measured, not inferred."""
    ctx = make_ctx(FAMILY, agg_root=AGG_ROOT)
    published = {}
    import yaml
    for repo, path in sorted(ctx.repo_paths.items()):
        for frag in sorted((path / "credentials" / "client-identity-roster").glob("*.yaml")):
            doc = yaml.safe_load(frag.read_text())
            for entry in doc["entries"]:
                published.setdefault(doc["client_ref"], []).append(entry)
    shared = published["client-shared"]
    assert all("provider_object_ref" not in e for e in shared), \
        "client-shared must probe disjunct (i) ALONE"
    assert len([f for f in findings() if "client-shared" in f.path]) == 1


def test_undeclared_cross_domain_reach_fires_and_names_both_sides():
    got = [f for f in findings() if "client-spanning" in f.path]
    assert len(got) == 1, got
    finding = got[0]
    assert "[undeclared-cross-domain-reach]" in finding.rule
    assert "exchange" in finding.rule
    assert finding.repo == "alphaxFactory", "the reaching domain owns the finding"
    assert "betaxfactory" in finding.rule, "the domain that DOES publish the entry"


def test_reach_requires_another_domain_to_declare_the_surface():
    """The second conjunct, measured by its absence: gamma's solo client
    publishes only business_central and nothing reaches anywhere else, so no
    reach finding exists for it. Reach into a surface NO domain declares is the
    intra-repo rule's business, not this family's."""
    assert not [f for f in findings() if "client-solo" in f.path]


# --------------------------------------------------------------------------
# FR-024 — the ratified non-finding
# --------------------------------------------------------------------------

def test_two_domains_with_separate_identities_on_one_surface_is_not_a_finding():
    """FR-024, at EVERY level: not a finding of either class, at any severity.
    The two entries sit in ONE client tenant on ONE surface at ONE authority
    class, which is exactly the collocation the rule must not be keyed on —
    keyed on the tenant it would fire here, and the ratified delta requires
    this pair to stay clean."""
    import yaml
    alpha = yaml.safe_load(
        (FAMILY_FIXTURES / "alphaxFactory" / "credentials" /
         "client-identity-roster" / "client-separate.yaml").read_text())
    beta = yaml.safe_load(
        (FAMILY_FIXTURES / "betaxFactory" / "credentials" /
         "client-identity-roster" / "client-separate.yaml").read_text())
    a, b = alpha["entries"][0], beta["entries"][0]
    assert alpha["client_tenant"] == beta["client_tenant"], "one client tenant"
    assert a["principal_locations"] == b["principal_locations"], "one tenant, again"
    assert a["admission_surface"] == b["admission_surface"]
    assert a["authority_class_achieved"] == b["authority_class_achieved"]
    assert a["identity_ref"] != b["identity_ref"]
    assert a["provider_object_ref"] != b["provider_object_ref"]

    assert not [f for f in findings() if "client-separate" in f.path]


# --------------------------------------------------------------------------
# the two skips — both EXPLICIT, never silence
# --------------------------------------------------------------------------

def test_single_repo_run_skips_with_a_reason():
    """`agg_root=None` is passed EXPLICITLY. Relying on the conftest default
    would make this test indistinguishable from one that forgot."""
    got = run_family(make_ctx(FAMILY, agg_root=None))
    assert isinstance(got, Skip)
    assert got.family == FAMILY
    assert "single-repo run" in got.reason


def test_a_corpus_with_nothing_to_compose_skips_with_a_reason():
    got = run_family(ctx_over(["gammaxFactory"]))
    assert isinstance(got, Skip)
    assert "no client is held by two or more domains" in got.reason


def test_a_mixed_corpus_reports_rather_than_skipping():
    """The skip is CORPUS-level, not per-client. A corpus holding both a
    single-fragment client and a composable one must REPORT — skipping would
    suppress real findings because some other client happened to be alone."""
    got = run_family(ctx_over(["gammaxFactory", "deltaxFactory"]))
    assert isinstance(got, list) and got, got
    assert all("client-object" in f.path for f in got), \
        "client-solo contributes nothing and is not a finding"


# --------------------------------------------------------------------------
# FR-023 / SC-009 — no intra-repo rule is duplicated here
# --------------------------------------------------------------------------

def test_no_intra_repo_finding_code_appears_in_this_familys_output():
    text = " ".join(f.rule + " " + f.action for f in findings())
    for code in INTRA_REPO_CODES:
        assert code not in text, f"intra-repo code {code!r} leaked into the report"


def test_the_family_adds_no_finding_to_another_familys_fixtures():
    """The sixteenth family must not become a sixteenth source of noise over
    corpora that were green before it existed. No other fixture repo publishes
    a roster fragment, so the family has nothing to compose and says so."""
    for other in ("tag-hygiene", "location-conformance", "status-validity"):
        got = run_family(make_ctx(other, agg_root=FIXTURES / other))
        assert isinstance(got, Skip), got
        assert "nothing to compose" in got.reason


def test_the_family_takes_no_blanket_resolution_entry():
    """FR-023: a `FAMILY_RESOLUTION` row assigns ONE class per family, and this
    family needs mixed classes."""
    from doc_health.families import FAMILY_RESOLUTION
    assert FAMILY not in FAMILY_RESOLUTION


# --------------------------------------------------------------------------
# US5 acceptance scenario 5 — the resolution class
# --------------------------------------------------------------------------

def test_a_finding_contradicting_a_ratified_capability_is_contested():
    """The reach is carried by a `declared_excess`: breadth declared as
    provider-forced, bound to a gate obligation that resolves, tested, and held
    under the entry's `ratified_by` capability. Curing the finding reverses a
    ratified fact, so it is contested rather than auto-fixable."""
    got = [f for f in findings() if "client-spanning" in f.path]
    assert [f.resolution for f in got] == [CONTESTED]


def test_a_finding_that_contradicts_no_ratified_capability_keeps_the_default():
    """`ratified_by` ratifies an identity's authority, never a SHARING
    arrangement between domains — the cure is for one domain to hold its own
    identity, which no ratification forbids."""
    got = [f for f in findings()
           if "client-shared" in f.path or "client-object" in f.path]
    assert len(got) == 2, got
    assert {f.resolution for f in got} == {AUTO_FIXABLE}


def test_the_family_produces_both_resolution_classes():
    """Stated as its own assertion: a family that only ever produced one class
    would satisfy each test above and still contradict FR-023's reason for
    keeping it out of the blanket registry."""
    assert {f.resolution for f in findings()} == {AUTO_FIXABLE, CONTESTED}


# --------------------------------------------------------------------------
# SC-011 — determinism, over a context that actually ran
# --------------------------------------------------------------------------

def test_determinism_identical_runs():
    a = run_family(make_ctx(FAMILY, agg_root=AGG_ROOT))
    b = run_family(make_ctx(FAMILY, agg_root=AGG_ROOT))
    assert isinstance(a, list) and a, "a vacuous skip would satisfy this trivially"
    assert [f.__dict__ for f in sorted(a, key=Finding.sort_key)] == \
           [f.__dict__ for f in sorted(b, key=Finding.sort_key)]


# --------------------------------------------------------------------------
# registration — the family renders a report section
# --------------------------------------------------------------------------

def test_the_family_is_registered_and_renders_a_report_section():
    from doc_health import FAMILY_IDS
    from doc_health import report
    assert FAMILY in FAMILIES
    assert FAMILY in FAMILY_IDS
    got = findings()
    text = report.render(AS_OF, got, [], [], [], 0, [], [])
    assert f"### {FAMILY}" in text
    assert all(f"— {f.rule}" in text or f.path in text for f in got)


# --------------------------------------------------------------------------
# 6.7 / ruling A-N4 — SC-006 across BOTH corpora
# --------------------------------------------------------------------------

@pytest.mark.parametrize("repo", sorted(p.name for p in FAMILY_FIXTURES.iterdir()
                                        if p.is_dir()))
def test_every_cross_domain_fixture_repo_passes_the_blocking_domain_gate(repo):
    """Without this, the "leaves the domain gate exit unchanged" half of SC-006
    is an assertion about a corpus nothing measured. With it, the shared
    identity is proven intra-repo CONFORMANT and the composition finding proven
    composition-only: the same fragments that raise a cross-domain finding here
    exit 0 under the blocking canonical validator."""
    result = subprocess.run(
        [sys.executable, str(ROSTER_VALIDATOR), str(FAMILY_FIXTURES / repo)],
        capture_output=True, text=True)
    assert result.returncode == 0, result.stdout
