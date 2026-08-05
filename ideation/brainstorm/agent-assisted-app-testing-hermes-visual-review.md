# Hermes Designer Visual Review — Brainstorm

Status: brainstorm
Kind: process
Summary: Use an independent Hermes visual-design specialist to classify visual evidence and prepare baseline-update findings for the Experience Council while Subject Hermes retains product admission and Merge Master retains enforcement.
Topics: agent-assisted-app-testing, hermes, visual-review, design-agent, experience-admission-council, baseline-approval, subject-hermes
Repository context: openxFactory; visual-design specialist review for browser evidence, with a future Flutter visual-review adapter
Captured: 2026-08-02

## Possible feats

- **Hermes visual review packet** — give a designer agent the raw comparison, declared derivatives, machine metrics, specs, tokens, and render identity in a structured input.
- **Candidate baseline PR assistant** — turn an explainable intentional-diff classification into a reviewable snapshot and metadata change without mutating the approved reference directly.
- **Experience Council visual lane** — contribute a specialized visual finding to a role-separated council without treating one model's classification as product approval.

## Focus

Hermes can make visual review faster by connecting a diff to project experience intent, component specifications, tokens, and the originating annotation or audit observation. This atomic role is a visual-design specialist. It should not be confused with Project/Subject Hermes, the Experience Admission Council, or an autonomous baseline writer.

The authority boundary is:

```text
machine diff ──► visual specialist finding ──► Experience Council
     │                    │                           │
     └──── raw evidence ──┴──── rationale ────────────┤
                                                      ▼
                                          Subject Hermes admission
                                                      │
                                                      ▼
                                          Merge Master enforcement
```

The specialist may say that a change appears intentional or that a platform difference is expected. It may prepare the candidate update and explain its affected profiles. Only a Project Owner admission followed by the configured merge path may make the candidate the new reference.

## Review inputs and output

Hermes should receive a bounded review packet containing:

- approved baseline and current capture references, with hashes;
- raw diff and declared derivative images, including transform metadata;
- pixel counts, ratios, connected regions, geometry, and protected-region intersections;
- canonical and user/OS render-manifest identities;
- application revision, fixture/state hash, route, component/flow identity, and annotation intent;
- relevant component specs, design tokens, accessibility/workflow constraints, and optional Figma context;
- prior accepted baseline lineage and any open migration record.

The output should be structured and limited to evidence-backed claims:

```json
{
  "outcome": "baseline-update-candidate",
  "confidence": 0.84,
  "affected_profiles": ["linux-loki-chromium-v1", "windows-chromium-v1"],
  "regions": [{ "id": "diff-01", "kind": "spacing", "severity": "review" }],
  "reason": "The requested button emphasis change changes the approved component state in the same region as the annotation.",
  "required_action": "open-baseline-update-pr",
  "evidence_refs": ["artifact://.../raw-diff.png", "artifact://.../metrics.json"]
}
```

Useful v1 outcomes are:

- `pass` — no material difference or an already permitted threshold result;
- `expected-change` — evidence and intent align, so a candidate update may be prepared;
- `platform-variance` — the difference is confined to a known profile-specific rendering behavior and should follow policy;
- `real-regression` — evidence conflicts with intent or safety constraints and should block or return to implementation;
- `inconclusive` — evidence is missing, contradictory, or too ambiguous for an agent decision;
- `baseline-update-candidate` — an explicit candidate artifact/PR is warranted, never an approval by itself.

Confidence should communicate uncertainty, not become a substitute for policy. Low confidence or disagreement with a spec should escalate.

## V1 operating model

V1 should start with deterministic machine checks, one design proposer when design interpretation is needed, and at least one independent visual reviewer for a changed baseline. The specialist is invoked after the raw comparison has been produced, and its finding is attached to the Experience Council packet. It should not be trained online, change trust weights from individual outcomes, or make a blocking decision from a derivative image alone.

The candidate update flow is:

