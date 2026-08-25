# Clarifications: add-wallet-carried-review-authority

**NOTED-class constraints.** Everything here is REAL and VERIFIED, and none of
it is proposal-level: these are scale, lookup-path, tooling and operational
constraints that the design must carry and that the S-work will hit. Findings
that changed the proposal's argument are in `proposal.md` § The council's
disposition ledger; findings that shaped a decision are in `design.md`
§ Decisions. This file holds the rest, so none of it is lost between
ratification and build.

Each note records: the constraint, how it was established, why it is not
proposal-level, and which build item consumes it.

---

## N1 — The scale question is answered by absence: there is no store to index

**Constraint.** `contracts/openxwallet/openxwallet-distinct-holder-constraint.schema.yaml`
fixes the comparison basis as "the PRIOR ACT'S RECORDED HOLDER — what the
exercise record for that act actually carries". Enforcing a distinct-holder
constraint therefore needs a queryable exercise-record store keyed by
(object, act). **None exists.** So at many holders × targets × grants there is
no lookup path, no index, no cache, and nothing to invalidate — **because there
is no store.**

**Source.** Systems architect, concern 3 (verified against the schema).

**Not proposal-level.** The proposal only needs to stop claiming
`distinct_holder_constraint_refs` is already the observable that supersedes
QA 4.2; it now says so, conditioned on S3. The index/cache/invalidations
question is a real design question the moment a store exists, and it is
premature before then.

**Consumed by.** S3 (which creates the first exercise records) and S3's
successor that makes distinct-holder enforceable.

## N2 — At the MVP shape the lookup question does not arise, and that is deliberate

**Constraint.** S4's first register is one file, one holder, one target, one act,
one `expires_at`, one row. There is no lookup path to design because there is one
row to read. Every scale property — indexing, caching, invalidation, per-target
sharding, cross-repo resolution — arrives with the FIRST successor that widens
any of those axes, and each should be costed at that point rather than now.

**Not proposal-level.** The MVP shape is normative in the proposal; the scale
plan for shapes that do not exist is not.

**Consumed by.** Any successor widening the MVP.

## N3 — openxFactory has NO pull-request-triggered workflow today

**Constraint, verified.** `.github/workflows/` contains exactly two files.
`doc-health-reusable.yml` is `on: workflow_call` (a reusable suite the
aggregation repo's nightly calls); `session-open-pr.yml` is
`on: workflow_dispatch`. A repository-wide grep for `pull_request` as a trigger
returns nothing — the only occurrence is inside a comment about
`pull_request_target`. **So S1 is not "add a step to an existing PR check": it
creates openxFactory's FIRST pull-request-triggered workflow.**

**Not proposal-level.** It does not change what the proposal claims — the
adversary's point stands either way ("the validator runs in NO workflow") — but
it changes S1's size from a one-line addition to a new workflow with its own
permissions, concurrency and trigger design.

**Consumed by.** S1.

## N4 — The validator's runtime dependencies and the house CI pattern

**Constraint, verified.** `scripts/validate-openxwallet.py` (1466 lines) does
`import yaml` inside a guarded block that exits 2 when PyYAML is absent, so
**PyYAML is a hard prerequisite.** openxFactory carries no `requirements.txt`,
no `pyproject.toml` and no venv in the tree; the established house pattern in
`doc-health-reusable.yml` is `actions/setup-python@v5` pinned to `3.12`
followed by `pip install pyyaml`, invoked as `python3 <script>` from the
checkout root. S1 should follow that pattern rather than introduce a dependency
manager for one script.

**Not proposal-level.** Pure tooling mechanics.

**Consumed by.** S1.

## N5 — The validator self-tests when given no path: a vacuous-pass trap

**Constraint, verified.** `main()` takes `path` as `nargs="?"` with
`default=None` and the help text says "omit to self-test only". A CI step
invoking `python3 scripts/validate-openxwallet.py` with no argument would pass
green while scanning **no repository artifacts at all** — a green check that
checks nothing, which is precisely the class of failure this change exists to
name. S1's step MUST pass the checkout path, and S1's gate is a deliberately
malformed grant that fails the PR, not the presence of the step.

There is a second knob: `--strict` "treat warnings as errors". S1 must decide
whether the gate runs strict; the doc-health precedent parameterizes `fail-on`
rather than hard-coding it.

**Not proposal-level.** An implementation trap, but a load-bearing one.

**Consumed by.** S1.

## N6 — "Required check" is a repository setting, not a tree fact

**Constraint.** Whether a workflow is a REQUIRED check lives in the GitHub
ruleset, not in the checkout. A merged workflow file is therefore not evidence
that S1 is done. S1's realization evidence must include the ruleset state (e.g.
`gh api` output for the branch ruleset showing the check as required), and the
act of making it required is the operator's.

**Not proposal-level.** The proposal's requirement — "no grant is operative
until a named validator reads it in a required check" — is already written; this
is how it is evidenced.

**Consumed by.** S1, as an `[OPERATOR]` task with its own evidence artifact.

## N7 — `repo_scan` builds its context from the scanned repository's own records

**Constraint, verified.** `repo_scan` assembles the validation context out of
the records found in the scanned tree — a corpus closed over itself. Scanning
openxFactory validates openxFactory's own example artifacts against each other.
For the register this matters twice: (a) the scan target must include the
register path AND the wallet records its rows reference; (b) **a grant whose
audience wallet lives in a different repository has no resolution path today**,
so the MVP's single holder must have its wallet record in the same tree as the
register, or the ceiling check silently has nothing to resolve against.

**Not proposal-level.** It constrains where the first wallet record is written,
which is a build decision.

**Consumed by.** S1, the first-wallet step, and S4.

