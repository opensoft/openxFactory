# xFactory UI Templates

Status: starter catalog
Repository context: openxFactory
Purpose: provide reusable UI templates that domain factories specialize.

## Files

- [avatar-first.yaml](avatar-first.yaml) defines the standard avatar-first UI
  template for all xFactories.

## Boundary

openxFactory owns the reusable UI grammar. Domain factory repos own domain
personas, domain language, safety policy, tool classes, escalation roles, and
implementation details.

The template is not a frontend application. It is the contract a frontend,
mobile app, kiosk, embedded widget, or voice session should satisfy.
