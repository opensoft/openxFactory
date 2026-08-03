"""Ideation-dashboard engineering surface (codexFactory realization of the
ratified openxFactory `add-ideation-dashboard` change, section 3).

A deterministic snapshot generator over `ideation/` plus active and archived
OpenSpec changes, a static repo-tracked renderer, and a bounded human/agent
action layer. The whole surface is bound by one non-negotiable interactivity
boundary (see `boundary.py`): the snapshot is the only data path, machinery is
non-mutating over source documents and never executes a lifecycle gate, and
gate authority is human-only.

The five contract schemas and the strict validator are consumed READ-ONLY from
the pinned openxFactory checkout; nothing normative is restated here.
"""

from __future__ import annotations

GENERATOR_VERSION = "ideation-dashboard-generator/0.1.0"