## N8 — `state` is a stored field and nothing recomputes it

**Constraint, verified.** `expires_at` is REQUIRED and `state` is a field inside
the grant record under `state: [active, expired, revoked]`. Nothing in the
family recomputes `state` from `expires_at`. A grant that expired an hour ago is
a file still reading `state: active`.

**Design consequence.** The register's validator must COMPUTE expiry from
`expires_at` at read time and treat a stale `state` field as a finding, not as
truth. The intake spec already requires this at exercise; the validator should
enforce the same at scan time so the two do not disagree.

**Not proposal-level.** A validator rule.

**Consumed by.** S4's validator, S5's exercise check.

## N9 — Where exercise records live is undecided, and both homes have costs

**Constraint.** S3 writes an exercise record at verdict conformance inside the
Hermes runtime. Two homes are available and neither is chosen here: the runtime's
Postgres (queryable, live, satisfies N1's store requirement, but the record then
lives outside any governed git corpus and its retention is an ops concern), or a
git artifact in the governed tree (auditable and diffable, but not queryable and
subject to the same pinning lag that disqualifies a file-based revocation
surface — see `design.md` D5).

**Not proposal-level.** The proposal requires an exercise record and names where
it is WRITTEN; where it is STORED is S3's design.

**Consumed by.** S3.

## N10 — The composition component set needs a concrete mapping to seat artifacts

**Constraint.** `openxwallet-agent-profile` names six declared components — model
version, prompt contract, tool manifest, policy version, parameters, retrieval
corpus. codexFactory's seats are defined across `hermes/domain/review-councils/`
and `hermes/domain/agent-mixes.yaml`. **No mapping exists** from those artifacts
to the six component slots, and S5's pinning requirement is unimplementable
without one. In particular the retrieval corpus slot must be filled by the
PINNED seat prompt plus ontology package — never the candidate repository at
HEAD, which the intake spec forbids because every candidate commit would revoke
the reviewer.

**Not proposal-level.** The proposal states the pinning rule; the mapping is
build work.

**Consumed by.** S5, and the first-wallet step (a wallet needs its composition
declared before a grant can name it).

## N11 — The holder count is approximate and must be re-derived at build time

**Constraint.** The ~8 figure in ## Cold start is derived from codexFactory's
`gate-rules.yaml` and `merge-readiness.yaml` as they stood 2026-08-22: roughly
six distinct seats (`company-policy-lead`, the intent-owner role slot,
`lead-quality`, `lead-security`, `lead-integration`, plus the conditional CSC
seat) plus the two councils as bodies. Council composition changes; the number is
an order-of-magnitude statement, not an inventory.

**Not proposal-level.** The proposal uses it to size the cold-start cost, which
is what it is for.

**Consumed by.** The first-wallet step and S4's successors.

## N12 — The house already has the notification shape Q8 asks for

**Constraint.** Q8's third limb asks who tells the operator the register emptied.
The Human Escalation Contract already defines the mechanism:
`docs/roles-and-authority.md:124-140` — decisions requiring human authority
PARK, never interrupt, and are delivered as a decision-ready packet ("situation
summary, at most three options with exactly one recommendation, evidence
references, and the consequence of each option and of deciding nothing"), with
packets deduplicating by root cause and silence fail-closed. A mass revocation is
squarely a parked decision — the list names "privileged capability grants"
explicitly. So the answer to Q8's third limb is likely "a parked packet", and the
open part is what raises it, not what shape it takes.

**Not proposal-level.** Q8 is posed with exits in the proposal; this note records
that the house's answer to the shape question already exists so the exit is not
re-invented.

**Consumed by.** Q8's resolution and S5's runbook.

## N13 — `holder_readable` is the only realistic custody model, and `act` is the tier it was designed for

**Constraint, verified.** `openxwallet-custody.registry.yaml:53-58`, on
`holder_readable`: "This tier reaches `act` deliberately. Capping software
custody lower would stall every consumer… there is no key infrastructure in the
stack today. **Approval before apply is the compensating control at this tier.**"
The MVP's tier is `act`, whose definition is "Complete an effecting act, with
approval required before apply." So the MVP sits exactly where the registry
intended a no-key-infrastructure consumer to sit, and the compensating control is
already in force by the constitutional floor.

**Not proposal-level.** It is reassurance about a choice the proposal already
makes, not a change to it — but it is worth recording so the choice is not
re-litigated as a compromise.

**Consumed by.** The first-wallet step; S4.

## N14 — The cross-repository deploy constraint gates any S-work touching live materialized content

**Constraint.** codexFactory `dcfbd96` (complete eight-kind content manifest plus
completeness guard) and hermes-install `3de0519` (runtime learns
`domain_ontology` plus schema-parity guard) are landed on `origin/main` in both
repositories. codexFactory `3143f34`
(`hermes/domain/review-councils/records/2026-08-23-reseed-deploy-ordering-addendum.md`)
records the constraint: **no reseed until a hermes-install image at `3de0519`+ is
deployed** — the repository state is safe in every order since `dcfbd96`, the
deployed state is not until the image ships.

**Not proposal-level.** The proposal cites the fix as landed evidence; the deploy
ordering is an execution constraint on the S-work.

**Consumed by.** S3 and S5 (both run against the live runtime), and any S4 gate
that exercises a real convening.

## N15 — Front-matter spelling: `target_release: implemented`

**Constraint.** `release-realization:6-12` admits `implemented` or a named
release. This change declares `implemented` (the doc-only pair; no contract
bundle is cut), matching ~70 archived changes and the ratified sibling.
The QA lead recorded the corpus-wide condition around this field as clean and
not this change's defect; it is noted here so it is not re-raised.

**Consumed by.** Archive bookkeeping.
