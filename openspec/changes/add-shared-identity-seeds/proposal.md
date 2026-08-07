---
code_surface: openxFactory (doc_health.shared_identity detector + deterministic seed drafter; dashboard serve drafting route; the repository lens's seed affordance and panel; tests)
target_release: none
Status: ratified
Ratified by: Brett's "yes, lets start that now" on 2026-08-07, accepting the successor named at the close of `add-repository-lens` — exporting a convergent lens region into the domain-neutralization candidate register
---

# Proposal: add-shared-identity-seeds

## Why

The promotion process names four ways a DTN candidate is born
(`docs/domain-to-neutral-promotion-process.md`, "Candidate Rule") and the
FIRST has never been implemented:

> Two or more domain repos use the same structure with different domain nouns.

The neutrality-drift lane's four stage-1 signals ask adjacent questions —
`near_duplicate` compares a domain file against the openxFactory tree,
`cross_repo_consumer` looks for references, `lexicon_absence` and
`uninventoried_tooling` read one repository at a time. None of them asks
whether two DOMAIN repositories carry the same thing, so that rule has been
served by manual search passes only.

The dashboard now computes exactly that. The repository lens (D21) plots
every document identity by CARRIER COUNT across a project's members, and
ring 2 and inward IS the rule's population. On the real five-factory
`domains` project that is four identities, including `docs/credentialing.md`
in three factories — findings the register has no automated path to.

## What Changes

- ADD `doc_health/shared_identity.py`: the deterministic detector (identities
  carried by two or more of a named repository set, optionally narrowed to an
  exact carrier combination — a lens region) and a seed drafter that emits the
  register's own row + `### DTN-NNN:` detail section, numbered from the
  register so a drafted-but-unmerged gap never collides.
- ADD a loopback DRAFTING route on the dashboard serve. It recomputes the
  carriers from the serve's own composed view — the client names the project,
  the visible set, and the region's combination, never the evidence — and
  returns TEXT.
- ADD the affordance to the repository lens's drill-in pane: a convergent
  region (two or more carriers) can be drafted; a single-carrier region cannot
  and says why. The drafted seed renders read-only with a copy control.

## Impact

SEED-FIRST, NEVER A WRITE — the same discipline the neutrality lane already
records: the register is never opened for writing, and a candidate enters the
lifecycle only when a human merges the seed. That is what makes the affordance
legitimate on a composed, READ-ONLY view: nothing is written, so no gate
capability is claimed and D10's read-only rule is untouched.

No contract growth: no schema, no gate verb, no gate-action record. The seed
is drafted deterministically — the carrier set is a fact about the pinned
trees, so the same corpus state drafts a byte-identical seed.

Named successor: promoting this detector to a FIFTH stage-1 signal in the
neutrality-drift lane, so the nightly run files these seeds without a human
opening the dashboard. This change deliberately ships the human-driven path
first, because the lens is where the question is already being asked.
