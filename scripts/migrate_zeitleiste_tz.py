#!/usr/bin/env python3
"""
Migration: zeitleiste.json TZ-Architektur reparieren.

Aktuelle Drift:
- B2/B3-Hauptevents haben synthetisches `tz` (Inkrement +4 pro Kapitel),
  was suggeriert echte TZ-Jahre, aber tatsächlich nur fortlaufende Sortier-
  Werte sind. Das `tz_datum`-Feld zeigt entsprechend falsche TZ-Zahlen
  (z.B. „MZ 5.78 · TZ 784" statt richtigem 2020 TZ für Expedition 1).

Ziel-Architektur:
- `tz` = echtes Thalassien-TZ-Jahr (NUR wo das Event ein echtes TZ-Datum
  trägt: alle B1, B0, Sync-Events, B3-Thalassien-Echo-Anker)
- `mz` = echtes Moragh-MZ-Jahr (Moragh-Events)
- `tz_sort` = reine Sortier-Marke (bleibt unverändert für Sortierungs-
  Stabilität)
- `tz_datum` = Anzeigetext, ohne falsche TZ-Zahlen

Run:
  python scripts/migrate_zeitleiste_tz.py            # dry-run
  python scripts/migrate_zeitleiste_tz.py --apply    # in-place
"""

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ZEITLEISTE_PATH = REPO_ROOT / "buch" / "zeitleiste.json"

# Echte Welt-TZ-Anker für B3-Events (aus Memory + Plot-Master).
# Identifikation primär über (kapitel) + Substring-Match im titel.
# Liste nach Titel-Substring, weil kapitel allein mehrdeutig wäre.
B3_TZ_ANCHORS = [
    # (titel_substring, tz_year)
    ("Maren gründet die Schwellenforschungsgesellschaft", 1990),
    ("Tyra Halvard + Team vor dem Aufbruch", 2019),
    ("Erste Expedition kommt durchs Portal", 2020),
    ("Erste Expedition scheitert", 2037),
    ("Verwüster-Angriff auf Vael", 2037),
    ("Junge Syra Halvard + Kelvar Velkan", 2080),
    ("Halvard + Velkan planen Expedition 2", 2110),
    ("Zweite Expedition kommt durch", 2120),
    ("Expedition 2 Aufbruch aus Vael", 2120),
    ("Portal-Finale", 2152),
    ("Kind in Vael berührt den Farn", 2155),
]

# Moragh-Monatsnamen für tz_datum-Formatierung
MZ_MONATE = [
    "Torash", "Ashral", "Keldath", "Reshvan",
    "Dravon", "Gormath", "Nyrkel", "Vethash",
]


def find_b3_tz_anchor(event):
    """Wenn das B3-Event ein echter TZ-Welt-Anker ist, gib das tz zurück."""
    titel = event.get("titel", "")
    for sub, year in B3_TZ_ANCHORS:
        if sub in titel:
            return year
    return None


def format_mz_datum(mz):
    """„MZ 5.78 (Gormath)" — Monat aus mz-Bruchteil ableiten."""
    if mz is None:
        return None
    try:
        mz_f = float(mz)
    except (TypeError, ValueError):
        return None
    # 8 Monate à 36 Tage = 288 Tage / Jahr
    frac = mz_f - int(mz_f) if mz_f >= 0 else (mz_f - int(mz_f) + 1) % 1
    monat_idx = int(frac * 8)
    monat_idx = max(0, min(7, monat_idx))
    monat_name = MZ_MONATE[monat_idx]
    return f"MZ {mz_f:.2f} ({monat_name})"


