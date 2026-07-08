# xFactory Installation Templates

Status: draft
Kind: template
Repository context: openxFactory
Purpose: provide machine-readable installation templates that can be reused by
generic openxFactory installs and specialized DomainxFactory overlays.

## Files

- [openxfactory-installation-spine.yaml](openxfactory-installation-spine.yaml)
  defines the domain-neutral installation spine that always runs.

Domain factories may add overlay manifests that supplement, replace, constrain,
or veto specific stages. The overlay must still emit the required openxFactory
artifact families.

See [openxFactory Installation Spine And Domain Overlays](../../docs/openxfactory-installation-spine.md).

