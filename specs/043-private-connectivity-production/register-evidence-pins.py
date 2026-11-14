#!/usr/bin/env python3
"""Generate/check only an exactly commissioned 043 record's commit inventory.

Use --check or --write explicitly, with --task and optional --instance. The
independent PC_EVIDENCE_TRUST/PC_EVIDENCE_TRUST_SHA256 and machine-local
PC_EVIDENCE_ROOTS inputs have the same meaning as verify-evidence.py. Check
mode never writes. Write mode only adds inventory to a new untracked draft,
within the current exact accepted file scope, before its immutable record
reference has been reviewed. Accepted/committed observations are never edited.
This helper establishes pin ownership/reachability, not task or gate acceptance.
--commissioning selects only the exact T010 commissioning.json control. Its
read-only inventory check may inspect pending custodian authentication; the
evidence verifier still refuses admission until that authentication is accepted.
Generation cannot rewrite a tracked or independently anchored control.
"""

import argparse
from contextlib import ExitStack
import json
import os
from pathlib import Path
import re
import runpy
import stat
import subprocess
import sys
from types import SimpleNamespace


TOKEN = re.compile(r"(?<![0-9A-Za-z])[0-9a-f]{40}(?![0-9A-Za-z])")
URL = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/(?:blob|commit)/([0-9a-f]{40})(?![0-9a-f])")
LOCAL = "opensoft/openxfactory"
FEATURE = "specs/043-private-connectivity-production"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(repository):
    require(isinstance(repository, str) and re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository), "invalid repository owner")
    return repository.lower()


def body(value):
    require(isinstance(value, dict), "evidence object required")
    return {key: item for key, item in value.items() if key != "pin_inventory"}


def hints(value):
    result = {}
    def add(pin, owner):
        if isinstance(pin, str) and TOKEN.fullmatch(pin):
            result.setdefault(pin, set()).add(canonical(owner))
    def visit(item):
        if isinstance(item, dict):
            if "repository" in item:
                for key in ("commit", "revision", "base"):
                    if key in item: add(item[key], item["repository"])
            for child in item.values(): visit(child)
        elif isinstance(item, list):
            for child in item: visit(child)
        elif isinstance(item, str):
            for owner, pin in URL.findall(item): add(pin, owner)
    visit(body(value))
    return result


def inventory(value, owners):
    normalized = {}
    for owner, commits in owners.items():
        name = canonical(owner)
        require(name not in normalized, "duplicate canonical owner")
        normalized[name] = set(commits)
    require(LOCAL in normalized, "coordinator reachability is required")
    content = body(value)
    tokens = sorted(set(TOKEN.findall(json.dumps(content, sort_keys=True))))
    declared = hints(content)
    rows = []
    for token in tokens:
        explicit = declared.get(token, set())
        require(len(explicit) <= 1, "conflicting explicit owners: " + token)
        available = {name for name, commits in normalized.items() if token in commits}
        if token in normalized[LOCAL]:
            require(not explicit or explicit == {LOCAL}, "local commit cannot be classified as foreign")
            owner = LOCAL
        elif explicit:
            owner = next(iter(explicit))
            require(owner in available, "explicit owner checkout/object unavailable: " + owner)
        else:
            require(len(available) == 1, "commit needs one verified owner: " + token)
            owner = next(iter(available))
        rows.append({"repository": owner, "openxfactory_commit" if owner == LOCAL else "foreign_commit": token})
    return rows


def validate_inventory(value, owners):
    require(isinstance(value.get("pin_inventory"), list), "missing pin_inventory")
    require(value["pin_inventory"] == inventory(value, owners), "inventory must exactly cover owned commit tokens in deterministic order")


def owner_commits(value, verifier):
    allowed = {canonical(name) for name in verifier.trust["repositories"].values()}
    allowed.update(canonical(name) for name in verifier.trust.get("pin_owners", []))
    roots = verifier.store.roots
    require(set(roots) <= allowed and LOCAL in roots, "uncommissioned/missing repository root")
    for declared in hints(value).values():
        require(declared <= set(roots), "explicit owner checkout unavailable")
    tokens = sorted(set(TOKEN.findall(json.dumps(body(value), sort_keys=True))))
    result = {}
    for owner, root in roots.items():
        if not tokens:
            result[owner] = set()
            continue
        # Fixed read-only batch operation. Missing objects stay missing; never fetch.
        environment = {key: item for key, item in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        try:
            process = subprocess.run(["git", "--no-optional-locks", "--no-replace-objects", "-C", str(root),
                                      "cat-file", "--batch-check=%(objectname) %(objecttype)"],
                                     input="\n".join(tokens) + "\n", capture_output=True, text=True, env=environment, check=False, timeout=30)
        except subprocess.TimeoutExpired as exc:
            raise ValueError("owner reachability read timed out") from exc
        require(process.returncode == 0, "owner reachability read failed")
        rows = process.stdout.splitlines()
        require(len(rows) == len(tokens), "incomplete owner reachability output")
        result[owner] = {token for token, row in zip(tokens, rows) if row == token + " commit"}
    return result


def _write_new_draft(root, relative, original, replacement):
    # Open each directory and the existing draft without following links. Keep
    # the same file descriptor through the final content check and write.
    with ExitStack() as stack:
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        stack.callback(os.close, directory)
        for part in relative.parts[:-1]:
            directory = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
            stack.callback(os.close, directory)
        descriptor = os.open(relative.name, os.O_RDWR | os.O_NOFOLLOW, dir_fd=directory)
        stream = stack.enter_context(os.fdopen(descriptor, "r+b"))
        info = os.fstat(stream.fileno())
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, "linked or non-regular draft refused")
        require(stream.read() == original, "draft changed during generation")
        stream.seek(0)
        stream.write(replacement)
        stream.truncate()
        stream.flush()
        os.fsync(stream.fileno())


