"""
Einmal-Skript: Buch-1-Events vollstaendig nachziehen.

1. Alte Kap-Nummern korrigieren (Aktplan hatte 12 Kap in Akt 1, jetzt 11)
2. Neue State-/Schluessel-Events fuer Akt 2-4 einpflegen

Kap-Mapping (alt -> neu):
  12 -> 11 (bereits frueher gemacht)
  13 -> 12
  14 -> 13
  15 -> 14 (Vesper+Maren Uhrengeschaeft)
  16 -> 15
  17 -> 16
  18 -> 17 (Alle vier Garten)
  19 -> 18 (Manuskript)
  20 -> 19
  21 -> 20
  22 -> 21 (Dunkelkammer)
  23 -> 22 (Vesper+Maren erste Nacht)
  24 -> 23
  25 -> 24 (Grenzverletzung Fotos)
  26 -> 25 (Bruch / Schem Wange)
  27 -> 26
  28 -> 27 (Maren Tunnel)
  29 -> 28 (Alphina Tunnel)
  30 -> 29
  31 -> 30 (Runa Feuer)
  32 -> 31 (Vesper Erkenntnis)
  33 -> 32
  34 -> 33 (Letzte Bluete)
  35 -> 34 (Durchgang)
  36 -> 35 (Varen)
  37 -> 36 (Sorels Tod)
  38 -> 37
  39 -> 38 (Elke findet sie)
  40 -> 39
  41 -> 40 (Epilog Vael)
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
ZEITLEISTE = REPO / "buch" / "zeitleiste.json"

# Alt -> Neu fuer Kap ab 13
KAP_RENUM = {str(i): str(i - 1) for i in range(13, 42)}

# Neue Events fuer Buch 1 Akt 2-4 (mit aktueller status.json Nummerierung)
# Tages-Rohplan Akt 2-4 (Option B, 6 Wochen Akt 1, dann Akt 2-4 spannen Mai-Nov):
#   Akt 2 (Kap 12-22 + I3-I5): Anfang Mai - Anfang Juli (~8 Wochen)
#   Akt 3 (Kap 23-32 + I6-I7): Juli - Oktober (~12 Wochen)
#   Akt 4 (Kap 33-40 + I8-I9): Oktober - Anfang November
# Tage ab Jahresanfang TZ 551:
#   Kap 12 (12 Mai)  -> Tag 132
#   Kap 14 (22 Mai)  -> Tag 142
#   Kap 17 (3 Juni)  -> Tag 154
#   Kap 18 (7 Juni)  -> Tag 158 (Manuskript)
#   Kap 21 (20 Juni) -> Tag 171 (Dunkelkammer)
#   Kap 22 (1 Juli)  -> Tag 182 (Vesper+Maren erste Nacht)
#   Kap 23 (10 Juli) -> Tag 191 (Archiv)
#   Kap 27 (5 Aug)   -> Tag 217 (Maren Tunnel)
#   Kap 28 (10 Aug)  -> Tag 222
#   Kap 30 (25 Aug)  -> Tag 237 (Runa Feuer)
#   Kap 31 (1 Sep)   -> Tag 244 (Vesper Erkenntnis)
#   Kap 33 (30 Sep)  -> Tag 273 (Letzte Bluete)
#   Kap 34 (30 Sep)  -> Tag 273 (Durchgang)
#   Kap 35-39 (30 Sep - 3 Okt) -> Tag 273-276
#   Kap 40 (Epilog) -> Tag 276+

TAGE = {
    "12": (132, "12. Mai"),
    "13": (137, "17. Mai"),
    "14": (142, "22. Mai"),
    "15": (147, "27. Mai"),
    "16": (151, "31. Mai"),
    "I3": (155, "1423"),
    "17": (158, "7. Juni"),
    "18": (162, "11. Juni"),
    "I4": (165, "1423"),
    "19": (168, "17. Juni"),
    "20": (171, "20. Juni"),
    "21": (175, "24. Juni"),
    "22": (182, "1. Juli"),
    "I5": (185, "1423"),
    "23": (191, "10. Juli"),
    "24": (198, "17. Juli"),
    "25": (205, "24. Juli"),
    "26": (210, "29. Juli"),
    "I6": (212, "1423"),
    "27": (217, "5. August"),
    "28": (222, "10. August"),
    "29": (228, "16. August"),
    "30": (237, "25. August"),
    "I7": (240, "1423"),
    "31": (244, "1. September"),
    "32": (272, "29. September"),
    "33": (273, "30. September — Nacht"),
    "34": (273, "30. September — 4:33 nach Mitternacht"),
    "35": (273, "30. September — Moragh-Morgen"),
    "36": (273, "30. September — Moragh"),
    "I8": (273, "1423 / Moragh"),
    "37": (274, "1. Oktober — Moragh"),
    "38": (275, "2. Oktober — Moragh"),
    "I9": (273, "Moragh, Stunden vorher"),
    "39": (276, "3. Oktober — Moragh"),
    "40": (277, "4. Oktober — Vael ohne die Fuenf"),
}


def make_event(kapitel, typen, titel, pov=None, **kwargs):
    tag, text = TAGE.get(kapitel, (None, ""))
    ev = {
        "tz": 551,
        "mz": 0,
        "kapitel": kapitel,
        "typen": typen,
        "titel": titel,
    }
    if pov:
        ev["pov"] = pov
    if tag is not None:
        ev["tz_tag"] = tag
    if text:
        ev["datum_text"] = text
    ev.update(kwargs)
    return ev


# =============================================================================
# NEUE EVENTS FUER BUCH 1 AKT 2-4
# =============================================================================

NEUE_EVENTS = []

# ---- Akt 2 — Zusammenfinden ---------------------------------------------
NEUE_EVENTS += [
    # Kap 12 — Alphina: Die Risse (Alphina sucht Sorel, findet Lichthaus)
    make_event("12", ["erkenntnis"],
               "Stadt-Anomalien eskalieren: Risse im Pflaster, heisses Wasser, Kaminfeuer",
               pov="Kap 12 · Alphina",
               tags=["Erkenntnis: Vael zerfaellt"]),

    # Kap 14 — Vesper+Maren: Das Uhrengeschaeft  (ersetzt Alt-Kap-15-Event)
    make_event("14", ["begegnung"],
               "Vesper und Maren treffen sich im Uhrengeschaeft",
               pov="Kap 14 · Vesper",
               figuren=["Vesper", "Maren"],
               intensitaet="fluechtig",
               ort="Uhrmacher-Werkstatt",
               detail="Maren braucht eine Schiffsuhr. Beide sehen die Grauwe rueckwaerts fliessen. Keiner sagt etwas.",
               tags=["Erste Begegnung: Vesper + Maren"]),

    # Kap 17 — Alle vier im Garten (ersetzt Alt-18-Event)
    make_event("17", ["begegnung", "schlüssel"],
               "Alle vier treffen sich erstmals gemeinsam im Botanischen Garten",
               pov="Kap 17 · Alle",
               figuren=["Alphina", "Sorel", "Vesper", "Maren"],
               intensitaet="fluechtig",
               ort="Botanischer Garten, Vael",
               detail="Vier Resonanzen auf engstem Raum. Die Schemen verschwinden schlagartig. Pochen unter der Erde — Herzschlag. Varens Augen sehen durch die Schemen: er weiss jetzt dass alle vier da sind.",
               tags=["Schluesselereignis: Vier zusammen", "Tschechow: Vier Resonanzen"]),

    # Kap 18 — Manuskript (ersetzt Alt-19-Event)
    make_event("18", ["schlüssel", "tschechow"],
               "Esther bringt das 400 Jahre alte Manuskript ins Tidemoor-Haus",
               pov="Kap 18 · Vesper",
               detail="Vier Fremde, ein Portal, eine Schwelle. Teilweise echt, teilweise von Varen ueberschrieben. Daemon-Fingerabdruecke im Kohlestaub: zu viele Gelenke.",
               tags=["Manuskript", "Tschechow: Varens Koeder"]),

    # Kap 19 — Alphina+Vesper lesen Manuskript zusammen
    make_event("19", ["begegnung"],
               "Alphina und Vesper studieren das Manuskript",
               pov="Kap 19 · Alphina",
               figuren=["Alphina", "Vesper"],
               intensitaet="bekannt",
               ort="Tidemoor-Haus (abends)",
               detail="Seine Hand auf ihrer — Stromschlag ohne Strom. 'Bei Vesper kann sie. Bei Sorel kann sie nicht.' Genau das ist der Punkt.",
               tags=["Erste Begegnung: Alphina + Vesper"]),

    # Kap 20 — Vesper + Maren Werft, Tee
    make_event("20", ["begegnung"],
               "Vesper bringt Maren die Schiffsuhr zur Werft",
               pov="Kap 20 · Vesper",
               figuren=["Vesper", "Maren"],
               intensitaet="bekannt",
               ort="Werft Dahl",
               detail="Saegemehl, Tee auf Holzkisten. Arm-Beruehrung. Erster ehrlicher Austausch ueber das Unmoegliche — Standuhr, Boot, Schemen.",
               tags=["Beziehung: Vesper + Maren"]),

    # Kap 21 — Dunkelkammer (ersetzt Alt-22)
    make_event("21", ["erotik", "erkenntnis"],
               "Alphina und Sorel: Dunkelkammer, erste intime Szene",
               pov="Kap 21 · Alphina",
               detail="Sorel zeigt ihr die Platten: Schemen hinter ihr auf jeder. Kontrollverlust. Farne brechen durch Kellerwaende.",
               tags=["Erotik: Alphina + Sorel", "Erkenntnis: Schemen folgen NUR Alphina"]),

    # Kap 22 — Vesper+Maren erste Nacht (ersetzt Alt-23)
    make_event("22", ["erotik"],
               "Vesper und Maren: erste Nacht",
               pov="Kap 22 · Maren",
               detail="Rohe Chemie. Maren geht morgens — weil sie immer geht.",
               tags=["Erotik: Vesper + Maren"]),
]

# ---- Akt 3 — Eskalation --------------------------------------------------
NEUE_EVENTS += [
    # Kap 23 — Archiv / Ritual-Papier
    make_event("23", ["schlüssel", "tschechow"],
               "Archiv: Ritual-Papier mit Schemen-Fingerabdruecken",
               pov="Kap 23 · Alphina",
               detail="Jara findet Randnotizen (andere Handschrift) + Moragh-Sprachbuch. Ritual-Anweisungen, Steinkreis-Zeichnung. Varen hat es per Schem platziert.",
               tags=["Schluesselereignis: Ritual-Anleitung gefunden"]),

    # Kap 24 — Grenzverletzung (ersetzt Alt-25)
    make_event("24", ["erkenntnis"],
               "Alphina findet die Steg-Fotos — 'Du hast mich genommen ohne zu fragen'",
               pov="Kap 24 · Sorel",
               tags=["Beziehung: Alphina + Sorel — Grenzverletzung"]),

    # Kap 25 — Bruch + Schem beruehrt Wange (ersetzt Alt-26)
    make_event("25", ["tschechow", "schlüssel"],
               "Schem beruehrt Alphinas Wange — Varens Hand durch die Welten",
               pov="Kap 25 · Alphina",
               detail="Alphina im Lichthaus-Keller allein. Ein Schem streckt die Hand aus, beruehrt ihre Wange. Warmer Fleck. Varen kann sie sehen und beruehren.",
               tags=["Tschechow: Varens Hand an Alphinas Kinn (Vorbote)"]),

    # Kap 27 — Maren Tunnel (ersetzt Alt-28)
    make_event("27", ["schlüssel"],
               "Maren folgt dem Wasser zum Steinkreis",
               pov="Kap 27 · Maren",
               detail="Durch Tunnel unter der Werft. Der Purpurstein schwitzt Salz — nicht Grauwe-Salz, anderes Meer. Hand auf den Stein: der Riss weint.",
               tags=["Schluesselereignis: Maren findet den Riss"]),

    # Kap 28 — Alphina Tunnel / Versoehnung (ersetzt Alt-29)
    make_event("28", ["begegnung"],
               "Alphina findet Sorel am Riss — Versoehnung",
               pov="Kap 28 · Alphina",
               detail="'Du bist nicht hier weil du mich liebst.' Alphina gibt ihm Recht. Zum ersten Mal.",
               tags=["Beziehung: Alphina + Sorel — Versoehnung"]),

    # Kap 30 — Runa Feuer (ersetzt Alt-31)
    make_event("30", ["erkenntnis", "tschechow"],
               "Runas Haende gluehen — Feuer-Resonanz entdeckt",
               pov="Kap 30 · Alphina",
               detail="Ein Schem toetet einen Haendler am Hafen. Andere Fraktion (Thar) am Hafen: Metall-Geruch. Runa bei Alphina — ihre Haende gluehen buchstaeblich, Brandfleck im Setzkasten.",
               tags=["Erkenntnis: Runa hat Feuer-Resonanz", "Tschechow: Thar-Schemen (andere Fraktion)"]),

    # Kap 31 — Vesper Erkenntnis (ersetzt Alt-32)
    make_event("31", ["erkenntnis", "schlüssel"],
               "Vesper: 4:33 + Gezeiten = Varens Atem",
               pov="Kap 31 · Vesper",
               detail="Jemand auf der anderen Seite atmet. Die Schemen kommen mit jedem Ausatmen. 4:33 ist nicht die Frequenz des Risses — es ist die Frequenz von etwas DAHINTER.",
               tags=["Erkenntnis: Jemand lebt auf der anderen Seite", "Tschechow: 4:33 = Varen"]),

    # Kap 32 — Nacht vor der Schwelle
    make_event("32", ["schlüssel"],
               "Die Vier entscheiden sich fuer den Durchgang",
               pov="Kap 32 · Alle",
               detail="Letzte Nacht in Vael. Vesper und Jara haben das Ritual uebersetzt. Runa bittet dazuzubleiben: 'Ich komme mit.'",
               tags=["Schluesselereignis: Entscheidung"]),
]

# ---- Akt 4 — Das Portal --------------------------------------------------
NEUE_EVENTS += [
    # Kap 33 — Letzte Bluete / Vier im Steinkreis (ersetzt Alt-34)
    make_event("33", ["erotik", "schlüssel"],
               "Alphina und Sorel kuessen sich im Steinkreis — der Garten blueht",
               pov="Kap 33 · Alphina",
               detail="Sorel haelt zum ersten Mal ihre Hand UNGEBETEN. 'Darf ich?' Kontrolle faellt. Die ganze Hoehle blueht. Runa folgt unbemerkt.",
               tags=["Beziehung: Alphina + Sorel — Zaertlichkeit"]),

    # Kap 34 — Portal oeffnet sich, Durchgang (ersetzt Alt-35)
    make_event("34", ["portal", "schlüssel"],
               "Portal oeffnet sich — Vier (plus Runa) gehen durch",
               pov="Kap 34 · Sorel",
               detail="Ritual. Vier Resonanzen. Das Portal bleibt 4:33 offen. Sorel zuerst. Runa stolpert im letzten Moment durch. Fuenf in Moragh, nicht vier.",
               tags=["Portal", "Schluesselereignis: Durchgang"]),

    # Kap 35 — Varens Begegnung (ersetzt Alt-36)
    make_event("35", ["begegnung", "schlüssel"],
               "Varen begegnet Alphina — 1423er Thalassisch, Hand an ihr Kinn",
               pov="Kap 35 · Alphina",
               figuren=["Alphina", "Varen"],
               intensitaet="intim",
               ort="Moragh, am Portal",
               detail="'Eure Resonanz. Ich hab sie durch den Riss erspueret. Ueber vierhundert Jaehrlein.' Bindungsmagie haelt sie. 4:33 war nie die Frequenz des Risses — es war Varens Signatur.",
               tags=["Erste Begegnung: Alphina + Varen", "Erkenntnis: Varens 1423er Thalassisch"]),

    # Kap 36 — Sorels Tod (ersetzt Alt-37)
    make_event("36", ["tod", "schlüssel"],
               "Sorel stirbt — Varens Abwehr, unterlassene Rettung",
               pov="Kap 36 · Alphina",
               detail="Sorel stellt sich zwischen Varen und Alphina. Varens Bindungsmagie trifft ihn voll. Varen KOENNTE helfen — tut es nicht. Deckt die Augen zu, fluestert ein Moragh-Wort. Alphinas Explosion: Dornen, Wurzeln, weisse Blumen auf Sorels Koerper.",
               tags=["Tod: Sorel", "Schluesselereignis: Alphinas Ausbruch"]),

    # Kap 38 — Maren: Elke spricht Thalassisch (ersetzt Alt-39)
    make_event("38", ["begegnung", "schlüssel"],
               "Elke findet die Gruppe — 1423er Thalassisch",
               pov="Kap 38 · Maren",
               figuren=["Alphina", "Vesper", "Maren", "Runa", "Elke"],
               intensitaet="bekannt",
               ort="Moragh, Elkes Garten",
               detail="Elke kennt Varen. Ist schockiert, dass er sich zurueckgezogen hat. Dasselbe alte Thalassisch — weil er es von IHR gelernt hat.",
               tags=["Erste Begegnung: Die Gruppe + Elke"]),

    # Kap 39 — Alphinas Rachschwur
    make_event("39", ["erkenntnis"],
               "Alphinas Trauer wird Hass — Dornen wachsen zum ersten Mal",
               pov="Kap 39 · Alphina",
               detail="Um sie herum waechst ein Kreis aus Dornen, nicht Farnen. Zum ersten Mal. Ihr Hass veraendert ihre Resonanz.",
               tags=["Tschechow: Alphinas Dornen"]),

    # Kap 40 — Epilog Vael (ersetzt Alt-41)
    make_event("40", ["schlüssel"],
               "Vael ohne die Fuenf — der Riss versiegt, Anomalien enden",
               pov="Kap 40 · Nebencharaktere",
               detail="Nebel lichtet sich. Grauwe fliesst vorwaerts. Farne stehen still. Halvard schreibt seinen Bericht — das einzige schriftliche Zeugnis. Jara archiviert Runas Flugblaetter daneben. Das Boot wartet, drei Viertel fertig.",
               tags=["Epilog Buch 1"]),
]


# =============================================================================
# MAIN
# =============================================================================

def main():
    with open(ZEITLEISTE, encoding="utf-8") as f:
        z = json.load(f)

    m10 = z["monate"][10]
    thal = m10["events"]["thalassien"]

    # 1) Kap-Nummern korrigieren (Alt -> Neu)
    renamed = 0
    for ev in thal:
        kap = ev.get("kapitel")
        if kap in KAP_RENUM:
            ev["kapitel"] = KAP_RENUM[kap]
            # pov-Feld ggf mit aktualisieren
            if "pov" in ev:
                pov = ev["pov"]
                # "Kap 15 · Vesper+Maren" -> "Kap 14 · Vesper+Maren"
                for old, new in KAP_RENUM.items():
                    if f"Kap {old} " in pov:
                        ev["pov"] = pov.replace(f"Kap {old} ", f"Kap {new} ")
                        break
            renamed += 1

    # 2) Neue Events hinzufuegen (dedupliziert via (kapitel, titel))
    existing_keys = {(e.get("kapitel"), e.get("titel")) for e in thal}
    added = 0
    for ev in NEUE_EVENTS:
        key = (ev["kapitel"], ev["titel"])
        if key not in existing_keys:
            thal.append(ev)
            existing_keys.add(key)
            added += 1

    # 3) Sortieren nach tz_tag, dann nach Kap-Reihenfolge
    # Lesereihenfolge aus status.json
    with open(REPO / "buch" / "status.json", encoding="utf-8") as f:
        status = json.load(f)
    reihenfolge = []
    for akt in status["buch1"]["akte"]:
        reihenfolge.extend(akt["kapitel"])
    pos_map = {k: i for i, k in enumerate(reihenfolge)}

    def sortkey(e):
        tag = e.get("tz_tag", 999)
        kap = e.get("kapitel", "")
        pos = pos_map.get(kap, 999)
        return (tag, pos)

    thal.sort(key=sortkey)
    m10["events"]["thalassien"] = thal

    # 4) Zurueckschreiben
    with open(ZEITLEISTE, "w", encoding="utf-8") as f:
        json.dump(z, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"OK: {renamed} Events umnummeriert, {added} neue Events hinzugefuegt")
    print(f"    thalassien-Events in monat[10] jetzt: {len(thal)}")


if __name__ == "__main__":
    main()
