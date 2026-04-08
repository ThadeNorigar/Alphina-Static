"""
Cleanup: Moragh-Seite von Buch-1-Akt-4 korrekt platzieren.

Problem:
- monat[10] thalassien enthaelt faelschlich neue Events fuer Kap 35-39 (Moragh-Szenen)
- monat[11] moragh enthaelt alte Duplikate (Alt-Kap 36, 37, 39, 40) mit veralteter Numerierung

Fix:
- Entferne die falsch platzierten Events aus monat[10] thalassien
- Korrigiere die Numerierung in monat[11] moragh
- Uebernehme die besseren detail-Texte aus meinen neueren Versionen
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
ZEITLEISTE = REPO / "buch" / "zeitleiste.json"


# Titel die ich in monat[10] thalassien hinzugefuegt habe,
# die eigentlich Moragh-Szenen sind und nach monat[11] gehoeren
# (titel, neue_kap_nummer) — identifiziert ueber Titel-Match
TO_MOVE = {
    ("35", "Varen begegnet Alphina — 1423er Thalassisch, Hand an ihr Kinn"),
    ("36", "Sorel stirbt — Varens Abwehr, unterlassene Rettung"),
    ("38", "Elke findet die Gruppe — 1423er Thalassisch"),
    ("39", "Alphinas Trauer wird Hass — Dornen wachsen zum ersten Mal"),
}

# Alt-Numerierung in monat[11] moragh korrigieren (-1)
MORAGH_RENUM = {"36": "35", "37": "36", "39": "38", "40": "39", "41": "40"}


def main():
    with open(ZEITLEISTE, encoding="utf-8") as f:
        z = json.load(f)

    m10 = z["monate"][10]
    m11 = z["monate"][11]

    # 1) Events aus monat[10] thalassien entfernen und in monat[11] moragh verschieben
    thal10 = m10["events"]["thalassien"]
    mor11 = m11["events"]["moragh"]
    moved = []
    remaining = []
    for ev in thal10:
        key = (ev.get("kapitel"), ev.get("titel"))
        if key in TO_MOVE:
            moved.append(ev)
        else:
            remaining.append(ev)
    m10["events"]["thalassien"] = remaining

    # 2) Alt-Duplikate in monat[11] moragh entfernen (die alte Nummerierung)
    # Alt-Kap 36, 37, 39, 40 — die werden durch die moved events ersetzt
    old_titles_to_remove = {
        "Varen tritt aus dem Schatten — Hand an Alphinas Kinn",
        "Sorel stirbt. Varen hätte helfen können. Tut es nicht.",
        "Elke findet die Überlebenden",
        "Alphinas Dornen — Hass wächst buchstäblich",
    }
    mor11_cleaned = [e for e in mor11 if e.get("titel") not in old_titles_to_remove]

    # 3) Die verschobenen Events hinzufuegen
    mor11_cleaned.extend(moved)

    # 4) Bestehende moragh-Events in monat[11] mit veralteten kap korrigieren
    # (falls noch uebrig, z.B. I9)
    for ev in mor11_cleaned:
        kap = ev.get("kapitel")
        if kap in MORAGH_RENUM:
            ev["kapitel"] = MORAGH_RENUM[kap]

    # 5) Sortieren nach tz_tag
    def sortkey(e):
        return (e.get("tz_tag", 999), e.get("kapitel", ""))

    mor11_cleaned.sort(key=sortkey)
    m11["events"]["moragh"] = mor11_cleaned

    # 6) Zurueckschreiben
    with open(ZEITLEISTE, "w", encoding="utf-8") as f:
        json.dump(z, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"OK: {len(moved)} Events von monat[10] thal nach monat[11] moragh verschoben")
    print(f"    monat[10] thalassien: {len(remaining)} events")
    print(f"    monat[11] moragh: {len(mor11_cleaned)} events")


if __name__ == "__main__":
    main()
