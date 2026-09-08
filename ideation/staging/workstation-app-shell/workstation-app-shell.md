# Staged: Workstation App Shell — the local surface stops being a typed command

Status: staged
Kind: architecture
Summary: The workstation counterpart to
[mobile-dashboard-surface](../mobile-dashboard-surface/mobile-dashboard-surface.md):
an app on the engineer's own machine that OWNS the local dashboard serve —
its checkout binding, its actor identity, its console token, its port and
its lifecycle — instead of leaving them to a hand-typed `python3 -m` line
with four flags. The layer-shaped UI posture is NOT redecided here: the
ratified `avatar-first-ui` "Hermes-layer surface defaults" requirement
already says subject surfaces default avatar-first, tenant surfaces default
hybrid, and domain surfaces default conventional-with-copilot. What this
topic decides is the DELIVERY VEHICLE and, load-bearing, its BOUNDARY with
the Worker Host App: the same workstation would host both the agent workers
and the human console, and those two have opposite trust postures — the
worker exists to run agents, while the console's entire purpose is to be
distinguishable from one. They therefore run as SEPARATE OS PRINCIPALS in
one shell, with the console's token unreadable by the worker principal.
Also names the gap this conversation exposed: codexFactory has no subject
surface at all. Its subject layer is `Project Hermes`, and every feature a
project stakeholder needs maps onto a gate the funnel already has.
Topics: avatar-first-ui, doxbench, ideation-dashboard, client-surface, hermes-layers, worker-host, workstation, gate-console, two-plane, identity
Repository context: openxFactory owns the neutral surface standard
(`avatar-first-ui`, ratified) and this topic; the shell platform decision is
shared with the avatar-client track (private `openAvatar` repo);
codexFactory realizes the local-serve integration it wraps; the Worker Host
App lives in `Omnigent-Install` and owns the principal separation this topic
depends on; per-domain subject surfaces land in the DomainxFactory repos.
Staging ID: openxFactory:staging:workstation-app-shell
Source: team-004 session 2026-07-27 — Brett, walking through review finding
2's console-token posture, asked whether the local served page should run
from an app on the host machine, proposed that the Worker Host App double as
the dashboard with the avatar built in, and confirmed the layer analogy
(doctor/patient in Medx = engineer/project in codex; subject avatar-first,
tenant hybrid). Confirmed against the ratified `avatar-first-ui` requirement
and the ratified `layer-vocabulary` alias table, which already names
codexFactory's layers `Project Hermes` and `Engineering Organization
Hermes`.
Target capabilities: `avatar-first-ui` (realization evidence, possibly a
small ADDED requirement for the workstation shell); `ideation-dashboard`
(MODIFIED — the local serve becomes app-managed); a later per-domain subject
surface (name open; codexFactory first consumer)

## Claims

1. **The layer defaults are ratified — this topic realizes, never
   redecides.** `avatar-first-ui`'s "Hermes-layer surface defaults"
   requirement already mandates avatar-first for the served subject, hybrid
   for the tenant operator, and conventional-with-copilot for domain
   authority, each with its own scenario. Brett's 2026-07-27 framing
   ("avatar first for the subjects and hybrid for the tenant") restates that
   requirement; it is not new policy. Any DomainxFactory override must still
   identify the user set, workflow need, risk class, accessibility fallback
   and authority boundary, exactly as that requirement demands.
2. **The subject layer for codexFactory is the PROJECT, not the client
   company (DECIDED, and it has a design consequence).** The ratified
   `layer-vocabulary` alias table names codexFactory's layers `Project
   Hermes` (subject) and `Engineering Organization Hermes` (tenant), and
   `client` is a RESERVED term that must not name a Hermes layer. The human
   in front of the avatar is a person at the client company, but the layer
   serving them is the project. Consequence: a client company with three
   projects has THREE subject contexts, so consent, journey state and
   private memory are per-project. A design that builds one avatar identity
   per customer makes consent ambiguous across their projects.
3. **An app should own the local serve, and the motivating evidence is in
   the tree.** The local plane's powers (create, edit, commit gate actions,
   push, open a pull request) require a real checkout, a loopback bind, a
   resolved actor and — since review finding 2 — a per-serve console token.
   Today all of that is assembled by hand: `python3 -m
   ideation_dashboard.cli generate-and-open --repo-root … --repository …
   --actor … --port …`. The T092 runbook's literal first command OMITTED two
   required flags and exited 2 (found 2026-07-27 by the second adversarial
   review, verified by re-running it). A human retyping a four-flag module
   invocation IS the defect; an app makes it a button and owns the token
   lifecycle the human should never see.
4. **The Worker Host App and the human console have OPPOSITE trust
   postures, and bundling them changes the accepted risk (DECIDED that they
   separate; HOW is claim 5).** Brett accepted review finding 2's residual
   on 2026-07-27: a process running as the identified human, on the human's
   machine, can read the console token from `/capabilities` (or set
   `XF_HUMAN_CONSOLE=1`) and act as the human — the console test is an
   anti-CSRF control, not authentication. That residual was accepted for a
   world where agent workers live ELSEWHERE. An app that hosts both the
   workers and the console makes agent co-residency the ARCHITECTURE rather
   than an edge case. The idea survives; the design must say so out loud.
5. **The separation mechanism already exists and must be used.** The Worker
   Host App's `worker_identities` step (merged, step 3/7, module 0.4.0)
   established per-worker identities with escrow-before-account, rotate-
   don't-read, and redaction by construction. The shell therefore runs the
   console and the workers as DIFFERENT OS principals, and the console's
   token, port binding and actor identity are unreadable by the worker
   principal. A single-principal shell would silently convert an accepted
   residual into a real exposure.
6. **One shell, two planes, never crossing.** Brett's 2026-07-25 two-plane
   decision stands: the dev-plane dashboard reads git checkouts and has no
   data path to a running install's content. If one app carries both the
   engineer's dev dashboard and a tenant's runtime surface, the planes stay
   separate systems inside it — packaging must not become the thing that
   violates the ruling. The `(repository, ref)` snapshot-source seam from
   [dashboard-repo-selector](../dashboard-repo-selector/dashboard-repo-selector.md)
   is the binding point: the runtime plane binds its own source, and a
   session ref is never published.
7. **The engineer's hybrid surface is largely already shipped.** The
   ideation dashboard IS the tenant-layer hybrid surface — wheel, funnel,
   staged workbench, gate console, health. The missing piece is doxBench's
   integrated editor/chat surface (historically Track C). Nothing in this topic
   asks for a new tenant UI; it asks for a host for the one that exists.
8. **codexFactory's subject surface is undefined, and its feature set maps
   onto gates the funnel already has.** MedxFactory has the pattern
   (avatar patient intake, shipped as the client-lab carveout);
   codexFactory has nothing subject-facing. The mapping, so the avatar is a
   subject-facing RENDERER over existing gates rather than a second system:
   intake of a want → a brainstorm/possible carrying subject-requested
   provenance (`add-proposal-origin-contract` already supplies the
   provenance shape); status → narrated position in the funnel (staged,
   proposed, merged, deployed); decision moments → scope approval, schedule
   or cost acknowledgment, delivery acceptance, each a recorded gate action
   structurally identical to `ratify`; demonstration → the avatar showing
   what was built (the avatar demo-enablement carveout is precedent).
9. **Subject visibility is a confinement problem already solved one layer
   down.** A project stakeholder must not see other projects, the
   engineering organization's internal deliberation, or unmerged
   exploration. That last rule is exactly the ratified
   `add-workbench-branch-sessions` posture — branch drafts are visible ONLY
   inside the session, `main` is the shared truth — applied one layer up.
   Reuse the rule; do not invent a second visibility model.
10. **Sequencing: do not couple two mid-flight programs to get one app.**
    The Worker Host App is at step 4/7 (`runner_services`) with benches
    unbuilt, and its remaining steps are substrate work with no UI content.
    The dashboard's runtime plane is unstarted (repo-selector is only the
    dev-plane step). Recommended order: finish the worker host AS A HOST;
    ship the app shell owning the local serve (which retires the typed-command
    defect class); and let each domain's subject surface be its own change,
    because the shell is neutral while the features are domain-specific.
    MedxFactory will teach the subject pattern more cheaply than
    codexFactory's project stakeholder will.


11. **The console carries a COMPUTE SHARE VALVE, scoped to the TEMP/VOLUNTEER
    ESTATE ONLY (DECIDED 2026-07-27).** An engineer works in the console AND
    volunteers the same workstation as a worker, whose dispatched jobs may
    belong to other projects entirely — the worker half just shares compute.
    The console therefore offers a valve: share while doing light work, and
    recover the machine when the work gets intense. Brett scoped it to the
    temp estate, which is what makes it coherent with the Worker Host App
    program rather than a reversal of it: that program moves PRODUCTION
    riders off personal machines onto dedicated Cloud PCs, while enrollment
    rule R8 already REFUSES AND AUDITS any attempt to bind a volunteer
    lease into a standing execution-lane runner group
    (`add-worker-enrollment-broker` spec, "a volunteer lease MUST NOT be
    bound into a standing execution-lane runner group"). Volunteered
    workstation compute is a separate, non-standing pool; production work
    still goes to the CPC fleet. The estate coupling is already contracted
    and bidirectional: `estate: temp` ⟺ `subject.class: engineer` ⟺
    `host.managed: false` ⟺ `trust_tier: volunteered_hardware`, with
    `host_class: service_rider` already meaning "pilot riders on a person's
    machine".
12. **SLOTS are the unit, and they already exist end to end — the valve
    invents no new unit of account.** `max_concurrent_jobs` and
    `current_jobs` are columns in the operational Postgres schema, fields on
    the live worker registry, per-lane declarations, and are enforced by the
    dispatcher; a three-level vocabulary (`normal_capacity` /
    `max_concurrent_jobs` / `upper_bound`) is already validated against the
    deployed environment. There is NO resource field — cpu, memory, share —
    anywhere in the host manifest, bench manifest, worker profiles, lease
    family or job envelope, and in the host manifest it is not merely absent
    but unrepresentable (`additionalProperties: false`). A PERCENTAGE is
    therefore schedulable nowhere: whole jobs go to whole runners by label,
    and the only quantity any gate reads is an integer job count. The
    percentage lives in the console's RECOMMENDATION TEXT and nowhere else.
13. **DRAIN ONLY (DECIDED 2026-07-27) — the valve never touches running
    work.** "Accept no more, let in-flight jobs finish" is nearly free: the
    dispatcher already skips any worker whose status is not
    `available`/`idle` (proven by an existing capacity smoke test), the
    lease-renewal response already carries a `required_action: stop`, and the
    per-runner `sc.exe stop` + `start= demand` pair with its exact inverse is
    already designed (broker-integration design, task 3.5, unbuilt). EVICTION
    is explicitly NOT funded: there is no job lease, no attempt counter, no
    idempotency or resumability contract, no reassign path and no destination
    host — and `current_jobs` decrements only on completion, so an abandoned
    job would consume its slot FOREVER. The valve's user-visible promise is a
    drain countdown bounded by the existing job timeout, never migration.
    Precedent for the doctrine already exists in code: the heartbeat step
    rebinds a runner's logon WITHOUT restarting it, because a restart "would
    kill a job this step had no business ending".
14. **A day-one DEFECT must be fixed before the valve is built.**
    `release_worker_job()` recomputes worker status unconditionally as
    available-or-busy from the slot count, and `assign_worker_job()` only ever
    writes busy or preserves — neither respects operator intent. So a drain
    expressed on `worker.status` is SILENTLY REVERTED by the next finishing
    job. Operator intent must survive job churn before anything else is
    built. Related: the valve is modelled as an ORTHOGONAL WORKER CONDITION
    with an `observed_at`, a `policy_ref` and clearing evidence — the corpus's
    own ratified modelling rule — not as a job state, not as a runner label,
    and not as a new lease state (the lease's state reasons are all about
    AUTHORITY, not capacity).
15. **The valve is DESIRED STATE, because reconcile repairs everything else —
    and a hand-stop is worse than merely undone.** A stopped-but-present
    runner service sets both `needs_rebind` and `needs_restart`, and
    `needs_rebind` plans a FULL ACCOUNT PASSWORD ROTATION (escrow a fresh
    password, reset the local account, rebind the service logon and the
    heartbeat task, rewrite the sidecars) before restarting. So the valve is
    expressed as an additive per-worker `desired_state: active | paused` on
    the broker-served temp manifest, plus an app-owned ProgramData intent
    sidecar that reconcile READS instead of repairing, explicitly bounded so
    it can NEVER override a lease `required_action: stop` (the renewal
    contract states that no local flag, retry or configuration edit on the
    host may override that decision). Reconcile is triggered ON DEMAND
    (`AllowStartOnDemand` is already true) so the valve does not wait out the
    hourly pass, and `paused` is realized only once the runner reports idle.
    Reconcile also needs a PRUNE path: it iterates only declared workers, so
    shrinking the set today would leave a runner service running and
    registered but unmanaged.
16. **Signalling joins the ALREADY-QUEUED heartbeat delta rather than opening
    a parallel path.** Today `unavailable` means "something is broken" — it is
    derived solely from service health — so operator intent has no spelling.
    The valve adds `draining` to the readiness statuses, projects
    `max_concurrent_jobs` into the sanitized read view (it is currently not
    projected at all), and relaxes the lane gate from a hard
    `current_jobs == 0` to a slot comparison. Per the broker change's D10 this
    lands in publisher, service and evaluator TOGETHER with a parity test —
    the valve rides that delta instead of growing the heartbeat contract
    twice.
17. **"Local work first" in v1 is ADMISSION CONTROL BY JOB CLASS, not a
    scheduler weight.** A low always-on cgroup weight would be the right
    mechanism — it reacts within one scheduler tick, cannot oscillate, needs
    no telemetry — but it is impossible today: the runner is a WINDOWS
    process, not a container, so there is no shared scheduling domain to
    weight within, and no resource governor exists anywhere in either install
    (no `--cpus`/`--memory`, no cgroup writes, no `.wslconfig` management).
    The existing expression of the same intent is lane admission: coder lanes
    are already forbidden full builds, full test suites, Compose stacks and
    browser E2E, while tester lanes own heavy validation at capacity 1-2.
    MEMORY is the asymmetry to respect regardless of mechanism: CPU yields to
    a weight change, RAM does not — a running container cannot hand memory
    back — so the never-shared memory reserve is a CONSTANT the engineer
    declares once and the recommender never tunes (its failure mode is the
    engineer's own build being OOM-killed).
18. **The recommender is read-only and advisory.** The console watches local
    usage over a window and SUGGESTS a slot count; it never adjusts silently.
    No host telemetry exists in the dashboard today — `/capabilities` reports
    action availability, not machine state — so this is entirely new console
    surface. Note for whoever builds it: the existing governance agents
    already own these concerns (HP owns `capacity_tradeoffs`, HD owns
    `worker_status` and `stuck_work_detection`), so whether the recommender is
    a delegated surface of those agents or a purely local advisory is open
    question 10.
19. **Today's only valve is global and binary.** `OMNIGENT_WORKER` is a single
    GitHub variable that turns self-hosted dispatch on or off for the whole
    factory, so an engineer wanting his machine back would close the window
    FOR EVERYONE. That is the status quo this claim replaces, and it is worth
    stating because it makes even a two-position per-host valve a strict
    improvement.

## Open questions

1. **Shell platform.** The mobile sibling already carries a "shell platform
   vs the frozen AVC ports" fork; the workstation shell either shares that
   decision or diverges. Recommendation: share it — one client codebase with
   a desktop target beats two shells, and the avatar client already exists.
   Blocks nothing until the shell is built.
2. **One app or two on the workstation?** Claim 5 requires two principals;
   it does NOT settle whether that is one installer presenting two services
   or two separately installed apps. Recommendation: one installer, two
   services, two principals — the human should not have to install twice to
   get a console and a worker, but the OS must still see two identities.
3. **Does the shell hold the console token, or mint per-launch?**
   Recommendation: never persist it. The serve already mints a fresh token
   per start precisely so a token cannot outlive its console; the shell
   should hold it in memory for the page it launched and let it die with the
   process.
4. **Which layer does an engineer's own workstation app default to?** An
   engineer is tenant-layer, so hybrid — but the same engineer may need a
   subject-layer preview to see what a stakeholder sees. Recommendation: the
   layer follows the SIGNED-IN identity (the mobile topic's rule), with
   subject preview an explicit, labelled mode that reads only what the
   subject may see, never a second data path.
5. **Where does the codexFactory subject surface live?** The feature set is
   codex-domain content, but the standard is neutral. Recommendation: the
   neutral surface standard stays in openxFactory, the codex subject feature
   set stages in codexFactory as its own topic, first consumer of a later
   ADDED runtime capability.

6. **H11 — does a temp/volunteer worker get a heartbeat write token?** Still
   open on Brett's own gate in the broker-integration change. If it does not,
   a volunteered workstation cannot publish readiness at all and the valve
   needs a signalling path that is not the heartbeat. This is the one open
   question that can invalidate claim 16's mechanism outright.
7. **Does the valve get more than one slot?** D5 currently pins one worker,
   the coding-patch profile, `max_concurrent_jobs: 1`, no benches — which
   makes v1's valve BINARY (share or don't). Revisiting D5 is what would give
   the dial real positions. Recommendation: accept the binary v1 and let the
   percentage live only in the recommendation text (claim 12).
8. **Tenant binding of a volunteered workstation.** codexFactory declares
   repositories and secrets `per_tenant`. Recommendation: require a
   volunteered workstation to be bound to exactly ONE `software_team` tenant
   on its lease and refuse cross-tenant co-residency outright — the alternative
   is one engineer's machine holding two tenants' content simultaneously.
9. **Generalize the handling gate, or not?** A dispatch-time gate comparing
   source-content policy to the target host's attested boundary already
   exists, validated and ratified — but scoped to the `document-cataloging`
   capability. Promoting it to the neutral job envelope would make "may this
   content land on this host" answerable for ANY job, which is exactly the
   question a volunteered workstation raises. Otherwise the valve ships with
   per-capability gating and a named gap.
10. **Who owns the recommendation?** A delegated surface of the governance
    agents that already own capacity tradeoffs and worker status, or a local
    advisory those agents never see? (Claim 18.)
11. **Is "set share level" a governed authority verb?** The closed
    `authority_action` enum — replicated in both the schema and the DDL — has
    no job or capacity verb, so "recover my compute" as a GRANTED action has
    nothing to bind to today. Either grow the enum or state deliberately that
    the valve is a local capacity preference outside the grant model, which
    the broker may ignore.
12. **The five "yield to the human" task booleans** (`RunOnlyIfIdle`,
    `StopOnIdleEnd`, `RestartOnIdle`, `DisallowStartIfOnBatteries`,
    `StopIfGoingOnBatteries`) are all deliberately FALSE today so attestation
    never goes quiet. Do they get revisited for a workstation host class, and
    should the RUNNER service inherit them rather than only the supervisor?

## Adjacent work in flight (coordinate, do not duplicate)

A brainstorm named `tenant-project-catalog-and-workstation-cache` was being
written in `ideation/brainstorm/` by another session on 2026-07-27, defining
the boundary between a company-scoped codexFactory PROJECT CATALOG and its
engineer-workstation projection — the deployed company runtime authoritative
for projects, repository composition and principal access, with the
workstation holding only a tenant- and principal-scoped cache. That is the
same workstation the shell in this topic runs on, and its principal scoping
is the same axis as claim 5's principal separation. Deliberately NOT linked
by path here because it was still untracked when this topic landed; reconcile
the two before either exits to a change, and expect the catalog topic to own
WHAT the workstation may hold while this topic owns WHO runs the surfaces
that read it.

## Recorded observation (not a claim of this topic)

`avatar-first-ui`'s ratified requirement text still uses the LEGACY layer
spellings ("Customer Hermes surfaces", "Client Hermes surfaces"), which the
2026-07-23 `adopt-subject-tenant-domain-vocabulary` ratification says MUST
NOT name a Hermes layer on new or substantively revised governance surfaces.
It is not a violation as released — released identifiers stay byte-stable
until the next major bundle, and `layer-vocabulary`'s `legacy_mapping`
interprets them — but the next SUBSTANTIVE revision of that requirement
should adopt subject/tenant/domain. Flagged here so the next editor does not
have to rediscover it.

## Exit path

Clusters with [mobile-dashboard-surface](../mobile-dashboard-surface/mobile-dashboard-surface.md)
(the same standard, the other form factor) and with
[dashboard-repo-selector](../dashboard-repo-selector/dashboard-repo-selector.md)
(the snapshot-source seam both planes bind). Realizes as an
`avatar-first-ui` realization plus a MODIFIED `ideation-dashboard` delta for
the app-managed local serve; the Worker Host App's principal separation is a
dependency satisfied in `Omnigent-Install`, not here. The codexFactory
subject feature set (claim 8) exits as its own staged topic in codexFactory
once Brett rules open questions 4 and 5. Nothing here is implementable until
the shell platform fork (open question 1) is closed.
