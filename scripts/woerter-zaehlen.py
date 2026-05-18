#!/usr/bin/env python3
"""Zaehlt Woerter aller finalen Kapitel aus status.json.

Output:
  - Pro Kapitel: Status-Wert vs. tatsaechliche Datei
  - Pro Akt: Summe + Anzahl Kapitel
  - Gesamt: Summe, Seiten (a 250 Woerter), Abweichung zu status.json

Header und Datums-Zeile werden NICHT mitgezaehlt (Prosa-Netto).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATUS = ROOT / "buch" / "status.json"
KAPITEL_DIR = ROOT / "buch" / "kapitel"

HEADER_RE = re.compile(r"^#\s")
DATUM_RE = re.compile(r"^\*[^*]+\*\s*$")
HR_RE = re.compile(r"^---+\s*$")


def zaehle_prosa(pfad: Path) -> int:
    """Woerter ohne Markdown-Header und Datums-Italics."""
    if not pfad.exists():
        return 0
    text = pfad.read_text(encoding="utf-8")
    zeilen = []
    for zeile in text.splitlines():
        stripped = zeile.strip()
        if not stripped:
            continue
        if HEADER_RE.match(stripped):
            continue
        if DATUM_RE.match(stripped):
            continue
        if HR_RE.match(stripped):
            continue
        zeilen.append(stripped)
    prosa = " ".join(zeilen)
    # Markdown-Marker entfernen, sonst werden ** oder _ als Wort gezaehlt
    prosa = re.sub(r"[*_`>]", " ", prosa)
    return len([w for w in prosa.split() if w.strip()])


def main() -> int:
    daten = json.loads(STATUS.read_text(encoding="utf-8"))
    buch = daten["buch1"]
    kapitel = buch["kapitel"]
    akte = buch["akte"]

    gesamt_woerter = 0
    gesamt_kapitel = 0
    abweichungen: list[tuple[str, int, int]] = []
    fehlend: list[str] = []

    print(f"{'KAP':<5} {'POV':<14} {'STATUS':<10} {'GEZAEHLT':>9} {'STATUS.JSON':>12}  DATEI")
    print("-" * 90)

    for akt in akte:
        akt_woerter = 0
        akt_anzahl = 0
        print(f"\n### {akt['name']}")
        for kap_id in akt["kapitel"]:
            eintrag = kapitel.get(kap_id)
            if not eintrag:
                print(f"{kap_id:<5} -- nicht in status.json --")
                continue
            status = eintrag.get("status", "?")
            pov = eintrag.get("pov", eintrag.get("titel", "?"))[:14]
            datei = eintrag.get("datei")
            woerter_status = eintrag.get("woerter", 0)
            if not datei:
                print(f"{kap_id:<5} {pov:<14} {status:<10} {'-':>9} {woerter_status:>12}  (keine Datei)")
                fehlend.append(kap_id)
                continue
            pfad = KAPITEL_DIR / datei
            gezaehlt = zaehle_prosa(pfad)
            if status == "final":
                akt_woerter += gezaehlt
                akt_anzahl += 1
                gesamt_woerter += gezaehlt
                gesamt_kapitel += 1
                if woerter_status and abs(gezaehlt - woerter_status) > 50:
                    abweichungen.append((kap_id, woerter_status, gezaehlt))
            print(f"{kap_id:<5} {pov:<14} {status:<10} {gezaehlt:>9} {woerter_status:>12}  {datei}")
        seiten = akt_woerter / 250
        print(f"   AKT-SUMME: {akt_woerter:>9} Woerter  ({akt_anzahl} Kapitel, {seiten:.0f} Seiten)")

    seiten_total = gesamt_woerter / 250
    print("\n" + "=" * 90)
    print(f"GESAMT (final): {gesamt_woerter:,} Woerter | {gesamt_kapitel} Kapitel | {seiten_total:.0f} Seiten (a 250 Woerter)")
    print(f"Ziel-Korridor:  ~225.000 Woerter / ~900 Seiten")
    diff = gesamt_woerter - 225000
    pct = (gesamt_woerter / 225000 - 1) * 100
    pfeil = "uber" if diff > 0 else "unter"
    print(f"Status:         {abs(diff):,} Woerter {pfeil} Ziel ({pct:+.1f}%)")

    if abweichungen:
        print("\n--- Abweichungen status.json vs. Datei (>50 Woerter) ---")
        for kid, soll, ist in abweichungen:
            print(f"  K{kid:<4} status.json: {soll:>6}  Datei: {ist:>6}  (Delta {ist - soll:+d})")

    if fehlend:
        print(f"\nFEHLENDE DATEIEN: {', '.join(fehlend)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
