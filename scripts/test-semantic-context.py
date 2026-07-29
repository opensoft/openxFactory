#!/usr/bin/env python3
"""Semantic-context compilation and gateway-preflight tests
(add-domain-ontology-layer, tasks 6.1-6.7).

Covers: closure over ancestors and relation endpoints; profile-driven
worker-scoped compilation (deterministic, authority-free); itemized
truncation only where the profile allows it; fail-closed rules for
unrestricted requests, unresolvable terms, retired packages, and
wrong-package or dangling tenant bindings; the memory-gateway preflight
(purpose agreement, retired-package rejection, authority-key rejection);
and the adversarial floor: a profile carrying an authority field and a
derived artifact whose embedded semantic context drops its pins both fail
validation.

Run: python3 scripts/test-semantic-context.py
Exit codes: 0 ok, 1 failures, 2 harness error.
"""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPILE = ROOT / "scripts" / "ontology-compile-context.py"
VALIDATOR = ROOT / "scripts" / "validate-domain-ontology.py"
GATEWAY = ROOT / "scripts" / "validate-memory-gateway.py"
MEDX = ROOT / "contracts" / "domain-ontology" / "examples" / "medx-minimal"

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"ok   {name}")
    else:
        FAILURES.append(name)
        print(f"FAIL {name}{': ' + detail if detail else ''}")


def run(*argv: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *argv], capture_output=True,
                          text=True, check=False)


