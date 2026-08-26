# Preview Verification and Feedback Loop — Brainstorm

Status: brainstorm
Kind: process
Summary: Put a verified change on an isolated preview surface where Subject Hermes can run final synthetic checks and policy-selected users can optionally review, reject, or annotate it before experience and merge admission.
Topics: agent-assisted-app-testing, preview-environment, experience-admission, feedback-loop, branch-preview, annotation-context
Repository context: openxFactory; browser preview is the first verification surface and the handoff pattern should later support Flutter device or build previews
Captured: 2026-08-02

## Possible feats

- **Preview target contract** — publish the revision, URL or launch instructions, environment identity, expiry, synthetic missions, and test credentials needed for Project Hermes and optional user review.
- **Annotation target switcher** — let the user move between the current app and a preview while stamping annotations with branch, commit, and preview context.
- **Preview admission record** — record Subject Hermes acceptance, rejection, iteration, or a policy-required human/professional decision separately from automated verification.

## Focus

Automated tests can show that a proposed change passes selected checks, but some UI questions are most honestly evaluated against the integrated revision. The preview loop isolates the change, makes the tested revision reachable, lets Project Hermes execute final persona/journey checks, and provides a human review surface only where policy or direct user feedback requires it.

The original user remains authoritative for what they actually said in an annotation. That does not require the user to manage every proposal, iteration, or merge. Project/Subject Hermes may interpret and admit routine work inside the UI autonomy envelope using the project constitution, evidence, and Experience Council result.

## Proposed model

After implementation and automated verification, the workflow publishes a preview for the exact revision under test. Candidate preview mechanisms include a hosted branch deploy, a Docker Compose environment on a known port, a Storybook static deploy, or a Codespace. The common contract matters more than the provider:

```text
verified revision → preview target → Subject Hermes synthetic review
                         │                  ├─ admit → merge-readiness workflow
                         │                  ├─ reject/fix → preserve evidence and iterate
                         │                  ├─ optional user review → feedback/annotation
                         │                  └─ protected decision → park at owning gate
```

The preview record should include the source branch and commit, URL or launch command, environment configuration, authentication/data mode, expiry, synthetic persona/journey missions, and the evidence IDs that led to publication. The annotation client can expose a target switcher between the current app and preview. An annotation made on the preview should carry `context: preview`, the preview revision, and a parent intent reference so the agent does not mistake a regression in the fix for the original defect.

Experience admission must be a distinct state from automated verification. A machine-green result means the selected checks passed; it does not establish product value or resolve specialist disagreement. Project Owner admission, Project Manager disposition, Experience Council evidence, and any policy-required user/professional decision should remain distinct records. Rejection should preserve preview evidence and allow a new annotation, Hermes observation, comment, or explicit revision of the intent.

The annotation cleanup operation is a design seam. One option removes the original badge once automated evidence is green. Another keeps it visible as `verified-pending-admission` until Project Hermes or the owning protected gate accepts the preview. Direct user annotations may also retain a `resolved-by-hermes` projection so the person can inspect or reopen the outcome without becoming a mandatory workflow approver. Every choice needs a durable resolution record.

For a future Flutter workflow, the preview target may be a device build, emulator session, desktop build, or web build rather than a URL. The experience-admission and optional user-feedback contract should stay common while launch and annotation adapters remain platform-specific.

## Interfaces and boundaries

The preview handoff consumes a verified revision, evidence bundle, project UI constitution, synthetic mission set, and target environment policy. It emits a preview record, agent and optional user test instructions, admission/rejection state, and any child annotations, observations, or iteration links.

It does not choose the test scope, bypass spec safety, or claim that a deployment provider is available. Preview environments must respect authentication, data isolation, secret handling, retention, and regulated-data constraints; a convenient public URL is not automatically an acceptable preview.

## Alternatives and tensions

- **Hosted preview versus local Compose:** hosted previews are easy to share; local environments give control and production-like dependencies but require setup.
- **Storybook preview versus full application preview:** Storybook is quick for component changes; the full app is necessary when routing, auth, backend, or workflow behavior matters.
- **Automatic continuation after experience admission versus separate merge gate:** automatic continuation minimizes latency; Merge Council and Merge Master still preserve engineering readiness and external-enforcement authority.
- **Delete badge at verification versus after admission:** early cleanup is tidy; delayed cleanup makes unresolved Project Hermes or protected-gate review visible.
- **Mandatory user preview versus policy-selected preview:** mandatory review preserves direct human judgment but recreates the management queue; policy-selected review keeps humans for ambiguity, protected surfaces, or requested participation.

## Open questions

- Which preview providers are supported first, and what is the minimum portable preview contract?
- How does the in-house annotation client authenticate and switch between main, local, and hosted preview targets?
- What is the exact admission vocabulary across Project Owner, Project Manager, user feedback, and protected gates?
- How long should preview environments and their evidence remain available?
- For Flutter, which preview surface gives the fastest honest integrated review without requiring a full release build?

## Relationships

- [Annotation-Centered Test Intent](agent-assisted-app-testing-intent.md) supplies identity and allows preview annotations to retain lineage.
- [Cross-Environment Verification and Parity](agent-assisted-app-testing-verification-parity.md) supplies the automated evidence that precedes preview publication.
- [Spec-Aware Change Safety](agent-assisted-app-testing-spec-safety.md) keeps Project Owner or user preference from becoming a substitute for required constraints.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) supplies the Project Owner decision and required specialist findings.
- [UI Change Autonomy Envelope](agent-assisted-app-testing-ui-autonomy-envelope.md) determines when human preview is optional or required.
- [Synthesis: Hermes Autonomy and Human Exception Control](agent-assisted-app-testing-synthesis-human-control-and-safety.md) explains the admission and exception boundary.
