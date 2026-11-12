"""Generate/check explicit per-record mixed-repository pilot pin ownership."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess

TOKEN=re.compile(r"(?<![0-9a-zA-Z])[0-9a-f]{40}(?![0-9a-zA-Z])")

OWNERS={"opensoft/openxFactory","opensoft/Headscale-Install","opensoft/openXsoft-Hosted-Services","opensoft/xFactory-Installer","opensoft/opsXfactory","codeXfactory/codexFactory","juanfont/headscale"}

def validate_stored_inventory(value,local_commits):
    body={k:v for k,v in value.items() if k!="pin_inventory"}
    tokens=set(TOKEN.findall(json.dumps(body,sort_keys=True)))
    rows=value.get("pin_inventory")
    if not isinstance(rows,list):raise ValueError("missing pin inventory")
    by_pin={}
    for row in rows:
        repository=row.get("repository")
        key="openxfactory_commit" if repository=="opensoft/openxFactory" else "foreign_commit"
        if repository not in OWNERS or set(row)!={"repository",key}:raise ValueError("invalid pin owner declaration")
        pin=row[key]
        if not isinstance(pin,str) or not TOKEN.fullmatch(pin) or pin in by_pin:raise ValueError("invalid or duplicate inventory pin")
        if pin in local_commits and repository!="opensoft/openxFactory":raise ValueError("local commit cannot be classified as foreign: "+pin)
        by_pin[pin]=repository
    if set(by_pin)!=tokens:raise ValueError("inventory must exactly cover record reference tokens")
    for repository,pin in re.findall(r"https://github\.com/([^/\s]+/[^/\s]+)/(?:blob|commit)/([a-f0-9]{40})",json.dumps(body)):
        if by_pin[pin].casefold()!=repository.casefold():raise ValueError("reference URL and declared owner disagree")

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
            validate_stored_inventory(value,resolved["opensoft/openxFactory"])
            if value.get("pin_inventory")!=rows:raise ValueError("stale pin ownership inventory: "+path.name)
        else:
            value["pin_inventory"]=rows
            validate_stored_inventory(value,resolved["opensoft/openxFactory"])
            path.write_text(json.dumps(value,indent=2)+"\n")
    print("PASS: explicit owner inventories match all feature evidence commit tokens")

if __name__=="__main__":main()
