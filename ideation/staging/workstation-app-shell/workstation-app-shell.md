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
Topics: avatar-first-ui, ideation-dashboard, client-surface, hermes-layers, worker-host, workstation, gate-console, two-plane, identity
Repository context: openxFactory owns the neutral surface standard
(`avatar-first-ui`, ratified) and this topic; the shell platform decision is
shared with the avatar-client track (private `xfactory-avatar-client` repo);
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
   staged workbench, gate console, health. The missing piece is Track C's
   chat rail. Nothing in this topic asks for a new tenant UI; it asks for a
   host for the one that exists.
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