1. capture all required profiles under the named render manifests;
2. run the raw deterministic comparison and preserve the complete packet;
3. ask the independent visual specialist to classify the difference against the UI constitution, intent, specs, tokens, and profile policy;
4. if the result supports an intentional change, prepare a branch or pull request containing snapshots, metadata, hashes, and rationale;
5. combine the visual finding with UX, accessibility, design-system, and browser-quality evidence required by the Experience Council;
6. obtain Project Owner admission and Project Manager disposition inside the autonomy envelope;
7. send the admitted revision to Merge Council/Merge Master and external enforcement, or return it for another iteration.

The visual specialist must not directly overwrite an approved snapshot, broaden a mask, relax a threshold, delete old evidence, or close the originating intent as a consequence of its own classification. A Project Hermes admission may authorize a candidate baseline only when the code, test, snapshot, and evidence changes remain atomic and inside the active autonomy policy.

## Experience Council integration

Visual review is one lane of the [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md). Other lanes can include:

- geometry/layout reviewer;
- visual style/color/typography reviewer;
- accessibility/semantics reviewer;
- browser-quality evidence and the Project Owner decision that applies project intent and repository policy.

The council should retain individual rationales and evidence references before Subject Hermes decides. Model swapping, weighted voting, and learned trust remain hypotheses to measure against a labeled visual-diff set, not assumptions to embed in the first blocking workflow. Historical outcomes may inform evaluation, but adaptive weights must not silently change acceptance policy.

The supplied Hermes/council examples are useful design inspiration. They do not, by themselves, establish controlled visual-regression accuracy or make an external Hermes product configuration a dependency of xFactory.

## Figma and design context

When a Figma MCP adapter is available, the specialist may use selected variables, component states, and links as design-intent context. It should report which design references it used and what claims they support. Figma context can explain why a change is expected; the repository baseline and Project Hermes admission still determine whether the runtime snapshot is accepted.

## Interfaces and boundaries

The specialist consumes the diff-review packet and produces a classification, rationale, confidence, and optional candidate update. It does not own the UI constitution, baseline registry, render environment, Project Owner verdict, merge authority, intent lifecycle, or spec override authority.

The review record should be append-only and linked to the exact application revision, profile IDs, input hashes, model/config identity, and policy version. This allows future evaluation of reviewer quality without rewriting history.

## Alternatives and tensions

- **Single visual reviewer:** lowers latency and simplifies audit, but cannot honestly cover interaction, accessibility, design-system, and quality concerns.
- **Risk-routed council:** expands specialist coverage only when the change class demands it, but depends on trustworthy classification and roster policy.
- **Local vision model:** keeps captures private and can be inexpensive, but may have weaker reasoning or require local hardware.
- **Hosted vision model:** may improve difficult judgments, but introduces data handling, cost, and availability concerns.
- **Automatic baseline update by the specialist:** fast, but collapses interpretation and authority and can erase regressions.
- **Subject Hermes-admitted candidate PR:** keeps the visual specialist advisory while allowing routine agent-only management and reversible enforcement.

## Open questions

- What model and deployment boundary can inspect regulated or sensitive screenshots safely?
- Which diff classes may open a candidate update automatically, and which require a larger specialist roster or protected gate?
- What labeled history and benchmark are needed before adding a council or adaptive weights?
- How should Hermes communicate uncertainty to the v1 SDLC session without stalling routine work?
- Which Figma context fields are stable enough to cite in a review record?

## Relationships

- [Approved UI Source of Truth](agent-assisted-app-testing-approved-ui-source.md) defines the authority Hermes must not replace.
- [Visual Diff Review](agent-assisted-app-testing-visual-diff-review.md) defines the raw evidence and derivative inputs.
- [OS Baseline Lifecycle](agent-assisted-app-testing-os-baseline-lifecycle.md) consumes candidate update proposals and governs migration.
- [Spec-Aware Change Safety](agent-assisted-app-testing-spec-safety.md) supplies constraints that can turn a visual change into a safety escalation.
- [UI Specialist Team and Separation of Duties](agent-assisted-app-testing-ui-specialist-separation.md) distinguishes the visual specialist from the proposer, implementer, reviewers, and authority roles.
- [Experience Admission Council](agent-assisted-app-testing-experience-admission-council.md) combines the visual finding with other specialist and deterministic evidence.
- [Synthesis: Hermes Autonomy and Human Exception Control](agent-assisted-app-testing-synthesis-human-control-and-safety.md) places Project Hermes inside the admission and exception boundary.
