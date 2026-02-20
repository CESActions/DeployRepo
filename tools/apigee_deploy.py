#!/usr/bin/env python3
import argparse, json, os, subprocess, requests

def token():
    return subprocess.check_output(["gcloud","auth","print-access-token"], text=True).strip()

def import_proxy(org, name, zip_path, access_token):
    with open(zip_path, "rb") as f:
        r = requests.post(
            f"https://apigee.googleapis.com/v1/organizations/{org}/apis",
            params={"action":"import", "name": name},
            headers={"Authorization": f"Bearer {access_token}"},
            files={"file": (os.path.basename(zip_path), f, "application/octet-stream")}
        )
    r.raise_for_status()
    return r.json()["revision"]

def deploy(org, env, name, rev, access_token, base_path=None):
    r = requests.post(
        f"https://apigee.googleapis.com/v1/organizations/{org}/environments/{env}/apis/{name}/revisions/{rev}/deployments",
        params={"override":"true"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    r.raise_for_status()
    if base_path:
        rb = requests.post(
            f"https://apigee.googleapis.com/v1/organizations/{org}/environments/{env}/apis/{name}/revisions/{rev}/deployments:setBasePath",
            headers={"Authorization": f"Bearer {access_token}", "Content-Type":"application/json"},
            data=json.dumps({"basePath": base_path}),
        )
        rb.raise_for_status()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--org", required=True)
    p.add_argument("--env", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--zip",  required=True)
    p.add_argument("--base-path", default="")
    args = p.parse_args()

    t = token()
    rev = import_proxy(args.org, args.name, args.zip, t)
    deploy(args.org, args.env, args.name, rev, t, base_path=args.base_path)
    print(f"Deployed {args.name} rev {rev} to {args.env}")