def migrate_event(event):
    """Gib (new_event, change_log) zurück. change_log ist Liste von Strings."""
    changes = []
    new_ev = dict(event)  # shallow copy
    buch = event.get("buch", "")
    welt = event.get("welt", "")

    # B1: alles bleibt — tz ist echtes TZ-Jahr
    if buch == "B1":
        return new_ev, changes

    # B0 + Sync-Events: tz ist echtes TZ-Jahr (Hintergrund), bleibt
    if buch == "B0" or welt == "synchronisation":
        return new_ev, changes

    # B2: alle Events sind reine Moragh-Events. tz war synthetisch — entfernen.
    if buch == "B2":
        old_tz = new_ev.pop("tz", None)
        old_tz_datum = new_ev.get("tz_datum")
        if old_tz is not None:
            changes.append(f"tz entfernt (war synthetisch: {old_tz})")
        # tz_datum neu: nur MZ + Monatsname
        mz = new_ev.get("mz")
        new_tz_datum = format_mz_datum(mz)
        if new_tz_datum and new_tz_datum != old_tz_datum:
            new_ev["tz_datum"] = new_tz_datum
            changes.append(f"tz_datum: {old_tz_datum!r} → {new_tz_datum!r}")
        return new_ev, changes

    # B3: zwei Klassen
    if buch == "B3":
        anchor_tz = find_b3_tz_anchor(event)
        old_tz = new_ev.get("tz")
        old_tz_datum = new_ev.get("tz_datum")
        mz = new_ev.get("mz")
        if anchor_tz is not None:
            # Sync-Punkt: tz auf echtes Welt-Jahr setzen
            if old_tz != anchor_tz:
                new_ev["tz"] = anchor_tz
                changes.append(f"tz: {old_tz} → {anchor_tz} (echter TZ-Anker)")
            # tz_datum: „MZ X.XX (Monat) · YYYY TZ"
            mz_part = format_mz_datum(mz) if mz is not None else None
            new_tz_datum = (
                f"{mz_part} · {anchor_tz} TZ" if mz_part else f"{anchor_tz} TZ"
            )
            if new_tz_datum != old_tz_datum:
                new_ev["tz_datum"] = new_tz_datum
                changes.append(f"tz_datum: {old_tz_datum!r} → {new_tz_datum!r}")
        else:
            # Reines Moragh-Event: tz entfernen
            if "tz" in new_ev:
                new_ev.pop("tz")
                changes.append(f"tz entfernt (war synthetisch: {old_tz})")
            new_tz_datum = format_mz_datum(mz)
            if new_tz_datum and new_tz_datum != old_tz_datum:
                new_ev["tz_datum"] = new_tz_datum
                changes.append(f"tz_datum: {old_tz_datum!r} → {new_tz_datum!r}")
        return new_ev, changes

    # Andere (z.B. leeres buch) — unverändert
    return new_ev, changes


def update_meta(meta):
    """Meta-Sektion-Beschreibung anpassen, damit Konvention klar ist."""
    new_meta = dict(meta)
    new_desc = (
        "Strikte Chronologie. TZ = Thalassien-Zeitrechnung (Gregorianisch + "
        "thalassische Monatsnamen, TZ 0 = Erfindung des Uhrwerks ~1269 UZ). "
        "MZ = Moragh-Zeitrechnung (26h/Tag, 8 Monate à 36 Tage, MZ 0 = "
        "Besiedelung Moragh). Kopplung am Übergang B1→B2: 1 MZ-Jahr ≈ 400 "
        "TZ-Jahre (B1-Ende 551 TZ → B2-Start MZ 0, was in Thalassien-Zeit "
        "etwa 1987 TZ entspricht). "
        "**Felder:** `tz` enthält echte TZ-Welt-Jahre und ist NUR gesetzt "
        "bei B1-Events, B0-Hintergrund, Sync-Events und B3-Thalassien-Echo-"
        "Ankern (Maren-SFG 1990, Expedition 1: 2020, Maren-Tod 2037, Syra+"
        "Kelvar 2080, Expedition-2-Plan 2110, Expedition 2: 2120, Portal-"
        "Finale 2152, Kind-in-Vael 2155). `mz` enthält echte Moragh-MZ-"
        "Werte (B0/B2/B3-Moragh-Events). `tz_sort` ist reine Sortier-Marke "
        "über alle Bücher hinweg (kein echtes Datum). `tz_datum` ist "
        "formatierter Anzeigetext."
    )
    new_meta.setdefault("meta", {})
    if "meta" in new_meta and isinstance(new_meta["meta"], dict):
        new_meta["meta"]["beschreibung"] = new_desc
    return new_meta


