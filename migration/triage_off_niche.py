#!/usr/bin/env python3
"""Phase 1c off-niche for Kostenschoorsteenveger.nl. bij twijfel → gesloten.

In scope: schoorsteenvegers, veegbedrijven, haard-/kachelspecialisten with
chimney service, ramoneur/sweep. Out: pure dakdekker/bouw without chimney
signal, food, unrelated trades. Personal names without signal → gesloten.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT.parent / "src/content/schoorsteenvegers"
NORM = ROOT / "scrape/normalized"
REPORT = ROOT / "OFF_NICHE_PASS.json"
MD = ROOT / "OFF_NICHE_TRIAGE.md"

STRONG = re.compile(
    r"schoorsteenveg|schoorsteenveeg|schoorsteen\s*veeg|"
    r"veegbedrijf|roetveeg|kachelveeg|haardveeg|"
    r"\bramoneur\b|\bsweep\b|clean\s*sweep|pro\s*sweep|"
    r"schoorsteenreinig|schouwveeg|schouw\s*reinig|"
    r"kachelspecialist|haardenspecialist|stylschouwen",
    re.I,
)
HARD_JUNK = re.compile(
    r"camping|hotel|restaurant|kapsalon|makelaar|tandarts|fysio|"
    r"hovenier|schilder|autobedrijf|\bgarage\b|sportschool|zwembad|"
    r"supermarkt|gemeente\b|architect|notaris|advocaat|dierenarts|"
    r"food\s*&\s*industry|hago\s*food|array\s*industries|"
    r"metaalhandel|metalas|"
    r"24-?uurs?\s*dakdekker|dakdekkerservice|"
    r"dakdekkersbedrijf|dakbedekking|rietdekker|"
    r"voegersbedrijf|schoonmaakbedrijf|"
    r"bouwbedrijf(?!.*schoorsteen)",
    re.I,
)
IN_TEXT = re.compile(
    r"schoorsteen|veegbedrijf|ramoneur|\bsweep\b|roet|"
    r"kachel|haard|schouw|schoorsteenveger|chimney",
    re.I,
)


def name_blob(d: dict) -> str:
    return f"{d.get('naam') or ''} {d.get('slug') or ''}"


def full(d: dict) -> str:
    # Prefer naam + omschrijving. meta_title is often just "Name phone".
    # Skip meta_description boilerplate / kenmerken defaults.
    return " ".join([name_blob(d), d.get("omschrijving") or "", d.get("meta_title") or ""])


def should_close(d: dict) -> str | None:
    nb, fb = name_blob(d), full(d)
    strong = bool(STRONG.search(nb) or STRONG.search(fb))
    if HARD_JUNK.search(nb) and not strong:
        return "hard junk name"
    if strong or IN_TEXT.search(fb):
        return None
    return "twijfel → gesloten (no schoorsteen/veeg signal)"


def main() -> None:
    closed = []
    reasons = Counter()
    actief = 0
    for path in sorted(CONTENT.glob("*.json")):
        d = json.loads(path.read_text())
        reason = should_close(d)
        if not reason:
            if d.get("status") != "actief" or d.get("_triage"):
                d["status"] = "actief"
                d.pop("_triage", None)
                path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
                npath = NORM / path.name
                if npath.exists():
                    nd = json.loads(npath.read_text())
                    nd["status"] = "actief"
                    nd.pop("_triage", None)
                    npath.write_text(json.dumps(nd, ensure_ascii=False, indent=2) + "\n")
            actief += 1
            continue
        d["status"] = "gesloten"
        d["_triage"] = {"reason": reason, "pass": "off-niche-1c"}
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
        npath = NORM / path.name
        if npath.exists():
            nd = json.loads(npath.read_text())
            nd["status"] = "gesloten"
            nd["_triage"] = d["_triage"]
            npath.write_text(json.dumps(nd, ensure_ascii=False, indent=2) + "\n")
        closed.append({"naam": d.get("naam"), "reason": reason})
        reasons[reason] += 1

    report = {
        "counts": {"twijfel": 0, "closed": len(closed), "actief": actief},
        "reasons": dict(reasons),
        "samples": closed[:40],
    }
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    MD.write_text(
        "# Off-niche — Kostenschoorsteenveger.nl\n\n"
        f"Actief {actief} · Gesloten {len(closed)} · twijfel=0\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in reasons.items())
        + "\n"
    )
    print(json.dumps(report["counts"], indent=2))
    print("reasons", dict(reasons))


if __name__ == "__main__":
    main()
