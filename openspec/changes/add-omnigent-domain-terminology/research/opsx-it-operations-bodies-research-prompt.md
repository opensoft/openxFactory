# Research prompt: current bodies for IT-operations WORK taxonomy — clean and lock

Status: record
Prepared: 2026-08-09 for a live-research AI (current web access required).
Serves: task 3b.5e. Results feed this registry and the OpsxFactory overlay
(`xFactories/OpsxFactory/omnigent/domain-overlay.yaml`).

Why: opsx ships 9 workers with ITIL 4 and SFIA crosswalks that have never
been verified. Two accounting rounds both overturned equivalent
working-knowledge drafts, and one forced a framework out of shipped
configuration on licensing grounds. Assume these are wrong until checked.

---

## PROMPT (copy from here down)

Verify and correct a registry of **bodies whose published taxonomies name IT
operations WORK**, so an agent system can display internal worker-role names
in terminology an IT operations professional recognizes.

### QUESTION ONE — reuse rights, before anything else

Not "is it free to obtain." This:

> May we embed the body's **element names and identifiers** verbatim inside a
> YAML configuration file shipped in a **publicly readable product
> repository** distributed to third parties, without a negotiated licence?

Per body: exact licence/terms (link the licence text, not a summary),
whether redistribution in a derived work is permitted and on what
conditions, required attribution wording, trademark constraints, and whether
the **specification** and the **element data** are licensed differently — it
is the data we would embed.

Two specific worries, because both bodies are commercially stewarded:

- **ITIL 4** is PeopleCert/Axelos property and a registered trade mark. May
  we cite practice names (e.g. "Change Enablement") in shipped product
  configuration at all, and under what attribution?
- **SFIA** — the SFIA Foundation operates a licensing scheme with conditions
  attached to some commercial use. Establish exactly which uses require a
  licence and whether ours does. Do not assume "free to view" means "free to
  embed."

Also check **COBIT 2019** (ISACA copyright) and **ISO/IEC 20000** (ISO sells
its standards; our registry currently implies it is freely usable).

### QUESTION TWO — verify, correct, or reject our shipped crosswalks

These ship today and are unverified. Give a verdict on each, including
whether the mapping names the right *kind* of thing:

| Worker | Current crosswalk |
|---|---|
| ops_request_decomposer | itil4 → Service Request Management |
| operation_planner | itil4 → Change Enablement; sfia → CHMG Change management |
| readiness_validator | itil4 → Service Validation and Testing |
| inventory_agent | itil4 → Service Configuration Management; sfia → CFMG Configuration management |
| blast_radius_reviewer | itil4 → `no_clean_equivalent` ("ITIL assigns impact assessment to the change authority within Change Enablement, not a distinct practice") |
| credential_grant_reviewer | itil4 → `no_clean_equivalent`; sfia → SCTY Information security |
| change_documentation_agent | itil4 → Knowledge Management |
| evidence_correlation_agent | itil4 → Change Enablement — post-implementation review |
| admission_packet_agent | itil4 → Change Enablement — change request submission |

Confirm the SFIA codes (CHMG, CFMG, SCTY) exist with those meanings in the
current SFIA version, and give the version. Confirm ITIL 4 practice names
are current (ITIL 4 renamed several practices from ITIL v3 — flag any we
have wrong).

### QUESTION THREE — what we may be missing

- **O\*NET** (US Dept of Labor, CC BY 4.0). The only obviously licence-clean
  role/task source we have found; already adopted for the accounting domain
  on that basis. Give **exact SOC occupations and task/work-activity
  vocabulary** for systems administration, IT operations, service desk,
  security operations, and cloud/platform work. Do not guess codes.
- **NIST CSF 2.0** — public domain, US. Our registry has it; confirm the
  current version and whether its Functions/Categories fit the
  security-adjacent reviewers.
- **ISO/IEC 20000**, **CMMI**, **DevOps/DORA**, **SRE** vocabulary — assess
  whether any is a usable *work* taxonomy with permissive reuse.
- Any body an IT operations professional would consider authoritative that
  we have not named.

### QUESTION FOUR — the domain boundary that must not be blurred

opsx's terminal action is the **provider operation** — install, apply,
deploy, delete, cut over. **No worker holds it**: execution is a
human-approved act under a just-in-time grant, enforced externally by GitHub
branch protection, Azure/Kubernetes RBAC, and the platform itself. Terms
implying **authority to execute, approve a change, or administer a gate**
are not honest labels here. Flag any such mismatch — for example, an ITIL
"change authority" or a SFIA management-level skill would misdescribe these
workers.

### The worker roles

| Worker | What it does |
|---|---|
| ops_request_decomposer | Frames an approved request into a bounded operation DAG |
| operation_planner | Produces the deterministic dry-run plan and rollback |
| readiness_validator | Runs read-only readiness/preflight; produces readiness results |
| inventory_agent | Complete-universe/delta inventory and environment observation |
| blast_radius_reviewer | Adversarial check against prohibited actions, blast radius, domain boundaries |
| credential_grant_reviewer | Challenges grant discipline: least privilege, JIT, declared excess |
| change_documentation_agent | Change documentation and reviewed rollback narrative |
| evidence_correlation_agent | Correlates execution evidence; confirms effect on a readable surface |
| admission_packet_agent | Assembles and *proposes* the packet for the governing workflow's gate |

### Output format

Registry-shaped YAML per recommended body:

```yaml
- id: <lowercase_snake_id>       # existing ids include itil4, sfia, cobit_2019, nist_csf, iso_iec_20000
  name: <official name>
  steward: <current maintaining organization>
  jurisdiction: <international | united_states | ...>
  names: <practices | processes | skills | functions_and_categories | competencies | other:describe>
  scope: >-
    Coverage and which of the nine workers it honestly fits.
  current_version: <version / date>
  status: <current | superseded_by:X | under_revision>
  source_url: <primary source>
  term_list_availability: <public | paywalled | membership_only>
  reuse_licence: <exact licence or terms, with link>
  redistribution_permitted_in_product_config: <yes | yes_with_conditions | no | unclear>
  attribution_required: <verbatim text if any>
  attribution_note: <trademark and other constraints>
  confidence: <high | medium | low>   # with reasoning
```

Then prose: a verdict per shipped crosswalk; a per-worker fit table naming
which you would mark `no_clean_equivalent` and why; and a single recommended
crosswalk set.

### Ground rules

- **Primary sources only** for licence and version claims.
- **Do not guess identifiers, codes, or version numbers.** Both prior
  corrections in this project came from exactly that. A gap beats a wrong
  citation.
- **"No equivalent" and "do not register" are useful answers.**
- Watch acronym collisions; our registry's `cim` is the Chartered Institute
  of Marketing, not the energy-sector Common Information Model.
- Distinguish verified fact from inference; give as-of dates.
