#!/usr/bin/env python3
"""Post-scrape off-niche triage for Kostenschoorsteenveger.nl.

Closes clear junk only (coaches-only, lifestyle, non-psych businesses).
Keeps schoorsteenvegers / praktijken / psychotherapie / GZ / EMDR / etc.

Rule: bij twijfel → leave actief (manual review); only auto-close true junk.

Updates both:
  migration/scrape/normalized/*.json
  src/content/schoorsteenvegers/*.json

Writes migration/OFF_NICHE_PASS.json summary.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NORM = ROOT / "scrape" / "normalized"
CONTENT = ROOT.parent / "src" / "content" / "schoorsteenvegers"
REPORT = ROOT / "OFF_NICHE_PASS.json"

PSYCH_OK = re.compile(
    r"psycholog|psychotherapie|psychotherapeut|psychiatr|"
    r"\bemdr\b|ggz|gz[- ]?psych|klinisch psych|neuropsych|"
    r"relatietherapie|gezinstherapie|kinderpsych|jeugdpsych|"
    r"psychosocia|psychomotor|psycho[- ]?sociaal|"
    r"gedragstherapie|cognitieve therapie|\bcgt\b|schema.?therapie|"
    r"basis.?ggz|specialistische.?ggz|eerstelijns.?psych|"
    r"kindertherapie|jeugdtherapie|\bpsychother",
    re.I,
)

# Clear junk — only close when NO psych signal.
JUNK = re.compile(
    r"schilder|steiger|hovenier|aannemer|installat|autobedrijf|garage|kapsalon|"
    r"restaurant|catering|makelaar|notaris|advocaat|tandarts|"
    r"fysiotherapie|fysiotherapeut|dierenarts|homeopathie|"
    r"paardencoaching|hondencoach|astrologie|tarot|spirituele psych|"
    r"gitaarles|muziekles|schildersbedrijf|gastouder|kinderdagverblijf|"
    r"\bbso\b|fitness|sportschool|personal\s*train|"
    r"dierenarts|veterinar",
    re.I,
)

COACH_ONLY = re.compile(
    r"(^|[^a-z])(life\s*)?coach(ing)?([^a-z]|$)|"
    r"lifestyle\s*coach|loopbaancoach|business\s*coach|"
    r"mindfulness\s*(trainer|coach)|yoga\s*(studio|teacher)|"
    r"nlp\s*coach|opstellingen\s*coach",
    re.I,
)

# Extra name-only junk patterns (slug/naam)
NAME_JUNK = re.compile(
    r"dierenarts|fysiotherapie|gastouder|schilder|"
    r"paardencoaching|astrologie|gitaar|muziekles|"
    r"performance.?advies|management.?organisatie|"
    r"insights.?personal|markies.?coaching|"
    r"lief.?met.?lef.?coaching|am.?coaching|"
    r"suzan.?muller.?gastouder|mijnpowernl|"
    r"een.?warm.?nest|hoogendoorn.?fysiotherapie",
    re.I,
)


def blob(data: dict) -> str:
    parts = [
        data.get("naam") or "",
        data.get("slug") or "",
        (data.get("slug") or "").replace("-", " "),
        data.get("omschrijving") or "",
        data.get("meta_title") or "",
        data.get("meta_description") or "",
        data.get("website") or "",
    ]
    ken = data.get("kenmerken") or {}
    for vals in ken.values():
        if isinstance(vals, list):
            parts.extend(vals)
    return " ".join(parts).lower()


def should_close(data: dict) -> str | None:
    if data.get("status") == "gesloten":
        return None
    b = blob(data)
    name = f"{data.get('naam') or ''} {data.get('slug') or ''}".lower()
    if PSYCH_OK.search(b):
        return None
    if JUNK.search(b) or NAME_JUNK.search(name):
        return "off-niche junk (no psych signal)"
    if COACH_ONLY.search(b) and not PSYCH_OK.search(b):
        return "coach/lifestyle only (no psych signal)"
    return None


def main() -> None:
    closed = []
    kept_coachish = []
    for path in sorted(NORM.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        reason = should_close(data)
        if not reason:
            b = blob(data)
            if COACH_ONLY.search(b) and PSYCH_OK.search(b):
                kept_coachish.append(
                    {"id": data.get("id"), "naam": data.get("naam"), "slug": path.name}
                )
            continue
        data["status"] = "gesloten"
        # annotate lightly for audit
        data.setdefault("_triage", {})
        data["_triage"]["off_niche"] = reason
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cpath = CONTENT / path.name
        if cpath.exists():
            cdata = json.loads(cpath.read_text(encoding="utf-8"))
            cdata["status"] = "gesloten"
            cdata.setdefault("_triage", {})
            cdata["_triage"]["off_niche"] = reason
            cpath.write_text(
                json.dumps(cdata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        closed.append(
            {
                "id": data.get("id"),
                "naam": data.get("naam"),
                "slug": path.name,
                "reason": reason,
            }
        )

    # status counts after
    statuses = Counter()
    for path in NORM.glob("*.json"):
        statuses[json.loads(path.read_text(encoding="utf-8")).get("status", "?")] += 1

    report = {
        "closed_count": len(closed),
        "closed": closed,
        "kept_coach_with_psych_signal": kept_coachish[:50],
        "kept_coach_with_psych_signal_count": len(kept_coachish),
        "status_counts": dict(statuses),
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"closed {len(closed)} clear junk")
    print("status counts:", dict(statuses))
    print(f"wrote {REPORT}")
    for row in closed[:30]:
        print(f"  - {row['naam']}: {row['reason']}")
    if len(closed) > 30:
        print(f"  … +{len(closed) - 30} more")


if __name__ == "__main__":
    main()