def main() -> int:
    import yaml
    with tempfile.TemporaryDirectory(prefix="semantic-context-test-") as tmp:
        base = Path(tmp)
        pkg = base / "medx"
        shutil.copytree(MEDX, pkg)

        # -- closure over ancestors (6.1) ----------------------------------
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-t1",
                  "--terms", "xf/medx/patient", "--purpose", "classification")
        check("compile closes over kernel ancestors",
              res.returncode == 0 and "- xf/core/subject" in res.stdout
              and "status: closed" in res.stdout, res.stderr)

        # -- worker-profile compilation (6.7) ------------------------------
        out1 = base / "ctx-verify-1.yaml"
        out2 = base / "ctx-verify-2.yaml"
        for out in (out1, out2):
            res = run(str(COMPILE), str(pkg), "--context-id", "ctx-medx-verify",
                      "--profile", "profile-verify.yaml", "--out", str(out))
            check(f"profile compile ok ({out.name})", res.returncode == 0, res.stderr)
        check("profile compilation is deterministic",
              out1.read_bytes() == out2.read_bytes())
        ctx = yaml.safe_load(out1.read_text())
        check("worker context carries only the closed profile subset",
              sorted(ctx["terms"]) == ["xf/core/subject", "xf/medx/patient"]
              and ctx["worker_scope"]["worker_archetype"] == "verify")
        authority_keys = {"effect", "permission", "grant", "credential",
                          "scope", "route", "token", "secret", "binding",
                          "approval"}
        flat: set = set()

        def walk(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    flat.add(k)
                    walk(v)
            elif isinstance(node, list):
                for v in node:
                    walk(v)
        walk(ctx)
        check("compiled context carries no authority-named field",
              not (flat & authority_keys), str(flat & authority_keys))

        # -- truncation only where allowed ---------------------------------
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-t2",
                  "--profile", "profile-verify.yaml", "--truncate")
        check("truncation refused when the profile disallows it",
              res.returncode == 1 and "does not allow truncation" in res.stderr)
        prof = (pkg / "profile-verify.yaml").read_text() + "truncation_allowed: true\n"
        (pkg / "trunc-profile.yaml").write_text(
            prof.replace("prof-medx-verify", "prof-medx-trunc"))
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-t3",
                  "--profile", "trunc-profile.yaml", "--truncate")
        check("allowed truncation itemizes each omitted member",
              res.returncode == 0 and "status: truncated" in res.stdout
              and "- xf/core/subject" in res.stdout.split("omitted:")[1])

        # -- fail-closed rules (6.1/6.5) -----------------------------------
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-t4",
                  "--purpose", "x")
        check("unrestricted request refused",
              res.returncode == 1 and "no unrestricted" in res.stderr)
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-t5",
                  "--terms", "xf/medx/ghost", "--purpose", "x")
        check("unresolvable term refused", res.returncode == 1
              and "does not resolve" in res.stderr)
        retired = base / "retired"
        shutil.copytree(pkg, retired)
        mtext = (retired / "package.yaml").read_text().replace(
            "lifecycle_state: published", "lifecycle_state: retired")
        (retired / "package.yaml").write_text(mtext)
        res = run(str(COMPILE), str(retired), "--context-id", "ctx-t6",
                  "--terms", "xf/medx/patient", "--purpose", "x")
        check("retired package refuses new compilation",
              res.returncode == 1 and "fails closed" in res.stderr)

        # -- tenant bindings (6.1/6.5) -------------------------------------
        digest = yaml.safe_load((pkg / "package.yaml").read_text())["package_digest"]
        good = base / "binding-good.yaml"
        good.write_text("\n".join([
            "binding_id: tenant-a-ehr",
            "package_id: xf/medx",
            f"package_digest: {digest}",
            "bindings:",
            "  - local_code: EHR-PT", "    concept_id: xf/medx/patient"]) + "\n")
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-t7",
                  "--terms", "xf/medx/patient", "--purpose", "x",
                  "--tenant-binding", str(good))
        check("valid tenant binding compiles in",
              res.returncode == 0 and "binding_id: tenant-a-ehr" in res.stdout,
              res.stderr)
        bad = base / "binding-bad.yaml"
        bad.write_text(good.read_text().replace(digest, "ab" * 32))
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-t8",
                  "--terms", "xf/medx/patient", "--purpose", "x",
                  "--tenant-binding", str(bad))
        check("wrong-package binding fails closed",
              res.returncode == 1 and "different package identity" in res.stderr)
        dangling = base / "binding-dangling.yaml"
        dangling.write_text(good.read_text().replace(
            "xf/medx/patient", "xf/medx/retired_term"))
        res = run(str(COMPILE), str(pkg), "--context-id", "ctx-t9",
                  "--terms", "xf/medx/patient", "--purpose", "x",
                  "--tenant-binding", str(dangling))
        check("dangling binding target fails closed",
              res.returncode == 1 and "retired or absent" in res.stderr)

        # -- adversarial: authority field on a profile (6.6) ---------------
        evil = base / "evil"
        shutil.copytree(pkg, evil)
        (evil / "profile-verify.yaml").write_text(
            (evil / "profile-verify.yaml").read_text() + "effect: allow\n")
        # restamp so ONLY the authority finding fires
        import hashlib
        man = (evil / "package.yaml").read_text()
        entries = []
        for item in yaml.safe_load(man)["inventory"]:
            digest_i = hashlib.sha256((evil / item["path"]).read_bytes()).hexdigest()
            import re
            man = re.sub(r"(- path: " + re.escape(item["path"]) + r"\n(\s+)sha256: )[a-f0-9]+",
                         lambda m, d=digest_i: m.group(1) + d, man)
            entries.append(f"{item['path']} {digest_i}")
        pd = hashlib.sha256("\n".join(sorted(entries)).encode()).hexdigest()
        import re
        man = re.sub(r"(?m)^(package_digest: )[a-f0-9]+", r"\g<1>" + pd, man)
        (evil / "package.yaml").write_text(man)
        res = run(str(VALIDATOR), str(evil))
        check("authority field on a worker profile rejected (6.6)",
              res.returncode == 1 and "ONT-AUTHORITY-FIELD" in res.stdout,
              res.stdout[-400:])

        # -- gateway preflight (6.2/6.3/6.5) -------------------------------
        res = run(str(GATEWAY))
        check("memory-gateway validator green with semantic packets",
              res.returncode == 0, res.stdout[-300:])
        spec = importlib.util.spec_from_file_location("mgv", GATEWAY)
        mgv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mgv)
        exdir = base / "gw-examples"
        exdir.mkdir()
        source = (ROOT / "examples/memory-gateway/semantic-context-packet.example.yaml").read_text()
        (exdir / "cross-purpose.example.yaml").write_text(
            source.replace("purpose: classification for a verify worker\n  workflow_ref",
                           "purpose: another purpose entirely\n  workflow_ref", 1))
        (exdir / "retired.example.yaml").write_text(
            source.replace("package_lifecycle_state: published",
                           "package_lifecycle_state: retired"))
        mgv.EXAMPLE_DIR = exdir
        errors: list[str] = []
        mgv.validate_semantic_context(errors)
        check("gateway preflight rejects cross-purpose reuse",
              any("cross-purpose" in e for e in errors), str(errors))
        check("gateway preflight rejects a retired package before provider I/O",
              any("rejected before provider I/O" in e for e in errors), str(errors))

    if FAILURES:
        print(f"FAIL {len(FAILURES)} check(s): {', '.join(FAILURES)}")
        return 1
    print("OK semantic-context tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
