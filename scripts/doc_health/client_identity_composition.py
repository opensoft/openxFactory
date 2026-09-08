"""The sixteenth deterministic family: client identity roster composition
(add-client-identity-roster; doc-health delta "Deterministic check families",
scenario "Roster composition is checked across domains").

CROSS-DOMAIN ONLY. This family assembles the per-client roster fragments that
each pinned domain repository publishes at
`credentials/client-identity-roster/` and reports exactly TWO concerns, both of
which are invisible inside any single repository:

1. **shared-identity-material** — two entries for one `client_ref`, published
   by DIFFERENT domains, naming the same identity MATERIAL. Keyed on material
   and on EXACTLY TWO DISJUNCTS (gate ruling G4): the same `identity_ref`, or
   an EQUAL `provider_object_ref` where BOTH entries declare it. The second
   disjunct is deliberately NOT read against `principal_locations[]`, which
   carries TENANT identifiers: read that way the rule would intersect on the
   shared client tenant, which two domains holding separate identities for one
   client necessarily share, and it would refuse the ratified non-finding
   below. An absent `provider_object_ref` is not evidence of sharing.
2. **undeclared-cross-domain-reach** — an admission act or a
   `declared_excess.spanned_surfaces` member in domain A's fragment achieves
   scope over an admission surface for which A publishes no entry, while
   another domain's fragment for the SAME client declares that surface.
   Composition is what makes it visible.

**THE RATIFIED NON-FINDING.** Two domains each holding their OWN separate
identity on one admission surface and authority class in one client tenant is
NOT a finding at any level — separate identities are what preserve
provider-side attribution and independent revocation. Neither class is keyed on
(surface, class) collocation, and neither is keyed on collocation in a tenant.

**NO INTRA-REPO RULE IS DUPLICATED HERE.** The uniqueness tuple, closed
vocabularies, verified admission, achieved-versus-intended authority, gate
obligations, residency, lifecycle, attestation, both roots and placement all
belong to `scripts/validate-client-identity-roster.py`, which is a BLOCKING
member of the domain-conformance-check pack. An intra-repo nonconformance fails
the owning domain's gate; it is not re-reported here as advice, and no
intra-repo finding code appears in this family's output.

**NO COMPLETENESS RULE.** Neither the absence of a fragment nor the absence of
an entry is a finding, and no code path here derives an expectation from any
inventory of a domain's credential needs. A domain that publishes nothing
contributes nothing.

**TWO EXPLICIT SKIPS, never silence.** `ctx.agg_root is None` (a single-repo
run has no aggregation checkout to compose across), and a corpus in which no
client is held by two or more domains (there is nothing to compose). The second
is CORPUS-level, not per-client: returning a skip because SOME client has one
fragment would suppress the findings of every client that qualifies, so a mixed
corpus reports.

**RESOLUTION CLASSES ARE PER FINDING** (the precedent of the three other late
families; this family takes no blanket `FAMILY_RESOLUTION` entry, which would
force one class onto both). A finding is CONTESTED when curing it would reverse
what a ratified capability the record NAMES authorizes:

  * `undeclared-cross-domain-reach` carried by a `declared_excess` is
    CONTESTED. That breadth is declared as provider-forced, bound to a gate
    obligation and an enforcement test, and held under the entry's
    `ratified_by` capability — resolving the finding means withdrawing a
    declared, ratified, gate-bound fact, not editing a record.
  * A reach carried only by an admission act the entry never declared as
    spanned takes the default: nothing ratifies it, and the cure is to declare
    the spanned surface or publish the entry.
  * `shared-identity-material` takes the default. `ratified_by` ratifies an
    identity's authority, never a SHARING arrangement between domains; the cure
    is for one domain to hold its own identity, which contradicts no ratified
    capability.

DETERMINISTIC AND NETWORK-FREE: filesystem reads only, every ordering sorted,
no clock, no model call, no subprocess. Identical inputs produce identical
findings.

One check this family deliberately does NOT implement (plan Cluster G, ruling
G2, where it is permitted and not required): two fragments for one client
declaring different `client_tenant` values. Nothing in this feature depends on
it and leaving it out is conformant.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

from . import AUTO_FIXABLE, CONTESTED, ERROR, Finding, Skip

FAMILY = "client-identity-composition"

# The contract's DECLARED PLACEMENT, as path parts relative to a domain repo.
# The glob is `*.y*ml`, not `*.yaml`: the blocking intra-repo pass accepts a
# `.yml` fragment, so a narrower glob here would leave the reporting pass blind
# to a file the gate had already checked.
PLACEMENT = ("credentials", "client-identity-roster")
PLACEMENT_DISPLAY = "credentials/client-identity-roster"
ROSTER_KIND = "xfactory_client_identity_roster"

SHARED_MATERIAL = "shared-identity-material"
CROSS_DOMAIN_REACH = "undeclared-cross-domain-reach"


@dataclass(frozen=True)
class Published:
    """One entry, with the fragment and repository that published it."""

    repo: str
    path: str
    domain: str
    client: str
    index: int
    entry: dict

    def sort_key(self) -> tuple:
        return (self.repo, self.path, self.index)

    def label(self) -> str:
        ref = _text(self.entry.get("identity_ref")) or f"entries[{self.index}]"
        return f"{self.domain} ({self.repo}:{self.path}) entry {ref!r}"


def _text(value) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _mapping(value) -> dict:
    return value if isinstance(value, dict) else {}


def _sequence(value) -> list:
    return value if isinstance(value, list) else []


def _load(path: Path):
    if yaml is None:  # pragma: no cover - the suite always has PyYAML
        return None
    try:
        with path.open(encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except (OSError, yaml.YAMLError):
        return None


def _published(ctx) -> list[Published]:
    """Every roster entry the pinned repositories publish, sorted.

    Reads ONLY the declared placement. A file that does not parse, does not
    carry the roster kind, or is not a mapping contributes nothing — placement
    and shape are the blocking pass's business, not this one's.
    """
    out: list[Published] = []
    for repo, repo_path in sorted(ctx.repo_paths.items()):
        root = Path(repo_path)
        placement = root.joinpath(*PLACEMENT)
        if not placement.is_dir():
            continue
        fragments = sorted(set(placement.glob("*.yaml"))
                           | set(placement.glob("*.yml")))
        for path in fragments:
            doc = _load(path)
            if not isinstance(doc, dict) or doc.get("kind") != ROSTER_KIND:
                continue
            client = _text(doc.get("client_ref"))
            domain = _text(doc.get("domain"))
            if not client or not domain:
                continue
            rel = path.relative_to(root).as_posix()
            for index, raw in enumerate(_sequence(doc.get("entries"))):
                if isinstance(raw, dict):
                    out.append(Published(repo, rel, domain, client, index, raw))
    return sorted(out, key=Published.sort_key)


def _shared_material(a: Published, b: Published) -> tuple[str, str] | None:
    """The two disjuncts, in order. `identity_ref` first, so a pair matching
    both is reported once and named by the stronger evidence."""
    ref_a, ref_b = _text(a.entry.get("identity_ref")), _text(b.entry.get("identity_ref"))
    if ref_a and ref_a == ref_b:
        return ("identity_ref", ref_a)
    obj_a = _text(a.entry.get("provider_object_ref"))
    obj_b = _text(b.entry.get("provider_object_ref"))
    if obj_a and obj_b and obj_a == obj_b:
        return ("provider_object_ref", obj_a)
    return None


def _reached_surfaces(pub: Published) -> dict[str, bool]:
    """Surface -> whether a `declared_excess.spanned_surfaces` member carries
    the reach. The flag is what the resolution class turns on."""
    reached: dict[str, bool] = {}
    for member in _sequence(_mapping(pub.entry.get("declared_excess"))
                            .get("spanned_surfaces")):
        name = _text(member)
        if name:
            reached[name] = True
    for act in _sequence(pub.entry.get("admission")):
        name = _text(_mapping(act).get("surface"))
        if name:
            reached.setdefault(name, False)
    return reached


def _shared_findings(published: list[Published]) -> list[Finding]:
    findings: list[Finding] = []
    for i, a in enumerate(published):
        for b in published[i + 1:]:
            if a.domain == b.domain:
                continue
            material = _shared_material(a, b)
            if material is None:
                continue
            field, value = material
            findings.append(Finding(
                ERROR, FAMILY, a.repo, a.path,
                f"[{SHARED_MATERIAL}] {a.label()} and {b.label()} name the "
                f"same identity material for client {a.client!r}: equal "
                f"{field} {value!r}. Two domains sharing one identity give up "
                f"provider-side attribution and independent revocation — "
                f"neither domain can be revoked without revoking the other.",
                f"give each domain its own identity in {a.client!r}, or record "
                f"the shared holding as a deliberate, cited arrangement"))
    return findings


def _reach_findings(published: list[Published]) -> list[Finding]:
    """A surface a domain reaches but publishes no entry for, which ANOTHER
    domain publishes an entry for. Both halves are required: the first alone is
    the intra-repo rule's business, and the second is what makes it composed."""
    own: dict[str, set[str]] = {}
    for pub in published:
        surface = _text(pub.entry.get("admission_surface"))
        if surface:
            own.setdefault(pub.domain, set()).add(surface)

    findings: list[Finding] = []
    for pub in published:
        for surface, declared in sorted(_reached_surfaces(pub).items()):
            if surface in own.get(pub.domain, set()):
                continue
            others = sorted({p.domain for p in published
                             if p.domain != pub.domain
                             and _text(p.entry.get("admission_surface")) == surface})
            if not others:
                continue
            findings.append(Finding(
                ERROR, FAMILY, pub.repo, pub.path,
                f"[{CROSS_DOMAIN_REACH}] {pub.label()} achieves scope over "
                f"admission surface {surface!r}, for which {pub.domain} "
                f"publishes no entry in client {pub.client!r}, while "
                f"{', '.join(others)} publishes one. The reach is carried by "
                f"{'a declared_excess' if declared else 'an admission act'} "
                f"and is visible only once the client's fragments are "
                f"composed.",
                "publish an entry for the reached surface, or narrow the reach "
                "to the surfaces this domain holds",
                resolution=CONTESTED if declared else AUTO_FIXABLE))
    return findings


def fam_client_identity_composition(ctx):
    if ctx.agg_root is None:
        return Skip(FAMILY, "single-repo run: no aggregation checkout")

    published = _published(ctx)
    domains_per_client: dict[str, set[str]] = {}
    for pub in published:
        domains_per_client.setdefault(pub.client, set()).add(pub.domain)
    composable = sorted(client for client, domains in domains_per_client.items()
                        if len(domains) >= 2)
    if not composable:
        return Skip(FAMILY, "no client is held by two or more domains: "
                            "nothing to compose")

    findings: list[Finding] = []
    for client in composable:
        held = [p for p in published if p.client == client]
        findings.extend(_shared_findings(held))
        findings.extend(_reach_findings(held))
    return sorted(findings, key=Finding.sort_key)
