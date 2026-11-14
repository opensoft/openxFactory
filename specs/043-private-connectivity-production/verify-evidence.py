#!/usr/bin/env python3
"""Read-only verifier for 043. Structural verification never grants acceptance.

The operator supplies PC_EVIDENCE_TRUST (commit:relative/path) and
PC_EVIDENCE_TRUST_SHA256 through an independently reviewed custody channel.
These are trust anchors, NOT receipt fields or discovered defaults. The pinned
manifest freezes bindings, owner repositories, actual commands/subchecks, scope,
authority, original outputs and history. Its reviewer must authenticate those
outputs and decisions. A hash or GitHub URL alone does not establish approval.
No production manifest is commissioned by this implementation.

PC_EVIDENCE_ROOTS is a machine-local JSON map of canonical owner aliases to
existing clones, for foreign Git-object reachability. No network calls occur.
Missing trust, objects, decisions or observations fail closed. This program
never executes the commands in evidence, writes files, or probes a target.
"""

import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from datetime import datetime, timezone


FEATURE = "043-private-connectivity-production"
FEATURE_PATH = "specs/" + FEATURE
DEFINITION = "547e398b615d08186719674774f379038740292e2472488010151a5f03bbba6d"
COORDINATOR = "opensoft/openxfactory"
FIXED_REPOSITORIES = {"C": COORDINATOR, "L": "opensoft/headscale-install", "I": "opensoft/xfactory-installer",
                      "H": "opensoft/openxsoft-hosted-services"}
SCOPE_FIELDS = frozenset("run candidate profile customer site network domain environment target region offering phase offer wave".split())
REF_FIELDS = frozenset(("repository", "commit", "path", "sha256"))
INSTANCE_TASKS = frozenset(f"T{i:03}" for i in range(57, 65))


class EvidenceError(ValueError):
    """An evidence obligation was not met."""


def require(condition, message):
    if not condition:
        raise EvidenceError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def decode(data):
    def reject(value):
        raise EvidenceError("non-finite JSON value: " + value)
    try:
        result = json.loads(data, object_pairs_hook=pairs, parse_constant=reject)
        def inspect(value):
            if isinstance(value, float):
                require(math.isfinite(value), "non-finite JSON number")
            elif isinstance(value, dict):
                for child in value.values(): inspect(child)
            elif isinstance(value, list):
                for child in value: inspect(child)
        inspect(result)
        return result
    except (ValueError, UnicodeError) as exc:
        raise EvidenceError("invalid JSON: " + str(exc)) from exc


def text(value, label):
    require(isinstance(value, str) and bool(value.strip()), label + " must be text")
    return value


def relative(value):
    text(value, "path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and "\\" not in value and ":" not in value
            and path.as_posix() == value and all(p not in (".", "..") for p in value.split("/")),
            "unsafe relative path")
    return value


def finite(value, label, minimum=0):
    require(type(value) in (int, float) and (type(value) is int or math.isfinite(value)) and value >= minimum,
            label + " must be finite and field-valid")
    return value


def timestamp(value):
    text(value, "timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        require(result.tzinfo is not None, "timestamp requires timezone")
        return result.astimezone(timezone.utc)
    except ValueError as exc:
        raise EvidenceError("invalid timestamp") from exc


def scope(value):
    require(isinstance(value, dict) and set(value) == SCOPE_FIELDS, "incomplete or unknown scope")
    for key, item in value.items():
        text(item, "scope " + key)
    return value


def reference(value):
    require(isinstance(value, dict) and set(value) == REF_FIELDS, "immutable reference required")
    text(value["repository"], "repository")
    require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value["repository"]), "invalid repository")
    require(isinstance(value["commit"], str) and re.fullmatch(r"[0-9a-f]{40}", value["commit"]), "exact commit required")
    require(isinstance(value["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", value["sha256"]), "exact SHA-256 required")
    relative(value["path"])
    return value


def canonical_origin(value):
    value = value.strip().removesuffix(".git").rstrip("/")
    for prefix in ("https://github.com/", "git@github.com:", "ssh://git@github.com/"):
        if value.startswith(prefix):
            value = value[len(prefix):]
            break
    require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value), "canonical GitHub origin required")
    return value.lower()


