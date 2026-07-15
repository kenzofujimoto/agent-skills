#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

STOP = {"the","and","for","with","site","website","build","create","project","a","an","to","of","de","do","da","para","com","um","uma","site"}

def tokens(text: str) -> set[str]:
    return {x for x in re.findall(r"[a-z0-9]+", text.lower()) if len(x) > 1 and x not in STOP}

def main() -> int:
    ap = argparse.ArgumentParser(description="Rank motion-site-builder industry profiles for a project brief.")
    ap.add_argument("brief", nargs="+", help="Project brief text")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    skill = Path(__file__).resolve().parents[1]
    data = json.loads((skill / "references" / "industry-profiles.json").read_text(encoding="utf-8"))
    query = tokens(" ".join(args.brief))
    ranked = []
    for item in data["industries"]:
        weighted = []
        weighted += [(x, 5) for x in item.get("keywords", [])]
        weighted += [(x, 3) for x in item.get("subindustries", [])]
        weighted += [(x, 2) for x in item.get("archetypes", [])]
        weighted += [(item.get("label_en", ""), 4), (item.get("label_pt", ""), 4)]
        score = 0
        matches = []
        for phrase, weight in weighted:
            ptoks = tokens(str(phrase))
            overlap = query & ptoks
            if overlap:
                inc = weight * len(overlap)
                score += inc
                matches.extend(sorted(overlap))
        if score:
            ranked.append({"id":item["id"],"label":item["label_pt"],"score":score,"matches":sorted(set(matches)),"risk":item["risk"],"motionIntensityRange":item["intensity"]})
    ranked.sort(key=lambda x:(-x["score"], x["id"]))
    result = ranked[:max(1,args.top)]
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for r in result:
            print(f"{r['score']:>3}  {r['id']:<30} {r['label']}  matches={','.join(r['matches'])}")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
