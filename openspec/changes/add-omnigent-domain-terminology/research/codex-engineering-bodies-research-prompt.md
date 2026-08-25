# Research prompt: current bodies for software-engineering WORK taxonomy

Status: record
Prepared: 2026-08-09 for a live-research AI (current web access required).
Serves: task 3b.5e. Results feed this registry and the codexFactory overlay
(`xFactories/codexFactory/omnigent/domain-overlay.yaml`).

Why: codex has **no terminology block at all** — no display labels, no
crosswalks. This is a from-scratch population rather than a correction, so
nothing here needs unpicking; the risk is introducing unverified terms in
the first place, which is exactly what went wrong in the two accounting
rounds.

---

## PROMPT (copy from here down)

Identify **bodies whose published taxonomies name software-engineering
WORK**, so an agent system can display internal worker-role names in
terminology an engineer recognizes.

### QUESTION ONE — reuse rights, before anything else

Not "is it free to obtain." This:

> May we embed the body's **element names and identifiers** verbatim inside a
> YAML configuration file shipped in a **publicly readable product
> repository** distributed to third parties, without a negotiated licence?

Per body: exact licence/terms (link the licence text), redistribution rights
in a derived work and their conditions, required attribution wording,
trademark constraints, and whether the **specification** and the **element
data** are licensed differently.

Specific licence questions for this domain:

- **SWEBOK** (IEEE Computer Society) — current edition (v4?) and its
  copyright/reuse terms for knowledge-area names.
- **ISO/IEC/IEEE 12207** — ISO sells its standards; confirm whether process
  names may be cited in product configuration.
- **SFIA** — the SFIA Foundation licences some commercial use; establish
  whether ours needs a licence. Do not assume "free to view" means "free to
  embed."
- **The Scrum Guide** is reportedly **CC BY-SA 4.0**. Share-alike is the
  catch: would embedding Scrum role/event names in our configuration
  **oblige us to license our own file under CC BY-SA**? That question
  decides whether Scrum vocabulary is usable at all, so answer it
  explicitly. **SAFe** is Scaled Agile Inc. property — assess separately.

### QUESTION TWO — candidates to assess

- **O\*NET** (CC BY 4.0) — the only obviously licence-clean role/task source
  we have found, already adopted for accounting. Give **exact SOC
  occupations and task/work-activity vocabulary** for software development,
  QA/testing, security engineering, technical writing, and engineering
  management. Do not guess codes.
- **SWEBOK** knowledge areas.
- **ISO/IEC/IEEE 12207** life-cycle processes.
- **SFIA** skills (PROG, TEST, DESN, ARCH and similar — confirm the codes
  exist with those meanings in the current version).
- **Scrum Guide** roles/events, subject to the share-alike question above.
- **DORA / DevOps** vocabulary — is it a taxonomy or just metrics?
- Anything authoritative we have not named.

### QUESTION THREE — the domain boundary that must not be blurred

codex's terminal action is the **merge** — admitting code to the trunk. **No
worker holds it**: merge authority sits with GitHub branch protection and a
human Merge Master. Terms implying **authority to merge, approve a release,
or sign off quality** are not honest labels here. Two specific traps:

- `pr_admission_agent` and `merge_readiness_agent` *propose*; naming them
  with a reviewer/approver term would imply the authority they are
  specifically denied.
- `scrum_master_worker` shares a name with a **human Scrum role** that
  carries team-facilitation and process authority over people. If Scrum
  vocabulary is licensable and used, this mismatch must be recorded, not
  smoothed — the same way we recorded that O\*NET's "bookkeeper" occupation
  includes posting while our bookkeeper worker cannot post.

### The worker roles

| Worker | Archetype | What it does |
|---|---|---|
| engineering_decomposer | frame | Splits approved scope into bounded feature DAGs |
| spec_planner | frame | Produces specification, clarification, plan, tasks, analysis |
| coding_agent | generate | Writes code changes |
| test_agent | verify | Runs and writes tests |
| security_agent | verify | Security review of changes |
| documentation_agent | generate | Produces documentation |
| branch_review_agent | challenge | Adversarial review of a branch |
| pr_admission_agent | assemble_for_admission | Assembles and proposes a PR for admission |
| merge_readiness_agent | assemble_for_admission | Assembles merge-readiness evidence; proposes only |
| scrum_master_worker | frame | Process framing and flow management |
| release_note_agent | generate | Produces release notes |

All are artifact-only: none merges, releases, or grants approval.

### Output format

Registry-shaped YAML per recommended body:

```yaml
- id: <lowercase_snake_id>       # existing ids include swebok, sfia, iso_iec_ieee_12207
  name: <official name>
  steward: <current maintaining organization>
  jurisdiction: <international | united_states | ...>
  names: <knowledge_areas | life_cycle_processes | skills | practices | roles_and_events | other:describe>
  scope: >-
    Coverage and which of the eleven workers it honestly fits.
  current_version: <version / date>
  status: <current | superseded_by:X | under_revision>
  source_url: <primary source>
  term_list_availability: <public | paywalled | membership_only>
  reuse_licence: <exact licence or terms, with link>
  redistribution_permitted_in_product_config: <yes | yes_with_conditions | no | unclear>
  share_alike_obligation: <none | yes — describe what it would oblige>
  attribution_required: <verbatim text if any>
  attribution_note: <trademark and other constraints>
  confidence: <high | medium | low>   # with reasoning
```

Then prose: a per-worker fit table for all eleven, naming which you would
mark `no_clean_equivalent` and why, and a single recommended crosswalk set.

### Ground rules

- **Primary sources only** for licence and version claims.
- **Do not guess identifiers, codes, or version numbers.** A gap beats a
  wrong citation; both prior corrections in this project came from guesses.
- **"No equivalent" and "do not register" are useful answers.**
- Distinguish verified fact from inference; give as-of dates.
