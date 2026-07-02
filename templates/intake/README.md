# xFactory Intake Templates

Status: starter catalog
Repository context: openxFactory
Purpose: provide machine-readable intake templates for website intake, TUI
self-install, and downloadable installer flows.

## Template Selection

Use the taxonomy model:

```text
factory_type + factory_subtype
  selects the expert work and Omnigent layer

target_domain + target_domain_subtype
  selects subject matter overlays

client_industry + client_type
  selects client-facing assumptions and deployment language
```

See [xFactory Taxonomy Model](../../docs/factory-taxonomy-model.md).

UI templates live separately under [templates/ui](../ui/README.md). Intake
selects the domain factory and profile; avatar-first UI profiles define how
users interact with the selected factory.

Installation templates live separately under
[templates/installation](../installation/README.md). Intake decides which
factory and profile should be installed; the installation spine decides how the
client environment is discovered, validated, migrated, and cut over.

Client-layer templates live under [templates/client-layer](../client-layer/README.md).
They define how a Client Hermes overlay models products, services,
subscriptions, managed services, and hybrid offers.

## Files

- [index.yaml](index.yaml) lists all starter templates.
- [schema.yaml](schema.yaml) describes the expected template shape.
- [subtypes/catalog.yaml](subtypes/catalog.yaml) lists 10 intake subtype/profile
  records for each top-level factory template.
- [medical.yaml](medical.yaml) covers clinical and medical operations.
- [operations.yaml](operations.yaml) covers IT operations, sysops, MSP, and DevOps.
- [accounting.yaml](accounting.yaml) covers accounting, tax, audit, and finance ops.
- [marketing.yaml](marketing.yaml) covers marketing, advertising, growth, and brand ops.
- [software.yaml](software.yaml) covers software engineering and product delivery.
- [law.yaml](law.yaml) covers legal, contracts, compliance, and policy work.
- [insurance.yaml](insurance.yaml) covers claims, underwriting, brokerage, and policy ops.
- [manufacturing.yaml](manufacturing.yaml) covers plant, quality, safety, and maintenance ops.
- [logistics.yaml](logistics.yaml) covers supply chain, freight, transportation, and warehouse ops.
- [retail.yaml](retail.yaml) covers retail, ecommerce, marketplace, and customer ops.

## Install Readiness Loop

Run the subtype readiness simulator after changing the catalog or after syncing
domain factory repos:

```bash
python3 scripts/simulate-subtype-install-readiness.py
```

It loops through every factory type and subtype, compares the catalog with the
local domain repos, and regenerates:

- [Intake Subtype Install Readiness Report](../../docs/intake-subtype-install-readiness-report.md)
- [Intake Subtype Install Runbook](../../docs/intake-subtype-install-runbook.md)
- [Intake Subtype Second-Pass Gap Report](../../docs/intake-subtype-second-pass-gap-report.md)
- [pass1.yaml](../../examples/intake-runtime-simulations/pass1.yaml)
- [pass2.yaml](../../examples/intake-runtime-simulations/pass2.yaml)

These templates contain no secrets and no customer records. They provide
defaults, prompts, and scaffold recommendations. User-entered answers must still
be labeled as declared, template_default, inferred, simulated, confirmed, or
approved_for_instantiation.