def process(verifier, task, instance=None, *, write=False, commissioning=False):
    require(task in verifier.tasks and int(task[1:]) >= 10, "only closed T010-T068 receipts may carry new inventories")
    require(not commissioning or (task == "T010" and instance is None),
            "commissioning inventory belongs only to coordinator T010")
    instances = task in verifier_module().INSTANCE_TASKS
    require(instance is None or instances, "task has no child instances")
    if instances and instance is None:
        required = verifier.trust["instances"].get(task, [])
        require(required and len(required) == len(set(required)), "commissioned instances required")
        keys = [task + "@" + name for name in required]
    else:
        keys = [task + ("@" + instance if instance else "")]
    bindings = [verifier.binding(key) for key in keys]
    owner = verifier.tasks[task]["owner"]
    prefix = FEATURE + "/evidence/" if owner == "C" else "evidence/private-connectivity-production/"
    path = prefix + task + ".json"
    if commissioning:
        require(owner == "C", "commissioning owner must be coordinator")
        path = FEATURE + "/evidence/commissioning.json"
    if instance:
        require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", instance), "invalid instance identity")
        path = prefix + "instances/" + task + "/" + instance + ".json"
    for binding in bindings:
        require(binding["owner"] == owner and path in binding["files"], "record outside exact accepted task scope")
        if commissioning or write or "record" not in binding:
            verifier.authority(binding["authority"], binding)
        else:
            # Reading accepted evidence does not require leaving an execution grant open.
            record = verifier.read(binding["record"])
            verifier.evidence_authority(binding, record)
    repository = canonical(verifier.trust["repositories"][owner])
    root = verifier.store.root(repository)
    relative = Path(path)
    target = root / relative
    require(target.resolve().is_relative_to(root) and all(not root.joinpath(*relative.parts[:i]).is_symlink()
            for i in range(1, len(relative.parts) + 1)), "record symlink/escape refused")
    require(target.is_file() and target.stat().st_nlink == 1, "linked or missing record refused")
    raw = target.read_bytes()
    module = verifier_module()
    value = module.decode(raw)
    if commissioning:
        require(value["schema"] == "043-reviewed-trust-v1" and value["feature"] == module.FEATURE
                and value["definition"] == module.DEFINITION and "source_container" in value,
                "wrong source commissioning object")
    else:
        require(value["task"] == task, "record task mismatch")
        if not instances or instance:
            require(value["instance"] == instance, "record instance mismatch")
    resolved = owner_commits(value, verifier)
    if write:
        require(commissioning or all("record" not in binding for binding in bindings), "reviewed immutable record cannot be rewritten")
        require(not commissioning or verifier.trust_reference["path"] != path,
                "reviewed commissioning control cannot be rewritten")
        require(not instances or instance is not None or task not in verifier.trust.get("aggregates", {}), "reviewed immutable aggregate cannot be rewritten")
        require(not verifier.store.git(root, "ls-files", "-z", "--", path), "committed/tracked record cannot be rewritten")
        value["pin_inventory"] = inventory(value, resolved)
        validate_inventory(value, resolved)
        _write_new_draft(root, relative, raw, (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode())
    else:
        validate_inventory(value, resolved)
        references = ([verifier.trust_reference] if commissioning else
                      [binding["record"] for binding in bindings if "record" in binding])
        if instances and instance is None:
            references = [verifier.trust["aggregates"][task]]
        for ref in references:
            require(ref["path"] == path and canonical(ref["repository"]) == repository
                    and verifier.store.blob(ref) == raw, "inventory record differs from reviewed immutable content")
    return path


def verifier_module():
    # run_path compiles the reviewed sibling without creating an owner-tree .pyc.
    return SimpleNamespace(**runpy.run_path(str(Path(__file__).with_name("verify-evidence.py")), run_name="_pc043_pin_reader"))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--instance")
    parser.add_argument("--commissioning", action="store_true",
                        help="exact T010 source commissioning container; inventory only, never evidence acceptance")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        module = verifier_module()
        root = Path(__file__).resolve().parents[2]
        tasks = module.load_contract(root)
        revision, separator, path = os.environ.get("PC_EVIDENCE_TRUST", "").partition(":")
        require(separator, "independently reviewed PC_EVIDENCE_TRUST is required")
        roots = module.decode(os.environ.get("PC_EVIDENCE_ROOTS", "{}"))
        require(isinstance(roots, dict) and LOCAL not in {key.lower() for key in roots}, "coordinator root cannot be overridden")
        roots[LOCAL] = str(root)
        store = module.GitStore(roots)
        ref = dict(repository=LOCAL, commit=revision, path=path, sha256=os.environ.get("PC_EVIDENCE_TRUST_SHA256", ""))
        verifier = module.Verifier(tasks, store, ref, prepare=arguments.commissioning)
        result = process(verifier, arguments.task, arguments.instance, write=arguments.write,
                         commissioning=arguments.commissioning)
        print(("GENERATED draft inventory: " if arguments.write else "CHECKED inventory (read-only): ") + result)
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError, RecursionError) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
