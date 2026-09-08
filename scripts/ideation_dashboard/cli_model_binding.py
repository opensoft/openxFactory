"""The MODEL-PROVIDER SETTINGS command line: the `model-binding` verbs
(`split-opendox-two-layer-product` § 2.4, PR 4 of 4).

FIXED CORE, NOT AN EXTENSION. Design § D3 files "provider and broker" in the
openDox column, so `build_parser` calls `_add_model_binding_parser` directly and
this surface keeps its position in the parser exactly.

The cleanest of the three moves: nothing here reaches back into the core at all
— the verbs are a closed loop over `doxbench_binding` — so this module needs no
`_core()` accessor and holds no reference to `cli` in either direction.
"""

from __future__ import annotations

import argparse
import dataclasses
import sys
from pathlib import Path

from ideation_dashboard import doxbench_binding as binding_mod


# ===========================================================================
# THE MODEL-PROVIDER SETTINGS SURFACE (add-model-provider-broker task 1.2)
#
# List, add, edit, remove — and a credential hand-off that retains nothing.
#
# WHY THE OPERATOR DOOR IS A CLI VERB AND NOT A BROWSER PANE, stated plainly
# because it is a decision and not an oversight (see tasks.md 1.2). Every other
# install-time declaration this console makes — the notebook adapter, the
# retrieval backend, the model session root — is made at the entrypoint, and
# this is the same kind of fact. It is also the stronger place for a credential
# to be typed: a key entered here travels from a terminal handle to the
# broker's standard input and crosses no HTTP wire at all, so the "no
# credential reaches the browser" property is not something the surface has to
# be careful about — it is structural.
# ===========================================================================


def _binding_store(args: argparse.Namespace) -> "binding_mod.BindingStore":
    """The store this invocation acts on. `--bindings` when given, else the
    checkout's own declared path — ONE rule, shared with the entrypoints."""
    path = (Path(args.bindings).resolve() if getattr(args, "bindings", None)
            else binding_mod.bindings_path(Path(args.repo_root).resolve()))
    return binding_mod.BindingStore(path)


def _declared_binding(args: argparse.Namespace) -> "binding_mod.ModelProviderBinding":
    return binding_mod.ModelProviderBinding(
        id=args.id, label=args.label, provider=args.provider,
        credential_ref=args.credential_ref, auth_kind=args.auth_kind,
        approved_by=args.approved_by, endpoint=args.endpoint,
        dialect=args.dialect, broker_argv=tuple(args.broker_argv))


def cmd_model_binding_list(args: argparse.Namespace) -> int:
    """DISCLOSE every declared binding (task 1.2's read-back).

    Prints the binding's own fields and the fixed custody sentence. There is no
    credential material to redact, which is the claim: a read-back cannot leak a
    secret it was never able to hold."""
    store = _binding_store(args)
    try:
        disclosure = store.read_back()
    except binding_mod.BindingRefused as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"  bindings {store.path}")
    if not disclosure["bindings"]:
        print("  (none declared — this install talks to no brokered provider)")
        return 0
    for record in disclosure["bindings"]:
        print(f"  {record['id']}  {record['label']}")
        print(f"    provider         {record['provider']}")
        print(f"    auth kind        {record['auth_kind']}")
        print(f"    approved by      {record['approved_by']}")
        print(f"    credential ref   {record['credential_ref']}")
        print(f"    endpoint         {record['endpoint']}")
        print(f"    dialect          {record['dialect']}")
        print(f"    broker argv      {record['broker_argv']}")
        print(f"    custody          {record['credential_custody']}")
    return 0


def cmd_model_binding_add(args: argparse.Namespace) -> int:
    store = _binding_store(args)
    try:
        binding = store.add(_declared_binding(args))
    except binding_mod.BindingRefused as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"  declared {binding.id} in {store.path}")
    print(f"  {binding_mod.CUSTODY_NOTICE}")
    return 0


def cmd_model_binding_edit(args: argparse.Namespace) -> int:
    store = _binding_store(args)
    try:
        binding = store.edit(_declared_binding(args))
    except binding_mod.BindingRefused as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"  updated {binding.id} in {store.path}")
    return 0


def cmd_model_binding_remove(args: argparse.Namespace) -> int:
    store = _binding_store(args)
    try:
        binding = store.remove(args.id)
    except binding_mod.BindingRefused as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"  retired {binding.id} from {store.path}")
    print(f"  {binding_mod.REMOVAL_NOTICE}")
    return 0


def cmd_model_binding_set_credential(args: argparse.Namespace, *,
                                     source=None) -> int:
    """Hand a credential to the broker and keep only the reference (task 1.3).

    THE VALUE IS NEVER READ HERE. `source` is the open handle — `sys.stdin` by
    default — and it is passed straight through to
    `doxbench_provider.hand_off_credential`, which streams it into the broker's
    standard input. No variable in this function ever holds the credential, so
    none can outlive the call, be echoed in a message, or reach an exception.
    It is deliberately NOT a command-line argument: an argv is visible in the
    process table and lands in a shell history."""
    from ideation_dashboard import doxbench_provider as provider_mod

    store = _binding_store(args)
    try:
        binding = store.get(args.id)
        if binding is None:
            raise binding_mod.BindingRefused(
                f"no binding with id {args.id!r} is declared")
        reference = provider_mod.hand_off_credential(
            binding, source if source is not None else sys.stdin)
        store.edit(dataclasses.replace(binding, credential_ref=reference))
    except (binding_mod.BindingRefused, provider_mod.BrokerRefused) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"  the broker took custody and returned the reference {reference}")
    print(f"  {binding_mod.CUSTODY_NOTICE}")
    return 0