def main():
    ap = argparse.ArgumentParser(description="Migriere zeitleiste.json TZ-Felder")
    ap.add_argument("--apply", action="store_true",
                    help="In-place schreiben (sonst nur dry-run)")
    args = ap.parse_args()

    with ZEITLEISTE_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    events = data.get("events", [])
    new_events = []
    total_changes = 0
    changed_events = 0
    samples_by_buch = {}

    for ev in events:
        new_ev, changes = migrate_event(ev)
        new_events.append(new_ev)
        if changes:
            changed_events += 1
            total_changes += len(changes)
            buch = ev.get("buch", "?")
            kap = ev.get("kapitel", "?")
            titel = ev.get("titel", "")[:55]
            samples_by_buch.setdefault(buch, []).append(
                (f"{buch}-K{kap}: {titel}", changes)
            )

    # Meta-Header aktualisieren
    new_meta_outer = data.get("meta", {})
    if isinstance(new_meta_outer, dict):
        new_desc = (
            "Strikte Chronologie. TZ = Thalassien-Zeitrechnung. MZ = "
            "Moragh-Zeitrechnung (26h/Tag, 8 Monate à 36 Tage). Kopplung "
            "am Übergang B1→B2: 1 MZ-Jahr ≈ 400 TZ-Jahre. **Felder:** "
            "`tz` enthält echte TZ-Welt-Jahre und ist NUR gesetzt bei "
            "B1-Events, B0-Hintergrund, Sync-Events und B3-Thalassien-"
            "Echo-Ankern (Maren-SFG 1990, Expedition 1: 2020, Maren-Tod "
            "2037, Syra+Kelvar 2080, Expedition-2-Plan 2110, Expedition "
            "2: 2120, Portal-Finale 2152, Kind-in-Vael 2155). `mz` "
            "enthält echte Moragh-MZ-Werte. `tz_sort` ist reine Sortier-"
            "Marke über alle Bücher hinweg. `tz_datum` ist formatierter "
            "Anzeigetext."
        )
        old_desc = new_meta_outer.get("beschreibung", "")
        if old_desc != new_desc:
            print(f"\n[META] beschreibung wird aktualisiert.")

    # Report
    print(f"=== Migrations-Report ===")
    print(f"Total Events:      {len(events)}")
    print(f"Geänderte Events:  {changed_events}")
    print(f"Total Änderungen:  {total_changes}")
    print()

    for buch in sorted(samples_by_buch.keys()):
        samples = samples_by_buch[buch]
        print(f"--- {buch}: {len(samples)} Events betroffen ---")
        for title, changes in samples[:3]:
            print(f"  {title}")
            for c in changes:
                print(f"    • {c}")
        if len(samples) > 3:
            print(f"  ... und {len(samples) - 3} weitere")
        print()

    # Sortierungs-Validierung
    print("=== Sortierungs-Check (tz_sort monoton?) ===")
    prev_sort = None
    monotonic = True
    for ev in new_events:
        s = ev.get("tz_sort")
        if s is None:
            continue
        if prev_sort is not None and s < prev_sort:
            print(f"  [!] tz_sort nicht monoton: {prev_sort} → {s} bei "
                  f"{ev.get('buch')}-K{ev.get('kapitel')}")
            monotonic = False
        prev_sort = s
    if monotonic:
        print("  ✓ tz_sort ist monoton steigend (Sortierung intakt)")
    print()

    if args.apply:
        # tatsächlich schreiben
        data["events"] = new_events
        if isinstance(data.get("meta"), dict):
            data["meta"]["beschreibung"] = new_desc
        with ZEITLEISTE_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ Geschrieben: {ZEITLEISTE_PATH}")
    else:
        print("[dry-run] Nichts geschrieben. Mit --apply erneut ausführen.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
