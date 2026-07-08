# xFactory Intake Subtype Catalog

Status: draft
Kind: template
Repository context: openxFactory
Purpose: provide 10 starter subtype/profile records for each top-level xFactory
intake template.

The top-level templates in `templates/intake/*.yaml` describe the factory
family. This subtype catalog expands each family into 10 selectable intake
profiles for the website, TUI, and downloadable installer.

Each subtype record includes:

- taxonomy fields
- supported client types
- customer-subject types
- workflow seeds
- credential families
- adapter families
- high-risk boundaries
- recommended intake questions
- Hermes council mode defaults
- runtime binding focus

Validate with:

```bash
python3 scripts/validate-intake-templates.py
```
