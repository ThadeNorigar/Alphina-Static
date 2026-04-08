"""
Buch 3 — Schluesselereignisse in zeitleiste.json einpflegen.

Buch 3 spannt ein paar Moragh-Monate aber ~300 Thalassien-Jahre (2250).
Nur monat[15] ist verfuegbar — alle Events dort.

Kap-Nummern: Buch-3-intern (41-80), praefixiert mit "B3-".
"""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
ZEITLEISTE = REPO / "buch" / "zeitleiste.json"


def ev(kap, typen, titel, pov=None, welt="moragh", **kwargs):
    e = {
        "tz": None,
        "mz": None,
        "kapitel": f"B3-{kap}",
        "typen": typen,
        "titel": titel,
    }
    if pov:
        e["pov"] = pov
    e.update(kwargs)
    e["_welt"] = welt
    return e


# =============================================================================
# BUCH 3 — alle 4 Akte, die wichtigsten Momente
# =============================================================================

EVENTS = [
    # ---- AKT I: Zwei Welten -------------------------------------------------
    ev("41", ["schlüssel"],
       "Maren, alt, am Schwellenforschungsinstitut — 2250 Thalassien, Expedition wird vorbereitet",
       pov="B3 Kap 41 · Maren", welt="thalassien", mz=5.0,
       detail="Dreihundert Jahre Thalassien-Zeit seit Buch 2 Ende. Maren weiss, Hands die nicht mehr schliessen. Das Institut: Glas und Stahl neben dem Steinkreis. Ihr Name steht am Gebaeude.",
       tags=["Schluesselereignis: Institut etabliert"]),

    ev("42", ["erkenntnis"],
       "Alphina + Varen: erste Quellen-Reparatur — die Quelle zuckt",
       pov="B3 Kap 42 · Alphina", mz=5.1,
       detail="Wurzeln tief in den toten Quellenkern. Alphinas Resonanz als Herzschrittmacher. Ein einzelnes Pochen. Noch nicht genug — aber der Beweis: es ist moeglich.",
       tags=["Erkenntnis: Quellen-Reparatur funktioniert"]),

    ev("43", ["schlüssel", "tschechow"],
       "Vesper bei den Thar — autonome Bestien, das Imperium waechst",
       pov="B3 Kap 43 · Vesper", mz=5.12,
       detail="Vier autonome Magitech-Bestien patrouillieren die Ankunftsstadt. Die Thar-Kommandantin plant etwas — Bauplan den Vesper nicht sieht. 'Etwas das mich nervoes macht. Und ich werde nicht nervoes.' (Nyr)",
       tags=["Tschechow: Thar-Plaene"]),

    ev("45", ["tschechow"],
       "Talven verteilt geerntete Resonanz — Held mit dunkler Brille",
       pov="B3 Kap 45 · Talven", mz=5.15,
       detail="Marktplatz, hundert Menschen. Er verteilt Dosen geernteter Magie. Applause, Jubel. Sein linkes Auge milchig. Die Brille 'gegen die Sonne'.",
       tags=["Tschechow: Talvens Preis"]),

    ev("46", ["portal", "schlüssel"],
       "Die Expedition geht durch das Portal — 15 Menschen mit 2250er Technik",
       pov="B3 Kap 46 · Maren", welt="thalassien", mz=5.2,
       detail="Resonanz-Verstaerker, trainierte Operatoren. Portal oeffnet sich — 4:33. Maren am Ufer, alt, weiss, allein. Nickt zum letzten. Wartet.",
       tags=["Portal", "Schluesselereignis: Expedition"]),

    ev("47", ["erkenntnis"],
       "Zweite Quellen-Reparatur — die Quelle pocht regelmaessig",
       pov="B3 Kap 47 · Alphina+Varen", mz=5.25,
       detail="Varens Nasenbluten. Er zahlt, Alphina nicht. Dornen statt Farne. 'Das sind zwei. Zwei von vier.'"),

    ev("48", ["schlüssel"],
       "Die Thar uebernehmen Thalassien-Technik — KI-gesteuerte Bestien, Kessler wird autonom",
       pov="B3 Kap 48 · Vesper+Nyr", mz=5.28,
       detail="Die Expedition kommt durch. Thar-Kommandantin sieht die Container. Innerhalb von Tagen: KI-Modul in Kessler. 'Das ist Kessler. Ohne mich.'",
       tags=["Schluesselereignis: Tech-Magie-Fusion"]),

    ev("I10", ["tschechow", "erkenntnis"],
       "Iven + Generator: Elektrizitaets-Resonanz entdeckt",
       pov="B3 I10 · Iven", mz=5.3,
       detail="Iven, 17, beruehrt einen Generator. Leistung verdoppelt. Der Computer flackert. Moragh-Preis: Kribbeln, Schwindel. Er zahlt, Alphina nicht.",
       tags=["Tschechow: Iven als Interface"]),

    ev("50", ["tschechow"],
       "Alphinas Hain welkt — jemand erntet ihre Resonanz systematisch",
       pov="B3 Kap 50 · Alphina", mz=5.35,
       detail="Die Baeume am Rand des Schlaf-Hains: welkend. 'Wer nimmt meine Resonanz?' Varen: 'Jemand der glaubt er hat ein Recht darauf.'"),

    # ---- AKT II: Das Imperium -----------------------------------------------
    ev("51", ["schlüssel"],
       "Autonome Bestien patrouillieren — die Thar werden zum Imperium",
       pov="B3 Kap 51 · Vesper", mz=5.4,
       detail="Schwarm-Schemen (Tausende Mikro-Schemen, KI-koordiniert). Temporal-KI mit Vespers Muster-Resonanz. 'Du bist unser wertvollstes Werkzeug.' Werkzeug — das Wort."),

    ev("53", ["schlüssel"],
       "Alphina konfrontiert Talven im toten Hain — er hat Recht und Unrecht",
       pov="B3 Kap 53 · Alphina+Talven", mz=5.45,
       detail="Talven nimmt die Brille ab. Beide Augen milchig. 'Der Preis ist FAIR. Zum ersten Mal in der Geschichte von Moragh ist der Preis fair.' Alphina hat keine Antwort — weil er Recht hat und Unrecht.",
       tags=["Schluesselereignis: Talven-Konfrontation"]),

    ev("54", ["schlüssel"],
       "Nyr findet die Resonanz-Kaefig-Plaene — Menschen an Maschinen, Dauerbetrieb",
       pov="B3 Kap 54 · Nyr", mz=5.48,
       detail="Metallklemmen. Infusionsleitungen. 20 Plaetze fuer Resonanz-Begabte. Nicht freiwillig. Nyr kennt den Unterschied: Pilotin ist Wahl, das hier ist Kaefig.",
       tags=["Schluesselereignis: Nyr erkennt den Kaefig"]),

    ev("56", ["erkenntnis"],
       "Dritte Quellen-Reparatur — die aelteste Quelle pocht",
       pov="B3 Kap 56 · Alphina+Varen", mz=5.5,
       detail="Bund-Patrouillen. Alphina und Varen muessen fliehen. Die dritte Quelle pocht — schwach, fragil, aber lebendig. Drei von vier."),

    ev("I11", ["tod"],
       "Elke stirbt im Garten — an Alter, nicht Magie",
       pov="B3 I11 · Elke", mz=5.52,
       detail="Leise, auf dem Stein den sie selbst geformt hat. 'Die Farne brauchen weniger Wasser als die Moragh-Pflanzen.' Varen fluestert das Wort — dasselbe das er ueber Sorels Augen fluesterte. Alphina versteht es diesmal.",
       tags=["Tod: Elke"]),

    ev("60", ["schlüssel"],
       "Talvens Bruch — gibt die Resonanz zurueck, wird halb blind",
       pov="B3 Kap 60 · Talven", mz=5.53,
       detail="Am Grab. Der Stein antwortet nicht. Er hoert auf zu ernten. Gibt zurueck. Zweites Auge milchig. Am Morgen: ein Grashalm im toten Hain.",
       tags=["Schluesselereignis: Talvens Busse"]),

    ev("I12", ["erkenntnis"],
       "Varen: 'Der Riss ist das Problem' — erste Saat der Loesung",
       pov="B3 I12 · Varen", mz=5.55,
       detail="Die Quellen-Reparatur reicht nicht. Der Bund zerstoert schneller als wir reparieren. Die Thar bauen schneller als wir verstehen. Die Riss-Quelle muss zerstoert werden.",
       tags=["Erkenntnis: Riss-Quelle als Ziel"]),

    # ---- AKT III: Ueberlaeufer ----------------------------------------------
    ev("61", ["schlüssel"],
       "Nyr + Vesper verlassen die Thar — das Wort 'Werkzeug' kippt",
       pov="B3 Kap 61 · Nyr+Vesper", mz=5.6,
       detail="Nyr zeigt den Kaefig-Bauplan. Vesper sagt 'effizient', Nyr schlaegt auf den Tisch. 15 Sekunden Entscheidung. Sie nehmen Kessler (kein KI-Modul), Daten, gehen.",
       tags=["Schluesselereignis: Ueberlauf"]),

    ev("63", ["schlüssel", "erkenntnis"],
       "Alphina repariert ihre eigene zerstoerte Quelle — die vierte",
       pov="B3 Kap 63 · Alphina+Varen", mz=5.65,
       detail="Die Quelle die sie in Buch 2 absichtlich zerstoert hat. Vernarbt, ihre Signatur im Stein eingebrannt. Alphina weint. Wo die Traenen den Boden beruehren: Moos. Vier von vier.",
       tags=["Schluesselereignis: Alphinas Schuld-Reparatur"]),

    ev("64", ["begegnung"],
       "Nyr + Vesper kommen zu Varens Quartier — Alphina empfaengt sie",
       pov="B3 Kap 64 · Vesper+Nyr", mz=5.68,
       figuren=["Alphina", "Vesper", "Nyr", "Varen"],
       intensitaet="vertraut",
       detail="Alphina: 'Ich weiss was du bringst. Setz dich. Varen hat Tee.' Iven am Generator. Talven blind am Rand. 'Gerechtigkeit. Die falsche Art.'",
       tags=["Schluesselereignis: Gruppe vereint"]),

    ev("65", ["schlüssel"],
       "Der Plan: die Riss-Quelle zerstoeren, Portal permanent schliessen",
       pov="B3 Kap 65 · Varen", mz=5.7,
       detail="'Ich waehle Moragh. Fuer immer. Kein Zurueck.' Alphina. Thalassien verliert alle Magie. Die Thar verlieren den Tech-Zugang. Iven, Talven bieten Unterstuetzung.",
       tags=["Schluesselereignis: Der Plan"]),

    ev("66", ["begegnung"],
       "Runa konfrontiert Alphina — Feuer gegen Dornen",
       pov="B3 Kap 66 · Runa", mz=5.72,
       figuren=["Runa Kvist", "Alphina"],
       intensitaet="intim",
       detail="Die Druckerin jagt Vesper und Nyr, findet Alphina. Patt. 'Moragh zahlt. Das weisst du.' Runa senkt die Klinge. Laesst sie im Boden stecken. Dornen huellen sie ein. Runa geht.",
       tags=["Beziehung: Runa + Alphina — Konfrontation"]),

    ev("69", ["erkenntnis"],
       "Alphina versteht Varens Wort — es bedeutet 'geh', nicht Befehl, Erlaubnis",
       pov="B3 Kap 69 · Alphina+Varen", mz=5.74,
       detail="Dasselbe Wort das er ueber Sorels Augen gefluestert hatte. 'Der Unterschied,' sagt Alphina, 'bin ich.'",
       tags=["Erkenntnis: Das Wort"]),

    # ---- AKT IV: Die Quelle -------------------------------------------------
    ev("71", ["schlüssel"],
       "Annaeherung an die Thar-Festung — Iven stoert die Ley-Linien",
       pov="B3 Kap 71 · Vesper", mz=5.8,
       detail="Vesper ohne Temporal-KI, nur Muster-Sinn. Iven am Generator. Nasenbluten. 'Nicht aufhoeren.'"),

    ev("72", ["schlüssel"],
       "Nyr auf Kessler — Durchbruch durch die Mauer, gegen autonome Bestien",
       pov="B3 Kap 72 · Nyr", mz=5.82,
       detail="Drei Ramm-Versuche. Kessler gegen fuenf autonome Bestien. Pilotin gegen KI. Die Pilotin gewinnt."),

    ev("75", ["schlüssel"],
       "Talven kalibriert die Riss-Quelle blind — praezise, genug",
       pov="B3 Kap 75 · Iven+Talven", mz=5.85,
       detail="Iven stoert das Imperium-Nervensystem. Talven fuehlt die Riss-Quelle, markiert den Kippunkt mit zitternden Fingern. Blind, praezise, der Buesser der sein Wissen einsetzt.",
       tags=["Schluesselereignis: Kalibrierung"]),

    ev("76", ["portal", "schlüssel", "tod"],
       "Alphina zerstoert die Riss-Quelle — das Portal schliesst sich permanent",
       pov="B3 Kap 76 · Alphina", mz=5.88,
       detail="Dieselbe Handlung wie in Buch 2. Anderer Mensch. In Thalassien fallen die Farne um, alle gleichzeitig. Die Glasplatte hoert auf zu vibrieren. In Moragh: der Riss heilt. Alphina lebt.",
       tags=["Schluesselereignis: Das Finale", "Portal", "Tod: Riss-Quelle"]),

    ev("I15", ["tod"],
       "Maren: Stille in Vael — das Meer riecht nur nach Salz",
       pov="B3 I15 · Maren", welt="thalassien", mz=5.9,
       detail="Die Farne stehen still. Die Sensoren zeigen Null. Die vestigiale Resonanz: weg. 'Alphina. Du hast es getan.' Marens Lebenswerk in Akten, auf dem Gebaeude. Ein Institut fuer etwas das nicht mehr existiert.",
       tags=["Epilog: Maren allein"]),

    ev("77", ["hintergrund"],
       "Die Thar-Festung im Chaos — ohne Ley-Linien-Netzwerk stagniert das Imperium",
       pov="B3 Kap 77 · Varen+Alphina", mz=5.92,
       detail="'Es ist vorbei. Das Portal bleibt geschlossen. Eure Bestien brauchen Ersatzteile die nicht kommen.' 'Verhandelt. Oder verarmt.'"),

    ev("78", ["erotik"],
       "Vesper + Nyr — frei, ohne KI, ohne Muster-Zwang",
       pov="B3 Kap 78 · Vesper+Nyr", mz=5.93,
       figuren=["Vesper", "Nyr"],
       intensitaet="intim",
       detail="'Bereust du es?' 'Jeden Tag.' 'Und?' 'Und ich wuerde es nicht wieder tun.' Nyr presst ihn an die Mauer. 'Was machen wir jetzt?' 'Keine Ahnung. Zum ersten Mal.'",
       tags=["Beziehung: Vesper + Nyr"]),

    ev("80", ["schlüssel"],
       "Alphina + Varen in Elkes Garten — der Garten, die Dornen, der Blick",
       pov="B3 Kap 80 · Alphina+Varen", mz=5.95,
       detail="Tage spaeter. Elkes Bank. Pflanzen aus zwei Welten. Dornen und Farne und Stein. 'Kein Zurueck.' 'Nein.' 'Elke hatte Recht. Es war gut. Das alles.' Sein Blick der nicht fragt.",
       tags=["Epilog Moragh"]),

    ev("EP", ["schlüssel"],
       "Epilog: Drei Bilder — Vael still, die Stadt mit Talven als Lehrer, Moragh heilt",
       pov="B3 EP · Alle", mz=6.0,
       detail="Vael: ein Kind beruehrt einen Farn, nichts passiert. Stadt: Talven unterrichtet Warnung, blind. Moragh: Alphina und Varen auf der Bank, Dornen, Buch im 1423er Thalassisch. Reparierte Quellen pochen. 'Die Welten sind zwei. Der Riss ist geschlossen. Die Quelle haelt.'",
       tags=["Epilog: Ende der Trilogie"]),
]


def main():
    with open(ZEITLEISTE, encoding="utf-8") as f:
        z = json.load(f)

    monat = z["monate"][15]
    existing_keys = set()
    for bucket in ("thalassien", "moragh"):
        for e in monat["events"].get(bucket, []):
            existing_keys.add((e.get("kapitel"), e.get("titel")))

    added = 0
    for raw in EVENTS:
        welt = raw["_welt"]
        clean = {k: v for k, v in raw.items() if not k.startswith("_")}
        key = (clean["kapitel"], clean["titel"])
        if key in existing_keys:
            continue
        monat["events"].setdefault(welt, [])
        monat["events"][welt].append(clean)
        existing_keys.add(key)
        added += 1

    with open(ZEITLEISTE, "w", encoding="utf-8") as f:
        json.dump(z, f, ensure_ascii=False, indent=2)
        f.write("\n")

    thal = len(monat["events"].get("thalassien", []))
    mor = len(monat["events"].get("moragh", []))
    print(f"OK: {added} Buch-3-Events hinzugefuegt")
    print(f"  monat[15] ({monat.get('label','-')})  thal={thal}  mor={mor}")


if __name__ == "__main__":
    main()