class GitStore:
    """Only fixed, local Git read operations; never execute an evidence command."""

    def __init__(self, roots):
        self.roots = {name.lower(): Path(root).resolve(strict=True) for name, root in roots.items()}
        for name, root in self.roots.items():
            require(canonical_origin(self.git(root, "config", "--get", "remote.origin.url").decode()) == name,
                    "owner root/origin mismatch")

    @staticmethod
    def git(root, *arguments):
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        result = subprocess.run(
            ["git", "--no-optional-locks", "--no-replace-objects", "--no-pager", "-C", str(root), *arguments],
            capture_output=True, check=False, env=environment,
        )
        require(result.returncode == 0, "local Git object or repository unavailable")
        return result.stdout

    def root(self, repository):
        require(repository.lower() in self.roots, "owner repository unavailable")
        return self.roots[repository.lower()]

    def blob(self, ref):
        reference(ref)
        root = self.root(ref["repository"])
        revision, path = ref["commit"], ref["path"]
        require(self.git(root, "cat-file", "-t", revision).strip() == b"commit", "reference is not a commit")
        # Walk every tree component; never follow a symlink or a gitlink.
        parts = path.split("/")
        for end in range(1, len(parts) + 1):
            name = "/".join(parts[:end])
            row = self.git(root, "ls-tree", "-z", revision, "--", name).split(b"\0")[0]
            header, separator, actual = row.partition(b"\t")
            require(separator and actual.decode() == name, "object path unavailable")
            mode = header.split()[0]
            require(mode in ((b"100644", b"100755") if end == len(parts) else (b"040000",)),
                    "symlink, gitlink or non-blob reference")
        data = self.git(root, "cat-file", "blob", revision + ":" + path)
        require(digest(data) == ref["sha256"], "immutable content digest mismatch")
        return data

    def changed(self, source):
        root = self.root(source["repository"])
        for field in ("base", "revision"):
            require(re.fullmatch(r"[0-9a-f]{40}", source[field]) is not None, "exact source commit required")
            require(self.git(root, "cat-file", "-t", source[field]).strip() == b"commit", "source is not commit")
        raw = self.git(root, "diff-tree", "-r", "--no-ext-diff", "--no-textconv", "--no-renames",
                       "--name-only", "-z", source["base"], source["revision"], "--")
        return {item.decode() for item in raw.split(b"\0") if item}


