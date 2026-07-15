#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    args = ap.parse_args()
    p = Path(args.path)
    try:
        data = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1
    required = ["primaryIndustryId","subindustry","audience","businessObjective","experienceArchetypes","contentPriorities","riskMode","motionIntensity"]
    missing = [x for x in required if x not in data]
    if missing:
        print("ERROR missing: " + ", ".join(missing), file=sys.stderr); return 1
    skill = Path(__file__).resolve().parents[1]
    profiles = json.loads((skill / "references" / "industry-profiles.json").read_text(encoding="utf-8"))
    ids = {x["id"] for x in profiles["industries"]}
    if data["primaryIndustryId"] not in ids:
        print(f"ERROR unknown primaryIndustryId: {data['primaryIndustryId']}", file=sys.stderr); return 1
    secondaries = data.get("secondaryIndustryIds", [])
    unknown = [x for x in secondaries if x not in ids]
    if unknown:
        print("ERROR unknown secondaryIndustryIds: " + ", ".join(unknown), file=sys.stderr); return 1
    if len(secondaries) > 2:
        print("ERROR at most two secondary industries are allowed", file=sys.stderr); return 1
    intensity = data["motionIntensity"]
    if not isinstance(intensity, (int,float)) or not 0 <= intensity <= 10:
        print("ERROR motionIntensity must be 0..10", file=sys.stderr); return 1
    print("OK: industry profile validated")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
