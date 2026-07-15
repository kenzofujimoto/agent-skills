#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser(description="List curated web references by industry.")
    ap.add_argument("industry", nargs="?", default="")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    skill = Path(__file__).resolve().parents[1]
    data = json.loads((skill / "references" / "industry-reference-catalog.json").read_text(encoding="utf-8"))
    q = args.industry.lower().strip()
    rows = [r for r in data["references"] if not q or q in r["industryId"].lower() or q in r["industry"].lower()]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for r in rows:
            print(f"[{r['industryId']}] {r['name']} — {r['url']} ({r['benchmarkType']})")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
