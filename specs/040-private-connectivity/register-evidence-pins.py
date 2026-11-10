"""Generate/check explicit per-record mixed-repository pilot pin ownership."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

TOKEN=re.compile(r"(?<![0-9a-zA-Z])[0-9a-f]{40}(?![0-9a-zA-Z])")

def inventory(value,owners):
    value={k:v for k,v in value.items() if k!="pin_inventory"}
    tokens=sorted(set(TOKEN.findall(json.dumps(value,sort_keys=True))))
    rows=[]
    for token in tokens:
        matches=[]
        for repository,commits in owners.items():
            if token in commits:matches.append(repository)
        if len(matches)!=1:raise ValueError("pin needs exactly one verified repository owner: "+token+" "+repr(matches))
        repository=matches[0]
        key="openxfactory_commit" if repository=="opensoft/openxFactory" else "foreign_commit"
        rows.append({"repository":repository,key:token})
    return rows

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner",action="append",required=True,metavar="REPOSITORY=CHECKOUT")
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args();owners={}
    for entry in args.owner:
        name,path=entry.split("=",1)
        if name in owners:parser.error("duplicate owner")
        owners[name]=Path(path).resolve()
    if "opensoft/openxFactory" not in owners:parser.error("local repository owner required")
    root=Path(__file__).resolve().parent/"evidence"
    values={path:json.loads(path.read_text()) for path in sorted(root.glob("*.json"))}
    tokens=sorted({token for value in values.values() for token in TOKEN.findall(json.dumps({k:v for k,v in value.items() if k!="pin_inventory"}))})
    resolved={}
    for repository,checkout in owners.items():
        result=subprocess.run(["git","cat-file","--batch-check=%(objectname) %(objecttype)"],cwd=checkout,input="\n".join(tokens)+"\n",capture_output=True,text=True,timeout=30,check=True,env={**os.environ,"GIT_NO_LAZY_FETCH":"1"})
        resolved[repository]={line.split()[0] for line in result.stdout.splitlines() if line.endswith(" commit")}
    for path,value in values.items():
        rows=inventory(value,resolved)
        if args.check:
            if value.get("pin_inventory")!=rows:raise ValueError("stale pin ownership inventory: "+path.name)
        else:
            value["pin_inventory"]=rows;path.write_text(json.dumps(value,indent=2)+"\n")
    print("PASS: explicit owner inventories match all feature evidence commit tokens")

if __name__=="__main__":main()