def load_contract(root):
    """Bind all 68 rows, command/file envelopes and 16 inputs to the T006 freeze."""
    feature = root / FEATURE_PATH
    contract = (feature / "contracts/task-evidence.md").read_text(encoding="utf-8")
    task_text = (feature / "tasks.md").read_text(encoding="utf-8")
    body, marker, footer = contract.partition("\n## T005 review freeze")
    require(marker, "missing reviewed definition freeze")
    inputs = {}
    for path, expected in re.findall(r"^\| ([^|]+?) \| ([0-9a-f]{64}) \|$", footer, re.M):
        relative(path)
        target = feature / path
        require(target.resolve().is_relative_to(feature.resolve()) and not target.is_symlink(), "unsafe contract input")
        data = body.encode() if path == "contracts/task-evidence.md" else target.read_bytes()
        inputs[path] = digest(data)
        require(inputs[path] == expected, "changed frozen contract input: " + path)
    rows = re.findall(r"^\| T\d{3} \|.*$", body, re.M)
    lines = re.findall(r"^- \[[ xX]\] T\d{3} .*$", task_text, re.M)
    frozen = {"inputs": inputs, "registry": rows,
              "tasks": [re.sub(r"^- \[[ xX]\]", "- [ ]", line) for line in lines]}
    require(len(inputs) == 16 and len(rows) == len(lines) == 68, "incomplete frozen registry")
    require(digest(json.dumps(frozen, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()) == DEFINITION,
            "unreviewed task/case/file/command definitions")
    tasks = {}
    for row, line in zip(rows, lines):
        task, owner, kind, deps, cases = [part.strip() for part in row.strip("|").split("|")]
        require(line.startswith("- [") and line[6:10] == task, "task order mismatch")
        files, command = line.split(" — files: ")[1].split(" — verify: ")
        tasks[task] = {"owner": owner, "class": kind, "dependencies": [] if deps == "none" else deps.split(", "),
                       "cases": cases.split(", "), "files": re.findall(r"`([^`]+)`", files),
                       "command": command.strip("`")}
    return tasks


class Verifier:
    def __init__(self, tasks, store, trust_reference, now=None):
        self.tasks, self.store = tasks, store
        self.now = now or datetime.now(timezone.utc)
        require(trust_reference["repository"].lower() == COORDINATOR, "trust must belong to coordinator")
        self.trust = decode(store.blob(reference(trust_reference)))
        t = self.trust
        require(t["schema"] == "043-reviewed-trust-v1" and t["feature"] == FEATURE and t["definition"] == DEFINITION,
                "wrong commissioning manifest")
        require(t["custodian"] == "Brett Heap", "uncommissioned evidence custodian")
        require(t["repositories"].get("C", "").lower() == COORDINATOR, "wrong coordinator identity")
        for alias, repository in t["repositories"].items():
            require(alias in "CLIHOD" and len(alias) == 1, "unknown owner alias")
            require(canonical_origin(repository) == repository.lower(), "invalid canonical repository")
            require(alias not in FIXED_REPOSITORIES or repository.lower() == FIXED_REPOSITORIES[alias], "wrong canonical component owner")
        require(store.blob(reference(t["review"])).strip(), "missing independent custody review")
        self.active, self.cache = set(), set()

    def read(self, ref):
        return decode(self.store.blob(reference(ref)))

    def validity(self, decision, expected_scope, start=None, end=None, historical=False, source_lifetime=False):
        """Source permissions may persist; execution channels remain time-bounded."""
        begin = timestamp(decision["valid_from"])
        expiry = (None if source_lifetime and expected_scope["phase"] == "source"
                  and decision["valid_until"] == "until-superseded"
                  else timestamp(decision["valid_until"]))
        require(expiry is None or begin < expiry, "invalid authority validity period")
        identity = decision["id"]
        closure = self.trust.get("completed_authorities", {}).get(identity)
        revoked = identity in self.trust["revoked_authorities"]
        if historical:
            require(start is not None and end is not None and begin <= start <= end
                    and (expiry is None or end < expiry),
                    "authority cannot retroactively authorize effects")
            if closure is not None:
                proof = self.read(closure)
                require(proof["kind"] == "authority-closure" and proof["authority_id"] == identity
                        and proof["scope"] == expected_scope and proof["disposition"] == "completed",
                        "invalid completion closure")
                text(proof["owner"], "actual closing owner")
                require(end <= timestamp(proof["closed_at"]) <= self.now, "closure does not cover original run")
            require(not revoked or closure is not None, "revoked authority without completion closure")
        else:
            require(not revoked and closure is None, "revoked or closed authority")
            require(begin <= self.now and (expiry is None or self.now < expiry), "authority expired or not current")
            if start is not None:
                require(begin <= start <= end and (expiry is None or end < expiry),
                        "later authority cannot authorize an earlier run")
        return begin, expiry

    def decision(self, ref, binding, kind, start=None, end=None, historical=False, source_lifetime=False):
        decision = self.read(ref)
        require(decision["kind"] == kind and decision["decision"] == "accepted", "required decision is not accepted")
        expected_scope = binding.get("decision_scopes", {}).get(kind, binding["scope"])
        require(scope(decision["scope"]) == expected_scope, "required decision scope mismatch")
        if (binding["scope"]["phase"] in ("staging", "production")
                and kind in ("C-03", "C-08", "C-09", "C-10", "C-11", "C-12", "C-13")):
            require(decision["scope"]["phase"] == binding["scope"]["phase"], "live decision phase mismatch")
        text(decision["owner"], "actual approving owner")
        self.validity(decision, expected_scope, start, end, historical, source_lifetime)
        return decision

    def authority(self, ref, binding, start=None, end=None, resume=False, historical=False):
        decision = self.read(ref)
        require(decision["decision"] == "accepted" and decision["scope"] == binding["scope"], "authority scope/status mismatch")
        text(decision["owner"], "actual decision owner")
        require(decision["roles"] == binding["roles"] and bool(decision["roles"]), "required named roles missing")
        mode = decision["mode"]
        require(mode in ("source", "managed-pull", "managed-push", "customer"), "unknown authority channel")
        if binding["scope"]["phase"] in ("staging", "production"):
            require(mode != "source", "source authority cannot authorize live evidence")
        source_lifetime = mode == "source" and binding["scope"]["phase"] == "source"
        self.validity(decision, binding["scope"], start, end, historical, source_lifetime)
        if mode.startswith("managed-"):
            self.decision(decision["request"], binding, "request", start, end, historical)
            field = "grant" if mode == "managed-push" else "reviewed_merge"
            self.decision(decision[field], binding, field, start, end, historical)
        if mode == "customer":
            self.decision(decision["consent"], binding, "consent", start, end, historical)
        required = binding["decisions"]
        require(set(decision["decisions"]) == set(required), "required gate decisions missing/extra")
        if resume:
            require("C-13" in required, "fresh resume decision missing")
        for item in required:
            self.decision(decision["decisions"][item], binding, item, start, end, historical,
                          source_lifetime=binding["scope"]["phase"] == "source")
        return decision

    def evidence_authority(self, binding, record):
        """Admit historical results without keeping an execution grant open."""
        require(record["authority"] == binding["authority"], "record authority mismatch")
        require(record.get("admission") == binding.get("admission"), "record admission mismatch")
        output = self.read(record["output"])
        start, end = timestamp(output["started_at"]), timestamp(output["ended_at"])
        require(start <= end <= self.now, "invalid/future actual run")
        historical = binding.get("admission") is not None
        if historical:
            admission = self.read(binding["admission"])
            require(admission["kind"] == "evidence-admission" and admission["decision"] == "accepted"
                    and scope(admission["scope"]) == binding["scope"], "invalid evidence admission scope/status")
            roles = binding["admission_roles"]
            require(isinstance(roles, list) and roles and all(isinstance(role, str) and role.strip() for role in roles)
                    and len(roles) == len(set(roles)) and admission["roles"] == roles, "required admission roles missing")
            text(admission["owner"], "actual admitting owner")
            begin, expiry = self.validity(admission, binding["scope"],
                                          source_lifetime=binding["scope"]["phase"] == "source")
            reviewed = timestamp(admission["reviewed_at"])
            require(end <= reviewed <= self.now and begin <= reviewed and (expiry is None or reviewed < expiry),
                    "invalid evidence review time")
            require(admission["authority"] == binding["authority"]
                    and admission["reviewed_output_sha256"] == reference(record["output"])["sha256"],
                    "admission is not for original authority/output")
        self.authority(binding["authority"], binding, start, end, historical=historical)
        return output, start, end, historical

    def binding(self, key):
        require(key in self.trust["bindings"], "uncommissioned task/instance")
        binding = self.trust["bindings"][key]
        task, separator, instance = key.partition("@")
        require(task in self.tasks, "unknown task")
        require(binding["task"] == task and binding["instance"] == (instance if separator else None), "binding identity mismatch")
        require(not separator or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", instance), "invalid opaque instance identity")
        require(not separator or task in INSTANCE_TASKS, "task has no child instances")
        scope(binding["scope"])
        roles = binding["roles"]
        require(isinstance(roles, list) and roles and all(isinstance(role, str) and role.strip() for role in roles)
                and len(roles) == len(set(roles)), "actual named owner roles required")
        number = int(task[1:])
        expected_phase = "staging" if 50 <= number <= 56 else "production" if 57 <= number <= 64 else "source"
        require(binding["scope"]["phase"] == expected_phase, "wrong task evidence phase")
        definition = self.tasks[task]
        require(binding["owner"] == definition["owner"] and binding["class"] == definition["class"], "owner/evidence class mismatch")
        require(set(binding["cases"]) == set(definition["cases"]), "required frozen cases changed")
        expected_deps = set(definition["dependencies"])
        require(set(binding["dependencies"]) == expected_deps, "required frozen dependencies changed")
        for predecessor, selected in binding["dependencies"].items():
            require(selected.split("@")[0] == predecessor, "substituted predecessor")
            if task in INSTANCE_TASKS and predecessor in INSTANCE_TASKS:
                require("@" in selected, "child cannot borrow an aggregate")
                old_scope = self.trust["bindings"][selected]["scope"]
                # Exact, separately reviewed transitions permit a canary-to-wave
                # scope expansion. Without one, target/customer identity is fixed.
                expected = binding.get("transitions", {}).get(predecessor, binding["scope"])
                require(old_scope == expected, "unapproved child scope transition")
            if 52 <= number <= 57:
                previous = self.trust["bindings"][selected]["scope"]
                require(previous["candidate"] == binding["scope"]["candidate"], "candidate changed across gate dependency")
                if number <= 56:
                    require(previous["run"] == binding["scope"]["run"], "mixed staging run")
        if task in INSTANCE_TASKS:
            require(separator and instance in self.trust["instances"].get(task, []), "missing commissioned instance")
            for predecessor in binding["dependencies"].values():
                if "@" in predecessor:
                    other = self.trust["bindings"][predecessor]["scope"]
                    for field in ("candidate", "profile", "offering", "phase", "offer"):
                        require(other[field] == binding["scope"][field], "foreign offering/candidate/profile predecessor")
            if task in ("T057", "T058"):
                require("C-09" in binding["decisions"], "canary requires C-09")
            if task == "T061":
                require("C-10" in binding["decisions"], "observation acceptance requires C-10")
            if task in ("T062", "T063", "T064"):
                require("C-11" in binding["decisions"], "offer requires C-11")
                if binding["scope"]["wave"] != "not-applicable":
                    require("C-12" in binding["decisions"], "wave requires C-12")
        if task == "T051":
            require(set(f"C-{i:02}" for i in range(3, 9)) <= set(binding["decisions"]), "Q1 decisions incomplete")
        if binding["scope"]["phase"] in ("staging", "production"):
            custody = self.trust.get("live_custody", {})
            require(custody.get("kind") == "protected" and custody.get("decision") == "C-08" and "C-08" in binding["decisions"],
                    "source-only custody cannot admit live evidence")
            require(binding["metrics"] and binding["observation"], "live numeric limits/observation missing")
        else:
            require(self.trust["custody"]["kind"] == "source-git", "unaccepted source custody")
        if int(task[1:]) < 10:
            require(binding["command"] == definition["command"], "bootstrap original command mismatch")
        else:
            require("verify-evidence.py" not in binding["command"], "self-verification is not an owner execution output")
        text(binding["command"], "approved owner command")
        return binding

    def source(self, value, binding):
        require(value == binding["source"], "tested revision or source mismatch")
        require(value["repository"].lower() == self.trust["repositories"][binding["owner"]].lower(), "source owner mismatch")
        allowed = binding["files"]
        require(allowed and len(allowed) == len(set(allowed)), "exact accepted file list required")
        envelopes = self.tasks[binding["task"]]["files"]
        for name in allowed:
            relative(name)
            require(any(name == p or (p.endswith("/") and name.startswith(p)) for p in envelopes), "file outside candidate envelope")
        changed = self.store.changed(value)
        require(changed <= set(allowed), "source diff exceeds exact accepted scope")
        if binding["task"] in ("T007", "T008", "T009"):
            require(changed, "bootstrap source implementation has no exact diff")

    def cases(self, output, binding):
        cases = output["cases"]
        require(isinstance(cases, list), "case array required")
        indexed = {}
        for case in cases:
            require(case["id"] not in indexed, "duplicate case")
            indexed[case["id"]] = case
            require(case["scope"] == binding["scope"] and case["source"] == binding["source"], "mixed case scope/source")
        require(set(indexed) == set(binding["cases"]), "missing/unknown frozen cases")
        for name, specs in binding["cases"].items():
            require(specs and len({s["id"] for s in specs}) == len(specs), "closed subchecks required")
            checks = indexed[name]["checks"]
            require(len(checks) == len(specs) and {c["id"] for c in checks} == {s["id"] for s in specs}, "missing/duplicate/unknown subchecks")
            actual = {c["id"]: c for c in checks}
            for spec in specs:
                check = actual[spec["id"]]
                kind = spec["kind"]
                require(kind in ("equal", "deny", "maximum", "minimum"), "unknown expected outcome type")
                if kind in ("maximum", "minimum"):
                    measured = finite(check["observed"], "measurement")
                    limit = finite(spec["expected"], "approved limit")
                    text(spec["unit"], "measurement unit")
                    text(spec["event"], "measurement event")
                    require(check["unit"] == spec["unit"] and check["event"] == spec["event"], "measurement units/event mismatch")
                    anchor = timestamp(output["events"][check["event"]])
                    require(timestamp(output["started_at"]) <= anchor <= timestamp(output["ended_at"]), "measurement event outside run")
                    require(measured <= limit if kind == "maximum" else measured >= limit, "approved numeric limit exceeded")
                else:
                    require(type(check["observed"]) is type(spec["expected"]) and check["observed"] == spec["expected"], "expected/observed mismatch")
                if kind == "deny":
                    require(spec["expected"] == "denied", "denial must be observed")
                    control = actual.get(spec["control"])
                    require(control is not None and control["observed"] == "allowed", "legitimate positive control missing/failed")
                if "neighbor" in spec:
                    require(spec["neighbor"] in actual and actual[spec["neighbor"]]["observed"] == "available", "authorized neighbor missing/failed")

    def observations(self, output, binding):
        require(set(output["metrics"]) == set(binding["metrics"]), "numeric metric inventory mismatch")
        for name, limits in binding["metrics"].items():
            measurement = output["metrics"][name]
            value = finite(measurement["value"], name)
            lo, hi = finite(limits["minimum"], "minimum"), finite(limits["maximum"], "maximum")
            text(limits["unit"], "metric unit")
            text(limits["event"], "metric event")
            require(lo <= value <= hi, "metric outside approved bounds")
            require(measurement["unit"] == limits["unit"] and measurement["event"] == limits["event"], "metric unit/event mismatch")
            anchor = timestamp(output["events"][limits["event"]])
            require(timestamp(output["started_at"]) <= anchor <= timestamp(output["ended_at"]), "metric event outside actual run")
        observation = binding["observation"]
        if observation is None:
            require(output["coverage"] is None, "uncommissioned observation window")
            return
        coverage = output["coverage"]
        require(coverage["window"] == observation["window"], "wrong observation window")
        start, end = map(timestamp, coverage["window"])
        require(timestamp(output["started_at"]) <= start < end <= timestamp(output["ended_at"]), "observation outside run")
        max_gap = finite(observation["max_gap_seconds"], "gap")
        minimum = finite(observation["minimum_observed_seconds"], "minimum observed", minimum=0.000001)
        cursor, observed = start, 0
        require(coverage["intervals"], "no monitoring coverage")
        for interval in coverage["intervals"]:
            begin, finish = map(timestamp, interval)
            require(cursor <= begin < finish <= end, "overlapping/out-of-window monitoring")
            require((begin - cursor).total_seconds() <= max_gap, "monitoring gap exceeds approved limit")
            observed += (finish - begin).total_seconds()
            cursor = finish
        require((end - cursor).total_seconds() <= max_gap and observed >= minimum, "omitted monitoring time is not healthy observation")

    def ci(self, output, binding):
        required = binding["ci"]
        require(isinstance(required, dict), "closed required CI inventory")
        if self.tasks[binding["task"]]["class"].startswith("CI-"):
            require(required, "required exact-head CI collection missing")
        if binding["task"] == "T010":
            require({FEATURE_PATH + "/tests/test_evidence.py", FEATURE_PATH + "/tests/test_evidence_pins.py"} <= set(required), "feature suites not explicitly collected")
        actual = output["ci"]
        require(set(actual) == set(required), "missing/unknown CI suites")
        for suite, count in required.items():
            run = actual[suite]
            require(type(count) is int and count > 0, "positive collected count required")
            require(run["repository"] == binding["source"]["repository"] and run["revision"] == binding["source"]["revision"], "CI is not exact owner/head")
            require(run["conclusion"] == "success" and run["required"] is True and run["collected"] == run["passed"] == count
                    and type(run["collected"]) is int and type(run["passed"]) is int
                    and type(run["skipped"]) is int and run["skipped"] == 0, "missing/failed/uncollected/waived CI")
            for field in ("run_id", "job_id"):
                require(type(run[field]) is int and run[field] > 0, "actual GitHub run/job identity required")

    def verify(self, key, supplied=None):
        if key in INSTANCE_TASKS:
            aggregate_ref = reference(self.trust["aggregates"][key])
            self.aggregate(key, self.store.blob(aggregate_ref) if supplied is None else supplied)
            return
        require(key not in self.active, "cyclic evidence dependency")
        binding = self.binding(key)
        ref = reference(binding["record"])
        data = self.store.blob(ref)
        if supplied is not None:
            require(supplied == data, "receipt differs from independently reviewed immutable reference")
        record = decode(data)
        # Current admission and original execution validity are checked even on cache hits.
        output, start, end, historical = self.evidence_authority(binding, record)
        if key in self.cache:
            return
        self.active.add(key)
        task = binding["task"]
        bootstrap = int(task[1:]) < 10
        require(record["schema"] == ("043-bootstrap-import-v1" if bootstrap else "043-task-evidence-v1"), "wrong evidence/import kind")
        if bootstrap:
            require(not re.fullmatch(r"T00[1-9]\.json", PurePosixPath(ref["path"]).name), "fabricated bootstrap task receipt")
        else:
            require(ref["path"] in binding["files"] and ref["repository"].lower() == self.trust["repositories"][binding["owner"]].lower(), "receipt outside exact accepted owner scope")
        for field, expected in (("task", task), ("instance", binding["instance"]), ("owner", binding["owner"]),
                                ("evidence_class", binding["class"]), ("scope", binding["scope"]), ("command", binding["command"]),
                                ("authority", binding["authority"]), ("history", binding["history"])):
            require(record[field] == expected, "record " + field + " mismatch")
        text(record["attempt"], "attempt identity")
        require(record["verdict"] == "pass", "failed/blocked evidence cannot satisfy a dependency")
        self.source(record["source"], binding)
        require(record["artifacts"] == binding["artifacts"] and record["artifacts"], "original source/governance artifacts missing")
        artifact_data = {a["path"]: self.store.blob(reference(a)) for a in record["artifacts"]}
        for artifact in record["artifacts"]:
            require(artifact["repository"] == record["source"]["repository"] and artifact["commit"] == record["source"]["revision"], "artifact is not tested source")
        if bootstrap:
            required_artifacts = set()
            for envelope in self.tasks[task]["files"]:
                if envelope.endswith("/"):
                    if envelope.startswith("openspec/"):
                        required_artifacts.update((envelope + "proposal.md", envelope + ".openspec.yaml"))
                else:
                    required_artifacts.add(envelope)
            require(required_artifacts <= set(artifact_data), "original bootstrap source/governance artifact missing")
        if task == "T002":
            baseline_path = FEATURE_PATH + "/evidence/baseline.json"
            require(baseline_path in artifact_data, "original historical baseline missing")
            baseline = decode(artifact_data[baseline_path])
            require(baseline["authorizes_production"] is False and baseline["evidence_class"] == "historical-lab", "lab cannot grant production authority")
            old = "specs/040-private-connectivity/evidence/T021.json"
            require(old in artifact_data and digest(artifact_data[old]) == baseline["evidence_sha256"], "historical content identity mismatch")
        if task == "T006":
            base = "openspec/changes/commission-private-connectivity-production-evidence/"
            require(b"Status: ratified" in artifact_data.get(base + "proposal.md", b"")
                    and b"Ratified:" in artifact_data.get(base + "review/ratification.md", b"")
                    and b"approved_by:" in artifact_data.get(base + ".openspec.yaml", b""), "actual E ratification/source provenance missing")
        for field in ("task", "instance", "scope", "source", "command"):
            require(output[field] == record[field], "actual output " + field + " mismatch")
        require(type(output["exit_code"]) is int and output["exit_code"] == 0, "missing/nonzero owner command result")
        self.cases(output, binding)
        self.observations(output, binding)
        self.ci(output, binding)
        require(record["dependencies"] == {dep: (self.trust["aggregates"][selected] if selected in INSTANCE_TASKS else self.trust["bindings"][selected]["record"])
                                           for dep, selected in binding["dependencies"].items()}, "immutable dependency substitution")
        for selected in binding["dependencies"].values():
            self.verify(selected)
        # Every child still depends on the complete program Q2; no partial union.
        if task in INSTANCE_TASKS:
            self.verify("T056")
            if binding["scope"]["offering"] in ("local-managed", "hosted-domain"):
                eligibility = binding["eligibility"]
                eligible = self.binding(eligibility)
                require(eligible["scope"]["offering"] == "hosted-headscale", "managed service eligibility missing")
                for field in SCOPE_FIELDS - {"offering", "domain", "profile"}:
                    require(eligible["scope"][field] == binding["scope"][field], "managed service is not eligible in this phase/scope")
                require(eligible["task"] == task, "managed service eligibility phase mismatch")
                self.verify(eligibility)
            if task == "T063" and binding["scope"]["wave"] != "not-applicable":
                offer = self.binding(binding["offer_admission"])
                require(offer["task"] == "T063" and offer["scope"]["wave"] == "not-applicable", "wave requires prior offer admission")
                for field in ("offer", "offering", "candidate", "profile", "phase"):
                    require(offer["scope"][field] == binding["scope"][field], "wrong corresponding offer admission")
                self.verify(binding["offer_admission"])
        for prior in record["history"]:
            failed = self.read(prior)
            require(failed["verdict"] in ("fail", "blocked") and failed["task"] == task
                    and failed["scope"] == record["scope"] and failed["attempt"] != record["attempt"], "failed/blocked attempt history lost or substituted")
        if record["history"]:
            require(record["remediation"] == binding["remediation"], "reviewed remediation missing")
            resumed = self.authority(record["remediation"], binding, start, end, resume=True, historical=historical)
            resume = self.read(resumed["decisions"]["C-13"])
            require(resume["reruns"] == binding["resume_outputs"] and record["output"] in resume["reruns"], "reviewed affected rerun outputs missing")
            for rerun in resume["reruns"]:
                self.store.blob(reference(rerun))
        require(record["incidents"] == binding["incidents"], "incident history omitted")
        for incident in record["incidents"]:
            closed = self.decision(incident, binding, "incident-closure")
            require(closed["reruns"], "affected/adjacent reruns missing")
            for rerun in closed["reruns"]:
                self.store.blob(reference(rerun))
        self.active.remove(key)
        self.cache.add(key)

    def aggregate(self, task, data):
        require(task in INSTANCE_TASKS, "task has no aggregate instances")
        record = decode(data)
        instances = self.trust["instances"].get(task, [])
        require(instances and len(instances) == len(set(instances)), "commissioned instance inventory required")
        ref = reference(self.trust["aggregates"][task])
        owner = self.tasks[task]["owner"]
        prefix = FEATURE_PATH + "/evidence/" if owner == "C" else "evidence/private-connectivity-production/"
        require(ref["path"] == prefix + task + ".json" and ref["repository"].lower() == self.trust["repositories"][owner].lower(), "aggregate outside accepted owner scope")
        require(data == self.store.blob(ref), "aggregate differs from reviewed immutable reference")
        expected = {instance: self.trust["bindings"][task + "@" + instance]["record"] for instance in instances}
        body = {key: value for key, value in record.items() if key != "pin_inventory"}
        require(body == {"schema": "043-instance-aggregate-v1", "task": task, "children": expected}, "missing/foreign/duplicate aggregate child")
        for instance in instances:
            self.verify(task + "@" + instance)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True)
    parser.add_argument("--instance")
    parser.add_argument("record", type=Path)
    arguments = parser.parse_args(argv)
    try:
        root = Path(__file__).resolve().parents[2]
        tasks = load_contract(root)
        require(arguments.task in tasks, "unknown task")
        anchor = os.environ.get("PC_EVIDENCE_TRUST", "")
        revision, separator, path = anchor.partition(":")
        require(separator, "independently approved PC_EVIDENCE_TRUST is required")
        roots = decode(os.environ.get("PC_EVIDENCE_ROOTS", "{}"))
        require(isinstance(roots, dict) and COORDINATOR not in {k.lower() for k in roots}, "coordinator root cannot be overridden")
        roots[COORDINATOR] = str(root)
        store = GitStore(roots)
        trust_ref = {"repository": COORDINATOR, "commit": revision, "path": path,
                     "sha256": os.environ.get("PC_EVIDENCE_TRUST_SHA256", "")}
        verifier = Verifier(tasks, store, trust_ref)
        owner = tasks[arguments.task]["owner"]
        owner_root = store.root(verifier.trust["repositories"][owner])
        record_path = arguments.record.absolute()
        require(record_path.resolve().is_relative_to(owner_root), "record outside accepted owner root")
        relative_path = record_path.relative_to(owner_root)
        require(all(not p.is_symlink() for p in (owner_root.joinpath(*relative_path.parts[:i]) for i in range(1, len(relative_path.parts) + 1))), "receipt symlink forbidden")
        data = record_path.read_bytes()
        if arguments.task in INSTANCE_TASKS and arguments.instance is None:
            require(relative_path.as_posix() == verifier.trust["aggregates"][arguments.task]["path"], "wrong accepted aggregate path")
            verifier.aggregate(arguments.task, data)
        else:
            key = arguments.task + ("@" + arguments.instance if arguments.instance else "")
            binding = verifier.binding(key)
            require(relative_path.as_posix() == binding["record"]["path"], "wrong accepted receipt path")
            if arguments.instance:
                prefix = (FEATURE_PATH + "/evidence/" if owner == "C" else "evidence/private-connectivity-production/") + "instances/" + arguments.task + "/"
                require(relative_path.as_posix().startswith(prefix), "child outside accepted instance area")
            verifier.verify(key, data)
        print(arguments.task + ": structurally verified; owner/gate acceptance remains independent")
        return 0
    except (EvidenceError, OSError, KeyError, TypeError, AttributeError, RecursionError) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