def _add_binding_store_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo-root", required=True,
                        help="the checkout whose bindings are being read")
    parser.add_argument(
        "--bindings", default=None,
        help="the bindings document (default: "
             f"<repo-root>/{binding_mod.DEFAULT_BINDINGS_RELPATH})")


def _add_binding_declaration_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--id", required=True, help="the binding's id")
    parser.add_argument("--label", required=True,
                        help="the label the model menu shows")
    parser.add_argument("--provider", required=True,
                        help="the provider name the broker takes custody for "
                             "(the broker's declared `--provider`)")
    parser.add_argument("--credential-ref", required=True,
                        dest="credential_ref",
                        help="the reference the broker resolves; NEVER the "
                             "credential itself")
    parser.add_argument("--auth-kind", required=True, dest="auth_kind",
                        choices=list(binding_mod.AUTH_KINDS),
                        help="the authentication kind the broker holds")
    # REQUIRED because the broker requires it: `credential-contracts` holds
    # that a grant without an approver is invalid, and the broker's `intake`
    # refuses without an approver flag. A binding that could not name one could
    # never enrol.
    #
    # SPELLED `--credential-approver` AND NOT AFTER THE BROKER'S OWN FLAG, and
    # that is deliberate rather than careless — MEASURED, in fact: the obvious
    # mirrored spelling turned the suite red.
    # `test_session_verbs.py`'s `test_the_save_cli_offers_no_token_and_no_
    # bypass_flag` scans THIS FILE'S SOURCE for a family of forbidden flag
    # spellings, one of which is the approving verb with two leading dashes,
    # because `contracts/cli.md` + D22 hold that no CLI flag may approve, merge
    # or bypass a record. A substring scan cannot tell a flag that APPROVES
    # from one that NAMES AN APPROVER, and the invariant it protects is worth
    # more than a mirrored spelling — so the flag is renamed rather than the
    # guard loosened, and this comment states the collision without restating
    # the spelling that trips it. The BINDING's field and the broker's own flag
    # keep the declaration's spelling; only this operator-facing name differs,
    # and `dest` carries it back.
    parser.add_argument("--credential-approver", required=True,
                        dest="approved_by",
                        help="the human principal who approved this "
                             "credential; the broker requires one at intake "
                             "and records it on every grant")
    # THE PROVIDER ROUTE IS THE CONSUMER'S. openProfiler's declaration emits
    # neither an endpoint nor a dialect from a mint, deliberately, so both are
    # declared here — see doxbench_binding's module docstring.
    parser.add_argument("--endpoint", required=True,
                        help="the provider endpoint this binding's minted "
                             "token is presented at")
    parser.add_argument("--dialect", required=True,
                        choices=list(binding_mod.DIALECTS),
                        help="the request grammar that endpoint speaks")
    # A POSITIONAL, taken after a bare `--`, and that is the fix for a real
    # trap rather than a style choice: a broker invocation is full of
    # option-shaped members (`--binding`, `--ref`), and as a flag's value they
    # are consumed by THIS parser instead — `--binding` was measured being
    # matched to `--bindings` by argparse's prefix abbreviation, silently
    # rewriting the operator's store path and truncating their template. The
    # subparsers below also set `allow_abbrev=False`, so the two defences are
    # independent.
    parser.add_argument(
        "broker_argv", nargs="+", metavar="-- BROKER ARGV",
        help="the broker invocation, as argv members, after a bare `--`. "
             f"Placeholders {binding_mod.ARGV_PLACEHOLDERS} are filled from "
             "this binding's own fields")


def _add_model_binding_parser(sub) -> None:
    group = sub.add_parser(
        "model-binding",
        help="model-provider settings: list / add / edit / remove bindings, "
             "and hand a credential to the broker")
    verbs = group.add_subparsers(dest="model_binding_command", required=True)

    listing = verbs.add_parser("list", help="disclose every declared binding",
                               allow_abbrev=False)
    _add_binding_store_args(listing)
    listing.set_defaults(func=cmd_model_binding_list)

    adding = verbs.add_parser("add", help="declare a new binding",
                              allow_abbrev=False)
    _add_binding_store_args(adding)
    _add_binding_declaration_args(adding)
    adding.set_defaults(func=cmd_model_binding_add)

    editing = verbs.add_parser("edit", help="replace an existing binding",
                               allow_abbrev=False)
    _add_binding_store_args(editing)
    _add_binding_declaration_args(editing)
    editing.set_defaults(func=cmd_model_binding_edit)

    removing = verbs.add_parser("remove", help="retire a binding",
                                allow_abbrev=False)
    _add_binding_store_args(removing)
    removing.add_argument("--id", required=True, help="the binding to retire")
    removing.set_defaults(func=cmd_model_binding_remove)

    handing = verbs.add_parser(
        "set-credential",
        help="read a credential from STANDARD INPUT, hand it to the broker, "
             "and keep only the reference it returns",
        allow_abbrev=False)
    _add_binding_store_args(handing)
    handing.add_argument("--id", required=True,
                         help="the binding whose credential is being set")
    handing.set_defaults(func=cmd_model_binding_set_credential)
